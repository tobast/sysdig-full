open Ast

let link program =
  let labels_index = Hashtbl.create 17 in
  ignore (List.fold_left
	(fun i instr -> match instr.instr with
	  | Label l -> Hashtbl.add labels_index l i; i
	  | _ -> i + 1) 0 program);
  let not_label = List.filter (fun instr ->
	 match instr.instr with | Label _ -> false | _ -> true) program in
  List.map (fun instr ->
	 match instr.instr with
	 | JMP l -> let i = Hashtbl.find labels_index l in
				{ instr = Move (MOV, 0, { value = ExplVal i;
										  shift = {
											shiftInstr = LSL;
											shiftVal = 0 } } );
				  cond = instr.cond;
				  setFlags = false }
	 | _ -> instr) not_label

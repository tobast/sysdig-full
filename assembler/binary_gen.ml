open Ast

(* dans la suite, on obtient l'instr, le carry et si il faut set les flags *)

let arith_op_instr = function
  | ADD -> (0b0000L, 0L, true)
  | ADC -> (0b0000L, 1L, true)
  | SUB -> (0b1000L, 0L, true)
  | SBC -> (0b1000L, 1L, true)
  | RSB -> (0b0010L, 0L, true)
  | RSC -> (0b0010L, 1L, true)
  | AND -> (0b0110L, 0L, true)
  | EOR -> (0b0100L, 0L, true)
  | ORR -> (0b0101L, 0L, true)
  | BIC -> (0b1110L, 0L, true)

let mem_op_instr = function
  | LDR -> (0b1001L, 0L, false)
  | STR -> (0b1011L, 0L, false)

let mov_op_instr = function
  | MOV -> (0b0000L, 0L, false)
  | MVN -> (0b1100L, 0L, false)

let comp_op_instr = function
  | CMP -> (0b1000L, 0L, true)
  | CMN -> (0b0000L, 0L, true)
  | TST -> (0b0110L, 0L, true)
  | TEQ -> (0b0100L, 0L, true)

(* dans la suite, on donne dans l'ordre : 
    - (instr, useCarry, setFlags)
	- destRegister
	- op1
	- isOp1Filled
	- op2
	- writeResult *)

let code_instr_separate = function
  | Arith(op, reg_dest, reg_op1, op2) 	->
     (arith_op_instr op, reg_dest, reg_op1, 0L, op2, 1L)
  | Compare(op, reg_op1, op2) 			->
     (comp_op_instr op, 0, reg_op1, 0L, op2, 0L)
  | Move(op, reg_dest, op2) 			->
     (mov_op_instr op, reg_dest, 0, 1L, op2, 1L)
  | Memory(op, reg_mem, op2) 			->
     (mem_op_instr op, reg_mem, reg_mem, 0L, op2, 1L)
  | _ -> assert false

let bool_to_bin = function
  | true  -> 1L
  | false -> 0L

let condType_to_int = function
  | EQ -> 0L
  | NE -> 1L
  | CS -> 2L
  | CC -> 3L
  | MI -> 4L
  | PL -> 5L
  | VS -> 6L
  | VC -> 7L
  | HI -> 8L
  | LS -> 9L
  | GE -> 10L
  | LT -> 11L
  | GT -> 12L
  | LE -> 13L
  | AL -> 14L
  | NV -> 15L

let op2_value = function
  | ExplVal n -> (0L, Int64.of_int n)
  | RegVal n  -> (1L, Int64.of_int n)

let shift_op_instr  = function
  | LSL -> 0L
  | LSR -> 2L
  | ASR -> 3L

let op2_bin op2 =
  let (isReg, value) = op2_value op2.value in
  let shift_opcode = shift_op_instr (op2.shift.shiftInstr) in
  let shift_val = Int64.of_int (op2.shift.shiftVal) in
  let res = ref(0L) in
  res := Int64.logor (!res) isReg ;
  res := Int64.logor (!res) (Int64.shift_left value 1) ;
  res := Int64.logor (!res) (Int64.shift_left shift_opcode 17) ;
  res := Int64.logor (!res) (Int64.shift_left shift_val 19) ;
  !res

let code_instr instr =
  let ((bin_instr, carry, flags), destRegister, op1, op1Filled, op2, write) =
     code_instr_separate instr.instr in
  let setFlags = bool_to_bin (flags && instr.setFlags) in
  let res = ref(0L) in
  let cond = condType_to_int instr.cond in
  res := Int64.logor (!res) cond ;
  res := Int64.logor (!res) (Int64.shift_left bin_instr 4) ;
  res := Int64.logor (!res) (Int64.shift_left write 8) ;
  res := Int64.logor (!res) (Int64.shift_left carry 9) ;
  res := Int64.logor (!res) (Int64.shift_left setFlags 10) ;
  res := Int64.logor (!res) (Int64.shift_left (Int64.of_int destRegister) 11) ;
  res := Int64.logor (!res) (Int64.shift_left (Int64.of_int op1) 15) ;
  res := Int64.logor (!res) (Int64.shift_left op1Filled 19) ;
  res := Int64.logor (!res) (Int64.shift_left (op2_bin op2) 20) ;
  !res

let binary_gen prog = List.map code_instr prog

{

exception Internal_error of string
exception Lexical_error of string

open Lexing
open Parser

let newline lexbuf =
	let pos = lexbuf.lex_curr_p in
	lexbuf.lex_curr_p <-
		{ pos with pos_lnum = pos.pos_lnum + 1; pos_bol = pos.pos_cnum }

let readConstant (base:int) cst =
	let inRange first last digit =
		digit >= first && digit <= last in
	let valOf first digit =
		(int_of_char digit) - (int_of_char first) in
	let digitVal digit =
		if inRange '0' '9' digit then
			valOf '0' digit
		else if inRange 'a' 'f' digit then
			(valOf 'a' digit) + 10
		else if inRange 'A' 'F' digit then
			(valOf 'A' digit) + 10
		else
			raise (Internal_error ("Unexpected character " ^
					(String.make 1 digit)^" while processing a base-"^
					(string_of_int base)^" number."))
	in
	let rec pow base = function
	| 0 -> 1
	| 1 -> base
	| n ->
		let x = pow base (n/2) in
		x * x * (if n mod 2 = 0 then 1 else base) in

	let strlen = String.length cst in
	if pow base strlen > (1 lsl 16) then
		raise (Lexical_error "Explicit constant is too large.");

	let rec doRead cNum = function
	| n when n = strlen -> cNum
	| n -> doRead (cNum * base + (digitVal (cst.[n]))) (n+1) in
	doRead 0 0

let readRegister regid =
	let out = int_of_string regid in
	if out < 0 || out > 15 then
		raise (Lexical_error ("Undefined register %r"^regid^"."));
	out

let readTextInstr =
	let instrList = [
		"ADD",	TinstrADD;
		"ADC",	TinstrADC;
		"SUB",	TinstrSUB;
		"SBC",	TinstrSBC;
		"RSB",	TinstrRSB;
		"RSC",	TinstrRSC;
		"AND",	TinstrAND;
		"EOR",	TinstrEOR;
		"ORR",	TinstrORR;
		"BIC",	TinstrBIC;
		"CMP",	TinstrCMP;
		"CMN",	TinstrCMN;
		"TST",	TinstrTST;
		"TEQ",	TinstrTEQ;
		"MOV",	TinstrMOV;
		"MVN",	TinstrMVN;
		"LDR",	TinstrLDR;
		"STR",	TinstrSTR;
		"JMP",	TinstrJMP;
		"LSL",	TinstrLSL;
		"LSR",	TinstrLSR;
		"ASR",	TinstrASR
		] in
	let flagsList = [
		"EQ",	TflagEQ;
		"NE",	TflagNE;
		"HS",	TflagCS;
		"CS",	TflagCS;
		"LO",	TflagCC;
		"CC",	TflagCC;
		"MI",	TflagMI;
		"PL",	TflagPL;
		"VS",	TflagVS;
		"VC",	TflagVC;
		"HI",	TflagHI;
		"LS",	TflagLS;
		"GE",	TflagGE;
		"LT",	TflagLT;
		"GT",	TflagGT;
		"LE",	TflagLE;
		"AL",	TflagAL;
		"NV",	TflagNV
		] in
	let instrHT = Hashtbl.create 17 in
		List.iter (fun (x,y) -> Hashtbl.add instrHT x y) instrList;
	let flagsHT = Hashtbl.create 17 in
		List.iter (fun (x,y) -> Hashtbl.add flagsHT x y) flagsList;

	(fun ident ->
		let strLen = String.length ident in
		if strLen < 3 then
			raise (Lexical_error ("Unbound identifier "^ident));
		
		let first3 = String.sub ident 0 3 in
		let instrname = (try
				Hashtbl.find instrHT first3
			with Not_found ->
				raise (Lexical_error ("Unknown instruction: "^first3))
			) in
		
		let rec identEndMatch len fpos = (match len with
			| 0 -> []
			| 1 ->
				if ident.[fpos] = 'S' then
					[ Tsetflags ]
				else
					raise (Lexical_error ("Expected nothing or 'S' at the \
							end of"^ident))
			| 2 ->
				(try
					[ Hashtbl.find flagsHT (String.sub ident fpos 2) ]
				with Not_found ->
					raise (Lexical_error ("Invalid conditionnal in "^ident))
				)
			| 3 ->
				(identEndMatch 2 fpos) @ (identEndMatch 1 (fpos+2))
			| _ ->
				raise (Lexical_error ("Instruction is waaay too long: "^ident))
			) in
		instrname :: (identEndMatch (strLen-3) 3)
	)
}

let whitespace = [' ' '\t']
let digits = [ '0'-'9' ]
let hexdigits = [ '0'-'9' 'A'-'F' 'a'-'f' ]
let bits = ['0'-'1']
let alpha = ['a'-'z' 'A'-'Z']
let alphaUp = ['A'-'Z']

rule tokens = parse
| '\n'						{ newline lexbuf ; [ Tendl ] }
| whitespace+				{ tokens lexbuf }
| ','						{ [ Tcomma ] }
| "#0x"(hexdigits+ as num)	{ [ Tval(readConstant 16 num) ] }
| "#0b"(bits+ as num)		{ [ Tval(readConstant 2 num) ] }
| '#'(digits+ as num)		{ [ Tval(readConstant 10 num) ] }
| "%r"(digits+ as regid)	{ [ Treg(readRegister regid) ] }
| (alpha+ as lab) ':'		{ [ Tlabel(lab) ] }
| (['a'-'z'] alpha+ as lab)	{ [ Tident(lab) ] }
| alphaUp+ as ident			{ readTextInstr ident }
| eof						{ [ Teof ] }
| _ as c					{ raise (Lexical_error ("Unexpected character "^
								(String.make 1 c)^".")) }

{
let token =
	let buffer = ref [] in
	(fun lexbuf ->
		if !buffer = [] then
			buffer := tokens lexbuf;
		let out = List.hd !buffer in
		buffer := List.tl !buffer ;
		out
	)
}

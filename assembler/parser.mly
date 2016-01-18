{
	open Ast
}

%token TinstrADD|TinstrADC|TinstrSUB|TinstrSBC|TinstrRSB|TinstrRSC|TinstrAND|
	TinstrEOR|TinstrORR|TinstrBIC|TinstrCMP|TinstrCMN|TinstrTST|TinstrTEQ|
	TinstrMOV|TinstrMVN|TinstrLDR|TinstrSTR|TinstrJMP|TinstrLSL|TinstrLSR|
	TinstrASR
%token TflagEQ|TflagNE|TflagCS|TflagCS|TflagCC|TflagCC|TflagMI|TflagPL|TflagVS|
	TflagVC|TflagHI|TflagLS|TflagGE|TflagLT|TflagGT|TflagLE|TflagAL|TflagNV
%token Tendl | Tcomma
%token <int> Treg
%token <int> Tval
%token <string> Tlabel

%start prgm
%type <Ast.prgm> prgm

%%

prgm:
| instrs = separated_list(instr, Tendl)			{ instrs }
;

instr:
| ins = arithOp ; cnd = cond ; sf = setflags ;
	dest=Treg; Tcomma; o1=Treg; Tcomma; o2=op2
								{ { instr = Arith(ins,dest,o1,o2) ;
								    cond = cnd ;
								    setFlags = sf } }
| ins = compOp ; cnd = cond ; sf = setflags ;
	o1=Treg; Tcomma; o2=op2
								{ { instr = Compare(ins,o1,o2) ;
								    cond = cnd ;
								    setFlags = sf } }
| ins = moveOp ; cnd = cond ; sf = setflags ;
	dest=Treg; Tcomma; o2=op2
								{ { instr = Move(ins,o1,o2) ;
								    cond = cnd ;
								    setFlags = sf } }
| ins = memOp ; cnd = cond ; sf = setflags ;
	o1=Treg; Tcomma; o2=op2
								{ { instr = Memory(ins,o1,o2) ;
								    cond = cnd ;
								    setFlags = sf } }
| ins = TinstrJMP ; cnd = cond ; lab = Tident
								{ { instr = JMP(lab) ;
								    cond = cnd ;
								    setFlags = false } }
| lab = Tlabel					{ { instr = Label(lab) ;
									cond = AL ;
									setFlags = false } }

arithOp:
| TinstrADD		{ ADD }
| TinstrADC		{ ADC }
| TinstrSUB		{ SUB }
| TinstrSBC		{ SBC }
| TinstrRSB		{ RSB }
| TinstrRSC		{ RSC }
| TinstrAND		{ AND }
| TinstrEOR		{ EOR }
| TinstrORR		{ ORR }
| TinstrBIC		{ BIC }
compOp:
| TinstrCMP		{ CMP }
| TinstrCMN		{ CMN }
| TinstrTST		{ TST }
| TinstrTEQ		{ TEQ }
moveOp:
| TinstrMOV		{ MOV }
| TinstrMVN		{ MVN }
memOp:
| TinstrLDR		{ LDR }
| TinstrSTR		{ STR }

op2:
| v = Tval ; sh = bshifter			{ { value = ExplVal(v) ; shift = sh }}
| r = Treg ; sh = bshifter			{ { value = RegVal(r) ; shift = sh }}

bshifter:
| 									{ { shiftInstr= LSL ; shiftVal = 0} }
| Tcomma ; op=shiftOp ; v = Tval	{ { shiftInstr= op ; shiftVal = v} }

shiftOp:
| TinstrLSL							{ LSL }
| TinstrLSR							{ LSR }
| TinstrASR							{ ASR }

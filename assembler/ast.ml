
type label = string

type reg = int

type op2val = ExplVal of int | RegVal of reg
type shiftOp = LSL | LSR | ASR
type barrelShift = {
	instr : shiftOp ;
	shiftVal : int
}

type op2 = {
	value : op2val ;
	shift : barrelShift
}

type arithOp = ADD | ADC | SUB | SBC | RSB | RSC | AND | EOR | ORR | BIC
type compOp = CMP | CMN | TST | TEQ
type moveOp = MOV | MVN
type memOp = LDR  | STR

type instrType =
	Arith of arithOp * reg * reg * op2 |
	Compare of compOp * reg * op2 |
	Move of moveOp * reg * op2 |
	Memory of memOp * reg * op2 |
	JMP of label |
	Label of label

type condType = EQ|NE|CS|CC|MI|PL|VS|VC|HI|LS|GE|LT|GT|LE|AL|NV

type instruction = {
	instr : instrType ;
	cond : condType ;
	setFlags : bool
}


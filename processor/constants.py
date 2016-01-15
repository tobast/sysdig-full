""" Contains the constants used all around the project """

class OPCODE_FRAME :
	conditionnal = 1
	instruction = 5
	writeResult = 9
	useCarry = 10
	setFlags = 11
	destRegister = 12
	op1 = 16
	isOp1Filled = 20
	op2 = 21

class FLAGS_POSITION:
	N = 1
	Z = 2
	C = 3
	V = 4

class REGISTERS:
	pc = 0
	number = 16

class INSTRUCTIONS_FORMAT:
	ADD = 0b0000
	SUB = 0b1000
	RSB = 0b0010
	AND = 0b0110
	EOR = 0b0100
	ORR = 0b0101
	BIC = 0b1110

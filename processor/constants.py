""" Contains the constants used all around the project """

class OPCODE_FRAME :
	conditionnal = 1
	instuction = 5
	writeResult = 9
	useCarry = 10
	setFlags = 11
	destRegister = 12
	op1 = 16
	isOp1Filled = 20
	op2 = 21
	memAddr = 46

class FLAGS_POSITION:
	N = 1
	Z = 2
	C = 3
	V = 4

class REGISTERS:
        pc = 0
        number = 16

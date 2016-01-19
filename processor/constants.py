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
	inputs = [1]
	outputs = [0, 1, 2, 3]

class INSTRUCTIONS_FORMAT:
	ADD = 0b0000
	SUB = 0b1000
	RSB = 0b0010
	AND = 0b0110
	EOR = 0b0100
	ORR = 0b0101
	BIC = 0b1110
	LDR = 0b1001
	STR = 0b1011

class OP2_FRAME:
	isRegister = 1
	value = 2 # register name or explicit 16-bits constant
	shift_opcode = 18
	shift_val = 20
class OP2_SHIFT_OPCODE:
	LSL = 0b00
	LSR = 0b10
	ASR = 0b11


#!/usr/bin/python3
# -*- coding: utf-8 -*-

import alu
import constants
import opcodeGetter
import netlist as nl

def main():
	### OPCODE_GETTER ###
	class opcodeGetPin:
		i_pctr = fresh(64)
		i_flagValue = fresh(1)
		o_flagSelect = fresh(4)
		o_opcode = fresh(64)

	opcodeGetter.opcodeGetter(opcodeGetPin.i_pctr,\
		opcodeGetPin.i_flagValue,\
		opcodeGetPin.o_flagSelect,\
		opcodeGetPin.o_opcode)
	
	### ALU ###
	class aluPin:
		i_opcode = opcodeGetPin.o_opcode,
		i_op1 = fresh(64)
		i_op2 = fresh(64)
		i_carryFlag = fresh(1)
		o_val = fresh(64)
		o_flags = fresh(4)

	alu.alu(aluPin.i_opcode,\
		aluPin.i_op1,\
		aluPin.i_op2,\
		aluPin.i_carryFlag,\
		aluPin.o_val,\
		aluPin.o_flags)

	### REGISTERS ###
	class registersPin:
		i_setVal = SELECT(constants.OPCODE_FRAME.writeResult,\
			opcodeGetPin.o_opcode)
		i_reg1addr = fresh(4)
		i_reg2addr = fresh(4)
		i_value = aluPin.o_val
		o_reg1 = fresh(64)
		o_reg2 = fresh(64)
		o_pctr = opcodeGetPin.i_pctr

	registers.registers(
		registersPin.i_opcode,\
		registersPin.i_setVal,\
		registersPin.o_reg1,\
		registersPin.o_reg2,\
		registersPin.o_pctr)
	
	### FLAGS ###
	class flagsPin:
		i_flags = aluPin.o_flags
		i_flagWrite =
			SELECT(constants.OPCODE_FRAME.setFlags, opcodeGetPin.o_opcode)
		i_flagSelect = opcodeGetPin.o_flagSelect
		o_flagVal = opcodeGetPin.i_flagValue
		o_flagsOut = fresh(4)
	
	SELECT(constants.FLAGS_POSITION.C, flagsPin.o_flagsOut, aluPin.i_carryFlag)

	flags.flags(
		i_flags,\
		i_flagWrite,\
		i_flagSelect,\
		o_flagVal,\
		o_flagsOut)

	### WE'RE DONE! ###
	nl.print_netlist()

if __name__ == '__main__':
	main()

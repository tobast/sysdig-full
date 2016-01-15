#!/usr/bin/python3
# -*- coding: utf-8 -*-

import alu
import flags
import op1processor
import op2processor
import opcodeGetter
import registers

import constants
from netlist import *

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
		i_instr = SLICE(constants.OPCODE_FRAME.instruction,\
				constants.OPCODE_FRAME+3, opcodeGetPin.o_opcode)
		i_useCarry = SELECT(constants.OPCODE_FRAME.useCarry,
				opcodeGetPin.o_opcode)
		i_op1 = fresh(64)
		i_op2 = fresh(64)
		i_carryFlag = fresh(1)
		o_val = fresh(64)
		o_flags = fresh(4)

	alu.alu(aluPin.i_instr,\
		aluPin.i_useCarry,\
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
		i_destReg = SLICE(constants.OPCODE_FRAME.destRegister,\
			constants.OPCODE_FRAME.destRegister+3, opcodeGetPin.o_opcode)
		i_value = aluPin.o_val
		o_reg1 = fresh(64)
		o_reg2 = fresh(64)
		o_pctr = opcodeGetPin.i_pctr

	registers.registers(
		registersPin.i_setVal,\
		registersPin.i_reg1addr,\
		registersPin.i_reg2addr,\
		registersPin.i_destReg,\
		registersPin.i_value,\
		registersPin.o_reg1,\
		registersPin.o_reg2,\
		registersPin.o_pctr)

	### OP1_PROCESSOR ###
	class op1processorPin:
		i_op1 = SLICE(constants.OPCODE_FRAME.op1,constants.OPCODE_FRAME.op1+3,\
				opcodeGetPin.o_opcode)
		i_op1cst = SELECT(constants.OPCODE_FRAME.isOp1Filled,\
				opcodeGetPin.o_opcode)
		i_regVal = registersPin.o_reg1
		o_reqAddr = registersPin.reg1addr
		o_val = aluPin.i_reg1
	
	op1processor.op1processor(
		op1processorPin.i_op1,\
		op1processorPin.i_op1cst,\
		op1processorPin.i_regVal,\
		op1processorPin.o_reqAddr,\
		op1processorPin.o_val)

	### OP2_PROCESSOR ###
	class op2processorPin:
		i_op2 = SLICE(constants.OPCODE_FRAME.op1,constants.OPCODE_FRAME.op1+3,\
				opcodeGetPin.o_opcode)
		i_regVal = registersPin.o_reg2
		o_reqAddr = registersPin.reg2addr
		o_val = aluPin.i_reg2

	op2processor.op2processor(
		op2processorPin.i_op2,\
		op2processorPin.i_regVal,\
		op2processorPin.o_reqAddr,\
		op2processorPin.o_val)
	
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

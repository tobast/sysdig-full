import constants
from netlist import *
import helpers as hel

def opcodeGetter(i_pctr, i_flagValue, o_flagSelect=None, o_opcode=None):
	if o_flagSelect == None:
		o_flagSelect = fresh(4)
	if o_opcode == None:
		o_opcode = fresh(64)

	romOut = ROM(16, 64, SLICE(1, 16, i_pctr))
	SLICE(constants.OPCODE_FRAME.conditionnal,
		constants.OPCODE_FRAME.conditionnal+3,
		romOut,
		o_flagSelect)
	
	maskWrite = hel.expandedCst_1bit(constants.OPCODE_FRAME.writeResult, 1,\
			i_flagValue)
	maskFlags = hel.expandedCst_1bit(constants.OPCODE_FRAME.setFlags, 1,\
			i_flagValue)

	return AND(romOut, AND(maskWrite, maskFlags), o_opcode)

import constants
from netlist import *
import helpers as hel

def flagsMem(i_flags, i_flagWrite, o_flagsOut):
	""" Handles the actual flags storage """
	writeArray = hel.wire_expand(4, i_flagWrite)
	regOutWire = fresh(4)
	flagsInput = MUX(regOutWire, i_flags, writeArray)
	REG(flagsInput, regOutWire)
	return regOutWire
	
def cndSelector(flags, i_flagSelect, o_flagVal):
	sBits = [-1] + [ SELECT(k, i_flagSelect) for k in range(1, 5) ]
	z = SELECT(constants.FLAGS_POSITION.Z, flags)
	c = SELECT(constants.FLAGS_POSITION.C, flags)
	n = SELECT(constants.FLAGS_POSITION.N, flags)
	v = SELECT(constants.FLAGS_POSITION.V, flags)
	notZ = NOT(z)
	ge = OR(AND(n,v), NOT(OR(n,v)))
	
	preB1 = \
		MUX(\
			MUX(\
				MUX(z,c,sBits[2]),\
				MUX(n,v,sBits[2]),\
				sBits[3]),\
			MUX(\
				MUX(AND(c,notZ), ge, sBits[2]),\
				MUX(AND(ge, notZ), CONST(1), sBits[2]),\
				sBits[3]),\
			sBits[4])
	
	return XOR(sBits[1], preB1, o_flagVal)

def flags(i_flags, i_flagWrite, i_flagSelect, o_flagVal, o_flagsOut):
	push_context("flags")
	o_flagsOut = flagsMem(i_flags, i_flagWrite, o_flagsOut)
	o_flagVal = cndSelector(o_flagsOut, i_flagSelect, o_flagVal)
	pop_context()
	return o_flagVal, o_flagsOut

import helpers as hel
from netlist import *

def op1processor(i_op1, i_op1cst, i_regVal, o_reqAddr, o_val):
	o_reqAddr = WIRE(i_op1, o_reqAddr) # TODO implement WIRE
	zero = hel.wire_expand(64, CONST(0))
	o_val = MUX(i_regVal, zero, hel.wire_expand(64, i_op1cst))
	return o_reqAddr, o_val

import constants
from netlist import *
import helpers as hel

def leftShifter(i_inputVal, i_shiftCode, wei):
	return CONCAT(hel.wire_expand(1<<wei, CONST(0)),\
		SLICE(1, 64 - (1<<wei), i_inputVal))
def rightShifter(i_inputVal, i_shiftCode, wei):
	extendWith = AND(SELECT(64, i_inputVal), SELECT(1, i_shiftCode))
	return CONCAT(SLICE((1<<wei) + 1, 64, i_inputVal),\
			hel.wire_expand(1<<wei, extendWith))

def barrelShifter(shifter, i_inputVal, i_shiftCode, i_shiftVal, o_val = None):
	push_context("shifter")
	group_pins([i_inputVal, i_shiftCode, i_shiftVal], [o_val])
	interWires = [i_inputVal] + [ fresh(64) for k in range(5) ] + [ o_val ]
	for shiftWeight in range(6):
		shifted = shifter(interWires[shiftWeight], i_shiftCode, shiftWeight)
		interWires[shiftWeight+1] = \
		    MUX(interWires[shiftWeight], shifted,\
		        hel.wire_expand(64, SELECT(shiftWeight+1, i_shiftVal)),\
		        interWires[shiftWeight+1])
	group_output(interWires[-1])
	pop_context()
	return interWires[-1]

def op2processor(i_op2, i_reqVal, o_reqAddr = None, o_val = None):
	push_context("op2processor")
	group_pins([i_op2, i_reqVal], [o_reqAddr, o_val])
	o_reqAddr = SLICE(constants.OP2_FRAME.value, constants.OP2_FRAME.value + 3,\
			i_op2, o_reqAddr)
	numCst = CONCAT(\
			SLICE(constants.OP2_FRAME.value, constants.OP2_FRAME.value + 15,\
				i_op2),\
			hel.wire_expand(64-16, CONST(0)))
	interValue = MUX(\
			numCst,\
			i_reqVal,\
			hel.wire_expand(64, SELECT(constants.OP2_FRAME.isRegister, i_op2)))
	
	shiftCode = SLICE(constants.OP2_FRAME.shift_opcode,\
				constants.OP2_FRAME.shift_opcode + 1, i_op2)
	shiftVal = SLICE(constants.OP2_FRAME.shift_val,\
				constants.OP2_FRAME.shift_val + 5, i_op2)
	o_val = MUX(
		barrelShifter(leftShifter,interValue, shiftCode, shiftVal),\
		barrelShifter(rightShifter,interValue, shiftCode, shiftVal),\
		hel.wire_expand(64,SELECT(2, shiftCode)),\
                o_val)
	group_outputs([o_reqAddr, o_val])
	pop_context()
	return o_reqAddr, o_val

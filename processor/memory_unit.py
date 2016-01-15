import netlist as nl
import helpers
from constants import INSTRUCTIONS_FORMAT

UNUSED_ADDR_ZERO = True

def memory_unit(instr, value, addr, result = None):
	is_memory = nl.AND(nl.SELECT(1, instr), nl.SELECT(4, instr))
	we = nl.AND(is_memory, nl.SELECT(3, instr))
	addr = nl.SLICE(1, 16, addr)
	if UNUSED_ADDR_ZERO:
		addr = nl.AND(addr, helpers.wire_expand(16, is_memory))
	uu = nl.fresh(64)
	return nl.RAM(16, 64, addr, we, nl.WIRE(addr, uu), value, result)
	

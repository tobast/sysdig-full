import netlist as nl
import helpers
from constants import INSTRUCTIONS_FORMAT

UNUSED_ADDR_ZERO = True

def memory_unit(instr, value, addr, result = None):
	is_memory = nl.AND(nl.SELECT(instr, 1), nl.SELCT(instr, 4))
	we = nl.AND(is_memory, nl.SELECT(instr, 3))
	addr = nl.SLICE(1, 16, addr)
	if UNUSED_ADDR_ZERO:
            addr = nl.AND(addr, helpers.wire_expand(16, is_memory))
	return nl.RAM(16, 64, addr, we, addr, value, result)
	

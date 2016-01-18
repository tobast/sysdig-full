import netlist as nl
import helpers as hel

def result_selector(instr, mem_result, alu_result, output = None):
	is_STR = nl.AND(nl.SELECT(1, instr), nl.SELECT(4, instr))
	return nl.MUX(alu_result, mem_result, hel.wire_expand(64, is_STR), output)


import netlist as nl
import helpers as hel

def result_selector(instr, mem_result, alu_result, output = None):
	nl.push_context("result_selector")
	nl.group_pins([instr, mem_result, alu_result], [output])
	is_STR = nl.AND(nl.SELECT(1, instr), nl.SELECT(4, instr))
	output = nl.MUX(alu_result, mem_result, hel.wire_expand(64, is_STR), output)
	nl.group_output(output)
	nl.pop_context()
	return output

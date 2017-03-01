import netlist as nl
import helpers as hel

def half_adder(source1, source2, s = None, c = None):
	"""peut prendre les fils de sortie ou les générer"""
	c = nl.AND(source1, source2, c)
	s = nl.XOR(source1, source2, s)
	return (s, c)

def incr(n, source, s = None, c = None):
	"""renvoie source + 1"""
	if n == 1:
		s, c = half_adder(nl.SELECT(1, source), nl.CONST(1), s, c)
		return s, c
	s_temp, c_temp = incr(n - 1, nl.SLICE(1, n-1, source))
	s1, c = half_adder(nl.SELECT(n, source), c_temp, None, c)
	s = nl.CONCAT(s_temp, s1, s)
	return (s, c)

def full_adder(source1, source2, c_in, s = None, c_out = None):
	r1 = nl.AND(source1, source2)
	r2 = nl.OR(source1, source2)
	r3 = nl.AND(r2, c_in)
	c_out = nl.OR(r1, r3, c_out)
	s1 = nl.XOR(source1, source2)
	s = nl.XOR(s1, c_in, s)
	return (s, c_out) 

def full_adder_n(n, nappe1, nappe2, c_in, need_fl_V, \
		  s = None, c_out = None, fl_V = None):
	if n == 1:
		s, c_out = full_adder(nl.SELECT(1, nappe1), nl.SELECT(1, nappe2), c_in)
		return (s, c_out, fl_V)
	s_temp, c_temp, fl_V_useless = full_adder_n(n - 1, nappe1, nappe2, \
			c_in, False)
	s1, c_out = full_adder(nl.SELECT(n, nappe1), nl.SELECT(n, nappe2), c_temp, None, c_out)
	s = nl.CONCAT(s_temp, s1, s)
	if need_fl_V:
		fl_V = nl.XOR(c_temp, c_out, fl_V)
	return (s, c_out, fl_V)

def alu(instr, useCarry, op1, op2, carryFlag, val = None, flags = None):
	nl.push_context("alu")
	nl.group_pins([instr, useCarry, op1, op2, carryFlag], [val, flags])
	"""calcule les opposés de op1 et op2 si (et seulement si) nécessaire"""
	op1_1 = nl.XOR(op1, hel.wire_expand(64, nl.SELECT(2, instr)))
	op2_1 = nl.XOR(op2, hel.wire_expand(64, nl.SELECT(4, instr)))
	"""calcule la sortie pour les opérations arithmétiques seulement"""
	c_in = nl.MUX(nl.OR(nl.SELECT(4, instr), nl.SELECT(2, instr)), \
		carryFlag, useCarry)
	arith, flag_C, flag_V = full_adder_n(64, op1_1, op2_1, c_in, True)
	"""calcule la sortie pour les opérations booléennes seulement"""
	eor = nl.XOR(op1, op2_1)
	orr = nl.OR(op1, op2_1)
	oand = nl.AND(op1, op2_1)
	boo_1 = nl.MUX(eor, orr, hel.wire_expand(64, nl.SELECT(1, instr)))
	boo = nl.MUX(boo_1, oand, hel.wire_expand(64, nl.SELECT(2, instr)))
	"""sélectionne la bonne sortie parmi les deux propositions"""
	val = nl.MUX(arith, boo, hel.wire_expand(64, nl.SELECT(3, instr)), val)
	"""détermine les flags"""
	n_flag_Z = hel.or_all(val)
	flag_Z = nl.NOT(n_flag_Z)
	flag_N = nl.SELECT(64, val)
	flags_1 = nl.CONCAT(flag_N, flag_Z)
	flags_2 = nl.CONCAT(flags_1, flag_C)
	flags = nl.CONCAT(flags_2, flag_V, flags)
	nl.group_outputs([val, flags])
	nl.pop_context()
	return (val, flags)

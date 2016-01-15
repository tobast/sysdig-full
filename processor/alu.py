import netlist as nl
import helpers as hel

def half_adder(source1, source2, s = None, c = None):
	"""peut prendre les fils de sortie ou les générer"""
	c = nl.AND(source1, source2, r)
	s = nl.XOR(source1, source2, s)
	return (r, s)

def incr(n, source, s = None, c = None):
	"""renvoie source = 1"""
	if n == 1:
		s, c = half_adder(nl.SELECT(1, source), nl.CONST(1), s, c)
		return s, c
	s_temp, c_temp = incr(n - 1, nl.SELECT(n, source))
	s1, c = half_adder(nl.SELECT(n, source), c_temp)
	s = nl.CONCAT(s_temp, s1)
	return (s, c)

def full_adder(source1, source2, c_in, s = None, c_out = None):
	r1 = nl.AND(source1, source2)
	r2 = nl.OR(source1, source2)
	r3 = nl.AND(r2, c_in)
	c_out = nl.OR(r1, r3)
	s1 = nl.XOR(source1, source2)
	s = nl.XOR(s1, c_in)
	return (s, c_out) 

def full_adder_n(n, nappe1, nappe2, c_in, need_fl_V, \
		  s = None, c_out = None, fl_Z = None, fl_V = None):
	if n == 1:
		s, c_out = full_adder(nl.SELECT(1, nappe1), nl.SELECT(1, nappe2), c_in)
		fl_Z = nl.NOT(s)
		return (s, c_out, fl_Z, fl_V)
	s_temp, c_temp = full_adder_n(n - 1, nappe1, nappe2, c_in, False)
	s1, c_out, fl_Z_1, fl_V_useless = full_adder(nl.SELECT(n, nappe1), \
		nl.SELECT(n, nappe2), c_temp)
	s = nl.CONCAT(s_temp, s1)
	fl_Z = nl.AND(nl.NOT(s1), fl_Z_1)
	if need_fl_V:
		fl_V = nl.XOR(c_temp, c_out)
	return (s, c_out, fl_Z, fl_V)

def alu(instr, useCarry, op1, op2, carryFlag, val = None, flags = None):
	op2_1 = nl.XOR(op2, hel.wire_expand(64, nl.SELECT(1, opcode)))
	c_in = nl.MUX(OR(nl.SELECT(1, opcode), SELECT(3,opcode)), \
		carryFlag, useCarry)
	adsu, flag_C, flag_Z, flag_V = full_adder_n(64, op1, op2_1, c_in, True)
	rs = full_adder_n(64, op1_1, op2, c_in, True)
	arith = nl.MUX(adsu, rs, hel.wire_expand(64, nl.SELECT(3, opcode))) 
	val = nl.MUX(arith, boo, hel.wire_expand(64, nl.SELECT(2, opcode)))
	flag_N = nl.SELECT(64, adsu)
	flags_1 = nl.CONCAT(flag_N, flag_Z)
	flags_2 = nl.CONCAT(flags_2, flag_C)
	flags = nl.CONCAT(flags_2, flag_V, flags)

import netlist as nl
import helpers
import alu
import constants

def register(data, write_enable, destr = None):
	n = nl.get_size(data)
	u = nl.fresh(n)
	destr = nl.REG(u, destr)
	write_n = helpers.wire_expand(n, write_enable)
	nl.MUX(destr, data, write_n, u)
	return destr

def register_pc(data, write_enable, destr = None):
	n = nl.get_size(data)
	u = nl.fresh(n)
	destr = nl.REG(u, destr)
	incremented, _ = alu.incr(n, destr)
	write_n = helpers.wire_expand(n, write_enable)
	nl.MUX(incremented, data, write_n, u)
	return destr

def mux_n(n, l, addr, destr = None):
	k = nl.get_size(l[0])
	if n == 1:
		return nl.MUX(l[0], l[1], helpers.wire_expand(k,
				nl.SELECT(1, addr)), destr)
	z = 1 << (n - 1)
	return nl.MUX(mux_n(n - 1, l[:z], addr), mux_n(n - 1, l[z:], addr),
		      helpers.wire_expand(k, nl.SELECT(n, addr)), destr)

def demux_n(n, l, source, addr):
	k = nl.get_size(source)
	u = helpers.wire_expand(k, nl.SELECT(n, addr))
	z = 1 << (n - 1)
	if n == 1:
		nl.AND(u, source, l[1])
		nl.AND(nl.NOT(u), source, l[0])
		return
	demux_n(n - 1, l[:z], nl.AND(nl.NOT(u), source), addr)
	demux_n(n - 1, l[z:], nl.AND(u, source), addr)

def registers(set_val, r1addr, r2addr, setaddr, value, r1 = None, r2 = None,
	      pc = None):
	n = nl.get_size(value)
	regs = []
	for i in range(constants.REGISTERS.number):
		write_enable = nl.fresh()
		if i == constants.REGISTERS.pc:
			pc = register_pc(value, write_enable, pc)
			reg = pc
		else:
			reg = register(value, write_enable)
		regs.append((write_enable, reg))
	addr_size = nl.get_size(r1addr)
	mux_n(addr_size, [r[1] for r in regs], r1addr, r1)
	mux_n(addr_size, [r[1] for r in regs], r2addr, r2)
	demux_n(addr_size, [r[0] for r in regs], set_val, setaddr)

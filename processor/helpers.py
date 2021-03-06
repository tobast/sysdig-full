import netlist as nl

def wire_expand(n, source, destr = None):
	"""Prend un fil, et retourne une nappe consistant en
	   n copies de ce fil (par exponentiation rapide)"""
	assert(n > 0)
	assert(destr == None or nl.get_size(destr) == n * nl.get_size(source))
	if n == 1 and destr == None:
		return source
	elif n == 1:
		return nl.WIRE(source, destr)
	nl.push_context("wire_expand")
	c = 1
	k = 0
	l = [source]
	bits = []
	m = n
	while 2 * c < n:
		l.append(nl.CONCAT(l[-1], l[-1]))
		if m % 2 == 1:
			bits.append(k)
		m //= 2
		c *= 2
		k += 1
	if 2 * c == n:
		nl.pop_context()
		return nl.CONCAT(l[-1], l[-1], destr)
	u = l[bits[0]]
	for i in range(1, len(bits)):
		u = nl.CONCAT(u, l[bits[i]])
	nl.pop_context()
	return nl.CONCAT(u, l[k], destr)

def or_all(source, destr = None):
        n = nl.get_size(source)
        if n == 1:
                return nl.WIRE(source, destr)
        nl.push_context("or_all")
        c = 1
        while 2 * c < n:
                c *= 2
        w = source
        if 2 * c > n:
                w = nl.CONCAT(wire_expand(2 * c - n, nl.CONST(0)), source)
        while c > 1:
                w = nl.OR(nl.SLICE(1, c, w), nl.SLICE(c + 1, 2 * c, w))
                c //= 2
        destr = nl.OR(nl.SLICE(1, c, w), nl.SLICE(c + 1, 2 * c, w), destr)
        nl.pop_context()
        return destr

def expandedCst_1bit(bitpos, cst, i_bitwire, o_out = None):
	""" Inserts a wire into a 64-sized array of `cst', replacing the wire at
	position `bitpos' with `i_bitwire' """
	if bitpos > 1:
		if bitpos == 64:
			lowOut = o_out
		else:
			lowOut = None
		lowWei = nl.CONCAT(wire_expand(bitpos-1, nl.CONST(cst)),\
				i_bitwire, lowOut)
	else:
		lowWei = nl.CONST(cst)
	
	if bitpos == 64:
		return lowWei
	return nl.CONCAT(lowWei, wire_expand(64-bitpos, nl.CONST(cst)), o_out)


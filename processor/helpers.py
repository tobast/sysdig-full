import netlist as nl

def wire_expand(n, source, destr = None):
	"""Prend un fil, et retourne une nappe consistant en
	   n copies de ce fil (par exponentiation rapide)"""
	assert(n > 0)
	assert(destr == None or nl.get_size(destr) == n * nl.get_size(source))
	if n == 1 and destr == None:
		return source
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
		return nl.CONCAT(l[-1], l[-1], destr)
	u = l[bits[0]]
	for i in range(1, len(bits)):
		u = nl.CONCAT(u, l[bits[i]])
	return nl.CONCAT(u, l[k], destr)

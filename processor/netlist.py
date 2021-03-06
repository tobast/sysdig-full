
vars = {}
instrs = []
inputs = []
outputs = []

context = ["l"]

def push_context(name):
	context.append(name)
def pop_context():
	context.pop()

var_id = 0
def fresh(num_bits = 1):
	"""Crée un nouveau fil, avec num_bits fils"""
	global var_id
	name = context[-1] + str(var_id)
	var_id += 1
	vars[name] = num_bits
	return name

def get_size(name):
	"""Retourne la taille de name"""
	return vars[name]

def input(name):
	"""Déclare name comme entrée"""
	inputs.append(name)

def output(name):
	"""Déclare name comme sortie"""
	outputs.append(name)

def CONST(value, destr = None):
	if destr == None:
		destr = fresh()
	assert(value == 0 or value == 1)
	instrs.append("{} = {}".format(destr, value))
	return destr

def WIRE(source, destr = None):
	if destr == None:
		return source
	assert(vars[source] == vars[destr])
	instrs.append("{} = {}".format(destr, source))
	return destr    

def REG(source, destr = None):
	if destr == None:
		destr = fresh(vars[source])
	assert(vars[source] == vars[destr])
	instrs.append("{} = REG {}".format(destr, source))
	return destr

def NOT(source, destr = None):
	if destr == None:
		destr = fresh(vars[source])
	assert(vars[source] == vars[destr])
	instrs.append("{} = NOT {}".format(destr, source))
	return destr

def OR(source1, source2, destr = None):
	if destr == None:
		destr = fresh(vars[source1])
	assert(vars[source1] == vars[source2] == vars[destr])
	instrs.append("{} = OR {} {}".format(destr, source1, source2))
	return destr

def AND(source1, source2, destr = None):
	if destr == None:
		destr = fresh(vars[source1])
	assert(vars[source1] == vars[source2] == vars[destr])
	instrs.append("{} = AND {} {}".format(destr, source1, source2))
	return destr

def XOR(source1, source2, destr = None):
	if destr == None:
		destr = fresh(vars[source1])
	assert(vars[source1] == vars[source2] == vars[destr])
	instrs.append("{} = XOR {} {}".format(destr, source1, source2))
	return destr

def NAND(source1, source2, destr = None):
	if destr == None:
		destr = fresh(vars[source1])
	assert(vars[source1] == vars[source2] == vars[destr])
	instrs.append("{} = NAND {} {}".format(destr, source1, source2))
	return destr

def MUX(source0, source1, choose, destr = None):
	if destr == None:
		destr = fresh(vars[source0])
	assert(vars[source0] == vars[source1] == vars[choose] == vars[destr])
	instrs.append("{} = MUX {} {} {}".format(destr, source0, source1, choose))
	return destr

def ROM(addr_size, word_size, addr, destr = None):
	if destr == None:
		destr = fresh(word_size)
	assert(vars[addr] == addr_size and vars[destr] == word_size)
	instrs.append("{} = ROM {} {} {}".format(destr, addr_size, word_size, addr))
	return destr

def RAM(addr_size, word_size, read_addr, write_enable, write_addr, data, \
		destr = None):
	if destr == None:
		destr = fresh(word_size)
	assert(vars[read_addr] == vars[write_addr] == addr_size)
	assert(vars[destr] == vars[data] == word_size)
	assert(vars[write_enable] == 1)
	instrs.append("{} = RAM {} {} {} {} {} {}".format(destr, addr_size,\
			word_size, read_addr, write_enable, write_addr, data))
	return destr

def CONCAT(source1, source2, destr = None):
	if destr == None:
		destr = fresh(vars[source1] + vars[source2])
	assert(vars[destr] == vars[source1] + vars[source2])
	instrs.append("{} = CONCAT {} {}".format(destr, source2, source1))
	return destr

def SLICE(i, j, source, destr = None):
	if destr == None:
		destr = fresh(j - i + 1)
	assert(vars[destr] == j - i + 1 and 1 <= i <= j <= vars[source])
	instrs.append("{} = SLICE {} {} {}".format(destr, vars[source] - j, vars[source] - i, source))
	return destr

def SELECT(index, source, destr = None):
	if destr == None:
		destr = fresh()
	assert(vars[destr] == 1 and 1 <= index <= vars[source])
	instrs.append("{} = SELECT {} {}".format(destr, vars[source] - index, source))
	return destr

def print_netlist():
	"""Affiche la netlist"""
	print("INPUT", ", ".join(inputs))
	print("OUTPUT", ", ".join(outputs))
	print("VAR")
	print("  " + ", ".join(name + " : " + str(size) for name, size in vars.items()))
	print("IN")
	print("\n".join(instrs))

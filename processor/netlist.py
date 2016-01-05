
vars = []
instrs = []
inputs = []
outputs = []

var_id = 0
def fresh(num_bits = 1):
    """Crée un nouveau fil, avec num_bits fils"""
    global var_id
    name = "l{}".format(var_id)
    var_id += 1
    vars.append((name, num_bits))
    return name

def input(name):
    """Déclare name comme entrée"""
    inputs.append(name)

def output(name):
    """Déclare name comme sortie"""
    outputs.append(name)

def REG(source, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = REG {}".format(destr, source))
    return destr

def NOT(source, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = NOT {}".format(destr, source))
    return destr

def OR(source1, source2, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = OR {} {}".format(destr, source1, source2))
    return destr

def AND(source1, source2, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = AND {} {}".format(destr, source1, source2))
    return destr

def XOR(source1, source2, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = XOR {} {}".format(destr, source1, source2))
    return destr

def NAND(source1, source2, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = NAND {} {}".format(destr, source1, source2))
    return destr

def MUX(source1, source2, choose, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = MUX {} {} {}".format(destr, source1, source2, choose))
    return destr

def ROM(addr_size, word_size, addr, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = ROM {} {} {}".format(destr, addr_size, word_size, addr))
    return destr

def RAM(addr_size, word_size, read_addr, write_enable, write_addr, data, \
        destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = RAM {} {} {} {} {} {}".format(destr, addr_size, word_size,
                                    read_addr, write_enable, write_addr, data))
    return destr

def CONCAT(source1, source2, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = CONCAT {} {}".format(destr, source1, source2))
    return destr

def SLICE(i, j, source, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = SLICE {} {} {}".format(destr, i, j, source))
    return destr

def SELECT(index, source, destr = None):
    if destr == None: destr = fresh()
    instrs.append("{} = SELECT {} {}".format(destr, index, source))
    return destr

def print_netlist():
    """Affiche la netlist"""
    print("INPUT", ", ".join(inputs))
    print("OUTPUT", ", ".join(outputs))
    print("VAR")
    print("  " + ", ".join(name + " : " + str(size) for name, size in vars))
    print("IN")
    print("\n".join(instrs))

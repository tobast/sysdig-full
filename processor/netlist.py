
vars = []
instrs = []
inputs = []
outputs = []

var_id = 0
def fresh(num_bits = 1):
    name = "l{}".format(var_id)
    var_id += 1
    vars.append((name, num_bits))
    return name

def input(name):
    inputs.append(name)

def output(name):
    outputs.append(name)

def REG(source, destr):
    instrs.append("{} = REG {}".format(destr, source))

def NOT(source, destr):
    instrs.append("{} = NOT {}".format(destr, source))

def OR(source1, source2, destr):
    instrs.append("{} = OR {} {}".format(destr, source1, source2))

def AND(source1, source2, destr):
    instrs.append("{} = AND {} {}".format(destr, source1, source2))

def XOR(source1, source2, destr):
    instrs.append("{} = XOR {} {}".format(destr, source1, source2))

def NAND(source1, source2, destr):
    instrs.append("{} = NAND {} {}".format(destr, source1, source2))

def MUX(source1, source2, choose, destr):
    instrs.append("{} = MUX {} {} {}".format(destr, source1, source2, choose))

def ROM(addr_size, word_size, addr, destr):
    instrs.append("{} = ROM {} {} {}".format(destr, addr_size, word_size, addr))

def RAM(addr_size, word_size, read_addr, write_enable, write_addr, data, destr):
    instrs.append("{} = RAM {} {} {} {} {} {}".format(destr, addr_size, word_size,
                                    read_addr, write_enable, write_addr, data))

def CONCAT(source1, source2, destr):
    instrs.append("{} = CONCAT {} {}".format(destr, source1, source2))

def SLICE(i, j, source, destr):
    instrs.append("{} = SLICE {} {} {}".format(destr, i, j, source))

def SELECT(index, source, destr):
    instrs.append("{} = SELECT {} {}".format(destr, index, source))

def print_netlist():
    print("INPUT", ", ".join(inputs))
    print("OUTPUT", ", ".join(outputs))
    print("VAR")
    print("  " + ", ".join(name + " : " + str(size) for name, size in vars))
    print("IN")
    print("\n".join(instrs))

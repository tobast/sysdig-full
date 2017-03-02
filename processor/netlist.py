import prettyprint


class Group:
    def __init__(self, name):
        self.inputs = []  # Pair (formal, actual)
        self.outputs = []  # idem
        self.instrs = []
        self.subgroups = []
        self.vars = {}
        self.foreignVars = {}
        self.name = name


rootGroup = Group('root')
curGroup = [rootGroup]

class PinNotFound(Exception):
    pass


class DuplicateWireName(Exception):
    pass


def push_context(name):
    curGroup.append(Group(name))
def pop_context():
    subGroup = curGroup.pop()
    curGroup[-1].subgroups.append(subGroup)


def isPinOfList(name, pinList):
    for (formal, actual) in pinList:
        if name == formal:
            return actual
    return None


def isPinOf(name, group):
    return isPinOfList(name, group.inputs + group.outputs)


def isInputOf(name, group):
    return isPinOfList(name, group.inputs)


def isOutputOf(name, group):
    return isPinOfList(name, group.outputs)


def findVar(name):
    if name in curGroup[-1].vars:
        return curGroup[-1].vars[name]
    if name in curGroup[-1].foreignVars:  # Pins
        return curGroup[-1].foreignVars[name]
    for child in curGroup[-1].subgroups:
        if isPinOf(name, child):
            return child.vars[isPinOf(name, child)]
#FIXME DEBUG
    for child in curGroup[-1].subgroups:
        print("Child {}: {} --> {}".format(child.name,
                                           child.inputs,
                                           child.outputs))
    print(curGroup[-1].inputs)
    print(curGroup[-1].foreignVars)
    print(curGroup[-1].vars)
    raise PinNotFound("Pin {} not found in {}{}".format(
        name, curGroup[-1].name,
        ' (child of {})'.format(curGroup[-2].name) if len(curGroup) > 1
            else ''))


var_id = 0
def fresh(num_bits = 1):
    """Crée un nouveau fil, avec num_bits fils"""
    global var_id
    name = curGroup[-1].name + str(var_id)
    var_id += 1
    curGroup[-1].vars[name] = num_bits
    return name

def get_size(name):
    """Retourne la taille de name"""
    return findVar(name)

def input(name):
    """Déclare name comme entrée"""
    rootGroup.inputs.append((name, name))


def declare_foreign(name):
    if name not in curGroup[-1].vars:
        topGrp = curGroup.pop()
        varLen = findVar(name)
        curGroup.append(topGrp)
        curGroup[-1].foreignVars[name] = varLen


def group_input(name):
    if (name, name) in curGroup[-1].inputs:
        return
    curGroup[-1].inputs.append((name, name))
    declare_foreign(name)


def group_inputs(names):
    for name in names:
        group_input(name)


def output(name):
    """Déclare name comme sortie"""
    rootGroup.outputs.append((name, name))


def group_output(name):
    if (name, name) in curGroup[-1].outputs:
        return
    if not name:
        return
    curGroup[-1].outputs.append((name, name))
    declare_foreign(name)


def group_outputs(names):
    for name in names:
        group_output(name)


def group_pins(inps, outs):
    group_inputs(inps)
    group_outputs(outs)


def CONST(value, destr = None):
    if destr == None:
        destr = fresh()
    assert(value == 0 or value == 1)
    curGroup[-1].instrs.append("{} = {}".format(destr, value))
    return destr

def WIRE(source, destr = None):
    if destr == None:
        return source
    assert(findVar(source) == findVar(destr))
    curGroup[-1].instrs.append("{} = {}".format(destr, source))
    return destr

def REG(source, destr = None):
    if destr == None:
        destr = fresh(findVar(source))
    assert(findVar(source) == findVar(destr))
    curGroup[-1].instrs.append("{} = REG {}".format(destr, source))
    return destr

def NOT(source, destr = None):
    if destr == None:
        destr = fresh(findVar(source))
    assert(findVar(source) == findVar(destr))
    curGroup[-1].instrs.append("{} = NOT {}".format(destr, source))
    return destr

def OR(source1, source2, destr = None):
    if destr == None:
        destr = fresh(findVar(source1))
    assert(findVar(source1) == findVar(source2) == findVar(destr))
    curGroup[-1].instrs.append("{} = OR {} {}".format(destr, source1, source2))
    return destr

def AND(source1, source2, destr = None):
    if destr == None:
        destr = fresh(findVar(source1))
    assert(findVar(source1) == findVar(source2) == findVar(destr))
    curGroup[-1].instrs.append("{} = AND {} {}".format(destr, source1, source2))
    return destr

def XOR(source1, source2, destr = None):
    if destr == None:
        destr = fresh(findVar(source1))
    assert(findVar(source1) == findVar(source2) == findVar(destr))
    curGroup[-1].instrs.append("{} = XOR {} {}".format(destr, source1, source2))
    return destr

def NAND(source1, source2, destr = None):
    if destr == None:
        destr = fresh(findVar(source1))
    assert(findVar(source1) == findVar(source2) == findVar(destr))
    curGroup[-1].instrs.append("{} = NAND {} {}".format(destr, source1, source2))
    return destr

def MUX(source0, source1, choose, destr = None):
    if destr == None:
        destr = fresh(findVar(source0))
    assert(findVar(source0) == findVar(source1) == findVar(choose) == findVar(destr))
    curGroup[-1].instrs.append("{} = MUX {} {} {}".format(
        destr, source0, source1, choose))
    return destr

def ROM(addr_size, word_size, addr, destr = None):
    if destr == None:
        destr = fresh(word_size)
    assert(findVar(addr) == addr_size and findVar(destr) == word_size)
    curGroup[-1].instrs.append("{} = ROM {} {} {}".format(
        destr, addr_size, word_size, addr))
    return destr

def RAM(addr_size, word_size, read_addr, write_enable, write_addr, data, \
        destr = None):
    if destr == None:
        destr = fresh(word_size)
    assert(findVar(read_addr) == findVar(write_addr) == addr_size)
    assert(findVar(destr) == findVar(data) == word_size)
    assert(findVar(write_enable) == 1)
    curGroup[-1].instrs.append("{} = RAM {} {} {} {} {} {}".format(
        destr, addr_size, word_size, read_addr, write_enable,
        write_addr, data))
    return destr

def CONCAT(source1, source2, destr = None):
    if destr == None:
        destr = fresh(findVar(source1) + findVar(source2))
    assert(findVar(destr) == findVar(source1) + findVar(source2))
    curGroup[-1].instrs.append("{} = CONCAT {} {}".format(
        destr, source2, source1))
    return destr

def SLICE(i, j, source, destr = None):
    if destr == None:
        destr = fresh(j - i + 1)
    assert(findVar(destr) == j - i + 1 and 1 <= i <= j <= findVar(source))
    curGroup[-1].instrs.append("{} = SLICE {} {} {}".format(
        destr, findVar(source) - j, findVar(source) - i, source))
    return destr

def SELECT(index, source, destr = None):
    if destr == None:
        destr = fresh()
    assert(findVar(destr) == 1 and 1 <= index <= findVar(source))
    curGroup[-1].instrs.append("{} = SELECT {} {}".format(
        destr, findVar(source) - index, source))
    return destr

def print_netlist():
    """Affiche la netlist"""
    allVars = {}
    allInstrs = []

    def walk(cGroup):
        nonlocal allVars
        nonlocal allInstrs

        for var in cGroup.vars.keys():
            if var in allVars:
                raise DuplicateWireName("{} (from {}) was already present"
                                        .format(var, cGroup.name))
        allVars.update(cGroup.vars)
        allInstrs += cGroup.instrs

        for sub in cGroup.subgroups:
            walk(sub)
    walk(rootGroup)


    print("INPUT", ", ".join(map(lambda x: x[0], rootGroup.inputs)))
    print("OUTPUT", ", ".join(map(lambda x: x[0], rootGroup.outputs)))
    print("VAR")
    print("  " + ", ".join(name + " : " + str(size)
                        for name, size in allVars.items()))
    print("IN")
    print("\n".join(allInstrs))


def print_isoml():
    prettyprint.toIsoML(rootGroup)

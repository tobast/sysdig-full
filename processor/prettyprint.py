'''
    Pretty-prints the circuit hierarchy to multiple possible output formats
'''


def toIsoML(group, indent=0):
    SHIFT_WIDTH = 2

    def line(msg):
        nonlocal indent
        print(' '*indent + msg)

    line('let {} ({}) -> ({}) {{'.format(
        group.name,
        ', '.join(map(lambda x: x[0], group.inputs)),
        ', '.join(map(lambda x: x[0], group.outputs))))
    indent += SHIFT_WIDTH

    for sub in group.subgroups:
        toIsoML(sub, indent)

    for instr in group.instrs:
        lval = instr.split('=')[0].strip()
        rvals = instr.split('=')[1].strip().split(' ')

        assert(len(rvals) > 0)
        if len(rvals) == 1:  # Wire
            line('{} = {}'.format(lval, rvals[0]))
        else:
            # More than one rval: rval[0] is the operator
            if rvals[0] in ['AND', 'OR', 'XOR', 'NOT']:  # No translation
                line('{} = {}'.format(lval, ' '.join(rvals)))
            elif rvals[0] == 'REG':
                assert(len(rvals) == 2)
                line('{} = DELAY {}'.format(lval, rvals[1]))
            elif rvals[0] == 'MUX':
                assert(len(rvals) == 4)
                choose = rvals[3]
                source0, source1 = rvals[1], rvals[2]
                line('{} = TRI {} {}'.format(lval, source1, choose))
                line('{} = TRI {} (NOT {})'.format(lval, source0, choose))
            elif rvals[0] in ['ROM', 'RAM']:
                # Not part of our description language. Should be OK this way?
                # FIXME maybe
                pass
            elif rvals[0] == 'SLICE':
                assert(len(rvals) == 4)
                line('{} = SLICE {} {} {}'.format(lval, rvals[3],
                                                  int(rvals[1]),
                                                  int(rvals[2]) + 1))
            elif rvals[0] == 'SELECT':
                assert(len(rvals) == 3)
                line('{} = SLICE {} {} {}'.format(lval, rvals[2],
                                                  int(rvals[1]),
                                                  int(rvals[1]) + 1))
            elif rvals[0] == 'CONCAT':
                assert(len(rvals) == 3)
                line('{} = MERGE {} {}'.format(lval, rvals[1], rvals[2]))
            else:
                raise Exception("Unknown operator {}.".format(rvals[0]))

    indent -= SHIFT_WIDTH
    line('}\n')

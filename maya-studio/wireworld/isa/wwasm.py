"""Tiny assembler for the WireWorld computer.

Source: list of strings.
  'label:'                 defines a code label at the next free register
  'MOV dst, src'           one instruction
  operands: R0..R63, a variable name (allocated after code), =number (constant pool),
            =@label (constant holding the label's address)
  'VAR name = value'       initialised variable
Code starts at R1.  Constants and variables follow the code.  Registers 53..63 are
special, so a program must end below 53 to fit the real machine; with big=True
the overflow goes to 64.. (only for logic tests in the emulator).
"""
import re

SPECIAL = set(range(53, 64))

def assemble(src, big=False, origin=1, data=None):
    """origin: first code register.  data: list of registers for constants/vars
    (default: right after the code)."""
    code, labels, vars_init = [], {}, {}
    for line in src:
        line = line.split(';')[0].strip()
        if not line: continue
        if line.endswith(':'):
            labels[line[:-1]] = len(code) + origin; continue
        if line.startswith('VAR'):
            m = re.match(r'VAR\s+(\w+)\s*=\s*(\S+)', line)
            vars_init[m.group(1)] = int(m.group(2), 0); continue
        m = re.match(r'MOV\s+(\S+)\s*,\s*(\S+)$', line)
        assert m, line
        code.append((m.group(1), m.group(2)))
    n = len(code)
    # allocate constants and variables
    pool, order = {}, []
    def need(op):
        if re.fullmatch(r'R\d+', op) or op in labels: return
        if op not in pool:
            pool[op] = None; order.append(op)
    for d, s in code:
        need(d); need(s)
    for v in vars_init:
        need(v)
    addr = n + origin
    def nextfree(a):
        while (a in SPECIAL) or a == 0: a += 1
        return a
    if data is None:
        for op in order:
            addr = nextfree(addr)
            pool[op] = addr; addr += 1
        last = addr - 1
    else:
        if len(order) > len(data):
            raise ValueError(f'{len(order)} data words but only {len(data)} slots: {order}')
        for op, a in zip(order, data):
            pool[op] = a
        last = n + origin - 1
    def reg(op):
        if re.fullmatch(r'R\d+', op): return int(op[1:])
        if op in labels: return labels[op]
        return pool[op]
    mem = {}
    for i, (d, s) in enumerate(code):
        mem[i + origin] = (reg(d), reg(s))
    for op, a in pool.items():
        if op.startswith('=@'): mem[a] = labels[op[2:]]
        elif op.startswith('='):
            v = int(op[1:], 0)
            mem[a] = (~(-v) & 0xFFFF) if v < 0 else v & 0xFFFF   # ones' complement negatives
        else: mem[a] = vars_init.get(op, 0)
    fits = last <= 52
    if not big and not fits:
        raise ValueError(f'program needs registers up to R{last}: does not fit (max R52)')
    return mem, labels, pool, last, n

def words(mem):
    """Encode for the real machine: instructions as (d<<8)|s."""
    return {a: ((v[0] << 8) | v[1]) if isinstance(v, tuple) else v for a, v in mem.items()}

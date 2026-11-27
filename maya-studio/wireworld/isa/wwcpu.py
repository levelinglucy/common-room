"""Instruction-level emulator of the Moore/Owen WireWorld computer, from quinapalus.com
(wires10 'The instruction set', wires11 'The final design').

One instruction: MOV Rd, Rs, coded as (d << 8) | s.  64 registers of 16 bits.
Special registers (read / write):
  R0  reads 0          / writes go to the display
  R53 reads R54 & ~R53 / plain
  R54 reads R53 & ~R54 / plain
  R55 reads 0          / plain
  R56 reads R55 if R56 != 0 else R57 / plain
  R57 reads 0          / plain
  R58 reads R58 rotated right 1 / plain
  R59 reads R59 rotated left 1  / plain
  R61 reads R60 + R61 (ones' complement, end-around carry) / plain
  R62 reads ~R62       / plain
  R63 reads PC         / write = branch, with one delay slot
PC is incremented after each fetch; execution starts at R1.
"""
M = 0xFFFF

def add1c(a, b):
    """Ones' complement add, end-around carry. The page says line 10 of the primes
    program 'always represents zero as plus zero'; a plain end-around adder would give
    3 + (-3) = 0xffff (minus zero), and then 3 is never found prime. The copper machine
    does find it, so here a sum of all ones is taken as +0: arithmetic mod 65535."""
    s = a + b
    while s >= M:
        s -= M
    return s

class CPU:
    def __init__(self, mem):
        self.r = [0] * 64
        for i, v in mem.items():
            self.r[i] = v & M
        self.pc = 1
        self.display = []      # (instruction index, value)
        self.n = 0             # instructions executed
        self.pending = None    # branch target waiting for the delay slot

    def read(self, s):
        r = self.r
        if s in (0, 55, 57): return 0
        if s == 53: return r[54] & ~r[53] & M
        if s == 54: return r[53] & ~r[54] & M
        if s == 56: return r[55] if r[56] else r[57]
        if s == 58: v = r[58]; return ((v >> 1) | ((v & 1) << 15)) & M
        if s == 59: v = r[59]; return ((v << 1) | (v >> 15)) & M
        if s == 61: return add1c(r[60], r[61])
        if s == 62: return ~r[62] & M
        if s == 63: return self.pc
        return r[s]

    def step(self):
        ins = self.r[self.pc]
        d, s = (ins >> 8) & 63, ins & 63
        self.pc = (self.pc + 1) & 63
        if self.pending is not None:   # the delay-slot instruction was just fetched
            self.pc, self.pending = self.pending, None
        v = self.read(s)
        self.n += 1
        if d == 0:
            self.display.append((self.n, v))
        elif d == 63:
            self.pending = v & 63
        else:
            self.r[d] = v

    def run(self, max_ins, stop=None):
        while self.n < max_ins:
            self.step()
            if stop and stop(self): break
        return self

def assemble(lines):
    """lines: list of (reg, value) where value is int or ('MOV', d, s)."""
    mem = {}
    for reg, v in lines:
        mem[reg] = (v[1] << 8) | v[2] if isinstance(v, tuple) else v
    return mem

# Fryers' primes program exactly as listed on quinapalus.com wires11 (hex column)
PRIMES_HEX = {1: 0x001e, 2: 0x361f, 3: 0x2021, 4: 0x3c22, 5: 0x3d23, 6: 0x3c3d, 7: 0x3d20,
    8: 0x3924, 9: 0x3725, 10: 0x383d, 11: 0x3f38, 12: 0x3d3d, 13: 0x3d3d, 14: 0x353d,
    15: 0x3926, 16: 0x3727, 17: 0x3836, 18: 0x3f38, 19: 0x3928, 20: 0x0020, 21: 0x3d20,
    22: 0x3c1e, 23: 0x3f29, 24: 0x203d, 30: 0x0002, 31: 0x7fff, 32: 0x0003, 33: 0x0003,
    34: 0xfffe, 35: 0xfffd, 36: 0x0014, 37: 0x000d, 38: 0x0009, 39: 0x0005, 40: 0x0015,
    41: 0x0004, 42: 0xfffc}
# note: the listing shows R32 = 0005 because it was a snapshot mid-run; at start it is 3
# (line 3 sets p = R33 = 3 anyway).

if __name__ == '__main__':
    c = CPU(PRIMES_HEX).run(40000)
    print([v for _, v in c.display][:30])

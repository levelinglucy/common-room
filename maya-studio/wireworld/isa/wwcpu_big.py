"""Same CPU as wwcpu.py but instructions may be (d, s) tuples and memory may extend
past R63 (registers 64.. behave as plain storage), for testing programs that do not
fit yet.  Semantics otherwise identical."""
from wwcpu import add1c, M

class BigCPU:
    def __init__(self, mem, size=128):
        self.r = [0] * size
        for i, v in mem.items():
            self.r[i] = v
        self.size = size
        self.pc = 1; self.n = 0; self.pending = None; self.display = []
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
        v = r[s]
        if isinstance(v, tuple): return ((v[0] << 8) | v[1]) & M
        return v
    def step(self):
        ins = self.r[self.pc]
        if isinstance(ins, tuple): d, s = ins
        else: d, s = (ins >> 8) & 63, ins & 63
        self.pc = (self.pc + 1) % self.size
        if self.pending is not None:
            self.pc, self.pending = self.pending, None
        v = self.read(s)
        self.n += 1
        if d == 0: self.display.append((self.n, v))
        elif d == 63: self.pending = v
        else: self.r[d] = v
    def run(self, max_ins, until_display=None):
        while self.n < max_ins:
            self.step()
            if until_display and len(self.display) >= until_display: break
        return self

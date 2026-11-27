"""both_bt + 'reach_out': a lone pair (hypha whose two ends both have degree 1) grows one 1.0 hypha
from a random end to a random organ outside the pair, after pruning, each tick. Registers itself in heal.CLS."""
import sys, random
sys.path.insert(0, '/home/sprite/maya-studio/memory')
import heal as H
B, M = H.B, H.M

class ReachOut:
    reached_out = 0
    def tick(self):
        r = super().tick()
        d = B.degree(self)
        for (a, b) in list(self.hyphae):
            if d[a] == 1 and d[b] == 1:
                end = self.rng.choice([a, b])
                far = self.rng.choice([n for n in self.nodes if n not in (a, b)])
                self.grow(end, far)
                d[end] += 1; d[far] += 1
                self.reached_out += 1
        return r

H.CLS['both_bt_ro'] = type('V', (ReachOut, B.BothBT), {})
H.CLS['both_bt_ro_heal'] = type('V', (H.Heal, ReachOut, B.BothBT), {})
H.CLS['base_ro'] = type('V', (ReachOut, M.Mycelium), {})

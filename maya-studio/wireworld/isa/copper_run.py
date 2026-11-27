"""Load a register image into the WireWorld computer and run it in copper.

usage (module): run(mem, gens, snap, tag) -> list of (number shown, first gen)
mem: {register: 16-bit word} for R1..R52 (unlisted registers are set to 0).
"""
import numpy as np, subprocess, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WW = os.path.join(HERE, '..')
sys.path.insert(0, HERE); sys.path.insert(0, WW)
from regmap import write_reg, G0
from decode_log import decode, events

ORDER = [tuple(o) for o in np.load(os.path.join(HERE, 'loop_order.npy'))]

def image(mem):
    g = np.load(G0).copy()
    for R in range(1, 53):
        write_reg(g, R, mem.get(R, 0) & 0xFFFF, ORDER)
    return g

def run(mem, gens, snap=100, tag='t', hold=3):
    g = image(mem)
    raw = f'/tmp/ww_{tag}.raw'
    g.astype(np.uint8).tofile(raw)
    log = f'/tmp/ww_{tag}.log'
    with open(log, 'w') as f:
        subprocess.run([os.path.join(WW, 'ww3'), raw, '905', '570', str(gens), str(snap),
                        os.path.join(WW, 'boxes.txt')], stdout=f, check=True)
    gs, shown = decode(log)
    return events(gs, shown, hold=hold), gs, shown

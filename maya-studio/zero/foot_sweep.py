"""How the corridor's reach depends on the foot's height (w=24 and w=32, foot 3w wide)."""
from strip_check import reach
for w in (24, 32):
    print(f"w={w}  w(w+4)/8={w*(w+4)/8:.0f}")
    for fh in (2, 4, 8, 12, 16, 20, 24, 32, 48, 80, 120):
        print(f"  foot_h {fh:<4} reach {reach(w, 700, 3*w, fh)}")

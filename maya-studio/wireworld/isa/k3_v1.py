"""Kaprekar's 3-digit routine (ends at 495) for the WireWorld computer, version 1.

Idea: digits are pulled out of N by repeated subtraction (100, 10, 1), like Fryers'
primes program, but each digit is counted in R59 by rotation, so it comes out as a
one-hot code 2^(d+1).  The three codes are OR-ed into W (kept inverted as NW, so one
AND-NOT per digit).  Then max - min = distance from W's lowest set bit to its highest:
walk a bit X upward from the lowest one, clearing W's bits as X passes them, adding 99
each step until nothing is left.  That sum is 99*(max-min) = the next number.
No sorting, no comparisons except the sign and zero tests.
(Repdigits would give 99 instead of 0; never reached from a non-repdigit start.)
"""
import sys
from wwasm import assemble
from wwcpu_big import BigCPU

def source(n0):
    return f"""
    MOV R61, N0
step:
    MOV R60, R0          ; so that reading R61 gives N itself
    MOV R0, R61          ; display N
    MOV NW, =0xFFFF      ; W = empty (stored inverted)
    MOV R55, =@r1
    MOV R63, =@div
    MOV R60, =-100       ; delay slot: divisor
r1:
    MOV R53, NW
    MOV R54, R59         ; one-hot code of the hundreds digit
    MOV NW, R54          ; NW &= ~code
    MOV R55, =@r2
    MOV R63, =@div
    MOV R60, =-10
r2:
    MOV R53, NW
    MOV R54, R59
    MOV NW, R54
    MOV R55, =@r3
    MOV R63, =@div
    MOV R60, =-1
r3:
    MOV R53, NW
    MOV R54, R59
    MOV NW, R54
    MOV R62, NW
    MOV R53, R62         ; R53 = W
    MOV R61, R62         ; R61 = W   (R60 is still -1)
    MOV R54, R61         ; R54 = W - 1
    MOV R59, R54         ; X = lowest set bit of W
    MOV R54, R54         ; R54 = lowest bit
    MOV R53, R54         ; Y = W without its lowest bit
    MOV R60, =99
    MOV R61, R0          ; acc = 0
    MOV R55, =@ml
    MOV R57, =@mx
ml:
    MOV R54, R59         ; X<<1
    MOV R59, R59         ; X <<= 1
    MOV R53, R54         ; Y &= ~X
    MOV R56, R54         ; Y (nonzero -> keep walking)
    MOV R63, R56
    MOV R61, R61         ; delay slot: acc += 99
mx:
    MOV R63, =@step
    MOV R60, R0          ; delay slot (harmless)
div:                     ; R61 = r, R60 = -D, R55 = return; leaves 2^q in R59
    MOV R57, =@dc
    MOV R59, =0x8000
    MOV R53, =0x7FFF
dl:
    MOV T, R61           ; T = r - D
    MOV R54, T
    MOV R56, R53         ; T & 0x8000
    MOV R63, R56         ; negative -> return, else -> dc
    MOV R59, R59         ; delay slot: q++
dc:
    MOV R63, =@dl
    MOV R61, T           ; delay slot: r = T
    VAR N0 = {n0}
""".split('\n')

def kaprekar3(n):
    d = sorted(f'{n:03d}')
    return int(''.join(d[::-1])) - int(''.join(d))

if __name__ == '__main__':
    mem, labels, pool, last, ncode = assemble(source(352), big=True)
    print(f'code {ncode} instructions, uses registers up to R{last}')
    bad, worst = 0, 0
    for n0 in range(1000):
        if len(set(f'{n0:03d}')) == 1: continue
        mem, *_ = assemble(source(n0), big=True)
        c = BigCPU(mem).run(200000, until_display=8)
        got = [v for _, v in c.display]
        want = [n0]
        while len(want) < 8: want.append(kaprekar3(want[-1]))
        if got != want: bad += 1; print('MISMATCH', n0, got, want)
        worst = max(worst, c.n)
    print('mismatches:', bad, ' max instructions for 8 displays:', worst)
    mem, *_ = assemble(source(352), big=True)
    c = BigCPU(mem).run(200000, until_display=5)
    print('352:', [(v, n) for n, v in c.display])

"""Kaprekar's 3-digit routine for the WireWorld computer, version 2: fits the machine.

Boot facts measured in copper (see notebook): after an image is written into R1..R52 of
primes.npy at gen 0, one stale instruction writes 0xFFFF into R12, then the machine
fetches R13, R14, ... one every 2304 gens.  So code lives in R13..R52 (40 words) and
constants in R1..R11 (11 words).  R12 is junk.

Algorithm as v1 (one-hot digit codes from repeated subtraction, OR-ed into W, then walk
from W's lowest bit to its highest adding 99).  Golf:
 - calls save their own return address: 'MOV R55, R63' in the jump's delay slot reads
   the address just after the slot (as in the emulator; to be confirmed in copper)
 - the division keeps the sign mask in R53 and tests T via R54 & ~R53... (see code)
 - the walk loop exits straight to the top.
"""
from wwasm import assemble
from wwcpu_big import BigCPU

SRC = """
    MOV R61, N0
    MOV R60, R0
step:
    MOV R0, R61          ; display N (R60 is 0 first time, 99 after: fixed below)
    MOV R53, =0x7FFF
    MOV NW, =0xFFFF
    MOV R57, =@dc
    MOV R59, =1
    MOV R63, =@div
    MOV R55, R63         ; delay slot: return address = next instruction
    MOV R53, NW          ; after hundreds
    MOV R54, R59
    MOV NW, R54
    MOV R59, =1
    MOV R63, =@div
    MOV R55, R63
    MOV R53, NW          ; after tens
    MOV R54, R59
    MOV NW, R54
    MOV R59, =1
    MOV R63, =@div
    MOV R55, R63
    MOV R53, NW          ; after units
    MOV R54, R59
    MOV R62, R54         ; NW final
    MOV R53, R62         ; W
    MOV R61, R62         ; W, with R60 = -1
    MOV R54, R61         ; W - 1
    MOV R59, R54         ; X = lowest bit
    MOV R54, R54
    MOV R53, R54         ; Y = W minus lowest bit
    MOV R60, =99
    MOV R61, R0
    MOV R55, =@ml
    MOV R57, =@step
ml:
    MOV R54, R59
    MOV R59, R59
    MOV R53, R54
    MOV R56, R54
    MOV R63, R56
    MOV R61, R61
div:
    ...
"""

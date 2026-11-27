#!/bin/bash
# quenched sweep: N 2000 three wirings, N 8000 one wiring (seed 7)
for p in 0.001 0.003 0.01 0.03 0.1 0.2 0.3 0.5 0.7 1; do
 for sd in 7 21 22; do echo "./bs_q 2000 $p 100 $sd 0.3 qruns/N2000_p${p}_s${sd}"; done
 echo "./bs_q 8000 $p 300 7 0.3 qruns/N8000_p${p}_s7"
done | xargs -P 8 -I{} sh -c '{}'

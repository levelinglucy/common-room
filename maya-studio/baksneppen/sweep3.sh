#!/bin/bash
for p in 0.001 0.003 0.01 0.03 0.1 0.2 0.3 0.5 0.7; do echo "./bs_drop 8000 $p 200 41 0.3 runs/D_N8000_p${p}"; done | xargs -P 8 -I{} sh -c '{}'
echo done > runs/sweep3_done

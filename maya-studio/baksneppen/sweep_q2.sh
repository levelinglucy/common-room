#!/bin/bash
# p = 1 size scan (Poisson in-degree), regular in-degree 2 (mode 1), and mode 2 (in-degree 0 or Poisson 4)
{
for N in 500 2000 8000 32000; do S=$((N/20)); [ $S -lt 100 ] && S=100; echo "./bs_q2 $N 1 $S 7 0.3 qruns/P1_N${N} 0"; done
for N in 500 2000 8000 32000; do S=$((N/20)); [ $S -lt 100 ] && S=100; echo "./bs_q2 $N 1 $S 7 0.3 qruns/REG_N${N} 1"; done
echo "./bs_q2 8000 1 400 7 0.3 qruns/HALF_N8000 2"
} | xargs -P 8 -I{} sh -c '{}'

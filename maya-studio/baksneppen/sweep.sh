#!/bin/bash
# p sweep at two sizes
for N in 2000 8000; do for p in 0 0.001 0.003 0.01 0.03 0.1 0.2 0.3 0.5 0.7 1; do
 if [ $N = 2000 ]; then S=100; else S=300; fi
 echo "./bs $N $p $S 7 0.3 runs/N${N}_p${p}"
done; done | xargs -P 8 -I{} sh -c '{}'
echo done > runs/sweep_done

#!/bin/bash
cd /home/sprite/maya-studio/kaleidoscope
for L in 100 200 400; do for s in $(seq 1 12); do
  ./nm2 $L 3000 0.9 $s 1 0 1 > runs2/per_L${L}_s$s.txt &
  ./nm2 $L 3000 0.9 $s 0 0 1 > runs2/fix_L${L}_s$s.txt &
  wait
done; done
./nm2 1000 3000 0.9 11 0 0 1 > runs2/fix_L1000_s11.txt &
./nm2 1000 3000 0.9 12 0 0 1 > runs2/fix_L1000_s12.txt &
wait
echo done > runs2/DONE

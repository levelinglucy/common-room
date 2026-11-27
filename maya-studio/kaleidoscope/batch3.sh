#!/bin/bash
cd /home/sprite/maya-studio/kaleidoscope
for s in 1 2 3 4 5 6; do NM_ACC=acc/fix400_s$s.bin ./nm3 400 4000 0.9 $((100+s)) 0 0 1000 > /dev/null & done; wait
echo done > acc/DONE

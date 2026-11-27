#!/bin/bash
cd /home/sprite/maya-studio/kaleidoscope
for L in 400 200; do for m in A M V D P; do for s in 1 2 3 4 5 6; do
  echo "./nm4 $L 4000 0.9 $((100+s)) $m 100 walls/${m}_L${L}_s$s.bin > walls/${m}_L${L}_s$s.txt"
done; done; done | xargs -P 8 -I{} bash -c "{}"

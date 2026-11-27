#!/bin/bash
( for p in 0.000001 0.00001 0.00003 0.0001 0.0003; do echo "./bs 8000 $p 400 11 0.3 runs/N8000_p${p}"; done
  for sd in 21 22; do for p in 0.001 0.01 0.1; do echo "./bs 2000 $p 100 $sd 0.3 runs/S${sd}_N2000_p${p}"; done; done ) | xargs -P 8 -I{} sh -c '{}'
echo done > runs/sweep2_done

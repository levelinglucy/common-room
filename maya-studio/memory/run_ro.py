"""Run heal.py's main with the reach_out variants registered. usage: python3 run_ro.py VARIANT SEEDS [floor] [rare]"""
import sys, statistics as st
sys.path.insert(0, '/home/sprite/maya-studio/memory')
import reach_out, heal as H
variant, seeds = sys.argv[1], int(sys.argv[2])
if len(sys.argv) > 3: H.M.PRUNE_BELOW = float(sys.argv[3])
if len(sys.argv) > 4: H.RARE = float(sys.argv[4])
rs = [H.run(variant, s) for s in range(seeds)]
P = sum(r['probes'] for r in rs)
F = {k: sum(r['fail'][k] for r in rs) for k in rs[0]['fail']}
print(f'variant={variant} prune_below={H.M.PRUNE_BELOW} rare={H.RARE} seeds={seeds}')
print(f'mean hyphae alive: {st.mean(r["nh"] for r in rs):.2f}')
print(f'whole body connected: {100 * st.mean(r["conn"] for r in rs):.1f}% of ticks')
print(f'live rare jobs that arrived: {100 * st.mean(r["jobs"] for r in rs):.1f}%')
print(f'probe io_channel -> idle organ reached: {100 * st.mean(r["reach"] for r in rs):.1f}%')
print(f'failed probes {F["no_path"] + F["path_missed"]}/{P}: no path {F["no_path"]}, path missed {F["path_missed"]}')

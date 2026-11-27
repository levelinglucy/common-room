import numpy as np
for ps in ['0', '0.0001', '0.001', '0.01', '0.1', '1']:
    J = np.loadtxt('runs/N8000_p%s_jump.txt' % ps)
    d, c = J[:, 0], J[:, 1]
    tot = c.sum()
    far = c[d > 100].sum() / tot
    line = 'p=%-7s jumps>100: %.5f  (2p/3 = %.5f)' % (ps, far, 2 * float(ps) / 3)
    if ps == '0':
        # tail exponent of P(d) on ring, fit d in 5..200 with log bins
        bins = np.unique(np.logspace(np.log10(5), np.log10(400), 25).astype(int))
        pd = [c[(d >= bins[k]) & (d < bins[k + 1])].sum() / (bins[k + 1] - bins[k]) for k in range(len(bins) - 1)]
        mid = np.sqrt(bins[:-1] * bins[1:])
        sl = np.polyfit(np.log(mid), np.log(np.array(pd) / tot), 1)[0]
        line += '  ring tail exponent %.2f' % (-sl)
    print(line)

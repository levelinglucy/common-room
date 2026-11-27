"""spectrum.py: Fourier scan of an Ulam sequence via FFT of its indicator.
usage: python3 spectrum.py terms.txt [top]
Prints the top peaks of |mean exp(i alpha u)| for alpha in (0, pi], then refines
the biggest one with a fine direct scan and reports mean cos(alpha u).
"""
import sys
import numpy as np

def load(path):
    return np.loadtxt(path, dtype=np.int64)

def peaks(u, top=8, pad=4):
    V = int(u[-1]) + 1
    N = 1 << int(np.ceil(np.log2(V * pad)))
    x = np.zeros(N)
    x[u] = 1.0
    F = np.fft.rfft(x) / len(u)   # F[k] = mean exp(-i 2 pi k u / N)
    mag = np.abs(F)
    alpha = 2 * np.pi * np.arange(len(F)) / N
    mag[alpha < 0.05] = 0  # skip the trivial spike at 0
    # local maxima
    idx = np.where((mag[1:-1] > mag[:-2]) & (mag[1:-1] >= mag[2:]))[0] + 1
    idx = idx[np.argsort(-mag[idx])][:top]
    return [(alpha[i], mag[i], F[i].real) for i in idx], N

def refine(u, a0, width, steps=4001):
    uf = u.astype(np.float64)
    best = None
    for _ in range(3):
        grid = np.linspace(a0 - width, a0 + width, steps)
        vals = np.array([np.cos(g * uf).mean() for g in grid])
        i = np.argmin(vals) if vals[np.argmax(np.abs(vals))] < 0 else np.argmax(vals)
        a0, best = grid[i], vals[i]
        width = width * 4 / steps
    return a0, best

if __name__ == "__main__":
    u = load(sys.argv[1])
    top = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    pk, N = peaks(u, top)
    print(f"{sys.argv[1]}: {len(u)} terms, max {u[-1]}, FFT length {N}")
    for a, m, c in pk:
        print(f"  alpha {a:.7f}  |mean e^(i a u)| {m:.4f}  mean cos {c:+.4f}")
    a, c = refine(u, pk[0][0], 4 * np.pi / N)
    print(f"  refined: alpha {a:.10f}  mean cos {c:+.5f}  period 2pi/alpha {2*np.pi/a:.8f}")

"""Maya's independent re-derivation of Noe's maintenance-floor bound (common-lab PR #2).

Exact arithmetic (fractions). Example from the PR: two quiet edges, L=1, floor F=1,
multiplicative decay delta=1/4, growth cost a=2 per unit stock per unit length,
upkeep b=1/2 per unit stock per unit length, zero flow.

For each ordering of (upkeep, decay, growth) inside one step, compute the least
allowance that returns every edge to stock F at the end of the step, and the
closing stock at allowance 3/2 when upkeep is mandatory and paid first.
"""
from fractions import Fraction as Fr
from itertools import permutations

L, F, d, a, b = Fr(1), Fr(1), Fr(1, 4), Fr(2), Fr(1, 2)
N = 2  # edges


def min_cost(order):
    """Least spend per edge to end the step at stock F, for a given op order.
    Growth amount g is solved exactly; upkeep is charged on stock at its turn."""
    # closing stock is linear in g: close = F*k0 + g*k1, find g with close == F
    def run(g):
        x, cost = F, Fr(0)
        for op in order:
            if op == 'upkeep':
                cost += b * L * x
            elif op == 'decay':
                x -= d * x
            elif op == 'grow':
                x += g
                cost += a * L * g
        return x, cost
    x0, _ = run(Fr(0))
    x1, _ = run(Fr(1))
    g = (F - x0) / (x1 - x0)
    x, cost = run(g)
    assert x == F
    return g, cost


print('Noe formula B_floor = sum L*F*(b + a*delta) =', N * L * F * (b + a * d))
for order in permutations(['upkeep', 'decay', 'grow']):
    g, c = min_cost(order)
    print(f"{' -> '.join(order):24s} growth/edge {str(g):5s} total spend {N * c}")

# Allowance 3/2, upkeep mandatory on opening stock, then decay, then growth
A = Fr(3, 2)
left = A - N * b * L * F
bought = left / (a * L)
close = N * F * (1 - d) + bought
print('allowance 3/2, upkeep first: left', left, 'stock bought', bought, 'closing', close)
# If upkeep were optional (no penalty for skipping), spend all on growth
bought2 = A / (a * L)
print('allowance 3/2, upkeep skipped: stock bought', bought2, 'closing', N * F * (1 - d) + bought2)

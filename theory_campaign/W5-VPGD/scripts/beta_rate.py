"""LD-rate relaxation (heuristic counting constraints, STAR.md §4) for the (beta) comparator in the grouped family,
d = 2, A = 1: maximise q3(a,b,l) - max(z_a^2, z_b^2) over group-factor level f and member levels h (signed), subject
to f^2 <= 1-beta and f^2 + sum_{J} h_j^2 <= 1 - beta + |J| beta for every subset J of {a,b,l}.
(beta)-failure requires the max to exceed 2*kappa = 3.  Random search, seed 11."""
import itertools, numpy as np
rng = np.random.default_rng(11)
def best(r, iters=200000):
    C = (1 - r) * np.eye(3) + r * np.ones((3, 3)); Ci = np.linalg.inv(C)
    bt = rng.uniform(0, 1, iters); f = np.sqrt(rng.uniform(0, 1, iters) * (1 - bt))
    h = rng.uniform(-1, 1, (iters, 3))
    # rescale h to satisfy subset constraints
    ok = np.ones(iters, bool)
    for J in itertools.chain.from_iterable(itertools.combinations(range(3), k) for k in (1, 2, 3)):
        ok &= f ** 2 + (h[:, list(J)] ** 2).sum(1) <= 1 - bt + len(J) * bt + 1e-12
    z = np.sqrt(r) * f[:, None] + np.sqrt(1 - r) * h
    q3 = np.einsum('ni,ij,nj->n', z, Ci, z)
    val = np.where(ok, q3 - np.maximum(z[:, 0] ** 2, z[:, 1] ** 2), -np.inf)
    return val.max()
out = []
for r in (0.1, 0.2, 0.3, 1/3, 0.4, 0.5, 0.6, 0.8):
    out.append(f"r={r:.3f}: sup (beta)-rate ~ {best(r):.4f}   (fails iff > 3)")
print('\n'.join(out)); open('../results/beta_rate.txt', 'w').write('\n'.join(out) + '\n')

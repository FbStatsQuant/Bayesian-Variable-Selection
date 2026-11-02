# Laptop check: fast one-move Neighbourhood scores vs brute-force F_exact on regenerated study data.
import numpy as np
from oswap_lib import F_exact, Neighbourhood, log_prior_table
from rgen import generate
rng = np.random.default_rng(7)
worst = 0.0
for (p, s, r, c) in [(500, 4, 1, 0.5), (1000, 5, 7, 1.0), (500, 2, 3, 0.5)]:
    X, eps, S0, b = generate(p, s, r)
    y = c * X[:, S0] @ b + eps; y = y - y.mean(); y = y / np.sqrt(y @ y / 199)
    lp = log_prior_table(p, 200); nb = Neighbourhood(X, S0, lp)
    F0, Fa, Fd, Fs = nb.scores(y)
    for _ in range(5):
        l = rng.integers(len(nb.nulls)); j = rng.integers(14)
        d = [F0 - F_exact(X, y, S0, lp), Fa[l] - F_exact(X, y, np.append(S0, nb.nulls[l]), lp),
             Fd[j] - F_exact(X, y, np.delete(S0, j), lp), Fs[j, l] - F_exact(X, y, np.append(np.delete(S0, j), nb.nulls[l]), lp)]
        worst = max(worst, max(abs(x) for x in d))
print('max |fast - brute| over 60 comparisons:', worst)

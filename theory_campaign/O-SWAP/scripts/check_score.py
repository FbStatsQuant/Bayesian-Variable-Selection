# Check F_exact and Neighbourhood against the R engine's logged F_S0 (LS0 run files) and brute force.
import sys, numpy as np, rdata
sys.path.insert(0, '.')
from oswap_lib import *
for (p, s, r, sc) in [(500, 4, 1, 'c050'), (500, 1, 3, 'c100'), (1000, 5, 7, 'c050')]:
    X, Y, act, beta, eps = load(p, s, r)
    Xs, y, sy = standardise(X, Y[:, SCALE_COL[sc]])
    lp = log_prior_table(p, 200)
    F0 = F_exact(Xs, y, act, lp)
    row = rdata.read_rds(f"/home/fb31/ls0_work/full/p{p:04d}/p{p:04d}_S{s}_r{r:03d}_{sc}.rds")['row']
    print(p, s, r, sc, 'python F_S0 =', F0, ' engine F_S0 =', float(row['F_S0'].values[0]),
          ' engine S0_best_nbr_gap=', float(row['S0_best_nbr_gap'].values[0]), row['S0_best_nbr_type'].values[0])
    nb = Neighbourhood(Xs, act, lp)
    F0b, Fa, Fd, Fs = nb.scores(y)
    rng = np.random.default_rng(1)
    l = rng.integers(len(nb.nulls)); j = rng.integers(14)
    Sa = np.append(act, nb.nulls[l]); Sd = np.delete(act, j); Ss = np.append(np.delete(act, j), nb.nulls[l])
    print('  fast vs brute: F0', F0b - F0, ' add', Fa[l] - F_exact(Xs, y, Sa, lp),
          ' drop', Fd[j] - F_exact(Xs, y, Sd, lp), ' swap', Fs[j, l] - F_exact(Xs, y, Ss, lp))
    best = max(Fa.max(), Fd.max(), Fs.max()) - F0
    print('  python best nbr gap', best)

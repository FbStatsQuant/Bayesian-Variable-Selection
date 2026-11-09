"""R04: early adaptive path at large n; proof quantities; full-path miss at moderate n."""
import sys; sys.dont_write_bytecode = True
import math, json, time, numpy as np
from scipy.stats import norm
from fastcs import Model, scan
rows = []
def run(n, c, s0, seed, full=False):
    p = int(math.floor(c * n)); rng = np.random.default_rng(10_000 * seed + 7 * s0 + int(1000 * c) + n)
    m = Model(n, p, s0, rng); K = m.K
    start, z, minlbf = m.start()
    ok_size = len(start) == K
    nulls = np.arange(s0, p)
    topnull = set(nulls[np.argsort(m.xi[s0:])[-(K - s0):]].tolist())
    ok_start = ok_size and set(range(s0)) <= set(start.tolist()) and set(start.tolist()) - set(range(s0)) == topnull
    q = (K - s0) / (p - s0); qq = 1 / (2 * c); t = norm.ppf(1 - qq); mu = norm.pdf(t) / qq
    sel_mean = float(m.xi[sorted(topnull)].mean())
    ell = math.ceil(math.log2(n + p + 1)); L0 = ell + s0 + 2; Lc = math.ceil((1 / math.log(2) + .05) * math.log(n)); L = max(L0, Lc)
    an = math.sqrt(1.5 * math.log(n)); tail = int((m.xi[s0:] <= -an).sum())
    inT = np.zeros(p, bool); inT[start] = True
    Delta = math.log((2 * p - K) / K) + .5 * (m.Lk[K] - m.Lk[K - 1])
    min_margin = np.inf; max_truth = -np.inf; minM = np.inf; xs = []; nullswaps = 0; maxdel = -np.inf; minswapgain = np.inf
    moves = 0; sizes = []
    lim = L if not full else 10 ** 9
    while moves < lim:
        r = scan(m, inT); best = max(r['del'], r['add'], r['swap'])
        if moves < L:
            min_margin = min(min_margin, r['swap'] - max(r['del'], r['add'])); max_truth = max(max_truth, r['truth_out'] - r['FT'])
            minM = min(minM, r['M']); xs.append(r['xT']); maxdel = max(maxdel, r['del'] - r['FT']); minswapgain = min(minswapgain, r['swap'] - r['FT'])
        if not best > r['FT']: break
        if best == r['swap']:
            j, l = r['swap_arg']
            if moves < L and j >= s0 and l >= s0 and nullswaps == moves: nullswaps += 1
            inT[j] = False; inT[l] = True
        elif best == r['del']: inT[r['del_arg']] = False
        else: inT[r['add_arg']] = True
        moves += 1; sizes.append(int(inT.sum()))
    row = dict(n=n, p=p, c=c, s0=s0, seed=seed, start_ok=bool(ok_start), min_logBF_over_n=minlbf / n, q_n=q, mu=mu, t=t,
               sel_null_mean=sel_mean, xT0=xs[0], max_drift=max(abs(x - xs[0]) for x in xs), L=L, L0=L0,
               first_L_nullswaps=nullswaps, all_L_nullswaps=nullswaps >= L, min_swap_minus_other=min_margin,
               min_swapgain_over_logn=minswapgain / math.log(n), Delta_K=Delta, maxdelgain=maxdel, Delta_over_logn=Delta / math.log(n),
               max_truthout_gain=max_truth, min_M=minM, tail_count=tail, two_L=2 * L)
    if full:
        a = ell + K; T = set(start.tolist()); S0 = set(range(s0)); first = None
        # replay sizes to find first scanned centre within one flip/swap of S0
        # (recompute path for membership)
        inT2 = np.zeros(p, bool); inT2[start] = True; tcount = 0
        while True:
            Tset = set(np.flatnonzero(inT2).tolist()); mis = S0 - Tset; ext = Tset - S0
            if Tset == S0 or len(mis) + len(ext) == 1 or (len(mis) == 1 and len(ext) == 1):
                first = tcount; break
            r = scan(m, inT2); best = max(r['del'], r['add'], r['swap'])
            if not best > r['FT']: break
            if best == r['swap']: j, l = r['swap_arg']; inT2[j] = False; inT2[l] = True
            elif best == r['del']: inT2[r['del_arg']] = False
            else: inT2[r['add_arg']] = True
            tcount += 1
        row.update(cap_a=a, uncapped_moves=moves, first_scan_scoring_S0=first, LS0_scores_S0=(first is not None and first <= a))
    return row
t0 = time.time()
for n in (1000, 10_000, 100_000, 1_000_000):
    for c in (.55, .75, .95):
        for s0 in (1, 2):
            for seed in range(3 if n <= 100_000 else 2):
                row = run(n, c, s0, seed, full=(n == 1000))
                rows.append(row); print(json.dumps(row, default=float), flush=True)
for n in (2000, 4000):
    for c in (.55, .75, .95):
        for s0 in (1, 2):
            row = run(n, c, s0, 0, full=True); rows.append(row); print(json.dumps(row, default=float), flush=True)
json.dump(rows, open('check2_out.json', 'w'), indent=1, default=float)
print('secs', time.time() - t0)

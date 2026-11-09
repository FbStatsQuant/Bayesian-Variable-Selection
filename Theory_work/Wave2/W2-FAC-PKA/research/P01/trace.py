"""Trace margins along one exact path: per step k, centre x, M, best deletion gain, best swap gain,
best addition gain, |xi| of the deleted null, number of imported nulls still inside. Output trace_<args>.json."""
import math, json, sys
import numpy as np
from sortedcontainers import SortedList
from pathsim import Model

n = int(sys.argv[1]); c = float(sys.argv[2]); s0 = int(sys.argv[3]); seed = int(sys.argv[4])
m = Model(n, c, s0, seed); K = m.K; p = m.p
T = m.start()
ins = SortedList((m.xi[j], j) for j in T if j >= s0)
out = SortedList((m.xi[j], j) for j in range(s0, p) if j not in T)
k = len(T); W1 = float(sum(m.w[j] for j in T)); W2 = float(sum(m.w[j] ** 2 for j in T))
imported = set(); rows = []; step = 0
while True:
    Fc = m.F(k, W1, W2); x = m.centre_w(k, W1); g = m.gam(k)
    M = m.nu * m.n * m.d ** 2 / (m.alpha * m.psi(k, W1, W2))
    bd = (-1e300, None)
    i = ins.bisect_left((x, -1))
    for ii in (i - 1, i, i + 1):
        if 0 <= ii < len(ins):
            j = ins[ii][1]; v = m.F(k - 1, W1 - m.w[j], W2 - m.w[j] ** 2) - Fc
            if v > bd[0]: bd = (v, j)
    bs = (-1e300, None); ba = (-1e300, None)
    for l in (out[0][1], out[-1][1]):
        if k < K:
            v = m.F(k + 1, W1 + m.w[l], W2 + m.w[l] ** 2) - Fc
            if v > ba[0]: ba = (v, l)
        tl = m.xi[l] - x; target = x + g * tl / (1 + g); i = ins.bisect_left((target, -1))
        for ii in (i - 1, i, i + 1):
            if 0 <= ii < len(ins):
                j = ins[ii][1]; v = m.F(k, W1 - m.w[j] + m.w[l], W2 - m.w[j] ** 2 + m.w[l] ** 2) - Fc
                if v > bs[0]: bs = (v, (j, l))
    best = max(bd[0], bs[0], ba[0])
    if best <= 0: break
    Delta = m.pen[k - 1] - m.pen[k]
    tlmax = max((m.xi[out[0][1]] - x) ** 2, (m.xi[out[-1][1]] - x) ** 2)
    row = dict(step=step, k=k, x=x, M=M, Delta=Delta, del_gain=bd[0], swap_gain=bs[0], add_gain=ba[0] if k < K else None,
               swap_index=M * tlmax - Delta, n_imp_inside=len(imported & set(j for _, j in ins)) if step % 50 == 0 or k < 200 else None)
    if bs[0] >= bd[0] and bs[0] >= ba[0]:
        j, l = bs[1]; row['move'] = 's'; row['xi_out'] = float(m.xi[j]); row['xi_in'] = float(m.xi[l])
        ins.remove((m.xi[j], j)); out.add((m.xi[j], j)); out.remove((m.xi[l], l)); ins.add((m.xi[l], l))
        W1 += m.w[l] - m.w[j]; W2 += m.w[l] ** 2 - m.w[j] ** 2; imported.add(l)
    elif bd[0] >= ba[0]:
        j = bd[1]; row['move'] = 'd'; row['xi_out'] = float(m.xi[j]); row['was_imported'] = j in imported
        ins.remove((m.xi[j], j)); out.add((m.xi[j], j)); W1 -= m.w[j]; W2 -= m.w[j] ** 2; k -= 1
    else:
        l = ba[1]; row['move'] = 'a'; out.remove((m.xi[l], l)); ins.add((m.xi[l], l)); W1 += m.w[l]; W2 += m.w[l] ** 2; k += 1
    rows.append(row); step += 1
json.dump(dict(n=n, c=c, s0=s0, seed=seed, K=K, rows=rows), open(f'trace_{n}_{c}_{s0}_{seed}.json', 'w'))
sw = [r for r in rows if r['move'] == 's']; dl = [r for r in rows if r['move'] == 'd']
fd = dl[0]['step'] if dl else None
post = [r for r in rows if fd is not None and r['step'] > fd]
print('swaps', len(sw), 'first_del', fd, 'adds', sum(r['move'] == 'a' for r in rows), 'final k', k)
print('max swap_index after first del', max(r['swap_index'] for r in post), 'max (swap-del) after', max(r['swap_gain'] - r['del_gain'] for r in post))
imp_del = [r for r in dl if r.get('was_imported')]
print('imported deleted:', len(imp_del), 'first at k', imp_del[0]['k'] if imp_del else None)
for kk in sorted(set([K - 1, K - 2, K - 5, K - 20, int(0.9 * K), int(.7 * K), int(.5 * K), int(.3 * K), int(.1 * K), int(.03 * K), 300, 100, 30, 10, 5, 3, 2]), reverse=True):
    rr = [r for r in post if r['k'] == kk]
    if rr:
        r = rr[0]
        print(f"k={kk:7d} x={r['x']:+.3f} M={r['M']:.3f} Delta={r['Delta']:.2f} del={r['del_gain']:.2f} swap-del={r['swap_gain']-r['del_gain']:+.2f} swapidx={r['swap_index']:+.2f} imp_in={r['n_imp_inside']} xi_del={r.get('xi_out'):+.2f}")

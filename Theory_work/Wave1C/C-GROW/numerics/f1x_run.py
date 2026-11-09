"""F1X (extra, beyond the spec): AR(1) exact Gram, p=100, P = the m = floor(0.9 log n) nulls nearest to a truth (so |P| <= (1-delta0) log n, the (G4-chi) regime),
all 2^m lattice sets tested, 20 noise seeds. -> f1x_results.pkl; report: f_report.py F1X"""
import sys, time, pickle, math
import numpy as np
import f_common as fc
from multiprocessing import Pool

def rows():
    R = []
    for rho in (0.5, 0.8):
        for n in (200, 800, 3200):
            r = fc.make_row_ar1(100, n, rho, nseeds=20, tag="F1X")
            m = int(math.floor(0.9 * math.log(n)))
            S0 = r['S0']
            nulls = sorted((j for j in range(100) if j not in S0), key=lambda j: (min(abs(j - t) for t in S0), j))
            r['P'] = sorted(nulls[:m]); r['dn'] = None; r['m'] = m
            r['id'] = f"F1X_rho{rho}_p100_n{n}_m{m}"
            R.append(r)
    return R
ROWS = {r['id']: r for r in rows()}

def work(task):
    rid, kind, s = task
    row = ROWS[rid]; t = time.time()
    try:
        if kind == 'pop': r = fc.pop_margins(row)
        elif kind == 'lat': r = fc.lattice_test(row, list(range(row['nseeds'])))
        else: r = fc.seed_run(row, s)
    except Exception:
        import traceback; r = dict(id=rid, kind=kind, seed=s, error=traceback.format_exc())
    r['wall'] = time.time() - t
    return r

if __name__ == '__main__':
    tasks = [(rid, 'lat', None) for rid in ROWS]
    for rid, row in ROWS.items():
        tasks += [(rid, 'seed', s) for s in range(row['nseeds'])] + [(rid, 'pop', None)]
    out = []
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 3) as pool:
        for i, r in enumerate(pool.imap_unordered(work, tasks)):
            out.append(r); print(i + 1, len(tasks), r.get('id'), r.get('kind'), r.get('seed'), round(r['wall'], 1), 'ERR' if 'error' in r else '', flush=True)
    pickle.dump(out, open('f1x_results.pkl', 'wb'))
    print('done')

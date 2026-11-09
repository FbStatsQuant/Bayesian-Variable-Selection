"""F2 runner: study S5 population design, exact Gram, p=100, s0=4, P = all nulls. -> f2_results.pkl"""
import sys, time, pickle
import f_common as fc
from multiprocessing import Pool

def rows():
    return [fc.make_row_s5(100, n, c) for c in (0.5, 1.0) for n in (800, 3200, 12800)]
ROWS = {r['id']: r for r in rows()}

def work(task):
    rid, kind, s = task
    row = ROWS[rid]; t = time.time()
    try:
        if kind == 'pop': r = fc.pop_margins(row)
        elif kind == 'lat': r = fc.lattice_test(row, list(range(row['nseeds'])))
        else: r = fc.seed_run(row, s)
    except Exception:
        import traceback
        r = dict(id=rid, kind=kind, seed=s, error=traceback.format_exc())
    r['wall'] = time.time() - t
    return r

if __name__ == '__main__':
    tasks = [(rid, 'lat', None) for rid in ROWS]
    for rid, row in ROWS.items():
        tasks += [(rid, 'seed', s) for s in range(row['nseeds'])] + [(rid, 'pop', None)]
    out = []; t0 = time.time()
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 3) as pool:
        for i, r in enumerate(pool.imap_unordered(work, tasks)):
            out.append(r)
            print(i + 1, len(tasks), r.get('id'), r.get('kind'), r.get('seed'), round(r.get('wall', 0), 1), 'ERR' if 'error' in r else '', flush=True)
            if (i + 1) % 5 == 0 or i + 1 == len(tasks): pickle.dump(out, open('f2_results.pkl', 'wb'))
    print('done', time.time() - t0)

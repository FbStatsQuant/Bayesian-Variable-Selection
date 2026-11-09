"""F3: AR(1) rho=0.5, n=400, p=399, s0=4, exact Gram; start mode only (no LS), 20 seeds. -> f3_results.pkl"""
import sys, time, pickle
import f_common as fc
from multiprocessing import Pool
ROW = fc.make_row_ar1(399, 400, 0.5, nseeds=20, tag="F3")
ROWS = {ROW['id']: ROW}
def work(task):
    rid, s = task; t = time.time()
    try: r = fc.seed_run(ROWS[rid], s, do_ls=False)
    except Exception:
        import traceback; r = dict(id=rid, kind='seed', seed=s, error=traceback.format_exc())
    r['wall'] = time.time() - t
    return r
if __name__ == '__main__':
    print(ROW['id'], 'S0', ROW['S0'], 'dn', ROW['dn'], '|P|', len(ROW['P']))
    out = []
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 2) as pool:
        for i, r in enumerate(pool.imap_unordered(work, [(ROW['id'], s) for s in range(20)])):
            out.append(r); print(i + 1, r.get('seed'), r.get('start_size'), round(r['wall'], 1), 'ERR' if 'error' in r else '', flush=True)
            pickle.dump(out, open('f3_results.pkl', 'wb'))
    pop = fc.pop_margins(ROW); pickle.dump(out + [pop], open('f3_results.pkl', 'wb')); print(pop)

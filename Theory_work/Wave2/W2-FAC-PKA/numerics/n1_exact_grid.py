"""Exploratory feasible-CS grid; source imports read-only, no outside bytecode.
Uses actual source block partition/start DP; adapts CS scan ONLY to accept start.
Not a proof or production tie-fidelity certification.
"""
import sys, os, json, inspect, math, time
from pathlib import Path
sys.dont_write_bytecode = True
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
HERE = Path(__file__).resolve().parent
SRC = HERE.parents[1] / 'W2-FAC-B' / 'numerics'
sys.path.insert(0, str(SRC))
import numpy as np
import bvs_core as bc
import cs_core as cs

source = inspect.getsource(cs.ls0_path_cs)
def replace_once(text, old, new):
    assert text.count(old)==1, ('source drift',old,text.count(old))
    return text.replace(old,new)
source = replace_once(source,'def ls0_path_cs(P, max_moves=10 ** 7, record_every=0):',
                        'def run_path(P, start, max_moves=10 ** 7, record_every=0):')
source = replace_once(source,'inT = np.ones(p, bool)', 'inT = np.zeros(p, bool); inT[list(start)] = True')
source = replace_once(source,'k = p\n    A = float(z @ z)\n    B = float(z.sum())',
                        'k = len(start)\n    A = float(z[inT] @ z[inT])\n    B = float(z[inT].sum())')
source = replace_once(source,'isN_in = np.array([j not in S0 for j in idx_in])',
                       'isN_in = np.array([j not in S0 for j in idx_in], dtype=bool)')
namespace = dict(cs.__dict__)
exec(source, namespace)
run_path = namespace['run_path']

class TableAdapter:
    def __init__(self, model):
        self.model = model
        self.n, self.p, self.K = model.n, model.p, model.K
        self.logw = model.lw
        self.logm0 = model.F(()) - self.logw[0]
        self.cache = {(): self.logm0}
    def logm_idx(self, idx):
        idx = np.asarray(idx)
        z = self.model.z[idx]
        k = idx.shape[1]
        return self.model.F_stats(k, (z*z).sum(1), z.sum(1)) - self.logw[k]
    logm_many = bc.Problem.logm_many
    logm = bc.Problem.logm

def main():
    with (HERE/'N1_exact_grid.jsonl').open('w', encoding='utf8') as out:
        for n in (200, 400, 800):
            for ratio in (.6, .85):
                p = int(n*ratio)
                rho = .5
                Sigma = (1-rho)*np.eye(p)+rho*np.ones((p,p))
                blocks = bc.partition_from_corr(Sigma, bc.block_size(n,p))
                for seed in range(2):
                    theta = np.zeros(p); truth = (2,26,53,75)
                    theta[list(truth)] = .5*np.array([1.4,1,1.8,1.2])
                    P = cs.CS(rho,theta,n,rng=np.random.default_rng(seed))
                    start = bc.start_mode(TableAdapter(P),blocks,tie_tol=0).mode
                    result = run_path(P,start)
                    counts = {}
                    for tag,_,_ in result['moves']: counts[tag]=counts.get(tag,0)+1
                    cap = bc.ell_cap(n,p)+len(start)
                    # Exact membership of truth in scanned flip/swap neighborhoods.
                    T = set(start); first_score = 0 if T==set(truth) else None
                    for t in range(len(result['moves'])+1):
                        missing, extra = set(truth)-T, T-set(truth)
                        if (len(missing)+len(extra)==1 or len(missing)==len(extra)==1 or T==set(truth)) and first_score is None:
                            first_score=t
                        if t<len(result['moves']):
                            _, jo, li = result['moves'][t]
                            if jo is not None: T.remove(jo)
                            if li is not None: T.add(li)
                    details={}
                    for tag,jo,li in result['moves']:
                        detail=('swap_' if tag.startswith('s') else 'move_')+('T' if jo in truth else 'N' if jo is not None else 'none')+'>'+('T' if li in truth else 'N' if li is not None else 'none')
                        details[detail]=details.get(detail,0)+1
                    row = dict(n=n,p=p,K=P.K,ell=bc.ell_cap(n,p),blocks=blocks,ratio=ratio,seed=seed,start=len(start),truth_in_start=set(truth)<=set(start),move_details=details,
                        counts=counts,moves=len(result['moves']),cap=cap,first_scoring_scan=first_score,
                        merged_scores_truth=first_score is not None and first_score<=cap,final_is_truth=result['final_is_S0'])
                    out.write(json.dumps(row)+'\n'); out.flush(); print(json.dumps(row),flush=True)
if __name__=='__main__': main()

from pathlib import Path
import collections
import hashlib
import json
import math
import itertools
import numpy as np

BASE = Path(__file__).resolve().parents[2]
NUM = BASE / 'numerics'

def rows(name):
    return [json.loads(s) for s in (NUM / name).read_text(encoding='utf-8').splitlines() if s.strip()]

result = {}
n1, n3 = rows('N1_raw.jsonl'), rows('N3_raw_final360.jsonl')
result['N1'] = dict(rows=len(n1), saturated=sum(r['saturated'] for r in n1),
    MR1_misses=sum(not r['MR1_scores'] for r in n1),
    doubled_scores=sum(r['k_hit'] is not None and r['k_hit'] <= r['cap_2K'] for r in n1),
    phase_exceptions=sum(r['swaps_after_first_del'] != 0 or set(r['counts']) - {'sN', '-N'} != set()
                         or r['counts'].get('-N', 0) != r['start']-r['s0'] for r in n1))
result['N3'] = dict(rows=len(n3), endpoint_misses=sum(not r['final_is_S0'] for r in n3),
    doubled_scores=sum(r['k_hit'] is not None and r['k_hit'] <= r['cap_2'] for r in n3),
    phase_exceptions=sum(r['swaps_after_first_del'] != 0 or any(t.startswith('+') for t in r['counts']) for r in n3),
    max_moves_K=max(r['moves']/r['K'] for r in n3), MW_range=[min(r['MW'] for r in n3), max(r['MW'] for r in n3)],
    max_p_cap_exceeds_double=sum(max(r['cap_MR1'], r['p']) > r['cap_2'] for r in n3))
chain = rows('L2_chain.jsonl')
cnt = dict(rows=len(chain), x_ok=0, j_ok=0, M_ok=0, V_ok=0, G_ok=0, impl_applicable=0, impl_ok=0)
for r in chain:
    cnt['x_ok'] += abs(r['xT']) <= 2
    cnt['j_ok'] += r['min_abs_tau_ret'] <= 3.5
    cnt['M_ok'] += r['MT'] >= r['MT_bound']
    cnt['V_ok'] += r['V'] >= r['Vlb'] - 1e-9
    cnt['G_ok'] += r['best_swap'] >= r['Gjl'] - 1e-9 and r['Gjl'] >= r['MTV'] - 1e-9
    if r['MTV'] > r['Delta_K']:
        cnt['impl_applicable'] += 1
        cnt['impl_ok'] += r['best_swap'] > max(r['best_del'], 0)
assert cnt == rows('L2_chain_summary.txt')[0]
result['L2_chain'] = cnt
st = rows('L3_static.jsonl')
for s in rows('L3_static_summary.txt'):
    rr = [r for r in st if all(r[k] == s[k] for k in ('n', 'p', 'rho', 'seed'))]
    for size, pred in [('small', lambda r: r['m'] <= r['m_e']), ('large', lambda r: r['m'] > r['m_e'])]:
        v = min((r for r in rr if pred(r)), key=lambda r: r['best_del_over_logn'])
        assert v['best_del_over_logn'] == s['min_ratio_'+size]
        assert v['kind'] == s['worst_'+size]
    assert math.isclose(s['budget_bound'], s['K']*(.5*math.log(s['n'])+2.4))
    assert math.isclose(s['moves_over_K'], s['moves']/s['K'])
result['L3_static'] = dict(rows=len(st), minimum_gain_ratio=min(r['best_del_over_logn'] for r in st), summaries_match=True)
small = rows('L3_small.jsonl')
for s in rows('L3_small_summary.txt'):
    rr = [r for r in small if r['rho'] == s['rho'] and r['n'] == s['n']]
    assert round(min(r['ratio'] for r in rr),4) == s['worst_ratio']
result['L3_small'] = dict(rows=len(small), summaries_match=True)
l12 = rows('L12_check.jsonl')
result['L12'] = dict(counts=dict(collections.Counter(r['test'] for r in l12)),
    L1_extreme_counts=[r['N_n'] for r in l12 if r['test']=='L1'],
    L2_deletion_bounds_pass=sum(r.get('i_del_le_DeltaK',False) for r in l12),
    L2_extreme_conditions=sum(r.get('extreme_outside',False) for r in l12))
result['hashes'] = {f: hashlib.sha256((NUM/f).read_bytes()).hexdigest() for f in ('N1_raw.jsonl','N3_raw_final360.jsonl')}

# Independent matrix check, without importing ticket implementations or writing their caches.
rng = np.random.default_rng(73107)
err = dict(score_identity=0.0, neighbour_gain=0.0, rss_comparison=0.0)
checks = 0
for rho, sigma in [(.2, .7), (.95, 2.3)]:
    n,p,K = 14,13,7
    q,_ = np.linalg.qr(np.column_stack([np.ones(n), rng.normal(size=(n,p))]))
    Sigma = (1-rho)*np.eye(p)+rho*np.ones((p,p))
    X = math.sqrt(n-1)*q[:,1:]@np.linalg.cholesky(Sigma).T
    theta = np.zeros(p); theta[[1,5]]=[1.4,-.6]
    Y = X@theta+sigma*rng.normal(size=n); Y -= Y.mean()
    s = np.linalg.norm(Y)/math.sqrt(n-1); y = Y/s
    z = X.T@y; alpha=(n*n-1)*(1-rho)+1; beta=(n*n-1)*rho; nu=.01+n/2
    def psi(T):
        k=len(T); zz=z[list(T)]
        return .02+n-1-n*(zz@zz-beta/(alpha+k*beta)*zz.sum()**2)/alpha
    def score(T):
        k=len(T); G=X[:,T].T@X[:,T]; H=(n+1)*G+np.eye(k)
        logdet=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(k))[1]
        Q=y@y-n*z[list(T)]@np.linalg.solve(H,z[list(T)]) if k else y@y
        f=-math.log(2)-math.log(math.comb(2*p-1,k))-.5*logdet-nu*math.log(.02+Q)
        return f, logdet
    # All containing-truth sets up to K; random arbitrary sets for all gain types.
    samples=[tuple(sorted(rng.choice(p,k,replace=False).tolist())) for k in range(1,K+1) for _ in range(10)]
    samples += [(1,5)+j for m in range(K-1) for j in itertools.combinations([t for t in range(p) if t not in (1,5)],m)]
    for raw in samples:
        T=tuple(sorted(raw)); k=len(T); f,L=score(T); ps=psi(T)
        G=X[:,T].T@X[:,T]; Q=y@y-n*z[list(T)]@np.linalg.solve((n+1)*G+np.eye(k),z[list(T)])
        err['score_identity']=max(err['score_identity'],abs(ps-(.02+Q)))
        if {1,5} <= set(T):
            rss=np.linalg.norm(Y-X[:,T]@np.linalg.lstsq(X[:,T],Y,rcond=None)[0])**2
            lo=rss/s**2; hi=lo+1+1/((n-1)*(1-rho))
            err['rss_comparison']=max(err['rss_comparison'],lo-Q,Q-hi)
        gamma=beta/(alpha+k*beta); t=z-gamma*z[list(T)].sum()
        j=T[0]; l=next(i for i in range(p) if i not in T)
        for U,typ in [(tuple(i for i in T if i!=j),'del'),(tuple(sorted(set(T)-{j}|{l})),'sw')]+([(tuple(sorted(T+(l,))),'add')] if k<K else []):
            fu,Lu=score(U)
            if typ=='del': dq=-(1+beta/(alpha+(k-1)*beta))*t[j]**2/alpha
            elif typ=='add': dq=(1-beta/(alpha+(k+1)*beta))*t[l]**2/alpha
            else: dq=(t[l]**2-t[j]**2-gamma*(t[l]-t[j])**2)/alpha
            prior=math.log(math.comb(2*p-1,k))-math.log(math.comb(2*p-1,len(U)))
            gain=prior-.5*(Lu-L)-nu*math.log1p(-n*dq/ps)
            err['neighbour_gain']=max(err['neighbour_gain'],abs(gain-(fu-f)))
            checks+=1
result['independent_matrix_checks']=dict(gains=checks, max_errors=err)
print(json.dumps(result,indent=2))

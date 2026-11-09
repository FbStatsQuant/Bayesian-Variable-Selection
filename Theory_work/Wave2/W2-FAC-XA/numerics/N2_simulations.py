"""N2 local diagnostics, not a proof. Run python -B N2_simulations.py.

Only N2-prefixed outputs beside this file; FAC-B and N1 imported read-only.
Centered Gaussian scatter W ~ Wishart_p(Sigma,n-1) is drawn by LOWER
Bartlett A: A_ii^2 ~ chi2(df-i), A_ij ~ N(0,1), i>j (zero based).
W=L A A' L'; R=D^-1 W D^-1, D=sqrt(diag(W)).
"""
import sys
sys.dont_write_bytecode = True
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import csv
import hashlib
import itertools
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
import N1_simulations as n1
bc, fc = n1.bc, n1.fc
NS, PS, SEEDS = (10**6, 10**8), (32, 100, 200), range(5)
TRUTH = (0, 1)


def scatter(sigma, n, rng):
    p = len(sigma)
    df = n-1
    assert df >= p
    a = np.zeros((p, p))
    ix = np.tril_indices(p, -1)
    a[ix] = rng.standard_normal(len(ix[0]))
    a[np.diag_indices(p)] = np.sqrt(rng.chisquare(df-np.arange(p)))
    b = np.linalg.cholesky(sigma) @ a
    return b @ b.T


def correlation(w):
    d = np.sqrt(np.diag(w))
    r = w / d[:, None] / d[None, :]
    return (r+r.T)/2


def response(gram, n, seed, p):
    theta = np.r_[1., 1.3, np.zeros(p-2)]
    sequence = np.random.SeedSequence([seed, n, p, 202])
    # FAC-B draws g=Lz, then an independent chi-square(df-p).
    problem = fc.ExactGram(gram, theta, n, np.random.default_rng(sequence), sigma2=1.)
    replay = np.random.default_rng(sequence)
    z = replay.standard_normal(p)
    residual = float(replay.chisquare(n-1-p)) if n-1-p else 0.
    g = np.linalg.cholesky(gram) @ z
    projection = float(z@z)
    signal = (n-1)*float(theta@gram@theta)
    cross = 2*math.sqrt(n-1)*float(theta@g)
    norm2 = signal+cross+projection+residual
    s = math.sqrt(norm2/(n-1))
    xty = ((n-1)*(gram@theta)+math.sqrt(n-1)*g)/s
    assert np.allclose(xty, problem.Xty, rtol=2e-14, atol=2e-12)
    assert math.isclose(s, problem.scale_s, rel_tol=2e-14)
    assert problem.yty == n-1
    return problem, dict(response_scale=s, response_raw_norm2=norm2,
                         noise_projection_norm2=projection, noise_residual_chi2=residual,
                         residual_df=n-1-p, signal_norm2=signal, signal_noise_cross=cross,
                         response_scaled_norm2=problem.yty)


def problem_for(n, p, seed, family, kind):
    sigma = n1.covariance(p, family)
    w = None
    if kind == 'iid':
        rng = np.random.default_rng(np.random.SeedSequence([seed, n, p, 101]))
        w = scatter(sigma, n, rng)
        gram = correlation(w)
    else:
        gram = sigma.copy()
    problem, audit = response(gram, n, seed, p)
    return problem, sigma, gram, w, audit


def finite(value):
    return float(value) if np.isfinite(value) else None


def path(problem, ids):
    t = tuple(range(problem.p))
    cap = bc.ell_cap(problem.n, problem.p)+len(t)
    states, tags, scans = [list(t)], [], []
    scored = False
    exhausted = False
    direct_errors = []
    s0_score = float(problem.F(TRUTH))  # audit only: does NOT mark S0 as path-scored
    for step in range(cap+1):
        sc = fc.scan(problem, t)
        nxt, info = fc.best_move(sc, set(TRUTH))
        missing, extras = set(TRUTH)-set(t), set(t)-set(TRUTH)
        visible = t == TRUTH or len(missing)+len(extras) == 1 or len(missing) == len(extras) == 1
        scored |= visible
        null_del = [float(v) for j,v in zip(t,sc['del']) if j not in TRUTH]
        competitors = [sc['del']]
        if sc['add'] is not None:
            competitors.append(sc['add'])
        competitors.append(sc['swap'].ravel())
        values = np.concatenate(competitors)
        values = values[np.isfinite(values)]
        ordered = np.sort(values)
        top_gap = float(ordered[-1]-ordered[-2]) if len(ordered)>1 else None
        tie_count = int(np.sum(values == info['best']))
        margin = max(null_del)-float(sc['swap'].max()) if null_del and sc['swap'].size else None
        # Direct Cholesky F_many audit at full, middle and terminal centres.
        error = None
        if step in (0, problem.p//2) or nxt is None:
            models = [t, TRUTH]
            estimates = [sc['FT'], s0_score]
            if nxt is not None:
                models.append(nxt)
                estimates.append(info['best'])
            else:
                mapped = n1.scan_map(sc)
                if mapped:
                    model = max(mapped, key=mapped.get)
                    models.append(model)
                    estimates.append(mapped[model])
            scores = problem.F_many(models)
            error = float(np.max(np.abs(scores-np.array(estimates))))
            direct_errors.append(error)
            assert error < 2e-4, (ids, step, error)
        scans.append(dict(**ids, step=step, size=len(t), missing=len(missing), extras=len(extras),
                          score=float(sc['FT']), S0_score=s0_score, score_minus_S0=float(sc['FT']-s0_score),
                          best_gain=finite(info['best']-sc['FT']),
                          best_null_deletion_gain=finite(info['best_del_N']),
                          best_truth_deletion_gain=finite(info['best_del_T']),
                          best_addition_gain=finite(info['best_add']),
                          best_swap_gain=finite(sc['swap'].max()-sc['FT']) if sc['swap'].size else None,
                          null_del_vs_all_swap_margin=margin,
                          top_two_neighbor_gap=top_gap, top_neighbor_ties=tie_count,
                          improving_ties=tie_count if nxt is not None else 0,
                          score_ulp=float(abs(np.spacing(sc['FT']))), direct_score_error=error,
                          move=info.get('move','stop'), next_model=list(nxt) if nxt is not None else None,
                          S0_in_this_scan=visible, scored_S0_so_far=scored))
        if nxt is None:
            break
        if step == cap:
            exhausted = True
            break
        tags.append(info['move'])
        t = nxt
        states.append(list(t))
    def minimum(key):
        v = [s[key] for s in scans if s[key] is not None]
        return min(v) if v else None
    record = dict(**ids, cap=cap, moves=len(tags), cap_slack=cap-len(tags), cap_exhausted=exhausted,
                  certified=not exhausted, final=list(t), final_is_S0=t == TRUTH, scored_S0=scored,
                  safe_only=all(tag == '-N' for tag in tags), truth_loss=any(not set(TRUTH)<=set(s) for s in states),
                  deletions=sum(tag.startswith('-') for tag in tags),
                  additions=sum(tag.startswith('+') for tag in tags), swaps=sum(tag.startswith('sw') for tag in tags),
                  scans=len(scans), S0_score=s0_score, final_score=scans[-1]['score'],
                  min_null_del_vs_all_swap_margin=minimum('null_del_vs_all_swap_margin'),
                  min_top_two_neighbor_gap=minimum('top_two_neighbor_gap'),
                  tied_scans=sum(s['top_neighbor_ties']>1 for s in scans),
                  improving_tied_scans=sum(s['improving_ties']>1 for s in scans),
                  max_direct_score_error=max(direct_errors), path=states, move_tags=tags)
    return record, scans


def csv_write(name, rows):
    assert name.startswith('N2')
    with (HERE/name).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def validate_law():
    """Small-n moment tests against exact Wishart formula AND N1 raw-row law.

    Var(W_ij)=df*(Sigma_ij^2+Sigma_ii*Sigma_jj). Also test centered,
    sd-normalized correlation and response moments using independent samples.
    Monte Carlo z statistics are diagnostic, with conservative 7-SE assertions.
    """
    rows = []
    reps, n, p = 6000, 32, 4
    for family in ('CS', 'unequal'):
        sigma = n1.covariance(p, family)
        a, b = np.random.default_rng(310), np.random.default_rng(411)
        ws, raw_ws, rs, raw_rs, resp, raw_resp = [], [], [], [], [], []
        theta = np.r_[1.,1.3,0.,0.]
        for _ in range(reps):
            w = scatter(sigma,n,a)
            xraw = bc.iid_design_raw(sigma,n,b)
            xc = xraw-xraw.mean(0)
            wr = xc.T@xc
            r, rr = correlation(w), correlation(wr)
            ws.append(w)
            raw_ws.append(wr)
            rs.append(r)
            raw_rs.append(rr)
            pr = fc.ExactGram(r,theta,n,a)
            x = bc.standardize_X(xraw)
            y = bc.make_y_std(x,theta,1.,b)
            resp.append(np.r_[pr.Xty,pr.scale_s**2])
            # Raw response scale recovered explicitly using a second raw draw.
            # First p columns compare exactly the N1 standardized-response law.
            yy = x@theta+b.standard_normal(n)
            yy -= yy.mean()
            raw_resp.append(np.r_[x.T@y,yy@yy/(n-1)])
        for law, data in (('Bartlett',np.array(ws)),('N1_raw_centered',np.array(raw_ws))):
            mean_target = (n-1)*sigma
            var_target = (n-1)*(sigma**2+np.outer(np.diag(sigma),np.diag(sigma)))
            z = (data.mean(0)-mean_target)/np.sqrt(var_target/reps)
            variance_relative_error = float(np.max(np.abs(data.var(0,ddof=1)/var_target-1)))
            assert np.max(np.abs(z)) < 7 and variance_relative_error < .12
            rows.append(dict(family=family, test=law+'_Wishart_moments', reps=reps,
                             max_abs_mean_z=float(np.max(np.abs(z))), max_variance_relative_error=variance_relative_error))
        for label, aa, bb in (('normalized_Gram',rs,raw_rs),('normalized_response_and_scale',resp,raw_resp)):
            aa,bb = np.array(aa),np.array(bb)
            se = np.sqrt((aa.var(0,ddof=1)+bb.var(0,ddof=1))/reps)
            z = np.divide(aa.mean(0)-bb.mean(0),se,out=np.zeros_like(se),where=se>1e-14)
            assert np.max(np.abs(z)) < 7
            rows.append(dict(family=family,test=label+'_vs_N1_raw_law',reps=reps,
                             max_abs_mean_z=float(np.max(np.abs(z))),max_variance_relative_error=None))
    return rows


def validate_scores():
    rows = []
    for p,family,kind in itertools.product((4,8),('CS','unequal'),('exact','iid')):
        problem,_,_,_,_ = problem_for(64,p,0,family,kind)
        models = [tuple(i for i in range(p) if mask>>i&1) for mask in range(1<<p)]
        scores = dict(zip(models,problem.F_many(models)))
        error, mismatches, neighbors = 0.,0,0
        for t in models:
            sc = fc.scan(problem,t)
            mapped = n1.scan_map(sc)
            expected = bc.neighbours(t,p,problem.K)
            assert set(mapped) == set(expected)
            error = max(error,abs(sc['FT']-scores[t]),*(abs(v-scores[s]) for s,v in mapped.items()))
            nxt,_ = fc.best_move(sc,set(TRUTH))
            best = max(scores[s] for s in expected)
            direct = min(s for s in expected if scores[s] == best) if best>scores[t] else None
            mismatches += nxt != direct
            neighbors += len(expected)
        assert error < 1e-8 and mismatches == 0
        rows.append(dict(p=p,n=64,seed=0,family=family,kind=kind,models=len(models),neighbors=neighbors,
                         max_abs_score_error=error,best_move_mismatches=mismatches))
    return rows


def main():
    started = datetime.now(timezone.utc).isoformat()
    sources = [Path(__file__),HERE/'N1_simulations.py',HERE.parent/'PLAN.md',HERE.parent/'STATEMENT.md']
    sources += [n1.SOURCE/name for name in ('fac_core.py','bvs_core.py','cs_core.py')]
    hashes = {str(s):hashlib.sha256(s.read_bytes()).hexdigest() for s in sources}
    law_checks = validate_law()
    score_checks = validate_scores()
    csv_write('N2_law_validation.csv',law_checks)
    csv_write('N2_score_validation.csv',score_checks)
    print('Small-n Wishart/response moments and exhaustive scorer checks passed.',flush=True)
    records, paired, all_scans = [], [], []
    stats = {}
    with (HERE/'N2_raw.jsonl').open('w',encoding='utf-8') as raw, (HERE/'N2_scans.jsonl').open('w',encoding='utf-8') as scanfile:
        for n,p,seed,family in itertools.product(NS,PS,SEEDS,('CS','unequal')):
            pair = []
            for kind in ('exact','iid'):
                problem,sigma,gram,w,audit = problem_for(n,p,seed,family,kind)
                ids = dict(n=n,p=p,seed=seed,family=family,kind=kind)
                record,scans = path(problem,ids)
                record.update(n1.spectral(sigma,gram,n))
                record.update(audit)
                key = f'n{n}_p{p}_seed{seed}_{family}_{kind}'
                stats[key+'_R'] = gram
                stats[key+'_Xty'] = problem.Xty
                stats[key+'_g'] = problem.g
                if w is not None:
                    stats[key+'_W'] = w
                raw.write(json.dumps(record,allow_nan=False)+'\n')
                raw.flush()
                for scan in scans:
                    scanfile.write(json.dumps(scan,allow_nan=False)+'\n')
                scanfile.flush()
                records.append(record)
                pair.append(record)
                all_scans.extend(scans)
            a,b = pair
            first = next((i for i,(s,t) in enumerate(zip(a['path'],b['path'])) if s != t),None)
            if first is None and len(a['path']) != len(b['path']):
                first = min(len(a['path']),len(b['path']))
            paired.append(dict(n=n,p=p,seed=seed,family=family,paths_identical=a['path']==b['path'],
                               first_differing_state=first,endpoints_equal=a['final']==b['final']))
            print(f'Completed n={n} p={p} seed={seed} family={family}',flush=True)
    np.savez_compressed(HERE/'N2_sufficient_stats.npz',**stats)
    csv_write('N2_runs.csv',[{k:v for k,v in r.items() if k not in ('path','move_tags')} for r in records])
    csv_write('N2_scans.csv',all_scans)
    csv_write('N2_paired_paths.csv',paired)
    groups = []
    for n,p,family,kind in itertools.product(NS,PS,('CS','unequal'),('exact','iid')):
        sub = [r for r in records if (r['n'],r['p'],r['family'],r['kind']) == (n,p,family,kind)]
        group = dict(n=n,p=p,family=family,kind=kind,runs=len(sub))
        for key in ('safe_only','scored_S0','final_is_S0','truth_loss','cap_exhausted','swaps','additions','tied_scans'):
            group[key] = sum(r[key] for r in sub)
        for key in ('abs_op','abs_over_sqrt_p_n','abs_over_p_sqrt_n','whitened_op','whitened_over_sqrt_p_n'):
            group[key+'_median'] = float(np.median([r[key] for r in sub]))
        for key in ('min_null_del_vs_all_swap_margin','min_top_two_neighbor_gap','cap_slack'):
            group[key+'_min'] = min(r[key] for r in sub)
        groups.append(group)
    csv_write('N2_grouped.csv',groups)
    after = {str(s):hashlib.sha256(s.read_bytes()).hexdigest() for s in sources}
    assert hashes == after
    metadata = dict(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),
                    python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
                    source_hashes=hashes,source_hashes_after=after,source_hashes_unchanged=True,
                    n=list(NS),p=list(PS),seeds=list(SEEDS),runs=len(records),
                    dont_write_bytecode=sys.dont_write_bytecode,law_validation_reps=6000,
                    statement='XA v1 LOCKED research target; diagnostics only',
                    gram_df='n-1',response_residual_df='n-1-p')
    (HERE/'N2_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    summary(records,paired,all_scans,law_checks,score_checks)
    print(json.dumps(metadata,indent=2),flush=True)


def summary(records,paired,scans,law,checks):
    count = lambda key: sum(bool(r[key]) for r in records)
    margins = [s['null_del_vs_all_swap_margin'] for s in scans if s['null_del_vs_all_swap_margin'] is not None]
    lines = ['# N2: Bartlett-Wishart full-start conditional diagnostics','',
             'Read XA PLAN.md and locked STATEMENT v1. No proof or asymptotic status is assigned.','',
             '120 runs: n=1e6,1e8; p=32,100,200; seeds 0-4; exact and random Grams for CS rho=.5 '
             'and unequal positive loadings linspace(.4,.85,p). Truth {0,1}, standardized theta=(1,1.3), noise variance 1. '
             'Every path starts from [p]; the actual start-mode event and visibility are not tested. '
             'The grid is not asserted to satisfy any locked growth or delivery hypothesis.','',
             '## Construction and validation','',
             'Lower Bartlett A has independent strict-lower N(0,1) entries and diagonal sqrt(chi2(n-1-i)), '
             'with i zero based. For Sigma=L L\', W=L A A\' L\' has exactly the centered raw Gaussian scatter law. '
             'Normalize R_ij=W_ij/sqrt(W_ii W_jj). No n-row matrix is allocated for the main grid.','',
             'FAC-B ExactGram supplies the conditional response law: g=chol(R)z, z~N(0,I); '
             '||C epsilon||^2=z\'z+chi2(n-1-p). For Y=X theta+C epsilon, '
             '||Y||^2=(n-1)theta\'R theta+2 sqrt(n-1)theta\'g+z\'z+chi2(n-1-p); '
             's^2=||Y||^2/(n-1), X\'y=((n-1)R theta+sqrt(n-1)g)/s, y\'y=n-1. '
             'Each run replays and verifies these identities and saves every normalization component. '
             'Exact/random pairs share z and the residual draw; cross-family cases share those coordinates too. '
             'This is a specified coupling of sufficient statistics.','',
             f'Small-n validation uses n=32,p=4,6000 replicates per family and generator. '
             'Checks E[W]=(n-1)Sigma and Var(W_ij)=(n-1)(Sigma_ij^2+Sigma_ii Sigma_jj) for Bartlett and explicitly centered raw rows, '
             'then compares mean normalized-Gram entries and response sufficient statistics/scale with the N1 raw-row law. '
             f'Maximum mean z statistic: {max(r["max_abs_mean_z"] for r in law):.5g}. '
             'These moment diagnostics do not prove equality in distribution; the Bartlett formula supplies the convention.','',
             f'Exhaustive general-scorer validation at n=64,p=4,8 for both families and Gram kinds: '
             f'{len(checks)} cases, {sum(c["models"] for c in checks)} model scores, '
             f'{sum(c["neighbors"] for c in checks)} neighbor comparisons. '
             f'Maximum score error {max(c["max_abs_score_error"] for c in checks):.6g}; no best-move mismatches. '
             'General FAC-B scan and production strict-improvement/exact-tie lexicographic rule are reused, '
             'with independent direct F_many Cholesky checks at full, middle and terminal centres. '
             f'Main-grid maximum direct score error: {max(r["max_direct_score_error"] for r in records):.6g}.','',
             '## Observations','',
             f'- Safe null-deletion-only paths: {count("safe_only")}/120; truth loss: {count("truth_loss")}. '
             f'Additions {sum(r["additions"] for r in records)}, swaps {sum(r["swaps"] for r in records)}.',
             f'- S0 scored by path scans: {count("scored_S0")}/120; endpoints S0: {count("final_is_S0")}/120. '
             'The separately audited S0 score does not count toward path discovery.',
             f'- Cap exhausted: {count("cap_exhausted")}; minimum slack {min(r["cap_slack"] for r in records)}. '
             'Cap=ceil(log2(n+p+1))+p; final complete scan included.',
             f'- Minimum best-null-deletion minus best-all-swap score: {min(margins):.9g}. '
             'No-swap/no-null scans excluded; additions and truth deletions also scanned.',
             f'- Exact top-neighbor tied scans: {sum(r["tied_scans"] for r in records)}; '
             f'improving tied scans: {sum(r["improving_tied_scans"] for r in records)}. '
             f'Minimum top-two-neighbor score gap: {min(r["min_top_two_neighbor_gap"] for r in records):.9g}. '
             'Raw gaps, score ULPs and direct-check errors are saved to expose floating-point sensitivity.',
             f'- Exact/random paths differ in {sum(not r["paths_identical"] for r in paired)}/60 pairs; '
             f'endpoints differ in {sum(not r["endpoints_equal"] for r in paired)}.','',
             'Absolute norm is ||R-Sigma||op; relative norm is '
             '||Sigma^(-1/2)(R-Sigma)Sigma^(-1/2)||op. Both, and competing scale normalizations, '
             'are in N2_runs.csv/N2_grouped.csv. Exact deviations are zero. No norm rate is inferred.','',
             '## Artifacts and limitations','',
             'N2_raw.jsonl contains each run and full path; N2_scans.jsonl/CSV contain every scan. '
             'N2_sufficient_stats.npz retains realized R, random scatter W, g and Xty for rescoring. '
             'N2_runs.csv, N2_grouped.csv and N2_paired_paths.csv provide summaries. '
             'N2_law_validation.csv and N2_score_validation.csv retain checks. '
             'N2_metadata.json records versions, times, grids and before/after source hashes.','',
             'Run: C:/Users/felip/anaconda3/python.exe -B Theory_work/Wave2/W2-FAC-XA/numerics/N2_simulations.py. '
             'Only N2-prefixed files are written; bytecode disabled. FAC-B sources and N1 are read-only. '
             'Local compute only; no start-mode, posterior/delivery, asymptotic proof or targeted lead-lemma norm experiment.']
    (HERE/'N2_summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()

"""XA numerics only: full-model CONDITIONAL paths, not start-mode tests.

Run with python -B; all generated files stay beside this script. FAC-B imports
are read-only. Conditional sufficient-statistic Gaussian simulation uses
fac_core.ExactGram also for the realized iid sample correlation matrix; this
has exactly the law of Y=X theta+C epsilon after response standardization.
No proofs or asymptotic claims are made by this experiment.
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
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'W2-FAC-B' / 'numerics'
sys.path.insert(0, str(SOURCE))
import bvs_core as bc
import fac_core as fc
import cs_core as cc

TRUTH = (0, 1)
SEEDS = range(10)
NS = (512, 2048)
PS = (16, 32, 64, 128)


def covariance(p, family):
    loading = np.full(p, math.sqrt(.5)) if family == 'CS' else np.linspace(.4, .85, p)
    return np.diag(1-loading**2) + np.outer(loading, loading)


def make_problem(n, p, seed, family, kind):
    sigma = covariance(p, family)
    if kind == 'iid':
        rng = np.random.default_rng(np.random.SeedSequence([seed, n, p, 101]))
        # Explicit raw iid N(0,Sigma) rows, then method's centering/scaling.
        x = bc.standardize_X(bc.iid_design_raw(sigma, n, rng))
        gram = x.T @ x / (n-1)
    else:
        gram = sigma.copy()
    theta = np.zeros(p)
    theta[:2] = (1., 1.3)
    # Same Cholesky-coordinate N(0,I_p) and chi-square residual in each pair.
    # This is a specified coupling, not literal shared row errors across designs.
    noise = np.random.default_rng(np.random.SeedSequence([seed, n, p, 202]))
    problem = fc.ExactGram(gram, theta, n, noise, sigma2=1.)
    return problem, sigma, gram


def scan_map(sc):
    t = sc['T']
    result = {}
    if sc['add'] is not None:
        for j, value in zip(sc['O'], sc['add']):
            if np.isfinite(value):
                result[tuple(sorted(t+(int(j),)))] = float(value)
    for i, value in enumerate(sc['del']):
        result[t[:i]+t[i+1:]] = float(value)
    for i, j in itertools.product(range(len(t)), range(len(sc['O']))):
        target = tuple(sorted(t[:i]+t[i+1:]+(int(sc['O'][j]),)))
        result[target] = float(sc['swap'][i,j])
    return result


def validation():
    rows = []
    for p, seed, family, kind in itertools.product((4, 8), (0, 1), ('CS', 'unequal'), ('exact', 'iid')):
        problem, _, _ = make_problem(64, p, seed, family, kind)
        models = [tuple(i for i in range(p) if mask >> i & 1) for mask in range(1 << p)]
        # Direct factorization of EVERY model, independent of Schur scan.
        scores = dict(zip(models, problem.F_many(models)))
        max_error = 0.
        choices = 0
        neighbors = 0
        cs_error = 0.
        if family == 'CS' and kind == 'exact':
            cs = cc.CS(.5, np.r_[1.,1.3,np.zeros(p-2)], 64, rng=np.random.default_rng(0))
            cs.z = problem.Xty.copy()
            cs_error = max(abs(cs.F(t)-scores[t]) for t in models)
        for t in models:
            sc = fc.scan(problem, t)
            mapped = scan_map(sc)
            expected = bc.neighbours(t, p, problem.K)
            assert set(mapped) == set(expected)
            max_error = max(max_error, abs(sc['FT']-scores[t]), *(abs(v-scores[s]) for s,v in mapped.items()))
            nxt, _ = fc.best_move(sc, set(TRUTH))
            best = max(scores[s] for s in expected)
            direct = min(s for s in expected if scores[s] == best) if best > scores[t] else None
            choices += nxt != direct
            neighbors += len(expected)
        assert max_error < 1e-8 and cs_error < 1e-8 and choices == 0
        # Full-path cross-check with FAC-B's independent CS path routine.
        cs_path_match = None
        if family == 'CS' and kind == 'exact':
            direct_path = bc.local_search(problem, tuple(range(p)), 100)
            cs_path = cc.ls0_path_cs(cs, max_moves=100)
            cs_path_match = tuple(cs_path['final']) == direct_path['final'] and len(cs_path['moves']) == direct_path['moves']
            assert cs_path_match
        rows.append(dict(p=p, seed=seed, family=family, kind=kind, models=len(models), neighbors=neighbors,
                         max_abs_score_error=max_error, best_move_mismatches=choices, cs_score_error=cs_error,
                         cs_endpoint_and_move_count_match=cs_path_match))
    return rows


def spectral(sigma, gram, n):
    delta = gram-sigma
    absolute = float(np.max(np.abs(np.linalg.eigvalsh(delta))))
    vals, vecs = np.linalg.eigh(sigma)
    whitener = (vecs / np.sqrt(vals)) @ vecs.T
    wd = whitener @ delta @ whitener
    relative = float(np.max(np.abs(np.linalg.eigvalsh((wd+wd.T)/2))))
    p = len(sigma)
    return dict(abs_op=absolute, abs_over_sqrt_p_n=absolute/math.sqrt(p/n),
                abs_over_p_sqrt_n=absolute/(p/math.sqrt(n)), whitened_op=relative,
                whitened_over_sqrt_p_n=relative/math.sqrt(p/n))


def path(problem, identifiers):
    t = tuple(range(problem.p))
    cap = bc.ell_cap(problem.n, problem.p) + len(t)
    scans, states, tags = [], [t], []
    scored_truth = False
    visited_truth_loss = False
    hpm, hpm_score = t, -math.inf
    exhausted = False
    for step in range(cap+1):
        sc = fc.scan(problem, t)
        # S0 is scored at a centre or if it differs by a feasible flip/swap.
        lost, extra = set(TRUTH)-set(t), set(t)-set(TRUTH)
        is_neighbor = len(lost)+len(extra) == 1 or (len(lost) == len(extra) == 1)
        scored_truth |= t == TRUTH or is_neighbor
        nxt, info = fc.best_move(sc, set(TRUTH))
        candidates = [(t, sc['FT'])]
        if nxt is not None:
            candidates.append((nxt, info['best']))
        for s, score in candidates:
            if score > hpm_score or (score == hpm_score and (len(s),s) < (len(hpm),hpm)):
                hpm, hpm_score = s, float(score)
        null_del = [float(v) for j,v in zip(t,sc['del']) if j not in TRUTH]
        # ALL swaps, including truth-out; margin recorded only when both exist.
        margin = max(null_del)-float(sc['swap'].max()) if null_del and sc['swap'].size else None
        dsort = np.sort(sc['del'])
        gap = float(dsort[-1]-dsort[-2]) if len(dsort) >= 2 else None
        null_sort = sorted(null_del)
        null_gap = null_sort[-1]-null_sort[-2] if len(null_sort) >= 2 else None
        scans.append(dict(**identifiers, step=step, size=len(t), missing=len(lost), extras=len(extra),
                          score=float(sc['FT']), best_gain=float(info['best']-sc['FT']),
                          best_null_deletion_gain=info['best_del_N'] if null_del else None,
                          best_swap_gain=float(sc['swap'].max()-sc['FT']) if sc['swap'].size else None,
                          best_addition_gain=info['best_add'] if sc['add'] is not None and len(sc['add']) else None,
                          null_del_vs_all_swap_margin=margin, top_two_deletion_gap=gap,
                          top_two_null_deletion_gap=null_gap,
                          move=info.get('move','stop'), next_model=list(nxt) if nxt is not None else None,
                          scored_S0_so_far=bool(scored_truth)))
        if nxt is None:
            break
        if step == cap:
            exhausted = True
            break
        tags.append(info['move'])
        t = nxt
        states.append(t)
        visited_truth_loss |= not set(TRUTH).issubset(t)
    def minimum(key):
        values = [row[key] for row in scans if row[key] is not None]
        return min(values) if values else None
    result = dict(**identifiers, cap=cap, moves=len(tags), cap_slack=cap-len(tags), cap_exhausted=exhausted,
                  certified=not exhausted, final=list(t), final_is_S0=t == TRUTH, scored_S0=bool(scored_truth),
                  truth_loss=visited_truth_loss, pure_null_deletion=all(tag == '-N' for tag in tags),
                  deletions=sum(tag.startswith('-') for tag in tags), additions=sum(tag.startswith('+') for tag in tags),
                  swaps=sum(tag.startswith('sw') for tag in tags), min_null_del_vs_all_swap_margin=minimum('null_del_vs_all_swap_margin'),
                  min_top_two_deletion_gap=minimum('top_two_deletion_gap'),
                  min_top_two_null_deletion_gap=minimum('top_two_null_deletion_gap'),
                  scored_set_HPM=list(hpm), path=[list(s) for s in states], move_tags=tags)
    return result, scans


def csv_write(name, rows):
    with (HERE/name).open('w',newline='',encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    started = datetime.now(timezone.utc).isoformat()
    hashes = {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
              for name in ('fac_core.py','cs_core.py','bvs_core.py')}
    checks = validation()
    csv_write('N1_validation.csv', checks)
    records, all_scans, paired = [], [], []
    with (HERE/'N1_raw.jsonl').open('w',encoding='utf-8') as raw:
        for n,p,seed,family in itertools.product(NS,PS,SEEDS,('CS','unequal')):
            pair = []
            for kind in ('exact','iid'):
                problem,sigma,gram = make_problem(n,p,seed,family,kind)
                ids = dict(n=n,p=p,seed=seed,family=family,kind=kind)
                record, scans = path(problem,ids)
                record.update(spectral(sigma,gram,n))
                # Reuse CS closed form as a second full-path check on all exact CS cases.
                if family == 'CS' and kind == 'exact':
                    cs = cc.CS(.5,np.r_[1.,1.3,np.zeros(p-2)],n,rng=np.random.default_rng(0))
                    cs.z = problem.Xty.copy()
                    closed = cc.ls0_path_cs(cs,max_moves=record['cap']+1)
                    record['cs_path_matches'] = (list(closed['final']) == record['final'] and
                                                len(closed['moves']) == record['moves'])
                    assert record['cs_path_matches']
                else:
                    record['cs_path_matches'] = None
                raw.write(json.dumps(record,allow_nan=False)+'\n')
                raw.flush()
                records.append(record)
                all_scans.extend(scans)
                pair.append(record)
            a,b = pair
            first = next((i for i,(s,t) in enumerate(zip(a['path'],b['path'])) if s != t),None)
            if first is None and len(a['path']) != len(b['path']):
                first = min(len(a['path']),len(b['path']))
            paired.append(dict(n=n,p=p,seed=seed,family=family,paths_identical=a['path']==b['path'],
                               first_differing_state=first, endpoints_equal=a['final']==b['final']))
            if seed == 9:
                print(f'Finished n={n} p={p} family={family}',flush=True)
    csv_write('N1_runs.csv',[{k:v for k,v in row.items() if k not in ('path','move_tags')} for row in records])
    csv_write('N1_scans.csv',all_scans)
    csv_write('N1_paired_paths.csv',paired)
    groups = []
    for n,p,family,kind in itertools.product(NS,PS,('CS','unequal'),('exact','iid')):
        subset = [r for r in records if (r['n'],r['p'],r['family'],r['kind']) == (n,p,family,kind)]
        group = dict(n=n,p=p,family=family,kind=kind,runs=len(subset))
        for key in ('pure_null_deletion','final_is_S0','scored_S0','truth_loss','cap_exhausted','swaps','additions'):
            group[key] = sum(r[key] for r in subset)
        for key in ('abs_op','abs_over_sqrt_p_n','abs_over_p_sqrt_n','whitened_op','whitened_over_sqrt_p_n'):
            group[key+'_median'] = float(np.median([r[key] for r in subset]))
        for key in ('min_null_del_vs_all_swap_margin','min_top_two_deletion_gap','cap_slack'):
            group[key+'_min'] = min(r[key] for r in subset)
        groups.append(group)
    csv_write('N1_grouped.csv',groups)
    metadata = dict(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),
                    python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
                    source_hashes=hashes,seeds=list(SEEDS),n=list(NS),p=list(PS),runs=len(records),
                    validation_cases=len(checks),dont_write_bytecode=sys.dont_write_bytecode)
    after_hashes = {name:hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in hashes}
    assert hashes == after_hashes
    metadata['source_hashes_after'] = after_hashes
    metadata['source_hashes_unchanged'] = True
    (HERE/'N1_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    write_summary(records,paired,checks,groups,all_scans)
    print(json.dumps(metadata,indent=2),flush=True)


def write_summary(records,paired,checks,groups,all_scans):
    def count(key):
        return sum(bool(r[key]) for r in records)
    lines = ['# N1: numerics only; conditional full-model paths', '',
             'XA STATEMENT.md was read as "v0 - proposed, NOT LOCKED". No proof work.', '',
             '## Setup', '',
             '320 runs: 10 seeds (0-9), n=512,2048; p=16,32,64,128; exact-CS, iid-CS, exact unequal loadings, iid unequal loadings. '
             'rho=0.5; unequal lambda_j=linspace(0.4,0.85,p), Sigma=diag(1-lambda^2)+lambda lambda\'. '
             'Truth S0={0,1}, fixed standardized coefficients (1,1.3), noise variance 1. '
             'These grids are diagnostics, not a check of an asymptotic growth condition.', '',
             'All paths start at [p]. This is a **conditional path experiment, not a start-mode test**. '
             'Neither the full-start event nor C2 visibility is tested. IID raw Gaussian rows are explicitly generated, '
             'centered and standardized. Response sufficient statistics are then sampled conditional on the realized Gram '
             'using FAC-B ExactGram, the exact Gaussian law for Y=X theta+C epsilon followed by response scaling. '
             'Exact designs use deterministic Gram Sigma. Each exact/iid pair shares Cholesky-coordinate Gaussian noise '
             'and the residual chi-square draw; ordering comparisons depend on this stated coupling. '
             'The four designs in each (n,p,seed) cell share noise coordinates, so their outcomes are correlated.', '',
             'FAC-B fac_core.py, cs_core.py and bvs_core.py were imported read-only; SHA256 before/after is in N1_metadata.json. '
             'PYTHONDONTWRITEBYTECODE=1 and python -B disable import caches. '
             'The FAC-B score/prior, complete flip/swap scans, strict improvement and lexicographic exact-tie rule are reused. '
             'Move cap is ceil(log2(n+p+1))+p, with the final complete scan included.', '',
             '## Observations', '',
             f'- Pure null-deletion paths: {count("pure_null_deletion")}/{len(records)}. '
             f'Additions: {sum(r["additions"] for r in records)}; swaps: {sum(r["swaps"] for r in records)}; '
             f'paths losing a truth: {count("truth_loss")}.',
             f'- S0 scored: {count("scored_S0")}/{len(records)}; endpoints equal S0: {count("final_is_S0")}/{len(records)}; '
             f'cap exhausted: {count("cap_exhausted")}; minimum cap slack: {min(r["cap_slack"] for r in records)}.',
             f'- Minimum best-null-deletion minus best **all-swap** score: '
             f'{min(r["min_null_del_vs_all_swap_margin"] for r in records):.9g}. '
             'Undefined scans (no null deletion or no swap) are excluded; terminal scans have no retained nulls in successful paths.',
             f'- Smallest gap between the best two deletions: {min(r["min_top_two_deletion_gap"] for r in records):.9g} '
             '(all scanned centres, including terminal centres). '
             f'Null-only version: {min(r["min_top_two_null_deletion_gap"] for r in records):.9g}.',
             f'- Exact/iid paths differed in {sum(not r["paths_identical"] for r in paired)}/{len(paired)} paired cases; '
             f'endpoints differed in {sum(not r["endpoints_equal"] for r in paired)}. '
             'See N1_paired_paths.csv for first differing state.',
             '- The four non-S0 endpoints all occur at n=512, p=32, seed=3, one in each design type: '
             'each stops at {0,1,4,21} after 28 null deletions. These are correlated outcomes under the shared-noise construction.',
             f'- Over scans that accept a move, the minimum deletion-versus-all-swap margin is '
             f'{min(r["null_del_vs_all_swap_margin"] for r in all_scans if r["move"] != "stop" and r["null_del_vs_all_swap_margin"] is not None):.9g}. '
             'The only two negative margins are terminal unequal-loading scans at the above cell: '
             'exact -0.297096945 and iid -0.130011822. Their best-neighbor gains are -1.91352630 and -1.60784682, '
             'respectively; neither accepts a swap. These observations do not refute an asymptotic statement.', '',
             '## Sample Gram diagnostics', '',
             'Rhat=X\'X/(n-1). Absolute norm is ||Rhat-Sigma||op. Relative norm is '
             '||Sigma^(-1/2)(Rhat-Sigma)Sigma^(-1/2)||op. Table entries are seed medians (iid only); '
             'normalizations inspect competing scales and do not establish a rate.', '',
             '| n | p | family | abs | abs/sqrt(p/n) | abs/(p/sqrt(n)) | relative | relative/sqrt(p/n) |',
             '|---|---|---|---|---|---|---|---|']
    for g in groups:
        if g['kind'] == 'iid':
            keys = ('abs_op','abs_over_sqrt_p_n','abs_over_p_sqrt_n','whitened_op','whitened_over_sqrt_p_n')
            lines.append('| '+ ' | '.join([str(g['n']),str(g['p']),g['family']]+[f'{g[k+"_median"]:.4g}' for k in keys])+' |')
    lines += ['', 'Exact-Gram deviations are zero by construction in the sufficient-statistic experiment.', '',
              '## Scan validation and artifacts', '',
              f'For p=4,8, n=64, seeds 0,1, all four design types: {len(checks)} validation cases; '
              f'{sum(r["models"] for r in checks)} models and {sum(r["neighbors"] for r in checks)} directed neighbor comparisons. '
              'Each scan is compared to direct Cholesky scoring of every feasible neighbor, at every possible centre. '
              f'Maximum absolute score discrepancy {max(r["max_abs_score_error"] for r in checks):.9g}; '
              f'best-move discrepancies {sum(r["best_move_mismatches"] for r in checks)}. '
              'Exact-CS closed-form scores and endpoint/move counts were also checked; every exact-CS main-grid endpoint/move count agrees.', '',
              '- Script: N1_simulations.py; rerun: `$env:PYTHONDONTWRITEBYTECODE="1"; & C:/Users/felip/anaconda3/python.exe -B Theory_work/Wave2/W2-FAC-XA/numerics/N1_simulations.py`.',
              '- N1_raw.jsonl: per-run results and full visited paths; N1_runs.csv: per-run scalar diagnostics.',
              '- N1_scans.csv: every scan, deletion gaps, deletion-versus-swap margins and accepted moves.',
              '- N1_paired_paths.csv: ordering comparisons; N1_grouped.csv: per-cell aggregates.',
              '- N1_validation.csv: exhaustive small-p scan checks; N1_metadata.json: versions, grid, UTC times and source hashes.', '',
              'These are observed local simulations only; no proof, start-mode, delivery, or asymptotic consistency status is assigned.']
    (HERE/'N1_summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()

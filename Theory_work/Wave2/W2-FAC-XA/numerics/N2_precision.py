"""Direct-score audit of floating ties; run python -B N2_precision.py after N2.

This checks double-precision scorer sensitivity, not exact real arithmetic.
"""
import sys
sys.dont_write_bytecode = True
import json
import numpy as np
import N2_simulations as n2


def main():
    records = [json.loads(line) for line in (n2.HERE/'N2_raw.jsonl').read_text().splitlines()]
    tied = [json.loads(line) for line in (n2.HERE/'N2_scans.jsonl').read_text().splitlines()
            if json.loads(line)['improving_ties'] > 1]
    results = []
    for row in tied:
        ids = {key:row[key] for key in ('n','p','seed','family','kind')}
        record = next(r for r in records if all(r[k] == v for k,v in ids.items()))
        problem,_,_,_,_ = n2.problem_for(**ids)
        t = tuple(record['path'][row['step']])
        sc = n2.fc.scan(problem,t)
        chosen,info = n2.fc.best_move(sc,set(n2.TRUTH))
        mapped = n2.n1.scan_map(sc)
        candidates = sorted(s for s,value in mapped.items() if value == info['best'])
        scores = problem.F_many(candidates)
        direct_choice = min(s for s,v in zip(candidates,scores) if v == max(scores))
        # Local tie order is verified, and audit makes the rounding sensitivity explicit.
        assert chosen == min(candidates)
        results.append(dict(**ids,step=row['step'],candidate_count=len(candidates),
                            removed_variables=[sorted(set(t)-set(s)) for s in candidates],
                            scan_scores=[mapped[s] for s in candidates],direct_scores=scores.tolist(),
                            direct_score_spread=float(max(scores)-min(scores)),
                            production_choice_removed=sorted(set(t)-set(chosen)),
                            direct_choice_removed=sorted(set(t)-set(direct_choice)),
                            choices_agree=chosen == direct_choice,
                            candidates_all_safe_null_deletions=all(set(n2.TRUTH)<=set(s) and len(s)==len(t)-1 for s in candidates)))
    (n2.HERE/'N2_tie_audit.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    lines = ['# N2 floating-point ordering audit','',
             'The main run follows FAC-B general scans and the production exact-float-tie lexicographic rule. '
             'This independent direct F_many Cholesky audit re-scores the candidates tied by that scan. '
             'It does not substitute a different rule or revise the recorded path.','',
             f'Improving tied scans: {len(results)}. '
             f'Direct/scanned choice disagreements: {sum(not r["choices_agree"] for r in results)}. '
             f'All tied candidates are safe null deletions: {all(r["candidates_all_safe_null_deletions"] for r in results)}.','']
    for r in results:
        lines += [f'- n={r["n"]}, p={r["p"]}, seed={r["seed"]}, {r["family"]}, {r["kind"]}, step={r["step"]}: '
                  f'tied deletions {r["removed_variables"]}; direct score spread {r["direct_score_spread"]:.9g}; '
                  f'production removes {r["production_choice_removed"]}, direct scoring removes {r["direct_choice_removed"]}.']
    lines += ['', 'Main-grid spot checks have maximum direct/scanned score discrepancy '
              f'{max(r["max_direct_score_error"] for r in records):.9g}. '
              'Tiny ordering gaps can therefore be numerically unresolved. Observed safe deletion and endpoint outcomes '
              'are diagnostics of the recorded implementation, not a claim of real-arithmetic path agreement. '
              'No alternate full path or high-precision proof is claimed.','',
              'Artifacts: N2_precision.py, N2_tie_audit.json, N2_precision_summary.md. '
              'Run after N2_simulations.py with python -B. Only N2-prefixed outputs are written.']
    (n2.HERE/'N2_precision_summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()

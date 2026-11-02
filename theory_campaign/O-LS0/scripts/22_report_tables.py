# 22_report_tables.py -- the four REPORT.md tables (a)-(d) from results/cell_summary.csv (20_aggregate.R) and
# results/paired_cell_summary.csv (21_paired.R). Aggregation only. Usage: python3 -I 22_report_tables.py <results dir>
import csv, sys, os
res = sys.argv[1]
C = {(r['scale_key'], r['p'], r['scenario']): r for r in csv.DictReader(open(os.path.join(res, 'cell_summary.csv')))}
P = {(r['scale_key'], r['p'], r['scenario']): r for r in csv.DictReader(open(os.path.join(res, 'paired_cell_summary.csv')))}
order = [(sk, p, s) for sk in ('c100', 'c050') for p in ('500', '1000') for s in '123456']
i = lambda v: str(int(float(v)))
f = lambda v, k=2: ('%.' + str(k) + 'f') % float(v)
out = []
def table(title, hdr, row, totals=None):
    for sk in ('c100', 'c050'):
        out.extend(['', '**%s, scale %s (c = %s), 100 fits per cell**' % (title, sk, '1' if sk == 'c100' else '0.5'), '',
                    '| cell | ' + ' | '.join(hdr) + ' |', '|' + '---|' * (len(hdr) + 1)])
        ks = [k for k in order if k[0] == sk]
        for k in ks:
            out.append('| p%s S%s | ' % (k[1], k[2]) + ' | '.join(row(C[k], P[k])) + ' |')
        if totals:
            out.append('| **all** | ' + ' | '.join(totals([C[k] for k in ks], [P[k] for k in ks])) + ' |')
S = lambda rows, c: str(sum(int(float(r[c])) for r in rows))
# (a) recovery
table('(a) Recovery', ['prod HPM = S₀', 'LS0 scored S₀', 'LS0 certified S₀', 'LS0 best = S₀ (LS0 alone)', 'prod + LS0 HPM = S₀'],
      lambda c, p: [p['prod_exact'], i(c['scored']), i(c['certified']), p['ls0_alone_exact'], p['with_ls0_exact']],
      lambda cs, ps: [S(ps, 'prod_exact'), S(cs, 'scored'), S(cs, 'certified'), S(ps, 'ls0_alone_exact'), S(ps, 'with_ls0_exact')])
# (b) harm
table('(b) Could LS0 hurt?', ['LS0 endpoint F > F(S₀), ≠ S₀', '… in prod-exact fits', 'LS0 best beats S₀', '… in prod-exact fits (harm)',
                              'LS0 best = prod HPM', 'LS0 changes prod HPM', 'gain', 'S₀ not a flip/swap local max', 'prod misses'],
      lambda c, p: [i(c['endpoint_beats_S0']), p['end_beats_S0_in_prod_exact'], i(c['best_beats_S0']), p['harm'], p['ls0_best_eq_prod'],
                    p['ls0_changes_hpm'], p['gain'], i(c['S0_not_locmax']), str(int(p['n']) - int(p['prod_exact']))],
      lambda cs, ps: [S(cs, 'endpoint_beats_S0'), S(ps, 'end_beats_S0_in_prod_exact'), S(cs, 'best_beats_S0'), S(ps, 'harm'),
                      S(ps, 'ls0_best_eq_prod'), S(ps, 'ls0_changes_hpm'), S(ps, 'gain'), S(cs, 'S0_not_locmax'),
                      str(sum(int(p['n']) - int(p['prod_exact']) for p in ps))])
# (c) path geometry / certification
table('(c) Path in 𝓡_d and certification', ['S̃₀∈𝓡₀', 'S̃₀∈𝓡₂', 'path ⊂ 𝓡₀', 'path ⊂ 𝓡₁', 'path ⊂ 𝓡₂', 'progress-only path', 'path ⊂ Lat(S̃₀)',
                                            'hit move cap', 'endpoint certified (any model)', 'P(cert S₀ | scored S₀)',
                                            'miss: S₀ not LM', 'miss: 0 moves', 'miss: cap', 'miss: non-progress', 'miss: other'],
      lambda c, p: [i(c['in_R0']), i(c['in_R2']), i(c['path_in_R0']), i(c['path_in_R1']), i(c['path_in_R2']), i(c['path_progress']),
                    i(c['path_in_lat']), i(c['move_limit']), str(100 - int(float(c['move_limit']))), f(c['cert_given_scored']),
                    i(c['f_post_notlm']), i(c['f_zero']), i(c['f_cap']), i(c['f_nonprog']), str(int(float(c['f_other'])) + int(float(c['f_post_better'])))],
      lambda cs, ps: [S(cs, 'in_R0'), S(cs, 'in_R2'), S(cs, 'path_in_R0'), S(cs, 'path_in_R1'), S(cs, 'path_in_R2'), S(cs, 'path_progress'),
                      S(cs, 'path_in_lat'), S(cs, 'move_limit'), str(sum(100 - int(float(c['move_limit'])) for c in cs)),
                      f(sum(float(c['certified']) for c in cs) / sum(float(c['scored']) for c in cs)),
                      S(cs, 'f_post_notlm'), S(cs, 'f_zero'), S(cs, 'f_cap'), S(cs, 'f_nonprog'),
                      str(sum(int(float(c['f_other'])) + int(float(c['f_post_better'])) for c in cs))])
# (d) T38(b1) premises
table('(d) Empirical T38(b1) premises at S° = S̃₀', ['med Φ(S̃₀)', 'ℓ ≥ Φ(S̃₀)−1', '(M1) π₀(S̃₀) > ½', 'med π₀(S̃₀)', 'med π₀(𝓡₂) = b_n',
                                                 'med log₁₀π₀(S₀)', '(M2) lattice fits checked', '(M2) D_S on all of Lat', 'Φ=2 states failing D_S',
                                                 '(M3) min λ_min'],
      lambda c, p: [f(c['Phi_start_med'], 1).rstrip('0').rstrip('.'), i(c['cap_ok']), i(c['elig']), f(c['pi0_start_med'], 3), f(c['pi0_R2_med'], 2),
                    f(c['log10_pi0_S0_med'], 1), i(c['lat_checked']), i(c['lat_DS_all']), f(c['lat_phi2_fail_frac']), f(c['lam_min_min'])],
      lambda cs, ps: ['', S(cs, 'cap_ok'), S(cs, 'elig'), '', '', '', S(cs, 'lat_checked'), S(cs, 'lat_DS_all'), '',
                      f(min(float(c['lam_min_min']) for c in cs))])
open(os.path.join(res, 'report_tables.md'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))

"""f_aggregate.py: pooled counts from F1_raw.csv, F1X_raw.csv, F2_raw.csv -> F_aggregates.txt (pure aggregation)"""
import csv, collections
L = ["# F_aggregates.txt -- pooled counts from F1_raw.csv, F1X_raw.csv, F2_raw.csv (script f_aggregate.py)"]
for f in ('F1_raw.csv', 'F1X_raw.csv', 'F2_raw.csv'):
    R = list(csv.DictReader(open(f)))
    L.append(f"\n## {f}: {len(R)} runs")
    def grp(keyf):
        g = collections.defaultdict(list)
        for r in R: g[keyf(r)].append(r)
        return g
    for k, rs in sorted(grp(lambda r: int(r['n'])).items()):
        na = [float(r['na_max_gain']) for r in rs]; z = [float(r['maxZ2_minus_cstar']) for r in rs]
        sw = [float(r['tl_swap_max']) for r in rs]; dl = [float(r['tl_del_max']) for r in rs]
        ex = sorted(int(r['n_extras']) for r in rs)
        L.append(f"n={k}: runs {len(rs)}; NA violated (max add gain >= 0) {sum(v >= 0 for v in na)}/{len(rs)}; largest max-gain {max(na):.2f}, median per-run max-gain {sorted(na)[len(na)//2]:.2f}; "
                 f"runs with some tested Z^2 > c*_n(k): {sum(v > 0 for v in z)}/{len(rs)}; TL largest swap diff {max(sw):.1f}, deletion diff {max(dl):.1f}; "
                 f"S0 in start {sum(r['S0_in_start'] == 'True' for r in rs)}; start in Q {sum(r['start_in_Q'] == 'True' for r in rs)}; extras in P {sum(r['extras_in_P'] == 'True' for r in rs)}; "
                 f"|extras| min/median/max {ex[0]}/{ex[len(ex)//2]}/{ex[-1]}")
    if f == 'F1_raw.csv':
        for k, rs in sorted(grp(lambda r: r['id'].split('_')[1]).items()):
            na = [float(r['na_max_gain']) for r in rs]
            L.append(f"{k}: NA violated {sum(v >= 0 for v in na)}/{len(rs)}; |extras| {min(int(r['n_extras']) for r in rs)}-{max(int(r['n_extras']) for r in rs)}")
    L.append(f"TL: largest swap diff over all runs {max(float(r['tl_swap_max']) for r in R):.2f}; largest deletion diff {max(float(r['tl_del_max']) for r in R):.2f}")
    L.append(f"incremental-vs-bvs_core verification (worst NA pair): max abs diff {max(abs(float(r['na_max_gain']) - float(r['na_verified'])) for r in R):.2e}; (worst TL swap) {max(abs(float(r['tl_swap_max']) - float(r['tl_swap_verified'])) for r in R):.2e}")
open('F_aggregates.txt', 'w', encoding='utf-8').write("\n".join(L) + "\n")

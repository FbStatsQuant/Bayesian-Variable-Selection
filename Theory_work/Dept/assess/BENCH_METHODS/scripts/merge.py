"""Merge BENCH_METHODS worker rows into MATRIX.csv and count tables.

Usage: python3 -I merge.py <BENCH_METHODS dir>
Writes out/MATRIX.csv (paper x method, cells: C=competitor, P=proposed, G=gold, V=variant),
out/counts.tsv (method, n_competitor_papers, n_any_role, example papers), out/papers_merged.tsv.
"""
import csv, sys, os, glob, collections

D = sys.argv[1]
rows_dir = os.path.join(D, 'rows')
out_dir = os.path.join(D, 'out')
os.makedirs(out_dir, exist_ok=True)

ALIAS = {}  # optional method-key aliases filled after review
alias_path = os.path.join(D, 'aliases.tsv')
if os.path.exists(alias_path):
    for line in open(alias_path):
        if line.strip() and not line.startswith('#'):
            a, b = line.rstrip('\n').split('\t')[:2]
            ALIAS[a.strip()] = b.strip()

def read_tsv(path):
    with open(path, newline='') as f:
        r = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        hdr = next(r)
        hdr = [h.strip() for h in hdr]
        for row in r:
            if not row or not any(c.strip() for c in row):
                continue
            row += [''] * (len(hdr) - len(row))
            yield dict(zip(hdr, [c.strip() for c in row]))

papers = {}
for p in sorted(glob.glob(os.path.join(rows_dir, '*_papers.tsv'))):
    src = os.path.basename(p).replace('_papers.tsv', '')
    for d in read_tsv(p):
        k = d['paper_key']
        if k in papers:
            continue
        d['source'] = src
        papers[k] = d

DROPS = set()
if os.path.exists(os.path.join(D, 'drops.tsv')):
    for d in read_tsv(os.path.join(D, 'drops.tsv')):
        DROPS.add((d['paper_key'], d['method_key']))
EXCLUDE_PAPERS = {'Schafer2012'}  # thesis duplicates Schafer2013's comparisons
FREQ = set('''LASSO ADALASSO ENET RELAXED_LASSO SCAD MCP SIS HOLP FSTEP STEPWISE_IC BEST_SUBSET_MIO L0LEARN ABESS STABSEL KNOCKOFF SLOPE DEBIASED MS_SPLIT SQRT_LASSO DANTZIG TLP_OTHER_NONCONVEX RIDGE MARGINAL RF_ML
NEW:ADAENET NEW:BEST_SUBSET_LEAPS NEW:BH_OLS NEW:BH_SCREEN_OLS NEW:BOOT_LASSO NEW:CALIB_CCCP NEW:CAPME NEW:CLUMP_THRESHOLD NEW:CONDITIONAL_METHOD NEW:COVTEST NEW:CRT NEW:DATA_SPLIT_FDR NEW:DCSIS NEW:FLASH NEW:FORWARDSTOP NEW:GARROTE NEW:GAUSSIAN_MIRROR NEW:GIC NEW:GPRS NEW:GRADES NEW:GROUP_LASSO NEW:GROUP_SCAD_MCP NEW:HARD_THRESHOLD NEW:HIER_TESTING NEW:HLASSO NEW:IHT NEW:L0BNB NEW:L0_SHRINK NEW:LAD_LASSO NEW:LASSOSUM NEW:LMM_BLUP NEW:MNET NEW:MRCE NEW:NSC NEW:OLS_HARD NEW:ONESTEP_PLS NEW:PC_SIMPLE NEW:PMLE_STADLER NEW:POSI NEW:RECIPROCAL_LASSO NEW:RESID_BOOT_ADALASSO NEW:RIDGE_PROJ NEW:RRCS NEW:SDAR NEW:SEQ_LR_TOPK NEW:SIRS NEW:SPARSE_GROUP_LASSO NEW:SPCA_ELASTICNET NEW:TILTING NEW:UNILASSO NEW:ALPHA_INVESTING NEW:ALPHA_THRESHOLDING NEW:SUPERLEARNER'''.split())
def camp(m): return 'F' if m in FREQ else 'B'
ROLE = {'competitor': 'C', 'proposed': 'P', 'gold': 'G', 'variant': 'V'}
srcmap = {}
cells = collections.defaultdict(dict)  # paper -> method -> role letter
raw = collections.defaultdict(list)
for p in sorted(glob.glob(os.path.join(rows_dir, '*_methods.tsv'))):
    for d in read_tsv(p):
        k, m = d['paper_key'], d['method_key']
        if 'COPIED' in d.get('note','') or k in EXCLUDE_PAPERS or ((k, m) in DROPS and not p.endswith('OPUSFIX_methods.tsv')):
            continue
        m = ALIAS.get(m, m)
        role = ROLE.get(d['role'].lower(), '?')
        prev = cells[k].get(m)
        # precedence: P > C > G > V
        order = 'PCGV?'
        if prev is None or order.index(role) < order.index(prev):
            cells[k][m] = role
        raw[(k, m)].append(d)
        srcmap[k] = os.path.basename(p).split('_')[0]

pcamp = {}
for k in cells:
    props = [camp(m) for m, r in cells[k].items() if r == 'P']
    if props:
        pcamp[k] = max(set(props), key=props.count)
    else:
        pcamp[k] = {'SWEEP': '?'}.get(srcmap.get(k), '?')
for k in ('Hastie2020', 'Buhlmann2014', 'Dezeure2015'):  # frequentist comparison/review papers, no proposed method
    if k in pcamp: pcamp[k] = 'F'
methods = sorted({m for k in cells for m in cells[k]})
pkeys = sorted(cells, key=lambda k: (papers.get(k, {}).get('year', ''), k))
with open(os.path.join(out_dir, 'MATRIX.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['paper_key', 'year', 'venue', 'camp', 'read_level'] + methods)
    for k in pkeys:
        pp = papers.get(k, {})
        rl = pp.get('read_level', '') or 'full-text'
        mark = '' if rl == 'full-text' else '~'  # ~ = paper not read in full (abstract/citing-paper evidence)
        w.writerow([k, pp.get('year', ''), pp.get('venue', ''), pcamp[k], rl] + [(cells[k][m] + mark) if m in cells[k] else '' for m in methods])

cnt = []
for m in methods:
    comp = [k for k in pkeys if cells[k].get(m) == 'C']
    anyr = [k for k in pkeys if m in cells[k]]
    prop = [k for k in pkeys if cells[k].get(m) == 'P']
    cb = sum(1 for k in comp if pcamp[k] == 'B'); cf = sum(1 for k in comp if pcamp[k] == 'F')
    recent = sum(1 for k in comp if papers.get(k, {}).get('year', '0')[:4] >= '2015')
    cnt.append((m, len(comp), len(anyr), prop, comp, cb, cf, recent))
cnt.sort(key=lambda t: (-t[1], -t[2], t[0]))
with open(os.path.join(out_dir, 'counts.tsv'), 'w') as f:
    f.write('method\tcamp\tn_competitor\tin_bayes_papers\tin_freq_papers\tsince2015\tn_any\tproposed_in\tcompetitor_in\n')
    for m, c, a, prop, comp, cb, cf, rc in cnt:
        f.write(f"{m}\t{camp(m)}\t{c}\t{cb}\t{cf}\t{rc}\t{a}\t{';'.join(prop)}\t{';'.join(comp)}\n")

with open(os.path.join(out_dir, 'papers_merged.tsv'), 'w') as f:
    keys = ['paper_key', 'authors', 'year', 'title', 'venue', 'doi', 'arxiv', 'read_level', 'has_sims', 'p_max', 'local_pdf', 'note', 'source']
    f.write('\t'.join(keys) + '\n')
    for k in sorted(papers, key=lambda k: (papers[k].get('year', ''), k)):
        f.write('\t'.join(papers[k].get(x, '') for x in keys) + '\n')

missing = [k for k in cells if k not in papers]
print('papers', len(papers), 'with cells', len(cells), 'methods', len(methods), 'cells', sum(len(v) for v in cells.values()))
print('cells without paper row:', missing)
import collections as C
print('paper camps', C.Counter(pcamp.values()), 'unknown:', [k for k in pcamp if pcamp[k]=='?'])
for m, c, a, prop, comp, cb, cf, rc in cnt[:45]:
    print(f'{m:24s} {camp(m)} comp={c:3d} B={cb:3d} F={cf:3d} >=2015={rc:3d} any={a:3d}')
with open(os.path.join(out_dir, 'paper_camp.tsv'), 'w') as f:
    for k in sorted(pcamp): f.write(f'{k}\t{pcamp[k]}\n')

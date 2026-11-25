import csv, sys, os
os.chdir(sys.argv[1])
pap=list(csv.DictReader(open('out/papers_merged.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE))
camp=dict(l.rstrip('\n').split('\t') for l in open('out/paper_camp.tsv'))
r=list(csv.reader(open('out/MATRIX.csv'))); h=r[0]
cells={row[0]:{h[i]:row[i] for i in range(5,len(h)) if row[i]} for row in r[1:]}
L=['# BENCH_METHODS: papers in the method × paper matrix','',
f'This file lists {len(pap)} papers.',
'',
'**Source** of each paper:',
'- CORPUS: the BENCH_DESIGN corpus (89 papers) plus the SMC_LIT method papers.',
'- SWEEP_B and SWEEP_F: the targeted 2010–2026 Bayesian and frequentist sweeps.',
'- PAYFIX: papers rebuilt after the paywall.',
'',
'**Columns:**',
'- **read**: `full-text` unless shown otherwise. `partial` means the paper was not read in full; its evidence comes from the abstract or from citing papers, and its cells carry a `~` in MATRIX.csv.',
'- **camp**: B (Bayesian) or F (frequentist), taken from the paper\'s own proposed method.',
'- **methods**: the role letter, then the method key. P = proposed, C = competitor, G = gold standard or reference, V = variant or ablation.',
'',
'No PDFs are committed.','',
'| key | year | venue | citation | DOI / arXiv | read | camp | methods |','|---|---|---|---|---|---|---|---|']
for d in sorted(pap,key=lambda d:(d['year'],d['paper_key'])):
    k=d['paper_key']; c=cells.get(k,{})
    ms='; '.join(f"{v}:{m}" for m,v in sorted(c.items(),key=lambda t:(t[1],t[0]))) or '— (no comparison run)'
    ax=(d['arxiv'] or '').replace('arXiv:','')
    ident=' / '.join(x for x in [d['doi'] or '', ('arXiv:'+ax) if ax else ''] if x)
    cit=f"{d['authors']}. {d['title']}".replace('|','/')
    L.append(f"| {k} | {d['year']} | {d['venue']} | {cit} | {ident} | {d['read_level'] or 'full-text'} | {camp.get(k,'-')} | {ms} |")
open('out/PAPERS.md','w').write('\n'.join(L)+'\n')
print(len(pap))

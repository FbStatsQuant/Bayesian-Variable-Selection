from pathlib import Path
import hashlib,re,sys
sys.stdout.reconfigure(encoding='utf-8')
C=Path('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign');S=C/'code/bench_v2/review/sol_scripts_r2';report=S.parent/'SOL_REVIEW_2.md'
text=report.read_text(encoding='utf-8');assert '](' in text and '[](' not in text
for target in re.findall(r'\]\(([^)]+)\)',text):
    m=re.match(r'^(.*?)(?::([0-9]+))?$',target);p=Path(m[1]);assert p.exists(),target
    if m[2]:assert int(m[2])<=len(p.read_text(encoding='utf-8-sig').splitlines()),target
for line in (S/'DELIVERABLE_SNAPSHOT_SHA256.txt').read_text().splitlines():
    h,rel=line.split('  ',1);assert hashlib.sha256((C/rel).read_bytes()).hexdigest()==h,rel
evidence=[p for p in S.rglob('*') if p.is_file() and 'tmp' not in p.relative_to(S).parts and p.name!='REVIEW_EVIDENCE_SHA256.txt']+[report]
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(S.parent)).replace('\\','/')+'\n' for p in sorted(evidence)]
(S/'REVIEW_EVIDENCE_SHA256.txt').write_text(''.join(lines),encoding='utf-8')
print('REPORT_LINKS_AND_LINE_TARGETS PASS; reviewed deliverables unchanged; evidence hashed',len(lines))
print('REPORT_SHA256',hashlib.sha256(report.read_bytes()).hexdigest())

import pathlib,hashlib,datetime
P=pathlib.Path
V=P('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review')
S=V/'sol_scripts'
files=sorted([V/'SOL_REVIEW_1.md']+[f for f in S.iterdir() if f.is_file() and f.suffix in ('.R','.py','.ps1','.log','.exit')])
text=''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(V).as_posix()}\n' for f in files)
(S/'REVIEW_EVIDENCE_SHA256.txt').write_text(text,encoding='utf-8')
print(datetime.datetime.now(datetime.timezone.utc).isoformat(),len(files),'review/evidence hashes written')

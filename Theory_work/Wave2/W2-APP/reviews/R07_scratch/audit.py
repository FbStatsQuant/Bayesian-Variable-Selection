from pathlib import Path
import csv, io, contextlib, builtins, hashlib, json, math
import numpy as np
from scipy.stats import beta
root=Path.cwd(); app=root/'Theory_work/Wave2/W2-APP'; scratch=app/'reviews/R07_scratch'
# Run citation checker with its sole write redirected into authorized scratch.
oldopen=builtins.open
def auditopen(file,mode='r',*a,**k):
    if 'w' in mode and Path(file).resolve()==(app/'reviews/CITECHECK.txt').resolve():
        file=scratch/'citecheck_rerun.txt'
    return oldopen(file,mode,*a,**k)
class Sink(io.StringIO):
    def reconfigure(self,**kwargs): pass
builtins.open=auditopen
try:
    with contextlib.redirect_stdout(Sink()):
        exec(compile((app/'citecheck.py').read_text(encoding='utf8'),str(app/'citecheck.py'),'exec'),{'__file__':str(app/'citecheck.py'),'__name__':'__main__'})
finally: builtins.open=oldopen
print('CITECHECK:',(scratch/'citecheck_rerun.txt').read_text(encoding='utf8').splitlines()[-1])
# Independently compare all snapshot source bytes to current production.
copy=app/'data_diag/core_copy'; core=root/'Scripts/SMC_BVS/core'
mismatch=[]; checked=0
for f in copy.rglob('*'):
    if not f.is_file() or f.name=='SOURCE_SHA256.txt': continue
    other=core/f.relative_to(copy)
    if other.is_file():
        checked+=1
        if f.read_bytes()!=other.read_bytes(): mismatch.append(str(f.relative_to(copy)))
print('CORE COPY',checked,'source files compared; mismatches',mismatch)
for fn in ['n2_results.csv','n3_merged.csv']:
    rows=list(csv.DictReader((app/'numerics'/fn).open()))
    print(fn,'rows',len(rows),'fields',list(rows[0]))
    for did in sorted({r['design'] for r in rows}):
        rr=[r for r in rows if r['design']==did]
        print(did,'runs',len(rr),'n,p',sorted({(int(r['n']),int(r['p'])) for r in rr}), 'mode sizes',min(int(r['mode_size']) for r in rr),max(int(r['mode_size']) for r in rr),'S0 endpoint',sum(r['ls_final_eq_S0']=='True' for r in rr),'extras',min(int(r['n_extra']) for r in rr),max(int(r['n_extra']) for r in rr))
for tau in [.3,.5,.7]:
    prob=beta.sf(tau*tau,.5,(71-2)/2)
    print('riboflavin iid Gaussian null tau',tau,'pair probability',prob,'expected pairs',prob*4088*4087/2)
kE=.52*12*(2+1)+1
print('V1 kappa_E',kE,'twice',2*kE,'corrected optimistic margin at n12800 p200',6.67-2*kE)
# One fixed-p counterexample to an alleged exclusion from all fixed-floor classes.
print('tecator positive observed floor, repeated fixed-p sequence has constant c=1.69874931695267e-11')
print('Missing onset script',not (app/'numerics/vn_onset.py').exists())
print('Empirical table cell counts',[(i,len(line.split('|'))-2) for i,line in enumerate((app/'EMPIRICAL.md').read_text(encoding='utf8').splitlines(),1) if 24<=i<=33])

# Extra counterexample checks for the review.
R3=np.array([[1,.3,.6],[.3,1,.5],[.6,.5,1.]])
print('Marginal-vs-partial counterexample spectrum',np.linalg.eigvalsh(R3).tolist(),'Cov(W1,W2 | W3)',R3[0,1]-R3[0,2]*R3[2,1])
R2=np.array([[1,.5],[.5,1.]])
print('Missing PTV counterexample, theta=(1,-2): Sigma theta',R2@np.array([1.,-2.]))
for fn in ['out_diabetes_quad_sparse_eig.csv','out_spam_sparse_eig.csv','out_digits_sparse_eig.csv','out_fred_qd_sparse_eig.csv']:
    rr=list(csv.DictReader((app/'data_diag'/fn).open()))
    print('SPOT',fn,[(r['k'],r['exact'],r['upper_best'],r['lambda_minR_lower']) for r in rr if int(r['k']) in (2,3,7,8,9)])
r=list(csv.DictReader((app/'numerics/n2_results.csv').open()))
print('n2 checks: inclusion',sum(x['S0_in_mode']=='True' for x in r),'scored',sum(x['ls_S0_scored']=='True' for x in r),'certified',sum(x['ls_certified']=='True' for x in r),'moves=extras',sum(x['ls_moves']==x['n_extra'] for x in r))

# S1-S2 compute estimate (EXPERIMENT_PLAN §6A, v0.4). Pure arithmetic on measured anchors; no job, no ssh. Run: python3 -I s1s3_compute_estimate.py
# v0.4 (owner 11-25): S3 is DROPPED. INCLUDE_S3 = False is the default; INCLUDE_S3 = True reproduces the v0.3 numbers (11,813 central) as a regression check.
# (File name kept from v0.3 because EXPERIMENT_PLAN and LOG cite it.)
# Anchors: A=44.0 (OVERLAP_1e4_VERDICT §4), F2 1.4 core-h at p=1e4 (science_per_fit.csv), tier multipliers from the same verdict.
import sys
INCLUDE_S3 = ('--with-s3' in sys.argv)
A=44.0            # billed core-h per T fit at p=1e4,n=200 (879.08/20, measured)
T0=33.2; T1=104.9
E1=T1/A; E0=T0/A  # tier-1 / tier-0 multipliers vs mixture mean
def Nlaw(n,p): return max(2500,n,p)
def Tbase(n,p): return A*Nlaw(n,p)*p/1e8
def nfac(n,case):
    if n<=200: return 1.0
    return {'low':0.8,'c':1.25,'high':(1+n/400)/1.5}[case]
# escalation multipliers per class (low,c,high)
ESC={'S1':(E0,1.0,1.40),'S2n50':(1.57,E1,3.27),'S2n100':(1.0,1.57,3.27),'S3':(1.57,E1,3.27)}
AM={'low':0.7,'c':1.0,'high':1.6}
IDX={'low':0,'c':1,'high':2}
def tcost(cls,n,p,case):
    return Tbase(n,p)*AM[case]*nfac(n,case)*ESC[cls][IDX[case]]
def fcost(p,case):
    m={'low':0.5,'c':1.0,'high':3.0}[case]
    return max(0.10,1.4*p/1e4)*m
# cells
S1=[(n,p,snr) for n in (500,1000) for p in (500,5000) for snr in (.5,1,2,3)]
S2=[(rho,n,p,s,bt,nu) for rho in (0,.35,.7) for (n,p,s) in ((50,1000,5),(100,1000,10)) for bt in (1,2) for nu in range(10)]
S3=[(rho,s0,n,p,snr) for rho in (.5,.8) for s0 in (5,10) for (n,p) in ((500,500),(500,5000),(1000,500),(1000,5000)) for snr in (1,2)] if INCLUDE_S3 else []
EC=2   # block E: 2 cells (S1 n=500,p=5000, SNR 1,2), 1 data set x 50 engine seeds
SUITES=['S1','S2']+(['S3'] if INCLUDE_S3 else [])
print('INCLUDE_S3 =',INCLUDE_S3,'| cells S1',len(S1),'S2',len(S2),'S3',len(S3),'E',EC,'| total cells',len(S1)+len(S2)+len(S3)+EC)
def t2cls(c): return 'S2n50' if c[1]==50 else 'S2n100'
def freq(n,p): return max(0.01,0.1*n*p/(1000*5000))
def mcmc(p): return max(0.05,0.33*p/5000)
def run(R_F=50,R_T=10,case='c',s2_bt=2):
    """s2_bt = number of S2 beta-types used (2 = all 120 cells; 1 = lever 'beta-type 1 only')."""
    s2=[c for c in S2 if c[4]<=s2_bt]
    f={'S1':sum(R_F*fcost(p,case) for n,p,_ in S1),
       'S2':sum(R_F*fcost(1000,case) for c in s2)}
    t={'S1':sum(R_T*tcost('S1',n,p,case) for n,p,_ in S1),
       'S2':sum(R_T*tcost(t2cls(c),c[1],1000,case) for c in s2)}
    cm={'low':0.4,'c':1.0,'high':4.0}[case]
    c={'S1':sum(R_F*(freq(n,p)+mcmc(p)) for n,p,_ in S1)*cm,
       'S2':sum(R_F*freq(c[1],1000) for c in s2)*cm}
    if INCLUDE_S3:
        f['S3']=sum(R_F*fcost(p,case) for (_,_,n,p,_) in S3)
        t['S3']=sum(R_T*tcost('S3',n,p,case) for (_,_,n,p,_) in S3)
        c['S3']=sum(R_F*(freq(n,p)+mcmc(p)) for (_,_,n,p,_) in S3)*cm
    # block E: 2 cells (n=500,p=5000, SNR 1,2) x 50 seeds F2; baselines 4 MCMC x 50 runs x 2 cells + 20 (gold standard) as in v0.3
    f['E']=100*fcost(5000,case)
    c['E']=(2*50*mcmc(5000)*1+20)*cm
    return f,t,c
def tot(d): return sum(d.values())
def R(d): return {k:round(v) for k,v in d.items()}
print('\n=== 6A.1 fit counts')
ncell={'S1':len(S1),'S2':len(S2),'S3':len(S3)}
for RF,RT in [(50,10)]:
    for s in SUITES:
        nd=RF*ncell[s]; print(s,'cells',ncell[s],'data sets',nd,'F2 fits',nd,'T fits',RT*ncell[s],'freq/VB fits (5 methods)',5*nd,'MCMC runs (4 methods)',(4*nd if s!='S2' else 0))
    print('E cells',EC,'F2 fits',100,'MCMC runs',4*100)
    nd=RF*sum(ncell[s] for s in SUITES); nt=RT*sum(ncell[s] for s in SUITES)
    print('TOTAL cells',sum(ncell[s] for s in SUITES)+EC,'data sets',nd+2,'F2 fits',nd+100,'T fits',nt,'SMC fits',nd+100+nt,
          'freq/VB fits',5*nd,'MCMC runs',4*RF*sum(ncell[s] for s in SUITES if s!='S2')+400)
print('\n=== 6A.4 totals by suite and engine (billed core-h)')
res={}
for case in ('low','c','high'):
    res[case]=run(case=case)
    f,t,c=res[case]
    print(case,'F2',R(f),round(tot(f)),'| T',R(t),round(tot(t)),'| comp',R(c),round(tot(c)),'| TOTAL',round(tot(f)+tot(t)+tot(c)))
print('per-suite totals (low / central / high):')
for s in SUITES+['E']:
    row=[]
    for case in ('low','c','high'):
        f,t,c=res[case]; row.append(round(f.get(s,0)+t.get(s,0)+c.get(s,0)))
    f,t,c=res['c']
    print(' ',s,'F2',round(f.get(s,0)),'T',round(t.get(s,0)),'comp',round(c.get(s,0)),'| total low/c/high',row)
f,t,c=res['c']; T=tot(f)+tot(t)+tot(c)
print('central by engine: T',round(tot(t)),f'({100*tot(t)/T:.0f}%)','F2',round(tot(f)),f'({100*tot(f)/T:.0f}%)','comp',round(tot(c)),f'({100*tot(c)/T:.0f}%)')
print('central T by suite share:',{k:f'{100*v/tot(t):.0f}%' for k,v in t.items()})
print('\n=== 6A.3 per-fit tables (central)')
for n,p in [(500,500),(1000,500),(500,5000),(1000,5000)]:
    print('S1',n,p,'T',round(tcost('S1',n,p,'c'),2),'F2',round(fcost(p,'c'),2))
print('S2 n50 T',round(tcost('S2n50',50,1000,'c'),2),'n100 T',round(tcost('S2n100',100,1000,'c'),2),'F2',round(fcost(1000,'c'),2))
if INCLUDE_S3:
    for n,p in [(500,500),(1000,500),(500,5000),(1000,5000)]: print('S3',n,p,'T',round(tcost('S3',n,p,'c'),2))
for lab,cl,n,p_ in [('S1 p=500','S1',500,500),('S1 p=5000','S1',500,5000),('S2 n=50','S2n50',50,1000),('S2 n=100','S2n100',100,1000)]:
    print('T/F2 ratio',lab,round(tcost(cl,n,p_,'c')/fcost(p_,'c')))
print('S2 mean T per fit (central)',round(sum(tcost(t2cls(c),c[1],1000,'c') for c in S2)/len(S2),2),'| S1 mean T per fit',round(sum(tcost('S1',n,p,'c') for n,p,_ in S1)/len(S1),2))
print('S1 T by p (10 fits/cell, central): p=500',round(sum(10*tcost('S1',n,p,'c') for n,p,_ in S1 if p==500)),'p=5000',round(sum(10*tcost('S1',n,p,'c') for n,p,_ in S1 if p==5000)))
print('S2 T by n (10 fits/cell, central): n=50',round(sum(10*tcost('S2n50',50,1000,'c') for c in S2 if c[1]==50)),'n=100',round(sum(10*tcost('S2n100',100,1000,'c') for c in S2 if c[1]==100)))
print('\n=== cost-driver breakdown (central)')
TT=tot(res['c'][1]); TOT=tot(res['c'][0])+tot(res['c'][1])+tot(res['c'][2])
s2t=res['c'][1]['S2']; s1t=res['c'][1]['S1']
s2n50=sum(10*tcost('S2n50',50,1000,'c') for c in S2 if c[1]==50)
s2n50_noesc=s2n50/ESC['S2n50'][1]
s1p5=sum(10*tcost('S1',n,p,'c') for n,p,_ in S1 if p==5000)
print('S2 T bridge',round(s2t),f'= {100*s2t/TOT:.0f}% of the central total, {100*s2t/TT:.0f}% of the T bridge')
print('  of which n=50 cells',round(s2n50),f'({100*s2n50/s2t:.0f}% of S2 T); same cells with no escalation (factor 1)',round(s2n50_noesc),'-> escalation adds',round(s2n50-s2n50_noesc))
print('S1 T bridge at p=5000',round(s1p5),f'= {100*s1p5/TOT:.0f}% of the central total, {100*s1p5/TT:.0f}% of the T bridge')
print('S2 n=50 + S1 p=5000 T together',round(s2n50+s1p5),f'= {100*(s2n50+s1p5)/TOT:.0f}% of the central total')
print('E block (F2 + competitors)',round(res['c'][0]['E']+res['c'][2]['E']))
print('v0.3 reference: S3 T bridge was 5507 (59% of the v0.3 T bridge) -- run with --with-s3 to reproduce')
print('\n=== 6A.6 replicate alternatives (central)')
for RF,RT in [(20,10),(50,10),(100,10),(50,20),(50,50),(100,50)]:
    f,t,c=run(RF,RT,'c'); nc=sum(ncell[s] for s in SUITES)
    print('RF',RF,'RT',RT,'SMC fits',RF*nc+100+RT*nc,'F2',round(tot(f)),'T',round(tot(t)),'comp',round(tot(c)),'tot',round(tot(f)+tot(t)+tot(c)))
for RF,RT in [(50,20),(50,50),(100,10)]:
    f,t,c=run(RF,RT,'c'); v=tot(f)+tot(t)+tot(c); print('share of remaining 22,258: RF',RF,'RT',RT,round(v),f'{100*v/22258:.0f}%')
print('levers (central, saving vs the 50/10 design):')
base=tot(res['c'][0])+tot(res['c'][1])+tot(res['c'][2])
l1=sum(5*tcost('S1',n,p,'c') for n,p,_ in S1 if p==5000)
print('  (a) T bridge at S1 p=5000, 10 -> 5 per cell: saves',round(l1))
l2=sum(5*tcost(t2cls(c),c[1],1000,'c') for c in S2)
print('  (b) T bridge on S2, 10 -> 5 per cell: saves',round(l2))
l2n=sum(10*tcost('S2n50',50,1000,'c') for c in S2 if c[1]==50)
print('  (b2) T bridge on S2 at n=50 only dropped (T at S2 n=100 only): saves',round(l2n))
f1,t1,c1=run(case='c',s2_bt=1); b1=tot(f1)+tot(t1)+tot(c1)
print('  (c) S2 beta-type 1 only (60 cells): saves',round(base-b1),'; total',round(b1))
l3=sum(5*tcost('S1',n,p,'c') for n,p,_ in S1 if p==5000)+sum(5*tcost(t2cls(c),c[1],1000,'c') for c in S2)
print('  (a)+(b) together saves',round(l3),'; total',round(base-l3))
print('\n=== counts for RF 20/100 and RT 50')
for RF,RT in [(20,10),(100,10),(50,50)]:
    nc=sum(ncell[s] for s in SUITES); print('RF',RF,'RT',RT,'SMC fits',RF*nc+100+RT*nc)
print('\n=== 6A.7 by machine (Owls conversions as in v0.3: T single-thread x0.97, F2 x1.5 if an Owls build existed, comp x1.0)')
split={}
for case in ('low','c','high'):
    Tsmall=sum(10*tcost('S1',n,p,case) for n,p,_ in S1 if p<=1000)+sum(10*tcost(t2cls(c),c[1],1000,case) for c in S2)+(sum(10*tcost('S3',n,p,case) for (_,_,n,p,_) in S3 if p<=1000) if INCLUDE_S3 else 0)
    Tbig=sum(10*tcost('S1',n,p,case) for n,p,_ in S1 if p>1000)+(sum(10*tcost('S3',n,p,case) for (_,_,n,p,_) in S3 if p>1000) if INCLUDE_S3 else 0)
    f,t,c=res[case]; F=tot(f); C=tot(c)
    split[case]=dict(Tsmall=Tsmall,Tbig=Tbig,F=F,C=C)
    print(case,'Tsmall',round(Tsmall),'Tbig',round(Tbig),'F2',round(F),'comp',round(C),
      '| owls Tsmall(x0.97)',round(Tsmall*0.97),'owls F2 (x1.5)',round(F*1.5),'owls comp',round(C),'| Tbig owls synth',round(Tbig*0.97),'ribo-anchor (x10)',round(Tbig*0.97*10),
      '| NOTS recommended (F2+Tbig)',round(F+Tbig),'| Owls recommended (Tsmall x0.97 + comp)',round(Tsmall*0.97+C),'| all NOTS',round(F+Tbig+Tsmall+C))
print('Owls days at 230 core-h/day: Tsmall(c)',round(split['c']['Tsmall']*0.97/230,1),'; Owls recommended total (c)',round((split['c']['Tsmall']*0.97+split['c']['C'])/230,1),'; Tbig synth (c)',round(split['c']['Tbig']*0.97/230,1))
print('ribo p=5000 scale (core-h per fit)',round(88*(5000**2)/(4088**2),1))
print('\n=== 6A.8 envelope')
ENV=28300; CLOSED=6042; REM=ENV-CLOSED
print('remaining',REM)
for lab,key,val in [('central all NOTS','c',lambda s:s['F']+s['Tbig']+s['Tsmall']+s['C']),('central recommended split','c',lambda s:s['F']+s['Tbig']),
                    ('low all NOTS','low',lambda s:s['F']+s['Tbig']+s['Tsmall']+s['C']),('high all NOTS','high',lambda s:s['F']+s['Tbig']+s['Tsmall']+s['C']),
                    ('low recommended','low',lambda s:s['F']+s['Tbig']),('high recommended','high',lambda s:s['F']+s['Tbig'])]:
    v=val(split[key]); print(f'{lab}: {v:.0f}  share of remaining {100*v/REM:.0f}%  share of envelope (cum. with closed) {100*(v+CLOSED)/ENV:.0f}%')
vc=sum(split['c'][k] for k in ('F','Tbig','Tsmall','C'))
print('25% reserve on the central all-NOTS total:',round(1.25*vc),'| on recommended:',round(1.25*(split['c']['F']+split['c']['Tbig'])))

# ---- 6A.9 calibration pilot (re-based on S1/S2, v0.4) ----
print('\n=== 6A.9 calibration pilot (T = theorem-covered method, F2 on the same data sets + F2-only floor fits)')
# (label, engine, n, p, cost class, number of fits)
PILOT_T=[('T1 S1 n=500 p=5000 (SNR 1,2 x 2 seeds)', 500,5000,'S1',4),
         ('T2 S1 n=1000 p=5000 (SNR 1,2 x 1 seed)', 1000,5000,'S1',2),
         ('T3 S1 n=500 p=500 (f_n at p=500)', 500,500,'S1',3),
         ('T4 S1 n=1000 p=500 (f_n at p=500)', 1000,500,'S1',3),
         ('T5 S2 n=50 p=1000 (rho in {0,.35,.7}, mid-grid nu)', 50,1000,'S2n50',5),
         ('T6 S2 n=100 p=1000 (same)', 100,1000,'S2n100',5)]
PILOT_F=[('F1 p=500 (6 paired with T3/T4 + 10 F2-only)',500,16),
         ('F2 p=1000 (10 paired with T5/T6 + 10 F2-only)',1000,20),
         ('F3 p=5000 (6 paired with T1/T2)',5000,6)]
pt={}
for case in ('low','c','high'):
    tt=[sum(k*tcost(cl,n,p,case) for (_,n,p,cl,k) in PILOT_T[i:i+1]) for i in range(len(PILOT_T))]
    ff=[k*fcost(p,case) for (_,p,k) in PILOT_F]
    pt[case]=(tt,ff)
for i,(lab,n,p,cl,k) in enumerate(PILOT_T):
    print(f'{lab}: {k} fits; per fit low/c/high {tcost(cl,n,p,"low"):.2f}/{tcost(cl,n,p,"c"):.2f}/{tcost(cl,n,p,"high"):.2f}; total low/c/high',[round(pt[c][0][i],1) for c in ('low','c','high')])
for i,(lab,p,k) in enumerate(PILOT_F):
    print(f'{lab}: {k} fits; per fit c {fcost(p,"c"):.2f}; total low/c/high',[round(pt[c][1][i],1) for c in ('low','c','high')])
for case in ('low','c','high'):
    tt,ff=pt[case]; print(case,'pilot T',round(sum(tt),1),'F2',round(sum(ff),1),'TOTAL',round(sum(tt)+sum(ff),1))
nT=sum(k for *_,k in PILOT_T); nF=sum(k for *_,k in PILOT_F)
print('pilot fits: T',nT,'F2',nF,'total',nT+nF)
print('stage 1 (cheap: T3,T4,T5,T6 + all F2 at p<=1000), central:',round(sum(pt['c'][0][i] for i in (2,3,4,5))+pt['c'][1][0]+pt['c'][1][1],1))
print('stage 2 (p=5000: T1,T2 + F3), central:',round(pt['c'][0][0]+pt['c'][0][1]+pt['c'][1][2],1))
print('pilot as share of 200 core-h exploratory authority: central',round(100*(sum(pt['c'][0])+sum(pt['c'][1]))/200),'% high',round(100*(sum(pt['high'][0])+sum(pt['high'][1]))/200),'%')
print('P6 observation, 16 h wall for a cs fit at n=100,p=1000 (billed core-h at 2 CPUs):',16*2)
print('pilot as share of the central total:',round(100*(sum(pt['c'][0])+sum(pt['c'][1]))/(tot(res['c'][0])+tot(res['c'][1])+tot(res['c'][2])),1),'%')
# pilot by machine (T at p<=1000 is the R core on Owls, F2 and T at p=5000 are NOTS; Owls T x0.97)
print('\n=== 6A.9 pilot by machine')
for case in ('low','c','high'):
    tt,ff=pt[case]
    nots=tt[0]+tt[1]+sum(ff); owls=0.97*(tt[2]+tt[3]+tt[4]+tt[5])
    print(case,'NOTS billed (T1+T2+all F2)',round(nots,1),'| Owls core-h (T3..T6 x0.97)',round(owls,1),'| all-NOTS equivalent',round(sum(tt)+sum(ff),1))
print('P(no escalation in 6 fits at a 15% incidence) =',round(0.85**6,2))
print('Owls days at 230/day: riboflavin-anchor T p=5000 (c):',round(split['c']['Tbig']*0.97*10/230,1))
print('pilot Owls days at 230/day (c):',round(0.97*(pt['c'][0][2]+pt['c'][0][3]+pt['c'][0][4]+pt['c'][0][5])/230,2))

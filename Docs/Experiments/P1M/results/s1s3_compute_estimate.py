# S1-S3 compute estimate (EXPERIMENT_PLAN §6A). Pure arithmetic on measured anchors; no job, no ssh. Run: python3 -I s1s3_compute_estimate.py
# Anchors: A=44.0 (OVERLAP_1e4_VERDICT §4), F2 1.4 core-h at p=1e4 (science_per_fit.csv), tier multipliers from the same verdict.
import itertools, json
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
S3=[(rho,s0,n,p,snr) for rho in (.5,.8) for s0 in (5,10) for (n,p) in ((500,500),(500,5000),(1000,500),(1000,5000)) for snr in (1,2)]
print(len(S1),len(S2),len(S3))
def run(R_F=50,R_T=10,case='c'):
    out={}
    # F2
    f={'S1':sum(R_F*fcost(p,case) for n,p,_ in S1),
       'S2':sum(R_F*fcost(1000,case) for c in S2),
       'S3':sum(R_F*fcost(p,case) for (_,_,n,p,_) in S3)}
    # efficiency block: 2 cells (n=500,p=5000, SNR 1,2) x 50 seeds F2
    f['E']=100*fcost(5000,case)
    t={'S1':sum(R_T*tcost('S1',n,p,case) for n,p,_ in S1),
       'S2':sum(R_T*tcost('S2n50' if c[1]==50 else 'S2n100',c[1],1000,case) for c in S2),
       'S3':sum(R_T*tcost('S3',n,p,case) for (_,_,n,p,_) in S3)}
    # competitors
    def freq(n,p): return max(0.01,0.1*n*p/(1000*5000))
    def mcmc(p): return max(0.05,0.33*p/5000)
    cm={'low':0.4,'c':1.0,'high':4.0}[case]
    c={'S1':sum(R_F*(freq(n,p)+mcmc(p)) for n,p,_ in S1)*cm,
       'S2':sum(R_F*freq(c[1],1000) for c in S2)*cm,
       'S3':sum(R_F*(freq(n,p)+mcmc(p)) for (_,_,n,p,_) in S3)*cm,
       'E':(2*50*mcmc(5000)*1+20)*cm}
    return f,t,c
for case in ('low','c','high'):
    f,t,c=run(case=case)
    print(case,'F2',{k:round(v) for k,v in f.items()},round(sum(f.values())),'T',{k:round(v) for k,v in t.items()},round(sum(t.values())),'comp',{k:round(v) for k,v in c.items()},round(sum(c.values())),'TOTAL',round(sum(f.values())+sum(t.values())+sum(c.values())))
# per-fit tables (central)
for n,p in [(500,500),(1000,500),(500,5000),(1000,5000)]:
    print('S1',n,p,'T',round(tcost('S1',n,p,'c'),2),'F2',round(fcost(p,'c'),2))
print('S2 n50 T',round(tcost('S2n50',50,1000,'c'),2),'n100 T',round(tcost('S2n100',100,1000,'c'),2),'F2',round(fcost(1000,'c'),2))
for n,p in [(500,500),(1000,500),(500,5000),(1000,5000)]:
    print('S3',n,p,'T',round(tcost('S3',n,p,'c'),2))
# alternatives (central cost): R_F 20/50/100, R_T 0/10/20/50
for RF,RT in [(20,10),(50,10),(100,10),(50,20),(50,50),(100,50)]:
    f,t,c=run(RF,RT,'c'); print('RF',RF,'RT',RT,'F2',round(sum(f.values())),'T',round(sum(t.values())),'comp',round(sum(c.values())),'tot',round(sum(f.values())+sum(t.values())+sum(c.values())))
# counts
for RF,RT in [(50,10),(100,10),(20,10),(50,50)]:
    nd=RF*(len(S1)+len(S2)+len(S3)); nt=RT*(len(S1)+len(S2)+len(S3)); print('datasets',nd,'T fits',nt,'F2 fits',nd+100,'SMC total',nd+100+nt)
print('--- owls split')
for case in ('low','c','high'):
    Tsmall=sum(10*tcost('S1',n,p,case) for n,p,_ in S1 if p<=1000)+sum(10*tcost('S2n50' if c[1]==50 else 'S2n100',c[1],1000,case) for c in S2)+sum(10*tcost('S3',n,p,case) for (_,_,n,p,_) in S3 if p<=1000)
    Tbig=sum(10*tcost('S1',n,p,case) for n,p,_ in S1 if p>1000)+sum(10*tcost('S3',n,p,case) for (_,_,n,p,_) in S3 if p>1000)
    f,t,c=run(case=case)
    F=sum(f.values()); C=sum(c.values())
    print(case,'Tsmall',round(Tsmall),'Tbig',round(Tbig),'F2',round(F),'comp',round(C),
      'owls Tsmall(x0.97)',round(Tsmall*0.97),'owls F2 (x1.5)',round(F*1.5),'owls comp(x1.93/..)',round(C*1.0))
    # Tbig on owls: synthetic anchor x0.97, riboflavin anchor x10
    print('   Tbig owls synth',round(Tbig*0.97),'ribo-anchor',round(Tbig*0.97*10))
# T-only per suite central
f,t,c=run(case='c'); print(t, f, c)
# riboflavin anchor
print('ribo p=5000 scale',88*(5000**2)/(4088**2))
print('env remaining',28300-6042, 'share central', 11813/(28300-6042))

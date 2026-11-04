"""W2 PC1: new-clause checks only; no re-proof of inherited checked propositions.

Local Python 3; seeds 0..9 only. Run with PYTHONDONTWRITEBYTECODE=1.
Outputs remain next to this script. Exact-Gram statistics are realised by a
centred design because z'G^{-1}z <= Y; the unused residual direction supplies Y.
"""
from pathlib import Path
import sys, math, json
import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'theory_campaign/MEET-THM/evidence/W1_PC2/scripts'))
import bvs_common as bc

OUT = {}

def grid(l0, d, theta=.9, targets=(1.,)):
    F = lambda t: float(logsumexp(l0+t*d))
    rho = lambda u,v: math.exp(2*F(v)-F(u)-F(2*v-u))
    u=0.; pts=[0.]
    for _ in range(1000):
        if u == 1.: return pts
        b=next(t for t in targets if t>u)
        if rho(u,b)>=theta: v=b
        else:
            lo,hi=u,b
            for _ in range(60):
                mid=(lo+hi)/2
                if rho(u,mid)>=theta:lo=mid
                else:hi=mid
            v=lo
        if v>=1-1e-12:v=1.
        if v<=u or rho(u,v)<theta-2e-13:
            raise RuntimeError('grid validation/nonprogress')
        pts.append(v);u=v
    raise RuntimeError('ceiling')

def bf(G,z,Y,n,S):
    return bc.log_m(G,z,Y,n,S)-bc.log_m(G,z,Y,n,[])

# D's new claim: at a threshold jump only the left/right counts can occur.
# Actual ridge/IG/BB target at n=40,p=2, with the method's B=1 blocks.
# Restrict V to {(0,), (0,1)}. Construct two simultaneous ESS=.9 boundaries.
q=.7; ell=np.log([1-q,q]); F=lambda t:float(logsumexp(ell+np.array([0.,t])))
rho=lambda u,v:math.exp(2*F(v)-F(u)-F(2*v-u))
a=brentq(lambda v:rho(0,v)-.9,.01,10,xtol=1e-14)
b=brentq(lambda v:rho(a,v)-.9,a+.01,10,xtol=1e-14)
n=40;Y=39.;Q=Y+.02;nu=n/2+.01
x2=1-math.exp(-(math.log(q/(1-q))+.5*math.log(n))/nu)
eb=math.exp(b/nu)
x1=(eb-1)*(1-x2)/(eb-1+x2)
z=np.sqrt(n*Q*np.array([x1,x2]));targets=(a/b,1.)
eps=1e-5;G=(n-1)*np.array([[1.,eps],[eps,1.]])
dtrue=bf(G,z,Y,n,[0,1])-bf(G,z,Y,n,[0])-bf(G,z,Y,n,[1])
logodds=bc.log_prior_w(2,2)-bc.log_prior_w(2,1)+bf(G,z,Y,n,[1])
assert abs(logodds-math.log(q/(1-q)))<1e-12
assert z@np.linalg.solve(G,z)<Y
assert bc.coded_partition(G,1)==[[0],[1]]
delta=eps;ubar=x1+x2
eta=2*-math.log1p(-delta)-nu*math.log1p(-delta*ubar/((1-delta)*(1-ubar)))
counts=[len(grid(ell,np.array([0.,b]),t,targets))-1 for t in (.9-1e-8,.9+1e-8)]
truegrid=grid(ell,np.array([0.,dtrue]),.9,targets)
assert counts==[2,4] and len(truegrid)-1==3
assert .9*math.exp(4*eta)<1
OUT['D_jump_counterexample']={
    'n':n,'p':2,'B':1,'blocks':[[0],[1]],'V':[[0],[0,1]],'eps':eps,
    'G':G.tolist(),'z':z.tolist(),'Y':Y,'x1':x1,'x2':x2,
    'zGinvz':float(z@np.linalg.solve(G,z)),'d_sigma_gap':b,'d_true_gap':dtrue,
    'targets':targets,'eta_D':eta,'threshold_upper':.9*math.exp(4*eta),
    'left_right_counts':counts,'perturbed_count':3,'perturbed_grid':truegrid,
    'point':'One-sided baseline counts 2 and 4 do not exclude the intermediate count 3.'}

# Independent method-partition check on all three revised finite exhibits.
part=[]
for p,g,r,n,eps in [(16,4,.5,64,1e-4),(8,2,.6,40,1e-5),(60,5,.5,100,0.)]:
    Sig=np.zeros((p,p)) if eps==0 else np.full((p,p),eps)
    groups=[list(range(i,i+g)) for i in range(0,p,g)]
    for C in groups:Sig[np.ix_(C,C)]=r
    np.fill_diagonal(Sig,1.)
    if p==60:
        Sig[0,5]=Sig[5,0]=Sig[10,15]=Sig[15,10]=.2
    K,B=bc.method_sizes(n,p);blocks=bc.coded_partition((n-1)*Sig,B)
    assert blocks==groups
    part.append(dict(n=n,p=p,g=g,B=B,K=K,groups_equal_blocks=True,eps=eps,
                     min_eigenvalue=float(np.linalg.eigvalsh(Sig).min())))
OUT['revised_partitions']=part

# A's fixed-eps multiplicative o_P(1) lower bound misses second-order terms.
# p=2 => the only nonzero d_X is the truth pair; all singleton d_X vanish.
eps=.1;theta=np.array([.8,.6]);Sig=np.array([[1.,eps],[eps,1.]])
v=1+theta@Sig@theta;c=Sig@theta/math.sqrt(v)
xbar=float(c@c);r2=float(theta@Sig@theta/v)
actual=abs(.5*math.log((1-xbar)/(1-r2)))
pred=eps*abs(c[0]*c[1])/(1-xbar)
assert actual<pred
OUT['A_Nd_fixed_eps_counterexample']={
    'eps':eps,'theta':theta.tolist(),'sigma2':1.,'population_c':c.tolist(),
    'xbar_limit':xbar,'actual_sup_dX_over_n_limit':actual,
    'claimed_lower_bound_over_n_limit':pred,'ratio_limit':actual/pred,
    'point':'Ratio stays below 1; a multiplicative 1+o_P(1) needs eps->0 and a signal/noise margin.'}

# D's claimed fixed-R2 consequence osc d >= const*n*eps misses cancellation.
eps=.1;t=math.sqrt(2*eps/((1+eps)*(1-eps)**2))
theta=np.array([t,t]);Sig=np.array([[1.,eps],[eps,1.]])
v=1+theta@Sig@theta;c=Sig@theta/math.sqrt(v)
r2=theta@Sig@theta/v;x=float(c[0]**2)
limit=.5*(2*math.log1p(-x)-math.log1p(-r2))
assert abs(limit)<1e-14
rows=[]
for n in (1000,10000,100000):
    G=(n-1)*Sig;Y=n-1;z=(n-1)*c
    dpair=bf(G,z,Y,n,[0,1])-bf(G,z,Y,n,[0])-bf(G,z,Y,n,[1])
    rows.append(dict(n=n,d_pair=dpair,osc_over_n_eps=abs(dpair)/(n*eps)))
OUT['D_NEC_fixed_R2_counterexample']={
    'eps':eps,'theta':theta.tolist(),'sigma2':1.,'R2':r2,
    'd_pair_over_n_limit':limit,'deterministic_LLNs':rows,
    'Gaussian_argument':'z/(n-1)->c; Y=n-1 after standardisation. Therefore osc(d)/n->0 in probability. There are only four models.'}

# B's NEC gives a relative noise rate without a beta-min premise.
weak=[]
for n in (10000,1000000):
    eps=.01;Sig=np.array([[1.,eps],[eps,1.]]);vals=[]
    for seed in range(10):
        G,z,Y,_=bc.exact_gram_suff(Sig,np.array([1/n,1/n]),n,1.,np.random.default_rng(seed))
        GD=np.diag(np.diag(G));dt=bf(G,z,Y,n,[0,1])-bf(GD,z,Y,n,[0,1])
        vals.append(abs(dt)/(n*eps*(1/n)**2))
    weak.append(dict(n=n,median_actual_over_claimed=float(np.median(vals))))
OUT['B_NEC_weak_signal_counterexample']={
    'theta_n':'(1/n,1/n)','eps':.01,'SE_min':.99,'rows':weak,
    'point':'Noise gain is O_P(eps), not eps/n. Neither two nonzero truths nor SE supplies beta-min.'}

# Actual 2x2 ridge identity in D's route uses e_H=(1-1/n^2)*eps.
n=40;eps=.1;G=(n-1)*np.array([[1.,eps],[eps,1.]]);z=np.array([10.,8.])
H=(n+1)*G+np.eye(2);HD=np.diag(np.diag(H))
exact=n*z@(np.linalg.solve(H,z)-np.linalg.solve(HD,z))
claimed=((z@z)*eps**2-2*eps*z[0]*z[1])/(n*(1-eps**2))
eH=(1-1/n**2)*eps
correct=((z@z)*eH**2-2*eH*z[0]*z[1])/(n*(1-eH**2))
assert abs(exact-correct)<1e-12 and abs(exact-claimed)>1e-6
OUT['D_ridge_formula']={'exact':exact,'claimed':claimed,'corrected':correct,'eH':eH}

# D T6 promotes a first-order expansion to an unconditional order equivalence.
# Choose opposite-sign truths for which full/BO gains agree to leading order.
eps=.1;rat=(-1+math.sqrt(1-eps**2))/eps
theta=np.array([.8,.8*rat]);Sig=np.array([[1.,eps],[eps,1.]])
v=1+theta@Sig@theta;c=Sig@theta/math.sqrt(v)
r2=theta@Sig@theta/v;xb=c@c
dxlimit=.5*math.log((1-xb)/(1-r2))
assert abs(dxlimit)<1e-14 and np.prod(theta)!=0
OUT['D_T6_dX_cancellation']={'eps':eps,'theta':theta.tolist(),
    'dX_over_n_limit':dxlimit,'claimed_order_over_n':eps*abs(float(np.prod(theta))),
    'point':'Gaussian LLN gives d_X/n->0 despite a positive claimed n-scale.'}

# D's local-V rescaling is not a global [0,1] h for N1.
G=39*np.array([[1.,1e-4],[1e-4,1.]]);Y=39.;z=np.array([15.,12.]);n=40
models,d,lbf=bc.d_table(G,z,Y,n,[[0],[1]],2)
mask=np.array([S in [(),(0,)] for S in models])
OUT['D_V_envelope_counterexample']={'V':[[],[0]],'d_on_V':d[mask].tolist(),
                                   'd_on_Omega':d.tolist(),
                                   'point':'osc_V=0 but osc_Omega>0. V is not a global envelope.'}
assert np.ptp(d[mask])==0 and np.ptp(d)>0

# A's additional shrinking-cross-correlation exhibit keeps fixed signals.
growth=[]
for n in (64,256,1024,4096):
    p=16;Sig=np.full((p,p),1/n**2)
    for i in range(0,p,4):Sig[i:i+4,i:i+4]=.5
    np.fill_diagonal(Sig,1.);beta=np.zeros(p);beta[0]=.8;beta[8]=.6
    v=1+beta@Sig@beta;G=(n-1)*Sig;z=(n-1)*(Sig@beta)/math.sqrt(v);Y=n-1
    # Population LLN sufficient statistics; truth pair alone lower-bounds osc d.
    ds=bf(G,z,Y,n,[0,8])-bf(G,z,Y,n,[0])-bf(G,z,Y,n,[8])
    growth.append(dict(n=n,eps=1/n**2,d_truth=ds,d_truth_over_n=ds/n))
OUT['A_fixed_signal_growth_exhibit']=growth

# The constant-discrepancy uniform-grid formula needs max(1, ceil(...)).
_,zero_d,_=bc.d_table(7*np.eye(2),np.zeros(2),7.,8,[[0],[1]],2)
assert np.max(np.abs(zero_d))<1e-12
assert grid(np.zeros(4),np.zeros(4))==[0.,1.]
OUT['A_zero_range_grid']={'n':8,'p':2,'G':(7*np.eye(2)).tolist(),'z':[0.,0.],
                         'd':[0.,0.,0.,0.],'claimed_stage_count':0,'necessary_stage_count':1}

# New comparison: retain common pilot targets, which A/D's quoted scripts omit.
stagecases=applicable=violations=0; eta_rows=[]
for eps in (1e-5,1e-4,1e-3,.01):
    Sig=np.full((8,8),eps)
    blocks=[[0,1],[2,3],[4,5],[6,7]]
    for C in blocks:Sig[np.ix_(C,C)]=.6
    np.fill_diagonal(Sig,1.)
    for seed in range(10):
        beta=np.zeros(8);beta[0]=.25;beta[4]=.2
        G,z,Y,n=bc.exact_gram_suff(Sig,beta,40,1.,np.random.default_rng(seed))
        assert bc.coded_partition(G,2)==blocks
        models,d,lbf=bc.d_table(G,z,Y,n,blocks,8)
        GD=np.zeros_like(G)
        for C in blocks:GD[np.ix_(C,C)]=G[np.ix_(C,C)]
        _,ds,_=bc.d_table(GD,z,Y,n,blocks,8)
        ell=np.array([bc.log_prior_w(8,len(S))+lbf[i]-d[i] for i,S in enumerate(models)])
        ub=40*z@np.linalg.solve(41*GD+np.eye(8),z)/(Y+.02)
        delta=7*eps/.4
        eta=8*-math.log1p(-delta)-20.01*math.log1p(-delta*ub/((1-delta)*(1-ub)))
        stagecases+=1
        if .9*math.exp(4*eta)<1:
            target=(.15,.3,.55,.8,1.)
            lo=len(grid(ell,ds,.9*math.exp(-4*eta),target))-1
            tr=len(grid(ell,d,.9,target))-1
            hi=len(grid(ell,ds,.9*math.exp(4*eta),target))-1
            applicable+=1
            violations+=int(not lo<=tr<=hi)
        eta_rows.append((eps,eta))
OUT['common_pilot_sandwich_search']={'cases':stagecases,'applicable':applicable,
    'violations':violations,'targets':[.15,.3,.55,.8,1.],
    'eta_ranges':{str(e):[min(v for ee,v in eta_rows if ee==e),max(v for ee,v in eta_rows if ee==e)] for e in (1e-5,1e-4,1e-3,.01)}}

# A/B's new unqualified 2/3 duplicate limit only describes the W1 p=2 example.
# With p fixed and a third orthogonal null, prior odds for pair/single change.
dup=[]
for n in (400,4000,40000):
    p=3;G=(n-1)*np.array([[1.,1.,0.],[1.,1.,0.],[0.,0.,1.]])
    z=(n-1)*np.array([math.sqrt(.5),math.sqrt(.5),0.]);Y=n-1
    models=bc.all_models(p,3)
    lp=np.array([bc.log_prior_w(p,len(S))+bf(G,z,Y,n,S) for S in models])
    prob=np.exp(lp-logsumexp(lp))
    pip=sum(prob[i] for i,S in enumerate(models) if 0 in S)
    dup.append({'n':n,'p':p,'PIP_duplicate':float(pip)})
OUT['AB_duplicate_limit_scope']={'rows':dup,'limit':3/5,
    'general_fixed_p_limit':'p/(2p-1) for two duplicate true columns and otherwise orthogonal nulls',
    'point':'2/3 needs the p=2 example or explicit prior-odds qualifications.'}

# SL's explicit lambda_s=|s|^-gamma is not uniformly a bounded prior odds.
# At singleton subsets the literal rate gives lambda_1=1; shrinking BF alone
# cannot imply exclusion, although lambda_1/sqrt(n)->0.
sl=[]
for n in (1000,10000):
    V=(n-1+.01)/n;G=n-1;z=math.sqrt(n);Y=n-1
    gain=V*z*z/(1+G*V)
    logBF=-.5*math.log1p(G*V)-(1+n/2)*math.log1p(-gain/(2+Y))
    sl.append({'n':n,'null_BF':math.exp(logBF),'lambda_s':1.,'PIP':1.})
OUT['SL_singleton_prior_boundary']={'rows':sl,
    'point':'Exclude singleton prior degeneracy or specify prior odds/retained initial subset rate, not just lambda_s/sqrt(n)->0.'}

HERE.joinpath('new_checks.json').write_text(json.dumps(OUT,indent=2)+'\n')
print(json.dumps(OUT,indent=2))

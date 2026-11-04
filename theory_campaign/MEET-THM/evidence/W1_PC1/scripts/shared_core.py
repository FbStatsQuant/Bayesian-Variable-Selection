"""Exact finite Feynman--Kac recursion, terminal-prefix records, moments and finite order facts."""
import itertools,json,math
import numpy as np
from scipy.special import logsumexp
from pathlib import Path
out={}
# Two particles, two states, two resample--move stages; enumerate every offspring/mutation outcome.
p0=np.array([.8,.2]);d=np.array([-1.,2.]);N=2;ss=list(itertools.product(range(2),repeat=N))
# maintain probability and probability*W; kernels are random mixtures of identity and refresh (invariant).
prob={s:float(np.prod(p0[list(s)])) for s in ss};weighted=prob.copy();Zprev=1.
for phi,prev in ((.4,0.),(1.,.4)):
    Z=float(p0@np.exp(phi*d));pi=p0*np.exp(phi*d)/Z
    K=.3*np.eye(2)+.7*np.tile(pi,(2,1))
    npb={s:0. for s in ss};nwt=npb.copy()
    for s in ss:
        g=np.exp((phi-prev)*d[list(s)]);inc=float(g.mean());parent=g/g.sum()
        marginal=sum(parent[i]*K[s[i]] for i in range(N))
        for t in ss:
            transition=float(np.prod(marginal[list(t)]));npb[t]+=prob[s]*transition;nwt[t]+=weighted[s]*inc*transition
    prob,weighted=npb,nwt;Zprev=Z
pi=p0*np.exp(d)/Zprev
assert abs(sum(weighted.values())-Zprev)<1e-12
h=np.array([.2,.8]);I=np.eye(2);refresh=np.tile(pi,(2,1));P=.5*I+.5*refresh
# Average records at all possible prefixes: composition preserves pi; use unnormalised weighted marginal.
marg=np.array([sum(v*np.mean(np.array(s)==j) for s,v in weighted.items()) for j in range(2)])
assert max(abs(marg-Zprev*pi))<1e-12
for pref in (I,P,refresh,P@refresh,refresh@P):assert abs(marg@pref@h-Zprev*(pi@h))<1e-12
out['N1']=dict(N=N,stages=[.4,1.],E_Z=sum(weighted.values()),Z=Zprev,E_ZH=float(marg@h),Z_pi_h=float(Zprev*(pi@h)),weighted_abs_error=float((marg/Zprev)@abs(h-h[0])),bound_2delta=float(2*pi[1]))
# N200 all orders, all nonempty scored sets, all truth states for 4 states.
cases=0
for ordering in itertools.permutations(range(4)):
    rank={x:i for i,x in enumerate(ordering)};mode=ordering[-1]
    for bits in itertools.product((False,True),repeat=4):
        T=[i for i in range(4) if bits[i]]
        if not T:continue
        reported=max(T,key=rank.get)
        for truth in range(4):
            wrong=reported!=truth;posterior=rank[reported]>rank[truth];miss=rank[reported]<rank[truth]
            assert wrong==posterior+miss
            assert not posterior or mode!=truth
            assert not miss or truth not in T
            assert not(mode!=truth and mode in T) or wrong
            cases+=1
out['N200_order_enumeration']=dict(cases=cases,result='PASS')
# Coverage selection: fixed pointwise bound cannot be substituted at final-run selected endpoints.
# Uniform[0,1] exact law; two equiprobable estimates distort opposite halves by +/-a.
# Each fixed interval can have cancellation, selected interval targets the positive distortion: needs uniform event.
out['coverage_scope']='Fixed predeclared h is covered. Data/final-run selected I needs uniform TV/CDF control; endpoint quantiles also need margins/density.'
# CEX off-terminal W: identity moves N=1, pi0=(.99,.005,.005), pi=(.9,.09,.01).
p0=np.array([.99,.005,.005]);pi=np.array([.9,.09,.01]);W=pi/p0
out['off_truth_pointwise_cex']=dict(pi0=p0.tolist(),pi=pi.tolist(),W=W.tolist(),delta=.1,off_state=1,off_event_probability=.005,W_off=18.,sqrt_delta=math.sqrt(.1),setting='N=1,T=1,identity invariant mutation')
# Need actual BVS off-event? Full-support actual N9 moves give positive probability all start S0, then move off after weighting.
# Therefore W=pi(S0)/pi0(S0)>1 with off-terminal population still possible, however small probability.
out['actual_kernel_off_event']='Choose masked pi0(S0)<pi(S0), pi(S0)>.5. All N initial particles S0; T=1 W=pi(S0)/pi0(S0)>1; resample S0, then all Gibbs draws delete a truth with positive probability. Terminal all off yet W>sqrt(delta).'
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

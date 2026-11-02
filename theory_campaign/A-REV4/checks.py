import math,json,itertools,platform,datetime,sys,random
random.seed(20261102)
out={'seed':20261102,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'host':platform.node(),'python':sys.version,'checks':{}}
# W2: realizable centered orthogonal n=20,p=4, blocks {0,2},{1,3}; z squares 100,30,0,0, residual positive.
n=20; nu=.01+n/2; c=.02+n-1; a=100/n; b=30/n
actual=nu*(math.log1p(-b/c)-math.log1p(-b/(c-a)))
rssT=n-1; rssS=n-1-100/(n-1)
rhs=nu*(math.log1p(-(30/(n-1))/rssT)-math.log1p(-(30/(n-1))/rssS))
out['checks']['W2']={'exact_LR':actual,'claimed_RSS_RHS':rhs,'difference':actual-rhs,'feasible':100/19+30/19<19}
# W1/Delta exact enumeration, any singleton/two-member partition, fixed orthogonal realizable sufficient statistics.
p=4; blocks=[{0,2},{1,3}]; zs=[100,30,0,0]
subs=[set(j for j in range(p) if mask>>j&1) for mask in range(2**p)]
def bf(S):return -.5*len(S)*math.log(n)-nu*math.log1p(-sum(zs[j]/n for j in S)/c)
def prior(S):return -math.log(2)-math.log(math.comb(2*p-1,len(S)))
d=[bf(S)-sum(bf(S&B) for B in blocks) for S in subs]
g0=[prior(S)+sum(bf(S&B) for B in blocks) for S in subs]
def norm(logs):
 m=max(logs); z=sum(math.exp(v-m) for v in logs);return [math.exp(v-m)/z for v in logs]
q0=norm(g0); q1=norm([v+w for v,w in zip(g0,d)])
ref=3; masses=[norm([v+t/100*w for v,w in zip(g0,d)])[ref] for t in range(101)]
out['checks']['W1_Delta']={'min_d':min(d),'max_d':max(d),'interior_deficit':1-min(masses),'endpoint_deficit':max(1-q0[ref],1-q1[ref])}
# abstract four-island bookkeeping law E Z=1 E ZP=.25; P=1 on low Z.
states=[(.5,1.),(1.5,0.)]; ezp=ez=ep=pool=0
for xs in itertools.product(states,repeat=4):
 w=1/16; z=sum(x[0] for x in xs)/4; f=sum(x[1] for x in xs)/4; pool+=w*z*f
cov=.25-1*.5
out['checks']['BOOK']={'E_Z':1,'E_ZP':.25,'E_P':.5,'pooled_product':pool,'bias':pool-.25,'minus_three_quarters_cov':-.75*cov,'E_Z_given_all_high':1.5,'output_probability':1/16}
# generic KL/TV vs chi2 contrast (not proof of BVS W4).
out['checks']['generic_divergence']=[]
for k in [10,100,1000]:
 a=1/k;b=1/k**3
 kl=a*math.log(a/b)+(1-a)*math.log((1-a)/(1-b));chi=a*a/b+(1-a)**2/(1-b)-1
 out['checks']['generic_divergence'].append({'k':k,'KL':kl,'TV':a-b,'chi2':chi})
assert abs(actual-rhs)>1e-3
assert abs(pool-.25+.75*cov)<1e-12
assert abs(1-min(masses)-max(1-q0[ref],1-q1[ref]))<1e-12
print(json.dumps(out,indent=2))

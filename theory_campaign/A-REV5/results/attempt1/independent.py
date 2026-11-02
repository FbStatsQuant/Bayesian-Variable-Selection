import json,math,datetime,platform,os
from pathlib import Path
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'host':platform.node(),'python':platform.python_version(),'pid':os.getpid(),'seed':None,'kind':'deterministic scalar sufficient statistics; independent formulas'}
f,e=.05,.9
r['ESS']={'unclipped':f-math.sqrt(f*(1-f)*(1/e-1)),'low_weight':1-math.sqrt((1/e-1)*(1-f)/f),'r_star':(11+2*math.sqrt(10))/9}
n=1000000; nu=n/2+.01; c=1/24; z2=65; L=5
kappa=1/(n-1)+nu*(1.02+1/n)/(c*n); theta=n**(-1/3)+L*math.log(n)/(n-1); theta2=L*math.log(n)*(theta+3/n)/(1-theta)
g=n-1; H=(n+1)*g+1; D=H/(g+1); Q0=n-1; inc=n*g*z2/(2*H)
stat=-.5*math.log(D)+nu*(-math.log1p(-inc/(.02+Q0)))+.5*math.log(n+1)
r['C3']={'actual':stat,'old_lower':z2/2-kappa-theta2,'repaired_weak_lower':-kappa+z2/12,'kappa':kappa,'theta_prime':theta2,'limit':.51/c}
n=20; g=19; H=21*g+1; D=H/20; nu=10.01
r1=math.exp(-.5*math.log(D)); r2=math.exp(-.5*math.log(D)-nu*math.log((.02+g-20*g*g/H)/(.02+g)))
r['E3']={'q':r2,'old_bound':(1-r2)**2/(1+4/r1),'actual_reference_mass':r1/(6+r1+r2)}
r['PXN']={'minimum_limit':.51*16,'unit_M_sigma_phi_limit':.51*24}
n=262144;p=18; N=max(2500,n,p); H0=math.ceil(512*N/2500)
r['T26']={'n':n,'p':p,'feasible_models':2**18,'exact_threshold':(5*H0+4*N)*p,'exact':2**18<=(5*H0+4*N)*p}
assert r['C3']['actual']<r['C3']['old_lower']
assert r['E3']['q']>1 and r['E3']['old_bound']>1 and r['E3']['actual_reference_mass']<.5
Path('independent.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

"""Independent reconstruction of described computations; A/D did not include executable script text.
Not a reproduction of their unprovided response/noise generation or hidden scripts.
"""
import contextlib,io,itertools,json
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
    import exact_checks as e
import numpy as np
from scipy.special import logsumexp
rows=[]
for eps in (0.,.002,.01):
    for seed in range(1,6):
        b=np.zeros(8);b[0]=.5;b[4]=.4
        a=e.setup(40,8,[list(range(4)),list(range(4,8))],.5,eps,seed=seed,beta=b)
        keep=np.array([len(s)<=4 for s in a['ss']]);l0=a['l0'][keep];d=a['d'][keep];ds=a['ds'][keep];eta=a['eta']
        # eta over full space is conservative for the described K=4 reconstruction.
        ratios=[float(np.exp(e.lc(l0,d,0,v)-e.lc(l0,ds,0,v))) for v in (.25,.5,1.)]
        assert max(abs(d-ds))<=eta+1e-10
        assert all(abs(np.log(r))<=4*v*eta+1e-10 for r,v in zip(ratios,(.25,.5,1.)))
        rows.append(dict(eps=eps,seed=seed,states=len(d),max_error=float(max(abs(d-ds))),eta=eta,ratios=ratios))
drows=[]
for eps in (.02,.05,.1,.2):
    for seed in (1,2,3):
        b=np.zeros(8);b[0]=.5
        a=e.setup(40,8,[list(range(4)),list(range(4,8))],.6,eps,seed=seed,beta=b)
        # Seat's K=4: choose only those states for comparison, and delta based on K=4.
        keep=np.array([len(s)<=4 for s in a['ss']]);l0=a['l0'][keep];d=a['d'][keep];ds=a['ds'][keep]
        # ubar computed exactly on kept subset.
        Gbd=a['G'].copy();Gbd[:4,4:]=0;Gbd[4:,:4]=0
        ub=max(e.score(Gbd,a['z'],a['Y'],40,s)[1] for s in a['ss'] if len(s)<=4)
        delta=3*eps/.4;r=delta*ub/((1-delta)*(1-ub)) if delta<1 else np.inf
        eta=4*np.log(1/(1-delta))+20.01*np.log(1/(1-r)) if delta<1 and r<1 else np.inf
        err=float(max(abs(d-ds)))
        if np.isfinite(eta):assert err<=eta+1e-10
        margin=max(abs(e.lc(l0,d,u,v)-e.lc(l0,ds,u,v))-4*v*err for u in np.linspace(0,.95,10) for v in np.linspace(u+.001,1,24))
        assert margin<=1e-9
        drows.append(dict(eps=eps,seed=seed,states=len(d),max_error=err,eta=float(eta),continuity_margin=float(margin)))
out=dict(note=__doc__,seat_a_15=rows,seat_d_12=drows)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print('A described-setting reconstruction:',len(rows),'cases PASS; ratios range',min(min(x['ratios']) for x in rows),max(max(x['ratios']) for x in rows))
print('D described-setting reconstruction:',len(drows),'cases PASS; finite eta',sum(np.isfinite(x['eta']) for x in drows))

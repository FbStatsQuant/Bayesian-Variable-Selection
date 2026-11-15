import time
from reps import *
for spec in [dict(eid=1,name="N1",kind="ar",n=800,p=12,beta="sparse",rep=0,family="exact",ndraw=4000,mfresh=20000),
             dict(eid=2,name="N2c",kind="spike",n=800,p=12,beta="sparse",rep=0,family="exact",ndraw=4000,mfresh=20000),
             dict(eid=7,name="N7",kind="ar",n=200,p=600,beta="sparse",rep=0,family="restricted",ndraw=4000,mfresh=20000),
             dict(eid=7,name="N7",kind="ar",n=200,p=800,beta="sparse",rep=0,family="restricted",ndraw=4000,mfresh=20000)]:
    t=time.time(); o,_,_=run_rep(spec); print(spec["name"],spec["n"],spec["p"],round(time.time()-t,2),"q",o["q"],"d2 q50/q99",o["d2_q50"]*spec["n"],o["d2_q99"]*spec["n"],"esize",o["esize"],"rho max",o["rho_max"],"nmod",o["nmodels"])

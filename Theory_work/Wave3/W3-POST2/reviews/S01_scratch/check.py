import importlib.util
import pathlib
import math
import numpy as np
import sys
sys.dont_write_bytecode = True

path = pathlib.Path(__file__).resolve().parents[2] / 'numerics/post2_checks.py'
spec = importlib.util.spec_from_file_location('post2', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for j,d in [(1,0),(2,1),(3,1),(3,2)]:
    old = 1 if d == 0 else (2*math.e*11*j*math.log(100)/d)**(d/2)
    new = 2**(j/2)*(math.e*11*j*math.log(100)/max(d,1))**(d/2)
    print('weight',j,d,'implemented',old,'specified',new,'ratio',new/old)
for n in [100,400,1600]:
    N=n-1
    # True columns have correlation 1 - n^-2; x3 is their normalized difference.
    g=np.array([[N,N*(1-n**-2)],[N*(1-n**-2),N]])
    a=np.array([1.,-1.])/math.sqrt(2*n**-2)
    gg=np.block([[g,(g@a)[:,None]],[(a@g)[None,:],np.array([[N]])]])
    def logD(x):
        return np.linalg.slogdet((n+1)*x+np.eye(len(x)))[1]-np.linalg.slogdet(x+np.eye(len(x)))[1]
    print('dependent addition',n,'D ratio',math.exp(logD(gg)-logD(g)))
def des(n,rng):
    z=rng.standard_normal((n,10)); z[:,2]=z[:,0]+z[:,1]; return z
slacks=[]
for n in [100,400]:
    for sd in range(4):
        X,y,sy,mu=m.gen(des,np.array([1.,-1.]),[0,1],n,sd)
        P=m.Post(X,y)
        slacks.append(m.basic(P,[0,1])['A2slack'])
print('minimum A2 slack in independent 8-case check',min(slacks))

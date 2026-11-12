import sys, pathlib, math
sys.dont_write_bytecode = True
base = pathlib.Path(__file__).resolve().parents[2] / 'numerics'
sys.path.insert(0, str(base))
import numpy as np
import mpmath as mp
import a_orth, a_sph, b_check, c_counter
rng = np.random.default_rng(6101)
a_orth.V1(rng)
a_sph.V1(rng)
b_check.F1(rng)
c_counter.V1(rng)
mp.mp.dps = 70
print('Independent reference-cost minimization, b=1: min B_T / (n-1)')
for n in (200, 1000, 1000000):
    k = math.ceil(12*math.log(n))
    eta = mp.mpf(n)**-2
    c = 1/mp.sqrt(1+eta**2*k)
    # Coordinates along x1/sqrt(n-1) and u/sqrt(k(n-1)).
    X = mp.sqrt(n-1)*mp.matrix([[1,c],[0,-c*eta*mp.sqrt(k)]])
    mu = mp.matrix([0,mp.sqrt(n-1)])
    G = X.T*X
    H = (n+1)*G+mp.eye(2)
    cost = (mu.T*mu)[0]-n*(mu.T*X*mp.lu_solve(H,X.T*mu))[0]
    print(n,k,mp.nstr(cost/(n-1),18))
worst = (0,0)
for n in range(200,20001):
    k=math.ceil(12*math.log(n)); p=k+2; m=k//2
    # R=choose(2p-1,2)*sum_{j>m} choose(p,j)/choose(2p-1,j).
    term=1.0; total=0.0
    for j in range(1,p+1):
        term *= (p-j+1)/(2*p-j)
        if j>m: total+=term
    val=math.comb(2*p-1,2)*total*n*n
    if val>worst[0]: worst=(val,n)
print('Independent cutoff scan max n^2 R, n:',worst)
for n in (400,1600,6400):
    s=round(n**.3)
    print('E2 energy/n:',n,s,(n-1)*s/n,'; repaired theta=1/sqrt(s):',(n-1)/n)

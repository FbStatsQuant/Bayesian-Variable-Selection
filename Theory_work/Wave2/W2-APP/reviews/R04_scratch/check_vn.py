"""Independent numerical checks for R04. Not evidence for asymptotic claims."""
import json
import math
from pathlib import Path
import numpy as np

rng = np.random.default_rng(20261109)
errors = {name: 0.0 for name in ('STAR', 'blocks', 'equicorrelation', 'factor')}
floor_ratios = {name: float('inf') for name in errors}
counts = {name: 0 for name in errors}

def cond(S, a, b, U):
    if not U:
        return S[a, b]
    return S[a, b] - S[a, U] @ np.linalg.solve(S[np.ix_(U, U)], S[U, b])

def check(name, S, truth, theta, l, U, cov_formula, var_formula, response_var_formula, kappa, sigma=0.8):
    coeff = np.zeros(len(S))
    coeff[truth] = theta
    # Append the population response and use a direct Schur complement.
    T = np.zeros((len(S)+1, len(S)+1))
    T[:-1, :-1] = S
    T[:-1, -1] = T[-1, :-1] = S @ coeff
    T[-1, -1] = coeff @ S @ coeff + sigma**2
    cv = cond(T, l, len(S), U)
    vl = cond(T, l, l, U)
    vy = cond(T, len(S), len(S), U)
    err = max(abs(cv-cov_formula), abs(vl-var_formula), abs(vy-response_var_formula))
    errors[name] = max(errors[name], float(err))
    floor_ratios[name] = min(floor_ratios[name], float(cv**2/(vl*vy)/kappa))
    counts[name] += 1
    assert err < 1e-11
    assert cv**2/(vl*vy) >= kappa*(1-1e-11)

p = 43
for rep in range(1200):
    size = rep % 16  # explicitly includes U empty and size 15
    # V1: 31 leaves, 11 additional independent variables.
    m = 31
    r = 1/(2*np.sqrt(m))
    S = np.eye(p)
    S[0, 1:m+1] = S[1:m+1, 0] = r
    l = int(rng.integers(1, m+1))
    U = rng.choice([j for j in range(p) if j not in (0,l)], size=size, replace=False).tolist()
    theta = np.array([1.3])
    kap = theta[0]**2/(4*m*(theta[0]**2+0.8**2))
    vy = theta[0]**2*(1-sum(1 <= j <= m for j in U)*r*r)+.8**2
    check('STAR', S, [0], theta, l, U, theta[0]*r, 1., vy, kap)
    # V2: independent blocks; condition also on nulls in other truth blocks.
    rho = float(rng.uniform(.05, .93))
    S = np.eye(48)
    for start in (0, 16, 32):
        S[start:start+16, start:start+16] = (1-rho)*np.eye(16)+rho*np.ones((16,16))
    truth = [0,16,32]
    theta = np.array([1.2,-.9,.7])
    l = int(rng.integers(1,16))
    U = rng.choice([j for j in range(48) if j not in truth+[l]], size=size, replace=False).tolist()
    u = sum(j<16 for j in U)
    d = 1+(u-1)*rho
    q = rho*(1-rho)/d
    kap = min(abs(theta))**2*rho**2*(1-rho)**2/((1+14*rho)**2*(3*max(abs(theta))**2+.8**2))
    vy = .8**2
    for j, th in zip(truth, theta):
        uj = sum(j <= k < j+16 for k in U)
        vy += th**2*(1-rho*rho*uj/(1+(uj-1)*rho))
    check('blocks', S, truth, theta, l, U, theta[0]*q, 1-rho**2*u/d, vy, kap)
    # V3: positive and negative coefficients, nonzero common signal.
    S = (1-rho)*np.eye(p)+rho*np.ones((p,p))
    truth = [0,1,2]
    theta = np.array([1.2,-.9,.7])
    l = 3
    U = rng.choice(list(range(4,p)), size=size, replace=False).tolist()
    d = 1+(size-1)*rho
    kap = sum(theta)**2*rho**2*(1-rho)**2/((1+14*rho)**2*(theta@S[np.ix_(truth,truth)]@theta+.8**2))
    vy = (1-rho)*sum(theta**2)+rho*(1-rho)/d*sum(theta)**2+.8**2
    check('equicorrelation', S, truth, theta, l, U, sum(theta)*rho*(1-rho)/d, 1-rho**2*size/d, vy, kap)
    # V4: heterogeneous loadings of either sign, and cancellation away from zero.
    b = rng.uniform(-.9,.9,p)
    b[3] = .75
    psi = 1-b*b
    S = np.outer(b,b)+np.diag(psi)
    beta = b[truth]@theta
    if abs(beta) < .02:
        continue
    v = 1/(1+sum(b[U]**2/psi[U]))
    kap = b[l]**2*beta**2/(1+15/min(psi))**2/(theta@S[np.ix_(truth,truth)]@theta+.8**2)
    vy = sum(psi[truth]*theta**2)+beta**2*v+.8**2
    check('factor', S, truth, theta, l, U, b[l]*beta*v, psi[l]+b[l]**2*v, vy, kap)

# Check actual shipped m(A), RSS expansion and additive prior inequality.
n, p = 2400, 24
W = rng.normal(size=(n,1))*np.sqrt(.5)+rng.normal(size=(n,p))*np.sqrt(.5)
W -= W.mean(axis=0)
X = W / np.sqrt(np.sum(W*W,axis=0)/(n-1))
Y = 1.4*X[:,0]+rng.normal(size=n)
Y -= Y.mean()
y = Y/np.sqrt(Y@Y/(n-1))
nu = n/2+.01
def score(A):
    if not A:
        return -nu*np.log(.02+y@y), float(Y@Y)
    Z = X[:, A]
    G = Z.T@Z
    z = Z.T@y
    H = (n+1)*G+np.eye(len(A))
    logdet = np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(A)))[1]
    Q = y@y-n*z@np.linalg.solve(H,z)
    rss = Y@Y-(Z.T@Y)@np.linalg.solve(G,Z.T@Y)
    return -.5*logdet-nu*np.log(.02+Q), float(rss)
min_margin = float('inf')
max_remainder_diff = 0.
for rep in range(600):
    U = rng.choice(list(range(1,p)),size=rep%16,replace=False).tolist()
    l = int(rng.choice([j for j in range(p) if j not in U]))
    a, rss = score(U)
    aa, rssa = score(U+[l])
    h = n*(1-rssa/rss)
    remainder = aa-a+.5*np.log(n+1)+nu*np.log(rssa/rss)
    max_remainder_diff = max(max_remainder_diff,abs(float(remainder)))
    min_margin = min(min_margin,float(aa-a+.5*np.log(n+1)-h/2-remainder))
assert min_margin > -1e-8
for pp in range(1,100):
    for k in range(pp):
        prior = math.comb(2*pp-1,k)/math.comb(2*pp-1,k+1)
        assert abs(prior-(k+1)/(2*pp-1-k)) < 1e-12
        assert prior >= 1/(2*pp)
result = dict(counts=counts, max_covariance_variance_error=errors,
              min_exact_corr_squared_over_floor=floor_ratios,
              shipped_score_checks=600, max_abs_remainder_difference=max_remainder_diff,
              min_likelihood_lower_bound_margin=min_margin,
              seed=20261109)
print(json.dumps(result,indent=2))
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')

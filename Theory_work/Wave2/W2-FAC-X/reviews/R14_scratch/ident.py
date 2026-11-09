import sympy as sp
k,kap,tl,tj=sp.symbols('k kappa tau_l tau_j',positive=True)
g=lambda m:1/(m+kap)
lhs=(1+g(k-1))*((1-g(k))**2*(tl+g(k-1)*tj)**2-tj**2); rhs=tl**2-tj**2-g(k)*(tl-tj)**2
print("swap",sp.simplify(lhs-rhs))
print("add",sp.simplify((1+g(k))*(1-g(k+1))**2-(1-g(k+1))))
print("inv",sp.simplify(1/(1-g(k))-(1+g(k-1))))
# drift identity
s,xj,rho_=sp.symbols('s xi_j varrho')
xT=(s-rho_)/(k+kap); xTm=(s-xj-rho_)/(k-1+kap)
print("drift",sp.simplify(xTm-(xT-(xj-xT)/(k-1+kap))))
# envelope |x_T|<=1.5 Hbar : k l^2 - 2 d l + 3 d >=0 for d in (0,2], k>=1
import numpy as np
mn=min(kk*l*l-2*d*l+3*d for kk in (1,2) for l in np.linspace(0,50,5001) for d in np.linspace(0.01,2,200)); print("env min",mn)

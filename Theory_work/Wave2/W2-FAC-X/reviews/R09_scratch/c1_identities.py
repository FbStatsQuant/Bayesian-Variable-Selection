# R09 council (Opus): independent checks of X1 algebra
import sympy as sp
tl,tj,k,kap,ell,phi,N=sp.symbols('tau_l tau_j k kappa ell phi N',positive=True)
g=lambda m: 1/(m+kap)
lhs=(1+g(k-1))*((1-g(k))**2*(tl+g(k-1)*tj)**2-tj**2)
rhs=tl**2-tj**2-g(k)*(tl-tj)**2
print("swap identity:",sp.simplify(lhs-rhs))
# addition factor (1+g_k)(1-g_{k+1})^2 = 1-g_{k+1}
print("add factor:",sp.simplify((1+g(k))*(1-g(k+1))**2-(1-g(k+1))))
print("1/(1-g_k)=1+g_{k-1}:",sp.simplify(1/(1-g(k))-(1+g(k-1))))
# X1.3: A0 = N I + l^2 phi^2 11^T ; gamma_k = l^2phi^2/(N+k l^2 phi^2) = 1/(kappa+k) with kappa=N/(l^2phi^2)
print("gamma:",sp.simplify(ell**2*phi**2/(N+k*ell**2*phi**2)-1/(N/(ell**2*phi**2)+k)))

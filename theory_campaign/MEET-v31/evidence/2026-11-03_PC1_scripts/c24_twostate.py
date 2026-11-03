# Two-state masked example: Omega={a,b}, pi0(a)=eps, pi(a)=1-delta; one particle, one stage (Zhat/Z = pi(x)/pi0(x), x~pi0)
from fractions import Fraction as Fr
eps,delta=Fr(1,100),Fr(1,100)
vals={'a':((1-delta)/eps,eps),'b':(delta/(1-eps),1-eps)}   # W value, prob
EW=sum(w*q for w,q in vals.values()); print("E W =",EW)
print("P(W>1) =",sum(q for w,q in vals.values() if w>1)," value",vals['a'][0])
print("P(0.05 Zhat > Z) = P(W>20) =",sum(q for w,q in vals.values() if w>20),"<= 0.05")
# top store T={x}: Z_T/Z = pi(x) <= 1; L/Z = max(pi(x), 0.05 W)
PL=sum(q for x,(w,q) in vals.items() if max((1-delta) if x=='a' else delta, Fr(1,20)*w)>1)
print("P(L>Z) =",PL)
print("E(W-1)+ =",sum(q*max(w-1,0) for w,q in vals.values())," E(1-W)+ =",sum(q*max(1-w,0) for w,q in vals.values()))

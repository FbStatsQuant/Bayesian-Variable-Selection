import math
for n in (10,20,100):
    nu=.01+n/2
    q2=(n-1)/n
    q1=(n-1)*(1+1/n)/2
    q0=n-1
    odds=2*math.sqrt(n)*((.02+q2)/(.02+q1))**nu+3*n*((.02+q2)/(.02+q0))**nu
    print(n, 'delta=',odds/(1+odds),'LB=',1/(1+math.sqrt(n+1)))

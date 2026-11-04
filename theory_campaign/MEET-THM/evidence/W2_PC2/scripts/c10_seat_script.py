# Seat C's quoted C10 scratch script, verbatim (R2_C.md line 179)
import math
n,p,Y=40,20,39
nu=.01+n/2
z2=Y*Y*.5
for k in (0,1,2):
    gain=0 if not k else n*k*z2/(1+(n+1)*k*(n-1))
    det=1 if not k else (1+(n+1)*k*(n-1))/(1+k*(n-1))
    logbf=-.5*math.log(det)-nu*math.log1p(-gain/(.02+Y))
    prior=math.lgamma(k+1)+math.lgamma(2*p-k)-math.lgamma(2*p)
    print(k, 'log_start_relative_to_empty=', round(logbf+prior,9))
print('models=',2**p,'dispatch_cutoff=',200000+64*n*p)

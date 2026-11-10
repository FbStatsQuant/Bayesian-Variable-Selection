import math
# Leading coefficients, p=n-1, s0=floor(n**a), q=s0+2.
a=.49; rho=.30
h=3-2*a
print("prior+det deletion threshold / log n:",h)
print("selected extreme-pair deletion gains / log n:",2*(1+rho))
print("largest remaining addition gain / log n:",2*(1+rho)/(1+2*rho))
print("superset floor:",1-rho,"advertised floor threshold:",2/3)
print("pair total likelihood gain / log n:",2.,"pair total prior+det cost / log n:",h)
assert 2*(1+rho)>h>2*(1+rho)/(1+2*rho)
assert 1-rho>2/3

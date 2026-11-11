import math
def c0(s0,A):
    j=math.ceil((2*A+1)*s0)+1
    Cs=2*s0+3*(A*j+s0+math.log(j+1)+1)
    return max(4*Cs,32*(s0*(A+1)+2)), 4*Cs
def c1(s0,A):
    j=math.ceil((2*A+1)*s0)+1; CA=8+3*A
    Cx=A*j+s0+math.log(j+1)+2
    return (math.sqrt(2*Cx)+math.sqrt(2*Cx+CA*j+(2/math.log(2))*(s0*(A+1)+2)))**2
for s0 in [1,2,3,5,10]:
    for A in [1,1.5,2,3,5]:
        a,b=c0(s0,A); print(s0,A,'c0=%.1f (4C*=%.1f)'%(a,b),'c1=%.1f'%c1(s0,A), 'c1<c0' if c1(s0,A)<a else '')

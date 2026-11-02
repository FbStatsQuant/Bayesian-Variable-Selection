"""API-FAVIID: independent check of c_ML = min_c c*E_{1/2}(1/c), E_{1/2}(x) = sum_j x^j/Gamma(j/2+1) = exp(x^2) erfc(-x).
Deterministic. Also checks the closed form against the series."""
import math
E = lambda x: math.exp(x * x) * math.erfc(-x)
S = lambda x: sum(x ** j / math.gamma(j / 2 + 1) for j in range(200))
f = lambda c: c * E(1 / c)
lo, hi = 0.5, 5.0
for _ in range(200):  # golden-section (f is unimodal on this range)
    a = hi - (hi - lo) / 1.618033988749895; b = lo + (hi - lo) / 1.618033988749895
    if f(a) < f(b): hi = b
    else: lo = a
c = (lo + hi) / 2
print("argmin c = %.4f, c_ML = %.5f ; f(1.684) = %.5f ; series vs closed form at 1/1.684: %.3e" % (c, f(c), f(1.684), abs(S(1/1.684) - E(1/1.684))))

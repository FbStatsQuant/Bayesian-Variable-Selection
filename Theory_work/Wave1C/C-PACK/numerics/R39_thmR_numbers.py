"""Recompute Theorem R's t*, I*, K_n at rho=0.7, psi_bar=0.5, (n,p)=(200,500) (formulas: item5 02_design_events.md §2.3)."""
import math
rho, psi, n, p = 0.7, 0.5, 200, 500
q = math.sqrt((1 - psi**2) / (1 - rho**2))
t = (q - 1) / (q * rho - psi)
I = lambda t, r: -0.5 * math.log((1 - r*r) * (1 - t*t) / (1 - r*t)**2)
Ist = I(t, psi)
print(f"t*={t:.10f}  I(t*;psi)={Ist:.10f}  I(t*;rho)={I(t, rho):.10f}")
K = 2 / (math.sqrt(math.pi) * (1 - rho)) * p**2 * math.sqrt(n) * math.exp(-(n - 4) * Ist)
print(f"K_n(200,500)={K:.9e}")

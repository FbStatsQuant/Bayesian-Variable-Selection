"""W5-B2ENV s1b: STAB-LH for c = 2 (two linked pairs), type-based exact computation (s1_stab.margins_types).
Deterministic.  Pairs (0,1) and (2,3), equal psi; beta_a1 = 1.4, beta_a2 = 1.8 (no visible group) unless stated."""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from s1_stab import margins_types
out = []
for g in (4, 9):
    for rho in (0.4, 0.7, 0.85):
        for psi in (0.1, 0.2, 0.35, 0.5):
            if psi >= rho: continue
            for vis in ({0: 1.4, 2: 1.8}, {0: 1.4, 2: 1.4}):
                md, ms, mg, arg = margins_types(g, rho, [(0, 1, psi), (2, 3, psi)], vis)
                ok = "OK  " if min(md, ms, mg) > 1e-9 else "FAIL"
                s = (f"{ok} c=2 g={g} rho={rho} psi={psi} betas={list(vis.values())}: m_del={md:.4f} m_swap={ms:.4f} "
                     f"m_gain={mg:.4f} worst swap {arg['swap']}")
                out.append(s); print(s, flush=True)
open(__file__.replace(".py", ".txt"), "w").write("\n".join(out) + "\n")

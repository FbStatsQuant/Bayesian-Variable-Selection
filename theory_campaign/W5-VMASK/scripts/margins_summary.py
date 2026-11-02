"""Summary of ../results/margins_grid.txt: how tight are PXN's c2 and T38FULL's m0 against the brute-force minimum.
Output appended to ../results/margins_grid.txt"""
import ast, numpy as np
rows = open('../results/margins_grid.txt').read().split('\n')
rc, rm, rcin, rmin_ = [], [], [], []
for r in rows:
    if '|' not in r or not r[0].isdigit():
        continue
    parts = r.split('|')
    left = parts[0].split(' ', 2)
    c, rho = int(left[0]), float(left[1])
    rest = left[2]; i = rest.index(']') + 1; psis = ast.literal_eval(rest[:i])
    c2, ba, bL = map(float, parts[1].split())
    m0, b2 = map(float, parts[2].split())
    inside = all(abs(s) < rho for s in psis)
    rc.append(c2 / ba); (rcin.append(c2 / ba) if inside else None)
    if c >= 2:
        rm.append(m0 / b2); (rmin_.append(m0 / b2) if inside else None)
s = [f"c2/brute_all: min {min(rc):.3f}, median {np.median(rc):.3f}, max {max(rc):.3f} (all rows); inside |psi|<rho: min {min(rcin):.3f} median {np.median(rcin):.3f}",
     f"m0/brute_phi2 (c>=2): min {min(rm):.3f}, median {np.median(rm):.3f}, max {max(rm):.3f}; inside: min {min(rmin_):.3f} median {np.median(rmin_):.3f}"]
print("\n".join(s))
open('../results/margins_grid.txt', 'a').write("\nTightness summary\n" + "\n".join(s) + "\n")

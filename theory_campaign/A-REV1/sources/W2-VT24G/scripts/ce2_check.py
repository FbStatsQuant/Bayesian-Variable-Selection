"""CE2 re-check (W2-VT24G). Abstract chain on {v, v-1, ..., 0}: each round moves down by exactly one w.p. c,
never up (it satisfies every hypothesis of a 'one correct step per round w.p. >= c' argument).
P(not at 0 after H rounds) = P(Bin(H, c) < v) exactly. Compare with the brief's form (1-c)^{floor(H/v)} and
W1's corrected form v (1-c)^{floor(H/v)}. Exact arithmetic (fractions)."""
from fractions import Fraction as Fr
from math import comb
import json, sys

def binlt(H, c, v):
    return sum(comb(H, k) * c**k * (1 - c)**(H - k) for k in range(min(v, H + 1)))

rows = []; viol = 0
for v in range(1, 8):
    for H in range(0, 30):
        for c in [Fr(1, 20), Fr(1, 7), Fr(1, 3), Fr(1, 2), Fr(9, 10)]:
            exact = binlt(H, c, v)
            brief = (1 - c) ** (H // v)
            w1 = v * (1 - c) ** (H // v)
            if exact > brief: viol += 1
            assert exact <= w1, (v, H, c)
            if (v, H) in [(2, 2), (2, 12), (5, 12), (12, 12), (13, 12)]:
                rows.append(dict(v=v, H=H, c=str(c), exact=float(exact), brief=float(brief), w1=float(min(1, w1))))
print('cases where exact > (1-c)^floor(H/v):', viol, '; v(1-c)^floor(H/v) >= exact in all cases')
for r in rows: print(r)
json.dump(dict(violations_of_brief_form=viol, rows=rows), open(sys.argv[1], 'w'), indent=1)

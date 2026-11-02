"""IND-T sanity check (W2-PREM).

The v3 engine (cpp/v3_engine.h, population_round) gives each final island ONE uniform stream and lets the
particles consume it sequentially: round h = particle 1, particle 2, ..., particle N, each consuming a
STATE-DEPENDENT number of uniforms (uniform swap skipped at |S| in {0,p}, neighbour swap rejected without
draws when N(j)\\S is empty, pi0 draw uses 1 + #nonempty-block-steps + #nonzero blocks uniforms, ...).

Lemma IND-T (PROOF.md §1) says: under EX-S (ideal iid uniforms) this is the same joint law as N independent
Markov chains. This script checks the claim on a toy chain whose per-round uniform consumption depends on the
state, by comparing the joint law of (X1_H, X2_H) under the shared sequential stream with the product of the
marginals, and with the law under separate streams. Fixed seed. Output: results/ind_streams.txt
"""
import numpy as np
from itertools import product

SEED = 20261102
STATES = 4
H = 3
REPS = 400_000


class Stream:
    """Sequential consumer of an iid U(0,1) stream (block-buffered for speed)."""
    def __init__(self, rng):
        self.rng = rng
        self.buf = rng.random(1 << 16)
        self.i = 0

    def u(self):
        if self.i == len(self.buf):
            self.buf = self.rng.random(1 << 16)
            self.i = 0
        v = self.buf[self.i]
        self.i += 1
        return v


def one_round(x, s):
    """A toy 'round': a random order of 3 labels, each consuming a state-dependent number of uniforms."""
    # order: Fisher-Yates on 3 labels (2 uniforms), like draw_order
    order = [0, 1, 2]
    for i in range(2, 0, -1):
        j = int(s.u() * (i + 1))
        order[i], order[j] = order[j], order[i]
    for lab in order:
        if lab == 0:            # 'Gibbs-like': always one uniform
            x = (x + 1) % STATES if s.u() < 0.3 + 0.1 * x else x
        elif lab == 1:          # 'swap-like': skipped (no uniform) in state 0, else 3 uniforms
            if x == 0:
                continue
            a, b, c = s.u(), s.u(), s.u()
            if c < 0.5 * a:
                x = int(b * STATES)
        else:                   # 'independence-like': variable number of uniforms (geometric-ish)
            k = 1
            while s.u() < 0.4 and k < 5:
                k += 1
            if s.u() < 0.2:
                x = (x + k) % STATES
    return x


def run(shared, rng, x0=(0, 2)):
    counts = np.zeros((STATES, STATES))
    if shared:
        s = Stream(rng)
        for _ in range(REPS):
            x = list(x0)
            for _h in range(H):
                for i in range(2):          # particle 1 then particle 2, same stream
                    x[i] = one_round(x[i], s)
            counts[x[0], x[1]] += 1
    else:
        s1, s2 = Stream(np.random.default_rng(rng.integers(1 << 62))), Stream(np.random.default_rng(rng.integers(1 << 62)))
        for _ in range(REPS):
            x = list(x0)
            for _h in range(H):
                x[0] = one_round(x[0], s1)
                x[1] = one_round(x[1], s2)
            counts[x[0], x[1]] += 1
    return counts / REPS


def chi2_indep(P, n):
    m1, m2 = P.sum(1), P.sum(0)
    E = np.outer(m1, m2)
    return n * np.sum((P - E) ** 2 / np.where(E > 0, E, 1)), (STATES - 1) ** 2


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    Ps = run(True, rng)
    Pi = run(False, rng)
    out = []
    c, df = chi2_indep(Ps, REPS)
    out.append(f"shared sequential stream: chi2 independence statistic {c:.2f} on {df} df (5% critical 16.92)")
    c2, df2 = chi2_indep(Pi, REPS)
    out.append(f"separate streams        : chi2 independence statistic {c2:.2f} on {df2} df")
    tv = 0.5 * np.abs(Ps - Pi).sum()
    out.append(f"total variation between joint laws (shared vs separate): {tv:.4f} (MC noise scale ~ {np.sqrt(STATES**2/REPS):.4f})")
    out.append("joint law (shared):\n" + np.array2string(Ps, precision=4))
    out.append("joint law (separate):\n" + np.array2string(Pi, precision=4))
    txt = "\n".join(out)
    print(txt)
    with open(__file__.replace("scripts/ind_streams.py", "results/ind_streams.txt"), "w") as f:
        f.write(txt + "\n")

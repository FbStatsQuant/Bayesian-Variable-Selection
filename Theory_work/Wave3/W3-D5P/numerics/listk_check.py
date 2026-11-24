"""Brute-force falsification of LIST-K (STATEMENT (C1)) on random small model spaces.
Exact rationals are not needed: double precision with a 1e-12 slack; any violation is printed.
Run: python3 -I numerics/listk_check.py > numerics/listk_check_out.txt"""
import itertools, math, random

def models(p, K):
    return [frozenset(c) for k in range(K + 1) for c in itertools.combinations(range(p), k)]

def run(trials=20000, seed=20261117):
    rng = random.Random(seed); worst = {}; viol = []
    def upd(k, v): worst[k] = max(worst.get(k, -1e9), v)
    for t in range(trials):
        p = rng.randint(1, 7); K = rng.randint(1, p); Om = models(p, K)
        s0 = frozenset(rng.sample(range(p), rng.randint(0, K)))
        scale = rng.choice([0.5, 2, 10, 50])
        F = {S: rng.gauss(0, scale) for S in Om}
        if rng.random() < 0.5: F[s0] = max(F.values()) + rng.expovariate(1.0) * scale  # S0 often the mode
        Fm = max(F.values()); Z = sum(math.exp(F[S] - Fm) for S in Om)
        pi = {S: math.exp(F[S] - Fm) / Z for S in Om}
        eps = 1 - pi[s0]
        others = [S for S in Om if S != s0]
        T = set(rng.sample(others, rng.randint(0, len(others)))) | {s0}
        ZT = sum(math.exp(F[S] - Fm) for S in T); piT = {S: math.exp(F[S] - Fm) / ZT for S in T}
        mT = sum(pi[S] for S in T)
        pipT = [sum(piT[S] for S in T if j in S) for j in range(p)]
        PIP = [sum(pi[S] for S in Om if j in S) for j in range(p)]
        a = max(abs(pipT[j] - (j in s0)) for j in range(p))
        upd('a: max|pipT-1S0| - (1-piT(S0))', a - (1 - piT[s0])); upd('a: 1-piT(S0) - eps', (1 - piT[s0]) - eps)
        b = max(abs(pipT[j] - PIP[j]) for j in range(p)); upd('b: max|pipT-PIP| - (1-pi(T))', b - (1 - mT))
        # TV identity over all events of Omega (small Omega only)
        if len(Om) <= 12:
            tv = 0.0
            for r in range(len(Om) + 1):
                for A in itertools.combinations(Om, r):
                    tv = max(tv, abs(sum(piT.get(S, 0) for S in A) - sum(pi[S] for S in A)))
            upd('b: |TV - (1-pi(T))|', abs(tv - (1 - mT)))
        if eps < 0.5:
            mpmT = frozenset(j for j in range(p) if pipT[j] > 0.5); MPM = frozenset(j for j in range(p) if PIP[j] > 0.5)
            if mpmT != s0 or MPM != s0: viol.append(('c', t))
        logZ = Fm + math.log(Z); logZT = Fm + math.log(ZT)
        upd('d: |logZT-(logZ+log pi(T))|', abs(logZT - (logZ + math.log(mT))))
        upd('d: logZT - logZ', logZT - logZ)
        if pi[s0] > 0: upd('d: logZ+log(pi(S0)) - logZT', logZ + math.log(pi[s0]) - logZT)
        if pi[s0] > 0: upd('d: (logZ-logZT) - eps/(1-eps)', (logZ - logZT) - (1 - pi[s0]) / pi[s0])
    return worst, viol, trials

if __name__ == '__main__':
    worst, viol, n = run()
    print(f'trials={n}; every "worst" value must be <= 1e-12 (inequality slack) or ~0 (identities)')
    for k, v in sorted(worst.items()): print(f'{k:42s} worst = {v:.3e}  {"OK" if v <= 1e-12 else "VIOLATION"}')
    print('clause (c) violations:', len(viol))

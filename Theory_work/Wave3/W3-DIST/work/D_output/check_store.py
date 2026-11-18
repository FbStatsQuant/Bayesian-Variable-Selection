"""Sanity check for P6_DISTC.md Lemma R (store retention), and for Lemma P6 (a), (b).
Replicates TopStore::offer of cpp/v3_ledger.h:43-57 (order TopCmp, hpm_order = true, :35-42) in Python
and checks, after every offer, that the store equals the cap best distinct offered models.
DRAFT (by this seat, unchecked)."""
import random, itertools, functools

def key(entry):                      # TopCmp with hpm_order: larger v, then smaller size, then lexicographic
    v, S = entry
    return (-v, len(S), S)          # python tuple order on sorted index tuples = std::lexicographical_compare

class TopStore:
    def __init__(self, cap): self.cap, self.s = cap, []       # s kept sorted by key (std::set)
    def offer(self, v, S):
        e = (v, S)
        if self.cap == 0: return False
        if len(self.s) >= self.cap and not key(e) < key(self.s[-1]): return False   # quick reject (:52)
        if e in self.s: return False                                                # (:53)
        self.s.append(e); self.s.sort(key=key)                                       # (:54)
        if len(self.s) > self.cap: self.s.pop()                                      # (:55)
        return True

def run(trials=3000, seed=1):
    rng = random.Random(seed)
    for _ in range(trials):
        p = rng.randint(2, 6); K = rng.randint(1, p)
        models = [tuple(c) for k in range(K + 1) for c in itertools.combinations(range(p), k)]
        # values: deterministic function of the model; few distinct values to force ties
        val = {S: float(rng.randint(0, 4)) for S in models}
        if rng.random() < 0.5:                                  # sometimes a unique maximiser
            star = rng.choice(models); val[star] = 10.0
        cap = rng.randint(1, len(models) + 2)
        st = TopStore(cap); offered = set()
        for _ in range(rng.randint(1, 4 * len(models))):
            S = rng.choice(models); st.offer(val[S], S); offered.add(S)
            best = sorted(((val[T], T) for T in offered), key=key)[:cap]
            assert st.s == best, (st.s, best)
        m = max(val.values())
        top = [S for S in models if val[S] == m]
        if len(top) == 1 and top[0] in offered:
            assert (m, top[0]) in st.s and st.s[0] == (m, top[0])
    print("store invariant and retention: OK,", trials, "trials")

def check_p6(trials=2000, seed=2):
    rng = random.Random(seed)
    for _ in range(trials):
        k = rng.randint(1, 8)
        pi = [rng.random() for _ in range(k)]; Z = sum(pi); pi = [x / Z for x in pi]
        cond = [rng.random() for _ in range(k)]          # Pi(B | S, D)
        PiB = sum(a * b for a, b in zip(pi, cond))
        T = [i for i in range(k) if rng.random() < 0.6] or [0]
        piT = sum(pi[i] for i in T)
        QB = sum(pi[i] / piT * cond[i] for i in T)       # store BMA
        assert QB <= PiB / piT + 1e-12                    # (a) with L = 1/pi(T)
        a = rng.random()
        bad = [i for i in range(k) if cond[i] > a]
        assert sum(pi[i] for i in bad) <= PiB / a + 1e-12  # (b)
    print("Lemma P6 (a), (b): OK,", trials, "trials")

if __name__ == "__main__":
    run(); check_p6()

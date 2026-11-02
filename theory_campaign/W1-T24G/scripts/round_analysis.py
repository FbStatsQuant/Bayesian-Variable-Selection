"""
Per-state exact quantities of the terminal round K_1 on R_{d,e} and the restated-T24 bound.

For x in R\\{S0} and each label e (p Gibbs labels, 1 uniform swap, n_nb neighbour swaps, 1 independence):
  s_e(x) = P(label e executed at x moves to a state x' in R with V(x') < V(x))       [progress]
  b_e(x) = P(label e executed at x moves to any other state x' != x)                   [other change]
  inc_e(x) = P(e at x -> x' in R with V(x') > V(x))                                   [non-fatal increase]
  ex_e(x)  = P(e at x -> x' not in R)                                                  [fatal exit]
Gibbs labels also 'score' S0 without moving: sc_e(x) = 1 if e is Gibbs j and x xor S0 subset {j}.
We treat a Gibbs evaluation that scores S0 as progress (it ends the repair).

Exact first-change progress probability (Lemma P of PROOF.md):
  P*(x) = sum_e s~_e(x) * int_0^1 prod_{j != e} (1 - t q_j(x)) dt,
  q_j = s~_j + b~_j, where for a scoring Gibbs label s~ = 1 (it ends the repair whatever the draw).
Polynomial lower bound (Corollary P'): for every label set D not containing g,
  c_poly(x) = max_{g,D} s~_g(x) * [1 - Q_{D^c}(x)/(|D|+2)] / (|D|+1),  Q_{D^c} = sum_{j notin D u {g}} q_j(x).
"""
import math, sys, json
import numpy as np
from bvs_engine import *

GL_T, GL_W = np.polynomial.legendre.leggauss(40)
GL_T = 0.5 * (GL_T + 1); GL_W = 0.5 * GL_W


def label_laws(M, x):
    laws = []
    for j in range(M.p):
        laws.append(('G', j, M.gibbs_law(x, j)))
    laws.append(('U', -1, M.uswap_law(x)))
    nl = M.nswap_law(x)
    for i in range(M.n_nb):
        laws.append(('N', i, nl))
    return laws


class IndTables:
    """sum_{S' in cat} pi0(S') min(1, e^{d(S')-d(x)}) for categories V<V(x), V=V(x), V>V(x) (in R) and R^c."""
    def __init__(self, M, inR, V):
        self.M = M; self.inR = inR; self.V = V
        self.cats = {}
        keys = np.where(inR, V, -1)
        for c in np.unique(keys):
            sel = keys == c
            dd = M.d[sel]; w = M.pi0[sel]
            o = np.argsort(dd); dd = dd[o]; w = w[o]
            mx = dd.max()
            self.cats[int(c)] = (dd, np.concatenate([[0], np.cumsum(w)]),
                                 np.concatenate([[0], np.cumsum(w * np.exp(dd - mx))]), mx)
    def acc(self, c, dx):
        dd, cw, cwe, mx = self.cats[c]
        i = np.searchsorted(dd, dx, side='left')
        return (cw[-1] - cw[i]) + cwe[i] * math.exp(mx - dx)
    def self_acc(self, x):
        return self.M.pi0[x]
    def query(self, x):
        Vx = self.V[x]; dx = self.M.d[x]
        lo = eq = hi = out = 0.0
        for c in self.cats:
            a = self.acc(c, dx)
            if c == -1: out += a
            elif c < Vx: lo += a
            elif c == Vx: eq += a
            else: hi += a
        eq -= self.M.pi0[x]
        return lo, eq, hi, out, lo + eq + hi + out + self.M.pi0[x]


def classify(M, x, inR, V, accind=None):
    """returns arrays s, b, inc, ex (length m) and score flags."""
    S0 = M.S0
    laws = label_laws(M, x)
    m = len(laws) + 1
    s = np.zeros(m); b = np.zeros(m); inc = np.zeros(m); ex = np.zeros(m); sc = np.zeros(m, bool)
    for i, (typ, j, law) in enumerate(laws):
        if typ == 'G' and ((x ^ S0) & ~(1 << j)) == 0:
            sc[i] = True
        if typ == 'U' or typ == 'N':
            # swaps score their proposal; a proposal equal to S0 ends the repair
            pass
        for dest, pr in law:
            if dest == x or pr <= 0:
                continue
            if not inR[dest]:
                ex[i] += pr; b[i] += pr
            elif V[dest] < V[x]:
                s[i] += pr
            else:
                b[i] += pr
                if V[dest] > V[x]:
                    inc[i] += pr
    # swap proposals of S0 score it: count proposal probability (accepted or not) as progress
    for i, (typ, j, law) in enumerate(laws):
        if typ in ('U', 'N'):
            pass  # handled via s (accepted moves to S0 have V=0 < V(x)); rejected proposals of S0 ignored (conservative)
    # independence (fast: per-category sorted tables, see IndTables)
    T = accind
    lo, eq, hi, out_, tot = T.query(x)
    ex[-1] = out_
    s[-1] = lo + (M.pi0[S0] * (1 - min(1.0, math.exp(M.d[S0] - M.d[x]))) if x != S0 else 0.0)
    inc[-1] = hi
    b[-1] = tot - lo - T.self_acc(x)
    st = s.copy(); st[sc] = 1.0
    bt = b.copy(); bt[sc] = 0.0
    return st, bt, inc, ex


def pstar(st, bt):
    q = np.clip(st + bt, 0, 1)
    tot = 0.0
    # prod_{j != e}(1 - t q_j) = prod_all / (1 - t q_e)  (careful when t q_e = 1)
    for e in np.nonzero(st > 0)[0]:
        qq = np.delete(q, e)
        vals = np.prod(1 - GL_T[:, None] * qq[None, :], axis=1)
        tot += st[e] * (GL_W @ vals)
    return min(1.0, tot)


def cpoly(st, bt):
    q = np.clip(st + bt, 0, 1)
    best = 0.0
    for g in np.nonzero(st > 0)[0]:
        rest = np.sort(np.delete(q, g))[::-1]
        tail = np.concatenate([np.cumsum(rest[::-1])[::-1], [0.0]])   # tail[k] = sum rest[k:]
        for k in range(len(rest) + 1):
            val = st[g] * (1 - tail[k] / (k + 2)) / (k + 1)
            best = max(best, val)
    return best


def analyse(M, d, e, states=None, verbose=False):
    inR, V, miss, extra = region_arrays(M, d, e)
    Rlist = np.nonzero(inR)[0]
    if states is None:
        states = [int(x) for x in Rlist if x != M.S0]
    m = M.m_labels
    sup_inc = np.zeros(m); sup_ex = np.zeros(m)
    recs = []
    T = IndTables(M, inR, V)
    for x in states:
        st, bt, inc, ex = classify(M, x, inR, V, T)
        sup_inc = np.maximum(sup_inc, inc); sup_ex = np.maximum(sup_ex, ex)
        recs.append(dict(x=x, V=int(V[x]), miss=int(miss[x]), extra=int(extra[x]),
                         pstar=pstar(st, bt), cpoly=cpoly(st, bt),
                         inc=float(inc.sum()), ex=float(ex.sum()),
                         logpi=float(M.logpi[x]), logpi0=float(M.logpi0[x])))
    # also S0 itself for the sups (increase/exit from S0)
    st, bt, inc, ex = classify(M, M.S0, inR, V, T)
    sup_inc = np.maximum(sup_inc, inc); sup_ex = np.maximum(sup_ex, ex)
    return recs, sup_inc, sup_ex, inR, V


def binom_tail_lt(H, c, k):
    """P(Bin(H,c) < k)."""
    return sum(math.comb(H, i) * c ** i * (1 - c) ** (H - i) for i in range(min(k, H + 1)))


def theorem_bound(H, cprime, iota, eta, Vmax):
    best = (1.0, None)
    for w in range(1, H + 1):
        win = min(1.0, w * iota + binom_tail_lt(w, cprime, Vmax))
        val = win ** (H // w) + H * eta
        if val < best[0]:
            best = (val, w)
    return best

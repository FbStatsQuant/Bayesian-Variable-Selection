"""item1_um_checks.py -- numerical checks of Lemma UM and Lemma UM-FP (Theory_work/Wave1C/C-PACK/lemmas/I1_e4_replacement.md)
against the FROZEN start_mode (v3_start.h:183-240), driven through the W1-N3 harness sm_harness.exe (read-only use).

Run:  C:/Users/felip/AppData/Local/Programs/Python/Python313/python.exe -B item1_um_checks.py
(needs numpy; the default `python` 3.15 on this PC has no numpy.)  Output: item1_um_checks_out.txt (same folder).

Parts
 (A) Lemma UM, exact arithmetic (integer tables, every sum exact in binary64), TABLE mode, caps 1, 2, 10^6.
 (B) Lemma UM-FP, binary64 random double tables (magnitudes 1..2^45), near-tie instances, eta = 0.
 (C) DATA mode (full coded pipeline), LH-like equicorrelated groups, p <= 12, n in {50,200,800}, 20 seeds each.
Seeds: A 20261109 ; B 20261110 ; C default_rng([20261111, n, s]) for n in {50,200,800}, s = 0..19.
Exact objects: f-hat(S) = exact real sum of the stored doubles (python ints scaled by 2^L), full enumeration of Omega_K.
"""
import sys, os, math, time, random
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W1N3 = r"C:\Users\felip\Bayesian-Variable-Selection\Theory_work\Wave1\W1-N3\numerics"
sys.path.insert(0, W1N3)
import numpy as np
import mpmath as mp
from fractions import Fraction
from collections import Counter
import n3lib
from n3lib import Inst, run_tables, run_data

mp.mp.dps = 50
T0 = time.time()
SEED_A, SEED_B = 20261109, 20261110
U53 = 1 << 53  # 1/u

# ----------------------------------------------------------------------------------------------------------
# exact machinery
_cache = {}


def struct(p, blocks):
    key = (p, tuple(tuple(b) for b in blocks))
    if key in _cache:
        return _cache[key]
    if len(_cache) > 40:
        _cache.clear()
    masks = np.arange(1 << p, dtype=np.int64)
    pop = np.zeros(1 << p, dtype=np.int64)
    for i in range(p):
        pop += (masks >> i) & 1
    codes, mm = [], np.zeros(1 << p, dtype=np.int64)
    for C in blocks:
        c = np.zeros(1 << p, dtype=np.int64)
        for i, x in enumerate(C):
            c |= ((masks >> x) & 1) << i
        codes.append(c)
        mm += (c != 0)
    S = (pop, codes, mm)
    _cache[key] = S
    return S


def pow2exp(v):
    n, d = float(v).as_integer_ratio()
    return d.bit_length() - 1


def mask_list(mask, p):
    return [i for i in range(p) if (mask >> i) & 1]


def analyze(I, want_pi=False, want_g=True):
    """Exact analysis of the instance's stored doubles: f-hat on every S in Omega_K, N, R, margin, eps, (pi0), g-hat."""
    p, K = I.p, I.K
    pop, codes, mm = struct(p, I.blocks)
    valid = np.nonzero(pop <= K)[0]
    lamf = [float(x) for x in I.lam]
    L = 0
    for v in lamf:
        assert math.isfinite(v)
        L = max(L, pow2exp(v))
    rhof = []
    for b, C in enumerate(I.blocks):
        m = len(C)
        arr = [0.0] * (1 << m)
        for c in range(1, 1 << m):
            if bin(c).count("1") <= K:
                v = float(I.rho[b][c])
                assert math.isfinite(v), ("non-finite table entry", b, c)
                arr[c] = v
                L = max(L, pow2exp(v))
        rhof.append(arr)
    sc = 1 << L

    def toint(v):
        n, d = float(v).as_integer_ratio()
        assert sc % d == 0
        return n * (sc // d)

    lam_i = np.array([toint(v) for v in lamf] + [0] * (p - K), dtype=object)
    lam_a = np.array([abs(toint(v)) for v in lamf] + [0] * (p - K), dtype=object)
    pv = pop[valid]
    f = lam_i[pv]
    ab = lam_a[pv]
    rho_i = [np.array([toint(v) for v in arr], dtype=object) for arr in rhof]
    rho_a = [np.array([abs(toint(v)) for v in arr], dtype=object) for arr in rhof]
    for b in range(len(I.blocks)):
        cb = codes[b][valid]
        f = f + rho_i[b][cb]
        ab = ab + rho_a[b][cb]
    fl = f.tolist()
    fmax = max(fl)
    argm = [i for i, v in enumerate(fl) if v == fmax]
    N = len(argm)
    A = dict(p=p, K=K, sc=sc, L=L, valid=valid, fl=fl, f_obj=f, abs_obj=ab, N=N, fmax=fmax,
             lamf=lamf, rhof=rhof, mmv=mm[valid], pop_v=pv, codes=codes)
    i0 = argm[0]
    A["Rmask"] = int(valid[i0])
    A["Rlist"] = mask_list(A["Rmask"], p)
    # margin to the best other set
    second, j2 = None, None
    for i, v in enumerate(fl):
        if i != i0 and (second is None or v > second):
            second, j2 = v, i
    if second is None:
        A["delta"] = None
        A["S2mask"] = None
    else:
        A["delta"] = Fraction(fmax - second, sc)  # 0 if N > 1
        A["S2mask"] = int(valid[j2])
    # eps (lemma definition): max_S gamma_{m(S)} (|lam|(|S|) + sum_b |rho_b(S_b)|), gamma_m = m u/(1 - m u)
    eps = Fraction(0)
    mmv = A["mmv"]
    for mval in np.unique(mmv):
        mval = int(mval)
        if mval == 0:
            continue
        sel = (mmv == mval)
        mx = max(ab[sel].tolist())
        eps = max(eps, Fraction(mval * mx, (U53 - mval) * sc))
    A["eps"] = eps
    A["ab"] = ab
    # crude quantities
    A["Lam"] = max(abs(v) for v in lamf)
    A["That"] = max([abs(v) for arr in rhof for v in arr] + [0.0])
    if want_pi and N == 1 and second is not None:
        cnt = Counter(v - fmax for i, v in enumerate(fl) if i != i0)
        zf = 0.0
        for d, c in cnt.items():
            x = float(Fraction(d, sc))
            zf += c * (math.exp(x) if x > -700 else 0.0)
        if abs(zf - 1.0) < 1e-6:
            z = mp.mpf(0)
            for d, c in cnt.items():
                z += c * mp.exp(mp.mpf(d) / sc)
            zf = float(z)
            gt_half = bool(z < 1)
        else:
            gt_half = zf < 1.0
        A["pi0"] = 1.0 / (1.0 + zf)
        A["pi0_gt_half"] = gt_half
    elif N == 1:
        A["pi0"] = 1.0
        A["pi0_gt_half"] = True
    if want_g:
        s = np.zeros(len(valid))
        for b in range(len(I.blocks)):
            s = s + np.array(rhof[b], dtype=np.float64)[codes[b][valid]]
        lam_f = np.array(lamf + [0.0] * (p - K), dtype=np.float64)
        A["g"] = lam_f[pv] + s
    return A


def popc(c):
    return bin(c).count("1")


def rand_blocks(rng, p, maxb=5):
    perm = rng.permutation(p).tolist()
    blocks, i = [], 0
    while i < p:
        sz = int(rng.integers(1, min(maxb, p - i) + 1))
        blocks.append(sorted(perm[i:i + sz]))
        i += sz
    order = rng.permutation(len(blocks))
    return [blocks[j] for j in order]


# ----------------------------------------------------------------------------------------------------------
REPORT = {"A": [], "B": [], "C": []}
CONTRA = []


def rep(sec, line=""):
    REPORT[sec].append(line)
    print(line, flush=True)


# ----------------------------------------------------------------------------------------------------------
# (A)
def make_A(rng, fam):
    p = int(rng.integers(1, 13))
    blocks = rand_blocks(rng, p, 5)
    K = int(rng.integers(0, p + 1))
    lo, hi = {"wide": (-1000, 1000), "mid": (-20, 20), "small": (-3, 3), "tiny": (-1, 1), "planted": (-3, 3)}[fam]
    lam = [int(rng.integers(lo, hi + 1)) for _ in range(K + 1)]
    rho = []
    for C in blocks:
        m = len(C)
        rho.append({c: int(rng.integers(lo, hi + 1)) for c in range(1, 1 << m) if popc(c) <= K})
    if fam == "planted":
        k = int(rng.integers(0, K + 1))
        Rset = sorted(rng.permutation(p)[:k].tolist())
        bonus = int(rng.choice([1, 2, 3, 5, 8]))
        pos = {}
        for b, C in enumerate(blocks):
            for i, x in enumerate(C):
                pos[x] = (b, i)
        codes = {}
        for x in Rset:
            b, i = pos[x]
            codes[b] = codes.get(b, 0) | (1 << i)
        if rng.random() < 0.3 or not codes:
            lam[k] += bonus
        else:
            for b, c in codes.items():
                rho[b][c] += bonus
    return Inst(p, K, blocks, lam, rho, 10**6, "a")


def part_A():
    rng = np.random.default_rng(SEED_A)
    fams = [("wide", 1500), ("mid", 1500), ("small", 1500), ("tiny", 800), ("planted", 2400)]
    uniq, nonuniq = [], 0
    attempts = Counter()
    t = time.time()
    for fam, n in fams:
        for _ in range(n):
            I = make_A(rng, fam)
            attempts[fam] += 1
            A = analyze(I, want_pi=True, want_g=False)
            if A["N"] != 1:
                nonuniq += 1
                continue
            uniq.append((fam, I, A))
    rep("A", f"[A] generated {sum(attempts.values())} instances ({dict(attempts)}); unique exact maximiser: {len(uniq)}; "
             f"excluded (non-unique argmax f): {nonuniq}; gen+exact time {time.time() - t:.1f}s")
    caps = (1, 2, 10**6)
    jobs = []
    for idx, (fam, I, A) in enumerate(uniq):
        for cap in caps:
            J = Inst(I.p, I.K, I.blocks, I.lam, I.rho, cap, f"a{idx}c{cap}")
            jobs.append((idx, cap, J))
    results = []
    for i in range(0, len(jobs), 600):
        chunk = jobs[i:i + 600]
        results += run_tables([j[2] for j in chunk])
    stats = Counter()
    bycat = {}
    viol = []
    pi_bins = Counter()
    pi_vals_gt = []
    for (idx, cap, J), R in zip(jobs, results):
        fam, I, A = uniq[idx]
        gt = bool(A["pi0_gt_half"])
        cat = "pi0>1/2" if gt else "pi0<=1/2"
        key = (cat, cap)
        d = bycat.setdefault(key, Counter())
        d["runs"] += 1
        okS = (R["S"] == A["Rlist"])
        okL = (R["lg0"] == float(Fraction(A["fmax"], A["sc"])))
        okT = (R["ties"] == 1)
        okTr = (R["truncated"] == (1 if cap <= 1 else 0))
        d["S==R"] += okS
        d["lg0==max f"] += okL
        d["ties==1"] += okT
        d["trunc as predicted ([N>=cap])"] += okTr
        d["truncated=1"] += R["truncated"]
        d["truncated=0"] += 1 - R["truncated"]
        if not (okS and okL and okT and okTr):
            viol.append((fam, idx, cap, R, A["Rlist"], J))
    for idx, (fam, I, A) in enumerate(uniq):
        if A["pi0_gt_half"]:
            pi_vals_gt.append(A["pi0"])
    famcat = Counter((fam, bool(A["pi0_gt_half"])) for fam, I, A in uniq)
    rep("A", "")
    rep("A", "(A) Lemma UM, exact arithmetic (integer tables |v|<=1000, <=13 terms/sum => all sums exact in binary64)")
    rep("A", f"  instances with unique exact maximiser R: {len(uniq)}   (x3 caps = {len(jobs)} harness runs)")
    rep("A", f"  by family and pi0(R)>1/2: " + ", ".join(f"{k[0]}:{'gt' if k[1] else 'le'}={v}" for k, v in sorted(famcat.items())))
    n_gt = sum(1 for _, _, A in uniq if A["pi0_gt_half"])
    rep("A", f"  unique-max instances with pi0(R) > 1/2: {n_gt};  with pi0(R) <= 1/2: {len(uniq) - n_gt}")
    if pi_vals_gt:
        q = np.quantile(pi_vals_gt, [0, 0.05, 0.25, 0.5, 0.75, 1])
        rep("A", "  pi0(R) over the pi0>1/2 group: min/5%/25%/50%/75%/max = " + " / ".join(f"{x:.6f}" for x in q))
        rep("A", "  pi0(R) in (0.5,0.6]: %d, (0.6,0.8]: %d, (0.8,0.99]: %d, >0.99: %d" % (
            sum(0.5 < x <= 0.6 for x in pi_vals_gt), sum(0.6 < x <= 0.8 for x in pi_vals_gt),
            sum(0.8 < x <= 0.99 for x in pi_vals_gt), sum(x > 0.99 for x in pi_vals_gt)))
    rep("A", "")
    rep("A", "  category        cap      runs   S==R   lg0==max f   ties==1   truncated=1   truncated=0   trunc==[N>=cap]")
    for key in sorted(bycat, key=lambda k: (k[0] != "pi0>1/2", k[1])):
        d = bycat[key]
        rep("A", f"  {key[0]:<14} {key[1]:>8} {d['runs']:>6} {d['S==R']:>6} {d['lg0==max f']:>10} {d['ties==1']:>9} "
                 f"{d['truncated=1']:>12} {d['truncated=0']:>13} {d['trunc as predicted ([N>=cap])']:>13}")
    N1gt = sum(1 for (idx, cap, J), R in zip(jobs, results) if uniq[idx][2]["pi0_gt_half"] and cap == 10**6 and R["ties"] == 1)
    rep("A", f"  among instances with pi0(R)>1/2: N==1 (code ties==1 at cap 1e6) in {N1gt}/{n_gt} "
             f"({100.0 * N1gt / max(n_gt, 1):.1f}%)")
    rep("A", f"  VIOLATIONS (any of S!=R, lg0!=max f, ties!=1, truncated != [1>=cap]): {len(viol)}")
    for v in viol[:20]:
        fam, idx, cap, R, Rl, J = v
        msg = f"  !! A violation fam={fam} idx={idx} cap={cap} code={R} exactR={Rl}\n     inst p={J.p} K={J.K} blocks={J.blocks} lam={J.lam} rho={J.rho}"
        rep("A", msg)
        CONTRA.append(msg)
    return len(viol)


# ----------------------------------------------------------------------------------------------------------
# (B)
def rand_val(rng):
    e = int(rng.integers(0, 45))
    return float(rng.choice([-1.0, 1.0])) * math.ldexp(1.0 + float(rng.random()), e)


def make_B(rng):
    p = int(rng.choice([3, 4, 5, 6, 7, 8, 9, 10, 12], p=[0.08, 0.12, 0.14, 0.16, 0.14, 0.12, 0.1, 0.08, 0.06]))
    blocks = rand_blocks(rng, p, 5)
    K = int(rng.integers(1, p + 1))
    lam = [rand_val(rng) for _ in range(K + 1)]
    rho = [{c: rand_val(rng) for c in range(1, 1 << len(C)) if popc(c) <= K} for C in blocks]
    return Inst(p, K, blocks, lam, rho, 10**6, "b")


def adjust(I, T, rng, maxit=12):
    """Move one stored double at a time so that margin Delta of the f-hat maximiser is ~ T (target, a Fraction)."""
    pos = {}
    for b, C in enumerate(I.blocks):
        for i, x in enumerate(C):
            pos[x] = (b, i)

    def codes_of(mask):
        c = {}
        for x in mask_list(mask, I.p):
            b, i = pos[x]
            c[b] = c.get(b, 0) | (1 << i)
        return c

    A = analyze(I, want_g=False)
    for it in range(maxit):
        if A["N"] != 1 or A["delta"] is None:
            return A
        err = A["delta"] - T
        if abs(err) <= T / 2000 or err == 0:
            return A
        cR, c2 = codes_of(A["Rmask"]), codes_of(A["S2mask"])
        cands = []  # (kind, b/ k, code, side)
        for b in range(len(I.blocks)):
            rb, sb = cR.get(b, 0), c2.get(b, 0)
            if rb != sb:
                if rb:
                    cands.append(("rho", b, rb, "R"))
                if sb:
                    cands.append(("rho", b, sb, "S2"))
        kR, k2 = popc(A["Rmask"]), popc(A["S2mask"])
        if kR != k2:
            cands.append(("lam", kR, 0, "R"))
            cands.append(("lam", k2, 0, "S2"))
        if not cands:
            return A
        best = None
        for kind, a, c, side in cands:
            cur = I.lam[a] if kind == "lam" else I.rho[a][c]
            want = Fraction(cur) - err if side == "R" else Fraction(cur) + err
            new = float(want)
            if not math.isfinite(new):
                continue
            shift = Fraction(new) - Fraction(cur)
            achieved = A["delta"] + (shift if side == "R" else -shift)
            res = abs(achieved - T)
            key = (res, float(rng.random()))
            if best is None or key < best[0]:
                best = (key, kind, a, c, new)
        if best is None:
            return A
        _, kind, a, c, new = best
        if kind == "lam":
            I.lam[a] = new
        else:
            I.rho[a][c] = new
        A = analyze(I, want_g=False)
    return A


def part_B():
    rng = np.random.default_rng(SEED_B)
    NINST = 2600
    insts, meta = [], []
    t = time.time()
    eps_mults = [0.05, 0.25, 0.5, 1.0, 1.5, 1.9, 2.05, 2.5, 3.0, 5.0, 10.0, 100.0]
    ulp_mults = [1, 2, 4, 8, 16, 64]
    tie_excl = 0
    for n in range(NINST):
        I = make_B(rng)
        mode = rng.choice(["natural", "eps", "eps", "eps", "eps", "ulp", "ulp"])
        A = analyze(I, want_g=False)
        if mode != "natural" and A["N"] == 1 and A["delta"] is not None:
            if mode == "eps":
                c = float(rng.choice(eps_mults))
                T = A["eps"] * Fraction(c)
                tag = f"eps*{c}"
            else:
                k = int(rng.choice(ulp_mults))
                fR = float(Fraction(A["fmax"], A["sc"]))
                u = math.ulp(fR) if fR != 0 else 2.0**-52
                T = Fraction(u) * k
                tag = f"ulp*{k}"
            A = adjust(I, T, rng)
        else:
            tag = "natural"
        A = analyze(I)  # final analysis with g-hat
        meta.append((tag, A))
        insts.append(I)
    rep("B", f"[B] generated {NINST} instances in {time.time() - t:.1f}s")
    # harness runs (cap 1e6, default)
    for i, I in enumerate(insts):
        I.cap = 10**6
        I.iid = f"b{i}"
    results = []
    for i in range(0, len(insts), 500):
        results += run_tables(insts[i:i + 500])
    # evaluation
    bins = [("<0.5", 0, 0.5), ("0.5-1", 0.5, 1), ("1-2", 1, 2), ("2-3 (>2: lemma applies)", 2, 3), ("3-10", 3, 10), (">=10", 10, 1e300)]
    tab = {b[0]: Counter() for b in bins}
    tie_f = 0
    viol, e_bad, g_bad, fold_bad = [], [], [], []
    rng2 = np.random.default_rng(SEED_B + 1)
    mingap_lemma = None
    for I, (tag, A), R in zip(insts, meta, results):
        valid = A["valid"]
        # clause (e) check (native): g-hat(code S) == lg0 == max g-hat
        mask = sum(1 << x for x in R["S"])
        pos = int(np.searchsorted(valid, mask))
        okpos = pos < len(valid) and valid[pos] == mask
        gmax = float(A["g"].max())
        e_ok = okpos and R["lg0"] == gmax and float(A["g"][pos]) == R["lg0"]
        if not e_ok:
            e_bad.append((I.iid, R))
        # unique g-hat maximiser must equal code S
        gm_idx = np.nonzero(A["g"] == gmax)[0]
        if len(gm_idx) == 1 and (not okpos or pos != gm_idx[0]):
            g_bad.append((I.iid, R))
        # fold bound check on a sample of sets
        n_v = len(valid)
        sample = range(n_v) if n_v <= 600 else rng2.choice(n_v, 600, replace=False).tolist()
        sc = A["sc"]
        for i in sample:
            gi = Fraction(float(A["g"][i]))
            err = abs(gi - Fraction(A["fl"][i], sc))
            m = int(A["mmv"][i])
            bound = Fraction(m * A["ab"][i], (U53 - m) * sc)
            if err > bound:
                fold_bad.append((I.iid, i, err, bound))
        if A["N"] != 1:
            tie_f += 1
            continue
        if A["delta"] is None:
            continue
        okS = (R["S"] == A["Rlist"])
        ratio = float(A["delta"] / A["eps"]) if A["eps"] > 0 else float("inf")
        for name, lo, hi in bins:
            if lo <= ratio < hi:
                d = tab[name]
                d["n"] += 1
                d["S==R"] += okS
                d["S!=R"] += (not okS)
                break
        if A["delta"] > 2 * A["eps"] and not okS:
            viol.append((I, A, R))
    nused = sum(tab[b[0]]["n"] for b in bins)
    rep("B", "")
    rep("B", "(B) Lemma UM-FP, binary64 random double tables (|v| spread over 1..2^45, signs random), eta = 0 (stored doubles = truth)")
    rep("B", f"  instances: {NINST}; f-hat has non-unique maximiser (excluded from the margin table): {tie_f}; used: {nused}")
    rep("B", "  construction: 'natural' random tables, or one stored double moved (<=12 steps) so that margin Delta ~ c*eps (c in "
             + str(eps_mults) + ") or ~ k ulps of |f-hat(R)| (k in " + str(ulp_mults) + ")")
    rep("B", "  Delta = f-hat(R) - max_{S!=R} f-hat(S) (exact),  eps = max_S gamma_{m(S)} (|lam-hat|+sum|rho-hat|) (exact, u=2^-53)")
    rep("B", "")
    rep("B", "  Delta/eps bin              runs   code S==R   code S!=R")
    for name, lo, hi in bins:
        d = tab[name]
        rep("B", f"  {name:<26} {d['n']:>5} {d['S==R']:>11} {d['S!=R']:>11}")
    n_gt2 = sum(tab[b[0]]["n"] for b in bins if b[1] >= 2)
    rep("B", f"  runs with Delta > 2 eps: {n_gt2};  VIOLATIONS (Delta>2eps and code S != R): {len(viol)}")
    n_le2 = sum(tab[b[0]]["n"] for b in bins if b[1] < 2)
    f_le2 = sum(tab[b[0]]["S!=R"] for b in bins if b[1] < 2)
    rep("B", f"  runs with Delta <= 2 eps: {n_le2};  of which code S != R: {f_le2} ({100.0 * f_le2 / max(n_le2, 1):.1f}%)  "
             f"(non-vacuous: failures occur there; allowed by the lemma)")
    # finer band right above 2 eps
    band = [(I, A, R) for I, (tag, A), R in zip(insts, meta, results) if A["N"] == 1 and A["delta"] is not None and A["eps"] > 0
            and 2 < float(A["delta"] / A["eps"]) <= 2.5]
    rep("B", f"  runs with 2 < Delta/eps <= 2.5 (just above the threshold): {len(band)}, code S==R in {sum(R['S'] == A['Rlist'] for I, A, R in band)}")
    # how far the observed worst-case rounding comes to eps: report max over (sampled) sets |g-f|/eps
    rep("B", f"  sanity (clause (e), native binary64): g-hat(code S) == lg0 == max g-hat failed in {len(e_bad)}/{NINST} runs; "
             f"unique g-hat maximiser != code S in {len(g_bad)} runs")
    rep("B", f"  sanity (fold bound |g-hat(S)-f-hat(S)| <= gamma_m sum|terms|, up to 600 sampled sets/instance): violations {len(fold_bad)}")
    for x in viol[:10]:
        I, A, R = x
        msg = (f"  !! B COUNTEREXAMPLE to Lemma UM-FP: id={I.iid} p={I.p} K={I.K} blocks={I.blocks}\n     lam={[float.hex(v) for v in I.lam]}\n"
               f"     rho={[{c: float.hex(v) for c, v in d.items()} for d in I.rho]}\n"
               f"     exact R={A['Rlist']} code S={R['S']} Delta={float(A['delta'])!r} eps={float(A['eps'])!r} ratio={float(A['delta'] / A['eps'])!r}")
        rep("B", msg)
        CONTRA.append(msg)
    for x in e_bad[:5]:
        msg = f"  !! B clause (e) sanity failed: {x}"
        rep("B", msg)
        CONTRA.append(msg)
    for x in fold_bad[:5]:
        msg = f"  !! B fold-bound sanity violated: {x}"
        rep("B", msg)
        CONTRA.append(msg)
    return len(viol) + len(e_bad) + len(fold_bad)


# ----------------------------------------------------------------------------------------------------------
# (C)
def standardise(v):
    n = len(v)
    mu = math.fsum(v) / n
    c = [x - mu for x in v]
    ss = math.sqrt(math.fsum(x * x for x in c) / (n - 1))
    return [x / ss for x in c]


def make_C(n, s):
    rng = np.random.default_rng([20261111, n, s])
    while True:
        ng, g = int(rng.integers(2, 5)), int(rng.integers(3, 5))
        if ng * g <= 12:
            break
    p = ng * g
    cols = []
    rws = []
    for gi in range(ng):
        rw = float(rng.uniform(0.4, 0.7))
        rws.append(rw)
        z = rng.standard_normal(n)
        for j in range(g):
            e = rng.standard_normal(n)
            cols.append((math.sqrt(rw) * z + math.sqrt(1 - rw) * e).tolist())
    nz = int(rng.integers(1, 4))
    support = rng.permutation(p)[:nz].tolist()
    beta = np.zeros(p)
    for j in support:
        beta[j] = float(rng.choice([-1.0, 1.0])) * float(rng.uniform(0.4, 1.2))
    cols = [standardise(c) for c in cols]
    Xm = np.array(cols).T  # n x p
    y = (Xm @ beta + rng.standard_normal(n)).tolist()
    y = standardise(y)
    X = [v for c in cols for v in c]
    desc = f"p={p} groups={ng}x{g} rho_w={[round(r, 2) for r in rws]} support={sorted(support)} beta={[round(beta[j], 2) for j in sorted(support)]}"
    return (f"c-{n}-{s}", n, p, 4, 10**6, X, y), desc


def part_C():
    cases, descs, keys = [], [], []
    for n in (50, 200, 800):
        for s in range(20):
            c, d = make_C(n, s)
            cases.append(c)
            descs.append(d)
            keys.append((n, s))
    t = time.time()
    out = run_data(cases)
    rep("C", f"[C] harness DATA runs: {len(out)} in {time.time() - t:.1f}s")
    rows = []
    viol = []
    for (I, R), key, d in zip(out, keys, descs):
        A = analyze(I, want_pi=True)
        n, s = key
        row = dict(n=n, s=s, desc=d, p=I.p, K=I.K, J=len(I.blocks), N=A["N"])
        row["Rlist"] = A["Rlist"]
        row["S"] = R["S"]
        row["ties"] = R["ties"]
        row["trunc"] = R["truncated"]
        row["eq"] = (R["S"] == A["Rlist"])
        row["pi0"] = A.get("pi0")
        row["gt"] = A.get("pi0_gt_half", False)
        row["Lam"] = A["Lam"]
        row["That"] = A["That"]
        row["eps"] = A["eps"]
        row["delta"] = A["delta"]
        row["ratio"] = float(A["delta"] / (2 * A["eps"])) if (A["delta"] is not None and A["eps"] > 0) else None
        mmax = min(row["J"], I.K)
        g_ = Fraction(I.K, U53 - I.K)
        row["eps_crude"] = float(g_ * (Fraction(A["Lam"]) + I.K * Fraction(A["That"])))
        row["eps_f"] = float(A["eps"])
        # (e)
        mask = sum(1 << x for x in R["S"])
        pos = int(np.searchsorted(A["valid"], mask))
        row["e_ok"] = bool(pos < len(A["valid"]) and A["valid"][pos] == mask and R["lg0"] == float(A["g"].max()) and float(A["g"][pos]) == R["lg0"])
        rows.append(row)
        if row["gt"] and not row["eq"]:
            viol.append(row)
    rep("C", "")
    rep("C", "(C) DATA mode (frozen scorer + real prior), LH-like designs: groups of equicorrelated columns (within corr 0.4-0.7), sparse beta, B=4")
    rep("C", "    p<=12 (K=min(p,n/2)=p), full enumeration of Omega_K; f-hat = exact sum of the code's own doubles; scorer error eta NOT assessed (out of scope)")
    rep("C", "")
    rep("C", " n    s  p  K  J  N  pi0(R)      ties trunc S==R  Lam-hat    T-hat       eps          Delta        Delta/(2eps)   eps<=crude  (e)")
    for r in rows:
        rep("C", f" {r['n']:<4} {r['s']:<2} {r['p']:<2} {r['K']:<2} {r['J']:<2} {r['N']:<2} "
                 f"{(r['pi0'] if r['pi0'] is not None else float('nan')):<12.9f} {r['ties']:<4} {r['trunc']:<5} {str(r['eq']):<5} "
                 f"{r['Lam']:<10.4g} {r['That']:<11.4g} {r['eps_f']:<12.4e} {(float(r['delta']) if r['delta'] is not None else float('nan')):<12.5g} "
                 f"{(r['ratio'] if r['ratio'] is not None else float('nan')):<14.5g} {str(r['eps_f'] <= r['eps_crude']):<10} {r['e_ok']}")
    rep("C", "")
    gt = [r for r in rows if r["gt"] and r["N"] == 1]
    rep("C", f"  runs: {len(rows)}; N (exact maximisers of f-hat) != 1: {sum(r['N'] != 1 for r in rows)}; "
             f"truncated==1: {sum(r['trunc'] for r in rows)}; clause (e) native check failed: {sum(not r['e_ok'] for r in rows)}")
    rep("C", f"  runs with pi0(R) > 1/2: {len(gt)};  code S == R in {sum(r['eq'] for r in gt)}/{len(gt)}  (all runs: S==R in {sum(r['eq'] for r in rows)}/{len(rows)})")
    for n in (50, 200, 800):
        g_n = [r for r in rows if r["n"] == n]
        gg = [r for r in g_n if r["gt"] and r["N"] == 1]
        rat = sorted(r["ratio"] for r in gg if r["ratio"] is not None)
        if rat:
            rep("C", f"  n={n}: runs {len(g_n)}, pi0>1/2: {len(gg)}, S==R {sum(r['eq'] for r in gg)}/{len(gg)}; Delta/(2eps) min/median/max = "
                     f"{rat[0]:.4g} / {rat[len(rat) // 2]:.4g} / {rat[-1]:.4g}")
        else:
            rep("C", f"  n={n}: runs {len(g_n)}, pi0>1/2: {len(gg)}")
        nogt = [r for r in g_n if not r["gt"]]
        if nogt:
            rep("C", f"        pi0<=1/2 runs: {len(nogt)}, S==R {sum(r['eq'] for r in nogt)}/{len(nogt)}")
    allrat = sorted(r["ratio"] for r in gt if r["ratio"] is not None)
    if allrat:
        rep("C", f"  ALL pi0>1/2 runs: Delta/(2eps) min/median/max = {allrat[0]:.6g} / {allrat[len(allrat) // 2]:.6g} / {allrat[-1]:.6g}; "
                 f"runs with ratio <= 1 (lemma condition would fail at eta=0): {sum(x <= 1 for x in allrat)}")
    rep("C", f"  eps (exact lemma definition) over all runs: min/max = {min(r['eps_f'] for r in rows):.3e} / {max(r['eps_f'] for r in rows):.3e}; "
             f"crude bound gamma_K(Lam+K T) >= exact eps in {sum(r['eps_f'] <= r['eps_crude'] for r in rows)}/{len(rows)}")
    rep("C", f"  Lam-hat range {min(r['Lam'] for r in rows):.4g}..{max(r['Lam'] for r in rows):.4g};  T-hat range {min(r['That'] for r in rows):.4g}..{max(r['That'] for r in rows):.4g}")
    rep("C", "  NOT assessed: the scorer's table error eta (|f-hat - f*|); eta is out of scope here, so the lemma's FP-TAB premise is untested.")
    for r in viol:
        msg = f"  !! C: pi0(R)>1/2 but code S != R: n={r['n']} s={r['s']} {r['desc']} R={r['Rlist']} code={r['S']} pi0={r['pi0']} ratio={r['ratio']}"
        rep("C", msg)
        CONTRA.append(msg)
    return len(viol)


# ----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    nA = part_A()
    nB = part_B()
    nC = part_C()
    head = []
    head.append("item1_um_checks_out.txt -- numerical checks of Lemma UM and Lemma UM-FP (I1_e4_replacement.md) against the frozen start_mode")
    head.append(f"script: item1_um_checks.py   python: {sys.version.split()[0]}  numpy {np.__version__}  mpmath {mp.__version__}   total time {time.time() - T0:.1f}s")
    head.append("harness: Theory_work/Wave1/W1-N3/numerics/sm_harness.exe (existing, ran as is; not rebuilt) driving v2_2_1 v3_start.h:183-240")
    head.append(f"seeds: A={SEED_A} (numpy default_rng); B={SEED_B} (+1 for sampling); C=default_rng([20261111, n, s]), n in {{50,200,800}}, s=0..19")
    head.append("")
    head.append("CONTRADICTIONS WITH THE LEMMAS: " + ("NONE (A: %d violations, B: %d, C: %d)" % (nA, nB, nC) if not CONTRA else "%d FOUND — details below and in sections" % len(CONTRA)))
    for m in CONTRA:
        head.append(m)
    head.append("")
    text = "\n".join(head + REPORT["A"] + [""] + REPORT["B"] + [""] + REPORT["C"]) + "\n"
    with open(os.path.join(HERE, "item1_um_checks_out.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    print("written", os.path.join(HERE, "item1_um_checks_out.txt"))

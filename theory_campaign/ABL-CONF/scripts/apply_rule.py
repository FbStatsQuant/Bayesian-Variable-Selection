"""apply_rule.py -- ABL-CONF pre-registered decision rules (PREREG.md section 7). Do not edit after launch.

Usage: python3 apply_rule.py <per_fit.csv> <reference.csv> <out_prefix> [--favourable S1]
Writes <out_prefix>_designs.csv (one row per design and claim) and <out_prefix>_verdict.txt; prints the verdict.

Inputs (columns used): per_fit: design, scen, role, arm, k, status, wall_s, log_Z, err_logZ, pip_zw_max
                       reference: design, scen, K, log_Zref, se_ref, KB, log_ZrefB, se_refB
Only role == "test" rows enter the tests. A fit is DELIVERED iff status == "completed" (process finished within the
cap, fit status "completed", finite log Zhat); every other terminal status (capped, failed, fit_*) is a delivery
failure. A pair is (design, k).

Constants: ALPHA = 0.05 (one-sided sign tests and one-sided distribution-free confidence bounds for a median;
two-sided bounds use ALPHA/2 per side), DZ = 0.5 nat, DP = 0.05, NMIN = 6 delivered pairs, KMIN = 6 reference fits,
GUARD_SLACK = 0.25 nat.

Claim 1 (cost; A vs B), per design:
  cost:  cost = process wall seconds; a delivery failure has cost +inf. Pairs where both failed, and exact ties, drop.
         p_A = P(Bin(n, 1/2) >= #{cost_A < cost_B}),  p_B = P(Bin(n, 1/2) >= #{cost_B < cost_A}).
         cost_holds iff p_A <= ALPHA;  cost_rev iff p_B <= ALPHA.
  accuracy on the n_a pairs where A and B both delivered (testable iff n_a >= NMIN):
         dZ = |err_A| - |err_B|,  dP = pipzw_A - pipzw_B,  h = log Zhat_A - log Zhat_B  (head to head).
         acc_holds iff UCB(dZ) <= DZ and UCB(dP) <= DP and [LCB2(h), UCB2(h)] inside [-DZ, DZ].
         acc_rev   iff LCB(dZ) > DZ or LCB(dP) > DP.
  verdict: refuted        if cost_rev or acc_rev;
           holds          if cost_holds and acc_holds;
           holds_nondeliv if cost_holds, accuracy not testable, and #{A delivered, B not} >= 5;
           inconclusive   otherwise (also when the design's reference has K < KMIN).
  overall: REFUSED if any design refuted; LICENSED if every design is holds/holds_nondeliv, >= 2 designs are
           'holds' (accuracy actually tested), the guard passed and no fit is pending; else INCONCLUSIVE.

Claim 2 (accuracy; A vs C), per design, on the n_a pairs where A and C both delivered (testable iff n_a >= NMIN):
         dC = err_C = log Zhat_C - log Z_ref,  hC = log Zhat_C - log Zhat_A,  dE = |err_C| - |err_A|.
         under iff UCB(dC) < -2 se_ref and UCB(hC) < 0;  less iff LCB(dE) > 0.
  verdict: refuted if testable and (UCB(dE) < 0 or LCB(hC) > 0 or LCB(dC) > 2 se_ref);
           holds if testable and under and less;  inconclusive otherwise (also K < KMIN).
  overall: REFUSED if any design refuted; LICENSED if every design holds, the guard passed, no fit pending;
           else INCONCLUSIVE.

Guard (reference not favouring arm A): on the favourable design, the reserved arm-B pool (KB >= 3 delivered) must agree
with the arm-A reference: |log Z_ref - log Z_refB| <= GUARD_SLACK + 2 sqrt(se_ref^2 + se_refB^2). If it fails or is
unavailable, neither claim can be LICENSED (it can still be REFUSED or INCONCLUSIVE). The head-to-head conditions above
(h, hC) are a second guard that does not use the reference.

UCB/LCB: distribution-free (sign-test inversion) one-sided bounds for the median at level 1 - ALPHA; UCB2/LCB2 the
same at 1 - ALPHA/2. UCB(x) = x_(u), u = min{u : P(Bin(n,1/2) <= u-1) >= 1-ALPHA} (+inf if no such u); LCB(x) = -UCB(-x).
"""
import csv, sys, math

ALPHA, DZ, DP, NMIN, KMIN, GUARD_SLACK = 0.05, 0.5, 0.05, 6, 6, 0.25
INF = float("inf")

def fnum(x):
    try: return float(x)
    except (TypeError, ValueError): return float("nan")

def binom_cdf(m, n):  # P(Bin(n,1/2) <= m)
    return sum(math.comb(n, i) for i in range(0, m + 1)) / 2 ** n if m >= 0 else 0.0

def ucb(x, alpha=ALPHA):
    x = sorted(x); n = len(x)
    for u in range(1, n + 1):
        if binom_cdf(u - 1, n) >= 1 - alpha: return x[u - 1]
    return INF

def lcb(x, alpha=ALPHA): return -ucb([-v for v in x], alpha)

def sign_p(wins, n): return 1 - binom_cdf(wins - 1, n) if n > 0 else 1.0

def fmt(v):
    if isinstance(v, float):
        return "inf" if v == INF else ("-inf" if v == -INF else ("NA" if math.isnan(v) else f"{v:.4g}"))
    return str(v)

def run(per_fit, reference, out_prefix, favourable="S1"):
    rows = list(csv.DictReader(open(per_fit)))
    ref = {r["design"]: r for r in csv.DictReader(open(reference))}
    pending = sum(r["status"] == "pending" for r in rows)
    test = [r for r in rows if r["role"] == "test"]
    D = {}
    for r in test: D.setdefault(r["design"], {}).setdefault(int(r["k"]), {})[r["arm"]] = r
    dl = lambda r: r is not None and r["status"] == "completed"
    # guard
    fav = [d for d in ref if ref[d]["scen"] == favourable]
    guard = {"design": fav[0] if fav else None, "status": "unavailable"}
    if fav:
        g = ref[fav[0]]; KA, KB = int(fnum(g["K"]) or 0), int(fnum(g["KB"]) or 0)
        if KA >= KMIN and KB >= 3 and not math.isnan(fnum(g["log_ZrefB"])):
            diff = fnum(g["log_Zref"]) - fnum(g["log_ZrefB"])
            tol = GUARD_SLACK + 2 * math.sqrt(fnum(g["se_ref"]) ** 2 + fnum(g["se_refB"]) ** 2)
            guard.update(status="pass" if abs(diff) <= tol else "fail", diff=diff, tol=tol)
    out = []
    for d in sorted(D):
        P = D[d]; R = ref.get(d, {}); K = int(fnum(R.get("K", 0)) or 0); se = fnum(R.get("se_ref"))
        ref_ok = K >= KMIN
        # ---- Claim 1
        c = {"claim": 1, "design": d, "scen": R.get("scen", ""), "ref_K": K, "se_ref": se}
        wa = wb = n = 0; nd_b_only = nd_a = nd_b = 0; acc = []
        for k, a in sorted(P.items()):
            A, B = a.get("A"), a.get("B")
            if A is None or B is None: continue
            ca = fnum(A["wall_s"]) if dl(A) else INF; cb = fnum(B["wall_s"]) if dl(B) else INF
            nd_a += not dl(A); nd_b += not dl(B); nd_b_only += dl(A) and not dl(B)
            if not (ca == INF and cb == INF) and ca != cb:
                n += 1; wa += ca < cb; wb += cb < ca
            if dl(A) and dl(B): acc.append((A, B))
        pA, pB = sign_p(wa, n), sign_p(wb, n)
        c.update(n_cost=n, wins_A=wa, wins_B=wb, p_A=pA, p_B=pB, nondeliv_A=nd_a, nondeliv_B=nd_b,
                 nondeliv_B_only=nd_b_only, n_acc=len(acc))
        cost_holds, cost_rev = pA <= ALPHA, pB <= ALPHA
        testable = len(acc) >= NMIN and ref_ok
        acc_holds = acc_rev = False
        if testable:
            dZ = [abs(fnum(A["err_logZ"])) - abs(fnum(B["err_logZ"])) for A, B in acc]
            dPp = [fnum(A["pip_zw_max"]) - fnum(B["pip_zw_max"]) for A, B in acc]
            h = [fnum(A["log_Z"]) - fnum(B["log_Z"]) for A, B in acc]
            c.update(med_dZ=sorted(dZ)[len(dZ) // 2], UCB_dZ=ucb(dZ), LCB_dZ=lcb(dZ), UCB_dP=ucb(dPp), LCB_dP=lcb(dPp),
                     LCB2_h=lcb(h, ALPHA / 2), UCB2_h=ucb(h, ALPHA / 2))
            acc_holds = c["UCB_dZ"] <= DZ and c["UCB_dP"] <= DP and c["LCB2_h"] >= -DZ and c["UCB2_h"] <= DZ
            acc_rev = c["LCB_dZ"] > DZ or c["LCB_dP"] > DP
        c.update(cost_holds=cost_holds, cost_rev=cost_rev, acc_testable=testable, acc_holds=acc_holds, acc_rev=acc_rev)
        if cost_rev or acc_rev: v = "refuted"
        elif not ref_ok: v = "inconclusive"
        elif cost_holds and acc_holds: v = "holds"
        elif cost_holds and not testable and nd_b_only >= 5: v = "holds_nondeliv"
        else: v = "inconclusive"
        c["verdict"] = v; out.append(c)
        # ---- Claim 2
        c = {"claim": 2, "design": d, "scen": R.get("scen", ""), "ref_K": K, "se_ref": se}
        pr = [(a["A"], a["C"]) for k, a in sorted(P.items()) if dl(a.get("A")) and dl(a.get("C"))]
        c.update(n_acc=len(pr), nondeliv_A=sum(not dl(a.get("A")) for a in P.values()),
                 nondeliv_C=sum(not dl(a.get("C")) for a in P.values()))
        testable = len(pr) >= NMIN and ref_ok
        v = "inconclusive"
        if testable:
            dC = [fnum(C["err_logZ"]) for A, C in pr]; hC = [fnum(C["log_Z"]) - fnum(A["log_Z"]) for A, C in pr]
            dE = [abs(fnum(C["err_logZ"])) - abs(fnum(A["err_logZ"])) for A, C in pr]
            c.update(med_errC=sorted(dC)[len(dC) // 2], UCB_dC=ucb(dC), LCB_dC=lcb(dC), UCB_hC=ucb(hC), LCB_hC=lcb(hC),
                     LCB_dE=lcb(dE), UCB_dE=ucb(dE), n_C_below_A=sum(x < 0 for x in hC))
            under = c["UCB_dC"] < -2 * se and c["UCB_hC"] < 0; less = c["LCB_dE"] > 0
            c.update(under=under, less=less)
            if c["UCB_dE"] < 0 or c["LCB_hC"] > 0 or c["LCB_dC"] > 2 * se: v = "refuted"
            elif under and less: v = "holds"
        c.update(acc_testable=testable, verdict=v); out.append(c)
    # overall
    lines = [f"ABL-CONF rule  (ALPHA={ALPHA}, DZ={DZ}, DP={DP}, NMIN={NMIN}, KMIN={KMIN}, GUARD_SLACK={GUARD_SLACK})",
             f"input: {per_fit}", f"designs: {len(D)}   pending fits: {pending}",
             "guard (" + str(guard["design"]) + "): " + guard["status"] +
             (f"  |refA - refB| = {abs(guard['diff']):.3f} vs tol {guard['tol']:.3f}" if "diff" in guard else "")]
    verdicts = {}
    for cl in (1, 2):
        vs = [r["verdict"] for r in out if r["claim"] == cl]
        if not vs: V = "INCONCLUSIVE"
        elif "refuted" in vs: V = "REFUSED"
        elif cl == 1 and all(v in ("holds", "holds_nondeliv") for v in vs) and vs.count("holds") >= 2 \
                and guard["status"] == "pass" and pending == 0: V = "LICENSED"
        elif cl == 2 and all(v == "holds" for v in vs) and guard["status"] == "pass" and pending == 0: V = "LICENSED"
        else: V = "INCONCLUSIVE"
        verdicts[cl] = V
        lines.append(f"Claim {cl}: {V}   per design: " + ", ".join(f"{r['design']}={r['verdict']}" for r in out if r["claim"] == cl))
    if pending: lines.append("NOTE: fits still pending -- this is an interim reading, not the pre-registered result.")
    keys = []
    for r in out:
        for k in r:
            if k not in keys: keys.append(k)
    with open(out_prefix + "_designs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for r in out: w.writerow({k: fmt(v) for k, v in r.items()})
    open(out_prefix + "_verdict.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return verdicts

if __name__ == "__main__":
    a = sys.argv[1:]; fav = "S1"
    if "--favourable" in a: i = a.index("--favourable"); fav = a[i + 1]; del a[i:i + 2]
    run(a[0], a[1], a[2], fav)

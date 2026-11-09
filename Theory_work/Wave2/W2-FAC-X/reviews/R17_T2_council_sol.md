# R17 — Target-2 Council seat: independent final quality gate

**Verdict: ACCEPT the locked `STATEMENT_T2.md` v2.1 and its proofs. Score: 9.2/10. All six gates PASS. REQUIRED fixes: none.**

Scope: Theorem FAC-GL, models (G) and (R), claims (G1)–(G4), and the **iid-only** Corollary FAC-NCS. This is one independent Council seat, not a declaration that both seats have passed. All conclusions are interpreted asymptotically. No objection concerns the size of an onset.

Paths below are relative to `Theory_work/Wave2/W2-FAC-X/` unless explicitly prefixed. I read the locked statement, `T2/STATEMENT_T2.md` §§1–3, `T2/L4r_path.md` §§L4r.0–L4r.3, X7–X10, the reused portions of X1–X6 and FAC-B L1–L5, and the specified posterior, random-design, correlation-tail, delivery, implementation and protocol sources. I also checked R10–R12, R15–R16 and their dispositions against the current files. The unproved extensions and obstruction discussion in L4r.4–L4r.6 are not inputs to the accepted theorem.

## Six gates

| Gate | Verdict | Reason |
|---|---|---|
| **G1 — correctness of every step** | **PASS** | The exact-Gram Schur/rank-one formulas, weighted-residual identity, top-square centre bound, prior cancellation and move comparisons close. X9 transfers these uniformly using a full-matrix perturbation bound and the correctly normalised statistic. X7 reruns the approximate-argmin/soft-gap proof at its enlarged scale; it does not presume preservation of an exact deletion order. X8 and X10 supply the start and assembly implications. Details below. |
| **G2 — hypotheses used equal hypotheses stated** | **PASS** | The coefficient convention differs correctly between fixed standardised coefficients in (G) and fixed raw coefficients in (R). (FS-G) is sign-corrected, population-level and uniformly bounded away from zero. A fixed A₁ is selected strictly below A_S. FAC-NCS explicitly replaces (P-S)/(FS-G) by (P-½), limiting-CS (FS), and Δ_n H̄_n ≤ n^(−1/3), and is restricted to (R). CAL is inherited for the M5(0) route, while delivery retains all of Proposition F's premises and allocation and is CAL-free. |
| **G3 — no hidden assumptions** | **PASS** | No finite loading alphabet, loading-class proportions, path-only invariant, independence of N₀ from ξ, or simultaneous coupling over loading arrays is required for FAC-GL. Uniformity over sets comes from deterministic inequalities on one event. Raw-design conditioning and common-constant de-randomisation handle random standardisation and partitioning. Bounded p and empty null sets are covered. |
| **G4 — adequate status of cited lemmas** | **PASS** | The proofs retain the recorded author/status qualifications and the actual cross-family verdicts, including the withdrawn (G) branch of X7, conditional assembly check for X10, and implementation/audit premises. The cited upstream results have adequate status for these uses; their qualifications are not upgraded. `CITECHECK.txt` was read, its five path/line checks were independently rerun successfully, and the relevant status strings were checked against sources. |
| **G5 — constants and rates tracked** | **PASS** | Both logarithmic coefficients are strictly positive under A₁ < A_S; their remainders are uniform, including for bounded p. X9 retains all three terms in its error envelope, whose product with H̄ tends to zero. X7's narrowed dispersion rate preserves the spacing, tail-window, band feedback and `p w² + w log n = o(1)` conditions. Path margins are separated from signal-dependent truth losses and start onsets. |
| **G6 — fidelity to the method** | **PASS** | Score, capped BB(1,p) prior, full-response block tables, actual start mode, every feasible flip/swap, strict improvement and production tie rule are retained. MR1 and the final complete scan give the claimed search certification. Delivery retains total tier-1 fallback and amended resource/preflight charges. I checked the merge identity 4676af6 and the current production LS0 loop/cap call against the cited method sources. No algorithm change is needed. |

## Mathematical checks supporting the verdict

**Exact-Gram representation and gains.** In `T2/L4r_path.md:23–74`, `H_U = (n²−1)Σ_UU + I` has the stated diagonal-plus-rank-one factorisation. Whitening gives κ₁² = σ²/[s²(n+1)], the Schur deletion statistic `(1+γ′_j)τ_j²`, the addition factor `1−ℓ′_l²/(D′_T+ℓ′_l²)`, and the exact centre drift. The determinant correction is loading-dependent but bounded by O(1/n). Accordingly the exact argmin claim is only **within a loading value**, as the locked theorem says. The reduced offset retains the truth-noise contribution; the earlier false simplification to η has been removed.

The Gaussian event in L4r.1 uses iid ξ and elementary norm/order-statistic bounds, not compound symmetry. The uniform projection bound `Φ(U) ≤ n/log n` and the full Gram eigenvalue floor control truth residuals for both deletions and swaps. In the RSS-to-Q comparison, `ψ_U < n` is now justified independently by `quad_U ≥ 0`, rather than by the insufficient RSS upper bound. The signal term exceeds the noise bound before squaring the truth-residual lower bound. Removing the possible improvement from the inserted null still leaves an order-n truth loss.

**The two uniform ingredients.** For arbitrary kept nulls K, L4r.2(a) gives exactly

    Σ_K ℓ′_i τ_i = κ′_S X_T + ϱ,   κ′_S = 1 + Σ_{S₀} ℓ′_i² > 0.

If X_T ≥ 0, each residual is at most H̄; positivity of the weights prevents every residual from being too negative. The reversed argument covers X_T < 0. This supplies a good deletion without a path or class-balance hypothesis. Separately, Cauchy–Schwarz and the top-square bound give

    |Σ_K ℓ′_i ζ_i|/D′_T ≤ sqrt(m(Z_m²+2)/Σ_K ℓ′_i²)
                        ≤ sqrt(Z_m²+2)/ℓ′_lo.

Both inequalities apply to every subset on the same event, so no exponentially large union bound is being hidden.

**The exponent and swap comparisons.** L4r.3(i) correctly cancels the leading log p contribution, leaving

    G_del(i;T) ≥ ½ log n − log k − γ_m log(2p) − o(log n).

The split at m = log n gives `d_del = ½ − A₁ max(1,γ̄)`. For additions, retaining the size-prior contribution yields

    G_add(l;T) ≤ −½ log n
                + ½[(H̄ + R′ sqrt(Z_m²+2))² − (Z_m²+2)] + o(log n).

The bracket is increasing in its square-root argument because R′ ≥ 1; `Z_m²+2 ≤ H̄²+O(log log n)` gives `d_add = ½ − A₁((1+R)²−1)`. The m = 0 case is treated separately and is stronger. One valid fixed margin is `c = ½ min(d_del,d_add)`, after enlarging the onset. Since γ̄ < R² and R ≥ 1, the addition constraint indeed determines A_S. Null-out swaps telescope through T minus the removed null, which still contains S₀; the same uniform negative addition bound applies there. Every maximising neighbour is a null deletion, including under ties. The induction therefore covers every permitted start and ends strictly at S₀.

**Iid transfer.** X9.1 uses `κ₀ = N/φ²`, `D_T = ||ℓ_T||²+κ₀` and

    s_j(T) = (ξ_j−ℓ_j X_T)/sqrt(1−ℓ_j²/D_T).

That denominator is essential and has a positive lower bound depending only on the loading endpoints. D3 gives `κ₀ = 1+O(n^(−1/3))`, which preserves γ̄ up to a relative o(1); merely bounding κ₀ between two constants would not suffice for the printed coefficient.

The operator-norm argument in X9.2 applies to all principal sets. For example, with `B = I+R+bbᵀ`, `B₀ = I+bbᵀ` and `c = B₀⁻¹ṽ1`, the identity `B⁻¹ṽ1−c = −B⁻¹Rc` gives the required structure-free bound directly. Together with coordinate and diagonal-normalisation bounds it yields

    δ̄_n ≤ C[p/√n + √(p log n/n) + √(log n/n)] H̄,
    δ̄_n H̄ → 0.

Thus the change in each relevant null square is o(1). The repaired second-order comparison also retains the `√p log n/n` term. X9.3 uses `(|s|+δ̄_n)²`, not the invalid signed upper square. The iid multiplier, determinant, ridge and RSS errors have the asserted orders. Truth moves use the eigenvalue/projection argument separately. There is no import of a band hypothesis into the all-sets proof.

**Near-CS transfer.** In X7, the extra deterministic loading vector and its effect on the noise coordinate add at most `C Δ_n H̄` to the statistic error. The remainder containing r_n retains its logarithmic term. Under the locked condition this addition is at most `C n^(−1/3)` and is absorbed by the fixed enlargement `ϖ′_n = (1+C₇)ϖ_n`, reserving the ordering slack required by X4.1. The CS reference retains its exact drift identity; X3 and the path induction are rerun at this new scale.

Specifically, for `w = O(H̄ sqrt(p log n/n)+n^(−1/3))`,

    p²w → 0 in regime p ≤ n^(1/200);
    w(1+H̄)m₁² exp(CwH̄) → 0 for the tail spacings;
    p w² = O(p² log² n/n + p n^(−2/3)) → 0;
    w log n → 0;
    p H̄ sqrt(log n/n) → 0;
    H̄(log n)^(3/2)/(√n ϖ′_n) → 0.

D7's fixed decay exponent remains valid. These checks address the actual failure mechanisms in the earlier unrestricted dispersion claim. Continuity of the bounded-size population functional preserves the finite CS nonzero margin, while zero pairs remain exactly zero. The centred-column representation and diagonal/off-diagonal covariance distinctions are now correct. The false exact-Gram multiplier import is explicitly withdrawn from the corollary; the retained (G) paragraphs are labelled notes and are not used here.

**Start and assembly.** X8 uses (FS-G) in the same coordinates as the signal. Sample-correlation and support-sd errors are uniformly small in (R), controlling the random θ*; its design event is measurable in the raw design even though the auxiliary rotation is not. Zero-pair Gaussian bounds are conditional on that design and involve only the realised truth-containing block. In (G), the event correctly omits any raw-sd-near-one requirement. Fixed raw scales can be arbitrary.

X10 verifies the full eigenvalue floor, bounded signal energy and beta-min required by T03♯. X6.1's every-sequence/common-envelope argument supplies the posterior expectation limit under the joint law; pointwise conditional convergence alone is not substituted. The path length is at most the start size, so MR1 and the prefix property give the scored-truth event 𝒦_n. Operational closure is used in the correct direction, `D_n ≤ P(𝒦_nᶜ)`. Delivery is instead deduced from the separate pointwise inclusion

    {output and wrong} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ,

with Proposition F's allocation/fallback and Lemma S regularity. It is not inferred from D_n tending to zero.

## Dependency and previous-fix audit

The relevant upstream strings are retained as recorded:

- FAC-B Theorem FAC-CS and FAC-A Theorem FAC-L: **PROVED-CHECKED**, with their respective scope restrictions. Individual lemma headers retain **PROVED (by this seat, unchecked)** and their separate review annotations.
- T38-(0): **PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))**.
- T03♯: **PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)**.
- Operational closure [OP]: **PROVED (by this seat, unchecked)** inside GEN **PROVED-CHECKED**; treated as an implication from named implementation premises.
- Lemma CAP: **PROVED (by this seat)**, with the recorded council check. Its single-search prefix argument covers nonnegative caps; the integrated monotonicity statement has the separate `a ≥ ℓ_n` qualification.
- Lemma CR: **PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)**.
- F-GROW: **PROVED (A2), checked by A3**; Proposition F's corrected statement, later preflight allocation addition and code-reading qualifications are preserved.
- L4r.0–L4r.3: R11 **VERIFIED**; X9: **VERIFIED-WITH-AMENDMENTS**, two X9-specific minor amendments applied; X8: R12 **VERIFIED**; X10: R12 **VERIFIED**, conditional on path inputs; X7: (R) **VERIFIED-WITH-AMENDMENTS**, (G) **FAILED as written** and withdrawn. These are the actual scopes, not an upgrade by association.

R10's four required changes and the restriction of X8's auxiliary range are present. R11's two X9 repairs and the auxiliary offset repair are present. R12's logarithmic remainder correction and iid-only narrowing are present. R15's raw-scale event correction, onset dependencies and frontier qualification are present. All five R16 corrections are present, including the independent `ψ_U < n` argument and the corrected X9 amendment count. None of the rejected broader claims is needed by the locked theorem/corollary.

For G6, the production code checks were `Scripts/SMC_BVS/core/cpp/v3_engine.h:379–416` and `v3_core.cpp:468–479`: all flips and swaps are scanned with a frozen centre, neighbour ties are lexicographic, an improvement must be strict, and the cap is `ℓ_n+|start mode|` with the additional final scan. The merge message for 4676af6 confirms LS0, the cap, tie-aware start DP, tier-1 fallback and preflight changes. Older FINAL prose about an unmerged branch does not supersede this method definition. Search certification is not confused with a public certification flag on the final reported HPM.

## Numbered issues

1. **EDITORIAL, ancillary summary; NOT REQUIRED for acceptance of the locked statement/proofs.** **Location:** `REPORT.md:90–97` (§5). This summary is stale: it still describes the earlier FAC-NCS draft for both (G) and (R) with merely polynomially vanishing dispersion, says it is not locked/reviewed, and describes per-class exact holes as available despite cross-class drift. The current statement and proofs explicitly narrow the corollary and identify the obstruction; I did not use this obsolete summary as a theorem or proof input. **Fix:** replace §5's draft account with the v2.1 iid-only condition `Δ_n H̄_n ≤ n^(−1/3)`, enlarged scale and actual review status; add FAC-GL's range and refer to the conditional non-crossing result in L4r.4 rather than asserting unconditional exact class intervals. This is a summary synchronisation issue, not a missing step in the reviewed deliverable.

**REQUIRED issues: none. No fatal, major or mathematical minor issue identified in the locked statement and its proofs.**

## Additional falsification checks performed by this seat

The following are supplementary finite calculations, not evidence replacing an asymptotic proof. Python 3.13 was run from `reviews/R17_scratch/` with bytecode writes disabled. No numerical script or output file was created; the executable check and its console output are recorded in this review, the sole file written.

1. Four heterogeneous exact-Gram instances, p = 8, n = 10,000, loadings uniform on [0.2,0.9], truths at 0 and 3 with coefficients (0.8,−0.45): every nonempty subset was checked against direct matrix inversion/determinants (1,020 subsets).
2. Four instances per design model, p = 8, n = 10^9, loadings uniform on [0.55,0.65], same truth: all 64 supersets of S₀ per instance were checked using direct scores. This choice is inside the stated compact-bound exponent range. All additions and truth moves lost, every nonterminal set had a positive null deletion beating every non-deletion, and S₀ was strict (512 supersets total).
3. Four iid near-CS instances, p = 40, n = 10^6, λ̄ = 0.6 and `λ_j = 0.6 + U_j n^(−1/3)/H̄`, U_j uniform on [−0.5,0.5]: production-rule searches from [p] each made 38 null deletions and ended at S₀. The tested dispersion satisfies the narrowed condition.

Captured output:

```text
algebra_subsets = 1020
max_quad_abs = 6.661338147750939e-16
max_L_abs = 4.263256414560601e-14
uniform_supersets = 512; violations = 0
min_best_null_deletion = 8.42281723022461
max_addition = -7.317394256591797
max_truth_move = -64593576.24309158
max_null_swap_minus_best_deletion = -7.574457168579102
ncs seeds 1720,1721,1722,1723:
  each moves = 38; pure_null_deletions = True; truth_endpoint = True
citation-check rerun: TOTAL ok=5 miss=0
```

The citation script initially encountered Windows stdout's cp1252 encoding on a Unicode status symbol; rerunning with `py -3.13 -X utf8 -B` completed successfully. This was an execution-encoding issue, not a missing citation.

Reproduction code for the numerical checks (run with `py -3.13 -B -c`, or execute this block as Python; all imports are read-only):

```python
import sys, math, pathlib
sys.dont_write_bytecode = True
root = pathlib.Path(r'C:/Users/felip/Bayesian-Variable-Selection')
base = root/'Theory_work/Wave2/W2-FAC-X'
sys.path[:0] = [str(base/'T2/numerics'), str(base/'numerics')]
import numpy as np
from eg_core import EGData
from iid_core import IidData, ls0_path

worst_quad = worst_ld = 0.0
checks = 0
for seed in range(4):
    rng = np.random.default_rng(1700+seed)
    p, n = 8, 10000
    lam = rng.uniform(.2, .9, p)
    th = np.zeros(p); th[[0, 3]] = [.8, -.45]
    P = EGData(lam, th, n, rng)
    for mask in range(1 << p):
        U = [j for j in range(p) if mask >> j & 1]
        if not U:
            continue
        sig = np.outer(lam[U], lam[U]) + np.diag(1-lam[U]**2)
        G = (n-1)*sig; H = (n+1)*G + np.eye(len(U)); z = P.z[U]
        qc = float(z @ np.linalg.solve(H, z))
        worst_quad = max(worst_quad, abs(qc-P.quad_closed(U)))
        ld = np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(U)))[1]
        worst_ld = max(worst_ld, abs(ld-P.L_closed(U)))
        checks += 1
print(checks, worst_quad, worst_ld)

viol = sup_count = 0
min_del = math.inf
max_add = max_truth = max_swapgap = -math.inf
for model in ['G', 'R']:
    for seed in range(4):
        rng = np.random.default_rng(1710+seed)
        p, n = 8, 10**9
        lam = rng.uniform(.55, .65, p)
        th = np.zeros(p); th[[0, 3]] = [.8, -.45]; truth = {0, 3}
        if model == 'G':
            P = EGData(lam, th, n, rng); score = P.F_direct
        else:
            P = IidData(lam, th, n, rng)
            score = lambda U: float(P.F(tuple(sorted(U))))
        nulls = sorted(set(range(p))-truth)
        for mask in range(1 << len(nulls)):
            T = truth | {j for i, j in enumerate(nulls) if mask >> i & 1}
            O = set(range(p))-T; ft = score(T)
            gd = {j: score(T-{j})-ft for j in T}
            ga = {l: score(T|{l})-ft for l in O}
            gs = {(j,l): score((T-{j})|{l})-ft for j in T for l in O}
            nD = [g for j,g in gd.items() if j not in truth]
            tM = [g for j,g in gd.items() if j in truth]
            tM += [g for (j,l),g in gs.items() if j in truth]
            max_truth = max(max_truth, max(tM))
            max_add = max([max_add]+list(ga.values()))
            if nD:
                bd = max(nD); min_del = min(min_del, bd)
                sN = [g-bd for (j,l),g in gs.items() if j not in truth]
                max_swapgap = max([max_swapgap]+sN)
                viol += int(bd <= 0 or max([0.]+list(ga.values())+tM
                                          +list(gs.values())) >= bd)
            else:
                viol += int(max([*gd.values(), *ga.values(), *gs.values()]) >= 0)
            sup_count += 1
print(sup_count, viol, min_del, max_add, max_truth, max_swapgap)

for seed in range(4):
    rng = np.random.default_rng(1720+seed)
    n, p = 10**6, 40
    th = np.zeros(p); th[[0, 3]] = [.8, -.45]
    H = math.sqrt(2*math.log(2*(p-2)+2)+2*math.log(math.log(n)))
    lam = .6 + rng.uniform(-.5, .5, p)*n**(-1/3)/H
    P = IidData(lam, th, n, rng)
    out = ls0_path(P, range(p), P.S0)
    print(1720+seed, len(out['moves']),
          all(m[0] == 'delN' for m in out['moves']), out['final_is_S0'])
```

**Final seat decision: G1 PASS; G2 PASS; G3 PASS; G4 PASS; G5 PASS; G6 PASS. Score 9.2/10. Required fixes: none.**

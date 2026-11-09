# W2-FAC-PK — REPORT to Theory HQ (compound symmetry, p > K = ⌊n/2⌋)

> **Flags (read first).**
> 1. **Method change proposed (HQ decides):** the merged LS0 cap ℓ_n + |S̃₀| (MR1) provably fails on this class; any
>    cap rule ≥ max(ℓ_n, ⌈(1 + δ)|S̃₀|⌉), δ > 0 fixed, provably works. Recommended: **ℓ_n + 2|S̃₀|** (METHOD_REQUIREMENTS.md:
>    rule table, option plumbing, cost ≤ ×2 on LS0's worst-case charges).
> 2. **Scope narrowed (flagged in STATEMENT v3.1 §0):** theorems are for the **exact-Gram stage** K < p ≤ n − 1 (an exact
>    compound-symmetric Gram needs p ≤ n − 1). **p ≫ n is not settled** (open deliverable F1; W2-SIM R3 requested; heuristic
>    in §5). NEG needs liminf p/K > 16/15; PATH needs p ≥ K + 16s₀ + 1.
> 3. **Full method (P6) is open.** No production fit completed locally: the merged preflight already charges LS0's worst
>    case at ≈ 146 h for n = 600, p = 450, so 2-hour allocations stop with `resource_limit` (operational finding);
>    completed runs requested from W2-SIM (R2). No full-method claim is made.
> 4. Statement history: v1 REJECTED (R01), v2 → v3 LOCKED (R02 LOCK-WITH-CHANGES), v3.1 = flagged post-lock narrowing of
>    (P4)(iii) to cheaply evaluated cap rules (R05 item 1). The dynamic proof route of v1 was replaced by a static one.
> 5. All results are asymptotic (Wave-2 scope rule); onsets are astronomically large (union bound over 2ⁿ sets).

## 1. RESULT
**PARTIAL relative to the brief; (P1)–(P5) on the exact-Gram stage: PROVED-CHECKED** (statement lock, lemma checks,
mid-point CONTINUE, sweep fixed, council round 2 passed: Sol 9.4, Opus 9.2). The question
"does the merged LS0 route work for p > K?" is settled negatively (checked asymptotic counterexample, Theorem NEG), and
the cap question is settled up to a polynomial gap (Theorem PATH + NEG). Open: p ≫ n; the full method.

## 2. Statement as proved (STATEMENT.md v3.1; proofs lemmas/L0–L4)
Exact-Gram compound symmetry XᵀX = (n − 1)Υ[(1 − ρ)I + ρ11ᵀ]Υ, ρ ∈ (0, 1) fixed; fixed s₀ and nonzero sign-corrected
coefficients ϑ with θ̄ = ϑ(S₀) ≠ 0; model G; method v3.1 + LS0 (main 4676af6) with its implementation premises.
* **(P1) Start mode** (p ≥ K + 16s₀ + 1, blocks ≤ 16): w.p. → 1 every maximiser of γ₀ has size K and keeps the top-ξ nulls
  of each truth-free block; under (PK) liminf p/K > 16/15 and (PB) (all but J₀ blocks of size 16), counts of full
  truth-free blocks differ by ≤ 1 and none is entirely kept.
* **(P2) Theorem NEG** ((PK), (PB)): for every β < ½, the first ⌊n^β⌋ LS0 moves are swaps, so LS0 with any nonnegative
  integer cap ≤ |S̃₀| − s₀ − 2 + ⌊n^β⌋ never scores S₀ — in particular the MR1 and legacy caps fail. [OP]'s upper bound on
  D_n is asymptotically uninformative; nothing is said about the full method or a lower bound on D_n.
* **(P3) Theorem PATH** (p ≥ K + 16s₀ + 1, blocks ≤ 16): for every δ > 0, w.p. → 1 the uncapped LS0 path ends at S₀ (a
  strict local maximum) after ≤ (1 + δ)|S̃₀| moves. No phase structure is claimed (observed: W swaps then deletions).
* **(P4) Theorem FAC-PK** (cap rules ≥ max(ℓ_n, ⌈(1 + δ)|S̃₀|⌉)): (H0) with A = 1; D_n → 0; P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 (with
  CAL); delivery P(no output) = 0 and P(Ŝ⁺ = S₀) → 1 for rules with a ≤ ℓ_n + 2K deterministically and O(1) evaluation,
  under Proposition F's premises, total tier-1 fallback and the re-charged allocation.
* **(P5)** Allowances ≤ n^β (β < ½) fail; ≥ δ|S̃₀| suffice; no optimality claim. Cost: each LS0 worst-case charge is at
  most (ℓ_n + 2K + 1)/(ℓ_n + K + 1) ≤ 2 times its MR1 charge (not a statement about total fit time).
* **(P6)** numerical, pending.

**Mechanism [R08-3].** NEG: on CS every null of a truth-free block carries order-n factor signal, so the start fills to
the size cap K and excludes at least p − K − s₀ nulls (the start need not contain all truths) — the lowest in each
truth-free block, including n^{1/2−o(1)} regular-block minima below −t_n, t_n = 2 + √(log n + 30). At size K every
deletion gains ≤ ½log n + log 3 + o(1), while a swap bringing in such an excluded null (and removing a retained null
within 3.5 of the centre) gains G_sw ≥ M_TV_{jl} ≥ ½log n + 2 (L2.2(iii); M_T ≥ ½ − o(1)); a start missing a truth has an
order-n swap. So the path first makes polynomially many size-preserving swaps, which MR1's O(log n) slack cannot absorb.
PATH (static, not path-restricted): every truth-containing set T ⊋ S₀ of size ≤ K has a deletion gaining
≥ (c_D − ε)log n (any fixed ε > 0), and ≥ (½ − ε)log n when T has > log²n extras (two-sided tail counts + the exact
centring identity Σ_retained(ξ − x_T) = x_T(s₀ + κ) − s_{S₀} + ϱ + a uniform residual floor); S₀ is a strict local maximum.
Move count: O(log n) initial truth-recovery swaps (if the start misses truths), then the main truth-containing phase,
whose total F increase is ≤ K(½log n + 2.4) (log C(2p − 1, K) ≤ 2.39K) and gives ≤ (1 + 6ε)K moves, then O(log²n) moves
after the first entry into the small region; total ≤ (1 + δ)K.

## 3. Status per clause
| clause | evidence |
|---|---|
| L0 imports (p ≤ n − 1) | R03 Sol xhigh VERIFIED-WITH-AMENDMENTS (items 1, 4 applied); pk_selftest_out.txt; R03_scratch (n = 14 direct scoring) |
| L1 / (P1) | R03 V-W-A (no-ties event 𝒟_n; scope); l12_check (L12_check.jsonl), N2 diagnostics |
| L2 / (P2) key negative | R03 V-W-A, no fatal/major; N1 (53/60 MR1 misses), N3 (360), l2_chain (48/48 links) |
| L3 / (P3) key positive | R04 Sol xhigh V-W-A (3 minor, 1 editorial) applied; l3_static (988 sets), l3_trend, l3_small; R04 exhaustive pair search 9.6·10⁷ pairs |
| L4 / (P4), (P5) | R05 Sol high V-W-A (1 major resource-scope → v3.1 narrowing; 4 minor; 2 editorial) applied |
| programme | R06 mid-point (fresh Sol xhigh) **CONTINUE** |
| whole package | R07 sweep (Sol xhigh): 0 fatal / 1 major (implementation plumbing) / 5 minor / 5 editorial — all fixed |
| citations | reviews/CITECHECK.txt: 38 checked, 0 misses |
| council | round 1: R08 Sol 8.6 (gate 3 FAIL, REPORT-level), R09 Opus 9.1 (all PASS) → not passed; fixes reviews/R08_R09_disposition.md. **Round 2: R10 Sol 9.4, R11 Opus 9.2, all six gates PASS in both → PASSED** |
| (P6) | pending (NF_summary.md; W2-SIM R2) |
Inputs (statuses verbatim): T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; T03♯ "PROVED; SF VERIFIED
(W2-VT03R); XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; Lemma CAP
"PROVED (by this seat)", council-checked; Proposition F (A1 "HOLDS-WITH-AMENDMENTS"; A2 "PROVED (A2), checked by A3"; A4
"OK-WITH-FIXES"); FACB L1/L2/L4.0(d,e)/L5 with their R03–R05 verdicts (FACB theorem council-passed).

## 4. Review trail
Statement lock: R01 Sol high **REJECT** (10 items) → v2; R02 fresh Sol high **LOCK-WITH-CHANGES** (3) → v3 locked;
v3.1 (R05-1 narrowing). Lemma checks: R03 (L0–L2, xhigh), R04 (L3, xhigh), R05 (L4, high) — all V-W-A, no fatal.
Mid-point R06 **CONTINUE**. Sweep R07: 0/1/5/5, all fixed. Council: round 1 R08 Sol 8.6 (gate 3 FAIL) / R09 Opus 9.1 → not passed; **round 2 R10 Sol 9.4 / R11 Opus 9.2, all gates PASS → PASSED**; R11's one non-blocking wording fix (F1 heuristic) applied. Astra/Fable: not used.
All reviewer replies verbatim in reviews/, with dispositions for every review (R01–R07, R08_R09, R10_R11).

## 5. Frontier and open items
* **(F1) p ≫ n.** Not proved. Heuristic (not a claim): the NEG mechanism needs only (a) a saturated start forced to
  exclude nulls (true whenever the start fills to K < p — W2-APP Lemma VN gives saturation-or-cover under pervasive
  exposure) and (b) excluded nulls whose swap gain exceeds the best deletion gain ≈ Δ_K = ½log n + log((2p − K)/K) + o(1);
  with M_T ≈ ½ the expected number of such nulls is ≈ K·n^{−1/2}/polylog regardless of p (it does not grow with p), still
  ≫ log n, so MR1 should fail there too [R11-1]. For iid rows M_T and the centre are no longer one-dimensional.
  The PATH budget argument is design-robust: it only needs every set above S₀ with many extras to have a deletion gaining ≈ (½ − ε)log n + log((2p − k)/k); if that "uniform weak-null" property and a
  uniform residual floor (G2 — not automatic for p ≫ n, see §6) hold for iid rows, the doubled cap would again suffice
  (moves ≲ (1 + δ)K, budget G1 with log C(2p − 1, K) in place of 2.4K). W2-SIM R3 (iid-row CS incl. (200, 500)) requested.
* **(F2)** NEG for K < p ≤ (16/15)K (cross-block exchange with block-sum adjustments); **(F2′)** PATH for
  K < p < K + 16s₀ + 1 (start may be unsaturated, R02's example).
* **(F3)** The full method under MR1 (P6): W2-SIM R2. Operational finding: the merged preflight's LS0 worst-case charge
  (≈ 146 h at n = 600, p = 450) makes default allocations stop before any SMC on such designs.
* **(F4)** An exact description of the path (swap count W ≈ p·n^{−1/(4M_W)}, observed) and the optimal allowance.

## 6. Design-agnostic ingredients (for W2-UNI; HQ framing update)
The proofs use these properties; each is stated so that it can become a hypothesis of a general theorem:
* **(G1) Potential budget — generic form [R08-2].** For any design and any T ⊇ S₀ with k = |T|: nested Q is
  nonincreasing and each added column raises the determinant penalty by at most log(n + 1) (the Schur ratio is ≤ n + 1
  because (G_U + I)⁻¹ ⪯ (G_U + I/(n + 1))⁻¹; R11 optional 4), so
  F(S₀) − F(T) ≤ log[w(s₀)/w(k)] + ½(k − s₀)log(n + 1) ≤ log C(2p − 1, K) + ½K log(n + 1). (L3.4 uses the sharper CS
  specialisation Σ_{k}Δ_k.) Combined with a per-move gain lower bound g_n on the sets the path visits, it gives
  m* ≲ budget/g_n + (initial and small-region overheads).
* **(G2) Uniform residual floor — proved only for p ≤ n − 1 (here) [R08-1].** RSS_T ≥ c n σ² for all T ⊇ S₀ with
  |T| ≤ K (χ² projection laws + union bound over ≤ 2ⁿ sets, using p ≤ n − 1); gives M_T ≤ C. It is **not** a consequence of
  Gaussian noise alone when p ≫ n: R08 gives a fixed design with p = Kn ≤ n² (K orthogonal planes, n dictionary
  directions each) where a data-selected size-K model has RSS_T/n → 0. A generic version needs an explicit model-count
  condition (e.g. p ≤ Cn) or design structure; for p ≫ n it is an additional proof obligation.
* **(G3) Truth moves lose / missing truth gains order n** — needs beta-min and an anchored eigenvalue floor (W2-UNI (A1),
  (A3)). Used in L2.2(ii), L3(a), (e).
* **(G4) Weak-null property (the design-specific input).** For every T ⊇ S₀ with m extras: some retained null has
  residual statistic (1 + γ)M_Tτ² ≤ Δ_k − g with g = (½ − ε)log n for m > log²n and g = c log n for 1 ≤ m ≤ log²n. On CS
  this is proved from the one-dimensional reduction (FACB L1), the centring identity and tail counts. For general factor
  models (A2) the centre becomes k-dimensional with loading-weighted residuals; this is the step a general theorem must
  supply.
* **(G5) For NEG only:** saturation under pervasive exposure (population partial covariances of truth-free-block nulls
  bounded away from 0 — factor signal bᵀθ ≠ 0; cf. W2-APP VNF) and the within-block order (CS-specific exchange
  factorisation).

## 7. Files produced (Theory_work/Wave2/W2-FAC-PK/)
STATEMENT.md (v3.1, locked), PLAN.md, LOG.md, CHECKPOINT.md, METHOD_REQUIREMENTS.md, REPORT.md; lemmas/L0_imports.md,
L1_start.md, L2_neg.md, L3_static.md, L4_assembly.md; reviews/R01–R11 (verbatim: lock R01–R02, lemma checks R03–R05, mid-point R06, sweep R07, council R08–R11) +
dispositions, COUNCIL_BRIEF.md, scratch folders of R03, R04, R07, R08, R10, R11, citecheck.py, CITECHECK.txt; numerics/: pk_core.py (closed-form CS start mode + path tracer), copied cs_core.py,
cs_gain.py, bvs_core.py, fac_core.py (unchanged from FACB), pk_selftest.py (+out), n1_scale.py (N1_raw.jsonl), n2_diag.py
(N2_*.json), n3_robust.py (N3_raw.jsonl, frozen N3_raw_final360.jsonl, FROZEN_SNAPSHOTS.sha256), l12_check.py,
l2_chain.py, l3_static.py, l3_trend.py, l3_small.py with outputs, SIM_REQUEST.md, full_method/ (helper's attempt; nf_run.R,
NF_summary.md). No files outside this folder were modified; no git state changes.

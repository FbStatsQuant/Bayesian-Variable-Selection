# R10 — Council seat (Claude Opus 5.5, high), round 2 — W2-FAC-S5

Independent of R09. Read: COUNCIL_BRIEF, STATEMENT v2.3, REPORT, L1–L5, numerics summaries (S1X2, S3, S4, W2-SIM
pilot01), CITECHECK, FACB STATEMENT §1 (D0/score/loop rule), SoP 04_theory.tex:69-74, 84, 492, W1-GEN STATEMENT:169,
HQ_AUDIT A2/A3/A4, FAC-A STATEMENT (scope of its S5 result), R07/R08 + disposition (trail only).

**Verdict: Tier 1 (Theorem FAC-BCS-R: (C1), (C2-R), (C3-R), (C4-R)) is correctly proved and honestly framed; RESULT =
PARTIAL with KL open is accurate. Score 8.8. All six gates PASS. No required fixes.**

## Independent checks (scratch: reviews/R10_scratch/)

* `indep_tau.py` — my own code (not bcs_core): 300 random BCS instances (random ρ_b < ρ_w, variable group sizes, random R):
  L1.3 identity τ = (√ψ_u A + a_u e_R)/√(ψ_u + a_u²V_R) to 6.4e−15, V_R formula to 2.6e−16, bound |τ| ≤ |A| + κ₀|e| 0 violations.
* `indep_path.py` — scorer written directly from D0 (w(k) = 1/(2C(2p−1,k)), H = (n+1)G + I, Q, ν), exact Gram S5,
  p = 30 (6 groups of 5), s₀ = 3, **complete** neighbourhood (all flips and all swaps), production tie rule, from [p]:
  8/8 runs (n = 10⁸, 10¹²) are pure null deletions to S₀ with a strict endpoint; min chosen-deletion gain ≥ 0.40 log n, min
  margin to best non-null-deletion move 0.50 log n; CC(0.05) holds along the whole path in 3/4 runs at n = 10¹² (fails in the
  run with end-phase κ₀|e|/H = 0.32, and in all n = 10⁸ runs because H_q² is not yet below Λ_k — consistent with REPORT §5's
  R08 note). Falsification only.

## Step-by-step audit (G1)

* **L1.2–L1.3.** Re-derived: within-group conditional mean (ub/(ub + d))ȳ_U and variance d(d + (u + 1)b)/(d + ub); posterior of
  h from the sufficient group means N(h, 1/ω_g); residual decomposition r_j = a_j(U) + c_u e_R with a_j ⟂ (h, g_R);
  c_u/s_u = √(d/((ub + d)(d + (u + 1)b))) decreasing, = κ₀ at u = 0. Inverse-M-matrix sign pattern and the 2×2-inverse
  argument for positive partial covariances are correct.
* **L1.4.** Schur increments with Σ̃ = Σ + a⁻¹I (H_T = aΣ̃_TT since (n + 1)(n − 1) = a); leakage σ_j = a⁻¹β̃ᵀϑ^R (uses S₀ ⊆ R and
  Σ̃_RR⁻¹Σ̃_{RS₀} = selection) — the repaired √k/n^{3/2} rate is right; ε decomposition exact; (L1.4.1) via the per-eigenvalue
  bracket on f, applied to both sums (|·| ≤ 2k/((n − 1)d)); M_T = ½(1 + o(1)) for T ⊇ S₀ from RSS sandwich and E2;
  the elementary log inequalities are correct (−log(1 − t) ≤ t + t² for t ≤ ½).
* **L2.** w(k + 1)/w(k) = (k + 1)/(2p − k − 1) ≥ 1/(2p); positive-pair increment ≥ (n/2)c₂ − 2 log n; zero-pair determinant
  increment and RSS_U bound give < −¼ log n; the dichotomy (l ∉ N₀ ⇒ not a zero pair) is exhaustive; FS-BCS is used exactly in
  the positive-pair case and is a finite hyperplane exclusion (finitely many incidence patterns, positive coefficients).
* **L3.** All five components: union counts p·2^{q̄−1} (E_A), s₀2^{q̄−1} (E3), 2¹⁵·16 (E_S, block-local; variance
  ṽ − (1 + ‖β̃‖²)/a ≤ ṽ re-derived), Laurent–Massart for E2 valid up to p = n/2. (c2)–(c4) follow.
* **L4.** Thresholds L4.1 re-derived (Λ_k with (k + 1) in the denominator serves deletions, additions to T and additions to
  T ∖ j simultaneously, up to b_n and 2/p). CC covers exactly the statistics needed: τ_j(T) via e_{T∖j}, τ_l(T) via e_T,
  τ_l(T ∖ j) via e_{T∖j}, including N₀ nulls (E_A is over all nulls). Swap = deletion + addition exactly, and G_del(j | T) ≤ G*
  because Π is defined by the exact score (this design choice makes the argument independent of deletion order — correct and
  clean). Truth-removing moves: bias ≥ (n − 1)dϑ_j² from the all-submatrix floor on T ∪ {l}, cross term via E3 + (c2), no CC
  needed; −(n/4)log(1 + c₃) beats O(log n). Endpoint S₀ and m₀ = 0, k = p (no additions/swaps feasible) handled.
* **L5.** (H0) from the all-submatrix floor; 𝒦_n data-measurable, E_n and CC_n on the enlarged space, union bound
  P̃(𝒦ᶜ) ≤ P̃(E_nᶜ) + P̃(CCᶜ) — no conditioning on a latent event; [OP]/[M5-0]/D′ composition as FACB. Cap: |S̃₀| = p − |N₀| ≥ m₀.

No step fails. **G1 PASS.**

## Gates

| gate | verdict | reasons |
|---|---|---|
| G1 correctness | **PASS** | Every step above re-derived; key identity and path claim independently falsification-tested with my own scorer and a complete neighbourhood. |
| G2 hypotheses used = stated | **PASS** | (C1) uses G, BCS, (P), (θ), FS-BCS; (C2-R) uses no FS-BCS (start given), only (P_α), α < 1/2 for M_T → ½ and b_n → 0; (C3-R)/(C4-R) add premises, MR1, CAL only for (C3-R). Report-level scope (N₀ ≠ ∅, s₀ = 4, exact-argmin vs Π, unchecked labels) now matches the sources (R07 fixes verified at REPORT flags 1–2 and §5). |
| G3 no hidden assumptions | **PASS** | No data-measurability of CC, no symmetry of adaptively chosen sets, no assumption on deletion order; exact Gram and all-principal-submatrix floor are stated (REPORT §7 items 1–2). |
| G4 cited status | **PASS** | CITECHECK 9/9 OK; T38-(0), T03♯, [OP] "unchecked", CAP, F/F-GROW "PROVED (A2), checked by A3", A4 "OK-WITH-FIXES" verbatim; BCS delivery labelled a new extension without inherited approval; KL prover files labelled unchecked and unused in L1–L5. |
| G5 constants/rates | **PASS** | δ/8 margins, b_n, η_n, ε ≤ n^{−1/2}, 2/p for bounded p, c_θ = (1/4)log(1 + c₃), c₃ = ϑ²_min d/(4s²_max), c_FS, union counts all tracked; L4.3 lists what o(1) absorbs. Non-vacuity 2a*(1 + κ₀)² < 1 − δ ⇒ S5 a* < 0.104 re-computed. |
| G6 fidelity (v3.1, 4676af6, MR1) | **PASS** | Score/prior exactly D0 (w(k) = 1/(2C(2p − 1, k)), K = p under (P)); start γ₀ with block tables; LS0 best-improvement over complete flip+swap scans, lexicographic tie rule, prefix property (a ≥ m₀ certified, a ≥ m₀ − 1 scores S₀); MR1 a_n = ℓ_n + |S̃₀| ≥ m₀; e4 irrelevant by uniqueness. Numerical replicas and candidate-restricted scans labelled as such. |

## Score: **8.8 / 10** (uncapped)

Clean, correct reduction with a well-chosen definition of Π (score-defined, so order-free) and honest PARTIAL framing; the
obstruction (KL, one scalar) is precisely located and its evidence correctly qualified. Not higher because the unconditional
content beyond FAC-A is nil (Tier 2 open) and the frontier evidence is all unchecked.

## Required fixes

None.

## Optional suggestions

1. REPORT flag 1 / §6 item 3: "the unconditional S5 frontier stays at FAC-A's 1/6" — add "under FAC-A's hypotheses ((TV) and
   its truth layouts, FAC-A STATEMENT §(c)), which differ from (FS-BCS)". Conversely, L4.6 remark 2 + Tier 1 give a
   self-contained unconditional corollary under (FS-BCS) for a* < 1/(2(1 + κ₀)²) (S5: 0.104); worth one sentence as a
   corollary so the paper has an FS-BCS-based unconditional statement.
2. STATEMENT §0(iii)/REPORT §5: the end-phase ratio κ₀|e|/H_q is sample-dependent; my p = 30 runs reach 0.32 (smaller p, smaller
   H). Say "≤ 0.23 in the S3 runs" rather than reading it as a bound.
3. L4 (b): the proof actually gives G* − G_add ≥ (δ/4)log n (G* ≥ (δ/8)log n and G_add ≤ −(δ/8)log n); stating the stronger
   margin is free.

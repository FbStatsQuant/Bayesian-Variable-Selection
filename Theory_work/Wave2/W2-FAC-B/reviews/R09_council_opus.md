# R09 — Council review, Claude Opus seat (W2-FAC-B, round 1)

Reviewer: Claude Opus 5.5 (council seat). Brief: reviews/COUNCIL_BRIEF.md. Scope rule applied: all results asymptotic; the
astronomically large onset n₀ implied by the constants is not penalised.

**Verdict: ACCEPT. All six gates PASS. Score 9.0 / 10.** No required fix to the mathematics. Two required fixes are
editorial and pre-close (REPORT.md); the rest are optional.

## 0. What I did

1. **Read and line-checked** STATEMENT v3.1 §0–§6 (including (C1-M)), L1–L5 and METHOD_REQUIREMENTS. I formed my view before
   reading R01–R07. Afterwards I read R07_disposition and CITECHECK.txt.
2. **Re-derived independently** the following:
   * the Sherman–Morrison neighbour formulas (L1.3);
   * the centre identity and the k-free offset ϱ (L1.4);
   * the Q-vs-RSS sandwich (L1.5(b));
   * the population partial covariance c(U, l) (L2.1);
   * the drift identity and the gap recursion (L4.1(iv));
   * every inequality chain in L4.2–L4.4, including the opposite-endpoint swap value V = 4σH̄(x − σγ_kH̄).
3. **Read the code on main.** I checked the local search (`Scripts/SMC_BVS/core/cpp/v3_engine.h:379-419`), the LS0
   integration and cap (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:460-482`), ℓ (`v3_preprocess.R:23`) and the fallback
   (`v3_calib.R:122-143`).
4. **Read the cited sources** for status and content: FINAL s3 (T03♯), s6 (Proposition F, D′, F-GROW), s7 (Lemma CAP), A2
   steps 1–3, GEN STATEMENT:169, C-GROW L4_assembly:12-14, SoP 02_method §6.10/LS0 and 04_theory:84/492.
5. **Ran an independent first-principles numerical falsification check** (reviews/R09_scratch/indep_check.py,
   indep_check2.py → indep_out.txt, indep_out2.txt). It does not use the CS closed form. It has:
   * the general D0 scorer (Cholesky of H_A, slogdet of G_A + I, exact BB prior);
   * either an explicit exact-Gram X (QR of a centred Gaussian matrix times Σ^{1/2}·√(n − 1); n = 10⁵, 10⁶) or Gram-level
     sufficient statistics (n = 10⁸);
   * a block-DP start mode with margin to the runner-up;
   * a transcription of the coded scan loop: flips j ascending, then swaps (j ∈ S asc) × (l ∉ S asc), lexicographic
     ties, strict improvement, cap ℓ_n + |S̃₀|, and one further scan.

   Results:
   * **Generic ϑ satisfying (FS)** (ρ ∈ {0.3, 0.5, 0.7, 0.95}, p ∈ {40, 48, 56, 60}, s₀ ∈ {1, 2, 3, 4}, block size 8 or
     16, layouts with N₀ = ∅ and N₀ ≠ ∅): 23/23 data sets give start mode = S*, unique, with margin ≥ 6.6 nats. In each
     the LS0 path is a pure null deletion of exactly m₀ moves, ending certified at S₀. In every case LS0 with the legacy
     cap ℓ_n does not score S₀ (m₀ ≥ ℓ_n + 2 holds in all of them).
   * **Masked truth** (ϑ = (1, −2), ρ = ½, c(∅, j) = 0; (FS′) holds): start = S*, path to S₀, 2/2. This supports (C1-M).
   * **(FS) deliberately violated** (my own control):
     * (FS-a) broken (ϑ₅ + ϑ₂₀ = 0): the start mode misses 7 nulls of S* in 3/3 data sets at n = 10⁸, while the path still
       ends at S₀. So (FS) is genuinely used by (C1). As stated, it is sufficient but not necessary for discovery.
     * (FS-b) broken at u = 1: the start was still S* (3/3 at n = 10⁸), consistent with "sufficient, not necessary".
   * The two start-mode misses at n = 10⁵ in my first batch are a finite-n effect plus that same (FS-b) equality. They
     disappear at n = 10⁸.

   These are diagnostics, not proofs; they agree with N1, N3, N4 and N7.

## 1. Gate 1 — correctness of every step: **PASS**

**L1.** All checked.
* Deletion, addition and swap identities follow from γ_u(1 + γ_{u−1}) = γ_{u−1} and γ_{u+1}(1 + γ_u) = γ_u.
* ϱ is k-free because r_k = γ_k·[…]/β with γ_k = 1/(k + α/β). This is the fact that makes the drift identity exact.
* The constant in Q_T − RSS_T/s² ≤ 1 + 1/((n − 1)(1 − ρ)) is right.
* The L_u-increment bound is right, using (α + vβ)/(α′ + vβ′) = (n + 1) − n/(α′ + vβ′).

**L2.**
* c(U, l) = (1 − ρ)[ϑ_l + ρϑ(S₀ ∖ U)/(1 + (u − 1)ρ)] is right, including the case u = 0.
* Positive pairs give an order-n increment against an O(log n) size cost.
* For zero pairs, the variance bound ≤ 4 and the 2²⁰ union are fine. ν·O(L_n/n) = O(L_n) gives the −¼ log n bound, and
  w(k − 1)/w(k) = (2p − k)/k ≥ 1.
* The case split in L2.4 is exhaustive: either some l ∈ S* ∖ S is a positive pair, or S ⊋ S* and an N₀ null can be removed.

**Corollary M (post-lock, council-only check; I checked it in full).** FS-b at u = 0 is used only in L2.4(a) with U = ∅.
There a null l′ ∈ C_b (∉ S since U = ∅) has c(∅, l′) = ρϑ(S₀) ≠ 0, so S is not a maximiser. FS ⇒ FS′, because FS forbids
masked truths, which makes the extra block clause vacuous. So (C1-M) weakens a hypothesis, as claimed.

**L3.** Each tail bound checks:
* E4: Markov on counts with dyadic blocks.
* E5: conditional Rademacher signs given |ξ|, so Top(j) is fixed and Hoeffding applies.
* E6: t₀ ≥ H − δ_e via the Mills lower bound and m₀ ≥ 5.
* E7: φ(b) ≥ Φ̄(b) ≥ Φ̄(t₀) = 2m₁/m₀ for 1 ≤ b ≤ t₀, so each cell fails with probability ≤ exp(−L_n m₁/2).

Consequence (c2): every consecutive gap of the sorted 𝒩* configuration, including across 0 and across b = H − δ_e, is
≤ L_n/2 + 2δ_e ≤ g_max.

**L4 (key lemma).** I find no gap.
* **L4.1.** The interval invariant needs only k − 1 + κ > 1 (k ≥ s₀ + 1 ≥ 2) and that the boundary point is the argmin.
  In (iv), g_i is a consecutive gap of 𝒩* itself, because the deleted point bounds the hole, so (c2) applies.
* **Regime (S).** H̄² ≤ (1/90) log n gives null τ² ≤ 0.1 log n. The margins 0.29 / −0.29 / 0.11 hold with M_T ≤ 1 + o(1)
  and V ≤ τ_l².
* **Bulk, B3 Case A.**
  * If x_i > Δ_i/2, then b_i > |a_i|, the kept set lies in Top(J), and K⁰ ∖ K is positive, so s_K ≤ D_J.
  * The count bound J ≤ 2N₋ + √(2Jx_J) ≤ 4m + 2x_J, together with x_J/J → 0, gives J ≤ 5m.
  * The numerical constant 10x_{5m}/m ≤ 11/K₁ = 0.11ε_b² holds once 2 log(5K₁L_n + 1) ≤ 0.1L_n. This is a very large but
    legitimate onset.
* **Bulk, B3 Case B.** All negatives are kept and the hole is positive, so s_K ≤ D_{m₀} and m ≥ m₀/3.
* **Bulk, B1.** A lone deleted lower point is min ξ < 0 with |a| ≥ H − δ_e. L ≤ R then forces b ≥ (1 − 3ε_b)H and
  x_{i−1} ≥ (1 − 4ε_b)H, which contradicts B3 at i − 1. The induction order B1 → B2 → B3 → B4 is non-circular.
* **Bulk, B4.**
  * Young with parameters 2ε_b (deletion) and 4ε_b (addition) gives the stated coefficients.
  * The comparison log(2m₀/m) ≤ log((2p − k)/k) + O(1) needs k ≤ p, which holds.
  * Null-out swaps satisfy V ≤ Δ(2d + Δ) ≤ 5ε_b log n.
  * Case (ii), m > n/log³ n, uses only M_T ≤ 1 + o(1) and Z_m² ≤ 10L_n.
* **End phase.**
  * The entry drift bound holds, and the structure a_i < 0 < b_i follows from m < m₁ < m₀/3.
  * Kept magnitudes lie in [H̄ − 2δ_e, H̄].
  * E-del: (k + κ − I)² ≤ (k + κ − 1)² for 1 ≤ I < k; the I = 0 margin is c_D = ½ − 1/(s₀ + 1 + κ_∞) > 0.
  * E-side: the majority side is deleted because x > δ_e. |I| is non-increasing and c_I is monotone iff |I| ≤ k + κ.
  * E-add covers the three cases.
  * E-swap: V is convex in τ_l. The same-side endpoint gives O(H̄δ_e). The opposite endpoint gives
    4γ_kh(σI − 1) + o(log n), which I recomputed. So G_sw ≤ 8ε_b log n when |I| ≥ 2 and o(log n) otherwise; both are
    strictly below the chosen deletion.
  * The sign reversal of ϱ for I < 0 is correctly flagged.
* **Ties.** The 𝒩𝒟_n exclusions are nontrivial linear relations: the η-coefficient of x_T is nonzero. So every deletion
  argmin is strict and the tie rule is never invoked. Cross-type comparisons have log-n margins.

**L5.**
* (H0) verification: φ₀² = 1 − ρ; SE_λ for every j₀; SE_w with g₀ = 1 − ρ ≤ (n − 1)(1 − ρ); BM-∞ with ϑ fixed; A = 1.
* The 𝒦_n inclusion G_n ⊆ 𝒦_n.
* The legacy-cap negative: every scored set has size ≥ |S*| − ℓ_n − 1 > s₀.
* The D′ pathwise inclusion for (C4).

All correct.

## 2. Gate 2 — hypotheses used = hypotheses stated: **PASS**

* (FS)/(FS′) is used only in L2. L3–L5 do not use it, as stated. My (FS-a)-violated control confirms that (C1) really
  needs it.
* (P) is used for K = p, for r ~ χ²_{n−1−p} with n − 1 − p ≥ n/2 − 1 (M_T ≤ 1 + o(1)), and for p ≤ n¹ in T03♯.
* (θ) (fixed sign-corrected ϑ, fixed s₀, σ²) is used for c_FS, TL, BM-∞ and M.
* (CS) with ρ ∈ (0, 1) gives nonsingularity, the exact 1-D reduction and λ_min = 1 − ρ.
* CAL enters only through [M5-0] in (C3), and (C4) is CAL-free. Both are stated.
* The partition is used only through |C_b| ≤ 16, as stated in §1 (statistical claims for every deterministic partition;
  (C4) for the method's partition).

## 3. Gate 3 — no hidden assumptions: **PASS**

* The model identification (C, D_x, θ* = D_xβ, μ = Xθ*, y = Y/s, yᵀy = n − 1) is explicit (R07 item 1).
* "Every method quantity is a function of (XᵀX, Xᵀy, yᵀy)" holds, including the partition (|r̂| from XᵀX).
* The enlargement of the probability space for (η, ξ) is legitimate. 𝒦_n is data-measurable, as L5.2 notes.
* Exact arithmetic is the named premise EX-A. The start-mode uniqueness makes e4/e4′ and the 10⁶-enumeration-vs-DP code
  paths irrelevant.
* No NA on the lattice [S₀, S*] is used anywhere (L4.5(3)), and none is needed.
* The only "assumption-like" content is the size of n₀, which is asymptotic and admissible.

## 4. Gate 4 — cited lemmas have adequate status (verbatim and correct): **PASS**

I checked each against its source:

| Input | Status as quoted | Source |
|---|---|---|
| T38-(0) | "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" | SoP 04_theory:492 |
| T03♯ | "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" | FINAL s3 status box |
| [OP] | "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED" | GEN STATEMENT:169; GROW L4:12-14 |
| Lemma CAP | "PROVED (by this seat)", council round 3 | FINAL s7 review flag |
| Proposition F | A1 corrected form, council round 3; A4 "OK-WITH-FIXES" | FINAL s6 |
| F-GROW | "PROVED (A2), checked by A3" | FINAL s6 |

* [OP]'s cap-independence is quoted correctly.
* CITECHECK reports 14/14 OK.
* The use of [OP] at its unchecked status is disclosed (L5.4: "A3 finding 4") and is the same as in GROW and A2.
* (C4)'s claim that P(no output) = 0 is class-free is justified by A2 step 2 (Lemma R counting is uniform in valid inputs)
  and step 1 (Lemma S inputs). I checked that both apply verbatim to a fixed CS design.

## 5. Gate 5 — constants / rates tracked and uniform: **PASS**

* L_n = log log n. Every probability bound in E1–E7 and E_n^S is explicit, depends only on n (and on m₀ only through
  regime-(L) quantities that diverge uniformly), and holds uniformly over p ≤ ⌊n/2⌋.
* The regime split p ≤ n^{1/200} / p > n^{1/200} is made per n with one n₀(ρ, ϑ, σ, s₀), so no subsequence argument is
  needed.
* Along the path, every o(log n) term is one of the following, each uniform in T on the path:
  * H̄e_n, hε′ or L_n in the end phase;
  * the O(1/log n) multiplier error from L4.0(d), or O(L_n) in the bulk.
* M_T ≤ 1 + n^{−1/4} holds for all T ⊇ S₀ at once (via Φ(T) ≤ gᵀΣ⁻¹g), and M_T ≤ ½(1 + C/log n) under the stated
  ℓ²-budget.
* The truth-move lower bound is uniform over T in [S₀, S*].
* The addition constant c = c(ρ, s₀) is effectively min(0.29, c_D/2) for n ≥ n₀. (See optional suggestion 2.)

## 6. Gate 6 — fidelity to the method as coded/specified: **PASS**

* **LS0 cap.** `cap_ll = ls0_ell + |m.S|`, with ls0_ell defaulting to ell = ⌈log₂(n + p + 1)⌉. This is a_n = ℓ_n + |S̃₀|.
  The final local search keeps ℓ_n.
* **Extra scan / termination.** `if (A.moves >= ell)` gives local_limit and returns the best neighbour, which is scored.
  So cap a scans C₀…C_{min(a, m*)}. This is exactly the prefix property used: "a ≥ d − 1 scores S₀; a ≥ d ends
  certified".
* **Scored set.** The emitted centre (emit_centre = true) and every scanned neighbour join the ledger.
* **Tie rules.** The scan uses largest F with plain lexicographic ties and a strict move. The HPM uses size-then-lex. The
  start mode uses size-then-lex (enumeration ≤ 10⁶ or e4 DP). All are irrelevant on the events used, and the proof says so.
* **K.** K = p. Additions beyond K are excluded. At S* with N₀ = ∅ there are no additions, and the "every addition"
  claims are then vacuous and correct.
* **Exact branch.** It is handled by the [OP] convention: enumeration only adds scored models, and the deterministic LS0
  is defined on every data set.
* **Delivery premises.** (C4) lists exactly Proposition F's premises, the amended W_G/M_G envelopes and the A4 preflight
  terms. The tier-1 fallback is on main (`v3_calib.R:122-143`, merge 4676af6).
* I re-implemented the coded loop independently. On every (FS) data set it reproduces the predicted path, move count and
  certified endpoint.

## 7. Score: **9.0 / 10** (uncapped)

The ticket solves a real and non-obvious problem. GROW's route provably cannot apply, because the start mode is the whole
model. The proof finds the right structure: an exact one-dimensional reduction with a k-free offset, which makes the drift
identity exact. It also uses a path-restricted analysis (gap invariant, sign-symmetric top-set bound, extreme-tail
imbalance dynamics) instead of a false lattice-wide NA.

The proof is complete, carefully quantified and uniform in p_n. The delivery extension is a correct and honestly
qualified reuse of A2. The scope is narrowed transparently, and the frontier is stated as obstructions to the technique
only.

Why not higher:
* The key lemma is long, and constant-heavy (ε_b = 1/50, K₁ = 2.5·10⁵), with an astronomically large onset. This is
  admissible but makes reading hard.
* (C1-M) was added after lock and is checked only by this council (I checked it).
* Some HQ-facing text is stale (below).

## 8. Required fixes (editorial, pre-close; no gate depends on them)

1. **REPORT.md §2 / flag 3.** The report still says "STATEMENT.md v3", and its theorem summary omits (C1-M) / (FS′) and
   Corollary M (L2.5). Update it to v3.1. Add (C1-M) with its "added after lock, flagged, checked only through the council"
   qualifier. Note that (C1-M) weakens a hypothesis, so flag 3's "no claim strengthened" stays true.
2. **REPORT.md §3–§7.** "Sweep R07 [pending]" and "CITECHECK [pending final run]" are outdated: R07 is dispositioned (17
   items fixed) and CITECHECK reports 14/14 OK. §1 and §5–§7 are placeholders. Finalise them, and add a status row for
   L2.5 (council-checked only).

## 9. Optional suggestions

1. **L4 statement / (C2)(ii).** Make the addition constant explicit, e.g. c := min{0.29, c_D/2} with
   c_D = ½ − 1/(s₀ + 1 + (1 − ρ)/ρ), for n ≥ n₀. The end-phase bound is −c_D log n + o(log n), so "c log n" silently
   absorbs the o-term.
2. **L4.3 (B3).** Add one line stating the onset condition implied by "10x_{5m}/m ≤ 11/K₁", namely
   2 log(5K₁L_n + 1) ≤ 0.1L_n, i.e. L_n ≳ 400. Readers then see that n₀ is astronomically large and that the numerics
   (n ≥ 10⁵) are far below the proof's onset. This is permitted by the scope rule, but worth stating once.
3. **L2.1.** "≤ 2 max|g_j| ≤ 16 max|g_j|" is harmless but odd. Keep "2 max|g_j|" and carry the constant.
4. **(FS) remark.** My control run with (FS-a) violated (ϑ_a + ϑ_b = 0) shows the start mode is a strict subset of S*,
   yet the LS0 path still ends at S₀. Record this in the frontier as evidence that (C3)/(C4) may survive (FS) failure. This
   would be a natural extension: a start between S₀ and S* with the same gap structure. It should not be claimed.
5. **L5.4.** State in one sentence that Proposition F's classes are extended here to fixed CS designs (model G), exactly
   as A2 extends them to GROW. Without it, a reader of FINAL s6 sees only LH/LH-iid/GEN/GROW.

## 10. After reading the review history (R01–R07)

My independent findings agree with the dispositions. The R01 swap-margin counterexample is correctly respected:
(C2)(ii) claims swaps are only below the chosen deletion, never below F(T), and the proof never uses more. I found no
issue that earlier rounds missed beyond the editorial items above.

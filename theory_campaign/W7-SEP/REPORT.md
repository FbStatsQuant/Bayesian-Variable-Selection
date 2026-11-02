# W7-SEP — REPORT: the separation theorem (what the tempering bridge buys)

Run of 2026-11-02, branch `theory/W7-SEP`. Proofs: `PROOF.md`. Scripts: `scripts/` (fixed seeds). Raw results and
tables: `results/`. Working notes: `NOTES.md`. Every result is a **candidate**: not reviewed, not adopted. Status
words follow `theory_campaign/PROTOCOL.md` and are never upgraded.

## 1. Headline

1. **The task's claim (a), as written, is false on its own family.** On LH, "start-only + production local search" does
   **not** fail: S̃₀ = S° and the search from it scores S₀ with probability → 1 (this is already T38(b1-LH)). The task's
   exception ("unless the greedy basin of S₀ contains S̃₀") is the generic case, not an exception. **COUNTEREXAMPLE**
   (by proof, Corollary GU-LH; and numerically in 100% of replicates).
2. **New: Proposition GU (greedy universality), PROVED (candidate).** On exact-Gram designs with an isolated relevant set R
   (Σ_{R,Rᶜ} = 0), SE on R and fixed signals, the production local search started at **every** C ⊆ R reaches, scores and
   certifies S₀ w.p. → 1, in ≤ τ_GU moves (a constant). It needs no PGD (which fails under SE + BM-∞). It proves
   W1-T37R's Conjecture C4 in this case, and extends W4-SHARE Prop. M: in R1 with SE and fixed signals the masked regime
   has **no posterior-level barrier** anywhere on the start's support. Stress test: 40 random designs (24 violating PGD),
   every relevant centre scores and certifies S₀ at n ≥ 5·10⁴.
3. **What is separated, PROVED (candidate): sampling-only start methods versus search.** On LH (exact Gram; LH-iid through
   W3-PXN, unverified) with cancellation depth c: iid π₀ draws score S₀ w.p. → 0 or → 1 according as Q/Q* → 0 or ∞,
   with the sharp two-sided threshold **Q\* = p^c n^{c/2}**; one-shot importance correction has 1 + χ² ≥ Q*e^{O_P(1)},
   relative variance (Q*/Q)e^{O_P(1)}, and the corrected estimator of π(S₀) is **0** w.p. → 1 below Q*.
   With p ≍ n^a the iid exponent c(a+½) exceeds v3's polynomial ceiling exponent a + max(1, a) **iff c ≥ 2**.
4. **There is no super-polynomial separation in the frozen setting**, because c ≤ s₀ is fixed, and **no separation at all
   between the tempering bridge and a single greedy search from the start mode** on LH: both have polynomial cost of a
   degree that does not grow with c. What the theory supports is "*moving off the start is needed*", not "*tempering is
   needed*". (c) v3 succeeds is a citation: T38(b1-LH) with LS0 (PROVED-UNDER, unreviewed); without LS0 via O-BGIBBS BG1
   (PROOF SKETCH, unverified).

## 2. Statements

Full statements with hypotheses: `PROOF.md` §1 (Theorem SEP), §4.1 (Prop. BASIN), §4.2 (Prop. GU, Cor. GU-LH).
Families: LH exact Gram (X′X = (n−1)Σ_LH, p ≤ n−1, c ≥ 1 linked pairs, 0 < |ψ_i| < min ρ, fixed coefficients,
g ≤ B_n < 2g); LH-iid (W3-PXN, n^a ≤ p ≤ n^A). Cancellation depth c = number of masked hubs. Q* := p^c n^{c/2}.
Mstat := log π₀(S₀) + c log p + (c/2) log n.

**Theorem SEP (refined).**
- **(A) iid start discovery.** P₀(S₀ scored by Q iid π₀ draws, plus all block tables) → 0 if Q/Q* → 0 and → 1 if
  Q/Q* → ∞. Polynomial budget n^α fails iff α < c(a+½) (p ≍ n^a). Hypotheses: EX-A; LH (W1-EXP Thm 5(b), Lemma 4.2).
  **PROVED.** (LH-iid: PROVED given W3-PXN P1, P4, unverified.)
- **(B) one-shot importance correction.** 1 + χ²(π‖π₀) ≥ π(S₀)²/π₀(S₀) = Q*e^{−Mstat}(1+o_P(1));
  KL(π‖π₀) ≥ (c log p + (c/2) log n)(1 − o_P(1)) − O_P(1); for Î_Q = Q⁻¹Σ w̄(X_i)1{X_i = S₀},
  relvar = (1/π₀(S₀) − 1)/Q; if Q/Q* → 0, Î_Q = Ĩ_Q = 0 w.p. → 1 while π(S₀) → 1. Hypotheses: (A)'s plus locked T03
  via W1-EXP Thm 5(d). **PROVED** (the χ²/KL/ESS parts overlap O-WSTAB WS7, PROVED there).
- **(C) start + search (negative).** Prop. GU ⇒ on LH, w.p. → 1, every C ⊆ R (R = union of non-null groups) is in the
  scoring basin 𝔅_ℓ; hence LS0 and "one iid draw + local search" score S₀ w.p. → 1 at cost O(p² log n).
  **PROVED** (candidate; uses W4-T38FULL Lemma M, same-family VERIFIED only). Clause (a) of the task restricted to
  search-augmented methods: **COUNTEREXAMPLE** on LH.
- **(D) v3.** T38(b1-LH) (LS0): PROVED-UNDER its premises, unreviewed. No LS0: D2 for c = 1 (NB step PROOF SKETCH);
  BG1 for every fixed c (PROOF SKETCH, unverified; needs n/(T_e log(p√n)) → ∞). Cost: T32(i) ceiling (CONJECTURE)
  + LS0 term (PROVED).
- **(E) exponents** (p ≍ n^a): iid / IS need c(a+½) (sharp); LS0 or one draw + search ≤ 2a (+log); v3 with LS0
  ≤ a + max(1, a) (+log, conditional on T32). Separation iid vs v3 ⇔ c ≥ 2; iid vs LS0 ⇔ c ≥ 2 or a < ½.

**Proposition BASIN (PROVED, deterministic).** LS0 scores S₀ iff S̃₀ ∈ 𝔅_ℓ (the set of centres whose best-improvement
path meets {S₀} ∪ N(S₀) within ℓ moves); "Q draws + search" succeeds with probability 1{S̃₀ ∈ 𝔅_ℓ} ∨ [1 − (1 − π₀(𝔅_ℓ))^Q]
given the data. This is the exact answer to "when does LS0 alone suffice"; GU, Lemma LS-score and Theorem A are
sufficient conditions for membership.

**Proposition GU (PROVED, candidate).** Hypotheses: G; exact Gram; R ⊇ S₀, |R| ≤ r fixed, Σ_{R,Rᶜ} = 0;
λ_min(Σ_R) ≥ φ₀²; min_{S₀}|θ*| = θ₀ > 0 and θ*′Σθ* ≤ M fixed; p ≤ n^A. Conclusion: w.p. → 1, from every C ⊆ R the
production search reaches, scores and certifies S₀ within τ_GU = 1 + ⌈(2s₀/φ₀²) log(M/(φ₀²θ₀²))⌉ + (r − s₀) moves
(eventually ≤ ℓ_n). Two phases: (1) while Δ > 0, every step lowers Δ by a factor (1 − φ₀²/(2s₀)), because the best
truth addition reduces Δ by ≥ (φ₀²/s₀)Δ (Lemma GU-1) and Lemma M makes the greedy choice Δ-optimal up to m_n → 0;
nulls never enter. (2) On supersets of S₀ inside R, every deletion of an extra gains ≥ ¼ log n and every addition or
swap loses (Lemma GU-2 + one χ² union over ≤ 2^r p pairs), so the search deletes the extras one by one and stops at S₀.

## 3. Proofs

All in `PROOF.md`:
- (A) §2: exact conditional miss probability (1 − π₀(S₀))^Q, the tables excluded on {blocks = groups}, and bounded
  convergence with Mstat = O_P(1) on both sides.
- (B) §3: one-atom lower bound for χ², data processing for KL, iid second moment for Î_Q, and the miss event.
- (C) §4: Lemma GU-1 (population descent: Schur complement + an ℓ₁/ℓ₂ argument), Lemma GU-2 (prior, determinant
  via Schur complements, fit via Lemma M's Q-versus-RSS bounds and an exact χ²₁ identity on supersets), then the
  two-phase proof. The crux is Lemma GU-1(b): red*(T) ≥ Δ(T)²/‖θ*_{M_T}‖₁² ≥ (φ₀²/s₀)Δ(T).

## 4. Evidence

All exact (no Monte Carlo inside a replicate): full enumeration of the 2^p models, start law with blocks = groups
(the v3 partition equals the groups w.p. → 1 on LH; at these p the method itself would take the exact branch, so π₀
is the analytically defined component law, as in W1-EXP), production local search from **every** centre via a
vectorised successor map. Scorer checked against the dense formula to 6·10⁻¹³ and the successor map against a direct
scan (`results/sanity.txt`).

**4.1 LH at p ≤ 20 (`scripts/sep_exact.py`, `results/summary.txt`).** Configurations: B2 = W1-EXP config B (c = 2,
p = 20, one null group), V2 (c = 2, one visible and one null group, p = 18), C3 (c = 3, p = 18). n from 100 to 409,600.

TABLE_PLACEHOLDER

Reading:
- **Masking (A).** log₁₀π₀(S₀) falls by c/2 per decade of n (C3: −5.42 → −10.7 over 3.6 decades, slope ≈ −1.5);
  Mstat is tight (W1-EXP's predicted limit for B2, q05/med/q95 = 1.29/1.42/1.89). At fixed p the p^c factor is a
  constant, so the final run's Q_f ≍ n log n still finds S₀ for c = 2 (R-T20(i): c ≤ 2 certain at fixed p) but not for
  c = 3 (P(hit | Q_f) → 0). The p-dependence is checked in 4.2.
- **IS (B).** log₁₀(1 + χ²) tracks −log₁₀π₀(S₀) to within 0.2 in every cell; the per-draw relative variance equals
  1/π₀(S₀) − 1 exactly; KL grows like c log(p√n).
- **Search (C).** LS0 scored S₀ in every replicate of every cell. π₀(𝔅_ℓ) (the per-draw success probability of
  "iid draw + search") is ≥ 0.999999 in every replicate. At small n some centres C ⊆ R fail; all of them are
  move-limited (max moves = ℓ) or posterior misses. From n = 1600 on, **every** centre in 2^R scores S₀ in every
  replicate, as GU predicts, and the fraction over all 2^p centres is ≥ 0.989.

**4.2 Budget scaling in p (`scripts/scaling.py`, `results/scaling.txt`).** LH exact Gram, g = 9, p ∈ {108, …, 864},
n ∈ {1000, 4000}, exact start law by convolution (W4-T38FULL code), 3 reps per cell.

| c | n | p | med log₁₀π₀(S₀) | med Mstat | log₁₀Q* | log₁₀Q_f | Q_f·π₀(S₀) | LS0 scores S₀ | LS0 score evaluations |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 1000 | 108 | −6.32 | 1.72 | 6.32 | 5.20 | 7.6e−2 | 3/3 | 1,355 |
| 2 | 1000 | 864 | −8.19 | 1.58 | 8.19 | 5.20 | 1.0e−3 | 3/3 | 11,183 |
| 2 | 4000 | 864 | −8.69 | 1.80 | 8.69 | 5.46 | 5.9e−4 | 3/3 | 11,183 |
| 3 | 1000 | 108 | −9.13 | 3.39 | 9.13 | 5.20 | 1.2e−4 | 3/3 | 2,359 |
| 3 | 4000 | 864 | −12.70 | 3.47 | 12.70 | 5.46 | 5.7e−8 | 3/3 | 19,747 |

Each doubling of p lowers log₁₀π₀(S₀) by 0.60–0.64 at c = 2 (predicted c·log₁₀2 = 0.60) and 0.80–1.06 at c = 3
(predicted 0.90); Mstat stays flat in p. At c = 3, p = 864, n = 4000, iid discovery needs ≈ 5·10¹² draws and the
final run's own iid budget hits S₀ with probability 6·10⁻⁸, while LS0 scores S₀ with 2·10⁴ evaluations, in 3/3.

**4.3 Stress test of Prop. GU (`scripts/gu_stress.py`, `results/gu_stress.txt`).** 40 random exact-Gram designs, p = 14,
|R| = 10 with 2–5 truths and combination look-alikes (24 designs violate PGD at ∅), 4 isolated nulls, search from all
2^14 centres:

| n | designs with every C ⊆ R scoring S₀ | … and certifying | mean fraction of C ⊆ R scoring | mean fraction of all centres | median π(S₀) |
|---|---|---|---|---|---|
| 200 | 22/40 | 18/40 | 0.839 | 0.842 | 0.48 |
| 1,000 | 32/40 | 31/40 | 0.965 | 0.977 | 0.88 |
| 5,000 | 37/40 | 37/40 | 0.985 | 0.992 | 0.95 |
| 50,000 | 40/40 | 40/40 | 1.000 | 1.000 | 0.98 |
| 500,000 | 40/40 | 40/40 | 1.000 | 1.000 | 0.99 |

The finite-n failures sit in near-collinear designs (φ₀² = λ_min(Σ_R) between 0.004 and 0.03) and mostly where
π(S₀) is small (posterior misses); GU's thresholds scale with 1/φ₀⁴, consistent with this.

## 5. What fails and why

- **"Start-only + local search fails" (task (a)).** False on LH, by Cor. GU-LH and T38(b1-LH). More generally false on
  every exact-Gram family with an isolated relevant set, SE and fixed signals (Prop. GU). Not a technicality: GU-1 shows
  that under SE every state missing a truth has a Θ(1) Δ-reduction available, so there is no population trap.
- **"Super-polynomial budget for start-only discovery".** False in R1: Q* = p^c n^{c/2} is polynomial because c ≤ s₀
  is fixed. R-T20(i)'s "exponential deficits fail for every polynomial budget" needs an exponential masking law, which
  LH does not have (T27's law is polynomial). A super-polynomial gap needs c_n → ∞ (outside R1, and outside every proved
  v3 route).
- **Separating the bridge from search.** Not possible on LH, and by GU not possible on any exact-Gram,
  isolated-relevant-set family with SE and fixed signals. The candidate places for a separation are all outside the
  frozen setting: a posterior barrier (needs SE to fail; W4-SHARE's PB design has one, but the bridge also fails there
  asymptotically: 82% → 51% of islands from n = 4000 to 16000), move-limit binding (Φ(S̃₀) > ℓ + 1, as in the study's
  S4/S6 at n = 200; an artefact of ℓ), growing c, or weak signals θ₀ → 0.
- **Using Theorem A / TD′_P for the general claim.** TD′_P needs PGD, which fails under SE + BM-∞ (W1-T37R C3); GU
  avoids PGD by a Δ-descent potential instead of the Φ-potential.
- **GU for centres containing data-chosen nulls.** Phase 2 would need deletion gains uniformly over data-chosen null
  sets (the NA/LD issue of W1-T37R C1). Not covered; OPEN.

## 6. Needs escalation

1. **Cross-family check of Prop. GU** (PROOF §4.2), especially Lemma GU-1(b) (the ℓ₁/ℓ₂ descent bound), the determinant
   bound in Lemma GU-2, and the use of W4-T38FULL Lemma M with data-chosen pairs (Lemma M's event is uniform, Remark 1
   there). GU is the result that changes the story, so it should be checked before HQ relies on it.
2. **Lemma M itself** is only same-family VERIFIED; GU inherits that.
3. **HQ decision on the paper's spine.** The theory supports "the start is masked, so the method must move off its
   draws", and it separates *sampling-only* start methods from v3 with exponents c(a+½) vs a + max(1,a). It does **not**
   support "tempering is needed for discovery": on LH a single greedy search from S̃₀ (LS0) does the job, and LS0 is the
   only fully proved masked-regime route of T38. Suggested wording: "Theorem SEP: no method that samples from the start
   and reweights can find or weight the truth with fewer than p^c n^{c/2} draws; v3 does it at polynomial cost of fixed
   degree, by moving off the start." Avoid "the sampler is needed" unless "sampler" means "moves".
4. **LH-iid (p ≫ n) version of GU.** PROOF SKETCH (PROOF §4.2 Remark 2); depends on W3-PXN being verified.

## 7. Outside scope

- **A possible no-LS0 route for T38(b) via GU.** v3's own final local search starts at the running best Ŝ_pre. If
  Ŝ_pre ⊆ R (or GU extends to centres with a bounded number of nulls), GU makes the final search score S₀ on LH without
  LS0, for every c. Whether Ŝ_pre ⊆ R w.p. → 1 is not checked (W1-T38E E1 shows some state outside 𝓡_d beats S°, but
  it may still lie in 2^R). CONJECTURE; worth one task.
- **GU answers W1-T37R Conjecture C4** (TD′_∞ without PGD on an enlarged region) in the exact-Gram isolated-R case, with
  the region all of 2^R.
- In the study's S4/S6 at n = 200 the start mode is 12–14 moves from S₀ (W3-PXN §5) with ℓ = 10–11, so the move limit,
  not a barrier, is what stops LS0 there.

## 8. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| SEP (A) iid discovery threshold | P(hit) → 0/1 as Q/Q* → 0/∞, Q* = p^c n^{c/2} (LH exact Gram) | 0.97 | done (PROVED, candidate) | two-sided T27 law (W1-EXP Thm 5(b), verified) | no |
| SEP (A) on LH-iid (p ≫ n) | same | 0.92 | done given W3-PXN P4 | W3-PXN verification | no |
| SEP (B) importance correction | χ² ≥ Q*e^{O_P(1)}; Î = 0 w.p. → 1 below Q* | 0.98 | done (PROVED; overlaps O-WSTAB WS7) | none | no |
| Task's (a) with local search | "start + LS fails unless basin ∋ S̃₀" — the exception holds w.p. → 1 on LH | false as a separation (COUNTEREXAMPLE) | n/a | Cor. GU-LH | no |
| Prop. GU (exact Gram, isolated R) | search from every C ⊆ R scores and certifies S₀ | 0.93 | done (PROVED, candidate; needs cross-family check) | GU-1(b) descent bound + Lemma M | no |
| GU on LH-iid / general SE designs | same, with sample-correlated nulls | 0.85 | 0.6 | union over nulls' sample correlations; NA for data-chosen nulls | no |
| SEP (C) v3 succeeds | T38(b1-LH) with LS0; BG1 without | 0.9 (LS0) / 0.75 (BG1) | done / 0.5 | Lemma M, LH-LAT / BG1 score estimates | LS0 (b1) or none (BG1) |
| Exponent separation iid vs v3 | iff c ≥ 2 (p ≍ n^a) | 0.9 | done given T32 | T32(i) is a CONJECTURE | no |
| Super-polynomial separation in R1 | — | false (c fixed ⇒ Q* polynomial) | n/a | — | — |
| Bridge-vs-search separation in R1 + SE + fixed signals | — | false on exact-Gram isolated-R families (GU); conjecturally false in general | n/a | a separation needs a posterior barrier, i.e. leaving R1/SE | would need a different target |

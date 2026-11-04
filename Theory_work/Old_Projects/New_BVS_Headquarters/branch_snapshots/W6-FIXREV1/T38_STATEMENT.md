# T38: consistency of the reported HPM — corrected statement (supersedes W4-T38FULL/T38_STATEMENT.md)

Run W6-FIXREV1, 2026-11-02, branch `theory/W6-FIXREV1`. This is a **candidate**. It applies the cross-family review
A-REV1 (`theory/A-REV1:theory_campaign/A-REV1/REVIEW.md`, cited [AR]) to W4-T38FULL's statement, and it has not been
reviewed after these edits. The proof is in `T38_PROOF.md`. The other corrected ingredients (Prop. U′, Theorem B
conventions, Lemma S′, D2-∞ with rates, E3′, Lemma U, NL0, CE1-narrow) are in `CONSOLIDATED.md` (cited [CON]).
Notation follows `Docs/Theory/theorems/00_COMMON.md`. Status words follow `theory_campaign/PROTOCOL.md`.

## Part 0. Change log relative to W4-T38FULL

| # | Where (W4) | Change | Source |
|---|---|---|---|
| S1 | Objects: "𝒪 = {exact, completed}, U := 𝒪ᶜ" | Kept, and made explicit: `schedule_limit` and `numerical_failure` return a best-scored model, but they are in U under the **strict convention**. A second convention 𝒪_H ("any reported HPM") is added, with its extra discovery term (part (0_H)). Partial returns after a guard stop are always in U. | [AR] §7.3 |
| S2 | Operational hypotheses | GUARD is spelled out as (G1) the guard consumes no randomness and changes no setting, and (G2) a run that no guard check stops is the R̄ computation. **STATUS** (completed ⇒ every designated round, scan and LS0 executed) is now derived from GUARD and R̄, not assumed separately. No probability is conditioned on completion. | [AR] §7.3, W2-BOOK Lemma RO |
| S3 | Setting | K = min(p, ⌊n/2⌋), not ⌊n/2⌋. | [AR] §7.3 |
| S4 | Route (b1′) | The hypotheses are now the D2-∞ rate margins: fixed b₀ > 1/10, bounded k_D, Dep ≤ 1 − c₀ with fixed c₀ > 0 on events of probability → 1, and P(NB′ᶜ) → 0. A general-rate version is given. The execution qualification is the potential first tier-0 pilot stage. | [AR] §7.1 |
| S5 | Route (b2) | The eligible-set interface is made explicit. 𝔛_n is data-measurable, and each state carries a **repair certificate** (Theorem B, B′ or B♯ family, with s₀ + a(x) ≤ K). β_H is the capped quantity of [CON] §2. The boundary is fixed at 𝔉_T (after stage-T resampling, before the stage-T round), with H′ = L + 5. DELIV is delivery **to 𝔛_n**, not to 𝓡_d. A single-particle form (the eligible particle with the smallest β, ties by index) needs only the Markov part IND-T(b), not the product part IND-T(a). The sufficient statistical inputs are named (bounded v, c_* ≥ c > 0, (L+5)η → 0, with NL0 in the Λ₂ form). | [AR] §7.2 |
| S6 | Part (0) proof | The "T11(vii)" citation is replaced by the direct set argument (locked T21(C1)). The two-sided form "P(𝒪, Ŝ⁺ = S₀) − (1 − P(U)) → 0" is added. | [AR] §8 |
| S7 | Part (c) | The LS0 term is 1 + (ℓ+1)·max_{k≤K}[p + k(p−k)]. The 1 is the emitted centre. | [AR] §6 |
| S8 | Dependency map | The A-REV1 verdicts are entered. Lemma S′ attainment is restricted to f > 1 − e. E3(ii) carries q < 1 and is not used. Prop. U′ replaces Prop. U. CE1 is narrowed. Lemma U's constant is 0.51/c_E. NL0 uses the Λ₂ form. Items A-REV1 did *not* review are marked. | [AR] §§2–5 |
| S9 | Route (b1) | No change in substance. The b1 sufficient condition never uses E3(ii). It uses E3′(i) together with W1-EXP Thm 6 / Thm 5(a), which carry u < 1. The centre emission and completed scans are stated in OP-LS0. | [AR] §§3.3, 6 |

Nothing in Part 0 changes part (a), Theorem b1, Lemma LS-score, Lemma M, Proposition LH-LAT or Corollary b1-LH, apart from
S3 and S6.

---

## Part I. The theorem

### Objects

- **Potential uninterrupted run.** R̄ is the record the method produces under EX-A with the preflight and the in-run
  guard removed (W2-BOOK §0.1). Its status is st̄ ∈ {exact, completed, schedule_limit}. `numerical_failure` does not occur
  under EX-A, and valid input excludes the remaining statuses. On the SMC branch, {st̄ = completed} = 𝒜, the calibration
  success event.
- **Actual run.** The actual status st and outputs are functions of (R̄, Ξ), where Ξ is the operational element
  (allocation, clock, load). 𝒢 := {st = resource_limit} is the stop event, from preflight or in-run guard.
- **Output events.**
  - *Strict convention (default):* 𝒪 := {st ∈ {exact, completed}} and U := 𝒪ᶜ. A `schedule_limit`,
    `numerical_failure` or guard-partial return counts as **no output**, even though it may carry a best-scored model.
  - *HPM convention:* 𝒪_H := {an HPM is reported and st ≠ resource_limit} and U_H := 𝒪_Hᶜ. Under EX-A and GUARD,
    𝒪_H = 𝒢ᶜ ∩ {st̄ ∈ {exact, completed, schedule_limit}}.
  - A bar marks the R̄ counterpart: 𝒪̄ := {st̄ ∈ {exact, completed}}, 𝒪̄_H := {st̄ ∈ {exact, completed, schedule_limit}}.
- **Scored sets.** 𝒮 is every model the method scored: tables, initial draws, the pilot, calibration, final rounds
  (both Gibbs configurations, rejected proposals) and local-search scans. With LS0, 𝒮⁺ := 𝒮 ∪ 𝒮_LS0; otherwise 𝒮⁺ := 𝒮. Ŝ⁺
  is the best model in 𝒮⁺ under the method's total order. 𝒮_cal ⊆ 𝒮 is the calibration part, and 𝒮̄, 𝒮̄⁺, Ŝ̄⁺ are the R̄
  versions.
- **LS0.** One extra production local search (M §6.10), centred at the start mode S̃₀ = argmax π₀. S̃₀ is computed exactly
  by max-plus convolution of the block tables, with a deterministic tie rule. **The centre is the first evaluation and is
  offered to the HPM** (`emit_centre = true`, or an equivalent explicit ledger insertion). Every scan is completed. LS0 is
  a deterministic function of the data. R̄⁺ is R̄ followed by LS0.
- **Geometry.** K = min(p, ⌊n/2⌋) and Ω = {S : |S| ≤ K}. Φ(S) := |S Δ S₀|. For S° = U° ∪ P° (U° ⊆ S₀, P° ∩ S₀ = ∅),
  Lat(S°) := {U′ ∪ P′ : U° ⊆ U′ ⊆ S₀, P′ ⊆ P°}. A progress neighbour of S is a flip or swap neighbour T with
  Φ(T) < Φ(S). Δ(T) := ‖(I − P_T)μ‖²/(n−1).
- **Terminal boundary.** For a final island, 𝔉_T is the σ-field of the data, 𝓒, and the island streams up to the end of
  the stage-T resampling. After it come H′ = L + 5 rounds at φ = 1: the stage-T round, L burn-in and 4 measured rounds.
  There is no reweighting or resampling in between. X_{r,i} denotes the state of particle i of island r at 𝔉_T.
- **Repair certificate** ([CON] §2). For a state x ≠ S₀, a certificate is a data-measurable choice (it may depend on
  S₀ and on (X, y), and is fixed before the algorithm's randomness) of one of the following:
  - [B]'s family 𝓕(x), with a look-alike set A(x);
  - [PREM]'s 𝓕♯(x), with a monotone look-alike map 𝔄.

  It must satisfy s₀ + a(x) ≤ K. The certificate determines v(x), c_*(x) (any of c_*, c′_*, c_*♯ with its own family) and
  η(x). Set β_H(x) := min{1, P(Bin(H, c_*⁺(x)) < v(x)) + H·η(x)} and β_H(S₀) := 0.

### Hypotheses

**Operational (all routes).**
- EX-A, EX-S, CAL: declared idealisations.
- SR: both Gibbs configurations and every proposal are scored. This is an implementation fact.
- **GUARD** (implementation fact, W2-BOOK §0.1):
  - (G1) the resource guard reads only the clock, consumes no random number and changes no setting;
  - (G2) a run that no guard check stops performs exactly the R̄ (or, with LS0, R̄⁺) computation.

  Hence on 𝒢ᶜ, st = st̄ and every reported output equals its R̄ version (Lemma RO).
- OP-LS0 (route b1 only): LS0 is executed, with its centre emitted and its scans completed, on every fit counted as
  output (𝒪 under the strict convention; 𝒪_H under the HPM convention). Post hoc execution is allowed. A stopped LS0 is
  counted in U.

**Posterior (all routes).** (P): δ₁ := 1 − π(S₀) → 0 in P₀-probability, along a triangular array R1 (s₀ fixed,
p_n ≤ n^A). Sufficient: locked T03 (G, R, SE, BM-C or BM-∞), or T03♯ (G, R, SE_λ(j₀), SE_w(m♯_n; g₀), BM).

**Route (a), favourable.** (F): 1 − π₀(S₀) → 0 in probability. Sufficient: (F1) locked T22(iii) with EXP′ discharged
(G, R, SE-blk, VIS, NL_η, NL_avg(κ)); (F2) G, R, SE-blk, BO, BM-blk; (F3) G, R-lite, SE-blk, ZL(S₀), SPREAD, VIS-lin(S₀).

**Route (b1), LS0.** There is a deterministic reference S° ∈ 𝓡_d with Φ(S°) ≤ φ̄ (d, φ̄ fixed) such that:
- (M1) ELIG(S°): P₀(π₀(S°) > ½) → 1. (By E3′(i), S̃₀ = S° on this event.) Sufficient: W1-EXP Thm 6 at S° (G, R-lite,
  SE-blk, ZL(S°), SPREAD, VIS-lin(S°)), which applies T22(i-a,b) under u < 1. **Do not establish (M1) through the printed
  E3(ii) without q < 1** ([CON] §6).
- (M2) POP-LAT(S°, m_n): for every S ∈ Lat(S°) with Φ(S) ≥ 2, some progress neighbour A_S satisfies
  Δ(B) − Δ(A_S) ≥ m_n for every non-progress neighbour B of S and for B = S. Here m_n ≥ M_n√(log n/n) with M_n → ∞.
- (M3) λ_min(R_{S°∪S₀}) ≥ φ₀² > 0 and ‖μ‖²/n ≤ M.
- OP-LS0.

**Route (b1′), D2, no method change.** x°_n and 𝒟_n are data-measurable, x°_n ∈ Ω and x°_n Δ S₀ = {j_n}. Either:
- **(fixed margins)** there are fixed b₀ > 1/10, k_D < ∞ and c₀ ∈ (0,1] with
  P₀(π₀(x°_n) ≥ b₀, |𝒟_n| ≤ k_D, Dep_n ≤ 1 − c₀) → 1 (Dep_n as in D2-c, computed at x°_n off 𝒟_n ∪ {j_n});
- **or (general rates)** the rate conditions of [CON] §5 (H₀t_n² → ∞ and H₀β_ng(b_n − t_n) → ∞ in probability).

In both cases also P(NB′ᶜ) → 0, where NB′ = {S₀ is among the initial pilot draws} ∪ {the ESS of e^{d(X_i)/T_e} over the
initial tier-0 pilot draws is ≥ 0.9H₀}. A sufficient condition for NB′ is a d-range ≤ T_e·log r*, with
r* = (11 + 2√10)/9.

**Route (b2), Gibbs path, no method change.** There is a data-measurable eligible set 𝔛_n ⊆ Ω such that every
x ∈ 𝔛_n∖{S₀} carries a repair certificate, and:
- **(DELIV(𝔛_n))** P(SMC ∩ 𝒜 ∩ {no final-run particle of any island lies in 𝔛_n at 𝔉_T}) → 0;
- **(REP(𝔛_n))** E[1_𝒜 1{N_𝔛 ≥ 1}·min_{(r,i): X_{r,i}∈𝔛_n} β_{L+5}(X_{r,i})] → 0.
  - Sufficient: sup_{x∈𝔛_n} β_{L+5}(x) → 0 in P₀-probability.
  - Sufficient for that: on events of P₀-probability → 1, sup_{𝔛_n} v ≤ v̄, inf_{𝔛_n} c_* ≥ c > 0, and
    (L+5)·sup_{𝔛_n} η → 0.
  - The η-premises must be in the sum-over-labels-of-sups form; for example NL0 is Λ₂(a) = Σ_l sup_W o_l(W)
    ([CON] §8).
- Alternatively (product form): E[1_𝒜 ∏_{(r,i): X_{r,i}∈𝔛_n} β_{L+5}(X_{r,i})] → 0 (uses IND-T).

### Theorem 5 (T38). Two-regime consistency of the reported HPM

Assume EX-A, EX-S, CAL, SR, GUARD and (P), on R1 with the v3 budgets indexed by n.

**(0) Composition (strict convention), for every n:**

  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n,   D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}).

If D_n → 0, then P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0. Since also P(𝒪 ∩ {Ŝ⁺ = S₀}) ≤ P(𝒪) = 1 − P(U),

  P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U)) → 0;   in particular liminf_n P(𝒪, Ŝ⁺ = S₀) = 1 − limsup_n P(U),

and P(𝒪, Ŝ⁺ = S₀) → 1 − u whenever P(U) → u. Recovery with probability → 1 additionally requires P(U) → 0, which this
theorem does not provide.

**(0_H) Composition (HPM convention):**

  P(𝒪_H ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n + D_n^{sl},   D_n^{sl} := P(SMC ∩ 𝒜ᶜ ∩ {S₀ ∉ 𝒮_cal ∪ 𝒮_LS0}),

with 𝒮_LS0 := ∅ without LS0. D_n^{sl} is the usable-but-unexecuted term. On 𝒜ᶜ the final run is never launched, and the
scored set is the calibration's.

**(a) Favourable regime.** Under (F), D_n → 0 with or without LS0. Under the HPM convention, D_n^{sl} ≤ P(SMC ∩ 𝒜ᶜ)
must be added, and nothing here makes it vanish.

**(b) Masked regime** (π₀(S₀) → 0 allowed). D_n → 0 under any one of the following:
- **(b1)** (M1), (M2), (M3), G and OP-LS0, with LS0 used. On these events S̃₀ = S°, and LS0 scores S₀ within Φ(S°) − 1
  moves (once ℓ_n ≥ Φ(S°) − 1). Under the HPM convention, D_n^{sl} → 0 as well, because OP-LS0 covers schedule_limit
  outputs.
- **(b1′)** the D2 route hypotheses. Then the potential first stage of the tier-0 pilot scores S₀. No method change is
  needed, and Ŝ⁺ = Ŝ. Under the HPM convention, D_n^{sl} → 0 as well, because 𝒮_cal contains the pilot.
- **(b2)** DELIV(𝔛_n) and REP(𝔛_n) (either form). No method change is needed. Under the HPM convention, D_n^{sl} ≤
  P(SMC ∩ 𝒜ᶜ) must be added.

**(b1-LH)** On the linked-hub family LH in exact Gram (X′X = (n−1)Σ_LH, p ≤ n − 1, c ≥ 1 linked pairs with
0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i}), g ≤ B_n < 2g eventually, fixed nonzero coefficients), with S° = S₀ ∖ M (M the masked
hubs): (P), (M1), (M2) with a fixed margin m₀ > 0, and (M3) all hold. π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}, and
Q_fπ₀(S₀) → 0 when c ≥ 2 and p → ∞, or c = 1 and p/(√n log²n) → ∞. With LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, with no
statistical hypothesis left open.

**(c) Cost.** The number of score evaluations is bounded deterministically by T32(i)'s ceiling plus
1 + (ℓ+1)·max_{k≤K}[p + k(p−k)] for LS0. Under the v3 budgets this is O((n+p)(p+B)log²(n+p) + p²log²(n+p)).

**Not claimed.**
- P(U) → 0, or any law of 𝒢 or of calibration failure.
- Evidence or PIP accuracy in the masked regime.
- Any statement conditional on completion or on diagnostics.
- Comparative superiority.
- Finite-n error rates at n = 200.
- A masked p ≫ n family (W3-PXN's LH-iid claim is unverified).
- Masked-regime consistency without LS0 on an explicit family (OPEN).
- DELIV for any BVS family (OPEN).

### Remarks for the paper text

1. **Execution.** All discovery statements are about R̄. On R̄, the designated draws, rounds and scans execute by
   definition. GUARD transfers them to the reported output on 𝒢ᶜ, and everything else is in U. Conditioning on observed
   completion is never used, and it is not a valid repair: Lemma RO(5) and the W2-BOOK §0.3 counterexample show that it
   breaks unbiasedness.
2. **Regime discipline.** (F) and the masked instances are never combined on one sequence.
3. **Delivery is part of the theorem.** In (b1) it is S̃₀ = S° plus the lattice condition. In (b1′) it is the pilot ESS
   rule (Lemma S′, used only in the range f > 1 − e). In (b2) it is DELIV(𝔛_n), which is OPEN. COUNTEREXAMPLE C1 shows that
   start mass, bridge mass and zero exits do not imply it.
4. **H24 is not used.** Its asymptotic input (L+4)η_n → 0 fails along the explicit sequence of [CON] §9 (CE1-narrow). This
   is not claimed for every correlated design.

---

## Part II. Dependency map (inputs → sources → status)

Status labels: PROVED-LOCKED (in `LOCKED_PROOFS.md`); PROVED (campaign candidate); PROOF SKETCH; CONJECTURE; OPEN; IMPL
(implementation fact read from code); IDEAL (declared idealisation). "A-REV1:" gives the cross-family verdict where one
exists. "not cross-family reviewed" means A-REV1 did not inspect the item.

### II.1 Composition and execution

| # | Input | Source | Status | Review |
|---|---|---|---|---|
| C1 | On {π(S₀) > ½} ∩ {S₀ scored}, the running-best HPM is S₀; Markov | locked T21(C1); direct set proof T38_PROOF §1 | PROVED-LOCKED / PROVED | A-REV1 §7.4: VERIFIED as a set argument |
| RO | Lemma RO: 𝒪 = 𝒢ᶜ ∩ 𝒪̄, outputs equal R̄'s on 𝒪, no conditioning | W2-BOOK §0.2 | PROVED | not cross-family reviewed |
| GUARD | stop-only coupling (G1), (G2) | W2-BOOK §0.1 code reading | IMPL | needs an independent code check |
| HPM conv. | D_n^{sl} term | T38_PROOF §1.3 (new) | PROVED | new, unreviewed |
| P | δ₁ → 0 | locked T03(i); T03♯ (W1-T03R, VERIFIED by W2-VT03R) | PROVED-LOCKED / PROVED | — |

### II.2 Route (a)

Unchanged from W4-T38FULL II.2 (a1–a8): locked T11(iii) on R̄; locked T22(iii); W1-EXP Thms 1, 2, 6; ORTH composition.

### II.3 Route (b1)

| # | Input | Source | Status | Review |
|---|---|---|---|---|
| b1.1 | E3′(i): π₀(x°) > ½ ⇒ S̃₀ = x°; centre emitted; LS0 cost 1 + (ℓ+1)max_k[p+k(p−k)] | [CON] §6 (from W1-T38E E3) | PROVED | A-REV1: E3 core VERIFIED; (ii) ERROR as printed, now restricted to q < 1 and **not used** |
| b1.2 | Lemma LS-score | W4-T38FULL §3.1 (copied in T38_PROOF §3.1) | PROVED | same-family VERIFIED; not cross-family reviewed |
| b1.4 | Lemma M | W4-T38FULL §3.2 (copied; rechecked here) | PROVED | not cross-family reviewed |
| b1.5 | Theorem b1 | W4-T38FULL §3.3 (copied) | PROVED (implication) | not cross-family reviewed |
| b1.6 | (M1) from W1-EXP Thm 6 (uses T22(i-a,b) under u < 1) | W1-EXP | PROVED | VERIFIED (W3-VEXP) |
| b1.7 | LH exact Gram: ELIG, masking, π(S₀) → 1 | W1-EXP Thm 5 | PROVED | VERIFIED (W3-VEXP) |
| b1.8 | Prop. LH-LAT | W4-T38FULL §3.4 (copied) | PROVED | same-family VERIFIED; not cross-family reviewed |
| b1.9 | LH-iid (p ≫ n) | W3-PXN P1–P8 (uses E3(i) and T22(i-a) with q < 1 only) | PROVED (W3-PXN's claim) | unverified |
| b1.11 | TD(d,0) false for d ≥ 1 on {π(S₀) > ½} | W1-T37R Prop 1; W3-VT38E V1 | PROVED (negative) | VERIFIED |

### II.4 Route (b1′)

| # | Input | Source | Status | Review |
|---|---|---|---|---|
| d1 | Lemma S′ (inequality everywhere; attained only for f > 1−e) | [CON] §4 | PROVED | A-REV1: inequality VERIFIED; global attainment ERROR, now corrected |
| d2 | Lemma A | W1-T38E §1 | PROVED | VERIFIED |
| d3 | D2 finite, NB′, r* | W1-T38E §4 + W3-VT38E §3.1 | PROVED | A-REV1: VERIFIED as a finite uninterrupted-pilot bound |
| d3′ | D2-∞ with rate margins | [CON] §5 | PROVED (implication) | A-REV1 §7.1 repair, written out here |
| d4 | statistical instance (Dep, NB′, π₀(x°) ≥ b₀) on a masked family | W4-T38FULL §4.2 (LH, c = 1); W3-PXN P7 | D2-a,b,c: PROVED (W3-PXN's claim, unverified); NB′: PROOF SKETCH; c ≥ 2: OPEN | — |

### II.5 Route (b2)

| # | Input | Source | Status | Review |
|---|---|---|---|---|
| g1 | Theorem B / B′ / B♯ with the β_H conventions | W1-T24G §4, W2-VT24G §§1–2, W2-PREM §5.2; [CON] §2 | PROVED | A-REV1: Theorem B VERIFIED after F′; B♯ not cross-family reviewed |
| g1′ | Prop. U′ (classification with the full Bad set) | [CON] §1 | PROVED | A-REV1: Prop. U as printed ERROR, now corrected; Theorem B unaffected |
| g2 | IND-T at 𝔉_T with H′ = L + 5 | W2-PREM §1 | PROVED (EX-S, EX-A) | A-REV1: VERIFIED for the uninterrupted process |
| g3 | Cor. B-M (corrected wording), Cor. P1, Lemma P (multi-target) | W1-T24G; [CON] §§2–3 | PROVED | A-REV1: VERIFIED; the multi-target sentence was a GAP, fixed in [CON] §3 |
| g4 | **DELIV(𝔛_n)** | W1-T38E D3 (for 𝓡_d; the same proof works for 𝔛_n) under SHARE + EXIT-end with **aggregate** (1−π₀(𝔛))^{N_e} + Σ_t(ζ_t + η_t) → 0 | **OPEN** | C1 COUNTEREXAMPLE VERIFIED |
| g5 | **REP(𝔛_n)** premises: Λ₂(a) (NL0, sum of sups), UDEL, PA/B1′, TS, FS, TL♯, ULR, IND-M | W2-PREM §§3–8 | PROVED UNDER named conditions; on LH PROOF SKETCH (Theorem L) | A-REV1: NL0 quantifier GAP in W1, corrected form is W2-PREM's; W2-PREM premises otherwise not cross-family reviewed |
| g6 | H24 not used; CE1-narrow | [CON] §9 | COUNTEREXAMPLE (explicit sequence) | A-REV1 §5 repair |
| g7 | v > H makes β trivial; Hη > 1 at n = 200 | W2-VT24G §5 | PROVED (observation) | — |
| g8 | Lemma U (used inside W2-PREM): κ_n ↓ 0.51/c_E | [CON] §7 | PROVED | A-REV1: finite VERIFIED; limit constant ERROR, corrected |

### II.6 Cost

| # | Input | Source | Status |
|---|---|---|---|
| k1 | T32(i) ceiling | T32(i) | CONJECTURE (checked as a valid loose bound by W3-VT38E) |
| k2 | LS0: 1 + (ℓ+1)max_k[p + k(p−k)] score calls | [CON] §6 | PROVED |

### II.7 Method-change dependencies

As in W4-T38FULL II.8, with two corrections:
- LS0 must emit its centre as the **first** evaluation, or insert it explicitly into the ledger. Caching an un-emitted
  centre and relying on a later cache-hit emission does not update the ledger.
- The LS0 cost includes that centre call.

### II.8 What the paper can claim without LS0

Unchanged from W4-T38FULL II.9, with these edits:
- item 3 now cites the rate form of (b1′);
- item 4 cites DELIV(𝔛_n);
- item 6's "H24's asymptotic input fails" reads "fails along an explicit design sequence (CE1-narrow)".

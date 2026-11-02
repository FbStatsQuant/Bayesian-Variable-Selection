# T38: the main theorem, consistency of the reported HPM (paper-ready statement)

Run W4-T38FULL, 2026-11-02, branch `theory/W4-T38FULL`. This is a **candidate** assembled from campaign results. It has not been reviewed or adopted. The proof is in `T38_PROOF.md`; status words follow `theory_campaign/PROTOCOL.md`. Notation follows `Docs/Theory/theorems/00_COMMON.md`. The labels in brackets (for example [W1-T38E E3]) point to the dependency map in Part II.

---

## Part I. The theorem as it would appear in the main text

### Objects

- **Run and output.**
  - R̄ is the *potential uninterrupted run*: the method with the resource guard removed.
  - 𝒪 is the event that output is available, meaning status `exact` or `completed`. Write U := 𝒪ᶜ.
  - Under the stop-only coupling GUARD below, the reported outputs equal those of R̄ on 𝒪. Nothing is ever conditioned on 𝒪.
- **Scored sets and the reported model.**
  - 𝒮 is the set of all models scored by the method. This includes calibration, the final run, rejected proposals, both Gibbs configurations and local-search scans.
  - With the optional tweak **LS0**, 𝒮⁺ := 𝒮 ∪ 𝒮_LS0. Without it, 𝒮⁺ := 𝒮.
  - Ŝ⁺ is the best model in 𝒮⁺ under the method's tie rule. Without LS0, Ŝ⁺ = Ŝ.
- **LS0.** Run the production local search (M §6.10) once more, centred at the start mode S̃₀ = argmax π₀. S̃₀ is computed exactly by max-plus convolution of the block tables. The centre must itself be recorded as a scored model ("emit the centre").
- **Distance to the truth.** Φ(S) := |S Δ S₀|.
- **Lattice.** For a reference S° = U° ∪ P° (U° ⊆ S₀, P° ∩ S₀ = ∅), Lat(S°) := {U′ ∪ P′ : U° ⊆ U′ ⊆ S₀, P′ ⊆ P°}.
- **Progress neighbours.** A flip or swap neighbour T of S is a *progress* neighbour if Φ(T) < Φ(S). These are: adding a missing truth, deleting an extra, or swapping an extra for a truth.
- **Population residual.** Δ(T) := ‖(I − P_T)μ‖²/(n−1). Under G this is a deterministic function of the fixed design.

### Hypotheses (grouped; each one's status is in Part II)

**Operational (all routes).**
- **EX-A, EX-S, CAL** are declared idealisations.
- **SR**: both Gibbs configurations are scored. This is an implementation fact.
- **GUARD**: the resource guard is a stop-only coupling to R̄. This is an implementation fact.

**Posterior (all routes).**
- **(P) H-T03**: δ₁ = 1 − π(S₀) → 0 in P₀-probability, on a triangular array R1 (s₀ fixed, p_n ≤ n^A).
- Sufficient for (P): either the locked hypotheses of T03 (G, R, SE, BM-C or BM-∞), or those of T03♯ (G, R, SE_λ(j₀), SE_w(m♯_n; g₀), BM).

**Favourable regime (route a).**
- **(F)** 1 − π₀(S₀) → 0 in probability. Sufficient for (F):
  - **(F1)** the locked T22(iii) hypotheses with EXP′ discharged: G, R, SE-blk, VIS, NL_η, NL_avg(κ);
  - **(F2)** G, R, SE-blk, BO, BM-blk;
  - **(F3)** G, R-lite, SE-blk, ZL(S₀), SPREAD, VIS-lin(S₀).

**Masked regime, route (b1): LS0.** There is a *deterministic* reference S° ∈ 𝓡_d, with Φ(S°) bounded, such that:
- **(M1) ELIG(S°)**: P₀(π₀(S°) > ½) → 1.
  - Sufficient: G, R-lite, SE-blk, ZL(S°), SPREAD, VIS-lin(S°), using W1-EXP Theorem 6 at the reference S°.
- **(M2) POP-LAT(S°, m_n)**: for every S ∈ Lat(S°) with Φ(S) ≥ 2, some progress neighbour A_S of S satisfies Δ(B) − Δ(A_S) ≥ m_n.
  - This must hold for every non-progress neighbour B of S, and for B = S.
  - The margin must satisfy m_n ≥ M_n √(log n / n) with M_n → ∞.
- **(M3)** λ_min(R_{S° ∪ S₀}) ≥ φ₀² > 0, and ‖μ‖²/n ≤ M.
- **(OP-LS0)** LS0 is executed, with its centre emitted, whenever output is available.

**Masked regime, route (b1′): D2, no method change.** For a one-flip reference x° = S₀ ⊕ j, the hypotheses of Theorem D2 hold with probability → 1:
- π₀(x°) ≥ b > 1/10;
- Dep ≤ 1 − c₁ off a data-measurable set 𝒟 with |𝒟| ≤ k_D;
- P(NB′ᶜ) → 0, with the corrected constant r* = (11 + 2√10)/9.

**Masked regime, route (b2): Gibbs path, no method change.** There is a data-measurable eligible set 𝔛_n such that:
- **(DELIV)** the final run of R̄ has, with probability → 1 on 𝒪̄, at least one particle in 𝔛_n after its last resampling;
- **(REP)** sup_{x ∈ 𝔛_n} β_{L+5}(x) → 0 in probability, where β_H(x) := P(Bin(H, c′_*(x)) < v(x)) + H·η(x) is the Theorem B′ bound.

### Theorem 5 (T38). Two-regime consistency of the reported HPM

Assume EX-A, EX-S, CAL, SR, GUARD and (P), on a triangular array R1 with the v3 budgets indexed by n.

**(0) Composition, for every n.**

  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}).

Hence, whenever the discovery term tends to 0,

  **P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and therefore liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − limsup_n P(U).**

The first form is the stronger one: it says P(𝒪 ∩ {Ŝ⁺ = S₀}) = P(𝒪) − o(1).

**(a) Favourable regime.** Under (F), the discovery term tends to 0 with or without LS0. The reason is that the final run's Q_f ≥ 4N_e(L+6) iid π₀ draws score S₀ (T11(iii)).

**(b) Masked regime.** Here π₀(S₀) → 0 is allowed, at the T27 rate p^{−c} n^{−c/2}. The discovery term tends to 0 under any one of the following routes.
- **(b1)** (M1), (M2), (M3), (OP-LS0) and G, with LS0 used. On these events S̃₀ = S°, and LS0 scores S₀ after at most Φ(S°) − 1 moves. The cap only needs ℓ_n ≥ Φ(S°) − 1.
- **(b1′)** The D2 hypotheses. Then the *first stage of the tier-0 pilot* scores S₀. No method change is needed, and Ŝ⁺ = Ŝ.
- **(b2)** (DELIV) and (REP). No method change is needed.

**(b1-LH) An explicit family on which every premise of (b1) holds jointly.**
- **The family.** The linked-hub family LH in its exact-Gram realisation (W1-EXP §4.1–4.2):
  - X′X = (n−1)Σ_LH and p ≤ n − 1;
  - c ≥ 1 linked hub pairs, with |ψ_i| < min(ρ_{a_i}, ρ_{b_i}) and ψ_i ≠ 0;
  - g ≤ B_n < 2g eventually;
  - fixed nonzero coefficients.
- **The reference.** S° = S₀ ∖ M, where M is the set of the c masked hubs.
- **What holds.** On LH:
  - (P), (M1), (M2) (with a fixed margin m₀ > 0) and (M3) all hold;
  - π₀(S₀) = p^{−c} n^{−c/2} e^{O_P(1)};
  - Q_f π₀(S₀) → 0 for c ≥ 2, and also for c = 1 when p/√n → ∞. So route (a) does not apply.
- **Conclusion.** With LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, with no statistical hypothesis left open.

**(c) Cost.** The number of score evaluations is bounded deterministically by T32(i)'s ceiling, plus (ℓ+1)·max_{k≤K}[p + k(p−k)] for LS0. Under the v3 budgets this is O((n+p)(p+B)log²n + p²log²n), which is polynomial in n under R1.

**Not claimed.**
- Evidence or PIP accuracy in the masked regime.
- Any statement given completion, or for fits selected on diagnostics.
- Comparative superiority over other methods.
- Any finite-n error rate at n = 200.
- A masked p ≫ n family; that is CONJECTURE.
- Masked-regime consistency **without LS0** on any explicit family; that is OPEN.

### Remarks for the paper text

1. **Regime discipline.** (F) and the masked instances are never combined on one sequence. On LH, VIS fails at the reference S₀ (W1-EXP Thm 5(c)), so (F1)–(F3) fail there.
2. **Delivery is part of the theorem.**
   - In (b1), delivery is the start-side event S̃₀ = S°, plus the lattice progress condition on Lat(S°).
   - In (b1′), delivery is the pilot's ESS rule (Lemma S).
   - In (b2), delivery is the open input DELIV.
3. **Why LS0.** Without LS0, the final local search starts at the running HPM. It can deliver S₀ only on E_LS = {F(S₀) > F(centre)} (W1-T37R Lemma 0, repaired in W3-VT37R R2). Moreover, the natural eligibility condition fails with probability → 1 under omission masking (W1-T38E E1). LS0 turns eligibility into a deterministic property of the start law.
4. **n = 200.** At n = 200 the theorem is a statement about mechanism, not about the study's numbers:
   - the start is dilution-masked (W3-VEXP Prop. D);
   - the misses are posterior misses (THEORY_PRIORITIES §5);
   - the deterministic thresholds of the T03 proof start near n ≈ 2×10⁶ (W2-VT03R R1).

---

## Part II. Dependency map (inputs → sources → verification status)

Status words used in this table:
- **PROVED-LOCKED**: in `LOCKED_PROOFS.md`; reviewed and not adopted.
- **PROVED**: a complete campaign proof. The verifier is named when there is one.
- **PROVED-UNDER [X]**: complete, given the named input X.
- **PROOF SKETCH**, **CONJECTURE**, **OPEN** as in the protocol.
- **IMPL**: an implementation fact read from the code, not a theorem.
- **IDEAL**: a declared idealisation.

"VERIFIED (W…)" means that a single adversarial verifier from the same model family checked the result line by line. Every campaign item is still a candidate pending cross-family review.

### II.1 Composition and posterior side (all routes)

| # | Input used by T38 | Where used | Source (proof label) | Status | Verification |
|---|---|---|---|---|---|
| C1 | P(𝒪, Ŝ⁺≠S₀) ≤ 2E₀δ₁ + P(𝒪̄, S₀∉𝒮̄⁺): strict maximiser when π(S₀) > ½, plus Markov | (0) | locked T21 (C1); re-derived in [W1-T38E §7 step 1]; GUARD form [W2-BOOK Thm 4 (C1)] | PROVED-LOCKED (T21); PROVED (W1 re-derivation) | locked review chain; VERIFIED (W3-VT38E) |
| RO | Lemma RO: run/output split, no conditioning on completion | (0), all routes | [W2-BOOK Lemma RO] | PROVED | single run; set inclusions only |
| GUARD | the resource guard is stop-only and touches no RNG or setting | (0) | [W2-BOOK §2, code reading of `v3_runtime.h`, `v3_engine.h`, `v3_core.cpp`] | IMPL | needs an independent code check (W2-BOOK escalation 1) |
| P | δ₁ → 0 | (0) | locked T03(i) under G, R, SE, BM-C/BM-∞ (H-T02 closed by locked T02(i)); or T03♯ [W1-T03R] under G, R, SE_λ(j₀), SE_w(m♯; g₀), BM | PROVED-LOCKED / PROVED | T03 locked (external review queued); T03♯ VERIFIED (W2-VT03R), with threshold correction R1 and wording R2 |
| P′ | SE_λ(j₀) can be replaced by SIG(c) | optional weakening | [W2-VT03R Prop. W] | PROOF SKETCH | — |
| EX | EX-A, EX-S, CAL | all | 00_COMMON | IDEAL | — |
| SR | both Gibbs configurations are scored | (b1′), (b2) | `step_gibbs` (held + eval) | IMPL | confirmed in code by W3-VT38E and W2-VT24G; Felipe's confirmation still pending |

### II.2 Part (a): favourable regime

| # | Input | Source | Status | Verification |
|---|---|---|---|---|
| a1 | P(output, S* ∉ final draws ∣ 𝓒) ≤ (1−π₀(S*))^{Q_f} | locked T11(iii), with the R̄ statement edit of [W2-BOOK §2] | PROVED-LOCKED | locked |
| a2 | T22(iii): 1 − π₀(S₀) = O_P(2^B √(log n) n^{−κ}) | locked T22(iii) | PROVED-LOCKED, CONDITIONAL on EXP′, VIS, NL_η, NL_avg(κ) | locked |
| a3 | EXP′ holds under G, R-lite, SE-blk (removes EXP′ from a2) | [W1-EXP Thm 1]; finite-n certificate [W3-VEXP R1] | PROVED | VERIFIED (W3-VEXP) |
| a4 | (F2): BO + BM-blk ⇒ (F) | [W1-EXP Thm 2] = verbatim corollary of a2 + a3 | W1 status word: PROOF SKETCH (kept, not upgraded); the composition was rechecked in T38_PROOF §2 | VERIFIED as a corollary (W3-VEXP R2) |
| a5 | (F3): ZL, SPREAD, VIS-lin ⇒ 1−π₀(S°) = O_P(2^B n^{−1/2}) | [W1-EXP Thm 6] | PROVED | VERIFIED (W3-VEXP) |
| a6 | joint family for (a) + (P): ORTH (X′X = (n−1)I, p ≤ n−1, fixed θ) | T38_PROOF §2.3 (composition of a2, a3, locked T03) | PROVED-UNDER the verified a3 | composition new here, unreviewed |
| a7 | study relevance: favourable only for n ≳ 800–1600 (S3, p = 500); the start is dilution-masked at n = 200 | [W3-VEXP Prop. D] (PROVED); threshold (PROOF SKETCH) | PROVED / PROOF SKETCH | single run |
| a8 | in-sample favourable regime for iid S1/S3/S4/S6 designs | [W3-VEXP row 24] | GAP; CONJECTURE (partition–noise decoupling) | — |

### II.3 Part (b1): LS0 route

| # | Input | Source | Status | Verification |
|---|---|---|---|---|
| b1.1 | LS0 eligibility: π₀(x°) > ½ ⇒ S̃₀ = x°; S̃₀ is exactly computable; cost ≤ (ℓ+1)max_k[p+k(p−k)] | [W1-T38E Thm E3] | PROVED | VERIFIED (W3-VT38E) |
| b1.2 | **Lemma LS-score**: if D_S holds on Lat(C₀) ∩ {Φ ≥ 2} and ℓ ≥ Φ(C₀) − 1, the search from C₀ scores S₀ | T38_PROOF §3.1 (new; scoring-only version of [W1-T37R Thm A(A3), lattice form]) | PROVED | new here, unreviewed |
| b1.3 | Theorem A (refined T37(i)): TD′_∞ / TD′_P / lattice; A5 with POS | [W1-T37R Thm A]; repair [W3-VT37R R1] | PROVED | VERIFIED (W3-VT37R, exhaustive 720 designs) |
| b1.4 | **Lemma M**: uniform score comparison under population margins m_n ≫ √(log n/n) | T38_PROOF §3.2 (new; it reuses [W1-T38E E1(a)(b)] and the RSS-floor idea of [W1-EXP Lemma 1.4]) | PROVED | new here, unreviewed |
| b1.5 | **Theorem b1**: (M1)–(M3) + OP-LS0 ⇒ P(S₀ ∉ 𝒮⁺) → 0 | T38_PROOF §3.3 | PROVED-UNDER (M1)–(M3) | new here, unreviewed |
| b1.6 | (M1) from Thm 6 at S° | [W1-EXP Thm 6] | PROVED | VERIFIED (W3-VEXP) |
| b1.7 | LH, exact Gram: (M1) S̃₀ = S° w.p. → 1; masking; π(S₀) → 1 | [W1-EXP Thm 5(a)(b)(d), Lemmas 4.1, 4.2] | PROVED ((d) by locked T03; limit law PROOF SKETCH) | VERIFIED (W3-VEXP); the |ψ| < ρ boundary is sharp in effect (W3-VEXP row 17) |
| b1.8 | **Prop. LH-LAT**: POP-LAT(S°, m₀) holds on LH with an explicit m₀ > 0 | T38_PROOF §3.4 (new; population algebra from Lemma 4.1) | PROVED | new here, unreviewed; numerics `scripts/lh_ls0_check.txt` |
| b1.9 | LH-iid realisation (p > n allowed) | [W3-VEXP R3] for the start; POP-LAT in sample not done | PROOF SKETCH (start); CONJECTURE (POP-LAT, p ≫ n) | W3-PXN in progress (interim scripts only) |
| b1.10 | general sufficient condition for (M2): TD′_P(R_{a,d}) w.p. → 1 under PGD + LD* | [W1-T37R Thm C] with repairs [W3-VT37R R4, R5] | PROOF SKETCH | VERIFIED as a sketch after repair; PGD fails under SE + BM-∞ (COUNTEREXAMPLE C3) |
| b1.11 | literal TD(d,0) is false for d ≥ 1 on {π(S₀) > ½} | [W1-T37R Prop 1]; [W3-VT38E Prop. V1] | PROVED (negative) | VERIFIED |
| b1.12 | eligibility without LS0: the brief's sufficient condition fails | [W1-T38E Prop. E1] | PROVED (deterministic); margin PROOF SKETCH | VERIFIED (W3-VT38E) |
| b1.13 | LS0 must emit its centre; tie rule for argmax π₀ | [W3-VT38E §4, escalation 3] | IMPL caveat | — |

### II.4 Part (b1′): D2 route

| # | Input | Source | Status | Verification |
|---|---|---|---|---|
| d1 | Lemma S (ESS share, tight); ESS non-increasing in φ | [W1-T38E §3] | PROVED | VERIFIED (W3-VT38E) |
| d2 | Lemma A (Gibbs change probability ≤ max endpoint odds) | [W1-T38E §1] | PROVED | VERIFIED (2,048,000 cases) |
| d3 | Theorem D2 with NB′ and r* = (11+2√10)/9 | [W1-T38E §4] + repair [W3-VT38E §3.1] | PROVED | VERIFIED after the constant repair |
| d4 | D2's statistical instance (Dep < 1 − c₁, NB′, π₀(x°) > 1/10 w.p. → 1) on a masked family | T38_PROOF §4.2 (sketch on LH, c = 1) | PROOF SKETCH (LH, c = 1, p/√n → ∞); otherwise CONJECTURE | — |
| d5 | pilot engine facts (pilot_next_phi, order, resampling) | [W3-VT38E §4] | IMPL | faithful |

### II.5 Part (b2): Gibbs-path route

| # | Input | Source | Status | Verification |
|---|---|---|---|---|
| g1 | Theorem B′ (restated T24): P_x(S₀ unscored in H rounds) ≤ β_H(x) | [W1-T24G Thm B] + [W2-VT24G Lemma F′, Props B1′/B2′] | PROVED | VERIFIED after the Lemma F′ repair (W2-VT24G) |
| g2 | IND-T: terminal trajectories are conditionally independent; H′ = L+5 | [W2-PREM Thm IND-T]; [W2-VT24G (R5)] | PROVED (under EX-S) | W2-VT24G verified (R5); the W2-PREM write-up itself is unverified |
| g3 | Cor. B-M (product bound); Cor. P1 (distance-one) | [W1-T24G] | PROVED | VERIFIED (W2-VT24G); P1's "a₁ ≥ 0.14" is shown only at B = 4 |
| g4 | **DELIV** (a particle in 𝔛_n at terminal start) | via [W1-T38E Prop. D3] under SHARE + EXIT-end, or D1 under LT | **OPEN** (SHARE/LT). C1 COUNTEREXAMPLE: start mass + bridge mass + zero exits do not imply DELIV | C1 VERIFIED after the kernel repair (W3-VT38E §3.2) |
| g5 | **REP**: c′_* ≥ c > 0, v bounded, (L+5)η → 0 | premises NL0, UDEL, TS, TL(𝒵,A), BTP, IND-M [W1-T24G §4]; NL0/UDEL PROVED UNDER PG [W2-PREM §3]; NL0 threshold fix [W2-VT24G §4] | phase 2: PROVED UNDER PG (unverified); phase 1: PROOF SKETCH / OPEN; COUNTEREXAMPLE for equicorrelated nulls | partial; W2-PREM has no REPORT |
| g6 | H24 is retired: its asymptotic input fails | [W1-T24G CE1], [W2-VT24G Lemma E] | COUNTEREXAMPLE | VERIFIED |
| g7 | v > H makes Theorem B vacuous; Hη > 1 at n = 200 | [W2-VT24G §5] | PROVED (observation) | — |
| g8 | SHARE work | W4-SHARE | not available when this run started | — |

### II.6 Part (c): cost

| # | Input | Source | Status | Verification |
|---|---|---|---|---|
| k1 | score-evaluation ceiling of the SMC branch | T32(i) | CONJECTURE (not locked) | the formula was checked against the engine as a valid, loose upper bound (W3-VT38E) |
| k2 | LS0 term (ℓ+1)max_k[p + k(p−k)] | [W1-T38E E3] | PROVED | VERIFIED |

### II.7 One-page dependency graph

```
                         ┌──────────── T38 (0): P(𝒪, Ŝ⁺≠S₀) ≤ 2E₀δ₁ + P(𝒪̄, S₀∉𝒮̄⁺) ─────────────┐
   C1 [locked T21 / W1-T38E §7] + RO [W2-BOOK] + GUARD (IMPL)          P: δ₁→0 [locked T03 | T03♯ VERIFIED]
                                         │
          ┌──────────────────────────────┼──────────────────────────────────┬───────────────────────────┐
     (a) favourable                (b1) LS0 (method change)          (b1′) D2 (no change)        (b2) Gibbs path (no change)
  a1 T11(iii) [locked]          b1.1 E3 [VERIFIED]                  d1 Lemma S [VERIFIED]        g1 Theorem B′ [VERIFIED]
  a2 T22(iii) [locked, COND]    b1.2 LS-score [new]                 d2 Lemma A [VERIFIED]        g2 IND-T [PROVED]
  a3 EXP′ Thm 1 [VERIFIED]      b1.4 Lemma M [new]                  d3 D2 + r*, NB′ [VERIFIED]   g4 DELIV ......... OPEN
  a4 BO Thm 2 / a5 Thm 6        b1.5 Thm b1 [new; under M1–M3]      d4 instance ...... SKETCH    g5 REP ..... partial/OPEN
  a6 ORTH family [new comp.]    M1 ← Thm 6 [VERIFIED]                                            C1 cex blocks bridge-mass route
                                M2 ← Prop LH-LAT [new] | Thm C [SKETCH]
                                b1-LH: LH exact Gram, p<n — all premises PROVED
                                p ≫ n (LH-iid) ........ CONJECTURE (W3-PXN)
                                         │
                               (c) cost: T32(i) [CONJECTURE] + LS0 term [PROVED]
```

### II.8 Method-change dependencies

| Change | Needed for | Nature | Caveats |
|---|---|---|---|
| **LS0**: one extra local search from S̃₀ = argmax π₀, with its scores joined to the HPM | (b1) and (b1-LH): the only masked-regime route proved on an explicit family | deterministic; adds (ℓ+1)max_k[p+k(p−k)] scores; can be added post hoc because the HPM can only improve | (i) it **must emit its centre as a score event** (`local_search(…, emit_centre = true)`), otherwise S̃₀ is not scored, which matters when S̃₀ = S₀; (ii) fix the tie rule for argmax π₀ (for example the HPM rule); (iii) record provenance and label refitted fits; (iv) it falls under the investment rule: a pilot must show that the method still performs; (v) at n = 200, LS0 cannot fix posterior misses |
| none | (a), (b1′), (b2) | — | (b1′) is proved only conditionally on D2's statistical instance; (b2) only conditionally on DELIV (OPEN) |
| T39 (repair tracks) | not needed if LS0 is accepted | method extension | stays a contingency |

### II.9 What the paper can claim **without** LS0

1. **(0) in full.** P(𝒪 ∩ {Ŝ ≠ S₀}) ≤ 2E₀δ₁ + P(𝒪̄, S₀ ∉ 𝒮̄). This is PROVED and holds for every n.
2. **Theorem 5(a).** Favourable-regime consistency is PROVED-UNDER (F1), or under the checkable (F2)/(F3). It holds unconditionally on the ORTH family (a6).
3. **Theorem 5(b1′).** If a one-flip neighbour of S₀ carries start mass > 1/10, the pilot's first stage scores S₀ w.p. → 1. This is PROVED given D2's design conditions (Dep, NB′). It is not proved on any explicit masked family; a sketch exists for LH with c = 1.
4. **Theorem 5(b2)** is conditional on DELIV, which is OPEN; C1 shows that DELIV is a genuine particle-level property.
5. **Finite-n inequalities.** These are PROVED and deterministic, but vacuous or weak at n = 200:
   - Theorem B′;
   - Cor. P1 (distance-one scoring in one round);
   - Theorem A (search from a given centre);
   - Lemma S;
   - the T21 composition.
6. **Negative results.** These are PROVED or COUNTEREXAMPLE:
   - literal TD(d,0) is false for d ≥ 1;
   - H24's asymptotic input fails;
   - start mass + bridge mass + zero exits do not imply delivery (C1);
   - the brief's eligibility condition fails under omission masking (E1).

So without LS0, the paper has **no masked-regime consistency theorem whose premises are all proved on an explicit family**.

# W3-PGD — REPORT: the asymptotic hypotheses of the refined T37 (PGD and LD)

Branch `theory/W3-PGD`. Full statements and proofs: `PROOF.md`. Scripts (fixed seeds): `scripts/`. Outputs:
`results/`. Everything here is a **candidate**: not reviewed, not adopted. Notation: `00_COMMON.md` and
W1-T37R `PROOF.md` (states R_{a,d}, progress/neutral/regressive moves, D_S, TD′_P, Theorem A, PGD, LD).

## 1. Headline

1. **PROVED (Theorem W).** TD′_P(R_{a,d}(𝒟)) holds with probability → 1 under G, R, anchored SE_λ(d+1), BM-∞,
   PGD(η) with fixed η > 0, plus one of: (H1) d ≤ 1; (H2) the admissible extras come from a deterministic set 𝒟
   with |𝒟|^{d−1} ≤ n^{1/2−ε} (e.g. the nulls in the truth blocks of the start partition, |𝒟| ≤ 15s₀); or (H3) a
   constant-threshold local-dependence condition LD♭ with (★) (1+ρ*√d)²/(1−ρ*²) < 1 + 1/(2A). Then the
   production local search returns S₀ certified from any centre in R_{a,d}(𝒟), w.p. → 1.
2. **PROVED: design conditions for PGD.** (a) PGD ⇐ GERC (a θ-free, ℓ₁/irrepresentable "greedy exact recovery
   condition" that bounds combination leakage; it is exactly the θ-uniform form of the add-null part of PGD) +
   TRC (truth retention, no masking). (b) Under block orthogonality with ≤ 1 truth per group, PGD ⇔ three
   explicit within-group/pairwise inequalities (B1)–(B3); for equicorrelated groups η* is in closed form.
   (c) PGD is sharp: a reverse margin forces TD′_P to fail w.p. → 1 (Prop P4).
3. **LD:** PROVED that it can be dropped for d = 1 and for block-local extras (H2); otherwise it can be weakened
   from κ_n log p → 0 to the constant threshold (★). **COUNTEREXAMPLE (C-LD):** for d = 2 with unrestricted
   extras it cannot be dropped (equicorrelated nulls, r > ½, p ≈ n), proved and reproduced numerically.
4. **Population check (S1–S6):** PGD holds in every scenario on R_{14,0}, R_{14,1}, R_{3,2}, with η between
   0.003 (S5, far states) and 0.198; the binding move is always the truth → truth swap. GERC holds
   (max ERC 0.5–0.94 < 1). LD♭ holds exactly (ρ* = 0) for the block designs S1, S3, S4, S6.
   **At n = 200 the hypotheses fail at the sample level** (spurious correlations ≈ 0.32; GERC 1.3–1.7; sample PGD
   negative on far states in S3, S4, S6), yet the greedy repair succeeded from every tested centre whenever S₀ was a
   local maximum (31/36 datasets); the 5 failures are posterior misses, as Lemma 0 forces.

## 2. Statements (full versions with proofs in PROOF.md)

**Region.** For a deterministic 𝒟 ⊆ S₀ᶜ: R_{a,d}(𝒟) := {U ∪ P : U ⊆ S₀, |S₀∖U| ≤ a, P ⊆ 𝒟, |P| ≤ d}.

**Hypotheses.**
- SE_λ(j₀), anchored: λ_min(R_{S₀∪J}) ≥ φ₀² for all J ⊆ S₀ᶜ with |J| ≤ j₀.
- PGD(η) on 𝓡: for every S ∈ 𝓡 with a missing truth, ρ⁰(S) ≤ (1−η)ρ⁺(S). Here ρ⁺ and ρ⁰ are the best
  population residual reductions ‖r_S‖² − ‖r_{S′}‖² over progress and over non-progress moves.
- GERC(𝓡; η): ERC(S, l) := ‖Ĝ_M⁻¹ X̂_Mᵀ x̂_l‖₁ ≤ √(1−η) for every S ∈ 𝓡 with M = S₀∖S ≠ ∅ and every null l ∉ S.
  The hats are atoms residualised on S and normalised.
- TRC(𝓡; η): a_u(S − u + j) ≥ η·a_j(S) for all such S, u ∈ S ∩ S₀, j ∈ M. Here a_x(T) is the residual reduction
  from adding x to T.
- LD♭(d; B′, ρ*): there is a map l ↦ 𝔑(l), |𝔑(l)| ≤ B′, such that ρ(l, T∖𝔑(l) | S₀ ∪ (T∩𝔑(l))) ≤ ρ* for every null l
  and every set of nulls T ∌ l with |T| ≤ d. Here ρ is the partial multiple correlation. Threshold:
  (★) (1+ρ*√d)²/(1−ρ*²) < 1 + 1/(2A), where p ≤ n^A.

**Theorem W (refined T37(iii)).** Regime R1 with s₀, a, d fixed. Assume EX-A, G, R, SE_λ(d+1), BM-∞, PGD(η) on
R_{a,d}(𝒟), and (H1) d ≤ 1, or (H2) (|𝒟|+1)^{d−1} ≤ n^{1/2−ε}, or (H3) LD♭ with (★). Then P₀(TD′_P(R_{a,d}(𝒟))) → 1.
For any data-dependent centre S_c, P(local search from S_c fails to return S₀ certified) ≤ P(S_c ∉ R_{a,d}(𝒟)) + o(1),
and Ŝ = S₀ afterwards. **PROVED.**

**Prop P1.** SE_λ(d), GERC(R_{a+1,d}(𝒟); η₁) and TRC(R_{a,d}(𝒟); η₂) imply PGD(min η) on R_{a,d}(𝒟). **PROVED.**
Remarks (PROVED): GERC is tight over θ, and holds under a coherence bound mμ_S ≤ √(1−η)(1 − (m−1)ν_S).

**Prop P2 (block reduction).** Assume BO(𝒢): X_gᵀX_h = 0 for g ≠ h, with ≤ 1 truth per group. Write D_g(P) for the
residual of truth j_g given its group-mates P. Then PGD(η) on R_{a,d}(𝒟), a ≥ 1, holds **iff**
- (B1) pcorr²(j_g, l | P) ≤ 1−η;
- (B2) D_g(P−e+l) ≥ ηD_g(P);
- (B3) D_h(Q) ≥ ηD_g(P) for g ≠ h, |P|+|Q| ≤ d.

**PROVED.** For equicorrelated groups (Cor P2′):
η*(d) = min{min_g(1−ρ_g²), min_{g≠h}(θ_h²/θ_g²)(1 − kρ_h²/(1+(k−1)ρ_h))}, with k = min(d, b_h−1).

**Prop P3.** TRC holds with η = φ₀²θ²_min/θ²_max when a = 1, or under BO. **PROVED.**

**Prop P4 (sharpness).** If some S ∈ R_{a,d}(𝒟) has ρ⁰ ≥ (1+ε)ρ⁺, then P(D_S) → 0, so TD′_P fails w.p. → 1.
**PROVED.**

**Lemma P5 / Cor P6 (stability, random designs).** PGD(η), SE and (★) are open conditions. If a Gaussian random
design's population Σ satisfies them and θ_max/θ_min is bounded, the realised design satisfies them with η/2 and
φ₀²/2 w.p. → 1. **PROVED**, given the cited entrywise concentration of sample correlations (Bickel–Levina type;
cited, not re-derived).

**Prop C-LD.** Take s₀ = 1, nulls x̂_i = √r f + √(1−r) g_i (orthonormal f, g_i), r > ½, p = n − 2. All of G, R,
SE (φ₀² = 1−r), BM-∞, PGD(1), GERC and TRC hold. Yet w.p. → 1 the state S₀ ∪ {argmax G, argmin G} is not left by
any progress move, so TD′_P(R_{0,2}) fails. **COUNTEREXAMPLE** (proof in PROOF §5).

## 3. Proofs and sketches
All in `PROOF.md`:
- §1: population side, P1–P6.
- §2: Lemma R (score = −ν log RSS − pen + O(1), uniformly on 𝒯), Lemma G (population-gap comparisons by Gaussian
  maxima), Lemma U (supersets).
- §3: Lemma LD (local/far decomposition) and Lemma S (superset states under H1/H2/H3).
- §4: Theorem W.
- §5: C-LD.

Structure of the proof of Theorem W:
1. At states with a missing truth, PGD gives a population gap ≥ ηNφ₀⁴θ²_min ≫ log n (BM-∞). The noise is
   O(√(gap·log n)), and the gap beats both the noise and the O(log n) penalties uniformly over the polynomially
   many comparisons.
2. At S₀ and its supersets the population gap is 0, and every comparison is a χ² tail against the penalty
   c ≈ ½ log n + log p. The needed events are (α), (β), (γ). Two of them have d.f. matched to their penalty: (β) is
   a 2-d.f. event with penalty 2c. Only (γ) is a one-d.f. event indexed by p·|𝒟|^{d−1} sets ("a null added on top
   of P − e′ is not worth its penalty"). That event is the whole reason LD exists.

## 4. Evidence

All scripts use fixed seeds. They are Python reimplementations: R is not available, and the generator reproduces
the law of `gen_prod_data.R`, not its bits.

**E0. Engine check** (`test_engine.py`): the batched population engine matches brute-force enumeration to 1e-12.
This covers R⁺, R⁰, the F̄ margins, GERC and TRC.

**E1. Population PGD, p = 500 and 1000** (`pop_check.py`, `results/pop_check_p*.json`). Exact reductions were used:
the 14 truth groups plus representative nulls, which is exact for S1, S3, S4, S6 (BO) and for S5 (exchangeability).
For S2, windows of ±10 around each truth are used, so S2 is approximate (truncation error ≤ 5e-4 correlation).
The values are identical for p = 1000.

| scen | η on R_{14,0} | η on R_{14,1} | η on R_{3,2} | binding move | max ERC (GERC) | Cor P2′ prediction |
|---|---|---|---|---|---|---|
| S1 | 0.198 | 0.198 | 0.198 | truth→truth swap | 0 | 0.198 / 0.198 / 0.198 ✓ |
| S2 (approx) | 0.198 | 0.148 | 0.119 | truth→truth swap | 0.50 | — (not BO) |
| S3 | 0.198 | 0.101 | 0.084 | truth→truth swap | 0.70 | 0.198 / 0.101 / 0.084 ✓ |
| S4 | 0.198 | 0.055 | 0.043 | truth→truth swap | 0.85 | 0.198 / 0.055 / 0.043 ✓ |
| S5 | 0.003 | 0.003 | 0.087 | truth→truth swap | 0.94 | — (one factor) |
| S6 | see `results/pop_check_p500.json` | | | | | 0.190 / 0.071 / 0.057 (predicted) |

- **PGD and its sufficient conditions.** PGD holds at the population level in every scenario. The binding
  constraint is (B3)/TRC: swapping a weak included truth (θ = 0.8) for the strongest missing one (θ = 1.8). In S5,
  the one-factor structure makes TRC nearly degenerate far from S₀ (TRC min 1e-4 on R_{14,0}, i.e. near-masking).
  Near S₀, on R_{3,2}, η = 0.087. GERC (ERC < 1) holds in all scenarios.
- **LD♭.** It holds with ρ* = 0 for S1, S3, S4, S6, taking 𝔑 = group-mates. S5 has residual partial correlations
  0.016–0.058 between nulls of different groups given S₀ (max ρ with two far nulls ≈ 0.079), which meets (★) only
  for moderate A (d = 2 needs A < 2.07). For S2 the far AR correlations decay as 0.5^k.
- **Finite-n population score at n = 200.** We used the score F̄ = −ν log v − pen, with the noise switched off.
  On R_{14,0} the progress move is not the F̄-best move in 57–86% of the states with many missing truths. The
  reason is that the truth→truth swap saves the 6.8-nat size penalty when ν log(1 + Δ/v) is diluted by a large
  residual v. On all states with m ≤ 2, the progress move is F̄-best in 95–100% of cases. In other words, **at
  n = 200 TD′_P is not even true without noise far from S₀; it is a near-truth property.**

**E2. Realised designs at n = 200, p = 500** (`n200_check.py`, `results/n200_p500_S*.json`; 3 replicates ×
c ∈ {1, 0.5} × S1–S6 = 36 datasets).
- **Sample PGD.** On R_{14,0}, sample PGD fails in every replicate of S3, S4, S6 and in one of S5: η̂ ranges from
  −0.36 to −0.05, with "add a spurious null" binding. It holds weakly in S1/S2 (η̂ = 0–0.03). On R_{2,1} it holds everywhere, with η̂ = 0.002–0.107
  (truth→truth swap binding).
- **Sample GERC and TRC.** Sample GERC fails everywhere: max ERC = 1.29–1.68. Sample TRC (R_{2,1}) = 0.002–0.08.
- **Anchored SE.** min λ_min(R_{S₀∪J}), |J| ≤ 2: 0.46 (S1), 0.26–0.30 (S2), 0.16–0.18 (S3, S5), 0.08–0.10 (S4),
  0.07–0.08 (S6). Note that |J| = 2 is a subsample of the nulls.
- **Sample LD level.** max |pcorr(l, e | S₀)| over non-neighbour pairs is 0.31–0.36 in every scenario. This is
  pure sampling noise (≈ √(4 log p/n)), and it is far above the (★) threshold (≈ 0.1 for d = 2). So at n = 200,
  (H3) fails and only (H1)/(H2) are available.
- **Noise side, (L) and (H1).** S₀ was a strict local maximum in 31/36 datasets. All 5 failures are at c = 0.5
  (S1 r2, S2 r1, S4 r1–r3, S5 r2), and there the best move at S₀ gains 0.1–3.5 nats (posterior misses). The (H1)
  superset event D_{S₀+e} held for all 486 nulls whenever (L) held.
- **Greedy paths.** There were 134 centres per dataset: 14 at S₀−j, 40 at S₀+e, 40 in R_{2,1}, and 40 with 3–6
  missing truths. Every centre reached S₀ certified in all 31 datasets with (L), and no centre reached it in the
  other 5 (Lemma 0 monotonicity). Paths from near centres were 100% progress moves (TD′_P). Paths from centres with
  3–6 missing truths were all-progress in only 7–78% (median ≈ 45%): they still reached S₀, but through neutral
  truth→truth swaps, i.e. TD′_∞ without TD′_P. This matches E1's finite-n picture.
- **Per-step margins.** The margin is F(best progress) − max(F(S), best non-progress). At c = 1 its median is
  7–20 nats, with a 10% quantile of 0–3.4. At c = 0.5 the median is 1–6 and the 10% quantile is −2 to 0. The
  noise-free F̄ margins are similar.

**E3. C-LD numerics** (`ld_counterexample.py`, `results/ld_counterexample.txt`; exact coordinates, so n up to 2·10⁵).
The table gives the fraction of replicates in which the d = 2 progress fails at the extreme pair.

| r | n=200 | 2·10³ | 2·10⁴ | 2·10⁵ |
|---|---|---|---|---|
| 0.30 | 0 | 0 | 0 | 0 |
| 0.55 | 0.03 | 0.03 | 0.035 | 0.017 |
| 0.70 | 0.08 | 0.095 | 0.12 | 0.17 |
| 0.90 | 0.28 | 0.33 | 0.49 | 0.68 |

- Every checked failure was a spurious strict local maximum, so TD′_∞ also fails.
- The d = 1 check holds in 98.5–100% of replicates and tends to 1, as Theorem W (H1) predicts.
- The approach to the limit is logarithmically slow. The margin is ≈ (r − ½)log n − O(log log n), so at r = 0.55
  the asymptotic failure is invisible below astronomically large n. The theorem is asymptotic; the numerics only
  show the trend for r ≥ 0.7.
- The tabulated fraction is a lower bound on P(TD′_P fails), because only the extreme pair is tested.

## 5. What fails and why

- **LD as stated in W1-T37R (κ_n log p → 0).** It is sufficient but needlessly strong. The W1-T37R route
  required NA_d (F(S₀∪P′∪l) < F(S₀∪P′) for all |P′| ≤ d), which is not needed and already costs a p² union at
  d = 1. Replacing it with the events (α)/(β)/(γ) removes LD at d = 1.
- **Dropping LD completely.** Fails for d ≥ 2 with unrestricted extras (C-LD).
- **A θ-free sufficient condition for PGD.** It is impossible in general. The truth→truth swap constraint (B3/TRC)
  is intrinsically θ-dependent: even S1 has η* = θ²_min/θ²_max. GERC is θ-free and handles the null side only.
- **Using PGD at n = 200.** Population PGD holds, but the finite-n score adds a size-penalty asymmetry. Far from
  S₀ this asymmetry makes neutral swaps beat additions even without noise. The asymptotic statement is fine; it
  is the finite-n reading that is wrong.
- **Chaining over all P′.** Tried and not needed: the plain union bound with matched degrees of freedom is
  enough for (α)/(β). For (γ), chaining over P′ is what LD♭ encodes (local/far split). Any further gain would
  need correlation decay, and C-LD shows that cannot be avoided in general.

## 6. Needs escalation

1. **Independent line-by-line check of Lemma R and Lemma G.** This covers the constants C₀, the ν/N bounds, and
   the claim that the b₀ and ridge terms are O(1) uniformly on 𝒯. These carry every probabilistic statement.
2. **Lemma S (H3).** Check the uniformity of the local/far decomposition over the map 𝔑, and the count
   (2p+1)^d of far subspaces.
3. **Cor P6** relies on a cited concentration bound for sample correlations. It should be replaced by an explicit
   reference with constants.
4. **The sharp LD threshold.** (★) is off from C-LD's 1/(2A) by a factor of about 3–4. A stronger prover might
   close the gap with a joint χ² treatment of the (γ) events.
5. **External precedent (OLS exact-recovery condition; Soussen et al. 2013, Tropp 2004)** is cited from memory
   and must be checked.

## 7. Outside scope

- **What the n = 200 data supports.** It supports a near-truth repair statement (R_{2,1}: TD′_P on every tested
  centre when S₀ is a local maximum) and a TD′_∞-type statement far from S₀ (neutral truth→truth swaps occur). It
  does not support TD′_P on R_{14,·}. For T38(b1)+LS0 this means the start mode must be near S₀ (m ≤ 2), or the
  repair input should be TD′_∞ with the W1-T37R move bound r_𝓡.
- **(H2) and the start partition.** (H2) with 𝒟 = nulls in the truth blocks of the start partition is the natural
  pairing with W1-T38E's LS0 route. It requires the start mode's extras to lie in truth blocks, which is an
  eligibility statement for T38, not proved here.
- **W1-T38E's CF family** should satisfy (H1)/(H2) and PGD; checking this would close their "uniform TD′ on CF"
  crux. Not done here.
- **S5 at the population level** has near-masking far from S₀ (TRC ≈ 1e-4). This is relevant to T27 compatibility.

## 8. Confidence cards

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| Theorem W (H1, d ≤ 1) | TD′_P(R_{a,1}) w.p. → 1 under G, R, SE_λ(2), BM-∞, PGD | high (0.9) | done (candidate; needs review of Lemmas R, G) | uniform O(1) score remainder | no |
| Theorem W (H2) | the same for any d with block-local extras | high (0.85) | done (candidate) | (γ) count \|𝒟\|^{d−1} | no (pairs with LS0) |
| Theorem W (H3) | any d with LD♭ + (★) | medium-high (0.8) | done (candidate) | local/far decomposition | no |
| P1: GERC + TRC ⇒ PGD | deterministic | high (0.95) | done | — | no |
| P2: block iff (B1)–(B3) | deterministic | high (0.95) | done; numerically matched | — | no |
| P4: PGD sharp | reverse margin ⇒ failure | high (0.9) | done | — | no |
| C-LD | LD needed for d ≥ 2 with unrestricted extras | high (0.9) | done (proof + trend numerics) | slow log n approach | no |
| PGD for S1–S6 (population) | holds, η = 0.003–0.198 | high (exact for S1, S3–S5, approx for S2) | numerical, exact reductions | S5 small η far from S₀ | no |
| PGD/GERC/LD at n = 200 (sample) | fail on far states; PGD holds on R_{2,1} | — (measured) | — | spurious correlations ≈ 0.32 | the theorem is asymptotic only; disclose |

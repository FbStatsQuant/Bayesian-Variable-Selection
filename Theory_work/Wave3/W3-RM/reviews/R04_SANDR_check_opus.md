# R04 — Cross-family check of Lemma SAND-R (`lemmas/L3_SANDR.md`) and Lemma SAND-R′ (`lemmas/L3b_rate.md`)

Checker: Claude Opus 5.5 (effort high), independent cross-family seat (L3_SANDR's author is Codex gpt-6.1-sol).
Date 2026-11-09. Mandate: try to break the delta-proof; open every reused source and check the reuse line by line.
No cited status is upgraded. Scratch numerics: `reviews/R04_scratch/recursion_check.py` → `recursion_check_out.txt`.

## Verdicts

* **`lemmas/L3_SANDR.md` (Lemma SAND-R): VERIFIED-WITH-AMENDMENTS.** No FATAL, no MAJOR. The lemma as stated in §1
  is proved, given the named inputs with their recorded statuses. The amendments (F1–F4) are wording and quantifier
  fixes. None changes a hypothesis or a conclusion.
* **`lemmas/L3b_rate.md` (Lemma SAND-R′): VERIFIED.** NITs only (F8–F10). One of them is optional: the route
  supports a weaker rate condition than the one stated.

## Sources opened and checked

G6 = `Wave1C/C-GROW/lemmas/L6_random_AR1.md` §§1–4 (lines 76–389, all read); G3 = `Wave1C/C-GROW/lemmas/L3_sandwich.md`
(all); G0 = `Wave1C/C-GROW/lemmas/L0_toolkit.md` (all) plus `Wave1/W1-GEN/lemmas/L1_lemmaE.md` L1.2, (E4), (E6), L1.4
(statements); APP = `Wave2/W2-APP/lemmas/L3_LOC.md` L3.0–L3.5; D4 = `Wave2/W2-LOC2/lemmas/L4_LOCd.md` (all);
D1 = `Wave2/W2-LOC2/lemmas/L1_toolkit.md` (all); UNI = `Wave2/W2-UNI/lemmas/L2_k0.md` (all) and `W2-UNI/STATEMENT.md`
(UNI-0); `W2-UNI/lemmas/L1_metric.md` CD_M statement; `W2-LOC2/STATEMENT.md` (D2); W3-RM `STATEMENT.md` §§1, 3.2, 4.
Every alias:line citation in L3_SANDR §2–§7 was spot-checked against the file. All point to the claimed argument, up to
±2-line drift that does not matter.

## Point-by-point record (attack points (a)–(h))

### (a) Inventory completeness — no unsupplied design property found
I checked each step of G6 L6.2 → L6.3 → L6.4 → L6.5 (with the APP/D4/UNI deltas) for any use of the AR(1)/local design:

| Candidate | Where it would enter | Finding |
|---|---|---|
| Markov property (P2) | G6 only in L6.6 (NA), lines 393ff | Not in §§1–4. APP:45-50 and UNI G16 agree. Not needed. |
| Global upper spectral bound | G6:108-113 (Gram on C_m log n sets), G6:110 "population eigenvalues in [c₋,c₊]" | Used in G6 only for the O(log n)-set floors (SE_w, G2, lattice family). These feed (H0)/NA/TL, not the sandwich. On ≤ 16+s₀ sets, unit diagonal bounds every entry by 1, and the operator error is ≤ (16+s₀)·Cħ_n. L3_SANDR:110-115 is correct. UNI:184-187 records the same (upper bound C only through CD). |
| Floors on sets larger than 16+s₀ | R⁻¹ (§4), α, τ² (§5), TV (§3), score family (§3) | Largest set needed: D ∪ {l} = U₀ ∪ S₀ ∪ {l}, size ≤ 15+s₀+1. Response comparisons need inverses only on U₀ or U (≤ 15), because Var(V_b given anything) ≥ σ² comes from the independent noise. The L0/GEN-L1 family needs floors only on |A| ≤ 16. No larger floor is used. |
| Small Cov(v, v′) for remote v, v′ | G6:205-207 | G6 itself already derives ‖R⁻¹‖ from Schur complements (G6:206-207). R = D^{-1/2} S D^{-1/2}, with S the sample Schur complement of W_V given W_{U₀}: λ_min(S) ≥ λ_min(R̂_U) ≥ c/2 and diag(S) ≤ 1 + Cħ_n, so λ_min(R) ≥ c/3. Not needed. (Numerics below use ρ_V = 0.9 among the remote v.) |
| Truths inside U₀ | UNI:109 | Cov(W_j, W_v given W_{U₀}) = 0 for j ∈ U₀, exactly. Correct. V = U ∖ H_l contains no truth because S₀ ⊆ H_l. |
| Response beyond Var ≥ σ² | G6:143-152, 197-201 | The only response facts used: Cov(V_b, W_v given U₀) = Σ_{j∈S₀∖U₀} b_j Cov(W_j, W_v given U₀) (linearity plus independent noise); Var(V_b given ·) ∈ [σ², (2s₀θ_hi)² + σ²] (unit diagonal); Y = C V_b at b = θ*/t. All supplied. |
| Exact independence | §5 innovation; §7 Z_{U,j} given X | Comes only from Gaussian rows plus ε independent of W (Setting R). Correct. |
| Specific R_n, d_n values | G6:174, 196, 200, 260 | Enter only as r^{R_n} ≤ n⁻² and r^{d_n} ≤ n^{-1/2}. These are exactly (L-loc-R) and (L-gain-R). |
| "H_l = O(log n)" with a constant | G6:176-177, 299-302 | Used only through L_n = exp(O(log log n)). (L-size) on H_l gives N^ref ≤ (1 + (log n)^κ)^15 = n^{o(1)}. Correct. |
| Conditions on blocks | G6:329-350 | Only |C_b| ≤ 16, disjointness, and "≤ s₀ bad blocks". Partition-free. |
| H0 / SE_w / lattice score family | G6:115-126, 157-167 (second family) | Not consumed by L6.5. (6.10) and the truth-inclusion bound use L0.2(c) and GEN-L1 L1.4(b) only on the first family (|A| ≤ 16). The inventory's "unused" rows (L3_SANDR:77-78, 94) are correct. |

### (b) Random sample scales — handled correctly in every step involving Y
* §3–§4 (L3_SANDR:117-126, 149-164). Sample covariances involving Y are N⁻¹ Σ_k (θ*_k/t_k) Ŝ_{k·} + N⁻¹ Ŝ_{ε·}, which is
  linear in the raw augmented entries. The O(ħ_n) error is uniform over the box |b_k| ≤ 2θ_hi, and the population bounds
  (L-loc-R)/(L-gain-R) are uniform over the box. Evaluating at b = θ*/t (which lies in the box on E_cov) is legitimate.
  Nothing is conditioned on the scales. This matches UNI:100-105 and the bridge note.
* §5 (L3_SANDR:208-220). Y = Σ_{k∈S₀} θ*_k CW_k/t_k + Cε is a function of (W_{S₀}, ε) only. P_{U₀} is
  scale-invariant and a function of W_{U₀}. The method's internal response scaling and the scale t_l of the tested
  column both cancel in the correlation h. So r_Y is (W_D, ε)-measurable. The innovation e = W_l − E[W_l given W_D]
  has rowwise iid N(0, τ²) entries and is independent of (W_D, ε). Since P_{U₀}C = P_{U₀}, (I − P_{U₀})C = C − P_{U₀}
  is an orthogonal projection of rank n − 1 − |U₀| (X_{U₀} has full rank a.s.). So g ~ N(0, τ²(C − P_{U₀})) is isotropic
  in that subspace, and r_Y lies in the same subspace. The C-centring is handled correctly (G6:264-266).
* This step does condition on the true-column scales, because they are W_D-measurable. That is legitimate: the
  conditional law of e is exact, not a Gaussian law asserted after conditioning on a sample-covariance event. See F1
  for a wording point this raises.

### (c) Selection removal — recursion, constants and uniformity verified
* Recursion. Partial correlation of (l, Y) given V after residualising on U₀: z_U = (z₀ − aᵀR⁻¹d)/√((1 − aᵀR⁻¹a)(1 − dᵀR⁻¹d)).
  This is an exact sample identity. Numerically it holds to 1e-16 (below).
* Bound. Put x = aᵀR⁻¹a and y = dᵀR⁻¹d, both ≤ C g_n². Then z_U − z₀ = −aᵀR⁻¹d + (z₀ − aᵀR⁻¹d)(1/√((1−x)(1−y)) − 1),
  so |z_U − z₀| ≤ C g_n² once C g_n² ≤ ½. With g_n = ħ_n this is the L3_SANDR:177 claim.
* |z₀| ≤ Cħ_n. The population partial correlation is Σ_{j∈S₀∖U₀} b_j Cov(W_l, W_j given U₀) / √(Var(W_l given U₀)·Var(V_b given U₀))
  ≤ 2s₀θ_hi C_L n^{-1/2}/√(cσ²), uniformly over the box, and the sample error is O(ħ_n). Correct.
* Then n|z_U² − z₀²| ≤ n·Cħ_n²·(2Cħ_n + Cħ_n²) = O((log n)^{3/2} n^{-1/2}). This is (1).
* Uniformity. Every bound is a deterministic consequence of E_cov. E_cov is partition-free and fixes no (U, l), so (1)
  holds simultaneously for all l ∉ Q and all U ∌ l with |U| ≤ 15, including data-selected U. Every U₀ = U ∩ H_l lies in
  the deterministic family I_l. Conversely, every U₀ ∈ I_l arises as U ∩ H_l with U = U₀, so (L-gain-R) as quantified
  covers all of I_l, as §5 needs.
* Truth–remote covariance. The only response–remote quantity is Cov(W_j, W_v given W_{U₀}) for j ∈ S₀ ∖ U₀ and v ∈ U ∖ H_l.
  This is exactly the second clause of (L-loc-R). Nothing more is needed.

### (d) Spherical tail and counting — verified
* ‖α‖ ≤ ‖Σ_{T given U₀}⁻¹‖·‖c‖ ≤ √s₀ C_L n^{-1/2}/c, using the floor on D (size ≤ 15+s₀). On CN_D,
  ‖m‖ ≤ Σ|α_j|·‖CW_j‖ ≤ 2s₀C_L/c. The U₀ part is annihilated, so β_j is not even needed.
* (6.9) → (2). From |⟨g+m, r̂⟩|/‖g+m‖ ≤ (|⟨g, r̂⟩| + ‖m‖)/(‖g‖ − ‖m‖) with ‖g‖ ≥ c√n:
  √h ≤ (1 + C/√n)√n|⟨ĝ, r̂⟩| + C. With the chi-square lower tail and the normal Chernoff bound,
  (√t − C)²(1 − O(n^{-1/4})) = t − O(√log n) for t ≤ (2A+3) log n. Correct.
* Count. exp(−t_n(k)/2) = e^{C₀/2}(n+1)^{-1/2} k/p, so p·N^ref·e^{−(t_n(k) − ω_n)/2}·e^{C√log n} = k n^{-1/2+o(1)},
  and the remainder p N^ref e^{−c√n} = o(n^{-1/2}). The thresholds lie in the range of (2):
  t_n(k) − ω_n ≥ log n − C₀ − o(1) ≥ ½ log n because p ≥ K ≥ k, and t_n(1) ≤ (2A+1) log n + 1.
* T_n. p·N^ref·e^{−T_n/2}·n^{o(1)} = n^{-1/4+o(1)}. In the margin,
  log(p/k) + ½ log(n+1) − ½T_n − 2κ_E − o(1) = ¼ log n − log k − 2κ_E − o(1), with k ≤ 2k₀ ≤ 2(log n)^κ + 32s₀, so
  log k = O(log log n) and the margin is positive. Constants agree with (3): C₀ = 4κ_E + 2 dominates
  4κ_E + o(1) (L3_SANDR:252).

### (e) Ladder — verified
* k ≤ q + 16s₀ + 16·#{good b: N_b ≠ ∅}.
* Prior. w(k − |N_b|)/w(k) = ∏(2p − j)/j ≥ (p/k)^{|N_b|}.
* Summing (3) over the re-additions gives one addition with h ≥ t_n(k). Note that (3) carries a remainder 2κ_E per step.
  This over-counts L0.2(c)'s total remainder but is still valid.
* Rungs. On m_i < k ≤ 2m_i: J(t_n(min(2m_i, K))) ≥ J(t_n(k)) > m_i/32. By Markov each rung costs ≤ 64 n^{-1/2+o(1)},
  and there are ≤ log₂(n) rungs.
* The witness counts J are random variables that do not depend on the maximiser. So "every maximiser", ties and
  near-cap sizes included, is covered.
* Branch Q = [p]. Then J ≡ 0 and k ≤ k₀ trivially.

### (f) Truth inclusion — verified
* N⁻¹x_jᵀ(I − P_U)μ = Σ_k θ*_k (R̂_{jk} − R̂_{jU}R̂_{UU}⁻¹R̂_{Uk}). Here R̂ is the standardised Gram, with unit diagonal and
  entrywise O(ħ_n) from Σ. The θ* are fixed and the inverse is taken on U (≤ 15).
* Its population counterpart is exactly the PTV quantity Cov(W_j, Σθ*_kW_k given W_U), because Σ has unit diagonal and
  μ uses standardised columns. This gives ≥ a₀/2.
* Dividing by ‖(I − P_U)x_j‖ ≤ √N gives δ² ≥ N a₀²/4. This is deterministic on E_cov, so no union over the n^{O(1)}
  sets U is needed. The only union is over the Z_{U,j}, conditionally on X. Correct.
* Feasibility follows from (L-feas) in both branches (L3_SANDR:278-281). The prior cost is ≤ log(2p).

### (g) Sanity checks — both classes satisfy the abstract hypotheses
* **UNI-0.** CD_M(a) holds for every conditioning set U (`L1_metric.md` CD_M "for every U ⊆ [p]"). It gives (L-gain-R)
  via UNI:76-77 and both (L-loc-R) bounds via UNI:106-109. FL-R follows from λ_min(Σ_n) ≥ c. Sizes: q, |H_l| =
  O((log n)^{d₀}) ≤ (log n)^{d₀+1}. If d₀ = 0, |H_l| ≤ (s₀+1)C₀ is still ≤ (log n)^1 eventually. Correct.
* **LOC-BF.**
  * (F1) gives exact zeros: Σ_{l,U₀}Σ_{U₀}⁻¹Σ_{U₀,v} = 0 when l and v lie in different groups, because Σ_{U₀} is block
    diagonal.
  * PTV follows from "≤ 1 truth per group": conditional covariances with other truths vanish, and those truths in U are
    conditioned out.
  * FL-R follows from c_B.
  * |H_l| ≤ (s₀+1)max(g₀, g_n) needs exponent κ+1, which is the stated enlargement.
  * Correct. b_lo is indeed unused here.

### (h) Is the stated lemma proved?
Yes, with the hypotheses exactly as in L3_SANDR §1 (= STATEMENT §3.2 (FL-R), (V-R), (L-R)). No hypothesis is missing,
and the floor on Q ∪ {l} is surplus (F3).

## Numerical sanity check (`R04_scratch/recursion_check.py`)
* Setup: U₀ = 3 independent variables. V = 5 remote variables, equicorrelated at ρ_V = 0.9 (floor 0.1; no v–v′
  smallness). Each v has covariance r with both l and the truth j. Cov(l, j) = n^{-1/2}. Y = W_j/t_j + ε.
  40 replications per cell.
* Exact recursion identity: |z_rec − z_U| ≤ 2e-16 in all cells.
* max|z_U − z₀|/(r + ħ_n)² ∈ [0.40, 1.13] across n ∈ {500, 2000, 8000, 32000} and r ∈ {n⁻², ħ_n, n^{-1/3}, n^{-1/4}}.
  This is consistent with |z_U − z₀| ≤ C g_n².
* max n|z_U² − z₀²|:
  * r = n^{-1/3} (inside L3b): 2.98 → 1.34 → 1.29 → 0.70, slowly decreasing.
  * r = ħ_n: 1.22 → 1.45 → 0.84 → 0.23.
  * r = n^{-1/4} (outside L3b's condition; boundary of the weaker condition in F8): ≈ 4, not decreasing.

  This is consistent with the analysis. It is a falsification probe, not evidence of the asymptotic rate.

## Findings

**F1 (MINOR) — wording: "never by conditioning on the scales" versus §5.**
* Location: `STATEMENT.md` §4, note under the bridge table ("never by conditioning on the scales [R01-Q6]");
  `L3_SANDR.md:126`, `:208-209`, `:345-346`.
* Problem: §5 conditions on (W_D, ε), whose σ-field contains the true-column scales t_k, k ∈ S₀. This is correct, because
  e ⟂ (W_D, ε) exactly. But a literal reader of the STATEMENT note could flag it as a violation. L3_SANDR:126 ("At no
  point do we condition on the sample scales") is literally false for §5.
* Fix: in L3_SANDR:126 replace "At no point" with "In the comparison steps (§§3–4) we never". Add to :208-209: "This
  conditioning contains t_{S₀}. That is legitimate, since the conditional law of the innovation e given (W_D, ε) is its
  unconditional N(0, τ²I) law. No law is asserted given a sample-covariance or scale event." Optionally add the same
  sentence to the STATEMENT bridge note.

**F2 (MINOR) — quantifiers of (1) and (3).**
* Location: `L3_SANDR.md:179-181`, `:242`.
* Problem: (3) reads "uniformly for l outside Q and abs(U) ≤ 15". It needs "U ∌ l". Also, (3) is applied to sets
  U ∪ {l} that must belong to the score family {|A| ≤ 16}; this holds automatically, but it is not stated.
* Fix: write "for all l ∉ Q and all U ⊆ [p] ∖ {l} with |U| ≤ 15 (so U, U ∪ {l} ∈ F)".

**F3 (MINOR) — surplus hypothesis.**
* Location: `L3_SANDR.md:22`, `:39-40`, `:299`.
* Problem: the floor on Q ∪ {l} is listed as a hypothesis of SAND-R but never used (confirmed). The lemma is therefore
  stronger than stated.
* Fix: state SAND-R with FL-R restricted to |S| ≤ 16+s₀. More precisely, the proof needs only the sets U ∪ S₀ ∪ {l}
  and their subsets. Keep the Q ∪ {l} floor in the (B8) input map. This needs no change to STATEMENT (B7), which only
  asserts sufficiency.

**F4 (NIT) — edge range of (2).**
* Location: `L3_SANDR.md:232`.
* Problem: when p = 1, T_n − ω_n falls just below ½ log n. That case is vacuous, because s₀ ≥ 1 forces Q = [p].
  Separately, (2) holds for every 0 ≤ t ≤ (2A+3) log n with the same proof, so the lower end of the range is
  cosmetic.
* Fix: say "p ≥ 2 or Q = [p]", or widen the range of (2).

**F5 (NIT) — the good/bad block split is not needed.**
* Location: `L3_SANDR.md:246-248`.
* Problem: (3) holds for every U, so the good-block restriction (inherited from G3, where NEG needs S₀ ∩ C_b ⊆ U) plays
  no role here. It is harmless.

**F6 (NIT) — optional strengthening of (L-gain-R).**
* Location: `L3_SANDR.md:308-311`.
* Problem: the remark correctly says C·√(log n/n) does not suffice. But any leak rate ρ_n = o(√(log n/n)) does suffice
  for this route: ‖m‖ = o(√log n) gives a tail loss e^{o(log n)} = n^{o(1)}, and |z₀| = O(ħ_n) is unchanged.
* Fix: optionally record this in SHARPNESS. Not needed for the lemma.

**F7 (NIT) — citation drift.**
* Location: `L3_SANDR.md:172` cites G6:207-215 for the recursion. The display is at G6:203-215.
* Also: the inventory row for L0 (`G0:12-20`) is the family premise list, which is correct. No substantive mis-citation
  was found.

**F8 (NIT, optional strengthening) — L3b rate condition is sufficient but not what the route needs.**
* Location: `L3b_rate.md:6-8`, `:26-27`.
* Problem: downstream, §§5–7 use (1) only through two facts:
  * h_{U,l} = O(log n), needed for (3) and the ν-expansion.
  * e^{ω_n/2} = n^{o(1)} in the reference count and in the T_n union bound.

  So ω_n = o(log n) suffices, i.e. √(n log n) r_n² = o(log n), i.e. r_n = o((log n/n)^{1/4}). The stated condition
  r_n = o((n log n)^{-1/4}) is a factor √log n stronger.
* Fix: if the strengthening is wanted, keep e^{ω_n/2} explicitly in the §5 count and use the range extension of F4.
  Otherwise leave as is. The stated lemma is correct.

**F9 (NIT) — dangling reference.**
* Location: `L3b_rate.md:33`.
* Problem: `../SHARPNESS.md` does not exist yet (it is planned in PLAN item 5 and STATEMENT (C5)).
* Fix: mark it "(to be created)".

**F10 (NIT) — L3b check of the derivation.**
* Location: `L3b_rate.md:22-28`.
* Re-derived. ‖a‖ + ‖d‖ ≤ C(r_n + ħ_n), using denominators ≥ min(c, σ²) and |V| ≤ 15.
  |h_U − h_{U₀}| ≤ C n g_n²(ħ_n + g_n²) = C[√(n log n) r_n² + (log n)^{3/2}n^{-1/2} + n r_n⁴ + (log n)²/n].
  Under the hypothesis, n r_n⁴ = (√(n log n) r_n²)²/log n → 0.
* The claim that (L-loc-R) is used only in L3_SANDR §4 is correct: §5 uses only (L-gain-R) and FL-R on D ∪ {l}.
  §8's case r_n = Cħ_n satisfies (L-loc-R′), because ħ_n(n log n)^{1/4} = (log n)^{3/4}n^{-1/4} → 0. No error.

## Summary for the lead
SAND-R: VERIFIED-WITH-AMENDMENTS. L3b: VERIFIED. No FATAL or MAJOR findings. The abstract hypotheses (FL-R small sets,
PTV, L-size, L-feas, L-gain-R, L-loc-R, Setting R) supply every design input of GROW L6.2–L6.5 as used for the
sandwich, with no hidden use of the Markov property, an upper spectrum, large-set floors, remote–remote smallness or
block conditions. The scale treatment is correct in every step involving Y. The two example classes satisfy the
hypotheses. The amendments: clarify the scale-conditioning wording (F1), the quantifiers (F2), and drop the surplus
Q ∪ {l} floor from the SAND-R statement (F3).

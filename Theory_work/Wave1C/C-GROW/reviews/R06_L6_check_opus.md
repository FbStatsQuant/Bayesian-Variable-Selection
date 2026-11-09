# R06 — Adversarial line-by-line check of L6_random_AR1.md (Claude Opus 5.5)

Reviewer: Claude Opus 5.5 (review sub-agent, read-only except this file). Date 2026-11-08.
Object: `lemmas/L6_random_AR1.md` (Theorem L6.1, Lemmas L6.2–L6.7, Corollary L6.8).
Inputs read: STATEMENT.md v2.1; L0, L1, L2, L3, L4, L5 of C-GROW; GEN `L1_lemmaE.md`, GEN `L5_assembly.md` (L5.3,
L5.4); `Scripts/Data_generators/gen_dev_data.R`.
Mandate: break it. Result: **I did not find a false step or a failing probability bound.** Every step I attacked
survived. What remains is a set of presentation and record amendments, plus two places where a step is correct but
under-justified as written. Details follow, then verdicts.

## 0. Setting and section 0

* Model. The generator (`gen_dev_data.R:54-61`): `raw_X = Z chol(Sigma)` (iid N(0,Σ) rows, Σ = 0.5^{|i−j|} for S2),
  `X = scale(raw_X)` (centre, sd with n − 1, i.e. X_j = CW_j/t_j with t_j = ‖CW_j‖/√N), `Y = c·Xβ + eps`, eps ~ N(0, 1)
  drawn after X. So Y = Xθ + ε with θ = cβ fixed on the standardized scale and σ = 1. The shipped score centres Y, so
  Y ↦ Xθ + Cε, as written in §0. The method re-standardizes X (idempotent). The output is a function of (X, ε, method
  uniforms) only. ✔
* Q construction, q = O(log n), "either Q = [p] or K ≥ 2q + 32s₀ + 1" and q ≤ K eventually. ✔ (Same as L5(a) v2.1.)
* Negative ρ. Every bound used is in absolute value (|Cov| ≤ r^{|j−k|}). The Markov property (P2) holds for either
  sign. The column sign flip D preserves the law of W up to Σ ↦ DΣD. ✔

## 1. L6.2 (concentration, H0/G1–G3b, A_X, A_cov, A_score)

Checked:
1. Helmert rotation. CW (with the noise column adjoined) equals H′(HW) with HW having N iid rows
   N(0, Σ ⊕ 1). The sample covariance is (HW)′(HW)/N. ✔
2. Chernoff. The upper tail gives exponent −N(th − 2t²) and t = h/4 gives −Nh²/8 (u = h/2 ≤ ½). The lower tail is
   the same with u = −2t. "Decreasing c covers both tails" ✔.
3. Polarization. Var(a ± b) ≤ 4 per coordinate, so the deviation of a sum of squares is at most 4h and the entry
   error is at most 2h. The union bound runs over ≤ 2(p + 1)² sums, with C_A² c > 2A + 2 sufficing. Noise column:
   Var = 2 against any W-coordinate. ✔
4. Standardized error.
   |S_jk/(t_jt_k) − Σ_jk| ≤ |S_jk − Σ_jk|/(t_jt_k) + |1/(t_jt_k) − 1| = O(h_n). The event A_X is X-measurable and
   A_cov ⊆ A_X (for a large enough multiple). ✔
5. Operator transfer. Size times maximum entry gives (C_m log n)·C h_n = O((log n)^{3/2}/√n) = o(1). The population
   spectrum lies in [c₋, c₊] (P1). This covers (G2) (|Q ∪ {l}| = O(log n)), (G3a) (blocks ≤ 16), SE_λ(j₀) and SE_w.
   ✔
6. m♯. The ratio C(p,k)/C(2p−1,k) = ∏_{i<k}(p−i)/(2p−1−i). The factor (p − i)/(2p − 1 − i) is non-increasing in i
   (this needs p ≥ 1) and equals p/(2p − 1) ≤ 2/3 at i = 0 for p ≥ 2. ✔ Checked numerically: the
   max_k ratio/(2/3)^k equals 1.0, 0.9, 0.79, 0.75 for p = 2, 3, 10, 500. R_m ≤ C(2p−1,s₀)·Σ_{k>m}(2/3)^k ≤
   (2p)^{s₀}·3(2/3)^{m+1}. So m♯ = O(log n), and the λ_min ≥ Nc₋/2 ≥ 1 = g₀ part of SE_w follows from item 5. ✔
7. R and BM. ‖μ‖ ≤ Σ|θ_j|‖X_j‖ = √N Σ|θ_j| holds deterministically. BM uses a deterministic envelope. ✔
8. TV. Population: |Cov(W_j, Σθ_kW_k | W_U)| ≥ |θ_j|(1−r²)/(1+r²) − Σ_{k≠j}|θ_k|r^{|j−k|} ≥ (|θ_j|/2)(1−r²)/(1+r²)
   by P3, P4 and (6.0). The sample Schur complements on index sets of size ≤ 16 + s₀ are within O(h_n), and
   R̂_{jj·U} ≤ 1. So δ²_{U,j} = N(Σ_kθ_kR̂_{jk·U})²/R̂_{jj·U} ≥ Na₀²/4. This uses μ = Xθ exactly; no t_j enters. It
   holds for every U ∌ j with |U| ≤ 15, so it holds for any X-measurable partition. ✔
9. A_cov (partial correlations involving Y). Write Y = Σ_{S₀}(θ_j/t_j)CW_j + σC(ε/σ). Every fixed-dimensional
   sample conditional quantity is a smooth function of augmented sample covariances on a bounded index set, with
   coefficients in a bounded set. The comparison "pseudo-population with coefficients θ_j/t_j" is the right device;
   the coefficients do not need to be independent of the sample. Var(Y*|W_U) ≥ σ². ✔
10. A_score. Conditional on X ∈ A_X, the families {A : |A| ≤ 16} (≤ 17(p+1)^16 sets) and the L2.0 lattice family
    are deterministic. They satisfy the Gram floor and the energy bound, and their 𝒱𝒱 sets are polynomial. So the L0
    events 𝒟₁–𝒟₃ have failure probability bounded uniformly in x ∈ A_X. Integrating gives P(A_X ∩ A_score) → 1. ✔
    Note: L1.4(b) (used for truth inclusion in L6.5) holds on the same event. ✔

Amendments (presentation only):
* (A1) Line 139: "μ = Σ θ_j W_j/t_j" should read μ = Σ θ_j CW_j/t_j.
* (A2) Notation clash. L6 uses h_n = C_A√(log n/n) (L6.2) and ω_n = C(log n)^{3/2}/√n (L6.3), but L0/GEN-L1 already
  define h_n = √(2(D_V+1) log n) and ω_n (the RSS floor), and L6.5 uses both families. Rename the L6 quantities
  (e.g. ħ_n, ϖ_n).
* (A3) State explicitly that A_score is the event "𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ for both families" with the L0 constants
  (D = 16A + O(1)), and that L1.4(b) and L1.2 hold on it. This is used silently in L6.5's truth-inclusion step.

## 2. L6.3 (selection-uniform reduction)

1. V ∩ S₀ = ∅ because S₀ ⊆ H_l. For v ∈ V, |l − v| > R_n and dist(v, S₀) > R_n, so
   r^{R_n} ≤ r^{2 log n/log(1/r)} = n^{−2}. P4 needs l, v ∉ U₀, which holds. ✔
2. Population z₀: l ∉ Q means dist(l, S₀) ≥ d_n + 1, so |Cov(W_l, Y*|W_{U₀})| ≤ 2s₀θ_max r^{d_n} ≤ C n^{−1/2}. The
   residual variances are ≥ c₋ and ≥ σ². ✔
3. Recursion. z_U = (z₀ − a′R⁻¹b)/√((1 − a′R⁻¹a)(1 − b′R⁻¹b)) is the standard formula for adding V to the
   conditioning set. **Numerically confirmed** (n = 200, |U₀| = 2, |V| = 3): recursion −0.0188602995920316 against
   direct −0.0188602995920316. The identity h = n(RSS_U − RSS_{U+l})/RSS_U = n·Corr² was also confirmed to 1e−12.
4. ‖a‖ + ‖b‖ ≤ C h_n (|V| ≤ 15; the population values are ≤ n^{−2}/c₋). ‖R⁻¹‖ ≤ C because the conditional
   correlation λ_min is ≥ c₋ − o(1). So z_U − z₀ = O(h_n²)(1 + |z₀|), and n|z_U² − z₀²| ≤ Cn h_n³ =
   C(log n)^{3/2}/√n. Also h_{U,l} ≤ Cn h_n² = C log n. ✔
5. Uniformity is a deterministic consequence of the single entrywise event. There is no union over U and no
   independence assumption. ✔

Verdict L6.3: VERIFIED.

## 3. L6.4 (spherical tail, counts (6.6), (6.7))

Attacked points:
1. Decomposition. E[W_l | W_D] = W_{U₀}b + Σ_{S₀∖U₀}α_j(W_j − W_{U₀}b_j) is the Gram–Schmidt split of the
   regression onto U₀ and the truth residuals. ✔ ‖α‖ ≤ (1/c₋)·√s₀·r^{d_n+1} (Schur floor c₋, P4). ✔ e is
   independent of W_D, with row-iid N(0, τ²) entries and τ² ∈ [(1−r²)/(1+r²), 1] ⊆ [c₋, 1]. ✔
2. **Is r_Y fixed given (W_D, ε)?** Yes. Y = Σ_{S₀}θ_jCW_j/t_j + Cε, t_j is a function of W_j only, and P_{U₀}
   depends on W_{U₀} only. The method's response scaling is irrelevant, because h is scale-invariant. ✔ m is
   W_D-measurable (m_raw involves W_{S₀}, W_{U₀} only). ✔
3. **Isotropy.** (I − P_{U₀})C = C − P_{U₀} is the orthogonal projection Π_V onto V = 1^⊥ ⊖ span(CW_{U₀}), because
   span(CW_{U₀}) ⊆ 1^⊥. Since e ⊥⊥ (W_D, ε), g = Π_V e ~ N(0, τ²Π_V) given (W_D, ε). r_Y = (C − P_{U₀})Y ∈ V. So
   ĝ′r̂_Y has the law of one coordinate of a uniform point on S^{d−1}. ✔
4. (6.9). √h = √n|(g+m)′r̂|/‖g+m‖ ≤ √n(|g′r̂| + ‖m‖)/(‖g‖ − ‖m‖), with ‖g‖ ≥ c√n and ‖m‖ ≤ C√n r^{d_n} ≤ C
   (column-norm event, r^{d_n} ≤ n^{−1/2}). ✔
5. Tail. On ‖G‖ ≥ √d(1 − n^{−1/4}) (failure probability exp(−c√n) by item 2 of §1, with h = 2n^{−1/4}), a tail at
   z needs |G′v| ≥ z√(d/n)(1 − n^{−1/4}). With z = (√t − C)/(1 + C/√n),
   z²(d/n)(1 − n^{−1/4})² = t − O(√(log n)) on the stated range of t. ✔ The loss e^{C√(log n)} = n^{o(1)} is
   harmless.
6. **Conditioning on A_cov.** The proof never uses a law conditional on A_cov. It bounds
   P(A_cov ∩ {h ≥ t}) ≤ P(CN_D ∩ {h ≥ t}) = E[1_{CN_D}P(h ≥ t | W_D, ε)], where CN_D is the W_D-measurable
   column-norm event. ✔ This is correct but terse in the text; see (A4).
7. (6.6). On A_cov, J(t) ≤ Σ_{l∉Q}Σ_{U₀∈I_l}1{h_{U₀,l} ≥ t − ω_n} (L6.3). Taking expectations gives
   pL_n[C e^{−(t−ω_n)/2 + C√(log n)} + C e^{−c√n}], and p e^{−t_n(k)/2} = e^{C₀/2} k (n+1)^{−1/2}. The thresholds
   t_n(k) − ω_n lie in [log n − C₀ − o(1), (2A + 1) log n + 1], inside the stated range for k ≤ K ≤ p. Uniform in
   k. ✔
8. (6.7). Taking t = 2 log p + ½ log n − ω_n gives pL_n·p^{−1}n^{−1/4}n^{o(1)} → 0. ✔ For fixed p the threshold is
   ½ log n + O(1), still in range.

Amendments:
* (A4) Write the integration step explicitly as in item 6. Introduce the W_D-measurable event CN_D and note
  A_cov ⊆ CN_D.
* (A5) Typo, line 289: "Equations (6.5)–(6.4)" should read "(6.4)–(6.5)".
* (A6) In (6.5) the bound C exp(−c√n) also absorbs the exp(−cn) term for ‖g‖. Say so.

Verdict L6.4: VERIFIED-WITH-AMENDMENTS (A4–A6).

## 4. L6.5 (sandwich, size ladder)

1. (6.10). RSS_{U+l}/RSS_U = 1 − h/n exactly. With ν = n/2 + 0.01 and h ≤ C log n (L6.3, l ∉ Q):
   ν(−log(1 − h/n)) ≤ (n/2 + 0.01)(h/n + h²/n²) = h/2 + O(log² n/n). L0.2(c) supplies the ±2κ_E remainder on
   A_score for all |U| ≤ 15. Normalizing by RSS_U is sharp and avoids the σ²n floor. ✔ The same inequality, read for
   deletions, is used for junk exclusion, in the correct direction. ✔
2. (6.11). k ≤ |S̃ ∩ Q| + 16·#bad + Σ_good|N_b|, with ≤ s₀ bad blocks. ✔ Removal: per-block optimality of a
   maximizer (as L3 (3.1)) together with w(j−1)/w(j) = (2p−j)/j ≥ p/k gives a gain ≥ |N_b| log(p/k). ✔ Adding back
   in any order: every intermediate conditioning set is ⊆ C_b, has size ≤ 15 and does not contain l. So some add has
   h ≥ log(n+1) + 2 log(p/k) − 4κ_E − o(1) ≥ t_n(k), with C₀ = 4κ_E + 2. Distinct blocks give distinct l, so
   #{good b : N_b ≠ ∅} ≤ J(t_n(k)). J does not depend on the partition or the maximizer. ✔
3. Ladder. m_i < k ≤ 2m_i with k > 2k₀, so k − k₀ > m_i/2 and # > m_i/32. Monotonicity in k and t holds, and
   Markov gives (32/m_i)·min(2m_i, K)·n^{−1/2+o(1)} ≤ 64n^{−1/2+o(1)} per i. There are O(log n) values of i. ✔ This
   covers near-cap maximizers.
4. Truth inclusion. Given X, Z_{U,j} ~ N(0,1) and a union over n^{O(1)} pairs holds. (δ + σZ)² ≥ δ²/2 − σ²Z² ≥ cn,
   and L1.4(b) gives a table gain ≥ cn/(2C_R) − ½ log(n+1) − 2κ_E against a prior cost ≤ log(2p). Feasibility:
   k ≤ 2k₀ = 2q + 32s₀ < K when Q ≠ [p]; the case Q = [p] is handled. ✔
5. Junk exclusion. The gain is ≥ log(p/k) + ½ log(n+1) − ½(2 log p + ½ log n) − 2κ_E − o(1) =
   ¼ log n − log k − O(1) > 0 with k = O(log n). This does not need S₀ ⊆ U (no NEG). ✔

Amendment:
* (A7) Cite the per-block optimality inequality (L3 (3.1)) explicitly, and say that the truth-inclusion step uses
  [GEN-L1] L1.4(b) on A_score (see A3).

Verdict L6.5: VERIFIED-WITH-AMENDMENTS (A7, presentation).

## 5. L6.6 (NA)

1. Innovation. a and b are the nearest elements of T around l, so T ∖ {a, b} ⊆ (−∞, a) ∪ (b, ∞). Markov gives
   e_{l,a,b} ⊥⊥ W_T. τ² ≥ Var(W_l | W_{−l}) ≥ c₋. ✔ (6.13) is exact because CW_a, CW_b ∈ span X_T. **Numerically
   confirmed** (T = {10,20,30,40}, l = 25, n = 400, 50 draws): max |(I−P_T)CW_l − (I−P_T)Ce| = 8.9e−16.
2. Chi-square. P_TCe = P_Te with P_T fixed given W_T, so ‖P_Tg‖²/τ² ~ χ²_{|T|}. ✔ Union over
   ≤ p2^{q−s₀} = n^{O(1)} pairs, with 2^{|T|/2} ≤ n^{O(1)} absorbed by v = C′ log n. ✔ ‖P_Tε‖ ≤ ‖P_Qε‖ and
   χ²_q with q = O(log n). ✔
3. Z⁰ ~ N(0,1) given raw W, because g is W-measurable and ε ⊥⊥ W. The union over ≤ p(q+1)² indices gives (6.14)
   with failure 1/log n. ✔
4. Error identity. h′ε = g′ε − (P_Tg)′(P_Tε), and the displayed bound is exact algebra. ‖g‖/‖h‖ − 1 = O(log n/n),
   so max|Z_{T,l} − Z⁰| = O(log n/√n). ✔ Then c_n − (2 log p + O(log log n)) = log n − O(log log n) → ∞, and L2.2
   applies on A_score. ✔ This covers l ∈ Q ∖ T as well as far l, and the case Q = [p].

Verdict L6.6: VERIFIED.

## 6. L6.7 (TL)

L2.1 is deterministic on 𝓔_n. Its n₀ depends only on (σ², M, φ₀, A, C_P, s₀, BM envelope), and these are common
on A_X. ✔ Verdict: VERIFIED.

## 7. Section 7 (assembly, de-randomisation)

* [OP] is a pathwise inclusion under named premises, so it is law-free. L1.2 is deterministic. The display
  D_n ≤ P(Sand^c) + P(NA^c) + P(TL^c) holds under the joint law. MR1 gives ℓ_n + |S̃₀| ≥ |S̃₀ ∖ S₀|. ✔
* [S-T] under the joint law. f_n(x) := P_ε(1 − π_x(S₀) > e) is a version of the conditional probability given X,
  because π depends on (X, Y) with Y = Xθ + Cε and ε ⊥⊥ X. Every sequence in A_X satisfies H0 with common
  constants, and A_X ≠ ∅ eventually. GEN L5.3 then applies verbatim. Note that GEN's bounded-certificate conclusion
  is not used. ✔ Bounded convergence gives E[1 − π] → 0. [M5-0] holds X-wise, so integration gives (6.2). ✔

Verdict: VERIFIED.

## 8. L6.8 (generator layouts)

The code gives active = 5·step·k + pos[(k mod 6)+1], with step 7 (p = 500) or 13 (p = 1000). **Numerically
checked:** min consecutive gap 32 (p = 500) and 62 (p = 1000); the claim "≥ 31" is a valid lower bound;
max active ≤ p. The exact max_j LHS/RHS of (6.0) at ρ = ½ is 1.17e−9 (p = 500) and 1.09e−18 (p = 1000). The
arithmetic 13·1.8 = 23.4 < 0.24·128 holds. |β| ∈ [0.8, 1.8], σ = 1, and Y = cXβ + ε with X standardized exactly
as t_j. ✔ Scope note (already in §9 of the file): N = 200 is fixed in the generator, so the corollary is about
sequences that extend the layout.

Verdict L6.8: VERIFIED.

## 9. Numerics (scratch, not proof)

Scripts are in the reviewer scratchpad (chk.py, chk2.py). Results: recursion and h-identity exact to 1e−12; m♯
ratio ≤ (2/3)^k; L6.8 ratios as above; L6.6 identity exact to 8.9e−16.

L6.4 tail. Simulation setup: AR(1) with r = 0.5, p = 60, n = 400, S₀ = {10, 40}, θ = (1, −1), σ = 1, far null
l = 25 (d_n = 5), 4000 draws. The table gives P(h_{U,l} > q) from the simulation, with the χ²₁ tail in brackets:

| U | q = 2 | q = 4 | q = 6 | q = 8 |
|---|---|---|---|---|
| U₀ = {24, 26} | .164 (.157) | .050 (.046) | .013 (.014) | .004 (.005) |
| U₀ = {24, 26, 10, 11} | .175 (.157) | .052 (.046) | .017 (.014) | .007 (.005) |
| U = {24, 26, 55, 56, 57} | .169 (.157) | .049 (.046) | .013 (.014) | .004 (.005) |

These are consistent with a χ²₁ tail up to Monte Carlo error and the O(1) leakage term m. The selection-uniform
reduction (third row, with V far from l and S₀) moves the statistic negligibly, consistent with L6.3. This is
illustration only; nothing above relies on it.

## 10. Record amendments for Theorem L6.1

* (A8) The input statuses in §0 are stale. L0 and L1 carry "lemma check R03 (Codex Sol high): VERIFIED". L2 carries
  R03 VERIFIED-WITH-AMENDMENTS (2), applied. L4 and L5 carry R04 VERIFIED-WITH-AMENDMENTS, applied. L6 records them
  only as "PROVED (by this seat, unchecked)". Quote the check records verbatim, as the protocol requires.
* (A9) State in Theorem L6.1 that A ≥ 1 enters C_A, the union constants and m♯, and that n₀ depends on
  (ρ, A, s₀, θ, σ) only.

## Verdicts

| Item | Verdict |
|---|---|
| L6.2 | VERIFIED-WITH-AMENDMENTS (A1–A3; presentation/notation, no mathematical change) |
| L6.3 | VERIFIED |
| L6.4 | VERIFIED-WITH-AMENDMENTS (A4–A6; integration step to be written out, typo) |
| L6.5 | VERIFIED-WITH-AMENDMENTS (A7; cite (3.1) and L1.4(b)) |
| L6.6 | VERIFIED |
| L6.7 | VERIFIED |
| §7 assembly | VERIFIED |
| L6.8 | VERIFIED |
| Theorem L6.1 | VERIFIED-WITH-AMENDMENTS (A1–A9), conditional on the named inputs and implementation premises (GUARD-W, OP-LS0, e4 [N3 OPEN], complete scans) and MR1, exactly as stated; no gap found |

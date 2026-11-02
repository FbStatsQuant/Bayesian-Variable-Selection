# W7-PART — REPORT: the partition-recovery lemma for iid Gaussian designs

Run of 2026-11-02, branch `theory/W7-PART`, from `theory/campaign` @ 6f93ea3.
- Proofs: `PROOF.md`.
- Scripts: `scripts/` (fixed seeds).
- Outputs: `results/`.

Every result is a **candidate**, not reviewed and not adopted.

## 1. Headline

1. **PROVED (candidate): the partition-recovery lemma, with explicit constants (Theorem B, Corollary B).**
   - **Setting.** Rows are iid N(μ, Σ). Within-group |Σ_jl| ≥ ρ; cross-group |Σ_jk| ≤ ψ̄ < ρ; g_max ≤ B < 2g_min;
     here B = min(⌊√n⌋, ⌊√p⌋, 16) is the method's own block size.
   - **Bound.** The actual v3 partition satisfies
     P(blocks ≠ groups) ≤ (2/(√π(1−ρ))) p² √n e^{−(n−4)I\*(ρ,ψ̄)}.
     The exponent I\* is in closed form, and the result is ≤ p^{−C} once n ≥ n₀(A, C, ρ, ψ̄); n₀ is tabulated.
   - **Scope.** This covers LH-iid (W3-PXN) and the S5-type global factor. It replaces W3-PXN's cited concentration
     lemma C1 with a self-contained proof. **The partition never reads y**, so the event is σ(X)-measurable and
     independent of ε.
2. **PROVED (candidate): an exact structural theorem for the actual algorithm (Theorem A).**
   - Complete linkage keeps every group intact if and only if a node-level condition (C\*) holds. The "only if"
     direction needs a mild side condition.
   - (C\*) is far weaker than the margin condition used so far. In 320 hard replicates the margin held 15 times;
     (C\*), laminarity and blocks = groups held 261 times.
   - For independent groups this gives a sharp bound (Theorem C, Corollary C) whose exponent is exactly **2I\***.
3. **Finite n at the study size (n = 200, B = 14). Rigorous bounds:**
   - **Independent groups, ρ = 0.7, g ∈ {8, 10, 14}:** P(blocks ≠ groups) ≤ 3.4e-9 to 1.1e-8 at p = 500 and
     1.4e-8 to 4.7e-8 at p = 1000 (Corollary C). Theorem B gives 3.4e-5 to 1.3e-4.
   - **LH-iid (ρ = 0.7, ψ = 0.5, g = 10, c = 1):** the rigorous bound is only **0.17**. It is dominated by the one
     *dependent* linked group pair. The 95% Monte Carlo bound for that pair is 1.5e-4.
   - **Actual algorithm:** 0 failures in each of these cells (500–2,000 replicates per cell).
4. **COUNTEREXAMPLES: the lemma is false outside its hypotheses; each case is a hypothesis failure, not an algorithm
   bug.**
   - **g > B.** At n = 200, B = 14, so the task's "9 ≤ g ≤ 16" fails for g = 15, 16 with probability 1. The correct
     range is g ∈ [⌊B/2⌋ + 1, B].
   - **2g ≤ B** (the study's g = 5). blocks ≠ groups surely, but blocks are unions of whole groups w.h.p. (PROVED).
   - **|ψ| > ρ.** Recovery fails w.p. → 1 (mechanism PROVED; blocks ≠ groups shown in simulation). At
     ψ = ρ (the boundary), 23–26% of replicates fail at n = 200; the limit is OPEN.
   - **No algorithm change is needed in the stated regime.**

## 2. Statements (full proofs in PROOF.md)

**Algorithm facts (read from `cpp/v3_blocks.h`, `v3_score.h`, `v3_preprocess.R`; PROOF §0.1).**
- **Input.** The partition uses only r̂_jl = G_jl/√(G_jj G_ll), with G = XᵀX of the standardised columns.
- **Steps.** Complete linkage on 1 − |r̂| with R13 ties; a top-down cut at B; next-fit packing of whole clusters
  into bins of B.
- **No y.** y enters only z = Xᵀy and the block tables, which are built after the partition.
- **Thresholds.** The only threshold is B = min(⌊√n⌋, ⌊√p⌋, 16), which is 14 at the study size.
- **Exact branch.** No partition is built there (p ≤ 17).
- **Port check.** The Python port matches the compiled, unmodified engine header on 70/70 designs, including
  exact-tie designs (`results/check_port.txt`).

**Hypotheses.**
- (GRP(ρ, ψ̄)): |Σ_jl| ≥ ρ within groups, |Σ_jk| ≤ ψ̄ across, 0 ≤ ψ̄ < ρ < 1, Σ positive definite.
- (SIZE): g_max ≤ B(n, p) < 2 g_min.
- (IND): the groups are independent.

| # | Statement | Hypotheses | Status |
|---|---|---|---|
| A0 | Complete-linkage heights are monotone. Until the first bad merge, each group's internal merges are those of its own dendrogram T_h. At the first bad merge (height δ), the current clusters of h are the nodes A ∈ T_h with ht(A) < δ < π(A) | no ties (a.s.) | PROVED |
| A1 | (C\*) ⇒ the dendrogram is laminar w.r.t. 𝒢. (C\*): for h ≠ h' and nodes A ∈ T_h, A' ∈ T_{h'} not both roots, min_{A×A'} \|r̂\| < max(σ(A), σ(A')), with σ(A) = 1 − (parent height of A in T_h) and σ(root) = −∞ | no ties | PROVED |
| A2 | Laminar ⇒ (C\*), provided no two whole groups merge below max_h H_h | no ties | PROVED |
| A3 | Laminar and g_max ≤ B ⇒ every block is a union of whole groups. If also B < 2g_min, blocks = 𝒢 | any tie rule and leaf order | PROVED |
| A4 | Local margin (M) ⇒ (C\*). (M): every cross \|r̂_jk\| < min(m_h, m_{h(k)}), with m_h the weakest within-h \|r̂\| | — | PROVED |
| L1 | √(n−2) r̂/√(1−r̂²) =_d (Z + a√W)/√(V/(n−2)), a = r/√(1−r²); hence P_r(\|r̂\| ≥ t) is nondecreasing in \|r\| | bivariate normal | PROVED |
| L2 | P_r(r̂ ≥ t) ≤ √((n−2)/2π)(1+\|r\|)^{3/2}(1−\|r\|)^{−1}(1−t)Λ_r(t)^{(n−4)/2} for t ≥ r, and the mirror bound for t ≤ r, with Λ_r(t) = (1−r²)(1−t²)/(1−rt)² | n ≥ 4; Hotelling's classical density | PROVED (density cited; checked numerically two ways) |
| B | For t ∈ (ψ̄, ρ): P(blocks ≠ 𝒢) ≤ Σ_within P_ρ(\|r̂\| ≤ t) + Σ_cross P_{\|Σ_jk\|}(\|r̂\| ≥ t) (exact laws), and the explicit L2 form | GRP, SIZE, n ≥ 5 | PROVED |
| Cor B | P(blocks ≠ 𝒢) ≤ (2/(√π(1−ρ))) p²√n e^{−(n−4)I\*}, with t\* = (q−1)/(qρ−ψ̄), q = √((1−ψ̄²)/(1−ρ²)), I\* = −½ log Λ_ψ̄(t\*). If p ≤ n^A, the bound is ≤ p^{−C} for n ≥ n₀ (table below) | as B | PROVED |
| L3 | Independent groups: given both within-group correlation matrices, the cross correlations (r̂_jk)_{j∈h} for fixed k are (⟨u_j, v⟩)_j with v uniform on S^{n−2} | X_h ⊥ X_{h'} | PROVED |
| C | P(blocks ≠ 𝒢) ≤ Σ_{dependent pairs} P((C\*) fails for the pair) + Σ_{independent ordered pairs} E[S_L + S_N]. Here S_L, S_N are explicit sums of null-law tails H₀ over node pairs, at thresholds max(σ(A), f_k) and max(σ(A), σ(A')) | SIZE, no ties | PROVED |
| Cor C | (IND), equal g: P ≤ G(G−1) K_g [H₀(τ₀) + Σ_i H₀(τ_{i+1}) min{1, g(g−1)P_ρ(\|r̂\| < τ_i)}], with K_g = (2g−1)g + (g−1)² | IND, SIZE | PROVED |
| κ | The exponent of Cor C is min_τ[I(τ;0) + I(τ;ρ)] = 2I\*(ρ, 0), attained at the Fisher-z midpoint t\* | — | PROVED (identity); PROOF SKETCH (the mesh-1/n bookkeeping for the asymptotic form) |
| CE1 | g_h > B ⇒ blocks ≠ 𝒢 with probability 1 | — | COUNTEREXAMPLE |
| CE2 | 2g_min ≤ B, G ≥ 2 ⇒ blocks ≠ 𝒢 surely; blocks are unions of whole groups with the same probability bounds as B/C | — | COUNTEREXAMPLE / PROVED |
| CE3 | LH with \|ψ\| > ρ: (C\*) fails w.p. → 1 at the hub pair; blocks ≠ 𝒢 observed | — | COUNTEREXAMPLE (mechanism PROVED; blocks ≠ 𝒢 by simulation) |

**Explicit constants (Corollary B; `results/union_bound.txt`).**
- n₀ for P ≤ p^{−C} at p = n^A:

  | ρ | ψ̄ | I\* | t\* | A = 1.25, C = 1 | A = 1.25, C = 2 | A = 2, C = 1 | A = 2, C = 2 |
  |---|---|---|---|---|---|---|---|
  | 0.7 | 0 | 0.0912 | 0.408 | 282 | 377 | 455 | 618 |
  | 0.85 | 0 | 0.185 | — | 126 | — | — | 272 |
  | 0.5 | 0 | 0.0373 | — | 787 | — | — | — |
  | 0.7 (S5-type) | 0.3 | 0.0384 | — | 775 | — | — | — |
  | 0.7 (LH) | 0.5 | 0.0126 | — | 2,788 | — | — | 5,982 |

- Corollary C halves these n₀: its exponent is 2I\*.

## 3. Proofs (skeleton; complete text in PROOF.md)

- **Theorem A.**
  - Complete linkage is monotone. Before anything crosses a group boundary, every group runs its own dendrogram,
    interleaved by height (A0).
  - The first bad merge joins a current node A of T_h either to a current node A' of T_{h'} or to a full union of
    groups containing some h'. Both clusters are still unmerged at that height, so
    max_{A×A'} d ≤ δ < min(π(A), π(A')), which is exactly the failure of (C\*).
  - Laminarity plus g_max ≤ B makes every retained cluster a union of whole groups. With B < 2g_min, packing cannot
    put two groups in one bin.
  - (M) ⇒ (C\*) because every non-root σ(A) ≥ m_h (the root height of complete linkage is the diameter).
- **Theorem B.** (M) fails ⇒ some within pair ≤ t or some cross pair ≥ t; take a union bound over pairs with exact
  pair laws. The closed form uses Hotelling's density (₂F₁ ≤ its value at 1, by Gauss's theorem; Wendel's inequality;
  Λ_r unimodal at r) and Corollary 1 (monotonicity in |r|).
- **Theorem C.** A (C\*) failure at (A, A') forces all |A| correlations between A and one k ∈ A' above
  s = max(σ(A), σ(A')). For independent groups, Lemma 3 makes these the projections of a uniform vector v onto
  vectors fixed by R̂_h. Bound that with one pair (H₀(s)), or with a sign union over 2^{|A|−1} sign patterns
  (H₀(|A|s/‖U_Aε‖)).
- **Corollary C.** Every threshold is ≥ μ = min(m_h, m_{h'}). Peeling on μ then gives the product of a null cross
  tail and a low within tail: that is the exponent 2I\*.

## 4. Evidence

**4.1 Checks of the lemmas.**
- `check_port.txt`: engine == faithful port == scipy port on 70/70 designs.
- `check_pairlaw.txt`:
  - the density integrates to 1;
  - Hotelling tails agree with noncentral-t quadrature to about 1e-9 relative, and with Monte Carlo;
  - the Lemma-1 representation passes KS (p = 0.43, 0.66);
  - Lemma 2 shows no violation on a 224-point grid (bound/exact ∈ [2.9, 1100]).
- `check_thmA.txt`: 320 hard replicates; (C\*) ⟺ laminar 320/320, laminar ⟺ blocks = groups 320/320, (M) ⇒ (C\*)
  always.
- `check_lemma3.txt`: cross correlations of independent groups follow the null law. KS p ∈ [0.12, 1.0] within
  terciles of f_j, f_k and m_h, and |Spearman| ≤ 0.022.

**4.2 Finite-n probabilities at the study size (n = 200, B = 14).**
- "Rigorous" means a proved bound.
- "MC actual" is the actual partition over independent replicates, with a Clopper–Pearson 95% interval.
- Sources: `results/union_bound.txt`, `results/thmC_analytic.txt`, `results/sim_partition.txt`.

| design | p | Theorem B (rigorous) | Corollary C / C (rigorous) | MC actual: failures / reps (95% upper) |
|---|---|---|---|---|
| indep, g=8, ρ=.7 | 496 / 1000 | 3.4e-5 / 9.5e-5 | 3.4e-9 / 1.4e-8 | 0/500 (7.4e-3) / 0/500 |
| indep, g=10, ρ=.7 | 500 / 1000 | 3.9e-5 / 1.1e-4 | 5.7e-9 / 2.3e-8 | 0/2000 (1.8e-3) / 0/2000 |
| indep, g=14, ρ=.7 | 490 / 994 | 4.7e-5 / 1.3e-4 | 1.1e-8 / 4.7e-8 | 0/500 / 0/500 |
| indep, g=10, ρ=.85 | 500 / 1000 | 2.2e-13 / 6.2e-13 | 1.7e-25 / 7.0e-25 | 0/300 / 0/300 |
| indep, g=10, ρ=.6 | 500 / 1000 | — | 3.1e-3 / 1.3e-2 | — |
| indep, g=10, ρ=.5 | 500 / 1000 | 2.4 / 6.5 (vacuous) | 24 / 97 (vacuous) | 0/300 / 0/300 |
| LH c=1, g=10, ρ=.7, ψ=.5 | 500 / 1000 | 0.17 / 0.17 | 0.17 / 0.17 (linked pair: local margin); **1.5e-4** with the linked pair by MC CP95 (0/20,000) | 0/2000 / 0/2000 |
| LH c=2, same | 500 / 1000 | 0.33 / 0.33 | 0.33; **3.0e-4** with MC CP95 | 0/2000 / 0/2000 |
| global factor ρ=.7, ψ=.3 | 500 / 1000 | 1.4 / 3.8 (vacuous) | not covered (dependent) | see 4.3 |

Reading the table:
- For independent groups at ρ ≥ 0.6 the lemma is not only asymptotic: it is a usable finite-n statement at
  (200, 500) and (200, 1000).
- For LH the only weak link is the single dependent linked pair. The rigorous bound there is the local margin
  restricted to that pair (≈ 0.17). The truth is ≤ 1.5e-4 at 95% confidence.
- Theorem B's bound grows like p² at fixed n (Cor B). Corollary C grows like G²: p = 1000 versus 500 multiplies it
  by about 4.

**4.3 The actual algorithm across regimes (`results/sim_partition.txt`; n = 200, B = 14, g = 10 unless stated).**

| regime | p = 500: fail / reps | p = 1000: fail / reps | margin (M) fails (p = 500 / 1000) |
|---|---|---|---|
| indep ρ = 0.30 | 208/300 | 299/300 | 300 / 300 |
| indep ρ = 0.35 | 30/300 | 117/300 | 300 / 300 |
| indep ρ = 0.40 | 1/300 | 11/300 | 300 / 300 |
| indep ρ = 0.50 | 0/300 | 0/300 | 65 / 157 |
| LH c=2, ψ = 0.60 | 2/300 | 1/300 | 164 / 182 |
| LH c=2, ψ = 0.65 | 6/300 | 9/300 | 283 / 290 |
| LH c=2, ψ = 0.70 (= ρ) | 68/300 | 78/300 | 300 / 300 |
| LH c=2, ψ = 0.75 (> ρ) | 239/300 | 248/300 | 300 / 300 |
| LH all groups linked (G/2 pairs), ψ = 0.5 | 0/1000 | 0/1000 | 265 / 453 |
| global ρ = .7, ψ = .1 / .2 / .3 | 0 / 0 / 0 (of 300) | 0 / 0 / 0 (of 300) | 0, 0, 0 / 0, 0, 5 |
| global ρ = .5, ψ = .1 / .2 | 0/300, 3/300 | 0/300, 14/300 | 299, 300 / 300, 300 |
| global ρ = .5, ψ = .3 (`sim_extra.txt`) | 73/100 | 98/100 | — |
| global ρ = .4, ψ = .25 / ρ = .6, ψ = .3 (`sim_extra.txt`) | 100/100, 0/100 | 100/100, 1/100 | — |
| CE1: g = 15, 16 | 50/50, 50/50 (laminar in all; the cut splits groups) | 50/50, 50/50 (same) | — |
| CE2: g = 5 (2g ≤ B) | 200/200 (blocks are unions of whole groups in 200/200) | 200/200 (unions in 200/200) | — |

The columns "not union" and "not laminar" in `sim_partition.txt` equal "fail" in every regime with g ≤ B < 2g. The
margin (M) fails in a large fraction of the replicates in which the algorithm succeeds. That is why Theorems A/C,
not the margin, describe the algorithm at n = 200.

**4.4 n-sweep (p ≈ n^{1.25}; `sim_partition.txt`, last rows).** Asymptotically the lemma bites, as it should. B = 14 at
n = 200 and B = 16 at n ≥ 400.

| regime | n = 200, p = 750 | n = 400, p = 1790 | n = 800, p = 4260 |
|---|---|---|---|
| LH c = 2, ρ = 0.7, ψ = 0.65: fail / reps | 3/200 | 1/200 | 0/60 |
| LH c = 2, ψ = 0.65: margin (M) fails | 186/200 | 170/200 | 33/60 |
| indep ρ = 0.4: fail / reps | 6/200 | 0/200 | 0/60 |
| indep ρ = 0.4: margin (M) fails | 200/200 | 28/200 | 0/60 |

The margin catches up with the algorithm only at n ≈ 800. This matches the factor-2 gap in the exponents
(Cor B versus Cor C).

## 5. What fails and why

- **The margin route (W3-PXN Lemma P1's D_in < D_out, or the local version) is a poor description at n = 200.**
  - It needs every cross |r̂| below the weakest of about G·C(g,2) within correlations.
  - Example: at ρ = 0.5 the margin fails in 22–52% of replicates, while the algorithm never fails.
  - Its exponent I\* is half the true one for independent groups.
  - It remains the right *general* tool when groups are dependent, and it is what Theorem B uses.
- **Plain Monte Carlo of E[S_L + S_N] is not a bound.** The expectation is dominated by rare groups with low within
  correlations, so a sample mean underestimates it by orders of magnitude (1e-21 versus a rigorous 2e-12 per pair).
  Corollary C replaces it with exact peeling. An MC-plus-Hoeffding version reproduced Corollary C exactly and was
  dropped.
- **A rigorous finite-n bound for a *dependent* LH linked pair beyond the local margin was not obtained.** Lemma 3
  needs independence. Peeling with min(P(A), P(B)) for dependent events keeps the margin exponent I\*(ρ, ψ) = 0.0126,
  which gives ≈ e^{−2.5} at n = 200.
- **"Not laminar ⇒ blocks ≠ 𝒢" is false in general.** The cut can split a bad node of size > B back into whole
  groups. It is never observed with g ≤ B, but it blocks a clean "iff" for blocks = 𝒢.

## 6. Needs escalation

1. **An independent check of Theorem A (A0–A2)**, especially A0(c) and the case of a bad merge with a *full* cluster.
   Everything downstream rests on it. Numerics agree 320/320.
2. **Hotelling's density in Lemma 2** is cited, not derived. It is checked numerically two independent ways to about
   1e-9. A reviewer should confirm the exact form and the n-convention (n = sample size, ν = n − 1).
3. **A rigorous n = 200 bound for the LH linked pair.** Proposed route: condition on the two hub columns. Given them,
   the non-hub members of the two groups are independent. A Lemma-3-type rotation in span(1, x_{a,hub}, x_{b,hub})^⊥
   (dimension n − 3) then applies to the residual parts. This would replace 0.17 by a number comparable to the
   Monte Carlo 1.5e-4.
4. **The κ_C asymptotic form** (mesh-1/n peeling bookkeeping); PROOF SKETCH, routine.

## 7. Outside scope

- **W3-VEXP GAP (b), partition–noise decoupling for 2g ≤ B** (the study's groups of 5), is still OPEN. Theorem A3/B/C
  give "blocks are unions of whole groups" w.h.p. *Which* groups pair up is decided by the minimum cross |r̂| between
  groups, which selects partners with atypically large cross correlations. Lemma 3 shows the cross correlations are
  Haar-rotated given the within-group matrices, which may be the right tool for a leave-one-column-out stability
  argument. Not pursued.
- **W3-PXN Lemma P1** can now cite Theorem B instead of the external C1. Its numerics "b = g 20/20" are consistent
  with §4.
- **The S5-type global factor at n = 200** (cross 0.3, within 0.7) recovers the groups in simulation (0/300
  failures), although Theorem B is vacuous there (1.4–3.8). With weaker within-group correlation it breaks down:
  ρ = 0.5, ψ = 0.3 fails in 73% / 98% of replicates at p = 500 / 1000. A Theorem-C analogue for factor-dependent groups (partial
  out the common factor in the analysis, not in the method) looks feasible.
- **The neighbour graph** (M §6.4) uses the threshold √(2 log p/n). It is not part of the partition and was not
  studied.

## 8. Confidence card

| target | refined statement | true? | provable at reasonable cost? | crux | method change? |
|---|---|---|---|---|---|
| Partition-recovery lemma (Theorem B + Cor B) | GRP(ρ, ψ̄), g_max ≤ B(n, p) < 2g_min, iid Gaussian rows ⇒ P(blocks ≠ 𝒢) ≤ (2/(√π(1−ρ))) p²√n e^{−(n−4)I\*}; ≤ p^{−C} for n ≥ n₀ | high | done (candidate; needs review of A and L2) | Theorem A (A1, A3, A4); Lemma 2 | no |
| Sharp version, independent groups (Theorem C + Cor C) | the Cor C formula; exponent 2I\* | high | done (candidate) | Lemma 3 (rotation invariance) + peeling | no |
| Finite-n at the study size, independent groups, ρ ≥ 0.7 | P(fail) ≤ 2.3e-8 (g = 10, p = 1000) | high | done | — | no |
| Finite-n at the study size, LH (ψ = 0.5) | P(fail) ≤ 1.5e-4 (MC, 95%); rigorous only 0.17 | high (MC 0/2000 actual, 0/20000 pair) | medium (escalation 3) | conditioning on the hubs | no |
| Task's range "9 ≤ g ≤ 16" | false at n < 256 (B = 14 at n = 200); correct range g ∈ [⌊B/2⌋+1, B] | — (COUNTEREXAMPLE) | — | — | no (restate the hypothesis) |
| blocks = unions of whole groups when 2g ≤ B | same bounds as B/C | high | done | A3 | no |
| Which groups share a block when 2g ≤ B (W3-VEXP GAP b) | OPEN | — | low–medium | partition–noise decoupling | maybe (row-split partition) |

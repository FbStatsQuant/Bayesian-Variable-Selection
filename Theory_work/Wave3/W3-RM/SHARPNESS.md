# W3-RM — SHARPNESS RECORD (claim (C5); for the registry in `Theory_work/INFRA/`)

Version 2 (rewritten after sweep R08, findings 2–5, 7–12: the first version drew necessity and "not sharp"
conclusions that its evidence did not support).

**How to read this file.** For each assumption four things are kept apart:
(P) what is **proved** about it (with file); (S) **successful designs outside it** — designs violating the assumption
on which the conclusion is nevertheless proved or observed (this shows the assumption is *not necessary for those
designs*; it says nothing about a worst-case converse); (F) **failing designs outside it** — a proved or observed
failure of the conclusion or of the route (an existential obstruction to dropping the assumption; not a necessity
statement for every design); (O) what is **open**. "Observed" always means numerics: observations only, never
proofs; all theorems are asymptotic. Numerics: §6 and `numerics/SUMMARY_SHARPNESS.md`.

## 1. The conditioning size "15" in (V) and (L)

* (P) 15 is the largest conditioning size that the uniform blockwise proof must cover when the block cap is B = 16
  (in general B − 1 with B = min(⌊√n⌋, ⌊√p⌋, 16), `Theory_work/State_of_Project/sections/02_method.tex:187-211`; B = 16
  eventually when p_n → ∞). Lemmas B1/B1′ (`lemmas/L1_fixed.md`) prove that the partition-free conditions (all
  conditioning sets of size ≤ 15) are equivalent to the block-relative conditions holding for **every** partition into
  blocks of size ≤ 16. This is an equivalence between these two universal conditions. It is **not** a necessity
  theorem: it does not show that every such partition can be produced by the coded clustering, nor that a theorem with
  a smaller conditioning size must fail.
* (O) Whether a hypothesis on the clustering output would allow a smaller conditioning size.

## 2. Visibility (V)

* (P) Only comparisons at the selected block subsets enter the proof (truth inclusion, with U = S̃ ∩ C_b ∖ {j}); the
  uniform diverging bound M_n log n is sufficient and is not shown necessary even for the sandwich (a large enough
  constant multiple of log n would already dominate the score cost).
* (S) Masked truths: W1-GEN and W1-PXN ("PROVED-CHECKED") prove the reported-model conclusion on designs where a
  truth is masked inside its block and the relevance set is bounded — the start mode omits the truth and LS0 re-adds
  it. So (V) is not necessary for those designs. Observed: numerics V1 (§6).
* (O) Uniform worst-case converse (is there a design class, with (L) and the floors but without (V), on which the
  conclusion fails?): not settled by these results. A growing-Q theorem for masked truths: open (R02: HIGH).
* Weakening recorded, not adopted (R02 P4): block-relative joint visibility (JV_b) — for each block C and U ⊆ C with
  M := (C ∩ S₀) ∖ U ≠ ∅, ‖(P_{U∪M} − P_U)μ‖² ≥ |M|M_n log n. (V_b) ⇒ (JV_b), not conversely. LOW risk; needs
  K ≥ 2|Q| + 33s₀ in (L-feas). It gives nothing in the partition-free form.

## 3. Leakage (L)

### 3.1 The constant η_A and the normalisation
* (P) η < η_A := (√(2A + 1) − √(2A))² is sufficient for the sandwich (GROW L3; Lemma B2τ in `lemmas/L1b_rss.md`): it
  is the optimum of the sufficient inequality Aε₁ + (1 + 1/ε₁)η/2 < ½. The leak is measured against the residual
  variance τ²_U (adopted from R02 P2).
* (O) **No converse is proved.** Heuristic only, under the extra assumptions log p/log n → A and τ_U/σ → 1: if ≍ p
  columns outside Q each had gain exactly ησ² log n and independent standard normal noise coordinates, the expected
  number passing the start-mode threshold would be ≈ p·exp(−[√((2A + 1) log n) − √(η log n)]₊²/2), which stays
  bounded when η < η_A and diverges when η > η_A. This suggests that the sandwich *with that Q* fails above η_A on
  such designs; it is not a statement about the conclusion (the entering columns can be put in a larger Q and may
  then be deleted by LS0), and for a particular design η_A is not necessary (with Q = [p], (L-gain) is vacuous).
  Numerics L2 (§6) is an exploratory experiment on leak strength; it does not test this threshold.
* Form R: (L-gain-R) asks a leak ≤ C_L n^{−1/2}. Weakenings recorded, not adopted: any leak rate o(√(log n/n))
  (R04 F6: same proof, tail loss n^{o(1)}); the standardised budget n·aᵀG⁻¹a/v ≤ η log n, η < η_A (R02 P3b: leaks of
  order √(log n/n), matching Form F; MEDIUM risk, separate ticket).

### 3.2 The size of Q
* (P) What each step uses: the sandwich needs log|Q| = o(log n) (Lemma B2); TL and NA use the lattice toolkit, whose
  cost is t_n + h_n² = O(|Q| + log n) — signal ≫ |Q| + log n (BM-Q) and a loss 2 log|Q| in c_n; (N-χ) covers
  |Q ∖ S₀| ≤ (1 − δ₀) log n; NA-F and NA-R are proved for polylogarithmic |Q|.
* (P) What makes Q large, as a route statement: APP Lemma VN (`Theory_work/Wave2/W2-APP/lemmas/L5_VN.md:23-26`;
  "Under (F16) and VNF(κ_n)", i.e. Gaussian rows with a floor on sets of size ≤ 16 + s₀ and a set 𝒩_n of nulls whose
  squared partial correlation with the response is ≥ κ_n, nκ_n/log n → ∞, given any ≤ 15 non-truth columns): every
  start-mode maximiser has size K or contains 𝒩_n minus the truth blocks. Under those hypotheses any Q admitting a
  sandwich has |Q ∖ S₀| ≥ min(K − s₀, |𝒩_n| − 15s₀). The lemma "says nothing about whether LS0 or the full method
  reaches S₀ from a large start mode" (APP `lemmas/L5_VN.md:9-11`).
* (S) Successful designs with larger leakage sets: LOC2 L6 (relevance envelope n^{1/(2α)}, polynomial decay
  α > 17/2); UNI-1 (full lattice Q = [p], one factor, limsup log p/log n < α₀(κ̄)). So a polylogarithmic leakage set is
  not necessary for those designs. Observed: numerics L1 (§6).
* (S) **GEN (C6) under the shipped cap.** GEN (C6) (`Theory_work/Wave1/W1-GEN/STATEMENT.md:145-155`; design 𝒲 of GEN
  `lemmas/L7_counterexample.md:14-36`) is an exact-Gram design (p = n − 1, s₀ ≥ 17 fixed orthogonal truths with a
  fixed coefficient θ, σ² = 1, one truth x₀ with d_n = 16(2ℓ_n + 5) proxies x_i = (a/√d_n)x₀ + √(1 − a²/d_n)z_i, all
  other columns orthogonal) on which LS0 with the **old** cap ℓ_n misses S₀ with probability → 1. Under the shipped
  cap ℓ_n + |S̃₀| the design satisfies the hypotheses of Theorem RM-F with Q := S₀ ∪ {proxies} [verification by this
  seat; checked by sweep R08 finding 11, whose corrections are incorporated]:
  (T1-F) = (H0): proved in the source (its (W2): fixed s₀, A = 1, ‖μ‖² = (n − 1)s₀θ², floors at every order from
  λ_min(Σ) ≥ 1 − a (its (W1)), BM-∞); (FL-16), (FL-Q) with φ₀² = 1 − a by (W1) and interlacing;
  (V) [C2-B1]: for j = x₀, every other truth is orthogonal to x₀ and to all proxies and nulls, hence to
  span(x₀, X_U) or contained in U, so u_{U,x₀} ⊥ x_k for k ≠ x₀; for a truth j ≠ x₀, x_j is orthogonal to every other
  column, so u_{U,j} = x_j/‖x_j‖, which is orthogonal to every other truth. In both cases
  δ²_{U,j} = θ²‖(I − P_U)x_j‖² ≥ θ²(n − 1)(1 − a);
  (L-gain) with η = 0: a null outside Q is orthogonal to every other column and to μ;
  (L-size): |Q| = s₀ + d_n = O(log n); (L-feas): K = ⌊n/2⌋ ≥ 2(s₀ + d_n) + 32s₀ + 1 eventually;
  (N-D)(i) with ρ_n = 0, h = 0 and p directions — special case (c) of `lemmas/L2_NAF.md`: given S₀ the proxies'
  residuals √(1 − a²/d_n)z_i are mutually orthogonal and the remaining nulls are orthogonal to span X_Q;
  (N-D)(ii) (BM-Q): θ²(n − 1)(1 − a)/(σ²(s₀ + d_n + log n)) → ∞ (fixed θ).
  Hence P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 on (C6)'s design under the shipped cap; the same computation applies to any
  polylogarithmic d_n. (C6) is an obstruction of the old cap, as ADJ_opus stated.
* (F) A failing class outside the feasibility clause: FAC-PK (status, verbatim: "PARTIAL relative to the brief;
  (P1)–(P5) on the exact-Gram stage: PROVED-CHECKED", `Theory_work/Wave2/W2-FAC-PK/REPORT.md:18-19`) [C1-B8]
  (`Theory_work/Wave2/W2-FAC-PK/REPORT.md:24-33`,
  exact-Gram compound symmetry with K < p ≤ n − 1, fixed ρ, nonzero sign-corrected total signal, (PK), (PB)): every
  start maximiser has size K (its (P1)), LS0 with the shipped cap never scores S₀ (Theorem NEG), while the uncapped
  path reaches S₀ after ≤ (1 + δ)|S̃₀| moves (Theorem PATH). This is a counterexample to an unrestricted extension of
  the LS0 route to saturated start modes when K < p; it is a statement about LS0 only (nothing about the full method;
  p ≫ n open), and it does not make (L-feas) or "|Q| < K" necessary for every design (the theorem itself allows
  Q = [p] with K = p). That report proposes a method change for this class — an LS0 cap ≥ max(ℓ_n, ⌈(1 + δ)|S̃₀|⌉),
  recommended ℓ_n + 2|S̃₀| ("Method change proposed (HQ decides)", `Theory_work/Wave2/W2-FAC-PK/REPORT.md:4-6`); it is
  not adopted in the shipped configuration that Theorem 3 assumes, and Theorem 3 would hold a fortiori with any larger
  cap (RM-0(a): the cap is never binding on the good event).
* (O) Leakage sets between polylogarithmic and the saturation regime. R02 P5 sketches a design-agnostic route to
  |Q| ≤ n^b, b < ¼ (and b < ½ − η/2 − √(2Aη) in Form F): toolkit at actual cardinalities, NA threshold losing
  2b log n, junk-exclusion margin losing b log n. MEDIUM risk, 3–5 proof days. **Recommended to HQ as the most
  valuable follow-up.**

### 3.3 The localisation clause (L-loc-R) (Form R only)
* (P) It is what the present route uses to handle the X-measurable partition: realised conditioning sets are
  data-selected, a union over all p^{15} sets would cost 32 log p against a budget of log n + 2 log p, and
  (L-loc-R) reduces them to n^{o(1)} references per column. Rate adopted: r_n = o((n log n)^{−1/4}) (R02 P3a;
  `lemmas/L3b_rate.md`). Recorded, not adopted: r_n = o((log n/n)^{1/4}) if the factor e^{ω_n/2} is carried (R04 F8).
* (O) Removing localisation (e.g. through a selection theorem for the coded clustering rule): open (R02: no valid
  shortcut found; HIGH).

## 4. The lattice condition (N) / (D-R)

* (P) Why it is there: the descent lemma (GROW L1) uses no-addition at every set of the lattice [S₀, Q]
  (2^{|Q∖S₀|} sets). (N-χ) uses the common-χ² upper bound Z²_{T,l} ≤ Z²_{Q_l,l} + χ²_{|Q∖S₀|}, which gives the range
  |Q ∖ S₀| ≤ (1 − δ₀) log n; whether that bound is attained by actual residual families is not established. A direct
  union ((N-D)(i) with ρ_n = 0, N_l = Q ∖ {l}, h < ½) gives |Q| < log n/(2 log 2). Beyond these, a condition on the
  directions {u_{T,l}} is used: (N-D)(i) (fixed design), (R1)–(R3) (Gaussian rows).
* (O) (N-D)(i) is not established from (V), (L) and the floors, and no proof that it can fail under them is given.
  **Heuristic design** (probe N1, `numerics/SPEC.md`; an exact-Gram design at fixed p in the probe, not an asymptotic
  counterexample): m orthonormal columns 𝒫 ⟂ S₀; outside columns x_l = cos(a)w_l + sin(a)m^{−1/2}Σ_{t∈𝒫}x_t. For the
  lattice set T_τ := S₀ ∪ {t ∈ 𝒫 : ε̂_t ≤ τ} (ε̂_t the noise coordinate of x_t), the residual direction of x_l is
  cos′·w_l + sin′·r̂ with r̂ the normalised sum of the removed columns, so Z_{T_τ,l} = cos′Z_l + sin′g(τ),
  g(τ) = Σ_{ε̂_t>τ}ε̂_t/√|{ε̂_t > τ}| ≈ √m·φ(τ)/√Φ̄(τ) (law of large numbers heuristic), maximal at τ ≈ 0.61 with
  g² ≈ 0.40m; with tan′ = g/Z_l the statistic is ≈ √(Z_l² + g²), i.e. sup Z² ≈ 2 log p + 0.40m, which exceeds
  c_n ≈ 2 log p + log n once m ≳ 2.5 log n. None of this is proved; exceeding c_n is not by itself a violation of NA
  (the score conversion is one-way); and in this design nothing leaks, so the theorem applies with Q = S₀ — the probe
  concerns whole-lattice NA on an unnecessarily large lattice. Observed: numerics N1 (§6).
* (P) What LS0 actually needs. NA on all deletion children T ∖ {e} is a *sufficient* way to make every swap (e → l)
  worse than the corresponding deletion of e (F((T ∖ e) ∪ l) − F(T ∖ e) < 0); it is stronger than necessary for a
  deletion-only greedy path, which only requires, at each visited set, that the best deletion score exceed the best
  swap and the best addition score. (S) On the FAC-PK class (`Theory_work/Wave2/W2-FAC-PK/REPORT.md:24-33`) the
  **uncapped** LS0 path reaches S₀ (Theorem PATH) although, by Theorem NEG, its first ⌊n^β⌋ moves are swaps: a proved
  example of a greedy path that is not deletion-only and still ends at S₀. With the shipped cap LS0 does **not** reach
  S₀ on that class (Theorem NEG; §3.2 (F)) [C1-B2].
* (P) What a Gram floor gives (R02 P6): min over extras e of the deletion loss satisfies
  min_e D_e/σ² ≤ ‖(P_Q − P_{S₀})ε‖²/(σ²φ₀²|E|) — an inexpensive deletion exists when many extras remain. It does not
  control swaps or additions, the visited sets depend on ε, and no bound on the number of non-deletion moves within
  the cap slack ℓ_n + s₀ follows.
* (O) **Open:** whether (V) + (L) + floors suffice without (N) at |Q| ≤ C log n (arbitrary C) or polylogarithmic |Q|.
  Neither a proof nor a counterexample satisfying all assumptions is known (R02: "I neither prove nor refute this
  statement"). HIGH-risk separate ticket (adaptive-path control). Widenings meanwhile: the entropy budget h < ½
  (adopted in Form F) and its analogue for (R1) of NA-R (recommended; it re-opens LOC2's proof).

## 5. Other limits of the statement
* Exact arithmetic: Lemma E4 and every consumer are under EX-A; in binary64 the start-mode identification is
  covered only by PACK Lemma UM-FP (unique maximiser with a margin) and N3 (e).
* Form R is not Form F conditional on X (ASSUMPTION_MAP; R02 P2): a distributional (counting) leakage condition would
  be needed and proving it over X is the selection problem.
* [POST] is Theorem 1 (PROGRAM item 1). The pathwise argument needs only that S₀ be the unique F-maximiser among the
  scored models with probability → 1; π(S₀) > ½ is the sufficient event used. Necessity of posterior concentration
  is not claimed.

## 6. Boundary-violation numerics (observations only; PROTOCOL item 3)

Source: `numerics/SUMMARY_SHARPNESS.md` (generated by `numerics/build_summary.py` from `v1_results.csv`,
`l1_results.csv`, `l2_results.csv`, `n1_results.csv`; deviations from `numerics/SPEC.md` are listed at its top).
Ported method objects (not the production code); p ∈ {200, 300, 400}, n ∈ {400, 1600, 6400}; "held" = LS0 from the
start mode with the shipped cap ends at S₀ with a completed scan finding no strict improvement. Counts are runs. They
are observations at these sizes, not evidence about any limit; the theorems are asymptotic.

| id | assumption probed (classification nominal for V1, L1, L2; exact for N1) | how | conclusion held outside it | other observations | flag |
|---|---|---|---|---|---|
| V1 | (V) | a truth j with Cov(W_j, signal) = 0 (and = 0 given its block-mates), j and its partner in different blocks (V1a, V1a13) or in the same block (V1b) | 296/300 runs (V1a: 118/120; V1a13: 60/60; V1b: 118/120) | when j is separated from its partner at p = 400 it is in the start mode in 0/60 runs and LS0 brings it in in 60/60 (59 by an addition move, 1 by a swap; the search then ends at S₀ in 58/60); in the same block (V1b) both truths are selected jointly in 120/120 runs although (V) fails | `improvable` |
| L1 | (N-χ) / size of the leak set | one truth in an equicorrelated group of size g ∈ {8, 32, 128} | with g − 1 > log n: 138/140 (old cap ℓ_n: 89/140) | \|S̃₀ ∖ S₀\| up to 64 at g = 128, n = 6400 (log n = 8.8); every move a deletion of an extra in 169/180 runs | `improvable` (size); the old cap is observed to fail (cf. GEN (C6)) |
| L2 | leak strength (exploratory; nominal population strength, see the note below) | Gaussian rows; every non-truth column a weak proxy of the single truth with population n r² = η log n, η ∈ {0, 0.5η_A, 2η_A, 0.5, 1, 2} | nominal η > nominal η_A: 418/420 (old cap: 354/420) — of which the 2η_A cells, which sit at the nominal τ-normalised boundary (note below): 119/120, and η ∈ {0.5, 1, 2}: 299/300; nominal η ≤ 0.5η_A: 240/240 | a proxy is in the start mode (the sandwich with Q = S₀ fails) in 0/240 runs at η ≤ 0.5η_A, 7/120 at η = 2η_A, 33/120 at η = 0.5, 109/120 at η = 1, 60/60 at η = 2; with up to 69 proxies in the start mode LS0 still ended at S₀ in 208/209 | larger leaks are observed to enter the start mode and to be deleted by LS0; no assumption is certified violated or satisfied |
| N1 | (N-χ) / whole-lattice NA | heuristic exact-Gram design of §4, m = ⌈C log n⌉, C ∈ {1, 2, 4, 8} | LS0 from the start mode: 179/180 (the start mode is S₀ in every run: nothing leaks) | a true NA violation (F(T ∪ l) > F(T)) was found on the searched part of the lattice in 90/180 runs (C = 4, 8: 60/60); LS0 started from the forced centre Q still ended at S₀ in 178/180 (deletions only in 171/180), and from the worst adversarial centre in 178/180 (all moves deletions of extras in 95/180); inside (N-χ) (m ≤ log n, C = 0.5): no NA violation found in 59/60 runs (one finite-n violation), LS0 from Q ended at S₀ in 60/60 | whole-lattice NA is observed to fail while the greedy path still reaches S₀: `improvable` (§4, open) |

**Note on "outside the assumption" (council C1, seat A, finding 1).** N1 is an exact-Gram fixed design: its
classification (m versus log n) is exact. V1, L1 and L2 use Gaussian rows and their classification is **nominal**:
it is defined through the population design (a population covariance equal to 0 in V1; the number g − 1 of
population-visible nulls in L1; the population proxy strength η in L2). The sample conditions of Form F were not
measured in any of them, and for L2 in particular: (i) the stored quantity is the population n r², not the realised
δ²_{U,l}/(τ²_U log n) uniformly over columns and conditioning sets; (ii) with θ = σ = 1 the residual-variance
normalisation of STATEMENT v1.2 gives τ²_∅ = 2, so the nominal τ-normalised strength is η/2 (the cell labelled 2η_A sits
at the nominal boundary, not at twice it); (iii) the column η_A of the L2 table uses the cellwise A = log p/log n, often
below 1, whereas the theorems fix A ≥ 1 (η_A ≤ 0.101); (iv) in Form R terms every η > 0 has n r² → ∞ and lies outside
the leak rate of (L-gain-R) asymptotically. L2 is therefore an exploratory experiment on leak strength: it shows
larger population leaks entering the start mode more often and being deleted by LS0; it does not locate a threshold
and certifies neither violation nor satisfaction of (L-gain).

Reading: in each experiment the conclusion was observed, nominally outside the corresponding assumption (exactly
outside for N1; in several cells far outside, e.g. g = 128 in L1), in ≥ 98% of the runs. All cells have p ≤ n; the
regime p > n was not probed [C1-B6]. This is what the analysis of §§2–4 leads one to expect (the assumptions are sufficient conditions of the route),
and it supports the two recommendations of this record: a design-agnostic extension to larger leakage sets (§3.2)
and a path-level replacement of the lattice condition (§4). None of these counts is a proof, and none says anything
about a worst-case converse.

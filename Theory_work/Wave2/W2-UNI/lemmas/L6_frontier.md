# L6 — Frontier: Lemma OBS-k (k ≥ 2), partial versions, absorption plan

Status: Lemma OBS-k **PROVED (by this seat, unchecked)** — v1, 2026-11-09; the rest is a plan (no claim). Check: R03 (Codex gpt-6.1-sol xhigh): OBS-k VERIFIED; file VERIFIED-WITH-AMENDMENTS
(items 5, 6 — wording narrowed, applied).
Falsification numerics [R05a-15]: `numerics/n5_obsk.py` → `numerics/n5_obsk_out.txt` (k ∈ {2, 3}, m ∈ {1, 2, k, k + 1, 5}
including m ≥ k, p up to 3200, non-diagonal AR-type Ψ ⪰ 0.6I, random bounded loadings): the proof's construction of T gives
an information ratio decreasing towards 0 as p grows (e.g. k = 2, m = 5: 3.8e-4 → 3.4e-8; k = 3, m = 5: 6.3e-4 → 8.3e-7),
0 violations of the proof's chain I(T) ≤ c⁻¹Σ_{j∈T}(Λ_jᵀu)²/|T| ≤ η²/c, while I([p]) stays ≈ 0.10–0.26 for p ≤ 800 (not computed at p = 3200) [C1-B NIT-1]; for m < k the
ratio is 0 trivially (rank). The R01-7 example (k = 2, alternating √a e₁/√a e₂ rows) gives I([p]) ≈ 0.11 but I(T) = 0 for
m rows of one type, consistent with the scope paragraph.

## L6.1 Lemma OBS-k (STATEMENT (iii′)(a))
Fix k ≥ 2 and an integer m ≥ 1 independent of n. Let p_n → ∞, Λ_n ∈ ℝ^{p×k} with rows ‖Λ_j‖ ≤ L (fixed), and
Ψ_n ⪰ cI (c > 0 fixed). Then inf_{m≤|T|≤p_n} λ_min(Λ_TᵀΨ_TT⁻¹Λ_T)/|T| → 0.
*Proof.* Fix η > 0. Ψ_TT⁻¹ ⪯ c⁻¹I, so for every unit u ∈ ℝ^k, λ_min(Λ_TᵀΨ_TT⁻¹Λ_T) ≤ c⁻¹uᵀΛ_TᵀΛ_Tu = c⁻¹Σ_{j∈T}(Λ_jᵀu)².
Since k ≥ 2, every row Λ_j has a unit vector u_j ⊥ Λ_j. Put L_* := max(1, L) > 0 [R05a-17] (so ‖Λ_j‖ ≤ L_*). Cover the
unit sphere S^{k−1} by M(η) sets of diameter ≤ η/L_* (M(η) finite, depending on (k, η, L_*) only). For p_n ≥ mM(η), some
set contains u_j for at least m indices j; let T be m of them and u any one of their u_j. Then
|Λ_jᵀu| = |Λ_jᵀ(u − u_j)| ≤ L_*·η/L_* = η for j ∈ T, so λ_min(…)/|T| ≤ η²/c. As η is arbitrary, the
infimum tends to 0. ∎
*Scope.* This obstructs only an extension of L3_ULOC (d) that would require c_𝒢-type uniform positive information
λ_min(Λ_TᵀΨ_TT⁻¹Λ_T) ≥ c₁|T| on every subset of size ≥ m (the matrix analogue of (A2-1) with singleton groups). It does not
obstruct conditions imposed only on large subsets, other proofs for k ≥ 2, or consistency (k = 2 designs with
λ_j ∈ {√a e₁, √a e₂} have positive information on [p]; R01 item 7). In the k-factor version of L3_ULOC(a) the factor part
is the projection on the k-dimensional space 𝓚_T ⊖ 𝓗_T = span((I + S_T)^{−1/2}ω_T), ω_T := ξ − Λ_TᵀΨ_TT⁻¹ζ_T,
S_T := Λ_TᵀΨ_TT⁻¹Λ_T (the same Pythagorean argument; not claimed here). [R03-5] OBS-k alone gives neither a bound on
nonzero eigenvalues nor an entropy bound for weak subsets. A k-factor extension must control the factor contribution
without assuming this impossible uniform full-rank floor; possible approaches include bounds sensitive to directions and
residual loadings, stratification of sets when justified, or a path argument.

## L6.2 Partial versions (family-specific, beyond UNI-1)
* **FACB Theorem FAC-CS** ("PROVED-CHECKED", W2-FAC-B/REPORT.md): exact-Gram compound symmetry, any p ≤ ⌊n/2⌋, under
  (FS)/(FS′) — k = 1, Ψ = (1 − ρ)I, κ = 1: beyond α₀(1) = 1/6 via the path route. A clearly-marked partial version of the
  target "UNI-1 for every p ≤ n^A".
* **FACA Proposition SHARP** ("PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" inside W2-FAC-A) [R03-6]: for exact CS, SHARP rules out full-lattice NA
  beyond 1/6; covering those exponents requires replacing that route, for example by a path argument. Necessity of
  α₀(κ̄) for other representations has not been established.

## L6.3 Absorption plan (which general hypothesis each parallel ticket would discharge)
| Ticket (status at writing: running) | Target | If proved, it upgrades … |
|---|---|---|
| W2-FAC-S5 / S5F | block CS, exact Gram, p ≤ n/2 (reduction to a global-centre condition) | UNI-1 beyond α₀ for Ψ block-CS (bounded groups): a "path" version of (iii) for the block-local Ψ subclass of LOC_M |
| W2-FAC-X / XA | iid rows CS; general one-factor loadings (exact Gram, then iid) | (R)-design and heterogeneous-λ versions of the path route: the first step toward "(iii) for all p ≤ n/2 under (A2-1)" with Ψ diagonal |
| W2-FAC-K2 | k ≥ 2 factors | (iii′): a k-factor U-LOC must achieve control of weak directions without a uniform full-rank subset floor, or use the path |
| W2-FAC-PK / PKA | p > K = ⌊n/2⌋ (saturated start, swap phase) | removes "p > K_n in (iii)" from Not-claimed; may require a cap change (METHOD_REQUIREMENTS, HQ decides) |
Mapping rule [R05a-9]: a source result is a corollary of an existing UNI theorem only after its hypotheses are shown to
imply all hypotheses of that UNI theorem. To use a parallel result to prove an extension under (A1)–(A3) plus a named
population-level condition, show that those proposed hypotheses imply the parallel result's hypotheses; such an extension
is stated and reviewed separately. Otherwise the parallel result is listed as a family-specific partial version.

# W2-FAC-A — STATEMENT (target statement)

Ticket W2-FAC-A, Theory Wave 2 (route A: low-rank common-component split). Lead: Claude Opus 5.5.
Status of this file: **v1.2 — LOCKED** (v1.2 = R06 sweep wording fixes, no hypothesis or claim changed) after statement-lock review R01 (Codex gpt-6.1-sol high,
LOCK-WITH-CHANGES; all ten required changes applied, see reviews/R01_disposition.md). Later changes are logged in
LOG.md and flagged in REPORT.md.

Abbreviations: FINAL = `Theory_work/Wave1C/FINAL/sections/`; GROW = `Theory_work/Wave1C/C-GROW/`;
GEN = `Theory_work/Wave1/W1-GEN/`; PXN = `Theory_work/Wave1/W1-PXN/`; DLV = `Theory_work/Wave1C/C-DLV/`;
A1/A2/A3/A4 = `Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md`, `A2_propF_GROW.md`, `A3_check_A2.md`,
`A4_postcouncil_check.md`. Scope rule (Wave 2 PROTOCOL): all results are asymptotic; no finite-n claim.

## 0. Target, diagnosis, and what changes vs the brief

**Brief.** Theorem FAC: for the method as merged (v3.1, main 4676af6), on factor designs Σ = ΛΛᵀ + Ψ with growing
p ≤ n^A, fixed s₀, fixed k: D_n → 0 and P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, then delivery P(Ŝ⁺ = S₀) → 1.

**Diagnosis (observations, not proofs; numerics/ and LOG.md).** (i) In the tested factor designs the start mode
tends to all of [p] as n grows (exact-Gram simulator, numerics/D2_summary.md, p ∈ {100, 200, 400}: S̃₀ = [p] in every tested
CS3/CS5/S5 run with n ≥ 10⁶ and every tested F2 run with n = 10⁷); the number of extras is then of order p, so when
p/log n → ∞, Q = [p] violates GROW's logarithmic size bound in (G1) and (G4-χ) ((G4-dir) is not asserted to fail). (Whether a given null is block-visible depends on the conditional, not marginal, factor
signal; it can cancel. This is not used below.) (ii) The add statistic depends on the design only through the Gram
matrix; for one global factor plus block-local structure it splits along the residual factor direction into an
idiosyncratic normal depending on T only through U = T ∩ g(l) and one residual-factor statistic per T (lemmas/L1). (iii) NA over the whole lattice fails
on one-sided lattice sets in tested rows with log p/log n > 1/6 (numerics/D2_lattice.md, e.g. CS3 p = 400,
n = 10⁷: 3/5 runs), while the MR1 search scored S₀ in every tested run (D2_summary.md "MR1 ok"). (Isolated one-sided failures
below 1/6 at small n, e.g. FNA_summary.md a = 0.3, s₀ = 4, n = 10⁶, p = 7, reflect bounded constants such as C_ω
when log p is small; 1/6 is an asymptotic boundary, not a finite-n threshold.)

**What is targeted.** Part I — Theorem FAC-L: reported-model consistency (and, with the total fallback, delivery)
for the class 𝔉 "one global factor + block-local idiosyncratic structure" (compound symmetry, block compound
symmetry, study S5), for fixed designs with exact or approximate factor Gram and for iid Gaussian rows, under the
sufficient strict growth condition (P). Part II — Proposition SHARP: for exact-Gram compound symmetry the exponent
1/6 of (P) is optimal for the full-lattice route (NA over the lattice fails with probability → 1 above 1/6).
Necessity for S5, other class members, approximate Grams or random rows is **not** asserted. Part III — frontier
(evidence only).
**Narrowing vs the brief (flag):** the strict growth condition limsup log p/log n < α₀(κ̄) (= 1/6 for every block
compound symmetry, incl. CS and S5) instead of p ≤ n^A; one global factor (+ bounded-size local blocks) instead of
fixed k.

## 1. Setting (as GROW STATEMENT §1; FINAL s1)

* **D0 / score / prior / start.** As in FINAL `s1_setting.tex` (shipped g = n score, IG(0.01, 0.01), capped
  BB(1, p) with w(k+1)/w(k) = (k+1)/(2p−1−k), K = min(p, ⌊n/2⌋), Ω = {|S| ≤ K}; F(S) = log w(|S|) + log m(S);
  block tables r_b, start γ₀, start mode S̃₀ = argmax_Ω γ₀; blocks C_b of size ≤ 16, the method's actual partition).
* **G (fixed design).** Raw design X^r (n × p, nonconstant columns), y^r = α1 + X^rβ + ε, ε ~ N_n(0, σ²I),
  σ² > 0 fixed; X = CX^rD_x⁻¹ (centred, ‖x_j‖² = n − 1), response centred and scaled to yᵀy = n − 1 inside the
  score; μ := CX^rβ = Xθ*, S₀ := supp β, s₀ := |S₀| ≥ 1 fixed; R̂ := XᵀX/(n − 1).
* **Random design (iid rows).** Raw rows iid N(m, Σ_n) with Σ_n a correlation matrix, columns standardised as
  above; ε independent of X^r; fixed s₀, fixed σ² > 0, fixed nonzero coefficients θ*_{S₀} on the standardised scale,
  Y = Xθ* + Cε (study generator convention, GEN STATEMENT (C5)(d), GROW STATEMENT (C5)(c)); joint law.
* **Method.** v3.1 as merged on main at 4676af6: LS0 from the start mode with move cap ℓ_n + |S̃₀| (MR1 (C-GROW)),
  all other caps ℓ_n = ⌈log₂(n + p + 1)⌉, tie-aware start DP; Ŝ⁺ = maximum of the all-scored set.
  **Premises for (L4)/(L5):** as GROW: EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0 (cap ℓ_n + |S̃₀|), "the emitted LS0
  centre is some maximiser of γ₀" (satisfied by the coded routine, W1-N3(a)), complete scans; IND-T and the c₄
  search when R′ > 4. **Premises for (D):** those of Proposition F (FINAL s6), listed in (D) below.
* **Lattice.** 𝓛 := {T : S₀ ⊆ T ⊆ [p]}; NA(𝓛) := {F(T ∪ {l}) < F(T) ∀T ∈ 𝓛 with |T| < K, ∀l ∉ T};
  TL(𝓛) := {F(A) < F(T) ∀T ∈ 𝓛, ∀ feasible neighbours A of T with S₀ ⊄ A}; Sand_n := {S₀ ⊆ S̃ for every
  maximiser S̃ of γ₀ on Ω}.

## 2. The factor class 𝔉

A correlation matrix Σ belongs to **𝔉(γ̄, ψ₀, κ̄)** if it admits a representation (λ, Ψ, 𝒢) — a partition 𝒢 of [p]
into groups of size ≤ γ̄, λ ∈ ℝ^p with every λ_l ≠ 0, Ψ block-diagonal w.r.t. 𝒢 with λ_min(Ψ) ≥ ψ₀ > 0 — with
Σ = λλᵀ + Ψ and κ(λ, Ψ, 𝒢) ≤ κ̄, where for l ∈ [p], U ⊆ g(l) ∖ {l}:
  ψ_{l|U} := Ψ_ll − Ψ_{lU}Ψ_UU⁻¹Ψ_{Ul},  λ̃_{l|U} := λ_l − Ψ_{lU}Ψ_UU⁻¹λ_U,
  c_min := min{λ_VᵀΨ_VV⁻¹λ_V : ∅ ≠ V ⊆ g ∈ 𝒢} (> 0),  κ := max_{l,U} |λ̃_{l|U}|/√(ψ_{l|U}c_min),
for a chosen admissible representation (existential definition; κ is representation-dependent). Always κ ≥ 1
(take U = ∅ and V = {l} for the l attaining c_min). The groups are unrelated to the method's blocks.

**Growth exponent.** α₀(κ̄) := 1/(2 max_{r∈[0,1]}[(1 + κ̄r)² − r²]) = 1/(2κ̄(κ̄ + 2)) (κ̄ ≥ 1); α₀(1) = 1/6.
*Derivation (to be proved in L3):* for p → ∞ and 1 ≤ k ≤ p − 1 put r² := log(p/k)/log p. The leading squared L1
bound on the add statistic at |T| = k is 2 log p (1 + κ̄r)², whereas the NA budget with the exact BB ratio is
log n + 2 log((2p − 1 − k)/(k + 1)) = log n + 2r² log p + O(1). The strict inequality needed is
2 (log p/log n) max_r[(1 + κ̄r)² − r²] < 1. Bounded or subpolynomial p are covered by the log log n allowance.
(Charging only log n would give 1/8 for κ̄ = 1; the BB ratio is essential.)

**Block compound symmetry has κ = 1** (to be proved in L5): Σ = ρ_b11ᵀ + (ρ_w − ρ_b)H + (1 − ρ_w)I with fixed
0 < ρ_b < ρ_w < 1, H the indicator of fixed-size groups; λ = √ρ_b 1, Ψ = (ρ_w − ρ_b)H + (1 − ρ_w)I. With d = 1 − ρ_w,
b = ρ_w − ρ_b, u = |U|: λ̃ = √ρ_b d/(d + ub), ψ_{l|U} = d[d + (u+1)b]/(d + ub), c_min = ρ_b/(1 − ρ_b), and the squared
ratio is d(d + b)/[(d + ub)(d + (u+1)b)] ≤ 1, equality at u = 0. Compound symmetry Σ = (1 − a)I + a11ᵀ (singleton
groups, λ = √a 1, Ψ = (1 − a)I; κ = 1 directly) and S5 (ρ_b = 0.3, ρ_w = 0.7, groups of 5) are instances.

## 3. Hypotheses

* **(H0)** the T03♯ hypotheses with BM-∞ (FINAL s3 Theorem S-T): energy ‖μ‖² ≤ Mn, anchored eigenvalue conditions,
  BM-∞, with fixed constants. (AG) supplies the anchored eigenvalue conditions; the energy bound and BM-∞ remain
  assumptions of the general theorem. For fixed nonzero bounded θ*_{S₀} they follow from fixed s₀, unit-scale
  columns and the Gram floor.
* **(AG) approximate factor Gram.** Σ_n ∈ 𝔉(γ̄, ψ₀, κ̄) with fixed (γ̄, ψ₀, κ̄) and ‖R̂ − Σ_n‖_op ≤ δ_n with
  δ_n√(p log log n) → 0 (δ_n = 0: exact Gram, needing p ≤ n − 1).
* **(P) growth.** limsup_n log p_n/log n < α₀(κ̄) (p fixed or growing). Since α₀ ≤ 1/6, (P) gives p = o(n), hence
  K = p eventually; this justifies the full lattice 𝓛 ⊆ Ω and the cap check.
* **(TV)** = GROW (G3b) on the actual blocks: for a deterministic M_n → ∞, every j ∈ S₀ and U ⊆ C_{b(j)} ∖ {j}:
  δ²_{U,j} ≥ M_n log n.
* **(TV-pop) (random design).** For each n a deterministic family 𝔅_n of subsets of [p] of size ≤ 16 and a
  measurable design event 𝓔'_n with P(𝓔'_n) → 1 such that every realised method block belongs to 𝔅_n on 𝓔'_n, and
  inf_n min{(Σ_{jμ|U})²/Σ_{jj|U} : j ∈ S₀, C ∈ 𝔅_n, j ∈ C, U ⊆ C ∖ {j}} ≥ τ₀ > 0, where Σ_{jμ|U} is the population
  partial covariance of x_j and μ = Σ_{S₀}θ*_ix_i given x_U. One may take 𝔅_n = all sets of size ≤ 16.

## 4. Claims

**Part I — Theorem FAC-L.**
* **(L1) Key lemma U.** For the exact factor Gram (R̂ = Σ ∈ 𝔉) write g := Xᵀε/(σ√(n−1)) = λξ₀ + ζ with ξ₀ ~ N(0,1),
  ζ ~ N(0, Ψ) independent (enlarged space). For every T ⊆ [p], l ∉ T, with U := T ∩ g(l),
  s_T := λ_TᵀΨ_TT⁻¹λ_T and W_T := (ξ₀ − λ_TᵀΨ_TT⁻¹ζ_T)/√(1 + s_T) (empty-set conventions: only empty-index sums/products vanish;
  s_∅ = 0, W_∅ = ξ₀, ψ_{l|∅} = Ψ_ll, λ̃_{l|∅} = λ_l, Ξ_{l,∅} = ζ_l/√Ψ_ll), the add statistic is exactly Z_{T,l} = [√ψ_{l|U} Ξ_{l,U} + (λ̃_{l|U}/√(1 + s_T)) W_T]/√(ψ_{l|U} +
  λ̃²_{l|U}/(1 + s_T)), Ξ_{l,U} := (ζ_l − Ψ_{lU}Ψ_UU⁻¹ζ_U)/√ψ_{l|U}; and on an event of probability ≥ 1 − 3/log n,
  simultaneously for all T, l: |Z_{T,l}| ≤ √(2 log(p2^{γ̄}) + 2 log log n) + κ'√(2 log log n) +
  κ̄(√(2 log(eγ̄p/|T|)) + ϱ_n)·1{T ≠ ∅}, ϱ_n = O((log p)^{1/4} + (log log n)^{1/2}) deterministic, κ' := κ̄√c_min.
  Under (AG) the bound transfers by coupling to this factor-Gram Gaussian vector with a uniform additive error
  O_P(δ_n√(p log log n)) = o_P(1). The displayed envelopes and their O(·)/o(·) remainders are deterministic and
  uniform in (T, l); the coupled random discrepancy is O_P(δ_n√(p log log n)) uniformly (L1 Corollary U gives an
  explicit deterministic allowance on an event of probability ≥ 1 − 4/log n); constants depend only on (γ̄, ψ₀, κ̄).
* **(L2) Sandwich.** Assumes G, the energy bound, (AG), (P), (TV): P(Sand_n) → 1.
* **(L3) Descent events.** Assumes G, (H0), (AG), (P): P(NA(𝓛)) → 1 and P(TL(𝓛)) → 1.
* **(L4) Main (fixed design).** Assumes in addition (TV) and the method premises of §1: D_n ≤ P(Sand_nᶜ) +
  P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0; hence P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n). On
  Sand_n ∩ NA ∩ TL, the prescribed deterministic LS0, viewed as an uninterrupted search on these data, reaches S₀
  after exactly τ := |S̃₀ ∖ S₀| deletion moves and scores it by the scan after max(τ − 1, 0) moves (the centre is
  scored when τ = 0), within the merged cap; a delivered SMC run executes this search, and the exact-enumeration
  branch scores S₀ directly. No delivery claim in (L4).
* **(L5) Random design.** Iid rows with Σ_n ∈ 𝔉(γ̄, ψ₀, κ̄), (P), (TV-pop), fixed s₀, fixed σ² > 0, fixed nonzero
  θ*_{S₀}, independent Gaussian noise, and the method premises of (L4) interpreted conditionally on the design: the
  conclusions of (L2)–(L4) under the joint law (design events = entrywise correlation concentration ∩ 𝓔'_n, H0 and TV
  verified on the same events with common envelopes, every-deterministic-sequence/diagonal argument as GEN (C4), GROW
  L6; conditional convergence alone is not used).
* **(D) Delivery (Proposition F-FAC).** Relative to Proposition F's abstract unit-cost/unbounded-word machine and its
  premises — EX-A (unit-cost reals), IDEAL-W, EX-S, SR, e4 with TDP-IMPL (exact start-mode maximiser), GUARD-W, MACH,
  CONFIG with fixed declared R′ = 4k and fixed worker count, OP-LS0 with cap a_n = ℓ_n + |S̃₀|, complete fallback-grid
  freezing (total tier-1 fallback), valid declared seed, and the raw-dimension allocation of A1's corrected statement
  including the A4 preflight addition; inheriting the P1/S.3 code-audit qualifications — and adding the classes of
  (L4) and (L5) (for which the retained p equals p_raw almost surely): P(no output) = 0 for every admissible n ≥ 3
  (inherited Proposition F conclusion), and P(Ŝ⁺ = S₀) → 1 (original unconditioned noise law, resp. joint law; new
  statistical assertion, via the event 𝒦_n = "deterministic LS0 with cap a_n scores S₀", NOT inferred from D_n → 0).
  CAL is not assumed. This premise list is stronger than the "some maximiser" premise sufficient for (L4).
* **(I) Instances.**
  (a) *Exact-Gram compound symmetry*: XᵀX = (n−1)[(1 − a)I + a11ᵀ], fixed a ∈ (0, 1), p ≤ n − 1 with
  limsup log p/log n < 1/6, fixed s₀ and fixed nonzero θ*_{S₀}, σ² fixed, any partition with blocks of size ≤ 16,
  under the genericity condition **(GC-CS)**: for every j ∈ S₀ and every U ⊆ [p] ∖ {j} with |U| ≤ 15,
  θ*_j + a(Θ − Σ_{i∈U}θ*_i)/(1 − a + a|U|) ≠ 0, where Θ := Σ_{i∈S₀}θ*_i and null coefficients are zero (finitely many
  distinct expressions as p varies, hence a uniform positive partial-signal minimum).
  (b) *Iid rows, compound symmetric Σ*: same a, exponent, fixed nonzero θ*_{S₀}, (GC-CS), independent Gaussian noise;
  𝔅_n = all sets of size ≤ 16.
  (c) *S5* (block CS ρ_b = 0.3, ρ_w = 0.7, groups of 5; `Scripts/Data_generators/gen_dev_data.R`, scenario 5), exact
  Gram and iid rows (= study S5), with the truth layouts (i) the C-GROW diagnostic layout (s₀ = 4, indices 2, 26, 53,
  75 (0-based), coefficients c(1.4, −1.0, 1.8, −1.2), GROW STATEMENT (C5)(b), numerics/d_common.py there) and (ii) the
  study's high-p layouts of GEN STATEMENT (C5)(d) (s₀ = 14, step 7 or 13, the R code's positions, cycled pattern
  (1.4, −1.0, 1.8, −1.2, 0.8, −1.6)), fixed scale c > 0, extended as theoretical sequences p_n = 5G_n; (TV) /
  (TV-pop) by an exact certificate either over 𝔅_n = unions of ≤ ⌊16/5⌋ whole groups, after proving that the
  complete-linkage cut and next-fit packing produce such blocks on a design event, or over all sets of size ≤ 16.
  (d) General block CS (ρ_b, ρ_w, group size): κ = 1, exponent 1/6, with the analogous TV condition.

**Part II — Proposition SHARP.** Exact-Gram compound symmetry with fixed a ∈ (0, 1), fixed s₀, fixed nonzero
θ*_{S₀}, fixed σ² > 0, model G: if liminf log p_n/log n > 1/6 and p_n ≤ K, then P(NA(𝓛)) → 0. Witness: m := ⌈log p⌉,
T := S₀ ∪ {the m null coordinates with the largest idiosyncratic ζ}, l := the null coordinate with the smallest ζ;
|Z_{T,l}| = (2 + o_P(1))√(2 log p) against the budget log n + 2 log p + o(log p); the score comparison for this
witness is proved separately (small-model argument, p possibly comparable to n). Nothing is claimed at equality 1/6.
This is a necessity statement for the full-lattice route, not a method inconsistency result.

**Part III — Frontier (evidence only, not claimed).** (i) *Path route for log p/log n ≥ 1/6, p ≤ K.* In exact-Gram CS
the score is an exact function of (k, Σ_T z_j², Σ_T z_j), z = Xᵀy (Lemma CS-1D, numerics/cs1d.py, agreement 5.6e-9
with the exact scorer); Lemma GAP (L8): for LS0 started at [p] whose moves so far are deletions of nulls, each the
element of the current set closest to its centre c_T, the deleted set is a contiguous run in the order of the null
z-values and c_T lies between the adjacent kept nulls. Numerics: in numerics/D2_summary.md the MR1 search reached S₀
in every run; paths were pure deletions in all CS3/CS5/S5/F2 rows with n ≥ 10⁵ (F2r, p = 200, n = 10⁷: 4/5 pure, one
swap, path-NA failing in 1/5) and not in all rows at n = 10⁴ (e.g. CS3 p = 400, n = 10⁴: 1/5 pure,
7 swaps; S5 p = 200, n = 10⁴: 3/5 pure, path-NA failing in 2/5). (ii) *p > K* (start mode capped at K): not tested at
asymptotic sizes; a swap phase longer than the MR1 slack is conceivable (heuristic only). (iii) *k ≥ 2 global
factors*: the present scalar residual-factor proof does not cover multiple global factors; any claimed lattice
obstruction would need a specified loading array and a proved lower bound (conjectural).

## 5. Not claimed

Finite-n statements; p ≤ n^A for exponents ≥ α₀; necessity of (P) outside exact-Gram CS; k ≥ 2 global factors;
anything for v3/v3.1 without LS0; changes to shipped components (none needed).

## 6. Dependencies (statuses verbatim)

M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; S-T/T03♯ "PROVED; SF VERIFIED (W2-VT03R);
XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; C-GROW
"PROVED-CHECKED" (L1 descent used verbatim; L3.3(a) re-proved here for the Q = [p] branch); Lemma CR / [CONC′]
"PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)"; Proposition F (cap ℓ_n form) "PROVED-CHECKED for the
patched calibration law"; A1 corrected statement (cap a_n) checked by the final council round 3 (PASSED), A4
"OK-WITH-FIXES"; A2 "PROVED (A2), checked by A3".

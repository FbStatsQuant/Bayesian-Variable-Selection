# W3-DIST — ASSUMPTION_MAP (sharpness gate; v1.1, 2026-11-15; v1.1 = after blind read S1, findings S1-10 applied)

Where each assumption enters the route of ROUTES.md, whether it looks necessary, and the boundary-violation numerics
that test it (helper H2, `work/numerics/RESULTS.md`; readings are filled in §3 after the run). Candidate level.

## 1. Assumptions of DIST-1 / DIST-2 / DIST-3
| id | assumption | enters at | necessity reading | boundary test |
|---|---|---|---|---|
| A-G | Gaussian noise, independent of the design | X1 (χ² tails), X2 (conjugacy), Lemma S | as in [SL] model (1). Sub-Gaussian noise would change the working model's exactness; not a target. | none |
| A-iid | rows i.i.d. | Lemma T only | needed for a *population* distance; the in-sample core is design-conditional | none |
| A-ν | **no** condition on ν_x in the transfer | Lemma T | the claim is that none is needed (truncated distance + VC). `improvable` does not apply; this is the strong form | N2 (t₂.₅, Pareto 2.1, spikes), N6 (ratio ρ bounded) |
| A-sp | strict sparsity, s₀ fixed | X3 (constant M₀ ∝ s₀(A+1)), Lemma S (cost (2p)^{s₀}n^{s₀/2}) | growing s₀ changes rates to s₀ log p/n at best; approximate sparsity is stretch S-APX | N5 |
| A-p | p ≤ n^A | constants in X1, X3; R1 | proof device for constants; S-EXP stretch | N7 (p ≫ n) |
| (E) | ‖μ‖² ≤ nM | X1(iv) (s_y), X3, Lemma S | some bound on signal energy is needed for the s_y-scaled prior; M enters constants only | — |
| (C) | ‖θ*‖² ≤ nM′ | Lemma S and X3 through L_{S₀} ≤ B_{S₀}(θ*) | very weak; replaces (F₀) (cf. [W3P] 1a′). Looks necessary only in this weak form | — |
| (ND) | average determinant growth on supersets up to size m_n(t) | X4(b),(c) only | **not necessary for consistency** (DIST-2 holds without it); needed by this proof for the sharp rate and the full exponent. Whether the sharp rate holds without it is S-FIT (open). Flag: `improvable` pending N4 | N4 (near-duplicate cluster, τ² ∈ {n⁻², n⁻¹, log n/n, 1}) |
| (L₀), δ_n, (TR₀) | DIST-3 only | oracle bound given S = S₀; transfer at the parametric scale | (F₀) of v1.0 was not needed (S1 better-theorem 1): dropped. (TR₀) (second moments on supp β*) is needed by this route at scale 1/n; δ_n enters additively | N1 vs N3 |
| 𝒟_n = {p_ret ≥ 2} | every theorem (remainder) | inherited lemmas need p ≥ 2 | proof device; p_ret ∈ {0, 1} are finite problems to be treated directly | N2c (dropped columns) |
| beta-min | **not assumed** in DIST-1/2 | — | — | N3 (weak signals) |
| [SL] Condition 3 | **not assumed** | — | identifiability is not needed for distribution consistency | N4 |

## 2. Premises of DIST-C (coded output)
| id | premise | enters at | reading |
|---|---|---|---|
| EX-A | exact arithmetic for scores | store weights e^F | inherited convention ([SAMP]) |
| completed | statements are intersected with {completed} | all | P(completed) → 1 not claimed |
| discovery (S₀ ∈ 𝓜) | (C-ii)(α), (C-iv) | supplied by [SAMP] D, RM2, START under their premises; needs beta-min-type selection results | conditional |
| P-STORE | π(𝒯) ≥ η without beta-min | (C-i) | OPEN premise; no output certificate |
| P-HIT | ledger contains one model with π(S′) > e^{−ct/2} | (C-iii) | weaker than discovery; OPEN premise |

## 3. Boundary-violation readings (from `work/numerics/RESULTS.md`)
Run: exact enumeration at p = 12 (4096 models), n ∈ {50, …, 800}, R = 40 replications per cell, 4000 posterior draws
and 20 000 fresh rows per replication; p ≫ n only on a declared **restricted** model family (N7). Finite-n evidence,
p small: it can refute a statement, it cannot establish a rate. Numbers are means over replications.
| test | assumption probed | what was simulated | reading |
|---|---|---|---|
| N1 | baseline | Gaussian AR(0.5), strong signals | n·d² median 1.9 → 1.1, q99 5.5 → 3.2 (n = 50 → 800); log Π(n·d² > t) ≈ −c_t·t, c_t = 1.0 → 1.6. Consistent with DIST-1 and with the parametric scale of DIST-3 |
| N2a, N2b | A-ν (no tail condition) | iid t₂.₅; symmetric Pareto(2.1) (infinite 4th moments) | n·d² median 1.2–1.3 at n = 800, q99 ≈ 3.5, same tail slopes as N1. **No degradation**: supports the claim that the transfer needs no moment condition |
| N2c | A-ν, dropped true columns | spike columns (0 w.p. 1 − 2/n) | a true column was constant in-sample and dropped in 11–17 of 40 replications; n·d² ≈ 0.3–0.4 either way. Supports the treatment of dropped columns in Lemma T; here the in-sample distance *overstates* the population one |
| N3 | no beta-min | two signals at 0.7√(log n/n) | n·d² flat at 1.3–1.4 although the weak signals are selected only 15–20% of the time. Consistent with DIST-1 without beta-min |
| N4 | **(ND)** violated | 6 null columns = x₁ + τ·noise, τ² ∈ {n⁻², n⁻¹, log n/n, 1} | at τ² = n⁻² the true x₁ is selected only ≈ 25% of the time (selection fails), yet n·d² median 1.1–1.5, q99 3.3–3.5, tail slopes as in N1, for all four τ². **(ND) flagged `improvable`**: in this family the sharp rate and the exponential tail survive its violation (evidence for S-FIT; one family, p = 12) |
| N5 | **not a violation of strict sparsity** (S1-10: 12 nonzero coefficients is still fixed finite support); fixed-dimensional weak-signal evidence | β*_j ∝ j⁻², all 12 nonzero | n·d² median 1.8 → 3.3, q99 3.9 → 5.8 (log–log slope 0.22); n·d²/log n flat (slope −0.05); E\|S\| 2.1 → 4.0. Reading: growth compatible with log n (the no-beta-min rate), not with the parametric scale (delayed inclusion of small signals). Says nothing about approximate sparsity proper; S-APX has no numerical evidence yet |
| N6 | Lemma T | ρ = E_x[1 ∧ Δ²/4σ*²] / (2·in-sample truncated mean + log n/n), every posterior draw | max ρ over all draws and designs = 1.004 (t₂.₅, n = 50); pooled 0.999-quantile ≤ 0.9; decreasing in n; spikes 0.14–0.25. No violation of Lemma T's form (which allows ρ up to a constant ≈ d·(A + 2)·4) |
| N7 | A-p (p ≫ n), restricted family | p = 4n and p = min(n^{1.5}, 600), AR and t₂.₅ | n = 50 not yet in the asymptotic regime (n·d² median 4–5); at n = 200: median 0.9–1.5, q99 3.2–4.0, as at p = 12. Restricted family only |
Summary: nothing contradicts a candidate statement. (ND) looks weaker than needed in one simulated family (N4); it is
recorded as `improvable` with the stretch item S-FIT and is not dropped from the targets.
**Limits of these numerics (S1-10).** (1) The tail slopes c_t are from posterior draws pooled over replications: an
*averaged* posterior tail, not the nested statement of DIST-1 (distribution over data sets of the conditional posterior
tail); per replication the resolution is 1/4000. They are finite-n diagnostics, not checks of (1.1). (2) N4 does not
probe the dangerous scale found by H1 (unnormalised Schur eigenvalue ≍ log n/n, i.e. τ² ≍ log n/n² for near-copies);
τ² = n⁻² probes the constant-penalty scale and τ² = log n/n is far above it. **To add in the proof leg:**
τ² ∈ {log n/n², c·log n/n²} and a per-replication (nested) tail estimate with ≥ 10⁵ draws. (3) No simulation is used to
discharge a theorem premise; S1 did not audit the scripts.

## 4. Reader-version assumptions (A1)–(A6) (HQ steer A5)
The primitive assumptions of the reader versions (STATEMENT §1R) map to the interfaces through the bridges:
(A3 for single coordinates) + (A5) ⇒ 𝒟_n, (E), (C) [B1]; (A3) + (A4) ⇒ (ND) [B2-core, B2]; (A1) with any σ* ⇒ unit noise
[B0]; (A4 with fixed ψ on small sets) + (A6) ⇒ δ_n → 0 and (TR₀) [B3, conditional on W3-POST:Thm-1]. Necessity lines:
TARGET.md §6. Boundary evidence: N2 (heavy tails: (A3) violated, no degradation), N4 ((A4) violated at τ² = n⁻²: no
degradation), N3 (no beta-min: Theorem A's rate, not Theorem B's). No simulation tests (A5)'s violation yet
(cancelling large coefficients) — to add in the proof leg.

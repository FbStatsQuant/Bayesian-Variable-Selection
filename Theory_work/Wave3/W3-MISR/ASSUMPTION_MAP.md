# ASSUMPTION_MAP.md — W3-MISR (Wave 3 protocol item 3; written after the statement lock, before proving)

Target statement: `STATEMENT.md` v1.3 (the map was written for v1.1, updated after the better-theorem review BT1, and
reworded after council R1 and sweep SW1; numerical statements below are finite-sample observations at four sample
sizes and 100 replicates, never limits), claims `W3-MISR:R'`, `MIS(i)`, `MIS(i')`, `MIS(ii)`, `Cor-G`, `Cor-H`, `Rem-SNR`,
`Rem-P`, `Rem-U`. Rules: `Theory_work/INFRA/LIFECYCLE.md` §4.3. Numerics: `numerics/N0_code_invariance.R` →
`numerics/N0_out.txt` (compiled code); `numerics/misr_numerics.py` → `numerics/misr_numerics_out.txt` (exact enumeration,
p = 8, 100 replicates, n ∈ {100, 400, 1600, 6400}; random design each replicate; finite-n observations at fixed p,
not limits, and they do not probe growing p).

## Entry map

| hypothesis (id) | where it enters | how | property actually used | necessity evidence so far | early sub-par signal? |
|---|---|---|---|---|---|
| A:MISR-GRC — GR^c: Uᵀ(y^r − xβ) ~ N_N(0, vI) | Lemma R′(b) only | the contrast vector, divided by √v, has the law of the unit-noise G-model; π depends on y^r through it | P: the standardised response has the law it has under a G-model with truth β/√v | scalar covariance: arbitrary non-scalar residual laws cannot be admitted with the same mean-only target — C-MIS E2 (a common random slope) is a counterexample, and in N3(iii) E π({0}) goes 0.23, 0.12, 0.03, 0.02 for the mean-only target; the slope can be put in 𝓕_n (§4). Scalar covariance itself is not necessary: under (PR) (R′(c)) the contrasts may be non-scalar, with β a reference target rather than a conditional-mean coefficient [SW1-2]; heteroscedastic residual within a design (N3(ii)): δ/r_n is 1.46, 1.71, 2.04, 2.59, HPM 0.92–0.95 — the rate looks lost at these n [SW1-6]; Gaussianity: t₃ residual (N3(i)) δ/r_n 1.30, 1.43, 1.09, 1.23, HPM 0.96–1.00: no visible deterioration in these runs — **looks improvable** | boundary-numerics (Gaussianity); inherited from the whole chain (A:GAUSS-NOISE), hard |
| v > 0 arbitrary (no fixed variance) | R′(a),(b) | exact invariance under y ↦ a1 + cy | — | this is the removal of v1's "σ², τ² fixed"; N1(i): posteriors agree to 5·10⁻¹⁴ across the five regimes v_n = σ² + τ_n² ∈ {2, 1 + n, 1 + n², 2/n, n⁻²} [SW1-3]; N1(ii): δ/r_n ∈ [1.07, 1.42] in every regime; code: N0 | none (assumption removed) |
| A:MISR-ESNR — (E^σ; M): ‖μ‖² ≤ nMv | through W3-POST2: Lemma C1/C2 (denominator, size tail), `lem:ongood` (‖y_c‖², b), R_n in E1 | bounds on ‖y_c‖²/(nv) and on the ridge cost of the reference | bounded ridge cost of S₀ and bounded ‖y_c‖²/(nv) | **cannot be dropped** (BT1 "Limits", confirmed by N5 = `numerics/N5_out.txt`: p = 2 orthogonal, v = 1, θ₁ = n, θ₂² = 200 log n/n. In this arm (F₀) holds, (OS) is void and every underfit has ridge loss ≥ n(n − 1) (L_{{1}} = n(n − 1) + 200(n − 1)log n/n; the other two are larger), so (ID^{M,σ}; c) holds eventually for any fixed c, e.g. c > c₁(2, 1) ≈ 258.9 [SW1-1]; energy/(nv) ≍ n², and E π(S₀) = 0.87, 0.18, 0.04, 0.014, 0.007, 0.003 for n = 100 … 102400: a huge signal inflates the coded residual scale and hides a threshold-level one). Not sharp either: in the control arms of N5 (θ₁ = 1 or √n; numerical controls, not verified instances of the margin class) E π(S₀) = 1.0000 at every n, and in N4 (all signals strong, energy/(nv) ≍ n^b, b ∈ {½, 1, 2}) δ/r_n is 0.47–1.22 with HPM ≥ 0.98: finite-sample behaviour compatible with the conclusion [SW1-5] — **weakenable, not removable** | boundary-numerics; single-use bounds |
| A:POST2-F0 — (F₀; φ₀) on S₀(κ) | W3-POST2 (C1, (C4′), E1) | coefficient bound, η_n | bounded ridge cost L_{S₀} | W3-POST2 N8: looks improvable; not re-tested | inherited; improvable |
| A:POST2-OS — (OS; C_OS) | W3-POST2 (C5′)(b), (C8′) | superset sums in expectation | — | unweighted feasible part necessary (W3-POST2:A2) | inherited |
| A:MISR-IDM-SNR — (ID^{M,σ}; c), c > c₁ | W3-POST2 Lemma E1 | underfit comparison | margin relative to v | N2: fixed raw coefficients, τ_n² = n^{2a}: relative ratio n^{1−2a}/log n; (nominal ratio, with population SDs) a = 0, 0.25 (ratio increasing): at n = 6400 δ/r_n is 1.242 and 1.216, HPM 1.00; a = 0.4 (ratio 0.5–0.7 at these n), a ≥ 0.5 (ratio decreasing): δ ≥ 0.98, HPM ≤ 0.01 [SW1-4, SW1-5] — the margin must be **relative to v** (this is v1's "R02 counterexample", now a margin failure); constant c₁ (≈ 161 at s = A = 1; ≈ 259 at s = 2, A = 1): ARTEFACT (inherited) | artefact-threshold (c₁) |
| A:POST2-FLAMBDA + A:BETAMIN (relative) — class 𝒦^λ_n | W3-POST2:C case (ii) | alternative to (ID^{M,σ}) for c₀ < c ≤ c₁ | — | inherited | — |
| A:FIXED-S0, A:P-POLY (s fixed, 2 ≤ p ≤ n^A) | inherited | union bounds, j₀, m♯_n | — | inherited (hard) | inherited |
| (GR^c ∣ 𝓕_n): W_n ⫫ 𝓕_n, N(0, I) (§4) | MIS(ii) | conditional expectation = fixed-configuration expectation | — | needed as stated for the conditioning step; any 𝓕_n allowed | none |
| A:IID-GAUSS-ROWS (Cor-G only) | Cor-G | Gaussian conditioning; C-MIS GD(b) steps | example only | — | family-named, in an example only (allowed) |

Conclusion level: posterior (MIS(i), (i′), (ii)); target/identity (R′); posterior for the parameter (Cor-H).
Rate: E δ_n ≤ C r_n, r_n = √(log n/n), constants free of v; lower bound (1 + √(n+1))⁻¹ inherited on LB's domain.
Scope: 2 ≤ p ≤ n^A, s ≥ 1 fixed; fixed designs uniformly over a configuration class; random designs by conditioning;
law: GR^c.

Unharvested conclusions: (1) E π(S ⊋ S₀) ≤ C r_n and E π(S ∌ j) ≤ C r_n are inside the W3-POST2 proofs but stated
there only as O_P — harvested here as MIS(i′)(a),(b). (2) The uniform-over-𝒜_n conclusion and the conditional form —
harvested as MIS(ii)(a). (3) From BT1, harvested in v1.2: the localisation E π(Ω∖𝒩_n) ≤ C r_n (MIS(i′)(d)), the first
(OS) inequality alone for (a), and the projective/total-variation form of the law condition (R′(c)). (4) Not
harvested (BT1-A2, recommended as an upstream ticket): uniform expectation versions of Cor-H with explicit
posterior-tail rates — needs W3-POST2:D's proof redone in expectation.

Boundary-violation numerics run (all in `numerics/misr_numerics_out.txt`): N1 (variance → 0 / → ∞, SNR held: inside
the new range, outside v1's), N2 (relative margin violated), N3 (outside GR^c: heavy tails, heteroscedastic, random
slope), N4 (outside (E^σ)); N5 (`numerics/N5_energy_obstruction.py` → `numerics/N5_out.txt`: (E^σ) violated with a huge
signal — the conclusion fails). For `ci/falsification.tsv` (`kind=boundary`): `misr_numerics.py` (≈ 10 min, py -3.13).

Closest literature result: Song–Liang (2015) §2.3 Theorem 4 (density consistency around the KL minimiser within a
misspecified candidate subset, fixed |s|, a.s.) and Corollary 2 (support inclusion). Ours: stronger conclusion (exact
model at rate r_n in expectation; inclusion of every coordinate that has a coordinate margin, without the global margin [R1-F9]; in-sample squared Hellinger distance at rate log n/n [SW1-8]), for the shipped
prior, with p_𝒞 ≤ n^A growing; narrower law (Gaussian contrast residual with scalar covariance, where SL allow what
their iid-row Gaussian linear model induces), in-sample and in probability instead of integrated and almost sure.
v1's extra restriction "σ², τ² fixed" is gone. Castillo–Schmidt-Hieber–van der Vaart (2015), Narisetty–He (2014),
Yang–Wainwright–Jordan (2016) treat well-specified models with growing s₀ and log p = o(n) for their own priors; the
restrictions fixed s, p ≤ n^A are inherited here and are the main literature gap (hard; upstream).

Sharpness reading (per hypothesis): GR^c — weakened in v1.2 to the law of the contrast direction (PR), with a
total-variation stability bound; non-scalar Gaussian residual laws — excluded for the same mean-only target by C-MIS E2 (scalar covariance itself not necessary under (PR));
Gaussianity of the direction law — improvable (hard, upstream); (E^σ) — needed in some form (N5), weakenable; (F₀) — improvable (inherited); (OS) — partly necessary;
(ID^{M,σ}) — relative form necessary in N2's sense, constant an artefact; fixed s, p ≤ n^A — inherited.

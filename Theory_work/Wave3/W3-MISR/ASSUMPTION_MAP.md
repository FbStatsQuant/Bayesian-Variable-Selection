# ASSUMPTION_MAP.md — W3-MISR (Wave 3 protocol item 3; written after the statement lock, before proving)

Target statement: `STATEMENT.md` v1.1, claims `W3-MISR:R'`, `MIS(i)`, `MIS(i')`, `MIS(ii)`, `Cor-G`, `Cor-H`, `Rem-SNR`,
`Rem-P`, `Rem-U`. Rules: `Theory_work/INFRA/LIFECYCLE.md` §4.3. Numerics: `numerics/N0_code_invariance.R` →
`numerics/N0_out.txt` (compiled code); `numerics/misr_numerics.py` → `numerics/misr_numerics_out.txt` (exact enumeration,
p = 8, 100 replicates, n ∈ {100, 400, 1600, 6400}; random design each replicate; finite-n observations at fixed p,
not limits, and they do not probe growing p).

## Entry map

| hypothesis (id) | where it enters | how | property actually used | necessity evidence so far | early sub-par signal? |
|---|---|---|---|---|---|
| A:MISR-GRC — GR^c: Uᵀ(y^r − xβ) ~ N_N(0, vI) | Lemma R′(b) only | the contrast vector, divided by √v, has the law of the unit-noise G-model; π depends on y^r through it | P: the standardised response has the law it has under a G-model with truth β/√v | scalar covariance: target changes under a common random slope (C-MIS E2; N3(iii): E π({0}) 0.23 → 0.02 for the mean-only target) — NECESSARY for a *named deterministic* target, removable by enlarging 𝓕_n (§4); heteroscedastic residual within a design (N3(ii)): δ/r_n grows 1.46 → 2.59, HPM ≈ 0.93–0.95 — the rate looks lost; Gaussianity: t₃ residual (N3(i)) δ/r_n 1.30, 1.43, 1.09, 1.23, HPM → 1.00 — **looks improvable** | boundary-numerics (Gaussianity); inherited from the whole chain (A:GAUSS-NOISE), hard |
| v > 0 arbitrary (no fixed variance) | R′(a),(b) | exact invariance under y ↦ a1 + cy | — | this is the removal of v1's "σ², τ² fixed"; N1(i): posteriors agree to 5·10⁻¹⁴ across v_n ∈ {n⁻², 1/n, 1, n, n²}; N1(ii): δ/r_n ∈ [1.07, 1.42] in every regime; code: N0 | none (assumption removed) |
| A:MISR-ESNR — (E^σ; M): ‖μ‖² ≤ nMv | through W3-POST2: Lemma C1/C2 (denominator, size tail), `lem:ongood` (‖y_c‖², b), R_n in E1 | bounds on ‖y_c‖²/(nv) and on the ridge cost of the reference | bounded ridge cost of S₀ and bounded ‖y_c‖²/(nv) | N4: with energy/(nv) ≍ n^b, b ∈ {½, 1, 2}, the conclusion holds and improves (δ/r_n 0.47–1.22, HPM ≥ 0.98) — **improvable** (proof artefact of the inherited chain) | boundary-numerics; single-use bounds |
| A:POST2-F0 — (F₀; φ₀) on S₀(κ) | W3-POST2 (C1, (C4′), E1) | coefficient bound, η_n | bounded ridge cost L_{S₀} | W3-POST2 N8: looks improvable; not re-tested | inherited; improvable |
| A:POST2-OS — (OS; C_OS) | W3-POST2 (C5′)(b), (C8′) | superset sums in expectation | — | unweighted feasible part necessary (W3-POST2:A2) | inherited |
| A:MISR-IDM-SNR — (ID^{M,σ}; c), c > c₁ | W3-POST2 Lemma E1 | underfit comparison | margin relative to v | N2: fixed raw coefficients, τ_n² = n^{2a}: relative ratio n^{1−2a}/log n; a = 0, 0.25 (ratio ↑): δ/r_n → 1.2, HPM → 1.00; a = 0.4 (ratio 0.5–0.7 at these n), a ≥ 0.5 (ratio → 0): δ ≥ 0.98, HPM ≤ 0.01 — the margin must be **relative to v** (this is v1's "R02 counterexample", now a margin failure); constant c₁ ≈ 161: ARTEFACT (inherited) | artefact-threshold (c₁) |
| A:POST2-FLAMBDA + A:BETAMIN (relative) — class 𝒦^λ_n | W3-POST2:C case (ii) | alternative to (ID^{M,σ}) for c₀ < c ≤ c₁ | — | inherited | — |
| A:FIXED-S0, A:P-POLY (s fixed, 2 ≤ p ≤ n^A) | inherited | union bounds, j₀, m♯_n | — | inherited (hard) | inherited |
| (GR^c ∣ 𝓕_n): W_n ⫫ 𝓕_n, N(0, I) (§4) | MIS(ii) | conditional expectation = fixed-configuration expectation | — | needed as stated for the conditioning step; any 𝓕_n allowed | none |
| A:IID-GAUSS-ROWS (Cor-G only) | Cor-G | Gaussian conditioning; C-MIS GD(b) steps | example only | — | family-named, in an example only (allowed) |

Conclusion level: posterior (MIS(i), (i′), (ii)); target/identity (R′); posterior for the parameter (Cor-H).
Rate: E δ_n ≤ C r_n, r_n = √(log n/n), constants free of v; lower bound (1 + √(n+1))⁻¹ inherited on LB's domain.
Scope: 2 ≤ p ≤ n^A, s ≥ 1 fixed; fixed designs uniformly over a configuration class; random designs by conditioning;
law: GR^c.

Unharvested conclusions: (1) E π(S ⊋ S₀) ≤ C r_n and E π(S ∌ j) ≤ C r_n are inside the W3-POST2 proofs but stated
there only as O_P — harvested here as MIS(i′). (2) The uniform-over-𝒜_n conclusion and the conditional form — harvested
as MIS(ii)(a). (3) Not harvested: an expectation version of Cor-H (posterior expectations of unbounded losses are not
controlled by W3-POST2:D).

Boundary-violation numerics run (all in `numerics/misr_numerics_out.txt`): N1 (variance → 0 / → ∞, SNR held: inside
the new range, outside v1's), N2 (relative margin violated), N3 (outside GR^c: heavy tails, heteroscedastic, random
slope), N4 (outside (E^σ)). For `ci/falsification.tsv` (`kind=boundary`): `misr_numerics.py` (≈ 10 min, py -3.13).

Closest literature result: Song–Liang (2015) §2.3 Theorem 4 (density consistency around the KL minimiser within a
misspecified candidate subset, fixed |s|, a.s.) and Corollary 2 (support inclusion). Ours: stronger conclusion (exact
model at rate r_n in expectation; inclusion without a margin; in-sample Hellinger rate log n/n), for the shipped
prior, with p_𝒞 ≤ n^A growing; narrower law (Gaussian contrast residual with scalar covariance, where SL allow what
their iid-row Gaussian linear model induces), in-sample and in probability instead of integrated and almost sure.
v1's extra restriction "σ², τ² fixed" is gone. Castillo–Schmidt-Hieber–van der Vaart (2015), Narisetty–He (2014),
Yang–Wainwright–Jordan (2016) treat well-specified models with growing s₀ and log p = o(n) for their own priors; the
restrictions fixed s, p ≤ n^A are inherited here and are the main literature gap (hard; upstream).

Sharpness reading (per hypothesis): GR^c scalar covariance — necessary for a named target, see above; Gaussianity —
improvable (hard, upstream); (E^σ) — improvable (artefact); (F₀) — improvable (inherited); (OS) — partly necessary;
(ID^{M,σ}) — relative form necessary in N2's sense, constant an artefact; fixed s, p ≤ n^A — inherited.

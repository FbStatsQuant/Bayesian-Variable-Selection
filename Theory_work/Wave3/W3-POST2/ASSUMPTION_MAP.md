# W3-POST2 — ASSUMPTION_MAP (sharpness gate; v1.3, 2026-11-09; v1.1 = K-AE wording; v1.2 = R03b adoptions; v1.3 = sweep S01 + numerics v2)

One page per protocol rule 3. Ids extend W3-POST's (POST-G, POST-E, POST-C, POST-F0, POST-Fλ, POST-Fw, POST-BM, …;
`../W3-POST/ASSUMPTION_MAP.md`). Numerics: `numerics/post2_checks.py` (v2) → `numerics/post2_checks_out.txt`: exact
enumeration of the coded posterior, p = 10, 20 seeds, n ∈ {100, 400, 1600, 6400} (N5 also 25600), σ* = 1; medians over
seeds unless a column is prefixed mean/P (mean), min (minimum) or sum (count). Fixed p, so log p/log n → 0; these runs do
not probe polynomially growing p, and are finite-n observations, not limits [S01-16].

## New assumption ids and where they enter (STATEMENT v1.2)

| id | statement | enters | necessary? |
|---|---|---|---|
| POST2-OS | superset Occam sum (OS; C_OS) | A1: (C5′)(b) E Υ′_n, (C8′) the > j₀ term; C (cases ii–iii); D(b); E | its unweighted feasible counterpart 𝒪⁰_n is **necessary** (A2: δ_n ≥ 𝒪⁰_n/(1+𝒪⁰_n), deterministic); the weights, the infeasible comparison unions and the amplified j > j₀ inequality are proof envelopes |
| POST2-ADG / DG | averaged / pointwise determinant ratio | ⇒ (OS) (Lemma A0) | sufficient only; (ADG) improvable to (OS) (N2) |
| POST2-F0 | floor λ_min(R_{S₀}) ≥ φ₀² | coefficient bound (tail; C1); (B3) in (C4′); R_n, L_{S₀} in E1, D | **looks improvable** (N8: rate holds as λ_min(R_{S₀}) → 0); R03b E-floor+ (bounded ridge cost L_{S₀}) recorded, not proved |
| POST2-ID / ID^M | margin on bounded-excess underfits: Δ_S (projection) or L_S ≥ Δ_S (ridge) ≥ cσ*² log n | E: Lemma E1 only; D(b) uses E1 at c₁ + 1 to discard far underfits (no hypothesis) | no converse proved; small-margin obstructions illustrated (N1 κ = 1, N4 c ≤ 2); c₁ ≈ 161 a proof artefact |
| POST2-GP | G′: Gaussian noise, arbitrary centred mean μ = Cf | B | the arbitrary mean is free (N6b); Gaussianity enters through the explicit f₀ exponent, the χ² fluctuation and the Gaussian cross term in the denominator, and the scale event ([P1] `thm:T01iii`); `lem:num` needs only a positive density f₀ [S01-15]. Non-Gaussian noise: not tested (the whole inherited chain assumes G; outside this ticket) |
| POST2-AR | reference cost B_T(ϑ) ≤ B (fixed) | B | **sufficient** for the uniform bound of this proof; **not necessary** (N6b growing-cost case: Θ″ stays bounded with B = n − 1; S01-1's example) [S01-1] |

## Boundary-violation numerics

| exp | violated / held | outcome | flag |
|---|---|---|---|
| N1 exact: null x₃ ∝ x₁ + x₂ ∈ col X_{S₀} (S₀ = {1, 2}, bounded representation) | (OS) j = 1 term ≍ 1/p (d_J = 0); (F_λ), (F_w), (DG); full (ID) min = 0 | δ_n 0.75 → 0.69, not → 0; 𝒪⁰_n ≈ 0.34 → 0.20; A2: 0 violations, min slack ≥ 0.47 | (OS)'s 𝒪⁰ part necessary here, as A2 says |
| N1 κ = 1: residual of x₃ of unnormalised size O(1) | (F_λ) fails (φ₀² ≍ 1/n); full (ID) min 0.38 → 0.22 × log n, (ID^M) min 0.80 → 0.45 × log n; (DG) holds at j = 1 | δ_n between 0.56 and 0.69; HPM = S₀ in 30–60% | small-margin obstruction (illustration; no converse proved) |
| N1 κ = ½: residual of size √n | (F_λ) fails (φ₀² ≍ n^{−1/2}); full (ID) min 3.2 → 17.5 × log n; (OS) finite | δ_n/r_n 1.20, 1.03, 1.16, 0.80; HPM = S₀ 85% → 100%; A2 min slack ≥ 0.0035 | (F_λ) **improvable** — consistent with Claim E |
| N2: exact duplicate null pair | (F_λ), (F_w), pointwise (DG) and, at fixed p, (ADG) fail; exact-weight 𝒪_n^{>0}/r_n 85 → 15, amplified (2p)^{s₀}(n+1)^{s₀/2}𝒪_n^{>j₀}/r_n 2.7·10⁴ → 45, both decreasing | δ_n/r_n 1.06, 0.98, 1.12, 0.79; HPM 85% → 100%; A2: 0 violations | consistent with strict weakening (ADG) → (OS) (finite-n; no asymptotic proof for this example) [C1A-2] |
| N4: coefficient scale θ² = c log n/n, s₀ = 1 (c is not the (ID) constant) | achieved full (ID) min ≈ c(1 − O(1/log n)) × log n ((ID^M) equal to 3 digits) | c = 1 fails (δ ≈ 0.86–0.96); c = 2 slow (δ/r_n 3.6 → 8.6); c = 4, 8: δ/r_n between 0.58 and 1.18 | at c = 4 the achieved margins are 3.67–3.99 × log n with δ/r_n 0.75–1.18 [C1A-2]; no universal improved constant proved (R03b: ≈ 2a_p + 2 is an obstruction at p = n^A) [S01-5, S01-9] |
| N5: expectation rate | BM holds | mean δ_n√n ∈ [2.0, 6.1] for n = 100 … 25600 (two designs) | consistent with Claim C (E δ_n = O(r_n), proved) |
| N6 / N6b: Claim B | references T = S₀; S₀ minus a weak coefficient; ∅ under weak total signal; mean with a component ⊥ col X (‖g‖² = 2, T = S₀); growing cost (T = ∅, B = n − 1) | max_{t≤m<K}Θ″ ≤ 1.1·10⁻² and decreasing in all bounded-cost cases (≤ 7.5·10⁻⁶ for the orthogonal mean); growing cost: 0.1 → 0.0125 | no counterexample; bounded cost not necessary |
| N7: Claim D | with BM / without (θ² = 0.5 log n/n) | n·E_Π[h̄² bound] ≈ 4–5 flat (BM); E_Π‖μ̂ − μ‖²/log n ≈ 1.0 (no BM); n·E_Π(v − 1)² ≈ 3 | **consistent with** the rates (posterior expectations of an upper bound; not lower bounds) [S01-8] |
| N8: (F₀) boundary: x₂ = x₁ + n^{−1/4}z, θ = (1, 1) | λ_min(R_{S₀}) 0.045 → 0.006 → 0; full (ID) min 1.8 → 9.1 × log n | δ_n/r_n 4.2, 2.8, 1.18, 0.80; HPM 10% → 100% | (F₀) **looks improvable** (finite-n) |

Not tested (recorded) [S01-13]: non-Gaussian noise (the inherited chain assumes G throughout); growing p (enumeration cap p ≤ 10).

Interface (protocol rule 5): the design conditions enter through two bridge properties — the superset Occam sum (OS)
(bridges: (F_w) ⇒ (DG) ⇒ (ADG) ⇒ (OS), Lemma A0) and the underfit margin (ID^M) (bridges: (F_λ) ∧ BM ⇒ (ID) ⇒ (ID^M), E3.1);
the floor (F₀) on S₀ is the only eigenvalue condition left in Claim E and in D(b).

## Literature comparison
- Song–Liang (2015) Thms 1–2 (printed pp. 952–953, from the attached PDF): posterior consistency in the Hellinger distance
  of the joint density of (x, y), d²(f, f*) = ∫∫|f^{1/2} − f*^{1/2}|² ν_x(dx) dy, random design with bounded predictors
  (Thm 1) or Condition 1 (Thm 2), conclusion P*[π{d(f, f*) > ε_n | D_n} > e^{−c₁nε_n²}] < e^{−c₁nε_n²}; Cor 1 (printed
  p. 954; under strict sparsity, P_n < exp(Cn^α) and its logarithmic model-size branch) ε_n = O(n^{−(1−α)/2}log^{k/2} n) (SL's α; their ξ is a model index);
  SL's d² = 2H² in Claim D's normalisation. Claim D: fixed-design in-sample average Hellinger, convergence in probability,
  rate log n/n without beta-min and without (F_λ) (D(b)), oracle 1/n with selection (D(a)).
- Narisetty–He (2014) Conditions 4.4 (identifiability) / 4.5 (minimum nonzero eigenvalue, together with an upper
  eigenvalue restriction, per S01) — (ID^M) is the analog of 4.4 restricted to bounded-excess underfits; (OS) plays the
  role of 4.5-type regularity for supersets (recorded in `../W3-POST/ASSUMPTION_MAP.md`; not re-read here).

## Sharpness record (v1.3)
- **Superset interface:** (OS) sufficient; its unweighted feasible counterpart 𝒪⁰_n necessary (A2, deterministic). Gap
  (STATEMENT A2): weights a_J, feasible supersets beyond m♯_n, infeasible comparison unions, amplified j > j₀ inequality.
- **Underfit interface:** (F_λ) not needed (Claim E; N1 κ = ½); (ID^M) sufficient with c > c₁; no converse proved.
- **Floor on S₀:** still assumed; looks improvable (N8); R03b's bounded-ridge-cost replacement recorded.
- **Expectation rate:** E δ_n = O(r_n) (Claim C); and, **when 1 ≤ s₀ < p and s₀ + 1 ≤ K** (LB's domain), E δ_n ≥
  (1 + √(n+1))⁻¹; so on that domain sharp up to √(log n) [S01-10]. (For p = s₀ the lower bound can fail; W3-POST
  `lb_domain_out.txt`.)
- **Predictive rate:** D(a) 1/n scale cannot be improved for the mean part (χ²_{s₀}-type conditional spread); D(b)
  log n/n: numerics consistent, no lower bound proved.
- **Reference cost (Claim B):** a bounded cost is sufficient for this proof's uniform constant; growing cost gives an
  exp(O_P(B_n)) upper payment; boundedness is **not** necessary (N6b; S01-1).

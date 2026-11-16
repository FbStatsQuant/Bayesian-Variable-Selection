# ASSUMPTION_MAP.md — W3-PSHARP (Wave 3 protocol item 3; written after the statement lock L01, before the lemma files)

Target statement: `STATEMENT.md` v1.2.2 (locked), claims `W3-PSHARP:S`, `W3-PSHARP:A`, `W3-PSHARP:B`, `W3-PSHARP:C`.
These are sharpness records: their "hypotheses" are the conditions of a witness / lower bound, so the question for
each is not "is it necessary for an upper bound" but "does the record survive without it".

| hypothesis | where it enters | how | property actually used | necessity evidence so far | early sub-par signal? |
|---|---|---|---|---|---|
| none (Lemma S, Claim B): any design, any data, s₀ ≤ K − 1 | Lemma S(1)–(4); B | Schur complement; fit factor ≥ 1 | a feasible one-step superset exists (A:EXT-FEAS) | NECESSARY: at s₀ = K (or p = s₀) the bound can fail (`W3-POST/numerics/lb_domain_out.txt`) | none; equality attained (orthogonal X, y ⟂ col X: `numerics/b_check_out.txt` F2) |
| s₀ ≤ p/2 (constant 1/3 in B1–B2) | B, constants | (p − s₀)/(2p − 1 − s₀) ≥ 1/3 | multiplicity ≍ p | cosmetic: c(p, s₀) is stated exactly | none |
| A:GAUSS-NOISE (G) in Claim A | A, laws of the null scores | exact χ²₁ (W-orth) / independence of ε and the null block (W-sph); the constant 1/√π is the Gaussian truncated mean | iid scores with E[e^{ζ/2}; ζ ≤ 2 log N] ~ 2√(log N/π) | NECESSARY-FOR-ROUTE; the constant is noise-specific (lighter-tailed noise would change it). Same hypothesis as the upper bound it sharpens | none |
| (E) ‖μ‖² ≤ nM, (C) ‖θ*‖² ≤ nM′ in Claim A | A, step κ_n ≥ 1 − c_n | variational form of Q_{S₀} at ϑ = θ*; s_y² = O_P(1) | 2b₀ + Q_{S₀} ≤ (‖Cε‖² + O(1))/s_y² | WEAKENABLE: both witnesses need only (M + M′) log N_n = o(n); kept fixed to match Theorem 1 | unharvested (growing M) — recorded, not stated |
| (W-orth) null block orthogonal, ⟂ col X_{S₀} | A, independence of scores | u_jᵀε iid N(0, σ*²) | independent null scores, D ratio = n | witness, not necessary: (W-sph) is a second witness. Evidence that the one-step mechanism need not retain the logarithmic enhancement under dependent null columns: on an equicorrelated null block the one-step odds L1 lose it (median L1/Λ_n 0.71, 0.72, 0.61 against ≈ 1.05 at ρ = 0; `numerics/a_boundary_out.txt`). The script computes only one-step odds (a lower bound): failure of Proposition A's full posterior conclusion without the witness condition is **not established** [K01-F2] | family-named? no: stated as a property of the null block |
| (W-sph) spherical null directions, independent of ε | A, independence + sphere law | conditional iid (n−1)Beta(½,(n−2)/2) projections on the ridge residual | same | as above (same qualification: one-step evidence only); covers p ≫ n | none |
| N_n → ∞ | A, Chebyshev | variance/mean² = O(1/√log N_n) | weak law | NECESSARY for the log factor (bounded N: only Claim B's constant) | none |
| (log N_n)² = o(n) (W-sph) | A, Lemma W(ii) | sphere density vs normal on t² ≤ 2 log N | density ratio → 1 | ARTEFACT-threshold of the route (beyond it the sphere law is lighter than Gaussian and the constant changes); outside regime R1 anyway (p ≤ n^A) | artefact-threshold (harmless) |
| (r₀ + 1) log N_n = o(n), r₀ = rank X_{S₀} (W-sph) [K01-P2: was s₀] | A, κ′_n ≥ 1 − O_P((r₀+1)/n) | Q_{S₀} − ‖ρ̃‖² ≤ 1 + (2M′ + ½σ*²χ²_{r₀})/s_y² | exponent coefficient → 1 faster than 1/log N | ARTEFACT of the crude bound e(1−e) ≤ ¼; trivially true for bounded rank | single-use bound |
| design 𝔇_n, k = ⌈12 log n⌉, η = n⁻², n b_n² ≥ 1200(σ*² + b̄²)(log n)² (Claim C) | C items 2–3 | cutoff ≤ k/2; fit loss e^{−c n b²} against prior × Occam × count ≤ e^{12 log² n} | reference with exact fit but ridge cost ≍ n b_n² | constants are ARTEFACTS; the record is "a cost allowance of a large constant times (log n)² (or more) breaks the conclusion; O(1) suffices"; allowances o((log n)²) are open [KBC-3] | artefact-threshold (the constants 12, 1200) |

Conclusion level: negative / lower bound (sharpness records) for posterior-level claims; rate: (s₀+1)√(log p/(πn))
(A), c(p, s₀)/√n (B; → (s₀+1)/(2√n) as p → ∞, s₀/p → 0); scope: A — witness classes (orthogonal block, p ≤ n − 1; spherical block, (log p)² = o(n));
B — every design, every data set; C — one design sequence.

Unharvested conclusions: (i) Claim A with growing M, M′; (ii) null-PIP floors
PIP_j ≥ π(S₀)(s₀+1)/((2p−1−s₀)√n)·e^{νγ_j} (from Lemma S(3)); (iii) [harvested in v1.2, K01-P1] the full-sum form of B gives
limsup π(S₀) ≤ e^{−λ/2} at s₀ ~ λ√n (table T1 in `numerics/b_check_out.txt`).

Boundary-violation numerics run: `numerics/a_boundary.py` (witness condition violated: equicorrelated nulls);
`numerics/c_counter.py` control arm (coefficient bound restored: Lemma 1a′'s conclusion holds, tail ≤ 1e-13);
`numerics/a_orth.py` small p (N_n bounded: ratio to Λ_n stays ≥ ~1 but the log factor is not visible).
To add to `ci/falsification.tsv` (HQ): `b_check.py` (kind=falsify, Corollary B, 55,740 cases), `c_counter.py` V1.

Closest literature: the n^{−1/2} floor and the multiplicity (s₀+1)/2 are properties of the coded prior (BB(1, p),
g = n): Yang–Wainwright–Jordan (2016) get 1 − π(γ*) = O(p⁻¹) with a p^{−κ|γ|} prior; Castillo–Schmidt-Hieber–van der
Vaart (2015) need prior decay p^{−A₄} per added variable (as quoted in `Theory_work/Wave3/API_AUDIT/sharp1/results/f17.md`;
not re-read here). No published lower bound for this target is known to us; nothing here is dominated.

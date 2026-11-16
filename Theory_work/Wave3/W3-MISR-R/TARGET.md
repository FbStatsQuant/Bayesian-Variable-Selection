# W3-MISR-R — TARGET (CP1 evidence; one page; v1.0, 2026-11-15)

Statement: `STATEMENT.md` v1.0 (delta over W3-MISR v1.3). SL = Song & Liang (2015) §2.3, Theorem 4 and Corollary 2, as
summarised in `Theory_work/Wave1C/C-MIS/STATEMENT.md:17-24` (full Gaussian linear model, iid random design, fixed
candidate subset; density consistency around the KL minimiser f₀, a.s.; support inclusion s̃ ⊆ ξ in probability).

## 1. Assumption map of the changed hypotheses

| hypothesis (id) | claim | where it enters | property used | necessity |
|---|---|---|---|---|
| A:MISR-OVC — (N) + (OV^c): ε Gaussian ⫫ (X_𝒞, X_𝓜); omitted contrasts | CorG-min (a), CorGb-plus, CorH-U (RD) via §2 | the conditional characteristic function of the contrast residual given X_𝒞 | Uᵀ(y^r − X_𝒞β^𝒞)/σ_𝒞(X_𝒞) ~ N(0, I) ⫫ X_𝒞 | **necessary and sufficient** for (GR^c \| σ(X_𝒞)) under (N) (§2(c)); with any independent noise, Gaussian contrasts are forced (§2(d), Cramér). Necessary for the *exact* law reduction only: N1 shows no cliff just outside (below) |
| law of X_𝒞 arbitrary (was: iid jointly Gaussian rows) | CorG-min | — (not used) | — | not needed for (a); design events (Cor-G(b)) still use Gaussian candidate rows |
| Σ_𝒞𝒞 ≻ 0 (dropped in CorG-min; floor only on \|T\| ≤ k_n in CorGb-plus) | CorG-min (E1), CorGb-plus | Gaussian conditioning (Moore–Penrose); step 3 of G.2 needs β^𝒞ᵀΣβ^𝒞 > 0 only | range(Σ_𝒞𝓜) ⊆ range(Σ_𝒞𝒞) | not needed |
| A:CORR-FLOOR λ_min(R_TT) ≥ c_R (was λ_min(Σ_TT) ≥ c_pop and Σ_jj ≤ C₀) | CorGb-plus | sample sparse eigenvalues after standardisation | only c_pop/C₀ enters BASE G.2 (`:40, 47-48`); the coded target is column-scale invariant | the variance bound C₀ is not needed |
| liminf ρ_n^{BM} > 16c₀/c_R (was ρ_n^{BM} → ∞) | CorGb-plus | step 4 of G.2 | eventually (c_R/16)ρ_n ≥ c > c₀ | constant-level (c₀ is a proof artefact, BASE `:266`) |
| A:SEL-P — δ_n → 0 in probability (replaces (OS) + margin in Cor-H(a)) | CorH-plus (a′) | [POST2] D2: Π(Bad) ≤ δ_n + Π(Bad′ \| S₀, y) | the posterior selects S₀ | necessary for the clause {S ≠ S₀} in B^a (it is part of the conclusion); (OS) and the margin enter only through δ_n |
| (UP) uniform selection premise | CorH-U (U-a), (RD) | subsequence argument | — | needed for the uniform form (pointwise δ_n → 0 does not give uniformity) |

## 2. Parity (per changed clause; matches / beats / short)

| clause | (a) PROGRAM goals | (b) closest published (SL Thm 4 / Cor 2) | (c) best registered (BASE) |
|---|---|---|---|
| CorG-min | design-agnostic: candidate-design law arbitrary — **beats** | SL: jointly Gaussian iid rows. Here: any candidate-design law, dependent rows, design-dependent γ, τ²; contrast-level iff — **beats** (scope) | Cor-G(a): jointly Gaussian rows, Σ_𝒞𝒞 ≻ 0 — **beats** (implies it, §8) |
| CorGb-plus | p ≤ n^A, method as coded — matches | SL Cor 2: inclusion only, fixed candidate size, a.s./in prob. Here: exact selection of supp β^𝒞 with rate O(√(log n/n)), p_𝒞 ≤ n^A — **beats** (metric, rate); hypotheses: Gaussian candidate rows (SL: Gaussian full rows) — matches | Cor-G(b) — **beats** (weaker floor, no C₀, liminf beta-min, no joint Gaussianity) |
| CorH-plus (a′), (b), (KL) | fixed design, p ≤ n^A — matches | SL Thm 4: integrated (x, y) density distance, a.s., KL projection f₀. Here: in-sample average Hellinger/KL, in probability, rate M_n/√n ((a′)) or log n/n ((b)) — **short** in metric/mode (in-sample, in probability), **beats** in rate and in p range. Reason for "short": out-of-sample needs a design law (W3-DIST's ticket) | Cor-H — **beats** ((a′) drops (OS) and the margin; KL clause new) |
| CorH-U | uniform over a configuration class; random designs by conditioning — matches the MIS-R (ii) standard | SL: no uniform or conditional form — **beats** | none — **new** (BASE ASSUMPTION_MAP "unharvested (4)" asked for the expectation form; that stays open, `STATEMENT.md` §6) |

No row is "short" without a reason; no stretch item.

## 3. Boundary numerics (`numerics/N1_boundary.py` → `numerics/N1_out.txt`; exact enumeration of the coded target, p = 5, 300 replications)

Candidate design binary with AR(1)-dependent rows (outside BASE Cor-G, inside CorG-min); σ²_𝒞 = 2 in IN.
E[1 − π(target)] at n = 100 / 400 / 1600:
**IN** ((OV) holds): 0.917 / 0.278 / 0.083 · **OUT-het** (non-scalar conditional covariance): 0.908 / 0.282 / 0.067 ·
**OUT-rad** (Rademacher omitted part; GR^c fails by §2(d)): 0.909 / 0.288 / 0.069 · **OUT-nl** (non-linear conditional mean;
target = population best-linear-predictor support {1, 2}): 0.317 / 0.152 / 0.076. (r_n = 0.215 / 0.122 / 0.068.)
Reading (finite-n observation at fixed p, not a limit): inside, the decay is consistent with the O(r_n) rate; just
outside (OV^c) nothing changes visibly. (OV^c) is the boundary of the **exact law reduction** (it is necessary for it,
§2(c)), not an observed boundary of the phenomenon; robustness beyond it is BASE's non-claim (`:259`) and stays open.

## 4. Better-theorem review
Not run at CP1 (RIDER_RULES §3.2: targets from the blind sharp2 audit, `API_AUDIT/sharp2/TRIAGE.md:40-42`, which served as
the better-theorem input). Credible proposals already known: Cor-H in expectation with explicit tail rates (BASE BT1-A2)
— named open item; sub-Gaussian candidate rows in Cor-G(b) (TRIAGE `:41`, class B) — named open item.

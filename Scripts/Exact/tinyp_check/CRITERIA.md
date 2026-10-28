# Tiny-p SMC versus exact enumeration: design and pre-declared criteria

Fixed 2026-10-23, before any tiny-p run, from PLAN_REVIEW.md (Fable rules, with the lead's decisions).

## Purpose

v2's SMC orchestration (calibration, evidence increments, RB-PIP pooling over 4 islands, local search) was never compared against an exact posterior. Here the public `v3_fit` of the v2.1 core (byte-identical to v2) runs at its fixed production budgets. The results are compared with B's independent Python oracle `oracle_score.enumerate_exact`, from B's frozen payload, which enumerates every model with |S| ≤ K.

## Designs (n, p chosen so that v3's branch rule selects SMC: Σ_{k≤K} C(p,k) > (5·H0 + 4·N0)·p = 12560·p, K = min(p, ⌊n/2⌋))

| Design | n | p | K | Σ_{k≤K} C(p,k) vs threshold | X | β (columns 1-based) | Role |
|---|---|---|---|---|---|---|---|
| D1 | 30 | 20 | 15 | 1,042,380 > 251,200 | iid N(0,1) | 1.5, −1.0, 0.8 on 1, 2, 3 | clear signal |
| D2 | 30 | 20 | 15 | 1,042,380 > 251,200 | N(0,Σ), Σ blocks of 5 with ρ = 0.6 | 1.0, 0.7, 0.5 on 1, 7, 13 | correlation, intermediate PIPs |
| D3 | 30 | 18 | 15 | 261,972 > 226,080 | iid N(0,1) | 0.6 on 1 | weak signal, diffuse posterior |
| D4 | 16 | 20 | 8 | 263,950 > 251,200 | iid N(0,1) | 2.0, −1.8, 1.6, −1.4, 1.2, −1.0, 0.8 on 1..7 | binding cap: posterior mass at sizes 7–8 |
| D5 | 30 | 20 | 15 | 1,042,380 > 251,200 | iid N(0,1) | 0 (null) | exposes the size prior and the baseline |

- Noise: σ = 1.
- Two data replicates per design.
- Data seed: `set.seed(2026102300 + 10·D + rep)`. X is drawn first, then ε.
- Four method seeds per dataset: `7000000 + 1000·D + 100·rep + m`, with m = 1..4.
- Total: 10 datasets and 40 fits.
- Allocation: `list(mem_gb = 2, hours = 1)`.
- Every fit must report `branch_run == "smc"` and status `completed`; otherwise the check fails outright.

## Quantities

For fit f (dataset d, design D):
- L_f = pooled log Ẑ on the Bayes-factor scale (`log_Z_rel_m0`);
- L_{f,r} = island values (`log_Z_r_rel_m0`, R = 4);
- Δ_f = L_f − log(Z/m(∅))_exact (B's `log_Z_bf`);
- s_f² = sample variance of the L_{f,r} (3 df);
- s_D² = mean of s_f² over the n_D = 8 fits of design D (24 df).

## Family-wise false-alarm rate

The gate's false-alarm rate is α = 0.05, split equally between the log Z family and the PIP family (0.025 each), with Bonferroni within each family. HPM checks are replicability rules with no stochastic threshold.

### log Z family: 3 rules × 5 designs = 15 tests, each at α_t = 0.025/15

- **Rule A, island independence.** V_D = Σ_d Σ_i (L_{d,i} − L̄_d)² / (2·(m−1)), with 6 df. The statistic is F_D = V_D / (s_D²/4). Investigate if F_D > F⁻¹(1 − α_t; 6, 24). If A fires for a design, Rules B and C for that design use V_D (6 df) in place of s_D²/4 (24 df).
- **Rule B, systematic shift.** t_D = mean_f Δ_f / √(s_D²/(4·n_D)). Investigate if |t_D| > t⁻¹(1 − α_t/2; 24). The minimum detectable shift is about s_D·q/√32, reported per design.
- **Rule C, dispersion.** Q_D/n_D = Σ_f Δ_f² / (n_D·s_D²/4). Investigate if Q_D/n_D > F⁻¹(1 − α_t; 8, 24).

### PIP family: 98 coordinates + 5 size tests = 103 tests, each two-sided at α_p = 0.025/103

- e_{f,j} = PIP̂_{f,j} − PIP_exact,j.
- s_{D,j}² = mean over fits of the island sample variance of `pip_r[j, ]` (24 df).
- t_{D,j} = mean_f e_{f,j} / √(s_{D,j}²/(4·n_D)).
- **Flag** coordinate j of design D iff |t_{D,j}| > t⁻¹(1 − α_p/2; 24) **and** |mean_f e_{f,j}| > 1/(N₀·R) = 1e-4. The floor is the resolution of the plain particle-frequency estimator at the production budget (N₀ = 2500, R = 4); RB differences below it are not resolvable by the design. A coordinate with s_{D,j} = 0 is flagged iff |mean e| > 1e-4.
- **Size test.** The same rule applies to Σ_j PIP (island values Σ_j pip_r[j, r]) against the exact E|S| = Σ_j PIP_exact,j.
- **Deterministic pooling checks**, zero false-alarm, which must hold for every fit:
  - `pip_primary == rowMeans(pip_r)` exactly;
  - min_r pip_r[j, r] ≤ PIP̂_j ≤ max_r pip_r[j, r].

### HPM (per dataset)

- If all 4 seeds return the same HPM and it differs from the exact HPM, **investigate**.
- If the seeds disagree among themselves, **report only**.
- Wherever v3's HPM equals the exact HPM, |hpm_F − hpm_score| ≤ 1e-9 nat must hold (B's frozen scorer tolerance). This also checks that the score scales agree.

### Scale cross-check (report)

Report max |log_m0 (v3) − log_m_empty (B)| and max |(log_Z − log_Z_full) − Δ|.

## Outcome

- **PASS:** every fit is SMC/completed, the deterministic checks hold, and no rule fires.
- **INVESTIGATE:** otherwise. Every fired rule is reported to HQ with its numbers; nothing is retuned.
- What the gate cannot detect:
  - errors smaller than its stated power (s_D·q/√32 for log Z; the per-coordinate t-thresholds for PIPs);
  - errors that only appear at n = 200, p ≥ 500 (scale and timing behaviour).

## Post-run note (2026-10-23, after the run; the criteria above are unchanged)

D4 did not reach the cap. The exact E|S| was 2.41 and 2.60, against K = 8. No fit escalated. See NOTS_READINESS.md §4.

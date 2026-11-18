# WP5 — evaluator (selection, PIP, distribution), law file, Slurm driver, competitor harness (Opus 5.5 builder)
Read BUILD_COMMON.md first. Branch: `exp/P1M-wp5-eval`. Mostly independent of the engine internals; use INTERFACES.md
(WP1, within hours) for the `fit.bin` / `law.bin` formats, and stub readers until then.

Inputs: EXPERIMENT_PLAN §3 (metrics; §3.3 is the W3-DIST metric set), ENGINEERING_SPEC §0-v2.3 (precision targets),
§0-v2.7 (overlap tolerances), §1 rows 5–7, `Theory_work/Wave3/W3-DIST/STATEMENT.md` §0 and §2 (read only; definitions of
d_H, f_{S,θ,v}, the three DIST-C objects), DECISIONS D-8, D-13.

Scope:
1. **Evaluator** (`eval`): selection metrics (HPM/MPM = S₀, outcome class with F(S₀) scored directly, provenance), PIP
   metrics (sup null, min true, Brier, reliability bins), evidence diagnostics (σ̂, R_eff, max W, log Z_𝒯, Ẑ_occ for
   M ∈ {1, 10, 100, 1000}), and cost fields.
2. **Distribution metrics** (plan §3.3), for Π̂^H, Π̂^M, Π̂^𝒯 and the oracle Π(·|S₀):
   - the closed-form plug-in Hellinger for Gaussian designs (the formula in plan §3.3 item 1; derive it and test it);
   - the posterior law of d_H by conjugate draws;
   - the predictive Hellinger (Student-t mixture; Gauss–Hermite) and KL;
   - prediction error;
   - the store-mass diagnostic.
   Gate **T7**: closed forms against brute-force Monte Carlo on 20 fixtures, to 3 significant digits.
3. **`post` / `law.bin`**: write and read the store-BMA law (models above relative weight 1e-12; weights; per-model
   conjugate parameters; standardisation constants; dropped mass).
4. **Slurm driver** (Python, in `engine_v4/tools/`): generates job **arrays** (never many separate sbatch calls) for
   setup → calibrate → islands → merge → eval with `--dependency=afterok`, and pipelines replicates. Paths only inside
   `~/SMC_Engineering_Department/` on NOTS: scripts in `scripts/<batch>/`; outputs, `--output` and TMPDIR via the
   `scratch` link. `--constraint=sapphirerapids`, the 150-task cap, one manifest per run, and the ledger rows for
   `LEDGER.md`. **Dry-run mode only** (writes sbatch files, never submits). Submission is the manager's.
5. **Competitor harness** (R): lasso-CV / MCP (glmnet, ncvreg or biglasso), L0Learn, SuSiE (susieR), varbvs, BAS (p ≤
   10⁴), SIS → our engine; the same evaluator. Check which packages exist on Owls; list what NOTS would need. **Do not
   install anything**: report the list to the manager.
6. Tests for all of the above; small fixtures only.

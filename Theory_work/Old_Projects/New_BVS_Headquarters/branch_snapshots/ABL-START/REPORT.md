# ABL-START: does the local-to-global (block) start earn its place? (DRAFT, results pending)

Status: running. This file is overwritten as results arrive.

## Design (fixed before results)

**Arms.** Every arm is the production `v3_fit` (preprocess, budgets, calibration with its caps, tiers and rebuild
limit, final run of 4 islands × N_e on the frozen grid, kernel, local search, HPM, seeds), loaded from a hash-verified
copy of `Scripts/SMC_BVS/core` plus one appended test-only export (`scripts/abl_exports.cpp`). Only the setup is
replaced, by `cpp_abl_setup(ctx, B, mode)`:

| arm | π₀ | how |
|---|---|---|
| A | v3 block start (production) | mode 0 = production `cpp_setup` code path. **Checked bitwise** against the unmodified production `v3_fit` on a synthetic n=100, p=150 design: identical log Ẑ_r, PIP_r, HPM and frozen grid (`scripts/check_armA_bitwise.R`). |
| B | blocks of size 1 (independent Bernoulli × capped size prior) | mode 1: `make_blocks(D, 1)`, exact single-variable tables, production `build_start` (exact normaliser and sampler). |
| C | capped model prior ϖ | mode 2: blocks of size 1 with every log r_b set to 0; `build_start` then gives exactly π₀ = ϖ(S)/Z̄₀ on {|S| ≤ K}. |
| D | backfit start of API-RESID (fixed-point sweep rule, ≤ 10 sweeps) | mode 3: production blocks, tables log r_b computed on the residualised response (API-RESID's formulas and `block_stats.cpp`, `scripts/backfit_tables.R`). The tables are a deterministic function of (X, y), so π₀ is a fixed product law with exact normaliser and exact sampler (production `build_start`); Ẑ stays unbiased. |

In all arms the kernel's B (m = p + B + 2 labels per round) and the neighbour graph N(j) are the production ones, so
the only difference is π₀ (its draws at stage 0 and in the independence move I, and the bridge's γ₀). The table
entries actually built are offered to the HPM ledger as in production (arm A: all 2^B sub-models per block; arms B, C:
the p singletons; arm D: the production blocks' entries scored on the full y, as in A).

**Designs.** p = 500, scenarios S1–S6, two designs each: replicate r001 at c = 1 (`c100`) and replicate r002 at
c = 0.5 (`c050`); 12 designs × 1 seed (study `method_seed`). Seeds are in `results/per_fit.csv`.

**Reference.** For arm X on a design: the islands of all *other* arms on the same design are pooled (leave-one-arm-out).
log Ẑ_ref = log of the mean of their Ẑ_r (each is unbiased for Z whatever the start); PIP_ref = Ẑ-weighted mean of
their island PIPs. Best-known mode = argmax F over all arms' HPMs and S₀.

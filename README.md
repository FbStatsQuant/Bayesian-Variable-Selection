# Bayesian Variable Selection (SMC-BVS)

Local-to-global Bayesian variable selection: a sequential Monte Carlo sampler over models, with a g-prior slab and a Beta-Binomial BB(1, p) size prior. It reports the highest-posterior model among all models it scored (HPM), Rao-Blackwellised and plain PIPs, and an evidence estimate.

| Item | Version |
|---|---|
| Method | SMC-BVS v3 |
| Code (frozen, used for every New Campaign run) | **v2.2.1** |
| Code (2026-10-23 production run) | v2.1, kept |

**Start here:**

| If you want… | Read |
|---|---|
| the plan from here to the paper | [`Docs/PLAN.md`](Docs/PLAN.md) |
| the theory targets we will pursue | [`Docs/THEORY_PRIORITIES.md`](Docs/THEORY_PRIORITIES.md) |
| every theorem and its status | [`Docs/THEORY.md`](Docs/THEORY.md), one-pagers in `Docs/Theory/one_pagers/` |
| how the HQ agent runs this project | [`Docs/HQ/BOOTSTRAP.md`](Docs/HQ/BOOTSTRAP.md), [`Docs/HQ/RULES.md`](Docs/HQ/RULES.md) |
| what must be refreshed after the experiments | [`Docs/SYNC_LATER.md`](Docs/SYNC_LATER.md) |

Data and per-seed outputs are **not** in Git. The New Campaign's bulk data currently lives in the data mirror on Felipe's PC, and earlier archives are off-repo too; see `Docs/Records/DATA_INDEX.md`. The git-ignored `_data/` on Owls is the intended always-on store, but it is empty: moving data there is Felipe's decision. Heavy compute runs on the NOTS cluster from the bundles in `Scripts/`.

## Layout

```
README.md
Docs/
  PLAN.md  THEORY.md  THEORY_PRIORITIES.md  SYNC_LATER.md  PUSH_CHECKLIST.md
  HQ/            BOOTSTRAP, RULES, OPS_FACTS, DECISIONS (final log D1–D94), STATUS (results summary)
  Campaigns/2026-10-28_New_Campaign/   charter, status, decisions, campaign plan, theory-extraction strategy (snapshot)
  Theory/        THEORY.tex/pdf, THEOREM_MAP, RULINGS, DROPPED; theorems/ (T01–T36);
                 proofs/ (locked register, statements, proofs, reviews); PAPER_SELECTION_20261028/
                 (frozen paper list, consultant reviews, new conjectures T37–T39);
                 INVENTORY_20261028/; one_pagers/ (T01–T39); legacy_pre_v3/
  Methodology/   METHODOLOGY_v3, master methodology and plan
  Records/       run records, handoff plans (GH_HANDOFF/), status briefing 2026-10-28, LEVERS
  History/       earlier campaigns, HQ tracker history
  Literature/
Scripts/
  Campaigns/2026-10-28_New_Campaign/   the vetted New Campaign code, bundles and review records (see its README)
  SMC_BVS/       v2.1 method code and its tooling (2026-10-23 production)
  Benchmarks/    the 8 benchmark methods of the n = 200 study + scoring (produced the reused p ≫ n benchmark results)
  Data_generators/  Exact/
Results/         final summary tables: 2026-10-23 production, benchmark study, and 2026-10-28_New_Campaign/ (L_20261102, H2_20261102, H_existing_20261030)
Papers/          reference papers
Others/          legacy holding area (no new material)
```

Folder-by-folder detail for the v2.1 code, the benchmark study, Results and Papers (the previous README) is kept in `Docs/Records/README_v2_1_layout.md`.

## The New Campaign code (`Scripts/Campaigns/2026-10-28_New_Campaign/`)

Relative paths are preserved from the campaign folder, so bundles still find each other.

| Path | What | Frozen manifest |
|---|---|---|
| `code/core/v2_2_1/` | SMC-BVS v2.2.1: one tree for both regimes (H: p ≫ n; L: p ≤ 30), P5 retry, plain PIPs, scored-model registry | `code/core/v2_2_1.SHA256SUMS` (27 files) |
| `code/core/v2_2/` | v2.2 (used by the NOTS identity gate) | `code/core/v2_2.SHA256SUMS` |
| `code/lowp/` | low-p generator and sealing, exact 2^p enumerator, pilot bundle rev 7d | `code/CODE_LEDGER.md` |
| `code/bench_v2/` | p ≫ n benchmark adapters F1–F3 with the adaptive-lasso lasso-pilot fix | `MANIFEST_SHA256.txt` |
| `code/bench_lowp/` | the 8 benchmarks adapted to p ≤ 30 (r2) | `bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt` |
| `code/scoring/` | metrics, theory measures, headline tables | `code/CODE_LEDGER.md` |
| `conformance/jobs/PROD_H/` | p ≫ n production bundle (2,400 fits) | `BUNDLE_SHA256SUMS` |
| `conformance/jobs/CONF_NOTS_IDENTITY/` | v2.2 identity gate on NOTS | — |
| `jobs/PROD_L/`, `jobs/PROD_L_BENCH/` | low-p production: enumeration + SMC + repeats; the benchmark wave | bundle ledgers |
| `bench_audit/jobs/BENCH_F3_{DEV,PROD}/` | adaptive-lasso dev pilot and production rerun | `BUNDLE_SHA256SUMS_FINAL` |
| `ops/` | NOTS guard, ssh lock shim, sha256-verified pull and verified delete; run chains; final run record `FINAL_NOTS_STATE.md` and completion reports | — |
| `analysis/{L_20261102,H2_20261102,H_existing_20261030}/` | Scoring, table, evidence and tie-out-claim scripts behind the final reports (outputs in `Results/2026-10-28_New_Campaign/`) | — |
| `*/review/` | Sol reviews and fix records: the vetting evidence | — |

Re-check every manifest from the repo root:

```sh
sh Scripts/Campaigns/2026-10-28_New_Campaign/verify_manifests.sh
```

Frozen scripts are byte-identical copies of what ran, so they still contain the NOTS paths they ran with. Never "fix" a frozen file in place; a change needs a new version, a regression, a review and a ledger entry.

## Results (New Campaign, complete 2026-11-03)

| Regime | Headline | Theory evidence |
|---|---|---|
| Low p (exact posterior by enumeration) | `Results/2026-10-28_New_Campaign/L_20261102/HEADLINE_L.md` | `EVIDENCE_L.md` |
| High p (p ≫ n) | `Results/2026-10-28_New_Campaign/H2_20261102/HEADLINE_H.md` | `EVIDENCE_H.md` |

One-screen summary: `Docs/HQ/STATUS.md`. Bulk data locations: `Docs/Records/DATA_INDEX.md`.

The v2.2.1 rerun reproduces the 2026-10-23 fits (`Results/SMC_BVS_v3_production/`) exactly.
End.
# CONTEXT: theory inventory and alignment audit, SMC-BVS v3 (2026-10-28)

All paths are relative to the project root `<OLD_ROOT>\` (written below as `ROOT/`). Every file listed here is READ-ONLY for every worker. Workers write only to their own output file in `ROOT/01_Methodology_and_Theory/Theory_architecture_v3/INVENTORY_20261028/work/`.

## The three layers of "the method"

| Layer | What it is | Path | SHA-256 |
|---|---|---|---|
| L0: theory target | METHODOLOGY_v3.0. The 36 conjectures were written about this text. Some locked statements were later amended (DP2 D1–D4, wording fixes; e.g. T22(iii) uses EXP′ and DP2). Audit each statement's EFFECTIVE specification as written in its STATEMENT.md, amendments included. | `ROOT/01_Methodology_and_Theory/Methodology/SMC_BVS_v3_20261019/METHODOLOGY_v3.md` | 93043758…8019c |
| L1: deployed spec | Master Part I (sections I.1–I.9) of the master document. It adds the Decision Point 2 changes and the deployment rulings. | `ROOT/01_Methodology_and_Theory/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md` (Part I = lines ~122–588) | 7d77dddb…757b6e |
| L1 change records | DP2 decisions D1–D4, plus the L0→L1 changes and fidelity table | `ROOT/01_Methodology_and_Theory/MASTER_Methodology_and_Plan/deployment_20261022_v3/source_snapshots/DP2_DECISIONS.md`; `.../deployment_20261022_v3/CHANGES.md`; `.../deployment_20261022_v3/source_snapshots/RULINGS_OPEN.md`, `RULINGS_2.md`, `RULINGS_3.md` | |
| L2: executed code | The production core v2.1 (core byte-identical to A's v2) that produced all 2,400 fits | `ROOT/02_Experiments/H_2026-10-22_smcbvs_v3_deploy/E_ops_claude/v2_1/code/core/` (R files `v3*.R`; C++ in `cpp/`); its README.md lists every production change from the prototype | `source_manifest.json` there |

The study layer (`.../v2_1/code/study/adapter.R`, `run_case.R`) maps the core output to the reported rules: `hpm` = the primary HPM; `pip05` = primary PIP > 0.5.

## Theory files

- Register of what is proved: `ROOT/01_Methodology_and_Theory/Theory_architecture_v3/proofs/LOCKED_PROOFS.md` (19 rows, 21 theorem entries; hypotheses and dependency closure).
- Statements of the proved results: `ROOT/01_Methodology_and_Theory/Theory_architecture_v3/proofs/<folder>/STATEMENT.md`. The folder names are in LOCKED_PROOFS.md. Proofs are in `<folder>/proof/PROOF_v*.tex`. Read the proof only when the statement does not make clear which algorithmic object it models.
- All 36 conjectures (proved or not): `ROOT/01_Methodology_and_Theory/Theory_architecture_v3/theorems/T*.md`; common notation in `theorems/00_COMMON.md`; overview in `THEORY_BRIEF.md`; ranks and dependencies in `THEOREM_MAP.md`; dropped items in `DROPPED.md`.
- Standing idealisations: EX-A (exact arithmetic), EX-S (ideal independent uniform random streams), CAL (calibration uses streams 0–9 only; the final run uses streams 10–13), EXEC (scans completed).

## Study setting that was executed

n = 200; p ∈ {500, 1000}; true model size s0 = 14; six covariance scenarios S1–S6 (master Part II.4); signal scales c = 1 and c = 0.5; 100 replicates each; 2,400 fits. The settings table is master §I.8; the empirical results are in `EMPIRICAL_SUMMARY.md` in this folder.

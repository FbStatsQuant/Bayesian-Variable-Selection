# SMC-BVS v3 deployment: n = 200, p ∈ {500, 1000}, scenarios S1–S6, scales c = 1 and c = 0.5 (2026-10-22)

**Owner.** Felipe. **Manager and reviewer:** the v3 lead (Claude, thread mcp:5e4b26e1…). The managing lead launches the threads, reads their STATUS.md files, reviews code and results, and gives the GO for production. **Execution is OpenAI-only:** each thread is led by GPT-6 Astra (high) and spawns GPT-6.1 Sol (high) and GPT-6 Astra (high) agents.

## 1. What is decided

- **The method is fixed. Nobody changes or retunes it.** It is SMC-BVS v3 exactly as written in Part I of
  `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\01_Methodology_and_Theory\MASTER_Methodology_and_Plan\MASTER_Methodology_and_Plan.md` (SHA-256 7d77dddb968135d86a6b6431a7a3e04e122eb0c09f5ec9a6a8329e9a20757b6e). It has been verified as "ready to deploy from" after 3 rounds. Supporting files: `...\MASTER_Methodology_and_Plan\deployment_20261022_v3\` (CHANGES.md, RULINGS_*.md, VERIFY_PART_I_r*.md, source_snapshots\).
- **Reference implementation:** the independently verified R + C++ prototype, in `...\deployment_20261022_v3\source_snapshots\prototype_core\` (checksums in prototype_core.sha256; the original is on NOTS at /projects/ml75/fb31/BVS/v3_profiling_20261020/code/core/).
  - Part I governs. Its deliberate differences from the prototype are listed in CHANGES.md: no secondary PIP, the `cut_group` flag, the `local_certified` tie rule, a memory-only preflight plus an in-run time guard, and no profiling features.
  - Everything else, including the order of random draws, must reproduce the prototype bit for bit given the same seed.
- **Design, already run for the benchmark study.** Master Parts II–IV, the benchmark study `...\02_Experiments\F_2026-10-19_benchmark_study_n200\Benchmark_Study_20261019\`, and the c = 0.5 preregistration `PREREG_c050.frozen_20261021.md` there.
- **The SMC arm uses EXACTLY the benchmark datasets:**
  - the 1,200 Regime-H cases under `$STUDY/inputs` on NOTS ($STUDY = /projects/ml75/fb31/BVS/bench20261019), keyed by `dataset_id`;
  - Y column by `scale_key`: c = 1 → `c100`, c = 0.5 → `c050`;
  - data seeds per master §II.7;
  - method seed = data seed + 4,000,000, recorded as `method_seed`;
  - output rule rows per master §IV.1.4: `method_id="SMCBVS"`, `rule_id ∈ {hpm, pip05}`, and the join asserts equal `x_sha256`/`y_sha256`.
- **Units:** 1,200 cases × 2 scales = 2,400 fits. The sealed held-out set (`$STUDY/holdout`) is NEVER read, and the `truth/` folders are never read by the fitting code. Only the scoring step reads truth, exactly as the benchmark scoring did.

## 2. Threads and ownership

Each thread writes ONLY to its own folders.

| Thread | Job | Local folder | NOTS folder |
|---|---|---|---|
| A build | Production implementation of Part I, starting from the prototype; bit-level regression tests against it; NOTS build | `A_build\` | `$D/code/` |
| B verify | Independent checker: its own reference code written from Part I only, never A's code (a scorer, exact enumeration for small p, start-sampler law tests); then a code review of A's v1 and cross-checks of outputs | `B_verify\` | `$D/verify/` |
| C ops | Data and seed verification against the benchmark manifests; runner and Slurm arrays; the pilot; production after the managing lead's GO; pulling outputs to the laptop | `C_ops\` | `$D/runs/`, scratch |
| D analysis | Scoring with the benchmark study's own scoring code and metrics; first reproducing the published benchmark tables, then joining the SMCBVS rows; the comparison tables and figures | `D_analysis\` | `$D/analysis/` |

- $D = /projects/ml75/fb31/BVS/smcbvs_v3_deploy_20261022. Small files only (the ml75 group quota is shared).
- Bulk outputs go to /scratch/fb31/smcbvs_v3_deploy_20261022/ and are pulled to `C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\` when finished. No hefty data stays on NOTS.
- Local folders are under `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\02_Experiments\H_2026-10-22_smcbvs_v3_deploy\`.

**Hand-offs.**
- A publishes `A_build\HANDOFF_v1.md` (frozen code path plus checksum, build command, test evidence). B and C read it.
- C publishes the pilot results in `C_ops\PILOT.md`. D reads `C_ops\OUTPUTS.md` for output paths.
- Threads never edit each other's files. Requests go through the managing lead, by writing them in your own STATUS.md under "Requests".

## 3. Gates (managing lead)

- **G1, before the pilot:**
  - A v1 passes its regression tests against the prototype;
  - B's independent checks pass on A v1;
  - C's data and seed check passes.
- **G2, before production:** the pilot (about 24 cases across S1–S6 × p × c on the dev/pilot seeds of §II.7, never production cases) gives runtime, memory, failure rates and a core-hour estimate. The managing lead reviews and gives GO in `GO_PRODUCTION.md`.
- **G3, results:** D's tables, independently recomputed by a Sol agent on a sample of cells; then an Astra review of the results.

## 4. Rules

- **Research code** (C:\Users\felip\.claude\protocols\research-code.md):
  - every core-code file is logged in the project's `CODE_LEDGER.md`, under a new section "SMC-BVS v3 deployment". Append rows only.
  - Core code is verified by someone other than its author.
  - Results stay provisional until the code is verified.
- **Compute:** all multi-seed work runs on NOTS through Slurm. Development and single-case tests may run on NOTS interactively or on Owls.
- **NOTS access:** `ssh nots`, which routes through Owls (see ~/.ssh/config). A connection repair is in progress today. If `ssh nots` times out, use `ssh -J owls -i ~/.ssh/id_rice -o IdentitiesOnly=yes -o HostKeyAlias=notsx.crc.rice.edu fb31@10.226.96.48` (loginx3) or `@10.226.96.47` (loginx2). Never edit ~/.ssh/config: the repair team owns it.
- **Modules:** GCC/14.3.0 and R/4.5.2 (as in the profiling campaign).
- **Never touch these** (read-only use of `$STUDY/inputs` and `$STUDY/manifests` is allowed):
  - /projects/ml75/fb31/BVS/bench20261019/ and /home/fb31/projects/BVS/Benchmarks/: frozen until RELOCATION_OK.md exists;
  - the sealed truth folders;
  - other users' files.
- **Before any Slurm array:** a frozen code snapshot with manifest.json (code checksum, command, job ID, seeds, environment, input checksums, output paths), and a row in `RUNS.md` at the deployment root.
- **Seeds** are tied to dataset IDs, never to array indices. Every unit must be reproducible alone.
- **Usage limits:** if your account hits a usage limit, stop cleanly and leave a resume point in STATUS.md. Never shut work down for that reason; resume after the reset.
- **Every thread keeps `<thread folder>\STATUS.md` current**, at least hourly. It holds: phase, what runs (job IDs), blockers, "Requests", the resume point, and agent counts per model.
- **Never fabricate.** Report failures plainly, with evidence.

---
## AMENDMENT 1 (Felipe, 2026-10-22 ~19:05Z): SKIP NOTS AND RUN ON OWLS, AT MOST 10 SEEDS PER SCENARIO

This overrides §1–§4 wherever they conflict.

**Compute.**
- No NOTS at all: no ssh or scp to NOTS, no Slurm.
- All building, testing and running happens on Owls (`ssh owls`, owls.stat.rice.edu; R 4.6.0, GCC 11.5.0, 80 cores, 92 GB RAM, shared /home).
- Owls is a SHARED LAB MACHINE. Felipe's rule is "do not monopolize".

**Owls caps across ALL deployment threads combined.**

| Resource | Cap |
|---|---|
| Cores | ≤ 16 busy at any time, at most 4 per thread for development; only C runs the batch, and C gets the remaining share |
| Memory | ≤ 24 GB resident in total |
| Priority | every process runs under `nice -n 19` |
| Disk | ≤ 20 GB in your area of `~/smcbvs_v3_deploy_20261022/` on Owls |

- **Before starting any batch,** check `uptime` and `free -g`. If the 1-minute load is above 40, or available memory is below 30 GB, wait and retry in 15 minutes.
- **Owls folders:** each thread writes only to its own subfolder of `~/smcbvs_v3_deploy_20261022/`: `A_build/`, `B_verify/`, `C_ops/` or `D_analysis/`.
- **Disk:**
  - Delete scratch intermediates once they are verified.
  - Pull finished outputs to the laptop at `C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\`: copy, then sha256-verify, then delete on Owls.
- **SSH discipline:** batch commands into one ssh call, and do not open many parallel connections.

**Design: the assessment run.**
- Use the benchmark study's own production cases, replicates r = 1..10 of each scenario: S1–S6 × p ∈ {500, 1000} × r = 1..10, so 120 datasets.
- Each dataset is fitted at both scales, c100 and c050: **240 SMC-BVS fits**, on exactly the datasets and seeds the benchmarks used, so the comparison is direct.
- **Inputs** come from the verified laptop copy, C:\Users\felip\Documents\NOTS_BVS\NOTS_projects_ml75\BVS\bench20261019\inputs\ (manifests in ..\manifests\).
  - C copies only the needed 120 files to Owls and verifies their sha256 against the manifest.
  - Never read truth or holdout for fitting. Only D's scoring reads truth, from the laptop copy, as the benchmark scoring did.
- **Method seed** = data seed + 4,000,000, as before.

**Gates.**
1. A v1 must pass on Owls: build there, then the prototype regression tests rerun on Owls.
2. B's verdict on A v1.
3. C's data check.
4. One smoke fit per p on a dev/pilot dataset, reporting time and memory.
5. The managing lead gives GO, and C runs the 240 fits under the caps.
6. D scores and compares against the benchmark rows for the same 120 datasets.

The full 1,200-case production run is deferred until these results are assessed.

---
## AMENDMENT 2 (Felipe, 2026-10-22 ~19:10Z): BUILD FIRST, THEN RUN ON NOTS IF IT IS AVAILABLE

**Phase now.** Priority is building the ENTIRE code infrastructure we will deploy:
- the method (A);
- the independent verification (B);
- the data/case table, the runner, snapshot and manifest tooling and pull tooling (C);
- the scoring and analysis pipeline (D).

Development and tests happen on Owls, under Amendment 1's caps, and locally.

**Runs.**
- Once the code is written and verified (G1), the managing lead decides where to run.
- **NOTS, if it is available then.** This is the preference. The route is now `ssh nots`, direct from this PC to loginx3. The rules: one ssh connection per thread, batched commands, poll every 10 minutes or less often, and back off 15 minutes after any timeout.
- **Otherwise Owls.**

**C's runner must therefore support both backends:**
- a capped local queue on Owls (Amendment 1);
- Slurm arrays on NOTS: chunks keyed by dataset ID, frozen snapshot plus manifest.json, scratch outputs, and pull to the laptop.

Same unit definition and output schema in both.

**Scope.** Unchanged: first the 240-fit assessment (r = 1..10). The full 1,200-case run comes after the results are assessed.

Until the managing lead writes "NOTS: open for runs" in STATUS.md, no thread uses NOTS. Read-only checks of `$STUDY/manifests` are allowed with ONE batched call.

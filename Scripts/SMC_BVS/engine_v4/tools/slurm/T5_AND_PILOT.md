# T5 at 10⁵ and the 10⁶ calibration pilot: commands and cost quotes (WP7 O5)

Both runs go through the WP5 driver (dry run on Owls, submission on NOTS by the manager). Builder 7 never submits.
Every core-h figure below is an ESTIMATE unless it says MEASURED.

## Preconditions
| run | needs merged into `exp/P1M-engine` (then frozen as `code_commit`) |
|---|---|
| T5 at 10⁵ (gate P4) | `setup` (WP2 #13), the `island` command (WP3), O1 (#47), O2 (#49), O5 (this), K1 (#48) |
| 10⁶ pilot (gate P7, H-11 (2)) | the T5 list + K3 (Gram rows) + WP3's StartView (`--plan-only` with the island plan); the pilot's `mem` re-set from the printed plan |

The `island` command (WP3) should:
- checkpoint to `<out>.ckpt` (`IslandConfig::ckpt_path`, every 600 s) and resume on a rerun;
- write `island_r.bin` through `write_island_file`, which carries `meta.cost` (O2) automatically.

T5 checks both.

## 1. T5 at 10⁵: the whole fit `5-AR-n200-r01-V-s1` (AR strong, n = 200, p = 10⁵, V, N = 2,500, R′ = 16)
On Owls (dry run):
```
cd Scripts/SMC_BVS/engine_v4/tools/slurm
# set code_commit in examples/plan_T5_1e5.json to the frozen commit first
python3 p1m_driver.py --plan examples/plan_T5_1e5.json --out /home/fb31/SMC_Engineering_Department/scripts/T5_1e5
```
On NOTS (manager):
```
cd ~/SMC_Engineering_Department/scripts/T5_1e5
mkdir -p code && git -C <clone> archive <code_commit> | tar -x -C code
bash build.sh                                   # -DV4_ISLAND_ISA=sapphirerapids (plan key island_isa)
CONFIRM=yes bash submit.sh                      # setup -> calibrate -> 16 islands -> merge -> eval (+post)
```
After it ends (Owls or NOTS):
```
python3 p1m_stage_cost.py t5 ~/SMC_Engineering_Department/scratch/runs/T5_1e5/5-AR-n200-r01-V-s1 \
        --bin ~/SMC_Engineering_Department/scripts/T5_1e5/bin/smcbvs4 --json t5_report.json
python3 p1m_cost.py --sacct <sacct dump> --submissions .../T5_1e5/submissions.jsonl --out-dir <dir>   # billed core-h
```
The report gives:
- per calibration island: the per-stage table (`$RUN/cost/*.jsonl`);
- per final island: `meta.cost` through `smcbvs4 info --meta 1`;
- the merge's `merge_islands_seconds`, `tail_local_seconds` and `ls0_seconds` (`fit.bin.json` `timings`);
- calibrate's `seconds`.

| stage | request | limit | worst case | expected (ESTIMATE) |
|---|---|---|---|---|
| setup | 32 CPUs, 16G | 0:30 | 16 | ≈ 1 |
| calibrate | 64 CPUs, 24G | 1:00 | 64 | ≈ 10–25 (pilot + 8 diagnostic islands of H, leader stores serial: R2) |
| islands | 16 × 48 CPUs, 16G | 0:20 | 256 | ≈ 35–120 (≈ 1.8·10¹⁰ steps per island × 500–1,100 ns·CPU; 4–14 min each) |
| merge (tail + LS0) | 16 CPUs, 16G | 0:30 | 8 | ≈ 1–4 (LS0 at 10⁵ is unmeasured: T5 measures it) |
| eval + post | 8 CPUs, 16G | 0:45 | 6 | ≈ 1–3 |
| **total** | 20 tasks | | **350** (driver, MEASURED from the limits) | **≈ 50–150, central ≈ 85** (manifest T5 row: 200) |

Basis:
- **Per-step cost:** ≈ 1,056 ns·CPU per step in late 10⁵ rounds on SPR today (MEASURED, job 2748104). O1 and K1 lower it (ESTIMATE −25 to −45%).
- **Steps per island:** T + 12 rounds at a T of 40–120 (G0 had 28–36 at 5k–10k).

## 2. The 10⁶ calibration pilot (H-11 gate (2)): `6-AR-n200-r01-V-s1`, setup → pilot island only
On Owls (dry run):
```
python3 p1m_driver.py --plan examples/plan_P7_pilot_1e6.json --out /home/fb31/SMC_Engineering_Department/scripts/P7_pilot_1e6
```
On NOTS (manager):
```
cd ~/SMC_Engineering_Department/scripts/P7_pilot_1e6
mkdir -p code && git -C <clone> archive <code_commit> | tar -x -C code
bash build.sh                                   # builds smcbvs4 and v4_pilot_island
CONFIRM=yes bash submit_pilot.sh                # setup[1] -> pilot[1] (aftercorr); NEVER submit.sh before HQ's GO
```
After it ends:
```
python3 p1m_stage_cost.py table ~/SMC_Engineering_Department/scratch/runs/P7_pilot_1e6/6-AR-n200-r01-V-s1/cost_pilot/cost_pilot_t0_k0_r0.jsonl
cat .../6-AR-n200-r01-V-s1/pilot.json           # T, forced steps, seconds, peak RSS, settings
```
What it runs:
- `v4_pilot_island` (`include/v4/island/pilot_only.h`) is the first island of `calibrate --mode V`: the same settings, runner, IslandSpec and seed. The test `pilot_only_equals_calibrate_pilot` checks it step by step against calibrate's own pilot record.
- With `--with-ledger 1` it also holds the calibration ledger with the table stores, so the task's memory is the calibration task's.
- The setup.bin stays in the run directory for the fit.

| stage | request | limit | worst case | expected (ESTIMATE) |
|---|---|---|---|---|
| setup (10⁶) | 48 CPUs, 48G | 1:00 | 48 | ≈ 5–15 |
| pilot island | 96 CPUs (one socket), 64G | 1:00 | 96 | ≈ 20–35 (WP3_ARCH_REVIEW §8.4: ≈ 27 with levers 1–3 at E₀ = 10; production E₀ = 3.6) |
| **total** | 2 tasks | | **144** (driver) | **≈ 25–50** (H-11: 27–50 for the island; ceiling ≈ 100) |

This run measures, at the target size with the real start law:
- M(φ) and |S|(φ);
- offers per stage at production N;
- the compactions and their seconds;
- the I1 check seconds (O1's SPR saving, against job 2749328's ≈ 5.7 s per step);
- the peak RSS.

Re-size per stage from it (R1, WP3_ARCH_REVIEW §8.2). If `pilot.json` shows resource_limit, re-set `pilot.mem` from the printed plan (calibrate `--plan-only`, P5) and resubmit `submit_pilot.sh` only.

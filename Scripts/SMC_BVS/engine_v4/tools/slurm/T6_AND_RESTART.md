# T6 by real kills at 10⁵, and the restart chain (WP7 O4)

Every core-h figure is an ESTIMATE unless it says MEASURED.

## Restart chain (plan key `restart`)
A final island whose task ends at its Slurm limit resumes from `island_<r>.ckpt.{a,b}`. Two mechanisms:
- **Soft stop** (`island --stop-after-s S`): the stage script passes `S = limit − margin − (seconds already used)`. At the first
  step boundary after S, the island writes a checkpoint and exits 22; the task ends cleanly. The margin must cover the step in
  flight and the checkpoint write: default `max(300 s, 15% of the limit)`.
- **Hard kill at the limit:** the island's last periodic checkpoint (every `--ckpt-every-s`, default 600 s) survives; the next attempt
  resumes from it (`load_ckpt` removes the dead writer's `.tmp.<pid>`).

```json
"restart": {"attempts": 3, "margin_s": 600}
```
- `submit.sh` submits the islands array `attempts` times: attempt k+1 with `--dependency=afterany:<attempt k>`. Merge, eval and the ISA check wait (`afterok`) for the last attempt.
- Each attempt's task:
  - skips a finished island (`island_<r>.done`);
  - repeats the exit code of a failed one (`island_<r>.failed`: a real failure is not retried);
  - otherwise runs the island, which resumes from its checkpoint.
- An island still unfinished after the last attempt ends with exit 22, so merge does not start.
- **Cost:** the driver counts every retry array at its limit in the worst case (Σ CPUs × limits), because it cannot know which islands will need one. A `core_h_cap` set for one attempt therefore refuses a chain. A finished island's retry task costs seconds, so the billed cost is the cost of the work.
- Tasks: a chain adds `Rp × (attempts − 1)` queued tasks per fit (150-task cap per batch).
- Without the key the plan is unchanged (one array, no soft stop).

## T6 by real kills (plan `plan_T6_1e5.json`, `t6_only`)
One island of the T5 fit `5-AR-n200-r01-V-s1`, on its real data/setup/calib, through `smcbvs4 island`:
1. reference: uninterrupted, no checkpoints;
2. kill 1 (SIGKILL by PID): after a second checkpoint generation of the process exists;
3. kill 2: during a checkpoint write (the writer's `.tmp.<pid>` appears, then the kill is immediate);
4. a last run resumes and finishes.

It checks: each killed process died of SIGKILL and left no island file; `resumed_from_step ≥ 1`; the record is `completed`; the output hash and every non-meta section hash equal the reference's; the checkpoint files are gone. Only processes started by the script are killed, by PID.

MEASURED locally (Owls, 3 threads, p = 2,000, n = 200, real gen → prep → setup → calibrate → island, `--ckpt-every-s 4`): kill 1 after 11.5 s (second checkpoint), kill 2 at 6.6 s into the resumed process during the write of `island.ckpt.a.tmp.<pid>`, resumed from step 6; output hash and all sections equal the reference (`0xceb29551194accf4`); checkpoint seconds in the final run 0.37 s.

### NOTS: exact commands (the manager submits)
Needs the T5 run directory `~/SMC_Engineering_Department/scratch/runs/T5_1e5/5-AR-n200-r01-V-s1/` (data.bin, setup.bin, calib.bin) and the frozen `code_commit`.
```
cd Scripts/SMC_BVS/engine_v4/tools/slurm
# set code_commit in examples/plan_T6_1e5.json first
python3 p1m_driver.py --plan examples/plan_T6_1e5.json --out ~/SMC_Engineering_Department/scripts/T6_1e5
# on NOTS:
cd ~/SMC_Engineering_Department/scripts/T6_1e5 && mkdir -p code && git -C <clone> archive <code_commit> | tar -x -C code
bash build.sh                       # -DV4_ISLAND_ISA=sapphirerapids (the same ISA family as T5)
CONFIRM=yes bash submit_t6.sh       # one task: 48 CPUs, 24G, 50 min
# afterwards: cat ~/SMC_Engineering_Department/scratch/runs/T6_1e5/5-AR-n200-r01-V-s1/t6.json   ("ok": true)
```

| item | request | limit | worst case | expected (ESTIMATE) |
|---|---|---|---|---|
| T6: reference + 2 killed runs + the resumed run | 48 CPUs, 24G | 0:50 | **40 core-h** (cap 50) | ≈ 5–16 (≈ 3.2 island-equivalents at 48 CPUs: 1.6–5 min each at 10⁵; kills at the second checkpoint and in a write, `--ckpt-every-s 20`) |

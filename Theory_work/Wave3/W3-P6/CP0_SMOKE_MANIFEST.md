# W3-P6 — CP0 smoke manifest (resume leg A, 2026-11-11, lead Opus 5.5)

Nothing here is submitted until HQ and the owner approve CP0 (PROTOCOL rule 10, "Compute tickets").
Facts below were read back from NOTS read-only on 2026-11-11 13:54–14:00 CT (ls, sha256sum, sacct, squeue, scp *from* NOTS).

## 1. Unit of account
`sacct` reports **AllocCPUS = 2 for every one of the 381 w3p6_ allocations** (the scripts ask for `--cpus-per-task=1`;
NOTS allocates a whole core = 2 hardware threads). CPUTimeRAW = 2 × elapsed. Everything below is in **CPUTimeRAW core-hours**,
so one task-hour costs 2 core-h and the worst case of a task is **time limit × 2**.

## 2. Core-hours already used (all w3p6_ jobs since 2026-11-09, CPUTimeRAW)
| job | Slurm id | allocations | state | core-h |
|---|---|---|---|---|
| w3p6_probe01 | 2647903 | 25 | 10 COMPLETED, 15 CANCELLED (at 4.73 h) | 158.99 |
| w3p6_b1 | 2651495 | 320 | 298 COMPLETED, 22 CANCELLED | 255.00 |
| w3p6_smoke_v3 | 2652108 | 2 | 2 COMPLETED | 0.44 |
| w3p6_b2 | 2652199 | 34 started | 34 CANCELLED (at ≤ 1.20 h); 206 never started | 81.45 |
| **total** | | 381 | queue now empty (`squeue`) | **495.88** |

## 3. Smoke set (5 tasks, two runs; exact production command lines, production seeds)
Each smoke task is a production key re-run under a new RUN_ID (DESIGN §5 policy: a Slurm interruption is rerun once with
the same seeds). Its result counts as that key's production record. Partition/account/QoS `commons`, `--no-requeue`.

| # | run (RUN_ID) | driver | origin task | cell | rep (seeds: data / method) | why | Slurm limit × CPUs | worst core-h |
|---|---|---|---|---|---|---|---|---|
| S1 | smk1_v2 | v2 (b1) | b1 #62 | cs ρ=.5, s₀=4, n=50, p=500 | 2 | v2 driver; largest p at n=50 (b1 max 1.52 h, med 1.25 h; this seed ran 1.55 h unfinished when cancelled) | 04:00:00 × 2 | 8 |
| S2 | smk1_v3 | v3 (b2) | b2 #41 | cs ρ=.5, s₀=4, n=75, p=750 | 1 | largest p at n=75; never run | 24:00:00 × 2 | 48 |
| S3 | smk1_v3 | v3 | b2 #61 | cs ρ=.5, s₀=4, n=100, p=250 | 1 | costs the 7 b2 cells at (100,250) (≈ half of b2); probe ran 4.73 h unfinished. **Optional: HQ may strike it** | 24:00:00 × 2 | 48 |
| S4 | smk1_v3 | v3 | b2 #21 | cs ρ=.5, s₀=4, n=150, p=150 | 1 | only n=150 cell; probe ran 4.73 h unfinished | 24:00:00 × 2 | 48 |
| S5 | smk1_v3 | v3 | b2 #1 | cs ρ=.5, s₀=4, n=100, p=1000 | 1 | largest p at n=100; probe ran 4.73 h, b2 seeds 1.20 h, none finished | 24:00:00 × 2 | 48 |

Seeds are the DESIGN §1 formula (data seed from rep, n, p, design, s₀, ρ; method seed = data seed + 4·10⁶), computed by the
frozen driver from the command line; nothing is re-seeded.
n = 200 (group B) and (50, 2500) are **not** in the smoke: they are conditional cells that the ceiling cannot afford (§5).

**Task tables (local, to be copied to NOTS and frozen by `submit_table.sh`):**
`configs/smk1_v2_tasks.tsv` sha256 `2d9cae2b79e40c0d672dbdd2943090c1035d1aeb9268f68d9e8a19e357a9a8eb` (1 line);
`configs/smk1_v3_tasks.tsv` sha256 `a208842ce9efe7dd61b6e47eb9812360a0df9b918c01475991009842bcdba791` (4 lines, order S2, S3, S4, S5).
Each line is byte-identical (after the task id) to the origin line in the frozen `runs/b1/tasks.tsv` / `runs/b2/tasks.tsv`.
If HQ strikes S3, I delete line 2 and renumber before submission (new sha recorded in LOG).

**Frozen scripts (submission passes the frozen run dir as SCRIPTS_DIR; the new manifest must reproduce these sha256):**
- v2 (`runs/b1/scripts`): p6_fit.R `64d2d74bb47a14755be1392231e64237f49a08a6cc8bb87e58e6b5ed1e23d1e4`,
  make_tasks.py `765cff4f1cbb27dedc7d76b87faf531246187ca4673bce5911f830c7f9e836ea`,
  summarize.py `400d7c34bf239bdcb9d4203a70704e98617d615e89bae82a84619862185c663c`.
- v3 (`runs/b2/scripts`): p6_fit.R `ba5299fbce6e24c62f8094132e406387225831fdeb9e814d9210163ba2dbd8f3`,
  p6_common.R `2bf08d62965a73b6d1195ac5bed4934a0a2cac0b032a1983d73c32abf792d6bc`,
  rederive.R `a94098bc0efe46ce735983eb757cc7d3ecc6cde276e22398e324045e78af3da2`,
  make_tasks.py `fe11d63fe456e77ce7e88a9cd620855c6f161834b3db0d6f9c312a66678172c4`,
  summarize.py `8011253eec0e1590a89f839c15b2ce5b1292bee526b2c9eb016a131f0b7835be`.
- Both: run_table.sh `adc805535805392550e6aa74f20d3870de1330d034ea37c14553b326c401b2ac`,
  env_sim.sh `a7fce02547e42c387a719b982268ee601964c4668587ee2f449960d7abe6ceca`, submit_table.sh (sim/)
  `f47aabe5f7e7d8cba44f540949dc31dc3c36afa8d0842c273866340cf65d9c73`.
- Code: `code/main_2252d57/repo` (COMMIT 2252d5730c43…); its 20 core files are sha256-identical to a fresh
  `git archive 2252d57 Scripts/SMC_BVS/core` made today. (The LOG's "SHA256SUMS" file does not exist on NOTS; this check
  replaces it.)
- The local repo copies equal the v3 frozen set (p6_common.R and summarize.py modulo CRLF only).

**Submission commands (next leg, after approval; not run):**
`sim/submit_table.sh smk1_v2 <smk1_v2_tasks.tsv> runs/b1/scripts commons 04:00:00 6G 1` and
`sim/submit_table.sh smk1_v3 <smk1_v3_tasks.tsv> runs/b2/scripts commons 24:00:00 8G 4`
(memory as in b1/b2; peak RSS seen in any w3p6 task ≤ 1.4 GB).

## 4. Worst-case admission (PROTOCOL rule 10 backstop)
| item | core-h |
|---|---|
| used (sacct CPUTimeRAW, §2) | 495.88 |
| queued + running w3p6_ now | 0 |
| smoke S1 (4 h × 2) | 8 |
| smoke S2–S5 (4 × 24 h × 2) | 192 |
| **worst-case total** | **695.88 ≤ 1,400** (647.88 without S3) |

Expected smoke cost (estimates, not measured): S1 ≈ 2.6, S2 ≈ 8–16, S3 ≈ 10–20, S4 ≈ 10–30, S5 ≈ 20–45 → **≈ 50–115 core-h**.
Wall clock ≤ 24 h (S5 dominates; the 22.5-h runtime guard returns `resource_limit` with the HPM so far before the 24-h limit).

## 5. Projected release plan after the smoke (re-costed at CP1 with measured times)
**Budget.** 1,400 − 495.88 = 904 core-h left before the smoke; ≈ 790–850 after it (expected). Note the watchdog places
`HOLD P6` above **1,200** (rule 12), so the working line is 1,200 unless HQ moves it.
**The full remaining design does not fit.** Expected cost of the rest of b2 (236 tasks) is ≈ 2,800 core-h at 2 CPUs per task
(the RESUME_PLAN's ≈ 1,240 counted task-hours, i.e. 1 CPU). The plan below is therefore a descoped, prioritised list.

Per-fit wall estimates (h): measured — n=50 cells (b1, 14–20 seeds), (100,100) 1.79 (1 seed), s5 (100,250) 3.86 (1 seed);
lower bounds only — cs (100,250), (100,1000), (150,150) > 4.73. Estimates used: (75,75) 0.6, (75,188) 1.2, (75,750) 6,
(100,250) 7, variants at (100,250) 6, (100,1000) 16, (150,150) 9.

**Plan A (recommended; 20 seeds per cell as in DESIGN, fewer cells):**
| batch | tasks | Slurm limit (illustrative; set at CP1 ≈ 1.5 × measured max, ≤ 24 h) | worst core-h | expected core-h |
|---|---|---|---|---|
| R1 | b1 remainder, 21 tasks (n=50: cs ρ=.5 s₀=4 p=500 reps 4–8; s5 p=250 reps 6,17–20; cs ρ=.5 s₀=8 p=250 × 11), v2 scripts | 3 h | 126 | 33 |
| R2a | (75,75) × 20, (75,188) × 20, (100,100) × 20, v3 | 3 / 4 / 4 h | 440 | 145 |
| R2b | (100,250) cs ρ=.5, reps 2–20 (19) | 12 h | 456 | 266 |
| R3 | (75,750) reps 2–20 (19), or fewer seeds if the ledger requires | 10 h | 380 | 228 |
Cumulative expected ≈ 496 + 80 (smoke) + 33 + 145 + 266 + 228 ≈ **1,250** — crosses the 1,200 watchdog line during R3;
R3 is sized at release so that expected spend stays ≤ 1,200 (≈ 12–15 seeds) unless HQ moves the line.
Each batch is admitted only if used + Σ(limit × 2 over queued and running) ≤ 1,400; R2a/R2b/R3 are sequential for that reason.
**Not run under the ceiling:** breadth variants at (100,250) (5 cells, ≈ 1,200 core-h), (100,1000) × 19 (≈ 610),
(150,150) × 19 (≈ 340), (50,2500), group B (n=200). Their only data are the smoke fits (one seed each; descriptive).
Coverage of Plan A, cs ρ=.5 s₀=4: p/n=1 at n ∈ {50,75,100} (+150 one seed), p/n=2.5 at n ∈ {50,75,100}, p/n=10 at
n ∈ {50,75} (+100 one seed); breadth only at n=50.

**Plan B (alternative): 10 seeds per cell, more n.** (75,75), (75,188), (100,100), (100,250), (75,750), (150,150) at 10
seeds (smoke seed included) ≈ 510 core-h expected (+ R1 33); adds n=150 at p/n=1, but Wilson intervals ≈ ±0.3 per cell.
(100,1000) at 10 seeds (+ ≈ 290) does not fit in either plan.

## 6. What I will report at CP1 (smoke gate)
- Per smoke task: sacct state, Elapsed, CPUTimeRAW, MaxRSS; RDS present; status (`completed` / `resource_limit` /
  preflight stop), `hpm_incomplete`; calibration tier, escalation, fallback; phase timings (calibration / final / LS0);
  preflight `est_seconds` vs actual.
- Invariants (any failure stops everything): new run manifests verify and reproduce the §3 sha256; seeds match the DESIGN
  formula; derivation status per cap `ok` or NA with a reason (tie/censored); |F_direct − F_ledger| = 0; HPM F is the ledger
  maximum; `rederive.R` reproduces the in-run derivation; S1's time and outcome lie within the b1 cell's range.
- Outcome class per cap (S₀ / posterior / search / NA) for the 5 fits — descriptive only.
- Ledger update: used core-h, measured per-cell times, the Slurm limit proposed per cell, and the re-costed Plan A/B
  batches with worst-case admission and expected cost each.

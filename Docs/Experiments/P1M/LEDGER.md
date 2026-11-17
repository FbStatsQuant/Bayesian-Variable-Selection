# NOTS core-hour ledger — SMC - Engineering Department

Envelope: **A + D ≈ 24,600 billed core-h** (HQ, 11-15; DECISIONS H-1).
Rules:
- **Exploratory batches** ≤ ~200 core-h each run on the HQ standing authorisation (11-15). They are logged here and in the
  daily report.
- **Gated stages** and batches above ~200 core-h need HQ's go.
- Billed core-h = allocated CPUs × elapsed (sacct CPUTimeRAW / 3600).
- Admission check before each submission: Σ actual (finished) + Σ worst case (time limit × CPUs, queued and running) +
  this batch's worst case ≤ envelope.

| date | batch | kind | job ids | worst case | actual | status |
|---|---|---|---|---|---|---|
| 2026-11-15 20:53 CST | G0 kernel benchmark (1 SPR node, 96 CPUs, 5 min) | gated (HQ go 11-15) | 2747371 | 8.0 | **0.88** | COMPLETED (33 s; benchmark segfault after the T = 1 offer test, results kept) |
| 2026-11-15 20:53 CST | G0 stage-level re-runs (5k: 16 islands, 7 h limit; 10k: 8 islands, 17.5 h), revision D unmodified | gated (HQ go 11-15) | 2747372_[1-2] | 49.0 | task 1: 0.001 (FAILED in 2 s: invalid `timeout 6h57m`); task 2: 16.87 | task 1 failed; task 2 COMPLETED (8 h 26 min; 8/8 islands; HPM = truth; sd(log Z_r) 1.099) |
| 2026-11-15 22:10 CST | G0 stage task 1 rerun (5k, 16 islands; timeout fixed to 417m) | gated (within the G0 approval) | 2747799_[1] | 14.0 (replaces task 1's reservation) | 9.67 | COMPLETED (4 h 50 min; 16/16 islands; HPM = truth; sd(log Z_r) 0.755) |

| 2026-11-15 21:28 CST | pmath bind check (WP1 PR #11 v4_pmath_check on SPR; 1 CPU, 15 min) | exploratory (standing authority) | 2747501 | 0.5 | 0.003 | FAILED (5 s; module load missing Lmod init; no compile) |
| 2026-11-15 21:40 CST | pmath bind check, rerun with the G0 module init | exploratory | 2747524 | 0.5 | 0.001 | FAILED (1 s; CMake 3.27.6 needs GCCcore 13.2; nothing compiled) |
| 2026-11-15 21:52 CST | pmath bind check, rerun 2 (GCC 14.3.0 + CMake 3.31.8) | exploratory | 2747598 | 0.5 | 0.001 | FAILED (2 s; pipefail on `g++ --version \| head`) |
| 2026-11-15 22:00 CST | pmath bind check, rerun 3 | exploratory | 2747666 | 0.5 | 0.04 | COMPLETED (75 s; 7/9 hashes equal; log1p, expm1 differ, unused by core) |

| 2026-11-16 00:2x CST | pmath check 2 (PR #15 5e3d5bf: + expl/logl rows) on SPR | exploratory | 2747875 | 0.5 | 0.05 | COMPLETED (83 s; expl/logl equal; all 8 guarded rows match) |
| 2026-11-16 00:3x CST | WP3 class-A island bench on SPR (820bd30; p = 10⁴ adaptive + geo:30 at 24/48/96 threads; p = 10⁵ at 48/96; 96 CPUs, 12 min) | exploratory | 2747881 | 19.2 | 19.5 | TIMEOUT at 12 min (p = 10⁴ runs complete; p = 10⁵ not reached) |

| 2026-11-15 23:3x CST | WP3 fixed-rounds island on SPR (cd1a7e02, PR #21): p = 10⁵, G = 256, transient + near-stationary islands at 24/48/96 threads; 96 CPUs, 20 min | exploratory (HQ sweep ≈ 40) | 2748104 | 32.0 | 10.3 | COMPLETED (6.5 min; MaxRSS 6.8 GB; hashes equal) |
| 2026-11-15 23:3x CST | WP3 fixed-rounds island on SPR (cd1a7e02, PR #21): p = 10⁶, G = 64, transient island (3 stages + 1 round) at 48 then 96 threads; 96 CPUs, 50 min | exploratory (HQ sweep + standing authority) | 2748105 | 80.0 | 67.1 | COMPLETED (42 min; MaxRSS 32.6 GB; hashes equal) |

| 2026-11-16 01:xx CST | WP3 10⁶ lever batch (efc0dfd0, pre-#24-fix, leaders unused): one exclusive SPR node, socket 0 G = 64 / socket 1 G = 256, block 4, parallel compaction; 192 CPUs, 35 min | exploratory (HQ GO ≤ 112) | 2748756 | 112.0 | 48.3 | COMPLETED (15.1 min; MaxRSS 58.7 GB both islands; G-invariance hash PASS) |
| 2026-11-16 08:xx CST | WP3 L5 measurement (be24e9d = exp/P1M-engine after #26): one exclusive SPR node, two G = 256 islands (ids 1, 2), k_store 8, socket-local; 192 CPUs, 30 min | exploratory (standing authority) | 2749328 | 96.0 | 42.7 | COMPLETED (13.3 min; island 1 hash = 2748756's; MaxRSS 70.4 GB both) |
| 2026-11-16 1x:xx CST | WP3 architect confirmation (39be5a08, prototype levers; measurement only): exclusive SPR node; socket 0 lever A/B + early bridge stages at 10⁶; socket 1 calibration-shaped island (leaders); 192 CPUs, 50 min | exploratory (standing authority; quoted to HQ ≈ 96 / worst 160) | 2749483 | 160.0 | 51.7 | COMPLETED (16.2 min; same-bits hashes identical; MaxRSS 80.2 GB both sockets) |
| 2026-11-16 16:49 CST | **W3-AUDIT track C (Theory, HQ-approved ≤ 150 core-h; NOT SMC, not in the P1M envelope)**: proxy computations, pkg 4f0f9a82, jobs 2754535–2754540 (6 arrays × 19 tasks, 1 CPU, 2G, commons) | Theory track C | quote 29.8 nominal / 66.5 ceiling | **actual 46.86 core-h** (114/114 COMPLETED, rc 0; 1.57× nominal, under the ceiling) |
| 2026-11-16 19:18 CST | WP6 K3 SPR bench (PR #51, 89366d4a): late 10⁶ rounds dense / K1 / K3 ×2 from one checkpoint, stand-in data; 96 CPUs (one socket), 72G, 60 min | exploratory (standing authority) | 2756524 | ≈ 50 (worst 96) | **21.2** | COMPLETED 13.2 min; one hash in all 6 variants; results/WP6_K3_SPR.md |
| 2026-11-17 00:40 CST | **T5 at 10⁵ (gate P4)**: 5-AR-n200-r01-V-s1 via the driver, code 04d8d2b5 (sapphirerapids + D-32 isa_check); setup 32 CPU → calibrate 64 → 16 islands × 48 → isa_check 48 → merge 16 → eval 8 | gate (HQ accepted worst ≤ 400; pre-announced) | 2758736–2758741 | ≈ 90 (worst 382; stop > ≈ 135) | **42.18** | ALL COMPLETED; P4 PASS (HPM = truth; D-32 pass); results/T5_1e5.md |
| 2026-11-17 06:53 CST | **P7: 10⁶ calibration pilot (H-11 gate (2))**: 6-AR-n200-r01-V-s1, production setup → pilot island (pilot_only), code 2cfaa9e5 (levers 1–3 + m3, floor, StartView); setup 48 CPU/48G + pilot 96 CPU/128G, 1 h each, SPR | gate (HQ standing approval; worst ≤ 144 accepted; pre-announce recorded in REQUESTS.md, HQ desktop unreachable) | 2761787–2761788 | 25–50 (worst 144; stop > 75) | **30.17** | COMPLETED (setup 19:01, pilot 9:21); results/P7_PILOT_1e6.md |
| 2026-11-17 07:33 CST | **1M PILOT FIT (P10)**: 6-AR-n200-r01-V-s1, batch F1M_pilot, code 2cfaa9e5; setup 48 → calibrate 96 → 16 islands × 96 (1 h) → merge 32 → eval 8 | HQ P9 GO 11-17 (worst 1,816 accepted as a limit; REQUESTS.md) | 2761931–2761935 | ≈ 450 (stop > ≈ 675) | **437.44** | ALL COMPLETED in 3:04; HPM = MPM = S₀; results/F1M_PILOT_FIT.md |
| 2026-11-17 10:54 CST | T6 at 10⁵: real-kill restart test (O4), one island of the T5 fit through `smcbvs4 island`, code 96137399; 1 task 48 CPUs 24G 50 min SPR | exploratory (standing authority; pre-announced REQUESTS.md) | 2763439 | 5–16 (worst 40) | pending | |
**Totals (2026-11-16 1x:xx):** actual ≈ 267.2 core-h closed (G0 kernel 0.88 + G0 stages 26.5 + pmath 0.10 + WP3 bench 19.5 + SPR sweep 77.4 + lever batch 48.3 + L5 batch 42.7 + architect batch 51.7) · open: none · remaining ≈ 28,030 of the re-sized envelope (H-9 ≈ 28.3k; manifest v0.4 plans 27,608).
**Envelope note (H-11 gate, 11-16):** planned A + D with contingency 27,608 (manifest v0.4); R1 brackets with the production π₀: ≈ 24.6–26.1k with levers 1–3 + m3, ≈ 22.3–23.4k with the offer floor (results/R1_RESIZE.md). No 1M stage on today's code (≈ 41–47k). Re-sized from the 10⁶ calibration pilot's MEASURED numbers.

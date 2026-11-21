# NOTS scratch hygiene proposal for the 1M block (report-only; ops, 2026-11-21; H-53 final step). DELETE NOTHING without the manager's OK.
Rules: H-41 / GC_PLAN §5 (class C = `island_*.bin` deleted after a VERIFIED merge V1-V5; A / A+ are collected and live on Owls + desktop; B = calib / data / raw / non-special setup, regenerable, never offloaded, the 14-day atime purge may take them). Inventory: one detached, nice'd, read-only `os.walk` on NOTS (`scratch/gc_inventory_1m.json`; the atime ages are < 1 day because the collection and the hash checks just read these files: **the 14-day purge clock restarted for everything we touched; it does not threaten the 1M files before ~12-05**). Desktop state from `crews/offload/desktop_verified.txt` (V5): **GC_P, GC_D, GC_W1 (3 units) and T2THR are verified; GC_W2 (3 units, collected 06:35Z) is pending the next hourly pull.**

| batch / run | total GB | islands (C) | fit.bin + law.bin (A) | setup.bin | calib.bin | data.bin | raw.bin | desktop-verified | oldest atime age (d) |
|---|---|---|---|---|---|---|---|---|---|
| GC_P / 6-AR-n200-r01-V-s1 | 60.1 | 36.0 | 2.71 | 10.14 (A+, on desktop) | 8.09 | 1.64 | 1.60 | yes | 0.61 |
| GC_D / 6-AR-n1000-r01-V-s1 | 71.8 | 35.3 | 2.65 | 9.22 (A+, on desktop) | 8.54 | 8.04 | 8.00 | yes | 0.46 |
| GC_W1 / 6-ADJOPP-n200-r01-V-s1 | 59.3 | 35.4 | 2.67 | 10.16 (A+, on desktop) | 7.82 | 1.64 | 1.60 | yes | 0.27 |
| GC_W1 / 6-AR-n200-r02-V-s1 | 59.6 | 35.6 | 2.68 | 10.15 | 7.92 | 1.64 | 1.60 | yes | 0.27 |
| GC_W2 / 6-AR-n200-r03-V-s1 | 59.5 | 35.5 | 2.67 | 10.14 | 7.95 | 1.64 | 1.60 | **pending (next hourly pull)** | 0.15 |
| GC_W2 / 6-AR-n200-r04-V-s1 | 59.3 | 35.3 | 2.66 | 10.15 | 7.95 | 1.64 | 1.60 | **pending (next hourly pull)** | 0.15 |
| GC_T2THR / 6-AR-n200-r01-V-s1 | 2.2 | 2.2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | yes | 0.29 |

**Total on NOTS scratch for the 1M block: 371.8 GB** (7 run dirs).

## What could go, in tiers (all behind V1-V5 + the manager's OK)
- **Tier 1a, islands of units already desktop-verified (class C): 144.5 GB** (GC_P 36.0 [the pilot's A++ exception: its islands and calib.bin are also on Owls + desktop; "kept until the block read-back": the manager decides whether the block read-back is done], GC_D 35.3, GC_W1 71.0, the T2THR re-run island 2.25 [its unit is verified and the island file is on Owls staging]). V1 (merge / eval COMPLETED, fit status completed), V2 (eval logZ_r length 16, finite) and V3 (no invalid / missing islands) are in the wave checks / read-backs; **V4 (each island's sidecar sha256 + size = what the fit's meta says the merge consumed) has been done by the plan workers for P and D only: it must still be run for W1 / W2 before any island is deleted.**
- **Tier 1b, A / A+ duplicates of verified units: 40.2 GB** (fit.bin + law.bin of P, D, W1: 10.7 GB; the A+ `setup.bin` of the pilot, option D and ADJ-OPP r01: 29.5 GB, all on the desktop).
- **After the next pull (GC_W2 verified): + 70.8 GB islands + 5.3 GB fit.bin / law.bin.**
- **Tier 2, class B (regenerable, not offloaded): 111.0 GB** (calib.bin 48.3 incl. the pilot's A++ 8.1, data.bin 16.3, raw.bin 16.0 [pure intermediate], setup.bin of AR r02 / r03 / r04 30.4). They can stay until the purge (~12-05), or go earlier to free scratch (re-running a plan regenerates them: setup ≈ 15 core-h + calibrate ≈ 24 per fit).
- **Proposed order if the manager approves:** (1) wait for the GC_W2 pull; (2) run V4 for W1 / W2 (one detached nice'd job, ~2.5 min per fit); (3) delete Tier 1a + 1b through `nots_wave_hygiene_check.py --apply-trash` extended with the islands allow-list fence (a NEW fence that GC_PLAN §5 says needs approval: the script today never deletes islands); (4) leave Tier 2 to the purge. Total reclaimable under the rules once everything is verified: **≈ 261 GB (Tier 1)**, + 111 GB (Tier 2) = 372 GB.
- Home is unaffected (6,105 MB; the 1M writes nothing to home).

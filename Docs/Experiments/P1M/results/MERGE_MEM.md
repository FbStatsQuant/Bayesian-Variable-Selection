# The first 1M merge: memory and time (WP4, 2026-11-18)

Question (manager, after `F1M_PILOT_FIT.md`): the merge task peaked at **75.1 GiB sacct MaxRSS** against a plan of **43.7 GiB**
(request 80G), the island stream took 834 s and `merge_tail_seconds` 1,215 s. Code: `exp/P1M-wp4-mergemem` (PR in the report).
No NOTS data was available on Owls (`scratch/runs/…` is on NOTS), so the components were measured with a **scaled probe**.

## Method (MEASURED on Owls, 3 cores)
`tests/test_merge_mem.cpp` writes the merge's inputs with the shapes of a 10⁶ run and runs the real `smcbvs4 merge`:
data.bin (n = 200), setup.bin (blocks of 14: logr 2¹⁴ codes per block; table stores at their caps 40p + 1 / 20p / 20p),
calib.bin (2c inherited models = 8.0·10⁷ at p = 10⁶, the pilot's `export`; the three calibration stores),
16 island_r.bin with **full** stores (c = 40p + 1 distinct models, mean |S| 7.0, the pilot's 7.25) above the offer floor.
Values are random: the probe measures memory and I/O time, not statistics (its local search is therefore slower than the real
8 s). The merge now records its phases (`meta.timings.phases`: seconds, RSS anon / file / total, VmHWM; the record adds
`peak_rss_kb`, `write_fit_seconds`). Probes at p = 2·10⁴ (R′ = 8), 5·10⁴ and 10⁵ (R′ = 16).

## Findings
1. **The process itself did not need 75 GiB.** Peak VmHWM, before any change: **36.8 KB per column** (p = 2·10⁴: 746 MB; 10⁵:
   3,682 MB; linear), i.e. **≈ 34 GiB at 10⁶**. The plan (43.7 GiB) bounded it. The rest of sacct's 75.1 GiB is **page cache**:
   the merge reads ≈ 59 GB of files (setup 10.1 + calib ≈ 9.8 + 16 islands ≈ 37 + data 1.6) and sacct's MaxRSS counts file pages
   until the cgroup reclaims them; a job at its limit reads ≈ 94% of the request (75.1 of 80 GiB) without needing it. Evidence on
   NOTS already in the record: P7's setup task, process peak 13.5 GB, sacct MaxRSS 23.7 GB, the difference 10.2 GB = setup.bin
   (10.14 GB). (INFERENCE for the merge; the new phase records settle it at the next fit.)
2. **Components of the peak** (measured at p = 10⁵ and scaled linearly to 10⁶):
   - `read_setup` copies setup.bin into the SetupView (logr 8 B × 874 M codes = 7.0 GB + three table stores ≈ 3.2 GB) while the file
     is mapped whole for the hash check: **≈ 2 × setup.bin** at the end of `read_setup` (the peak after the fixes: 25.8 KB/col).
   - `read_calib` materialised the **8·10⁷ inherited models** as `vector<InheritedModel>`: **146 B each, 11.7 GB, held for the whole
     merge**, plus the mapped calib.bin: the baseline's peak (36.8 KB/col).
   - the three table stores stayed in the SetupView after they were in the ledger (3.2 GB).
   - streaming: merged store 2.5 c entries (capacity kept) + one island (file mapped + loaded copy) ≈ 11 GB at 10⁶: not the peak.
3. **Fixes (no output bit changes; quick golden 540,419 checks, 0 failures; T9 merge comparisons included):** the inherited models are
   validated in place and offered from the mapped calib.bin (same offers, same order); the table stores are released after
   `offer_tables`. Peak at p = 10⁵: **3,682 → 2,578 MB (−30%)**, 25.8 KB per column, **≈ 24 GiB at 10⁶** (the setup-read phase).
4. **Plan.** `estimate_merge_memory` is now a plan by phase (resident = anonymous + mapped file pages; 1.15 × the largest phase
   + 80 MiB). It bounds the measured VmHWM by **×1.22 (p = 10⁵), ×1.25 (5·10⁴), ×1.83 (4,000, the 80 MiB floor)**; the default
   suite test fails below ×1.1. The load phases are admitted from the files' sizes before `read_setup` / `read_calib` allocate.

## 10⁶ projection (formula with the pilot's sizes: setup.bin 10.14 GB, S_all 10.4 GB, S_kept 7.1 GB, calib.bin ≈ 9.8 GB (probe
ratio), islands ≈ 2.3 GB each, c = 4·10⁷ + 1, k = 7.3, R′ = 16, 32 threads)
| phase | resident |
|---|---|
| load_setup (copy + file mapped + data) | 22.1 GB |
| load_calib | 21.8 GB |
| offers (table stores into the ledger; inherited from the mapped file) | 24.4 GB |
| streaming (kept setup + merged store + one island) | 20.2 GB |
| tail | 14.9 GB |
| **plan total** (1.15 × 24.4 + 80 MiB) | **28.2 GB = 26.2 GiB** (old formula, same sizes: 39.1 GB; the pilot printed 43.7 GiB) |
| `sacct_upper` (+ every file read or written) | 88.7 GB = 82.6 GiB (the pilot's 75.1 was reclaim-capped) |

**Request for a 10⁶ merge: 48G** (process 26.2 GiB + ≈ 22 GiB headroom so the page cache is reclaimed lazily); **32G** is the
functional minimum (the 90% `--mem-budget` = 28.8 GiB ≥ the 26.2 GiB plan). sacct's MaxRSS will keep reading ≈ the request
because of the cache; use `peak_rss_kb` in the merge record (VmHWM) for the process.

## The "20-minute tail" (report only)
`merge_tail_seconds` (1,215 s) is **the whole command up to the write** (data load, `read_setup`, `read_calib`, pass 1 over the 16
island heads, the table and inherited offers, the island stream, local search, LS0, assembly), not the tail. Local search +
LS0 = 7.8 s. By the probe's per-file costs (hash 221 MB in 1.21 s on Owls; the bundled software SHA-256, ≈ 180 MB/s):
- ≈ 94 GB are hashed per merge: setup 10.1 + calib 9.8 + islands **twice** (pass 1 heads, pass 2 loads) 2 × 37 + data 1.6;
  at 250–300 MB/s (NOTS) ≈ 5.5–6.5 min of the 31.7;
- the 6.4·10⁸ island offers into the merged store ≈ 10 min (the island stream, 834 s, includes the second hash ≈ 2.5 min);
- load + offers ≈ 1.5 min; local search + LS0 8 s.
- ≈ 690 s of the 1,902 s job elapsed are **after** `merge_tail_seconds` (write_fit + exit). At p = 10⁵ `write_fit` is 3.7 s, so the
  write alone does not explain it; the exit freed the 8·10⁷-model heap (now gone). The new `write_fit_seconds` records it.
Cheap cuts (not done): (1) verify each island once (pass 2 `Reader(path, verify = false)` when pass 1 proved the file and the
header hash is unchanged): −2.5 min; (2) hash sections in parallel (`Reader::verify_all` over 32 idle threads, ≥ 4× on the
island files): −5 min; (3) SHA-NI on the Sapphire Rapids nodes. A mapped (not copied) `SetupView::logr` would remove
the 7 GB copy and the 2× peak of the load phase (peak ≈ 14 GB): a refactor of `SetupView`, not cheap.

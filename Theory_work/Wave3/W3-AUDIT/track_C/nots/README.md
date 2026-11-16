# W3-AUDIT track C — NOTS package (for Engineering)

Theory Department, W3-AUDIT track C (internal design-proxy check; **proxy computations only, no SMC fits**).
Built from branch `theory/W3-AUDIT`, folder `Theory_work/Wave3/W3-AUDIT/track_C/`. Engineering runs it; Theory writes
all analysis code. Questions: Theory Dept manager.

## What it computes
For each of 19 Gaussian-row designs (D01–D19) and 6 large cells (n, p), 10 replicates of X: proxies P1–P10 of the
design assumptions (sparse eigenvalue floors, visibility, leakage set size, local regressions, Occam term, operator
norm). One array task = one (design, n, p) with its 10 replicates. Python 3 + numpy + scipy only; 1 CPU; no network.

## What to run (on NOTS)
1. Copy the package (built on Owls by `make_pkg.sh`, read-only, with `MANIFEST.sha256` and `COMMIT`) to
   `/home/fb31/SMC_Theory_Department/W3-AUDIT-C/pkg` and check it: `cd pkg && sha256sum -c MANIFEST.sha256`.
2. Optional smoke test (≈ 10 s; any node with the modules): `source pkg/env_c.sh; C_LDIR=pkg/data python3 pkg/scripts/c_test.py`
   → last line `SUMMARY: ALL PASS`.
3. Submit: `bash pkg/submit.sh /home/fb31/SMC_Theory_Department/W3-AUDIT-C/pkg 60`
   (6 array jobs × 19 tasks = 114 tasks; throttle 60 concurrent; account/partition/qos `commons`; `--export=NONE`;
   modules `GCC/14.3.0 SciPy-bundle/2025.07`, see `env_c.sh`).

| class | n | p | tasks | time limit | mem |
|---|---|---|---|---|---|
| c200_20000 | 200 | 20000 | 19 | 00:30:00 | 2G |
| c400_4000 | 400 | 4000 | 19 | 00:10:00 | 2G |
| c400_20000 | 400 | 20000 | 19 | 00:30:00 | 2G |
| c800_8000 | 800 | 8000 | 19 | 00:10:00 | 2G |
| c800_20000 | 800 | 20000 | 19 | 01:10:00 | 2G |
| c1600_16000 | 1600 | 16000 | 19 | 01:00:00 | 2G |

## Where outputs go
`/scratch/fb31/SMC_Theory_Department/W3-AUDIT-C/`
- `out/D<did>_n<n>_p<p>.csv` — one small CSV per task (≈ 50 KB; 114 files, < 10 MB total). **These are the results**:
  please copy `out/` and `log/` to Owls `/home/fb31/SMC_Theory_Department/helpers/W3-AUDIT-C/nots_out/` (rsync -a,
  with `sha256sum` check) when the run ends.
- `log/ends.jsonl` (one line per task: rc, wall seconds, host), `log/<class>_<task>.log`, `log/submitted.txt`,
  `log/pkg_sha256.txt`; `slurm/` (stdout/stderr).
A task writes its CSV atomically (tmp + rename) at the end, so a missing CSV = a failed or killed task; rerun just that
task id (`sbatch --array=<id> ...` with the same class line).

## Cost (measured basis)
Owls pilot 2026-11-16 (`nice 19`, 1 thread/process, 12–9 concurrent processes on a node at load ≈ 26/80), one replicate
per cell, designs D01 (IND), D05 (block), D14 (strong factor), D18 (riboflavin-like); max over the measured designs,
seconds per replicate: c200_20000 84, c400_4000 5, c400_20000 83, c800_8000 24, c800_20000 199, c1600_16000 166
(strong-factor / real-data-like designs cost ≈ 2× IND in the p = 2·10⁴ and n = 1600 cells). Task estimate = 10 × that +
6 s population layer; the max is applied to all 19 designs (conservative).
- **Nominal: 29.8 core-h** (114 tasks).
- **Ceiling at the time limits (2× measured, rounded up to 5 min, floor 10 min): 66.5 core-h.** Peak RSS 0.7 GB.
- Budget (BRIEF track C): ≤ 150 core-h on NOTS; this run leaves ≥ 83 core-h for a rerun round.
Wall time ≈ 1.2 h at 60 concurrent tasks.

# ADDENDUM_2_VF: carry-over check of the 14 re-run overlap V fits (I_max = 0) against the existing overlap T fits

**Status: COMMITTED by the Engineering manager 2026-11-19, before S1 (draft by the Sonnet FZ worker; FZ_CHECK_OPUS F4; HQ OK 5a44e163 / H-30).** Descriptive only: no new pass/fail, no change to any registered script, threshold or table. No new compute: the T fits and the VF fits already exist or are in the science plan.

## Why
The overlap verdict (H-25, CLEAN under v2) validated V at **I_max = 3**. The freeze adopts **I_max = 0** (FZ_READBACK §1). The evidence for I_max = 0 so far covers 3 datasets at R′ = 64 (M1–M3 non-inferiority; I_max offset contrast −0.00089 [−0.0040, +0.0022]; HPM identical). Without this step the campaign's validated configuration would change silently from the one the overlap verdict checked.

## What
The 14 `VF` fits (the overlap's V fits re-run at I_max = 0; same data and engine seeds, R′ = 16, N 2,500, m 1, leg build `d0c30b65…`): AR r01–r04 × s1, s2 (8), AR-weak r01, r02 × s1 (2), ADJ-OPP r01, r02 × s1 (2), IND r01 × s1 (1), NULL r01 × s1 (1) = 14 pairs on all 10 overlap datasets. Each is scored against the **existing overlap T fit of the same dataset and seed** (`records/overlap1e4/`), with the **overlap's v2 criteria** (OVERLAP_1e4_VERDICT §2: PAIR, S1 HPM equal, S2 T never higher F, S3 MPM equal, S4 NULL, P PIP, E1 log Ẑ within 3 s.e., E2 lower bound, H Hellinger ≤ 10 %, C cost; the overlap's V(I_max = 3) values were: HPM equal 10/10, worst PIP ratio 0.038, worst log Ẑ 1.76 s.e., max Hellinger 0.0136), and the overlap's own V(I_max = 3) result beside it for the same pairs.

## How
- **Scorer:** `results/overlap1e4/compare_overlap_v2.py`, sha256 `4f402e5127efd4754cf25e4ade6ad799f697ebc28e1c657ff49f93fd2905b5c6`, unchanged, in `--wave-check` mode (per-(dataset, seed) V-vs-T pair table, island-only s.e., no verdict; the mode used for B1), `--cross-file` for d_H(V, T) as in the overlap. The VF fits carry the tag `VF` in their run ids (`4-<d>-n200-rNN-VF-sN`), so the manager or the read-back worker supplies them to the script under the overlap's V name (a thin wrapper, its sha256 recorded here at the S1 / S2 read-back **before** the output is read). If the wrapper needs any change after the first output is seen, it is a logged deviation.
- **When:** at the read-back of the wave that holds the VF fits (S1 / S2 of the I_max = 0 plan; the 12 + 2 VF fits).
- **Reported:** the pair table and, per criterion, the I_max = 3 result and the I_max = 0 result for the same pair; the dataset-level V − T log Ẑ for the VF fits as one more row of the offset surface (`src` = `vf`, 10 datasets), computed with `precision_offset.py` unchanged only if its run-id pattern accepts `VF`, else by hand from the pair table. 6 of the 20 overlap V fits have no VF twin (second seeds of AR-weak r01–r02, ADJ-OPP r01–r02, IND, NULL): they stay as the I_max = 3 record.

## Reading (declared now)
- Every criterion V(I_max 3) passed and VF also passes: carry-over confirmed on these 14 pairs; recorded.
- **A v2 criterion that V(I_max 3) passed and a VF fit fails: report to HQ at once (report-and-continue; the science waves are not stopped by this addendum).**
- A criterion already failed or NOT EVALUATED at I_max = 3 stays as it was; no new reading is made of it.
- Single-seed pairs cannot support seed-to-seed statements; they are listed as single pairs. No statement of the form "I_max = 0 is validated" is made beyond these 14 pairs, p = 10⁴, n = 200.

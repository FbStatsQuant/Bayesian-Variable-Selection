CLEAN: V0 canary read-back, all MINILEG_PLAN §5.4 rows pass (XB2 bit-identical, 2/2 pairings identical, f inside 3.2–4.6, no re-quote)

# V0 canary read-back (V-N mini-leg; Engineering ops, 2026-11-20 00:3xZ)
Wave V0 (VN_V0_1/2/3), F2 binary BUILD_F2 `da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a` (git e993ece2…). Collected by `vn_collect_wave.sh V0` into `records/vn_minileg/V0/` (**8 units verified, 0 problems**; one `SHA256SUMS` per unit, none nested; 5 fit units + 3 `_batch_` units). Per-fit table machine-readable: `readback_V0.json` (tool `ops_tools/vn_readback.py`). `calib_meta.json` present for all 5 fits. Nothing was freed on NOTS.

| fit | class | billed core-h | soft / hard | states | arm recorded = plan | data X/y = leg | build | R′ / logZ_r |
|---|---|---|---|---|---|---|---|---|
| AR N 10⁴ I_max 0 c1 | vn N10⁴ m1 I0 | **20.58** | 28.6 / 47.6 | COMPLETED | N 10⁴, m 1, I_max 0, I_used 0, bounded ✓ | ✓ | BUILD_F2 ✓ | 64 / 64 |
| AR N 10⁴ I_max 3 c1 | vn N10⁴ m1 I3 | **20.75** | 31.0 / 51.7 | COMPLETED | N 10⁴, m 1, I_max 3, I_used 3, bounded ✓ | ✓ | ✓ | 64 / 64 |
| XB2 (N 2,500, I_max 0) | XB2 | **6.29** | 8.6 / 14.3 | COMPLETED | N 2,500, m 1, I_max 0, I_used 0 ✓ | ✓ | ✓ | 64 / 64 |
| r04 VI3-s1 (R′ 16) | r04 pair | **2.69** | 3.0 / 5.0 | COMPLETED | N 2,500, m 1, I_max 3, I_used 3 ✓ | ✓ | ✓ | 16 / 16 |
| r04 V-s2 (R′ 16) | r04 pair | **1.76** | 3.0 / 5.0 | COMPLETED | N 2,500, m 1, I_max 0, I_used 0 ✓ | ✓ | ✓ | 16 / 16 |
Wave **52.07 core-h** (sacct CPUTimeRAW/3600) vs quote 50 (stop > 100): 1.04×; 0 soft trips, 0 hard. Class means vs the committed model E: I0 20.58 / 19.06 = 1.08×, I3 20.75 / 20.68 = 1.00×, XB2 6.29 / 5.71 = 1.10×, r04 2.22 / 1.99 = 1.11× (G-B cost criterion: mean ≤ 1.5×, no fit > 2.5×: met). `prior_after_V0.json` = 5 fits, 52.07 core-h (mini-leg ledger only; the leg's 462.48 is not in it).

## §5.4 checklist
1. **5/5 delivered, all stages COMPLETED:** PASS (`INCOMPLETE.txt` absent; every cost record states COMPLETED; sha256sum -c OK).
2. **Arm = plan, `I_used` 0 for I_max 0:** PASS on 5/5 (N 10⁴ for the two N 10⁴ fits, 2,500 for XB2 and the r04 pair; `refine_m` 1; rule bounded). I_max 3 fits: `cost_diag_*` files 12, largest index k = 3 = `I_used`; I_max 0 fits: 0 diag files.
3. **PAIRING with the N 2,500 twin (calib_meta.json sections except meta): PASS 2/2.** AR N 10⁴ I_max 0 vs leg `A0/4-AR-n200-r01-P-N2500-m1-I0-c1-s1`: 40 sections, **0 differing**, `grid` and `grid_unrefined` equal; AR N 10⁴ I_max 3 vs `P1/4-AR-n200-r01-P-N2500-m1-c1-s1`: 40 sections, 0 differing, grids equal. The only `meta` field that differs is `N` (10,000 vs 2,500). So N is the only thing the contrast changes. (Every V0 calibration has `grid_unconverged: true` and the "preliminary" grid label, identical to the twins: the sections are equal, so the same flag is in the leg.)
4. **XB2 bit check (F2 vs the leg's F record `A0/4-AR-n200-r01-P-N2500-m1-I0-c1-s1`): PASS, 0 scientific differences.** `xb_check_vn.py --R 64` (`xb_check_XB2_output.txt`): (1) 64/64 `evidence.logZ_r` bit-equal; (2) `selection.hpm` equal [1000, 3000, 5000, 7000, 9000]; (3) 64/64 island `output_hash` equal; (4) 72 sidecars compared (fit, eval, calib, setup, data, truth, 64 islands), 6,251 provenance keys dropped, **0 differing fields**; (5) `fit.bin` 44 sections and `eval.bin` 4 sections equal through `smcbvs4 info` (Owls F+xeval build b9dc443e…, reads files only). **F2 = F at R′ 64: the pooled baseline is valid.** (`xb_check.py` was copied to `xb_check_vn.py` with the island count as an argument, `--R`; the checks are the same.)
5. **f measured (N 10⁴ islands / twin's N 2,500 islands):** I_max 0: wall 313 / 94 s = **3.33**, billed 20.03 / 5.19 = **3.86**; I_max 3: wall 325 / 90 s = **3.61**, billed 19.48 / 4.84 = **4.02**. Mean wall f 3.47, mean billed f 3.94 (plan 3.85). Both inside 3.2–4.6 → **no re-quote** of V1 / V2 on this row (the manager may still choose to refresh the soft lines).
6. **Merge at R′ 64, N 10⁴:** wall 157 s (I0) / 142 s (I3), max RSS 1.93 GB / 1.71 GB (request 16 G), billed 0.35 / 0.32 core-h; XB2 merge 157 s, 1.69 GB. Eval 17–23 s.
7. **Cost ≤ the wave stop and each fit ≤ its soft stop:** PASS (52.07 ≤ 100; largest fit 20.75 vs soft 28.6 / 31.0).
8. **X/y sha256 equal to the leg's; one binary sha:** PASS. `truth.json` X/y equal `vn_refs.json` for all 5 fits; all 264 sidecars carrying a `binary` block, the three `_batch_*/bin_version.json` and every calib_meta say sha256 `da0cf85b5fe0…`, git `e993ece2`.
9. **`fit.bin` readable, `evidence.logZ_r` length 64, `fit.meta.occ` present:** PASS (`smcbvs4 info fit.bin --meta 1` rc 0 on 5/5, 45 sections, header+table+meta verified; `occ`, `occ_alpha`, `occ_total`, `occ_total_r(_all)` present; length 64 on the R′ 64 fits, 16 on the r04 pair).

## Notes (facts, no interpretation)
- Stage timings of the N 10⁴ fits: calibrate 24 s (I0; N-independent, as in the twin) and 192 s (I3, I_max 3 refinement), islands 313–325 s wall (twin 90–94 s), billed islands = 97% of the fit's core-h.
- The monitor's probe had one transient ssh failure at 23:52Z (probe file truncated); fixed the same hour (`OPS_VN.md`), no effect on the records.
- Offload to the desktop is not done (not asked); the units are at `records/vn_minileg/V0/` on Owls (depth 3 under records/, serve_pull layout).
- **V1 waits for the manager's GO.** For the V1 monitor: `PRIOR=/home/fb31/SMC_Engineering_Department/staging/vn_minileg/prior_after_V0.json` (a copy is next to this file).

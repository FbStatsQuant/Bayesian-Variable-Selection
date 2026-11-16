# certfreq_search: how often `fit$local_certified = TRUE` with a small HPM (read-only search, 2026-11-16)
Counts of rows/records only; no new fits. "small" = |HPM| <= 2*s0. Files marked [NOTS] are under /home/fb31/SMC_Theory_Department/records.

## A. 2,400-fit production study (n=200, p in {500,1000}, c in {1,0.5}, S1-S6, 100 reps, s0=14, v2.2.1 core d880afdb)
Scenarios (Docs/Records/STATUS_BRIEFING_20261028/BRIEFING.md:52-57): S1 indep; S2 AR(1) .5; S3 blocks-of-5 .7; S4 blocks .85;
S5 .7 within blocks + .3 between ALL blocks; S6 block rho .4..0.9. NO one-factor/equicorrelated-strong design; S5 is closest.
- Certification field: Results/SMC_BVS_v3_production/p{0500,1000}/smc_flag_rates.csv, col `n_local_certified_false` (count of FALSE only; no TRUE column).
  FALSE total = 6/2400 (p500 c100 S5: 1; p1000 c100 S5: 3; p1000 c050 S5: 2; the p500 c050 cell: 0). All 6 are `resource_limit` stops
  (Scripts/Campaigns/2026-10-28_New_Campaign/ops/PRODH_COMPLETION_20261102.md:15-26; all S5; HPM path, no Z/PIP).
- TRUE count: not tabulated per fit in any CSV. Statement "in all 2,394 completed fits ... local_certified = TRUE, local_limit = FALSE, 0 LS moves":
  Theory_work/Old_Projects/New_BVS_Headquarters/03_results_and_conclusions.md:168; "0 moves in 2,394 fits": Results/2026-10-28_New_Campaign/H2_20261102/HEADLINE_H.md:94.
  Cross-check of n: tables/ev_local_search.csv (centre rows sum 600+599+598+597 = 2,394).
  So certified = 2,394/2,394 completed (99.75% of 2,400).
- Per-fit HPM size: NO file has the size distribution. Only means: size = tp_mean+fp_mean from
  Results/SMC_BVS_v3_production/p*/exact_recovery_long.csv (rows method SMCBVS, rule hpm; also err_exact/err_extra_only/err_missed_only/err_mixed counts).
  Mean |HPM|: c100 p500 14.065, c100 p1000 14.06, c050 p500 13.995, c050 p1000 13.893.
- Size bound derived from counts (each extra-only/mixed fit has >=1 FP, so max FP <= FPsum-(#FP-fits-1)):
  c100: max |HPM| <= 18 (p500), <= 17 (p1000): all 1,196 completed c100 fits have |HPM| <= 28.
  c050: per-cell max FP bound S1 4, S2 2, S3 1, S5 3, S6 9 (p500); S1 3, S2 3, S3 6, S5 9, S6 3 (p1000) => |HPM| <= 23. S4 cells: bound 40 (both p),
  NOT excluded above 28 (FP sums 109 / 101, mean size 14.03 / 13.96). So |HPM| <= 28 is certain for 2,194/2,394 fits; unknown for the 200 c050-S4 fits.
- Contains S0 (exact + extra_only): c100 p500 595/599, c100 p1000 594/597, c050 p500 420/600, c050 p1000 387/598 => 1,996/2,394 overall.
  Equals S0 (err_exact): 559, 560, 370, 340 => 1,829/2,394 (matches H2 ev_local_search.csv `centre = S0`).
  Among the 2,194 fits with |HPM| <= 28 guaranteed: contain S0 1,928; equal S0 1,769.
  S5 (nearest strong-correlation), fits containing S0: c100 p500 99/99 completed, c100 p1000 97/97;
  c050 p500 65/100, c050 p1000 41/98 (missed_only+mixed = 35, 57; 2 resource_limit not counted).
  Misses are real: 565 of 2,394 are "posterior misses" (F(S0) < F(HPM) strictly; H2 ev_miss_class.csv; 03_results:160-168), every one certified TRUE.
- Same numbers, other copies: Results/2026-10-28_New_Campaign/H_existing_20261030/tables/smc_diag_flag_rates.csv (identical columns), RESULTS_TABLES.md:272-279
  ("local_certified_false" 0/1, 0/3, 0/2 exact-recovery rows).
- Semantics: this core's `local_certified` = FINAL search only; the later core (main 2252d57) also includes LS0 (Theory_work/Pause_2026-11/RERUN_SPEC.md:77,195).

## B. W3-P6 strong-factor experiment (main 2252d57 code; iid rows; n=50..150; s0=4 or 8; sigma=1; aligned signs) [NOTS] theory_w3/*/raw/fits.jsonl
Fields present per fit: `local_certified`, `local_certified_by` (both/final), `hpm`, `hpm_size`, `hpm_eq_S0`, `final_ls_limit`, `ls0_local_limit`, `status`.
(Theory_work/Wave3/W3-P6/reviews/R02_inputs/*_derived.jsonl has hpm but NOT local_certified. The b1 raw file has 295 lines, 4 unparseable; 291 used.)
Runs parsed: b1 291, s1_b1r 21, probe01 10, s1_b_hw 9, s1_c_hw 9, s1_g1/g2/h1/h2 5 each, s1_d2 4, smk1_v3 4, s1_d1 3, s1_d1hw 2, smoke_v3 2, smk1_v2 1 = 376 fits
(335 arm wide + 41 arm mr1; all status `completed`). Designs: cs(rho)=x=sqrt(rho)f+sqrt(1-rho)e; fac2 (two factors); s5 (blocks) per Theory_work/Wave3/W3-P6/DESIGN.md:11-14.
- ALL 376: certified TRUE 376 (by "both" 346, by "final" 30); |HPM| <= 2*s0: 376; max |HPM| = 8 (s0=8); contain S0: 275 (equal S0 273; 2 supersets, |HPM|=5, p=n=50).
- p > n (p/n >= 2): 234 fits: certified 234, |HPM| <= 2*s0 234 (max |HPM|/s0 = 1.0), contain S0 165 (all equal S0).
- p >= 5n: 162 fits, certified 162, small 162, contain S0 97.  cs rho>=.5, p>=2n: 172 fits, 172 certified+small, 109 contain S0 (63 certified-small HPMs MISS a truth).
Per cell (design, n, p, s0): fits / certified / contain S0:
 cs.3 n50 p250 s4: 20/20/18; cs.5 n50 p125 s4: 40/40/36; cs.5 n50 p250 s4: 21/21/10; cs.5 n50 p250 s8: 20/20/0 (max |HPM| 7);
 cs.5 n50 p500 s4: 21/21/11; cs.7 n50 p250 s4: 20/20/4; cs.5 n75 p188 s4: 10/10/10; cs.5 n75 p750 s4: 10/10/8; cs.5 n100 p250 s4: 10/10/10;
 cs.5 n100 p250 s8: 5/5/5; cs.5 n100 p1000 s4: 10/10/10; cs.7 n100 p250 s4: 5/5/5; fac2 n50 p250 s4: 20/20/16; s5 n50 p250 s4: 20/20/20; s5 n100 p250 s4: 1/1/1.
 (p<=n cells, for reference: cs.5 n50 p50 s4 40/40/38; cs.5 n50 p50 s8 20/20/2; cs.3 n50 p50 19/19/19; cs.7 n50 p50 19/19/11.)
- Reading: on strong-factor p>>n designs the method's final search ALWAYS certifies and ALWAYS returns |HPM| <= s0 (here <= 8), yet S0 is missed in 10-100% of
  the n=50 cs fits at p>=125 (cs.5 p250 s8: 0/20 contain S0). So certified+small does NOT imply S0 contained; at n>=75, p>=188 it did in 49/51.

## C. W2-FAC / W2 NOTS records (theory_w2) -- fit-level `local_certified` exists only in 8 loc_pilot01-02, prod_diag02, x_Cpilot_a/b, x_Q5pilot01 raw files
- 16 records: TRUE 8, FALSE 8. All TRUE are `completed` with p<n (loc_pilot01 C1 n500 p125, C2 n2000 p500, C3 n2000 p495, C4 n500 p115; loc_pilot02 n8000 p2000;
  x_Q5pilot01 n500 p100, n500 p250, n2000 p100), |HPM| 3-4, `hpm_eq_S0` TRUE in all 8. All 8 FALSE are `resource_limit` (prod_diag02 x5: n200 p90-500;
  x_Cpilot_a n20000 p2000; x_Cpilot_b n50000 p5000; x_Q5pilot01 n2000 p1000); none has p > n. s0 not stored in these records.
- pk_r1_01 (540), pk_r3_01 (280), pk_s5ex_01 (180), pk_s5iid_01 (280): key `certified` (NOT fit$local_certified) in LS0 Gram-reduced component runs
  (s0=4, p/n 0.6-10): certified TRUE in 1,280/1,280; final = S0 in 537, 238, 178, 261; |final| <= 2*s0 in 540, 246, 180, 268. p>n only in pk_r3/pk_s5iid. Not the full method.
- Theory_work/Wave2/W2-APP/numerics/agg_tables.md:119-231, LEAD_READING.md:20-34: Python LS0 port (not production); `ls_certified` and S0 endpoint in
  n2 96/96, n3 V1/V2/V3a 40/40 (24 complete-scan certified + 16 screened, whose flag is not a complete-scan certificate). Component only.
- No other W2-FAC dir (W2-FAC-A/B/K2/PK/PKA/S5/S5F/X/XA) holds fit-level local_certified rates: git grep finds no hits in their md/csv text.

## D. Other
- git grep local_certified on origin/main & origin/theory/W3-P6 (non-core): only code/spec/theory docs plus the sources in A. No further rate tables.
  Theory_work/Wave1/W1-PXN/numerics/SUMMARY.md:100: one small enumeration where S0 is not the certified end (ends certified at (0,1,2,4,7)); no rate.
- Sources with NO certification field: production exact_recovery_long.csv/smc_recovery_*.csv (only the FALSE code), W3-P6 R02_inputs derived.jsonl, W2-FAC pk_*/s5_*/x_A1/x_pilot*
  (theory-side tables), Results/p500_comparison, Results/Benchmarks_n200.

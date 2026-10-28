# REPORT_B — engine_v2bb (BB(a,b) composite-start SMC), executor B (Opus), 2026-10-13
(Saved by the lead from the agent's final message; the agent's tool could not write this file.)

**Status: all gates G0–G5 PASS.** G4 needed one fix of the test statistic, not the engine (see G4).

## Files (local `phase2/B_bb_engine/`, mirrored on Owls `E/dev/B/`); code tar sha256 (launcher method) a26d3f344b9fb19b4af80ad02e3888b5298b3cff8c7c14042e99693eea37b93d
| file | sha256 |
|---|---|
| code/scripts/engine_v2bb/01_configuration_and_data.R | 034966d1b3b1daa5ab325b844125bbadf6b9e7d59db6de46af6156c502123152 |
| …/02_model_and_exact_reference.R | 29d9dec756df44c2465b43fff31c0317b30c0d0555e0786f8e4eba5f48eb23aa |
| …/03_composite_likelihood.R | 5206d95d79552b039804f76200816db5c8b0ff7ffee287892fb97348c512029b |
| …/04_smc.R | 975d5e0443bf2218fa4d34fb7cc2f7d679b7dd984cfadbd28feb518f57b22b59 |
| …/exact_reference.cpp (unchanged) | 263dde27…c5f |
| …/SHA256SUMS (new) | c038ad10e2623c420e561163f5ff97295aff60806b38bcff2847d0a28740f075 |
| code/scripts/campaign/00_bootstrap.R (folder name only) | a087eeec9900119b858f0d785c87bd9ec9e92dcf65dcceb7df5b80c828aa2a54 |
| 01_design.R, 02_evaluate.R | byte-identical to FD1 |
| code/precheck_case.R | 464c328a4378f810ad9168173aeac24d7ef3324e689f97ce1619b2b497798b38 |
| code/run_precheck_bb.R | 7ddcb6d086309caec70012396f594539f22511e81a6dc552212c648ba38f89b8 |
| code/launch_precheck_bb.sh | 3c743b5b56eb1aaf7c345ac3ed4fbef275c25dd4f4ed512d73585746bbfe0906 |
gates/ (g0–g5, g4_diag.R, gate_common.R; gates/ref/exact_stratified.R unmodified 40bed713…e24; gates/results/ logs+CSVs);
jobspec/cases_pilot.txt (25 ids, a25a1b61…), jobspec/cases_full.txt (1,200 ids, 1d1ffda5…; all data files exist on Owls).

## Diff vs engine_v2 (each prior-dependent change commented with its equation)
- 01: validates optional `model_prior` (default "bernoulli"; "betabinomial" needs prior_a, prior_b).
- 02: new `log_model_prior_cfg()`: Bernoulli → `log_model_prior` (same arguments); BB → lbeta(a+|S|, b+p−|S|) − lbeta(a,b).
- 03: BB: block tables hold m̃_b only (no prior) + size profiles c_k^(b); `log_convolve`, `bb_composite_start` (partial
  convolutions F_b, c_k, w_k = c_k B(a+k,b+p−k)/B(a,b), log Z_0 = LSE(w_k), π_0(k)). Bernoulli branch is the v2 code.
- 04: `draw_bb_start()` (k, then block sizes by backward DP, then T_b ∝ m̃_b); `gibbs_sweep` under BB uses prior log-odds
  log((a+k)/(b+p−k−1)), k = |S_−j| per particle (RB PIPs use the same conditional); optional `trace` argument (validation only,
  does not change draws); `visited_summary` weights use the run's prior; BB results carry engine = "v2bb" and `prior`.
  Incremental weights unchanged.
- Runner: `precheck_case.R` shared by runner and gates; vs run_s6_visited.R: S/W ids, seed_data read from the sealed object and
  checked against the manifest, prior as argument, SMC seed offset s, extra fields `prior` (both modes), `seed_offset_index`.
  Usage: `run_precheck_bb.R <case_list|id> <data_dir> <out_dir> bernoulli 0.2 [s]` or `... betabinomial 1 30 [s]`;
  seed_smc = data + 200000 + 50000·s; s > 0 → `<id>__seed<s>__precheck.rds`.

## Gates (Owls, R 4.6.0, `Rscript gates/<g>.R` from E/dev/B)
- **G1 regression:** Bernoulli mode S6 r001, r002 vs existing v2 objects: identical() TRUE for log_Z, log_Z_hybrid, pip_rb,
  pip_hybrid_mean, model_codes, and all 31 common fields except seconds/versions. Extended: S6 r001–r010 through the launcher
  identical on all 31 fields (10/10).
- **G0 (m := m̃):** BB(1,30), S6_r001 and S4_r001: 1 stage, log Ẑ − log Z_0 = 0 exactly; polish |S| vs exact π_0(k) p = .42, .93;
  RB PIP MAE vs exact π_0 PIPs 4.8e-4, 8.9e-4.
- **Empty model** (p = 30, S6_r001 X, noise y): π_0(∅) = .7941, 2e5 draws .7942 (z = 0.13); ∅ in V with finite score; 79 % of final particles ∅.
- **G2 start** (2e5 draws, seed = seed_smc; exact distributions from an independent enumeration of block-size vectors with
  linear-scale profiles, not the engine DP; engine π_0(k) vs enumeration ≤ 8e-14): all 24 p-values > .01.
  | id | (i) | (ii) two most frequent k | (iii) |
  |---|---|---|---|
  | S6 r1 | .81 | .94, .88 | .064 |
  | S6 r2 | .80 | .14, .14 | .073 |
  | S6 r3 | .58 | .87, .073 | .18 |
  | S6 r4 | .97 | .053, .63 | .63 |
  | S6 r5 | .56 | .28, .89 | .11 |
  | S4 r1 | .94 | .97, .11 | .39 |
- **G3 Z_0:** Beta-mixture integral (Gauss–Legendre 64 and 256 nodes, integrate(); 64 nodes exact for the degree-59 integrand):
  relative diff vs convolution Z_0 ≤ 2.3e-13 on 6 datasets; Bernoulli-mode log_Z0 identical() to v2 on all 6; Bernoulli Z_0 rebuilt from c_k within 2e-13.
- **G4 Gibbs** (p = 10: S6_r001 columns 1–10, blocks 5+5; real and noise y; BB(1,10), BB(2.5,7)): engine conditional = brute-force
  q_φ ratio for every state × coordinate × φ ∈ {0, .37, 1} (max err 4.6e-14); start draws vs exact π_0(S) over 1,024 models p = .31–.86;
  Z_0 vs brute force ≤ 6e-14; long Gibbs (2,000 chains × 400 sweeps) max |z| 1.65, max |err| 4.2e-5; full SMC hybrid log err ≤ 6.6e-5.
  First run FAILED (|z| = 23): x4 has exact PIP 1 − O(1e-15), SE ~1e-16, error 9e-15 of rounding; all other coordinates |z| ≤ 1.3
  (g4_diag.log). SE floored at 1e-12; failing log kept as g4_gibbs_run1_FAIL.log.
- **G5 end-to-end** (S6 r1–10 + S1 r1–10, production seeds, exact from E/out/enum_strat):
  | | BB(1,30) | Bern(0.2) |
  |---|---|---|
  | median |e| product (%) | 0.88 | 1.19 |
  | median |e| hybrid (%) | 0.033 | 0.043 |
  | max |e| hybrid (%) | 0.10 | 0.21 |
  | median |log Ẑ_hyb err| | 3.3e-4 | 4.3e-4 |
  | median PIP MAE plain / RB / hybrid-mean | 1.1e-3 / 1.1e-4 / 5.5e-5 | 1.5e-3 / 1.7e-4 / 9.0e-5 |
  | exact HPM in V; HPM from V = exact; median = exact | 20/20 each | 20/20 each |
  | median stages; seconds | 11.5; 14 | 10.5; 26 |
  W1_r001 (both modes) and the s = 1 seed path on S6_r001 (seed_smc 357001) also ran cleanly.

## Job spec
Freeze E/dev/B/code to E/runs/<UTC>_smc_{bb,bern}/code/ (read-only; tar a26d3f34…); copy jobspec/cases_*.txt; pilot then full:
`nohup sh code/launch_precheck_bb.sh cases_pilot.txt 8 E/out/smc_bb betabinomial 1 30` and `... E/out/smc_bern bernoulli 0.2`;
seed-SD: append 1 or 2, separate out dirs. Completion: ALL_DONE and `grep -L "Exit status: 0" logs/*__<tag>.time` empty.
Cost (5 concurrent, busy node): BB ~7 s (S1) / 30 s (S6); Bern ~14 s / 55 s; ≤ 0.49 GB; 1,200 at 8 workers ~0.5–1 h BB, 1–2 h Bern.

## Unsure about
S2–S5 and W2–W6 not run end to end (pilot covers S4, W6). W1_r001 under BB took 1 stage (start ≈ target with weak signals) —
plausible, pilot should confirm vs exact. Seeds: s = 0 in 307001–322100; s = 1, 2 in 357001–422100; no collisions. No agents spawned.

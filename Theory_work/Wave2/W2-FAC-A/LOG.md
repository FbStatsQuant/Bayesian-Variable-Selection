# W2-FAC-A — LOG (dated running log)

Lead: Claude Opus 5.5 (Claude Personal). Ticket: reported-model consistency on factor / equicorrelated designs with
growing p, route A (low-rank common-component split). Protocols read: Theory_work/Wave2/PROTOCOL.md,
Wave1C/PROTOCOL.md, Wave1/PROTOCOL.md.

## 2026-11-09

* 05:58 Start. Read protocols, FINAL/sections s1, s3, s5, s6 (consistency.pdf sources), C-GROW REPORT/STATEMENT/
  lemmas L0–L4, D2/D3 summaries, bvs_core.py.
* 06:10 Numerics infrastructure (numerics/): `fac_common.py` (designs S5, CS3, CS5, F2, F2r; fast exact local
  search by Schur up/down-dates; selftest vs bvs_core.Problem.F: max error 4.3e-14, identical LS paths);
  `d_run.py` (diagnosis D1, iid rows), `d_summ.py`.
* 06:16 D1a (iid rows, c = 1, p = 100/200/400, n = 400…3200, 8 seeds): `D1a_summary.md`. MR1 cap: S₀ reached
  in every run (S5, CS3, F2r); paths mostly pure null deletions (occasional swaps, within the MR1 slack); NA fails
  along the path in a minority of runs and on 0–30% of random lattice sets; TL never fails. Fraction of nulls in
  the start mode 0.02–0.42 (finite n; growing with n).
* 06:20 D1b (c = 4, S5 iid; CS3 p > K): start mode size essentially unchanged by c (partial correlations, not the
  signal scale, limit the start mode); at n ≤ 800 the p > K regime is not reached by the start mode.
* 06:25 Structural observation (to be proved): the shipped score is a function of (G_T, X_Tᵀy, yᵀy); for an
  exact-Gram design every search object is a function of (Σ, z = Xᵀy). `fac_exact.py`: exact-Gram simulator
  (draws z from its exact law; selftest: scores agree with the explicit-X computation to 2.8e-14; MC means agree).
* 06:28 D2 (exact Gram, n = 1e4…1e7, CS3): from n = 1e5 on the start mode is (almost) all of [p]; from n = 1e6
  exactly [p] in 15/15 runs; LS0 path = pure null deletions in all runs, NA never fails along the path (max add
  gain ≈ −½ log n), swap gains ≈ −1e-6; but NA FAILS on one-sided lattice sets T = S₀ ∪ {top-m nulls by noise}
  (e.g. p = 400, n = 1e7) — the whole-lattice NA is genuinely limited (consistent with the analysis: sup over the
  lattice of the add statistic ≈ (1+κ̄)·√(2 log p) with κ̄ = 1 for CS, i.e. lattice NA iff p ≲ n^{1/6}).
* 06:35 Analysis (notes in PLAN.md): (i) the add statistic Z_{T,l} depends on the design only through
  (G, g = Xᵀε/σ ~ N(0, G)); (ii) for Σ = λλᵀ + Ψ (Ψ block-diagonal, bounded groups), Pythagorean split along the
  residual factor direction ŵ_T = (I − P_T)f gives |Z_{T,l}| ≤ |Ξ_{l,T∩g(l)}| + κ̄·M_ζ, uniformly over ALL T —
  direction count p·2^γ̄ for Ξ, one group χ² maximum for the factor term; (iii) exact 1-D reduction for exact-Gram
  compound symmetry (`cs1d.py`, selftest vs exact scorer 5.6e-9, identical LS paths) and the two-tail ("gap")
  invariant of the deletion path.
* 07:02 R01 statement lock (Codex Sol high): LOCK-WITH-CHANGES, 10 required changes — all applied; STATEMENT v1.1
  LOCKED (reviews/R01_statement_lock_sol.md, R01_disposition.md). New numerics/D2_lattice.md (one-sided lattice NA
  failures, d_exact.py fields lat_adv_*; the earlier D2_summary column read another field and showed 0/0).
* 07:05 L1 (key lemma U) written: lemmas/L1_uniform_add.md. Falsification: numerics/FU_out.txt (exact identity max
  error 8.9e-15 over 53,003 (T,l); deterministic bound (1.2) 0 violations; one-sided envelope ratio ≤ 0.885 (CS) /
  0.736 (BCS) at p = 2000; perturbation ratio to δ√p ≤ 0.14) and FU5_out.txt (adversarial members: tiny loadings,
  sign changes, negative within-group correlations; 39,895 tests, 0 violations). R02 (Sol xhigh) launched.
* 07:08 D3 stress (cs1d.py, exact 1-D CS LS0 from [p], a ∈ {0.3,0.7,0.9}, s₀ ∈ {1,4}, p ∈ {200,1000},
  n ∈ {1e4,1e6,1e9}, 20 seeds): 720/720 pure null-deletion paths (no swap, no add), 718/720 ended at S₀
  (numerics/D3_summary.md) — evidence for the path route beyond 1/6 (Part III).
* 07:10 L2 (sandwich, Q = [p] re-proof), L3 (NA/TL full lattice), L4 (assembly) written.
* 07:15 F-NA/F-SHARP (numerics/fna_check.py → FNA_summary.md; exact 1-D formulas validated to 1.2e-9): exact CS, n up
  to 1e12: no one-sided NA failure for log p/log n ≤ 0.14 at n ≥ 1e9 (0/40 runs per row group); at 0.30 the number
  of failing runs grows with n (s₀ = 4, a = 0.7: 1, 3, 5 of 10 at n = 1e6, 1e9, 1e12) and the median max add gain
  rises towards 0 — consistent with the threshold 1/6 (slow O(√log) corrections).
* 07:18 R02 (Sol xhigh, key lemma L1): VERIFIED-WITH-AMENDMENTS (5 MINOR: representation-dependent κ and κ'_* vs κ'_bd;
  explicit L_ψ constants; PSD domain and empty-set conventions; wording of the union bound; original-space event in the
  coupling) — all applied to L1 v1.1. Reviewer's independent exhaustive check: 2310 pairs, 0 violations.
* 07:20 L5 (random design + instances), L6 (SHARP), L7 (delivery), L8 (frontier tools: CS-1D, GAP; Conjecture PATH-CS)
  written. CHECKPOINT.md written. R03 (Sol high: L2–L4) and R05 (fresh Sol xhigh mid-point, STATEMENT + lemmas only)
  launched.
* 07:25 TV certificates (numerics/TV_cert_out.txt): S5 positive for all three layouts; (GC-CS) fails exactly at a = 0.5
  for the study patterns (masked truth) — recorded in L5.3. R04 (Sol high: L5–L7) launched.
* 07:40 R03 (Sol high): L2 V-W-A, L3 V-W-A, L4 VERIFIED; 3 MINOR applied (reviews/R03_disposition.md).
* 07:50 R05 mid-point (fresh Sol xhigh): CONTINUE; 1 MAJOR (exact S5 certificate) fixed via Lemma TVF + tv_cert_exact.py (exact minima 2023/32500, 7/2080); 2 MINOR fixed (reviews/R05_disposition.md).
* 08:00 R04 (Sol high, L5–L7): no FATAL; 1 MAJOR (already fixed after R05), 6 MINOR — all applied (reviews/R04_disposition.md). All lemmas L1–L7 now cross-family checked.
* 08:20 R06 sweep (Sol xhigh): 0 FATAL / 0 MAJOR / 13 MINOR / 4 EDITORIAL — all fixed (reviews/R06_disposition.md); STATEMENT v1.2 wording. CITECHECK 28/0 misses.
* 08:45 Council seat A (Codex Sol xhigh, R07): PASS 9.2, all six gates PASS, no required fixes; 2 optional suggestions applied (00_MAIN version; fna_check.py writer header).
* 09:00 Council seat B (Claude Opus 5.5 high, R08): PASS 8.9, all gates PASS; 2 editorial fixes + 5 optional suggestions applied. COUNCIL ROUND 1 PASSED (Sol 9.2 / Opus 8.9). REPORT.md written.
* Note (07:59 CST by the system clock): the clock times written in entries after 07:25 were estimated and run ahead of the actual clock; the order of events is correct.

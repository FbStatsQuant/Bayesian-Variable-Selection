# W2-FAC-B — LOG

* 2026-11-09 05:54 — start; read Wave2/Wave1C/Wave1 protocols, FINAL s3/s5/s6/s7, C-GROW REPORT/STATEMENT/L0/L4, A2.
* 06:05 — numerics: fac_core.py (exact-Gram reduction: score depends on (Sigma, g ~ N(0,Sigma), chi2)); self-test
  fac_selftest_out.txt (scorer = direct to 4e-14; closed-form scans = direct to 1.4e-12).
* 06:15 — N1 grid (700 runs): at large n the start mode is [p] for S5/F1/F2 and the LS0 path is pure deletion with NA
  margin about -0.5 log n; at intermediate n (start != [p]) NA fails at the start and a few swaps occur (<= 3 extra
  moves). Heuristic analysis: the factor coupling enters through a k-dim posterior error e_T; adversarial (lattice)
  bounds give only p <= n^(1/6)-type results; path structure is needed.
* 06:35 — N2: saturated start p > n/2 (n=600, p=500): 19 swaps then deletions, 315 moves > MR1 cap 311 -> obstruction.
* 06:45 — Compound symmetry: exact 1-D reduction (every neighbour depends on xi_j - x_T, one common centre);
  cs_core.py / cs_gain.py (closed form, log1p-stable), validated against the general scanner (cs_selftest_out.txt).
  Decision: core theorem = compound symmetry, exact Gram, p <= n/2; S5/general factor/iid rows/p > n/2 = frontier.
* 07:00 — STATEMENT v1, PLAN; N3 grid running; statement lock requested (R01).
* 07:00-07:20 — N3 grid done (468 runs; violations only at n <= 1e4 with weak truths = finite-n TL failure;
  N3_summary.md). N4 start-mode falsification (66/72; misses only at n = 1e5). N5 invariants (drift identity exact,
  argmin = closest to x_T, Top+/- structure, bulk |x|/H <= 0.06, end |I| <= 2).
* Deviation (logged): lemma drafts L1-L5 were written while R01 (statement lock) was running; none is used downstream
  or sent for checks before the lock verdict; they will be revised to the locked statement.
* 07:25 — R01 (Sol high) REJECT: swap log-n margin in (C2)(iii) false (analytic p = 3 counterexample) + 6 required
  changes; all accepted (reviews/R01_disposition.md). STATEMENT v2; cs_gain/cs_core now implement the lexicographic
  tie rule and record best-swap-minus-current; cs_selftest rerun 4/4. L4 claim aligned (swap domination only).
* 07:35 — R02 (fresh Sol high) lock review of v2 requested. N3b hard-corner falsification launched.
* 07:40 — R02 (fresh Sol high): LOCK-WITH-CHANGES (4 items: extended a_T/b_T, signed energy constant, bounded-p
  regime + relevance-set wording, direct gap-invariant diagnostic); all applied → **STATEMENT v3 LOCKED**
  (reviews/R02_disposition.md). numerics/n6_gap.py (direct (C2)(iii) test incl. N0 != empty) launched.
* 07:41 — lemma checks launched: R03 (Sol high) L1-L3; R04 (Sol xhigh) key lemma L4.
* 07:47 — R03 (Sol high) L1/L2/L3 VERIFIED-WITH-AMENDMENTS (8 items) — all applied (reviews/R03_disposition.md).
* 07:49 — R04 (Sol xhigh) key lemma L4: VERIFIED-WITH-AMENDMENTS, no fatal issue; 7 items applied (reviews/R04_disposition.md).
* 07:52 — CHECKPOINT.md written (key lemma checked). Launching R05 (L5 check) and R06 (mid-point).
* 08:00 — citecheck.py written (draft run 13/13 resolve); fixed stale cite 04_theory.tex:489 -> :492 (M5(0) card TH05.0) in L5.
* 08:05 — R05 (Sol high) L5 VERIFIED-WITH-AMENDMENTS (4 minor), applied. Waiting for R06 mid-point.
* 08:08 — R06 mid-point (fresh Sol xhigh): CONTINUE; 2 minor items (both already applied via R05). Launching R07 exhaustive sweep.
* 08:15 — HQ update read (FAC-A done: lattice route to 1/6, SHARP; route B is the route beyond 1/6). Added L2.5 Corollary M (masked truths via FS′), flagged post-lock, for the council.
* 08:25 — N7 masked-truth falsification: 18/18 start = S*, path pure to S0.
* 08:11 — R07 sweep (Sol xhigh): 0 fatal / 2 major / 11 minor / 4 editorial — all fixed (reviews/R07_disposition.md); STATEMENT v3.1.
* 08:14 — CITECHECK.txt final run 14/14 ok. Council round 1 launched: R08 (Codex Sol xhigh), R09 (Claude Opus 5.5 high, Claude Work); brief reviews/COUNCIL_BRIEF.md.
* 08:20 — R08 council seat Sol (xhigh): ACCEPT 9.3, all six gates PASS, no required fixes. Waiting for R09 (Opus).
* 08:27 — Council round 1: R08 Sol 9.3 ACCEPT, R09 Opus 9.0 ACCEPT, all six gates PASS in both → PASSED. Editorial fixes applied (reviews/R08_R09_disposition.md).
* 08:35 — REPORT.md finalised; CITECHECK rerun incl. REPORT. RESULT: PROVED-CHECKED (FAC-CS).

# W3-RM — LOG

2026-11-09 (CST). Times are taken from `date` and file modification times (an earlier draft of this log carried
estimated times; corrected 17:03).

* ~16:00-16:20 Read PROTOCOL.md, PROGRAM.md (Wave 3), the Wave 1/1C/2 protocols, C-GROW (STATEMENT, REPORT, L0–L4), W2-LOC2
  (STATEMENT, REPORT, L1, L2 head), W2-UNI (STATEMENT, L2_k0), SR critique §2/§4, ADJ_opus §3–§5, ADJ_astra §3, W1-N3
  REPORT, C-PACK e4′ (I1 §4), C-DLV L4 pathwise claim, GEN L5 [OP], APP L3 (PTV), L5 (VN head), code
  `Scripts/SMC_BVS/core/cpp/v3_start.h`, `v3_core.cpp:405-480`, `v3_engine.h:370-400`.
* 16:20 Design decisions (lead):
  1. Theorem 3 = deterministic core RM-0 + Form F (fixed design) + Form R (Gaussian rows), with interface properties
     [POST], [SAND], [TL], [NA], [E4] and one bridge lemma per assumption.
  2. Partition-free (V), (L): quantify over all conditioning sets of size ≤ 15; the block-relative forms (GROW G3) are
     kept as the weaker hypotheses the proof consumes.
  3. **Finding:** "(V) + (L) with |Q| ≤ C log n, arbitrary C" is not what GROW proves (ADJ_astra was right): the
     whole-lattice NA needs (G4). Form F therefore carries a lattice condition (N): (N-χ) |Q∖S₀| ≤ (1−δ₀) log n, or a
     new direction-complexity condition (N-D) generalising (G4-dir) (new Lemma NA-F), which reaches polylog |Q| in
     fixed design.
  4. **Finding:** Form R cannot be obtained from Form F by conditioning on X (off-block signal = extra Gaussian
     noise; sample (L-gain) with η < η_A fails). Form R keeps population conditions; (L-R) needs a localisation clause
     because the partition is X-measurable (selection removal). New abstraction SAND-R.
  5. e4: closable at code level as "some maximiser" under EX-A: enumeration path = N3(a); fallback path by a direct
     tight-path argument; integration at `v3_core.cpp:469-476`.
* 16:22 STATEMENT.md v1.0 (draft), PLAN.md written.
* 16:23 R01 statement lock launched (Codex gpt-6.1-sol, high).
* 16:24 numerics/SPEC.md written; sharpness-probe helper launched (Claude Sonnet 5.5 on claudeAgent, high) in parallel
  with R01: the probes depend only on the HQ-specified assumptions (V), (L) and on (N), not on the wording under
  review. (Recorded as a deliberate parallelisation, not proof work before the lock.)
* 16:26 ASSUMPTION_MAP.md drafted (verdict column to be completed after numerics and R02).
* 16:27-16:30 R01 returned LOCK-WITH-CHANGES (5 required, 4 optional); all applied; STATEMENT v1.1 LOCKED
  (reviews/R01_statement_lock_sol.md, R01_disposition.md).
* 16:31 Launched R02 "better theorem" (Codex gpt-6-astra, high) and the parallel prover for Lemma SAND-R (Codex
  gpt-6.1-sol, high; lemmas/L3_SANDR.md).
* 16:31-16:37 Lead wrote lemmas/L0_core.md (RM-0), L1_fixed.md (B1, B1', B2, B3, B4, B6, RM-F), L2_NAF.md (new Lemma
  NA-F, N-loc), L5_E4.md (code-level e4 closure), L4_formR.md (B8a, D-loc, B8b, B9, RM-R assembly; depends on L3).
* 16:38 Falsification numerics for NA-F / N-loc: numerics/f1_naf_check.py -> f1_naf_out.txt (60 runs, 3 designs,
  4416 lattice pairs each): 0 violations of the identity, the bound, decomposition (2.1) and the Step-3 implication.
  (Python with numpy is `py -3.13`; the default `python` 3.15 has no numpy.)
* 16:38 Launched lemma checks R03 (L0, L1, L2; Codex gpt-6.1-sol high) and R05 (L5 E4 against the code; Codex
  gpt-6.1-sol high).
* 16:36 R02 (Astra) returned: 8 proposals; no counterexample to any locked assumption. Disposition
  reviews/R02_disposition.md: adopted as post-lock weakenings P1 (Form F entropy budget h < 1/2), P2 (RSS-normalised
  leakage; lemmas/L1b_rss.md), P3a (localisation rate r_n = o((n log n)^(-1/4)); lemmas/L3b_rate.md), P7 (archive
  corollary); recommended to HQ: P5 (polynomial |Q|, design-agnostic) as the most valuable follow-up, P3b, P4, P1 for
  NA-R; P6 (dropping (N)) open.
* 16:39 Parallel prover returned lemmas/L3_SANDR.md: "PROVED (by this seat, unchecked)", lemma exactly as targeted,
  no repair of (L-R); remote/remote covariance bounds not needed; floors only on sets of size <= 16 + s0.
* 16:44 Launched R04: cross-family check of L3_SANDR.md + L3b_rate.md (Claude Opus 5.5 on claudeAgent, high).
* 16:46 lemmas/L7_examples.md written (B10 verifications for UNI-0 and LOC-BF classes; fixed-design instances; table).
* 16:43-16:48 R03 returned (L0/L1/L2): all VERIFIED or VERIFIED-WITH-AMENDMENTS, 1 MINOR (empty family), applied.
  R05 returned (E4 vs code): VERIFIED-WITH-AMENDMENTS (1 MINOR citation, 2 NIT), applied; reviewer's falsification
  84,000 calls / 0 failures on the production header. Disposition: reviews/R03_R05_disposition.md.
* 16:49 STATEMENT v1.2: adopted weakenings [P1] (h < 1/2), [P2] (tau-normalised leakage), [P3a] (rate r_n), corollary
  [P7]. v1.1 hypotheses imply v1.2 hypotheses; flagged for HQ in REPORT (HQ may revert to v1.1 wording at no cost).
* 16:50 launched, 16:56 returned: R06 (batch 2, Sol high) returned: Lemma tau/B2tau, B1', [P1], archive corollary, Form R bridges VERIFIED (some
  with minor amendments); examples file WRONG as first written (4 MAJOR: missing energy bound in E-F2; three overstated
  rows about families outside the theorem). All corrected; reviews/R06_disposition.md. No finding touches RM-F/RM-R.
* 17:02 R04 (Opus, cross-family) returned: SAND-R VERIFIED-WITH-AMENDMENTS (3 MINOR, 4 NIT), SAND-R' VERIFIED;
  amendments applied; reviews/R04_disposition.md. All lemma files now have a cross-family check.
* 17:09 R07 mid-point (fresh Astra high; statement + lemma files only): CONTINUE; no FATAL/MAJOR; 3 MINOR + 1 NIT applied
  (p = 1 branch of POST-R; AR example hypotheses; feasibility-enlargement footnote; empty-pair conventions);
  reviews/R07_disposition.md.
* 17:12 SHARPNESS.md drafted (analytic content; numerics section pending). citecheck.py written.
* ~17:15 T3 server restart (HQ notice). After restart: citation check re-run to completion — reviews/CITECHECK.txt:
  265 citation ranges, 0 misses; 27 token assertions, 0 failures; 8 quoted statuses, all found verbatim. Numerics helper
  (Sonnet) still alive (V1 and L2 finished; L1 and N1 running). No delegated review was lost (R01–R07 all on disk).
* 17:26 R08 exhaustive sweep launched (Codex gpt-6-astra, high).
* 17:33 R08 sweep returned: 0 FATAL, 6 MAJOR, 11 MINOR, 4 EDITORIAL; no finding breaks (C1)/(C2); the MAJOR items were
  overstated necessity/sharpness claims in SHARPNESS.md / ASSUMPTION_MAP.md, a false "path-NA is necessary" sentence,
  and an unsafe citation resolver. All 21 fixed: SHARPNESS.md and ASSUMPTION_MAP.md rewritten (v2), citecheck.py v2,
  statement and lemma wording; reviews/R08_disposition.md. CITECHECK: 274 ranges / 0 failures, 32 tokens / 0 failures.
* 17:55 Numerics helper found stalled after the restart (N1 log overwritten by a failed relaunch, no results file, script
  left with a syntax error which the helper then fixed). Lead cancelled the helper and took over: n1_lattice.py
  (10 seeds for C >= 4; 240 runs, 1624 s) and l1_groupsize.py (180 runs, 812 s) re-run in the background;
  build_summary.py fixed (sort key) and run; numerics/SUMMARY_SHARPNESS.md assembled (provenance note + generated body).
* 18:40 SHARPNESS.md section 6 (observed numerics) appended, every count re-derived from the CSVs:
  V1 296/300, L1 138/140 (old cap 89/140), L2 418/420 (sandwich with Q = S0 fails in 209/420), N1 whole-lattice NA
  violated in 90/180 while LS0 from Q reaches S0 in 178/180. Sharpness gate outcome: every assumption probed is flagged
  `improvable` for the conclusion; HQ to decide on follow-up tickets (REPORT section 6).
* 18:42 REPORT.md drafted (result line pending the council). reviews/COUNCIL_BRIEF.md written.
* 18:45 Council round 1 launched: seat A Codex gpt-6-astra (high), seat B Claude Opus 5.5 (high, claudeAgent).
* Council round 1 returned: seat A (Astra) 8.8, G1-G5 PASS, G6 FAIL (L2 numerics mislabelled as assumption violations);
  seat B (Opus) 8.9, all gates PASS, no required finding. Round NOT passed (one gate failed). All findings of both seats
  fixed: L2 relabelled as exploratory with a note on nominal classification; statuses of DLV and FAC-PK quoted; FAC-PK
  PATH wording; input-map edges; (N-chi) old-cap remark; ell_n defined; STATEMENT v1.2.1 (no hypothesis or conclusion
  changed). reviews/C1_disposition.md. CITECHECK re-run: 280 ranges / 0 failures; 32 tokens; 10 statuses.
* 19:02 Council round 2 launched with two fresh seats (Astra high; Opus high on claudeAgent), brief reviews/COUNCIL_BRIEF_R2.md.
* Council round 2 returned: seat A (Astra) 9.8, seat B (Opus) 9.1, all six gates PASS in both, no required finding ->
  PASSED. Optional items (1 MINOR, 7 NIT) applied; reviews/C2_disposition.md. CITECHECK after final edits: 280 ranges /
  0 failures.
* 19:15 REPORT.md finalised: RESULT PROVED-CHECKED (with flag 1: a lattice condition remains). Nothing committed (HQ commits).

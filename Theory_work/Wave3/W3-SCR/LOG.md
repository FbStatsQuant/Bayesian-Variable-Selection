# W3-SCR — LOG (2026-11-09)

- Read Wave3 PROTOCOL/PROGRAM, Wave2/Wave1 protocols, BLIND_fable Thm 5, CRITIQUE_fable §1.1/§4, s1_setting.tex.
- **Code check** done → `CODE_CHECK.md` (CC1-CC5). `local_certified` = the reported HPM is the scanned endpoint of the
  final search or of LS0 and no neighbour (deletion / addition if |Ŝ| < K / swap) has strictly larger F. Certified ⇒ 𝒪.
- Core copied to `numerics/core_copy/` (main @ 2252d57) and compiled locally; N0 fidelity passed (`numerics/n0_out.txt`).
- N1 batch 1 launched (80 fits, n = 100, p = 400, 4 designs × 2 signal scales × 10 reps).
- Statement drafted (`STATEMENT.md` v1). Decisions:
  - consume **sparse visibility Γ_n(q)** (the noiseless gain of the best missing truth, in the method's own ridge
    geometry) instead of the sparse eigenvalue floor; floor / anchored floor / identifiability margin enter through
    bridge Lemma B (PROTOCOL item 5);
  - q_n up to c₁ n / log(p ∨ n); conclusion for every certified search endpoint (CC3);
  - added SCR-C (exact recovery under φ_n > 2 log p/(2 log p + log n) + ε), SCR-R (refit rates), SCR-N (sharpness at q = 0).
  - The brief pre-authorises strengthening ("make it as strong as possible"); the card's statement is kept as Corollary A1.
- N3 (lemma falsification, v1 lemmas): all identities / inequalities of L1, L4, L5 step 2, L6 pass (`numerics/n3_out.txt`,
  first run); the end-to-end check showed MC is driven by the total scale τ_n (motivates SCR-A°).
- **R01 statement lock (gpt-6.1-sol high): DO-NOT-LOCK** — 1 blocker (A1 at q_n = 0), 3 major (SCR-C with growing s₀;
  SCR-N domain; log s₀ in A∞), 3 minor, 5 notes; CC1-CC5 confirmed. All accepted → `reviews/R01_disposition.md`;
  STATEMENT v2; lemmas L1-L6 updated (witness t(S), E4, L1.5°, SCR-A°, B2°, A1°, exact B_n in SCR-N, s₀ = O(1) in SCR-C).
- `scr_lib.py` prior normaliser aligned with the core; N0 rerun: max |F_py − F_core| = 6.0e-13 on 16,004 models.
- ASSUMPTION_MAP.md written. N2 boundary numerics launched (16 scenarios × 10 draws).
- Launched in parallel: R01b statement re-lock v2 (sol high), R02 better-theorem review (astra high),
  R03 lemma check L1-L4 (sol high), R04 lemma check L5-L6 (sol high).
- (T3 server restart.) R01b: **LOCK** (v2). R02 (astra, better theorem): proposals 1, 2, 3, 4/f, 5 adopted → STATEMENT v3,
  L7 (SCR-M, M1-M6), B2d, L5 rewrite; proposal 6 (quadratic contrasts) not adopted. R03, R04 (sol, lemma checks on v2):
  no blocker/major in claimed results; minor fixes applied; false ω-only remark removed. Dispositions:
  `reviews/R02_R03_R04_disposition.md`.
- After the restart both numerics batches were found still alive (not killed), so the relaunch had doubled them and two
  writers shared output files. All related processes were stopped, outputs validated (`numerics/validate_out.py`:
  corrupt N2 files removed, N1 records deduplicated), and the missing work restarted once.
- N4 (`numerics/n4_master.py`): SCR-M gap inequality 105,955 checks, 0 violations; M3 4/4; M5 2,721 moves, 0 truths dropped.
- N3 rerun with the new items (L1.5°, B2°, E4, SCR-A° step 1): all pass (`numerics/n3_out.txt`).
- N2 complete (16 scenarios). In cs/fac/dupnoise "strong" scenarios 1/10 draws has a sparse LO model missing truths:
  diagnosed as visibility-margin failures at n = 100 (noiseless ratio 0.80-1.23, `numerics/n2_out/DIAG_visibility.txt`),
  i.e. mixed-sign truths under a common factor mask each other at this sample size.
- R05 (sol, v3 delta check): new mathematics correct; DO-NOT-LOCK on 3 overstated summaries + 7 minor → all fixed (v3.1),
  `reviews/R05_disposition.md`. Citation check written and passing (28 citations, 20/20 tokens).
- Launched: R05b re-lock v3.1 (sol high), R06 mid-point (astra high, statement + proofs only).
- R05b (sol, re-lock v3.1): DO-NOT-LOCK — one major (maximising witness in STATEMENT M3) + 3 minor; fixed → v3.2.
- R06 (astra, independent mid-point on statement + proofs + code): **CONTINUE** ("SCR-A and SCR-M are proved"); its
  major = R05b N1 (already fixed); two minor wording fixes applied (`reviews/R06_disposition.md`).
- R05c (sol, lock confirmation of v3.2): **LOCK**.
- ASSUMPTION_MAP updated to v3.2 with N2 outcomes. R07 exhaustive sweep (astra high) launched.
- R07 (astra, exhaustive sweep): 0 blocker, 3 major, 9 minor — all majors in ASSUMPTION_MAP ("necessary" labels); every
  theorem chain verified. All 12 fixed (`reviews/R07_disposition.md`); STATEMENT v3.3 (wording/notation only).
- Council C1 launched: gpt-6-astra (high) and Claude Opus 5.5 (high, claudeAgent); brief `reviews/C1_brief.md`.
- **Council C1: PASSED in round 1** — gpt-6-astra 9.3, Claude Opus 5.5 8.9, all six gates PASS on both seats.
  Minor/note-level findings applied as post-pass edits (STATEMENT v3.4), `reviews/C1_disposition.md`.
- N1: 58/80 production fits done at 18:42; five equicorrelated strong-signal fits (reps 1, 2, 7, 9, 10) and one
  factor fit have been running for > 50 min (others of the same cell took 8-24 min).
- N1 closed at 20:40: 71/80 production fits finished (all certified, reported size ≤ 5; strong signals: S₀ ⊆ Ŝ in 32/32);
  9 fits (5 cs strong, 3 fac strong, 1 fac weak) were stopped unfinished after 0.8-3.1 h (`numerics/n1_unfinished.txt`).
- REPORT.md written. Build cache removed. Final citation check passes.

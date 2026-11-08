# W1-PXN — LOG

## 2026-11-08
- Read PROTOCOL.md, FR01 card (06_open_and_plan.tex:73-83), M5 card TH05 (04_theory.tex:464-540), regime map
  (04_theory.tex:820-860), history H.20 (05_history.tex:203), registry rows TH160, TH161, TH163, TH123, TH116, TH09,
  API-PXNGAP REPORT/PLAN/PROOF in full, W7-PART PROOF §0-§3, locked T03 STATEMENT, T22 STATEMENT.
- Own read of PROOF §§1-10 (lead seat, unchecked): found two dependency points: D1 (T03 cited without H-T02; T03♯
  available with XF VERIFIED), D2 (Theorem R explicit constant = W7 Corollary B, XF GAP per A-REV9). Minor points listed
  in PLAN.md. No counterexample to the statement seen.
- Wrote STATEMENT.md (draft v1), PLAN.md (v1). Called orchestrator_capabilities (codex gpt-6.1-sol available).
- Statement-lock review R00 (Codex gpt-6.1-sol high): "LOCK WITH CHANGES", 8 findings (6 MAJOR, 2 MINOR). All applied:
  STATEMENT v2 (headline liminf form; exact score/target; potential run R̄⁺ and D_n defined; omitted conclusions restored;
  D1/D2 sharpened; A-accounting completed); PLAN v2 (I8 Lean-readiness restored, I9 repair files, numerics specs, N8).
  Disposition in reviews/R00_statement_lock_codex.md. STATEMENT v2 LOCKED.
- HQ update: subagents authorized (PROTOCOL "Subagents"). Numerics N1–N7 delegated to a Sonnet 5.5 helper (claude-personal).
- HQ brief for this ticket (verbatim excerpt, recorded as the scope source for item 6): "the six items the report itself
  lists as needing independent check (REPORT.md:133-144): Lemma Tr-J(c) constants; Lemma E (E2),(E3); Lemma Lambda(a)
  Haar-span step; Theorem R (= W7 Theorem B); the operational closure OP-LS0 + GUARD; and the dependencies T22(i),(ii),
  T03, CONC, W7 Thm B have adequate status (report their exact statuses)". FR01's Lean-readiness item kept as I8.
- Repairs drafted (PROVED by this seat, unchecked): lemmas/P8_T03sharp.md (D1), lemmas/CR_corr_tails.md ([CONC′], (R′),
  D2 fallback), lemmas/L_strict_localmax.md ((L) via (E5)).
- Launched 8 fresh Codex gpt-6.1-sol (high) item reviewers in parallel, common brief reviews/_COMMON_BRIEF.md:
  I1 Tr-J → R11; I2 Lemma E → R12; I3 P2/B/Λ → R13; I4 Theorem R/W7/Lemma T → R14; I5 LS/P5/(C)/closure → R15;
  I6 P3′/P4/dependency statuses → R16; I7 Lemma U/(D_S)/(L) + L repair → R17; I9 repairs CR + P8♯ (+ L arithmetic) → R19.
- R12 (I2 Lemma E): VERIFIED WITH MINOR FIXES; 3 minors adopted verbatim (ERRATA E-1..E-4). (E2),(E3) VERIFIED.
- R11 (I1 Tr-J): VERIFIED WITH MINOR FIXES (ERRATA E-5, E-6). Report item #1 VERIFIED.
- R13 (I3 P2/B/Λ): VERDICT ERROR on Lemma B(ii) only (missing |A| ≤ n−3; false for |A| ≥ n−2 when p ≫ n). B(ii) is not used
  downstream (grep). Repair lemmas/B_ii_domain.md (ERRATA E-7), pending re-check by a new reviewer. Λ(a) Haar step,
  B(i),(i′),(iii), P2, Λ(b),(c), F2–F5 VERIFIED. Report item #3 VERIFIED.
- R19 (I9 repairs): VERIFIED WITH MINOR FIXES. CR/[CONC′]/(R′) and P8♯ (D1) XF VERIFIED; fix applied (P8♯ v2). D1 RESOLVED. D2 fallback (R′) available (summable, explicit).
- R15 (I5 LS/closure): VERDICT ERROR ×2 (Lemma LS(i) lacks ℓ ≥ c; P6′ sharp cost false and its event lacks (L)). Closure, (C), P5 VERIFIED (report item #5 VERIFIED under (OP)). Repairs lemmas/LS_P6_repair.md (E-8..E-11), pending new-reviewer re-check.
- R17 (I7 key lemma P6′): VERIFIED WITH MINOR FIXES (original (L) step ERROR, repaired file VERIFIED). ERRATA E-12..E-14. Mid-point review triggered.
- R14 (I4 Theorem R): VERDICT ERROR (arbitrary-t display; A0(c) auxiliary; exact-branch convention). Hotelling/Lemma 2/Cor. B constant VERIFIED ⇒ D2 RESOLVED. Repairs lemmas/R_branch_repair.md (E-15..E-18), pending new-reviewer re-check.
- R16 (I6 P3′/P4/deps): VERDICT GAP — #1 = D1 (already repaired, R19 VERIFIED), #2 = D2 (resolved by R14), #5 unproved sharpness remark → deleted (E-19); minors E-20. P3′, P4 VERIFIED; dependency ledger recorded.
- Numerics N1–N7 (Sonnet helper; numerics/SUMMARY.md): no violation of any checked inequality, identity or implication.
  N1 Tr-J (a) max ratio .46, (b) .99999 (tight but holds), (c-core) never fails on t′/j ∈ [1,10]; N2 Lemma E (E1)–(E5) hold on
  63,505 sets per (n,p), κ_E ≈ 30× loose; N3 Haar/Beta KS diagnostics fine incl. equicorrelated null groups, negative
  control rejected; N4 Hotelling density normalised to 6e-13, W7 Lemma 2 (U)/(L) 0 violations on 1,482 triples, Cor. B
  dominates exact union sum (vacuous at n = 200); N5 population margins c₂, c₅ attained (sharp), 0 violations over 80
  settings incl. adversarial; N6 Lemma LS and (C) implications 0 violations (p = 10 exact); N7 median 1−π(S₀) ~ n^{−1/2}
  (diagnostic; rare (L)-type upper-tail draws at n = 1600, 6400 with Z² ≈ 13, consistent with chi2_1 tails).
- R20 mid-point (fresh Codex, proof files only): MIDPOINT VERDICT: CONTINUE. Required: D2 choice (kept explicit constant per R14 + (R′)), SIZE onset n₁ in (R), cutoff sync, single consolidated proof. First two applied to STATEMENT; FINAL_PROOF.md next.
- N8 (Sonnet helper; numerics/n8/SUMMARY.md): end-to-end LS0 route, LH-iid g = 9, SIZE, p > n, (n,p) ∈ {(150,270),(300,540)},
  10 cells × 10 seeds. Partition recovered 100/100; S̃₀ = S° 43/50 → 48/50; S₀ scored by LS0 46/50 → 50/50; certified
  34/50 → 49/50; one (D_S) failure at a visited lattice state at n = 300 (proxy addition, margin −0.44; LS0 still reached and
  certified S₀ in 3 moves). Reading: consistent with the asymptotic theorem (failure frequencies fall with n); finite-n
  failures are expected (proven margins vacuous at these n). Not a counterexample: the theorem is a limit statement.
  N8 item 6 (observed log π₀(S₀) + c log p + (c/2) log n below the P4 limit mean, shifts −0.3…−0.7 at n = 300): explained
  at finite n by log π₀(S°) < 0 (median 1 − π₀(S°) ≈ 0.24 ⇒ log π₀(S°) ≈ −0.27, larger in other cells), the term P4's
  proof sends to 0 via P3′; not a contradiction of the limit law. Recorded as a diagnostic.
- R21 (new reviewer, repair re-check): VERIFIED WITH MINOR FIXES; 2 minors applied (exact-branch cases with s₀ ≤ K; W6 line cite). All repairs now checked by a reviewer different from the finder. Next: exhaustive sweep.
- Exhaustive sweep launched (fresh Codex gpt-6.1-sol high) on STATEMENT + FINAL_PROOF + PROOF/ERRATA + lemmas → reviews/R30_sweep_codex.md.
- R30 exhaustive sweep: 1 ERROR (sharper exact-branch D_n bound false when s₀ > K), 2 GAP (common Lemma-E event undefined; heuristic rate at PX:475), 4 MINOR. All 7 fixed (FINAL_PROOF v2, R_branch_repair, L_strict_localmax, STATEMENT precedence note, ERRATA E-21, E-22). Next: council round 1.
- Council round 1 launched: Codex gpt-6.1-sol high → reviews/C1_council_codex.md; Claude Opus 5.5 high (claude-personal) → reviews/C1_council_opus.md. Brief reviews/_COUNCIL_BRIEF.md.
- Council R1 Codex: all gates PASS, SCORE 8.6; 2 minors fixed (FINAL_PROOF errata range, onset gloss).
- Council R1 Opus (claude-personal): all gates PASS, SCORE 8.3; 1 MAJOR (form: consolidate into one supplement text,
  non-blocking) + 7 MINOR; minors fixed; MAJOR recorded as open item.
- COUNCIL PASSED in round 1 (Codex 8.6, Opus 8.3; all gates PASS in the same round). Writing REPORT.md.
- REPORT.md written. RESULT: PROVED-CHECKED.

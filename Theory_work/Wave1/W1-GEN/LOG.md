# W1-GEN — LOG

## 2026-11-08
- Read PROTOCOL.md; SoP 00, 01, 04 (TH05, TH09, shared defs, regime map), 06 (FR01–FR03), 02 (start, HPM/LS0);
  BS/W1-T37R/PROOF.md (Theorem A, Lemma 3, Theorem C), BS/API-PXNGAP/{REPORT,PROOF}.md, locked T22 (i)(ii)(iv) and
  T22(iii) STATEMENT + PROOF_v2.tex.
- Explore helper located: study generator (Scripts/Data_generators/gen_dev_data.R:18-42; iid rows, groups of 5, one
  active per signal group, scenarios S1–S6), W = exact-Gram fixed design (BS/MEET-THM/R1_C.md:362), LH-LAT m₀ and
  Thm5-LH (BS/W4-T38FULL/T38_PROOF.md:217-269; BS/W1-EXP/PROOF.md:343-362).
- Key decision D1: centre law = T22(iii) with a general reference S* (the locked proof uses S₀ only as the reference
  and as the label of the leakage family; checked by reading PROOF_v2.tex lines 35-481). EXP′ to be proved (L1).
- Key decision D2: descent via bounded relevance set 𝒱 + SEP, not via a lattice margin. Reason: Lemma 3 (W1-T37R)
  gives an order-n Λ-decrement from every state missing a truth under SE + BM-∞, so no progress/non-progress margin is
  needed inside 𝒱 (avoids RF176's failure of PGD on masked LH); F strictly increasing on the finite 2^𝒱 bounds moves.
- Key decision D3: counterexample = bounded-𝒱 cannot be dropped (proxy flood vs move cap ℓ_n). Study scenario S5
  (between-group 0.3) looks like a natural instance of the same obstruction.
- Wrote STATEMENT.md v1, PLAN.md. Next: statement lock (Sol), numerics helper.
- R01 statement lock (Sol): LOCK-WITH-CHANGES, 9 required changes; all applied → STATEMENT v2 LOCKED
  (reviews/R01_statement_lock_sol.md, reviews/R01_disposition.md). Notable: SEP made relative (c_S < 1); S* existential;
  C6 redesigned with weak nearly-orthogonal proxies so only |𝒱| bounded fails; study sequence defined (S2/S5 expected
  outside: AR(1) start mode grows ~log n with gray-zone crossings; S5 common factor floods every block).
- Drafted lemmas L1 (score expansion + contrast toolkit), L2 (centre law, generalized T22(iii) by substitution
  list), L3 (descent; key lemma), L4 (search semantics), L5 (assembly, de-randomisation), L6 (instances: LH exact
  Gram, LH-iid, W, study S1/S3/S4/S6 covered favourable; S2/S5 sufficient conditions fail), L7 (counterexample with
  weak nearly-orthogonal proxies, λ_min ≥ 1 − a). All "PROVED (by this seat, unchecked)".
- Launched Sol lemma checks: R02 (L1), R03 (L2), R04 (L3+L4). Numerics helper (Sonnet) running E1–E7.
- R02 (L1), R03 (L2), R04 (L3+L4): all VERIFIED-WITH-AMENDMENTS (Sol). Amendments applied → lemmas v2
  (reviews/R02_R04_disposition.md). STATEMENT (C2) wording clarified (search endpoint vs public flag); no change of
  hypotheses or conclusions.
- R02 (L1), R03 (L2), R04 (L3+L4): all VERIFIED-WITH-AMENDMENTS (Sol). Amendments applied -> lemmas v2
  (reviews/R02_R04_disposition.md). STATEMENT (C2) wording clarified (search endpoint vs public flag); no change of
  hypotheses or conclusions.
- Numerics partial (E1 unit tests all pass; E2 LH exact Gram: start = S* 240/240, LS0 scores S0 in all cells at n >= 800
  and in all but (rho,psi,c)=(.4,.2,2) at n=200 (6/20); E4(i) look-alike: first move from the empty centre is the
  non-progress "add x3" yet paths stay in V and reach S0). Finite-n failures at n = 200 only.
- Launched: mid-point independent review R05 (Sol; STATEMENT + lemmas only), lemma checks R06 (L5+L7), R07 (L6).
- R06 (Sol): L5 VERIFIED-WITH-AMENDMENTS; L7 GAP. All repairs applied (reviews/R06_disposition.md). Statement change
  (C6, v2.1): counterexample design now uses s0 >= 17 orthogonal truths so the block tables cannot score S0 (v1's
  singleton truth made the full-method D_n trivially 0); the claim remains "no universal LS0 discovery", both size
  bounds fail. Flag in REPORT.
- R05 mid-point (Sol, independent): CONTINUE. Major: (i) study-generator NL_avg under data-dependent packing is a gap
  -> C5(d) covered part downgraded to conditional on open lemma SEL; (ii) scope/checkability -> new L8 canonical
  certificate (block beta-min on block regression coefficients) + STATEMENT (C1') (addition, logged as v2.2).
- R08 (Sol) on L7 v2: GAP (extras count when a proxy block also holds further truths). Applied the reviewer's concrete
  repair (comparison with start mode + proxy in such blocks, uniform over U ⊆ S₀∖{0}) -> L7 v3; plus mixed-block VIS
  formula, leakage case list, exact-branch remark. L7 has 2 GAP verdicts; v3 sent to R09 (attempt 3 under the stop
  rule).
- R07 (Sol) on L6: (a)-(c) VERIFIED-WITH-AMENDMENTS, (d) GAP (NL_avg under X-selected packing). Wrote L6 v2: all
  amendments + Lemma SEL (selection-uniform leakage via reduction to a constant-size deterministic family and the
  recursive partial-correlation formula). L6(d) v2 to be checked in the sweep.
- R09 (Sol) on L7 v3: VERIFIED. L7 closed at its third attempt (two GAPs, then VERIFIED).
- R10 exhaustive sweep (Sol): 0 fatal / 1 major / 6 minor / 1 editorial. All fixed (reviews/R10_disposition.md).
  Statement v2.3: (C5)(d) locked to the actual 14-signal layouts (step 7 / 13) as a theoretical sequence; (C1′) gains
  the bounded-energy assumption. Next: council round 1.
- Numerics helper done (numerics/SUMMARY.md). E1 unit tests pass. At n = 3200 all route flags hold in E2 (80/80), E3
  (160/160), E4(i) (40/40), E4(ii) (20/20). Study generator (E6): S1/S3/S4/S6 have S* = S₀ (canonical certificate),
  NL ≈ 0, VIS margins growing ~ n/log n; at the REAL study size (p = 500, n = 200) VIS ratios are 0.16–0.94 (< 1):
  sigma²-dilution = VIS failing at finite n (FR02). S2: |S*| = 18–66, VIS ~ 1e-9 (outside); S5: start floods, LS0
  scores S₀ 20/20 at n = 200 but 0/20 at n = 3200 (cap) — the (C6) mechanism in the study's own S5. E7 (old C6 design)
  confirms the cap mechanism (d = 40: LS0 fails at n >= 800; threshold d/(2B) > ℓ + 1 is loose). Finite-n trap in
  E4(i) at n = 200 (one seed); centre law converges slowly. No contradiction of the asymptotic claims.
- Council round 1: Sol 9.0, all gates PASS, no required fixes (reviews/R11_council1_sol.md). Opus pending.
- Council round 1: Sol 9.0 (all gates PASS), Opus 8.9 (all gates PASS) -> PASSED in round 1. Opus's minor required
  fixes and most optional items applied afterwards (reviews/R11_R12_disposition.md); no hypothesis or conclusion changed.
- REPORT.md written; run complete.

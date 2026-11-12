# W3-MISR — LOG (heartbeat; PROTOCOL rule 12)

Lead: Claude Fable 5.2, effort high, Claude Work (`claudeAgent`). Branch `theory/W3-MISR` (base main @ 16a7f85).
Agents started so far (model, provider, role) are listed at each step. Claude-inference tally: all on Claude Work.

- 2026-11-11 19:20 CST. Branch created. HOLDS.md read: empty (no hold). Read: BRIEF; Wave3 PROGRAM, PROTOCOL (rules
  9–16), HOLDS; INFRA LIFECYCLE (§4.1 and the rest), templates ASSUMPTION_MAP, COUNCIL_BRIEF; parent C-MIS STATEMENT
  v1.2, `lemmas/L1_reduction.md`, `L2_gaussian.md`, `L5_frontier.md` §6, `L3_hpm.md:60-73`; sharp1 TRIAGE §1 rows 4–5,
  §2 T1; `sharp1/results/f05.md`; W3-POST2 STATEMENT v1.2.1 and lemmas A_occam, C_expectation, E_visibility; W3-POST
  STATEMENT v1.4 §0–§2; HQ_DECISIONS; registry rows C-MIS:*, W3-POST2:*, SOP:TH09.
- 19:43 Code path read (commit 16a7f85; last change to `Scripts/SMC_BVS/core` = 72785fe): `v3_preprocess.R:37-68,
  123-127`, `v3_fit.R:97,118`, `v3_setup.R:7-13`, `cpp/v3_score.h:14,39-60,217-223`. Finding: the scorer receives only
  the standardised response (`pre$y = sy$z`); `b0 = 0.01` is a constant on that scale; `s_y` is stored for reporting
  only (no other use in `core/*.R` or `core/cpp/*`). So the real-arithmetic target is invariant under y ↦ a1 + c·y,
  c ≠ 0. A run of the compiled code on rescaled responses is planned as numerics N0 (R 4.6.1 + Rtools present locally).
- 19:43 Findings while reading (design of v2):
  1. W3-POST2:C is a per-n, uniform expectation bound. With the invariance it gives MIS in expectation with constants
     free of σ²_𝒞; the random-design clause then needs no diagonal argument (conditioning + Markov), and the
     uniform-over-𝒜_n conclusion, tight constants and s-slicing are immediate.
  2. Registry: W3-POST2:A1/C/E/D are ACTIVE with council C1 passed, but their verbatim status is still "PROVED (by this
     seat, unchecked)" (HQ_DECISIONS:48-49 says PROVED-CHECKED restored). Rule 11 ⇒ MIS-R statuses carry
     "conditional on" these ids until HQ's acceptance record exists. Flag for HQ at CP1.
  3. The recorded gap to Song–Liang Thm 4 has two parts (registry note of C-MIS:Thm-MIS(i)): "fixed τ²" and "no density
     contraction claimed". The second closes by transferring W3-POST2:D through the same lemma (the parameter posterior
     is scale-equivariant). Added as a separately-statused corollary (beyond T1 items (a)–(d); flagged for HQ).
- 19:50 LOG.md, PLAN.md written. Next: STATEMENT v1.0, then Sol statement lock (blind).
- 20:05 STATEMENT v1.0 written; commit 197f557 (restore point). [agent 1] L01 statement lock launched: gpt-6.1-sol, codex,
  reasoningEffort high, blind (brief `reviews/BRIEF_L01_sol.md`).
- 20:10–20:40 Numerics started in the background: N0 (`numerics/N0_code_invariance.R`: compiles the core locally with
  Rtools, runs `v3_fit` on rescaled responses) and N1–N4 (`numerics/misr_numerics.py`).
- (run interrupted by the Claude Work 5-hour limit; resumed by HQ at 23:00 CST. HOLDS.md re-read: empty.)
- 23:02 Results read. N0: status/HPM identical in 25 runs, max |ΔPIP| 1.3e-10. N1: posteriors agree to 5e-14 across
  v_n ∈ {n⁻², 1/n, 1, n, n²}; δ/r_n ∈ [1.07, 1.42]. N2: relative margin is the right condition (a < ½ recovers, a ≥ ½
  fails). N3: t₃ residual harmless; heteroscedastic residual degrades the rate; random slope changes the target.
  N4: (E^σ) not needed numerically (improvable).
- 23:05 L01 returned: **REJECT**, 0 FATAL / 1 MAJOR / 3 MINOR. MAJOR = Remark P (Theorem F's BM-∞ not normalised;
  analytic counterexample). No counterexample to R′, MIS-R (i), (i′), (ii), Cor G, Cor H. All four accepted and
  applied → STATEMENT v1.1 (`reviews/L01_disposition.md`). This is the one fix round.
- 23:04 ASSUMPTION_MAP.md written. Briefs written: `reviews/BRIEF_L02_sol.md` (re-check of L01, sees L01 + diff) and
  `reviews/BRIEF_BT1_astra.md` (better theorem, blind). Commit, then launch [agent 2] L02 gpt-6.1-sol (codex, high) and
  [agent 3] BT1 gpt-6-astra (codex, high).
  (Clock note: the two entries above were written at 23:03–23:04; earlier drafts of this log guessed later times.)
- 23:08 [agent 2] L02 returned: **LOCK**, 0/0/0/0; every L01 finding RESOLVED (full scale audit of Theorem F in the
  review). STATEMENT v1.1 locked. [agent 3] BT1 (Astra) returned: 3 class-A, 2 class-B proposals + an obstruction to
  dropping (E^σ).
- 23:10 Proof files drafted: `lemmas/R_reduction.md`, `lemmas/M_misr.md`, `lemmas/G_corollaries.md`. `citecheck.py`
  written → `reviews/CITECHECK.txt`: 0 failures.
- 23:15 BT1 dispositions (`reviews/BT1_disposition.md`): A1 (projective law + TV stability) and A3 (localisation;
  first (OS) inequality for the superset clause) ADOPTED → STATEMENT v1.2, proofs R.5 and M.2(d); A2, B1, B2
  recommended as tickets (upstream, need new lemmas); the (E^σ) obstruction confirmed by numerics N5
  (`numerics/N5_out.txt`: E π(S₀) 0.87 → 0.003) and recorded. citecheck: 170 checks, 0 failures.
- 23:20 HOLDS.md re-read: empty. CHECKPOINT_1.md written; commit. Legs CP1 → CP2 are pre-approved and the reviews are
  clean after the one fix round (L02 LOCK), so the run continues to CP2: lemma line checks, then council.

# C-PACK — REPORT to Theory HQ (Wave 1C, closure of Wave-1 residuals), 2026-11-08 22:50 CST

> **Flags (read first).**
> 1. **Method requirement (for C-ENG):** `METHOD_REQUIREMENTS.md` MR1–MR3 — LS0 must start from and emit the coded
>    `start_mode(st, cap).S` (or a replacement returning the unique maximiser under exact arithmetic), as a deterministic data
>    function on every branch; keep cap ≥ 2 if an e4 fallback is triggered by `truncated`; no result needs the lex rule.
> 2. **Scope of item 1:** e4 is replaced by e4′ under the consumers' **existing EX-A**. The binary64 lemma covers the
>    start-mode identification step only (premise FP-TAB, untested for the coded scorer); it gives no floating-point
>    theorem for the full method. GEN (C6) and the T38 data-dependent-centre sketch are outside the replacement.
> 3. **A W1-PXN remark was wrong (non-headline):** the finite-n centring rate "O_P(√(log n/n))" added after the W1-PXN
>    council (C1 Opus #8) fails for slowly growing p; corrected in the consolidated supplement to O_P(√(log n/n) + 1/p)
>    (sweep R39 #1). PXN's limit law and headline are unaffected.
> 4. **Item 2's literal event identity** needs PXN's exact-branch convention (blocks = hypothetical make_blocks data
>    function on every branch); with it the discharge holds on GEN's whole p range (R35 #1).
> 5. Protocol deviation: lemma drafts for items 1, 2, 4 and the first item checks were started before the statement lock
>    (targets fixed by HQ's brief); the lock (R30) then changed the targets' wording, and the lemmas were re-aligned and
>    re-read by the blind mid-point review and the sweep. Council scope = items 1–4 per HQ's brief (R30 objected; recorded).

## 1. RESULT
**PROVED-CHECKED** — items 1–4 (council round 1 passed: Codex gpt-6.1-sol xhigh 9.0, Claude Opus 5.5 high 8.7, all six gates
PASS for both); item 5 delivered with its fidelity check FAITHFUL-WITH-FIXES (all fixes applied).

## 2. Statements as proved
`STATEMENT.md` (LOCKED v2 after R30). In short:
- **Item 1** (`lemmas/I1_e4_replacement.md` v2): audit of every e4/N3/tie occurrence in W1-PXN, W1-GEN, M5(b1-LH) — the
  positive consistency proofs use the centre only to identify it with a deterministic reference R on {π₀(R) > ½}.
  **Lemma UM:** under W1-N3 (H1)–(H4), argmax f = {R} ⇒ `start_mode(st, cap).S` = R (from N3(c) with N = 1, or N3(a); any
  cap ≥ 1, truncation flag irrelevant); π₀(R) > ½ suffices. **Lemma UM-FP:** under (H2-FP), a unique ĝ-maximiser is
  returned (N3(e)); FP-TAB Δ(R) > 2(η + ε) (table error + fold error γ_m Σ|terms|, ku < 1) gives it. **PXN repair (§1.1):**
  Lemma T(i)'s off-event centre identity is false for the capped coded routine (abstract block-order counterexample) and
  is replaced by P(C₀ ≠ S°) ≤ P(𝒜_nᶜ) + P(π̃₀(S°) ≤ ½). **Premise replacement** e4 → e4′ (I1 §4; patches
  `patches/P_e4_consumers.md` items 1–19).
- **Item 2** (`lemmas/I2_LHiid_unconditional.md` v2, `patches/P_GEN_LHiid.md`): GEN (C5)(b) uses W7 Thm B / [CONC] only via
  P(blocks ≠ groups) → 0 and P(𝒞_n) → 1; both follow from W1-PXN's repaired Theorem R ((R-c), or route (R′)) and [CONC′]
  (δ_n = 32√(2(A+1) log n/(n−1)), operator error L′_nδ_n = O((log n)^{3/2}n^{−1/2})) on the identical LH-iid family, with the
  exact-branch convention. GEN (C5)(b) holds **without** the two candidate inputs; GEN's other hypotheses/premises remain.
  The same [CONC′] replacement works in L6(d). Asymptotic only (onset ≈ 10¹⁰, council estimate).
- **Item 3** (`patches/P_SEL_L6d.md`, `patches/P_L8_certificate.md`): GEN Lemma SEL and L8 (C1′) each VERIFIED-WITH-AMENDMENTS
  by a dedicated xhigh check; amendments (localised Markov step; c > 0 and coefficient embedding; admissible (ε₀, κ) range;
  corrected W split θ(1 + ε_n/3); notation) independently re-checked. No counterexample.
- **Item 4** (`lemmas/I4_SL_corollaries.md` v2, `SONG_LIANG_MAP.md` v2): **SL0** (deterministic) max_j|PIP_j − 1{j∈S₀}| ≤
  1 − π(S₀), hence max_{j∈S₀}(1 − PIP_j) + max_{j∉S₀}PIP_j ≤ 2(1 − π(S₀)) (constant 2 sharp over arbitrary laws, not attained
  by a D0 posterior), uniform summaries = TV, ξ_q/MPM/HPM exactness for δ < min(q, 1−q) / ½. **SL1:** under T03♯ (fixed
  design), W1-PXN (P) (LH-iid joint law), GEN (C4), LH exact Gram: all these errors are O_P(√(log n/n)); P(HPM = S₀),
  P(MPM = S₀), P(ξ_{q_n} = S₀) → 1. **SL1′:** large-signal sensitivity without beta-min. **Reported quantities:** reported HPM
  jointly with output (M5/PXN/GEN); W1-N1 Corollary E islandwise only; **no in-probability sure-screening theorem for the
  shipped pooled R′ = 4 PIPs** in the cited cards — M1(i) ("(h), (i): PROVED (by this seat, unchecked)") needs stacking
  R′_n = 4⌈log₂(n+p+1)⌉ for a fixed finite list (or R′_n = 4⌈(n+p)⁶/4⌉ for ≤ (n+p)² summaries) and osc d ≤ D* = O_P(1);
  **SL2:** store-restricted PIP^𝒯 satisfy P(𝒪 ∩ {max_j|PIP^𝒯_j − 1{j∈S₀}| > 2δ_n}) → 0 on LH-iid and GEN's class, conditional
  on M4(b),(c) (statuses verbatim). Map: 13 rows; Theorem S's supplement NOT INSPECTED; Thm 4/Cor 2 → C-MIS.
- **Item 5** (`item5_PXN_consolidated/`, 7 proof files + INDEX/MAP/APPLIED_ERRATA/OPEN_QUESTIONS): self-contained proof of the
  council-passed W1-PXN statement with E-1..E-22 in place, no line references to API-PXNGAP PROOF.md; C-PACK's item-1/2
  results are separate addenda (INDEX), not incorporated.

## 3. Status per item, with evidence
| item / clause | status | evidence (reviews/) | numerics (numerics/) |
|---|---|---|---|
| 1 audit, UM, UM-FP, §1.1, e4′ | PROVED; XF-checked (R33 GAP → 7 fixes), re-read R38/R39, council | R33_item1_check_sol.md + R33_disposition.md; R38; R39; C1_* | item1_um_checks (17,136 + 1,546 + 60 runs, 0 violations); R33_falsify (1,912 FP-TAB instances, 0 violations; block-order counterexample) |
| 2 Lemma I2 + patch | PROVED; XF-checked (R35 V-W-A, 3 fixes), R38/R39, council | R35_item2_check_sol.md; R38; R39; C1_* | R35_falsify (144/144 blocks = groups; finite-n eigen onset not met, as expected) |
| 3 SEL | dedicated XF check VERIFIED-WITH-AMENDMENTS; patch re-checked | R31_SEL_check_sol.md; R37_patch_recheck_sol.md | item3_SEL_falsify (68.6M leakage triples; NL_avg(1/8) fails at finite n in 5/12 draws — asymptotic lemma, not a counterexample) |
| 3 L8 (C1′) | dedicated XF check VERIFIED-WITH-AMENDMENTS; patch re-checked | R32_L8_check_sol.md; R37 | item3_L8_falsify (108 designs, 9,504 checks, 0 falsifications) |
| 4 SL0–SL2 + map | PROVED; XF-checked (R34 ERROR-as-written → 9 fixes; core re-derived valid), R38/R39, council | R34_item4_check_sol.md + R34_disposition.md; R38; R39; C1_* | R34_falsify (216 D0 posteriors, 84,096 pairs, 0 violations) |
| 5 consolidated PXN | fidelity FAITHFUL-WITH-FIXES (0/0/4/2), all applied; swept (R39 #1, #4–#8, #10) | R36_item5_fidelity_sol.md; R39 | R39_thmR_numbers (t*, I*, K_n recomputed) |
Input statuses are quoted verbatim in the lemma files (I1 §2 remark, I2 §2, I4 §4); none upgraded.

## 4. Review trail
- Statement lock R30 (Sol high): LOCK-WITH-CHANGES, 8 changes applied → v2 (R30_disposition.md).
- Item checks (fresh Codex Sol xhigh each): R31 SEL V-W-A (0/0/1/2); R32 L8 V-W-A (0/0/2/1); R33 item 1 GAP (0/3/4); R34
  item 4 ERROR-as-written (0/2/7); R35 item 2 V-W-A (0/1/1/1); R36 item 5 fidelity FAITHFUL-WITH-FIXES (0/0/4/2); R37 patch
  re-check V-W-A (0/0/1/1). All findings applied.
- Mid-point R38 (fresh Sol xhigh, statement + proof files only): **CONTINUE** (0/0/4), applied. It re-read the v2 repairs of
  items 1, 2, 4 and the item-3 patches. (Its extra numerics — 280 laws, 2,000 binary64 instances — are reported by R38, not
  reproducible from the package.)
- Citation check: `numerics/citecheck.py` → `reviews/CITECHECK.txt`: 142 path:line citations resolve; 2 short-form and 14 quote
  flags all dispositioned by hand; 0 unresolved.
- Exhaustive sweep R39 (Sol high, whole ticket incl. item 5): 0 FATAL / 1 MAJOR / 8 MINOR / 1 NIT, all fixed.
- Council round 1: **Sol 9.0, Opus 8.7, all gates PASS, no blockers → passed.** Non-blocking items applied afterwards
  (C1_disposition.md; documentation/wording only).
- Helpers: Sonnet 5.5 (item-5 transcription; item-1 numerics). Not used: gpt-6-astra, Fable 5.1.

## 5. Open items and recommended next steps
1. **C-ENG:** implement MR1–MR3 (LS0 centred at and emitting the coded start mode; integration replay N2(c)/ENG02). Until then
   e4′'s integration clauses remain implementation premises.
2. **HQ registry/cards:** apply `patches/` on adoption (P-e4 items 1–19, P-LHiid, P-SEL, P-L8); M5(b1-LH)'s "conditional on N3"
   fallback label becomes unnecessary; GEN (C5)(b) loses its candidate condition; TH163 registry row stays HQ's call.
3. **FP-TAB** (scorer table error η) is untested; needed only if EX-A is to be dropped for the start-mode step.
4. **Song–Liang Theorem S** supplement not obtained (publisher access failed, R38); comparison is with the main-text description.
5. **Pooled shipped-R′ = 4 PIPs:** no in-probability sure-screening theorem exists; the paper should state the stacking routes
   (M1(i)) and the store-restricted route (SL2) as what is proved.
6. W1-PXN's council-added finite-n centring remark should be corrected in any W1-PXN text HQ adopts (Flag 3).

## 6. Files produced (all in `Theory_work/Wave1C/C-PACK/`)
STATEMENT.md (v2), PLAN.md (v2), LOG.md, CHECKPOINT.md, REPORT.md, METHOD_REQUIREMENTS.md, SONG_LIANG_MAP.md (v2);
lemmas/: I1_e4_replacement.md (v2), I2_LHiid_unconditional.md (v2), I4_SL_corollaries.md (v2);
patches/: P_e4_consumers.md, P_GEN_LHiid.md, P_SEL_L6d.md, P_L8_certificate.md;
item5_PXN_consolidated/: 00_statement_and_conventions.md, 01_tools.md, 02_design_events.md, 03_start.md, 04_search.md,
05_posterior_output.md, 06_A_dependence_and_scope.md, INDEX.md, MAP.md, APPLIED_ERRATA.md, OPEN_QUESTIONS.md, selfcheck.txt;
numerics/: item1_um_checks.py/_out.txt, R33_falsify.py/_out.txt, R34_falsify.py/_out.txt (+ R34_song_liang_layout.txt,
R34_SL-*.png), R35_falsify.py/_out.txt, item3_SEL_falsify.py/_out.txt, item3_L8_falsify.py/_out.txt,
R39_thmR_numbers.py/_out.txt, R37_constants.py/.txt, citecheck.py;
reviews/: R30–R39 replies (+ R30, R33, R34, R38 dispositions), C1_council_sol.md, C1_council_opus.md, C1_disposition.md,
COUNCIL_BRIEF.md, CITECHECK.txt, reviewer artefacts R34_citecheck.txt, C1_sol_checks.py/_out.txt, C1_sol_citecheck.txt, C1_sol_snapshot.sha256.
No file outside this folder was edited; no git state was changed.

# Reviewer families outside the council: what each caught (record only)

Mined 2026-11-15, read-only. Builds on `WAVE12.md` and `WAVE3.md` here (their REAL/COSM classes, late-slip rows cited
`W12-T3#n` / `W3-T3#n`, T7 launch counts). Paths are relative to `Theory_work/`. **OAI** = sol/codex (gpt-6.1-sol), astra
(gpt-6-astra); **CL** = Claude (opus, fable; "claude" in W2-FAC-PKA = Opus 5.5, cf. `Wave2/W2-FAC-XA/LOG.md:6`). Model from
the file suffix, else the LOG: W1-N3 Sol (`Wave1/W1-N3/LOG.md:10-24`); W3-START LC1-A/B, LC2-A/B Sol, LC1-C Astra
(`Wave3/W3-START/LOG.md:21,36`); START2 LC1 Sol (`BRIEF_LC1_*_sol.md`); C-ENG Codex (`Wave1C/C-ENG/LOG.md:6,27`); HQ A1 Sol
(`State_of_Project/registry/theory_loop.tsv:11`); A2 Codex, A3 Opus (`Wave1C/HQ_AUDIT/A3_check_A2.md:3`). **A4, B1–B4: model
not recorded** (headers, commits, registry checked). Author family matters for F2: W2-FAC-XA and FAC-PKA had an **OpenAI
lead with Claude reviewers**; C-GROW L6, W2-LOC2 L6_poly, W3-RM SAND-R and W3-RM2 L6 (PV1) were written by **Sol provers**.

## F1. Census

Counts are reply files (scored reviews). Interrupted launches with no file are excluded (see F6). PC1 post-council diffs
are counted under "diff", not under "council". Classification script: one pass over `reviews/` file names.

| layer | W1–W2 sol | W1–W2 astra | W1–W2 opus/claude | W3 sol | W3 astra | W3 opus | W3 fable |
|---|---|---|---|---|---|---|---|
| statement lock / re-lock | 21 | 0 | 3 (XA R01; PKA R01, R03) | 14 | 0 | 0 | 0 |
| lemma line check (incl. item checks, repair re-checks) | 65 | 0 | 7 (C-GROW R06, LOC2 R06a, PKA R02, R04, XA R02b, R03, R04) | 24 | 2 | 2 (RM R04, RM2 LC2-C) | 0 |
| break review | 0 | 0 | 0 | 0 | 2 (START BR1, PSHARP K01) | 0 | 0 |
| mid-point | 17 | 0 | 2 (PKA R05, XA R05) | 0 | 6 | 0 | 0 |
| sweep | 17 | 1 (UNI R05b) | 0 | 2 (POST2 S01, SAMP SW1) | 5 | 0 | 0 |
| better theorem | 0 | 0 | 0 | 0 | 10 | 0 | 0 |
| diff / statement-change / reconciliation / post-council / whole-chain re-check | 1 (FINAL F1 fidelity) | 0 | 0 | 23 | 1 (POST R01) | 1 (POST R02) | 0 |
| council seat (for scale; another helper covers it) | 25 | 2 | 26 | 7 | 9 | 16 | 0 |
| blind audit, HQ audit | A1 sol, A2 codex | 0 | A3 opus | R-AUD1, R-AUD2 (sol) | 0 | acceptance audit 11-12 (opus, record/tool only, `HQD:201`) | API pass1/1b, 2/2b, 3: 251 claims; sharp1/1b: 25 verdicts |
| other | C-ENG 9 (codex) | SR: 2 blind + 1 adjudication | SR: ADJ_opus | pipeline 5, INFRA 2 (sol) | pipeline 2, INFRA 3 | 0 | SR: 1 blind + 1 critique (W2 SR, fable) |
| **non-council maths reviews (lock→diff rows)** | **121** | **1** | **12 (+A3)** | **63** | **26** | **3** | **5 batches** |

Non-council Claude reviews of mathematics: 13 (W1–W2; 10 of them in the two OpenAI-led tickets) and 3 (W3).
Audits A4, B1–B4 (5 reviews) are not in the table: model not recorded.

**Per ticket, launches sol / astra / CL** (council seats included; same file pass): W1-GEN 11/0/1, W1-N1 5/0/1,
W1-N3 7/0/1, W1-PXN 13/0/1, C-DLV 8/0/2, C-ENG 9/0/0, C-GROW 8/0/2, C-MIS 7/0/1, C-PACK 11/0/1, FINAL 4/0/3, W2-APP 10/0/3,
FAC-A 7/0/1, FAC-B 8/0/1, FAC-PK 9/0/2, FAC-PKA 0/0/5, FAC-S5 8/0/2, FAC-S5F 1/0/0, FAC-X 16/1/3, FAC-XA 0/0/5, LOC2 8/0/2,
UNI 5/2/1; W3-POST 0/5/4, POST2 8/3/1, RM 5/5/3, RM2 14/6/2, START 13/6/2, START2 5/0/1, MISR 6/2/2, PSHARP 6/1/2,
SAMP 6/3/1, SCR 7/4/1.

OpenAI launches per ticket (sol + astra):
- (a) full-chain tickets with a new key lemma. Wave 3 (RM 10, RM2 20, START 19, SAMP 9, SCR 11, POST2 11): mean 13.3,
  range 9–20; of which sol mean 8.8, astra mean 4.5. W1/W1C/W2 proof tickets (GEN, N1, N3, PXN, C-DLV, C-GROW, C-MIS,
  C-PACK, APP, FAC-A, FAC-B, FAC-PK, S5, FAC-X, LOC2, UNI): mean 9.0, range 5 (N1) – 17 (FAC-X). All 22: mean 10.2.
- (b) small rider/restatement tickets (START2 5, MISR 8, PSHARP 7, POST 5): mean 6.25, range 5–8; sol mean 4.25,
  astra mean 2.0.
- Claude launches per ticket: 1–4 everywhere except PKA and XA (5 each, all reviews). In Claude-led tickets the Claude
  launch is the council seat, plus at most one non-council review (C-GROW, LOC2, RM, RM2, POST: 1–2).

## F2. Every non-council review by a Claude-family reviewer, and what happened to the same object afterwards

| # | review (model) | object, author | verdict; REAL findings | afterwards, same object |
|---|---|---|---|---|
| 1 | C-GROW R06 (Opus) `Wave1C/C-GROW/reviews/R06_R07_disposition.md:3-5` | L6_random_AR1, Sol prover | VWA A1–A9 "presentation/records only, no gap"; REAL 0 (A4 integration step written out ≈) | parallel Sol R07: VERIFIED, no amendments (`:2`). Sweep R08 Sol: stale prose only (`R08_disposition.md:12`). Fable API: L6.2–L6.7, Cor-L6.8 OK (`API_AUDIT/pass*/VERDICTS.tsv`). **Clean in every later layer** |
| 2 | W2-LOC2 R06a (Opus) `Wave2/W2-LOC2/reviews/R06_disposition.md:2-11` | L6_poly (D3), Sol prover (`W2-LOC2/LOG.md:13`) | VWA, 3 MINOR + 3 NIT: R06a-1 cite + Schur/Neumann steps, R06a-2 D description; REAL ≈0 (R06a-4 not applied) | parallel Sol R06b: VWA, 1 MINOR R06b-1 (τ range, REAL). Sweep R07: no L6 maths. Fable API Thm-Poly, Lemma-BC, Lemma-IR OK. **Clean** (Opus and Sol on the same lemma, in parallel: no shared finding) |
| 3 | HQ A3 (Opus) `Wave1C/HQ_AUDIT/A3_check_A2.md:5` | A2 Prop F-GROW, Codex | VERIFIED-WITH-AMENDMENTS, "no gap and no error" | FINAL council r3 "checked in full", PASS 9.3/8.6 (`Wave1C/FINAL/reviews/C3_disposition.md:28-37`). No later error recorded |
| 4 | W3-RM R04 (Opus) `Wave3/W3-RM/reviews/R04_disposition.md:1-20` | SAND-R, SAND-R′, Sol prover (`W3-RM/LOG.md:32-33,46`) | SAND-R VWA (3 MINOR + NITs), SAND-R′ VERIFIED. REAL: F2 quantifier (proof wording), F3 surplus hypothesis recorded | R07 MP Astra, R08 sweep Astra: "historical wording" only (`R08_disposition.md:26`). Council C1 Opus B5: status line names only one check. Fable API SAND-R, SAND-Rp OK. **Clean** |
| 5 | W3-RM2 LC2-C (Opus) `Wave3/W3-RM2/reviews/LC2_disposition.md:27-38` | L6 examples E1–E5, Sol prover PV1 (`BRIEF_PV1_sol.md`; `BRIEF_LC2C_opus.md:5`) | E1–E3 + table VWA, E4/E5 VERIFIED; 3 MINOR + 3 NIT. REAL: LC2C-3 (E2/E3 status lines must name BC/IR conditions) | **SW1 Astra MAJOR 1** (`SW1_disposition.md:18`; `SW1_sweep_astra.md:10`): STATEMENT §3 has M ∈ (0,1] but E3–E5 use M > 1; hypothesis broadened to M > 0 (= W3-T3#2). **Verified:** the brief gave LC2-C STATEMENT §3 "the hypotheses each example must satisfy" (`BRIEF_LC2C_opus.md:23`), and LC2-C wrote "L6's M = Cs₀θ_hi² + 1 is valid" (`LC2C_L6_check_opus.md:134-135`) without testing it against M ≤ 1. Later still: Ex-PolyR/Ex-PolyF NOT-EXAMINED in the opus seat addendum (`C_R1_council_opus.md:198-199`), recorded unchecked (`HQD:245`) |
| 6 | W3-POST R02 (Opus) `Wave3/W3-POST/reviews/R02_disposition.md` | whole chain, Claude lead | 0/0/4 MINOR/7 NIT; REAL 4 (F1–F4) | Astra council C1 FAILED on literature faithfulness both R01 and R02 had passed (YWJ rate, NH14, Song–Liang qualifications; `C1_disposition.md:9`, `WAVE3.md:131`). Opus C3 seat: a REPORT sentence false without ε-independence (`C3_council_opus.md:244-250`). See F3(a) |
| 7 | W2-FAC-XA R01, R02b, R03, R04, R05 (Opus) `Wave2/W2-FAC-XA/reviews/R0*_disposition.md` | OpenAI lead | R01 LOCK-WITH-CHANGES, 12 required (one: absolute √(p/n) operator-norm bound false, `R01_statement_lock.md:23,38`); R02b PASS-WITH-FIXES F1–F6; R03 M1–M3; R04 ACCEPT WITH REQUIRED FIXES (F3-3 sign case split); R05 CONTINUE. REAL ≈18 (WAVE12:117) | No OpenAI review of these objects afterwards. Fable API pass 3: XA:L2 and XA:L8-S MINOR, rest OK (`pass3/TRIAGE.md:9`). Stopped by SR |
| 8 | W2-FAC-PKA R01–R05 (Claude) `Wave2/W2-FAC-PKA/reviews/R0*_disposition.md` | OpenAI lead | R01 12 fixes (FAC-B items false for p > K; E5–E7, B3 false for the retained set; rank sentence false, `R01_statement_lock_claude.md:19,74,85`); R02 L0/L1 VERIFIED, numerics INADEQUATE; R03 R1–R5 (D_n > 0 false for s₀ = 1, `R03_…:111`); R04 VWA; R05 CONTINUE | No OpenAI review afterwards. Fable pass 3: PKA:L4 MINOR (L4 never reviewed; R06 gave no verdict). Stopped by SR |
| 9 | Wave 2 SR: BLIND_fable, CRITIQUE_fable (Fable), ADJ_opus (Opus) `Wave2/SR/` | programme strategy | regime drift (≈2/3 of W2 off the paper's regime), stop list of 6 tickets (`CRITIQUE_fable.md:23-26,291-292`); ADJ_opus: re-check the unreviewed T03♯ spine (`ADJ_opus.md:17`) | Stop list adopted. The spine re-check became W3-POST (R01 Astra / R02 Opus). The Astra adjudicator also ran (`ADJ_astra.md:3`); no later reversal recorded |
| 10 | API audit pass 1/1b (Fable, blind) `API_AUDIT/pass1/TRIAGE.md:20-40` | 109 PROVED-CHECKED claims (passed OAI line checks + councils) | 87 OK, 21 MINOR, 1 GAP (C-DLV:Prop-F) | Sol R-AUD1: CONFIRMED-WORDING, not a gap (`pass1/R-AUD1_sol.md:3`). MINORs batched for an editorial pass; see F3(b) |
| 11 | API audit pass 2/2b (Fable) `pass2/TRIAGE.md` | 92 author-only PROVED claims | 79 OK, 13 MINOR, 0 GAP | no OAI follow-up |
| 12 | API audit pass 3 (Fable) `pass3/TRIAGE.md` | 50 author-only claims of stopped W2 tickets | 42 OK, 5 MINOR, 3 GAP | Sol R-AUD2 confirmed all 3 GAP claims (4 findings CONFIRMED, 1 CONFIRMED-WORDING; `R-AUD2_sol.md:10-15`) → 3 lemmas SUSPECT |
| 13 | sharp1/1b (Fable) `sharp1/TRIAGE.md:13-22` | 25 headline claims | all IMPROVABLE-EASY; triage (Fable consultant): "not 13 findings"; 8 of 13 mostly class B | class A C-MIS fixed-variance removal → ticket W3-MISR (`WAVE12.md:133`) |

Summary: of the 6 Claude-family line/whole-chain checks in Claude-led tickets (#1–#6), one object later got a REAL
error from an OpenAI reviewer that the Claude reviewer had passed (#5, RM2 L6/§3 glue). One more passed literature
faithfulness that the Astra council seat then failed, but so had the Astra re-check (#6). #1–#4 stayed clean in every
later layer; in #1 and #2 a Sol check ran in parallel and was also clean.

## F3. Direct paired comparisons

**(a) W3-POST R01 (Astra) vs R02 (Opus).** Same brief, launched together, independent (`W3-POST/LOG.md:9-10,17,20`;
`R01_disposition.md:7-12`, `R02_disposition.md:7-19`).

| | Astra R01 | Opus R02 |
|---|---|---|
| counts | 0/0/4 MINOR | 0/0/4 MINOR/7 NIT |
| REAL | 4: R01-1 E2(ii) cutoff display false for ω = −100 (restrictions restored); R01-2 ridge-bias remark false (exact formula); R01-3 constant missing +1/log 2; R01-4 positivity/hypotheses explicit | 4: F1 L1a′ headline needs ‖Xθ*‖² ≤ nM; F2 floors overclaimed vs Song–Liang; F3 item 5(a) mis-titled; F4 item 6 claims split |
| shared | R01-1 ≈ F5 (NIT), R01-4 ≈ F8 (NIT) | same 2 |
| unique REAL | R01-2, R01-3 (+ the substance of R01-1, R01-4) | F1–F4 |
| "false as written" | 2 (R01-1, R01-2) | 0 |
| missed by both, caught later | literature: YWJ/NH14/Song–Liang (Astra council C1, 2 MAJOR); LB domain in REPORT (Astra C2) | same |

**(b) Fable blind API audit of OAI-passed claims.** Ten pass-1 MINORs, each read against the cited text:

| # | claim, finding (result file) | in the text? |
|---|---|---|
| 1 | W1-N1 Thm-N1 #3: invariance cited as "N9 rows 1–6", KERNEL covers rows 1–5 (`pass1/results/f01.md:44`) | real slip: `Wave1/W1-N1/lemmas/L2_post_terminal.md:20` vs `STATEMENT.md:76-77` (citation) |
| 2 | C-DLV L1-R #3: archive count (2(ℓ+1)+3)(ℓ+1)K ≤ K(ℓ+3)² false for large ℓ (`f04.md:33`) | real: `C-DLV/lemmas/L1_resources.md:90-91`; (2ℓ+5)(ℓ+1) > (ℓ+3)² for ℓ ≥ 2; absorbed by C_M |
| 3 | C-GROW L3: header omits \|Q\| ≤ K used at line 78 (`f13.md:40`) | real: `C-GROW/lemmas/L3_sandwich.md:6-7` vs `:78` |
| 4 | W2-APP: summary cells "per FAC (pending)" stale (`f15.md:59`) | real: `W2-APP/lemmas/L4_families.md:167-168` vs `:148-149` |
| 5 | W2-APP REPORT: φ²(8) bracket, the table's witness is k = 7 (`f15.md:63`) | real: `W2-APP/REPORT.md:99` vs `EMPIRICAL.md:24,33` |
| 6 | W2-FAC-S5 L4: n₀ omits its dependence on the sequence (p_n) (`f24.md:50`) | real: `W2-FAC-S5/lemmas/L4_path.md:16` (limsup hypothesis) |
| 7 | W2-UNI: energy constant M := s₀θ_hi², derived bound gives s₀²θ_hi² (`f27.md:69`) | real: `W2-UNI/lemmas/L4_k1.md:40` vs `:57`; the θ = (1,1), ρ = .99 example checks (3.98 > 2) |
| 8 | W3-RM Form R p = 1: "H_A = n²" vs displayed Q_A (normaliser n) (`f32.md:52`) | real internal inconsistency: `W3-RM/lemmas/L4_formR.md:53` |
| 9 | W3-SAMP: T ≤ 4·max(1000, ℓ²) needs tier e ≤ 1, unstated (`f33.md:39`) | real (unstated condition): `W3-SAMP/lemmas/CC_code_check.md:95-99` |
| 10 | W3-SCR: "SCR-A … special case" though SCR-M carries 4e^{−x}, SCR-A 3e^{−x} (`f35.md:49`) | real (wording): `W3-SCR/STATEMENT.md:122-123` vs `:80,:115` |

All 10 are real local slips in text that had passed OAI line checks (and councils); none changes a claim, as Fable said.
GAP precision: 4 GAP claims in 251 audited. Sol confirmed 3 (pass 3: S5F L0, S5F L1, FAC-X L4r.5; 4 of 5 findings
CONFIRMED) and downgraded 1 (pass 1 C-DLV:Prop-F → wording). All 3 confirmed GAPs were in lemmas no reviewer had line-checked
(`WAVE12.md:222-223`). On claims that had passed OAI line checks: 1 GAP call, 0 confirmed.

**(c) Late catches (REAL MAJOR+, from both T3 tables) with the reviewer family of the earlier pass and of the finder.**

| earlier pass ↓ / finder → | sol | astra | opus | fable (Sol-confirmed) |
|---|---|---|---|---|
| OAI only, same model (sol) | 14: W12-T3#1,2,3,8,9,10,13(F1→council),15,16,17,18,20; W3-T3#4,8 | – | (1 of 5 in W12-T3#13: Opus O1) | – |
| OAI only, other OAI model in the chain | 1: W3-T3#5 (sol LC2 + astra MP1 → sol SW1) | 3: W3-T3#3, #6, #7 (sol → astra) | – | – |
| both families | 6: W12-T3#4, 5, 11, 12, 14; W3-T3#1 | 1: W3-T3#2 (sol locks + **opus LC2-C** → astra SW1) | – | – |
| none (never checked) | 3: W12-T3#6, 7, 19 | – | – | 2: W12-T3#21, 22 |

Finders of the 30 rows: OAI 28 (sol 24, astra 4; Opus also in #13), Fable 2; all fresh agents. Of the 25 rows with an
earlier pass, the finder's model had already passed the object in 21 (all sol), a different OAI model found it in 4 (astra
after sol), a different family in 0. Non-MAJOR REAL catches by the Opus council seat on OAI-checked objects: SAMP C1 #1–#3,
SCR C1 Opus 1, POST2 C1 B-5, RM C2 B1 (`WAVE3.md:182-190`; seat B = Opus, `W3-POST2/reviews/C1_disposition.md:4`).

**(d) Sol vs Astra on the same content.**

| content | Sol | Astra | overlap / note |
|---|---|---|---|
| W2-UNI sweep: R05a Sol (xhigh, v1.1.1) then R05b Astra (v1.1.2, after R05a fixes; not parallel) `Wave2/W2-UNI/reviews/R05a_disposition.md:1-8`, `R05b_disposition.md:1-6` | 1 MAJOR (FAC-L containment needs fixed beta-min) + 14 MINOR + 3 NIT; incl. a wrong Ψ formula (#8) | 0 MAJOR, 10 MINOR, 3 NIT: REPORT overclaims (#1–#4), numerics (#5–#8, a wrong 95/100 count), tooling (#9–#10) | no shared finding; both found citecheck-resolver defects (Astra after Sol's fix) |
| POST2 K2 (Sol) ∥ M01 (Astra) | K2-1 | M01-1 | same finding, parallel (`WAVE3.md:38`) |
| SAMP LC2 (Sol) ∥ MP1 (Astra) | #1, #3 | #1, #3 | 2 shared, parallel (`WAVE3.md:95`) |
| SCR R05b (Sol) ∥ R06 (Astra) | N1 STATEMENT M3 omission (counterexample) | same | shared, parallel (`W3-SCR/reviews/R05_disposition.md:26`) |
| Pipeline, commit eb1f9da: R02 Astra blind ∥ R02 Sol reconciliation `Wave3/PIPELINE_REVIEW/` | 17 per-finding verdicts: 11 PARTIALLY-RESOLVED (R01–R11, Sol-1–6) | 9 new findings (F1, F7 CRITICAL; F2–F6, F8 MAJOR; F9 MINOR) | F2 ≈ R05 and F3 ≈ R04 residuals (fix commit `d6da494` message); F8 ≈ R11 (`R03_reconciliation_sol.md:141`) |
| Pipeline toolfix2 (fixes of Astra F1/F2/F6/R10 and Sol-4): Sol review | 6 breaks reproduced, 1 CRITICAL (`R02_toolfix2_review_sol.md:26-122`) | – | Sol broke 4 fixes made for Astra findings |
| INFRA tools: Astra R01–R03, then Sol R04–R05 `INFRA/reviews/R0*_disposition.md` | R04: 3 MAJOR + 1 MINOR (Job-object race and whole-token status_at, both in fixes from Astra rounds); R05: 5 MAJOR + 1 MINOR | R01 17, R02 12, R03 items incl. "partly" re-raises of own F2, F5/F6, F8, F10 | Sol found new bypasses after three Astra rounds |

## F4. What OAI reviewers caught in Claude-written proofs, and Claude-family "false" verdicts

**OAI, lock and line-check layers.** WAVE12 counts ≈23 failed-as-written lemma verdicts and ≥12 false claims at lock
(`WAVE12.md:139-141`); Wave 3 adds the rows below. Method: A = analytic (explicit construction or argument in the review),
S = the reviewer's own script found it, S+ = analytic and confirmed by the reviewer's script, C = code/spec reading.

| ticket: verdict (reviewer) | method | pointer |
|---|---|---|
| W1-GEN R01 #2 W counter-instance; L6(d) GAP, L7 GAP ×2 (sol); W1-N1 LC1 L1 GAP (codex) | A | `WAVE12.md:19-20,26` |
| W1-N3 R02 L1 GAP; L5 WRONG, counterexample p = 2 on the frozen harness (sol) | A; **S** | `Wave1/W1-N3/reviews/R02_batch1_check.md:6,10` |
| W1-PXN R13, R14, R15 ×2, R17 ERROR; R16 GAP; R30 ERROR (codex) | A | `R14_I4_TheoremR_codex.md:3`, `R30_sweep_codex.md:5` |
| C-DLV R01 FATAL (codex); R03 Cor 5.3 ERROR, three-model counterexample (codex) | A; **S+** | `R03_L3L5_codex.md:25,162` |
| C-GROW R01 #1 counterexample to C5(b), R04 \|Q\| bound; C-MIS R03 O2 FALSE, R04 singleton counterexample, R05 parenthesis FALSE (sol) | A (GROW R04 numerics "support only") | `C-GROW/r/R01_…:96`, `R04_…:102`; `C-MIS/r/R04_…:11`, `R05_…:26` |
| W2-APP R05 L4 FALSE as written (sol) | A | `Wave2/W2-APP/reviews/R05_L4_check_sol.md:1,9` |
| W2-FAC-B R01 false swap margin, asymptotic counterexample p = 3 (sol); R03–R05 reversed inequality, false small-p bound | A (uses the method's block size from the method text) | `Wave2/W2-FAC-B/reviews/R01_statement_lock_sol.md:11-17` |
| W2-FAC-PK R01, S5F R01, FAC-X R01 (X3), R03 X3, R12 X7(G), LOC2 R01 (LSF), UNI R01, S5 R02 L1 (all sol) | A | `WAVE12.md:87-125` |
| W3-POST R01-1, R01-2 false display/remark (astra); R03 §5A item-5 counterexample (astra) | A (§5A sketch; Opus C1 later confirmed it by its own script) | `W3-POST/reviews/R01_disposition.md:9-10`; `C1_council_opus.md:16-17` |
| W3-START SL1 4 CRITICAL (sol), BR1 CRITICAL (astra), SW1 M1 (astra); RM2 SW1 M1, RM R08 M4 (astra) | A | `W3-START/r/SL1_…:6-24`, `BR1_…:8`; `W3-RM2/r/SW1_…:10` |
| W3-SCR R01 BLOCKER (sol); R04 ω-only remark refuted (sol); R05b N1 deterministic counterexample (sol) | A; **S** (`R04_scratch/remark_counterexample.py`); A | `R01_statement_lock_sol.md:5`; `W3-SCR/reviews/R05b_relock_v31_sol.md:30` |
| W3-POST2 PC1: false inequality at p = K = 2 (sol) | A | `PC1_postcouncil_diff_sol.md:22,44` |
| W3-SAMP SW1 M1 (HPM not a function of island records), M2 (example not a realisation of the coded target) (sol) | **C** | `SW1_sweep_sol.md:5-7` |

Tally: analytic in nearly all; found by the reviewer's script 2 (W1-N3 L5, SCR R04); script-confirmed 2 (C-DLV Cor 5.3;
POST §5A, by the Opus seat); code/spec reading 2 (SAMP SW1 M1, M2), plus W2-APP council r1 (`WAVE12.md:167`).

**Claude-family counterexamples or "false as written" verdicts in the record.**

| review (model) | target | kind | pointer |
|---|---|---|---|
| W2-FAC-XA R01 (Opus) | OpenAI lead's plan claim: absolute √(p/n) operator-norm bound | false, analytic (§A) | `Wave2/W2-FAC-XA/reviews/R01_statement_lock.md:23,38` |
| W2-FAC-PKA R01, R03 (Claude) | OpenAI lead's statements: FAC-B items for p > K; E5–E7, B3 for the retained set; rank sentence; D_n > 0 | false (analytic, explicit constructions; D_n ≡ 0 at s₀ = 1) | `R01_statement_lock_claude.md:19,74,85`; `R03_…:111` |
| W3-RM R04 (Opus) | Sol prover's wording "never condition on the scales" | literally false (wording) | `W3-RM/reviews/R04_disposition.md` F1 |
| C-DLV C1 seat (Opus) | n_β endpoint "(β) impossible for n ≤ 2.28·10⁸" | false at the endpoint (editorial) | `Wave1C/C-DLV/reviews/C1_council_opus.md:143-148` |
| W2-APP C2, C3 seats (Opus) | "unproved" label outside ENUM; EMPIRICAL "every pair > 0.7" | counterexample to the label (own script); false as written | `Wave2/W2-APP/reviews/C2_council_opus.md:76-84`; `C3_…:108` |
| W2-FAC-X R20 seat (Opus) | (C2)(ii) uniform form beyond ½; REPORT attribution of the ½ | false, own exact check | `Wave2/W2-FAC-X/reviews/R20_council_opus.md:28-33` |
| W3-POST C3 seat (Opus) | REPORT sentence omitting ε-independence | false, explicit p = 2 counterexample | `W3-POST/reviews/C3_council_opus.md:244-250` |
| W3-PSHARP R1 seat (Opus) | registry label NECESSARY | overclaim → FAILED-REMOVAL | `W3-PSHARP/reviews/R1_council_opus.md:155-163` |
| W3-SAMP C1 seat (Opus) #3, #2 | TR-b proof step; D's premise list | proof slip; missing premise | `WAVE3.md:183-185` |
| C-GROW R10 seat (Opus) F1 | fixed-p instances fall to exact enumeration (code reading) | recorded as wording | `WAVE12.md:57` |

No Claude-family reviewer produced a counterexample or "false as written" verdict against a **lemma proof** of a Claude
lead. Their "false" verdicts hit OpenAI-led statements and plans at lock (XA, PKA), REPORT sentences, labels, side remarks
and one proof step at council (SAMP #3). Their line checks of Sol-written lemmas (F2 #1, #2, #4, #5) found nothing false.

## F5. Session reuse and relaxed freshness

**Continuation of a reviewer session: none found** (scoped `LOG.md`s, `HQ_DECISIONS.md`, briefs, pipeline/INFRA folders
searched for "same thread/reviewer/session", "resume the reviewer", "t3_thread_send", "re-ask", "follow-up to", "your
earlier review"). `t3_thread_send` occurs only for a simulation request (`Wave2/W2-FAC-PKA/LOG.md:17`).

**Informed re-checks (same model, earlier findings given; thread not recorded):**

| case | given earlier material | found |
|---|---|---|
| INFRA R05FIX Sol re-check (outside the listed folders) | "Your earlier review is … read it" (`INFRA/R05FIX/BRIEF_sol_recheck.md:6`) | B1, B2 RESOLVED; no new findings (`INFRA/R05FIX/REPORT.md:91`) |
| Pipeline R02, R03, R04 Sol reconciliations (rule 15: separate reconciliation reviewer) | the earlier findings, per finding | R02: 11 PARTIALLY-RESOLVED; R03: NOT-READY, new N1–N5 incl. CRITICAL N2 (`R03_reconciliation_sol.md:3,59-141`); R04: READY, 2 new MAJOR |
| INFRA R02, R03 (Astra after Astra) | earlier dispositions (the R03 disposition lists "F2 (partly)", "F5/F6 (partly)" …) | partial fixes of its own findings re-raised; then Sol R04 found 3 new MAJOR |

**Freshness or blindness knowingly relaxed:**

| case | relaxation | outcome |
|---|---|---|
| Seat addenda, 2026-11-12 (`HQD:208`; `ACCEPTANCE/ADDENDUM_BRIEF.md:3-6`) | same seat model, fresh thread, frozen manifest + own earlier review; ACCEPT / NOT-EXAMINED only | 9 addenda (START R2 ×2, START2 ×2, MISR R2 ×2, PSHARP R2 ×2, RM2 opus + astra): 98 ACCEPT, 2 NOT-EXAMINED (RM2 Ex-PolyR, Ex-PolyF, opus seat) → recorded unchecked (`HQD:245`) |
| W3-POST layer substitution (`HQD:3`) | SL/LC/MP/SW replaced by two whole-chain re-checks, ruled after the fact | council needed 3 rounds (Astra seat FAILED C1, C2 on literature/REPORT) |
| W3-MISR mid-point waived at CP2 (`HQD:181-185`) | layer dropped | sweep after the council caused a re-round (`WAVE3.md:163`) |
| Wave 2 SR blind proposals (`Wave2/SR/BRIEF_ADJUDICATION.md:5`) | BLIND_astra scope-contaminated (disclosed, `BLIND_astra.md:5`); BLIND_astra2 exposed through a permitted file (`BLIND_astra2.md:3`) | both used by the adjudicators, labelled |
| W2-UNI R05b Astra sweep | ran on text already fixed after R05a (not a parallel blind pair) | 13 new, none shared (F3(d)) |

**Repair re-checks: same model as the finder vs a different one, and later errors in the repair.**

| repair (finder → re-checker) | same model? | later error in the repair or its consequence? |
|---|---|---|
| W1-PXN errata E-1..E-20 (sol R13–R17 → sol R21, "different from the finder" = another agent, `Wave1/W1-PXN/LOG.md:51`) | yes | **yes**: R30 sol ERROR on the repaired lines (W12-T3#1) |
| W1-GEN L7 (sol R06 → R08, R09); W1-N3 L1, L5 (sol R02 → R03); W2-FAC-X X3 (sol R03 → R03b) | yes | no |
| C-DLV L1, sweep fix (codex R02 → "folded into the sweep", codex) | yes | **yes**: council codex 2 MAJOR in the CONFIG fix (W12-T3#7, #8) |
| W2-FAC-B statement (sol R01 REJECT → sol R02 relock) | yes | **yes**: sweep R07 sol 2 MAJOR (W12-T3#17) |
| W2-FAC-S5 L1 (sol R02 → sol R03) | yes | **adjacent**: sweep MAJOR on L3, edited in the same repair round (W12-T3#18) |
| W3-START SL1/SL2 fixes (sol → sol RC2) | yes | **yes**: BR1 astra CRITICAL, (B-R) vs the "p > s₀" added at SL1 (W3-T3#7) |
| W3-RM2 SL1 fixes (sol → sol RC1, RC2) | yes | **yes (glue)**: SW1 astra M1 on §3's M range (W3-T3#2) |
| W3-SCR R05 fixes (sol → sol R05b) | yes | R05b itself found N1 that R05 passed; later Opus council 1 (κ, b, M fixed) on v3.4 |
| W3-POST2 PC1 (sol → sol PC2); W3-SAMP PC1 (sol → sol PC2); W3-PSHARP R1 (sol → sol R2 reconciliation) | yes | no |
| W3-RM2 MP1, SW1 fixes (astra → sol RC4, RC6) | no | no (council: no REQUIRED; PC1 clean) |
| Pipeline/INFRA fixes of Astra findings (astra → sol) | no | **yes**: Sol toolfix2 review broke 4; INFRA R04 found bypasses in Astra-round fixes |

Same-model re-checks: 13 repairs, 6 with a later error in or next to the repair (found by sol 4: PXN, C-DLV, FAC-B, S5;
by astra 2: START, RM2). Different-model re-checks: 2 rows; in the tool reviews the later model found broken repairs.

## F6. Reviewer failures

| kind | case (model) | pointer |
|---|---|---|
| no output, OAI (7, all infrastructure) | W3-START LC1 ×3 (sol, sol, astra) and SC5 ×2 (sol) cancelled by handoffs/restarts; W3-SAMP SW1 (sol) restart; W2-LOC2 R04 (sol) ECONNRESET | `W3-START/LOG.md:20,43-44`; `W3-SAMP/LOG.md:45-51`; `Wave2/W2-LOC2/LOG.md:13` |
| no output, Claude seats (2) | W3-MISR R1 opus (rate limit, relaunched); W2-FAC-X R18 opus (pause; T2 council never completed) | `W3-MISR/LOG.md:65-68`; `WAVE12.md:115` |
| returned early, no review | W2-FAC-XA R02 (Opus): "script still running", no file → fresh R02b | `Wave2/W2-FAC-XA/reviews/R02_incomplete_reply.md:3-6` |
| returned early, no review | W2-FAC-PKA R06 (Claude): interim message; L3/L4 stayed unchecked | `Wave2/W2-FAC-PKA/reviews/R06_interim_message.md:3-6` |
| output limit (Fable) | pass 1: 3 requests at max_tokens 64k → pass1b; pass 2 f00 → pass2b; sharp1: 13 verdicts of 22 requests, sharp1b 12 (f20 partial) | `API_AUDIT/pass1/TRIAGE.md:11`; `pass2/TRIAGE.md:11`; `sharp1b/TRIAGE.md:1-4` |
| file-rule breach | W3-RM C1 opus seat ran citecheck.py, rewriting CITECHECK.txt | `W3-RM/reviews/C1_disposition.md:24` |
| blindness breach | Wave 2 SR BLIND_astra, BLIND_astra2 (astra), disclosed | `Wave2/SR/BLIND_astra.md:5`; `BLIND_astra2.md:3` |
| wrong, overturned | Fable pass-1 GAP C-DLV:Prop-F → Sol CONFIRMED-WORDING; Fable pass-3 L4r.5 F2 → CONFIRMED-WORDING | `pass1/R-AUD1_sol.md:3`; `pass3/R-AUD2_sol.md:15` |
| wrong, rejected with evidence | W2-FAC-PK council opus optional 4 (G2 via \|T\| ≤ K ≤ n/2), refuted by the Sol seat's counterexample; W2-FAC-PKA R01 S1 (Claude) arrival/scoring equivalence ("scoring a neighbor does not imply choosing it") | `Wave2/W2-FAC-PK/reviews/R08_R09_disposition.md:13-16`; `W2-FAC-PKA/reviews/R01_disposition.md:5` |
| objection stood (scope, not maths) | W1-N1 SL1 #3 Lean requirement (codex) | `Wave1/W1-N1/reviews/SL1_disposition.md:10` |
| lead's rejection overturned (reviewer was right) | C-MIS R02 onset remark (sol), upheld by sweep R06 (sol) | `WAVE12.md:209` |
| VERIFIED, later overturned (non-council) | sol: W1-PXN R21 and R12, W2-FAC-S5 R02 (L3), START LC2-B (OVL), SAMP LC1 (PC), SCR R05 (M3), RM R03 (L2_NAF, ≈); astra: POST R01 fidelity; opus: RM2 LC2-C (L6/§3), POST R02 fidelity | W12-T3#1,2,18; W3-T3#2,3,4,6,8; F3(a) |

Tally of "VERIFIED later overturned" outside councils: sol 7, astra 1, opus 2, against ≈184 sol, 27 astra and 16 Claude
non-council maths reviews (F1).

## What the numbers say

1. Outside councils, OAI ran ≈211 maths reviews (sol ≈184, astra 27, 10 of them better-theorem); Claude ran 16, 10 of them in the two OpenAI-led tickets.
2. OAI launches per full-chain ticket: mean 9.0 (W1–W2, 5–17) and 13.3 (W3, 9–20); per small rider ticket 6.25 (5–8).
3. Opus line checks of Sol-written lemmas: 4. Three stayed clean in every later layer; RM2 L6 then got Astra SW1 MAJOR 1, which LC2-C had passed (`LC2C_L6_check_opus.md:134-135`).
4. POST R01 (Astra) vs R02 (Opus): 4 REAL each, 2 shared at NIT level. Astra had 2 "false as written", Opus 0. Both missed the literature issues the Astra council seat failed.
5. Fable's blind audit of 109 claims that had passed OAI review: 21 MINOR, 1 GAP (downgraded). 10 of 10 sampled MINORs are real text slips, none affecting a claim.
6. Fable GAP calls: 3 of 4 confirmed by Sol, all in never-line-checked lemmas.
7. Late MAJOR catches: 28 of 30 by OAI (24 sol), 2 by Fable. In 21 of 25 the finder's model had already passed the object (fresh agent); 4 were astra after sol; 0 came from the other family.
8. Counterexamples against Claude-lead lemmas came only from OAI reviewers, mostly analytic: 2 found by the reviewer's own script, 2 by code reading.
9. Claude "false" verdicts: at the XA/PKA locks (OpenAI-written statements), and at councils on REPORT text, labels and one proof slip. None against a Claude lead's lemma.
10. No reviewer session was continued in the record. Same-model repair re-checks: 6 of 13 had a later error in or next to the repair. No usable output: OAI 7 (all infrastructure), Claude 4 (2 seats cut off, 2 returned early), Fable 3 batches at token limits.

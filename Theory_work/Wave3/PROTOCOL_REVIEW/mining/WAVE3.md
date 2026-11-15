# Wave 3 review-trail mining (record only)

Scope: W3-POST, POST2, RM, RM2, START, START2, MISR, PSHARP, SAMP, SCR. Mined 2026-11-15, read-only.

**Sources.** Working tree on `main`. For MISR, PSHARP, RM2, START and START2, the `origin/theory/<T>` ticket folders were
extracted with `git archive` and compared: they are identical to the working tree, except that START2's branch `LOG.md`
has one later entry (the HQ CP2 decision, 2026-11-12 15:10). That branch LOG was used. Cross-ticket facts come from
`Wave3/HQ_DECISIONS.md` (cited as `HQD:<line>`) and from `Wave3/API_AUDIT/pass*/VERDICTS.tsv`. All paths below are
relative to `Theory_work/Wave3/`. `T/r/` means `W3-T/reviews/`.

**Classification rules (mine; applied per disposition row).**
- **REAL**: the finding changed a statement, a hypothesis, a proof step, or a status label. Status labels include the
  necessity/sharpness labels in ASSUMPTION_MAP and SHARPNESS, and any "proved"/"verified" claims.
- **COSMETIC**: wording, notation, record-keeping, citation format, registry pointers. This also covers fixes to the
  numerics evidence (wrong labels, experiments run outside the assumptions, script bugs); those are marked `num`.
- **RE-RAISED**: the finding was already raised by an earlier layer or round. Parallel duplicates (two reviews running
  at the same time) are marked `par`.
- **REJ**: the lead objected with evidence and the objection stood.
- **oth**: deferred, moot, or recorded with no change. Frozen-content items that were never applied also go here.

Severities are as the reviewer labelled them: C = CRITICAL/FATAL/BLOCKER, M = MAJOR, m = MINOR, n = NIT/NOTE/EXPOSITION.
"req/opt" = required/optional, used where a reviewer gave no severity. "NB" = non-blocking with no severity label.
"≈" marks counts where a single disposition row mixes classes, or where seats are merged.

## T1. Yield per layer, per ticket

| ticket | layer | n | C/M/m/n | REAL | COS | RE-RAISED | REJ | oth | disposition used |
|---|---|---|---|---|---|---|---|---|---|
| POST | whole-chain re-checks R01+R02 (replaced SL/LC/MP/SW, HQD:3) | 2 | 0/0/8/7 | 8 | 3 | 2 (F5, F8 = R01-1, R01-4) | 0 | 2 recorded | `POST/r/R01_disposition.md`, `R02_disposition.md` |
| POST | falsification numerics | – | – | numerics E5 + R03 §5A turned STATEMENT item 5 into "False in general" (`POST/LOG.md:19`); `lb_check`: 34,920 cases, 0 fail | | | | | `POST/LOG.md:11-19,28` |
| POST | better theorem R03 | 1 | proposals | → follow-up ticket W3-POST2 (HQD:8) | | | | | `REPORT.md` §4 |
| POST | council C1 | 2 | 0/2/10/8 | 9 | 11 (2 num) | 0 | 0 | 0 | `POST/r/C1_disposition.md` |
| POST | council C2 | 2 | 0/1/2/10 | 1 | 11 | 1 (A-F2 NH14, after C1 A-F2) | 0 | 0 | `POST/r/C2_disposition.md` |
| POST | council C3 | 2 | 0/0/2/10 | 0 | 11 | ≈1 (B-F1 REPORT conditions, the same class as C1 A-F4) | 0 | 1 (B-N8 not applied) | `POST/r/C3_disposition.md` |
| POST2 | statement lock L01 | 1 | 0/3/2/1 | ≈6 | 0 | 0 | 0 | 0 | `POST2/r/L01_disposition.md` |
| POST2 | falsification numerics | – | – | no refutation; first-run labels were wrong (`POST2/LOG.md:12`); S01 #2 found wrong Occam weights in the numerics | | | | | `POST2/LOG.md:12,36` |
| POST2 | better theorem R03b | 1 | 7 proposals | 3 adopted (C+, D+, E1 ridge form) | | | | 5 recorded → `better:PENDING` (HQD:24) | `POST2/r/R03b_disposition.md` |
| POST2 | line checks K-AE, K-BC, K-D, K2 | 4 | 0/2/10/4 | 8 | 5 | 1 par (K2-1 = M01-1) | 0 | 2 moot (C v1 superseded) | `K_AE_`, `K_BC_`, `K_D_`, `K2_disposition.md` |
| POST2 | mid-point M01 | 1 | 0/0/2/1 | 2 | 1 | 0 | 0 | 0 | `POST2/r/M01_disposition.md` |
| POST2 | sweep S01 | 1 | 0/2/13/2 | 6 | 10 (6 num) | 1 (#10 LB domain dropped = W3-POST C2 A-F1, another ticket) | 0 | 0 | `POST2/r/S01_disposition.md` |
| POST2 | council C1 | 2 | 0/0/7/8 | ≈5 (A-2, B-4, B-5, B-7, B-10) | ≈10 | 0 | 0 | 0 | `POST2/r/C1_disposition.md` (merged seat rows) |
| POST2 | post-council PC1, PC2 | 2 | PC1: 3 findings (P1 "required repair") | 3 (P1 false inequality; P2, P3 status propagation) | 0 | 0 | 0 | PC2: 0 new | `POST2/r/PC1_postcouncil_diff_sol.md:44-56`, `PC2_repair_check_sol.md:48` |
| RM | statement lock R01 | 1 | 5 req / 4 opt | 7 | 1 | 0 | 0 | 1 (moved to the numerics plan) | `RM/r/R01_disposition.md` |
| RM | falsification numerics | – | – | `f1_naf_check`: 0 violations in 60 runs; R05 reviewer: 84,000 calls, 0 failures; no refutation | | | | | `RM/LOG.md:36,51` |
| RM | better theorem R02 | 1 | 8 proposals | 4 adopted (P1 Form F only, P2, P3a, P7) | | | | P5 → follow-up ticket W3-RM2; P3b, P4 recommended; P6 open | `RM/r/R02_disposition.md` |
| RM | line checks R03, R04, R05, R06 | 4 | 0/4/10/10 | 9 | 10 | 0 | 0 | 5 recorded | `R03_R05_`, `R04_`, `R06_disposition.md` |
| RM | mid-point R07 | 1 | 0/0/3/1 | 2 | 2 | 0 | 0 | 0 | `RM/r/R07_disposition.md` |
| RM | sweep R08 | 1 | 0/6/11/4 | 12 | 9 | 0 | 0 | 0 | `RM/r/R08_disposition.md` |
| RM | council C1 | 2 | 0/1/4/6 | ≈2 (B-2, B-6 status wording) | ≈9 (A-1 num) | 0 | 0 | 0 | `RM/r/C1_disposition.md` |
| RM | council C2 | 2 | 0/0/1/7 | 2 (B1 proof argument by cases; B4 bridge premise, per PC1) | 6 | 0 | 0 | 0 | `RM/r/C2_disposition.md`; `PC1_…:70-79` |
| RM | post-council PC1 | 1 | CLEAN | 0 | – | – | – | 4 record issues | `RM/r/PC1_postcouncil_diff_sol.md:77-79`; HQD:30-32 |
| RM2 | statement lock SL1 + RC1 + RC2 | 3 | SL1 0/2/4 + 4 opt; RC1 0/1/1 | 7 | 4 | 1 (RC1 R4 = SL1 #4, partly resolved) | 0 | 0 | `RM2/r/SL1_`, `RC1_disposition.md`; RC2 attestation |
| RM2 | sharpness numerics | – | – | 207/208 runs; no refutation; η = 1 probe failures kept as a flag (`RM2/LOG.md:21`) | | | | | `RM2/LOG.md` 18:09 |
| RM2 | better theorem BT1 (CP1) | 1 | 3 proposals + G1–G4 | P1, P2 (G1 form) adopted → v1.3 | | | | P3 deferred, later adopted in v1.4; O1–O4 open | `RM2/r/BT1_disposition.md` |
| RM2 | statement-change SC1 + RC3 | 2 | SC1 0/2/2 | 0 | 4 (record) | 0 | 0 | RC3: 0 | `RM2/r/SC1_disposition.md` |
| RM2 | line checks LC1-A/B, LC2-A/B/C | 5 | 0/0/8/5 | 5 | 7 | 0 | 0 | 1 (LC2-C #1 not adopted → O4′) | `RM2/r/LC1_`, `LC2_disposition.md` |
| RM2 | statement-change SC2 + RC5 | 2 | SC2 0/1/3 (the MAJOR is notation) | 0 | 4 | 0 | 0 | RC5: 0 | `RM2/r/LC2_disposition.md` §SC2 |
| RM2 | mid-point MP1 + RC4 | 2 | 0/0/3/1 | 2 (necessity labels) | 2 | 0 | 0 | RC4: 0 | `RM2/r/MP1_disposition.md` |
| RM2 | sweep SW1 + RC6 | 2 | 0/2/4/1 | 2 (M1: hypothesis broadened to M > 0; SHARPNESS log) | 5 (2 num) | 0 | 0 | RC6: 0 | `RM2/r/SW1_disposition.md:18` |
| RM2 | better theorem BT2 (final) | 1 | 7 proposals | 0 applied | | | | 5 "ADOPT in v1.5" (not done; post-council parked); 2 → O3′, O4′ | `RM2/r/BT2_disposition.md:21-27` |
| RM2 | council R1 | 2 | 0/0/4/≈8 + 1 obs | 0 | 9 | 0 | 0 | 3 deferred to v1.5 (F8, F9, F11) + 1 obs | `RM2/r/C1_disposition.md` |
| RM2 | post-council PC1; ACC carrier match | 2 | clean; ALL-MATCH | 0 | – | – | – | – | `PC1_postcouncil_diff_sol.md`, `ACC_carrier_match_sol.md` |
| START | statement lock SL1 + SL2 + RC2 | 3 | SL1 4/3/1 + 4 opt; SL2 1/0/2 + 3 opt | ≈16 | ≈2 | 0 | 0 | RC2: 0 (+1 PLAN edit) | `START/r/SL1_`, `SL2_disposition.md` |
| START | sharpness + falsification numerics | – | – | sharpness numerics changed the statement ([G1]: (V-c) improvable → new functional Ξ, v1.1, `SL1_disposition.md:20`); lemma falsification: 0 violations (2 development "violations" were script errors, `START/LOG.md` 17:19) | | | | | |
| START | better theorem BT1 (CP1) | 1 | 3 + G1–G6 | P1, P3 adopted; P2 adopted with a kill budget; G1 adopted | | 2 (G3, G5) | | G2, G4, G6 deferred | `START/r/BT1_disposition.md` |
| START | statement-change SC3 | 1 | 0/1/1 + 3 opt | ≈4 | ≈1 | 0 | 0 | 0 | `START/r/SC3_disposition.md` |
| START | line checks LC1-A/B/C | 3 | 0/0/6/0 | 3 | 3 (2 num) | 0 | 0 | 0 | `START/r/LC1_disposition.md` |
| START | mid-point MP1 | 1 | 0/0/2/0 | 1 | 1 | 0 | 0 | 0 | `START/r/MP1_disposition.md` |
| START | statement-change SC4 | 1 | 0/1/1 + 3 opt | 2 | 3 | 0 | 0 | 0 | `START/r/SC4_disposition.md` |
| START | line checks LC2-A/B + break review BR1 | 3 | 2/0/4/0 | 4 (BR1-1, BR1-3, A-1, B-1) | 2 | 0 | 0 | 0 | `START/r/LC2_BR1_disposition.md` |
| START | sweep SW1 | 1 | 0/1/7/0 | 3 | 5 (3 num) | 0 | 0 | 0 | `START/r/SW1_disposition.md` |
| START | council R1 | 2 | 10 NB | ≈3 (S3, O1, O4; applied later in v1.3.4) | ≈6 | 0 | 1 (O2, owner's rule) | not applied to frozen R1 content | `START/r/R1_disposition.md`, `R1_disposition_v134.md` |
| START | statement-change SC5 + RC_R2 | 2 | SC5 0/0/2 | 0 | 2 | 0 | 0 | RC_R2: 0 | `START/r/SC5_disposition.md`, `R2_disposition.md` |
| START | council R2 | 2 | 6 NB (opus) | 0 | – | 0 | 0 | 6 deferred (frozen) | `START/r/R2_disposition.md` |
| START | better theorem BT2 (final) | 1 | 4 proposals | 0 adopted here | | | | 4 → follow-up ticket W3-START2 (HQD:187) | `START/r/BT2_disposition.md:23` |
| START2 | statement lock SL1 + SC1 | 2 | 0/0/4 + 2 opt | ≈0 ("no definition, hypothesis or claim changes") | 6 | 0 | 0 | SC1: 0 | `START2/r/SL1_disposition.md` |
| START2 | line checks LC1-A/B | 2 | 0 findings | 0 | 0 | 0 | 0 | 0 | `START2/r/LC1_disposition.md` |
| START2 | council R1 | 2 | 9 NB | 0 | – | 0 | 0 | 8 errata deferred, 1 applied in registry | `START2/r/R1_disposition.md` |
| MISR | statement lock L01 + L02 | 2 | 0/1/3/0 | 4 | 0 | 0 | 0 | L02: 0 | `MISR/r/L01_disposition.md` |
| MISR | numerics | – | – | N4: (E^σ) "improvable"; BT1 gave an analytic obstruction, confirmed by N5 (`MISR/LOG.md` 23:02, 23:15); no lemma refuted | | | | | |
| MISR | better theorem BT1 | 1 | 5 proposals | 2 adopted (A1, A3) → v1.2 | | | | A2, B1, B2 recommended as tickets (queued, HQD:181-185) | `MISR/r/BT1_disposition.md` |
| MISR | line checks K1, K2 | 2 | 0/0/3/0 | 3 | 0 | 0 | 0 | 0 | `MISR/r/K_disposition.md` |
| MISR | mid-point | 0 | waived by HQ at CP2 (HQD:181-185) | | | | | | |
| MISR | council R1 | 2 | 0/0/5/9 | 2 (F3, F5) | 11 | 0 | 0 | 1 (F13 not applied) | `MISR/r/R1_SW1_disposition.md` |
| MISR | sweep SW1 (after R1, same manifest) | 1 | 0/0/8/1 | 1 (SW1-2) | 7 (num) | 1 (SW1-1 = sol S1 at R1) | 0 | 0 | `MISR/r/R1_SW1_disposition.md:15` |
| MISR | council R2 | 2 | 0/0/3/4 | 0 | – | 0 | 0 | 7 deferred (frozen) | `MISR/CHECKPOINT_3.md` |
| PSHARP | statement lock L01 | 1 | 0/1/2/0 | 3 | 0 | 0 | 0 | 0 | `PSHARP/r/L01_disposition.md` |
| PSHARP | break review K01 (also gave proposals; no separate BT) | 1 | 0/2/1/0 + 2 proposals | 2 | 1 (num: E2 outside (E)) | 0 | 0 | P1, P2 adopted → v1.2 | `PSHARP/r/K01_disposition.md` |
| PSHARP | line checks KSA, KBC | 2 | 0/0/3/1 | ≈1 | 3 | 0 | 0 | 0 | `PSHARP/r/KSA_KBC_disposition.md` |
| PSHARP | council R1 | 2 | 0/1/4/6 | 2 (registry label NECESSARY → FAILED-REMOVAL; existence remark) | 9 | 0 | 0 | 0 | `PSHARP/r/R1_disposition.md` |
| PSHARP | council R2 + reconciliation | 3 | 0/0/0/8 | 0 | – | 0 | 0 | 8 deferred; reconciliation 11/11 resolved | `PSHARP/r/R2_disposition.md` |
| SAMP | statement lock SL1 | 1 | 5 req | 4 | 1 | 0 | 0 | 0 | `SAMP/r/SL1_disposition.md` |
| SAMP | numerics v1–v4 | – | – | 0 violations; SW1 MAJ3/MAJ4 and LC1 #6 corrected the numerics labels and provenance | | | | | `SAMP/LOG.md` |
| SAMP | better theorem BT1 | 1 | 12 items | 8 adopted → v3 | | 3 not adopted (§3.2, §4.3, §5 constant 18) | | 1 superseded | `SAMP/r/BT1_disposition.md` |
| SAMP | line checks LC1, LC2 | 2 | 0/3/9/0 | 8 | 2 | 2 par (LC2 #1 = MP1 #1; #3 ≈ MP1 #3) | 0 | 0 | `SAMP/r/LC1_`, `LC2_disposition.md` |
| SAMP | mid-point MP1 | 1 | 1 MEDIUM / 2 LOW | 3 | 0 | 0 | 0 | 0 | `SAMP/r/MP1_disposition.md` |
| SAMP | sweep SW1 (first run cancelled by a restart) | 1 | 0/4/16/8 | ≈9 | ≈19 (≥6 num) | 0 | 0 | 0 | `SAMP/r/SW1_disposition.md` |
| SAMP | council C1 | 2 | 11 NB | 4 (opus #1 PC scope, #2 D omits KERNEL, #3 TR-b proof slip, #8 constant) | 7 | 0 | 0 | 0 | `SAMP/r/C1_disposition.md` (HQ correction at :10) |
| SAMP | post-council PC1, PC2 | 2 | PC1: maths CLEAN, record NOT-CLEAN | 0 | 3 record fixes | 0 | 0 | PC2: RESOLVED | `PC1_postcouncil_diff_sol.md:50-52`; HQD:33-41 |
| SCR | statement lock R01 + R01b | 2 | 1/3/3/5 | 9 | 1 | 0 | 0 | 2 notes, no change | `SCR/r/R01_disposition.md` |
| SCR | numerics | – | – | N3 end-to-end check led to the lead's SCR-A° (`R01_disposition.md:21`); reviewer script `R04_scratch/remark_counterexample.py` refuted an unclaimed remark; N4: 105,955 checks, 0 violations | | | | | `SCR/LOG.md` |
| SCR | better theorem R02 | 1 | 6 proposals + headings | 5 adopted → v3 (master theorem SCR-M) | | 1 (#6) | | | `SCR/r/R02_R03_R04_disposition.md` |
| SCR | line checks R03, R04 | 2 | 0/1/7/2 | 9 | 1 | 0 | 0 | 0 | same file |
| SCR | post-BT change check / re-lock R05, R05b, R05c | 3 | 0/4/10/0 | 10 | 4 | 0 | 0 | R05c: 0 | `SCR/r/R05_disposition.md` |
| SCR | mid-point R06 | 1 | 0/1/3/1 | 1 | 1 | 2 (R05b N1, N2) | 0 | 1 | `SCR/r/R06_disposition.md` |
| SCR | sweep R07 | 1 | 0/3/9/0 | 7 | 5 | 0 | 0 | 0 | `SCR/r/R07_disposition.md` |
| SCR | council C1 | 2 | 0/0/2/4 | 2 (Opus 1: κ, b, M fixed added to A1/SCR-G/M4; Astra 1) | 4 | 0 | 0 | 0 | `SCR/r/C1_disposition.md` |

Later layers, all tickets:
- **API audit** (blind Fable batch): 58 Wave-3 claims audited (pass 1: 33; pass 2: 25). Result: 0 GAP, 0 ERROR, 53 OK,
  5 MINOR (W3-RM:Examples, W3-RM:RM-R, W3-SAMP:Pkg, W3-SCR:L5.1, W3-SCR:SCR-M). No finding concerned a Wave-3
  statement (`API_AUDIT/pass1/VERDICTS.tsv`, `pass2/VERDICTS.tsv`).
- **Acceptance audits** refused START twice (HQD:133, 161), and RM2, MISR and PSHARP once (HQD:201). Every refusal was
  on record or tool grounds; none was on mathematics.

**Did falsification numerics ever refute or correct a lemma or statement?**
- No lemma was refuted by the lead's falsification numerics in any ticket. Every lemma-falsification run reports
  0 violations. The development "violations" (START, PSHARP) were script errors.
- Numerics did change statements in three tickets:
  - POST: the E5 numerics, together with R03's analytic counterexample, made item 5 "False in general".
  - START: sharpness numerics led to the [G1] functional Ξ.
  - SCR: N3 led to SCR-A°.
- One remark was refuted by a reviewer's own script: SCR R04, the ω-only remark, which was deleted.
- In 8 of the 10 tickets, reviewers found defects in the numerics themselves: POST C1 A-F5/F6; POST2 S01 #2;
  RM C1 A-1; RM2 SW1 M2; START LC1 A2 and SW1 #5–7; MISR SW1-1; PSHARP K01 F1; SAMP SW1 M3/M4.

## T2. Council rounds

| ticket | round | seat | score | gates | C/M/m/n | blocking findings → class |
|---|---|---|---|---|---|---|
| POST | C1 | astra | 7.5 | FAIL G1, G2, G3, G5 | 0/2/6/1 | F1 MAJOR: rate optimality and YWJ comparison overclaimed → FAITHFULNESS (sources) + STRENGTH overclaim; fixed by new Prop. LB. F2 MAJOR: NH14 misrepresented → FAITHFULNESS. F3: Song–Liang qualifications → FAITHFULNESS. F4: REPORT drops coefficient conditions → RECORD/WORDING. F5: numeric quotes → RECORD (`POST/r/C1_council_astra.md:13-17`) |
| POST | C1 | opus | 8.4 | PASS | 0/0/4/7 | – |
| POST | C2 | astra | 8.3 | FAIL G1, G2, G3 | 0/1/1/3 | F1 MAJOR: REPORT states LB without its domain (STATEMENT and lemma correct) → RECORD/WORDING, **new** (LB was new after C1). F2: NH14 Cond. 4.5 parameters → FAITHFULNESS, **re-raised area** (C1 F2) (`C2_council_astra.md:13-15`) |
| POST | C2 | opus | 8.8 | PASS | 0/0/1/7 | – |
| POST | C3 | astra / opus | 8.8 / 8.7 | PASS / PASS | 0/0/0/2 ; 0/0/2/8 | – |
| POST2 | C1 | astra / opus | 8.6 / 8.6 | PASS / PASS | 0/0/2/1 ; 0/0/5/7 | – |
| RM | C1 | astra | 8.8 | FAIL G6 | 0/1/1/1 | F1 MAJOR: L2 runs labelled as (L-gain) violations, though the experiment sets a population proxy strength → RECORD/WORDING (numerics labels in the sharpness record) (`RM/r/C1_disposition.md:7`) |
| RM | C1 | opus | 8.9 | PASS | 0/0/3/5 | – |
| RM | C2 | astra / opus | 9.8 / 9.1 | PASS / PASS | 0/0/1/1 ; 0/0/0/6 | – |
| RM2 | R1 | astra / opus | 9.5 / 8.8 | PASS / PASS | ≈ 0/0/4/8 (mostly opus) | – |
| START | R1 | sol / opus | 9.1 / 8.8 | PASS / PASS | 3 NB ; 7 NB | – |
| START | R2 | sol / opus | 9.2 / 8.9 | PASS / PASS | 0 ; 6 NB | – (round run for acceptance tool A4, see below) |
| START2 | R1 | sol / opus | 9.1 / 9.1 | PASS / PASS | 2 NB ; 7 NB | – |
| MISR | R1 | sol / opus | 9.3 / 8.7 | PASS / PASS | 0/0/0/1 ; 0/0/5/8 | – |
| MISR | R2 | sol / opus | 9.2 / 8.9 | PASS / PASS | total 0/0/3/4 | – |
| PSHARP | R1 | sol | 7.6 | FAIL G3–G6 | 0/1/2/0 | M1 MAJOR: REPORT and registry of Claim B dropped s₀ ≤ min(K−1, p/2) and s₀/p → 0 (locked STATEMENT correct) → RECORD/WORDING (`PSHARP/r/R1_disposition.md:8`) |
| PSHARP | R1 | opus | 9.0 | PASS | 0/0/2/6 | – |
| PSHARP | R2 | sol / opus | 9.2 / 9.3 | PASS / PASS | 0/0/0/2 ; 0/0/0/6 | – |
| SAMP | C1 | astra / opus | 9.1 / 8.8 | PASS / PASS | 2 NB ; 9 NB | – |
| SCR | C1 | astra / opus | 9.3 / 8.9 | PASS / PASS | 0/0/1/0 ; 0/0/1/4 | – |

Rounds per ticket: POST 3, RM 2, START 2, MISR 2, PSHARP 2, and 1 each for POST2, RM2, START2, SAMP and SCR (16 rounds,
32 seat-reviews). Four seat-reviews failed (POST C1, POST C2, RM C1, PSHARP R1). All four were the OpenAI seat
(astra ×3, sol ×1). The Claude seat passed in every round. No blocking finding in any round was CORRECTNESS: every
failing seat states that the formal proofs pass (e.g. `POST/r/C1_disposition.md:5`, `PSHARP/r/R1_disposition.md:3`).

Why extra rounds happened:
- **POST** (C2, C3): literature and sharpness overclaims at C1, then a REPORT-only omission of LB's domain at C2.
- **RM** (C2): numerics labelling in SHARPNESS.
- **PSHARP** (R2): a REPORT/registry summary dropped hypotheses.
- **START** (R2): process. R1 passed, but acceptance check A4 refused it because MANIFEST_R1 listed PROTOCOL.md,
  LIFECYCLE.md, a template and claims.tsv, all edited on `main` afterwards (HQD:133-136).
- **MISR** (R2): process. A sweep ordered after R1 classed a numerics-docstring fix as "substantive", and HQ's CP2 rule
  then required a re-round (`MISR/LOG.md` 04:16-04:27). That fix was also the R1 sol NIT S1.

No round-2+ blocking finding re-raised an earlier blocking finding verbatim. POST C2 F2 is a further omission in the
same NH14 summary that C1 F2 had rewritten.

## T3. Late slips (REAL; found at sweep or later, or by a re-check, on an object that had already passed an earlier check)

| # | ticket | error (one line) | found by | earlier pass of the same object | why missed (record only) |
|---|---|---|---|---|---|
| 1 | POST2 | D(b) proof step D3: chain asserts s₀+j₀−1 ≤ min(s₀+j₀, K), false at p = K = 2 (`D_hellinger.md:53`) | PC1 post-council diff, 2026-11-11, "required repair" (`POST2/r/PC1_…:44`) | D: K-D, K2 (D v2), M01, S01, council C1 | The step was **edited after the council**: Lemma E0 was added per C1 B-5 (`C1_disposition.md:15`) and D3 rewritten to cite it. The disposition said no edit changed a hypothesis, rate or constant (`C1_disposition.md:5`). PC1 ran 2 days later on HQ's order (HQD:20-24). Rolled back via SUSPECT → repair → PC2 (HQD:36-39, 48-50) |
| 2 | RM2 | STATEMENT §3 required M, φ₀ ∈ (0, 1], but examples E3–E5 use M > 1; hypothesis broadened to M > 0 | SW1 MAJOR 1 (`RM2/r/SW1_disposition.md:18`) | §3: SL1, RC1, RC2, SC1, SC2. Examples L6: LC2-C VERIFIED / V-W-A (`LC2_disposition.md:30`) | Glue between the statement and the examples. L6 was written by a separate prover (PV1) after the lock and checked in its own round. The record states no reason. RC6 notes it is "not merely typographical" |
| 3 | START | Proposition OVL said "fixed a_l" while Q_n varies; the proof needs a uniform bound ā | SW1 MAJOR 1 (`START/r/SW1_disposition.md:11`) | L10 (IF-START, OVL, MIS) VERIFIED by LC2-B (`LC2_BR1_disposition.md:11`) | No reason recorded. The gap is a quantifier mismatch between the statement wording and the proof |
| 4 | SAMP | Lemma PC: the HPM is the max of the final ledger's offered set, not a function of island records; PC (ii)–(iii) changed | SW1 MAJOR 1 (`SAMP/r/SW1_disposition.md:8`) | PC VERIFIED by LC1 (`LC1_disposition.md:3`) | No reason recorded. At council, opus #1 still found PC's scope narrower than its downstream use in D/LT/C/TR, i.e. glue (`C1_council_opus.md:158`) |
| 5 | SAMP | The three-state example is not a realisation of the coded target; TR non-nesting holds only for abstract targets (a narrowing) | SW1 MAJOR 2 (`SW1_disposition.md:9`) | TR: LC2 ("TR's kernel/path arguments verified"), MP1 | TR was new after BT1. The defect is a scope label: abstract vs coded target (FAITHFULNESS) |
| 6 | RM | "(V)+(L) do not imply (N-D)(i)" was asserted in L2_NAF without proof | R08 sweep MAJOR 4 (`RM/r/R08_disposition.md:13`) | L2_NAF V-W-A by R03 | ≈: the record does not say whether the sentence existed when R03 ran. [P1] was added to L2_NAF after R03 (`R03_R05_disposition.md:12`) |
| 7 | START (stage: break review, before the sweep) | Bridge (B-R) claimed all of (E), including p > s₀, from hypotheses that allow p = s₀ | BR1 CRITICAL (`LC2_BR1_disposition.md:25`) | "p > s₀ eventually" entered (E) via the SL1 fix (`SL1_disposition.md:7`). The statement then passed SL2, SC3 and SC4 | Statement changed at the lock; bridge-row vs hypothesis glue |
| 8 | SCR (stage: re-lock) | STATEMENT M3 omitted the maximising-witness hypothesis that L7's M3 has (counterexample given) | R05b MAJOR N1; R06 in parallel (`R05_disposition.md:26`) | R05 marked M3 CORRECT (`R05_disposition.md:4`) | Glue: R05 passed L7's M3; the STATEMENT copy differed |

Non-MAJOR but REAL late catches (council stage, on checked objects):
- SAMP C1, unlabelled non-blocking items: opus #2, D omits the KERNEL premise; #3, TR-b proof slip; #1, PC scope
  (`C1_council_opus.md:158-175`). These edits were applied after the vote, the disposition said "no claim changed", and
  the HQ correction at `C1_disposition.md:10` says that was inaccurate.
- SCR C1 Opus 1 (MINOR): A1, SCR-G and M4 also need κ, b, M fixed. This was added after the pass, with no diff check
  (`C1_disposition.md:13-17`).
- POST2 C1 B-5 (MINOR): m♯ ≥ min(j₀, K) was unproved but used in E1(b) and D3; new Lemma E0.
- RM C2 B1 (NIT): a SHARPNESS argument failed in one sub-case. PC1 calls the rewrite a proof repair
  (`RM/r/PC1_…:70`).

## T4. Statement history

| ticket | version sequence (stage) | change type | reviewed by | HQ told |
|---|---|---|---|---|
| POST | v1.0 → v1.1 (R01) → v1.2 (R02) → v1.3 (after C1: interface form, Cor 1R, p ≥ 2) → v1.4 (post-C3 wording) | v1.1: hypotheses made explicit (=). Item 5 → "False in general" (narrowing of a claim). LB added (new) | R01/R02, C2/C3 | Final report; layer substitution ruled after the fact (HQD:3) |
| POST2 | v1.0 → v1.1 LOCK (L01) → v1.1 + (G2*) after the lock ("no hypothesis change", `POST2/LOG.md:25`) → v1.2 (R03b C+, D+, E1 under (ID^M): **strengthening**) → v1.2.1 post-council | strengthening after the lock | K2 line-checked C v2, D v2, E1 v2; no separate statement-change check | "Recorded for HQ" (HQ not reachable); approved 2026-11-11 at the final (HQD:16) |
| RM | v1.0 → v1.1 LOCK (R01) → v1.2 (P1, P2, P3a, P7: hypotheses weakened = **strengthening**) → v1.2.1 (C1 wording) → post-C2 edits (B1, B4) | strengthening | R06, R04 (line checks); PC1 (post-C2) | Flagged in REPORT; HQ kept v1.2.1 at the final (HQD:11) |
| RM2 | v1.0 → v1.1 (SL1) → v1.2 LOCK (RC1, RC2) → v1.3 (CP1 P1/P2: strengthening) → v1.4 (Form R riders P3, T6: strengthening) → M > 0 after SW1 (broadening) → post-council edits parked; v1.5 never made | strengthening ×3 | SC1 + RC3; SC2 + RC5; RC6 | CP1 decision at the time (HQD:130); riders pre-approved at CP1/CP2; M > 0 only via CP3 |
| START | v1.0 → v1.1 (SL1 + [G1]) → v1.2 LOCK (SL2, RC2) → v1.3 LOCK (CP1 P1–P3, SC3) → v1.3.1 (MP1 edits + 2 lead-initiated **narrowings**: (B-R) C_L = 0 clause as O_P tightness; example families) → v1.3.2 (BR1: p > s₀ explicit in (B-R), (T3)(b)) → v1.3.3 (SW1: OVL uniform levels, convention) → v1.3.4 (R1 non-blocking) | narrowings at v1.3.1–v1.3.3 | SC4 (v1.3.1; classes item 3 as a "substantive narrowing"); SW1 read v1.3.2; council R1 read v1.3.3; SC5 v1.3.4 | Flagged in LOG at the time (`START/LOG.md:32`). HQ accepted at the CP3 audit (`START/LOG.md:41`; `CHECKPOINT_3.md:98-103`). The CP2 decision had said a narrowing of (T3)(b) returns through CP1 (`START/LOG.md:30`); SC4 says (T3)(b) itself was unchanged |
| START2 | v1.4.0 (P1, P4 taken stronger than the brief) → v1.4.1 (SL1) | = (SL1); strengthening vs START | SL1, SC1 | CP1 (HQD:198) |
| MISR | v1.0 → v1.1 (L01; L02 LOCK) → v1.2 (BT1 A1, A3: new clauses) → v1.3 (R1 + SW1 batch: §3(a) over a larger class) | strengthening | v1.2 not lock-reviewed (K1/K2 + council read it); v1.3 by council R2 | CP1 file written after v1.2 (pre-approved legs) |
| PSHARP | v1.0 → v1.1 LOCK (L01) → v1.2 (K01 P1, P2 + F3) → v1.2.1 (KBC remark) → v1.2.2 (R1 wording) | strengthening | KSA/KBC read v1.2; council | CP1 file written after v1.2 |
| SAMP | v1 → v2 LOCK (SL1) → v3 (BT1: strengthening, flagged) → SW1: PC HPM scope, TR non-nesting abstract-only (**narrowing**) → post-C1: D gains the KERNEL premise, PC(i) includes 𝓜_r (**narrowing**) | strengthening, then narrowings | v3 by LC2/MP1; SW1 edits by council; post-vote edits by PC1 (2 days later) | v3 accepted by HQ mid-ticket (`SAMP/LOG.md` 17:26). D/TR narrowing **found by HQ at registry** ("registered from a mid-ticket draft", HQD:27-29), approved 11-12 (HQD:141) |
| SCR | v1 → v2 (R01; SCR-C restricted to s₀ = O(1): narrowing, plus SCR-A°) → R01b LOCK → v3 (R02 adoption: strengthening) → v3.1 (R05) → v3.2 (R05b) → R05c LOCK → v3.3 (R07 wording) → v3.4 post-pass (κ, b, M, σ fixed added to A1, SCR-G, M4) | narrowing at the lock; strengthening; hypothesis addition post-pass | R01b, R05/R05b/R05c; v3.4: **none** (no PC check for SCR; HQD:20-24 lists only RM, SAMP, POST2) | REPORT only; the brief pre-authorised strengthening (`SCR/LOG.md`) |

Weakenings not flagged at the time:
- SAMP D/TR narrowings: the disposition said "no claim changed"; HQ found them at registry (HQD:27-29).
- SCR v3.4 hypothesis addition: the disposition says "none changes a conclusion or a constant"; never diff-checked.
- POST2 (G2*) event added after the lock, described as "no hypothesis change".

## T5. Sharpness gate

| ticket | ASSUMPTION_MAP | boundary numerics | BT proposals → outcome | changed target before heavy proving? | adopted later / follow-up |
|---|---|---|---|---|---|
| POST | yes | yes (E1–E5) | R03 ranked proposals; §5A counterexample | partly: item 5 → false (re-check ticket; no CP1) | R03 items → **W3-POST2** (HQD:8) |
| POST2 | yes | yes (N1–N8) | 7: 3 adopted, 4–5 recorded | no: R03b ran in parallel with the line checks; C, D, E rewritten to v2 after K-BC/K-D checked v1 (`POST2/LOG.md` steps 5-8) | 4 open → `better:PENDING` (HQD:24) |
| RM | yes | yes (V1, L1, L2, N1) | 8: 4 adopted, 3 recommended, 1 open | no: R02 ran in parallel with lemma writing (16:31–16:49) | P5 → **W3-RM2** (`RM2/BRIEF.md:1`) |
| RM2 | yes | yes (B1–B4, 208 runs) | BT1: P1, P2 adopted at CP1; P3 deferred. BT2: 5 "ADOPT in v1.5", 2 open | **yes** (v1.3 before the key lemma; `CHECKPOINT_1.md`) | P3 adopted after CP2 (v1.4). BT2 P1–P5 never applied (post-council parked) |
| START | yes | yes (8 boundary experiments) | BT1: P1, P3 adopted, P2 kill-budgeted, G3/G5 rejected. BT2: 4 | **yes** (v1.3 at CP1, HQD:77) | BT2 P1–P4 → **W3-START2** (HQD:187) |
| START2 | no | no (falsify_P.R only) | none (the ticket is the BT2 follow-up) | – | – |
| MISR | yes | yes (N1–N5) | 5: A1, A3 adopted; A2, B1, B2 tickets | yes, but concurrently with the proof drafts (`MISR/LOG.md` 23:08–23:15) | A2, B1, B2 queued (HQD:181-185) |
| PSHARP | yes | yes (a_boundary, c_counter) | via break review K01: P1, P2 adopted | yes (v1.2 before the line checks; CP1) | – |
| SAMP | yes | yes (v1–v4) | 12: 8 adopted, 3 not adopted | no: proofs were already written (16:29); LC1 checked C v1 and LT v1 before BT1 (`LC1_disposition.md:3`) | §3.2, §4.3 recorded for HQ |
| SCR | yes | yes (N2, 16 scenarios) | 6: 5 adopted, 1 not | no: R02 ran in parallel with R03/R04 on v2; L5 rewrite + new L7 then re-checked by R05 | #6 open |

CHECKPOINT_1 exists for RM2, START, START2, MISR and PSHARP. SAMP has a single `CHECKPOINT.md`. POST, POST2, RM and SCR
predate rule 10 and have no checkpoint.

## T6. Rework and rollback inside tickets

| ticket | object changed after dependents used it | how noticed | dependents re-checked? | time from change to re-check |
|---|---|---|---|---|
| POST2 | D3 cutoff step (post-council edit) | PC1, ordered by HQ | yes: SUSPECT on D.D(b); PC2 re-checked D(b) and its dependents (HQD:36-39, 48-50) | council 2026-11-09 ~20:16 → PC1 2026-11-11 (≈2 days); PC2 the same day |
| POST2 | C, D, E1 rewritten to v2 (R03b) after line checks of v1 | lead (LOG step 8) | yes: K2 on C v2, D v2, E1 v2, then M01 and S01 | steps 8 → 12 (LOG clock unreliable; erratum `POST2/LOG.md`) |
| RM | B1′, L1b, [P1] in L2_NAF, [P7] added after R03 | lead (`R03_R05_disposition.md:12`) | yes: R06, R07, R08 | 16:48 → R06 16:50–16:56 |
| RM | post-C2 edits B1, B2, B4, B5 (two of them substantive) | HQ rule after pipeline review R01 | yes: PC1 CLEAN (HQD:30-32) | 2026-11-09 → 2026-11-11 |
| RM2 | statement v1.3 → v1.4 after L0–L3 were checked | lead | SC2 checked v1.3 ⇒ v1.4; council F6: "written for v1.3; unchanged for Form F" | 04:03 → SW1 04:17 |
| RM2 | 7 post-council edits inside MANIFEST_R1 | acceptance audit (HQD:201) | not re-checked: the R1 snapshot was restored and the edits parked (`RM2/LOG.md:37`) | – |
| START | (E) gained "p > s₀" at SL1; the (B-R) row still claimed (E) | BR1 break review | yes: v1.3.2 read by SW1 | lock 12:14 → BR1 18:11 (≈6 h) → SW1 frozen 18:12 |
| START | OVL (L10, VERIFIED by LC2-B) | SW1 | yes: v1.3.3 read by council R1 | 18:11 → SW1 before 18:33 → R1 18:55 |
| SAMP | C v1, LT v1 changed by BT1 after LC1 started | lead | yes: LC2 + MP1 on the new pieces | 16:58 → 17:13–17:15 |
| SAMP | PC (HPM scope) changed at SW1 while D/LT/C/TR consume it | council opus #1 | post-vote edits verified only by PC1 | 18:12 → council 18:44 → PC1 2026-11-11 |
| SCR | L5 rewrite, new L7 after R03/R04 checked v2 | lead | yes: R05 delta check, line by line | no clock times in `SCR/LOG.md` |
| PSHARP | v1.2 (K01 proposals) after the lock | lead | yes: KSA/KBC read v1.2 | 23:40 → 04:20 the next day |
| MISR | v1.2 clauses after L01/L02 | lead | K1/K2 + council (no re-lock) | 23:15 → 23:24 |

No lemma in any ticket was refuted after its dependents had been written. Every change above is a repair, an amendment
or a strengthening.

## T7. Cost signals

| ticket | review launches (reply files) | BRIEF_* | MANIFEST_* | RC/SC/PC-type checks (incl. re-lock/recheck/recon) | of which found REAL |
|---|---|---|---|---|---|
| POST | 9 | 0 | 0 | 0 | – |
| POST2 | 12 | 0 | 0 | 2 (PC1, PC2) | 1 (PC1) |
| RM | 13 | 0 | 0 | 1 (PC1) | 0 |
| RM2 | 22 (+1 prover brief PV1) | 23 | 12 | 9 (RC1–6, SC1–2, PC1) + ACC | 0 (RC1, SC1, SC2: record only) |
| START | 21 | 21 | 12 | 5 (RC2, RC_R2, SC3, SC4, SC5) | 2 (SC3 [TK] rate; SC4 status label + example conditions) |
| START2 | 6 | 6 | 4 | 1 (SC1) | 0 |
| MISR | 10 | 10 | 2 | 1 (L02) | 0 |
| PSHARP | 9 | 9 | 2 | 1 (R2 reconciliation) | 0 |
| SAMP | 10 (+1 cancelled SW1) | 0 | 0 | 2 (PC1, PC2) | 0 (PC1: record NOT-CLEAN only) |
| SCR | 12 | 0 | 0 | 4 (R01b, R05, R05b, R05c) | 2 (R05, R05b) |
| **total** | **124** | 69 | 32 | 26 (+1 ACC) | 5 |

Interrupted launches with no output are not counted: START LC1 ×3 and SC5 ×2; the MISR opus seat (relaunched once).

## What the numbers say

1. 124 review launches over 10 tickets. RM2 and START used 43 of them, plus 24 manifests and 14 diff/reconciliation checks.
2. No falsification-numerics run refuted a lemma. Numerics changed a statement 3 times (POST, START, SCR). Reviewers found defects in the numerics themselves in 8 of the 10 tickets.
3. Statement locks produced the largest early REAL counts: START 4 CRITICAL, SCR 1 BLOCKER + 3 MAJOR, RM2/POST2/MISR/PSHARP 1–3 MAJOR each.
4. Sweeps found MAJORs in 6 tickets. Of those MAJORs, 5 were REAL errors in objects that had already passed a line check (T3 #2–#6; #6 is ≈). The others were overclaimed necessity labels in ASSUMPTION_MAP/SHARPNESS, or numerics/record issues.
5. 16 council rounds, 32 seat-reviews, 4 failing seat-reviews, all from the OpenAI seat. Every blocking finding was FAITHFULNESS (literature, overclaimed strength) or RECORD/WORDING; none was CORRECTNESS.
6. Extra rounds came from 3 record/REPORT issues (POST ×2, RM, PSHARP) and 2 process causes (START: acceptance tool A4; MISR: sweep after the council).
7. Post-council edits caused the one confirmed false proof step after a council pass (POST2 D3). It was caught 2 days later by a diff check that HQ ordered.
8. Of 26 diff/reconciliation/re-lock checks, 5 found something REAL: POST2 PC1, START SC3 and SC4, SCR R05 and R05b. 21 attested "editorial/record only".
9. Better-theorem reviews changed the target before heavy proving in RM2, START and PSHARP (and concurrently in MISR). They spawned 3 follow-up tickets (POST2, RM2, START2). BT2 on RM2 (5 ADOPT NOW) was never applied.
10. Weakenings not flagged at the time: SAMP D/TR (HQ found them at registry), SCR v3.4 (never diff-checked), POST2 (G2*). Acceptance audits refused 5 times, all on record or tool grounds. The API audit found 0 GAP/ERROR in 58 Wave-3 claims.

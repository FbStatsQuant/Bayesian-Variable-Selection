# Review-trail mining: Wave 1, Wave 1C, Wave 2

Scope: Wave1 W1-GEN, W1-N1, W1-N3, W1-PXN; Wave1C C-DLV, C-ENG, C-GROW, C-MIS, C-PACK, FINAL, HQ_AUDIT; Wave2 W2-APP,
FAC-A, FAC-B, FAC-PK, FAC-PKA, FAC-S5, FAC-S5F, FAC-X, FAC-XA, FAC-K2, LOC2, UNI, HQ_AUDIT, SR. Paths are relative to
`Theory_work/`. "disp" = the `reviews/R*_disposition.md` (or `C*_disposition.md`) of that ticket. W1-N3 and W1-PXN have no
disposition files; their verdicts come from `REPORT.md §4` and `LOG.md`.

How findings were classified:
- REAL = changed a statement, proof step, hypothesis or status label. COSM = wording, notation, record, citation, or
  numerics-package only. RR = re-raised (an earlier layer or round already raised it). REJ = the lead objected and the objection stood.
- Sev = the reviewer's own labels: F = FATAL/CRITICAL/ERROR, M = MAJOR (and GAP verdicts on whole items), m = MINOR, e = editorial/NIT.
  "req" = required changes that the reviewer left unlabelled.
- "≈" marks a split I made from one-line disposition entries without opening every item.

## T1. Yield per layer, per ticket

| ticket | layer | n | sev F/M/m (+e) | REAL | COSM | RR | REJ | source |
|---|---|---|---|---|---|---|---|---|
| W1-GEN | stmt lock R01 | 1 | 9 req | 9 | 0 | 0 | 0 | R01_disposition.md (#2: W counter-instance to canonical S*) |
| W1-GEN | lemma checks R02–R04,R06–R09 | 7 | verdicts: 4 V-W-A, L6(d) GAP, L7 GAP×2 then VERIFIED | ≈30 | ≈4 (cites) | 0 | 0 | R02_R04, R06, R07 disp; LOG:44-51 |
| W1-GEN | numerics E1–E7 | – | no refutation; E7 ran the v1 (C6) design only | – | – | – | – | REPORT:76-78, :96 |
| W1-GEN | mid-point R05 | 1 | 2 M + 6 other | ≈6 (SEL gap → C5(d) downgraded; L8 + (C1′) added) | ≈1 | 2 (#6, #7 already repaired) | 0 | R05_disposition.md |
| W1-GEN | sweep R10 | 1 | 0/1/6 (+1) | 4 (M: L8 bounded-energy hypothesis; C5(d) restricted; remark removed; convention) | 4 | 0 | 0 | R10_disposition.md |
| W1-GEN | council r1 | 2 | Sol 0 req; Opus 4 m | ≈1 ((C3) onset alignment) | ≈3 | 0 | 0 | R11_R12_disposition.md |
| W1-N1 | stmt lock SL1 | 1 | 4 req + 3 opt | 3 | 3 | 0 | 1 (Lean) | SL1_disposition.md |
| W1-N1 | lemma check LC1 | 1 | 2 blocking + 4 non-blocking; L1 GAP | 2 | 4 | 0 | 0 | LC1_disposition.md |
| W1-N1 | numerics | – | no refutation; the numerics package was itself rewritten after the sweep | – | – | – | – | SW1_disposition.md |
| W1-N1 | mid-point MP1 | 1 | 1 non-blocking | 0 | 1 | 0 | 0 | MP1_disposition.md |
| W1-N1 | sweep SW1 | 1 | 0/5/11 | 0 | 16 (all 5 M in the numerics package) | 0 | 0 | SW1_disposition.md; REPORT:76-77 |
| W1-N1 | council r1 | 2 | 2 + 8 non-blocking | 0 | 9 | 1 (Lean) | 1 | C1_disposition.md |
| W1-N3 | stmt lock R01 | 1 | 5 fixes | ≈5 (STATEMENT v1.1) | – | 0 | 0 | LOG:10; REPORT:56 |
| W1-N3 | lemma checks R02,R03,R05 | 3 | L1 GAP, L5 WRONG (counterexample to the wording), 3 minor | ≈4 | ≈1 | 0 | 0 | REPORT:57-59; LOG:17,21-22 |
| W1-N3 | numerics | – | the harness confirmed the card-vs-code deviation before lock (529 truncation instances); 0 lemma failures | (corroborated a statement change) | – | – | – | LOG:6-9 |
| W1-N3 | mid-point R04 | 1 | 3 points | ≈2 | ≈1 | 0 | 0 | LOG:19 |
| W1-N3 | sweep R06 | 1 | 0/0/8 (+4) | 3 (m #2 added hypothesis (H4) to the theorem) | 9 | 0 | 0 | reviews/R06_sweep.md:9-20 |
| W1-N3 | council r1 | 2 | minor points (not itemised) | 0 | all (v1.3 wording) | 0 | 0 | LOG:24 |
| W1-PXN | stmt lock R00 | 1 | 6 M / 2 m | 8 | 0 | 0 | 0 | LOG:11-14 |
| W1-PXN | item checks R11–R17, R19, R21 | 9 | ERROR in R13, R14, R15 (×2), R17 (L) step; GAP in R16 | ≈10 (errata E-1..E-20) | ≈4 | 2 (R16 #1, #2 = D1, D2 already found by the lead) | 0 | LOG:20-36 |
| W1-PXN | numerics N1–N8 | – | 0 violations; N8 finite-n failures, not a counterexample | – | – | – | – | LOG:37-48 |
| W1-PXN | mid-point R20 | 1 | 4 req | 2 (SIZE onset; D2 choice) | 2 | 0 | 0 | LOG:39 |
| W1-PXN | sweep R30 | 1 | 1 E / 2 GAP / 4 m | 3 | ≈4 | 0 | 0 | reviews/R30_sweep_codex.md:1-9,38-41 |
| W1-PXN | council r1 | 2 | Codex 2 m; Opus 1 M (form) + 7 m | 0 (Opus #8 added a remark later found false, see T3) | 9 | 1 (Opus M = R20 "single consolidated proof") | 0 | LOG:52-56 |
| C-DLV | stmt lock R01 | 1 | 1 F / 7 M / 2 m (REJECT) | 10 (F: target kept as unclaimed goal; M7: route removed) | 0 | 0 | 0 | R01_disposition.md |
| C-DLV | lemma checks R02–R04 | 3 | 1 F (Cor 5.3 ERROR) / 5 M / 10 m | ≈15 | ≈1 | 0 | 0 | R02_R04, R03 disp |
| C-DLV | numerics N1–N3 | – | 0 violations; never reached tier 1 (C1 Opus #8) | – | – | – | – | R03_disposition.md:21; C1_disposition.md |
| C-DLV | mid-point R05 | 1 | 0/1/2 | 3 (premise TDP-IMPL added) | 0 | 0 | 0 | R05_disposition.md |
| C-DLV | sweep R06 | 1 | 0/4/9 (+2) | ≈8 (4 M: premises CONFIG/MACH, overstatement) | ≈7 | 0 | 0 | R06_disposition.md |
| C-DLV | council r1 | 2 | Codex 2 M (gates FAIL); Opus 10 items | ≈7 | ≈5 | 2 (Codex M1, M2 continue the sweep #1 / R02 #2 family) | 0 | C1_disposition.md |
| C-DLV | council r2 | 2 | 1 + 6 m | ≈1 | ≈6 | 0 | 0 | C2_disposition.md |
| C-ENG | plan reviews R01, R02 | 2 | R01 1 blocker / 4 M / 2 m; R02 2 M / 2 m | 11 (plan/tests/code) | 0 | 0 | 0 | R01, R02 disp |
| C-ENG | code reviews R03–R09 | 7 | 2 M (R07) + 3 m | 5 | 0 | 0 | 0 | REPORT:101-109 |
| C-GROW | stmt lock R01 | 1 | 9 req | 9 (#1: C5(b) violated G1) | 0 | 0 | 0 | R01_disposition.md |
| C-GROW | lemma checks R02–R04, R06, R07 | 5 | R02, R07 VERIFIED; R03 2; R04 7 (counterexample → STATEMENT v2.1); R06 9 presentation | ≈6 | ≈12 | 0 | 0 | R03, R04, R06_R07 disp |
| C-GROW | numerics F1–F3, G1 | – | finite-n violations at n ≤ 800; no refutation | – | – | – | – | R06_R07_disposition.md |
| C-GROW | mid-point R05 | 1 | 0/0/4 | 1 | 3 | 0 | 0 | R05_disposition.md |
| C-GROW | sweep R08 | 1 | 0/0/9 (+7) | ≈4 | ≈12 | 0 | 0 | R08_disposition.md |
| C-GROW | council r1 | 2 | Sol 0 req; Opus F1 req + 5 opt | 0 (F1: fixed-p instances fall to exact enumeration; recorded as wording) | ≈4 | 0 | 2 opt not applied | R09_R10_disposition.md |
| C-MIS | stmt lock R01 | 1 | 7 req | 7 (#1: SL attribution wrong) | 0 | 0 | 0 | R01_disposition.md |
| C-MIS | lemma checks R02, R03, R05 | 3 | V-W-A; R03 O2 paragraph GAP+FALSE; R05 statement parenthesis FALSE | ≈14 | ≈8 | 0 | 1 (R02 onset remark: "no change") | R02_R03, R05 disp |
| C-MIS | numerics N1–N7 | – | none used as proof; no refutation | – | – | – | – | R01_disposition.md #7 |
| C-MIS | mid-point R04 | 1 | 2 M + 7 m (M1: counterexample to singleton formula) | ≈6 | ≈3 | 0 | 0 | R04_disposition.md |
| C-MIS | sweep R06 | 1 | 0/3/7 (+5) | ≈5 | ≈8 | 3 (#4, #5 from R05; #3 = R02 onset remark) | 0 | R06_disposition.md |
| C-MIS | council r1 | 2 | 2 + 9 m | 0 | 11 | 2 (between seats) | 0 | R07_R08_disposition.md |
| C-PACK | stmt lock R30 | 1 | 8 req | 8 | 0 | 0 | 1 partial (#7 council scope; HQ prevails) | R30_disposition.md |
| C-PACK | item checks R31–R37 | 7 | 0 / 6 / 20 (+7) | ≈16 | ≈17 | 0 | 0 | REPORT:5-7 (§4) |
| C-PACK | mid-point R38 | 1 | 0/0/4 | 1 | 3 | 0 | 0 | R38_disposition.md |
| C-PACK | sweep R39 | 1 | 0/1/8 (+1) | ≈4 (M: W1-PXN post-council remark false) | ≈6 | 0 | 0 | reviews/R39_sweep_sol.md:7-95 |
| C-PACK | council r1 | 2 | non-blocking only | 0 | ≈10 | 0 | 0 | C1_disposition.md |
| FINAL | fidelity F1 | 1 | 0/5/5 | 5 (hypotheses restored) + ≈3 | ≈2 | 0 | 0 | F1_disposition.md |
| FINAL | council r1 | 2 | Sol 4 M / 1 m; Opus 1 M / 8 m / 5 e | ≈9 | ≈10 | 0 | 0 | C1_disposition.md |
| FINAL | council r2 | 2 | Sol 1 M / 2 m; Opus 4 m / 6 e | ≈3 | ≈10 | 0 | 1 opt not applied | C2_disposition.md |
| FINAL | council r3 | 2 | Sol 0; Opus 1 M (non-gate) / 2 m / 3 e | 1 (allocation term added after the round) | 5 | 0 | 0 | C3_disposition.md |
| W1C HQ | A1–A4 | 4 | A1 1 M; A3 5 m; A4 2 m | 8 | 0 | 0 | 0 | HQ_AUDIT/A1:7, A3:25-41, A4 |
| W2-APP | stmt lock R01 | 1 | 10 req | 10 | 0 | 0 | 0 | R01_disposition.md |
| W2-APP | lemma checks R02–R05 | 4 | 0 / 9 / 9 (+1); R05: L4 FALSE as written | ≈16 | ≈3 | 0 | 0 | R02–R05 disp |
| W2-APP | numerics | – | no refutation; vn_onset output itself wrong (omitted −2κ_E, R07 #5) | – | – | – | – | R07_disposition.md |
| W2-APP | mid-point R06 | 1 | 3 M | 0 | 0 | 3 (all fixed in L4 v2) | 0 | R06_disposition.md |
| W2-APP | sweep R07 | 1 | 0/6/16 (+1) | ≈10 (claims withdrawn or qualified) | ≈13 | ≈1 (#1, cf. R03 #1) | 0 | R07_disposition.md |
| W2-APP | council r1 | 2 | Sol 1 M / 3 m (FAIL); Opus 9 | ≈3 (Lemma ENUM added) | ≈9 | 1 (Sol 2 = Opus 2) | 0 | C1_disposition.md |
| W2-APP | council r2 | 2 | Sol 1 M / 1 m / 1 e (FAIL); Opus ≈3 + e | 1 | ≈5 | 1 (ENUM, incomplete fix) | 0 | C2_disposition.md |
| W2-APP | council r3 | 2 | ≈9 editorial | 0 | ≈9 | 0 | 0 | C3_disposition.md |
| W2-FAC-A | stmt lock R01 | 1 | 10 req | 10 | 0 | 0 | 0 | R01_disposition.md |
| W2-FAC-A | lemma checks R02–R04 | 3 | 0 / 1 / 14 | ≈8 | ≈6 | 1 (R04 #3 = R03 #1) | 0 | R02–R04 disp |
| W2-FAC-A | mid-point R05 | 1 | 1 M / 2 m | 1 (Lemma TVF, exact certificate) | 0 | 2 | 0 | R05_disposition.md |
| W2-FAC-A | sweep R06 | 1 | 0/0/13 (+4) | ≈6 (claims restricted or relabelled HEURISTIC) | ≈11 | 0 | 0 | R06_disposition.md |
| W2-FAC-A | council r1 | 2 | Sol 0 req; Opus 2 editorial + 5 opt | 0 | 9 | 0 | 0 | R07_R08_disposition.md |
| W2-FAC-B | stmt lock R01 (REJECT), R02 | 2 | R01 false swap margin + 6 req; R02 4 req | ≈10 | ≈1 | 0 | 0 | R01, R02 disp; LOG:20 |
| W2-FAC-B | lemma checks R03–R05 | 3 | V-W-A ×5 (19 items; reversed inequality, false small-p bound) | ≈14 | ≈5 | 0 | 0 | R03–R05 disp |
| W2-FAC-B | numerics N3–N7 | – | finite-n violations only; confirmed R01's counterexample | – | – | – | – | LOG:15-16; R02_disposition.md |
| W2-FAC-B | mid-point R06 | 1 | 2 items | 0 | 0 | 2 | 0 | R06_disposition.md |
| W2-FAC-B | sweep R07 | 1 | 0/2/11 (+4) | ≈5 (M: model identification; saturation claim withdrawn) | ≈12 | 0 | 0 | R07_disposition.md |
| W2-FAC-B | council r1 | 2 | Sol 0 req; Opus 2 editorial + 5 opt | 0 | 7 | 0 | 0 | R08_R09_disposition.md |
| W2-FAC-PK | stmt lock R01 (REJECT), R02 | 2 | R01 ≥4 (false swap rule; scope); R02 3 req | ≈7 (route replaced; scope narrowed) | 0 | 0 | 0 | R01, R02 disp |
| W2-FAC-PK | lemma checks R03–R05 | 3 | 0 / 1 / 8 (+6) | ≈7 (M: post-lock narrowing v3.1) | ≈6 | 0 | 0 | R03–R05 disp |
| W2-FAC-PK | mid-point R06 | 1 | 1 M / 2 m | 2 | 0 | 1 (M = R05 #1) | 0 | R06_disposition.md |
| W2-FAC-PK | sweep R07 | 1 | 0/1/5 (+5) | ≈1 | ≈10 (M: implementation handoff doc) | 0 | 0 | R07_disposition.md |
| W2-FAC-PK | council r1 | 2 | Sol 1 M / 2 m (G3 FAIL); Opus 1 m + 4 e | ≈2 | ≈6 | 0 | 1 (Opus opt 4) | R08_R09_disposition.md |
| W2-FAC-PK | council r2 | 2 | 1 m | 0 | ≈3 | 0 | 0 | R10_R11_disposition.md |
| W2-FAC-PKA | stmt locks R01, R03 | 2 | LOCK-WITH-CHANGES (not itemised) | ≈ | – | – | – | REPORT:5-7 |
| W2-FAC-PKA | lemma checks R02, R04 | 2 | R02 VERIFIED + numerics repairs; R04 7 wording/scope items | 0 | ≈7 | 0 | 0 | LOG:7-9 |
| W2-FAC-PKA | mid-point R05 | 1 | CONTINUE, minor | ≈1 | – | 0 | 0 | LOG:5 |
| W2-FAC-S5 | stmt lock R01 | 1 | ≥5 req | ≈5 | 0 | 0 | 0 | R01_disposition.md |
| W2-FAC-S5 | lemma checks R02–R04 | 3 | 0 / 2 / ≈8; R02: L1 FAILED | ≈6 | ≈4 | 0 | 0 | R02–R04 disp |
| W2-FAC-S5 | numerics | – | CC_n violated at path start at simulated n (finite-n); no refutation | – | – | – | – | LOG:21 |
| W2-FAC-S5 | mid-point R05 | 1 | 0/0/2 | 1 | 1 | 0 | 0 | R05_disposition.md |
| W2-FAC-S5 | sweep R06 | 1 | 0/1/11 (+7) | ≈5 | ≈14 | 0 | 0 | R06_disposition.md |
| W2-FAC-S5 | council r1 | 2 | Sol 3 req (G1/G2 FAIL); Opus 2 + opt | ≈3 (REPORT claims) | ≈3 | 0 | 0 | R07_R08_disposition.md |
| W2-FAC-S5 | council r2 | 2 | 0 req; 4 opt | 0 | 4 | 0 | 0 | R09_R10_disposition.md |
| W2-FAC-S5F | stmt lock R01 | 1 | REJECT (false gain formula, contradictory clause, missing hypotheses) | – (no disposition) | – | – | – | reviews/R01_statement_lock_sol.md:1-3 |
| W2-FAC-X | stmt locks R01 (REJECT), R02, R10 (T2) | 3 | 6 + 5 + ≥1 req | ≈12 | 0 | 0 | 0 | R01, R02, R10 disp |
| W2-FAC-X | lemma checks R03, R03b, R04, R05, R11, R12 | 6 | ≥3 M (X3 FAILED; conditioning; X7(G) FAILED) + ≈10 m | ≈12 | ≈3 | 0 | 0 | R03–R05, R11, R12 disp; LOG:34-66 |
| W2-FAC-X | mid-points R06, R15 | 2 | 2 m; 3 items | ≈3 | ≈2 | 0 | 0 | R06, R15 disp |
| W2-FAC-X | sweeps R07, R16 | 2 | 0/0/3 (+9); 0/0/1 (+4) | ≈2 | ≈15 | 0 | 0 | R07, R16 disp |
| W2-FAC-X | council T1 r1, r2, final | 6 | r1: Sol 1 m-req (G1 FAIL) + 2; r2, final: 0 req | 1 (REPORT §6) | ≈6 | 0 | 0 | R08_R09, R13_R14, R19_R20 disp |
| W2-FAC-X | council T2 | 1 of 2 | Sol 9.2 PASS; Opus seat R18 not completed | – | – | – | – | REPORT:16-19 |
| W2-FAC-XA | stmt lock R01 | 1 | 12 req (R1–R12) | ≈12 | 0 | 0 | 0 | R01_disposition.md |
| W2-FAC-XA | lemma checks R02(incomplete), R02b, R03, R04 | 4 | 6 + 3 + 14 required fixes | ≈18 | ≈5 | 0 | 0 | R02b, R03, R04 disp |
| W2-FAC-XA | numerics N1–N8 | – | N5: rational counterexample to the width-ε hull claim (an intermediate claim, not the target) | 1 | – | – | – | LOG:34-35 |
| W2-FAC-XA | mid-point R05 (early) | 1 | CONTINUE; not the post-key gate | 0 | – | – | – | R05_disposition.md |
| W2-LOC2 | stmt lock R01 | 1 | 2 M / 4 m | 6 | 0 | 0 | 0 | R01_disposition.md |
| W2-LOC2 | lemma checks R02, R03, R04, R06a, R06b | 5 | 0 / 2 / 10 (+5) | ≈10 | ≈6 | 0 | 1 (R06a-4) | R02–R04, R06 disp |
| W2-LOC2 | mid-point R05 | 1 | 1 m | 1 (κ ≥ 1 in the locked statement) | 0 | 0 | 0 | R05_disposition.md |
| W2-LOC2 | sweep R07 | 1 | 0/0/10 (+6) | ≈4 | ≈12 | 0 | 0 | R07_disposition.md |
| W2-LOC2 | council r1 | 2 | 3 m + 3 e | 0 | 6 | 0 | 0 | C1_disposition.md |
| W2-UNI | stmt lock R01 | 1 | 8 req | 8 | 0 | 0 | 0 | R01_disposition.md |
| W2-UNI | lemma checks R02, R03 | 2 | 0 / 1 / 7 | ≈4 | ≈4 | 0 | 0 | R02, R03 disp |
| W2-UNI | mid-point R04 | 1 | 1 M / 2 m / 1 e | 2 | 2 | 0 | 0 | R04_disposition.md |
| W2-UNI | sweeps R05a (Sol), R05b (Astra) | 2 | 0/1/14 (+3); 0/0/10 (+3) | ≈9 | ≈22 | 0 | 0 | R05a, R05b disp |
| W2-UNI | council r1 | 2 | minors only | 0 | ≈6 | 0 | 0 | C1_disposition.md |
| W2 HQ | B1–B4 red-teams | 4 | 0 / 0 / 4 (one m each) | 0 | 4 | 0 | 0 | HQ_AUDIT/B1:11, B2:9, B3:13, B4:11 |
| later | Wave3 API audit pass 1/2 (W1–W2 claims) | 2 batches | pass 1: 1 GAP (C-DLV Prop-F) → CONFIRMED-WORDING, 19 m; pass 2: 0 GAP, 13 m | 0 | ≈32 | 0 | 1 (GAP downgraded) | Wave3/API_AUDIT/pass1/TRIAGE.md, pass2/TRIAGE.md |
| later | Wave3 API audit pass 3 (stopped FAC tickets) | 1 batch | 3 GAP (S5F L0, L1; FAC-X L4r.5), 5 m | 3 (→ SUSPECT) | 5 | 0 | 0 | Wave3/API_AUDIT/pass3/TRIAGE.md |
| later | Wave3 sharp1 (C-MIS) | 1 | "fixed σ², τ²" removable (class A) | 1 statement (W3-MISR) | – | – | – | Wave3/API_AUDIT/sharp1/TRIAGE.md:35-36,57 |

**Aggregate per layer (math tickets; C-ENG and FINAL listed separately above)**

| layer | reviews | sev (F/M/m) | REAL | COSM | RR | REJ | notes |
|---|---|---|---|---|---|---|---|
| statement lock | 26 (W1 4, W1C 4, W2 18) | ≈137 req itemised; 5 REJECT verdicts (C-DLV, FAC-B, FAC-PK, S5F, FAC-X) | ≈130 | ≈7 | 0 | 1 (+1 partial) | Every lock asked for changes. A false claim or counterexample was caught at lock in ≥12 tickets (GEN, C-DLV, C-GROW, C-MIS, FAC-B, FAC-PK, S5F, FAC-X ×2, LOC2 ×2, UNI) |
| lemma line checks | ≈73 | ≈23 failed-as-written verdicts (GAP/ERROR/WRONG/FAILED/FALSE); ≈40 M | ≈210 | ≈110 | ≈3 | ≈2 | most proof corrections come from this layer |
| falsification numerics (lead) | all tickets | – | 0 lemmas or statements refuted | – | – | – | 1 intermediate claim refuted (XA N5); 1 code deviation corroborated (N3). Every counterexample to a lemma came from a reviewer, analytic or via the reviewer's own script (e.g. C-DLV R03, FAC-X R03, LOC2 R02) |
| mid-point | 19 | 0 F / 13 M | 7 new M REAL (GEN 2, C-DLV 1, C-MIS 2, FAC-A 1, UNI 1) | – | 6 M (APP 3, FAC-PK 1, FAC-B 2 items) | 0 | 19/19 CONTINUE (T5) |
| sweep | 18 | 1 E + 27 M (28 major-level) / 156 m / 66 e | ≈19 major-level REAL; ≈70 m REAL | ≈9 major-level (W1-N1 5 numerics, FAC-PK 1, APP ≈2, C-MIS 1); ≈150 m/e | ≈7 | 0 | 0 FATAL in any sweep |
| council (all rounds) | 27 rounds / ≈53 seats | blocking findings in 8 rounds (T2) | ≈25 | ≈150 | ≈6 | ≈4 opt not applied | 11/17 councilled objects passed in round 1 |
| HQ audits | 8 (A1–A4, B1–B4) | 1 M (A1) | 8 (all Wave 1C) | 4 (Wave 2) | 0 | 0 | the Wave 2 red-teams found 0 FATAL/MAJOR |
| later (Wave3 API, sharp1) | 4 batches | 4 GAP, ≈37 m | 3 GAP → SUSPECT (unreviewed lemmas); 1 strength (C-MIS) | ≈37 | 0 | 1 | pass 1/2 over council-passed W1–W2 claims: 0 surviving GAP |

## T2. Council rounds

| ticket | rd | seat | score | gates | sev (M/m/e) | blocking finding → class; new/RR |
|---|---|---|---|---|---|---|
| W1-GEN | 1 | Sol / Opus | 9.0 / 8.9 | PASS / PASS | 0 / 4 m | – |
| W1-N1 | 1 | Codex / Opus | 9.3 / 8.9 | PASS / PASS | 2 / 8 non-blocking | – |
| W1-N3 | 1 | Sol / Opus | 9.3 / 8.6 | PASS / PASS | minor (not itemised) | – |
| W1-PXN | 1 | Codex / Opus | 8.6 / 8.3 | PASS / PASS | 0/2 ; 1 M (form) / 7 m | – (Opus M non-blocking) |
| C-DLV | 1 | Codex xhigh | 7.6 | G1,G2,G3,G5 FAIL | 2 M | custom-h branch outside the work/memory envelopes → CORRECTNESS (fix narrowed CONFIG to default 𝓗); simplified allocation drops Cert/Cert_M → CORRECTNESS. Both continue the sweep #1 / R02 #2 family |
| C-DLV | 1 | Opus | 8.6 | PASS | 10 items | – |
| C-DLV | 2 | Codex / Opus | 9.0 / 8.9 | PASS / PASS | 1 m / 6 | – (7.6→9.0 driven by a real fix: statement scope + allocation display) |
| C-GROW | 1 | Sol / Opus | 9.2 / 9.0 | PASS / PASS | 0 / F1 + opt | – |
| C-MIS | 1 | Sol / Opus | 9.2 / 9.0 | PASS / PASS | 2 m / 9 m | – |
| C-PACK | 1 | Sol / Opus | 9.0 / 8.7 | PASS / PASS | non-blocking | – |
| FINAL | 1 | Sol | 7.4 | G1, G6 FAIL | 4 M / 1 m | N1 fixed-data convention dropped; Thm F TAIL-discharge cutoffs dropped; GEN (C4) favourable branch dropped; Thm D allocation hypothesis weakened → all FAITHFULNESS (chapter vs ticket source); new |
| FINAL | 1 | Opus | 8.5 | PASS | 1 M / 8 m / 5 e | – (O1 cap-ℓ_n over-transfer, non-blocking) |
| FINAL | 2 | Sol | 7.9 | G1, G6 FAIL | 1 M / 2 m | SL1(b) dropped the source's q_n ∈ (0,1) domain (false at the endpoints) → FAITHFULNESS, new; §8 "only under GR" contradicts the §3.3 EP theorem (G6) → RECORD/WORDING, new |
| FINAL | 2 | Opus | 8.8 | PASS | 4 m / 6 e | – |
| FINAL | 3 | Sol / Opus | 9.3 / 8.6 | PASS / PASS | 0 ; 1 M non-gate / 2 / 3 | – (Sol 7.4→7.9→9.3: text restorations; no ticket mathematics changed) |
| W2-APP | 1 | Sol xhigh | 8.2 | G1, G2, G6 FAIL | 1 M / 3 m | "unproved" frontier ignores the coded exact-enumeration branch → FAITHFULNESS (method as coded), new (C-GROW council Opus F1 had flagged the same mechanism in Wave 1C); summary rows drop qualifiers (G2) → RECORD/WORDING |
| W2-APP | 1 | Opus | 8.8 | PASS | 9 items | – |
| W2-APP | 2 | Sol | 8.8 | G1, G6 FAIL | 1 M / 1 m / 1 e | ENUM shortcut treated as the whole override → FAITHFULNESS; RR (r1 fix incomplete) |
| W2-APP | 2 | Opus | 8.9 | PASS | ≈3 + e | – |
| W2-APP | 3 | Sol / Opus | 9.1 / 9.1 | PASS / PASS | editorial | – (8.2→8.8→9.1: new Lemma ENUM, then generalised = real addition) |
| W2-FAC-A | 1 | Sol / Opus | 9.2 / 8.9 | PASS / PASS | 0 / 2 e | – |
| W2-FAC-B | 1 | Sol / Opus | 9.3 / 9.0 | PASS / PASS | 0 / 2 e | – |
| W2-FAC-PK | 1 | Sol xhigh | 8.6 | G3 FAIL | 1 M / 2 m | REPORT §6 exports G2 as design-free; Sol gives a counterexample at p = Kn → CORRECTNESS (REPORT claim, not the theorem); new (REPORT §6 first written at the sweep, R07 #8) |
| W2-FAC-PK | 1 | Opus | 9.1 | PASS | 1 m / 4 e | – |
| W2-FAC-PK | 2 | Sol / Opus | 9.4 / 9.2 | PASS / PASS | 0 / 1 m | – (8.6→9.4: REPORT scope restricted) |
| W2-FAC-S5 | 1 | Sol xhigh | 7.8 | G1, G2 FAIL | 3 req | REPORT's "start = whole model" false when N₀ ≠ ∅ → CORRECTNESS (REPORT); s₀ = 4 restriction dropped, Sol counter-witness at s₀ = 1 → CORRECTNESS (REPORT); unchecked exact-argmin modules not labelled → RECORD/WORDING. All new. Both seats judged Tier 1 sound |
| W2-FAC-S5 | 1 | Opus | 8.6 | PASS | 2 + opt | – |
| W2-FAC-S5 | 2 | Sol / Opus | 8.8 / 8.8 | PASS / PASS | 0 req | – (7.8→8.8: REPORT/label fixes only) |
| W2-FAC-X T1 | 1 | Sol xhigh | 8.8 | G1 FAIL | 1 m (REQUIRED) + 1 m + 1 e | REPORT §6 says log-size eigenvalue floors suffice for truth moves; Sol gives a non-CS counterexample → CORRECTNESS (REPORT); new |
| W2-FAC-X T1 | 1 | Opus | 9.0 | PASS | – | – |
| W2-FAC-X T1 | 2 | Sol / Opus | 9.2 / 9.0 | PASS / PASS | 0 req | – (would pass; R14 not dispositioned before the pause) |
| W2-FAC-X T1 | final | Astra / Opus | 9.2 / 8.9 | PASS / PASS | 0 req | – (fresh council required by the take-over brief after the pause) |
| W2-FAC-X T2 | 1 | Sol / Opus | 9.2 / – | PASS / not completed | – | ended without a pass: Opus seat R18 interrupted by the pause; then stopped (SR stop list) |
| W2-LOC2 | 1 | Sol / Opus | 9.3 / 9.1 | PASS / PASS | 1 m / 2 m + 3 e | – |
| W2-UNI | 1 | Astra / Opus | 9.0 / 8.9 | PASS / PASS | minors | – |

Rounds needed: 1 round for W1-GEN, N1, N3, PXN, C-GROW, C-MIS, C-PACK, FAC-A, FAC-B, LOC2 and UNI (11). Two rounds for C-DLV,
FAC-PK and FAC-S5. Three for FINAL and APP. FAC-X T1 took 3 councils, two of them passing. In every failed round the
Codex/Sol seat failed. The Claude Opus seat never failed a gate and never scored below 8.0 (lowest 8.3, W1-PXN). Of the
16 blocking findings, 3 were re-raises (APP r2; C-DLV r1 ×2 continuing the sweep family) and 13 were new. By class: 7
FAITHFULNESS (5 FINAL, 2 APP), 6 CORRECTNESS (2 C-DLV in the ticket's proofs; 4 in REPORT text: FAC-PK, FAC-S5 ×2, FAC-X),
3 RECORD/WORDING (FINAL r2, APP r1, FAC-S5), 0 STRENGTH.

Tickets with no council pass: FAC-X Target 2 (one seat only); S5F, XA, K2 and PKA never reached council (stopped). C-DLV
and FAC-S5 passed council but have RESULT PARTIAL: the council scored the proved reduction, not the ticket target.

## T3. Late slips (REAL CRITICAL/MAJOR at sweep, council, HQ audit or later, on an object that had already passed an earlier check)

| # | ticket | error (one line) | found by | earlier pass of the same object | why missed (record only) |
|---|---|---|---|---|---|
| 1 | W1-PXN | exact-branch bound D_n ≤ P(SMC branch, LS0 misses) false when s₀ > K (`lemmas/R_branch_repair.md:35-40`) | sweep R30 #1 (ERROR) | repair re-check R21 VERIFIED-WITH-MINOR on the same lines (R21:24, :34) | R21 flagged :35-38 as MINOR; the "by cases" edit made after R21 was not re-checked. ≈ The record does not say which version held the false clause |
| 2 | W1-PXN | common score-expansion event for the two uses of Lemma E undefined | sweep R30 #2 (GAP) | Lemma E VERIFIED (R12) | glue between lemmas: FINAL_PROOF.md was assembled after the item checks |
| 3 | W1-PXN | sharp failure rate PX:475 survived the errata; unproved | sweep R30 #3 (GAP) | E-14 erratum checked (R17/R21) | the erratum replaced the same assertion only at PX:369 |
| 4 | W1-PXN | finite-n centring rate O_P(√(log n/n)) false for slowly growing p | C-PACK sweep R39 #1 (MAJOR) | W1-PXN council C1 passed; C-PACK fidelity R36 FAITHFUL | added after the council (C1 Opus #8) and never checked; R36 checked transcription only (R39:5; C-PACK REPORT flag 3) |
| 5 | W1-PXN | Lemma T off-event centre identity; abstract block-order counterexample for the capped routine | C-PACK item check R33 #2 (MAJOR) | W1-PXN item checks + council | new use context (the e4 → e4′ replacement audit); ≈ |
| 6 | W1-GEN | L8 certificate needs bounded energy ‖μ‖² ≤ Mn | sweep R10 #1 (MAJOR) | none: L8 and Lemma SEL were never line-checked | lemma added after the mid-point (R05 #4), checked only by the sweep (REPORT:94-95) |
| 7 | C-DLV | resource lemma: allocation dropped the (n+p)²p log³ and cache terms; tie-DP cost unproved | lemma check R02 (GAP); then 4 sweep MAJORs on P2's scope | L1 "PROVED (by this seat)" after the R02 fixes | the re-check was "folded into the sweep" (R02_R04_disposition.md); L1 v2 was never line-re-checked |
| 8 | C-DLV | custom-h branch uncosted; Cert/Cert_M dropped from the simplified allocation | council r1 Codex (2 MAJOR) | sweep R06 #1 fix (premise CONFIG added) | that fix introduced CONFIG and changed the statement after lock; it was not re-checked before the council |
| 9 | C-MIS | onset 2·10⁶ exported to every result | sweep R06 #3 (MAJOR) | R02 raised it; the lead kept it ("already worded as a disclosure") | the earlier objection did not stand at the sweep |
| 10 | C-MIS | SL β₀ equals the intercept slope only for centred rows | sweep R06 #1 (MAJOR) | stmt lock R01 #1 (SL attribution fixed) | partial fix at lock |
| 11 | C-DLV × C-GROW | Prop F envelopes assume LS0 cap ℓ_n; C-GROW MR1 cap ℓ_n + \|S̃₀\| breaks them | HQ audit A1 #1 (MAJOR) | C-DLV council r2 PASS; C-GROW council PASS | glue between tickets: each passed with its own cap |
| 12 | FINAL | 5 MAJOR transcription omissions (Lemma Z Gram floor; GEN H2a/H2c; GROW NA/TL, C2/C3 antecedents; AR(1) hypotheses) | fidelity F1 | ticket councils passed the sources | errors made in transcription to the chapter |
| 13 | FINAL | 5 MAJOR transcription omissions (N1 convention, Thm F cutoffs, GEN (C4), Thm D allocation, cap-ℓ_n over-transfer) | council r1 (Sol 4, Opus 1) | F1 fidelity check | F1 was "not re-reviewed after the fixes" (F1_disposition.md); the revision also added A2/A3 and C-ENG content (C1_disposition.md) |
| 14 | FINAL | SL1(b) fixed-q clause false at the endpoints | council r2 Sol (MAJOR) | council r1 (both seats) | ≈ new at round 2; the ξ_q row had been edited in r1 (Opus O12) |
| 15 | W2-APP | frontier omits the coded exact-enumeration branch | council r1 Sol (MAJOR) | sweep R07, mid-point R06, L4 check R05 | the same mechanism was raised in Wave 1C (C-GROW R10 F1) but did not carry over to this ticket |
| 16 | W2-APP | REPORT/map claims withdrawn (tecator, onset from a wrong script, riboflavin, ≤ 1 truth per block) | sweep R07 (6 MAJOR) | L4 v2 re-checked by mid-point R06 | REPORT and numerics text not under the lemma checks |
| 17 | W2-FAC-B | model identification missing; blanket saturation claim | sweep R07 (2 MAJOR) | two statement locks (R01, R02) | not stated in the record |
| 18 | W2-FAC-S5 | E_S block-local quantifier wrong in L3 | sweep R06 #1 (MAJOR) | L3 V-W-A (R02) | not stated; L3 was also edited after R02 (c4, c1′) |
| 19 | W2-FAC-PK | REPORT §6 design-free residual floor false for p ≫ n | council r1 Sol (MAJOR) | – | REPORT §6 first written at the sweep (R07 #8); never checked before the council |
| 20 | W2-UNI | FAC-L containment claim needs fixed positive beta-min | sweep R05a #1 (MAJOR) | stmt lock R01, mid-point R04 | claim about another ticket's theorem (cross-ticket import) |
| 21 | W2-FAC-X | L4r.5 missing hypothesis/constant relation (GAP) | Wave3 API pass 3, confirmed by Sol R-AUD2 | none ("not reviewed; not used by FAC-GL", REPORT §5) | never line-checked |
| 22 | W2-FAC-S5F | L0, L1 GAPs (2 each) | Wave3 API pass 3, confirmed by Sol R-AUD2 | none (only the stmt lock, REJECT) | written after a REJECTed lock; ticket stopped |

C-DLV Prop-F (Wave3 API pass 1 GAP) is not counted: Sol R-AUD1 downgraded it to wording. Of the 22 rows: 11 concern text changed
after its last check (#1-4, #7, #8, #12-14, #16, #18: repairs, assembly, post-lock or post-council edits, transcriptions,
late REPORT text); 4 concern objects never line-checked (#6, #19, #21, #22); 4 are cross-ticket glue or reuse (#5, #11,
#15, #20); 3 other (#9 the lead's objection overturned, #10 partial fix at lock, #17 reason not recorded).

## T4. Statement history and weak targets

| ticket | narrowed / reformed / refuted | stage; layer | flagged at the time? |
|---|---|---|---|
| W1-GEN | v2 (9 lock changes); v2.1 C6 design changed (v1 singleton scored trivially); v2.2 (C1′) added; v2.3 C5(d) restricted | lock R01; line check R06 #12; mid-point R05; sweep R10 #6 | yes, REPORT flag 1 |
| W1-N1 | strengthened at lock (any bounded h; per round; δ₁) | lock SL1 | yes |
| W1-N3 | card's unconditional N3 false for the frozen code (cap 10⁶); target = true version + counterexample | before lock: lead's code reading, corroborated by numerics (LOG:6-9) | yes, REPORT flag |
| W1-PXN | (P) input changed T03 → T03♯; (R) display split ("for every t" false); exact-branch convention | lock R00; item checks R14 | yes |
| C-DLV | target (T) not delivered; reformed to reductions P1–P5 + open obstruction (O); RESULT PARTIAL | lock R01 FATAL (first ticket review) | yes, flag 1 |
| C-GROW | v2.1 piecewise relevance set (counterexample to the \|Q\| bound); v2.3 extension (C5)(c); v2.5 fixed-p caveat | line check R04; parallel prover; council Opus F1 | yes, flag 2 |
| C-MIS | narrowed vs Song–Liang at lock (inclusion vs exact model); v1.2 additions; later found weaker than provable ("σ², τ² fixed" removable by scale invariance) → W3-MISR | lock R01 (attribution); weakness: Wave3 sharp1, 2026-11-11, ≈3 days after the council | attribution yes (flag 1, "stronger hypotheses"). Removability: never raised in the C-MIS trail. Earlier signals: R01:25 notes y-standardisation with b = b₀s_y²; R02:104 "under the locked fixed-variance scope"; council G2 checks that the hypotheses used match those stated (R07:26), not whether they are needed; SR CRITIQUE:249 "Keep C-MIS" |
| C-PACK | lock changes; item checks started before the lock on v1 (protocol deviation) | lock R30 | yes (R30_disposition.md, last paragraph) |
| W2-APP | LOC-B enlargement bound added; ENUM claim (F) added after council r1 | line check R03; council r1 | yes |
| W2-FAC-A | narrowed to one factor + bounded blocks, limsup log p/log n < 1/6 (not p ≤ n^A) | lock R01 #4 (strict limsup); route limit from the lead's own analysis (LOG:27) | yes, flag 1 |
| W2-FAC-B | v1 REJECTED (false swap margin); scope = exact-Gram CS, p ≤ n/2 | lock R01 | yes, flags 1, 3 |
| W2-FAC-PK | v1 REJECTED; exact-Gram K < p ≤ n − 1 only, p ≫ n "not settled"; v3.1 post-lock narrowing | lock R01; line check R05 | yes, flags 2, 4 |
| W2-FAC-PKA | target moved to singleton (non-production) partitions; second lock R03 | lock R01, R03 | yes; stopped by SR (CRITIQUE:176) |
| W2-FAC-S5 | Tier 1 reduction only; Lemma KL open. Unconditional exponent 0.104 < FAC-A's 1/6 | lead's analysis at opening (LOG:10-14: "lattice bounds on e_T match the deletion level (=> FACA's 1/6)"); two KL prover rounds PARTIAL | yes, flag 1. SR: "unconditional exponent it would improve (0.104) is already below FAC-A's 1/6" (CRITIQUE:164) |
| W2-FAC-S5F | v1 REJECTED at lock (false gain formula); parallel duplicate of FAC-S5, "no coordination" (LOG:3) | lock R01 | stopped; later API pass-3 GAPs |
| W2-FAC-X | T1 v1 REJECTED (X3 counterexample); T2 FAC-NCS narrowed to iid rows (X7 (G) FAILED) | lock R01; line check R12 | yes, flag 3 |
| W2-FAC-XA | locked as "research target (not a theorem)"; X2 stayed open; R05 explicitly not the post-key gate | lock R01; R05 | yes; stopped by SR |
| W2-FAC-K2 | numerics only; no STATEMENT; LOG predicts a possible method-level LS0 trap | – | stopped by SR |
| W2-LOC2 | (C) split into C-i/C-ii (LSF counterexample); VN attribution restricted | lock R01 | yes |
| W2-UNI | 8 lock changes; PLR summary missing LSF (mid-point R04 M, the same split LOC2 got at its lock) | lock R01; mid-point R04 | yes |

The weak-target finding came at portfolio level, not from any ticket review. SR (Wave2/SR/CRITIQUE_fable.md, committed
2026-11-09 15:31, after the 14:51 pause) found:
- The program drifted from the binding goals: every factor result needs p < n/2, UNI-1 needs p = o(n^{1/6}), and about 2/3
  of the Wave 2 tickets sit in a regime the paper does not target (:23-26, :137-138).
- Signal conditions differ across tickets for the same design (:149-150).
- T03♯ has the lightest verification trail (:121-126).
- Stop list: FAC-S5/KL, S5F, XA, K2, PKA, FAC-X T2 (:291-292).
The ticket briefs, locks and councils each checked a statement against its own brief. No ticket-level review compared it
with the binding goals (Wave2/PROTOCOL.md:17,51 set the factor targets). The Wave1C audits A1–A4 found one cross-ticket
MAJOR (T3 #11). The Wave2 audits B1–B4 found no FATAL/MAJOR. No mid-point raised the regime issue (T5).

## T5. Mid-point verdicts

| ticket | verdict | justified by what followed? |
|---|---|---|
| W1-GEN, N1, N3, PXN | CONTINUE ×4 | all four council-passed in round 1 |
| C-DLV | CONTINUE (the reviewer said "no immediate argument closes (O)") | council passed the reduction; ticket target never proved (PARTIAL) |
| C-GROW, C-MIS, C-PACK | CONTINUE ×3 | council round 1 passed. C-MIS later weakened (T4) |
| W2-APP, FAC-A, FAC-B, FAC-PK, LOC2, UNI | CONTINUE ×6 | all council-passed (APP in r3, PK in r2) |
| W2-FAC-S5 | CONTINUE | Tier 1 passed in r2; KL never closed; stopped by SR |
| W2-FAC-X | CONTINUE (T1 R06, T2 R15) | T1 passed; T2 not council-passed, stopped |
| W2-FAC-PKA | CONTINUE | stopped by SR (non-production partitions) |
| W2-FAC-XA | CONTINUE (early; the record says it is not the post-key gate) | key lemma X2 never proved; stopped by SR |
| W2-FAC-S5F, K2, C-ENG, FINAL | no mid-point | – |

19 mid-points: 19 CONTINUE, 0 REDIRECT, 0 STOP. Each mid-point reviewer saw only STATEMENT plus proofs (e.g.
C-DLV R05, W1-N1 MP1). Four tickets that later stopped or stayed PARTIAL (C-DLV target, FAC-S5, PKA, XA) had CONTINUE.

## T6. Rework inside tickets (lemma refuted or changed after dependents used it)

| ticket | change | how noticed | dependents re-checked? | delay (LOG) |
|---|---|---|---|---|
| W1-GEN | L6(d) GAP → new Lemma SEL; C5(d) downgraded, then restricted (v2.3) | R07 line check; R05 mid-point | SEL: sweep only, no dedicated check (REPORT:94) | same day, R07 → R10 (11-08) |
| W1-GEN | L7 v1 → v2 → v3 (GAP, GAP, VERIFIED); C6 statement changed v2.1 | R06, R08, R09 | yes: L7 v3 VERIFIED at the 3rd attempt, the limit of the stop rule | same day |
| W1-N3 | L5 WRONG in (A); L6 drafted but held "not yet used, pending batch-2 check" | R02 | yes: R03 re-check of L1, L5; L6 checked in R05 | same day |
| W1-PXN | B(ii) domain, Theorem R display, LS(i), P6′ sharp cost repaired (E-1..E-20) | R13–R17 | yes: R21, a different reviewer; R30 then found an error in a repair (T3 #1) | same day |
| C-DLV | Cor 5.3 ERROR (three-model counterexample) → STATEMENT (P5)(b), (C1) updated | R03 (22:25) | Lemmas 5.2/5.2′ stood; re-check folded into the sweep R06 (22:47) | ≈22 min |
| C-GROW | \|Q\| bound counterexample → L5(a) piecewise; STATEMENT v2.1 | R04 (22:12) | via mid-point R05 and sweep R08 (22:54); R05 gave L5(a) as an audit focus | ≈40 min |
| C-MIS | singleton precision formula counterexample → STATEMENT §2(iii), L2 | mid-point R04 | yes: dedicated check R05 ("Prop P setting / P(a) (R04 edits) VERIFIED") | same day |
| C-PACK | lemmas drafted and checked (R31–R35) on statement v1 before the v2 lock | R30 lock | re-aligned to v2, then re-read by mid-point R38 and sweep R39 | same day |
| W2-APP | L4_families v1 FALSE as written → v2 | R05 | mid-point R06 re-raised 3 MAJOR already fixed; sweep found 6 more MAJOR | same day |
| W2-FAC-S5 | L1 FAILED (leakage rate); L3 (c4) and (c1′) changed while R03 (L4) ran in parallel | R02 (10:05) | R03 (10:25) reproduced the repaired bound; L4 used only \|ε\| ≤ n^{−1/2}; sweep later found an L3 MAJOR (T3 #18) | ≈20 min |
| W2-FAC-X | X3 FAILED → repaired; X7 (G) FAILED → corollary narrowed | R03 (09:40); R12 (10:33) | X3: fresh re-check R03b (09:47); X7: narrowing only | 7 min; same session |
| W2-LOC2 | lemma assumed a stronger (R2) than the locked statement → restored | R03 | via mid-point/sweep | same day |
| W2-UNI | Corollary U-LOC omitted T = ∅, needed by FAC-A's TL proof | R03 | applied to both corollaries; cross-ticket consumer FAC-A not re-checked in the record | same day |

In C-GROW (21:58) and FAC-S5 (09:55), lemma checks were launched in parallel, before the lemmas they depend on had passed
(C-GROW LOG:21; FAC-S5 LOG:30). W1-GEN's mid-point R05 ran in parallel with the R06/R07 lemma checks (LOG:36).

## T7. Cost signals

| ticket | reviewer launches | council rounds | stuck / kill |
|---|---|---|---|
| W1-GEN | 12 | 1 | L7 passed at the 3rd attempt (two GAPs) |
| W1-N1 | 6 | 1 | – |
| W1-N3 | 7 | 1 | L1, L5 at attempt 2 |
| W1-PXN | 14 | 1 | – |
| C-DLV | 10 | 2 | target not proved (PARTIAL) |
| C-ENG | 9 (2 plan + 7 code) | 0 | – |
| C-GROW | 10 (+1 parallel prover) | 1 | – |
| C-MIS | 8 | 1 | later superseded by W3-MISR |
| C-PACK | 12 | 1 | – |
| FINAL | 7 (+4 HQ audits A1–A4) | 3 | – |
| W2-APP | 13 | 3 | – |
| W2-FAC-A | 8 | 1 | – |
| W2-FAC-B | 9 | 1 | – |
| W2-FAC-PK | 11 | 2 | full method (P6) open |
| W2-FAC-PKA | 5 (+1 interim message) | 0 | stopped (SR) |
| W2-FAC-S5 | 10 (+2 KL prover rounds) | 2 | KL open; stopped (SR) |
| W2-FAC-S5F | 1 | 0 | lock REJECT; stopped (SR) |
| W2-FAC-X | 20 (+1 unfinished seat R18) | 3 for T1 + 1 partial for T2 | paused mid-pipeline, then a successor lead; T2 stopped (SR) |
| W2-FAC-XA | 5 (+1 incomplete reply) | 0 | stopped (SR) |
| W2-FAC-K2 | 0 | 0 | stopped (SR) |
| W2-LOC2 | 10 | 1 | – |
| W2-UNI | 8 | 1 | – |
| HQ audits / SR | 8 audits; SR 3 blind + 1 critique + 2 adjudications | – | – |

Total ≈ 195 reviewer launches across the scoped tickets (counted from the reply files in `reviews/`; scratch, brief and
disposition files excluded; HQ audits, SR and provers not included), 27 council rounds including FAC-X T2. No ticket hit the 3-failed-attempts STUCK rule. One
lemma (W1-GEN L7) passed on its last allowed attempt.

## What the numbers say

1. Statement locks (26) asked for changes every time (≈137 required items, ≈130 REAL; 5 REJECT). In ≥12 tickets the lock caught a false claim or counterexample.
2. Lemma line checks (≈73 reviews) returned ≈23 failed-as-written verdicts and supplied most proof corrections.
3. Lead-run falsification numerics refuted no lemma or statement. The one refutation was of an intermediate claim (XA N5). Every lemma counterexample came from a reviewer.
4. All 19 mid-points said CONTINUE. Their 13 MAJORs: 7 new REAL, 6 re-raised. Four tickets that later stopped or stayed PARTIAL had CONTINUE.
5. Sweeps (18) found 28 major-level and 156 minor findings, 0 FATAL. About a third of the major-level findings were numerics or record items (5 of them in W1-N1).
6. Councils: 11 of 17 objects passed in round 1. All 16 blocking findings came from the Codex/Sol seat; Opus never failed a gate (lowest score 8.3).
7. Council blocking findings were FAITHFULNESS (7: chapter transcription, coded exact-enumeration branch), CORRECTNESS (6: 4 of them in REPORT text, not theorems) and RECORD (3). None was STRENGTH. 13 were new and 3 re-raised.
8. Late slips (22 rows): 11 concern text changed after its last check (repairs, assembly, post-lock or post-council edits, transcriptions, late REPORT text); 4 concern objects never line-checked; 4 are cross-ticket; 3 other.
9. Weak targets surfaced outside the ticket layers: the factor-program regime drift through SR (after the Wave 2 pause), and C-MIS's removable fixed-variance hypotheses through Wave3 sharp1 (≈3 days after its council). Wave2 audits B1–B4 found 0 MAJOR.
10. Late blind API audits of council-passed W1–W2 claims found 0 surviving GAP (pass 1's one GAP became wording). The 3 confirmed GAPs were all in lemmas that had never been line-checked (S5F L0/L1, FAC-X L4r.5).

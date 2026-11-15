# Council seats head-to-head: OpenAI seat vs Claude (Opus) seat (record only)

Scope: the 43 council rounds of `WAVE12.md` T2 (27) and `WAVE3.md` T2 (16). Mined 2026-11-15, read-only. This file builds on
those two files: their round lists, scores and REAL/COSMETIC classes are reused, not redone.
**Paths.** Relative to `Theory_work/`: `W1/` = Wave1, `W1C/` = Wave1C, `W2/` = Wave2, `W3/` = Wave3/W3-; `/r/` = `/reviews/`.
"disp" = the council disposition file of that round. Seat files: OpenAI = `_sol`/`_codex`/`_astra`; Claude = `_opus`.
**Rules.** REAL = led to a change in a statement, hypothesis, proof step or status label (`WAVE3.md:11-19`). One extension,
applied the same way to both seats: a false or broadened mathematical sentence in REPORT/registry/chapter text that was
corrected counts as REAL with class "REPORT". So PSHARP R1 sol M1 counts as REAL here (WAVE3 T1 counted it cosmetic), as
POST C2 A-F1 already was. Items deferred under the frozen-manifest rule (never applied) are not REAL. "≈" = my judgement.
**Classes.** proof = proof step; stmt = statement/hypothesis text in ticket files; REPORT = REPORT/summary/registry text;
code = faithfulness to code; lit = faithfulness to literature/sources; transc = transcription (FINAL chapter); label =
status/sharpness/record label.
**Seat models.** OpenAI seat: gpt-6.1-sol (Codex) in 25 W1–2 reviews and 7 W3 reviews; gpt-6-astra in 2 W2 reviews
(FAC-X final, UNI) and 9 W3 reviews (POST ×3, POST2, RM ×2, RM2, SAMP, SCR). Claude seat: Opus 5.5 everywhere.
**Not same content.** Files changed while a seat was reviewing in 4 rounds: POST C2 (Opus read the post-fix files,
`W3/POST/r/C2_council_opus.md:6-9`); FAC-X T1 r1 (`W2/W2-FAC-X/r/R09_council_opus.md:128-131`); C-PACK
(`W1C/C-PACK/r/C1_disposition.md:10-11`); RM C2 (`W3/RM/r/C2_disposition.md:19-20`).

## S1. OpenAI-seat blocking findings vs the Claude seat on the same content

Opus column: (a) same point, (b) neighbouring point, (c) nothing; then the Opus gate verdict on the clause at issue.

| # | round | OpenAI finding (one line) | class | Opus seat on the same content | pointers (OpenAI ; Opus) |
|---|---|---|---|---|---|
| 1 | C-DLV r1 | M1: CONFIG's custom-h branch outside the proved work/memory envelopes | proof | (b) #5 MINOR: work inventory "not exhaustive", items "already dominated"; G1 PASS, G2/G3 "PASS (minor)": "No unstated assumption carries weight" | `W1C/C-DLV/r/C1_council_codex.md:11-13,20` ; `C1_council_opus.md:21-23,94` |
| 2 | C-DLV r1 | M2: simplified allocation drops Cert/Cert_M (polynomial ≠ quadratic) | proof | (c); G1/G5 PASS (G5 lists only "4000pK" and n_β slips) | `codex:28-34` ; `opus:21,25` |
| 3 | FINAL r1 | S1: N1/Cor E omit the fixed-data probability convention | transc | (c); G1 PASS: "Every theorem statement I checked matches its source" | `W1C/FINAL/r/C1_council_sol.md:16,40` ; `C1_council_opus.md:43-46` |
| 4 | FINAL r1 | S2: Thm F tail discharge lost its cutoffs; symbols undefined | transc | (b) O11 NIT: N, μ_c, X_{c,𝒞} undefined in Thm F; cutoff not raised; G1 PASS | `sol:52` ; `opus:163-166` |
| 5 | FINAL r1 | S3: GEN (C4) drops the favourable random-design branch | transc | (c); G1 PASS, names GEN (H2a)/(H2c) as checked | `sol:70` ; `opus:44` |
| 6 | FINAL r1 | S4: Thm D needs Corollary R's allocation, not "a valid" one | transc | (b) O1 MAJOR (non-blocking): Thm D/D′/CONFIG are cap-ℓ_n results; G1 "PASS (finding 1 required)" | `sol:82` ; `opus:46,69` |
| 7 | FINAL r2 | Sol 1 MAJOR: SL1(b) drops q_n ∈ (0,1); false at the endpoints | transc | (c); G4 PASS lists "the ξ_q sentence" as re-checked; Opus's own r1 O12 had edited the ξ_q map row | `C2_council_sol.md:11,20` ; `C2_council_opus.md:26`; `C1_disposition.md:33` |
| 8 | FINAL r2 | Sol 2: §8 "only under GR" contradicts the §3.3 EP theorem (G6) | REPORT | (c); G5 PASS lists "misspecification EP" present; G6 PASS "consistent across §§1, 5, 6, 7 and 8" | `sol:16,58` ; `opus:31-32` |
| 9 | W2-APP r1 | Sol 1 MAJOR: "unproved" frontier ignores the coded exact-enumeration branch | code | (b) G3: "exact-branch convention makes fixed-p sequences harmless" (growing p ≤ c log n not raised); G1/G3/G6 PASS. Same mechanism had been Opus's C-GROW F1 (Wave 1C) | `W2/W2-APP/r/C1_council_sol.md:3,8,12` ; `C1_council_opus.md:48-49,110` |
| 10 | W2-APP r1 | Sol 2 (G2): poly-Toeplitz row drops the two-sided-tail qualifier | REPORT | (a) Opus #2 MINOR, same cell; gates PASS | `sol:4` ; `opus:82-85` |
| 11 | W2-APP r2 | Sol 1 MAJOR: ENUM shortcut treated as the whole override | code | (a) Opus issue 1 MINOR, "defensible as a label"; all gates PASS | `C2_council_sol.md:3,12` ; `C2_council_opus.md:19,40-41` |
| 12 | FAC-PK r1 | Sol 1 MAJOR: REPORT §6 exports G2 as design-free; counterexample p = Kn | REPORT | (b, opposite) Opus optional 4 asked to phrase G2 *as design-free* via \|T\| ≤ K ≤ n/2; lead rejected it with Sol's counterexample; gates PASS | `W2/W2-FAC-PK/r/R08_council_sol.md:26` ; `R09_council_opus.md:143-144`; disp `R08_R09_disposition.md:14-16` |
| 13 | FAC-S5 r1 | R07-1: REPORT "start = whole model" false when N₀ ≠ ∅ | REPORT | (c); Opus's own run used N₀ = ∅; G1 PASS ("re-derived the load-bearing steps") | `W2/W2-FAC-S5/r/R07_council_sol.md:13,38` ; `R08_council_opus.md:15,25` |
| 14 | FAC-S5 r1 | R07-2: s₀ = 4 restriction of the 250-null results dropped | REPORT | (c); G2 PASS | `sol:14,42` ; `opus:47` |
| 15 | FAC-S5 r1 | R07-3: unchecked exact-argmin modules not labelled | label | (b) Opus fixes 1–2: unchecked prover output called "proved"; inconsistent status labels | `sol:55` ; `opus:85-87` |
| 16 | FAC-X T1 r1 | R08-1: REPORT §6 says log-size eigenvalue floors suffice for truth moves; counterexample | REPORT | (b) Opus #3 EDITORIAL on the same §6 row: citation "Bai–Yin" → Davidson–Szarek only; G1 PASS | `W2/W2-FAC-X/r/R08_council_sol.md:22-26` ; `R09_council_opus.md:11,145` |
| 17 | POST C1 | A-F1 MAJOR: rate optimality and YWJ comparison overclaimed | lit + label | (b) F2 MINOR: heuristic sharpness (beta-min order) stated as fact, suggests proving the fixed-p lower bound; on YWJ: "recalled, not re-read — acceptable"; G5 PASS | `W3/POST/r/C1_council_astra.md:17,36` ; `C1_council_opus.md:79-80,109,132-138` |
| 18 | POST C1 | A-F2 MAJOR: NH14 conditions misrepresented | lit | (c); explicitly accepted ("acceptable", lines 79-80); G4 PASS | `astra:46` ; `opus:79-80,108` |
| 19 | POST C1 | A-F3 (gate MINOR, G1–G3): Song–Liang qualifications missing | lit | (b) page-by-page Song–Liang check, "One loose item (N6)": r_n ≻ 1 attribution; G3 PASS | `astra:54` ; `opus:73-78,107,173` |
| 20 | POST C1 | A-F4 (gate MINOR, G2): REPORT drops coefficient / reference-size conditions | REPORT | (a) N3 NIT: "Automatic for fixed s₀" drops \|θ*_j\| ≤ θ_hi; G2 PASS | `astra:62` ; `opus:106,161` |
| 21 | POST C1 | A-F5 (gate MINOR, G5): numeric quotes need exact quantities/scope | label (num) | (b) F1 MINOR: numbers stale vs the p = 10 re-run; N1 over-tight quotes; G5 PASS | `astra:70` ; `opus:82,109` |
| 22 | POST C2 | A-F1 MAJOR: REPORT states LB outside its domain (false at p = s₀) | REPORT | not same content: Opus read the files after the lead had applied this fix; it then checked the domain ("now carry the domain") | `C2_council_astra.md:12,48` ; `C2_council_opus.md:6-9,55-57` |
| 23 | POST C2 | A-F2 (gate MINOR, G2): NH14 Cond. 4.5 parameters omitted | lit | not same content (fix applied before Opus read it) | `astra:13,56` ; `opus:8-9,144-145` |
| 24 | RM C1 | A-1 MAJOR: L2 runs labelled as (L-gain) violations though a population proxy was set | label (num) | (b) NIT 6: "observed just outside" loose, "L2 at η = 2 … far outside"; G6 PASS | `W3/RM/r/C1_council_astra.md:17,25` ; `C1_council_opus.md:114,174-178` |
| 25 | PSHARP R1 | M1 MAJOR: REPORT/registry of Claim B drop s₀ ≤ min(K−1, p/2) and s₀/p → 0; false as written | REPORT | (b) NIT-5: the same registry block's rate holds only as s₀/p → 0; dropped hypotheses not raised; G3–G6 PASS | `W3/PSHARP/r/R1_council_sol.md:11-12,18-34` ; `R1_council_opus.md:84-134,191` |

Count over the 23 rows with same content (rows 22–23 excluded): (a) 3 (rows 10, 11, 20; rows 11 and 20 at lower
severity), (b) 12, (c) 8. In all 23 the Opus seat gave PASS on every gate, including the gate the OpenAI seat failed.
By class of the 25 rows: REPORT 9, transc 5, lit 3, label 3, lit + label 1, code 2, proof 2.
W2-APP r1 Sol 3 (screened certification wording) is also cited in Sol's G6 reason (`W2/W2-APP/r/C1_council_sol.md:8`);
WAVE12 did not count it as blocking and it is not a row here.

## S2. REAL findings raised only by the Claude seat

"OpenAI seat" column: did the OpenAI review of the same round explicitly pass that object?

| # | round | Opus finding → change | class | Opus sev | OpenAI seat on that object | pointer |
|---|---|---|---|---|---|---|
| 1 | W1-GEN r1 | #1 (C3) onset aligned with L5.1; rate O(1/log n) stated | stmt | MINOR (req) | no mention; 0 required, all gates PASS | `W1/W1-GEN/r/R11_R12_disposition.md:5`; `R11_council1_sol.md:1` |
| 2 | C-DLV r1 | #1 (O) restated in exact form (P(E_n ∩ F¹_n) → 0, routes O-a/O-b) | stmt | MINOR | yes: "O identifies the correct remaining statistical obstruction" | disp `:10`; `C1_council_codex.md:40` |
| 3 | C-DLV r1 | #2 C1 measured status / tier-1 restriction | label | MINOR | yes: classification "substantively honest" | disp `:11`; `codex:38` |
| 4 | C-DLV r1 | #3 Prop F fallback proof: last successful construction | proof | MINOR | yes: "no error in … the delivery/consistency arguments" | disp `:12`; `codex:11` |
| 5 | C-DLV r1 | #4 L4 Setting omits CONFIG, TDP-IMPL | stmt | MINOR | yes: G4 PASS on L4's inputs | disp `:13`; `codex:14` |
| 6 | C-DLV r1 | #7 C2/D′ exact sources and class hypotheses | stmt | MINOR | yes: G4 PASS | disp `:16`; `codex:14` |
| 7 | C-DLV r2 | #1 P1, L2 S.3 relabelled AUDITED (code reading) | label | MINOR | all gates PASS, no mention | `W1C/C-DLV/r/C2_disposition.md:6` |
| 8 | C-GROW r1 | F1 fixed-p instances fall to the exact-enumeration branch; (C5)(b) v2.5 (WAVE12 classed it wording) | code | required | no required fix; G1–G6 PASS | `W1C/C-GROW/r/R09_R10_disposition.md:5-8` |
| 9 | FINAL r1 | O1 Thm D/D′/CONFIG are cap-ℓ_n results; §7 over-transfer | transc | MAJOR | yes: G3 "The positive transfer list is valid" | `W1C/FINAL/r/C1_disposition.md:21`; `C1_council_sol.md:13` |
| 10 | FINAL r1 | O4a caps below ℓ_n; O4b GROW needs "some maximiser" | transc | MINOR | yes: same G3 sentence | disp `:24-25` |
| 11 | FINAL r1 | O5 Thm S row attached C-DLV status to corrected Prop F | label | MINOR | yes: G2 PASS, "original fallback result is distinguished" | disp `:26`; `sol:12` |
| 12 | FINAL r1 | O9 e4 definition dropped the tie rule | transc | MINOR | no mention | disp `:30` |
| 13 | FINAL r2 | Opus 1 model G on random-design GEN members (Prop F) | transc | MINOR | yes: G3 PASS; checked Lemma S delivery inputs | `C2_disposition.md:19`; `C2_council_sol.md:122` |
| 14 | FINAL r2 | Opus 2 Thm S row "unconditionally" → qualifier | REPORT | MINOR | G5 PASS, no mention | `C2_disposition.md:20` |
| 15 | FINAL r3 | Opus 1 branch head moved; allocation term added to Prop F | code | MAJOR (non-gate) | yes, opposite: "later preflight changes must not be substituted for the chapter's snapshot" | `C3_disposition.md:10-11`; `C3_council_sol.md:11` |
| 16 | FAC-PK r1 | M1 delivery claim refers to unplumbed code; (P4)(iii) clarified | stmt | MINOR | G6 PASS | `W2/W2-FAC-PK/r/R08_R09_disposition.md:10`; `R08_council_sol.md:14` |
| 17 | FAC-S5 r1 | R08-1 "provers proved the lattice bound" → round 2 only, unchecked | label | fix 1 | passed the content: "a valid obstruction"; label not raised | `R07_R08_disposition.md:11`; `R07_council_sol.md:34` |
| 18 | FAC-S5 r1 | R08-2 lemma-header statuses | label | fix 2 | G4 PASS | disp `:12`; `sol:16` |
| 19 | POST C1 | B-F2 heuristic sharpness stated as fact → labelled | label | MINOR | neighbouring A-F1 (rate side) | `W3/POST/r/C1_disposition.md:19` |
| 20 | POST C1 | B-F3 p ≥ 2 unstated → added to R1 and Lemma 1a | stmt | MINOR | yes: G2 "The formal theorem passes" | disp `:20`; `C1_council_astra.md:14` |
| 21 | POST C1 | B-F4 counterexample unlabelled → "numerical, E5; sketch, unchecked" | label | MINOR | yes: "The specificity counterexample is independently valid" | disp `:21`; `astra:30` |
| 22 | POST2 C1 | B-4 Claim D Hellinger is intercept-free → D4 Remark 0 | stmt | MINOR | G6 PASS, no mention | `W3/POST2/r/C1_disposition.md:14`; `C1_council_opus.md:143` |
| 23 | POST2 C1 | B-5 m♯ ≥ min(j₀, K) used, not proved → Lemma E0 | proof | MINOR | yes: astra re-derived "m♯ ≥ B eventually" inline | disp `:15`; `C1_council_astra.md:54` |
| 24 | POST2 C1 | B-7 Claim B implies Lemma 1a exactly | stmt | NIT | no mention | disp `:17` |
| 25 | POST2 C1 | B-10 two REPORT overstatements | REPORT | NIT | no mention | disp `:20` |
| 26 | RM C1 | B-2 SHARPNESS read as if shipped LS0 succeeds on FAC-PK class | label | MINOR | G6 FAIL on SHARPNESS L2 only; no mention | `W3/RM/r/C1_disposition.md:17` |
| 27 | RM C1 | B-6 "fails in general" rests on a heuristic → reworded in STATEMENT §6 | label | NIT | no mention | disp `:21` |
| 28 | RM C2 | B1 SHARPNESS (V) on GEN (C6) fails in one sub-case → by cases (PC1: proof repair) | proof | NIT | G1 PASS, no mention | `C2_disposition.md:13` |
| 29 | RM C2 | B4 bridge row B2 lists (FL_b), only (G3a) used | stmt | NIT | G2 PASS | disp `:16`; `C2_council_astra.md:9` |
| 30 | START R1 | O1 Setting F also allows any A > 0 (C-GROW has A ≥ 1) | stmt | NB | yes: G4 checked C-GROW L0.1/L0.2 imports | `W3/START/r/R1_disposition_v134.md:12`; `R1_council_sol.md:10` |
| 31 | START R1 | O4 L3.3 shows e^{2κ_E+1}, proof gives e^{2κ_E+ς_n} | stmt | NB | yes: LEAK (L3) "accepted" | `v134:14`; `sol:21` |
| 32 | MISR R1 | F3 (E^σ) obstruction stated as fact → "numerical, with an analytic sketch" | label | MINOR | yes: sol re-derived the obstruction | `W3/MISR/r/R1_SW1_disposition.md:18`; `R1_council_sol.md:69` |
| 33 | MISR R1 | F5 §3(a) stated over 𝒦⁰_n, proof uses the first (OS) inequality only → 𝒦⁰′_n | stmt | MINOR | no mention; gates PASS | `R1_SW1_disposition.md:20` |
| 34 | PSHARP R1 | MINOR-1 registry A:COEF-REP NECESSARY → FAILED-REMOVAL | label | MINOR | no mention (G4 FAIL on M1 only) | `W3/PSHARP/r/R1_disposition.md:11` |
| 35 | PSHARP R1 | NIT-1 unproved existence remark removed | stmt | NIT | no mention | disp `:12` |
| 36 | PSHARP R1 | NIT-5 registry rate → c(p, s₀)/√n | REPORT | NIT | neighbouring (M1, same block) | disp `:16` |
| 37 | SAMP C1 | #1 PC scope vs 𝓜_r → PC(i) includes 𝓜_r | stmt | NB | no mention | `W3/SAMP/r/C1_disposition.md:16` |
| 38 | SAMP C1 | #2 D omits the KERNEL premise | stmt | NB | yes: G2 "START/KERNEL … explicit" | disp `:17`; `C1_council_astra.md:14` |
| 39 | SAMP C1 | #3 TR-b endpoint proof slip | proof | NB | G1 PASS, no mention | disp `:18` |
| 40 | SAMP C1 | #8 constant 19 holds only for B = 16 → (B+3)o₁ ≤ 19o₁ | stmt | NB | yes: G5 "Checked 19 = 16 + 3" | disp `:23`; `astra:17` |
| 41 | SCR C1 | Opus 1 κ, b, M must be fixed for M4/A1 → added (v3.4) | stmt | MINOR | yes: re-derived A1, M4; G5 "No … nonuniform asymptotic step found" | `W3/SCR/r/C1_disposition.md:17`; `C1_council_astra.md:11,40,48` |

41 rows (W1–2: 18 rows, 19 items; W3: 23). The OpenAI seat explicitly passed the object in 19 of the 41 rows (rows marked "yes").
Opus severity on these: MAJOR 2, MINOR or unlabelled required fix 26, NIT 7, unlabelled non-blocking 6.
Not REAL by the rule but substantive: FAC-X final R20-1 (uniform-in-𝔫 form of (C2)(ii) false beyond ½; remark only,
`W2/W2-FAC-X/r/R19_R20_disposition.md:21-26`); UNI B MINOR-3 (sharper κ_J, not incorporated, `W2/W2-UNI/r/C1_disposition.md:18`).

## S3. REAL findings unique to the OpenAI seat that did not block, and findings raised by both

| round | OpenAI finding → change | class | sev | Opus on that object | pointer |
|---|---|---|---|---|---|
| FINAL r1 | S5 BM(c), empty-max, f in Lemma UM, e4′ coded-routine clause (≈ REAL) | transc | MINOR | neighbouring O4b/O9 (e4, e4′) | `W1C/FINAL/r/C1_disposition.md:16` |
| FAC-X T1 r1 | R08-3 §6 states the checked class first; Target-2 labelled unchecked | label | EDITORIAL | Opus saw it already being fixed during its review | `R08_R09_disposition.md:8`; `R09_council_opus.md:128-131` |
| FAC-PK r1 | Sol 2 G1 uses CS-specific Δ_k → generic budget (≈ REAL) | REPORT | MINOR | no mention | `R08_R09_disposition.md:6` |
| POST C1 | A-F8 benchmark boundary terms; boundary cases not claimed | label | MINOR | no mention | `W3/POST/r/C1_disposition.md:16` |
| POST2 C1 | A-2 N4/N2 evidential wording (later found not fully propagated, PC1 P2) | REPORT | MINOR | no mention | `W3/POST2/r/C1_disposition.md:10`; `PC1_postcouncil_diff_sol.md:50` |
| START R1 | S3 (N1) needs κ_V > ½ (applied v1.3.4) | stmt | NB | no mention | `W3/START/r/R1_disposition_v134.md:11` |
| SCR C1 | Astra 1 M6 prose on b_𝓗 | stmt | MINOR | no mention | `W3/SCR/r/C1_disposition.md:16` |

**REAL findings raised by both seats independently: 5.** W2-APP r1 Sol 2 / Opus #2 (S1 row 10); W2-APP r2 Sol 1 MAJOR /
Opus 1 MINOR (row 11); POST C1 A-F4 MINOR / B-N3 NIT (row 20); POST C1 A-F7 MINOR / B-N7 NIT, design family inside
Theorem 1 (`W3/POST/r/C1_disposition.md:15,28`); POST2 C1 A-1 / B-1 MINOR, scope flag undercount (`W3/POST2/r/C1_disposition.md:9`).
In 4 of the 5 the OpenAI seat graded it higher. Shared cosmetic items: C-MIS ×2, RM2 F1/A1, START S1/O3, START2 sol 2/opus 7,
W2-APP r3 ×2, PSHARP m2/MINOR-2.

## S4. Totals per seat family

Finding counts are numbered items in the dispositions (optional items included); W1-N3 (not itemised) and FAC-X T2 (one
seat) are left out of the per-review means.

| | OpenAI W1–2 | Opus W1–2 | OpenAI W3 | Opus W3 |
|---|---|---|---|---|
| seat-reviews | 27 (sol 25, astra 2) | 26 | 16 (astra 9, sol 7) | 16 |
| findings (reviews counted) | ≈55 (25) | ≈196 (25) | ≈42 (16) | ≈133 (16) |
| mean findings / review | ≈2.2 | ≈7.8 | ≈2.6 | ≈8.3 |
| REAL unique to the seat | 15 (+2 ≈) | 19 | 10 | 23 |
| … by class | transc 5 (+1), REPORT 5 (+1), proof 2, label 2, code 1 | stmt 5, transc 5, label 5, code 2, proof 1, REPORT 1 | lit 4, REPORT 3, stmt 2, label 1 | stmt 12, label 6, proof 3, REPORT 2 |
| REAL shared with the other seat | 2 | 2 | 3 | 3 |
| deferred / not applied (frozen content or by choice) | ≈2 | ≈5 | ≈6 | ≈31 |
| cosmetic (remainder) | ≈35 | ≈169 | ≈23 | ≈76 |
| rejected by the lead with evidence (false positive) | 0 | 1 (FAC-PK opt 4) | 0 | 0 |
| rejected on a policy/scope ruling | 1 (W1-N1 Codex 2, Lean) | 0 | 0 | 1 (START R1 O2, owner's rule) |
| gate FAILs | 8 | 0 | 4 | 0 |
| REAL (unique + shared) per review | ≈0.6 | ≈0.8 | ≈0.8 | ≈1.6 |

Pointers: FAC-PK opt 4 `W2/W2-FAC-PK/r/R08_R09_disposition.md:14-16`; Lean `W1/W1-N1/r/C1_disposition.md:14`; O2
`W3/START/r/R1_disposition_v134.md:13`. Of the 12 failing OpenAI seat-reviews, 1 rested on ticket proof steps (C-DLV r1),
2 on chapter transcription (FINAL r1–r2), 2 on fidelity to the coded exact branch (W2-APP r1–r2), and 7 on REPORT/registry,
literature or numerics-label text.

**Thoroughness signal (rough).** Script count over the 85 review files: lines matching re-derived / recomputed /
checked against / re-ran / re-implemented / "I checked|verified|computed" ("deriv"), and pointers into `Scripts/`, `cpp/`,
`v3_*.h|R|cpp`, `*.py:`/`*.R:`/`*.h:` ("code"). Rough: wording differs by model, one line may hold several checks, and
OpenAI files put a paragraph on one line. Raw output: scratchpad `thor.txt` (not committed).

| family | reviews | words / review | deriv lines / review | code pointers / review | reviews with ≥1 deriv | with ≥1 code |
|---|---|---|---|---|---|---|
| OpenAI W1–2 | 27 | 1614 | 2.0 | 4.7 | 20 | 20 |
| Opus W1–2 | 26 | 2001 | 4.5 | 10.8 | 26 | 19 |
| OpenAI W3 | 16 | 1783 | 2.5 | 4.2 | 15 | 11 |
| Opus W3 | 16 | 2654 | 7.2 | 7.9 | 16 | 15 |

Both seats wrote their own check scripts in some rounds (e.g. `W1C/C-PACK/r/C1_sol_checks.py`, `W2/W2-APP/r/C?_scratch_sol`,
`W3/POST/r/C2_scratch_astra`; Opus: `W2/W2-UNI/r/C1_scratch_opus/joint.py`, `W2/W2-APP/r/C2_scratch_opus/enum_boundary.py`).

## S5. Wrong passes, and seat suggestions that carried an error

| # | object | later REAL error | found by | passed at council by | in council content? | pointer |
|---|---|---|---|---|---|---|
| 1 | MISR R1 | "scalar covariance necessary" overstated (necessity label) | sweep SW1-2, same manifest d3f5c91 | both (sol 9.3, opus 8.7) | yes | `W3/MISR/r/R1_SW1_disposition.md:3-5,29` |
| 2 | FINAL r1 | SL1(b) fixed-q clause false at q ∈ {0, 1} | Sol at r2 | both r1 seats (Sol failed r1 on other items) | ≈ yes (WAVE12 T3 #14 marks ≈) | `WAVE12.md:215`; `W1C/FINAL/r/C2_disposition.md:10-12` |
| 3 | W1-PXN | Lemma T off-event centre identity; capped-routine counterexample | C-PACK item check R33 #2 | both | ≈ (new use context) | `WAVE12.md:206` |
| 4 | C-DLV × C-GROW | Prop F envelopes assume cap ℓ_n; C-GROW MR1 cap breaks them | HQ audit A1 #1 | both seats in C-DLV r2 and in C-GROW r1 | each council saw only its own ticket (cross-ticket) | `WAVE12.md:212` |
| 5 | W1-PXN | finite-n centring rate O_P(√(log n/n)) false for slowly growing p | C-PACK sweep R39 #1 | both (PXN r1) | no: added afterwards, from **Opus #8's optional sentence** | `W1/W1-PXN/r/C1_council_opus.md:50,69-70`; `W1C/C-PACK/r/R39_sweep_sol.md:7-23` |
| 6 | POST2 | D3 chain "4 ≤ 2" at `D_hellinger.md:53` | post-council diff PC1 | both | no: written by the lead after the vote while applying **Opus B-5** (which cited the same line) | `W3/POST2/r/C1_council_opus.md:152`; `PC1_postcouncil_diff_sol.md:44-48` |
| 7 | FINAL r3 | Prop F allocation addition needed 2 MINOR fixes (U_K, archive bytes) | HQ audit A4 | – | no: added after round 3 from **Opus r3 #1** | `W1C/FINAL/r/C3_disposition.md:41-51` |
| 8 | FAC-PK r1 | G2 "design-free via \|T\| ≤ K ≤ n/2" would be false for p ≫ n | lead, using Sol's counterexample | – | never applied (**Opus optional 4**, rejected) | `W2/W2-FAC-PK/r/R08_R09_disposition.md:14-16` |

Not errors, listed for completeness: C-MIS fixed σ², τ² removable (weaker than provable; Wave3 sharp1 ≈3 days after a
both-seat pass, `WAVE12.md:240`); SAMP post-vote edits from Opus #1–#3 (PC1 maths CLEAN, `WAVE3.md:99`); SCR v3.4 post-pass
addition from Opus 1 (never diff-checked, no error found, `WAVE3.md:205`). API audits found 0 surviving GAP in
council-passed claims (W1–2 pass 1/2; W3 58 claims); the 3 confirmed GAPs were in lemmas no council reviewed (`WAVE12.md:347`).
No case was found where an OpenAI-seat suggestion, once applied, was later found false; POST2 PC1 P2 found the A-2 fix
incompletely propagated (`PC1_postcouncil_diff_sol.md:50`), as P3 did for the B-10 fix (`:52`).

## S6. Sol vs Astra in the OpenAI seat; the Opus seat by lead model

| OpenAI model | reviews (W1–2 / W3) | gate FAILs | mean score | findings / review | REAL (unique + shared) / review |
|---|---|---|---|---|---|
| gpt-6.1-sol | 32 (25 / 7) | 9 (8 / 1) = 28% | 8.82 / 8.96 | ≈2.2 / ≈1.9 | ≈0.68 (17/25) / 0.29 (2/7) |
| gpt-6-astra | 11 (2 / 9) | 3 (0 / 3) = 27% | 9.10 / 8.86 | ≈2.0 / ≈3.2 | 0 (0/2) / ≈1.2 (11/9) |

Confounds: all 7 W3 sol reviews are on Fable-led tickets under the frozen-manifest rule (findings deferred, not applied);
5 of 9 W3 astra reviews are on Opus-led tickets (POST ×3, POST2, SAMP). Astra's 3 FAILs are POST C1, C2 and RM C1.

Lead model: recorded as Opus 5.5 in 12 of the 17 W1–2 tickets, not recorded in 5 (W1-N1, N3, PXN, C-DLV, FINAL; Wave1
`PROTOCOL.md:35` allowed Fable only for short steps). W3: Opus leads POST, POST2, SAMP (5 rounds); Fable 5.2 leads RM, RM2,
START, START2, MISR, PSHARP, SCR (11 rounds) (LOG/BRIEF/REPORT headers of each ticket).

| Opus seat, by lead | reviews | mean Opus score | findings / review | Opus-unique REAL / review |
|---|---|---|---|---|
| W1–2 (Opus lead or unrecorded) | 26 | 8.85 | ≈7.8 | 0.73 (19/26) |
| W3, Opus lead | 5 | 8.66 | 10.0 | 2.2 (11/5) |
| W3, Fable 5.2 lead | 11 | 8.95 | 7.5 | 1.09 (12/11); 1.7 (12/7) leaving out the 4 rounds whose items were all deferred (START R2, START2 R1, MISR R2, PSHARP R2) |

## What the numbers say

1. 43 rounds, 85 seat-reviews (OpenAI 43, Opus 42). All 12 failing seat-reviews were the OpenAI seat; Opus passed every gate in every round.
2. 25 OpenAI blocking items checked (S1). On the 23 with the same content, Opus raised the same point in 3 (2 at lower severity), a neighbouring point in 12, nothing in 8. Each time it passed the gate the OpenAI seat failed.
3. By class the 25 OpenAI blocking items were: REPORT 9, transcription 5, literature 3, labels 3, literature + label 1, code 2, ticket proof steps 2 (both C-DLV r1).
4. Opus-only REAL findings: 42 items in 41 rows (19 W1–2, 23 W3), almost all graded MINOR/NIT/non-blocking; 2 MAJOR, both non-gate (FINAL r1 O1, r3 #1).
5. In 19 of those 41 rows the OpenAI seat explicitly passed the same object (e.g. SAMP "Checked 19 = 16 + 3"; POST2 m♯ re-derived inline; SCR M4 re-derived).
6. OpenAI-only REAL: 25 (+2 ≈) in total (W1–2 15 + 2 ≈, W3 10), 20 of them blocking. Both seats independently: 5 REAL items.
7. Opus writes 3.2–3.5× more findings per review (≈7.8–8.3 vs ≈2.2–2.6). Its share that is REAL is lower; its count of REAL items per review is higher (≈0.8 vs ≈0.6 W1–2; ≈1.6 vs ≈0.8 W3).
8. Rough thoroughness counts: Opus has 2.2–2.9× the re-derivation mentions per review; code pointers 2.3× in W1–2 and 1.9× in W3.
9. Wrong passes: 1 clear both-seat pass of a REAL error in council content (MISR R1, sweep SW1-2), plus 3 ≈/cross-ticket cases. 4 cases link an error to an Opus suggestion: 3 applied after the vote (PXN #8 sentence false; POST2 B-5 repair written with a false line; FINAL r3 #1 needed 2 MINOR fixes) and 1 rejected before use (FAC-PK opt 4). None links to an OpenAI suggestion.
10. Sol and Astra fail at the same rate (28% vs 27%). Opus seat scores are flat across lead models (8.66–8.95). Its REAL yield per review is higher on Opus-led W3 tickets (2.2 vs 1.1), confounded by frozen-content deferrals on the Fable-led tickets.

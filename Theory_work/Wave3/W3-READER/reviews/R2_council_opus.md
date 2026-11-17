# W3-READER — CP3 council, round R2, seat `opus`

Reviewer: Claude Opus 5.5 (effort high). Content reviewed: `MANIFEST 3af23c3572d21511fe59fe7a610991eb2b92858e0309a8ee7ac1e8ff43636a4b`.

**Freeze check.** `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-READER Theory_work/Wave3/W3-READER/reviews/MANIFEST_R2.txt`
printed `verify: OK MANIFEST 3af23c3572d21511fe59fe7a610991eb2b92858e0309a8ee7ac1e8ff43636a4b`.

**What I read.**
- *Under review (all of each file):* `READER_VERSIONS.md` (1–1392), `CLAIMS_CARD.md`, `NOTATION.md`, `METHOD_INTUITION.md`,
  `STATEMENT.md`, `REPORT.md`, `lemmas/R3_delivery_assembly.md`, `lemmas/R4_printed_outputs.md` and `lemmas/B3_8_orth_witness.md`.
  `lemmas/R1`, `R2` are byte-identical to the R1 freeze (git diff 3e1e5a5c..HEAD), and I re-used my R1 re-derivation of them.
- *Diff of the frozen content against the R1 freeze* (git diff 3e1e5a5c..HEAD). I restricted it to the files under review;
  `LOG.md` was not opened.
- *Under `reviews/`:* only `BRIEF_R2_opus.md`, `MANIFEST_R2.txt`, `R1_council_opus.md` and `R1_council_sol.md`.
- *Masters and sources:*
  - `W3-PSHARP/STATEMENT.md:88-112` and `W3-POST/lemmas/LB_rate_lower_bound.md:1-30`;
  - `W3-RM2-R/STATEMENT.md:36-182`, i.e. (D), IDEAL-W⁺, (T1-F♭), (V♭), (BM-W⁺)/(BM-Q♭), RM0-plus, DLV-0, RM2-F-plus, RM2-R-plus;
  - `W3-SCR/STATEMENT.md:45-92`;
  - `claims.tsv` rows for 24 ids (W3-RM2 Ex-Proxy, Ex-Equi, Ex-PolyF, Ex-PolyR; RM2-R-plus, RM2-F-plus, DLV-0; SCR A1, A-inf,
    SCR-C; N1; SAMP C; START2-R IF-START; POST2 C; POST Thm-1, Cor-1R; SOP:TH09; PSHARP-R AE; DIST Thm-A; MISR-R CorGb-plus;
    W2-APP POST; RM2 RM2-F, RM2-R; F-UNI);
  - code: `v3_fit.R:75-175`, `v3_run.R:85-170`, `v3_calib.R:115-172`, `cpp/v3_calib.h:22-46`, `cpp/v3_engine.h:295-325`,
    `cpp/v3_score.h:60-72`, `cpp/v3_core.cpp:120-140` and all `resource_limit` sites.
- *B3.8 source check:* B3.8's source file (theory/W3-PSHARP-R `reviews/post_cp3/BRIDGE_orth_thm1.md`, outside the manifest)
  was only hashed, to confirm the copy.

**Checks run** (`reviews/R2_scratch_opus/r2_check.py`).
- **B2.1** with exact ceilings, harmonised constant: A ∈ {1,…,20}, s₀ ≤ 39, log n ∈ [1.1, 35]. 0 violations of
  k̄ₙ < (2.4664As₀ + 3.6996s₀ + 4.9327) log n ≤ 5(A+1)(s₀+1) log n; worst ratio 0.99986.
- **B3.8 identity:** (s₀+1)(p−s₀) − (2p−1−s₀) = (s₀−1)(p−s₀−1), together with f_p ≥ ½ for s₀ ≤ p/2. Checked for
  s₀ < 60, p < 400 with 0 failures.
- **Theorem 7 (A5)(b) ⇒ (BM-Q♭):** I checked that some explicit C_Q exists. C_Q > max{32, 64A + c}, with c the
  (BM-Q♭) constant, works for all large n when p ≤ n^A. This holds on the tested grid and also analytically.
- **B3.8 copy:** `tail -n +2 lemmas/B3_8_orth_witness.md` has sha256 `d54a2a7a3759…`, equal to the source file and to the
  blob at 34d56f5b. The copy is verbatim apart from its one-line provenance header.

---

## Per-claim decisions

| id | decision |
|---|---|
| `W3-READER:PoolZ` | ACCEPT |
| `W3-READER:R1` | ACCEPT |
| `W3-READER:R2` | ACCEPT |
| `W3-READER:R3` | ACCEPT (as the historical lemma it now is: target restricted to the hypotheses of `W3-RM2:RM2-R` / `RM2-F`) |
| `W3-READER:R4` | ACCEPT |
| `RV/thm1` (Theorems 1, 1′; row 1.1 Form A) | ACCEPT |
| `RV/thm2` | ACCEPT |
| `RV/thm3` | ACCEPT |
| `RV/thm4` | ACCEPT |
| `RV/thm5` | ACCEPT |
| `RV/thm6` | ACCEPT |
| `RV/thm7` | ACCEPT |
| `RV/thm8` (Theorems 8, 8′; row 3.7 form (a)) | ACCEPT |
| `RV/thm9` (9, 9B, 9C) | ACCEPT |
| `RV/thm10` (and remark row 3.5) | ACCEPT |

---

## Verification of the R1 fixes

| R1 item | where now | check | verdict |
|---|---|---|---|
| S3 (opus) / S1 (sol): lower-bound domain | RV:148, :160 | Corollary B holds for 0 ≤ s₀ ≤ K−1 and its consequences for s₀ ≤ min(K−1, p/2) (`W3-PSHARP/STATEMENT.md:92-104`). Prop. LB needs 1 ≤ s₀ < p and s₀+1 ≤ K (`LB_rate_lower_bound.md:10-11`). The restored domain is the master's, or narrower. | fixed (see E2 for a precision) |
| S2 (sol): row 3.2 case (b) beta-min | Card:69 | The row now carries θ*²_min ≥ C_Q σ*²(\|Q\|+log n)/(nφ₀²) for (b), as Theorem 7 (A5)(b) (RV:829). | fixed |
| S2 (opus) / F1 (sol): printed vs potential Ẑ | Card:72, :80; METHOD:128; STATEMENT:21-23, :37-38 | All three places now say: potential uninterrupted records; equal to the printed field on completed runs; no unbiasedness conditional on completion. PoolZ has "data fixed", and its joint-law form is "consequently, under H-U/SI". This is exactly N1 :86-88, :98-104. | fixed (E1: duplicated phrase) |
| F2 (sol): R3 target | R3:1-18, :57-60; REPORT:34-38; STATEMENT:45; RV:758, :1383 | R3 is restricted to the RM2-R / RM2-F hypotheses and labelled historical. Current Theorems 6–7 use only B6.6′ / B7.5 with DLV-0. Every "(S4)(v)" reference is gone. I re-derived R3 against `L5_delivery.md`: union bound for (S), identity for (P), operational premises carried. | fixed |
| F3 (sol): moderate-n shape | RV:152-155, :1315-1317; Card:159-164; METHOD:111-115, :149-151 | Every instance is labelled an Engineering observation (D-17), with an explicit "no general finite-n statement". The χ² mechanism sentence is removed. | fixed |
| F4 (sol): code facts | METHOD:51-53, :76-80, :92-94, :107-117; NOTATION:121-123 | Re-read against the code. Prior: `log((2p−1−k)/(k+1))` (`v3_score.h:64-65`). Occam cost comes from m(S). Pilot forced floor: `v3_calib.h:39-44`. Fallback "last successful construction, else pilot schedule", tier 1 only: `v3_calib.R:120-124, 160-166`. Initial factor m(∅)Z̄₀: `v3_engine.h:299`. Preflight timing has no ledger: `cpp/v3_core.cpp:123-137`. Preflight stop happens before any record: `v3_fit.R:117`. | fixed |
| S1 (opus) / F5 (sol): row 3.6 AR/block | Card:73; METHOD:128 | "for particular AR or block designs that satisfy Theorem 6's visibility, leakage, floor and local-regression conditions, row 3.1 still gives the reported-model result". This makes no claim about a design family. | fixed |
| F6 (sol): F-UNI description | RV:747; Card:6, :68 | `L5_delivery.md:8-12` states the shipped cap; C-DLV Prop-F used ℓₙ; DLV-0 is the active route. | fixed |
| S4 (opus): row 3.7 "Buys" | Card:74 | Narrowed to "the only guarantee about the reported model's support …". | fixed |
| S5 (opus): row 3.3 | Card:70; METHOD:71-72 | "with probability tending to one" is in both clauses and in METHOD. | fixed (E3: "at least") |
| S6 (opus): Thm 7 honest limits (ii) | RV:892-893 | "Theorem 6, which gives the same conclusion under population analogues". | fixed |
| E1 (opus): Thm 5 leakage form | RV:600-601 | Only "l ∉ S₀" changes, as in (L-R⁺⁺). | fixed |
| E2 (opus): Thm 7 Remark (a) | RV:845-846 | Now worded as the master's (BM-Q♭) replacement, which matches `W3-RM2-R/STATEMENT.md:107-112` with c = max{c_TL,16}. | fixed (E4: dangling pointer in (A5)(b)) |
| E2 (sol): Thm 8′ gain | RV:956-959 | The formula equals `W3-SCR/STATEMENT.md:51-56` (λ₀ = 1/(n+1)), including the (n+1)/n factor. | fixed |
| E3–E11 (opus), E1 (sol) | R3, R4, REPORT, RV:23, :300, :700, :894-897, Card:34-35, METHOD:80, :105 | Updated as described. REPORT line ranges match the files (R1 59, R2 43, R3 63, R4 51 lines). The B3.8 record is copied verbatim (sha verified). | fixed (E5, E6 leftovers) |
| GUARD-W (new, HQ) | RV:695, :1304, :1310; Card:68, :72, :73 | Checked against the code. Every `resource_limit` return sets `partial_results` and NA's the estimate fields (`v3_fit.R:84-85`, `v3_run.R:105-114`). A time-guard stop in calibration (`v3_calib.R:81, 113`, `v3_fit.R:154-159`) or in the final run (`v3_run.R:142-145`) returns the ledger HPM marked `hpm_incomplete`. "No output" therefore matches NOTATION §5's output event 𝒪. The sentence restricts and claims nothing new. | supported |

---

## Re-derivations (G1, G2)

**PoolZ** (`STATEMENT.md:12-39`).
- N1 (`W1-N1/STATEMENT.md:98-104`, "in particular" clause) gives E[Ẑ_r/Z | 𝒞] = 1 a.s. on 𝒜 ∩ {r ≤ R′} for each fixed r,
  with the data fixed.
- On 𝒜, R′ = 4. A union of four null sets and linearity give E[Ẑ/Z | 𝒞] = 1, and Z is a positive constant.
- The joint-law form: under H-U/SI, condition on (data, 𝒞). 𝒜 ∈ σ(𝒞), and Ẑ ≥ 0, so the tower property applies.
- The claim line now separates the data-fixed identity from this joint-law consequence and names the extra idealisation.
- Code: `v3_run.R:91` gives `islands = 4L`; `:154` computes `log_sum_exp(logZr) − log(R)`, the log of the arithmetic mean.

Correct; hypotheses as stated.

**R1, R2.** These are unchanged since R1, where I re-derived every step and checked the arithmetic numerically. The
harmonised B2.1 constant in READER_VERSIONS (RV:300) is R1's. I re-checked it with exact ceilings (0 violations, above).

**R3 (historical).** The target, the premise table and the assembly now quantify over the RM2-R / RM2-F hypotheses, so the
stated hypotheses imply what the proof uses:
- (S) follows by a union bound from [SAND(Q)], [NA(Q)], [TL(Q)] (RM2 :207-208, :217-218);
- (P) is [POST];
- (V) is input validity;
- the operational premises are carried as (S4).

The R1 G1/G2 failure (sol F2) is gone. The current Theorems 6–7 do not cite R3: RV:747, :758, :1383, and STATEMENT:45.

**R4.** Unchanged except for the (S4)(i) wording in "Not claimed". The steps:
1. Theorem 2 via `W2-APP:POST` in the standardised-signal convention. On {δ ≤ ½}, o₁ ≤ 2δ.
2. (T3⁺⁺)(b) at Q = S₀ needs (FL-R16) (B6.1), (V-R), (L-R⁺⁺) and p > s₀. Then IF-START⁺⁺ gives
   1_𝒜 o₀ = O_P(n^{−1/2}e^{C√log n}).
3. √(log n/n) ≤ ρₙ eventually.
4. ρₙ is eventually decreasing, so (C-v) of `W3-SAMP/STATEMENT.md:158-162` applies.

Correct. Every hypothesis used is in the claim.

**B3.8** (record copied into the manifest). I re-derived it:
- the fully orthogonal design satisfies (A1)–(A6) with A = 1, φ₀ = g₀ = 1 and the second form of (A6);
- the identity (s₀+1)(p−s₀) − (2p−1−s₀) = (s₀−1)(p−s₀−1) ≥ 0;
- Λ^E_n ≥ 2√(log n/(2πn));
- f_p ≥ ½ when s₀ ≤ p/2;
- the threshold is uniform in p.

Correct.

---

## Faithfulness, row by row (G3)

The theorem statements are textually unchanged from R1, except for the fixes verified above. My R1 row-by-row check
therefore stands for every hypothesis and conclusion. The new or changed text:

- **Thm 1.**
  - Remark (vi) and the (A2) line now carry the master's domain.
  - Remark (vii) is an observation, and the text says no theorem backs it.
  - The main displays are unchanged. The expectation display is POST2 C (i) at :85-91. HPM = MPM via 2Eδ each, union bound.
- **Thm 5.** The leakage form now matches (L-R⁺⁺) exactly. Only "l ∉ Q" changes; H_l and the truths are unchanged.
- **Thm 6.**
  - The 𝒢ₙ of remark (i) is 𝓜ₙ ∩ Sandₙ(Q) ∩ NA ∩ TL. It lies inside 𝒢⁺ₙ = 𝓜ₙ ∩ 𝒦ₙ, because Sand ⊆ St and
    𝒦ₙᶜ ⊆ Stᶜ ∪ NAᶜ ∪ TLᶜ. Its probability tends to 1 under RM2-R-plus.
  - On it, RM0-plus (a′) gives exactly |S̃₀∖S₀| ≤ |Q∖S₀| ≤ n^b deletions, a completed scan with no improvement, and a
    non-binding cap.
  - The theorem's 𝒢ₙ may be taken to be this set.
  - The GUARD-W sentence is a restriction and matches the code.
- **Thm 7.**
  - Remark (a) states (BM-Q♭) with c > max{16, c_TL⁰}. This is equivalent to the master's max{c_TL,16} with c_TL > c_TL⁰.
  - (A5)(b)'s C_Q form implies (BM-Q♭) for large n, as checked above.
  - Honest limits (ii) is now supported (RM2-R-plus gives the conclusion under population conditions).
  - The example statuses are verbatim (`claims.tsv`: Ex-Proxy, Ex-Equi, Ex-PolyF).
- **Thm 8′.** The gain is the master's γ(t|S) (`W3-SCR/STATEMENT.md:51-56`). The margin condition is (A∞) verbatim (:87-90).
- **Thm 10.**
  - The GUARD-W sentence is consistent with (S5): estimates refer to the potential (uninterrupted) run.
  - The moderate-n parenthesis is an observation.
  - The conclusions, localisation to 𝒜 and branch scope are unchanged.
- **Card.**
  - Rows 3.2, 3.3, 3.5, 3.6, 3.7, 4.1 and the setting line now match their reader statements (see table above).
  - Row 3.1's delivery and GUARD-W sentences match Thm 6.
  - Rows 1.1–1.4, 2.1 and 2.2 are unchanged and were faithful in R1.

No reader conclusion is stronger than its master in quantifiers, uniformity, expectation vs probability, localisation,
branch or scope.

---

## Findings

There are no C, S or F findings of my own.

### Editorial (E) — not counted in the score
- **E1** `CLAIMS_CARD.md:72` (row 3.5): "Given the frozen calibration, on calibration success, given the frozen
  calibration and the data, …". The conditioning appears twice. Write "On calibration success, given the frozen
  calibration and the data, the equal-weight mean …".
- **E2** `READER_VERSIONS.md:148`: "($s_0<p$ suffices by Prop. LB)". Prop. LB also needs $s_0+1\le K$, and it is "PROVED
  (by this seat, unchecked)". The checked Corollary B already gives order $n^{-1/2}$ for every $s_0\le K-1$, since
  $c(p,s_0)\ge1$ for $s_0\ge1$ (`W3-PSHARP/STATEMENT.md:95-96`). Write "($s_0\le K-1$ suffices: Corollary B with
  $c(p,s_0)\ge1$, or Prop. LB)". The current wording is correct for fixed $s_0$ and large $n$.
- **E3** `METHOD_INTUITION.md:71-72`: "$\pi_0$ puts mass $1-n^{-c}$" (twice). Write "at least $1-n^{-c}$", as in
  Theorem 5 and card row 3.3.
- **E4** `READER_VERSIONS.md:829-830`: (A5)(b) says "$C_Q$ above an explicit constant (Remark (a))". Since the R1 fix,
  Remark (a) gives the (BM-Q♭) replacement, not a threshold for $C_Q$. Either add "e.g. any fixed
  $C_Q>\max\{32,\,64A+c\}$ with $c$ as in Remark (a)" (this suffices for large $n$; checked), or point to (BM-Q♭) only.
- **E5** `STATEMENT.md:43`: the R1 row says "used by Thms 1, 2, 3, 4, 6", but `REPORT.md:19` (corrected in R1) says
  "(Thms 1, 2, 3, 4, 6, 10)". Harmonise both to the latter (R4 uses B2.1/B6.1).
- **E6** `READER_VERSIONS.md:703`: Thm 6 remark (iii) still paraphrases "(example status unchecked)" for polynomial decay.
  Quote `W3-RM2:Ex-PolyR@1.0.3` verbatim, as was done for Thm 7: "PROVED; line-checked LC2-C; Astra seat ACCEPT; not
  examined by the Opus seat — next council round; conditional on W2-APP:POST, W2-LOC2:Lemma-BC, W2-LOC2:Lemma-IR; …".
- **E7** `lemmas/R4_printed_outputs.md:48-49`: the "Not claimed" remark cites "F-UNI Step 2" for completion under (S4).
  F-UNI is now history; the active deterministic delivery is `W3-RM2-R:DLV-0`. Cite DLV-0, which is also what
  READER_VERSIONS:1341 means.
- **E8** `METHOD_INTUITION.md:81-83`: "this is what makes its evidence estimate unbiased". Add "(the uninterrupted final
  run's estimate, given the calibration)" so this sentence carries the same scope as the table at :128 and row 3.5.
- **E9** `REPORT.md:13`: the PoolZ registry conclusion does not say that Ẑ is the potential (uninterrupted) record with
  the data fixed. Only "N1 premises" implies it. Since registry rows are cited downstream, add "(potential record, data
  fixed; equals the printed field on completed runs)".
- **E10** `CLAIMS_CARD.md:6`: the v1.8 changelog entry was rewritten in place with the R1-F6 wording. Keep history entries
  as they were, and record the correction only in v1.11 (already done at :3).

---

## Interpretive sentences (D71)

Rows 1–30 continue my R1 table. Re-judged rows are marked, and new sentences are appended.

| # | where | sentence (abridged) | verdict |
|---|---|---|---|
| 1 | Thm 1 display | "consequently … P(HPM = MPM = S₀) ≥ 1 − 4C√(log n/n)" | SUPPORTED (POST2 :91, union bound) |
| 2 | Thm 1 rem (i) | PIP sensitivity and specificity at rate √(log n/n), uniformly in j | SUPPORTED (W3-POST :84; POST2 :91) |
| 3 | Thm 1 rem (ii) | no over-fitting mass; specificity can fail without beta-min (numerical) | SUPPORTED (W3-POST :87-94, labelled) |
| 4 | Thm 1 rem (o) | Thm 1′ contains Thm 1 when C_β²φ₀² > c₁; otherwise they coexist | SUPPORTED (POST2 :47, :135-136) |
| 5 | Thm 1 rem (v) | large models carry O_P(n^{−1/2}) with no eigenvalue condition | SUPPORTED (W3-POST :52-58 + B1.3) |
| 6 | Thm 1 rem (vi), (A2) line | "on every design with s₀ ≤ min(K−1, p/2) … at least of order n^{−1/2}"; sparsity forced | **SUPPORTED** (re-judged; PSHARP :92-104; E2 precision) |
| 7 | Thm 1 rem (vii) | moderate-n mass on one-variable supersets, "an observation, not a theorem" | **SUPPORTED as an observation** (re-judged; labelled; no theorem support claimed) |
| 8 | Thm 1′ title | "no eigenvalue condition off S₀ beyond the vanishing floor (A5)" | SUPPORTED (POST2 :133) |
| 9 | Thm 3 "In words" | rate cannot be improved under its assumptions; c free of s₀ when s₀ ≤ p/2 | SUPPORTED (AE + B3.8; arithmetic re-checked) |
| 10 | Thm 3 rem (i) | named exactness cases; "rare large gains of a single extra variable" | SUPPORTED (A1-E; PSHARP-R :104-114) |
| 11 | Thm 4 remark | KL projection; concentrates on the support of the best candidate predictor | SUPPORTED (MISR-R :89-91, :126-128) |
| 12 | Thm 4 remark | Hellinger/KL contraction at M_n/√n and M_n/n; fixed-design uniform form | SUPPORTED (CorH-plus, CorH-U) |
| 13 | Card 1.4 | "uniformly over the residual variance (fixed candidate design)" | SUPPORTED (MIS(i) :114) |
| 14 | Thm 5 | "so the rate under (A6) is optimal up to the factor √log n" | SUPPORTED (START2-R :237; FLOOR) |
| 15 | Card 3.3, METHOD:71-72 | start mass ≥ 1 − n^{−c} "with probability tending to one" | **SUPPORTED** (re-judged; START2-R :229-231; E3) |
| 16 | Thm 6 | "in particular P(output and Ŝ ≠ S₀) → 0" | SUPPORTED (RM0-plus (b⁺)) |
| 17 | Thm 6 rem (o) / Thm 7 rem (b) | error split; interpretation labelled "not part of the theorem" | SUPPORTED (RM0-plus (c⁺)) |
| 18 | Thm 6 rem (i) | "𝒢ₙ can be chosen (𝓜ₙ ∩ Sandₙ(Q) ∩ NA ∩ TL) so that … only deletes … ≤ n^b moves, certifies S₀; cap never binds" | **SUPPORTED** (re-judged; RM0-plus (a′), RM2-R-plus) |
| 19 | Thm 6/7, Card 3.1 | "neither limit can bind unless n+p+1 > 2^{10⁶} or n ≳ 4×10⁹" | SUPPORTED (arithmetic; IDEAL-W⁺ text) |
| 20 | Thm 6 (A4)/(A6) lines | b < ½ boundary "heuristic"; width condition "forced by this route" | SUPPORTED (labelled; RM2 C6, C3(b)) |
| 21 | Thm 7 intuition | (A5)(a) "holds automatically when Q has fewer than log n extra columns" | SUPPORTED ((W-χ) ⇒ (W)) |
| 22 | Thm 7 honest limits (ii) | "Theorem 6, which gives the same conclusion under population analogues" | **SUPPORTED** (re-judged; RM2-R-plus :177-182) |
| 23 | Thm 8 honest limits | intersection, not conditional; certification not claimed w.p. → 1 | SUPPORTED (SCR :80-90, :217-218) |
| 24 | Card 3.7 Buys | "the only guarantee about the reported model's support that needs no visibility, leakage, start or block condition"; can hold where 3.1–3.2 fail | **SUPPORTED** (re-judged; 9C's reported-model clause is a conditional implication, not a probability guarantee) |
| 25 | Thm 9 "In words" | "the posterior contracts at the rate √(log n/n)" | SUPPORTED (DIST :193-195) |
| 26 | Thm 10 "Which designs", Card 3.6 | (A5) holds only for no-leakage designs, e.g. independent predictors; AR/block not covered | SUPPORTED |
| 27 | Thm 10 why-line | vanishing mass to transport, Ẑ/Z → 1 independent of ladder length; moderate-n parenthesis an observation | SUPPORTED (SAMP :161-163; observation labelled) |
| 28 | Card 3.6 | "for particular AR or block designs that satisfy Theorem 6's visibility, leakage, floor and local-regression conditions, row 3.1 still gives the reported-model result" | **SUPPORTED** (re-judged; Thm 6 / RM2-R-plus) |
| 29 | Card 3.5, 4.1; METHOD:128 | potential uninterrupted records have expectation Z; equal to printed on completed runs; nothing conditional on completion | **SUPPORTED** (re-judged; N1 :86-88, :98-104; PoolZ) |
| 30 | Thm 10 remark (row 3.5) | "E[Ẑ \| calibration] = Z for every design and data set" (Ẑ the potential record per (S5)) | SUPPORTED (PoolZ) |
| 31 | Thm 6, Thm 10, Card 3.1/3.5/3.6 (new) | "The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and no output"; "the best model found before the stop is returned marked incomplete" | SUPPORTED (code: `v3_fit.R:84-85, 154-159`; `v3_run.R:105-114, 142-145`; `v3_calib.R:81, 113`; NOTATION §5) |
| 32 | Card 3.2 (new) | case (b) needs beta-min at σ*√((\|Q\|+log n)/(nφ₀²)); the standard scale suffices for (a) | SUPPORTED (Thm 7 (A5)(b); RM2-R (BM-W⁺)/(BM-Q♭)) |
| 33 | Thm 7 rem (a) (changed) | "(A5)(b)'s signal clause may be replaced by the master's (BM-Q♭)" | SUPPORTED (RM2-R :107-112; E4) |
| 34 | METHOD:80 (new) | "the run proceeds unless another stop occurs or the allocation is insufficient" | SUPPORTED (`v3_calib.R:160-166`) |
| 35 | METHOD:102-105 (changed) | Theorem 8: "the chance that a run certifies a small model missing a truth tends to zero" | SUPPORTED (SCR A1) |
| 36 | METHOD:81-83 | freezing "is what makes its evidence estimate unbiased" | SUPPORTED as a mechanism for the uninterrupted final run (N1); E8 for scope wording |
| 37 | RV:747, Card:6, :68 (changed) | Prop-F used ℓₙ; frozen F-UNI@2.1.0 states the shipped cap; DLV-0 is active | SUPPORTED (`C-DLV/STATEMENT.md:32`; `L5_delivery.md:8-12`) |

There is no OVERSTATED or UNSUPPORTED sentence.

---

## Gates

- **G1 correctness — PASS.**
  - PoolZ, R1–R4 and B3.8 re-derive.
  - R3's target now matches its proof (historical scope).
  - Arithmetic re-checked numerically, with 0 violations.
- **G2 hypotheses used = stated — PASS.**
  - Each bridge consumes exactly its stated hypotheses.
  - R3's former-hypothesis restriction removes the R1 mismatch.
  - R4's p > s₀ is explicit.
- **G3 faithfulness — PASS.**
  - Every reader statement (Thms 1, 1′, 2–7, 8, 8′, 9, 9B, 9C, 10) implies its master's hypotheses via listed bridges or
    (S1)–(S5), and states no stronger conclusion.
  - All six R1 opus S-findings and the sol S/F findings on card rows and remarks are fixed.
  - The D71 inventory has no overstated or unsupported sentence.
- **G4 statuses and citations — PASS.**
  - The 24 ids checked against `claims.tsv` are verbatim, including the newly quoted Ex-Proxy, Ex-Equi and Ex-PolyF.
  - "Conditional on …" clauses are carried, and nothing below PROVED-CHECKED is called checked.
  - REPORT line ranges match the files, and the B3.8 record is inside the manifest and verbatim.
  - Paraphrase leftovers: E6, E9.
- **G5 no hidden finite-n or scope claims — PASS.**
  - Every moderate-n sentence is now labelled an Engineering observation, with an explicit non-claim.
  - No two-sided rate on every design is claimed; the lower-bound domain is restored.
  - Theorem 8 keeps fixed constants.
- **G6 fidelity to the code — PASS.**
  - The R1 code-fact corrections were verified at the pins: prior cost, Occam attribution, pilot forced steps, fallback
    order and tier, m(∅)Z̄₀ initial factor, ledger scope (preflight timing unrecorded), preflight stop before any record.
  - The GUARD-W behaviour and equal-weight pooling (`v3_run.R:154, 162`) were also checked.

**Score: 9.3 / 10** (C, S and F only). I hold no C, S or F finding. Every R1 finding from both seats is fixed correctly
and completely, and the new GUARD-W text matches the code. The deduction reflects only that PoolZ and R1–R4 remain
author-checked ("PROVED (by this seat, unchecked)", which the text honestly labels) and the small editorial residue
E1–E10, none of which changes a statement's strength.

`COUNCIL-VERDICT round=R2 manifest=3af23c3572d21511fe59fe7a610991eb2b92858e0309a8ee7ac1e8ff43636a4b seat=opus score=9.3 gates=PASS`

# MEAS-D: author's texts for the R3 round (T9 widening + integrability step), consistent with R2's F4 and E9–E12

Written against the staged ticket under `PRE_LEAN_PASS/MEAS-D/ticket/Theory_work/Wave3/W3-SAMP/`. I read two states:
- **MEASD2** (manifest 00426ac2, the text Opus R2 reviewed);
- **MEASD3** (manifest 3a409352, at `origin/theory/PRE-LEAN` 43e1b07f), in which the coordinator has already applied R2's F4 and E9–E12 and my T9 texts A and B.

Every "old" string below is quoted from MEASD2. Where MEASD3 already differs, I say so. Line numbers are those of MEASD3.

## 0. Status of each text

| Text | What | In MEASD3 already? |
|---|---|---|
| R2 F4, E9, E10, E11, E12 | Opus's corrections; accepted as the seat wrote them | Yes; I checked lines 38 and 48 of `MEAS_D.md` and lines 203, 205 of `REPORT.md` |
| P1 (T9 text A) | pair independence derived, Step 5 | Yes (`MEAS_D.md:42`) |
| P2 (T9 text B) | the ledger's offers, Step 4 | Yes (`MEAS_D.md:39`); one phrase to adjust for W1 (§2 (a)) |
| **W1, W2, W3** | statement widening | **No** (§1) |
| **P3** | new Step 6: Z bounded, integrability | **No** (§2 (b)) |
| Mathlib rows, "serves" line, registry block | follow from W1–W3 and P3 | **No** (§2 (c), (d); §3) |
| E1 sentence in `STATEMENT.md:36` | the 𝒜 reading (T9 card §B.1); same file, same re-freeze | **No** (§4) |

Consistency with F4 and E9: none of the new texts names a route for (C-v) or (TR-d), and none cites `v3_core.cpp:475`. Step 6 uses only (MR-b) at h ≡ 1 and Step 5's [0, ∞] form.

## 1. STATEMENT sentence (`STATEMENT.md:190`, and its copy at `lemmas/MEAS_D.md:24`)

The sentence is identical in MEASD2 and MEASD3. Three replacements inside it; everything else in the line is unchanged.

**W1.** Old: "the records of the four final islands; the final local-search"
New: "the records of the four final islands, with the sets 𝓜_r of models they evaluate; the final local-search"

**W3.** Old: "the output event 𝒪°; and Z, π, π₀. Consequently,"
New: "the output event 𝒪°; and Z, π, π₀. Moreover 0 < Z ≤ κ_n for every valid data set, with κ_n depending on n only, so 1_{𝒜°}Z, 1_{𝒜°}Ẑ and 1_{𝒜°}Ẑ_r·H_r(h), for every bounded h of §2, are integrable under every law of the data. Consequently,"
(The clause on H_r(h) is the consultant's rider 3; see `T9_addendum.md`.)

**W2.** Old: "under the joint law of §0 (H-U/SI, :35-36), for each island r"
New: "under the joint law of §0 (H-U/SI, :29 and :35-36, which together make each final stream independent of the pair (data, streams 0–9)), for each island r"

The claim's lines stay 190-192. `STATEMENT.md:192` (Conventions) is unchanged.

## 2. `lemmas/MEAS_D.md`

**(a) Step 4, Ledger bullet (line 39), for W1.**
- Against MEASD3. Old: "Its offers are the islands' evaluations, the block-table models" → New: "Its offers are the islands' evaluations (the sets 𝓜_r), the block-table models".
- Against MEASD2 (which lacks the sentence). Append to the bullet: "Its offers are the islands' evaluations (the sets 𝓜_r), the block-table models (functions of the data, Step 2), the models inherited from calibration (coordinates of 𝓒°) and the two searches' scans (`W3-SAMP:PC` (iii))."

**(b) P3: new Step 6.** At the end of Step 5's "Several islands" paragraph (line 48), delete the final " ∎" (the paragraph then ends "…it does not already state."). Insert after it, before "**What the proof does not use.**":

> **Step 6 (Z is bounded; integrability).** The coded marginal likelihood is m(S) = C_n·D_S^{−1/2}(2b₀ + Q_S)^{−ν}, with C_n = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) depending on n only (`cpp/v3_score.h:59, 223`; `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:29-30`). Here D_S = det((n+1)G_S + I)/det(G_S + I) = Π_i((n+1)λ_i + 1)/(λ_i + 1) ≥ 1, the λ_i ≥ 0 being the eigenvalues of G_S; and Q_S ≥ 0, because Q_S is the minimum of a sum of two nonnegative quadratic forms (Lemma V, `Theory_work/Wave3/W3-PSHARP/lemmas/S_one_step.md:7-15`). Hence m(S) ≤ κ_n := C_n(2b₀)^{−ν} for every S and every valid data set. The prior weights sum to 1 over Ω, so 0 < Z ≤ κ_n. Thus 1_{𝒜°}Z is bounded, hence integrable under every law of the data. For the estimates: Ẑ_r ≥ 0 is Borel (Step 4), and Step 5 in its [0, ∞] form with (MR-b) at h ≡ 1 gives E[1_{𝒜°}Ẑ_r | data, 𝓒°] = 1_{𝒜°}Z; so E[1_{𝒜°}Ẑ_r] = E[1_{𝒜°}Z] ≤ κ_n. Each 1_{𝒜°}Ẑ_r, and their mean 1_{𝒜°}Ẑ, is therefore integrable, and the real-valued conditional expectations of §2 and of PoolZ are defined. The same holds with a bounded model summary. For h as in `W1-N1/STATEMENT.md` §1, with a deterministic bound |h| ≤ B_h that does not depend on the data, |H_r(h)| ≤ B_h, so |1_{𝒜°}Ẑ_r·H_r(h)| ≤ B_h·1_{𝒜°}Ẑ_r is integrable with expectation at most κ_n·B_h, and |1_{𝒜°}Z·π(h)| ≤ κ_n·B_h. Hence (N1), and likewise (MR-a)–(MR-c), integrate to E[1_{𝒜°}Ẑ_r·H_r(h)] = E[1_{𝒜°}Z·π(h)], with both sides finite. ∎

**(c) §3, Mathlib table (after line 64).** Add two rows:

```
| Bounded measurable implies integrable (probability space) | `Integrable.of_bound` |
| Monotonicity and monotone convergence of the lower integral | `lintegral_mono`, `lintegral_iSup` |
```

All three names are in the pinned checkout (verified by grep).

**(d) §4, the Theorem 10 line (line 85).**
Old: "Theorem 10 (card row 3.6): through (LT-e), (C-v) and (TR-d). **To be confirmed against `walks/T9_Thm10.md` before the T9 card.**"
New: "Theorem 10 (card row 3.6): through (C-v), by `W3-READER:R4`; (TR-d) is the alternative route of the reader's remark. Confirmed against `walks/T9_Thm10.md` §1 and §6."

**(e) §5, Limits.** Add a bullet: "Step 6's constant κ_n is read from the coded formula at pin 4676af6 (`cpp/v3_score.h:59, 223`); the list-field re-pin does not touch `cpp/`."

## 3. REGISTRY block (`REPORT.md:203-204`)

**Line 203.** Two replacements inside the conclusion, matching W1 and W3 (no bar characters):
- Old: "the four potential island records, the final local-search" → New: "the four potential island records with their evaluated-model sets, the final local-search"
- Old: "are Borel functions of (X^r, y^r, U(0), ..., U(13)); so, under the joint law (H-U/SI)," → New: "are Borel functions of (X^r, y^r, U(0), ..., U(13)); 0 < Z <= kappa_n with kappa_n depending on n only, so 1_A0 Z and 1_A0 Zhat are integrable under every law of the data; so, under the joint law (H-U/SI, which make each final stream independent of the pair (data, streams 0-9)),"

**Line 204.** Append to depends_on: " ; W3-SAMP:MR@stmt:MR-b ; W3-PSHARP:S@proof:Lemma-V"

Line 205 (`gates: … R3_council_opus.md`) is already as E12 asks.

## 4. The E1 sentence (`STATEMENT.md:36`; T9 card §B.1; CORRECTION-ONLY wording)

Split per the consultant's rider 4: the clock clause goes in a remark, not in the statement text.

**Theorem-side.** Line 36 currently ends "…: Lemma MEAS-D (§4, `lemmas/MEAS_D.md`)." Append, on the same line:

> By erratum E1 (`Theory_work/Wave3/ERRATA_W3-SAMP.md`), 𝒜 and 𝓒 are read throughout as the potential pair (𝒜°, 𝓒°) of `W3-AUDIT-A:GW`; on completed runs the actual calibration record equals 𝓒° (GW-iii), and statements about actual runs are obtained through 𝒪 ∩ A ⊆ 𝒪° ∩ A° (GW-iv, `W3-AUDIT-A:CAL-C`).

It adds no line, so §§0–3 keep their line numbers.

**Remark.** A new paragraph after line 192, at the end of the file (outside MEAS-D's span 190-192):

> *Remark (actual runs; not part of any claim).* The guard's clock is not modelled (`W3-AUDIT-A:GW`, "Not claimed"). A probability of an actual-run event, that is, one intersected with {completed} or with the actual 𝒜, is therefore read as an outer probability unless the clock is taken jointly measurable with the streams; in either reading it is bounded by the probability of the corresponding potential event.

The reader-side split and the two changelog lines are in `T9_addendum.md`.

## 5. Outside the MEAS-D ticket (for the same batch; texts in the T9 card)

- PoolZ's proof: the one-clause citation of MEAS-D for measurability and finiteness; recorder adds `W3-SAMP:MEAS-D` to PoolZ's depends_on.
- R4, PoolZ's Setting and the reader: the 𝒜 alignment (T9 card §B.2–4).

## 6. For the R3 seat

- **What is new in substance:** the integrability clause (W3) and Step 6. W1 and W2 only make explicit what Steps 4 and 5 already prove.
- **Three things to check in Step 6:** the constant C_n at `cpp/v3_score.h:59` and its use at `:223`; D_S ≥ 1 (each factor ((n+1)λ + 1)/(λ + 1) is ≥ 1 for λ ≥ 0); and that Lemma V's file gives Q_S ≥ 0 for every S, including S = ∅.
- **One dependency added across tickets:** `W3-PSHARP:S` for Lemma V. If the seat prefers no cross-ticket edge, Q_S ≥ 0 can instead be cited from [P1] `lem:spec`(b), which W3-POST already uses.

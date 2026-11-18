# T9 Fable card (consistency tier): Thm 10 (row 3.6), evidence unbiased (row 3.5), pooling (row 4.1)

Inputs: Astra (4 points) and blind Sol (3 points), found independently; walks `walks/T9_Thm10.md` (walkB: 1 MINOR, 2 NOTE) and `walks/T9_rest.md` (walkD: 2 MINOR, 2 NOTE), both complete to recorded inputs; MEAS-D as fixed after R1, with Opus R2 (8.7, gates FAIL on F4 and E9–E12). Snapshot: `origin/theory/PRE-LEAN` a8f70d2b, main ad29c22e. **For the consultant: answer AGREE or OBJECT per row.**

**Verdict:** no flaw in the mathematics of any of the three rows; both reviewers' CHECKED lists and both walks confirm every identity, constant and event at fixed data. All seven Codex points concern the passage from fixed data to the joint law, and they reduce to three things, each closed without adding a premise:
1. joint measurability in the data: **MEAS-D** (proved);
2. which calibration event 𝒜 is: already recorded as erratum E1; three texts need aligning;
3. integrability of Z under the joint law: a one-line deterministic bound.

**Line for the consultant on MEAS-D.** New W3-SAMP lemma, proved, no premise added: under exact arithmetic, on valid inputs, the potential calibration record, the four potential island records, the final-run ledger and Z are Borel functions of (data, streams). So every joint-law clause of W3-SAMP, PoolZ's "Consequently" clause and DIST-C's P⊗ clauses are well posed for the potential pair (𝒜°, 𝓒°). It claims nothing about the actual 𝒜, 𝒪 or the guard. AGREE or OBJECT?

## (a) Coverage by MEAS-D

| Reviewer point | Covered by MEAS-D? | What remains |
|---|---|---|
| Astra T9-1, Sol T9-2 (first half): measurability, as the data vary, of the potential calibration record and its success flag, the island records and the evaluated-model sets | **Yes** (Steps 1–4) | Nothing |
| Same points: each final stream must be independent of the **pair** (data, streams 0–9); two marginal independences would not do | **Not yet written** | One sentence in Step 5 (text A below). It is derived, not assumed. |
| Astra T9-3, Sol T9-2 (second half): measurable completion flag and reported model; ledger offers from outside the islands; the clock | **Yes for the potential run** (𝒪°, the ledger, Ŝ of P°) | Name the ledger's offers in Step 4 (text B). State once that probabilities of actual-run events are bounded through 𝒪 ∩ A ⊆ 𝒪° ∩ A° (text C). |
| Astra T9-2, Sol T9-1: 𝒜 identified with the coded calibration returning "ok" | Not a MEAS-D matter | See (c) |
| Astra T9-4, Sol T9-3: joint integrability of Z | Not a MEAS-D matter | See (b) |

So nothing substantive remains beyond MEAS-D: texts A, B and C are three sentences. For Opus R2, as author I accept F4 and E9–E12 as written by the seat (route list for (C-v) and (TR-d); the `:474` pin; the derived IND-T wording; two registry wordings). A, B and R2's fixes go into one R3 round.

**Text A** (`lemmas/MEAS_D.md`, Step 5, after its first sentence): "Independence from the pair follows from two stated facts: SI holds for each fixed data set, that is, given the data U^{(9+r)} is independent of U^{(0:9)} (`STATEMENT.md:29`); and U^{(9+r)} is independent of the data (`:35-36`). Hence P(U^{(9+r)} ∈ A, U^{(0:9)} ∈ B | data) = P(U^{(9+r)} ∈ A)·P(U^{(0:9)} ∈ B | data)."

**Text B** (Step 4, Ledger bullet, append): "Its offers are the islands' evaluations, the block-table models (functions of the data, Step 2), the models inherited from calibration (coordinates of 𝓒°) and the two searches' scans (`W3-SAMP:PC` (iii))."

**Text C**: the sentence in (c)1 below.

## (b) Integrability (Astra T9-4, Sol T9-3)

**Genuine, and closed by a short standard proof; it does not need HQ.** The reviewers are right that Lemma F's bound is data-dependent. But Z itself is bounded by a constant depending on n only:
- the coded marginal likelihood is m(S) = c_n·D_S^{−1/2}(2b₀ + Q_S)^{−ν} (`W3-T03ACC/STATEMENT.md:30-31`);
- D_S = Π_i((n+1)λ_i + 1)/(λ_i + 1) ≥ 1 and Q_S ≥ 0, so m(S) ≤ κ_n := c_n·(2b₀)^{−ν};
- the prior weights sum to 1, so Z = Σ_Ω ϖ(S)m(S) ≤ κ_n for every data set.

Kind: proof completion. Span: PoolZ's proof lies inside its registry span (`W3-READER/STATEMENT.md:12-39`); the claim sentence does not change. **Exact fix**, inserted in the proof before "taking expectations": "(Both sides are finite. For every data set m(S) ≤ κ_n := c_n(2b₀)^{−ν}, because D_S ≥ 1 and Q_S ≥ 0, so Z ≤ κ_n, a constant depending on n only. Since Ẑ ≥ 0, E[1_𝒜 Ẑ] is obtained by monotone convergence and equals E[1_𝒜 Z] ≤ κ_n.)"

## (c) The 𝒜 identification (Astra T9-2, Sol T9-1, walk H2)

**A wording fix, not more.** The reading is already recorded: erratum E1 (`Theory_work/Wave3/ERRATA_W3-SAMP.md`, HQ D111) says W3-SAMP's conditional identities are read with the potential pair (𝒜°, 𝓒°); `W3-AUDIT-A:GW` (GW-iii) proves that on completed runs the actual calibration record equals the potential one, which is exactly the pathwise implication Astra asks to import; `W3-AUDIT-A:CAL-C` gives the transfer rules. E1 edited no hashed file, so three texts still say only "calibration returns ok". Theorem 10's conclusions are intersections and indicator-multiplied bounds, so they pass to the actual 𝒜 ⊆ 𝒜°; row 3.5's conditional identity is true only in the potential reading. Exact fixes:

1. `W3-SAMP/STATEMENT.md:36` (premises span of the W3-SAMP claims; wording). Append after MEAS-D's pointer sentence: "By erratum E1 (`Theory_work/Wave3/ERRATA_W3-SAMP.md`), 𝒜 and 𝓒 are read throughout as the potential pair (𝒜°, 𝓒°) of `W3-AUDIT-A:GW`; on completed runs the actual calibration record equals 𝓒° (GW-iii), and probabilities of actual-run events (those intersected with {completed} or with the actual 𝒜) are bounded through 𝒪 ∩ A ⊆ 𝒪° ∩ A° (GW-iv, `W3-AUDIT-A:CAL-C`), as outer probabilities if the clock is not modelled."
2. `W3-READER/STATEMENT.md:15-16` (PoolZ Setting; inside its span, wording). After "success event $\mathcal A\in\sigma(\mathcal C)$" insert "(the potential pair of the uninterrupted run, `W3-SAMP` erratum E1)".
3. `W3-READER/lemmas/R4_printed_outputs.md:17-18` (Inputs paragraph, not the claim). After "$\{\text{completed}\}\subseteq\mathcal A$ (:38-41)" add "; read as the potential pair by erratum E1 (`W3-AUDIT-A:GW`, `:CAL-C`)".
4. `READER_VERSIONS.md:1301-1302` (reader prose). "its calibration succeeds (fallback ladder included)" → "its calibration succeeds (fallback ladder included), in the run taken as if uninterrupted".

## Rulings on the walk rows

| Row | Ruling | Kind | Recorded STATEMENT? | Fix |
|---|---|---|---|---|
| Thm10 **H1** (MINOR): row 3.6 rests on T12, whose registry status reads "PROVED-LOCKED … not adopted" | AGREE | Status record, not mathematics | No | Recorder: the T12 relabel carrier (owner adopted T12 on 2026-11-18; draft in `T9/T12_relabel_carrier_draft.md`). `W3-AUDIT-AX:FR` (PROVED-CHECKED) also re-checks the T12 identities at the code of record. |
| Thm10 **H2** (NOTE): 𝒜 must be read as 𝒜° | AGREE | Wording | Yes, wording | (c) above |
| Thm10 **H3** (NOTE, Lean): the N1 premises define the abstract algorithm | AGREE | Lean note | No | None |
| rest **F1** (MINOR): PoolZ cites only N1 (v2.2.1 core) | AGREE | Citation and registry edge | Proof text inside PoolZ's span | Applied as CITATION-ONLY (`T9/T9-F1_correction.patch`, PURE). The pin in my prep note was one line short; the coordinator corrected it to `:107-111`. |
| rest **F2** (MINOR): joint-law clause needs measurability in the data | AGREE | Proved by MEAS-D | No premise added | (a) above |
| rest **F3** (NOTE): "printed evidence" should name `log_Z` | AGREE | Card wording | No | `CLAIMS_CARD.md:76`: "equals the printed evidence" → "equals $\exp$ of the printed field `log_Z` (not `log_Z_list`, row 3.1L)". `:97`: "(equal to the printed evidence on completed runs" → "(equal to $\exp$(`log_Z`), the printed pooled evidence, on completed runs". |
| rest **F4** (NOTE, Lean) | AGREE | Lean note | No | None |

**Left uncovered by the walks:** both stop at recorded inputs. Not opened: T12's own proof text, the START and KERNEL code bridges (N9), and for Theorem 10 the posterior and start inputs (`W2-APP:POST`, `W3-START2-R:IF-START`), which T4 and the T8 addendum cover.

## Lean readiness (ranked; no item changes a statement)

1. **Row 3.5 at fixed calibration value first.** E[Ẑ_r] = Z for the abstract frozen island on a finite state space (the unbiasedness induction of Lemma P / MR-b), then linearity over four islands.
   - Gain: the December target is certified with finite sums only; no freezing, no measurability. Named axioms: none; the N1 premises are the definition of the abstract algorithm.
2. **Then the freezing step as a separate lemma** (`condExp_indep_eq`), and the joint-law form last, with MEAS-D's code readings as hypotheses and Z ≤ κ_n as a proved bound.
3. **Theorem C above MR is finite Markov-chain algebra plus Markov's inequality** ((C-i) deterministic; (C-iii), (C-iv), ST, LT). Level 1 given the MR identities.
4. **Define 𝒜 as 𝒜° in Lean**; actual runs enter through the two inclusion hypotheses of GW (iii), (iv).
5. **Theorem 10's assembly (R4)** is three O_P bounds added. Its two imported theorems are the posterior rate (T4 headline) and the start rate (T8 addendum), which bring their own named axioms.

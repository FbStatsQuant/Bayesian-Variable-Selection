# PRE-LEAN PASS: SUMMARY (DRAFT 2026-11-18 by the coordinator; the manager finalizes; b′-1 / T6-1 closed by HQ ruling (C), see §6)

Method frozen for this pass: `method-v3.1.1-listpip` = 7100bb3b (guard merged); the owner signed the method FINAL.

## 1. Findings (one line per target: Astra / blind Sol / Fable ruling; from each `T*/FABLE_CARD.md`)
Counts of FLAW / UNSTATED-HYPOTHESIS / LEAN-COMPILE as ruled are left to the manager: the cards rule point by point, and I have not re-counted them.
- **T1** (Thm 3(a), `W3-PSHARP:B`): no genuine flaw; T1-1 (λ ≥ 0) reclassified FLAW → Lean-compile; CORRECTION-ONLY.
- **T2** (SL0, LT-d): Astra NO-FLAW; no flaw, no change.
- **T3** (domination transfer, Hellinger reduction, D0): no recorded statement affected; T3-1 a one-clause gap in a proof-file justification (conclusion true); T3-2 Lean-only.
- **T4** (Thm 1, 1′, 2): no flaw in the mathematics; one definedness clause (R1); two points answered by records outside the packets; walk complete.
- **T5** (Thm 9 with 9B, 9C, DIST-1/2/3): Theorem 9 holds as stated; two commentary sentences overclaim (R1 = the DIST-2 (1 + s₀^r) sentence, now WEAKER row 1.4.11, **Sol-6 (c) 9.6 PASS**; R2), a convention (R4), a measurability slip fixed by an existing lemma (R3).
- **T6** (Thm 6, Cor 6L, Cor-FAMC; `T6/FABLE_CARD.md`): no flaw in the mathematics. T6-1 (helper allocation) = ERRATA E1 = Sol-5b b′-1: **not claimed beyond output runs (HQ ruling, option C)**; the allocation proof (NA_DROP v1.4) failed Sol-6 (b″) 8.4, and v1.5 scopes the delivery conclusion to output runs, see §6; T6-2 = T8-1 (already on main); **T6-3 (Astra: the list is 'offered to the final-run ledger', not 'met by the run') applied: D5Pa v3 `a9353d82…` (Opus PURE 9.6)**; Sol T6-3 Lean-only; walk F2 (re-pin of DLV-0/LIST-CODE for rows 3.1/3.2) is in the A re-pin scope.
- **T7** (Thm 4): no flaw in the masters; two reader sentences need one phrase each; T7-3 answered by a registered lemma.
- **T8** (Thm 7, Thm 5): no flaw; T8-1 a wording inversion already an erratum; T8-2 a qualifier restored; T8-3 "=" → "≤" on a probability-zero event.
- **T9** (rows 3.5, 3.6, 4.1) → **GAPS CLOSED (filter (a)), not "no flaw"**: all seven Codex points are the passage from fixed data to the joint law; closed by MEAS-D (measurability), the Z ≤ κ_n bound (integrability) and the 𝒜 identification (CORRECTION-ONLY), no premise added; complete only once MEAS-D is recorded; no row cites MEAS-D before its seats pass.
- **T10** (Thm 8, certified screening): no flaw; two sentences of reader/card text inaccurate (one overstates, one understates).
- **Sol-1 … Sol-4**: see `Sol1/` … `Sol4/` and `CORRECTIONS.md` (seat additions and recorder-only items).
- **Sol-5** (`Sol5/CODEX_gpt-6.2-sol.md`): (a) D5P 8.5 FAIL (LIST-CODE a-1; a-2, a-3 wording), (b) NA_DROP 8.6 FAIL (b-1 = T6 F3; b-2..b-4), (c) MEAS-D (MEASD7) **9.1 PASS**.
- **Sol-5b** (`Sol5/Sol5b/`): D5Pa 9.0 FAIL (a-1..a-3 FIXED; two WORDING points, applied in D5Pa v2); NA_DROP v1.3 8.7 FAIL (b-1..b-4 FIXED; **b′-1 blocking OVERREACH: the helper's tail work after the last guard**).
- **Sol-6** (`Sol6/CODEX_gpt-6.2-sol.md`): (b″) NA_DROP v1.4 **8.4 FAIL**: **b″-1 FLAW (blocking)**: the allocation proof does not bound the creation/interning of the `paste` keys, the global string cache, or the IDEAL-W⁺ decimal cost; b″-2, b″-3, b″-4 WORDING; b-1..b-4 FIXED, claim (o) ACCEPT, qualifier removals NOT-JUSTIFIED. (c) DIST-2 delta **9.6 PASS**.
- **MEAS-D** (T9's lemma): Opus R1 … R6, Sol-5 (c) 9.1 PASS on MEASD7; MEASD8 (CITATION-ONLY) = `bdf9e70d…` on main 97f9c8c3.

## 2. Changes staged (see `CORRECTIONS.md`, `BATCH_READY_v2.md`)
The pre-Lean correction batch landed as **main 97f9c8c3** (theory-ci green; 28 patches; 17 re-freezes; requotes, rehashes, seat additions, A:IDEAL-W+ E2 note, T12 notes-only line). Staged, not landed (`NEXT_BATCH/NEXT_BATCH.md`): the MEAS-D stage (MEASD8) and its NB-C items, NA_DROP v1.4, D5Pa v2 (a-1, a-2), the DIST-2 delta (R1 edits; Sol-6 verdict goes into the 1.4.11 cell), the T10 texts, the T12 carrier, the `W3-START2-R:MIS` status re-point carrier. Digests on 97f9c8c3: MEASD8 bdf9e70d, D5Pa v3 a9353d82 (T6-3 folded in; supersedes v2 0c84bf9f), NA_DROP v1.5 9ddef7fd (supersedes v1.4 f398a048), DIST-2 985b75cf (rebase PURE 9.5). Deferred: T4-R4.

## 3. Declined / not changed
_to fill by the manager from the cards (the coordinator does not rule on findings)._

## 4. Lean-readiness notes (see `BLUEPRINT_NOTES.md`)
See `BLUEPRINT_NOTES.md` (ranked items per target; first paper-only dependency of each Level-2 target; T9/T10 sections).

## 5. Coverage statement (HQ a810898a; `Lean/BRIEF.md` on main)
- **Certificates.** Only a MATCH (fidelity check: the Lean statement equals the paper statement) counts as a certificate of a paper theorem, cited by its number. A WEAKER result gets its own lemma label and is never cited as the paper theorem.
- **Level-2 headlines.** Each Level-2 headline names its first paper-only dependency, the first named axiom or hypothesis that Lean assumes without proof (listed per target in `BLUEPRINT_NOTES.md`; `FIDELITY.md` records it with every named axiom).
- **Counterexamples.** A counterexample found during formalization means the target is SUSPECT: escalate to HQ and stop work on that target.

## 6. Status of b′-1 / T6-1 and open items at the time of this draft
- **T6-1 = ERRATA E1 = Sol-5b b′-1: not claimed beyond output runs (HQ ruling, option C).** The Fable's allocation proof (FITS) was applied as NA_DROP v1.4 (Opus R4 8.7, PURE 9.3), but Sol-6 (b″) returned 8.4 FAIL with b″-1: the creation/interning of the `paste` keys, the global string cache and the IDEAL-W⁺ decimal cost are not bounded. HQ ruled option (C): the delivery conclusion keeps "on output"; the allocation card's claim is withdrawn (its inventory stays as a note, not a claim); no new premise; Cor 6L's other conclusions, clause (o) and the qualifier removals on output runs stand. **NA_DROP v1.5** = `9ddef7fd…` on main 97f9c8c3 (tag WEAKER: (C3)(iii) rewritten, same 4 lines; Opus R6 8.7 PASS, Opus PURE 9.5 PASS; there is no Sol PASS on the final text; the Sol R3 8.7 FAIL and R5 8.4 FAIL are superseded by the (C) scoping).
- **DIST-2 row 1.4.11 is checked:** Sol-6 (c) R2 **9.6 PASS** on 578913a6, carried to 985b75cf by the Opus PURE of the rebase (9.5); the recorder fills the cell (`NEXT_BATCH/DIST2_cell_fill_carrier.md`).
- **Landing set** for the MEAS-D + NA_DROP + T12 dry run: `NEXT_BATCH/LANDING_SET_MEASD_NADROP_T12.md` (MEASD8 bdf9e70d, NB-C6err, NA_DROP v1.5 9ddef7fd, T12 scoped carrier, MIS re-point, DIST-2 985b75cf + cell fill). D5Pa v3 (a9353d82, T6-3) lands with the A re-pin; whichever of D5Pa v3 and NA_DROP v1.5 lands second carries the other's edits.
- **Open:** the reader clause "without 'on output' under the delivery conventions (S4)" (`CLAIMS_CARD.md:71`, `READER_VERSIONS.md:1441`, and the D5Pa v3 stage) is the unscoped Cor 6L clause that (C) withdraws: it needs the (C) scoping at the A re-pin (D5Pa v4).
- Engineering observation (not a LIST-R gap): on the exact branch `finish(fit)` is forced after `v3_list_fields` (`v3_fit.R:131`, `v3_run.R:274-277`), so `peak_memory_kb`, `timings$total` and `runtime_guard$elapsed_seconds` are measured after the helper. L3 now says so; a one-line reorder would change it but is a method change.
- Process notes: `LOG.md` (the seat cancelled on a superseded manifest, POLICIES §10; the unapplied-paragraph slip and the claimed-edit rule).

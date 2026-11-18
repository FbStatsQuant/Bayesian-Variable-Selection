# T6 Fable card (consistency tier): Thm 6 (row 3.1), Cor 6L (row 3.1L), Cor-FAMC (row 3.1F)

Inputs: Astra (3 points) and blind Sol (3 points), both with evidence trails; walk `walks/T6.md` on walkB dc2e7174 (WALK COMPLETE for all three results: 2 MINOR, 3 NOTE). Snapshot: `origin/theory/PRE-LEAN` 292f52c5, main as fetched today. **For the consultant: answer AGREE or OBJECT per row.** I changed no file.

**Verdict:** no flaw in the mathematics of Theorem 6, Corollary 6L or Corollary FAMC. Of the six Codex points, four are already closed by work done since the reads (T6-1 twice, T6-2 twice), one is Lean-only, and **one needs a wording correction** (Astra T6-3, the reader's description of the list). Nothing that is not wording is new; the one non-wording item still open (the delivery clause's code pin for rows 3.1 and 3.2) is already with HQ.

## 1. Rulings on the Codex points

| # | Point | Ruling | (a) Kind | (b) Recorded STATEMENT? | (c) Outcome |
|---|---|---|---|---|---|
| R1 | **T6-1** (Astra and Sol, independently): delivery was transferred to the tagged method without bounding the helper's allocation | AGREE; **closed** | Genuine gap in a proof (not wording) | LIST-R's proof file; no statement text | **No change now.** Closed by the allocation proof: `Sol5/FABLE_ALLOC_CARD.md`, applied as paragraph (0.6) of `L3_listR.md` in NA_DROP v1.4 (`Sol5/NA_DROP_v14/`; HQ ruled FITS; Opus R4 8.7, PURE 9.3). Not re-opened. |
| R2 | **T6-2** (Astra and Sol): IDEAL-W⁺ says the two rejection predicates are "treated as true" | AGREE; **closed** | Wording inversion | DLV-0's premise span | **No change now.** This is T8-1. The correction is already on main: `W3-RM2-R/STATEMENT.md:80-81` reads "the two bounds are treated as satisfied (the rejection predicates … never fire)". |
| R3 | **Astra T6-3**: the reader calls the list "the best-scored models met by the run" | AGREE | **Wording overclaim** | No (reader prose and card; the master LIST-CODE (iii) is right) | **Correction needed**; text below. |
| R4 | **Sol T6-3** (Lean-compile): measurability of the data events, the output indicator and the summaries; rate on output as a joint event | AGREE, Lean-only | Not a flaw | No | **No change.** The proof already takes "probability, or outer probability if measurability …" (`L3_listR.md:100`) and states the rate through the joint event of output and error. MEAS-D supplies measurability for the uninterrupted run once it is recorded. |

### R3: why, and the exact text

- LIST-CODE (iii) defines the list as distinct models of 𝓜^run, the set of models **offered to the final-run ledger** (`W3-D5P/STATEMENT.md:81-83, 91-92`). That set holds the models scored in the final run and the models carried into it (block tables, models inherited from calibration). It does not hold every model the calibration scored.
- So a model scored during calibration, better than some list entry but not carried forward, is "met by the run" and not in the list. The reader's parenthesis says more than the master. The 40p + 1 bound and the retention of S₀ use exactly 𝓜^run, so nothing in the corollary depends on the loose wording.
- Corollary 9C's reader text already has the accurate description (`READER_VERSIONS.md:1144-1147`); the fix reuses it.

**`READER_VERSIONS.md:1435`.** Old: "(the best-scored models met by the run)"
New: "(on a sampler run, the best-scored models among those offered to its final stage: the models scored there and the models carried into it from the precomputed tables and the calibration; on exact enumeration, the best-scored of all models)"

**`CLAIMS_CARD.md:71`.** Old: "holds it in its returned list of at most $40p+1$ best-scored models"
New: "holds it in its returned list of at most $40p+1$ models, the best-scored among those offered to the run's final stage"

The same sentence sits in the staged reader copies (`Sol5/D5Pa/staged_reader/`, `Sol5/D5Pa_b330/staged_reader/`, line 1435); they need the same replacement when that batch lands.

## 2. Rulings on the walk rows

| Row | Ruling | (a) Kind | (b) Recorded STATEMENT? | (c) Outcome |
|---|---|---|---|---|
| **F1** (NOTE, Lean): RM0-plus's link from mathematics to code is two sentences resting on named premises | AGREE | Lean note | No | No change. The interface is in the T8 card and its delta (four clauses). |
| **F2** (MINOR): row 3.1's delivery clause rests on DLV-0 at its pin; the core is three commits later | AGREE | Record gap, not wording | No text is wrong | **For the manager, already ruled by HQ (G1):** re-pin DLV-0 and LIST-CODE to `method-v3.1.1-listpip`. For Cor 6L the transfer is now proved (NA_DROP v1.4, (0.5)–(0.6)). For rows 3.1 and 3.2 themselves it waits for that re-pin. No file changed by me. |
| **F3** (MINOR): L3 (0.5) named one `stop` row; there are three | AGREE; **closed** | Proof text | No | No change now. The staged L3 since v1.3 lists all three rows with the reason each cannot fire (`v3_run.R:251, 253, 263`). |
| **F4** (NOTE): at main the guard hunk was missing, so a non-completed sampler fit got NA list fields flagged `empty_list` | AGREE; **closed** | Code and spec agreement | No | No change. At the tag the helper runs only when `status == "completed"` (`v3_fit.R:176`; I read it at core tree 61b0a582). This also closes the extra finding in my Sol-1 card. |
| **F5** (NOTE, Lean): DLV-0 and LIST-CODE are code readings | AGREE | Lean note | No | No change. They enter Lean as hypotheses. |

**Left uncovered by the walk:** it is complete for all three results, down to recorded inputs (`W3-RM:E4`, `W2-APP:POST`, the C-DLV results, and the classical facts it names). By its own note it walked the logic of DLV-0's steps, not the completeness of the exit inventory, which rests on the C-DLV audits that Sol-1 confirmed. Corollary FAMC has "no finding of its own"; its dossier wording was handled in the Sol-4 card.

## 3. Correctness (beyond Codex and the walk)

Nothing further. Two cross-checks against my earlier cards:
- The Cor 6L ↔ Cor 9C sentence at `READER_VERSIONS.md:1443` and `CLAIMS_CARD.md:71` is the Sol-2 S2-1 correction; R3 above is a different phrase in the same card cell, so the two edits should be applied together.
- Astra's check of FAMC's AR conditions matches the Sol-4 card: the separation bound is quantitative, and no uniformity as |ρ| → 1 is used.

## 4. Lean readiness (ranked; no item changes a statement)

1. **LIST-K at Level 1.** For a probability π on a finite Ω and a list 𝒯 ∋ S₀ with m = π(𝒯): 1 − ε ≤ m ≤ 1; the list PIPs are within ε of the truth and of the exact PIPs (the distance from π to π restricted to 𝒯 is 1 − m); the list median is S₀ when ε < ½.
   - Gain: Cor 6L's displays are certified with finite sums. It reuses the master lemma of T2 and the finite-sum transfer of T3. Named axioms: none.
2. **RM0-plus's core at Level 1**, over the four-clause interface (F1): the descent on a down-closed family under the no-addition and no-truth-loss events, and the inclusion 𝒪 ∩ {Ŝ ≠ S₀} ⊆ 𝓜_nᶜ ∪ 𝒦_nᶜ. Same item as T8 Lean item 1.
3. **Theorem 6's probability layer as two bounds.** P(𝓜_nᶜ) ≤ 2·E[1 − π(S₀)] from the T4 headline through the Gaussian-row bridge; P(𝒦_nᶜ) → 0 from the three imported events.
   - Level-2 named axioms: Laurent–Massart χ² tails; Gaussian concentration for Lipschitz functions; Gaussian tail with a union bound.
4. **Delivery and the list as hypotheses:** "every valid input gives output under (D)" and LIST-CODE (i)–(v). The allocation chain of (0.6) is plain arithmetic and can be Level 1 if wanted.
5. **Cor-FAMC as an assembly:** Lemma VIS (Schur complements; the sign route; the generic-position route, which needs compactness of the closure of the visibility directions) plus the block and AR computations, feeding Theorem 6's hypotheses. No new named axiom.

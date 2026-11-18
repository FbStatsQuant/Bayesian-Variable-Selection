# Pre-Lean pass: brief (HQ, 2026-11-18; owner GO this morning)

Owner (11-17/18):
- Codex is fine for this check (resets are available). Split it about half Astra `gpt-6.2-astra` and half Sol `gpt-6.2-sol`, both at high effort.
- A Fable on Claude Personal validates the final ruling on every Codex point; its interventions are short and precise.
- Acceptance filter: accept only (a) genuine flaws we missed or (b) changes needed to compile in Lean. No complexity growth, no changing what works, no nitpicks.
- New (11-18): the Fable pass also asks whether each Lean-bound proof can be **simplified or restructured so that the Lean work is easier**.

Owner: the Theory Department. It runs the pass serially, staffs it token-lean (POLICIES §4–5, §14), and reports to HQ at each block.

## Targets
| # | Target | Astra 6.2 (break it) | Fable (rulings + Lean readiness) | Lean |
|---|---|---|---|---|
| T1 | Thm 3(a) rate lower bound (W3-PSHARP:B) | yes | yes | shortlist 1 |
| T2 | Posterior summaries SL0 + pooling bound LT-d (C-PACK:SL0, W3-SAMP:LT-d) | yes | yes | shortlist 2 |
| T3 | Domination transfer (Cor 9C core) + Hellinger reduction (W3-DIST:H), Lemma D0 | yes | yes | shortlist 3 |
| T4 | Thm 1 (true model, rows 1.1/1.2) + the presented Thm 2 (Thm2SG) | yes | yes | Dec (Level 2) |
| T5 | Thm 9 (true distribution, row 2.1) | yes | yes | Dec (Level 2) |
| T6 | Thm 6 + Cor 6L + Cor-FAMC (rows 3.1, 3.1L, 3.1F) | yes, **after** Cor 6L is recorded | yes | later |
| T7 | Thm 4, omitted variables (row 1.4) | yes | yes | later |
| T8 | Thm 7, fixed-design reported model (row 3.2), + Thm 5, start law concentrates (row 3.3) | yes | yes | later |
| T9 | Row 3.5 evidence unbiased + Thm 10 printed outputs (row 3.6) + pooling (row 4.1) | yes | yes | Dec (row 3.5) |
| T10 | Thm 8, certified screening (row 3.7) | yes | yes | later |

**Owner, 11-18 morning: "a whole pre-Lean check".** Every presented theorem and corollary in the card (rows 1.1–1.4, 2.1, 3.1–3.7, 4.1; T4 includes Thm 1′) is covered, not only the Lean-bound ones. The order is T1–T5 (Lean-bound first), then T7–T10, then T6 once Cor 6L is recorded. The empirical rows (4.2, 4.3, 5.x) and the body remark 2.2 are out of scope.

**Sol 6.2 final-text confirmations** (results whose last round was Opus only), consolidated to about 5 calls:
1. C1 code audit;
2. READER R4/R5;
3. W3-D2 + W3-D3;
4. track V R4 + FAMC;
5. W3-D5P (Cor 6L), after it is recorded. The NA_DROP Sol seat piggybacks on this call.

Order: T1–T5 and Sol 1–4 start now; T6 and Sol 5 follow the Cor 6L recording. Run the format converter locally before every Codex call. Work one Codex call at a time.

## Fable role (one Fable 5.2, Claude Personal, effort high, a Theory child, sequential over T1–T6 in one context)
For each target, after Codex has returned, it writes a card of at most 1 page:
1. **Rulings:** each Codex point gets AGREE or OBJECT with the proposed ruling, in at most 3 lines.
2. **Correctness:** anything Codex missed, if seen while reading. No open-ended hunts.
3. **Lean readiness:** at most 5 ranked suggestions, each giving its gain for Lean, its cost, and whether the statement changes:
   - simplifications (fewer cases, a shorter route, standard textbook or Mathlib-available lemmas in place of bespoke ones);
   - restructurings (isolating the deterministic core, explicit constants, cleaner dependency order);
   - the Level-2 named axioms each proof would need.

The consultant (HQ's Fable) is consulted only where the Fable OBJECTs to a ruling or proposes a statement change.

## Acceptance (binding)
- **Proof simplifications** with the statement unchanged are adopted if localized and cheaper to formalize. They get an Opus diff check, plus Sol 6.2 if the change is substantive. Recorded as CORRECTION-ONLY or PATCH.
- **Statement changes** (including those Lean needs) go through the normal route: seats, then H5 with the consultant, then HQ. They must not weaken any headline statement without HQ and owner sign-off.
- Everything else is logged and declined. No complexity growth.
- Kill budget: the whole pass ≈ 3–4 days. Codex ≈ 15 calls (10 Astra, 5 Sol). Fable ≈ 10 short passes plus at most 3 consultant cards.

## Output
`Theory_work/Wave3/PRE_LEAN_PASS/` holds, per target, the Codex review, the Fable card, the rulings and the adopted changes. It also holds a one-page SUMMARY for the owner's theory sign-off: findings, what changed, what was declined, and the Lean-readiness notes the Lean Department will use as its blueprint input.

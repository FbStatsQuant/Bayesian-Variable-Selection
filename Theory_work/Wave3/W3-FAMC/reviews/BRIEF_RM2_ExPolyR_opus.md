# BRIEF — RM2 Opus seat for W3-RM2:Ex-PolyR, W2-LOC2:Lemma-BC, W2-LOC2:Lemma-IR (HQ route (b); saved before launch)

Seat: claude-opus-5-5 (claudeAgent_personal, effort high). Fresh: not the author of E2, BC or IR, not the W3-FAMC E2-check
seat, not a W3-FAMC council seat. Checkout `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3fadba7-ec4a2133fdcc2bcf`.

**Binding manifest.** `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1r.txt` = MANIFEST
322e8c121e76a3d19d31b4870b39da8e09baa18d6c92f330d8f74ee293eaadd6. This is the digest that Astra's Ex-PolyR ACCEPT is bound to
(`W3-RM2/reviews/R1r_record_astra.md:21`, verdict line :26, round R1). It contains `W3-RM2/STATEMENT.md`,
`W3-RM2/lemmas/L6_examples.md` and `W2-LOC2/lemmas/L6_poly.md` (EXT). First run, from the repo root,
`python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2 Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1r.txt`.
If it does not print OK, stop and write gates=FAIL.

**Files.** Write ONLY `Theory_work/Wave3/W3-FAMC/reviews/RM2_ExPolyR_seat_opus.md`. Do not edit anything in W3-RM2 or
W2-LOC2, make no git changes and start no sub-agents. Read long files in chunks of at most 120 lines. Do not read RM2's
LOG/CHECKPOINTs or other reviews of these claims, except: `Theory_work/Wave3/W3-FAMC/reviews/E2_check_opus_R1.md`, which you
may use as a POINTER ONLY (where to look). Its verdicts are not evidence for you. Re-derive everything yourself.

**Scope (each claim in full).**
1. `W3-RM2:Ex-PolyR@1.0.3`: registered statement `W3-RM2/STATEMENT.md:259-275` (the E2 part of the examples claim,
   Form R polynomial decay) and its full proof, `W3-RM2/lemmas/L6_examples.md:164-263` (all of §E2), together with the parts
   of §0 (`L6_examples.md:33-103`) that E2 uses. Check E2 for its **whole class**: general Σ with unit diagonal, spectrum
   [c, C], polynomial envelope with any α > 2, any injection π, any b ∈ [1/(2α), ½), ϱ = (½ − b)/30, every hypothesis of
   RM2-R it claims to verify (`W3-RM2/STATEMENT.md` §3.2, :172-202; RM `W3-RM/STATEMENT.md:126-156`), and the implication
   it stipulates (`(D-loc^b) ⇒ (D-R^b) ⇒ (W-R)`; you may take `W3-RM2:D-to-W` as given and check only that E2 supplies its
   inputs, `W3-RM2/lemmas/L5_formR.md:108-117`).
2. `W2-LOC2:Lemma-BC@1.0.0` **as a whole lemma**: statement `W2-LOC2/lemmas/L6_poly.md:78-84` (for every fixed integer M,
   uniform in p, positions, indices and U with |U| ≤ M; the spectral clause without size restriction), premises :33-41, and
   the full proof through :109.
3. `W2-LOC2:Lemma-IR@1.0.0` **as a whole lemma**: statement `L6_poly.md:118-129` (every α > 2; uniform in the subset and n),
   premises :33-41, and the full proof through :167.
If you read or verify only part of a claim (e.g. one value of M or α, or one instance), mark that row **NOT-EXAMINED**.

**Gates (as in RM2 council R1).** G1 the mathematics is correct; G2 the load-bearing assumptions match the statements;
G3 no hidden hypothesis (independence, uniformity, selection); G4 inherited statuses and conditions are carried (BC and IR
are conditions of Ex-PolyR); G5 constants and exponents are tracked where the conclusion needs them. Acceptance filter:
genuine flaws only, no nitpicks; null-set caveats never block. Tag findings C (wrong or unproved step), S (claims more than
proved), F (unfaithful to a cited source) or E (editorial).

**Output, exactly.** (i) the header line `model: claude-opus-5-5 (claudeAgent_personal, high); round=R1; seat=opus;
manifest=322e8c121e76a3d19d31b4870b39da8e09baa18d6c92f330d8f74ee293eaadd6`; (ii) the table
```
| id | decision |
|---|---|
| W3-RM2:Ex-PolyR | ACCEPT / NOT-EXAMINED / REJECT |
| W2-LOC2:Lemma-BC | … |
| W2-LOC2:Lemma-IR | … |
```
(iii) findings and gate verdicts (G1–G5, PASS/FAIL, one line each), with file:line; (iv) a score 0.0–10.0; (v) exactly ONE
line of its own, in exactly this form (backticks allowed; write no other line containing COUNCIL-VERDICT):
```
COUNCIL-VERDICT round=R1 manifest=322e8c121e76a3d19d31b4870b39da8e09baa18d6c92f330d8f74ee293eaadd6 seat=opus score=<x.y> gates=PASS|FAIL
```
gates=PASS only if all of G1–G5 pass and you hold no C, S or F finding. Final message: ≤ 6 lines.

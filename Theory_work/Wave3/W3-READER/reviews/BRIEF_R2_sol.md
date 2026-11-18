# BRIEF R2 — council seat `sol` (round R2, after R1 fixes) — W3-READER

You are one of two independent council seats (gpt-6.1-sol, reasoning effort high). You decide whether the frozen content below is correct,
faithful to its master theorems and honestly reported. Be adversarial: a pass from you means you checked each reader
statement against its master and re-derived each bridge, not that it read well.

## Content under review (frozen as `MANIFEST 3af23c3572d21511fe59fe7a610991eb2b92858e0309a8ee7ac1e8ff43636a4b`, file `Theory_work/Wave3/W3-READER/reviews/MANIFEST_R2.txt`)
Everything in `Theory_work/Wave3/W3-READER/` that `manifest.py` covers (all except `reviews/`, `LOG.md`,
`CHECKPOINT_*.md`). **Under review:** `READER_VERSIONS.md` (reader versions of the headline theorems, each = a registered
master theorem + bridges), `NOTATION.md` (setup), `CLAIMS_CARD.md` (plain-word rows), `STATEMENT.md` (claim
`W3-READER:PoolZ`), `lemmas/R1_set_sizes.md`, `lemmas/R2_local_regression.md`, `lemmas/R3_delivery_assembly.md`,
`lemmas/R4_printed_outputs.md`, `lemmas/B3_8_orth_witness.md` (record of bridge B3.8), `REPORT.md` (registry blocks), `METHOD_INTUITION.md` (code facts only).
**Not under review, do not read:** `GATES.md`, `gates_staged.tsv`, `TRIAGE_SHARP3.md`, `CARD_ROW11_R03b.md`, `SHARP3_REQUEST.md`,
`helpers/`, `api/` (strength-gate records and blind sharpness audits); `deltas/` (a staged, not-in-force delta); `tools/`; `BRIEF*.md`.
External inputs (the masters and their sources; the list is in `reviews/MANIFEST_R2.txt`'s extra inputs): the STATEMENT files and cited lemma
lines of W3-POST, W3-POST2, W2-APP (`lemmas/L1_POST.md`), W3-PSHARP, W3-PSHARP-R, W3-MISR, W3-MISR-R, W3-START,
W3-START2, W3-START2-R, W3-RM, W3-RM2, W3-RM2-R, W3-SAMP, W3-SCR, W3-DIST, W1-N1, W2-UNI (`lemmas/L5_delivery.md`), C-DLV
(`STATEMENT.md`), `Wave1C/FINAL/sections/s6_delivery.tex`; the assumption registry `Theory_work/INFRA/registry/assumptions.tsv`
(row `A:IDEAL-W+`);
the registry `Theory_work/INFRA/registry/claims.tsv` (status column, for G4 only); the code `Scripts/SMC_BVS/core/`.
**Do not read** anything under `Theory_work/Wave3/W3-READER/reviews/` except `MANIFEST_R2.txt` and the two R1 reviews named below,
nor `LOG.md`, nor `CHECKPOINT_*.md`. You may write and run code; keep it under
`/home/fb31/BVS-wt/W3-READER/.rc_tmp/R2_scratch_sol/` (git-ignored; D62). Change no other file; do not commit; start no subagents.

## What the ticket claims
(1) Reader versions: each headline theorem restated with numbered assumptions in standard terms and a 1–3-display
conclusion, claimed to follow from its master theorem plus the listed bridges, with nothing hidden and nothing stronger
than the master; statuses quoted verbatim, conditions carried. Where a row has two forms (row 1.1 is in Form A; Form B is kept for the record only and is not under review; row 3.7
and Theorem 8′ forms (a) / (b1)), review both. (2) New claims: `W3-READER:PoolZ` and bridge lemmas R1–R4.

## Previous round (R1, MANIFEST_R1 759a7dfd…): findings and the lead's changes
R1 scores: sol 7.4 (gates FAIL, FIDELITY: NOT-FAITHFUL), opus 7.6 (gates FAIL). You may read the two R1 reviews
(`reviews/R1_council_sol.md`, `reviews/R1_council_opus.md`) for detail; read nothing else under `reviews/`.
Every R1 finding was accepted; check that each fix is correct and complete, then review the whole content afresh.
- Theorem 1 remark (vi) and (A2) line: lower-bound domain $s_0\le\min(K-1,p/2)$ restored ($s_0<p$ via Prop. LB).
- Card row 3.2: case (b) carries its own beta-min at $\sigma_*\sqrt{(|Q|+\log n)/(n\varphi_0^2)}$; standard scale for case (a).
- Card rows 3.5 / 4.1 and METHOD_INTUITION table: potential uninterrupted records; equal to the printed evidence on completed
  runs; no unbiasedness conditional on completion. PoolZ claim line: "data fixed"; joint-law form "consequently", with H-U/SI.
- R3: restricted to the former hypotheses (those of W3-RM2:RM2-R / RM2-F) and labelled historical; the current Theorems 6–7
  use only the identities B6.6′ / B7.5 with W3-RM2-R:DLV-0 (summary table and REPORT updated). (S4)(v) references removed.
- Moderate-$n$ posterior shape (Thm 1 (vii), Thm 10 why-line, card note, METHOD_INTUITION): relabelled an Engineering
  observation (D-17); no finite-$n$ statement claimed; the odds/chi-square mechanism sentence removed.
- METHOD_INTUITION / NOTATION code facts: prior cost $\log((2p-1-k)/(k+1))$ plus Occam $\tfrac12\log n$ from the marginal
  likelihood; pilot ESS with forced steps; fallback order; $m(\emptyset)\bar Z_0$ initial factor; ledger scope of the reported
  model; preflight stop before any record; Theorem 8 gloss.
- Card row 3.6: AR/block sentence now "for particular AR or block designs that satisfy Theorem 6's visibility, leakage, floor
  and local-regression conditions" (the two seats proposed different wordings; Sol's, which makes no family-level claim, was used).
- Delivery-route sentence: the original C-DLV Prop-F used the LS0 cap $\ell_n$; frozen F-UNI@2.1.0 states the shipped cap; the
  active route is DLV-0.
- Card: setting exceptions (rows 1.4, 2.1); row 3.3 "with probability tending to one"; row 3.7 "Buys" narrowed.
- Theorem 5 leakage form (only "$l\notin S_0$" changes); Theorem 7 honest limits (ii), Remark (a) as (BM-Q♭), example statuses
  verbatim; Theorem 6 remark (i) $\mathcal G_n$ choice; Theorem 8′ exact gain formula; B2.1 constant; REPORT line ranges;
  status base line; B3.8 record copied to `lemmas/B3_8_orth_witness.md`.
Also new since R1 (HQ order, presentation): rows 3.1, 3.5, 3.6 state "The guarantees describe the run as if uninterrupted; a run
stopped by its time guard reports status `resource_limit` and no output", with a pointer to the meaning of "output" in Theorem 6.

## Gates (each PASS or FAIL, with reasons)
- **G1 correctness.** Re-derive every step of R1–R4 and PoolZ (arithmetic, inequalities, assembly of cited results).
- **G2 hypotheses used = stated.** Each bridge proves exactly what the reader version needs from exactly its hypotheses.
- **G3 faithfulness (gate F).** For every reader statement (Theorems 1, 1′, 2–10, 8′): every hypothesis of the master
  is implied by the reader assumptions via a listed bridge or is a listed standing convention ((S1)–(S5)); no conclusion
  is stronger than the master (quantifiers, uniformity, expectation vs probability, localisation to events, branch and
  scope); card rows are faithful to their reader statements.
- **Interpretive sentences (D71).** List every interpretive sentence in the reader statements and card rows ("hence …",
  "so …", "i.e. …", readings such as "the posterior concentrates on the support of the best candidate predictor", remarks
  that paraphrase a conclusion) and judge each: SUPPORTED by the master (cite the line) / OVERSTATED / UNSUPPORTED. An
  overstated or unsupported reading is an S or F finding and counts under G3.
- **G4 statuses and citations.** Statuses verbatim against `claims.tsv`; nothing below PROVED-CHECKED presented as
  checked; "conditional on …" carried; cited line ranges say what is claimed.
- **G5 no hidden finite-n or scope claims.** No text claims a finite-n property the masters do not give, a two-sided rate
  on every design, or n-dependent signals where the master fixes constants.
- **G6 fidelity to the code.** NOTATION and METHOD_INTUITION describe the coded prior, posterior, start law, local
  search, pooling (equal weights) and outputs as the code does (pins cited).

## Output (PROTOCOL_v4 §5)
Write your review to `Theory_work/Wave3/W3-READER/reviews/R2_council_sol.md`:
- a per-claim table `| id | decision |` with ACCEPT / REJECT / NOT-EXAMINED for: `W3-READER:PoolZ`, `W3-READER:R1`,
  `W3-READER:R2`, `W3-READER:R3`, `W3-READER:R4`, `RV/thm1` … `RV/thm10`;
- findings, each tagged **C** (correctness), **S** (strength: claims more than proved, or uses an unstated hypothesis),
  **F** (faithfulness to master / code / cited source) or **E** (editorial), with file:line and the exact correction;
- the six gates; an overall score (0.0–10.0, one decimal) reflecting C, S and F only.
You **must** give `gates=FAIL` if you hold a C, S or F finding of your own, whatever severity you would give it.

## Fidelity line (this seat only; HQ order)
Besides the gates, give exactly one line `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL` on the **final reader
statements** (every hypothesis of each master carried, nothing stronger than the master). This is the fresh fidelity
read required before acceptance; NOT-FAITHFUL requires at least one F or S finding naming the statement and clause.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 3af23c3572d21511fe59fe7a610991eb2b92858e0309a8ee7ac1e8ff43636a4b` (round R2, seat `sol`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R2 manifest=3af23c3572d21511fe59fe7a610991eb2b92858e0309a8ee7ac1e8ff43636a4b seat=sol score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---

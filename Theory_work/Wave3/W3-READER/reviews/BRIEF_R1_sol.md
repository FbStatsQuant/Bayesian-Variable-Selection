# BRIEF R1 — council seat `sol` (blind first read) — W3-READER (DRAFT: `<digest>` filled at the CP3 freeze)

You are one of two independent council seats (gpt-6.1-sol, reasoning effort high). You decide whether the frozen content below is correct,
faithful to its master theorems and honestly reported. Be adversarial: a pass from you means you checked each reader
statement against its master and re-derived each bridge, not that it read well.

## Content under review (frozen as `MANIFEST <digest>`, file `Theory_work/Wave3/W3-READER/reviews/MANIFEST_R1.txt`)
Everything in `Theory_work/Wave3/W3-READER/` that `manifest.py` covers (all except `reviews/`, `LOG.md`,
`CHECKPOINT_*.md`). **Under review:** `READER_VERSIONS.md` (reader versions of the headline theorems, each = a registered
master theorem + bridges), `NOTATION.md` (setup), `CLAIMS_CARD.md` (plain-word rows), `STATEMENT.md` (claim
`W3-READER:PoolZ`), `lemmas/R1_set_sizes.md`, `lemmas/R2_local_regression.md`, `lemmas/R3_delivery_assembly.md`,
`lemmas/R4_printed_outputs.md`, `REPORT.md` (registry blocks), `METHOD_INTUITION.md` (code facts only).
**Not under review, do not read:** `GATES.md`, `gates_staged.tsv`, `TRIAGE_SHARP3.md`, `CARD_ROW11_R03b.md`, `SHARP3_REQUEST.md`,
`helpers/`, `api/` (strength-gate records and blind sharpness audits); `deltas/` (a staged, not-in-force delta); `BRIEF*.md`.
External inputs (the masters and their sources; listed in `reviews/INPUTS_R1.txt`): the STATEMENT files and cited lemma
lines of W3-POST, W3-POST2, W2-APP (`lemmas/L1_POST.md`), W3-PSHARP, W3-MISR, W3-START, W3-START2, W3-RM, W3-RM2, W3-SAMP,
W3-SCR, W1-N1, W2-UNI (`lemmas/L5_delivery.md`), C-DLV (`STATEMENT.md`), `Wave1C/FINAL/sections/s6_delivery.tex`;
the registry `Theory_work/INFRA/registry/claims.tsv` (status column, for G4 only); the code `Scripts/SMC_BVS/core/`.
**Do not read** anything under `Theory_work/Wave3/W3-READER/reviews/` (no earlier review, disposition, brief or score),
nor `LOG.md`, nor `CHECKPOINT_*.md`. You may write and run code; keep it under
`Theory_work/Wave3/W3-READER/reviews/R1_scratch_sol/`. Change no other file; do not commit; start no subagents.

## What the ticket claims
(1) Reader versions: each headline theorem restated with numbered assumptions in standard terms and a 1–3-display
conclusion, claimed to follow from its master theorem plus the listed bridges, with nothing hidden and nothing stronger
than the master; statuses quoted verbatim, conditions carried. Where a row has two forms (row 1.1 Form A / B1; row 3.7
and Theorem 8′ forms (a) / (b1)), review both. (2) New claims: `W3-READER:PoolZ` and bridge lemmas R1–R4.

## Gates (each PASS or FAIL, with reasons)
- **G1 correctness.** Re-derive every step of R1–R4 and PoolZ (arithmetic, inequalities, assembly of cited results).
- **G2 hypotheses used = stated.** Each bridge proves exactly what the reader version needs from exactly its hypotheses.
- **G3 faithfulness (gate F).** For every reader statement (Theorems 1, 1′, 2–8, 8′, 10): every hypothesis of the master
  is implied by the reader assumptions via a listed bridge or is a listed standing convention ((S1)–(S5)); no conclusion
  is stronger than the master (quantifiers, uniformity, expectation vs probability, localisation to events, branch and
  scope); card rows are faithful to their reader statements.
- **G4 statuses and citations.** Statuses verbatim against `claims.tsv`; nothing below PROVED-CHECKED presented as
  checked; "conditional on …" carried; cited line ranges say what is claimed.
- **G5 no hidden finite-n or scope claims.** No text claims a finite-n property the masters do not give, a two-sided rate
  on every design, or n-dependent signals where the master fixes constants.
- **G6 fidelity to the code.** NOTATION and METHOD_INTUITION describe the coded prior, posterior, start law, local
  search, pooling (equal weights) and outputs as the code does (pins cited).

## Output (PROTOCOL_v4 §5)
Write your review to `Theory_work/Wave3/W3-READER/reviews/R1_council_sol.md`:
- a per-claim table `| id | decision |` with ACCEPT / REJECT / NOT-EXAMINED for: `W3-READER:PoolZ`, `W3-READER:R1`,
  `W3-READER:R2`, `W3-READER:R3`, `W3-READER:R4`, `RV/thm1` … `RV/thm8`, `RV/thm10` (thm9 is a placeholder: NOT-EXAMINED);
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

You are reviewing the content frozen as `MANIFEST <digest>` (round R1, seat `sol`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=<digest> seat=sol score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---

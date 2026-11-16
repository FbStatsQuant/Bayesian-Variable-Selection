# BRIEF — council round R1, seat `opus` (Claude Opus 5.5, effort high, Claude Third) — blind first read

You are one of the two council seats for theory ticket W3-START2-R (Tier B rider) of the SMC-BVS project. This file is
your whole brief. Work only inside the worktree `/home/fb31/BVS-wt/W3-START2-R`. Paths that start with `lemmas/`,
`numerics/`, `reviews/` or are `STATEMENT.md`, `REPORT.md`, `PLAN.md`, `BRIEF.md`, `TARGET.md`, `READER_DELTA.md`,
`DEPS.tsv`, `citecheck.py` are relative to the ticket folder `Theory_work/Wave3/W3-START2-R/`; "BASE" means `Theory_work/Wave3/W3-START/`
(statement v1.3.4), "PARENT" means `Theory_work/Wave3/W3-START2/` (statement v1.4.1); all other paths are relative to the
worktree root. **Change no git state and write no file in the repository.** Set no TMPDIR. If you need scratch output
(for example `python Theory_work/Wave3/W3-START2-R/citecheck.py /home/fb31/BVS-wt/W3-START2-R/.rc_tmp/cc.txt`), write it only under
`/home/fb31/BVS-wt/W3-START2-R/.rc_tmp/` (git-ignored) and delete that folder at the end. Do not start subagents. Return
your review as your final message; the lead saves it verbatim to `Theory_work/Wave3/W3-START2-R/reviews/R1_council_opus.md`.

## Frozen content
The round is frozen in `reviews/MANIFEST_R1.txt`; its first line is `MANIFEST 1834d1c0941f297eef629337b02361097a0d2f02ae1596afeaa4bf322ebbab19`. You may run
`python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START2-R Theory_work/Wave3/W3-START2-R/reviews/MANIFEST_R1.txt`.

## Files you may read
The files listed in that manifest: `STATEMENT.md` (the claims, version 1.5 — a **delta statement** over PARENT
`STATEMENT.md` v1.4.1, itself a delta over BASE `STATEMENT.md` v1.3.4), the five proof files `lemmas/R1_VIS.md`,
`lemmas/R2_NEC.md`, `lemmas/R3_RATE.md`, `lemmas/R4_TRANSFER_COR.md`, `lemmas/R5_EX.md`, `REPORT.md` (technical report with
the registry blocks), `TARGET.md`, `READER_DELTA.md` (proposed reader version of the headline statements), `PLAN.md`,
`BRIEF.md`, `RIDER_RULES.md`, `DEPS.tsv`, `citecheck.py`, the `numerics/` folder, and the external inputs listed in
`reviews/INPUTS.txt` (BASE and PARENT statements and proof files, one source statement, one numerics helper). For
context only, not proof premises: `Theory_work/INFRA/registry/claims.tsv`, `Theory_work/Wave3/PROTOCOL_v4.md`,
`Theory_work/Wave3/PROGRAM.md`. **Do not read** any other file in any `reviews/` folder (except the manifest and
INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`, and do not use `git log`, `git show` or `git diff` on the ticket
folder: this is a blind first read.

## Standing of the parents
BASE and PARENT are other tickets' recorded content and are **not** under review: take their statements and proof steps
as given. Under review is every new step and every use of a parent result: wherever a proof cites a parent line range,
open it and check that it says what is taken from it, hypotheses included.

## What the council decides
The package claims that every claim of `STATEMENT.md` §3 (ids in `REPORT.md` §3: VIS-c, VIS-m, START-F, F1–F3, F4, NEC-b,
NEC, TRANSFER, MIS, EX, OVL, BR, START-R, IF-START) is proved in `lemmas/`, and that each implies the parent claim named in
`STATEMENT.md` §5. Decide whether the package can be accepted as **checked mathematics**. You are briefed to break it:
assume there is an error and look for it.

* **G1 — correctness of every step.** Re-derive; do not sample. Most effort on the new steps: `lemmas/R3_RATE.md` R3.3
  (the bound 𝔏^♯_n = O_P(√log n) under (FL-R16) and (D5) only: conditional law at U ⊊ S₀, the shift d̄⁰_n, the event E⁰,
  Markov) and R3.6 (composition with PARENT Proposition P1.4 / P1.7); R3.1–R3.2, R3.5 (N̄_n; C_B with 15κ_H; the index
  n_H); `lemmas/R1_VIS.md` R1.2–R1.3 (the exact price π_n(d, a; Q), both signs; log(2p) kept) and R1.5 (only the
  visibility thresholds change); `lemmas/R2_NEC.md` R2.1–R2.4 (pointwise level; drifting clauses, large gains), R2.5
  (pigeonhole), R2.6 (example), R2.7 (F4⁺⁺ bound); `lemmas/R4_TRANSFER_COR.md` R4.1 (conditional probabilities, maxima
  over s₀ ≤ s̄, random rates), R4.4 (Gaussian (GR)); `lemmas/R5_EX.md` R5.2 ((V-mp) check, rates, A > 3/4).
* **G2 — hypotheses used = hypotheses stated**, claim by claim.
* **G3 — no hidden assumptions** (independence across columns or directions; p → ∞; a bound on |Q| or |H_l| beyond the
  stated ones; a uniform starting index where only "for all large n" is assumed; conditioning on a response-dependent
  object; s₀ ≥ 1 where s₀ = 0 is covered).
* **G4 — imports and supersession.** Each parent result is used as stated; nothing else is consumed; each row of the
  supersession table (`STATEMENT.md` §5) really implies the parent claim; `REPORT.md` claims no status the files do
  not support.
* **G5 — constants and rates tracked**, including the uniformity in (T1⁺⁺)(d) and in Q, and the dependence of
  thresholds on n_H.
* **G6 — fidelity.** No new property of the coded start is needed beyond BASE `STATEMENT.md` §1; `path:line` citations
  resolve to what is said (`citecheck.py`); the reader version in `READER_DELTA.md` follows from the master statements
  through the bridges it names (PROGRAM "Readability"; a reader version may assume more, never conclude more).

Also check `REPORT.md` (claims table vs statement and proofs; sharpness record and numerics paragraph say no more than the
files support; open items honest) and `DEPS.tsv` (spot-check rows).

**Finding tags (PROTOCOL_v4 §5).** Tag every finding **C** (a step is wrong or unproved), **S** (the text claims more than
is proved, or uses an unstated hypothesis), **F** (unfaithful to the code as pinned, to a cited source, or to STATEMENT in
derived text such as REPORT or READER_DELTA) or **E** (editorial: wording, notation, record, citation form, presentation
of numerics). Name the clause or line and say what fails. **You must give `gates=FAIL` if you hold any C, S or F finding
of your own, whatever severity you would give it.** E findings never block. "A stronger theorem is provable" is not a
finding: list such proposals separately as better-theorem proposals.

Project convention (owner's rule, not a defect): every result is asymptotic (n → ∞) unless marked *deterministic*. Do not
score the size of n at which a bound becomes informative; do score any asymptotic claim that is false, unproved or
stated more strongly than proved.

## Output format (your final message)
```
Verdict summary: one paragraph.
Gate table: G1 … G6, each PASS or FAIL with a justification naming what you re-derived.
Per-claim table: | id | decision |  — every id of REPORT.md §3, decision ACCEPT / REJECT / NOT-EXAMINED.
Findings: numbered; each tagged C / S / F / E, with file:line, what fails, and the repair you propose.
Better-theorem proposals (if any).
Overall score: x.y / 10 (reflects C, S, F findings only; 8.0 or more means acceptable as checked mathematics as it stands).
Checks performed. Not checked.
```

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 1834d1c0941f297eef629337b02361097a0d2f02ae1596afeaa4bf322ebbab19` (round R1, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=1834d1c0941f297eef629337b02361097a0d2f02ae1596afeaa4bf322ebbab19 seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---

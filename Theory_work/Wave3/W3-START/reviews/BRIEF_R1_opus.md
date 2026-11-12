# BRIEF — council round R1, seat `opus` (Claude Opus 5.5 on Claude Work, effort high) — blind first read

You are one of the two council seats for theory ticket W3-START of the SMC-BVS project. This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START`. Paths below that start with `lemmas/`,
`numerics/`, `reviews/` or are `STATEMENT.md`, `REPORT.md`, `PLAN.md`, `BRIEF.md`, `ASSUMPTION_MAP.md`, `citecheck.py` are
relative to the ticket folder `Theory_work/Wave3/W3-START/`; all other paths are relative to the worktree root.
**Change no git state. Write exactly one file:** `Theory_work/Wave3/W3-START/reviews/R1_council_opus.md`. Do not edit
any other file in the repository. Do not start subagents. Use no effort setting above high. If you run code, keep
your scripts outside the repository or inline; do not let any script write into the repository (run copies elsewhere
if a script writes output files).

## Frozen content
The round is frozen in `reviews/MANIFEST_R1.txt`. Its first line is `MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97`. You may run
`python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START Theory_work/Wave3/W3-START/reviews/MANIFEST_R1.txt`.

## Files you may read
Only files listed in that manifest: `STATEMENT.md` (the claims, v1.3.3), the eleven proof files
`lemmas/L1_AGG_FLOOR.md` … `lemmas/L11_EXAMPLES.md`, `REPORT.md` (the technical report: claims table, assumption ids,
relations to existing results, sharpness record, open items), `PLAN.md`, `BRIEF.md` (HQ's ticket brief),
`ASSUMPTION_MAP.md`, `citecheck.py`, the `numerics/` folder, and the external inputs listed in `reviews/INPUTS.txt` (pinned
code, wave documents, sources of the argument, consumers' statements, the registry). **Do not read** any other file
in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`: this is a blind
first read, and you must form your verdict without any earlier review, disposition or score.

## What the council decides
The package claims that every item of `STATEMENT.md` §5 — the component lemmas (C0)–(C2), the bridge lemmas (B1),
(B-TK), (B-L), (B-V1), (B-V2), (B-R), the theorems (T0)–(T6), and the five verified example families of (T7) — is
proved in `lemmas/`, with no registry claim consumed. `REPORT.md` §3 gives one line per claim. You decide whether this
package can be accepted as **checked mathematics**. You are briefed to break it: assume there is an error and look
for it. Score the package on six gates; a gate PASSes only if you found no blocking issue for it.

* **G1 — correctness of every step.** Re-derive the arguments; do not sample. Give most of your effort to the steps
  on which the main results rest: the fibre bound and the two-sided identities of `lemmas/L1_AGG_FLOOR.md`; the score
  expansion under the unnormalised Gram floor in `lemmas/L2_TK.md`; the linearisation and the Markov step of
  `lemmas/L3_LEAK.md`; Steps 2–6 of `lemmas/L4_VIS.md` L4.1; the probability accounting and the uniformity of
  `lemmas/L5_ASM_STARTF.md` L5.2; the conditional law and the Gaussian integral of `lemmas/L9_BR.md` L9.5 and the
  assembly L9.6–L9.7; the transfer `lemmas/L8_TRANSFER.md`; Proposition OVL in `lemmas/L10_INTERFACES.md`; example F-2 in
  `lemmas/L11_EXAMPLES.md`.
* **G2 — hypotheses used = hypotheses stated.** For each claim compare `STATEMENT.md` with what its proof uses.
* **G3 — no hidden assumptions** (independence between Gaussian directions or columns; a normalised Gram floor;
  s₀ ≥ 1; p > s₀; A ≥ 1; conditioning on a non-measurable event; levels, supports or sets depending on the response).
* **G4 — imports have adequate status and say what is claimed.** The ticket consumes no registry claim: check that
  nothing is used as a premise from another ticket, that every status quoted in `STATEMENT.md` §7, `REPORT.md` §4 and the
  lemma files is verbatim from `Theory_work/INFRA/registry/claims.tsv` or from the cited file, and that the consumers'
  interfaces (`Theory_work/Wave3/W3-SAMP/STATEMENT.md`) are quoted correctly and receive exactly what (T5) says.
* **G5 — constants and rates tracked.** Every constant, exponent and threshold: where it comes from, what it depends
  on, and whether the claimed uniformity (in (T1)(d), and through it in (T3)) really holds.
* **G6 — fidelity to the method as coded.** "π₀" must be the start distribution exactly as the pinned code computes
  it: check `STATEMENT.md` §1 against `Scripts/SMC_BVS/core/` (score, prior, cap, partition contract, tables, start,
  normaliser, preprocessing) and the `path:line` citations.
Also check `REPORT.md`: that each line of its claims table matches the statement and the proof it names; that the
assumption ids, the relations to existing results and the sharpness record say no more than the proofs and the
numerics support; that the honesty of scope (`STATEMENT.md` §6, the tightness clause of (B-R), the "expected, not
verified" examples, the vacuity note on (N2)) is adequate.

## Output format (in your one file)
```
Verdict summary: one paragraph.
Gate table: G1 … G6, each PASS or FAIL with a justification that names what you re-derived.
Per-claim table: every id of REPORT.md §3 — accepted | accepted with non-blocking remarks | not accepted (why).
Issues: numbered; each BLOCKING (prevents a gate from passing) or NON-BLOCKING, with location (file:line), the
        problem and the repair you propose.
Overall score: x.y / 10 (8.0 or more means: acceptable as checked mathematics as it stands).
Checks performed. Not checked.
```
The frozen content cannot be edited after this round without a new round, so say clearly which issues, if any, must
be fixed before acceptance (BLOCKING) and which can wait for a later version (NON-BLOCKING).

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97` (round R1, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97 seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---

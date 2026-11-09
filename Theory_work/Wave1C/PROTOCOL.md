# Theory Wave 1C (closure) — protocol (binding for every worker thread)

Set by Theory HQ on 2026-11-08 21:30 CST, under Felipe Bedoya's greenlight ("settle Wave 1 as close as mathematically
possible; Song–Liang (2015) is the guideline for the whole story; full autonomy; rigour; no hallucinations").

**This file extends `Theory_work/Wave1/PROTOCOL.md`. Read that file first: every rule there applies here**, with the
folder `Theory_work/Wave1C/<TICKET>/` in place of `Theory_work/Wave1/<TICKET>/`, and with the changes below.

## Goal of the wave
Close the open items of Wave 1 so that the paper's consistency story (Song–Liang 2015 as the template: posterior
consistency, sure screening, MAP/HPM selection consistency, misspecification) is stated, proved and independently
checked for SMC-BVS with p ≤ n^A (any fixed A), on correlated designs as general as possible, for the method **as it
will ship**. Inputs: `Theory_work/Wave1/*/REPORT.md` (results of Wave 1), `Theory_work/State_of_Project/` (ground truth),
Song & Liang (2015) PDF at `C:\Users\felip\.t3\userdata\attachments\647bfd65-83bc-403a-b3b0-0a8352044e7f-588fe83a-5cbe-4a20-8055-1cfbd7c9c936-pdf.pdf`.

## Deadline and checkpoints (Houston time, CST)
- **01:30** — write `CHECKPOINT.md` in your folder: what is proved/checked so far, what is left, honest estimate of
  whether the target closes by the deadline, and any narrowing you foresee. HQ reads it and may redirect you.
- **04:30** — final `REPORT.md` and final message to HQ, whatever the state. If the council has not passed by then,
  report the best checked partial result (PARTIAL), with the exact frontier. Do not stop early: if a route fails,
  try the next route; if the target fails, prove the narrowest meaningful version and characterise the obstruction
  (counterexample or explicit failing step). An answer that settles the question negatively (a checked
  counterexample, a proof that a condition is necessary) counts as closing the item.
- Check the clock (`date`) at every major step.

## Rigour and anti-hallucination rules (added)
1. **No claim without a file.** Every "verified/checked" sentence names the review file in `reviews/` containing the
   reviewer's verbatim reply. Every numerical claim names the script and output file in `numerics/` that produced it.
2. **Citation check before the council.** Run a script that opens every `path:line` you cite and confirms the
   quoted text/statement is there; save its output in `reviews/CITECHECK.txt`. Fix every miss.
3. **Reviewers are briefed to break the result**, not to confirm it: give them the statement and proof files, never
   your conclusion or log; ask for counterexamples, false steps, unstated hypotheses, constants that do not track.
4. **Falsification numerics for every lemma** before it is used downstream (exact small cases or ≤ 20-seed
   simulations; local compute only — n up to a few thousand is fine if it runs in minutes).
5. **Statuses are copied verbatim** from sources; never upgraded. "PROVED-CHECKED" = proof file + cross-family lemma
   checks + mid-point CONTINUE + sweep fixed + council passed (both ≥ 8.0, all gates, same round).
6. If a reviewer and you disagree on a step, do not argue it away: either fix it, or get a second fresh reviewer
   (different family) on that step alone, and record both.

## Method-side changes
- LS0 and the e4 tie fallback are **not yet in the production core**; ticket C-ENG merges them. Their parameters
  (e.g. the LS0 move cap ℓ_n, scan order, tie rule) may therefore still be chosen. If a proof needs a specific
  choice for a not-yet-shipped component, you may adopt it: state it explicitly in `STATEMENT.md` as a method
  requirement, flag it at the top of `REPORT.md`, and write it in `METHOD_REQUIREMENTS.md` in your folder (HQ
  forwards it to C-ENG). Changes to **already-shipped** components (prior, SMC kernels, calibration, tables) are not
  allowed: report them as findings instead.

## Models and budget (changes)
- Leads: Claude Opus 5.5 (effort high) on Claude Personal unless the brief says otherwise.
- Cross-family reviewers: Codex `gpt-6.1-sol`, reasoningEffort high (xhigh for the key lemma check, the mid-point and
  the council seat).
- Second-opinion / parallel proof attempts: Codex `gpt-6.1-sol` (high) is allowed as a long-running parallel prover.
- `gpt-6-astra`: at most two short, targeted calls per ticket. Claude Fable 5.1: only a short hard step on which Opus
  failed; log the reason. Helpers: Sonnet 5.5 / Haiku 5.5 on your own provider.
- Subagents may spawn their own subagents under the same rules; the lead remains responsible.

## Tickets
| ID | Lead | Target (brief in the delegate task) |
|---|---|---|
| C-GROW | Opus, Claude Personal | Reported-HPM consistency for growing relevance sets (study S2 AR(1), S5 factor) |
| C-DLV | Opus, Claude Personal | Delivery: P(𝒪) → 1 under a declared polynomial resource allocation |
| C-PACK | Opus, Claude Personal | Close Wave 1 residuals: e4 not needed; LH-iid unconditional; SEL/L8 checks; Song–Liang corollaries; PXN consolidated supplement |
| C-MIS | Opus, Claude Personal | Song–Liang Thm 4 analog: misspecified candidate sets |
| C-ENG | Opus, Claude Work (worktree) | Merge LS0 + tie-aware DP into the production core; tests and regression |

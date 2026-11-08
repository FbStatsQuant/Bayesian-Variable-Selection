# Theory Wave 1 — protocol (binding for every worker thread)

Set by Theory HQ on 2026-11-08, approved by Felipe Bedoya. Every worker thread reads this file first.

## Chain of command
- Felipe (owner) sets goals and decides what the paper claims. Theory HQ (the parent thread) runs the wave and reports to Felipe. Each worker thread owns **one ticket** and reports only to HQ.
- Paper goal for this wave: Song–Liang (2015)-type consistency results for SMC-BVS, polynomial dimension p ≤ n^A (A > 1 allowed), and correlated designs as general as possible.

## Ground truth and inputs
- Start from `Theory_work/State_of_Project/` (PDF `State_of_Project_v1.0.pdf`, sources in `sections/`, machine-readable registry in `registry/*.tsv`). Read `sections/00_agent_brief.tex`, your ticket's card in `sections/06_open_and_plan.tex`, and the theorem cards your ticket touches in `sections/04_theory.tex` / `04b_supplement.tex`.
- The archive is `Theory_work/Old_Projects/New_BVS_Headquarters/` (NBH), frozen at commit 21ebc28. Method code and proofs are cited from the State-of-Project document by path:line.
- Every claim you write cites its source (path:line) or your own file. Status words are copied verbatim; never upgrade a status beyond the evidence. "PROVED" by you alone = "PROVED (by this seat, unchecked)".

## Workspace
- Write only inside `Theory_work/Wave1/<TICKET>/`. Required files: `STATEMENT.md` (target statement, locked), `PLAN.md`, `LOG.md` (dated running log of decisions, results, reviews), `lemmas/` (one file per lemma), `numerics/` (scripts + outputs), `reviews/` (every reviewer reply verbatim + your disposition), `REPORT.md` (final).
- Do not edit anything outside your folder. No git commands that change state (no commit, checkout, stash, reset, push): HQ commits and pushes.
- Long proofs go in several files, never one giant response (64K output-token failure rule).
- Compute: local only, small (exact enumeration p ≤ 10, simulations ≤ 20 seeds). Nothing on Owls/NOTS.

## Review pipeline (three layers)
1. **Continuous**
   - **Statement lock** before any proof work: one cross-family reviewer checks `STATEMENT.md` + `PLAN.md` against the State-of-Project sources (is this the right target, faithfully stated, are hypotheses explicit, is the plan viable). Fix, then lock.
   - **Lemma by lemma**: before a lemma is used downstream, (a) a numerical falsification attempt (exact small cases or simulation) and (b) a line-by-line check by a cross-family reviewer. Record both in `reviews/`.
   - **LOG.md** updated at every step.
2. **Independent mid-point review** once the key lemma is proved: a fresh cross-family reviewer receives only `STATEMENT.md` and the proof files so far (not your reasoning or log) and returns CONTINUE / REDIRECT / STOP with reasons. On REDIRECT or STOP: end your run and report to HQ (do not proceed on your own).
3. **Independent final review**
   - **Exhaustive sweep** first: one cross-family reviewer lists every flaw in the full proof (not a sample); fix all or record an objection with evidence.
   - **Council**: two reviewers — Codex `gpt-6.1-sol` (reasoningEffort high) and Claude Opus 5.5 (effort high, on your own Claude provider) — score independently on: correctness of every step; hypotheses used = hypotheses stated; no hidden assumptions; cited lemmas have adequate status; constants/rates tracked; fidelity to the method as coded. Each returns gate verdicts AND an uncapped 0–10 score. Pass = both ≥ 8.0 with all gates passing in the same round. Max 3 council rounds, then report as is.
- Reviewers are started with `delegate_task`.
- **Subagents (authorized by Felipe, 2026-11-08):** each lead may spin subagents whenever useful — parallel proof attempts, lemma provers, numerics, literature/source lookups — under the model rules below. Subagents write only inside the lead's folder, follow this protocol, and their work is reviewed like the lead's. The lead stays responsible for the result. Every review is a **new** `delegate_task` with a self-contained brief: give the files, not your conclusion. Never reuse a reviewer's context for a later review.

## Models and budget
- Cross-family reviewers: Codex `gpt-6.1-sol` (default, reasoningEffort high).
- Codex `gpt-6-astra`: at most one short, targeted call per thread (e.g. a hard step the Sol reviews disagree on). Never a long run.
- Claude Fable 5.1 (`claude-fable-5-1`): only for a specific, short, hard step that Opus has failed on; never a long run. Log the reason.
- Claude helpers (numerics, transcription): Sonnet 5.5 or Haiku 5.5 on **your own** Claude provider only.
- Use `orchestrator_capabilities` once before your first `delegate_task`.

## Statement changes
- If the target must be narrowed, reformed or is refuted: log the reason and evidence, continue with the narrowest change that is still meaningful, and flag it at the top of `REPORT.md`. A counterexample to the target statement → stop and report immediately.

## Stop rules
- A lemma that fails 3 proof attempts (each with a reviewer verdict) → stop, mark STUCK with a diagnosis, report.
- Mid-point REDIRECT/STOP → report.
- Council not passed after 3 rounds → report with the scores and the open issues.

## Final report to HQ (`REPORT.md`, and the same content as your final message)
1. RESULT (one line): PROVED-CHECKED / PARTIAL / REFUTED / STUCK.
2. The statement as proved (file pointer) and any change vs the card, with reason.
3. Status per clause with evidence (which reviewer, which file).
4. Review trail: statement-lock verdict; lemma checks; mid-point verdict; sweep counts; council scores per round.
5. Open items left and the next step you recommend.
6. Files produced.

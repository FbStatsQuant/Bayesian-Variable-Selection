# BRIEF — statement diff check SC1 (seat: Codex gpt-6.1-sol, reasoningEffort high) — reconciliation, not a scored read

You are an independent reviewer for theory ticket W3-START2 of the SMC-BVS project. This file is your whole brief.
Work only inside the worktree `C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-0d1ae879-e1e1cd03cea23a59`
(all paths below are relative to it). **Change no git state** (no git command is needed). **Write exactly one file:**
`Theory_work/Wave3/W3-START2/reviews/SC1_diff_check_sol.md`. Do not edit any other file. Do not start subagents. Use
no effort setting above high. Keep the review short: this is a small diff.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START2/reviews/MANIFEST_SC1.txt`. **Quote its first line (`MANIFEST
<digest>`) verbatim at the top of your review.** You may run `python -B Theory_work/Wave3/tools/manifest.py verify
Theory_work/Wave3/W3-START2 Theory_work/Wave3/W3-START2/reviews/MANIFEST_SC1.txt` and report its result.

## Files you may read
* `Theory_work/Wave3/W3-START2/STATEMENT.md` — **version 1.4.1, the object under review**; `PLAN.md` (sketches).
* `Theory_work/Wave3/W3-START2/reviews/prev/STATEMENT_v1.4.0.md` — the previous version (sha256
  `0128495d8955383ef23f068008c5750f7a528d03084598769cc795a1bc22a029`, the `STATEMENT.md` row of
  `reviews/MANIFEST_SL1.txt`). Compare the two files with any diff tool that does not touch git state (for example
  `python -c "import difflib,io; ..."`, or `git diff --no-index` which only reads).
* `Theory_work/Wave3/W3-START2/reviews/SL1_statement_lock_sol.md` — the statement-lock review of v1.4.0 (verdict LOCK
  WITH CHANGES: required changes 1–4, optional 1–2), and `reviews/SL1_disposition.md` — the lead's disposition.
* Only if a judgement needs it: the base statement `Theory_work/Wave3/W3-START/STATEMENT.md` and the base proof files
  `Theory_work/Wave3/W3-START/lemmas/` (both in the manifest).
Read nothing else: no `LOG.md`, no `CHECKPOINT*.md`, no file in `Theory_work/Wave3/W3-START/reviews/`.

## What to decide
Version 1.4.0 was reviewed for a statement lock. Version 1.4.1 is meant to differ from it only by the corrections
that review required. The proofs are still not written. Decide two things, with file:line evidence.

**A. Each earlier finding.** For required changes 1, 2, 3, 4 and optional suggestions 1, 2 of the SL1 review give one
verdict each: RESOLVED / PARTLY RESOLVED / NOT RESOLVED. Two places deliberately do not use the reviewer's exact
wording; judge them on substance:
* finding 1 — the lead used status-neutral wording (the file "fixes target statements only and asserts no proof
  status"; "proof file: …") instead of "planned" / "to be proved" / "will be supplied". Is any assertion left that a
  proof exists, is author-proved, or is supplied?
* finding 2 — the lead lists five changed hypotheses instead of three. Is the list correct and complete: is there a
  hypothesis of any claim that differs between version 1.3.4 (base) and version 1.4.1 and is not on the list, or an
  item on the list that is not a changed hypothesis?
* finding 3 — is the new parenthesis under (T3⁺)(b) mathematically correct as an explanation, including the clause
  C_L = 0 for an arbitrary deterministic sequence Q_n with |Q_n| ≤ K?

**B. Editorial only?** List every difference between the two versions (PLAN.md has one changed line, `PLAN.md:25`;
its previous text was "so |𝒩_exc| ≤ 16 − s₀ ≤ 15 (empty if s₀ ≥ 16)"). For each, say whether it changes a definition,
an assumption, a hypothesis, a conclusion, a constant or the scope of any claim of §2–§5. Attest "editorial only"
if and only if no difference does. If some difference is substantive, name it and say what must be re-reviewed.
Also report any new error the edits introduced (a wrong line reference, a symbol clash, a sentence that is false).

## Output format (in your one file)
```
MANIFEST <digest>            (verbatim first line of the manifest)
Verdict: LOCKED (editorial only; all findings resolved) | CHANGES REQUIRED | SUBSTANTIVE CHANGE — re-review needed
Findings table: one row per SL1 item (R1–R4, O1–O2): verdict, evidence (file:line).
Differences: the list for part B, each marked editorial / substantive.
Required changes: numbered, each CRITICAL / MAJOR / MINOR, with the exact edit. "None" if none.
Not checked: list.
```
Do not propose a different theorem. End your reply with the verdict line and the path of your file.

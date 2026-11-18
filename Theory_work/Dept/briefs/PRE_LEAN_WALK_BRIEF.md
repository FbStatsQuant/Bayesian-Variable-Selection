# Pre-Lean consistency tier: FULL PROOF WALK brief (owner via HQ, 11-18; Fable 5.2 on Claude Third)

You are a Fable 5.2 proof walker, run on **Claude Third** by the owner's explicit decision, to use its headroom before the reset (≈ 12:55 CT). **You do not need the Codex replies.**

## What you do
For each assigned target, walk the **key-lemma chain step by step**, from the presented statement down to recorded inputs:
- every assumption is actually used, and none is used without being stated;
- every step is justified, by a recorded result (registry id), a standard fact or an explicit computation;
- every constant is tracked: where it is fixed and what it may depend on;
- the probability events are exactly as stated: which law, which event, whether conditional or unconditional, and "eventually" vs "for every n".

## Sources (read-only)
- **The presented statement.** Start from `Theory_work/Wave3/W3-READER/CLAIMS_CARD.md` on origin/main: row 1.1 (Thm 1, 1′), 1.2 (Thm 2), 2.1 (Thm 9), 3.1 (Thm 6), 3.1L (Cor 6L), 3.1F (Cor-FAMC), 3.2 (Thm 7), 3.6 (Thm 10). Take the master claim id from the row, then use the registry (`Theory_work/INFRA/registry/claims.tsv`) for statement and proof file:line spans and dependencies.
- **Exception, Cor 6L:** read it **as frozen at R3r**, on branch `origin/theory/W3-D5P`, ticket folder `Theory_work/Wave3/W3-D5P/`, MANIFEST_R3r `64a3ec05…`. It is not on main yet. W3-D5P's R3r patch is applied there.
- **How to read:** use `git show origin/<branch>:<path>`. Read long files in chunks.

## Output (incremental, so nothing is lost if your account limit hits)
- **File:** `Theory_work/Wave3/PRE_LEAN_PASS/walks/<target>.md`, on your own branch (see your task).
- **Top table:** findings, one row each: severity (FATAL / MAJOR / MINOR / NOTE) | file:line | claim | why.
- **Body:** one section per lemma in the chain. **Commit and push after each lemma.**
- **Footer:** "STOPPED AT: <lemma>" if you stop before the end, or "WALK COMPLETE".
- **Severity bar:** MAJOR or above means a step that is wrong, or a hypothesis that is missing in a way that would change a stated result. Report any MAJOR or above to the manager **immediately**, by finishing your turn with it, and don't wait for the end of the walk.

## Rules
- **No edits to any theory file.** Write only your walk files.
- **Scratch only in `<worktree>/.rc_tmp/`.** No shell redirects outside the worktree, no deletes.
- **No subagents.**
- **Acceptance filter:** report only (a) genuine flaws or (b) things that would block a Lean formalization. No nitpicks or style points.
- When the Claude Third limit hits or the account resets, stop. The manager records where you stopped, and the Claude Personal pre-Lean Fable takes your walk files as input.

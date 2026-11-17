# SL1+LC2 brief — statement lock and line check of track-A lemmas T1 (GW) and T2 (BLK) (Codex gpt-6.1-sol, high)

The gate read for T1 and T2 (PROTOCOL_v4 §2, Tier B, NORMAL mode: Sol lock + Sol line check, here combined in one read
on the manager's order). **Blind first read:** you get the files below and nothing else. Do not open any LOG,
CHECKPOINT, INDEX, CHECK, AUDIT or `reviews/` file. Read only; write no files; change no git state.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT` (branch `theory/W3-AUDIT`).
- T1: `Theory_work/Wave3/W3-AUDIT/track_A/T1_GW/STATEMENT.md` (v4) and `.../T1_GW/PROOF.md` (v4).
- T2: `Theory_work/Wave3/W3-AUDIT/track_A/T2_BLK/STATEMENT.md` (v4) and `.../T2_BLK/PROOF.md` (v4).
- Code of record: `Scripts/SMC_BVS/core/` (registry method pin 4676af6; confirm with
  `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core`). Read the code yourself; do not trust the line quotes.
- The sources each STATEMENT cites for its premise and its downstream uses (open them).

Context in one line each: T1 discharges the named implementation premise GUARD-W ("stop-only guard: operational
interruption ⇒ no output") of the coded SMC-BVS method; T2 discharges "the method's partition is a function of X with
blocks of at most 16 columns". Both are code lemmas under exact arithmetic (EX-A).

**Part 1 — statement lock.** For each STATEMENT: right target (does it discharge the premise as the cited downstream
statements use it?), faithful to the code and sources, every hypothesis explicit, no clause stronger than what is
proved. **Check the definitions closely** (T1: fields, Booleans, internal values, operational fields 𝒱_op with the
"cut" rule, statistical state, potential fit P°, 𝓒° = ⊥, G; T2: the partition map C(X), setting R): they were reworded
last and no reviewer has read the final wording. Verdict: LOCK / LOCK WITH CHANGES (list the required changes) /
DO NOT LOCK.

**Part 2 — line check.** Every step of each PROOF against the code: try to break it (a check site missed, a clock or
environment value that reaches a statistical field other than through a check's Boolean, a fired check that can still
end in output, a stream read by a check, an inclusion in (GW-iv) that fails; for BLK an empty or oversize block, a
dependence on y or a stream, a wrong B, a gap in the measurability or setting-R argument). Verdict per lemma:
VERIFIED / VERIFIED WITH AMENDMENTS / NOT VERIFIED.

**Reply format** (plain markdown, returned as your final message): Part 1 verdicts with required changes; Part 2
verdicts; numbered findings, each tagged **C** (correctness), **S** (strength), **F** (faithfulness) or **E**
(editorial), with file:line, what fails, and the fix where you can. Last line:
`SL1LC2-VERDICT: T1 lock=<…>, check=<…>; T2 lock=<…>, check=<…>`.

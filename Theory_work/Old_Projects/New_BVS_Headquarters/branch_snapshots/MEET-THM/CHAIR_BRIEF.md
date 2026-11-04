# MEET-THM chair brief (from HQ, 2026-11-04)

You chair "Theorems - Final meeting": the meeting that fixes the list of main theorems of paper 1 of the SMC-BVS project. You do not vote. HQ (the "SMC-BVS New HQ" thread, id `5e38497d-7dfd-48f9-88e9-b21895922f58`) approves your final package and brings it to Felipe (the PI), who approves the theorem list.

**Read first, in this order:** `theory_campaign/MEET-THM/DOSSIER.md` (frozen; binding ground rules, roster, inclusion criteria, theorem card, agenda, procedure, rules, deliverables, HQ's known issues, IC dry run); the previous meeting's `FORMAT_NOTES.md` (`git show origin/theory/MEET-v31:theory_campaign/MEET-v31/FORMAT_NOTES.md`); then the inputs listed in DOSSIER §3 as needed. `git fetch origin` first; read other branches with `git show origin/<branch>:<path>`.

## Where you work
Branch `theory/MEET-THM` (your thread's worktree). Commit everything there and push to origin after each step. Write `STATUS.md` after every step (where the meeting is, what runs, what you wait for).

## How to dispatch (T3 tools)
Call `orchestrator_capabilities` once before the first `delegate_task`. Every seat answer and every check is a **fresh `delegate_task`** (no memory between rounds; give each the files it must read). Seats are read-only: they return their answer as their final message, and you commit it **verbatim** into the meeting folder (extract the final message from the session transcript rather than retyping: Claude `~/.claude*/projects/<cwd>/<session>.jsonl`; Codex `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`).

| Role | target |
|---|---|
| Seat A | `{providerInstanceId: "claudeAgent_personal", model: "claude-fable-5-1", options: {effort: "high"}}` |
| Seat B | `{providerInstanceId: "claudeAgent", model: "claude-fable-5-1", options: {effort: "high"}}` |
| Seat C | `{providerInstanceId: "codex", model: "gpt-6-astra", options: {reasoningEffort: "high"}}` |
| Seat D (fresh eyes; its Round 0 plan is `R0_D.md`; from Round 1 it sees everything) | `{providerInstanceId: "claudeAgent_personal", model: "claude-fable-5-1", options: {effort: "high"}}` |
| Advisor E | done (Round 0 only, `R0_E.md`); its proposals stay on the table |
| Proof checker 1 (claims of A, B, D and yours) | `{providerInstanceId: "codex", model: "gpt-6.1-sol", options: {reasoningEffort: "high"}}` |
| Proof checker 2 (claims of C and E) | `{providerInstanceId: "claudeAgent", model: "claude-opus-5-5", options: {effort: "high"}}` |
| Auditor (after each synthesis and at close) | `{providerInstanceId: "codex", model: "gpt-6.1-sol", options: {reasoningEffort: "high"}}`; move to Opus on claudeAgent if Codex is tight |
| Registrar, citation checker | `{providerInstanceId: "claudeAgent", model: "claude-sonnet-5-5", options: {effort: "high"}}` |
| Clerks | `{providerInstanceId: "claudeAgent", model: "claude-haiku-5-5"}` |

The registrar has already built the inherited-results index (`origin/theory/MEET-THM-REG:theory_campaign/MEET-THM/evidence/REGISTRY_INDEX.md`); reuse it, and give the registrar the job of keeping IDs, notation and the dependency graph during the meeting.

**Accounts:** subscriptions only, **never API credit**. If an account hits its usage limit, that role **waits for the reset**. Codex is the most limited account: batch checks, keep Codex prompts tight, and prefer one larger check task over many small ones.

## Order of work
1. **R0 diff** (you + registrar): one candidate table merging the 24 draft entries, Seat D's 72 items, Advisor E's 44 packages and the 17 obligations N1–N17. Assign IDs; mark for each: draft entry it matches (independent confirmation), new candidate, or already known false (cite the registry entry). Commit `R0_DIFF.md`.
2. **Round 1** (Seats A–D, independent): agenda items 1–5 and 8, one theorem card per candidate (DOSSIER §5), tables only, a word cap per item (≤ 300 words of free text per card).
3. **Check wave 1** (statement sanity): every candidate statement → true as written? non-vacuous (exhibit a design)? route plausible? Verdict per claim; never upgrade; route by model family as in the table.
4. **Synthesis 1** + disagreement table (crux + what settles it per row) → auditor.
5. **Round 2**: rebuttals; final statements; agenda 6, 7, 9–11.
6. **Check wave 2** on revised statements → synthesis 2 → auditor.
7. **Round 3**: agenda 12 (HQ plan, charters, waves); every seat confirms "nothing missing" or names what is.
8. **Close**: deliverables of DOSSIER §9; auditor's final pass; `FORMAT_NOTES.md`; then send HQ a short message (below).

## Binding constraints
- The method is fixed (v3.1 as amended). The one allowed change: a fixed budget (R, L, ℓ, N) may become an explicit function of (n, p) if a theorem needs it. Anything else → write it in `HQ_QUESTIONS.md` and ask HQ; do not decide it.
- Paper 1 claims island-level depth only (Felipe, 2026-11-03).
- Per-theorem HQs are for paper 1 (Biometrika) only; everything else goes to `FUTURE_WORK.md` with a reason.
- Binding proposal goals (§5.1–5.4, §13.1): a theorem's failure branch may never silently drop a binding goal; it escalates to HQ.
- Status words never upgraded; "PROVED (by this seat, unchecked)" is the only status a seat gives its own argument.
- Compute: Owls only through `owls_run`, small checks; anything that must outlive a task's session is launched as a `systemd-run --user` unit (`~/.config/bvs-hq/owls/POLICY.md`). Empirical checks ≤ 20 seeds.
- Open questions at close: **none** (DOSSIER §0).

## Talking to HQ
For a decision only HQ can make, or at close, send a short message to the HQ thread with `t3_thread_send` (thread id above): what you need or what is done, and the file to read. Do not wait idle for an answer; continue with what does not depend on it.

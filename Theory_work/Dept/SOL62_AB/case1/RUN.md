# Case 1 — RUN (do not run until the manager releases it; ≤ 4 calls overall)

- **Model:** gpt-6.2-sol (codex). **Effort:** reasoningEffort **high** (as the original: "Sol (codex, gpt-6.1-sol, reasoningEffort high)"). Fresh thread, no repo/tool access needed (inputs inline); one call.
- **Prompt to send:** the contents of `case1/PROMPT_6.2.txt` verbatim (= fixed REPLAY NOTICE + the original brief text after its saved-before-launch header [BRIEF.md] + INPUTS.md blocks). Regenerate with `python3 -I Theory_work/Dept/SOL62_AB/build_inputs.py` (reads git only).
- **Deltas vs the original framing (disclosed):** (a) REPLAY NOTICE added at the top; (b) the brief's "Files to review" are supplied inline instead of read from a worktree; POST2/POST/TRIAGE/M_misr/R_reduction omitted for size (see KNOWN_ANSWER.md); (c) the brief's "write your reply to reviews/L1_statement_lock_sol.md" is overridden by the notice (reply = final message). The brief wording itself is unedited.
- **Input size:** 43,057 chars → ≈ 12,300 tokens (chars/3.5).
- **Record per run:** model id in the header, wall time, tokens (USAGE), verdict line, finding list.

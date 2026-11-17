# Case 2 — RUN (hold until released; ≤ 4 calls overall)

- **Model:** gpt-6.2-sol (codex). **Effort:** reasoningEffort **high** (as the original). Fresh thread. Code execution allowed (the original used it for the 65-digit check); no repo access.
- **Prompt to send:** `case2/PROMPT_6.2.txt` verbatim (REPLAY NOTICE + original brief text [BRIEF.md after its header] + INPUTS.md blocks).
- **Deltas (disclosed):** REPLAY NOTICE added; only the files listed in KNOWN_ANSWER.md "Not supplied" are inline (STATEMENT, PROOF, TARGET, numerics script+output, two source excerpts); the brief's output-file instruction is overridden by the notice. The brief itself is unedited, including the machine-checked verdict line with manifest 6f8c05aa… (the 6.2 is asked to emit it; treat it as format only — it did not review that manifest byte-for-byte, so `gates=FAIL` would be formally forced by the brief's own rule; judge the 6.2 on the findings/ACCEPT decisions, not on that line).
- **Input size:** 39,693 chars → ≈ 11,300 tokens.
- **Record per run:** model id, wall time, tokens, per-claim decisions, finding list, whether F1 is named (and with which numbers).

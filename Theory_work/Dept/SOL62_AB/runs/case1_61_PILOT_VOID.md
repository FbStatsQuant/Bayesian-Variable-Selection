# case1 · gpt-6.1-sol (codex, high), PILOT, VOID for scoring (input truncated)

Run 2026-11-17 19:03 to about 19:20 CT. Wrapper: "cat the prompt file exactly once". The shell tool truncated the 46.7k-char file, so the model missed the end of §4 and most of §§5–8 of the delta statement. **This is a harness artifact. Do not score it.** The wrapper for all scored runs (both arms) is fixed to read the file in chunks of 120 lines.

What it produced on the truncated input (for reference only):
- **Verdict:** LOCK-VERDICT: NO-LOCK.
- **L1-1 MAJOR:** KL(ii) row-wise identification is false for design-dependent α. The counterexample is α = X²_{𝒞,2,1}. This **catches the known answer**.
- **L1-2 MINOR:** the Cramér summary omits "conditionally".
- **L1-3 MINOR:** the conditional-mean remark needs an integrability convention.
- **L1-4 MAJOR:** the record is incomplete. This is partly the truncation, and partly the omitted sources, which are disclosed in RUN.md.
- **Q1–Q6:** answered. Q5 could not be verified (truncation).

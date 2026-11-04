# Fable 5.1 (high) Stage C review — phase 2 (rulings), thread <thread>, completed 2026-10-22 17:53Z

Rulings and edits below are verbatim. The per-claim reasoning, also verbatim, is in the thread.

**Outcome.** Every fatal or gap claim in the Review records was accepted by the per-theorem leads, and none was rejected. Fable agrees with every lead answer, and each fix works in the final proof:
- T09: Astra #1 r1 fatal; Opus r1 F1.
- T11(iii): A1-F1, A1-F2, A1-F3, A1-R2-F2, Opus OB-F8.
- T12: Astra #2 claim 1, Opus G1, Opus G2.
- T13: A1-1; B-A2-1, B-O-1 to B-O-4.
- T20: A1-1 fatal, A1-2.
- T14(i), T15, T22, T23(ii) and T31(i) had no fatal or gap claim. Their deferred exposition items are harmless.

**Astra's findings.** T12-E1 is correct and needs a wording change. T23-E1 is correct and needs a one-line convention.

**Fable's own caveats, closed.**
- The T12 certificate code, read as code, computes what the proof claims, and the build copies are byte-identical to the originals. The phase-1 note that the certificate was "only referenced" is withdrawn.
- T20's H03 matches T03(i), plus the "eventually s₀ ≤ K" clause of assumption R.

## Final verdicts

| Theorem | Final verdict |
|---|---|
| T09 | correct as is |
| T11(iii) | correct as is |
| T12 | correct, with exposition edits E12-1 and E12-2 |
| T13 | correct as is |
| T14(i) | correct as is |
| T15 | correct as is |
| T20(i)–(ii) | correct as is |
| T22(i)(ii)(iv) | correct as is |
| T23(ii) | correct, with exposition edit E23-1 |
| T31(i) | correct as is |

## Edits

**E12-1 (T12 proof §8.2, the sentence beginning "Every enclosure has width below").** Replace

> Every enclosure has width below $10^{-52}$, which the code checks by an exact endpoint comparison (the last \texttt{CHECK} line of each block of the log, reproduced in Appendix~\ref{T12:app:log}).

with

> Every enclosure has width below $10^{-52}$: the last \texttt{CHECK} line of each block of the log (Appendix~\ref{T12:app:log}) subtracts the two exact endpoints of each enclosure in ordinary \texttt{mpf} arithmetic and compares the largest difference with the floating-point constant \texttt{1e-52}; that subtraction rounds by at most one part in $2^{53}$, against a margin of a factor five, and no conclusion of the proof uses this width. The five decisive \texttt{CHECK} lines compare an exact interval endpoint with a floating-point constant whose rounding cannot cross the threshold it stands for.

**E12-2 (T12 proof, Appendix B, last sentence before the log).** Replace

> The last \texttt{CHECK} line of each block compares the exact width of every enclosure in that block with $10^{-52}$.

with

> The last \texttt{CHECK} line of each block computes, for every enclosure in that block, the difference of its two exact endpoints in ordinary \texttt{mpf} arithmetic and compares the largest with the floating-point constant \texttt{1e-52}; this is a display check and is not used by the proof.

**E23-1 (T23 STATEMENT §3, conclusion (ii-a)).** Append after the displayed inequality:

> If S₀ ∉ Ω, the method does not define o_j(S₀, 1); it may then be given any real value, and the inequality holds for every such choice, because every path state lies in Ω and so B̄_r = 1.

No other edit is required.

**Closing statement.** "I agree with Astra on both findings and with every lead answer, so no argument is opened. Both final reviewers hold all ten proofs correct."

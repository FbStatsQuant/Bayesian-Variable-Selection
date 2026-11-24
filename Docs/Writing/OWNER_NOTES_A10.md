# Owner feedback on A9 (the short version, smc_bvs_short_2026-11-24.pdf), collected by HQ, 2026-11-24

Screenshots are in the HQ thread; the gist is below, in order.

1. **Table 1, "vs Song and Liang" column: unreadable without knowing their paper by heart.** "Their model (1)",
   "their strict sparsity (4)", "their Condition 5 (marginal, no margin)" mean nothing to the reader.
   - Each cell must say in words what their condition is and how ours compares, self-contained.
   - Example: "they assume every true predictor has nonzero marginal covariance with y; we assume it stays bounded away
     from 0 even after conditioning on any 15 others".
   - No bare equation or condition numbers. A citation may follow in parentheses.
2. **What he LIKED (keep and extend this style):**
   - the "In words" paragraph after A9: (a) only a small set Q, fewer than √n, can imitate the signal…; (b)…; (c)…;
     examples for independent, block and AR designs; why pervasive factors fail. This gives him intuition;
   - the A10 explanation paragraph ("an eigenvalue floor and signal bounds of the same kind as A6 and A5, now on the
     observed design and on sets of the budget size…").
   - Every assumption should get an "in words" explanation of this quality.
3. **Table 1 is meant to tell him whether each assumption is reasonable.**
   - The "Reasonable?" column is "not bad, not great".
   - The "vs Song and Liang" column is "as good as nothing for some rows".
   - Both columns must actually answer the question: is this assumption reasonable for real data, why, and how does
     it compare to theirs, in plain words.
4. **Add a short section, before Table 1, stating Song and Liang's conditions** that the table compares against: model,
   sparsity, Conditions 1, 3, 5, and the rest. Give each a formula plus words, with its page. "Else it is pointless."

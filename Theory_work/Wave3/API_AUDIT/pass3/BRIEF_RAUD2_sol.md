# R-AUD2 — confirm or reject three audit GAP findings (Sol, HQ 2026-11-11)

You are an independent correctness reviewer (gpt-6.1-sol, reasoningEffort high). Repo
`C:/Users/felip/Bayesian-Variable-Selection` (main). **Change no git state and no repo file except your output file.**

A blind automated audit (pass 3) reported GAPs in three author-only PROVED (never council-checked) claims of stopped
factor-design tickets. Findings verbatim in `Theory_work/Wave3/API_AUDIT/pass3/results/`:
1. **W2-FAC-S5F:L0** (`Theory_work/Wave2/W2-FAC-S5F/lemmas/L0_general_tools.md`) — results/f20.md: Finding 1 (L0.2
   multiplier bound M_A ≤ ½(1+2/log n) needs a lower bound on ‖e‖² not in E⁰_n; repair: add {‖e‖²/σ² ≥ n−1−n^{2/3}});
   Finding 2 (L0.6(b) uses an unstated hypothesis (TR′); repair: add it).
2. **W2-FAC-S5F:L1** (`.../lemmas/L1_bcs_structure.md`) — results/f21.md: Finding 1 (L1.6 needs an unstated growth
   condition on p, or R_n restated as 2R_loc + š_max√a·L_n); Finding 2 (L1.7 inherits the L0.2 issue).
3. **W2-FAC-X:L4r.5** (`Theory_work/Wave2/W2-FAC-X/lemmas/L4r_path.md` ~l.205–225) — results/f23.md: Finding 1 (FACB
   L4.3 Case A "J_c ≤ 5m_c" quoted for all m_c, counterexample at small m_c); Finding 2 (the "in particular" bound has an
   O(1), not o(1), remainder and an unstated constant relation (11/K₁)^{1/2} ≤ 0.34ε_b).

For each finding decide **CONFIRMED** (give the minimal correct repair or restatement; say whether the lemma's
downstream use survives the repair), **REJECTED** (cite the lines that carry the hypothesis), or **CONFIRMED-WORDING**.
Check the counterexamples. Then, using `Theory_work/INFRA/registry/claims.tsv` (`depends_on`, `premises`) and a search of
`Theory_work/` (incl. `FINAL/` chapter sources), list every claim or chapter passage that relies on these three lemmas
and say whether any PROVED-CHECKED claim or chapter statement is affected (HQ's quick check found only W2-FAC-S5F:C1,
C4 within the ticket).

Output: `Theory_work/Wave3/API_AUDIT/pass3/R-AUD2_sol.md`. Final message ≤ 8 lines: one verdict per finding + impact.

# R-AUD1 — confirm or reject one audit finding (Sol, brief, HQ 2026-11-11)

You are an independent correctness reviewer (gpt-6.1-sol, reasoningEffort high). Repo
`C:/Users/felip/Bayesian-Variable-Selection` (main). **Change no git state and no repo file except your output file.**

An automated blind audit reported a GAP in registry claim **C-DLV:Prop-F** (Proposition F, fallback;
`Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md` l.79–91; statement l.79–84). The finding (verbatim in
`Theory_work/Wave3/API_AUDIT/pass1/results/f07.md`, section "C-DLV:Prop-F", finding 1): the conclusion "on the classes
above P(Ŝ⁺ = S₀) → 1 unconditionally" is asserted under Theorem D's premises (l.7–9: computational/idealisation
premises + model G) only, but the proof gets it from Corollary D′ (l.51–77), which needs P(𝒦_nᶜ) → 0 and
E[1 − π(S₀|y)] → 0 — available only under the hypotheses of the consumed results (W1-GEN (H0)–(H2), W1-PXN SIZE,
p_n → ∞, (OP)), which the proposition does not state. Context: `Theory_work/Wave1C/C-DLV/STATEMENT.md` (C2), the
registry row in `Theory_work/INFRA/registry/claims.tsv`, and the consumed results' statements.

Decide: **CONFIRMED** (the statement as written claims more than the proof gives; say exactly what hypothesis is
missing and give the minimal correct restatement), **REJECTED** (the hypotheses are in fact carried by the statement's
wording or by "the classes above"; cite the lines), or **CONFIRMED-WORDING** (only the word "unconditionally"/scope is
misleading, the intended reading is correct). Also say whether any registered consumer of C-DLV:Prop-F relies on the
over-strong reading (search `depends_on`/`consumes` in claims.tsv and the chapter sources under `Theory_work/`).

Output: `Theory_work/Wave3/API_AUDIT/pass1/R-AUD1_sol.md`. Final message ≤ 6 lines with the verdict.

# SL1 disposition (statement lock, Codex gpt-6.1-sol high) — 2026-11-09

Verdict: LOCK WITH CHANGES; no counterexample found; reviewer independently re-derived LT-b, LT-d, C-ii, C-iii constants.

| # | Required change | Disposition |
|---|---|---|
| 1 | Localise asymptotics to 𝒜 / completed; joint law; integrate min(1, ρ) | ACCEPTED. STATEMENT v2 §0 "Two probability levels"; LT-e, C-v, D-iv restated as P(𝒜 ∩ {error}) → 0 and P(completed ∩ {Ŝ ≠ S₀}) → 0; P-START, P-OVL localised with 1_𝒜; §3 states P(𝒜) → 1 not claimed. |
| 2 | Restore admissible-h class in MR; identify the extension imported | ACCEPTED. MR now uses W1-N1's jointly measurable, deterministically bounded h(S; c); prefixes deterministic given the order; fixed s. MR cites T12 (i.a)-(i.c),(ii) for fixed c and announces the freezing extension to the augmented path record, proved in `lemmas/MR_identities.md`. PLAN updated. |
| 3 | Ẑ_r = exp(log_Z_r); component vs production corollaries; explicit rate antecedents in C-v | ACCEPTED. §0 and labels "production corollary" (D-iii, D-iv, C-v); C-v names W3-POST Thm 1 (Rate) and p ≤ n^A. |
| 4 | Faithful dependency statuses; limited completed-vs-potential comparison | ACCEPTED. §1 quotes W1-N1, START/KERNEL, T12 STATUS ("not adopted") and the card's PROVED-LOCKED with provenance; new Lemma PC (proved in `lemmas/PC_completed.md`); §3 keeps the full GUARD-W audit out of scope. |
| 5 | CC text corrections (run_island_s, τ indexing, pilot final step, start.h:92, W3-POST line) | ACCEPTED. CC v2; W3-POST citation now `:76-77` with antecedents `:59-77`. |

Optional suggestions: falsification tests at ½ ties, cap, island dependence, rare large W, stopped-sum inequality itself, regression-realisable vs artificial examples — adopted into the LC numerics plan.

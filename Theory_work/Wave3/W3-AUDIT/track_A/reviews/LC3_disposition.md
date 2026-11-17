# LC3 disposition (lead, 2026-11-16 17:44 CST) — reply `LC3_reply_opus.md`

All 18 findings accepted; none is C ("No mathematical step failed in any of the four items"). T6 → v2, T7 → v2, T8 → v2,
T9 → v2.

| # | item | tag | action |
|---|---|---|---|
| T6-1 | T6 | S | (Z): log Ẑ₀ = log m(∅) + log Z̄₀ stated exactly. |
| T6-2 | T6 | F | N9 citation corrected to `PROOF.md:254-255`. |
| T6-3 | T6 | E | m_b ≤ B ≤ K from BLK-b and BLK-a (and ENC-a). |
| T6-4 | T6 | E | `start_summary` (`cpp/v3_core.cpp:198`) and `v3_setup.R:73` added (the reviewer's `:72` is the setup-failure return; `:73` is `start <- r$start`). |
| T6-5 | T6 | F | "Reading" paragraph: START = (Z) + (S) + (S′) + CC4. |
| T6-6 | T6 | E | Index-convention sentence; s_b vs N9's r_b noted. |
| T7-1 | T7 | S | Cache exactness argued directly (no dependence on T3). |
| T7-2 | T7 | E | Graph: symmetric, loop-free, duplicate-free; which properties the ratio uses. |
| T7-3 | T7 | E | (KER-d) "the score function is fixed by the data". |
| T8-1 | T8 | S | (A5) defined in the STATEMENT as IF-START's leakage hypothesis Q = S₀ (the reader version's "no leakage"). |
| T8-2 | T8 | S | "hypotheses of IF-START, which include (A5)". |
| T8-3 | T8 | S/F | OVL route: full hypotheses of OVL⁺ and the two substitutions of OVL⁺⁺; "word for word" removed. |
| T8-4 | T8 | E | T ≥ 1 cited at the call `v3_run.R:225`. |
| T8-5 | T8 | E | 0·∞ convention; actual D_r = potential D_r on 𝒜 (T5 CAL-d). |
| T9-1 | T9 | F | Verdict paragraph: TDP_E (4) holds at the pin only for cap ≥ 2; its line numbers are stale. |
| T9-2 | T9 | F | (TDP-c) now proved directly for the code at the pin (slack telescoping), not via W1-N3's earlier copy. |
| T9-3 | T9 | F | Statement says how TDP-IMPL is met (output + bounds, routine TDP-E ≠ literal L7); fast-path cost O(min(|E|, cap)·(J(B+2) + p log p)) proved. |
| T9-4 | T9 | E | Precision (i) reworded: deterministic recomputation under (H2-FP). |

Re-check of the LC2 and LC3 repairs: LC4 (a new Opus agent).

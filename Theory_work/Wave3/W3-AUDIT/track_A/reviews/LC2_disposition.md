# LC2 disposition (lead, 2026-11-16 17:33 CST) — reply `LC2_reply_opus.md`

All 19 findings accepted. No failing argument: the two C findings were a wrong justification (T3 #1) and a missed site
(T10 #13); both repaired. T3 → v2, T4 → v2, T5 → v2, T10 → v2, T9 → v1.1 (clause TDP-e).

| # | item | tag | action |
|---|---|---|---|
| 1 | T3 | C | The validators X7/X8 are not claimed to pass by an inequality; on a completed run they have passed (their failure is an R error without a fit). |
| 2 | T3 | F | (OPC-d): enumeration-branch line added (Ŝ⁺ = max over Ω, `cpp/v3_core.cpp:548`), so RM-0 (b)'s inclusion holds on every output run. |
| 3 | T3 | S | 𝒪̄ := 𝒪°, 𝒮̄⁺ := the potential all-scored set ⊇ 𝓜, stated in Step 4. |
| 4 | T3 | E | "same sequence of centres". |
| 5 | T4 | S | (ENC-b) extended to the `Data` (written only by `data_init`; `mutable` counters not read by `start_mode`). |
| 6 | T4 | E | `cpp_tables`' local `Start` added to the writer list. |
| 7 | T4 | E | |C_b| ≤ B from BLK-b; `check_B` bounds B. |
| 8 | T4 | F | λ finite stated. |
| 9 | T5 | F | (CAL-d) now cites T1 PROOF Step 4 (⊇) — the induction to the return of `v3_calibrate` — instead of GW-iii; no T1 edit (T1 is at the Sol gate). |
| 10 | T5 | S | Flag paragraph: only upper bounds on statistical events transfer; W3-SAMP makes no lower-bound or conditional claim (`W3-SAMP/STATEMENT.md:35`). |
| 11 | T5 | S | Ψ(X, y, seed, U⁰…U⁹), the seed only as the label. |
| 12 | T5 | E | `runtime` named as operational. |
| 13 | T10 | C | `get_holder`'s stop added as an unreachable X2 site. |
| 14 | T10 | F | T9 gains (TDP-e) (E ≠ ∅, root check passes); T10 cites it. |
| 15 | T10 | S | X2-imp line: implicit Rcpp/R errors argued unreachable (code-reading standard of S.3). |
| 16 | T10 | S | X7/X8 reachable only under IDEAL-W's unbounded reading; dead for inputs R represents (ℓ_n ≤ 32). Recorder note for the C-DLV erratum. |
| 17 | T10 | E | `check_blocks` callers and the rethrow corrected. |
| 18 | T10 | E | Callers of the scorer's k > K check completed. |
| 19 | T10 | E | `C-DLV:Prop-F` cited (`REPORT.md:70`; `lemmas/L4_delivery.md:79-93`); D1 also in binary64. |

Re-check of the repair: folded into LC4 (a new Opus agent, after LC3), together with LC3's repairs.

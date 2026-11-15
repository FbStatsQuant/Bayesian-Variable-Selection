# LC1 disposition (lead, 2026-11-11) — cross-family line checks of lemmas L1–L5

Manifest `867e1c933d6fbbcbfd47b5deccf3b7f132d156fef1a29113de20e55eb5fefe38` quoted by all three reviewers; `manifest.py bind` OK.
All three are blind first reads (briefs `BRIEF_LC1_A_sol.md`, `BRIEF_LC1_B_sol.md`, `BRIEF_LC1_C_astra.md`).

| seat | object | verdict | file |
|---|---|---|---|
| LC1-A, Codex gpt-6.1-sol high | L1 (AGG, FLOOR, T0) | VERIFIED-WITH-AMENDMENTS (2 MINOR) | `LC1_A_line_check.md` |
| LC1-B, Codex gpt-6.1-sol high | L2 (Lemma TK) | VERIFIED | `LC1_B_line_check.md` |
| LC1-B, Codex gpt-6.1-sol high | L4 ((B-V2), (B-V1)) | VERIFIED-WITH-AMENDMENTS (1 MINOR, 1 MINOR on numerics reporting) | `LC1_B_line_check.md` |
| LC1-C, Codex gpt-6-astra high | L3 (Lemma J, (B-L), F4) | VERIFIED-WITH-AMENDMENTS (2 MINOR) | `LC1_C_line_check.md` |
| LC1-C, Codex gpt-6-astra high | L5 ((C1), (T1)(a)–(d)) | VERIFIED | `LC1_C_line_check.md` |

No CRITICAL or MAJOR finding. Every amendment is the reviewer's exact local repair; `STATEMENT.md` v1.3 is unchanged.

| # | finding | action |
|---|---|---|
| A1 | (P3) quantifier did not keep k inside the domain of w | applied: "For integers 0 ≤ D ≤ k ≤ p and a ≥ 0 with k − D + a ≤ p" (`lemmas/L1_AGG_FLOOR.md`); every application has k ≤ K ≤ p |
| A2 | `falsify_L1.R`: `sample(mb:p, 1)` misreads mb = p, so some trials had a block larger than K | applied: `sample.int` + `stopifnot(mb <= K, K <= p)`; both recorded seeds re-run, 0 violations |
| B1 | ϑ̄_n used in L4 Step 4 without a definition | applied: defined at the start of Step 4 (`lemmas/L4_VIS.md`) |
| B2 | numerics: identity errors and max\|ρ\| vs ω_n were printed, not asserted; R_U tested with realised constants | applied: identities (2.1), (TK-e) are now asserted; the ρ/ω_n comparison and the realised-constant checks are labelled as such in the script header and in `RESULTS_LEMMAS.md`; re-run, 0 violations |
| C1 | "all four depend only on (n, A)" false because g_n used z_n (which depends on p) | applied: g_n, x̄_n, ς_n are now defined with the envelope z̄_n² = 2 log(2²¹) + 2A log n + 2 log log n, so they depend only on (n, A); L3.3 notes z_n ≤ z̄_n (`lemmas/L3_LEAK.md`) |
| C2 | F4 remark on default levels omitted the factor \|Q\| + 1 | applied: the charge is stated for ϱ_n/(\|Q\| + 1) (`lemmas/L3_LEAK.md` L3.5); the locked statement already carries the factor |

Coverage notes of the reviewers recorded in `numerics/lemmas/RESULTS_LEMMAS.md` ("What the scripts do not test").
The amended files are read in full by the independent mid-point reviewer (next round, fresh manifest), which serves
as the fresh read of these changes.

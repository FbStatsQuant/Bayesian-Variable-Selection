# SC3 disposition (lead, 2026-11-11) — review `reviews/SC3_change_check_sol.md` (Codex gpt-6.1-sol high, blind)

Manifest `bf619625bf0880c6dd270771fcd0e9c94c9eeb268e75212cb918c8ab5a24dd61` quoted by the reviewer; `manifest.py bind` OK.
Verdict: **ACCEPT WITH CHANGES** (1 MAJOR, 1 MINOR, 3 optional). All applied; STATEMENT v1.3 is LOCKED with them.

| # | class | finding | action |
|---|---|---|---|
| 1 | MAJOR | [TK] promised only ω_n → 0; the step bound of (B-L) linearises a gain of order log n, so it needs ω_n log n → 0 | applied verbatim: the [TK] row now reads "max\|ρ_U\| ≤ ω_n, where ω_n is deterministic and ω_n log n → 0". Lemma TK (`lemmas/L2_TK.md`) proves it locally with ω_n = O(n^{−1/3}); no RSS lemma is imported |
| 2 | MINOR | the default-level parenthesis of (T1) evaluated 𝔏⁰_n(h), 𝔏_n(S₀; h) for Q ≠ S₀, where h has no entries on Q ∖ S₀ | applied verbatim: the identities for 𝔏⁰_n and 𝔏_n(S₀) are stated for Q = S₀ only |
| O1 | optional | Proposition OVL became provisional; say so in §0 and §6 | applied: §0 (v) and §6 qualified ("provisionally, see (T5)"); (AGG-c) stays unconditional. HQ's CP1 decision is the source of the proviso |
| O2 | optional | F4 does not show that default-level (AL) fails for every leaking column; the (J2) comparison is a threshold for an upper bound | applied: examples table and the F4 remark reworded |
| O3 | optional | r̄_n in (T3)(a) deterministic and nonnegative | applied |

No hypothesis or conclusion changed beyond the reviewer's exact edits; the two required edits were dictated verbatim by
the reviewer, so no further round is run on them (same handling as SL2 in leg A). The mid-point review reads the final
v1.3 text.

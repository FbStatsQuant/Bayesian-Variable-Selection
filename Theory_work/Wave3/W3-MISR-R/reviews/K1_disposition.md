# K1 disposition (line check of G1, G2, H1, H2 + statement-change check; Sol gpt-6.1-sol high, new agent, blind; NORMAL)

Reply verbatim: `K1_linecheck_sol.md`. K1-VERDICT: 0 FATAL / 0 MAJOR / 2 MINOR / 1 NIT. Lemma verdicts: G1_min VERIFIED,
G2_corr VERIFIED, H1_plus VERIFIED-WITH-AMENDMENTS, H2_uniform VERIFIED-WITH-AMENDMENTS. Lead: Claude Opus 5.5.

| finding | severity | disposition | where |
|---|---|---|---|
| K1-1 changelog v1.1 not wholly EQUAL (row-wise KL reading restricted to deterministic α) | MINOR | ACCEPT; row split: v1.1a WEAKER (interpretive sentence, no display changed, not a target-clause display; reported at CP3 per v4 §4.2), v1.1b EQUAL; K1 is the statement-change check of both | STATEMENT §10 |
| K1-2 "n ≥ 5" false for √(log n/n) ≤ ½ | MINOR | ACCEPT; n ≥ 9 with the reason | `lemmas/H1_plus.md` H1.2 [K1-2] |
| K1-3 support-dependent event not continuous on the p-stratum | NIT | ACCEPT; finer strata {p = p′, supp β = T} | `lemmas/H2_uniform.md` H2.0(ii) [K1-3] |
| G2 reading note: "κ_n = (X, …)" on line 18 means the raw matrix | — (note) | ERRATA E1 (editorial; not applied, to keep the checked G2 unchanged) | `ERRATA.md` |
| Scope 2: v1.2 [LA-1] NEW-CLAIM | — | confirmed; clause (G) correct as stated and proved | STATEMENT §10 |

Repairs to H1, H2 → DEPS rows L:H1_plus, L:H2_uniform STALE → re-check K2 (new Sol agent) on the repair diff
`K2_repair_diff.txt` and the STALE rows (RIDER_RULES §3.3).

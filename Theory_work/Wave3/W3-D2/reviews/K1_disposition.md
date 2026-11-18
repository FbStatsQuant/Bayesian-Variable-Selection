# W3-D2 — K1 disposition (lead, 2026-11-17)

Reply: `reviews/K1_linecheck_opus.md` (Opus 5.5 high, Claude Third, fresh, blind; per the ticket's check plan): P0 VERIFIED,
P1 VERIFIED-WITH-AMENDMENTS, P2 VERIFIED, P3 VERIFIED-WITH-AMENDMENTS; 0 C, 1 S, 2 F, 1 E. All accepted; PROOF v1.1
(diff `reviews/K1_repair.diff`). No step changed; no statement clause changed.

| finding | tag | disposition |
|---|---|---|
| K1-1 floor available only for n ≥ max(3, 2s₀): say why applying the master to eventually-true hypotheses is legitimate | S | ACCEPT: sentence added at the end of P1 (bounds at n concern the n-th law; master's proof checks membership n by n) |
| K1-2 B4.1's domain list omits p ≤ n^A (used in B1.3) | F | ACCEPT: added "p ≤ n^A ((A1); [R1] `:25`)" |
| K1-3 attributions of determinism (P3 NOTATION cite; P1 σ²; P4 "no condition on α") | F | ACCEPT: wording per the reviewer's fixes |
| K1-4 [MISR] `:20-22` → `:21-22` | E | ACCEPT |

Re-check: K2, new Opus agent (finder's family), on `reviews/K1_repair.diff` and the STATEMENT v1.1 → v1.2 diff
(`reviews/STATEMENT_v1.1_to_v1.2.diff`: §0 posterior gloss and §7 caveats, both EQUAL; the §0 edit landed while K1 ran).

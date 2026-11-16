# Council R1 disposition (MANIFEST fadb67e8cceacbceaf7b226925155c5817aa5915b4f333542e3aef7bfba8a994)

Seats (NORMAL mode, fresh, blind): Sol (OpenAI seat) `R1_council_sol.md` — 4/4 ACCEPT, score 7.8, gates=FAIL (strength,
faithful, sweep, reader); Opus 5.5 (Claude seat) `R1_council_opus.md` — 4/4 ACCEPT, score 8.5, gates=FAIL (faithful, sweep,
reader). No C finding; all blocking items are F (Sol F1, F3 also counted under strength) in derived texts (READER_DELTA,
REPORT registry blocks). No STATEMENT, lemma or DEPS row changes, so the changelog has no new row and DEPS stays 10/10 OK.
Lead: Claude Opus 5.5. → Diff round R2 (PROTOCOL_v4 §5.5).

| finding | seat(s) | tag | disposition | where |
|---|---|---|---|---|
| "(A0) necessary and sufficient" — necessity is proved only for the contrast condition | Sol 1, Opus F1 | F (S) | ACCEPT: (A0) called a sufficient form; the weaker contrast condition stated; equivalence only as CorG-min (a)+(c) | READER_DELTA §3 (A0) |
| reference law must be centred | Opus F2 | F | ACCEPT: "around this law, with its mean centred over the sample (the fitted mean carries no intercept)"; B4.4 cites STATEMENT §1 | READER_DELTA §2 Remark; §4 B4.4 |
| selection premise weakened; uniformity needs (UP) | Sol 3, Opus F3 | F (S) | ACCEPT: "posterior mass of S₀ tends to one in probability"; uniform "over any class … on which this convergence is uniform"; B4.4 names (UP) | READER_DELTA §2 Remark; §4 B4.4 |
| Example uses Σ_𝒞𝒞⁻¹ without invertibility | Sol 2 (F), Opus E5 (E) | F | ACCEPT: example states Σ_𝒞𝒞 invertible, Moore–Penrose otherwise; iid noise rows in the linear-plus-noise sentence; B4.1 "for all large n" | READER_DELTA §2, §4 B4.1 |
| registry assumption lists omit (N), population energy/beta-min, and (G)'s hypotheses | Opus F4 | F | ACCEPT: CorGb-plus adds A:MISR-OVC and new A:MISR-POP-SNR; CorH-U adds the (G) ids with "(G) only" in its conclusion | REPORT :52, :68, conclusion of CorH-U |
| fixed-design-version sentence has no master | Opus E6 | E | APPLIED (same file): B4.4 names W3-MISR:MIS(i)@1.0.0 | READER_DELTA §4 |
| REPORT record details (premises, depends_on, garbled line) | Opus E3 | E | APPLIED (same file) except the "pointer only" prose → ERRATA E6 | REPORT :15, :42, :62, :66 |
| DEPS uses incomplete; DOWNSTREAM not transitive | Opus E4 | E | APPLIED: uses lists completed; fixed-point propagation in deps_hand.py (states unchanged: all OK) | deps_hand.py, DEPS.tsv |
| (OV) ⇒ (OV^c) needs σ²+τ² > 0 | Opus E1 | E | ERRATA E2 (STATEMENT/lemma untouched to keep them checked) | ERRATA.md |
| (E3) "is" → "gives" | Opus E2 | E | ERRATA E3 | ERRATA.md |
| (G) conditional list conservative | Opus E7 | E | ERRATA E4 | ERRATA.md |
| §8 implies-row and the restricted KL reading | Opus E8 | E | ERRATA E5 | ERRATA.md |
| G2:18 raw-design notation | Sol 4 | E | already ERRATA E1 | ERRATA.md |

**Better-theorem proposals (Opus §4; for HQ, not findings):** (P1) clause (G) in the no-beta-min (b) form (G2 steps 1–3, 5
put κ_n in 𝒦⁰_n; (RD) + (U-b) give log n/n contraction for Gaussian candidate rows without beta-min); (P2) CorGb-plus in the
conditional form E[δ_n | X_𝒞] ≤ C r_n on 𝒜_n (from MIS-R (ii)(a)); (P3) CorG-min (d): with Σ_ε = σ²I_N it returns (OV^c)
exactly. Disposition: named open items for HQ (P1 is cheap and could be a future rider; not adopted here, since a new clause
would need a change check and a re-round after the cut-off planning).
Staged ingest after the fixes (and after merging origin/main): 4 claims, 0 problems, 0 acceptance ERROR (the stale accept
records on W3-MISR parents no longer appear on current main).

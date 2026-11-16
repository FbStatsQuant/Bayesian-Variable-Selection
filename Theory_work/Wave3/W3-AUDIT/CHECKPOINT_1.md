# W3-AUDIT — CHECKPOINT 1 (step 1, assumptions; audit Fable, 2026-11-16) — waiting for the manager's go

1. **FLAG — one assumption is narrow (not false): "no leakage", Thm 10 (A5), row 3.6** (`TRACK_B.md` B11). It asks every null to be uncorrelated with every truth up to C n^{-1/2}. Inside: S1, IND. Outside: S2–S6 of the 2,400-fit study, all of P6, and AR (the primary 1M design) and BLK. On those designs the printed PIPs, MPM and Ẑ have no theorem; Thm 6 (reported model) and row 3.5 (unbiased Ẑ) still hold. SUSPECT/NARROW route is the manager's call; no recorded statement was touched.
2. **Done.** `AUDIT.md` (one table per core theorem; track-A check; method version per study) and `TRACK_B.md` (12 dossiers, summary table), every Song–Liang line cited to the paper (pp. 950–959). Supplement (Theorem S, proofs) not inspected.
3. **Track B result.** Core 1 and core 2 (posterior): assumptions same as or comparable to Song–Liang; **all** our designs are inside, strong factors included (no upper eigenvalue bound is used). Stronger than Song–Liang only: range of p (B2), a c/n collinearity floor (B6), row law (B7). Core 3 adds visibility (stronger than their Condition 5) and a leakage set (their remark (a), p. 958): S5, P6 and FAC are outside, as expected.
4. **Track A.** The helper's inventory is right on classification and statuses. Four corrections (`AUDIT.md` §6): two buckets read above their quoted labels; P-START and NC_r are closed only under (A5); drift D2 resolved (Cor 9C uses only DIST-C's deterministic clauses, so row 2.1 does not carry the sampler contract); the frozen-run identities T12 ("PROVED-LOCKED") were not listed.
5. **Open gaps.** The 13 items, ordered in the annex. Rows 1.x and 2.1 have none. Extra open claims X1–X5: T12 label, Prop-LB, Lemma 1a′, the Cor-C edge, PoolZ.
6. **Method versions.** Engineering's report is confirmed for the 2,400-fit study (v2.2.1, no LS0, memory-only preflight) and **not confirmed for P6** (v3.1 at main 2252d57, LS0 on with the wide cap, `W3-P6/scripts/p6_fit.R:55`). Rerun recommendation: partial (post-hoc LS0 only, no sampler rerun), and only if the paper reports the printed model.
7. **Map against paper.** No disagreement found between `SONG_LIANG_MAP.md` and the paper. Three passages I use are not in the map: the sufficient forms of Condition 3 (pp. 955–956), the ridge prior example c_n ∝ 1/n (p. 953), remark (a) (p. 958).
8. **Disagreement with the helper:** do not drop Thm TR from row 3.6; it is the only recorded route past (A5).
9. **Not done:** track C results are not cited (not landed); `[audit calc]` lines in `TRACK_B.md` are unchecked.
10. **Needed from the manager:** the go for track D; a ruling on item 1 (narrow row 3.6's wording now, or a repair ticket: "leaks inside a method block are harmless", `TRACK_B.md` B11); whether X1–X5 join the Tier B queue.

## Annex — Tier B order of the 13 track-A items (item → core row blocked → smallest lemma; full statements in `AUDIT.md` §6)

| Order | Item | Blocks | Smallest lemma |
|---|---|---|---|
| 1 | GUARD-W (missing) | 3.1, 3.5, 3.6 | GW: guards read only the clock; an unstopped run equals the potential run; a stopped run returns no estimates |
| 2 | Blocks ≤ 16 (missing, partial) | 3.1, 3.6 | BLK: the partition is a function of X; every block ≤ min(⌊√n⌋, ⌊√p⌋, 16) |
| 3 | OP-LS0 (unchecked) | 3.1 | OPC: LS0 runs from the returned start mode with complete scans; its models enter the final comparison |
| 4 | Start-table encoding (unchecked) | 3.1 | ENC: tables and index maps are built as Lemma E4 assumes |
| 5 | CAL (missing) | 3.5, 3.6 | CAL-C: the calibration record depends on the data and streams 0–9 only |
| 6 | START (unchecked) | 3.5, 3.6 | START-X: the start sampler is exact and its normaliser is exact |
| 7 | KERNEL (unchecked) | 3.5, 3.6 | KER: each coded move is π_φ-reversible; the order is uniform and state-independent |
| 8 | P-OVL (missing, one line) | 3.6 (Thm D clause) | OVL: D_r·π₀(S₀) → ∞ from the production budget and P-START |
| 9 | Start-mode DP implementation (unchecked) | 3.1, delivery clause | TDP: the DP returns the lexicographically first maximiser within its stated cost |
| 10 | P1 inventory, case S.3 (read only) | 3.1, delivery clause | second-seat code reading |
| 11 | P-OVL∞ (missing) | 3.6, remark route only | not Tier B (needs a key lemma); keep as a named open premise; track-D candidate |
| 12, 13 | SCORE-EXP, START-CENTRE (unchecked, route only) | none | no ticket; record that the core rows do not use them |

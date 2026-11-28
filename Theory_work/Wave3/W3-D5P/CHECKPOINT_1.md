# W3-D5P — CHECKPOINT_1 (statement lock; 2026-11-17)
1. STATEMENT v1.0 LOCKED: SL1 (Sol gpt-6.1-sol high) LOCK WITH CHANGES, 3 findings (1 MAJOR, 2 MINOR) all accepted and applied (`reviews/SL1_*`); changelog row v1.0 EQUAL.
2. Claims: LIST-K (deterministic list algebra), LIST-CODE (code reading at core 4676af6 = main 029bb748; closes both DIST links :297-303: completed = output on the sampler branch; `hpm` = Ŝ⁺; S₀ ∈ `top_store`), LIST-R (Thm 6 designs incl. AR/BLK: on 𝒢⁺_n every output run has S₀ in its list, `hpm` = S₀, PIP errors ≤ 1 − π(S₀|y) vs truth and exact PIP, π(S₀|y)Z ≤ Z_list ≤ Z, `mpm_list` = S₀ if 1 − π(S₀|y) < ½; O_P(√(log n/n)) for p ≥ 2; unconditional under (D)).
3. Target clauses T1–T3 (TARGET.md). No hypothesis beyond Theorem 6; `log_Z_list` kept. Named premise IMPL-LIST (method commit pending; code-read when it lands).
4. Tags: row 3.1 STRONGER (added conclusions, same hypotheses and event); rows 3.6, 3.5 NEW-CLAIM (different outputs; both rows unchanged). READER_DELTA draft: "Corollary 6L"; placement for HQ.
5. Numerics (falsification): LIST-K 20 000 random cases, 0 violations; real core, 27 small AR cases vs exact enumeration: S₀ ∈ top_store 27/27, all bounds hold.
6. Route: corollary works, no new key lemma (SL1 concurs). Plan ≈ 10 h lead + reviews: L1–L3 proofs → blind Opus line check → citecheck → council (Sol + Opus) → CP3 + card text + API blind-audit card.
7. HOLDS.md (origin/main): no hold on a consumed claim. Kill clock: started 12:38 CST 11-17 (3 d).
8. Asks: GO for proofs; HQ placement of the card text can wait for CP3.

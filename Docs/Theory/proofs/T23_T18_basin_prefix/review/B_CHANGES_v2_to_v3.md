# Changes from PROOF_v2 to PROOF_v3 (after Stage B round 2)

Both reviewers ruled PROOF_v2 verified. They agreed with all six v1→v2 changes and raised no fatal or gap finding. Their remaining points were all exposition-level; the lead accepted all of them. No change to the statement, the hypotheses, the conclusions or the constants.

| Round-2 finding | Lead's judgment | Change in PROOF_v3 |
|---|---|---|
| Opus F1: 𝓕_s ⊆ 𝒢_τ assumes population-level round processing and time-ordered consumption; the sub-stream case is asserted, not shown | Accepted | §2 rewritten. (i) Per-particle σ-fields 𝓕ⁱ_s = all variates of island r drawn before particle i's round s+1 begins; increasing in s, with X_{i,0..s} measurable. (ii) EX-S is stated in the form used, (F): each random choice (a round's order, or one step's outcome) has, given everything drawn before it, the law the method prescribes from the current state. This is independent of processing order and sub-stream layout. (iii) Lemma 1 is proved from (F) by conditioning step by step through the round (tower property on finite spaces), with no stopping-time construction. The q-round version is proved by induction. §4 conditions on 𝓕ⁱ_s; the ranges are checked in the text ((l−1)r₀ ≤ L+3, lr₀ ≤ L+4). |
| Opus F2 / Astra #2: method details credited to STATEMENT.md but not in it (π₀ construction, "block size B", neighbour graph, backward sampler) | Accepted | All removed. §2 cites only STATEMENT §1: one round, one kernel K₁, fixed by the data and 𝓒, for all terminal rounds. B appears only as the number of neighbour swaps. |
| Opus F3: "stream r" mislabel | Accepted | Now "island r's streams are among 10–13". |
| Opus F4: P vs P_𝓒; τ < ∞ a.s. | Accepted | §2 opens "𝓒 is fixed … all probabilities are P_𝓒". The stopping time is gone. |
| Opus F5: clipped display | Accepted | That display is gone. Three wide displays (§1 PIP̂/B̄ definitions, §4 E₂/E₃ bounds, Theorem (c)) are split across lines; pdflatex reports no overfull boxes. |
| Opus F6: stray comma after Lemma 2's display; EX-A inconsistently listed for Theorem (a) | Accepted | Comma replaced by a period and the blank line removed. Theorem (a) now reads "Under EX-A, on every realisation …"; the "part of the setting" wording is removed. |

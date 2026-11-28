# Track A lemmas — CHECKPOINT 1 (after T1 GW + T2 BLK; lead Opus 5.5; 2026-11-16 17:06 CST) — waiting for the manager's go
1. **T1 GW (GUARD-W) proved**, code of record 4676af6: every check (2 preflights, 7 guard sites) only stops; a fired check gives no estimates; on 𝒪 the run equals the potential run P°; plus (GW-iv) 𝒜 = 𝒜° ∩ G ⊆ 𝒜°, 𝒪 ⊆ 𝒪°, and (GW-v) "complete scans" discharged. Lean: no.
2. **T2 BLK proved**: B = min(⌊√n⌋, ⌊√p⌋, 16) ≤ min(16, K); blocks partition [p], each ≤ B; a Borel function of the correlation matrix only (not y, no stream). Lean: yes for the cut-and-pack invariant.
3. **Checks (Claude only, Codex untouched):** LC1 (blind Opus) → LC1r → LC1r2 (new Opus agents): all VERIFIED WITH AMENDMENTS; 31 findings, 1 C (a mis-scoped event in a new clause, fixed), none a failing step; all applied; citecheck 0 MISS. Files: `T1_GW/`, `T2_BLK/`, `reviews/`.
4. **Labels:** both "PROVED; Claude LC verified" — not PROVED-CHECKED until the OpenAI reads (PROTOCOL_v4 §2A: Sol lock, Sol line check, OpenAI seat).
5. **F flag for HQ (no edit made):** W3-SAMP's "𝒜 ∈ σ(𝓒)" holds only for the potential pair (𝒜°, 𝓒°), since the real 𝒜 depends on the clock. Read W3-SAMP with 𝒜° throughout; conclusions transfer (𝒜 ⊆ 𝒜°), but premises written with 1_𝒜 (P-START, proved only under (A5); P-OVL) must hold with 1_𝒜°. I will check that in T8 (OVL). Detail: `T1_GW/CHECK.md`.
6. **Recorder notes:** `A:BLOCK-LE-16`'s registry source line is stale (C-GROW `:61` → `:65-67`); code comment `cpp/v3_core.cpp:144` says B ≤ 20, the code enforces 16.
7. **Gate ask (Codex):** one Sol read now, covering the lock and line check of T1 + T2 together; council seats later, as one batch for T1–T10. Alternative: hold all Codex until T10.
8. **HQ ruling needed:** skip the better-theorem review for code lemmas with no CP1 target (T1, T2, and later T3–T5, T10)?
9. **Next on go:** T3 OPC → T4 ENC → T5 CAL-C → T6–T10, then CHECKPOINT_2. Kill budgets untouched; 3 subagents used, one at a time.

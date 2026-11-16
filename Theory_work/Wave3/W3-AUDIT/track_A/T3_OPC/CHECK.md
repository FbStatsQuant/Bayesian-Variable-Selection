# T3 · OPC (OP-LS0) — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Claude line check VERIFIED WITH AMENDMENTS (all applied); OpenAI layers pending
(council batch T1–T10).** Not "PROVED-CHECKED" (needs the Sol lock, a Sol line check and the OpenAI council seat).
Blocks row(s): 3.1.

Frozen text (sha256, first 12 hex, 2026-11-16 17:54 CST): STATEMENT `fd198cacd783`, PROOF `e529e69c62d5`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

**What it says.** On every completed sampler run, LS0 runs once from the coded start mode with cap ℓ_n + |S̃₀|, reads no uniform, is not interrupted, is the abstract search LS, and all its models reach the ledger; hence 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ (RM-0 (b)), the exact branch included. Re-check of `W1-GEN:L5` [OP]: correct at the pin; its note "LS0 is not in production code" is stale.

| Tier B step (PROTOCOL_v4 §3, step 4 omitted) | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **pending (gate)** | — |
| 2 better-theorem review | — | skipped (HQ 11-16, RIDER_RULES) | — |
| 3 line check | Sol (NORMAL); Claude stand-in | Claude: LC2 → LC4; no C/F finding open | `../reviews/LC2_*`, `LC3_*`, `LC4_*` |
| statement-change check (§4.2), rows not EQUAL | Sol, new agent | **pending (gate)**; v2 (OPC-d) enumeration branch STRONGER | STATEMENT changelog |
| 6 citation check | script | **0 MISS** (76 citations) | `CITECHECK.txt` |
| 7 council R1 | Sol + Opus, blind | **pending (batch T1–T10)** | — |



Lean target: **no**.

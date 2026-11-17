# T9 · TDP (start-mode DP) — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Claude line check VERIFIED WITH AMENDMENTS (all applied); OpenAI layers pending
(council batch T1–T10).** Not "PROVED-CHECKED" (needs the Sol lock, a Sol line check and the OpenAI council seat).
Blocks row(s): 3.1 delivery.

Frozen text (sha256, first 12 hex, 2026-11-16 18:17 CST, as frozen for the R1 diff round R1d): STATEMENT `ec3da65edd35`, PROOF `8eec9e60ec2b`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

**What it says.** `start_mode(st, cap ≥ 2, true)` returns lex_min E = S* (E = 𝒜* proved directly at the pin), the root check never fails (TDP-e), and the fallback and the fast path fit TDP-IMPL's operation and storage bounds (fast path with an explicit factor 10⁶). Re-check of `C-ENG:TDP_E`: mathematics correct; its claim (4) holds only for cap ≥ 2 at the pin; its line numbers are stale.

| Tier B step (PROTOCOL_v4 §3, step 4 omitted) | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **pending (gate)** | — |
| 2 better-theorem review | — | skipped (HQ 11-16, RIDER_RULES; premise-closer) | — |
| 3 line check | Sol (NORMAL); Claude stand-in | Claude: LC3 → LC4; no C/F finding open | `../reviews/LC2_*`, `LC3_*`, `LC4_*` |
| statement-change check (§4.2), rows not EQUAL | Sol, new agent | **pending (gate)**; v1.1 (TDP-e), v2 fast-path cost, v2.1 envelope — STRONGER | STATEMENT changelog |
| 6 citation check | script | **0 MISS** (35 citations) | `CITECHECK.txt` |
| 7 council R1 | Sol + Opus, blind | R1 (`../reviews/MANIFEST_R1.txt`): Sol REJECT (repaired), Opus ACCEPT; diff round R1d (`../reviews/MANIFEST_R1d.txt`); outcome in `../reviews/` and `../CHECKPOINT_3.md` | — |



Lean target: **yes**.

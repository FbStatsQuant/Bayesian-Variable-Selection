# T9 · TDP (start-mode DP) — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Claude line check VERIFIED WITH AMENDMENTS (all applied); OpenAI layers pending
(council batch T1–T10).** Not "PROVED-CHECKED" (needs the Sol lock, a Sol line check and the OpenAI council seat).
Blocks row(s): 3.1 delivery.

Frozen text (sha256, first 12 hex, 2026-11-16 17:54 CST): STATEMENT `5b51c977ec74`, PROOF `1d1c05e0bd00`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

**What it says.** `start_mode(st, cap ≥ 2, true)` returns lex_min E = S* (E = 𝒜* proved directly at the pin), the root check never fails (TDP-e), and the fallback and the fast path fit TDP-IMPL's operation and storage bounds (fast path with an explicit factor 10⁶). Re-check of `C-ENG:TDP_E`: mathematics correct; its claim (4) holds only for cap ≥ 2 at the pin; its line numbers are stale.

| Tier B step (PROTOCOL_v4 §3, step 4 omitted) | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **pending (gate)** | — |
| 2 better-theorem review | — | **placeholder: not covered by HQ's 11-16 skip ruling (T1–T5, T10 only); HQ ruling pending; not run** | — |
| 3 line check | Sol (NORMAL); Claude stand-in | Claude: LC3 → LC4; no C/F finding open | `../reviews/LC2_*`, `LC3_*`, `LC4_*` |
| statement-change check (§4.2), rows not EQUAL | Sol, new agent | **pending (gate)**; v1.1 (TDP-e), v2 fast-path cost, v2.1 envelope — STRONGER | STATEMENT changelog |
| 6 citation check | script | **0 MISS** (35 citations) | `CITECHECK.txt` |
| 7 council R1 | Sol + Opus, blind | **pending (batch T1–T10)** | — |



Lean target: **yes**.

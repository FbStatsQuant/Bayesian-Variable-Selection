# T7 · KER (kernels, order) — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Claude line check VERIFIED (after amendments); OpenAI layers pending
(council batch T1–T10).** Not "PROVED-CHECKED" (needs the Sol lock, a Sol line check and the OpenAI council seat).
Blocks row(s): 3.5, 3.6.

Frozen text (sha256, first 12 hex, 2026-11-16 18:00 CST, as frozen for council R1): STATEMENT `405e91d724a6`, PROOF `df6cdba57761`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

**What it says.** Each coded move is the T12 §1 kernel and is γ_φ-reversible; the round order is a uniform Fisher–Yates permutation drawn before any step (re-check of N9 rows 1–5; no error in N9).

| Tier B step (PROTOCOL_v4 §3, step 4 omitted) | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **pending (gate)** | — |
| 2 better-theorem review | — | **placeholder: not covered by HQ's 11-16 skip ruling (T1–T5, T10 only); HQ ruling pending; not run** | — |
| 3 line check | Sol (NORMAL); Claude stand-in | Claude: LC3 → LC4 (VERIFIED); no C/F finding open | `../reviews/LC2_*`, `LC3_*`, `LC4_*` |
| statement-change check (§4.2), rows not EQUAL | Sol, new agent | **pending (gate)**; none beyond wording | STATEMENT changelog |
| 6 citation check | script | **0 MISS** (51 citations) | `CITECHECK.txt` |
| 7 council R1 | Sol + Opus, blind | batch T1–T10, manifest `../reviews/MANIFEST_R1.txt`; outcome recorded in `../reviews/` and `../CHECKPOINT_3.md` (this file is frozen in the manifest) | — |



Lean target: **yes for (KER-b); no for the code correspondence**.

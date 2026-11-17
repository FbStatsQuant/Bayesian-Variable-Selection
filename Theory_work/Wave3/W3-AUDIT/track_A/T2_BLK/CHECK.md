# T2 · Lemma BLK — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Claude line check VERIFIED WITH AMENDMENTS (all applied); OpenAI layers pending at the
gate.** Not "PROVED-CHECKED" (needs the Sol lock, a Sol line check and the OpenAI council seat).

Frozen text (sha256, first 12 hex, 2026-11-16 18:17 CST, as frozen for the R1 diff round R1d): STATEMENT `2bc68097d046`, PROOF `59bb28806ce0`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

| Tier B step (PROTOCOL_v4 §3, step 4 omitted) | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **LOCK WITH CHANGES** (Sol, 11-16), changes applied (v5) | `../reviews/SL1LC2_reply_sol.md`, `SL1LC2_disposition.md` |
| 2 better-theorem review | — | skipped (HQ 11-16, RIDER_RULES) | — |
| 3 line check | Sol (NORMAL); Codex held for the gate | Claude stand-in done: LC1 (Opus, blind) → LC1r → LC1r2, all **VERIFIED WITH AMENDMENTS**; no C/F finding open | `../reviews/LC1_*`, `LC1r_*`, `LC1r2_*` |
| 3 line check (Sol) | Sol | **VERIFIED WITH AMENDMENTS** (Sol, 11-16), amendments applied; no C | `../reviews/SL1LC2_reply_sol.md` |
| statement-change check (§4.2) | Sol, new agent | **pending (gate)**; rows: v2 (BLK-c) setting R STRONGER; v4 setting-R premise STRONGER, (BLK-c) σ(X^r) wording WEAKER | STATEMENT changelog |
| 6 citation check | script | **0 MISS** (81 citations) | `CITECHECK.txt` |
| 7 council R1 | Sol + Opus, blind | R1 (`../reviews/MANIFEST_R1.txt`): Sol REJECT (repaired), Opus ACCEPT; diff round R1d (`../reviews/MANIFEST_R1d.txt`); outcome in `../reviews/` and `../CHECKPOINT_3.md` | — |

All three checkers found (BLK-a)–(BLK-c) correct from the first read; the amendments concern the setting (partition map
defined for every X; setting R premise: i.i.d. rows, atomless coordinate marginals, ε independent of the rows), the
binary64 remark (now proved) and the downstream list.

**Recorder notes (no edit made):** the registry source of `A:BLOCK-LE-16` points to `C-GROW/STATEMENT.md` line 61; the
definition is at `:65-67`. Code comment `cpp/v3_core.cpp:144` says "1 <= B <= 20"; enforced limit is 16 (`:145-146`) —
an Engineering note, not a lemma issue.

Lean target: **yes** for (BLK-b) — "cut a full binary tree on p leaves at size ≤ B (B ≥ 1), then next-fit pack whole
clusters into bins of capacity B: the bins partition the leaves, are nonempty and have size ≤ B" (finite, structural).
No for the code correspondence.

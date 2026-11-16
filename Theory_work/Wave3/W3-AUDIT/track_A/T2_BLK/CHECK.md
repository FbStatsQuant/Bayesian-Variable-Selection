# T2 · Lemma BLK — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Claude line check VERIFIED WITH AMENDMENTS (all applied); OpenAI layers pending at the
gate.** Not "PROVED-CHECKED" (needs the Sol lock, a Sol line check and the OpenAI council seat).

Frozen text (sha256, first 12 hex, 2026-11-16 17:04 CST): STATEMENT v4 `ad63feb31ebb`, PROOF v4 `6d2be5ad58d2`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

| Tier B step (PROTOCOL_v4 §3, step 4 omitted) | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **pending (gate)** | — |
| 2 better-theorem review | code lemma, no CP1 target; lead proposes to skip, HQ to rule | **HQ ruling** | — |
| 3 line check | Sol (NORMAL); Codex held for the gate | Claude stand-in done: LC1 (Opus, blind) → LC1r → LC1r2, all **VERIFIED WITH AMENDMENTS**; no C/F finding open | `../reviews/LC1_*`, `LC1r_*`, `LC1r2_*` |
| statement-change check (§4.2) | Sol, new agent | **pending (gate)**; rows: v2 (BLK-c) setting R STRONGER; v4 setting-R premise STRONGER, (BLK-c) σ(X^r) wording WEAKER | STATEMENT changelog |
| 6 citation check | script | **0 MISS** (81 citations) | `CITECHECK.txt` |
| 7 council R1 | Sol + Opus, blind | **pending (gate)** | — |

All three checkers found (BLK-a)–(BLK-c) correct from the first read; the amendments concern the setting (partition map
defined for every X; setting R premise: i.i.d. rows, atomless coordinate marginals, ε independent of the rows), the
binary64 remark (now proved) and the downstream list.

**Recorder notes (no edit made):** the registry source of `A:BLOCK-LE-16` points to `C-GROW/STATEMENT.md` line 61; the
definition is at `:65-67`. Code comment `cpp/v3_core.cpp:144` says "1 <= B <= 20"; enforced limit is 16 (`:145-146`) —
an Engineering note, not a lemma issue.

Lean target: **yes** for (BLK-b) — "cut a full binary tree on p leaves at size ≤ B (B ≥ 1), then next-fit pack whole
clusters into bins of capacity B: the bins partition the leaves, are nonempty and have size ≤ B" (finite, structural).
No for the code correspondence.

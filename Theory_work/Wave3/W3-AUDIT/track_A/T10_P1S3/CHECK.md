# T10 · Re-audit P1/S.3 — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Claude line check VERIFIED WITH AMENDMENTS (all applied); OpenAI layers pending
(council batch T1–T10).** Not "PROVED-CHECKED" (needs the Sol lock, a Sol line check and the OpenAI council seat).
Blocks row(s): 3.1 delivery.

Frozen text (sha256, first 12 hex, 2026-11-16 18:00 CST, as frozen for council R1): STATEMENT `bb7c8461da1e`, PROOF `105cccd101ef`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

**What it says.** Every no-output exit of the shipped fit maps to an INVENTORY row at re-located pin lines; new X9 (start_mode throws, unreachable) and X10 (coded LS0 guard); get_holder and the class of implicit errors unreachable; **D1 (`schedule_limit`) is unreachable on the shipped path** (tier-1 fallback; consistent with C-DLV:Prop-F); X7/X8 cannot fire for inputs R represents.

| Tier B step (PROTOCOL_v4 §3, step 4 omitted) | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **pending (gate)** | — |
| 2 better-theorem review | — | skipped (HQ 11-16, RIDER_RULES) | — |
| 3 line check | Sol (NORMAL); Claude stand-in | Claude: LC2 → LC4; no C/F finding open | `../reviews/LC2_*`, `LC3_*`, `LC4_*` |
| statement-change check (§4.2), rows not EQUAL | Sol, new agent | **pending (gate)**; v2/v2.1 STRONGER (more sites covered) | STATEMENT changelog |
| 6 citation check | script | **0 MISS** (176 citations) | `CITECHECK.txt` |
| 7 council R1 | Sol + Opus, blind | batch T1–T10, manifest `../reviews/MANIFEST_R1.txt`; outcome recorded in `../reviews/` and `../CHECKPOINT_3.md` (this file is frozen in the manifest) | — |

**Recorder notes:** INVENTORY/S.3 line numbers predate LS0; the INVENTORY summary "D1 … the only random no-output path" predates the fallback; the X7/X8 erratum should add that both are dead for R-representable inputs.

Lean target: **no**.

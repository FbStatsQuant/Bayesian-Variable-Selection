# T8 · OVL (P-OVL) — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Claude line check VERIFIED WITH AMENDMENTS (all applied); OpenAI layers pending
(council batch T1–T10).** Not "PROVED-CHECKED" (needs the Sol lock, a Sol line check and the OpenAI council seat).
Blocks row(s): 3.6 (Thm D).

Frozen text (sha256, first 12 hex, 2026-11-16 18:18 CST, as frozen for the R1 diff round R1d): STATEMENT `f03afc297221`, PROOF `d8fa0b36fde8`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

**What it says.** On 𝒜°, D_r ≥ max(2500, n, p)(L + 6) ≥ 10n; P-START on 𝒜° ⇒ P-OVL on 𝒜° (and on 𝒜). **Proved only under IF-START's hypotheses, in particular (A5)**; without (A5) the checked `W3-START2-R:OVL` route gives P-OVL's production form under its own hypotheses.

| Tier B step (PROTOCOL_v4 §3, step 4 omitted) | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **pending (gate)** | — |
| 2 better-theorem review | — | skipped (HQ 11-16, RIDER_RULES; premise-closer) | — |
| 3 line check | Sol (NORMAL); Claude stand-in | Claude: LC3 → LC4; no C/F finding open | `../reviews/LC2_*`, `LC3_*`, `LC4_*` |
| statement-change check (§4.2), rows not EQUAL | Sol, new agent | **pending (gate)**; none | STATEMENT changelog |
| 6 citation check | script | **0 MISS** (18 citations) | `CITECHECK.txt` |
| 7 council R1 | Sol + Opus, blind | R1 (`../reviews/MANIFEST_R1.txt`): Sol REJECT (repaired), Opus ACCEPT; diff round R1d (`../reviews/MANIFEST_R1d.txt`); outcome in `../reviews/` and `../CHECKPOINT_3.md` | — |

**Flag (where it bites), HQ check (c) 11-16 — done, no failure:** (OVL-d) P-START holds with 1_𝒜° (IF-START's proof is 0 ≤ 1_𝒜o₀ ≤ o₀ = O_P(r_n) for any event; o₀ depends on (X, y) only), and P-OVL holds with 𝒜° ((OVL-b) with the uninterrupted run's budget; without (A5) via the event-free OVL route). (OVL-d) added after LC4; it has had no Claude read and goes to the council batch.

Lean target: **yes**.

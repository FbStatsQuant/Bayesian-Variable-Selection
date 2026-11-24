# T12-RELABEL: draft carrier for `SOP:TH110` (T12), for the recorder (DRAFT, coordinator; nothing here is recorded)

Requested by the manager (HQ ruling: the owner ADOPTED T12 on 2026-11-18). Closes walk finding T9 H1. Recorder item; I patch nothing. Written against `origin/main` 802317c1 (`Theory_work/INFRA/registry/claims.tsv:12`). The layout follows the precedent `W3-POST:Prop-LB` (HQ-written carrier `Theory_work/Wave3/W3-POST/CHECKPOINT_2.md`, relabel event `correct-status`, events.log line 2996, commit 33bfcb9c).

## 1. Registry row today (verbatim from `claims.tsv:12`)
- id: `SOP:TH110`; alias `T12`; version `1.0.0`; kind `external`; ACTIVE; commit `dd60e09`
- name: `T12; T8; frozen-run evidence; recorded RB identities; JRSS-B Prop 2; THEORY.md row T12`
- short: `Frozen-run evidence and recorded-RB identities (old label T8)`
- file: `Theory_work/State_of_Project/registry/history.tsv`, lines `161-161`; sha256 `aa82f5d928c23b9423f5ceaa2dffd147e4d78af23f42f854c80aa8f6ab3af730`; `status_source`: `Theory_work/State_of_Project/registry/history.tsv:161`
- **status (verbatim):**
  `PROVED-LOCKED (all parts (i)-(iv), wave 1); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted]`

## 2. The review record, exactly as it appears in `claims.tsv:12` (the bracketed field of the status cell)
`[review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted]`
(Everything inside the brackets is quoted unchanged in the carrier below, except that the trailing clause `; not adopted` is dropped, because the owner has now adopted the result. The review record itself, i.e. who reviewed which stage and the verdict "correct", is not edited.)

## 3. Proposed new status string (what the carrier file must start with, verbatim, on its `status_source` line)
`PROVED-CHECKED (all parts (i)-(iv), wave 1; owner adoption 2026-11-18 + HQ carrier relabel, precedent Prop-LB) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra)]`
The label wording requested by the manager is kept as one clause: **"owner adoption 2026-11-18 + HQ carrier relabel, precedent Prop-LB"**. The phrase "all parts (i)-(iv)" is kept from the old status (the walk and the SAMP consumers cite T12 (i.a), (i.b), (i.c), (ii) and the invariance part).

## 4. Draft carrier file (HQ carrier, PROTOCOL_v4 §7; NOT a lead checkpoint). Suggested path: a new file the recorder chooses (e.g. `Theory_work/Wave3/W3-SAMP/CHECKPOINT_T12.md`); the `status_source` of the registry row is then `<that file>:<line of the status string>`, as `Theory_work/Wave3/W3-POST/CHECKPOINT_2.md:6` was for Prop-LB.

```
# CHECKPOINT_T12 — SOP:TH110 (T12): relabel to PROVED-CHECKED (HQ-written carrier, PROTOCOL_v4 §7; NOT a lead checkpoint)

Written by the HQ recorder (<recorder run id and date>), on the owner's adoption of T12 on 2026-11-18. Wave 1 reviewed T12 in full: the wave-1 review record is quoted verbatim from the registry row `SOP:TH110` (`Theory_work/INFRA/registry/claims.tsv`, status cell): [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted]. Its previous status was `PROVED-LOCKED (all parts (i)-(iv), wave 1); not adopted (adoption is Felipe's decision)`; the one thing that stopped it from being PROVED-CHECKED in the v4 vocabulary was the missing owner adoption, not a review finding. No proof text and no statement of T12 changes.

PROVED-CHECKED (all parts (i)-(iv), wave 1; owner adoption 2026-11-18 + HQ carrier relabel, precedent Prop-LB) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra)]
```
(The status string in the carrier must be the first text on its own line, so that `ingest.py`'s "each status must start verbatim on its status_source" holds; adjust the line number accordingly.)

## 5. Proposed `correct-status` event (events.log style, as for Prop-LB)
`<timestamp> HQ correct-status SOP:TH110 <old status> @ Theory_work/State_of_Project/registry/history.tsv:161 → <new status> @ <carrier file>:<line> — HQ GO real run (task T12-RELABEL, owner adoption 2026-11-18): relabel (legacy label PROVED-LOCKED, not adopted → v4 HQ carrier <carrier file>; precedent W3-POST:Prop-LB, events.log line 2996, commit 33bfcb9c); version 1.0.0 → 1.0.1 (a status change bumps the row version; see "Checkpoint re-point version bump" in the HQ rules)`
`notes` cell addition (as for Prop-LB): `RELABEL (HQ GO real run, owner adoption 2026-11-18): v4 HQ carrier <carrier file>; previous status "PROVED-LOCKED (all parts (i)-(iv), wave 1); not adopted (adoption is Felipe's decision) [review record: …; not adopted]"; the history.tsv row keeps its text, the registry governs`.

## 6. What the relabel does and does not do (facts for the recorder; nothing else is edited)
- **Closes walk finding T9 H1.** Row 3.6 (Thm 10) rests on `W3-SAMP:MR`, `ST` and `TR`, whose `depends_on` cite `SOP:TH110` (`MR`: "T12 (i.a),(i.b),(i.c),(ii)"; `ST`: "π-invariance of the elementary kernels (T12 invariance)"; `TR`: "T12 (R3)"). Those three statuses are already unconditional ("PROVED-CHECKED; council R1, MANIFEST 68480a72…, astra=9.1 PASS, opus=8.8 PASS") and **stay unchanged**; the relabel removes the one place where an input read "not adopted". Row 3.6 stays unconditional.
- **Cascade (recorder, citation-only):** claims whose `depends_on` edges name `SOP:TH110` get a re-pinned version quoted in their evidence; no status text of a consumer changes. Dependents seen in `claims.tsv` on 802317c1: `W3-SAMP:MR` (1.1.3), `W3-SAMP:ST` (2.1.3), `W3-SAMP:TR` (2.1.6), `W3-AUDIT-AX:FR` (T12 frozen-run identities) and, through them, `W3-READER` card rows quoting T12 (check `CLAIMS_CARD.md`). The recorder confirms the full list from the dependency graph.
- **Precedent mechanics (from `W3-POST:Prop-LB`, commit 33bfcb9c):** the registry `status` and `status_source` change; `council` is not needed (there is no new council; the old review record is quoted); the carrier is a new file; a requote of the card rows citing T12 follows; manifests that pinned the old status become CITATION-ONLY re-freezes.
- **Not done here:** nothing is recorded, nothing is edited in the registry, `history.tsv` or any ticket. This is a draft.

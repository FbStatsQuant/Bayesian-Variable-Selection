# Track A lemmas — CHECKPOINT 2 (after T3–T10 and their re-checks; lead Opus 5.5; 2026-11-16 17:56 CST) — waiting for the manager's go
1. **T3–T10 all proved** at code pin 4676af6 (OPC, ENC, CAL-C, START-X, KER, OVL, TDP, P1/S.3 re-audit); STATEMENT/PROOF/CHECK.md in each folder; citecheck 0 MISS. Lean: T6, T7 (math half), T8, T9 yes; T3, T4, T5, T10 no.
2. **Checks (Claude only):** LC2 (T3, T4, T5, T10) and LC3 (T6–T9), blind Opus; LC4 re-checked every repair. Final: T4, T6, T7 VERIFIED; the rest VERIFIED WITH AMENDMENTS, all applied. 43 findings; 2 C (a wrong justification in T3, a missed unreachable stop site in T10), both fixed; no step failed. No item spent a kill-budget attempt.
3. **Sol gate read (T1 + T2, lock + line check, current text incl. the reworded definitions):** launched 17:07, still running; findings will be applied on arrival (Claude re-read only if Sol finds a C).
4. **Flag status (𝒜°, carried into T5/T8):** P-START's source holds "for every event", so P-START with 1_𝒜° costs nothing (still only under (A5)). P-OVL with 𝒜° follows in one line (T8), only under (A5); without (A5) the checked `W3-START2-R:OVL` route applies. Upper bounds transfer to the actual 𝒜 only for potential and calibration-time events; W3-SAMP needs no more.
5. **Findings for HQ:**
   - (a) D1 `schedule_limit` is unreachable on the shipped path, because the tier-1 fallback always yields a valid grid. The INVENTORY summary "the only random no-output path" predates the fallback (consistent with C-DLV:Prop-F).
   - (b) X7/X8 (LS0 cap validators) cannot fire for inputs R can represent.
   - (c) `W1-GEN:L5` [OP] is correct at the pin; `C-ENG:TDP_E` is correct, but its "every cap ≥ 1" holds only for cap ≥ 2 at the pin.
   - (d) N9 Claims S/Z and rows 1–5 re-checked: no error.
6. **Recorder queue (no edits made):** stale line numbers in INVENTORY/S.3/TDP_E; W1-GEN:L5 note "LS0 not in production"; the X7/X8 erratum sentence; the drift D1–D7 of `work/A_inventory.md`.
7. **Better-theorem review:** placeholder line in all ten CHECK.md; not run (HQ ruling pending).
8. **Gate ask:** one OpenAI council batch for T1–T10 (Sol seat + Opus seat, blind), with the statement-change checks of the non-EQUAL changelog rows folded into the Sol seat's brief. T12/T13 recorded as unused by core rows; T11 kept open.
9. **Next on go:** X1–X5 once the Fable marks the relabelling-only ones; the council batch when Codex is allotted.

# STATUS — T09 (T7) kernel validity

- Protocol: proof.md with Felipe's run overrides (lead Opus 5.5 high; one Astra session as consultant/reviewer; no Fable/Opus subagents/Sol) + **Protocol Amendment 1** (managing lead, Felipe-authorized 2026-10-22): Stage A = lead + Astra #1 reach a proof candidate; Stage B = two fresh independent reviews started together (Astra #2, new codex session, high; Opus 5.5 xhigh via T3 delegate_task on claudeAgent_claude_work, model claude-opus-5-5), processed as proof.md step 4, rulings by those reviewers, Astra xhigh judge after 3 rounds of dispute; result label "proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted". Thread ends after Stage B. **Correction to Amendment 1:** the Stage B Opus reviewer runs on Claude Personal (native Agent tool, model opus, effort xhigh, read-only type; or delegate_task on provider claudeAgent, claude-opus-5-5, xhigh), not Claude Work.
- PROOF_v1 written and compiled (7 pp). Sonnet numerical check (helpers/numcheck/REPORT.md): consistent with all claims. Step 1 decision: (a) correct as stated; two informal clauses given precise readings in STATEMENT.md.
- Restarts: 0. Counterexamples presented: 0.
- Astra #1 session id: <uuid> (call 1 failed: "Selected model is at capacity", log in review/; call 2 = one retry by resume of the same session)
- Astra #2 session id: <uuid> (Stage B call 1: no findings, VERIFIED)
- Opus Stage B reviewer: native Agent tool, Plan type, model opus, effort xhigh (Claude Personal)
- Assistants: Sonnet 1 (numerical check, helpers/numcheck/).
- Astra #1 round 1 (call 2): not verified; 1 fatal (my mis-stated gloss in the reading of (v)) + 1 exposition; both accepted and fixed in PROOF_v2 + STATEMENT change log; CLAIMS_OF_FATAL_FLAWS.md written.
- Astra #1 round 2 (call 3): both findings resolved; PROOF_v2 VERIFIED. **Stage A done; proof candidate = proof/PROOF_v2.tex.**
- Stage B round 1: Astra #2 verified, no findings; Opus xhigh verified, 7 exposition findings (all accepted) → unified PROOF_v3 (compiled, 7 pp); claims log updated; changes in review/STAGE_B_CHANGES_v2_to_v3.md.
- Opus Stage B reviewer: native Agent (Plan type, opus, effort xhigh), continued by SendMessage for round 2.
- Stage B round 2: Astra #2 verified (1 new exposition: argmax braces); Opus xhigh verified (3 new exposition: notation clashes). No dispute; Astra judge not used.
- **Phase: DONE (2026-10-22).** Outcome: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted. Final proof proof/PROOF_v3.tex/.pdf. FINAL_REPORT.md written. Temp packet folder deleted.
- Calls: Astra 5 (Astra #1: 3 incl. 1 capacity failure; Astra #2: 2); Opus reviewer 1 agent / 2 calls; Sonnet 1; Haiku 0; Fable 0; judge 0.
- Resume point: none (thread ends after Stage B; Stage C by the managing lead).

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.

# STATUS — T22 (T16) parts (i), (ii), (iv)

Run: theorem proving (proof.md) with Felipe's overrides: lead Opus 5.5 (high), one Astra (GPT-6 Astra, high) session as statement checker / counterexample referee / proof reviewer; Sonnet/Haiku assistants only.

- Phase: DONE (2026-10-22). Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted. Final proof: proof/PROOF_v3.tex/.pdf. See FINAL_REPORT.md.
- Astra session id: <uuid>
- Statement restarts: 0
- Counterexamples presented: 0
- Review rounds: Stage A 1 (verified); Stage B 2 (both reviewers verified v2 and v3); Astra judge not used
- Packet folder: deleted at end of run (all logs copied to review/).
- Resume point: none (run complete). Deferred: Opus N1 (cosmetic dummy-variable rename in (i-a)).

## Protocol amendment 1 (managing lead, authorized by Felipe 2026-10-22)
- Stage A: lead + Astra #1 (the session above) reach a proof both hold correct = proof candidate.
- Stage B: two more independent reviews started together, fresh context: Astra #2 (GPT-6 Astra high, NEW codex session, packet <PC_TEMP_PATH>) and an Opus 5.5 xhigh reviewer (native Agent, read-only; packet ...\T22_T16_start_aggregation\review_B_opus\). Packets: STATEMENT.md, proof tex+pdf, report format only. Process per proof.md step 4; log fatal/gap findings in CLAIMS_OF_FATAL_FLAWS.md; send unified proof + log back to both for rulings. Disputes after 3 rounds -> fresh Astra judge (xhigh); its ruling decides.
eview_B_astra\) and an Opus 5.5 xhigh reviewer (native Agent, read-only; packet ...
eview_B_opus\). Packets: STATEMENT.md, proof tex+pdf, report format only. Process per proof.md step 4; log fatal/gap findings in CLAIMS_OF_FATAL_FLAWS.md; send unified proof + log back to both for rulings. Disputes after 3 rounds -> fresh Astra judge (xhigh); its ruling decides.
- Stage C is the managing lead's; this thread ends after Stage B.
- Result label: "proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted".

## Counts
- Astra #1 calls: 2 (statement check; review v1)
- Astra #2 session id: <uuid>
- Astra #2 calls: 2 (review v2; round-2 ruling v3)
- Opus agents: 1 (Stage B reviewer, xhigh); calls: 2 (review v2; round-2 ruling v3)
- Sonnet agents: 1 (numerical sanity check, helpers/numcheck/)
- Haiku agents: 0

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.

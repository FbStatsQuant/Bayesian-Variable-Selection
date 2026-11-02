# STATUS — T15 (L-OCC) proof run

- Protocol: proof.md with Felipe's overrides (lead Opus 5.5 high; one Astra session, reasoning high; no Fable/Opus subagents/Sol).
- Phase: DONE (2026-10-22). Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted. See FINAL_REPORT.md. Stage A: Astra #1 verified v1 (1 exposition) and v2. Stage B: Astra #2 verified v2, v3, v4; Opus xhigh verified v2, v3, v4; no fatal/gap finding at any point; judge not used.
- Step 1 outcome: (a) correct as stated. T12 dependency made an explicit hypothesis (H-T12) per run rules; pooled-tail sentence formalised as part (iv); no change to inequalities. No statement-checker call needed.
- Astra session ids: #1 <uuid> (2 calls); #2 <uuid> (3 calls).
- Restarts: 0. Counterexamples presented: 0. Statement-checker calls: 0.
- Proof: proof/PROOF_v4.tex/.pdf (current; wording-only revision of v3; 4 pages). v1-v3 kept.
- Helpers: Haiku exact check of the part (iv) example → helpers/check_iv.py: 49/49 pass, canary fails as expected (output helpers/check_iv_output.txt). v2 law re-check → helpers/check_iv_v2.py: 49/49 pass, canary fails (output helpers/check_iv_v2_output.txt). v3 generalised law + population identity -> helpers/check_iv_v3.py: 147/147 and Part B pass, canaries fail (helpers/check_iv_v3_output.txt).
- Packet folders (temp, deleted at end): <PC_TEMP_PATH> (packet, review_B_astra, review_B_opus).
- Stage B: Astra #2 session id <uuid> (log temp ../astraB_r1.log); Opus reviewer = T3 delegated task on Claude Personal (claudeAgent), clientRequestId T15-stageB-opus-personal-r1. (A first launch on Claude Work, T15-stageB-opus-r1, was cancelled unfinished per the managing lead's correction; its output is not used.)
- Resume point: none (thread complete). Stage C (collected Fable + Astra review) belongs to the managing lead. Temp packet folders deleted.

## Protocol Amendment 1 (managing lead, authorized by Felipe 2026-10-22; overrides the review part of the brief)
- Stage A: lead + Astra #1 (session above) reach the proof candidate.
- Stage B (before FINAL_REPORT.md): two fresh independent reviews in parallel — Astra #2 (new codex session, high; packet <PC_TEMP_PATH>) and Opus 5.5 xhigh via T3 delegate_task (provider claudeAgent_claude_work, model claude-opus-5-5; packet ...\review_B_opus\). Packets: STATEMENT.md, proof tex+pdf, report format only.
- Process per proof.md step 4; fatal/gap findings → CLAIMS_OF_FATAL_FLAWS.md; send unified proof + log back to both for rulings. Unresolved after 3 rounds → Astra judge (xhigh, fresh session) decides.
- Stage C (collected review) is the managing lead's; this thread ends after Stage B.
- New label: "proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted".
- Correction to Amendment 1 (managing lead, 2026-10-22): Stage B Opus reviewer runs on Claude Personal (provider claudeAgent), not Claude Work (account balance ~60/40).

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.

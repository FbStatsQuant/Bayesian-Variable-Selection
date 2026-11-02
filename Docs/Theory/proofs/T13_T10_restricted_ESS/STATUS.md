# STATUS — T13 (T10) restricted ESS proof run

- **Phase: DONE (2026-10-22).** Outcome: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted. See FINAL_REPORT.md.
- Final proof: proof\PROOF_v4.tex / PROOF_v4.pdf (xelatex). Statement: STATEMENT.md v3 (approved by Astra #1).
- Lead: Opus 5.5 (high), also operator (Felipe's overrides for this run). Protocol: proof.md with overrides + Protocol Amendment 1 (managing lead, authorized by Felipe 2026-10-22) and its correction (Stage B Opus reviewer on Claude Personal).
- Step-1 restarts: 1 of 3. Counterexamples presented: 0. Astra judge: not used.
- Astra #1 session id: <uuid> (7 calls). Astra #2 session id: <uuid> (2 calls).
- Stage A: v1 not verified (1 gap: uncertified numerics) → v2 verified (1 exposition) → v3 verified (proof candidate).
- Stage B: v3 not verified by both (same gap: method definitions not in the packet) → unified v4 with Appendix B (verbatim quotes, with SHA-256) → v4 verified by Astra #2 and by the Opus xhigh reviewer.
- Calls: Astra #1 7; Astra #2 2; Opus reviewer 1 agent / 2 calls; Sonnet assistant 1; Fable 0; Sol 0; judge 0.
- Packet folders (Temp\v3proofs\T13_T10_restricted_ESS\) deleted at the end; their inputs are archived in review\packets_archive\.
- Resume point: none (thread complete). Stage C (collected document + Fable/Astra campaign review) belongs to the managing lead.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.

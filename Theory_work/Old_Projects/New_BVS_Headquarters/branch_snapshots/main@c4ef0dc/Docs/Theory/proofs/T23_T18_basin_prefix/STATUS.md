# STATUS — T23(ii) proof run

- Protocol: proof.md with the run overrides (lead Opus 5.5 high; one Astra session; no Fable/Sol).
- **Protocol Amendment 1** (managing lead, authorized by Felipe 2026-10-22):
  - After Stage A (lead + Astra #1 agree), Stage B adds two independent reviews started together: Astra #2 (new codex session, high) and an Opus 5.5 xhigh reviewer (own account, read-only).
  - The reviews are processed per proof.md step 4. Disputes still open after 3 rounds go to a fresh Astra xhigh judge.
  - New label: "proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted".
  - Stage C is the managing lead's, not this thread's.
- **Phase: DONE.** Outcome: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.
- Final proof: proof/PROOF_v4.tex + proof/PROOF_v4.pdf. Report: FINAL_REPORT.md.
- Statement restarts: 0. Counterexamples presented: 0. Statement changes: none.

## Stage A — DONE
- Astra #1, session <uuid> (gpt-6-astra, high): 1 call. PROOF_v1 verified, no findings.

## Stage B — DONE
- Astra #2, session <uuid> (gpt-6-astra, high, new session): 4 calls (1 new + 3 resumes).
- Opus reviewer: native Agent (Plan type, model opus, effort xhigh): 1 agent, 4 calls (1 launch + 3 SendMessage continuations).

| Round | Astra #2 | Opus reviewer | Result |
|---|---|---|---|
| 1 (review of v1) | verified, no findings | verified, 6 exposition findings (all accepted) | → PROOF_v2 (review/B_CHANGES_v1_to_v2.md) |
| 2 (rulings on v2) | verified, 1 exposition point | verified, 6 exposition points | all accepted → PROOF_v3 (review/B_CHANGES_v2_to_v3.md) |
| 3 (rulings on v3) | verified, no findings | verified, 2 exposition points | accepted → PROOF_v4, wording only (review/B_CHANGES_v3_to_v4.md) |
| 4 (confirmation of v4) | verified, no findings | verified, 1 cosmetic note | note deferred (the path symbol Z reuses the evidence symbol Z) |

- No fatal or gap finding in any round, so no dispute and no Astra judge.
- Packet folders under the Temp v3proofs T23 folder: deleted.
- Calls: Astra 5 in total (Astra #1: 1, Astra #2: 4); Opus reviewer 4; Astra judge 0; Sonnet / Haiku / Fable / Sol 0.
- Resume point: none. The thread ends after Stage B; Stage C belongs to the managing lead.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edit applied: E23-1 (STATEMENT.md section 3, one sentence appended after the displayed inequality of conclusion (ii-a), also in Theorem (a) of the proof). New final files: proof/PROOF_v5.tex and proof/PROOF_v5.pdf (PROOF_v4 kept unchanged); STATEMENT.md updated (copy before the edit: STATEMENT_before_stageC.md). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.

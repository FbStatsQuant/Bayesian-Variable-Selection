# Proof audit experiment (2026-10-15)

**What this is.** An experiment designed by Felipe. It is not one of the official protocols; its purpose is to learn how far automated scientific review can go. Felipe approved it on 2026-10-15 and waived the plan-review gate (Gate A).

**Goal.** Independently audit every proved result in the paper draft, adjudicate the findings, repair the proofs, and then rewrite `paper_draft.tex` so it is cohesive.

## Roles
- **22 GPT-6.1 Sol auditors** (reasoning effort high), one per proved result.
  - Invoked with `codex exec -m gpt-6.1-sol -s read-only`, which can only read.
  - Each gets the current draft, the proof file and the instructions inlined in its prompt (`SOL_INSTRUCTIONS.md`).
  - Output: `_audit/<ID>/SOL_AUDIT.md`. The session ID is saved in `_audit/<ID>/SESSION_ID`.
- **3 Opus 5.5 adjudicators** (effort high), one per group.
  - They rule on each finding.
  - They may hold a dialogue with **their own** Sol auditors only, by resuming those sessions: at most 2 exchanges per finding.
  - They edit `PROOF.md` in place, after backing it up as `PROOF_pre_audit.md`, and rerun the folder's check scripts.
  - They ask the same Sol to confirm the changed sections.
  - **They never edit the paper.** They write `RULINGS.md` and `PAPER_CHANGES.md` in `_audit/group_<X>/`.
- **The lead** (this session, Opus 5.5) integrates `PAPER_CHANGES.md` and then rewrites the paper for cohesion.

## Groups (by folder, so no two adjudicators edit the same file)

| Group | Folders | Results |
|---|---|---|
| A | elementary_I | P1, T1, L1, L2, L3, L5, L7 |
| B | T3_T11, T4, T5, foundations | T3, T11, T4, T5, L4, L6, P6, P7, F4 |
| C | T6, T7_T8, T9_C9 | T6 (with T9a(i)), T7, T8, T10, T9 (with T9a(iii)), C9 |

## Waves
The Sol audits run in waves, one group per wave: A, then B, then C. Each group's adjudicator starts as soon as that group's audits are in.

## Budget
- 22 Sol audits.
- About 40 Sol follow-up exchanges at most.
- 3 Opus adjudicators.
- No Fable.

## Backups
- Draft before the audit: `paper_draft/paper_draft_v10_preAudit.tex/.pdf`.
- Each proof before the audit: `proofs/<folder>/PROOF_pre_audit.md`, made by the adjudicators.

## Log
- 2026-10-15: smoke test of gpt-6.1-sol passed. Wave 1 (group A) launched.
- 2026-10-15: wave 1 done (7/7 exit 0): all VERIFIED; 7 EXPOSITION findings. Adjudicator A launched. Wave 2 (group B, 9 audits) launched.
- 2026-10-15: adjudicator A done: 7/7 PROVED, 7 EXPOSITION accepted, no proof changes, 0 Sol exchanges; PAPER_CHANGES E1-E10; check_audit_A 26/26 (rerun by lead).
- 2026-10-15: wave 2 done (9/9 exit 0): 6 VERIFIED; NOT VERIFIED: T5 (FATAL on (vi)), P6 (FATAL on Gibbs-sweep sentence), P7 (FATAL on terminal weights). Adjudicator B and wave 3 launched.
- 2026-10-15: wave 3 done (6/6 exit 0): all VERIFIED, 17 MINOR/EXPOSITION. Adjudicator C launched.
- 2026-10-15: adjudicator C done: 6/6 PROVED; 18 findings (7 MINOR, 11 EXPOSITION) all ACCEPT; proof remarks edited in T6, T7_T8, T9_C9; 8 Sol exchanges, all changes confirmed; check_audit_C rerun by lead.
- 2026-10-15: lead applied group A (E1-E9) and group C (all but G3: the Laurent-Massart 'checked against source' claim rests on Sol recall, not access; kept unverified) to paper_draft.tex; compiles 0 errors.
- 2026-10-15: group B applied (39/39 edits); all groups integrated; backup v12_preCohesion; cohesion pass started.
- 2026-10-15: cohesion pass applied (apply_cohesion.py: abstract, reading guide incl. proof-folder map, intro/contributions, unified status tags, notes label, Sec 4 standing-assumption relaxation, T2 template note, dependency map incl. F4 row, headline results with T2/Pb4 as open slots, consolidated revision history as Appendix C). Draft 37 pp, 0 errors. EXPERIMENT COMPLETE.

# Theory Wave 3 — HQ decisions log

- 2026-11-09 W3-POST: the protocol's mid-point + sweep layers are replaced, for this re-check ticket, by the two
  independent whole-chain adversarial re-checks R01 (gpt-6-astra high) and R02 (Opus high), followed by a passed council
  (C3: 8.8/8.7). Reason: the object was an existing proof chain, and two whole-chain adversarial reviews cover more than a
  mid-point + sweep. Labels: Theorem 1 chain "PROVED-CHECKED (W3-POST re-check)"; Lemma 1a′ and Proposition LB
  "PROVED-CHECKED (W3-POST: R01/R02 + council C2/C3 line checks)".
- 2026-11-09 W3-POST follow-up: launch W3-POST2 (improvements 1, 3, 4, 1b; 2 as stretch with a kill budget).
- 2026-11-11 (resume, owner go for launch 13:00 CT): providers per PROTOCOL item 2 amendment of 2026-11-11 (CP = Fable 5.2
  only; all other Claude on CW).
- 2026-11-11 W3-RM: keep STATEMENT v1.2.1 (both council rounds reviewed v1.2.x). Result stated as (V)+(L)+lattice
  condition (N)/(D-R); replacing (N) is the kill-budgeted path-level follow-up. Labels per clause: RM-0, RM-F, RM-R,
  Lemma E4, examples PROVED-CHECKED (council C2 Astra 9.8 / Opus 9.1).
- 2026-11-11 W3-SAMP: labels per clause CC, PC, MR, ST, D, LT#, C, TR PROVED-CHECKED (SW1 + council C1 9.1 / 8.8);
  NC_r necessity OPEN; P-START remains a named input (W3-START).
- 2026-11-11 W3-POST2: post-lock strengthenings (items 3, 4, 5 via (ID^M)) approved; E1 v2 restatement ruled within the
  kill budget. Claims A-E PROVED-CHECKED (council C1 8.6 / 8.6).
- 2026-11-11 W3-RM2 lead upgraded to Fable 5.2 (hardest open proof; sub-par theorem risk).
- 2026-11-11 registry ingest of W3-RM, W3-SCR, W3-POST2 via tools/ingest.py after PR #6 merges (rule 8 post-dates them).
- 2026-11-11 CORRECTION to this morning's labels (following pipeline review R01, rule 15): W3-SAMP:CC keeps its
  REPORT status (CODE-CHECKED); HQ does not upgrade it. The PROVED-CHECKED labels for W3-RM, W3-SAMP and W3-POST2 are
  **on hold** until a Sol diff check confirms that the edits made after each council (RM C2_disposition, SAMP C1 "11
  items applied", POST2 C1 disposition) are editorial or correct. Until then, registry statuses stay verbatim from
  each REPORT. W3-POST2 strength stays `better:PENDING` (four R03b proposals open).
- 2026-11-11 Headline flags: all 43 `headline=yes` rows were set by tools (ingest.py marks any claim with strength
  fields); none is an owner decision. They are treated as headline (changes need Felipe) until Felipe confirms the
  headline set at chapter v2.0. W3-SAMP:D and W3-SAMP:TR were registered from a mid-ticket draft; their final, council-
  reviewed statements are narrower (D: KERNEL hypothesis added; TR: the non-nesting label holds only for abstract
  targets). Recorded as NARROW+CLEAR, no dependent became SUSPECT. **Awaiting Felipe's approval.**
- 2026-11-11 W3-RM post-council diff check PC1 (Sol): CLEAN. Four substantive edits (B1, B2, B4, B5), each verified
  correct. The review notes that the disposition called some of them editorial, inaccurately. PROVED-CHECKED labels for
  W3-RM are restored (RM-0, RM-F, RM-R, E4, examples), with evidence = council C2 + PC1.
- 2026-11-11 W3-SAMP PC1 (Sol): math CLEAN (8 substantive post-C1 edits verified), record NOT-CLEAN. HQ record fixes made
  (LT Step 3 shows the λ₀ display; REPORT states the joint-law idealisation; provenance notes corrected). PC2 check running.
  Labels stay on hold until PC2.
- 2026-11-11 W3-POST2 PC1 (Sol): NOT-CLEAN. A post-council edit introduced a false inequality in the D(b) proof
  (D_hellinger.md:53; the intended bound is valid). Rollback: `propagate.py suspect W3-POST2:D.D(b)` applied (D becomes
  SUSPECT; repair issue opened). Repaired by HQ per PC1 P1; P2/P3 qualifications propagated. PC2 repair check running;
  then `propagate.py patch` and `clear`. This shows R01 was a real failure mode, not a theoretical one.
- 2026-11-11 W3-SAMP PC2 (Sol): RESOLVED. PROVED-CHECKED labels restored for PC, MR, ST, D, LT♯ (a–e, b′, e′), C and TR
  (evidence: C1 pre-edit votes + PC1 + PC2). CC stays CODE-CHECKED; LT♯(f) stays OPEN.
- 2026-11-11 Schedules (rule 12/13), all T3 scheduled tasks:
  - daily CI audit 06:00 CT, `scheduled-task:1ddaffb6-3203-45be-b086-bb1f3cc65280`, next 2026-11-12 06:00;
  - watchdog every 6 h, not bound to HQ, `scheduled-task:e3816541-adbf-4337-901d-3d9e1a36cf1a`, next 2026-11-11 15:01;
  - weekly re-audit Monday 07:00, `scheduled-task:e9c81940-591c-4d95-bd6c-8a07e10409d3`, next 2026-11-16;
  - HQ heartbeat every 3 h, `scheduled-task:c88adcb5-a968-4746-8b46-791d062f57b9`, next 2026-11-11 12:01;
  - launch once at 13:00, `scheduled-task:bddb093c-41e5-4a57-ade9-f3a3eb910f23`.
- 2026-11-11 W3-POST2 PC2 (Sol): REPAIRED. `propagate.py patch` + `clear` on W3-POST2:D.D(b) and W3-POST2:D; both
  ACTIVE. PROVED-CHECKED labels for W3-POST2 claims A–E restored (evidence: C1 + PC1 + PC2); strength `better:PENDING`.
  First full use of the rollback path (suspect → repair → check → patch → clear): it worked end to end.
- 2026-11-11 11:40 Owner (Felipe): deploy now, in owner-gated legs ("checkpoints"); HQ reports at each and waits for the
  owner's greenlight. The 13:00 one-shot launch task is deleted (superseded). INFRA tool fixes round 2 merged (d6da494;
  103/103 scenarios; Sol review breaks R1–R6 fixed); tag `theory-v2.0-pre` pushed. **Leg A**: W3-START to CP1 (Fable CP,
  branch theory/W3-START), W3-MEMO-SCR-RM complete (Fable CP + blind Astra), pipeline reconciliation R03 (Sol). W3-P6 lead
  (Opus CW) starts only if R03 finds no open CRITICAL, and stops at CP0 (smoke manifest; nothing submitted on NOTS in
  leg A). Leg A ends → report to Felipe → wait.
- 2026-11-11 Pipeline R03 (Sol reconciliation): NOT-READY. F1, F3–F7, R02–R04, R07–R09, Sol-2–6 and toolfix2 R1–R6 RESOLVED.
  Open: N2 CRITICAL (a review "binds" by quoting a digest, without a bound outcome), N1/N3/N4 MAJOR (transitive assurance,
  disposition evidence, crash-safe journal) → INFRA tool fixes round 3 (Opus CW, worktree, own Sol review). N5 MAJOR and
  F9 MINOR fixed by HQ (2ab1dca): fail-closed hold file `Wave3/HOLDS.md`; watchdog, daily CI and weekly re-audit prompts
  now append holds; leads told. Per the launch rule, **W3-P6 stays held** until round 3 merges and a narrow Sol re-check
  finds no CRITICAL. CP3 hold (rule 16) unchanged. START and memo unaffected (no CP3 in leg A).
- 2026-11-11 Console API credits (owner; ≈ $113, expire 11-15): key `bvs-audit` stored outside the repo. Proposed use:
  Message Batches Fable 5.2 blind audit of all 109 PROVED-CHECKED claims (≈ $50), then needed PROVED claims (≈ $40);
  findings → HQ triage → Sol confirmation → rule 11. Awaiting owner go.
- 2026-11-11 W3-MEMO-SCR-RM done (branch theory/W3-MEMO-SCR-RM @ 20bf513; Astra B1 blind review of v1: REJECT as written,
  8 findings all accepted; v2 not re-reviewed). HQ adopts recommendation (a): SCR-C enters chapter v2.0 as the
  exact-recovery corollary of Theorem 5, plus a certificate column in the examples table; headline unchanged; no RM
  supersession claimed. W3-RM2 keeps its polynomial-leakage target (PL does not give its key lemma). The two PL sketches
  and Corollary CERT go to the path-level ticket / chapter v2.0 as inputs, each needing its own review before any claim
  enters the registry; memo v2 is scoping input only. A new ticket (c) only if W3-P6 shows Ŝ = S₀ at frequency ≈ 1 on
  dense-leak designs. Memo branch merges with the other Wave 3 work after rule 16 lifts.

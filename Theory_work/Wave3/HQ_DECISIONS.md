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
- 2026-11-11 Pipeline R04 (Sol, narrow): READY — no open CRITICAL; R03 N1–N4 and toolfix3 defects resolved; 127/127.
  Two MAJOR open (R04-N1 accepted-input evidence/verdict changes do not stale its accept record; R04-N2 statement-file
  relocation not in the fingerprint) → small tool fix in leg B. Rule 16 (no CP3 ingest/merge) stays until they are fixed.
  W3-P6 cleared to start: lead Opus CW, leg A = CP0 only (smoke manifest; NOTS read-only).
- 2026-11-11 W3-START CP1 (branch @ 58309da): adopt P1, P3; P2 with a one-attempt kill budget; OVL inequality kept,
  corollary if cheap; O1–O3 deferred. Continuation waits for the owner's leg-B go.
- 2026-11-11 ~17:40 CT (owner): all Claude threads on Claude Work, Fable 5.2 included; Claude Personal unused
  (PROTOCOL item 2 amended). Switched: W3-START lead thread → CW Fable 5.2 high; watchdog thread → CW Opus high.
  HQ thread moves to CW Opus high at the end of this turn (memory copied to the CW config).
- 2026-11-11 ~18:00 CT (owner): API audit GO. Pass 1 submitted: Message Batches `msgbatch_0148MUMvKUm8r1au3Y6W7Xpk`,
  Fable 5.2 effort high, 39 requests (one per claim file), 109 PROVED-CHECKED claims, blind (reviews/ withheld).
  Input 2.13 M tokens (≈ $8.5 at batch rate); worst-case output $50. Tool + inputs: Theory_work/Wave3/API_AUDIT/.
  Findings → HQ triage → Sol confirmation → rule 11 (holds via HOLDS.md if confirmed CRITICAL/ERROR).
- 2026-11-11 (owner): the HQ consultant runs on Claude Personal, Fable 5.1, effort high — the one exception to the
  all-CW rule. Consulted on the W3-P6 ceiling basis and S3.
- 2026-11-11 ~18:20 CT W3-P6 CP0 (owner delegated to HQ + consultant, CP Fable 5.1): ceiling basis (B) — 1,400 core-h
  counted from the resume = **1,896 total** since 2026-11-09 (worst-case admission against 1,896); watchdog HOLD at
  1,700 total. Smoke manifest approved **with S3** (S1–S5, worst +200 → 695.88). Release plan replaced by the
  consultant's staged design, pre-declared before any outcome is seen: stage 1 = reps 1–10 on all kept cells; stage 2 =
  reps 11–20 on the D1 cells (75,750), (100,1000), (75,188), (100,250) cs ρ=.5 and on any cell with 1–3 failures in
  stage 1. Kept cells: b1 remainder, (75,75), (100,100), (75,188), (75,750), (100,250) cs .5, (100,1000); at (100,250)
  breadth only cs ρ=.7 and s₀=8 at 10 seeds. Deferred: (150,150) (smoke seed only). Dropped: n=200, (50,2500).
  Scheduled seeds stay in the denominator; cells stopped at 10 are budget cuts. Admission: measured max × 1.5 × 2 for
  costed cells, worst case for uncosted; (100,1000) and (150,150) in sub-batches of 5; longest first. Expected ≈ 1,500
  from resume; stop after stage 1 if the ceiling binds (stage 1 is decision-grade for persisting search failures).
  Execution waits for the owner's leg-B go.
- 2026-11-11 ~18:35 CT (owner): **leg B GO, full version**; "lean fully on CW until further notice" — the consultant
  exception is withdrawn (consultant thread now CW Fable 5.1 high); no Claude Personal use at all. Launched: W3-RM2 lead
  (CW Fable 5.2, worktree BVS-wt/W3-RM2 @ 9700e17) to CP1; INFRA R04 fix (CW Opus, worktree BVS-wt/INFRA-R04 @ 3d6d84d)
  + one Sol check; W3-START lead resumed (CW Fable 5.2) to CP2; W3-P6 lead resumed (CW Opus) to submit the smoke S1–S5.
- 2026-11-11 API audit pass 1: 86 OK / 19 MINOR / 1 GAP (C-DLV:Prop-F) / 3 requests re-run at 128k (pass1b). R-AUD1 Sol:
  CONFIRMED-WORDING — scope clarification only, no consumer relies on the strong reading; no registry mark. Wording fix +
  MINORs → editorial pass with chapter v2.0 (API_AUDIT/pass1/TRIAGE.md).
- 2026-11-11 API audit: pass 1 final 87 OK / 21 MINOR / 1 wording / 0 ERROR over 109 PROVED-CHECKED (≈ $32 incl. re-run).
  Pass 2 submitted (plan's second item): msgbatch_01JERwr2jhDAFhxUhuLk2vmG, 48 requests, 92 author-only PROVED claims
  of the tickets feeding running work and the headline (W3-RM, W3-POST2, W3-POST, W2-LOC2, W1-GEN, W1-PXN, W1-N1,
  W1-N3, C-PACK, W2-UNI, C-ENG, W2-APP); input ≈ $10, worst-case output $61 (balance ≈ $80). Remaining factor-design
  PROVED claims (W2-FAC-*) only if credit remains.
- 2026-11-11 ~18:45 CT (owner): **continuous mode** — CW has ~20 h of weekly capacity before reset; do not stop and do
  not burst; effort ≤ high; HQ answers checkpoints itself and asks the owner only key decisions. A meta-HQ Sol thread
  (owner's) resumes HQ after any 5-h limit. Resume card: Wave3/HQ_NOW.md.
- 2026-11-11 API audit pass 2: 72 OK / 12 MINOR / 0 GAP/ERROR (≈ $14); f00 (8 W1-GEN headline claims) hit 64k → pass2b
  at 128k. Pass 3 (plan item 3, credit remains): msgbatch_017Qeq255ojPUvhjEePbobwf, 40 requests, 50 author-only PROVED
  W2-FAC-* claims; input ≈ $9, worst-case output $51 (balance ≈ $67, expires 2026-11-15).
- 2026-11-11 W3-START CP2 (branch @ b469719): START-F proved (L1–L5), LC1 line checks + MP1 Astra
  CONTINUE, audit OK. GO to CP3; STATEMENT v1.3.1 (necessity on the actual partition; partition-free only s₀ ≥ 16) +
  Sol diff check; (B-R) kill budget one Fable attempt + one Astra break review, else narrow (T3)(b) via CP1.
- 2026-11-11 API audit pass 3: 42 OK / 5 MINOR / 3 GAP (≈ $16; audit total ≈ $64, ≈ $49 credit left). R-AUD2 Sol
  confirmed the GAPs (S5F:L0, S5F:L1, FAC-X:L4r.5; one wording-only); no PROVED-CHECKED or chapter impact. Rule 11:
  SUSPECT on the three lemmas (+ S5F C1–C4 dependents); repairs not scheduled (stop list).
- 2026-11-11 ~18:15 CT (owner): HQ has discretion over the remaining API credits ($44.98, expire 2026-11-15; month
  spend limit $195 leaves ≈ $40). Plan: blind Fable audit of W3-START and W3-RM2 at CP3 (in place of a Claude council
  seat where the protocol allows), cap ≈ $35; keep ≈ $5 margin.
- 2026-11-12 00:30 UTC INFRA R04 fix merged (656982a; Sol R04FIX RESOLVED for R04-N1, R04-N2; 134/134 on merged main;
  check.py 0 ERROR). Rule 16 LIFTED: CP3 ingest/merge allowed again under rules 9–15.
- 2026-11-12 ~00:21 UTC CW account incident (owner fixed: CW now the Team account). Runs cut off: W3-START lead (CP3 leg)
  → resumed. W3-RM2 lead was already stopped at CP1 (waiting on HQ).
- 2026-11-12 W3-RM2 CP1 (branch @ 81ff7d6): v1.2 locked (b < ½ via width condition (W)); adopt P1,
  P2/G1 → v1.3 + Sol check; P3 one attempt in Form R after CP2; Form R kept; RM2-F/R as candidates implying RM-F/R
  (supersession at CP3, owner informed). GO to CP2.
- 2026-11-12 W3-START CP3-PASS (R1 sol 9.1 / opus 8.8, gates PASS; branch e2f2271, merged with main 29b3aab). HQ audit:
  bind OK; staged ingest 21 claims / 0 problems, but acceptance REFUSED (A4): MANIFEST_R1 lists PROTOCOL.md,
  LIFECYCLE.md, the ASSUMPTION_MAP template and claims.tsv as inputs, all edited on main after the round (HQ edits,
  none a proof premise). Decision: council R2 on the merged tree (v1.3.4 with R1's non-blocking edits; INPUTS pruned
  of wave documents/registry tables) + Sol diff check v1.3.3→v1.3.4; Astra better-theorem review BT2 on the final
  statement in parallel (statement changed materially after CP1 → headline gate). PROTOCOL rule 15 amended: INPUTS
  never lists wave documents or registry tables.
- 2026-11-12 ~01:30 UTC (Felipe away; delegated owner decisions to HQ with the CW Fable 5.2 consultant).
  W3-SAMP D/TR narrows APPROVED (consultant concurs): wider statements were never proved; the council reviewed the narrow
  ones; headline flags were tool-set; no dependents. Open sharpness item for Felipe: TR separation from π₀(S₀) → 1 is
  open for the coded target ("method as coded" goal).
  Track 3 scaling leg A LAUNCHED (W3-SCALE, BRIEF.md): profile-first, bit-identical speedups (no Gram-free scoring),
  bit-identity on NOTS PROD-H (= track 1 gate 0), sd(log Ẑ_r) table, DESIGN_v1 last; cap 150 task-h (≈300 core-h);
  P6 keeps priority. Reserved for Felipe: p = 1M fixed-N islands; primary PIP switch.
  Track 1 NOT ready (v3.2 comes from track 3). Note for Felipe: on v3.1 the rerun is a deterministic identity check;
  if v3.2 stays bit-identical, a gate-0-size sample may replace the full 910 core-h rerun.
- 2026-11-12 ~02:20 UTC (Felipe): next API grant (~$200, ≈11-15) allocated to theory: ~$100 blind audits of new
  results (W3-START, W3-RM2, parallel-SMC theorems, final chapter v2.0 pass), ~$50 sharpness follow-up, ~$50 reserve for
  Fable break reviews of risky scaling theory. The p = 1M campaign runs on NOTS + CW, decided at W3-SCALE CP1.
- 2026-11-12 ~02:40 UTC sharp1 triage (consultant, API_AUDIT/sharp1/TRIAGE.md): A-list T1 MIS-R, T2 RM-0 rider (after
  RM2 council), T3 POST-SHARP; B* T4 (constant-level signals, rider on RM2), T5 (Cor 1R v2, lowest). LAUNCHED W3-MISR (T1)
  and W3-PSHARP (T3), Fable 5.2 CW leads, legs to CP2 pre-approved when reviews are clean. f01 handed to W3-SCALE.
- 2026-11-12 ~03:00 UTC sharp1b triage (consultant, API_AUDIT/sharp1b/TRIAGE.md): 9 B, 1 C, new: T2(c) (RM-0(a) on any
  deterministic down-closed sub-lattice ⊇ [S₀, S̃₀]); T6 product-form localisation (entrywise cross-term bound; polynomial
  decay α > 17/2 → α > 2) as a rider on RM2's Form R leg next to P3; T7 masked truths at growing Q (separation via
  underfit-phase energy lemma; GEN/PXN become examples), kill-budgeted, after RM2 council. f18/f20/f21: redo per claim.
- 2026-11-12 ~05:10 UTC W3-RM2 CP2 ACCEPTED (Form F key lemma, 1/3 attempts; LC1/RC3/RC4 clean; MP1 Astra no FATAL/MAJOR).
  GO Form R leg → CP3; P7 kill budget 2 then Form-F-alone fallback; MP1 witness to (C5); T6 rider one attempt in L4.
- 2026-11-12 ~05:40 UTC W3-START CP3 acceptance REFUSED (delegate audit; branch 808ddd1, not merged): checks a, d, e, f
  PASS; b/c FAIL — bvsreg.py coverage rule requires the status-source file in the frozen manifest, but status lines live
  in CHECKPOINT_3.md (excluded by design): a tool defect affecting every CHECKPOINT-layout ticket. Decision (consultant
  concurs): option (T), INFRA R05 tool fix, not council R3. Safeguards: (1) exempt only the ticket's own
  CHECKPOINT_<k>.md and only as status source; statement/premise files still covered; (2) council files bind to the
  acceptance manifest with PASS (earlier rounds bind to their own manifests); (3) record the checkpoint sha256 in the
  registry row at ingest, CI flags later edits; (4) claim ids in the checkpoint == ids both council seats accepted;
  (5) Sol review with negative tests (unbound review, arbitrary uncovered status file, uncovered statement, extra claim
  id) + re-run on already-accepted tickets with no verdict change. Check (e) becomes tool-enforced: each cited round id
  resolves to exactly one existing review file quoting a digest. Then re-run W3-START acceptance.
- 2026-11-12 ~10:40 UTC W3-SCALE CP1 ACCEPTED (branch theory/W3-SCALE b2c0194): bit-identity PASS 24/24 PROD-H + 10/10
  supplementary (two Sol reviews, no output difference on valid fits); setup 20k 85.6 → 23.1 s, peak 9.24 → 6.26 GiB;
  profile 1k/2k/20k-island; sd(log Ẑ_r) table; NOTS 27.8 task-h used. DESIGN_v1 rev 2 unreviewed (Astra judged rev 1
  UNSOUND, 18 findings applied). Leg B APPROVED (B1–B5, new cap 150 task-h, bit-identical only), order: B5 (second Astra
  round on DESIGN_v1 rev 2) BEFORE B2 relies on §4.1; B4, B1 in parallel; B3 measurements after B1.
  O17 RULING: "output-identical" covers every statistical output (estimates, PIPs, HPM, evidences, top store) AND every
  quantity that enters a published table or theorem check (incl. the RERUN_SPEC / EVIDENCE §8 cost column). Diagnostic
  counters (`fresh`, cache statistics) may differ only if (a) none feeds a published table, or (b) the island-only
  worker also reports serial-equivalent totals that match the serial run exactly; B2 must show which holds.
  5k profile (job 2692690): the lead folds it in at the start of leg B. Reserved items stay with Felipe.
- 2026-11-12 10:17 UTC W3-MISR CP2 ACCEPTED (branch theory/W3-MISR ba2cd0c): council R1 PASS sol 9.3 / opus 8.7 (manifest d3f5c91f…);
  Lemma R′ (exact affine invariance of the coded posterior, code-pinned 16a7f85, 25 rescaled fits |ΔPIP| ≤ 1.3e-10); MIS-R
  without fixed σ², τ²; Song–Liang Thm 4 analog corollaries. Final leg: one Astra sweep on d3f5c91f (mid-point waived:
  council + line checks cover a ticket this size); wording fixes batched + Sol "editorial only" diff check; CHECKPOINT_3.
  Acceptance after INFRA R05; C-MIS → MIS-R supersession decided at acceptance (owner informed). Queue: BT1-A2, B1, B2.
- 2026-11-12 10:34 UTC W3-MISR CP3 final (branch 4437ecd): sweep 0 FATAL/MAJOR; council R2 sol 9.2 / opus 8.9 (manifest 217d6708…);
  acceptance after R05. W3-START BT2 P1–P4 → ticket W3-START2 LAUNCHED (Fable 5.2 CW; branch from theory/W3-START).
  Queue INFRA R06: manifest hashes are EOL-dependent (CRLF-only verify; fails on an LF checkout) — normalise or pin
  .gitattributes; do after R05, without invalidating existing bound manifests.
- 2026-11-12 ~07:30 CT (owner): Claude threads on **Claude Personal** for now (CW hit its 5-h limit twice). Model policy:
  Opus leads by default; Fable only for new hard proofs (W3-START2 keeps Fable 5.2) or kill-budgeted consults on a stuck
  key lemma. Switched: W3-SCALE → Opus, W3-PSHARP → Opus, W3-START2 stays Fable; consultant → CP Fable 5.2. Owner busy
  today: HQ settles operational decisions with the consultant; owner only for big picture and token management. 09:05
  auto-resume task disabled; leads resume on HQ's order after housekeeping (R05 merge, acceptances).
- 2026-11-12 W3-PSHARP CP3-PASS (branch 11524d0; council R2 sol 9.2 / opus 9.3, manifest 4513e05a…, bind OK; reconciliation
  11/11 resolved). Claims S, A, B, C → acceptance audit (with W3-START, W3-MISR, W3-RM2). Editorial batch E1–E9 applied
  only after acceptance, with the pass-1/2/3 MINORs, under one Sol "editorial only" diff check (rule 15).
- 2026-11-12 W3-START2 CP1 ACCEPTED (branch 2c66e61): STATEMENT v1.4.1 (BT2 P1–P4) locked, SL1 + SC1 Sol clean. GO to
  CP2/final per the pre-approved brief; one repair attempt per broken step, else that P-item → open item. Council Opus seat
  and Claude helpers on claude-personal today (CW unavailable).
- 2026-11-12 ~07:50 CT acceptance audit (Opus; clones): R05 MERGED to main (3ce2e27; 146/146; 0 ERROR). W3-START
  ACCEPTABLE (21 claims); W3-MISR, W3-PSHARP, W3-RM2 refused on record-keeping only (no per-claim seat tables; MISR 3
  'remark' rows; RM2 malformed REPORT fence + 7 post-council edits inside MANIFEST_R1). Cross-cutting: manifests verify
  only on the frozen mixed-EOL tree. Decisions (consultant concurs, its advice adopted in full):
  (1) INFRA R06 = one PR: manifest/registry hashes accept raw, LF-normalised or CRLF-ised text (NUL files raw); sha256,
  status_sha256, fp2 normalised; tests on LF and CRLF checkouts; + confirm safeguard 4 reads a dated addendum table and
  ingest from a carrier file outside the manifest. One Sol review. Before any `--record`.
  (2) Seat tables by addendum: same seat models, fresh threads, frozen manifest + own review; rows cite where the review
  examined the claim; ACCEPT / NOT-EXAMINED only; no rescoring, no second COUNCIL-VERDICT; NOT-EXAMINED loses the label
  or gets a targeted review.
  (3) RM2: accept on the restored R1 snapshot via a separate carrier (F.jsonl), Sol field-by-field match; post-council
  edits inside the manifest parked for RM2's next council round (outside-manifest edits may go in now); fall back to
  council R2 only if PC1 doesn't cover all 7 files or an edit touches a statement/proof line. RM2-F/R accepted as checked
  intermediates; headline supersession of RM-F/R → owner.
  (4) MISR: drop the 3 remark rows from the carrier (no consumer). Order: R06 → START --record → PSHARP addendum → MISR →
  RM2. Opus/Sol only, no Fable.
- 2026-11-12 ~11:00 CT W3-P6 CP1 ACCEPTED (branch 703a6b2; consultant concurs): smoke 5/5 completed, HPM = S₀ in all,
  invariants pass; 581.9 core-h. GO stage-1 wave 1 (d1, h1, h2, c, b, b1r); later waves self-released by the lead under the
  ledger rule (finished core-h + Σ limit×2 of queued/running ≤ 1,896; stop if projected > 1,700; a 24:00 rerun reserves 48
  core-h and passes the same check). b1 remainder: all 21. (100,100) at a 4:00 limit in a later wave (after b1r).
  Pre-declared before any stage-1 outcome: failure = completed fit with HPM (MR1 cap, as coded) ≠ S₀; a fit stopped by the
  22.5-h guard is censored (neither; stays in the denominator; reported by bounds per DESIGN §6); ≥ 3/10 censored in a cell
  = infeasibility finding → return to HQ. Stage 2 conditional: reps 11–20 only on cells with 1–3 failures; within the
  remaining budget, else the owner is asked for that cell's measured cost. Pooled 0/40 is a gate statement only.
  summarize.py v4 (Sol R02 fixes + Group A header) with a fresh Sol review before any analysis.

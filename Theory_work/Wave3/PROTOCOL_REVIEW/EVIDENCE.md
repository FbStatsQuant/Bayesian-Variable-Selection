# Protocol review — evidence (consultant, 2026-11-15)

Source data: `mining/WAVE3.md` (10 Wave 3 tickets, 124 review launches) and `mining/WAVE12.md` (22 Wave 1/1C/2
tickets, ≈195 launches), both mined by Opus helpers from dispositions and review files; plus my own reading of
`Wave3/HQ_DECISIONS.md` (cited `HQD:<line>`), `WATCHDOG.md`, `PIPELINE_REVIEW/`, `API_AUDIT/*/TRIAGE.md`,
`INFRA/registry/events.log`, `INFRA/reviews/`, `INFRA/LIFECYCLE.md`. Table ids such as `W3:T3#2` point into the mining
files, which carry the file:line pointers.

**How to read the counts.** REAL = the finding changed a statement, a hypothesis, a proof step or a status label.
COS = wording, notation, record, citations, or the numerics package. The REAL/COS split is the helpers' call per
disposition row; rows they marked "≈" are estimates. Treat totals as ±15%. The qualitative pattern does not depend on
that margin. Nothing here was re-derived mathematically; I did not re-check any proof.

## 1. Yield per layer (question 1)

| layer | reviews (W1–2 / W3) | findings, as labelled | REAL | COS | what it caught that nothing earlier did | verdict |
|---|---|---|---|---|---|---|
| statement lock | 26 / 16 | W1–2: ≈137 required, 5 REJECT. W3: 6 C, 14 M, ≈50 other | ≈130 / ≈56 | ≈7 / ≈15 | a false claim or counterexample in ≥ 12 of 22 W1–2 tickets; START 4 CRITICAL, SCR 1 BLOCKER (`W12:T1` aggregate; `W3:T1`) | **best yield per review** |
| lemma line checks (incl. break reviews) | ≈73 / 30 | W1–2: ≈23 "failed as written", ≈40 M. W3: 2 C, 12 M, 61 m | ≈210 / ≈52 | ≈110 / ≈34 | most proof corrections; every lemma counterexample came from a reviewer (`W12` summary 2–3) | **earns its cost** |
| lead's falsification numerics | every ticket | – | 0 lemmas refuted in 32 tickets | – | statement changes came only from boundary / end-to-end numerics: POST item 5, START [G1], SCR-A°, W1-N3 code deviation (`W3:T1` numerics note; `W12:T1` W1-N3) | **noise as a per-lemma duty**: reviewers found defects in the numerics themselves in 8 of 10 W3 tickets; all 5 MAJORs of the W1-N1 sweep were numerics |
| mid-point | 19 / 6 | W1–2: 13 M. W3: 1 M | W1–2: 7 new M; W3: ≈11 minor | 6 M re-raised | 25 of 25 said CONTINUE; 4 tickets that later stopped or stayed PARTIAL had CONTINUE (`W12:T5`) | **never did its own job** (redirect); its finds are line-check finds |
| sweep | 18 / 7 | 0 FATAL anywhere; W1–2: 28 major-level, 156 m. W3: 18 M, 68 m | ≈19 M + ≈70 m / ≈40 | ≈160 / ≈60 | glue errors and text changed after its check: 5 REAL MAJOR on line-checked objects in W3 (`W3:T3#2–6`), ≈10 in W1–2 (`W12:T3`) | **earns its cost**; a third of its MAJORs are numerics/record |
| council | 27 rounds / 16 rounds (≈85 seat-reviews) | 21 MAJOR-level blocking findings; 0 CRITICAL in W3 | ≈25 / ≈34 | ≈150 / ≈104 | see §2 | **round 1 earns its cost; later rounds do not** |
| post-council diff check (PC) | – / 7 | – | 3 (POST2 PC1) + verified 4 + 8 substantive edits in RM, SAMP | record items | the only false proof step known to survive a council pass (`W3:T3#1`; HQD:36) | **earns its cost** (one Sol review) |
| other diff / reconciliation / re-lock checks | – / 20 | – | 4 checks found REAL (START SC3, SC4; SCR R05, R05b) | 16 clean | all 4 followed a substantive statement change; RM2's 9 checks found 0 (`W3:T7`) | useful **only after a statement change** |
| better-theorem + sharpness gate | – / 11 | proposals | proposals adopted in 8 of the 9 tickets that ran it | – | see §5 | **best strength layer** |
| acceptance audit (tools) | – / 5 runs | 5 refusals | 0 mathematical | 5 | 2 claims a seat never examined (RM2 Ex-PolyR/F, HQD:241); 7 post-council edits inside a manifest (HQD:201) | **costs more than it returns in its current form** (§6) |
| blind API audit (batch) | 251 claims, ≈ $64 | 3 GAP, 39 MINOR, 1 wording | 3 GAP (→ SUSPECT) | 40 | all 3 GAPs sit in lemmas that were never line-checked (S5F L0/L1, FAC-X L4r.5); 0 GAP in the 109 council-passed claims and in 92 further claims of the priority tickets (`API_AUDIT/pass1–3/TRIAGE.md`) | cheap, independent confirmation |
| sharpness batch (sharp1/1b) | 25 claims, ≈ $15 + triage | 25/25 "IMPROVABLE-EASY" | 2 class A + residuals → MIS-R, PSHARP, T6, T7 | scale miscalibrated | C-MIS's removable fixed variances (`sharp1/TRIAGE.md:35-36`) | high yield **with triage** |
| daily CI | 4 days | 1 finding | 0 | 6 line-drifted cites (`HQ_NOW.md:21`) | – | low; keep cheap |
| weekly Astra re-audit | 0 runs yet | – | – | – | – | untested |
| watchdog | 8 runs, 8 flags | – | 6 silent-ticket flags, among them the real 8-h P6 stall (HQD:276) | 2 flags and 3 notes "decision in HQ_DECISIONS but not in ticket LOG" | 0 holds ever written (`HOLDS.md`) | keep, drop the duplicate-record check |

## 2. Councils (question 2)

43 rounds over 27 councilled objects (`W12:T2`, `W3:T2`).

| fact | W1–2 | W3 | pointer |
|---|---|---|---|
| objects passing in round 1 | 11 of 17 | 5 of 10 | T2 tables |
| failing seat-reviews | all from the OpenAI seat | 4, all OpenAI seat | Claude Opus seat: 0 gate FAILs in 43 rounds, lowest score 8.3 |
| MAJOR-level blocking findings | 16 | 5 | – |
| … a wrong or unproved step in a theorem or lemma | 2 (C-DLV r1) | 0 | `W12:T2` C-DLV |
| … a false claim in REPORT or summary text only | 4 (FAC-PK, FAC-S5 ×2, FAC-X) | 0 | `W12:T2` |
| … faithfulness (sources, code, chapter transcription) | 7 (FINAL 5, APP 2) | 2 (POST C1) | – |
| … record / wording / labels | 3 | 3 (POST C2 REPORT, RM C1 numerics labels, PSHARP R1 REPORT/registry) | – |
| rounds ≥ 2 that existed because of a mathematical error in the proofs | C-DLV r2, APP r2–r3 (new Lemma ENUM) | **0 of 6** | `W3:T2` "why extra rounds" |
| REAL findings in rounds ≥ 2 | ≈5 | 3 of ≈45 | `W3:T1` |

Observations.
1. **Severity labels do not track substance.** The REAL council catches in W3 were labelled MINOR or non-blocking:
   SAMP C1 opus #2 (Theorem D omits the KERNEL premise), #3 (TR-b proof slip); SCR C1 Opus 1 (κ, b, M fixed missing);
   POST2 C1 B-5 (an unproved inequality, new Lemma E0); RM C2 B1 (`W3:T3` "non-MAJOR but REAL"). The blocking MAJORs
   were REPORT text, labels and literature wording.
2. **The unverified fix is the dangerous step.** Fixes for those "minor" items went in after the vote with the
   disposition saying "no claim changed" (RM, SAMP, POST2: HQD:20–41; SCR v3.4 never checked: `W3:T4`). One of them
   put a false inequality into POST2 D(b) (HQD:36).
3. **About half of all blocking findings concern text that restates results** (REPORT §6, summary rows, registry
   block, chapter transcription): the 4 REPORT-only "correctness" findings, FINAL's 5, APP r1 G2, POST C1 F4, POST C2
   F1, PSHARP R1 M1. The locked STATEMENT was correct in each W3 case (`PSHARP/reviews/R1_disposition.md:3,8`).
4. **The 8.0 score threshold never decided a round.** Every score < 8.0 came with a gate FAIL; gate FAILs also
   occurred at 8.2, 8.3, 8.6, 8.8, 8.8, 8.8 (APP r1, POST C2, FAC-PK r1, APP r2, FAC-X r1, RM C1). Gates decide.
5. **Process-forced rounds.** START R2 was run because acceptance check A4 refused R1's manifest (it listed wave
   documents later edited on main; HQD:133–136). MISR R2 was run because a sweep ordered after the council classed a
   numerics-docstring fix "substantive" (`W3:T2`). PSHARP R2 (two blind seats + reconciliation, 11/11 resolved) fixed
   one dropped hypothesis line in REPORT.

What the proposed rules (MEMO #2, #4) would have changed in W3: POST C2 and C3, RM C2, PSHARP R2 → one diff round
each (same seats, diff only); START R2 and MISR R2 → not run. That is 12 blind seat-reviews and 3 reconciliations
replaced by ≈8 diff reads. In W1–2: FAC-PK r2, FAC-S5 r2, FAC-X r2 (REPORT text) and FINAL r2–r3 (restored hypotheses)
→ diff rounds; C-DLV r2 and APP r2 stay full rounds (statement scope changed; new lemma).

## 3. Embedded review (question 3)

30 late slips: REAL MAJOR/CRITICAL findings at sweep or later on an object that had passed an earlier check
(`W12:T3` 22 rows, `W3:T3` 8 rows).

| why the earlier check missed it | W1–2 | W3 | examples |
|---|---|---|---|
| text changed after its last check (repair, assembly, post-lock or post-council edit, transcription, late REPORT text) | 11 | ≈3 | W1-PXN #1, #3, #4 (remark added after council, later false); C-DLV #7–8; FINAL #12–14; POST2 D3; RM L2_NAF |
| object never line-checked | 4 | 0 | W1-GEN L8/SEL; FAC-PK REPORT §6; S5F L0/L1; FAC-X L4r.5 |
| glue: statement copy vs lemma, quantifiers, scope narrower than the downstream use | 0 + (in "other") | ≈5 | RM2 §3 vs examples; START OVL, (B-R) vs (E); SAMP PC; SCR M3 |
| cross-ticket reuse | 4 | 0 | C-DLV × C-GROW cap; APP enumeration branch (raised in C-GROW first) |
| other | 3 | 0 | – |

- **Is the per-lemma chain applied consistently?** Mostly. Exceptions: lemmas added late and checked only by the sweep
  (W1-GEN L8, SEL); re-checks "folded into the sweep" (C-DLV L1 v2); checks launched before the lemmas they depend on
  had passed (C-GROW, FAC-S5: `W12:T6` last paragraph); C-PACK item checks before the lock.
- **Did a refuted lemma ever poison dependents unnoticed?** No. In W3 no lemma was refuted after dependents were
  written; every change was a repair or a strengthening and got a re-check (`W3:T6`). In W1–2 the ≈23 failed lemmas
  were repaired the same day (`W12:T6`). The cases where dependents were *not* re-checked are edits, not refutations:
  SAMP's PC changed at the sweep while D/LT/C/TR consume it (council found the mismatch); RM2 L0–L3 "written for v1.3"
  after the statement moved to v1.4; W2-UNI's corollary changed with consumer FAC-A not re-checked.
- **Judgement on DEPS.** A dependency file with a content hash per object and the hash at its last check would have
  flagged the two largest classes (≈14 "changed after check" + 4 "never checked" = 18 of 30) mechanically, at the
  moment of the edit. It would not catch glue errors; the sweep does. RM2 already kept hand-made copies
  (`reviews/as_reviewed_by_LC2/`, `…_MP1/`, `…_SW1/`, `…_R1/`) and 12 manifests to answer the same question.
- **Judgement on "no lemma consumed before its line check".** Not supported as an ordering rule: the record has no
  case it would have prevented, and the fast tickets ran proofs and checks in parallel (MISR: lock to council R2 in under
  6 h of LOG time). The rule the record supports is a gate at the freeze: nothing stale or unchecked under a claim when the sweep
  or council manifest is frozen.

## 4. Trace and rollback (question 4)

- **Lifecycle operations actually used** (`INFRA/registry/events.log`, action column): suspect 4, patch 1, clear 6,
  narrow 4. Never used since seeding: retract, deprecate, downgrade, supersede, coexist, promote, re-point,
  rollback-ticket. The one full correctness rollback (POST2 D(b): suspect → repair → PC2 → patch → clear) took one day
  and worked (HQD:36–50).
- **Supersession stalls.** RM-F/R → RM2, C-MIS → MIS-R and START → START2 have waited for the owner since 11-12
  (HQD:249–257). The cause is in HQD:25: all 43 `headline=yes` flags were set by a tool, so every change counts as
  headline-changing.
- **Statement drift cases** (`W3:T4`, `W12:T4`):

| case | direction | flagged at the time? | checked? |
|---|---|---|---|
| SAMP D, TR | weaker (KERNEL premise; abstract targets only) | no: disposition said "no claim changed"; HQ found it at registry, which held a mid-ticket draft (HQD:27–29) | PC1, 2 days later |
| SCR v3.4 | weaker (κ, b, M, σ fixed added after the pass) | no | never |
| POST2 (G2*) | event added after lock | "no hypothesis change" | no separate check |
| RM v1.1 → v1.2 | stronger, by the lead, without an HQ decision | REPORT flag 3 only (`W3-RM/REPORT.md:10-14`) | line checks |
| START v1.3.1–v1.3.3 | three narrowings | yes, in LOG at the time (`W3-START/LOG.md:32`) | SC4, sweep, council |
| C-DLV sweep fix (premise CONFIG) | statement changed after lock | – | not before council → 2 council MAJORs (`W12:T3#8`) |

  A changelog tagged stronger / weaker / equal would have surfaced the first four. "Any weakening = early checkpoint"
  is too broad: START's three narrowings were reviewer-driven repairs within 6 h, and three stop/resume cycles would
  have cost more than they returned. The cases that hurt were weakenings of what the ticket claims (a premise added to
  a main theorem, a claim's scope cut).
- **Restore points.** Rule 9 has HQ commit at every checkpoint and before every review round. On Owls this is now an
  hourly cron (`~/.config/bvs-hq/snap/snapshot_ticket.sh W3-DIST`, minute 17). Read on 2026-11-15 15:56 CST:
  - W3-DIST had LOG, PLAN, STATEMENT, ROUTES, DEPS and reviews on disk and **no snapshot commit yet**
    (`origin/theory/W3-DIST` = HQ's brief commits only). Up to an hour of lead work has no restore point.
  - Commits are named by time, not by event, so a manifest digest cannot be mapped to a restore point.
  - The script is silent on the three failure paths: no log line when nothing changed, `git push … && echo` hides a
    failed push, and cron discards stderr. No `W3-DIST.log` exists, so "not running" and "nothing to do" look the same.
  - `--max-size=5m` drops large files without a note. The lock sits in `/tmp`.
- **LIFECYCLE §3 in practice.** The level table (PATCH … CLEAR) is usable and was used. The git recipe
  (`rollback-ticket`, tombstones, per-claim tags, archive branches) has never run on a real claim. It drew findings in
  every tooling review round (INFRA R01 #3–5, R02 F3, R03 F8, R04 re-point binding, R05 #4: `INFRA/reviews/`).

## 5. Sub-par results (question 5)

| case | what was weak | who found it, when | what would have caught it earlier |
|---|---|---|---|
| Wave 2 factor program | every factor result needs p < n/2; ≈ 2/3 of W2 tickets outside the paper's regime; FAC-S5's exponent 0.104 below FAC-A's 1/6 | strategy review, after the pause (`Wave2/SR/CRITIQUE_fable.md:23-26,137-138,164`). No lock, mid-point or council compared a statement with the binding goals (`W12:T4`) | a CP1 table: target vs PROGRAM goals and vs our own best result. FAC-S5's lead knew the exponent at opening (`W2-FAC-S5/LOG.md:10-14`) |
| C-MIS → MIS-R | "σ², τ² fixed", removable by scale invariance; registry notes already called MIS "narrower than Song–Liang" | sharp1 batch + triage, ≈ 3 days after its council (`sharp1/TRIAGE.md:35-36`). MIS-R then took under 8 h from launch to CP3 (HQD:152, 186) | a literature parity row at CP1 ("variance: fixed vs Song–Liang Thm 4: SHORT — why?"); the lock had noted the y-standardisation (`W12:T4` C-MIS) |
| RM → RM2 | polylogarithmic leakage set | RM's own better-theorem review (P5), same ticket (`W3:T5`) | nothing cheaper: RM2 was real new work with its own key lemma. Correct use of a follow-up |
| START → START2 | 4 cheap restatements (BT2 P1–P4), each "ADOPT NOW" | better-theorem review on the final statement, run in parallel with council R2 (`W3-START/reviews/BT2_disposition.md:8-31`) | run the final better-theorem review **before** the council freeze. The lead declined adoption because it "would discard that round" |
| RM2 BT2 | 5 proposals "ADOPT in v1.5" | BT2, after the council | same; v1.5 was never made (`W3:T5`) |
| POST2 | 4 R03b proposals | BT in parallel with line checks | still `better:PENDING` (HQD:24) |
| PSHARP | open √(log p) question listed in two REPORTs, owned by nobody | sharp1 residuals (`sharp1/TRIAGE.md` rows 11–13) | the wave-boundary sharpness batch (it did) |

Sharpness-gate timing (`W3:T5`): where the better-theorem review finished **before** proving (RM2, START, PSHARP, and
MISR nearly), the target changed at CP1 with no rework. Where it ran in parallel with proving (POST2, RM, SAMP, SCR),
checked lemmas were rewritten: SCR needed three re-lock reviews (10 REAL findings), POST2 re-checked C, D, E1 as v2,
SAMP re-checked C and LT. Boundary numerics changed a statement in POST and START and produced a necessity label
elsewhere; ASSUMPTION_MAP was written in 9 of 10 tickets.

## 6. Complexity (question 6)

| item | size / cost | return in the record |
|---|---|---|
| binding stack | W1 53 + W1C 64 + W2 54 + W3 162 = 333 lines, read as a chain; LIFECYCLE 527 lines | rule 2 has four dated provider amendments; rule 16 is lifted but printed; P6 core-hour rules sit inside the theory protocol |
| acceptance tooling | `INFRA/tools` + `manifest.py` ≈ 8,200 lines; LIFECYCLE §4.1 parser spec ≈ 80 lines (table grammar down to U+2028) | 5 refusals, 0 mathematical. Costs: START council R2 + reconciliation; INFRA fixes R05, R06, R07 with ≈ 8 Sol reviews; 8 seat-addendum threads; RM2 carrier file (HQD:133–136, 161–170, 201–257) |
| reviews of the tooling itself | INFRA R01–R05 + pipeline R01–R04 + fix reviews ≈ 13 rounds | findings were executed on synthetic fixtures. One process finding was confirmed by a real incident: post-council edits (pipeline R01 → POST2 D(b)). Features reviewed repeatedly have 0 real uses (§4) |
| manifests | 32 in 5 tickets (12 each in RM2, START), one per line-check / mid-point / change-check round | the council and sweep manifests carried the value; no finding came from a line-check manifest |
| diff / reconciliation checks between rounds | 20 (excluding PC) | 4 REAL, all after a substantive statement change |
| reconciliation reviewer (rule 15, rounds ≥ 2) | 3 runs | 0 REAL (PSHARP 11/11 resolved) |
| rule 14 "no layer skipped without Felipe" | – | HQ waived the mid-point (MISR, HQD:183) and replaced mid-point + sweep (POST, HQD:3) itself; START2 ran lock + line checks + council only, 6 reviews, 9.1 / 9.1 |
| ticket-LOG copy of HQ decisions | – | 2 of 8 watchdog flags, 3 further notes |
| HOLDS.md read "before every step" | – | 0 holds in the file's life |

## 7. Reviewer families (added 2026-11-15, second pass)

Sources: `mining/SEATS.md` (43 council rounds, both seats on the same frozen content) and `mining/FAMILIES.md` (all
other layers), cited `SEATS:Sn`, `FAM:Fn`. OAI = OpenAI (Sol = gpt-6.1-sol, Astra = gpt-6-astra). Leads were Claude
(Opus or Fable) in all but two tickets.

**The basic limit of this evidence.** Outside councils, OpenAI ran ≈ 211 mathematics reviews and Claude ran 16, of
which 10 were in the two OpenAI-led tickets (`FAM:F1`). The record can say what OpenAI reviewers caught in
Claude-written proofs. It can say very little about what Claude reviewers would have caught in the same place. Only
the council (85 seat-reviews) and three small pairs are real head-to-head comparisons.

### 7.1 Per layer

| layer | reviews OAI / Claude | what OAI caught that Claude missed | what Claude caught that OAI missed | comparison quality |
|---|---|---|---|---|
| statement lock | 35 / 3 | every false claim or counterexample found at the lock of a Claude-led ticket (≥ 12 tickets in W1–2; START 4 CRITICAL, SCR BLOCKER) | at the locks of the two OpenAI-led tickets, Opus found false statements too: FAC-XA (an operator-norm bound), FAC-PKA (four false items) (`FAM:F2#7–8`) | **none direct.** No statement was locked by both. What the record shows is that a lock by the *other family than the author* finds false claims in both directions |
| lemma line check | ≈ 91 / 9 | all ≈ 30 "false as written" verdicts and counterexamples against Claude-written lemmas, almost all by argument, 2 by the reviewer's own script (`FAM:F4`). In two parallel pairs on a Sol-written lemma, Sol found 1 REAL item Opus did not (LOC2 L6) | nothing false in the 4 Sol-written lemmas Opus checked; 3 of them stayed clean in every later layer; on RM2 L6, Opus passed a statement/example mismatch that the Astra sweep then found (`FAM:F2#5`) | **weak.** No Claude reviewer line-checked a Claude-written lemma. The closest evidence is the Fable blind audit (row below) |
| break review | 2 / 0 | START BR1: 2 CRITICAL after two Sol locks (`W3:T3#7`) | – | none |
| sweep | 25 / 0 | 28 of 30 late MAJOR catches came from OAI reviewers | 2 of 30 (Fable audit, in never-checked lemmas) | none direct. **But:** in 21 of the 25 catches that had an earlier pass, the finder was the *same model* that had passed the object, as a fresh agent. In 4 it was Astra after Sol. In 0 it was the other family (`FAM:F3c`). Late catches came from a fresh whole read, not from a change of family |
| whole-chain re-check (W3-POST) | 1 / 1, same brief, parallel | Astra R01: 4 REAL, 2 of them "false as written" | Opus R02: 4 REAL, different ones, none "false as written" | **direct, n = 1.** 2 items shared. Both missed the literature problems the Astra council seat failed later (`FAM:F3a`) |
| better-theorem / strategy | 10 Astra / Fable: 25 sharpness verdicts + the Wave 2 strategy review | Astra changed the target in 8 tickets (§5) | Fable's strategy critique found the Wave 2 regime drift; the Fable sharpness batch found C-MIS's removable variances. Triage found no wrong proposal in the steps checked (`sharp1/TRIAGE.md` §0) | no direct pair; both families have a good record here |
| blind audit of finished claims | Sol confirmations only / Fable 251 claims | Sol downgraded 1 of Fable's 4 GAP calls to wording | on 109 claims that had passed OAI line checks and councils: 21 MINOR slips, 10 of 10 sampled are real slips in the text; 0 confirmed GAP. On never-checked lemmas: 3 GAPs, all confirmed by Sol (`FAM:F3b`) | Fable reads Claude-written proofs line by line and finds real gaps where they exist. Its recall is unknown |
| council | 43 / 42 seat-reviews | §7.2 | §7.2 | **direct**: 42 two-seat rounds; in 4 of them files changed while a seat was reading (`SEATS` header) |

"Verified, later overturned" outside councils: Sol 7 of ≈ 184, Astra 1 of 27, Opus 2 of 16 (`FAM:F6`). The Claude
sample is too small to rank the families on this.

### 7.2 Council seats head-to-head (`SEATS:S1–S5`)

| | OpenAI seat | Claude (Opus) seat |
|---|---|---|
| gate FAILs in 43 rounds | 12 | 0 |
| findings per review | ≈ 2.2–2.6 | ≈ 7.8–8.3 |
| REAL findings unique to the seat | 25 (+2), **20 of them blocking** | 42, **none blocking** (2 MAJOR "non-gate", 26 MINOR, 13 NIT or unlabelled) |
| … by class | REPORT or summary text 9, chapter transcription 5, literature 4, labels 3, code 2, proof steps 2 | statement or hypothesis text 17, labels 11, transcription 5, proof steps 4, code 2, REPORT 3 |
| on the other seat's finds | passed the object explicitly in 19 of Opus's 41 rows (e.g. SAMP "Checked 19 = 16 + 3", where 19 holds only for B = 16) | on OpenAI's 23 same-content blocking items: same point 3 (2 at lower severity), a neighbouring point 12, nothing 8; passed the failed gate every time |
| REAL findings raised by both | 5 | 5 (the OpenAI seat graded 4 of them higher) |
| lead rejected with evidence | 0 | 1 |
| a suggestion that led to an error | 0 | 4: three applied after the vote without a check (W1-PXN #8 false sentence; POST2 B-5 repair written with a false line; FINAL r3 addition), one rejected before use |
| mentions of re-deriving a step, per review (rough) | 2.0–2.5 | 4.5–7.2 |

Reading, with the "Claude seat never failed a gate" fact as one input:
1. **The seats are complementary, not redundant.** Each explicitly passed objects in which the other found a real
   defect. The OpenAI seat finds mismatches between derived text and the statement, literature claims, and the coded
   branch. The Opus seat finds missing premises and scope slips in statement text.
2. **The Opus seat reads closely and grades leniently.** It found more REAL items per review than the OpenAI seat
   (≈ 0.8 vs 0.6 in W1–2; 1.6 vs 0.8 in W3) and never turned one into a gate FAIL, even a theorem missing a premise.
   So in the record the gate has been enforced by the OpenAI seat alone. Replacing that seat with an Opus seat under
   the old brief would have passed all 12 failing rounds.
3. **Whether this is the model or the brief is not known.** The old brief asks for a score and gates. v4 asks each
   seat to tag findings by class, and any correctness, strength or faithfulness finding blocks. The seat test
   (MEMO #11) is built to separate the two.
4. **Both seats passed a real error once** in content they saw (MISR R1, a necessity label, caught by the sweep on
   the same manifest). The blind audit found no gap in council-passed claims.
5. **Sol and Astra fail the gate at the same rate** (28% vs 27%, `SEATS:S6`). Astra found 4 late errors after a Sol
   pass (`FAM:F3c`); Sol found new bypasses after three Astra rounds on the tools (`FAM:F3d`). The record does not
   show one dominating the other.

### 7.3 Fresh sessions

- **No review in the record continued an earlier reviewer session** (`FAM:F5`). Every statement below about
  continuing a session is a judgement, not a finding.
- **A fresh whole read is what catches late errors** (21 of 25, same model, new agent: §7.1 sweep row).
- **Narrow re-checks of repairs are the weak step, fresh or not.** Of 13 repairs re-checked by a fresh agent of the
  finder's model, 6 later had an error in or next to the repair. In 2 the error was in an object edited in the same
  repair round and not re-checked (FAC-S5 L3), or in a row elsewhere that the repair made stale (START (B-R)); a
  later whole read found each (`FAM:F5`, last table). The three final-stage repairs (POST2 PC2, SAMP PC2, PSHARP R2)
  had no later error.
- **Relaxed blindness has one data point.** The seat addenda of 11-12 (same seat model, fresh thread, own earlier
  review, frozen manifest): 98 ACCEPT and 2 NOT-EXAMINED in 9 addenda, no reversal (`FAM:F5`).

### 7.4 OpenAI reviews per ticket in the record (`FAM:F1`)

| ticket kind | OpenAI launches, mean (range) | Sol / Astra | Claude launches |
|---|---|---|---|
| full chain, Wave 3 (RM, RM2, START, SAMP, SCR, POST2) | 13.3 (9–20) | 8.8 / 4.5 | 1–3 |
| full chain, Waves 1–2 (16 tickets) | 9.0 (5–17) | almost all Sol | 1–3 |
| small rider (START2, MISR, PSHARP, POST) | 6.25 (5–8) | 4.25 / 2.0 | 1–4 |

Where the Wave 3 OpenAI reviews went (all 10 tickets, 105 reviews, `FAM:F1`): lock and re-lock 14, line checks 26,
break reviews 2, mid-point 6, sweep 7, better-theorem 10, diff / change / reconciliation / post-council checks 24,
council seats 16. The diff-type checks are the largest avoidable block: outside the post-council checks, 16 of 20
found nothing (§1).

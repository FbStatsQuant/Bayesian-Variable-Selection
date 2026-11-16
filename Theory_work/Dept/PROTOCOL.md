# SMC - Theory Department — protocol variant (DRAFT for HQ approval, POLICIES §13; 2026-11-15)

Baseline: `Theory_work/Wave3/PROTOCOL_v4.md` (H1–H6) and `Theory_work/INFRA/LIFECYCLE.md`. This file lists **only the
deviations**, each with its reason and the decision that introduced it (`DECISIONS.md` D-number). Until HQ approves a
row, the baseline applies to it. Every later change to this file goes to HQ before use.

## A. Company minimums kept (not negotiable; how this department meets them)
| minimum | how |
|---|---|
| independent review before "checked" | every lemma line-checked by a blind reviewer of the other family (Sol/Astra) per v4 §2A NORMAL; council with an OpenAI seat; no "checked" without a review file |
| restore points + rollback path | per-ticket snapshot cron every 15 min (commit-in-place, RP labels on CHECKPOINT/MANIFEST); parent folders read-only (A-1) so recorded claims never move under a running ticket; LIFECYCLE §3 for rollbacks after merge |
| decision log | `Theory_work/Dept/DECISIONS.md` (department), HQ_DECISIONS for CP3 / headline; each ticket's LOG |
| honest labels | statuses verbatim; "conditional on …" carried (W3-11); STATEMENT changelog tags confirmed by a reviewer; narrowed readings sent to Writing before the chapter cites them |
| escalation | counterexample, WEAKER target clause, blocked dependency, anything touching a headline → HQ at once (POLICIES §2–§4) |
| compute discipline | POLICIES §12: temp under `/home/fb31/bvs_tmp/theory/…`, `nice`, ≤ 16 cores, no NOTS from tickets, no swarming |

## B. Deviations from the baseline
| # | deviation | baseline | why | decision |
|---|---|---|---|---|
| B1 | **Rider tickets are new folders `<PARENT>-R` with a delta STATEMENT** over the parent's recorded version; the parent folder is read-only while recorded. New claim ids get `implies` edges; supersession by H5 card. | v4 §1 assumes one folder per ticket; nothing forbids editing a recorded ticket's files | parent STATEMENT / lemma / CHECKPOINT lines are hashed in the registry (sha256, status_sha256, check C12); editing them breaks recorded claims and v4 principle 2 | D1 (HQ approved) |
| B2 | **No Astra better-theorem review at a rider's CP1** when its targets come from a blind API sharpness audit (sharp1/1b/2/3) | v4 §2A: better-theorem review for Tier B "if the statement is new" | the sharpness audit is itself a fresh strong reviewer asked only for strictly better statements; saves Codex for DIST and line checks | D3 |
| B3 | **"better:" strength gate for headline candidates** = the blind API sharpness verdict + its triage disposition where one exists; an API Fable sharpness batch (HQ's credits) for uncovered rows | LIFECYCLE §4.2(c): one fresh reviewer (Astra, or Claude at effort high) per gate | same reviewer type and blindness; no Codex; cheaper; every proposal still gets a recorded disposition | D17 (HQ approved, API route by HQ) |
| B4 | **A council's Sol seat may double as the fresh fidelity read** when its brief asks for an explicit `FIDELITY: FAITHFUL / NOT-FAITHFUL` line on the reader statements | H5 card 5 condition (i)(a): a separate fresh Sol fidelity read | the seat is fresh and blind on the frozen manifest, which is exactly the fidelity read's input | D28 (HQ approved) |
| B5 | **One Sol review may cover two scopes** (e.g. new bridges + the diff since the last fidelity read) | v4: a new agent per review | both scopes are small and on the same files; the review file states both scopes; blind first reads (§2A) are never merged | D26 |
| B6 | **Errata in parent files consumed by running riders are CHAPTER-ONLY** until the riders' CP3; then one in-place editorial batch (one Sol "editorial only" diff check) | v4 §5.3: E findings applied later in one batch (no rule on consumed files) | an in-place edit would make rider DEPS rows STALE and drift their frozen manifests | D19 |
| B7 | **Audit findings that may touch a statement get an independent adjudication** (fresh Opus, blind to the triage) before any LIFECYCLE §3 operation; NARROW items run as one priced batch after the freeze; headline-candidate rows via H5 | LIFECYCLE §3 starts from a finding; no adjudication step specified | separates "looks statement-level" from real narrowing before touching the registry; avoids piecemeal registry churn during a freeze week | D27, D31 (HQ approved) |
| B8 | **Recorder tasks are staged as dry runs by the department; HQ approves every real run**; clones in `bvs_tmp`, one at a time | RECORD_BRIEF: HQ runs or delegates recording | handover of the recorder to the department (owner, 11-15); HQ keeps the gate | D12, D29 |
| B9 | **Checkpoint files continue the parent's integer numbering only inside new folders** (`CHECKPOINT_1.md`, `CHECKPOINT_3.md`); never `CHECKPOINT_R1` | — (tool convention) | registry tools read only `CHECKPOINT_<digit>.md` | D1 / RIDER_RULES |
| B11 | **Diff checks of citation-only or wording-only changes may be done by a fresh Opus reviewer** (not Codex) when the change touches no mathematical text; the reviewer must confirm, line by line, the same cited content | v4 §2A: statement-change / diff checks by an OpenAI reviewer | citation re-points have no mathematical content; saves Codex for line checks and councils | HQ 11-15 (C-MIS manifest drift) |
| B10 | **Sweep duties of Tier B tickets go into the council briefs** (no separate sweep) — as v4 §2 already allows for Tier B; stated here so the briefs carry the named duties | v4 §2 | — (clarification) | RIDER_RULES §3 |

## C. Operating rules this department adds (not deviations; stricter than baseline)
- **Manifest-impact check before any merge (HQ, 11-15, after the citefix incident):** before an edit to any file is
  merged, grep **every** `MANIFEST_*` and `INPUTS*` in the repo (accepted tickets included) and every running ticket's
  DEPS/STATEMENT for that file. If an accepted manifest lists it, the edit needs an impact plan first (diff check +
  re-frozen manifest with seat carriers, or defer). If a running ticket consumes it, route CHAPTER-ONLY until that
  ticket's CP3 (B6).
- **Never move one claim's status source off a council CHECKPOINT_<k>.md** (11-15 incident, f526e45b): LIFECYCLE §4.1
  requires the checkpoint to carry every id both seats accepted, so removing one breaks A4 for every row it sources.
  A status change for a council-sourced row goes into a NEW full checkpoint (verbatim copy of all status lines, the one
  line changed), then correct-status all rows to it and re-record.
- **Implication lemmas record their target in `implies`, never in `depends_on`** (HQ 11-15, Cont-F/R): a lemma that
  proves A ⇒ B lists B as the implication's target and is cited as the evidence of the `implies` edge; B is not an input.
- Timestamps only from `date` (two leads mis-stamped on 11-15).
- Codex order W3-DIST > riders > the rest; any review queued > 2 h is reported to HQ.
- Leads are child agents of the department thread (POLICIES §10); never cancelled; settled when finished.
- A rider reads `HOLDS.md` on `origin/main` at each checkpoint and before each freeze.

## D. Open for HQ
- Approve B1–B11 (B1, B3, B4, B7, B11 already approved in substance; listed for the record).

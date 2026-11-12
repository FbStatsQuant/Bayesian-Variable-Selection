# R03 reconciliation — independent Sol review

**Verdict: NOT-READY.** The original six toolfix2 reproductions are blocked, but acceptance still has a CRITICAL review-content binding gap and MAJOR assurance, disposition-evidence, transaction-durability and independent-containment gaps.

Reviewed `e46d9dcaca522bc213ab2102938141a71dd27e0f`, the actual main HEAD when this review started, rather than assuming the brief's `d6da494`. `git diff d6da494 HEAD -- Theory_work/INFRA/tools Theory_work/Wave3/PROTOCOL.md Theory_work/Wave3/tools/manifest.py --stat` produced no output: the relevant implementations are unchanged between those commits. The original repository's git state was not changed. Only this report was written there. No agents, cluster actions, notifications or schedule changes were made.

## Execution and evidence conventions

All destructive fixtures, fault injections and test git operations ran in a disposable clone, never in the original checkout. Scratch root **T** = `C:/Users/felip/AppData/Local/Temp/bvs-r03-a09b93b45027434d8436c6a9ddbe3d7a`; clone **S** = `T/repo`. Setup: `git clone --no-hardlinks --quiet . <S>` from the original checkout. The regression suite creates its own sandbox/worktree in the scratch clone's git database.

Commands executed, with complete fixture definitions and stdout/stderr retained outside the repository:

- **SUITE**: from S, `python -B Theory_work/INFRA/tools/test_lifecycle.py`; output `T/suite.log`. **103 PASS, 0 FAIL; Python exit 0 captured.** Intentional failed-restore stderr includes ROLLBACK FAILED / REGISTRY LOCKED; these are successful fault-injection scenarios, not suite failures. Scenario implementations were read, including the conditional, case-folding, evidence, parser, rollback and recovery cases; the result is not inferred from fix notes.
- **P**: `python -B <T>/probes.py <S>`; exit 0; output `T/probes.log`.
- **M**: `python -u -B <T>/more.py <S>`; exit 0; output `T/more.log`. Run P before M on a fresh clone. The scripts print the exact subprocess arguments and return codes. The scripts themselves returning 0 is not a claim that their attempted acceptance checks were refused: successful bypasses are called out below.
- **TASKS**: read-only `list_scheduled_tasks({})`, inspected actual enabled tasks and prompts, rather than inferring their existence from HQ notes.

Paths/line numbers below refer to the reviewed source. `SUITE: PASS <scenario>` denotes the printed result of the exact SUITE command above. Multiple rows intentionally overlap because the brief requests independent verdicts on several earlier inventories. RESOLVED refers to the specified failure; it does not certify mathematical correctness or all possible variants.

## Finding-by-finding reconciliation

| ID / original finding | Original severity | Verdict | Reproduction evidence and residual |
|---|---|---|---|
| Astra F1 — ack clears over invalid premise | CRITICAL | RESOLVED | SUITE: PASS `F1 clear refused while an input is SUSPECT, even with an ack`, PASS `F1 acceptance of the dependent refused`, and PASS on the transitive `@proof` case. `check.py:437` calls `invalid_inputs`; direct stmt/proof uses cannot be waived with acks. Conditional `@hyp` has separate explicit treatment. |
| Astra F2 — nonexistent evidence / unchecked intermediate | MAJOR | PARTIAL | SUITE rejects four nonexistent headline evidence paths and a directly accepted non-headline without council/correctness evidence. P independently gives `--acceptance R03:W`: exit 1, A1-correct + A4-council; **`--acceptance R03:Y`: exit 0, PASS**, although Y consumes that W. M extends W to use a PARTIAL leaf and Y still passes. N1 below. |
| Astra F3 — staged ingest omits acceptance | MAJOR | RESOLVED | SUITE: PASS `F3 --staged runs --acceptance on the ingested ids: A1 ERRORs printed, exit 1, live untouched`. `ingest.py:633`–`:666` computes new IDs and runs staged A checks. P also actually exercises this path (its different A2 bypass is N3). |
| Astra F4 — external review inputs mutable | MAJOR | RESOLVED | P: `manifest.py freeze <ticket> <manifest> --extra <ticket>/reviews/INPUTS.txt`, then change the listed external file; `verify` exits 1: `CHANGED EXT:Theory_work/WaveT/R03-external.md`. PROTOCOL:123–128 makes the complete external input inventory and fresh review of substantive premise/code changes mandatory. Inventory completeness remains an HQ/reviewer obligation, not automatic inference from prose. N2 is a separate binding flaw. |
| Astra F5 — forged header accepted | MAJOR | RESOLVED | P replaces header with `MANIFEST ` + 64 zeroes; `manifest.py verify` exits 1: `verify: header digest does not match the stored rows (corrupted or hand-edited manifest)`. |
| Astra F6 — rollback loses dependent premise spans | MAJOR | RESOLVED | SUITE: PASS `F6 rollback-ticket: dependent SUSPECT, its premise span re-read at the archive (provenance)` and PASS `F6 after the revert the final check has no ERROR for the ticket or its dependent`; the scenario actually removes the ticket directory. Proposed-tree check refuses a surviving statement in the removed file. |
| Astra F7 — projected cost permits >1,400 core-hours | CRITICAL | RESOLVED | Current PROTOCOL:79–82 adds admission by **time limit × cores for all queued/running jobs plus already used core-hours**, not smoke projections. Original counterexample, 150 tasks × 22.5 h = 3,375, is now inadmissible even if the smoke predicts 750. The scheduler's per-task limits bound the admitted reservation without HQ. This is a protocol resolution, not a tested cluster controller; no jobs were submitted. Every attempt must count in used cost/reservations. |
| Astra F8 — missing schedules / no independent containment | MAJOR | PARTIAL | TASKS confirms four enabled tasks, IDs matching HQ_DECISIONS:43–48; watchdog/CI/weekly are `freshSession:true`, `boundThreadId:null`. However watchdog explicitly says `Never submit, cancel or modify anything on NOTS`; daily CI says `Do not change the registry or open issues yourself; HQ decides`. All four have `lastRunStatus:never`. Schedule existence is resolved; finding containment still depends on HQ. N5 below. |
| Reconciliation R01 — immutable council content | CRITICAL | PARTIAL | External inventory and corrupt-header failures are blocked (F4/F5); M changes Y's actual statement and rehashes it with a major bump. Current `verify`, `bind` and acceptance all return 0 although both reviews explicitly say that new manifest is NOT REVIEWED and FAIL. N2 is the remaining content/outcome binding failure. |
| Reconciliation R02 — deleted propagation root | CRITICAL | RESOLVED | SUITE rollback/tombstone chain scenarios retain roots and propagate SUSPECT through later dependents; wrong archive is refused; removal of the original statement/tex directory does not break archived tombstones. The narrower dependent-premise case is also exercised under F6. |
| Reconciliation R03 — consumes/bindings/method fields dropped | CRITICAL | RESOLVED | SUITE JSONL/REPORT round-trip scenarios preserve bound consumes, method pins/components and binding rows; graph invalidation follows the bridge; unknown JSON keys are refused without registry mutation. These are real ingestion/propagation operations, not just field-list inspection. |
| Reconciliation R04 — old-registry dry run / partial ingest | MAJOR | RESOLVED | SUITE mixed-invalid-fragment tests refuse both claims and splits without writes; independent `python -B <T>/cycle.py <S>` creates a cyclic fragment and runs `ingest.py claims <ticket>/cycle.jsonl --staged`: exit 1, `NEW ERROR C6-cycle R03:CYCLE1 -> R03:CYCLE2 -> R03:CYCLE1` (`T/cycle.log`); the new-ID acceptance scenario refuses missing gates. The exact earlier zero-space converter loss is blocked (Sol-4 below). Staging and later apply are still separate invocations; the documented audit must use unchanged inputs. |
| Reconciliation R05 — strength bypass | MAJOR | PARTIAL | SUITE rejects empty/contradictory gates, missing evidence and deferred/absent dispositions. **P's staged headline with `better-disposition:P=declined(reviews/DOES_NOT_EXIST.md)` exits 0: `acceptance (R03:D): PASS; 0 acceptance ERROR`.** N3. |
| Reconciliation R06 — ACTIVE launders assurance | MAJOR | PARTIAL | SUITE blocks the exact direct weak-input/incidental-mention cases, requires conditional status and carries declared conditions into descendants. M demonstrates **Y → checked-labelled W → PARTIAL V**, all ACTIVE, unconditional Y: exit 0/PASS. A3 examines only Y's direct input assurance; W's admission was never validated. N1. |
| Reconciliation R07 — stale isolated branch | MAJOR | RESOLVED | SUITE `--consumed-vs` tests compare real committed registry versions: identical ref has no ERROR; changed state and higher major produce R7-consumed ERROR. LIFECYCLE:198–201 requires the command before continuation/merge. `check.py:548` implements direct external consumed-claim comparison. Proof/text/minor changes give WARN and require human proof-use recheck; this is not an automatic transitive source comparison or fetch. |
| Reconciliation R08 — anchoring / unverifiable blind brief | MAJOR | RESOLVED | PROTOCOL:129–139 now requires a saved whole brief before launch, allowed-file list excluding earlier reviews/dispositions/scores, and separate reconciliation. This creates the missing inspectable launch record. No new completed scored blind round is certified here: the tracked Wave3 tree currently has only this review's reconciliation brief matching `BRIEF*`, and no post-rule blind run was executed for this audit. This is a procedural design resolution, not proof of future reviewer compliance or access isolation. |
| Reconciliation R09 — unrepresentative smoke / no cost backstop | MAJOR | RESOLVED | PROTOCOL:72–86 requires representative CP0 smoke approval, CP1 read-back/invariants/timing, then worst-case reservations. HQ_DECISIONS:52–57 restricts P6 leg A to CP0 and **nothing submitted on NOTS**. An absent completed smoke ledger is not a violation at this authorized phase. The earlier 150 × 22.5 h example fails the new admission inequality; no actual cluster admission is certified. |
| Reconciliation R10 — EXHAUSTED labelled PASS | MAJOR | PARTIAL | SUITE refuses explicit low score, FAIL, missing round/digest/review, stale digest and duplicate-seat/file records. But current A4 trusts the cell's PASS/score while only searching review text for the digest (`bvsreg.py:1146`); M's review files explicitly FAIL the current content yet A4 passes. N2. |
| Reconciliation R11 — coordinator-dependent monitoring | MAJOR | PARTIAL | TASKS verifies the schedules actually exist independently; the actual watchdog/CI prompts still authorize reporting only. HQ-unavailable containment remains unresolved (F8 / N5). |
| Sol-1 — multi-file atomicity | MAJOR | PARTIAL | SUITE reproduces failed second replacement AND failed restoration: .TXN_FAILED blocks tools and `recover` restores old files/removes lock. P then kills a writer between replacements: `CRASH EXIT 73 CONTENTS 'new\\n' 'old\\n' LOCK False`; ordinary check exits 0. `replace_all` explicitly excludes process death (`bvsreg.py:244`), while `write_many` still claims all-or-nothing (`:330`). N4. |
| Sol-2 — token mention waives assurance | MAJOR | RESOLVED | SUITE exact `Unlike Lemma Weak, this result assumes nothing.` + `@hyp` + unconditional status is A3 ERROR; no-name and no-@hyp cases also refuse. Affirmative complete conditional status is now additionally required. This fixes the original mechanical token-only waiver; HQ still attests the statement really declares a hypothesis. N1 is a different route around intermediate assurance. |
| Sol-3 — lit FAIL / not-lit PASS | MAJOR | RESOLVED | SUITE rejects contradictory lit PASS/FAIL plus not-lit PASS; complete gate-name parsing in `bvsreg.py:1008`–`:1028` requires the exact name and all its results PASS. A substring `not-lit` cannot satisfy `lit`. |
| Sol-4 — blank/zero-space field truncation | MAJOR | RESOLVED | SUITE: PASS `Sol-4 zero-space field after a blank line kept; unknown field after it reported`; also non-field prose inside a fence errors without ending the block. Sol-R6 exercises the later tilde-fence variant. |
| Sol-5 — tombstone tex requires worktree | MAJOR | RESOLVED | SUITE archives the tombstone tex/statement, removes the source directory and checks without tombstone/tex errors. No live checkout dependency remains for this case. |
| Sol-6 — BVS_STAGE_INFRA widens writes | MAJOR | RESOLVED | SUITE refuses a stage variable naming the repo, and its separate write-guard scenario refuses an outside-INFRA destination. Existing stage marker/link guards remain in `bvsreg.py:49`–`:63`, `:203`–`:224`. |
| Toolfix2 R1 — negated/misplaced/longer condition | CRITICAL | RESOLVED | SUITE tests all THREE original strings: `not conditional on Lemma Weak`; `conditional on Other. Unlike Lemma Weak, no assumption is needed.`; `conditional on Lemma Weak Extra`. Each has A3 ERROR and each clear over SUSPECT fails, including the ack case. This verdict is scoped to those exact breaks. |
| Toolfix2 R2 — one file counts as two reviews | MAJOR | RESOLVED | SUITE malformed-council loop includes both original Windows case variant and pinned/unpinned same path; each gives A4-council. Canonical path identity ignores case on Windows and pin spelling (`bvsreg.py:1142`). |
| Toolfix2 R3 — pinned directory as evidence | MAJOR | RESOLVED | SUITE directly calls resolver and acceptance with pinned trees: refused; pinned blob succeeds. `resolve_evidence` requires `git cat-file -t` result `blob`, not merely object existence. |
| Toolfix2 R4 — later path token escapes | MINOR | RESOLVED | SUITE exercises missing `missing@name.md`, `missing.longextension`, plus pinned file/tree variants; later missing files now produce A1-evidence. `_pathlike` recognizes these tokens. |
| Toolfix2 R5 — rollback map case mismatch | MAJOR | RESOLVED | Windows SUITE actually registers `F6K:Z` in `Theory_work/WaveT/f6c/STATEMENT.md` while the rollback root uses `F6C`; rollback refuses and registry digest stays unchanged. This is the actual survivor scenario, not just a unit test of case folding. |
| Toolfix2 R6 — tilde fence / heading loses fields | MAJOR | RESOLVED | SUITE converter reproduction `~~~ / REGISTRY / claim / blank / # heading / shade:grey / ~~~` returns nonzero and reports both heading and shade. Longer backtick fence also stays open across shorter inner backticks. |
| Astra F9 — published freeze path | MINOR | OPEN | Additional listed finding: from S, `python -B Theory_work/Wave3/tools/manifest.py freeze Theory_work/WaveT/R03 reviews/MANIFEST_R03.txt --extra reviews/INPUTS.txt` fails: `FileNotFoundError ... 'reviews/INPUTS.txt'`. PROTOCOL:124 still uses root-relative `reviews/...`; output has the same cwd problem. Use full repository-relative ticket paths or explicitly `cd` to the ticket. |

## New findings / newly isolated failure mechanisms

### N1 — MAJOR: assurance validation stops at an unchecked checked-labelled intermediate

Locations: `check.py:422` (A checks only named acceptance claims), `:522` (direct strength-3 input trusted), `bvsreg.py:1200`–`:1242` (invalid-state traversal / conditional inheritance do not recursively establish assurance).

Reproduction: execute P then M. P ingests new W and Y through the current ingest tool. W is ACTIVE/PROVED-CHECKED with no council or correctness evidence; Y has two review files and consumes `W@stmt`. Exact commands and outputs:

```
python -B Theory_work/INFRA/tools/check.py --quiet --acceptance R03:W
# exit 1; A1-correct; A4-council; acceptance (R03:W): REFUSED
python -B Theory_work/INFRA/tools/check.py --quiet --acceptance R03:Y
# exit 0; acceptance (R03:Y): PASS; 0 acceptance ERROR, 0 other ERROR
```

M adds ACTIVE/PARTIAL V, then runs:

```
python -B Theory_work/INFRA/tools/registry.py set R03:W depends_on=R03:V@stmt --reason probe
python -B Theory_work/INFRA/tools/check.py --quiet --acceptance R03:Y
# exit 0; 409 claims; 0 ERROR, 185 WARN; unconditional PROVED-CHECKED Y passes
```

Thus A0's transitive ACTIVE check does not provide transitive assurance. This requires an intermediate admitted without passing acceptance (the current `--apply` route permits it), not bypassing both seats' mathematical judgment. It is a mechanical fail-open boundary, not an allegation that any live theorem is false. Validate a durable acceptance identity/version for each new checked premise, or recursively audit assurance with an explicit trusted legacy boundary. Test named acceptance on the leaf consumer, not just on the intermediate.

### N2 — CRITICAL: a mention of the current digest is treated as a passing review of that content

Locations: `manifest.py:94`; `bvsreg.py:1104`–`:1148`; `registry.py:153`–`:169`. Neither binder nor A4 binds a structured **outcome and score** to the digest. This is more specific than the fixed corrupt-header or duplicate-path issues.

M changes the actual second statement line to `Theorem Y. A strictly stronger Y holds for all parameters.`, runs `registry.py rehash R03:Y --bump major --reason "stronger statement fixture"` (v2.0.0), freezes it, and places this in each distinct review file:

```
Scored OLD text: 8.5 PASS.
MANIFEST 33957572014b3a980773cd5871447338fe5e8bb8b5a76f16b39db7575ab10cce: new stronger text NOT REVIEWED; gates FAIL pending review.
```

The council cell cites that new digest and says both seats scored 8.5 PASS. All three mandatory mechanical commands succeed:

```
python -B Theory_work/Wave3/tools/manifest.py verify <ticket> <ticket>/reviews/M.txt
# exit 0: verify: OK MANIFEST 33957572...ab10cce
python -B Theory_work/Wave3/tools/manifest.py bind <ticket>/reviews/M.txt <ticket>/reviews/sol.md <ticket>/reviews/opus.md
# exit 0: bind: OK, 2 review(s) quote MANIFEST 33957572...ab10cce
python -B Theory_work/INFRA/tools/check.py --quiet --acceptance R03:Y
# exit 0: acceptance (R03:Y): PASS; 0 acceptance ERROR, 0 other ERROR
```

P additionally demonstrates that acceptance's council digest can remain the OLD digest while `verify`/`bind` validate a DIFFERENT current digest quoted as unreviewed in the same files. No hash collision or file identity trick is needed. Human enforcement of rule 15 should reject these fixtures; the advertised mechanical checks do not. Preserve the hold on CP3. Require a structured per-review round/digest/score/gates outcome, validate it against the actual manifest and registry record, and reject contradictory current-content outcomes. A digest occurring in a negative sentence must not be a content approval.

### N3 — MAJOR: headline disposition evidence is never resolved

Locations: `check.py:446` validates only entries whose RESULT is exactly PASS; `:479` only tests disposition enum and nonempty evidence. `declined` is not PASS.

P stages a headline with existing correct/lit/necessity reviews, valid council, and:

```
better-proposal:P(reviews/sol.md);
better-disposition:P=declined(reviews/DOES_NOT_EXIST.md)
```

`python -B Theory_work/INFRA/tools/ingest.py claims <ticket>/disposition.jsonl --staged` returns **0**, `409 claims; 0 ERROR`, `acceptance (R03:D): PASS; 0 acceptance ERROR`. The nonexistent disposition replaces the missing better:PASS gate. Validate evidence for every proposal/disposition independently of PASS parsing; add this staged acceptance case.

### N4 — MAJOR: a killed transaction leaves mixed files and no fail-closed marker

Locations: `bvsreg.py:239`–`:280`, `:330`–`:353`. Existing failed-restore handling is a real improvement, but its lock is created only after an exception is caught. There is no prewritten durable in-progress journal.

P's child invokes actual `R.write_many` on two dedicated scratch registry files, each initially `old`. It replaces the first normally, then calls `os._exit(73)` when the second replacement is about to run. This models process termination between those writes, without changing the implementation on disk. Parent output:

```
CRASH EXIT 73 CONTENTS 'new\n' 'old\n' LOCK False
python -B Theory_work/INFRA/tools/check.py --quiet
# exit 0; 408 claims; 0 ERROR
```

The fixture files deliberately are not production claims/events; the check result establishes absence of a global transaction lock, not that arbitrary corrupt claims would pass schema validation. The same replace loop serves claims/bindings/events, so readers can consume a partial production transaction. `replace_all` disclaims killed processes, but clean rollback still needs durable transaction recovery. Write and flush recovery metadata before replacement, block readers until commit/recovery, and make recovery restartable. Do not describe the current implementation as crash-atomic.

### N5 — MAJOR: independently scheduled detection still cannot contain a finding without HQ

This is the remaining F8/R11 mechanism, verified against actual task configuration rather than a hypothesized missing scheduler. `list_scheduled_tasks({})` returns enabled fresh-session watchdog `scheduled-task:e3816541-adbf-4337-901d-3d9e1a36cf1a` and CI `scheduled-task:1ddaffb6-3203-45be-b086-bb1f3cc65280`. The former explicitly forbids cluster modifications and only writes WATCHDOG plus queues HQ; the latter explicitly forbids changing registry or opening issues. Weekly re-audit also says `Change nothing in the registry.` Heartbeat is bound to the HQ thread.

Reproduction is configuration-level: let an independent run find an invalid ACTIVE premise while HQ is unavailable. Follow those prompts exactly: it can report, but cannot quarantine the premise or stop affected consumers. No live scheduled run or failure was induced in this review; all currently report `lastRunStatus:never`. Authorize a narrowly scoped fail-closed quarantine/consumer-stop path with an independent destination/escalation. The new worst-case compute admission rule mitigates the budget part, not this claim-validity part.

## Overall decision

**NOT-READY:** CRITICAL N2 / residual R01 and R10 permits the mechanical acceptance bundle to pass on an unreviewed stronger statement. Open MAJORs: N1 (F2/R06), N3 (R05), N4 (Sol-1), N5 (F8/R11). Open MINOR: F9. The six exact toolfix2 R1–R6 breaks are resolved; they are not being relabelled as still open because a different bypass exists.

This verdict concerns lifting the CP3/tooling hold. It does not assert that the existing mathematics is false, that any scheduled task already failed, or that the authorized P6 CP0 planning itself spends compute.


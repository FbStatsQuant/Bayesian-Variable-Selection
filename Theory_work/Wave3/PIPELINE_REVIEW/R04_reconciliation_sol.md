# R04 reconciliation — independent Sol correctness review

**Overall verdict: READY under the brief's criterion (no open CRITICAL; MAJORs listed).** The specified original reproductions are blocked. Two new **MAJOR** defects remain: **R04-N1**, accepted-input evidence/verdict changes do not invalidate its acceptance record; **R04-N2**, the acceptance fingerprint omits statement-file provenance. READY is not a claim that these defects are harmless, permission to lift rule 16, or a certification of mathematical correctness.

Reviewed actual HEAD `438f63d181d911147424fa4a6da34575a2188a48`, rather than assuming the brief's `0b0906c`. Read-only `git diff 0b0906c HEAD --stat -- Theory_work/INFRA/tools Theory_work/Wave3/tools/manifest.py Theory_work/Wave3/PROTOCOL.md Theory_work/Wave3/HQ_DECISIONS.md` returned no output. The original checkout was initially clean. Only this output file was written in it; no original git state was changed. No subagents, notifications, jobs, schedule edits, or live hold/registry edits were made.

## Reproduction inventory

All fixture execution and git mutation occurred in disposable clones created from the original checkout using `git clone --no-hardlinks --quiet . <destination>`.

Scratch root **T** = `C:/Users/felip/AppData/Local/Temp/bvs-r04-d1d6ed5190454fdabedfa2c9b9595813`.

- **S** = `T/repo`: untouched fixture-source clone for the regression suite. Command: `python -B <S>/Theory_work/INFRA/tools/test_lifecycle.py`; complete output `T/suite.log`. Its own sandbox/worktree belongs to the disposable clone, not the original git database. **Exit 0; 127 PASS, 0 FAIL.**
- **P**: `python -B C:/Users/felip/AppData/Local/Temp/bvs-r03-a09b93b45027434d8436c6a9ddbe3d7a/probes.py <T>/original`; script exit **0**, `T/probes.log`.
- P intentionally kills a transaction. Before M, from that clone, `python -B Theory_work/INFRA/tools/bvsreg.py recover` exited **0**, restored both dedicated files, and printed `recovered 2 file(s) from .TXN_INPROGRESS; journal / lock removed` (`T/recover-original.log`). This recovery is necessary to exercise M independently of P's now-working lock.
- **M**: `python -u -B C:/Users/felip/AppData/Local/Temp/bvs-r03-a09b93b45027434d8436c6a9ddbe3d7a/more.py <T>/original`; script exit **0**, `T/more.log`.
- **F**: `python -B C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/probe.py <T>/toolfix`; script exit **0**, `T/toolfix.log`. This is the exact executable fixture reproduced in R03_toolfix3_review_sol.md. It restores its boundary and recovers its transaction before the additional tests below.
- **B**: `python -u -B <T>/boundary_f9.py <T>/original`; exit **0**, `T/boundary_f9.log`. Tests the corrected freeze command and independent L1 boundary tampering.
- **A**: `python -u -B <T>/adjacent.py <T>/toolfix`; exit **0**, `T/adjacent.log`. Run after F. Exact source remains at that path. Sets up a genuinely accepted W and its consumer Y, then independently removes W's gate evidence and withdraws W's council verdict.
- **R**: `python -u -B <T>/relocate.py <T>`; exit **0**, `T/relocate-clean.log`. Run after A and after copying the ticket's STATEMENT.md to `Theory_work/WaveT/r04-relocated.md` in the disposable toolfix clone. Restores W's original file, records a passing control, then relocates it through registry.py and tests W and Y. `T/relocation.log` is the initial equivalent run; use the clean log for inspection.
- **TASKS**: read-only `list_scheduled_tasks({})`; actual returned prompts retained as `T/tasks.json`. All three independent audit tasks are enabled, `freshSession:true`, `boundThreadId:null`, `lastRunStatus:never`. No task was run or edited.

Script exit 0 means execution completed; each attempted bypass has its own printed command, return code and output. Table commands below run at the corresponding clone's repository root. `I/` abbreviates `Theory_work/INFRA/tools/`, `M.py` abbreviates `Theory_work/Wave3/tools/manifest.py`. Expand these literal prefixes when executing. Full expanded argv and outputs are in the named logs.

## Required reconciliation

| ID | Severity | Verdict | Exact command and observed output (relevant excerpt; exit recorded) |
|---|---|---|---|
| R03 N1: unchecked checked-labelled intermediate | MAJOR | RESOLVED, original failure | P: `python -B I/check.py --quiet --acceptance R03:Y` → **1**, `ERROR A5-accepted ... consumes the checked claim R03:W ... it has no accept event and is not in the legacy boundary`; `acceptance (R03:Y): REFUSED; 5 acceptance ERROR, 0 other ERROR`. M adds PARTIAL V and W→V with the original commands; the same Y command still exits **1** with A5 naming W. F isolates the consumer with valid structured council: `python -B I/check.py --quiet --acceptance SOLFIX3:Y` → **1**, exactly **1 A5-accepted ERROR**, before any record is minted. The old P/M reviews also fail A4 because they lack verdict lines and use M.txt instead of MANIFEST_*.txt; F provides the independent A5 isolation. New adjacent failures are R04-N1/N2 below. |
| R03 N2: digest mention accepted as current-content approval | CRITICAL | RESOLVED, original failure | M's stronger statement, major rehash and fresh freeze: `python -B M.py verify <ticket> <ticket>/reviews/M.txt` → **0**, `verify: OK MANIFEST 063d4758d005058a93261c8800b084231b855b15a26aa496f8413d8e4cfd1c30`; `python -B M.py bind <ticket>/reviews/M.txt <ticket>/reviews/sol.md <ticket>/reviews/opus.md` → **1**, `bind: REFUSED (2 problem(s))`, both `no COUNCIL-VERDICT line ... (a mention of the digest is not a verdict)`. `python -B I/check.py --quiet --acceptance R03:Y` → **1**, A4-council plus A5. Here `<ticket>` is the absolute `T/original/Theory_work/WaveT/R03`. Valid structured verdicts bind and record in A, so blanket refusal is not mistaken for a fix. |
| R03 N3: declined-disposition evidence never resolved | MAJOR | RESOLVED, original failure | P: `python -B I/ingest.py claims <ticket>/disposition.jsonl --staged` → **1**, `acceptance (R03:D): REFUSED; 4 acceptance ERROR`; specifically `ACC ERROR A1-evidence ... gate better-disposition:P=declined: evidence 'reviews/DOES_NOT_EXIST.md' resolves to no file`. Additional A4 errors do not conceal whether this evidence check ran. |
| R03 N4: killed writer leaves unguarded mixed files | MAJOR | RESOLVED, original failure | P's original real write_many fault injection → `CRASH EXIT 73 CONTENTS 'new\n' 'old\n' LOCK False`; its following `python -B I/check.py --quiet` now exits **1**, `REGISTRY LOCKED: .../.TXN_INPROGRESS exists`. The script's `LOCK False` refers to the old `.TXN_FAILED` path, not the new persistent journal. Explicit recover command above exits **0** and restores both files. F separately prints `crash exit 73 journal True`, refuses check and manifest commands, then recovers both files. |
| R03 N5: containment waits for HQ | MAJOR | RESOLVED at protocol/prompt level | Read `PROTOCOL.md` rule 12, `HOLDS.md`, `HQ_DECISIONS.md`; TASKS returns three enabled independent prompts with explicit permission to append to the same absolute main-checkout hold file. Rule 12 requires every lead to read it before each step, stop transitive consumers/P6, checkpoint and end; only HQ appends LIFT after triage. Thus the tasks can contain a finding without a registry mutation or an HQ reply. Exact prompt excerpts and limits below. No synthetic HOLD was written in the live checkout. |
| R03 F9: published freeze command's cwd/path failure | MINOR | RESOLVED | Rule 15 now specifies repository-root cwd and full repository-relative ticket paths. B: `python -B M.py freeze Theory_work/Wave3/R04-F9 Theory_work/Wave3/R04-F9/reviews/MANIFEST_R1.txt --extra Theory_work/Wave3/R04-F9/reviews/INPUTS.txt` → **0**, `MANIFEST 8ad31ce7aac9d02b98d227345fd0cb9c8729a5ab62752b2cb7db33bd306468aa (1 files, 0 extra input(s))`; the matching `verify` command → **0**, `verify: OK MANIFEST 8ad31ce7aac9d02b98d227345fd0cb9c8729a5ab62752b2cb7db33bd306468aa`. Fixture has an existing empty INPUTS.txt and one statement file. |
| Toolfix3 N1.a: filtered acceptance mints event | MAJOR | RESOLVED | F: `python -B I/check.py --quiet --acceptance SOLFIX3:W --only A5 --record` → **2**, `error: --only cannot be combined with --acceptance: the acceptance verdict and --record cover every finding`. Subsequent unfiltered Y acceptance → **1**, A5 says W has no accept event. Thus no forged event was written. |
| Toolfix3 N1.b: boundary chooses a later trusted tag | MAJOR | RESOLVED | F: `python -B I/bvsreg.py legacy-boundary --tag solfix3-unaccepted` → **2**, `error: unrecognized arguments: --tag solfix3-unaccepted`; Y remains refused with A5. B independently edits only the disposable boundary's tag name: `python -B I/check.py --quiet --only L1` → **1**, `ERROR L1-legacy ... names tag 'solfix3-unaccepted'; the legacy boundary is the registry at theory-v2.0-pre only`. A hand-added row produces **1**, `L1-legacy ... 1 row(s) not there (e.g. R03:Y), 0 missing ... boundary is frozen`. Boundary restored after each experiment. |
| Toolfix3 N3.a: malformed non-headline gate hides evidence | MAJOR | RESOLVED | F first runs `python -B I/registry.py set SOLFIX3:Y depends_on= "gates=lit:PENDING(reviews/DOES_NOT_EXIST.md) trailing" --reason "malformed gate fixture"` → **0**; `python -B I/check.py --quiet --acceptance SOLFIX3:Y` → **1**, `ERROR A1-gates ... unparsable gate entry 'lit:PENDING(reviews/DOES_NOT_EXIST.md) trailing'`. Removing only ` trailing` via the fixture's registry command still exits **1**, now `ERROR A1-evidence ... resolves to no file`. |
| Toolfix3 N4.a: manifest CLI works under transaction journal | MINOR | RESOLVED | F's genuine killed transaction: `python -B M.py verify Theory_work/WaveT/SOLFIX3 Theory_work/WaveT/SOLFIX3/reviews/MANIFEST_R1.txt`, `python -B M.py bind Theory_work/WaveT/SOLFIX3/reviews/MANIFEST_R1.txt Theory_work/WaveT/SOLFIX3/reviews/sol.md Theory_work/WaveT/SOLFIX3/reviews/opus.md --council "R1; MANIFEST 25831c280cd740ff3bbc36009245af6bc963a305fc55bf044ec5344686fe8bc0; sol=8.5 PASS(reviews/sol.md); opus=8.5 PASS(reviews/opus.md)"`, and `python -B M.py freeze Theory_work/WaveT/SOLFIX3 Theory_work/WaveT/SOLFIX3/reviews/MANIFEST_LOCKED.txt` each → **1**, `REGISTRY LOCKED: .../.TXN_INPROGRESS exists (an unfinished registry transaction)`. |

### N5 prompt evidence and limits

HQ_DECISIONS.md records the three schedule IDs and says their prompts now append holds; it does **not** actually quote the prompts as the brief suggests. I fetched the real prompts rather than infer them from that assertion:

- Watchdog `scheduled-task:e3816541-adbf-4337-901d-3d9e1a36cf1a`: “if P6 core-hours exceed 1,200, append to C:\\Users\\felip\\Bayesian-Variable-Selection\\Theory_work\\Wave3\\HOLDS.md the line `HOLD P6 <UTC time> watchdog <core-hours used>`”; explicitly allows writes to WATCHDOG.md and HOLDS.md, while NOTS remains read-only.
- Daily CI `scheduled-task:1ddaffb6-3203-45be-b086-bb1f3cc65280`: on check ERROR, failed or timed-out falsification, append `HOLD <claim id> <UTC time> daily-CI <one-line finding>` for each affected ACTIVE claim to that same absolute file; registry writes remain prohibited.
- Weekly re-audit `scheduled-task:e9c81940-591c-4d95-bd6c-8a07e10409d3`: on a CRITICAL or MAJOR reviewer error, append `HOLD <claim id> <UTC time> weekly-reaudit <one-line finding>` to that absolute file.

These are working instructions for an independent writer and cooperating leads, not an OS-enforced stop. The independent tasks have never run; I did not certify actual append/lead-stop execution or arbitrary infrastructure outages. The six-hour watchdog hold stops new submissions; it does not cancel running jobs. The independent worst-case admission ceiling in rule 10 remains the backstop for those jobs. This is sufficient to resolve the original reporting-only authorization gap; no new operational enforcement is claimed.

## New findings

### R04-N1 — MAJOR, OPEN: accepted input's evidence and council outcome can change without invalidating its stamp

Locations: `bvsreg.py:1344` ACCEPT_FIELDS, `:1349` accept_stamp, `:1455–1476` unaccepted_inputs; `check.py:447` acceptance_checks. A5 checks a fingerprint of the registry cell strings. It does not re-resolve the input's gate evidence, re-read its council verdicts, or bind their contents into the stamp. A1/A4 are run only for the claims named in the current acceptance invocation. Reviews are excluded from normal ticket manifest enumeration.

A provides a valid control, without editing acceptance events or forging hashes. In the F clone it clears Y's deliberately missing gate, restores Y→W, gives W its own two valid structured council reviews and `correct:PASS(reviews/w-evidence.md)`, then runs:

```text
python -B I/check.py --quiet --acceptance SOLFIX3:W --record
EXIT 0; acceptance (SOLFIX3:W): PASS; 0 acceptance ERROR, 0 other ERROR
record: accept event written for SOLFIX3:W (v1.0.0 fp:525f9e1b992a6925)
python -B I/check.py --quiet --acceptance SOLFIX3:Y --record
EXIT 0; acceptance (SOLFIX3:Y): PASS; 0 acceptance ERROR, 0 other ERROR
record: accept event written for SOLFIX3:Y (v1.0.0 fp:7c530e1c3a9022ca)
```

**Variant A:** delete only W's `reviews/w-evidence.md` in the disposable clone. A performs this with `ev.unlink()`. Registry rows, W's acceptance stamp, manifest and both council verdicts remain unchanged.

```text
python -B I/check.py --quiet --acceptance SOLFIX3:W --record
EXIT 1; ERROR A1-evidence ... gate correct:PASS: evidence 'reviews/w-evidence.md' resolves to no file
acceptance (SOLFIX3:W): REFUSED; 1 acceptance ERROR, 0 other ERROR
record: nothing recorded (acceptance REFUSED)
python -B I/check.py --quiet --acceptance SOLFIX3:Y --record
EXIT 0; acceptance (SOLFIX3:Y): PASS; 0 acceptance ERROR, 0 other ERROR
record: accept event written for SOLFIX3:Y (v1.0.0 fp:7c530e1c3a9022ca)
```

**Variant B:** restore that evidence, then change only W's sol review's `gates=PASS` to `gates=FAIL`. A does this with `p.write_text(old.replace('gates=PASS','gates=FAIL'))`. Y has separate sol/opus review files, so its own verdicts remain valid.

```text
python -B M.py bind Theory_work/WaveT/SOLFIX3/reviews/MANIFEST_R1.txt Theory_work/WaveT/SOLFIX3/reviews/w-sol.md Theory_work/WaveT/SOLFIX3/reviews/w-opus.md --council "R1; MANIFEST 25831c280cd740ff3bbc36009245af6bc963a305fc55bf044ec5344686fe8bc0; sol=8.5 PASS(reviews/w-sol.md); opus=8.5 PASS(reviews/w-opus.md)"
EXIT 1; NOT BOUND ... verdict gates=FAIL (not all gates PASS); bind: REFUSED (1 problem(s))
python -B I/check.py --quiet --acceptance SOLFIX3:W --record
EXIT 1; ERROR A4-council ... verdict gates=FAIL (not all gates PASS)
acceptance (SOLFIX3:W): REFUSED; 1 acceptance ERROR, 0 other ERROR
record: nothing recorded (acceptance REFUSED)
python -B I/check.py --quiet --acceptance SOLFIX3:Y --record
EXIT 0; acceptance (SOLFIX3:Y): PASS; 0 acceptance ERROR, 0 other ERROR
record: accept event written for SOLFIX3:Y (v1.0.0 fp:7c530e1c3a9022ca)
```

Thus a newly recorded checked consumer rests on an input which currently fails its own acceptance due to missing cited evidence or a withdrawn council outcome. The historical acceptance event is real; the failure is current validation of its supporting artifacts. This is a transitive acceptance/evidence defect, not the original direct digest-mention CRITICAL bypass: Y's own council still approves Y's current manifest. Scope/severity follows the original MAJOR intermediate-assurance/evidence findings.

Fix: revalidate current evidence/outcomes of nonlegacy accepted inputs during acceptance (memoized transitively), or store and validate a complete identity for their supporting artifact contents/existence. Changing or deleting an artifact must make the input unacceptable until a fresh passing acceptance. Add the direct-input-refusal versus consumer-acceptance pair to regression coverage. Merely hashing the council cell does not fix this.

### R04-N2 — MAJOR, OPEN: documented statement relocation leaves an accepted-input record current

Locations: the same ACCEPT_FIELDS/accept_stamp and unaccepted_inputs functions; `registry.py:129` set allows `file`; `bvsreg.py:1226` ticket_dir chooses the statement folder when tickets.tsv has no folder. ACCEPT_FIELDS omits `file` (also `lines`, `premises`, and other provenance fields). `file` is not protected, and changing it does not bump version/hash. Only the file omission is claimed as an independently reproduced defect here.

Fixture R restores W's original file and verifies that W passes and is recorded. A scratch-only copy of STATEMENT.md already exists at `Theory_work/WaveT/r04-relocated.md`, with identical bytes. Then only documented registry/check commands are needed:

```text
python -B I/registry.py set SOLFIX3:W file=Theory_work/WaveT/r04-relocated.md --reason "R04 statement relocation"
EXIT 0
python -B I/check.py --quiet --acceptance SOLFIX3:W --record
EXIT 1
ERROR A4-council ... no Theory_work/WaveT/reviews/MANIFEST_*.txt has the header `MANIFEST 25831c280cd7...`: the council digest must be the round's frozen manifest of this ticket (manifest.py freeze), still present
acceptance (SOLFIX3:W): REFUSED; 1 acceptance ERROR, 0 other ERROR
record: nothing recorded (acceptance REFUSED)
python -B I/check.py --quiet --acceptance SOLFIX3:Y --record
EXIT 0
acceptance (SOLFIX3:Y): PASS; 0 acceptance ERROR, 0 other ERROR
record: accept event written for SOLFIX3:Y (v1.0.0 fp:7c530e1c3a9022ca)
```

The current input fails the manifest/provenance rule, but its old acceptance stamp still matches. This does not make a stronger mathematical statement: the copied text is deliberately identical. It demonstrates a concrete mismatch with the contract that a durable record covers the CURRENT claim and that a changed input must be accepted again. It uses neither a hand-edited event log nor an altered legacy boundary. A separate attempted `registry.py set ... status_source=...` was correctly refused (`field 'status_source' not settable here`) and is **not** a finding.

Fix: include all acceptance-relevant source/provenance and dependency metadata in the acceptance identity, and ensure relevant mutations invalidate it. At minimum, `file` must be included. Validate the effective dependency graph and referenced artifacts, not just selected row strings; expanding row fields alone will not resolve R04-N1. Add a regression for file relocation followed by consumer acceptance.

## Boundary and remaining limits

L1's validator now requires the constant `theory-v2.0-pre`, checks its recorded commit, and recomputes exact boundary rows from that tag. Generation has no alternate-tag argument and refuses an existing file. Independent B and F exercises show that adding a row or substituting the source does not widen acceptance. The full suite additionally exercises a self-consistent boundary derived from a later commit. No documented command-only widening was found. Deliberately replacing git tags plus rewriting the boundary itself would cross the trusted-source boundary and is not a reproduced command-only bypass here.

The reviewed state/assurance traversal still checks transitive non-ACTIVE statement/proof inputs, declared hypotheses and inherited conditions. No additional non-ACTIVE-input route was established. Parser/manifest checks and staged ingest were read alongside the reproductions. Full transitive revalidation of a previously accepted input's evidence is the remaining concrete gap, rather than a claim that A0 itself failed.

Regression result: **127 PASS, 0 FAIL; Python exit 0 captured** for the full SUITE command above. The log's intentional `ROLLBACK FAILED` / `.TXN_FAILED` stderr belongs to successful fault-injection/recovery scenarios; it is not an additional failed scenario. The source clone was never used for the independent probes, so the earlier toolfix3 review's concurrent-source contamination was avoided. Relevant passing scenarios explicitly include the unaccepted/transitive intermediate, ordinary acceptance recording, stale record, filtered-record refusal, added legacy row, self-consistent alternate legacy source, missing disposition evidence, malformed non-headline entry, verdict grammar/outcomes and coverage, journal-present CLI refusal, interrupted recovery and normal transaction cleanup. These tests do not cover the two new failures reproduced independently above.

No concurrent-writer race, system-power-loss test, cluster job, mathematical re-proof, or executed scheduled hold/lead-stop simulation is certified. The original CP3 hold remains a separate HQ decision. The two new MAJOR findings above remain open even if the existing regression suite passes.

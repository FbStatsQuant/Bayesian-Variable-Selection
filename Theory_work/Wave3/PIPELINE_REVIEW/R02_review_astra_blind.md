# Independent adversarial pipeline review

Reviewed main at `eb1f9daa6bcea5e7d75168ec3cfaedcbd26e597d`. Read no other PIPELINE_REVIEW file. No subagents, live registry writes, cluster actions, or git state changes. Experiments used a tracked-file copy and copied git database at `C:/Users/felip/AppData/Local/Temp/bvs-r02-xgrx0nme`, excluding PIPELINE_REVIEW before copying. Synthetic registry rows below are fixtures, not allegations about existing theorem statements.

Baseline scratch `check.py --quiet`: exit 0, 406 claims, 0 ERROR, 184 WARN, 217 INFO; `registry.py stats`: all 406 ACTIVE. Exercised ingest, check, registry, propagate, bvsreg (through imports and tools), and manifest. Did not run test_lifecycle.py: it creates a git worktree, which would exceed this review's no-git-state-change constraint. No assertion here depends on live scheduler or cluster access.

Rule 16 currently forbids CP3 ingest/merge and propagation apply on claims introduced by merged tickets until the tool fixes are merged and reviewed. That hold must remain. Tool bypasses below describe what can happen when the hold is lifted or a coordinator mistakes a passing tool result for the complete gate; they are not a claim that rule 16 authorizes those actions today.

## F1 ? CRITICAL: an acknowledgment restores acceptance while a premise remains invalid

**Locations:** `Theory_work/INFRA/tools/check.py:150`, `:410`, `:454-458`; `Theory_work/INFRA/tools/propagate.py:629-633`. Conflicts with `Theory_work/Wave3/PROTOCOL.md:84-87`.

**Failure:** SUSPECT changes lifecycle state without changing the old PROVED-CHECKED status. C4 exempts an input listed in `acks`; CLEAR has the same exemption. Acceptance checks the candidate's ACTIVE state but skips an upstream claim whose status strength is 3 without checking that input's state. Thus an ordinary acknowledgment can bypass the newer rule that consumed claims must be ACTIVE.

**Executed:** created checked X and checked Y depending on X; `suspect X --apply` made both SUSPECT; `registry.py set Y acks=X --reason ...`; `clear Y --apply`; `check.py --acceptance Y` returned PASS, exit 0, zero errors, while X remained SUSPECT. There was no hypothesis declaration or proof repair. The same stale-status mechanism applies to a retracted checked premise. A wrong upstream proof can therefore return to an accepted downstream result.

**Smallest fix:** in acceptance, require every consumed claim to be ACTIVE independently of status and acknowledgments. For Wave 3, refuse CLEAR over non-ACTIVE inputs unless the dependency is actually removed/replaced or the allowed conditional-result treatment is explicitly recorded and audited; an ack alone must not suffice.

## F2 ? MAJOR: nonexistent evidence satisfies headline gates; intermediate correctness is not gated

**Locations:** `Theory_work/INFRA/tools/bvsreg.py:894-900`; `Theory_work/INFRA/tools/check.py:421-450`, `:195-209`.

**Failure:** passed_gates requires only nonempty evidence text. C9 inspects the separate `evidence` column, not the references inside `gates`, and missing evidence there is only WARN. Headline acceptance can therefore accept fabricated or mistyped review paths. For non-headlines, the entire A1 correctness check is skipped with the strength checks, although only strength is supposed to be optional. A worker can self-label a lemma checked, supply no council evidence, and introduce an input that later checked descendants treat as fully assured.

**Executed:** ingested a fixture headline with each of `correct`, `lit`, `necessity`, `better` set to `PASS(does-not-exist.md)`, no council and no review evidence. Staged ingestion and `check.py --acceptance TEST:X` both returned exit 0 with zero errors and zero warnings. This is enough for a sub-par theorem to appear mechanically strength-approved, without any literature or better-theorem review file existing.

**Smallest fix:** require resolvable, immutable evidence references for all required gates, and require correctness evidence for every accepted checked claim regardless of headline status. Validate that council evidence records both scores/gates and the reviewed digest; keep mathematical adequacy as a reviewer/HQ judgment.

## F3 ? MAJOR: staged ingestion does not run the acceptance checks required at CP3

**Locations:** `Theory_work/INFRA/tools/ingest.py:613-631`; `Theory_work/INFRA/tools/bvsreg.py:799-812`; `Theory_work/Wave3/PROTOCOL.md:57-59`.

**Failure:** `--staged` runs check.py without `--acceptance` and discards the stage. There is no CLI option to supply the newly ingested claims for acceptance on that stage. Following the advertised staged-then-apply workflow can write inadmissible rows before the acceptance refusal appears. A coordinator using the printed zero-error staged result and ordinary post-apply check can label/merge them; this violates the intended gate but is precisely the automation gap the gate should catch.

**Executed:** a checked headline with empty gates yielded `--staged` exit 0, 0 ERROR; apply succeeded. Explicit `check.py --acceptance TEST:NOGATES` then failed with four A1 errors. Ordinary consistency checking was not a substitute.

**Smallest fix:** let staged ingestion pass all incoming claim IDs to acceptance, or add a required CP3 acceptance option and use it in the exact documented command. Apply only the staged artifact that passed, and repeat acceptance after apply.

## F4 ? MAJOR: the frozen manifest does not freeze the sources on which the proof depends

**Locations:** `Theory_work/Wave3/tools/manifest.py:12-24`; `Theory_work/Wave3/PROTOCOL.md:54-56`, `:119-129`; `Theory_work/INFRA/tools/bvsreg.py:452-464`.

**Failure:** only files inside the ticket are hashed. External proof files, source code and imported premises remain mutable outside that manifest. Two seats can quote the identical digest while reading different upstream sources. During the later main merge, an upstream proof-only edit can leave statement hashes and ticket bytes unchanged; the current-state comparison alone does not establish that both seats examined the same source version. Even a detected upstream version change has no explicit rule here requiring re-review of the dependent argument before acceptance.

**Executed:** froze a ticket whose statement references an external source, changed only that source, and verified the ticket: exit 0, identical digest. This is not cryptographic breakage; the relevant input was never included.

**Smallest fix:** add the exact imported source spans/files and code pins to the review manifest, or record an immutable repository commit and make reviewers read all external inputs at it. On proposed-merge audit, require dependent re-review for changed consumed inputs.

## F5 ? MAJOR: verify trusts the displayed manifest digest without validating it

**Location:** `Theory_work/Wave3/tools/manifest.py:37-45`.

**Failure:** verify compares file rows but neither recomputes their recorded digest nor compares the first line with a trusted reviewer-quoted value. A mistaken overwrite of the per-file rows can preserve an earlier digest label; verification then certifies new content under an old review identity. This defeats the purpose of reviewers quoting the digest.

**Executed:** replaced the first line of an otherwise valid manifest with `MANIFEST ` followed by 64 zeroes. Verify printed `verify: OK MANIFEST 000...000`, exit 0. Updating file hashes while preserving a prior header exploits the same unchecked association.

**Smallest fix:** validate header format and compare it with the recomputed digest of the recorded rows, then compare the verified digest with the immutable review-round digest. Reject malformed/duplicate rows as well.

## F6 ? MAJOR: the documented rollback can pass staging and then fail its mandatory final check

**Locations:** `Theory_work/INFRA/LIFECYCLE.md:138-150`; `Theory_work/INFRA/tools/propagate.py:267-277`; `Theory_work/INFRA/tools/check.py:100-121`; `Theory_work/INFRA/tools/bvsreg.py:373-377`.

**Failure:** rollback-ticket validates before reverting non-registry files. Only RETRACTED/DEPRECATED rows read archived source text. A later dependent becomes SUSPECT but still hashes its premise spans from the working tree. If its premise is a span in the removed ticket, final check raises C2-hash even though the original claim's tombstone verifies. The published recipe promises no new ERROR but has no executable treatment for this dependency. It cannot finish the rollback cleanly without an unplanned edit to the dependent's provenance.

**Executed:** rollback-ticket with archive HEAD succeeded, zero new errors, original X RETRACTED and dependent Y SUSPECT. With Y's own statement kept in a separate surviving file and its hashed premise in X's file, removing X's file caused final check to exit 1: `a premise span is unreadable`. Restoring the file returned check to zero errors. The scratch removal models the relevant effect of the documented revert; no git revert was run.

**Smallest fix:** before reverting, retain the required premise text for affected dependents in an immutable archive-backed location and update their provenance without clearing SUSPECT. Extend the rollback check to the proposed post-revert tree, not only the pre-revert registry stage.

## F7 ? CRITICAL: projected batches do not enforce the 1,400 core-hour ceiling

**Locations:** `Theory_work/Wave3/PROTOCOL.md:73-81`, `:101-107`; `Theory_work/Wave3/W3-P6/DESIGN.md:20-22`, `:80-82`; `Theory_work/Pause_2026-11/RESUME_PLAN.md:124-136`.

**Failure:** admission is based on smoke-measured/projected time, while already released tasks may run for 22.5 hours each; stopping further releases does not cancel them. At the allowed concurrency of 150 one-core tasks, just one batch can consume 3,375 core-hours. For example, a 5-hour smoke estimate admits 150 tasks for 750 projected core-hours; slow production seeds taking 10 hours consume 1,500, before counting smoke. The design expressly anticipates calibration escalation, unknown long-cell costs and resource limits. A compliant agent can exceed the ceiling without queuing another batch. Required Slurm retries also need budget reservations; the current wording supplies none. The six-hour watchdog reports an overrun after it occurs, potentially after another 900 core-hours at full concurrency.

**Smallest fix:** before release reserve the scheduler-enforced maximum cost of each queued/running task plus actual completed cost and retries against 1,400. Reduce batch size/time limits to fit the remaining allowance. Use a cluster-enforced aggregate cap if available; otherwise a cancellation controller must include bounded accounting lag in its reservation. Charge failed, cancelled and smoke attempts too. An alert is not enforcement.

## F8 ? MAJOR: independent supervision is specified but not recorded, and cannot contain a finding without HQ

**Locations:** `Theory_work/Wave3/PROTOCOL.md:90-107`, `:108-112`; `Theory_work/Wave3/HQ_DECISIONS.md:9-41`; `Theory_work/INFRA/ci/README.md:33-42`.

**Failure:** rule 12 requires heartbeat, watchdog and CI task IDs/next-run times before launch. The complete HQ decision log at this HEAD records none. This establishes missing launch evidence, not proof that no external task exists. Moreover, the watchdog only writes alerts to HQ and WATCHDOG.md; the daily CI prompt explicitly says not to change the registry. If HQ disappears after CP1 releases compute or while another proof is between checkpoints, neither scheduled path quarantines a newly disputed ACTIVE input, notifies/stops its consumers, or cancels compute. Proof leads do stop at their next checkpoint under rule 10, but that does not contain already running work or pending cluster tasks.

**Smallest fix:** block launch until the required independently runnable task IDs and next runs are recorded and verified. Give the watchdog/CI a narrowly authorized fail-closed action: record the suspect claim, notify and stop affected running consumers/releases, and trigger the budget controller when HQ does not acknowledge within the stated deadline. Reserve resumption/acceptance decisions for HQ.

## F9 ? MINOR: the published freeze command resolves the output in the wrong directory

**Locations:** `Theory_work/Wave3/PROTOCOL.md:119-121`; `Theory_work/Wave3/tools/manifest.py:31-35`.

**Failure:** the documented repo-root command passes `reviews/MANIFEST_<round>.txt` as output, but freeze opens that path relative to the process working directory, not the ticket. It fails if root reviews/ does not exist, or stores the freeze outside the ticket review directory if it does. This invites improvised, inconsistent checkpoint artifacts.

**Smallest fix:** document a full ticket-relative repository path for OUT, or deliberately resolve OUT against TICKET_DIR and create its parent directory.

## Worked-example consequences

`W3-POST2/reviews/PC1_postcouncil_diff_sol.md:22,44-48` demonstrates the actual false post-council cutoff inequality, including the admissible `4 <= 2` counterexample. Its line 7 limits the reconstruction to identifiable changes because byte-for-byte snapshots are unavailable. `W3-SAMP/reviews/PC1_postcouncil_diff_sol.md:23,30,52` distinguishes verified mathematics from the unsupported assertion that the two original votes reviewed the final text. These are concrete reasons to require complete, digest-authenticated source freezes and acceptance evidence, rather than inferring a current-text approval from old scores or a disposition. I do not treat the new resume rules as retroactively binding those old council runs, and I do not assert that the now-repaired D(b) theorem is false.

The no-CP3 interim hold is still necessary. A successful consistency audit alone is not a release criterion for this pipeline.

Verdict: NOT-READY
Score: 3/10

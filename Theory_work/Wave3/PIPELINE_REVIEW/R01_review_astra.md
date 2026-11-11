# Adversarial pipeline review R01 — Astra

Scope: all four inherited protocols, LIFECYCLE, CI README, PROGRAM, HQ_DECISIONS, RESUME_PLAN, and W3-RM LOG/REPORT/reviews. Targeted implementation inspection covered ingest.py, check.py and propagate.py; P6 DESIGN was checked for existing safeguards. This reviews the pipeline, not the truth of RM's theorems. No git changes, experiments, or lifecycle mutations were performed. Observations and hypothetical failure scenarios are distinguished below.

## R01 — CRITICAL: council approval is not bound to immutable reviewed content

**Locations:** `Theory_work/Wave3/W3-RM/reviews/C2_disposition.md:8`, `:13`, `:19`; `Theory_work/Wave3/PROTOCOL.md:48`; `Theory_work/INFRA/LIFECYCLE.md:30`, `:229`.

**Evidence and scenario:** RM's disposition records edits after the pass, including rewriting an argument by cases, and statement/map edits while seat B was reviewing. Thus seat A can approve version A, seat B version B, and the final package contain a further mistaken repair, while both scores are counted in the same round. Registry hashes cover statement/premise spans, not the complete proof/review snapshot; version coverage is a human attestation. A quantifier error introduced as an editorial correction can survive citecheck and acquire PROVED-CHECKED without either seat checking the final proof. The observed edits demonstrate exposure, not that RM is false.

**Smallest fix:** freeze a commit or full content manifest before each council, covering statements, proofs, premises and code pins; record it in both replies and compare it at CP3. Never edit under a running council. Subsequent substantive changes require fresh review of the change and consequences; editorial-only changes require an independently attested diff.

## R02 — CRITICAL: merge rollback can remove the claim needed for propagation

**Locations:** `Theory_work/INFRA/LIFECYCLE.md:122`; `Theory_work/Wave3/PROTOCOL.md:39`; `Theory_work/INFRA/tools/propagate.py:224`, `:230`, `:236`.

**Scenario:** ticket A introduces claim A and its registry row; later B depends on A. HQ prices a retraction on the current graph, then reverts A's merge as instructed. Even with a clean git resolution, A's row and source files can disappear while B survives. Applying `propagate.py retract A` now fails: `need()` resolves current registry IDs only and exits on unknown IDs. The dry-run report is not an executable saved plan. `check.py` sees a dangling dependency. A merge commit makes a code revert expressible; it does not preserve the dependency graph required by the prescribed next step.

**Smallest fix:** retain withdrawn claims and source evidence as tombstones. Apply propagation on the current graph, revert ticket changes while explicitly retaining/restoring lifecycle rows and archived evidence, then check the combined PR. Document this sequence for a newly introduced claim with later dependents, or add an atomic rollback operation consuming a saved graph snapshot.

## R03 — CRITICAL: ingestion drops bridge bindings and method pins

**Locations:** `Theory_work/INFRA/tools/ingest.py:65`, `:78`; `Theory_work/INFRA/templates/ASSUMPTION_MAP.md:27`, `:32`; `Theory_work/INFRA/LIFECYCLE.md:61`, `:241`.

**Evidence and scenario:** `ingest_claims()` copies a fixed field list plus selected strength fields; it does not import `consumes`, `method_commit`, `method_components`, or binding-map rows. A theorem supplying `consumes: P:X@B` can rely on LIFECYCLE's automatic proof-use edge instead of duplicating it in `depends_on`. Ingestion loses that binding. If bridge B is wrong, propagation misses this theorem, which can remain usable in the paper. Imported `method` is not a method pin, so code-drift auditing can also have no input to compare.

**Smallest fix:** round-trip the supported registry schema, persist bound consumes/method pins/binding rows, and reject unknown supplied fields. Require explicit dependency edges until fixed. Add a fixture proving that an ingested bridge consumer becomes SUSPECT when its bridge does.

## R04 — MAJOR: CP3's dry-run check validates the old registry

**Locations:** `Theory_work/Wave3/PROTOCOL.md:50`, `:54`; `Theory_work/INFRA/templates/ASSUMPTION_MAP.md:23`; `Theory_work/INFRA/tools/ingest.py:55`, `:109`, `:113`, `:116`.

**Evidence and scenario:** the REPORT template is a REGISTRY block, but ingest reads JSONL; the conversion step is unspecified. Dry run writes nothing, so the subsequent `check.py` validates existing rows, not proposed ones. Moreover, `ingest_claims --apply` writes accepted rows even when `problems` is nonempty, unlike `ingest_splits`; reported dry-run problems do not produce a failure exit. A duplicate or invalid row can be omitted while another accepted row references it or an unknown ID. HQ has a clean old-registry check followed by a partial ingestion rather than a validated transaction.

**Smallest fix:** specify extraction to JSONL, reject the entire transaction on any problem with a nonzero exit, and check the proposed registry in memory or a disposable staged copy. Require the staged report and a post-apply check before labeling/merging.

## R05 — MAJOR: the strength gate does not block acceptance

**Locations:** `Theory_work/INFRA/LIFECYCLE.md:134`, `:142`, `:149`; `Theory_work/Wave3/PROTOCOL.md:19`, `:43`, `:48`; `Theory_work/INFRA/tools/check.py:288`.

**Scenario:** RM2 returns a correct theorem with an avoidable exponent restriction. The better-theorem reviewer proposes a credible strengthening; HQ defers it and continues CP1. CP3 does not require lit/necessity/better PASS or a resolution of that proposal. Missing strength gates are INFO in check.py, so even `--strict` does not block them. A correct but dominated theorem can become a final headline despite LIFECYCLE requiring both gates and defining better:PASS as no credible better statement. RM's retained improvement proposals illustrate why a correctness council score cannot substitute for this decision.

**Smallest fix:** explicitly require strength acceptance for headline admission at CP3 and make missing gates blocking there. Useful checked intermediate results can remain, with headline-strength acceptance pending. Require evidence-backed disposition of each credible improvement and repeat the comparison after substantial statement changes.

## R06 — MAJOR: ACTIVE is mistaken for adequate assurance

**Locations:** `Theory_work/Wave3/PROTOCOL.md:53`, `:57`; `Theory_work/INFRA/LIFECYCLE.md:39`, `:47`; `Theory_work/INFRA/tools/check.py:119`; `Theory_work/INFRA/tools/ingest.py:40`.

**Scenario:** an author-only or PARTIAL inherited lemma is ACTIVE. A downstream ticket invokes it as proved, copies its source status verbatim, and labels its own result PROVED-CHECKED. The ACTIVE check passes; C5 produces only WARN for weak inputs and INFO for author-level inputs. Zero ERROR is still achieved. Local councils can thus launder an unproved premise into checked descendants without changing the source label. The council's qualitative adequate-status gate is the only barrier; the mechanical acceptance gate does not enforce assurance dependencies.

**Smallest fix:** check assurance as well as lifecycle validity for every dependency. Explicitly conditional results may consume open premises, but must retain those premises in their statements and generated statuses. Make unexplained assurance escalation a CP3 error, not a warning waivable by a generic acknowledgement.

## R07 — MAJOR: isolated tickets can accept stale validity states

**Locations:** `Theory_work/Wave3/PROTOCOL.md:37`, `:53`, `:57`; `Theory_work/INFRA/LIFECYCLE.md:114`.

**Scenario:** RM2 branches while RM is ACTIVE. A later audit marks RM SUSPECT on main, but RM2's worktree still contains ACTIVE and its lead has not received the finding. It passes branch-local CP3. If RM2 does not edit RM's row, git can merge without a conflict. There is no explicit requirement for a latest-main dependency/version check or validation of the proposed merged registry. Creating a repair issue does not guarantee delivery to every running consumer.

**Smallest fix:** compare consumed claim states/versions with current main before every continuation and merge. On invalidation, HQ must stop/notify all running consumers and record acknowledgements. Run the acceptance check against the proposed merged tree.

## R08 — MAJOR: fresh reviewers are exposed to previous verdicts

**Locations:** `Theory_work/Wave3/W3-RM/reviews/COUNCIL_BRIEF_R2.md:17`, `:54`; `Theory_work/Wave1C/PROTOCOL.md:31`; `Theory_work/INFRA/LIFECYCLE.md:229`.

**Evidence and scenario:** the round-two brief permits earlier reviews/dispositions, supplies both earlier scores, and directs verification of prior findings. A fresh delegate context is therefore not a blind first reading. Both seats can anchor on the earlier diagnosis that numerical labeling was the only blocker and inherit an incorrect interpretation of an asymptotic step. Different model families do not remove this information coupling.

**Smallest fix:** save a sealed first-pass review of the frozen statement/proof and necessary sources, without previous verdicts or dispositions. Expose earlier findings only in a subsequent reconciliation pass, separately from the independent score.

## R09 — MAJOR: cheap smoke tasks can unlock an uncosted expensive batch

**Locations:** `Theory_work/Wave3/PROTOCOL.md:55`; `Theory_work/Pause_2026-11/RESUME_PLAN.md:124`, `:126`, `:134`; `Theory_work/Wave3/W3-P6/DESIGN.md:56`, `:67`, `:80`.

**Scenario:** the first at-most-20 resumed tasks are n=50 remainder tasks and pass timing/output checks. HQ releases b2, although the expensive n=100, p=1000 regime lacks a completed timing probe. The resume plan also says to resubmit the remainder and b2 together, allowing hundreds of jobs to be queued before the smoke decision. At 22.5 hours per fit, 240 tasks allow 5,400 core-hours versus roughly 1,240 estimated. Existing seed retention, concurrency limits, and per-fit guards do not bound aggregate spending or make the smoke sample representative.

**Smallest fix:** explicitly supersede simultaneous resubmission with an unsent/held remainder. Specify a small representative smoke manifest covering both driver versions and high-cost calibration regimes. Release measured, budgeted batches under an aggregate core-hour ceiling; projected overruns return to HQ before further launch. Distinguish invariant failures from expected resource-limit outcomes.

## R10 — MAJOR: failed council rounds fall through to council-pass labeling

**Locations:** `Theory_work/Wave3/PROTOCOL.md:48`, `:54`, `:71`; `Theory_work/Wave1C/PROTOCOL.md:35`; `Theory_work/INFRA/LIFECYCLE.md:258`.

**Scenario:** a ticket exhausts three rounds with a failed correctness gate. It enters CP3 as instructed and satisfies the listed registry/citation/mechanical checks. The next sentence unconditionally says to apply labels, add council-pass and merge. Rule 14 permits reporting as-is or narrowing but does not distinguish this branch in the acceptance procedure. HQ following a condensed checklist can confuse administrative acceptance with mathematical approval.

**Smallest fix:** split CP3 into PASS and EXHAUSTED. Only a manifest-matched dual pass receives council-pass or PROVED-CHECKED. Exhausted results retain actual status and may be archived without that label. A narrowed theorem must satisfy the applicable gates on its new statement.

## R11 — MAJOR: the monitor depends on the coordinator whose failure it cannot detect

**Locations:** `Theory_work/Wave3/PROTOCOL.md:40`, `:62`, `:65`; `Theory_work/INFRA/ci/README.md:15`, `:33`, `:38`; `Theory_work/Wave3/HQ_DECISIONS.md:3`.

**Scenario:** HQ restarts or loses context after launching P6 and proof tickets. Leads continue to their next checkpoints and cluster jobs keep spending, but HQ's three-hour LOG inspection never happens. Daily and weekly audits are obligations assigned to the same HQ; CI schedules nothing itself. Launch does not require durable schedule IDs, next-run evidence, or missed-HQ escalation. HQ also dispositions reviews and labels results, with precedent for replacing review layers, so a missed gate lacks a separate completion check. This is a failure path, not evidence that schedules are currently absent.

**Smallest fix:** require recorded durable heartbeat/audit task IDs and next-run times before launch, with missed-HQ escalation to the owner. Bind checkpoint decisions to checkpoint commits. Require explicit owner approval for review-layer waivers. Aggregate compute limits must continue to hold while HQ is unavailable.

## Overall verdict

**NOT-READY — 3/10.** Close the immutable-review, rollback/ingestion, staged-acceptance and compute-release gaps before today's expensive or dependency-producing tickets proceed. This score assesses protection against false acceptance and failed propagation, not the truth of existing theorems.

Adversarial review of R02 tool fixes

Six breaks reproduced. Both protected checkouts were left untouched; all mutations and commits were in a fresh scratch clone. No subagents were used.

Scratch: `C:/Users/felip/AppData/Local/Temp/bvs-sol-review-82c2c1a1d0394f5c99f724c976e6b519`.

Setup executed:
```powershell
git clone --no-hardlinks C:/Users/felip/Bayesian-Variable-Selection <scratch>
git -C <scratch> checkout --detach 5ed086c
git -C <scratch> apply --whitespace=nowarn C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/r02_fix.diff
# From scratch:
git add Theory_work/INFRA
git -c user.name=Reviewer -c user.email=review@example.invalid commit -m 'Scratch R02 review baseline'
python -B Theory_work/INFRA/tools/check.py --quiet
python -B Theory_work/INFRA/tools/test_lifecycle.py > suite.log 2>&1
python -B probe_sol.py > probes.log 2>&1
python -u -B probe_more.py > more.log 2>&1
python -u -B probe_conditions.py > conditions.log 2>&1
```

The three probe scripts contain the complete executable fixtures, subprocess commands, fault injection, restoration, and printed outputs. Run them in the order above on a freshly prepared scratch clone. Copies are beside this report: [probe_sol.py](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probe_sol.py), [probe_more.py](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probe_more.py), [probe_conditions.py](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probe_conditions.py). They restore the original working claims rows after probing; their scratch commits and other fixture artifacts are intentionally retained.

**CONFIRMED breaks**

1. **CRITICAL — F1 / R06: negated or unrelated conditional text waives a weak/non-ACTIVE hypothesis.**

   Fixture: `SOL:W`, name `Lemma Weak`, PARTIAL; Y names it in its hashed statement and depends on `SOL:W@hyp`. Y has a valid two-file council. Its source-backed status is:
   ```text
   PROVED-CHECKED not conditional on Lemma Weak
   ```
   With W ACTIVE, `check.py --quiet --acceptance SOL:Y` returns 0:
   ```text
   INFO A3-assurance ... its status is conditional on it ('Lemma Weak')
   check.py: 408 claims; 0 ERROR, 185 WARN, 219 INFO
   acceptance (SOL:Y): PASS; 0 acceptance ERROR, 0 other ERROR
   ```
   Then set W and Y SUSPECT, give each a state_reason, and give Y `acks=SOL:W`. Executed:
   ```text
   propagate.py clear SOL:Y --reason probe --apply
   ```
   It returns 0 and makes Y ACTIVE. Acceptance again returns 0 / PASS / 0 ERROR while W remains SUSPECT. The ack removes routine C4 noise; it does not account for the missing A0/A3 refusal.

   Also reproduced with both:
   ```text
   PROVED-CHECKED conditional on Other. Unlike Lemma Weak, no assumption is needed.
   PROVED-CHECKED conditional on Lemma Weak Extra
   ```
   Each passed acceptance and clear. Exact fixture and output: [probe_conditions.py](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probe_conditions.py), [conditions.log](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/conditions.log).

   Smallest fix: replace substring searching in `conditional_on` with an affirmative clause parser. Reject negation, stop at sentence/clause boundaries, and resolve complete condition names/IDs rather than a shorter name inside another name.

2. **MAJOR — R10: the same review file counts as two reviews.**

   Only one review file is used by these two entries; it contains the required digest:
   ```text
   sol=8 PASS(Theory_work/WaveT/SOL/sol.md)
   opus=8 PASS(Theory_work/WaveT/SOL/SOL.md)
   ```
   On this Windows filesystem both paths open the same file. The full record has one R1 and one MANIFEST. Executing acceptance returns:
   ```text
   check.py: 407 claims; 0 ERROR, 184 WARN, 218 INFO
   acceptance (SOL:Y): PASS; 0 acceptance ERROR, 0 other ERROR
   ```
   Reproduced independently with one entry unpinned and the other `sol.md@3af8d811017273c1ae03049c57b537b503b7fbe2`, pointing to the committed identical file. The comparison key `(path, pin)` treats these as distinct.

   Exact fixture: council-identity loop in [probe_sol.py](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probe_sol.py); output: [probes.log](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probes.log).

   Smallest fix: compare canonical repository file identity, case-normalized on Windows, independently of pin spelling. Reject two seats citing the same repository path even if one is pinned.

3. **MAJOR — F2: a pinned directory is accepted as gate evidence.**

   Y has a valid council and this gate:
   ```text
   correct:PASS(Theory_work@3af8d811017273c1ae03049c57b537b503b7fbe2)
   ```
   `Theory_work` is a directory/tree, not a file. Acceptance returns 0 / PASS / 0 ERROR (407 claims). Exact probe: first evidence-loop case in [probe_sol.py](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probe_sol.py); [probes.log](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probes.log).

   Smallest fix: after resolving a pinned object, require its Git object type to be `blob`; `git cat-file -e` alone accepts trees.

4. **MINOR — F2: later path-like evidence tokens escape validation.**

   These gates each passed acceptance with 0 ERROR, despite the second reference being nonexistent:
   ```text
   correct:PASS(Theory_work/WaveT/SOL/sol.md missing@name.md)
   correct:PASS(Theory_work/WaveT/SOL/sol.md missing.longextension)
   ```
   A later nonexistent absolute Windows path also passed. The first reference exists. `_PATHLIKE` excludes @ in filenames, extensions longer than five characters, and drive-letter paths, so those later tokens disappear from validation.

   Exact full Windows path, fixture, and outputs: evidence loop in [probe_sol.py](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probe_sol.py), [probes.log](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probes.log).

   Smallest fix: use an explicit list grammar for evidence references, or broaden path-token recognition without the extension-length/drive-letter exclusions; reject ambiguous references instead of silently ignoring them.

5. **MAJOR — F6: case differences bypass the proposed post-revert tree on Windows.**

   Exact fixture in [probe_more.py](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probe_more.py):
   ```text
   F6SOL:X file=Theory_work/WaveT/F6SOL/STATEMENT.md lines=1-1
   F6SURV:Y file=Theory_work/WaveT/f6sol/STATEMENT.md lines=2-2
   F6SURV:Y depends_on=F6SOL:X
   ```
   Both paths read the same physical file. Normal check before rollback: 0 ERROR. Executed:
   ```text
   propagate.py rollback-ticket F6SOL --archive 93debb3f639b819a6e9d74242025cd11781926ad --reason "case probe" --apply
   ```
   Return code 0; output:
   ```text
   Staged check.py: 408 claims; 0 ERROR
   Post-revert check.py ... 1 file(s) ... removed
   further ERROR after the revert: 0
   written: 6 file(s)
   ```
   The probe then unlinks that ticket file, simulating the file removal produced by its revert. Executed `check.py --only C2`:
   ```text
   ERROR C2-hash F6SURV:Y statement file missing: 'Theory_work/WaveT/f6sol/STATEMENT.md'
   check.py: 408 claims; 1 ERROR, 0 WARN, 0 INFO
   ```
   Full output: [more.log](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/more.log). This was the no-`--merge` path; the failure was demonstrated by actual file removal, rather than running a Git revert.

   Smallest fix: normalize case consistently for post-revert map insertion/lookups and premise matching on Windows, while retaining Git's actual path spelling for Git reads.

6. **MAJOR — Sol-4: valid tilde fences silently lose fields after a heading.**

   Executed `ingest.py convert Theory_work/WaveT/SOL/heading.md` on:
   ```text
   ~~~
   REGISTRY
   claim: T:X | kind: theorem | statement: STATEMENT.md:1-1

   # heading
   shade:grey
   ~~~
   ```
   It returns 0, emits a claim JSON object, and reports no problem for either the heading or unknown shade. Its parser recognizes only backtick fences, so this valid Markdown fenced block is treated as unfenced and silently ends at the heading. Output JSON lacks any indication of the dropped fields.

   Exact fixture/output: convert `heading` case in [probe_sol.py](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probe_sol.py), [probes.log](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/probes.log).

   Smallest fix: track Markdown fence character and opening length for both backticks and tildes; apply strict in-block field validation until the matching closing fence.

**Things tried that held**

- **F1:** local `W@stmt`, mixed `SOL:W@hyp; W@stmt`, and proof uses over an acknowledged SUSPECT input all produced A0-inputs and refused clear. A bound bridge `consumes=P:X@SOL:W` also produced A0-inputs. A two-node cycle was rejected by C6. The suite's transitive proof-input checks passed.
- **F2:** a nonexistent later `../outside.md` produced A1-evidence. The suite rejected missing first evidence files, non-headline checked claims without correctness evidence, and pins predating the evidence file.
- **R10:** case-duplicated seat names `sol/SOL`, score 10.5, and duplicate paths containing `./` were refused. Scores `8` and `08.0` passed numerically, as expected. The suite rejected failed/low-score seats, missing/stale review files, missing MANIFEST, and legacy free text.
- **F3:** staged ingestion of a checked headline with empty gates returned 1 and printed six acceptance ERRORs including A1-gates, A1-correct, and A4-council.
- **R06:** the suite rejected the original incidental-mention waiver and unconditional descendants, including when accepting their conditional ancestor; correctly carried conditions passed. The bypass in finding 1 remains.
- **R07:** a consumed direct input SUSPECT and v2.0.0 at the comparison ref yielded two R7-consumed ERRORs. Identical registries passed in the suite. Also observed: for Z -> Y -> X across three tickets, checking Z's ticket did not flag X's remote change. I do not count that as a confirmed contract violation because R07 does not explicitly specify transitive comparison.
- **F6:** the suite preserved archived premise spans after file removal and refused a surviving same-spelling statement in the removed ticket file. My modified-file probe with `--merge` preserved a changed premise at its archive and gave 0 ERROR after restoring the old file content. That additional probe used a single-parent commit as the `--merge` argument; it exercised the changed-file map, not merge-conflict behavior.
- **Sol-1:** injected second replacement failure plus failed first restore produced .TXN_FAILED and retained the backup. check, registry, ingest, assemble, and build_registry refused even `--help`. An already-imported module's `safe_dest` and `write_many` also refused. Recovery restored both files to old contents and removed the lock. Direct reads through an already-imported library remain possible; no writing/tool bypass was confirmed.
- **Sol-4:** zero-space `gates:` survived a blank line and unknown shade was reported. A heading inside backtick fences was reported without dropping following gates. A second REGISTRY inside a fence started another block, and its incomplete claim was refused.

**Regression results**

Normal checking before and after probes:
```text
check.py: 406 claims; 0 ERROR, 184 WARN, 217 INFO
```

The regression suite printed **94 PASS, 0 FAIL**, including every pipeline-review-R02 scenario. [suite.log](C:/Users/felip/AppData/Local/Temp/claude/23449ccee6efcb2b/3c61ae05-c4e8-45f3-8978-b1b58ad8eb89/scratchpad/suite.log) retains the complete output. Its intentional fault injection prints ROLLBACK FAILED / REGISTRY LOCKED on stderr; PowerShell rendered that as NativeCommandError and the shell tool reported exit 1 despite all scenario results passing. I do not claim a separately captured Python exit code.

Initial conditional probes had unrelated hash/lifecycle errors; those are not used as evidence of successful acceptance. Finding 1 uses the corrected, fully passing fixtures in conditions.log.

Verdict: NOT-READY


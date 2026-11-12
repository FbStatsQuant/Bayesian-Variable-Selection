# R03 toolfix3 — independent correctness review

**Verdict: NOT-READY for N1–N4.** N2 is RESOLVED in the exercised cases. N1 has two MAJOR bypasses; N3 has a MAJOR malformed-entry bypass for non-headlines; N4 has a MINOR missing guard on the manifest command. The original reproductions are covered by the regression suite; the defects below are adjacent inputs.

Reviewed the uncommitted tools in the specified checkout (base 0ae2044). No checkout files or git state were changed. All fixture writes, commits, tags, crashes and recovery ran in `C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/repo`. No agents, schedules or external services were used.

## Reproduction setup and evidence

The exact executed fixture is [probe.py](C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/probe.py), reproduced in full in the appendix. Its complete command lines, return codes, stdout and stderr are in [probe.log](C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/probe.log). Run it once against a fresh clone. It exercises the findings sequentially and resets the acceptance event / boundary between the two independent N1 bypasses.

PowerShell setup (choose an unused destination):

```powershell
$src = 'C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-e7bb0808-e49e4642c11fe733'
$dst = Join-Path $env:TEMP ('bvs-toolfix3-repro-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory $dst | Out-Null
git clone --no-hardlinks --quiet $src "$dst/repo"
git -C "$dst/repo" fetch --quiet --tags $src
$files = @(
 'Theory_work/INFRA/tools/bvsreg.py',
 'Theory_work/INFRA/tools/check.py',
 'Theory_work/INFRA/tools/ingest.py',
 'Theory_work/Wave3/tools/manifest.py',
 'Theory_work/INFRA/tools/test_lifecycle.py',
 'Theory_work/INFRA/LIFECYCLE.md',
 'Theory_work/INFRA/LEGACY_ACCEPTED.tsv',
 'Theory_work/INFRA/templates/COUNCIL_BRIEF.md'
)
foreach ($f in $files) { Copy-Item -LiteralPath "$src/$f" -Destination "$dst/repo/$f" }
python -B C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/probe.py "$dst/repo"
```

The clone's git commit identity is supplied per command by the fixture; no global git configuration is needed. The fixture's `solfix3-unaccepted` tag is new and leaves `theory-v2.0-pre` unchanged.

## N1 — DEFECT

### N1.a — MAJOR: output filtering can mint an acceptance event after failed acceptance

Location: `check.py:674–704`. `run()` computes all findings, but `--only` then discards findings before `counts` controls the printed verdict, event recording and exit status. The new durable acceptance writer trusts this filtered count. A claim without any council can therefore get a current, tool-written acceptance stamp. Its consumer then passes an ordinary unfiltered acceptance check.

Exact fixture: appendix / probe.py, section `N1 FILTERED RECORD BYPASS`. W is ACTIVE and PROVED-CHECKED, with no correctness gate or council; Y depends on W@stmt and has a current manifest and two valid council verdicts.

Commands and observed output (from scratch repo):

```text
python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:W
EXIT 1
ERROR A1-correct ... without correctness evidence
ERROR A4-council ... no council record
acceptance (SOLFIX3:W): REFUSED; 2 acceptance ERROR, 0 other ERROR

python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:Y
EXIT 1
ERROR A5-accepted ... SOLFIX3:W ... no accept event and is not in the legacy boundary

python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:W --only A5 --record
EXIT 0
check.py: 408 claims; 0 ERROR, 0 WARN, 0 INFO
acceptance (SOLFIX3:W): PASS; 0 acceptance ERROR, 0 other ERROR
record: accept event written for SOLFIX3:W (v1.0.0 fp:eddbb027baf5a19b)

python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:Y
EXIT 0
acceptance (SOLFIX3:Y): PASS; 0 acceptance ERROR, 0 other ERROR
```

Minimal fix: retain the original error count/findings for acceptance, recording and exit status; apply `--only` exclusively to display. Alternatively reject `--only` together with acceptance/record, but still avoid reporting a filtered diagnostic as a full acceptance PASS. Add a regression that attempts recording W with `--only A5` and checks both event absence and unfiltered consumer refusal.

### N1.b — MAJOR: the boundary file chooses its own trusted tag

Location: `bvsreg.py:1401–1429`, especially `legacy_rows_at(tag)` at 1413. The validator checks agreement with the tag named *inside the editable boundary file*, without requiring `tag == LEGACY_TAG`. Changing the file to a self-consistent boundary from a later tag makes newly introduced, never-accepted claims trusted. This is a stronger variant of the hand-added-row test: the file and its selected source agree, but the source is the wrong legacy boundary.

Exact fixture: appendix / probe.py, section `N1 SUBSTITUTE LEGACY TAG`. The script first removes the N1.a accept event and demonstrates Y is refused again. It commits the scratch registry containing W and Y, creates `solfix3-unaccepted`, deletes only the scratch boundary file, and regenerates it from that new tag. No change to `theory-v2.0-pre` is involved.

Equivalent critical commands after fixture setup:

```powershell
git add Theory_work/INFRA/registry/claims.tsv
git -c user.name='Review Fixture' -c user.email=review@example.invalid commit -qm 'scratch unaccepted claim'
git tag solfix3-unaccepted
Remove-Item -LiteralPath Theory_work/INFRA/LEGACY_ACCEPTED.tsv
python -B Theory_work/INFRA/tools/bvsreg.py legacy-boundary --tag solfix3-unaccepted
python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:Y
```

Observed:

```text
# Before replacing the boundary:
EXIT 1
ERROR A5-accepted ... SOLFIX3:W ... no accept event and is not in the legacy boundary
# Boundary generation:
EXIT 0
wrote .../LEGACY_ACCEPTED.tsv: 130 claim(s) at solfix3-unaccepted (620fad175c3d)
# Unfiltered acceptance after replacing the boundary:
EXIT 0
check.py: 408 claims; 0 ERROR, 184 WARN, 218 INFO
acceptance (SOLFIX3:Y): PASS; 0 acceptance ERROR, 0 other ERROR
```

There is no L1-legacy error. The scratch commit hash is incidental and changes on rerun. This does not rely on forging an events.log line.

Minimal fix: require the boundary's tag to equal the mandated `theory-v2.0-pre` (`LEGACY_TAG`) and compute the expected rows from that constant. Keep the recorded-commit comparison. Reject alternate tags for this production boundary, or clearly separate any generic export command from the acceptance boundary generator.

## N2 — RESOLVED

**No N2 defect found.** The outcome parser now rejects missing, duplicate, conflicting, malformed, wrong-digest, wrong-round, wrong-seat, wrong-score, low-score and FAIL verdicts. Both acceptance and binding use it. Acceptance also checks the stored manifest's header/current tree and coverage of the statement, unpinned premise and status-source files. The old digest-mention-only bypass is no longer sufficient.

Independent parser probe: `python -B C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/n2.py <fresh-clone>`; [source](C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/n2.py), [observed output](C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/n2.log). It returned exit 0 with `valid: PASS` and all ten invalid variants REFUSED. End-to-end valid bind/acceptance are also exercised in probe.py. The suite's new N2 tests exercise both original stale/outcome reproductions and the additional verdict/coverage variants.

## N3 — DEFECT

### N3.a — MAJOR: malformed non-headline gate entries silently lose all evidence checks

Location: `check.py:457–487`. Only successfully parsed gate entries enter the new all-results evidence loop. `unparsable` is reported only inside `if headline == "yes"`. A non-headline can thus name a nonexistent evidence file in a PENDING entry and gain acceptance by adding a trailing word that makes the entire entry unparsable. This is a malformed-input bypass, not a claim that the trailing-word syntax is a supported legitimate format: it should be refused rather than silently omitted.

Exact fixture: appendix / probe.py, section `N3 MALFORMED NONHEADLINE EVIDENCE`. Y has its valid council, no dependencies, and `headline != yes`. Its gate cell is:

```text
lit:PENDING(reviews/DOES_NOT_EXIST.md) trailing
```

Commands and observed output:

```text
python -B Theory_work/INFRA/tools/registry.py set SOLFIX3:Y depends_on= "gates=lit:PENDING(reviews/DOES_NOT_EXIST.md) trailing" --reason "malformed gate fixture"
EXIT 0
python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:Y
EXIT 0
check.py: 408 claims; 0 ERROR, 184 WARN, 218 INFO
acceptance (SOLFIX3:Y): PASS; 0 acceptance ERROR, 0 other ERROR

# Control: remove only the trailing word, keeping the same nonexistent file.
python -B Theory_work/INFRA/tools/registry.py set SOLFIX3:Y "gates=lit:PENDING(reviews/DOES_NOT_EXIST.md)" --reason "well formed control"
EXIT 0
python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:Y
EXIT 1
ERROR A1-evidence ... gate lit:PENDING: evidence 'reviews/DOES_NOT_EXIST.md' resolves to no file
acceptance (SOLFIX3:Y): REFUSED; 1 acceptance ERROR, 0 other ERROR
```

Minimal fix: reject unparsable gate entries for every claim being accepted, before the headline-specific strength requirements. Do not try to recover evidence heuristically from malformed syntax. Add this non-headline malformed/valid-control pair to the N3 tests. The original well-formed declined-disposition reproduction is fixed.

## N4 — DEFECT

### N4.a — MINOR: manifest CLI still runs while the transaction journal exists

Location: `Wave3/tools/manifest.py:255`, all three CLI branches. The INFRA tools import the guard, but this fourth reviewed tool has no journal/lock guard. Under the requested rule that every tool refuses while the journal exists, freeze, verify and bind should refuse too. The normal acceptance command correctly blocks, so this is not an end-to-end bypass of locked acceptance.

Exact fixture: appendix / probe.py, section `N4 MANIFEST UNDER LOCK`. A child runs real `R.write_many` on two dedicated scratch registry files. The only fault injection terminates the process (exit 73) just before replacement of the second destination. The resulting `.TXN_INPROGRESS` is genuine, with two existing backups; no fabricated journal is used.

Observed commands/results before recovery:

```text
crash exit 73 journal True
python -B Theory_work/INFRA/tools/check.py --quiet
EXIT 1
REGISTRY LOCKED: .../registry/.TXN_INPROGRESS exists ...

python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/WaveT/SOLFIX3 Theory_work/WaveT/SOLFIX3/reviews/MANIFEST_R1.txt
EXIT 0
verify: OK MANIFEST 25831c280cd740ff3bbc36009245af6bc963a305fc55bf044ec5344686fe8bc0

python -B Theory_work/Wave3/tools/manifest.py bind Theory_work/WaveT/SOLFIX3/reviews/MANIFEST_R1.txt Theory_work/WaveT/SOLFIX3/reviews/sol.md Theory_work/WaveT/SOLFIX3/reviews/opus.md --council "<fixture cell>"
EXIT 0
bind: OK, 2 review(s) give a PASS verdict (>= 8.0) on MANIFEST 25831c280cd740ff3bbc36009245af6bc963a305fc55bf044ec5344686fe8bc0

python -B Theory_work/Wave3/tools/manifest.py freeze Theory_work/WaveT/SOLFIX3 Theory_work/WaveT/SOLFIX3/reviews/MANIFEST_LOCKED.txt
EXIT 0
MANIFEST 25831c280cd740ff3bbc36009245af6bc963a305fc55bf044ec5344686fe8bc0 (2 files, 0 extra input(s))
```

The appendix contains the full actual council argument. `bvsreg.py recover` subsequently returned 0, restored both files and removed the journal. Core crash/recovery behavior is working in this reproduction; the defect is specifically incomplete tool blocking.

Minimal fix: invoke the shared transaction guard at the manifest CLI boundary before freeze/verify/bind. Keep the manifest library usable from bvsreg without a circular import. Include the manifest commands in the journal-present regression.

## Validation results and an execution limitation

- Independent adversarial fixture: `python -B .../probe.py .../repo`, exit **0**; all four reported defects have the actual subprocess return codes and output recorded in probe.log and above. The fixture's exit 0 is not a claim that acceptance was refused: the successful bypasses are explicitly identified.
- Independent N2 parser probe: **11 cases**, exit **0**; the valid case passes and all ten invalid variants are refused.
- Full `python -B Theory_work/INFRA/tools/test_lifecycle.py`: exit **1**, **120 PASS, 3 FAIL**, [complete log](C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/suite.log). The three FAIL lines are the N1 ordinary record, consumer-after-record and stale-record scenarios. **This was a contaminated full-suite run, not a clean regression verdict.** I incorrectly used the same scratch clone as the source of the suite and as the target of the independent probes concurrently. At test_lifecycle.py:836–837 the suite refreshes its registry from LIVE_INFRA/registry mid-run. By then my probe had added SOLFIX3 rows to that live scratch registry; their untracked ticket source files were absent in the suite's earlier detached worktree. This introduces unrelated registry errors precisely where `--record` requires zero errors globally, while the helper acc_errs filters errors to the named claim. These failures are not reported as additional defects. No clean full-suite pass is claimed; an isolated rerun is a remaining validation limit.
- Separate ordinary-record control after the suite finished: in the probe clone, clear the deliberately missing gate with `python -B Theory_work/INFRA/tools/registry.py set SOLFIX3:Y gates= --reason "clean normal-record control"`, then run `python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:Y --record`. Exit **0**, `check.py: 408 claims; 0 ERROR`, `acceptance (SOLFIX3:Y): PASS`, `record: accept event written for SOLFIX3:Y (v1.0.0 fp:1464f11cc02971b5)`. [Output](C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/normal-record.log). Thus the independent evidence does not support a fifth defect in ordinary recording.
- Read-back after the crash/recovery probe confirmed both dedicated registry files contain `old` and `.TXN_INPROGRESS` is absent.

## Hypotheses / limits

No additional unproved hypothesis is asserted as a defect. Concurrency and operating-system power-loss durability were not fault-tested. N4.a is scoped to the explicitly requested all-tools rule; it does not claim that the manifest content itself was corrupt in this fixture. Mathematical truth and whether reviewers really examined the content remain outside these four mechanical fixes.

## Exact fixture source

Save as `probe.py` outside the clone and run with the clone's absolute path as its only argument. The executable source follows (also retained at the evidence path above):

```python
import pathlib,sys,subprocess,json,os
sys.dont_write_bytecode=True
root=pathlib.Path(sys.argv[1]).resolve();os.chdir(root)
sys.path.insert(0,str(root/'Theory_work/INFRA/tools'));import bvsreg as R
base=root/'Theory_work/WaveT/SOLFIX3';(base/'reviews').mkdir(parents=True,exist_ok=True)
def put(rel,txt):
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(txt,encoding='utf-8');return p
N=base.relative_to(root).as_posix()
put(N+'/STATEMENT.md','Lemma W. W holds.\nTheorem Y. Y follows from W.\n')
put(N+'/REPORT.md','PROVED-CHECKED\n')
def run(script,*args):
 cmd=[sys.executable,'-B',str(root/script),*map(str,args)]
 p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
 print('COMMAND',subprocess.list2cmdline(cmd),'\nEXIT',p.returncode,'\n'+p.stdout+p.stderr,flush=True);return p
T='Theory_work/INFRA/tools/'
M='Theory_work/Wave3/tools/manifest.py'
# Keep fragment outside reviewed ticket tree.
f=root.parent/'fixture.jsonl'
f.write_text(''.join(json.dumps(dict(ticket='SOLFIX3',local_id=loc,kind='lemma',name=loc,file=N+'/STATEMENT.md',lines=[line,line],status='PROVED-CHECKED',status_source=N+'/REPORT.md:1',**kw))+'\n' for loc,line,kw in [('W',1,{}),('Y',2,{'depends_on':['SOLFIX3:W@stmt']})]),encoding='utf-8')
run(T+'ingest.py','claims',f,'--apply')
man=N+'/reviews/MANIFEST_R1.txt';run(M,'freeze',N,man)
dg=(root/man).read_text().split()[1]
for seat in ['sol','opus']:put(N+'/reviews/'+seat+'.md',f'COUNCIL-VERDICT round=R1 manifest={dg} seat={seat} score=8.5 gates=PASS\n')
cell=f'R1; MANIFEST {dg}; sol=8.5 PASS(reviews/sol.md); opus=8.5 PASS(reviews/opus.md)'
run(T+'registry.py','set','SOLFIX3:Y','council='+cell,'--reason','review fixture')
print('\nN1 FILTERED RECORD BYPASS',flush=True)
run(T+'check.py','--quiet','--acceptance','SOLFIX3:W')
run(T+'check.py','--quiet','--acceptance','SOLFIX3:Y')
run(T+'check.py','--quiet','--acceptance','SOLFIX3:W','--only','A5','--record')
run(T+'check.py','--quiet','--acceptance','SOLFIX3:Y')
# Remove the forged record so the independent legacy experiment starts unaccepted.
h,ev=R.read_tsv(R.EVENTS);R.write_tsv(R.EVENTS,h,[e for e in ev if not(e['id']=='SOLFIX3:W' and e['action']=='accept')])
print('\nN1 SUBSTITUTE LEGACY TAG',flush=True)
run(T+'check.py','--quiet','--acceptance','SOLFIX3:Y')
# Commit the scratch-only registry and point a fresh tag at it, not theory-v2.0-pre.
run_git=lambda *a: subprocess.run(['git',*a],check=True,capture_output=True,text=True)
run_git('add','Theory_work/INFRA/registry/claims.tsv')
run_git('-c','user.name=Review Fixture','-c','user.email=review@example.invalid','commit','-qm','scratch unaccepted claim')
run_git('tag','solfix3-unaccepted')
legacy=pathlib.Path(R.LEGACY_FILE);saved=legacy.read_text(encoding='utf-8');legacy.unlink()
run(T+'bvsreg.py','legacy-boundary','--tag','solfix3-unaccepted')
run(T+'check.py','--quiet','--acceptance','SOLFIX3:Y')
legacy.write_text(saved,encoding='utf-8')
print('\nN3 MALFORMED NONHEADLINE EVIDENCE',flush=True)
run(T+'registry.py','set','SOLFIX3:Y','depends_on=','gates=lit:PENDING(reviews/DOES_NOT_EXIST.md) trailing','--reason','malformed gate fixture')
run(T+'check.py','--quiet','--acceptance','SOLFIX3:Y')
run(T+'registry.py','set','SOLFIX3:Y','gates=lit:PENDING(reviews/DOES_NOT_EXIST.md)','--reason','well formed control')
run(T+'check.py','--quiet','--acceptance','SOLFIX3:Y')
print('\nN4 MANIFEST UNDER LOCK',flush=True)
# Actual valid transaction journal, left by process death after the first replacement.
c1=pathlib.Path(R.REG)/'sol-c1.tsv';c2=pathlib.Path(R.REG)/'sol-c2.tsv'
for c in (c1,c2):c.write_text('old\n')
child=root.parent/'kill.py';child.write_text(f"import os,sys\nsys.path.insert(0,{str(root/'Theory_work/INFRA/tools')!r})\nimport bvsreg as R\nreal=os.replace\ndef kill(s,d):\n if d=={str(c2)!r}:os._exit(73)\n return real(s,d)\nos.replace=kill\nR.write_many([({str(c1)!r},'new\\n'),({str(c2)!r},'new\\n')])\n")
run_git # no-op
p=subprocess.run([sys.executable,'-B',str(child)]);print('crash exit',p.returncode,'journal',pathlib.Path(R.TXN_JOURNAL).exists(),flush=True)
run(T+'check.py','--quiet')
run(M,'verify',N,man)
run(M,'bind',man,N+'/reviews/sol.md',N+'/reviews/opus.md','--council',cell)
run(M,'freeze',N,N+'/reviews/MANIFEST_LOCKED.txt')
run(T+'bvsreg.py','recover')

```

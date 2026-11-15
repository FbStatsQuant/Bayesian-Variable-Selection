BYPASS FOUND

Independent correctness review of the uncommitted INFRA R06 change. No implementation changes made; original checkouts were read only, apart from this requested report. Scratch base: `C:/Users/felip/AppData/Local/Temp/r6s-7812`.

| Item | Verdict and evidence |
|---|---|
| 1 hashes | **BYPASS FOUND (MAJOR F1).** CRCRLF ambiguity permits a non-EOL-equivalent file to verify. Content edits, moved CR, BOM, extra newline, NUL insertion, UTF-16 conversion, binary EOL edits, file rename and extra-directory content/rename controls were rejected. |
| 2 fingerprints | **HOLDS in reviewed scope.** All 406 `(id, recomputed sha256, status_sha256, fp2)` tuples identical on LF/CRLF HEAD clones. Registry hash sites use line-wise strings, not raw bytes (`bvsreg.py:636,1646,1707`); no EOL migration needed. Changing council/status_source/sha256 fields, adding an alias, or changing a referenced evidence artifact changed the stamp. |
| 3a addendum | **BYPASS FOUND (MAJOR F2).** Ordinary ACCEPT addenda pass. NOT-EXAMINED retained as unchecked passes; checked version refuses. Contradictory body/addendum decisions and second/rescored verdicts refuse. Malformed negative decision `ACCEPT=NO` incorrectly passes even through the own-checkpoint route. |
| 3b seat tables | **BYPASS FOUND via F2.** Missing id, NOT-EXAMINED, and one-seat-only table all refuse. Local/full ids resolve as intended; other-ticket ids and alias spellings remain literal. Decision parsing accepts `ACCEPT=NO` and `ACCEPT/NOT-EXAMINED`. |
| 3c carrier | **Coverage HOLDS; decision bypass F2 applies.** JSONL and Markdown carriers pass with covered sources. Markdown `../STATEMENT.md` and `../REPORT.md` resolve correctly from `reviews/`. Uncovered statement/premise/carrier-as-statement refuse. A carrier added directly in the ticket folder yields `ADDED CARRIER.jsonl`, as expected: use an excluded/outside folder. |

## F1 — MAJOR: CR insertion/removal crosses the three accepted hash variants

Location: `Theory_work/Wave3/tools/manifest.py:accepted_hashes` and `lf_normalised`.

A legacy raw-byte hash of `b'a\r\n'` also matches LF-normalisation of `b'a\r\r\n'`. The latter adds a lone CR; universal text reading sees an extra blank line. This is beyond uniform LF/CRLF conversion, but verify exits 0. A fresh freeze of the latter records the same hash, then accepts `b'a\n'`, losing the extra CR. Thus the defect also affects newly frozen manifests.

Minimal reproduction, run in a disposable clone with the new tool (Python; creates only scratch files):

```python
import pathlib, hashlib, importlib.util, subprocess, sys
s = importlib.util.spec_from_file_location('M', 'Theory_work/Wave3/tools/manifest.py')
M = importlib.util.module_from_spec(s); s.loader.exec_module(M)
t = pathlib.Path('Theory_work/WaveT/CRPROBE'); (t/'reviews').mkdir(parents=True)
a = t/'a.md'; m = t/'reviews/MANIFEST_R1.txt'
a.write_bytes(b'a\r\n')
rows = [hashlib.sha256(a.read_bytes()).hexdigest() + '  a.md']
m.write_text('MANIFEST ' + M.digest(rows) + '\n' + '\n'.join(rows) + '\n', encoding='utf-8')
def call(cmd):
    p = subprocess.run([sys.executable, '-B', 'Theory_work/Wave3/tools/manifest.py', cmd, str(t), str(m)], capture_output=True, text=True)
    print(p.returncode, p.stdout.strip())
call('verify')
a.write_bytes(b'a\r\r\n'); call('verify')
call('freeze')
a.write_bytes(b'a\n'); call('verify')
```

Observed all four commands exit **0**. All three verifies print `verify: OK MANIFEST df439991c50d67a15eb33089883f644fefbc65d3b17d8327f09e0b9e0a91a9f9`. Evidence: scratch `more.log`, first four lines. This is a collision between transformation variants, not a cryptographic SHA collision.

Fix direction: distinguish ordinary LF/CRLF text from content with residual/lone CR. Hash the latter raw and do not apply variant fallbacks to it; ensure fresh freeze and verify use compatible, unambiguous rules (version the format if needed). Add both legacy-manifest CR insertion and fresh-manifest CR removal regressions. Do not solve this by repeatedly stripping CR: that would erase the content distinction the specification promises.

## F2 — MAJOR: punctuation boundary treats a negative/malformed decision as acceptance

Location: `Theory_work/INFRA/tools/bvsreg.py:1297` (`_ACCEPT_DEC`) / `seat_table`.

`accept(?:ed)?(?![\w-])` tests only the next character. `ACCEPT=NO` and `ACCEPT/NOT-EXAMINED` both return accepted=True, although neither is the documented ACCEPT/accepted token optionally followed by more words. `ACCEPT=NO` explicitly denies acceptance. This changes the old behavior: the old parser did not accept strings starting with `ACCEPT=`.

Minimal parser reproduction, from the scratch probe clone:

```python
import sys
sys.path.insert(0, 'Theory_work/INFRA/tools')
import bvsreg as R
print(R.seat_decisions('| id | decision |\n|---|---|\n| A | ACCEPT=NO |\n', 'REV'))
```

Observed `({'REV:A': True}, [])`, exit **0**.

End-to-end reproduction: scratch `more.py` constructs ticket `REV`, two covered files `STATEMENT.md` / `REPORT.md`, freezes them, writes two valid single-verdict reviews, and appends matching seat tables. For each decision it invokes:

```
python -B Theory_work/INFRA/tools/ingest.py claims <probe>/Theory_work/WaveT/REV/reviews/carrier.jsonl --staged
```

With both seats' A decision set to `ACCEPT=NO` or `ACCEPT/NOT-EXAMINED`: exit **0**, `acceptance (REV:A): PASS; 0 acceptance ERROR`. With NOT-EXAMINED, acceptable, or accepted-ish: exit **1**, REFUSED. Full transcripts: scratch `probe_ACCEPT=NO.out`, `probe_ACCEPT_NOT-EXAMINED.out`; fixture and command runner: `more.py`.

The separate `ck.py` fixture uses `CHECKPOINT_3.md` with A checked and B unchecked/NOT-EXAMINED. Both seats' A decision `ACCEPT=NO` still gives exit **0**, `acceptance (REV:A, REV:B): PASS; 0 acceptance ERROR` (`ck_bad_decision.out`). With B checked instead, ordinary ACCEPT tables correctly refuse (`ck_checked.out`).

Fix direction: validate the entire decision grammar. At minimum require end-of-cell or whitespace after the allowed token, rather than any non-word/non-hyphen character. Keep explicitly supported explanatory suffixes, and reject malformed/negative decision syntax. Add parser and staged-ingest regressions for both carrier and checkpoint paths.

## Regression evidence

- Fresh HEAD clone, old vs new tools: standard check exit **0**, 406 claims, **0 ERROR / 184 WARN / 217 INFO**, **401 findings**; complete parsed JSON identical. All-406 acceptance exit **1**, **1019 ERROR / 184 WARN / 580 INFO**, **1,783 findings**; complete parsed JSON identical. Evidence: `fixreg.log`, `old_check.json`, `new_check.json`, `old_accept.json`, `new_accept.json`.
- New verifier on LF and CRLF clones versus old verifier on the corresponding read-only frozen trees: identical difference lists for **all 28 currently present ticket manifests**, on both clones (**56 comparisons**): START 12, RM2 12, PSHARP 2, MISR 2. The brief mentions 30; current inventories in all four named frozen worktrees total 28. Evidence: `review.log`; no differences found.
- Fresh theory/W3-START LF and CRLF clones with **all current INFRA/Wave3 Python tools** overlaid: `ingest.py claims Theory_work/Wave3/W3-START/CHECKPOINT_3.md --staged` exits **0**, acceptance PASS, **21 claims** on each. Evidence: `start_fixed_LF.out`, `start_fixed_CRLF.out`.
- Fingerprints: identical recomputed tuples for all **406 claims** (`fp_LF.json`, `fp_CRLF.json`). Artifact mutation control: `W1-GEN:Thm-GEN` stamp changed; row-field and alias mutation controls also changed stamps. No separate fingerprint bypass found.

## Full suite

`python -B Theory_work/INFRA/tools/test_lifecycle.py`, run once in fresh `suite` clone with the requested overlay and no independent probes: **161/161 PASS, 0 FAIL**. The suite also confirmed 52 manifest/commit comparisons on five refs with no missing refs. Full output: scratch `suite/suite.log`.

Exit-code caveat: the outer PowerShell command reported **1**, with `NativeCommandError` records for the suite's deliberate rollback/registry-lock stderr. The log completes normally through all 161 PASS lines, with no traceback or FAIL. The Python script's final expression exits 0 when all these results pass; its numeric process code was not captured separately from the PowerShell wrapper. Thus the pass count is verified; a separately measured Python exit status is not claimed.

## Scratch paths

All review scratch under `C:/Users/felip/AppData/Local/Temp/r6s-7812`: `suite` (fresh suite clone, no independent probes), `probe` (bypass fixtures), `reg` (HEAD regression), `LF` / `CRLF` (manifest/fingerprint clones), `start-LF` / `start-CRLF` (fresh staged acceptance). The suite itself creates its standard disposable sandbox under `C:/Users/felip/AppData/Local/Temp/bvs-ci-sandboxes` and temporary EOL clones. Scripts/logs named above are under the review scratch base. No subagents used.

## Round 2 (re-check)

**BYPASS FOUND — F1 RESOLVED; F2 NOT RESOLVED (original probes fixed, but one remaining MAJOR decision-parsing bypass).**

Reviewed the fixed uncommitted tools in fresh disposable clones; no implementation edits, no subagents, no git-state changes in the supplied or frozen worktrees. All four changed files in the suite clone still byte-match the source overlay.

### Fix re-check

- **F1 resolved.** The exact round-1 legacy CRLF -> CRCRLF insertion and fresh CRCRLF freeze -> LF removal probes now exit **1**, reporting `CHANGED a.md` (unchanged baseline/freeze exit 0). Exhaustive accepted-hash overlap checking on all **1,365** byte strings of length 0–5 over `{a, LF, CR, NUL}` found no overlap beyond LF/CRLF equivalence. Legacy raw manifests containing lone CRs and NULs verify unchanged and refuse the tested changes. CR/NUL placements and replacements of UTF-8 NEL/U+2028/U+2029 with LF also refuse. Evidence: `probes.py`, `probes3.log` under the scratch base below.
- **Original F2 probes fixed.** `ACCEPT=NO`, `ACCEPT/NOT-EXAMINED`, `accepted, no`, and `ACCEPT not` parse false. The first two refuse staged carrier ingest (exit **1**); `ACCEPT=NO` also refuses the own-checkpoint route (exit **1**). Ordinary `ACCEPT` and the documented `accepted`, `accepted (...)`, `accepted with non-blocking remarks ...` forms still parse true; the real START ingest passes below. NBSP/em-space before `NOT` and Markdown-emphasized `not` refuse. No break of the documented real-seat workflow found.

### R2-F2 — MAJOR: punctuation or a remark hides an explicit negative decision

Location: `Theory_work/INFRA/tools/bvsreg.py:1297–1330`, `_ACCEPT_DEC` / `seat_table`. The negative lookahead checks only the first character after whitespace; `(` or `:` bypasses it, and a negative word later in the suffix is never examined. Separately, `text.splitlines()` splits U+2028 before cell parsing, leaving an accepted truncated row.

Minimal parser reproduction (from a fixed clone, exit **0**):

```python
import sys
sys.path.insert(0, 'Theory_work/INFRA/tools')
import bvsreg as R
for decision in ['accepted (not accepted)', 'ACCEPT : NO',
                 'accepted with remarks; withdrawn', 'ACCEPT\u2028NOT-EXAMINED']:
    print(repr(decision), R.seat_decisions(
        '| id | decision |\n|---|---|\n| A | ' + decision + ' |\n', 'REV'))
```

All four produce `({'REV:A': True}, [])`. These are negative/withdrawn decisions counted as acceptance, not merely harmless formatting rejected by a strict parser.

End-to-end reproduction: `neg.py` builds a fresh `neg` clone with covered `STATEMENT.md`/`REPORT.md`, a valid manifest and two single-verdict council reviews; each seat has `| A | <decision> |`. For **each of the four strings above**:

```
python -B Theory_work/INFRA/tools/ingest.py claims Theory_work/WaveT/REV/reviews/carrier.jsonl --staged
```

exits **0**, `acceptance (REV:A): PASS; 0 acceptance ERROR`. Both seats using `accepted (not accepted)` also gives **0**, `acceptance (REV:A, REV:B): PASS; 0 acceptance ERROR` for staged ingest of `Theory_work/WaveT/REV/CHECKPOINT_3.md` (A checked; B unchecked and NOT-EXAMINED). Controls: ordinary ACCEPT passes; checking B refuses; restoring `ACCEPT=NO` refuses. Evidence: `neg.py`, `neg.log`, `probe_neg_0.out` through `probe_neg_3.out`, `ck_negation.out`; these clean-fixture results establish the bypass independently of the earlier `variant_*` probes, which had an extra carrier file invalidating their manifest.

Fix direction: use an unambiguous decision field and separate remarks, or a constrained suffix grammar preserving the real accepted forms while refusing contradictory/withdrawn dispositions, including punctuation-wrapped and later negations. Do not truncate Unicode separators into a valid partial row: reject such cells/rows or parse physical Markdown lines without `splitlines()`'s extra separators. Add parser and both staged-ingest regressions for these variants; avoid a blanket rejection of innocuous remarks such as “no blocking issues”.

### Regression and suite

- HEAD old/new parsed JSON is **identical**: standard check exit **0**, **406 claims / 401 findings**; all-406 acceptance exit **1**, **1,783 findings**. Evidence: `head.log`, `old_check.json`, `new_check.json`, `old_accept.json`, `new_accept.json`.
- All **28 branch manifests** match the old verifier's difference lists on the read-only frozen trees on **both LF and CRLF clones (56/56)**: START 12, RM2 12, PSHARP 2, MISR 2. No mismatches. Evidence: `real.log`.
- Fresh START LF and CRLF clones with current INFRA/Wave3 Python tools: staged `CHECKPOINT_3.md` ingest exits **0**, acceptance **PASS for 21 claims**, zero acceptance errors on each. Evidence: `start_LF.out`, `start_CRLF.out`.
- Full suite run **once** in fresh `suite`, with no independent probes: **164/164 PASS, 0 FAIL; Python exit 0**, measured directly by `subprocess.run().returncode` (`suite.exit`), not inferred from PowerShell. All three F1/F2 regression results pass despite the additional bypass above. Evidence: `suite.log`, `suite.exit`.

Scratch base: `C:/Users/felip/AppData/Local/Temp/r6s2-112`; clones `suite` (fresh, no independent probes), `probe`, `neg`, `reg`, and `W3-{START,RM2,PSHARP,MISR}-{LF,CRLF}`. The suite also uses its standard disposable `bvs-ci-sandboxes` sandbox and temporary EOL clones. Only this appended section was written to the supplied worktree.


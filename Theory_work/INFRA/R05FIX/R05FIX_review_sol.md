BYPASS FOUND

Reviewed bfdb968e5f10927de1b97ee60ac5e7e1b92c7d51 against c8a970f. Two MAJOR bypasses of the earlier-round/citation safeguard were reproduced independently. No CRITICAL finding.

| Safeguard | Verdict | Evidence |
|---|---|---|
| 1. Own checkpoint, status only | Holds in tested routes | LOG.md, sub/CHECKPOINT_3.md, ../R05OTHER/CHECKPOINT_3.md, lowercase checkpoint_3.md and tickets.tsv folder redirection: acceptance exit 1. Using the checkpoint as the statement: exit 1, A4 “does not cover”. Uncovered external premise: exit 1, A4 coverage. ./ and sub/../ resolving to the actual own checkpoint pass (expected). |
| 2. Council PASS binding; earlier-round binding | Council holds; historical binding bypass | Foreign council-seat digest: exit 1, matching-verdict/contradictory-verdict errors. Earlier review without digest: exit 1. An internally invalid historical manifest satisfies binding: B2. |
| 3. Frozen checkpoint digest | Holds in tested routes | Ingest records digest; edit after ingest: exit 1 with C12-checkpoint AND A4. Clearing digest: A4 refusal. registry.py set status_sha256=0: exit 1, “not settable”. Rehash/set code has no digest-refresh route; designated status-change commands intentionally refresh it. |
| 4. Exact accepted-id sets | Holds in tested routes | Local/full-id contradictory decisions, contradictions across multiple tables and an extra seat-accepted id all refuse (exit 1). Fresh suite also checks checkpoint extra ids, rejected/missing ids and absent tables. W3-START has exactly 21 ids in each seat and checkpoint. |
| 5. Cited rounds resolve uniquely to frozen manifests | BYPASS | Ordinary unresolved/ambiguous rounds refuse (exit 1); continued status hides a well-formed unresolved citation (B1); historical manifest is accepted without internal integrity (B2). |

Findings

B1 — MAJOR: a continued status hides an unresolved cited round.
Location: Theory_work/INFRA/tools/bvsreg.py:1376–1382; compare status_at at :603–622.
status_at explicitly permits a status to continue onto the following three lines, but checkpoint_problems scans only the explicitly named source span. Thus a citation that is part of the actual registry status is silently omitted when its continuation falls outside that span. This is not an unsupported spelling of a citation: LC9-A: VERIFIED uses the documented grammar.

Reproduction (scratch clone r5s-f1b89c2d; the scripts retain/restore their fixture):
  python -B markdown_confirm.py
The script temporarily removes the synthetic R05P:A row, retains its valid frozen acceptance manifest and two bound PASS seat reviews accepting A, and writes this own CHECKPOINT_3.md:
  PROVED-CHECKED
  LC9-A: VERIFIED

  ```
  REGISTRY
  claim: R05P:A | kind: lemma | statement: STATEMENT.md:1 | premises: none
  name: Lemma A
  status: PROVED-CHECKED LC9-A: VERIFIED | status_source: CHECKPOINT_3.md:1
  council: <unchanged valid R1 cell>
  ```
It runs:
  python -B Theory_work/INFRA/tools/ingest.py claims Theory_work/WaveT/R05P/CHECKPOINT_3.md --staged
Observed exit 0; “407 claims; 0 ERROR”; “acceptance (R05P:A): PASS; 0 acceptance ERROR”. No LC9-A review exists. Ingest itself computes status_sha256; the reproduction does not forge/clear a recorded digest. Full output: markdown-repro.log.
Control: python -B confirm.py tests the identical continued status via JSONL, first with source :1 (exit 0/PASS), then :1-2 (exit 1, A4 “LC9-A ... resolves to no file”). Evidence: confirmed-repros.json.
Fix direction: share the status-location/matching logic and scan all lines that actually supply the accepted status (or require an explicit span covering the full status). Add the Markdown staged-ingest regression above. Do not scan unrelated neighboring claims indiscriminately.

B2 — MAJOR: a header-only or corrupted historical manifest counts as a frozen manifest.
Location: Theory_work/INFRA/tools/bvsreg.py:1333–1343, :1393–1396.
manifest_digests checks only the header, so the earlier review can quote a digest that never hashes the manifest's stored entries. The acceptance manifest and both council verdicts remain valid; the earlier round's own supposed frozen artifact is invalid. Not verifying historical files against today's tree is intended, but verifying the historical manifest's INTERNAL digest is a different requirement.

Reproduction:
  python -B confirm.py
Its “B2 corrupt historical manifest” case creates reviews/MANIFEST_corrupt.txt containing:
  MANIFEST <64 zeroes>
  not a manifest row
and makes the unique LC1_A_check.md quote those 64 zeroes. The unchanged checkpoint cites “LC1-A: VERIFIED.” It then runs:
  python -B Theory_work/INFRA/tools/check.py --quiet --acceptance R05P:A
Observed exit 0; “407 claims; 0 ERROR”; “acceptance (R05P:A): PASS; 0 acceptance ERROR, 0 other ERROR”.
Contrast:
  python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/WaveT/R05P Theory_work/WaveT/R05P/reviews/MANIFEST_corrupt.txt
Exit 1: “header digest does not match the stored rows (corrupted or hand-edited manifest)”. This failure precedes comparison against the current tree. Evidence: confirmed-repros.json.
Fix direction: parse the stored historical entries, validate their syntax, and recompute their digest before accepting the header. Do not require historical manifests to match current ticket contents.

NOTE — Citation grammar is deliberately narrow. “LC9-A:VERIFIED” (no whitespace after colon) passes, while “LC9-A: VERIFIED” refuses. The code documents the whitespace boundary; free-text mentions are explicitly not citations. Also, “acceptedness rejected” counts as accepted because decisions are documented as starting with “accepted”. These are grammar limits, not additional bypass findings under the stated contract.

Regression
On a disposable clone checked out at c8a970f, ran old check.py --quiet --json <file>, and --acceptance <all 406 ids> --json <file>; overlaid the new tools and repeated. Parsed JSON objects match exactly: routine 401 findings (exit 0); acceptance 1,783 findings (exit 1). Logs/data: r5s-reg-4c9a/{old,new}-{routine,acceptance}.json; reproduction driver regression_fix.py in r5s-f1b89c2d. This reproduces the supplied non-checkpoint regression evidence.

W3-START dry run
Cloned theory/W3-START at 808ddd1afcb45b426b7788b07d11a9d8bc337241; copied every tracked file byte-for-byte from the read-only W3-START worktree, then overlaid R05 tools/*.py. Requested staged ingest: exit 0, 427 claims, 0 ERROR, acceptance PASS for all 21 ingested ids. Output: r5s-w3-4c9a/dry-run.log.
Non-vacuity: a subsequent scratch-only --apply records 21 nonempty matching status digests; all 21 rows resolve to the own checkpoint; checkpoint ids = 21; each R2 council table accepts exactly 21 with no parser problems; A4 problems = 0. Status lines exercise seven actual round resolutions: BR1, LC1-A/B/C, LC2-A/B, SW1, each to exactly one file. Driver: exercise.py in the W3 scratch clone.

Full suite
Ran python -B Theory_work/INFRA/tools/test_lifecycle.py once in the fresh, otherwise unmodified branch clone r5s-suite-a8680c62. Exit 0: 145 PASS, 0 FAIL, including all 11 INFRA R05 scenarios. Full final output retained in that clone at suite-result.log. The rollback/REGISTRY LOCKED stderr emitted earlier belongs to intentional recovery fault-injection cases, which passed.

Scratch paths (all under C:/Users/felip/AppData/Local/Temp/)
- r5s-f1b89c2d — isolated branch clone, independent fixtures/probes and retained JSON evidence/scripts.
- r5s-suite-a8680c62 — fresh branch clone used only for the full suite; the suite creates/removes its own disposable detached worktree bvs-ci-sandboxes/sb-bg0ykikx.
- r5s-reg-4c9a — main c8a970f regression clone.
- r5s-w3-4c9a — W3-START byte-preserving dry-run clone.
No existing checkout/worktree git state changed. W3-START was read only. No subagents started. Only this review file was written in the task worktree.


## Re-check (b0c21b0)

SAFEGUARDS HOLD — B1 RESOLVED; B2 RESOLVED. Focused re-check of b0c21b0446d70bf309805b9f18a80cb48c789730 against bfdb968; no new findings.

All commands below ran in disposable clones under `C:/Users/felip/AppData/Local/Temp/`. The probe and suite clones were freshly cloned from `infra/R05-ckpt-status` and detached at the exact requested commit. Existing checkouts/worktrees and their git state were untouched. No subagents were started.

### B1 — RESOLVED

In `r5sr-fe6d397e`, copied the original `probes.py`, `markdown_confirm.py`, and `confirm.py` scripts from `r5s-f1b89c2d`; rebuilt the original fixture using `python -B probes.py` (driver exit 0; initial fixture ingest exit 0).

- `python -B markdown_confirm.py` (driver exit 0): the original Markdown staged-ingest reproduction now exits **1**: `acceptance (R05P:A): REFUSED; 2 acceptance ERROR`; A4 says `the status line cites review round LC9-A, which resolves to no file .../reviews/LC9-A_*`. The fixture still records the complete status `PROVED-CHECKED LC9-A: VERIFIED` with source `CHECKPOINT_3.md:1`; no explicit second source line is needed to trigger refusal. Evidence: `markdown-repro.log`, `markdown-run.log`.
- `python -B confirm.py` (driver exit 0): both JSONL staged-ingest cases, source `:1` and control `:1-2`, exit **1** with the same unresolved-LC9-A A4 error. Evidence: `confirmed-repros.json`, `confirm-run.log`.

The code scans the recorded status in addition to the explicit source span; it does not scan neighboring claims indiscriminately.

### B2 — RESOLVED

`python -B confirm.py`: the original corrupted historical manifest case now makes `python -B Theory_work/INFRA/tools/check.py --quiet --acceptance R05P:A` exit **1**, `acceptance (R05P:A): REFUSED; 2 acceptance ERROR`; A4 reports `review .../LC1_A_check.md ... quotes no digest of a frozen .../reviews/MANIFEST_*.txt`. The independent manifest verifier also exits **1**: `header digest does not match the stored rows (corrupted or hand-edited manifest)`. Evidence: `confirmed-repros.json`.

`python -B extra_recheck.py` (driver exit 0) adds four negative controls: header-only with zero digest, empty rows with the correctly computed empty digest, malformed row with its correctly computed digest, and well-formed row with an incorrect header. Every acceptance command exits **1** with the A4 frozen-manifest binding error. A positive control with well-formed stored rows and a matching header, referencing a file absent from today's tree, exits **0**, `PASS; 0 acceptance ERROR, 0 other ERROR`. Thus internal integrity is enforced without requiring historical manifests to match current files. Evidence: `extra-results.json`, `extra-run.log`.

### Safeguards 1–5 / new findings

None found. Diff inspection and the original 23 probe cases (`python -B probes.py`, driver exit 0; `probe-results.json`, `safeguards.log`) support:

| Safeguard | Re-check evidence |
|---|---|
| 1. Own checkpoint, status only | LOG, nested/other-ticket/lowercase checkpoint sources and uncovered statement/premise exit 1. Own-checkpoint `./` and `sub/../` aliases still exit 0. Markdown driver's checkpoint-as-statement control exits 1 with A4 coverage; `confirm.py` folder redirection exits 1. |
| 2. Review binding | Foreign council digest and earlier review without a digest exit 1. B2 integrity checks above now refuse; valid historical binding remains usable. |
| 3. Recorded checkpoint digest | Post-ingest edit exits 1 with C12-checkpoint and A4; empty recorded digest exits 1. `registry.py set R05P:A status_sha256=0 --reason probe` exits 1, `field 'status_sha256' not settable here`. |
| 4. Exact accepted-id sets | Contradictory local/full ids, contradictions across tables, and extra accepted seat id exit 1. W3-START confirms exact 21-id equality for both seats. |
| 5. Round resolution / frozen binding | Unresolved and ambiguous rounds exit 1; continued recorded-status citation now exits 1; malformed historical manifests refuse. W3-START still exercises seven unique earlier-round resolutions. |

The previously documented no-space citation and `accepted`-prefix grammar limits are unchanged; they are not new findings.

### W3-START dry run

Recreated the earlier W3 scratch baseline in a fresh clone `r5sr-w3-8b361a` at 808ddd1afcb45b426b7788b07d11a9d8bc337241, using the earlier setup procedure: copy every tracked file byte-for-byte from the read-only W3-START worktree, then overlay the requested commit's `tools/*.py`. This avoids using the already-applied registry from the earlier `r5s-w3-4c9a` run. Driver: `python -B w3_setup_recheck.py` in the probe clone, exit **0**.

`python -B Theory_work/INFRA/tools/ingest.py claims Theory_work/Wave3/W3-START/CHECKPOINT_3.md --staged` exits **0**: `21 claim(s) to add; 0 problem(s)`; staged check has `427 claims; 0 ERROR`; acceptance for all 21 ingested ids is `PASS; 0 acceptance ERROR`. Evidence: W3 clone `recheck-dry-run.log`.

Copied and ran the original `exercise.py` (exit **0**) in this scratch W3 clone: scratch-only apply exits 0; 21 rows, 21 own checkpoints, 21 matching nonempty recorded digests, 21 checkpoint ids, both R2 seats accept exactly 21 with no parser problems, A4 problems 0. BR1, LC1-A/B/C, LC2-A/B and SW1 each resolve to exactly one review file. Evidence: `exercise-recheck.log`.

### Full suite

Ran `python -B Theory_work/INFRA/tools/test_lifecycle.py` exactly once in the fresh, otherwise unprobed exact-head clone `r5sr-suite-71aa958a`. Exit **0**: **146 PASS, 0 FAIL**, including the continued-status regression and corrupted-historical-manifest check. Full output: `suite-result.log` in that clone. Its disposable test sandbox was `C:/Users/felip/AppData/Local/Temp/bvs-ci-sandboxes/sb-eu35vs8u`. The rollback/REGISTRY LOCKED diagnostics are intentional recovery fault-injection output; the corresponding recovery tests all PASS.

### Scratch paths

- `C:/Users/felip/AppData/Local/Temp/r5sr-fe6d397e` — fresh exact-head clone; original reproductions, 23 safeguard probes, additional manifest controls, scripts and evidence.
- `C:/Users/felip/AppData/Local/Temp/r5sr-suite-71aa958a` — fresh exact-head clone used only for the one full-suite run and its output log.
- `C:/Users/felip/AppData/Local/Temp/r5sr-w3-8b361a` — recreated byte-preserving W3 baseline with exact-head tools, staged dry run and scratch-only non-vacuity checks.

Only this appended review section was written outside scratch clones; the earlier review text was preserved.

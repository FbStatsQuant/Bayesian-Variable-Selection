Overall verdict: RESOLVED for R04-N1 and R04-N2; no additional invalidation defect found in the reviewed scope.

Reviewed worktree HEAD `3d6d84d0bc48b4de23f9f4327bb4eeedf1f34b60` plus its uncommitted changes to `bvsreg.py`, `check.py`, `test_lifecycle.py` and `LIFECYCLE.md`. Read the full brief, both original findings/reproductions, original `probe.py`, `adjacent.py`, `relocate.py`, and condensed `repro.py`. No subagents or git mutations in the source worktree. This report is the only file written there; the main checkout, live state, schedules and holds were untouched.

## Required reproductions

Commands below use repository-root cwd in disposable clone **S** (defined below); `python` is `C:/Users/felip/AppData/Local/Programs/Python/Python315/python.exe`. Complete fixture invocation: `python -u -B C:/Users/felip/AppData/Local/Temp/r4f/repro.py C:/Users/felip/AppData/Local/Temp/r4s-f290a792` (exit **0**, `S/repro.log`). Setup and mutations are in that script, following the original fixtures.

| Finding | Verdict | Mutation and exact check commands | Exit codes and relevant output |
|---|---|---|---|
| R04-N1, A: deleted evidence | RESOLVED | Delete `Theory_work/WaveT/SOLFIX3/reviews/w-evidence.md` (`ev.unlink()`). Run `python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:W`, then `python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:Y`. | **1 / 1**. W: `A1-evidence`, `evidence 'reviews/w-evidence.md' resolves to no file`. Y: `A5-accepted`, W's `accept record is stale`; `REFUSED; 1 acceptance ERROR, 0 other ERROR`. |
| R04-N1, B: withdrawn council outcome | RESOLVED | Restore evidence; replace `gates=PASS` with `gates=FAIL` in `reviews/w-sol.md`. Same two commands above. | **1 / 1**. W: `A4-council`, `verdict gates=FAIL (not all gates PASS)`. Y: `A5-accepted`, stale W record; `REFUSED; 1 acceptance ERROR, 0 other ERROR`. |
| R04-N2: statement provenance | RESOLVED | Copy the statement unchanged to `Theory_work/WaveT/r04-relocated.md`; fixture invokes `python -B Theory_work/INFRA/tools/registry.py set SOLFIX3:W file=Theory_work/WaveT/r04-relocated.md --reason reloc`. Same two check commands above. | Checks **1 / 1**. W: `A4-council`, `no Theory_work/WaveT/reviews/MANIFEST_*.txt has the header ...`. Y: `A5-accepted`, stale W record; `REFUSED; 1 acceptance ERROR, 0 other ERROR`. |

Passing control: `python -B Theory_work/INFRA/tools/check.py --quiet --acceptance SOLFIX3:W --record` exits **0**, recording `v1.0.0 fp2:bd9dfd52b57199ac8da23e65`; Y acceptance exits **0** before mutations and after restoration. Editing the evidence content while leaving it present also refuses Y (**1**, A5 stale). The condensed script's final `['C Y']` warning is not a reproduced defect: C attempts a non-settable `status_source` edit, explicitly excluded by the brief; its unchanged control passes.

## Additional invalidation review

**New findings: none found.** Examined identity construction, artifact resolution, memoised per-claim revalidation, graph traversal, same-run handling, staged recording, and frozen-boundary validation. Additional executable fixture: `python -u -B extra.py C:/Users/felip/AppData/Local/Temp/r4s-f290a792` (exit **0**, source `S/extra.py`, full commands/outputs `S/extra.log`):

- Same invocation `check.py --quiet --acceptance SOLFIX3:W SOLFIX3:Y --record`: valid control **0**; deleted W evidence **1**, A1-evidence, `record: nothing recorded`. The same-run A5 exemption does not bypass W's own checks.
- Add an alias naming W: Y `--record` **1**, A5 stale. Edit SOLFIX3's tickets.tsv folder: Y **1**, including A5 stale (its own A4 also fails). Restore metadata after each test.
- Replace W's accept stamps with old `v1.0.0 fp:0123456789abcdef`: Y **1**, A5 `predates the fp2 acceptance identity`; nothing recorded. Restore events afterward.
- `python -B Theory_work/INFRA/tools/ingest.py claims C:/Users/felip/AppData/Local/Temp/r4s-f290a792/extra.jsonl --staged --record`: **0**, committed claims and accept events for Z consuming Y. Live Z acceptance **0**. Staged and live stamps both `v1.0.0 fp2:ab86b883b385ba25df2e5de6`.
- Delete W evidence with Z -> Y -> W: Z `--record` **1**, A5 explicitly names that transitive path; nothing recorded.
- Corrected boundary fixture `python -u -B legacy.py C:/Users/felip/AppData/Local/Temp/r4s-f290a792` (**0**, `S/legacy.log`): validated baseline **128**, no problems. Append W as a correctly formatted id/version/hash row; `python -B Theory_work/INFRA/tools/check.py --quiet --only L1` exits **1**, `1 row(s) not there (e.g. SOLFIX3:W), 0 missing`; boundary restored to **128**, no problems. The first extra.py boundary attempt used the generic TSV reader on this special-format file and only tested malformed-file refusal; legacy.py corrects that fixture and is the relevant widening result.

## Full regression suite

`python -B Theory_work/INFRA/tools/test_lifecycle.py`, cwd **U**: waited for the full process and cleanup to finish; **exit 0, 134 PASS, 0 FAIL**. All seven new R04 scenarios pass, including unchanged-identity ticket-content revalidation and old-format migration. Full output: `U/suite.log`. Dedicated sandbox: `C:/Users/felip/AppData/Local/Temp/bvs-ci-sandboxes/sb-k_l1pcm5` (removed by suite cleanup). Source-registry SHA-256 before/after: `42110C33DA177149F0391B95F0BA34D5BD30DD3E372E30F37778532327AB2439`, unchanged.

Reviewer setup correction: an earlier full attempt in S completed with exit 1, 124 PASS / 10 FAIL (`S/suite.log`). I had run standalone probes in that same source clone, overlooking that test_lifecycle.py reloads LIVE_INFRA/registry partway through. Those probe rows contaminated the acceptance controls. That result is invalid as product evidence. I then created U, copied the fixes, ran the entire suite again without other fixture mutations in U, and waited for the clean result above. No product or test code was changed to obtain the passing result.

## Isolation and scratch inventory

Fresh clone **S** = `C:/Users/felip/AppData/Local/Temp/r4s-f290a792`, created with `git -c core.longpaths=true clone --no-hardlinks --quiet -c core.longpaths=true C:/Users/felip/BVS-wt/INFRA-R04 <S>`. Copied source `Theory_work/INFRA/tools/*.py` and `Theory_work/INFRA/LIFECYCLE.md` into it before execution. SHA-256 comparisons confirmed all four modified review targets match the source worktree. The valid full-suite run uses a separate dedicated fresh clone **U** = `C:/Users/felip/AppData/Local/Temp/r4s-0174b535`, created with the same clone/copy commands. No standalone probes run in U. Standalone mutations stayed in S; suite fixtures stayed in U's sandbox. Did not reuse `r4s-34ee5984`.

Retained dedicated-suite evidence: `U/suite.log`, `U/registry-baseline.sha256`. Retained standalone scratch evidence: `S/repro.log`, `S/extra.py`, `S/extra.jsonl`, `S/extra.log`, `S/legacy.py`, `S/legacy.log`, `S/suite.log`; condensed fixture also writes `C:/Users/felip/AppData/Local/Temp/fixture.jsonl`. Original fixture directories were read only. This is a software acceptance/invalidation review, not certification of the mathematical claims.



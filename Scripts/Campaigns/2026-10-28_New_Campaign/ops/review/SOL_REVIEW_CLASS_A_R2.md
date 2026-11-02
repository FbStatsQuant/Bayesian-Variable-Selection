# Independent review: class-A cleanup, round 2

Overall verdict: **APPROVE WITH FIXES**. A1's data-safety blockers are resolved; A2 must wait for F1-F2. All new SSH must satisfy F3. This is conditional execution approval, not a claim that cleanup has occurred.
Scope: only the named local files were read; local source/list SHA-256 values were checked. No SSH, deletion tools, simulations, or source-data rehashes were run. Only this verdict file was written.

## Per-item verdicts

| Item | Verdict | Execution conditions |
|---|---|---|
| A1.1 | APPROVE WITH FIXES | F3 only; use the exact allowlisted results base and authenticated 4,800-file list; existing remote recheck must pass. No remapping is needed. |
| A1.2 | APPROVE WITH FIXES | F3 only; same conditions for the p1000 base and its own 4,800-file list. |
| A1.3 | APPROVE WITH FIXES | F3 only; pass the authenticated 55,024-file list AND the 34-link list. Remove link objects only; retain the promised README record. |
| A2.1 | APPROVE WITH FIXES | F1-F3; after A1, transfer the complete remainder to the stated empty destination, obtain VERIFIED, then use manifest-gated deletion and save receipts. |
| A2.2 | APPROVE WITH FIXES | F1-F3; transfer the complete folder, not just partC; obtain VERIFIED, save receipts, and leave the promised MOVED pointer. |
| A3 | APPROVE | Classification of the two explicitly listed owned temporary paths only. Already reported removed; no repeat deletion. This does not independently certify the historical command/host. |

## Round-1 findings

| # | Status | Assessment |
|---|---|---|
| 1 | resolved | The earlier mismatch diagnosis was incorrect: inv3.sh:3,7-8 hashes from BASE; the deployment list proves the nested results/prod_<run>/ layout. |
| 2 | resolved | Canonical exact bases, strict file paths, and equality with non-following find confine A1 to its approved trees. |
| 3 | open | A1's main checked inventories/deletion and guard are improved; remote_pack still masks command failures: N1-N2 below. |
| 4 | resolved | Accept OPS as sole writer and no jobs as stipulated. Private manifest copies and enumerated unlink replace recursive deletion. No additional locking machinery required. N2 concerns a failed queue query, not a demand for stronger writer exclusion. |
| 5 | resolved | Exact SHA-pinned link inventory is compared and only approved links are unlinked; the 31 external/3 internal distinction is corrected. |
| 6 | resolved | Exact A1/A2 legacy targets, canonical scope checks and ownership/type inventories address ordinary execution; N1 covers failed inventories. No MOVED pointers occur in the supplied target hash lists. |
| 7 | resolved | All three reports bind current list bytes, verifier digest, mapping and timestamp; recomputed digests match. Current A1 paths are the previously reviewed ordinary paths. |
| 8 | resolved | Unsupported types explicitly refused; skipped tar members must equal manifest link names; link metadata survives in receipts. |
| 9 | resolved | Global status is PENDING; A2 receipts are future execution gates. A3 is separately identified as historical with exact names; 23 local bundle files exist. |
| 10 | open | OPS_RESPONSE_R1.md:16 acknowledges loginx2, while charter section 3 explicitly requires loginx3 and no other login node. Merely naming the ssh alias does not reconcile this. |
| 11 | resolved | Both du calls check status; quota fields must be numeric; nonzero quota status is deliberately tolerated for soft-limit reporting. Test overrides require explicit opt-in. |
| 12 | resolved | B/C holds remain; A3 is explicitly listed outside BVS. No broader deletion authorization follows. |

## Evidence checked

- remote_pack.sh, verified_delete.sh and guard.sh byte hashes equal staged_tools.sha256; tooltest3_raw.txt:1-3 confirms all three remote checks. Local verifier SHA matches all three JSON reports.
- A1 lists contain 4,800 / 4,800 / 55,024 rows; SHA-256 values equal the respective reports. Reports show zero missing/mismatch and 1,097,537,311 / 2,905,373,304 / 321,924,368 matched bytes.
- Whole-deployment list: 23,053 rows, including exactly 4,800 under each nested production results prefix. Remainder count is therefore 13,453. Profiling list: 16,436 rows.
- A1 link counts: 0 / 0 / 34; Others link-list SHA is 42f3bb5b954ff8d51c16c33902473832dfa185083870a6cce43f1b777c21c597. A2 inventories contain 3 / 5 links with ordinary names/targets.
- Accept remote_pack/guard cases in tooltest2; discard its CRLF verified_delete cases and use tooltest3's refusals plus successful removal. OPS_LOG.md:12-16 records two dummy pulls/deletes; only the second demonstrates the hardened tool generation. These tests do not inject command failures.
- Frozen benchmark roots are outside all approved legacy bases; no symlink targets are followed during inventory or unlink. Felipe's current production-deletion authorization supersedes OUTPUTS.md:25's historical stop.

## Remaining/new defects (paths relative to ops/)

**N1 - HIGH, continuation of R1 #3: transfer/remote_pack.sh:33-41,48,55.** manifest_to is invoked on the left of `||`. Bash suppresses errexit throughout that function, including its subshell; setting `-e` inside does not repair this context. A failed cd, find, sort or sha256sum can be followed by successful commands and a zero function return. In particular, a failed ownership traversal can yield a zero count, allowing that safety gate to pass. Python's counts and the delete digest catch many incomplete manifests, but do not prove ownership checks succeeded. Also, find substitutions inside the mount comparison hide producer status even with ordinary errexit. This is a static finding, not an observed loss.

**N2 - HIGH, new: transfer/remote_pack.sh:13,53.** With no outer errexit, a failing squeue that emits no stdout makes the pipefail assignment nonzero, but execution continues; wc supplies 0 and the next test passes. Deletion can proceed without establishing the required empty queue. verified_delete.sh:54 does not have this defect because its standalone assignment runs under active errexit.

## Exact fixes required before execution

**F1 (A2 only):** Make manifest_to explicitly propagate every cd, enumeration, sort, hash and output failure, including producers inside substitutions; do not rely on errexit inside a conditionally invoked function. Also explicitly check temporary-file creation, manifest digest/path-list generation, directory pruning and final enumeration in delete mode, so failure cannot reach a success report. Keep manifest stdout empty on failure and retain unexpected entries.

**F2 (A2 only):** Capture/check squeue's own exit status before accepting empty output; any query error must refuse deletion. Have OPS save focused remote tests showing failed inventory/hash commands and failed squeue give nonzero status and preserve the dummy target, plus a successful normal case. Re-stage changed tools and record matching local/remote SHA-256. No extra reviewer SSH or full production dry run is required.

**F3 (all new SSH):** Reconcile host authorization before connecting: use the charter-authorized loginx3, or record a superseding authorized loginx2 instruction and align the charter. OPS's explanation alone is not that authorization. This is a policy prerequisite, not an additional A1 data-copy defect.

No further code changes, transfers of A1 data, symlink-target copies, or concurrency machinery are required for this approval. Preserve the standard command/status/hash/receipt logs and the existing B/C holds.

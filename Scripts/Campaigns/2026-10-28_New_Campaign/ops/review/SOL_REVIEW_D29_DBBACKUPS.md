# Independent Sol review: D29 Codex db-backups deletion list

Review time: 2026-10-30T00:39:43Z. Reviewer: Sol 6.1, independent review only.

## Verdict: REJECT

The inventory partition and the scope of all 89 proposed rows are correct. However, the current evidence does not establish that these NFS-shared databases are unused on other nodes, and the executor has fail-open checks. Do not execute deletion from this submission.

**Per-row decision: all deletion-list rows 1-89 are REJECTED for deletion / KEEP pending resolution of the blocking findings. Accepted for execution: 0 rows, 0 KB.** All 89 are valid, in-scope *candidates* under the snapshot's age/top-three rules, totaling 168,128 KB; no individual row has a partition, size, filename, or authorization-category defect. This distinction is intentional: a correct candidate list is not evidence that its databases are safe to unlink.

Only this review file was written. No SSH, NOTS connection, deletion, executor run, or changes to the reviewed inputs were performed. The verification below was a local, read-only Python parsing check explicitly requested for this review; it was not a remote computational workload.

## Inputs and identity

Read the raw listing, both TSVs, the D28 and D29 sections of CLEANUP_LOG.md, and all 43 lines of scaffold/d29_dbbackups_delete.sh. Executor line numbers below refer to that exact snapshot.

| Input | SHA-256 |
|---|---|
| evidence/ops4_dbbackups_list_raw.txt | `32050e263f399c51b542db8236944e306c0c3d1e4571ee3774fe9a3f3e3bbffe` |
| evidence/ops4_dbbackups_delete_list.tsv | `b5a2f47d5ff1537d305211b26738551e91d6fee51422f494a1e43c0c84571e9c` |
| evidence/ops4_dbbackups_keep_list.tsv | `ec1eb02e525cf5e907563cff41547027c31c0de621a5b268a2d6cd51ac31a30e` |
| scaffold/d29_dbbackups_delete.sh | `fefb88d29b574c5a00c8c7f7449d348c2c05404848f2287387d5c9535e9e0842` |

The deletion-list hash matches the hash supplied for review. All four files have LF line endings, no CRLF and no UTF-8 BOM, and end in LF. The delete TSV has 90 lines (one header plus 89 rows); the script has 43.

## A. Independent partition and arithmetic verification: PASS

The read-only Python check parsed the raw depth-one `d<TAB>name` records separately from its pipe-delimited per-folder records. It checked uniqueness and set equality; parsed both TSVs with csv.DictReader using a tab delimiter; checked disjoint/exhaustive membership; recomputed retention from the raw mtimes; compared every delete-row field, every keep-row size/time/reason, and all 89 D29 log-table rows against the raw records. The check returned `errors: []` and exit status 0.

| Quantity independently derived from raw records | Result |
|---|---:|
| Depth-one directories / distinct per-folder records | 109 / 109 |
| Sum of per-folder du values | 188,340 KB |
| Files in those folders | 325 |
| Delete candidates | 89 folders, 168,128 KB, 265 files |
| Kept folders | 20 folders, 20,212 KB, 60 files |
| Sum of partitions | 109 folders, 188,340 KB, 325 files |
| Duplicate, missing, extra, or overlapping paths | 0 |

`now_epoch = 1793320544`; the inclusive keep threshold is `1793234144` (2026-10-29T00:35:44Z). Exactly 20 folders have newest mtime >= that threshold, and all are kept. The top three are a subset of those 20:

| Folder | Newest mtime epoch | KB |
|---|---:|---:|
| sqlite-1793319865-0 | 1793320397 | 252 |
| sqlite-1793318060-0 | 1793319160 | 312 |
| sqlite-1793317157-0 | 1793318237 | 240 |

Their sizes sum to 804 KB; the other 17 retained folders sum to 19,408 KB. The open folder shown by lsof, sqlite-1793319865-0, is kept: codex PID 550200 holds its SQLite/WAL/SHM files. The shell/lsof/head cwd entries are for the parent db-backups directory, not a deletion candidate. The raw listing also reports another codex PID, 3794027; its presence is not evidence that all possible users of old folders have been excluded.

The youngest deletion candidate, row 1 (sqlite-1793233767-0), has newest mtime 1793233808: age 86,736 seconds, only 336 seconds beyond the 24-hour boundary at inventory time. It satisfies the stated strict age rule; the narrow margin is not a partition error. No folder is exactly on the cutoff.

188,340 KB is the sum of the 109 raw per-folder du values. It need not equal a du of their parent including the parent's own blocks. D28's earlier 188,344 KB parent figure is also from an earlier inventory; it is not a mismatch in the D29 partition. Disk allocation from du is distinct from the logical file byte sizes in the final field.

## B. Authorization-category verification: PASS for every candidate

All 89 paths match exactly `/home/fb31/.codex/db-backups/sqlite-[0-9]+-0`. Their raw contents are exclusively regular files named logs_2.sqlite, logs_2.sqlite-shm, or logs_2.sqlite-wal. Row 89 has just logs_2.sqlite; rows 1-88 have all three. The raw symlink section is empty. Nothing on this list is a packages/ Codex program version, VS Code version, top-level ~/.codex/*.sqlite database, session, or other out-of-scope category.

D29 specifically authorizes old databases in db-backups, so D28's earlier database exclusion does not itself disqualify these candidates. Nevertheless, the directory name is not proof of backup semantics: the observed open newest folder establishes that this tree also contains an actively used logs database.

## Numbered findings and concrete fixes

1. **BLOCKING — NFS-wide non-use remains unproven (all rows 1-89).** lsof on loginx2 establishes local positive opens; it cannot establish the absence of an open file on another NFS client. A quiet or idle Codex process elsewhere can retain an old database without advancing its mtime. Thus age >24 hours, absence from this node's lsof output, and keeping three newer folders are insufficient under the standing rules “anything held open ... is kept” and “if unsure, keep it.” SQLite WAL/SHM files are part of the database's working state; unlinking an in-use set is not established safe by its logs-only contents. The earlier VS Code decision recorded in CLEANUP_LOG.md recognizes the same visibility limit. **Fix:** keep all uncertain folders. Obtain trustworthy cluster-wide non-use evidence through an authorized facility or administrator accessible without OPS contacting another node, and establish a period without writers for execution. If that cannot be obtained, return the decision to HQ/Felipe for an explicit change in the applicable rule or risk authorization; D29 as quoted does not waive it. Do not probe other login nodes. A longer retention window can preserve more diagnostic history but cannot by itself resolve open-file uncertainty.

2. **BLOCKING — lsof and discovery errors can authorize deletion (lines 17, 19, 30-35, 38).** `lsof +D ... 2>/dev/null | grep -q .` treats missing lsof, a failed/incomplete scan, or permission/visibility problems with no stdout as “not open.” stderr is discarded. `set -u` does not propagate command/pipeline failure. The content-check find can fail with no output and be accepted; newest() can return a plausible maximum from a partial traversal; top-three collection and du errors also lack explicit handling. **Fix:** check tool availability and capture complete stdout, stderr, and exit statuses for each scan before evaluating its output. Keep/refuse on unexpected status, warnings, inaccessible entries, timeouts, or incomplete process visibility. Distinguish the documented lsof no-match outcome from actual failures; a generic nonzero/zero test alone is not enough. Check find independently of sort/tail and avoid early-consuming pipelines that obscure producer status. `pipefail` can help but does not replace explicit handling, particularly with head/grep short-circuiting. Preserve diagnostics in the execution evidence.

3. **BLOCKING — retention state is cached rather than rechecked per deletion (lines 16-19, 32-35, 40).** NOW/CUT and TOP3 are taken once before the loop. If newer folders disappear or change during the run, an originally eligible row can become one of the current three newest and still be deleted. TOP3 also admits symlinked directories via `-d` and nonnumeric wildcard names; a discovery error can produce an incomplete retained set. The initial cutoff is conservatively stale as time advances under a stable clock, but it is not a fresh per-row check. **Fix:** immediately before each mutation, obtain a successful fresh inventory of real eligible directories, recompute the top-three set and current cutoff, and keep on ambiguity or scan failure. Reject unexpected candidate types/names rather than allowing them to displace real retained folders. Ensure ties retain at least three folders, conservatively keeping all tied at the boundary. Repeat these gates in the execution run even if a prior dry run passed.

4. **BLOCKING — lexical containment and prechecks do not protect against path replacement or resumed writers (lines 15, 25-40).** The anchored numeric path regex and quoted `rm -rf -- "$path"` correctly prevent traversal strings, option injection, and accidental wildcard expansion. The initial checks also reject a symlink at .codex, db-backups, or the selected leaf, and find normally rejects descendant symlinks/subdirectories. However, other ancestors are not canonicalized, the checked parent or leaf can be replaced after the checks, and files can be opened/created/changed after lsof/mtime validation but before rm. Recursive rm then removes whatever is reachable under that pathname at that moment, including newly added unreviewed contents; a substituted parent can redirect it outside the reviewed tree. **Fix:** validate canonical containment, ancestor/leaf identity, ownership and unexpected mount boundaries; establish exclusive, cluster-wide quiescence respected by every writer before checks and deletion. A private cleanup flock alone does not stop Codex writers. Revalidate identities, exact entries, retention, timestamps and opens directly before mutation, and keep on any change. Prefer unlinking only the verified regular files and then rmdir so unexpected extra entries prevent directory removal, with directory identity preserved throughout. Rechecks alone do not eliminate races if writers remain active; without enforceable quiescence, keep.

5. **SHOULD-FIX — the executor does not bind execution to the reviewed TSV or validate its schema (lines 14, 22-23, 42).** For this exact LF TSV, parsing is correct: path/kb/mt are the first three fields and `rest` absorbs the remaining four. A CRLF conversion of this seven-field TSV would put the trailing CR in the unused rest field, not the path or mt, so it is not the current blocker. Still, tab IFS collapses empty fields, any row whose first field is `path` is silently skipped, duplicate/extra rows are unchecked, and a different valid-path TSV could select folders absent from this reviewed list. An unterminated last line is skipped by the present read loop. **Fix:** authenticate the remote copy against the full reviewed SHA-256 before opening it for deletion; prevalidate the entire exact header, seven nonempty fields, numeric fields, uniqueness and expected row set before any mutation. Use the same immutable validated input for execution. Preserve LF bytes and reject transformations/BOM/CR unless normalized into a newly hashed, reviewed artifact. Preserve the current final newline or handle an unterminated line explicitly. Also verify the reviewed executor hash at deployment; any fixed script needs a new hash and review.

6. **SHOULD-FIX — missing-input and partial-deletion failures can finish with success (lines 38-43).** An unreadable/missing LIST causes loop redirection to fail, but the following SUMMARY echo can still return status 0. An rm failure is counted as `kept_or_failed` even when some files were already removed, and the script also normally returns 0. du failure can produce incorrect accounting. **Fix:** open/validate the list before all work, check every required command, separate unchanged KEEP from FAILED/PARTIAL, return nonzero for operational failures, and verify/report residual contents after any failed mutation. Report freed space only from verified successful removals, with a final accounting check. Save the launch command, host, input/script hashes, start/end times, process identifier, per-row results, stderr and final status in persistent evidence. Never report a partial removal as an intact kept folder.

7. **SHOULD-FIX — deployment usage is partly incorrect and the pinned host is unenforced (lines 3, 14-15).** There is no __LIST__ marker parser or embedded-list support despite the usage comment. With LIST passed as $1, copying the script under /scratch/fb31/New_Campaign is otherwise fine: BASE is absolute and independent of the script directory; the TSV argument must name a file actually present on NOTS. For a piped script, Bash must receive `-s -- REMOTE_LIST_PATH [--yes]`; appending TSV text to the script is unsupported. No host/user gate prevents an accidental run on another login node or local machine. **Fix:** remove the unsupported appended-list instructions, document the two real invocation forms with an explicit remote TSV path, reject extra/unknown arguments, and refuse before scanning unless the actual host is loginx2 and the effective user is fb31. OPS must continue using only the pinned loginx2 connection; this review does not authorize another node.

8. **MINOR — “mtime unchanged” is weaker than an unchanged manifest (lines 17, 32).** newest() truncates the maximum timestamp to integer seconds and compares only that one value. This verifies the recorded aggregate epoch, not every entry's identity, size, timestamp or contents; same-timestamp replacements or preserved mtimes need not change it. The snapshot's >24-hour separation makes ordinary present-time writes detectable before the scan, but does not establish exact identity or eliminate the race in finding 4. **Fix:** describe the guarantee accurately, and for a revised execution snapshot record/recheck the precise directory and per-file identities, names, sizes and high-resolution timestamps (plus content hashes if exact content identity is required). Treat any discrepancy as KEEP; do not invent subsecond values for this older snapshot.

## Other executor conclusions

- Dry-run default is correct: only an exact second argument `--yes` enables the sole rm call. Dry-run still needs the blocking fixes to give meaningful eligibility evidence. No executor mode was run in this review.
- For an unchanged filesystem and this exact trusted list, the loop targets only its listed paths. Syntax alone does not expand deletion to siblings, packages, sessions, or top-level databases. Findings 4 and 5 explain the remaining containment/input exceptions.
- The explicit age predicate `newest < cutoff` correctly keeps equality at 24 hours. The existing local lsof positive-match branch correctly keeps an observed open folder; its negative/error interpretation is the defect.
- Keeping 20 instead of only three is correct under the additional 24-hour procedure. More retention may be sensible for recovery/debug history because these appear to be rolling logs databases, but no alternative age or count supplies the missing cross-node non-use evidence. There is no evidence-based smaller subset of the 89 that can be approved now.

Re-review the revised executor and the evidence resolving findings 1-4 before any deletion. Preserve the currently reviewed inputs unchanged for audit.

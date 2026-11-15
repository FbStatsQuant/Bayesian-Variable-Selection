# INFRA R06 — line-ending-independent hashes (+ two acceptance-path confirmations) — brief (HQ, 2026-11-12)

You are the implementer (Claude Opus 5.5, effort high, provider claude-personal). Worktree `C:/Users/felip/BVS-wt/INFRA-R06`
(branch `infra/R06-eol`, from main 849dfb5, R05 merged). Work only there. **Change no git state** (HQ commits).

## Problem
Council manifests (`Theory_work/Wave3/tools/manifest.py`) hash raw bytes. Frozen trees had mixed LF/CRLF; git (autocrlf)
stores LF blobs, so on any uniform checkout `manifest.py verify` fails although content is identical (audit 2026-11-12:
START 28 CRLF/24 LF, PSHARP 15/14, RM2-PC1 17/40, MISR 0/36). After merging tickets to main, START/PSHARP would not verify
and A4/A5 acceptance would refuse. Decision in `Theory_work/Wave3/HQ_DECISIONS.md` (entry "acceptance audit
dispositions").

## Do (one PR)
1. **Hashes:** `verify`/`bind` accept a recorded hash equal to the hash of the raw content, the LF-normalised content, or
   the CRLF-ised content. Normalise text only (a file containing a NUL byte is hashed raw). New freezes record the
   LF-normalised hash (document it). No existing MANIFEST file may change.
2. **Registry fingerprints** (`sha256`, `status_sha256`, `fp2` in `Theory_work/INFRA/tools/` bvsreg/check/ingest/registry):
   same normalised hash, accepting legacy raw values, so accept records do not go stale between LF and CRLF clones.
3. **Tests** (`test_lifecycle.py`): every existing MANIFEST_*.txt in the repo and on the ticket branches theory/W3-START,
   theory/W3-PSHARP, theory/W3-MISR, theory/W3-RM2 verifies on an LF checkout and on a CRLF checkout (use
   `git -c core.autocrlf=…` clones in your temp folder); a one-byte content edit still fails; a binary file is raw. Full
   suite must pass (currently 146/146) and `check.py --quiet` 0 ERROR. **Wait for them in your run.**
4. **Confirm (and fix if needed) two acceptance paths** the next steps rely on:
   (a) R05 safeguard 4 reads a per-claim `| id | decision |` table that is appended to a council review file as a dated
   **addendum** after its `COUNCIL-VERDICT` line (values ACCEPT / NOT-EXAMINED; NOT-EXAMINED ids must not get a checked
   label); the verdict line stays the binding one and a second verdict line is refused.
   (b) `ingest.py` can take registry blocks from a **carrier file outside the frozen manifest** (`REPORT.md|F.jsonl`
   form) while the coverage rule still requires statement/premise files to be inside the manifest.
   Add a regression test for each.
5. One fresh correctness reviewer: `delegate_task`, provider `codex`, model `gpt-6.1-sol`, reasoningEffort high, mode
   wait; brief `Theory_work/INFRA/R06FIX/BRIEF_sol.md`; output `R06FIX_review_sol.md`: try to make a changed file verify,
   a stale accept stay current, or an addendum/carrier route accept something the council did not. Fix findings (one more
   Sol round at most).
6. `Theory_work/INFRA/R06FIX/REPORT.md`; end your run with a ≤ 10-line summary.

No other agents. Any Claude helper only on provider claude-personal, Opus, effort high max.

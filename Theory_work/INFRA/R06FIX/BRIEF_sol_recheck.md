# R06FIX — Sol re-check (round 2, the last) — brief

Context: software-correctness review of a research-project bookkeeping tool. No security testing is involved.

You are an independent correctness reviewer (Codex GPT-6.1 Sol, effort high). Same rules as round 1
(`Theory_work/INFRA/R06FIX/BRIEF_sol.md` in the worktree `C:/Users/felip/BVS-wt/INFRA-R06`): read that worktree only,
change no git state anywhere, work in disposable clones under a short temp path, start no subagents.

Round 1 (`Theory_work/INFRA/R06FIX/R06FIX_review_sol.md`) found two MAJOR bypasses. The implementer's fixes (uncommitted
in the worktree; `git -C C:/Users/felip/BVS-wt/INFRA-R06 diff`, read only):
- **F1** (`Theory_work/Wave3/tools/manifest.py`: `eol_text`, `lf_normalised`, `sha`, `accepted_hashes`): only
  EOL-normalisable text (no NUL byte, and every CR is the first half of a CRLF pair) is normalised; any other file (NUL,
  or a lone CR such as CR CR LF) is hashed raw only, on freeze and on verify.
- **F2** (`Theory_work/INFRA/tools/bvsreg.py`: `_ACCEPT_DEC`, `seat_table`): a decision is accepted iff the cell is
  `accept` / `accepted` alone, or followed by whitespace and words that do not start with not / no / never / pending /
  withdrawn / rejected. So `ACCEPT=NO`, `ACCEPT/NOT-EXAMINED`, `accepted, no`, `ACCEPT not` are refused.
- Regressions: test_lifecycle.py results "R06FIX F1 ..." and "R06FIX F2 ..." (parser, and staged ingest on the carrier
  and own-checkpoint paths). Docs: LIFECYCLE.md §4.1 "Line endings", item 2 of "Checkpoint status source".

## Do
1. Reproduce your F1 and F2 probes against the fixed tools: both must now refuse.
2. Try to bypass the fixes (other CR / NUL placements, variant collisions between EOL-normalisable and raw-hashed
   files, legacy raw manifests of files with lone CR, Unicode line separators; decision strings with punctuation,
   Markdown, non-breaking or other Unicode whitespace, negations after remarks). Note any documented workflow the
   stricter grammar breaks (the real seat tables on theory/W3-START/PSHARP/MISR/RM2 use only `accepted`,
   `accepted (…)` and `accepted with non-blocking remarks …`).
3. Spot-check that the real-data results still hold: W3-START staged acceptance PASS (21 claims) on fresh LF and CRLF
   clones; new-tool verify on LF/CRLF clones equals old-tool verify on the frozen worktrees for the 28 branch manifests.
4. Run the full suite once in a fresh clone with the changes and no other probes (expected all PASS).

## Output
Append a section `## Round 2 (re-check)` to `C:/Users/felip/BVS-wt/INFRA-R06/Theory_work/INFRA/R06FIX/R06FIX_review_sol.md`
(the only file you write): verdict line first (F1, F2 RESOLVED / NOT RESOLVED; new findings or none), each new finding
with severity, reproduction and fix direction; suite result; scratch paths. End with a ≤ 5-line summary.

# BRIEF — diff check SC5, v1.3.3 → v1.3.4 (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole brief.
Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START` (paths below are relative to it). **Change no git
state** (read-only git commands such as `git show`, `git diff` are allowed). **Write exactly one file:**
`Theory_work/Wave3/W3-START/reviews/SC5_diff_check_sol.md`. Do not edit any other file. Do not start subagents. Use no
effort setting above high. If you run code, do not let it write into the repository (`citecheck.py` accepts an
output path: `python Theory_work/Wave3/W3-START/citecheck.py <file outside the repository>`).

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START/reviews/MANIFEST_SC5.txt`. Its first line is
`MANIFEST e6d594199cb7f0c527c091cfdb5785ec155ba7b5dc17ecaa88debfee9e19415c`. **Quote this digest line verbatim at the
top of your review.** You may run `python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START
Theory_work/Wave3/W3-START/reviews/MANIFEST_SC5.txt`.

## Files you may read
The files listed in that manifest: the ticket's `STATEMENT.md` (v1.3.4), `REPORT.md`, `PLAN.md`, `BRIEF.md`,
`ASSUMPTION_MAP.md`, `citecheck.py`, the `lemmas/` folder (L1–L11), the `numerics/` folder, and the external inputs of
`Theory_work/Wave3/W3-START/reviews/INPUTS.txt`. In addition: the previous committed version of every ticket file,
with `git show HEAD:<path>` and `git diff HEAD -- Theory_work/Wave3/W3-START` (HEAD holds v1.3.3); and, for context
only, `Theory_work/Wave3/PROTOCOL.md` and `Theory_work/INFRA/registry/claims.tsv` (they are not part of the frozen
content). Do not read any other file in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, or
any `CHECKPOINT*.md`.

## What this review is
Version 1.3.3 of the statement, the eleven proof files and the report were reviewed as a whole. Version 1.3.4 is
meant to contain **only editorial changes** to that reviewed content. The intended changes are:
1. `STATEMENT.md`: version line; "for some constant C" added to the Gaussian-row summary of §0; the code pin phrased as
   "the CORE tree as of commit 72785fe"; Setting F described as C-GROW's setting "with s₀ ≥ 0 and any fixed A > 0
   allowed"; (N1) repeats the condition "κ_V > ½" of the exact-order clause.
2. `lemmas/L3_LEAK.md`: Lemma L3.3 displays the bound with the constant e^{2κ_E+ς_n} as well as e^{2κ_E+1}.
3. `ASSUMPTION_MAP.md`: rewritten as one map of the final statement (the previous file had a body written for an
   early version and three appended correction sections).
4. `REPORT.md`: version, "for some constant C", one cross-reference to the assumption map.
5. `numerics/RESULTS.md`: two sentences reworded as observations.
6. `citecheck.py`: optional output-path argument.
7. `reviews/INPUTS.txt`: the wave documents and the registry table removed from the list of external inputs (they
   are not proof premises).

Your task:
A. **Completeness.** List every difference between HEAD and the working tree in the ticket folder outside `reviews/`,
   `LOG.md` and `CHECKPOINT*.md` (plus `reviews/INPUTS.txt`). Is there any change not covered by the seven items?
B. **Classification.** For each change decide: *editorial only* (no hypothesis, conclusion, proof step, premise or
   code pin changes in meaning), or *substantive*. For the items that touch mathematics, check them:
   * (N1): is "under F2 with η′ = 0 and κ_V > ½ the order is exact" what Corollary F2 and `lemmas/L7_NEC.md` /
     `lemmas/L6_COROLLARIES.md` state and prove?
   * Setting F: do the proofs use A ≥ 1 or s₀ ≥ 1 anywhere? Is the sentence about C-GROW's setting accurate
     (`Theory_work/Wave1C/C-GROW/STATEMENT.md:51-64`)?
   * Code pin: is 72785fe the last commit touching `Scripts/SMC_BVS/core/` (`git log -1 -- Scripts/SMC_BVS/core`), and
     do the `path:line` pins still point at the cited code?
   * L3.3: does the proof of the lemma give e^{2κ_E+ς_n}, with ς_n as defined in L3.3 and ς_n ≤ 1 for n ≥ n₂? Is the
     constant c_L of Proposition L3.4, and every later use (`lemmas/L5_ASM_STARTF.md`, `lemmas/L10_INTERFACES.md`),
     unaffected?
   * `ASSUMPTION_MAP.md`: does the new map say anything that the statement, the proofs or the numerics reports do
     not support? In particular its statements about necessity (what is necessary, what is only sufficient for the
     proof route), about the partition-free limit (N2), and about what the numerics do and do not show. Does it drop
     anything of substance that the previous file (with its correction sections) said correctly?
   * `REPORT.md` and `numerics/RESULTS.md`: are the reworded sentences accurate?
C. **External inputs.** With the pruned list, is every file that a proof or a pin relies on still covered (pinned code;
   sources of arguments; the consumers' statement)? Is any remaining entry a wave document or a registry table?
D. **Citations.** Run the citation check to an output file outside the repository and report its count line.

## Output format (in your one file)
```
MANIFEST <digest>            (verbatim first line of the manifest)
Verdict: EDITORIAL ONLY | EDITORIAL ONLY WITH CHANGES | SUBSTANTIVE CHANGE FOUND
Findings: numbered; each with class (CRITICAL / MAJOR / MINOR), location (file:line), the problem and the exact
          change you require. For a verdict of EDITORIAL ONLY, state explicitly: "I attest that the changes from v1.3.3
          to v1.3.4 are editorial only."
Per-change table: each difference found under A — editorial | substantive, with a one-line reason.
Checks performed. Not checked.
```
End your reply with the verdict line and the path of your file.

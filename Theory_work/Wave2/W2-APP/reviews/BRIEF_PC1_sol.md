# BRIEF PC1 — post-council check of W2-APP (one fresh reviewer, Codex gpt-6.1-sol, reasoning high)

HQ, 2026-11-15. You are a fresh reviewer for ticket W2-APP (Theory Wave 2, an applicability map for a Bayesian
variable-selection method). You have never reviewed this ticket. Break things if they are broken.

## Workspace (strict)
- Read files ONLY under `/home/fb31/BVS-wt/record-1115/` (a git worktree). All paths below are relative to it.
- Write exactly ONE file: `Theory_work/Wave2/W2-APP/reviews/PC1_postcouncil_check_sol.md`. No other writes, no git
  operations, no subagents.

## Background (facts, not conclusions)
W2-APP passed council round 3 (C3) with two seats. After C3, edits were made to the ticket files; the lead's list of
those edits is `reviews/C3_disposition.md`. The ticket has a single git commit, so no snapshot of the exact text the
C3 seats read survives. The current ticket files are frozen as
`MANIFEST 72ac86f9fd0ca9fef850562ca9680d328de7dcef451c907bb693b925a2b31460` (`reviews/MANIFEST_PC1.txt`, 126 files;
`python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave2/W2-APP Theory_work/Wave2/W2-APP/reviews/MANIFEST_PC1.txt`
checks it). Your job is to establish whether anything of mathematical substance changed after C3.

## Inputs
- `Theory_work/Wave2/W2-APP/reviews/C3_council_sol.md`, `reviews/C3_council_opus.md` (the two C3 seat reviews:
  what they read, quote and require), `reviews/C3_disposition.md` (the post-council edit list).
- The frozen current files: everything listed in `Theory_work/Wave2/W2-APP/reviews/MANIFEST_PC1.txt` (in particular
  `STATEMENT.md`, `REPORT.md`, `EMPIRICAL.md`, `lemmas/L1_POST.md` … `lemmas/L6_ENUM.md`, `numerics/LEAD_READING.md`).
- For item (b): `Theory_work/Wave2/W2-FAC-A/REPORT.md:20-53` (the source that the FAC-A sync quotes).
- Any source a lemma cites, if you need it to judge whether a change is mathematical.

## Tasks
(a) For EACH item of `C3_disposition.md`: locate the edit in the current text; confirm it is the edit the disposition
    describes (and, where it answers a seat issue, what that issue asked for); classify it EDITORIAL (wording, notation,
    status transcription, presentation) or MATHEMATICAL (any change to a hypothesis, conclusion, scope, proof step,
    constant, or to what the applicability map asserts is covered).
(b) Check the FAC-A sync into the family map line by line — `STATEMENT.md:94`, `lemmas/L4_families.md:149` (and the
    corresponding REPORT / EMPIRICAL sentences) — against `Theory_work/Wave2/W2-FAC-A/REPORT.md:20-53`: verbatim
    status, the narrowed class, the growth condition, what stays open. Say whether the map now asserts anything that
    the C3 seats did not review, and whether it is faithful to the source.
(c) Look for ANY other change of mathematical content you can detect relative to what the C3 reviews quote or
    describe (line references, quoted text, the statements and proof steps they say they re-derived, version labels).
(d) Per-claim decision table for these 11 registry claims (local id → statement location in the current files):
    POST (`lemmas/L1_POST.md:27-33`), CT (`lemmas/L2_CT.md:9-13`), CD (`lemmas/L2_CT.md:41-50`), Thm-LOC
    (`lemmas/L3_LOC.md:34-38`), L3.6 (`lemmas/L3_LOC.md:99`), LOC-B (`lemmas/L3_LOC.md:169-178`), VN
    (`lemmas/L5_VN.md:23-26`), VN-routes (`lemmas/L5_VN.md:28-34`), Ex-STAR (`lemmas/L5_VN.md:64-72`), Family-map
    (`lemmas/L4_families.md:152-171`), ENUM (`lemmas/L6_ENUM.md:16-22`).
    ACCEPT means: the C3 pass (both seats actually examined this claim, by their own text) plus your check covers the
    current text of this claim. REJECT means a mathematical change or defect you found. NOT-EXAMINED means a C3 seat
    did not examine it, or you could not settle it. Use exactly this table form (remarks go below it, not in it):

    | id | decision |
    |---|---|
    | W2-APP:POST | ACCEPT |

    (cells exactly `ACCEPT`, `REJECT` or `NOT-EXAMINED`; one row per claim, all 11 rows, ids `W2-APP:<local id>`).
(e) Findings: tag each **C** (correctness), **S** (strength: claims more than proved, or uses an unstated
    hypothesis), **F** (faithfulness: to the code as pinned, to a cited source, or to STATEMENT) or **E** (editorial).
    Only C/S/F block. You must give `gates=FAIL` if you hold any C, S or F finding of your own.

## Verdict line (mandatory, machine-checked)
End the file with exactly ONE line of its own, in exactly this form (no other text on the line; backticks allowed):

```
COUNCIL-VERDICT round=R3 manifest=72ac86f9fd0ca9fef850562ca9680d328de7dcef451c907bb693b925a2b31460 seat=pc1-sol score=<x.y> gates=PASS|FAIL
```

`score` (0.0–10.0) reflects C/S/F only. `gates=PASS` only if you hold no C, S or F finding on exactly this manifest.
Write no other line containing `COUNCIL-VERDICT`.

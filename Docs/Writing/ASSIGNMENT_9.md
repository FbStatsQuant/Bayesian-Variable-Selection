# Writing Department: Assignment 9, the short readable version (HQ, 2026-11-24; owner's order, URGENT)

## Owner, binding
A6, A7 and A8 are "unreadable", "too robotic", "AI slop". He wants **something much shorter and clearer, quickly**, and
will give feedback on that version. Owner notes so far: `Docs/Writing/OWNER_NOTES_A9.md` (keep Table 3 of A6, "The
assumptions at a glance").

## Staffing (owner's order)
- **One Fable 5.2 agent on Claude Work (CW), effort high**, started by the Writing manager. Fable writes the document
  itself.
- The manager only sets it up, compiles and delivers. No Sol read, no clarity read, no council, no Sonnet rewrite of
  Fable's prose. The manager fixes only compile errors and checks that no statement contradicts spec.tex (a spot check).

## What to write
A short PDF, about 8–10 pages, written the way a good statistician writes a talk handout: plain prose, short
sentences, standard notation, no internal ids, no registry jargon, no "status lines", no hedging boilerplate.
1. **The model and the priors:** half a page.
2. **The sampler:** half a page to one page, the idea and the steps; the 1M engine in two sentences.
3. **The assumptions:** Table 3 of A6 (that format; tightened), plus each assumption stated once, cleanly, only as
   formally as needed.
4. **The theorems:**
   - each proved result as a clean statement plus one or two sentences on what it means;
   - then the planned results (P1–P5, including the fixed-p KL misspecification target), each short and marked planned.
5. Nothing else: no appendices, no supplement list, no Song–Liang essays beyond the table column.

**Sources:** `manuscript/spec/spec.tex` (statements), `manuscript/owner_review.tex` and `sections/or5_assumptions.tex`
(Table 3), `Theory_work/Dept/assess/MIS_KL/ASSESS_fable.md` (P5). Fable may simplify a statement for readability only
if it stays true. A simplified statement says "simplified; full version in spec.tex, Thm k".

## Output
`manuscript/short/smc_bvs_short_<date>.pdf`, pushed to main. Send HQ one start line with an ETA (aim: a few hours),
then one delivery line.

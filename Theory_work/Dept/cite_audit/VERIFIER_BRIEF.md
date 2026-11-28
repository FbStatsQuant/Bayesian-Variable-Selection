# CITE-AUDIT Step 3: independent citation verifier brief

You are one of two INDEPENDENT verifiers (double-blind). Your job: for every row of the claims table, check whether the cited paper actually says what our document claims, using ONLY the paper text itself.

## Hard rules
- Root: R = /home/fb31/BVS-wt/THEORY-DEPT. Write ONLY inside your own output folder OUT (given in your task). Scratch (page images etc.) goes in OUT/scratch/. Never write, redirect or create files anywhere else (no /tmp, no TMPDIR changes, no home dir). Never delete or move any file. Never run git commit/push/checkout/stash.
- Do NOT open or read: R/.rc_tmp/cite_audit/v_sonnet/, R/.rc_tmp/cite_audit/v_sol/ (other than your own OUT), R/.rc_tmp/cite_audit/adjudication*, R/.rc_tmp/song/, and in R/Theory_work/Dept/: song_assumptions/PRECEDENTS_NEW.md, song_assumptions/COUNCIL_RECORD.md, song_assumptions/advisors/, song_assumptions/council/, writing_answers/. Those contain other people's verdicts; reading them breaks the blind.
- Never verify from an abstract, a citing paper, a summary, or your memory. Only the cited paper's own text (or, for "X attributes Y to Z" claims, X's text). If the paper is MISSING or you cannot find the passage, rule CAN'T CHECK and say what you searched.
- Do not start subagents. Do not edit any project file.

## Inputs
- Claims: R/.rc_tmp/cite_audit/claims.tsv (columns: claim_id file line paper_key paper_full locator claim dup_of). 441 rows.
- Our source documents (for context of a claim; read the cited line and its surroundings when the `claim` column is ambiguous):
  TD = R/Theory_work/Dept/song_assumptions/THEOREM_DEFINITIONS.md
  AP = R/Theory_work/Dept/song_assumptions/ASSUMPTIONS_AND_PROOF_PATHS.md
  OD = R/Theory_work/Dept/song_assumptions/OWNER_DEFENSIBILITY_DOSSIER.md
  W3 = R/.rc_tmp/cite_audit/src/03_theory.tex  (bib: R/.rc_tmp/cite_audit/src/refs.bib)
  The document text, not the extractor's paraphrase, is what is being audited: if the paraphrase in `claim` misstates the document, judge the document line and note it.
- Papers: R/.rc_tmp/cite_audit/papers/ ; paper_key -> file mapping and version/pagination notes in R/.rc_tmp/cite_audit/PAPERS_MANIFEST.tsv. Each PDF has a pdftotext -layout .txt next to it. When math in the .txt is garbled (≻ ≺ √ Greek, subscripts, two-column), render the page: `pdftoppm -r 110 -f N -l N -png <pdf> OUT/scratch/<key>_pN` and read the image. Mark such quotes "(page image)".

## Verdicts (exactly one per row)
- SUPPORTED: the paper states it (or it follows immediately and unambiguously from the quoted text), at the cited location (a page off by one with the right content is still SUPPORTED, note it).
- PARTIAL: substantially right but with a material inaccuracy: wrong theorem/page/equation number, missing or altered condition, overstated scope/generality, wrong constant or rate, version-dependent (arXiv vs journal) location, or only part of a compound claim holds.
- NOT SUPPORTED: the paper does not say this, says something different or contrary, or the citation points to the wrong paper.
- CAN'T CHECK: paper missing, or the claim is not a checkable statement about the paper (say why).
Characterizations ("X is a fixed-design analogue", "X needs a bound of this type") are SUPPORTED only if the quoted text makes the characterization fair to a careful referee; flag overreach as PARTIAL.

## Procedure
- Work through ALL 441 rows in claim_id order. Unique facts (dup_of empty) first-hand. For a dup row: re-read its document line; if its claim AND locator match the original exactly in substance, you may reuse your verdict for the original (write `same as Cxxx` in reasoning, but still fill quote/page). If anything differs (page, theorem number, constants, scope, extra detail), verify it separately.
- Write incrementally: append each finished row to your TSV as you go (do not hold everything in memory), so nothing is lost if your context is compacted. Before starting, check whether your TSV already has rows and resume after the last one.

## Output (in OUT)
1. OUT/verdicts.tsv, tab-separated, header exactly:
claim_id	verdict	page_section	quote	reasoning
 - page_section: where in the paper (printed page as in the PDF header/footer, plus theorem/eq/section label), e.g. "p. 957 (PDF p. 11), Cor 2". For SL15 give the journal page.
 - quote: the exact sentence or equation from the paper, max ~40 words (short excerpt only: public repo rule). Use "…" for cuts. For CAN'T CHECK write "-".
 - reasoning: ONE line.
 - No tabs/newlines inside fields.
2. OUT/notes.md: counts per verdict, list of PARTIAL / NOT SUPPORTED rows with a one-line suggested fix each (reword / re-cite / drop), and any problems with sources (wrong version, garbled pages, pagination mismatches).
Final message: verdict counts and the path of your files.

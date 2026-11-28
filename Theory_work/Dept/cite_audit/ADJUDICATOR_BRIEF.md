# CITE-AUDIT Step 4: adjudication brief

Two independent verifiers (A = Sonnet 5.5, B = Sol 6.2) disagreed on 33 citation claims. You decide each one by reading the cited passage yourself.

## Rules
- Root R = /home/fb31/BVS-wt/THEORY-DEPT. Write ONLY in OUT = R/.rc_tmp/cite_audit/adjudication/ (scratch in OUT/scratch/). No /tmp. Never delete or move files. No git state changes. No subagents. Do not edit project files.
- Decide from the paper text only (never memory, abstracts or citing papers). The verifiers' quotes are leads, not evidence: open the paper and confirm the passage yourself. Render page images (`pdftoppm -r 110 -f N -l N -png <pdf> OUT/scratch/<key>_pN`) when math in the .txt is garbled.
- Do not read R/.rc_tmp/song/, song_assumptions/PRECEDENTS_NEW.md, COUNCIL_RECORD.md, advisors/, council/ or writing_answers/ (earlier authors' views).

## Inputs
- R/.rc_tmp/cite_audit/disagreements.tsv: the 33 rows with our claim and both verdicts (verdict, page, quote, reasoning each).
- Full verifier notes if useful: R/.rc_tmp/cite_audit/v_sonnet/notes.md, R/.rc_tmp/cite_audit/v_sol/notes.md.
- Our documents (the audited text is the document line, not the extractor's paraphrase): TD/AP/OD = R/Theory_work/Dept/song_assumptions/{THEOREM_DEFINITIONS,ASSUMPTIONS_AND_PROOF_PATHS,OWNER_DEFENSIBILITY_DOSSIER}.md ; W3 = R/.rc_tmp/cite_audit/src/03_theory.tex.
- Papers: R/.rc_tmp/cite_audit/papers/, mapping and pagination notes in R/.rc_tmp/cite_audit/PAPERS_MANIFEST.tsv. Verdict definitions: R/.rc_tmp/cite_audit/VERIFIER_BRIEF.md.

## Standard
SUPPORTED only if a careful referee reading the paper would accept the sentence as written. PARTIAL if materially imprecise (location, conditions, scope, constants) but substantially right. NOT SUPPORTED if wrong, contrary, or wrong paper. Do not split the difference: pick the verdict the passage warrants, which may differ from both A and B.

## Output
1. OUT/adjudication.tsv, header exactly:
claim_id	final_verdict	page_section	quote	reasoning	fix
 - quote: the exact sentence/equation (≤ ~40 words; short excerpt only, public repo).
 - reasoning: one or two lines, saying which verifier was right and why.
 - fix: for PARTIAL / NOT SUPPORTED, a concrete fix to OUR text (reword / re-cite / drop, with the suggested wording); else "-".
 Write rows incrementally.
2. OUT/notes.md: counts of final verdicts, and how many times you sided with A, with B, or with neither.
Final message: the counts.

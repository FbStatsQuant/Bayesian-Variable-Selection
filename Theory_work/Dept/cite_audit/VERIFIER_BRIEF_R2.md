# CITE-AUDIT Step 3, round 2: the 8 rows that needed the owner-supplied papers

Follow R/.rc_tmp/cite_audit/VERIFIER_BRIEF.md in full (rules, forbidden paths, verdict definitions, output format), with these changes:
- Rows to verify: ONLY C124, C174, C239, C255, C352, C383, C408, C426 of R/.rc_tmp/cite_audit/claims.tsv.
- The two papers are now available (see PAPERS_MANIFEST.tsv): Chen & Chen (2008) = papers/CC08.pdf, Cramér (1936) = papers/Cramer36.pdf (German, poor OCR: read page images). For Cramér, quote the German original (short) and give your English gloss in the reasoning.
- For C124, C255, C383 (claims about what Luo & Chen / SBJ say about Chen & Chen, or that the primary text is unverified): check both the attribution in LC13/SBJ AND whether Chen & Chen's own text supports the attributed content; say so in one line.
- Also read R/.rc_tmp/cite_audit/src/03_theory.tex lines 205-212 and 335-342 for context.
- Do not read any other verifier folder (v_sonnet*, v_sol*) except your own OUT.
- Output: OUT/verdicts.tsv (same header) and a short OUT/notes.md. Final message: the 8 verdicts.

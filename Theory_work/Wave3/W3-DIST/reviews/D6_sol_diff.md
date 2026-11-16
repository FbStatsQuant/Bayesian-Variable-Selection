D6 diff check — lemmas/DIST12.md 111c31af7990b881; DEPS.tsv d79e1e997179b55b

Read reviews/BRIEF_D6_sol_diff.md in full first, then the exact patch, D5's review, the current proof and the six dependency rows. Searched all six proof scopes for `lem:`, `thm:` and "[P1]", and compared the cited/used items with the locked PROOF_v3.tex. This is an inventory of the proof files' imports/citations, including locally re-derived instances and commentary citations; it is not the recursive dependency closure of every locked theorem. API_CARDS common definitions are treated as the supplied setting, rather than expanding their entire context list into every row.

DIST12 check

The sentence now correctly says "gives no rate linear in A". It makes no identification of A with the actual exponent log p_raw/log n. The assumption p_raw <= n^A therefore suffices. The fixed-A rate and the explanation that C depends on A remain correct, taking D5's verification of the other mathematics as given.

A small inline Python computation, run under nice, found exactly one occurrence of the repaired clause. Reinserting only " = log p_raw/log n" recovers SHA-256 a786d3fc80069520adfd28a235d615ca431dee7444c650deeff959447e0b6071, whose prefix is precisely the D5 version a786d3fc80069520. Thus there is no other change in this file relative to the version D5 checked.

Finding D6-01 — MINOR.
Place: DEPS.tsv:8, row S, uses; work/C_size/S.md:60–62.
Error: S.md explicitly cites thm:T01ii at line 61, with its locked-proof line range 213–222, while explaining the deterministic inputs of thm:Ta. Row S omits it. All currently listed items are cited in S.md: thm:T01i (23, 61), thm:T01iii (103–104, 152), thm:Ta (60), lem:num (57), lem:den's proof (65, 77), lem:prior(c)'s proof (135–136), lem:spec(e) (138), and lem:slab (64).
Minimal repair: add thm:T01ii to row S. The fact that it is already an input to thm:Ta does not remove the explicit citation from S.md.

Finding D6-02 — MINOR.
Place: DEPS.tsv:11, row X'; lemmas/X.md:197–223, especially line 201.
Error: the row says X' uses the same locked items as X through sections 2 and 4–7. Section 9 expressly says "section 3 is not used". The explicit uses of lem:prior(b),(e) and lem:spec(d) belong to sections 1/3 (74, 115, 125, 128), which X' does not invoke. In particular, X' needs no superset comparison or combinatorial superset-prior bound. Section 4 re-derives the q_k recurrence within the cited proof of lem:prior(c); this does not require a separate import of lem:prior(b). Section 9 still uses lem:chi(a) through sections 2/6, lem:prior(c)'s proof through section 4, lem:spec(b) through the projection bounds in sections 5/6, lem:spec(e) through the determinant bounds in sections 4/5, lem:num, lem:den's proof and thm:Ta through section 4, lem:slab through its minimum/conditional formulas, and thm:T01i through the posterior formulas. No ND input remains.
Minimal repair: replace the "same ... as X" wording with the corrected X' list below; remove lem:prior(b),(e) and lem:spec(d).

Finding D6-03 — MINOR.
Place: DEPS.tsv:26, row NEC; lemmas/NEC.md:39–56.
Error: listing only the functions f,h and lem:spec(b) misses lem:spec(e)'s determinant product D_S = product_i f(lambda_i(G_S)), used at NEC.md:47 and 53 and in D_{ {0} } = n at 56. The definition of f alone does not state this determinant identity. The functions f,h and part (b) are indeed used, and lem:slab supplies both the minimum formula at 66 and the conditional normal law at 148.
Minimal repair: add lem:spec(e), retaining the functions f,h, part (b), and lem:slab.

Other rows

V: all listed items occur: lem:slab at V.md:50, lem:spec(a) at 54, lem:spec(e) at 93–94, and lem:prior(e) in the remark at 142–143. Their relevant identities are re-derived locally. No additional named P1 import was found.
X (sections 0–8): the row matches the full list in X.md:28,31. Parts prior(b),(e) and spec(d), which are unnecessary for X', are actually cited/used in the X proof at 74,115,125,128. The remaining items are used in sections 2,4–6. No missing item was found in this scope.
TC/DIST-3: DIST3.md:25–28 expressly identifies its only inherited posterior premise as thm:T01i. Its spectrum and fitted-mean calculations are proved locally at 61–68, and the tail tools are proved in section 2. H is separately recorded in the row. No additional P1 item is missing.

Limits: no requested local check was inaccessible or left unchecked. As directed, I relied on D5 for the unchanged mathematical verification of DIST-1/DIST-2. I did not independently re-prove all six supporting results, audit the locked proof's assurance status, or check unrelated DEPS rows/hash-maintenance changes. No git command, agent, cluster job or scratch file was used; the only write was this authorized review file.

D5-01 RESOLVED.
lemmas/DIST12.md (DIST-1, DIST-2): VERIFIED.
DEPS S: corrected list — locked T01 ([P1] thm:T01i, thm:T01ii, thm:T01iii, thm:Ta, lem:num, lem:den (proof re-derived), lem:prior(c) (proof), lem:spec(e), lem:slab).
DEPS V: CORRECT.
DEPS X: CORRECT.
DEPS X': corrected list — locked T01 ([P1] thm:T01i, thm:Ta, lem:chi(a), lem:prior(c) (proof), lem:num, lem:den (proof), lem:spec(b),(e), lem:slab), through sections 2 and 4–7; no ND.
DEPS NEC: corrected list — locked T01 ([P1] lem:spec (the functions f,h; (b),(e)), lem:slab (minimum representation and conditional normal law)).
DEPS TC/DIST-3: CORRECT.
Overall verdict: VERIFIED-WITH-AMENDMENTS — DIST12 verified; three MINOR dependency-inventory findings; no MAJOR or CRITICAL findings.

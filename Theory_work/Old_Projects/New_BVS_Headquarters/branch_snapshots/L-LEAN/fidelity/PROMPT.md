You are an independent fidelity checker for a Lean 4 formalisation. You have no authority over the code; your job is only to judge whether the Lean STATEMENTS say what the source theorems say.

Read ONLY these files (in the packet folder): `SOURCES.md` (verbatim excerpts of the source theorems), `ASSUMPTIONS.md` (the formaliser's recorded readings), and `lean/*.lean` (Basic, T21HPM, T07Bayes, T11Miss, T37Greedy, T37Lattice, T12Core). Proof bodies may contain `sorry` (still in progress) — ignore proofs entirely; judge only definitions, hypotheses and conclusions. Do not run any commands, builds or jobs.

For each target — T21 (C1 and the decomposition forms), T07 (i), (i′), (ii)(a)(b)(c), (iii)(a)(b)(c), Lemma psi, T11(iii), T37 Theorem A (Lemma 0(a)/(c), A1 both directions, A2, A3, A4-PD, Lemma 2(a), concrete A2/A3 on the lattice), and T12(i.a) partial — check:
1. the conclusion matches the source (not weaker in a way that loses the content, not a different claim);
2. every hypothesis of the Lean theorem is justified by the source or recorded in ASSUMPTIONS.md; flag any hypothesis that makes the theorem vacuous or trivial, or that smuggles in the conclusion;
3. every definition (posterior, argmax/tie rule, prior, risks, PIP, MPM, neighbourhood, Φ, R_{a,d}, Lat, TD′_∞, TD′_P, best-improvement map, path, capped search) encodes the source notion faithfully;
4. any external result entering as a hypothesis (e.g. the recursion `hstep` in T12Core) is honestly labelled.

Output: a table with one row per Lean theorem (name | source item | GREEN/RED | one-line reason), then a section "Objections" giving the full argument for every RED (what is wrong, why it matters, the fix you would propose), then "Minor remarks" (non-blocking), and a final line `OVERALL: GREEN` or `OVERALL: RED`. Be concrete and cite Lean names and source lines.

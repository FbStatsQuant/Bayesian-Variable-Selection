codex
The arguments establish (i)–(iv), including the nonreversible realised order, and the quantitative family asserted in (v). However, the final mixing-time consequence in STATEMENT.md is false as written.

1. **Location:** STATEMENT.md, claim (v), final sentence; PROOF_v1.tex, Section 6, closing paragraph (line 199).

   **Severity:** fatal (the literal concluding claim is false).

   **Claim:** The statement asserts that no upper bound on the absolute gap “(equivalently, no lower bound on its mixing time) that tends to 0” can follow from the listed conditions. The parenthetical does not give an equivalent assertion: a mixing-time lower bound tending to zero is compatible with uniformly fast mixing and is available here.

   **Evidence:** Define the usual worst-case mixing time
   \[
   t_{\mathrm{mix}}(1/4)
   =\min\left\{h\ge0:
   \sup_x\|K_\phi^h(x,\cdot)-q_\phi\|_{\mathrm{TV}}\le1/4
   \right\}.
   \]
   Every permitted state space contains at least \(\emptyset\) and \(\{1\}\). Therefore
   \[
   \sup_x\|\delta_x-q_\phi\|_{\mathrm{TV}}
   =1-\min_xq_\phi(x)\ge\tfrac12,
   \]
   so \(t_{\mathrm{mix}}(1/4)\ge1\). In particular,
   \[
   t_{\mathrm{mix}}(1/4)\ge\frac1n,
   \]
   a valid lower bound tending to zero, including on the constructed family satisfying all three conditions.

   The quoted original wording concerns an **exponentially large** mixing-time lower bound. The explicit family faithfully demonstrates that such a conclusion need not follow: its geometric TV bound gives a mixing time bounded independently of \(n\). The final parenthetical, read literally, does not faithfully express that conclusion. This finding concerns the concluding statement, not the validity of the constructed family.

2. **Location:** PROOF_v1.tex, Section 3, “Neighbour swap,” proposal-probability display (lines 96–101).

   **Severity:** exposition.

   **Claim:** The displayed formula for the reverse proposal probability can be undefined in the arbitrary-neighbour-family case covered by (ii).

   **Evidence:** Take \(p=2\), \(N(1)=\{2\}\), \(N(2)=\emptyset\), \(S=\{1\}\), and \(S'=\{2\}\). The forward proposal has probability one, and the actual reverse proposal has probability zero. Nevertheless, the displayed expression is
   \[
   \mathcal Q(S',S)
   =\frac{\mathbf1\{1\in N(2)\}}
   {|S'|\,|N(2)\setminus S'|}
   =\frac00.
   \]
   The subsequent case analysis correctly treats the absent reverse proposal as having probability zero, so the detailed-balance argument is valid. The defect is confined to the unconditional fractional notation.

The remaining proof steps check out. In particular, the backward-sampling probabilities telescope correctly; the elementary kernels handle the stated boundaries; reversal of products establishes self-adjointness of the averaged round; and the independence-step minorisation survives composition with invariant kernels. The family’s score bounds establish the switch, exponentially small \(\varepsilon_1\), and linear discrepancy range. The six orders ending with Gibbs 1 followed by Gibbs 2 yield the claimed \(1/40\) minorisation and both mixing bounds.

The reading of “an individual realised order need not be reversible” is faithful and is established by the supplied example. The quantitative existence assertion in (v) is a stronger sufficient witness for the original warning and is also established. The obstacle to verification of **every claim as written** is finding 1.

**Verdict: not verified.**
tokens used
44,854
The arguments establish (i)–(iv), including the nonreversible realised order, and the quantitative family asserted in (v). However, the final mixing-time consequence in STATEMENT.md is false as written.

1. **Location:** STATEMENT.md, claim (v), final sentence; PROOF_v1.tex, Section 6, closing paragraph (line 199).

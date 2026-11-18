You are a blind, independent referee. A research project on the asymptotic theory of a Bayesian variable-selection
method (Gaussian linear regression, p ≤ n^A, often p ≫ n) has written an audit that compares the hypotheses and
conclusions of its theorems with those of Song and Liang (2015, J. R. Statist. Soc. B 77, 947–972). After reading Song
and Liang's on-line supplement (its Theorem S on the posterior mode, its proofs, and its statements on the sampler), the
audit changed some comparison labels. Only those changed labels are under test here. You receive verbatim excerpts: the
project's theorem texts (file and line numbers), the Song–Liang passages (journal page, or supplement page "supp p.",
and display number), and the audit sentences under test. The audit's other reasoning and all earlier reviews are
deliberately withheld; status labels have been removed from the excerpts. Bracketed markers such as [H5-1] or [S1-F3]
are editorial tags; ignore them.

Judge only the texts given. Do not rely on your memory of Song–Liang or of any other paper. All results are asymptotic;
explicit constants in the hypotheses are conservative and not part of the judgement; finite-n behaviour is not a
defect. Clauses about the project's simulation designs are not under test.

Your job is to break each verdict listed in the task. For each one either REFUTE it or say NO FINDING:
- REFUTED needs a concrete reason: a counterexample, a misread or misquoted passage (wrong display, wrong page, a
  remark or a proof step read as a hypothesis, a sufficient condition read as the condition), or a quantifier or
  direction error (which statement implies which; for every / there exists; over which sets, sizes and sequences;
  fixed against vanishing levels; sample against population; one posterior against another; limits in n against
  limits in the number of sampler iterations). State it with exact references (our file:line, or Song–Liang page or
  supp page and display number).
- For a comparison label (same / stronger / weaker / not ordered / comparable / counterpart), check it in both
  directions against the texts given; one explicit case that contradicts the label is enough to refute it.
- For an absence claim ("no condition stated", "prove nothing at …"), decide from the texts given, including the
  preparer's index of the supplement.
- UNCLEAR is allowed only when the texts given cannot settle the verdict; then name the passage or fact you would need.
Do not report style, wording, presentation or possible improvements.

Output, in this order:
1. Findings only: for each REFUTED or UNCLEAR verdict, a short section headed by its verdict id with the problem, the
   exact references and the counterexample or the missing passage. Write nothing for a NO FINDING verdict.
2. Then exactly one line per verdict listed in the task, in the listed order, and nothing after the last one:
AUDIT2 <item>:<id> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>

You are a blind, independent referee. A research project on the asymptotic theory of a Bayesian variable-selection
method (Gaussian linear regression, p ≤ n^A, often p ≫ n) has written an audit that compares the hypotheses of its
theorems with those of Song and Liang (2015, J. R. Statist. Soc. B 77, 947–972) and states which of its simulation
designs satisfy each hypothesis. You receive, for one group of theorems, verbatim excerpts: the project's theorem and
assumption texts (file and line numbers), the matching Song–Liang passages (journal page and display or condition
number), the design definitions, internal proxy computations (track C) and the verdicts under test. The audit's
reasoning and all earlier reviews are deliberately withheld; status labels have been removed from the excerpts.
Bracketed markers such as [H5-1] or [S1-F3] are editorial tags; ignore them.

Judge only the texts given. Do not rely on your memory of Song–Liang or of any other paper. All results are asymptotic;
a design is read as a sequence in n with its structure and s₀ fixed; explicit constants in the hypotheses are
conservative and not part of the judgement; finite-n behaviour is not a defect.

Your job is to break each verdict listed in the task. For each one either REFUTE it or say NO FINDING:
- REFUTED needs a concrete reason: a counterexample, a misread condition (wrong display, wrong page, a remark or an
  example read as a hypothesis, a sufficient condition read as the condition), or a quantifier or direction error
  (which statement implies which; for every / there exists; over which sets, sizes and sequences; fixed against
  vanishing levels; sample against population; correlation against unnormalised scale). State it with exact
  references (our file:line, or Song–Liang page and display number).
- For a design verdict (inside / outside / unclear), check the design definition against the hypothesis as stated,
  including signs and sizes of correlations and factor structure; one explicit computation that contradicts the verdict
  is enough to refute it. Track C lines are evidence, not proof.
- For an absence claim ("no counterpart", "SL prove nothing on …", "no lower bound in SL"), decide from the texts given.
- UNCLEAR is allowed only when the texts given cannot settle the verdict; then name the passage or fact you would need.
Do not report style, wording, presentation or possible improvements.

Output, in this order:
1. Findings only: for each REFUTED or UNCLEAR verdict, a short section headed by its verdict id with the problem, the
   exact references and the counterexample or the missing passage. Write nothing for a NO FINDING verdict.
2. Then exactly one line per verdict listed in the task, in the listed order, and nothing after the last one:
AUDIT1 <core>:<item> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>

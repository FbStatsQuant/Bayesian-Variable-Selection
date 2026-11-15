# R2 reconciliation — sol

Reconciled all round-R1 findings against HEAD `f16f1b3a490d76ef14fc6411a855c8d07228d60e`, using `1f205b2` as the diff base. This is a reconciliation review, not a scoring seat. Read both R1 reviews, their disposition, and the current ticket files, excluding LOG, CHECKPOINT files and other review material. No subagents or commits. All paths below are relative to `Theory_work/Wave3/W3-PSHARP/`.

The required command

```
py -3.13 -I Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-PSHARP Theory_work/Wave3/W3-PSHARP/reviews/MANIFEST_R2.txt
```

printed `verify: OK MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14`.

## Finding-by-finding reconciliation

| Finding | Verdict | Place of fix (current file:line) | Correctness of fix |
|---|---|---|---|
| sol M1 (MAJOR): missing Claim B hypotheses | RESOLVED | REPORT.md:40–53, REPORT.md:113, REPORT.md:156 | The general inequality retains `0 ≤ s₀ ≤ K−1`. The consistency and rate consequences now explicitly require `s₀ ≤ min(K−1,p/2)`; the critical cap additionally requires `s₀/p → 0`. The rate is the exact `c(p,s₀)/√n`; the half-constant is expressly asymptotic. These agree with STATEMENT.md:92–110 and the Consequences section of lemmas/B_sparsity.md. Both newly quoted examples are correct; see below. |
| sol m1 (MINOR): omitted orthogonal size truncation | RESOLVED | REPORT.md:86–91 | Reports sums over sizes at most `min(K,s₀+60)` and `s₀+80` in E2. Calls them lower bounds before quadrature error, states that quadrature is not a certified enclosure, and identifies the reported ratios as restricted odds. This matches numerics/a_orth.py:37–47 and its E1/E2 calls. |
| sol m2 (MINOR): unqualified counterexample numerical summary | RESOLVED | REPORT.md:103–105 | Now specifies b=3, medians, and rounding; gives the b=1 and b=0.5 medians separately. The output has 0.9968 at n=50,b=3, 0.9489 at n=400,b=1 and 0.4656 at n=1600,b=0.5. The largest recorded control tail is 3.149e−13. All qualifications are correct. |
| opus MINOR-1: inflated NECESSARY label | RESOLVED | REPORT.md:60–61, REPORT.md:115, REPORT.md:168; STATEMENT.md:141–144 | FAILED-REMOVAL accurately describes Proposition C: removing coefficient control while retaining exact representation and energy control fails for the specified reference. The text expressly allows weakening the particular coefficient bound to bounded ridge cost. It no longer asserts that this particular norm hypothesis is necessary. |
| opus MINOR-2: counterexample b qualifier | RESOLVED | REPORT.md:103–105 | Same correction as sol m2; also states that these finite mechanism checks fall far below the theorem's signal constant. Checked against the displayed rows and script configurations. |
| opus NIT-1: unproved existence remark at small log p | RESOLVED | STATEMENT.md:109 | Removes the assertion that the rate can survive; now says that this obstruction does not apply and makes no claim there. In context this refers to the preceding growing-support obstruction at `log p ≍ log n`, not to a new upper bound. |
| opus NIT-2: garbled energy/coefficient weakening sentence | RESOLVED | ASSUMPTION_MAP.md:12 | Replaced by the requested `(M+M′) log N_n = o(n)` condition for both witnesses. Correct with the other witness conditions retained and fixed positive noise variance: the energy/coefficient contribution to the exponent error is of this order in both proofs. Still marked unharvested, not added to Proposition A. |
| opus NIT-3: numerical header overclaims testing the equality iff | RESOLVED | numerics/b_check.py:4, numerics/b_check.py:51; numerics/b_check_out.txt:1 | Docstring now disclaims testing the equality case in F1; printed header claims only Schur formulas and the determinant inequality. The F2 explicit equality examples remain correctly separate. Full rerun matches the frozen output. |
| opus NIT-4: two notation clashes | RESOLVED | lemmas/A_log_factor.md:65–68; lemmas/C_counterexample.md:72–73 | All local uses of the error envelope become `e_n(x)`; the projected chi-square variable and its event become `E_𝒳`. The inequalities, distributions and probability bounds are unchanged and consistent. |
| opus NIT-5: half-constant needs sparse asymptotics | RESOLVED | REPORT.md:156; ASSUMPTION_MAP.md:21 | Both now give `c(p,s₀)/√n`, with the asymptotic half-constant requiring `p → ∞, s₀/p → 0`. This follows directly from `c/(s₀+1)=(1−s₀/p)/(2−(1+s₀)/p)`. The arrow in the map is shorthand for this asymptotic equivalence. |
| opus NIT-6: admissibility versus n₀ | RESOLVED | STATEMENT.md:122–124 | Dividing the existing signal condition by `b̄²`, using `b_n² ≤ b̄²`, gives exactly the added necessary inequality `n ≥ C_b(1+σ*²/b̄²)(log n)²`. This is a consequence of the existing premises, not a new premise. |

## Independent check of the two examples

For orthogonal standardized columns choose `y=Σ_{j∈S₀}x_j/√s₀`. For t included signal columns and u included nulls,

```
D_S = n^(t+u),
Q_S = (n−1)/n + [(n−1)^2/n](s₀−t)/s₀.
```

These follow directly from the diagonal Gram matrix. Models containing every signal have fit ratio one. The total odds of missing-signal models vanish when `s₀ ~ λ√n` in either example: a missing signal increases Q by order `n/s₀`, giving a fit penalty `exp(−Ω(n log n))`, whereas a uniform bound on their combinatorial, prior and determinant factors is `exp(O(s₀ log n))`.

For `p=s₀+1` there is exactly one strict superset, with prior ratio one and odds `n^(−1/2)`. Thus `c=1` and `π(S₀)→1` is possible at `s₀~√n`. Fresh grouped enumeration gives 0.9900990099 at `(n,s₀)=(10000,99)` and 0.9990009990 at `(1000000,999)`.

For `p=2s₀`, the j-th superset group tends to `(λ/3)^j/j!`: each product factor tends to 1/3. To justify summing, all product factors are at most `r_s=s₀/(3s₀−1)`. Hence the entire superset sum including j=0 is bounded above by the negative-binomial series `(1−r_s/√n)^(−s₀−1)→exp(λ/3)`. Fixed partial sums give the matching lower limit. Therefore `π(S₀)→exp(−λ/3)` on this example. For λ=1, fresh values are 0.7132154480 at n=10000 and 0.7161995961 at n=1000000, approaching 0.7165313106. The REPORT's example is correct as an attainable weaker cap; it is not a universal equality on all designs.

## Exact diff assessment

Ran the exact requested diff, with reviews and LOG excluded. Seven files changed; no CHECKPOINT change appeared, and no other eligible file changed.

- ASSUMPTION_MAP: NIT-2 and NIT-5, plus the statement-version reference.
- REPORT: M1, m1, m2/MINOR-2, MINOR-1 and NIT-5; version references and the Claim C registry range updated to account for inserted explanatory lines.
- STATEMENT: NIT-1, MINOR-1 and NIT-6, plus version-history wording. The numbered statement items, premises, constants and conclusions are unchanged. B3 loses an unsupported existence aside; the new Claim C admissibility sentence is derived from its existing premise.
- A_log_factor and C_counterexample: exactly the two NIT-4 symbol renames, with no changed proof step.
- b_check.py and b_check_out.txt: exactly the NIT-3 docstring/printed-header changes. No computational path changes.

Not literally traceable to an individual R1 finding: REPORT.md:74 generalizes the council review-trail row from R1 to `R<k>` and adds the frozen-file explanation; REPORT.md:140,150,160,169 move the four pending correctness-gate brief references from R1 to R2. These are round-transition bookkeeping. Thus **not every changed line is an individual finding fix**, but these additional edits are editorial, remain pending, and neither assert a passing score nor alter mathematics. Version/reference maintenance is consequential housekeeping for the listed fixes.

The report/registry scope corrections change the accuracy of the summaries, as requested by M1; they do not change the locked mathematical result. No substantive change in the brief's sense (statement item, proof step, premise, constant, or numerical computation) was found.

## Numerical consistency and regressions

Re-ran the final `b_check.py` in full, storing output only under `reviews/R2_scratch_reconciliation/`. All output lines match `numerics/b_check_out.txt` after normalizing text encoding/newlines. F1 passes for 8,064 pairs; F2 passes for 55,740 cases, with minimum odds/O_lb 1.033240 and minimum odds/(c/√n) 1.040592. Against `1f205b2`, every output line after the first is unchanged. A syntax-tree comparison after applying only the two documented text replacements confirms that b_check.py has no other change.

Scratch evidence: `R2_scratch_reconciliation/checks.py`, `checks_out.txt`, and `b_check_rerun.txt` (all under reviews). The independent grouped checks reproduce both examples. Unchanged Monte Carlo suites were read, not rerun. No regression introduced by these fixes was found. The unchanged shorthand critical-scale remark in ASSUMPTION_MAP.md:26 must be read under STATEMENT §3's hypotheses; it is not a new unrestricted result or a regression from this diff.

Counts: **11/11 R1 finding entries RESOLVED; 0 PARTLY; 0 NOT-RESOLVED** (1 MAJOR, 4 MINOR, 6 NIT entries; sol m2 and opus MINOR-2 overlap, so 10 distinct issues). **0 substantive diff changes; 0 new regressions; 2 kinds of additional editorial bookkeeping** as listed above.

RECONCILIATION: ALL-RESOLVED

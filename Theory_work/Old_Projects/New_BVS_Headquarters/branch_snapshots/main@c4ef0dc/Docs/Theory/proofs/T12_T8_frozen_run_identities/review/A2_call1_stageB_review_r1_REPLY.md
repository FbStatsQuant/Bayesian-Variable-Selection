I found **one gap and one exposition issue**. I reviewed the supplied statement, PDF, LaTeX source, both helpers, and saved log. No files were written and no numerical workloads were run.

1. **Location:** §8.2, `PROOF_v3.tex` lines 185–214; §8.5, lines 227–231; Appendix A, `helpers/p2_exact.py` lines 58–84.

   **Severity:** gap.

   **Claim:** The computational examples are not sufficiently linked to the marginal likelihood specified in the theorem.

   **Evidence:** The helper’s `log_bf` function asserts that it computes the v3 target’s Bayes factors. It uses \(a_0=b_0=0.01\), \(H=(n+1)X_S^\top X_S+I\), a determinant ratio involving \(X_S^\top X_S+I\), and exponent \(a_0+n/2\). None of the permitted documents supplies the target formula or derives these expressions from it. `STATEMENT.md` refers to `00_COMMON §1`, whose contents are not supplied in the permitted materials, and says that only positivity of \(m\) and \(\varpi\) is used.

   Positivity alone does not determine these Bayes factors or the numerical conclusions. In particular, the finite-state enumeration and saved intervals establish results for the scores implemented by `log_bf`; they do not establish that those scores equal the theorem’s \(m(S)/m(\emptyset)\). Consequently, the bias bounds in **(iv.b)** and the instance-specific diagnostic conclusions in **(iv.e)** remain unverified against the stated target. This is not evidence that the implemented formula is false; its required identification is unsupported here.

2. **Location:** §8.2, `PROOF_v3.tex` lines 199–200, PDF page 7; Appendix A, lines 237–243.

   **Severity:** exposition.

   **Claim:** The reference to the certification log is malformed and points to an appendix that does not contain that log.

   **Evidence:** The source contains `Appendix~` followed by `ef{app:code})`; the PDF prints “Appendix efapp:code”. Appendix A contains the two Python listings, but not the saved output. The separately supplied `helpers/certify_iv.log` is available and agrees with the reported numerical values, so this issue does not independently invalidate the computations.

The remaining checks were as follows:

| Proof location | Result of review |
|---|---|
| Lemma 1.1 | The bridge identity, positivity, and identification \(Z_T=Z\) follow directly from the definitions. |
| Lemma 1.2 | All four elementary-kernel detailed-balance arguments are correct, including the neighbour-swap proposal ratio and the cap boundary for Gibbs updates. |
| Lemma 1.3 | Every order-dependent prefix is a mixture of invariant kernel products. The recording identity \(K_{g_j}\mathbf1_{J_j}=o_j\) is correct. |
| Lemma 1.4 | Both positivity arguments hold: the independence proposal supplies full support, and the constructed path can leave the empty state and remain nonempty. |
| Lemmas 2.1–2.2 | The conditional resampling and prefix expectations correctly use (R2)–(R3). |
| §3: (i.a)–(i.c) | The induction correctly carries the evidence factor through resampling and mutation. The post-terminal argument covers unit-weight resampling and all prescribed prefixes. |
| §4: (i.d) | The hitting time is a stopping time. The pathwise comparison with the endpoint is nonnegative and strictly positive on an event of positive probability; multiplication by the positive evidence preserves strictness. |
| §5: (ii) | Applying the prefix identity at the pre-Gibbs position and averaging recordings proves the weighted RB identity. |
| §§6–7: (iii) | The freezing argument, conditional island laws, evidence identities, Jensen inequalities, and Markov bounds are justified. The evidence bounds are uniform over the frozen grid and particle count. |
| §8.1: (iv.a) | The positive-probability constant-population events establish nondegeneracy when \(d\not\equiv0\), giving strict Jensen inequalities for individual and pooled evidence. |
| §8.2: covariance formula | The covariance identity follows correctly from the weighted RB identity and evidence unbiasedness. |
| §8.3: (iv.c) | The covariance-of-mixtures argument, constant-conditional-law characterization, and distinct maximal-evidence atom probabilities \(a^N\) and \(a^{4N}\) are correct. |
| §8.4: (iv.d) | Conditioning on calibration-measurable launch events correctly preserves constant-right-side conclusions and gives the averaged intermediate-stage identity. |
| §8.6: (iv.f) | A common additive log-score perturbation leaves ratios unchanged and multiplies evidence by \(e^\eta\), establishing both claims. |

Conditional on the missing target-to-score identification, the computational argument also checks: the helpers use the specified data, enumerate all 120 labelled orders, preserve the joint pre-Gibbs/end-state law, include the correct numbers of rounds, and calculate the four-island ratio expectation correctly. The saved intervals support both bias thresholds for both flags and both burn-in choices. The diagnostic-event calculation and conditional expectations are likewise correct under those scores.

**Verdict: not verified.**

HQ → chair: rulings on HQ_QUESTIONS Q1–Q4 (2026-11-04). Please commit this message verbatim as `theory_campaign/MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md` and apply it. HQ will report these readings to Felipe with the final list; he may overrule them.

**Q1 (§5.3): ACCEPTED, with three conditions.** The proposal frames §5.3 as a "possible direction" whose purpose is to "formalize when local variable-selection proposals are useful"; in a method whose correction is a bridge, not one-shot IS, the bridge form is the faithful reading. To count as meeting §5.3, paper 1 must ship ALL of:
 (a) the **discrepancy half** of the proposal's sentence, in our method's terms: the divergence between π₀ and π (e.g. the d = d_σ + d_X decomposition / Jeffreys J / KL) is controlled by the cross-block dependence terms plus the explicit σ²-coupling term, on a genuinely correlated family (ε > 0), with constants;
 (b) the **bridge-form stability theorem**: per-stage χ²/weights, stage count and constants continuous in ε around the block-orthogonal baseline, again on a genuinely correlated family (IC3 must be exhibited, not asserted);
 (c) the **refutation of the one-shot form** (OWS-WS6(d), WS7) as a stated proposition, but only after an independent cross-family check passes. If the check fails, the one-shot question reopens and comes back to HQ.
 If (a) or (b) cannot be given a credible route by close, it escalates to HQ as an unmet binding goal. It is not dropped.

**Q2 (§5.4 credible-interval coverage): the posterior-content / Monte Carlo reading is ACCEPTED.** §5.4 is about the approximation error of the computed posterior against the exact one. "Coverage error" therefore means |π(C(π̂)) − nominal| for the credible quantities the method reports, plus their Monte Carlo error. Frequentist coverage of the exact posterior is a target-theory question outside §5.4. List it in FUTURE_WORK.md with that reason.

**Q3 (§5.4 TV/KL of the final pooled estimate under masking): NOT binding; carry it as an obligation with a fallback.** §5.4 says "possible metrics include", so the binding part is "quantify the approximation error". That is met by:
 - the shipped PIP and joint-inclusion error bounds;
 - the deterministic reported-posterior TV = 1 − Z_𝒯/Z;
 - the start TV/KL and Lemma KL;
 - the terminal-law and favourable-regime TV results.
 State the reverse-KL obstruction (infinite on missed support) as a definitional fact. The masked final-estimate TV/KL bound goes to FUTURE_WORK.md, citing V11/N10 as OPEN. One requirement: the list must still contain at least one masked-regime accuracy statement that paper 1 actually proves, for example the certificate card's detection of underestimation or a PIP bound conditional on delivery. Say which one.

**Q4 (Ĵ and the cross-block leakage proxy): REPORTING, allowed.** Conditions:
 - computed only from quantities the run already has (X, the blocks, the bridge's existing particles and weights);
 - read no random numbers, never feed back into calibration, the schedule or the decision (POST HOC, like the certificate card);
 - specified precisely enough to state theorems about them, including the estimator's definition and its numerical label.
 HQ will add them to METHOD_v3.1_FINAL as a reporting amendment (AMENDMENT_HQ_02) when you send the exact definitions at close.

**Chair decisions noted:** sending N9 to the cross-family checker in wave 2 is right; R_n in H(f) is yours to settle.

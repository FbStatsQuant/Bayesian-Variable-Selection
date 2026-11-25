# check_A: statement check of sam_style/smc_bvs_theory_sam_style.tex against the specification

Document: `Docs/Writing/manuscript/sam_style/smc_bvs_theory_sam_style.tex` (SAM). Source: `spec/spec.tex` with `sections/sp2_model.tex`, `sp3_distributions.tex`, `sp4_sampler.tex`, `sp4_algorithms.tex` (for the searches), `sp5_assumptions.tex`, `sp6_theorems.tex`, `sp7_supplementary.tex` (examples only). P5 from `Theory_work/Dept/assess/MIS_KL/ASSESS_fable.md` section 2, Target A. Numbering: A1 GL, A2 DIM, A3 SP, A4(a) SGR, A4(b) GR, A5(a) FSb, A5(b) FSt, A6 EFS, A7 dist, A8 V, A9 reported, A10 SCR; Theorems 1-6 = post-random, dist, reported, screen, Prop 5 (unbiased), sharp (this is also the order in sp6).

Not checked (outside the spec): the literature claims about Song and Liang, Yang-Wainwright-Jordan, Zhou et al., Zanella-Roberts (Theory's CITE_CHECK covers them), and the proof sketches in the prose after Theorem 3.

## Counts

Statements (assumptions, conventions, theorem-type results, planned results): MATCH 19, SIMPLIFIED-TAGGED-OK 4, DIFF 2 (both planned, minor).
Model/prior/outputs rows: 2 DIFF (minor, prose). Commentary: 2 DIFF.
Total DIFF: 6. No DIFF makes a theorem, proposition or assumption false. One (D3) is stronger than proved in a corner case of commentary.

## Table

| Item (doc) | Source | Class | Note |
|---|---|---|---|
| A1 Gaussian linear model | GL | MATCH | "independent of the predictors" = "of the design" |
| A2 Dimension | DIM | MATCH | |
| A3 Sparsity | SP | MATCH | |
| A4(a) sub-Gaussian on sparse directions | SGR | MATCH | count 5(A+1)(s0+1) log n, L>0, same inequality |
| A4(b) Gaussian rows | GR | MATCH | "case (a) with L=1" as in SGR |
| A5(a) raw scale | FSb | MATCH | |
| A5(b) standardised scale | FSt | MATCH | |
| A6 eigenvalue floor | EFS | MATCH | |
| A7 density setting | dist (a)-(e) | MATCH | C_q, q_n, c_psi/n floor, bounded signal all agree |
| A8 visibility | V | MATCH | |
| A9 leakage set (a)(i)-(iii), (b), (c) | reported | MATCH | (iii) is the spec's side conditions on Q, K |
| A10 certified screening | SCR | MATCH | c = c_SB, same constants |
| C1 | C1 | SIMPLIFIED-TAGGED-OK | "admissible" and "every valid seed" folded in; doc says the spec lists conventions item by item |
| C2 | C2 and C2p | SIMPLIFIED-TAGGED-OK | doc's C2 is the spec's C2p (the two integer limits ignored); spec C2 alone would not give "every n>=3". Footnote after Thm 3 says so |
| C3 | C3 | SIMPLIFIED-TAGGED-OK | items (v) measurability, (vi) potential run and the random order of moves omitted; (vi) is covered in the text before Prop 5 |
| Theorem 1 posterior concentration | Thm 1 | MATCH | hypotheses, rates, dropped-column conventions identical |
| Theorem 2 fitted density | Thm 2 | MATCH | constants, n >= n0, sqrt(n)/log n >= M, "read as 1" clause |
| Theorem 3 reported model | Thm 3 | SIMPLIFIED-TAGGED-OK | title tags it; hypotheses A2, A4(b), A5(b), A6, A8, A9, C1 = DIM, GR, FSt, EFS, V, reported, C1; G_n clause and the delivery clause agree with spec under C2p |
| Theorem 4 certified screening | Thm 4 | MATCH | |
| Proposition 5 evidence unbiased | Prop 5 | MATCH | statement identical; see D2 for the definition of Z |
| Theorem 6(a) | sharp (a) | MATCH | same bound and range of S; see D3 for commentary |
| Theorem 6(b) | sharp (b) with WIT | MATCH | WIT inlined (s0 fixed, M_mu, M_theta, N-orth or N-gauss, "conditionally" clause), both displays identical |
| Table 1 (what each result assumes) | spec Table usage | MATCH | |
| P1 trap | planthm trap | DIFF (minor) | D4 |
| P2 p = 10^7 | planthm cov7 | MATCH | A = log(10^7)/log 200 = 3.04; omits "known true model", harmless |
| P3 raw-scale bridge | planthm bridge | DIFF (minor) | D5 |
| P4 aggregated leak | planthm agg-leak | MATCH | |
| P5 wrong model, p fixed | ASSESS Target A | MATCH | rows iid from a fixed law, E[|x|^2 r^2] and E r^4 finite, three consequences, KL and Hellinger display, "KL projection whenever finite", all as in Target A. The paragraph on Song and Liang Theorem 4 and Corollary 2 agrees with ASSESS section 1 |
| Model (1), standardisation, theta*, model space Omega, K | sp2, sp1 | MATCH | |
| Priors (model, g-prior with unit ridge, IG(0.01,0.01)) | sp3 | MATCH | pi(S) proportional to binom(2p-1,|S|)^{-1} equals w(|S|)/w_K; BB(1,p) |
| m(S) formula | def:marglik | MATCH | up to the constant C_n, see D2 |
| Posterior, Z, PIP, HPM, MPM | def:posterior, summaries | DIFF (minor) | D2 |
| Sampler steps 1-5 | sp4 | MATCH except the search start | B, h_k, pi_0, Delta, path, weights, moves, caps l_n and l_n+|S0~| agree; see D6 |
| What a run reports (i)-(iv), exact case, "produces output" | def:shat, pipr, zhat, list, outcomes | DIFF (minor) | D6 |
| Zhat formula | def:zhat | MATCH | |

## Details of each DIFF

**D1 (not a DIFF, remark).** Commentary on A10 says "the true model size s0 need not be fixed". True as written (A3 is not assumed), but A10 forces s0 <= M_1/theta_low, so s0 is bounded. No action needed.

**D2. Section 2.4 (Z, m(S), pi(S) defined with proportionality).** The document writes pi(S) proportional to ..., m(S) proportional to ..., and Z = sum of pi(S) m(S). The spec has pi(S) = w(|S|)/w_K (normalised) and m(S) with the constant C_n, so Z = sum of exp F(S). Proposition 5 and Zhat = m(empty) Z0bar prod(...) are unbiased for that Z only. As written, Z is determined only up to the dropped constants. The statement is not false if pi and m are read as the exact normalised versions. Fix: write "pi(S) = w(|S|)/w_K" and "m(S) = C_n (...)" or say "with all constants kept in m and pi".

**D3. Commentary on Theorem 6(a): the proviso s0 <= min(K-1, p/2) is dropped.** In the A3 paragraph ("the rate sqrt(log n/n) is possible only if s0 = O(sqrt(log n))") and in the paragraph after Theorem 6 ("no design gives a rate faster than n^{-1/2}" and "possible only when s0 = O(sqrt(log n))"). Spec (Theorem 6(a) text) states both consequences "for true models with s0 <= min(K-1, p/2)". With A2 and A3 only (p >= 2, s0 fixed), a design with p < 2 s0 (for example p = s0) is not covered, so the commentary is stronger than proved in that corner. The displayed inequality in (a) is correct. Fix: add "for s0 <= min(K-1, p/2)".

**D4. P1, trap statement.** Spec says "with probability tending to one, t_mix(P) >= tau_n for every single-flip chain P ... where tau_n tends to infinity", and defines mixing time (TV <= 1/4) and single-flip chain. The document says "has a mixing time that grows quickly", without "with probability tending to one" and without tau_n -> infinity. Open items agree (family, which of Theorems 1, 3, 4, class of chains, growth rate). Planned result, so nothing false; add "with probability tending to one".

**D5. P3, raw-scale bridge.** Spec: A7 with s >= 1 and a level M >= M_0, then data events of probability tending to one on which every admissible completed run, whatever its seed and calibration outcome, returns a list with pi(T | D_n) >= n^{-c_H M/2}. The document omits "M >= M_0" (c_H exists only for M >= M_0) and "whatever its seed and calibration outcome" (spec's version of "every completed run"). Planned result; minor.

**D6. Sampler and "what a run reports" (prose, minor).**
(a) "A run reports four things": the spec's completed run also reports log Zhat lower bound, list-renormalised inclusion probabilities, median model and log Z_T, and flags. The four listed are described correctly; the count is not exhaustive.
(b) Step 5: "one from the best model the particles found". Spec (Algorithm TwoSearches, LS_1): from the model with the best F scored so far, in the block tables, the calibration, the islands and earlier scans. Not only the particles.
(c) Reported model: "ties going to the smaller model"; spec adds "then to the lexicographically smaller one".
(d) Certified: "local optimum under additions, deletions and swaps"; additions are allowed only while the size is below K (def:localsearch).
(e) PIPhat_j: spec averages the Gibbs probability o_j over particles and the four measured rounds (at xi = 1), then over the 4 islands; the document omits the rounds.
(f) List: "the 40p+1 best models"; spec says "at most 40p+1".
None of these affects a theorem (Theorems 3, 4 and Prop 5 do not use (e), (f)); (b) and (d) are the only ones a careful reader could object to. D6 is the only group not covered by a "simplified" tag.

**D7 (commentary on A8, counted as the 2nd commentary DIFF).** "A8 holds ... for autoregressive correlation with true effects of one sign." Spec (Corollary on block and autoregressive designs, Lemma on visibility, item 5): for rho > 0 one sign suffices; for rho < 0 the signs must alternate, sgn(theta_k) = varsigma (-1)^k, or other conditions (ARsep, ARg) hold. For rho < 0 and one sign, A8 can fail: theta_{j+1} = -theta_j/rho gives Cov(W_j, W'theta) = 0 with U empty. Fix: "autoregressive correlation rho >= 0 with true effects of one sign (alternating signs if rho < 0)". Not a statement of a theorem.

Counting note: the "6 DIFF" in the counts above are D2, D3, D4, D5, D6, D7 (D1 is only a remark).

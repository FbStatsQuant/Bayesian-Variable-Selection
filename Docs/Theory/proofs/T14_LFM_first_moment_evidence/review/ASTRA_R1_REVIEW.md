# Astra review, round 1 (session <uuid>, gpt-6-astra, reasoning high), 2026-10-22

Packet: STATEMENT.md, PROOF.tex (= proof/PROOF_v1.tex), REPORT_FORMAT.md. Full log: astra_r1_full_log.txt.

The proof establishes (i-a)–(i-d) under the stated hypotheses. I found no fatal error or substantive gap. There is one notational exposition issue.

**Finding 1**

- **Location:** STATEMENT.md §1; PROOF.tex §1 (“Bridge” and “Grid”) and §4, proof of (i-a).
- **Severity:** exposition.
- **Claim:** The notation \(q_1,\bar Z_1\) is used both for temperature \(1\) and for stage \(1\). These meanings generally differ when \(T>1\). In particular, the assertion “\(q_T=q_1\)” requires the temperature interpretation of the right-hand side.
- **Evidence:** The grid definition gives \(q_t=q_{\varphi_t}\). For \(T>1\), stage \(1\) has \(\varphi_1<1\), whereas stage \(T\) has \(\varphi_T=1\). For nonconstant \(d\), these distributions generally differ. The surrounding expressions involving \(\gamma_0(S)e^{d(S)}\) make the intended endpoint interpretation clear, so this does not undermine the argument.

The mathematical steps check out as follows.

1. **Conditioning and well-definedness.** Conditioning on the data and successful calibration fixes the grid, particle count, reference model and prescribed kernels. The stated independence of final-run streams supplies the required conditional sampling laws. Positivity ensures that every resampling denominator, \(G_t(S^\circ)\), \(b_t\), and \(1-\varepsilon_*\) is strictly positive. For the fixed finite grid and finite state space, all random variables used in the argument are bounded.

2. **Three exact identities.** The change-of-temperature identity follows pointwise from
   \[
   q_{t-1}(S)G_t(S)
   =\frac{\bar Z_t}{\bar Z_{t-1}}q_t(S).
   \]
   Evaluation at \(S^\circ\) gives the claimed ratio \(b_t/b_{t-1}\). The conditional-mean identity correctly integrates mutation conditional on the resampled particles, then integrates resampling conditional on \(\mathcal F_{t-1}\), and averages over particles. No stronger sampling assumptions are introduced.

3. **Weighted mean identity.** The induction is valid for all deterministic functions simultaneously. Its base case follows from the exact initial marginal laws. In the induction step, \(A_t\) is \(\mathcal F_{t-1}\)-measurable, the cancellation involving \(\widehat q_{t-1}(G_t)\) is legitimate, and the function \(R_tK_tf\) is eligible for the induction hypothesis. Invariance supplies precisely \(q_t(K_tf)=q_t(f)\). The proved range \(0\le t\le T-1\) is sufficient for every subsequent application, including the final increment.

4. **Conclusion (i-a).** The factorization of each \(G_t\) and the equality \(\sum_t\Delta_t=1\) give the displayed expression for \(\widehat Z_r/Z\). Interpreting the endpoint notation as described in Finding 1, its deterministic prefactor is \(q_T(S^\circ)/q_0(S^\circ)=1/b_T\). Thus the claimed identity holds for every realization.

5. **Conclusion (i-b), first inequality.** Because \(R_t(S^\circ)=1\), the increment is supported on the complement of the reference state. The pointwise inequality \(|R_t-1|\le R_t+1\), followed by the empirical triangle inequality, justifies the displayed increment bound. Multiplication by positive \(A_{t-1}\), the weighted mean identity, and change of temperature yield
   \[
   \mathbb E|A_t-A_{t-1}|
   \le b_{t-1}\eta_{t-1}+b_t\eta_t.
   \]
   Telescoping from \(A_0=1\) and applying the triangle inequality around \(b_T\) then give exactly the first requested bound.

6. **Conclusion (i-b), second inequality.** The bound
   \[
   \frac{b_s}{b_T}
   =\frac{q_T(S^\circ)}{q_s(S^\circ)}
   \le\frac1{1-\varepsilon_*}
   \]
   is valid for every \(s\). The sum counts the interior \(\eta_s\)'s twice and the endpoint terms once. The separate endpoint calculation
   \[
   \frac{|1-b_T|}{b_T}
   =\frac{|\eta_0-\eta_T|}{1-\eta_0}
   \le\frac{\eta_0+\eta_T}{1-\varepsilon_*}
   \]
   is correct. Adding these bounds gives exactly the stated constant.

7. **Conclusion (i-c).** The triangle inequality for the average of the four relative errors proves the pooled bound. The right-hand sides are shared across islands under the stated conditioning. Independence between islands is unnecessary for this step.

8. **Conclusion (i-d).** The example satisfies the abstract hypotheses: both initial masses are positive, \(d(x)=\log 11\) is finite, \(T=N=1\) is permitted, and the identity kernel is invariant. The two-state space can also be realized as \(\{\emptyset,\{1\}\}\). Its distributions are
   \[
   q_0=(0.99,0.01),\qquad q_1=(0.9,0.1).
   \]
   The relative estimator takes values \(10/11\) and \(10\), with probabilities \(0.99\) and \(0.01\). Consequently,
   \[
   \mathbb E\left|\frac{\widehat Z_r}{Z}-1\right|
   =0.99\frac1{11}+0.01(9)=0.18.
   \]
   The proposed bound without the endpoint term is
   \[
   \frac{0.01+1.1(0.1)}{1.1}
   =\frac6{55}<0.18.
   \]
   The reported full bound \(0.2\) and final bound \(0.2444\ldots\) are also correct.

The boundary cases are covered. For \(T=1\), only the base case of the weighted identity is needed. No argument requires \(N>1\). Every fixed \(S^\circ\in\Omega\) is allowed. If \(\Omega=\{S^\circ\}\), all \(\eta_t=0\), all \(R_t=A_t=b_t=1\), and the asserted errors and bounds vanish.

Reading (i-d) is a fair, precise interpretation of the informal claim that the endpoint term is “essential”: simply deleting that term does not preserve the universal inequality. The supplied example proves this interpretation. It does not establish optimality of the particular endpoint correction or require realization by an actual SMC-BVS dataset, neither of which STATEMENT.md asks for.

VERDICT: verified

# Stage B — Astra #2 review, round 1 (new session <uuid>, gpt-6-astra, reasoning high), 2026-10-22

Packet: STATEMENT.md, PROOF.tex/PROOF.pdf (= proof/PROOF_v2), REPORT_FORMAT.md. Full log: stageB_astra2_r1_full_log.txt.

The proof establishes all four conclusions of STATEMENT.md under the stated hypotheses. I found no fatal errors, gaps, or exposition issues requiring a finding.

1. **Setting and hypotheses.** Conditioning on the data and successful calibration makes the grid, reference model, and prescribed kernels fixed for the argument. The proof uses precisely the stipulated initial distribution, resampling and mutation laws, and kernel invariance. Finiteness of \(\Omega\), positivity of the bridge weights, and finite \(T\) ensure that all denominators are positive and all random variables used are integrable. No mixing assumption, EXP condition, or additional conjecture is invoked.

2. **Three exact identities.** The change-of-temperature identity follows directly from
   \[
   q_{t-1}(S)G_t(S)=\frac{\bar Z_t}{\bar Z_{t-1}}q_t(S).
   \]
   Evaluating this at \(S^\circ\) yields the stated formula for \(b_t/b_{t-1}\). The conditional-mean identity follows by conditioning first on the resampled population and then on \(\mathcal F_{t-1}\). Its denominators are strictly positive. The observation that these calculations require only the specified conditional marginal laws is correct.

3. **Weighted mean identity.** The induction is valid. At \(t=0\), the exact start gives \(\mathbb E\widehat q_0(f)=q_0(f)\). At subsequent stages, \(A_t\) is \(\mathcal F_{t-1}\)-measurable, and the cancellation using \(R_t=G_t/G_t(S^\circ)\) is exact. Applying the induction hypothesis to the fixed function \(R_tK_tf\), followed by the change-of-temperature identity and \(q_tK_t=q_t\), gives \(b_tq_t(f)\). The proved range \(0\le t\le T-1\) suffices for every later application, including the increment at \(t=T\).

4. **Conclusion (i-a).** Factoring \(G_t(S^\circ)\) out of each empirical mean gives
   \[
   \frac{\widehat Z_r}{Z}
   =\frac{\bar Z_0}{\bar Z_T}e^{d(S^\circ)}A_T.
   \]
   The deterministic prefactor equals \(q_T(S^\circ)/q_0(S^\circ)=1/b_T\). Thus the asserted equality holds for every realization.

5. **Conclusion (i-b).** Since \(R_t(S^\circ)=1\), the increment is supported on the complement of the reference state. Positivity of \(R_t\), the triangle inequality, and the weighted mean identity correctly yield
   \[
   \mathbb E|A_t-A_{t-1}|
   \le b_{t-1}\eta_{t-1}+b_t\eta_t.
   \]
   Telescoping from \(A_0=1\) and accounting for the deterministic difference between \(1\) and \(b_T\) gives the first bound. For the second bound, both
   \[
   \frac{b_s}{b_T}\le\frac1{1-\varepsilon_*},
   \qquad
   \frac{|1-b_T|}{b_T}
   =\frac{|\eta_0-\eta_T|}{1-\eta_0}
   \le\frac{\eta_0+\eta_T}{1-\varepsilon_*}
   \]
   are valid. The sum of adjacent-stage terms counts each interior \(\eta_t\) twice and each endpoint once, giving exactly the claimed final bound.

6. **Conclusion (i-c).** The triangle inequality for the average of the four normalized errors transfers the single-island bound to the pooled estimator. The deterministic bounds are common to all islands. Independence between islands is unnecessary for this step.

7. **Conclusion (i-d).** The two-state example satisfies the abstract hypotheses: its initial masses are positive, its score is finite, and the identity kernel preserves \(q_1\). The specified score gives \(q_0=(0.99,0.01)\) and \(q_1=(0.9,0.1)\). With \(N=T=1\),
   \[
   \mathbb E\left|\frac{\widehat Z_r}{Z}-1\right|
   =\sum_y|q_1(y)-q_0(y)|=\frac9{50},
   \]
   whereas the expression omitting the endpoint term is
   \[
   \frac{0.01+1.1(0.1)}{1.1}=\frac6{55}<\frac9{50}.
   \]
   The full middle bound is \(1/5\), and the final bound is \(11/45\), consistent with the proof. This establishes exactly the existential claim requested, without asserting realization by an actual SMC-BVS data set.

The argument also covers \(T=1\), \(N=1\), and a singleton state space; none requires an omitted case.

VERDICT: verified

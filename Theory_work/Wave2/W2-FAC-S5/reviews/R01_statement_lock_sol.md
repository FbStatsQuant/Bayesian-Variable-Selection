# R01 — statement-lock review (Sol)

**Verdict: LOCK-WITH-CHANGES.** Reviewed STATEMENT v1 and PLAN against the requested SoP, FINAL, FAC-B and FAC-A sources and the inherited protocols. No counterexample found to (C1) or (C2-R) under the intended definitions. The conditional target is viable; the following changes are required before lock. This is a statement review, not verification of unwritten lemmas.

## Required changes

1. **Define the statistics and probability space precisely (STATEMENT §§0,3).** Define
   \(\tau_{l\mid R}=(g_l-\Sigma_{lR}\Sigma_{RR}^{-1}g_R)/\sqrt{v_{l\mid R}}\), with \(v_{l\mid R}=\Sigma_{ll}-\Sigma_{lR}\Sigma_{RR}^{-1}\Sigma_{Rl}\), and empty-set conventions. Write \(A_l(U)=[y_l-b\sum_U y_j/(d+ub)]/\sqrt{\psi_u}\), \(\psi_u=d[d+(u+1)b]/(d+ub)\). The exact identity is
   \[
   \tau_{l\mid R}=\frac{\sqrt{\psi_u}A_l(U)+a_u e_R}{\sqrt{\psi_u+a_u^2 V_R}},\quad a_u=\frac d{d+ub},\quad V_R=\left[\rho_b^{-1}+\sum_g\frac{|R\cap G_g|}{d+b|R\cap G_g|}\right]^{-1}.
   \]
   Thus the *contracted* group part is bounded by \(|A_l(U)|\), and \(a_u/\sqrt{v_{l\mid R}}\le\kappa_0\); the controlling error is **e_R**, not always e_T. Declare the enlarged latent Gaussian space, including the independent residual \(r\sim\chi^2_{n-1-p}\) used to reconstruct the score. CC is an event on that space. Π uses the **actual ridge score**, response normalization, signal and residual energy; it is not a path determined by g alone. Specify its tie rule as lexicographic order of the resulting sets, or prove ties have probability zero. Explicitly include the terminal index in CC and take c>0.

2. **Make the score-level bridge and truth-move argument explicit deliverables of PLAN L1/L3/L4.** The Gaussian bound alone does not prove the ridge-score claims. Require uniform control of (a) regularization \(H=(n^2-1)\Sigma+I\) and the resulting nonzero signal leakage even for \(T\supseteq S_0\); (b) \(M_T=\tfrac12(1+o(1))\), including every null one-deletion base; (c) occupancy-dependent determinant increments, with \(L(R\cup l)-L(R)=\log(n+1)+o(1)\) uniformly; and (d) truth deletion/truth-out swap losses, including sets \(T\setminus j\) with j true, where the noise-only reduction is invalid. Prove (d) separately using the Gram floor d and uniform noise-projection bounds, or enlarge CC and restate KL accordingly. For the separate signal argument, no extra CC sets appear necessary. All outside-null bounds must include N₀, not only previously deleted nulls. These are proof obligations, not identified counterexamples.

3. **Correct the positivity and genericity wording (STATEMENT §2).** Partial covariances with i in U are zero, so “every partial covariance ... is >0” and “positive coefficients” for all truth coordinates are literally false. State positivity for l,i outside U, and positive coefficients only on \(S_0\setminus U\), with zero coefficients on conditioned truths, all after sign correction. The intended fact is true: for \(D=\bigoplus_g(dI+bJ)\),
   \(\Sigma^{-1}=D^{-1}-\rho_b(D^{-1}1)(D^{-1}1)^t/(1+\rho_b1^tD^{-1}1)\), whose off-diagonals are strictly negative. Explicitly quantify the finite incidence types over the whole n-sequence (bounded |U|, q̄ and s₀, with truth coefficient labels retained). This gives finitely many proper hyperplanes and a uniform positive lower bound c_FS; it is not an additional unexplained assumption.

4. **Remove unsupported necessity assertions (STATEMENT §0 lines 27–28 and C6).** FAC-A proves sharpness of 1/6 for the full-lattice route in exact compound symmetry; its statement expressly does **not** assert necessity for S5. Failure of a particular lattice envelope does not establish that this specific CC condition is necessary beyond 1/6. Likewise the asserted ingredient “needed beyond 1/2” is a proposed route, not a necessity result. Label both as conjectural proof directions, or supply separate proofs with their precise scopes.

5. **Correct the numerical evidence claims and citations (STATEMENT §0; PLAN step 1).** `numerics/s1_path.py:run` defaults to J=12 and exhaustive=False; its CLI and `s1_grid.sh` do not override this. `bcs_core.py:Path._swaps` then maximizes over selected pairs, not all swaps. Therefore 27/27 runs currently establish a candidate-restricted search outcome, not the full uncapped §6.10 path or the best-swap margin. Relabel those observations, or certify every omitted swap / rerun complete scans. Cite concrete saved output paths for each reported numerical claim, as the protocol requires. This evidence defect does not refute the asymptotic theorem.

## Reduction sanity check and scope

With the above bridge, put \(\epsilon=1/2-\alpha(1+c)^2>0\). The H_q union bound is valid over at most p·2^{q̄} pairs (each A is standard normal; independence is unnecessary). Uniformly, null deletion gains are at least \((\epsilon-o(1))\log n\), and null additions at the CC-covered bases are at most \(-(\epsilon-o(1))\log n\): p=o(n) supplies the multiplier control, while the BB prior favors deletion for k≤p. For a null-out swap, the exact identity
\[
G_{sw}(j,l;T)=G_{del}(j;T)+G_{add}(l;T\setminus j)
\]
then places it below the best deletion by a positive log-n margin. This explains why CC includes *every* null one-deletion set, and why within-group jumps do not by themselves defeat this restricted-exponent reduction. The predecessor's failed general log-n swap margin is not a counterexample to this narrower, conditional claim.

The two-tier framing is acceptable under the protocol: Tier 1 may be proved and checked with KL open, but the HQ target remains PARTIAL. C5 must retain all C1/C3/C4 statistical and implementation premises, including Proposition F's amended resource allocation for delivery; it does not inherit unconditional consistency or council status merely by analogy with FAC-B. The plan can plausibly deliver Tier 1 after the additions above; it does not currently justify promising KL.

Optional: falsify the bridge on variable group sizes, mixed signs, N₀≠∅, m₀=0, and truth-out swaps. Keep complete-scan verification distinct from candidate-restricted diagnostics.

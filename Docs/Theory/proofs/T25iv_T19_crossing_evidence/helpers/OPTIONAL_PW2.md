# Optional investigation: sufficient conditions for PW2

**Overall status: partial.** The sufficient-condition calculations below are derived by the lead. They are outside the reviewed T25(iv) deliverable, have not been independently reviewed, and are not adopted. They supply explicit assumptions and constants. Establishing these assumptions with useful bounds for the actual profiled v3 inputs was **not achieved** in this run.

## 1. The distinction from the reviewed theorem

The reviewed theorem takes PW2 as a hypothesis. This note investigates stronger, more directly interpretable hypotheses that imply PW2. All kernels below are the prescribed actual v3 kernels: none is silently replaced by an exact-refresh kernel. If the displayed kernel conditions hold, the calculation applies to that actual run.

Fix data and calibration, write N=N_e, and retain the notation of STATEMENT.md. At t=1 the particles are iid q_0 and W_0=1, so exactly

\[
E_c[(\widehat q_0g_1)^2-1]
=\{q_0(g_1^2)-1\}/N=\chi_1^2/N.
\]

Thus PW2 always holds at the first stage with a_1=chi_1^2 and nu_1=0. This does not resolve later stages.

## 2. A sufficient condition on the next weight

For each t>=2 suppose explicit constants epsilon_t>=0 and b_t>=0 obey, for every parent state x in Omega,

\[
K_{t-1}g_t(x)\le 1+\epsilon_t,
\qquad K_{t-1}(g_t^2)(x)\le 1+b_t. \tag{A}
\]

These are conditions on a single prescribed mutation round acting on the *next* incremental weight and its square. They are uniform in the possible parent state. They are stronger than ordinary target-law weight-moment bounds and can be expensive to verify.

Then PW2 holds with zero slack and

\[
a_t=b_t+(N-1)(2\epsilon_t+\epsilon_t^2),\qquad \nu_t=0. \tag{B}
\]

**Derivation.** Let H_{t-1} be the history immediately before the stage-(t-1) resampling, after its weight computation. W_{t-1} is H_{t-1}-measurable. If lambda_{t-1} is the weighted empirical parent law, the resulting stage-(t-1) children, after independent resampling and mutation, are conditionally iid with law

\[
\mu_{t-1}=\lambda_{t-1}K_{t-1}.
\]

Independent ancestors and independent child mutations justify the iid assertion even though the unconditional particle law is dependent. For any probability law mu and N iid draws, expansion of the squared empirical mean gives

\[
E[(\widehat q g)^2]=(1-1/N)(\mu g)^2+(1/N)\mu(g^2).
\]

Under (A), mu_{t-1}g_t<=1+epsilon_t and mu_{t-1}(g_t^2)<=1+b_t. As g_t>0, squaring the first upper bound preserves it. Therefore

\[
E_c[(\widehat q_{t-1}g_t)^2-1\mid H_{t-1}]
\le (1-1/N)(2\epsilon_t+\epsilon_t^2)+b_t/N=a_t/N.
\]

Multiplication by the measurable nonnegative W_{t-1}^2 and averaging proves PW2 with (B). No independence of W_{t-1} and the preceding history was assumed.

**When are these constants useful?** If b_t<=b and epsilon_t<=kappa/N uniformly, for fixed b,kappa, then

\[
a_t\le b+2\kappa+\kappa^2/N.
\]

If also chi_1^2<=b, the reviewed theorem implies

\[
\operatorname{Var}_c(W_{\rm pool})
\le \tfrac14\left[\exp\{T(b+2\kappa+\kappa^2/N)/N\}-1\right].
\]

Here we used 1+x<=exp(x). In particular the bound vanishes when T/N tends to zero and b,kappa are bounded. Exact averaging of the next weight, K_{t-1}g_t identically 1, is the special case epsilon_t=0; it requires no bias charge, and a_t=b_t. Exact refresh of the entire state is sufficient for this special case but is not necessary.

The important limitation is explicit: an O(1) epsilon_t generally makes (B) grow as N, which defeats a useful T/N bound. A small measured target chi-square alone does not control epsilon_t.

## 3. An explicit, conservative kernel condition

A pointwise minorisation K_{t-1}(x,dy)>=beta_{t-1}q_{t-1}(dy), 0<=beta_{t-1}<=1, implies

\[
K_{t-1}=\beta_{t-1}\Pi_{t-1}+(1-\beta_{t-1})R_{t-1},
\qquad \Pi_{t-1}(x,dy)=q_{t-1}(dy),
\]

where R_{t-1} is a Markov kernel when beta<1 (beta=1 is exact refresh). Set h_t=max_Omega g_t>=1 and chi_t^2=q_{t-1}(g_t^2)-1. Since R is stochastic, (A) follows with

\[
\epsilon_t=(1-\beta_{t-1})(h_t-1),\qquad
b_t=\beta_{t-1}\chi_t^2+(1-\beta_{t-1})(h_t^2-1). \tag{C}
\]

For the actual v3 round one valid minorisation is

\[
\beta_{t-1}=\min_{y\in\Omega}\frac{q_0(y)}{q_{t-1}(y)}>0.
\]

To see this directly, its independence Metropolis step has off-diagonal transition probability

\[
q_0(y)\min\left\{1,\frac{q_{t-1}(y)q_0(x)}{q_{t-1}(x)q_0(y)}\right\}
=\min\left\{q_0(y),q_{t-1}(y)\frac{q_0(x)}{q_{t-1}(x)}\right\}
\ge\beta_{t-1}q_{t-1}(y).
\]

On the diagonal its probability is at least the proposal probability q_0(x), which has the same lower bound. All preceding steps are stochastic and all subsequent steps preserve q_{t-1}, so the minorisation holds for every full order and for their average. This also agrees with proved wave-1 T09(iv), whose proof was inspected in the collected source.

Equations (B)--(C) are explicit finite-state PW2 constants for the actual kernel. They are mathematically valid for fixed data, but their global maxima and the small minorisation can make them too large. A useful sufficient regime is bounded b_t and (1-beta_{t-1})(h_t-1)<=kappa/N. No claim is made that a discovered crossing or the candidate-grid rule guarantees that regime. Direct verification of (A) may be much sharper than (C), because the actual Gibbs and swap moves can average g_t well even when the independence-step minorisation is poor.

## 4. Allowing an exceptional set of histories

There is also a version with genuine slack. Suppose the conditional moment bounds mu_{t-1}g_t<=1+epsilon_t and mu_{t-1}(g_t^2)<=1+b_t hold on a good event G_{t-1} measurable with respect to H_{t-1}. On its complement, every realised empirical mean is at most h_t. Put L_t=h_t^2-1>=0. The same calculation gives

\[
E_c[W_{t-1}^2\{(\widehat q_{t-1}g_t)^2-1\}]
\le (a_t/N)E_cW_{t-1}^2
+L_t E_c[W_{t-1}^2\mathbf1_{G_{t-1}^c}].
\]

This follows by applying a_t/N on the good event, L_t on the bad event, and then enlarging the good-event first term to its full expectation. Thus one valid slack is

\[
\nu_t=L_t E_c[W_{t-1}^2\mathbf1_{G_{t-1}^c}]. \tag{D}
\]

For a fully explicit but possibly crude alternative, let D=max d-min d. The pathwise evidence bounds and Z_{t-1}/Z_0=q_0(exp(phi_{t-1}d)) imply W_{t-1}<=exp(phi_{t-1}D). Hence a known probability upper bound P_c(G_{t-1}^c)<=p_t gives

\[
\nu_t\le L_t\exp(2\varphi_{t-1}D)p_t. \tag{E}
\]

This displays the remaining difficulty: the relevant exceptional-history charge is weighted by squared evidence. Marginal occupancy or return information alone does not provide the small charge required in (D); using the crude envelope (E) may lose usefulness. This note does not revive the withdrawn RET+OCC variance rate. Wave-1 T14(i)'s first-moment result is not used to infer a second-moment bound.

## 5. Profiling evidence and its limits

The archived `PROFILING_REPORT.md`, section 3, row T25(iv), reports an empirical maximum-over-stage a_t with median **2.74** and 90th percentile **4.78**, and describes the implied scale as approximately 3T/N, approximately **0.02**. It also explicitly says **a_t versus nu_t is not separable at N=2,500**. Section 4 calls PW2 a live target whose measured constants make the variance bound informative.

Those figures were read from the existing report, not recalculated here. Their reported scale motivates the theorem; it is not a proved upper bound on conditional expectations, not a certification of zero slack, and not a verification of (A). The reviewed theorem divides a rigorously established per-island bound by four for the pooled estimate; its whole slack sum is divided too.

Evidence source read locally: `01_Methodology_and_Theory/MASTER_Methodology_and_Plan/deployment_20261022_v3/source_snapshots/PROFILING_REPORT.md`; Decision Point 2 was read beside it. Copies and SHA-256 hashes are archived in this run's `helpers/source_snapshots/`. The initial direct read attempt on NOTS timed out during banner exchange. A later Owls connection succeeded; no remote simulation was needed or launched. This investigation performed no numerical experiments, and did not inspect the raw profiling outputs or independently validate their estimates.

**Assessment.** Sufficient-condition implications (A)--(E): derived analytically above, unreviewed. Useful constants under the stated uniform next-weight averaging assumptions: derived. Verification of those assumptions or of suitably small squared-evidence-weighted exceptional-history charges on the reported crossing experiments: not achieved. Overall optional investigation: **partial**, outside the reviewed result.

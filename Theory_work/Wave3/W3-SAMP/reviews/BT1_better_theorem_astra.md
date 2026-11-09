# BT1 — BETTER THEOREM review (Astra, high)

Date: 2026-11-09. Target: W3-SAMP locked statement v2. This is a strengthening review, not a correctness verdict on that statement. No source, locked statement, or git state was changed.

## Recommendation and ranking

**Replace the concentrated-bridge evidence bound by a T-free bound.** There is a short telescoping proof, not merely numerical encouragement. Under the existing interfaces,

\[
 E[|W_r-1|\mid\mathcal C]\le 2\bar\delta.
\]

Consequently, replace the hypothesis \(1_{\mathcal A}T\bar\delta\to0\) in C-v by \(1_{\mathcal A}\bar\delta\to0\). No dependence on the grid length, particle count, discrepancy range, or terminal mixing is needed. The proof below also gives a sharper distribution-specific constant.

Ranking by paper value times subjective probability of a short successful proof (scores are prioritisation, not certification):

| Rank | Proposed strengthening | Value / 10 | Short-proof probability | Product |
|---|---|---:|---:|---:|
| 1 | T-free C, with explicit L1 constant and rates | 10 | .98 | 9.8 |
| 2 | Dimension-free terminal repair under global overlap, without NC or an escape/entry ratio condition | 8 | .98 | 7.8 |
| 3 | Discovery from scored neighbours, and MAP rather than mass-concentration premise | 7 | .96 | 6.7 |
| 4 | Weighted uniform RB-error bound; pooled-secondary and exact-PIP comparisons | 6 | .98 | 5.9 |
| 5 | Sharper staying constant and rate-relative replacement for NC | 4 | .99 | 4.0 |

All statements below retain the locked localisation: conditional finite-sample inequalities mean “given data and calibration on \(\mathcal A\)” for potential records; integrate bounded probability bounds with \(1_{\mathcal A}\), and use PC for reported outputs on completion. They do not assert delivery probability or validity after conditioning on completion. No design family is a premise.

## 1. T-free concentrated bridge: executable proof

Fix data and a valid frozen calibration record. Write \(s=S_0\), \(a(S)=d(S)-d(s)\),

\[
 c_t=\sum_S\pi_0(S)e^{\phi_t a(S)},\qquad
 V_t=\frac{\widehat Z_{r,t}}{Z_0e^{\phi_t d(s)}},\qquad
 c=c_T=\frac{\pi_0(s)}{\pi(s)}.
\]

Then \(V_0=1\), \(W_r=V_T/c\), and the actual pre-resampling evidence update gives

\[
 V_t=V_{t-1}\widehat q_{t-1}(e^{\Delta_t a}).
\tag{1}
\]

The bridge identity MR-a, after this deterministic rescaling, is

\[
 E[V_{t-1}\widehat q_{t-1}(f)]
 =\sum_S\pi_0(S)e^{\phi_{t-1}a(S)}f(S).
\tag{2}
\]

Use only the bounded, calibration-measurable functions
\(f_t(S)=(1-e^{\Delta_t a(S)})_+\in[0,1]\). Equation (1) implies

\[
 (V_{t-1}-V_t)_+
 \le V_{t-1}\widehat q_{t-1}(f_t).
\]

Taking expectations, summing, and applying (2) gives the exact telescoping budget

\[
 E\sum_{t=1}^T(V_{t-1}-V_t)_+
 \le \sum_{a(S)<0}\pi_0(S)
       \sum_t[e^{\phi_{t-1}a(S)}-e^{\phi_t a(S)}]
 =:b_- =\sum_S\pi_0(S)(1-e^{a(S)})_+.
\tag{3}
\]

In particular \(E(1-V_T)_+\le b_-\). Define also
\(b_+=\sum_S\pi_0(S)(e^{a(S)}-1)_+\), so that \(c-1=b_+-b_-\).
Since \(EV_T=c\),

\[
 E|W_r-1|
 =\frac{2}{c}E(c-V_T)_+
 \le \frac{2}{c}\{b_-+(c-1)_+\}
 =\frac{2\max(b_-,b_+)}c=:\beta.
\tag{4}
\]

Both positive and negative terms vanish at \(s\). Therefore

\[
 b_-\le\delta_0,\qquad b_+\le\sum_{S\ne s}\pi_0(S)e^{a(S)}=c\delta,
\]

and hence

\[
 \boxed{E|W_r-1|\le\beta
 \le2\max\{\delta,(1-\delta)o_0\}
 \le2\bar\delta.}
\tag{5}
\]

This proof uses neither a stopping-time argument nor Hölder nor a union bound over stages. It is valid for every frozen grid and every \(N_e\ge1\). The relevant code is `v3_engine.h:317-322`: evidence is multiplied by the empirical mean of the incremental potentials before resampling. Mutation only enters through MR-a. The bounded test functions in (3) satisfy the locked MR admissibility requirement even when the discrepancy is unbounded across datasets. For random finite T, perform the argument separately on each frozen record, exactly as in the existing freezing interface.

The pooled evidence satisfies the same bound by convexity, with no independence assumption. Markov and bounded integration give all evidence assertions of C-v and discharge NC for every fixed island under \(1_{\mathcal A}\bar\delta\to0\). LT then gives its coded PIP/MPM assertions; §4 below gives direct rates instead.

**Scope of this improvement.** Do not replace the bound for the unweighted occupation sum \(U_r\) in C-ii by a T-free bound. Large T can produce a large occupation sum even while the evidence is accurate; the supplied numerical table already illustrates this. Replace the evidence proof and its downstream assumptions, not that different occupation statistic. The statement still describes a concentrating start, but no longer imposes a start-concentration rate relative to a computational schedule.

**A broader interface, beyond the three candidates.** Formula (4) is useful without concentration at any truth. One may choose any fixed/calibration-measurable scalar anchor \(d_*\), replace \(a=d-d(s)\) by \(d-d_*\), and use the same proof. The sufficient condition \(\beta\to0\) is an interface controlling the integrated change in the geometric bridge. It includes \(d\) constant, where evidence is exact regardless of posterior concentration. Posterior concentration is still needed for truth-selection conclusions.

### Candidate 1: min(T,D+) — valid fallback, superseded

The pointwise factor can be sharpened from \(\min(1,\Delta_tD^+)\) to
\(c_t^{\rm loss}=1-e^{-\Delta_tD^+}\):

\[
 \widehat q_{t-1}(e^{\Delta_ta})
 \ge1-c_t^{\rm loss}(1-A^{br}_{r,t-1}),\qquad
 \sum_tc_t^{\rm loss}\le\min(T,D^+).
\]

Thus a weighted occupation stopping proof is possible. It must retain a terminal normalisation/posterior term, such as \(o_1\); replacing every term by \(\min(T,D^+)\bar\delta\) is not justified when \(D^+=0\). With P-CONC, the proposed rate condition is a sufficient alternative. But (3) integrates the actual negative potential loss against the exact unnormalised marginals and telescopes it, which is stronger and shorter. Do not spend a separate proof ticket on this fallback.

### Candidate 2: T-free C — adopt

Equations (1)–(5) supply the missing proof. The numerical decrease in error with T is compatible with this bound; monotonicity in T is not asserted or needed.

## 2. Replace NC for output accuracy by terminal repair

This is an alternative **output theorem**, not a theorem that terminal rounds restore NC. The code does not update evidence during terminal rounds. No amount of terminal repair can repair an already collapsed W.

Let

\[
 M=\max_{S\in\Omega}\frac{\pi(S)}{\pi_0(S)}\ge1,
 \qquad e_L=(1-1/M)^L
\]

(take \(e_0=1\)). These are target/start interface quantities, not realised-particle properties. The independence MH kernel has the elementary minorization

\[
 K_I(x,dy)\ge M^{-1}\pi(dy).
\tag{6}
\]

Proof: its accepted off-diagonal mass is
\(\min\{\pi_0(y),\pi(y)\pi_0(x)/\pi(x)\}\ge\pi(y)/M\); the diagonal satisfies the same lower bound by the proposal-to-self contribution. Every other elementary kernel preserves \(\pi\). For every fixed order, writing the round as \(K_{\rm pre}K_IK_{\rm post}\) preserves (6), because \(\pi K_{\rm post}=\pi\). Averaging orders preserves it too. Splitting off the common \(\pi/M\) component proves

\[
 \sup_x\|K_1^L(x,\cdot)-\pi\|_{TV}\le e_L.
\tag{7}
\]

Let \(E_r=\|\widehat p_r-1_s\|_\infty\), and let \(\lambda_0\) be ST's actual first-exit sum, truncated by 1 if desired when used as an escape probability. A stationary particle's measured-round path has expected uniform RB error at most

\[
 g:=\min\{1,\kappa_0+\delta+(1-\delta)\lambda_0\}.
\tag{8}
\]

Indeed, entering away from s costs at most one, entering at s and ever leaving costs at most one, and otherwise the entire vector is within \(\kappa_0\) of truth. Average the four rounds and use convexity of the sup norm. Coupling at the start of measurement in (7), then using common future randomness, gives for an arbitrary bridge-end population

\[
 \boxed{E E_r\le g+e_L,\qquad
 E(1-A_{r,q})\le\delta+e_L\quad(0\le q\le4).}
\tag{9}
\]

No independence across particles, growth of N, or union bound over p is needed. Thus P-CONC plus \(1_{\mathcal A}L/M\to\infty\) gives primary PIP consistency, MPM recovery, and HPM recovery on completion. For HPM, absence of a truth endpoint has probability at most the expected fraction away at that endpoint. This improves BLIND_astra2 Theorem 5 in the concentrating-posterior regime by removing its \(\log(p+1)/N_e\to0\) condition.

### Candidate 3: terminal repair — remove its unnecessary escape/entry condition

The candidate uses \(\widetilde M=M/[\pi(s)/\pi_0(s)]\), so
\(L\pi_0(s)/\widetilde M=L\pi(s)/M\). Under P-CONC, its first condition is precisely the useful condition \(L/M\to\infty\). Its second condition \(\lambda_0\widetilde M/\pi_0(s)\to0\) is unnecessary. The stationary regeneration argument avoids accumulating escape errors across the entire burn-in. Only the fixed measured path needs an escape bound.

**Implication by start mass?** The new T-free C is already implied by \(\pi_0(s)\to1\), strictly weaker than the locked rate condition \(T\bar\delta\to0\). However, a lower bound on \(\pi_0(s)\) alone does not control M, even if \(\pi_0(s)\to1\). On a three-state interface, set \(\pi(s)=\pi_0(s)=1-\epsilon\), assign a second state posterior mass \(\epsilon/2\) and start mass \(\epsilon e^{-H}\), and assign the remaining masses to the third state. Then \(M\ge e^H/2\), for arbitrary H. This is a counterexample to that logical implication, not a claim that these tables arise from a particular regression design.

Conversely, the minorization route can allow nonconcentrating starts. Under the additional pairwise domination interface
\(\max_S\pi(S)/\pi_0(S)\le C/\pi_0(s)\), it is enough that \(L\pi_0(s)\to\infty\); with production L of logarithmic order this allows \(\pi_0(s)\to0\). Domination is an extra hypothesis and must be stated, not inferred from the atom mass. For example, at the abstract interface level, assigning the nontruth start probabilities proportionally to nontruth posterior probabilities makes this domination transparent.

Do not claim a general impossibility theorem for all mass-only output conditions from the three-state example. It proves the failure to control global overlap; it does not prove failure of the coded local moves. Those moves can repair states that defeat the independence bound, as the supplied “near” numerics show.

## 3. Strictly stronger discovery for the coded method

### 3.1 Weaken the statistical premise immediately

Let \(S^\dagger\) be the global `hpm_better` maximiser over \(\Omega\), with the coded tie rule. In D-iii replace \(P(\delta\ge1/2)\) by
\(P(S^\dagger\ne S_0)\). In D-iv replace P-CONC by \(P(S^\dagger=S_0)\to1\). This is strictly weaker: a unique global mode need not have mass approaching one or even exceed one half. The proof is the ledger maximum property alone.

### 3.2 A concrete all-history bound that counts Gibbs scoring

Here is an explicit enhancement that avoids assuming independence of local proposals. Put \(m=p+B+2\), \(w=\pi/\pi_0\), and let
\(\mathcal F(s)=\{x\in\Omega:|x\triangle s|=1\}\). Define

\[
 b_G=\frac1m\sum_{x\in\mathcal F(s)}\pi_0(x)\frac{w(x)}M
 =\frac{\pi(\mathcal F(s))}{mM},\qquad a_0=\pi_0(s).
\tag{10}
\]

For **each particle terminal round**, whatever its entry state and past ledger, the conditional probability of scoring s is at least \(a_0+b_G\). A draw of s already scores it. Disjointly, suppose the independence proposal is x in \(\mathcal F(s)\), is accepted, and is immediately followed by the unique Gibbs label j flipping x to s. The probability that I is immediately followed by this specified label in a uniform permutation is \(1/m\). Conditional on any pre-I state, acceptance of x is at least \(w(x)/M\). The Gibbs step scores the other configuration before its acceptance decision. Sum these disjoint proposal-value events. This argument remains valid although the pre-I state depends on the permutation: the acceptance lower bound is uniform in that state.

There are \(N_e(L+4)\) such terminal particle rounds. Sequential conditioning, retaining the ordinary initial/bridge draw bound for the earlier part, gives

\[
 \boxed{P(s\notin\mathcal M_r\mid\mathcal C)
 \le(1-a_0)^{N_e(1+T)}
       (1-a_0-b_G)^{N_e(L+4)}.}
\tag{11}
\]

This is strictly smaller than the draw-only bound whenever \(\pi(\mathcal F(s))>0\) and the ordinary bound is nonzero. Positivity of \(\pi_0\) guarantees feasibility of the expression; in particular \(b_G\le(1-a_0)/m\). Under IND-T raise the whole right side to the fourth power. Without IND-T retain the single-island statement. A sufficient discovery condition is
\(N_e(1+T)a_0+N_e(L+4)(a_0+b_G)\to\infty\), interpreted on \(\mathcal A\).

The same construction can add a disjoint two-swap-neighbour term. Let \(\mathcal U(s)\) consist of x with \(|x|=|s|\), \(|x\triangle s|=2\). Requiring I immediately followed by U gives

\[
 b_U=\frac1m\sum_{x\in\mathcal U(s)}
 \pi_0(x)\frac{w(x)}M\frac1{|x|(p-|x|)}.
\]

The denominator is nonzero on this set. Add \(b_U\) to \(b_G\) in (11); the proposal classes are disjoint. Neighbour-swap variants use the actual proposal probability and disjoint adjacency events; they need not be included to establish strict improvement.

**Code basis:** `step_gibbs` calls `eval(tmpQ, ME_GIBBS_FLIP)` before the Gibbs uniform; `step_uswap` and `step_nswap` call `eval` before acceptance; `draw_order` samples a uniform permutation. These are stronger usable facts than CC1 alone. CC2 handles cache idempotence.

**Limit of this enhancement:** the global M can make (10) very small. Do not sell (11) as a sharp description of the observed local-search advantage. More ambitious, still design-agnostic bounds can replace M by an interface controlling likelihood ratios on states reachable before I, but that requires a separately proved reachability property. Nor may one casually multiply empirical local hit frequencies: adaptive states invalidate that argument. The exact draw-miss equality itself cannot be improved; the method-miss upper bound can.

## 4. Stronger conclusions and rates available cheaply

### 4.1 Uniform evidence-weighted RB error

Retain g from (8). MR at measured-round entries and ST's first-exit argument imply

\[
 E[W_rE_r]\le g.
\tag{12}
\]

Proof: the deterministic path decomposition is \(E_r\le\kappa_0+\overline B+\overline\Lambda\). MR gives \(E[W_r\overline B]=\delta\). Conditional on the history before each terminal round, W is already fixed and a particle at s exits with probability at most \(\lambda_0\); MR gives weighted mass \(1-\delta\) at s. Also \(EW=1\) and \(E_r\le1\). This proves (12), including the truncation by one. This controls the maximum over all coordinates without a factor p.

Consequently, an alternative LT bound is

\[
 P(E_r>u)\le\frac{g}{u\eta}+P(W_r<\eta).
\tag{13}
\]

It is not uniformly better in constants than every locked LT threshold, so retain the minimum of valid bounds. Its main advantage is that it composes directly with evidence and pooling.

Under (4), since \(E(1-W_r)_+=\tfrac12E|1-W_r|\),

\[
 \boxed{E E_r\le g+\beta/2.}
\tag{14}
\]

This gives an O(\(\bar\delta\)) expected uniform truth-error, and hence O(\(\bar\delta\)) MPM failure probability for the fixed four-island primary estimator, conditional on data/calibration. Indeed the primary error is at most the average island error and MPM failure implies error at least one half, so the failure bound is \(2(g+\beta/2)\). It avoids both the locked factor T and a union over islands. For random data integrate the bounded probability bound, not an uncontrolled expectation of \(\bar\delta\).

### 4.2 Comparison to the exact posterior PIPs

For \(p^\pi_j=\pi(j\in S)\),
\(\|p^\pi-1_s\|_\infty\le\delta\). Thus (14) also bounds expected uniform error relative to exact PIPs by \(g+\beta/2+\delta\).
There is a sharper **bias** statement requiring no concentration argument: MR-c and \(0\le\widehat p_r(j)\le1\) give

\[
 |E\widehat p_r(j)-p^\pi_j|
 =|E[(1-W_r)\widehat p_r(j)]|
 \le\tfrac12E|1-W_r|\le\beta/2.
\tag{15}
\]

The factor one half uses \(E(1-W_r)=0\); it is uniform in j and holds for the primary average. This is a bias bound, not by itself a realised Monte Carlo accuracy bound.

### 4.3 Evidence-pooled secondary estimator

For the mathematical estimator
\(\widetilde p=\sum_rW_r\widehat p_r/\sum_rW_r\), set \(\overline W=\frac14\sum_rW_r\). Equations (12) and convexity give

\[
 E[\overline W\|\widetilde p-1_s\|_\infty]\le g,
\quad
 P(\|\widetilde p-1_s\|_\infty>u)
 \le g/(u\eta)+P(\overline W<\eta).
\tag{16}
\]

Only pooled non-collapse is needed here, rather than NC for every island. Under T-free C, \(E|\overline W-1|\le\beta\), so the analogue of (14) follows. A deterministic comparison is

\[
 \|\widetilde p-p_{\rm primary}\|_\infty
 \le\frac{\sum_{r=1}^4|W_r-\overline W|}{8\overline W}.
\tag{17}
\]

This is the total-variation distance between the four normalised evidence weights and uniform weights. Do not label \(\widetilde p\) a current reported field: the inspected assembly computes `pip_primary = rowMeans(P)` and `mpm`; the secondary object is a mathematical/reconstructible estimator from `pip_r` and `log_Z_r`. No implementation change is proposed here.

### 4.4 Log-evidence tails and rates

For \(\overline W=\widehat Z/Z\), (4) gives

\[
 P(|\log\overline W|>u)
 \le\min\left\{1,\frac{\beta}{1-e^{-u}}\right\},\qquad u>0.
\tag{18}
\]

The same holds islandwise. If \(1_{\mathcal A}\bar\delta=O_P(r_n)\) with deterministic \(r_n\downarrow0\), bounded conditional Markov arguments give localised \(\overline W-1=O_P(r_n)\), \(\log\overline W=O_P(r_n)\), and uniform primary PIP truth-error \(O_P(r_n)\). These are probability rates, not L1 rates under the joint data law unless the corresponding integrability is supplied. Nor does an L1 bound for W imply an L1 bound for log W: rare extremely small values require extra lower-tail integrability.

## 5. Two smaller improvements and sharpness boundaries

**ST constant.** Partition nontruth states into feasible single flips, swaps, and the remainder. Write their posterior odds masses as \(o_F,o_U,o_R\), summing to \(o_1\). Gibbs exits sum to at most \(o_F\). Each swap label exits only to swap neighbours, so by invariance its exit probability is at most \(o_U\). The independence exit probability is exactly

\[
 \sum_{y\ne s}\pi_0(y)\min(1,w(y)/w(s))
 \le\min\{1-\pi_0(s),\pi_0(s)o_1\}.
\]

Thus
\(\lambda_0\le o_F+(B+1)o_U+\min\{1-\pi_0(s),\pi_0(s)o_1\}\le(B+2)o_1\le18o_1\).
Use the actual sum when available; 18 replaces 19 without changing hypotheses. This is a minor constant improvement, not the principal recommendation.

**NC can be weakened even without terminal analysis.** By (13), it suffices to choose a positive calibration/data-measurable threshold \(\eta_n\) such that \(1_{\mathcal A}g/\eta_n\to0\) in probability and \(P(\mathcal A\cap\{W_r<\eta_n\})\to0\). This allows \(W_r\to0\) on ordinary runs, provided collapse is slower than posterior error. The threshold formulation is strictly weaker than bounded-away-from-zero NC. It remains a computational interface, not a primitive design theorem. It also makes precise why unbiasedness and lower tails must be distinguished: a mean-one random variable can be tiny on most runs and huge on rare runs.

**What is already sharp / not claimed.**

- D's exact no-draw probability is an equality. Improving its exponent without another scoring mechanism is impossible.
- The \(\kappa_0\) error baseline cannot be removed from a pathwise statement: on a measured path staying at s throughout, the RB vector equals \((o_j(s))_j\), so its uniform error equals \(\kappa_0\). Endpoints at s alone are insufficient for this observation.
- For arbitrary N including N=1 and T=1, linear dependence on a small concentration error is natural: a rare initial nontruth draw can give a fixed evidence error before any mutation. No uniform higher-order rate follows just from concentration and the interfaces. The new proof does not assert optimal constants for every coded regression instance.
- P-CONC alone gives neither NC nor general PIP accuracy; the supplied trap numerics exhibit the relevant obstruction. Those finite numerical experiments are motivation, not an asymptotic counterexample proof. Terminal repair can produce accurate PIPs while W remains collapsed, as in the revised “near” results.

## Source trail and proposed disposition

Read: W3-SAMP `STATEMENT.md` v2, `ASSUMPTION_MAP.md`, `PLAN.md`, `lemmas/CC_code_check.md`, both requested numerical result files; Wave3 `PROGRAM.md` item 4 and `PROTOCOL.md`; T12 frozen-run `STATEMENT.md`; the requested Wave2 Astra/Fable theorem passages and Opus §1(d); and the production elementary steps, `run_island_s`, and final assembly in `v3_run.R`. The revised sec4b numerics, rather than the erroneous original “near” caption, inform the discussion of repair.

Recommended lock amendment: adopt (4)–(5) and the T-free hypothesis first; add (14)–(15), (18), and the weaker MAP premise to D as cheap corollaries; add terminal repair as a clearly separate alternative theorem; include (11) if the paper wants a concrete local-scoring contribution. Keep the secondary-estimator result labelled mathematical. Preserve all existing completion/localisation language and dependency statuses. These are new proof proposals with detailed derivations, not claims of independent proof-check or council approval.

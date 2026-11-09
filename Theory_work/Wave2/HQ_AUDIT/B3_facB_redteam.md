# HOLDS-WITH-AMENDMENTS

Independent adversarial audit of **Theorem FAC-CS, W2-FAC-B, STATEMENT.md v3.1**. Date: 2026-11-09.

**No FATAL or MAJOR defect found in (C1), (C1-M), (C2), (C3), or the conditional extension (C4).** One MINOR wording amendment is warranted: the exact reduction is a common-centre reduction, but swaps are not ordered by absolute distance to that centre. The displayed swap identity and its subsequent use in L4 are correct. No change to the theorem's hypotheses or conclusions is needed.

This verdict is for fixed \(s_0\), fixed \(\rho\in(0,1)\), fixed nonzero coefficients as specified, exact Gram, eventual \(p\le\lfloor n/2\rfloor\), and the named implementation/dependency premises. It is not uniform as \(\rho\uparrow1\). C3 gives consistency jointly with output; unconditional consistency requires C4's fallback and allocation premises.

Read independently: STATEMENT.md, L1–L5, the numerical implementation and summaries; checked the relevant shipped score, LS0, cap, fallback and preflight code, the final posterior theorem, Proposition F and Lemma S. The numerical checks below are fresh implementations, not calls to the ticket's numerical modules. Only this audit file was written. No git commands, commits, checkout/index changes, or sub-agents were used.

## Findings and exact fixes

### F1 — MINOR: disambiguate the “every-neighbour one-dimensional reduction”

**Locations:** `Theory_work/Wave2/W2-FAC-B/lemmas/L1_cs_reduction.md:84-85` and `:98-99`. The precise, already correct qualifications are in `STATEMENT.md:94-97` and `L1_cs_reduction.md:63-65,79-81`.

The question “is every neighbour gain a monotone function of \(|\xi_j-x_T|\)?” has answer **no**. For null flips, yes. For truth flips there is the coefficient shift in L1.4. For a swap the relevant scalar is
\[
 V_{jl}=\tau_l^2-\tau_j^2-\gamma_k(\tau_l-\tau_j)^2
       =(1-\gamma_k)\tau_l^2+2\gamma_k\tau_j\tau_l-(1+\gamma_k)\tau_j^2.
\]
The sign-dependent cross term cannot be suppressed. This is a wording qualification, not a newly discovered error in the displayed formula: L4 uses \(V_{jl}\), rather than an invalid radial ordering, throughout its swap comparisons.

**Exact counterexample to the stronger radial reading.** Set \(n=100,p=4,\rho=1/2,S_0=\{1\},\theta_1=1,T=\{1,2\}\). In L1's enlarged representation choose
\[
 \xi=(0,1,1.5,-1.5),\quad r=95,\quad
 \eta=\frac{1-\sqrt{99}/(\sqrt{1/2}\,9999)}{1+2/9999}
      =0.9983930359684561.
\]
Then \(\varrho=1,\ x_T=0,\ \tau_2=1\), and \(\tau_3,\tau_4=\pm1.5\). Both outside nulls have the same distance from the centre, but
\[
 \gamma_2=(3+2/9999)^{-1},\quad
 V_{2,3}=1.1666722224074135,\qquad
 V_{2,4}=-0.8331944398146605.
\]
Independent dense D0 scores give swap gains \(+0.576903693303251\) and \(-0.40796757044438436\), respectively. This is an admissible exact-Gram sufficient-statistic configuration; nearby configurations preserve the opposite signs. It refutes any purported distance-only swap rule.

**Exact fix:** replace L1:84-85 with:

> Each deletion gain is strictly decreasing in \(|t_j|\), and each addition gain is strictly increasing in \(|t_l|\), with common residual origin \(c_T\). A swap gain is strictly increasing in the signed-pair quadratic \(t_l^2-t_j^2-\gamma_k(t_l-t_j)^2\); it is generally not determined by either absolute residual alone.

At L1:98, replace “the scan is a one-dimensional problem” with “the null coordinates lie on a fixed line, with radial flip orderings about \(x_T\) and the signed-pair swap score of L1.3.” Retain STATEMENT:97, which correctly restricts the radial claim to null deletions/additions. **Do not replace the production scan by a nearest-distance swap heuristic.**

No other amendment is required for the audited theorem.

## Checks of the six requested pressure points

### 1. Exact score, prior, ridge, response scaling, and centre

**Survives, with F1's qualification.** I re-derived the Sherman–Morrison identities and checked every flip and swap against dense matrix scores. The size prior contributes exactly
\[
 \log[w(k-1)/w(k)]=\log((2p-k)/k).
\]
Its cap normalizer is model-independent. Under P, \(K=p\), so it introduces no extra geometric term. The ridge gives \(H=\alpha I+\beta J\), with the \(+1\) retained in \(\alpha\), hence \(\kappa_n=(1-\rho)/\rho+1/[\rho(n^2-1)]\). Dropping that ridge correction would change the exact centre.

The response is standardized once for the whole data set, not re-standardized per model. Thus \(s\) is random and global, \(y^\top y=n-1\), and the shipped standardized IG rate is \(b_0=.01\). In unstandardized response units this corresponds to rate \(.01s^2\). The reduction retains \(s\) in \(z,\kappa_1,\psi_T\), and in the multiplier; it does not assume standardized errors are iid Gaussian. The \(.02\) and \(\nu=n/2+.01\) are also retained.

Shipped-score checks: `Scripts/SMC_BVS/core/cpp/v3_score.h:14-17,39-64,204-223` agree with D0 and L1. The representation enlarging the probability space is legitimate: \((g,r)\) has the original joint law, and method outputs are functions of \((g,r)\). Auxiliary sign events need not themselves be measurable in the original representation.

For \(T\supseteq S_0\),
\[
 z_j-\gamma_k B_T=\kappa_1(\xi_j-x_T)+\lambda_1\theta_j^*.
\]
Consequently the same exact \(x_T\) orders null deletions and additions. Truths retain their deterministic shift. Swaps retain both signed coordinates. L4's convexity reduction in the outside coordinate is correct; the maximum over outside nulls occurs at an extreme coordinate, not necessarily at the largest absolute distance for every fixed outgoing coordinate.

### 2. Conditional Rademacher control and an adaptive path

**Survives.** The conditioning in `lemmas/L3_event.md:51-54` is on all null magnitudes, not on the realized path, the start-mode event, E2, the offset, or a retained set. Conditional on those magnitudes, the signs in their magnitude ordering are iid Rademacher. Hoeffding is applied to every deterministic prefix length \(j\); the summable union over \(j\) constructs one simultaneous event E5 before looking at the path.

The key step at `lemmas/L4_path.md:110-121` is then pointwise. In the cross-zero case, if \(x_i>\Delta_i/2\), the retained set \(K\) is contained in a magnitude prefix \(\operatorname{Top}(J)\) and the omitted elements of that prefix are all positive. Therefore
\[
 \sum_K\xi_j\le D_J.
\]
The prefix index \(J\) is random and path-dependent, but E5 controls **all** \(J\) simultaneously. Its count bound yields \(J\le5m\) for the stated eventual onset. Negative \(x_i\) is symmetric. If the hole is wholly on one sign side, all observations of the opposite sign remain, giving the separate \(m\ge m_0/3\) bound.

Thus the proof does not incorrectly claim iid signs conditional on the selected retained set. Dependence of \(s\), E2 and the start-mode event on signs causes no conditioning problem: the proof intersects events and uses a union bound on their failures. No union over \(2^{m_0}\) retained sets is needed.

The induction order is valid: two-sidedness at \(i\) uses the preceding centre bound; the gap bound uses two-sidedness at \(i-1,i\); then the current centre bound follows; finally move dominance closes the induction. The deterministic gap lemma uses \(k-1+\kappa>1\), which follows from \(s_0\ge1\) and a remaining null. It would not extend automatically to the null-truth case \(s_0=0\).

### 3. End phase, majority deletion, and \(c_D\)

**Survives.** At `lemmas/L4_path.md:160-189`, retained coordinates are extreme one-sign prefixes. E6 makes their magnitudes \(\bar H+O(\delta_e)\), and
\[
 x=(I\bar H+E')/(k+\kappa),\quad |E'|=O(L_n),\quad
 m_1\delta_e\to0,\quad L_n=o(H).
\]
For \(I\ge1\), \(x\gtrsim H/(s_0+m_1+\kappa)\gg\delta_e\), so the closest retained point is positive. The majority deletion reduces \(I\) by one; at \(I=0\) either sign gives \(|I'|=1\). The normalized imbalance cannot increase during the \(|I|\ge2\) stage. This is deterministic after the event is fixed, including one-sided configurations.

The claimed margin is strictly positive:
\[
 c_D=\frac12-\frac1{s_0+1+\kappa_\infty}
     =\frac{s_0-1+\kappa_\infty}{2(s_0+1+\kappa_\infty)}>0.
\]
At the worst fixed sparsity \(s_0=1\),
\[
 c_D=\frac{1-\rho}{2(1+\rho)}.
\]
For example \(\rho=.9999\) gives about \(2.5001250\,10^{-5}\). There is no positive margin uniform over \(\rho\in(0,1)\), and no such uniformity is claimed. Allowing \(\rho_n\uparrow1\) would require a new argument.

The balanced \(m\ge2,I=0\) deletion bound and the \(|I|=1\) addition bound use precisely this same denominator. When \(|I|\ge2\), the entry imbalance gives the separate fixed positive margin; swaps are bounded using their signed quadratic. At \(S_0\), truth-out swaps remain covered by TL, not just by the addition estimate.

A fresh ideal-end algebra sweep checked 760,328 feasible coefficient comparisons over \(s_0\in\{1,2,4,16\}\), \(\rho\in\{10^{-8},.001,.3,.7,.95,.99999999\}\), \(1\le m\le250\), parity-compatible \(I\), the entry restriction for \(|I|\ge2\), and \(\log p/\log n\in\{.005,.2,.5,1\}\). No sign or dominance violation; smallest normalized slack was \(2.49999998\,10^{-9}\). The strict positivity is established by the displayed algebra, not by this finite grid.

### 4. Small \(p\), bounded \(p\), and oscillating regimes

**Survives.** `lemmas/L4_path.md:82-93` deliberately avoids comparing \(L_n\) with \(H\). Uniformly for \(p\le n^{1/200}\),
\[
 \bar H^2\le(\log n)/90,\qquad
 (2\bar H+CL_n)^2\le .1\log n
\]
eventually, since \(L_n/\sqrt{\log n}\to0\). The fixed number of \(S_0\cup N_0\) coordinates have the E1 bound. With \(M_T\le1+o(1)\), this yields the separated deletion/addition/swap bounds quoted there. TL handles truth moves, including the \(k=1\) endpoint; the factor \(1+\gamma_{k-1}\le2\) is needed only for null deletions, where \(k\ge2\).

For the large regime, \(p>n^{1/200}\) implies \(m_0\ge p-s_0-15\), hence uniformly diverging \(m_0\), \(H^2\gtrsim\log n\), \(m_0/m_1\to\infty\), and all the required order-statistic events. With fixed class parameters and block bound 16, one can take the maximum of the two deterministic onsets and the probability error bounds. The per-index split is exhaustive; oscillating \(p_n\) does not create a missing subsequence. Bounded \(p\), \(m_0=0\), and \(p=s_0\) are covered by the small regime and its empty-set conventions.

### 5. Corollary M / masked truths / FS′

**Survives.** `lemmas/L2_start.md:89-101` supplies the missing witness when the only proposed addition has \(U=\varnothing\) and zero marginal truth covariance. A null in that same block has
\[
 c(\varnothing,l')=\rho\,\vartheta(S_0)\ne0
\]
by FS-a and is absent when the block is empty. Adding it strictly improves the start objective. It need not belong to \(S^*\): one improving neighbour suffices to exclude the current set from global maximization. Once the block is nonempty, FS-b for \(u\ge1\) handles the truth. The size cap causes no obstruction because \(K=p\). The other half of L2's uniqueness proof is unchanged.

Fresh exhaustive \(p=8\) start-mode checks used the genuinely masked coefficient pair \((-\rho,1)\), which satisfies FS′, with both a same-block null witness and a block containing all truths plus a null. All 12 admissible cases at \(n=10^8,10^{12}\) gave \(S^*\) uniquely in floating-point comparison. At \(n=10^4\), 4/6 did so; both misses were at \(\rho=.95\). As a negative control, putting the masked truth in a singleton block violates FS′ and failed to give \(S^*\) in all 9 checked cases. That control supports retaining the block-witness condition.

L3–L5 do not otherwise use FS or marginal visibility, so the downstream extension under FS′ is valid.

### 6. C4 delivery extension

**Survives relative to its expressly inherited premises.** `lemmas/L5_assembly.md:55-68` verifies the inputs that depend on the design class: nonconstant standardized columns, a.s. nonconstant response, no dropped columns, and
\[
 Q_A\ge y^\top y/(n+1)>0.
\]
Lemma S's scorer/input argument is not a relevance-set or sparse-start theorem. Thus it applies to exact-Gram CS. The resource accounting transfers because the cap adds at most \(K\) scans, each with at most \(q(p)=p+p^2/4\) neighbours. Proposition F already uses the amended \(W_G,M_G\), the LS0 timing preflight and archive terms. None relies on \(|\widetilde S_0\setminus S_0|=O(\log n)\).

The consistency step has the correct direction:
\[
 \mathcal O\cap\{\widehat S^+\ne S_0\}
 \subseteq\{\pi(S_0)\le1/2\}\cup\mathcal K_n^c.
\]
It uses discovery \(\Pr(\mathcal K_n^c)\to0\) directly; it does not infer it from \(D_n\to0\). The exact-Gram CS eigenvalues, fixed signal and \(p\le n/2\) verify T03♯, so \(E[1-\pi(S_0)]\to0\). Fallback plus allocation gives \(\Pr(\mathcal O)=1\). CAL and fallback-frequency estimates are unnecessary.

Relevant shipped-code checks agree with the extension: `cpp/v3_core.cpp:465-480` forms the augmented cap and runs LS0; `cpp/v3_engine.h:370-415` scans fully before enforcing the move cap and retains scan scores; `v3_calib.R:120-170` retains a complete fallback and substitutes it before normal continuation; `v3_fit.R:43-65` charges the augmented scans and archive. These paths are relative to `Scripts/SMC_BVS/core/`.

This check does not upgrade EX-A, MACH, e4, GUARD-W or the inherited code-reading audits into unconditional binary reliability claims. In particular C4 does not prove delivery under the default finite allocation or floating-point execution.

## Fresh falsification numerics

Environment: Python 3.13, NumPy 2.3.0, SciPy 1.15.3. Code was passed on stdin to `C:/Users/felip/AppData/Local/Programs/Python/Python313/python.exe -B -`; no numerical files or bytecode caches were written. Reproduction code is embedded below.

| Test | Coverage | Result |
|---|---|---|
| Dense D0 versus all L1 neighbour identities | 24 data sets; \(p=8\); every subset and feasible flip/swap; \(n=20,200,10^6\); \(\rho=.001,.3,.95,.9999\); one and four truths | 135,168 comparisons; max quadratic discrepancy \(1.7940\,10^{-11}\); max gain discrepancy \(5.4826\,10^{-7}\) |
| Independent fast scanner versus dense scores | 79 visited states, \(p=12\), \(n=40,200,10^4\), same four correlations | Max gain discrepancy \(1.4165\,10^{-11}\); max centre discrepancy \(3.4651\,10^{-13}\) |
| End-phase coefficient inequalities | 760,328 comparisons, including \(\rho=.99999999,s_0=1\) | No violation |
| Exhaustive masked-truth starts | 27 data sets, every one of \(2^8\) models | Admissible FS′ layouts: 16/18 successes; both misses at \(n=10^4,\rho=.95\). Invalid singleton control: 0/9 |
| Full-path dominance checks | 254 data sets; 1,005,168 visited/terminal states; \(n=10^4,10^8,10^{12},10^{100},10^{300}\); \(p=12,512,2000\), plus large-\(p\) and masked cases | 242 successes; 12 failures, all at \(n=10^4,\rho=.9999\), where truth moves win. All 206 cases with \(n\ge10^8\) passed |
| Large-\(p\) paths | Eight cases with \(p=100000,\ s_0=1,\ N_0=\varnothing,\ \rho=.3,.95,\ n=10^8,10^{300}\), two seeds each | All made exactly 99,999 null deletions and terminated at \(S_0\) |
| Boundary \(p=n/2\) paths | Eight cases at \(n=200000,p=100000\), \(\rho=.001,.3,.95,.9999\), one/four truths, plus \(n=10^6,p=500000,\rho=.95,s_0=1\); \(|N_0|=15\) in the one-truth cases | 8/9 successes; one finite-\(n\) truth-move failure at \(n=200000,\rho=.9999,s_0=1\); largest case made exactly 499,984 null deletions |

For the full-path test, the scanner evaluates exact log1p gains using the shipped prior and ridge, not a quadratic approximation to those gains. At each retained set it checks the closest null deletion against zero, the best addition, the best null-out swap, all truth deletions and the best truth-out swaps. A sorted-gap representation makes the closest-coordinate lookup fast. For a fixed outside extreme, the swap quadratic is concave in the outgoing residual and is maximized at the retained coordinate nearest \(\gamma_k\tau_l/(1+\gamma_k)\); this search also checks truths. Exhaustive scans at \(p\le20\), and the separate dense validation, checked these optimization shortcuts. The run stops at the first dominance failure; successful runs therefore verify the full actual path, not merely a forced deletion trajectory.

The tests intentionally include a nonempty \(N_0\) and genuinely masked truths. They use exact-Gram sufficient statistics, so the largest \(n\) does not require allocating an \(n\times p\) matrix. \(10^{300}\) denotes a floating-point sufficient-statistic experiment, not an actual production run at that dimension; fluctuations below floating precision in the chi-square residual are unresolved. Its \(\log\log n\) is still only 6.538. None of these simulations validates the enormous eventual-onset conditions of E6/E7 or L4:117. The proof, not the simulations, must carry those conditions. The finite-\(n\) failures are retained as falsification evidence and do not contradict the stated asymptotic theorem.

Across both path suites: **263 data sets, 2,305,038 checked states, 250 successes and 13 finite-\(n\) failures**. In the boundary failure, after 99,941 null deletions and with 43 nulls left, the best truth-move gain was 8.23296376 versus 8.22400160 for the best null deletion. In the largest boundary success, the minimum deletion gain was 6.90780578, maximum addition gain -2.09966349, and minimum deletion-over-swap advantage 2.09966749.

Representative large-\(p\) margins: at \(n=10^8,p=10^5,\rho=.95\), seed 2026111000, the minimum chosen deletion gain was 8.3613494, maximum addition gain -8.3613494, and minimum chosen-deletion advantage over null-out swaps 8.6704367. At \(n=10^{300}\), the corresponding values were 344.5396176, -344.5396176, and 344.8486831.

## Disposition

Accept (C1)–(C4), including Corollary M, subject to the existing premises and F1's wording correction. No repaired probabilistic argument, stronger no-cancellation condition, narrower \(p\)-range, or altered cap is required. The stronger informal claim that *all* neighbour scores are monotone in absolute distance is false; the theorem's actual swap proof does not use it.

## Reproduction appendix

The following independent programs reproduce the principal falsification suites. They import no ticket modules. The first program checks dense algebra, end-phase coefficients, and masked starts. The second checks paths, including the \(p=n/2\) boundary. The extra 79-state dense-scanner validation and the explicit signed-swap counterexample are described above; their reported tolerances are not inferred from the fast path code.


### Program A: dense identities, end coefficients, masked starts

```python
import numpy as np, math, itertools, json
from scipy.special import gammaln
rng=np.random.default_rng(2026110903)
out={}; maxq=0.; maxg=0.; checks=0; data_cases=0
for n,rho,coeff in itertools.product([20,200,10**6],[.001,.3,.95,.9999],[[1.0],[1.4,-1.,1.8,-1.2]]):
 p=8; theta=np.zeros(p); theta[:len(coeff)]=coeff
 Sig=(1-rho)*np.eye(p)+rho*np.ones((p,p)); G=(n-1)*Sig
 g=np.linalg.cholesky(Sig)@rng.normal(size=p); chi=rng.chisquare(n-1-p)
 ss=(n-1)*(theta@Sig@theta)+2*math.sqrt(n-1)*(theta@g)+g@np.linalg.solve(Sig,g)+chi
 scale=math.sqrt(ss/(n-1)); z=((n-1)*(Sig@theta)+math.sqrt(n-1)*g)/scale
 al=(n*n-1)*(1-rho)+1; be=(n*n-1)*rho
 gam=lambda k: be/(al+k*be)
 nu=n/2+.01
 lw=lambda k: -math.log(2)-gammaln(2*p)+gammaln(k+1)+gammaln(2*p-k)
 dense=[]; qs=[]; lds=[]
 for mask in range(1<<p):
  ids=[j for j in range(p) if mask>>j&1]; k=len(ids)
  if k:
   H=(n+1)*G[np.ix_(ids,ids)]+np.eye(k); A=G[np.ix_(ids,ids)]+np.eye(k)
   q=float(z[ids]@np.linalg.solve(H,z[ids])); ld=np.linalg.slogdet(H)[1]-np.linalg.slogdet(A)[1]
  else:q=0.;ld=0.
  qc=(sum(z[j]**2 for j in ids)-gam(k)*sum(z[j] for j in ids)**2)/al
  maxq=max(maxq,abs(q-qc)); qs.append(q);lds.append(ld);dense.append(lw(k)-ld/2-nu*math.log(.02+n-1-n*q))
 for mask in range(1<<p):
  ins=[j for j in range(p) if mask>>j&1]; outside=[j for j in range(p) if not mask>>j&1];k=len(ins)
  B=sum(z[j] for j in ins); t=z-gam(k)*B; psi=.02+n-1-n*qs[mask]
  def verify(other, dq):
   global checks,maxg
   kk=other.bit_count()
   gain=lw(kk)-lw(k)-(lds[other]-lds[mask])/2-nu*math.log1p(-n*dq/psi)
   err=abs(gain-(dense[other]-dense[mask]))
   maxg=max(maxg,err); checks+=1
  for j in ins:verify(mask^(1<<j),-(1+gam(k-1))*t[j]**2/al)
  for l in outside:verify(mask^(1<<l),(1-gam(k+1))*t[l]**2/al)
  for j in ins:
   for l in outside:verify(mask^(1<<j)^(1<<l),(t[l]**2-t[j]**2-gam(k)*(t[l]-t[j])**2)/al)
 data_cases+=1
out["dense_algebra"]={"cases":data_cases,"neighbor_checks":checks,"max_quad_abs_error":maxq,"max_gain_abs_error":maxg}
# Constructed equal-distance swap obstruction in residual units:
n=100;rho=.5;k=2;gamma=1/(k+(1-rho)/rho+1/(rho*(n*n-1)))
tj=1.
out["swap_obstruction"]={"gamma":gamma,"tau_j":tj,"V_plus":1.5**2-tj**2-gamma*(1.5-tj)**2,"V_minus":(-1.5)**2-tj**2-gamma*(-1.5-tj)**2}
# Exact ideal-end coefficients: log p / log n = a in [.005,1], M=1/2.
bad=0;worst=1.;count=0
for s,rho,m in itertools.product([1,2,4,16],[1e-8,.001,.3,.7,.95,.99999999],range(1,251)):
 d=s+m+(1-rho)/rho
 for I in range(-m,m+1,2):
  ci=abs(I)/d
  if abs(I)>=2 and ci>.0400001:continue
  # H^2/log n=2a. deletion chooses majority; I=0 either side.
  cost=(d/(d-1))*(1-abs(I)/d)**2
  addcost=(d+abs(I))**2/(d*(d+1))
  for a in [.005,.2,.5,1.]:
   dele=.5+a-a*cost; add=-.5-a+a*addcost
   sw=4*a*max(abs(I)-1,0)/d
   cd=.5-1/(s+1+(1-rho)/rho)
   if dele<=0 or add>=0 or sw>=dele:bad+=1
   worst=min(worst,dele,-add,dele-sw);count+=1
out["ideal_end_grid"]={"checks":count,"violations":bad,"minimum_normalized_slack":worst}
# All-model start scores independent of production code; p=8, masked theta=(-rho,1).
start=[]
for rho,n,layout in itertools.product([.3,.5,.95],[10**4,10**8,10**12],["spread_null","oneblock","masked_singleton"]):
 p=8;theta=np.array([-rho,1.,0,0,0,0,0,0]);Sig=(1-rho)*np.eye(p)+rho*np.ones((p,p))
 eta=rng.normal();xi=rng.normal(size=p);g=math.sqrt(rho)*eta+math.sqrt(1-rho)*xi
 phi=(g@g-rho/(1-rho+p*rho)*sum(g)**2)/(1-rho)
 ss=(n-1)*(theta@Sig@theta)+2*math.sqrt(n-1)*(theta@g)+phi+rng.chisquare(n-1-p)
 z=((n-1)*(Sig@theta)+math.sqrt(n-1)*g)/math.sqrt(ss/(n-1))
 al=(n*n-1)*(1-rho)+1;be=(n*n-1)*rho;al2=(n-1)*(1-rho)+1;be2=(n-1)*rho;nu=n/2+.01
 blocks= [[0,2],[1],[3,4,5,6,7]] if layout=="spread_null" else ([[0,1,2],[3,4,5,6,7]] if layout=="oneblock" else [[0],[1],[2,3,4,5,6,7]])
 def lm(ids):
  k=len(ids)
  if not k:return -nu*math.log(.02+n-1)
  B=sum(z[ids]);A=sum(z[ids]**2)
  q=(A-be/(al+k*be)*B*B)/al
  ld=(k-1)*math.log(al/al2)+math.log((al+k*be)/(al2+k*be2))
  return -ld/2-nu*math.log(.02+n-1-n*q)
 vals=[]
 for mask in range(1<<p):
  k=mask.bit_count()
  vals.append(-math.log(2)-gammaln(2*p)+gammaln(k+1)+gammaln(2*p-k)+sum(lm([j for j in b if mask>>j&1])-lm([]) for b in blocks))
 best=int(np.argmax(vals));N0={j for b in blocks if {0,1}.issubset(b) for j in b if j>=2};star=sum(1<<j for j in range(p) if j not in N0)
 start.append({"rho":rho,"n":n,"layout":layout,"best_mask":best,"target_mask":star,"match":best==star,"unique":sum(v==max(vals) for v in vals)==1})
out["masked_start"]=start
print(json.dumps({"dense_algebra":out["dense_algebra"],"ideal_end_grid":out["ideal_end_grid"],"masked_ties":[r for r in start if not r["unique"]],"masked_success_count":sum(r["match"] and r["layout"]!="masked_singleton" for r in start)},indent=2))

```

### Program B: exact-gain path falsifier and boundary suite

```python
import numpy as np, math, bisect, itertools, json, time
class Audit:
 def __init__(self,n,p,rho,theta,seed,N0=0):
  self.n=n;self.p=p;self.rho=rho;self.th=np.array(theta);self.s0=len(theta);self.N0=N0
  rng=np.random.default_rng(seed);xi=rng.normal(size=p);self.tx=xi[:self.s0]
  self.zero=xi[self.s0:self.s0+N0]
  self.val=np.sort(xi[self.s0+N0:]);self.eta=float(rng.normal());self.inv=1/n;self.v=1-rho
  kap0=self.v/rho;self.kap=kap0+(self.inv*self.inv)/(rho*(1-self.inv*self.inv))
  self.off=math.sqrt(rho/self.v)*self.kap*self.eta+math.sqrt(n-1)*sum(theta)/(math.sqrt(self.v)*(n-1)*(n+1))
  g=math.sqrt(rho)*self.eta+math.sqrt(self.v)*xi
  phif=(g@g-rho/(self.v+p*rho)*float(sum(g))**2)/self.v
  self.e2=phif+rng.chisquare(n-1-p)
  self.energy=self.v*float(self.th@self.th)+rho*float(sum(self.th))**2
  self.tg=float(self.th@g[:self.s0]);self.txi=float(self.th@self.tx)
  self.ss=self.energy+2*self.tg/math.sqrt(n-1)+self.e2/(n-1)
  self.ts=float(sum(self.tx));self.tq=float(self.tx@self.tx)
  self.sum=float(sum(self.val));self.sq=float(self.val@self.val)
  self.lo=0;self.hi=0;self.m=len(self.val);self.m0=self.m
 def ldinc(self,k):
  n,p,rho=self.n,self.p,self.rho;v=1-rho
  base=math.log1p(-(n/(n+1))/((n-1)*v+1))
  def common(u):return math.log1p(-(n/(n+1))/((n-1)*(v+u*rho)+1))
  return math.log(n+1)+common(1) if k==1 else math.log(n+1)+base+common(k)-common(k-1)
 def delta(self,k):return math.log((2*self.p-k)/k)+.5*self.ldinc(k)
 def nearest(self,target):
  ids=[]
  for a,b in [(0,self.lo),(self.hi,self.m0)]:
   if a>=b:continue
   h=int(np.searchsorted(self.val,target,side='left'))
   ids.extend([max(a,min(b-1,h)),max(a,min(b-1,h-1))])
  return min(set(ids),key=lambda j:abs(self.val[j]-target)) if ids else None
 def step(self,brute=False):
  n,rho=self.n,self.rho;v=self.v;k=self.s0+self.m;d=k+self.kap;gam=1/d
  sx=self.ts+self.sum;sxx=self.tq+self.sq
  x=(sx-self.off)/d
  # Exact Q via RSS + diagonal/common ridge corrections, without subtracting O(n) response scores.
  ag=math.sqrt(rho/v)*self.eta
  ph=(sxx+2*ag*sx+k*ag*ag-(sx+k*ag)**2/(k+v/rho))
  rss=self.e2-ph
  tb=float(sum(self.th));tt=float(self.th@self.th)
  hdev=((n-1)*v*(tt-tb*tb/k)+2*math.sqrt((n-1)*v)*(self.txi-tb*sx/k)+sxx-sx*sx/k)/self.ss
  zmean=(math.sqrt(n-1)*(rho*tb+v*tb/k)+math.sqrt(rho)*self.eta+math.sqrt(v)*sx/k)/math.sqrt(self.ss)
  hcommon=k*zmean*zmean/(v+k*rho)
  ga=(n-1)*v;gc=(n-1)*(v+k*rho)
  ridge=hdev*(1+1/ga)/(n+1+1/ga)+hcommon*(1+1/gc)/(n+1+1/gc)
  psi=(rss/self.ss+ridge+.02)
  factor=(n/(n+1))/(1+(self.inv*self.inv)/((1-self.inv*self.inv)*v))
  nu=n/2+.01
  M=(nu/n)*factor/(self.ss*(psi/n))
  def gd(t):return self.delta(k)-nu*math.log1p((1+1/(d-1))*M*t*t/nu)
  def gad(t):return -self.delta(k+1)-nu*math.log1p(-(1-1/(d+1))*M*t*t/nu)
  def gs(tj,tl):
   V=tl*tl-tj*tj-gam*(tl-tj)**2
   return -nu*math.log1p(-M*V/nu)
  j=self.nearest(x);bestdel=gd(self.val[j]-x) if j is not None else -math.inf
  out=list(self.zero)
  if self.hi>self.lo:out.extend([float(self.val[self.lo]),float(self.val[self.hi-1])])
  ext=[min(out)-x,max(out)-x] if out else []
  add=max([gad(t) for t in ext],default=-math.inf) if k<self.p else -math.inf
  truth=self.tx-x+math.sqrt((n-1)*v)*self.th
  tr=max([gd(float(t)) for t in truth])
  sw=-math.inf
  for tl in ext:
   q=self.nearest(x+gam/(1+gam)*tl)
   if q is not None:sw=max(sw,gs(self.val[q]-x,tl))
   tr=max(tr,max(gs(float(t),tl) for t in truth))
  if brute:
   ids=list(range(self.lo))+list(range(self.hi,self.m0))
   allouts=list(self.zero)+list(self.val[self.lo:self.hi])
   bd=max([gd(self.val[q]-x) for q in ids],default=-math.inf)
   ba=max([gad(float(u-x)) for u in allouts],default=-math.inf) if k<self.p else -math.inf
   bs=max([gs(self.val[q]-x,float(u-x)) for q in ids for u in allouts],default=-math.inf)
   for a,b in [(bd,bestdel),(ba,add),(bs,sw)]:
    assert a==b or abs(a-b)<1e-9,(a,b)
  if self.m:
   ok=bestdel>max(0.,add,sw,tr)
   if not ok:return False,dict(m=self.m,x=x,deletion=bestdel,addition=add,swap=sw,truth=tr)
   if self.lo==self.hi:self.lo=j;self.hi=j+1
   elif j==self.lo-1:self.lo-=1
   elif j==self.hi:self.hi+=1
   else:raise AssertionError("gap failed")
   zz=float(self.val[j]);self.sum-=zz;self.sq-=zz*zz;self.m-=1
   return True,dict(deletion=bestdel,addition=add,swap_gap=bestdel-sw)
  return add<0 and tr<0,dict(addition=add,truth=tr)
def run(n,p,rho,coeff,seed,N0=0):
 a=Audit(n,p,rho,coeff,seed,N0)
 min_del=math.inf;maxadd=-math.inf;mingap=math.inf
 for i in range(a.m0+1):
  ok,info=a.step(brute=p<=20)
  if not ok:return dict(n=n,p=p,rho=rho,coeff=coeff,seed=seed,N0=N0,ok=False,at=i,info=info)
  if i<a.m0:
   min_del=min(min_del,info["deletion"]);mingap=min(mingap,info["swap_gap"])
  maxadd=max(maxadd,info["addition"])
 return dict(n=n,p=p,rho=rho,coeff=coeff,seed=seed,N0=N0,ok=True,moves=a.m0,min_del=min_del,max_add=maxadd,min_del_swap_gap=mingap)
t=time.time();rows=[];states=0
for n,p,rho,s,rep in itertools.product([1e4,1e8,1e12,1e100,1e300],[12,512,2000],[.001,.3,.95,.9999],[1,4],range(2)):
 coeff=[1.] if s==1 else [1.4,-1,1.8,-1.2]
 r=run(n,p,rho,coeff,2026110900+rep,N0=3 if s==1 else 0);rows.append(r);states+=r.get("moves",r.get("at",0))+1
for n,rho,rep in itertools.product([1e8,1e300],[.3,.95],[0,1]):
 r=run(n,100000,rho,[1.],2026111000+rep);rows.append(r);states+=r.get("moves",r.get("at",0))+1
for rho in [.3,.5,.95]:
 for n in [1e8,1e300]:
  r=run(n,2000,rho,[-rho,1.],2026111122,N0=1);rows.append(r);states+=r.get("moves",r.get("at",0))+1
fails=[r for r in rows if not r["ok"]]
summary={"cases":len(rows),"states":states,"successes":len(rows)-len(fails),"failures":fails,"seconds":time.time()-t,"n_ge_1e8_failures":sum(not r["ok"] and r["n"]>=1e8 for r in rows),"large_p":[r for r in rows if r["p"]==100000]}
summary["failures"]=[{key:r[key] for key in ["n","p","rho","coeff","seed","N0","at"]} for r in fails]
print(json.dumps(summary,indent=2))

# Additional p=n/2 suite, using the same independent scanner.
t=time.time();rows=[]
for rho,s in itertools.product([.001,.3,.95,.9999],[1,4]):
 rows.append(run(200000,100000,rho,[1.] if s==1 else [1.4,-1,1.8,-1.2],2026112000,15 if s==1 else 0))
rows.append(run(1000000,500000,.95,[1.],2026112001,15))
print(json.dumps({"cases":len(rows),"successes":sum(r["ok"] for r in rows),"rows":rows,"seconds":time.time()-t},indent=2))

```


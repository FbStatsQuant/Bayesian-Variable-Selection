# T21: Composition theorem for the reported HPM

Scope: (C1) and discovery routes (a)-(f) of T21_T14H_HPM_composition.md. This is a conditional composition theorem, not a proof of T03, T10, or T24. Method: SMC-BVS v3.0, with the user's Decision Point 2 corrections. Only the primary PIP is an output considered here. All statements below concern the exact-score idealisation.

## 1. Objects and probability laws

For integers n >= 3 and p >= 1, take the method's standardised data X,y (centred columns and response, squared norms n-1). Put K=min(p,floor(n/2)) and Omega={S subset of [p]: |S|<=K}. The true support S0 belongs to Omega. For asymptotic statements this is required eventually. Write s0=|S0|. The finite-sample statements apply to any law P0 of the data; P is the joint law of data and algorithm randomness, with data marginal P0. E0 and E denote the corresponding expectations.

For S in Omega, let G_S=X_S'X_S, z_S=X_S'y, H_S=(n+1)G_S+I, D_S=det(H_S)/det(G_S+I), Q_S=y'y-n z_S'H_S^{-1}z_S, a0=b0=0.01, nu=a0+n/2, and

    m(S)=(2b0)^a0 Gamma(nu)/(pi^(n/2) Gamma(a0)) D_S^(-1/2) (2b0+Q_S)^(-nu).

Empty matrices give D_empty=1 and Q_empty=y'y. Let w(k)=1/[2 binom(2p-1,k)], W_K=sum_{k=0}^K binom(p,k)w(k), varpi(S)=w(|S|)/W_K, F(S)=log(varpi(S)m(S)), Z=sum_Omega exp(F(S)), pi(S)=exp(F(S))/Z, delta1=1-pi(S0). A larger F is preferred; exactly equal scores are ordered by smaller size, then lexicographically smaller sorted index list. Sdagger is the unique model selected by this total order on Omega.

The cumulative scored set Sscr contains every model scored in tables, pilot, diagnostics, final initialisations, Gibbs evaluations under SR, accepted and rejected proposals, and local scans. Scores retained for the HPM are never lost through cache eviction. Scal is the subset scored before final randomness (including the tables); Sscr contains Scal. U is the event that no usable HPM output is produced. On U^c, Shat is the total-order maximum of the nonempty Sscr. Expressions 'U or Shat != S0' mean U union {U^c, Shat != S0}, so no output is needed on U.

The method's deterministic block partition C_1,...,C_J has sizes at most B=min(floor(sqrt(n)),floor(sqrt(p)),16). Tables r_b(A)=m(A)/m(empty), for every A subset of C_b, use the full response. Set gamma0(S)=varpi(S) product_b r_b(S intersect C_b), Zbar0=sum_Omega gamma0(S), pi0=gamma0/Zbar0. On the exact branch these component objects may be defined mathematically without being constructed by the algorithm.

Budgets: N0=max(2500,n,p), H0=ceil(512N0/2500), ell=ceil(log2(n+p+1)), T0=max(1000,ell^2), (N_e,H_e,T_e)=4^e(N0,H0,T0), e in {0,1}, L=max(4,ceil(log2(n+1))). Let Fcal be the event that calibration permits the prescribed final SMC run. It is false on the exact branch. Conditional on data and all pre-final information, Fcal, the tier and grid 0=phi_0<...<phi_T=1 are fixed; on Fcal, 1<=T<=T_e. There are four final islands, each with N_e fresh pi0 initial draws and T+L+4 rounds per particle, with one fresh pi0 independence proposal per round. All these models are scored, irrespective of proposal acceptance. Thus Q_f=4N_e(T+L+5) on Fcal; off Fcal set Q_f=0 for formulas containing its indicator.

At an elementary Gibbs execution of coordinate j, X_pre-j is the state just before that execution. SR means both feasible configurations given X_pre-j minus {j} are evaluated and counted as scored. A uniform swap at S with 1<=|S|=k<p draws j uniformly in S and l uniformly in [p] minus S. A neighbour swap draws j uniformly in S, then l uniformly in N(j) minus S when that set is nonempty, using the method's actual symmetric-union graph. Every swap proposal is scored before its accept/reject decision. Local scans evaluate every feasible one-variable addition, deletion and same-size swap of their frozen centre, including the last scan at the move cap.

## 2. Hypotheses and dependency boundary

EX-A: scores, probabilities, convolutions and comparisons are exact. EX-S for random routes: fresh ideal independent uniforms, independent of the data, with all choices based on the available past. CAL for final-run formulas: streams 0-9 determine calibration and streams 10-13 are fresh. Operations are measurable. Operational execution is explicit: a launched final run used in (a) executes and scores all Q_f designated draws; scans used in (d) are completed; rounds used in (e) execute. There is no conditioning on future completion or on passing final diagnostics. Environmental aborts after launch are outside this full-execution idealisation; the formulas are not asserted for a truncated draw count. U remains explicit in C1, and consistency additionally needs P(U)->0. A schedule failure need not belong to U if the best already-scored HPM is usable.

The following are *hypotheses*, never cited as proved results:

- **H03 (T03 posterior concentration conclusion):** along a sequence n->infinity, delta1=O_{P0}(sqrt(log n/n)). It implies delta1->0 in probability. The proposed derivation under G, R, SE, BM-C is not assumed proved. T21 does not derive H03 from those conditions.
- **H10 (T10 addition conclusion, used only for (a)'s one-deletion corollary):** for each required feasible addition S+j, pi0(S+j)>=r_k pi0(S), where k=|S|<K and r_k=(k+1)/[(2p-k-1)sqrt(n+1)]. It suffices to assume this for S=S0 minus {i}.
- **H24 (T24 terminal repair inputs, used only in (e)):** fix d>=1, s0+d<=K, and R_d={U0 union P0extra: U0 subset of S0, P0extra subset of [p] minus S0, |P0extra|<=d}. For the actual terminal round kernel K1, there are data-measurable a_n,eta_n in [0,1] such that, uniformly for x in R_d,

      K1(x,{S0})>=a_n,
      P_x(first exit from R_d during the round)<=eta_n.

  They hold uniformly before a particle is selected. These are the inputs in T24(i); they are assumed here, not proved from LK_d, EXIT_d, GAIN_d, or T03. If using T24's proposed values, let Lambda=max_{x in R_d} sum_{l not in S0 union x} o_l(x,1), where o_l is the exact Gibbs inclusion probability; xi is a uniform upper bound on the one-round probability of a first exit caused by a non-Gibbs label; gplus is the infimum, over states missing truth in R_d, of the best missing-true addition log-score gain; gminus is the infimum, over proper truth supersets in R_d, of the best extra-variable deletion log-score gain (empty infima are +infinity); g=min(gplus,gminus). Put D_rep=2^(s0+d), c_n=1/(s0+d+B+2)!, rho_star=min(1,(B+3)delta1/pi(S0)), a_n=[c_n{1-(s0+d)exp(-g)}-D_rep Lambda-rho_star]_+, eta_n=min(1,(B+3)D_rep Lambda+xi). Assuming these formulas does not establish the two uniform bounds: those bounds are still H24. For the asymptotic repair claim also assume the T24 conclusions a_n>=c_n/2 with probability tending to one and (L+4)eta_n->0 in probability, with s0,d fixed. These are explicit additional conditional inputs.

The wave-1 results available as proved, not adopted, are T11(iii) (iid final draws), T20(ii) (completed neighbour scans), and T09(i) (exact start convolution/sampling). Their precise content used here is restated in the proof. Other ledger facts required below are proved directly from the specified algorithm; no other v3 conjecture is silently invoked. EXP' and cluster separation are not used: no no-switch or block-likelihood expansion conclusion is claimed.

## 3. Conclusions

**(C1)** For every such n and data law,

    P(U or Shat != S0) <= P(U) + 2 E0 delta1 + P(U^c, S0 not in Sscr).

Under H03 the middle term tends to zero. If P(U)->0 and any applicable discovery bound below tends to zero, recovery probability tends to one. The finite bounds, and not merely the name of a route, specify the needed occurrence/exposure conditions.

**(a) Fresh iid draws.** Under EX-S, CAL and full operational execution,

    P(S0 not in Sscr)
    <= P(Fcal^c, S0 not in Scal)
       + E[1_Fcal 1_{S0 not in Scal} (1-pi0(S0))^Q_f].

The second term is at most E[1_Fcal 1_{S0 not in Scal} exp(-Q_f pi0(S0))]. If the first term vanishes and, for every finite M, P(Fcal, Q_f pi0(S0)<=M)->0, then discovery failure tends to zero. This is the precise meaning of intensity diverging 'on launched runs'; conditional divergence given Fcal, when defined, is sufficient as well.

If s0>=1 is fixed, i in S0, and Stilde0=S0 minus {i} has pi0(Stilde0)>=c>0 (Stilde0 need not be the start mode), H10 gives pi0(S0)>=c r_{s0-1} and

    Q_f pi0(S0) >= 4 c s0 N_e(T+L+5)/[(2p-s0)sqrt(n+1)].

This guaranteed lower-bound intensity has scale N_e(T+L+5)/(p sqrt(n)) for fixed s0,c. Under actual budgets it diverges whenever p<=C sqrt(n) for a fixed C, including the boundary because L grows logarithmically. If the start-mass event holds only with probability tending to one, add its failure probability. This is a sufficient range, not a necessary range: this lower bound supplies no proof of failure above it. No two-sided law from the unproved T27 is used.

**(b) Gibbs execution.** If, before discovery, an actual Gibbs execution satisfies X_pre-j minus {j}=S0 minus {j}, SR scores S0. Let E_G be the event that such an execution occurs before discovery. Then {S0 not in Sscr} is contained in E_G^c. Thus P(U^c,E_G^c)->0 is sufficient for the discovery term in C1. Occupancy of a round-start state alone is not the execution-time condition.

**(c) Swap execution.** A size-k proxy is S=(S0 minus {l}) union {j}, where l in S0, j not in S0, and 1<=k=s0<p. At each actual uniform-swap execution in such a proxy before the first truth score, the conditional probability of proposing and scoring S0 is b=1/[k(p-k)]. Let O be the number of these actual opportunities before discovery or the end of the run. For deterministic integer D>=0 and delta>=0,

    P(S0 not in Sscr, O<D)<=delta
    implies P(S0 not in Sscr)<=delta+(1-b)^D.

Use (1-b)^0=1, including b=1. The same statement may be conditioned on data or pre-run information, with D fixed under that conditioning. No independence of opportunities, or conditioning on their future count, is required. PX means such exposure is sufficiently large: for some omega_n->infinity, P(S0 not in Sscr, O<ceil(omega_n k(p-k)))->0. It yields discovery. ONE (a start-mode flip or same-block proxy relation) alone specifies no such count and is not substituted for PX.

For a neighbour swap at that proxy the probability is 1/[k|N(j) minus S|] if the actual required edge l in N(j) is present, and zero if absent. A deterministic lower bound b_* in (0,1], valid at every counted neighbour-swap opportunity before discovery, can replace b. A random b_* may be used in the conditional version when it is measurable with respect to the information conditioned on and bounds every subsequent counted opportunity. Unconditional averaging then requires the corresponding expectation of (1-b_*)^D. A same-block description alone does not replace the actual edge condition.

**(d) Tables and scans.** If S0 is contained in some C_b and that table is constructed, S0 is table-scored. If a completed local scan has a feasible flip-or-swap neighbour of S0 as its centre, it scores S0, whether or not any move budget remains. Let E_TS be the event that at least one such table construction or completed scan occurs. Then P(U^c,S0 not in Sscr)<=P(U^c,E_TS^c); vanishing of the latter suffices. No schedule-success assumption is needed if tables or calibration already supply the score.

**(e) Terminal repair.** Under H24 and SR, select an eligible particle (state in R_d) using only the available past at a terminal-round boundary. Future randomness for that particle is fresh and its next H rounds, at temperature one and without intervening resampling, execute; H>=0 is fixed given the selection past. Conditional on that past and the data, on eligibility, let M_H be the event that S0 not in Sscr when those H rounds end. Then

    P(M_H | available past) <= (1-a_n)^H+H eta_n.

For an availability event A measurable at selection, the unconditional failure bound is P(A^c)+E[1_A min{1,(1-a_n)^H+H eta_n}]. The truth already being scored only improves the bound. For final-run repair put A_F=Fcal intersect {an eligible particle is available at the chosen terminal boundary}; then a sharper whole-run bound is

    P(S0 not in Sscr) <= P(Fcal^c,S0 not in Scal)
       + P(Fcal, no eligible particle at that boundary)
       + E[1_{A_F} min{1,(1-a_n)^H+H eta_n}].

Thus the nonlaunch term is retained. Pilot repair uses its forward filtration at the selection boundary, never conditioning on the subsequently constructed grid or final calibration record. With H=L+4, fixed s0,d, H24's asymptotic inputs and vanishing availability/nonlaunch terms imply discovery. For arbitrary H the sufficient repair condition is Ha_n->infinity and H eta_n->0 in probability on availability. These are HPM scoring guarantees, not PIP accuracy guarantees.

**(f) Exact branch.** If sum_{k=0}^K binom(p,k)<=(5H0+4N0)p and the exact enumeration completes under EX-A, Sscr=Omega, Shat=Sdagger, and the evidence and primary PIPs are the exact finite sums Z and sum_{S:j in S} exp(F(S))/Z. Every fixed p eventually satisfies this branch inequality as n->infinity. Actual completion remains a separate operational requirement; truth recovery additionally uses H03 through C1.

## 4. Formalisation record

The replacement of unproved T03/T10/T24 by H03/H10/H24 is explicitly required by the user. The remaining clarifications expose the source's operational availability and execution conditions, make conditional probability and asymptotic quantifiers explicit, and distinguish scoring from visitation/occupancy. No algorithm, prior, budget, or claimed finite bound is changed. The neighbour-swap extension uses a fixed deterministic lower bound for unconditional numerical inequalities; random bounds require conditioning and averaging.



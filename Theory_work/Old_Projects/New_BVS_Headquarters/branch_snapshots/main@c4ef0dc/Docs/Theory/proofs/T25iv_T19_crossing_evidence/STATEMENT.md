# T25(iv): conditional variance under PW2

## Scope and source

Only part (iv) of `theorems/T25_T19_crossing_evidence.md` is in scope. The statement is conditional on PW2. No assertion establishing PW2, and no other part of T25, is included in this deliverable.

Source conclusion: if the actual particle system satisfies

E_C[W_{t-1}^2 { (qhat_{t-1} g_t)^2 - 1 }]
<= (a_t/N_e) E_C W_{t-1}^2 + nu_t,

then

Var_C(W_T) <= product_{t=1}^T (1+a_t/N_e) - 1
+ sum_{s=1}^T nu_s product_{t=s+1}^T (1+a_t/N_e),

divided by four under island pooling.

## Definitions and quantifiers

Fix any valid data input for the SMC branch of SMC-BVS v3.0 and any successful frozen calibration value c. All probabilities below are over fresh final-run randomness, with the data and c fixed. Equivalently the conclusions hold almost surely given the calibration C on its success event. We do not condition further on final flags or on a subset of final particle outcomes. Completed final runs means execution of the prescribed finite ideal run under EX-A, EX-S and CAL, not selection by a later random diagnostic.

The finite state space is Omega = {S subset of [p]: |S| <= K}, K=min(p,floor(n/2)). The method's exact marginal likelihood m(S) and capped prior varpi(S) are strictly positive and finite on Omega. The fixed blocks C_b partition [p]; r_b(U)=m(U)/m(empty). Set

- gamma_0(S)=varpi(S) product_b r_b(S intersect C_b);
- d(S)=log[m(S)/m(empty)]-sum_b log r_b(S intersect C_b);
- gamma_phi(S)=gamma_0(S) exp(phi d(S)); Zbar_phi=sum_Omega gamma_phi(S); q_phi=gamma_phi/Zbar_phi;
- 0=phi_0<...<phi_T=1 is the frozen finite grid; T>=1;
- q_t=q_{phi_t}, Z_t=m(empty) Zbar_{phi_t}, so Z_T=Z=sum_Omega varpi(S)m(S);
- G_t(S)=exp[(phi_t-phi_{t-1})d(S)], c_t=Z_t/Z_{t-1}=q_{t-1}(G_t), and g_t=G_t/c_t. In particular q_{t-1}(g_t)=1.

N=N_e is the frozen positive integer particle count **per island**. In one island the initial N particles are iid q_0, Zhat_0=Z_0 exactly, and qhat_0 is their empirical probability measure. At stage t, compute

Zhat_t=Zhat_{t-1} qhat_{t-1}(G_t),

then resample N ancestors independently with probabilities proportional to G_t, and independently mutate each resampled particle by the method's q_t-invariant round kernel K_t=K_{phi_t}. qhat_t is the empirical probability measure after this resampling and mutation. The round consists of the p Gibbs labels, one uniform swap, B neighbour swaps, and one independence proposal, in a fresh uniformly random order for each particle. All steps use their exact probabilities. The terminal burn-in, measured rounds and local search do not alter Zhat_T.

Define W_t=Zhat_t/Z_t for a single island, with W_0=1. The symbol W_t is a scalar evidence ratio, not a working set. E_c and Var_c denote the conditional expectation and variance just specified.

EX-A means exact scores, normalisers, probabilities and comparisons. EX-S means independent ideal random streams and fresh independent randomness for the stated sampling operations. CAL means that all final-run settings use calibration streams 0--9 only; the four final islands use independent fresh streams 10--13. They are thus independent copies conditional on c. The exact start and the q_t-invariance of the prescribed kernels are established properties of the method; in particular they are the setting of proved wave-1 T12.

## PW2 hypothesis and conclusion

Let a_t and nu_t, 1<=t<=T, be finite nonnegative upper-bound constants, fixed given c (they may depend on the data, calibration and N). This spells out the rate-coefficient/slack convention in PW2. Assume PW2 for every t:

E_c[W_{t-1}^2 { (qhat_{t-1}(g_t))^2 - 1 }]
<= (a_t/N) E_c[W_{t-1}^2] + nu_t.

Then, with an empty product equal to 1,

B_T := product_{t=1}^T (1+a_t/N) - 1
+ sum_{s=1}^T nu_s product_{t=s+1}^T (1+a_t/N)

satisfies Var_c(W_T) <= B_T.

For four final islands r=1,...,4, let W_{r,T}=Zhat_{r,T}/Z and W_pool=(1/4)sum_r W_{r,T}=Zhat/Z. When PW2 holds with the same bounds for each island, Var_c(W_pool) <= B_T/4. This divides the **whole** bound, including the slack sum, by four; N remains N_e, not 4N_e.

The constants need not be uniform over calibrations for this conditional statement. No RET, OCC, COVER, BW2, or BW_W premise is used to establish PW2 here. No statement about measured constants is a hypothesis of the theorem.

## Dependencies and statement history

Wave-1 T12(i.a), (iii), and (iv.c), as reproduced in `proofs/COLLECTED/COLLECTED_PROOFS_v2.tex`, give stagewise unbiasedness and conditional independence of the final islands. They may be cited as proved, not adopted. The proof also supplies the short first-moment induction, so its variance argument is self-contained. No unproved v3 conjecture is used as a result.

No mathematical change to T25(iv). The notation, the nonnegative upper-bound constants, the conditioning, and the meaning of pooling are made explicit. No assumption intended to imply PW2 has been added.

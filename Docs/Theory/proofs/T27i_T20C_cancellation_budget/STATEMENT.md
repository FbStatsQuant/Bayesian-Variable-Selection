# T27(i): sequential cancellation mass law

Scope: part (i) only. The conclusion is conditional on the premises below. No discovery-budget, mixing, or other-part conclusion is included. The statistical premises remain open inputs.

## Definitions

Let n tend to infinity, n>=3, p=p_n>=1 integer, with d_- n^a <= p_n <= d_+ n^a eventually for fixed a>=0 and 0<d_-<=d_+<infinity. P_0 is the data law, with project notation y^r=alpha* 1+X^r beta*+epsilon and S_0=supp(beta*). All stochastic orders and probability limits below are unconditional under P_0. No distributional restriction beyond the explicit stochastic premises is required by this implication.

Retained raw columns and raw response are nonconstant. Center and divide them by their sample standard deviations (denominator n-1), giving X,y with squared column and response norms n-1. K=min(p,floor(n/2)); Omega={S subset [p]: |S|<=K}. The actual method partition C_1,...,C_J is obtained from X alone by complete linkage on 1-|x_j' x_l|/(n-1), with lexicographic merge ties, top-down splitting (smallest-index child first) until clusters have size at most B=min(floor(sqrt(n)),floor(sqrt(p)),16), then next-fit packing of whole clusters in dendrogram leaf order.

For a table set U subset C_b, let G_U=X_U'X_U, z_U=X_U'y, H_U=(n+1)G_U+I, D_U=det(H_U)/det(G_U+I), Q_U=y'y-n z_U'H_U^{-1}z_U, nu=0.01+n/2, and

    C_n=(0.02)^0.01 Gamma(nu)/(pi^(n/2) Gamma(0.01)),
    m(U)=C_n D_U^(-1/2) (0.02+Q_U)^(-nu),
    r_b(U)=m(U)/m(empty).

Empty determinants are one and empty quadratic forms zero. Scores and tables are finite and positive. The capped BB(1,p) prior and composite start are

    w(k)=1/[2 binom(2p-1,k)],
    W_K=sum_{k=0}^K binom(p,k)w(k),
    gamma_0(S)=[w(|S|)/W_K] product_b r_b(S intersect C_b), S in Omega,
    Zbar_0=sum_{S in Omega}gamma_0(S),  pi_0(S)=gamma_0(S)/Zbar_0.

On the exact-enumeration branch the algorithm builds no blocks; pi_0 is then the analytically defined component law given by these formulas, not an actual sampling stage. This interpretation applies eventually to bounded p (a=0).

## Every premise

H1. **Fixed feasible completion chain.** Fix integers s>=0 and c>=1. There is a specified data-measurable chain S^(0) subset ... subset S^(c)=S_0 with |S^(0)|=s and S^(i+1)=S^(i) union {l_i}, l_i not in S^(i), for i=0,...,c-1. Every state is feasible and |S_0|=s+c<=K eventually. Deterministic chains are included. Let b_i be the block of l_i and T_i=S^(i) intersect C_{b_i}.

H2. **Joint sequential ratio law, assumed statistical input.** For this specified chain,

    E_{n,i}=log[r_{b_i}(T_i union {l_i})/r_{b_i}(T_i)]+(1/2)log n,
    max_{0<=i<c}|E_{n,i}|=O_{P_0}(1).

This is two-sided log tightness jointly at the successive states. A data-selected chain must itself satisfy this premise; no uniform guarantee over all selection rules is asserted. The remainders need not be independent. Cancellation at an initial table state alone does not assert H2.

H3. **Normalized reference-mass lower bound, assumed statistical input.** A deterministic constant c_0 in (0,1] satisfies P_0{pi_0(S^(0))>=c_0}->1. This premise includes the full capped composite normalizer. A lower bound on an unnormalized table product does not replace it.

H4. **Retained operational assumptions.** EX-A: exact scores, convolutions, probabilities, comparisons. EX-S: independent ideal uniform streams with the method's stream separation. CAL: calibration uses streams 0-9 only, final streams 10-13 are fresh and independent of calibration, and escalation precedes final randomness. Successful final execution: the final run completes its frozen schedule. These are retained as the theorem file's operational setting; the mass implication uses the exact start definition and H1-H3 and is independent of final-run randomness. No probability-of-completion assertion is added. In particular no stochastic-order statement conditioned on completion or diagnostics is claimed.

The scaling p asymptotic to n^a is retained, although the mass implication itself only needs p>=s+c and fixed s,c. G/R, Gaussianity, eigenvalue or beta-min assumptions are not silently used to derive H2 or H3.

## Exact conclusion

    log pi_0(S_0)+c log p+(c/2)log n=O_{P_0}(1),

equivalently pi_0(S_0)=p^(-c)n^(-c/2)exp{O_{P_0}(1)}. Here O_{P_0}(1) means tightness: for each epsilon>0 a finite M and N exist such that P_0{|Z_n|>M}<epsilon for n>=N. The positive mass multiplier and its reciprocal are both tight.

**Empty-chain extension:** if c=0, S^(0)=S_0, H2 is vacuous (empty maximum zero), and the conclusion is log pi_0(S_0)=O_{P_0}(1), with empty products one and empty sums zero.

## EXP-prime scope, not an extra premise of the mass theorem

Whenever a score expansion is discussed, use Decision Point 2's EXP' only. Let F_n be a specified family of actual-block comparisons (T,l), T subset C_b and l in C_b\T, containing every selected (T_i,l_i). Let P_T be the orthogonal projection onto span(X_T), v=(I-P_T)x_l and e=(I-P_T)y. In this optional discussion require nonzero v,e and partial R-squared x_{T,l}=(v'e)^2/(||v||^2||e||^2) in [0,1). The optional EXP' hypothesis is

    log[r_b(T union {l})/r_b(T)]
      = -(1/2)log(n+1)-nu log(1-x_{T,l})+R_{n,T,l},
    sup_{(T,l) in F_n}|R_{n,T,l}|=O_{P_0}(1).

Under that hypothesis, H2 is equivalent to max_i[-nu log(1-x_{T_i,l_i})]=O_{P_0}(1), equivalently max_i n x_{T_i,l_i}=O_{P_0}(1). This does not follow merely from max_i n x_{T_i,l_i}^2=O_{P_0}(1), which only controls the Taylor remainder when replacing -nu log(1-x) by nu x. Neither a Gaussian quadratic-score identity nor transfer from NL_eta on a leakage family to a missing-true-coordinate chain is assumed. EXP' itself is not proved here and is not needed when H2 is assumed directly.

## Sources, qualifications, and approved clarifications

Definitions are from METHODOLOGY_v3.md sections 4-6.3 and 00_COMMON.md. The source assertion is T27_T20C_cancellation_budget.md part (i). Wave-1 T22(ii-a), in COLLECTED_PROOFS_v2.tex, is available for the exact reference-to-truth odds; the proof also derives that identity directly. No other unproved v3 conjecture is used. If wave-1 T22(i) is used in a future application to discharge H3, its lower bound must exceed a fixed positive constant with probability tending to one; q_n<1 alone is insufficient.

Clarifications approved by a separate Astra xhigh statement checker on 2026-10-22: explicit joint two-sided remainder, selected-chain quantifiers, normalized mass premise, unconditional P_0 interpretation, exact-branch component interpretation, empty-chain extension, and the optional EXP' scope/equivalence above. The mass conclusion and substantive premises are unchanged. EXP is not a premise of this part; EXP' is the only expansion discussed. No theorem or method source was edited. The approval concerns statement fidelity, not verification of this proof or its statistical premises.

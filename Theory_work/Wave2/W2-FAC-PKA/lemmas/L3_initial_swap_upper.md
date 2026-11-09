# L3: sublinear upper bound for the initial swap phase (singleton subclass)

Status: PROVED (by this seat, unchecked). Same fixed singleton setting as L2, no new statistical hypotheses. This does NOT prove a doubled cap suffices: swaps/additions after the first deletion are not controlled here.

Inputs: L2 start law and exact score formulas, lemma check R04 VERIFIED-WITH-AMENDMENTS with amendments applied (reviews/R04_L2_claude.md, R04_disposition.md); independent midpoint R05 CONTINUE. We re-establish all longer-path bounds below; L2's O(log n) family bound is not extrapolated without proof.

Claim: let W_n be the number of consecutive initial null-null swaps before the first other move. With eta0=(1-c)/80, P(the first non-swap is a null deletion and W_n<=n^(1-eta0))->1. In particular W_n=o_P(n), whereas L2 implies W_n/log n->infinity in probability. Constants here are deliberately loose. Nothing is claimed uniformly as c approaches 1 with n.

## 1. Family and residual bounds

Set H=ceil(n^(1-eta0)). On the L2 high-probability start event T0 has size K and all truth; x_T0->mu and its nulls form the upper order-statistic fraction. Use the maximum-coordinate event max|xi_j|<=2sqrt(log n). For EVERY T formed from T0 by at most H null swaps, the change of sum xi is at most 4H sqrt(log n), so sup_T|x_T-x_T0|<=C H sqrt(log n)/n=o(1). All T have size K and contain truth. Fix delta as in L2, so the initial set has at least epsilon*n nulls in [mu-delta,mu+delta], with fixed epsilon>0. Since H=o(n), every family member has a retained null j with |xi_j-x_T|<=1 eventually. Put B=|mu|+2; then |x_T|<=B eventually throughout this family.

Unlike the general p=n-1 saturation lemma, here c<1 is fixed. The residual r=||(C-P_X)e||^2 has n-1-p degrees of freedom, so P(r>=(1-c)n/2)->1. For any T, RSS_T>=r. Together with L2's Q-RSS bound and ||e||^2/n->1, the multiplier M_T=nu*n*d^2/(alpha*psi_T) obeys, uniformly over the family,

.5-o(1) <= M_T <= 2/(1-c) =: Mbar.

The upper bound follows from psi_T>=RSS_T/s^2>=r/s^2 and nu*n*d^2*s^2/alpha=(n/2)(1+o(1)). Here all comparisons occur on a single event of probability ->1.

## 2. Any chosen swap must import a rare extreme

The available near-centre null has deletion gain
Delta_K - nu log(1+(1+gamma_{K-1})M_T tau_j^2/nu)
>= Delta_K -(1+gamma_{K-1})Mbar >= .5 log n-O(1),
where tau_j=xi_j-x_T and log(1+x)<=x. Thus the best deletion has gain >=.4 log n eventually. A chosen swap must gain at least this much. For every null pair, |V_jl|<=C log n on the maximum-coordinate/centre event, so u=M_T V_jl/nu=O(log n/n). For a positive swap, -log(1-u)<=2u eventually; since V_jl<=tau_l^2, its gain is <=2Mbar tau_l^2. Hence a chosen null swap satisfies tau_l^2>=(1-c)log n/10 eventually.

As |x_T|<=B, this implies |xi_l|>=sqrt(a log n) for a=(1-c)/20, eventually. Define the fixed exceptional pool E={j null: |xi_j|>=sqrt(a log n)}. By a Gaussian tail bound, E|E|<=2p*n^(-a/2)=O(n^(1-2eta0)), since a/2=2eta0. Markov gives P(|E|>H/2)=O(n^(-eta0))->0.

## 3. Imported extremes cannot be swapped out during this phase

For a fixed incoming null l the swap quadratic is
V_jl=constant_l-(1+gamma_K)[tau_j-gamma_K tau_l/(1+gamma_K)]^2.
Thus the best outgoing null minimizes the displayed distance. A retained near-centre null has |tau_j|<=1; also |gamma_K tau_l|=O(sqrt(log n)/n). Therefore every maximizing outgoing null has |tau_j|<=2 eventually, uniformly over l. Its raw coordinate satisfies |xi_j|<=B+2. This is less than sqrt(a log n) eventually. Consequently a selected swap never removes a member of E; since each selected swap imports an outside member of E, all its imported exceptional indices are distinct.

Truth-out moves are not an alternative: the L2 uniform bound t_truth=f+O(sqrt(n log n)), t_null=O(sqrt(n log n)) still holds throughout this enlarged family, so every truth-out swap has negative gain. A truth deletion also has negative gain: its log-loss argument (1+gamma) M_T(t_truth/d)^2/nu is bounded below by a fixed positive constant, since f/d=sqrt((n-1)/2) and M_T>=.5-o(1). Its loss is therefore of order n, against Delta_K=O(log n). Additions are infeasible at K. A positive null deletion is always available, so the search cannot stop in this phase.

## 4. Stopping the swap phase

On the combined event |E|<=H/2, induct along the path while it makes null swaps. Every preceding family argument is valid up to H moves. If the first H moves were all swaps, they would import H distinct members of E, contradicting |E|<=H/2. Hence the first nonswap occurs before H; by section 3 it is a null deletion. In fact W_n<=|E|<=H/2<=n^(1-eta0) eventually. This proves the claim. The lower divergence W_n/log n->infinity follows from L2's assertion for each fixed C.

## Scope and remaining step

For the initial phase alone, the wasted swap moves are o_P(n), hence smaller than K with probability ->1. It remains to prove that later deletions reach S0 without an uncontrolled number of swaps or additions; this lemma does not assert a globally two-phase path. Even a completed singleton cap remedy would not establish the production-partition result.

Falsification script/output: numerics/n6_initial_phase.py and N6_initial_phase.json. Independent lemma review pending.

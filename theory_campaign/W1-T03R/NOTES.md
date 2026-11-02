# W1-T03R working notes (progress log; REPORT.md is the deliverable)

## 2026-11-02 step 1 — reading done; key findings (to be proved in PROOF.md)
1. EXACT BB(1,p) size marginal: q_k = C(p,k)w(k) = 1/2 * prod_{i<k} (p-i)/(2p-1-i); each factor = 1/2(1-(i-1)/(2p-1-i)).
   So the size marginal is GEOMETRIC(1/2) up to exp(-k^2/(4p)). The per-MODEL ratio w(k+1)/w(k) ~ k/(2p) is
   cancelled by the multiplicity C(p,k+1)/C(p,k) ~ p/k. (FABLE_REVIEW's "ratio ~ k/2p, not 1/2" is the per-model ratio.)
   => exact tail gains ~log2(s0!) bits + Gaussian factor exp(-m^2/(4p)); m_n - s0 stays ~ log2 C(p,s0) + (s0+2)/2 log2 n
   = Theta(s0 log n). The hoped-for m_n = s0 + O(s0 log n / log p) is NOT reachable by the Markov route (lower bound),
   and is FALSE in general under G,R (duplicate-column counterexample: Pi(|S|>m) >= c 2^{-m}).
2. With the cap, R_m = 0 for m >= K, so the new threshold m# <= K automatically.
3. SE can be split: normalised SE only on S0 u J, |J| <= j* (fixed); for |J| <= m# only lambda_min(G_{S0uJ}) >= g0 > 0
   (unnormalised, i.e. lambda_min(R) >= g0/(n-1)) is needed (determinant penalty f(g) >= (n+1)/(1+1/g)).

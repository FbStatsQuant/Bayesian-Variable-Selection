# Notes 02: Johnson–Rossell 2012; Shin–Bhattacharya–Johnson 2018; Rossell 2022; Narisetty–He 2014

## Johnson & Rossell (2012), JASA 107(498) 649–660. READ: Papers/Core_bibliography/17_2012_Johnson_Rossell_...pdf
- Thm 1 (pMOM nonlocal priors, order r ≥ 2): "Suppose there exists ε > 0 such that p(t)/p(k) > ε for all k ∈ J. Assume further
  that p ≤ n and ... λ1(X'X) < nM and λp(X'X) > nc ... then p(t | y_n) →p 1." (σ² known.) Cor 1: σ² ~ common IG, p < bn, b < 1.
- Thm 2 (local priors fail), quoted: "If the prior densities assumed for model t and k ∈ J1 satisfy p(k)/p(t) > δ > 0, and there exists
  an N such that p > n^{1/2+ε} ... for all n > N, then p(t | y_n) →a.s. 0." Their gloss: fails "whenever (1) p > O(√n), (2) local
  prior densities ..., and (3) the relative prior probabilities assigned to all models are bounded away from 0."
- Bearing on T03♯: our prior IS local (Gaussian slab) and p = n^{1.17..1.30} ≫ √n, but BB(1,p) violates JR's (3):
  w(s0+1)/w(s0) = (s0+1)/(2p−1−s0) → 0. So JR Thm 2 does not apply and there is no contradiction; T03♯ is a concrete instance of
  "local prior + multiplicity-correcting model prior is consistent for polynomial p", which JR's Thm 2 leaves open by its hypothesis (3).
  JR also need full-rank X'X (p ≤ n); T03♯ does not (only SE up to size m♯_n).

## Shin, Bhattacharya & Johnson (2018), JASA 113(523) 1176–1190 (arXiv:1507.07106). READ: Papers/Core_bibliography/18_...pdf
- Assumptions (quoted): "A1 There exists α ∈ (0,1) such that log p = O(n^α)"; A2 log p ≺ τ ≺ n; A3 |k| ≤ q_n ≺ n/τ... [garbled
  in text extraction]; A4 sparse Riesz: min_{|k|≤q_n} ν_*(X_k'X_k/n) bounded below by a rate; A5 eigenvalues of the true model bounded.
- Thm 1 (σ² known, peMoM, uniform prior on models of size ≤ q_n): "π(t | y) converges to one in probability". Thm 3: σ² ~ proper IG.
  Their remark (quoted): "these results apply also if a beta-Bernoulli prior is imposed on the model space as in Scott and Berger (2010),
  because the effect of that prior is asymptotically negligible when |k| ≤ q_n ≺ n."
- Nonlocal prior; SR condition over ALL models of size ≤ q_n (unanchored). Not our prior.

## Rossell (2022), Bayesian Analysis 17(2) 565–591, doi:10.1214/21-BA1262 (arXiv:1806.04071). READ: arXiv PDF (downloaded, pdftotext)
**Closest prior art to T03♯ and to the 2E[1−π] step.**
- Prop 1, quoted: "Let k̂ = arg max_k p(M_k | y) be the posterior mode, then P_f*(k̂ ≠ t) ≤ 2E_f*(1 − p(M_t | y))." Text: "Proposition 1
  also holds when k̂ is the median probability model of Barbieri and Berger [2004]".
  → this is EXACTLY T03♯(3) [P₀(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)]] and the first term of Thm 4 (T21) and Thm 5(0). KNOWN.
- Priors covered: Zellner (τ fixed or growing; known and unknown variance, IG on φ), pMOM; model priors uniform, "Beta-Binomial(1,1)"
  (P(p_k = l) = 1/p̄) and Complexity(c) (P(p_k = l) ∝ p^{−cl}); max model size p̄ with (B1) "p̄ ≪ min{n, p, nτ}", (B2) p_t ≪ min{p̄, n}.
- §5.2 (BB(1,1), spurious = supersets of t), quoted: "under τ = 1 one can handle p − p_t ≪ n^{a/2} variables, i.e. p can grow
  polynomially with n ... the Beta-Binomial prior can handle problems of fairly large dimension and still discard all spurious models."
  Explicit L1 rate (unknown φ, Zellner): E(P(S | y)) ≲ (p_t+1)·exp{2[log^{3/2}((τn)^{1/2}(p−p_t))]√((p−p_t)/(n−p̄))}/(τn)^{1/2}.
- §5.4 Prop 9: non-spurious models, with λ_tm = (X_tθ*)'(I−H_m)X_tθ*/φ* and Lemma 3 lower bounds via v_tm = smallest nonzero
  eigenvalue of X_t'(I−H_m)X_t/n — i.e. eigenvalue conditions ANCHORED at the true model, over models of size ≤ p̄;
  (F1) for BB: λ/2 + (1−α) log p − 0.5 log(nτ) → ∞ (λ ≈ [n v min θ²/φ]^α, a beta-min).
- Rossell's own comparison (quoted): NH 2014 and YWJ 2016 "required τn ≫ p²"; CSvdV and YWJ "required p(M_k) to be a Complexity prior";
  "Our C1-C2 in principle allow more general τ and p(M_k), such as fixed τ and p(M_k) that do not penalize model size exponentially,
  e.g. the Beta-Binomial."
- Bearing: Rossell already proves concentration for a unit-information-type Zellner prior (τ = 1) with a NON-complexity BB model prior,
  polynomial p, anchored eigenvalue quantities and an L1 rate. Differences from T03♯: (a) his BB is BB(1,1), ours BB(1,p) (per-model
  w(k) ≈ k!/(2p)^k vs C(p,k)^{−1}/(p̄+1)); (b) he needs p̄ ≪ n, our cap K = ⌊n/2⌋ is not o(n) — T02(i♯)'s exact tail is what lets us
  live with K = n/2 (the tail beyond m♯_n is handled by prior mass, not by a p̄ restriction); (c) our slab is the ridge-stabilised
  N(0, nσ²(G_S+I)^{−1}), not Zellner; (d) standardised data and a data-dependent scale. Net: T03♯ is a MODEST EXTENSION in the
  Rossell line, not a new phenomenon. Its exact-tail/size-cutoff device (T02(i♯), m♯_n) is the most distinctive technical piece.

## Narisetty & He (2014), Ann. Statist. 42(2) 789–817 (arXiv:1405.6545). READ: arXiv PDF
- Prior: independent inclusion with prob q_n, Gaussian spike N(0, σ²τ0n²) (shrinking) and slab N(0, σ²τ1n²) (diffusing).
- Cond 4.1: log p_n = o(n). Cond 4.2 (garbled extraction; reading): nτ0n² = o(1), nτ1n² ∼ (n ∨ p^{2+3δ}), q_n ∼ p_n^{−1}.
  Cond 4.3: |t| fixed; small nonzero inactive coefficients allowed (‖X_{t^c}β_{t^c}‖₂ = O(1)). Cond 4.4 (identifiability):
  Δ_n(K) := inf_{|k|<K|t|, k⊉t} ‖(I−P_k)X_tβ_t‖² > γ_n = 5σ²|t|(1+δ) log(√n ∨ p_n) for some K > 1 + 8/δ.
  Cond 4.5: eigenvalue regularity λ_m(ν) on models of size up to a growing bound.
- Thm 4.1/4.2: strong selection consistency P(Z = t | Y) → 1 in probability (fixed σ² and σ² ~ IG respectively) [statement lines
  not fully legible in extraction; consistent with abstract: "the posterior probability of the true model converges to one even when
  the number of covariates grows nearly exponentially with the sample size"].
- Bearing: q_n ∼ 1/p is per-model like BB(1,p) (both ≈ p^{−1} per variable), but NH's slab variance ≳ p^{2+3δ}/n gives a ≥ p^{1+δ}
  Occam penalty per variable; ours (g = n) gives only √(n+1) < p. This is precisely why T03♯ needs p ≤ n^A and the exact-tail device;
  NH's identifiability Δ_n(K) is anchored at t, over models of size < K|t| — a close analogue of our anchored, size-restricted SE.

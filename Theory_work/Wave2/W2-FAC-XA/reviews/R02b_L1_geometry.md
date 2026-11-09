# R02b — Fresh cross-family review of XA lemmas/L1_geometry.md (L1a, L1b, L1c)

Reviewer: fresh Claude Opus 5.5 review seat (replaces the incomplete R02). It read only:
STATEMENT.md, lemmas/L1_geometry.md, numerics/N4_geometry.py, N4_geometry_out.json,
reviews/R02_incomplete_reply.md, R02_scratch/r02_checks.py, r02_checks_out.json.
It did not read LOG.md or any lead conclusions. No new script was run. The R02 scratch
JSON is complete: it is written once, at the end of r02_checks.py, and all three sections
are present. No downstream (path, score, start or delivery) consistency is assessed or
claimed.

## VERDICT: PASS-WITH-FIXES (MINOR)

Every step of L1a, L1b and L1c is correct as mathematics. No step is false, and none
needs a new idea. Four fixes are needed before downstream use. Each one either makes
explicit something the text leaves implicit (F1–F3) or tightens wording that is loose (F4–F6).
After F1–F6, L1 may be marked PROVED-CHECKED for exactly its stated scope: it couples
noise statistics at the same T and says nothing about adaptive T, score transfer or signal.

## Line-by-line check

### L1a
- Helmert rotation: dS = sum over d = n-1 iid N(0,Sigma) rows. Correct.
- E(S_ij - Sigma_ij)^2 = Var(x_i x_j)/d = (Sigma_ii Sigma_jj + Sigma_ij^2)/d =
  (1+Sigma_ij^2)/d, and the diagonal gives 2/d (Isserlis). Correct. Hence
  E||S-Sigma||_F^2 = (p^2 + ||Sigma||_F^2)/d <= 2p^2/d. Correct.
- P(|S_ii - 1| > 1/2) <= (2/d)/(1/4) = 8/d, so P(B^c) <= 8p/d. Correct.
- On B: R_ij - Sigma_ij = (S_ij - Sigma_ij) f(S_ii,S_jj) + Sigma_ij (f(S_ii,S_jj) - 1), with
  f(u,v) = (uv)^{-1/2}. On [1/2,3/2]^2, f <= 2 and |grad f| <= 2 in each coordinate
  (the maximum is at u=v=1/2). So |R_ij - Sigma_ij| <= 2|dS_ij| + 2|Sigma_ij|(|dS_ii| + |dS_jj|),
  i.e. the absolute constant is C=2. The diagonal entries of R - Sigma are exactly 0.
- Squaring with (a+b)^2 <= 2a^2 + 2b^2 and taking expectations:
  E[1_B ||R-Sigma||_F^2] <= sum_{i!=j} [8(1+Sigma_ij^2) + 64 Sigma_ij^2]/d <= 80 p(p-1)/d.
  Correct, using |Sigma_ij| <= 1. Bounding 1_B times the B-valid expression by the
  unconditional expectation is legitimate.
- Markov plus P(B^c) -> 0 gives the O_P rate. Then op <= F, and ||Sigma^{-1/2} M Sigma^{-1/2}|| <=
  ||M||/lambda_min. Correct. No spike-free assumption is used. Correct.
- Scope remark: only P(B^c) -> 0 needs p = o(n). The hypothesis p = o(sqrt n) is used only
  to make e = o_P(1). Both hold for p <= n^a with a < 1/4.

### L1b
- L = (I+E)^{1/2} is symmetric. B'B = A L^2 A = A(I+E)A = R, because A = Sigma^{1/2} is symmetric.
  The eigenvalues of L are sqrt(1+mu) with |mu| <= e, and |sqrt(1+mu) - 1| = |mu|/(1+sqrt(1+mu)) <= |mu|.
  So ||L - I|| <= e and sigma_min(L) >= sqrt(1-e). Correct.
- V = L U = span(B_T), since B_T = L A_T. Correct.
- ||(I-P_V)P_U|| <= e and ||(I-P_U)P_V|| <= e/sqrt(1-e). Correct.
  The identity P_U - P_V = P_U(I-P_V) - (I-P_U)P_V checks by expansion. The transpose step is correct.
  At e <= 1/4: e + e/sqrt(1-e) <= 0.539 <= 3e (in fact <= 2.16e). Correct.
- ||(I-P_V)b_j - (I-P_U)a_j|| <= ||b_j - a_j|| + ||(P_U - P_V)a_j|| <= e + 3e. This uses
  ||a_j||^2 = Sigma_jj = 1 and b_j - a_j = (L-I)a_j. Correct.
- Residual lower bound: ||a_j - A_T t||^2 = (1,-t)' Sigma_{{j}uT} (1,-t) >= lambda_min(Sigma) ||(1,-t)||^2 >= c,
  by Cauchy interlacing for principal submatrices. Correct.
- ||r/|r| - s/|s|| <= 2|r-s|/|s|. Correct (triangle inequality on |s| - |r|). This gives 8e/sqrt(c).
  The stated 10 is valid slack.
- The statement is deterministic, so "simultaneously for all T, j" needs no union bound. Correct.
  The case T empty is correct.
- e <= 1/4 is used only for the factor 3 and for the invertibility of L. Any e <= 3/4 would also do.

### L1c, joint covariance and residual-energy coupling
The coupling can be realised exactly on the ORIGINAL space; no enlargement is needed.
Let Xt be the centred, sample-sd-standardised design, so that Xt'Xt = dR = d B'B.
Let C be the centring matrix and normalise the noise so that eps ~ N(0, I_n).

On {R positive definite}, which holds a.s. when p <= d and in particular on {e <= 1/4} because
I+E >= (1-e)I, put
  O = Xt B^{-1} / sqrt(d),    z = O'eps,    r = ||C eps||^2 - ||z||^2.

Then:
- O'O = B^{-T} R B^{-1} = I.
- col(O) lies in 1-perp, so C O = O and O'eps = O'C eps.
- Conditionally on X: z ~ N_p(0, O'CO) = N_p(0, I), and r = ||(C - OO')eps||^2 ~ chi^2(d-p).
  The two are independent, since C - OO' and OO' are orthogonal projections.
  Neither conditional law depends on X, so (z, r) is independent of ALL of X, not just of R.
- For each (T, j), with v = (I - P_{Xt_T}) xt_j = sqrt(d) O (I - P_{B_T}) b_j, the data statistic
  v'eps/||v|| equals q_B(T,j)'z EXACTLY, jointly for all (T, j).
- Xt'eps/sqrt(d) = B'z = g_B.

Hence the joint covariance of {Z_B(T,j)} is {q_B'q_B'}, which is exactly the data's, and the
full-model residual energy is r (the signal X_c theta lies in col(Xt)).
Similarly, (g_A, ||z||^2 + r) has the exact law of (X'eps/sqrt(d), ||C eps||^2) in an exact-Gram-Sigma
design, i.e. C2-E. Z_A and Z_B share the same z, as the lemma intends.

The R02 scratch confirms this identity to machine precision. Over 12 data cases
(CS0.5 and one-factor, n = 400..40000, p = 8 and 32, all T up to the stated size):
identity_err <= 2.1e-14 and orth_err <= 2.0e-14.

- sup_{T,j} |Z_B - Z_A| <= sup ||q_B - q_A|| ||z|| <= 10 e ||z|| / sqrt(c). This holds on {e <= 1/4}.
- e = O_P(p/sqrt n) and ||z|| = O_P(sqrt p) give O_P(p^{3/2}/sqrt n). This is o_P(1) iff
  p = o(n^{1/3}), and it covers every p <= n^a with a < 1/3, including bounded p. Correct.

### Uniform constants and the event e <= 1/4 (explicit; see F1, F2)
From L1a with C=2, for every unit-diagonal Sigma with lambda_min(Sigma) >= c, every n, every p <= d,
and every M, K > 0:
  (U1) P(||R-Sigma||_F > M p/sqrt d) <= 80/M^2 + 8p/d.
  (U2) G_n := {e <= 1/4} satisfies P(G_n^c) <= P(||R-Sigma||_F > c/4) <= 1280 p^2/(c^2 d) + 8p/d.
  (U3) P( G_n and sup_{T,j} |Z_B - Z_A| > 10 M K p^{3/2} / (c^{3/2} sqrt d) ) <= 80/M^2 + 8p/d + 1/K^2,
       using P(||z|| > K sqrt p) <= 1/K^2.
All three bounds depend only on (c, n, p). They hold uniformly over all such Sigma and over truth
positions and loadings varying with n. So they serve the random-design transfer obligation
(the common-constant design events A_n of STATEMENT.md).
For C1, c = 1 - rho. For C2, c >= 1 - lambda_hi^2, since in Loewner order
Sigma = diag(1 - lambda^2) + lambda lambda' >= diag(1 - lambda^2) >= (1 - lambda_hi^2) I. Both are fixed. Note that the absolute
||R-Sigma|| = O_P(p/sqrt n) here is PROVED inside L1a from fourth moments. It is not the
forbidden sqrt(p/n) input, so the norm discipline is respected.

## Numerics audit
- N4: 20 cases (p = 4, 8; 10 seeds; 5,280 (T,j) directions); ||E|| = 0.24 <= 1/4.
  The largest ratio maxdir/bound is about 0.028. N4's E does not keep diag(R) = 1, but the proof
  never uses ||b_j|| = 1, so N4 tests a slightly more general claim. Valid, but random rather
  than adversarial.
- R02 L1b adversarial (Nelder-Mead over symmetric E with 6 starts, including c down to 1e-3):
  the worst K is 0.36, against the proved 8. Empirically worst ||q_B - q_A|| is about 0.5e
  regardless of c, which suggests the 1/sqrt(c) factor is slack. This is an observation, not a claim.
- R02 L1a: relative norm / sqrt(p/d) is about 1.2–2.2 and stable. Absolute / (p/sqrt d) is about
  0.4–0.66 and flat in p for CS. This is consistent with L1a's deliberate conservatism and with
  the R01 absolute-norm caution. fro^2·d/p^2 <= 0.75 <= 80. rel <= abs/c holds in all cases.
- R02 L1c: sup|Z_B - Z_A|/bound <= 0.022. sup/(p/sqrt n) is about 0.23–0.69, while sup/(p^{3/2}/sqrt n)
  falls with p, so the p^{3/2} rate looks conservative. One case (1F, n=400, p=8) has e = 0.42 > 1/4,
  i.e. it lies OUTSIDE G_n. The bound still held empirically, but this shows the event must be stated (F2).
- No falsification was found. The numerics are consistent with every claim.

## Exact fixes required
F1 (L1a, uniformity). After "the asserted O_P rate", add:
  "Explicitly, with C=2 (sup of |grad (uv)^{-1/2}| on [1/2,3/2]^2),
   E[1_B||R-Sigma||_F^2] <= 80p(p-1)/d, so P(||R-Sigma||_F > Mp/sqrt d) <= 80/M^2 + 8p/d
   for every unit-diagonal Sigma, all n, p <= d, M > 0. The relative bound adds the factor 1/c."

F2 (L1c, event). Replace "Thus sup_{T,j}|Z_B-Z_A|<=10 e||z||/sqrt(c)." with:
  "On G_n = {e <= 1/4}, sup_{T,j}|Z_B-Z_A| <= 10 e||z||/sqrt(c). By F1,
   P(G_n^c) <= 1280p^2/(c^2 d) + 8p/d -> 0, and
   P(G_n and sup > 10MKp^{3/2}/(c^{3/2}sqrt d)) <= 80/M^2 + 8p/d + 1/K^2,
   uniformly over unit-diagonal Sigma with lambda_min >= c."

F3 (L1c, independence and realisation). Replace "On an enlarged probability space choose
  z~N_p(0,I) independent of R and r~chi-square(d-p) independent of both (r=0 when d=p)." with:
  "Normalise eps ~ N(0,I_n) (divide by the fixed noise sd). On {R > 0} (a.s. for p <= d; always on G_n)
   set O = Xt B^{-1}/sqrt d, z = O'eps, r = ||C eps||^2 - ||z||^2. Then O'O = I and CO = O;
   conditionally on X, z ~ N_p(0,I) and r ~ chi^2(d-p) are independent with laws free of X.
   So (z, r) is independent of the whole design sigma-field (not merely of R), and
   Xt_j'(I-P_{Xt_T})eps / ||(I-P_{Xt_T})Xt_j|| = q_B(T,j)'z exactly, for all (T,j) jointly.
   No enlargement is needed."
  Also replace the sentence "The joint law assertion follows because ..." with this identity.
  It is stronger: an almost-sure equality, which is what the diagonal / conditional argument needs.

F4 (L1c, definitions). Define the statistic explicitly: Z(T,j) = xt_j'(I-P_T)eps / ||(I-P_T)xt_j||
  on the noise-sd-normalised scale. State that g_A, Z_A reproduce jointly, in law, the exact-Gram-Sigma
  (C2-E) noise statistics and residual energy. Do not just say "has the correct joint law with each g".

F5 (L1b, cosmetics). Note that 8e/sqrt(c) is what the proof gives (10 is slack), and that e <= 1/4 is
  used only for invertibility and the factor 3. Optionally state ||P_U - P_V|| <= e + e/sqrt(1-e).

F6 (L1, Setting, scope). Add: "Raw rows may have any mean and any positive column scales: R is
  invariant to both, so Sigma denotes the correlation matrix. For C1, c = 1-rho. For C2,
  c = 1-lambda_hi^2." Keep the existing disclaimers (same-T only; no score, start, path or
  signal transfer) unchanged.

## What is NOT established (unchanged by this review)
L1 couples noise statistics at fixed (T, j) only. It gives no control of the signal terms
(R theta vs Sigma theta), the ridge or determinant parts of the production score, argmin or ordering
stability, or adaptive paths. These remain open obligations, as the lemma itself says.

Recommended status after F1–F6: PROVED-CHECKED (L1 scope only).

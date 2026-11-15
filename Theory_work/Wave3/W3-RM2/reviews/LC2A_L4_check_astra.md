MANIFEST b643f323a2ac2948975e3f01e54d30c0e64cf6643eebe911d1475fac270c3dc6

# LC2-A: independent check of L4, W3-RM2

Verdict per lemma/claim:

- Lemma SAND-R^b / bridge (P7): **VERIFIED-WITH-AMENDMENTS** (minor conditional-law wording correction below; no hypothesis or conclusion needs changing).
- Lemma 2, including (2.1), (2.2), (2.3), and (★): **VERIFIED**.
- Lemma 3, spherical tail (3.1): **VERIFIED-WITH-AMENDMENTS** (Finding 1; its inequality and proof after the stated correction are valid).
- Lemma 4, counting bound (4.1): **VERIFIED**.
- §7 item 1, v1.3 sufficient form implies (R-G): **VERIFIED**.

No FATAL or MAJOR finding. Neither the product-form step nor the slower localisation rate introduces a missing hypothesis. The principal proof works for every X-measurable partition and simultaneously for every maximiser.

I read the assigned brief first. Only manifest-listed source files and the manifest were read thereafter; no other review, log, or checkpoint was consulted. The SHA256 hashes of L4, STATEMENT, L0, and L1 match the manifest. L0's toolkit statements are accepted as instructed; I checked their application here. No git operation was performed.

## Findings

1. **MINOR — `lemmas/L4_sandR_b.md:157-165`: distinguish an independent innovation from its random projection.** The statement that the ambient vector G is independent of the sigma-field G-script is literally incorrect when its support is the G-script-measurable random subspace V. In the displayed construction, G = Pi e/tau, and its conditional covariance is Pi, which generally depends on W_U0. This does not invalidate the tail bound: only the conditional Gaussian law is needed, and the unprojected innovation really is independent.

   Exact correction: replace “g = tau G with G a standard Gaussian vector of V, independent of G-script” by “z := e/tau is N_n(0,I_n) and independent of G-script; g = tau Pi z. Conditional on G-script, G := Pi z has law N_n(0,Pi), hence ||G||^2 has law chi-square_d and G^T v has law N(0,1) for each G-script-measurable unit v in V.” No independence of the last two statistics is required. Equivalently use coordinates in a measurable orthonormal frame for V. With this replacement, lines 160–171 establish exactly (3.1).

2. **NIT — `STATEMENT.md:182`: incorrect section pointer.** The sufficient-form implication is in L4 §7 item 1, not §6. Replace the cited section with “§7 item 1.” The mathematical statement agrees with L4.

## Independent derivations

### 1. Covariance event and bounded-dimensional regularity

Write delta = C_A h_n, d0 = 16+s0. After applying O^T, the N rows are independent centered Gaussians, including the noise coordinate. For each sign the polarisation variable has variance at most 4. Laurent–Massart gives its empirical-variance error at most 8 sqrt(x/N)+8x/N, with failure probability at most 2 exp(-x). Dividing the difference of two such errors by four gives

    |S_hat_ab - Sigma_tilde_ab| <= 4 sqrt(x/N)+4x/N.

For x=(2A+3)log n this is at most 8 sqrt(2A+3) h_n for sufficiently large n. There are at most 4 n^(2A) ordered pairs and four exp(-x) failure probability per pair, yielding exactly 16 n^(-3). Singular plus/minus variables cause no difficulty.

For m=|B|<=d0, ||S_hat_BB-Sigma_BB|| <= m delta. Thus S_hat_BB has floor c/2 and its inverse differs from Sigma_BB^(-1) by at most 2m delta/c^2. For coordinate cross-vectors their norms are at most 2 sqrt(m) and sqrt(m), and the error norm is at most sqrt(m)delta. One explicit bound on the triple-product difference is

    (6m/c + 4m^2/c^2) delta.

Adding the direct covariance error supplies a uniform O(h_n) Schur-complement error. Bilinearity multiplies the bound by at most max(1,2s0 theta_hi+sigma)^2 for the stated coefficient box. No covering argument or independence of beta* is involved. Even the broad formulation of 1.2(ii), where S0 need not be contained in D, can be proved this way: only Sigma_BB is inverted, and all needed cross entries are controlled by the global entrywise event. In the actual uses D already includes S0 and has size at most 16+s0.

Sample standardisation changes each correlation entry by at most 3delta eventually; d0 times this tends to zero, giving the asserted c/2 sample floor after enlarging n0. Population residual design variances have floor c by the Schur-complement variational formula. The response's population residual variance is at least sigma^2 for every beta in the box, since its noise coordinate is independent. The same comparison therefore bounds the sample residual response variance away from zero uniformly in beta.

With a_res=(I-P_B)CW_a and y_res=(I-P_B)Y, the RSS reduction is (a_res^T y_res)^2/||a_res||^2. Both inner products are N times the corresponding sample conditional covariances; dividing by RSS_B proves h=n z_hat^2 exactly. Scaling CW_a to x_a does not affect its residual direction.

For visibility, conditional coordinate covariances have absolute value at most one. Replacing theta by theta/t changes the population signal covariance by at most s0 theta_hi max|1/t-1|=O(h_n). The sample comparison costs another O(h_n). Consequently

    delta_Uj^2 >= N (a0-O(h_n))^2/(1+C_A h_n) >= N a0^2/4.

The energy bound is deterministic: ||mu|| <= s0 theta_hi sqrt(N).

Conditional on W, X, mu, the partition, and all vectors in the toolkit family are fixed. The family of all sets of size at most 16 contains every realised block subset. H-F, H-G with phi0^2=c/2, H-E with M=s0^2 theta_hi^2, H-V, and H-S all hold; both logarithmic cardinalities are O(log n), so H-S is O((log n)^2/n). The probability constants can be uniform over W in E_W. Conditional Z_Uj variables are standard normal, and the displayed union bound s0 2^16 n^(-16) follows from z_n^2=2(15A+16)log n. No conditioning on the selected block alone is used.

### 2. Product identity and sample perturbation

Fix l,U, put U0=U intersect H_l and V=U minus H_l. Since H_l contains S0, V contains no truth. Conditional on U0, the covariance matrix for (l,V,V_beta) has cross-vectors c_l,c_y and V-block S_VV. Eliminating that block gives

    S(l,V_beta | U) = S(l,V_beta | U0) - c_l^T S_VV^(-1)c_y.

The two signal covariances are sums of at most s0 terms with coefficient magnitude at most 2theta_hi and leak at most ell_n; independent noise contributes zero. Therefore their difference has magnitude at most 4s0 theta_hi ell_n. This proves (★) directly, without any bound involving r_n^2. Crucially (R-G) is available at both U and U0, not just at the latter.

Let m=|V|<=15, e_l=c_hat_l-c_l, e_y=c_hat_y-c_y, A=S_VV^(-1), A_hat=S_hat_VV^(-1). The relevant bounds are

    ||c_l|| <= sqrt(15)r_n,
    ||c_y|| <= 2s0 theta_hi sqrt(15)r_n,
    ||e_l||, ||e_y|| <= sqrt(15)C1 h_n,
    ||A|| <= 1/c,  ||A_hat|| <= 2/c,
    ||A_hat-A|| <= 30 C1 h_n/c^2.

The exact difference of cross products is

    e_l^T A_hat c_hat_y + c_l^T(A_hat-A)c_hat_y + c_l^T A e_y.

Its terms have orders h_n(r_n+h_n), r_n h_n(r_n+h_n), and r_n h_n. For r_n<=1 their sum is O(r_n h_n+h_n^2). In particular there is no surviving h_n times a nonvanishing cross-vector: both population cross-vectors are O(r_n).

The variance reductions are O((r_n+h_n)^2). The response and column residual variances, both before and after eliminating V, have fixed positive floors. On this region the inverse square-root denominator is Lipschitz. Multiplying its change by |s_hat_ly|=O(ell_n+h_n)=O(h_n) gives O(h_n(r_n+h_n)^2), which is bounded by O(r_n h_n+h_n^2). Adding the numerator change proves (2.1). It also proves (2.2), since the reference numerator is O(h_n).

Finally ||z_U|-|z_U0|| <= |z_U-z_U0| and h=n z^2 imply (2.3). Its error divided by sqrt(log n) is O(ell_n/h_n+r_n+h_n), which tends to zero. All these statements hold uniformly over the coefficient box before substitution of beta*. Every floor used is on U, U0, or a subset of U union {l} union S0; none exceeds 16+s0.

### 3. Spherical tail, including the shifted mean

For deterministic (l,U0), regression on D=U0 union S0 produces an innovation e independent of (W_D,epsilon), with variance tau^2 in [c,1]. The truth conditional covariance matrix has floor c, and the leak vector has norm at most sqrt(s0)ell_n, so ||alpha||<=sqrt(s0)ell_n/c and ||alpha||_1<=s0 ell_n/c. On CN_D,

    ||m|| <= (2s0/c)sqrt(n)ell_n = M_n = o(sqrt(log n)).

Both the signal scale beta*=theta/t and the response are measurable with respect to sigma(W_D,epsilon), because all truths belong to D. This measurability does not extend to scales of arbitrary other columns, and the proof correctly avoids conditioning on them. Also E_cov implies CN_D; it is not used as a conditioning event for the innovation law.

Using the corrected conditional formulation in Finding 1, d=N-|U0|>=n-16 and ||G||^2 is conditionally chi-square_d. With x=d n^(-1/2)/4, the lower-tail bound gives P(B^c | G-script)<=exp(-sqrt(n)/8) eventually. On B, triangle inequalities and 1/(1-x)<=1+2x give

    sqrt(h) <= (1+4 n^(-1/4)) |G^T v| + (4/sqrt(c))M_n.

The constants in the manuscript suffice: ||g||>=sqrt(cn)/2 and M_n/sqrt(n)=o(n^(-1/4)). The conditional scalar G^T v is standard normal; it need not be independent of ||G||. Union with B^c gives line 167.

For a=kappa M_n, (sqrt(t)-a)_+^2 >= t-2a sqrt(t). The factor (1+4n^(-1/4))^(-2) is at least 1-8n^(-1/4). Uniformly over 0<=t<=(2A+3)log n, the resulting exponent is bounded above by

    -t/2 + kappa M_n sqrt((2A+3)log n) + 1/2,

and the middle term equals 8s0 c^(-3/2)sqrt(2A+3) sqrt(n log n)ell_n. This verifies the claimed n^{o(1)} loss, including small t where the positive part vanishes. Integrating only with the CN_D indicator proves (3.1). Null residual-response events have probability zero and may be assigned h=0.

### 4. Reference count, thresholds, ladder, and final improvements

If |H_l|=m, each subset of H_l minus {l} of size at most 15 can be encoded by its ordered elements followed by padding, in a length-15 word on m symbols. Hence |I_l|<=m^15<=n^(15rho). Determinism of H_l makes Lemma 3 applicable to each reference pair.

On E_cov a crossing at t implies a reference crossing at t'=(sqrt(t)-C2 vartheta_n)^2. The positive lower endpoint epsilon0 log n guarantees the parenthesis is nonnegative eventually; t'<=t and the loss in t/2 is at most C2 vartheta_n sqrt((2A+2)log n)=o(log n). Union over the references proves (4.1).

For 1<=k<=K, t_n(k) is between log n-C0 and (2A+1)log n+1, inside Lemma 4's range eventually. The exact cancellation p exp(-t_n(k)/2)=k exp(C0/2)/sqrt(n+1) gives (4.2). For epsilon*=(1-2b-30rho)/2, one has 0<30rho+epsilon*<1, so T_n is in the claimed range. Its reference-count factor cancels to n^(-epsilon*/2+epsilon_n), proving (4.3).

From E6-tab and h=O(log n), the error in replacing -nu log(1-h/n) by h/2 is O((log n)^2/n), eventually at most 1/2. This gives (5.1). Per-block optimality and the exact prior ratio force at least one selected outside column in each contributing good block to exceed t_n(k_tilde). The imported count (2.1) then gives (5.2).

On a rung m_i<k_tilde<=2m_i, J(t_n(min(2m_i,K)))>m_i/32. This event contains the existence of any such maximiser, so there is no union over maximisers. Markov costs at most 64C5 n^(-1/2+15rho+epsilon_n) per rung, plus an exponentially small term. There are O(log n) rungs; 15rho<1/2 suffices.

When Q is proper, k_tilde<=2q+32s0<=K-1 makes a missing truth addition feasible. When Q=[p], q<=K forces K=p, and a missing truth again makes addition feasible. Its fit gain is at least Na0^2/8-sigma^2 z_n^2, whereas determinant and prior losses are O(log n). The improvement is strict eventually.

For outside-column deletion, substituting T_n cancels log p. The remaining logarithmic coefficient is

    (1-30rho-epsilon*)/2 - b
      = (1-2b-30rho-epsilon*)/2 = epsilon*/2 > 0.

Using k_tilde<=(2+32s0)n^b gives exactly the constant loss and margin in lines 232–234. Every improvement is strict on the same event, establishing uniformity over all maximisers.

### 5. Older form and agreement with the statement

For a single truth j outside U, the Schur correction from U0 to U is bounded by ||c_l|| ||S_VV^(-1)|| ||c_j|| <=15r_n^2/c. Therefore ell_n=ell'_n+15r_n^2/c works at every U. The older rate implies r_n^2 sqrt(n/log n)=[r_n(n/log n)^(1/4)]^2 ->0, and also r_n->0. This proves §7 item 1 without an additional assumption.

L4 §0 matches STATEMENT §3.2 (L-R^b) and bridge (P7), including deterministic Q and H_l, all conditioning sets of size at most 15, the feasibility clause, and the strict budget. The full Form R theorem has additional large-set floors, T1-R, and lattice hypotheses; (P7) explicitly does not require them. Restricting c to (0,1] loses nothing for unit-diagonal covariance matrices. No unstated large-set floor or coefficient-independence assumption is needed.

### 6. Independent numerical stress test

I ran a separate, in-memory Python standard-library experiment (seed 246810; no scratch files). The first attempted NumPy version could not run because NumPy was unavailable; the executed replacement used elementary matrix algebra and random.gammavariate for Bartlett factors.

Take four design coordinates, truth 0 with theta=1, Q={0}, and H_l={0,l} for each outside column. The only nonzero off-diagonal covariances are Sigma_12=r and Sigma_01=d, where

    r = 1/log(log(n+exp(e))),  d = r sqrt(log n/n).

The fifth coordinate is independent noise of variance one. Exhausting every outside l and every conditioning subset of the other three design columns gives ell_n=d and localisation level r_n=r. The full covariance floor is 1-sqrt(r^2+d^2). Thus this sequence has genuinely slow localisation, ell_n/h_n=r->0, and fixed-size neighbourhoods. Visibility is bounded away from zero eventually. The ambient dimension is small, so it tests the algebra and perturbation mechanism rather than polynomial family counts.

For each n I generated 300 exact centered-Gaussian sample covariance draws using Wishart degrees of freedom n-1. I checked all 24 (l,U) pairs, with beta=-2, beta=2, and the random beta*=1/sqrt(S_hat_00). All 1,200 draws satisfied E_cov with A=1. No violation was found; the maximum observed |z_U-z_U0|/(ell_n+r_n h_n+h_n^2) over the entire experiment was 0.95518. The minimum population floor among the tested cases was 0.48137. The tested n values were 1000, 10000, 1000000, and 10000000000. Across the enumerated population cases the computed Schur identity error was zero at reported floating precision, and the largest |cross term|/(4ell_n) was 0.25842 (beta=2, s0=theta_hi=1).

These observations do not prove a uniform constant or an asymptotic statement. They exercise slow r_n, nonzero leak, and the random response coefficient. The supplied K8–K10 code and outputs were also inspected: K8 tests the identity, K9 uses pairwise population scales, and K10 has a very small mean shift. Their stated limitations in RESULTS §6 are appropriate; none substitutes for the tail proof above.

## Not checked

- The proofs of the accepted L0 toolkit statements, production-code equivalence, posterior results, lattice conditions, and L5/L6 are outside this review.
- I did not rerun the supplied R scripts (they write additional output files), reproduce their Monte Carlo tail frequencies, or simulate rare-event tails near the asymptotic leak boundary.
- I did not compare the historical templates line by line; L4's size- and rate-dependent steps were checked directly.
- Only the four principal source hashes noted above were individually checked, not every manifest entry.

The only file written by this review is `Theory_work/Wave3/W3-RM2/reviews/LC2A_L4_check_astra.md`.

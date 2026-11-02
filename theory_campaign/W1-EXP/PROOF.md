# W1-EXP — proofs

Notation of `Docs/Theory/theorems/00_COMMON.md`. Status words as in the BRIEF. Every result is a
candidate pending cross-family review. Throughout: the fixed-design Gaussian model of G,
`Y = C y^r = mu + C eps`, `mu = X theta*` centred, `eps ~ N_n(0, sigma^2 I)`; `y = Y/s_y`,
`||y||^2 = ||x_j||^2 = n-1`; blocks `C_b` deterministic in X with `|C_b| <= B <= 16`;
`nu = 0.01 + n/2`; `P_T` = orthogonal projection on span `X_T`, `P_empty = 0`.
For `U` a subset of a block: `RSS_U = ||(C - P_U) Y||^2`, `RSS^y_U = y'(I - P_U) y = (n-1) RSS_U/||Y||^2`.
For a within-block addition `(b, T, l)` (`T ⊆ C_b \ {l}`): `u_{T,l}`, `delta_{T,l}`, `Z_{T,l}`, `Delta_T`,
`v_T`, `x_{T,l} = (RSS_T - RSS_{T+l})/RSS_T = (delta_{T,l} + sigma Z_{T,l})^2 / RSS_T` exactly as in the
T22(iii) STATEMENT.md.

Named hypotheses used below.

* **G**: as in 00_COMMON.
* **R-lite(A, M)**: `p <= n^A` (A >= 1 fixed) and `||mu||^2 <= M n`. (Nothing else from R is used in §1.)
* **SE-blk(phi0)**: `lambda_min(X_U'X_U/(n-1)) >= phi0^2` for every nonempty `U ⊆ C_b`, every b.
  *Checkable*: by Cauchy interlacing SE-blk(phi0) holds iff `min_b lambda_min(R_{C_b}) >= phi0^2`
  (J eigenvalue computations on the actual blocks).
* **BO**: `X_{C_b}' X_{C_b'} = 0` for `b != b'`.

---------------------------------------------------------------------------------------------------

## 1. EXP′ is a theorem (all fixed designs with SE-blk; BO not needed)

**Theorem 1 (EXP′).** Status: **PROVED** (complete; checked line by line below).
Assume G, R-lite(A, M), SE-blk(phi0). Put `c_* = sigma^2 / (8(M + 2 sigma^2))` and
`kappa_EXP = (1 + phi0^{-2})/(2 phi0^2 (n-1)) + (n/2 + 0.01)(1.02 + 1/(n phi0^2))/(c_* n)`.
On an event `E_n` with `P_0(E_n) -> 1`, *every* within-block addition `(b, T, l)` satisfies

    log[ r_b(T+l) / r_b(T) ] = -(1/2) log(n+1) - nu log(1 - x_{T,l}) + R_{n,b,T,l},
    |R_{n,b,T,l}| <= kappa_EXP  (-> 0.52/c_* = 4.16 (M + 2 sigma^2)/sigma^2 + o(1)).

In particular EXP′ holds in its strict form, `rho_n = max |R| = O_{P_0}(1)`, with an explicit
deterministic bound on `E_n`. The decomposition into a determinant part and a Q part is exact
(Lemmas 1.1–1.3); probability enters only through the RSS floor (Lemma 1.4).

### Lemma 1.1 (Q_S versus RSS). For nonempty S with `lambda_min(G_S) >= phi^2 (n-1)`:
`Q_S = RSS^y_S + c_S` with `0 <= c_S <= 1 + 1/(n phi^2)`; and `c_empty = 0`.

*Proof.* `H_S = (n+1)(G_S + eps I)`, `eps = 1/(n+1)`. Put `t = z_S' G_S^{-1} z_S = y' P_S y <= ||y||^2 = n-1`
and `tau = t - z_S'(G_S + eps I)^{-1} z_S = eps z_S' G_S^{-1}(G_S + eps I)^{-1} z_S`. Since `G_S^{-1}` and `(G_S + eps I)^{-1}` commute and are positive definite,
`0 <= tau <= eps z' G^{-2} z <= eps t / lambda_min(G_S) <= eps/phi^2`
(using `t <= n-1` and `lambda_min(G_S) >= phi^2 (n-1)`).
Then `n z_S' H_S^{-1} z_S = (n/(n+1)) (t - tau)` and
`Q_S = (n-1) - (n/(n+1))(t - tau) = [(n-1) - t] + t/(n+1) + (n/(n+1)) tau`.
The bracket is `RSS^y_S` (y is centred and X_S centred, so `y'(I-P_S)y = (n-1) - t`). Hence
`c_S = t/(n+1) + n tau/(n+1) ∈ [0, (n-1)/(n+1) + n/((n+1)^2 phi^2)] ⊆ [0, 1 + 1/(n phi^2)]`. ∎

### Lemma 1.2 (determinant ratio). Let `T ⊆ C_b`, `l ∈ C_b \ T` and `lambda_min(G_{T+l}) >= phi^2(n-1)`.
Then `log D_{T+l} - log D_T = log(n+1) + eta_D` with `|eta_D| <= (1 + phi^{-2})/(phi^2 (n-1))`.

*Proof.* Write `G = G_T`, `g = X_T' x_l`, `a = ||x_l||^2 = n-1`, and `rho = a - g'G^{-1}g`, the Schur complement
of `G_{T+l}`; `rho >= lambda_min(G_{T+l}) >= phi^2(n-1)` (the inverse Schur complement is a diagonal entry of
`G_{T+l}^{-1}`, at most `1/lambda_min`). If `T` is nonempty, interlacing gives `lambda_min(G) >= phi^2(n-1)`.
By the Schur determinant formula,

    N := det H_{T+l}/det H_T = 1 + (n+1)[a - g'(G + eps I)^{-1} g],   eps = 1/(n+1),
    M := det(G_{T+l}+I)/det(G_T+I) = 1 + a - g'(G + I)^{-1} g.

For `e' > 0`: `0 <= g'G^{-1}g - g'(G+e'I)^{-1}g = e' g'G^{-1}(G+e'I)^{-1}g <= e' g'G^{-2}g <= e' (g'G^{-1}g)/lambda_min(G)
<= e' a /(phi^2 (n-1)) = e'/phi^2` (`g'G^{-1}g <= a`). Hence `N = (n+1)(rho + alpha_1)`, `M = rho + alpha_2` with
`alpha_1 ∈ [1/(n+1), (1+phi^{-2})/(n+1)]`, `alpha_2 ∈ [1, 1 + phi^{-2}]` (for T empty: `alpha_1 = 1/(n+1)`,
`alpha_2 = 1`). Since `D_{T+l}/D_T = N/M`,
`|log(N/M) - log(n+1)| = |log((rho+alpha_1)/(rho+alpha_2))| <= |alpha_1 - alpha_2|/rho <= (1+phi^{-2})/(phi^2(n-1))`. ∎

### Lemma 1.3 (exact decomposition). Under SE-blk(phi0), for every within-block addition, if all
`RSS^y_U > 0`:

    R_{n,b,T,l} = -(1/2) eta_D - nu [ log(1 + a_{T+l}/RSS^y_{T+l}) - log(1 + a_T/RSS^y_T) ],
    a_U := 0.02 + c_U ∈ [0.02, 1.02 + 1/(n phi0^2)].

Hence `|R_{n,b,T,l}| <= (1+phi0^{-2})/(2 phi0^2 (n-1)) + nu (1.02 + 1/(n phi0^2)) / min_{U ⊆ C_b} RSS^y_U`.

*Proof.* `log r_b(T+l) - log r_b(T) = -(1/2)(log D_{T+l} - log D_T) - nu[log(0.02 + Q_{T+l}) - log(0.02 + Q_T)]`
(the constant `C_n` cancels). By Lemma 1.1, `0.02 + Q_U = RSS^y_U + a_U`, so
`log(0.02+Q_{T+l}) - log(0.02+Q_T) = log(RSS^y_{T+l}/RSS^y_T) + log(1 + a_{T+l}/RSS^y_{T+l}) - log(1 + a_T/RSS^y_T)`,
and `RSS^y_{T+l}/RSS^y_T = RSS_{T+l}/RSS_T = 1 - x_{T,l}` (response scaling cancels). Insert Lemma 1.2.
Both bracketed logs lie in `[0, a/RSS^y]`, so their difference is at most the larger one in absolute value. ∎

### Lemma 1.4 (RSS floor). Under G and R-lite(A, M), with `|C_b| <= 16`:
`P_0( min_{b, U ⊆ C_b} RSS^y_U >= c_* n ) -> 1`, `c_* = sigma^2/(8(M + 2 sigma^2))`.

*Proof.* Fix `(b, U)` and let `W = span(X_U, mu)`, a subspace of range(C) (X and mu are centred) of
dimension `<= 17`. Since `P_W P_U = P_U` and `C P_U = P_U`, `C - P_W = (C - P_W)(C - P_U)`, a contraction applied to
`(C - P_U)Y`; thus `RSS_U >= ||(C - P_W) Y||^2 = ||(C - P_W) C eps||^2 = ||C eps||^2 - ||P_W eps||^2` (mu ∈ W, `P_W C = P_W`).
`||P_W eps||^2/sigma^2 ~ chi^2_{dim W}` and `E exp(||P_W eps||^2/(4 sigma^2)) = 2^{dim W/2} <= 2^{8.5}`. The number of
pairs `(b, U)` is `<= sum_b 2^{|C_b|} <= 2^{16} p <= 2^{16} n^A`. Markov + union bound:
`P(max ||P_W eps||^2 > L sigma^2 log n) <= 2^{24.5} n^{A - L/4} -> 0` for fixed `L > 4A`.
`||C eps||^2/sigma^2 ~ chi^2_{n-1}`, so w.p. -> 1, `||C eps||^2 >= (3/4) sigma^2 (n-1)` and `<= 2 sigma^2 (n-1)`.
Thus w.p. -> 1, simultaneously `RSS_U >= sigma^2(n-1)/2` for all `(b, U)` and
`||Y||^2 <= 2||mu||^2 + 2||C eps||^2 <= 2Mn + 4 sigma^2 n`. Then
`RSS^y_U = (n-1) RSS_U/||Y||^2 >= sigma^2 (n-1)^2 / (4n(M + 2 sigma^2)) >= c_* n` for `n >= 4`. ∎

*Proof of Theorem 1.* SE-blk gives the eigenvalue premise of Lemmas 1.1–1.2 for every `T+l ⊆ C_b`
(and for T). On the event of Lemma 1.4 all `RSS^y_U >= c_* n > 0`, and Lemma 1.3 gives
`|R| <= (1+phi0^{-2})/(2 phi0^2(n-1)) + (n/2 + 0.01)(1.02 + 1/(n phi0^2))/(c_* n) = kappa_EXP`. ∎

**Remarks.** (a) Only G, `p <= n^A`, `||mu||^2 <= Mn`, `|C_b| <= 16` and SE-blk are used — no BO, no s0, no
beta-min, no VIS/NL, no `lambda_min(R_{S0})`. (b) Under the weaker `lambda_min >= phi_n^2` with
`n^{1/2} phi_n^2 -> inf`, the same proof gives `|R| <= 0.52/c_* + o(1)`. (c) The remainder is genuinely O(1),
not o(1): its main part is `nu[a_T/RSS^y_T - a_{T+l}/RSS^y_{T+l}]`, of order `(1/2)(R^2_T - R^2_{T+l})/(1-R^2)`.
(d) Numerical check: `scripts/exp_family.py` records `max |R|` over all within-block additions; see REPORT §4.

### 1.5 How far it extends

* **Weak cross-block correlation / any cross-block structure.** Theorem 1 never uses cross-block structure:
  EXP′ is a *within-block* statement. It holds for every fixed design satisfying SE-blk.
* **iid Gaussian designs with the actual X-dependent partition.** (PROOF SKETCH; standard ingredients.) Let the rows
  of `X^r` be iid `N(0, Sigma)`, independent of eps, with `kappa_17(Sigma) := min_{|T|<=17} lambda_min(corr(Sigma)_T) >= 2 phi0^2`
  and `p <= n^A`. Because blocks have size `<= 16`, every set `T+l` lies in `{|T| <= 17}`, a family that does not depend
  on the partition. Gaussian covariance concentration and a union bound over `<= p^{17}` sets give
  `max_{|T|<=17} ||R_T - corr(Sigma)_T||_op = O_P(sqrt(log p/n)) -> 0`, so SE-blk(phi0) holds w.p. -> 1 for *every*
  partition into blocks of size `<= 16`, in particular the X-dependent one. Conditional on X (eps independent of X),
  Theorem 1 applies on that event; `||mu||^2/n -> theta' Sigma theta` gives R-lite. All six study covariances have
  `kappa_17 >= 0.15` (S4: `1 - 0.85`; S3: 0.3; S5: >= 0.3; S6: >= 0.1 for the 0.9 groups; S2: >= 1/3). Caveat:
  at n = 200, p = 1000 the concentration term `sqrt(17 log p / n) ~ 0.77` is not small, so SE-blk is an
  *empirical* matter there — but it is checkable on the actual blocks (min_b lambda_min(R_{C_b})).

---------------------------------------------------------------------------------------------------

## 2. Consequences for T22(iii) (favourable regime) — what is now unconditional

The locked T22(iii) proof (`Docs/Theory/proofs/T22iii_T16_start_aggregation/PROOF_v2.tex`, read line by line for
this run) uses its hypotheses as follows: EXP′ in Prop. un and Prop. en; NL_eta **only** in Lemma quad (to get
`max_{L_n} x = O_P(log n/n)`) and in §"Admissible rates" (to *supply* NL_avg(kappa)); VIS only in Prop. en; within-block
SE for residual directions; the truth property `supp theta* = S0` is **never** used — `S0` enters only through
`U_b* = S0 ∩ C_b`, the leakage family `L_n`, `u_n`, `e_n`, the size `s0` and feasibility.

**Proposition 2.1 (NL_eta -> NL_C in Lemma quad).** Status: **PROOF SKETCH** (one-constant change in a locked proof;
the changed lines are checked here). In Lemma quad replace NL_eta by
**NL_C**: `delta_{T,l}^2 <= C sigma^2 log n` on `L_n`, any fixed `C < inf`. The bound becomes
`max (delta + sigma Z)^2 <= sigma^2 (sqrt C + sqrt(2(A+eps0)))^2 log n`, still `O(log n)`, and every subsequent line of
Lemma quad (x = O_P(log n/n), `n x^2 = o_P(1)`, `d_n = o_P(1)`) is unchanged. Hence T22(iii) holds under
**G, R, SE-blk, VIS, NL_C, NL_avg(kappa)**, EXP′ being supplied by Theorem 1. NL_eta (with its threshold) remains only as
one sufficient condition for NL_avg(kappa).

**Proposition 2.2 (reference transfer, "T22(iii)°").** Status: **PROOF SKETCH** (verbatim transfer of a locked proof;
checked that no line uses `supp theta* = S0`). Let `S°` be a deterministic feasible set of fixed size `s°`, put
`U_b° = S° ∩ C_b`, define `L_n°`, `u_n°`, `e_n°`, VIS°, NL_C°, NL_avg°(kappa) by replacing `S0` with `S°`. Under
G, R-lite, SE-blk, VIS°, NL_C°, NL_avg°(kappa):

    1 - pi_0(S°) = O_{P_0}( 2^B sqrt(log n) n^{-kappa} ),   kappa = 1/2 allowed under exact zero leakage.

The aggregation step is wave-1 T22(i) with reference `S°` (it holds for every feasible reference).

**Block-projection form of the hypotheses (checkable).** For a reference `S°` define per block

    lambda_b(S°) = ||(P_{C_b} - P_{U_b°}) mu||^2          (in-block signal not carried by S°),
    g_b(S°)      = min_{U ⊆ C_b, U_b° ⊄ U} ||(P_{U ∪ U_b°} - P_U) mu||^2   (visibility gain).

*Lemma 2.3.* Status: **PROVED**. (i) For `(b,T,l) ∈ L_n°`: `|delta_{T,l}| <= sqrt(lambda_b(S°))`. Hence
`max_b lambda_b(S°) <= C sigma^2 log n` implies NL_C°; `<= eta sigma^2 log n` implies NL_eta°; `lambda_b(S°) = 0` for all b
(exact zero leakage) implies `E_{T,l} = 0` on `L_n°`, i.e. NL_avg°(1/2). (ii) VIS° is `min_b g_b(S°) >= M_n^V v log n`
and, since `v_U <= sigma^2 + 2M`, it is implied by `min_b g_b(S°) >= M_n (sigma^2 + 2M) log n`, `M_n -> inf`.

*Proof.* (i) `u = u_{T,l} ∈ span X_{C_b}` and `u ⟂ span X_T`, so `delta = u'mu = u' P_{C_b} mu = u'(P_{C_b} - P_T) mu`.
Since `span X_{U_b°} ⊆ span X_T ⊆ span X_{C_b}`, `(P_{C_b} - P_T)` is the restriction of `(P_{C_b} - P_{U_b°})` to a
subspace and `||(P_{C_b} - P_T)mu|| <= ||(P_{C_b} - P_{U_b°})mu||`. Cauchy–Schwarz with `||u|| = 1`. (ii) is the definition
together with `Delta_U <= ||mu||^2/(n-1) <= 2M` (n >= 2). ∎

The quantity `P_{C_b} mu = X_{C_b} gamma_b`, `gamma_b = G_{C_b}^{-1} X_{C_b}' mu`, is the *block projection* of the
signal. `lambda_b(S°) = 0` iff `supp gamma_b ⊆ U_b°`. So the start concentrates on the **block-projection support**
`S^bp = ∪_b supp gamma_b` whenever its coefficients are visible (VIS) — and on `S^bp` minus small coordinates
whenever the dropped coordinates leave `lambda_b = O(log n)`.

**Theorem 2 (T22(iii) unconditional in the BO benchmark — favourable regime).** Status: **PROOF SKETCH**
(rests on Theorem 1 [PROVED], Lemma 2.3 [PROVED] and the locked T22(iii) proof with Prop. 2.1).
Assume G, R (s0 fixed, `p <= n^A`, `||mu||^2 <= Mn`, s0 <= K eventually), SE-blk(phi0), **BO**, and the block beta-min
**BM-blk**: `min_{j ∈ S0} theta*_j^2 >= M_n (sigma^2 + 2M) log n / (phi0^2 (n-1))`, `M_n -> inf`. Then

    1 - pi_0(S0) = O_{P_0}( 2^B sqrt(log n) n^{-1/2} ).

*Proof.* EXP′: Theorem 1. BO gives `P_{C_b} mu = X_{U_b*} theta*_{U_b*}` (the other blocks' columns are orthogonal
to span `X_{C_b}`), so `lambda_b(S0) = 0` for every b: NL_0 and NL_avg(1/2) by Lemma 2.3(i). VIS: for
`U_b* ⊄ U ⊆ C_b`, `(P_{U ∪ U*} - P_U) mu = (P_{U ∪ U*} - P_U) X_{U*} theta*_{U*} = (I - P_U) X_{U* \ U} theta*_{U* \ U}`,
whose squared norm is `>= lambda_min(G_{U ∪ U*}) ||theta*_{U* \ U}||^2 >= phi0^2 (n-1) min_j theta*_j^2
>= M_n (sigma^2 + 2M) log n >= M_n v_U log n`. Apply Prop. 2.1 (with C = 0) — the locked T22(iii). ∎

**Extensions of Theorem 2.** (a) *Weak cross-block correlation* (PROOF SKETCH): with `mu_{-b} = mu - X_{U_b*} theta*_{U_b*}`,
`lambda_b(S0) = ||(P_{C_b} - P_{U_b*}) mu_{-b}||^2 <= ||P_{C_b} mu_{-b}||^2 <= (n-1) |C_b| s0 ||theta*||_inf^2
max_{j ∈ C_b, k ∈ S0 \ C_b} r_jk^2 / phi0^2`; so `max |r_{cross}| <= c sqrt(log n / n)` gives NL_C, and VIS follows
from BM-blk by the triangle inequality `sqrt(g) >= phi0 sqrt(n-1) theta_min - sqrt(lambda_b)`. NL_avg(kappa) then
needs either NL_eta (small c) or a direct average bound. (b) *iid Gaussian designs with population BO*
(S3, S4, S6, whose groups are independent; the actual blocks are unions of whole groups w.p. -> 1): sample
cross-block correlations are `O_P(sqrt(log p/n))` so NL_C holds w.p. -> 1, but NL_eta (a maximum over ~p
comparisons) fails at fixed SNR because `max_l delta_{∅,l}^2 ≈ 2A (theta'Sigma theta) log n`. The average condition is
the right one; §4.3 sketches a direct route giving kappa = 1/2. Status: PROOF SKETCH.

**Theorem 6 (direct start concentration under exact zero leakage; no truncation, no locked-proof transfer).**
Status: **PROVED**. Let `S°` be deterministic, feasible, `|S°| = s` fixed. Assume G, R-lite(A, M), SE-blk(phi0), and
* **ZL(S°)** (exact zero leakage): `lambda_b(S°) = 0` for every block, i.e. `P_{C_b} mu ∈ span X_{U_b°}`;
* **SPREAD(Delta_0)**: `min_b ||(I - P_{C_b}) mu||^2/(n-1) >= Delta_0 > 0` (no single block carries all the signal);
* **VIS-lin(c_V)**: `min_b g_b(S°) >= c_V n` with fixed `c_V > 0` (empty minimum = +inf).
Then `1 - pi_0(S°) = O_{P_0}(2^B n^{-1/2})` (in particular `pi_0(S°) -> 1`), and `e_n° = O_P(e^{-c n})` for some c > 0.

*Proof.* Step 0 (events). Let `E_n` be the event of Lemma 1.4 intersected with: (i) `||Y||^2 <= C_R n`,
`C_R = 2M + 4 sigma^2`; (ii) `sup_{b, U ⊆ C_b} |RSS_U - (n-1) v_U| <= n^{3/4}`; (iii) `max ||(P_V - P_U) eps||^2 <= L sigma^2 log n`
over nested within-block pairs `U ⊂ V = U ∪ U_b°` (L > 4A fixed). (ii) holds w.p. -> 1 because
`RSS_U - (n-1)v_U = 2 r_U' eps + (||C eps||^2 - (n-1) sigma^2) - ||P_U eps||^2`, `r_U = (I - P_U) mu`, `||r_U||^2 <= Mn`:
the first term is `O_P(sqrt(n log n))` uniformly by Gaussian tails and a union bound over `<= 2^16 n^A` sets, the second
`O_P(sqrt n)`, the third `O_P(log n)` uniformly (as in Lemma 1.4). (iii) as in Lemma 1.4 (ranks <= 16, `<= 2^16 n^A` pairs).

Step 1 (u°). Fix `l ∉ S°`, `b = b(l)`, `U_b° ⊆ T ⊆ C_b \ {l}`. By ZL and Lemma 2.3(i), `delta_{T,l} = 0`, hence
`x = sigma^2 Z^2/RSS_T`, `Z = Z_{T,l} ~ N(0,1)`, and `x/(1-x) = sigma^2 Z^2 / RSS_{T+l}`. Also `Delta_{T+l} >= Delta_0`
(`span X_{T+l} ⊆ span X_{C_b}`). On `E_n`, `RSS_{T+l} >= (n-1)(sigma^2 + Delta_0) - n^{3/4}`, so for `n >= n_0`
`nu x/(1-x) <= a Z^2`, `a := (1/2) * sigma^2 / (sigma^2 + Delta_0/2) < 1/2`. Theorem 1 then gives, on `E_n`,
`r_b(T+l)/r_b(T) <= (n+1)^{-1/2} e^{kappa_EXP} exp(a Z_{T,l}^2)` (using `-log(1-x) <= x/(1-x)`). Bounding the max over T
by the sum,
`u_n° <= (n+1)^{-1/2} e^{kappa_EXP} V_n`, `V_n := (p - s)^{-1} sum_{l ∉ S°} sum_{T} exp(a Z_{T,l}^2)`.
`E V_n <= 2^B (1 - 2a)^{-1/2}` (linearity; no independence needed), so `V_n = O_P(2^B)` by Markov and
`u_n° = O_P(2^B n^{-1/2})` (the event `E_n^c` has vanishing probability).

Step 2 (e°). Fix b, `U ⊆ C_b` with `a = |U_b° \ U| > 0`, `V = U ∪ U_b°`. Add the missing members of `U_b°` one at a
time; the logs telescope (`1 - x_k = RSS_{T_k}/RSS_{T_{k-1}}`), and Theorem 1 gives on `E_n`
`log[r_b(V)/r_b(U)] >= -(a/2) log(n+1) - a kappa_EXP + nu log(RSS_U/RSS_V)`. Now
`RSS_U - RSS_V = ||(P_V - P_U) Y||^2` and `(P_V - P_U)Y = (P_V - P_U)mu + (P_V - P_U)eps` (`P_V - P_U ≼ C`); by VIS-lin and (iii),
`||(P_V - P_U)Y||^2 >= (sqrt(c_V n) - sqrt(L sigma^2 log n))^2 >= c_V n/2` for large n. With `-log t >= 1 - t` and
`RSS_U <= ||Y||^2 <= C_R n`: `nu log(RSS_U/RSS_V) >= (n/2)(c_V/2)/C_R`. As `a <= 16`,
`[r_b(U)/r_b(V)]^{1/a} <= (n+1)^{1/2} e^{kappa_EXP} exp(-n c_V/(64 C_R))`, so `e_n° <= 2 n^A (n+1)^{1/2} e^{kappa_EXP} e^{-n c_V/(64 C_R)}`.

Step 3. Wave-1 T22(i-a,b) with reference S°: on `{u_n° < 1}`, `1 - pi_0(S°) <= (s+1) u_n°/(1 - u_n°) + s e_n°`.
Steps 1–2 finish the proof. ∎

**Remarks.** (1) The rate has no `sqrt(log n)`: exact zero leakage plus SPREAD keeps the exponent `a < 1/2` integrable.
(2) In the BO benchmark with `S° = S0`, ZL(S0) is automatic; SPREAD holds whenever the true variables meet `>= 2`
blocks; VIS-lin holds under fixed beta-min and SE-blk. So Theorem 6 also gives, under a *fixed* beta-min `min_{S0}|theta_j| >= b_0 > 0` (which yields VIS-lin), the favourable-regime statement
`1 - pi_0(S0) = O_P(2^B n^{-1/2})` in BO **without** the locked T22(iii) (when the truth meets >= 2 blocks).

---------------------------------------------------------------------------------------------------

## 3. T27(i) from bounded leakage along the chain (masked regime)

**Hypotheses.**
* **H1** (fixed chain): as in the T27(i) STATEMENT: deterministic `S^(0) ⊂ … ⊂ S^(c) = S0`, `S^(i+1) = S^(i) + l_i`,
  fixed s = |S^(0)|, c >= 1, all feasible; `b_i = b(l_i)`, `T_i = S^(i) ∩ C_{b_i}`.
* **SE-chain(phi0)**: `lambda_min(R_{T_i + l_i}) >= phi0^2` for i < c (implied by SE-blk).
* **CL(L_n)** (chain leakage): `max_{i<c} |delta_{T_i, l_i}| <= L_n sigma`. Fixed `L_n = L` is the *bounded-leakage*
  case; `L_n -> inf` is allowed in part (b).
* **H3** (unchanged): `P_0(pi_0(S^(0)) >= c0) -> 1`; or **H3-T22**: the hypotheses of Prop. 2.2 with `S° = S^(0)`.

**Theorem 3 (two-sided ratio law).** Status: **PROVED**. Under G, R-lite, SE-chain, H1, CL(L_n): w.p. -> 1, for all i < c,

    -1 - kappa_EXP <= E_{n,i} := log[r_{b_i}(T_i+l_i)/r_{b_i}(T_i)] + (1/2) log n
                   <= kappa_EXP + nu sigma^2 (L_n + |Z_i|)^2 / RSS_{T_i+l_i},

with `Z_i = Z_{T_i,l_i} ~ N(0,1)` and `RSS_{T_i+l_i} >= sigma^2 (n-1)/2` on the event, so the upper bound is
`<= kappa_EXP + 1.01 (L_n + |Z_i|)^2` for n >= 400. (a) If `L_n = L` is fixed, `max_i |E_{n,i}| = O_{P_0}(1)`: **H2 holds**.
(b) In general `E_{n,i} ∈ [-O_P(1), O_P(1) + 1.01(L_n + O_P(1))^2]` — a two-sided law with multiplier `e^{O(L_n^2)}` on
the upper side only.

*Proof.* Theorem 1 restricted to the c chain additions needs SE only on `T_i + l_i` (Lemmas 1.1–1.3) and the RSS
floor (Lemma 1.4, which needs no SE); so on the event `E_n`,
`E_{n,i} = (1/2) log(n/(n+1)) - nu log(1 - x_i) + R_i`, `|R_i| <= kappa_EXP`. Lower side: `-nu log(1-x) >= 0` and
`(1/2) log(n/(n+1)) >= -1`. Upper side: `-log(1-x) <= x/(1-x)` and
`x/(1-x) = (RSS_T - RSS_{T+l})/RSS_{T+l} = (delta + sigma Z)^2/RSS_{T+l}`
(`RSS_T - RSS_{T+l} = ||(P_{T+l} - P_T) Y||^2 = (u'Y)^2 = (u'mu + u'eps)^2`, `u ∈ range C`). Lemma 1.4's proof gives
`RSS_{T+l} >= sigma^2(n-1)/2` on `E_n`, and `|delta + sigma Z| <= sigma(L_n + |Z|)`. So
`-nu log(1-x_i) <= (n/2 + 0.01)(L_n + |Z_i|)^2 / ((n-1)/2) <= 1.01 (L_n + |Z_i|)^2` for n >= 400. Each `Z_i` is exactly
N(0,1) (deterministic unit vector `u_{T_i,l_i}`), and `max_{i<c} |Z_i| = O_P(1)` (c fixed). ∎

**Theorem 4 (T27(i) from bounded chain leakage).** Status: **PROVED** given H3 (and **PROOF SKETCH** when H3 is
discharged through Prop. 2.2). Under G, R-lite, SE-chain, H1, CL(L) with L fixed, H3, and `p >= 2(s + c)`:

    log pi_0(S0) + c log p + (c/2) log n = O_{P_0}(1);   i.e. pi_0(S0) = p^{-c} n^{-c/2} e^{O_P(1)}.

Under CL(L_n) with `L_n -> inf`: `-O_P(1) <= log pi_0(S0) + c log p + (c/2) log n <= O_P(1) + 1.01 c (L_n + O_P(1))^2`.
In particular `L_n^2 <= eta log n` gives `pi_0(S0) <= p^{-c} n^{-c(1/2 - 1.01 eta - o(1))}` (masking persists iff
`eta < 1/2.02`, a sufficient condition).

*Proof.* T22(ii-a) (wave 1, locked) with reference `S^(0)` and telescoping along the chain (each step changes only
block `b_i`, from `T_i` to `T_i + l_i`):
`log pi_0(S0) = log pi_0(S^(0)) + log[w(s+c)/w(s)] + sum_{i<c} log[r_{b_i}(T_i+l_i)/r_{b_i}(T_i)]`.
`w(k+1)/w(k) = (k+1)/(2p-k-1)`, so `log[w(s+c)/w(s)] + c log p = sum_{i<c} log[(s+i+1) p/(2p-s-i-1)]`, which lies in
`[c log((s+1)/2), c log(2(s+c))]` for `p >= 2(s+c)`: bounded. The sum of table ratios equals
`-(c/2) log n + sum_i E_{n,i}`, bounded in probability by Theorem 3. `log pi_0(S^(0)) ∈ [log c0, 0]` w.p. -> 1 by H3. ∎

**Limit law (refinement).** Status: **PROOF SKETCH**. If moreover `delta_{T_i,l_i} = 0` exactly, `T_i = ∅` for all i,
`pi_0(S^(0)) -> 1` in probability, and the chain directions `x_{l_i}` are mutually orthogonal, then

    log pi_0(S0) + c log p + (c/2) log n  ->_d  sum_{i<c} log((s+i+1)/2) + sum_{i<c} (sigma^2/(2 v_∅)) chi^2_{1,i},

`v_∅ = sigma^2 + ||mu||^2/(n-1)` (independent chi-squares). Sketch: `nu x_i = nu sigma^2 Z_i^2 / RSS_∅ -> sigma^2 Z_i^2/(2 v_∅)`
(RSS_∅/(n-1) -> v_∅), `nu x_i^2 -> 0`, and the EXP′ remainder tends to 0 at T = ∅ because
`a_∅ = 0.02`, `a_{l} = 0.02 + R^2_{l} + O(1/n)` with `R^2_l = x_l'y^2/(n-1)^2 = O_P(1/n)`, and `eta_D = O(1/n)`.

---------------------------------------------------------------------------------------------------

## 4. One design family carrying both: masked T27 start AND near-truth T22(i) mass

### 4.1 The linked-hub family LH (S3/S4/S6 groups + one suppressor edge per masked variable)

Population correlation `Sigma` on `p = G g` variables, `G` groups `C_1..C_G` of size `g`:
* within group h: equicorrelation `rho_h ∈ [rho_-, rho_+] ⊂ (0,1)` (S3: 0.7; S4: 0.85; S6: 0.4–0.9);
* each group has a hub `j_h` (the position of its potential true variable);
* groups independent (S3/S4/S6) **except** c disjoint *linked pairs* `(a_i, b_i, psi_i)`, `|psi_i| <= psi_+ < 1`, with the
  rank-one cross-covariance through the hubs

      Sigma[C_a, C_b] = psi Sigma[C_a, j_a] Sigma[j_b, C_b]
      (corr(j_a, j_b) = psi; corr(j_a, k) = psi rho_b, k ∈ C_b \ j_b; corr(k, k') = psi rho_a rho_b off-hub).

  Equivalently the two groups are conditionally independent given the hub pair: a two-node "tree" link.
* truth: `theta_{j_{a_i}} = beta_i != 0`, `theta_{j_{b_i}} = -psi_i beta_i` (the **suppressor**), and `theta_{j_h} = beta_h != 0`
  for a fixed set of further unlinked "visible" groups; all other coefficients 0. `s0 = 2c + #visible`, fixed.
  `S° := S0 \ M`, `M = {j_{b_1}, …, j_{b_c}}` (the masked set), `s = s0 - c`.

**Lemma 4.1 (population algebra).** Status: **PROVED**.
(a) `lambda_min(Sigma) >= (1 - psi_+)(1 - rho_+)`.
(b) `Cov(X_{C_{b_i}}, mu) = 0`: every masked group is orthogonal to the signal.
(c) `Cov(X_{C_{a_i}}, mu) = beta_i (1 - psi_i^2) Sigma[C_{a_i}, j_{a_i}]`, so the block projection of mu on `C_{a_i}` is
    `beta_i(1 - psi_i^2) x_{j_{a_i}}`; on a visible group h it is `beta_h x_{j_h}`; on any other group it is 0.
    Hence the population block-projection support is exactly `S°` (when blocks = groups).

*Proof.* (a) For `(x, y)` on a linked pair, `x'Sigma_aa x + y'Sigma_bb y + 2 psi (x'Sigma_aa e_a)(e_b'Sigma_bb y)
>= ||x||_a^2 + ||y||_b^2 - 2|psi| ||x||_a ||y||_b >= (1 - |psi|)(||x||_a^2 + ||y||_b^2)` (Cauchy–Schwarz in the
`Sigma_aa`-inner product, `e_a'Sigma_aa e_a = 1`), and `lambda_min` of an equicorrelated block is `1 - rho_h`; unlinked
groups are independent. (b) `Cov(X_{C_b}, mu) = beta Sigma[C_b, j_a] - psi beta Sigma[C_b, j_b]` and
`Sigma[C_b, j_a] = psi Sigma[C_b, j_b] Sigma[j_a, j_a] = psi Sigma[C_b, j_b]`. (c) `Sigma[C_a, j_b] = psi Sigma[C_a, j_a]`; other
groups are independent of both hubs. ∎

**Lemma 4.2 (the method partition).** Status: **PROVED** (for the exact-Gram realisation; deterministic).
If `R = Sigma`, `|psi_i| < min(rho_{a_i}, rho_{b_i})` and `g <= B < 2g`, then the v3 partition (complete linkage on
`1 - |r|`, R13 ties, top-down cut, next-fit packing) has blocks exactly equal to the groups.

*Proof.* Complete-linkage distance between two sub-clusters of group h is `1 - rho_h`. Any cluster pair meeting two
different groups has distance `>= 1 - |psi|` if the groups are linked, `= 1` otherwise (cross correlations are
`psi, psi rho, psi rho^2` or 0). Since `1 - |psi_i| > 1 - rho` for both groups of a linked pair, every group
completes (as a cluster of size g) before any of its members merges outside it: the dendrogram contains each
group as a subtree. The top-down cut splits only nodes of size > B; nodes that are unions of `>= 2` whole groups have
size `>= 2g > B` and are split, groups (size `g <= B`) are retained. Next-fit packing: a bin holding one group
cannot take another (`2g > B`). ∎

(For `p <= 20` one has `B = floor(sqrt p) = 4` for `n >= 16`: `g = 3` or `4` works. For growing p, B -> 16 and
`9 <= g <= 16` works; at the study's `B = 14` packing *would* merge two groups of 5 into one block, and if the
linked pair is merged the masking disappears — see REPORT "what fails".)

### 4.2 The joint theorem on LH (exact-Gram realisation, p <= n - 1)

Realisation: `X'X = (n-1) Sigma` exactly for every n (any centred orthonormal frame), so all population
statements hold in-sample *exactly*. Regime R1 with `p = p_n <= n - 1` (G may grow; c, s0, the betas, psis and rhos fixed;
`g <= B_n < 2g` for all large n).

**Theorem 5 (masked regime on LH; input for T38(b)).** Status: parts (a), (b), (c), (e): **PROVED** here from
Theorems 1, 3, 4, 6, Lemmas 2.3, 4.1, 4.2 and the locked wave-1 T22(i), T22(ii-a), T22(iv-b); part (d) by citation of
the locked T03 (its hypotheses verified below); the limit-law refinement in (b) is a PROOF SKETCH. Under G, `sigma^2 > 0` fixed:

(a) **Near-truth start mass (T22(i) at S° ∈ R_0).** `1 - pi_0(S°) = O_{P_0}(2^B n^{-1/2})`; hence
    `pi_0(R_d) >= pi_0(R_0) >= pi_0(S°) = 1 - O_P(2^B n^{-1/2})` for every `d >= 0`: `b_n -> 1`.
(b) **Masking (T27(i)).** `pi_0(S0) = p^{-c} n^{-c/2} e^{O_P(1)}`, with the limit law of §3 (the masked hubs are
    mutually independent and orthogonal).
(c) **Regime.** VIS fails at reference S0 (block `C_{b_i}`, `U = ∅`: gain `||P_{x_{j_{b_i}}} mu||^2 = 0`), so the
    favourable branch T22(iii) does not apply — consistently, (b) gives `pi_0(S0) -> 0`.
(d) **Posterior.** `1 - pi(S0) = O_P(sqrt(log n/n))` (locked T03 under G, R, SE, BM-∞: SE from Lemma 4.1(a),
    `lambda_min(R_{S0}) >= lambda_min(Sigma)`, fixed nonzero betas give BM-∞, `||mu||^2/n <= theta'Sigma theta`).
(e) **Bridge endpoints.** The start is masked, the target is not: `pi_0(S0) -> 0`, `pi(S0) -> 1`, while
    `pi_0(R_0) -> 1`. By T22(iv-b) `inf_phi q_phi(S0) >= pi_0(S0)` only — the bridge must transport mass
    from `S° ∈ R_0` to `S0` (c missing-true additions), which is what T38(b) has to handle.

*Proof of (a).* Blocks = groups (Lemma 4.2). Reference `S°`: by Lemma 4.1(b)(c) (exact in-sample, since `X'X = (n-1)Sigma`),
`P_{C_b} mu ∈ span X_{U_b°}` for every block: ZL(S°). SPREAD: `||(I - P_{C_b})mu||^2/(n-1) = theta'Sigma theta - gamma_b'Sigma_bb gamma_b`,
which is `>= min{beta_i^2 psi_i^2 (1 - psi_i^2), beta_h^2, ...} > 0` because every block misses at least one linked pair's or
visible group's contribution (the pair contributes `beta^2(1-psi^2)` to `theta'Sigma theta`, of which block `C_a` carries
`beta^2(1-psi^2)^2`); it is a fixed positive number. VIS-lin: on `C_{a_i}`, `U_b° = {j_a}` and for
`j_a ∉ U ⊆ C_a`: `(P_{U+j_a} - P_U) mu = (P_{U + j_a} - P_U) X_{C_a} gamma = beta(1-psi^2)(I - P_U) x_{j_a}` with squared norm
`>= beta^2 (1-psi^2)^2 lambda_min(G_{U + j_a}) >= beta^2(1-psi^2)^2 (1-rho_+)(n-1)`; on visible groups the same with
`beta_h^2`; on other groups `U_b° = ∅` (vacuous). So `c_V = (1 - rho_+) min{beta_i^2(1-psi_i^2)^2, beta_h^2}`. SE-blk from Lemma 4.1(a). Theorem 6. ∎
*Proof of (b).* Chain: `S^(0) = S°`, add `j_{b_1}, …, j_{b_c}` in order; each `C_{b_i}` contains no other true variable,
so `T_i = ∅` and `delta_{∅, j_{b_i}} = x_{j_{b_i}}' mu / sqrt(n-1) = 0` (Lemma 4.1(b)): CL(0). H3 holds with `c0 = 1/2` by (a).
Theorem 4. ∎

### 4.3 iid Gaussian realisation (closest to the study's generators) — PROOF SKETCH

Rows iid `N(0, Sigma_LH)` (as `gen_dev_data.R` does with `scenario_covariance`), `p <= n^A` allowed (p > n included).
(i) Sample correlations are uniformly within `O_P(sqrt(log p/n))` of Sigma; the margins in Lemma 4.2 are strict, so
blocks = groups w.p. -> 1. (ii) SE-blk w.p. -> 1 (§1.5). (iii) Chain: `x_{j_b}` and `mu` are jointly Gaussian and
uncorrelated, hence independent, so `delta_{∅, j_b} ~ N(0, ||mu||^2/(n-1))` given mu: CL(L) holds w.p. >= 1 - eps for
L = L(eps): Theorem 4 applies conditionally on X. (iv) Near-truth mass: for a null or masked l in block b and
`T ⊇ U_b°`, zero population partial covariance gives `x_l = X_T a + w_l` with `w_l` independent of `(X_T, mu, eps)`, so
`x_{T,l} ~ Beta(1/2, (n-|T|-2)/2)` *exactly*, independent of Y. Then
`E[(1-x)^{-nu} 1{x <= h_n^2/n}] = O(h_n)` while `P(max x > h_n^2/n) -> 0` (union over `p 2^B` comparisons), giving
`u_n° = O_P(2^B sqrt(log n) n^{-1/2})` *without* NL_eta (note `E(1-x)^{-nu} = inf` because `nu > (n-|T|-2)/2`:
the truncation is essential). VIS° holds w.p. -> 1 by sample-covariance consistency. So (a), (b), (d) persist.
Still to be written in full: the conditioning argument for the leakage family uniformly over the X-dependent
partition (handled by working on the event "blocks = groups", which is X-measurable).

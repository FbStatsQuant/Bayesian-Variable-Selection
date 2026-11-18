model: claude-opus-5-5 (claudeAgent_personal, high); round=R1; seat=Opus E2 check

# W3-FAMC — independent check of Example E2 (`W3-RM2:Ex-PolyR@1.0.3`), scope = what FAMC consumes

Instance checked: Sigma_lk = rho^{|l-k|}, fixed rho in (-1,1), pi = id, alpha = 3, b = 1/4,
locality exponent varrho = (1/2 - b)/30 = 1/120, unit diagonal, spectrum in
[c, C] = [(1-|rho|)/(1+|rho|), (1+|rho|)/(1-|rho|)], K_dec = sup_d |rho|^d (1+d)^3 < inf.
(V-R)/PTV(a0) is out of scope. I re-derived every step below by hand; I did not author the text.

Abbreviations: L6 = `Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md`; POLY = `Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md`;
RM2S = `Theory_work/Wave3/W3-RM2/STATEMENT.md`; RMS = `Theory_work/Wave3/W3-RM/STATEMENT.md`;
L5R = `Theory_work/Wave3/W3-RM2/lemmas/L5_formR.md`; GROW-L5 = `Theory_work/Wave1C/C-GROW/lemmas/L5_instances.md`.

## Verdict table

| item | verdict | one-line reason | file:line |
|---|---|---|---|
| Lemma BC (`W2-LOC2:Lemma-BC@1.0.0`), M = 15 | PASS | cofactor path argument correct (i has in-degree 0, j out-degree 0, path length 1 <= h <= m-1; edge with d >= d(i,j)/h; (1+d/h)^-a <= h^a (1+d)^-a); det B >= c^m; 2x2 Schur step det H >= 1/C^2; K_15 formula matches m = |U|+2 <= 17; any positions | POLY:78-109; L6:45-56 |
| Lemma IR (`W2-LOC2:Lemma-IR@1.0.0`), alpha = 3 | PASS | band truncation + column-specific exponential weight + Schur test + Neumann (sigma_min(A_B+E) >= c/4) + resolvent error (2/c^2)H1 B^{1-a}; B ~ d/(M1 log(2+d)) gives f(d); constants depend only on (c,K_dec,alpha); summability of f needs alpha > 2 (alpha = 3: f = (1+d)^-2 log^2(2+d)) | POLY:118-167 |
| (P3) regression bound | PASS | beta_T(l)_v = -(B^-1)_vl/(B^-1)_ll, (B^-1)_ll = 1/Var(W_l given W_T) >= 1 (unit diagonal); uniform over all T, any l | POLY:162-167 |
| Identity beta_A = beta_T,A + B_AA^-1 B_AE beta_T,E | PASS | rows A of Sigma_TT beta_T = Sigma_Tl; sign correct; A = empty case consistent | L6:79 |
| (0.1) l1 bound, L(r) = (1+JD)F(r) | PASS | column-sum norms: inverse <= J (IR, <= 2 sites per distance), rectangular block <= D; E = {v in T: d(l,v) > r} because T is a subset of Q (lattice) | L6:76-84 |
| (0.2) variance inequality | PASS | e_A - e_T in span W_T, orthogonal to e_T; Var of combination <= (l1 norm)^2 since sd(W_v) = 1; Var(l given T) >= c | L6:86-95 |
| r = floor(sqrt(log n)) consequences | PASS | abs(N_l) <= 2r = o(log n); L(r) -> 0; log(q+1) = O(log n) so L(r)^2 log(q+1) = o(log n); frames <= p 2^{2r} = p n^{o(1)} | L6:97-101, :233-240 |
| Leak radius R_Q, (2.2) | PASS | gamma = 1/6; varpi_n = K_15 (1+R_Q)^-3 <= K_15 n^{-1/2}(log n)^{1/4}; varpi_n sqrt(n/log n) <= K_15 (log n)^{-1/4} -> 0 | L6:176-201 |
| (L-size^b), b = 1/4 | PASS | abs(Q) <= 4 s0 R_Q + 34 s0 = O(n^{1/6}) <= n^{1/4} eventually (b >= gamma) | L6:183-187, :221 |
| (L-feas) vs K = min(p, floor(n/2)) | PASS | branch 1: p >= 2q+32s0+1 and floor(n/2) >= 2q+32s0+1 eventually (q = o(n)), so K >= 2q+32s0+1 >= q; branch 2: Q = [p], p <= 2abs(Q0)+32s0 = o(n) so K = p = q; both branches uniform in n >= n0 | L6:180, :221-223; RM2S:178 |
| (L-gain-R) | PASS | for l not in Q, j in S0 minus U: l, j not in U, distinct, d(l,j) >= R_Q+1; BC with abs(U) <= 15 gives <= varpi_n for the full U (as v1.4 requires, not only U0); vacuous in branch 2 | L6:224-225; RM2S:180-181 |
| (L-loc-R) | PASS | H_l = r0-neighbourhood of {l} union S0, r0 = ceil(log n); l not in U so l not in U0; v in U minus H_l is not in U0, has d(v,l), d(v,j) > r0; BC with U0 gives r_n = K_15 (1+r0)^-3 -> 0; abs(H_l) <= (s0+1)(2r0+1) <= n^{1/120} eventually; 15 varrho + b = 3/8 < 1/2 | L6:226-232; RM2S:182-185 |
| (T1-R) | PASS | global floor lambda_min(Sigma) >= c gives phi^2 = psi_n = c, psi_n sqrt(n)/(log n)^{3/2} -> inf; no upper bound needed | L6:213-216; RMS:126-133 |
| (FL-R) | PASS | interlacing from the global spectrum, all S incl. Q union {l} | L6:217-218 |
| (D-loc^b) and match to `W3-RM2:D-to-W` | PASS | L5R Lemma D-loc^b needs: N_l subset Q minus {l}, abs(N_l) = o(log n), L_n^2 log(q+1) = o(log n), eta_n -> 0, over pairs (T,l) with T subset Q, l not in T, beta zero-padded to Q; frames = single functionals psi_{N,l}, N subset N_l (m0 = 1), atoms e_v, v in Q (variance 1), no latent extension. E2 supplies exactly these with L_n = L(r), eta_n = L(r)^2/c; (N0^b), (N1) from (L-size^b), (L-feas), (FL-R) | L6:233-245; L5R:108-117; RM2S:194-202 |
| (W-R) via (D-loc^b) => (D-R^b) => (W-R) | PASS (conditional on the stipulated RM2 implication) | spectral event W^0_n contains E_W is L5R (S2) (q <= n^b, b < 1/2); E2's remark at :241-245 agrees | L6:240-245; L5R:19-22 |

No GAP and no blocking amendment.

## AR(1) cross-check (independent of BC/IR; uses GROW-L5 (P1)-(P4), PROVED-CHECKED)

After the sign flip D = diag((-1)^i) (absolute values of all covariances and regression coefficients are invariant),
take 0 <= rho < 1.

* Spectrum: (P1) gives exactly [c, C] above, for every principal submatrix. Confirms (T1-R), (FL-R) and §0's [c,C].
* Leak / locality: (P4) gives 0 <= Cov(x_j, x_k given x_T) <= rho^{abs(j-k)} for EVERY T (no size limit). Since
  rho^d <= K_dec (1+d)^-3, BC holds in the AR case with K_dec in place of K_15 and with no restriction abs(U) <= 15.
  Hence (L-gain-R) with varpi_n = rho^{R_Q+1} (superpolynomially small) and (L-loc-R) with r_n = rho^{r0+1} <= n^{-log(1/rho)}.
* Regression localisation: by (P2), beta_T(l) is supported on the nearest elements a < l < b of T, with
  c_a = rho^{d1}(1 - rho^{2 d2})/(1 - rho^{2(d1+d2)}) in [0, rho^{d1}] and symmetrically c_b in [0, rho^{d2}]
  (d1 = l-a, d2 = b-l; one-sided case: rho^{d}). With A = T intersect N_l (T subset Q, so a, b in N_l iff within r):
  (i) both within r: A has the same nearest neighbours, beta_A(l) = beta_T(l) exactly (Markov), difference 0;
  (ii) exactly one (say a) beyond r: beta_A(l) = rho^{d2} e_b, and the difference has l1 norm
       c_a + (rho^{d2} - c_b) <= rho^{d1} + rho^{2 d1} <= 2 rho^{r+1};
  (iii) both beyond r: difference c_a + c_b <= 2 rho^{r+1}.
  So (0.1) holds in the AR case with L_n = 2 rho^{r+1}, and (0.2) follows by the same orthogonality argument
  (Var(l given A) - Var(l given T) <= L_n^2, Var(l given T) >= (1-rho^2)/(1+rho^2) by (P3)).
  With r = floor(sqrt(log n)): L_n -> 0 and L_n^2 log(q+1) = o(log n).
* Thus every FAMC-consumed item except (V-R) is closed in the AR(1) special case by (P1)-(P4) plus the
  explicit two-neighbour computation above, without using Lemma BC or Lemma IR at all. This is a fallback if the
  "unchecked" status of BC/IR is an issue for the registry; it is not needed for correctness.

## Non-blocking notes (wording only; no verdict change)

1. POLY:106-107 says the Schur complement is "the inverse of a principal submatrix of Sigma^-1". Precisely it is the
   inverse of the V-block of (Sigma_{U union V})^-1, which is not a submatrix of Sigma^-1 unless U union V = [p].
   The spectral conclusion [c, C] is unaffected (principal submatrix of an inverse of a principal submatrix).
2. L6:76-84: the step ||beta_T(l)_E||_1 <= F(r) uses that E = {v in T : d(l,v) > r}, which needs T subset Q
   (true on the lattice, RM2S:70); one clause saying "T subset Q" would make (0.1) self-contained.
3. L6:164-166 records E2 as "PROVED (by this seat, unchecked)" while the registry says "line-checked LC2-C"; the
   file header (L6:1-5) already records the check. Bookkeeping only.

OVERALL: PASS — every FAMC-consumed E2 item (T1-R, FL-R, L-size^b, L-feas, L-gain-R, L-loc-R, W-R via D-loc^b) holds
at alpha = 3, b = 1/4, varrho = 1/120; there are no gaps, and the AR(1) case is independently closed by GROW-L5 (P1)-(P4)
and the explicit Markov regression computation.

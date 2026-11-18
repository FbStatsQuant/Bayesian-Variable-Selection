model: claude-opus-5-5 (claudeAgent_personal, high); round=R1; seat=opus; manifest=322e8c121e76a3d19d31b4870b39da8e09baa18d6c92f330d8f74ee293eaadd6

# RM2 council R1 — Opus seat: W3-RM2:Ex-PolyR, W2-LOC2:Lemma-BC, W2-LOC2:Lemma-IR

Binding: `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2 Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1r.txt`
printed `verify: OK MANIFEST 322e8c121e76a3d19d31b4870b39da8e09baa18d6c92f330d8f74ee293eaadd6`.
Read in full (chunks of at most 120 lines): `W3-RM2/STATEMENT.md:160-276` (§3.2 and (C2)-(C5)); `W3-RM/STATEMENT.md:100-160`;
`W3-RM2/lemmas/L6_examples.md:1-110, 160-265` (§0 and all of §E2); `W2-LOC2/lemmas/L6_poly.md:1-200` (premises, BC, IR)
and `:228-275, :326-341` (the old-cutoff ledger targets); `W3-RM2/lemmas/L5_formR.md:14-20, :100-117`;
`W2-LOC2/lemmas/L2_NAR.md:12-38`; `W2-APP/lemmas/L1_POST.md:18-52`; `W2-APP/lemmas/L3_LOC.md:24-34`.
`W3-FAMC/reviews/E2_check_opus_R1.md` was used as a pointer only; every step below was re-derived here.

| id | decision |
|---|---|
| W3-RM2:Ex-PolyR | ACCEPT |
| W2-LOC2:Lemma-BC | ACCEPT |
| W2-LOC2:Lemma-IR | ACCEPT |

## 1. Lemma BC (whole lemma, every fixed M) — `L6_poly.md:78-109`

* Cofactor path (`:89-96`). In the cofactor of (B^-1)_ij (rows minus j, columns minus i) each monomial is a map
  r -> sigma(r): every vertex except j has out-degree 1, every vertex except i has in-degree 1, and i has in-degree 0. The
  walk from i cannot revisit a vertex (that vertex would get two predecessors; i has none), so it ends at j, which has
  out-degree 0. Path length h is in [1, m-1]. Re-derived.
* Some path edge has distance >= d(i,j)/h (triangle inequality), and (1 + d/h) >= (1 + d)/h for h >= 1, so that factor is
  <= K0 h^alpha (1+d(i,j))^-alpha <= K0 (m-1)^alpha (1+d)^-alpha. The other m-2 factors are <= K0 (diagonal 1, off-diagonal
  <= K_dec). (m-1)! monomials, det B >= c^m by interlacing. (P1) holds. Since K0 >= 1 and c <= 1 (unit diagonal), the
  bound increases in m, so the maximum over m <= M+2 gives K_M, uniform in p, positions, indices and U with |U| <= M.
* Conditioning (`:99-103`). The 2x2 conditional covariance is H^-1, with H the {j,k} block of (Sigma_{U u {j,k}})^-1;
  eig(H) is in [1/C, 1/c], so |S_jk| = |H_jk|/det H <= C^2 |H_jk|. Re-derived. The case U empty (m = 2) is included.
* Spectral clause (`:104-107`): conditional covariance of W_V given W_U = [((Sigma_{U u V})^-1)_{VV}]^-1; its spectrum
  is in [c, C] for every U, of any size. Variances are in [c, 1]. Re-derived.
* The proof uses only unit diagonal, spectrum [c, C], the envelope and distinctness of positions. It uses neither
  alpha > 17/2 nor bijectivity of pi; it holds for every alpha > 0 and every injection. The lemma is correct as stated.

## 2. Lemma IR (whole lemma, every alpha > 2) — `L6_poly.md:118-167`

* At most two positions at each positive distance (injectivity). ||A - A_B|| <= 2 K_dec sum_{d>B} (1+d)^-alpha
  <= H1 B^(1-alpha) (alpha > 1); for B >= B0, lambda_min(A_B) >= c/2.
* Weighting (`:136-145`): E_ik = (A_B)_ik (e^{t(d(i,j)-d(k,j))} - 1), |.| <= |A_ik|(e^{t d(i,k)} - 1) <= |A_ik| t d(i,k) e^k
  on the band (t d <= k). Row and column sums are <= 2 K_dec t e^k sum_d d(1+d)^-alpha, finite exactly when alpha > 2,
  and <= c/4 for small fixed k and every B >= 1 (t = k/B <= k). The Schur test gives ||E|| <= c/4. Then sigma_min(A_B + E)
  >= c/4. The (i,j) entry of D A_B^-1 D^-1 is e^{t d(i,j)} (A_B^-1)_ij (d(j,j) = 0), so |(A_B^-1)_ij| <= (4/c) e^{-k d/B}.
* Resolvent: ||A^-1 - A_B^-1|| <= (1/c)(2/c) H1 B^(1-alpha). With B = floor(d/(M1 log(2+d))), k M1 > alpha:
  e^{-kd/B} <= (2+d)^{-k M1} = o(f(d)); B >= d/(2 M1 log(2+d)) for large d, so B^(1-alpha) <= (2M1)^(alpha-1) f(d) up to a
  constant. Bounded d (and the diagonal) is absorbed with ||A^-1|| <= 1/c. (P2) holds with H depending on (c, K_dec, alpha)
  only, uniform in the subset, p and n.
* (P3): beta_v = -(B^-1)_vl / (B^-1)_ll and (B^-1)_ll = 1/Var(W_l | W_T) >= 1. The l1 bound and the tail F(r) follow from
  two positions per distance and sum_d f(d) < infinity, which holds iff alpha > 2. Correct as stated.

## 3. W3-RM2:Ex-PolyR — registered `STATEMENT.md:259-275`, proof `L6_examples.md:164-263` with §0 `:33-103`

§0 (`:33-103`), re-derived:
* K_15 = C^2 max_{2<=m<=17}[...] is BC with M = 15 (m <= M+2). The extension to an injection into Z is valid (see §1).
* J (inverse column-sum norm, including the diagonal H f(0)) and D (rectangular column-sum norm) are correct.
  Normal equations B_AA beta_A + B_AE beta_E = B_Al give beta_A(l) = beta_T(l)_A + B_AA^-1 B_AE beta_T(l)_E. Hence (0.1):
  ||beta_bar_T - beta_bar_A||_1 <= (1 + JD) ||beta_T(l)_E||_1, and ||beta_T(l)_E||_1 <= F(r) because T is a subset of Q
  (lattice), so every v in E = T \ N_l has d(l,v) > r. The empty case A = empty is the same bound.
* (0.2): e_A = e_T + W_T delta, with e_T uncorrelated with W_T, and delta' B_TT delta <= ||delta||_1^2 (|B_ij| <= 1). So
  Var(l|A) <= Var(l|T) + L^2 <= (1 + L^2/c) Var(l|T), using the BC floor Var(l|T) >= c. Correct.
* r = floor(sqrt(log n)): |N_l| <= 2r = o(log n), L(r) -> 0, L(r)^2 log(q+1) <= L(r)^2 (b log n + 1) = o(log n).

§E2, against RM2 §3.2 (`STATEMENT.md:172-202`) and RM `STATEMENT.md:129-156`:
* Leak set (`:176-201`). R_Q = ceil(n^gamma (log n)^(-gamma/2)) is the registered radius (n/sqrt(log n))^{1/(2 alpha)}.
  (2.1): p <= 2|Q0| + 32 s0 in the enlarged branch, so q <= 4 s0 R_Q + 34 s0. That is <= n^b for every b in [gamma, 1/2),
  including b = gamma because of the (log n)^(-gamma/2) factor. (2.2): for l not in Q0, d(l,j) >= R_Q + 1 for all j in S0.
  BC then gives |Cov| <= K_15 R_Q^-alpha <= K_15 n^-1/2 (log n)^{1/4}, since gamma alpha = 1/2, and
  varpi_n sqrt(n/log n) <= K_15 (log n)^-1/4 -> 0. This holds for every U of size <= 15 avoiding l and j. Correct.
* (T1-R): LSF with phi^2 = psi_n = c (`L1_POST.md:23-25`, phi in (0,1] since c <= 1). (FL-R): interlacing. (V-R): assumed
  PTV(a0), matching `L3_LOC.md:28`. Not deducing it is correct.
* (L-feas) with K = min(p, floor(n/2)) (`STATEMENT.md:51, :134`). The bound q <= 4 s0 R_Q + 34 s0 = o(n) is
  deterministic, so both branches give q <= K and the dichotomy holds for n >= n0. Correct.
* (L-loc-R) (`:226-232`). H_l is deterministic and contains {l} u S0, with |H_l| <= (s0+1)(2 ceil(log n) + 1) <= n^rho
  eventually for every fixed rho > 0. For v in U \ H_l: v is not in U0, v != j, and d(v,l), d(v,j) > r0. BC with
  |U0| <= 15 gives r_n = K_15 (1+r0)^-alpha -> 0 (only r_n -> 0 is required in v1.4, `STATEMENT.md:178`).
  rho = (1/2 - b)/30 gives 15 rho + b = 1/4 + b/2 < 1/2. Correct for every b < 1/2.
* (W-R) via (D-loc^b) (`:233-246`). Checked against the exact inputs of Lemma D-loc^b (`L5_formR.md:108-111`):
  - (N0^b): p <= n^A, S0 in Q, q <= n^b, q <= K.
  - (N1): (FL-R) on Q u {l}.
  - N_l: deterministic, contained in Q \ {l}, with nu_n = 2 floor(sqrt(log n)) = o(log n).
  - L_n = L(r) and eta_n = L(r)^2/c: deterministic, with L_n^2 log(q+1) = o(log n) and eta_n -> 0.
  - Both inequalities hold for every (T, l) in P+ (any lattice T and l not in T, with beta_{empty,l} = 0) by (0.1)-(0.2).
  All inputs are supplied. The frame and atom count p 2^{2r} = p n^{o(1)} and q unit-variance atoms is consistent with
  L5_formR's own proof (`:112-116`). The sample-floor remark is correct (q sqrt(log n/n) -> 0 since b < 1/2).
* Registered claims (`STATEMENT.md:270-275`) match: alpha > 2 from IR (J < infinity iff alpha > 2), any
  b in [1/(2 alpha), 1/2), logarithmic H_l, (L-gain-R) at every conditioning set by BC, (W-R) via (D-loc^b) + IR.
  "Leak and size budgets alone need only alpha > 1" holds: gamma < 1/2 iff alpha > 1, and BC holds for every alpha.
* Old-cutoff ledger (`:253-262`) is faithful to `L6_poly.md:233-238, :264-271, :329-339`:
  1/(4 alpha) < (1/2 - 1/(2 alpha))/15 iff alpha > 17/2. This is commentary and not load-bearing.
* Status line (`:166-168`) carries BC and IR verbatim as "PROVED (by this seat, unchecked)" (`L6_poly.md:78, :116`)
  and makes E2 conditional on RM2-R. D-to-W is taken as given, as the brief allows.

## 4. Findings (editorial only; none blocks)

* E1 — `L6_examples.md:45-56` cites Lemma BC for every alpha > 2. The file-level premises it sits under
  (`L6_poly.md:33-41`) include alpha > 17/2 and a bijection pi. §0 justifies the injection extension (`:55-56`) but does
  not say that BC's proof (`L6_poly.md:86-107`) does not use alpha > 17/2. It does not (see §1), so the use is sound.
  Suggested clause: "BC's proof uses only unit diagonal, spectrum and envelope; it holds for every alpha > 0."
  IR is explicitly stated for alpha > 2 (`L6_poly.md:120`), so no such note is needed there.
* E2 — `L6_poly.md:104-106`: "the Schur complement is the inverse of a principal submatrix of Sigma^-1". Precisely, it is
  the inverse of the V-block of (Sigma_{U u V})^-1, which is not a submatrix of the full Sigma^-1. The spectral
  conclusion is unchanged.
* E3 — `L6_examples.md:83-84`: the step ||beta_T(l)_E||_1 <= F(r) uses T in Q (lattice sets). One clause saying so would
  make (0.1) self-contained.
* E4 — `STATEMENT.md:273` "(every rho > 0 admissible)" is meant as |H_l| <= n^rho for every rho > 0. The budget
  15 rho + b < 1/2 still restricts rho. "Arbitrarily small rho > 0" (as in `L6_examples.md:260`) is the accurate wording.

No C, S or F finding.

## 5. Gates

* G1 PASS — BC (all M), IR (all alpha > 2) and E2 (whole class) re-derived; `L6_poly.md:86-167`, `L6_examples.md:33-246`.
* G2 PASS — every RM2-R hypothesis E2 claims (`STATEMENT.md:172-202`) and the D-loc^b inputs (`L5_formR.md:108-111`)
  are supplied with the exact quantifiers; BC/IR are used within what their proofs establish (E1 is wording).
* G3 PASS — no hidden independence, uniformity or selection: all constants depend on (c, C, K_dec, alpha, s0) only. Q,
  H_l and N_l are deterministic functions of (pi, S0, n). PTV is assumed explicitly (`L6_examples.md:219-220`).
* G4 PASS — BC and IR statuses carried verbatim, and E2 is conditional on RM2-R and on the stipulated
  D-loc^b => D-R^b => W-R (`L6_examples.md:24-26, :166-168, :242`).
* G5 PASS — K_15 explicit (`:52-53`). varpi_n = O(n^-1/2 (log n)^{1/4}). The exponents |Q| <= n^b (b >= gamma),
  |H_l| = O(log n), 15 rho + b = 1/4 + b/2 and L(r)^2 log(q+1) = o(log n) are all tracked.

Score: 9.5 (all three claims correct for their full class; four editorial points only).

`COUNCIL-VERDICT round=R1 manifest=322e8c121e76a3d19d31b4870b39da8e09baa18d6c92f330d8f74ee293eaadd6 seat=opus score=9.5 gates=PASS`

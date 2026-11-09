# Verdict: HOLDS-WITH-AMENDMENTS

**W2-LOC2, STATEMENT v1.2. Independent adversarial review, 2026-11-09.**

**Findings: 0 FATAL, 0 MAJOR, 1 MINOR.** The amendment concerns the description of numerical coverage, not a theorem hypothesis or proof step. I found no counterexample to NA-R, PLR, LOC-d, LOC-BF, the polynomial-decay result for alpha > 17/2, or F-LOC2 **under their stated inherited premises**. No theorem narrowing is required by this review. This does not discharge the inherited open implementation input N3/e4 or upgrade the code-reading audits.

Only this report was written. No git commands were run. Fresh numerical probes ran in memory with Python 3.13, NumPy 2.3.0, and `-B`; the shipped numerical scripts were read, not executed with their output-writing entry points. No other agents or prior review reports were used to derive the findings.

## Findings and exact fixes

### B4-M1 — MINOR: NA-R numerical fixture overstates which index pairs it tests

**Locations:** `Theory_work/Wave2/W2-LOC2/numerics/n4_nar_check.py:7`, `:8`, `:107`, `:116`.

The docstring says “random T + T on a greedy path” and “all l not in T.” The implementation constructs eight random subsets, the full relevance set, and the truth set (`:107–111`); it does not generate a greedy path. It builds candidate indices from `Qx` plus 30 sampled indices, filters them, and truncates to 60 (`:116`). It therefore does not test all candidate additions or enumerate the lattice. The same candidate may also appear more than once.

**Impact:** this is a numerical-coverage description error. It does not invalidate the identities checked on the sampled pairs, the analytic uniformity proof, or the more carefully qualified conclusions in L2. The fresh complete-lattice probe below closes the small-instance numerical coverage gap for this review; it is not an asymptotic certificate.

**Exact fix:** replace the docstring at lines 7–9 with:

> Part 2 (NA-R): raw W ~ N(0, Sigma) rows, eps ~ N(0, I); test eight random T in [S0,Q], plus T=Q and T=S0. For each T, test up to 60 candidate additions drawn from Qx and 30 sampled indices outside T, allowing repetitions. Check the sample/population residual identity and the reference-plus-atoms bound. This fixture does not enumerate the lattice or generate an LS0 greedy path.

No change to the mathematical statement is needed. The numerical fixture can retain its present sampling algorithm after correcting its description.

## 1. NA-R: attempted breaks and why they fail

References in this section are to `Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md` unless expanded otherwise.

### 1.1 The sharp union really is over frames, not over lattice sets

The general lemma **assumes**, rather than derives, the frame-count condition (`:28–30`). Its applications supply it explicitly:

* LOC-d: for each l, only the near pattern `T' = T intersect B_l` determines the reference. With radius `log log n`, separation gives at most `(2 log log n + 3)^d` nearby sites. Consequently `log N <= log p + O((log log n)^d) = log p + o(log n)` for every fixed d. Every one of the `2^(q-s0)` lattice sets maps to one of these patterns. See `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:46–50`.
* LOC-BF: bounded groups need at most `p 2^g0` one-dimensional frames. A growing one-factor group uses the **whole two-dimensional frame** `(F_G, xi_l)`, one per l. Its coefficients may vary with T without creating a new frame. Total `N <= p 2^g0 + p`; see `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:99–111`.
* Polynomial decay: integer positions give at most `2r_n` neighbors, hence `N <= p 2^(2r_n)` with `r_n = ceil(log log(n+exp(exp(1))))`; see `Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md:358–361`.

Step 2's frame event bounds the norm of the noise projection onto **each entire realized frame subspace** (`:74–78`). Bounding a single reference direction and then choosing another direction after observing noise would have been invalid. That is not the proof given here. Conditional on the full Gaussian extension, each frame projection has chi-square rank at most fixed m0. At threshold `2 log N + (m0+2) log log n`, the union failure is `O(1/log n)`. Near linear dependence or rank loss only reduces the rank and does not defeat this argument.

The exponentially many pairs still appear in the norm and projection events E_a/E_b (`:62–71`). Their logarithmic cardinality is `O(q+log n)`. Those unions are affordable because they enter relative norm errors and the sample-comparison error, not the leading sharp noise threshold. There is no omitted factor `2^q` in E_d.

### 1.2 Conditioning on noise in the atom bound is legitimate

The latent extension, its row law, all functionals, and the decomposition coefficients are fixed population objects, independent of the entire epsilon vector (`:15–20`, `:31–36`; also `STATEMENT.md:45–56`). Conditional on epsilon, each atom satisfies

```text
(C W a)' epsilon = (W a)' C epsilon
                 ~ N(0, Var(a) ||C epsilon||^2).
```

Atom coordinates need not be independent of one another, of raw columns, or of frames. The union bound needs only these marginal conditional tails. The E_e threshold explicitly adapts to L_n and the number of atoms, **not to the realized noise or selected T** (`:79–85`). R2 implies both `b_n -> infinity` and `L_n^2 y_n^2 = o(log n)`, even if L_n is not bounded.

The frame tails condition on the extension; the atom tails condition on epsilon. These are separate unconditional failure bounds, integrated and combined by a union bound (`:86`). The proof never needs either tail assertion to remain true after conditioning on all the other events.

After those simultaneous events hold, choosing a noise-dependent T, partition, or start maximizer is harmless. The argument does not apply a Gaussian law to an atom fitted using the selected T. In LOC-d the atoms are the fixed coordinates indexed by deterministic Q. In LOC-BF they are fixed latent idiosyncratic coordinates indexed by Q. The Gaussian conditional construction of the latter (`L4_LOCd.md:93–97`) preserves independence from epsilon and the original marginal law of (X,epsilon).

**Boundary of this conclusion:** empirical regression coefficients, noise-dependent frames, or a Q chosen using the response would require a different argument. They are excluded by the present hypotheses; no such substitution appears in the applications inspected.

### 1.3 Uniform coefficient bounds survive arbitrary lattice conditioning

For LOC-d, `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:67–75` applies CT_d to the principal matrix on `A union {l}`. Block inversion gives

```text
beta_A(l)_v = -Psi_vl/Psi_ll,
Psi_ll = 1/Var(W_l | W_A) >= 1.
```

Exponential inverse decay and packing give a finite L0 independent of A, p, and n. Thus `||beta_T - padded(beta_T')||_1 <= 2L0` on every lattice set. The near-reference variance ratio follows separately from TAIL, whose conditional covariance and Schur-complement floors are uniform in **all** conditioning sets (`L3_CTd.md:77–85`). Large or disconnected T causes no problem. The constants may be extremely conservative, but remain fixed when d and the LOC constants are fixed.

For LOC-BF, Sherman–Morrison gives

```text
beta_A(l)_v = b_l [b_v/(1-b_v^2)] / (1+s2),
s2 = sum_{v in A} b_v^2/(1-b_v^2).
```

The loading gap `b_v in {0} union [b_lo,b_bar]` is essential to the stated bound. It gives `||lambda||_1 <= ||beta_A||_1 <= 1/b_lo`, uniformly even when A contains an arbitrary number of group members. Zero loadings contribute zero. The reference depends only on `(F_G,xi_l)`, which is independent of the idiosyncratic atom coordinates in A; hence `Var(e) = Var(r) + sum lambda_v^2`, so R3 holds with eta=0. See `L4_LOCd.md:102–112`. No bounded upper eigenvalue for a growing factor group was smuggled into this step.

### 1.4 The sample error has the claimed rate and is sufficient

The exact identity uses the **full population residual** e_T, not the near reference (`:54–60`). Gaussian population regression makes e_T independent of W_T for each deterministic pair. Uniform chi-square bounds give

```text
||P_T e_T|| <= tau_T sqrt(v_n),        v_n = O(q+log n),
||P_T epsilon|| <= ||P_Q epsilon|| = O_P(sigma sqrt(q+log n)),
||(I-P_T) C e_T|| >= tau_T sqrt((n-1)/2).
```

Multiplication yields `epsilon_n = O((q+log n)/sqrt(n))`, exactly as asserted (`:96–100`). This is a simultaneous bound; it does not require T to be independent of the data. The normalization multiplier is `1+O((q+log n)/n)`.

For polylogarithmic q, epsilon_n tends to zero for every fixed power. Together with R1–R3, the squared upper bound is `2 log p + o(log n)` (`:102–109`). Its cross terms have been included. The actual NA threshold exceeds `2 log p` by `log n - O(log log n)`, so the error control is more than sufficient. This is an asymptotic statement with sequence-dependent onset, not a practical finite-n threshold guarantee.

## 2. LOC-d sandwich, toolkit, and shipped cap

`Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:23–41` correctly bounds the conjugation error by row and column sums using the separated-site packing bound. It does not assume a one-dimensional ordering or a dimension-independent packing constant. CD_d takes the inverse of the precision matrix on the **full unconditioned complement**, then takes principal submatrices for smaller target sets (`:58–65`). This avoids the common error of identifying a marginal conditional covariance with the inverse of an undersized precision submatrix.

The relevance radius is O(log n); packing gives `q = O((log n)^d)`, including after enlargement (`L4_LOCd.md:14–16`). The proof sometimes uses the weaker envelope `(log n)^(d+1)`; it does not replace the sharper stated order by a stronger unsupported claim.

The selection-removal reference count is `O((log n)^(15d)) = n^o(1)` (`L4_LOCd.md:25–36`). Only bounded-dimensional partial correlations are conditioned on here. The count is per candidate l; multiplying by p is canceled by the `2 log(p/k)` part of the spherical-tail threshold in the count expectation. The global size ladder still has O(log n) rungs and gives failure `n^(-1/2+o(1)) O(log n)`. After the ladder, `log k = O(log log n)` makes the junk-deletion gain positive (`:38–43`). There is no assumption that a maximizer starts small.

The lattice score family itself has logarithmic cardinality `O(q+log n)`. L1 explicitly increases the projection and contrast thresholds, rechecks the RSS floor, and checks `omega_n log n -> 0` for the sharp NA reduction: `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:19–42`. Thus simply reusing an O(log n) noise threshold on the much larger lattice is not an unacknowledged step.

For PLR, the local floor on `Q union {l}` covers all models used by the lattice and its one-move neighbors. The additional global/sparse floor is needed only for the posterior clause, and the theorem explicitly separates it (`Theory_work/Wave2/W2-LOC2/lemmas/L5_assembly.md:13–33`).

On the three events, deterministic descent removes exactly one extra per move, including the swap comparison: `Theory_work/Wave1C/C-GROW/lemmas/L1_descent.md:21–56`. Therefore the shipped cap `ell_n + |start mode|` suffices regardless of whether the extra count is superlogarithmic. I also checked the current production implementation: `Scripts/SMC_BVS/core/v3_run.R:95–101` defaults to the enlarged cap, and `Scripts/SMC_BVS/core/cpp/v3_core.cpp:469–476` adds the actual mode size before calling local search. The smaller testing override is not the cap asserted by this theorem.

## 3. LOC-BF does not contradict Lemma VN

`Theory_work/Wave2/W2-APP/lemmas/L5_VN.md:23–34` obstructs a bounded start or a sandwich with an **O(log n)** relevance set. It explicitly makes no impossibility claim about LS0 starting from a larger model (`:9–11`). For fixed-rho truth groups of actual size g_n with `g_n/log n -> infinity`, its visible-null lower bound is of order g_n (`:74–83`).

LOC-BF allows Q to include those entire truth groups, giving `q = O(s0 g_n)` before enlargement. Its enlarged cap permits the necessary number of deletions. NA-R then controls all superset residual statistics using two-dimensional factor frames and bounded-l1 atoms, rather than charging a common chi-square projection of rank about q or union-bounding `2^g_n` directions. These statements can all hold simultaneously. The new result answers the deletion-path question left open by VN for this subclass; it does not refute VN's start-mode lower bound.

The class also contains zero-loaded groups without visible nulls. The current statements restrict the VN obstruction to the applicable subclass (`STATEMENT.md:82–84`, `L4_LOCd.md:116–120`). I found no remaining overgeneralized VN attribution in the inspected theorem statements.

## 4. Polynomial decay: BC, IR, and the 17/2 cutoff

All references in this section are to `Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md`.

**BC (`:78–109`) holds with exponent alpha for fixed conditioning size.** In the cofactor expansion for an inverse off-diagonal entry, each monomial has a directed path from i to j with at most m-1 edges. At least one edge spans distance at least `d(i,j)/(m-1)`; retaining that factor's decay suffices, while all other factors are bounded by K0. Determinant division costs at most `c^(-m)`. With `m <= M+2`, the factorial and power factors are fixed constants. Inverting the final 2-by-2 precision block costs at most C^2 because its determinant is at least `1/C^2`. This proves the stated uniform bound. It would not give a useful uniform constant for growing M; the sandwich uses only M=15. The subsequent regression on truth residuals uses their spectral floor, not a new large-conditioning decay assertion (`:111–114`, `:277–285`).

**IR (`:118–167`) is a valid separate large-set estimate.** Truncating at bandwidth B gives operator error `O(B^(1-alpha))` uniformly in a principal subset, since at most two original sites occur at each positive integer distance. For B sufficiently large, the truncated matrix retains floor c/2. The column-specific exponential weight with rate k/B has conjugation error at most c/4, using summability of `sum d(1+d)^(-alpha)` for alpha>2. Neumann inversion gives the exponential bound for the banded inverse; the resolvent identity gives the truncation error. Choosing `B = floor(d/(M1 log(2+d)))` produces

```text
|(A^-1)_ij| <= H (1+d)^(1-alpha) [log(2+d)]^(alpha-1).
```

This envelope is summable for alpha>2. The original positions are retained on every principal subset, so there is no illicit compression of distances. The same inverse-entry regression identity gives a uniform l1 bound and a tail F(r) tending to zero.

**The shrinking atom bound is necessary and actually proved (`:354–385`).** A merely bounded coefficient norm would leave a leading-order atom contribution when `log q` is proportional to `log n`. The tower property supplies the stronger identity on T':

```text
lambda_on_T' = -sum_{w in T\T'} beta_T(w) gamma_w,
||lambda||_1 <= (1+L0) sum_{w in T\T'} |beta_T(w)|
             <= (1+L0) F(r_n) -> 0.
```

Here gamma_w regresses W_w on W_T', so IR bounds its l1 norm uniformly. This controls the coefficient changes on near coordinates as well as the omitted far coefficients. Unit marginal variances imply `Var(D) <= ||lambda||_1^2`; orthogonality of e_T and D gives R3. Thus `L_n^2 log(q+1) = o(log n)` holds even for polynomial q. This is not a silent invocation of the original polylogarithmic NA-R hypothesis.

**The cutoff accounting is internally consistent.** Write `b=1/(2 alpha)`, `R=n^rho`, and `lambda=15rho`. The constraints are:

| Step | Required strict inequality | Source |
|---|---|---|
| Selection removal: `sqrt(n log n) R^(-2alpha) + n R^(-4alpha) -> 0` | `rho > 1/(4alpha)` | `:233–271` |
| Reference count and global size ladder | `lambda < 1/2` | `:298–319` |
| Maximum far-null tail at `2 log p + tau log n` | `tau > 2lambda` | `:329–341` |
| Positive deletion gain after `k=O(n^b)` | `tau < 1-2b` | `:342–347` |
| Tail-range safeguard | `tau > 1/2` | `:331–335` |

Since b<1/4 in this regime, the last constraint is compatible with the upper bound. The binding compatibility is `15/(4alpha) + 1/(2alpha) < 1/2`, equivalent to alpha>17/2. At equality no fixed rho/tau slack remains. The cutoff is correctly described as belonging to this proof, not as a lower bound on the method's applicability.

The polynomial score toolkit also checks its size-sensitive conditions (`:174–211`), and NA's sample error remains `O((q+log n)/sqrt(n)) -> 0` (`:387–411`). The NA threshold now retains slack `(1-2b) log n - O(1)` (`:415–421`). Ignoring `2 log q` here would have been a real error; it is explicitly included.

## 5. F-LOC2 delivery

`Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md:7–12` imports the full resource and exact-arithmetic premises, the total tier-1 fallback, the e4 start-mode premise, and the enlarged scan budget. Its finite-n no-output assertion is conditional on those premises; the covariance assumptions alone do not imply it.

Step 1 only needs nonconstant Gaussian columns/response and regularized score positivity; neither sample rank nor lattice concentration is required for that finite-n assertion (`:21–25`). Step 2 uses a design-independent resource/fallback argument with at most `ell_n+K+1` LS0 scans (`:26–28`). The current production fallback is present at `Scripts/SMC_BVS/core/v3_calib.R:120–124` and enabled by default at `:144`; this read-only check is not a new proof of all allocation bounds.

Step 3 correctly defines the deterministic event that LS0 scores S0, even on data where an actual run might not deliver. It bounds that event's complement directly by the three data-event failures (`L7_delivery.md:29–31`). It does **not** invert the one-sided inequality involving D_n. On output, the scored-set argument and `pi(S0)>1/2` force the reported HPM to be S0 (`:32–35`). The posterior expectation input is independent of the calibration law, so replacing the CAL-bearing assembly step by this pathwise argument is valid.

**HQ qualification to preserve:** e4/TDP-IMPL remains a named premise resting on the inherited N3 “OPEN” input, and S.3 remains a code-reading audit (`:37–39`). F-LOC2 is a conditional delivery theorem under those inputs, not a new implementation-correctness proof or a floating-point no-failure guarantee. These qualifications are already present, so they are not new MAJOR findings.

## 6. Fresh falsification numerics

These probes are evidence about finite algebraic implementations of the arguments. None estimates the probability of an asymptotic theorem, certifies its onset, or exhausts the claimed design classes.

### 6.1 Complete small lattices, including noise-selected T

Protocol: NumPy `default_rng(20261109)`, n=256, p=11, S0={0}, Q={0,...,9}. Enumerate every one of the 512 supersets T of S0 in Q and **every** l outside T, including l=10 outside Q: 2,816 pairs per design, 8,448 total. Use independent standard Gaussian epsilon. Center all raw columns; obtain P_T by QR. For each pair compute population beta_T by solving the corresponding covariance submatrix, e_T, the sample residual h, its signed Z statistic, the reference, and the atom coefficients. Take the maximum over the complete pair family, so the selected maximizing T may depend on epsilon.

Designs, processed in the order below with that single RNG:

* Heterogeneous factor: loadings `(0.87,0,0.22,0.93,0.51,0.8,0,0.29,0.91,0.4,0.65)`, independent standard normal factor and idiosyncratic coordinates, `W_l=b_l F+sqrt(1-b_l^2) xi_l`. This tests zero loadings and unequal loadings, beyond the shipped equicorrelation fixture.
* Local: first 11 sites `(i//4,i%4)`, covariance `exp(-EuclideanDistance/1.6)`; reference uses T within Euclidean radius 2.
* Polynomial: sites `(0,1,2,3,5,8,13,21,34,55,89)`, covariance `(1+distance/20)^(-8.51)`; reference uses T within radius 2. This covariance has a finite polynomial envelope with a fixed, possibly large envelope constant.

For local/polynomial designs also check the exact near-coordinate tower identity underlying (P16), using the actual maximum regression l1 norm of gamma_w in the given pair. For the factor design check `Var(r)+sum lambda^2=Var(e)` and `||lambda||_1 <= 1/0.22`. In all designs check the deterministic reference-plus-atoms noise bound and the sample-comparison bound with the actual `||P_Q epsilon||`.

| Design | Max sample/population residual identity error (Euclidean norm) | Max positive atom-bound violation | Max positive sample-comparison violation | Max coefficient l1 norm | Max signed `|Z-Zpop|` | Complete-family max Z² |
|---|---:|---:|---:|---:|---:|---:|
| Heterogeneous factor | 8.80e-15 | 0 | 0 | 0.658430 | 0.34777 | 3.7600 |
| 2-D local | 1.53e-14 | 2.78e-16 | 0 | 0.551510 | 0.29615 | 3.6060 |
| Polynomial | 1.19e-14 | 6.66e-16 | 0 | 0.568133 | 0.31303 | 3.6144 |

Variance-decomposition discrepancies were at most 3.02e-16 in these calculations; the near/far l1 inequality had maximum positive discrepancy 4.79e-16. All assertions allowed tolerance 1e-10. No violation beyond roundoff was found. These q=10 probes validate neither polylogarithmic growth nor a full start-mode sandwich; their purpose is to attack the algebra and post-selection uniformity on genuinely complete small lattices.

### 6.2 BC through 15 conditioning variables

Protocol: seed 20261112, p=18, sites `(0,1,2,3,5,7,10,15,23,35,52,78,110,151,210,290,410,600)`. For alpha in `(2.1,8.5001,12)`, use covariance `(1+distance/20)^(-alpha)` conjugated by independent random diagonal signs. This preserves positive definiteness while introducing signed covariances and conditional cancellation. For each alpha test 300 random pairs and conditioning sets; every third set has exactly 15 variables, and the others have uniformly sampled size 0 through 15.

Compare the direct Schur complement with inversion of the 2-by-2 precision block and with the explicit cofactor bound in (P1), using the actual full spectral floor/ceiling and `K_dec=20^alpha`.

```text
Cases: 900; maximum |U|: 15
Minimum spectral floor: 0.060099837
Maximum inverse-block/direct-Schur discrepancy: 4.4408921e-16
Maximum |conditional covariance| / explicit BC bound: 0.010759435
```

No failure. The small ratios also emphasize that the BC constant is conservative, not that the claimed exponent is optimal.

### 6.3 IR intermediate inequalities and cutoff

Separate seed 20261110; the same three exponents, signed Cauchy covariances, 14 sites through position 151, 30 random principal subsets per exponent, and bandwidths `(2,7,25,80)`. Keep cases with actual truncation error at most c/2. Choose positive k small enough that the actual conjugation Schur bound is at most c/4. Compare the computed inverse with `(4/c) exp(-k distance/B)` and compare inverse differences with `2||A-A_B||/c^2`.

```text
Admissible banded-inverse probes: 203
Maximum resolvent error / bound: 0.074186
Maximum banded-inverse entry / conjugation bound: 0.15332
```

This probes the two inequalities used to derive IR; it does not empirically prove the final uniform asymptotic envelope. The same run included 600 additional BC/Schur probes with conditioning sizes at most 12, with no failure.

Direct evaluation of the strict rho/tau constraints gave an empty rho interval at alpha=8.5 and a nonempty interval at alpha=8.5001. At 8.5001 the rho interval width was about 3.92e-7 and the deletion log-slack coefficient about 1.47e-6. Thus the proof has fixed positive slack arbitrarily close to the cutoff, but can have extremely slow asymptotic onset. No finite-n usefulness near 17/2 is asserted.

## Disposition for HQ

Accept the mathematical claims as stated, preserving their named dependencies and delivery qualifications. Correct B4-M1's numerical-coverage description. No FATAL or MAJOR repair, extra theorem hypothesis, change to the shipped cap, or withdrawal of the polynomial result is supported by this audit.

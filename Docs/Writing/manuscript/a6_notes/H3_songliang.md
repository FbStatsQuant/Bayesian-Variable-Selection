# H3 — Song & Liang (2015): assumption catalogue and citation audit

Helper H3 (Sonnet), read-only; output file only. Sources: `Song_Liang_2015.pdf` (journal pp. 947–972) and `Song_Liang_2015_supplement.pdf` (20 pp.), text extracted with `pdftotext -layout` into `.rc_tmp/sl/` (git-ignored; PDFs never copied into the tree).

**Reading method and caveat.** `pdftotext` silently drops the symbols ≤, ≻, ≺, ≫ and ≠. Every condition whose meaning depends on such a symbol was therefore checked on the rendered page image: journal pp. 947, 950, 952, 953, 954, 955, 958 and supp. pp. 13, 15, 16. The quotes below use the symbols as seen in the images.

**Conventions.**
- Page numbers are journal pages (947–972) for the paper and "supp. p." for the supplement's own pagination (supp. pp. 1–20).
- The paper's `a ≻ b` means lim b/a = 0 (p. 950). In the paper `ch_i` is the i-th *largest* eigenvalue and `ch'_i` the i-th *smallest* (p. 952).
- The supplement names the main-text items differently: Theorem 2.1–2.4 = Theorems 1–4; Corollary 2.1 = Corollary 1; "(A1)", "(A2)" = Conditions 1, 2; "(A1')" = Condition 4; "(B1)" = Condition 3 (rescaled by β*_t, supp. p. 5). Theorem S, Corollary S1 and Lemma S2 exist only in the supplement.
- In tables a pipe inside a quote is written `\|`.
- Quotes are ≤ 40 words; `…` marks an elision.

---

## 1. Catalogue (76 items, A1–J3)

### A. Model, density, dimension

| ID | Label as printed | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| A1 | model (1) | 947 | `y = Xβ* + ε` … `ε = (ε1, …, εn)^T ∼ N_n(0, σ*²) is Gaussian random error.` | Gaussian linear model, no intercept, fixed noise variance σ*²; X is n×P_n. |
| A2 | (text under (1)) | 947 | `The subscript n in Pn means that Pn is a non-decreasing function of n.` | P_n is non-decreasing in n. |
| A3 | focus statement | 947 | `our study of variable selection will focus on the scenario Pn ≫ n, i.e. the column dimension of X is ultrahigh.` | Intended regime is P_n ≫ n. |
| A4 | density (2) | 950 | `f*(y, x) dx dy = … = φ(y; x^T β*, σ*) νx(dx) dy` | Random design: x has an arbitrary law ν_x, y given x is Gaussian with mean x^T β*. No condition on ν_x here. |
| A5 | "P_n ≻ n^θ" (standing assumption of §2.1) | 950 | `To be specific, we assume that Pn ≻ n^θ for some θ > 0, where bn ≻ an means lim_{n→∞}(an/bn) = 0.` | P_n grows faster than some power of n. Not repeated in the statements of Thms 1–3 or S. |
| A6 | Corollary 1, dimension clause | 954 | `Suppose that Pn < exp(Cn^α) for some α ∈ (0, 1)` | Allows exponential-in-n^α dimension. |
| A7 | Theorem S, dimension clause 1 (V_ξ^{-1} = I) | supp. 13 | `nln ≻ log l'n, log(√(n ln)/rn) ≻ √(log Pn), and we set Vξ^{-1} = I for any ξ` | Growth limit on log P_n via n·l_n and r_n; ridge-free prior. |
| A8 | Theorem S, dimension clause 2 (V_ξ^{-1} = X_ξ^T X_ξ/n) | supp. 13 | `nln ≻ l'n, log(√n/rn) ≻ √(log Pn), and we set Vξ^{-1} = Xξ^T Xξ/n for any ξ` | Same with √n in place of √(n l_n). With r_n ≥ 1 this forces log P_n ≺ (log n)²/4. |
| A9 | Corollary S1, dimension clause | supp. 16 | `Assume that Pn < n^{κ log n} for some κ ∈ (0, 1/4)` | Quasi-polynomial dimension; consistent with A8. |
| A10 | λ_n → 0 (corresponds to (13)) | 951 | `we assume that λn → 0 as Pn → ∞, which corresponds to condition (13) in theorem 1.` | Prior inclusion probability must vanish. |

### B. Sparsity and signal

| ID | Label as printed | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| B1 | (3) | 950 | `lim_{n→∞} Σ_{j=1}^{Pn} \|β*_j\| < ∞` | Weak sparsity: bounded ℓ1 norm. Used by Thm 1 only. This is the growing-support option. |
| B2 | (4) | 950 | `lim_{n→∞} Σ_{j=1}^{Pn} 1{β*_j ≠ 0} < ∞` | Strict sparsity: the number of nonzero coefficients stays bounded. |
| B3 | text after (4) | 950 | `the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ Pn} has a finite model size.` | \|t\| is finite (fixed). |
| B4 | Δ(p) and (8) | 952, 952 | `Δ(p) = inf_{ξ:\|ξ\|=p} Σ_{i∉ξ} \|β*_i\|` and `Δ(rn) ≺ εn.  (8)` | ℓ1 mass of the coefficients outside the best r_n-term model must vanish faster than ε_n. Redundant under (4) (p. 953). |
| B5 | Thm 2 sparsity clause | 953 | `the model is strictly sparse, i.e. condition (4) holds, and rn ≻ 1` | Thm 2 (and so Thm 3) needs (4) and r_n → ∞. |
| B6 | proof step, Thm 2.3 (Thm 3) | supp. 6 | `d²(f*, f) ≥ min{δn, β*_t² δn / 20σ*², 1 − √0.8}` | Not a stated hypothesis. To conclude d > ε_n the proof needs β*_t² δ_n ≻ ε_n², i.e. a size condition on β*_t (automatic if β*_t is fixed). |
| B7 | proof of Thm S | supp. 15 | `c = min_{i∈t} \|β*_i\|` … `nln c²` | Not a stated hypothesis. The proof needs n·l_n·c² ≻ log r̄_n + r̄_n log P_n, a beta-min at rate √(r̄_n log P_n/(n l_n)). |
| B8 | proof of Thm S | supp. 14 | `ωt = λ2 Σ_{i∈t} \|β*_i\|² + op(1). Therefore, {1 + 2b0/R*_t + ωt/R*_t}^{n/2+a0} = Op(1).` | Not a stated hypothesis. Op(1) needs λ₂·‖β*_t‖² = O(1), an implicit upper bound on the signal. λ₂ = 1 for V^{-1} = I; λ₂ = l'_n for V^{-1} = X^T X/n. |

(No theorem states a lower bound on nonzero |β*_j|; see flag F3.)

### C. Prior and hyperparameters

| ID | Label as printed | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| C1 | prior (6), cap r̄_n | 951 | `each predictor has a prior probability λn = rn/Pn … we impose a constraint on the model size such that \|ξ\| ≤ r̄n, where the upper bound r̄n is prespecified.` π(ξ) ∝ λn^{\|ξ\|}(1−λn)^{Pn−\|ξ\|} I(\|ξ\| ≤ r̄n) | Independent Bernoulli(r_n/P_n) inclusion, truncated at model size r̄_n. |
| C2 | remark on the cap | 951 | `this constraint can be removed by imposing an additional condition, say, there exists r̄n such that π(\|ξ\| > r̄n) → 0 with an appropriate rate` | The cap can be replaced by a tail bound on the prior model size. Not proved here (refers to Jiang 2007, §7). |
| C3 | σ² and β priors | 951 | `σ² ∼ IG(a0, b0)` … `βξ \| ξ, σ² ∼ N_{\|ξ\|}(0, σ² Vξ), where Vξ is a positive definite matrix depending on ξ.` | Inverse-gamma noise prior; Gaussian slab with a user-chosen covariance V_ξ. |
| C4 | posterior (7) | 951 | `π(ξ\|Dn) ∝ (rn/Pn)^{\|ξ\|}(1 − rn/Pn)^{Pn−\|ξ\|} √det(Vξ^{-1}) / √det(Xξ^T Xξ + Vξ^{-1}) × {2b0 + y^T(I − Xξ(Xξ^T Xξ + Vξ^{-1})^{-1} Xξ^T)y}^{−n/2−a0} I(\|ξ\| ≤ r̄n)` | The posterior on models after integrating out β and σ². The object all theorems are about. |
| C5 | (12) | 952 | `1 ≤ rn ≤ r̄n < Pn` | Ordering of prior parameters. Theorem S also assumes (12). |
| C6 | (13) | 952 | `rn ≺ Pn` | r_n/P_n → 0, so P_n → ∞ is forced even if P_n ≻ n^θ is dropped. |
| C7 | choices of V_ξ | 953 | `For most choices of Vξ, B(rn) ≤ B rn^v and B̃n ≤ B rn^v hold for some positive constants B and v.` | The eigenvalue conditions on the prior covariance are mild for standard choices of V_ξ. |
| C8 | ridge prior | 953 | `let Vξ^{-1} = E(Xξ^T Xξ) + cn I_{\|ξ\|}; then B(rn) ≤ rn + cn and B̃n ≤ cn^{-1}, where cn is proportional to 1/n, i.e. cn ∝ n^{-1}.` | With this ridge (population covariance plus c_n I, c_n ∝ 1/n, standardized predictors) conditions (11) and (14) become conditions on r_n and r̄_n only. |
| C9 | EBIC link | 952 | `If we set Vξ^{-1} = Xξ^T Xξ/n, a0 = b0 ≈ 0, and rn = Pn^{1−γ} for a constant γ ∈ (0, 1)` | The posterior then mimics EBIC. Gives the choice r_n = P_n^{1−γ}. |
| C10 | hyperparameters used | 959–960 | `we set γ = 0.75 and rn = Pn^{1−γ} … λs = \|s\|^{−γ} … a0 = b0 = 1 and τ = 0.01.` | Numerical defaults. The ridge is V^{-1} = (X^T X + τI)/n (§3.1, p. 959). |
| C11 | simulation choices | 961; supp. 18 | `rn = √n and r̄n = 2√n` (p. 961); `rn = √Pn and r̄n = 2√Pn` (supp. p. 18) | Example settings for the cap and for r_n. |
| C12 | SAM prior in stages 1/2 | 959 | `π(ξ) = λs^{\|ξ\|}(1 − λs)^{\|s\|−\|ξ\|} I(\|ξ\| ≤ s̄)` … `π(βξ\|ξ, σ) ∼ N{0, σ²(Xξ^T Xξ + τI)/n}` | The prior used inside the subsets and in the merged set. |
| C13 | complexity assumption | 968 | `by assuming that s̄n = o{(Pn/Kn)^{1/3}} holds` | Cap-size growth bound used only in the computing-cost count. |

### D. Conditions (8)–(14) of Theorem 1 (p. 952)

| ID | Label | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| D1 | Theorem 1 hypotheses | 952 | `all predictors \|xi\| ≤ 1. If there is a sequence {εn} ∈ (0,1) such that nεn² ≻ 1` | Bounded predictors and a rate ε_n with nε_n² → ∞. |
| D2 | (9) | 952 | `r̄n ln(1/εn²) ≺ nεn²` | Entropy-type size condition on ε_n. |
| D3 | (10) | 952 | `r̄n ln(Pn) ≺ nεn²` | ε_n² must dominate r̄_n·log P_n/n. This is the rate floor. With P_n ≻ n^θ and r̄_n ≥ 1 it gives ε_n² ≻ log n/n. |
| D4 | (11) | 952 | `r̄n ln(nεn² B̃n) ≺ nεn²` | Condition on the prior covariance, through B̃_n = sup_{\|ξ\|≤r̄n} ch_1(V_ξ). |
| D5 | (14) | 952 | `B(rn) ≺ nεn²` | Condition on the prior precision, B(r_n) = sup_{\|ξ\|=rn} ch_1(V_ξ^{-1}). |
| D6 | definitions B, B̄, B̃, Δ | 952 | `B(rn) = sup_{ξ:\|ξ\|=rn} ch1(Vξ^{-1}), B̄(rn) = sup_{ξ:\|ξ\|=rn} ch1(Vξ), B̃n = sup_{ξ:\|ξ\|≤r̄n} ch1(Vξ)` | These eigenvalue quantities concern the *prior* matrix V_ξ, not the design. |
| D7 | row law of Thm 1 | 952 | `all predictors have been standardized and uniformly bounded, and the sparsity condition (3) holds.` … `all predictors \|xi\| ≤ 1` | Bounded, standardized predictors. With unit variance, \|x\| ≤ 1 would force \|x\| = 1 a.s., so "standardized" must mean centred and scaled loosely. |

### E. Law of the rows

| ID | Label as printed | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| E1 | Condition 1 | 953 | `for any subvector of x, (xj1, …, xjr)^T with … r ≤ r̄n, and \|ai\| ≤ δ for i = 1, …, r, we have E[exp{(Σ_{i=1}^r ai xji / r)²}] ≤ exp(M)` | Sub-Gaussian-type exponential moment on sparse combinations, up to size r̄_n. It is a *raw* moment bound, so it is not centring-invariant. Worked case (p. 953): zero-mean Gaussian process with var(x_i) = 1. |
| E2 | Condition 2 | 954 | `E(Σ_{i=1}^r ai xji / r)² ≤ M` | Second-moment bound on the same combinations. Gives only the weaker (16) (convergence in probability). |
| E3 | Condition 4 | 957 | `There is a constant δ > 0 such that for any a = (a1, …, as)^T ∈ R^s, with \|ai\| ≤ δ for i = 1, …, s, we have E{(a^T xs)²} < ∞` | Finite second moments for a *fixed* subset s (misspecified-model theorem). |

### F. Eigenvalue and identifiability conditions

| ID | Label as printed | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| F1 | Condition 3 | 955 | `A predictor xk is said to be identifiable among all other predictors, if, for any 1 ≤ j1, …, j_{r̄n} ≤ Pn (ji ≠ k for all i) and bi ∈ R, E[exp{−(xk + Σ_{i=1}^{r̄n} bi xji)²}] ≤ 1 − δn, δn ≻ εn².` | Population "no mimic" condition. A *single* predictor x_k is not approximated, at vanishing level δ_n ≻ ε_n², by any combination of r̄_n others. It constrains only identifiable (true) predictors, and gives no floor on sets of null predictors. |
| F2 | sufficient forms of Cond 3 | 955–956 | `if ch'1{var(x̃)} ≻ r̄n εn² for any choice of x̃, xt is identifiable` (bounded, mean-0); `if ch'1{var(x)} ≻ εn², then all the predictors are identifiable` (standard normal, p. 956) | The only eigenvalue form of Cond 3 is a *sufficient* condition, with an extra factor r̄_n in the bounded case. |
| F3 | (22) | supp. 13 | `For any model ζ with size \|ζ\| = min{\|t\| + r̄n, n}, … nln < ch'1(Xζ^T Xζ) ≤ ch1(Xζ^T Xζ) < nl'n` | Sample eigenvalues of every (\|t\|+r̄_n)-column submatrix lie in (n l_n, n l'_n). {l_n} non-increasing, {l'_n} non-decreasing, both free. A condition on the realised X. |
| F4 | (23) | supp. 13 | `r̄n log Pn ≺ nln.` | The lower eigenvalue level n·l_n must dominate r̄_n·log P_n. A relation among r̄_n, P_n, n, l_n, not a design-only condition. |
| F5 | (26) | supp. 15 | `Pr{nln > ch'1(Xζ^T Xζ) or ch1(Xζ^T Xζ) > nl'n} < e^{−nC}` for any model \|ζ\| = r̄n + \|t\| | SL's own replacement of (22) for random designs: the eigenvalue condition may fail with probability ≤ e^{−nC}. Theorem S "still holds" (supp. p. 15). |
| F6 | remark on (22) | supp. 15 | `the eigenvalue condition (22) is hardly satisfied, although similar conditions have been used in the literature` | SL's own caveat. |
| F7 | Cor 2 hypothesis | 957 | `If xs does not have exact multicollinearity between variables, i.e. there does not exist a non-zero vector a ∈ R^s such that P(a^T xs = 0) = 1` | Only exact collinearity is excluded within a fixed subset. |

### G. Misspecified (split) stage and the algorithm

| ID | Label as printed | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| G1 | (17), Lemma 1.2 | 956; supp. 6 | `f0 = arg min_{f∈Ps} ∫ ln(f*/f) f*` | The limit of the posterior in a misspecified subset is the KL-projection; the proof (supp. p. 6) uses de Blasi–Walker conditions (4), (5). |
| G2 | (19) | 957 | `β0 = Σs^{-1} Σ_{s,t} β*_t = Σs^{-1} cov(xs, y)` | The projection coefficient; links to Cond 5. |
| G3 | Condition 5 | 958 | `\|cov(xt, y)\| > 0 for any true predictor xt.` | Every true predictor has nonzero *marginal* covariance with y (a fixed number, no margin, no conditioning). Used for the iterative screening, not in any numbered theorem (see F8). |
| G4 | remark (a) on p. 958 | 958 | `if there are pn predictors correlated with the true predictor Xt, pn ≺ Pn, then there are at most c pn predictors to be selected into X_s̃ for some constant c.` | Informal "it is easy to show" claim that the leakage into stage 2 is O(p_n). Not a condition; labelled a remark on the procedure. |
| G5 | remark (b) | 958 | `we set the iteration number to 2.` | Stage-1 iteration cap. |
| G6 | remark (c) | 958 | `When \|s\| is large, we suggest imposing an upper bound for the model size` … `corollary 2 does not hold anymore` | With a cap in stage 1, Cor 2 is lost; sure screening "should still hold" (no proof). |
| G7 | remark (d) | 958 | `the SAM approach tends to work better with a large value of s, say s ≥ 500.` | Practical advice on the subset size s. |
| G8 | SAM algorithm | 959 | `Split Pn predictors into Kn groups … max_{i} \|si\| ≤ s` … `at an FDR level of α1` … `at an FDR level of α2` | The two-stage algorithm. §3.1 says only `Clearly, it follows from the theory … that the SAM approach will lead to a consistent selection` (p. 959). No theorem is stated for the two-stage procedure. |

### H. Conclusions

| ID | Label as printed | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| H1 | Theorem 1 (posterior consistency), display (15) | 952 | `P*[π{d(f, f*) > εn \| Dn} > exp(−c1 nεn²)] < exp(−c1 nεn²)` | Posterior mass outside the ε_n-Hellinger ball is ≤ e^{−c nε²} with P*-probability ≥ 1 − e^{−c nε²}. Assumes (3), (8)–(14), \|x_i\| ≤ 1. |
| H2 | Theorem 2 | 953 | `Given a sequence {εn}, εn → 0, and nεn² → ∞, if the conditions (9)–(14) of theorem 1 hold, the model is strictly sparse, … and rn ≻ 1, then the posterior consistency still holds` | Same conclusion as (15) under Condition 1 and (4) in place of \|x_i\| ≤ 1. With Condition 2 only, the weaker (16) (limit in probability). |
| H3 | Corollary 1 | 954 | `Then the convergence rate in theorem 2 can be taken as εn = O{n^{−(1−α)/2} log^{k/2}(n)}` or `εn = O(n^{−(min{1−α−q, 1−vq})/2})` | Rates for P_n < exp(Cn^α), with r̄_n ≺ log^k n or ≺ n^q. |
| H4 | Theorem 3 (sure screening) | 956 | `If a true predictor xt is identifiable, then P*[π{t ∈ ξ\|Dn} < 1 − exp(−c1 nεn²)] < exp(−c1 nεn²)` | Sensitivity: each identifiable true predictor is included with posterior probability ≥ 1 − e^{−c nε²}. SL themselves: `the sensitivity is asymptotically 1, but the specificity is not controlled` (p. 956). |
| H5 | Theorem 4 (misspecified), display (18) | 957 | `π[{f ∈ Ps : d(f0, f) > ε}\|Dns] → 0, almost surely, as n → ∞` | Posterior concentrates on the KL-projection f0, for a fixed subset s (supp. p. 7: "the number of predictors s is fixed"). |
| H6 | Corollary 2 | 957 | `π(s̃ ⊂ ξ \| Dns) →p 1` | Under Cond 4 + no exact multicollinearity, the posterior includes every predictor of s̃ (nonzero entries of β0). |
| H7 | Theorem S (consistency of the MAP model), display (24) | supp. 13 | `max_{k≠t} π(k\|Dn)/π(t\|Dn) →p 0.` | The true model is the posterior mode w.h.p. Assumes a sparse true model t, (12), (22), (23) and either dimension clause A7 or A8. No rate stated; does *not* say π(t\|D_n) → 1. |
| H8 | Corollary S1 | supp. 16 | `r̄n ≺ log^{k1}(n), or r̄n ≺ n^q … for some k1 > 0 or q ≤ 1/2 − √κ, and l'n = ln^{-1} = √n/log^{k2}(n) … Then the consistency of the MAP model holds.` | Theorem S in an explicit regime: P_n < n^{κ log n}, V^{-1} = X^T X/n (+ τI/n). |

### I. Sampler and algorithmic statements (supplement and main text)

| ID | Label as printed | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| I1 | gain-sequence conditions (9) | supp. 9 | `Σ_{t=1}^∞ at = ∞, Σ_{t=1}^∞ at^ζ < ∞, for some ζ ∈ (1, 2)` | Robbins–Monro conditions on the positive non-increasing gains. The gain a_t = t0/max{t,t0} (supp. p. 12) satisfies them. |
| I2 | SAMC setup | supp. 8–9 | `Without loss of generality, we assume ωi > 0 for all i` … `we set Θ = [−10^{100}, 10^{100}]^m` | Non-empty subregions; compact weight space (practically equal to R^m). |
| I3 | SAMC convergence (13) | supp. 9–10 | `Under mild conditions, Liang et al. (2007) showed that as t → ∞, θti → Const + log(ωi) − log(πi + π̄0), if Ei ≠ ∅` | The convergence claim is cited. The "mild conditions" are not listed. |
| I4 | importance-weight invariance | supp. 10 | `as n → ∞, Êf h(x) → Ef h(x) almost surely for the same reason that the usual importance sampling estimate converges.` | Weighted SAMC draws give a consistent estimator of E_f h for integrable h. Cited from Liang (2009); no hypotheses stated. |
| I5 | proposals (16)–(20) | supp. 10–11 | `we specify three types of MH moves, birth, death and exchange` … `where rn < Pn denotes the maximum model size considered by the user` | Single-predictor-deviance weights ρ_i, d_0 > 0. The symbol r_n in (19) is the cap, i.e. r̄_n of the main text. |
| I6 | implementation settings | supp. 11–12 | `we set ∆ = 1, set u1 to be a small number such that E1 is empty` … `a histogram can be considered as flat, if the sampling frequency of each subregion is not < 80% of the average` | Partition by energy, uniform π, flat-histogram stopping rule. Settings, not hypotheses. |
| I7 | marginal inclusion estimator (21) | supp. 12–13 | `It follows from Liang (2009) that q̂j → qj almost surely as N → ∞` | Limit in the number of SAMC iterations, at fixed data. |
| I8 | Lemma S2 | supp. 16–17 | `(i) If Xn ⇒ X, then g(Xn) ⇒ g(X)` … `(ii) If there exists a subsequence {Xnk} such that {g(Xnk)} are mutually independent, then max_n g(Xn) → g* … in probability.` | Used to claim the sampled best model is a consistent MAP estimator (supp. p. 16). Its premises (convergence in distribution; an independent subsequence) are not verified for SAMC. |
| I9 | main-text SAMC description | 959–961 | `the SAMC algorithm adapts the invariant distribution at each iteration` … `270Pn iterations, where the first 20Pn were for the burn-in` | Adaptive chain. Run lengths are chosen by the user, not covered by a theorem. |

### J. Proof-internal items (not hypotheses of the printed theorems)

| ID | Label | Page | Verbatim quote | Plain words |
|---|---|---|---|---|
| J1 | Lemma 1.1 (Jiang 2005, Thm 6) | supp. 1 | `ln N(εn/4, Pn) ≤ nεn²/16;  π(Pn^c) ≤ e^{−nεn²/8};  π[f : dt(f, f*) ≤ εn²/64] ≥ e^{−nεn²/64}` | The three conditions (sieve entropy, outside-sieve prior mass, KL-neighbourhood prior mass) verified for Thms 1–2. |
| J2 | sieve choices | supp. 3 | `choosing Cn = η3 √(B̃n nεn²)` … `ln ln(σ̄n²/σn²) = nεn²/32` | Sieve bound on β and on σ²; this is how B̃_n enters (11). |
| J3 | Cond (B1) in proof of Thm 3 | supp. 5 | `by condition (B1), ∫ exp(−∆h²/β*_t²) νx(dx) ≤ 1 − δn` | Cond 3 is applied to ∆h = −β*_t x_t + Σ_{i≠t} ∆βi xi, so it enters with the scale β*_t. |

---

## 2. Verification of every Song–Liang citation in the manuscript

Searched `Song`, `\SL`, `SongLiang2015`, `their` in `s1_intro.tex`, `s3_method.tex`, `s4_results.tex`, `s5_assumptions.tex`, `supplement.tex`. Lines whose "their" refers to something else (e.g. s1:16, s3:8, s4:113, 131, 360, 424, supplement:4, 194, 196) are not Song–Liang citations. Bibliography entry (`shared/refs.bib`: JRSS-B 77(5), 947–972, 2015) is correct.

Verdict key: **CORRECT**; **CORRECT+n** (correct, with a note); **OVERSTATED** (true in spirit, false as worded); **WRONG**; **UNVERIFIABLE**.

| # | file:line | Sentence (shortened) | Cited item, page | Verdict | Note |
|---|---|---|---|---|---|
| 1 | s1_intro:38–39 | "prove selection and distribution consistency of a posterior with p≫n and run a sampler on it" | Thms 1–2 pp. 952–953; Thm 3 p. 956; Thm S supp. p. 13; SAMC pp. 959–961 | CORRECT+n | "Selection consistency" = MAP consistency (Thm S) plus sure screening (Thm 3). No theorem for the two-stage SAM procedure (p. 959: "Clearly, it follows…"). Focus P_n ≫ n is p. 947 (A3). |
| 2 | s1_intro:39–41 | sampler statements "are limits as the number of iterations grows, at fixed data and for every data set" | supp. pp. 9–10, 12–13, 16–17 (via s3:255) | CORRECT+n | Matches I3, I4, I7 ("as N → ∞", fixed data) and Lemma S2. "For every data set" is an interpretation; SL state a.s./in-probability limits in the sampler randomness. Their premises are cited, not verified (flag F9). |
| 3 | s1_intro:47 | "Our theorems use the same kinds of assumptions as SL" | see #11 | OVERSTATED | Same as #11 (beta-min). |
| 4 | s3_method:254–255 | "Exact arithmetic and ideal random numbers are also presupposed by SL's statements about their own sampler (their supplement, pp. 9–10, 12–13)" | supp. pp. 9–10, 12–13 | UNVERIFIABLE | SL never say this. Pages are right (SAMC convergence p. 9–10, (21) and "a.s. as N → ∞" pp. 12–13), but "presupposed" is the manuscript's inference. Safer wording: "idealised limits whose conditions are cited, not verified". |
| 5 | s4_results:206 | bound exp(−c nε_n²) is "display (15) (their Theorem 1, p. 952)" | (15), p. 952 | CORRECT | |
| 6 | s4_results:207 | "their Theorem 2 has the same form, p. 953" | Thm 2, p. 953 | CORRECT | |
| 7 | s4_results:206–208 | with ε_n² = M log n/n the bound "equals n^{−cM}; so (eq:dist-i) is of the same exponential form, for levels M ≤ √n/log n" | (15), p. 952 | CORRECT+n | The arithmetic is right. SL's Theorem 1/2 does *not* apply at fixed M: (9)–(10) need nε_n² ≻ r̄_n log P_n ≥ θ log n. The manuscript says this in s5:45–46, so no conflict. |
| 8 | s4_results:210–211 | "Song and Liang give no rate for selecting the whole model: their Theorem 3 (p. 956) controls sensitivity only" | Thm 3, p. 956 | CORRECT | SL's own words, p. 956 (H4). |
| 9 | s4_results:211–212 | "their Theorem S (supp. p. 13, display (24)) states consistency of the posterior mode without a rate" | Thm S, (24), supp. p. 13 | CORRECT | (24) is a ratio statement →p 0; no rate, and no π(t\|D_n) → 1. |
| 10 | s5:6–7 | "same kinds of assumptions as SL: a Gaussian linear model, exact sparsity, a bound on the dimension, a law for the predictors, eigenvalue floors on small sets of columns, and nonzero coefficients that are not too small" | A1, B2, A5–A9, E1, F3–F4 | OVERSTATED | Every item is right except the last. SL's theorems state no lower bound (table row s5:70 says so). It appears only inside proofs (B6, B7). |
| 11 | s5:9–10, 36–37 | conventions: journal pages; "supp. p."; r̄_n is their model-size cap | — | CORRECT | r̄_n as the cap (6), p. 951. |
| 12 | s5:40–42 | Thm 3 (p. 956): theirs is sensitivity with exponentially small error; "neither implies the other" | Thm 3, p. 956 | CORRECT | Error is exp(−c1 nε_n²). The implication claim concerns different posteriors, as stated. |
| 13 | s5:42–43 | Thm S (supp. p. 13): different posteriors; mass on the true model with a rate is stronger than a statement about the mode | Thm S, supp. p. 13 | CORRECT | If π(t\|D) > ½ then t is the unique mode. |
| 14 | s5:44 | "same distance as their Theorems 1–2" | d, p. 952 | CORRECT+n | Main-text d² = ∫(√f1 − √f2)² has no ½; the manuscript's d_H² = 1 − ∫√(ff*) is half of it. The supplement's proofs (supp. p. 2, eq. (2); p. 5) use d² = 1 − ∫√(f1 f2), the manuscript's convention. Constants only (flag F7). |
| 15 | s5:44–46 | "same exponential form … it reaches a radius of order r_n, which their conditions do not reach at polynomial p" | (9)–(10), p. 952; Cor 1, p. 954 | CORRECT | (10) with r̄_n ≥ 1 and ln P_n ≥ θ ln n gives ε_n² ≻ log n/n, strictly above radius² of order log n/n. |
| 16 | s5:46–48 | reported model: "their statements are limits in the number of iterations at fixed data, for every data set" | I7, I8 | CORRECT+n | As #2. |
| 17 | s5:63 (table) | GL: "(1), p. 947; (2), p. 950. The same, in every regime" | A1, A4 | CORRECT | |
| 18 | s5:64–65 (table) | DIM: "Cor. 1, p. 954; Thm S, supp. pp. 13, 16; their P_n ≻ n^θ, p. 950" | A5–A9 | CORRECT+n | Pages right. See #28 on "needs". |
| 19 | s5:66–67 (table), 133–134 | SP: "(4), p. 950. The same for their Thms 2, 3, S; their Thm 1 also admits growing supports under (3)" | B1, B2, B5, H7 | CORRECT+n | Thms 2, 3: (4) is explicit. Thm S says only `a sparse true model t` (supp. p. 13) and does not cite (4) or fix \|t\|; \|t\| enters (22) through \|ζ\| = min{\|t\|+r̄_n, n}. Thm 1 under (3): p. 952. |
| 20 | s5:70–71 (table), 144–147 | signal size: "No lower bound stated; (3), (8), pp. 950, 952; supp. pp. 6, 15"; "their proof steps need rates (supp. pp. 6, 15)" | B1, B4, B6, B7 | CORRECT | Supp. p. 6 (β*_t² δ_n step) and p. 15 (c = min\|β*_i\|) are the right places. Supp. p. 14 (B8) also implies an upper bound. |
| 21 | s5:72–73 (table) | EF: "Cond. 3, p. 955; (22)–(23), supp. p. 13" | F1, F3, F4 | CORRECT | Pages right. |
| 22 | s5:74 (table) | NC: "None in their Thms 1–2; Cond. 3, p. 955; (22), supp. p. 13" | D6, F1, F3 | CORRECT | Thms 1–2 have eigenvalue conditions only on V_ξ ((11), (14)). |
| 23 | s5:75 (table) | SGR/GR: "\|x_i\| ≤ 1, p. 952; Cond. 1, p. 953" | D7, E1 | CORRECT | |
| 24 | s5:78–79 (table), 216–217 | V: "Cond. 5, p. 958 … Ours implies theirs, in every regime: theirs is our condition with no conditioning and no margin" | G3 | CORRECT+n | Verified against \as{V} (s4:252–254): U ranges over \|U\| ≤ 15, so U = ∅ is allowed and gives \|Cov(W_j, W^T θ*)\| ≥ a > 0. Same sign as cov(x_t, y) after standardising. Note Cond 5 is not a hypothesis of any numbered theorem (flag F8). |
| 25 | s5:80–81 (table), 252–253 | leakage set: "No hypothesis of this kind; informal remark (a), p. 958 … not a condition of any of their theorems" | G4 | CORRECT | Remark (a) is the first of "a few remarks on this iterative procedure" (p. 958); "it is easy to show". Correct and fairly stated. |
| 26 | s5:116 | "their model (1), p. 947, and density (2), p. 950" | A1, A4 | CORRECT | "Ours adds an intercept" (s5:117): SL's (1) has none. |
| 27 | s5:120–122 | DIM: far fewer than Cor 1 (P_n < exp(Cn^α), p. 954); "slightly fewer than their Theorem S" | A6, A8, A9 | CORRECT | |
| 28 | s5:122 | "theirs needs P_n ≻ n^θ (p. 950)" | A5 | CORRECT+n | p. 950 states it as a standing choice ("To be specific, we assume…"). It is not repeated in the statements of Thms 1–3 or S. What the statements force is P_n → ∞ (via (13), r_n ≺ P_n). Wording: "assumes" or "requires P_n → ∞". |
| 29 | s5:123–126 | Thm S needs log(√n/r_n) ≻ √log P_n (supp. p. 13, condition 2), hence log P_n ≺ (log n)²/4; Cor S1: P_n < n^{κ log n}, κ ∈ (0, ¼) (supp. p. 16) | A7–A9 | CORRECT+n | Both exact. "Condition 2" is the V^{-1} = X^T X/n clause. Clause 1 has √(n l_n) in place of √n; with standardized columns l_n ≤ 1, so the same bound holds. |
| 30 | s5:143–147 | "SL state no lower bound in their theorems. If their β* does not change with n (the natural reading of p. 950)…" | B1, B2 | CORRECT | The reading is natural but not stated; both readings are treated. |
| 31 | s5:156–157 | "our fixed floor implies their (22)–(23) (supp. p. 13; standardised columns) and their Condition 3 (p. 955; Gaussian predictors)" where their sets are no larger | F1, F3, F4 | OVERSTATED | Cond 3 for Gaussian x: E exp(−Z²) = (1+2v)^{-1/2} with v ≥ λ_min(Σ)(1+Σb²) gives a fixed δ_n ≻ ε_n² (ε_n → 0): CORRECT. (22) is a condition on the *realised* X. In a fixed design the implication is direct; for random rows SL's own version is (26) with failure probability e^{−nC} (flag F4). (23) is not design-only; it holds here because r̄_n log P_n = O(log² n) ≺ n. |
| 32 | s5:158–159 | "Where their sets are larger (r̄_n ≻ log n): the two constrain different sets; neither implies the other" | F1, F3 | CORRECT | Their floor on larger sets does imply a floor on subsets, but at a vanishing level, so it need not give ours. |
| 33 | s5:160–162 | "Condition 3 asks a vanishing level δ_n ≻ ε_n² (ε_n their contraction rate) on r̄_n + 1 columns that contain a true predictor" | F1 | CORRECT | |
| 34 | s5:174–177 | NC: "Against their Condition 3 (p. 955) and (22) (supp. p. 13), if their sets are at least as large as ours: theirs gives ours on the sets they cover" | F1, F3 | WRONG | Cond 3 constrains one (true) predictor against combinations of others; it gives no floor on sets of null predictors. Counterexample: x_k, x_a = x_b independent N(0,1), with a, b null duplicates. Cond 3 holds (E exp(−(x_k + c x_a)²) ≤ 3^{-1/2}) but λ_min(Corr(x_a, x_b)) = 0 violates the floor c_ψ/n. Only (22) can give a floor, and it is a sample-level condition (flag F1). The "Where SL's sets are no larger" half (#31) is the safe direction. |
| 35 | s5:178 | "Their eigenvalue conditions (11) and (14) (p. 952) are on the prior covariance" | D4–D6 | CORRECT | B̃_n and B(r_n) are sup ch_1(V_ξ) and sup ch_1(V_ξ^{-1}). |
| 36 | s5:178–180 | "With their own ridge choice, c_n ∝ 1/n (p. 953), no design condition is left, and their rate carries the diverging factor r̄_n: ε_n² ≻ r̄_n log P_n/n (their (10))" | C8, D3 | CORRECT | B̃_n ≤ c_n^{-1} ∝ n, B(r_n) ≤ r_n + c_n. "Diverging": Thm 2 assumes r_n ≻ 1, so r̄_n ≥ r_n → ∞ (p. 953). |
| 37 | s5:194–196 | "On centred, unit-variance predictors, SGR, Gaussian rows (Result 3) and Assumption dist(c) (Result 2) each imply SL's Condition 1 (p. 953); on raw predictors, and against their \|x_i\| ≤ 1 (Thm 1, p. 952), neither implies the other" | E1, D7 | WRONG (as worded) | Cond 1 is for every subvector of size r ≤ r̄_n. SGR has windows 5(A+1)(s+1) log n (s4:105–106), dist(c) q_n = ⌈C_q M log n⌉ (s4:182–184). So the implication holds only for r̄_n ≤ that window. SL's Cor 1 allows r̄_n ≺ log^k n (k > 1) or ≺ n^q, which is beyond. Gaussian rows: true for every r. Raw/bounded part: fine. |
| 38 | s5:197–199 | "implies their Condition 1 for every r … δ = √(3/8)/L, M = log 2" | E1 | WRONG (as worded) / CORRECT (constants) | "for every r" as #37. The constants check out: sub-Gaussian proxy L²v with v ≤ δ² gives E exp(Z²) ≤ (1 − 2L²δ²)^{-1/2}, and δ² = 3/(8L²) gives 2 = e^{log 2}. For L = 1 this is SL's own Gaussian computation (p. 953). |
| 39 | s5:200–202 | "Gaussian rows with mean n … violate Condition 1, which is a raw exponential-moment bound. Our generators draw centred Gaussian rows with unit variances, which satisfy Condition 1 itself" | E1 | CORRECT | With a_i ≡ δ and mean n: E exp(Z²) ≥ exp(δ²n²) → ∞. |
| 40 | s5:205–207 | "Condition 1, whose worked case is a zero-mean Gaussian process (p. 953)" | E1 | CORRECT | |
| 41 | s5:218 | "The start law must see every true predictor, as their first stage must" | G3, G8 | CORRECT+n | SL's stage 1 needs Cond 5 for the iterative screening (p. 958); not a theorem. |
| 42 | s5:225–226 | "SL's Condition 5 is the marginal case of visibility only, and their remark (a) on the leakage set is not a hypothesis" | G3, G4 | CORRECT | |
| 43 | s5:254–256 | quote: "if there are p_n predictors correlated with the true predictor X_t, p_n ≺ P_n, then there are at most c p_n predictors to be selected" (p. 958) | G4 | CORRECT | Verbatim up to a truncated end (omits "into X_s̃ for some constant c"). In SL, X_t is bold: "the set of all true predictors". |
| 44 | s5:255–256 | "Their results on their sampler's output carry no design condition of this kind (supp. pp. 9–10, 12–13, 16–17)" | I3–I8 | CORRECT | No design condition appears in the sampler statements. Design conditions appear only in Thm S, on the posterior mode. |
| 45 | s5:263–266 | "Floor on Q ∪ {l} … of the kind of SL's Condition 3 (p. 955) and (22) (supp. p. 13), on other sets"; "Local regressions: no counterpart (… local search, which SL do not analyse)" | F1, F3, I5 | CORRECT | SL's proposals are birth/death/exchange with weights from single-predictor deviances (supp. pp. 10–11); no analysis of a local search. |
| 46 | supplement:55–56 | beta-min "has the same form as SL's proof rates, with a fixed multiple of log n where theirs has a diverging multiple of r̄_n log P_n (supp. p. 15)" | B7 | CORRECT | From n·l_n·c² ≻ log r̄_n + r̄_n log P_n (supp. p. 15). |
| 47 | supplement:56–57 | "SL's Theorem 1 bounds the coefficients above through (3) and (8) (pp. 950, 952)" | B1, B4 | CORRECT+n | (3) bounds ‖β*‖₁. (8) bounds the ℓ1 tail beyond the best r_n terms, not the size of coefficients; "bounds above" is loose for (8). |
| 48 | supplement:345 | NL: "In no regime do SL have a condition of this kind: none of their theorems concerns a start law" | all theorems | CORRECT | SL do accept leakage in stage 1 (remark (a), p. 958). |

**Totals: 48 citation rows checked** (a table row and its prose twin are merged into one row). Verdicts: CORRECT 29; CORRECT+n 12 (#1, 2, 7, 14, 16, 18, 19, 24, 28, 29, 41, 47); **OVERSTATED 3** (#3, #10, #31); **WRONG 3 rows covering 2 distinct claims** (#34 Condition 3 "theirs gives ours"; #37 and #38 "for every r" in the Condition 1 comparison; #38's constants are right, only the "every r" is wrong); UNVERIFIABLE 1 (#4).

---

## 3. Flags

Ranked by how much a referee could embarrass the manuscript with them. Each is a reason to reword; none touches a theorem of ours.

**F1 — WRONG: s5:174–177, "theirs gives ours" for Condition 3.**
- Condition 3 (p. 955) is a *one-coordinate* identifiability condition: a given predictor x_k, at a vanishing level δ_n ≻ ε_n², is not mimicked by r̄_n others. It does not bound the smallest eigenvalue of any set of null predictors. Counterexample: two exactly duplicated null columns independent of x_k satisfy Condition 3 but violate the floor c_ψ/n on {a, b}.
- Only (22) (supp. p. 13) gives a floor on all sets of size \|t\| + r̄_n, at level n l_n ≻ r̄_n log P_n. That is above our c_ψ/n once r̄_n ≥ 3(A+1)(s+1) log n. But (22) is a condition on the *realised* X, while our Assumption dist(d) is on the *population* correlation; a sample floor does not imply a population floor.
- Suggested rewording: "(22) gives a sample-level floor at a higher level on the sets it covers; Condition 3 gives none on null sets."
- Also keep the direction in s5:156–157 (ours ⇒ Cond 3), which is correct.

**F2 — WRONG as worded: s5:194–199, "implies Condition 1 for every r".**
- SL's Condition 1 concerns all subvectors of size r ≤ r̄_n. SGR constrains directions with at most 5(A+1)(s+1) log n nonzeros, and dist(c) at most q_n = ⌈C_q M log n⌉.
- The implication therefore needs r̄_n ≤ that window. SL's Cor 1 allows r̄_n ≺ log^k n (any k > 0) and ≺ n^q, so it fails there.
- It does hold in the manuscript's own "no larger" regime (s5:160: r̄_n + 1 ≤ 5(A+1)(s+1) log n), and for Gaussian rows for every r.
- The constants δ = √(3/8)/L, M = log 2 are right.

**F3 — OVERSTATED: s5:6–7 and s1:47, "nonzero coefficients that are not too small" as a shared kind.**
- No SL theorem states a lower bound. The table (s5:70) and s5:144 say so; the sentence at the top contradicts them. The idea appears only in proofs: supp. p. 6 (β*_t² δ_n step of Thm 3), supp. p. 15 (c = min\|β*_i\|, n l_n c² ≻ …).
- Their Thm S proof also implicitly bounds the signal above (supp. p. 14, B8: λ₂‖β*_t‖² = O(1)).
- Suggested rewording: "…and, in the proofs only, nonzero coefficients bounded away from zero".

**F4 — OVERSTATED: s5:156–157, "our fixed floor implies (22)–(23)" for random rows.**
- (22) is deterministic in the realised X. SL themselves note it "is hardly satisfied" (supp. p. 15) and replace it, for random designs, by (26) with failure probability < e^{−nC}; Thm S "still holds" with (26).
- For the fixed-design theorem the implication is direct. For random rows it holds only if our floor on the sample design is shown with probability ≥ 1 − e^{−nC}. For sub-Gaussian rows and O(log n)-size sets this seems plausible, but it is not what the sentence says.
- (23) is a relation r̄_n log P_n ≺ n l_n, not a design condition. It holds in the stated regime because r̄_n log P_n = O(log² n).

**F5 — Regime caveat: "where their sets are no larger than ours" (s5:156–161, 174–177).**
- Thm 2, hence Thm 3 and Condition 3, assumes r_n ≻ 1 (p. 953), so r̄_n ≥ r_n → ∞.
- The fixed-design regime \|t\| + r̄_n ≤ 2(A+1)s + 2 is therefore empty for Thm 3 / Condition 3. It can be non-empty only for Thm 1 and Thm S (which need only 1 ≤ r_n ≤ r̄_n), and for random rows with r̄_n ≲ log n.
- Worth one clause so a referee does not read the comparison as vacuous.

**F6 — Wording: s5:122, "theirs needs P_n ≻ n^θ".**
- p. 950 introduces it as a standing choice; it is not in the statements of Thms 1–3 or S, and no printed proof step uses it.
- What the statements force is P_n → ∞ via (13) (r_n ≺ P_n with r_n ≥ 1). Hence "bounded p is excluded" is right, but "needs P_n ≻ n^θ" is stronger than the paper requires.

**F7 — "Same distance" (s5:44): constants.**
- Main text (p. 952): d² = ∫(√f1 − √f2)², no ½.
- Supplement proofs (supp. p. 2, eq. (2); p. 5): d² = 1 − ∫√(f1 f2).
- The manuscript's d_H² = 1 − ∫√(ff*) matches the supplement's convention and is half of the main-text d². A one-line footnote "up to the factor √2 of the main text" would remove any doubt.

**F8 — Condition 5 is not a hypothesis of a numbered theorem either.**
- It is used only to justify the iterative screening ("Under assumption 5, this procedure ensures that all true predictors that are contained in X_s will be selected", p. 958). Theorem 4 / Cor 2 use Condition 4 and no multicollinearity.
- The manuscript flags remark (a) as "not a condition of any theorem" (s5:252–253, correct) but presents Condition 5 in the table as an SL hypothesis. One clause ("used for their iterative screening, not in a numbered theorem") would be fair.

**F9 — s3:255 and s1:39–41 (sampler statements).**
- SL's statements are: SAMC convergence "under mild conditions" cited to Liang et al. (2007) (supp. pp. 9–10); importance-weight estimates cited to Liang (2009) (supp. p. 10); q̂_j → q_j a.s. as N → ∞ (supp. pp. 12–13); Lemma S2 (supp. pp. 16–17), whose premises are convergence in distribution and an independent subsequence. None is verified for SAMC, an adaptive chain.
- They never say "exact arithmetic and ideal random numbers". The manuscript's phrase is an inference. Suggest "their statements are idealised limits whose conditions are cited, not verified".
- SL also give no theorem for the two-stage SAM procedure (FDR thresholds α1, α2 are not analysed; Thm 4 and Cor 2 are for a *fixed* subset size s: supp. p. 7 "Since the number of predictors s is fixed"). s1:38 says "a posterior" and is correct.

**F10 — Minor SL typos/inconsistencies (do not affect the manuscript, but useful if a reader checks).**
- supp. (19), p. 11: "r_n < P_n denotes the maximum model size", which is r̄_n.
- supp. p. 16: cites "Lemma A.2 of the Appendix", but the supplement has no appendix.
- p. 952: "standardized" together with \|x_i\| ≤ 1 would force \|x_i\| = 1 under unit variance.
- supp. numbering Theorem 2.1–2.4 / Corollary 2.1 = main-text Theorems 1–4 / Corollary 1.

**Not flagged (checked and fine).**
- s5:120–126 (dimension ranges, including the (log n)²/4 bound).
- s5:178–180 (ridge and (10)).
- s5:200–202 (raw Gaussian with mean n versus Condition 1).
- s5:216–217 (visibility ⇒ Condition 5; U = ∅ is allowed in \as{V}).
- s5:254–256 (remark (a) quote).
- s4:206–212 and s5:40–48 (conclusion comparisons).
- All page numbers cited.

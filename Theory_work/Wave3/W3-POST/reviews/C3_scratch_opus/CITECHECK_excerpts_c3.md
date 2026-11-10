# CITECHECK excerpts (W3-POST)


## STATEMENT.md:18 -> Scripts/SMC_BVS/core/v3_preprocess.R:111-127
```
  constant <- apply(X, 2, function(x) all(x == x[1]))   # dropped only if all entries are exactly equal
  kept <- which(!constant); dropped <- which(constant)
  base <- list(n = n, p_raw = p_raw, p = length(kept), kept = kept, dropped = dropped)
  if (!length(kept)) return(c(list(status = "no_predictors", hpm = integer(0)), base))
  if (all(y == y[1])) return(c(list(status = "y_constant", hpm = integer(0)), base))
  Xs <- matrix(0, n, length(kept)); cm <- cmu <- csd <- numeric(length(kept))
  centers <- vector("list", length(kept))
  for (a in seq_along(kept)) {
    s <- v3_standardise(X[, kept[a]])
    Xs[, a] <- s$z; cm[a] <- s$max; cmu[a] <- s$mean; csd[a] <- s$sd
    centers[a] <- list(s$centering)
  }
```

## STATEMENT.md:23 -> ARC/main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md:9-14
```
- Raw data (X^r, y^r), n ≥ 3, no constant column, non-constant y^r. C = I − 11ᵀ/n; D_x = diag of retained raw column sample SDs. Standardised X = CX^rD_x⁻¹, y = Cy^r/s_y with s_y² = ‖Cy^r‖²/(n−1); so ‖x_j‖² = ‖y‖² = n − 
- State space Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋). G_S = X_SᵀX_S = (n−1)R_S; z_S = X_Sᵀy; H_S = (n+1)G_S + I; D_S = det H_S/det(G_S+I); Q_S = yᵀy − n z_SᵀH_S⁻¹z_S; ν = 0.01 + n/2; a₀ = b₀ = 0.01.
- m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q_S)^{−ν}; w(k) = ½/C(2p−1, k); W_K = Σ_{k≤K} C(p,k)w(k); ϖ(S) = w(|S|)/W_K.
- F(S) = log[ϖ(S)m(S)]; Z = Σ_Ω ϖ(S)m(S); π(S) = e^{F(S)}/Z; BF(S) = m(S)/m(∅).
- Global HPM S† = argmax_Ω F (ties: smallest size, then lexicographic). Reported HPM Ŝ = the same rule over 𝒮, the set of all models ever scored (calibration, final run, rejected proposals, local scans); 𝒮_cal ⊆ 𝒮 is the
- Statistical model: y^r = α*1 + X^rβ* + ε; μ = CX^rβ* = Xθ*, θ* = D_xβ*; S₀ = supp β*, s₀ = |S₀|. Contrast-scale parameters θ = s_yβ, v = s_y²σ². P₀ is over ε; "joint probability" adds the algorithm's randomness. r_n :=
```

## STATEMENT.md:24 -> Scripts/SMC_BVS/core/cpp/v3_score.h:40-71
```
  D.n = n; D.p = p; D.K = std::min(p, n / 2); D.W = nwords(p);
  D.X.assign(X, X + (size_t)n * p);
  D.y.assign(y, y + n);
  D.orig = orig;
  D.G.assign((size_t)p * p, 0.0);
  for (int a = 0; a < p; ++a) {
    const double* xa = D.col(a);
    for (int b = a; b < p; ++b) {
      const double* xb = D.col(b);
      double s = 0;
      for (int i = 0; i < n; ++i) s += xa[i] * xb[i];
      D.G[(size_t)b * p + a] = s; D.G[(size_t)a * p + b] = s;
```

## STATEMENT.md:24 -> Scripts/SMC_BVS/core/cpp/v3_score.h:196-224
```
      for (int i = 0; i < n; ++i) { MH[(size_t)a * m + i] = s1 * xa[i]; MA[(size_t)a * m + i] = xa[i]; }
      MH[(size_t)a * m + n + a] = 1.0; MA[(size_t)a * m + n + a] = 1.0;
    }
    if (!householder_lower(MH, m, k, LH) || !householder_lower(MA, m, k, LA)) return false;
    finish_from_factors(S, LH, LA, o);
    return std::isfinite(o.logm);
  }
  // Common finish: log det from factor diagonals, Q by subtraction, recomputed by the non-negative form when small.
  void finish_from_factors(const std::vector<int>& S, const std::vector<double>& LH, const std::vector<double>& LA, ScoreOut& o) {
    int k = (int)S.size();
    double ldH = 0, ldA = 0, mxH = 0, mnH = POS_INF, mxA = 0, mnA = POS_INF;
    for (int a = 0; a < k; ++a) {
```

## STATEMENT.md:37 -> T03R:15-17
```
Put $q_k:=\binom pk w(k)$ ($0\le k\le p$) and, for every integer $m$ and $0\le s_0\le K$,
$$R_m:=\frac{\varpi(\{S\in\Omega:|S|>m\})}{\varpi(S_0)}=\sum_{k=m+1}^{K}\frac{q_k}{w(s_0)}\qquad(\text{empty sum}=0;\ W_K\text{ cancels}).$$
$R_m$ is a data-free number (it depends on $p$, $s_0$, $K$, $m$ only), and $R_m=0$ for $m\ge K$.
```

## STATEMENT.md:37 -> T03R:44-47
```
### Definition (new size cutoff)
For $s_0\le K$ and real $\omega$:
$$m^\sharp_n(\omega):=\min\{m\in\mathbb Z:\ m\ge s_0,\ R_m\le n^{-(s_0+1)/2}e^{-\omega}\},\qquad m^\sharp_n:=m^\sharp_n(\tfrac12\log n).$$
The minimum exists and $m^\sharp_n(\omega)\le K$, because $R_K=0$. It is computable exactly (`scripts/tail_bound.py`).
```

## STATEMENT.md:38 -> T03R:50-54
```
Assume $s_0\le K$, $\omega\ge0$, and $s_0\ge1$ in (ii)–(iii) ($n\ge5$ if $s_0=0$ in (i)).

**(i)** $s_0\le m^\sharp_n(\omega)\le\min\{K,\ m_n(\omega)\}$.

**(ii)** $m^\sharp_n(\omega)\le\min\Big\{K,\ s_0+\Big\lceil\dfrac{\log\binom p{s_0}+\frac{s_0+1}2\log n+\omega}{\log2}\Big\rceil\Big\}$.
```

## STATEMENT.md:42 -> T03R:79-85
```
**Theorem T02(i♯).** Assume G and R, and let $n$ be such that $s_0\le K$. For every integer $m$ define $\Theta^\sharp_{n,m}\ge0$ by
$$\Pi(|S|>m\mid y)=R_m\,(n+1)^{s_0/2}\sqrt n\;\Theta^\sharp_{n,m}\quad\text{if }R_m>0,\qquad\Theta^\sharp_{n,m}:=0\ \text{ if }R_m=0 .$$
Then for every $L>c^{\sharp2}$,
$$\sup_m P_0(\Theta^\sharp_{n,m}>L)\ \le\ \frac{8+24M/\sigma_*^2}{n-1}+\frac1{\sqrt L}+\frac{C_\Lambda}{\log(\sqrt L/c^\sharp)} .$$
Consequently $\lim_{L\to\infty}\limsup_n\sup_mP_0(\Theta^\sharp_{n,m}>L)=0$, and for every deterministic real sequence $\omega_n$,
$$\Pi(|S|>m^\sharp_n(\omega_n)\mid y)\le(1+\tfrac1n)^{s_0/2}e^{-\omega_n}\,\Theta^\sharp_{n,m^\sharp_n(\omega_n)}=O_{P_0}(e^{-\omega_n}).$$
(When $R_m=0$, $\{S\in\Omega:|S|>m\}=\emptyset$ because $\varpi>0$ on $\Omega$, so $\Pi(|S|>m\mid y)=0$ and the definition is consistent.) The inequality is non-asymptotic: it holds at every $n$ with $s_0\le K$.
```

## STATEMENT.md:43 -> Theory_work/State_of_Project/sections/04_theory.tex:771-771
```
\textbf{Status (registry, verbatim):} \status{T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ON
```

## STATEMENT.md:58 -> Theory_work/Wave2/SR/BLIND_fable.md:92-93
```
**Lemma A (design-free size reduction) — the new ingredient.** Under A1–A3 only (no condition on X at all),
π(|S| > k_n | y) → 0 in probability, with k_n as in A4.
```

## STATEMENT.md:62 -> T03R:9-9
```
Throughout: $N=n-1$, $K=\min(p,\lfloor n/2\rfloor)$, $w(k)=\tfrac12/\binom{2p-1}{k}$, $\varpi(S)=w(|S|)/W_K$, $r_n=\sqrt{\log n/n}$, $m_n(\omega)=\lceil(s_0\log(2p)+(s_0+1)(\log n)/2+\omega)/\log 2\rceil$ (00_COMMON). We
```

## STATEMENT.md:76 -> Theory_work/State_of_Project/sections/04_theory.tex:780-788
```
\begin{stmt}{NBH/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:448-451}
\par\smallskip\noindent\textbf{R1, R.}\enspace Fixed-design triangular array, fixed \(s_0\ge1\), \(p\le n^A\) for fixed \(A\), \(s_0\le K\) eventually; G; \(\mu=X\theta^*\), \(\Vert\mu\Vert^2\le Mn\), and normalized trut
\par\smallskip\noindent\textbf{Tail cutoff.}\enspace With per-model prior weight \(w(k)\), \(R_m=\sum_{k=\max(m+1,0)}^K\binom pk w(k)/w(s_0)\), and \(m_n^\sharp=\min\{m\ge s_0:R_m\le n^{-(s_0+2)/2}\}\). It is determinist
\par\smallskip\noindent\textbf{Anchored eigenvalues.}\enspace \(j_0=\lceil(2A+1)s_0\rceil+1\). SE\(_\lambda(j_0)\): every \(S_0\cup J\), \(\lvert J\rvert\le j_0\), has normalized minimum eigenvalue at least \(\phi_0^2\).
\par\smallskip\noindent\textbf{Signal thresholds.}\enspace BM-∞: \(\theta_{\min}^{*2}n\phi_0^2/(\sigma^2\log n)\to\infty\). Alternatively BM\((c)\) uses a fixed \(c>c_0(s_0,A)\), with \(c_0=\max\{4C_*,32[s_0(A+1)+2]\}\),
\end{stmt}

\begin{stmt}{NBH/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:462}
\par\smallskip\noindent\textbf{Final statement.}\enspace Under R1, G, R, SE\(_\lambda(j_0)\), SE\(_w(m_n^\sharp;g_0)\), and BM-∞ or BM\((c>c_0)\), \(1-\pi(S_0)=O_P(\sqrt{\log n/n})\); exact HPM and MPM are consistent. Wi
```

## STATEMENT.md:76 -> T03R:162-168
```
**Hypotheses.** Regime R1 (triangular array, $n\to\infty$, $s_0$ fixed, $p=p_n\le n^A$); **G**; **R**; **SE$_\lambda(j_0)$**; **SE$_w(m^\sharp_n;g_0)$** for a fixed $g_0>0$; and, for (i)–(iii), a beta-min condition in on
- **BM-∞**: $\min_{j\in S_0}\theta^{*2}_j\ge M_n\sigma_*^2\log n/(n\varphi_0^2)$ with $M_n\to\infty$;
- **BM($c$)**: the same with a fixed constant $c>c_0(s_0,A)$, where $c_0(s_0,A)<\infty$ depends only on $s_0$ and $A$ (the proof gives $c_0=L_*=\max\{4C_*,32[s_0(A+1)+2]\}$ with $C_*$ of [P3]; this value is a proof artef

No hypothesis H-T02: T02(i♯) (§2) is proved and used directly.

**Conclusions.** (i) $1-\pi(S_0)=O_{P_0}(r_n)$. (ii) $\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|\le1-\pi(S_0)$ for every data set; $P_0(\mathrm{MPM}=S_0)\to1$. (iii) $P_0(S^\dagger\ne S_0)\le2E_0[1-\pi(S_0)]\to0$; on $
```

## STATEMENT.md:77 -> Theory_work/State_of_Project/sections/04_theory.tex:771-771
```
\textbf{Status (registry, verbatim):} \status{T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ON
```

## STATEMENT.md:87 -> T03R:149-149
```
**Statement.** In R1 under G, R and SE$_w(m^\sharp_n;g_0)$: $\Pi(\{S\in\Omega:S\supsetneq S_0\}\mid y)=O_{P_0}(r_n)$.
```

## STATEMENT.md:109 -> POST:12-18
```
ε ~ N(0, σ²I) independent of the raw design. (Raw-scale convention, fixed raw slopes with |β_j| ∈ [b_lo, b_hi] and unit population variances [R02-3]: then
θ* = D_xβ is raw-design-measurable; use the raw-design event 𝒢_n ∩ ℋ_n, ℋ_n := {all sample/population sd ratios in
[½, 2]} (P(ℋ_n) → 1 by χ² tails and p ≤ n^A), take θ_lo = b_lo/2, θ_hi = 2b_hi, and run the diagonal argument over
raw-design sequences; otherwise unchanged.) For the standardised-signal convention: conditionally on X, Y is
Gaussian on the centred contrast space with mean Xθ* and noise variance σ², so the posterior's noise kernel depends
only on X and the supremum over standardised designs below is legitimate [R02-4] (model G with β := D_x⁻¹θ*, which is
raw-design-measurable, not X-measurable).
```

## STATEMENT.md:111 -> POST:23-33
```
**Hypothesis LSF (logarithmic sparse floor).** (i) λ_min(Σ_{n,S}) ≥ φ² for every S with |S| ≤ min(p, s₀ + j₀),
for a fixed φ ∈ (0, 1]; and (ii) λ_min(Σ_{n,S}) ≥ ψ_n for every S with |S| ≤ k̄_n, where
ψ_n √n/(log n)^{3/2} → ∞. (If λ_min(Σ_n) ≥ c > 0 for all n, both hold with φ² = ψ_n = c.)

## Lemma POST
**(a)** Under LSF there are X-measurable events 𝒜_n with P(𝒜_n) → 1 on which every design satisfies the T03♯
hypotheses R (with M := s₀²θ_hi² + 1 and φ₀² := φ²/2), SE_λ(j₀) (φ₀²), SE_w(m♯_n; g₀) (g₀ := 1), s₀ ≤ K, and BM-∞ with
the deterministic envelope θ_lo² nφ₀²/(σ² log n) → ∞ — with these common constants and envelope, for n ≥ n₀.
**(b)** Consequently, under the joint law of (raw design, ε): 1 − π(S₀) = O_P(√(log n/n)), and the conclusions of
SL1 (a)–(e) hold with r_n = √(log n/n) (PIP sure screening and specificity uniformly in j, MPM, ξ_q for fixed q ∈ (0, 1) or
deterministic q_n with r_n = o(min(q_n, 1 − q_n)) only, exact HPM, model size); without beta-min (θ*_j allowed to vary, some → 0) the inclusion clause for J_n(c) holds likewise.
```

## STATEMENT.md:120 -> SL:20-63
```
## 1. Lemma SL0 (deterministic; every data set, every n)
(i) For every j: |PIP_j − 1{j ∈ S₀}| ≤ δ. Hence max_{j∈S₀}(1 − PIP_j) + max_{j∉S₀} PIP_j ≤ 2δ.
(ii) For every A ⊆ [p]: |π({S : A ⊆ S}) − 1{A ⊆ S₀}| ≤ δ. If S₀ ∈ Ω, for every h : Ω → ℝ: |π(h) − h(S₀)| ≤ δ·osc(h),
osc(h) := max_Ω h − min_Ω h; in particular sup_{h:Ω→[0,1]} |π(h) − h(S₀)| = TV(π, point mass at S₀) = δ.
(iii) For every q ∈ (0,1): δ < min(q, 1 − q) ⇒ ξ_q = S₀. In particular δ < ½ ⇒ MPM = S₀.
(iv) δ < ½ ⇒ S₀ is the unique maximiser of π (HPM = S₀ for every tie rule).
(v) π({S : |S| = s₀}) ≥ 1 − δ.
(vi) (R34 #1 text) As a bound over arbitrary probability laws on Ω, the constant 2 in (i) is sharp when 1 ≤ s₀ ≤ K and
s₀ < p. Put mass 1−δ on S₀ and δ on a feasible one-for-one swap. This is not an attainment claim for the strictly
positive finite-data D0 posterior. (For a D0 posterior every model, incl. ∅, has positive mass, so for nonempty proper
feasible S₀, PIP_k ≤ δ − π(∅) < δ for k ∉ S₀ and the max-sum is < 2δ; sharpness *within* D0 is not claimed.)

```

## ASSUMPTION_MAP.md:22 -> Theory_work/State_of_Project/sections/04_theory.tex:816-816
```
\item ``no expectation rate inferred from $O_P$, no universal onset $n_0$, no random-design or growing-sparsity extension'' (Repairs row). $p\le n^A$ comes ``from the prior and proof technique; $e^{Cn^{\alpha}}$ OPEN'' (
```

## ASSUMPTION_MAP.md:30 -> T03R:134-134
```
These are restrictions of SE to the **comparison unions** $S\cup S_0$ used by the proofs. The locked SE (all $T$ with $|T|\le\min(p,m_n+s_0)$, constant $\varphi_0^2$) implies SE$_\lambda(j_0)$ (as $j_0\le m_n$ for large 
```

## lemmas\L1a_size_tail.md:14 -> T03R:77-77
```
$$c^\sharp:=\kappa^2/(c_{\rm IG}\sigma_*^2).$$
```

## lemmas\L1a_size_tail.md:22 -> T03R:93-97
```
*Proof of T02(i♯).* Fix $n$ with $s_0\le K$ and an integer $m$ with $R_m>0$ (otherwise there is nothing to prove). Put $E_m=\{|S|>m\}$, $v_m:=\varpi(E_m)=R_m\varpi(S_0)>0$, $N_m:=I_{b_-}(E_m)/f_0(y_c)$ and $\Theta^{(1)}_
$$\Pi(E_m\mid y)\le\kappa^2\frac{I_{b_-}(E_m)}{\varpi(S_0)m^c_{b_+}(S_0)}=\kappa^2\frac{v_m\Theta^{(1)}_{n,m}}{\varpi(S_0)\,m^c_{b_+}(S_0)/f_0(y_c)}\le R_m(n+1)^{s_0/2}\sqrt n\cdot c^\sharp e^{\Lambda_n}\Theta^{(1)}_{n,m
So on $\mathcal B_n$, $\Theta^\sharp_{n,m}\le c^\sharp e^{\Lambda_n}\Theta^{(1)}_{n,m}$. For $L>c^{\sharp2}$, $\{c^\sharp e^{\Lambda_n}\Theta^{(1)}>L\}\subseteq\{\Theta^{(1)}>\sqrt L\}\cup\{c^\sharp e^{\Lambda_n}>\sqrt L
$$P_0(\Theta^\sharp_{n,m}>L)\le P_0(\mathcal B_n^c)+P_0(\Theta^{(1)}_{n,m}>\sqrt L)+P_0\big(\Lambda_n>\log(\sqrt L/c^\sharp)\big)\le P_0(\mathcal B_n^c)+\frac1{\sqrt L}+\frac{C_\Lambda}{\log(\sqrt L/c^\sharp)},$$
by Markov's inequality ($\Theta^{(1)}\ge0$, $\Lambda_n\ge0$). $P_0(\mathcal B_n^c)\le(8+24M/\sigma_*^2)/(n-1)$ by [P1] `thm:T01iii`. The right side does not depend on $m$. For the consequence take $m=m^\sharp_n(\omega_n)
```

## lemmas\L1a_size_tail.md:24 -> T03R:89-91
```
**Lemma den′** (= [P1] `lem:den` without its last factor). Under G, R and $s_0\le K$, with $\Lambda_n$ as in [P1] `lem:den`,
$$\frac{m^c_{b_+}(S_0)}{f_0(y_c)}\ \ge\ (n+1)^{-s_0/2}\,c_{\rm IG}\,\sigma_*^2\,n^{-1/2}e^{-\Lambda_n},\qquad E_0\Lambda_n\le C_\Lambda .$$
*Proof.* This is exactly what the paragraphs "Bound on $Q^c_{S_0}$", "Integral representation", "Lower bound on the exponent" and the first two sentences of "Assembling" in the proof of [P1] `lem:den` establish: restrict
```

## lemmas\L1a_size_tail.md:39 -> T03R:93-97
```
*Proof of T02(i♯).* Fix $n$ with $s_0\le K$ and an integer $m$ with $R_m>0$ (otherwise there is nothing to prove). Put $E_m=\{|S|>m\}$, $v_m:=\varpi(E_m)=R_m\varpi(S_0)>0$, $N_m:=I_{b_-}(E_m)/f_0(y_c)$ and $\Theta^{(1)}_
$$\Pi(E_m\mid y)\le\kappa^2\frac{I_{b_-}(E_m)}{\varpi(S_0)m^c_{b_+}(S_0)}=\kappa^2\frac{v_m\Theta^{(1)}_{n,m}}{\varpi(S_0)\,m^c_{b_+}(S_0)/f_0(y_c)}\le R_m(n+1)^{s_0/2}\sqrt n\cdot c^\sharp e^{\Lambda_n}\Theta^{(1)}_{n,m
So on $\mathcal B_n$, $\Theta^\sharp_{n,m}\le c^\sharp e^{\Lambda_n}\Theta^{(1)}_{n,m}$. For $L>c^{\sharp2}$, $\{c^\sharp e^{\Lambda_n}\Theta^{(1)}>L\}\subseteq\{\Theta^{(1)}>\sqrt L\}\cup\{c^\sharp e^{\Lambda_n}>\sqrt L
$$P_0(\Theta^\sharp_{n,m}>L)\le P_0(\mathcal B_n^c)+P_0(\Theta^{(1)}_{n,m}>\sqrt L)+P_0\big(\Lambda_n>\log(\sqrt L/c^\sharp)\big)\le P_0(\mathcal B_n^c)+\frac1{\sqrt L}+\frac{C_\Lambda}{\log(\sqrt L/c^\sharp)},$$
by Markov's inequality ($\Theta^{(1)}\ge0$, $\Lambda_n\ge0$). $P_0(\mathcal B_n^c)\le(8+24M/\sigma_*^2)/(n-1)$ by [P1] `thm:T01iii`. The right side does not depend on $m$. For the consequence take $m=m^\sharp_n(\omega_n)
```

## lemmas\L1a_size_tail.md:63 -> T03R:103-121
```
## 3. Proposition D: COUNTEREXAMPLE to the target scale without SE (COUNTEREXAMPLE, reproducible)

**Design.** $n\ge3$, $2\le p$ (e.g. $p=n$, so $A=1$), $x\in\mathbb R^n$ fixed with $\|Cx\|^2=n-1$, $X^r=[x,\dots,x]$ ($p$ identical columns), $\beta^*=(\beta_1,0,\dots,0)$ with fixed $\beta_1\ne0$, any $\alpha^*$, $\sigm

**Claim.** With $E_n:=\{m(\emptyset)\le m(\{1\})\}$, $P_0(E_n)\to1$, and on $E_n$, for every integer $0\le m\le K-1$,
$$\Pi(|S|>m\mid y)\ \ge\ 2^{-(m+4)}\exp\Big\{-\frac{m(m-1)}{4(p-m)}\Big\}.$$
Consequently, for any deterministic $m_n\le\sqrt p$ with $\Pi(|S|>m_n\mid y)=O_{P_0}(n^{-1/2})$, necessarily $m_n\ge\frac12\log_2n-O(1)$; in particular no cutoff $m_n=s_0+O(s_0\log n/\log p)=1+O(1)$ (here $p=n$) works, a

*Proof.* Let $S$ have $|S|=k\ge1$. Then $X_S=\tilde x\mathbf 1_k^\top$, $G_S=N\mathbf 1\mathbf 1^\top$ (eigenvalues $kN,0,\dots,0$), so $D_S=\frac{(n+1)kN+1}{kN+1}=:D_k$; $H_S=(n+1)N\mathbf 1\mathbf 1^\top+I$ has $\mathb

*Two-sided comparison of $m_k$, $k\ge1$, with $m_1$ (deterministic).* $D_k\le n+1$ and $D_1\ge\frac{(n+1)N}{N+1}$, so $(D_1/D_k)^{1/2}\ge(N/(N+1))^{1/2}\ge(2/3)^{1/2}$; and $k\mapsto\frac k{(n+1)Nk+1}$ is increasing, so 

```

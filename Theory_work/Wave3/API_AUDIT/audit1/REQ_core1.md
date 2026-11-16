# AUDIT1 — core1: rows 1.1, 1.2, 1.3 (Theorems 1, 1′, 2, 3: the posterior finds the true model; the rate)

Material for a blind review of the audit's Song–Liang comparisons and inside/outside verdicts. Every excerpt is
verbatim with its file and line numbers; Song–Liang passages carry the journal page and display or condition
number. Status labels have been replaced by [status omitted] or [review omitted].

## 0. Conventions
Meaning of inside / outside (the audit's convention):
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 55–57:
```
   55| "Inside / outside" means: the design, continued as a sequence in n with its structure and s₀ fixed, satisfies the
   56| assumption. The dossiers judge the qualitative conditions (a floor bounded below, a signal on the √(log n/n) scale, a
   57| leakage set of size n^b). The explicit constants in the proofs are conservative and are not part of the judgement
```

Track C = internal proxy computations on simulated designs (no proofs, no fits of the method). Legend of its table:
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 13–18:
```
   13| ## How to read
   14| Trend is along the p = n series, n = 200 → 1600 (log-log slope in brackets). **IN↑** = inside, improving with n;
   15| **IN** = inside, bounded/flat; **UNCL↑** = unclear now, moving toward inside; **UNCL** = unclear; **OUT** = outside.
   16| Search-based floors and visibility are upper bounds (they can refute, not certify); population floors are certified by
   17| λ_min(Σ) > 0; P5 leak sets are subsets (never "inside", only "not refuted"; written IN for brevity). sp = spread truth
   18| (study positions, signs + − + −), cl = clustered (four adjacent columns, aligned signs).
```


## 1. Our theorem statements (verbatim)
Standing assumptions (S1), (S2) of the reader versions:
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 28–29:
```
   28| (S1) Model of §1 of the notation: Gaussian errors with fixed variance $\sigma_*^2>0$, independent of the design.
   29| (S2) Asymptotics: $n\to\infty$, $p=p_n$ with $2\le p\le n^A$ for a fixed $A\ge1$ ($p\gg n$ allowed).
```

Reader statement of Theorem 1 and Theorem 1′ (row 1.1):
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 103–134:
```
  103| **Theorem 1.** Let the design be fixed. Assume
  104| - **(A1) Model.** (S1) and (S2).
  105| - **(A2) Sparsity.** $s_0\ge1$ is fixed.
  106| - **(A3) Bounded coefficients.** $\max_{j}|\theta^*_j|\le\bar\theta$ for a fixed $\bar\theta<\infty$.
  107| - **(A4) Sparse eigenvalue floor.** $\lambda_{\min}(\hat R_S)\ge\varphi_0^2$ for every $S\subseteq[p]$ with
  108|   $|S|\le 2(A+1)s_0+2$, for a fixed $\varphi_0\in(0,1]$.
  109| - **(A5) No near-collinearity among $O(\log n)$ columns.** $\lambda_{\min}(X_S^\top X_S)\ge g_0$ for every $S$ with
  110|   $|S|\le 3(A+1)(s_0+1)\log n$, for a fixed $g_0>0$.
  111| - **(A6) Beta-min.** $\theta^*_{\min}\ge C_\beta\,\sigma_*\sqrt{\log n/n}$ with a fixed $C_\beta>0$ such that
  112|   $C_\beta^2\varphi_0^2>c_0(s_0,A)$ [S1-F1]; or $\theta^*_{\min}\sqrt{n/\log n}\to\infty$.
  113| 
  114| Then there are $n_0$ and $C$, depending only on $(s_0,A,\sigma_*^2,\bar\theta,\varphi_0,g_0,C_\beta)$, such that for every
  115| $n\ge n_0$ and every design and $\theta^*$ satisfying (A1)–(A6) at that $n$ [H5-1]
  116| $$
  117| E\big[1-\pi(S_0\mid y)\big]\ \le\ C\sqrt{\tfrac{\log n}{n}},
  118| $$
  119| and consequently, along any sequence satisfying (A1)–(A6),
  120| $$
  121| P\big(\mathrm{HPM}=\mathrm{MPM}=S_0\big)\ \ge\ 1-4C\sqrt{\tfrac{\log n}{n}}\ \to1,\qquad
  122| \max_{j\le p}\big|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}\big|\le 1-\pi(S_0\mid y)=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big).
  123| $$
  124| (Expectation over the noise, design fixed. With the second form of (A6), $n_0$ depends also on the divergence of
  125| $\theta^*_{\min}\sqrt{n/\log n}$.)
  126| 
  127| **Theorem 1′ (no eigenvalue condition off $S_0$ beyond the vanishing floor (A5)).** Replace (A4) by
  128| - **(A4′) Floor on the truth and an identifiability margin.** $\lambda_{\min}(\hat R_{S_0})\ge\varphi_0^2$, and every model
  129|   $S$ with $|S|\le K$, $S_0\not\subseteq S$ and at most $j_0:=\lceil(2A+1)s_0\rceil+1$ variables outside $S_0$ leaves
  130|   residual signal $\|(I-P_S)X\theta^*\|^2\ge c\,\sigma_*^2\log n$, with a fixed $c>c_1(s_0,A)$, where $c_1(s_0,A)$ is an
  131|   explicit constant, not optimised [H5-6],
  132| 
  133| and drop (A6). Then the conclusions of Theorem 1 hold (the expectation bound with constants depending on
  134| $(s_0,A,\sigma_*^2,\bar\theta,\varphi_0,g_0,c)$). [H5-1]
```

Reader statement of Theorem 2 (row 1.2):
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 269–285:
```
  269| **Theorem 2.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a correlation matrix, and
  270| assume
  271| - **(A1) Model.** (S1) and (S2).
  272| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ is fixed and $b_{\mathrm{lo}}\le|\beta^*_j|\le b_{\mathrm{hi}}$ for
  273|   $j\in S_0$, with fixed $0<b_{\mathrm{lo}}\le b_{\mathrm{hi}}<\infty$.
  274| - **(A3) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge\varphi^2$ for every $S$ with
  275|   $|S|\le 5(A+1)(s_0+1)\log n$, for a fixed $\varphi\in(0,1]$ (for instance, $\lambda_{\min}(\Sigma_n)\ge\varphi^2$).
  276| 
  277| Then, under the joint law of design and noise, the three conclusions of Theorem 1 hold:
  278| $$
  279| 1-\pi(S_0\mid y)=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big),\qquad P(\mathrm{HPM}=\mathrm{MPM}=S_0)\to1,\qquad
  280| \max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big).
  281| $$
  282| 
  283| *Remarks.* No upper eigenvalue bound on $\Sigma_n$ and no beta-min beyond (A2) are needed; $p\gg n$ is allowed. The
  284| master allows the floor on sets of size $O(\log n)$ to vanish slowly ($\psi_n\gg(\log n)^{3/2}/\sqrt n$); the reader
  285| version uses a constant for simplicity.
```

Reader statement of Theorem 3 (row 1.3):
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 333–356:
```
  333| **Theorem 3.** (a) *(Every design.)* For every $n\ge3$, every standardised design with $p\ge2$, every response and every
  334| model $S$ with $|S|\le\min(K-1,p/2)$,
  335| $$
  336| \pi(S\mid y)\ \le\ \Big(1+\frac{|S|+1}{3\sqrt n}\Big)^{-1}.
  337| $$
  338| (b) *(Orthogonal or Gaussian null columns.)* Assume (S1), $s_0$ fixed, $\|X\theta^*\|^2\le nM$ and
  339| $\|\theta^*\|^2\le nM'$ with fixed $M,M'$, and either
  340| - **(N-orth)** the columns outside $S_0$ are mutually orthogonal and orthogonal to the columns in $S_0$; or
  341| - **(N-gauss)** the raw columns outside $S_0$ have i.i.d. $N(0,1)$ entries, independent of $X^{\mathrm r}_{S_0}$ and
  342|   $\varepsilon$, and $p\le n^A$.
  343| 
  344| Then, for every $p$ with $s_0<p$ (bounded or growing),
  345| $$
  346| \mathbb E\big[1-\pi(S_0\mid y)\big]\ \ge\ (1-o(1))\,(s_0+1)\,\frac{2(p-s_0)}{2p-1-s_0}\,\sqrt{\frac{\log\!\big(p\sqrt n/(s_0+1)\big)}{\pi n}},
  347| $$
  348| and, if moreover $p\to\infty$,
  349| $$
  350| 1-\pi(S_0\mid y)\ \ge\ (1-o_P(1))\,(s_0+1)\sqrt{\frac{\log p}{\pi n}}.
  351| $$
  352| 
  353| *In words (headline).* The rate of Theorem 1 cannot be improved under its assumptions: on orthogonal or Gaussian null
  354| columns, $E[1-\pi(S_0\mid y)]\ge c\cdot(s_0+1)\cdot\sqrt{\log n/n}$, for every $p$. Here $c>0$ depends only on $s_0$, and does
  355| not depend on $s_0$ when $s_0\le p/2$. The $\sqrt{\log n}$ bounds hold on these null-column designs only; on every design
  356| only the order $n^{-1/2}$ of part (a) is proved.
```

Master: the target posterior π and the truth (prior, standardisation, outputs):
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 18–34:
```
   18| Data (X^r, y^r), n ≥ 3, with non-constant y^r (s_y > 0; a.s. under G) [R01-4]. p = number of **retained** (non-constant)
   19| raw columns (the code drops constant columns before K and the prior are formed, `Scripts/SMC_BVS/core/v3_preprocess.R:111-127`);
   20| X = CX^rD_x⁻¹ = standardised design of the retained columns (centred, ‖x_j‖² = n − 1), y = Cy^r/s_y with
   21| s_y² = ‖Cy^r‖²/(n − 1). Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋). G_S = X_SᵀX_S, H_S = (n + 1)G_S + I,
   22| D_S = det H_S / det(G_S + I), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S (z_S = X_Sᵀy), ν = 0.01 + n/2;
   23| m(S) ∝ D_S^{−1/2}(2b₀ + Q_S)^{−ν}, a₀ = b₀ = 0.01; prior ϖ(S) = w(|S|)/W_K, w(k) = ½/C(2p − 1, k) (capped BB(1, p));
   24| π(S) ∝ ϖ(S)m(S) on Ω. (Definitions: `ARC/main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md:9-14`; code:
   25| `Scripts/SMC_BVS/core/cpp/v3_score.h:40-71, 196-224` — K = min(p, n/2), ν = a₀ + n/2, H = (n+1)G + I, A = G + I,
   26| log w(k) = −log 2 − log C(2p−1, k).) Equivalently π is the exact posterior under the **working** likelihood
   27| y | S, β_S, σ² ~ N_n(X_Sβ_S, σ²I) with β_S | S, σ² ~ N(0, nσ²(G_S + I)⁻¹), σ² ~ IG(0.01, 0.01) on the standardised
   28| scale (the standardised y does not have this law under the truth; the proofs treat it as a working model, [P1]
   29| lines 155-221) [R01-4]. π is the real-arithmetic target of the code; floating-point fidelity is not part of this file.
   30| 
   31| Truth: y^r = α*1 + X^rβ* + ε, ε ~ N_n(0, σ*²I) (**G**), μ := CX^rβ* = Xθ*, θ* = D_xβ*, S₀ = supp θ*, s₀ = |S₀|,
   32| r_n := √(log n/n). Exact posterior outputs: δ_n := 1 − π(S₀) (π(S₀) := 0 if s₀ > K); PIP_j := π(j ∈ S);
   33| HPM := argmax_Ω π (any tie rule); MPM := {j : PIP_j > ½}; ξ_q := {j : PIP_j > q}. These are properties of π, not of the
   34| sampler.
```

Master Theorem 1 (hypotheses, conclusions 1–4, random-design item 6):
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 63–75:
```
   63| **Regime R1.** Triangular array, n → ∞; s₀ ≥ 1 fixed; 2 ≤ p = p_n ≤ n^A ([T03R] line 9 assumes p ≥ 2) [C1B-F3] for a fixed A ≥ 1 (p ≫ n allowed); s₀ ≤ K
   64| eventually; σ*² > 0 fixed; G.
   65| 
   66| **Hypotheses on (X, θ*)** (fixed design; fixed constants 0 < φ₀ ≤ 1, 0 < g₀ < ∞, 0 ≤ M < ∞ [R01-4]; j₀ := ⌈(2A + 1)s₀⌉ + 1):
   67| - **(E) energy**: ‖μ‖² ≤ nM.
   68| - **(F_λ) anchored floor, bounded size** = SE_λ(j₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}/(n−1)) ≥ φ₀² for every J ⊆ [p]∖S₀ with
   69|   |J| ≤ j₀ (J = ∅ included: this contains R's condition on S₀). *By interlacing it implies* λ_min(R_S) ≥ φ₀² for
   70|   **every** S with |S| ≤ j₀ (S ⊆ S₀ ∪ S), so it excludes e.g. duplicated null columns [R02-F2].
   71| - **(F_w) anchored unnormalised floor, logarithmic size** = SE_w(m♯_n; g₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ for every
   72|   J ⊆ [p]∖S₀ with |J| ≤ m♯_n (m♯_n = O(log n) under R1). By interlacing it implies λ_min(G_S) ≥ g₀ for every S with
   73|   |S| ≤ m♯_n: no exact linear dependence among ≤ m♯_n columns [R02-F2].
   74| - **(BM) beta-min**, either BM-∞: θ*²_min nφ₀²/(σ*² log n) → ∞; or BM(c): θ*²_min ≥ cσ*² log n/(nφ₀²) with a fixed
   75|   c > c₀(s₀, A) := max{4C_*, 32[s₀(A + 1) + 2]} (C_* the [P3] proof constant; a proof artefact, not sharp).
```
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 80–86:
```
   80| **Theorem 1.** In R1 under G, (E), (F_λ), (F_w):
   81| 1. **(Rate)** Under (BM): δ_n = 1 − π(S₀) = O_P(r_n).
   82| 2. **(Exact HPM, MPM, thresholded models)** Under (BM): P(HPM = S₀) ≥ P(δ_n < ½) → 1 and P(HPM ≠ S₀) ≤ 2Eδ_n → 0;
   83|    P(MPM = S₀) → 1; P(ξ_{q_n} = S₀) → 1 for every deterministic q_n ∈ (0, 1) with r_n = o(min(q_n, 1 − q_n)).
   84| 3. **(PIPs)** For every data set, max_j |PIP_j − 1{j ∈ S₀}| ≤ δ_n; under (BM) this is O_P(r_n) (sensitivity and
   85|    specificity uniformly in j), and E max_j |PIP_j − 1{j ∈ S₀}| → 0 (no expectation rate claimed).
   86| 4. **(Size, functionals)** Under (BM): π(|S| = s₀) = 1 − O_P(r_n); sup_{h:Ω→[0,1]} |π(h) − h(S₀)| = O_P(r_n).
```
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 95–100:
```
   95| 6. **(Random design, interface form)** [C1A-F7] Let (X, θ*) be random with ε independent of (X, θ*), and suppose there
   96|    are (X, θ*)-measurable events 𝒜_n with P(𝒜_n) → 1 on which |supp θ*| = s₀ [C2B-N2] and (E), (F_λ), (F_w) hold with common constants
   97|    (M, φ₀, g₀) and (BM) holds with a common c > c₀ or a common deterministic envelope M_n → ∞. Then 1–4 hold under the
   98|    joint law of (X, θ*, ε); if only (E), (F_λ), (F_w) hold on 𝒜_n, 5(a) and 5(b) hold under the joint law. (Proof:
   99|    apply the fixed-design statements along every deterministic sequence in 𝒜_n; the diagonal tightness transfer of
  100|    [POST] step (5) gives uniformity; add P(𝒜_nᶜ) → 0.)
```

Master Corollary 1R (Gaussian rows, LSF):
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 106–112:
```
  106| **Corollary 1R (a sufficient bridge for item 6; Gaussian rows — an example, not part of Theorem 1).** Let the raw rows
  107| be iid N(m, Σ_n), Σ_n a unit-diagonal correlation matrix, ε independent of the design, and **LSF** (fixed 0 < φ ≤ 1):
  108| (i) λ_min(Σ_{n,S}) ≥ φ² for |S| ≤ min(p, s₀ + j₀); (ii) λ_min(Σ_{n,S}) ≥ ψ_n for |S| ≤ k̄_n := min(p, s₀ + max(j₀, m̄_n)),
  109| m̄_n := ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n]/log(3/2)⌉ = O(log n), with ψ_n√n/(log n)^{3/2} → ∞.
  110| (a) With fixed 0 < b_lo ≤ |β_j| ≤ b_hi < ∞ on S₀ and the raw-design event of [POST] lines 12-18 (or fixed standardised
  111| 0 < θ_lo ≤ |θ*_j| ≤ θ_hi < ∞) [R01-4], the events of item 6 exist with φ₀² = φ²/2, g₀ = 1, M = s₀²θ_hi² + 1 and the
  112| envelope θ_lo²nφ₀²/(σ*² log n) → ∞ (raw case: θ_lo = b_lo/2, θ_hi = 2b_hi) [C3B-N5]; hence 1–4 hold under the joint law ([POST] Lemma POST(a)-(b), lines 23-33;
```

Master Theorem 1′ (Claim E):
`Theory_work/Wave3/W3-POST2/STATEMENT.md` @ e8b5351c, lines 126–133:
```
  126| ## Claim E (brief item 5, stretch) — Theorem 1-VIS: (F_λ) away from S₀ replaced by an identifiability margin
  127| 
  128| In R1 under G, (E), (F₀), (OS) and (ID^M; c) with c > c₁(s₀, A) — (ID^M; c): L_S := μ_cᵀ(I − M_S)μ_c ≥ cσ*² log n for every
  129| S ∈ Ω with S₀ ⊄ S, |S∖S₀| ≤ j₀; L_S = min_ϑ B_S(ϑ) ≥ Δ_S, so (ID; c) ⇒ (ID^M; c) (v1.2, R03b §D) — where
  130|   c₁ := (√(2C_x) + √(2C_x + C_A j₀ + (2/log 2)(s₀(A + 1) + 2)))²,  C_x := Aj₀ + s₀ + log(j₀ + 1) + 2,
  131| conclusions 1–4 of [W3P] Theorem 1 hold (δ_n = O_P(r_n); exact HPM = MPM = S₀ w.p. → 1; ξ_{q_n} = S₀ w.p. → 1 for
  132| deterministic q_n with r_n = o(min(q_n, 1 − q_n)); PIPs; size and functionals), and Claim C applies [L01-6]. Without (ID^M), (ID^M_j; c) gives π(S ∌ j) = O_P(r_n) (5(b) analog). Item 6
  133| (random design) as in [W3P]. No eigenvalue condition is imposed on any set other than S₀; (OS) holds e.g. under (DG).
```

Master Corollary B (Theorem 3(a)):
`Theory_work/Wave3/W3-PSHARP/STATEMENT.md` @ e8b5351c, lines 92–100:
```
   92| **Corollary B.** For every n ≥ 3, every standardised design with p ≥ 2, every data set and every S₀ ⊆ [p] with
   93| 0 ≤ s₀ ≤ K − 1 (deterministic; no law, no truth):
   94|   δ_n/(1 − δ_n) ≥ 𝒪^{lb}_n := Σ_{j=1}^{K−s₀} C(s₀ + j, j) n^{−j/2} Π_{i=0}^{j−1} (p − s₀ − i)/(2p − 1 − s₀ − i) ≥ c(p, s₀)/√n,
   95| equivalently π(S₀) ≤ 1/(1 + 𝒪^{lb}_n), and in particular π(S₀) ≤ √n/(√n + c(p, s₀)) [K01-F3]. Here c(p, s₀) ≥ (s₀ + 1)/3 whenever s₀ ≤ p/2; c(p, s₀) ≥ 1 for s₀ ≥ 1;
   96| c(p, 0) > ½; and c(p, s₀)/(s₀ + 1) → ½ when p → ∞ and s₀/p → 0 [L01-m1].
   97| 
   98| **Consequences** (any sequence with s₀ ≤ min(K − 1, p/2); any designs; any data, random or not):
   99| - **(B1)** π(S₀) ≤ [1 + (s₀ + 1)/(3√n)]⁻¹ surely. So π(S₀) → 1 (in probability, along any subsequence) forces
  100|   s₀ = o(√n); if s₀ ≥ λ√n then π(S₀) ≤ 1/(1 + λ/3); and if s₀/√n → ∞ then π(S₀) → 0 surely.
```


## 2. Our designs (verbatim)
The audit's summary of our designs:
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 40–48:
```
   40| **Our designs** (all have i.i.d. Gaussian rows, σ = 1, fixed nonzero coefficients):
   41| - **Study** = the 2,400-fit study: n = 200, p ∈ {500, 1000}, s₀ = 14 (one truth per group of 5, coefficients ±0.8…1.8
   42|   times c ∈ {1, 0.5}); S1 identity; S2 AR(1) 0.5; S3 / S4 blocks of 5 with correlation 0.7 / 0.85; S5 = blocks of 5 at 0.7
   43|   **plus a global factor** (0.3 between all columns); S6 blocks of 5 with correlation 0.4–0.9
   44|   (`Scripts/Data_generators/gen_dev_data.R:18-41`; `Theory_work/Pause_2026-11/RERUN_SPEC.md:41-42`).
   45| - **P6** = strong factors, n ∈ {50,…,150}, p up to 10n, s₀ ∈ {4, 8}: `cs(ρ)` one factor, ρ ∈ {0.3, 0.5, 0.7}; `fac2` two
   46|   pervasive factors; `s5` (= S5) (`Theory_work/Wave3/W3-P6/DESIGN.md:13-17`).
   47| - **1M** = the p = 10⁶ plan: IND; AR Toeplitz 0.6 (primary); BLK blocks of 20 at 0.5; FAC `cs(0.3)` (contingent, 10⁴
   48|   only); s₀ = 5 (`/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/EXPERIMENT_PLAN.md:87-92`, untracked).
```

Generator of the 2,400-fit study (scenarios S1–S6 = cases 1–6; truth):
`Scripts/Data_generators/gen_dev_data.R` @ e8b5351c, lines 18–41:
```
   18| scenario_covariance <- function(scenario, p=500L) {
   19|   stopifnot(length(scenario)==1L, scenario %in% 1:6, p>=1L, p==as.integer(p))
   20|   group <- ceiling(seq_len(p)/5)
   21|   H <- outer(group,group,"==")
   22|   I <- diag(p)
   23|   switch(as.integer(scenario),
   24|     I,
   25|     0.5^abs(outer(seq_len(p),seq_len(p),"-")),
   26|     0.7*H+0.3*I,
   27|     0.85*H+0.15*I,
   28|     0.3*matrix(1,p,p)+0.4*H+0.3*I,
   29|     {rho <- 0.4+0.1*((group-1L)%%6L); S <- H*matrix(rho,p,p); diag(S)<-1; S})
   30| }
   31| 
   32| # Port of tools/scenario_check.py::truth (§II.3, §II.9). Uses no random numbers.
   33| truth <- function(p) {
   34|   s0   <- c(`30` = 5L, `500` = 14L, `1000` = 14L)[[as.character(p)]]
   35|   step <- c(`30` = 1L, `500` = 7L, `1000` = 13L)[[as.character(p)]]
   36|   pos  <- c(3L, 2L, 4L, 1L, 5L, 3L)
   37|   pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
   38|   k <- 0:(s0 - 1L)
   39|   block <- 1L + step * k
   40|   active <- 5L * (block - 1L) + pos[(k %% 6L) + 1L]
   41|   list(active = active, beta = pattern[(k %% 6L) + 1L], block = block)
```

Study specification (designs, truth, signal):
`Theory_work/Pause_2026-11/RERUN_SPEC.md` @ e8b5351c, lines 37–42:
```
   37| | n | 200 | `RES/HEADLINE_H.md:3`; `ops/PRODH_COMPLETION_20261102.md:3` |
   38| | p | 500, 1000 | `CAMP/conformance/jobs/PROD_H/JOB.md:7` |
   39| | Designs | S1 independent; S2 AR(1) 0.5^\|j−k\|; S3 0.7H+0.3I; S4 0.85H+0.15I; S5 0.3J+0.4H+0.3I; S6 heterogeneous blocks ρ_b = 0.4+0.1((b−1) mod 6). Population blocks of 5 | `Docs/Methodology/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md:648–666` |
   40| | s0 / truth | 14 signals; β = (1.4, −1.0, 1.8, −1.2, 0.8, −1.6) cycled. Active p500: 3, 37, 74, 106, 145, 178, 213, 247, 284, 316, 355, 388, 423, 457. Active p1000: 3, 67, 134, 196, 265, 328, 393, 457, 524, 586, 655, 718, 783, 847 | MASTER `:621–646` |
   41| | Signal | y_c = c·Xβ + ε, σ = 1, no intercept. c ∈ {1.00 (`c100`), 0.50 (`c050`)}, both scales on the same X and ε (paired). Nominal SNR at c = 1: 24.64 (S5: 17.44) | MASTER `:609–620, 667–686`; `PROD_H/JOB.md:7` |
   42| | Reps | r001–r100 per (p, S) → 1,200 datasets × 2 scales = **2,400 fits** | `PROD_H/tables/units.tsv` (2,400 rows, 100 per p×S×c, checked by awk) |
```

P6 designs:
`Theory_work/Wave3/W3-P6/DESIGN.md` @ e8b5351c, lines 13–17:
```
   13| * **Designs (iid Gaussian rows, unit variances; the method standardises):**
   14|   `cs(ρ)` x = √ρ f + √(1−ρ) e, ρ ∈ {0.3, 0.5, 0.7}; `fac2` x_j = √.35 f₁ + √.25 (−1)^j f₂ + √.40 e_j (corr .60 / .10,
   15|   two pervasive factors); `s5` x_j = √.3 f + √.4 g_{group(j)} + √.3 e_j, groups of 5 consecutive columns (corr .7 / .3).
   16| * **Truth:** S₀_k = (k−1)·step + 3 + ((k−1) mod 2), step = ⌊p/s₀⌋ rounded down to even (v2, R01-8; v1 = ⌊p/s₀⌋, same when even), s₀ ∈ {4, 8}; β = (1.4, 1.0, 1.8, 1.2) repeated, aligned signs
   17|   (factor signal bᵀθ ≠ 0, the NEG regime); σ = 1. Truths in distinct s5 groups and alternating fac2 parity.
```

1M plan designs and truth:
`/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/EXPERIMENT_PLAN.md` (untracked file), lines 84–92:
```
   84| ### 2.2 Design families (examples only)
   85| | code | law of x (unit variances) | role | random access for test points |
   86| |---|---|---|---|
   87| | IND | iid N(0, 1) | no correlation: the cleanest feasibility case | yes |
   88| | AR | Toeplitz 0.6^{\|j−l\|} (AR(1) recursion along the columns) | metric-local (UNI-0 example), the **primary** design | yes (Markov bridge on any sorted subset) |
   89| | BLK | blocks of 20 consecutive columns, within-block correlation 0.5 (x_j = √.5 f_b + √.5 e_j) | grouped proxies, (V)/(L) with a non-trivial Q | yes |
   90| | FAC (C9) | one factor, cs ρ = 0.3 | D1 only, at 10⁴, contingent | yes |
   91| 
   92| Truth: S₀ spread evenly (k-th truth at ⌊(k − ½)p/5⌋, shifted so that no two truths share a BLK block).
```


## 3. Track C table (internal proxy computations; verbatim)
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 21–41:
```
   21| | D | design | P1–P3 floors: sample φ̂²(k=16) at n=1600 [slope]; pop λ_min(Σ) | P4 visibility v̂ = δ̂²/log n (sample) / pop | P5 leak size \|Q̂\| (pop, ε=0.2), n=200→1600 | P6 local-regression ℓ¹ tail (ν=4, q99) | P9 width 𝔴̂⁰ | P7 BM rate, margin/log n | P8 𝒪¹/r_n | P10 |
   22| |---|---|---|---|---|---|---|---|---|---|
   23| | 01 | IND | IN↑ 0.60 [+.42]; 1 | IN↑ both [+1.5] / 1 | IN 4 → 4 | IN 0 | IN −0.77 | IN↑ | IN | OUT |
   24| | 02 | AR0.5 | IN↑ 0.29 [+.28]; 0.33 | IN↑ both / 0.6 | IN sp 32→46, cl 8→10 (slow) | IN↑ 2.5→1.2 | IN↑ sp +.02→−.19 | IN↑ | IN | OUT |
   25| | 03 | AR0.8 | IN↑ 0.10 [+.19]; 0.11 | IN↑ (sp 0.005→26) / 0.22 | IN sp 109→137, cl 19→23 (slow) | IN↑ 18→6.5 | sp UNCL↑ +.54→+.02; cl IN | IN↑ | IN | OUT |
   26| | 04 | AR0.95 | IN↑ but small 0.024 [+.23]; 0.026 | sp UNCL↑ (≈0 to n=800, 0.7 at 1600); cl IN↑ / 0.05 | sp UNCL 200→585 (n^0.5); cl IN 70→87 | sp UNCL; cl IN↑ 22→8 | sp UNCL↑ +.79→+.52; cl IN↑ | IN↑ (margin small, 1.6→10) | IN | OUT |
   27| | 05 | BLK5-0.7 | IN↑ 0.22 [+.33]; 0.3 | IN↑ both / 0.37 | IN 20, 5 (bounded) | IN↑ 1.8→0.6 | IN | IN↑ | IN | OUT |
   28| | 06 | BLK5-0.85 | IN↑ 0.11 [+.33]; 0.15 | IN↑ both / 0.19 | IN 20, 5 | IN↑ | IN | IN↑ | IN | OUT |
   29| | 07 | BLK√p-0.5 | IN↑ 0.34 [+.39]; 0.5 | IN↑ both / 0.53 | UNCL sp 60→160, cl 15→40 (n^0.5 = block size √p, by design) | IN (flat ≈5 sp, ≈1 cl) | sp UNCL↑ +.26→+.07; cl IN | IN↑ | IN | OUT |
   30| | 08 | TOEP α=1 | IN↑ 0.34 [+.30]; 0.39 | IN↑ both / 0.61 | UNCL sp 180→508 (n^0.5), cl 33→76 (n^0.4) | sp UNCL ≈10–20; cl IN 2.6→2.1 | sp UNCL +.77→+.61; cl IN weak (−.02→−.11) | IN↑ | IN | OUT |
   31| | 09 | TOEP α=2 | IN↑ 0.52 [+.37]; 0.65 | IN↑ both / 0.88 | IN sp 32→53 (n^0.24), cl 8→11 | IN↑ | IN↑ | IN↑ | IN | OUT |
   32| | 10 | FAC a=.5 k=1 | IN↑ 0.59 [+.43]; 0.97–0.99 | IN↑ both / 0.79–0.99 | IN↑ Q̂ = [p] at n ≤ 400, = S₀ from n = 800 (weak factor falls below √(log n/n)) | IN (0 from n = 800) | IN from n = 800 | IN↑ | IN | OUT |
   33| | 11 | FAC a=.5 k=3 | IN↑ 0.59; 0.97–0.99 | IN↑ both / 0.79–0.99 | IN↑ as D10 | IN from n = 800 | IN from n = 800 | IN↑ | IN | OUT |
   34| | 12 | FAC a=.75 k=1 | IN↑ 0.56 [+.44]; 0.87–0.92 | IN↑ both / sp 0.38→0.58 | OUT Q̂ = [p] | OUT (≈9–17, flat) | OUT +0.84 flat | IN↑ | IN | OUT |
   35| | 13 | FAC a=.75 k=3 | IN↑ 0.56; 0.87–0.92 | IN↑ both / sp 0.38→0.58 | OUT Q̂ = [p] | OUT | OUT +0.83 | IN↑ | IN | OUT |
   36| | 14 | FAC a=1 k=1 (cs .5) | IN↑ 0.30 [+.40]; 0.5 | **sp OUT** (pop 0; sample 4e-4→0.13); cl IN↑ / 0.53 | OUT Q̂ = [p] | OUT | OUT +0.85 | IN↑ | IN | OUT |
   37| | 15 | FAC a=1 k=3 | IN↑ 0.32 [+.42]; 0.5 | **sp OUT** (pop 0; sample ≈1e-10, falling); cl IN↑ / 0.54 | OUT Q̂ = [p] | OUT | OUT +0.86 | IN↑ | IN | OUT |
   38| | 16 | S5 (0.3 global + block) | IN↑ 0.22 [+.32]; 0.3 | IN↑ both (sp 0.55→18) / sp 0.06, cl 0.36 | OUT Q̂ = [p] (global factor) | OUT | OUT +0.84 | IN↑ | IN | OUT |
   39| | 17 | S6 (blocks ρ .4–.9) | IN↑ 0.16 [+.34]; 0.1 | IN↑ both (sp ≈0 at n = 200 only) / 0.25–0.71 | IN 20, 5 | IN↑ 1.5→0.5 | IN | IN↑ | IN | OUT |
   40| | 18 | riboflavin-like | IN↑ but small 0.09 [+.21]; 0.1 | **OUT both** (pop ≈0; sample ≈0 at every n) | OUT Q̂ = [p] | OUT (≈13–21) | OUT +0.85 | IN↑ (margin 4→35) | IN | OUT |
   41| | 19 | FRED-QD-like | IN↑ but small 0.09 [+.23]; 0.1 | sp UNCL↑ (≈0 to n = 400, 10.7 at 1600; pop 0.15); cl IN↑ / 0.08 | UNCL whole 170-blocks: sp 170→672 (= 4 tiles × 170, then bounded), cl 170 | sp UNCL ≈17–19; cl IN↑ 17→8 | sp UNCL +.73→+.61; cl UNCL↑ +.75→+.13 | IN↑ | IN | OUT |
```


## 4. Items under test

### core1:B1 — Gaussian linear model with independent Gaussian errors
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 28–28:
```
   28| (S1) Model of §1 of the notation: Gaussian errors with fixed variance $\sigma_*^2>0$, independent of the design.
```

`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 31–31:
```
   31| Truth: y^r = α*1 + X^rβ* + ε, ε ~ N_n(0, σ*²I) (**G**), μ := CX^rβ* = Xθ*, θ* = D_xβ*, S₀ = supp θ*, s₀ = |S₀|,
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 947, §1, model (1) [SL-M1; transcribed from p. 947 image]:
```
Consider the problem of variable selection for the linear regression model:
    y = Xβ* + ε,    (1)
where y = (y_1, …, y_n)^T ∈ ℝ^n is the response vector, n is the sample size, X = (x_1, …, x_{P_n}) ∈ ℝ^{n×P_n} is the design matrix, P_n is the number of explanatory variables (which are also known as predictors), β* is the vector of unknown regression coefficients and ε = (ε_1, …, ε_n)^T ∼ N_n(0, σ*²) is Gaussian random error. In this paper, we use the bold letter x_i to denote an n-vector realization of the ith predictor. The subscript n in P_n means that P_n is a non-decreasing function of n. … In this paper, our study of variable selection will focus on the scenario P_n ≫ n, i.e. the column dimension of X is ultrahigh.
```
Song & Liang (2015), p. 950, §2.1, density (2) [SL-M2; transcribed from p. 950 image]:
```
Let D_n = {y; x_1, …, x_{P_n}} denote a data set of n observations drawn from model (1). Let x = (x_1, …, x_{P_n})^T denote a generic observation of the P_n predictors, and let y denote a generic observation of the response variable corresponding to x. Let ν_x denote the probability measure of x. Then the true probability density of (y, x) is given by
    f*(y, x) dx dy = (1/(√(2π) σ*)) exp{−(y − x^Tβ*)²/(2σ*²)} ν_x(dx) dy = φ(y; x^Tβ*, σ*) ν_x(dx) dy,    (2)
where φ(·; μ, σ) denotes a Gaussian density function with mean μ and standard deviation σ.
```
**(c) Verdict(s) under test.**
- `core1:B1.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 63–63:
```
   63| **Verdict: same as Song–Liang** (their model (1) and density (2), p. 950).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–36, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   34| | Assumption | Song–Liang (2015) |
   36| | Gaussian errors, fixed variance (S1) | same: model (1), density (2), p. 950 |
```

- `core1:B1.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–244:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
  244| | B1 | Gaussian linear model (all) | same: (1)–(2), p. 950 | in / in / in / in | in | in / in / in / in |
```

**(d) Track C evidence.**
(none)

### core1:B2 — Dimension p ≤ n^A
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 29–29:
```
   29| (S2) Asymptotics: $n\to\infty$, $p=p_n$ with $2\le p\le n^A$ for a fixed $A\ge1$ ($p\gg n$ allowed).
```

`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 63–64:
```
   63| **Regime R1.** Triangular array, n → ∞; s₀ ≥ 1 fixed; 2 ≤ p = p_n ≤ n^A ([T03R] line 9 assumes p ≥ 2) [C1B-F3] for a fixed A ≥ 1 (p ≫ n allowed); s₀ ≤ K
   64| eventually; σ*² > 0 fixed; G.
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 947, §1, model (1) [SL-M1; transcribed from p. 947 image]:
```
Consider the problem of variable selection for the linear regression model:
    y = Xβ* + ε,    (1)
where y = (y_1, …, y_n)^T ∈ ℝ^n is the response vector, n is the sample size, X = (x_1, …, x_{P_n}) ∈ ℝ^{n×P_n} is the design matrix, P_n is the number of explanatory variables (which are also known as predictors), β* is the vector of unknown regression coefficients and ε = (ε_1, …, ε_n)^T ∼ N_n(0, σ*²) is Gaussian random error. In this paper, we use the bold letter x_i to denote an n-vector realization of the ith predictor. The subscript n in P_n means that P_n is a non-decreasing function of n. … In this paper, our study of variable selection will focus on the scenario P_n ≫ n, i.e. the column dimension of X is ultrahigh.
```
Song & Liang (2015), p. 950, §2.1, growth of P_n; sparsity conditions (3) and (4) [SL-M3; transcribed from p. 950 image]:
```
As in conventional studies of high dimensional variable selection, we consider the asymptotics of the SAM approach under the assumption that P_n increases as n increases. To be specific, we assume that P_n ≻ n^θ for some θ > 0, where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0. In addition, we assume that the true model is sparse. Two sparseness conditions are considered in this paper. One states that most components of β* are very small such that
    lim_{n→∞} Σ_{j=1}^{P_n} |β*_j| < ∞,    (3)
where β*_j denotes the jth entry of β*. The other one is stronger but more usual, which requires that most components of β* are 0 such that
    lim_{n→∞} Σ_{j=1}^{P_n} 1{β*_j ≠ 0} < ∞.    (4)
Let ξ ⊂ {1, …, P_n} denote a subset model, which includes the indices of all selected predictors. Let |ξ| denote the number of predictors included in ξ. Thus, the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ P_n} has a finite model size.
```
Song & Liang (2015), p. 954, Corollary 1 [SL-CO1; transcribed from p. 954 image]:
```
Corollary 1. Consider a strict sparse model, i.e. condition (4) holds. Suppose that P_n < exp(Cn^α) for some α ∈ (0, 1), and the prior specification in Section 2.1.1 is used such that B(r_n) ≤ B r_n^v and B̃_n ≤ B n^v for some positive constants B and v. Take
    r_n < r̄_n ≺ log^k(n),
or
    r_n < r̄_n ≺ n^q,
for some k > 0 or some 0 < q < min{1 − α, 1/v}. Then the convergence rate in theorem 2 can be taken as
    ε_n = O{n^{−(1−α)/2} log^{k/2}(n)},
or
    ε_n = O(n^{−(min{1−α−q, 1−vq})/2}).
```
**(c) Verdict(s) under test.**
- `core1:B2.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 69–70:
```
   69| **Verdict: stronger than Song–Liang on the upper range** (their Corollary 1, p. 954, allows P_n < exp(Cn^α), α ∈ (0, 1));
   70| **weaker on the lower range** (they assume P_n ≻ n^θ for some θ > 0, p. 950; we need no growth of p).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 37–37, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   37| | p ≤ n^A (S2) | stronger above (Cor 1, p. 954: P_n < exp(Cn^α)); weaker below (P_n ≻ n^θ, p. 950) |
```

- `core1:B2.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 245–245:
```
  245| | B2 | p ≤ n^A (all) | stronger above (Cor 1, p. 954); weaker below (P_n ≻ n^θ, p. 950) | in | in | in (A ≈ 2.6) |
```

**(d) Track C evidence.**
(none)

### core1:B3 — Exact sparsity with s₀ fixed
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 105–105:
```
  105| - **(A2) Sparsity.** $s_0\ge1$ is fixed.
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 272–273:
```
  272| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ is fixed and $b_{\mathrm{lo}}\le|\beta^*_j|\le b_{\mathrm{hi}}$ for
  273|   $j\in S_0$, with fixed $0<b_{\mathrm{lo}}\le b_{\mathrm{hi}}<\infty$.
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 338–338:
```
  338| (b) *(Orthogonal or Gaussian null columns.)* Assume (S1), $s_0$ fixed, $\|X\theta^*\|^2\le nM$ and
```

`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 63–63:
```
   63| **Regime R1.** Triangular array, n → ∞; s₀ ≥ 1 fixed; 2 ≤ p = p_n ≤ n^A ([T03R] line 9 assumes p ≥ 2) [C1B-F3] for a fixed A ≥ 1 (p ≫ n allowed); s₀ ≤ K
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 950, §2.1, growth of P_n; sparsity conditions (3) and (4) [SL-M3; transcribed from p. 950 image]:
```
As in conventional studies of high dimensional variable selection, we consider the asymptotics of the SAM approach under the assumption that P_n increases as n increases. To be specific, we assume that P_n ≻ n^θ for some θ > 0, where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0. In addition, we assume that the true model is sparse. Two sparseness conditions are considered in this paper. One states that most components of β* are very small such that
    lim_{n→∞} Σ_{j=1}^{P_n} |β*_j| < ∞,    (3)
where β*_j denotes the jth entry of β*. The other one is stronger but more usual, which requires that most components of β* are 0 such that
    lim_{n→∞} Σ_{j=1}^{P_n} 1{β*_j ≠ 0} < ∞.    (4)
Let ξ ⊂ {1, …, P_n} denote a subset model, which includes the indices of all selected predictors. Let |ξ| denote the number of predictors included in ξ. Thus, the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ P_n} has a finite model size.
```
Song & Liang (2015), p. 952, §2.1.2, Hellinger distance; eigenvalue notation; B(r_n), B̃_n, Δ(p) [SL-H; transcribed from p. 952 image]:
```
In what follows, we study the asymptotics of the posterior distribution with respect to the Hellinger distance under appropriate conditions of r_n, r̄_n and V_ξ. For two density functions f_1(x, y) and f_2(x, y), the Hellinger distance is defined as
    d(f_1, f_2) = √( ∫∫ {f_1^{1/2}(x, y) − f_2^{1/2}(x, y)}² dx dy ).
For a matrix Σ, we let ch_i(Σ) denote the ith largest eigenvalue, and let ch′_i(Σ) denote the ith smallest eigenvalue. Define B(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ^{−1}), B̄(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ), B̃_n = sup_{ξ:|ξ|≤r̄_n} ch_1(V_ξ) and Δ(p) = inf_{ξ:|ξ|=p} Σ_{i∉ξ} |β*_i|.
Theorem 1 follows from Jiang (2007). Here we consider the simple situation that all predictors have been standardized and uniformly bounded, and the sparsity condition (3) holds.
```
Song & Liang (2015), p. 953, Theorem 2 (pp. 953–954, with the note on (8)) [SL-T2; transcribed from p. 953 image]:
```
Theorem 2. Assume that the data set D_n is generated from model (1) and all the predictors satisfy condition 1. Given a sequence {ε_n}, ε_n → 0, and nε_n² → ∞, if the conditions (9)–(14) of theorem 1 hold, the model is strictly sparse, i.e. condition (4) holds, and r_n ≻ 1, then the posterior consistency still holds, i.e. there is a constant c_1 > 0 such that, for sufficiently large n,
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²).
Note that condition (8) of theorem 1 is redundant here as, for large n, r_n > |t| and Δ(r_n) = 0 hold under the sparseness condition (4). [the last words, from 'hold under', are on p. 954]
```
**(c) Verdict(s) under test.**
- `core1:B3.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 78–79:
```
   78| **Verdict: same as Song–Liang** (their strict sparsity (4), p. 950, used by Theorems 2–3; their Theorem 1 alone allows
   79| the weaker (3)).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 39–39, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   39| | s₀ fixed (Thm 1 (A2), Thm 2 (A2)) | same: (4), p. 950 |
```

- `core1:B3.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 246–246:
```
  246| | B3 | s₀ fixed (all) | same: (4), p. 950 | in (as a sequence) | in | in |
```

**(d) Track C evidence.**
(none)

### core1:B4-UP — Signal bounded above (Thm 1 (A3); master (E))
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 106–106:
```
  106| - **(A3) Bounded coefficients.** $\max_{j}|\theta^*_j|\le\bar\theta$ for a fixed $\bar\theta<\infty$.
```

`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 67–67:
```
   67| - **(E) energy**: ‖μ‖² ≤ nM.
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 950, §2.1, growth of P_n; sparsity conditions (3) and (4) [SL-M3; transcribed from p. 950 image]:
```
As in conventional studies of high dimensional variable selection, we consider the asymptotics of the SAM approach under the assumption that P_n increases as n increases. To be specific, we assume that P_n ≻ n^θ for some θ > 0, where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0. In addition, we assume that the true model is sparse. Two sparseness conditions are considered in this paper. One states that most components of β* are very small such that
    lim_{n→∞} Σ_{j=1}^{P_n} |β*_j| < ∞,    (3)
where β*_j denotes the jth entry of β*. The other one is stronger but more usual, which requires that most components of β* are 0 such that
    lim_{n→∞} Σ_{j=1}^{P_n} 1{β*_j ≠ 0} < ∞.    (4)
Let ξ ⊂ {1, …, P_n} denote a subset model, which includes the indices of all selected predictors. Let |ξ| denote the number of predictors included in ξ. Thus, the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ P_n} has a finite model size.
```
Song & Liang (2015), p. 952, §2.1.2, Hellinger distance; eigenvalue notation; B(r_n), B̃_n, Δ(p) [SL-H; transcribed from p. 952 image]:
```
In what follows, we study the asymptotics of the posterior distribution with respect to the Hellinger distance under appropriate conditions of r_n, r̄_n and V_ξ. For two density functions f_1(x, y) and f_2(x, y), the Hellinger distance is defined as
    d(f_1, f_2) = √( ∫∫ {f_1^{1/2}(x, y) − f_2^{1/2}(x, y)}² dx dy ).
For a matrix Σ, we let ch_i(Σ) denote the ith largest eigenvalue, and let ch′_i(Σ) denote the ith smallest eigenvalue. Define B(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ^{−1}), B̄(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ), B̃_n = sup_{ξ:|ξ|≤r̄_n} ch_1(V_ξ) and Δ(p) = inf_{ξ:|ξ|=p} Σ_{i∉ξ} |β*_i|.
Theorem 1 follows from Jiang (2007). Here we consider the simple situation that all predictors have been standardized and uniformly bounded, and the sparsity condition (3) holds.
```
Song & Liang (2015), p. 952, Theorem 1 and conditions (8)–(15) [SL-T1; transcribed from p. 952 image]:
```
Theorem 1 (posterior consistency). Assume that the data set D_n is drawn from model (1) and all predictors |x_i| ≤ 1. If there is a sequence {ε_n} ∈ (0, 1) such that nε_n² ≻ 1, and the following conditions hold,
    Δ(r_n) ≺ ε_n,    (8)
    r̄_n ln(1/ε_n²) ≺ nε_n²,    (9)
    r̄_n ln(P_n) ≺ nε_n²,    (10)
    r̄_n ln(nε_n² B̃_n) ≺ nε_n²,    (11)
    1 ≤ r_n ≤ r̄_n < P_n,    (12)
    r_n ≺ P_n,    (13)
    B(r_n) ≺ nε_n²,    (14)
then the posterior consistency holds, i.e. there is a constant c_1 > 0 such that
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²),    (15)
for sufficiently large n, where the Hellinger distance is
    d²(f, f*) = ∫∫ |φ^{1/2}(y; x^Tβ*, σ*) − φ^{1/2}(y; x^Tβ, σ)|² ν_x(dx) dy,
f* is as defined in expression (2), f is the density function for a model simulated from the posterior and P* denotes the probability measure of data generation.
```
**(c) Verdict(s) under test.**
- `core1:B4-UP.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 89–92:
```
   89| **Verdict: comparable to Song–Liang.** Above: their (3) with |x_i| ≤ 1 (Theorem 1, p. 952) bounds the signal; under (4)
   90| alone their main text states no bound. Below: their Theorem 3 (p. 956) states **no** beta-min; a true predictor needs
   91| only to be "identifiable" (Condition 3, p. 955), and the step "d(f*, f) ≥ ε_n for any density f that does not select x_t"
   92| is in their supplement (not inspected).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 40–40, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   40| | Bounded coefficients (Thm 1 (A3)) | comparable: (3), p. 950, with \|x_i\| ≤ 1 |
```

- `core1:B4.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 247–247:
```
  247| | B4 | signal bounded; fixed nonzero or beta-min (1, 2, 6, 10; 9 above only) | comparable: (3), p. 950; no beta-min stated in Thm 3, p. 956 | in | in | in |
```

**(d) Track C evidence.**
(none)

### core1:B4-LO — Signal bounded below: beta-min at √(log n/n) (Thm 1 (A6)); fixed nonzero signals (Thm 2 (A2))
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 111–113:
```
  111| - **(A6) Beta-min.** $\theta^*_{\min}\ge C_\beta\,\sigma_*\sqrt{\log n/n}$ with a fixed $C_\beta>0$ such that
  112|   $C_\beta^2\varphi_0^2>c_0(s_0,A)$ [S1-F1]; or $\theta^*_{\min}\sqrt{n/\log n}\to\infty$.
  113| 
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 272–273:
```
  272| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ is fixed and $b_{\mathrm{lo}}\le|\beta^*_j|\le b_{\mathrm{hi}}$ for
  273|   $j\in S_0$, with fixed $0<b_{\mathrm{lo}}\le b_{\mathrm{hi}}<\infty$.
```

`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 74–75:
```
   74| - **(BM) beta-min**, either BM-∞: θ*²_min nφ₀²/(σ*² log n) → ∞; or BM(c): θ*²_min ≥ cσ*² log n/(nφ₀²) with a fixed
   75|   c > c₀(s₀, A) := max{4C_*, 32[s₀(A + 1) + 2]} (C_* the [P3] proof constant; a proof artefact, not sharp).
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 955, §2.2, marginal inclusion probability; Condition 3 [SL-C3; transcribed from p. 955 image]:
```
Let q_j denote the marginal inclusion probability of the predictor x_j, which is given by
    q_j = π(j ∈ ξ | D_n) = Σ_{ξ∈{ξ̃: j∈ξ̃}} π(ξ | D_n).
… Therefore, to select true predictors consistently, it is necessary to control the severeness of multicollinearity. For this purpose, we introduce the following identifiability condition which controls the severeness of multicollinearity through the sequence {ε_n}.
Condition 3. A predictor x_k is said to be identifiable among all other predictors, if, for any 1 ≤ j_1, …, j_{r̄_n} ≤ P_n (j_i ≠ k for all i) and b_i ∈ ℝ,
    E[ exp{ −( x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i} )² } ] ≤ 1 − δ_n,    δ_n ≻ ε_n²,
where x_l denotes a generic observation of the predictor x_l.
This condition states that, if a predictor x_k is identifiable, then there does not exist a linear combination of other predictors in X which can mimic it.
```
Song & Liang (2015), p. 955, sufficient forms of Condition 3 (pp. 955–956) [SL-C3S; transcribed from p. 955 image]:
```
If all the predictors have mean 0 and are bounded with |x_i| ≤ 1, then
    E[ exp{ −( x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i} )² } ] ≤ E[ 1 − ( 1 − exp{ −(1 + Σ_i |b_i|)² } ) / (1 + Σ_i |b_i|)² · ( x_k + Σ_i b_i x_{j_i} )² ]
        ≤ 1 − {1 − exp(−1)} var( x_k + Σ_i b_i x_{j_i} ) / (1 + Σ |b_i|)²
        ≤ 1 − (1 − exp(−1))/(r̄_n + 1) · ch′_1{var(x̃)},
where x̃ = (x_k, x_{j_1}, …, x_{j_{r̄_n}})^T, and ch′_1{var(x̃)} is the smallest eigenvalue of the covariance matrix of x̃. Hence, if ch′_1{var(x̃)} ≻ r̄_n ε_n² for any choice of x̃, x_t is identifiable. Furthermore, if ch′_1{var(x)} ≻ r̄_n ε_n², then all the predictors are identifiable, where x = (x_1, …, x_{P_n})^T denotes a generic observation of all predictors.
If all the predictors follow the standard normal distribution, by the moment-generating function of the χ²-distribution, we have
    E[exp{−(x_k + Σ b_i x_{j_i})²}] = { 1 + 2 var( x_k + Σ_i b_i x_{j_i} ) }^{−1/2} < max{ 0.5, 1 − var( x_k + Σ_i b_i x_{j_i} )/8 }.
Thus, if var(x_k + Σ_i b_i x_{j_i}) ≻ ε_n², then the identifiability condition is satisfied. Since [p. 956]
    var( x_k + Σ_i b_i x_{j_i} ) ≥ var(x_k | x̃∖x_k) ≥ ch′_1{var(x̃)} ≥ ch′_1{var(x)},
by the same arguments, all predictors are identifiable if ch′_1{var(x)} ≻ ε_n². Further, it can be shown (in the proof of theorem 3) that, if a true predictor x_t is identifiable, then d(f*, f) ≥ ε_n for any density f that does not select x_t. Therefore, we have the following sure screening property.
```
Song & Liang (2015), p. 956, Theorem 3 (sure screening) and the paragraphs after it [SL-T3; transcribed from p. 956 image]:
```
Theorem 3 (sure screening). Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] < exp(−c_1 nε_n²), where ξ denotes a model sampled from the posterior distribution. Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] = 0.
The proof of theorem 3 can be found in the on-line supplementary material. Let ξ_q = {i : 1 ≤ i ≤ P_n, q_i > q} denote a model including all the predictors with the marginal inclusion probability greater than a threshold value of q ∈ (0, 1). Then it follows from theorem 3 that π(t ⊂ ξ_q) →^p 1 if all true predictors are identifiable. … Theorem S in the on-line supplementary material establishes the consistency of MAP models. Thus, we have two criteria for variable selection, by either marginal inclusion probabilities or the MAP model. Although theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled), we suggest the use of marginal inclusion probabilities as the criterion for variable selection.
```
**(c) Verdict(s) under test.**
- `core1:B4-LO.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 89–92:
```
   89| **Verdict: comparable to Song–Liang.** Above: their (3) with |x_i| ≤ 1 (Theorem 1, p. 952) bounds the signal; under (4)
   90| alone their main text states no bound. Below: their Theorem 3 (p. 956) states **no** beta-min; a true predictor needs
   91| only to be "identifiable" (Condition 3, p. 955), and the step "d(f*, f) ≥ ε_n for any density f that does not select x_t"
   92| is in their supplement (not inspected).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 43–43, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   43| | Beta-min at √(log n/n) (Thm 1 (A6)); fixed nonzero signals (Thm 2 (A2)) | comparable: no beta-min is stated in Thm 3, p. 956 |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 45–45:
```
   45| P7: BM rate θ_min²nφ̂₀²/log n and margin Δ̂/log n grow like n^0.7–1.15 in every design and placement; M̂ is bounded.
```


### core1:B5 — Eigenvalue floor on small sets (Thm 1 (A4), Thm 1′ (A4′), Thm 2 (A3))
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 107–108:
```
  107| - **(A4) Sparse eigenvalue floor.** $\lambda_{\min}(\hat R_S)\ge\varphi_0^2$ for every $S\subseteq[p]$ with
  108|   $|S|\le 2(A+1)s_0+2$, for a fixed $\varphi_0\in(0,1]$.
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 128–131:
```
  128| - **(A4′) Floor on the truth and an identifiability margin.** $\lambda_{\min}(\hat R_{S_0})\ge\varphi_0^2$, and every model
  129|   $S$ with $|S|\le K$, $S_0\not\subseteq S$ and at most $j_0:=\lceil(2A+1)s_0\rceil+1$ variables outside $S_0$ leaves
  130|   residual signal $\|(I-P_S)X\theta^*\|^2\ge c\,\sigma_*^2\log n$, with a fixed $c>c_1(s_0,A)$, where $c_1(s_0,A)$ is an
  131|   explicit constant, not optimised [H5-6],
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 274–276:
```
  274| - **(A3) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge\varphi^2$ for every $S$ with
  275|   $|S|\le 5(A+1)(s_0+1)\log n$, for a fixed $\varphi\in(0,1]$ (for instance, $\lambda_{\min}(\Sigma_n)\ge\varphi^2$).
  276| 
```

`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 68–70:
```
   68| - **(F_λ) anchored floor, bounded size** = SE_λ(j₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}/(n−1)) ≥ φ₀² for every J ⊆ [p]∖S₀ with
   69|   |J| ≤ j₀ (J = ∅ included: this contains R's condition on S₀). *By interlacing it implies* λ_min(R_S) ≥ φ₀² for
   70|   **every** S with |S| ≤ j₀ (S ⊆ S₀ ∪ S), so it excludes e.g. duplicated null columns [R02-F2].
```
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 106–109:
```
  106| **Corollary 1R (a sufficient bridge for item 6; Gaussian rows — an example, not part of Theorem 1).** Let the raw rows
  107| be iid N(m, Σ_n), Σ_n a unit-diagonal correlation matrix, ε independent of the design, and **LSF** (fixed 0 < φ ≤ 1):
  108| (i) λ_min(Σ_{n,S}) ≥ φ² for |S| ≤ min(p, s₀ + j₀); (ii) λ_min(Σ_{n,S}) ≥ ψ_n for |S| ≤ k̄_n := min(p, s₀ + max(j₀, m̄_n)),
  109| m̄_n := ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n]/log(3/2)⌉ = O(log n), with ψ_n√n/(log n)^{3/2} → ∞.
```

`Theory_work/Wave3/W3-POST2/STATEMENT.md` @ e8b5351c, lines 126–130:
```
  126| ## Claim E (brief item 5, stretch) — Theorem 1-VIS: (F_λ) away from S₀ replaced by an identifiability margin
  127| 
  128| In R1 under G, (E), (F₀), (OS) and (ID^M; c) with c > c₁(s₀, A) — (ID^M; c): L_S := μ_cᵀ(I − M_S)μ_c ≥ cσ*² log n for every
  129| S ∈ Ω with S₀ ⊄ S, |S∖S₀| ≤ j₀; L_S = min_ϑ B_S(ϑ) ≥ Δ_S, so (ID; c) ⇒ (ID^M; c) (v1.2, R03b §D) — where
  130|   c₁ := (√(2C_x) + √(2C_x + C_A j₀ + (2/log 2)(s₀(A + 1) + 2)))²,  C_x := Aj₀ + s₀ + log(j₀ + 1) + 2,
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 952, Theorem 1 and conditions (8)–(15) [SL-T1; transcribed from p. 952 image]:
```
Theorem 1 (posterior consistency). Assume that the data set D_n is drawn from model (1) and all predictors |x_i| ≤ 1. If there is a sequence {ε_n} ∈ (0, 1) such that nε_n² ≻ 1, and the following conditions hold,
    Δ(r_n) ≺ ε_n,    (8)
    r̄_n ln(1/ε_n²) ≺ nε_n²,    (9)
    r̄_n ln(P_n) ≺ nε_n²,    (10)
    r̄_n ln(nε_n² B̃_n) ≺ nε_n²,    (11)
    1 ≤ r_n ≤ r̄_n < P_n,    (12)
    r_n ≺ P_n,    (13)
    B(r_n) ≺ nε_n²,    (14)
then the posterior consistency holds, i.e. there is a constant c_1 > 0 such that
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²),    (15)
for sufficiently large n, where the Hellinger distance is
    d²(f, f*) = ∫∫ |φ^{1/2}(y; x^Tβ*, σ*) − φ^{1/2}(y; x^Tβ, σ)|² ν_x(dx) dy,
f* is as defined in expression (2), f is the density function for a model simulated from the posterior and P* denotes the probability measure of data generation.
```
Song & Liang (2015), p. 953, Theorem 2 (pp. 953–954, with the note on (8)) [SL-T2; transcribed from p. 953 image]:
```
Theorem 2. Assume that the data set D_n is generated from model (1) and all the predictors satisfy condition 1. Given a sequence {ε_n}, ε_n → 0, and nε_n² → ∞, if the conditions (9)–(14) of theorem 1 hold, the model is strictly sparse, i.e. condition (4) holds, and r_n ≻ 1, then the posterior consistency still holds, i.e. there is a constant c_1 > 0 such that, for sufficiently large n,
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²).
Note that condition (8) of theorem 1 is redundant here as, for large n, r_n > |t| and Δ(r_n) = 0 hold under the sparseness condition (4). [the last words, from 'hold under', are on p. 954]
```
Song & Liang (2015), p. 955, §2.2, marginal inclusion probability; Condition 3 [SL-C3; transcribed from p. 955 image]:
```
Let q_j denote the marginal inclusion probability of the predictor x_j, which is given by
    q_j = π(j ∈ ξ | D_n) = Σ_{ξ∈{ξ̃: j∈ξ̃}} π(ξ | D_n).
… Therefore, to select true predictors consistently, it is necessary to control the severeness of multicollinearity. For this purpose, we introduce the following identifiability condition which controls the severeness of multicollinearity through the sequence {ε_n}.
Condition 3. A predictor x_k is said to be identifiable among all other predictors, if, for any 1 ≤ j_1, …, j_{r̄_n} ≤ P_n (j_i ≠ k for all i) and b_i ∈ ℝ,
    E[ exp{ −( x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i} )² } ] ≤ 1 − δ_n,    δ_n ≻ ε_n²,
where x_l denotes a generic observation of the predictor x_l.
This condition states that, if a predictor x_k is identifiable, then there does not exist a linear combination of other predictors in X which can mimic it.
```
Song & Liang (2015), p. 955, sufficient forms of Condition 3 (pp. 955–956) [SL-C3S; transcribed from p. 955 image]:
```
If all the predictors have mean 0 and are bounded with |x_i| ≤ 1, then
    E[ exp{ −( x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i} )² } ] ≤ E[ 1 − ( 1 − exp{ −(1 + Σ_i |b_i|)² } ) / (1 + Σ_i |b_i|)² · ( x_k + Σ_i b_i x_{j_i} )² ]
        ≤ 1 − {1 − exp(−1)} var( x_k + Σ_i b_i x_{j_i} ) / (1 + Σ |b_i|)²
        ≤ 1 − (1 − exp(−1))/(r̄_n + 1) · ch′_1{var(x̃)},
where x̃ = (x_k, x_{j_1}, …, x_{j_{r̄_n}})^T, and ch′_1{var(x̃)} is the smallest eigenvalue of the covariance matrix of x̃. Hence, if ch′_1{var(x̃)} ≻ r̄_n ε_n² for any choice of x̃, x_t is identifiable. Furthermore, if ch′_1{var(x)} ≻ r̄_n ε_n², then all the predictors are identifiable, where x = (x_1, …, x_{P_n})^T denotes a generic observation of all predictors.
If all the predictors follow the standard normal distribution, by the moment-generating function of the χ²-distribution, we have
    E[exp{−(x_k + Σ b_i x_{j_i})²}] = { 1 + 2 var( x_k + Σ_i b_i x_{j_i} ) }^{−1/2} < max{ 0.5, 1 − var( x_k + Σ_i b_i x_{j_i} )/8 }.
Thus, if var(x_k + Σ_i b_i x_{j_i}) ≻ ε_n², then the identifiability condition is satisfied. Since [p. 956]
    var( x_k + Σ_i b_i x_{j_i} ) ≥ var(x_k | x̃∖x_k) ≥ ch′_1{var(x̃)} ≥ ch′_1{var(x)},
by the same arguments, all predictors are identifiable if ch′_1{var(x)} ≻ ε_n². Further, it can be shown (in the proof of theorem 3) that, if a true predictor x_t is identifiable, then d(f*, f) ≥ ε_n for any density f that does not select x_t. Therefore, we have the following sure screening property.
```
Song & Liang (2015), p. 956, Theorem 3 (sure screening) and the paragraphs after it [SL-T3; transcribed from p. 956 image]:
```
Theorem 3 (sure screening). Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] < exp(−c_1 nε_n²), where ξ denotes a model sampled from the posterior distribution. Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] = 0.
The proof of theorem 3 can be found in the on-line supplementary material. Let ξ_q = {i : 1 ≤ i ≤ P_n, q_i > q} denote a model including all the predictors with the marginal inclusion probability greater than a threshold value of q ∈ (0, 1). Then it follows from theorem 3 that π(t ⊂ ξ_q) →^p 1 if all true predictors are identifiable. … Theorem S in the on-line supplementary material establishes the consistency of MAP models. Thus, we have two criteria for variable selection, by either marginal inclusion probabilities or the MAP model. Although theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled), we suggest the use of marginal inclusion probabilities as the criterion for variable selection.
```
**(c) Verdict(s) under test.**
- `core1:B5.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 101–101:
```
  101| **Verdict: comparable to Song–Liang's Condition 3** — stronger in level, on smaller sets, and for a stronger conclusion.
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 41–41, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   41| | Sparse eigenvalue floor on bounded sets (Thm 1 (A4)); floor on S₀ + residual-signal margin (Thm 1′ (A4′)); population floor (Thm 2 (A3)) | comparable to Condition 3, p. 955 (sufficient forms pp. 955–956) |
```

- `core1:B5.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 248–248:
```
  248| | B5 | eigenvalue floor on small sets (1, 2, 6, 10, 9B) | comparable to Condition 3, p. 955: fixed level against vanishing, smaller sets, stronger conclusion | in | **in** | in |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 43–44:
```
   43| Rows P2 (unanchored floor at the size cutoff m♯_n, m♯ = 49–80) and P3 (FL-Q, where Q̂ fits the lattice cap) follow
   44| the P1 column: rising in n in all 19 designs (P2 slopes +0.46 to +0.68), at levels 0.017–0.35 at n = 1600.
```
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 49–55:
```
   49| ## p = 10n (Owls only n = 200; NOTS gives n = 400–1600)
   50| At (n, p) = (200, 2000) the sample visibility v̂ collapses to ≈ 0 (< 1e-4) in most designs (spread: 16 of 19; clustered: 5 of
   51| 19), and the m♯-size floor is ≈ 0.001–0.006 in every design. Checked by explicit projections: a greedy masking set of
   52| ≤ 15 columns from p ≫ n candidates cancels the truth column's gain ‖(P_{U∪j} − P_U)μ‖² (not a numerical artefact).
   53| *(pilot, 1 replicate)* At large p this recovers with n for IND (v̂ ≈ 0 → 67 → 180 at (n, p) = (200, 2·10⁴),
   54| (800, 2·10⁴), (1600, 16000); m♯ floor 0.0002 → 0.08 → 0.21) and block D05 (v̂ 38 at n = 1600), but not for the strong factor with the spread truth
   55| (D14: v̂ 0.012 at n = 1600). The NOTS cells settle this trend.
```
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 57–60:
```
   57| ## Top findings (Owls part)
   58| 1. **Sparse floors are inside and improve with n in all 19 designs** (anchored k ≤ 16, at the size cutoff m♯, and Q̂ ∪ {l});
   59|    population floors are certified by λ_min(Σ) ≥ 0.026. Levels are small for AR(0.95), riboflavin- and FRED-like
   60|    designs (≈ 0.02–0.09 at n = 1600) but rising.
```


### core1:B6 — No near-exact collinearity among O(log n) columns (Thm 1 (A5); master (F_w))
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 109–110:
```
  109| - **(A5) No near-collinearity among $O(\log n)$ columns.** $\lambda_{\min}(X_S^\top X_S)\ge g_0$ for every $S$ with
  110|   $|S|\le 3(A+1)(s_0+1)\log n$, for a fixed $g_0>0$.
```

`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 71–73:
```
   71| - **(F_w) anchored unnormalised floor, logarithmic size** = SE_w(m♯_n; g₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ for every
   72|   J ⊆ [p]∖S₀ with |J| ≤ m♯_n (m♯_n = O(log n) under R1). By interlacing it implies λ_min(G_S) ≥ g₀ for every S with
   73|   |S| ≤ m♯_n: no exact linear dependence among ≤ m♯_n columns [R02-F2].
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 952, §2.1.2, Hellinger distance; eigenvalue notation; B(r_n), B̃_n, Δ(p) [SL-H; transcribed from p. 952 image]:
```
In what follows, we study the asymptotics of the posterior distribution with respect to the Hellinger distance under appropriate conditions of r_n, r̄_n and V_ξ. For two density functions f_1(x, y) and f_2(x, y), the Hellinger distance is defined as
    d(f_1, f_2) = √( ∫∫ {f_1^{1/2}(x, y) − f_2^{1/2}(x, y)}² dx dy ).
For a matrix Σ, we let ch_i(Σ) denote the ith largest eigenvalue, and let ch′_i(Σ) denote the ith smallest eigenvalue. Define B(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ^{−1}), B̄(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ), B̃_n = sup_{ξ:|ξ|≤r̄_n} ch_1(V_ξ) and Δ(p) = inf_{ξ:|ξ|=p} Σ_{i∉ξ} |β*_i|.
Theorem 1 follows from Jiang (2007). Here we consider the simple situation that all predictors have been standardized and uniformly bounded, and the sparsity condition (3) holds.
```
Song & Liang (2015), p. 952, Theorem 1 and conditions (8)–(15) [SL-T1; transcribed from p. 952 image]:
```
Theorem 1 (posterior consistency). Assume that the data set D_n is drawn from model (1) and all predictors |x_i| ≤ 1. If there is a sequence {ε_n} ∈ (0, 1) such that nε_n² ≻ 1, and the following conditions hold,
    Δ(r_n) ≺ ε_n,    (8)
    r̄_n ln(1/ε_n²) ≺ nε_n²,    (9)
    r̄_n ln(P_n) ≺ nε_n²,    (10)
    r̄_n ln(nε_n² B̃_n) ≺ nε_n²,    (11)
    1 ≤ r_n ≤ r̄_n < P_n,    (12)
    r_n ≺ P_n,    (13)
    B(r_n) ≺ nε_n²,    (14)
then the posterior consistency holds, i.e. there is a constant c_1 > 0 such that
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²),    (15)
for sufficiently large n, where the Hellinger distance is
    d²(f, f*) = ∫∫ |φ^{1/2}(y; x^Tβ*, σ*) − φ^{1/2}(y; x^Tβ, σ)|² ν_x(dx) dy,
f* is as defined in expression (2), f is the density function for a model simulated from the posterior and P* denotes the probability measure of data generation.
```
Song & Liang (2015), p. 953, choices of V_ξ; 'ridge prior' [SL-V; transcribed from p. 953 image]:
```
The validity of this theorem depends on the choice of the prior covariance matrix V_ξ or, more precisely, the largest eigenvalues of V_ξ and V_ξ^{−1}. For most choices of V_ξ, B(r_n) ≤ B r_n^v and B̃_n ≤ B r_n^v hold for some positive constants B and v. For example, if V_ξ = c I_{|ξ|}, where I_p is an identity matrix of order p, then both B(r_n) and B̃_n are constants. One can also set V_ξ^{−1} = c E(x_ξ^T x_ξ) as in Zellner (1986) and Liang et al. (2008), where the expectation is replaced by its sample empirical estimator. If all x_i s are standardized with zero mean and equal variance, then B(r_n) ≤ r_n. Furthermore, if x_i has some specific covariance structure, then B̃_n can be shown to be bounded. For example, if all pairwise covariances cov(x_i, x_j) = ρ ∈ (0, 1), then B̃_n = 1 − ρ; if x_i is generated from a finite order auto-regressive or moving average model without root for the characteristic polynomial on the unit circle, then B̃_n is also bounded by some constant (Bickel and Levina, 2004). In general, for standardized x_i s, we can choose a 'ridge prior' as suggested by Gupta and Ibrahim (2009): let V_ξ^{−1} = E(x_ξ^T x_ξ) + c_n I_{|ξ|}; then B(r_n) ≤ r_n + c_n and B̃_n ≤ c_n^{−1}, where c_n is proportional to 1/n, i.e. c_n ∝ n^{−1}.
```
Song & Liang (2015), p. 956, Theorem 3 (sure screening) and the paragraphs after it [SL-T3; transcribed from p. 956 image]:
```
Theorem 3 (sure screening). Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] < exp(−c_1 nε_n²), where ξ denotes a model sampled from the posterior distribution. Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] = 0.
The proof of theorem 3 can be found in the on-line supplementary material. Let ξ_q = {i : 1 ≤ i ≤ P_n, q_i > q} denote a model including all the predictors with the marginal inclusion probability greater than a threshold value of q ∈ (0, 1). Then it follows from theorem 3 that π(t ⊂ ξ_q) →^p 1 if all true predictors are identifiable. … Theorem S in the on-line supplementary material establishes the consistency of MAP models. Thus, we have two criteria for variable selection, by either marginal inclusion probabilities or the MAP model. Although theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled), we suggest the use of marginal inclusion probabilities as the criterion for variable selection.
```
**(c) Verdict(s) under test.**
- `core1:B6.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 125–126:
```
  125| **Verdict: stronger than Song–Liang's Theorems 1–2, which have no design eigenvalue condition;** very weak in absolute
  126| terms, and it is the population twin of a term SL put in their prior.
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 42–42, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   42| | No near-collinearity among O(log n) columns (Thm 1 (A5)) | stronger: no counterpart in Thm 3, p. 956, which controls sensitivity only |
```

- `core1:B6.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 249–249:
```
  249| | B6 | no near-exact collinearity on O(log n) sets (1, 9) | stronger: none in Thm 1–2 ((11), (14) are on the prior, p. 952); same order as their ridge c_n ∝ 1/n, p. 953 | in | in | in |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 46–47:
```
   46| P8: 𝒪¹_n/r_n (j = 1 and 2 terms) = 1.08 → 0.92, the same in every design (the j = 1 term is design-insensitive at
   47| p = n); bounded and decreasing, not refuted. P10: δ̂_n√(p log log n) grows like n^0.55–1.1 everywhere (pre-announced).
```


### core1:B7 — Law of the rows: i.i.d. Gaussian (Thm 2)
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 269–270:
```
  269| **Theorem 2.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a correlation matrix, and
  270| assume
```

`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 106–107:
```
  106| **Corollary 1R (a sufficient bridge for item 6; Gaussian rows — an example, not part of Theorem 1).** Let the raw rows
  107| be iid N(m, Σ_n), Σ_n a unit-diagonal correlation matrix, ε independent of the design, and **LSF** (fixed 0 < φ ≤ 1):
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 953, Condition 1 and the two sufficient cases [SL-C1; transcribed from p. 953 image]:
```
Theorem 1 assumes that all the predictors are uniformly bounded. However, this condition might not be satisfied for continuous predictors. In what follows, we relax this condition.
Condition 1. There are some constants M > 0 and δ > 0 such that for any subvector of x, (x_{j_1}, …, x_{j_r})^T with 1 ≤ j_1 < … < j_r ≤ P_n, r ≤ r̄_n, and |a_i| ≤ δ for i = 1, …, r, we have
    E[ exp{ ( Σ_{i=1}^r a_i x_{j_i} / r )² } ] ≤ exp(M),
where the expectation is taken with respect to the distribution of the random variables x_{j_i}.
Condition 1 controls the tail distribution of x such that the marginal distribution of y does not change dramatically in the sense of d_1-divergence (which is defined in the on-line supplementary material) with respect to the change of β. If x has a heavy tail distribution, the prior information around f* will be too weak to induce good posterior asymptotics. If all the variables are bounded by some constant m, as assumed in theorem 1, then
    E[ exp{ ( Σ_{i=1}^r a_i x_{j_i} / r )² } ] ≤ exp(δ² m)
and thus condition 1 holds. If x follows a Gaussian process with zero mean and var(x_i) = 1, then (Σ_{i=1}^r a_i x_{j_i})² follows the sχ²_1-distribution, where the scale s ≤ δ² r². Therefore, by the moment-generating function of the χ²_1-distribution,
    E[ exp{ ( Σ_{i=1}^r a_i x_{j_i} )² / r² } ] ≤ (1 − 2δ²)^{−1/2},
condition 1 holds.
```
**(c) Verdict(s) under test.**
- `core1:B7.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 140–140:
```
  140| **Verdict: Thm 9 (A3) is stronger than Song–Liang's Condition 1 and implies it; Gaussian rows are stronger still.**
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 44–44, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   44| | Rows i.i.d. Gaussian (Thm 2) | stronger than Condition 1, p. 953 |
```

- `core1:B7.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 250–250:
```
  250| | B7 | Gaussian rows (2, 6, 10); sub-Gaussian sparse directions (9) | stronger than Condition 1, p. 953 (implies it) | in | in | in |
```

**(d) Track C evidence.**
(none)

### core1:DR — Fixed-to-random design transfer
**(a) Our assumption text.**
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 95–100:
```
   95| 6. **(Random design, interface form)** [C1A-F7] Let (X, θ*) be random with ε independent of (X, θ*), and suppose there
   96|    are (X, θ*)-measurable events 𝒜_n with P(𝒜_n) → 1 on which |supp θ*| = s₀ [C2B-N2] and (E), (F_λ), (F_w) hold with common constants
   97|    (M, φ₀, g₀) and (BM) holds with a common c > c₀ or a common deterministic envelope M_n → ∞. Then 1–4 hold under the
   98|    joint law of (X, θ*, ε); if only (E), (F_λ), (F_w) hold on 𝒜_n, 5(a) and 5(b) hold under the joint law. (Proof:
   99|    apply the fixed-design statements along every deterministic sequence in 𝒜_n; the diagonal tightness transfer of
  100|    [POST] step (5) gives uniformity; add P(𝒜_nᶜ) → 0.)
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 950, §2.1, density (2) [SL-M2; transcribed from p. 950 image]:
```
Let D_n = {y; x_1, …, x_{P_n}} denote a data set of n observations drawn from model (1). Let x = (x_1, …, x_{P_n})^T denote a generic observation of the P_n predictors, and let y denote a generic observation of the response variable corresponding to x. Let ν_x denote the probability measure of x. Then the true probability density of (y, x) is given by
    f*(y, x) dx dy = (1/(√(2π) σ*)) exp{−(y − x^Tβ*)²/(2σ*²)} ν_x(dx) dy = φ(y; x^Tβ*, σ*) ν_x(dx) dy,    (2)
where φ(·; μ, σ) denotes a Gaussian density function with mean μ and standard deviation σ.
```
Song & Liang (2015), p. 952, Theorem 1 and conditions (8)–(15) [SL-T1; transcribed from p. 952 image]:
```
Theorem 1 (posterior consistency). Assume that the data set D_n is drawn from model (1) and all predictors |x_i| ≤ 1. If there is a sequence {ε_n} ∈ (0, 1) such that nε_n² ≻ 1, and the following conditions hold,
    Δ(r_n) ≺ ε_n,    (8)
    r̄_n ln(1/ε_n²) ≺ nε_n²,    (9)
    r̄_n ln(P_n) ≺ nε_n²,    (10)
    r̄_n ln(nε_n² B̃_n) ≺ nε_n²,    (11)
    1 ≤ r_n ≤ r̄_n < P_n,    (12)
    r_n ≺ P_n,    (13)
    B(r_n) ≺ nε_n²,    (14)
then the posterior consistency holds, i.e. there is a constant c_1 > 0 such that
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²),    (15)
for sufficiently large n, where the Hellinger distance is
    d²(f, f*) = ∫∫ |φ^{1/2}(y; x^Tβ*, σ*) − φ^{1/2}(y; x^Tβ, σ)|² ν_x(dx) dy,
f* is as defined in expression (2), f is the density function for a model simulated from the posterior and P* denotes the probability measure of data generation.
```
**(c) Verdict(s) under test.**
- `core1:DR.SL`
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 45–45, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   45| | Fixed-to-random design transfer | not needed (random design throughout) |
```

**(d) Track C evidence.**
(none)

### core1:SUM — HPM, MPM, PIPs from 1 − π(S₀ | y)
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 114–123:
```
  114| Then there are $n_0$ and $C$, depending only on $(s_0,A,\sigma_*^2,\bar\theta,\varphi_0,g_0,C_\beta)$, such that for every
  115| $n\ge n_0$ and every design and $\theta^*$ satisfying (A1)–(A6) at that $n$ [H5-1]
  116| $$
  117| E\big[1-\pi(S_0\mid y)\big]\ \le\ C\sqrt{\tfrac{\log n}{n}},
  118| $$
  119| and consequently, along any sequence satisfying (A1)–(A6),
  120| $$
  121| P\big(\mathrm{HPM}=\mathrm{MPM}=S_0\big)\ \ge\ 1-4C\sqrt{\tfrac{\log n}{n}}\ \to1,\qquad
  122| \max_{j\le p}\big|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}\big|\le 1-\pi(S_0\mid y)=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big).
  123| $$
```

`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 80–86:
```
   80| **Theorem 1.** In R1 under G, (E), (F_λ), (F_w):
   81| 1. **(Rate)** Under (BM): δ_n = 1 − π(S₀) = O_P(r_n).
   82| 2. **(Exact HPM, MPM, thresholded models)** Under (BM): P(HPM = S₀) ≥ P(δ_n < ½) → 1 and P(HPM ≠ S₀) ≤ 2Eδ_n → 0;
   83|    P(MPM = S₀) → 1; P(ξ_{q_n} = S₀) → 1 for every deterministic q_n ∈ (0, 1) with r_n = o(min(q_n, 1 − q_n)).
   84| 3. **(PIPs)** For every data set, max_j |PIP_j − 1{j ∈ S₀}| ≤ δ_n; under (BM) this is O_P(r_n) (sensitivity and
   85|    specificity uniformly in j), and E max_j |PIP_j − 1{j ∈ S₀}| → 0 (no expectation rate claimed).
   86| 4. **(Size, functionals)** Under (BM): π(|S| = s₀) = 1 − O_P(r_n); sup_{h:Ω→[0,1]} |π(h) − h(S₀)| = O_P(r_n).
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 955, §2.2, marginal inclusion probability; Condition 3 [SL-C3; transcribed from p. 955 image]:
```
Let q_j denote the marginal inclusion probability of the predictor x_j, which is given by
    q_j = π(j ∈ ξ | D_n) = Σ_{ξ∈{ξ̃: j∈ξ̃}} π(ξ | D_n).
… Therefore, to select true predictors consistently, it is necessary to control the severeness of multicollinearity. For this purpose, we introduce the following identifiability condition which controls the severeness of multicollinearity through the sequence {ε_n}.
Condition 3. A predictor x_k is said to be identifiable among all other predictors, if, for any 1 ≤ j_1, …, j_{r̄_n} ≤ P_n (j_i ≠ k for all i) and b_i ∈ ℝ,
    E[ exp{ −( x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i} )² } ] ≤ 1 − δ_n,    δ_n ≻ ε_n²,
where x_l denotes a generic observation of the predictor x_l.
This condition states that, if a predictor x_k is identifiable, then there does not exist a linear combination of other predictors in X which can mimic it.
```
Song & Liang (2015), p. 956, Theorem 3 (sure screening) and the paragraphs after it [SL-T3; transcribed from p. 956 image]:
```
Theorem 3 (sure screening). Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] < exp(−c_1 nε_n²), where ξ denotes a model sampled from the posterior distribution. Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] = 0.
The proof of theorem 3 can be found in the on-line supplementary material. Let ξ_q = {i : 1 ≤ i ≤ P_n, q_i > q} denote a model including all the predictors with the marginal inclusion probability greater than a threshold value of q ∈ (0, 1). Then it follows from theorem 3 that π(t ⊂ ξ_q) →^p 1 if all true predictors are identifiable. … Theorem S in the on-line supplementary material establishes the consistency of MAP models. Thus, we have two criteria for variable selection, by either marginal inclusion probabilities or the MAP model. Although theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled), we suggest the use of marginal inclusion probabilities as the criterion for variable selection.
```
**(c) Verdict(s) under test.**
- `core1:SUM.SL`
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 46–46, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   46| | HPM, MPM, PIPs from 1 − π(S₀ \| y) | Thm 3 gives screening only; MAP consistency is their Theorem S (supplement, not inspected) |
```

**(d) Track C evidence.**
(none)

### core1:PRIOR — The prior as coded (a setting, not an assumption)
**(a) Our assumption text.**
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 18–30:
```
   18| Data (X^r, y^r), n ≥ 3, with non-constant y^r (s_y > 0; a.s. under G) [R01-4]. p = number of **retained** (non-constant)
   19| raw columns (the code drops constant columns before K and the prior are formed, `Scripts/SMC_BVS/core/v3_preprocess.R:111-127`);
   20| X = CX^rD_x⁻¹ = standardised design of the retained columns (centred, ‖x_j‖² = n − 1), y = Cy^r/s_y with
   21| s_y² = ‖Cy^r‖²/(n − 1). Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋). G_S = X_SᵀX_S, H_S = (n + 1)G_S + I,
   22| D_S = det H_S / det(G_S + I), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S (z_S = X_Sᵀy), ν = 0.01 + n/2;
   23| m(S) ∝ D_S^{−1/2}(2b₀ + Q_S)^{−ν}, a₀ = b₀ = 0.01; prior ϖ(S) = w(|S|)/W_K, w(k) = ½/C(2p − 1, k) (capped BB(1, p));
   24| π(S) ∝ ϖ(S)m(S) on Ω. (Definitions: `ARC/main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md:9-14`; code:
   25| `Scripts/SMC_BVS/core/cpp/v3_score.h:40-71, 196-224` — K = min(p, n/2), ν = a₀ + n/2, H = (n+1)G + I, A = G + I,
   26| log w(k) = −log 2 − log C(2p−1, k).) Equivalently π is the exact posterior under the **working** likelihood
   27| y | S, β_S, σ² ~ N_n(X_Sβ_S, σ²I) with β_S | S, σ² ~ N(0, nσ²(G_S + I)⁻¹), σ² ~ IG(0.01, 0.01) on the standardised
   28| scale (the standardised y does not have this law under the truth; the proofs treat it as a working model, [P1]
   29| lines 155-221) [R01-4]. π is the real-arithmetic target of the code; floating-point fidelity is not part of this file.
   30| 
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 951, §2.1.1, prior (6) [SL-P6; transcribed from p. 951 image]:
```
For the model ξ, we assume that each predictor has a prior probability λ_n = r_n/P_n, independent of other predictors, to be included in the model ξ. Further, we impose a constraint on the model size such that |ξ| ≤ r̄_n, where the upper bound r̄_n is prespecified. Then the prior probability of ξ can be expressed as
    π(ξ) ∝ λ_n^{|ξ|} (1 − λ_n)^{P_n−|ξ|} I(|ξ| ≤ r̄_n).    (6)
… We let the variance σ² be subject to an inverse gamma prior distribution with the hyperparameters a_0 and b_0, i.e. σ² ∼ IG(a_0, b_0). Conditioned on the model ξ and σ², we let β_ξ be subject to a Gaussian prior:
    β_ξ | ξ, σ² ∼ N_{|ξ|}(0, σ² V_ξ),
where V_ξ is a positive definite matrix depending on ξ. … In this paper, we assume that λ_n → 0 as P_n → ∞, which corresponds to condition (13) in theorem 1.
```
Song & Liang (2015), p. 952, Theorem 1 and conditions (8)–(15) [SL-T1; transcribed from p. 952 image]:
```
Theorem 1 (posterior consistency). Assume that the data set D_n is drawn from model (1) and all predictors |x_i| ≤ 1. If there is a sequence {ε_n} ∈ (0, 1) such that nε_n² ≻ 1, and the following conditions hold,
    Δ(r_n) ≺ ε_n,    (8)
    r̄_n ln(1/ε_n²) ≺ nε_n²,    (9)
    r̄_n ln(P_n) ≺ nε_n²,    (10)
    r̄_n ln(nε_n² B̃_n) ≺ nε_n²,    (11)
    1 ≤ r_n ≤ r̄_n < P_n,    (12)
    r_n ≺ P_n,    (13)
    B(r_n) ≺ nε_n²,    (14)
then the posterior consistency holds, i.e. there is a constant c_1 > 0 such that
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²),    (15)
for sufficiently large n, where the Hellinger distance is
    d²(f, f*) = ∫∫ |φ^{1/2}(y; x^Tβ*, σ*) − φ^{1/2}(y; x^Tβ, σ)|² ν_x(dx) dy,
f* is as defined in expression (2), f is the density function for a model simulated from the posterior and P* denotes the probability measure of data generation.
```
Song & Liang (2015), p. 953, choices of V_ξ; 'ridge prior' [SL-V; transcribed from p. 953 image]:
```
The validity of this theorem depends on the choice of the prior covariance matrix V_ξ or, more precisely, the largest eigenvalues of V_ξ and V_ξ^{−1}. For most choices of V_ξ, B(r_n) ≤ B r_n^v and B̃_n ≤ B r_n^v hold for some positive constants B and v. For example, if V_ξ = c I_{|ξ|}, where I_p is an identity matrix of order p, then both B(r_n) and B̃_n are constants. One can also set V_ξ^{−1} = c E(x_ξ^T x_ξ) as in Zellner (1986) and Liang et al. (2008), where the expectation is replaced by its sample empirical estimator. If all x_i s are standardized with zero mean and equal variance, then B(r_n) ≤ r_n. Furthermore, if x_i has some specific covariance structure, then B̃_n can be shown to be bounded. For example, if all pairwise covariances cov(x_i, x_j) = ρ ∈ (0, 1), then B̃_n = 1 − ρ; if x_i is generated from a finite order auto-regressive or moving average model without root for the characteristic polynomial on the unit circle, then B̃_n is also bounded by some constant (Bickel and Levina, 2004). In general, for standardized x_i s, we can choose a 'ridge prior' as suggested by Gupta and Ibrahim (2009): let V_ξ^{−1} = E(x_ξ^T x_ξ) + c_n I_{|ξ|}; then B(r_n) ≤ r_n + c_n and B̃_n ≤ c_n^{−1}, where c_n is proportional to 1/n, i.e. c_n ∝ n^{−1}.
```
**(c) Verdict(s) under test.**
- `core1:PRIOR.SL`
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 34–35, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   34| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 38–38, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   38| | The prior as coded (a setting, not an assumption) | they tune: inclusion r_n/P_n, cap r̄_n, (6) p. 951, under conditions (9)–(14), p. 952; ours has no tuning |
```

**(d) Track C evidence.**
(none)

### core1:ROW13 — Theorem 3 (row 1.3): lower bound; witness designs
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 333–352:
```
  333| **Theorem 3.** (a) *(Every design.)* For every $n\ge3$, every standardised design with $p\ge2$, every response and every
  334| model $S$ with $|S|\le\min(K-1,p/2)$,
  335| $$
  336| \pi(S\mid y)\ \le\ \Big(1+\frac{|S|+1}{3\sqrt n}\Big)^{-1}.
  337| $$
  338| (b) *(Orthogonal or Gaussian null columns.)* Assume (S1), $s_0$ fixed, $\|X\theta^*\|^2\le nM$ and
  339| $\|\theta^*\|^2\le nM'$ with fixed $M,M'$, and either
  340| - **(N-orth)** the columns outside $S_0$ are mutually orthogonal and orthogonal to the columns in $S_0$; or
  341| - **(N-gauss)** the raw columns outside $S_0$ have i.i.d. $N(0,1)$ entries, independent of $X^{\mathrm r}_{S_0}$ and
  342|   $\varepsilon$, and $p\le n^A$.
  343| 
  344| Then, for every $p$ with $s_0<p$ (bounded or growing),
  345| $$
  346| \mathbb E\big[1-\pi(S_0\mid y)\big]\ \ge\ (1-o(1))\,(s_0+1)\,\frac{2(p-s_0)}{2p-1-s_0}\,\sqrt{\frac{\log\!\big(p\sqrt n/(s_0+1)\big)}{\pi n}},
  347| $$
  348| and, if moreover $p\to\infty$,
  349| $$
  350| 1-\pi(S_0\mid y)\ \ge\ (1-o_P(1))\,(s_0+1)\sqrt{\frac{\log p}{\pi n}}.
  351| $$
  352| 
```

`Theory_work/Wave3/W3-PSHARP/STATEMENT.md` @ e8b5351c, lines 92–100:
```
   92| **Corollary B.** For every n ≥ 3, every standardised design with p ≥ 2, every data set and every S₀ ⊆ [p] with
   93| 0 ≤ s₀ ≤ K − 1 (deterministic; no law, no truth):
   94|   δ_n/(1 − δ_n) ≥ 𝒪^{lb}_n := Σ_{j=1}^{K−s₀} C(s₀ + j, j) n^{−j/2} Π_{i=0}^{j−1} (p − s₀ − i)/(2p − 1 − s₀ − i) ≥ c(p, s₀)/√n,
   95| equivalently π(S₀) ≤ 1/(1 + 𝒪^{lb}_n), and in particular π(S₀) ≤ √n/(√n + c(p, s₀)) [K01-F3]. Here c(p, s₀) ≥ (s₀ + 1)/3 whenever s₀ ≤ p/2; c(p, s₀) ≥ 1 for s₀ ≥ 1;
   96| c(p, 0) > ½; and c(p, s₀)/(s₀ + 1) → ½ when p → ∞ and s₀/p → 0 [L01-m1].
   97| 
   98| **Consequences** (any sequence with s₀ ≤ min(K − 1, p/2); any designs; any data, random or not):
   99| - **(B1)** π(S₀) ≤ [1 + (s₀ + 1)/(3√n)]⁻¹ surely. So π(S₀) → 1 (in probability, along any subsequence) forces
  100|   s₀ = o(√n); if s₀ ≥ λ√n then π(S₀) ≤ 1/(1 + λ/3); and if s₀/√n → ∞ then π(S₀) → 0 surely.
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 952, Theorem 1 and conditions (8)–(15) [SL-T1; transcribed from p. 952 image]:
```
Theorem 1 (posterior consistency). Assume that the data set D_n is drawn from model (1) and all predictors |x_i| ≤ 1. If there is a sequence {ε_n} ∈ (0, 1) such that nε_n² ≻ 1, and the following conditions hold,
    Δ(r_n) ≺ ε_n,    (8)
    r̄_n ln(1/ε_n²) ≺ nε_n²,    (9)
    r̄_n ln(P_n) ≺ nε_n²,    (10)
    r̄_n ln(nε_n² B̃_n) ≺ nε_n²,    (11)
    1 ≤ r_n ≤ r̄_n < P_n,    (12)
    r_n ≺ P_n,    (13)
    B(r_n) ≺ nε_n²,    (14)
then the posterior consistency holds, i.e. there is a constant c_1 > 0 such that
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²),    (15)
for sufficiently large n, where the Hellinger distance is
    d²(f, f*) = ∫∫ |φ^{1/2}(y; x^Tβ*, σ*) − φ^{1/2}(y; x^Tβ, σ)|² ν_x(dx) dy,
f* is as defined in expression (2), f is the density function for a model simulated from the posterior and P* denotes the probability measure of data generation.
```
Song & Liang (2015), p. 953, Theorem 2 (pp. 953–954, with the note on (8)) [SL-T2; transcribed from p. 953 image]:
```
Theorem 2. Assume that the data set D_n is generated from model (1) and all the predictors satisfy condition 1. Given a sequence {ε_n}, ε_n → 0, and nε_n² → ∞, if the conditions (9)–(14) of theorem 1 hold, the model is strictly sparse, i.e. condition (4) holds, and r_n ≻ 1, then the posterior consistency still holds, i.e. there is a constant c_1 > 0 such that, for sufficiently large n,
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²).
Note that condition (8) of theorem 1 is redundant here as, for large n, r_n > |t| and Δ(r_n) = 0 hold under the sparseness condition (4). [the last words, from 'hold under', are on p. 954]
```
Song & Liang (2015), p. 954, Corollary 1 [SL-CO1; transcribed from p. 954 image]:
```
Corollary 1. Consider a strict sparse model, i.e. condition (4) holds. Suppose that P_n < exp(Cn^α) for some α ∈ (0, 1), and the prior specification in Section 2.1.1 is used such that B(r_n) ≤ B r_n^v and B̃_n ≤ B n^v for some positive constants B and v. Take
    r_n < r̄_n ≺ log^k(n),
or
    r_n < r̄_n ≺ n^q,
for some k > 0 or some 0 < q < min{1 − α, 1/v}. Then the convergence rate in theorem 2 can be taken as
    ε_n = O{n^{−(1−α)/2} log^{k/2}(n)},
or
    ε_n = O(n^{−(min{1−α−q, 1−vq})/2}).
```
Song & Liang (2015), p. 956, Theorem 3 (sure screening) and the paragraphs after it [SL-T3; transcribed from p. 956 image]:
```
Theorem 3 (sure screening). Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] < exp(−c_1 nε_n²), where ξ denotes a model sampled from the posterior distribution. Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] = 0.
The proof of theorem 3 can be found in the on-line supplementary material. Let ξ_q = {i : 1 ≤ i ≤ P_n, q_i > q} denote a model including all the predictors with the marginal inclusion probability greater than a threshold value of q ∈ (0, 1). Then it follows from theorem 3 that π(t ⊂ ξ_q) →^p 1 if all true predictors are identifiable. … Theorem S in the on-line supplementary material establishes the consistency of MAP models. Thus, we have two criteria for variable selection, by either marginal inclusion probabilities or the MAP model. Although theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled), we suggest the use of marginal inclusion probabilities as the criterion for variable selection.
```
**(c) Verdict(s) under test.**
- `core1:ROW13.SL`
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 117–121, cells 'Assumption' and 'Song–Liang (2015)' only:
```
  117| | Assumption | Song–Liang (2015) |
  119| | Part (a): none (every design, every response) | no lower bound in SL |
  120| | Part (b): Gaussian errors, s₀ fixed, energy and coefficient bounds | — |
  121| | Part (b): orthogonal or i.i.d. N(0, 1) null columns | — |
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 235–236:
```
  235| **Verdict: not an assumption to defend** (a lower bound needs one design; SL have no lower bound). Part (a) has no
  236| assumption. **Designs.** S1 and IND are of type (N-gauss) only if the truths are independent of the nulls (they are).
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 255–255:
```
  255| | B12 | witness designs (3(b)) | no counterpart (no lower bound in SL) | — | — | — |
```

**(d) Track C evidence.**
(none)

### core1:SCOPE — Core-level verdict for the posterior theorems
**(a) Our assumption text.**
(core-level verdict; see §1 and the items above)
**(b) Song–Liang text.**
(none cited by the audit for this item)
**(c) Verdict(s) under test.**
- `core1:SCOPE.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 14–17:
```
   14| 1. **The posterior theorems (core 1: the true model; core 2: the true distribution) hold on all our designs** — the
   15|    2,400-fit study, P6 with its strong factors, and the 1M plan — **under assumptions that are the same as, or comparable
   16|    to, Song–Liang's.** Three items are stronger than theirs: the range of p (p ≤ n^A, B2), a collinearity floor of order
   17|    c/n on O(log n) columns (B6), and the law of the rows (Gaussian or sub-Gaussian, B7).
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 24–26:
```
   24| | Core theorem | Assumptions against Song–Liang | Our designs inside |
   25| |---|---|---|
   26| | 1 and 2 (posterior) | same or comparable; stronger: B2, B6, B7 | **all** |
```

**(d) Track C evidence.**
(none)

---

## Task (sent as a separate block)

Break the comparison; findings only.

Verdicts to judge (20), in this order; return one machine line for each:
core1:B1.SL
core1:B1.IO
core1:B2.SL
core1:B2.IO
core1:B3.SL
core1:B3.IO
core1:B4-UP.SL
core1:B4.IO
core1:B4-LO.SL
core1:B5.SL
core1:B5.IO
core1:B6.SL
core1:B6.IO
core1:B7.SL
core1:B7.IO
core1:DR.SL
core1:SUM.SL
core1:PRIOR.SL
core1:ROW13.SL
core1:SCOPE.IO

# AUDIT1 — core3: row 3.1 (Theorem 6: the coded method reports the true model)

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
Standing assumptions (S1)–(S3) of the reader versions:
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 28–31:
```
   28| (S1) Model of §1 of the notation: Gaussian errors with fixed variance $\sigma_*^2>0$, independent of the design.
   29| (S2) Asymptotics: $n\to\infty$, $p=p_n$ with $2\le p\le n^A$ for a fixed $A\ge1$ ($p\gg n$ allowed).
   30| (S3) "The method" means the method as coded, under the standing conventions of `NOTATION.md` §5 (exact arithmetic,
   31| shipped configuration, admissible runs). (S3) matters only for Theorems 5–8.
```

Reader statement of Theorem 6 (row 3.1):
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 666–703:
```
  666| **Theorem 6.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a positive definite
  667| correlation matrix, and $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with deterministic $\theta^*$. Fix
  668| $b\in(0,\tfrac12)$ and $\rho>0$ with $15\rho+b<\tfrac12$. Assume
  669| - **(A1) Model.** (S1), (S2) ($p\gg n$ allowed), (S3).
  670| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  671|   $S_0$.
  672| - **(A3) Visibility.** $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a>0$ for every $j\in S_0$ and every
  673|   $U\not\ni j$ with $|U|\le15$.
  674| - **(A4) Polynomial leakage set.** There is a deterministic $Q\supseteq S_0$ with $|Q|\le n^b$ and, for large $n$,
  675|   $|Q|\le K$ and ($Q=[p]$ or $K\ge2|Q|+32s_0+1$), such that:
  676|   (i) *(no leak outside $Q$)* there is a deterministic $\varpi_n$ with $\varpi_n\sqrt{n/\log n}\to0$ such that
  677|   $|\operatorname{Cov}(W_l,W_j\mid W_U)|\le\varpi_n$ for all $l\notin Q$, $j\in S_0\setminus U$, $|U|\le15$;
  678|   (ii) *(locality)* there is a deterministic $r_n\to0$, and every $l\notin Q$ has a deterministic
  679|   $H_l\supseteq\{l\}\cup S_0$, $|H_l|\le n^{\rho}$, such that for all $l\notin Q$, all $U\not\ni l$ with $|U|\le15$
  680|   and $U_0:=U\cap H_l$: $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|\le r_n$ and
  681|   $|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for all $v\in U\setminus H_l$, $j\in S_0\setminus U_0$ [S1-F3].
  682| - **(A5) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c>0$ for every $S$ with
  683|   $|S|\le5(A+1)(s_0+1)\log n$ and for every $S=Q\cup\{l\}$, $l\in[p]$.
  684| - **(A6) Local regressions within $Q$.** There are deterministic sequences $\nu_n=o(\log n)$ and $L_n$, and for every
  685|   $l\in[p]$ a deterministic $N_l\subseteq Q\setminus\{l\}$ with $|N_l|\le\nu_n$ [S1-F3], such that
  686|   $\|\bar\beta_{T,l}-\bar\beta_{T\cap N_l,l}\|_1\le L_n$ for every $T$ with $S_0\subseteq T\subseteq Q$, $l\notin T$,
  687|   where $L_n\to0$ and $L_n^2\log(|Q|+1)=o(\log n)$ (bars: population regression coefficients, zero-padded).
  688| 
  689| Then, under the joint law of design and noise, there are data events $\mathcal G_n$ with $P(\mathcal G_n)\to1$ on
  690| which **every** admissible run that produces output reports $\hat S=S_0$, whatever its seed and the outcome of its
  691| internal calibration; in particular $P(\text{output and }\hat S\neq S_0)\to0$. If moreover the delivery conventions (S4)(i)–(iv) hold [S1-F2], $P(\text{the run produces output})=1$ for every admissible
  692| $n\ge3$ with $(n,p_{\mathrm{raw}})$ in the bounded domain $\mathfrak D$ of (S4)(v), where the code's two fixed integer limits are not
  693| reached. If in addition IDEAL-W⁺ holds ((S4)(v): the two limits lifted),
  694| $$
  695| P(\text{the run produces output})=1\ \ \text{for every admissible }n\ge3,\qquad P(\hat S=S_0)\to1 .
  696| $$
  697| The delivery statement idealises two fixed integer limits in the code (a base search cap of $10^6$, `v3_run.R:96`, and a 32-bit integer bound $2^{31}-1$ on the search cap, `cpp/v3_core.cpp:474`): the first can bind only when $n+p+1$ exceeds $2^{10^6}$, the second only when the starting model has more than about $2.1\times10^9$ variables, which needs $n\gtrsim4.3\times10^9$ since $|\tilde S_0|\le\lfloor n/2\rfloor$; without the idealisation, delivery holds on the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, and with it (IDEAL-W⁺) for every $n$ [RM2R-5].
  698| 
  699| *Remarks.* (i) On $\mathcal G_n$ the local search from the start mode only deletes the spurious members of the start
  700| mode, one per move, at most $n^b$ moves, and certifies $S_0$; its move cap never binds. (ii) The polylogarithmic case
  701| $|Q|\le(\log n)^{\kappa}$ is a special case (the earlier version of the theorem). (iii) Examples (never hypotheses):
  702| metric-local correlation, polynomial correlation decay of exponent $\alpha>2$ (example status unchecked), one-factor
  703| blocks.
```

Master Setting R (W3-RM) and constants (Form R, W3-RM2):
`Theory_work/Wave3/W3-RM/STATEMENT.md` @ e8b5351c, lines 41–44:
```
   41| * **Setting R (Gaussian rows)** = UNI `STATEMENT.md` §1 design (R) / LOC2 `STATEMENT.md` §1: raw rows iid
   42|   N(m_n, Σ_n), Σ_n unit-diagonal, X centred and sample-standardised, Y = Xθ* + Cε, ε ~ N(0, σ²I_n) independent of the
   43|   raw design, σ² > 0 fixed [C1-B7], s₀ fixed, |θ*_j| ∈ [θ_lo, θ_hi] ⊂ (0, ∞) on S₀, p ≤ n^A (p ≫ n allowed). W denotes a
   44|   population row.
```

`Theory_work/Wave3/W3-RM2/STATEMENT.md` @ e8b5351c, lines 112–116:
```
  112| Fixed constants [SL1-1: the two forms have separate constants]. Common: A ≥ 1, s₀; δ₀ ∈ (0, 1) for the
  113| fixed-fraction form (W-δ).
  114| **Form F:** M > 0, φ₀ ∈ (0, 1], g₀ > 0, η ∈ [0, η_A), **b ∈ (0, β(η, A))**; for the sufficient forms h ≥ 0 with
  115| **h + b < ½**, m₀ ∈ ℕ, δ₁ ∈ (0, 1). **Form R:** c > 0, θ_lo, θ_hi, a₀ > 0, **b ∈ (0, ½)** (no η; not tied to
  116| β(η, A)), ρ > 0 with **15ρ + b < ½** [v1.4: the constant C_L of v1.3 is replaced by the leak sequence ϖ_n].
```

Master conditions inherited from W3-RM (T1-R), (FL-R), (V-R):
`Theory_work/Wave3/W3-RM/STATEMENT.md` @ e8b5351c, lines 129–136:
```
  129| * **(T1-R) Theorem 1's conditions** = (A1-post) of UNI `STATEMENT.md` §2, i.e. the LSF conditions of APP L1_POST(b)
  130|   [R01-opt]: with j₀ = ⌈(2A + 1)s₀⌉ + 1, m̄_n = ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n]/log(3/2)⌉ and
  131|   k̄_n = min{p, s₀ + max(j₀, m̄_n)}: for a fixed φ > 0, λ_min(Σ_{n,S}) ≥ φ² whenever |S| ≤ min(p, s₀ + j₀), and
  132|   λ_min(Σ_{n,S}) ≥ ψ_n whenever |S| ≤ k̄_n, with ψ_n√n/(log n)^{3/2} → ∞. No upper spectral bound.
  133|   Sufficient: λ_min(Σ_n) ≥ c.
  134| * **(FL-R)** λ_min(Σ_{n,S}) ≥ c for every S with |S| ≤ 16 + s₀, and for S = Q ∪ {l}, l ∈ [p].
  135| * **(V-R) Visibility** = PTV(a₀) (APP `lemmas/L3_LOC.md:28`): for every j ∈ S₀ and U ⊆ [p] ∖ {j}, |U| ≤ 15:
  136|   |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀.
```

Master §3.2 (Gaussian rows) and the theorem (C2):
`Theory_work/Wave3/W3-RM2/STATEMENT.md` @ e8b5351c, lines 172–202:
```
  172| ### 3.2 Gaussian rows (conditions on (Σ_n, θ*) and Q only)
  173| 
  174| * **(T1-R)**, **(FL-R)**, **(V-R)**: exactly as in RM `STATEMENT.md:129-136` ((FL-R): λ_min(Σ_{n,S}) ≥ c for
  175|   |S| ≤ 16 + s₀ and for S = Q ∪ {l}, l ∈ [p]; (V-R) = PTV(a₀)).
  176| * **(L-R^b) Polynomial leakage, localised** [CP2-P3, CP2-T6: v1.4]. A deterministic Q ⊇ S₀ with (L-size^b)
  177|   |Q| ≤ n^b and (L-feas), and deterministic sequences ϖ_n, r_n ≥ 0 (ϖ_n is the leak sequence — written ℓ_n in
  178|   v1.4 as first drafted; the symbol ℓ_n is reserved for the LS0 move cap of §1 [SC2-1]) with **ϖ_n√(n/log n) → 0** and **r_n → 0** (no rate),
  179|   such that
  180|   **(L-gain-R)** for every l ∉ Q, every U ⊆ [p] ∖ {l} with |U| ≤ 15 and every j ∈ S₀ ∖ U:
  181|   |Cov(W_l, W_j | W_U)| ≤ ϖ_n;
  182|   **(L-loc-R)** for every l ∉ Q there is a deterministic H_l ⊇ {l} ∪ S₀ with **|H_l| ≤ n^ρ** such that for every
  183|   U ⊆ [p] ∖ {l} with |U| ≤ 15, writing U₀ := U ∩ H_l: |Cov(W_l, W_v | W_{U₀})| ≤ r_n and |Cov(W_j, W_v | W_{U₀})| ≤ r_n
  184|   for every v ∈ U ∖ H_l and j ∈ S₀ ∖ U₀. Budget: 15ρ + b < ½.
  185|   In words: outside Q, the conditional covariance of a column with a truth, given any 15 other columns, is below
  186|   the noise scale √(log n/n) (the Gaussian-row counterpart of (L-gain) with η → 0); and every column outside Q has
  187|   a neighbourhood H_l, with at most n^ρ members, outside which columns are asymptotically conditionally
  188|   uncorrelated with it and with the truths. H_l only has to capture correlations that do not vanish, so ρ may be
  189|   taken as small as the design allows.
  190|   **Sufficient — a generalisation of the v1.3 localised form, (L-R^b-loc)** [SC2-4], which contains RM's (L-R): the leak bound only at the localised sets,
  191|   |Cov(W_l, W_j | W_{U₀})| ≤ ϖ′_n for j ∈ S₀ ∖ U₀ with ϖ′_n√(n/log n) → 0 (RM: ϖ′_n = C_L n^{−1/2}), together with the
  192|   rate r_n(n/log n)^{1/4} → 0 (RM: r_n(n log n)^{1/4} → 0); then (L-gain-R) holds with ϖ_n = ϖ′_n + 15r_n²/c
  193|   (`lemmas/L4_sandR_b.md` §7, item 1 [SC2-3]).
  194| * **(W-R) Lattice width on the realised design** [CP1-P2]. Let 𝒲⁰_n := {λ_min(R̂_{Q∪{l}}) ≥ c/2 for every
  195|   l ∈ [p]} (on it every u_{T,l}, (T, l) ∈ 𝔓, is defined, so 𝔴⁰_n and 𝔴_n(δ) are defined for the realised X)
  196|   [SL1-opt3]. (W-R): there is a deterministic t_n → ∞ with P(𝒲⁰_n ∩ {𝔴⁰_n ≤ −t_n}) → 1.
  197|   Sufficient: P(𝒲⁰_n ∩ {𝔴_n(δ₀) ≤ 0}) → 1 for some fixed δ₀ ∈ (0, 1) (the v1.2 form; then t_n = δ₀√(log n)/(2√(2A + 2))).
  198|   The latter holds **for every fixed δ₀ ∈ (0, 1 − 2b)** [SL1-1] under **(D-R^b)**: hypotheses (N1), (R1)–(R3) of LOC2 Lemma NA-R (`Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md:23-36`)
  199|   for (Σ_n, Q), with its deterministic latent-extension contract (`L2_NAR.md:15-20`), where (N0)'s size bound is
  200|   replaced by |Q| ≤ n^b, b < ½ (frames: log N_n ≤ log p + o(log n); atoms: L_n² log(|𝒜_n| + 1) = o(log n); variance
  201|   ratio η_n → 0). Sufficient for (D-R^b) — **(D-loc^b)**: RM's (D-loc) (`STATEMENT.md:154-156`) with
  202|   L_n² log(|Q| + 1) = o(log n) (so L_n → 0 at polynomial size).
```
`Theory_work/Wave3/W3-RM2/STATEMENT.md` @ e8b5351c, lines 215–218:
```
  215| 
  216| **(C2) Theorem RM2-R (Gaussian rows, polynomial leakage).** Setting R, the method as coded, any X-measurable
  217| partition with blocks ≤ 16. Assume (T1-R), (FL-R), (V-R), (L-R^b) with 15ρ + b < ½, and (W-R). Then, under the joint
  218| law of (X, ε): [SAND(Q)], [TL(Q)], [NA(Q)], [POST], hence all conclusions of RM-0 as in (C1).
```

Master sufficient form (W-loc) for the width condition (referred to by (A6)):
`Theory_work/Wave3/W3-RM2/STATEMENT.md` @ e8b5351c, lines 159–168:
```
  159|   **(W-loc) Local regressions.** For every l ∈ [p] a deterministic N_l ⊆ Q ∖ {l} with |N_l| ≤ ν_n,
  160|   ν_n log 2 ≤ h log n, and a deterministic L_n ≥ 0 with L_n² log(|Q| + 1) = o(log n), such that
  161| 
  162|     ‖β̄_{T,l} − β̄_{T∩N_l,l}‖₁ ≤ L_n  and  ‖(I − P_{T∩N_l})x_l‖² ≤ (1 + η_n)‖(I − P_T)x_l‖²  for every (T, l) ∈ 𝔓,
  163| 
  164|   with a deterministic η_n → 0 (under (FL-Q) the second inequality follows from the first with η_n = L_n²/φ₀²
  165|   whenever L_n → 0). T ∩ N_l need not contain S₀ and may be empty; β_{T∩N_l,l} is the regression of §1 [SL1-2]. In
  166|   words: the regression of any column on any lattice set is carried, up to a small ℓ¹ coefficient error, by at most
  167|   ν_n ≤ h log n/log 2 lattice members attached to that column, h < ½ − b [SL1-opt2]. (When |Q| has genuine polynomial
  168|   order, |Q| ≥ n^{b′} for a fixed b′ > 0, log(|Q| + 1) ≍ log n and L_n → 0 is required; N_l = ∅ is allowed.)
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

### core3:B7 — Rows i.i.d. Gaussian; (S1), (S2)
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 666–669:
```
  666| **Theorem 6.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a positive definite
  667| correlation matrix, and $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with deterministic $\theta^*$. Fix
  668| $b\in(0,\tfrac12)$ and $\rho>0$ with $15\rho+b<\tfrac12$. Assume
  669| - **(A1) Model.** (S1), (S2) ($p\gg n$ allowed), (S3).
```

`Theory_work/Wave3/W3-RM/STATEMENT.md` @ e8b5351c, lines 41–44:
```
   41| * **Setting R (Gaussian rows)** = UNI `STATEMENT.md` §1 design (R) / LOC2 `STATEMENT.md` §1: raw rows iid
   42|   N(m_n, Σ_n), Σ_n unit-diagonal, X centred and sample-standardised, Y = Xθ* + Cε, ε ~ N(0, σ²I_n) independent of the
   43|   raw design, σ² > 0 fixed [C1-B7], s₀ fixed, |θ*_j| ∈ [θ_lo, θ_hi] ⊂ (0, ∞) on S₀, p ≤ n^A (p ≫ n allowed). W denotes a
   44|   population row.
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
Song & Liang (2015), p. 950, §2.1, growth of P_n; sparsity conditions (3) and (4) [SL-M3; transcribed from p. 950 image]:
```
As in conventional studies of high dimensional variable selection, we consider the asymptotics of the SAM approach under the assumption that P_n increases as n increases. To be specific, we assume that P_n ≻ n^θ for some θ > 0, where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0. In addition, we assume that the true model is sparse. Two sparseness conditions are considered in this paper. One states that most components of β* are very small such that
    lim_{n→∞} Σ_{j=1}^{P_n} |β*_j| < ∞,    (3)
where β*_j denotes the jth entry of β*. The other one is stronger but more usual, which requires that most components of β* are 0 such that
    lim_{n→∞} Σ_{j=1}^{P_n} 1{β*_j ≠ 0} < ∞.    (4)
Let ξ ⊂ {1, …, P_n} denote a subset model, which includes the indices of all selected predictors. Let |ξ| denote the number of predictors included in ξ. Thus, the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ P_n} has a finite model size.
```
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
- `core3:B7.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 140–140:
```
  140| **Verdict: Thm 9 (A3) is stronger than Song–Liang's Condition 1 and implies it; Gaussian rows are stronger still.**
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 74–76, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   74| | Assumption | Song–Liang (2015) |
   76| | Rows i.i.d. Gaussian; (S1), (S2) | stronger than Condition 1, p. 953 |
```

- `core3:B1.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 63–63:
```
   63| **Verdict: same as Song–Liang** (their model (1) and density (2), p. 950).
```

- `core3:B2.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 69–70:
```
   69| **Verdict: stronger than Song–Liang on the upper range** (their Corollary 1, p. 954, allows P_n < exp(Cn^α), α ∈ (0, 1));
   70| **weaker on the lower range** (they assume P_n ≻ n^θ for some θ > 0, p. 950; we need no growth of p).
```

- `core3:B7.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–245:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
  244| | B1 | Gaussian linear model (all) | same: (1)–(2), p. 950 | in / in / in / in | in | in / in / in / in |
  245| | B2 | p ≤ n^A (all) | stronger above (Cor 1, p. 954); weaker below (P_n ≻ n^θ, p. 950) | in | in | in (A ≈ 2.6) |
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 250–250:
```
  250| | B7 | Gaussian rows (2, 6, 10); sub-Gaussian sparse directions (9) | stronger than Condition 1, p. 953 (implies it) | in | in | in |
```

**(d) Track C evidence.**
(none)

### core3:A2 — (A2) s₀ fixed, fixed nonzero signals
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 670–671:
```
  670| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  671|   $S_0$.
```

`Theory_work/Wave3/W3-RM/STATEMENT.md` @ e8b5351c, lines 41–44:
```
   41| * **Setting R (Gaussian rows)** = UNI `STATEMENT.md` §1 design (R) / LOC2 `STATEMENT.md` §1: raw rows iid
   42|   N(m_n, Σ_n), Σ_n unit-diagonal, X centred and sample-standardised, Y = Xθ* + Cε, ε ~ N(0, σ²I_n) independent of the
   43|   raw design, σ² > 0 fixed [C1-B7], s₀ fixed, |θ*_j| ∈ [θ_lo, θ_hi] ⊂ (0, ∞) on S₀, p ≤ n^A (p ≫ n allowed). W denotes a
   44|   population row.
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
- `core3:A2.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 78–79:
```
   78| **Verdict: same as Song–Liang** (their strict sparsity (4), p. 950, used by Theorems 2–3; their Theorem 1 alone allows
   79| the weaker (3)).
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 89–92:
```
   89| **Verdict: comparable to Song–Liang.** Above: their (3) with |x_i| ≤ 1 (Theorem 1, p. 952) bounds the signal; under (4)
   90| alone their main text states no bound. Below: their Theorem 3 (p. 956) states **no** beta-min; a true predictor needs
   91| only to be "identifiable" (Condition 3, p. 955), and the step "d(f*, f) ≥ ε_n for any density f that does not select x_t"
   92| is in their supplement (not inspected).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 74–75, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   74| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 77–77, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   77| | (A2) s₀ fixed, fixed nonzero signals | same: (4), p. 950 |
```

- `core3:A2.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 246–247:
```
  246| | B3 | s₀ fixed (all) | same: (4), p. 950 | in (as a sequence) | in | in |
  247| | B4 | signal bounded; fixed nonzero or beta-min (1, 2, 6, 10; 9 above only) | comparable: (3), p. 950; no beta-min stated in Thm 3, p. 956 | in | in | in |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 45–45:
```
   45| P7: BM rate θ_min²nφ̂₀²/log n and margin Δ̂/log n grow like n^0.7–1.15 in every design and placement; M̂ is bounded.
```


### core3:B8 — (A3) visibility given ≤ 15 columns
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 672–673:
```
  672| - **(A3) Visibility.** $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a>0$ for every $j\in S_0$ and every
  673|   $U\not\ni j$ with $|U|\le15$.
```

`Theory_work/Wave3/W3-RM/STATEMENT.md` @ e8b5351c, lines 135–136:
```
  135| * **(V-R) Visibility** = PTV(a₀) (APP `lemmas/L3_LOC.md:28`): for every j ∈ S₀ and U ⊆ [p] ∖ {j}, |U| ≤ 15:
  136|   |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀.
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 956, §2.3 (pp. 956–957): subset model, (17), Condition 4, Theorem 4, β_0, Corollary 2 [SL-MIS; transcribed from p. 956 image]:
```
Let D_n^s = {y, X_s} denote a fixed subset of observations, where s ⊂ {1, 2, …, P_n} and X_s contains only s = |s| < P_n predictors with the indices belonging to s. Assume that X_s does not include all of the true predictors of model (1). Therefore, the model
    y = X_s β_s + ε
is misspecified. … Let P_s denote a set of parameterized densities for all possible models formed with X_s. It is obvious that f* ∉ P_s. Let f_0 denote the minimization point of the Kullback–Leibler divergence in P_s, i.e.
    f_0 = arg min_{f∈P_s} ∫ ln(f*/f) f*.    (17)
… [p. 957] Condition 4. There is a constant δ > 0 such that for any a = (a_1, …, a_s)^T ∈ ℝ^s, with |a_i| ≤ δ for i = 1, …, s, we have
    E{(a^T x_s)²} < ∞,
where x_s denote a generic observation of the predictors included in X_s.
Theorem 4. (posterior consistency for misspecified models). Assume that condition 4 holds for a given subset s. Under the prior setting as described above, for any ε > 0,
    π[{f ∈ P_s : d(f_0, f) > ε} | D_n^s] → 0,    almost surely,    (18)
as n → ∞, where f_0 is as defined in equation (17), and f is a parameterized density proposed from posterior.
It follows from lemma 1.2 (in the on-line supplementary material) that f_0 = φ(y; β_0^T x_s, σ_0) ν(x_s), where ν(x_s) denotes the probability measure of x_s, and β_0 is given by
    β_0 = arg min_{β_s} E(β_s^T x_s − β*^T x)²,
i.e. β_0^T x_s is the projection of β*^T x. Let s̃ denote the subset of s corresponding to non-zero entries of β_0. Following the proof of theorem 3, we have the following corollary.
Corollary 2. Assume that the conditions of theorem 4 hold. If x_s does not have exact multicollinearity between variables, i.e. there does not exist a non-zero vector a ∈ ℝ^s such that P(a^T x_s = 0) = 1, then for the posterior probability of model ξ, conditioned on the subset D_n^s, we have
    π(s̃ ⊂ ξ | D_n^s) →^p 1.
```
Song & Liang (2015), p. 957, eq. (19); Condition 5 and remark (a) (pp. 957–958) [SL-C5; transcribed from p. 957 image]:
```
Corollary 2 implies that the marginal inclusion probability criterion is still applicable for selection of predictors in X_s. For any true predictor x_t with t ∈ t ∩ s, it will be asymptotically selected under this criterion if and only if β_{0,t} ≠ 0, where β_{0,t} is the entry of β_0 corresponding to x_t. Let y denote a generic observation of the response variable, let x_t denote a generic observation of the true predictors and let β*_t denote the regression coefficient vector of the true predictors. Since
    β_0 = Σ_s^{−1} Σ_{s,t} β*_t = Σ_s^{−1} cov(x_s, y),    (19)
where Σ_s = var(x_s) and Σ_{s,t} = cov(x_s, x_t), s̃ is determined by the correlation structure of x_s and x_t and the value of the true regression coefficients. However, when t ⊄ s, it is unclear whether β_{0,t} is exactly 0 or not. Following from equation (19), if cov(x_s, y) ≠ 0, then β_0 ≠ 0 and thus at least one predictor in s will be selected according to the marginal inclusion probability criterion. This motivates us to propose an iterative variable selection method for the subset data, provided that the following condition holds.
[p. 958] Condition 5. |cov(x_t, y)| > 0 for any true predictor x_t.
The iterative variable selection method can be described as follows: first select predictors from X_s based on the marginal inclusion probabilities estimated from the posterior π(ξ | D_n^s); denote the set of unselected predictors by X_{s′}, and then select predictors again from X_{s′} based on the marginal inclusion probabilities estimated from the posterior π(ξ | y, X_{s′}); keep running the iterative procedure until no predictors can be selected. Denote all the selected predictors by X_{s̃}. Under assumption 5, this procedure ensures that all true predictors that are contained in X_s will be selected.
There are a few remarks on this iterative procedure.
(a) Other than true predictors, how many other predictors will be selected? Generally speaking, all the predictors that are correlated with X_t will be selected, because they are correlated with y, where X_t denotes the set of all true predictors in D_n. This means that, if all the predictors are linearly correlated, it is futile to apply this iterative procedure, as all the predictors will be selected. The rationale underlying the SAM strategy lies in the belief that, for a big data set, there are only a small proportion of predictors that are linearly correlated with X_t. It is easy to show that if there are p_n predictors correlated with the true predictor X_t, p_n ≺ P_n, then there are at most c p_n predictors to be selected into X_{s̃} for some constant c.
```
**(c) Verdict(s) under test.**
- `core3:B8.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 155–156:
```
  155| **Verdict: stronger than Song–Liang's Condition 5** (p. 958: |cov(x_t, y)| > 0 for every true predictor), which is its
  156| case U = ∅ without the margin; same role (the cheap first stage must see every true predictor).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 74–75, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   74| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 78–78, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   78| | (A3) visibility given ≤ 15 columns | stronger than Condition 5, p. 958 (its case U = ∅) |
```

- `core3:B8.LEMMA`
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 183–183, cells 'Assumption' and 'Song–Liang (2015)' only (the implication proposed as a lemma; under test as stated):
```
  183| Thm 6 (A3) ⇒ their Condition 5 (dossier B8). Candidate corollaries in primitive terms: Thm 2 and Thm 9 already are (their
```

- `core3:B8.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 251–251:
```
  251| | B8 | visibility, ≤ 15 conditioning columns (6, 10) | stronger than Condition 5, p. 958 (its case U = ∅) | in / in / in / unclear | cs in; fac2, s5 unclear | in / in / in / unclear |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 21–23:
```
   21| | D | design | P1–P3 floors: sample φ̂²(k=16) at n=1600 [slope]; pop λ_min(Σ) | P4 visibility v̂ = δ̂²/log n (sample) / pop | P5 leak size \|Q̂\| (pop, ε=0.2), n=200→1600 | P6 local-regression ℓ¹ tail (ν=4, q99) | P9 width 𝔴̂⁰ | P7 BM rate, margin/log n | P8 𝒪¹/r_n | P10 |
   22| |---|---|---|---|---|---|---|---|---|---|
   23| | 01 | IND | IN↑ 0.60 [+.42]; 1 | IN↑ both [+1.5] / 1 | IN 4 → 4 | IN 0 | IN −0.77 | IN↑ | IN | OUT |
```
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 36–40:
```
   36| | 14 | FAC a=1 k=1 (cs .5) | IN↑ 0.30 [+.40]; 0.5 | **sp OUT** (pop 0; sample 4e-4→0.13); cl IN↑ / 0.53 | OUT Q̂ = [p] | OUT | OUT +0.85 | IN↑ | IN | OUT |
   37| | 15 | FAC a=1 k=3 | IN↑ 0.32 [+.42]; 0.5 | **sp OUT** (pop 0; sample ≈1e-10, falling); cl IN↑ / 0.54 | OUT Q̂ = [p] | OUT | OUT +0.86 | IN↑ | IN | OUT |
   38| | 16 | S5 (0.3 global + block) | IN↑ 0.22 [+.32]; 0.3 | IN↑ both (sp 0.55→18) / sp 0.06, cl 0.36 | OUT Q̂ = [p] (global factor) | OUT | OUT +0.84 | IN↑ | IN | OUT |
   39| | 17 | S6 (blocks ρ .4–.9) | IN↑ 0.16 [+.34]; 0.1 | IN↑ both (sp ≈0 at n = 200 only) / 0.25–0.71 | IN 20, 5 | IN↑ 1.5→0.5 | IN | IN↑ | IN | OUT |
   40| | 18 | riboflavin-like | IN↑ but small 0.09 [+.21]; 0.1 | **OUT both** (pop ≈0; sample ≈0 at every n) | OUT Q̂ = [p] | OUT (≈13–21) | OUT +0.85 | IN↑ (margin 4→35) | IN | OUT |
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
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 61–64:
```
   61| 2. **Visibility (V)/(V-R) = PTV fails at the population level for the strong-factor designs with the spread (mixed-sign)
   62|    truth (D14, D15) and for the riboflavin-like design (both placements):** a masking set drives the truth column's
   63|    conditional covariance with μ to 0 (sign cancellation), and the sample v̂ does not grow. Clustered aligned truths in
   64|    factor designs are inside. Same mechanism as the NEG regime of W3-P6.
```


### core3:B9 — (A4) leakage set |Q| ≤ n^b, no leak outside, locality
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 674–681:
```
  674| - **(A4) Polynomial leakage set.** There is a deterministic $Q\supseteq S_0$ with $|Q|\le n^b$ and, for large $n$,
  675|   $|Q|\le K$ and ($Q=[p]$ or $K\ge2|Q|+32s_0+1$), such that:
  676|   (i) *(no leak outside $Q$)* there is a deterministic $\varpi_n$ with $\varpi_n\sqrt{n/\log n}\to0$ such that
  677|   $|\operatorname{Cov}(W_l,W_j\mid W_U)|\le\varpi_n$ for all $l\notin Q$, $j\in S_0\setminus U$, $|U|\le15$;
  678|   (ii) *(locality)* there is a deterministic $r_n\to0$, and every $l\notin Q$ has a deterministic
  679|   $H_l\supseteq\{l\}\cup S_0$, $|H_l|\le n^{\rho}$, such that for all $l\notin Q$, all $U\not\ni l$ with $|U|\le15$
  680|   and $U_0:=U\cap H_l$: $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|\le r_n$ and
  681|   $|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for all $v\in U\setminus H_l$, $j\in S_0\setminus U_0$ [S1-F3].
```

`Theory_work/Wave3/W3-RM2/STATEMENT.md` @ e8b5351c, lines 176–184:
```
  176| * **(L-R^b) Polynomial leakage, localised** [CP2-P3, CP2-T6: v1.4]. A deterministic Q ⊇ S₀ with (L-size^b)
  177|   |Q| ≤ n^b and (L-feas), and deterministic sequences ϖ_n, r_n ≥ 0 (ϖ_n is the leak sequence — written ℓ_n in
  178|   v1.4 as first drafted; the symbol ℓ_n is reserved for the LS0 move cap of §1 [SC2-1]) with **ϖ_n√(n/log n) → 0** and **r_n → 0** (no rate),
  179|   such that
  180|   **(L-gain-R)** for every l ∉ Q, every U ⊆ [p] ∖ {l} with |U| ≤ 15 and every j ∈ S₀ ∖ U:
  181|   |Cov(W_l, W_j | W_U)| ≤ ϖ_n;
  182|   **(L-loc-R)** for every l ∉ Q there is a deterministic H_l ⊇ {l} ∪ S₀ with **|H_l| ≤ n^ρ** such that for every
  183|   U ⊆ [p] ∖ {l} with |U| ≤ 15, writing U₀ := U ∩ H_l: |Cov(W_l, W_v | W_{U₀})| ≤ r_n and |Cov(W_j, W_v | W_{U₀})| ≤ r_n
  184|   for every v ∈ U ∖ H_l and j ∈ S₀ ∖ U₀. Budget: 15ρ + b < ½.
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 957, eq. (19); Condition 5 and remark (a) (pp. 957–958) [SL-C5; transcribed from p. 957 image]:
```
Corollary 2 implies that the marginal inclusion probability criterion is still applicable for selection of predictors in X_s. For any true predictor x_t with t ∈ t ∩ s, it will be asymptotically selected under this criterion if and only if β_{0,t} ≠ 0, where β_{0,t} is the entry of β_0 corresponding to x_t. Let y denote a generic observation of the response variable, let x_t denote a generic observation of the true predictors and let β*_t denote the regression coefficient vector of the true predictors. Since
    β_0 = Σ_s^{−1} Σ_{s,t} β*_t = Σ_s^{−1} cov(x_s, y),    (19)
where Σ_s = var(x_s) and Σ_{s,t} = cov(x_s, x_t), s̃ is determined by the correlation structure of x_s and x_t and the value of the true regression coefficients. However, when t ⊄ s, it is unclear whether β_{0,t} is exactly 0 or not. Following from equation (19), if cov(x_s, y) ≠ 0, then β_0 ≠ 0 and thus at least one predictor in s will be selected according to the marginal inclusion probability criterion. This motivates us to propose an iterative variable selection method for the subset data, provided that the following condition holds.
[p. 958] Condition 5. |cov(x_t, y)| > 0 for any true predictor x_t.
The iterative variable selection method can be described as follows: first select predictors from X_s based on the marginal inclusion probabilities estimated from the posterior π(ξ | D_n^s); denote the set of unselected predictors by X_{s′}, and then select predictors again from X_{s′} based on the marginal inclusion probabilities estimated from the posterior π(ξ | y, X_{s′}); keep running the iterative procedure until no predictors can be selected. Denote all the selected predictors by X_{s̃}. Under assumption 5, this procedure ensures that all true predictors that are contained in X_s will be selected.
There are a few remarks on this iterative procedure.
(a) Other than true predictors, how many other predictors will be selected? Generally speaking, all the predictors that are correlated with X_t will be selected, because they are correlated with y, where X_t denotes the set of all true predictors in D_n. This means that, if all the predictors are linearly correlated, it is futile to apply this iterative procedure, as all the predictors will be selected. The rationale underlying the SAM strategy lies in the belief that, for a big data set, there are only a small proportion of predictors that are linearly correlated with X_t. It is easy to show that if there are p_n predictors correlated with the true predictor X_t, p_n ≺ P_n, then there are at most c p_n predictors to be selected into X_{s̃} for some constant c.
```
Song & Liang (2015), p. 959, §3.1 (SAM steps) and §3.2 (sampler) [SL-SAM; transcribed from p. 959 image]:
```
3.1. Split-and-merge approach
Based on the priors given in Section 2, the SAM approach can be summarized as follows.
(a) Split P_n predictors into K_n groups, s_1, …, s_{K_n}, with max_{i=1,…,K_n} |s_i| ≤ s for a prespecified value of s.
(b) Stage 1: apply the iterative procedure, proposed in Section 2.3, to select predictors from each subset D_n^{s_i} = {y, X_{s_i}}, i = 1, …, K_n, at an FDR level of α_1. At each iteration, the Bayesian variable selection is subject to the prior setting π(σ) ∼ IG(a_0, b_0), π(ξ) = λ_s^{|ξ|}(1 − λ_s)^{|s|−|ξ|} I(|ξ| ≤ s̄) and π(β_ξ | ξ, σ) ∼ N{0, σ²(X_ξ^T X_ξ + τI)/n}, where s̄ denotes the upper bound of the size of the models that are considered for each subset of data. Let s̃_1, …, s̃_{K_n} denote the sets of indices of the selected predictors from the K_n subsets.
(c) Stage 2: merge the sets s̃_1, …, s̃_{K_n} into a single set S̃ = ∪_{i=1}^{K_n} s̃_i, and define p_n = |S̃|. Perform Bayesian variable selection on the subset data D_n^{S̃} = {y, X_{S̃}} at an FDR level of α_2. The Bayesian variable selection is subject to the prior setting π(σ) ∼ IG(a_0, b_0), π(ξ) = (r_n/p_n)^{|ξ|}(1 − r_n/p_n)^{p_n−|ξ|} I(|ξ| ≤ r̄_n) and π(β_ξ | ξ, σ) ∼ N{0, σ²(X_ξ^T X_ξ + τI)/n}.
Clearly, it follows from the theory that was developed in Section 2 that the SAM approach will lead to a consistent selection of true predictors. In step 3, the predictors can also be selected according to the MAP model.
3.2. Simulation and hyperparameter setting
Since different predictors can be highly correlated, the posterior (7) can have a rugged energy landscape for some problems. Conventional MCMC algorithms, such as the Metropolis–Hasting algorithm, tend to become trapped in a local mode in simulations. To avoid this problem, the stochastic approximation Monte Carlo (SAMC) algorithm (Liang et al., 2007) was used in this paper. … Refer to the on-line supplementary material for the details of implementation of this algorithm.
```
**(c) Verdict(s) under test.**
- `core3:B9.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 175–175:
```
  175| **Verdict: comparable to Song–Liang, where the same requirement is an informal remark, not a condition.**
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 74–75, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   74| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 79–79, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   79| | (A4) leakage set \|Q\| ≤ n^b, no leak outside, locality | comparable: informal remark (a), p. 958 |
```

- `core3:B9.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 252–252:
```
  252| | B9 | leakage set \|Q\| ≤ n^b with locality (6) | comparable: informal remark (a), p. 958 | in / in / in / **out** | **out** | in / in / in / **out** |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 65–68:
```
   65| 3. **Leakage size:** bounded for IND, fixed blocks, AR(≤ 0.8), Toeplitz α = 2, S6; growing like n^0.4–0.5 for
   66|    AR(0.95) spread, Toeplitz α = 1 and growing blocks; Q̂ = [p] for factors with a ≥ 0.75, S5 (global factor) and
   67|    riboflavin-like (pre-announced: global CS and strong factors). Weak factors (a = 0.5) move inside by n = 800.
   68|    The width (P9) and local regressions (P6) follow the same split.
```


### core3:A5 — (A5) population floor on O(log n) sets and on Q ∪ {l}
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 682–683:
```
  682| - **(A5) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c>0$ for every $S$ with
  683|   $|S|\le5(A+1)(s_0+1)\log n$ and for every $S=Q\cup\{l\}$, $l\in[p]$.
```

`Theory_work/Wave3/W3-RM/STATEMENT.md` @ e8b5351c, lines 129–134:
```
  129| * **(T1-R) Theorem 1's conditions** = (A1-post) of UNI `STATEMENT.md` §2, i.e. the LSF conditions of APP L1_POST(b)
  130|   [R01-opt]: with j₀ = ⌈(2A + 1)s₀⌉ + 1, m̄_n = ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n]/log(3/2)⌉ and
  131|   k̄_n = min{p, s₀ + max(j₀, m̄_n)}: for a fixed φ > 0, λ_min(Σ_{n,S}) ≥ φ² whenever |S| ≤ min(p, s₀ + j₀), and
  132|   λ_min(Σ_{n,S}) ≥ ψ_n whenever |S| ≤ k̄_n, with ψ_n√n/(log n)^{3/2} → ∞. No upper spectral bound.
  133|   Sufficient: λ_min(Σ_n) ≥ c.
  134| * **(FL-R)** λ_min(Σ_{n,S}) ≥ c for every S with |S| ≤ 16 + s₀, and for S = Q ∪ {l}, l ∈ [p].
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
- `core3:B5.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 101–101:
```
  101| **Verdict: comparable to Song–Liang's Condition 3** — stronger in level, on smaller sets, and for a stronger conclusion.
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 74–75, cells 'Assumption' and 'Song–Liang (2015)' only (first part):
```
   74| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 80–80, cells 'Assumption' and 'Song–Liang (2015)' only (first part):
```
   80| | (A5) population floor on O(log n) sets and on Q ∪ {l} | comparable to Condition 3, p. 955 (first part); none (second part) |
```

- `core3:B10-FL.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 199–200:
```
  199| **Verdict: no Song–Liang counterpart** (it serves the search, which they do not analyse); implied by B5's global floor
  200| plus a locality property of Σ.
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 74–75, cells 'Assumption' and 'Song–Liang (2015)' only (second part):
```
   74| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 80–80, cells 'Assumption' and 'Song–Liang (2015)' only (second part):
```
   80| | (A5) population floor on O(log n) sets and on Q ∪ {l} | comparable to Condition 3, p. 955 (first part); none (second part) |
```

- `core3:A5.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 248–248:
```
  248| | B5 | eigenvalue floor on small sets (1, 2, 6, 10, 9B) | comparable to Condition 3, p. 955: fixed level against vanishing, smaller sets, stronger conclusion | in | **in** | in |
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 253–253:
```
  253| | B10 | floor on Q ∪ {l}, local regressions in Q (6) | no counterpart | in / in / in / n.a. | n.a. | in / in / in / n.a. |
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


### core3:A6 — (A6) local regressions inside Q
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 684–688:
```
  684| - **(A6) Local regressions within $Q$.** There are deterministic sequences $\nu_n=o(\log n)$ and $L_n$, and for every
  685|   $l\in[p]$ a deterministic $N_l\subseteq Q\setminus\{l\}$ with $|N_l|\le\nu_n$ [S1-F3], such that
  686|   $\|\bar\beta_{T,l}-\bar\beta_{T\cap N_l,l}\|_1\le L_n$ for every $T$ with $S_0\subseteq T\subseteq Q$, $l\notin T$,
  687|   where $L_n\to0$ and $L_n^2\log(|Q|+1)=o(\log n)$ (bars: population regression coefficients, zero-padded).
  688| 
```

`Theory_work/Wave3/W3-RM2/STATEMENT.md` @ e8b5351c, lines 159–168:
```
  159|   **(W-loc) Local regressions.** For every l ∈ [p] a deterministic N_l ⊆ Q ∖ {l} with |N_l| ≤ ν_n,
  160|   ν_n log 2 ≤ h log n, and a deterministic L_n ≥ 0 with L_n² log(|Q| + 1) = o(log n), such that
  161| 
  162|     ‖β̄_{T,l} − β̄_{T∩N_l,l}‖₁ ≤ L_n  and  ‖(I − P_{T∩N_l})x_l‖² ≤ (1 + η_n)‖(I − P_T)x_l‖²  for every (T, l) ∈ 𝔓,
  163| 
  164|   with a deterministic η_n → 0 (under (FL-Q) the second inequality follows from the first with η_n = L_n²/φ₀²
  165|   whenever L_n → 0). T ∩ N_l need not contain S₀ and may be empty; β_{T∩N_l,l} is the regression of §1 [SL1-2]. In
  166|   words: the regression of any column on any lattice set is carried, up to a small ℓ¹ coefficient error, by at most
  167|   ν_n ≤ h log n/log 2 lattice members attached to that column, h < ½ − b [SL1-opt2]. (When |Q| has genuine polynomial
  168|   order, |Q| ≥ n^{b′} for a fixed b′ > 0, log(|Q| + 1) ≍ log n and L_n → 0 is required; N_l = ∅ is allowed.)
```

**(b) Song–Liang text.**
(none cited by the audit for this item)
**(c) Verdict(s) under test.**
- `core3:A6.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 199–200:
```
  199| **Verdict: no Song–Liang counterpart** (it serves the search, which they do not analyse); implied by B5's global floor
  200| plus a locality property of Σ.
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 74–75, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   74| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 81–81, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   81| | (A6) local regressions inside Q | none |
```

- `core3:A6.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 253–253:
```
  253| | B10 | floor on Q ∪ {l}, local regressions in Q (6) | no counterpart | in / in / in / n.a. | n.a. | in / in / in / n.a. |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 65–68:
```
   65| 3. **Leakage size:** bounded for IND, fixed blocks, AR(≤ 0.8), Toeplitz α = 2, S6; growing like n^0.4–0.5 for
   66|    AR(0.95) spread, Toeplitz α = 1 and growing blocks; Q̂ = [p] for factors with a ≥ 0.75, S5 (global factor) and
   67|    riboflavin-like (pre-announced: global CS and strong factors). Weak factors (a = 0.5) move inside by n = 800.
   68|    The width (P9) and local regressions (P6) follow the same split.
```


### core3:SCOPE — Core-level verdict for the reported-model theorem
**(a) Our assumption text.**
(core-level verdict; see §1 and the items above)
**(b) Song–Liang text.**
(none cited by the audit for this item)
**(c) Verdict(s) under test.**
- `core3:SCOPE.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 18–20:
```
   18| 2. **The reported-model theorem (core 3)** adds two method-specific conditions with Song–Liang counterparts: visibility
   19|    (stronger than their Condition 5, B8) and a leakage set (their remark (a), p. 958, B9). Inside: S1–S4, S6, IND, AR,
   20|    BLK. Outside: pervasive factors at p ≫ √n (S5, P6, FAC).
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 24–25:
```
   24| | Core theorem | Assumptions against Song–Liang | Our designs inside |
   25| |---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 27–27:
```
   27| | 3 (reported model) | + B8 (stronger than Condition 5), B9 (comparable to remark (a)), B10 (no counterpart) | S1–S4, S6, IND, AR, BLK; not S5, P6, FAC |
```

**(d) Track C evidence.**
(none)

---

## Task (sent as a separate block)

Break the comparison; findings only.

Verdicts to judge (17), in this order; return one machine line for each:
core3:B7.SL
core3:B1.SL
core3:B2.SL
core3:B7.IO
core3:A2.SL
core3:A2.IO
core3:B8.SL
core3:B8.LEMMA
core3:B8.IO
core3:B9.SL
core3:B9.IO
core3:B5.SL
core3:B10-FL.SL
core3:A5.IO
core3:A6.SL
core3:A6.IO
core3:SCOPE.IO

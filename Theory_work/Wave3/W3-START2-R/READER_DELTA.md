# W3-START2-R — READER_DELTA (draft for CP1; RIDER_RULES §5; for HQ → W3-READER)

Source of the current reader text (read only): `/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
§5 "Theorem 5 — The start law already concentrates" (`:267-324`, draft v0.1). Notation, (S1)–(S3): that file `:16-21`
and `NOTATION.md`. Nothing here is written in W3-READER's folder.
READER_VERSIONS row for this delta: **thm5** (manager, CP1 answer). Per the owner's rule, asymptotic statements carry no
n₀ or constants caveats.

## 1. What changes in plain words
1. **Faster start rate when nulls are uncorrelated with the truths (Gaussian rows).** If every null column is
   uncorrelated with every true column, the start puts mass 1 − O_P(√(log n/n)) on the true model. Before: only
   1 − n^{−c} for every c < ½ (equivalently n^{−1/2}e^{C√log n}). The floor is ⅓(n + 1)^{−1/2}, so the new rate is optimal
   up to √log n.
2. **Larger locality sets.** The sets H_l in the no-leakage assumption may have size e^{κ√log n} instead of (log n)^κ.
3. **Fixed design: the visibility level is log n + 2 log p of the actual p, and it is sharp for every p.** Before, the
   level was (1 + 2A) log n with A the exponent of the envelope p ≤ n^A, and the matching necessity statement used
   liminf log p/log n. This matters in a reader statement only if a fixed-design start theorem is shown (§3); for the
   Gaussian-row Theorem 5 it changes one "why" line.

## 2. Theorem 5 — new reader text (replaces `READER_VERSIONS.md:269-299`; changed parts in bold)

**Theorem 5.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$, $\Sigma_n$ a correlation matrix, and let
$y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with a deterministic $\theta^*$ (signal fixed on the standardised
scale). Assume
- **(A1) Model.** (S1), (S2), and $p>s_0$.
- **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on $S_0$.
- **(A3) Small-set floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c$ for every $|S|\le16+s_0$.
- **(A4) Visibility.** For every $j\in S_0$ and every $U\not\ni j$ with $|U|\le15$:
  $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a$, for a fixed $a>0$.
- **(A5) No leakage.** For every $l\notin S_0$ there is a set $H_l\supseteq\{l\}\cup S_0$ with
  **$|H_l|\le e^{\kappa\sqrt{\log n}}$** such that, for every $U\not\ni l$ with $|U|\le15$ and $U_0:=U\cap H_l$:
  $|\operatorname{Cov}(W_l,W_j\mid W_{U_0})|\le Cn^{-1/2}$ for $j\in S_0\setminus U_0$, and
  $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|,|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for $v\in U\setminus H_l$,
  $j\in S_0\setminus U_0$, where $r_n(n\log n)^{1/4}\to0$.

Then for every $c<\tfrac12$,
$$P\big(\pi_0(S_0)\ge1-n^{-c}\big)\to1 .$$
**If moreover (A6) every null column is uncorrelated with every true column, $\operatorname{Cov}(W_l,W_j)=0$ for
$l\notin S_0$, $j\in S_0$, then**
$$\mathbf{1-\pi_0(S_0)=O_P\big(\sqrt{\log n/n}\big)} ,$$
and in all cases $1-\pi_0(S_0)\ge\tfrac13(n+1)^{-1/2}$ for every data set, so the exponent $\tfrac12$ cannot be
improved **and the rate under (A6) is optimal up to the factor $\sqrt{\log n}$**.

*With leakage (remark).* Unchanged (`:291-294`), with $|H_l|\le e^{\kappa\sqrt{\log n}}$ in (A5).

### Why each assumption (changed lines only)
- (A4) "The level is sharp in the fixed-design analogue **(threshold $\log n+2\log p$ for every $p$)**; masked truths
  violate it and are treated separately."
- (A5) add: "**The size bound on $H_l$ only counts reference sets in a union bound; it is not known to be needed.**"
- **(A6) The start odds are, to first order, a sum over null columns of block Bayes factors computed given subsets of
  the truth. Uncorrelated nulls make each expected factor of order $\sqrt{\log n}$; under (A5) alone a small correlation
  $Cn^{-1/2}$ shifts the Gaussian score and costs a factor $e^{O(\sqrt{\log n})}$. It suffices that these correlations be
  at most $C/\sqrt{n\log n}$ given every proper subset of the truth (master statement). Not known to be necessary.**

### Master theorem and bridges
Master: `W3-START2-R:START-R` (STATEMENT v1.5 §3.2 (T3⁺⁺)(b)(i), (iii)) with `W3-START:FLOOR` for the floor. Status:
none yet (target at CP1); the reader text may go to the card only after CP3 and acceptance.
| # | bridge | mark | detail |
|---|---|---|---|
| B5.1′ | (A3)–(A5) = (FL-R16), (V-R), (L-R⁺⁺) with Q = S₀, H̄_n = e^{κ√log n} (κ_H = κ) | identity | STATEMENT (D4) |
| B5.3 (new) | (A6) ⇒ (L-gain-0) with C₀ = 0 | NEW, 2 lines | Schur complement: for U ⊆ S₀, Cov(W_l, W_j \| W_U) = Σ_{lj} − Σ_{lU}Σ_{UU}⁻¹Σ_{Uj} = 0; STATEMENT (D5) |
| B5.2 | floor | EXISTS-CHECKED | unchanged |

## 3. Fixed-design start — proposed reader version (W3-READER has none; optional, for HQ to decide)

**Theorem 5F (fixed design).** Let $X$ be a deterministic standardised design and $y=\alpha\mathbf 1+X\theta^*+\varepsilon$
under (S1), (S2), $p>s_0$. For a set $U$ of columns let $\delta^2_{U,k}$ be the part of the squared length of the mean
$\mu=X\theta^*$ that column $k$ explains after the columns of $U$ (the drop in $\|(I-P_U)\mu\|^2$ when $k$ joins $U$),
and $\tau_U^2:=\sigma^2+\|(I-P_U)\mu\|^2/(n-1)$. Assume
- (F1) $s_0$ fixed and $\|\mu\|^2\le Mn$;
- (F2) $\lambda_{\min}(X_T^\top X_T)\ge g>0$ for every set $T$ of at most 16 columns;
- (F3) *visibility:* $\delta^2_{U,j}\ge\tau_U^2\,(c\log n+2\log p)$ for every truth $j$ and every $U\not\ni j$ with
  $|U|\le15$, for a fixed $c>1$;
- (F4) *bounded null gains:* $\delta^2_{U,l}\le C_0\tau_U^2$ for every null $l$ and every $|U|\le15$.

Then for every $\kappa<(c-1)/2$, with probability tending to one,
$$1-\pi_0(S_0)\le n^{-1/2}e^{C\sqrt{\log n}}+n^{-\kappa},$$
and if no null explains anything ($\delta_{U,l}=0$ in (F4)), $1-\pi_0(S_0)=O_P(\sqrt{\log n/n})+o_P(n^{-\kappa})$.
Conversely, if one truth has $\delta^2_{V,j}\le\tau_V^2(c'\log n+2\log p)$ with $c'<1$ for every set $V$ of at most 15
other truths, then $\pi_0(S_0)\to0$ in probability: **the constant 1 in (F3) is sharp, for every sequence $p\le n^A$.**

Master: `W3-START2-R:F3` and `:F1` (η = 0) with Q = S₀, via (T1⁺⁺); converse `W3-START2-R:NEC` (N3⁺⁺). Bridges: (F1),
(F2) = (E), (GF-16) (identity); (F3) = (V-cp) (identity); (F4) = the hypothesis of F3⁺⁺ (identity), and F3⁺⁺'s growth
premise holds at Q = S₀. All marked NEW-TARGET until CP3.

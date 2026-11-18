# W3-START2-R — READER_DELTA v-next (post-CP3; RIDER_RULES §5; for W3-READER, applied after the recording)

Source of the current reader text (read only): `/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
§5 "Theorem 5 — The start law already concentrates", block `<!-- ROW thm5 BEGIN -->` … `<!-- ROW thm5 END -->`
(`:549-612`), **section version 0.2** at W3-READER HEAD 6a07d34c (it carries the S1 restriction [S1-F4] of the floor
clause). Notation, (S1)–(S3): that file `:26-28` and `NOTATION.md`. Nothing here is written in W3-READER's folder.
Changes from the CP3 version of this file (`READER_DELTA.md`, frozen in MANIFEST_R2): (i) §1 item 1 no longer says
"equivalently" (council R1 sol finding; ERRATA #1); (ii) §2 is now a complete replacement of the thm5 block, merged onto
section version 0.2, so the floor clause keeps the [S1-F4] restriction (ERRATA #2); (iii) the master record points to the
recorded ids. No mathematics changes.
READER_VERSIONS row for this delta: **thm5** (manager, CP1 answer). Per the owner's rule, asymptotic statements carry no
n₀ or constants caveats.

## 1. What changes in plain words
1. **Faster start rate when nulls are uncorrelated with the truths (Gaussian rows).** If every null column is
   uncorrelated with every true column, the start puts mass 1 − O_P(√(log n/n)) on the true model. Before: only
   1 − n^{−c} for every c < ½ (from the explicit parent envelope n^{−1/2}e^{C√log n}, which implies it). The floor is ⅓(n + 1)^{−1/2}, so the new rate is optimal
   up to √log n.
2. **Larger locality sets.** The sets H_l in the no-leakage assumption may have size e^{κ√log n} instead of (log n)^κ.
3. **Fixed design: the visibility level is log n + 2 log p of the actual p, and it is sharp for every p.** Before, the
   level was (1 + 2A) log n with A the exponent of the envelope p ≤ n^A, and the matching necessity statement used
   liminf log p/log n. This matters in a reader statement only if a fixed-design start theorem is shown (§3); for the
   Gaussian-row Theorem 5 it changes one "why" line.

## 2. Theorem 5 — replacement for the thm5 block of READER_VERSIONS (section version 0.2 → 0.3)

Replace everything between `<!-- ROW thm5 BEGIN -->` and `<!-- ROW thm5 END -->` (exclusive) by the text below. Changed
parts against section version 0.2 are in bold.

```markdown
**Card row** 3.3 · **Section version** 0.3 (2026-11-16)


### Reader statement
**Theorem 5.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$, $\Sigma_n$ a correlation matrix, and let
$y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with a deterministic $\theta^*$ (signal fixed on the standardised
scale). Assume
- **(A1) Model.** (S1), (S2), and $p>s_0$.
- **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  $S_0$.
- **(A3) Small-set floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c$ for every $|S|\le16+s_0$.
- **(A4) Visibility.** For every $j\in S_0$ and every $U\not\ni j$ with $|U|\le15$:
  $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a$, for a fixed $a>0$.
- **(A5) No leakage.** For every $l\notin S_0$ there is a set $H_l\supseteq\{l\}\cup S_0$ with
  **$|H_l|\le e^{\kappa\sqrt{\log n}}$** such that, for every $U\not\ni l$ with $|U|\le15$ and $U_0:=U\cap H_l$:
  $|\operatorname{Cov}(W_l,W_j\mid W_{U_0})|\le Cn^{-1/2}$ for $j\in S_0\setminus U_0$, and
  $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|,|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for $v\in U\setminus H_l$,
  $j\in S_0\setminus U_0$, where $r_n(n\log n)^{1/4}\to0$.

Then for every $c<\tfrac12$,
$$
P\big(\pi_0(S_0)\ge1-n^{-c}\big)\to1 .
$$
**If moreover (A6) every null column is uncorrelated with every true column, $\operatorname{Cov}(W_l,W_j)=0$ for
$l\notin S_0$, $j\in S_0$, then**
$$
\mathbf{1-\pi_0(S_0)=O_P\big(\sqrt{\log n/n}\big)} .
$$
The exponent $\tfrac12$ cannot be improved: $1-\pi_0(S_0)\ge\tfrac13(n+1)^{-1/2}$ for every valid data set with
$n\ge4$ and $s_0<K$ (hence for all large $n$) [S1-F4]; **so the rate under (A6) is optimal up to the factor
$\sqrt{\log n}$.**

*With leakage (remark or second display).* If (A5) holds with $S_0$ replaced by a deterministic $Q\supseteq S_0$,
$|Q|\le K$ (columns outside $Q$ do not leak), then
$P\big(\pi_0(\mathcal L(Q))\ge1-(|Q|+1)n^{-1/2}e^{C\sqrt{\log n}}\big)\to1$; for $|Q|\le n^{1/2-\epsilon}$ this is
$\ge1-n^{-c}$ for every $c<\epsilon$.

### Why each assumption
- (A3) Block regressions of at most 16 columns are well posed. Necessity open.
- (A4) Each truth, alone, improves the fit of every small model it is missing from: then the start law, which only sees
  within-block interactions, still ranks $S_0$ first. The level is sharp in the fixed-design analogue **(threshold
  $\log n+2\log p$ for every $p$)**; masked truths violate it and are treated separately.
- (A5) Nulls must not imitate truths within the start law's block view; the partial-covariance level $n^{-1/2}$ is a
  proof threshold (numerics show no cliff there); localisation is needed because the blocks are data-dependent.
  **The size bound on $H_l$ only counts reference sets in a union bound; it is not known to be needed.**
- **(A6) The start odds are, to first order, a sum over null columns of block Bayes factors computed given subsets of
  the truth. With uncorrelated nulls the proof bounds the expectation of a truncated envelope of these factors by
  $O(\sqrt{\log n})$ (an upper bound), and averaging over the columns and Markov's inequality give the displayed rate;
  under (A5) alone a correlation of size $Cn^{-1/2}$ shifts the Gaussian score, and the same upper bound then carries a
  factor $e^{O(\sqrt{\log n})}$. It suffices that these correlations be at most $C/\sqrt{n\log n}$ given every proper
  subset of the truth (master statement). Not known to be necessary.**
- The exponent $\tfrac12$ is optimal (deterministic floor).

### Master theorem
**`W3-START2-R:START-R`, `Theory_work/Wave3/W3-START2-R/STATEMENT.md:226-240` (clauses (i), (iii); (L-R⁺⁺) at :70-81,
(L-gain-0) at :82-87; (FL-R16), (V-R) at `W3-START/STATEMENT.md:160-162`), status as recorded at acceptance (HQ quotes it
verbatim on recording). Bridge (B-R⁺⁺): `W3-START2-R:BR` (`W3-START2-R/STATEMENT.md:217-225`), same.** Floor:
`W3-START:FLOOR@1.0.0` (`W3-START/STATEMENT.md:241-243`), **"PROVED-CHECKED"**.

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| **B5.1′** | **(A3)–(A5) = (FL-R16), (V-R), (L-R⁺⁺) with $Q=S_0$, $\bar H_n=e^{\kappa\sqrt{\log n}}$ ($\kappa_H=\kappa$)** | identity | **word for word (`W3-START2-R/STATEMENT.md:70-81`).** |
| B5.2 | floor $\tfrac13(n+1)^{-1/2}$ | EXISTS-CHECKED | (T0) holds for valid data with $n\ge4$ and $|S|<K$; with $S=S_0$ this is all large $n$ since $p>s_0$ (statement restricted accordingly [S1-F4]). |
| **B5.3** | **(A6) ⇒ (L-gain-0) with $C_0=0$** | **checked with the master (council R1/R2 of W3-START2-R)** | **for $U\subseteq S_0$: $\operatorname{Cov}(W_l,W_j\mid W_U)=\Sigma_{lj}-\Sigma_{lU}\Sigma_{UU}^{-1}\Sigma_{Uj}=0$ (`W3-START2-R/STATEMENT.md:82-87`).** |

### Honest limits
The statement is in population terms but (A5) is long. Two presentation options for HQ: (i) state the theorem with
$Q=S_0$ only (as above) and move the leakage form to a remark; (ii) a shorter sufficient condition (e.g. exact conditional uncorrelatedness of nulls and truths) does **not**
immediately give the localisation clause, because that clause also constrains columns outside $H_l$; no such
simplification is proposed without a proof. Recommendation: option (i). **(A6) is an additional hypothesis for the
sharper rate only; it does not replace (A5).**
Also: this theorem is about an internal object of the method; it belongs in the paper's method section, not in the
abstract.

#### Update log (thm5)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes [S1-F4] floor restricted to n≥4, s₀<K (WEAKER clause, now faithful).
- **v0.3 2026-11-16: rider START2 v1.5 (W3-START2-R, CP3 accepted; H5 card 14 AGREED, row 3.3 STRONGER): (A5) with
  $|H_l|\le e^{\kappa\sqrt{\log n}}$; new (A6) with the rate $O_P(\sqrt{\log n/n})$; "why" lines for (A4)–(A6); master
  W3-START2-R:START-R/BR.**
```

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

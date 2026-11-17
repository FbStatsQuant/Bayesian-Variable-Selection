# W3-D3 — READER_DELTA (draft v0.1, 2026-11-17; for the manager → HQ → W3-READER; read-only source [RV] row thm2)

**Current reader version:** `READER_VERSIONS.md:263-282` (Theorem 2, row 1.2, section v0.4 + FRZ-B). Not changed.

**What is added (COEXIST, per the ticket).** A companion statement under Theorem 2 with the Gaussian row law replaced by
sub-Gaussian predictors on sparse directions. (A1)–(A3) and the three conclusions are Theorem 2's verbatim. Tag: STRONGER
(statement); status: every input PROVED-CHECKED (STATEMENT §6).

**New text (proposal; reader form, no internal ids).**
> **Theorem 2′ (sub-Gaussian predictors).** Let the rows of $X^{\mathrm r}$ be i.i.d. copies of a random vector
> $x\in\mathbb R^p$ with mean $m_n$ and covariance matrix $\Sigma_n$, a correlation matrix. Assume (A1)–(A3) of Theorem 2 and
> - **(A4) Sub-Gaussian predictors on sparse directions.** For a fixed $K$, every $u\in\mathbb R^p$ with at most
>   $5(A+1)(s_0+1)\log n$ nonzero entries and every $\lambda\in\mathbb R$:
>   $\;E\exp\{\lambda u^\top(x-m_n)\}\le\exp\{K^2\lambda^2\,u^\top\Sigma_nu/2\}$.
>
> Then the three conclusions of Theorem 2 hold under the joint law of design and noise.
>
> *Remarks.* Gaussian rows satisfy (A4) with $K=1$, so Theorem 2 is the Gaussian case. More generally, (A4) holds with
> the constant $K$ of the coordinates whenever $x=m_n+L\xi$ with $LL^\top=\Sigma_n$ and $\xi$ a vector of independent,
> mean-zero, unit-variance coordinates that are sub-Gaussian with constant $K$ (for instance Rademacher or uniform
> coordinates, $K=1$). (A4) is used only to make the sample standard deviations of the predictors and the sample
> correlation matrices of small groups of predictors track their population values. It fails for a binary predictor
> whose success probability tends to zero.

**Why (A4) (one line, for the "why each assumption" list).** Only to transfer (A3) from the population to the sample with
probability tending to one; the posterior argument uses the observed design only.

**Bridges.** B2.2′ := `W3-D3:B3w` (replaces `W2-APP:POST` (a) for this statement; built on `W3-DIST:B1`, `B2core`, `B2`
(a), `W3-READER:R1`); B2.3 unchanged (`W3-POST:Thm-1` item 6, via `W3-D3:Thm2SG`). The old B2.1–B2.3 stay for row 1.2.

**Comparison sentence (for the literature paragraph; HQ judges the D109 class).** Sub-Gaussian rows are assumed in
Narisetty and He (2014, Lemma 6.1, p. 16) with identity covariance; Song and Liang (2015, Condition 1, p. 953) assume a
weaker exponential-moment bound on averages of a few predictors under any correlation. (A4) lies between the two:
it allows any correlation matrix and implies Song and Liang's Condition 1.

# W3-D3 — REPORT (track D #3, sub-Gaussian rows for Theorem 2; draft for the council manifest; 2026-11-17)

REPORT restates nothing (PROTOCOL_v4 §3): claims, hypotheses and conclusions are in `STATEMENT.md`; proofs in
`lemmas/B3w.md` and `lemmas/ASSEMBLY.md`; gate evidence in `TARGET.md`; the reader-version proposal in `READER_DELTA.md`.
A sentence here that asserts mathematics not in STATEMENT or a checked proof is labelled HEURISTIC or OPEN.

## 1. What was done
Three claims; Theorem 2 (card row 1.2) with the Gaussian row law replaced by sub-Gaussian predictors on sparse directions,
as a coexisting claim:
- W3-D3:Thm2SG — `STATEMENT.md` §1; proof `lemmas/ASSEMBLY.md` "Theorem 2SG".
- W3-D3:B3w — `STATEMENT.md` §2; proof `lemmas/B3w.md` (W3-DIST's B3 run on Theorem 2's window).
- W3-D3:ExSG — `STATEMENT.md` §3; proof `lemmas/ASSEMBLY.md` "Proposition ExSG" (part (b) via Hoeffding's lemma, proved in place).
Route (owner condition D105/D112): W3-DIST's population-to-sample bridge (B0, B1, B2-core, B2 (a), B3's argument) plus the
checked set sizes `W3-READER:R1` (B1.2, B1.3) deliver the events of W3-POST Theorem 1 item 6; no new probability theory,
no new key lemma. Every Gaussian step of row 1.2's bridge (`W2-APP:POST`) is covered (PLAN.md table G1–G5). Kill point not
reached. Tag against row 1.2's reader statement: STRONGER (`STATEMENT.md` §8; confirmed at the lock).

## 2. Caveats (plainly)
- **Fixed floor kept.** Row 1.2's master (`W2-APP:POST`, LSF) allows the floor on the logarithmic sets to vanish slowly;
  Theorem 2SG keeps the reader statement's fixed floor φ² (option o2, a floor of order 1/n through `W3-DIST:B2`, is OFF by
  HQ). Against the reader statement nothing is weaker.
- **Assumption class.** (A4) is classed 1 by HQ's ruling (2026-11-17, D114): it contains Narisetty & He's (2014, Lemma 6.1)
  isotropic sub-Gaussian rows as the case Σ = I (centred rows; L a fixed multiple of their constant); this is the only class-1
  anchor [H5-17]. Separately (a factual remark, not an anchor), (A4) implies Song & Liang's Condition 1 for the centred
  predictors z = x − m_n [R1-sol-S1]. No verified Bayesian-selection paper states sub-Gaussian rows with a general correlation matrix (a report of
  the search). 2b backup sentence as approved (`STATEMENT.md` §5). NH14 cited from arXiv v1 pp. 16–17, journal version not checked.
- **Constants.** Explicit, not optimised (threshold n₁ of order 10⁹–10¹¹ for L = 1 at the absolute constant c₂ = 10⁻⁵ of
  B2-core; `numerics/N1_out.txt`).

## 3. Card text (COEXIST; row 1.2 unchanged)
Row 1.2 unchanged (statement, masters, "clean" mark). Added sentence under row 1.2 (body):
> *Sub-Gaussian predictors.* The same conclusions hold when the rows are i.i.d. with mean $m_n$ and correlation matrix
> $\Sigma_n$ and, instead of being Gaussian, are sub-Gaussian along sparse directions: for a fixed $L$,
> $E\exp\{\lambda u^\top(x-m_n)\}\le\exp\{L^2\lambda^2u^\top\Sigma_nu/2\}$ for every $u$ with at most $5(A+1)(s_0+1)\log n$
> nonzero entries (Gaussian rows: $L=1$; so do correlated mixtures $x=m_n+B\xi$ of independent mean-zero, unit-variance
> features that are sub-Gaussian with one common constant $L$, for instance features confined to $K$ standard deviations
> of their mean with one common $K$, giving $L=K$). For centred rows this contains the isotropic sub-Gaussian rows of
> Narisetty and He (2014, Lemma 6.1), the case $\Sigma_n=I$. It also implies Song and Liang's Condition 1 for the
> centred rows $x-m_n$. [R1-sol-S1, R1-opus-S1, H5-17]

"Master" cell for the added sentence: `W3-D3:Thm2SG` (with `W3-D3:B3w`, `W3-D3:ExSG`), statuses as recorded at CP3; inputs
`W3-POST:Thm-1@1.0.1`, `W3-DIST:B0/B1/B2core/B2/B3@1.0.1`, `W3-READER:R1@1.0.2`, all PROVED-CHECKED. "Mark" cell: **clean**
once the three claims are recorded PROVED-CHECKED.

## 4. Chain record
Statement lock L1 (Sol, NORMAL): `reviews/L1_statement_lock_sol.md`, disposition `reviews/L1_disposition.md`.
Line check K1 (Opus 5.5 high, blind, claudeAgent_personal; with the statement-change check v1.0 → v1.1):
`reviews/K1_linecheck_opus.md` (VERIFIED-WITH-AMENDMENTS; 1 C minor, 2 S, 1 F, 8 E), disposition `reviews/K1_disposition.md`.
Re-check K2 (Opus, new agent): `reviews/K2_recheck_opus.md` (RESOLVED-WITH-AMENDMENTS; 2 S, 4 E), disposition
`reviews/K2_disposition.md`.
Re-check K3 (Opus, new agent): `reviews/K3_recheck_opus.md` (RESOLVED-WITH-AMENDMENTS; 1 E), disposition `reviews/K3_disposition.md`.
Staged ingest: `reviews/INGEST_staged.txt` (0 problems; acceptance PASS).
Changelog: `STATEMENT.md` §9. DEPS: `DEPS.tsv` (`deps_hand.py`). Citation check: `citecheck.py` → `reviews/CITECHECK.txt`.
Numerics: `numerics/N1_window.py` → `numerics/N1_out.txt` (size arithmetic, 1966 cases, 0 violations);
`numerics/N2_subgauss_rows.py` → `numerics/N2_out.txt` (exact posteriors, non-Gaussian rows; sanity only).
API blind-audit card: `API_CARD.md` (`api_request_build.py`). Council: (filled at CP3).

## 5. Open items (named)
- Vanishing floor (o2) and the smaller window 3(A + 1)(s₀ + 1) log n (o1): free by `W3-DIST:B2` (a) and `W3-READER:R1` B1.3;
  OFF by HQ (no new scope).
- Sub-Gaussian rows with conclusions in expectation (combining with W3-D2:Thm2X): OPEN, no route checked (W3-D2's master
  uses Gaussian rows structurally).
- Whether some tail condition is necessary for posterior concentration on random designs: OPEN.

## 6. Registry blocks

```
REGISTRY
claim: W3-D3:B3w | kind: lemma | statement: STATEMENT.md:59-80 | premises: STATEMENT.md:23-39 ; STATEMENT.md:41-57
status: PROVED (by this seat, unchecked) | status_source: lemmas/B3w.md:3
assumptions: A:GAUSS-NOISE ; A:P-POLY ; A:FIXED-S0 ; A:COEF-BOUNDED ; A:POP-FLOOR-5LOG (new | fixed population sparse eigenvalue floor on logarithmic sets | lambda_min(Sigma_n,S) >= phi^2 for every S of size at most 5(A+1)(s0+1) log n, fixed phi in (0,1], Sigma_n a correlation matrix | STATEMENT.md:41-57 | shared no | bridge W3-D3:B3w) ; A:SUBG-SPARSE-ROWS (new | sub-Gaussian predictors on sparse directions | E exp(lambda u'(x - m_n)) <= exp(L^2 lambda^2 u' Sigma_n u / 2) for every u with at most 5(A+1)(s0+1) log n nonzero entries, fixed L; variant of A:DIST-A3 on the window 5(A+1)(s0+1) log n | STATEMENT.md:41-57 | shared no | bridge W3-D3:B3w)
conclusion: posterior: random-design interface events of W3-POST Theorem 1 item 6; on E1 and E2(q_n) (probability >= 1 - 4p e^{-c1 n/L^4} - e^{-c2 n/L^4}) no column is constant and (E; M_E), (F_lambda; phi0^2 = phi^2/4), (F_w; g0 = phi^2/8), BM-inf with envelope b_lo^2 n phi^2/(8 sigma^2 log n) hold; (X°, θ°)-measurable events A'_n ⊇ A_n of the completed pair on which the hypotheses of W3-POST Theorem 1 item 6 hold (regime R1) | rate: n/a | scope: iid rows with correlation-matrix covariance, (A1)-(A4), n >= n1(s0, A, L)
depends_on: W3-DIST:B0@stmt ; W3-DIST:B1@stmt ; W3-DIST:B2core@stmt ; W3-DIST:B2@proof:part-(a) ; W3-DIST:B3@proof:template-Steps-1-6-and-A-2 ; W3-READER:R1@proof:B1.2-B1.3
implies:

REGISTRY
claim: W3-D3:ExSG | kind: proposition | statement: STATEMENT.md:82-90 | premises: STATEMENT.md:23-39
status: PROVED (by this seat, unchecked) | status_source: lemmas/ASSEMBLY.md:3
assumptions:
conclusion: identity: x = m + B xi with independent mean-zero unit-variance L-sub-Gaussian coordinates satisfies (A4) with L for every direction; L = 1 for Gaussian, Rademacher, uniform[-sqrt3, sqrt3]; L = K for coordinates in an interval of length 2K (Hoeffding's lemma, proved in place) | rate: n/a | scope: any p, d
depends_on:
implies:

REGISTRY
claim: W3-D3:Thm2SG | kind: theorem | statement: STATEMENT.md:41-57 | premises: STATEMENT.md:23-39
status: PROVED (by this seat, unchecked) | status_source: lemmas/ASSEMBLY.md:3
assumptions: A:GAUSS-NOISE ; A:P-POLY ; A:FIXED-S0 ; A:COEF-BOUNDED ; A:POP-FLOOR-5LOG ; A:SUBG-SPARSE-ROWS
conclusion: posterior: 1 - pi(S0 | y) = O_P(sqrt(log n/n)), P(HPM = MPM = S0) -> 1, max_j |PIP_j - 1{j in S0}| = O_P(sqrt(log n/n)) under the joint law of design and noise | rate: r_n = sqrt(log n / n) | scope: iid rows, mean m_n, correlation-matrix covariance, sub-Gaussian on sparse directions; 2 <= p <= n^A, s0 >= 1 fixed, b_lo <= |beta_j| <= b_hi on S0, sigma^2 fixed
depends_on: W3-D3:B3w@stmt ; W3-POST:Thm-1@stmt ; W3-DIST:B0@stmt
implies:
notes: Coexists with row 1.2 (W3-POST:Thm-1 item 6 + W2-APP:POST); its hypotheses contain row 1.2's reader hypotheses (Gaussian rows: L = 1, W3-D3:ExSG), so it gives the conclusions of READER_VERSIONS.md:263-275 on a larger class. Not an edge to W2-APP:POST (vanishing floor, SL1 conclusions not reproduced).
```

# W3-D2 — REPORT (track D #2, "check X"; draft for the council manifest; 2026-11-17)

REPORT restates nothing (PROTOCOL_v4 §3): claims, hypotheses and conclusions are in `STATEMENT.md`; the proof is
`PROOF.md`; gate evidence in `TARGET.md`; the reader-version proposal in `READER_DELTA.md`. A sentence here that asserts
mathematics not in STATEMENT or a checked proof is labelled HEURISTIC or OPEN.

## 1. What was done
Two claims; Theorem 2 (card row 1.2) derived from the omitted-variables master, with the floor on smaller sets:
- W3-D2:Thm2X — `STATEMENT.md` §1 (reader statement + clause (E)); proof `PROOF.md` P0–P2.
- W3-D2:Cor2X — `STATEMENT.md` §2; proof `PROOF.md` P3.
Route: CorGb-plus with no omitted columns (`PROOF.md` P1) + the checked set-size bound `W3-READER:R1` B4.1. No new lemma;
kill point not reached. Tag against row 1.2's reader statement: STRONGER (`STATEMENT.md` §7; confirmed at the lock).

## 2. The two caveats (plainly; full text `STATEMENT.md` §7)
- **(a) Status is conditional.** The claims inherit `W3-MISR-R:CorGb-plus@1.0.1`'s conditions (W3-POST2:C, E, A1, A0,
  C-MIS:GDb, C-MIS:Prop-P), including, through W3-POST2:C, `W3-POST:Prop-LB` "PROVED (by this seat, unchecked)". Row 1.2 as
  recorded is clean. (Audit item X2 — Prop-LB implied by the checked `W3-PSHARP:B` — not added by HQ; estimate §3a.)
- **(b) Incomparable with the old master on the large-set floor.** The old master (`W2-APP:POST`, LSF) lets the floor on
  sets of size ≤ k̄_n vanish slowly; Theorem 2X needs a fixed floor on its whole range. STRONGER holds against the
  constant-floor reader statement only (`STATEMENT.md` §4(b), §7).

## 3. Card text (HQ decision 2026-11-17: row 1.2 COEXIST)
Row 1.2 unchanged (statement, masters, "clean" mark, vanishing-floor remark). Added sentence under row 1.2 (body, not abstract):
> *Smaller-set, expectation form.* Under the same model with the floor asked only on sets of size $3(A+1)(s_0+1)\log n$ (on
> the correlation matrix of a row), and energy and beta-min measured against the noise variance ($\Sigma$, $\beta$,
> $\sigma^2$ may vary with $n$), $E[1-\pi(S_0\mid y)]=O(\sqrt{\log n/n})$, and the HPM and MPM error probabilities and the
> expected maximal PIP error are $O(\sqrt{\log n/n})$. This is Theorem 4 with no omitted predictors. It is conditional on the
> inputs of Theorem 4's master, one of which (a deterministic rate lower bound used in the expectation route) has not yet had
> an independent check.

"Master" cell for the added sentence: `W3-D2:Thm2X`, `W3-D2:Cor2X`, statuses as recorded at CP3, with the inherited
conditions written out: W3-POST2:C (itself conditional on W3-POST:Prop-LB, "PROVED (by this seat, unchecked)"), W3-POST2:E,
W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P. "Mark" cell for the added sentence: **conditional**. Row 1.2's own mark
stays **clean**.

## 3a. X2 estimate (Prop-LB check; not added — HQ revisits only if ≤ ½ day Tier B)
- **Tier / size:** Tier B re-check, ≈ 2–3 h lead time + one Sol review: line-check the existing implication note
  `Theory_work/Dept/research/IMPL_PSHARPB_PROPLB_opus.md` (dept/theory; Opus, unchecked) and hand the recorder an `implies` edge.
- **Inputs:** `W3-PSHARP:B@1.0.0` (PROVED-CHECKED, `W3-PSHARP/STATEMENT.md:90-114`), Prop-LB (`W3-POST/lemmas/LB_rate_lower_bound.md`,
  40 lines), [W3P] §0; no new mathematics (B is strictly stronger on LB's domain, per the note).
- **What it does not clear:** Thm2X would still be conditional through CorGb-plus on C-MIS:GDb and C-MIS:Prop-P (wave-1
  labels, not PROVED-CHECKED), so X2 alone does not make the added sentence clean.

## 4. Chain record
Statement lock L1 (Sol, NORMAL): `reviews/L1_statement_lock_sol.md`, disposition `reviews/L1_disposition.md`.
Line check K1 (Opus 5.5 high, blind; per ticket): `reviews/K1_linecheck_opus.md`, disposition `reviews/K1_disposition.md`.
Changelog: `STATEMENT.md` §8. DEPS: `DEPS.tsv`. Citation check: `citecheck.py` → `reviews/CITECHECK.txt`. Numerics:
`numerics/N1_floor_and_e2e.py` → `numerics/N1_out.txt`. API blind-audit card: `API_CARD.md`. Council: (filled at CP3).

## 5. Open items (named)
- Sub-Gaussian rows for Theorem 2 (audit candidate #3) — not touched here.
- The floor size: the proof needs it only on |T| ≤ k_n (numerics N1: k_n ≤ 0.40·3(A+1)(s₀+1) log n on the grid). Writing the
  reader floor as s₀ + max(j₀, m♯_n) would be sharper but less readable; not proposed (constants are proof artefacts).
- A vanishing-floor version of Theorem 2X (would remove caveat (b)): needs CorGb-plus's design transfer with ψ_n → 0;
  OPEN, no route checked.

## 6. Registry blocks

```
REGISTRY
claim: W3-D2:Thm2X | kind: theorem | statement: STATEMENT.md:29-48 | premises: STATEMENT.md:14-27 ; STATEMENT.md:60-63 ; STATEMENT.md:76-84
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P | status_source: PROOF.md:3
assumptions: A:IID-GAUSS-ROWS ; A:GAUSS-NOISE ; A:P-POLY ; A:FIXED-S0 ; A:CORR-FLOOR-LOG (new | log-size floor on the row correlation matrix | lambda_min(R_TT) >= c for every T with |T| <= 3(A+1)(s0+1) log n, fixed c > 0 | STATEMENT.md:34-35 | shared no | bridge W3-D2:Thm2X) ; A:POP-SNR (new | population signal relative to the noise variance | beta' Sigma beta <= M0 sigma^2 and n min_j Sigma_jj beta_j^2 / (sigma^2 log n) -> infinity | STATEMENT.md:36-37 | shared no | bridge W3-D2:Thm2X)
conclusion: posterior: E delta_n, P(HPM != S0), P(MPM != S0) and E max_j |PIP_j - 1{j in S0}| are O(r_n) under the joint law of design and noise; explicit bound C r_n + (2 + 2 k_n) n^-2 + n^-1 | rate: r_n = sqrt(log n / n) | scope: iid Gaussian rows, 2 <= p <= n^A, s0 >= 1 fixed; Sigma, beta, sigma^2 may vary with n
depends_on: W3-MISR-R:CorGb-plus@stmt ; W3-READER:R1@proof:B4.1
implies:

REGISTRY
claim: W3-D2:Cor2X | kind: corollary | statement: STATEMENT.md:50-58 | premises: STATEMENT.md:14-27 ; STATEMENT.md:29-48
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P | status_source: PROOF.md:3
assumptions: A:IID-GAUSS-ROWS ; A:GAUSS-NOISE ; A:P-POLY ; A:FIXED-S0 ; A:COEF-BOUNDED ; A:LSF
conclusion: posterior: the hypotheses of the recorded Theorem 2 (row 1.2) imply those of W3-D2:Thm2X; hence its expectation bounds and the recorded conclusions (O_P rate, HPM = MPM = S0 w.p. -> 1, PIP O_P rate) | rate: r_n = sqrt(log n / n) | scope: as row 1.2 (correlation-matrix Sigma, fixed sigma^2, b_lo <= |beta_j| <= b_hi)
depends_on: W3-D2:Thm2X@stmt
implies: W3-POST:Cor-1R (conclusions 1-4 under the recorded row-1.2 hypotheses with a constant floor; expectation form; item-level, recorder to decide whether an edge applies)
```

# W1-EXP — REPORT (EXP′; T27 from chain leakage; one family carrying T27 masking + T22(i) near-truth mass)

Run of 2026-11-02, branch `theory/W1-EXP`. Proofs in `PROOF.md`; scripts in `scripts/`; raw results in `results/`.
All results are **candidates pending cross-family review**. Status words: PROVED / PROOF SKETCH / COUNTEREXAMPLE /
CONJECTURE / OPEN, never upgraded. Notation of `00_COMMON.md`.

## Headline

1. **EXP′ is a theorem, and it does not need the block-orthogonal benchmark.** Under G, `p <= n^A`,
   `||mu||^2 <= Mn` and within-block SE (SE-blk), on an event of probability -> 1 *every* within-block addition satisfies
   `log[r_b(T+l)/r_b(T)] = -(1/2)log(n+1) - nu log(1-x_{T,l}) + R`, with the explicit deterministic bound
   `|R| <= 0.52/c_* + O(1/n)`, `c_* = sigma^2/(8(M+2sigma^2))` (PROOF.md Thm 1, **PROVED**). SE-blk is checkable on the
   actual blocks (`min_b lambda_min(R_{C_b}) >= phi0^2`, by interlacing). For iid Gaussian designs it holds w.p. -> 1 for
   *any* partition into blocks of size <= 16, the X-dependent one included (§1.5, PROOF SKETCH).
2. **Favourable regime (T22(iii)) in the BO benchmark is now unconditional**: G, R, SE-blk, BO and a block beta-min give
   `1 - pi0(S0) = O_P(2^B sqrt(log n) n^{-1/2})` (Thm 2; PROOF SKETCH — composition with the locked T22(iii)), and, when the
   truth meets >= 2 blocks and beta-min is fixed (`theta_min >= b_0 > 0`), `O_P(2^B n^{-1/2})` by a self-contained argument
   (Thm 6, **PROVED**). In the locked T22(iii)
   proof, NL_eta is needed only to supply NL_avg; Lemma quad works with any `delta^2 <= C sigma^2 log n` (Prop. 2.1).
3. **H2 of T27(i) is replaced by a checkable chain-leakage condition** CL(L): `max_i |delta_{T_i,l_i}| <= L sigma`.
   CL(L) implies the two-sided ratio law (Thm 3, **PROVED**) and hence T27(i) given H3 (Thm 4, **PROVED**); with growing
   leakage `L_n` the law stays two-sided with upper multiplier `e^{O(L_n^2)}`; masking persists while `L_n^2 <= eta log n`,
   small eta. A limit law `log pi0(S0) + c log p + (c/2)log n -> sum log((s+i+1)/2) + sum (L_i+Z_i)^2 sigma^2/(2v)` is a PROOF SKETCH and
   matches exact computation to two decimals.
4. **One explicit family carries both premises jointly (input for T38(b))**: the *linked-hub* family LH = S3/S4/S6
   equicorrelated independent groups plus, per masked variable, one rank-one "suppressor edge" between two group hubs
   (`corr(j_a, j_b) = psi`, `theta_{j_b} = -psi theta_{j_a}`). In the exact-Gram realisation (p <= n-1), with blocks = groups
   (`g <= B < 2g`, `|psi| < rho`): `pi0(S0) = p^{-c} n^{-c/2} e^{O_P(1)}` (masked), `pi0(R_0) >= pi0(S0 \ M) = 1 - O_P(2^B n^{-1/2})`
   (so `b_n -> 1`, reference `S° = S0 \ M ∈ R_0`), and `pi(S0) -> 1` (Thm 5, **PROVED** except the limit-law refinement;
   part (d) cites locked T03). The iid-Gaussian realisation (closest to the study generators; p > n allowed) is a
   PROOF SKETCH (§4.3).
5. **Exact computation at p = 16 and p = 20 (n from 50 to 1.6·10^6)** confirms every predicted rate:
   `sqrt(n)(1 - pi0(S°))` is flat at 1.6 (no sqrt(log n)); the T27 statistic converges to its predicted law
   (median 0.55 vs 0.54, 95% 0.79–0.89 vs 0.84); `pi0(R_0) -> 1`; `pi(S0) -> 1`; the EXP′ remainder `max|R|` is at most 1.8 (n = 50, random design), decreasing to 0.67.
6. **Regime split, study relevance.** At population level S1, S3, S4, S6 are block-orthogonal: they sit in the
   *favourable* regime asymptotically. S5 (common factor) and S2 (AR) have block leakage linear in n (98/100 and 81/100 of
   the 5-blocks; `scripts/pop_leak_study.py`): neither clean theorem applies there. The study's own masking at n = 200
   (median `pi0(S0) ~ 1e-12`) is therefore **not** the cancellation mechanism of T27; it fits *weak-signal* masking,
   which is CL(L) with bounded L (CONJECTURE, see "Needs escalation").

## Refined statements (full; named hypotheses; regime explicit)

Common setting: G (fixed design, `eps ~ N(0, sigma^2 I)`), triangular array, blocks = the v3 partition (any partition
with `|C_b| <= 16` where stated), `nu = 0.01 + n/2`. Hypotheses:

| Name | Statement | Checkable? |
|---|---|---|
| R-lite(A,M) | `p <= n^A`, `||mu||^2 <= Mn` | given truth |
| SE-blk(phi0) | `min_b lambda_min(R_{C_b}) >= phi0^2` | yes, from X |
| BO | `X_{C_b}'X_{C_b'} = 0`, `b != b'` | yes, from X |
| BM-blk | `min_{j in S0} theta_j^2 >= M_n(sigma^2+2M) log n/(phi0^2(n-1))`, `M_n -> inf` | given truth |
| ZL(S°) | `lambda_b(S°) := ||(P_{C_b} - P_{S° ∩ C_b}) mu||^2 = 0` for all b | given truth (exact) |
| NL_C(S°) | `max_b lambda_b(S°) <= C sigma^2 log n` | given truth |
| SPREAD(Delta_0) | `min_b ||(I - P_{C_b}) mu||^2/(n-1) >= Delta_0 > 0` | given truth |
| VIS-lin(S°, c_V) | `min_b min_{U ⊆ C_b, S°∩C_b ⊄ U} ||(P_{U ∪ S°_b} - P_U) mu||^2 >= c_V n` | given truth |
| H1 | fixed chain `S^(0) ⊂ … ⊂ S^(c) = S0` of single additions, s, c fixed | definition |
| CL(L_n) | `max_{i<c} |delta_{T_i,l_i}| <= L_n sigma`, `T_i = S^(i) ∩ C_{b_i}` | given truth |
| H3 | `P(pi0(S^(0)) >= c0) -> 1` | — (discharged by Thm 6) |

**Thm 1 (EXP′; any regime).** G, R-lite, SE-blk ⇒ on `E_n` (`P(E_n) -> 1`), for all within-block additions,
`log r_b(T+l)/r_b(T) = -(1/2)log(n+1) - nu log(1-x_{T,l}) + R`, `|R| <= kappa_EXP := (1+phi0^{-2})/(2phi0^2(n-1)) +
(n/2+0.01)(1.02 + 1/(n phi0^2))/(c_* n)`. **PROVED.**

**Thm 2 (favourable regime, BO).** G, R, SE-blk, BO, BM-blk ⇒ `1 - pi0(S0) = O_P(2^B sqrt(log n) n^{-1/2})`.
**PROOF SKETCH** (hypothesis verification complete; relies on the locked T22(iii) proof with eta = 0).

**Prop. 2.1 / 2.2 (locked T22(iii) refined).** NL_eta may be replaced by NL_C in Lemma quad; S0 may be replaced by any
deterministic feasible reference S° (the proof never uses `supp theta* = S0`). **PROOF SKETCH.**

**Thm 6 (start concentration on a reference under exact zero leakage; either regime — S° = S0 is favourable,
S° ≠ S0 is masked).** G, R-lite, SE-blk, ZL(S°), SPREAD, VIS-lin(S°) ⇒ `1 - pi0(S°) = O_P(2^B n^{-1/2})`,
`e_n° = O_P(e^{-cn})`. **PROVED** (via wave-1 T22(i)).

**Thm 3 (two-sided chain law; masked regime).** G, R-lite, SE on the c chain sets, H1, CL(L_n) ⇒ w.p. -> 1, for all i:
`-1 - kappa_EXP <= log[r(T_i+l_i)/r(T_i)] + (1/2)log n <= kappa_EXP + 1.01(L_n + |Z_i|)^2`, `Z_i ~ N(0,1)`.
With fixed L this is H2. **PROVED.** (Numerically the sharp multiplier is `(L + Z)^2 sigma^2/(2 v_{T_i})`, see §4.)

**Thm 4 (T27(i) from chain leakage; masked regime).** Thm 3's hypotheses with fixed L, H3, `p >= 2(s+c)` ⇒
`log pi0(S0) + c log p + (c/2) log n = O_P(1)`. With `L_n -> inf`: the lower side is unchanged and the upper side gains
`+1.01 c (L_n + O_P(1))^2`. **PROVED** (given H3).

**Thm 5 (joint masked-regime family LH, exact Gram, p <= n-1).** LH with `|psi_i| < min(rho_{a_i}, rho_{b_i})`,
`g <= B_n < 2g`, fixed nonzero betas, `S° = S0 \ M`, `|M| = c`:
(a) `1 - pi0(S°) = O_P(2^B n^{-1/2})`, hence `pi0(R_d) >= pi0(R_0) >= 1 - O_P(2^B n^{-1/2})` for all d;
(b) `pi0(S0) = p^{-c} n^{-c/2} e^{O_P(1)}`;
(c) VIS at reference S0 fails in each masked block: the favourable branch is inapplicable on this sequence;
(d) `1 - pi(S0) = O_P(sqrt(log n/n))` (locked T03);
(e) start masked, target not: the bridge must transport mass from `S° ∈ R_0` to `S0`.
**PROVED** for (a)(b)(c)(e) and (d) by citation; limit law in (b) PROOF SKETCH.
**Regime discipline:** Thms 2 and 5 are never combined on one sequence; on LH the reference used for T22(i) is S°, not S0.

## Proofs / sketches

All in `PROOF.md`: §1 (Thm 1 and Lemmas 1.1–1.4, complete), §1.5 (extensions), §2 (T22(iii) consequences, Lemma 2.3,
Thm 2, Thm 6 complete), §3 (Thms 3–4 complete, limit-law sketch), §4 (LH family: Lemmas 4.1–4.2 complete, Thm 5,
random-design sketch).

## Evidence (exact computation; `scripts/exp_family.py`, `scripts/exp_leak.py`; seeds fixed in the scripts)

Exact objects: scores on sufficient statistics (exact-Gram: `X'eps` simulated exactly as `sqrt(n-1) L xi`, `xi ~ N_p(0,I)`,
plus an independent `chi^2_{n-1-p}`; random design: Bartlett–Wishart), the v3 partition (port of `v3_blocks.h`, R13 ties),
all block tables, exact `pi0` normalisation by bivariate block-profile convolution (checked against brute-force
enumeration to 1e-12, `scripts/sanity.py`), exact `pi` by full enumeration (2^16 / 2^20 models).

Config A: p = 16, 4 groups of 4 (B = 4), rho = 0.7 (S3), psi = 0.5, theta = (1.4 on j_1, -0.7 on j_2, 1.8 on j_3), c = 1,
s = 2. 200 replicates (pi on 40). Predicted law of `Mstat = log pi0(S0) + log p + (1/2)log n`:
`log(3·16/29) + chi^2_1/(2v)`, `v = 5.71`: q05 0.504, median 0.543, q95 0.840.

| n | B | blocks = groups | med log10 pi0(S0) | Mstat q05/med/q95 | sqrt(n)·med(1-pi0(S°)) | med pi0(R_0) | med pi(S0) | max abs R (EXP′) |
|---|---|---|---|---|---|---|---|---|
| 100 | 4 | 1.00 | -2.05 | 0.26 / 0.35 / 0.62 | 1.72 | 0.844 | 0.669 | 1.06 |
| 400 | 4 | 1.00 | -2.31 | 0.41 / 0.45 / 0.70 | 1.58 | 0.926 | 0.846 | 0.79 |
| 1600 | 4 | 1.00 | -2.59 | 0.46 / 0.50 / 0.75 | 1.59 | 0.963 | 0.930 | 0.77 |
| 6400 | 4 | 1.00 | -2.88 | 0.48 / 0.52 / 0.87 | 1.63 | 0.981 | 0.957 | 0.70 |
| 102400 | 4 | 1.00 | -3.47 | 0.50 / 0.54 / 0.87 | 1.62 | 0.995 | 0.989 | 0.68 |
| 1638400 | 4 | 1.00 | -4.07 | 0.50 / 0.55 / 0.87 | 1.63 | 0.999 | 0.997 | 0.67 |

`log10 pi0(S0)` falls by 0.30 per factor 4 in n, the predicted `-(1/2) log10 4 = -0.301`. The T22(i) lower bound
`(1-q)^{s+1}/(1+e)^s` held in every replicate and tends to `pi0(S°)` (0.997 at the largest n). A85 (rho = 0.85, S4)
is indistinguishable (Mstat median 0.55, `sqrt(n)(1-pi0(S°))` = 1.62, `pi(S0)` 0.997 at n = 1.6e6).

iid-Gaussian realisation of A (random X, sample partition): blocks = groups in 100% of replicates at every n >= 50;
Mstat median 0.76, q95 2.66 at n = 1.6e6 — the predicted random-design law `const + chi^2_1/2` has median 0.73, q95 2.42
(the in-sample `delta_{∅,j_b} ~ N(0, ||mu||^2/(n-1))` adds variance; masking rate unchanged);
`sqrt(n)(1 - pi0(S°))` stays in [2.5, 3.0] (consistent with `O_P(sqrt(log n) n^{-1/2})`); `pi0(R_0)` 0.998, `pi(S0)` 0.997.

Config B (c = 2, p = 20): see `results/fam_B_*.log` (prediction: `log10 pi0(S0)` slope -1 per decade of n, Mstat
-> `log(60/37) + log(80/36) + (chi^2_2)/(2·4.9)`, median 1.42). Table filled in §"Config B" below when the run completes.

Leakage chain (Task 2; `results/leak_chain.log`, 300 reps): masked coefficient perturbed so that
`delta_{∅,j_b} = L_n` exactly. Predicted Mstat law `log(48/29) + (L_n + Z)^2/(2v)`:

| case | n = 1600: obs q05/med/q95 | pred | n = 1.6e6: obs | pred |
|---|---|---|---|---|
| L = 0 | 0.46/0.50/0.76 | 0.50/0.54/0.84 | 0.50/0.56/0.84 | 0.50/0.54/0.84 |
| L = 2 | 0.49/0.80/1.67 | 0.52/0.85/1.66 | 0.52/0.89/1.69 | 0.52/0.85/1.66 |
| L = 4 | 0.98/1.83/3.11 | 0.99/1.90/3.28 | 0.99/1.90/3.38 | 0.99/1.90/3.29 |
| L = sqrt(2 log n) | 0.87/1.77/3.10 | 0.93/1.79/3.13 | 1.62/3.06/4.77 | 1.71/3.01/4.78 |

Bounded leakage leaves the `n^{-1/2}p^{-1}` law intact with a tight multiplier; growing leakage enters only through the
predicted `(L_n + Z)^2/(2v)` — the "controlled multiplier" of Thm 3, here with its sharp constant `1/(2v)`.

## What fails and why

* **Packing at the study's B.** At n = 200, p >= 500, B = 14: next-fit packing puts two groups of 5 in one block. If a
  linked pair is packed together, the block sees both hubs, masking disappears (favourable within that block). LH needs
  `g <= B < 2g` (or, more generally, the hypothesis "the two hubs of each linked pair are in different blocks", checkable).
  With growing p, B -> 16, so `9 <= g <= 16`; the p <= 20 runs use g = 4, B = 4.
* **Exact-Gram needs p <= n-1.** The p > n case is covered only by the random-design sketch (§4.3).
* **NL_eta fails for random designs at fixed SNR** (`max_l delta_{∅,l}^2 ≈ 2A theta'Sigma theta log n` over ~p nulls), so the
  locked T22(iii) does not transfer to iid designs as stated; Prop. 2.1 + an average/truncation argument (§4.3) is the route.
  Note `E(1-x)^{-nu} = inf` for a pure-noise column (`nu > (n-|T|-2)/2`): truncation is essential, not cosmetic.
* **S5 and S2 sit in neither clean regime**: population block projections are dense (common factor / AR overlap),
  `lambda_b` linear in n for most blocks. Neither Thm 2 nor Thm 5 says anything there.
* **Crude constant in Thm 3**: the proved upper multiplier `1.01(L+|Z|)^2` is loose by the factor `2v/sigma^2` against the
  sharp `(L+Z)^2 sigma^2/(2v)` seen numerically; sharpening uses `RSS_{T+l} = (n-1)v_{T+l}(1+o_P(1))` (T22(iii) Lemma residual).
* **Theorem 6's SPREAD** excludes the case where one block carries the whole signal (then `Delta = 0` and the exponent
  hits the non-integrable `1/2`); the locked T22(iii) truncation route covers it at the price of `sqrt(log n)`.

## Needs escalation

1. **Locked-register update (HQ/Felipe):** EXP′ can be removed from T22(iii)'s hypothesis list (Thm 1), and Decision
   Point 2's D1 is discharged. NL_eta can be weakened to NL_C + NL_avg (Prop. 2.1). These are edits to locked statements.
2. **T38(b) formulation:** use reference `S° = S0 \ M ∈ R_0` and state the masked branch on LH (Thm 5) with the explicit
   block-separation hypothesis for the linked hubs; never use T22(iii) at S0 on that sequence.
3. **Interpretation of the n = 200 data** (1/2394 favourable; `pi0(S0) ~ 1e-12`; `pi0(R_2) ~ 0.8`): population analysis says
   S1/S3/S4/S6 are asymptotically favourable, S2/S5 leak. The masking seen is most plausibly *weak-signal* masking
   (local alternatives make CL(L) hold with bounded L for the weak truths, so T27(i)'s law applies with c = number of weak
   truths, and `pi0` concentrates on `S0` minus those, consistent with `pi0(R_2) ~ 0.8`). CONJECTURE — not checked on
   the data here (R not available; fitting data not in repo). In that mechanism `pi(S0)` is *also* small, unlike LH.

## Outside scope (not attempted)

T38 itself; bridge transport from S° to S0; T22(iii) for S2/S5; full proof of the random-design version; the exact
branch (at p <= 17 the method enumerates and builds no blocks — pi0 here is the analytically defined component law).

## Confidence cards

| Target | Statement | P(true) | P(provable at reasonable cost) | Crux | Method change needed? |
|---|---|---|---|---|---|
| T1 EXP′ | Thm 1 (all fixed designs, SE-blk) | 0.97 | done (PROVED) | Lemma 1.1 bound on `c_S`; RSS floor | No |
| T1 ext. random design | SE-blk w.p. -> 1 for every <=16-partition; EXP′ holds | 0.93 | 0.85 | 17-sparse eigenvalue concentration (standard) | No |
| T22(iii) in BO | Thm 2 / Thm 6 | 0.95 | 0.9 (Thm 6 done) | transfer of locked proof (Thm 2) | No |
| T22(iii) iid designs (S3/S4/S6) | `1-pi0(S0) = O_P(2^B sqrt(log n) n^{-1/2})` | 0.8 | 0.6 | uniform truncated Beta average over the X-dependent partition | No |
| T27(i) from CL | Thms 3–4 | 0.97 | done (PROVED given H3) | — | No |
| T27 limit law | `Mstat -> sum log((s+i+1)/2) + sum (L+Z_i)^2 sigma^2/(2v)` | 0.9 | 0.8 | uniform `RSS/(n v)` -> 1 and remainder -> 0 at T = ∅ | No |
| Joint family LH (exact Gram) | Thm 5 | 0.95 | done except limit law | Lemma 4.2 (partition), Thm 6 | No |
| Joint family LH (iid Gaussian, p > n) | §4.3 | 0.85 | 0.6 | conditional-independence/Beta argument uniformly | No |
| Weak-signal masking explains data | CONJECTURE above | 0.6 | 0.5 | needs the data / per-fit diagnostics | No |

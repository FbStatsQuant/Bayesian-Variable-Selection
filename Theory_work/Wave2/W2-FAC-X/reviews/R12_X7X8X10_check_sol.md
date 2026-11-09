# R12 — X7, X8 and X10 lemma check

Reviewed against `STATEMENT_T2.md` **v2, locked**, and Target 1's `STATEMENT.md` v3. All claims are interpreted asymptotically, as instructed. Only this review file was written. No numerical experiment is claimed.

| Lemma | Verdict |
|---|---|
| X8, general-loading start mode | **VERIFIED**, models (R) and (G) |
| X10, FAC-GL assembly | **VERIFIED**, conditional on its explicitly cited (G2) inputs |
| X7, FAC-NCS | **FAILED as written for (G)**; **VERIFIED-WITH-AMENDMENTS for (R)** |

There are **no FATAL findings**. Issue 1 is **MAJOR**: the exact-Gram path transfer imports an iid multiplier bound that is false even at zero dispersion, and does not specify all the required replacements. This is a failure of the supplied proof transfer, not a counterexample to FAC-NCS. A repair preserving the locked statement is described below. The narrowed (NCS) condition does repair R10's spacing/rate objection in both models.

## Numbered issues

### 1. MAJOR — X7's exact-Gram transfer does not preserve X4's standing bounds and noise formulas

**Location:** `lemmas/X7_near_cs_loadings.md:30–35,44,48–54`; imported `X1_representation.md` §X1.4 (g3), (g5), and `X4_path.md` §§X4.0, X4.4–X4.6.

**Reason.** X7 correctly obtains the exact-Gram multiplier

\[
M_T=\frac{\nu n\sigma^2}{(n+1)s^2\psi_T}.
\]

However, X4's bulk and end-phase calculations explicitly use the iid bound

\[
M_T\le\tfrac12(1+C/n).
\]

This bound does **not** transfer. In the iid proof its sharp upper bound comes from cancellation of the observed noise norm in the numerator with RSS in the denominator, together with the two `(1+q)` factors. In (G) the numerator instead contains the fixed population variance.

An analytic falsification is available already with equal loadings, hence with **Delta = 0**, satisfying (NCS). Fix p and a fixed set T containing the truth, of size k. For example take one positive truth coefficient and fixed p > 16; the start set has fixed size and contains a null whatever its truth-containing block. Exact Gram gives

\[
\mathrm{RSS}_T/\sigma^2\sim\chi^2_{n-1-k},\qquad
s^2\psi_T=\mathrm{RSS}_T+O_P(1).
\]

The latter follows from the Q-versus-RSS bound in FACB L1.5(b), whose eigenvalue-based proof applies here, and boundedness in probability of s squared. Therefore

\[
\sqrt n(2M_T-1)\ \Rightarrow\ N(0,2).
\]

For every fixed C, the probability of the imported upper bound tends to **1/2**, not 1. Thus it cannot be a consequence of an event of probability tending to one. This is an asymptotic obstruction to the asserted verbatim transfer, rather than a finite-n objection.

There are related missing replacements. X7's exact-Gram omega is of order one per fixed null statistic; it is not the iid omega divided by sqrt(n). Hence the standing iid condition `omega_j^2 <= 1/10` and the end-phase assertion `omega_j^2 = O(Hbar^2/n)` cannot be reused. Leaving X1.4(g5)'s `C Hbar^4 max omega^2` remainder in place would not give X4.5's o(1) error. Likewise, X4.6's identity bounding the noise projection through `q_U/(1+q_U)` has no literal exact-Gram counterpart. Saying that all W-terms are absent does not replace these formulas or the phi/a parts of D3.

**Fix, without changing the locked hypotheses or conclusion:** insert an explicit exact-Gram event and gain-transfer paragraph, with the following ingredients.

* Enlarge the Gaussian space as in FACB L1.1 / T2 L4r.0: `g = lambda eta + Psi^(1/2) xi`, with independent standard eta and iid standard xi; retain the correct joint noise norm, for example through the independent residual chi-square construction. Require `| ||e||^2/sigma^2 - (n-1) | <= n^(2/3)` and D4. Retain D6, E-prime, D7, D8 and ND from X4 with the new deterministic widths. Delete D1, D2, D5 and the phi/a requirements; they are unnecessary in (G). The norm and xi events need not be independent: a union bound suffices.
* Define explicitly `tauhat_j = sqrt(1-gamma_k) omega_j^G`, `delta_j = tauhat_j - (xi_j-x_T)`, with `kappa = 1/ellbar^2`. The stated rank-one perturbation calculation then gives the (G) delta estimate uniformly over sets, with no Wishart or band-count term.
* Put `Phi(U) = g_U' Sigma_UU^(-1) g_U`. Uniformly in U, D4 gives `Phi(U) <= C p Hbar^2`. Q-versus-RSS then yields

  \[
  |M_T-\tfrac12|\le C\{n^{-1/3}+p\bar H^2/n\}=:C\epsilon_n,
  \qquad \epsilon_n\bar H^2=o(1).
  \]

  This replaces the false O(1/n) upper bound. The last displayed rate holds under (P-half), so the changed quadratic terms are o(1), preserving both logarithmic margins and the end-phase comparisons.
* In (g3) set the iid multiplicative correction `epsilon_j^d` to **zero**. In (g5) use the exact identity `M_T psi_T = nu n sigma^2/((n+1)s^2)`, independent of T. Thus its multiplier ratio is exactly one and the iid `Hbar^4 max omega^2` correction disappears, rather than being estimated using the differently scaled (G) omega. Ridge and determinant remainders still have their stated absolute orders. The remaining swap error is `O(Hbar max|delta| + max delta^2) + o(1) = o(1)`.
* In X4.6 use `||P_U e||^2 = sigma^2 Phi(U) <= C p Hbar^2` and `||r_j||^2 >= (n-1) min psi_j`. This supplies the truth-move proof directly, without q. X4.1's ordering slack also follows directly with `epsilon_j^d=0` and the same ridge/determinant bounds.

These replacements explain why the (G) conclusion remains plausible and repairable with `varpi_G = C0 n^(-1/3)`. They are needed before certifying the current two-model X7 proof. Merely enlarging C7 or the dispersion floor does not make the imported multiplier inequality true.

### 2. MINOR — an intermediate envelope drops the log term in r_n

**Location:** `lemmas/X7_near_cs_loadings.md:43`.

**Reason.** The displayed bound replaces `r_n sqrt(k)` by `C p/sqrt(n)`. But X2 defines `r_n = 3 sqrt(p/N) + 3 sqrt(2 log n/N)`; with bounded p the second term cannot be absorbed by the first with a fixed constant. The final desired perturbation bound is unaffected.

**Fix:** retain

\[
C\left\{p/\sqrt n+\sqrt{p\log n/n}\right\}
\left\{\sqrt{\log n/n}+\Delta_n\right\}\bar H.
\]

For p <= sqrt(n), its non-dispersion part is at most `C Hbar sqrt(p log n/n)`, and its dispersion part is at most `C Delta_n Hbar` eventually. This proves the next line with the same form and handles bounded p as well. This is a missing term in the algebraic bound, not an objection to asymptotic scope.

## Checks of the narrowed NCS condition

Write `A1 < 1/2` with `p <= n^A1`, and suppress fixed constants. For (R), the enlarged deterministic scale is

\[
w\asymp\varpi'_n=O(\bar H\sqrt{p\log n/n}+n^{-1/3}).
\]

The loading perturbation is bounded by `C Delta_n Hbar <= C n^(-1/3)`. The reference centre satisfies `|x_T| <= C Hbar`, so the same conclusion holds for the displayed (G) perturbation; in (G) one can use `w = O(n^(-1/3))`. Constants in this step must absorb the centre bound as well; the notation C7-prime may be enlarged accordingly.

The following are the actual rate checks, rather than a transfer based only on w tending to zero:

* **D6:** the finitely many deterministic widths `4.3 varpi'` and `9 varpi'` eventually lie in `[n^(-1),1]`. The same iid-xi window-count proof works in both models.
* **D7:** in (R), `w <= n^(-min((1-A1)/2,1/3)+o(1))`, which is stronger than the exponent `n^(-(1/2-A1)/2+o(1))` used by X4. In (G), `w = O(n^(-1/3))` also satisfies that weaker bound. Thus X4's `c_w` and `T0` still suffice; in particular `w Hbar log^3 n <= n^(-c_w)` eventually.
* **D8(S):** if `p <= n^(1/200)`, then `p^2 w = O(n^(-0.4875) log n + n^(-1/3+1/100)) -> 0` in (R), and the second term alone suffices in (G). R10's earlier slow-decay counterexample is excluded.
* **D8(L):** the close-tail-pair bound is `O(w (1+Hbar) m1^2 exp(Cw Hbar)) = o(1)` for either scale, since `m1 = O(log log n)` and w has a fixed polynomial decay exponent.
* **B3 Case B:** `p w^2 + w log n = o(1)`. In (R), `p w^2 = O(p^2 log^2 n/n + p n^(-2/3))`; both terms vanish. In (G), it is `O(p n^(-2/3))`. Thus the negative contribution of the narrow band is indeed o(1).
* **Band absorption / deletion budget:** the iid feedback coefficient is `C p Hbar sqrt(log n/n) -> 0`, and the additive remainder divided by the floor is `O(Hbar (log n)^(3/2) n^(-1/6)) -> 0`. Taking C7 sufficiently large absorbs the dispersion term while reserving the X4.1 ordering slack. In (G) there is no Wishart band term to absorb. ND, E-prime, Gaussian order/sign events and X3's deterministic drift remain valid for the same iid xi sample. In (G), kappa equals kappa-infinity exactly.

Thus **no additional spacing/rate failure survives (NCS)**. The issue in the (G) proof is the model-specific gain/event transfer in issue 1, not loading dispersion. For (R), the representation, inverse and normalisation perturbations, X3, the rate checks above, and X4's gain comparisons give the claimed path after issue 2's local algebra correction. Non-masking follows from the finite CS population margin and continuity on the fixed-size blocks; zero pairs remain exactly zero. X6 then assembles (R) consistency and delivery.

## X8: line-by-line disposition — VERIFIED

* **Lines 6–15:** sign correction is legitimate under locked v2's corrected (FS-G). The eigenvalue floor `psi_lo` and bounded covariance entries are uniform in the loading array. The four listed properties are precisely the ingredients of X5's proof.
* **Lines 17–19:** the asserted range suffices; (P-S) lies within it. No assumption of independence between the realised partition and the noise coordinates is introduced.
* **Lines 21–27:** Lemma CR is uniform in the bivariate population correlation. Sample-sd concentration also controls the random coefficients: `||theta* - vartheta|| <= delta'_n ||vartheta||`. Together with the inverse identity and fixed `|V| <= 16+s0`, this gives the stated uniform Lipschitz error. The rotation/Wishart eigenvalue argument holds for general diagonal Psi. Although the auxiliary rotation uses the noise direction, the resulting event A_n is a raw-design event, as required for conditioning. The probability bound for that design event follows by containment in the auxiliary good event.
* **Lines 27–31:** for zero pairs the signal residual vanishes identically; for all other pairs (FS-G) supplies one common positive margin. Conditional on the raw design, E1 bounds all projections and E2 unions over only the finitely many zero pairs in the realised truth block. E3 and the energy bound give common s-squared bounds. X5.3 therefore gives positive order-n increments for nonzero pairs and negative order-log-n additions for zero pairs. X5.4's combinatorial proof of uniqueness applies without CS. For (G) the same argument holds with deterministic design and exact population partial covariances.

No amendments required. In particular, the random coefficient issue in (R) is covered by X8's inherited sd event and its explicit joint Lipschitz formulation, rather than an assumption that standardized coefficients are fixed.

## X10: line-by-line disposition — VERIFIED, conditional on G2

* **Lines 3–10:** the dependency qualification is explicit. Start and uniform path events can be intersected without independence. The MR1 cap covers all null deletions and the final scan; CAP(a) gives certification, hence the stronger event that S0 is scored.
* **Lines 12–15:** the global lower eigenvalue bound supplies both anchored eigenvalue requirements, with fixed positive constants. Entries bounded by one and fixed support size give the energy bound. Beta-min follows from the nonzero fixed truth vector, and in (R) from the sample-sd bounds with common constants. X6.1's every-sequence argument applies to raw-design conditioning; no illicit exchange of pointwise convergence and integration is needed.
* **Lines 17–18:** operational closure bounds D_n by the LS0 failure probability in the correct direction. T03-sharp and boundedness give the posterior expectation limit; M5-0 then gives the joint error bound. The liminf identity follows from `P(output and correct) = 1-P(U_n)-P(output and wrong)`.
* **Lines 20–22:** the cited amended allocation and total tier-1 fallback are retained. A2's Lemma-S and resource proof uses nonconstant columns, Gaussian response regularity and positive Q, not compound symmetry. D-prime's pathwise inclusion with the scored-truth event gives delivery consistency without CAL. The existing qualifications of the reused implementation/audit inputs are not upgraded.

This verdict checks the assembly implication; it is **not** a new certification of X9 or of all of T2/L4r. Those are explicitly assumed path inputs. X10 does not depend on X7, so issue 1 does not invalidate FAC-GL's assembly.

## Final disposition

**X8 VERIFIED; X10 VERIFIED conditional on its stated path inputs; X7 FAILED as written for (G), VERIFIED-WITH-AMENDMENTS for (R).**

**FATAL: none. MAJOR: issue 1 only — supply the exact-Gram event, multiplier, swap-error and truth-projection replacements before certifying FAC-NCS for (G).**

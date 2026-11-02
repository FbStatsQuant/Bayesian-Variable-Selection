# CLAIMS OF FATAL FLAWS — T13 (T10) restricted ESS

Every fatal or gap finding, copied verbatim, with the lead's answer. Exposition findings are listed briefly at the end of each round.

## Stage A, round 1 — Astra #1 review of PROOF_v1 (review\astra_05_proof_review_v1.log)

### A1-1 (gap)

> **Location:** §5.1, “Numerical values”; §§5.2–5.3, numerical comparisons; Appendix A, particularly `mp.dps = 40`.
>
> **Severity:** gap.
>
> **Claim:** The exact inequalities establishing the witnesses lack a justified numerical error bound.
>
> **Evidence:** Appendix A evaluates noninteger powers, logarithms, exponentials, sums, and ratios using ordinary finite-precision `mpmath` arithmetic. It supplies neither certified enclosures nor an error analysis. Consequently, the displayed approximations alone do not rigorously establish \(a_c(1)\ge0.9\), \(a_c(2)<0.9\), the divergence-bound violation, \(\beta>\alpha\), or the two acceptance inequalities. These comparisons are essential to parts (ii)(c)–(d). EX-A specifies the idealized construction’s arithmetic; it does not certify the appendix’s floating-point calculations. Independent agreement and the substantial numerical margins make this plausibly fixable, but do not supply the missing certification.

**Lead's answer: accepted and fixed in PROOF_v2.** All rational inputs (ϖ(k), t_i, ν, binomial counts) are now computed exactly with integer and fraction arithmetic and converted to enclosing intervals. Every transcendental step (√, log, exp) is evaluated in interval arithmetic with outward rounding (`mpmath.iv`, 50 digits), so each output interval contains the exact real value. The seven inequalities the witnesses use (D > 0, a_c(1) ≥ 0.9, a_c(2) < 0.9, 1+χ² > 1000/729, β > α, ρ_{V_d}(0,½) ≥ 0.9, ρ_{V_d}(½,1) ≥ 0.9) are decided by comparing interval endpoints, and all pass. All enclosures are narrower than 10⁻²⁰. The script `witness_certified.py` and its full output are in Appendix A of PROOF_v2. §5.1 now states the certification rule, and the displayed decimals are marked "≈" and described as orientation only.

### Exposition findings, round 1 (not fatal or gap; handled in PROOF_v2)
- A1-2: the claimed independent validation (Cholesky check, reduced enumeration) could not be audited from the packet. **Fixed:** the claim is removed from the proof. The proof does not rely on it; the check itself is in `helpers\check_sonnet\`.
- A1-3: rounded values were written as exact equalities, and 10/(9·0.81) is exactly 1000/729. **Fixed:** "≈" with a stated meaning, and 1000/729 written exactly.

## Stage A, round 2 — Astra #1 ruling on the log and review of PROOF_v2 (review\astra_06_ruling_v2.log)

Rulings: A1-1 agree, fix works; A1-2 agree, fix works; A1-3 agree for the main text, incomplete in Appendix A. Verdict on PROOF_v2: **verified**.
No fatal or gap finding. One exposition finding: printed interval endpoints were rounded to nearest, so a printed interval could fail to contain the exact value (e.g. the printed 1000/729 singleton). **Fixed in PROOF_v3:** the endpoints are converted exactly to rationals and rounded outward to 22 decimals, and the docstring and §5.1 now say so. The decisive checks were already on internal endpoints and are unchanged.

## Stage A, round 3 — Astra #1 confirmation of PROOF_v3 (review/astra_07_confirm_v3.log)
Fix confirmed; no remaining findings; verdict **verified**. PROOF_v3 = Stage A proof candidate.

## Stage B, round 1 — independent reviews of PROOF_v3

### B-A2-1 (Astra #2, gap) — review/stageB_astra2_01_review_v3.log

> - **Location:** §1, Lemma 1; §5.1, “The data set” and Lemma 4.
> - **Severity:** gap.
> - **Claim:** The identification of the proof’s likelihood, block construction and budgets with the method incorporated into STATEMENT.md cannot be verified from the permitted files.
> - **Evidence:** STATEMENT.md imports definitions from `00_COMMON.md` and `METHODOLOGY_v3.md` without reproducing the marginal-likelihood formula, hyperparameters, block-size rule, dependence of blocks on \(X\) alone, or budget formulas. The proof supplies these as facts. Their conformity with the imported method is essential: the likelihood determines positivity and the witness scores; the block rule permits choosing \(j_2\) before defining \(y\); and the budgets establish the SMC branch and allowable grids. The subsequent calculations are consistent, but the correspondence to the referenced method remains unchecked. This is a verification limitation, not evidence that those assertions are false.

**Lead's answer: accepted and fixed in PROOF_v4.** New Appendix B quotes verbatim, copied mechanically by line number with both files' SHA-256 checksums, every definition the proof uses: 00_COMMON §1 (data, standardisation, Ω, G_S, z_S, H_S, D_S, Q_S, ν, a₀ = b₀ = 0.01, m(S), w, W_K, ϖ), 00_COMMON §2 (blocks deterministic in X with |C_b| ≤ B, tables, γ₀, d, bridge; budgets; exact branch), and METHODOLOGY §3 (budget table), §4 items 1–4 (input checks, standardisation with the n − 1 SD), §5 (target), §6.2 (exact branch), §6.3 (clustering, cut, packing, tables, start, discrepancy) and §6.7 (V, F_V, ρ_V, construction). Lemma 1 now restates the definitions with citations. §5.1 now derives the three block properties (X-only, partition, size cap) and the standardisation and budget facts from the quotes.

### B-O-1 (Opus, gap) — review/stageB_opus_01_review_v3.md, finding 1

> **Claim:** The proof uses a specific formula for m(S) that I cannot check against its source. STATEMENT.md defines m(S) only by reference to 00_COMMON §1, which is not in the packet. [...] The proof never states the definition of Q_S or the values of a₀ and b₀. [...] The only open question is whether this is the m(S) of 00_COMMON.

(Full text verbatim in review/stageB_opus_01_review_v3.md, finding 1.)

**Lead's answer: accepted and fixed in PROOF_v4.** The m(S) formula with a₀ = b₀ = 0.01, ν = 0.01 + n/2, the definition of Q_S, H_S and D_S are now stated in the proof of Lemma 1, cited to Appendix B (00_COMMON §1 lines 10–11; METHODOLOGY §5). They match what v3 used.

### B-O-2 (Opus, gap) — finding 2

> **Claim:** The step "‖x_j‖² = 41 = n−1, so every sample SD equals 1 … standardisation returns X and y unchanged" assumes 00_COMMON standardises with the n−1 denominator. That convention is not in the packet.

**Lead's answer: accepted and fixed in PROOF_v4.** Both sources use the n − 1 denominator: 00_COMMON §1 line 9 ("s_y² = ‖Cy^r‖²/(n−1); so ‖x_j‖² = ‖y‖² = n − 1") and METHODOLOGY §4 item 4 ("divide by the sample SD (denominator n − 1)"). Both are quoted in Appendix B. §5.1 now shows that both forms of the standardisation (00_COMMON's CX^rD_x⁻¹, and the method's divide by max |x|, centre, divide by SD) return X and y unchanged. Lemma 4 is therefore correct as written.

### B-O-3 (Opus, gap) — finding 3

> **Claim:** The proof uses three properties of the method's block construction that the packet does not contain. [...] (a) The blocks depend on X only, not on y. [...] (b) The blocks partition [p]. [...] (c) Block size is capped at B = min(⌊√n⌋, ⌊√p⌋, 16).

**Lead's answer: accepted and fixed in PROOF_v4.** §5.1 "Blocks" derives the three properties from the quotes:
- (a) 00_COMMON §2 line 18 ("deterministic in X") and METHODOLOGY §6.3 (distance "computed from X"; the cut and packing use only the dendrogram, B and index order).
- (b) The root holds all p columns; the cut replaces a node by its two children until every retained cluster has at most B members; packing places whole clusters ("a retained cluster is never split") into blocks.
- (c) |C_b| ≤ B = min(⌊√n⌋, ⌊√p⌋, 16).

Lemma 4's proof cites (b).

### B-O-4 (Opus, gap, low risk) — finding 4

> **Claim:** The formulas N₀ = max(2500, n, p), H₀ = ⌈512·2500/2500⌉, ℓ = ⌈log₂(n+p+1)⌉ and T₀ = max(1000, ℓ²), and the constants in the exact-branch condition, come from 00_COMMON §2 and cannot be checked in the packet. The H₀ expression as printed (2500/2500) does not show which of the two 2500s is N₀.

**Lead's answer: accepted and fixed in PROOF_v4.** The formulas are cited to 00_COMMON §2 lines 24–25 and METHODOLOGY §3 and §6.2, all quoted in Appendix B. H₀ is now written ⌈512N₀/2500⌉ = ⌈512·2500/2500⌉.

### Exposition findings, Stage B round 1 (handled in PROOF_v4)
- B-O-5 (no implementation named): §5.2 "Grid" now names one (test b first, then midpoint bisection), and notes that no bisection is ever used in either witness, so every implementation gives the same output.
- B-O-6 (reading of the output grid; the frozen-grid parenthetical): §4 (ii)(b) now states the reading explicitly and why it is the only consistent one; the parenthetical is the special case.
- B-O-7 (a) (the seven checks do not cover every inequality): §5.1 now lists the exact integer and rational facts separately. (b) (re^D and re^{2D} had no printed enclosure): the script now prints certified enclosures for both.
- B-O-8 (Z_c/P and α display identically): §5.3 notes that they differ (Z_c − A > 0, about 5·10⁻²² relative) and that their enclosures are disjoint.
- B-O-9 (B, C_b used before definition; |U| ≤ K step unneeded): Lemma 1 now argues m(U) ∈ (0, ∞) for every U ⊆ [p], without using the size cap.

## Stage B, round 2 — rulings on this log and review of PROOF_v4

- **Astra #2** (review/stageB_astra2_02_ruling_v4.log): agrees with the lead's answer on every logged item (A1-1..3, Stage A round 2, B-A2-1, B-O-1..9), and every fix works. No new or remaining findings. **Verdict: verified.**
- **Opus reviewer** (review/stageB_opus_02_ruling_v4.md): agrees with the lead's answer on every logged item, and every fix works. No fatal or gap finding. **Verdict: verified.** Three exposition notes:
  1. Provenance of the Appendix B quotes could not be checked from the packet. **Closed by the lead:** helpers/proof_build/check_appendix_B.py compares the quotes inside PROOF_v4.tex with the cited source lines. Result: 9/9 passages match, and both SHA-256 checksums in the proof equal those of the current files (output in helpers/proof_build/check_appendix_B_output.txt).
  2. The example implementation in §5.2 is a sketch. **No change:** the reviewer agrees that existence is not in doubt, and that no unspecified branch is reached in either witness.
  3. Lemma 1 extends the m formula to every U ⊆ [p], beyond the source's |S| ≤ K. **No change:** the reviewer rates it harmless; positivity is needed only where m is defined.

No fatal or gap finding is open. Astra judge not needed.

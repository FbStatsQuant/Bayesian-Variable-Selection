L2: VERIFIED-WITH-AMENDMENTS.
L3: VERIFIED-WITH-AMENDMENTS.
L4: VERIFIED.

No FATAL or MAJOR issue found. The amendments below correct an impossible feasibility sentence, imprecise normalisation language, and a probability-limit typo. They do not require strengthening the locked target's hypotheses. I relied on Corollary U as authorised and checked the other cited inputs against their stated hypotheses.

1. Location: lemmas/L3_NA_TL.md:12 (L3.0).
   Problem: “p + 1 ≤ K” is impossible because K = min(p, floor(n/2)) ≤ p. Taking n arbitrarily large never makes this assertion true. It is unnecessary: every set used here is a subset of [p], and an addition starts at k ≤ p − 1, so its result has size at most p.
   Severity: MINOR (a false setup sentence with a local repair, not a false NA/TL conclusion).
   Exact fix: replace “and p + 1 ≤ K (true eventually since p ≤ n^{α₀} ≤ n^{1/6})” by “and K = p (true eventually under (P), since p = o(n)); hence every A ⊆ [p] is feasible.” Keep the valid k ≤ p − 1 < K in line 35.

2. Location: lemmas/L2_sandwich.md:35–36 and 44–45.
   Problem: the explanation that “the score is invariant up to the 0.02 term” is imprecise. The pure RSS ratio is invariant under response scaling, but the ridge correction Q_A − RSS_A^y also enters the score. The actual cited GEN-L1 expansion handles both corrections, so the proof's use of its remainder is legitimate.
   Severity: MINOR.
   Exact fix: replace the explanatory language by: “GEN-L1 L1.3 gives log m(A) = c'_n − |A| log(n+1)/2 − ν log RSS_A + R_A, with RSS_A computed from unscaled Y and |R_A| ≤ κ_E uniformly on the block family. The change from scaled RSS_A^y to RSS_A contributes only to the common c'_n; both the ridge correction and 0.02 are included in R_A.” Use the same explanation in Remark (2). Do not describe the exact shipped score itself as scale invariant.

3. Location: lemmas/L3_NA_TL.md:78 (L3.3).
   Problem: the displayed lower bound for P(E_n ∩ E_Y) tends to 1, whereas the line ends “→ 0 complement.” Its intended meaning is recoverable, but the written limit is ambiguous/incorrect.
   Severity: MINOR.
   Exact fix: write “P((E_n ∩ E_Y)^c) ≤ 4/log n + 2/n + exp(−n/8) → 0,” or end the current lower-bound display with “→ 1.”

The following are the substantive checks behind the verdicts; no additional amendments are required.

For L2, the block-family re-proof closes without importing C-GROW's logarithmic bound on |Q|. Under fixed design, the actual partition is deterministic, the family contains the empty set, J = 16 is fixed, and |F_blk| ≤ 2^16 p ≤ 2^16 n^A. One may take C_F = 2^16, D = A and, for the residual vectors and all pairwise differences, C_V = 2C_F^2, D_V = 2A. GEN-L1 imposes no Gram condition on unions of members merely because their residual-vector differences appear in D_3. Its required Gram floor holds on each family member by (AG); its energy assumption is explicitly present. Thus the block events, uniform RSS floors, and bounded score remainders really are available.

The noise count in L2 is conservative and valid: at most 16·2^16 p ≤ 2^20 p add directions, each standard normal, gives the stated 1/log n failure bound with the two-sided Gaussian tail. For nested block models, GEN-L1 L1.4(b) applies because RSS_U ≥ RSS_{U+j} > 0 on the event. The gain in line 32 is eventually at least

  [M_n/(4C_R) − σ²(A+1)/C_R − A − 3/2] log n − O(1),

which is positive as M_n → ∞. This verifies positivity of the complete log-score gain, not just positivity of the RSS improvement. The branch k̃ = K does need K = p, and L2 explicitly assumes it. Under the locked (P), it holds eventually. Both good events are independent of the selected maximiser, so an arbitrary missing truth in any maximiser gives the same contradiction. Every-maximiser uniformity is valid; no union over maximisers is missing.

For L3.0, (E1) has the correct sign and factor 1/2: for each Gram eigenvalue g, log((g+1/(n+1))/(g+1)) lies between −log(1+1/g) and 0, hence between −1/g and 0. Principal-submatrix interlacing supplies g ≥ (n−1)φ² for every model. Empty models have zero remainder. The decomposition and PSD inequalities in (E2) are correct because all matrices involved are functions of G. They give exactly the stated bound on ω_A, and it is ≤ 2 once n is sufficiently large. The bounds are deterministic for all subsets, so exponential lattice size causes no loss.

The three E_Y bounds have the stated failure probability. For the last one, the Laurent–Massart threshold at x = n/8 is below 2n, since (n−1)+2sqrt((n−1)n/8)+n/4 < 2n. For every truth-containing T, P_T ≤ P_[p] and the signal residual vanishes. Subtracting the single full-design projection bound from the single total-noise lower bound proves (0.1) simultaneously for the whole lattice. Explicitly, η_n = [1+p+4sqrt(n log n)+2log n]/n → 0. No exponential union bound or lower bound on s_Y² is needed; its upper bound suffices.

For L3.1, the exact score difference in line 38 is correct. From (E1), −2(ρ_A−ρ_T) ≤ |A|/((n−1)φ²) ≤ (p+1)/((n−1)φ²); from (E2), Q_T−Q_A ≤ σ²Z²/s_Y²+2. Applying log(a/b) ≤ (a−b)/b and then using the positive envelope for the numerator justifies replacement of the denominator by RSS_A. The latter detail remains valid even if Q_T−Q_A happens to be negative. One can take η'_n = (1+0.02/n)/(1−η_n)−1. The additive ridge contribution is ≤ 4s̄²/σ² eventually. Although s̄² in the text depends on n, it is bounded by 2(sqrt(M)+σsqrt(2))² for n ≥ 2; thus C_ω is uniformly bounded and the final margin is valid. Alternatively use that fixed upper bound throughout.

The exact BB ratio is used correctly: for 1 ≤ k ≤ p−1, 2log((2p−1−k)/(k+1)) ≥ 2log(p/k)−2log 2. The endpoint maximisation giving α₀ is also correct: (1+κ̄s)²−s² = 1+2κ̄s+(κ̄²−1)s² increases on [0,1] when κ̄ ≥ 1, and its maximum is κ̄(κ̄+2). The displayed epsilon slack algebra preserves a fixed positive multiple of log n, uniformly in k. Choose α₁ explicitly in (max(0, limsup log p/log n), α₀).

All small terms in NA can be bounded by deterministic envelopes independent of T and l. In particular κ' ≤ κ̄/sqrt(ψ₀), the square-root difference in ε_n is O(sqrt(log log n)), ϱ_n = O((log p)^(1/4)+sqrt(log log n)), and the perturbation term tends to zero by (AG). Consequently ε_n = o(sqrt(log n)) for bounded, subpolynomial, or polynomial p allowed by (P). Bounded p ≥ 2 causes no division problem and has the same slack proof. For p = 1, s₀ ≥ 1 forces S₀ = [p] and NA is vacuous. The same reasoning covers sequences alternating between these cases. The proof does not need p → ∞.

For L3.2, the relevant noise directions are indexed by B = T\{i}, which need not contain S₀. Corollary U covers every subset, so its use here is legitimate, including B = empty. In that case its empty-set bound is dominated by the stated Z̄_n envelope. In the deletion case use only a and Z₁; b and Z₂ are needed only for swaps. The Schur-complement Gram floor gives a² ≥ (n−1)φ² and, for swaps, a²−b² ≥ (n−1)φ². Thus both displayed RSS comparisons are valid.

More explicitly, uniformly over T, i and l, the swap cross term divided by θ_i*²(n−1)φ² is at most 4σZ̄_n/(|θ_i*|sqrt(n−1)φ²), and the negative quadratic noise term divided by the same signal is at most σ²Z̄_n²/(θ_i*²(n−1)φ²). Both tend to zero under BM-∞ alone. The deletion bound similarly leaves at least one quarter of θ_i*²(n−1)φ² eventually. Division by s_Y² ≤ s̄² proves the common τ_n lower bound. This permits shrinking coefficients; it does not assume fixed θ* or a fixed positive lower bound on their magnitudes.

The TL log-ratio lower bound has the right direction: Q_A−Q_T ≥ τ_n−2 > 0 eventually, while 0.02+Q_T ≤ n+1.02. For t = (τ_n−2)/(n+1.02), log(1+t) ≥ t/2 for 0 ≤ t ≤ 1 and log(1+t) ≥ log 2 for t ≥ 1. Hence the penalty is much larger than log n whenever τ_n/log n → ∞, including the regime log n ≪ τ_n ≪ n. No assumption τ_n = o(n) is necessary, and it would be false in general for fixed nonzero signals. The determinant/prior costs are O(log n) uniformly, so the TL conclusion follows.

For L4, C-GROW L1.2 is a deterministic descent result requiring S₀ ⊆ Q and |Q| ≤ K, not |Q| = O(log n). Under (P), p ≤ n^α₁ eventually with α₁ < α₀ ≤ 1/6, whence K = p. Taking Q = [p] is legitimate. NA compares extra-removing swaps to the corresponding extra deletion, while TL excludes truth-removing neighbours; thus the stated deletion path and exact move count follow, including zero moves when the centre is S₀. The merged cap exceeds the required move count. These are statements about the prescribed completed deterministic LS0 search; output-run applicability is supplied by the named operational premises.

The [OP] inclusion transfers to this data-dependent cap because both the centre and the cap are deterministic given the data and prescribed tie rule, and completed scans contribute their scores to the all-scored set. Every-maximiser sandwich makes the weaker emitted-centre premise sufficient. The exact branch already scores S₀. T03♯'s fixed-sparsity, polynomial-p, eventual feasibility, energy and BM-∞ assumptions are present. Its anchored normalised eigenvalue conditions follow from the full Gram floor; its unnormalised floor follows from (n−1)φ² ≥ g₀ eventually, regardless of the tail-cutoff size. Finally boundedness of 1−π(S₀) turns convergence in probability into convergence of its expectation, without asserting an expectation rate. M5(0), [OP] and the final identity then yield exactly the claimed intersection probabilities and liminf statement. There is no implicit conditioning on output and no extra delivery assertion.

Numerical checks run independently:

Used py -3.13 with an inline NumPy script from C:\Users\felip\AppData\Local\Temp, seed 20261109; no numerical files were written. Used exact-Gram compound symmetry with p = 7, correlation 0.3, n in {80, 400, 2000}, eight Gaussian draws per n, σ = 1, and truth coefficients (1.2 n^(−0.2), −n^(−0.2)). Calculations took place in n−1 contrast coordinates, with XᵀX = (n−1)R, and used the exact shipped ridge score and BB prior. A conservative φ² = 0.25 was used.

Exhaustively checked all 128 subsets per draw: 3,072 model evaluations for (E1)/(E2), 1,920 lattice addition inequalities from L3 line 39, and 5,376 truth-deletion/swap score inequalities from line 71. Also checked the lattice RSS floor whenever E_Y held. Maximum positive violations were 0.0 for each of E1, E2, NA score envelope, TL score envelope and RSS floor. These are algebra/envelope checks, not finite-n claims that NA or TL must hold.

Evaluated the α₀ maximisation on 10,001 points in [0,1] for κ̄ in {1, 1.5, 2, 5}; all maxima agreed with κ̄(κ̄+2) to tolerance 1e−10. Confirmed the feasibility counterexample n = 1,000,000, p = 7, K = 7: p+1 ≤ K is false.

Read the author's FNA_summary.md, fna_check.py, D2_lattice.md and D2_summary.md; did not rerun their file-writing drivers. Their finite-n failures, including occasional failures below the target exponent, do not contradict an asymptotic theorem with a sequence-dependent onset. The numerical evidence does not replace the uniform proofs checked above.

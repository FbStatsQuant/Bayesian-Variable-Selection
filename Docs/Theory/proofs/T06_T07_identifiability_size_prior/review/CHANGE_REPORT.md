# Change report for the statement checker: T06 and T07

The original conjectures are `theorems/T06_A5_identifiability_ties.md` and `theorems/T07_A6_size_prior_ceiling.md`. The proposed precise statement is `STATEMENT.md`. Each item below says how STATEMENT.md departs from, or makes precise, the original wording, and why. Items marked **[necessary]** change what is claimed: the original wording would be false or undefined without them. The other items are readings that make an informal phrase precise, or harmless strengthenings.

## T06

1. (i) "for every standardised y" means every y in the contrast sphere 𝕊 = {y ∈ V : ‖y‖² = n − 1}, V = 1^⊥. This is exactly the set of standardised responses of valid inputs. Reading.
2. (i) "Equal column spans with unequal outer products need not tie" is proved in a stronger form: such pairs never have identical score functions (a consequence of the "only if" direction), and an explicit valid example of such a pair is given. Strengthening.
3. (i) "Under G and NIS, accidental exact ties among feasible models have probability zero" is read as P₀(∃ S ≠ S′ ∈ Ω : F(S) = F(S′)) = 0. It is proved in a stronger form: under G alone, almost surely every exact tie is between models with equal outer products. NIS then gives the stated clause. Reading plus strengthening.
4. (ii) "Under T03's hypotheses" is replaced by the explicit hypothesis H-T03: G, R, SE, BM-C (or BM-∞) in R1, together with the *conclusion* T03(i), 1 − π(S₀) = O_{P₀}(r_n). T03 is unproved, and the managing lead asked for it to be an explicit hypothesis. Only P₀(π(S₀) > ½) → 1 is used. "The tie rule is not invoked at S₀" is read as argmax_Ω F = {S₀}. The strict-maximiser part is proved deterministically on {π(S₀) > ½}, with no hypothesis. **[conditioning on a declared dependency (relabelled after the statement check): T03 is not a proved result, so (ii)(b) is conditional on T03]**
5. (iii) "Signed duplicate columns x_i = ±x_j" requires i ≠ j. "Relabelling" is the transposition τ = (i j). "Neither atom exceeds ½" is proved strictly (< ½), since π(∅) > 0. PIP_i = PIP_j is added (an immediate consequence). Reading plus strengthening.
6. (iii) Two-point bound. **[necessary]** "Every selector has maximal error ≥ Φ(−‖μ₁ − μ₂‖/(2σ*))" is false as literally stated for selectors that may use the raw mean of y^r.
   - μ_k = CX^rβ_k removes the intercept, but the raw data y^r also carry the intercept direction. Example: fix β₁, β₂ with supports S₁ ≠ S₂ and put α₁ = 0, α₂ = M. Then ȳ^r ~ N(α_k + x̄^{r⊤}β_k, σ*²/n). The selector "Ŝ = S₁ if ȳ^r is below the midpoint of the two means, else S₂" has both errors equal to Φ(−√n |M + x̄^{r⊤}(β₂ − β₁)|/(2σ*)) → 0 as M → ∞, while ‖μ₁ − μ₂‖ stays fixed (possibly 0).
   - The precise statement therefore gives two versions: (1) every selector, with the bound Φ(−‖m₁ − m₂‖/(2σ*)), where m_k = α_k1 + X^rβ_k is the full mean, and ‖m₁ − m₂‖ = ‖μ₁ − μ₂‖ exactly when 1ᵀm₁ = 1ᵀm₂, i.e. α₁ + x̄^{r⊤}β₁ = α₂ + x̄^{r⊤}β₂ (mean-matched; not α₁ = α₂); (2) every location-invariant selector (one that depends on y^r only through Cy^r), with Φ(−‖μ₁ − μ₂‖/(2σ*)) for any intercepts.
   - Version (2) covers everything the method computes: its target and outputs are functions of the standardised data. Randomised selectors are allowed. "Two Gaussian truths" requires distinct supports S₁ ≠ S₂ (otherwise a constant selector has error 0).
7. (iii) "Uniform recovery is impossible when ‖μ₁ − μ₂‖/σ* → 0" is read as follows: if, for each n, the class Θ_n contains such a pair with distinct supports, then liminf_n sup_{Θ_n} P_θ(Ŝ_n ≠ S₀(θ)) ≥ ½ for location-invariant selectors (or for all selectors with matched intercepts). The DUP(a) instance μ₁ = μ₂ is added as an example. Reading. It inherits the restriction of item 6.
8. (iii) "The near-duplicate reporting threshold is a warning, not an exact-identifiability statement" is made mathematical in two parts:
   - For i ≠ j, A∪{i} and A∪{j} have identical score functions iff |r_ij| = 1, so a reported pair with |r_ij| < 1 gives no such identity.
   - Exact score identities can occur with no reported pair (an explicit valid design with max |r_ij| = 1/√2).

   Reading: this gives the informal sentence a provable meaning.

## T07

9. (i) "Positive size-only prior on Ω" means w̃(k) > 0 for 0 ≤ k ≤ K. "A fixed tie order" means a fixed total order on subsets, used both for S†_w̃ and for S*_k, which is defined for 0 ≤ k ≤ p. When s₀ > K, {S† = S₀} is empty and the inclusion is trivial. "No size-only prior can repair a within-size likelihood ranking error" means: on {S*_{s₀} ≠ S₀}, S†_w̃ ≠ S₀ for every positive w̃. Reading.
10. (ii) "Minimises" means "is a minimiser". The 0–1 action space is all subsets of [p]; uniqueness holds iff argmax F is a singleton. For the MPM, uniqueness holds iff no PIP equals ½. The capped minimiser is a* ⊆ J₊, the ℓ = min(K, N₊) elements with the largest PIPs. Boundary ties are broken by a fixed deterministic rule, as the original says. Reading.
11. (iii) The original sentence ("these conclusions … do not automatically apply to Ŝ or to estimated PIPs, which need their computational guarantees") is informal. It is replaced by three exact statements that show precisely what transfer requires:
    - Ŝ = S† iff S† ∈ 𝒮, and Ŝ is a 0–1 Bayes action iff 𝒮 meets argmax F;
    - {Ŝ = S₀} ∩ {S*_{s₀} ≠ S₀} ⊆ {S*_{s₀} ∉ 𝒮};
    - the Hamming excess risk of plug-in decisions is ≤ 2 Σ_{â △ a_opt}|p̂_j − PIP_j| ≤ 2‖p̂ − PIP‖₁, and MPM̂ = MPM iff no coordinate crosses ½.

    The pointer to T21/T23/T26 stays as a remark; nothing from them is used. Reading (a formalisation of a caveat; no claim is weakened).


## Post-check note (2026-10-22)

The statement checker approved all 11 items, with required edits (review/STATEMENT_CHECK.md). Items 4 and 6 above are amended accordingly; the STATEMENT.md edits are listed in its §3.

LOCK-WITH-AMENDMENTS

Findings: FATAL 0; MAJOR 1; MINOR 3; NIT 0.

Scope: independent statement-lock review of STATEMENT v1.0 and PLAN v1.0 against the parent and the specific sources authorized by BRIEF_L01_sol.md. No other ticket material or reviews were read. No git operations were performed. The mathematical checks below are analytic derivations. The optional numerics source and saved output were inspected, but no numerical experiment was rerun.

## Findings

### F1 — MAJOR — The summary claims an expectation rate that its own corollary disproves

Place: `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:23` (table row R1).

The gain stated as “r_n exact in expectation for every p on the witnesses” is false over the announced witness class. For example, take fixed s₀ = 1, a deterministic standardized signal column with coefficient 1, and all other columns iid spherical, with p = ceil(exp(n^(1/3))). Then (E), (C), (W-sph-E), and Setting-E all hold: (log p)²/n = O(n^(-1/3)) and (r₀+1)log(pn)/n = O(n^(-2/3)). Corollary A1-E(a) itself gives

    E δ_n ≥ (1-o(1)) (2/√π) n^(-1/3),

whereas r_n = n^(-1/2)√log n. Thus E δ_n/r_n → ∞, and r_n cannot be an exact expectation rate for every allowed p. Even for fixed p, this ticket expressly says the upper half has not been checked (`STATEMENT.md:108-109`). The formal discussion there is appropriately narrower than the table.

Exact correction: replace the R1 gain by “the √log n expectation obstruction includes bounded p; r_n is exact where the quoted expectation upper bound applies.” Preserve the polynomial-p restrictions and random-design proviso in §4.1. Do not import the broader “exact for every p” wording from the motivating audit.

Status: refuted analytically by an admissible sequence; no numerical test needed. This is a summary overclaim, not a counterexample to Proposition A-E or A1-E.

### F2 — MINOR — The abstract truncation lemma has an incorrect equality

Place: `Theory_work/Wave3/W3-PSHARP-R/PLAN.md:19`.

The hypotheses allow unequal P(G_j). Independence of U_j from its own G_j gives

    E Y = e^(-e)c(E U) Σ_j P(G_j)
        ≥ e^(-e)cN(E U) min_j P(G_j),

not the displayed equality to the minimum. For example, N = 2, U_j identically 1, and event probabilities 1 and 1/2 give 3c/2 rather than c when e = 0. Both planned applications happen to have equal event probabilities, so the error does not invalidate their bounds.

Exact correction: replace the equality involving min_j P(G_j) by the equality to the sum followed by the lower bound above. Keep the second-moment bound and line 20 unchanged. Add T > 0 and c > 0 when invoking T = ϵ/c (the actual c_n is strictly positive).

Status: derived analytically; the corrected lemma suffices for both witnesses.

### F3 — MINOR — The spherical rank restriction is unnecessary in Corollary A2-E

Place: `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:87-90`; proof route at `PLAN.md:46-49`.

This is an optional strengthening at essentially no cost, rather than a false existing claim. For the spherical version of A2-E, retain (log p)² = o(n) but drop (r₀+1)log(pn) = o(n). Either antecedent in A2-E first implies E δ_n → 0. Parent Corollary B/B1, applicable to every design with the present cutoff and s₀ ≤ p/2, gives deterministically

    δ_n ≥ (s₀+1)/(3√n+s₀+1).

Consequently s₀ = o(√n). Since r₀ ≤ s₀ and log(pn) = o(√n) under (log p)² = o(n), the omitted rank restriction follows. One can then invoke the existing A2-E proof without modification.

Exact correction: at line 87 allow “(W-orth), or the spherical design/independence conditions of (W-sph-E) with (log p)² = o(n).” At the start of the proof, use parent B1 and the antecedent to recover the rank restriction before applying A-E. If the author prefers the present inherited hypothesis, explicitly record this removable restriction instead of suggesting it is needed for this corollary. This finding does not propose removing it from the general Proposition A-E.

Status: derived analytically, using the supplied parent statement only.

### F4 — MINOR — An expectation consequence of A2C is free

Place: `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:125` and `STATEMENT.md:97`.

“No expectation form of A2C” leaves out an immediate consequence; there is no additional fit-control problem for this implication. Since 0 ≤ π(S₀) ≤ 1, the displayed in-probability upper bound implies

    limsup E π(S₀) ≤ e^(-λ),
    liminf E δ_n ≥ 1-e^(-λ).

Indeed E π(S₀) ≤ e^(-λ)+η+P(π(S₀)>e^(-λ)+η); take limsup and then η ↓ 0.

Exact correction: append these consequences to A2C and replace “No expectation form of A2C” by “The expectation consequence of A2C follows by boundedness; no matching upper bound for E δ_n is claimed.” Alternatively say “No separate expectation claim is registered,” which avoids implying an unresolved mathematical extension.

Status: derived analytically. Optional strengthening, not a defect in the stated probability bound.

## Claim-by-claim checks

### Definitions, domains, uniformity, and Proposition A-E

Derived, for both witnesses. The imported p ≥ 2, n ≥ 3 and s₀+1 ≤ K make c_n positive, (2p-1-s₀)/p ∈ [1,2), c_n ≤ n^(-1/2), and ℓ_n ≥ (1/2)log n. In particular, with a fixed internal truncation parameter α > 0, T = α/c_n is eventually greater than 1 uniformly. N_n = 1, s₀ = 0, and fixed p are legitimate. The hypotheses are satisfiable, including when s₀ grows (coefficients can shrink).

For (W-orth), put U_j = exp(g_j²/2)1{g_j²≤2log T}. The centered Gaussian orthogonal decomposition really is

    E = g_j²+R_j,  R_j ~ χ²_(n-2),  R_j independent of g_j.

Although R_j includes other null scores, only independence of U_j from its own G_j is needed for the first moment. For the second moment, simply discard the indicators:

    Y² ≤ c_n²(Σ_j U_j)²,
    E Y² ≤ c_n²[N T E U + N(N-1)(E U)²]
          ≤ c_n²[N T E U + N²(E U)²].

The U_j themselves are independent. No independence between different G_j, or between U_k and G_j for k ≠ j, is required. Thus the potentially problematic dependence through V causes no gap. On the proposed event, the parent V bound yields the stated exponent loss, which vanishes because log T = o(√n) and x_n can tend to infinity with x_n log T/√n → 0. Also E U = 2√(log T/π) exactly.

For (W-sph), the conditional joint law of the entire score vector (ζ_j)_j given ε is a fixed product law. This establishes joint independence of that vector from ε, not just marginal independence. The proposed common G is ε-measurable. The parent density argument, at τ = 2log T, gives exactly

    2√(log T/π)(1-1/d)exp(-2(log T)²/d)
      ≤ E U ≤ 2√(log T/π)exp(3log T/d).

The new logarithmic and rank restrictions ensure both sphere comparison and the exponent loss are uniform and vanish. The event probability tends to one by the displayed bounds. With c_n T = α, the corrected Lemma T gives E δ_n ≥ L(a_n-α-L), where a_n → 1 uniformly and L = c_n N E U.

Finally,

    log T = ℓ_n + log(α(2p-1-s₀)/p)

differs from ℓ_n by a bounded quantity depending only on α. Hence L/Λ_n^E → 1 uniformly, including bounded N and p. Taking α smaller than the final ϵ and using slack gives (1-ϵ-Λ_n^E)Λ_n^E; when Λ_n^E ≥ 1-ϵ the asserted inequality is trivial. The claimed n₀ dependence is justified if “same o(·) sequences” means common deterministic bounds/moduli for the displayed normalized logarithmic quantities. There is no additional dependence on a lower bound for N_n. Without common moduli, a uniform n₀ over all little-o sequences would not follow; the text explicitly supplies common sequences.

The conditional random-(X_{S₀},θ*) clause follows by conditioning and integrating the uniform inequality. As in the parent, 𝒜_n must be measurable with respect to the conditioning variables and the conditional hypotheses include the specified noise/null-block law. With the deterministic p, S₀ and null-block size stipulated in Setting-E, Λ_n^E is deterministic and can be factored out as written.

### Corollary A1-E, including (a) and (b)

Derived. All-null orthogonality implies p ≤ n-1+s₀-r₀, so its new log-p restriction is automatic. For fixed s₀, Λ_n^E → 0 on both witnesses. If p → ∞, 2(p-s₀)/(2p-1-s₀) → 1. Polynomial p gives ℓ_n = (a+1/2)log n+O(1), yielding √((a+1/2)/π). Fixed p gives ℓ_n = (1/2)log n+O(1), yielding the full displayed finite-p multiplier times 1/√(2π). These checks include p = s₀+1 within the imported p ≥ 2 domain. The clipped orthogonal p at a = 1 has the same logarithmic asymptotic.

### Corollary A2-E (i) and (ii)

Derived under the stated assumptions. Sub-blocks preserve both witness classes. Their Λ increment is Δ_n = 2c_n√(ℓ_n/π) → 0. For nonempty sub-blocks with Λ bounded by 1/4, Proposition A-E at ϵ = 1/2 gives the proposed lower bound. If the selected interval contains only block size zero, its advertised right-hand side is nonpositive and the inequality follows from δ_n ≥ 0; the proof should state this harmless case rather than apply A-E to an empty block. Thus E δ_n → 0 forces Λ_n^E → 0. For s₀ ≤ p/2, 2(p-s₀)/(2p-1-s₀) is bounded below by a positive constant, proving (i). The small-Λ conclusion and ℓ_n ≥ (1/2)log n then prove (ii). See F3 for the removable spherical rank assumption.

### Proposition A2C

Derived. For any feasible J of null columns, orthogonality makes each determinant multiplier exactly n and every Q decrement additive. Therefore Σ_J γ_k < 1 and

    π(S₀∪J)/π(S₀)
      = [w(s₀+j)/w(s₀)] n^(-j/2)(1-Σ_Jγ_k)^(-ν)
      ≥ c_n^j Π_(k∈J) exp(νγ_k).

The lower bound on the prior ratio is in the correct direction. On the parent κ event each factor dominates e^(-ϵ/2)W_k with W_k ≤ N. For a_k = c_n W_k, the elementary-symmetric inequality in PLAN follows by bounding the weight of ordered j-tuples with a repeated index via the union over their C(j,2) colliding pairs:

    j! e_j(a) ≥ A^j-C(j,2)B A^(j-2),
    A=Σa_k, B=Σa_k².

Treat j = 1 directly. Lemma W gives A ≥ (1-o_P(1))Λ_n and E A = Λ_n = O(1), so A = O_P(1). Moreover B ≤ (c_n N)A = o_P(1): bounded Λ_n and log N → ∞ imply (s₀+1)/√n → 0. For each fixed j the collision error vanishes. Choose a fixed finite truncation large enough for the desired η, then small ϵ and large n; this avoids any need for an unproved growing-j uniform estimate.

The cutoff does not obstruct that truncation: s₀ = o(√n), n/2-s₀ → ∞, and p-s₀ → ∞, hence K-s₀ → ∞. Summing the fixed-degree bounds yields e^λ-1. The λ = 0 case is immediate. The two probability formulations are equivalent as families quantified over every η > 0; a literal same-η event identity is unnecessary. See F4 for the expectation consequence.

## Faithfulness, citations, and the optional numerics

- The “taken unchanged” references in §1 point to the announced parent definitions, setting, witnesses, and claims. The cited parent proof steps supply the reductions actually used; the new truncation and collision arguments still need to be written, as the delta acknowledges.
- The §6 A1-E implication row is correct: for fixed s₀ and p → ∞ the parent's spherical conditions imply (W-sph-E), since log(p-s₀) ~ log p and r₀ is bounded. On the orthogonal witness the new log-p restriction is automatic. The limiting multiplicity and ℓ_n ≥ log p eventually recover the parent's expectation lower bound.
- The §6 A2C implication row is correct on its expressly restricted finite positive critical-scale slice: choose η less than the gap e^λ-1-(1-ϵ)λ. It does not supersede the parent's full growing-s₀ statement.
- The formal corrected readings in §4.1 and §4.2 are supported. For log p = o(log n), the expectation lower bound rules out a universal expectation upper bound of order √((1∨log p)/n) on the applicable witnesses. It supplies no such exclusion in probability. The polynomial-p expectation comparison keeps the parent's upper-bound provisos, and fixed-p upper bounds are explicitly left unchecked. F1 concerns the broader summary table only.
- The fixed-p numerical script uses the correct orthogonal D_S and Q_S, enumerates all models where K=p, and applies the correct Gaussian importance weights. Its saved n=10^6 ratios agree with the reported 0.99–1.03 range. This is an inspected Monte Carlo illustration with stated standard errors, not an asymptotic proof or certified enclosure; no stronger numerical conclusion was used here.
- The extra logarithmic conditions are sufficient for the present general A-E route: the orthogonal route uses (log T)²/n → 0 and the spherical route uses that condition plus (r₀+1)log T/n → 0. For a proper orthogonal block p can be much larger than n, so the rank bound on N alone does not establish the log-T condition. Removing these restrictions from the general A-E proposition would require another argument, not simply the parent's log-N proof. The all-null orthogonal restriction is automatic, and F3 identifies the immediate spherical-corollary weakening.

No counterexample to the formal new propositions or corollaries was found. Amend the false table summary and the abstract-lemma equality before locking; F3 and F4 are inexpensive scope improvements.

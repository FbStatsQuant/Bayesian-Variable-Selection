# T8 blind Sol read: ruling on its two points

Input: `T8/CODEX_gpt-6.2-sol_adv.md` on `origin/theory/PRE-LEAN` (FLAWS-FOUND, 2 points, with evidence trail). Sources read at origin/main ad29c22e.

## Point 1 (`W3-START2-R/STATEMENT.md:237`, FLOOR needs s₀ < K)

Same as Astra's T8-2. Ruling unchanged: AGREE with the staged patch. Two independent Codex reads and the Theorem 5 walk now agree on it.

## Point 2 (`W3-START2-R/STATEMENT.md:167-188`, TRANSFER: ϱ_n, b_n(h), R^♯_n must be total measurable functions of the design)

**Ruling: AGREE. It is a totality convention, Lean-compile in kind; not a flaw in the mathematics.**

- **What is true in Sol's point.** TRANSFER allows any design law. On a realisation with no retained column, p = 0 and the averages p⁻¹Σ_{l∉Q}(…) that define 𝔏_n and 𝔏^♯_n are 0/0; this can happen with Q = S₀ = ∅, where the statement says R^♯_n is given by the displayed formula. The inherited convention (BASE `W3-START/STATEMENT.md:301-305`) sets only 1 − π₀(𝓛(Q)) and o₀ to 0 there, not these three functions. Yet the statement calls them "random variables" and clauses (a2), (a3) take limits in probability of them.
- **Why it is not a flaw.** Clause (a1) is stated on admissible designs, where |S₀| < p forces p ≥ 1 and everything is defined. In (a2) and (a3) the admissible event has probability tending to 1, so the conclusions do not depend on how the functions are extended off it.
- **Recorded span affected: yes, wording only.** The convention sentence at `:187-188` lies inside `W3-START2-R:TRANSFER`'s span (`:167-188`). The change is EQUAL on admissible designs. Theorem 5 (START-R) cites the same convention ("also in (b)") and is unchanged.

### Exact fix

1. `W3-START2-R/STATEMENT.md:187-188`. Replace
   "*Convention off the admissible designs:* as BASE `:301-305` (also in (b))."
   by
   "*Convention off the admissible designs:* as BASE `:301-305` (also in (b)); in addition ϱ_n, R^♯_n and b_n(h) are set to 0 on realisations where their defining expressions are not available (no retained column, or h not a level vector for Q). With this they are measurable functions of X^r on the whole design space (`lemmas/R4_TRANSFER_COR.md`, Measurability), and no clause changes on admissible designs."
2. `W3-START2-R/lemmas/R4_TRANSFER_COR.md:16-18` (the Measurability paragraph). Append the argument below.

### The measurability argument (proved, not assumed; short and standard)

The extension is a definition; what has to be proved is that the extended functions are measurable.

- **The set where the formulas are available is Borel.** D_n := {p ≥ 1} ∩ {h is a level vector for Q}. {p ≥ 1} is a finite union of the sets {Cx_j ≠ 0}, which are open. Q and S₀ take finitely many values and are measurable (Q by hypothesis; S₀ = supp β on the retained columns), so the space splits into finitely many measurable cells on which Q and S₀ are constant; on a cell, {1 ≤ h_l ≤ z_n for all l ∉ Q} is a finite intersection of measurable sets.
- **On each cell inside D_n the functions are measurable.** They are finite sums and finite maxima of J_h(δ_{U,l}, τ_U) over fixed index sets; this is the paragraph already in the proof file. Its two ingredients are standard: (i) the projection P_U is a Borel function of the design, being the pointwise limit of the continuous maps X_U(X_UᵀX_U + λI)⁻¹X_Uᵀ as λ ↓ 0; (ii) J_h(d, t) is an integral of a jointly measurable nonnegative integrand, hence measurable in (d, t, h) by Tonelli.
- **Gluing.** A function that is measurable on each of finitely many measurable cells and equal to 0 on the measurable complement is measurable.

Mathlib names verified in the pinned checkout: `Measurable.piecewise`, `Measurable.ite`, `Measurable.comp`, `measurableSet_le`, `measurableSet_lt`, `Measurable.find`. For the two ingredients I have not looked up names: a pointwise limit of measurable maps into a metric space is measurable, and the parameter-integral fact is the measurability clause of Tonelli.

Nothing here is a supremum over an uncountable set, and no selection is involved.

## Process

The edit rides on the START2-R re-freeze that T8-2 and T8-3 already need (one re-freeze for the three). Statement text changes in the TRANSFER span, so that row takes a patch bump like START-R's.

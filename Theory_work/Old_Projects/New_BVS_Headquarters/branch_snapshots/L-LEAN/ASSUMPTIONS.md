# ASSUMPTIONS (L-LEAN)

Readings taken where the brief, the protocol or the sources left a choice. Each is the most reasonable reading; change any of them by editing the statement files and this list.

## Process
- A-P1. **Location.** The HQ brief puts everything under `theory_campaign/L-LEAN/` on branch `theory/L-LEAN`. That overrides the Lean protocol's default project location (OneDrive `Lean_4\<Project>`) and its work copies under `C:\lean\work`. The Lake package is `theory_campaign/L-LEAN/SmcBvs/`.
- A-P2. **Mathlib.** The shared copy `C:/lean/packages/v4.35.0-rc2` (Lean `v4.35.0-rc2`, Mathlib rev `065356127b1dc0016f66b7283ce0ce2c4055aa55`) is used through `packagesDir`, as in every project on this laptop. `lake-manifest.json` and `lean-toolchain` are copied from `C:\lean\work\L0_elementary`. Nothing was downloaded, and the BNP library was not touched.
- A-P3. **Agents.** The HQ caps are at most 3 helpers at once, Opus or Sonnet at effort high. They replace the protocol's design department, co-coders, and Haiku/Sonnet helper budget. There was no 5-agent Sol review round, because the code is small and HQ set agent sizes; the lead's review, `stmtdiff`-style freezing and `#print axioms` stand in for it. Fable and Astra are used for the fidelity check (the protocol's main risk control).

## T21
- A-T21-1. **Abstract probability space.** The joint law `P` of data and algorithm randomness is a probability measure on a sample space `Ω`. The paper's `E₀δ₁` is written `∫ δ₁ dP`. These are equal because `δ₁ = 1 − π(S₀)` depends on the data only and the data marginal of `P` is `P₀`. The Lean statement allows `F` to depend on all of `ω`, so it is more general.
- A-T21-2. **Tie rule.** "Ŝ = argmax of F over 𝒮 with a fixed tie rule" is formalised as "on `Uᶜ`, `Ŝ ω` is a maximiser of `F ω` over `𝒮 ω`" (`IsArgmax`). Every tie rule satisfies this, the method's included (`IsLeastArgmax → IsArgmax`). C1 never uses the tie rule (PROOF_v3 line 68: "no tie").
- A-T21-3. **Model space.** The model space `Ω = {S : |S| ≤ K}` is an arbitrary `A : Finset M`, with `𝒮 ω ⊆ A` on `Uᶜ`. The regression score formula is not used by C1, so `F` is an arbitrary real score.
- A-T21-4. **Measurability.** The decomposition inequalities need none (outer measure). C1 with `2Eδ₁` assumes each `ω ↦ F ω S` is measurable, so that `δ₁` is integrable.
- A-T21-5. **Routes (a)–(f) and the asymptotic H03 consequences** are not formalised. This is the "abstract, finite" version the brief asks for. The one asymptotic ingredient (`E δ ≤ ε + P(δ > ε)`) is formalised as a finite inequality.

## T07
- A-T07-1. **Tie order** `≺` is an injective rank `rk : Finset (Fin p) → ℕ`. Every total order on a finite set has this form, and PROOF_v2's Remark "the tie order" states that any fixed total order works.
- A-T07-2. **(ii) and (iii).** `F` is an arbitrary real score on models and `π = e^F/Z` on `Ω` (0 off `Ω`). (iii)(b) uses `F = log(pw(|S|)·m(S))` with `pw > 0` on `0..K` and `m > 0`. That is the paper's `F = log(ϖ m)` with `ϖ(S) = w(|S|)/W_K`.
- A-T07-3. **(iii)(c).** The action class `𝒜` is any finite set of subsets. The paper uses `2^[p]` or `Ω`; both are instances.

## T11(iii)
- A-T11-1. **Conditioning on 𝓒.** Given `𝓒`, the count `Q = Q_f`, the model `S*` and `π₀` are fixed. The draws are independent with law `π₀` (EX-S, CAL, START: STATEMENT.md "Setting"). The Lean statements are the unconditional identity for fixed `Q`, `S*`, `π₀`, applied pointwise in `𝓒`. A regular-conditional-probability version is not formalised.

## T37(i)
- A-T37-1. **Abstract core.** States form an arbitrary type, with neighbourhood `N`, score `F` and potential `Φ : α → ℕ`. The greedy map is any best strict-improvement map (any tie rule; one exists for every rank). In TD′_P, closure of `R` under the greedy move is a hypothesis. For the concrete `R_{a,d}` it is W1 Lemma 2(a) (`T37Lattice.lean`, if completed).
- A-T37-2. **Production search.** It is modelled as `path M S_c ℓ`, the greedy iterate capped at `ℓ` moves (a state with no improving neighbour is a fixed point). "Certified" means `M (returned) = none`. The scored set of the search is the centres plus their scanned neighbourhoods.

# T38: Two-regime consistency of the reported HPM (main theorem)

**Status:** NEW conjecture, added 2026-10-28. It is a composite statement written by HQ from:
- Fable's Change A (`../FABLE_REVIEW.md` §1);
- Astra's delivery critique (`../ASTRA_REVIEW.md` §1–2).

It replaces T26(iii) as the paper's main HPM theorem. Read with `../../theorems/00_COMMON.md`.

**Category / rank:** core; the headline theorem.

## Why it is needed
T26 reaches the HPM through start concentration (T22(iii)). That regime does not need the sampler. In the masked regime (T27) the start gives the truth vanishing mass, and T26 says nothing. Both consultants found the same gap: **a repair theorem (T24 or T37) repairs an eligible particle or centre, but it does not deliver one.** The main theorem must contain the delivery step.

## Setting and assumptions
- **Asymptotic setting.** A triangular array with s₀ fixed, p_n ≤ n^A, B ≤ 16 and K_n = ⌊n/2⌋. The v3 budgets N_n, ℓ_n, L_n and T_n are indexed by n, as in master §I.8.
- **One statistical family.** All statistical premises must hold *jointly*, for the actual data-dependent block partition, on one family of designs.
- **Optional method tweak LS0.** Also run the local search from the start mode S̃₀.
  - It is deterministic and costs about ℓ·p extra scores.
  - It can be added after the fact to existing fits: the HPM is the best model ever scored, so extra scoring can only raise the reported HPM's score.
  - It is needed only if eligibility cannot be proved otherwise.

## Precise statement
By T21,

P(no output or Ŝ ≠ S₀) ≤ P(U) + 2E₀[1 − π(S₀)] + P(Uᶜ, S₀ ∉ 𝒮),

and T03 sends the middle term to 0. The discovery term P(Uᶜ, S₀ ∉ 𝒮) → 0 in each of two regimes:

- **(a) Favourable regime.** Under T22(iii)'s hypotheses (EXP′, VIS, NL), Q_f π₀(S₀) → ∞. The fresh iid start draws then score S₀ by T11(iii).
- **(b) Masked regime.** π₀(S₀) may vanish as in T27, but the start puts mass π₀(𝓡_d) ≥ b_n on the near-truth region. This follows from T22(i) with a reference S° ∈ 𝓡_d, which need not be S₀. Then one of two routes applies:
  - **(b1)** TD(d, 0) holds with probability → 1 (T37), and some local-search centre lies in 𝓡_d with probability → 1. Either the best-scored model before the final search lies in 𝓡_d, or the start mode S̃₀ does and LS0 is used.
  - **(b2)** T24's conditions hold, and a particle in 𝓡_d is available at the terminal rounds.
- **(c) Cost corollary.** The expected number of score evaluations is polynomial: O(N_n T_n (p + B + 2) + ℓ_n p) under the declared budgets. Arithmetic costs follow from T32.

Hence P(Ŝ = S₀) → 1 − limsup P(U).

## Not claimed
- Evidence or PIP accuracy in the masked regime. Those are T26(i)–(ii), favourable regime only.
- Any result about fits selected for having completed.
- Comparative superiority over other methods.

## Main risks
- **Eligibility in the masked regime.** Showing that the best-scored model, or S̃₀, lands in 𝓡_d.
- **Compatibility.** T22(i)'s reference bounds may not be compatible with T27's masking hypotheses on the same family.
- **Move budget.** At n = 200, ℓ_n is smaller than s₀ + d.
- **Fallback.** If (b) fails for the original method, use T39, the explicit repair-track extension.

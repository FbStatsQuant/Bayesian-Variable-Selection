# T39: Independent start-to-terminal scoring tracks with an explicit budget (contingency)

**Status:** NEW conjecture, added 2026-10-28 as a **contingency target**. Source: Astra's C37 (`../ASTRA_REVIEW.md` §2), renumbered T39.

**Category / rank:** contingency. Use it only if T38(b) cannot be proved for the original method.

**Method change.** This is a genuine algorithm extension. The existing 2,400 fits did not run it, and it would need separately labelled validation runs.

## Setting and assumptions
- **Repair tracks.** The exact target, the actual block start and the terminal hybrid kernel, plus M independent *scoring-only* repair tracks.
  - Each track starts from an exact π₀ draw and runs h rounds at φ = 1.
  - Their scores update the reported HPM. They do not feed the SMC particles, calibration, evidence or PIPs.
  - They use separate random streams, and all budgets are fixed before they run.
- **Data event.** On a data event G_n with probability ≥ 1 − δ_n:
  - π₀(𝓡_d) ≥ b_n > 0;
  - inf_{x∈𝓡_d} K₁(x, S₀) ≥ a_n > 0;
  - sup_{x∈𝓡_d} P_x(one-round first exit) ≤ η_n.
- **Sources of the bounds.** T24 or T37 supplies a_n and η_n. T22(i) supplies b_n from a reference in 𝓡_d, which need not be S₀.

## Precise statement
Let s_n = 1 − (1−a_n)^h − hη_n > 0.

**Miss probability.** Conditional on data in G_n, for the potential uninterrupted tracks,

P(S₀ never scored) ≤ (1 − b_n s_n)^M ≤ e^{−M b_n s_n}.

**Budget.** Each track uses at most 1 + 2mh score evaluations, where m = p + B + 2. Choose:
- h = ⌈log 4 / a_n⌉, with hη_n ≤ 1/4;
- M = ⌈2 b_n⁻¹ log(1/ε_n)⌉.

The miss probability is then ≤ ε_n.

**Error bound.** Together with T21,

P(no usable output or wrong HPM) ≤ P(U) + 2E₀[1−π(S₀)] + δ_n + ε_n.

**Polynomial cost.** If b_n ≥ n^{−r}, a_n ≥ n^{−s} and η_n = o(a_n), the expected cost of discovery is C_setup + O(p n^{r+s}) score evaluations.

## Main risks
- **The value lies in the inputs.** The probability argument is elementary. The research work is a compatible statistical family with useful b_n and a_n, ideally one where T27 holds, so that direct iid discovery is expensive, while b_n and a_n stay bounded below.
- **T24's factorial constant** may make the guarantee impractical.
- **Role of tempering.** If the tracks explain essentially all of the selection gain, the paper must say what tempering contributes.

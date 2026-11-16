# T7 · Lemma KER (the coded moves are the stated kernels; the round order is uniform) — STATEMENT v2 (draft, not locked)

Track A item T7 (`AUDIT.md` §6; CHECKPOINT_1 annex order 7). Tier B (second-seat re-check of N9 rows 1–5 against the code
of record). **Lean target: yes for (KER-b) (detailed balance of four finite kernels and the uniformity of Fisher–Yates);
no for (KER-a), (KER-c)** (code correspondence). Blocks rows 3.5, 3.6.

## Source of the premise
- "**KERNEL** the four coded step functions and the order realise the T12 §1 kernels and a uniform state-independent
  order (N9 rows 1–5, … status PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT)"
  (`Theory_work/Wave1/W1-N1/STATEMENT.md:76-78`).
- T12 §1 kernels and round (`Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md:23-31`); N9 rows 1–5
  (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/N9-KERNEL/REPORT.md:17-21`), proofs
  (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/N9-KERNEL/PROOF.md:59-197`), code-checked at 39db138.
- `W3-SAMP:ST` uses "every kernel K on Ω with πK = π" for the coded steps at φ = 1
  (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:118-124`).

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core). `cpp/v3_engine.h` up to line 373 (step functions, order,
round, resampling, island) and `cpp/v3_blocks.h` (neighbour graph) are identical at 39db138 and at the pin (`git diff
39db138 4676af6`: the only engine hunk starts at line 374, `local_search`; no hunk in `v3_blocks.h`).

## Setting
A run's engine at temperature φ ∈ [0, 1]: p, K, B (T2 BLK-a), the neighbour graph N = `Nb` built once in `cpp_setup`
(`cpp/v3_core.cpp:302`) from X only, `st` of T4. γ_φ(S) := γ₀(S)e^{φd(S)} on Ω, d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b).
EX-A; H-U (the step's uniforms are fresh i.i.d. U[0, 1)); START-X (T6) for the independence proposal.

## Lemma KER
- **(KER-a) Code = T12 kernels.** For each label — Gibbs coordinate j (`step_gibbs`), uniform swap (`step_uswap`),
  neighbour swap N1..NB (`step_nswap`), independence proposal (`step_indep`) — the coded step maps the current state S
  and fresh uniforms to the next state with exactly the transition law of the T12 §1 kernel of that label at φ; the
  Gibbs step's pre-draw value `oj` is T12's o_j(S, φ). No step leaves Ω.
- **(KER-b) Reversibility (math half).** Each of the four kernels is γ_φ-reversible on Ω (detailed balance), hence leaves
  q_φ = γ_φ/Z̄_φ invariant. The neighbour graph N is symmetric, loop-free and duplicate-free; symmetry and duplicate-freeness are what the
  proposal ratio uses.
- **(KER-c) Order.** Each round (`one_round`) first draws an order by Fisher–Yates with m − 1 fresh uniforms, before any
  step, where m = p + B + 2 is fixed for the run; under H-U the order is uniform on the m! permutations and independent
  of the particle's state; the steps are then applied in that order, each with fresh uniforms.
- **(KER-d) Inputs fixed before the islands.** N, B and `st` are built from the data before any island, and the score
  function S ↦ log m(S) is fixed by the data; none of them depends on particles; the only state-dependent quantities in a step are its own feasibility rules and
  |N(j) ∖ S|, |N(l) ∖ S′|, which (KER-a) covers.

## Not claimed
- Binary64 and the 2⁻⁵³ grid (N9 PROOF §5, REPORT §4; not re-checked).
- N9 row 6 (self-adjointness of a random-order round) — not part of W1-N1's KERNEL premise.
- Mixing of any kind.

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (re-states N9 rows 1–5 for the pin) | track A T7 | `AUDIT.md` §6 T7 | `CHECK.md` |
| v2 | (KER-b) graph properties; (KER-d) scores | EQUAL (exact wording) | LC3 T7 #2, #3 | `reviews/LC3_reply_opus.md` | pending (gate) |

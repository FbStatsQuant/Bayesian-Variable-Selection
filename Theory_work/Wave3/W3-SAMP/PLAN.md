# W3-SAMP · PLAN (v2, after SL1)

## Route (proof sketches; full proofs go to lemmas/ after the lock and the sharpness gate)

1. **CC (code)** — done by the lead in `lemmas/CC_code_check.md`; checked by the LC reviewer against the code.
2. **Theorem D** — CC1 + CC4: the draws are iid π₀ given 𝓒 (stopping-time positions in an iid uniform stream; START);
   P(no draw = S₀) = (1 − π₀(S₀))^{D_r}. CC2 + CC5: if S₀ ∈ 𝓜 and π(S₀) > ½ then F(S₀) > F(S) for all S ∈ Ω∖S₀, so the
   hpm_better-maximum of 𝓜 is S₀. Integrate over 𝓒 and data. Independent of the bridge and of Ẑ.
3. **Lemma MR** — T12 (i.a)–(i.c), (ii) for fixed c (with W1-N1's code bridge L1, valid on main up to the removed
   plain-PIP lines: CC header); then a short extension of W1-N1's freezing lemma L3 from endpoints to the augmented path
   record (bridge stages, terminal endpoints, pre-step states) using its evidence bound.
3b. **Lemma PC** — completed ⇒ no guard return in any island (`v3_engine.h:335-337`, `v3_core.cpp:451-453`), so each
   island record is the potential one; caches/ledger do not feed transitions under EX-A (W1-N1 L1); reported fields are
   functions of these records.
4. **Lemma ST** — (a) from πK = π: π(S₀)K(S₀, S₀ᶜ) = Σ_{S≠S₀} π(S)K(S, S₀) ≤ π(S₀ᶜ). (b) explicit Gibbs: the move from S₀ at
   coordinate j goes to S₀ ⊕ j with probability π(S₀⊕j)/(π(S₀)+π(S₀⊕j)) (0 at the cap), and these targets are distinct.
   (c) first-exit decomposition over the m steps of the round with the order a bijection; U, I and each of the B copies of
   N via (a); Gibbs via (b).
5. **Theorem LT♯** — deterministic decomposition |p̂_r(j) − 1_{S₀}(j)| ≤ κ₀ + B̄ + Λ̄ (B̄ = mean fraction not at S₀
   entering the measured rounds; Λ̄ = mean fraction entering at S₀ that leave during the round); E[W_r B̄] = δ (MR);
   E[Λ̄] ≤ λ₀ (ST, unweighted); Markov on {W_r ≥ η}. Pooling by the triangle inequality; MPM by the ½-threshold; HPM by CC2.
   Asymptotics by bounded convergence.
6. **Theorem C** — deterministic product lower bound; Hölder for the bridge odds; MR at each stage; a stopping-time
   argument (first t with Σ_{s≤t}(1 − A^{br}_s) > u) that turns the stagewise weighted bounds into E[min(U, ½)] ≤ 2(T+1)δ̄
   (improves BLIND_fable's T²δ̄ to Tδ̄); mean-one argument for E|W − 1|; then LT♯ with η = ½.

## Pipeline (PROTOCOL Wave 3)

Statement lock (Codex gpt-6.1-sol, high) → ASSUMPTION_MAP.md + boundary-violation numerics + "better theorem" review
(gpt-6-astra, high) → HQ-visible record in LOG/CHECKPOINT → proofs (lemmas/) → lemma-by-lemma falsification numerics +
cross-family check (Sol high) → independent mid-point (Astra high, statement + proofs only) → exhaustive sweep (Sol high) →
citation check (`reviews/CITECHECK.txt`) → council (gpt-6-astra high + Claude Opus 5.5 high on claudeAgent), ≥ 8.0 both,
all six gates, ≤ 3 rounds.

## Numerics plan (local, small; Python 3.13 + numpy)

Exact/MC implementation of T12's island on a small Ω (p ≤ 6) with arbitrary positive γ₀, d (the kernels are defined for any
such pair), plus regression-generated targets:
- MR / LT identities (weighted means of B̄, Λ̄-free RB error) by Monte Carlo with many islands;
- ST bounds exactly (kernel matrices);
- C: E|W − 1| vs the bound 18Tδ̄, and the boundary T·δ̄ ≫ 1 (is the T factor needed? expected: no → `improvable`);
- LT: an example where P-CONC holds but NC fails and the RB PIPs / MPM are wrong (NC cannot be dropped), and an example
  where NC fails yet PIPs are right (NC is not necessary);
- D: equality of the draw-miss probability; boundary D·π₀(S₀) → 0 with S₀ found by other moves (sharp for draws, not for
  the method).

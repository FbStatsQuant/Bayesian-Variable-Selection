# T12(i.a): abstract statement and Lean plan

Source: `Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md` §§1–3. The claim is (i.a): for every set of frozen parameters `c`, every `t ∈ {0,…,T}` and every `f : Ω → ℝ`, `E_c[Ẑ_t q̂_t(f)] = Z_t q_t(f)`. In particular `E_c[Ẑ] = Z`.

## Abstract statement (finite state space)

- State space: a finite type `α` (the feasible models Ω).
- Unnormalised targets: `γ_0 > 0` with `γ_t = γ_{t−1}·G_t` (`G_t = e^{Δ_t d}`). `Z_t q_t(f) = Σ_x γ_t(x) f(x)`.
- Round kernels: `K_t` is a row-stochastic kernel that leaves `γ_t` invariant: `Σ_x γ_t(x) K_t(x,y) = γ_t(y)` (method §6.5; every elementary step is `q_t`-invariant).
- Island I(c) with `N` particles:
  - stage 0: `N` iid draws from `π_0 = γ_0/Z_0`, with `Ẑ_0 = Z_0`;
  - stage `t`: `Ẑ_t = Ẑ_{t−1}·(1/N)Σ_k G_t(X^k_{t−1})`; multinomial ancestors; one `K_t` round per particle.
- Claim: `E[Ẑ_t · (1/N) Σ_i f(X^i_t)] = Σ_x γ_t(x) f(x)`.

## What is in Lean now (`SmcBvs/T12Core.lean`, no `sorry`)

1. `invariance_step`: `Σ_x γ_{t−1}(x) G_t(x) (K_t f)(x) = Σ_y γ_t(y) f(y)`.
2. `resample_move_step`: the resample–move algebra for a fixed population. The new evidence times the mean of the mixture marginals `Σ_k (G_k/ΣG) K(x_k,·)` equals `Ẑ (1/N) Σ_k G_k (K f)(x_k)`.
3. `unbiased_of_step`: the induction. Stage 0 gives `E_0 f = Σ γ_0 f`, and the recursion `E_t f = E_{t−1}(G_t · K_t f)` then gives `E_t f = Σ γ_t f` for every `t`.

The recursion `hstep` is an explicit hypothesis of (3). It is the only probabilistic content of (i.a).

## TODO: derive `hstep` from a probabilistic model

Plan (estimated at 300–600 lines):

1. Model the island as a `PMF` on populations. The state at stage `t` is `(x : Fin N → α, Ẑ : ℝ)`; the type is countable once `Ẑ` is restricted to a finite set of reachable values, or the evidence can be carried as a function of the history. Simplest route: carry the full history `Fin (t+1) → (Fin N → α)` and define `Ẑ_t` as a deterministic function of it, so that only `PMF (history)` is needed.
2. One step: given population `x`, the next population has law `PMF.pi`-style iid draws `i ↦ (ancestor ~ Categorical(G(x_k)/ΣG)) >>= K(x_ancestor, ·)`. Mathlib has no `PMF.pi`, so either build it as `Measure.pi` on a finite type or define the joint law by `Finset.univ.prod`.
3. Linearity of expectation over `PMF` (finite sums), plus the marginal of each coordinate of the product law, gives `E[(1/N)Σ_i f(Y_i) | x] = Σ_k (G_k/ΣG) (K f)(x_k)`. Then `resample_move_step` gives `hstep`.
4. Stage 0, iid `π_0`: `E[(1/N)Σ_i f(X_i)] = π_0(f)` and `Ẑ_0 = Z_0`, so `E_0 f = Σ γ_0 f`. With the stage-0 flag set, apply `invariance_step` with `G ≡ 1` once more.
5. Instantiate `γ_t = γ_0 e^{φ_t d}` and `K_t` = the round kernel. The invariance of the round kernel (a random order of `γ_t`-invariant elementary steps) is a separate lemma: a composition and a mixture of invariant kernels are invariant.

Estimated effort: one focused session. The main cost is the product-law plumbing in step 2.

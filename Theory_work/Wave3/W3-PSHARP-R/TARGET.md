# TARGET.md — W3-PSHARP-R (one page; PROTOCOL_v4 §3.2, RIDER_RULES §2)

Target statement: `STATEMENT.md` v1.1, locked (delta over W3-PSHARP), claims `W3-PSHARP-R:AE` (Prop A-E, Cor A1-E, Cor A2-E)
and `W3-PSHARP-R:A2C`. These are sharpness records (lower bounds): a hypothesis is read as "does the record survive
without it", not "is it needed for an upper bound". Reader version: `READER_DELTA.md` (PROTOCOL_v4 H6).

## 1. Assumption map — changed hypotheses only (all others: PARENT `ASSUMPTION_MAP.md:9-17`, unchanged)

| hypothesis | where it enters | how | property used | necessity reading | signal |
|---|---|---|---|---|---|
| N_n ≥ 1 (was N_n → ∞), AE | Lemma T (PLAN §2.1) | truncation at T = ϵ/c_n; E U² ≤ T·E U; no weak law needed | one null column already gives E[min(c_n e^{χ²₁/2}, 1)] ≈ 2c_n√(log(1/c_n)/π) | NONE: N_n = 1 is the boundary and is covered; numerics N1 at p = 2 (N = 1) | none |
| (log p)² = o(n) added to (W-orth) for a general null block (AE) | κ-bound, PLAN §2.2 | (1 − κ_n) log T → 0 with log T ≈ ℓ_n ≤ log p + ½ log n | exponent coefficient → 1 faster than 1/log T | ARTEFACT of the route; automatic for 𝒩 = [p]∖S₀ (p ≤ 2n) and inside regime R1 (p ≤ n^A); beyond it Λ^E_n is tiny anyway (N_n ≤ n) | artefact-threshold (harmless) |
| (W-sph): log N_n → log(pn) in both growth conditions (AE) | Lemma W(ii) at τ = 2 log T; κ′-bound | sphere density vs normal on t² ≤ 2 log T; (1 − κ′_n) log T → 0 | as PARENT rows :16-17 with T for N | ARTEFACT (as PARENT :16-17); with s₀ fixed reduces to (log p)² = o(n), i.e. the parent's scope for 𝒩 = [p]∖S₀ | artefact-threshold |
| (W-sph-E) rank condition dropped in A2-E [L01-F3] | A2-E, first step | PARENT B1 gives s₀ = o(√n) from E δ_n → 0 | — | NONE for A2-E | none |
| s₀ ≤ p/2 (A2-E) | sub-block step, PLAN §2.5 | per-column increment of Λ^E ≤ 2√(ℓ_n/(πn)); 2N/(2p−1−s₀) ≥ ½ | multiplicity ≍ p | cosmetic (any s₀/p ≤ θ < 1 works with other constants) | none |
| Λ_n → λ, s₀/p → 0, (W-orth) (A2C) | multi-step sum, PLAN §2.6 | exact D-ratio n^j and additive fit on orthogonal blocks; e_j ≈ e₁^j/j! | independent scores, max weight ≪ sum | witness; (W-sph) version needs multi-step fit control (not attempted) | unharvested on (W-sph) |

Conclusion level: negative / lower bound. Rate: (s₀+1)·[2N/(2p−1−s₀)]·√(log(p√n/(s₀+1))/(πn)) for E δ_n (AE);
e^{−λ} cap on π(S₀) in probability (A2C). Scope: orthogonal null block (any p with (log p)² = o(n); p ≤ 2n when all
nulls) or spherical null block (p ≫ n allowed); bounded p and bounded N included in AE.

## 2. Parity table (per changed clause)

| clause | (a) PROGRAM goals (design-agnostic; p ≫ n; method as coded) | (b) closest published | (c) our best registered (PARENT `W3-PSHARP:A`@1.0.0) |
|---|---|---|---|
| A-E: E δ_n ≥ (1 − ϵ − Λ^E_n)Λ^E_n, every N ≥ 1 | witness classes (lower bounds need a witness); p ≫ n via (W-sph); coded prior, exact π — matches | no published lower bound of this form known to us (PARENT `ASSUMPTION_MAP.md:33-36`; audit f02 `:31`); the upper-bound literature uses per-variable penalties p^{−c}, not comparable — n/a | **beats**: PARENT has no expectation claim for a general block, and none for bounded N |
| A1-E(a): constant √((a+½)/π) for E δ_n | matches (same sequences as PARENT Remark A3) | — | **beats** PARENT :72 (√(a/π)); factor √(1 + 1/(2a)) |
| A1-E(b): E δ_n ≥ (1 − o(1))C_{p,s₀} r_n at fixed p, C_{p,s₀} = (s₀+1)[2(p−s₀)/(2p−1−s₀)]/√(2π) (a lower bound of order r_n; no upper bound claimed) [R1-F1] | matches | — | **beats**: PARENT makes no claim at fixed p (Cor A1 needs p → ∞) |
| A2-E: E δ_n = O(r_n) ⇒ s₀ = O(1), every p | matches | — | **beats** PARENT :77, :104, :109 (log p ≍ log n needed there) |
| A2C: limsup π(S₀) ≤ e^{−λ} on (W-orth) | short of design-agnostic (one witness; reason: multi-step fit control on (W-sph) is new work) | — | **beats** PARENT :75-77 (1/(1 + λ)); compare Cor B critical cap e^{−λ/2} (PARENT :101-102), which holds on every design |

No "short" row on a target clause except A2C's scope (reason given; (W-sph) version is a named open item).

## 3. Boundary numerics
- N1 `numerics/ae_fixed_p.py` → `ae_fixed_p_out.txt`: the dropped hypothesis N_n → ∞ at its boundary (N = 1, 2, 3, 4;
  p fixed), exact orthogonal design, n = 10²…10⁶, E δ_n by importance sampling (MC s.e. ≤ 5·10⁻⁴ relative). E δ_n/Λ^E_n
  = 0.935 → 0.990 (p = 2), 0.99 → 1.01 (p = 3), 1.01 → 1.02 (p = 5); against the parent's normaliser the ratio grows
  1.7 → 3.1 (∝ √log n). So the new constant is attained numerically at fixed p (not claimed).
- Planned (optional): N2 p = n − 1 (constant √(1.5/π)); N3 A2C cap e^{−λ}.

## 4. Better-theorem review
Not run (RIDER_RULES §3.2: the blind sharpness audit sharp2/f02 served as the better-theorem input). Dispositions of
f02's proposals for Claim A: (1) expectation for every p — **adopted** (AE); (3) e^λ − 1 on (W-orth) — **adopted** (A2C);
(2) dropping (G) under (W-sph) and (4) a coherence witness — **named open items, parked** (BRIEF).

# W1-T38E — REPORT: delivery and eligibility for T38(b)

Run of 2026-11-02, branch `theory/W1-T38E`. Full proofs are in `PROOF.md`; scripts and outputs are in `scripts/` and `*.out`. Every result is a **candidate pending cross-family review**.

## Headline

1. **The composition T38(b) is PROVED given named inputs** (Theorem T38(b)-R, PROOF §7): liminf P(Uᶜ, Ŝ⁺ = S₀) ≥ 1 − limsup P(U). The brief's "P(Ŝ = S₀) → 1 − limsup P(U)" is not a well-formed limit; this is the corrected form. The repair step enters only as a black box (TD′ or REPAIR).
2. **Delivery to the terminal rounds (route b2) is OPEN, and the candidate ingredients provably do not suffice.**
   - COUNTEREXAMPLE C1 (reproducible SMC): start mass on A ≈ 1, uniform bridge mass on A ≥ 0.9997, zero exits from A. Yet every particle of A dies in 99.5% of islands at N = 10⁶ (48% at N = 10⁵).
   - The T15 route needs an evidence lower tail. That tail fails in **every** island of C1, including the islands where A survives. It fails exactly when particles cross late, which is the masked case.
   - Route (b2) therefore needs a particle-level hypothesis: SHARE (Prop. D3) or the lower tail LT (Thm D1).
3. **Two routes avoid delivery and are PROVED.**
   - **D2 (original method, no tweak):** if a one-flip neighbour x° of S₀ has start mass > 1/10, the *pilot's first round* scores S₀ w.p. → 1. It uses the pilot's own ESS rule through a new deterministic share lemma (Lemma S, tight) and the SR Gibbs scoring. This covers one-cancellation masking at every p ≲ n^A, including p ≫ √n, where iid discovery fails.
   - **E3 (LS0 tweak):** if the start mode S̃₀ is in a greedy basin (for example π₀(x°) > ½ for some x° ∈ 𝓡_d), a local search from S̃₀ scores S₀ deterministically. S̃₀ is computable exactly by max-plus convolution.
4. **Eligibility of the best-scored model without LS0 cannot come from the brief's sufficient condition.** E1 (PROVED, deterministic) shows F(S₀ ∪ P) ≥ F(S₀) − (d+1)[log 2p + ½ log(n+1)]. Under omission (T27) masking, some state outside 𝓡_d therefore beats the reference S° w.p. → 1 (CF2: by 38–172 nats).
5. **T37's TD(d,0) is false for d ≥ 1 in proxy-rich designs** (reproducible). The swap "proxy → missing truth" beats the plain addition by ≈ ½ log n + log p. Greedy still repairs, so the right black-box input is reachability TD′. **Escalate to W1-T37R.**
6. **Compatibility: no obstruction for route (b1) + LS0.** The explicit family CF(c) satisfies jointly G, R, SE (exact for n ≥ 1,626), BM-∞, T27 masking (iid discovery misses w.p. ≥ 0.86 at n = 1600, c = 2), T22(i)-type start mass on 𝓡₀, eligibility S̃₀ ∈ 𝓡₀, and TD′. T27's H3 *implies* the start premise of (b). CF has p = n^{3/4} < n; a p ≫ n family is CONJECTURE.

**Recommendation to HQ.**
- State T38(b) with (b1)+LS0 as the main masked-regime route, and D2 as the no-tweak route for one-flip masking.
- Keep (b2) as a conditional theorem with SHARE named as its crux.
- Replace TD(d,0) by TD′.
- T39 (repair tracks) is not needed for the HPM if LS0 is accepted. LS0 is a much smaller method change: one deterministic local search, which can be added post hoc.

## Refined statements (full proofs in PROOF.md)

**Lemma A (PROVED).** γ_φ = γ₀^{1−φ}γ₁^{φ}. Hence γ_φ(S′)/γ_φ(S) ≤ max of the endpoint ratios, and every Gibbs change probability at any φ ∈ [0,1] is ≤ max{κ₀, κ₁}(S,l).

**Lemma B (PROVED, deterministic).** For d < m, references x, y, and a good/bad split of true contents:
sup_φ q_φ(𝓡_d^c) ≤ θ/(1−θ) + max{π₀(𝔅), π(𝔅)}/[min(π₀(x), π(y))·max(π(x), π₀(y))],
where θ is a uniform two-endpoint extra-addition ratio over good classes and 𝔅 = {N > m} ∪ {bad U, N > d}.
COUNTEREXAMPLE C0: the naive set version of T22(iv) is false (q₀(A) = q₁(A) = 0.993, q_{1/2}(A) = 9·10⁻⁵).

**Lemma S (PROVED, tight).** For weights with ESS ≥ eH and a subset of fraction f, the weighted share is ≥ f − √(f(1−f)(1/e−1)). Population ESS is non-increasing in φ.

**Theorem D2 (PROVED).** Hypotheses:
- EX-A, EX-S, SR;
- x° Δ S₀ = {j};
- π₀(x°) ≥ b > 1/10;
- a data-measurable 𝒟 with |𝒟| ≤ k_D and Dep = Σ_{l∉𝒟∪{j}} max(κ₀,κ₁)(x°,l);
- NB: the initial pilot d-range ≤ T_e log 1.925 unless S₀ was drawn.

Conclusion: P(S₀ ∉ 𝒮_cal) ≤ e^{−2Ht²} + P(NB^c) + exp{−H(1−Dep)₊ g(b−t)/(k_D + B + 3)}, with g(f) = f − √(f(1−f))/3 and H = H₀ ≥ 0.2 max(n,p).

**Theorem D1 (PROVED from locked T15).** P_𝓒(no 𝓡_d particle of island r at τ) ≤ π(𝓡_d^c)/c + P_𝓒(Ẑ_r/Z < c).

**Proposition D3 (PROVED, conditional).** P(no 𝓡_d particle after stage T) ≤ (1−π₀(𝓡_d))^N + Σ_t(ζ_t + η_t), under SHARE(ζ) and EXIT-end(η).

**Proposition E1 (PROVED, deterministic).** F(S∪P) − F(S) ≥ −|P|[log 2p + ½ log(n+1)]. Hence F(S₀) − F(S°) > κ_n(d) implies that some S ∉ 𝓡_d beats S°.

**Theorem E3 (PROVED).** Under TD′(𝔅, ℓ), S̃₀ ∈ 𝔅 implies that LS0 scores S₀. Further, π₀(x°) > ½ with x° ∈ 𝓡_d implies S̃₀ = x°. LS0 costs ≤ (ℓ+1)·max_k[p + k(p−k)] scores.

**Theorem T38(b)-R (PROVED given inputs).** Route (b1): ELIG + TD′. Route (b1′): D2. Route (b2): DELIV + REPAIR(a_n, L+4). Each, together with H-T03, gives liminf P(Uᶜ, Ŝ⁺ = S₀) ≥ 1 − limsup P(U).
**Cost corollary:** a deterministic polynomial ceiling given T32(i) (itself an unlocked conjecture), plus LS0's term.

## Evidence (all fixed seeds; Python 3.13 with numpy/scipy)

| check | file | result |
|---|---|---|
| C0 set-transfer failure | `toys_C0_C1.out` | q₀(A) = q₁(A) = 0.9933, inf q_φ(A) = 9.1·10⁻⁵ |
| C1 extinction | `toys_C0_C1.out` | A extinct in 0.480 (N = 10⁵) and 0.995 (N = 10⁶) of 200 islands; median log Ẑ/Z = −1817 and −1930; Ẑ/Z < ½ in 100% |
| Lemma S | `share_lemma_check.out` | worst slack −1.1·10⁻¹³ over 2·10⁵ cases; equality in two-level cases |
| CF1/CF2 start law, LS0, TD, GP, D2 | `cf_family.out` | see PROOF §8 table; LS0 scores S₀ in all 4 configurations; D2 bound 3·10⁻⁹ (n = 400), 1·10⁻⁶ (n = 1600) |
| GP(2) failures | `gp_fail_probe.out` | 4 states (two proxies replace x₃); all reach S₀ in 3 greedy moves |
| E1 margins, SE | `cf_extra.out` | F(S₀) − F({1}) = 44.5, 180 ≫ κ_n(d) = 16–30; λ_min(R) = 0.024, 0.015 |

Exact enumeration: start law by exact convolution (all p); TD/GP by exhaustive enumeration of 𝓡_d (up to 29,936 states) with all flips and swaps scored. The full posterior π was not enumerated (p = 89 and 252 exceed p ≤ 20); π(S₀) → 1 rests on locked T03.

## What fails and why

- **T15/LT route in the masked regime.** LT is equivalent to the particle system tracking the mode switch. When the crossing is late, Ẑ/Z ≈ 0 even if delivery holds (C1).
- **Bridge mass ⇒ delivery.** False (C1). Selection can wipe out the 𝓡_d sub-population before the within-𝓡_d kernel moves.
- **Lemma A for exits** is useless at states missing a truth that has proxies (φ = 1 odds e^{Θ(n)}). D2 handles this by excluding a bounded set 𝒟; EXIT-end in general must use actual-φ odds.
- **The ESS share lemma over many stages.** The share loss compounds as √ε grows linearly (ε_t ≈ (t/6)²), so the pilot's ESS control gives single-stage delivery only.
- **Brief's eligibility condition F(S°) > sup_{𝓡_d^c} F.** False w.p. → 1 under omission masking (E1).
- **T37 TD(d,0), d ≥ 1.** False (swap dominance; §6.4); GP(2) also fails at 4 states, but reachability holds.
- **D2 beyond Gibbs distance 1.** Needs a crossing temperature, so it is the delivery problem again.

## Needs escalation

1. **W1-T37R:** replace TD(d,0) by TD′ (or GP(d)). Report the swap-dominance counterexample and the true-variable-deletion-by-two-proxies paths.
2. **HQ / Felipe:** adopt LS0 (local search from the exact start mode) as the masked-regime route. It is a method change, but deterministic, cheap and post-hoc applicable. Label any fits rerun with it.
3. **HQ:** route (b2) needs SHARE or LT, a particle-system property. Decide whether to keep (b2) in the paper as conditional, or drop it in favour of (b1)+LS0 and D2.
4. **Felipe:** D2 relies on SR (both Gibbs configurations scored). The engine does this (`step_gibbs`), but the inventory still lists SR as "to be confirmed".
5. **T38 text corrections:**
   - the limit form;
   - the cost formula (scans have k(p−k) swaps; the number of searches is O(ℓ²));
   - "ℓ_n < s₀ + d" should read "path length |S̃₀ Δ S₀| ≤ ℓ_n + 1";
   - T27-H3 already implies π₀(𝓡_d) ≥ c₀ (no separate T22(i) premise is needed when S^{(0)} ⊆ S₀).

## Outside scope (not attempted)

- Masked-regime evidence and PIP accuracy (T38 does not claim them).
- Proof of TD′ or REPAIR (W1-T37R, W1-T24G).
- Proof of T32(i).
- A p ≫ n compatibility family.
- Reviewing the preliminary n = 200 data. It is consistent with D2/C1-type reasoning: Gibbs scores S₀ early, so local search has nothing left to repair. This is unverified.

## Confidence cards

| target | statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| Lemma A | log-linear odds domination | 0.99 | done | — | no |
| Lemma B | structured bridge mass on 𝓡_d | 0.95 | done (deterministic); asymptotic instance 0.5 | start extras tail, d > c(A+½)/κ − 1 | no |
| Lemma S | ESS share lemma | 0.99 | done | — | no |
| D2 | pilot one-flip discovery | 0.9 | done; statistical instance (Dep, NB) 0.6 | Dep at x° off a bounded proxy set; NB | no |
| D1 | T15 delivery | 0.98 (as implication) | done | LT, which fails in the masked regime | no |
| D3 + SHARE | terminal delivery in masked regime | 0.6 (that SHARE holds in realistic BVS designs) | 0.15 | selection vs within-𝓡_d progress; C1 | no (but unprovable as is) |
| E1 | brief's eligibility condition fails | 0.95 | done (deterministic); margin sketch 0.85 | T03 margin for S° ⊉ S₀ | no |
| E3 + LS0 | LS0 eligibility | 0.97 | done | needs TD′ and π₀(x°) > ½ | **yes, minor (LS0)** |
| T38(b)-R | composition | 0.97 (given inputs) | done | the inputs | (b1) yes-minor; (b1′), (b2) no |
| CF compatibility | one family satisfies (b1)+LS0 premises | 0.85 | 0.7 for an asymptotic proof (TD′ on CF, H2 two-sided) | uniform TD′ on CF; p ≫ n version | no |
| T37 TD(d,0), d ≥ 1 | holds w.p. → 1 | 0.05 | — | swap dominance | — |

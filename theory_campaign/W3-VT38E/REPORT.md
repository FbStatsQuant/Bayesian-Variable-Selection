# W3-VT38E — REPORT: adversarial verification of W1-T38E

Run of 2026-11-02, branch `theory/W3-VT38E`. Object of review: `origin/theory/W1-T38E`, commit 436a712, folder `theory_campaign/W1-T38E/` (REPORT.md, PROOF.md, BRIEF.md, five scripts). All scripts of this run are in `scripts/` with fixed seeds; their outputs are saved as `scripts/*.txt` (not `*.out`, which the repository's `.gitignore` drops). Every verdict below is a **candidate pending cross-family review**.

## 1. Headline

1. **No fatal error found.** Each of the following checks out line by line against the spec, the engine and the locked results: the composition Theorem T38(b)-R, Lemma A, Lemma B, Lemma S, Theorem D1, Proposition D3, Theorem D2, Proposition E1 and Theorem E3. The proofs as written are correct, with one small constant error in D2 (item 2). Everything here is **PROVED given its stated inputs**, but several results are close to restatements of their inputs; see §5.
2. **One ERROR, cosmetic and repaired.** D2's no-blow-up event uses the ratio 1.925, but 4r/(1+r)² = 0.899993 < 0.9 at r = 1.925. The right constant is r* = (11 + 2√10)/9 ≈ 1.924951. With that constant D2 is PROVED. A sharper repair replaces the hypothesis NB by the event actually needed (§3.1).
3. **COUNTEREXAMPLE C1 is confirmed, after a repair.** W1's toy kernel is not reversible (its proposal is asymmetric and has no Hastings factor). With a properly γ_φ-reversible kernel, extinction of every particle in A still happens: in 56% of islands at N = 10⁵ and in 100% at N = 10⁶ (200 islands each). C0 is confirmed exactly.
4. **W1's finding that TD(d,0) fails is VERIFIED, and it is stronger than W1 states.** TD(d,0) fails for **every** d ≥ 1 in **every** design on the event π(S₀) > ½, because at (S₀∖j)∪{l} the swap l→j beats the addition of j. So T37(iii) is false under T03's own hypotheses (PROVED, two lines, §3.4); proxies play no role. Numerically, every one of the 174/500/747/258 states of this form fails, in all 16 configurations.
5. **The numerical evidence is reproduced** with independent code on W1's exact design, matching to every reported digit, and on three independent designs. The reproduction also shows four reporting GAPs:
   - The "D2 bound 3·10⁻⁹ / 1·10⁻⁶" is only one of D2's three terms. The full bound is 2.2·10⁻⁷ at n = 400 and 1.6·10⁻⁵ at n = 1600.
   - The CF(1) instances used for D2 are **not masked**: iid discovery succeeds there.
   - "iid miss ≥ 0.86" holds for the tier-0 final run of W1's single design. It is 0.64–0.86 across designs, and 0.001–0.09 at tier 1.
   - "CF satisfies jointly …" is finite-n numerics at n ∈ {400, 1600}. The asymptotic joint claim for H3, ELIG and TD′ is a CONJECTURE.
6. **The engine models the method faithfully** for every step the proofs use. One implementation caveat for HQ: LS0 must emit its centre as a score event (§4).

## 2. Verdict table

Legend: VERIFIED = every step checked; GAP = a step is missing or overstated (fixable unless said otherwise); ERROR = a false step (with counterexample). "Engine" = `Scripts/SMC_BVS/core/cpp`.

| claim (W1 label) | verdict | evidence / reason |
|---|---|---|
| **T38(b)-R composition**: liminf P(Uᶜ, Ŝ⁺ = S₀) ≥ 1 − limsup P(U) via routes (b1), (b1′), (b2) | **VERIFIED** (PROVED given inputs) | Steps (1)–(6) checked: strict maximiser when π(S₀) > ½; Markov; bounded convergence; LS0 deterministic; terminal rounds have no reweighting or resampling (engine `run_island_s`); smallest-index eligible particle is measurable, then fresh randomness. GP(d) with ℓ+1 ≥ s₀+d ⇒ TD′(𝓡_d, ℓ) also checked (§3.5). Caveat §5.1: (b1) is nearly a restatement of TD′. |
| Brief's limit form "P(Ŝ = S₀) → 1 − limsup P(U)" is ill-posed | VERIFIED | trivial |
| Cost corollary (c) | VERIFIED as an upper bound, conditional on unlocked T32(i) | It counts 2m scores per round and 8ℓ+3 local searches. The engine does ≤ m and ≤ 2ℓ+3, so the formula is loose but valid. |
| **Lemma A** (Gibbs change probability ≤ max endpoint odds) | VERIFIED | Proof checked against `step_gibbs` (heat bath, cap). Exhaustive check: 2,048,000 (state, label, φ) cases, 0 violations (`v6_lemmaB_enum.txt`). |
| **C0** (endpoint bound does not transfer to sets) | VERIFIED (COUNTEREXAMPLE) | q₀(A) = q₁(A) = 0.99331; inf q_φ(A) = 9.0792·10⁻⁵ at φ = ½, equal to the closed form 2e⁻¹⁰/(1+2e⁻¹⁰) (`v2_toys_C0_C1.txt`). |
| **Lemma B** (structured bridge mass on 𝓡_d) | VERIFIED (deterministic) | Peeling (k+1 representations), Hölder, affinity bound all checked. Exhaustive check: 40 small exact instances, 3,255 (d, m, partition, x) cases with θ < 1, 0 violations, max LHS/RHS = 0.59. Its asymptotic reading is a PROOF SKETCH, not checked here. |
| **Lemma S** (ESS share lemma, tight) | VERIFIED | Cauchy–Schwarz proof checked. 300,000 adversarial cases (smallest-weight subsets, three weight laws): worst slack −1.5·10⁻¹⁴. Two-level weights attain the bound. g increasing on [0.1, 1), g(0.1) = 0. ESS non-increasing in φ (2,000 random d vectors, 0 violations). |
| Kantorovich companion "ratio ≤ 1.925 ⇒ ESS ≥ 0.9H" | **ERROR (cosmetic, repaired)** | 4r/(1+r)² = 0.8999927 at r = 1.925. Two-level weights {1, 1.925} give ESS/H = 0.8999927 < 0.9. Repair: r* = (11+2√10)/9 = 1.9249506 (`v1_share_ess.txt`). |
| **Theorem D2** (pilot first round scores S₀) | **VERIFIED after the constant repair** (PROVED) | Every modelling assumption matches the engine: uniform Fisher–Yates order fresh per particle and round; SR (`eval(tmpQ)` of the flipped configuration, offered to the HPM); `pilot_next_phi` (≥ test, lo passes, floor φ+1/T_e); initial draws scored; multinomial resampling. Step 5's union bound is valid because the order is independent of the step uniforms. |
| D2's reported numbers (3·10⁻⁹ at n = 400, 1·10⁻⁶ at n = 1600) | **GAP (reporting)** | These are only the term exp(−Hβg(b)), with t = 0 and NB ignored. Recomputed: Dep = 0.0910 and 0.0487, β = 0.0454 and 0.0297 (W1 values reproduced). The full bound min_t[e^{−2Ht²} + exp(−Hβg(b−t))] is 2.2·10⁻⁷ and 1.6·10⁻⁵. Simulated P(NB^c): 0/100 per design at n = 400; n = 1600 in `v4_d2_pilot.txt`. |
| D2 mechanism, simulated end to end | VERIFIED | Engine-faithful simulation of the pilot's first stage (iid π₀ draws, pilot rule, multinomial resampling, full random-order round with all four step types). S₀ was scored in stage 1 in 100/100 replications for each of 3 designs at n = 400; 98% of the S₀ hits came from Gibbs flips. The per-round hit probability from x° is 0.96, 0.95, 0.88, 0.43, 0.37 at φ = 0, 0.03, 0.1, 0.3, 1, always ≥ β = 0.045 (`v5_d2_round_prob.txt`). |
| "D2 covers one-cancellation masking … including p ≫ √n where iid fails" | **GAP (overstated)** | The theorem covers it **conditionally** on Dep < 1 − c₁ off a bounded set, NB and π₀(x°) > 1/10. None of these is proved for any family as n → ∞. In every CF(1) instance used (n = 400, 1600, 4 designs), π₀(S₀) = 9.6·10⁻⁵ to 2.2·10⁻³, and the tier-0 iid miss is 0.000. Those instances are therefore not masked. Masking of CF(1) is asymptotic only (β = −¼; it needs n of order 10¹⁵ at these constants). |
| **Theorem D1** (T15 route) | VERIFIED | Immediate from locked T15 with u ↑ 1. |
| **C1** (extinction despite start mass, bridge mass and zero exits) | **VERIFIED (COUNTEREXAMPLE) after kernel repair** | W1's kernel: extinction 0.450 (N = 10⁵) and 1.000 (N = 10⁶), vs W1's 0.480 and 0.995, within MC error. Reversible kernel: 0.560 and 1.000. Reversible kernel with 5 moves per stage: 0.550 and 1.000. Ẑ/Z < ½ in every island. π₀(A) = 0.999955, sup_φ q_φ(A^c) = 3.30·10⁻⁴, d(o) − d(a₁) = 80, all reproduced. |
| W1's C1 kernel is a valid SMC move | **GAP (fixed)** | The ends propose m w.p. 1 and m proposes each end w.p. ½, with no Hastings factor, so the kernel is not γ_φ-reversible. Fixed with a lazy symmetric proposal. The conclusion is unchanged. |
| **Prop. D3** (forward chain under SHARE, EXIT-end) | VERIFIED (PROVED, conditional) | First-failure decomposition; the smallest-index resampled 𝓡_d particle is measurable; its round uses fresh randomness. Note SHARE is nearly the conclusion itself (§5.2). |
| **Prop. E1** (deterministic loss bound) | VERIFIED | (a) Q_S as a ridge minimum: re-derived. (b) Schur/Woodbury ratio 1+(n+1)a vs 1+b with a ≤ b, so the D ratio is ≤ n+1: re-derived. (c) w(k+1)/w(k) ≥ 1/(2p). Numerically, F(S₀∪P) − F(S₀) ≥ −κ_n(d) held in all 48 (design, d) cases (`v3_cf_checks.txt`). |
| E1's consequence (brief's eligibility condition fails under omission masking) | VERIFIED (deterministic part); margin = PROOF SKETCH | At n = 1600, F(S₀) − F(S̃₀) = 109–180 ≫ κ_n(2) = 29.7 in all 8 designs, and an outside-𝓡_d state beats S̃₀ in every one of the 16 configurations. One n = 400 design (seed 2, c = 2) has a margin of 17.2 < κ(2) = 24.5, yet an outside state still beats S̃₀ by 7.8. |
| **Theorem E3** (LS0 eligibility) | VERIFIED (PROVED) | (i) is trivial (two states cannot both have mass > ½). (ii) cites locked T22(i) correctly. (iii) cites T27 H3 correctly. LS0 cost ≤ (ℓ+1)max_k[p + k(p−k)]. Max-plus computation of S̃₀ re-implemented: S̃₀ = {1} in all 16 configurations, and LS0 scores S₀ in all 16. |
| **T37 TD(d,0) fails for d ≥ 1** | **VERIFIED and strengthened** | TD(1,0) failures on W1's design: 248/352 (n = 400) and 728/1004 (n = 1600), identical to W1. TD(2,0): 26,019/29,936 identical. Every failure is a "missing truth + extra" state except one superset state. New: failure is universal on {π(S₀) > ½} (§3.4). |
| GP(d) and TD′ in CF | VERIFIED numerically (finite n) | GP(0), GP(1): 0 failures in all 16 configurations. GP(2) at n = 400, c = 2: 4 failures (W1 design, matching W1) and **149** (independent design seed 1). In every failure the production local search from that centre still scored S₀, so TD′(𝓡₂, ℓ) holds while GP(2) does not. |
| **CF(c)** construction: pure truth blocks, SE, H2 | VERIFIED | Truth-cluster blocks are pure under the engine's R13 tie rule (W1 used a different tie rule; nulls only). λ_min(full corr) = 0.0243/0.0241 (B = 9) and 0.0150/0.0149 (B = 15). The "exact for n ≥ 1626" argument is correct: the correlation matrix is a fixed matrix ⊕ I. |
| CF masking numbers ("iid miss ≥ 0.86") | **GAP (qualification)** | Tier-0 final run, c = 2, n = 1600: 0.858 (W1 design), 0.854, 0.665, 0.641 (independent designs). At tier 1 (if escalation fires): 0.089, 0.082, 0.002, 0.001. At n = 400, c = 2: 0.003, 0.000, 0.001, 0.000, so not masked. |
| "CF satisfies jointly G, R, SE, BM-∞, T27 masking, start mass, ELIG, TD′" | **GAP (status)** | G, R, SE, BM-∞ and H2 hold by construction for all n. H3 (π₀({1}) ≥ c₀), ELIG (S̃₀ ∈ 𝓡₀) and TD′ are verified only at n ∈ {400, 1600}; as asymptotic (w.p. → 1) statements they are CONJECTURE. W1's confidence card (0.85 / 0.7) is consistent with this; its headline wording is not. |
| "No obstruction for (b1)+LS0" (compatibility) | VERIFIED as "no obstruction found"; not a proof | Consistent across 4 designs and 2 sample sizes. |

## 3. Repairs and refinements (complete)

### 3.1 D2, corrected constant and a sharper no-blow-up hypothesis — PROVED
Replace (D2-d) by the event actually used in step 2:

**(D2-d′)** NB′ := {S₀ is among the initial pilot draws} ∪ {ESS of the weights e^{d(X_i)/T_e} over the initial draws is ≥ 0.9H}.

*Proof of step 2 under NB′.* By Lemma S(i), ESS(φ) is non-increasing in φ. So:
- If φ′ = 1 passes, φ₁ = 1 has ESS ≥ 0.9H.
- If the bisection is not forced, lo passes by construction (`pilot_next_phi` sets lo only to passing midpoints).
- If it is forced, φ₁ = 1/T_e, which passes on NB′.

The rest of the proof is unchanged, and the conclusion holds with P(NB′^c | data) in place of P(NB^c | data). W1's NB, with log 1.925 replaced by log r*, r* = (11 + 2√10)/9, is a sufficient condition for NB′. Proof: 4r/(1+r)² is decreasing on r ≥ 1 and equals 9/10 at r*, and Kantorovich gives ESS/H ≥ 4mM/(m+M)² (re-derived: mean(w²) ≤ (m+M)mean(w) − mM, then minimise x²/((m+M)x − mM)). NB′ is strictly weaker than NB. For example, a single outlier draw with d higher by Δ keeps ESS(1/T_e) ≥ 0.9H as long as Δ ≲ 2T_e (for H = 512), whereas NB needs Δ ≤ 0.65 T_e.

### 3.2 C1 with a valid move kernel — COUNTEREXAMPLE (reproducible)
Same four states and log γ₀, log γ₁. Kernel: at a₁ or a₂, propose m w.p. ½ (else stay); at m, propose a₁ or a₂ w.p. ½ each; Metropolis acceptance. This proposal is symmetric, so the kernel is γ_φ-reversible on A, and o is isolated. With T = 1000 uniform stages, multinomial resampling and 9 terminal steps, the fraction of islands with no particle in A is 0.560 ± 0.035 (N = 10⁵) and 1.000 (N = 10⁶), out of 200 islands each, seed 4242. Every island has Ẑ/Z < ½. W1's conclusion stands: start mass, uniform bridge mass and zero exits do not imply delivery.

### 3.3 Correct reporting of the D2 and masking numbers
- **D2 bound in CF(1), W1 design.** Optimised over t, the bound is 2.2·10⁻⁷ at n = 400 (t = 0.131) and 1.6·10⁻⁵ at n = 1600 (t = 0.115), plus P(NB′^c). P(NB^c) was estimated at 0/100 at n = 400.
- **iid masking of CF(2).** At n = 1600, the tier-0 final-run miss probability is 0.64–0.86 depending on the design, and the tier-1 miss is ≤ 0.09. The asymptotic statement (β = −2a < 0) is unaffected.

### 3.4 Universal failure of TD(d,0), d ≥ 1 — PROVED (new; strengthens W1 §6.4)
**Proposition V1.** Assume s₀ ≥ 1, p ≥ s₀ + 1 and s₀ + 1 ≤ K. Let j ∈ S₀ and l ∉ S₀ satisfy F(S₀) > F(S₀ ∪ {l}). Then TD(d, m) fails for every d ≥ 1 and every m ≥ 0. In particular, TD(d,0) fails for all d ≥ 1 on the event {π(S₀) > ½}, so under T03's hypotheses P(TD(d,0) holds) → 0. This means T37(iii) is false for every d ≥ 1.

*Proof.* Let S := (S₀∖{j}) ∪ {l}.
- S ∈ 𝓡₁ ⊆ 𝓡_d, and S ⊉ S₀ with j its only missing true variable.
- |S| = s₀ < K, so the addition of j is feasible, with gain g(S,j) = F(S₀∪{l}) − F(S). The swap l→j is another feasible move, with gain F(S₀) − F(S).
- T37's clause for S ⊉ S₀ requires g(S,j) ≥ m + F(S₀) − F(S), that is, F(S₀∪{l}) ≥ F(S₀) + m ≥ F(S₀). This contradicts the assumption.
- If π(S₀) > ½, then F(S₀) > F(T) for every T ≠ S₀, and in particular for T = S₀ ∪ {l}. ∎

So the failures W1 found are not a proxy effect. Greedy progress fails to be *addition-first*, but it still makes progress, through a swap that reduces |S Δ S₀| by 2. The correct black-box input is TD′ or GP(d), as W1 recommends.

### 3.5 GP(d) ⇒ TD′(𝓡_d, ℓ) when ℓ + 1 ≥ s₀ + d — PROVED (fills a step W1 states without proof)
Under GP(d), from every S ∈ 𝓡_d ∖ {S₀}, the production best move strictly improves F, stays in 𝓡_d and lowers |S Δ S₀| by at least 1. The search therefore never stops early before S₀ (a strict improvement exists), and it stays in 𝓡_d, so GP applies again at every step.

After min(ℓ, ·) moves, the centre has |S_ℓ Δ S₀| ≤ max(0, s₀ + d − ℓ) ≤ 1. Either S₀ has already been reached, and so scored, or S_ℓ is a flip neighbour of S₀. In the latter case the next scan, which the engine always performs (`local_search`: a scan precedes the move-limit test), scores S₀. ∎

## 4. Is the method modelled faithfully?

Each assumption below was checked against `METHODOLOGY_v3.md` §§6.5–6.10 and against `v3_engine.h`, `v3_calib.h`, `v3_ledger.h` and `v3_core.cpp` (pilot driver). Full notes are in `NOTES.md`.

| assumption used by W1 | spec | engine | verdict |
|---|---|---|---|
| Round = uniform random order of m = p+B+2 labels, fresh per particle and round | §6.5 | `draw_order` (Fisher–Yates), called in `one_round` | faithful |
| Gibbs heat bath; addition at the cap excluded; both configurations count as scored (SR) | §6.5, 00_COMMON SR | `step_gibbs`: `held` + `eval(tmpQ, ME_GIBBS_FLIP)`; o_j = 0 and no evaluation when the addition is infeasible | faithful. SR is implemented, so W1's "to be confirmed" can be closed for the engine. |
| Every evaluated model enters the HPM | §6.10 | `Ledger::event` → `offer_hpm` on fresh evaluations; cache hits were offered when first scored | faithful |
| Initial draws scored | §6.10 | `eval(P[i], ME_INIT)` | faithful |
| Stage = reweight e^{Δd}, multinomial resampling, one round | §6.6, §6.8 | `run_island_s` | faithful |
| Pilot rule: φ′ = 1 if it passes; else 60 bisections; floor 1/T_e (forced) | §6.6 | `pilot_next_phi` (≥ 0.9H, lo passes, floor φ + 1/T_e, snapped to 1) | faithful |
| Terminal rounds: L burn-in + 4 measured at φ = 1, no reweighting or resampling | §6.8 | `run_island_s` | faithful |
| Local search: ≤ ℓ moves then one scan; strict improvement; lexicographic ties | §6.10 | `local_search` | faithful |
| Streams: pilot uses stream 0 (tier 0), final uses 10–13 | §6.8 | `cpp_cal_pilot` sid 0/5 | faithful |
| Complete-linkage tie rule | §6.3 (R13: smallest union) | `complete_linkage` | W1's `cf_family.py` breaks ties by pair (lo, hi) instead. This affects only the null blocks of CF; truth blocks are pure either way (checked with the engine rule). |
| LS0 | not in the method (proposed tweak) | `local_search(centre, …, emit_centre)` does **not** emit the centre when `emit_centre = false`, which is how production calls it | **Implementation caveat.** An LS0 implementation must call it with `emit_centre = true`. Otherwise S̃₀ itself is not scored, which matters exactly when S̃₀ = S₀. |

Nothing in W1's proofs assumes a behaviour the engine does not have.

## 5. What is weaker than it looks

### 5.1 The composition carries little content beyond its inputs
Route (b1) proves "S₀ ∈ 𝒮⁺" from TD′(𝔅, ℓ) and S̃₀ ∈ 𝔅, and TD′ is by definition "the local search from any centre in 𝔅 scores S₀". The theorem is correct, but the entire masked-regime difficulty sits in TD′ at the single centre S̃₀, plus ELIG. Neither is proved for any asymptotic family; both are verified numerically in CF. Route (b2) is likewise DELIV + REPAIR, and both are black boxes. The genuinely new mathematical content of W1 is D2, together with E1, C1 and the TD failure.

### 5.2 SHARE is close to the conclusion of D3
ζ_t bounds exactly the event "some 𝓡_d particle before stage t, none after resampling". D3 is a correct bookkeeping identity. Delivery in route (b2) is OPEN, as W1 says.

### 5.3 D2's asymptotic instance
D2-∞ needs four things, none proved for any family as n → ∞:
- Dep ≤ 1 − c₁ off a bounded set 𝒟;
- P(NB′^c) → 0;
- π₀(S₀ ⊕ j) > 1/10;
- k_D bounded.

In CF(1) they hold comfortably at n = 400 and 1600, but those instances are not masked. A plausibility estimate for CF-type designs: a draw containing a proxy of the missing variable has d higher by Θ(n), while T_e stays at 1000 up to n + p ≈ 2³¹. NB then fails once Θ(n) > 0.65 T_e; NB′ fails once it exceeds ≈ 2T_e. The probability that some pilot draw contains a proxy is ≈ H·B/(2p√n) ≍ B n^{−1/4}/10 (p = n^{3/4}) → 0, but slowly. So P(NB′^c) → 0 is plausible, but only at a slow rate. This is a CONJECTURE, not checked beyond n = 1600.

## 6. Needs escalation

1. **To HQ / W1-T37R (high priority).** Proposition V1 makes T37(iii) false for every d ≥ 1 in every design, on T03's own high-probability event. T37 must be restated with TD′ or GP(d) before any paper text cites it. This is a two-line argument, so a reviewer can check it in minutes.
2. **To HQ.** The D2 statistical instance (Dep, NB′, π₀(x°) > 1/10 as n → ∞) is the most valuable open item: it is the only no-tweak masked-regime route. It needs a family that is masked at n where the method is actually run. CF(1) is not masked at n ≤ 1600; masking needs larger c, or p ≥ n.
3. **To HQ (method).** If LS0 is adopted, implement it with `emit_centre = true` and record its provenance. Also fix its tie rule for argmax π₀ (for example the HPM tie rule) so that S̃₀ is well defined.
4. **Independent check wanted.** The asymptotic CF claims (H3, ELIG and TD′ w.p. → 1). Only numerics at two sample sizes exist.

## 7. Outside scope

- T37(ii)'s union bound is also mis-specified. It includes the comparison "add j vs swap l→j", whose score difference has the wrong sign w.h.p., so the bound cannot go to 0. That is a T37 restatement issue (item 1 above).
- In CF(2) at n = 1600, tier-1 escalation alone would make iid discovery likely (miss ≤ 0.09). Any "masked" illustration should state the tier, or use a design where Q_f(tier 1)·π₀(S₀) → 0 visibly.

## 8. Confidence card

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| T38(b)-R composition | as W1 PROOF §7, with D2 corrected per §3.1 | 0.97 (given inputs) | done (verified here) | the inputs TD′+ELIG, D2's instance, DELIV+REPAIR | (b1) LS0 minor; (b1′), (b2) no |
| D2 (corrected) | P(S₀ ∉ 𝒮_cal) ≤ e^{−2Ht²} + P(NB′^c) + exp{−Hβg(b−t)} | 0.97 | done | — | no |
| D2 statistical instance | Dep < 1−c₁, NB′, π₀(x°) > 1/10 w.p. → 1 in a masked one-cancellation family | 0.6 | 0.4 | uniform odds control off a bounded proxy set; NB′ at T_e = 1000 | no |
| Lemma A, B, S; D1; D3; E1 (deterministic); E3 | as W1 | 0.99 | done | — | no (E3 needs LS0) |
| C0, C1 | counterexamples to set-transfer and to "bridge mass ⇒ delivery" | 0.99 | done (reproduced, C1 with a valid kernel) | — | — |
| V1: TD(d,0) false for d ≥ 1 on {π(S₀) > ½} | §3.4 | 0.99 | done (PROVED here) | — | — |
| CF compatibility for (b1)+LS0, asymptotic | H3, ELIG, TD′ w.p. → 1 on CF(c) | 0.8 | 0.6 | TD′ uniform over the greedy path; π₀({1}) > ½ uniformly | no |
| Route (b2) delivery (SHARE/LT) | OPEN | 0.5 | 0.15 | selection vs within-𝓡_d moves (C1) | no |

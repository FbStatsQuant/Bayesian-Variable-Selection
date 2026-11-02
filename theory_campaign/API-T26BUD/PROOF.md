# API-T26BUD (task R5, T26-BUDGET): statements and proofs

Every result here is a **candidate**. It has not been reviewed or adopted. Notation follows `00_COMMON.md`, METHODOLOGY_v3 §6.3–6.8 and W2-T26 `PROOF.md`.
γ₀(S) = ϖ(S)∏_b r_b(S∩C_b) is the start (π₀ = γ₀/Z̄₀); d(S) = log BF(S) − Σ_b log r_b(S∩C_b); γ_t = γ₀e^{td}; and q_t = γ_t/Σγ_t
for any real t. The posterior is π = q₁. We write Δ_n = max{1 − π₀(S₀), 1 − π(S₀)} (W2-T26 Lemma 1), and 𝒢_n is the event that
the SMC branch is taken and calibration succeeds.

## 0. New symbols

| symbol | definition |
|---|---|
| r_S, e_S | r_S = γ₀(S)/γ₀(S₀) (start odds of S against S₀); e_S = d(S) − d(S₀) |
| R(t) | Σ_{S ∈ Ω_K, S ≠ S₀} r_S e^{t e_S} = (1 − q_t(S₀))/q_t(S₀), for t ∈ ℝ (Ω_K = feasible models) |
| R_V(t) | the same sum restricted to S ∈ V∖{S₀}; R_V ≤ R termwise when S₀ ∈ V |
| ε₀ | 0.9^{−1/2} − 1 ≈ 0.05409, so that 2 log(1 + ε₀) = log(1/0.9) |
| η_n | sup{η ∈ (0, 1] : R(0) ≤ ε₀ and R(1 + η) ≤ ε₀} (sup ∅ := 0) |
| N^pil | number of pilot stages = number of distinct pilot temperatures in (0, 1] (the last one is 1) |
| k^bis | number of grid intervals whose right endpoint came from the bisection branch of `build_grid` |
| D_k | for pilot stage k with population d₁, …, d_H: max_i d_i − (the ⌈0.02H⌉-th smallest d_i) (2 %-trimmed range) |
| a | 0.5125 ≤ 2 arccosh(0.98/√0.9) (≈ 0.51249…; we use a = 0.5124 in proofs, 0.5125 in the script — immaterial) |
| T^cap_n | an optional cap on the number of grid intervals (Rule CAP, §5) |

Identity used throughout: R(1 + η) = Σ_{S≠S₀} r_S^{−η} (r_S e^{e_S})^{1+η}. Here r_S e^{e_S} = π(S)/π(S₀). So R(1 + η) is the
order-(1+η) Rényi-type moment of the posterior odds against the start odds. In particular
**R(2) = [π₀(S₀)/π(S₀)²]·Σ_{S≠S₀} π(S)²/π₀(S)**, and exactly 1 + χ²(π‖π₀) = [π(S₀)²/π₀(S₀)]·(1 + R(2)). So, when π(S₀), π₀(S₀) → 1,
R(2) → 0 ⇔ χ²(π‖π₀) → 0.

## 1. Two facts about the calibration rules (`v3_calib.h`)

Let F_V(t) = log Σ_{S∈V} γ₀(S)e^{td(S)} and ρ_V(u, v) = exp{2F_V(v) − F_V(u) − F_V(2v − u)}, exactly as in `rho_V`.

**Fact 1 (monotonicity). PROVED.** For fixed u, v ↦ ρ_V(u, v) is non-increasing on [u, ∞). The same holds for the pilot's
population ESS, δ ↦ ESS(δ) = (Σ_i e^{δd_i})²/Σ_i e^{2δd_i}, on [0, ∞).
*Proof.* d/dv[−log ρ_V] = 2F′_V(2v − u) − 2F′_V(v) ≥ 0, because F_V is convex (it is a log-sum-exp of affine functions)
and 2v − u ≥ v. For the pilot, d/dδ log ESS = 2Ē_δ[d] − 2Ē_{2δ}[d] ≤ 0. Here Ē_s is the mean under weights ∝ e^{sd_i}, which is
non-decreasing in s (its derivative is a variance). ∎

Consequence: in both bisections the set of passing points in (u, b] is an interval (u, v*] ∩ (u, b]. The invariant "lo
passes or lo = u; hi fails" holds, so after 60 halvings lo ≥ v* − (b − u)2^{−60} whenever some tested point passed.

**Fact 2 (reference decomposition). PROVED.** If S₀ ∈ V, then for u < v,
 −log ρ_V(u, v) = L_V(u) + L_V(2v − u) − 2L_V(v) ≤ L_V(u) + L_V(2v − u),  L_V := log(1 + R_V) ≥ 0.
*Proof.* F_V(t) = log γ₀(S₀) + t d(S₀) + L_V(t). The affine parts cancel in the second difference, because
u + (2v − u) − 2v = 0. L_V ≥ 0. ∎

R_V is a positive combination of exponentials in t, so it is convex. Hence sup_{[a,b]} R_V = max{R_V(a), R_V(b)}. Also
R_V ≤ R, and R(0) = (1 − π₀(S₀))/π₀(S₀), R(1) = (1 − π(S₀))/π(S₀).

## 2. Theorem G (grid stage count). PROVED (deterministic)

**Statement.** Take any data, any successful pilot with temperatures 0 < φ₁ < … < φ_{N^pil} = 1, and any frozen V with
S₀ ∈ V. Let `build_grid` succeed with T intervals. Then:
(a) T = N^pil + k^bis, and every pilot temperature is a grid point;
(b) if η := η_n > 0, then k^bis ≤ ⌈log₂(1/η)⌉ (and k^bis = 0 when η = 1, i.e. when R(0) ≤ ε₀ and R(2) ≤ ε₀);
(c) hence N^pil ≤ T ≤ N^pil + ⌈log₂(1/η_n)⌉.
This holds for every construction in the rebuild loop, in particular for the final grid, because the targets (the pilot
temperatures of the tier) do not change across rebuilds.

**Proof.** (a) From u, the next target is b = min{φ_i > u}. The appended v lies in (u, b], because the bisection runs on
(u, b], the snap only moves v ≥ 1 − 10⁻¹² to 1 ≥ b, and validation requires v > u. So u never passes a target without
appending it. Each target is appended exactly once (u strictly increases), and every other appended point comes from
the bisection branch.

(b) Let η = η_n > 0 and fix u ∈ [0, 1). For every v ∈ (u, 1] with 2v − u ≤ 1 + η, both u and 2v − u lie in [0, 1 + η].
By convexity, R_V ≤ R ≤ max{R(0), R(1 + η)} ≤ ε₀ there. Fact 2 then gives −log ρ_V(u, v) ≤ 2 log(1 + ε₀) = log(1/0.9),
so v passes. (The set {η : R(1 + η) ≤ ε₀} is closed because R is continuous, so η_n is attained.)
Now take a bisection step from u. The target b fails, so b > (u + 1 + η)/2 =: m, since every point ≤ m passes. Hence
v* ≥ m. The bisection returns v ≥ m − 2^{−60}. Write g = 1 − u for the gap. A bisection step needs b ≤ 1 and b > m,
so g > η. After the step the gap is g′ ≤ (g − η)/2 + 2^{−60} < g/2 (for η > 2^{−59}). If the snap fires, g′ = 0.
Target steps never increase the gap. So after j bisection steps the gap is < 2^{−j}. The j-th bisection step needs a gap
> η at its start, and that gap is < 2^{−(j−1)}. So η < 2^{−(j−1)}, i.e. j < 1 + log₂(1/η), i.e. j ≤ ⌈log₂(1/η)⌉. For η = 1,
every v ≤ 1 passes from every u, so no bisection step occurs.

Edge cases: a validation failure after a snap, non-progress, and "too many intervals" are calibration failures, outside 𝒢_n.
The theorem is a statement on successful constructions only. ∎

*Remark (sharper form, same proof).* The condition actually used is L_V(u) + L_V(2v − u) ≤ log(1/0.9). The ε₀ form is a
convenient sufficient condition. The script also records the exact one-step quantity: on V = Ω, the one-step grid {0, 1}
passes iff χ²(π‖π₀) ≤ 1/9, since ρ_Ω(0, 1) = 1/(1 + χ²(π‖π₀)).

## 3. Lemma P (pilot step). PROVED (deterministic)

**Statement.** At a pilot stage at temperature φ < 1 with population d₁, …, d_H and 2 %-trimmed range D (D > 0), the next
temperature satisfies φ′ − φ ≥ min{1 − φ, a/D − 2^{−60}}. It also satisfies φ′ − φ ≥ 1/T_e, by the floor rule. Hence
 N^pil ≤ 1 + ⌈D̄/a⌉ (up to the 2^{−60} slack), D̄ := max_k D_k,
 and always N^pil ≤ T_e.
**Proof.** Let m be the ⌈0.02H⌉-th smallest d_i. Let J = {i : d_i ≥ m} (|J| ≥ 0.98H) and f = 1 − |J|/H ≤ 0.02. Put
w_i = e^{δ(d_i − m)}. On J, w_i ∈ [1, e^{δD}]. Off J, w_i < 1, so Σ_{i∉J} w_i² < fH ≤ (f/(1−f))|J| ≤ (f/(1−f))Σ_J w_i².
Hence Σ_i w_i² ≤ Σ_J w_i²/(1 − f), and
 ESS/H = (Σw)²/(HΣw²) ≥ (1 − f)·(Σ_J w)²/(H Σ_J w²) = (1 − f)(|J|/H)·κ_J ≥ (1 − f)²κ_J.
Here κ_J = (mean_J w)²/mean_J w² ≥ 4e^{δD}/(1 + e^{δD})² = cosh^{−2}(δD/2), the Kantorovich bound for w ∈ [1, e^{δD}]. To see it,
(w − 1)(e^{δD} − w) ≥ 0 gives E w² ≤ (1 + e^{δD})Ew − e^{δD}; then minimise μ²/((1 + e^{δD})μ − e^{δD}) over μ. So ESS ≥ 0.9H
whenever cosh(δD/2) ≤ 0.98/√0.9, i.e. δ ≤ a/D. By Fact 1 the bisection returns lo ≥ min(1 − φ, a/D) − 2^{−60}. If
δ = 1 − φ passes, φ′ = 1. Each non-final stage advances by at least a/D̄ − 2^{−60}, so there are at most ⌈D̄/a⌉ non-final
stages. ∎

## 4. Corollaries

**Corollary 1 (realised budget, general). PROVED.** On 𝒢_n ∩ {S₀ ∈ V_final} ∩ {η_n > 0}, the realised number of final-run
stages satisfies
 T_n ≤ min{T_e, N^pil + ⌈log₂(1/η_n)⌉} ≤ min{T_e, 1 + ⌈D̄_n/a⌉ + ⌈log₂(1/η_n)⌉}.
Hence (P1) of W2-T26 Theorem A holds as soon as
 (i) P(𝒢_n ∩ {S₀ ∉ V_final}) → 0, (ii) P(η_n ≤ η) → 0 for some fixed η > 0 (or merely Δ_n log(1/η_n) →_P 0), and
 (iii) (N^pil_n + 1)Δ_n → 0 in probability on 𝒢_n (sufficient: D̄_nΔ_n →_P 0).
*Proof.* Combine Theorem G(c), Lemma P, and T_n ≤ T_e from the "more than T_e intervals" rule. ∎

About (i): V contains the top 20p scored models by log γ₁. If S₀ is the posterior mode and is scored during calibration,
then S₀ ∈ V. The pilot scores its H_e iid π₀ draws (they are reweighted by e^{δd}, which needs d), so S₀ is scored
unless every draw misses it, which has probability (1 − π₀(S₀))^{H_e}. Hence P(S₀ ∉ V) ≤ P(S₀ not the HPM of π) +
E(1 − π₀(S₀))^{H_e} → 0 whenever T03 (HPM of π = S₀ w.p. → 1) holds and 1 − π₀(S₀) →_P 0. **PROVED** given those
inputs (T03 is locked; 1 − π₀(S₀) → 0 is T22(iii) / Prop. C on ORTH).

**Theorem 1 (one-stage regime). PROVED (given its hypotheses).** Suppose that, in P₀-probability,
1 − π₀(S₀) → 0, 1 − π(S₀) → 0 and R(2) → 0 (equivalently, χ²(π‖π₀) → 0; any H_e ≥ 1). Suppose also that
P(S₀ is the HPM of π) → 1. Then P(𝒢_n ∩ {T_n ≠ 1}) → 0. Hence (T_n + 1)Δ_n = 2Δ_n + o_P(1) → 0, and (P1) holds with T_n = 1.
*Proof.* (1) First pilot stage. The H particles are iid π₀ given the data. Put w_i = e^{(d_i − d(S₀))} (δ = 1 − 0 = 1).
Then mean_i w_i ≥ Ĝ := #{i : S_i = S₀}/H, and E[mean_i w_i² | data] = Σ_S π₀(S)e^{2e_S} = π₀(S₀)(1 + R(2)). Write
mean w² = Ĝ + M̂ with M̂ = H^{−1}Σ_{S_i≠S₀} w_i², so E[M̂ | data] = π₀(S₀)R(2). By Markov, M̂ →_P 0. By Markov applied to
1 − Ĝ ≥ 0, Ĝ →_P 1, because E[1 − Ĝ | data] = 1 − π₀(S₀) → 0. So ESS(1)/H ≥ Ĝ²/(Ĝ + M̂) →_P 1 > 0.9, and the pilot jumps to φ = 1: N^pil = 1 w.p. → 1.
(This is the population ESS in `pilot_next_phi`; the reference shift by d(S₀) does not change the ESS.)
(2) Grid. R(0) → 0 and R(2) → 0 give η_n = 1 w.p. → 1. With S₀ ∈ V w.p. → 1 (above), Theorem G gives k^bis = 0, so
T = N^pil = 1 for every construction. At tier 1 the same argument applies to the tier-1 pilot (new iid π₀ draws). ∎
Note: this result needs no particle-occupancy control at all, because only the iid first stage is used.

## 5. Rule CAP (the weakest extra rule) and Corollary 2. PROVED

**Rule CAP.** Replace "more than T_e intervals → the construction fails" by "more than min{T_e, T^cap_n} intervals → the
construction fails". Here T^cap_n is any deterministic sequence with T^cap_n Δ_n →_P 0. Under Theorem B's hypotheses
Δ_n = O_P(r_n), with r_n = 2^B√(log n)n^{−κ} + e_n + √(log n/n). So any T^cap_n = o(1/r_n) works, for example T^cap_n = ⌈C log n⌉.
On ORTH (κ = ½, e_n = o(n^{−m})), any T^cap_n = o(√(n/log n)) works.
**Corollary 2.** Under Rule CAP, T_n ≤ T^cap_n on 𝒢_n deterministically. So (P1) holds whenever T^cap_nΔ_n →_P 0, with no
premise on the run. The cap enters Theorem A only through 𝒢_n. Theorem A never claims P(𝒪_n) → 1, so a cap that fires
only lowers P(𝒪_n) and costs nothing in (A-i) and (A-ii).
*Remark.* The existing rule already gives T_n ≤ T_e = 4^e max(1000, ℓ²) = O(log²n). This is the deterministic form used by
W2-T26 Theorem B, so on ORTH (P1) is **already** a theorem asymptotically (conditional on Prop. C). The defect is
quantitative: the constant 1000 makes (T_e + 1)Δ_n ≥ 44 at n = 163,840. Rule CAP with T^cap_n = ⌈log₂ n⌉ (= 8 at n = 200,
= 18 at n = 163,840) removes that constant. Corollary 1 and Theorem 1 show that the cap does not bind when their hypotheses
hold. Numerically it never binds (§ evidence: realised T ∈ {1, 2} in the favourable designs).

## 6. Proposition O (ORTH: the grid inputs). PROOF SKETCH

**Family.** ORTH-F of W2-T26 Prop. C: XᵀX = (n−1)I_p, p ≤ min(n − 1, n^A), fixed s₀, fixed nonzero θ, Gaussian errors, and
the method's blocks. Let R²₀ ∈ (0, 1) be the population fraction of var(y) explained by S₀. Let A_b be the share explained
by the signals in block b, and λ_b = (1 − R²₀)/(1 − A_b) ∈ [1 − R²₀, 1]. Put λ* = min_b λ_b over blocks containing a null
(λ* = 1 − R²₀ as soon as some block has no signal).
**Claim.** For every fixed η ∈ (0, 1] with η(1 − λ*)A < ½,
 R(1 + η) = O_P(n^{−1/2 + Aη(1−λ*)}·polylog n) → 0.
Consequently, together with 1 − π₀(S₀) →_P 0 (Prop. C), η_n ≥ η_A := min{1, 1/(4A(1 − λ*))} w.p. → 1, and
k^bis ≤ ⌈log₂(1/η_A)⌉ = O(1). If A(1 − λ*) < ½ (e.g. p fixed, or A·R²₀ < ½), then R(2) →_P 0, and **Theorem 1 gives
T_n = 1 w.p. → 1 on ORTH-F**.
**Sketch.** On ORTH, with g = n as in `bvs_exact.all_log_m`, log BF(S) = −(|S|/2)log n − ν log(1 − Σ_{j∈S} a_j + b₀-terms).
Here a_j = z_j²/(n(n − 1)) and ν = n/2 + a₀. So with h(A) = −log(1 − A),
 d(S) = ν[h(Σ_b A_b(S)) − Σ_b h(A_b(S))] (the log n terms cancel), A_b(S) = Σ_{j∈S∩C_b} a_j.
Write S = (S₀∖M) ∪ E. Then ϖ appears in both γ₀ and γ₁, so log(π(S)/π(S₀)) − log r_S = e_S.
*Missing signals (M ≠ ∅).* h′ is increasing and the full-model share ≥ the block share. So deleting a signal costs at least
as much in the full model as in its block: posterior odds ≤ start odds for the M-part, both e^{−Θ(n)}. Hence
r_S^{−η}(π(S)/π(S₀))^{1+η} ≤ π(S)/π(S₀) (up to the cross-terms with E, which are lower order). The sum over M ≠ ∅ is
≤ e^{−cn}·(the E-sum below).
*Pure extras (M = ∅).* Let W_j = z_j²/((n − 1)σ̂²₀) ≈ χ²₁ (iid under ORTH and Gaussian errors, nulls orthogonal to S₀).
To first order, log(π/π₀-odds) adds, per null j ∈ C_b, π-odds ≈ c_n e^{W_j/2} and π₀-odds ≈ c_n e^{λ_bW_j/2}, with
c_n ≍ (s₀ + 1)/(2p√n). So
 r^{−η}(π-odds)^{1+η} ≈ c_n e^{s_bW_j/2},  s_b = 1 + η(1 − λ_b).
For s > 1, e^{sW/2} has tail index 1/s < 1, so Σ_{j≤p} e^{sW_j/2} = O_P(p^s·polylog). This gives a single-extra sum
O_P(n^{−1/2}p^{s−1}·polylog) = O_P(n^{−1/2+Aη(1−λ*)}polylog). Sets E with |E| = k contribute about (that)^k/k!. Sets with
|E| > k_n are handled by a T02-type dimension bound applied to the tilted law q_{1+η}.
**Unverified steps (why this is a SKETCH):** (1) uniform second-order control of the h-expansions when a_E is not small;
(2) the T02-type truncation for q_{1+η} (T02 is proved for q₁); (3) the cross-terms between M and E; (4) the σ̂₀ plug-in.
Each step looks routine, but none was checked line by line.
**Converse (shows the A-dependence is real).** If A(1 − λ*) > ½, the single-extra sum at η = 1 is ≍ n^{−1/2}p^{1−λ*} → ∞.
Then R(2) → ∞, the one-step grid fails, and k^bis ≥ 1 for large n. T_n still stays bounded by N^pil + ⌈log₂(1/η_A)⌉.
The heuristic is the same as above (PROOF SKETCH).

## 7. Conjecture P (pilot count on ORTH). CONJECTURE

On ORTH-F, N^pil = O_P(1). More precisely, N^pil ≤ 1 + ⌈log₂(1/η_A)⌉ w.p. → 1. Hence T_n = O_P(1).
*What is proved:* the first pilot stage. Its particles are iid π₀. The proof of Theorem 1 at a general δ ≤ 1 gives
ESS(δ)/H →_P 1 whenever R(2δ) →_P 0. So φ₁ ≥ min{1, (1 + η_A)/2} w.p. → 1 (the condition is used at t = 2δ ≤ 1 + η_A).
*What is missing:* at later stages the particles are resampled and moved under an adaptive schedule, so their law is not
q_φ. The locked occupancy result T15 is stated for frozen grids, and T12's unbiasedness also needs a frozen grid. A proof
needs either an adaptive-schedule occupancy bound, or a high-probability bound D̄_n = O_P(log n) on the trimmed d-range of
every pilot population (Lemma P then gives N^pil = O_P(log n), which is enough for (P1)). The second route needs the pilot
particles to stay on supersets of S₀ with O(1) extras. This is plausible, because every move is γ_φ-reversible and
models missing a signal have q_φ-mass e^{−Θ(n)} for all φ ∈ [0, 1], but it is not proved.

# F-SIGMA — the theory of the common-σ̂² start

Run F-SIGMA (Fable 5.1), branch `theory/F-SIGMA`, 2026-11-02, Felipe's laptop (exact small-p numerics only). Everything here is a **candidate**: not reviewed, not adopted. Status words of `theory_campaign/PROTOCOL.md`, never upgraded. Notation of `00_COMMON.md`, F-DRAFT `NEW_TARGETS.md` §0 and O-MIX §2: ν = a₀ + n/2, t_S = n z_SᵀH_S⁻¹z_S, Q_S = yᵀy − t_S, D_S = det H_S/det(G_S + I), c := 2b₀ + yᵀy, ψ(u) := u − 1 − log u ≥ 0.

**The variant.** Fix a plug-in σ̂² > 0 computed from (X, y) (and, if wanted, streams 0–9) before any table is built. Every block table is r_b^C(U) := D_U^{−1/2} exp{t_U/(2σ̂²)} for U ⊆ C_b (the known-σ² g-prior Bayes factor with σ² := σ̂²); γ₀^C := ϖ ∏_b r_b^C(S ∩ C_b), π₀^C := γ₀^C/Z̄₀^C, d^C := log BF − Σ_b log r_b^C. Everything else (target, partition, moves, calibration, final run, local search, decision rule) is unchanged. O-MIX §4 (Prop C0, Thm C1, Prop C2, Prop C3, §4.4) is the starting point; this report does not repeat its proofs and adds what the HQ brief asks for.

## 1. Headline

1. **Validity is untouched (Lemma S0, PROVED).** T09, T11(iii), T12, T13, T21 and T22(i)(ii)(iv) hold verbatim: their statements quantify over positive product-form tables, σ̂² is 𝓒-measurable, and the start stays exactly samplable. Two things change: the table-score ingestion into the HPM must use log m(U) (free from the same factorisation), and every *table-specific* expansion (EXP′, T22(iii), T27(i)'s H2, W1-EXP Thms 2–6, F-DRAFT W1/W2, Theorem W) must be re-derived. All of them are re-derived below in exact form.
2. **Under exact block orthogonality the common-σ̂² start is the posterior up to one scalar (Lemma S1, PROVED).** π₀^C(S)/π₀^C(S₀) = [π(S)/π(S₀)]·exp{−ν[ψ(u(S)) − ψ(u(S₀))]} with u(S) = (2b₀ + Q_S)/(2νσ̂²); hence the start's odds against S₀ are at most e^{νψ(u₀)} times the posterior's, and the W2 null log-odds gap is (1 − u₀)·Z²/2: the dilution fraction κ_b of F-DRAFT is replaced by the relative plug-in error 1 − σ̃²_{S₀}/σ̂². Checked to 10⁻¹³ by exact enumeration.
3. **Start mass is a dichotomy in a := σ²/σ̂² (Theorem S2, PROVED under BO).** With p ≍ n^A: if a < 1 + 1/(2A) (plug-in not more than a fixed factor below σ²) then 1 − π₀^C(S₀) = O_P(B2^B p^{(a−1)₊}√(log p) n^{−1/2}) → 0 and route (a) of T38 applies with no LS0 (Theorem S4). If a > 1 + 1/(2A) then π₀^C(S₀) → 0: the start fills with nulls. Cancellation masking (CL(L) chains) is untouched (Theorem S3, PROVED; = O-MIX Prop C3 in exact form).
4. **In a random design the common-σ̂² start is catastrophic at the study's size (Theorem S6, PROVED as a counterexample; exact numerics).** When null columns are independent of μ, each null's table exponent under common σ̂² is (v_∅/σ̂²)·χ²₁/2 with v_∅/σ² = 1/(1 − R²_pop) ≈ 25 at c = 1: the threshold of S2 then reads σ̂² > v_∅·2A/(2A+1), which is the *null* plug-in that reproduces v3's dilution. **No single σ̂² serves truths and nulls at once.** In the synthetic iid cell (n, p, s₀) = (200, 500, 14), c = 1: v3 gives log₁₀π₀(S₀) = −12.4 (the study's median) and the common-σ̂² start with the *oracle* σ² gives −1303 with the start mode at the cap K = 100. In the exact-BO cell p = 196 the same variant lifts the start from 10^{−7.5} to 10^{−0.5} = π(S₀).
5. **Consequence for Felipe's decision.** The common-σ̂² variant (tables only, everything else unchanged) is the exact cure for dilution *only* under block orthogonality; in the study's generators (S1/S3/S4/S6 are BO at population level but not in sample at p > n) the in-sample cross-block leakage ‖μ‖²/n per null is what v3's dilution protects against. The variant should **not** be deployed as specified. The mechanism identified here points to *residualised* tables (each block scored against y minus the other blocks' fitted signal) as the fix that keeps the protection; that is a different method change (Outside scope, §9). The pilot design of §8 is written so that the first, free step (post-hoc recomputation from saved tables) would have detected this.

## 2. Lemma S0 (variant invariance). PROVED.

**Statement.** Let σ̂² > 0 be measurable with respect to (X, y) and the calibration streams 0–9, and computed before any table. Then:

- **(a)** r_b^C(U) > 0 for all U ⊆ C_b, and γ₀^C = ϖ ∏_b r_b^C(S ∩ C_b) has the product form of M §6.3. Z̄₀^C is computed exactly by the size-profile convolution and the backward sampler returns exact iid π₀^C draws: T09(i) holds verbatim (its proof uses only positivity, the product form and ϖ depending on |S|).
- **(b)** T09(ii)–(v), T12(i)–(iv), T13, T21 (C1 and routes (a)–(f)), T22(i), (ii-a), (ii-b), (iv-a), (iv-b) and T31(i) hold verbatim with γ₀ := γ₀^C. The target π is unchanged, q₁ = π, d^C is evaluable pointwise (log BF(S) and the block table lookups).
- **(c)** T11(iii) holds verbatim: P(S* ∉ final iid draws | 𝓒) = (1 − π₀^C(S*))^{Q_f} for S* measurable w.r.t. (data, 𝓒); σ̂² is part of 𝓒.
- **(d)** CAL / EX-S: σ̂² must be frozen before the final streams 10–13; if it uses a pilot (e.g. C-fix iterations using the pilot's mode) that pilot must run on streams 0–9. A σ̂² that depends on final-run states breaks T12 exactly as a state-dependent stopping rule does (T12(iv)).
- **(e)** HPM ingestion (M §6.3 "every table score counts for the HPM"): r_b^C(U) is not m(U). The engine must record log m(U) = log C_n − ½ log D_U − ν log(2b₀ + Q_U) for every table entry; both D_U and Q_U = yᵀy − t_U come from the same factorisation, so this costs one logarithm per entry and keeps T21 route (d).
- **(f)** What is *not* invariant (table-specific statements): EXP′ (W1-EXP Thm 1), T22(iii), T27(i)'s H2, W1-EXP Thms 2–6, F-DRAFT W1/W2/W5/Theorem W/W′, O-MIX §4.4. They are re-derived in §§3–7; the exact branch (M §6.2) is unaffected since it builds no tables.

*Proof.* (a) and (b): the four facts used by the cited proofs are positivity, pointwise evaluability, exact iid draws with known Z̄₀, and (for T22(i)) the product form; O-MIX Prop B1(c) lists where each statement text says so (T22 STATEMENT.md line 35: "for every partition and positive tables"). (c): T11(iii)'s proof conditions on 𝓒 and uses only iid draws. (d) is CAL. (e) is arithmetic. ∎

## 3. Lemma S1 (exact structure under BO; odds transfer; the W2 analogue). PROVED.

Assume BO (X_{C_b}ᵀX_{C_b′} = 0, b ≠ b′). Define h(t) := −ν log(1 − t/c) − t/(2σ̂²) on [0, c), u(S) := (c − t_S)/(2νσ̂²) = (2b₀ + Q_S)/(2νσ̂²), u₀ := u(S₀), σ̃²_S := (2b₀ + Q_S)/(2ν) (so u(S) = σ̃²_S/σ̂²).

- **(a)** d^C(S) = h(t_S) for every S ∈ Ω, and h(t_S) − min h = νψ(u(S)) (O-MIX Thm C1(a)(b)).
- **(b) Odds transfer.** For every S, S′ ∈ Ω:
  log[π₀^C(S)/π₀^C(S′)] = log[π(S)/π(S′)] − ν[ψ(u(S)) − ψ(u(S′))].
- **(c) Odds bound.** With u_π := (1 − π(S₀))/π(S₀) and u_{π₀} likewise: u_{π₀^C} ≤ e^{νψ(u₀)}·u_π, hence 1 − π₀^C(S₀) ≤ e^{νψ(u₀)}(1 − π(S₀))/π(S₀). Equivalently, R₀ ≤ e^{νψ(u₀)}R₁ in T22(iv)'s notation: the start's endpoint odds are the posterior's times the plug-in penalty, and T22(iv-a) then gives inf_φ q_φ(S₀) ≥ 1/(1 + e^{νψ(u₀)}R₁).
- **(d) W2 analogue.** For l ∉ S₀ with g_l := t_{S₀+l} − t_{S₀} ≥ 0:
  LR_l^C := d^C(S₀+l) − d^C(S₀) = ν[ψ(u(S₀+l)) − ψ(u₀)] = (1/u₀ − 1)·g_l/(2σ̂²) + O(g_l²/n)
  = (1 − u₀)·(g_l/(2σ̃²_{S₀})) + O(g_l²/n).
  Under BO with ZL(S₀) (automatic: (P_{S₀+l} − P_{S₀})μ = 0), g_l = σ²Z_l²(1 + O(1/n)) with Z_l ~ N(0,1), so LR_l^C = (1 − u₀)Z_l²/2·(1 + o_P(1)): F-DRAFT Lemma W2 with κ_b replaced by ε₀ := 1 − σ̃²_{S₀}/σ̂². v3's tables are the case σ̂²_b = v_{T_b} per block, ε₀ = Δ_{T_b}/v_{T_b} = κ_b.
- **(e) Table increments are exact.** For T ⊆ C_b, l ∈ C_b ∖ T: log[r_b^C(T+l)/r_b^C(T)] = −½ log(D_{T+l}/D_T) + (t_{T+l} − t_T)/(2σ̂²), with no remainder (EXP′ becomes an identity); and under BO, t_{T+l} − t_T = t_{S+l} − t_S for every S with S ∩ C_b = T.

*Proof.* (a) is O-MIX Thm C1. (b): π/π₀^C = e^{d^C}·Z̄₀/Z̄₁ pointwise; take the ratio at S and S′ and use (a). (c): sum (b) over S ≠ S₀ with S′ = S₀ and drop e^{−νψ(u(S))} ≤ 1. (d): the identity is (b) at S₀ + l; the expansion is h(t₀ + g) − h(t₀) = g h′(t₀) + g²h″/2 with h′(t₀) = ν/(c − t₀) − 1/(2σ̂²) = (1/u₀ − 1)/(2σ̂²) and h″ = ν/(c − t)² = O(1/n). Under BO t_{S₀+l} − t_{S₀} is the block-b increment, whose population part vanishes and whose noise part is (u_{T,l}ᵀε)²·n/(n+1)·(1 + O(1/n)) by the standard rank-one update of z_SᵀH_S⁻¹z_S (W1-EXP Lemma 1.1 with the ν-log replaced by the linear term). (e): definition and block-diagonality of H_S under BO. ∎

*Check (`scripts/exact_small_p.py`, p = 12, three BO blocks of 4, n = 200, truths θ = (1.5, 1.5, 0.35) one per block, 3 replicates; `results/exact_small_p.txt`).* max|d^C − h(t_S)| ≤ 4.5·10⁻¹³ and max over all 4096 models of the odds-transfer identity error ≤ 5·10⁻¹³ at every σ̂² tried; the odds bound (c) held in all 30 (replicate, σ̂²) cases; the W2 approximation error is ≤ 0.03 nats against LR values up to 2.5. At σ̂² = σ̃²_{S₀} (u₀ = 1): π₀^C(S₀) = 0.737 / 0.805 / 0.815 against π(S₀) = 0.733 / 0.804 / 0.815, while v3's start has π₀(S₀) = 0.089 / 0.336 / 0.049 (the weak third truth is dilution-masked). The C-fix iteration from the v3 mode converged to S₀ in 2 iterations in all three replicates.

## 4. Theorem S2 (start concentration under common σ̂²: the dichotomy). PROVED under BO (upper bounds (i)–(iii) and lower bound (iv)); the remainders are those of W1-EXP Lemma 1.1/1.4.

**Setting.** G; BO; SE-blk(φ₀); s₀ fixed; s₀ ≤ K; p ≤ n^A; |C_b| ≤ B ≤ 16; BM-blk in the form min_{j∈S₀} θ_j²(n−1)φ₀²/(2σ̂²) ≥ (1 + A + B/2) log n + ω_n, ω_n → ∞ (this is the block beta-min with the plug-in in place of v_T). Let a₊, a₋ be constants with P(σ²/σ̂² ≤ a₊) → 1 (upper bounds) or P(σ²/σ̂² ≥ a₋) → 1 (lower bound).

**Statement.**
- **(i)** If a₊ < 1: 1 − π₀^C(S₀) = O_P(B 2^B (1 − a₊)^{−1/2} n^{−1/2}) (the n^{−1/2} rate of W1-EXP Thm 6, no √log).
- **(ii)** If a₊ = 1 (σ̂² ≥ σ²(1 − o(1))): 1 − π₀^C(S₀) = O_P(B 2^B √(log p + B) n^{−1/2}) (the T22(iii) rate).
- **(iii)** If 1 < a₊ < 1 + 1/(2A): 1 − π₀^C(S₀) = O_P(B 2^{a₊B} p^{a₊−1} L(p) n^{−1/2}) → 0, L slowly varying.
- **(iv)** If a₋ > 1 + 1/(2A) and p ≥ n^A: π₀^C(S₀) → 0 in probability; more precisely 1/π₀^C(S₀) ≥ c (s₀+1) p^{a₋−1} B^{−a₋} (log p)^{−a₋/2} n^{−1/2} e^{−O_P(1)} → ∞.

So the common-σ̂² start concentrates on S₀ iff σ̂² is not below σ²·2A/(2A+1) by a fixed factor, with p ≍ n^A. The same statement holds for any deterministic feasible reference S° with ZL(S°) in place of S₀ (the proof never uses supp θ = S₀; cf. W1-EXP Prop 2.2), which is what §5 needs.

*Proof.* T22(i) (verbatim, Lemma S0) gives 1 − π₀^C(S₀) ≤ (s₀+1)q/(1 − q) + s₀e with the AGG quantities of the common tables.

*The q term.* For U ⊇ U_b* := S₀ ∩ C_b in block b with |U ∖ U_b*| = j, write U as a chain of j single additions from U_b*. By Lemma S1(e), r_b^C(U)/r_b^C(U_b*) = ∏_{i}(D_{T_i+l_i}/D_{T_i})^{−1/2} exp{(t_{T_i+l_i} − t_{T_i})/(2σ̂²)}. Under SE-blk, D_{T+l}/D_T = (n+1)(1 + O(1/(nφ₀²))) (W1-EXP Lemma 1.2). Under BO and ZL(S₀), t_{T+l} − t_T = σ²Z_{T,l}²(1 + O(1/n)) with Z_{T,l} = u_{T,l}ᵀε/σ ~ N(0,1) (Lemma S1(d)). Hence on {σ²/σ̂² ≤ a₊},
  r_b^C(U)/r_b^C(U_b*) ≤ (n+1)^{−j/2} e^{O(j/n)} ∏_i e^{a₊Z_{T_i,l_i}²/2} ≤ (n+1)^{−j/2} e^{O(1)} exp{a₊ j M_b/2},
with M_b := max over the ≤ B2^B pairs (T, l) in block b of Z_{T,l}². So j!a_{bj} ≤ j! C(B, j) (n+1)^{−j/2} e^{O(1)} e^{a₊ j M_b/2} and (j!a_{bj})^{1/j} ≤ B n^{−1/2} e^{O(1)} e^{a₊M_b/2}, giving
  q ≤ (p − s₀)^{−1} B n^{−1/2} e^{O(1)} Σ_b e^{a₊M_b/2} ≤ (p − s₀)^{−1} B n^{−1/2} e^{O(1)} Σ_{b} Σ_{(T,l) ∈ b} e^{a₊Z_{T,l}²/2}.
The double sum has at most p2^B terms, each e^{a₊Z²/2} with Z ~ N(0,1) (dependent within a block, independent across blocks under BO).
- a₊ < 1: E e^{a₊Z²/2} = (1 − a₊)^{−1/2}, so the sum is O_P(p2^B(1 − a₊)^{−1/2}) by Markov: (i).
- a₊ = 1: P(e^{Z²/2} > t) ~ (2/π)^{1/2} t^{−1}(2 log t)^{−1/2}, tail index 1 with a slowly varying factor; the sum of N := p2^B such terms is O_P(N√(log N)) (truncate at N√(log N)·ω and bound the mean of the truncated part: ∫₁^{N} P(X > t)dt ≍ √(log N)): (ii).
- a₊ > 1: tail index 1/a₊ < 1; the sum of N terms is O_P(N^{a₊}L(N)) (standard for sums of iid-type heavy-tailed positive terms with dependence confined to blocks of size ≤ B2^B: apply the union bound block by block as in W3-VEXP; never take expectations): (iii). Then q ≤ B n^{−1/2} 2^{a₊B} p^{a₊−1} L(p) e^{O_P(1)} → 0 iff (a₊ − 1)A < 1/2.

*The e term.* For U ⊆ C_b with a := |U_b* ∖ U| > 0: r_b^C(U)/r_b^C(U ∪ U_b*) = (D_{U∪U*}/D_U)^{1/2} exp{−(t_{U∪U*} − t_U)/(2σ̂²)}; the determinant ratio is ≤ (n+1)^{a/2}(1 + O(1/n))^a, and t_{U∪U*} − t_U ≥ ‖(P_{U∪U*} − P_U)μ‖²(1 − o_P(1)) − O_P(√(n) · ‖·‖) ≥ a(n−1)φ₀²θ_min²(1 − o_P(1)) uniformly over the ≤ p2^B pairs by the Gaussian tail bound (W1-EXP Lemma 1.4). So e ≤ 2p·n^{1/2}·exp{−(n−1)φ₀²θ_min²(1 − o_P(1))/(2σ̂²)} = o_P(1) under BM-blk as stated (the factor n^{B/2} absorbs the block-size union). Hence (i)–(iii).

*(iv).* Take one null l_b in each of the ≥ (p − s₀B)/B ≥ J′ signal-free blocks. For such a block U_b* = ∅ and, by T22(ii-a) (verbatim), π₀^C(S₀ + l_b)/π₀^C(S₀) = [w(s₀+1)/w(s₀)]·r_b^C({l_b}) = [(s₀+1)/(2p − s₀ − 1)]·D_{l_b}^{−1/2} e^{t_{l_b}/(2σ̂²)}, with t_{l_b} = (x_{l_b}ᵀε)²·n/((n+1)(n−1)+1) = σ²Z_b²(1 + O(1/n)) since x_{l_b}ᵀμ = 0 under BO. The Z_b are iid N(0,1) across blocks. On {σ²/σ̂² ≥ a₋}, 1/π₀^C(S₀) ≥ Σ_b π₀^C(S₀+l_b)/π₀^C(S₀) ≥ [(s₀+1)/(2p)] (n+1)^{−1/2} e^{−O(1)} exp{a₋ max_b Z_b²/2}. With x := 2 log J′ − 2 log log J′: P(max_b Z_b² ≤ x) ≤ exp{−J′P(Z² > x)} ≤ exp{−c√(log J′)} → 0, so max_b Z_b² ≥ 2 log J′ − 2 log log J′ w.p. → 1, which gives the display with J′ ≍ p/B. The exponent (a₋ − 1) log p − ½ log n → +∞ iff (a₋ − 1)A > 1/2 when p = n^A. ∎

*Remarks.* (1) The threshold a* = 1 + 1/(2A) is the statement "the top null's chance score 2 log p, inflated by a, must stay below the cost log p + ½ log n". At the study's size, A = log 500/log 200 = 1.17 and a* = 1.43: the plug-in may be at most 30% below σ² (finite-n: the 2 log p is really 2 log(p/B)). (2) Under BO the *posterior* is the case a = 1 of the same calculation (Lemma S1 with u₀ = 1), which is why (ii) reproduces T03's √(log n/n)-type rate. (3) The within-block cap never binds (B ≤ K) but the *total* size law of π₀^C does interact with K in regime (iv): the convolution truncates at K, so when nulls flood in the start mode sits at |S| = K and the plug-in iteration of §7 runs away (counterexample C-E4). (4) v3's tables are the block-wise case σ̂²_b = v_{T_b}; F-DRAFT W5's "dilution protects" is exactly a_b = σ²/v_{T_b} < 1 in (i), at the price of masked weak truths (the e term with σ̂² replaced by v_{T_b}).

## 5. Theorem S3 (the masked regime survives: cancellation chains). PROVED.

**Statement.** Let H1 and CL(L) of W1-EXP hold along a chain S° = S^{(0)} ⊂ … ⊂ S^{(c)} = S₀ of single within-block additions l_i into blocks b_i with T_i = S^{(i)} ∩ C_{b_i}, SE on the chain sets, and σ̂² ≥ σ²/a₊ w.p. → 1. Then, w.p. → 1,
  log π₀^C(S₀) − log π₀^C(S°) = −c log p − (c/2) log n + Σ_{i<c} log((s+i+1)/2) + Σ_{i<c} (δ_{T_i,l_i} + σZ_i)²/(2σ̂²) + O(c/(nφ₀²)),
with Z_i ~ N(0,1) (jointly Gaussian). In particular with bounded L: π₀^C(S₀) ≤ π₀^C(S₀)/π₀^C(S°) = p^{−c}n^{−c/2}e^{O_P(1)}, masking of the T27(i) type with the same polynomial rate as v3; the only change is the multiplier σ²/σ̂² in place of σ²/v_{T_i} in the exponent (v_{T_i} ≥ σ², so the common-σ̂² start is at most a bounded factor e^{Σ_i(δ_i+σZ_i)²Δ_{T_i}/(2σ²v_{T_i})} *less* masked). If moreover ZL(S°), SPREAD and VIS-lin(S°) hold (the LH family), the reference carries the mass: 1 − π₀^C(S°) → 0 by Theorem S2 applied at S°, so H3 holds and the display is a two-sided law for π₀^C(S₀) itself.

*Proof.* T22(ii-a) verbatim along the chain, Lemma S1(e) for each increment (exact, no EXP′ remainder), the determinant ratio D_{T+l}/D_T = (n+1)(1 + O(1/(nφ₀²))) and w(k+1)/w(k) = (k+1)/(2p − k − 1). The increment t_{T_i+l_i} − t_{T_i} = (u_{T_i,l_i}ᵀy)²·n/(n+1)·(1 + O(1/n)) = (δ_{T_i,l_i} + σZ_i)²(1 + O(1/n)) (the explained-sum-of-squares increment of a single added regressor, W1-EXP Lemma 1.1). Multiply over the chain. The last sentence is Theorem S2 at reference S° (its proof uses ZL(S°), not supp θ = S°). ∎

This is O-MIX Prop C3 restated with the exact exponent and the comparison to v3. Consequence for T38(b): unchanged from O-MIX: route (a) fails under (C) whenever Q_f = o(p^c n^{c/2}); (C) is not a cancellation fix.

## 6. Theorem S4 (T38 route (a) under common σ̂², no LS0) and the finite-n quantification.

**Statement (asymptotic, BO).** Under the setting of Theorem S2 with a₊ < 1 + 1/(2A), together with T03's hypotheses (G, R, SE, BM-C) for the posterior, P(U) → 0, EX-A, EX-S, CAL, SR:
  Q_f·π₀^C(S₀) → ∞ in probability, P(S₀ ∉ 𝒮) → 0, and P(Ŝ ≠ S₀) → 0,
with no LS0 and no delivery argument. **PROVED-UNDER** Theorem S2 and the locked T03, T11(iii), T21.

*Proof.* Theorem S2 gives π₀^C(S₀) → 1 in probability; Q_f ≥ 4N₀(L+6) → ∞; T11(iii) (Lemma S0(c)) gives E(1 − π₀^C(S₀))^{Q_f} ≤ P(π₀^C(S₀) < ½) + 2^{−Q_f} → 0; T21 (C1) with route (a) and 2E₀[1 − π(S₀)] → 0 (T03) closes. ∎

*Honest reading.* As O-MIX §7 notes, in the fixed-β BO regime the v3 start is already favourable asymptotically (W1-EXP Thm 2/6), so S4's asymptotic content coincides with T38(a) under v3; the gain of the variant is at finite n, in the weak-signal window where a truth's table gain δ²/(2v_T) is below the cost while δ²/(2σ²) is above it. That window is exactly where T03's BM-∞ is silent (M_n → ∞ required), so a theorem in which (C) beats v3 needs a posterior statement in the window; this is the crux of the confidence card.

**Finite-n quantification at (n, p, s₀) = (200, 500, 14), study β pattern (1.4, −1, 1.8, −1.2, 0.8, −1.6)·c, σ = 1.** Energy ‖μ‖² ≈ 199·10.84·(14/6) = 5030 at c = 1 (R²_pop = 0.96, v_∅/σ² = 26), 1258 at c = 0.5 (R² = 0.86, v_∅/σ² = 7.3). Per-truth signal δ_j² ≈ 199θ_j². Cost of one variable in the start ≈ log((2p − s₀)/(s₀+1)) + ½ log(n+1) = 4.18 + 2.65 = 6.83 nats.

| |θ_j| at c = 1 | δ_j² | v3 table gain δ²/(2v_T), v_T ≈ 26 − δ²/199 | common σ̂² = σ² gain δ²/2 | v3 masked? |
|---|---|---|---|---|
| 0.8 | 127 | 2.5 | 64 | yes |
| 1.0 | 199 | 4.0 | 100 | yes |
| 1.2 | 287 | 5.9 | 143 | yes |
| 1.4 | 390 | 8.2 | 195 | no (marginal) |
| 1.6 | 510 | 11.0 | 255 | no |
| 1.8 | 645 | 14.4 | 322 | no |

With one truth per block, 7 of the 14 truths (those with |θ| ≤ 1.2) are dilution-masked in v3, each costing 6.8 − gain ≈ 1–4 nats, total ≈ 21 nats ≈ 10^{−9} before the within-block null layer; this is the study's median π₀(S₀) ≈ 10^{−12} (THEORY_PRIORITIES §5) and the exact synthetic cells below reproduce it (10^{−7.5} at p = 196 BO, 10^{−12.4} at p = 500 iid). Under common σ̂² ≈ σ² *and BO*, every truth is visible by ≥ 57 nats and the start is the posterior (Lemma S1): Q_f·π₀^C(S₀) ≈ 1.4·10⁵·π(S₀) ≫ 1, with π(S₀) ≈ 0.3–0.9 (O-SWAP: one-move posterior miss probability 6–9% at c = 1; the exact cell gives π(S₀) ≈ 0.29). Route (a) would apply at the study's size **if the design were block-orthogonal**. It is not; see Theorem S6.

## 7. Risks and counterexamples

### Theorem S6 (random-design leakage catastrophe). PROVED (the mechanism is exact; the extreme-value step is that of S2(iv)); exact numerics.

**Statement.** Let the null columns be independent of μ in the sense of a random design: x_l = (standardised) vector with x_lᵀμ/(‖x_l‖‖μ‖) ~ N(0, 1/n)·(1 + o(1)) across l ∉ S₀ in signal-free blocks (iid Gaussian designs; the study's S1/S3/S4/S6 generators). Then for such a null, at T = ∅,
  t_{l} = (x_lᵀy)²/(n−1)·(1 + O(1/n)) = (δ_{∅,l} + σZ_l)²(1 + O(1/n)),  δ_{∅,l}² = (u_lᵀμ)² ≈ (‖μ‖²/n)·χ²₁ = Δ_∅·χ²₁(1 + o(1)),
so (δ + σZ)² ≈ v_∅·χ²₁ in law, and the single-null start odds under common σ̂² are
  π₀^C(S₀+l)/π₀^C(S₀) = [(s₀+1)/(2p − s₀ − 1)]·(n+1)^{−1/2}·exp{(v_∅/σ̂²)·χ²_{1,l}/2}·e^{O(1/n)},
whereas v3's tables give the same with exponent (v_∅/v_∅)·χ²₁/2 = χ²₁/2. Hence Theorem S2 holds with a := v_∅/σ̂² in place of σ²/σ̂²: the common-σ̂² start concentrates only if σ̂² > v_∅·2A/(2A+1), i.e. only for a plug-in at the level of the *marginal* variance of y, which is the null plug-in that reproduces v3's dilution exactly (O-MIX: u₀ − 1 ≈ −R²). For σ̂² ≈ σ² and R²_pop fixed, the exponent inflation is 1/(1 − R²_pop) = 26 at c = 1, every null with χ²₁ > 2·6.83/26 = 0.53 (≈ 47% of nulls) has positive start log-odds, and the start mode sits at the cap K.

*Proof.* Lemma S1(e) for the increment; the law of u_lᵀy for a direction u_l independent of μ and ε; the counting of §4(iv). ∎

*Numerics (`scripts/study_size.py`, cells BO196 and IID500, `results/study_size_*.txt`; exact tables of all 2^14 sub-models of every block, exact convolution normalisers, exact start modes, importance-sampling estimate of π(S₀) from exact iid π₀^C draws with weights e^{d^C}, 400 draws; seeds in the script).* See §8 table. Headline rows: IID500, c = 1, oracle σ̂² = σ²: log₁₀π₀^C(S₀) = −1302.7, start mode size 100 = K; v3: −12.35 with mode size 5. BO196, c = 1: v3 −7.47 (mode = 7 truths), common σ̂² at σ̃²_{S₀}: −0.52 against π(S₀) = 10^{−0.55}.

### C-E1: screening plug-in underestimates (PROVED by S2(iv)).
A pooled residual variance from a marginal screening fit of the top-m columns at p ≫ n selects nulls with Z² of order 2 log p; with m = 20 nulls each explaining ≈ 6–8σ², RSS falls to ≈ (0.3–0.5)σ²(n − m): a = 2–3 > a* = 1.43 and S2(iv) applies even under BO. In the IID500 cell the top-20 screening plug-in gave σ̂² = 0.114 on the y scale against σ² = 0.038 (a = 0.33, over-estimated: at p = 500 the screening set is dominated by the truths); at BO196 it gave a = 1.15 (safe). The direction of the error depends on p/n and R²; no degrees-of-freedom correction fixes selection bias. Any deployment needs a floor.

### C-E2: cancellation chains (PROVED, Theorem S3 = O-MIX Prop C3). Unchanged masking at rate p^{−c}n^{−c/2}.

### C-E3: non-BO leakage at population level (S5 common-factor family). PROOF SKETCH.
With δ²_{∅,l} ≍ n for nulls in 98/100 blocks (W1-EXP pop_leak_study), both starts include proxies; the common-σ̂² exponent δ²/(2σ̂²) exceeds v3's δ²/(2v_T) by the factor v_T/σ̂² ≈ 1/(1 − R²), so the start's proxy count and size grow, hitting K: NM-type overcounting amplified. Not a counterexample to validity; a counterexample to "helps".

### C-E4: runaway of the iterative plug-in (C-fix). COUNTEREXAMPLE (exact numerics) + PROOF SKETCH.
The map σ̂² ↦ σ̃²(mode of π₀^C[σ̂²]) has, in regime S2(iv)/S6, a second fixed point at |mode| = K: nulls enter, RSS of the mode falls, σ̂² falls, more nulls enter. IID500, c = 1: from the v3 mode (σ̂² = 0.50, a = 0.08) the iteration went 0.50 → … → 0.0207 (a = 1.85) in 4 steps with |S_fix| = 100 = K and S₀ ⊆ S_fix. In BO196 the same iteration converged to S₀ in 2 steps. *Sketch:* at |S| = K = n/2 the RSS of the start mode is ≈ (n − K)σ² − (leaked signal) ≪ nσ²/2, so σ̂² < σ²/a* and S2(iv) keeps the mode at K; the fixed point is stable.

### C-E5: interaction with the cap K.
Within a block the cap is inactive (B ≤ K). Globally, the common-σ̂² start in the flooding regime has its size law truncated at K; validity (exact normaliser, exact sampler) is unaffected, delivery is dead (π₀^C(S₀) ≤ 10^{−1300}), and every final iid draw is a K-model: the bridge then has to shed ≈ 86 nulls, a crossing of Θ(K) flips (F-DRAFT W″ gives ≈ 3π stages per two-state crossing; here the crossings are many).

## 8. Evidence tables

Exact small p: §3. Study-size cells (medians are not meaningful with 2 replicates; all rows reported in `results/`). "IS log₁₀ π(S₀)" is the importance-sampling estimate from π₀^C; it is reliable only when the ESS fraction is ≳ 0.5 (rows with ESS ≈ 0 are marked unreliable).

| cell | c | rep | v3: log₁₀π₀(S₀) | IS log₁₀π(S₀) | common σ̂² = σ² (oracle) | σ̂² = σ̃²_{S₀} | C-fix | v3-mode RSS | screen top-20 | null s_y² | 0.7σ² | 0.5σ² |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BO196 | 1.0 | 0 | -7.47 (|mode|=7, ∩S₀=7) | -0.55 | -0.49 (a=1.000, |mode|=14) | -0.52 (a=1.052, |mode|=14) | -0.52 (a=1.052, |mode|=14) (2 its, |S_fix|=14, ∩S₀=14) | -0.40 (a=0.120, |mode|=14) | -0.60 (a=1.146, |mode|=14) | -7.82 (a=0.038, |mode|=7) | -0.94 (a=1.429, |mode|=14) | -2.68 (a=2.000, |mode|=16) |
| BO196 | 1.0 | 1 | -7.55 (|mode|=8, ∩S₀=8) | -0.74 | -0.95 (a=1.000, |mode|=14) | -0.69 (a=0.865, |mode|=14) | -0.69 (a=0.865, |mode|=14) (2 its, |S_fix|=14, ∩S₀=14) | -0.44 (a=0.151, |mode|=14) | -0.77 (a=0.911, |mode|=14) | -7.84 (a=0.039, |mode|=8) | -2.76 (a=1.429, |mode|=16) | -8.41 (a=2.000, |mode|=21) |
| BO196 | 0.5 | 0 | -8.57 (|mode|=6, ∩S₀=6) | -0.71 | -0.61 (a=1.000, |mode|=14) | -0.67 (a=1.057, |mode|=14) | -0.67 (a=1.057, |mode|=14) (3 its, |S_fix|=14, ∩S₀=14) | -1.62 (a=0.322, |mode|=13) | -0.85 (a=1.184, |mode|=14) | -8.94 (a=0.150, |mode|=6) | -1.39 (a=1.429, |mode|=14) | -4.37 (a=2.000, |mode|=18) |
| BO196 | 0.5 | 1 | -9.52 (|mode|=4, ∩S₀=4) | -0.77 | -0.73 (a=1.000, |mode|=14) | -0.73 (a=0.999, |mode|=14) | -0.73 (a=0.999, |mode|=14) (4 its, |S_fix|=14, ∩S₀=14) | -4.24 (a=0.244, |mode|=11) | -0.73 (a=1.017, |mode|=14) | -9.93 (a=0.142, |mode|=4) | -1.40 (a=1.429, |mode|=15) | -4.74 (a=2.000, |mode|=19) |
| IID500 | 1.0 | 0 | -12.35 (|mode|=5, ∩S₀=5) | unreliable | -1302.69 (a=1.000, |mode|=100) | -1194.54 (a=0.928, |mode|=100) | -2569.19 (a=1.841, |mode|=100) (4 its, |S_fix|=100, ∩S₀=14) | -8.08 (a=0.076, |mode|=11) | -306.21 (a=0.335, |mode|=100) | -12.80 (a=0.038, |mode|=5) | -1947.94 (a=1.429, |mode|=100) | -2808.86 (a=2.000, |mode|=100) |
| IID500 | 1.0 | 1 | -10.54 (|mode|=8, ∩S₀=7) | unreliable | -1541.75 (a=1.000, |mode|=100) | -1418.50 (a=0.929, |mode|=100) | -2215.62 (a=1.386, |mode|=100) (3 its, |S_fix|=100, ∩S₀=14) | -48.43 (a=0.123, |mode|=38) | -672.65 (a=0.501, |mode|=100) | -10.81 (a=0.039, |mode|=7) | -2289.46 (a=1.429, |mode|=100) | -3286.94 (a=2.000, |mode|=100) |
| IID500 | 0.5 | 0 | -13.50 (|mode|=6, ∩S₀=6) | unreliable | -302.45 (a=1.000, |mode|=100) | -309.82 (a=1.015, |mode|=100) | -835.68 (a=2.076, |mode|=100) (4 its, |S_fix|=100, ∩S₀=14) | -18.65 (a=0.299, |mode|=25) | -141.77 (a=0.663, |mode|=78) | -13.85 (a=0.141, |mode|=6) | -513.44 (a=1.429, |mode|=100) | -797.60 (a=2.000, |mode|=100) |
| IID500 | 0.5 | 1 | -18.60 (|mode|=4, ∩S₀=4) | unreliable | -169.16 (a=1.000, |mode|=100) | -160.48 (a=0.975, |mode|=100) | -394.32 (a=1.637, |mode|=100) (6 its, |S_fix|=100, ∩S₀=12) | -13.29 (a=0.293, |mode|=7) | -48.98 (a=0.622, |mode|=49) | -19.03 (a=0.169, |mode|=2) | -319.84 (a=1.429, |mode|=100) | -524.46 (a=2.000, |mode|=100) |

Each common-σ̂² entry is log₁₀π₀^C(S₀) with a = σ²/σ̂² and the start-mode size. 'unreliable' marks IS estimates with ESS fraction < 0.5 (the BO196 estimates at σ̂² = σ̃²_{S₀} have ESS fraction ≥ 0.96). The Thm C1 bound log₁₀π₀^C(S₀) ≥ IS log₁₀π(S₀) − νψ(u₀)/log 10 held in every BO196 row with a reliable π(S₀) estimate (it is a BO theorem and is not expected to hold in IID500).

Readings. (1) BO196: v3 is masked by dilution at exactly the predicted level and the common-σ̂² start with any plug-in within a factor 1.4 of σ² restores π₀^C(S₀) to the posterior level; the Thm C1 bound holds in every row; the over-estimated v3-mode plug-in (a = 0.12) still gives a concentrated start (regime S2(i)), since all 14 truths' δ²/(2σ̂²) stay above the cost at c = 1. (2) IID500: v3 reproduces the study's median masking (10^{−12}); every common-σ̂² plug-in near σ² floods the start (Theorem S6); the only plug-ins that do not flood are those at the level of v_∅ (the null plug-in), which reproduce v3's dilution. (3) The C-fix iteration converges to S₀ under BO and runs away to the cap in the iid design.

## 9. What fails and why; outside scope

- **Route tried and abandoned:** an asymptotic theorem in which the common-σ̂² start beats v3 under BO needs the weak-signal window (θ_w² between 2σ²·cost/n and 2v_T·cost/n); in that window T03's BM-∞ fails, so the posterior side has no locked statement. A finite-n statement (Lemma S1(c): start odds ≤ e^{νψ(u₀)}·posterior odds) is the honest form.
- **The fundamental obstruction (outside the brief's "everything else unchanged"):** the dilution in v3's tables is not an accident; it is the correct noise scale for a block that sees the other blocks' signal as leaked variance. Removing it without removing the leaked signal is wrong in every non-orthogonal design. The natural fix that keeps "tables only" in spirit is **residualised tables**: score block b against y_{(b)} := y − P_{Ŝ∖C_b}y (the other blocks' fitted signal removed, Ŝ a cheap screen or the v3 mode, iterated once or twice: backfitting), with the common σ̂² from the final residual. Under BO this equals the common-σ̂² variant; in random designs it removes the leaked Δ_∅ from the nulls' increments while keeping each truth's full gain. Validity: the tables remain positive and 𝓒-measurable (Lemma S0 applies verbatim); the HPM ingestion needs the full-y log m(U) recorded separately. Not pursued here (scope); recorded for HQ.
- **Needs escalation:** (a) the heavy-tailed-sum step of S2(iii) (dependence within blocks; I used the block-wise union bound of W3-VEXP without re-checking it line by line); (b) the exact O(1/n) remainders of Lemma S1(d)/(e) in the increments (W1-EXP Lemma 1.1); (c) an independent check of Theorem S6's law of (u_lᵀμ)² for the study's actual generators (S3/S4/S6 have within-group correlation; the leaked energy per null is then Δ_∅·χ²₁ only up to constants).

## 10. Pilot design under the investment rule

Smallest experiment that would decide whether the variant keeps the empirical results and lifts π₀(S₀):

1. **Step 0, free, no SMC runs (do this first).** From the saved tables of the 2,400 fits (log m(U) per table entry; D_U recomputable from X), recover t_U = yᵀy − Q_U and rebuild π₀^C(S₀), π₀^C(𝓡₂), the start mode size and the Thm C1 bound for σ̂² ∈ {σ̃²_{S̃₀}, C-fix, s_y²} per fit; compare with π₀(S₀) and with the exact-cell predictions of §8. Expected outcome from Theorem S6: flooding (mode size ≈ K) in S1/S3/S4/S6 at c = 1 for every plug-in near σ². If Step 0 shows flooding, stop: no SMC pilot is needed.
2. **Step 1, only if Step 0 passes (it should not):** 2 cells, S4 at (200, 500), c ∈ {1, 0.5}, 20 paired datasets each (same seeds), v3 vs variant with the floored C-fix plug-in; record HPM = S₀ rate, π₀(S₀), first-stage ESS, stage count, E1–E3, run time. Pass criterion: median π₀^C(S₀) > 0.1 and HPM rate within 2 datasets of v3 (paired). Plus one stress cell S5 (common factor) for C-E3.
3. **Step 2 (the residualised-table alternative, if HQ wants it):** same Step 0 recomputation with y residualised by the v3 mode's other-block fit, which needs the table scores against the residual (new scoring pass over all tables: ≈ 3 s per fit at p = 1,000, B = 14; no SMC runs).

## 11. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| Lemma S0 (validity) | §2 | high | done (PROVED; full-proof reading of T09/T12 by a reviewer still advisable, as O-MIX §9.2) | HPM ingestion of log m(U) | yes (tables) |
| Lemma S1 (BO structure, odds transfer, W2 analogue) | §3 | high | done (PROVED; checked to 10⁻¹³) | — | yes |
| Theorem S2 (dichotomy at a* = 1 + 1/(2A)) | §4 | high | done modulo the heavy-tail aggregation step (escalation (a)) | sums of e^{aZ²/2} with block dependence | yes |
| Theorem S3 (cancellation untouched) | §5 | high | done (PROVED) | remainder bookkeeping | — |
| Theorem S4 (T38(a) without LS0, BO) | §6 | high asymptotically; **vacuous as an improvement** over v3 in the fixed-β regime | done under S2 | weak-signal window where T03 is silent | yes |
| Theorem S6 (random-design catastrophe) | §7 | high (exact numerics: 10^{−1303}) | done | law of leaked energy in the study generators | — |
| (C) as deployed variant | "tables only, common σ̂²" | **fails** in the study's designs | — | — | do not deploy; consider residualised tables (§9) |

## 12. Summary (8 lines)

1. Validity: T09, T11(iii), T12, T13, T21, T22(i)(ii)(iv) hold verbatim for common-σ̂² tables; σ̂² must be 𝓒-measurable (streams 0–9 at most); HPM ingestion must record log m(U) (Lemma S0, PROVED).
2. Under BO: π₀^C(S)/π₀^C(S₀) = [π(S)/π(S₀)]e^{−ν[ψ(u(S)) − ψ(u₀)]}; start odds ≤ e^{νψ(u₀)}·posterior odds; the W2 gap is (1 − σ̃²_{S₀}/σ̂²)Z²/2 (Lemma S1, PROVED, exact to 10⁻¹³).
3. Start dichotomy (Theorem S2, PROVED under BO): concentration iff σ²/σ̂² < 1 + 1/(2A); rates n^{−1/2}, √(log p)n^{−1/2}, p^{a−1}n^{−1/2}; flooding above the threshold.
4. Cancellation masking is untouched (Theorem S3, PROVED); T38 route (a) holds without LS0 under BO (Theorem S4), but only where v3 is already favourable asymptotically.
5. Random designs: each null's exponent is (v_∅/σ̂²)χ²₁/2, inflation 1/(1 − R²) ≈ 26 at c = 1: the common-σ̂² start floods to the cap (Theorem S6; exact IID500 cell: 10^{−1303} vs v3's 10^{−12.4}, which matches the study's median).
6. The exact BO cell confirms the cure where BO holds: v3 10^{−7.5} → common σ̂² 10^{−0.5} = π(S₀); C-fix converges to S₀ in 2 steps there and runs away to |S| = K in the iid design (C-E4).
7. Recommendation: do not deploy "common σ̂², everything else unchanged"; the dilution is the right null scale in non-orthogonal designs. Residualised tables (y minus other blocks' fit) are the candidate that keeps the protection (outside scope). Pilot Step 0 (free, post hoc from saved tables) decides before any SMC run.
8. Head SHA: 025b8d6 (content commit; this line stamped in the follow-up commit).

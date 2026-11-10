DO-NOT-LOCK

## R05 findings 1–10: current-text disposition

Paths below are relative to `Theory_work/Wave3/W3-SCR/`. Quotations are from the current files. A finding marked FIXED BUT NEW PROBLEM has its original mathematical defect repaired; the residual issue is identified separately below.

| R05 finding | Disposition | Current text and assessment |
|---|---|---|
| 1. M6 drops signal/growth assumptions | FIXED | `STATEMENT.md`, SCR-M M6: “provided the resulting gaps δ_S are positive”; the illustration now specifies “θ*_1 ≠ 0 and σ fixed, x fixed, log p = o(n)”. `lemmas/L7_master.md`, M6: “δ_S > 0 for all large n when θ*_1 ≠ 0 and σ are fixed and log p = o(n).” This retains the necessary signal and growth conditions; x in this fixed-parameter illustration is understood as fixed, and STATEMENT makes that explicit. Geometry alone is no longer asserted to screen. |
| 2. Capping incorrectly forces aggregate flag FALSE | FIXED | `STATEMENT.md`, SCR-G(ii): “its own archive has `termination = "move_limit"`” and “even if the top-level `local_certified` is FALSE (the capped search itself is uncertified; the top-level flag can still be TRUE when the other search certified the same model)”. This correctly distinguishes the search archive, returned model, and aggregate flag. |
| 3. L5 incorrectly forces small α / large ω | FIXED BUT NEW PROBLEM | `lemmas/L5_exact.md`, Reading (ii): “for A > 0 is the explicit upper bound α ≤ (n/(n²−1))·exp(R_1/A − 2 log((2p−k)/k))”; (iii): “ω(S) ≥ A·(Λ_k(α(S)))₊/R_m”. It closes: “No universal bound on |E|, and no general statement that α must be small or ω large, is claimed.” `STATEMENT.md`, excess paragraph: “(EC′) says ω(S) ≥ A·(Λ)₊/R_m” and “are not claimed to force small α or large ω in general.” These exact inequalities and disclaimers repair R05. The replacement qualitative sentence about when bounds are informative still needs correction (N2); Λ also needs a definition in STATEMENT (N3). |
| 4. M4 falsely assumes κ ≤ 1 | FIXED | `lemmas/L7_master.md`, M4: “κ ≤ φ^d_n(q_n) ≤ ‖Xθ*‖²/((n−1)‖θ*‖₂²) ≤ ‖θ*‖₁²/‖θ*‖₂² ≤ ‖θ*‖₁/b ≤ M/b” and “so κb ≤ M ≤ τ_*”. This proves u* ≤ 1/26 without κ ≤ 1. |
| 5. Strict comparison missing for SCR-G | FIXED | `lemmas/L7_master.md`, M4 states “δ_S > c₂ n for every S ∈ 𝓗⁻ (so δ_𝓗 > c₂n)” and proves “δ_S ≥ nu*/2 − o(n) > nu*/4 = c₂n”. Its closing parenthesis uses “`hpm_F` − F(C) ≤ c₂n < δ_𝓗”. `STATEMENT.md`, SCR-G closes with “exceeds c₂n for all large n”. The weak application threshold now implies M2's strict comparison. |
| 6. δ_C undefined for containing models / empty family | FIXED | `STATEMENT.md`, conventions: “δ_S := +∞ for S ∈ 𝓗∖𝓗⁻; if 𝓗⁻ = ∅ then δ_𝓗 := +∞ and b_𝓗, c_𝓗 are not used (everything is vacuous).” `lemmas/L7_master.md` has the same conventions. STATEMENT M2: “every scanned centre C ∈ 𝓗⁻ has F(Ŝ) − F(C) ≥ δ_C; hence every scanned centre C ∈ 𝓗 with F(Ŝ) − F(C) < δ_𝓗 contains S₀”. L7 M2 additionally permits the defined model-specific δ_C. Both M3 statements now restrict positivity to “S ∈ 𝓗⁻”. The predicates and empty-family case are well-defined. There is a different missing hypothesis in STATEMENT M3 (N1). |
| 7. Excess paragraph lacks parameters and event scope | FIXED | `STATEMENT.md`: “m := |E|”, “Let x, x′ > 0 and let η_n(k, x) ∈ [0, 1] be the explicit quantity of L5.1”, followed by its full formula and “U(k, x) := (√k + √(2 log C(p,k) + 2x))²”. The assertion is for “every LO strict superset S of S₀ with |S| = k ≤ q ≤ K−1”. It then says “intersecting with a screening event (SCR-A / SCR-A°)” before discussing certified models. This matches L5's event and quantification. |
| 8. Optional LS0 / invocation-local meaning of unscanned | FIXED | `STATEMENT.md`, §0: “a search that was run: `fit$local_search`, and `fit$ls0` when LS0 is enabled (the default)”. `CODE_CHECK.md`, step 3: “scored as a neighbour but was **not** scanned as a centre by this search”. CC6: “of each search that was run” and “with `ls0 = FALSE` there is no `fit$ls0`”. `lemmas/L7_master.md`, M5: “not scanned as a centre of this search”; the parenthesis after M4 likewise scopes the results to “the searches that were run.” All relevant quantifiers are properly scoped. |
| 9. L6 ratio omits c_θ correction | FIXED | `lemmas/L6_sharp.md`, Consequence 2: “their ratio tends to 1, since c_θ/√Δ = √(n/(n²−1)) → 0 and Γ_n(0)/[Δ²/(n‖θ*‖₁²)] = (n+1)/n”. The exact (n+1)/n ratio is now attached only to the uncorrected expression, and the full B1 ratio is asserted only to converge to 1. Correct. |
| 10. Unsupported generic neighbour-score rate | FIXED | `STATEMENT.md`, SCR-G now closes only with: “The certified case is `hpm_F` − F(C) = 0 with C = Ŝ. Under these hypotheses the deterministic gap δ of SCR-M exceeds c₂n for all large n, L7 M4.” The generic order-log neighbour-score claim is gone. The replacement order-n gap claim is proved. |

## Newly identified findings

### N1 — MAJOR: STATEMENT M3 omits the maximising-witness hypothesis

Location: `STATEMENT.md`, SCR-M opening permits “t(S) ∈ S₀∖S a witness depending on (X, θ*, σ) only”. M3 then asserts:

> “For 𝓗 = {|S| ≤ q}: MC(q, x) ⇒ δ_S > 0 for all S ∈ 𝓗⁻, and MC°(q, x) ⇒ δ_S > 0 for all S ∈ 𝓗⁻”.

This is false for the arbitrary deterministic witnesses allowed in that statement. Visibility controls the *maximum* missing-truth gain, not the gain of every missing truth. L7 correctly includes the additional words “with the default witness” in M3, and its proof explicitly uses √γ(t|S) ≥ √Γ_n(q) (and its normalised counterpart). STATEMENT neither defines a default witness nor requires its maximisation for M3. The interface implication to GAP in §4 inherits this ambiguity.

Explicit deterministic counterexample: let p = 2, n ≥ 4, q = 0, take orthogonal centred columns of squared norm n−1, σ = 1, θ* = (1, 1/n), and fixed x = 1. Then S₀ = {1,2}, 𝓗 = {∅}, and the permitted witness t(∅) = 2 has

    γ(2|∅) = (n−1)²(n+1)/n⁴ ~ 1/n.

For this singleton family b_𝓗(1) = √2, so G_∅ = 0 eventually, u_∅ = 0, and

    δ_∅ = −B_∅ = −log 3 − ½ log n < 0.

Nevertheless Γ_n(0) = γ(1|∅) ~ n, τ_n² = 2 + n⁻², and r_n(0,1) is constant. MC(0,1) holds for all sufficiently large n: its right side is O(√log n). MC° also holds, since Ψ_n(0) is of order n and its threshold is of order √log n. Thus both printed implications fail. This is a false special-case assertion, not a failure of the underlying master theorem or of SCR-A/SCR-A°.

Fix: prepend to STATEMENT M3 “with t(S) chosen to maximise γ(t|S) over t ∈ S₀∖S (ties by smallest index)”. State the same witness choice when invoking M4 for SCR-G and when defining the GAP interface induced by SV/SV°. Alternatively explicitly define this default immediately after the arbitrary-witness construction and say M3 uses it, exactly as L7 does. No new proof or weaker screening conclusion is needed. This omission may predate v3.1; it is newly identified by this whole-statement re-lock check.

### N2 — MINOR: the new ‘informative only’ gloss is not a valid equivalence or necessary condition

Locations: `lemmas/L5_exact.md`, Reading:

> “These bounds are informative only when A is bounded away from 0 (i.e. U(k, x) ≪ n, x ≪ n) and x′ is moderate”.

`STATEMENT.md`, excess paragraph:

> “these bounds are informative only where A is bounded away from 0 (q log p ≪ n)”.

The exact bounds are correct. The new gloss is not a theorem about them. A bounded away from zero is not equivalent to U(k,x) = o(n), x = o(n): positive constant fractions can leave A bounded away from zero. Conversely, even U(k,x) = o(n), x = o(n) do not ensure A stays positive unless the coefficient-bias term ‖θ*‖₂/(σ√(n²−1)) is also controlled. Likewise q log p = o(n) alone controls neither x nor that bias. A positive A tending to zero does not by itself preclude a useful bound: usefulness depends on R_m, Λ_k(α), and the applicable comparison scale. No quantitative definition of ‘informative’ is supplied.

Fix: replace both sentences by “If A = 0, (EC′) is vacuous. For A > 0, whether these bounds are restrictive depends on their numerical values, including x, x′, the coefficient bias, and the other displayed parameters.” If sufficient asymptotic conditions are desired, list U(k,x) = o(n), x = o(n), and ‖θ*‖₂/(σn) = o(1), which give A → 1; do not call these necessary or equivalent conditions. This does not undo R05 finding 3's substantive repair.

### N3 — MINOR: STATEMENT introduces Λ without defining it

Location: `STATEMENT.md`, excess paragraph:

> “(EC′) says ω(S) ≥ A·(Λ)₊/R_m”.

Λ has not been defined in STATEMENT. L5 defines Λ_k(α), but the statement reproduces its expanded expression and then changes to a bare Λ. This fails the requested symbol-definition check.

Fix: define “Λ := 2 log((2p−k)/k) + log(α(S)(n²−1)/n)” immediately before this use, or write Λ_k(α(S)) and explicitly refer to its definition in L5. For tighter self-containment also reproduce a_1(t|S) := x_tᵀ[I−X_S(G_S+I)⁻¹X_Sᵀ]x_t + 1 when introducing the determinant ratio; currently this symbol is supplied only through the explicit L1 cross-reference, unlike Λ which has no such identification.

### N4 — MINOR: the §4 interface should distinguish a gap bound from gap positivity

Location: `STATEMENT.md`, §4:

> “GAP(𝓗) positive deterministic gap δ_S > 0 on 𝓗⁻ (consumed by SCR-M; the weakest hypothesis)”

and

> “these enter only through Lemma B ⇒ SV / SV°”.

SCR-M itself proves a lower bound without assuming gap positivity; M1 and M5 consume positivity. M2 instead consumes a strict score-to-gap comparison. Also ID/DF/AF/SF by themselves do not imply MC/MC°: the coefficient-size and growth conditions identified in A1/A1° and the numerical margin comparison are essential. The main text acknowledges this after Lemma B; the interface summary should preserve it rather than appear to assert an unconditional implication.

Fix: write “GAP(𝓗), consumed by M1/M5; M2 uses the model-specific gap bound and its comparison threshold”, and “ID/DF/AF/SF enter through Lemma B's visibility lower bounds; together with the stated coefficient/noise/growth conditions these establish SV/SV°”. Specify the maximising witness for the resulting GAP bridge (N1). This is an interface-description repair, not a new mathematical obstruction.

## Independent mathematical verification

### M4 and the strict order-n gap

The revised chain is correct. The empty model belongs to the minimisation family because q_n ≥ 0 and s₀ ≥ 1. Put V = ‖θ*‖₂² and L = ‖θ*‖₁. Standardisation gives ‖Xθ*‖ ≤ √(n−1)L, and beta-min gives V = Σ|θ*_t|² ≥ bΣ|θ*_t| = bL. Thus

    κ ≤ φ^d_n(q_n) ≤ ‖Xθ*‖²/((n−1)V) ≤ L²/V ≤ L/b ≤ M/b.

Consequently κ²b²/(26τ_*²) ≤ M²/(26τ_*²) ≤ 1/26. No κ ≤ 1 assumption is needed. With the maximising witness used by L7, Γ_n(q_n) ≥ κ²b²n/16, σr_n = o(√n), and hence G_S ≥ κ²b²n/25 uniformly eventually. The denominator bound and n ≥ 34 give u_S ≥ u* = κ²b²/(26τ_*²). For u_S < 1, −ν log(1−u_S) ≥ nu*/2; B_S = o(n) uniformly because log p + log n = o(n). Therefore δ_S > nu*/4 = c₂n uniformly. The +∞ branch is harmless. This verifies both the repaired bound and the strict inequality, including its constant.

### M2 and SCR-G(i)–(iii)

Every completely scanned missing-truth centre C in 𝓗 has its witness addition scored. CC6 gives

    F(Ŝ) ≥ F(C∪t(C)) ≥ F(C) + δ_C.

Since δ_C ≥ δ_𝓗 for such C, F(Ŝ)−F(C) < δ_𝓗 excludes all missing-truth centres. No certificate or positive-gap assumption is needed for this implication. The +∞ conventions also make L7's model-specific version meaningful.

For SCR-G choose 𝓗 = {|S| ≤ q_n}, maximising witnesses, and x_n = √log n. Under A1 plus (q_n+1)log p + log n = o(n), M4 supplies δ_𝓗 > c₂n and the master event has failure at most 4exp(−√log n) → 0. Thus (i) follows from M2 even at equality with c₂n. For (ii), M2 first screens C and then M5 screens N; both sizes ≤ q_n are precisely what makes N belong to 𝓗 and permits the swap argument's addition. For (iii), M5 applies inductively while the sizes stay ≤ q_n, including an improving cap-returned neighbour. A path that leaves the size range is not covered beyond that exit by this assertion. The completed-run qualification excludes interrupted or failed scans. Capping itself is a completed-search outcome. The certified case C = Ŝ has zero ledger gap and is consistent with the archives and enumeration interpretation.

M5's argument is sound: a deletion or swap dropping a truth leaves exactly that truth missing, so its witness is forced. In a swap, N∪t is the feasible addition C∪{l}, already scanned from C, and cannot beat the chosen best neighbour N. In a deletion, N∪t = C has strictly smaller score than N. Both contradict δ_N > 0. SCR-G's conclusions therefore follow exactly from L7; the witness omission is in the compressed STATEMENT M3, not an obstruction to choosing the witnesses needed for SCR-G.

### Exact reading of EC′ and the L6 ratio

Let c = (n²−1)/n and L_k = 2log((2p−k)/k). R_m is the positive squared bracket (indeed R_m ≥ 1). For m = 1, ω = 1 and EC′ is A(L_k+log(cα))₊ ≤ R_1. When A > 0, R_1/A ≥ 0, so z₊ ≤ R_1/A is equivalent to z ≤ R_1/A. Exponentiating gives exactly

    α ≤ n/(n²−1) · exp(R_1/A − 2log((2p−k)/k)).

No branch of the positive part is lost. For general m division by R_m > 0 gives exactly ω ≥ A(Λ_k(α))₊/R_m, including A = 0 where the condition is vacuous. Neither expression by itself forces small α or large ω. These requested algebraic repairs pass.

For L6 Consequence 2 the ratio to the full B1 expression is

    Γ_n(0) / [Δ(√Δ−c_θ)²/(n‖θ*‖₁²)]
      = ((n+1)/n)/(1−√(n/(n²−1)))² → 1.

The revised text correctly separates the exact ratio to Δ²/(n‖θ*‖₁²) from this limiting ratio. The (log n)²/n rate and screening counterexample remain intact.

## Whole-statement, probability, code, and target-card check

I reread all of STATEMENT v3.1 and compared it with L3, L5, L7, CODE_CHECK, PROGRAM item 5, and PROTOCOL items 4–5. I also inspected the actual local-search scan/cap implementation, `eval`, ledger offering, final/LS0 invocation, and R output/flag assembly in `Scripts/SMC_BVS/core/`. This was a static mathematical/code review; no simulations, subagents, or Git commands were used. Only this report was written.

* SCR-A's 3e^{-x} and SCR-A°'s 4e^{-x} match L3's event constructions. SCR-M's 4e^{-x} is one witness event, one cross-term event, and the two E2⁺ failures; L7's crude-denominator alternative saves the cross-term event and gives 3e^{-x}. Calling the original SCR-A a special case does not require worsening its direct 3e^{-x} bound: L7 explicitly permits the crude branch.
* The excess-set probability matches L5/L2: e^{-x} for E2ᶜʰⁱ, 2qe^{-x} for E3a, and e^{-x′}/(1−e^{-x′}) for E3b. The certified-model representation explicitly intersects a screening event. SCR-C's bounded-s₀, bias, growth, and superset-floor hypotheses match L5; SCR-R's prediction/refit distinction and bound also match it. The q < s₀ cases are vacuous on the screening event. No new discrepancy in these probability bounds or hypotheses was found.
* A1/A1° retain the coefficient and growth conditions used in L3. Bridge formulas and directional-floor definitions match their uses. Symbols are supplied locally or through named lemma cross-references except for N3; repeated symbols such as M and G_S have local scopes, with SCR-G's M supplied by its A1 hypotheses. The witness restriction needed for M3 is the significant missing hypothesis (N1).
* The code appends `scan_complete=1` only after both complete neighbourhood loops. Every considered neighbour calls `eval`; fresh scores reach the ledger and cache hits retain the previous offer. The final search's non-emitting initial centre is already the ledger HPM. The cap branch requires strict improvement and returns the best neighbour after recording the scan; the no-improvement branch certifies the current centre. LS0 is optional, uses the same ledger/cache, and emits its initial centre. R keeps archives only when present and combines the two HPM-matching certificates with logical OR. These facts support CC1–CC6 and SCR-M M1/M2/M5 and SCR-G without assuming that aggregate `local_limit` negates aggregate `local_certified`.
* §3 correctly declines claims about the probability of certification, size-K screening, arbitrary uncertified HPMs outside SCR-G, general excess-size bounds, PIPs/MPM/evidence, and floating-point guarantees. SCR-N is restricted to the empty-model LO threshold, not a claim that the algorithm outputs ∅. M6's orthogonal example is explicitly an illustration with conditions, not an imposed design family.
* PROGRAM item 5 is delivered by A1: sparse-floor ⇒ anchored-floor ⇒ directional-floor, with explicit signal and growth hypotheses, no start/leakage condition, and the exact coded meaning of the certificate. The broader non-asymptotic and geometric statements preserve that target. PROTOCOL item 4 is respected: theorem hypotheses use deterministic functional properties rather than named design families. The interface ids G, EX-A, GAP, SV/SV°, ID, DF, AF, SF, NF are consistent with the intended dependencies, subject to the qualifiers in N1/N4. NF is an additional exact-recovery condition, not a prerequisite for screening.

The ten R05 defects have their substantive repairs in place. I cannot lock the current statement unchanged because N1 is an explicit false implication with an admissible deterministic counterexample. Its repair is local and already present in the full lemma; N2–N4 are wording/interface repairs. I found no need to weaken SCR-G, the master gap bound, or the target certified-screening theorem.

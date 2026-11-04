# STATEMENT.md — T20 (T15), clauses (i)–(ii): local-search semantics

Source: `Theory_architecture_v3/theorems/T20_T15_local_search.md` (clauses (i)–(ii) only; (iii)–(v) are out of scope). Method: SMC-BVS v3.0, `Methodology/SMC_BVS_v3_20261019/METHODOLOGY_v3.md`, SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c (checked 2026-10-22). Statement analysis outcome: **(a) correct as stated**; no hypothesis was changed or added. Section 5 lists the readings used to make the informal wording precise.

## 0. Original clauses (verbatim)

> (i) [certificate] `local_certified` certifies exactly that the returned model was itself scanned as a centre and had no strictly improving feasible flip or swap within the cap; equal-score neighbours are allowed; weak local maximality only. All scanned candidates, including rejected ones, enter the running HPM comparison; a model first discovered by the final extra scan can be the reported HPM without a certificate.
>
> (ii) [one neighbour] On E_n, every completed scan from a feasible flip-or-swap neighbour of S₀ scores S₀; if a move remains the search moves to S₀; if the subsequent scan executes it certifies S₀. Under T03, P₀(E_n) → 1, and a sufficient global margin is min_{S≠S₀}{F(S₀) − F(S)} ≥ log[π(S₀)/(1−π(S₀))] ≥ ½ log n − ½ log log n − O_{P₀}(1).

Assumptions named by the source for (i)–(ii): EX-A (exact scores and comparisons) and execution of the relevant scans; for the statistical reading, G, R, SE and BM-C or BM-∞ through T03. The source defines (its "Definitions used"): "E_n := {S₀ is the strict global maximiser of F}".

Method text formalised in §2 (METHODOLOGY_v3 §6.10, verbatim): "**Local search:** from the current best scored model (the centre), scan every feasible flip and swap (additions beyond K excluded) with the centre frozen during the scan; move to the best strict improvement (lexicographic ties); at most ℓ moves, then one further scan; stop earlier when a scan finds no improvement. Every evaluated model updates the global best. If the last scan still improves, set `local_limit` (no restart). `local_certified` only when the returned model is a scanned centre with no improving neighbour. The search never alters particles." and "**HPM:** the strict maximum of log ϖ(S) + log m(S) over every model ever scored (tables, pilot, calibration, final rounds, rejected proposals, independence proposals, local searches), kept as a running best that survives cache eviction. Only exactly equal scores invoke the tie rule: smallest |S|, then lexicographically smallest index set." Execution order (§6.1/§7): "… final local search; final checks (flags only); report" — nothing is scored after the final local search. ℓ = ⌈log₂(n + p + 1)⌉ (§3).

## 1. Setting

- p ≥ 1 predictors, n ≥ 3, K = min(p, ⌊n/2⌋) ≥ 1, state space Ω = {S ⊆ [p] : |S| ≤ K}.
- **Score.** F : Ω → ℝ. Clause (i) and the deterministic part of clause (ii) are proved for an **arbitrary** F : Ω → ℝ; only (ii-B)–(ii-C) use the method's score F(S) = log[ϖ(S) m(S)], π(S) = e^{F(S)}/Σ_{T∈Ω} e^{F(T)} for S ∈ Ω, and the convention π(S) := 0 for S ∉ Ω. The method's score (00_COMMON §1; METHODOLOGY_v3 §5), on standardised data X ∈ ℝ^{n×p}, y ∈ ℝⁿ (y ≠ 0; columns and y centred, ‖x_j‖² = ‖y‖² = n − 1): for S ∈ Ω with k = |S|, X_S the columns in S, G_S = X_SᵀX_S, z_S = X_Sᵀy, H_S = (n+1)G_S + I_k, D_S = det H_S / det(G_S + I_k), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S (for S = ∅: D_∅ = 1, Q_∅ = yᵀy); a₀ = b₀ = 0.01, ν = a₀ + n/2;
  m(S) = (2b₀)^{a₀} Γ(ν) / (π^{n/2} Γ(a₀)) · D_S^{−1/2} (2b₀ + Q_S)^{−ν};
  w(k) = ½ / C(2p−1, k), W_K = Σ_{j≤K} C(p, j) w(j), ϖ(S) = w(|S|)/W_K.
  (This is the marginal likelihood of the model y | β_S, σ² ~ N(X_Sβ_S, σ²I), β_S | σ² ~ N(0, nσ²(G_S+I)⁻¹), σ² ~ IG(a₀, b₀), times the beta-binomial BB(1, p) prior capped at K; the proof uses only the displayed formulas.)
- **EX-A.** All scores are exact real numbers and all comparisons are exact.
- **HPM order ≻** (method §6.10): S ≻ T iff F(S) > F(T); or F(S) = F(T) and |S| < |T|; or F(S) = F(T), |S| = |T| and the increasingly sorted index list of S is lexicographically smaller than that of T. This is a strict total order on Ω. For a finite nonempty 𝒜 ⊆ Ω, best(𝒜) is its ≻-maximum. The running HPM after any step is best(𝒮) where 𝒮 is the set of all models scored so far in the run (tables, pilot, calibration, final rounds, accepted and rejected proposals including independence proposals, local scans).
- **Move order ▷.** A fixed strict total order on Ω with F(S) > F(T) ⇒ S ▷ T (maximise F, exact ties broken by a fixed deterministic rule; the method says "lexicographic ties"). Every result holds for every such rule.
- **Feasible flip-or-swap neighbourhood** of c ∈ Ω:
  𝒩(c) = {c ∪ {j} : j ∉ c, |c| < K} ∪ {c ∖ {i} : i ∈ c} ∪ {(c ∖ {i}) ∪ {j} : i ∈ c, j ∉ c} ⊆ Ω.
  (All swaps, not only neighbour-graph swaps; additions beyond K excluded.) The relation N ∈ 𝒩(c) is symmetric on Ω.

## 2. The local search (method §6.10), as formalised

Input: the finite nonempty set 𝒮⁻ ⊆ Ω of models scored in the run before the search starts; the move cap ℓ ≥ 0 (the method has ℓ = ⌈log₂(n+p+1)⌉).

```
c_0 := best(𝒮⁻);  𝒮 := 𝒮⁻;  k := 0
loop:
   scan k (centre c_k frozen): 𝒮 := 𝒮 ∪ 𝒩(c_k)          # every neighbour scored; running HPM updated
   I_k := {N ∈ 𝒩(c_k) : F(N) > F(c_k)}                    # strict improvements over the centre
   if I_k = ∅:  stop; outcome NOIMP; m := k
   elif k < ℓ:  c_{k+1} := the ▷-maximum of I_k; k := k + 1  # a move
   else (k = ℓ): stop; outcome LIMIT; m := ℓ                 # the "one further scan" still improved
```

Outputs: centres 𝒞 = {c_0, …, c_m}; final scored set 𝒮_end; **returned model R := best(𝒮_end)** (the running HPM when the search ends); `local_limit` := 1 iff outcome LIMIT; **`local_certified` := 1 iff R ∈ 𝒞 and there is no N ∈ 𝒩(R) with F(N) > F(R)** (method: "`local_certified` only when the returned model is a scanned centre with no improving neighbour").

The run may contain several local searches (after the pilot, after each set of diagnostic islands, after the final run); between them the scored set may grow. In the method nothing is scored after the final local search, so for the final search R equals the reported HPM Ŝ.

**Execution hypothesis (EXEC).** Every scan that the procedure calls is completed, i.e. all of 𝒩(c_k) is scored.

## 3. Clause (i): certificate semantics (EX-A, EXEC; arbitrary F)

For any execution of one local search:

- **(i-a) Characterisation.** `local_certified` = 1 iff the outcome is NOIMP and R = c_m. In that case F(R) = max_{𝒮_end} F and F(R) ≥ F(N) for every N ∈ 𝒩(R) (weak local maximality over the feasible flips and swaps; neighbours with F(N) = F(R) are permitted, and every such neighbour N satisfies R ≻ N, i.e. |N| > |R|, or |N| = |R| and N is lexicographically later). Moreover R ∈ 𝒞 holds iff R was a scan centre in any local search of the run up to and including this one.
- **(i-b) Only weak local information.** The whole execution (centres, outcome, 𝒮_end, R, both flags) is unchanged if F is replaced by any F′ : Ω → ℝ with F′ = F on 𝒮_end, the F′-run using the same input 𝒮⁻, the same ℓ, the HPM order ≻ computed from F′, and the move order computed from F′ with the same fixed tie-break rule. Hence `local_certified` = 1 carries no information about F on Ω ∖ 𝒮_end; in particular, when Ω ∖ 𝒮_end ≠ ∅ it does not certify global maximality (when 𝒮_end = Ω, R is the global maximiser of F trivially).
- **(i-c) Ledger.** Every model scored by any scan of the search, whether or not it was selected as a move, belongs to 𝒮_end, so R ⪰ N (R = N or R ≻ N) for each of them; in particular F(R) ≥ F(N). For the final search R = Ŝ.
- **(i-d) Final extra scan.** On outcome LIMIT: R ∈ 𝒩(c_ℓ), F(R) > F(c_ℓ), R was first scored by scan ℓ (R ∉ the scored set before scan ℓ), R was never a scan centre of any local search of the run up to this one, and `local_certified` = 0. For the final search this R is the reported HPM Ŝ.
- **(i-e) Generic case.** If exactly one model of 𝒮_end attains max_{𝒮_end} F, then `local_certified` = 1 ⟺ outcome NOIMP ⟺ `local_limit` = 0.

## 4. Clause (ii): one neighbour of S₀

Let S₀ ⊆ [p] be the true support and **E_n := {S₀ ∈ Ω and F(S₀) > F(S) for every S ∈ Ω ∖ {S₀}}**.

**(ii-A) Deterministic (EX-A, EXEC; arbitrary F).** On E_n, for every local search of the run and every scan k of it whose centre c_k is a feasible flip-or-swap neighbour of S₀ (c_k ∈ 𝒩(S₀)):
1. scan k scores S₀ (S₀ ∈ 𝒩(c_k));
2. S₀ ∈ I_k and S₀ is the ▷-maximum of I_k; if k < ℓ (a move remains), c_{k+1} = S₀;
3. if k < ℓ, scan k+1 (with centre S₀) is called by the procedure; it finds I_{k+1} = ∅, the search stops with outcome NOIMP, R = S₀ and `local_certified` = 1;
4. if k = ℓ (no move remains), the search stops with outcome LIMIT, R = S₀ and `local_certified` = 0.
In both cases S₀ is the running HPM from the moment scan k scores it; for the final search Ŝ = S₀.

**(ii-B) Margin inequality (method's F; deterministic).** If S₀ ∈ Ω then 0 < π(S₀) < 1 and
  Δ_n := min_{S∈Ω∖{S₀}} [F(S₀) − F(S)] ≥ λ_n := log[π(S₀)/(1 − π(S₀))].
Consequently {π(S₀) > ½} ⊆ E_n.

**(ii-C) Statistical (method's F).** Regime: a sequence of problems indexed by n → ∞ (design fixed, P₀ = law of the Gaussian errors), r_n := √(log n / n). Hypothesis **H03** (the conclusion of T03(i), conjectured there under R1 with G, R, SE and BM-C or BM-∞; it is used here only as a hypothesis): there is n₀ with S₀ ∈ Ω for all n ≥ n₀, and 1 − π(S₀) = O_{P₀}(r_n). Under H03:
1. P₀(E_n) → 1;
2. (½ log n − ½ log log n − λ_n)⁺ = O_{P₀}(1) (over n ≥ n₀), i.e. Δ_n ≥ λ_n ≥ ½ log n − ½ log log n − O_{P₀}(1);
3. under EX-A and EXEC, for any joint law of data and algorithm randomness whose data marginal is P₀, the probability that conclusions (ii-A)1–4 hold simultaneously for every scan of every local search of the run is at least P₀(E_n), hence tends to 1.

## 5. Readings used (the informal text made precise)

1. "Returned model" = the running HPM when the search ends (R above); this matches the source's "a model first discovered by the final extra scan can be the reported HPM without a certificate". If one instead read it as the last centre c_m: on outcome LIMIT, R ≠ c_m (by (i-d), F(R) > F(c_m)), but the flag is 0 under both readings (c_m has a strictly improving neighbour); on outcome NOIMP, R = c_m unless another model of 𝒮_end has exactly the score F(c_m) and precedes c_m in the HPM order. So the two readings give different flag values only on NOIMP with such an exact tie.
2. "Scanned as a centre" = R ∈ 𝒞; (i-a) shows this is the same as having been a centre in any local search of the run up to and including the current one.
3. "Within the cap" = among feasible models, |S| ≤ K. (Reading it as the move cap ℓ gives nothing different: certification implies outcome NOIMP at some m ≤ ℓ.) The method's "`local_certified` only when …" is read as "iff", as the source's "certifies exactly that" requires.
4. "Weak local maximality only" is made precise by (i-a) (what is implied) and (i-b) (nothing about unscored models is implied).
5. "Can be the reported HPM without a certificate" is made precise by (i-d): on outcome LIMIT the reported model is such a model and is uncertified. Whether outcome LIMIT has positive probability for given data is not asserted. (A second, tie-only route to an uncertified reported model also exists: on NOIMP, if some scored model has exactly the score F(c_m) and precedes c_m in the HPM order, then R is the HPM-first of all such models (it may be a neighbour of c_m or a model scored earlier), R ≠ c_m, and both flags are 0; (i-a) covers it.)
6. "If the subsequent scan executes" = EXEC; in the procedure a scan always follows a move (a regular scan or the one further scan).
7. "Under T03" = hypothesis H03; "a sufficient global margin is … ≥ …" = the chain Δ_n ≥ λ_n ≥ ½ log n − ½ log log n − O_{P₀}(1) of (ii-B)–(ii-C), with Δ_n > 0 equivalent to E_n when S₀ ∈ Ω.

## 6. Change log

- v3 → v3.1 (2026-10-22, after the Stage B ruling round; text of §1 and §5 only, proof unchanged): §5 item 5 tie-route sentence made precise (Opus N1 = Astra #2 exposition finding); §1 list of HPM sources now names independence proposals (Opus N2).
- v2 → v3 (2026-10-22, after the Stage B reviews; exposition only, no hypothesis added or changed): verbatim source text for E_n and for METHODOLOGY_v3 §6.10 added to §0; (i-a) states that equal-score neighbours of a certified R come after R in the HPM order; (i-b) says which move order the F′-run uses and qualifies "does not certify global maximality" by Ω ∖ 𝒮_end ≠ ∅; (ii-A) closing sentence "from the moment scan k scores it"; (ii-C)3 names EX-A and EXEC; §5 items 3 and 5 extended.
- v1 → v2 (2026-10-22, after Astra #1 round 1; no hypothesis or claim of §§3–4 changed): §1 now writes out the method's score formulas (Q_S, D_S, m, ϖ) in full, so the statement is self-contained; §5 item 1 corrected (the two readings of "returned model" also differ on outcome LIMIT, where both give flag 0); §5 item 2 wording corrected ("up to and including the current one").

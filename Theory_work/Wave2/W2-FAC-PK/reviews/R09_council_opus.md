# W2-FAC-PK — council round 1, Claude seat (Opus 5.5)

**Score: 9.1 / 10. All six gates PASS. Required fixes: 1 minor and 4 editorial (listed below). None of them affects a claim.**

Scope of the review: STATEMENT v3.1, L0–L4, METHOD_REQUIREMENTS, REPORT, and R01–R07 with their dispositions. I compared
the sources FACB L1/L2/L4.0/L5, W1-GEN [OP], FINAL s7 (Lemma CAP, loop rule (L3)) and CITECHECK against the production
code: `v3_engine.h:379–418` (local_search), `v3_core.cpp:394–404, 466–481`, `v3_run.R:95–101` and `v3_fit.R:35–62, 114–145`.
I re-derived every inequality chain by hand. I ran no numerics and wrote no scratch files; the reviewer reruns in R04 and R07
already cover the saved aggregates.

## Gate verdicts

**1. Correctness (L0–L4): PASS.** I tried to break the following steps; each one holds.
* L0. The τ-form gives G_sw ≥ M_T·V because −log(1 − v) ≥ v. Prior ratio: for BB(1, p), w(k−1)/w(k) = (2p−k)/k. Also checked
  the bounds on M_T in L0.5(c).
* L1(a). FACB L2.3(i) carries over: truth-free U gives V = S₀ and c = (1−ρ)ρθ̄/(1+(u−1)ρ) > 0. The case u = 0 gives c = ρθ̄.
  The proof needs only |S| < K and the counting bound p − 16s₀ ≥ K + 1.
* L1(b). Exchange factorisation. The bracket equals 2κ_cκ/(u+κ) + κ₁E, and κ_c is of order n while κ₁H̄ = O(√(n log n)).
  The constant in |E| ≤ 5H̄ is off; see editorial E2.
* L1(c). Concavity: h″ < 0 because (1−A)(u+κ) < (1−A)u+κ. A_n → A < 1. The four O(√n·H̄) remainders are dominated by
  c_g·n.
* L1(d). Counting against liminf p/K > 16/15.
* L2.1, event (N2). φ(t_n) = n^{−1/2}·e^{−17−2√(log n+30)}/√(2π). The regular blocks are deterministic given the fixed X, so
  their minima are independent. The mean is n^{1/2−o(1)}, which dominates n^β.
* L2.2.
  * (i) Δ_K < ½ log n + 1.2.
  * (ii) The decomposition V = (1−γ)(t_l−t_j)² + 2t_j(t_l−t_j) is correct.
  * (iii) |x_T| ≤ 2 holds because Σ|ξ| ≤ 0.81p ≤ 0.81(2K+1). The step "|ξ_j| > 1.5 ⇒ count ≤ 0.14p < K − s₀" leaves a null
    j ∈ T with |τ_j| ≤ 3.5. τ_l² ≥ log n + 30, so V ≥ log n + 5; the bound is conservative (about log n + 17 is available).
    M_T ≥ ½(1 − 3n^{−1/3}), so G_sw ≥ ½ log n + 2 > Δ_K.
* L2.3 and L2.4. The induction uses only that each move adds at most one variable, and L1(d) gives O* ∩ C₀ = ∅. The
  counting "deletions ≤ max(0, i − N_n) ⇒ |C_i| ≥ s₀ + 2" holds. It is consistent with the code: when the run hits the cap,
  the improving neighbour it returns belongs to N(C_a), so it is already in the scored set.
* L3 events.
  * (E3): the Bernstein step P(Bin ≥ 2p′q + λ) ≤ e^{−3λ/8} holds; the grid interpolation adds ≤ 2p/n; the tails are handled.
  * (E4): (n−1−p) + (p−K) = n−1−K ≥ n/2 − 1 forces one of the two cases. Φ([p]) − Φ(T) ~ χ²_{p−|T|} for every T. The union
    bound gives 2ⁿ·2^{−9n/8} → 0.
  * (M2): Φ(T) ≤ ‖g_T‖²/(1−ρ).
* L3(a)–(e).
  * (b): the ½h terms cancel exactly, leaving O(L_n·H̄) = o(log n).
  * (c), two-sided case: d_T ≤ H̄ and γ_{k−1} ≤ 1/(s₀+1+κ_∞) give c_D.
  * (c), one-sided case: (1+γ_{k−1})d_T² ≤ t·h/(t+1).
  * (d) Step 1 counting: S₊ = d·U₊(x+d) + ∫U₊ is correct.
  * (d) Step 3: Mills' ratio gives 6 + 2a, and m > ⌈log² n⌉ ≫ 12·H̄·log n.
  * (d-i)/(d-ii): with c₀ = ε/(8C_M), 2C_M·2c₀ = ε/2.
  * Small-d case: the bound Δ_k − 2C_M holds.
* L3.4.
  * The proof order is sound: endpoint first, then the bound F(C_i) ≤ F(S₀), then the budgets.
  * Phase A: Σ_{k=s₀+1}^{K} Δ_k + O(n), divided by c₃n, is O(log n).
  * The bound log C(2p−1, K) ≤ K(1 + log 4) ≤ 2.39K holds.
  * Constant check: the ratio K(½ log n + 2.4)/((½−ε) log n) tends to K/(1−2ε). This is < (1+6ε)K whenever ε < 1/3, which
    covers the whole range ε < c_D/2 < ¼. The choice ε = min(δ/12, c_D/4) then gives m* ≤ (1+δ/2)K + O(log² n).
* L4: (H0) with A = 1; [OP] does not depend on the cap value; inclusion D′; and the cap rule max(ℓ_n + |S̃₀|, p) is
  ≥ ⌈17|S̃₀|/16⌉ on every input.

**2. Hypotheses used = hypotheses stated: PASS.**
* (P1)(a)(b) need only (PK′) and blocks ≤ 16; (c)(d) also need (PK) and (PB).
* (P2) needs (PK) and (PB). (PB) is used through the regular blocks in (N2) and through L1(d). Every ϑ_r ≠ 0 is used in
  L2.2(ii) and is included in (θ).
* (P3) needs (PK′) and does not need (PB), (TK) or the 16/15 condition, as stated.
* (P4)(iii) carries the (α)/(β) narrowing, and it is flagged.
* (PB) is kept as a hypothesis; the L1.4(3) partition argument is labelled as a sketch.

**3. No hidden assumptions: PASS, with fix M1.**
* Events: E^S, E^N, E1–E4 and 𝒟_n are explicit.
* Uniformity: E3 holds for every real t, and E4 holds for every T ∈ 𝒯 (it is used at the data-dependent point t = a).
* Ties: 𝒟_n handles ties in ξ. L2.2 says the maximum is "attained only by swaps", so the lexicographic tie-break in the code
  does not matter. L3 needs only the gain of the chosen move, which is at least the best deletion.
* Cap-rule evaluation: covered by (β).
* Imports: each one is re-read for p ≤ n − 1. The bulk bound of FACB L4.0(d) and FACB's E2 lower bound on r are correctly
  excluded.
* Fix M1 concerns the delivery claim's code premise.

**4. Citations and statuses: PASS.**
* I checked these verbatim: [OP] "PROVED (by this seat, unchecked)" (W1-GEN STATEMENT:169); GEN "PROVED-CHECKED" (W1-GEN
  REPORT:20); Lemma CAP's council history (s7:63–64); and the FACB statuses as recorded.
* No status is upgraded. L0–L4 are marked "PROVED (by this seat, unchecked)" together with their lemma-check verdicts.
* CITECHECK reports 38 citations checked and 0 misses. Its summary line conflicts with REPORT §3, which says 33; see E5.

**5. Constants and rates: PASS.**
* All o(1) and O(log log n) terms are dominated.
* L_n·H̄ = O(√log n · log log n) = o(log n).
* The constant chain c_D → ε < c_D/2 → c₀ = ε/(8C_M) → threshold n^{1−c₀} is consistent; c_D > 0 because s₀ ≥ 1 and
  κ_∞ > 0.
* The δ ↔ ε choice is consistent. c₃ and c₅ are handled; see E3 for the definition of c₅.
* The (P5) slack β′ ∈ (β, ½) is correct.

**6. Fidelity to the coded method: PASS, with fix M1.** These code facts match the deliverable:
* Loop rule: the code completes the full scan of the current centre and picks the best neighbour (lexicographic ties). On a
  strict improvement it either moves, or, if `A.moves >= ell`, stops with `move_limit` and returns that neighbour. Otherwise
  it stops certified (`v3_engine.h:385–413`). This gives the prefix property used in L2.4 and Theorem PATH.
* Additions are skipped at size ≥ K; swaps are scanned at every size. Each scan has at most q(p) = p + p²/4 entries.
* MR1 cap: `ls0_ell + |m.S|`, computed after `start_mode` (`v3_core.cpp:473`).
* Preflight: scans `b$ell + K + 1`, requests × (p + p²/4), time 2·requests·ŝ_K, and the archive formula (`v3_fit.R:44–47`).
  These match the formulas in L4.2 and METHOD_REQUIREMENTS.
* Plumbing: the description of the current plumbing (`v3_run.R:101` collapses every non-legacy value; the Boolean at
  `v3_core.cpp:394/404`) is accurate.

## Required fixes

**M1 (minor; gates 3 and 6). The delivery claim refers to code that does not exist yet.**
* STATEMENT (P4)(iii) and L4.2(iii) end with "the … code-audit qualifications of Proposition F are inherited."
* Proposition F's exit inventory (P1, AUDITED) and S.3 audit the head code. The head code cannot select any MR-PK rule:
  `v3_run.R:101` maps every non-legacy value to MR1, and `v3_fit.R:44` charges ℓ_n + K + 1 scans.
* So (iii) is a statement about the method with the rule plumbed as METHOD_REQUIREMENTS specifies. The changed lines are not
  covered by any audit: the cap selection and its range-check `stop` at `v3_core.cpp:473–474`, the rule-specific scan count
  in both preflights, and the labels.
* Fix: add one sentence to STATEMENT (P4)(iii) and to L4.2(iii) along these lines: "for the method with the rule implemented
  as in METHOD_REQUIREMENTS (not done by this ticket); Proposition F's code audit is inherited for unchanged code, and the
  changed lines are an implementation premise requiring the same audit (the range-check exit is unreachable because
  a ≤ ℓ_n + 2K < INT_MAX)."
* This is a declaration fix only. The mathematics is unaffected.

**E1 (editorial). L3.4, phase A.** It cites L2.2(i) for "every deletion gains ≤ Δ_K". As stated, L2.2 holds on
E^S ∩ E^N ∩ 𝒟 under (PK) and (PB), and (P3) assumes neither. Part (i) is deterministic: it uses only L0.3, L0.5(a) and
p ≤ 2K + 1. Say so, so that (P3) visibly does not depend on (N1), (N2) or (PB).

**E2 (editorial). L1(b): |E| ≤ 5H̄ should be |E| ≤ 6H̄.**
* When κ < 1 (ρ > ½) and u = 1, the term γ_u(ξ_{l′} − ξ_l) contributes up to 2H̄/(1+κ) > H̄.
* The total bound is |E| ≤ (2 + 2(u+1)/(u+κ))H̄ ≤ 6H̄.
* No consequence, since only O(H̄) matters.

**E3 (editorial). L2.2(ii): define c₅ := min(c₄²/8, ½)**, as L3(e) does. Alternatively, note that nV/(αψ_T) < 1
automatically. As written, "c₄²/8 =: c₅ ∈ (0, 1)" is asserted, not derived.

**E4 (editorial). L1(a) proof: "implied by (PK) for n ≥ n₀" should say "this is (PK′)".** Parts (a) and (b) are stated
under (PK′) alone.

**E5 (editorial). The citation count is inconsistent.** REPORT §3 says "33 checked" and CITECHECK.txt ends with
"38 citations checked, 0 misses". Align them.

## Optional suggestions

1. **Plumbing: use the same base cap in the preflight and in LS0.** The preflight charges `b$ell`, but LS0 uses
   `ro$ls0_ell`. These differ under the testing option `v3.ls0_ell`, which is outside CONFIG. When the rule is plumbed,
   compute the preflight's worst-case scan count from the same validated value that LS0 uses, so the charge can never
   understate the cap.
2. **L2.2(iii) slack.** The bound V ≥ log n + 5 throws away about 12 units; (1+γ_K)·12.25 is about 12.3, not 24.6. Harmless,
   but a remark could note that the threshold t_n could be lowered. That would not change the n^{1/2−o(1)} count.
3. **L3_trend.txt.** At m ≈ K (d-ii regime) the ratio of best-deletion gain to log n is about 0.28–0.33 and rises only
   slowly with n. The cause is an O(1) offset M_T·d² ≈ 3, with M_T ≈ 6.5. That matches the asymptotic argument
   (ratio → ½ − ε). A one-line note in L3.5 would stop readers from mistaking it for a counterexample.
4. **REPORT §6 (G2).** State that the χ² union bound needs only n − 1 − K ≥ n/2 − 1, i.e. |T| ≤ K ≤ n/2. Do not phrase it
   through p. That is what makes it design-free for W2-UNI.

## Summary

The negative result, Theorem NEG, is a clean static argument, and it is correct. The saturation and within-block order
(L1), the static scan bounds at size K (L2.2) and the counting step (L2.3–L2.4) together show that any additive slack of
size o(n^{1/2}) fails. The positive result, Theorem PATH, is also correct: the uniform gain bounds over the lattice above S₀
(centring identity, tail counts, χ² residual floor) combine with the F-budget to give m* ≤ (1+δ)K. I re-checked every
constant chain and found no gap. The narrowings are declared honestly: the exact-Gram stage only, frontiers F1/F2/F2′,
(P6) numerical and pending, and the (P4)(iii) cost restriction. The only substantive item is the declaration in M1. Score
9.1.

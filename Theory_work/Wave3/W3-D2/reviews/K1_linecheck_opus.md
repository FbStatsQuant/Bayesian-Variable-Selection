# W3-D2 — K1 line check of `PROOF.md` v1.0 (blind; Claude Opus 5.5, high; 2026-11-17)

Brief: `reviews/K1_brief.md`. Object: `Theory_work/Wave3/W3-D2/PROOF.md` (P0–P4) against `STATEMENT.md` v1.1 §§0–3.
Not read: LOG.md, CHECKPOINT_*, other files in `reviews/`. Sources read at the cited lines: [MISR-R] `:1-120`;
`W3-MISR-R/lemmas/G2_corr.md` (all); [MISR] `:17-66`, `:108-123`; [W3P] `:16-39`; [R1] (all, B1.3 and B4.1 in
particular); [RV] `:20-32`, `:257-284`, `:445-466`; `W3-READER/NOTATION.md` §1. Registry claims taken as quoted in the brief.
How I read the tags (the brief does not define them): **C** = a step is false or does not follow; **S** = the step is
true, but the text leaves out a needed justification; **F** = a citation or attribution is not exact (fidelity);
**E** = editorial.

## Verdicts per unit

| unit | verdict |
|---|---|
| P0 (deterministic facts) | **VERIFIED** |
| P1 (instance of CorGb-plus) | **VERIFIED-WITH-AMENDMENTS** (K1-1 S, K1-2 F, K1-4 E) |
| P2 (remaining displays, b_n = O(r_n)) | **VERIFIED** |
| P3 (Corollary 2X) | **VERIFIED-WITH-AMENDMENTS** (K1-3 F) |
| (P4, not a proof unit) | one wording item, K1-3 |

## The named points

1. **q = 0 instance.** [MISR-R] `:52` allows q = q_n ≥ 0, so q = 0 is allowed. With X^r_𝓜β_𝓜 ≡ 0 ∈ ℝⁿ and the constant maps
   a ≡ 0, γ ≡ 0, τ² ≡ 0 (τ² takes values in [0, ∞), `:57`), (OV) at `:67-68` reads "conditionally on X^r_𝒞,
   0 ~ N_n(0, 0·I_n) = δ₀". This holds trivially under the convention N_k(m, 0) := δ_m (`:31`) and the
   conditional-law definition at `:29-31`. (N) at `:56` holds: σ² > 0 is deterministic, and ε is independent of
   (X^r, empty). σ²_𝒞 = σ² > 0 (`:98`). a, γ, τ² are deterministic, as `:97-98` requires. α: §0 assumes it deterministic,
   which is allowed by `:52-53` (any real random variable). **Correct.**
2. **π_𝒞 = π.** [MISR] `:21-22` says verbatim "π_𝒞(· | x, y^r) is the coded target of [W3P] §0 (lines 16-29) computed from
   (x, y^r)". STATEMENT §0 `:22-25` defines π as the same object computed from (X^r, y^r), with the same Ω and K. The
   convention π(T) := 0 off Ω agrees ([MISR] `:28` vs STATEMENT `:26`). π_𝒞 needs non-constant columns
   (p ≥ 1 retained) and a non-constant y^r. Both hold almost surely: Σ_jj > 0, n ≥ 2 and σ² > 0. supp β^𝒞 = supp β = S₀,
   so the two δ_n agree, and so do the HPMs (both are "any tie rule", [MISR] `:24`, `:28`). **Correct.** (Citation range: K1-4.)
3. **Floor step.** The master's floor is on |T| ≤ k_n = s + max(j₀, m♯_n), where m♯_n is that of [MISR] `:34` = [W3P]
   `:36-39` with p = |𝒞|. B4.1 ([R1] `:43-45`) gives k_n ≤ 3(A + 1)(s + 1) log n for s ≤ K. Its proof also needs n ≥ 3, A ≥ 1 and
   s ≥ 1 ([R1] `:7`), and p ≤ n^A, which B1.3 uses at `:25` (C(p, s) ≤ n^{As}); see K1-2. For n ≥ max(3, 2s₀):
   p ≥ s₀ because S₀ ⊆ [p], and ⌊n/2⌋ ≥ s₀, so s₀ ≤ K. Every non-empty T with |T| ≤ k_n is then covered by (A2).
   The master's proof uses only non-empty T (G2 step 2, `:30`; step 3 uses supp β^𝒞, which is non-empty, `:35-36`). **Correct.**
   The handling of n < 2s₀ is right but left implicit; see K1-1.
4. **C depends only on (s₀, A, M₀, c).** The master's C ([MISR-R] `:106-107`; G2 `:22-24`, `:50`) is the MIS-R (i) constant on
   𝒦^λ_n(s, A, 2M₀ + 1, (c_R/8)^{1/2}, C_OS, c′). That is the [POST2] Claim C case-(ii) constant at σ*² = 1 for these
   arguments ([MISR] `:63-64`, `:110-113`). C_OS depends only on (s, A) at g₀ = 1 / c_D = ½ ([MISR] `:51-52`; G2 `:23`).
   c′ = c₀(s, A) + 1 on the L = ∞ branch (G2 [R-3] `:24`), and c₀ depends on (s, A) only ([MISR] `:63`). With c_R = c, C is a
   function of (s₀, A, M₀, c). **Correct.**
5. **P0.** Item 1: {S ∌ j} ⊆ {S ≠ S₀} for j ∈ S₀, and {S ∋ j} ⊆ {S ≠ S₀} for j ∉ S₀. π(S ≠ S₀) = δ also when
   S₀ ∉ Ω, because π(S₀) := 0. Item 2: T is a maximiser, so π(T) ≥ π(S₀). This holds for any tie rule. Item 3:
   MPM ≠ S₀ gives j ∈ S₀∖MPM (PIP_j ≤ ½) or j ∈ MPM∖S₀ (PIP_j > ½). The strict threshold matches [W3P] `:33`.
   "y^r non-constant a.s.": given X^r, y^r has a non-degenerate Gaussian law on ℝⁿ, and span(1) is a null set for n ≥ 2.
   The citation of [MISR] `:118-119` is exact. **Correct.**
6. **Markov and b_n.** P(δ_n ≥ ½) ≤ 2E δ_n. The master's HPM bound is 2C r_n + X ≤ 2(C r_n + X) = 2b_n, since X ≥ 0.
   k_n ≤ 3(A + 1)(s₀ + 1) log n gives (2 + 2k_n)n^{−2} = O(log n/n²) = o(r_n), and n^{−1} = o(r_n). **Correct.**
7. **Corollary.** The quadratic form reduces to the S₀ block because β vanishes off S₀. For the positive semidefinite
   block, λ_max ≤ tr = s₀, and ‖β_{S₀}‖² ≤ s₀b_hi², so the bound is s₀²b_hi². M₀ is then fixed. Beta-min: Σ_jj = 1, so
   ρ_n ≥ nb_lo²/(σ*² log n) → ∞. (A2): R = Σ_n, the 3(·) range lies inside the 5(·) range, and c = φ² > 0.
   The recorded conclusions ([RV] `:271-275`) follow: Markov for the two O_P statements, and a union bound for
   P(HPM = MPM = S₀) → 1. **Correct.**
8. **Faithfulness / hypotheses used but not stated.** Every hypothesis used is in STATEMENT §§0–1: n ≥ 3 (`:14`),
   Σ_jj > 0, σ² > 0, ε independent of X^r, p ≤ n^A and fixed s₀ ≥ 1, (A2), (A3). Two are used only implicitly in §0:
   that p and σ² are deterministic (the "everything may depend on n" list at `:21` reads them as deterministic
   sequences). PROOF states these as "this is §0". That reading is fair; see K1-3. PROOF does not re-copy §§1–3; it
   cites them. Its restatements of (E) (P1 `:44-48`, P2) agree with STATEMENT `:44-48` term by term (k_n, j₀, m♯_n, b_n, and the
   factor 2 on the HPM and MPM bounds). The "same holds with the floor asked only on 3(·)" clause of §2 is handled at P3
   `:62-63`. No hypothesis is used that is not stated.

## Findings

- **K1-1 [S] PROOF `:35-39`, `:48` — the floor is available only for n ≥ max(3, 2s₀); the text should say why that
  suffices.** For 3 ≤ n < 2s₀ we have s₀ > K, so m♯_n and k_n are not defined. This applies to the master's k_n too
  ([W3P] `:37`, "defined for s₀ ≤ K"). The master's floor hypothesis is therefore meaningful only from n ≥ 2s₀ on.
  PROOF handles this with the parenthesis "(Take n* ≥ max(3, 2s₀) as well…)". It does not say why the master may be
  applied to hypotheses that hold only eventually. The reason is correct: the master's conclusion at each n is about the
  n-th law alone, and its proof checks the class membership n by n (G2 steps 1–5, `:27-45`). But it is not written down.
  *Fix:* at `:48` add one sentence: "CorGb-plus's hypotheses, like its k_n, are required only for all large n (k_n is undefined for
  s > K); its bounds at n concern the n-th law only, so they hold here for n ≥ max(n*_master, 3, 2s₀)."
- **K1-2 [F] PROOF `:36-37` — B4.1's domain is incomplete.** The parenthesis lists "s ≤ K, n ≥ 3, A ≥ 1, s ≥ 1". B4.1's
  m♯_n branch is B1.3, whose proof uses p ≤ n^A ([R1] `:25`, "binom(p, s) ≤ p^s ≤ n^{As}"). That hypothesis is
  supplied by (A1), so nothing breaks. *Fix:* add "p ≤ n^A ((A1))" to the list.
- **K1-3 [F] PROOF `:59` (and P1 `:23`, P4 `:74`) — attributions of determinism.** (a) P3 calls α* and β* "deterministic: the model of
  `NOTATION.md:15-20`". Those lines state the model with parameters α*, β*, σ*² but do not use the word "deterministic".
  The reading is natural, and for β* it is forced by `NOTATION.md:41-43`. For α* it is not needed at all: the master
  allows a random α ([MISR-R] `:52-53`). (b) P1 `:23` says "σ² deterministic — this is §0". §0 `:19` calls only α and β
  deterministic; for σ² the determinism is implicit in `:21`. (c) P4 `:74` says "no condition on m or α". §0 does require α to be
  deterministic, a requirement stronger than the master's. *Fix:* in P3 write "(parameters of the model of
  `NOTATION.md:15-20`; α* may even be random, [MISR-R] `:52-53`)". In P1 write "σ² a deterministic (n-dependent)
  parameter, §0 `:19`, `:21`". In P4 write "no condition on m; α only deterministic (and even that is not used)". This is
  wording only; no step changes.
- **K1-4 [E] PROOF `:29` — line range.** The quoted sentence is at [MISR] `:21-22`; line 20 is the preceding text. Cite
  `:21-22`, or keep `:20-22` as the containing passage. Cosmetic.

No C findings. I checked the points most likely to break, and none did: the degenerate (OV) with τ² = 0 and q = 0;
the "any tie rule" HPM; the convention π(S₀) := 0 off Ω; the factor 2 in the master's HPM bound versus 2b_n; λ_max ≤ trace;
and the dependence of C (C_OS and c′ are both functions of (s, A)).

K1-VERDICT: VERIFIED-WITH-AMENDMENTS (P0 VERIFIED, P1 VERIFIED-WITH-AMENDMENTS, P2 VERIFIED, P3 VERIFIED-WITH-AMENDMENTS; 0 C, 1 S, 2 F, 1 E)

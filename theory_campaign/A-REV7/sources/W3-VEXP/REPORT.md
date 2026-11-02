# W3-VEXP: referee report on W1-EXP

**Run:** 2026-11-02, branch `theory/W3-VEXP`. **Object:** `origin/theory/W1-EXP`, files `theory_campaign/W1-EXP/` (REPORT, PROOF,
scripts, results).
**Supporting files:** `REPAIRS.md` (repairs and new statements, with proofs), `NOTES.md` (log), `scripts/` (my own code,
written from the spec, not from W1's scripts), `results/`.
**Status words:** the protocol's. Every proof here is a candidate: it has not been reviewed or adopted.

## 1. Headline

1. **No mathematical ERROR in any W1 theorem.** I checked Thm 1 (EXP′), Prop 2.1/2.2, Lemma 2.3, Thm 2, Thm 6,
   Thm 3, Thm 4, Lemmas 4.1–4.2 and Thm 5 line by line against the spec, the locked T22(i)/(ii-a)/(iii) and T27(i)
   statements and proofs, and T03. All are VERIFIED. Thm 2 is a verbatim corollary of the locked T22(iii) (NL_η with
   η = 0), so its PROOF SKETCH label is conservative. Four wording errors need fixing (REPAIRS R4); none is load-bearing.
2. **I reproduced every key number independently.** I used my own scorer and my own port of the engine's partition,
   with explicit n×p designs and noise vectors (W1 simulated sufficient statistics). Config A/B rates, the T27 limit law,
   the leakage-chain table, √n(1−π₀(S°)) ≈ 1.6, π(S₀) → 1, the T22(i) bound (300/300) and blocks = groups (300/300)
   all agree with W1 to about two decimals.
3. **Two GAPs and one boundary.**
   - (a) The iid-design version of the LH theorem had an open conditioning step. **Repaired** (REPAIRS R3, PROOF SKETCH):
     on the event "blocks = groups" the partition is fixed, and the masked/null residuals have an exact Beta law.
   - (b) "S1/S3/S4/S6 sit in the favourable regime asymptotically" is VERIFIED at **population** level only. In-sample
     it is **not proved** (GAP, not fixed here): with ≥ 2 groups per block the packing depends on the noise column.
   - (c) Lemma 4.2's hypothesis |ψ| < ρ is **sharp in effect**. At ψ = 0.71 > ρ = 0.7 the hubs pair up, and π₀(S°),
     π₀(R₂) → 0 exponentially, with the mass moving to R_{g−1}.
4. **Finite-n EXP′.** W1's κ_EXP is ≈ 100–1,700 nats at the study's signal scale, so it is vacuous there. I give a
   data-computable certificate, **PROVED** (REPAIRS R1): at most 1.52 nats on study-like designs. The actual max |R| is
   at most 0.145.
5. **W1's escalation item 3 (weak-signal masking) has the wrong mechanism.** My exact computations at n = 200 show that
   the start is masked by **dilution**: tables score against the full y, so each truth sees noise v ≈ 25σ². The start
   misses 6–12 of the 14 truths, strong ones included, at **every** signal scale (c = 4 included). It becomes favourable
   only by n ≈ 800–1600. I prove a deterministic ceiling, **PROVED** (Prop D): π₀(S₀) ≤ prior factor × ∏ BF({j}).
   It holds in all 26 paired designs. This reconciles HQ's π₀(S₀) ≈ 1e-12 and π₀(R₂) ≈ 0.8. The R₂ mass sits on
   *small subsets of S₀*, which are 6–11 additions from the truth.

## 2. Verdict table

**Legend.** V = VERIFIED, G = GAP, E = ERROR. "repro" means I reproduced it with my own code.

| # | Claim (W1 label) | Verdict | Evidence / reason |
|---|---|---|---|
| 1 | Lemma 1.1, Q_S = RSS^y_S + c_S, 0 ≤ c_S ≤ 1 + 1/(nφ²) | V | Algebra rechecked; Q decomposition and τ ≤ ε/φ² correct. |
| 2 | Lemma 1.2, determinant ratio = log(n+1) + η_D | V | Schur formulas for H and G+I; α ranges; ρ ≥ λ_min(G_{T+l}). |
| 3 | Lemma 1.3, exact decomposition and bound | V | Identity rechecked. The bound holds on 300 adversarial small designs, max ratio 0.77 (`results/sanity.txt`). |
| 4 | Lemma 1.4, RSS floor c_* n | V | (C−P_W) = (C−P_W)(C−P_U); E e^{χ²_k/4} = 2^{k/2}; union bound over ≤ 2^16 p pairs. |
| 5 | **Thm 1, EXP′ from G, p ≤ n^A, ‖μ‖² ≤ Mn, SE-blk; \|R\| ≤ κ_EXP** (PROVED) | V | Composition of 1–4. Its form equals the locked T22(iii) EXP′. On LH, max\|R\| → 0.67 ≠ 0 (repro), confirming W1 Remark (c) that the remainder is O(1), not o(1). κ_EXP is loose: 27 on LH, 100–1,700 at study SNR. Finite-n repair in R1. |
| 6 | §1.5, random designs give SE-blk w.p. → 1 for every ≤ 16-partition (PROOF SKETCH) | V (sketch) / E (minor) | The argument is standard. Minor error: "κ_17 ≥ 0.15 for all six" is false for S6 (0.1). Harmless (R4). |
| 7 | Prop 2.1, NL_η → NL_C in Lemma quad (PROOF SKETCH) | V | NL_η is used only for the O(log n) bound on (δ+σZ)²; every later line is unchanged. |
| 8 | Prop 2.2, reference transfer S₀ → S° (PROOF SKETCH) | V | I read the locked proof line by line: supp θ* = S₀ is never used. S₀ enters only via U_b*, 𝓛_n, VIS, e_n and s₀. |
| 9 | Lemma 2.3, \|δ\| ≤ √λ_b(S°); VIS from block gain (PROVED) | V | Nested projections. |
| 10 | **Thm 2, unconditional favourable regime in BO** (PROOF SKETCH) | V | BO gives δ ≡ 0 on 𝓛_n, i.e. the locked NL_η with η = 0, hence NL_avg(½). BM-blk gives VIS; Thm 1 gives EXP′. The locked T22(iii) applies verbatim (R2). |
| 11 | **Thm 6, 1 − π₀(S°) = O_P(2^B n^{−1/2}) under ZL, SPREAD, VIS-lin** (PROVED) | V | Steps 0–3 rechecked: a < ½ makes E e^{aZ²} finite; telescoping lower bound; T22(i-a,b). Repro: flat √n(1−π₀(S°)) ≈ 1.6 for n = 100…102400, with no √(log n). |
| 12 | **Thm 3, CL(L) ⇒ two-sided ratio law** (PROVED) | V | Upper bound via −log(1−x) ≤ x/(1−x) = (δ+σZ)²/RSS_{T+l}; 1.01 valid for n ≥ 103. Note: needs a deterministic chain (R4). |
| 13 | **Thm 4, T27(i) from CL(L) + H3** (PROVED given H3) | V / E (wording) | Telescoping via T22(ii-a); the prior-ratio bounds are correct. "iff … sufficient" is self-contradictory (R4). Repro of the leakage table at L ∈ {0, 2, 4, √(2 log n)}, n ∈ {1600, 102400}: agrees with the predicted (L+Z)²/(2v) law (`results/lh_more_L.txt`). |
| 14 | Limit law of Mstat (PROOF SKETCH) | V (sketch) | The remainder → 0 at T = ∅ is checked (a_l − a_∅ = O_P(1/n)). Repro, Gram: medians 0.50/0.52/0.53/0.54 at n = 1.6e3/6.4e3/2.6e4/1.0e5 vs predicted 0.544; q95 0.80–0.89 vs 0.84. Wording: p → ∞ constant (R4). |
| 15 | **Prop 2.1 (escalation): EXP′ removable from T22(iii)** | V | Thm 1's hypotheses are a subset of the locked T22(iii) hypotheses (same SE-blk definition). |
| 16 | Lemma 4.1, LH population algebra (PROVED) | V | (a) λ_min ≥ (1−\|ψ\|)(1−ρ) (Config A: 0.242 ≥ 0.15). (b)/(c) Cov identities rechecked. |
| 17 | Lemma 4.2, partition = groups if \|ψ\| < ρ and g ≤ B < 2g (PROVED) | V; boundary found | The complete-linkage invariant argument holds, with strict margin. Repro: 300/300 and 200/200. **Beyond the hypothesis** (ψ = 0.71, 0.8): the hub pair forms its own block, and π₀(S°) and π₀(S₀) become e^{−Θ(n)} (log₁₀π₀(S₀) = −1285 at n = 102400). Mass moves to S₀ ∪ (rest of hub group) ∈ R₃ (`results/lh_more_P.txt`, `lh_boundary_Rd.txt`). Packing with 2g ≤ B kills the masking (π₀(S₀) → 1, `lh_more_G.txt`), as W1 says. |
| 18 | **Thm 5(a), b_n → 1 at S° = S₀∖M** (PROVED) | V | Hypotheses of Thm 6 checked: ZL from 4.1(b)(c) is exact in-sample; SPREAD residual ≥ β²ψ²(1−ψ²) > 0; VIS-lin with c_V = (1−ρ₊)min β²(1−ψ²)². Repro: Config A/B. |
| 19 | **Thm 5(b), masking π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}** (PROVED) | V | CL(0) since δ_{∅,j_b} = 0; H3 from (a). Repro: slope −0.301 per factor 4 in n (A); −0.98 per decade (B, c = 2). |
| 20 | Thm 5(c)(e), VIS fails at S₀; bridge endpoints | V | Gain is zero on the masked block; T22(iv-b) is quoted correctly. |
| 21 | Thm 5(d), π(S₀) → 1 via locked T03 | V | SE for \|T\| ≤ m_n + s₀ from λ_min(Σ); BM-∞ with fixed betas. H-T02 is closed in the register (T02(i) locked). Repro: median π(S₀) 0.72 → 0.99. |
| 22 | §4.3, LH iid realisation (PROOF SKETCH, conditioning step open) | G → repaired | Repaired in R3: on P_n = {blocks = 𝒢} the partition is fixed, and the residual is exactly Beta(½, (n−\|T\|−2)/2) and independent of (X_T, Y). Repro: √n(1−π₀(S°)) ∈ [2.5, 3.1] (√(log n) behaviour), Mstat median 0.73 vs predicted 0.73. |
| 23 | **Headline 6: S1/S3/S4/S6 block-orthogonal at population level** | V | On the **actual** sample partition (my port), population leakage λ_b(S₀) is exactly 0 in S1, S3, S4 and S6 (all blocks, 3 designs × 2 p). It is positive in most blocks of S5 (54/56–56/57 at p = 500; 110/112–115/117 at p = 1000) and S2 (46/48–48/50; 81/101–83/105). In S3–S6, blocks are unions of whole groups of 5 in every design (`results/study_check.txt`). |
| 24 | Headline 6: "favourable regime asymptotically" (in-sample) | G (not fixable here) | Not proved for iid designs with ≥ 2 groups per block: the packing depends on x_l (R3, last paragraph). **Empirically true** (S3, p = 500): median π₀(S₀) ≈ 1e-10, 4e-4, 0.1, 0.45 at n = 200, 400, 800, 1600 (2 designs each, c = 1 and c = 4 alike). CONJECTURE, high confidence. |
| 25 | Headline 6: SE-blk at n = 200 (min_b λ_min = .46/.25/.17/.086/.17/.064) | V (repro) | Mine: .44–.49 / .23–.25 / .15–.18 / .07–.09 / .15–.17 / .057–.069. |
| 26 | "… so EXP′ (Thm 1) applies at the study size" | G (fixed) | Thm 1 is asymptotic and κ_EXP ≈ 100+ nats there. Replaced by R1 certificate (0.59–1.52 nats); actual max\|R\| ≤ 0.145. |
| 27 | Escalation 3: n = 200 masking = weak-signal masking, c = #weak truths, π(S₀) also small (CONJECTURE) | Evidence against | Prop D and the computations in REPAIRS §D: dilution, half to most of S₀ masked, strong truths included, independent of the signal scale. The π(S₀) part is untested by me. |

## 3. Statements (refined or new; full text and proofs in `REPAIRS.md`)

- **R1. EXP′ certificate (PROVED).** Assume SE-blk(φ) on the realised blocks. Then every within-block addition satisfies
  |R| ≤ (1+φ^{-2})/(2φ²(n−1)) + ν(1.02 + 1/(nφ²))/min_b RSS^y_{C_b}. This holds for any data and any n. It is the
  form to use at finite n.
- **R2. Thm 2 (W1).** G, R, SE-blk, BO and BM-blk imply 1 − π₀(S₀) = O_P(2^B √(log n) n^{−1/2}). This is a verbatim
  corollary of the locked T22(iii) plus Thm 1. No missing step.
- **R3. LH-iid (a).** Rows iid N(0, Σ_LH), |ψ_i| < min ρ, g ≤ B < 2g, p ≤ n^A, fixed betas. Then
  1 − π₀(S₀∖M) = O_P(2^B √(log n) n^{−1/2}), and (b) holds as in W1. PROOF SKETCH; the only unwritten step is a routine
  uniform LLN for VIS-lin.
- **Prop D (PROVED).** Let U ⊆ S₀ consist of truths each alone (among S₀) in its block. Then
  π₀(S₀) ≤ ∏_{i=1}^{|U|}(s₀−|U|+i)/(2p−s₀+|U|−i) · ∏_{j∈U} BF({j}). BF({j}) is a closed form in r_{jy}. Regime: any data.
- **Dilution threshold (PROOF SKETCH for the population limit; numerically confirmed).** For independent unit-variance
  truths, truth j enters the start mode only if (n/2) log(1/(1 − θ_j²/v)) ≳ log((2p−s₀)/s₀) + ½ log n, with
  v = σ² + Σθ_k². The start is favourable only when n ≳ 2v log(2p/s₀)/θ_min². This threshold does not improve as the
  signal scale grows.

## 4. Evidence (all scripts seeded; outputs in `results/`)

- `sanity.py`: batch and single scores agree; brute-force Z̄₀ equals the convolution Z̄₀ to 1e-12; partition-port merge
  heights equal scipy's complete linkage; Lemma 1.3 bound ratio ≤ 0.77 on 300 adversarial designs.
- `lh_repro.py gram|iid`: Config A, 300 Gram / 200 iid replicates, n = 100 … 102400. Table in `results/lh_gram.txt`,
  `lh_iid.txt`.

  | n | Mstat q05/med/q95 (Gram) | √n·med(1−π₀(S°)) | med π₀(R₀) | med π(S₀) | max\|R\| | T22(i) bound |
  |---|---|---|---|---|---|---|
  | 100 | 0.25/0.35/0.66 | 1.72 | 0.843 | 0.719 | 1.03 | 300/300 |
  | 1600 | 0.46/0.50/0.89 | 1.62 | 0.962 | 0.920 | 0.77 | 300/300 |
  | 102400 | 0.50/0.54/0.80 | 1.62 | 0.995 | 0.988 | 0.68 | 300/300 |
  | predicted | 0.50/0.54/0.84 | — | → 1 | → 1 | — | — |

- `lh_more.py B`: Config B (c = 2). Median log₁₀π₀(S₀) is −4.64, −5.78, −6.99 at n = 400, 6400, 102400. Mstat median
  1.30, 1.44, 1.43 vs predicted 1.42; π(S₀) 0.69–0.99.
- `lh_more.py L`: leakage chain. For example, n = 102400 with L = √(2 log n): observed 1.44/2.51/4.14 vs predicted 1.37/2.52/4.15.
- `lh_more.py P`, `lh_boundary_Rd.py`: the ψ/ρ boundary (row 17). `lh_more.py G`: packing failure.
- `study_check.py`: SE-blk, whole-group blocks and population leakage on the actual partition (rows 23 and 25).
- `study_exp.py`, `dilution_ceiling.py`: exact EXP′ remainders, the R1 certificate, exact π₀(S₀), π₀(R_d) via bivariate
  capped convolution, 1000 exact π₀ draws per design, and the n/c sweep (REPAIRS §D).

## 5. Fidelity of the modelled method (task item 3)

| Ingredient | Spec / engine | W1's model | Verdict |
|---|---|---|---|
| Score m(S), ν = 0.01 + n/2, 2b₀ = 0.02 | M §5; `v3_score.h` | same | faithful |
| Tables r_b(U) = m(U)/m(∅) on full y | M §6.3; `v3_start.h build_tables` | same | faithful |
| γ₀ = ϖ(\|S\|)∏r_b, cap K = min(p, ⌊n/2⌋), w(k) = ½/C(2p−1,k) | M §6.3; `v3_score.h data_init` | same (cap included) | faithful |
| Partition: complete linkage on 1−\|r\|, R13 ties, top-down cut left-first, next-fit packing | `v3_blocks.h` | port of the engine; my independent port agrees | faithful |
| B = min(⌊√n⌋, ⌊√p⌋, 16) | M §3 | same | faithful |
| Exact branch | M §6.2 | acknowledged for p ≤ 17; **omitted for p = 20 at n ≥ 10,435** (Config B large-n rows are component-law values) | minor omission (R4) |
| Moves, order, ESS/resampling, grid, local search, streams | M §§6.5–6.10 | **not used**: every W1 claim concerns π₀ or π, which are deterministic functionals of the data | n/a, no mismatch |
| T38(b) use of b_n | final run: Q_f iid π₀ draws (00_COMMON) | "b_n → 1" is a π₀ statement | consistent |

## 6. What fails and why (routes I tried)

- **Extending R3 to S3/S4/S6 at B ≥ 2g.** A fixed-partition surrogate does not exist. A union over candidate blocks
  costs (p/g)^{⌊B/g⌋−1}. Hölder decoupling with P(β is a block) also loses a polynomial factor. Left as a GAP.
- **Using NL_avg on X directly** (fixed-design route conditional on X). In random designs E_{T,l} has
  e^{|N|√Δσh/v} tails, giving κ = ½ − (A+ε)Δσ²/v². In the worst case (Δ = σ²) this is positive only if A < 2, and the max over T in the
  X-dependent block still needs decoupling. Abandoned.
- **Searching for a counterexample to Thm 1, 3 or 6.** No violation in adversarial small-n, high-SNR, near-collinear
  designs (Lemma 1.3 ratio ≤ 0.77), or in any LH run (T22(i) bound and Thm 6 rate always held).

## 7. Needs escalation

1. **Locked-register edits proposed by W1** (EXP′ removed from T22(iii); NL_η → NL_C). I verified both. They need
   Felipe's decision and a second-family review, because they edit locked statements.
2. **R3 and Thm 6** should go to a stronger prover for a full write-up of the uniform-LLN steps (VIS-lin in sample;
   P(P_n) → 1). These steps are routine, but they are not written out.
3. **The in-sample favourable regime for S1/S3/S4/S6** (row 24) needs a partition-stability lemma (leave-one-column-out).
   This is real research. Its failure would not hurt the paper, since the study is pre-asymptotic anyway (§D).
4. **For HQ / T38(b): the n = 200 start is dilution-masked.** π₀(R₂) ≈ 0.8 is carried by subsets of S₀ that are 6–11
   additions from the truth. Delivery "into R_d" therefore does not put a centre within a fixed Hamming distance of S₀
   at the study size. Any T37/T38 repair statement must count missing truths, not only extras. ℓ = 10 < 11, so the local
   search alone cannot cover it, which is consistent with HQ's finding that Gibbs moves, not the local search,
   deliver the HPM.
5. Independent check of Prop D's population threshold (n* ≈ 600–800 for S3, p = 500) against the real ANALYSIS-H2 fits,
   which I do not have.

## 8. Outside scope (recorded, not pursued)

- **S5 (common factor):** the start is the most masked of all six (log₁₀π₀(S₀) −16 to −25), yet π₀(R₂) ≈ 0.97–0.996.
  The mass is on 1–5-truth subsets plus few extras. Leakage is linear in n, so neither W1 theorem applies; dilution and
  leakage compound.
- **R_d's definition** makes ∅ "near-truth" (∅ ∈ R₀). Restating the T38 delivery region with a cap on |S₀ ∖ S| is advisable.
- The posterior π at p = 500 was not computed. Whether c = 1 misses are posterior misses (HQ) is untouched here.

## 9. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| EXP′ (Thm 1) | as W1, plus the R1 certificate at finite n | 0.98 | done (VERIFIED; R1 PROVED) | none left | No |
| T22(iii) in BO (Thm 2) | as W1 | 0.97 | done (verbatim corollary) | — | No |
| Thm 6 (zero leakage, reference S°) | as W1 | 0.95 | done | review of the uniform RSS event (ii) | No |
| T27(i) from CL(L) (Thms 3–4) | as W1, deterministic chain | 0.97 | done | — | No |
| LH joint family, exact Gram (Thm 5) | as W1, with \|ψ\| < ρ **and** hubs in different blocks stated as the operative condition | 0.95 | done | the ψ ≥ ρ cliff must be disclosed | No |
| LH joint family, iid (R3) | 1 − π₀(S₀∖M) = O_P(2^B √(log n) n^{−1/2}) plus masking | 0.9 | 0.8 | uniform LLN for VIS-lin; P(blocks = groups) | No |
| S1/S3/S4/S6 favourable in-sample, n → ∞ | 1 − π₀(S₀) → 0 for iid designs, X-dependent packing | 0.85 (numerics agree) | 0.4 | partition–noise decoupling | No (yes if sample-split partitions were adopted) |
| Study-size start masking = dilution (Prop D plus threshold) | as in §3 | 0.9 | Prop D done; population threshold 0.8 | r_{jy}² → θ_j²/v uniformly | No |
| W1's weak-signal-masking conjecture | as W1 stated it | 0.15 | — | contradicted by exact computation | — |

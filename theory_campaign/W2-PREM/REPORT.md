# W2-PREM — REPORT: discharging the premises of Theorem B (restated T24)

Run of 2026-11-02, branch `theory/W2-PREM` (from `theory/campaign` @ 2f6d0ab). Nothing here is reviewed; every
PROVED is a **candidate** pending cross-family review. Proofs: `PROOF.md` (§ numbers below refer to it). Scripts:
`scripts/` (fixed seeds). Outputs: `results/`. Notation: 00_COMMON and W1-T24G `PROOF.md` ([B]); W1-EXP is [E].

## 1. Headline

1. **IND is two different premises, and the one the task names is PROVED.** The task's IND (conditional
   independence of terminal trajectories) is not what [B] called "genuinely open in the masked regime"; that was
   IND(𝓕), the *independence-proposal bad acceptance*. Conditional independence (**IND-T**) is **PROVED** under EX-S and
   EX-A from the engine's actual stream discipline: one sequential stream per island, read at state-dependent rates.
   The proof is a stopping-time argument (§1). It holds in every regime, and the resampling-free segment has
   **L + 5** rounds, not L + 4.
2. **One shared lemma (Lemma U, PROVED)** gives the uniform log-BF expansion over any polynomial family of bounded-size
   additions. EXP′ is its within-block instance, so EXP′ and Theorem B's premises now rest on the same lemma (§2).
3. **Phase 2 (supersets).** Truth removal by every non-independence label: **PROVED**. UDEL(1): **PROVED**. NL0(a) and
   UDEL(a ≥ 2): **PROVED UNDER** a partner-graph condition PG, and there is a **COUNTEREXAMPLE** without it
   (equicorrelated nulls, exact Gram, p = n^0.9; §3). NL0 at a = 1 for correlated nulls is therefore a genuine
   design condition.
4. **Phase 1 (incomplete starts).**
   - **BTP is unnecessary.** New Prop. B1′ (PROVED) gives progress constant ≥ 1/|M(x)| from *pointwise*
     addability, and pointwise addability is PROVED under G, R, SE, BM-∞ alone (§4).
   - **TS:** COUNTEREXAMPLE (a cancellation pair); PROVED UNDER a coefficient condition.
   - **[B]'s repair family has a defect:** COUNTEREXAMPLE on LH. Useless look-alikes from the neighbour graph make η₁
     of order one. The fix is **Theorem B♯** (PROVED), with a monotone look-alike map (§5).
   - Swap truth removal, junk additions and look-alike retention: PROVED UNDER explicit conditions (FS, TL♯, ULR; §6).
5. **IND-M (independence-move bad acceptance): PROVED UNDER start concentration on a reference S° ⊆ S₀ plus a
   subset-gain condition, for starts x ⊇ S° (§7).** On the linked-hub family LH, every premise is discharged
   (**Theorem L, PROOF SKETCH**). Every component is proved except two finite population inequalities, which were
   verified numerically for configuration B. The open case is a start that concentrates on a *superset* of S₀.
6. **Usefulness is still asymptotic.** On LH at p = 20, the junk/null-addition and independence terms decay like
   n^{−1/2} as predicted. The swap-substitute term is D′/(k(p−k)) = 1/16 and needs p → ∞, and the single-particle
   binomial factor stays near 1 for n ≤ 10⁶. The multi-particle product (now rigorous through IND-T) is the
   operative route.

## 2. Premise-by-premise table

"Under" lists hypotheses beyond G, R-lite(A,M), SE(k) for a fixed k, BM-∞, s₀ and a fixed, EX-S, EX-A, SR.

| premise ([B]/task code) | verdict | extra condition / obstruction | § |
|---|---|---|---|
| IND (task: conditional independence of terminal trajectories) = **IND-T** | **PROVED** | EX-S, EX-A only; any regime; H′ = L+5 | 1 |
| uniform log-BF expansions "of EXP type over finite families" | **PROVED** (Lemma U) | SE on the sets of the family; EXP′ = block instance | 2 |
| τ₂ truth removal at supersets (Gibbs, uniform swap, B neighbour swaps) | **PROVED** | — (super-polynomial) | 3.1 |
| NL0(0) (leakage at W = S₀) | **PROVED** | — | 3.3 (a = 0) |
| NL0(a), a ≥ 1 (incl. a = 1, correlated nulls) | **PROVED UNDER** PG(a); **COUNTEREXAMPLE** without | PG: partial-correlation partner graph given S₀ at threshold c_n (c_n log n → 0) with degree D_n, (eD_n+1)^a log^{3/2}n/√n → 0. Fails for equicorrelated / common-factor nulls once p^r ≫ √n | 3.2–3.4 |
| UDEL(1) | **PROVED** | — (O_P(log n/√n)) | 3.3 |
| UDEL(a ≥ 2) | **PROVED UNDER** PG(a−1); **COUNTEREXAMPLE** without | same as NL0 | 3.3–3.4 |
| BTP (ε_add → 0) | **not needed** | replaced by Prop. B1′ + PA (both **PROVED**; PA needs nothing extra) | 4 |
| TS (Gibbs truth removal at incomplete states) | **PROVED UNDER** TS(𝒲) (≡ coefficient non-cancellation); **COUNTEREXAMPLE** without | cancellation pair θ₂ = −θ₁/r | 6.1 |
| swap truth removal at incomplete states | **PROVED UNDER** FS(D′, c₀) + p_n/log n → ∞ | few substitutes, none a neighbour | 6.2 |
| TL(𝒵, A) with [B]'s A = neighbour graph | **COUNTEREXAMPLE** (family defect, LH) | useless look-alikes swapped for junk exit with O(1) probability | 5.1 |
| TL♯ (junk additions at budget, repaired family) | **PROVED UNDER** ZJL + CS(g₀) | zero junk leakage + bounded components; bounded-leakage relaxation PROOF SKETCH; random designs OPEN | 6.3 |
| ULR (new: keep useful look-alikes) | **PROVED UNDER** ULR(c₀) | — | 6.4 |
| IND(𝓕) of [B] = **IND-M** | **PROVED UNDER** SCR(S°) + GS(S°), starts x ⊇ S° | superset starts S° ⊋ S₀: **OPEN** | 7 |
| all of the above on LH (exact Gram, p/log n → ∞) | **PROOF SKETCH** (Theorem L) | FS-neighbour gap and ULR verified numerically for configuration B; SCR cites [E] Thm 5(a) | 8 |

## 3. Statements (full; hypotheses named)

Common: G; R-lite(A,M): p ≤ n^A, ‖μ‖² ≤ Mn; SE(k; φ₀): λ_min(R_V) ≥ φ₀² for 1 ≤ |V| ≤ k; BM-∞; C_R = 2M + 4σ²;
L = ⌈log₂(n+1)⌉.

- **Theorem IND-T** (§1). Under EX-S, EX-A, conditionally on everything up to the stage-T resampling of a final island
  (data, 𝓒, bridge history), the extended round outputs of the N particles over the L+5 rounds at φ = 1 are
  independent across particles, each a Markov chain with the round kernel K̄₁. The same holds across islands.
- **Lemma U(𝔉)** (§2). For a family 𝔉 of pairs (T,l) with |T+l| ≤ k, at most n^{A′} sets, and SE on those sets:
  w.p. → 1, simultaneously, log BF(T+l)/BF(T) = −½log(n+1) − ν log(1 − x_{T,l}) + R, |R| ≤ κ_n
  (κ_n → 4.16(M+2σ²)/σ²); plus the events (E1)–(E4) and corollaries (C1)–(C6).
- **Prop. T2** (§3.1). Under SE(s₀+a+2), BM-∞: truth removal at 𝒮_a by Gibbs, uniform swap or neighbour swap has
  probability n^{−ω(1)} uniformly.
- **Prop. NL0 / UDEL** (§3.3). Under SE(s₀+a+2) and PG(a): Λ₂(a) = O_P((s₀+a+1)(eD_n+1)^a√(log n/n)).
  ε_del(1) = O_P(log n/√n) always; ε_del(a) = O_P((s₀+a)(eD_n+1)^{a−1}log n/√n) under PG(a−1).
- **Counterexample EQ** (§3.4). Exact Gram, nulls equicorrelated (r), p = n^β, rβ > ½ (e.g. r = 0.8, β = 0.9; G, R,
  SE, BM-∞ all hold): Λ₂(1) ≥ 1 − o_P(1) and ε_del(2) → 1.
- **Prop. B1′** (§4). For any closed phase-1 family, P_W(no bad, no progress) ≤ 1 − (1 − ε_pt)/|M(W)|, with
  ε_pt := sup_W min_{j∈M(W)}(1 − o_j(W)). **Prop. PA:** under SE(k), BM-∞, ε_pt = n^{−ω(1)} over all bounded-size
  states.
- **Theorem B♯** (§5.2). Theorem B holds with the family 𝒵♯(x) built from any monotone look-alike map 𝔄 (current
  junk may grow by the look-alikes that stopped being look-alikes), and with c₁♯ = max{1−ε_add♯, (1−ε_pt♯)/|M(x)|}.
  The constant map gives back [B].
- **Props. TS, SW, TL, ULR** (§6). Each turns its condition into an o_P(1/log n) bad rate: TS(𝒲) super-polynomial;
  FS gives O(D′/p) + e^{−Ω(n)}; ZJL + CS give O_P(2^{g₀}√(log n/n)); ULR gives e^{−Ω(n)}.
- **Prop. IM / IND-M** (§7). β_I(W) ≤ (1 − π₀(S°)) + 1{S° bad at W}·π(S°)/(π(W)π₀(S°)) always. Under SCR(S°)
  (1 − π₀(S°) = o_P(1/log n), S° ⊆ S₀) and GS(S°) (every nonempty subset T of the masked set has signal gain
  ≥ M′_nσ² log n at S°), uniformly over the family of any start x ⊇ S°: β_I = o_P(1/log n).
- **Corollary A** (§9). Under the premises of the table, sup_{x∈𝓧} P_x(S₀ not scored within L+5 rounds) → 0, with
  c_* ≥ min{1/|M(x)|, 1/(B+3)} − o_P(1).
- **Theorem L** (§8, PROOF SKETCH). On LH (exact Gram, [E] Thm 5 setting, p/log n → ∞) all premises hold for starts
  S° ⊆ x ⊆ S₀ ∪ 𝔄_LH(M), with 𝔄_LH = group-mates of the missing masked hubs.

## 4. Evidence

All scripts use the exact v3 score from sufficient statistics (`scripts/bvs_score.py`; exact Gram as in [E]).

**IND-T** (`ind_streams.py`). A toy chain with state-dependent uniform consumption, two particles, one shared
sequential stream vs separate streams, 4·10⁵ reps: χ² independence 13.2 / 9 df (critical 16.9); TV between the two
joint laws 0.0035 (MC scale 0.006).

**Lemma U** (`lemma_u_check.py`; p = 24, AR(0.5), all 49,152 pairs with |T+l| ≤ 4): max|R| = 0.63 / 0.80 / 0.71 /
0.76 / 0.76 at n = 200 / 10³ / 5·10³ / 2.5·10⁴ / 1.25·10⁵; bound κ_n ≈ 20.

**NL0 / UDEL: partner graph vs equicorrelated nulls** (`nl0_equicorr.py`; s₀ = 2, r = 0.8, p = n^0.9; medians).
EQ = every null pair partnered (PG fails); BLK = groups of 5 (D = 4).

NL0_TABLE_PLACEHOLDER

**TS counterexample** (`ts_cancel.py`; r = 0.5, θ = (1, −2), 20 reps): P(G₁ deletes truth 1 at {1}) = 0.996, 0.998,
0.9992, 0.9997, 0.99984, 0.99993 at n = 200 … 6.25·10⁵, while P(G₂ adds truth 2 at {1}) = 1.000. Repair is not
blocked; only the potential's accounting fails.

**LH, configuration B** (`lh_premises.py`, `lh_fs_gap.py`). p = 20, five groups of 4 (ρ = 0.7), pairs (0,4), (8,12)
with ψ = 0.5, θ = (1.4, −0.7, 1.8, −0.9), x = S° = {0, 8}, B = 4, blocks = groups. Exact per-label bad probabilities
over the whole family: 6,112 phase-1 states for 𝒵♯ and 14,893 phase-2 states (a = 6). I-move entries use the §7
upper bound.

- *Population (n-free) checks over all 6,112 phase-1 states:*
  - TS min loss 0.168 (> 0);
  - at most 4 substitutes, all of the cross-pair type;
  - min loss over neighbours 0.168;
  - ULR min loss 0.0137;
  - GS: Δ_{4} = 0.3675, Δ_{12} = 0.6075, Δ_{4,12} = 0.975, equal to Σψ²β²(1−ψ²) as derived;
  - max junk leakage |δ|/(n−1) = 2·10⁻¹⁶ (ZJL).
- *[B]'s family vs 𝒵♯ at n = 1600:*
  - [B]: A_nb = {1,2,3,5,6,7,9,10,11,13,14,15} includes the useless group-mates {1,2,3}, {9,10,11} of the present
    hubs, so a = 12 and v = 14.
  - [B]: at W* = S° + {1}, the uniform-swap bad probability is 0.088; across the family, the U part of η₁ is 0.43.
  - 𝒵♯: the U part of η₁ is 0.0625 = 4/64. That is exactly the substitute count over k(p−k), i.e. the D′/p term,
    which needs p → ∞.

*SH = 𝒵♯ family, x = S°, a = 6, v = 8 (2 replicates per n; ranges shown):*

| n | 1−π₀(S°) | η₁♯ total | phase-1 junk (TL♯) | phase-1 U (substitutes) | I-move | η₂ total | phase-2 null additions (NL0) | ε_del | c₂ | c_*♯ | H′ | P(Bin(H′,c_*) < 8) | H′·η |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 400 | 0.0814–0.0844 | 0.857–1.44 | 0.625–1.12 | 0.151–0.242 | 0.0814–0.0844 | 0.938–1.89 | 0.856–1.81 | 0.265–0.388 | 0.07–0.194 | 0.07–0.194 | 14 | 0.998–1 | 25.1–46.7 |
| 1600 | 0.0396–0.0406 | 0.355–0.421 | 0.252–0.319 | 0.0625 | 0.0396–0.0406 | 0.373–0.478 | 0.333–0.439 | 0.06–0.148 | 0.332–0.42 | 0.332–0.42 | 16 | 0.658–0.875 | 11.7–14.4 |
| 6400 | 0.0192–0.0196 | 0.216–0.251 | 0.135–0.169 | 0.0625 | 0.0192–0.0196 | 0.201–0.311 | 0.182–0.291 | 0.0279–0.162 | 0.328–0.463 | 0.328–0.463 | 18 | 0.351–0.792 | 7.51–10.1 |
| 25600 | 0.0102–0.0105 | 0.164–0.24 | 0.0914–0.167 | 0.0625 | 0.0102–0.0105 | 0.151–0.287 | 0.14–0.277 | 0.0713–0.0857 | 0.409–0.423 | 0.409–0.423 | 20 | 0.335–0.383 | 6.3–10.5 |
| 102400 | 0.00484–0.00492 | 0.131–0.135 | 0.0638–0.0678 | 0.0625 | 0.00484–0.00492 | 0.108–0.116 | 0.103–0.111 | 0.0414–0.0462 | 0.451–0.456 | 0.451–0.456 | 22 | 0.139–0.149 | 5.27–5.53 |
| 409600 | 0.00241–0.00278 | 0.0871–0.0951 | 0.0221–0.0299 | 0.0625 | 0.00241–0.00278 | 0.0341–0.05 | 0.0317–0.0472 | 0.00728–0.0176 | 0.481–0.492 | 0.481–0.492 | 24 | 0.0384–0.0478 | 2.91–3.48 |
| 1638400 | 0.00124–0.00134 | 0.0722–0.0849 | 0.00842–0.021 | 0.0625 | 0.00124–0.00134 | 0.0123–0.0497 | 0.011–0.0484 | 0.00126–0.03 | 0.469–0.498 | 0.469–0.498 | 26 | 0.0152–0.0305 | 2.19–3.5 |

Reading:
- Every bad-rate term decays at the predicted rate: the junk additions (TL♯), the null additions at supersets (NL0)
  and the independence move. 1 − π₀(S°) halves per 4× in n, i.e. n^{−1/2}.
- The one exception is the swap-substitute term, which is exactly 0.0625 = 4/(4·16) at every n. It is the D′/p term
  and needs p → ∞, so H′η cannot reach 0 at p = 20 (2.2–3.5 at n = 1.6·10⁶).
- The binomial factor reaches 0.015–0.03 at n = 1.6·10⁶.
- [B]'s family (W1), same data: the U part of η₁ is 0.429 at n = 1600 and 0.437 at n = 102400. It does not decay,
  and the per-state rate at W* = S° + {1} is 0.098 at both n. This is the §5.1 counterexample.

## 5. What fails, and why

- **NL0/UDEL without a design condition.** With common-factor or equicorrelated nulls, the residual Z-statistic of a
  null given another null is inflated by up to a factor (1+r). The sup over pairs then reaches odds p^r/√n. This is
  the same phenomenon [B] saw in S5. A sum-of-sups bad rate cannot avoid it; only a state-averaged (drift) version
  of Theorem B could. That version is OPEN ([B] Prop. D is still sup-based).
- **TS under cancellation.** It is a real failure of the potential (truth removal counted as regress), not of
  repair. A layered potential is the fix and is OPEN.
- **[B]'s family with A = the method's neighbour graph.** Under the symmetric union, the group-mates of the *present*
  partner hub are neighbours of the masked hub. They carry no residual signal, and swapping them for junk exits the
  family. Fixed by Theorem B♯ with a useful-look-alike map, which is a proof device the method does not use.
- **Swap substitutes at fixed p.** The uniform swap proposes a given pair with probability 1/(k(p−k)), so a bounded
  number of substitutes costs D′/p per round. This vanishes only if p_n/log n → ∞. It is harmless in the SMC branch
  for p ≥ n^a, but it is visible at p = 20.
- **IND-M for superset starts.** If π₀ concentrates on S° ⊋ S₀ (double counting across split groups, as [B] saw at
  n = 200 in S3/S4/S6), the draw S° is bad at supersets with fewer extras. Its acceptance e^{d(S°)−d(W)} has no
  reason to be small. OPEN; plausibly false at finite n.
- **TL♯ in random designs.** ZJL is exact zero leakage. With iid Gaussian rows, max-type NL_η fails at fixed SNR
  ([E]), and an average/Beta argument would be needed. OPEN.
- **Rates.** Every o_P(1/log n) here holds, but the binomial factor P(Bin(L+5, c) < v) decays like n^{−c/(v ln 2)}.
  For LH configuration B (v = 8, c ≈ 0.3–0.46), it is still 0.2–0.9 at n ≤ 1.6·10⁶.

## 6. Needs escalation

1. **Naming (HQ).** The register should split IND into IND-T (now PROVED) and IND-M (PROVED UNDER SCR + GS; superset
   starts OPEN). The task file's description of IND as "open in the masked regime" conflates them.
2. **Review of Prop. B1′ and Theorem B♯ (independent prover).** Both modify [B]'s proof. The delicate points:
   - the independence of J* from 𝓗 in B1′ (argmin of iid arrival times, plus the label-attached realisation of the
     round);
   - the closure step (F3) of the monotone family.
3. **Review of Lemma CMP** (partial-correlation recursion, constants C_a), and of the extreme-value step in the EQ
   counterexample.
4. **The two numerical population inequalities on LH** (FS-neighbour gap 0.168, ULR 0.0137) should be proved
   symbolically for general (ρ, ψ, g). They are finite-dimensional per component type. Prefer an independent check.
5. **Implementation (Felipe/HQ).**
   - IND-T rests on EX-S. The production streams are xoshiro256** seeded by SplitMix64 of seed·2³² + stream, with no
     jump-ahead separation. That is fine as an idealisation but should be stated.
   - Also confirm that the stage-T round is meant to count as terminal (H′ = L + 5).

## 7. Outside scope (found, not pursued)

- [B]'s REPORT lists (R5) as "per-particle fresh randomness (METHODOLOGY §§6.5, 6.6, 6.8)". The code does not use
  per-particle streams; IND-T shows this does not matter under EX-S. But any future *parallel* implementation that
  splits the stream by particle count would change the realised trajectories, though not the law.
- At n = 200 in S3/S4/S6 [B] saw π₀ concentrating on supersets of S₀. That is exactly the case where IND-M is OPEN.
  It may also bear on T38(b) delivery: a superset start is "near-truth" but the independence move can pull particles
  back to it.
- The LH swap substitutes are *cross-pair*: an added masked hub replaced by the other pair's masked hub or one of its
  look-alikes. That suggests a potential counting "missing residual signal" rather than |M| would remove both the
  TS and the FS issues. Not pursued.

## 8. Confidence cards

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change needed? |
|---|---|---|---|---|---|
| IND-T | Theorem IND-T (§1) | 0.97 | done (PROVED) | stopping-time reading of the code's sequential stream | no |
| Lemma U (shared with EXP′) | §2 | 0.97 | done | [E] Lemmas 1.1–1.4 are block-free | no |
| τ₂ at supersets (all non-I labels) | Prop. T2 | 0.95 | done | swap comparison through W ∪ l | no |
| NL0(a), UDEL(a≥2) | under PG; false without (EQ) | 0.9 (statement) / 0.9 (CE) | done (review CMP) | Lemma CMP; extreme values | no |
| BTP removal | Props. B1′ + PA | 0.92 | done (review) | J* independent of the pre-τ path | no |
| Theorem B♯ | §5.2 | 0.9 | done (review) | closure (F3) with monotone 𝔄 | no |
| TS | under TS(𝒲); false in general | 0.95 | done | — | no (layered potential would need new proof, not a method change) |
| swaps (FS), TL♯, ULR | §6 | 0.85 | 0.7 for general designs (bounded-leakage TL, random designs) | ZJL is exact zero leakage | no |
| IND-M | under SCR + GS, x ⊇ S° | 0.9 | done; superset starts 0.3 | superset starts S° ⊋ S₀ | possibly (if superset starts matter: e.g. no independence move at φ = 1 in terminal rounds) |
| Theorem L (LH, all premises) | §8 | 0.85 | 0.75 (two population inequalities symbolically) | FS-neighbour gap and ULR for general (ρ, ψ, g) | no |
| Corollary A as a useful finite-n statement | §9 | — | 0.2 (single particle) | binomial factor with H′ ≈ log₂ n | no; multi-particle route is the operative one |

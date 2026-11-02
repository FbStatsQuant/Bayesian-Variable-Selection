# API-VSTAB: Claude check of A-REV7's STAB-LH certificate and the no-LS0 masked theorem

Run: API-VSTAB (Claude Opus 5.5), 2026-11-02, branch `theory/API-VSTAB`.

Sources checked (frozen branch heads fetched 2026-11-02):
- `theory/A-REV7` REVIEW.md §3 and §4, the referee text under check;
- `theory/W5-B2ENV` PROOF.md §§0, 2.1–2.2, 4.1–4.5, the theorem B2-LH that A-REV7 verified conditionally;
- `theory/W1-EXP` PROOF.md §4.1–4.2, the LH definition and Lemmas 4.1–4.2;
- `theory/T38-RECORD` T38_STATEMENT.md (I.B STAB-LH, I.C (b2-LH)), REGISTRY_v2.md and LOCKABLE_v2.md;
- `Docs/Methodology/METHODOLOGY_v3.md` §§4–6, `Scripts/SMC_BVS/core/cpp/v3_engine.h`, and `theory_campaign/HQ/SR_AUDIT.md`.

All verdicts below are by a Claude model. Like every result in this campaign, they are candidates: not adopted.

## 1. Headline

- **Every step that A-REV7 §4 (and the §3 pieces named in the task) adds is VERIFIED.** That covers the analytic STAB certificate, the concrete growing-p subfamily, the η_n event correction, and the fixed-p BG3 chain: the common data event, start-mass injection, the all-move exit bound, the 1/m! repair order and the BG3 inequality. I found **no GAP and no ERROR**. Five remarks (R1–R5) are clarifications, not repairs.
- **The STAB certificate is PROVED** (I checked it line by line). If λ₀b_vis² > R_M, then m_STAB ≥ λ₀b_vis² − R_M. A Claude-written exact check, independent of W5 and A-REV7 code, confirms it:
  - on A-REV7's instance (g = 9, c = 2, ρ = 0.4, ψ = 0.2, β = 1), the exact m_STAB = **0.5728**, which is ≥ 0.4032;
  - in 1500 random LH configurations there were **0** violations.
- **Resulting theorem (§3 below).** The unchanged v3 method, with no LS0, has P(output ∩ {Ŝ ≠ S₀}) → 0 on an explicit masked, growing-p, exact-Gram LH subfamily, under EX-A, EX-S, SR, CAL and (P).
  - Its theorem-specific parts are now **cross-family verified in both directions**: W5's Claude-authored B2-LH by Astra (A-REV7), and Astra's certificate, instance and η_n correction by Claude (this run).
  - The cited inputs keep their own registry statuses. Note that IND-T is VERIFIED* by A-REV1 only, with no same-family verifier.
- **New corollary, PROVED.** On the same parameter region {λ₀b_vis² > R_M}, A-REV7 §3's strict-gap hypotheses C1–C3 hold at every fixed p. So the fixed-p BG3/LH-lock component result also holds there with no further hypothesis.

## 2. Verdict table

"Engine" refers to `v3_engine.h` line numbers.

| # | A-REV7 step | Verdict | Checked against / note |
|---|---|---|---|
| 1 | §3 **common data event**. A single event E_n, with P₀(E_n) → 1 and a deterministic tolerance, makes every strict population gap a log-score margin ≥ an. P₀(E_nᶜ) is added once. | VERIFIED | At fixed p the family of sets is finite. RSS(T)/(n−1) = σ² + Δ(T) + O_P(n^{−1/2}) uniformly (Gaussian cross-term and χ² tails). Q = RSS_y + O(1) by W1-EXP Lemma 1.1. Determinant and prior terms are O(log n). The deterministic tolerance n^{−1/4} works. |
| 2 | §3 **start mass**. Add a missing visible hub; summing gives π₀(Uᶜ) ≤ Ce^{−an}, with U = {T ⊇ S°}. | VERIFIED | Block tables use the full response. By W1-EXP Lemma 4.1(c), P_{C_h}μ = γ_t x_t, with γ_t = β(1−ψ²) or β_h. Adding t to any U ⊆ C_h∖t reduces the block RSS by ≥ (n−1)λ₀γ_t² (Schur bound), so the gain is exponential. The size-prior factor is ≤ (2p)^{\|A\|}. The map T ↦ T ∪ S° is at most 2^s-to-1, and K = p makes it feasible. This is the same argument as W5 Lemma 2.2(iii). |
| 3 | §3 **all move types**: ε_U ≤ Cm e^{−an}, m = p + B + 2. | VERIFIED | Engine lines 113–194:<br>• **Gibbs**: the deletion probability is ≤ γ_φ(V−t)/γ_φ(V) ≤ max of the two endpoint ratios (Lemma A).<br>• **Uniform swap**: no Hastings factor.<br>• **Neighbour swap**: Hastings factor \|N(j)∖S\|/\|N(l)∖S′\| ≤ B ≤ p (engine lines 152–174).<br>• **Independence step**: S′ is an exact π₀ draw (`draw_pi0`, engine lines 175–186), so P(exit) ≤ π₀(Uᶜ) whatever the acceptance rule. It occurs once per round.<br>• **Additions** cannot leave U.<br>The first-exit union over the m labels is correct, and an end-of-round exit implies some step left U. |
| 4 | §3 **terminal repair order**, probability ≥ 1/m!: missing hubs first, then the extras of y, then the rest. β₁ ≥ (1 − o(1))/m!. | VERIFIED | The round order is a uniform Fisher–Yates permutation of the m labels (engine lines 188–196). Terminal rounds run at φ = 1 (engine lines 341–360).<br>• **Hub additions.** Hub gain (G) needs no hypothesis on LH: for V ∋ j_a with j_b ∉ V, the gain is ≥ λ₀ψ²β² > 0. The check found a minimum of 0.0261 ≥ 0.0192 on the instance.<br>• **Extra deletions.** With S₀ ⊆ V, extras have zero signal (PZL; the check found 3e−18). The finitely many keep odds are O_P(n^{−1/2}).<br>• **Scoring.** The last Gibbs step evaluates S₀ whether or not the move is accepted (engine lines 113–132; SR).<br>• **y = S₀.** S₀ was scored on entry: every state a particle enters, including initial draws, is evaluated (engine line 289; SR_AUDIT item 4). |
| 5 | §3 **BG3 inequality without conditioning on a future survival event**: P(S₀ unscored) ≤ Nπ₀(Uᶜ) + N(T+L+4)ε_U + e^{−N(L+4)β₁}. | VERIFIED | Let A_k := {round k fails} ∩ {all starts ∈ U up to k}. Then {start of round k ∈ U} is F_{k−1}-measurable, and P(A_k \| F_{k−1}) ≤ (1−β₁)1{A_{k−1}}. Induction gives ∏(1−β₁). Resampling copies states, so a first entry into Uᶜ happens at an initial draw or at the end of a round. There are N(T+L+4) rounds: the T stage mutations, L burn-in and Hm = 4 measured rounds (engine lines 323–360). Burn-in rounds emit score events, since every `eval` call emits; the only `emit=false` call is the local-search centre, which is already scored. Using only L+4 of the L+5 post-resampling rounds is conservative. |
| 6 | §4 **uniform likelihood events U1–U3, Lemma J** (\|𝔉\| = O(p^{v_max}), p4^g normals, truncation, E[e^{Z²/2}1{\|Z\|≤z}] = 2z/√(2π)) | VERIFIED | The integral is exact: φ(z)e^{z²/2} = 1/√(2π). The union bound for (U3) is ≤ (log n·√(πx))^{−1} → 0. Each residualised noise coordinate depends on V only through V ∩ u(l), by exact unit orthogonality and ZJL (the check found 1e−16 on random V ⊇ S°). |
| 7 | §4 **η_n correction**: U2's χ² error σ²n^{2/3} gives relative error O(n^{−1/3}), not O(√(log n/n)). | VERIFIED (A-REV7's correction is right) | W5 Lemma J writes η_n = O(√(log n/n)), but U2 as displayed only gives n^{−1/3}. Lemma J needs e^{2η_n z_n²} → 1, with z_n² ≍ log n, and n^{−1/3}log n → 0 is enough. No stated order changes. |
| 8 | §4 **confinement against actual moves** (CONF: predrawn S′, NGI product bound ε^r/r!, neutral accounting, k = 19 and k₁ = 40, a_n = O_P((log n/n)^{3/2}), N T_e a_n = O_P(log^{7/2}n/√n)) | VERIFIED | **NGIs.** Initial neutrals that survive their own label are NGIs (an execution that ends with l included), so they are counted correctly. At most B+1 ≤ 17 swap labels each add at most one variable.<br>**Rate.** In a_n the j-split terms are: ε³ ≍ (log n/n)^{3/2}, π₀(ν≥1)ε² ≍ n^{−3/2}log n, and q³ ≍ n^{−3/2}. N ≤ 4max(2500, n) and T_e ≤ 4max(1000, ℓ²) = O(log²n).<br>**Independence step.** Predrawing S′ is legitimate under fresh randomness (EX-S). |
| 9 | §4 **repair R1**: order constant c_* = g^{−c}/C(2cg+19+B+2, B+2); stage T suffices. | VERIFIED | **Order event.** P(O) = g^{−c_x}/C(\|Λ_x\|+B+2, B+2) exactly. "All Λ_x before all non-Gibbs labels" depends only on the position pattern, "hub first in its group" depends only on the relative order inside Λ_x, and the two are independent under a uniform permutation. c_* matches W5's lower bound with k = 19.<br>**Chain of failures.** Each failure bound holds on states in 𝒩′ ⊇ S°: deletion part of STAB, (G), and ε_n and ε′_n from Lemma J. Proxies of present-hub groups outside x are covered by the extra cg·ε′_n term.<br>**Product over particles.** Conditional on F_{T−1} and the stage-T resampling, the N stage-T rounds are independent. E is F_{T−1}-measurable, so nothing future is conditioned on. |
| 10 | §4 **analytic STAB certificate**: λ₀b_vis² > R_M ⇒ m_STAB ≥ λ₀b_vis² − R_M | VERIFIED; PROVED here, §4.1 | (i) Δ(V) ≤ Δ(S°) = R_M for V ⊇ S°. Δ is monotone; units are orthogonal; each pair's residual with only its a-hub is β²ψ²(1−ψ²); visible units have residual 0.<br>(ii) Every deletion or swap of t ∈ S° gives a set W ∌ t, and Δ(W) = min_{b: supp b ⊆ W}(θ−b)ᵀΣ(θ−b) ≥ λ_min(Σ)θ_t².<br>(iii) λ_min(Σ_LH) ≥ (1−max\|ψ\|)(1−ρ₊), by W1-EXP Lemma 4.1(a), whose Cauchy–Schwarz proof I re-checked; numerically λ_min = 0.528 ≥ 0.48 on the instance.<br>Swaps to l ∉ 𝒮𝒰 and to any proxy, in any unit, are covered. Null columns are irrelevant. |
| 11 | §4 **C3 and block keep bounds** (no hypothesis needed) | VERIFIED | C3 is W5 (G). Start-side block bounds are W5 Lemma T, case i = 0. A within-block swap gives a Schur residual ≥ (n−1)λ₀γ_t². In a cross-block swap the table factorises into e_n/(2p) times p4^g log n. Neither part uses m_STAB. |
| 12 | §4 **concrete subfamily** (g = 9, c = 2, v = 0, ρ = 0.4, ψ = 0.2, β = 1, σ² = 1, p_n = 9⌊n/18⌋) | VERIFIED (with remark R1) | **Certificate values.** λ₀ = 0.48, R_M = 0.0768, b_vis² = 1, margin 0.4032; exact m_STAB = 0.5728.<br>**LH conditions.** \|ψ\| = 0.2 < ρ = 0.4. B = min(⌊√n⌋, ⌊√p⌋, 16) (Methodology §4 table) equals 16 once p ≥ 256, so g ≤ B < 2g and blocks are groups (W1-EXP Lemma 4.2).<br>**Exact Gram.** p_n ≤ n/2 ≤ n−1, so an exact centred Gram exists. K = min(p, ⌊n/2⌋) = p.<br>**SMC branch.** E = 2^p exceeds (5H₀+4N₀)p = O(n²), so the exact branch (Methodology §6.2) is never taken asymptotically.<br>**Masking.** π₀(S₀) = p^{−2}n^{−1}e^{O_P(1)} (W1-EXP Thm 5(b)), against an iid budget O(n log²n): the product ≍ log²n/p² → 0.<br>**Posterior.** T03 premises hold by W1-EXP Thm 5(d). |
| 13 | §4 "B2-LH proves P(output and wrong) → 0; integrate truncated at one; no unconditional rate" | VERIFIED | This is the T38E-R composition. It does **not** give completion, a finite-n rate, or accuracy conditional on a rare output, and A-REV7 says so. |
| 14 | §7 reproduced numbers used by §4/§5 | VERIFIED (independent code) | **Within-unit swap margin.** 0.606926504 at g = 9, ρ = 0.4, ψ = 0.2, matching A-REV7's 0.6069265045.<br>**§5 witness.** Δ(V) = 0.3675, Δ(W) = 0.3627106863596872, improvement 0.004789313640313, all exact.<br>**Brute force.** Type reduction agrees with brute force over all S° ⊆ V ⊆ 𝒮𝒰 in 4 small cases, including the g = 4, (0.85, 0.5) failure −0.0047893136. |

### Remarks (clarifications, not GAPs)

- **R1 (instance specification).** A-REV7 writes "ρ = .4" without saying what within-group correlation the appended null groups have.
  - The certificate needs only λ_min on the signal units. The null-group Δ terms vanish because the null groups are orthogonal and carry no signal.
  - B2-LH's (U1) and Lemma 4.2 need every group to have ρ_h ∈ [ρ₋, ρ₊] ⊂ (0,1), fixed.
  - So state the instance as: all groups have ρ_h = 0.4, or any fixed values in a compact subset of (0,1).
- **R2 (which move binds).** The margin A-REV7 reports in §7 (0.6069) is the within-unit swap margin. On the c = 2 instance the binding move is a **cross-unit** swap: drop the a-hub of one pair and add a variable of the other pair's unit, giving m_STAB = 0.5728. This does not affect A-REV7's claim, which is a lower bound of 0.4032.
- **R3 (sharper certificate).** Replacing λ₀ by the exact λ_min(Σ_{𝒮𝒰}) is still a valid sufficient condition (proof unchanged); on the instance it gives 0.4516. The certificate is a strict subset of the STAB region: in the sweep it applied in 820 of the 1149 STAB-true draws, and in no STAB-false draw.
- **R4 (size of constants).** c_* = 1/(81·C(73,18)) ≈ 10^{−18.3} on the instance, and c₀(S°) ≈ 10^{−12.6}. So (1 − c_*)^N → 0 only for astronomically large N. The theorem is asymptotic only, and A-REV7 does not claim otherwise.
- **R5 (IND-T).** The product over particles uses fresh randomness per particle-round. The engine reads one shared stream, which is covered by W2-PREM IND-T. Its registry status is author PROVED, XF VERIFIED* (A-REV1, uninterrupted process), and no same-family verifier. That is the one cited input of B2-LH with no Claude verifier. It sits outside this task.

## 3. The resulting theorem (statement of record proposal)

**Theorem (no-LS0 masked consistency on an explicit LH subfamily).**

*Family 𝔉_cert.* LH with an exact centred Gram, X′X = (n−1)Σ_LH, as in W1-EXP §4.1 and W5-B2ENV §0, with:
- fixed g, c ≥ 1, v ≥ 0;
- all within-group correlations ρ_h fixed in a compact subset of (0,1);
- linked pairs with 0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i});
- fixed nonzero β_i and β_h, and fixed σ² > 0;
- p = p_n ≤ n − 1 and g ≤ B_n < 2g for all large n;
- the population condition **(CERT)**: λ₀ b_vis² > R_M, where
  - λ₀ := (1 − max_i|ψ_i|)(1 − max_{h∈signal groups} ρ_h),
  - R_M := Σ_i β_i²ψ_i²(1 − ψ_i²),
  - b_vis² := min(min_i β_i², min_h β_h²).

*Explicit member.* g = 9, c = 2, v = 0, all ρ_h = 0.4, ψ₁ = ψ₂ = 0.2, β₁ = β₂ = 1, σ² = 1 and p_n = 9⌊n/18⌋. This member is masked: π₀(S₀)·(iid budget) → 0, and the run is asymptotically in the SMC branch.

*Hypotheses on the method.*
- v3 as run, with no LS0;
- EX-A, EX-S, SR, CAL, and the output-potential convention;
- (P) from locked T03 via W1-EXP Thm 5(d);
- IND-T for the shared stream.

*Conclusion.*
1. On an event 𝔈_n with P₀(𝔈_n) → 1, for every successful calibration 𝓒 (any frozen grid with T ≤ T_e) and one final island with N = N_e particles:

   P(S₀ ∉ 𝒮 | 𝓒, data) ≤ Nπ₀(𝒩ᶜ) + N T_e a_n + (1 − c_* + r_n)^N → 0,

   with a_n = O_P((log n/n)^{3/2}) and c_* = g^{−c}/C(2cg + 19 + B + 2, B + 2).
2. Hence P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 and liminf P(𝒪 ∩ {Ŝ = S₀}) ≥ 1 − limsup P(no output).

*Not claimed:*
- completion (an output is not guaranteed);
- an unconditional numerical rate;
- finite-n accuracy;
- unrestricted LH (general locking is false: A-REV7 §5, reproduced here);
- random or iid designs.

*Status.*
- B2-LH: author PROVED-UNDER STAB-LH (W5-B2ENV); XF VERIFIED, conditional on STAB (A-REV7).
- STAB certificate and subfamily: Astra-authored (A-REV7); **Claude VERIFIED (this run)**.
- The composite theorem: PROVED (candidate), given the cited inputs.

*Cross-family status.*
- Both directions are now covered for the theorem-specific parts: CONF and R1 by Astra, and the certificate, instance and η_n by Claude.
- The inputs carry their own statuses: [E-T1], [E-L4], [E-T5d] VERIFIED; T03 locked; T38E-R VERIFIED; IND-T VERIFIED* (Astra only).

**Corollary (fixed-p component, PROVED here).** On (CERT), A-REV7 §3's hypotheses C1–C3 hold strictly at every fixed p:
- C1 and C2 by the certificate, since m_STAB does not depend on p or on the null columns;
- C3 by W5 (G).

Hence the fixed-p BG3/LH-lock bound of A-REV7 §3 holds on (CERT) with no further hypothesis. It remains a *component* result, because fixed-p production problems are eventually enumerated (Methodology §6.2).

### 4.1 Proof of the certificate, written out
Use exact Gram, so Δ(V) = min_{b: supp b⊆V}(θ − b)ᵀΣ(θ − b).

1. **Upper bound on Δ(V).** For V ⊇ S°: Δ(V) ≤ Δ(S°). Unit orthogonality splits Δ(S°) into a sum over units:
   - a visible unit contributes 0;
   - pair unit i, with only j_{a_i} present, contributes β_i²·Var(x_a − ψx_b | x_a) = β_i²ψ²(1 − ψ²).

   So Δ(V) ≤ R_M.
2. **Lower bound on Δ(W).** Let W ∌ t with t ∈ S°. For any b supported on W, (θ − b)_t = θ_t, so (θ − b)ᵀΣ(θ − b) ≥ λ_min(Σ)‖θ − b‖² ≥ λ_min(Σ)θ_t². Moreover λ_min(Σ_LH) ≥ λ₀ (W1-EXP Lemma 4.1(a)): on a linked pair, x′Σ_aa x + y′Σ_bb y + 2ψ(x′Σ_aa e_a)(e_b′Σ_bb y) ≥ (1 − |ψ|)(‖x‖²_a + ‖y‖²_b) by Cauchy–Schwarz, and λ_min of an equicorrelation block is 1 − ρ_h. Null groups do not enter: b is optimally 0 on them, because they are orthogonal to signal.
3. **Combine.** Every deletion V − t and every swap V − t + l, for any l ∉ V, is such a W. So Δ(W) − Δ(V) ≥ λ₀θ_t² − R_M ≥ λ₀b_vis² − R_M. ∎

## 4. Evidence

- **Script and outputs.** The script is `scripts/vstab_check.py`; outputs are in `scripts/vstab_check.txt` and `scripts/vstab_check.json`.
- **How it was run.** Under owls_run with `-j 1`, seed 20261102.
- **Independence.** It is written from the LH definition and imports no W5 or A-REV7 code.
- **Results.**
  - **C0.** λ_min ≥ λ₀ in all 1500 draws and on the instance.
  - **C1.** Type-reduced m_STAB agrees exactly with brute force over all S° ⊆ V ⊆ 𝒮𝒰, in 4 small cases.
  - **C2.** On the instance: m_del = 0.6112, m_wswap = 0.6069, m_xswap = 0.5728, so m_STAB = 0.5728 ≥ 0.4032. Δ(S°) = R_M = 0.0768.
  - **C3.** Random sweep, 1500 draws: g ∈ [2,6], c ∈ {1,2}, v ∈ {0,1,2}, random ρ, ψ, β. **0 violations** of m_STAB ≥ λ₀b_vis² − R_M; the minimum slack is 2.7e−4 > 0.
  - **C4.** On random V ⊇ S° in the instance: ZJL max 1e−16 and PZL max 3e−18. The minimum hub gain is 0.0261, against the bound λ₀ψ²β² = 0.0192.
  - **C5.** A-REV7 §5's swap witness, an ERROR against unrestricted LH-lock, is reproduced exactly.
- **What was not run.** No full SMC simulation. It is not needed for any of these steps, and the asymptotic constants (R4) make finite-n runs uninformative about the bound.

## 5. What fails and why

- **No step failed verification.** The only route I considered and dropped was strengthening the certificate to an iff characterisation of STAB. That is not possible: the certificate is strictly smaller than the STAB region (R3), and the true STAB boundary is set by the cross-unit or within-unit swap types (W5 §4.1). That is out of scope.

## 6. Needs escalation

- **IND-T.** It has no Claude verifier (R5). That matters only if the paper does not simply assume fresh randomness per particle-round.
- **CONF and R1 have now been read by Astra and by this run.** An independent Claude-family check of W5's full PROOF.md §4 (Lemma 2.2 start tails, Lemma T case i = 0) went beyond A-REV7 §4's paragraphs. I read those lemmas as well and found no problem, but not with the same line-by-line care as items 1–12.

## 7. Outside scope

- **The fixed-p corollary in §3** is a cheap strengthening of O-BGIBBS's LH-lock. Under (CERT) the strict-gap hypotheses are automatic. HQ may want to record it next to the `OBG-T38b-BG3` row.
- **Sharper certificate.** For the instance, the sharper certificate λ_min(Σ_{𝒮𝒰})b_vis² − R_M = 0.4516 is available at no cost.

## 8. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| STAB certificate | (CERT) ⇒ m_STAB ≥ λ₀b_vis² − R_M | high (PROVED, numerically confirmed) | done | λ_min lower bound + Δ(V) ≤ Δ(S°) | no |
| B2-LH on 𝔉_cert, including the explicit instance | P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 for v3 as run | high | done (conditional on cited inputs incl. IND-T) | CONF (bounded neutral extras, non-persistent junk) + R1 order event | no |
| Fixed-p BG3/LH-lock on (CERT) | §3 bound with no extra hypothesis | high | done | C1–C3 from the certificate and (G) | no (component only) |
| Unrestricted LH no-LS0 | — | low/unknown | not by this route (A-REV7 §5 counterexample to C2) | profitable swaps out of the visible-superset class | maybe |

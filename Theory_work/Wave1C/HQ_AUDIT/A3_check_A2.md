# A3 — Cross-family check of A2 (Proposition F on the C-GROW class)

Reviewer: Claude Opus 5.5 (cross-family to the A2 author, Codex). Object: `HQ_AUDIT/A2_propF_GROW.md`. Paths below are relative to `Theory_work/Wave1C/` unless stated otherwise.

**Verdict: VERIFIED-WITH-AMENDMENTS.** Both conclusions follow on both GROW instances under A1's corrected premises: P(no output) = 0 for every admissible n ≥ 3, and P(Ŝ⁺ = S₀) → 1 under the unconditioned (fixed-design) or joint (iid-row) law, with no CAL premise. I found no gap and no error. All five amendments below are MINOR: precision, scope wording and status records.

## Line-by-line verification

| A2 step | Check | Result |
|---|---|---|
| Citations (all) | Every path:line cited in A2 says what A2 says it says. I checked A1:7–19, 39–43, 62–75; DLV L1:32–43, 70–83, 110–116, 118–137; L2:6–18, 20–35, 38–70; L4:24–40, 65–77, 80–91; GROW STATEMENT:51–98, 84–88, 102–113, 119–126, 139–149; METHOD_REQUIREMENTS:3–18; L4_assembly:10–14, 25–29; L5_instances:48–68 (Claim (a)); L6:12–16, 35–49, 78–83, 470–476, 478–489; `FINAL/sections/s6_delivery.tex:43` (remark (4), on a single line). | OK. One imprecision: finding 5. |
| S.1 inputs, fixed designs | G (STATEMENT:57) assumes nonconstant raw columns, so A4 is empty. A5 is null by the line argument. The exact-Gram instance has standardised columns with norm n − 1 > 0, so its raw columns are nonconstant. Preprocessing drops only constant columns (`Scripts/SMC_BVS/core/v3_preprocess.R:111–114`). Duplicate columns are only recorded, never a stop (`v3_fit.R:92`). | OK |
| S.1 inputs, iid AR(1) | Σ_jj = 1, so each raw column is iid N(0,1) and nonconstant a.s. In (C5)(c) the raw β = D_x⁻¹θ* depends on X, so this is **not** literally Lemma S's model G. A2 correctly re-proves A5 instead of instantiating it: Cy^r = Xθ* + Cε, and given X, Cε is nondegenerate on 1⊥ (dimension n − 1 ≥ 2), so {Cy^r = 0} is null. Integrating over X gives a joint-law null set. This holds whether the generator passes raw W or pre-standardised X. | OK |
| S.2 numerics | Uses only G_S ⪰ 0 and yᵀy = n − 1. It needs no rank condition and no bound on the relevance size, so p ≫ n is harmless. Under MR1, LS0 still never adds at \|S\| = K, so the k ≤ K invariant holds. | OK |
| S.3 (vii) | Amending "successful construction" to "or completed fallback pilot" is supported by A1:39–41 (endpoints 0 and 1, strict increase, ≤ T₁ intervals) and by L3. | OK |
| Delivery (Step 2) | The extra LS0 work is ≤ K·q(p) requests, each costing ≤ κ + ω ≤ C[n³ + p(n+2)]. Its archive is ≤ (ℓ_n+K+1)·K words, covered by M_G. Corollary R's argument is uniform in data, seed and uniforms, so it carries over with W_G and M_G. With the fallback, 𝒮ℒ_n = ∅, so Theorem D's walk leaves only null exits. Note that this step uses no statistical class property: Lemma S is the only class-dependent input. | OK, see finding 1 |
| Consistency (Step 3) | On Sand_n ∩ NA(𝓛) ∩ TL(𝓛): every maximiser lies in 𝓛, and e4 makes the emitted centre one of them. G1 gives \|Q\| ≤ K, so 𝓛 ⊆ Ω. (C1) then shows LS0 scores S₀ once its cap ≥ \|S̃₀∖S₀\| − 1, and a_n = ℓ_n + \|S̃₀\| exceeds that. The D′ pathwise claim (L4:65–69) needs only scored-set retention, OP-LS0 and e4. Since π ∝ exp F, π(S₀) > ½ makes S₀ the strict F-maximum, which matches M5(0)'s δ₁-corrected deterministic clause (SoP `04_theory.tex` TH05, note 4). Markov's inequality gives P(π(S₀) ≤ ½) ≤ 2E[1 − π(S₀)]. With P(𝒪) = 1: P(Ŝ⁺ ≠ S₀) ≤ 2E[1−π(S₀)] + P(𝒦_nᶜ) → 0. A2 correctly refuses to derive this from D_n → 0, because [OP] bounds in the opposite direction. | OK |
| Posterior input | Fixed designs: (H0) is assumed, and it is verified for (C5)(a) in L5 Claim (a). iid instance: L6.2 gives the A_X events, and the diagonal argument (L6:478–489) gives E[1 − π_X(S₀)] → 0 under the joint law. This uses neither GEN's bounded-relevance certificate nor (H0) on every realisation. | OK |
| CAL | Sand, NA and TL are functions of (X, y) only. A2 bypasses GROW's CAL-bearing [M5-0] assembly (STATEMENT:73; L4_assembly:8–9) through D′'s pathwise claim. | OK — not needed |
| IND-T / R′ > 4 | GROW lists IND-T and the extra c₄ search when R′ > 4. The pathwise claim uses only the fact that LS0's scored models join 𝒮⁺, and the extra searches only add scored models. DLV L4:8 already records that IND-T is unused. | OK — not needed |
| SIZE-type conditions | For GROW, the role of SIZE is played by (G1) (\|Q\| ≤ K, the K-gap), together with s₀ ≤ K eventually. Both are inside the cited hypotheses. LH's SIZE (A1:56) is irrelevant here. | OK |

## Findings

1. **MINOR — the LS0 score count in Theorem D's walk is not explicitly amended.** A2 Step 2 reuses the walk of `C-DLV/lemmas/L4_delivery.md:24–40`. That walk states "scores ≤ 1 + (ℓ+1)(p + p²/4)" (:38), and Lemma R's LS0 row (L1:25) and count (L1:43, 50–52) also assume cap ℓ. A1:7 flagged all of these. The reasoning in A2 is right, but these lines need an explicit replacement. **Fix:** at the end of Step 2, add: "In L4:38, L1:25 and L1:43, replace ℓ for LS0 by a_n ≤ ℓ_n + K; the LS0 count becomes ≤ 1 + (ℓ_n + K + 1)q(p), and Σ̄ becomes Σ̄ + Kq(p)."

2. **MINOR — S5 scope is not stated.** Class (i) ("fixed designs under G, (H0), (G1)–(G4)") is general, so it also contains (C5)(b), the S5 population covariance at fixed p = 100. That instance satisfies the hypotheses (STATEMENT:127–134), and including it is mathematically correct. However, A2's sentence "Precisely these hypotheses are …:51–98,119–126,139–149" reads as if (b) were excluded. It also omits the fixed-p caveat (STATEMENT:134–138; L6:Corollary L6.8 caveat): for any fixed-p sequence, including (b), fixed-p (a) and (c), and the generator's p = 500/1000 layouts, the exact branch is eventually taken, so the result there follows from T03♯ plus enumeration and LS0 is not the operative mechanism. **Fix:** after the class list, add: "(i) contains the fixed-p illustration (C5)(b); for every fixed-p sequence the conclusion is eventually delivered by enumeration plus T03♯ (STATEMENT:134–138). Random-row S5 (study S5) and the (C6) frontier are not covered."

3. **MINOR — p_raw and the retained p are conflated.** Step 1 says "p_raw = p a.s.". p_raw is the deterministic input column count. What Lemma S gives is that the retained count equals p_raw a.s. This matters only because W_G and M_G are evaluated at p_raw, which is deterministic, so the allocation is a deterministic function of (n, p_raw). **Fix:** reword to "no column is dropped, so the retained p equals p_raw a.s.; the allocation depends only on (n, p_raw)."

4. **MINOR — inherited statuses are not enumerated.** The phrase "All reused results retain their recorded … qualifications" is too thin for a new combined claim. **Fix:** add a status line covering the following points:
   - A1's corrected statement has not been through a separate council (`s6_delivery.tex` statusbox).
   - GROW L4 and L6 are "PROVED (by this seat, unchecked)", with checks R04 and R06/R07 respectively.
   - [OP] is "PROVED (by this seat, unchecked)".
   - e4 rests on N3, which is OPEN.
   - S.3 is a code-reading audit.
   - LS0 is not shipped, and the fallback is an unmade change to a shipped component.
   - A2 itself has been checked only by this A3.
   - The extended Proposition F should therefore be labelled PROVED (A2), checked by A3, not council-passed.

5. **MINOR — a citation range is too broad.** Step 3 says the event bound is "precisely the deterministic/data steps of … L4_assembly.md:25–29". But :25 is the [OP] step, which bounds D_n in the opposite direction, as A2 itself notes. **Fix:** cite `L4_assembly.md:26–28` (descent on Sand ∩ NA ∩ TL, and the cap check) together with :28–29 (event limits).

**Net:** after amendments 1–5, A2's extended statement can replace remark (4) in `FINAL/sections/s6_delivery.tex:43`, with the status label from finding 4.

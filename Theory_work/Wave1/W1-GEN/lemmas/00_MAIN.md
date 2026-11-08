# W1-GEN — Main theorem and proof map

Status: assembly **PROVED (by this seat, unchecked)** from the lemma files below, each with its own status and check
record (reviews/). Statement: STATEMENT.md v2.3 (locked v2; v2.1 (C6) design; v2.2 (C1′) added; v2.3 (C5)(d) layout, (C1′) energy; all logged).

## Theorem GEN (reported-HPM consistency on a general correlated design class)

Assume the fixed-design Gaussian model G with standardized design, fixed s₀ ≥ 1, p ≤ n^A (any fixed A ≥ 1; p ≫ n
allowed), the shipped score/prior/blocks of SMC-BVS v3.1 with LS0, and the named implementation premises (EX-A, EX-S,
CAL, SR, GUARD-W, OP-LS0, e4 [N3 OPEN], complete scans; for R′ > 4 IND-T and the c₄ extra search). Suppose
* (H0) the hypotheses of S-T/T03♯ (R, SE_λ(j₀), SE_w(m♯_n; g₀), BM-∞);
* (H1) a bounded relevance set 𝒱 ⊇ S₀ (|𝒱| ≤ v̄) with a Gram floor on 𝒱 ∪ {l} for every l and separation SEP(c_S):
  no outside variable reduces Λ_S by more than c_S(n − 1)φ₀⁴θ*²_min for any S ⊆ 𝒱 (c_S < 1);
* (H2) a bounded reference S* ⊆ 𝒱 on the actual blocks with within-block SE, VIS(S*) and NL(S*) — e.g. the canonical
  certificate of L8 (block beta-min dichotomy on the block regression coefficients of μ).
Then D_n → 0 and P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; hence liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n). If S* = S₀, (H1) is not
needed. The same holds under random designs when the hypotheses hold on X-events of probability → 1 (C4). Masking is
allowed: truths with no (or negligible) block-level signal are omitted from S* and recovered by LS0's descent.

## Proof map

| Claim | Content | File | Check record |
|---|---|---|---|
| L1 | uniform score expansion (EXP′), RSS floor/ceiling, contrast bounds on polynomial families | L1_lemmaE.md | R02 Sol: VERIFIED-WITH-AMENDMENTS, applied |
| (C1) | start mode = S* w.p. → 1 (T22(iii) re-run with reference S*) | L2_centre.md | R03 Sol: VERIFIED-WITH-AMENDMENTS, applied |
| (C1′) | canonical certificate for (H2b)–(H2c) | L8_certificate.md | checked only inside the sweep R10 (items 1–4, fixed) |
| (C2) prob. | descent events on 2^𝒱 (missing-truth states, supersets, local max at S₀) | L3_descent.md | R04 Sol: VERIFIED-WITH-AMENDMENTS, applied |
| (C2) det. | production search semantics: path in 2^𝒱, τ ≤ 2^{v̄} − 1, scoring vs endpoint | L4_search.md | R04 (same) |
| (C3), (C3-fav), (C4) | assembly with M5(0) + T03♯; de-randomisation | L5_assembly.md | R06 Sol: VERIFIED-WITH-AMENDMENTS, applied |
| (C5) | instances: LH exact Gram, LH-iid, W, study generator | L6_instances.md | R07 Sol: (a)–(c) V-W-A applied; (d) GAP → v2 (Lemma SEL), checked only inside the sweep R10 (one minor item, fixed) |
| (C6) | bounded 𝒱/S* cannot be dropped from the LS0 route | L7_counterexample.md | R06 GAP, R08 GAP, R09 VERIFIED (v3) |

Proof of Theorem GEN: L5.1 (from L2, L3, L4, M5(0), T03♯); (C3-fav): L5.2; random designs: L5.4.

## External inputs (statuses verbatim; never upgraded)
M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF
VERIFIED (A-REV2)"; T22(i) "PROVED-LOCKED"; T22(iii) proof text "PROVED-LOCKED CONDITIONAL" (re-run, EXP′ proved here);
instances: W1-EXP Lemma 4.1(a)/4.2 (via Thm5-LH, SAME-FAMILY-ONLY), W7-PART Theorem B (candidate), [CONC]
(classical); W partition proved inline in L6(c). Operational closure [OP]: PROVED (by this seat, unchecked) from the
named premises, corroborated by [W6] (candidate). Scope: v3.1 + LS0 **as specified** (LS0 is not in production code).

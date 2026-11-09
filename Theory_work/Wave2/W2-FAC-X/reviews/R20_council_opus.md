# R20 — Council seat (Claude Opus 5.5, high) — W2-FAC-X, Theorem FAC-CS-iid

Deliverable reviewed: STATEMENT.md v3 (C1)–(C4); lemmas X1–X6; REPORT.md §1–§4, §6. Brief: reviews/COUNCIL_BRIEF_FINAL.md.
Read: STATEMENT, X1–X6, REPORT, CITECHECK.txt, FAC-B L2 (L2.4) and L3 (event definitions E3–E7), FINAL s3_posterior.tex
(T03♯ hypotheses), iid_core.py, R09_scratch/c3_out.txt and R14_scratch/adv_n0_out.txt (numbers only). I did not read
R08*, R09_council*, R13*, R14_council*, R17*, or any council disposition. Scratch: reviews/R20_scratch/.

## Verdict

| gate | verdict | reason |
|---|---|---|
| G1 correctness | **PASS** | I re-derived every load-bearing step (list below) and found no false step. The chain works: exact rotation (ξ ⊥ W) → resolvent bound with Gaussian conditioning over ξ-defined intervals → feeding the band count back → (R_ϖ) → deterministic soft gap → FAC-B Claim B and end phase with τ̂ = τ + δ. My exact numerics agree with it (see below). |
| G2 hyps used = stated | **PASS** | (CS-R), (P-½), (θ), (FS) and s₀ ≥ 1 are each used where stated. X4 correctly needs no (FS). X5 uses (FS) only for the dichotomy between positive and zero pairs (checked against FAC-B L2.4). The implementation premises are inherited verbatim. |
| G3 no hidden assumptions | **PASS** | N₀ depends on the data. This is neutralised by uniformity over 𝔫 (X4) and by conditioning on Z (X5/X6). Nondegeneracy is an intersected probability-one event (ND_n). The "𝒜_n is a Z-event" claim is correct: the event is in Z, and only its probability bound goes through 𝔈_n. |
| G4 citations/status | **PASS** | CITECHECK: 5/5 and 8/8 OK. I spot-checked FAC-B REPORT:30 ("PROVED-CHECKED", 9.3/9.0), B3 "HOLDS-WITH-AMENDMENTS", Lemma CAP in s7_impl.tex, and T03♯ hypotheses (SE_w with unnormalised g₀ = c₀ is supplied by X6.1). There is no status upgrade: the lemmas say "PROVED (by this seat, unchecked)" and REPORT §1 says "[pending council]". One quotation is truncated (issue 4). |
| G5 constants/rates | **PASS** | ϖ_n = 6C_X H̄√(p log n/n) + n^{−1/3} is used consistently in STATEMENT §3, X2, X4.0 and Cor. X4.1. C_X depends only on ρ. ε_b, K₁, m₁, ε′, T₀, c_w and c₁ are tracked. The absorption arithmetic (ϖ/2 + ϖ/8 + n^{−1/3}/8, slack ≤ 1.5ϖ + C_g n^{−1/2} ≤ 2ϖ) checks. |
| G6 fidelity | **PASS** | The score, prior and move rule in X1.4 and iid_core.py match SoP 04_theory.tex:69-74 (H = (n+1)G + I, ν = n/2 + .01, w(k) = 1/(2·C(2p−1,k)), ratio (2p−k)/k). The neighbourhood is complete (deletion, addition, swap); ties are handled in X4.7; the MR1 cap a_n ≥ m₀ is used essentially. Production gains agree with the (g3) formula to O(1/n) in my run. |

**Overall score: 8.9 / 10.** No REQUIRED issues. Two MINOR and three EDITORIAL issues follow. The MINOR items concern
how accurately §5/§6 describe the frontier, not the theorem.

## Issues

1. **MINOR — the frontier at ½ has a third, independent cause, and for the uniform-in-𝔫 (C2) it is not only a technique
   artefact.** Locations: REPORT §6, growth row, last column ("the band term and the second-order resolvent term are two
   independent reasons the present technique stops at ½"); REPORT flag 4; STATEMENT §5 first bullet ("obstruction of the
   proof technique (worst-case control of band membership …)").
   (C2) is claimed simultaneously for every 𝔫 with |𝔫| ≤ 15. For 𝔫 equal to the 15 largest positive null ξ, the gain of
   re-adding l ∈ 𝔫 at T₀ = [p] ∖ 𝔫 is ≈ ½ξ_max² − ½log n + O(1) ≈ log p − ½log n − ½log log p + O(1). This tends to +∞
   when limsup log p/log n > ½. So (C2)(ii) ("every addition at T has gain ≤ −c log n") is genuinely false beyond ½ in its
   uniform-in-𝔫 form, whatever is done about the band. X4.4's Remark (R14 item 1) already says this margin is binding,
   but §5, §6 and flag 4 attribute the ½ only to the band and second-order terms. Exact check
   (R20_scratch/r20_addmargin_out.txt): the production addition gain tracks ½ξ_max² − ½log n to within ≈ 0.5 and is
   positive at log p/log n ∈ {0.62, 0.64, 0.70, 0.79}.
   **Fix:** In §6 replace "two independent reasons" with three: (a) the band term; (b) the second-order term p^{3/2}/n;
   (c) the bulk addition margin ½log n − log(2p) of the uniform-in-𝔫 device. Say in STATEMENT §5 / REPORT flag 4 that
   going beyond ½ needs both the band decoupling and a replacement for uniformity over 𝔫. For example, control N₀
   directly: it is a block of ≤ 15 nulls whose ξ are not extreme with high probability. This matters for W2-UNI, which
   relies on §6.

2. **MINOR — the REPORT review trail omits the earlier council rounds.** Location: REPORT §4 ("Council: [pending]"), §1.
   The deliverable cites results and items from council seats R09 and R14 and from R13 (X4.4 Remark, the X4.5 audit
   table, REPORT §3 rows), so at least two council rounds took place. §4 does not list them or their outcomes. §4 also
   says "All reviewers via delegate_task (Codex gpt-6.1-sol)", which is inaccurate because the R09/R14 seats were Opus.
   **Fix:** In §4, list each council round (seats, scores, pass/fail, disposition file) and correct the reviewer-family
   sentence. No status change.

3. **EDITORIAL — X4.5 end-phase move count.** Location: X4_path.md, the line "after m₁ − 1 further moves T = S₀".
   **Fix:** Write "after m_{i_e} (≤ m₁ − 1) further moves". The total is exactly m₀ by (C2)(iv).

4. **EDITORIAL — truncated verbatim status.** Location: STATEMENT §7 and REPORT §3 (FAC-A). FAC-A's REPORT reads
   "**PROVED-CHECKED** (for the narrowed, flagged target STATEMENT.md v1.2)".
   **Fix:** Quote the qualifier, and add that only L5.1's de-randomisation pattern is used, which is unaffected by the
   narrowing.

5. **EDITORIAL — B1 at i = i_e.** Location: X4.5 "Entry", which asserts a_{i_e} < 0 < b_{i_e}. B1 is stated for i < i*.
   The wide-phase argument also covers i = i* because N₊ ≥ m₁ − 1, but this is not said. One-sided states are in any
   case handled by the sign/separation invariant.
   **Fix:** Add one sentence: "B1 also holds at i = i* by the same argument (N₊ ≥ m₁ − 1)".

## What I re-derived

* **X1.1–X1.2.** The rotation representation, the independence of (‖e‖, η, φ, ξ, a, W), N = n − 3,
  G^r_T = (1 − ρ)[ṽ1ṽ1ᵀ + A_T], ‖P_Te₁‖² = q/(1 + q) by Sherman–Morrison, and the Schur identity for ω_j.
* **X1.3.** The reference identity N(A⁰)⁻¹ṽ1 = ξ − x_T with ϱ = κℓη, and the drift identities.
* **X1.4.**
  * M_T ≈ ½(1 − q).
  * 1/(1 − γ_k) = 1 + γ_{k−1}.
  * The addition statistic (1 + γ_k)(1 − γ_{k+1})² = 1 − γ_{k+1}.
  * The swap identity V_{jl}.
  * The prior ratio (2p − k)/k for w(k) = 1/(2·C(2p−1, k)).
* **X2.**
  * D5 holds: conditionally on (u_j^⊥, ξ), the W_jl (l ≠ j) are iid N(0, ‖u_j^⊥‖²), and 𝒜_j depends on ξ only. Any
    (a, b) reduces to null-valued endpoints.
  * The decomposition T ∖ j = ([p] ∖ j) ∖ (I ∖ j) Δ (band ∪ E).
  * The bounds for the common term, the a-terms and the normalisation; the second-order term needs p ≤ √n.
  * D6 and D7 are binomial/Chernoff bounds over grids (hazard bound φ/Φ̄ ≤ t + 1); D8 is a separation union bound.
* **X3.** Claims (ii)–(ix) line by line, including both cases of (iii) and the contradiction count in (vii).
* **X4.**
  * Cor. X4.1 arithmetic and the |x_T| ≤ 1.5H̄ envelope (discriminant d(d − 3k) < 0).
  * B2 propagation: b_i − b_{i−1} ≤ w + g_max uses (4.1) at i − 1.
  * B3 Case A: the J″ ≤ 5m_i and 0.34ε_bH computation with FAC-B's E5.
  * B1 wide phase.
  * The bulk addition margin −0.78(½ − A₁) log n.
  * The end-phase exact structure: b is among the top 2m₁ + 1 values via D7 and D8.
  * δ_e ≥ H̄ − H.
  * The X4.6 truth-move bound: (|ϑ|_min√((1 − ρ)N/2) − C√p H̄)².
* **X5.** c(U, l) = (1 − ρ)[ϑ_l + ρϑ(S₀ ∖ U)/(1 + (u − 1)ρ)] from the CS partial covariances, and the
  positive-pair/zero-pair dichotomy against FAC-B L2.4.
* **X6.** Conditioning on Z with integration of D_n(z), and the every-sequence argument for T03♯ (all of T03♯'s
  hypotheses are supplied on 𝒜_n with common constants).

## What I computed (R20_scratch/)

* **r20_checks.py → r20_checks_out.txt.** Exact iid-row sufficient statistics and the exact production LS0 from [p];
  ρ ∈ {0.02, 0.3, 0.5, 0.8}; n ∈ {10⁵, …, 10⁸}; p ≤ 900; log p/log n ≤ 0.495.
  * 20/20 paths are pure null deletions ending at S₀.
  * The exact max_j|δ_j(T)|, sampled along each path, divided by H̄√(p log n/n), stays in 0.16–0.28. It is flat in
    p (100 → 900 at n = 10⁶) and in n (10⁵ → 10⁸ at p = 300), so the √(p log n/n) shape in Proposition X2 is not
    violated.
  * The rule slack is ≤ 1.59·max|δ| (the theory allows 2ϖ ≥ 2.67·max|δ|). The band is ≤ 1.59·max|δ| (the theory allows
    4.3ϖ).
  * The production deletion gains minus the (g3) formula without e¹ and r is about 7/n (7.2e−6 at n = 10⁵, 7.2e−9 at
    n = 10⁸), as (g1)–(g2) predict.
  * The X1.3 reference identity holds to 1e−16, and the (g5) swap identity to 4e−14 over 2000 random (k, κ, τ).
* **r20_addmargin.py → r20_addmargin_out.txt.** Supports issue 1: the adversarial-𝔫 addition gain is
  ≈ ½ξ_max² − ½log n and is positive beyond ½.

No REQUIRED issues. G1–G6 all PASS. Score 8.9.

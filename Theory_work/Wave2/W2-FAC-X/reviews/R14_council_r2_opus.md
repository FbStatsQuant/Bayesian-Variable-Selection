# R14 — Council seat, round 2 (Claude Opus 5.5): Theorem FAC-CS-iid (W2-FAC-X)

Deliverable reviewed: STATEMENT.md v3 (locked), lemmas/X1–X6, REPORT.md §1–§4 and §6 (brief: reviews/COUNCIL_BRIEF.md).
Not reviewed: Target 2 (REPORT §5, X7–X10, T2/, STATEMENT_T2.md). I read round 1 (R08, R09, R08_R09_disposition), but
re-derived the load-bearing steps myself. Scope rule applied: all results are asymptotic, and neither n₀ nor finite-n
behaviour counts as a defect. Scratch: reviews/R14_scratch/ (ident.py, adv_n0.py → adv_n0_out.txt, adv_fail.py →
adv_fail_out.txt).

## Verdict

| gate | verdict |
|---|---|
| G1 correctness of every step | **PASS** |
| G2 hypotheses used = hypotheses stated | **PASS** |
| G3 no hidden assumptions | **PASS** |
| G4 cited lemmas have adequate status | **PASS** |
| G5 constants / rates tracked | **PASS** |
| G6 fidelity to the method | **PASS** |

**Overall score: 9.0 / 10.** **No REQUIRED fixes.** Issues 1–6 below are recommended (minor or editorial).

## Round-1 items: are they really fixed?

| item | status now | check |
|---|---|---|
| R08-1 (REQUIRED): log-size floor does not suffice for truth moves | **fixed** | REPORT §6 "sparse eigenvalue floor" row now limits the log-size floor to the (H0) inputs. It says X4.6 needs a residual-variance floor on the large visited models and their one-move enlargements, and records R08's counterexample. I re-derived X4.6: it uses ‖r‖² ≥ λ_min(G^r_U) with \|U\| up to p + 1, i.e. the full-design floor. The new wording is accurate. |
| R08-2: provenance of the Gaussian ξ | fixed | The §6 rows now attribute ξ ~ iid N(0, 1) to isotropic Gaussian idiosyncratic vectors, and the Gaussian-noise uses to X1.1, X5 and X6. Correct. |
| R08-3: Target-2 labelling in §6 | fixed | §6 states the checked class first; FAC-GL and FAC-NCS are labelled unchecked and outside the verdict. |
| R09-1: Ψ row | fixed | "unequal Ψ → unequal loadings, Target 2, outside this theorem" is correct. |
| R09-2: C₀ traceability | fixed in STATEMENT §3 (C₀ := 6C_X, C_X = C_X(ρ)) | The X2 preamble still says constants depend on ρ "and, where stated, on σ, ϑ, s₀". This is harmless, because C_X itself is ρ-only (see issue 5). |
| R09-3: Davidson–Szarek | fixed | X2 D1 and REPORT §6 now name it. |
| R09-4: L4.4 audit table | fixed | X4.5 has the table, and I checked its four rows (G1 below). |
| R09-5, R09-6 | fixed | X2 status line is clean; R09's exact-δ evidence is cited in REPORT §3 and X2. |

## What I re-derived or re-computed

**Algebra (ident.py, sympy; all differences simplify to 0).**
* The swap identity (1+γ_{k−1})[(1−γ_k)²(τ_l+γ_{k−1}τ_j)² − τ_j²] = τ_l² − τ_j² − γ_k(τ_l−τ_j)².
* The addition factor (1+γ_k)(1−γ_{k+1})² = 1−γ_{k+1}, and 1/(1−γ_k) = 1+γ_{k−1}.
* The drift identity x_{T∖j} = x_T − (ξ_j − x_T)/(k−1+κ).
* The X4.1 envelope: the quadratic kℓ² − 2dℓ + 3d stays positive for d ∈ (0, 2], k ≥ 1 (grid minimum 0.03 > 0), so
  |x_T| ≤ 1.5H̄.

**By hand.**
* *X1.1.* Conditional-independence chain e₁ → (η, φ) → e₂ → (ξ, a, u^⊥).
* *X1.2.* Sherman–Morrison and Schur steps.
* *X1.4 (g1)–(g5):*
  * prior ratio (2p−k)/k;
  * (n/(n+1))·Schur for the Q-difference;
  * Q_T ≥ RSS_T/s² and Q_T ≤ RSS_T/s² + 1.1;
  * the M_T normalisation (it reproduces the factor (1+γ_{k−1})(1+ε^d) exactly);
  * the swap size-term cancellation;
  * the ratio M_{T′}ψ_{T′}/(M_Tψ_T) = (1+q_T)²/(1+q_{T′})².
* *Proposition X2 (i)–(v).*
  * The resolvent identity.
  * The D5 decomposition T⁰∖j = ([p]∖j) ∖ (I(a,b)∖j). Both pieces lie in the ξ-measurable family 𝒜_j, and W ⊥ ξ, so
    the conditional union bound is legitimate even though the path set T depends on W.
  * The second-order term r_n²√k(H̄+|x|) ≍ p^{3/2}H̄/n ≤ √(p/n)H̄ needs p ≤ √n, which holds under (P-½).
  * The common part 2ℓr_n‖c‖/‖b‖ ≤ 4r_n(H̄+|x|).
  * The normalisation error C·r_n.
* *Band absorption in Corollary X4.1.*
  3C_XH̄·(17.2e²pϖ + 6 log n + 19)√(log n/n) ≤ ϖ/8 + n^{−1/3}/8 once pH̄√(log n/n) → 0. Together with
  3C_XH̄√(p log n/n) ≤ ϖ/2 this gives |δ| ≤ ¾ϖ and the 2ϖ rule slack.
* *X3.* (iii) in both cases (the bound is on d_i, not on the opposite side), (iv), (vii), (viii) and (ix).
* *X4.*
  * D7 (both μ regimes, including ϖ ≤ n^{−(½−A₁)/2+o(1)}) and D8 (L) separation.
  * Bulk (B1)–(B4): Case A's K⁰ ⊇ K_i decomposition and the J″ ≤ 5m bootstrap; Case B; the wide-phase B1
    contradiction; the B2 recursion, which uses (c2)'s "all gaps ≤ g_max" including the tails.
  * The crude bulk-addition margin: log((k+1)(2p+2)/(2p−k−1)) ≤ log(2p+2), giving (A₁(1+2.2ε_b) − ½) log n.
  * Swaps via G_sw = G_del(j; T) + G_add(l; T∖j).
* *End phase.*
  * Entry through D7/D8; exact structure; no crossing via c(κ′) ≤ c₁.
  * (E-side) margin 2x − 2δ_e ≫ 2ϖ.
  * c_D = ½ − 1/(s₀+1+κ_∞) > 0 (for s₀ = 1 it is (1−ρ)/(2(1+ρ)), consistent with HQ audit B3).
  * At T = S₀, G_add ≤ −½ log n − γ log 2p + O(L_n).
* *X4.6.* rᵀY = β_j‖r‖² + rᵀe; ‖r‖² ≥ λ_min(G^r_U) ≥ (1−ρ)N/2; |rᵀe|/‖r‖ ≤ ‖P_Ue‖ ≤ C√p H̄ (X1.2(a) holds for any U).
  The ridge comparison has error O(n^{−1/2}) for O(n) statistics.
* *X5.2.* I recomputed the population c(U,l) from Σ_CS:
  * Cov(r_l, x_i) = ρ(1−ρ)/(1+(u−1)ρ), and Var(r_l) = (1−ρ)(1+uρ)/(1+(u−1)ρ);
  * this gives (1−ρ)[ϑ_l + ρϑ(S₀∖U)/(1+(u−1)ρ)];
  * the case analysis shows (FS)(a)/(b) are exactly the nonvanishing conditions;
  * the two-sided zero-pair event (≤ 2¹⁹ pairs) and the zero-pair increment ≤ −½log(n+1) + C(20+L_n) both check out.
* *X6.*
  * Every T03♯ hypothesis (s3_posterior.tex:5–13: R, SE_λ(j₀), SE_w(m♯; g₀), BM-∞, p ≤ n^A) follows on 𝒜_n with
    z-free constants. The every-sequence contradiction is sound (1 − π ∈ [0, 1]).
  * [OP] and [M5-0] apply conditionally on Z and are then integrated.
  * Delivery uses 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ plus Markov.

**New adversarial numerics (adv_n0.py; exact iid sufficient statistics and the exact production move rule via
numerics/iid_core.py).** All earlier path numerics (N1X, R09's c3, N5X) start from [p] or the production N₀. But (C2)
is claimed **simultaneously for every 𝔫 with |𝔫| ≤ 15**, so I started from S*(𝔫) for three adversarial 𝔫:
* "near": the 15 nulls closest to x_0;
* "top": the 15 largest |ξ|;
* "toppos": the 15 largest positive ξ, which unbalances the sample and leaves the strongest outside additions.

Configurations: (n, p, ρ, s₀) ∈ {(10⁵, 180, 0.5, 1), (10⁵, 180, 0.1, 2), (10⁶, 400, 0.9, 1), (10⁶, 400, 0.3, 3)}, two
seeds each, 24 runs. I computed the exact δ_j(T) at 20 sampled steps per path.

Results:
* **23/24** runs are pure null deletions of length |S*| − s₀ ending at S₀.
* The rule excess |ξ_{j°} − x_T| − d_T is ≤ 1.59·max|δ|, below the proved 2ϖ (ϖ ≥ (4/3)max|δ|).
* The band overshoot is ≤ 1.59·max|δ|, below 4.3ϖ.
* Truth moves are hugely negative, and swaps stay below the best deletion.
* The one failure is (10⁵, 180, ρ = 0.1, s₀ = 2, "toppos", seed 11). There the first move is a null-out swap that brings
  back an excluded top positive (max addition gain +0.025 log n; swap − best deletion = +0.28).

**Diagnosis (adv_fail.py → adv_fail_out.txt).**
* *What failed.* The first move is a null-out swap: it removes a kept null and re-adds the excluded maximum
  ξ = 3.263. Its gain is 6.205, against 5.923 for the best deletion. Equivalently,
  G_sw = G_del(j; T) + G_add(l; T∖j) with G_add > 0. At T₀ the reference addition value is
  −Δ_{k+1} + ½(1−γ)(ξ_l − x_T)² = +0.082.
* *Why this is not a counterexample.* X4.4's bulk addition bound is
  G_add ≤ log((k+1)(2p+2)/(2p−k−1)) + 2.2ε_b log(2p+2) + O(L_n) − ½ log n. Its margin
  ½ log n − log(2p+2) − O(L_n) is **negative** at this n: ½ log n = 5.76, while log(2p+2) + L_n = 8.34. So the
  proof's own bound does not exclude this move at n = 10⁵; it is a finite-n effect, not a contradiction.
* *Larger n.* With p = 180 and the same ρ, s₀ and adversarial 𝔫, the margin becomes positive and the paths are clean:

  * n = 10⁷: 4/4 seeds pure deletions to S₀. Max addition gain/log n ∈ [−0.31, −0.14]; swap − best deletion
    ≤ −2.2; rule excess ≤ 1.05·max|δ|; band ≤ 1.02·max|δ|.
  * n = 10⁹: 4/4 seeds pure deletions to S₀. Max addition gain/log n ≤ −0.22; swap − best deletion ≤ −4.5;
    excess and band ≤ 0.43·max|δ|.

* *Takeaway.* The uniform-in-𝔫 claim is the place where the crude addition margin binds first. Excluding the
  extreme tail values and then offering them back as additions is the worst case. This is consistent with the
  theorem, but none of the ticket's numerics exercised it (issue 1).

## Gate reasons

**G1 (PASS).** I found no incorrect step. The load-bearing points:
* X1.1 exact independence of ξ and W;
* the ξ-measurable interval family in D5, with the W-dependent band controlled by counts (D6/D7);
* the prefix-only induction (the dependency table is accurate: B1(i) uses B3(i−1), and no step uses a future move);
* X3's d_i-based crossing bound, with the general-|K| constant c(κ′) ≤ c₁ in regime (S) and in the end phase;
* the four reused FACB L4.4 bounds, whose margins are Θ(log n) (or 2x − 2δ_e ≫ 2ϖ) against o(1) perturbations;
* X4.6 under the full-design floor.

The only round-1 G1 failure (REPORT §6) is correctly repaired. The adversarial-𝔫 failure is a finite-n effect inside
the stated asymptotic margin (see the diagnosis).

**G2 (PASS).** Each hypothesis is used where it is stated:
* (CS-R) with Υ_n = I w.l.o.g. (data, scores and partition are invariant).
* (P-½) through A₁ ∈ (limsup, ½), in these places:
  * the second-order term (p ≤ √n);
  * D2 (p² ≤ n);
  * q_T ≤ 1/10;
  * band absorption;
  * D7's c_w;
  * the bulk addition and swap margins (½ − A₁);
  * (B3) Case B's w·count = o(1);
  * T03♯ with A = ½.
* (θ): |β_j| = |ϑ_j| in X4.6, and θ* = D_xβ in X5/X6.
* (FS) only in X5; X4 correctly does not need it.
* s₀ ≥ 1, σ² > 0 and fixed ρ: in the constants (c_D, C_X, c₀).

Nothing stated is unused, and nothing used is unstated.

**G3 (PASS).** Each potential hidden assumption is handled explicitly:
* the random partition and N₀ (uniformity over 𝔫 in X4; conditioning on the raw design Z in X5/X6, with z-free
  constants);
* nondegeneracy (ND_n, a probability-one event inside 𝔊_n);
* ties (every maximiser satisfies (R_ϖ));
* bounded p and p = s₀ (regime (S), empty-max conventions);
* K = p eventually;
* (FS′) explicitly not claimed.

**G4 (PASS).** These statuses match their sources: T38-(0), T03♯, [OP], Lemma CAP (s7_impl.tex:64), Proposition F/A2
(s6_delivery.tex:58) and Lemma CR (CR_corr_tails.md:3). CITECHECK is 5/5 + 8/8 OK. Issue 2 is a verbatim-quotation nit
that does not affect adequacy.

**G5 (PASS).** All of the following are explicit, and n₀ = n₀(ρ, ϑ, σ, s₀, A₁):
* the constants ε_b, K₁, m₁, ε′, T₀, c_w, c₁;
* ϖ_n = 6C_XH̄√(p log n/n) + n^{−1/3};
* the slacks ¾ϖ, 2ϖ, ϖ/10, 4.1ϖ and 4.3ϖ;
* the margins 0.29, 0.35, 0.7(½−A₁), 0.6(½−A₁), c_D and c = min{0.29, c_D/2, 0.6(½−A₁)}.

The absorption criterion is stated as sufficient, not necessary.

**G6 (PASS).** The method matches the specification:
* Score, prior, cap K, standardisation and the production local search (all flips and swaps, best strict
  improvement, lexicographic ties) match SoP 02_method/04_theory. numerics/iid_core.py implements the same forms.
* MR1's LS0 cap ℓ_n + |S̃₀| matches FINAL s7_impl.tex:10,25.
* `git diff 4676af6 HEAD -- Scripts Theory_work/State_of_Project Theory_work/Wave1C/FINAL` is empty, so nothing the
  theorem relies on has drifted since merged main.
* (C4) keeps Proposition F's fallback/allocation premises and their qualifications (X6.4 last sentence).

## Numbered issues (none REQUIRED)

1. **MINOR (evidence) — (C2)'s uniformity over 𝔫 is untested by the ticket's numerics.**
   * *Location:* REPORT §3 (X4 row), X4 header.
   * *Problem:* N1X, R09's c3 and N5X all start from [p] or the production N₀. But (C2) is claimed simultaneously for
     every |𝔫| ≤ 15, and adversarial 𝔫 is exactly where the margin is thinnest (the crude bulk addition bound at T₀
     and T₀∖j). My runs show this: 23/24 adversarial-𝔫 paths are clean, and the single n = 10⁵ failure is fully
     explained by the asymptotic margin ½ log n − log(2p+2) − O(L_n) still being negative at that n. It disappears at
     larger n (diagnosis above).
   * *Fix:* cite reviews/R14_scratch/adv_n0_out.txt and adv_fail_out.txt in REPORT §3. Add one sentence to X4.4: "the
     binding margin of the uniform-in-𝔫 claim is the bulk addition bound, which has margin ½ log n − log(2p+2) −
     O(L_n)". No change to the statement.

2. **MINOR (G4 wording) — STATEMENT §7: "FACB Theorem FAC-CS and lemmas L1–L5: 'PROVED-CHECKED'".**
   * *Problem:* That string is the theorem-level status (W2-FAC-B/REPORT.md:30). The lemma headers read
     "PROVED (by this seat, unchecked); lemma check R0x … VERIFIED-WITH-AMENDMENTS". Also, HQ audit B3
     (HQ_AUDIT/B3_facB_redteam.md: "HOLDS-WITH-AMENDMENTS", F1 wording only) post-dates FAC-B's council and is not
     mentioned.
   * *Why it is minor:* the status is adequate for the use made of it, so G4 still passes.
   * *Fix:* quote "Theorem FAC-CS: PROVED-CHECKED (L1–L5 are its proof; individual headers PROVED (by this seat,
     unchecked) + lemma checks); HQ audit B3: HOLDS-WITH-AMENDMENTS (F1, wording)".

3. **EDITORIAL — propagate B3's F1 qualification.**
   * *Location:* X1.3 header "FACB's one-dimensional scan", the X1.4 Remark "FACB's scan is the case δ ≡ 0", and
     REPORT §2 "FAC-B's one-dimensional statistic".
   * *Problem:* B3 showed that swaps are not ordered by distance to the centre. X1.4 (g5) and X4 correctly use the
     signed-pair quantity V_{jl} throughout, so nothing is wrong. But the "one-dimensional scan" wording invites the
     radial misreading that B3 refuted.
   * *Fix:* write "radial ordering for null deletions/additions; swaps via V_{jl}".

4. **EDITORIAL — X4.1 constant bookkeeping.**
   * *Problem:* The slack lemma derives |τ̂_j| ≤ |τ̂_{j′}| + C_g n^{−1/2}(1 + H̄³n^{−1/2}) and notes that the last
     factor is ≤ 2. But its statement, and Corollary X4.1, use "+ C_g n^{−1/2}" without the factor 2.
   * *Why it is harmless:* the term is absorbed by n^{−1/3}/2 either way.
   * *Fix:* define C_g to include the 2.

5. **EDITORIAL — X2 preamble.**
   * *Problem:* The preamble says constants depend on ρ "and, where stated, on σ, ϑ, s₀". But C_X depends on ρ only:
     Proposition X2 involves only (W, ξ, a, η, φ), D3/D4 and κ, ℓ. Only n₀ depends on (σ, ϑ, s₀, A₁).
   * *Fix:* state this in X2, matching STATEMENT §3 (completes R09-2).

6. **MINOR (W2-UNI framing) — REPORT §6 "growth" row is incomplete.**
   * *Problem:* The row lists only band absorption (X4.1) and crude bulk additions (X4.4). A₁ < ½ (or p ≤ √n) is
     also used in several other places:
     * X2(ii)'s second-order bound (p^{3/2}/n ≤ √(p/n) needs p ≤ √n — itself exactly at the ½ threshold);
     * D2's p² ≤ n union bound;
     * q_T ≤ 1/10 and X4.6's pH̄² = o(n);
     * (B3) Case B's w·#window = o(1);
     * D7's c_w;
     * T03♯ with A = ½.
   * *Why it matters:* §6 is the ingredient list W2-UNI will read. The second-order term is a second, independent
     reason why the present technique stops at ½. It is noted in X2's Remark but missing from §6 and STATEMENT §5.
   * *Fix:* list these uses.

7. **EDITORIAL — REPORT §1 and §4** still say "[pending council]" / "Council: [pending]". Update them on pass.

## Attempts to break the result (none succeeded asymptotically)

* **Path-dependent T in D5.** T depends on W. This is resolved because T⁰(a, b) ranges over a ξ-measurable family,
  T Δ T⁰ ⊆ Band ∪ 𝔫, and the band is controlled only through counts. Correct.
* **Adversarial 𝔫 (new).** Excluding the 15 extreme or 15 central values does not break the path asymptotically. The
  only failure is a finite-n swap/addition, inside the proof's explicit margin (diagnosis above).
* **Crossings under the approximate rule.** These need a hole narrower than c(κ′)ϖ. They are excluded in regime (S)
  and in the end phase by D8, since c(κ′) ≤ 2 + 8/κ_∞ < c₁. In the bulk they are confined to the initial phase,
  which lasts ≤ Q steps.
* **One-sided end-phase configurations.** The sign/separation invariant holds with margin
  ((s₀+κ)H̄ − |B|)/(m+s₀+κ) ≫ δ_e + ϖ.
* **Truth moves on p-size models.** X4.6 holds with the full-design floor, and REPORT §6 now states correctly that a
  log-size floor would not suffice.
* **Start mode with a data-dependent partition.** X5 conditions on Z. The zero pairs are exact (r_lᵀμ = 0). The
  population increments match (FS) exactly by my recomputation.
* **Random design vs T03♯.** Every hypothesis holds on 𝒜_n with z-free constants, and the every-sequence argument is
  valid.

## Score

9.0 / 10. The proof of (C1)–(C4) is complete and correct, with explicit constants, and round 1's blocking item is
genuinely fixed. Deductions are for presentation and evidence only:
* the uniform-in-𝔫 claim is untested in the ticket's own numerics;
* there are small status/wording nits;
* REPORT §6's growth row is incomplete.

None affects a gate.

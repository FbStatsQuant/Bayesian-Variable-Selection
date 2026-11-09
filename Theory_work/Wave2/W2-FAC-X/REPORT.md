# W2-FAC-X — REPORT to Theory HQ (iid rows and general loadings for the one-factor result)

> **Flags (read first).**
> 1. **Scope.** On 2026-11-09 09:22 HQ moved target item 3 (k ≥ 2) to W2-FAC-K2. This ticket covers Target 1 (iid
>    Gaussian rows, compound symmetry, the largest exponent reachable) and Target 2 (general one-factor loadings).
> 2. **Target 1: Theorem FAC-CS-iid is PROVED-CHECKED.** It covers iid Gaussian rows with covariance
>    Υ[(1 − ρ)I + ρ11ᵀ]Υ, with:
>    * fixed ρ ∈ (0, 1);
>    * **limsup log p/log n < 1/2**. That is 3× FAC-A's 1/6. FAC-B's p ≤ n/2 holds for exact Gram only;
>    * fixed s₀ ≥ 1;
>    * fixed raw coefficients satisfying population no-cancellation (FS).
>
>    Claims: (C1) start mode; (C2) path lemma; (C3) reported-model consistency under the joint law; (C4) delivery
>    P(Ŝ⁺ = S₀) → 1. The final council (updated protocol, effort high) passed in round 1: gpt-6-astra 9.2 and Claude
>    Opus 5.5 8.9, all six gates PASS on both seats.
> 3. **Target 2: PARTIAL.** No new proof work was done after take-over (HQ instruction). The result is Theorem FAC-GL:
>    arbitrary loadings in [λ_lo, λ_hi] ⊂ (0, 1), exact Gram and iid rows, log p/log n < A_S = 1/(2(R² + 2R)) with
>    R = ℓ_hi/ℓ_lo. Corollary FAC-NCS covers iid rows with nearly equal loadings, Δ_nH̄_n ≤ n^{−1/3}, log p/log n < ½.
>    Both completed the pipeline through the sweep. Their council has one PASS seat (Sol 9.2); the Claude seat was not
>    completed (interrupted by the pause), so they are **not council-passed**. The exact obstruction is in §5.
> 4. **No method change.** The method is as merged (v3.1, main 4676af6). The MR1 cap ℓ_n + |S̃₀| is used essentially:
>    the start mode is [p] ∖ N₀, and LS0 needs m₀ ≈ p moves (as in FAC-B).
> 5. **The ½ is a limit of this proof, not evidence of a method limit.** N1X: 121/121 paths from [p] are fine up to
>    log p/log n = 0.75. Three things stop the proof at ½ (§6, growth row):
>    * (a) the worst-case band term p·H̄·√(log n/n)·ϖ, absorbed into ϖ;
>    * (b) the second-order resolvent term p^{3/2}/n, which needs p ≤ √n;
>    * (c) (council R20) the uniform-over-𝔫 form of (C2). Beyond ½ it is false as stated: re-adding the largest excluded
>      positive ξ gains ≈ log p − ½log n → +∞.
>
>    Going past ½ therefore needs a band decoupling **and** control of the actual N₀ in place of uniformity over all 𝔫.
> 6. **Framing (HQ, Felipe).** §6 lists every general-assumption ingredient the proofs use, for the design-agnostic
>    main theorem (W2-UNI).
> 7. **Successor lead.** The original lead was stopped mid-pipeline by the HQ pause (2026-11-09). This report was
>    finalised by a successor lead (Claude Opus 5.5, high) on the same day. LOG.md records the hand-over.
> 8. All results are asymptotic (scope rule).

## 1. RESULT

* **Target 1 — PROVED-CHECKED** (Theorem FAC-CS-iid, STATEMENT.md v3 locked, proofs lemmas/X1–X6). Pipeline:
  * statement lock: R01 REJECT → R02 LOCK-WITH-CHANGES → v3 locked;
  * every lemma checked cross-family (R03, R03b, R04, R05);
  * independent mid-point R06: **CONTINUE**;
  * exhaustive sweep R07: 0 FATAL / 0 MAJOR / 3 MINOR / 9 EDITORIAL, all fixed;
  * **final council (updated protocol) round 1: PASS.** R19 gpt-6-astra (high) 9.2, R20 Claude Opus 5.5 (high,
    claude-personal) 8.9, all six gates PASS on both, no REQUIRED items. Earlier rounds under the previous protocol are
    in §4.
* **Target 2 — PARTIAL** (§5).

## 2. The statement (STATEMENT.md v3, locked; proofs lemmas/X1–X6)

**Setting (model R).**
* Rows of X^r are iid N_p(m, Σ_n). The noise ε ~ N(0, σ²I) is independent of X^r.
* The method's centring/standardisation: X = CX^rD_x⁻¹, θ* = D_xβ.
* Covariance: Σ_n = Υ_n[(1 − ρ)I + ρ11ᵀ]Υ_n.

**Hypotheses.**
* (P-½): limsup log p/log n < 1/2.
* (θ): s₀ ≥ 1 is fixed. The sign-corrected raw coefficients form a fixed nonzero vector ϑ; positions are arbitrary.
* (FS): population no-cancellation (FAC-B's condition).

**Theorem FAC-CS-iid.**
* **(C1)** S* = [p] ∖ N₀ is the unique maximiser of γ₀. Here N₀ is the set of nulls in the realised block that
  contains S₀, with |N₀| ≤ 15.
* **(C2)** Take one event of probability → 1. On it, simultaneously for every set 𝔫 of ≤ 15 nulls, the uncapped LS0
  search from [p] ∖ 𝔫 makes only null deletions. Each deletion is a ϖ_n-approximate argmin of |ξ_j − x_T|, with
  ϖ_n = 6C_X H̄√(p log n/n) + n^{−1/3}. Along the path:
  * every addition has gain ≤ −c log n;
  * swaps fall below the chosen deletion;
  * truth moves are negative;
  * deleted nulls lie inside (a_T − 4.3ϖ_n, b_T + 4.3ϖ_n);
  * the search ends after exactly m₀ moves at S₀, a strict local maximum.

  Consequently, LS0 with the MR1 cap scores and certifies S₀; the legacy cap misses it when m₀ ≥ ℓ_n + 2.
* **(C3)** Under the joint law: D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n).
* **(C4)** Assume Proposition F's premises and allocation, with total tier-1 fallback (CAL-free). Then
  P(no output) = 0 and P(Ŝ⁺ = S₀) → 1.

**Mechanism.**
* **(X1) Exact rotation in 1^⊥.** The axes are the noise direction and the factor direction. The noise coordinates
  ξ_j = u_jᵀe/‖e‖ are iid N(0, 1) and **exactly independent** of the idiosyncratic Wishart matrix W ~ W_p(n − 3, I).
  * RSS_T = ‖e‖²/(1 + q_T).
  * Replacing W by (n − 3)I gives FAC-B's reference statistic ξ_j − x_T with the exact drift identity. Null
    deletions/additions are ordered radially; swaps are compared via V_{jl} (HQ audit B3, F1).
  * The ridge, determinant and Q-versus-RSS corrections are bounded in absolute terms.
* **(X2) Resolvent expansion.** δ_j(T) = −(Rc)_j + …, with R = W_T/N − I. On band-structured sets the first-order sum is
  bounded by:
  * Gaussian conditioning over ξ-defined intervals, using W ⊥ ξ;
  * crude bounds on the band and on N₀.
* **(X3) Deterministic soft gap.** ϖ-approximate argmin deletions keep the hole an interval up to a 4.3ϖ band, as
  follows:
  * crossings happen only while the hole is narrower than 4ϖ;
  * under a density hypothesis that phase lasts ≤ Q steps.
* **(X4) Induction on established prefixes.** One step:
  * band structure;
  * perturbation bound (band count fed back);
  * approximate rule;
  * FAC-B's bulk Claim B and end phase, with τ̂ = τ + δ.

  Truth moves use a residual-variance floor on large models (X4.6).
* **(X5)** Start mode, conditionally on the raw design.
* **(X6)** Every-sequence de-randomisation for T03♯, [OP] and [M5-0], given the raw design and then integrated.
  Delivery follows FAC-B L5.4 / A2.

## 3. Status per clause

| clause | content | evidence |
|---|---|---|
| X1 | representation, reference statistic, gains (g1)–(g5) | R03 Sol high V-W-A (minor, applied). iid_selftest_out.txt. Identities recomputed independently by R19 (R19_scratch/check_output.json: Schur 4.4e−16, swap 2.7e−15) and R20 (R20_scratch/r20_checks_out.txt: swap identity 4e−14, reference identity 1e−16). |
| X2 | event 𝔈_n, Proposition X2 | R03 V-W-A (4 minor, applied). R20's exact δ along 20 paths: max\|δ\|/(H̄√(p log n/n)) ∈ [0.16, 0.28], flat in p and n (R20_scratch/r20_checks_out.txt). |
| X3 | deterministic soft gap | R03 FAILED (iii) as written (MAJOR, counterexamples). Repaired, then fresh re-check R03b V-W-A. N3X: 0 violations in 480 runs. R19: 400 approximate-deletion paths, 223 crossings, 9282 containment checks, 0 failures. |
| X4 / (C2) | key path lemma | R04 Sol xhigh V-W-A, no FATAL/MAJOR. N1X 121/121. R09_scratch/c3_out.txt: ρ ∈ {0.02, 0.05, 0.95}, 16/16. R20: 20/20 pure deletions to S₀, rule slack and band ≤ 1.59·max\|δ\|. Adversarial 𝔫 (R14_scratch/adv_n0_out.txt, adv_fail_out.txt): 23/24 clean at n ≤ 10⁶. The one failure, at n = 10⁵, is where the bulk-addition margin ½log n − log(2p + 2) − O(L_n) is still negative; it disappears at n ∈ {10⁷, 10⁹} (8/8). |
| X5 / (C1) | start mode | R05 V-W-A (2 MAJOR: raw-design conditioning, two-sided zero-pair event; applied). N5X 48/48. |
| X6 / (C3), (C4) | assembly, delivery | R05 V-W-A (applied) |
| programme | mid-point | R06 fresh Sol **CONTINUE** (3 minor, applied) |
| whole proof | sweep | R07 Sol 0/0/3/9, all fixed |
| deliverable | council | **PASS**: R19 astra 9.2 + R20 Opus 8.9, all gates (§4) |

**Inputs (statuses verbatim, checked in reviews/CITECHECK_FINAL.txt):**
* T38-(0): "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))".
* T03♯: "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)".
* [OP]: "PROVED (by this seat, unchecked)", inside Theorem GEN "PROVED-CHECKED".
* Lemma CAP: "PROVED (by this seat)", council-checked.
* Proposition F (A1 corrected statement) and F-GROW: "PROVED (A2), checked by A3".
* Lemma CR: "PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)". This is an upstream review id, not this
  ticket's R19.
* FAC-B Theorem FAC-CS: "PROVED-CHECKED". Its lemma headers read "PROVED (by this seat, unchecked)" plus checks. HQ
  audit B3: "HOLDS-WITH-AMENDMENTS" (F1, wording).
* FAC-A Theorem FAC-L: "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)". Only the L5.1
  de-randomisation pattern is used.

## 4. Review trail

* **Statement lock.**
  * R01 (Sol high): REJECT, 6 changes.
  * R02 (fresh Sol high): LOCK-WITH-CHANGES, 5 changes.
  * Result: v3 locked.
* **Lemma checks.** R03 (Sol high: X1–X3); R03b (X3 re-check); R04 (Sol xhigh: X4); R05 (Sol high: X5–X6).
* **Mid-point.** R06 (Sol xhigh): CONTINUE.
* **Sweep.** R07 (Sol xhigh): 0/0/3/9, all fixed.
* **Council rounds.**
  * **Previous protocol (Sol xhigh + Opus high):**
    * Round 1: R08 Sol 8.8, G1 FAIL. The failure was a REPORT §6 overstatement: log-size eigenvalue floors do not
      suffice for truth moves. R09 Opus 9.0, all PASS. Not passed; fixed (R08_R09_disposition.md).
    * Round 2: R13 Sol 9.2, all PASS. R14 Opus 9.0, all PASS. Both ≥ 8 with all gates PASS. R14 was returned but not
      dispositioned before the pause. Recommendations applied by the successor (R13_R14_disposition.md).
  * **Final council under the updated protocol** (effort cap high; HQ take-over brief; fresh, independent seats, not
    shown earlier council seats; brief COUNCIL_BRIEF_FINAL.md), round 1:
    * **R19 gpt-6-astra (high): 9.2, all PASS.**
    * **R20 Claude Opus 5.5 (high, claude-personal): 8.9, all PASS.**
    * Result: **PASS**. Non-blocking items applied (R19_R20_disposition.md); no claim changed.
* **Reviewer families.** Codex gpt-6.1-sol: R01–R08, R10–R13, R15–R17. gpt-6-astra: R19. Claude Opus 5.5: R09, R14,
  R20 (and the unfinished T2 seat R18). Every reply is saved verbatim in reviews/, each with its disposition file.
* **Citation check.** reviews/CITECHECK_FINAL.txt: 7/7 path:line citations, 11/11 verbatim status strings, every review
  and numerics file named in this REPORT present (7/7). The earlier CITECHECK.txt is kept for the trail.

## 5. Target 2 (general one-factor loadings) — PARTIAL

The statement is STATEMENT_T2.md v2.1, locked (R10 LOCK-WITH-CHANGES; v2.1 is a flagged narrowing per R12). The
loadings are λ_j ∈ [λ_lo, λ_hi] ⊂ (0, 1) and may depend on n. Define:
* ℓ_j = λ_j/√(1 − λ_j²);
* R = ℓ_hi/ℓ_lo;
* A_S = 1/(2(R² + 2R)). This equals 1/6 at compound symmetry and ≈ 0.002 for λ ∈ {0.2, 0.95}.

**What is proved and how far it is checked.**

| result | content | status / evidence |
|---|---|---|
| Theorem FAC-GL (G) exact Gram and (R) iid rows | (G1) start mode; (G2) **uniform over all T ⊇ S₀** (best move a null deletion with gain ≥ c log n, additions ≤ −c log n, swaps below, truth moves negative, S₀ strict local max), hence a pure null-deletion path from any start between S₀ and [p]. Under (G), within one loading value each deletion is the exact argmin of \|ξ_j − ℓ_jX_T\|. (G3) consistency; (G4) delivery. Hypotheses: (1F), (θ), (FS-G), log p/log n < A_S. | Proofs T2/L4r_path.md §L4r.0–3, lemmas X8, X9, X10, each "PROVED (by this seat, unchecked)". Checks: R11 Sol xhigh (L4r.0–3 **VERIFIED**; X9 V-W-A, applied); R12 (X8 **VERIFIED**; X10 **VERIFIED**, conditional on its path inputs). Mid-point R15 **CONTINUE**. Sweep R16 0/0/1/4, fixed. Council round 1: **R17 Sol xhigh 9.2, all PASS**; Claude seat R18 **not completed** (pause), so not council-passed. Numerics: N2X 64/64; T2/numerics 366/366 exact-Gram paths (1–3 loading classes, λ from 0.1 to 0.98, log p/log n ≤ 0.87). |
| Corollary FAC-NCS ((R) only) | nearly equal loadings Δ_nH̄_n ≤ n^{−1/3}, log p/log n < ½, (FS) at ρ = λ̄²: (C1)–(C4) with ϖ′_n = (1 + C₇)ϖ_n | lemmas/X7 "PROVED (by this seat, unchecked)". R12: (R) V-W-A. R12 found the (G) branch FAILED (an iid multiplier bound that is false for exact Gram), so the corollary was narrowed to (R). Same R15/R16/R17 trail; not council-passed. |
| L4r.4, L4r.5 | per-class gap invariant (deterministic); static per-class centre bound under per-class two-sidedness | PROVED (by this seat, unchecked); not reviewed; not used by FAC-GL |

**Exact obstruction (the region between FAC-GL/FAC-NCS and the full FAC-B-type range is open).**
1. **Uncovered region.** Fixed loading dispersion with A_S ≤ limsup log p/log n < ½ is not covered, and neither is
   dispersion between n^{−1/3}/H̄_n and fixed when log p/log n ≥ A_S.
2. **The uniform-over-sets route stops at A_S.** FAC-GL bounds additions on *every* T ⊇ S₀. On sets the path never
   visits (S₀ plus same-sign, low-loading nulls), additions have positive gains beyond A_S at finite n:
   * CS at log p/log n = 0.33: +0.083 log n;
   * λ ∈ {0.2, 0.95} at 0.155: +0.115 log n.

   Evidence: T2/numerics/adversarial_T_out.txt. A two-class heuristic suggests the addition threshold is sharp for
   worst-case sets, but this is not established, and no asymptotic necessity is claimed. Any proof beyond A_S must use
   the path.
3. **The path route (FAC-B's L4 per loading class) fails at three named steps.** Source: T2/L4r_path.md §L4r.6 and
   T2/NOTES.md §2, with numerics in T2/numerics/end_phase_detail_out.txt and N_T2_summary.md.
   * **(B2):** with ≥ 2 classes, a deletion in class c′ moves class c's centre by ℓ_cℓ_{c′}τ/(D′ − ℓ′²_{c′}) without
     touching class c's hole. The hole asymmetry Δ_c then accumulates (Δ_c ≲ 2ℓ_c·TV(X)). Numerically,
     max Δ_c/(2ℓ_c) = 0.70H̄, against max |X_T| = 0.074H̄ in the bulk.
   * **(B1):** classes become one-sided during the bulk (up to 30 steps with m ≥ 30), so the per-class centre bound's
     hypothesis is false on actual paths.
   * **(E-side):** in the end phase the smallest-loading class is deleted first on either side, and minority-side
     deletions occur (13/160 end-phase steps; never under CS). There is no centre-ratio invariant
     (max_c ℓ_c|X_T|/H̄ up to 1.75; T2/numerics/run_t2_stress_log.txt).
   * The variable centres ℓ_jX_T are the root cause: they add (ℓ_j − ℓ̄)X_T to the statistic, a band of width
     ≍ Δℓ·|X_T|, which the Target-1 balance argument cannot absorb for fixed dispersion.
4. **(FS-G) is restrictive for continuous loadings.** W2-SIM (Theory_work/Wave2/W2-SIM/results/X/Q2_visibility.md,
   population computation) finds that the non-masking constant is small but n-free for CS (with the study's
   coefficients, except the FS-failing ρ = ½) and for two-class loadings. For loadings uniform on [0.2, 0.9] it → 0
   generically: a truth's partial covariance changes sign over the attainable conditioning sets. So FAC-GL as stated
   applies mainly to finitely many loading classes. Route, not carried out: (G2) holds from **any** start ⊇ S₀, so (G1)
   can be weakened to sure screening of the start mode.
5. **Nothing falsifies the full Target-2 path claim.** All 430 simulated paths (N2X 64, T2 366) are pure null deletions
   to S₀. The gap is in the proof technique.

## 6. General-assumption ingredients used (for W2-UNI; HQ framing note)

Checked population class: Σ_n = Υ[(1 − ρ)I + ρ11ᵀ]Υ (Theorem FAC-CS-iid, PROVED-CHECKED). The rows below are what its
proof uses. The last table gives the different profile of the uniform-over-sets route (FAC-GL, not council-passed).

| ingredient | where used | general form it needs |
|---|---|---|
| iid **Gaussian** rows | X1: exact rotation; ξ ⊥ W. The ξ_j are iid N(0, 1) because the idiosyncratic vectors are isotropic Gaussian, so their projections on any independent direction are iid standard normal; this gives the sign symmetry used in E5 / B3. X2: Wishart concentration, conditional Gaussian row sums. X5/X6: Lemma CR, de-randomisation. | Gaussian rows; rotation invariance of the idiosyncratic part |
| **one factor, equal loadings** (compound symmetry) | X1.3: single common centre and exact drift identity → X3 (deterministic gap) and X4 (FAC-B's balance and end-phase dynamics) | the CS-specific step; general loadings need loading-specific centres ℓ_jX_T (§5) |
| idiosyncratic Ψ ∝ I | X1: whitened Gram = ṽ1ṽ1ᵀ + ṽ2ṽ2ᵀ + W with W ~ W_p(N, I) | Unequal diagonal Ψ becomes **unequal loadings** ℓ_j = λ_j/√ψ_j after whitening, i.e. Target 2 (§5), outside this theorem. Block-local Ψ is not covered: the identity-plus-rank-one reference and the iid-coordinate argument do not cover it (R19 item 1) |
| eigenvalue floor | λ_min(R̂) ≥ c₀ on the **full** matrix (Davidson–Szarek, p ≤ n^{1/2}, X2 D1). Used for the ridge bounds (X1.4), truth moves (X4.6) and (H0) (X6.1). | W2-UNI's (A1) floor on log-size sets suffices **only** for the posterior (H0) inputs. X4.6 needs a **residual-variance floor for a truth after conditioning on the large models the path visits** (sets of size ≈ p and their one-move enlargements). A log-size floor alone does not suffice (R08 item 1). Counterexample: orthonormal nulls u₁…u_m with m ≫ log n and truth x₀ = Σu_l/√m. All log-size floors → 1, but x₀ has zero residual on the nulls, and the shipped score's truth deletion gains (1 − b²/σ²)/(4n) > 0 for \|b\| < σ. |
| beta-min + non-masking | fixed nonzero ϑ (BM-∞, TL); (FS): population partial covariances nonzero for block-local conditioning sets (start mode only, X5; X4 does not use it) | W2-UNI's (A3); (FS) is exactly a block-local non-masking condition |
| growth | p ≤ n^{A₁} with A₁ < ½. Used in: band absorption pH̄√(log n/n) → 0 (X4.1); X2(ii)'s second-order term p^{3/2}/n ≤ √(p/n), which needs p ≤ √n; D2's p² ≤ n union bound; q_T ≤ 1/10; X4.6's pH̄² = o(n); (B3) Case B's w·#window = o(1); D7's c_w; the bulk addition and swap margins (½ − A₁)log n (X4.4), which carry the uniform-in-𝔫 claim; T03♯ with A = ½ (X6). | Three independent reasons the present technique stops at ½: (a) the band term; (b) the second-order resolvent term; (c) the uniform-in-𝔫 bulk addition margin ½log n − log(2p). Beyond ½, (c) makes the uniform form of (C2)(ii) false (R20 item 1; R20_scratch/r20_addmargin_out.txt). Beyond ½ one must control the realised N₀ directly. |
| Gaussian noise | X1.1: ‖e‖²/σ² ~ χ²_{n−1}, with direction e₁ uniform and independent of ‖e‖. X5: conditional Gaussian zero-pair and noise-projection bounds. X6: fixed-design posterior inputs T03♯, M5-0. | — |
| method | MR1 cap ℓ_n + \|S̃₀\| (LS0 needs m₀ ≈ p moves); complete flip/swap scans; strict improvement; tie rule | as merged (4676af6); no change |

**Profile of the uniform-over-sets route** (FAC-GL; T2/L4r_path.md, lemmas X8–X10; not council-passed). It needs fewer
structural ingredients but reaches a smaller exponent:
* No common centre, no band or path induction, no compound symmetry, no finite loading alphabet.
* Uses rank-one factor plus diagonal Ψ with ψ_j ≥ ψ_lo (so λ_min(Σ) ≥ ψ_lo).
* Uses a full-Gram eigenvalue floor and a uniform projection bound ‖P_Ue‖ ≤ C√p H̄ (truth moves).
* Uses one deletion identity Σ_K ℓ′_iτ_i = κ′_SX_T + ϱ and a top-square centre bound.
* Uses Gaussian rows (X9 transfer: |δ| ≤ C(p/√n + √(p log n/n) + √(log n/n))H̄), (FS-G) and log p/log n < A_S.

For W2-UNI this is the ingredient set of a "no path structure" argument; its exponent is limited by the worst-case
addition margin over all T.

## 7. Open items and recommended next steps

1. **Target 2 council.** Run one Claude seat (Fable 5.2 or Opus 5.5, high) on FAC-GL and FAC-NCS. Sol's seat R17
   (9.2, all PASS) is on file. With the protocol update, a fresh astra + Claude pair may be needed. This is the
   cheapest way to move FAC-GL from PARTIAL-checked to PROVED-CHECKED. No new proof work is required.
2. **(FS-G) for continuous loadings** (§5 item 4). Replace (G1) uniqueness by sure screening of the start mode, which
   is all (G2) needs.
3. **Target 2 beyond A_S.** Use a single weighted potential in place of FAC-B's per-class B1–B3 (T2/NOTES.md §4):
   X_T is the ridge slope of the kept ξ on their loadings. The end phase becomes a finite-state analysis of signed
   per-class counts, with the addition statistic as the invariant.
4. **Target 1 beyond ½.** Needs both (a) a leave-one-out decoupling of band membership from W_{j·} and the
   second-order term, and (b) replacing uniformity over 𝔫 by direct control of the realised N₀ (§6 growth row).
   W2-SIM item A (numerics/SIM_REQUEST.md) is testing A ∈ [0.5, 0.9]. Its batch was submitted on NOTS at 10:40 and had
   no results in W2-SIM/results/X/ at the time of this report. W2-SIM's pilot at n = 10⁴, p = 1000 (log p/log n =
   0.75) found a non-[p] start mode (565/1000) and a path with 2 null swaps that still ended at S₀ (W2-SIM/LOG.md;
   finite-n, outside (P-½)).
5. Exact-Gram near-CS with p ≤ n/2 (X7 remark 1): FAC-B's finer bulk analysis with ϖ-perturbations.

## 8. Files (Theory_work/Wave2/W2-FAC-X/)

* **Statements and logs:** STATEMENT.md (v3 locked; §5/§7 annotated post-council, no claim changed), STATEMENT_T2.md
  (v2.1 locked), PLAN.md, LOG.md, CHECKPOINT.md, REPORT.md.
* **lemmas/:** X1_representation.md, X2_perturbation.md, X3_softgap.md, X4_path.md, X5_start.md, X6_assembly.md
  (Target 1); X7_near_cs_loadings.md, X8_start_general.md, X9_iid_general.md, X10_assembly_T2.md (Target 2).
* **T2/:** STATEMENT_T2.md, L4r_path.md, NOTES.md, numerics/ (eg_core.py, run_t2.py, adversarial_T.py,
  end_phase_detail.py, outputs, N_T2_summary.md).
* **reviews/:** R01–R20 verbatim, with dispositions R01–R07, R08_R09, R10–R12, R13_R14, R15, R16, R19_R20.
  * Not reached: a Claude T2 seat. R18_scratch holds scripts only; no review file.
  * Council briefs: COUNCIL_BRIEF.md, COUNCIL_BRIEF_T2.md, COUNCIL_BRIEF_FINAL.md.
  * Citation checks: citecheck.py → CITECHECK.txt; citecheck_final.py → CITECHECK_FINAL.txt.
  * Reviewer scratch: R09_scratch, R11_scratch, R14_scratch, R19_scratch, R20_scratch.
* **numerics/:** iid_core.py (exact iid-row sufficient statistics and the exact production LS0 path),
  iid_selftest(.py/_out.txt), n1x_iid_cs.py → N1X_raw.jsonl, N1X_summary.md; n2x_loadings.py → N2X_raw.jsonl,
  N2X_summary.md; n3x_softgap.py → N3X_out.txt; n5x_start.py → N5X_out.txt; SIM_REQUEST.md; copies of FAC-B's
  bvs_core.py, fac_core.py, cs_core.py, cs_gain.py.

No files outside this folder were modified, and no git state was changed.

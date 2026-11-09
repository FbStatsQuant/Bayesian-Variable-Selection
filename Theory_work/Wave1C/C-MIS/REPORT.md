# C-MIS — REPORT to Theory HQ

> **Flags (read first).**
> 1. **Scope vs Song–Liang.** SL's Corollary 2 is *support inclusion* (π(s̃ ⊂ ξ) → 1) and their Theorem 4 is *density*
>    consistency, for a fixed-size candidate set. Our main theorem gives *exact-model* concentration π(S₀^𝒞) → 1 at rate
>    √(log n/n), with p_𝒞 ≤ n^A, but under *stronger* hypotheses: a Gaussian-residual condition (GR) on the omitted part,
>    fixed effective variance, fixed projected sparsity s₀^𝒞 ≥ 1, and T03♯'s eigenvalue and beta-min conditions on the
>    projected truth. No density-contraction analog is claimed. β^𝒞 equals SL's β₀ for **centred** jointly Gaussian
>    rows; otherwise it is the analogue adjusted for the intercept.
> 2. **Main theorem = transfer.** Theorem MIS is an exact reduction to T03♯: under GR the candidate-only problem *is*
>    a well-specified model. The new technical content is Lemma DR, which handles random designs, and the
>    fixed-design Theorem F with Lemma T.
> 3. **Statement edits after lock** (all logged, none weakens a locked claim): v1.1 → v1.2 adds Lemma T / Corollary F(b),
>    Lemma Z (null projection), Examples E1–E3 and Corollary N; it also qualifies the SL identification by centring and
>    renames the omitted set 𝓜.
> 4. **Corollary D (reported HPM) inherits GEN's premises**: v3.1 + LS0 *as specified* (LS0 is not in production code),
>    e4 (N3 "OPEN" as a general invariant), GUARD-W/OP-LS0, and BM-∞. There is no delivery claim.
> 5. Everything is asymptotic. Thresholds depend on the stated constants. TH09's ≈ 2·10⁶ illustration is not
>    transferred. No method requirement for C-ENG.

## 1. RESULT

**PROVED-CHECKED.** This is the narrowed form in §2: Theorem MIS (i)–(iii) with Proposition P, Lemma DR and Lemma
GD(a)/(b); Corollaries H, D and D′; Theorem F with Corollaries F(a) and F(b) and Lemma T; Lemma Z; Corollary N; and
Examples E1–E3. Lemmas O1 and O2 are frontier statements about the proof technique.

The evidence chain was: statement lock R01; lemma checks R02, R03 and R05; mid-point R04 **CONTINUE**; exhaustive sweep
R06 with 0 fatal findings, all fixed; and council round 1 **PASSED**, with Sol 9.2 and Opus 9.0 and all six gates
passing for both seats in the same round.

## 2. The statement as proved (STATEMENT.md v1.2; proof map lemmas/00_MAIN.md)

Notation: candidate set 𝒞 with |𝒞| = p_𝒞 ≤ n^A. The method is **re-run on the candidate data** (X^r_𝒞, y^r) with the
shipped prior and score: g = n ridge, IG(0.01, 0.01) with the response-dependent rate, BB(1, p_𝒞) and cap K.

The true model is y = α + X_𝒞β_𝒞 + ω + ε, where ω = X_𝓜β_𝓜 is the omitted contribution.

**(GR)** Given X_𝒞, ω = a + X_𝒞γ + ξ, with ξ ~ N(0, τ²I) independent of ε and τ² fixed.

The best approximating model is **S₀^𝒞 := supp(β_𝒞 + γ)**, with σ_𝒞² := σ² + τ².

* **Theorem MIS (i)** (fixed candidate design). Under GR and the T03♯ hypotheses for (X_𝒞, β^𝒞, σ_𝒞²):
  - 1 − π_𝒞(S₀^𝒞 | y) = O_P(√(log n/n)).
  - The PIP, MPM and exact-HPM consequences hold.
  - Without beta-min, inclusion holds for the large projected signals.
  - Proxies (candidates that are null in the full model but have γ_j ≠ 0) get PIP → 1.
  - Cancelled true candidates (β_j + γ_j = 0) get PIP → 0.
  - The beta-min condition is relative to σ_𝒞² (dilution).
* **Corollary N.** Every T ≠ S₀^𝒞 has π(T) ≤ 1 − π(S₀^𝒞). So the retained truth S₀ ∩ 𝒞 and the dense sample-projection
  support (dense when τ² > 0) both lose all posterior mass whenever they differ from S₀^𝒞.
* **Theorem MIS (ii)/(ii′)** (random candidate design). The same conclusions hold under the joint law, assuming
  finite-n envelopes with fixed constants on design events of probability → 1. The proof uses the diagonal
  uniform-tightness argument of Lemma DR.
* **Theorem MIS (iii) / Proposition P** (jointly Gaussian rows, 𝓜 := active omitted set):
  - At each n, γ = Σ_𝒞𝒞⁻¹Σ_𝒞𝓜β_𝓜 = −Θ_𝒞𝓜Θ_𝓜𝓜⁻¹β_𝓜, where Θ is the precision of the *marginal* vector
    (x_𝒞, x_𝓜), and τ² = β_𝓜ᵀΘ_𝓜𝓜⁻¹β_𝓜.
  - For one active omitted variable k, a candidate that is null in the full model is a proxy **iff Θ_jk ≠ 0**, i.e.
    iff it has nonzero partial correlation with x_k. Marginal correlation does not matter. Examples: an AR(1) design
    gives the two neighbours; a one-factor design can make s₀^𝒞 grow, which falls outside the theorem.
  - GR in the theorem's sense additionally needs τ_n² ≡ τ².
  - Lemma GD(a): for fixed p_𝒞 (SL's regime) all hypotheses hold with probability → 1. This recovers SL's Corollary 2
    conclusion in the jointly Gaussian special case, now with a rate.
  - Lemma GD(b) (optional): growing p_𝒞 under stated population restricted-eigenvalue, variance, energy and projected
    beta-min assumptions. Projection sparsity is assumed, not inferred.
* **Corollary H.** At every n and for any feasible T:
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀^𝒞}) ≤ 2E[1 − π_𝒞(S₀^𝒞 | y)] + D_n^𝒞.
* **Corollary D.** Under GR, D_n^𝒞 → 0 on the GEN class (σ² := σ_𝒞² throughout GEN). Therefore
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀^𝒞}) → 0 and liminf P(𝒪 ∩ {Ŝ⁺ = S₀^𝒞}) = 1 − limsup P(U_n).
  - **Instance D′** (GEN's W family): the omitted variable is a noisy copy of a candidate j₂ that is null in the full
    model. The reported HPM contains the proxy j₂ in place of the omitted k.
* **Theorem F** (fixed design, exact sparse projection EP: r := μ − X_𝒞θ^𝒞 is orthogonal to every candidate).
  - Statement: T03♯'s conclusions hold for S₀^𝒞 = supp θ^𝒞, with beta-min relative to σ²_{𝒞,n} = σ² + ‖r‖²/N, given
    the tail hypothesis TAIL^𝒞 at a cutoff m_n = O(log n).
  - Every changed step is written out: the new event (G5); δ_n^𝒞 propagated through (C4), (C5) and (C8); E_n^𝒞 with
    σ²_{𝒞,n}; the signal computed with μ^𝒞; and (P_{S′} − P_S)r = 0.
  - **Corollary F(a):** bounded p_𝒞 ⇒ TAIL^𝒞 holds automatically.
  - **Lemma T / Corollary F(b) (new):** for growing p_𝒞, TAIL^𝒞 holds under
    (TL) σ²/(Δ_n + σ²(1 − rank/N)) ≤ ¾(1 − κ), i.e. roughly Δ_n ≳ σ²/3. The proof needs no eigenvalue condition beyond
    S₀^𝒞.
* **Lemma Z** (null projection, s₀^𝒞 = 0, bounded p_𝒞, under GR or EP): 1 − π(∅) = O_P(n^{−1/2}).
* **Boundary examples.**
  - E1 (analytic): candidate 1 is cancelled, candidate 2 is a proxy, and the sample-projection support is dense.
  - E2: a common random omitted slope with Gaussian marginals defeats the transfer, so GR's covariance content matters.
  - E3: EP cannot be dropped for a pre-named target.

**Change vs the brief.** The brief's target (a Song–Liang Thm 4-type theorem with p ≤ n^A) is met in fixed-design and
random-design forms under GR, together with the HPM statement via M5(0) and D_n^𝒞 → 0 on the GEN class with an explicit
instance.

The brief's suggested *fixed-design* definition, "projection up to a beta-min margin, with the omitted signal acting as
extra noise σ² + ‖(I − P_𝒞)Xβ‖²/n", is proved only for exact projection (Theorem F). The size tail is discharged only for
bounded p_𝒞 or under (TL).

## 3. Status per clause (cited statuses verbatim, nothing upgraded)

| Clause | Evidence |
|---|---|
| Lemma R, MIS (i), Lemma DR, Cor H, Cor D | R02 VERIFIED; council R07/R08 PASS |
| MIS (ii)/(ii′), GD(b), D′ | R02 VERIFIED-WITH-AMENDMENTS (applied); council PASS |
| Prop P, GD(a) | R02 VERIFIED; R04 wording fixes checked in R05; council PASS |
| Theorem F (changed steps), Cor F(a), Lemma T, Cor F(b), cutoff remark | R03 (xhigh) VERIFIED / V-W-A (applied); pathwise inequalities corroborated by `numerics/check_L4.py` (no violation); council PASS |
| Lemma Z, E1, E2, E3, Cor N | R05 VERIFIED / V-W-A (applied); council PASS |
| Lemma O1, O2 (frontier) | R03 V-W-A. O2's original consequence paragraph was GAP/FALSE and has been replaced: it is now only an obstruction to T02(i♯)'s denominator strategy. Council PASS |
| Inputs | T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; T01–T03 "PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY"; T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; Theorem GEN "PROVED-CHECKED" (Wave 1) with its premises |

Numerics (`numerics/SUMMARY.md`): exact enumeration with p_𝒞 ≤ 10, 20 seeds and n ≤ 6400, runs N1–N7 and N3b, plus
check_L4. No contradiction was found.

- N1: π(S₀^𝒞) → 0.956; π(S₀ ∩ 𝒞) → 0; the sample projection has 10/10 nonzero coefficients.
- N2: the neighbour rule holds — a marginally correlated non-neighbour has PIP → 0.005.
- N3 vs N3b: the dilution scale is σ²_𝒞.
- N4: cancellation works as predicted.
- N6: π(∅) → 0.989.
- N7: Example E1 gives π({x₂}) → 0.983.

## 4. Review trail

* Statement lock R01 (Sol high): LOCK-WITH-CHANGES, 7 required changes, all applied.
* Lemma checks:
  - R02 (L1–L3, Sol high): VERIFIED-WITH-AMENDMENTS.
  - R03 (L4–L5, Sol xhigh): VERIFIED-WITH-AMENDMENTS; one frontier paragraph GAP/FALSE, replaced.
  - R05 (Lemma Z and examples, Sol high): VERIFIED-WITH-AMENDMENTS.
* Mid-point R04 (fresh Sol xhigh): **CONTINUE**, with 2 major findings (statement wording of the Gaussian-design part)
  and 7 minor ones, all addressed.
* Exhaustive sweep R06 (Sol high): 0 fatal, 3 major, 7 minor, 5 editorial; all fixed.
* Council round 1: **R07 Sol (xhigh) 9.2, R08 Opus (high) 9.0; all six gates PASS for both → PASSED.** The 11 minor
  post-round fixes are listed in `reviews/R07_R08_disposition.md`.
* CITECHECK: `reviews/CITECHECK.txt`, ALL OK (34 locators).
* Not used: Astra, Fable.

## 5. Open items and recommended next step

1. **Fixed-design EP, growing p_𝒞, small omitted residual** (0 < Δ_n ≲ σ²(1/3 + rank/N)): TAIL^𝒞 is not proved there.
   T02(i♯)'s denominator strategy provably loses a factor e^{−cN} (Lemma O2). Next step: a sufficient-statistic
   reduction to (P_V y, ‖(I − P_V)y‖²), conjectured to lose only e^{−c·rank} (L5 §3a).
2. **Approximate (non-exact) projection in fixed design**, i.e. a sparse part plus a small leaking residual. The
   natural hypotheses are GEN-type leakage conditions NL_η / NL_avg. Not attempted.
3. **Outside GR** (non-Gaussian or heteroscedastic omitted residual): SL-style KL-projection results are not covered.
   Example E2 shows that Gaussian marginals alone are not enough.
4. Growing-p null projection, random-design EP versions, and n-dependent τ_n²: not claimed.
5. **For the paper:** state Theorem MIS (with Proposition P's neighbour rule and Corollary N) as the misspecification
   analog of SL Thm 4 / Cor 2; give Corollary D′ as the reported-HPM instance; put Theorem F with Lemma T in the
   supplement; and list items 1–3 as the frontier.

## 6. Files produced (Theory_work/Wave1C/C-MIS/)

STATEMENT.md (v1.2), PLAN.md, LOG.md, CHECKPOINT.md, REPORT.md.

lemmas/: 00_MAIN.md (proof map and hypothesis-to-step table), L1_reduction.md, L2_gaussian.md, L3_hpm.md,
L4_theoremF.md, L5_frontier.md, L6_null.md.

numerics/:
- Core and drivers: mis_core.py, run_experiments.py, check_L4.py, citecheck.py.
- Results: N1–N7 and N3b `*_results.json` / `*_summary.md`; check_L4_results.json and check_L4_summary.md.
- Logs and summary: run_all_output.txt, N3b_output.txt, SUMMARY.md.

reviews/: R01–R08 verbatim, dispositions (R01, R02_R03, R04, R05, R06, R07_R08), COUNCIL_BRIEF.md, CITECHECK.txt.

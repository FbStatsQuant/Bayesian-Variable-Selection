# W2-FAC-X — REPORT to Theory HQ (iid rows and general loadings for the factor result)

> **Flags (read first).**
> 1. **Scope.** HQ moved target item 3 (k ≥ 2) to W2-FAC-K2 (09:22). This ticket: Target 1 (iid Gaussian rows,
>    compound symmetry, largest exponent) and Target 2 (general one-factor loadings).
> 2. **Target 1 result: Theorem FAC-CS-iid** — iid Gaussian rows with covariance Υ[(1 − ρ)I + ρ11ᵀ]Υ, fixed ρ ∈ (0, 1),
>    **limsup log p/log n < 1/2** (3× FAC-A's 1/6; FAC-B's p ≤ n/2 is for exact Gram only), fixed s₀ ≥ 1, fixed raw
>    coefficients with the population no-cancellation condition (FS); claims (C1) start mode, (C2) path lemma,
>    (C3) reported-model consistency under the joint law, (C4) delivery P(Ŝ⁺ = S₀) → 1. Status: see §1.
> 3. **No method change.** Method as merged (v3.1, main 4676af6); the MR1 cap ℓ_n + |S̃₀| is used essentially (the
>    start mode is [p] ∖ N₀ and LS0 needs m₀ ≈ p moves), as in FAC-B.
> 4. **The 1/2 is a proof-technique limit, not a method limit** (evidence: N1X, 121/121 paths fine up to
>    log p/log n = 0.75). The technique absorbs a worst-case "band" term of size ≍ p·H̄·√(log n/n)·ϖ into ϖ; that is
>    possible when p H̄ √(log n/n) → 0 (sufficient, not necessary).
> 5. **Target 2** (general loadings): diagnosed (N2X); a corollary for polynomially vanishing loading dispersion
>    (lemmas/X7, draft, unchecked) and a parallel prover on finitely many loading classes (T2/) — status in §5.
> 6. **Framing (HQ, Felipe):** §6 lists exactly which general-assumption ingredients the proof uses, for W2-UNI.
> 7. All results asymptotic (scope rule); the onset n₀ is astronomically large (FAC-B's K₁ = 250 000, now
>    K₁ = 100/ε_b² with ε_b ≤ (½ − A₁)/5).

## 1. RESULT

Target 1: **[pending council]** — statement lock R01 REJECT → R02 LOCK-WITH-CHANGES → v3 locked; every lemma
cross-family checked (R03, R03b, R04 xhigh, R05); independent mid-point R06 **CONTINUE**; exhaustive sweep R07
**0 FATAL / 0 MAJOR / 3 MINOR / 9 EDITORIAL**, all fixed; council: §4. Target 2: PARTIAL (§5).

## 2. The statement (STATEMENT.md v3, locked; proofs lemmas/X1–X6)

**Setting.** Model R: rows of X^r iid N_p(m, Σ_n), ε ~ N(0, σ²I) independent; X = CX^rD_x⁻¹, θ* = D_xβ;
Σ_n = Υ_n[(1 − ρ)I + ρ11ᵀ]Υ_n; (P-½) limsup log p/log n < 1/2; (θ) s₀ ≥ 1 fixed, sign-corrected raw coefficients a
fixed nonzero vector ϑ, positions arbitrary; (FS) population no-cancellation (FAC-B's condition).
**Theorem FAC-CS-iid.** (C1) S* = [p] ∖ N₀ is the unique maximiser of γ₀ (N₀ = nulls in the realised block containing
S₀, ≤ 15). (C2) On one event of probability → 1, simultaneously for every set 𝔫 of ≤ 15 nulls, the uncapped LS0 search
from [p] ∖ 𝔫 makes only null deletions, each a ϖ_n-approximate argmin of |ξ_j − x_T| (ϖ_n = C H̄√(p log n/n) + n^{−1/3}),
with additions ≤ −c log n, swaps below the chosen deletion, truth moves negative, deleted nulls inside
(a_T − 4.3ϖ_n, b_T + 4.3ϖ_n), ending after exactly m₀ moves at S₀ (strict local maximum); so LS0 with the MR1 cap
scores and certifies S₀, the legacy cap misses it when m₀ ≥ ℓ_n + 2. (C3) D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0,
liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n), under the joint law. (C4) With Proposition F's premises, allocation and
total tier-1 fallback (CAL-free): P(no output) = 0 and P(Ŝ⁺ = S₀) → 1.

**Mechanism.** (X1) Exact rotation in 1^⊥ (axes: noise direction, factor direction): the noise coordinates
ξ_j = u_jᵀe/‖e‖ are iid N(0, 1) and **exactly independent** of the idiosyncratic Wishart matrix W ~ W_p(n − 3, I);
RSS_T = ‖e‖²/(1 + q_T) with q_T = ṽ1ᵀ(W_T + ṽ2ṽ2ᵀ)⁻¹ṽ1; replacing W by (n − 3)I gives FAC-B's one-dimensional statistic
ξ_j − x_T with the exact drift identity; all ridge/determinant/Q-vs-RSS corrections are bounded in absolute terms.
(X2) Resolvent expansion: δ_j(T) = −(Rc)_j + …, R = W_T/N − I; on band-structured sets the first-order sum is bounded by
Gaussian conditioning over ξ-defined intervals (independence of W and ξ) plus crude bounds on the band and on N₀.
(X3) Deterministic: ϖ-approximate argmin deletions with the exact drift identity keep the deleted set an interval up to a
4.3ϖ band — a kept point can be crossed by the centre only while the hole is narrower than 4ϖ (|K| ≥ 3), and under a
density hypothesis that phase lasts ≤ Q steps with centre movement ≤ ϖ/10. (X4) Induction on established prefixes:
band structure → perturbation bound (band count fed back; needs p H̄√(log n/n) → 0) → approximate rule → FAC-B's bulk
Claim B (centre bound with band corrections via a tail-ratio event) and end phase (top-value spacings make the band
empty; FAC-B's majority-side dynamics with τ̂ = τ + δ). (X5) Start mode conditionally on the raw design. (X6)
Every-sequence de-randomisation for T03♯; [OP], [M5-0] given the raw design, integrated; delivery as FAC-B L5.4 / A2.

## 3. Status per clause

| clause | content | evidence |
|---|---|---|
| X1 | representation, reference statistic, gains (g1)–(g5) | R03 Sol high V-W-A (1 minor, applied); iid_selftest_out.txt; R03 recomputed Schur/swap identities to 1e−15 |
| X2 | event 𝔈_n, Proposition X2 | R03 V-W-A (4 minor, applied); N1X (proxy) |
| X3 | deterministic soft gap | R03 FAILED as written on (iii) (MAJOR, counterexamples) → repaired per R03 → fresh re-check R03b V-W-A (3 minor, applied); N3X 0 violations (480 runs) |
| X4 / (C2) | key path lemma | R04 Sol xhigh V-W-A, no FATAL/MAJOR (7 minor, applied); N1X 121/121; council seat R09's exact-perturbation runs at ρ ∈ {0.02, 0.05, 0.95} (reviews/R09_scratch/c3_out.txt): 16/16 pure deletions to S₀, observed slack and band within 2ϖ, 4.3ϖ |
| X5 / (C1) | start mode | R05 V-W-A (2 MAJOR: raw-design conditioning, two-sided zero-pair event — applied); N5X 48/48 |
| X6 / (C3), (C4) | assembly, delivery | R05 V-W-A (applied) |
| programme | mid-point | R06 fresh Sol xhigh **CONTINUE** (3 minor, applied) |
| whole proof | sweep | R07 Sol xhigh 0/0/3/9, all fixed |
| deliverable | council | §4 |

Inputs (statuses verbatim): T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; T03♯ "PROVED; SF VERIFIED
(W2-VT03R); XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; Lemma CAP
"PROVED (by this seat)", council-checked; Proposition F (A1 corrected statement) and F-GROW "PROVED (A2), checked by A3";
Lemma CR "PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)"; FAC-B Theorem FAC-CS and FAC-A Theorem FAC-L
PROVED-CHECKED (used as templates / for the de-randomisation pattern).

## 4. Review trail

Statement lock R01 (Sol high) REJECT (6 changes: a deterministic counterexample to the plan's informal soft gap; no
family-wide no-addition; normalisation; random N₀; s₀ ≥ 1 and (FS′); frontier) → v2; R02 (fresh Sol high)
LOCK-WITH-CHANGES (5: prefix form of X3; bounded-p event constants with an explicit counterexample; bindings in (C2);
gain slack; "iff" wording) → v3 locked. Lemma checks R03, R03b, R04 (xhigh), R05. Mid-point R06 CONTINUE. Sweep R07.
Council: [pending]. Dispositions: reviews/R0x_disposition.md. Citation check: reviews/CITECHECK.txt. Astra / Fable:
not used. All reviewers via delegate_task (Codex gpt-6.1-sol).

## 5. Target 2 (general one-factor loadings) — status

* **Diagnosis (N2X, 64/64 paths fine, exact reference and iid rows; two-class loadings 0.3/0.9, 0.5/0.95, uniform
  [0.2, 0.9]).** With ℓ_j = λ_j/√(1 − λ_j²) the whitened deletion statistic is |ξ_j − ℓ_jX_T|/norm_j with **one scalar
  X_T** but loading-specific centres ℓ_jX_T; in the exact reference the path is exactly the argmin of this statistic, and
  a common centre does not describe it.
* **Corollary FAC-NCS (lemmas/X7, draft, PROVED (by this seat, unchecked)):** for loadings with
  max_j|λ_j − λ̄| ≤ n^{−c} (exact Gram and iid rows, limsup log p/log n < 1/2), (C1)–(C4) hold: the dispersion enters
  the perturbation as O(Δ·H̄) and is absorbed into ϖ. Not yet statement-locked or reviewed.
* **Fixed dispersion — exact obstruction to this technique:** the variable centres add (ℓ_j − ℓ̄)X_T to the statistic;
  the proof only controls |X_T| ≤ ε_bH in the bulk, so the induced band has width ≍ Δ·ε_bH, a fixed fraction of the
  kept tail falls in it, and the balance argument (B3) breaks. A finer route (per-loading-class interval holes, which
  are exact for finitely many classes since cross-class drift is ≤ ℓ_cℓ_{c′}d/Σℓ² < d) is being attempted by a parallel
  prover (T2/); [result pending].

## 6. General-assumption ingredients used (for W2-UNI; HQ framing note)

| ingredient | where used | general form it needs |
|---|---|---|
| iid **Gaussian** rows | X1 (exact rotation; ξ ⊥ W; the ξ_j are iid N(0, 1) because the idiosyncratic vectors are isotropic Gaussian — their projections on any independent direction e₁ are iid standard normal; this gives the sign symmetry used in E5 / B3), X2 (Wishart concentration, conditional Gaussian row sums), X5/X6 (Lemma CR, de-randomisation) | Gaussian rows; rotation invariance of the idiosyncratic part |
| **one factor, equal loadings** (compound symmetry; the near-equal-loadings extension FAC-NCS of §5 is outside this council verdict) | X1.3 single common centre and exact drift identity → X3 (deterministic gap) and X4 (FAC-B's balance and end-phase dynamics) | this is the CS-specific step; general loadings need loading-specific centres (§5) |
| idiosyncratic Ψ ∝ I (diagonal, equal) | X1: whitened Gram = ṽ1ṽ1ᵀ + ṽ2ṽ2ᵀ + W with W ~ W_p(N, I) | diagonal Ψ with unequal entries turns, after whitening, into **unequal loadings** ℓ_j = λ_j/√ψ_j — i.e. Target 2 (§5), outside this theorem; block-local Ψ is **not** covered (it breaks the rank-one structure — FAC-B §5(b)) |
| sparse eigenvalue floor | λ_min(R̂) ≥ c₀ on all subsets (here on the full matrix, from the Davidson–Szarek singular-value bound with p ≤ n^{1/2}, X2 D1): ridge bounds X1.4, truth moves X4.6, (H0) X6.1 | W2-UNI's (A1) floor on log-size sets suffices for the posterior (H0) inputs only. The truth-move argument X4.6 needs a **residual-variance floor for a truth after conditioning on the large models the path visits** (sets of size ≈ p, and their one-move enlargements for swaps); a full-design eigenvalue floor is what this theorem supplies and uses. A log-size floor alone does **not** suffice (R08 item 1: orthonormal nulls u₁…u_m with m ≫ log n and truth x₀ = Σu_l/√m have all log-size floors → 1 but zero residual of x₀ on the nulls, and the shipped score's truth deletion then gains (1 − b²/σ²)/(4n) > 0 for |b| < σ) — an ingredient W2-UNI needs for path-type arguments |
| beta-min + non-masking | fixed nonzero ϑ (BM-∞, TL), (FS) = population partial covariances nonzero for block-local conditioning sets (start mode) | W2-UNI's (A3); (FS) is exactly a block-local non-masking condition |
| growth | p ≤ n^{A₁}, A₁ < ½: band absorption (X4.1), crude bulk additions (X4.4) | — |
| Gaussian noise | X1.1 (‖e‖²/σ² ~ χ²_{n−1}, direction e₁ uniform and independent of ‖e‖), X5 (conditional Gaussian zero-pair and noise-projection bounds), X6 (fixed-design posterior input T03♯, M5-0) | — |
Checked population class: Σ_n = Υ[(1 − ρ)I + ρ11ᵀ]Υ (Theorem FAC-CS-iid). Unchecked Target-2 extensions (§5, outside
this council verdict): general loadings λ_j ∈ [λ_lo, λ_hi] for log p/log n < A_S (Theorem FAC-GL) and near-equal loadings
Δ_nH̄_n ≤ n^{−1/3} for log p/log n < ½ (Corollary FAC-NCS).

## 7. Open items and recommended next steps

1. Target 2 beyond vanishing dispersion: per-class gap invariant (T2/), then a two-scale argument for continuous
   loadings; W2-SIM item B (numerics/SIM_REQUEST.md) tests heterogeneous loadings at p up to 5000.
2. A ≥ 1/2: decouple band membership from the Wishart row (leave-one-out) — a possible approach only; W2-SIM item A tests
   A ∈ [0.5, 0.9].
3. Exact-Gram near-CS with p ≤ n/2 (X7 remark 1): FAC-B's finer bulk analysis with ϖ-perturbations.

## 8. Files (Theory_work/Wave2/W2-FAC-X/)

STATEMENT.md (v3 locked), PLAN.md, LOG.md, CHECKPOINT.md, REPORT.md; lemmas/X1_representation.md, X2_perturbation.md,
X3_softgap.md, X4_path.md, X5_start.md, X6_assembly.md, X7_near_cs_loadings.md (Target 2 draft); reviews/R01–R07 (+R03b)
verbatim with dispositions, citecheck.py, CITECHECK.txt; numerics/: iid_core.py (exact iid-row sufficient statistics via
Bartlett at any n; exact incremental production LS0 path; reference mode), iid_selftest(.py/_out.txt), n1x_iid_cs.py →
N1X_raw.jsonl, N1X_summary.md; n2x_loadings.py → N2X_raw.jsonl, N2X_summary.md; n3x_softgap.py → N3X_out.txt;
n5x_start.py → N5X_out.txt; SIM_REQUEST.md; copies of FAC-B's bvs_core.py, fac_core.py, cs_core.py, cs_gain.py;
T2/ (parallel prover). No files outside this folder were modified; no git state changes.

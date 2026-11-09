# W2-FAC-B — REPORT to Theory HQ (route B: start-mode structure + path-restricted analysis)

> **Flags (read first).**
> 1. **Scope = the cleanest meaningful subclass** (protocol: "if the general class is out of reach"): **Theorem FAC-CS**
>    for exact-Gram **compound symmetry** Σ = (1 − ρ)I + ρ11ᵀ (up to column signs), fixed ρ ∈ (0, 1), **any p_n ≤ ⌊n/2⌋**
>    (bounded, growing, oscillating; the substantive regime p ≫ log n up to linear p, i.e. log p/log n up to 1 —
>    **far beyond FAC-A's whole-lattice limit 1/6**). Fixed s₀ and coefficients with a generic no-cancellation condition
>    (FS) — or the weaker (FS′), which covers FAC-A's masked-truth instance (flag 4). **Not covered:** study S5 (block CS with
>    p/5 blocks), general one-factor loadings, k ≥ 2 factors, iid-row designs, p > n/2. For each, §5 gives the exact
>    obstruction **to this proof technique**; none is a proved obstruction to consistency.
> 2. **No new method requirement.** The theorem is for the method as merged (v3.1, 4676af6). The merged LS0 cap
>    ℓ_n + |S̃₀| (MR1) is **used essentially**: the start mode is the whole model and LS0 needs exactly m₀ = p − s₀ − |N₀|
>    moves, so the legacy cap ℓ_n would miss S₀ (LS0 scored set). **Finding** (not a requirement): for p > n/2 one
>    diagnostic data set exceeds MR1's cap through a noise-fitting swap phase (METHOD_REQUIREMENTS.md).
> 3. **Statement history.** v1 REJECTED at lock (R01: a claimed log-n margin for swaps was false — analytic O_P(1)
>    counterexample; only "swaps are dominated by the chosen deletion" is claimed now); v2 LOCK-WITH-CHANGES (R02) → v3
>    locked; v3.1 = sweep fixes (R07) + the flagged post-lock addition (C1-M). No conclusion was strengthened; (C1-M) only
>    weakens a hypothesis.
> 4. **Post-lock addition (C1-M) / Corollary M (lemmas/L2.5)**, added after HQ's note on FAC-A's open item 4: masked
>    truths ((1 − ρ)ϑ_j + ρϑ(S₀) = 0, FAC-A's a = 1/2 instance) are covered under (FS′). Status "PROVED (by this seat,
>    unchecked)"; checked only by the council (R08 and R09 both verified it in full); numerics N7 18/18.
> 5. **Relation to W2-FAC-A** (read after HQ's update; not used in the proofs): FAC-A's open item 1 ("path route for CS
>    beyond 1/6; remaining step: the late stage with all remaining extras on one side") is exactly what this ticket's
>    end-phase analysis (L4.4: majority-side deletion and the extreme-tail imbalance dynamics) closes, for exact-Gram CS
>    with p ≤ n/2. FAC-A's S5 coverage (1 global factor + bounded blocks, log p/log n < 1/6) is not reproduced here.
> 6. All results are asymptotic (Wave-2 scope rule); the proof's onset is astronomically large (L_n = log log n ≳ 400).

## 1. RESULT

**PROVED-CHECKED** — Theorem FAC-CS (claims (C1)–(C4) of STATEMENT v3.1, plus the flagged (C1-M)). Statement lock
R02; every lemma cross-family checked (R03, R04 xhigh, R05); independent mid-point R06 **CONTINUE**; exhaustive sweep
R07 (0 fatal / 2 major / 11 minor / 4 editorial, all fixed); **council round 1 passed: Codex Sol 9.3, Claude Opus 9.0,
all six gates PASS in both seats.** Citation check 14/14.

## 2. The statement as proved (STATEMENT.md v3.1; proofs lemmas/L1–L5)

**Setting.** Fixed design (model G with θ* = D_xβ, μ = CX^rβ = Xθ*), exact Gram XᵀX = (n − 1)Υ_n[(1 − ρ)I + ρ11ᵀ]Υ_n,
Υ_n diagonal ±1; ρ ∈ (0, 1) fixed; p_n ≤ ⌊n/2⌋ (so K = p); s₀ fixed, sign-corrected truth coefficients ϑ fixed nonzero,
positions arbitrary; σ² fixed. **(FS):** ϑ(V) ≠ 0 for nonempty V ⊆ S₀, and ϑ_l + ρϑ(V)/(1 + (u − 1)ρ) ≠ 0 for l ∈ V ⊆ S₀,
u ∈ {0, …, 15} (sufficient generic no-cancellation; every population block increment c(U, l) = Cov(x_l, μ | x_U) is then
nonzero unless U ⊇ S₀ and l is null). **(FS′)** (C1-M): (FS-b) only for u ≥ 1, plus: a block holding a masked truth also
holds a null. Method v3.1 + LS0 with cap a_n = ℓ_n + |S̃₀| and the named implementation premises.

**Theorem FAC-CS.**
* **(C1) start mode** = S* := [p] ∖ N₀ (unique maximiser of γ₀, w.p. → 1), N₀ = nulls sharing a block with all truths
  (|N₀| ≤ 15; usually empty).
* **(C2) path** (key lemma) — the uncapped LS0 search from S* (i) deletes, at each step, the null whose ξ_j is closest to
  the explicit centre x_T = (Σ_{j∈T}ξ_j − ϱ_n)/(|T| + κ_n) (a shrunk mean of the standardised noise coordinates);
  (ii) every addition loses ≥ c log n (c = min{0.29, c_D/2}), every truth move loses, every swap and every other deletion is
  strictly below the chosen deletion; (iii) the deleted nulls always form an open gap (a_T, b_T) ∋ x_T of the sorted
  configuration (extended endpoints); (iv) after exactly m₀ moves it is at S₀, a strict local maximum. So LS0 with any cap
  ≥ m₀ − 1 scores S₀, with a_n ends there as a certified search endpoint; the legacy cap ℓ_n misses S₀ when m₀ ≥ ℓ_n + 2.
* **(C3)** (H0) is automatic (A = 1, φ₀² = g₀ = 1 − ρ, BM-∞); D_n ≤ P(LS0 misses S₀) → 0; P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0;
  liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n).
* **(C4) delivery** (new class extension of Proposition F, exactly as A2 does for GROW; CAL-free; all of Proposition F's
  premises, total tier-1 fallback, amended allocation W_G/M_G and the LS0 preflight terms): P(no output) = 0 for every
  admissible n ≥ 3, and **P(Ŝ⁺ = S₀) → 1** under the original noise law.

**Mechanism.** (1) Every null block absorbs the common-factor signal through the full-response block tables: order-n
likelihood increments against an O(log n) size cost, so the start mode is the whole model (L2; numerics N1, N4) and no
O(log n) relevance set exists — GROW's route cannot apply and the LS0 cap must be ≳ |S̃₀|. (2) Under compound symmetry the
score of every neighbour is an exact monotone function of |ξ_j − x_T| with **one common centre** for deletions,
additions and swaps, and an exact drift identity x_{T∖j} = x_T − (ξ_j − x_T)/(|T| − 1 + κ_n) (L1). (3) Path-restricted
analysis (L4) — never whole-lattice NA (which is false here): the gap invariant with self-correcting asymmetry (L4.1);
in the bulk, the centre is controlled by comparing the path's retained set with a symmetric top set, whose sum is a
conditional Rademacher sum (sign symmetry, no union over exponentially many sets); at the end, the majority-side deletion
rule keeps the sign imbalance of the remaining extremes at ≤ 1 (margin c_D = ½ − 1/(s₀ + 1 + (1 − ρ)/ρ) > 0, also for
s₀ = 1 and ρ near 1); a crude regime p ≤ n^{1/200} covers bounded p.

## 3. Status per clause

| clause | content | evidence |
|---|---|---|
| L1 | exact 1-D reduction, gains, centre, Q vs RSS | R03 Sol high VERIFIED-WITH-AMENDMENTS (2), applied; cs_selftest_out.txt, fac_selftest_out.txt |
| L2 / (C1) | start mode = S* | R03 V-W-A (1), applied; N4_out.txt (66/72; the 6 misses all at n = 10⁵; every data set with n ≥ 10⁷ matches) |
| L2.5 / (C1-M) | masked truths under (FS′) | PROVED (by this seat, unchecked); council-checked only (R08, R09); N7_out.txt 18/18 |
| L3 | event E_n, P → 1 | R03 V-W-A (5), applied |
| L4 / (C2) | key path lemma | R04 Sol xhigh V-W-A, no fatal (7), applied; N3 (468 runs), N3b (12 hard corners), N6 (direct gap test incl. N₀ ≠ ∅), N5 (exploratory) |
| L5 / (C3), (C4) | assembly, (H0), delivery | R05 Sol high V-W-A (4 minor), applied |
| whole programme | mid-point | R06 fresh Sol xhigh **CONTINUE** (2 minor, applied) |
| whole proof | sweep | R07 Sol xhigh: 0 / 2 / 11 / 4, all fixed |
| deliverable | council | R08 Sol xhigh **9.3**, R09 Opus high **9.0**, all gates PASS |

Inputs (statuses verbatim): T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; T03♯ "PROVED; SF VERIFIED
(W2-VT03R); XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; Lemma CAP
"PROVED (by this seat)", council-checked; Proposition F (A1 corrected form, council round 3; A4 "OK-WITH-FIXES") and
F-GROW "PROVED (A2), checked by A3". Premises e4/e4′ (N3 OPEN — only uniqueness of the maximiser is used), EX-A, GUARD-W
etc. remain named premises.

## 4. Review trail

* Statement lock: R01 (Sol high) **REJECT** (swap margin false; 7 changes) → v2; R02 (fresh Sol high) **LOCK-WITH-CHANGES**
  (4 changes) → v3 locked.
* Lemma checks: R03 (L1–L3) V-W-A ×3; R04 (L4, xhigh) V-W-A, no fatal; R05 (L5) V-W-A.
* Mid-point: R06 (fresh Sol xhigh) **CONTINUE**.
* Exhaustive sweep: R07 (Sol xhigh) 0 fatal / 2 major / 11 minor / 4 editorial — all fixed (v3.1).
* Council round 1: **R08 Sol 9.3, R09 Opus 9.0; all six gates PASS in both → PASSED.** R09's two required fixes were
  editorial (this report); its optional suggestions applied (reviews/R08_R09_disposition.md).
* Citation check: reviews/CITECHECK.txt, 14 citations, 0 misses. Astra / Fable: not used. All reviewers via delegate_task.

## 5. Frontier — exact obstructions (to this technique) and evidence

* **(a) p > n/2 (p > K; the study's p ≫ n S5 regime).** The start mode can be size-saturated (|S̃₀| = K, not in general: if
  p − |N₀| < K it is not); at |T| ≈ n/2 the residual dimension halves, swaps (outside null in, retained null out) gain
  ≈ M·(τ_in² − τ_out²) with M ≈ 1 while deletions gain ≈ ½log n + log((2p − K)/K) − M τ² — so the path need not be a pure
  deletion. Evidence: N2 (exact Gram, ρ = 0.5, n = 600, p = 500): 19 swaps then 296 deletions, 315 moves > MR1 cap 311 ⇒
  LS0 misses S₀ (last scanned centre 4 extras, returned neighbour 3). Heuristic: the number of profitable swaps grows
  polynomially when log p/log n > 1, so MR1's slack ℓ_n + s₀ would not cover it. **Not proved**; a cap allowing a swap
  phase is a possible response, not shown to suffice.
* **(b) S5 / block compound symmetry (bounded groups, p/5 groups, plus a global factor).** The scan is no longer
  one-dimensional: a null's deletion statistic is its noise coordinate minus a **group-level** centre (depending on which
  group-mates are retained) minus the global centre, with group-size-dependent normalisations. When a group-mate is
  deleted, the effective values of the other group members (retained or deleted) jump by a within-group regression term
  (weight b/(c + bu) for Ψ_G = bJ + cI; S5: 0.4/(0.3 + 0.4u)), so the gap invariant fails as stated and deleted nulls can
  move toward the add threshold. A proof needs a two-level (group/global) gap invariant controlling these jumps; a crude
  end-phase bound suggests a constraint like log p/log n ≲ 1/3 for S5's constants unless the jumps are controlled
  through the path (heuristic). Evidence: N1 (exact-Gram S5, p ≤ 400): full start and pure deletion at n ≥ 10⁸ (most at
  10⁶); FAC-A covers S5 for log p/log n < 1/6.
* **(c) general one-factor loadings (unequal λ_j) and k ≥ 2.** Variable-specific centres ρ_jx_T (or a k-dimensional
  centre) make the retained set history-dependent in a band of width ≈ max|x_T|; the bulk sign comparison is then exact
  only up to that band, and a naive bootstrap of |x_T| loses a factor ≈ log n. Multi-class exchangeable designs (k classes
  of equal loadings) keep a finite-dimensional exact reduction and look like the natural next case.
* **(d) iid rows.** The sample Gram is not exactly compound symmetric (‖R̂ − Σ‖ ≈ √(p/n)); the exact reduction holds only
  up to perturbations that again enter through the band of (c).
* **(e) (FS) failures** (council R09 control): with ϑ_a + ϑ_b = 0 the start mode is a strict subset of S* but the LS0 path
  still ended at S₀ (3/3 data sets, R09 scratch) — suggesting (C3)/(C4) survive more general no-cancellation failures.
  Not claimed.

## 6. Open items and recommended next step

1. **S5 beyond 1/6 (HQ priority 1):** extend L1 to block exchangeability (two-level closed form: per-group sums and the
   global aggregate, all exact) and L4 to a two-level gap invariant; FAC-A's lattice result covers log p/log n < 1/6.
   Recommended follow-up ticket; the obstruction is precisely the within-group jumps of §5(b).
2. **p > K (HQ priority 2):** characterise the saturated start and the swap phase; either bound the number of swaps
   (then a cap like ℓ_n + 2|S̃₀| might suffice — needs proof and would be a method change) or show the LS0 route fails
   asymptotically (a counterexample for the LS0 route, not for the method).
3. **k ≥ 2 (HQ priority 3):** multi-class exchangeable designs first.
4. iid rows for CS (perturbation of the exact reduction).
5. For the paper: state Theorem FAC-CS next to GEN, GROW and FAC-A's Theorem FAC-L; compound symmetry is covered for all
   p ≤ n/2 (S5 remains at FAC-A's 1/6 coverage); note that MR1 is essential on this class.

## 7. Files produced (Theory_work/Wave2/W2-FAC-B/)

STATEMENT.md (v3.1, locked), PLAN.md, LOG.md, CHECKPOINT.md, METHOD_REQUIREMENTS.md, REPORT.md;
lemmas/L1_cs_reduction.md, L2_start.md (incl. L2.5 Corollary M), L3_event.md, L4_path.md, L5_assembly.md;
reviews/R01–R09 (verbatim reviewer outputs; R08_scratch, R09_scratch are the council seats' own checks), dispositions
R01–R07 and R08_R09, COUNCIL_BRIEF.md, citecheck.py, CITECHECK.txt;
numerics/: fac_core.py (exact-Gram general scorer and closed-form Schur scans), bvs_core.py (copied unchanged from C-GROW),
cs_core.py, cs_gain.py (compound-symmetry closed form, production tie rule), self-tests (fac_selftest, cs_selftest +
outputs), n1_run/n1_grid/n1_summary (N1), n2_saturated (N2), n3_cs (N3), n3b_corners (N3b), n4_start (N4), n5_invariants
(N5, exploratory), n6_gap (N6), n7_masked (N7); raw JSONL/CSV outputs and summaries N1–N4, N6, N3b, N7_out.txt.
No files outside this folder were modified; no git state changes.

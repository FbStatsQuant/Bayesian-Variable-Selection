# C-GROW — REPORT to Theory HQ

> **Flags (read first).**
> 1. **Method requirement MR1 (for C-ENG):** LS0 must run with move cap **ℓ^{LS0} = ℓ_n + |S̃₀|** (instead of the
>    production ℓ_n = ⌈log₂(n + p + 1)⌉). LS0 is not shipped, so this is a permitted parameter choice (Wave-1C protocol
>    "Method-side changes"); details and cost in METHOD_REQUIREMENTS.md. Without MR1 the theorem holds only under
>    (G4-χ) (relevance set ≤ (1 − δ₀) log n), where the production cap suffices.
> 2. **Statement changes after lock (all logged):** v2.1 piecewise AR(1) relevance set (R04); v2.2 wording (R05);
>    **v2.3 extension — claim (C5)(c), random-design (iid-row) AR(1) = the study generator's S2 design, p ≤ n^A incl.
>    p ≫ n**, proved by a parallel prover (Codex Sol) and checked by two independent reviewers (R06 Claude Opus,
>    cross-family; R07 Sol); v2.4 sweep fixes, v2.5 council-F1 fixed-p caveat (no claim changed).
> 3. **Diagnosis:** S2 was a proof gap (closed, incl. random design). S5 is an **LS0-cap** gap at practical n (closed
>    by MR1 in the component numerics); the production core *without* LS0 reported S₀ as HPM in all 25 tested fits
>    (S2/S5, n ≤ 3200), so no failure of discovery by the full method was observed. S5 is covered only as a fixed-p
>    population-covariance illustration; random-design S5 and factor designs with growing p remain frontier.
> 4. **Everything is asymptotic.** Falsification numerics show the asymptotic events failing at tested finite n
>    (NA over the whole lattice; far nulls in the start mode at n ≤ 800); the sufficient conditions' onsets are far
>    beyond practical n. No finite-n claim is made.
> 5. Conditional on the named implementation premises (EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, **e4 (N3 OPEN)**, complete
>    scans), on [OP] as in GEN, and on MR1. No delivery claim.
> 6. Side finding: W1-GEN numerics templates (e.g. `Theory_work/Wave1/W1-GEN/numerics/e5_outside.py`) contain literal
>    "\S0" text in place of digits at git HEAD and do not run.

## 1. RESULT

**PROVED-CHECKED** — Theorem GROW (reported-HPM consistency with a growing relevance set, under MR1) and its
instances (C5)(a) AR(1) exact Gram, (C5)(c) **AR(1) with iid rows = study S2, p ≤ n^A incl. p ≫ n**, (C5)(b) S5
population covariance at fixed p (illustration only, see the caveat in §2). Every lemma cross-family checked;
mid-point CONTINUE; sweep 0 fatal / 0 major, all fixed; **council round 1 passed: Sol 9.2, Opus 9.0, all six gates
PASS in both seats.** S5/factor designs with growing p and random-design S5: not proved (frontier, (C6)).

## 2. The statement as proved (STATEMENT.md v2.5; proof map lemmas/00_MAIN.md)

**Theorem GROW.** Fixed Gaussian design, standardized, fixed s₀, p ≤ n^A; v3.1 + LS0 with MR1 and the named premises.
Assume (H0) (the T03♯ hypotheses) and, for a deterministic null set 𝒫_n with Q = S₀ ∪ 𝒫_n, |Q| = O(log n):
(G1) feasibility; (G2) Gram floor on Q ∪ {l}; (G3) on the method's blocks: within-block SE, every truth block-visible
(TV), every variable outside Q block-negligible given its block's truths (NEG(η), η < (√(2A+1) − √(2A))²);
(G4) |𝒫_n| ≤ (1 − δ₀) log n, or at most p·n^{o(1)} add directions over the lattice [S₀, Q]. Then
D_n ≤ P(sandwich fails) + P(NAᶜ) + P(TLᶜ) → 0, **P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0**, liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n).
Mechanism: (C3) every start-mode maximiser lies between S₀ and Q (global size ladder + exchanges; no huge start
mode); (C2) on the lattice no addition and no truth-removing move improves the score; (C1) LS0 then deletes the extras
one at a time — **exactly |S̃₀ ∖ S₀| moves** (GEN used the upper bound 2^{v̄} − 1 and a bounded 𝒱).
**Instances (C5).** (a) AR(1), exact Gram, fixed ρ ≠ 0, separated truths, any p ≤ n − 1: relevance envelope of
radius ⌈log n/(2 log(1/|ρ|))⌉. (c) **AR(1) with iid Gaussian rows (study S2), p ≤ n^A incl. p ≫ n, under the joint
law** — the three events proved directly (selection-uniform reduction of block conditioning sets, conditional-sphere
tail of the RSS-normalised add statistic, exact population innovations for NA); the generator's p = 500/1000 S2
layouts satisfy the separation condition for every signal scale. (b) S5's population covariance at fixed p = 100
(diagnostic layout): TV by an exact rational certificate (τ₀ = 4/25, 1/25); asymptotic only (needs log n ≳ 96).

**Where the theorem has content (council F1).** For fixed p (or p growing slower than ≈ log₂ n) the production run
eventually enumerates all models (SoP `02_method.tex:167`) — for p = 100 from n ≳ 2.5·10²⁷, before the (G4-χ) onset —
and T03♯ alone gives the conclusion; so (C5)(b) only shows that S5's population covariance satisfies the hypotheses.
The LS0 mechanism is the operative one for p ≫ log n: (C5)(a) with growing p ≤ n − 1 and (C5)(c) with p ≤ n^A.

**Change vs the brief.** Target met for S2 (fixed and random design, polynomial p) with MR1; S5 met only as a fixed-p
illustration; general class stated with checkable block-level and lattice conditions (Song–Liang-type: Gram floors,
beta-min, plus block visibility/negligibility).

## 3. Status per clause

| Clause | Content | Evidence |
|---|---|---|
| L0 | score expansion for sets of size O(log n) | lemmas/L0_toolkit.md; R03 Sol VERIFIED (reviews/R03_L0L1L2_check_sol.md) |
| (C1) | deterministic lattice descent, exact move count | L1_descent.md; R03 Sol VERIFIED |
| (C2) | TL, NA (χ²-route, direction-count route) | L2_NA_TL.md; R03 Sol V-W-A (2), applied; numerics F1X (NA in the χ² regime, 0/80 failures at n ≥ 800) |
| (C3) | centre sandwich, all maximisers | L3_sandwich.md; **R02 Sol xhigh VERIFIED** (reviews/R02_L3_check_sol.md); numerics F1, F3 |
| (C4) | assembly ([OP], M5(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))", T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)", MR1) | L4_assembly.md; R04 Sol V-W-A (1), applied |
| (C5)(a),(b) | AR(1) exact Gram; S5 fixed p | L5_instances.md; R04 Sol V-W-A (2–7), applied; τ₀ certificate numerics/f2_exact_tau0.py → F2_exact_tau0.txt |
| (C5)(c) | AR(1) iid rows, p ≤ n^A | L6_random_AR1.md (author: Codex Sol parallel prover); R07 Sol xhigh VERIFIED; R06 Opus high V-W-A (A1–A9 presentation), applied |
| (C6) | frontier | STATEMENT (C6); numerics D2/D3 (p = 400), SUMMARY_FALSIF, G1 |

## 4. Review trail

* Statement lock R01 (Sol high): LOCK-WITH-CHANGES, 9 changes applied → v2 locked.
* Lemma checks: R02 L3 (Sol xhigh) VERIFIED; R03 L0/L1 VERIFIED, L2 V-W-A; R04 L4 V-W-A, L5 V-W-A; R06 (Opus) L6
  V-W-A; R07 (Sol) L6 VERIFIED.
* Mid-point R05 (fresh Sol xhigh): **CONTINUE** (4 minor items, applied).
* Exhaustive sweep R08 (Sol xhigh): 0 fatal, 0 major, 9 minor, 7 editorial — all fixed.
* Council round 1: **R09 Sol 9.2, R10 Opus 9.0; all six gates PASS in both → PASSED.** R10's one required fix (F1,
  wording: fixed-p caveat) applied afterwards (STATEMENT v2.5; no hypothesis or conclusion changed); see
  reviews/R09_R10_disposition.md. Citation check: reviews/CITECHECK.txt, 18 citations, 0 misses.
* Astra / Fable: not used. Helpers: Claude Sonnet 5.5 (numerics D, F, G); parallel prover Codex Sol (L6).

## 5. Open items and recommended next step

1. **S5 / factor designs with growing p, and random-design S5.** The start mode grows (median 23/43/74 extras at
   p = 100/200/400, n = 3200); LS0 with MR1 still scored S₀ in all tested runs. Proof obstacles: the sandwich needs
   |Q| = O(log n) (every null block carries factor signal), and NA needs a factor-aware direction count (residual
   directions depend on all of T through the factor). Suggested route: NA with a low-rank common component
   (Pythagorean split along the residual factor direction), and a sandwich with a growing Q but a polynomial ladder.
2. **Finite-n.** All statements are asymptotic; a sharper NA restricted to {T : |T ∖ S₀| ≤ |S̃₀ ∖ S₀|} (what the
   path uses) would bring the AR(1) onset much closer to practical n.
3. MR1 to C-ENG (METHOD_REQUIREMENTS.md); premise e4/N3 and LS0 integration remain with C-ENG/W1-N3. Council remark
   (R10 S1): this theorem uses e4 only as "the emitted LS0 centre is some maximiser of γ₀" (the sandwich holds for
   every maximiser), so the N3 tie-rule invariant is not needed here — HQ may weaken the premise (consistent with
   C-PACK's "e4 not needed").
4. For the paper: state Theorem GROW with the AR(1) random-design corollary (study S2) next to Theorem GEN; S5 as the
   frontier with the numerics.

## 6. Files produced (Theory_work/Wave1C/C-GROW/)

STATEMENT.md (v2.5), PLAN.md, LOG.md, CHECKPOINT.md, METHOD_REQUIREMENTS.md, REPORT.md; lemmas/00_MAIN.md,
L0_toolkit.md, L1_descent.md, L2_NA_TL.md, L3_sandwich.md, L4_assembly.md, L5_instances.md, L6_random_AR1.md;
reviews/R01–R10 (verbatim reviewer outputs) + dispositions R01, R03, R04, R05, R06_R07, R08, R09_R10, COUNCIL_BRIEF.md, CITECHECK.txt, citecheck.py; numerics/ (D1–D4 diagnosis, F1–F3 +
F1X falsification, G1 random-design falsification, f2_exact_tau0 certificate; scripts, raw CSVs, summaries).

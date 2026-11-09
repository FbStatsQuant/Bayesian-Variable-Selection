# W2-FAC-S5 — REPORT to Theory HQ (block compound symmetry / study S5 beyond 1/6)

> **Flags (read first).**
> 1. **RESULT = PARTIAL.** **PROVED-CHECKED** (lemma checks R02–R04, mid-point R05, sweep R06, council round 2 passed: R09
>    Sol 8.8, R10 Opus 8.8, all six gates PASS): **Theorem FAC-BCS-R (reduction)** — on exact-Gram block compound symmetry
>    (S5 and any fixed (ρ_b, ρ_w, q̄)), with probability → 1 the unique start mode is S* = [p] ∖ N₀ (|N₀| ≤ 15; the whole
>    model when N₀ = ∅) for every p ≤ n/2, and for log p/log n < α < 1/2
>    the LS0 path is the best-null-deletion path ending certified at S₀ **on the event CC_n(δ)** (control of one scalar, the
>    latent global-factor error e_T, along that path); consistency and delivery hold **up to P̃(CC_n(δ)ᶜ)**. **Not proved:**
>    Lemma KL (P̃(CC_n(δ)) → 1) for any exponent above 1/6 — so the unconditional S5 frontier stays at FAC-A's 1/6 (under
>    FAC-A's own hypotheses, its (TV) condition and truth layouts, which differ from (FS-BCS)). Unconditional corollary of
>    Tier 1 under (FS-BCS): consistency and delivery for limsup log p/log n < 1/(2(1 + κ₀)²) (S5: 0.104), via the crude
>    all-set bound (R05, R10).
> 2. **The obstruction is now exact and one-dimensional**: everything except e_T is controlled by a union bound over
>    (null, group-mate set) pairs; the within-group jumps HQ asked about are irrelevant below exponent 1/2. All-set bounds on
>    e_T are of the same order as the deletion level (sharp for all-set arguments by a matching lattice lower bound in prover
>    round 2, `KL_attempt_sol2/02_lattice_obstruction.md` — unchecked),
>    so any progress must use the path. Partial results (unchecked, two Codex prover rounds; for s₀ = 4 where stated, and
>    for exact noise-argmin paths rather than the score-defined Π where stated — §5) cover the dense range and the last
>    ≤ 250 retained nulls at exponent 0.17; a middle band remains.
> 3. **No new method requirement.** The merged MR1 cap a_n = ℓ_n + |S̃₀| is used essentially in the growing-start regime
>    (m₀ = |S* ∖ S₀| ≫ log n: the start S* contains all but ≤ 15 nulls, and LS0 needs m₀ moves).
> 4. Statement history: v1 → R01 LOCK-WITH-CHANGES → **v2 locked**; v2.1–v2.3 are post-lock wording/notation fixes
>    (R03, R05, R06), no hypothesis or claim changed. Before the lock verdict the lead corrected the centre condition to a
>    size-dependent form (the first form, κ₀|e| ≤ cH for every c, is false near the end of the path).
> 5. All results asymptotic (Wave-2 scope rule). HQ framing note (design-agnostic main theorem, W2-UNI): §7 lists the
>    general ingredients the proof uses.

## 1. RESULT

**PARTIAL.** Tier 1 (Theorem FAC-BCS-R: claims (C1), (C2-R), (C3-R), (C4-R) of STATEMENT v2.3) is **PROVED-CHECKED**:
statement lock R01; lemma checks R02 (L1 FAILED as written → repaired; L2, L3 V-W-A), R03 (key lemma, xhigh, V-W-A), R04
(V-W-A); mid-point R05 **CONTINUE**; exhaustive sweep R06 (0 fatal / 1 major / 11 minor / 7 editorial, all fixed); council
round 1 not passed (R07 Sol 7.8, report-scope fixes; R08 Opus 8.6), **round 2 passed: R09 Sol 8.8, R10 Opus 8.8, all six
gates PASS in both, no required fixes.**
Tier 2 (Lemma KL, claim (C5)): **open**; not claimed.

## 2. The statement as proved (STATEMENT.md v2.3; proofs lemmas/L1–L5)

**Setting.** Model G (fixed design), exact Gram XᵀX = (n − 1)ΥΣΥ, Σ = ρ_b11ᵀ + ⊕_g(bJ + dI), b = ρ_w − ρ_b > 0,
d = 1 − ρ_w > 0, groups of size ≤ q̄ (S5: .3/.7/5); fixed s₀ and nonzero sign-corrected coefficients ϑ; generic
no-cancellation (FS-BCS) (finitely many proper hyperplanes, via the inverse-M-matrix property of Σ); method v3.1 (main
4676af6) with MR1 and the named implementation premises.
* **(C1) start mode** = S* = [p] ∖ N₀ (unique maximiser of γ₀, w.p. → 1) for every p ≤ ⌊n/2⌋ (L2); N₀ (nulls sharing the
  unique method block that contains all truths, |N₀| ≤ 15) is nonempty in practice too (numerics/S4_out.txt: N₀ of size 8–9
  with one or two truths at p = 100).
* **(C2-R) path lemma** (key lemma, L4): for log p/log n < α < 1/2 and fixed δ ∈ (0, 1), on E_n ∩ CC_n(δ) the uncapped
  §6.10 search from S* follows Π (exact best null deletion); every addition and null-out swap loses ≥ (δ/8) log n to the
  chosen deletion, every truth-removing move loses ≥ c n; S₀ is a certified endpoint after m₀ moves.
  **CC_n(δ):** for every set T_i of Π (size k, terminal included) and every T′ ∈ {T_i} ∪ {T_i ∖ j: j retained null},
  (H_q + κ₀|e_{T′}|)² ≤ (1 − δ)(log n + 2 log((2p − k)/(k + 1))), e_R := h − E[h | g_R] (latent factor-prediction error),
  κ₀ = (1 − ρ_b)^{−1/2}, H_q² = 2 log(2^{q̄}p) + 2 log log n.
* **(C3-R)** D_n ≤ P̃(CC_n(δ)ᶜ) + o(1); P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P̃(CC_n(δ)ᶜ) + o(1) (L5; P̃ = enlarged space).
* **(C4-R)** under all Proposition F premises (CAL-free): P(no output) = 0 for every admissible n ≥ 3 and
  P(Ŝ⁺ ≠ S₀) ≤ P̃(CC_n(δ)ᶜ) + o(1).
* **Mechanism.** (L1) Every neighbour score is an exact function of per-group compound-symmetry residuals A_l(U)
  (U = retained group-mates) and one scalar e_R: τ_{l|R} = (√ψ_u A_l(U) + a_u e_R)/√(ψ_u + a_u²V_R), so
  |τ| ≤ |A| + κ₀|e_R|. There are ≤ p·2^{q̄} distinct A's, so |A| ≤ H_q uniformly (E_A); for α < 1/2 this alone makes the
  group parts harmless, and CC handles the rest. Truth moves lose order n by a separate signal argument (Gram floor d).
  **Non-vacuity** (R05): crude all-set bounds give P̃(CC_n(δ)) → 1 when 2a*(1 + κ₀)² < 1 − δ (S5: a* < 0.104).

## 3. Status per clause

| clause | content | evidence |
|---|---|---|
| L1 | exact two-level reduction; ridge/leakage/multiplier/determinant bounds | R02 FAILED as written (leakage rate √k/n^{3/2}), repaired; confirmed R03; R06 fixes. numerics: l1_identities_out.txt (361 instances, ≤ 1.5e−14), l1_leak_out.txt, bcs_selftest_out.txt |
| L2 / (C1) | start mode = S*, p ≤ n/2 | R02 V-W-A, applied; S4_out.txt 36/36 (FACB Python replica) |
| L3 | event E_n | R02 V-W-A; R06 item 1 (major: E_S block-local quantifier) fixed |
| L4 / (C2-R) | key path lemma under CC | R03 (Sol xhigh) V-W-A (3 minor) applied; S1X_summary.txt, S1X2_summary.txt (15/15 complete-scan paths pure null deletion to S₀, 0 exact ties, swap margin ≤ −0.436 log n) |
| L5 / (C3-R), (C4-R) | assembly, (H0), delivery | R04 V-W-A (measurability on enlarged space) applied |
| programme | mid-point | R05 fresh Sol xhigh **CONTINUE** (2 minor, applied) |
| whole proof | sweep | R06 Sol xhigh 0/1/11/7, all fixed (R06_disposition.md) |
| (C5) KL | P̃(CC_n) → 1 | **open**; prover outputs lemmas/KL_attempt_sol/, KL_attempt_sol2/ (unchecked) |

Inputs (statuses verbatim): T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; T03♯ "PROVED; SF VERIFIED
(W2-VT03R); XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; Lemma
CAP "PROVED (by this seat)", council-checked; Proposition F (A1) and F-GROW "PROVED (A2), checked by A3", preflight A4
"OK-WITH-FIXES"; FAC-CS "PROVED-CHECKED" (pattern only).

## 4. Review trail

* Statement lock: R01 (Sol high) LOCK-WITH-CHANGES (5 items) → v2 locked.
* Lemma checks: R02 (L1–L3, Sol high): L1 FAILED as written (one major, counterexample), L2/L3 V-W-A; R03 (L4, Sol xhigh)
  V-W-A, no fatal/major; R04 (L5, Sol high) V-W-A.
* Mid-point: R05 (fresh Sol xhigh) CONTINUE.
* Sweep: R06 (Sol xhigh) 0 fatal / 1 major / 11 minor / 7 editorial — all fixed.
* Council round 1 — R07 (Codex Sol xhigh) **7.8**, G1/G2 FAIL (report-level scope: N₀ exception; s₀ = 4 and exact-argmin
  qualifiers of the frontier), G3–G6 PASS; Tier 1 judged sound; fixes applied (reviews/R07_R08_disposition.md).
  R08 (Claude Opus 5.5 high) **8.6**, all six gates PASS (two label fixes). Round 1 not passed; all fixes of both seats
  applied (reviews/R07_R08_disposition.md). **Round 2 (fresh seats): R09 Codex Sol xhigh 8.8, R10 Claude Opus 5.5 high 8.8;
  all six gates PASS in both; no required fixes → PASSED.** Optional suggestions applied (reviews/R09_R10_disposition.md).
* Citation check: reviews/CITECHECK.txt. Astra/Fable: not used.

## 5. Frontier and exact obstruction (evidence; not claimed)

* **KL (the only missing piece for exponents in (1/6, 1/2)).** Prove that e_T stays below the size-dependent CC level
  along the greedy path. Known: (i) all-set (lattice) bounds give κ₀|e_T| ≈ √(2 log(p/k)) at size k — the same order as
  the deletion level — and this is sharp for all-set arguments (prover round 2, 02_lattice_obstruction.md, **unchecked**: the cutoff
  1/(2 + 4√(1 − θ)) at k ≈ p^θ, → 1/6), so a path argument is necessary for this route; (ii) round-1/2 prover partials
  (**unchecked**): *all-set results* — CC for full S5 with **s₀ = 4** on parents with ≤ 2 retained nulls (round 1,
  `lemmas/KL_attempt_sol/README.md:9-15`); the dense-size bound (CC on all parents with k ≥ p^θ when
  log p/log n < 1/(2 + 4√(1 − θ)), any s₀; round 2, `KL_attempt_sol2/01_group_lattice.md`) and, **for s₀ = 4**, at
  log p/log n ≤ 0.17 on all parents with k ≥ ⌈p^0.06⌉ or ≤ 250 retained nulls (`01_group_lattice.md:135-159`) — the s₀ = 4
  restriction matters: for s₀ = 1 a 250-null one-sided set violates CC at exponent 0.17 (R07 fix 2); *exact noise-argmin
  path modules* (deletion of the exact argmin of |τ_j(T)|, which is not the score-defined Π of Tier 1; transfer/perturbation
  stability to Π is unproved) — a retained null singleton never crosses the centre; cohort interval theorem with an
  explicit forcing term; a protected-champion lemma (the field-shifted group maximum is never the exact argmin while its
  group has ≥ 2 members; not established for near-argmin rules); a conditional terminal theorem for **s₀ = 4** (if
  κ₀|e| ≤ .05H up to the first champion deletion, CC holds afterwards for α < 0.4126; `05_conditional_terminal.md:3-29`).
  **Missing:** control of e_T in the remaining band (in the s₀ = 4 specialisation: at least 251 retained nulls and parent
  size k < ⌈p^0.06⌉), where genuine multi-member null groups evolve; the transfer from exact-argmin to the score path; the q-dimensional analogue of FAC-CS's static centre argument (B3) with path-dependent group states.
* **Numerics.** Pure null deletion to S₀ in every simulated S5 path (27 candidate-restricted, 15 + 15 complete-scan,
  log p/log n up to 0.92); observed (not a bound): κ₀|e|/H_q ≤ 0.05 while ≥ 30 nulls remain and ≤ 0.23 overall in the
  S3 runs (S3_summary.txt; R10's p = 30 runs reached 0.32 near the end); W2-SIM pilot
  (W2-SIM/results/FAC-S5_CC/pilot01, p up to 10⁴): bulk ratio decreasing with the retained count, end-phase ratio
  0.21–0.26, |imbalance| ≤ 2 at 30 retained nulls. Note (R08, corrected per R09): the diagnostic CC(0) margin is negative
  in 16/18 rows of S3_summary.txt; in many bulk cases H_q² alone exceeds the threshold Λ_k at simulated n, and some
  late-path failures also involve e_T (e.g. p = 500, n = 10¹², seed 3, k = 6). These finite-n checks do not establish the
  asymptotic high-probability CC assertion (W2-SIM's n = 10²⁰ run has positive margin 0.28 log n). Within one group (global level known) greedy elimination is exactly
  compound symmetric and satisfies re-add invariants exactly (s2_readd_out.txt) — a proposed route beyond 1/2, no
  necessity claimed.
* **p > n/2**: as FAC-B §5(a).

## 6. Open items and recommended next step

1. **KL in the middle band** (recommended follow-up ticket, research-grade): combine the round-2 modules (exact singleton
   interval dynamics, orthogonal-transition counts, protected champions) with a stopping-time argument that keeps
   κ₀|e_T| ≤ .05H until the champion gate; a cross-family check of the round-1/2 prover files first.
2. Extend Tier 1 to general one-factor loadings and bounded Ψ-blocks (direct: replace κ₀ by FAC-A's κ-type constant) and to
   k fixed factors (vector e_R) — for W2-UNI.
3. For the paper: state Theorem FAC-BCS-R as a reduction (S5 consistency up to the centre event), next to FAC-L (1/6,
   unconditional) and FAC-CS (CS, all p ≤ n/2).

## 7. General-assumption ingredients used (for W2-UNI)

1. Exact Gram XᵀX = (n − 1)Σ (random rows would add ‖R̂ − Σ‖ ≈ √(p/n) through L1.4's ε — not handled).
2. Eigenvalue floor on **all** principal submatrices, λ_min(Σ_TT) ≥ d > 0 (ridge/leakage bounds, determinant
   increments, start mode, truth moves, (H0)) — stronger than W2-UNI's (A1) floor on log-size sets, because sets of size up
   to p are scored along the path. **This is the main obstacle to a design-agnostic version** (R08): along the LS0 path the
   method scores sets of size up to p, so the floor is needed on all principal submatrices, not only on log-size sets.
3. One factor + bounded blocks, Σ = λλᵀ + Ψ, Ψ block-diagonal with blocks ≤ q̄: gives the exact residual split (group part
   on ≤ p·2^{q̄} statistics + coefficient × scalar factor error) and a uniform coefficient bound κ₀. General loadings /
   general bounded Ψ-blocks: same split with κ₀ replaced by FAC-A's κ-type constant; k fixed factors: e_R becomes a
   k-vector (both extensions direct but not written or checked here).
4. Positive partial covariances (inverse M-matrix) — only for the genericity of (FS-BCS) in the start mode; in general a
   non-cancellation hypothesis (W2-UNI (A3)).
5. Beta-min (fixed ϑ, i.e. √n-scale signal) and (FS-BCS) non-masking.
6. Growth: p ≤ n/2 (start), p ≤ n^α with α < 1/2 (path: H_q² ≈ 2 log p below log n), p = o(n) (multiplier M_T → ½).
7. The path event CC_n(δ) on the factor-prediction error — the only non-structural ingredient (open: KL).

## 8. Files produced (Theory_work/Wave2/W2-FAC-S5/)

STATEMENT.md (v2.3, locked), PLAN.md, LOG.md, CHECKPOINT.md, REPORT.md, REPORT_DRAFT_ingredients.md (superseded by §7);
lemmas/L1_bcs_reduction.md, L2_start.md, L3_event.md, L4_path.md, L5_assembly.md; lemmas/KL_attempt_sol/ and
KL_attempt_sol2/ (Codex prover outputs, unchecked); reviews/R01–R10 (verbatim reviewer reports; R07–R10 council) with dispositions, R08_scratch/, R10_scratch/,
KL_BRIEF.md, citecheck.py, CITECHECK.txt, council files; numerics/: bcs_core.py (closed-form BCS scorer), bcs_selftest.py
(+out), l1_identities.py (+out), l1_leak.py (+out), s1_path.py, s1_grid.sh, s1_out/, s1_exh.sh, s1_exh/, s1_exh2.sh, s1_exh2/,
S1X_summary.txt, S1X2_summary.txt, s2_readd.py (+out), s3_cc.py, s3_out/, s3b_out/, S3_summary.txt, s4_start.py, S4_out.txt,
SIM_REQUEST.md. No files outside this folder were modified (W2-SIM wrote its own results); no git state changes.

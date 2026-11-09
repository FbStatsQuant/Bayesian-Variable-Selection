# C-DLV — REPORT to Theory HQ (Wave 1C, delivery), 2026-11-08/09

> **Flags (read first).**
> 1. **The ticket target is NOT proved.** (T) "P(no output) → 0 on LH, LH-iid and the W1-GEN class for v3.1 + LS0
>    under a declared polynomial allocation" remains open for the shipped calibration. What is proved is the exact
>    reduction of delivery to one event and everything around it (below).
> 2. **Finding on a shipped component (calibration), reported not made** (METHOD_REQUIREMENTS.md B): if a failed
>    tier-1 grid construction froze the tier-1 pilot schedule (always a valid ≤ T₁-stage grid) instead of returning
>    `schedule_limit`, then P(no output) = 0 under the premises and P(Ŝ⁺ = S₀) → 1 on all three classes —
>    i.e. (T) holds for the patched method (Proposition F). HQ decides whether C-ENG takes it.
> 3. **Method requirement adopted for a not-yet-shipped component** (METHOD_REQUIREMENTS.md A.2, premise TDP-IMPL): the
>    e4 tie-aware fallback = W1-N3's reference algorithm TDP (its cost bound is needed for the resource lemma).
> 4. **New idealisation premises** (all class (d), flagged): IDEAL-W (unbounded words: the spec's `unsupported_size`
>    fires for any fixed word size), MACH (wall time/bytes proportional to operations/words; allocations succeed within
>    the declared memory; no external interruption), CONFIG (default 𝓗, polynomial certificate budget, fixed worker
>    count). CAL is NOT assumed.
> 5. Statement changes after lock R01 (REJECT → v2): target kept but not claimed; Ψ_n route demoted; snapping,
>    `validation_failed`, `non_progress` carried explicitly. Later (sweep/council): CONFIG restricted to the default 𝓗;
>    (O) restated in exact form; P1 and L2 S.3 labelled AUDITED (code reading).
> 6. Status words "PROVED-CHECKED" below follow the Wave 1C protocol definition (proof file + cross-family checks +
>    mid-point CONTINUE + sweep fixed + council passed); they apply to the reduction package only.

## 1. RESULT
**PARTIAL.** Every no-output path except `schedule_limit` is excluded (probability 0) under a declared polynomial
allocation; `schedule_limit` is reduced to an explicit three-part failure event of the tier-1 grid construction; grid
lemmas give sufficient conditions and an insertion bound; the residual open item (O) is stated exactly.
**Council PASSED in round 2** (Codex gpt-6.1-sol 9.0, Claude Opus 5.5 8.9; all six gates PASS for both). The pass
certifies the reduction package (P1–P5, C1–C2, F1, the statement of O), not the target (T).

## 2. Statement as proved (STATEMENT.md v2.2; proofs lemmas/L1–L5)
- **(P1) Inventory** (INVENTORY.md v2; AUDITED by code reading): every exit of `v3_fit` without estimates, with path:line and class.
- **(P2) Lemma R** (L1): within CONFIG and TDP-IMPL, for every valid input (n ≥ 3, raw p), seed and uniform realisation,
  operations, words, preflight bytes and the exact-branch preflight time are bounded by polynomials (explicit shapes,
  implementation constants). Sufficient allocation: `mem_gb` ≥ C[(n+p)² + Cert_M]/2³⁰, `hours` ≥ C[(n+p)p(n³+pn)log³(n+p) +
  (n+p)²p log³(n+p) + p²n² + p³ + Cert]/3600 (default 𝓗 only; Cert, Cert_M the declared certificate envelopes). Under MACH no resource path (preflight, escalation preflight, wall guard,
  OOM, allocation exception) fires.
- **(P3) Lemma S** (L2): on the classes (model G, n ≥ 3) the input/degenerate statuses have probability 0; under EX-A
  the scorer never fails (H_S, G_S + I positive definite; Q_S ≥ yᵀy/(n+1); the fallback Q formula is an exact identity);
  internal error sites are unreachable on the `v3_fit` call graph (AUDITED by code reading).
- **(P4) Theorem D** (L4; relative to the audits in P1/P3): 𝒰_n = 𝒮ℒ_n up to a null set, where 𝒮ℒ_n = {tier-0 trigger ⇒ escalation, and some tier-1 grid
  construction fails}; a construction fails iff (α) #intervals > T_e (pilot stages + appended bisection points),
  (β) `non_progress` (needs d-range on V > 2√c₀2⁶⁰ ≈ 7.48·10¹⁷; excluded for n ≤ 2.277·10⁸), or (γ) failed validation
  after the snap to 1. Hence P(𝒰_n) → 0 ⟺ P(𝒮ℒ_n) → 0.
- **(P5) Grid lemmas** (L3, L5): exact identity ρ_V(u,v) = q_u(M)q_{2v−u}(M)/q_v(M)² for every M ∈ V; Peano-kernel
  variance bound; pilot ≤ T_e strictly increasing stages ending at 1; dominance (one model ≥ √0.9 at t = 0 and 2) or
  sup Var < log(10/9) ⇒ no insertion and ≤ k intervals; two-model family with ε-remainder ⇒ ≤ 22 + ⌈log_{4/3}
  max{1, (−x₀ − λ_θ)/(2s_θ)}⌉ bisection trials (ε = 0.01), + ⌈log_{4/3}((1+η)/η)⌉ if the remainder is controlled only on
  [0, 1+η].
- **(C1) Conditional delivery**: P(𝒰_n) ≤ P(E_n ∩ ∪_{tier-1 constructions} (α) ∨ (β) ∨ (γ)) (E_n = a tier-0 trigger
  fires). No design sequence is known to satisfy the (P5) sufficient conditions; at the tested sizes they fail.
- **(C2) Joint consistency with the delivery term** (Corollary D′, pathwise, no CAL): P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − o(1) −
  P(𝒮ℒ_n) on LH, LH-iid, GEN (via W1-GEN (C1)+(C2), T03♯ and W1-PXN (T), (P), under their hypotheses; report statuses
  "PROVED-CHECKED"; the LH exact-Gram instance carries W1-GEN's instance-level input "SAME-FAMILY-ONLY").
- **(F1) Proposition F**: with the pilot-schedule fallback, P(𝒰_n) = 0 and P(Ŝ⁺ = S₀) → 1.
- **(O) Open (exact form)**: P(𝒮ℒ_n) → 0, i.e. P(E_n ∩ F¹_n) → 0 (E_n = a tier-0 trigger fires; F¹_n = a tier-1
  construction fails via (α)–(γ)). Sufficient routes: (O-a) P(E_n) → 0 (no tier-0 trigger w.p. → 1); (O-b) control of
  (α)–(γ) for the realised tier-1 candidate sets and pilot schedule jointly with the trigger (forced pilots attain
  k = T_e). The pilot stage count is the CJ06 / Conjecture P question. Neither a pilot bound alone nor endpoint posterior
  concentration suffices (R05).

## 3. Status per clause, with evidence
| clause | status | evidence |
|---|---|---|
| P1 inventory | AUDITED (code reading) by R01 (REJECT → fixes), R02, R05, R06, both council seats | INVENTORY.md v2; reviews/R01, R02, R06 |
| P2 Lemma R | PROVED-CHECKED (council round 2); R02 GAP → fixed; R05 MAJOR (TDP-IMPL) fixed; R06 MAJORs (CONFIG, concurrency, allocation success) fixed | lemmas/L1_resources.md; reviews/R02, R05, R06 dispositions |
| P3 Lemma S | S.1, S.2 PROVED-CHECKED; S.3 AUDITED (code reading); R02: S.1, S.2 survive; S.3 extended (R02 #5, R06 #13) | lemmas/L2_degenerate.md |
| P4 Theorem D | PROVED-CHECKED (relative to the P1/P3 audits); R04 VERIFIED-WITH-AMENDMENTS (applied); R05 CONTINUE | lemmas/L4_delivery.md; reviews/R04, R05 |
| P5 grid lemmas | PROVED-CHECKED; R03 (xhigh): 3.1, 3.2, 3.2′, 3.3, 3.5(a), 5.1 VERIFIED; others V-W-A; Cor 5.3 ERROR → fixed | lemmas/L3_grid.md, L5_insertions.md; reviews/R03 |
| C2 Corollary D′ | PROVED-CHECKED (pathwise argument supplied by R04; council round 2) | lemmas/L4_delivery.md |
| F1 Proposition F | PROVED-CHECKED for the patched calibration law (R04; council round 2) | lemmas/L4_delivery.md |
| O | OPEN | STATEMENT.md §3; L5 Remark 5.4 |
| numerics | (no fit escalated: tier 1 never reached, so the numerics bear on route (O-a), not (O-b)) production core, 80 fits: 80/80 completed, max 17 intervals vs T_e = 1000; N1; N2/N2b 0 violations; N3 replay 51/51 exact, two-model hypothesis not met at n ≤ 1600 (selected pair); N4 stress: 54 harder fits (3 masked pairs; strong links; weak signal) up to (3200,189): 54/54 completed, no escalation, max 39 intervals | numerics/SUMMARY_dlv.md, N1_psi_*.txt, N2_grid_lemmas.txt, N2b_pilot_and_counts.txt, N3_SUMMARY.md, N4_SUMMARY.md |

## 4. Review trail
- Statement lock R01 (Codex high): REJECT (1 FATAL scope, 7 MAJOR, 2 MINOR) → STATEMENT v2, all dispositioned.
- Lemma checks: R02 L1+L2 (Codex high) GAP → fixed; R03 L3+L5 (Codex xhigh) core VERIFIED, Cor 5.3 ERROR → fixed;
  R04 L4 (Codex high) VERIFIED-WITH-AMENDMENTS → applied.
- Mid-point R05 (fresh Codex xhigh, proofs only): CONTINUE (1 MAJOR, 2 MINOR, applied).
- Exhaustive sweep R06 (fresh Codex high): 0 FATAL, 4 MAJOR, 9 MINOR, 2 EDITORIAL — all fixed.
- CITECHECK: 160 citations, 0 missing; every cited range compared with its claim (reviews/CITECHECK.txt).
- Council round 1: Codex 7.6 (G1, G2, G3, G5 FAIL: uncosted custom-h branch of CONFIG; certificate terms dropped from
  the simplified allocation), Opus 8.6 (all PASS, 10 MINOR) — not passed; all findings fixed (reviews/C1_disposition.md).
- Council round 2 (fresh seats): **Codex 9.0, all PASS; Opus 8.9, all PASS → PASSED.** Remaining minors applied after
  the vote, no conclusion changed (reviews/C2_disposition.md).
- Not used: gpt-6-astra, Fable 5.1.

## 5. Open items and recommended next step
1. **(O)** — the probability of a failed tier-1 grid construction on the classes. Routes: (a) a particle-system bound on
   the pilot stage count (show some pilot step ≥ (N̄+1)/T_e w.h.p., which already gives k ≤ T_e − N̄); (b) a
   data-only remainder bound sup_{[0,1+η]} R_t ≤ ε plus candidate inclusion of the two models in every V; (c) a
   multi-model generalisation of Lemma 5.2 (N3 shows the two-model remainder is ≥ 0.08 at n ≤ 1600).
2. **Recommended:** adopt the fallback of Proposition F (one line in `v3_calibrate`, plus labelling), which makes delivery
   a theorem under the declared allocation and turns all reported-HPM results into unconditional P(Ŝ⁺ = S₀) → 1.
3. Implementation obligations unchanged: GUARD-W audit, merged-LS0 replay, TDP implementation (C-ENG).

## 6. Files produced (Theory_work/Wave1C/C-DLV/)
STATEMENT.md (v2.2), PLAN.md, LOG.md, INVENTORY.md (v2), METHOD_REQUIREMENTS.md, CHECKPOINT.md, REPORT.md;
lemmas/L1_resources.md, L2_degenerate.md, L3_grid.md, L4_delivery.md, L5_insertions.md;
numerics/: BRIEF_numerics.md, core_copy/ (+ hashes), run_dlv.R, dlv_lib.R, summarize.R, dlv_runs.csv,
dlv_constructions.csv, rds/, SUMMARY_dlv.md, psi_enum.py, N1_psi_{F,M}.{txt,json}, n2_grid_lemmas.py,
N2_grid_lemmas.txt, n2b_pilot_and_counts.py, N2b_pilot_and_counts.txt, n3_run.R, n3/, n3_twomodel.py, N3_twomodel.csv,
N3_SUMMARY.md, n4 files, citecheck.py;
reviews/: R01–R06 verbatim + dispositions, COUNCIL_BRIEF.md, C1_ and C2_council_{codex,opus}.md + dispositions,
CITECHECK.txt.

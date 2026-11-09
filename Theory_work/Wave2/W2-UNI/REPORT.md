# W2-UNI — REPORT to Theory HQ (design-agnostic main consistency theorem)

> **Flags (read first).**
> 1. **No method change.** All claims use the method as merged (v3.1, main 4676af6). The merged LS0 cap ℓ_n + |S̃₀| suffices
>    uniformly; admitted factor subclasses can require order-p deletion paths [R05a-6].
> 2. **Scope as locked (STATEMENT v1.1.4).** General theorems for k = 0 (any p ≤ n^A) and k = 1 (limsup log p/log n < α₀(κ̄)
>    = 1/(2κ̄(κ̄ + 2)); = 1/6 for every block compound symmetry). **k ≥ 2 and k = 1 beyond α₀ are not proved here**
>    (frontier: Lemma OBS-k + family-specific FAC-B; absorption plan for the parallel tickets).
> 3. Statement changes vs the brief (all logged; no hypothesis or conclusion of UNI-0/UNI-1 changed after the lock):
>    R01's eight lock changes (exact LSF; UNI-1 visibility via TV-pop / actual-block TV with PTV only sufficient; per-n
>    subset-exposure ratio instead of a uniform loading floor; corollary table corrections; OBS-k quantified); v1.1.1 R04's
>    editorial split of the PLR summary (C-i)/(C-ii); v1.1.2 sweep R05a (PLR scope stated — setting (R), fixed s₀, (A3)
>    coefficient bounds; LS0 move count qualified by its event; FAC-L containment restricted to its fixed-positive-beta-min
>    subclass, BM-∞ relaxation kept as a separate imported result); v1.1.3 sweep R05b (Not-claimed wording "Ψ outside
>    LOC_M"); v1.1.4 council NIT (status wording of PLR's source).
> 4. All results are asymptotic (binding scope rule).
> 5. Process: the ticket was paused by HQ mid-pipeline and **resumed by a new lead** (Claude Opus 5.5, Claude Work,
>    2026-11-09 ~14:45 CST), which finished the sweep, council, citation check and this report.

## 1. RESULT
**PROVED-CHECKED** — STATEMENT v1.1.4: Theorem UNI-0 (ii), Theorem UNI-1 (iii), reduction lemmas R1–R4 (metric toolkit,
UNI-0 engine inputs, key lemma U-LOC, Proposition F-UNI) and Lemma OBS-k (R5). UNI-P (i) and PLR (i′) are restated
from APP L1_POST and LOC2 L5 with their source statuses (inside "PROVED-CHECKED" tickets) and scopes. Council round 1
passed: Codex gpt-6-astra high **9.0** and Claude Opus 5.5 high **8.9**, all six gates PASS on both seats.

## 2. Headline for Felipe — the main theorem under general assumptions on X

**Assumptions (population-level; STATEMENT §2).**
* **(A1)** Gaussian rows (random design), p ≤ n^A; for the posterior a sparse eigenvalue floor on sets of size O(log n)
  (LSF; λ_max unrestricted).
* **(A2)** Σ = ΛΛᵀ + Ψ with a fixed number k of factors (pervasive loadings, λ_max(Σ) ≍ p allowed) and an idiosyncratic part
  Ψ that is **metric-local**: spectrum in [c, C] and |Ψ_jk| (or |(Ψ⁻¹)_jk|) ≤ K e^{−aδ(j,k)} for **some** pseudometric δ on
  the variables with polynomial growth (#{k : δ(j,k) ≤ r} ≤ C₀(1 + r)^{d₀}). The geometry is arbitrary (a line, sites in
  ℝ^d, a graph, or blocks; zero distances and distances below 1 allowed) and unrelated to the method's partition.
  For k = 1: a bounded subset-exposure ratio κ ≤ κ̄.
* **(A3)** fixed s₀, fixed beta-min, and non-masking (no truth's partial signal vanishes after conditioning on ≤ 15
  variables).

**Theorems.**
* **UNI-P (posterior, any k, any p ≤ n^A):** 1 − π(S₀) = O_P(√(log n/n)) under (A1) and the signal bounds of (A3), with no
  PTV needed. This is APP POST.
* **PLR (abstract engine; random design, fixed s₀ and beta-min):** a polylog relevance set, the sandwich, and NA-R
  references/atoms give D_n → 0. Adding LSF gives P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 (output-intersected). Unconditional
  reported-model consistency additionally uses F-UNI's delivery premises [R05b-1].
* **UNI-0 (k = 0, any p ≤ n^A, p ≫ n allowed):** Σ metric-local + (A3) give P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and P(Ŝ⁺ = S₀) → 1
  under the delivery premises (F-UNI) [R05b-1]. New: the abstract metric toolkit (Combes–Thomas under polynomial growth,
  conditional decay, ℓ¹ regression bounds, and the new ℓ¹-localisation lemma LOCL).
* **UNI-1 (k = 1, local Ψ, limsup log p/log n < α₀(κ̄)):** Σ = λλᵀ + Ψ with Ψ metric-local, κ ≤ κ̄, and visibility give the
  same conclusions. Visibility means TV-pop under (R) (sufficient: PTV) and TV on the actual blocks under (E) [C1-B NIT-5].
  NA/TL hold on the **full lattice**: every start maximiser contains S₀, and on Sand ∩ NA ∩ TL LS0 removes its extras by
  pure deletions [R05a-6].
  * **New key lemma U-LOC**: an exact Pythagorean split of the add statistic along the residual factor direction for
    **non-block** Ψ. The idiosyncratic innovation is controlled by p·n^{o(1)} local references plus atoms whose ℓ¹
    weight **vanishes** (LOCL). The factor term is controlled by an entropy-stratified union over all subsets (no
    independence needed).
  * Structurally this strictly contains FAC-A's class (Ψ block-diagonal), with the same exponent (κ = 1 ⇒ 1/6 for CS,
    block CS, S5). As theorems, UNI-1 contains the fixed-positive-beta-min subclass of FAC-L; FAC-L's fixed-design BM-∞
    relaxation remains a separate imported result [R05a-1].
* **Family results [C1-B MINOR-2].** Every family result listed in `lemmas/C_corollaries.md` (STATEMENT §5) is an instance,
  a separate extension, or a marked partial version:
  * UNI-0: iid, AR(1)/S2, bounded blocks/S1/S3/S4/S6, d-dimensional spatial sites.
  * UNI-1 (below 1/6): one factor + local blocks, CS, block CS, S5.
  * Partial versions beyond UNI-1: FAC-B (CS up to p ≤ n/2) and masked CS (FS′).
  * PLR, or its polynomial extension: LOC-BF and polynomial decay.

  GEN's masked-truth theorems (LH, LH-iid, W), PXN and FAC-L's BM-∞ relaxation remain separate imported results.

## 3. Statement as proved
`STATEMENT.md` v1.1.4. Version history: locked after R01; v1.1.1 = R04-1 editorial; v1.1.2 = R05a-1/2/5;
v1.1.3 = R05b-4; v1.1.4 = C1 NIT-3. Proof map:
| Claim | Proof file | Engine inputs |
|---|---|---|
| (i) UNI-P | APP `lemmas/L1_POST.md` (cited) | — |
| (i′) PLR | LOC2 `lemmas/L5_assembly.md` (cited) | — |
| R1 metric toolkit (CT_M, CD_M, RB_M, TAIL_M, LOCL, SC_M) | `lemmas/L1_metric.md` | LOC2 L3_CTd (model) |
| R2 / (ii) UNI-0 | `lemmas/L2_k0.md` | PLR, NA-R, LOC2 L4 Part A chain |
| R3 key lemma U-LOC | `lemmas/L3_ULOC.md` | L1_metric; FACA U(a)–(d) (model) |
| (iii) UNI-1 | `lemmas/L4_k1.md` | L3_ULOC; FACA L2–L5 |
| R4 Proposition F-UNI | `lemmas/L5_delivery.md` | FACA L7, LOC2 L7 |
| R5 OBS-k; frontier, absorption plan | `lemmas/L6_frontier.md` | — |
| Corollary table | `lemmas/C_corollaries.md` | sources' statements |

## 4. Status per clause (statuses verbatim; review files in reviews/)
Lemma files L1–L5 and Lemma OBS-k (L6) keep their header status "PROVED (by this seat, unchecked)" (the rest of L6 is a plan; C_corollaries is "assumption checks by this seat"). The ticket-level PROVED-CHECKED rests on the
checks listed here plus the mid-point, the sweeps and the council (§5).
| Clause | Status | Checks |
|---|---|---|
| L1_metric | PROVED (by this seat, unchecked) | R02 Sol high V-W-A (1 MINOR applied); numerics n1, n2; sweeps R05a/R05b; council C1 |
| L2_k0 (UNI-0) | PROVED (by this seat, unchecked) | R02 Sol high V-W-A (1 MINOR applied); falsification probe n4 (zero/small distances); sweeps; C1 |
| L3_ULOC (key) | PROVED (by this seat, unchecked) | R03 Sol xhigh V-W-A (1 MAJOR: T = ∅ for TL; fixed); numerics n3, n3b (exhaustive); sweeps; C1 (seat B re-checked (a)/(b) numerically, 0 violations) |
| L4_k1 (UNI-1) | PROVED (by this seat, unchecked) | R03 V-W-A (applied); sweeps; C1 |
| L5_delivery (F-UNI) | PROVED (by this seat, unchecked) | R03 V-W-A (applied); sweeps; C1 |
| L6 OBS-k | PROVED (by this seat, unchecked) | R03: VERIFIED; numerics n5; sweeps; C1 |
| C_corollaries | assumption checks (by this seat) | R04 mid-point (2 items fixed); sweeps R05a (5 items), R05b (2 items) fixed; C1 (1 item fixed) |

Inputs (verbatim):
* "PROVED-CHECKED": W2-LOC2, W2-FAC-B, W2-APP, C-GROW, W1-GEN. W2-FAC-A: "PROVED-CHECKED (for the narrowed, flagged target
  STATEMENT.md v1.2)".
* APP L1_POST: "PROVED (by this seat, unchecked)" (R02 V-W-A).
* LOC2 L5 (PLR): "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS.
* T03♯: "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)".
* M5(0): "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))".
* Inherited: e4/N3 "OPEN" (only "some maximiser" is used for consistency). As recorded in FACA `lemmas/L7_delivery.md`:
  S.3/P1 "AUDITED (code reading)".

## 5. Review trail
* **R01 statement lock** (Sol high): LOCK-WITH-CHANGES; 8/8 changes applied.
* **R02** (Sol high, L1/L2): V-W-A ×2.
* **R03 key lemma** (Sol xhigh, L3–L6): V-W-A ×4 (OBS-k VERIFIED); 1 MAJOR + 5 MINOR applied.
* **R04 independent mid-point** (fresh Sol xhigh): **CONTINUE**; 1 MAJOR, 2 MINOR, 1 NIT, all applied [R05a-18].
* **Sweep R05a** (Codex Sol xhigh, pre-pause, kept as an extra layer): FATAL 0 / MAJOR 1 / MINOR 14 / NIT 3; all 18 fixed
  (reviews/R05a_disposition.md).
* **Exhaustive sweep R05b** (fresh Codex gpt-6-astra, high): VERIFIED-WITH-AMENDMENTS at the proof level; FATAL 0 /
  MAJOR 0 / MINOR 10 / NIT 3; all 13 fixed (reviews/R05b_disposition.md).
* **Council round 1** (fresh, independent, high):
  * seat A, Codex gpt-6-astra: G1–G6 PASS, **9.0** (reviews/C1_council_astra.md);
  * seat B, Claude Opus 5.5 on claude-personal: G1–G6 PASS, **8.9** (reviews/C1_council_opus.md).

  **PASSED in round 1.** The non-blocking items were applied after the vote (2 MINOR from A; 3 MINOR + 6 NIT from B).
  B's sharpening κ → κ_J was deliberately not incorporated (see §7) (reviews/C1_disposition.md).
* **CITECHECK** (citecheck.py v2.1 → reviews/CITECHECK.txt, final run after all edits):
  * 131 path:line citations: 0 existence/range misses; one explicit rule-based resolution each, no fallback.
  * 0 self-citation content failures: every citation of this STATEMENT is content-asserted.
  * 19 claim-specific tokens: 0 misses.
  * 67 quoted status occurrences: 0 misses (extracted automatically, verbatim and word-bounded in the attributed source).
  * Manual content audit of every entry (reviews/CITECHECK_AUDIT.md, separate auditor seat Claude Sonnet 5.5 high):
    127 citations: 124 MATCH / 3 PARTIAL / 0 MISMATCH. 67 status occurrences: 66 ATTACHED / 1 NOT-ATTACHED.
    All 4 required fixes, plus the advisory FAC-A-qualifier item, were applied. The 4 citations added by those fixes
    were checked by the lead (addendum in the audit file).
* **Seats and effort:**
  * R03, R04 and R05a ran at xhigh **before** the binding effort cap (protocol commit a5c2688, 2026-11-09 14:32 CST);
    every review after resumption (R05b, C1 A/B, the citation audit) ran at high [C1-B NIT-4].
  * The parallel prover (Claude Opus 5.5 subagent) authored L1_metric and L2_k0, which were checked cross-family (R02).
  * Numerics helpers after resumption: Claude Sonnet 5.5 high on Claude Work (n4, two passes).

## 6. Why the assumptions are mild and standard (justification, not a claim)
* **(A1)** Gaussian rows with polynomial dimension and a floor on sparse eigenvalues of the population correlation:
  * This is the random-design setting of the Wave-1/1C posterior theory (T03♯ via APP POST).
  * The floor is on sets of size O(log n) only and λ_max may diverge, which is weaker than bounded-spectrum assumptions.
  * Its role parallels the identifiability condition of Song–Liang (Condition 3), descriptively and without an ordering
    of assumption classes (`Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md` row 9).
* **(A2)** is an approximate factor model in the sense of Fan–Liao–Mincheva (2013) / Fan–Ke–Wang (2020): a low-rank common
  component plus an idiosyncratic part. The idiosyncratic sparsity is replaced by **additional sufficient structure**:
  exponential decay along an arbitrary geometry of polynomial growth (bandable/spatial/graph classes).
  * Examples covered:
    * stationary AR/ARMA with roots uniformly outside the unit circle;
    * covariance or precision of fixed bandwidth with uniform spectral bounds;
    * block-diagonal with bounded blocks;
    * spatial fields on ℤ^d or on separated sites, with exponential decay;
    * GMRFs whose precision has fixed range or uniformly exponential decay on a polynomial-growth geometry, with uniform
      spectral bounds. Bounded spectrum alone is not enough [R05b-3].
  * For k = 1 the subset-exposure ratio κ is an additional representation-dependent sufficient condition. It excludes zero
    loadings and allows a vanishing common loading scale. It controls every subset and is not equivalent to average
    pervasiveness: neither condition implies the other [R05b-2].
  * For k = 0 the LOC_M spectral bounds and decay, polynomial dimension, and PTV suffice. No prescribed ordering or relation
    to the method's partition is required. The bound λ_max(Σ_n) ≤ C is part of LOC_M [R05a-3].
* **(A3)** Fixed sparsity and beta-min are the standard selection-consistency signal conditions.
  * PTV ("no truth masked by conditioning on ≤ 15 variables") is the partial-correlation analogue of Song–Liang's
    Condition 5 |cov(x_t, y)| > 0 (SONG_LIANG_MAP row 12). It is automatic when truths sit in mutually independent groups.
  * Masked truths are handled only by family results (PXN, FAC-B (FS′)).
* **What is not mild:** the k = 1 exponent α₀(κ̄) can be small for heterogeneous signed loadings.
  * Exhaustive numerical estimates [C1-A2] for the four p = 10 designs of N3b give κ = 3.3–7.3, so α₀ = 0.0074–0.0284. These
    are illustrations, not bounds for any growing-p class [R05a-14].
  * 1/6 is reached for (block) compound symmetry.
  * For exact CS above 1/6, SHARP rules out full-lattice NA, while FAC-B supplies a path proof.
  * Necessity of α₀(κ̄) for other representations, and exclusivity of a path approach, have not been established [R05a-4].

## 7. Open items / next steps
1. **Sharper exposure ratio (suggested by council seat B; unchecked).** Replace κ = κ′/√c_𝒢 by the joint ratio
   κ_J := max{1, sup_{∅≠T, l∉T} κ′_{l,T}√(h_𝒢(T)/s_T)} ≤ κ.
   * Argument: in U-LOC(b), κ′_{l,T}√s_T|F_T|/(1 + s_T) ≤ [κ′_{l,T}√(h/s_T)]·|F_T|/√h ≤ κ_J√(2x_h/h) on E_F, and FACA L3.1
     then runs with κ̄ ≥ κ_J.
   * Gain: seat B's exhaustive p = 9 examples go from κ = 6.09 to κ_J = 3.61 (α₀ 0.0101 → 0.0247); κ_J = κ for (block) CS
     (`reviews/C1_scratch_opus/joint.py`).
   * Not incorporated: it would strengthen a statement that is locked, swept and council-passed. Next step: a lemma check
     plus a numerical probe, then a statement amendment (HQ decides).
2. **k = 1 beyond α₀ under general (A2):** the path route. Parallel tickets S5/S5F (block CS) and X/XA (iid CS, general
   loadings) would supply the first general pieces (L6 absorption table).
3. **k ≥ 2:** OBS-k shows that a uniform subset-information floor on fixed-size subsets is impossible. A direction-sensitive
   bound or the path is needed (FAC-K2).
4. **p > K_n in UNI-1:** FAC-PK/PKA.
5. Non-Gaussian rows, growing s₀, and masked truths in general.
6. **Paper:** state (A1)–(A3) and Theorems UNI-P, PLR, UNI-0 and UNI-1 in the main text; move the family results to a
   corollary table/examples (C_corollaries.md).

## 8. Files
* Top level: STATEMENT.md, PLAN.md, LOG.md, CHECKPOINT.md, REPORT.md, citecheck.py.
* lemmas/: L1_metric.md, L2_k0.md, L3_ULOC.md, L4_k1.md, L5_delivery.md, L6_frontier.md, C_corollaries.md.
* numerics/:
  * n1_metric.py (+ n1_out.txt);
  * n2_metric.py (+ n2_metric_out.txt);
  * n3_uloc.py (+ n3_out.txt);
  * n3b_exhaustive.py (+ n3b_out.txt);
  * n4_r2_pseudo.py (+ n4_r2_pseudo_out.txt, _out_n8000.txt, _results.csv, _results_n8000.csv, _summary.txt);
  * n5_obsk.py (+ n5_obsk_out.txt).
* reviews/:
  * R01–R04, R05a_sweep_sol.md, R05b_sweep_astra.md, C1_council_astra.md and C1_council_opus.md, each with its disposition;
  * scratch folders C1_scratch_astra/ and C1_scratch_opus/;
  * CITECHECK.txt, CITECHECK_excerpts.md, CITECHECK_AUDIT.md.

Nothing committed (HQ commits); no files outside this folder were modified by this ticket.

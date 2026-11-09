# W2-UNI — REPORT to Theory HQ (design-agnostic main consistency theorem)

> **Flags (read first).**
> 1. **No method change.** All claims use the method as merged (v3.1, main 4676af6); the merged LS0 cap ℓ_n + |S̃₀| is used
>    essentially in UNI-1 (start mode ≈ [p]).
> 2. **Scope as locked (STATEMENT v1.1.1).** General theorems for k = 0 (any p ≤ n^A) and k = 1 (limsup log p/log n < α₀(κ̄)
>    = 1/(2κ̄(κ̄ + 2)); = 1/6 for every block compound symmetry). **k ≥ 2 and k = 1 beyond α₀ are not proved here**
>    (frontier: Lemma OBS-k + family-specific FAC-B; absorption plan for the parallel tickets).
> 3. Statement changes vs the brief (all logged): R01's eight lock changes (exact LSF; UNI-1 visibility via TV-pop /
>    actual-block TV with PTV only sufficient; per-n subset-exposure ratio instead of a uniform loading floor; corollary
>    table corrections; OBS-k quantified); R04's editorial split of the PLR summary (C-i)/(C-ii).
> 4. All results are asymptotic (binding scope rule).

## 1. RESULT
**[pending sweep R05 and council]** — target: PROVED-CHECKED for STATEMENT v1.1.1 claims (i), (i′), (ii), (iii), R1–R5.

## 2. Headline for Felipe — the main theorem under general assumptions on X

**Assumptions (population-level; STATEMENT §2).**
* **(A1)** Gaussian rows (random design), p ≤ n^A; for the posterior a sparse eigenvalue floor on sets of size O(log n)
  (LSF; λ_max unrestricted).
* **(A2)** Σ = ΛΛᵀ + Ψ with a fixed number k of factors (pervasive loadings, λ_max(Σ) ≍ p allowed) and an idiosyncratic part
  Ψ that is **metric-local**: spectrum in [c, C] and |Ψ_jk| (or |(Ψ⁻¹)_jk|) ≤ K e^{−aδ(j,k)} for **some** pseudometric δ on
  the variables with polynomial growth (#{k : δ(j,k) ≤ r} ≤ C₀(1 + r)^{d₀}). The geometry is arbitrary — a line, sites in
  ℝ^d, a graph, or blocks — and unrelated to the method's partition. For k = 1: a bounded subset-exposure ratio κ ≤ κ̄.
* **(A3)** fixed s₀, beta-min, and non-masking (no truth's partial signal vanishes after conditioning on ≤ 15 variables).

**Theorems.**
* **UNI-P (posterior, any k, any p ≤ n^A):** 1 − π(S₀) = O_P(√(log n/n)) under (A1)+(A3). (= APP POST.)
* **PLR (abstract engine):** polylog relevance set + sandwich + NA-R references/atoms ⇒ D_n → 0; + LSF ⇒ reported-model
  consistency.
* **UNI-0 (k = 0, any p ≤ n^A, p ≫ n allowed):** Σ metric-local + (A3) ⇒ the reported HPM equals S₀ w.p. → 1 (with output;
  and P(Ŝ⁺ = S₀) → 1 under the delivery premises). New: the abstract metric toolkit (Combes–Thomas under polynomial growth,
  conditional decay, ℓ¹ regression bounds, and the new ℓ¹-localisation lemma LOCL).
* **UNI-1 (k = 1, local Ψ, limsup log p/log n < α₀(κ̄)):** Σ = λλᵀ + Ψ with Ψ metric-local, κ ≤ κ̄, visibility (TV-pop;
  sufficient: PTV) ⇒ the same conclusions, with NA/TL on the **full lattice** and the start mode ⊆ [p] reduced by pure
  deletions. **New key lemma U-LOC**: exact Pythagorean split of the add statistic along the residual factor direction
  for **non-block** Ψ; the idiosyncratic innovation is controlled by p·n^{o(1)} local references plus atoms whose ℓ¹ weight
  **vanishes** (LOCL); the factor term by an entropy-stratified union over all subsets (no independence needed). This
  strictly contains FAC-A's class (Ψ block-diagonal), with the same exponent (κ = 1 ⇒ 1/6 for CS, block CS, S5).
* **Every existing family result is an instance or a marked partial version** (§4): iid, AR(1)/S2, banded/ARMA, bounded
  blocks/S1/S3/S4/S6, d-dimensional spatial grids → UNI-0; one factor + local blocks, CS, block CS, S5 → UNI-1 (below 1/6);
  FAC-B (CS up to p ≤ n/2) and masked CS (FS′) → partial versions beyond UNI-1; LOC-BF and polynomial decay → PLR /
  its polynomial extension.

## 3. Statement as proved
`STATEMENT.md` v1.1.1 (locked after R01; v1.1.1 = R04-1 editorial). Proof map:
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
| Clause | Status | Checks |
|---|---|---|
| L1_metric | PROVED (by this seat, unchecked) | R02 Sol high V-W-A (1 MINOR applied); numerics n1, n2 |
| L2_k0 (UNI-0) | PROVED (by this seat, unchecked) | R02 Sol high V-W-A (1 MINOR applied) |
| L3_ULOC (key) | PROVED (by this seat, unchecked) | R03 Sol xhigh V-W-A (1 MAJOR: T = ∅ for TL; fixed); numerics n3, n3b (exhaustive) |
| L4_k1 (UNI-1) | PROVED (by this seat, unchecked) | R03 V-W-A (applied) |
| L5_delivery (F-UNI) | PROVED (by this seat, unchecked) | R03 V-W-A (applied) |
| L6 OBS-k | PROVED (by this seat, unchecked) | R03: VERIFIED |
| C_corollaries | assumption checks (by this seat) | R04 mid-point (2 items fixed), sweep |
Inputs (verbatim): W2-LOC2, W2-FAC-A ("PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)"), W2-FAC-B, W2-APP,
C-GROW, W1-GEN "PROVED-CHECKED"; APP L1_POST "PROVED (by this seat, unchecked)" (R02 V-W-A); T03♯ "PROVED; SF VERIFIED
(W2-VT03R); XF VERIFIED (A-REV2)"; M5(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; inherited: e4/N3 "OPEN"
(only "some maximiser" used for consistency), S.3/P1 "AUDITED (code reading)".

## 5. Review trail
R01 statement lock (Sol high): LOCK-WITH-CHANGES, 8/8 applied. R02 (Sol high, L1/L2): V-W-A ×2. R03 key lemma (Sol xhigh,
L3–L6): V-W-A ×4 (OBS-k VERIFIED), 1 MAJOR + 5 MINOR applied. R04 independent mid-point (fresh Sol xhigh): **CONTINUE**
(1 MAJOR editorial + 3 minor, applied). R05 sweep: [pending]. Council: [pending]. CITECHECK: reviews/CITECHECK.txt — 107
path:line citations, 0 misses; 12 tokens, 0; 12 statuses, 0 (ambiguous resolutions checked manually).
Parallel prover (Claude Opus 5.5 subagent) authored L1_metric and L2_k0; checked cross-family (R02). Astra/Fable: not used.

## 6. Why the assumptions are mild and standard (justification, not a claim)
* **(A1)** Gaussian rows with polynomial dimension and a floor on sparse eigenvalues of the population correlation is the
  random-design setting of the Wave-1/1C posterior theory (T03♯ via APP POST); the floor is on sets of size O(log n) only and
  λ_max may diverge — weaker than bounded-spectrum assumptions; its role parallels the identifiability condition of
  Song–Liang (Condition 3), descriptively and without an ordering of assumption classes (`Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md` row 9).
* **(A2)** is an approximate factor model in the sense of Fan–Liao–Mincheva (2013) / Fan–Ke–Wang (2020) — low-rank common
  component + idiosyncratic part — with the idiosyncratic sparsity replaced by **additional sufficient structure**:
  exponential decay along an arbitrary geometry of polynomial growth (bandable/spatial/graph classes; covers AR/ARMA,
  banded covariance or precision, block-diagonal, spatial fields on ℤ^d or separated sites, GMRFs with bounded spectrum).
  For k = 1 the subset-exposure ratio κ is an additional representation-dependent sufficient condition (it excludes zero
  loadings; it is stronger than average pervasiveness; a vanishing common loading scale is allowed). For k = 0 nothing
  beyond locality is needed: no condition on λ_max, on the ordering, or on the method's partition.
* **(A3)** fixed sparsity and beta-min are the standard selection-consistency signal conditions; PTV ("no truth masked by
  conditioning on ≤ 15 variables") is the partial-correlation analogue of Song–Liang's Condition 5 |cov(x_t, y)| > 0
  (SONG_LIANG_MAP row 12), automatic when truths sit in mutually independent groups; masked truths are handled only by
  family results (PXN, FAC-B (FS′)).
* What is **not** mild: the k = 1 exponent α₀(κ̄) can be small for heterogeneous signed loadings (κ ≈ 3–7 ⇒ α₀ ≈ 0.007–0.03
  in our probes); 1/6 is reached for (block) compound symmetry. Beyond α₀ only the path route works (FAC-B for CS).

## 7. Open items / next steps
1. **k = 1 beyond α₀ under general (A2)**: path route; parallel tickets S5/S5F (block CS), X/XA (iid CS, general loadings)
   would supply the first general pieces (L6 absorption table). 2. **k ≥ 2**: OBS-k shows a naive uniform subset-information
   floor is impossible; a direction-sensitive bound or the path is needed (FAC-K2). 3. **p > K_n** in UNI-1 (FAC-PK/PKA).
4. Non-Gaussian rows, growing s₀, masked truths in general. 5. **Paper:** state (A1)–(A3), Theorems UNI-P, PLR, UNI-0, UNI-1
   in the main text; move the family results to a corollary table/examples (C_corollaries.md).

## 8. Files
STATEMENT.md, PLAN.md, LOG.md, CHECKPOINT.md, REPORT.md, citecheck.py; lemmas/L1_metric.md, L2_k0.md, L3_ULOC.md, L4_k1.md,
L5_delivery.md, L6_frontier.md, C_corollaries.md; numerics/n1_metric.py (+n1_out.txt), n2_metric.py (+n2_metric_out.txt),
n3_uloc.py (+n3_out.txt), n3b_exhaustive.py (+n3b_out.txt); reviews/R01–R04 (+ dispositions), CITECHECK.txt.
Nothing committed (HQ commits); no files outside this folder were modified.

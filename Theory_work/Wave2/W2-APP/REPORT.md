# W2-APP — REPORT (applicability map)

**RESULT: PROVED-CHECKED** — council round 3 PASSED (Codex gpt-6.1-sol xhigh 9.1, Claude Opus 5.5 high 9.1, all six gates
PASS in both seats; rounds 1 and 2 not passed: Sol 8.2 / Opus 8.8, Sol 8.8 / Opus 8.9, with Sol gate failures on the
map's enumeration frontier, fixed). Post-council edits are editorial/status-sync only (§6) — the applicability map (Part 1) with its new results (Lemma POST,
Lemma CT/CD, Theorem LOC + variant LOC-B, Lemma VN, family map) and the real-design classification (Part 2).
No method requirement: the shipped v3.1 LS0 cap ℓ_n + |S̃₀| (main 4676af6) is what Theorem LOC uses.
Statement changes vs the brief: R01's lock changes, the LOC-B enlargement qualification (R03), and the post-council-r1
ENUM addition (STATEMENT v1.3.1; see §2).

## 1. Headline (for Felipe)
* **Posterior level holds for essentially every standard design family**, including equicorrelation, strong factor
  models and long memory: the only design condition is a fixed positive floor of the population correlation matrix on
  sets of logarithmic size (λ_max may diverge). Random design, p ≤ n^A incl. p ≫ n, joint law; rate √(log n/n).
* **Reported model (the method's output) is proved consistent jointly with output — under the named implementation
  premises (EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, complete scans, IND-T/c₄ when R′ > 4, emitted LS0 centre a maximiser of
  γ₀), with no delivery claim [C1-Opus-3] — for all *local* designs** — iid, AR(1), ARMA-type
  Toeplitz with exponential decay, fixed-bandwidth banded covariance or precision, block-diagonal with bounded blocks
  of any size (incl. > 16), equicorrelated blocks with ≤ one truth per block growing up to ≈ (1 − δ₀) log n/s₀ (LOC-B, incl. its
  post-enlargement bound) [R07-2] — under one signal condition, PTV (no truth masked by conditioning on ≤ 15 variables;
  automatic with ≤ one truth per independent block). No condition
  on the method's partition. The study's S1–S4, S6 are covered (S1/S3/S4/S6 also by GEN with the production cap).
* **Small p (any correlation structure with POST's sparse floor LSF) [C3-Opus-2]:** whenever the coded exact-branch inequality (EXB) Σ_{k≤K}C(p,k) ≤ (5H₀ + 4N₀)p holds eventually — sufficient:
  2^{p_n} ≤ 4n·p_n, e.g. fixed p or p_n ≤ c log n with c < 1/log 2 — the method enumerates all models and the reported
  model is consistent by the posterior result alone (new Lemma ENUM, lemmas/L6_ENUM.md) [C1-Sol-1, C2-Sol-1]. All
  "unproved"/"obstructed" labels below refer to sequences off that branch.
* **Bounded condition number alone is not enough for any current reported-model proof** (STAR counterexample:
  condition number 3, start mode provably contains at least n^{1/3} − O(1) nulls in the stated STAR sequence) [R07-21]. The key general statement is: bounded spectrum
  ⇒ posterior consistency; bounded spectrum + exponential locality along some ordering + PTV ⇒ reported-model
  consistency.
* **Pervasive correlation** [R07-3]: under Lemma VN's quantified floors — fixed equicorrelation with coefficient sum |Σ_kθ*_k| ≥ θ̄₀ > 0;
  one-factor with loadings ≥ b₀ on a null set 𝒩_n, weighted exposure |b_{S₀}ᵀθ*| ≥ β₀ and an idiosyncratic floor;
  equicorrelated blocks of size g_n with ≤ one truth each — the GEN route is provably blocked once the visible-null set
  diverges, and the GROW/LOC route once min(K, |𝒩_n|)/log n → ∞ (e.g. p/log n → ∞, resp. g_n/log n → ∞): the start mode
  fills with visible nulls (for sequences off the exact branch). In a Python component port of the method (not production runs), LS0 nevertheless reached
  S₀ in 40/40 runs of these examples (24 with complete scans and a certified endpoint; 16 with a screened search whose
  certification flag is not a complete-scan certificate) and in 12/12 cancellation controls [R07-11, -15; C1-Sol-3].
  So the obstruction is to the proof routes; whether the method itself is consistent on pervasive designs is
  **unproved** (the simulations are observations only) [C1-Opus-1]; FAC status (verbatim, synced after council r3 [C3-Sol-1]): W2-FAC-A "PROVED-CHECKED" (for its narrowed, flagged target: Theorem FAC-L — one global factor + bounded-size local blocks, class 𝔉(γ̄, ψ₀, κ̄), limsup log p/log n < α₀(κ̄) = 1/(2κ̄(κ̄+2)), = 1/6 for every block compound symmetry incl. CS and S5; iid-row version (L5) under (TV-pop); CS instances need (GC-CS), which fails at a = 1/2; W2-FAC-A/REPORT.md:20-24, :29-53) — so compound symmetry, block compound symmetry and
  study S5 ARE covered for p up to n^{1/6−}; the general factor / p ≤ n^A target remains open; W2-FAC-B: provisional
  (no final status at sync time).
* **Real designs:** of 8 public designs, spam / digits / diabetes-quadratic are local (resemble the covered class;
  digits is an image; growing 2-D grids are outside LOC's proved scope), riboflavin / FRED-QD / FRED-MD are pervasive-factor
  (posterior class; reported model for growing-p models: FAC-A's class where it applies, otherwise open), iclaims is a one-factor design with fixed
  p = 10 (exact branch: covered by ENUM + POST) [C2-Opus-2], tecator (NIR spectra) is extremely near-collinear
  (λ_min = 1.7e-11): its appropriate asymptotic model (fixed design vs refined grid) is not decided here [R07-4, -7]. With p FIXED, every one of the 8 designs is eventually on the exact branch
  (ENUM + POST, given a positive population floor and an iid-Gaussian-row model); the local/pervasive classification
  matters for growing-p models of them [C3-Opus-1].
  All design-only and descriptive: a single design cannot confirm or refute membership of an asymptotic class, and
  "resembles" refers to the correlation pattern only — the theorems assume iid Gaussian rows, which none of these
  data sets has (counts, pixels, polynomial terms, serially dependent macro series) [C2-Opus-3].

## 2. Statement as proved
`STATEMENT.md` v1.3.1 (locked after R01; v1.2 = R03 item 1; v1.2.1 = R07 #1, same bound in (E)(f); v1.3/v1.3.1 = claim (F)
Lemma ENUM added after council round 1 and restated with the coded inequality after round 2 — a substantive addition). Changes vs the brief's wording, with reasons: the
growing-block, factor and MIS entries are conditional (R01 items 6, 7, 9); the small-log growing-block regime is
covered by the new variant LOC-B (R01 item 6 counterexample to "open"); LOC-B requires the post-enlargement bound
|Q ∖ S₀| ≤ (1 − δ₀) log n (R03 item 1). Signal-dependent conditions are never claimed to hold for a family; every
table entry separates (Σ) / (θ) / (T).

## 3. Applicability table
Legend: **holds** = hypotheses verified for the family (random design, joint law); **covered under X** = the
reported-model theorem applies when the added signal condition X holds (plus the named implementation premises; no
delivery claim); **obstructed** = the route's own conclusion is false w.p. → 1 (Lemma VN) — a statement about the
proof route, not the method; **unproved** = neither covered nor obstructed; **cited** = existing result, status
verbatim. Full entries, hypotheses and examples: `lemmas/L4_families.md` (v2).

| Family (Σ) | Posterior: T03♯ hypotheses (R, SE_λ(j₀), SE_w, BM) | GEN (H1)/(H2)/(C1′) | GROW (G1)–(G4) | LOC / LOC-B (new) | Reported model | Lemma / check |
|---|---|---|---|---|---|---|
| (a) iid | holds (φ = 1) | study S1 (cited, PROVED-CHECKED) | — | LOC; PTV automatic | **covered** | L1 (R02), L3 (R03), GEN (C5)(d) |
| (b) any Σ, spectrum ⊂ [c, C] | **holds** (any p ≤ n^A) | not implied; STAR obstructed | not implied; STAR obstructed | Σ ∈ LOC (exp. decay along some ordering) ⇒ Theorem LOC | covered under exp. locality + PTV; STAR-type: route-obstructed | L1, L3, L5 V1 (R04) |
| (c) AR(1), fixed 0 < \|ρ\| < 1 | holds | study S2 outside GEN's class (cited) | (C5)(c) under separation (6.0) (cited, PROVED-CHECKED) | LOC | covered under (6.0) / PTV | GROW L6, L3 |
| (c) Toeplitz, exp. decaying γ, spectral density ∈ [m, M] (e.g. ARMA) | holds | — | — | LOC | covered under PTV | L4 F1, L2 (R02), L3 |
| (c) Toeplitz, two-sided polynomial tail \|γ(h)/γ(0)\| ≥ c′h^{−β} (incl. long memory), density ≥ m | holds | — | — | Σ ∉ LOC once p → ∞ (L4 (c) counting argument); a polynomial UPPER envelope alone does not exclude LOC | **unproved** off the exact branch; covered by ENUM when (EXB) holds eventually | L4 F1, L1, L6 |
| (d) banded Σ or Σ⁻¹ (fixed bandwidth), spectrum ⊂ [c, C] | holds | — | — | LOC | covered under PTV | L2 §2.3, L3 |
| (e) block-diagonal, bounded blocks (any g), spectral floor | holds | study S1/S3/S4/S6 (cited); LH-iid raw-slope masking: PXN (cited) | — | LOC; PTV automatic with ≤ 1 truth/block, can fail otherwise | covered under PTV; masked LH-iid via PXN | L4 F2–F3, L3 |
| (f) equicorrelated blocks, size g_n → ∞, fixed ρ, ≤ 1 truth per block | holds | obstructed | sandwich obstructed if g_n/log n → ∞ | LOC-B if s₀(g_n − 1) ≤ (1 − δ₀) log n and post-enlargement bound | covered (LOC-B); covered by ENUM when (EXB) holds eventually; **unproved** otherwise unless g_n/log n → ∞ (route-obstructed) | L3 §3.8B (R03), L5 V2, L6 |
| (g1) equicorrelation, fixed ρ ∈ (0,1) | holds (floor 1 − ρ) | obstructed if \|Σ_kθ*_k\| ≥ θ̄₀ > 0, p → ∞ | obstructed if \|Σ_kθ*_k\| ≥ θ̄₀ > 0, p/log n → ∞ | Σ ∉ LOC once p → ∞ | **covered by FAC-A (cited, PROVED-CHECKED) for limsup log p/log n < 1/6 under (GC-CS)/(TV-pop)**; beyond: open; ENUM on the exact branch; Σ_kθ*_k = 0: no claim | L5 V3, L6 |
| (g3) factor models, fixed correlation floor (e.g. study S5: floor 0.3) | holds | obstructed under V4 exposure floors, \|𝒩\| → ∞; S5: GEN excludes (cited) | obstructed under V4 floors, min(K,\|𝒩\|)/log n → ∞; S5: frontier (cited) | can be LOC (decaying loadings) | FAC-A for one factor + bounded blocks, κ ≤ κ̄, limsup log p/log n < α₀(κ̄) (S5 incl., α₀ = 1/6); covered if local + PTV; ENUM on the exact branch; otherwise open | L5 V4, L4 (g), L6 |
| any family on which (EXB) holds eventually (sufficient 2^{p_n} ≤ 4np_n: fixed p, p_n ≤ c log n with c < 1/log 2, …) | holds under LSF | — | — | — | **covered** by exact enumeration + POST (Lemma ENUM) | L6 (council r2) |
| MIS (omitted variables) | — | — | — | — | AR(1): Prop. P(d) (one active omission, marginal precision); bounded blocks: projected support inside omitted blocks (L4 F4, raw-slope model); general banded precision, factor: no claim | L4 F4, C-MIS |

**Role of make_blocks.** LOC/LOC-B/VN: none (any X-measurable partition with blocks ≤ 16). GEN (S1/S3/S4/S6): actual
blocks contain whole groups (proved there). PXN: SIZE and partition recovery. In real pervasive designs most strong
pairs are split across blocks (riboflavin 99.5%) — a descriptive observation; the VN obstruction is proved only for the
quantified models V1–V4 [C1-Opus-4].

**Proof limitation vs necessary.** Necessary *for the routes*: STAR, growing blocks ≫ log n, equicorrelation/factor
with exposed signal (VN, checked R04). Not shown necessary for the method (component-port numerics: LS0 succeeded in 40/40 runs
of these examples and 12/12 controls, `numerics/LEAD_READING.md`). Unproved, no GROW/LOC-route obstruction known (and only for sequences off the exact branch, i.e. (EXB) failing infinitely often) [C1-Opus-6]: polynomial-decay/long-memory Toeplitz; growing
blocks where a LOC-B bound fails but g_n/log n does not diverge; masked truths outside LH-iid; growing d ≥ 2 spatial neighbourhoods
(e.g. refined image grids); non-Gaussian rows. Design-class question left open: whether densely refined smooth-curve
designs have vanishing sparse floors (then they would be outside every fixed-floor class) [R07-4].

## 4. Part 2 — real designs (`EMPIRICAL.md`; data_diag/)
| design | n × p | pattern | resembles | key numbers |
|---|---|---|---|---|
| spam | 4601 × 57 | local: one cluster of ≈ 11–12 correlated variables plus isolated pairs | (a)/(e) local class | φ²(k) ∈ [0.003855, 0.003934] for k ≥ 2 |
| digits | 1797 × 61 | local pixel neighbourhoods (image) | local; growing 2-D grids outside LOC's proved scope | φ²(8) ∈ [0.050, 0.055] |
| diabetes (quadratic, Efron et al.) | 442 × 64 | local clusters, near-collinear | (e) with small floor | φ²(3) = 0.012 exact; λ_min = 3.6e-7 |
| iclaims | 456 × 10 | one factor (83%), fixed small p | (g) pattern; fixed p = 10 → exact branch: ENUM + POST | λ_min = 0.064 |
| riboflavin | 71 × 4088 | pervasive factor + dense | (g): POST class; growing-p models: FAC-A class if one factor + bounded blocks | median 982 partners > 0.5; 99.5% strong pairs split across blocks |
| FRED-QD / FRED-MD | 257 × 170 / 775 × 99 | factor + tight local clusters | (g)+(e) | φ²(3) = 1.9e-5 / 9.1e-5 exact |
| tecator | 215 × 100 | smooth curves, extreme near-collinearity | not decided (depends on the asymptotic model) | λ_min = 1.7e-11; φ²(3) = 4.1e-9 |
Design-only; observed sample eigenvalues (exact / upper / lower bounds as labelled), not the population φ₀²; signal
conditions not checkable; plug-in numbers labelled in data_diag/SUMMARY.md (with the lead erratum at its end).

## 5. Status per clause with evidence
| Item | Status | Evidence |
|---|---|---|
| L1 POST | PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied | reviews/R02_*, numerics/post_check_out.txt |
| L2 CT, CD | PROVED (by this seat, unchecked); R02 VERIFIED (1 NIT applied) | reviews/R02_*, numerics/ct_check_out.txt |
| L3 Theorem LOC (key) | PROVED (by this seat, unchecked); R03 Sol xhigh VERIFIED-WITH-AMENDMENTS, applied | reviews/R03_*, numerics/n1, n2 |
| L3 LOC-B | as above; target gap (enlarged-Q bound) fixed in STATEMENT v1.2 | reviews/R03_* |
| L5 VN (+V1–V4) | PROVED (by this seat, unchecked); R04 VERIFIED-WITH-AMENDMENTS, applied | reviews/R04_*, numerics/n3, vn_bound_recheck.py, vn_bound_recheck_out.txt [C1-Sol-4] |
| L4 family map | v1 FALSE as written (R05) → v2 with all repairs; R06, sweep R07 and council-r1 corrections applied | reviews/R05_*, R06_*, R07_*, C1_* |
| L6 ENUM | PROVED (by this seat, unchecked); added after council r1; proof judged correct by both r2 seats; v2 states the general (EXB) override | lemmas/L6_ENUM.md, code v3_preprocess.R:18-27, v3_fit.R:120-125 |
| EMPIRICAL | descriptive | data_diag/SUMMARY.md |
Inputs (verbatim): T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; M5(0) "PROVED (SF: VERIFIED (W3-VT38E);
XF: VERIFIED* (A-REV5))"; GEN, C-GROW, W1-PXN, C-MIS "PROVED-CHECKED"; SEL "VERIFIED-WITH-AMENDMENTS"; GROW L6 R07
VERIFIED / R06 VERIFIED-WITH-AMENDMENTS; [OP] "PROVED (by this seat, unchecked)" inside GEN.

## 6. Review trail
Statement lock R01 (Sol high): LOCK-WITH-CHANGES, 10/10 applied. Lemma checks: R02 (L1 V-W-A, L2 VERIFIED), R03 key
(Sol xhigh, LOC V-W-A), R04 (VN V-W-A), R05 (L4 FALSE-as-written → v2). Mid-point R06 (fresh Sol xhigh): CONTINUE.
Sweep R07 (Sol xhigh): 0 FATAL / 6 MAJOR / 16 MINOR / 1 NIT — all fixed (reviews/R07_disposition.md). Council: r1 NOT PASSED (Sol 8.2, G1/G2/G6 FAIL; Opus 8.8 PASS); r2 NOT PASSED (Sol 8.8, G1/G6 FAIL; Opus 8.9 PASS); **r3 PASSED (Sol 9.1, Opus 9.1, all gates PASS)** (reviews/C1–C3_*.md, dispositions). Post-council edits (C3 MINOR/NIT items: FAC-A status sync, wording, notation, ENUM resource_limit clause) are editorial and listed in reviews/C3_disposition.md. Citation check: reviews/CITECHECK.txt (a citation-LOCATION and verbatim-status check with claim-specific tokens; R07 #19).

## 7. Open items / recommended next steps
1. FAC: FAC-A covers one factor + bounded blocks up to p ≍ n^{1/6−} (route-optimal for the full lattice); open: beyond
   1/6 (path route), k ≥ 2 factors, p > K — the VN obstruction says any proof must handle start modes with ≍ min(K, p)
   visible nulls; numerics suggest the LS0 deletion path still reaches S₀. Merge FAC-B when it lands.
2. Polynomial-decay Toeplitz and d ≥ 2 local designs (images, spatial): extend LOC (needs a lattice/NA argument for
   |Q| ≍ (log n)^d or polynomial relevance sets).
3. Growing blocks in the middle regime: NA with exchangeable innovations (2^{g_n} directions).
4. Paper: state Theorem LOC as the general reported-model result; put the applicability table in the discussion.

## 8. Files
STATEMENT.md, PLAN.md, LOG.md, CHECKPOINT.md, EMPIRICAL.md, REPORT.md, citecheck.py; lemmas/L1_POST.md, L2_CT.md,
L3_LOC.md, L4_families.md, L5_VN.md, L6_ENUM.md; numerics/ (ct_check, post_check, n0–n3, n3b, vn_bound_recheck, NUMERICS_LOC_VN.md,
LEAD_READING.md); data_diag/ (scripts, outputs, SUMMARY.md, data/, downloads/hdi/, core_copy/ source copy);
reviews/ (R01–R07 and council C1–C3 verbatim + dispositions + scratch, CITECHECK.txt). Nothing committed (HQ commits).

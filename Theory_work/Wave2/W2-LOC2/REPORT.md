# W2-LOC2 — REPORT (polylogarithmic relevance sets: d ≥ 2 local designs, growing one-factor groups, polynomial decay)

**RESULT: PROVED-CHECKED** — council round 1 PASSED (Codex gpt-6.1-sol xhigh 9.3, Claude Opus 5.5 high 9.1; all six gates
PASS in both seats). Post-council edits are editorial/status-sync only (reviews/C1_disposition.md).
**No method requirement:** every claim uses the shipped LS0 cap ℓ_n + |S̃₀| (main 4676af6); the former/smaller cap ℓ_n
is not claimed to suffice. **Statement changes vs the brief** (logged): R01's six lock changes — notably (C) split into
(C-i) [events and D_n → 0] and (C-ii) [+ LSF ⇒ posterior rate and output-intersected consistency], and the VN attribution in
(D2) restricted to the sub-class with visible nulls; R05 editorial κ ≥ 1; v1.2 fills the stretch slot (D3) with α₀ = 17/2.

## 1. Headline (for Felipe)
* **New key lemma NA-R (whole-lattice no-addition for large relevance sets).** NA(𝓛) must hold on the lattice
  𝓛 = {T : S₀ ⊆ T ⊆ Q}. NA-R writes each population residual e_{T,l} as a reference in a fixed-dimensional frame (from
  ≤ p·n^{o(1)} frames) minus an ℓ¹-bounded combination of atoms. Frames are controlled as whole subspaces, atoms one by one
  conditionally on the noise. The lattice (2^{|Q|} sets) enters only through relative norm errors and an additive
  sample-vs-population error ϵ_n = O((|Q| + log n)/√n). Result: max_{T,l} Z²_{T,l} ≤ 2 log p + o(log n) w.p. → 1, below the
  threshold c_n = 2 log p + log n − O(log log n), for any polylogarithmic |Q|. The earlier routes (GROW (G4-χ): one common
  χ²_{|𝒫|} charge, |𝒫| ≤ (1 − δ₀) log n; GROW L6.6/APP L3.6: reference innovations) were stated for |Q| = O(log n). NA-R is a
  different sufficient construction; it also covers one-factor groups and, re-run with vanishing atom norms, polynomial |Q|.
  No claim is made that the earlier routes could not be retuned.
* **(a) d-dimensional local designs — the main target — covered.** *Theorem LOC-d:* iid Gaussian rows whose correlation (or
  precision) decays exponentially in the Euclidean distance between sites in ℝ^d. This covers any fixed d, sites with
  minimum separation (grids, images, spatial lattices, irregular separated sites), spectrum in [c, C], PTV, and p ≤ n^A.
  Asymptotics are increasing-domain (fixed range in site units). Conclusions: D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0,
  1 − π(S₀) = O_P(√(log n/n)), and delivery P(Ŝ⁺ = S₀) → 1 under F-LOC2's premises and allocation. The proof bounds the
  start-mode extras by |Q| = O((log n)^d), an upper bound. Component-port runs in d = 2 suggest growth faster than log n [C1-Opus-5]
  (observations only). The shipped cap deletes the extras one per move.
* **(c) Growing equicorrelated / one-factor groups (the middle regime and beyond) — covered.** *Theorem LOC-BF:*
  block-diagonal designs whose groups are either bounded, or one-factor (incl. compound symmetry with ρ ∈ [b_lo², b̄²]) of
  size up to (log n)^κ, with ≤ one truth per group. No LOC-B size inequality s₀(g_n − 1) ≤ (1 − δ₀) log n is needed. The
  class includes sequences where W2-APP's Lemma VN obstructs the old |Q| = O(log n) route: compound-symmetric truth groups
  with g_n/log n → ∞ and polylogarithmic g_n.
* **(b) Polynomial decay — covered for α > 17/2.** *Theorem (L6_poly):* |Σ_jk| ≤ K(1 + |π(j) − π(k)|)^{−α} on a line
  (π a bijection), spectrum in [c, C], PTV, α > 17/2. Proved by a parallel Codex prover; checked by Opus (cross-family)
  and a fresh Sol, both V-W-A, applied. New tools:
  - Lemma BC: conditioning on ≤ 15 variables keeps the decay exponent α (cofactor paths).
  - Lemma IR: large-set inverses are bounded by H(1 + d)^{1−α}[log(2 + d)]^{α−1} — exponent α − 1 with a logarithmic loss (banded
    truncation + Combes–Thomas) [C1-Sol-1].
  - Selection removal with radius n^ρ: reference count O(n^{15ρ}); start modes O(n^{1/(2α)}).
  - NA with vanishing atom ℓ¹ norms.

  α₀ = 17/2 is the infimum for this counting argument (ρ > 1/(4α) and 15ρ + 1/(2α) < ½), not a necessity statement.
  **Open:** 1 < α ≤ 17/2 and long memory (α ≤ 1).
* **Numerics (component port, observations only):** 74 runs (2-D exponential grids, 2-D separable AR(1), polynomial
  Toeplitz α = 1.5, 3, middle-regime equicorrelated blocks). LS0 reached S₀, certified, in every run. Falsification
  checks of NA-R and CT_d passed. The polynomial runs do not probe the polynomial-|Q| regime.

## 2. Statement as proved
`STATEMENT.md` v1.2: (A) Lemma L0′; (B) Lemma NA-R; (C) Theorem PLR (C-i)/(C-ii); (D1) Theorem LOC-d; (D2) Theorem LOC-BF;
(D3) polynomial decay, α > 17/2; (E) Proposition F-LOC2 (delivery) for (D1)–(D3). Not claimed (STATEMENT §3):
non-Gaussian rows, fixed-domain (infill) asymptotics, growing s₀, θ*_min → 0, PTV failures, general/multi-factor growing
groups, groups with ≥ 2 truths, polynomially growing groups, pervasive non-block factor designs.

## 3. Status per clause (statuses verbatim; "PROVED (by this seat, unchecked)" + check record)
| Claim | File | Status | Checks |
|---|---|---|---|
| (A) L0′ + regularity | lemmas/L1_toolkit.md | PROVED (by this seat, unchecked) | R02 Sol high V-W-A (2 MINOR applied) |
| (B) NA-R (key) | lemmas/L2_NAR.md | PROVED (by this seat, unchecked) | R03 Sol xhigh V-W-A (1 MAJOR, 1 MINOR, 1 NIT applied) |
| CT_d, CD_d, RB, TAIL | lemmas/L3_CTd.md | PROVED (by this seat, unchecked) | R02 Sol high V-W-A (1 MAJOR CD_d indexing, applied) |
| (D1) LOC-d, (D2) LOC-BF | lemmas/L4_LOCd.md | PROVED (by this seat, unchecked) | R04 Sol high V-W-A (2 MINOR applied) |
| (C) PLR | lemmas/L5_assembly.md | PROVED (by this seat, unchecked) | R04 Sol high V-W-A (applied) |
| (D3) polynomial decay | lemmas/L6_poly.md (author: Codex prover) | PROVED (by this seat, unchecked) | R06a Opus high V-W-A; R06b Sol xhigh V-W-A (applied) |
| (E) F-LOC2 | lemmas/L7_delivery.md | PROVED (by this seat, unchecked) | R04 Sol high VERIFIED |
Mid-point R05 (fresh Sol xhigh): CONTINUE. Sweep R07 (Sol xhigh): 0 FATAL / 0 MAJOR / 10 MINOR / 6 NIT, all fixed. Council
round 1 PASSED (Sol 9.3, Opus 9.1, all gates). Hence every clause (A)–(E), incl. (D3), is PROVED-CHECKED in the protocol's
sense (proof file + cross-family lemma checks + mid-point CONTINUE + sweep fixed + council passed); the (D3) mid-point
coverage is through its two dedicated checks R06a/R06b, the sweep and the council (the mid-point R05 preceded L6).
Inputs (verbatim): T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; M5(0) "PROVED (SF: VERIFIED (W3-VT38E); XF:
VERIFIED* (A-REV5))"; C-GROW, W1-GEN, W2-APP, W2-FAC-A "PROVED-CHECKED"; [OP], APP L1_POST, GROW L0–L4/L6, GEN L1 "PROVED (by
this seat, unchecked)" with their recorded checks.

## 4. Review trail
R01 statement lock (Sol high): LOCK-WITH-CHANGES, 6/6 applied. R02 (L1 + L3, Sol high): V-W-A. R03 key lemma (Sol xhigh):
V-W-A. R04 (L4, L5, L7, Sol high): V-W-A, V-W-A, VERIFIED. R05 mid-point (fresh Sol xhigh): CONTINUE. R06a (Opus high,
cross-family) and R06b (fresh Sol xhigh) on L6: V-W-A ×2. R07 sweep (Sol xhigh): 16 items, all fixed. Citation check:
reviews/CITECHECK.txt (0 misses; location/token/status check only). **Council round 1 PASSED: Sol xhigh 9.3, Opus high 9.1,
G1–G6 PASS in both seats** (reviews/C1_council_sol.md, C1_council_opus.md, C1_disposition.md). All replies verbatim and
dispositions in reviews/.

## 5. Open items / next steps
1. Polynomial decay 1 < α ≤ 17/2 and long memory. The binding step is the sandwich's reference counting. Possible
   improvements: a sharper selection removal (deterministic families smaller than all ≤ 15-subsets of H_l), or a
   chaining bound for the far-null add statistic.
2. Polynomially growing one-factor groups (g_n = n^b). Needs the polynomial NA/assembly re-run (as L6) plus the
   sandwich inequality 16b < ½.
3. Multi-factor growing groups. NA-R applies if the Woodbury coefficients have bounded ℓ¹ norm (a loading condition).
4. Fixed-domain (infill) spatial asymptotics (range growing in site units) remain outside every current class.
5. Paper: state Theorem PLR with Lemma NA-R as the general reported-model engine, and list LOC-d, LOC-BF and
   polynomial decay as corollaries. Update W2-APP's applicability table rows (b), (c), (f) and its "Not claimed" d ≥ 2
   entry.

## 6. Files
STATEMENT.md, PLAN.md, LOG.md, CHECKPOINT.md, REPORT.md, citecheck.py; lemmas/L1_toolkit.md, L2_NAR.md, L3_CTd.md,
L4_LOCd.md, L5_assembly.md, L6_poly.md, L7_delivery.md; numerics/d1_diag.py, d1_out.txt, d1_results.csv, d1_stdout.txt,
D1_SUMMARY.md, n4_nar_check.py, n4_out.txt, poly_check.py, poly_out.txt; reviews/ (R01–R07 verbatim + dispositions +
scratch, C1 council replies + disposition, CITECHECK.txt). Nothing committed (HQ commits).

# W2-APP — Council round 1, Claude Opus 5.5 seat (verbatim reply)

Scope read: STATEMENT v1.2.1; lemmas L1_POST, L2_CT, L3_LOC (full, against C-GROW `lemmas/L6_random_AR1.md` read in full,
plus C-GROW L0 (score increment, ν = n/2 + 0.01), L2 (L2.1–L2.3), REPORT), L4_families v2, L5_VN; EMPIRICAL; REPORT;
numerics/LEAD_READING, NUMERICS_LOC_VN, vn_bound_recheck_out, n3_merged.csv; data_diag/SUMMARY.md (+ erratum),
summary_table.csv, summary_tables.md; reviews/CITECHECK.txt, R03, R07 + dispositions; FIN s3_posterior.tex (T03♯, SL0/SL1,
MIS), s5_hpm.tex (GEN/GROW statements, e4′, [OP]), s7_impl.tex (Lemma CAP, MR1, exact-branch convention); C-PACK I4:50-62;
production `v3_preprocess.R:22` (B = min(isqrt n, isqrt p, 16)) and `cpp/v3_core.cpp:473` (cap ℓ_n + |S̃₀|).
Independent checks (scratch `reviews/C1_scratch_opus/checks.py`): STAR spectrum {½, 1, 3/2} and Cov(W_l, W₁ | W_U) = r_n,
Var = 1; equicorrelated Schur formula ρ(1−ρ)/(1+(u−1)ρ) for u = 0, 1, 5, 15; one-factor Cov = b_lb_kVar(f|W_U) with
Var(f|W_U) = (1+Σb_u²/ψ_u)⁻¹; F3(iv) Σθ* = (0, −1.5); b_j = 2^{−j} spectrum ⊂ [¾, 4/3]; S5 floor 0.3; R06-2 weighted
cancellation (zero null covariance with Σθ* ≠ 0); MIS AR(1) cancellation γ₂ = 0 — all reproduce. n3_merged.csv: 40/40
(V1/V2/V3a) and 12/12 (V3b) certified LS0 endpoints = S₀, no start-mode truncation, LS0 cap never reached — reproduces.
Empirical master numbers in EMPIRICAL.md/REPORT §4 match summary_table.csv.

## Gate verdicts

**(G1) Correctness — PASS.** Checked step by step:
* L1_POST: m♯_n ≤ max(s₀, m̄_n) via C(p,k)/C(2p−1,k) ≤ (2/3)^k, w(k) = [2C(2p−1,k)]⁻¹ (BB(1,p) prior; I re-derived it),
  Σ_{k>m}(2/3)^k = 2(2/3)^m; Weyl/size×max-entry bound with k̄_n ħ_n = O((log n)^{3/2}/√n) = o(ψ_n); energy via
  λ_max(R̂_{S₀}) ≤ s₀; the diagonal tightness transfer (negation of uniform tightness gives n_k ↑, completed sequence
  contradicts T03♯'s O_P) is correctly written. (c) exact-Gram is immediate.
* L2_CT: S(t) = 2K[1/(e^{a−t}−1) − 1/(e^a−1)], S(t*) = α/2, Schur test with ≤ 2 indices per distance, Neumann bound
  ‖A_t⁻¹‖ ≤ 2/α — correct. CD: Cov(W_V|W_U) = (Θ_VV)⁻¹, principal-submatrix spectra, two CT applications — correct; (c)
  equivalence correct.
* L3 Theorem LOC: every AR(1)-specific use in [L6] (P1 spectrum, P3 floor, P4 conditional decay; P2 only in L6.6) is
  replaced; I grep-checked L6 for all P1–P4/c₋/c₊/Markov uses and found no use left unreplaced (L6:111 uses only the
  lower bound). New d_n, R_n make K₂e^{−t₂d_n} ≤ n^{−1/2}/(1+s₀θ_hiK₂)·K₂ and K₂e^{−t₂R_n} ≤ n^{−2}/(1+s₀θ_hi), as needed by
  L6.3(i)–(iii) and (6.8). The new NA argument L3.6 is correct: exact identity (I−P_T)x_l ∝ (I−P_T)Ce_{T′}; P_TC = P_T;
  P_Tg = P_Te_T + CD_{T,l}; v_{T,l} = cᵀM⁻¹c ≤ κ_D(log n)^{−2} by CD(a)/(b) and two-per-distance counting; χ² mgf
  2^{d/2}e^{−v/4}, Laurent–Massart (n+2·n/√2+n ≤ 4n); ‖g‖/‖h‖−1 ≤ ‖P_Tg‖²/‖h‖²; η_n = O((log n)^{−1/2}) so
  2η_n|Z′| = O(1) = o(√log n); 2log(2N) = 2log p + O(log log n) < c_n = 2log p + log n − O(log log n). LOC-B: exact
  cross-group zeros under any conditioning, α = 0, m = 0, H_l = G(l) ∪ Q⁰ of size O(log n) under (B-χ), NA by
  GROW L2.3(a) with the post-enlargement bound — correct.
* L5_VN: increment −ν log(1−h/n) ≥ h/2 (ν = n/2+0.01, GROW L0:42), prior ratio ≥ −log(2p), U = S̃ ∩ C_b truth-free with
  |U| ≤ 15, count ≤ 15s₀ — correct. V1–V4 κ's verified numerically (above).
* L4: F1 (Toeplitz floor by Fourier orthogonality), F2, F3(ii) (D* gives a₀ = cθ_lo/2), F4 (block-diagonal projection
  support), ordering-invariant non-LOC argument for two-sided polynomial tails (+ precision alternative via CD(c)),
  AR(1) marginal-Markov neighbour rule — all correct.
No false mathematical claim found.

**(G2) Hypotheses used = hypotheses stated — PASS.** LSF (i)/(ii) exactly what L1 uses; (LOC)+(PTV) exactly what L3 uses
(PTV for |U| ≤ 15, U ⊆ [p]∖{j}, matches the TV use in L6.5 inclusion with blocks ≤ 16); LOC-B's (B-χ) incl. the
enlarged-Q clause is exactly what GROW L2.3(a) needs; VN uses (F16) on |S| ≤ 16 + s₀ and VNF over null-only U.

**(G3) No hidden assumptions — PASS.** Implementation premises are named (EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, complete
scans, IND-T/c₄, "emitted centre is some maximiser of γ₀"), zero-mean reduction stated, empty-𝔓 case handled, partition
only required to be X-measurable with blocks ≤ 16 (production: B ≤ 16 verified). The exact-branch convention (s7) makes
fixed-p sequences harmless (D_n concerns potential scored sets; on the exact branch S₀ is scored). One presentational
omission in the headline (issue 3) — not a hidden assumption in any lemma.

**(G4) Cited lemmas: adequate status, quoted verbatim — PASS.** T03♯, M5(0)/T38-(0), GEN, C-GROW (incl. L6, which is
inside the council-passed C-GROW; L6's own header line "council pending" is stale but W2-APP quotes the correct C-GROW
REPORT status), PXN, C-MIS, SEL, SL0/SL1, [OP] — quoted verbatim, verified against FIN and source REPORTs. CITECHECK is
honestly labelled a location/status check (R07 #19).

**(G5) Constants/rates tracked — PASS.** j₀, m̄_n, k̄_n, φ₀² = φ²/2, g₀ = 1, M = s₀²θ_hi² + 1, BM envelope; t*, (K₁,t₁),
(K₂,t₂); d_n, R_n, r_n, κ_D, b_n, η_n, c_n; VN κ's explicit for V1–V4; F3(ii) D*. Rate √(log n/n). Scope rule respected
(no finite-n caveats; L3.9 onset sentence removed).

**(G6) Fidelity to the method as coded — PASS.** Theorem LOC uses the shipped v3.1 cap ℓ_n + |S̃₀| (`v3_core.cpp:473`,
default on); any X-measurable partition with blocks ≤ 16 (`v3_preprocess.R:22`); start law γ₀ = prior × product of block
tables r_b(U) = m(U)/m(∅) as in GROW L0; LS0 descent via GROW L4/L1 and [OP]; Lemma CAP monotonicity needs no further
use since the theorem is proved directly at the shipped cap. Numerics are correctly labelled as a Python component port
with recorded tie/cap differences.

## Score: 8.8 / 10

A careful, well-reviewed applicability map whose new mathematics (POST transfer, CT/CD, the window-innovation NA proof,
LOC-B, VN and its four quantified applications) I could verify line by line; the family map now separates (Σ)/(θ)/(T)
consistently and no table cell asserts more than its lemma proves, apart from the wording items below. Deductions are
for residual summary-level phrasing that slightly outruns the lemmas (issues 1–4), not for correctness.

## Issues

1. **MINOR — `REPORT.md:28` (also echoed `REPORT.md:66–68`).** "So the gap is a proof-route limitation, not evidence of
   method failure" can be read as a conclusion that the method succeeds on pervasive designs. VN proves only that the
   GEN/GROW/LOC routes are blocked; the method's behaviour there is unproved, and 40/40 port runs at n ≤ 12800 (where VN's
   own bound is not yet met for V2 and for V3a at n ≤ 3200, `vn_bound_recheck_out.txt`) are observations. **Fix:** "VN
   obstructs the proof routes only; whether the method's LS0 deletion path reaches S₀ there is open (FAC); in the
   component port it did in 40/40 runs."
2. **MINOR — `REPORT.md:55`; `lemmas/L4_families.md:158`.** Cell "Σ ∉ LOC" for the row "Toeplitz, polynomial decay / long
   memory" is unqualified, but L4:86–91 proves non-membership only for the two-sided family |γ(h)/γ(0)| ≥ c′h^{−β} for all
   h ≥ 1. A row defined by a polynomial *upper* bound includes exponentially decaying (LOC) members. **Fix:** label the row
   "two-sided polynomial tails (incl. long memory h^{2d−1}), density ≥ m" or qualify the cell.
3. **MINOR — `REPORT.md:12–16`.** The headline "Reported model (the method's output) is proved consistent for all local
   designs … under one signal condition, PTV" omits that the conclusion is P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 under the named
   implementation premises (EX-A … OP-LS0, complete scans, emitted centre a maximiser of γ₀), with no delivery claim —
   stated in the body (§3 legend, L3.0) but not in the headline that Felipe reads first. **Fix:** add "(under the chapter's
   named implementation premises; no delivery claim)".
4. **MINOR — `REPORT.md:64–65`.** "most strong pairs are split across blocks (riboflavin 99.5%), which is where the VN
   obstruction acts" re-links marginal cross-block correlation to VN's mechanism, which R07 #8's disposition (and
   EMPIRICAL:65–67) correctly withdrew: marginal leakage does not establish VNF. **Fix:** "… consistent with, but not
   establishing, the mechanism quantified in VN's models V1–V4."
5. **MINOR — `EMPIRICAL.md:40`.** Heading "Local, moderately conditioned" covers diabetes-quadratic, whose observed
   λ_min(R) = 3.6e-7 and φ²(7) ≤ 8.1e-5 (and spam, λ_min = 0.0039), i.e. not moderately conditioned; REPORT §4 correctly
   says "(e) with small floor". **Fix:** "Local (bounded clusters; some near-collinear)".
6. **NIT — `REPORT.md:69–70`.** "Unproved, no obstruction known: … growing blocks where a LOC-B bound fails but g_n/log n
   does not diverge" — the GEN route *is* obstructed there whenever g_n → ∞ (V2). **Fix:** "no GROW/LOC-route obstruction
   known".
7. **NIT — `EMPIRICAL.md:44`.** spam described as "isolated pairs", but its partner distribution (90% quantile 10, max 11
   above 0.3) shows a bounded cluster of ~11 variables besides the near-duplicate pair. **Fix:** "isolated pairs and small
   bounded clusters".
8. **NIT — `lemmas/L2_CT.md:67` vs `lemmas/L4_families.md:83`.** K′ normalisation differs (|γ(h)| ≤ K′ρ^h with K = K′/γ(0)
   vs |γ(h)/γ(0)| ≤ K′ϱ^h). Harmless; unify.
9. **NIT (housekeeping) — `REPORT.md:3`.** The RESULT line must be finalised after the council (and the "Council:
   (pending)" entry at REPORT §6). Not scored.

**Which fixes change my score:** fixing 1–4 together would raise the score to about 9.1; 5–9 are cosmetic (≤ 0.1 combined).
None of the issues is gate-blocking; all six gates PASS in this round as the files stand.

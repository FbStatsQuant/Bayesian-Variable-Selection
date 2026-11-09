# Council round 1 — seat B — Claude Opus 5.5, high

Ticket W2-UNI, STATEMENT v1.1.3 (locked). Reviewed: STATEMENT.md; lemmas L1_metric, L2_k0, L3_ULOC, L4_k1, L5_delivery,
L6_frontier, C_corollaries; REPORT.md (draft; RESULT/council/citecheck lines treated as intentionally pending); numerics/
(scripts and outputs, incl. n3_out, n3b_out, n4_r2_pseudo_summary, n5_obsk_out); citecheck.py and reviews/CITECHECK.txt.
Sources checked for every load-bearing use: FACA STATEMENT §2–§4, L1_uniform_add (U(a)–(d), Corollary U), L2_sandwich,
L3_NA_TL (L3.0–L3.3), L4_assembly, L5_random_instances (L5.0–L5.3), L7_delivery; LOC2 REPORT, L2_NAR (hypotheses and
statement), L4_LOCd Part A, L5_assembly (PLR), L7_delivery; APP L1_POST (LSF cutoffs), L3_LOC (§L3.0–L3.6), REPORT;
FACB REPORT; C-DLV L4_delivery Corollary D′ (:65-77); production core (`v3_preprocess.R:21,111-112`,
`v3_run.R:100-101`, `cpp/v3_core.cpp:402-404,473-479`); Wave2/Wave1C/Wave1 protocols. Review-verdict files opened only
to confirm that cited verdicts exist (R02, R03, R04 CONTINUE, R05b) — after forming my own judgment.
Scope rule respected: nothing below concerns "asymptotic only".

## Independent checks run (scratch: reviews/C1_scratch_opus/)

* `chk.py`: non-block Ψ (AR-type correlation rescaled to diag 1 − λ_j², signed heterogeneous loadings, p = 9, λ_min(Ψ) =
  0.27). U-LOC(a) identity against the direct Schur-complement innovation of Σ: max error 1.3e-15 over 6000 random
  (T, l, draw) triples including T = ∅; U-LOC(b) deterministic bound: 0 violations. Exhaustive block-CS check
  (ρ_b = .3, ρ_w = .7, 3 groups of 3): c_𝒢 = 0.428571 = c_min = ρ_b/(1 − ρ_b), confirming the L3_ULOC §L3.4 remark and
  C_corollaries row 8.
* `joint.py`: exhaustive κ = κ′/√c_𝒢 versus the joint ratio κ_J of MINOR-3 below on four random non-block designs
  (p = 9): (6.09, 3.61), (3.66, 3.66), (4.82, 4.25), (3.74, 3.35).
* Arithmetic re-checks: α₀ values for κ = 7.270/5.390/5.560/3.317 (0.0074/0.0126/0.0119/0.0284); the union constant in
  U-LOC(d) (Σ_h |𝒯_h|e^{−x_h} = Σ_h [2(h+1)² log n]⁻¹ ≤ (π²/6 − 1)/(2 log n)); x_h/h ≤ log(eG/h) + (γ̄ + 3) log 2 + log log n;
  log log 16 = 1.0198; R_n and d_n give K₂e^{−t₂R_n} ≤ n^{−2}/(1 + s₀θ_hi) and K₂e^{−t₂d_n} ≤ K₂n^{−1/2}/(1 + s₀θ_hiK₂);
  every count quoted from n4_r2_pseudo_summary.txt in L2_k0 §12 (120/120, 119/120, 101/120, 117/120, 64/120, 41/120,
  19→10→3/20, max gain 5.3→4.1→1.1, min TL margin 61) and from n5_obsk_out.txt in L6 header matches the output files.

## Mathematical assessment

**L1_metric (R1).** CT_M: S(t) finite, continuous, nondecreasing, S(0) = 0, S → ∞ as t ↑ a′ (partial-sum argument is
right), so t* ∈ (0, a′); the conjugation uses only 1-Lipschitzness of δ(·, j); E_ik = 0 on zero-distance pairs; the
shell-wise bound of the non-monotone g on [m, m + 1) is correct; Schur test and ‖A⁻¹E‖ ≤ ½ give the claim; restricted
version by interlacing and (G-restr). CD_M: Θ_HH principal submatrix, (Θ_HH)⁻¹ = Cov(ζ_H | ζ_U), spectra in [c, C]; the
"Var ≤ min(Ψ_jj, C)" correction is right. RB_M with G_ll ≥ 1/C (non-unit diagonal) is right and the numerics confirm the
correction is needed. TAIL_M: 𝒟 = bᵀM⁻¹𝒱, Var ≤ ‖b‖²/c. LOCL (i)–(v): normal-equation restriction, 1→1 norm as max column
ℓ¹ norm with columns β_U(w), ‖Δ‖₁ ≤ (1 + L₀)‖β_{T,V}‖₁ ≤ ε(r), variance identity by orthogonality, Hölder; empty-set
conventions consistent. SC_M correct (remark only). No gap.

**L2_k0 (UNI-0).** The inventory G1–G17 identifies every place where the LOC2/APP/GROW chain used geometry; I checked
the cited source lines (LOC2 L4_LOCd A.1–A.6, APP L3_LOC L3.2–L3.5, the "linear-growth fact") and found no further use
of separation ≥ 1 or of Euclidean structure. Relevance set, size O((log n)^{d₀}), dichotomy, |Q| ≤ K_n eventually,
separation property, selection-removal inputs (i)–(iii) (with the R02-2 auxiliary coordinate V_b), spherical tail
(‖m‖ ≤ C√n e^{−t₂d_n} ≤ C), ladder with k₀ = |Q| + 16s₀, NA-R (R1) frames N_n ≤ p·2^{C₀(1+log log n)^{d₀}}, (R2) atoms
with L = 2L₀ and L² log(|Q| + 1) = O(log log n), (R3) via TAIL_M — all match NA-R's locked hypotheses (`L2_NAR.md:23-36`)
and PLR's (`L5_assembly.md:13-19`). (C-ii) via LSF from the global floor; delivery via the LS0-scoring event 𝒦_n, not
via D_n. Unit-diagonal and upper-bound audits (§11) are accurate. No gap.

**L3_ULOC (key lemma).** (a) The Pythagorean decomposition needs block structure in FACA only at two places; here
P_{𝓚_T}ζ_l = β_T(l)ᵀζ_T and E[γ_lW_T] = λ̃_{l|T}/√(1 + s_T) hold for any Ψ ≻ 0 — verified analytically and numerically.
(b) |Z| ≤ |Ξ| + κ′_{l,T}|ξ₀ − √s_TF_T|/(1 + s_T), then √s/(1 + s) ≤ 1/√s: correct. (c) The decisive new step: A := T ∩
B(l, r_n), √ψ_{l|T}|Ξ_{l,T}| ≤ √ψ_{l|A}|R_{l,A}| + ‖Δ‖₁ max_v|ζ_v| with ‖Δ‖₁ ≤ ε(r_n) uniformly (LOCL), ψ_{l|A} ≤
ψ_{l|T} + Cε_n² (LOCL(iv)); unions only over p·2^{N_n} references and p atoms (Var ζ_v = Ψ_vv ≤ 1). With r_n =
⌈(log log n)²⌉, N_n = O((log log n)^{2d₀}) and ε_n → 0, the envelope is √(2 log p) + o(√log n) with a deterministic
remainder. Correct. (d) Entropy-stratified union over all nonempty T with thresholds x_h; no independence used; the
inequality chain to √(2 log(eγ̄p/|T|)) + ϱ_n is correct (h ≥ |T|/γ̄, G ≤ p). Corollary (population incl. T = ∅; sample
version via FACA's coupling, which uses no block structure, and FACA U(d), whose hypotheses — Σ correlation with
Σ ⪰ ψ₀I, R̂ correlation, ‖R̂ − Σ‖ ≤ ψ₀/4 — hold with ψ₀ = c). The resulting form is exactly what FACA L3.1 consumes
(`L3_NA_TL.md:44-46`: "|Z_{T,l}| ≤ √(2P) + κ̄√(2x_k) + ε_n" with ε_n = o(√L)); FACA L3.2 needs only Z̄_n = O(√log n),
which the all-T form supplies (R03-1 fix is correct). No gap.

**L4_k1 (UNI-1).** I checked FACA L2 (uses only the method blocks, (G3a), energy, TV, K = p), L3.0–L3.3 (block
structure of Ψ enters only through Corollary U; κ′ only through κ′_bd; λ_min ≥ ψ₀ only through φ² = 3ψ₀/4), L4.1 and
L5.0/L5.1 (design events via Lemma CR; δ_n√(p log log n) → 0 since α₀ ≤ 1/6 < 1/3; TV from TV-pop via a Lipschitz
argument on |V| ≤ 16 + s₀; PTV(a₀) ⇒ TV-pop with τ₀ = a₀² because Σ_{jj|U} ≤ 1). Inventory items 1–8 are complete. κ ≥ 1
holds automatically in the UNI representation (take T = ∅ for κ′ and T = {l} for c_𝒢), so the α₀ formula is valid.
Containment of FACA's 𝔉 (block pseudometric, C₀ = γ̄, d₀ = 1, spectrum in [ψ₀, γ̄], c_𝒢 = c_min, κ_UNI = κ_FACA) is
correct, and the restriction of the containment claim to FAC-L's fixed-positive-beta-min subclass is right.

**L5_delivery (F-UNI).** Steps 1–3 match FACA L7 / LOC2 L7; Step 3 goes through 𝒦_n and D′'s pathwise scored-set
argument (`C-DLV/lemmas/L4_delivery.md:65-77`); input validity checked against the code (only exactly-constant columns
are dropped, `v3_preprocess.R:111-112`). Correct.

**L6_frontier (OBS-k).** Covering/pigeonhole proof is correct (|Λ_jᵀu| ≤ L_*·η/L_* = η, λ_min ≤ c⁻¹mη², ratio ≤ η²/c);
the scope paragraph is appropriately narrow. Plan table makes no claims.

**C_corollaries / STATEMENT §5.** Rows checked against the cited sources and `gen_dev_data.R:18-42` (S3/S4/S6 group size
5, spectral floors 0.3/0.15/≥ 0.1, one truth per group, PTV(θ_lo c) via block independence; S5 = 0.3·11ᵀ + 0.4H + 0.3I
with Ψ_jj = 0.7, λ_j² = 0.3; AR(1) spectrum; FACB "fixed nonzero ϑ" and actual-block-TV qualifier). Correct as
qualified.

**Fidelity (G6).** K = min(p, ⌊n/2⌋) (`v3_preprocess.R:21`); default LS0 cap ell + |start mode|
(`v3_core.cpp:404,473`; `v3_run.R:101`); the premises (complete scans, e4/TDP-IMPL, fallback) are inherited verbatim
with their recorded statuses (e4/N3 "OPEN", S.3/P1 "AUDITED (code reading)"), not silently assumed.

## Gates

* **G1 correctness — PASS.** Every step of L1–L6 checked; no false step found. Key lemma independently re-verified
  numerically.
* **G2 hypotheses used = stated — PASS.** UNI-0 uses exactly (R), unit diagonal, LOC_M, PTV, fixed s₀, coefficient
  bounds, p ≤ n^A; UNI-1 uses (A2-1) through κ ≤ κ̄ and κ′_bd only, (P), TV/TV-pop. MINOR-4 is a missing explicit
  sentence, not an unstated hypothesis.
* **G3 no hidden assumptions — PASS.** Zero/sub-unit distances, non-unit Ψ diagonals, empty conditioning sets, Q
  deterministic, X-measurable partitions, enlarged-space coupling (no claim of σ-field membership) are all handled.
* **G4 cited-lemma status — PASS.** Statuses quoted verbatim and adequate for the uses (each lemma "PROVED (by this
  seat, unchecked)" with its check verdict inside a "PROVED-CHECKED" ticket; T03♯, M5(0), [OP], e4/N3 strings
  verbatim; cited review verdicts exist as recorded). MINOR-1 (missing CITECHECK_AUDIT.md) concerns the pending
  citation-audit package, not the status of any cited result.
* **G5 constants/rates — PASS.** All constants explicit (L1 §M7, L3 η_n, ϱ_n, ε^U_n, L_ψ); rates d_n, R_n, r_n, N_n,
  ε(r_n) = o((log n)^{−M}), remainder o(√log n), probability budgets (4/log n, 5/log n) tracked.
* **G6 fidelity to the method as coded — PASS.** See above.

## Issues

No FATAL, no MAJOR. None of the issues below blocks passing.

**MINOR-1 (evidence package; `reviews/CITECHECK.txt:2`, `REPORT.md:129`).** Both refer to `reviews/CITECHECK_AUDIT.md`
("content audited manually … (see reviews/CITECHECK_AUDIT.md)"), which does not exist in `reviews/`. A citation-check
record must not point to a non-existent audit. *Fix:* write the manual content audit of the non-self citations
(from `CITECHECK_excerpts.md`) to that file before the REPORT's CITECHECK line is filled, or remove the reference from
`citecheck.py`'s header text and REPORT §8.

**MINOR-2 (overclaim in REPORT headline; `REPORT.md:46-49`).** "Every existing family result is an instance or a
marked partial version (§4)" overstates C_corollaries itself: row 4 states that GEN's masked-truth theorems (LH, LH-iid,
W) are not imported; PXN's masked results and FAC-L's fixed-design BM-∞ relaxation are separate imported results
(STATEMENT §6, row 8); "banded/ARMA" is an example class, not a listed existing result; and "§4" points to the status
table, not the corollary table. *Fix:* "Every family result listed in `lemmas/C_corollaries.md` (STATEMENT §5) is an
instance, a separate extension, or a marked partial version; GEN's masked-truth theorems (LH, LH-iid, W), PXN and
FAC-L's BM-∞ relaxation remain separate imported results." Move "banded/ARMA" to the §6 examples sentence.

**MINOR-3 (sharpness, non-blocking; `L3_ULOC.md:54-57,93`, `STATEMENT.md:61-64,72`).** The factor term needs only the
joint ratio κ_J := max{1, sup_{∅≠T, l∉T} κ′_{l,T}·√(h_𝒢(T)/s_T)} ≤ κ = κ′/√c_𝒢. Proof unchanged: in (b),
κ′_{l,T}√s_T|F_T|/(1 + s_T) ≤ κ′_{l,T}|F_T|/√s_T = [κ′_{l,T}√(h/s_T)]·|F_T|/√h ≤ κ_J√(2x_h/h) on E_F; the ξ₀ term keeps
κ′_bd; FACA L3.1 then runs with κ̄ ≥ κ_J (max with 1 keeps the α₀ formula valid). The gain is real for non-block Ψ:
exhaustive p = 9 examples (`C1_scratch_opus/joint.py`) give κ = 6.09 vs κ_J = 3.61 (α₀ 0.0101 → 0.0247), 4.82 vs 4.25,
3.74 vs 3.35; equality for diagonal/CS-type cases. Given the project's optimality concern, *recommended fix:* state
UNI-1 with κ_J (or add a remark that κ may be replaced by κ_J, with this two-line proof), and note κ_J = κ for every
block CS. The theorem as stated is correct.

**MINOR-4 (explicitness of a source extension; `L4_k1.md:36-43,60-62`).** FACA L5.1 is stated for "fixed nonzero
θ*_{S₀}" (`FAC-A/lemmas/L5_random_instances.md:71,83`, "BM-∞ since θ* is fixed and nonzero"), while UNI-1(R) allows
n-dependent coefficients with |θ*_j| ∈ [θ_lo, θ_hi]. The extension is valid (L5.0's table depends only on M, the BM-∞
envelope, the TV envelope; the TV-pop Lipschitz constant depends on ‖θ*‖ ≤ √s₀θ_hi; T03♯'s every-sequence argument uses
common constants), but L4_k1 never says so. *Fix:* add to item 5 or 6: "FACA L5.1 uses fixed θ* only through
M := s₀θ_hi², the BM-∞ envelope θ_lo²n/log n and the Lipschitz constant (via ‖θ*‖ ≤ √s₀θ_hi); hence it applies verbatim
to coefficient sequences with |θ*_j| ∈ [θ_lo, θ_hi]."

**NIT-1 (`L6_frontier.md:8`).** "I([p]) stays ≈ 0.10–0.26" — `n5_obsk_out.txt` reports I([p]) = nan at p = 3200. Say
"for p ≤ 800 (not computed at p = 3200)".

**NIT-2 (`L4_k1.md:65`).** "K := max(1, max|Ψ_jk|)e^{0}" is garbled; write "K := 1 (|Ψ_jk| ≤ √(Ψ_jjΨ_kk) ≤ 1), any
a > 0", as in C_corollaries (G-block).

**NIT-3 (`STATEMENT.md:93`).** "LOC2 L5, PROVED-CHECKED there": the lemma's status is "PROVED (by this seat,
unchecked)" (R04 VERIFIED-WITH-AMENDMENTS) inside the "PROVED-CHECKED" ticket W2-LOC2; phrase it that way (statuses
verbatim).

**NIT-4 (process disclosure; `L3_ULOC.md:6`, `L4_k1.md:4`, `REPORT.md:81-84`).** R03, R04 and R05a are recorded as Sol
"xhigh", whereas `Wave2/PROTOCOL.md:37-40` caps effort at high. If these reviews predate the cap, say so in REPORT §5
so the trail does not read as a protocol breach.

**NIT-5 (`REPORT.md:38-39`).** The UNI-1 headline lists only "visibility (TV-pop; sufficient: PTV)"; add "(E): TV on
the actual blocks".

**NIT-6 (`L2_k0.md:19`).** GROW L6 is quoted with "R07 'VERIFIED'" only; APP `L3_LOC.md:3-5` records R07 VERIFIED and
R06 Opus VERIFIED-WITH-AMENDMENTS — quote both.

## Overall

A correct, carefully assembled result. The new mathematics — the pseudometric Combes–Thomas toolkit with shells from
m = 0, the ℓ¹-localisation lemma LOCL, and above all U-LOC(c), which replaces FACA's block-local innovation by
p·n^{o(1)} references plus atoms whose ℓ¹ weight vanishes — is right and is exactly what is needed to transfer FACA's
full-lattice NA/TL to non-block Ψ without changing the exponent formula. The UNI-0 delta is complete, and the
corollary/containment claims are correctly qualified. The deductions are for the evidence-package gap (MINOR-1), one
headline overclaim (MINOR-2), and a free sharpening of the exposure ratio that the statement leaves on the table
(MINOR-3).

GATES: G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS; SCORE: 8.9

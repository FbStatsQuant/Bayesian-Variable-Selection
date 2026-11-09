# W2-APP — Council round 3 (final), Claude Opus 5.5 seat (fresh reviewer; verbatim reply)

Scope read: STATEMENT v1.3.1; lemmas L1_POST, L2_CT, L3_LOC (full, incl. the L3.6 window-innovation NA proof and LOC-B),
L4_families v2, L5_VN, L6_ENUM v2; EMPIRICAL; REPORT; numerics/LEAD_READING (+ NUMERICS_LOC_VN supersession notice,
n3b_fastls.py docstring); data_diag/SUMMARY.md (+ lead erratum), summary_table.csv, out_iclaims.txt; reviews/CITECHECK.txt;
C1_*, C2_* replies and dispositions. Sources: C-GROW `lemmas/L6_random_AR1.md` (read in full), `L2_NA_TL.md` (L2.2 threshold
c_n, L2.3(a) hypothesis |𝒫| ≤ (1 − δ₀) log n), C-GROW STATEMENT §1/(G1)–(G4); FIN `s1_setting.tex:18-28` (LS0, reported HPM,
𝒪 = status exact or completed), `s3_posterior.tex:20-34` (SL0(iv), SL1, I-c transfer), `s5_hpm.tex:40-76` (GEN, GROW,
(C5)(b) fixed-p caveat); C-PACK I4:55-60; production `v3_preprocess.R:17-33` (v3_budgets), `cpp/v3_core.cpp:72-85`
(cpp_exact_count), `v3_fit.R:100-131` (branch on post-preprocessing (n, p); exact branch returns before setup/LS0),
`cpp/v3_core.cpp:403-475` (LS0 cap ℓ_n + |S̃₀| default).
Independent checks (`reviews/C3_scratch_opus/checks.py` → `checks_out.txt`): (EXB) re-implemented with saturating integer
arithmetic — 0 cases with 2^p ≤ 4np but (EXB) false over n = 10⁴…10²⁹, p ≤ 119; fixed-p exact-branch onsets for the eight
Part-2 widths; riboflavin null max-|r| reference by the exact t law. iclaims pairwise |r| recomputed from `data/iclaims.rds`.
All other analytic steps re-derived by hand (below).

## Round-1 and round-2 issues — status

| Issue | Fixed? |
|---|---|
| C1 Sol 1 (enumeration override) | Yes — Lemma ENUM. |
| C1 Sol 2 / Opus 2 (polynomial-tail qualifier) | Yes (L4:91-97, REPORT row (c)-poly). |
| C1 Sol 3 (screened "certified") | Yes (REPORT:33-35, LEAD_READING:31-34). |
| C1 Sol 4 (dangling evidence file) | Yes (CITECHECK checks deliverables; TOTAL MISSES 0). |
| C1 Opus 1, 3–8 | Yes (re-checked at REPORT:13-16, 36-37, 77-80, 84; EMPIRICAL:43-49; L2_CT:67-68). |
| C2 Sol 1 / Opus 1 (ENUM shortcut ≠ whole override) | **Yes.** L6_ENUM:15-20 states the general (EXB) override with 2^{p_n} ≤ 4np_n as a sufficient condition; the blanket "earlier statuses stand" is gone; L4:7-11, STATEMENT:99-102, REPORT:21-24, 68, 71-74, 84 restrict "unproved/obstructed" to sequences on which (EXB) fails infinitely often. Sol's 2^{p_n} ≤ n example and my p = log₂n + log₂log₂n example are both covered (2^p ≤ 4np). |
| C2 Sol 2 (NUMERICS_LOC_VN superseded claims) | Yes (supersession notice NUMERICS_LOC_VN:3-11; n3b_fastls.py:1-2). |
| C2 Sol 3 / Opus 5 (versions, inventory) | Mostly: STATEMENT v1.3.1, REPORT §2 and §8 updated; REPORT:7 still says "none beyond R01's lock changes" (issue 5). |
| C2 Opus 2 (iclaims inconsistency) | Yes (REPORT:40-41, EMPIRICAL:61-63, 88). |
| C2 Opus 3 (Gaussian rows in Part 2) | Yes (EMPIRICAL:38-40, REPORT:43-45). |
| C2 Opus 4 (Σθ* notation) | Yes except one residue, LEAD_READING:28 (issue 4). |
| C2 Opus 6, 7 (a.s. preprocessing; floating-point) | Yes (L6_ENUM:7-8; EMPIRICAL:41). |

## Gate verdicts

**(G1) Correctness — PASS.** Re-derived: POST (C(p,k)/C(2p−1,k) ≤ (2/3)^k; R_m ≤ 2(2p)^{s₀}(2/3)^m; m̄_n threshold;
k̄_nC′ħ_n = O((log n)^{3/2}/√n) = o(ψ_n); diagonal tightness transfer). CT (S(t*) = α/2, Schur test with ≤ 2 indices per
distance, Neumann bound 2/α) and CD (Cov(W_V | W_U) = (Θ_VV)⁻¹ with uncompressed positions; spectrum of (Θ_VV)⁻¹ in [c, C]).
LOC delta proof against [L6]: L6.3's R_n replacement makes K₂e^{−t₂R_n} ≤ n⁻²; d_n makes s₀θ_hiK₂e^{−t₂d_n} ≤ n^{−1/2};
L6.4's ‖m‖ ≤ C√n e^{−t₂d_n}; L3.6 — exact identity (I − P_T)x_l ∝ (I − P_T)Ce_{T′}; v_{T,l} = cᵀM⁻¹c ≤ ‖c‖²/c ≤ κ_D(log n)⁻²
(Σ_{d>r}2K₂²e^{−2t₂d} and e^{−2t₂r_n} ≤ (log n)⁻²); χ² MGF at ¼ for ‖P_Te_T‖²; Laurent–Massart at x = n/2 gives
(2 + √2)n ≤ 4n; η_n = O((log n)^{−1/2}); max Z² ≤ 2 log p + O(log log n) < c_n = 2 log p + log n − O(log log n) (c_n
matches GROW L2.2 verbatim). LOC-B: exact cross-group zeros survive any conditioning; α = 0, m = 0; (B-χ) incl. the
enlarged-Q clause is exactly L2.3(a)'s |𝒫| ≤ (1 − δ₀) log n. VN: increment ≥ −log(2p) − ½log(n+1) − 2κ_E + nκ_n/4 (prior
ratio (k+1)/(2p−1−k) ≥ 1/(2p), only block b's table changes); V1 spectrum {½, 1, 3/2} and Cov(W_l, W₁ | W_U) = r_n
(Σ_{lU} = 0); V2/V3 Schur complement ρ(1−ρ)/(1+(u−1)ρ); V4 Cov = b_lb_kVar(f | W_U), Var(f | W_U) = (1 + Σb_u²/ψ_u)⁻¹;
STAR ∉ LOC and two-sided-polynomial Toeplitz ∉ LOC counting arguments (LOC-Θ excluded via CD(c)); F2–F4; AR(1) MIS
cancellation example (γ₂ = ½ − ½ = 0). ENUM: (ii) Σ_{k≤K}C(p,k) ≤ 2^p ≤ 4np ≤ 4N₀p ≤ (5H₀+4N₀)p; (i) SL0(iv) ⇒ S₀ the
unique F-maximiser on the fully scored Ω, so the strict order (F, −|S|, lex) returns S₀; liminf identity by subtraction.
No mathematical defect found. Remaining defects are summary-level wording (issues 1–2), not proof steps.

**(G2) Hypotheses used = hypotheses stated — PASS.** LSF (i)/(ii); (LOC) + PTV(|U| ≤ 15) exactly as consumed by L3.2 (TV)
and L3.5; L3.6 correctly marked "PTV not needed"; LOC-B's (B-χ) with the post-enlargement clause; VN's (F16) on
|S| ≤ 16 + s₀ and VNF over null-only U; ENUM: EX-A + POST's conclusion + the coded inequality. One headline phrase
("Small p (any correlation structure)") drops POST's LSF hypothesis — issue 2; the lemma and table row state it.

**(G3) No hidden assumptions — PASS.** Gaussian rows, independent noise, fixed s₀ and θ-bounds, uniform constants and named
implementation premises explicit throughout Part 1; Part 2 now states that the theorems assume iid Gaussian rows. The
iclaims "settled by ENUM + POST" sentence is the one place that forgets this caveat (issue 1).

**(G4) Cited lemmas: adequate status, verbatim — PASS.** Statuses checked against sources: T03♯, M5(0)/T38-(0), GEN, C-GROW
(L6: R07 VERIFIED, R06 V-W-A), W1-PXN, C-MIS "PROVED-CHECKED", SEL "VERIFIED-WITH-AMENDMENTS", SL0/SL1 "PROVED (by this
seat, unchecked)" with C-PACK council, [OP]. L6_ENUM's code citations (`v3_preprocess.R:18-27`, `v3_fit.R:120-125`,
`cpp_exact_count`) and FIN `s1_setting.tex:24` resolve to the quoted content. CITECHECK: TOTAL MISSES 0 (a location/status
check, correctly described as such). New lemmas carry "PROVED (by this seat, unchecked)" with their check records.

**(G5) Constants/rates tracked — PASS.** j₀, m̄_n, k̄_n, φ₀² = φ²/2, g₀ = 1, M, BM envelope; t*, (K₁, t₁), (K₂, t₂); d_n, R_n,
r_n, κ_D, b_n, η_n, c_n; VN κ's for V1–V4; ENUM's threshold (5H₀ + 4N₀ ≥ 4n). Rate √(log n/n). Scope rule respected.

**(G6) Fidelity to the method as coded — PASS.** Exact branch decided on the post-preprocessing (n, p) by the saturating
count with N₀ = max(2500, n, p), H₀ = ⌈512N₀/2500⌉, K = min(p, ⌊n/2⌋) (`v3_preprocess.R:19-31`, `v3_core.cpp:72-85`);
exact branch returns before setup/LS0 with provenance phase = exact (`v3_fit.R:120-130`); LS0 cap ℓ_n + |S̃₀| is the
default (`v3_core.cpp:403-475`); B = min(isqrt n, isqrt p, 16) ≤ 16 as Theorem LOC/VN require. (FIN `s1_setting.tex:20`
still says LS0 is "not merged to main"; that is the source chapter lagging the 4676af6 merge, not a W2-APP defect.)

## Score: 9.1 / 10

All mathematics re-derives; every round-1 and round-2 blocking issue is genuinely fixed, including the (EXB) override
throughout the map. Deductions are for Part-2 conclusion-level asymmetry and a headline phrase that drops a hypothesis
(issues 1–2), plus housekeeping.

## Issues

1. **MINOR — `EMPIRICAL.md:61-63, 76-82, 84-89`; `REPORT.md:38-45, 95-98`. The fixed-p reading is applied to iclaims only,
   and there without the iid-Gaussian caveat.** Lemma ENUM (ii) gives: for ANY fixed p, (EXB) holds for all
   n ≥ 2^p/(4p). Under a fixed-p asymptotic model (the natural one for a fixed set of measured variables), all eight
   designs are therefore eventually on the exact branch and covered by ENUM + POST given a positive population floor
   (onsets n ≈ 10^{1.4} (iclaims), 10^{15}–10^{17} (spam/digits/diabetes), 10^{27} (FRED-MD, tecator), 10^{48} (FRED-QD),
   10^{1226} (riboflavin); `C3_scratch_opus/checks_out.txt`; onsets are irrelevant under the scope rule — this is exactly
   C-GROW's (C5)(b) caveat). Consequences: (a) the local/pervasive classification of Part 2 is informative only for
   growing-p models — REPORT:39-40 says so for the pervasive designs ("for growing-p models of them") but not for the
   local ones or tecator; (b) tecator's "appropriate asymptotic model is not decided" (REPORT:42, EMPIRICAL:80-82) omits
   that in the fixed-design branch of that dichotomy it IS decided (ENUM + POST; EMPIRICAL:80-81 itself notes the fixed
   positive floor); (c) iclaims is singled out as "settled by Lemma ENUM + POST" (EMPIRICAL:62-63), but iclaims is a
   weekly time series (serially dependent rows) — the same iid-Gaussian caveat of EMPIRICAL:38-40 applies, and the
   caveat's parenthetical list names FRED but not iclaims. **Fix:** one sentence in EMPIRICAL's "Nature of this part" and
   in REPORT §4's note: "In a fixed-p model every design here is eventually on the exact branch (Lemma ENUM (ii)) and is
   covered by ENUM + POST under a positive population floor; the classification below matters for growing-p models";
   for iclaims replace "settled" by "covered in a fixed-p iid-Gaussian model (iclaims rows are serially dependent)"; add
   the fixed-design case to tecator's reading. No new proof.

2. **MINOR — `REPORT.md:21`. "Small p (any correlation structure)" drops POST's hypothesis.** ENUM transfers POST's
   conclusion, which requires LSF (for fixed p: λ_min(Σ_n) ≥ ψ_n with ψ_n√n/(log n)^{3/2} → ∞). Counter-reading: fixed
   p = 2 with ρ_n = 1 − n⁻² (L1_POST Remark 1's own example) is "small p" with a correlation structure for which no claim
   is proved. The table row (REPORT:74 "holds under LSF") and L6_ENUM:28 ("given POST's hypotheses") are correct; the
   headline is not. **Fix:** "Small p (any correlation structure with a posterior-level floor, LSF)".

3. **NIT — `EMPIRICAL.md:61`. "every pair > 0.7" for iclaims is false as written:** recomputed pairwise |r| range is
   [0.698, 0.899] (min 0.6978). Say "every pair ≥ 0.69" (or "> 0.69").

4. **NIT — `numerics/LEAD_READING.md:28`. "V3b (Σθ* = 0)"** — residue of C2 Opus issue 4 (disposition says fixed); write
   Σ_kθ*_k = 0, as in NUMERICS_LOC_VN:10 and L4.

5. **NIT (housekeeping) — `REPORT.md:3-4, 7, 120`.** REPORT:7 "Statement changes vs the brief: none beyond R01's lock
   changes" contradicts §2 (ENUM = "a substantive addition" after council r1); the RESULT line has an unbalanced
   parenthesis ("…all PASS); round 2 not passed: …PASS)") and §6 still says "Council: (pending)" — finalise both with this
   round's outcome.

6. **NIT — `EMPIRICAL.md:65-66` (and SUMMARY.md:95, Table 2 "null ref max abs r").** "The largest |r| among 8.4·10⁶
   independent pairs at n = 71 would be ≈ 0.67" — 0.67 is the crude envelope √(2 log N/n) (`make_summary.R:25`); under the
   same independent-pairs heuristic with the exact null law of r, the median of the maximum is ≈ 0.585 and P(max > 0.67)
   ≈ 0.0014 (`C3_scratch_opus/checks_out.txt`). Say "at most about 0.67 (crude bound; typical value ≈ 0.59)". Labelled a
   context statistic, so no conclusion changes.

7. **NIT — `lemmas/L6_ENUM.md:15-17`.** Optional clause from C2 Opus 6 still absent: on the exact branch the preflight can
   return `resource_limit` (time ∝ 2^p); this lies in U_n and is covered by the no-delivery convention. One clause.

## Which issues would change my score

Fixing 1 and 2 would raise my score to about 9.3 (both are one-sentence summary corrections; 1 is the only point where a
Part-2 conclusion is asymmetric with what Lemma ENUM already proves). Issues 3–7 are cosmetic (≤ 0.1 combined). None is
gate-blocking: all six gates PASS, score 9.1 ≥ 8.0 — **council PASS from this seat.** I found no reason to change the
POST, CT/CD, LOC, LOC-B, VN or ENUM proofs.

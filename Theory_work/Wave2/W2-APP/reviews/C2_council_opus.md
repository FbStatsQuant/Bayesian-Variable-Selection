# W2-APP — Council round 2, Claude Opus 5.5 seat (fresh reviewer; verbatim reply)

Scope read: STATEMENT v1.3; lemmas L1_POST, L2_CT, L3_LOC (full; LOC-B against C-GROW `lemmas/L2_NA_TL.md` L2.2/L2.3(a)),
L4_families, L5_VN, L6_ENUM (new); EMPIRICAL; REPORT; numerics/LEAD_READING (+ n3_merged.csv, n3_results.csv,
n3b_results.csv, vn_bound_recheck_out.txt); data_diag/SUMMARY.md (+ erratum) and summary_table.csv; reviews/CITECHECK.txt;
C1_council_sol.md, C1_council_opus.md, C1_disposition.md. Sources checked: FIN `s1_setting.tex:20-28` (LS0, reported HPM,
output event 𝒪/U_n), `s3_posterior.tex:23-33` (SL0 incl. (iv)); C-GROW STATEMENT (C5)(b) caveat (lines 134-138);
production `v3_preprocess.R:17-33`, `cpp/v3_core.cpp:72-85` (cpp_exact_count), `v3_fit.R:100-131` (branch decision on
post-preprocessing (n, p); exact branch returns before setup/LS0), `cpp/v3_core.cpp:465-480` (LS0 only when status
"completed"; cap ℓ_n + |S̃₀| default).
Independent checks (scratch `reviews/C2_scratch_opus/`): `enum_boundary.py` → `enum_boundary_out.txt` re-implements the
coded exact-branch rule (saturating Σ_{k≤K}C(p,k) ≤ (5H₀+4N₀)p) and computes the largest enumerated p for n = 10⁴…10⁶⁰;
n3 tallies (52 runs: 24 complete-scan + 16 screened VN-example runs + 12 controls; all ls_final_eq_S0) re-derived from
n3_results.csv / n3b_results.csv; Part-2 key numbers re-read from summary_table.csv (all match REPORT §4 / EMPIRICAL).

## Round-1 issues — status
| Round-1 issue | Fixed? |
|---|---|
| Sol 1 (enumeration override) | Yes in substance: Lemma ENUM + new row + overrides. Residual boundary overstatement — issue 1 below. |
| Sol 2 / Opus 2 (polynomial-tail qualifier) | Yes (REPORT row (c)-poly; L4:161; body L4:89-94). |
| Sol 3 (screened "certified") | Yes (REPORT:32-34, LEAD_READING:30-33; tallies reproduce: 24 + 16 + 12). |
| Sol 4 (dangling vn_onset file) | Yes (REPORT:104; CITECHECK now checks named deliverables, 0 misses). |
| Opus 1 (method-failure wording) | Yes (REPORT:35-36). |
| Opus 3 (premises / no delivery in headline) | Yes (REPORT:13-16). |
| Opus 4 (block splitting ↔ VN) | Yes (REPORT:72-75; EMPIRICAL:66-69, 88-90). |
| Opus 5, 6, 7, 8 | Yes (EMPIRICAL:40-41, REPORT:79, EMPIRICAL:45-46, L2_CT:67-68 / L4:86). |
| Opus 9 (RESULT line) | Still provisional, as expected before this council (issue 5). |

## Gate verdicts

**(G1) Correctness — PASS.** POST (m̄_n via C(p,k)/C(2p−1,k) ≤ (2/3)^k and R_m ≤ 2(2p)^{s₀}(2/3)^m; Weyl with
k̄_nħ_n = O((log n)^{3/2}/√n) = o(ψ_n); diagonal tightness transfer), CT (S(t*) = α/2, Schur test, Neumann ‖A_t⁻¹‖ ≤ 2/α),
CD ((Θ_VV)⁻¹, two CT applications, constants depend only on (c, C, K, a)), Theorem LOC's delta proof and the new NA window
argument L3.6 (exact identity (I − P_T)x_l ∝ (I − P_T)Ce_{T′}; v_{T,l} ≤ κ_D(log n)⁻²; Laurent–Massart x = n/2 gives ≤ 4n;
η_n = O((log n)^{−1/2}); 2 log(2N) = 2 log p + O(log log n) < c_n), LOC-B (exact cross-group zeros; NA via GROW L2.3(a),
whose hypothesis is exactly |𝒫| ≤ (1 − δ₀) log n — matched by (B-χ) including the post-enlargement clause), VN (increment
≥ −log(2p) − ½log(n+1) − 2κ_E + nκ_n/4; V1 spectrum {½, 1, 3/2}, Cov(W_l, W₁ | W_U) = r_n; V2/V3 Schur complement
ρ(1−ρ)/(1+(u−1)ρ); V4 Var(f | W_U) = (1 + Σb_u²/ψ_u)⁻¹), the L4 non-LOC counting argument, F1–F4, and the new Lemma ENUM
((i) 2^p ≤ n^{c log 2} < 4n ≤ threshold; (ii) SL0(iv) ⇒ S₀ unique maximiser of F on the fully scored Ω; liminf identity)
are all correct as proved. The only correctness-adjacent defect is a map label: the "unproved" complement of ENUM's
sufficient condition contains sequences that the coded rule enumerates (issue 1) — "unproved" is defensible as a
statement about the corpus, so I do not fail the gate on it, but it must be fixed.

**(G2) Hypotheses used = hypotheses stated — PASS.** LSF (i)/(ii) exactly as used; (LOC) + PTV(|U| ≤ 15) exactly as in L6.5
and L3.2; LOC-B's (B-χ) incl. the enlarged-Q clause exactly what L2.3(a) needs; VN's (F16) on |S| ≤ 16 + s₀ and VNF over
null-only U; ENUM uses only EX-A, POST's conclusion and the coded counting rule.

**(G3) No hidden assumptions — PASS (with a Part-2 caveat, issue 3).** Part 1 retains Gaussian rows, independent noise,
fixed s₀/θ-bounds, uniform constants and named implementation premises everywhere. Part 2's "resembles the covered class"
conclusions are correlation-pattern statements that never mention that none of the eight designs plausibly has Gaussian
rows (counts, binary, polynomial features) — a design hypothesis of every theorem here. Descriptive framing keeps this
from being gate-level.

**(G4) Cited lemmas: adequate status, verbatim — PASS.** ENUM's citations verified: `v3_preprocess.R:18-27` (budget and
exact-branch rule), `cpp_exact_count` (`v3_core.cpp:72-85`, K = min(p, ⌊n/2⌋), saturating sum), `v3_fit.R:120-125`
(enumeration, provenance phase = exact), FIN `s1_setting.tex:24` (status exact ∈ 𝒪), SL0(iv) (`s3_posterior.tex:24`),
C-GROW STATEMENT (C5)(b) caveat. All other statuses as in round 1 (CITECHECK 0 misses; verbatim strings spot-checked).
ENUM's own status "PROVED (by this seat, unchecked)", check record = this council: adequate; I verified it.

**(G5) Constants/rates tracked — PASS.** j₀, m̄_n, k̄_n, φ₀², g₀, M, BM envelope; t*, (K₁,t₁), (K₂,t₂); d_n, R_n, r_n, κ_D,
b_n, η_n, c_n; VN κ's for V1–V4; ENUM threshold asymptotics (5H₀ + 4N₀ ~ 5.024n). Rate √(log n/n). Scope rule respected.

**(G6) Fidelity to the method as coded — PASS.** Branch decided on the post-preprocessing (n, p) by the coded saturating
count; exact branch returns before setup and LS0, so Ŝ⁺ = the enumeration HPM under (F, −|S|, lex); LS0 runs only on
status "completed" with cap ℓ_n + |S̃₀| (default), start mode by enumeration (cap 10⁶) with tie-aware DP — covered by the
named premise "emitted centre a maximiser of γ₀"; partition B = min(isqrt n, isqrt p, 16) ≤ 16 as Theorem LOC requires.

## Score: 8.9 / 10

The new mathematics is sound and every round-1 issue is genuinely fixed; ENUM is correct and faithful to the code. The
deductions are for map/summary-level statements that still slightly outrun or under-qualify what is proved (issues 1–3),
plus housekeeping.

## Issues

1. **MINOR — `lemmas/L6_ENUM.md:13-14, 25-28`; `REPORT.md:63` (row (c)-poly: "unproved for p/log n not bounded below
   1/log 2"), `REPORT.md:66-68`; `lemmas/L4_families.md:7-9`.** ENUM proves only the sufficient condition p_n ≤ c log n,
   c < 1/log 2, and the map then asserts "Outside this sub-regime the earlier statuses stand" / "unproved for p/log n not
   bounded below 1/log 2". The coded rule enumerates strictly more: for p ≤ ⌊n/2⌋ and n ≥ 2500 it is 2^p ≤ (5H₀ + 4N₀)p
   ≈ 5.024np, i.e. p − log₂p ≲ log₂ n + 2.33. Counterexample to the label: p_n = ⌊log₂ n⌋ + ⌊log₂ log₂ n⌋ (so
   p_n/log n > 1/log 2 eventually) is on the exact branch for every n checked from 10⁴ to 10⁶⁰ (`C2_scratch_opus/
   enum_boundary_out.txt`; largest enumerated p is 19, 27, 33, 40, 58, 74, 108, 142, 209 at n = 10^{4,6,…,60}, ratio
   p_max/log n ↓ 1/log 2 only at rate log log n/log n). Such sequences in rows (f), (g1), (g3), (c)-poly are covered by
   ENUM (ii) verbatim, yet labelled unproved. **Fix:** state ENUM (i′): "if Σ_{k≤K_n}C(p_n,k) ≤ (5H₀+4N₀)p_n for all large n
   (equivalently, for p_n ≤ n/2, 2^{p_n} ≤ (5H₀+4N₀)p_n), the exact branch is taken" with (i) as a clean sufficient
   corollary, and relabel the complements "outside the coded exact-branch regime" (or "not covered by ENUM's sufficient
   condition"). One line each; no new proof.

2. **MINOR — `REPORT.md:38-39`; `EMPIRICAL.md:57-59, 82-84`.** iclaims (n = 456, p = 10) is listed among the
   "pervasive-factor (posterior class; reported model per FAC)" / "reported-model theory awaits FAC" designs, while
   REPORT §4 (line 90) and EMPIRICAL:58-59 correctly say fixed p → enumeration + T03♯. Post-ENUM the headline and the HQ
   summary are inconsistent with the table; moreover, at its actual size iclaims is on the production exact branch
   (2¹⁰ = 1024 ≤ threshold), so the method enumerates it. **Fix:** headline: "riboflavin / FRED-QD / FRED-MD pervasive
   factor (posterior class; reported model per FAC); iclaims one-factor but p = 10 — exact branch, reported model by ENUM
   in any fixed-p asymptotic model". Same in EMPIRICAL:82-84.

3. **MINOR — `EMPIRICAL.md:35-55, 80-85`; `REPORT.md:37-41, 94`.** Part-2 conclusions ("local — resemble the covered
   class", "the patterns match the classes where POST and, under PTV, Theorem LOC apply") are drawn from correlation
   patterns only and never note that every theorem assumes iid Gaussian rows, which none of these designs resembles:
   spam = heavy-tailed word frequencies (SUMMARY:107 "raw heavy-tailed frequencies"), digits = integer pixels 0–16,
   diabetes-quadratic = a binary column plus deterministic polynomial features (x_j², x_jx_k are functions of other
   columns — no Gaussian-row model generates them), FRED = transformed macro series (time-dependent rows, not iid).
   REPORT:81 lists "non-Gaussian rows" only among unproved family extensions. **Fix:** one sentence in EMPIRICAL's
   "Nature of this part" and REPORT §4 note: "'Resembles' refers to the correlation pattern only; the theorems assume iid
   Gaussian rows, which these designs do not have (and FRED rows are serially dependent); the sub-Gaussian / dependent-row
   extensions are open."

4. **NIT — `REPORT.md:28, 67`; `lemmas/L4_families.md:47, 133-134, 142, 165`; `numerics/LEAD_READING.md:29`.**
   "|Σθ*| ≥ θ̄₀", "Σθ* = 0: no claim", "V3b (Σθ* = 0)" mean the coefficient sum Σ_kθ*_k, but L4:47 and L4:142 use Σθ* as
   the matrix–vector product (F3(iv): "Σθ* = (0, −1.5)ᵀ"; R06-2: "Σθ* ≠ 0"). Under the matrix reading "Σθ* = 0" is
   impossible for θ* ≠ 0 (Σ ≻ 0), making the no-claim clause and the V3b label vacuous. **Fix:** write 1ᵀθ* (or θ̄ as in
   L5 V3) in all sum uses.

5. **NIT (housekeeping) — `REPORT.md:3, 7, 44, 115, 126-127`; `STATEMENT.md:3`.** RESULT line provisional and "Council:
   (pending)" (to be finalised); REPORT:7 and :44 still say "STATEMENT v1.2.1 … none beyond R01's lock changes" although
   STATEMENT is v1.3 with claim (F) added after council r1; §8 file list omits `lemmas/L6_ENUM.md`. STATEMENT:3 should
   record v1.3 as a post-lock addition (it does) and REPORT §2 should list it as a statement change with its reason
   (Sol C1 issue 1).

6. **NIT — `lemmas/L6_ENUM.md:13-14`.** "(deterministically)": the decision uses the post-preprocessing p (`v3_fit.R:102`),
   which equals p_n almost surely for a continuous design (no constant columns); say "almost surely (deterministic given
   that preprocessing drops no column)". Also worth one clause: on the exact branch the preflight can return
   `resource_limit` (time ∝ 2^p · per-score cost) — this lies in U_n and is covered by the no-delivery convention, so the
   lemma is unaffected.

7. **NIT — `EMPIRICAL.md:20`.** "LB = rigorous lower bound (… λ_min(R) when p < n)": a floating-point eigenvalue is
   rigorous only up to O(ε‖R‖) ≈ 2e-14 here; harmless (tecator's 1.7e-11 ≫ 2e-14) but say "up to floating-point error
   O(ε p)".

## Which issues would change my score
Fixing 1–3 together would raise my score to about 9.2 (1 is the only one touching a table cell's truth; 2–3 are
conclusion-level qualifications of Part 2). Issues 4–7 are cosmetic (≤ 0.1 combined). None is gate-blocking as the files
stand: all six gates PASS, score 8.9 ≥ 8.0 — council PASS from this seat.

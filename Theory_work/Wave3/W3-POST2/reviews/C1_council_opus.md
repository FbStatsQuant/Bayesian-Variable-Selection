# W3-POST2 — Council C1, seat B (Claude Opus 5.5, high, claudeAgent)

Reviewed: REPORT.md, STATEMENT.md v1.2, ASSUMPTION_MAP.md v1.3, lemmas A–E, numerics (script and output), citecheck,
and the review trail. Sources were read directly: [T03R] PROOF.md §§1–7; [P3] PROOF_v2.tex §§1–5 (lem:red, smoother,
cor:diff, det, prior, signal, chi, Gprob, ongood, onesup, prop:sup); [P1] PROOF_v3.tex (lem:slab, spec, prior, thm:T01iii,
thm:Ta, lem:num, lem:den); W3-POST STATEMENT v1.4, REPORT §4, L1a′; code `v3_score.h` (data_init, finish_from_factors);
Song–Liang printed pp. 952–954; PROTOCOL.md, HQ_DECISIONS.md.
I treated every earlier verdict as a claim to check. Scratch: `reviews/C1_scratch_opus/` (`chk.py`, `consts.py`). No
git state changes.

## Verdict

**Score: 8.6 / 10 (uncapped). All six gates PASS. → PASS (≥ 8.0, 6/6).**

I re-derived every changed step and found no FATAL or MAJOR defect. Every one of A1, A2, B, C, D(a), D(b) and E holds
as stated. The findings below are about traceability, wording and one unproved (true) bookkeeping line.

## What I re-derived (independently)

- **A0.** (i) is [P1] `lem:spec`(e). (iii) The map d ↦ (xj/d)^{d/2} is increasing on 1 ≤ d ≤ j because x = eC_A log n > e,
  so a_J ≤ (2eC_A log n)^{j/2}. Combined with [P3] `lem:prior`(b) and (ADG), this gives exactly 2(j+1)^{s₀}q̃_n^j. The
  amplified tail uses (j₀+1)/2 ≥ s₀(A+½)+1, which holds because j₀ + 1 ≥ (2A+1)s₀ + 2.
- **Lemma M.** E[e^{χ²_d/2}1{χ²_d ≤ τ}] = (τ/2)^{d/2}/Γ(d/2+1) ≤ (eτ/d)^{d/2}. Absorbing e^{jε_n} ≤ 2^{j/2} needs
  e^{2ε_n} ≤ 2, which is the reason for the 2^{|J|/2} factor in a_J.
- **(G3′) and (C4′).**
  - Rank domination ([P3] `lem:chi`(a), last claim) keeps the (G3) union bound valid for any rank.
  - (B3) needs the floor on S₀ only; M_T ⪯ (n/(n+1))P_T holds for rank-deficient T.
  - `lem:ongood`(b) uses (G1) and (G2), and (G2) never needs full rank.
- **(C5′) and (C8′).** Υ′ has deterministic weights. The expectation bound follows termwise. (C8′) puts (C6)(a), which
  has no condition, on |J′| > j₀, and the second (OS) inequality controls that term.
- **A2.** Q_S ≤ Q_{S₀} for S ⊇ S₀ ([P1] `lem:spec`(d); h is operator-monotone). Hence π(S_J)/π(S₀) ≥ prior ratio × det
  ratio, and δ_n ≥ (1 − δ_n)𝒪⁰_n.
  - The j = 1 term gives [LB] because (p−s₀)(s₀+1) ≥ 2p−1−s₀ ⟺ (s₀−1)(p−s₀−1) ≥ 0.
  - Numerically, over 400 random coded posteriors (exact enumeration, rank-deficient designs included), min(δ_n −
    𝒪⁰/(1+𝒪⁰)) = 7·10⁻¹⁰ ≥ 0.
- **B.**
  - y_c − X_{c,T}ϑ = ε_c + Uᵀr, with ‖Uᵀr‖ = ‖r‖ and ε_cᵀUᵀr = εᵀr (r ∈ 1^⊥).
  - The [P1] `lem:den` exponent bound needs only Q^c ≤ σ*²E′ + (a nonnegative quantity).
  - E Λ″ ≤ C″_Λ(B) by linearity.
  - `thm:T01iii`, `lem:num` and `thm:Ta` never use μ ∈ col X. I checked their proofs: (n−1)s_y² = ‖μ‖² + 2μᵀε + ‖Cε‖² holds
    for any centred μ.
- **C.**
  - *C1.* F(1) = 0, F′(1) = (E′−N)/2 and F″ = N/(2u²) − E′/u³. On I ⊆ [3/4, 5/4] with E′ ≤ 2N, |F″| ≤ 0.89N + 4.74N ≤
    6N. The data-dependent window makes the linear term ≥ 0, so F ≥ −3.
  - *ρ̄.* ‖θ*‖² ≤ nM/(Nφ₀²) ≤ 1.5M/φ₀², so ρ ≤ M + 1.5M/(nφ₀²) ≤ ρ̄.
  - *Laurent–Massart.* N + 2√(N·N/8) + N/4 ≈ 1.96N ≤ 2N.
  - *C2.* The bound is a deterministic multiple of N_m ≥ 0, so E N_m = ϖ(E_m) suffices.
  - *Main bound.* δ_n ≤ T₀ + T_sup + T_U covers every S ≠ S₀. Each term has expectation O(r_n) with deterministic κ̄_n.
- **D.**
  - *H² inequality.* 1 − AB ≤ (1−A)+(1−B) because the difference is (1−A)(1−B) ≥ 0. Numerically, over 2·10⁵ random
    pairs the minimum slack is 8·10⁻⁷ ≥ 0.
  - *D1(a)–(d).* Re-derived. Numerically, D1(b) and D1(d) never fail in 56 842 (S, design, e) cases.
  - *D2.* The IG moments and Chebyshev step check out: Var = (Ev)²/(ν−2) ≤ 4(Ev)²/n for n ≥ 8.
  - *D3.*
    - The decomposition Ω∖𝒮_n ⊆ tail ∪ supersets ∪ 𝒰_far is complete.
    - The S₀ cross term is deterministic on (G2*), since a₀ ∈ col X_{c,S₀}.
    - E[v | S, y] − σ*² has the stated exact form.
    - C_H = 8σ*²(C_A(s₀+j₀) + c₂) + 1 and C′_H follow.
- **E1.**
  - The exact decomposition Q^c_S = L_S + 2eᵀ(I−M_S)μ_c + eᵀ(I−M_S)e holds, and L_S = min_ϑ B_S(ϑ).
  - The chain D ≥ L_S − 2|cross| + ‖P_{S₀}e‖² − ‖P_{S′}e‖² − R_n holds for every e. Numerically, over 56 842 cases
    (exact and near dependence included), min(lhs − rhs) = 6·10⁻⁷ ≥ 0.
  - B′ ≤ E_n of [P3] `lem:ongood`(c). The prefactor is ≤ n^{s₀(A+1)} for n ≥ 5.
  - The union bound for 𝒢⁵_n gives (2/e)^{s₀}(p/n^A)^{j₀}/n ≤ 1/n.
  - The c₁ algebra: φ(c) > (2/log 2)(s₀(A+1)+2) ⟺ √c > √(2C_x) + √(2C_x + C_A j₀ + …). At s₀ = A = 1, c₁ = 160.8 is
    reproduced.
- **G6.**
  - `v3_score.h` matches [W3P] §0: K = min(p, n/2); ν = a₀ + n/2; H = (n+1)G + I and A = G + I; Q = yᵀy − n zᵀH⁻¹z;
    log w(k) = −log 2 − log C(2p−1, k).
  - `post2_checks.py` implements the same target.
  - The D parameter posterior is the exact working-model joint posterior. Its S-marginal is the coded π, and shape
    ν = 0.51 + N/2 is the contrast form of [P1] `thm:T01i`.

## Gates

- **G1 correctness — PASS.** Every changed step re-derived, as listed above. One true but unproved bookkeeping line
  (F5).
- **G2 hypotheses used = stated — PASS.** I checked each claim's proof against its statement:
  - A1 uses (F_λ) only in (C10) and 5(b). 5(a) uses only G, (E), (F₀) and (OS).
  - C's three cases use exactly their listed hypotheses.
  - D(b) uses no (F_λ), (ID), (G4) or beta-min; E1 is invoked at c₂ = c₁+1 as a lemma, not as a hypothesis.
  - E never uses (G4) or (F_λ).
- **G3 no hidden assumptions — PASS.** The thresholds n₀ depend only on the listed constants. The one implicit fact
  (m♯_n ≥ min(j₀, K)) is true uniformly over 2 ≤ p ≤ n^A (F5). s_y > 0 is a.s.; A2 holds wherever π is defined.
- **G4 cited statuses — PASS.**
  - [P1] and [P3] are locked; [T03R] is "PROVED; SF/XF VERIFIED".
  - [L1a′] and [LB] are HQ-labelled PROVED-CHECKED. [POST] (item 6 only) carries the status inherited by [W3P].
  - Citecheck re-run: 120 checks, 0 failures.
  - The new results' own statuses are verbatim, but their check records are not filled (F2).
- **G5 constants/rates — PASS.** c₁ = 160.8 and C_x = 8.609 reproduced; C_H, C′_H, c_den, C″_Λ(B) and q̃_n re-derived.
  On the grid s₀ ∈ {1, 2, 3, 5, 10}, A ∈ {1, 1.5, 2, 3, 5}, c₁ > c₀ throughout (`consts.py`), so the "coexists" range is
  non-empty there (F8).
- **G6 fidelity to the coded target — PASS.** The target matches the code, as above. Claim D's distance is
  intercept-free, which should be said and is harmless (F4).

**Relation claims.**

| claim | relation claimed | my check |
|---|---|---|
| A1 | implies [W3P] Thm 1 | correct, via (F_w) ⇒ (DG) ⇒ (ADG) ⇒ (OS), n ≥ n_OS |
| A2 | implies [LB] | correct (computation above) |
| B | implies [L1a′] | correct; it also implies Lemma 1a *exactly*, not only "up to constants" (F7) |
| C, D | new | correct |
| E | supersedes items 1–4 for c > c₁ (via (F_λ) ∧ BM(c) ⇒ (ID; c(1−1/n)) ⇒ (ID^M)) and (F_w) ⇒ (OS) | correct |
| E | coexists for c₀ < c ≤ c₁ | correct, given c₀ < c₁ (F8) |

**Sharpness record.** It is honest and matches `post2_checks_out.txt`, which I checked line by line: N1, N2, N4, N5,
N6/N6b, N7, N8 and A2's 0 violations. Finite-n observations are labelled as such.

**Scope flag.** Honest in substance, but under-counted (F1).

## Findings

1. **MINOR — the scope flag lists two adoptions, but there were three.** `REPORT.md:14-21`
   - The flag lists two strengthenings, and line 21 says "No other proposal was adopted".
   - But `STATEMENT.md:1` ("v1.2 = sharpness-gate adoptions from R03b [C+, D+, E ridge margin]"), `REPORT.md:155` and
     `reviews/R03b_disposition.md` (row "—", ADOPTED for Claim E) record a third adoption: E's hypothesis was weakened from
     (ID) to (ID^M), and E1 was re-proved (v2).
   - This also bears on `REPORT.md:12` ("closed within its kill budget"; budget = lock + one proof attempt,
     `STATEMENT.md:138`).
   - *Fix:* add "item 5: (ID) → (ID^M) (ridge loss), E1 v2" to the flag, and delete "No other proposal was adopted". State
     that E1 v1 was the proof attempt and v2 a sharpness-gate restatement under its own line check (K2), so HQ can rule on
     the budget.
2. **MINOR — the check records in the lemma files were never filled.**
   - `lemmas/A_occam.md:3` still reads "Check record: see LOG.md / reviews (filled as checks return)". B:3, C:4, D:4 and E:4
     point only to "LOG.md / reviews".
   - `STATEMENT.md:6-7` makes each status depend on "the check record in that file".
   - *Fix:* write a per-file check record, as [L1a′] does:
     - A: K-AE (VERIFIED-WITH-AMENDMENTS), M01, S01;
     - B: K-BC;
     - C v2: K2 VERIFIED, M01;
     - D v2: K-D, K2;
     - E v2: K-AE, K2.

     List each with its disposition, and keep the status words verbatim.
3. **MINOR — the brief is not in any file ("no claim without a file").**
   - `STATEMENT.md` and `REPORT.md` cite "brief item 1…5", but no file holds that numbering.
   - `HQ_DECISIONS.md:7` uses W3-POST REPORT §4 numbering: "1, 3, 4, 1b; 2 as stretch". In that numbering, Claim B is §4
     item 3 and Claim E is §4 item 2, not items 2 and 5.
   - The substance matches.
   - *Fix:* add a mapping line to STATEMENT or PLAN: A = §4.1, B = §4.3, C = §4.4, D = PROGRAM 1b / §4.11, E = §4.2
     (stretch).
4. **MINOR — Claim D's "in-sample predictive" Hellinger is intercept-free (G6 wording).** `STATEMENT.md:99-104`,
   `D_hellinger.md:8-17`
   - h̄_n compares N(μ̂_i, v) with N(μ_i, σ*²) on the centred scale.
   - The coded model's plug-in law for y^r_i is N(ȳ^r + μ̂_i, v), and the truth is N(α* + x^r_iβ*, σ*²).
   - *Fix (one line, rates unchanged):* the full mean error is ε̄1 + (μ̂ − μ), and the two pieces are orthogonal because
     μ̂ − μ ∈ 1^⊥. Hence
     h̄²_{int} ≤ (v/σ*² − 1)² + ‖μ̂ − μ‖²/(4nσ*²) + ε̄²/(4σ*²), with nε̄²/σ*² ~ χ²₁.
     So D(a) and D(b) hold verbatim for the intercept-inclusive distance. Alternatively, rename the distance "centred
     in-sample Hellinger".
5. **MINOR — m♯_n ≥ min(j₀, K) is used but not proved.** `E_visibility.md:39`, `D_hellinger.md:53`
   - The lemmas assert "j₀ ≤ m♯_n for n ≥ n₀, or K = m♯_n" without proof. (G3′) is needed for |J′| ≤ j₀.
   - It is true uniformly in 2 ≤ p ≤ n^A. For m < min(j₀, K):
     R_m ≥ q_{m+1}/w(s₀) ≥ 2 Π_{i≤m}(p−i)/(2p−1−i) ≥ c(j₀) > 0.
     The bound c(j₀) holds because each factor is ≥ 1/4 when p ≥ 2j₀, and otherwise the product is ≥ (4j₀)^{−j₀}. So
     R_m > n^{−(s₀+2)/2} for n ≥ n₀(s₀, A).
   - *Fix:* add this line (or a pointer) to E1(b).
6. **NIT — registry rows carry two relation labels.** `REPORT.md:101-102`
   - Row A2: "implies … coexists as a separate converse". Row A1: "implies … supersedes".
   - *Fix:* use one label per row (A2 **implies** [LB]; LB is its j = 1 corollary).
7. **NIT — B implies Lemma 1a exactly, not just "up to constants".** `STATEMENT.md:77-78`
   - With T = S₀ and ϑ = θ*, B ≤ M + M/(2φ₀²), so C″_Λ ≤ C_Λ. Also Θ♯ = Θ″√D_{S₀}/(n+1)^{s₀/2} ≤ Θ″.
   - *Fix:* say "implies [W3P] Lemma 1a".
8. **NIT — c₀ < c₁ is shown only at s₀ = A = 1.** `STATEMENT.md:132`
   - The "coexists for c₀ < c ≤ c₁" sentence needs c₀ < c₁ in general.
   - *Fix:* add "c₀ < c₁ on the grid s₀ ≤ 10, A ≤ 5 (numerical)", or bound c₁ ≥ 4C_* analytically.
9. **NIT — housekeeping.**
   - `REPORT.md:162` says "119 checks"; `CITECHECK.txt` and my re-run say 120.
   - `A_occam.md:4` cites "STATEMENT (v1.1)".
   - The N5 header in `post2_checks.py` / `post2_checks_out.txt` keeps the v1 phrase "bounded ⇒ e^(C√log n) is an
     artefact".
   - `ASSUMPTION_MAP.md:182` and `D_hellinger.md:84` write SL's dimension exponent as ξ. SL uses α (P_n < exp(Cn^α)); SL's ξ
     is a model index.
10. **NIT — two overstatements in the REPORT.** `REPORT.md:39-40`, `REPORT.md:143`
    - "Rank loss costs nothing": only the χ² part is free; rank loss is still charged through D_{S₀}/D_{S_J} in (OS).
    - "D(a)'s 1/n scale cannot be improved for the mean part" rests on the conditional-Gaussian-spread argument in D4
      Remark 2, not on a proved lower bound.
    - *Fix:* reword both, e.g. "(argued, D4 Remark 2)".
11. **NIT — PROTOCOL rule 8 (registry block, per-clause statuses).** `REPORT.md:6-7`
    - The rule applies from 2026-11-10. If the council closes on or after that date, add the block with one status per
      clause (A1, A2, B, C, D(a), D(b), E).
12. **NIT — B Remark 4 cites the wrong part of `lem:prior`(c).** `B_tail_approx.md:54`
    - The statement of [P1] `lem:prior`(c) bounds ϖ(|S| > m) and gives R^∅_m ≤ 2^{2−m}.
    - The cited 2^{1−m} comes from the proof line Σ_{k>m}q_k ≤ 2^{−m}.
    - *Fix:* cite that line, or use 2^{2−m}. Nothing downstream changes.

## Why 8.6, not higher

The mathematics is clean and, as far as I can push it, correct. The rates are well chosen, and the sufficient/necessary
split in A is genuine (A2 is deterministic and short). Two things keep the score down:
- **Process hygiene.** The scope flag is under-counted (F1), the per-file check records are empty (F2), and the brief
  numbering is in no file (F3). Under this protocol these matter.
- **Two loose ends.** One silent bookkeeping step (F5) and the intercept-free naming in D (F4).

None of these affects a hypothesis, a rate or a constant.

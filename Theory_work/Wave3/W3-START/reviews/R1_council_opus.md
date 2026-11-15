# W3-START — council round R1 — seat `opus` (Claude Opus 5.5, effort high) — blind first read

Reviewed content: `MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97`
(`python -B Theory_work/Wave3/tools/manifest.py verify …` → `verify: OK`, run at the start of the review). I read only
the files in the manifest, the manifest itself and `reviews/INPUTS.txt`. I read no LOG, checkpoint or other review
file.

## Verdict summary

I tried to break the package and could not. I re-derived every step on which the main results rest: the
fibre bound (L1.1) with its path bound (P3) and the bookkeeping |S| = |T| − D + E + a′ and E ≤ 15s₀; the two-sided
identities (AGG-b), including both prior estimates behind o₀ ≥ c_sΞ; (AGG-c), (AGG-d); the ridge and Schur arguments
of (FLOOR); the score expansion of Lemma TK under the unnormalised floor ((E1), (E2), (E4), (TK-a)–(TK-f)); the
small-gain linearisation L3.3 and the Markov step L3.4; Steps 1–7 of L4.1 (constants ε₁, (4.1), price Π) and the chain
of L4.2; the probability accounting and the uniformity of L5.2; the Gaussian-row bridge L9.1–L9.7 (Schur
perturbation, localisation identities, population regression, the conditional law (9.1) given σ(W_D), the Gaussian
integral giving Φ_n, the assembly through (F2) and Markov); the transfer L8; Proposition OVL; example F-2. Every
inequality I checked holds as written, and every constant has the dependence the statement claims. The hypotheses the
proofs use are the ones stated. No hidden independence, normalised floor, s₀ ≥ 1, A ≥ 1, non-measurable conditioning
or response-dependent level appears. Every quoted status is verbatim from `claims.tsv`, nothing from another ticket is
used as a premise, the W3-SAMP interfaces are quoted correctly, and the coded π₀ matches the pinned code. My issues are
all NON-BLOCKING. The two that matter most: the finite-n vacuity of the F4 levels, which is recorded in the numerics
but not in the statement or report, and a stale assumption map. **All six gates pass. The package is acceptable as
checked mathematics as it stands.**

## Gate table

| gate | result | what I re-derived / checked |
|---|---|---|
| G1 correctness | **PASS** | **L1:** (P1)–(P5), (CH); L1.1 line by line: the decomposition T(S) = (S ∩ Q) ∪ S₀, the per-block identity \|U_b\| = \|T_b\| − d_b + a_b, a_b ≤ 15, D ≤ s₀ ≤ \|T\|, the (P3) premises k − D + a = \|S\| ≤ K ≤ p, (x)_E ≤ c_Q^E and (x + E)_{a′} ≤ (c_Q + 1)_{a′} from \|T\| + E ≤ \|Q\| + 15s₀, injectivity, and the use of (P5) over a superset. (AGG-a) by (P4). (AGG-b): items (i)–(iii), with R₂ exactly the a′ ≥ 2 tail, and the lower bound c_sΞ in both cases (d ≥ a: (p/s₀)^e ≥ (2p)^e(2s₀)^{−16}; a > d: ((s₀+1)/(2p))^e = (16s₀/p)^e((s₀+1)/(32s₀))^e ≥ (16s₀/p)^e 32^{−15}). (AGG-c): the factorisation over (S₀ ∖ S, N_Q, N_o). (AGG-d): both cases e_n^d(U_Q/2)^a and e_n^d(c_QU_Q)^{a−d}(U_Q/2)^d. (FLOOR): Q_S = yᵀy/(n + 1) + (n/(n + 1))ρ_S, D_{S∪l}/D_S = (n + 1)s(1/(n + 1))/s(1) ≤ n + 1, and 2(k + 1)(p − k) − (2p − 1 − k) = k(2(p − k) − 1) + 1. **L2:** (2.1); the three tail bounds and the counts (2^{d/2} ≤ 2⁸; 2^{16}p sets); (TK-a) through 2ab ≤ a²c + b²/c; (TK-b) with (n − 1)² ≥ n²/2; (E1) eigenvalue factors in [g_*/(g_* + 1), 1]; (E2) G⁻¹ − nH⁻¹ = G^{−1/2}(G + I)H⁻¹G^{−1/2} with eigenvalues ≤ (1 + 1/g_*)/(n + 1); (E4); (f1)–(f3). **L3:** (J0)–(J4); P(𝓩_hᶜ) ≤ b_n(h); the default budget = 1/(32 log n); (B1)(i)–(iii), including the ≤ 15 columns sharing a block with all of S₀ and the s₀ = 0 case; L3.3 (ς_n = O(n^{−1/3}log n)); the small-gain consequence of (J0); L3.4(a), (b) (E V = Σ J ≤ 2^{15}𝔏^b, max ≤ sum, so no independence is used); the F4 arithmetic, including h_l ≥ 1 (4 log log 4 > 1.3) and the default-level threshold (√(4A + 1) − √(2A))². **L4:** 𝓧 (≤ 3^{16} nested pairs per block); (Q±); L4.1: the instance map (V, D, R, N), \|U\| − \|T\| = a − d, both inequalities defining ε₁, Steps 2–6, and n₃'s dependence; L4.2: the chain, ε₁ ≤ (κ_V − κ)/(2c_V), and e_n ≤ 2^{−16}n^{−(κ_V+κ)/2}; Corollary L4.3 (c_Q ≤ 16s₀(\|Q\| + 1)). **L5:** (e1)–(e3) (Lagrange remainder with (1 − u)^{−c−2} ≤ (4/3)^{c+2}); (C1)(a)–(c); L5.2: (c_Q + 1)U_Q ≤ 16s₀′λc₀ = ¼, the 128/3 ≤ 43 step, P(𝒢ᶜ) ≤ ε/2 + b_n + ε/4 + ε/4, and C′; L5.3(a)–(c). **L6:** L6.0, L6.0′; F1 ((J2) exponent √(2Aη)); F2 (Schur-complement floor for Δ_U, (J1) with τ² − σ² = Δ_U, ϱ_n(S₀) = (s₀ + 1)n^{−1/4}(n^{−1/2}𝔏²)^{1/2}); F3; F4. **L7:** both chains, the choices of ε₁, and the (P1), (P2) prior factors. (N2)/(N3) reductions and the (N2) vacuity for s₀ ≤ 15. **L8:** the Fubini version of the conditional law and the inequality form L8.2. **L9:** L9.1 (polarisation, Laurent–Massart, union over p² pairs); (c1) 2h/(1 − h) ≤ 3h; (c2); (c3) term by term (15/c_Σ + 450/c_Σ² + 30/c_Σ + 1 = C_S); (c4); L9.2 (truths in U contribute 0; δ² ≥ Na_V²/4); L9.3 (δ = √Δ_U·g, J_n = F(g, a)); (F1), (F2); the L9.4 identities ρ̂_{U,l} = (z₀ − aᵀR⁻¹d)/√((1 − aᵀR⁻¹a)(1 − dᵀR⁻¹d)) and Δ_U = Δ_{U₀}(1 − dᵀR⁻¹d), λ_min(R) ≥ c_Σ/2, (1 − q)^{−1/2} ≤ 1 + q on [0, ½], C₄, C₅, and √(N log n)ε_n² → 0; L9.5: γ² as a partial-regression coefficient, Π = (I − P_{U₀})C, ΠW_l = m + Πe, ξ ⟂ R given 𝒲 (orthogonal projections of e), (9.1), E_R and E_ξ, and the exponent r²/(1 − s′²) − 1 = η_n(1 − a)/(a − η_n) ≤ 2η_n/a̲; L9.6 (P(Eᶜ), \|g\| ≤ G_n, ς′_n → 0, (9.2), and the constant C₆ (e·2^{16}·√2·√(2/π) ≈ 2.0·10⁵ ≤ 2^{18})); L9.7. **L10:** IF-START; OVL (i)–(v), P(𝓨ᶜ) ≤ q̄2^{16}/log n, and the P-OVL deduction; Lemma R′. **L11:** F-1, F-3 (λ_min = N(1 − cos φ_n) = d²/2), F-2 (q_k, q₁₅ = 1/11, both (V-m) cases, the (V-c) failure at U = {2,…,16}, q_k − q_{k+1} ≤ 0.24/1.4, the F4 rate 0.1(1 + 2A), and the default-level lower bound −0.1 − 0.2A + √(1.6A + 3.2A²) ≥ 0.318), G-1, G-2. |
| G2 hyp. used = stated | **PASS** | For each claim I compared what the proof uses with `STATEMENT.md` §5. (C0) uses only r_b > 0, the w formula, K ≤ p and blocks ≤ min(16, K). (C1) uses only the interfaces and (C0)/(T0). (C2) uses Setting F, (E) and quantitative [TK]. (B-TK) uses only (E) and (GF-blk); s₀ is not used. (B-L) uses (SG) from the displayed premise. (B-V1) uses (V-c) and c_QU_Q ≤ 1, which comes from (AL), and (AL) is listed. (B-V2) uses (V-m) only. (T1)(d)'s class matches L5.2. (T3)(a) matches L8.2/L8.3. (B-R) and (T3)(b) state p > s₀, as L9.2 requires. OVL's uniform ā is stated and used. (T6) is conditioned on the substituted hypotheses. The F2 normalised floor on S₀ is an explicit hypothesis. |
| G3 no hidden assumptions | **PASS** | No independence between Z_{T,l}: max ≤ sum (L3.4 remark 2), union bounds in 𝒟₂, 𝒟₃, 𝓧, 𝓨, and single witnesses in L7. The only independence used (ξ ⟂ R given W_D in L9.5) is exact. No normalised floor except where stated: F2, and L9 derives it. s₀ = 0 is handled (L2, L4.0, s₀′ in L5, 𝔏⁰ for s₀ = 0). p > s₀ is explicit. A ≥ 1 is not used: every step works for A > 0 (z̄_n² ≤ (2A + 1) log n eventually; F-2 uses A ∈ [0.1, 1]), but see Issue 1. Conditioning: L8 uses a regular conditional law; L9.5 conditions only on σ(W_D) and states that E_cov is not conditioned on. Levels, supports and sets: h, Q, a_{n,l}, I_n are deterministic (Setting F) or design-measurable ((T3)(a), (T6)); response selection is explicitly excluded. |
| G4 imports and statuses | **PASS** | I extracted the version and status columns from `claims.tsv` (awk on fields 1, 11, 12). C-GROW:L0.1/L0.2@1.0.0 "PROVED-CHECKED", W3-SAMP:C@1.1.1 and :D@2.1.1 "PROVED-CHECKED", W1-PXN:Thm-PXN(S)@1.0.0 "XF VERIFIED", C-MIS:LemR@1.0.0 "R02 VERIFIED; council R07/R08 PASS", W3-RM:B1, :B2tau, :SAND-R@1.0.0 "PROVED (by this seat, unchecked)", and the SOP:TH116 clause-(iii) substring are all verbatim. No other ticket's result is a premise: the toolkit, Lemma R′ and the Gaussian-row facts are re-proved, and the only external tools are textbook facts (Laurent–Massart, Gaussian MGF, noncentral-χ² dominance). SAMP quotes are checked against `W3-SAMP/STATEMENT.md`: :26-27 (δ̄ = max(o₀, o₁)), :76 (P-START), :82 (P-OVL), :103-104 (D-iv production form), :158-162 (C-v). IF-START delivers exactly 1_𝒜o₀ = O_P(r_n) with a deterministic r_n, and the r_n ↓ 0 requirement of (C-v) is addressed (sup_{m≥n}). OVL delivers only the production form, as stated. RM, GROW, MIS, PXN, SANDR and BRIEF citations match their line ranges in content. A scratch copy of `citecheck.py` gives 202 citations, 0 missing or out of range. |
| G5 constants and rates | **PASS** | Traced: t_n, q_n, ω̄_n(n, A) = O(n^{−1/3}); κ₁, κ₂, κ_E(g_*, M, σ²); n₁, n₂(A); g⁰_n, g_n, x̄_n, ς_n; ζ_n(s₀, n); ε₁, C₁, C₂ = 16 log(32s₀), n₃(κ, A, M, σ², g_*, s₀, c_m, ε₀), n₄(…, c_V); c_L = 2^{15}e^{2κ_E+1}, λ = 4c_L/ε, c₀, C = 43s₀′λ, C′; ε_n = 4/log n, giving C_n = O(log n) and C′_n = O((log n)²); Φ_n, C_B, C_R = C_B + 1, C₆. None depends on p, Q, the design or the partition beyond the stated constants. The (T1)(d) uniformity holds: n₀ = max(n*(κ), n_ε) (L6.0), and every event bound depends only on (n, A, s₀). It passes intact to (T3)(a), where L8.2 uses no union over supports, and to (T3)(b). |
| G6 fidelity to the code | **PASS** | Checked against CORE: `cpp/v3_score.h:14` (a₀ = b₀ = 0.01), `:39-72` (K = min(p, n/2), log w = −log 2 − lchoose(2p − 1, k), W_K, ϖ = w/W_K, log c_n, m(∅)), `:175-224` (H = (n + 1)G + I, A = G + I, Q = yᵀy − n zᵀH⁻¹z, log m = log c_n − ½(ldH − ldA) − ν log(2b₀ + Q)); `cpp/v3_start.h:68-70` (log γ₀ = log ϖ + Σ_b log r_b; log π₀ = log γ₀ − log Z̄₀), `:76-98` (tables against the full y, r_b(∅) = 1, skipped only when \|U\| > K), `:101-137` (size-profile convolution truncated at K = Σ_{V∈Ω}); `cpp/v3_blocks.h:124-144` (top-down cut and next-fit, blocks ≤ B); `v3_preprocess.R:22` (B = min(isqrt n, isqrt p, 16)), `:37-60` (standardisation equals (x − x̄)/sd with denominator n − 1 under EX-A), `:111-127` (constant columns dropped, y standardised); `v3_setup.R:67-69` (production uses the prescribed B); `cpp/v3_core.cpp:146` (B ≤ B_MAX). I confirmed B ≤ K for n ≥ 4. Git (read-only): the last commit touching CORE is 72785fe, and CORE is identical at d6da494 and fe9a066. |

## Per-claim table (ids of `REPORT.md` §3)

| id | decision |
|---|---|
| AGG | accepted |
| FLOOR | accepted |
| TK | accepted |
| LEAK | accepted with non-blocking remarks (Issue 4) |
| VIS-c | accepted |
| VIS-m | accepted |
| ASM | accepted |
| START-F | accepted |
| F1 | accepted |
| F2 | accepted |
| F3 | accepted |
| F4 | accepted with non-blocking remarks (Issue 2) |
| NEC-b | accepted |
| NEC | accepted |
| TRANSFER | accepted |
| BR | accepted |
| START-R | accepted |
| IF-START | accepted |
| OVL | accepted |
| MIS | accepted |
| EX | accepted with non-blocking remarks (Issue 2: F-2 is purely asymptotic; F-1, F-3, G-1, G-2 accepted as written; UNI-0/AR(1) correctly listed as not verified) |

## Issues

All issues are **NON-BLOCKING**; none needs to be fixed before acceptance.

1. **NON-BLOCKING — Setting F is described as equal to GROW's, but its range of A differs.** `STATEMENT.md:65-67`
   says "Setting F = GROW `STATEMENT.md:51-64` (D0, model G), with s₀ ≥ 0 allowed", then states "A > 0 fixed". GROW
   fixes A ≥ 1 (`Theory_work/Wave1C/C-GROW/STATEMENT.md:62`). The proofs do not use A ≥ 1, and example F-2 uses
   A ∈ [0.1, 1], so the content is right. Only the "=" sentence names one deviation and silently makes a second.
   *Repair:* "with s₀ ≥ 0 and any fixed A > 0 allowed".
2. **NON-BLOCKING — F4 and example F-2 are asymptotic only, and the statement does not say how far.** With the F4
   levels, the tail budget b_n(h) ≤ 1/(32 log n) + 2^{16}ī(log n)^{−2} is below 1 only for log n > 256. The o(1) in
   the exponent is of order √(log log n/log n). `numerics/lemmas/RESULTS_LEMMAS.md` records both facts ("the F4 bound
   becomes small only for astronomically large n"). (T1)(d)'s bound ε + b_n(h) is therefore vacuous at every
   simulable n under the F4 levels. The mathematics is correct. But `STATEMENT.md:277-286` (F4), `:363-366` (F-2
   entry), `REPORT.md:54` and `REPORT.md:137` ("reached from below by F4") present F4 without this caveat.
   *Repair:* add one scope sentence to F4 and to the F-2 entry, for example "an asymptotic statement only: the tail
   budget of these levels is below 1 only for log n > 256".
3. **NON-BLOCKING — the body of `ASSUMPTION_MAP.md` is stale.** The §1 table and §2 still describe v1.2: the target
   "v1.2 (LOCKED)", the row "A:START-FL (FL-16)", (N2) cited as necessity evidence for the leak level, "uniformly over
   ≤ p¹⁶ sets" for A:START-R-FL (L9 actually uses the pairwise event E_cov), and "(AL) forced by …" in the binding map.
   Appended notes §3–§5 correct these readings, and `REPORT.md` §5 is the corrected version, so nothing false is
   claimed in the end. A reader of §1 alone is misled. *Repair:* regenerate the §1 table and §2 for v1.3.3, and keep
   §3–§5 as history.
4. **NON-BLOCKING — the (B-L) row is slightly stronger than Lemma L3.3 as written.** `STATEMENT.md:233` gives the step
   bound as e^{2κ_E+o(1)}(n + 1)^{−1/2}exp(…). `lemmas/L3_LEAK.md:53` states and proves e^{2κ_E+1}. The proof actually
   gives e^{2κ_E+ς_n} with ς_n → 0 (`L3_LEAK.md:57`), so the row is true, but the lemma's displayed statement does not
   carry it. *Repair:* state L3.3 with e^{2κ_E+ς_n} (≤ e^{2κ_E+1}).
5. **NON-BLOCKING — the code pin names a commit that is no longer `main`.** `STATEMENT.md:46-47` pins "`main` =
   fe9a066". `main` has since advanced (c939971 in this worktree). I verified that CORE is unchanged since 72785fe and
   identical at d6da494 and fe9a066, so every `path:line` pin is still valid. *Repair:* at the next version, phrase
   the pin as "CORE tree as of 72785fe (unchanged through …)".
6. **NON-BLOCKING — the Gaussian-row rate in the summaries drops the (s₀ + 1) factor.** `STATEMENT.md:29` and
   `REPORT.md:27` write π₀(S₀) ≥ 1 − n^{−1/2}e^{C√log n}. The theorem has (s₀ + 1)n^{−1/2}e^{C_R√log n} (`L9_BR.md:165`);
   the factor is absorbed by enlarging C, so the summaries are correct. *Repair (optional):* write "for some C".
7. **NON-BLOCKING (process) — `citecheck.py` writes into the repository.** It writes to `reviews/CITECHECK.txt` inside
   the ticket. A reviewer under a no-write rule must run a copy, as I did, with the output redirected to scratch.
   *Repair:* add an output-path argument.

## Overall score: 8.8 / 10

I found no error in the mathematics. The proofs are complete at the level of detail a referee needs, and the
constants are explicit and tracked. The scope statements are careful: the (N2) vacuity, the tightness clause of (B-R),
the "expected, not verified" families, and the exclusion of response-selected targets are all handled well. The
deductions from 10 are for presentation and honesty-of-scope items (Issues 1–3) and for the fact that several
quantitative conclusions (F4, F-2, the uniform constants) are meaningful only at astronomically large n. That is
disclosed in the numerics but not in the statement.

## Checks performed

* `manifest.py verify` on the frozen round: OK at the start of the review. Before writing this file, I confirmed that
  `git status` showed only changes that were already there.
* Line-by-line re-derivation of L1–L11, detailed in the G1 row: every inequality, every constant, and every
  probability bound and union-bound count.
* Registry statuses extracted from `claims.tsv` fields (id, version, status) and compared character for character.
* Consumer and source citations read at their line ranges: SAMP :26-27, :70-110, :150-165; RM :38-46, :130-148,
  :268-275; SANDR :38-46; GROW :49-66; MIS :37-60; PXN :56-61, :101-107; BRIEF :19-22.
* Code read at every pin in `STATEMENT.md` §1 plus the score constants, the Cholesky and QR routes, the
  standardisation, the B override path and check_B. Read-only git checks of the CORE history.
* A scratch copy of `citecheck.py`, run with output outside the repository: 202 citations, 0 missing or out of range.
* Read `numerics/lemmas/RESULTS_LEMMAS.md` and the outputs `out_L4_L5.txt` and `out_L6_L11.txt`, and checked them for
  consistency with the claims. The numbers I re-derived for F-2 (λ_min(BᵀB), q₁₅, the margins, the 2.40 = 0.4c gain)
  agree with the printed values.

## Not checked

* I did not re-run any R script. The numerics were read, not reproduced.
* Textbook inputs were not re-proved: the Laurent–Massart χ² tails, the stochastic dominance of noncentral over
  central χ², and the Gaussian MGF formula.
* `complete_linkage` in `v3_blocks.h` and the exact-branch dispatch code were not audited beyond what the statement
  uses: the partition is a function of X, blocks have at most 16 members, and π₀ is the same function on every branch.
* Read only where cited, not in full: the argument sources (GEN `L1_lemmaE.md`, GROW `L0_toolkit.md` and
  `L3_sandwich.md`, RM `L1b_rss.md`, MIS `L1_reduction.md`), the T22 statement, `PROGRAM.md`, `PROTOCOL.md`,
  `LIFECYCLE.md` and the template. Nothing is consumed from any of them.
* `numerics/RESULTS.md` (the 1018 production runs) was read only through its use in `ASSUMPTION_MAP.md` and
  `REPORT.md` §5–§6. `numerics/*.R` and the CSV files were not opened.

`COUNCIL-VERDICT round=R1 manifest=0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97 seat=opus score=8.8 gates=PASS`

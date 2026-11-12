# W3-START — council round R2, seat `opus` (Claude Opus 5.5, effort high) — blind first read

Frozen content reviewed: `MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885`
(`python -B Theory_work/Wave3/tools/manifest.py verify …` → `verify: OK`). I read only the files the brief allows: the
manifest's files, the external inputs of `reviews/INPUTS.txt`, and `Theory_work/INFRA/registry/claims.tsv` for statuses.
I did not read any other review, LOG or checkpoint, and I did not use git history on the ticket folder.

## Verdict summary

I tried to break the package and did not find a mathematical error. I re-derived every step of L1–L11 at the level
of the individual inequalities. That includes the fibre bound and both two-sided identities of L1, the score
expansion under the unnormalised floor in L2, and the linearisation and Markov step of L3. It also includes Steps 1–7
of L4.1 and L4.2, the probability budget of L5.2, the conditional law, the Gaussian integral and the assembly in L9,
the transfer in L8, Proposition OVL, and the five examples. Each step holds as written, and the hypotheses each proof
uses are the ones its claim states. The uniformity claimed in (T1)(d) is real: no threshold or constant depends on p,
on |Q|, on the design or on the level vector beyond what is displayed. The coded start matches §1 of `STATEMENT.md`.
Every quoted registry status is verbatim. I found only non-blocking defects:
* The statement line numbers in the REPORT's claims table and assumption table are off by one line.
* The interface table in `STATEMENT.md` §4 overstates which form of P-OVL is delivered.
* There are a few small precision slips.

None of them affects a claim. The package can be accepted as checked mathematics as it stands.

## Gate table

| gate | verdict | what I re-derived |
|---|---|---|
| G1 correctness | **PASS** | **L1:** (P1)–(P5); the path bound (P3); the fibre bound L1.1, including \|S\| = \|T\| − D + E + a′, (x)_E ≤ c_Q^E, (x + E)_{a′} ≤ (c_Q + 1)_{a′}, injectivity and the factorised sum with (P5); (AGG-a); the three-way split of (AGG-b) with R₂ from (P4); the lower bound c_sΞ, with both prior-ratio cases checked against (2s₀)^{−16} and 32^{−15}; (AGG-c) (path bound with k = s₀, (s₀ + 1)_{a_Q} ≤ \|Q\|^{a_Q}); (AGG-d) in both cases d ≥ a and a > d; FLOOR, by the ridge form of Q_S, the Schur identity D_{S∪l}/D_S = (n + 1)s(1/(n + 1))/s(1) with s′ > 0, and the elementary inequality 2(k + 1)(p − k) − (2p − 1 − k) = k(2p − 2k − 1) + 1. **L2:** (2.1); the tail bounds of 𝒟₁–𝒟₃ and their union counts (2^{24}, 2^{17}); (TK-a) via 2ab ≤ a²c + b²/c; (TK-b); (E1) eigenvalue factors in [g_*/(g_* + 1), 1]; (E2) G⁻¹ − nH⁻¹ = G^{−1/2}(G + I)H⁻¹G^{−1/2} with eigenvalues ≤ (1 + 1/g_*)/(n + 1); (E4) and the decomposition of R_U; (TK-e); (f1)–(f3), including −log(1 − x) ≤ x + x² on [0, ½]. **L3:** (J0)–(J4) (the J1 moment formula with λ = a/2); the budget b_n(h) and the default value 1/(32 log n); (B1)(iii), including the ≤ 15 nulls of an all-truth block; L3.3 with ς_n; the small-gain consequence of (J0); Proposition L3.4 (the indicator-weighted V, E V = Σ J_{h_l}, Markov with no independence used); F4's arithmetic and the default-level threshold (√c < √(4A + 1) − √(2A), which is below 1 + 2A). **L4:** P(𝓧ᶜ) ≤ 1/log n; (Q±); the instance mapping (V, D, R, N) ↦ (U, T, W) of L4.1; the choice of ε₁ (both inequalities); Steps 2–4 (the bracket is ≥ 0 once (1 + ω̄)(1 + ϑ̄) ≤ 1 + ε₀/3); Step 5 (C₂ = 16 log(32s₀) dominates both cases); Step 6; L4.2's exponent chain down to e_n ≤ 2^{−16}n^{−(κ_V+κ)/2}. **L5:** (e1)–(e3); the event 𝒢, with P(𝒢ᶜ) ≤ ε/2 + b_n + 2·ε/4; (c_Q + 1)U_Q ≤ 16s₀′λc₀ = ¼; C = 43s₀′λ ≥ (8/3)·16s₀′λ; (ii) with C′; the passage from (d) to (a)–(c), including o₀/T₁ − 1 ≤ 2√(n + 1)[…] with κ′ > ½. **L6:** L6.0′ (λ_n = c_L log n); F1 (i)–(iv); F2 (Schur complement ≥ λ_min(R̂_{S₀}); (J1) with τ² − σ² = Δ_U); F3. **L7:** both chains, including log(2p) ≤ (Ā + ϵ) log n and the margin 3ϵ. **L8:** the Fubini version f_B of the conditional probability and the inequality P(B) ≤ P(X ∉ 𝒳) + E[1_𝒳f_B]. **L9:** L9.1 (rotation by O, polarisation, union over p²); (c1)–(c4), including C_S = 1 + 45/c_Σ + 450/c_Σ²; L9.2; the identity J = F(g, a); (F1); (F2) (Lipschitz constants of √a and √(1 − a)); the projection identities of L9.4 and the bounds C₄, C₅, √(N log n)ε_n² → 0; L9.5 (population regression with e ⊥ W_D, ‖γ²‖, Π = (I − P_{U₀})C, independence of ξ and R, (9.1), the dominance step for E_R with k ≥ N − 16, and the Gaussian integral: r²/(1 − s′²) − 1 = η(1 − a)/(a − η), 1 − s′² ≥ a̲/2); L9.6, (9.2), (a) and (b) (the constant 2^{18}); L9.7 (κ_V = 3/2, κ = 1, and the absorption of C_n into e^{√log n}). **L10:** IF-START; OVL (i)–(v); Lemma R′. **L11:** all five families (see F-2 below). |
| G2 hypotheses used = stated | **PASS** | For every claim I compared the hypothesis list with what the proof uses. (T0) and (C0) are deterministic and use only r_b > 0, the formula for w, K ≤ p and the block bound. (C1) uses only the interface properties. (T1) uses (E), (GF-16), visibility, (AL) and the level vector. (C2) uses [TK] in quantitative form, and `STATEMENT.md` §4 last paragraph and (T4) list (GF-16). (T2)'s F2 states its normalised floor on S₀ explicitly. (T3)(b) states p > s₀ explicitly. OVL states the uniform bound ā and (V-c). (T6) requires every substituted hypothesis. I found no unused or silently strengthened hypothesis. |
| G3 no hidden assumptions | **PASS** | No independence between the Z_{T,l} or between columns is used: L3.4 bounds a maximum by a sum and uses Markov, and L4.0 and L2.1 are union bounds. The only floor in (T1) is unnormalised: L2 uses g_* only in (E1), (E2) and for rank. s₀ = 0 is handled everywhere: L2, L3.2(iii), L4.0 and L5.2 (via s₀′). p > s₀ is stated wherever it is used. A ≥ 1 is never used. The only conditioning is on σ(W_D) (L9.5), a σ-algebra generated by design columns. Levels, Q, S₀ and θ* never depend on the response: L3 Remark 3, L8.1, and the exclusions in (T3)(a) and (T6). |
| G4 imports | **PASS** | No registry claim is used as a premise. GROW, GEN, MIS and RM are sources of argument only; I checked that L2, L9 and L10 re-derive what they need. Statuses checked against `claims.tsv`: C-GROW:L0.1@1.0.0 and L0.2@1.0.0 "PROVED-CHECKED"; W3-SAMP:C@1.1.1 and D@2.1.1 "PROVED-CHECKED"; W1-PXN:Thm-PXN(S)@1.0.0 "XF VERIFIED"; C-MIS:LemR@1.0.0 "R02 VERIFIED; council R07/R08 PASS"; W3-RM:B1, B2tau and SAND-R @1.0.0 "PROVED (by this seat, unchecked)"; the TH116 fragment quoted in (T1) is a verbatim substring. All are verbatim. The consumer quotes (SAMP:76 P-START, :82 P-OVL, :104 the production corollary of D-iv, :158–161 C-v, :27 δ̄ := max(o₀, o₁)) are correct. IF-START gives exactly 1_𝒜o₀ = O_P(r_n), and with δ̄ = max(o₀, o₁) the rate max(r_n, r^post_n) follows. The other quotes I checked are also correct: PXN:58-60, PXN:103-106, RM:41-44, RM:134-145, RM:271-273, GROW:51-64, SANDR:42-44, BRIEF:20-21. The two non-blocking defects are Issues 1 and 2. |
| G5 constants and rates | **PASS** | I traced κ_E(g_*, M, σ²), ω̄_n(n, A) = O(n^{−1/3}), ϑ̄_n, g_n, ς_n, n₁ and n₂(A), ζ_n(s₀), n₃ and n₄, c_L = 2^{15}e^{2κ_E+1}, λ, c₀, C, C′, and in L9 the constants d̄, a̲, ā, C_B, C_R and C₆. None depends on p beyond p ≤ n^A, nor on \|Q\| (Step 5 of L4.1 uses c_Q/p ≤ 16s₀ via \|Q\| ≤ K ≤ p), nor on the design, nor on h. So (T1)(d), and through it (T3)(a) and (b), are uniform as claimed. The exponents check: κ_V = (c_V − 1 − 2A)/2 or c_m/2; κ_L(η, A); F4's (1 + 2A̲ − c)/2; and the 15κ_Q + ½ of the C_L = 0 clause. |
| G6 fidelity to the code | **PASS** | Checked against the pinned CORE files. Prior: `v3_score.h:39-72` (K = min(p, n/2) with integer division; log w(k) = −log 2 − log C(2p − 1, k); log W_K by log-sum-exp; logprior = logw − logW_K). Score: `v3_score.h:162-224` (H = (n + 1)G_S + I, A = G_S + I, Q = yᵀy − n·zᵀH⁻¹z, logm = logC_n − ½(ldH − ldA) − ν log(2b₀ + Q); a₀ = b₀ = 0.01 at line 14; the non-negative recomputation of a small Q is covered by EX-A). Tables: `v3_start.h:76-98` (logr = logm − logm0 with logm0 = log m(∅) against the full y). Start: `v3_start.h:66-70` (logprior[\|S\|] + Σ_b logr) and `v3_start.h:101-137` (convolution truncated at K). Partition: `v3_blocks.h:124-144`; B is set at `v3_preprocess.R:22`; production setup uses that B (`v3_setup.R:66-70`, `v3_core.cpp:279`). Preprocessing: `v3_preprocess.R:111-127` drops constant columns; `v3_standardise` gives X = CX^rD_x⁻¹ and y = Y/s_y in exact arithmetic, in both branches. The code accepts n ≥ 3; the claims require n ≥ 4, which is a stated restriction, not an infidelity. |

**REPORT and ASSUMPTION_MAP.** The REPORT's content matches the statement and the proofs, apart from the line offsets
in Issue 1. The sharpness record and the assumption map claim no more than the proofs support:
* T₁ → 0, Ξ → 0 and the exponent ½ are labelled NECESSARY with correct evidence.
* (AL) is labelled sufficient only.
* The leak level is NECESSARY on the actual partition only, with the vacuity of (N2) stated.
* The factor e^{C√log n} is "not known to be sharp".
* The numerics are labelled as observations, and they record what they do not test.

The honesty of scope is adequate: `STATEMENT.md` §6, the tightness clause of (B-R) and (T3)(b), the "expected, not
verified" UNI-0/AR(1) entries, and the vacuity note on (N2).

## Per-claim table (ids of REPORT.md §3)

| id | decision |
|---|---|
| AGG | accepted |
| FLOOR | accepted |
| TK | accepted |
| LEAK | accepted |
| VIS-c | accepted |
| VIS-m | accepted |
| ASM | accepted |
| START-F | accepted |
| F1 | accepted with non-blocking remarks (Issue 5: the η = 0 sentence is read under the premise of F1(ii)) |
| F2 | accepted |
| F3 | accepted |
| F4 | accepted |
| NEC-b | accepted |
| NEC | accepted |
| TRANSFER | accepted |
| BR | accepted with non-blocking remarks (Issue 3) |
| START-R | accepted |
| IF-START | accepted |
| OVL | accepted with non-blocking remarks (Issue 2: wording of the P-OVL row in `STATEMENT.md` §4, not of OVL itself) |
| MIS | accepted |
| EX | accepted (F-1, F-2, F-3, G-1, G-2 verified; UNI-0 and AR(1) correctly not claimed) |

Example F-2, re-derived in full:
* q_k = (1 − ρ²)/(1 + (k − 1)ρ²), from the eigenvector 1 of the correlates' Gram matrix.
* Λ_N = cσ² log n·q_k.
* (V-m) instances: N = ∅ needs (7/12)c, and N ≠ ∅ has c/11 ≥ c/12 = c_m.
* (V-c) fails, since 2(1 + 2A)/11 < 1 + 2A.
* The gain of a correlate is ≤ 0.4c = c′ = 0.8(1 + 2A).
* Default (AL) fails: the exponent is −0.1 − 0.2A + √(1.6A + 3.2A²) ≥ 0.318 at A = 0.1, and it increases in A.
* The resulting rate is n^{−0.1(1+2A)+o(1)}, which is below n^{−κ} for κ < (1 + 2A)/12.

## Issues

1. **NON-BLOCKING (traceability). The statement line citations in the REPORT are off by one.**
   - Location: `REPORT.md:72-92` (claims table) and `REPORT.md:103-111` (assumption table).
   - Problem: every `STATEMENT.md:<line>` reference starts one line before its target. Ranges still mostly overlap the
     claim, but several single-line references point at the wrong item:
     - TK `:232` points at the (B1) row (B-TK is line 233).
     - LEAK `:233` → (B-TK); VIS-c `:234` → (B-L); VIS-m `:235` → (B-V1); BR `:236` → (B-V2).
     - A:START-E `:134` points at the §3.1 heading ((E) is line 135).
     - The remaining ranges (AGG, FLOOR, START-F, F1–F4, …) start on the blank or heading line before their claim.

     `citecheck.py` checks only that a range exists, so it cannot catch this.
   - Repair: shift every `STATEMENT.md` line reference in REPORT §3–§4 by +1, and re-check the range ends.
2. **NON-BLOCKING (interface wording). The §4 interface table overstates the P-OVL delivery.**
   - Location: `STATEMENT.md:185`, row P-OVL of the §4 table.
   - Problem: the "delivered by" column reads "P-START; Proposition OVL" against SAMP's general P-OVL
     (D_r·π₀(S₀) → ∞ for SAMP's own budget D_r). What is proved is only the production form
     max(n, p)·log₂(n + 1)·π₀(S₀) → ∞ of SAMP (D-iv) (`STATEMENT.md` (T5), `lemmas/L10_INTERFACES.md` L10.2, last
     paragraph). P-START gives the general form only if D_r is bounded below, which it is in production. (T5) and
     REPORT §4 state the scope correctly; only the table row is loose.
   - Repair: write "production form (SAMP `STATEMENT.md:104`): P-START, or Proposition OVL".
3. **NON-BLOCKING (precision). Two events in L9.5 are undefined when μ̃ = 0.**
   - Location: `lemmas/L9_BR.md:110`.
   - Problem: ξ, R, E_R and E_ξ are defined only when μ̃ ≠ 0. On E_cov, μ̃ ≠ 0 for every reference pair
     (Δ_{U₀} ≥ Δ_lo), so nothing breaks, but E in L9.6 uses the events for all pairs.
   - Repair: "if μ̃ = 0 put E_R = E_ξ := the sure event".
4. **NON-BLOCKING (precision). The order of C_n is misstated.**
   - Location: `lemmas/L6_COROLLARIES.md:26`.
   - Problem: the text says "C_n, C′_n = O((log n)²)". In fact C_n = O(log n) and C′_n = O((log n)²). L6.1 and L6.3
     correctly use C_n = O(log n).
   - Repair: state the two orders separately.
5. **NON-BLOCKING (wording). The η = 0 clause of F1 reads as standalone.**
   - Location: `STATEMENT.md:271`.
   - Problem: the clause has no premise of its own, yet it needs (\|Q\| + 1)√(log n/n) → 0, i.e. the premise of F1(ii)
     with κ₁ < ½. `lemmas/L6_COROLLARIES.md` L6.1(iv) uses that premise.
   - Repair: "With η = 0, under the premise above, …".
6. **NON-BLOCKING (cosmetic). The range of ε in (T1)(d) differs from its proof.**
   - Location: `STATEMENT.md:254` versus `lemmas/L5_ASM_STARTF.md:40`.
   - Problem: the statement has "for every ε > 0", the proof ε ∈ (0, 1). For ε ≥ 1 the bound is trivial, so nothing is
     lost.
   - Repair: optional; align the two.

Nothing must be fixed before acceptance. Issues 1–6 can wait for a later version.

## Overall score

**8.9 / 10.** The mathematics is complete and correct as far as I could re-derive it, with explicit, uniform
constants, honest scope, and verbatim imports. The deductions are for the systematic citation offset (Issue 1) and the
loose P-OVL row (Issue 2).

## Checks performed

* `manifest.py verify` on MANIFEST_R2: OK.
* Read in full: STATEMENT.md v1.3.4, the eleven lemma files, REPORT.md and ASSUMPTION_MAP.md. Skimmed: BRIEF.md,
  numerics/RESULTS.md and numerics/lemmas/RESULTS_LEMMAS.md.
* Re-derived every step of L1–L11 by hand (detail in the gate table).
* Read the pinned code at the cited lines: v3_score.h, v3_start.h, v3_blocks.h, v3_preprocess.R, v3_setup.R and
  v3_core.cpp.
* Checked registry statuses with a parsed read of claims.tsv.
* Checked the consumer and source quotes in the SAMP, MIS, RM, GROW, PXN and SANDR inputs.
* Ran `citecheck.py` with its output written outside the repository and then deleted: 203 citations, 0
  missing/out-of-range.
* Checked by direct `sed` that the REPORT's line references are offset (Issue 1).

## Not checked

* I did not re-run any numerics script, and I did not check the numerical values in the numerics files.
* I did not read PLAN.md beyond its role, or PROTOCOL.md.
* I did not verify the semantic content of the GROW `L0_toolkit.md:19-53` range quoted in §7, because it is not
  consumed.
* I did not check the measurability of the coded partition map (complete linkage with ties) beyond accepting it as a
  function of X.
* I did not re-verify the Laurent–Massart and Gaussian tail inequalities themselves; they are standard.

COUNCIL-VERDICT round=R2 manifest=5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885 seat=opus score=8.9 gates=PASS

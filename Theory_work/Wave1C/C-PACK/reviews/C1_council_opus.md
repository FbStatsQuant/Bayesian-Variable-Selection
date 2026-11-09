# C-PACK council round 1, Claude seat (opus)

Reviewer: Claude Opus 5.5 (high), council seat "opus". I scored independently and did not coordinate with the Sol seat.
Scope: items 1–4, as specified in `reviews/COUNCIL_BRIEF.md`. Item 5 and R36 were read as context only.
Everything outside this file was read-only. I made no git changes and spawned no subagents.

## What I checked independently (I did not take reviewer conclusions on trust)
- **Frozen code.** I read `CODE/cpp/v3_start.h:30-240` directly.
  - `comp` (`:54-66`) folds `logr` from 0, over nonempty blocks only, in increasing block order.
    `log_gamma0` (`:69`) is `logprior[|S|] + comp(S)`.
  - `start_mode` (`:183-240`) builds per-block per-size maxima, then a max-plus convolution in the same order, skipping
    `j = 0`. Size is chosen by strict `>` (ties keep the smaller size). Backtracking enumeration has `trunc` set at
    `count >= cap`.
  - `build_tables` sets `logr[b][0] = 0` and NaN above K. `D.K = min(p, n/2)` and `logprior` match
    `v3_score.h:40,63-70`.
  - A grep of the frozen core finds no caller of `start_mode` outside `v3_start.h`. This is consistent with LS0/e4
    integration being a premise (G6).
- **Item 1 re-derivations.**
  - UM: uniqueness gives N = 1, so N3(c) applies (`W1-N3/STATEMENT.md:120-122`).
  - The {π₀(R) > ½} ⇒ uniqueness step.
  - Fold bound: m + 1 summands give m roundings, hence γ_m. The first addition is exact; the subnormal-sum exactness
    claim is correct.
  - ε ≤ γ_K(Λ̂ + KT̂) and η ≤ η_λ + Kη_ρ.
  - FP-TAB chain: ĝ(R) ≥ f\*(R) − η − ε > f\*(S) + η + ε ≥ ĝ(S).
  - Margin bound: Δ ≥ log((1 − t)/t). The constants c = ½ / κ follow from the cited rates.
  - Numeric spot-check: γ₁₀₀(10³ + 100·10³) ≈ 1.1·10⁻⁹, as stated.
  - §1.1: PXN's 𝒯_n contains {S̃₀ = S°} explicitly (`W1-PXN/FINAL_PROOF.md:63`). The capped-routine order dependence
    therefore matters only for Lemma T(i)'s centre clause, and §1.1 removes that clause correctly.
  - T38 Theorem b1, step 4 (`T38_PROOF.md:259`) uses the centre only through P₀(π₀(S°) ≤ ½).
- **Item 2 re-derivations.**
  - (R-c) second display = (R-b) with p ≤ n^A.
  - [CONC′] at δ_n gives 3p²n^{−2(A+1)} ≤ 3n^{−2}.
  - Off-diagonal row sum ≤ (|T| − 1)δ_n, then Weyl, then interlacing for λ_min(Σ_T) ≥ λ₀.
  - GEN's λ₀ = (1 − max|ψ|)(1 − ρ₊) with the single ρ of PX:36-60 equals PXN's (F4) lower bound.
  - GEN L6(b)'s 𝒞_n index range is covered by L′_n.
- **Item 3 re-derivations.**
  - P-L8.1. Using v_T ≥ σ² and |δ| ≤ √(η log n)σ, I get E ≤ (η/2 + √(2η(A + ε₀))) log n. The condition
    η < (√(2A+1) − √(2A))² is exactly the ε₀ ↓ 0 limit of η/2 + √(2Aη) < ½. The patch is correct.
  - P-SEL.1. The Markov step is now localised to F_n; the domination holds only on 𝒢_n ∩ 𝒦_n, as the patch says.
  - I re-read L6(d) (i)–(iv):
    - The Beta law for T₀ ∈ 𝒯₀(l) holds in all three cases: null group, signal group with its truth in T₀, and S1.
    - The partial-correlation recursion and the ω_n order are correct.
    - |G_l ∪ 𝒮𝒢| ≤ 75 gives the 2^{75} count.
- **Item 4 re-derivations.**
  - SL0(i)–(vi), SL1(a)–(e), SL1′ and SL2, including the δ_n ≥ ½ case of SL2.
  - D0 positivity used in (vi): m(U) > 0, because .02 + Q_U > 0 (`SoP/04_theory.tex:71`).
  - I-c: the de-randomisation/diagonal argument works.
  - Map rows 5, 6, 7, 11, 12 and 13 match the Song–Liang text (`numerics/R34_song_liang_layout.txt` lines 575-596,
    656-668, 685-720, 1393-1398): Thm 3 bound, ξ_q inclusion, Thm S sentence, Cor 2 withdrawal at 958(c), Condition 5,
    and the O(P_n^{(1+α)/2}) + O(nP_n) complexity.
- **Verbatim quotes.** I checked the quoted lines in `SoP/04_theory.tex`: :35, :78, :84, :111, :117, :130, :305, :397,
  :400-401, :410-412, :484, :489, :491, :505, :782, :787, :824. I also checked the W1-N3, W1-N1, W1-PXN and W1-GEN
  REPORT status lines, and `T38_PROOF.md:247-266`. All match.

## Per-item assessment

### Item 1: e4 not needed for consistency (I1 v2, P-e4, METHOD_REQUIREMENTS)
The proof is correct and the conclusion is honestly scoped.
- **Lemma UM** is a two-line consequence of a PROVED-CHECKED Wave-1 result. It is quoted with its status and is not
  upgraded.
- **Lemma UM-FP** is a correct, self-contained binary64 statement that stops at the identification step. It explicitly
  says it does not replace EX-A elsewhere.
- **The audit** is the real value. It finds the two genuine off-event uses:
  - GEN (C6): global maximality, which is N3(a) under EX-A.
  - PXN Lemma T(i): the centre-transfer clause, which is false for the capped ordered routine. The block-order
    counterexample is legitimate.
  
  It resolves both correctly. The M4 sketch route is excluded honestly.
- **e4′** keeps everything that is still integration: H1, H4, OP-LS0, the scored-set contract, a deterministic
  measurable centre on every branch, and no truncation veto.
- **Completeness of the patch locations.** Some e4 premise-list occurrences are not listed. See non-blocking issue 1.

### Item 2: LH-iid without candidate Theorem B / [CONC] (I2 v2, P-LHiid)
The proof is correct.
- The two probability facts GEN needs are isolated correctly. Each is discharged by a PXN result whose ticket status is
  quoted.
- The exact-branch mismatch, the 𝒜_n name collision and the ρ₊/ρ notation are recorded explicitly.
- The rate change from log p to log n is handled honestly ("weaker but sufficient").
- The (C5)(d) carry-over is correct, and the alternative δ = 32√(3 log p/(n−1)) is offered.
- The onset of (ii) is astronomically large. For typical constants, L′_nδ_n ≤ λ₀/2 first holds near n ≈ 1.5·10¹⁰
  (my computation). This does not affect the asymptotic claim, which is all that is made. See non-blocking issue 3.

### Item 3: SEL / L8 dedicated checks (P-SEL, P-L8)
Done to protocol: dedicated xhigh checks R31/R32, falsification numerics, patches outside Wave1, and an independent
re-check R37 whose amendments are applied. There is no counterexample, so the stop rule did not trigger. My own
re-derivation of P-L8.1's (ε₀, κ) inequality and of SEL (i)–(iv) agrees.
- The finite-n disclaimer is appropriate: NL_avg(1/8) fails at n = 200 in 5 of 12 draws. It is correctly called "not a
  counterexample to an asymptotic lemma".

### Item 4: Song–Liang corollaries (I4 v2, SONG_LIANG_MAP v2)
The SL lemmas are elementary and correct, with the attainment caveat, empty-max conventions and HPM-vs-Ŝ⁺ distinction
in place.
- **Instances** are tied to complete hypothesis sets.
- **SL1′** is restricted to sensitivity.
- **SL2** is conditional on M4(b)/(c), with their AUTHOR-ONLY / candidate statuses quoted verbatim. The 𝒮 ≡ 𝒮⁺ reading
  is justified from the card.
- **The map** is careful:
  - Thm S is marked NOT INSPECTED.
  - The domain mismatch is recorded: P_n/n^θ → ∞ there; p_n ≤ n^A here.
  - Thm 4/Cor 2 are routed to C-MIS.
  - The pooled R′ = 4 PIP gap is stated.

## Gate verdicts
- **G1 (correctness): PASS.** Every new step was re-derived (list above). The only inherited facts are the cited Wave-1
  or registry results.
- **G2 (hypotheses used = stated): PASS.**
  - UM: H1–H4, cap ≥ 1.
  - UM-FP: H1, H2-FP, H3, H4 and FP-TAB, with ku < 1 explicit.
  - I2: GEN's (C5)(b) setting plus the exact-branch convention.
  - SL2: (α)–(γ) plus EX-A.
- **G3 (no hidden assumptions): PASS.** The exact-branch convention, measurability of the coded centre, D0 positivity,
  the 𝒮 ≡ 𝒮⁺ reading, and "S₀ ∈ Ω for h(S₀)" are all made explicit. Non-blocking issue 2 is a wording mismatch, not a
  hidden assumption.
- **G4 (citation status, verbatim, no upgrade): PASS**, with one wording nit (non-blocking issue 4).
- **G5 (constants and rates): PASS.** Every constant is explicit: (R-c) constant and exponent, [CONC′] 1024/32, onset
  conditions, ε/η bounds, margin constants c = ½/κ, and 2^{75}, C_L, κ for SEL. No finite-n reading is claimed.
- **G6 (fidelity to coded and shipping method): PASS.** The frozen v2.2.1 `start_mode` and `log_gamma0` evaluation
  paths are described exactly. LS0/e4 integration is an explicit premise (e4′ (i)–(iii), MR1–MR3). Shipped R′ = 4 PIPs,
  `pip_plain` vs `pip_primary`, and the store-restricted PIPs are kept apart.

## Blocking issues
None.

## Non-blocking issues (with fix text)
1. **P-e4 location completeness (T1.d).** These premise-list occurrences of e4/N3 are neither in the audit nor in
   P-e4:
   - `W1/W1-GEN/REPORT.md:16, :30, :97`
   - `W1/W1-PXN/REPORT.md:47` (row "(E) P5 … bypasses, does not prove, N3")
   - the shared-premise definition of **e4** at `SoP/04_theory.tex:84`, which both cards use
   - the measurability use "the deterministic tie rules (all chosen as measurable versions …)" at
     `W1/W1-GEN/lemmas/L5_assembly.md:69`
   
   None of them is a deduction off a uniqueness event, so no conclusion changes. Fix: add to P-e4:
   > "17. `W1-GEN/REPORT.md:16,30,97` and `W1-PXN/REPORT.md:47`: read e4 as e4′ (C-PACK I1 §4); keep the historical
   > verdict text. 18. `SoP/04_theory.tex:84`: after the e4 definition add 'C-PACK addendum: for the consistency cards,
   > e4 may be replaced by e4′ (C-PACK I1 §4); N3 status unchanged.' 19. `W1-GEN/lemmas/L5_assembly.md:69`: the
   > start-mode part of 'the deterministic tie rules' is the coded centre of e4′ (ii), a deterministic measurable data
   > function on every branch."
   
   Add audit row G9 (kind D, structural) for L5:69.
2. **e4′ (i) vs MR1.** e4′ (i) fixes the centre as the current routine's output. MR1 allows "any replacement routine"
   that returns the unique maximiser under exact arithmetic. Harmonise by appending to e4′ (i):
   > "or a replacement routine satisfying METHOD_REQUIREMENTS MR1; Lemma UM then holds with W1-N3 (c) replaced by MR1's
   > unique-maximiser property, while Lemma UM-FP applies only to the current routine."
3. **I2 finite-n remark.** Add after the proof of (ii):
   > "The onset L′_nδ_n ≤ λ₀/2 is far beyond practical n (≈ 10¹⁰ for g = 10, c = 1, ρ = .7, ψ̄ = .5, A = 1); (ii) is an
   > asymptotic statement only."
4. **I2 §5 status wording (G4 nit).** "GEN's own (R07 VERIFIED-WITH-AMENDMENTS)" could be read as a lemma status. The
   L6 header status of (b) is "PROVED (by this seat, unchecked)". Replace with:
   > "GEN's own L6(b) argument (status 'PROVED (by this seat, unchecked)'; R07 recorded (a)–(c) VERIFIED-WITH-AMENDMENTS)".
5. **"v2 repairs pending re-check" (I1, I4 headers).** R38 (blind mid-point) and R39 (sweep) re-read the v2 texts.
   REPORT.md should state, clause by clause, which review re-checked which v2 repair. Without that, the headers should
   keep "pending".
6. **I-c over-requirement (nit).** The parenthesis "The transfer requires GEN's every-sequence/common-envelope
   quantifiers" is stronger than needed. For O_P tightness, the diagonal argument needs only T03♯'s O_P conclusion
   along every deterministic sequence in the X-events. This is harmless and conservative; it may be left as is.
7. **Map "Reading" (wording).** "Thm 1–2 at the selection level" reads as if Song–Liang had selection-level Thm 1–2.
   Replace with:
   > "every correctly specified Song–Liang selection-level result (Thm 3, ξ_q, the MAP description of Thm S), and the
   > selection-level counterparts of Thm 1–2".
8. **Evidence trail.** R38's extra numerics (280 laws, 2,000 binary64 instances) are reported but no script is saved in
   `numerics/`. Either save them or cite them as "reported by R38, not reproducible from the package".

## Score
The package does what the locked statement asks, with unusually careful status discipline.
- I found no error in any new deduction.
- The reviewer-found MAJORs (R33 #1–#3, R34 #1–#2, R35 #1, R39 #1) are fixed with sound texts.
- The remaining items are completeness and wording.

Deductions: patch-location completeness for e4 (issue 1), the e4′/MR1 mismatch (issue 2), and the "pending re-check"
labels on two core lemmas.

SCORE: 8.7; GATES: G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS

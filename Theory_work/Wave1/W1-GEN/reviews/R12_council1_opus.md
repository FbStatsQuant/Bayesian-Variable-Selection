SCORE 8.9 / GATES G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS

# R12 — Council round 1, reviewer Claude Opus 5.5 (independent)

Target: W1-GEN, STATEMENT.md v2.3 and lemmas/00_MAIN.md, L1–L8. I read PROTOCOL.md, STATEMENT.md and every proof
file in full. I also checked these sources directly: T22iii PROOF_v2.tex (lines 35–481), T22 STATEMENT.md §1–2, SoP
02_method.tex (150–211, 463–506), SoP 04_theory.tex (TH05 card 464–540; regime map 840–852), TLF:71 (W) and
Scripts/Data_generators/gen_dev_data.R. I re-derived the algebra of each step myself (details below). I did not read
any council file (R11) before writing this review.

## Gate verdicts

**G1 — correctness of every step: PASS.** I re-derived each step that carries weight.
- L1: the identity (E1) for D_A; the commuting-matrix bound for Q_A − RSS^y_A in (E2); the remainder interval in (E4);
  the floor and ceiling L1.2(a)–(d); and the contrast bounds L1.4.
- L3.1: the Schur-complement step, then the step ⟨ρ_k, r_S⟩ = δ_{S,k}‖ρ_k‖ with ‖ρ_k‖ ≤ √(n−1), then Cauchy–Schwarz.
- L3.2(b1)/(b2): the ε = (1 − c_S)/4 bookkeeping, using (1−ε)E₂ − (1+ε)c_S E₂ ≥ (1−c_S)E₂/2, with three-term
  triangle inequalities.
- L3.3(a): the BB(1,p) addition penalty log((k+1)/(2p−1−k)) ≤ log(v̄+1) − log p cancels the log(2^{v̄}p) from 𝒟₅, so
  an extra addition loses ½log n − log log n − O(1).
- L3.3(c3), (d): the swap bound Λ_A = θ*_i²‖(I − P_A)x_i‖² uses the Gram floor on S₀ ∪ {l} only; SEP is not needed.
- L4(iii): scan counting gives "scored iff ℓ ≥ τ − 1" and "certified endpoint iff ℓ ≥ τ".
- L2: the substitution list against [P]. [P] uses S₀ only as the reference: Lemma residual and Lemma integral do not
  depend on the reference, and Lemma quad uses only the O(log n) size of the leakage numerator. T22(i) is stated for
  any feasible reference S°, and its u matches 𝓛(S*).
- L6(b) and Lemma SEL: the Beta(½, (m−1)/2) moment bound. The exponent drift is (|T|+3)/2 ≤ (L+3)/2, and
  ∫z^{−1/2}e^{−cz²} = Γ(¼)c^{−1/4}/2 gives O(m^{1/4}). This is correct even though the heuristic χ²₁ comparison would
  suggest divergence.
- Lemma SEL further: the reduction T ↦ T₀ is well defined because blocks are unions of whole groups, so a signal
  group's truth is in T whenever any member is. The recursive partial-correlation perturbation is O(log p/n)(1 + |ρ₀|).
- L7: W1 (the 2×2 PSD check); the proxy-addition contradiction in L7.1, with a Gram floor of 1 on the family; the
  arithmetic ⌈d/B⌉ − 1 ≥ 2ℓ + 4.
- L8.1/L8.2: the projection identities.
- Instances: W's conditional covariance 3ε/(3+q), and the (c)/(d) S5 pattern sum (0.8). For S2 I confirmed in
  gen_dev_data.R that consecutive truths are ≥ 31 indices apart, and the last two exactly 34 apart.

The only defects are a few mis-stated constants and indices; none affects a conclusion (see the optional items).

**G2 — hypotheses used = hypotheses stated: PASS.**
- L2 uses G, ‖μ‖² ≤ Mn, p ≤ n^A, (H2), s* ≤ v̄ and S* ∈ Ω, as (C1) states.
- L3 uses G, R, fixed s₀, p ≤ n^A, BM-∞ and (H1); φ₀ ≤ 1 is derived, not assumed.
- L5 adds T03♯ (H0), M5(0) and the premises.
- (C3-fav) correctly drops (H1).
- (C6) shows the two size bounds are the hypotheses doing the work.

One mismatch in wording: the onset in the (C3) display differs from what L5.1 proves (required fix 1). The asymptotic
conclusions are unaffected.

**G3 — no hidden assumptions: PASS.** These are all explicit:
- Feasibility: |𝒱| + 1 ≤ K, or 𝒱 = [p].
- Existence of directions for 𝒟₄ and 𝒟₅ via (H1a).
- The bounded-energy assumption added to L8.
- Measurable versions in L5.4.
- X-measurability of β, 𝒱 and S* in (C4).
- The exact branch.
- The fact that the uniqueness of the start mode makes the tie rule irrelevant.

The only implicit item is standard: the run is a measurable function of (x, e, u). L5.4 states this.

**G4 — status of cited inputs: PASS.** M5(0)/T38-(0), T03♯, T22(i) and T22(iii) are quoted verbatim. W7-PART Theorem B
is labelled candidate, and (C5)(b) is labelled conditional on it. W1-EXP 4.1/4.2 carries its SAME-FAMILY-ONLY tag.
Nothing is upgraded. Three small record problems (required fixes 2–3):
- The W partition input (TLF:71) is cited without a status.
- L6's header still says Lemma SEL is "not yet re-checked", while 00_MAIN's proof map credits the sweep.
- The [OP] closure is presented in two ways: L5 writes it as the seat's own pathwise argument, and §5 cites [W6] as
  "candidate". Make the two consistent.

**G5 — constants and rates tracked: PASS.**
- L1 constants are explicit: C_R = 3(M+σ²), c_E, κ_E.
- L3's Π, W_n and H_n are explicit, and each n₀ lists what it depends on.
- The centre rate is a_n = 2^B√(log n) n^{−κ}, and e_n is superpolynomial.
- The move bound is τ ≤ 2^{v̄} − 1.
- The instance constants are explicit: φ₀², g₀, M, C_L, κ = 1/8, ε₀ = 1, and the BM and VIS envelopes.

The D_n rate is implicit; it is O(1/log n), driven by P(𝒟₅ᶜ) ≤ 2/log n. Stating it would help (optional).

**G6 — fidelity to the method: PASS.** I checked each item against SoP 02_method:
- Blocks: complete linkage on 1 − |r̂|, top-down size cut, next-fit packing, B = min(⌊√n⌋, ⌊√p⌋, 16).
- Tables: r_b = BF over every U ⊆ C_b.
- Start mode: size-then-lex tie rule.
- Local search: the centre is frozen during a scan; all feasible flips and swaps are scanned; a move requires a strict
  improvement; ties within a scan go to the lexicographically smallest set (L4 Remark 3 makes this irrelevant); at
  most ℓ = ⌈log₂(n+p+1)⌉ moves plus one further scan; `local_limit` and `local_certified` are kept apart from the
  public flag (SoP:505-506).
- LS0: run after the final search and after the c₄ extra search, reads no uniforms, and its scored models join 𝒮⁺.
- The exact-branch dispatch is used correctly (L7 Remark 1, L5 Note 2).
- The implementation premises are named, never proved.

The study generator is modelled faithfully, including standardised columns, so θ* = cβ^pat, and the step-7/13
layouts. The result concerns v3.1 + LS0 *as specified*: LS0 is not in production code (SoP TH05 notproved list; W1-N3
REPORT). STATEMENT §1 says this; the headline wording could be sharper (optional item 1).

## Score: 8.9 / 10 (uncapped)

This is a correct and well-organised extension of M5(b1-LH) to a general, explicitly checkable class with masking.
- The centre law generalises T22(iii) with EXP′ now proved instead of assumed.
- The descent rests on a bounded relevance set with relative separation, and needs no lattice margin.
- The canonical block-coefficient certificate gives the class a usable form.
- The (C6) counterexample shows the bounded-size hypotheses cannot be dropped.
- Instances (a)–(d) are verified directly, including a selection-uniform leakage argument for data-dependent packing.

I deducted for the remaining wording and record inconsistencies, and for rates left implicit. I found no mathematical
gap.

## Required fixes (all minor; none changes a hypothesis or a conclusion)

1. **STATEMENT.md (C3) display vs L5_assembly.md Theorem L5.1.**
   - Problem: the STATEMENT says the bound D_n ≤ P(S̃₀ ≠ S*) + P(Ω_nᶜ) holds "for all n large enough that |𝒱_n| ≤ K
     and ℓ_n ≥ 2^{v̄} − 1". L5.1 proves it only for n ≥ n₀, the L3 onset, which also depends on the BM-∞ envelope,
     the SEP onset, σ², M, φ₀, A, v̄ and c_S. On Ω_n alone, Corollary L3.4 is not available below n₀.
   - Fix: replace the clause with "for all n ≥ n₀ (the onset of L3, which includes ⌊n/2⌋ ≥ v̄ + 1) with
     ℓ_n ≥ 2^{v̄} − 1", or keep L5.1's "+ 1{n < n₀}" form in the STATEMENT.

2. **L6_instances.md header vs 00_MAIN.md proof map (Lemma SEL check status).**
   - Problem: L6 says (d-covered) is "not yet re-checked". 00_MAIN records "(d) GAP → v2 (Lemma SEL), sweep", and R10
     raised SEL item 5, which was fixed.
   - Fix: state the record in both places exactly: "Lemma SEL: checked only inside the exhaustive sweep R10 (one minor
     item, fixed); no dedicated lemma check". Do not upgrade it further.

3. **Missing status for the W partition input and the [OP] closure (L6(c); STATEMENT §5; 00_MAIN external inputs; L5).**
   - Problem: "blocks = groups (TLF:71)" is used without a status. The [OP] closure is described two ways (see G4).
   - Fix (a): either quote the recorded status of the TLF:71/W2P2 §1 claim, or prove it inline in two lines. The
     proof: within-group distance ¾ < 1 − ε_n, so complete linkage completes the groups first. B ∈ [9, 16] for g = 9,
     so a group node (size 9) is retained and any union of groups (size ≥ 18) is split. Next-fit cannot place two
     groups in one block (9 + 9 > B).
   - Fix (b): label [OP] once as "PROVED (by this seat, unchecked) from the named premises; corroborated by [W6]
     (candidate)", and use the same wording in STATEMENT §5.

4. **STATEMENT.md (C1′) wording.**
   - Problem: "squared entries ≥ [M_n(σ² + 2M) log n]/((n − 1)φ₀²) after absorbing the small part" is not the
     condition that L8.2 proves.
   - Fix: state L8.2(ii) verbatim:
     √((n−1)φ₀²)·min_{j∈supp γ^L_b}|γ^L_{b,j}| ≥ √(ησ² log n) + √(M_n(σ²+2M) log n).

## Optional suggestions

1. **Premise e4 can be narrowed (G6).**
   - L2 step 9 needs e4 only on {π₀(S*) > ½}, where the start-mode maximiser is unique.
   - W1-N3's clause (c) (N ≤ cap ⇒ the coded `start_mode` returns S*; N = 1 here) covers the coded start mode in
     exact arithmetic. The gap of at least log 2 makes rounding irrelevant at that margin under EX-A.
   - Add a remark in 00_MAIN/L5 that only "unique maximiser ⇒ emitted centre = maximiser" is used. Cite W1-N3 with
     its status as recorded by HQ, and keep "N3 OPEN" for the general invariant.
   - Make the headline say "v3.1 + LS0 as specified (LS0 not in production code)".

2. **Explicit rate (G5).** Record P(Ω_nᶜ) ≤ 2e^{−n^{1/3}} + O(n^{−2}) + O(n^{−1}) + 2v̄2^{v̄}e^{−(log log n)²/2} + 2/log n.
   This gives D_n ≤ P(S̃₀ ≠ S*) + O(1/log n) for n ≥ n₀. Note that the 2 log log n slack in 𝒟₅ can be any ω_n → ∞
   with ω_n = o(log n).

3. **L6(b) "Tails" index slip.** Beta(½, (m−1)/2) = χ²₁/(χ²₁ + χ²_{m−1}), so the comparison event should be
   {χ²_{m−1} ≥ (m−1)/2}, not {χ²_m ≥ m/2}. The bound 16(A+3) log n/n is unchanged once m ≥ n/2 + 1.

4. **L5.1 cap condition.** Scoring S₀ needs only ℓ_n ≥ 2^{v̄} − 2, which is ℓ ≥ τ − 1. The stated 2^{v̄} − 1 is
   correct but slightly stronger; say which one is used.

5. **L3.3(a) "o(1)" factor.** The parenthetical "(the product of O(log n) and o(1/log n)-free factors …)" is hard to
   parse. Write it as Z²·[(1+2x)(1+0.02/n)/(1−ω_n) − 1] = O(log n)·O(n^{−1/3} + log n/n) = o(1).

6. **L8.3 W bullet.** "θε_nΣ_CC⁻¹1·(const)" is loose. State the bound ‖X_Cγ^S‖² ≤ ‖P_C θx_{j₂}‖² = O(nθ²ε_n²) directly.
   This is the only thing L8.2(i) needs.

7. **REPORT.md.** Put (C6)'s scope sentence ("no universal LS0-discovery guarantee; nothing about the full method's
   D_n") and the n = 200 dilution finding (E6 VIS ratios 0.16–0.94) next to the headline, so the asymptotic result is
   not read as a finite-n claim about the study.

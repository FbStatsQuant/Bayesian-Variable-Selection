# Strategy review: adjudication (Claude Opus 5.5)

Date: 2026-11-09. Brief: `SR/BRIEF_ADJUDICATION.md`. Independent of the Astra adjudicator.

**What I read.** I read `CRITIQUE_fable.md`, `BLIND_fable.md` and `BLIND_astra2.md` in full, and `BRIEF_BLIND.md`. I read `W2-UNI/STATEMENT.md` (v1.1.3) and `W2-UNI/REPORT.md` in full. From the chapter I read `FINAL/sections/s3_posterior.tex` and `s4_sampler.tex` in full, and the GEN and GROW parts of `s5_hpm.tex` plus the (C6) lines in `s7_impl.tex` and `s8_scope.tex`. I also read the headers and flags of the APP, FAC-A, FAC-B, FAC-X, FAC-S5 and FAC-PK reports. In the code I checked `v3_run.R:150-163` and `cpp/v3_engine.h:111-128` and `182-192`, and the bridge definition in `02_method.tex:196-201`. I did not open `BLIND_astra.md`, which is scope-contaminated and not one of the scored packages.

I re-checked no full proof. Wherever a statement below is my own reasoning and not taken from a file, it is marked **[O]**.

---

## 1. Verification of the critique's load-bearing claims

**(a) Verification level of UNI-P and T03♯. Mostly accurate, but it understates the checks.**
- T03♯'s status is "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)", with no council score (`s3_posterior.tex`). The critique is right that there is no council pass.
- It is not true that T03♯ has the lightest trail. It has one same-family verification and one cross-family verification, which is two independent checks.
- UNI-P is APP L1_POST. At lemma level that file reads "PROVED (by this seat, unchecked)", with one review (R02, V-W-A). However, the APP report as a whole passed council round 3 (Sol 9.1, Opus 9.1; `W2-APP/REPORT.md:2`). The critique's "one review" leaves this out.
- Verdict: the spine is checked but has never had a council pass. Every other theorem rests on it, so the recommended independent adversarial re-check is still right. The focus list in critique §2.1 is good: the middle range j₀ < |J| ≤ m♯ under the unnormalised floor g₀ only, rank-deficient models under the unit ridge, response standardisation, and the IG(0.01, 0.01) term.

**(b) Factor results and the scope of Theorem NEG. Verified, with one nuance.**
The growth limits of the positive factor results are:

| Result | Growth limit |
|---|---|
| FAC-A / UNI-1 | log p/log n < α₀(κ̄) ≤ 1/6 |
| FAC-X | < 1/2, iid compound symmetry; A_S for general loadings |
| FAC-B | p ≤ n/2, exact Gram |
| FAC-S5 | p ≤ n/2 for the start; < 1/2 for the path |

The nuance is FAC-PK's Theorem PATH and Theorem FAC-PK. They are positive results for K < p ≤ n − 1, but only under a changed cap (≥ (1+δ)|S̃₀|), so they do not describe the coded method.

Structural point **[O]**: every exact-Gram result needs p ≤ n − 1 by construction. No exact-Gram ticket can ever reach p ≫ n.

NEG's scope is as the critique states. It covers exact-Gram compound symmetry with liminf p/K > 16/15 and condition (PB). It is about LS0 with any cap ≤ |S̃₀| − s₀ − 2 + ⌊n^β⌋, which includes the shipped cap. It says nothing about the full method, and P6 is pending (`W2-FAC-PK/REPORT.md:7-11, 29-31`).

**(c) The sampler has no proved in-probability role. Verified.**
The chapter's own not-proved box says: "No in-probability sure-screening or selection theorem for the shipped pooled R′ = 4 PIPs or MPM." N1 and Corollary E hold in expectation, are evidence-weighted, and concern `pip_plain`. M1(i) needs the stacking configuration R′_n ≈ 4 log₂(n+p). I found no relative-consistency result for Ẑ.

Code check:
- `pip_primary` is `rowMeans` over islands of the **Rao–Blackwell** PIPs (`v3_run.R:162`).
- Those RB PIPs are o_j values recorded mid-round, before each Gibbs draw (`v3_engine.h:128`, `:364`).
- The MPM is `pip_primary > 0.5`.

Reported-HPM discovery is carried only by LS0 through M5(0) + [OP]. The bridge particles and the π₀ draws are scored but are used by no theorem.

**(d) Lemma LT. The inequality is correct; two of its claimed uses fail as stated.**

*Proof check.* N1 with h = 1{S ≠ S₀} gives E[W_r(1 − A_r) | 𝒞] = δ_n, where W_r = Ẑ_r/Z. On the event {A_r ≤ ½, W_r ≥ η}, the product W_r(1 − A_r) is at least η/2. Markov's inequality then gives P(A_r ≤ ½) ≤ 2δ_n/η + P(W_r < η). Because δ_n is data-dependent, the bound has to be integrated as E[min(1, 2δ_n/η_n)]. With δ_n = O_P(√(log n/n)) and η_n = n^{-1/2} log n, this tends to 0. So the conclusion holds for **end-of-round particle states**, that is, for `pip_plain`.

*Flaw 1: RB PIPs, `pip_primary` and the MPM do not follow.* The RB accumulator records o_j at the **intermediate** state at the moment coordinate j is updated, not at the end-of-round state.
- N1 as proved covers end-of-round populations only. An extension to intermediate states is plausible, because every elementary kernel is invariant, but it is unproved.
- Even with that extension, max_j |RB-PIP_j − 1{j ∈ S₀}| needs control at p different intermediate times. A per-step Markov bound loses a factor of p.
- The summed route bounds the error through Σ_{j∉S₀} π(j ∈ S) = E_π|S ∖ S₀|. That needs E_π|S △ S₀| = o(η_n). The available bound is roughly m♯_n·δ_n ≍ (log n)^{3/2} n^{-1/2}, which is **not** o(n^{-1/2} log n) **[O]**.
- Fix: assume the stronger premise that W_r is bounded away from 0 in probability, and prove the mid-round N1 extension.

*Flaw 2: "much weaker than relative consistency" oversells the lemma.*
- By the deterministic bound in F Thm 4(b), A large at every stage implies W ≳ π(S₀). By LT, W ≥ η implies A large.
- So the premise is close to equivalent to "the particle system holds S₀", which is the sampler question itself.
- LT is a correct **interface** and a useful one-line remark. It is not a reduction, and the paper should not present it as one.
- The ledger-sum diagnostic catches only one failure: S₀ found by LS0 but lost by the particles. When nothing ever scored S₀, the diagnostic is blind.

*Smaller point.* The single-step equivalence with Astra's N_e·π₀(S₀) → ∞ is right up to logs **[O]**.

*Related check that passes.* F Thm 4(b)'s Hölder step requires a geometric bridge. The coded bridge is γ_φ = γ₀e^{φd} (`02_method.tex:200-201`), which is geometric, so the step is valid. The deterministic lower bound Ẑ_r/Z ≥ (π(S₀)/π₀(S₀))·Π_t A_{t−1} also checks **[O]**.

**(e) GEN (C6) and NEG as counterexamples. Only partly valid.**

*(C6) is misused.* The chapter states that (C6) "is about the cap ℓ_n … (C6) is **not established for MR1**", and MR1 is the shipped cap ℓ_n + |S̃₀| (`s7_impl.tex:80`). Critique §3(1) cites (C6) as evidence against the method as coded. That use is wrong.

*NEG is valid but narrow.* It covers LS0 only, on exact-Gram compound symmetry, for K < p ≤ n − 1.

*No full-method counterexample exists.* Draws, particles and the final local search all score models, and no theorem shows that all of them miss S₀.

APP reports that a Python component port reached S₀ with LS0 in 40/40 runs on pervasive designs where the proof routes are blocked (`W2-APP/REPORT.md`, "Pervasive correlation"). Those runs are observations only, not production runs. Even so, the files say explicitly that the obstruction is to the proof routes.

So "unconditionally no" (critique §3(1)) is a **conjecture**. It is plausible for p ≫ n with saturated starts, but it is not proved. With s₀ fixed and p ≤ n^A, there is also no computational barrier in principle. Any impossibility claim has to be method-specific and proved for the full pipeline.

---

## 2. Scores (0–10)

Criteria: **DA** = design-agnosticism/generality of assumptions; **Str** = strength of conclusions, especially at p ≫ n; **Faith** = faithfulness to the coded method; **Prov** = provability/risk (10 = safe); **Reuse** = reuse of checked work; **Val** = paper value vs Song–Liang.

| | DA | Str | Faith | Prov | Reuse | Val | Mean |
|---|---|---|---|---|---|---|---|
| **A** current program | 5 | 6 | 8 | 8 | 10 | 6 | 7.2 |
| **B** CRITIQUE package | 7 | 7 | 8 | 7 | 9 | 8 | **7.7** |
| **C** BLIND_fable | 7 | 6 | 8 | 6 | 5 | 7 | 6.5 |
| **D** BLIND_astra2 | 6 | 4 | 9 | 5 | 4 | 5 | 5.5 |

**A, current program.**
- DA 5: the posterior theorem is genuinely general, but the reported-model theorems are structural classes (metric locality; one factor) presented as general assumptions.
- Str 6: posterior concentration and UNI-0 hold at any A. There is nothing for pervasive designs at p ≫ n, and nothing in probability about PIPs or evidence.
- Faith 8: shipped cap and premises are explicit. The PIP statements concern estimators that are not shipped (`pip_plain`, stacking).
- Prov 8: almost everything is proved-checked. The remaining factor tickets are high-risk with low yield.
- Reuse 10: by definition.
- Val 6: it goes beyond Song–Liang on the reported model, but the story is fragmented, the sampler has no role, and there is no predictive corollary.

**B, CRITIQUE package.**
- DA 7: theorem statements are free of design families, and certified screening needs only a sparse floor. (V)+(L) is still defined relative to the method's blocks.
- Str 7: it adds a screening statement at p ≫ n for every floor design, and sampler outputs in a narrow or conditional regime. It is still silent on the reported model for pervasive p ≫ n designs.
- Faith 8: it targets `pip_primary` for any frozen schedule. The RB gap in LT (§1(d)) has to be fixed.
- Prov 7: most additions are cheap. However, "(V)+(L) at polylog |Q| for Gaussian rows" is **not** a restatement. PLR also needs Lemma NA-R's reference/atom conditions (R1)–(R3), which are locality-type. Only GROW's C log n fixed-design form follows from existing proofs.
- Reuse 9: everything checked is kept; it adds and demotes rather than discarding.
- Val 8: the closest of the four to a Song–Liang-shaped paper with a real output theorem.

**C, BLIND_fable.**
- DA 7: primitive conditions B1/B2, no design families.
- Str 6: the leakage budget is at most log n, against polylog in the current program. The sampler theorem covers only the concentrated bridge.
- Faith 8: it found the code cap and treats both PIP poolings.
- Prov 6: Theorem 1 would be re-proved from scratch. Thm 2(a) "exact reduction" is wrong for fixed designs (critique §1.3(b) is correct). Thm 5(b) is speculative.
- Reuse 5: it maps onto T03♯ and GROW but does not use them.
- Val 7: clean story, with the design-free size lemma as visible novelty.

**D, BLIND_astra2.**
- DA 6: it needs a two-sided sieve eigenvalue condition, which is stronger than T03♯. Its interface theorems have no primitive premises.
- Str 4: there is no primitive reported-model theorem. Its PIP premise L/M_n → ∞, with M_n = sup π/π₀, essentially requires π₀ ≈ π globally, and its global-oscillation evidence condition is similar. Neither will hold in any regime of interest **[O]**.
- Faith 9: the most careful code reading of the four (equal-weight `pip_primary`, rejected proposals scored, fallback, PRNG caveat).
- Prov 5: (Tail) was open for Astra but is already done in T03♯. Its primitive basin step is high risk.
- Reuse 4: it reuses little of the existing program.
- Val 5: an honest set of interfaces, but thin on primitive theorems.

---

## 3. Recommendation

**Adopt package B, with the five modifications below.** Its architecture is right: the posterior theorem; start and misspecification; the reported model under method-relative primitive conditions; sampler outputs; certified screening; a limits section; and design classes moved to an examples table.

1. **Repair Theorem 4.**
   - 4(b) LT: state it for end-of-round particle summaries. For `pip_primary` and the MPM, either prove the mid-round N1 extension and assume Ẑ_r/Z bounded away from 0 in probability, or prove a "particles stay at S₀ through a sweep" lemma.
   - Present LT as an interface, not as a weak premise.
   - 4(c), the concentrated bridge: label it honestly. Zero leakage fails whenever a truth's correlated neighbour falls in a different block, which can happen even in local designs **[O]**. It is a narrow regime.
   - 4(d), draw discovery: keep it. It is cheap and verified from code: `step_indep` scores the π₀ draw before the accept step (`v3_engine.h:184-186`).

2. **Do not promise Theorem 3 in partition-free (V)+(L) form at polylog |Q|.**
   - Headline: GROW's fixed-design form (|Q| ≤ C log n), restated with no reference to design families.
   - Main example: UNI-0 at polylog |Q| for local designs and any A.
   - Optional medium-risk ticket: generalise PLR's (R1)–(R3) to a non-local primitive condition. The critique's 4–5 days for this is an underestimate.

3. **Correct the limits section.**
   - (C6) concerns the old cap ℓ_n only.
   - NEG concerns LS0 only.
   - Do not write "an unconditional design-agnostic reported-model theorem is impossible". Write "no current route; a counterexample for the full method is open".
   - Cheap strengthening **[O]**: on the NEG design, show D_n·π₀(S₀) → 0. Together with NEG, that proves both deterministic discovery and draw discovery fail, which leaves only the particles and the final local search.

4. **Do not freeze p ≫ n pervasive designs entirely. Freeze the p < n/2 exponent work.**
   - Stop FAC-S5/S5F, XA, K2, PKA, FAC-GL and all exact-Gram tickets. Exact-Gram tickets cannot reach p ≫ n in any case.
   - Run P6 (full method; compound symmetry and two factors; p > K and p ≫ n) **first**, then decide D1. If the full method succeeds there, a theorem for that regime is the most valuable missing piece and the main "weaker than achievable" risk (Felipe's main risk). D1(c), removing factors before selection, is then the natural route, and it is a method change for Felipe to decide.

5. **Add a sharpness item for the spine.** This is the gap described in §5.

## 4. Top three risks

1. **The spine.** T03♯/UNI-P carries everything and has had no council pass. One error in the middle size range or in the standardisation step would propagate to every theorem. Mitigation: an independent adversarial re-check in week 1, before any new proving, and a reading of Song–Liang's Theorem S.
2. **Sampler theorems only where the sampler is not needed.** 4(c) needs a start that is already concentrated on S₀. LT's premise is close to circular. A referee will see this immediately. Mitigation: label both honestly, and make draw discovery and LS0 the stated discovery mechanisms.
3. **The headline regime is uncovered.** At p ≫ n with pervasive correlation, which is Felipe's motivating regime, the package offers only posterior concentration and conditional screening. The APP port observations (40/40) suggest the method may do better than the proofs show. Freezing without P6 risks shipping a weaker theorem than is achievable.

## 5. What all four miss

- **The (C6) cap mismatch** (§1(e)). The critique's impossibility argument partly relies on a counterexample for a cap the code no longer ships.
- **Exact-Gram constructions are structurally capped at p ≤ n − 1.** That alone should end every exact-Gram factor ticket for the p ≫ n goal.
- **Empirical evidence against "freeze".** The APP port reached S₀ on pervasive designs where all proof routes are blocked. None of the four packages weighs this.
- **Optimality of the posterior theorem.** No package asks whether T03♯'s conditions are near-necessary for this prior:
  - the floor size j₀ = ⌈(2A+1)s₀⌉ + 1;
  - the unnormalised floor up to m♯_n;
  - the beta-min constant c₀ = max{4C*, 32[s₀(A+1)+2]} against the information-theoretic scale ≍ A·log n/n.

  A short sharpness section is cheap insurance against the "weaker than achievable" risk, and it fits the memory rule on a sharpness gate. Two possible contents **[O]**: a design whose floor holds at size j₀ − 1 but whose posterior is inconsistent, or a beta-min constant at which exact selection fails.
- **A full-method negative result.** The modest combined "LS0 plus draws fail" result in §3 item 3 would turn the limits section from statements about LS0 into statements about the method.

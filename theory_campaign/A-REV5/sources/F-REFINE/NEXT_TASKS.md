# F-REFINE — NEXT_TASKS: the five highest-value remaining proof tasks (ready-to-run Opus cloud specs)

Lead: F-REFINE (Fable 5.1), 2026-11-02. Each spec below is written in the style of `theory_campaign/tasks/*.md` and
can be copied into `theory_campaign/tasks/<ID>.md` unchanged. All runs follow `theory_campaign/PROTOCOL.md`: work on
`theory/<ID>`, write only under `theory_campaign/<ID>/`, commit and push after every step, protocol status words
only, Python only (no R), scripts with fixed seeds.

Ranking (value to the paper per credit): W5-VMASK > W5-VPGD > W5-B2ENV > W5-FAVIID > W5-LOCKBOOK. The first two are
verifications of load-bearing but unreviewed proofs and are cheap; the third is the one research task; the fourth
closes relevance; the fifth locks the low-risk half. Items that are **not** Opus proof tasks are listed at the end.

---

## W5-VMASK: Adversarial verification of the masked-regime instance of T38 (W3-PXN and W4-T38FULL's new lemmas)

**Paper role:** Thm 5(b1), (b1-LH), (b1-LH-iid): the only masked-regime consistency instance with every premise
proved. Today it rests on two single runs with same-family checks only.

Fetch and read: `origin/theory/W3-PXN` (`theory_campaign/W3-PXN/`: REPORT, PROOF §§0–14, scripts, results),
`origin/theory/W4-T38FULL` (`T38_STATEMENT.md`, `T38_PROOF.md` §§1–3, `scripts/`), and the inputs they cite:
`origin/theory/W1-EXP` (PROOF §§1, 4: Lemmas 1.1–1.4, 4.1–4.2, Thms 5–6), `origin/theory/W3-VEXP` (REPAIRS R3),
`origin/theory/W1-T37R` (PROOF: Lemma 2(a), Theorem A(A3) lattice form), `origin/theory/W1-T38E` (PROOF: E1(a)(b),
E3). Also `Docs/Theory/theorems/00_COMMON.md`, `Docs/Methodology/METHODOLOGY_v3.md` §§6.3, 6.10, and
`Scripts/SMC_BVS/core/cpp/v3_blocks.h`, `v3_engine.h::local_search`.

You are an **independent referee**. Try to break the claims. For each step record VERIFIED, GAP (fixable or not) or
ERROR (with a counterexample). Claims to check, in this order:
1. **W3-PXN Lemma B** (exact Beta laws of the start statistics at the reference S°, independent of y, through the
   conditional-independence identities F1–F3 and the Grassmannian step after standardisation) and **Lemma Tr** (the
   truncated moment E[(1−X)^{−ν}1{X ≤ τ}] bound). These two carry the 2^B-free rate 1 − π₀(S°) = O_P(√(log n/n)) at
   p ≫ n. Check that W1-EXP Lemmas 1.1, 1.2, 1.4 really never use block membership (PXN uses them for arbitrary sets
   of size ≤ s₀ + 2).
2. **W3-PXN P1** (partition = groups w.p. → 1 under the cited correlation concentration; the R13 tie rule; the
   margin condition used when p > 4300), **P3**, **P4** (limit law), **P5**, **P6** (the TD′ lattice condition at
   S° from the component decomposition Lemma Λ and the margin table §9.3; the (L) margin and its failure probability
   (s₀+1)/√(2π(n+1)t_n)), **P7** (D2-a,b,c proved; D2-d NB is a sketch: say exactly what is missing), **P8** (the
   design de-randomisation lemma for T03).
3. **W4-T38FULL Lemma LS-score** (scoring without certification; the scan-before-limit engine fact; the emitted
   centre), **Lemma M** (uniform score comparison under a population margin m_n ≥ M_n√(log n/n): the χ²/Gaussian
   union over all sets of size ≤ k + s₀, the RSS floor through span(A ∪ S₀), the deterministic E1 bounds), **Theorem
   b1** ((M1)–(M3) + OP-LS0 ⇒ D_n → 0), **Proposition LH-LAT** (unit additivity of Δ on LH; the neighbour case list;
   the explicit sharp margin m₀; the referee's remark that only |ψ| < 1 is needed for the algebra).
4. Consistency between the two runs: PXN's P6 (lattice condition via its own margins) and T38FULL's LH-LAT (margins
   via unit additivity) must agree on LH exact Gram. Compute both margins on the same parameter grid and report
   any discrepancy.
5. Reproduce independently, with your own scorer and your own port of the partition (do not import their code):
   the LH-iid table at n ∈ {200, 400, 800} (config A and B), the LH exact-Gram LS0 check (G = 12, g = 9), the
   KS tests of Lemma B, and the (L)-failure rate. Add one adversarial design: |ψ| close to ρ, and a null group with
   within-group correlation above ρ, to probe P1 and the (M1) margin.
6. Method faithfulness: LS0 as modelled (centre emitted, tie rule for argmax π₀, cost) versus `local_search`; the
   start mode by max-plus convolution versus `v3_start.h`.

Deliverable: `theory_campaign/W5-VMASK/REPORT.md` with the verdict table (claim | verdict | evidence), complete
repairs of fixable GAPs in `REPAIRS.md`, your scripts and outputs, and the confidence card. State plainly whether
Thm 5(b1-LH-iid) can be cited as PROVED (pending cross-family review) or must stay a single-run claim.

---

## W5-VPGD: Verify and complete the asymptotic repair theorem (W3-PGD Theorem W), and check PGD on the study's designs

**Paper role:** Thm 3(iii), the asymptotic clause of the repair theorem (refined T37(iii)). W3-PGD proved Theorem W
in `PROOF.md` but left `REPORT.md` as a stub, and no referee has read it.

Fetch and read: `origin/theory/W3-PGD` (PROOF.md in full, PLAN.md, scripts, results), `origin/theory/W1-T37R`
(PROOF: Lemma 0, Lemma 2, Lemma 3, Theorem A, Theorem B, Theorem C and the PGD/LD definitions; Exp 3),
`origin/theory/W3-VT37R` (REPORT §4.3 EXP3-R; REPAIRS R4, R5), `origin/theory/W1-T03R` (PROOF §4: SE_λ, SE_w),
`origin/theory/W4-T38FULL` (`T38_PROOF.md` §3.4 Prop. LH-LAT, for consistency). Also 00_COMMON and
`Scripts/Data_generators/` (reimplement S1–S6 in Python; R is not available).

Goals, in order:
1. **Referee Theorem W and its lemmas** line by line: Lemma 1.1–1.3, Prop P1 (GERC + TRC ⇒ PGD; the five
   non-progress move types), Prop P2 (block iff criteria (B1)–(B3)) and Cor P2′ (equicorrelated formula), Prop P3
   (TRC sufficient conditions), Prop P4 (sharpness), Lemma P5/Cor P6 (stability, random designs; the cited
   Bickel–Levina bound), Lemma Q/R/G/U (noise side; the score representation with the ridge; the pair geometry
   ‖r_A − r_B‖² ≤ C₁g), Lemma LD and Lemma S ((α), (β), (γ) under (H1)/(H2)/(H3)), Theorem W, Cor W′, Prop C-LD.
   Record VERIFIED / GAP / ERROR per step; repair what you can.
2. **The constant in (★).** W3-PGD notes its threshold is off by a factor 3–4 from C-LD's 1/(2A). Sharpen (★) or
   show why the gap is intrinsic to the local/far decomposition.
3. **PGD on the study's population covariances.** For S1, S3, S4, S6 (block-orthogonal at population level, one
   truth per group of 5, the β pattern of `gen_dev_data.R`) compute η*(d) from Cor P2′ for d ∈ {1, 2, 3} and check
   it by direct enumeration of (B1)–(B3). For S2 (AR) and S5 (common factor), which are not block-orthogonal,
   evaluate GERC and TRC numerically on R_{2,2} at the population Gram and say whether PGD(η) holds for some η > 0.
   Then check the realised-design transfer (Cor P6) at n ∈ {200, 800, 3200}, p = 500: fraction of designs with
   PGD(η/2) on R_{2,2}(𝒟) for 𝒟 = nulls in the truth blocks, and the realised TD′_P(R_{2,2}(𝒟)) frequency.
4. **Consistency with Prop. LH-LAT.** On LH exact Gram, Theorem W's PGD(η) on Lat(S°) should be implied by
   POP-LAT(S°, m₀). Show the implication or the discrepancy.
5. **Write the missing REPORT** for W3-PGD's results in the protocol format (headline, statements, proofs cited by
   label, evidence, what fails, escalation, confidence card), so that Thm 3(iii) has a citable source.

Deliverable: `theory_campaign/W5-VPGD/REPORT.md` (verdict table + the completed report of Theorem W), `REPAIRS.md`,
scripts, results, confidence card. Numerics at p ≤ 30 exact where enumeration is needed (R_{2,2} has ≤ C(s₀,2)·p²
states).

---

## W5-B2ENV: A no-method-change masked theorem. (1) Finish D2's NB′ on LH, c = 1. (2) Instantiate the envelope route (b2) on LH via W4-SHARE's D5 and Prop. M

**Paper role:** Thm 5(b1′) and (b2). Without LS0 the masked regime is conditional. Two routes avoid the method
change: the pilot's first stage (D2) for one masked variable, and the Gibbs path after envelope-controlled
delivery (W4-SHARE D4/D5). Part (1) has a guaranteed deliverable; part (2) is the research part.

Fetch and read: `origin/theory/W4-SHARE` (PROOF.md §§0–7: D4, D5, Prop G, SH, X, M, Theorem B2-W4; NOTES;
scripts), `origin/theory/W1-T38E` (PROOF §§3–5: Lemma A, Lemma S, Theorem D2, C1; §7), `origin/theory/W3-VT38E`
(REPORT §3.1 NB′ and r*, §3.2 reversible C1, §5.3), `origin/theory/W3-PXN` (PROOF §12: P7, the NB sketch;
REPORT §6), `origin/theory/W4-T38FULL` (`T38_PROOF.md` §4.2: the second NB sketch; §5), `origin/theory/W1-T24G`
and `origin/theory/W2-PREM` (Theorem B♯, Theorem L on LH, IND-T), `origin/theory/W1-EXP` (PROOF §4: LH).
Also METHODOLOGY_v3 §§6.5–6.8 and `v3_engine.h` (`pilot_next_phi`, `run_island_s`, `resample`).

Goals, in order:
1. **Referee W4-SHARE** (it has no verifier): D4's supermartingale (the predictable stopping time τ, the convexity
   step, the monotonicity of P ↦ P(1 − e^{−θ/P})), D5's fitness-ratio bound (2.1) and Prop G (grid independence),
   Prop SH, Prop X, Prop M(a) (deterministic), Theorem B2-W4 (islands, REPAIR on W). Record verdicts; repair gaps.
2. **Finish NB′ for D2 on LH exact Gram, c = 1** (and on LH-iid if time permits). Both existing sketches reduce to:
   the H₀ = max(n, p, 2500)-ish initial pilot draws have d-range ≤ 2T_e·(something) with probability → 1, or S₀ is
   drawn. Prove P(NB′ᶜ) → 0 by bounding (a) the probability that any pilot draw contains a proxy of the masked hub
   or an outsider with d higher by Θ(n) (peeling bound on π₀(S ⊉ S°)), (b) the uniform d-range on the good set
   (O(log n) against the threshold ≈ 2T_e). State the rate. This upgrades Thm 5(b1′) on LH (c = 1) from PROOF SKETCH
   to PROVED, giving the paper its first masked instance **without LS0**.
3. **Envelope route on LH, c = 1 first.** Build the potentials: h_t = indicator (or a smoothed version) of the
   lattice state that is γ_{φ_t}-optimal on Lat(S°) (Prop M(b): the within-lattice path is downhill for
   φ ≥ φ_n → 0), with W = {S₀} ∪ (lattice states at distance one) at the end. Bound: (TRACK) exits η_t by Lemma A
   endpoint odds and the gain expansions (W1-EXP Lemma U); the oscillation κ_t against outsiders (states outside
   the lattice with higher d: proxies of hubs, S° + null, S₀ + null) using F- and π₀-gaps; confinement 𝔛_t by
   Prop X-type gates. Target: Γ + Σ_t η_t ≤ log(Nπ₀(h₀)/T_e) − ω(1) with N = N_e and T ≤ T_e = 1000 under the v3
   budgets. If it fails, say exactly which outsider class or which exit term is too large, and whether a larger N_e
   schedule (a budget sequence, allowed by Felipe's premise) repairs it. Then REP on W from Theorem B♯ / Cor P1
   (distance one) with IND-T.
4. **Prove Prop M(b)** (score gain along the lattice; currently PROOF SKETCH) as a lemma, since (3) needs it.
5. **Numerics** (exact scores, p ≤ 30, LH config A of W1-EXP, production packing from `v3_blocks.h`, the method's
   pilot/final-run rules): simulate the potential uninterrupted final run and measure Γ, the η_t, the envelope
   breach frequency, and delivery, against the bound; and the pilot-stage scoring frequency for D2.

Deliverable: `theory_campaign/W5-B2ENV/REPORT.md` with statements, proofs (PROOF.md), numerics, what fails and why,
escalation, confidence card. A clean negative on (3) ("the envelope needs N ≫ T e^Γ with Γ ≍ … on LH, so (b2) needs
a budget sequence N_n = …") is a valuable result.

---

## W5-FAVIID: A 2^B-free favourable-regime start rate on iid designs with the actual partition, and T26's (P1) on study-like designs

**Paper role:** Thm 2(iii), Thm 5(a), Thm 6 (P1). The locked and W1-EXP favourable rates carry 2^B (≥ 16,384 at
B = 14), which makes them numerically vacuous below n ≈ 10⁹; and the in-sample favourable regime for the study's iid
designs S1/S3/S4/S6 is a GAP (the packing depends on the noise column). W3-PXN's Beta-truncation method (exact Beta
laws + Lemma Tr) removes 2^B on LH-iid and should transfer to the favourable case.

Fetch and read: `origin/theory/W3-PXN` (PROOF §§2–6: Lemma B, Lemma Tr, P1, P3; REPORT §8 "Sharpened T22(iii)"),
`origin/theory/W3-VEXP` (REPORT rows 23–24; REPAIRS R3 and §D dilution; `scripts/study_check.py`), `origin/theory/W1-EXP`
(PROOF §§1–2: Thm 1, Prop 2.1/2.2, Thm 2, Thm 6; §4.3), `origin/theory/W2-T26` (REPORT §4.1–4.2; PROOF §1:
Theorem A/B; the (P1) premise), locked T22(iii) (`Docs/Theory/proofs/`, `LOCKED_PROOFS.md`), 00_COMMON,
`v3_blocks.h`, `Scripts/Data_generators/`.

Goals, in order:
1. **Theorem (favourable, iid rows, fixed partition).** Rows iid N(0, Σ) with Σ block-diagonal over groups, one
   truth per group, p ≤ n^A, fixed nonzero θ, and the event P_n = {the v3 partition equals a fixed union of groups}
   (W3-VEXP R3's device). On P_n, prove 1 − π₀(S₀) = O_P(√(log n/n)) **without** the 2^B factor, by PXN's method at
   the reference S₀ (U_h° = S₀ ∩ C_h; the visible-group computation). State the constant's dependence on B and g.
2. **P(P_n) → 1 for the study's group structure** (groups of 5, B = 14, two groups per block): is there a fixed
   partition the engine converges to? If the packing of whole groups into blocks is noise-dependent, prove the
   rate on the event "every block is a union of whole groups" (W3-VEXP found this holds in every design at
   n = 200) and show that the bound is uniform over the finitely many such packings. This closes the partition–noise
   decoupling GAP without a leave-one-column-out lemma.
3. **Dilution threshold.** From W3-VEXP's Prop D and W3-PXN's Prop W, derive the finite-n threshold n*(design) at
   which the start becomes favourable (median π₀(S₀) > ½) for S1/S3/S4/S6 at p ∈ {500, 1000}, scale ∈ {0.5, 1},
   as a function of (θ, v_T, p, s₀); check it against exact π₀ computations at n ∈ {200, 400, 800, 1600, 3200}.
4. **Consequences.** State the resulting versions of Thm 5(a) and Thm 6's (P1) for the study-like family with the
   realised grid T_n, and give the first n at which (T_n+1)Δ_n < 1 with T_n from the method's pilot rule (simulate
   the pilot's grid, not T^max).
5. Numerics at p ≤ 30 exact (convolution of block tables), and at p = 500 by the same convolution (the start law is
   block-wise, so exact π₀ is cheap).

Deliverable: `theory_campaign/W5-FAVIID/REPORT.md` + PROOF.md + scripts + results + confidence card.

---

## W5-LOCKBOOK: Lock the low-risk half. T32(i); the GUARD/OUT/SR code audit; referee W2-BOOK and W2-T26; one STATEMENTS.tex for Prop 1, Prop 2, Thm 4, Thm 6

**Paper role:** Prop 1, Prop 2, Thm 4, Thm 6 and Thm 5(c). All are PROVED candidates from single runs with no
referee, and three implementation facts (GUARD, OUT, SR) are used as hypotheses without an independent code check.

Fetch and read: `origin/theory/W2-BOOK` (REPORT, PROOF §§0–4, STATEMENTS.tex, scripts), `origin/theory/W2-T26`
(REPORT, PROOF §§1–6), `origin/theory/W2-VT24G` (REPORT §6: the (e′) edits), `origin/theory/W1-T24G` (Theorem B,
Cor B-M), `origin/theory/W4-T38FULL` (`T38_STATEMENT.md` Part I (0), (c); `T38_PROOF.md` §§1, 6), locked T07,
T06, T12, T31, T21, T11(iii), T14, T15, T23, T25, T32 (`Docs/Theory/proofs/`, `COLLECTED_PROOFS_v2.tex`,
`LOCKED_PROOFS.md`), and the engine: `v3_runtime.h`, `v3_engine.h`, `v3_core.cpp`, `v3_ledger.h`, `v3_calib.h`,
`v3_run.R` (read only; R cannot be run).

Goals, in order:
1. **Referee W2-BOOK**: Lemma RO and its counterexample (conditioning on completion), Prop 2 (a)–(f) including the
   ¾-covariance formula and the locked island independence it uses, Prop 1 (i′) sharpness and (iii′) certificate,
   Thm 4's (e′)/(e-M)/(d⁺) wiring against W2-VT24G's three edits, the run/output split edits for T11(iii), T14(i),
   T15, T23(ii), T25(iv), T31, T34. Reproduce the exact-law numbers (`frozen_run_exact.py`) with your own code.
2. **Referee W2-T26**: Lemma 1 (Δ_n exact), Lemma 2 (ρ̄ exact), **Lemma 3's use of T15 at a terminal-round prefix
   (T12(i.b))**, Theorem A (A-0)–(A-ii) including the output form, Theorem B's composition, Prop C (ORTH) as a
   sketch. Reproduce the p = 18 premise scan at three sizes.
3. **Code audit (read-only), as a referee of implementation facts.** (a) GUARD: list every code path that can set
   `resource_limit` after the final run starts and confirm none touches an RNG, a setting, the inherited store or
   the cache; confirm the stop-only coupling. (b) OUT: can any failure mode (`resource_limit` after allocation,
   `numerical_failure` in the final run) return a *partial* evidence or PIP differing from the potential run's? (c)
   SR: `step_gibbs` scores both configurations and offers both to the HPM, including when the flip is infeasible at
   the cap. (d) IND-T's premise: one sequential stream per island, read at state-dependent rates, no per-particle
   streams. (e) The scan-before-limit rule of `local_search` and the `emit_centre` flag. Write each as a one-line
   implementation lemma with file:line evidence.
4. **Prove T32(i)** (the score-evaluation ceiling of the SMC branch) from METHODOLOGY_v3 §§6.5–6.10 and the engine
   loops, as a deterministic count: per round ≤ m = p + B + 2 evaluations, per stage one round per particle, the
   pilot and final budgets, the local searches (≤ 2ℓ + 3 of them, each ≤ (ℓ+1)max_k[p + k(p−k)] scores). This makes
   Thm 5(c) a theorem.
5. **STATEMENTS.tex**: paper-ready statements of Prop 1, Prop 2, Thm 4 (with routes (a), (d)/(d⁺), (e′)/(e-M)) and
   Thm 6 (with (P1) in the realised-T_n form), each with the hypotheses named and the run/output split applied, plus
   the n = 200 disclosure sentences they need (P(U) = 6/2,400 with Wilson interval; "never given completion").

Deliverable: `theory_campaign/W5-LOCKBOOK/REPORT.md` (verdict tables for W2-BOOK and W2-T26; the implementation
lemmas; the T32(i) proof in PROOF.md), `STATEMENTS.tex`, scripts, results, confidence card.

---

## Not Opus cloud proof tasks (recorded so HQ can route them)

- **E_LS ledger extraction (Owls, R):** for each of the 541 fits with a final centre in 𝓡₂∖S₀, compute F(S₀) − F(S_c)
  at the final local-search centre and whether the final search improved the HPM (W3-VT37R escalation 1). Also the
  count of strict same-size posterior misses by scenario at c = 0.5 (Prop 1's certificate).
- **O-LS0 pilot (Owls, running):** LS0 post hoc on the 2,400 regenerated datasets; report scored/certified by
  scenario and |S̃₀ Δ S₀| ≤ ℓ+1 split; this is the investment-rule evidence for LS0.
- **Cross-family review (Astra, A-REV1/A-REV2, not started):** Theorem B/B′, T38(b)-R, Lemma S, D2, E3; T03♯,
  Theorem A, EXP′. Add after W5-VMASK: Lemma M, LS-score, LH-LAT, PXN Lemma B.
- **Felipe:** confirm SR; decide LS0 (emit centre, tie rule, labels, run-to-certification option); the n = 200
  disclosure wording; correct FROZEN_LIST's m_n sentence and FABLE_REVIEW's "(e′ = T37)" label.
- **VAL-FP replay (OPS):** η and ε for Prop 2(f) on a sample of PROD-H fits.

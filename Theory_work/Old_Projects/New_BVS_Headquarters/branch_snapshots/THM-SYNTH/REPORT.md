# THM-SYNTH — REPORT: the final theorem list for paper 1 (Track B, step 2)

Run THM-SYNTH (Opus 5.5), branch `theory/THM-SYNTH`, 2026-11-03. Deliverables: `THEOREM_LIST.md` (the list; fields
(i)–(vii) and tier per item; summary table at the top), `HQ_PLAN.md` (the per-theorem HQs, dependency graph, Lean
plan), this report (tiering, the thesis sentence as a theorem, disagreements, what was dropped, confidence card).
Script: `scripts/check_lemmas.py` (seed 20261103; run through `owls_run -j 1`; output `scripts/check_lemmas.out`).
**No new proofs.** Every status is copied from its source and never upgraded. Three statements are **NEW-SYNTH**
(proposed here; PROOF SKETCH at most): Theorem H (bounded functionals, joint inclusion), Lemma KL (the exp(KL) cost
scale), Theorem SL (the analytic split-and-merge failure). They are proposals for HQs, not results.

**Protocol mapping.** Statements: THEOREM_LIST §G1–G6 and §2 below. Proofs/sketches: §3. Evidence: §4. What fails: §6.
Escalation: §7. Outside scope: §8. Confidence card: §9.

## 1. Headline

1. **The v1 list has 19 items in six groups (THEOREM_LIST §0), of which 14 are theorems/propositions and 5 are cited
   lemmas or dropped.** All three objectives and the parallel claim are covered in v1, with these honest limits: posterior
   accuracy (objective 1) is covered in the masked regime only for Ẑ-weighted estimates (Theorem H, PROOF SKETCH) and
   the top-store sum (Z𝒯, PROVED), never for two-sided Ẑ; parallel depth is covered on the ideal grid plus the
   deterministic cap T ≤ T_e, not for the as-coded masked stage count (OPEN); selection is covered on exact-Gram LH, not on
   the study's generator.
2. **What is KNOWN—CITE and becomes a cited lemma, not a theorem:** SMC invariance/consistency and unbiased Ẑ (Del Moral et
   al.; T12), Ẑ-weighted island pooling (Whiteley–Lee–Heine; T31(i)), the Markov 95% bound, plain-averaging bias (Vergé),
   greedy-schedule optimality G(i) (Štefankovič–Vempala–Vigoda), the fine-grid length law (Syed et al.), the exp(KL)
   sample size (Chatterjee–Diaconis), the 2E₀δ₁ term (Rossell Prop. 1), the Bayes rules (Barbieri–Berger). The list
   says so at every such item.
3. **The thesis sentence is a theorem in a stated scope (§3): fixed data for "never correctness"; ideal grid + T_e cap
   for "costs depth"; a non-asymptotic island bound with E[W²|𝓒] for "costs particles"; exact-Gram LH for the selection
   half and for the split-and-merge contrast.** Outside that scope the paper may use the wording in §3.3.
4. **Disagreements settled from the sources:** D1 (what the paper may say about rapid mixing: §4.1), D4 (Vergé vs WLH:
   both right, different poolings), D5 (μ⋆: polynomially small on LH at fixed c; ≈ 10⁻¹² on the study designs, scaling with
   the number of invisible truths, not "exponentially small" without saying in what), D6 (T26: standard pattern; its new
   content is the stage-count input; remark, not theorem), D10 (Song–Liang citation: Thm 4/Cor 2 + eq. (19) + Condition 5).
   Left as escalations with a named check: D9 (citation details), the Cérou et al. novelty check of O-PW2 Thm A, the
   Mathews–Schmidler reduction of T38(a), and Song–Liang's supplement (Theorem S) for Theorem SL's FDR variant.
5. **Seven v1 HQs (HQ_PLAN):** VALID, START, SELECT (wave 1, S/S/M); ISLAND, DEPTH (wave 2, M/S); SL, EVID (wave 3, M/S).
   Critical path VALID → ISLAND → EVID. Nine v2 HQs are named so the paper can cite them as future work.
6. **Two corrections to inherited claims found while writing:** (a) the Song–Liang failure on the W1-EXP LH family needs the
   masked hub to be *isolated* in its split (from its partner *and* its own group), because its group members carry the
   marginal signal −ρψβ and Stage 1 then retains the hub (THEOREM_LIST C1(e), checked numerically); LIT-PAR's 5/318 used
   a singleton masked variable (g = 1), where isolation = separation. (b) F-MASKPIP M3 is recorded as XF ERROR in
   THM-INV; the "R ≳ 1/P(crossing)" remark must not cite it (replaced by Cauchy–Schwarz + M2).

## 2. Statements

All statements are in `THEOREM_LIST.md` with hypotheses named. The three NEW-SYNTH ones, in full:

**Lemma KL.** For probability measures π, π₀ on a finite Ω and a state S₀ with δ₁ := 1 − π(S₀):
KL(π‖π₀) ≥ (1 − δ₁)·log(1/π₀(S₀)) − log 2. Hypotheses: none (π₀(S₀) > 0).

**Theorem H (Ẑ-weighted estimates of bounded functionals).** Setting of Theorem V (fixed data; frozen 𝓒; EX-A, EX-S,
CAL; V5; R declared). For h: Ω → [0,1] and ĥ_r island r's measured-round plain average of h, W_r = Ẑ_r/Z:
(a) E[W_r·|ĥ_r − h(S₀)| | 𝓒] ≤ δ₁ (plain average; ≤ 2δ₁ + c_h(ρ̄ + u_π) for the Rao–Blackwellised version with M1's terms);
(b) for ĥ^zw = Σ_r W_r ĥ_r/Σ_r W_r, s ∈ (0,1), t > 0: P(|ĥ^zw − h(S₀)| > t | 𝓒) ≤ exp{−R(1−s)²/(2E[W_1²|𝓒])} + δ₁/(st)
(Maurer), or exp{−2R(1−ε−s)²/M_𝓒(ε)²} + δ₁/(st) with M_𝓒(ε) = inf{M: E[W 1{W>M}] ≤ ε} (Hoeffding on W ∧ M);
(c) joint inclusion: h_A(S) = 1{A ⊆ S} for any A ⊆ [p];
(d) on R1 under T03♯'s hypotheses, if R_n(1−s)²/E[W²|𝓒_n] → ∞ in probability then ĥ^zw → h(S₀) in probability, jointly
with output; (e) fixed data: ĥ^zw → π(h) a.s. as R → ∞ at fixed N (cited).

**Theorem SL (split-and-merge versus v3.1 on LH).** LH exact Gram with c ≥ 1 linked pairs (hubs j_{a_i}, j_{b_i};
θ_{j_{b_i}} = −ψ_iθ_{j_{a_i}}; groups of size g, correlation ρ). Song–Liang's procedure with a uniformly random
equipartition into K_n subsets of size s_n, Stage-1 selection at a fixed PIP threshold q ∈ (0,1) (FDR variant: escalation),
SL's priors. Let E_n = {some j_{b_i} is isolated in its subset from j_{a_i} and from its g − 1 group members}. Then:
(a) P(j_{b_i} isolated) = C(P_n−1−g, s_n−1)/C(P_n−1, s_n−1) ≥ 1 − g(s_n−1)/(P_n−1) for each i, so P(E_n) → 1 if
K_n → ∞ (SL's K_n = O(√P_n)) and P(E_n) is bounded away from 0 at fixed K_n (0.53 at K = 2, g = 1; 0.05 at K = 2, g = 4);
(b) on E_n, cov(x_{j_{b_i}}, y) = 0 and x_{j_{b_i}}′μ = 0 exactly, x_{j_{b_i}} is orthogonal to its subset, so Condition 5
fails exactly, β_{0,j_{b_i}} = 0 at every iteration, π(j_{b_i} ∈ ξ | D_n^s) → 0, j_{b_i} ∉ S̃ w.p. → 1, and SL's output
(prior mass 0 outside S̃) cannot equal S₀: limsup P(SL output = S₀) ≤ 1 − liminf P(E_n);
(c) the exact posterior concentrates on S₀ on the same family (W1-EXP Thm 5(d)/T03♯);
(d) v3.1 on the same family: Theorem V holds for any R; with LS0 P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 (T38 (b1-LH)); without LS0 on the
STAB-LH subfamily (T38 (b2-LH)); Theorem H for PIPs and joint inclusions;
(e) if the split keeps j_{b_i} with its group, β_{0,j_{b_i}} = ψ_iθ_{j_{a_i}}([Σ_bb^{−1}]₁₁ − 1) ≠ 0 and Stage 1 retains it.

## 3. The thesis sentence as a theorem

**Draft sentence.** "In split-and-merge, correlation breaks correctness; in local-to-global SMC, correlation costs only
sequential depth and particles, never correctness."

### 3.1 The formal version v1 proves (Theorem CD, THEOREM_LIST D3)

Fix X (any correlation), y, EX-A, EX-S, CAL, R declared before final randomness.
- **Never correctness** (fixed data): every island's final stage targets π exactly; E[Ẑ_r|𝓒] = Z; Ẑ-weighted pooled
  estimates of any bounded h converge to π(h) as R → ∞ at fixed N, and as N → ∞ (Theorem V: KNOWN—CITE + locked T12/T31(i));
  on every island E[W_r|ĥ_r − h(S₀)| | 𝓒] ≤ δ₁ with no premise on X or on the start (Theorem H(a): PROOF SKETCH). No
  hypothesis on X enters any of these.
- **Costs depth:** the critical path is (I+2)(T+L+4)(p+B+2) score evaluations, free of N, H, R (Prop D: PROVED counting);
  T ≤ T_e deterministically (Theorem G: PROVED); on the ideal exact-frontier grid T* = O(1) (favourable) and
  log₂A₀ + O(1) (masked crossing) with A₀ = log[π₀(S°)/π₀(S₀)] the start's masking depth (STG-F/STG-M: PROVED, XF
  VERIFIED*); A₀ = c log p + (c/2) log n on LH (T27(i) locked). So correlation enters the depth through A₀ only, logarithmically.
- **Costs particles/islands:** the Ẑ-weighted error exceeds t with probability ≤ exp{−R(1−s)²/(2E[W²|𝓒])} + δ₁/(st) (Prop
  P(iii)/Theorem H(b): PROVED/PROOF SKETCH); E[W²|𝓒] ≳ 1/P_𝓒(crossing) (PROOF SKETCH), so the islands needed grow with the
  masking depth through the crossing probability; the equal-weight PIP's bias is set by N (Prop P(i): PROVED).
- **The contrast:** on exact-Gram LH, split-and-merge loses an isolated masked hub w.p. → 1 under K_n → ∞ (Theorem SL:
  COUNTEREXAMPLE + PROOF SKETCH), while v3.1's reported HPM equals S₀ w.p. → 1 − limsup P(U) (T38 (b1-LH): PROVED
  candidate, XF VERIFIED).

### 3.2 Scope, exactly
- "Never correctness" is **fixed data** (any n, any X). It is KNOWN—CITE in its positive clauses; what is ours is the
  hypothesis list and the two negative clauses (pooled product not unbiased; adaptive R breaks it).
- "Costs depth" is proved for the **ideal grid** (STG-M) and as a **deterministic cap** for the coded one; the as-coded
  masked stage law is OPEN (Conjecture P). The per-round factor Θ(p) is part of the depth and must be printed.
- "Costs particles" is a **non-asymptotic island bound with an unbounded constant** E[W²|𝓒]; an upper bound in the
  masked regime is OPEN (v2 HQ-VAR). The paper must say "correctness at a cost in islands, with the cost not bounded above".
- Both halves of the contrast are **n → ∞ on exact-Gram LH**; neither covers the study's dilution designs or LH-iid.
- "Never correctness" does **not** include P(U) → 0: every consistency statement is joint with "output exists".

### 3.3 Wording the paper may use
- Proved form (one sentence): "For any design and fixed data, the final-stage target is the exact posterior and the
  island estimates are unbiased or consistent (Theorem V); correlation enters only the stage count, through the start's
  masking depth A₀ (Theorem STG), and the number of islands needed, through the single-island relative second moment of
  the evidence (Theorem H)."
- Contrast (proved on LH): "A feature-splitting procedure whose correctness condition is a nonzero within-split
  projection coefficient (Song–Liang Cor. 2, eq. (19), Condition 5) loses a cancelling true variable whenever the random
  split isolates it, which under K_n → ∞ happens with probability → 1 (Theorem SL); the local-to-global sampler has no
  such condition."
- Do not print: "methods with guarantees are sequential" (false: ZYVR with parallel neighbour scoring), "faster than
  SaM", "depth = T" without the Θ(p) factor, "first parallel exact BVS", "tempering is needed" (W7-SEP: only "moving off
  the start is needed").

## 4. Disagreements

### 4.1 D1 (API-POS vs LIT-MCMC on rapid mixing): settled as far as the sources allow
- Both are right about different objects. API-POS: no published theorem (YWJ, ZYVR, Zhou–Smith, Chang–Zhou) applies
  to the paper's prior as stated (g = n gives κ_eff ≈ 1 against ZYVR's κ ≥ 18; the cap ⌊n/2⌋ breaks YWJ's D(s₀)); it
  *expects* a YWJ-style proof for our prior to succeed (CONJECTURE). LIT-MCMC: the sufficient condition R > M fails at
  n = 200 and 1,600 on LH and in 12/12 study-like designs by ≥ p^{0.87}, with the binding side the overfitted one;
  this refutes the *applicability of the unimodal-ratio route*, not fast mixing. LIT-VENUE's "R > M since S₀ is the unique
  local mode" is wrong: unimodality gives R > 1, not R > M.
- **What the paper may say:** "No published rapid-mixing theorem covers the paper's prior and cap; the standard
  sufficient condition (a best-neighbour ratio exceeding the neighbourhood size) fails on our designs because the BB(1,p)
  + g = n penalty per extra variable is ≍ p√n against a neighbourhood of size ≍ p (LIT-MCMC Prop. OB, PROOF SKETCH). We
  make no mixing claim in either direction. Our output theorems (Thm 5) do not use mixing: the truth is scored, not
  mixed to." Plus, as evidence not theorem: "On LH the exact posterior is unimodal at p ≤ 20 (API-POS enumeration); the
  masking is a property of the start, not of the posterior."
- **What it may not say:** "covered by YWJ/ZYVR" or "provably not coverable". The honest positioning sentence for Thm 5
  is LIT-MCMC's: "novel for the paper's target and method; under YWJ/ZYVR's priors a corollary of their results on LH".
- **Escalation retained (named check):** whether a YWJ-style theorem for *our* prior is a cheap v2 HQ (HQ-MIX). A
  reader should check API-POS §3's constants against YWJ's proof to decide if the obstruction is only the constants.

### 4.2 D4 (island pooling: Vergé vs Whiteley–Lee–Heine): settled
Vergé et al. 2015 analyse *plain* averaging (bias O(1/N₁), not reduced by islands) — that is exactly Prop P(i) for the
equal-weight PIP. WLH 2016 §5.1 / Dai et al. 2022 (4.8) analyse *Ẑ-weighted* pooling — that is T31(i)/Prop P(ii). Cite
both, each for its pooling. Both reports call T31(i) standard; the list does.

### 4.3 D5 (how small is μ⋆ under a masked start): settled by naming the family
μ⋆ (Mathews–Schmidler) is the minimum over stages of the mode mass of the truth's basin. On LH at fixed c it is
polynomially small, π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (and larger for the basin 𝓡 than for S₀ alone): LIT-SMC/LIT-MCMC are
right there. On the study's dilution designs O-DILUTE measures median π₀(S₀) = 10^{−15.7} (study: ≈ 10⁻¹²), with the
deficit V = Σ_b softplus(−λ_b) growing with the number of invisible truths (≈ 7 of 14): LIT-PAR's "exponentially small"
is right only if "in the number of invisible truths" is said. **Wording:** "μ⋆ is polynomially small in (n, p) on LH at
fixed cancellation depth, and of order 10⁻¹² on the study's designs, where it decays with the number of truths invisible
to their own block; either way the generic SMC bounds are vacuous." Never bare "exponentially small".

### 4.4 D6 (Thm 6 / T26 novelty): settled
LIT-VENUE is right that the *pattern* (SMC consistency/CLT composed with posterior concentration) is standard (Dau–Chopin
2022, Beskos et al. 2016). LIT-SMC is right that no published statement has the budgets (N_n, T_n) indexed by n with a
premise on the method's own adaptive grid. Both reviewers already demoted T26 to the favourable regime (1/2,394 study
fits). **Decision for the list:** T26-ThmA is a remark inside Theorem Z (A2(v)), labelled "standard composition; the
method-specific content is the stage-count input (Theorem G / STG-F) that makes (P1) checkable". Not a headline theorem.

### 4.5 D10 (Song–Liang's correlation condition): settled against the text
Use Theorem 4 / Corollary 2 with eq. (19) and Condition 5 from JRSS-B 77(5):947–972; never "Thm 5" from slides.
Condition 5 (|cov(x_t, y)| > 0) justifies the iterative Stage-1 step and is not part of any formal theorem; Cor 2 gives
sure screening of the projected support s̃ (lower bound); the "only if" ("a true predictor is selected iff β_{0,t} ≠ 0") is
text after Cor 2, not a proved statement — Theorem SL proves the "only if" itself on LH via the orthogonal-null lemma.
SL has **no theorem for the composed procedure** and says its UQ is approximate (SL §7).

### 4.6 Left as escalations (named check)
- **D9** citation clashes (Shin–Bhattacharya–Johnson venue; Le Fay–Chopin–Vihola theorem number; YWJ's cap constant; ZYVR has
  five authors): bibliography pass against primary sources before printing.
- **O-PW2 Thm A vs Cérou–Del Moral–Guyader 2011 Thm 1.4** (KNOWN—CITE or NEW): someone must read CDG Thm 1.4 (HQ-EVID step 1).
- **Whether T38(a) reduces to Mathews–Schmidler 2024 Thm 1** (LIT-PAR TH6): if yes, (a) is a corollary and the paper says so.
- **ADRAFT-ThmA** has only Astra-on-Astra review: cite Del Moral et al. 2006 instead, or get a Claude check.
- **V5** (reversibility and self-adjointness of the round) has no registry row: HQ-VALID writes it.

## 5. Tiering: what v1 closes, states as a limitation, or defers (THM-INV §5 gaps)

| THM-INV §5 gap | v1 | How |
|---|---|---|
| 1. E_π[h] accuracy as n grows, masked regime (joint inclusion, PIPs at p ≫ n) | **closed for Ẑ-weighted estimates, with R_n as a hypothesis**; limitation: R_n not bounded above | Theorem H (A1) + Z𝒯 (A3) |
| 2. Two-sided relative accuracy of Ẑ, masked regime | **limitation** (one-sided + certificate + Z𝒯 two-sided for a different quantity) | Theorem Z (A2); v2 HQ-VAR |
| 3. Parallel work/depth theorem; R vs N | **closed on the ideal grid + T_e cap**; limitation: as-coded masked T_n; Cor V v2 | Theorems D, STG, CD (D1–D3) |
| 4. P(U) → 0 | **limitation** (6/2,400 measured; v3.1 lowers wall-time stops) | R6; v2 HQ-DELIV |
| 5. Masked consistency on non-LH / study generator | **limitation** (LH exact Gram only; LS0 route verified; no-LS0 on the subfamily) | R5; v2 HQ-GEN |
| 6. Finite-n guarantees | **partly**: N200's inequality is exact at every n with a lower bracket; the upper bound on Π(X) is deferred | R4; v2 HQ-FINN |
| 7. Mixing of the φ = 1 round | **deferred**, with the §4.1 wording | v2 HQ-MIX |
| 8. Positive power of diagnostics | **deferred** (only negative results; Biswas–Jacob–Vanetti route named) | v2 HQ-DIAG |
| 9. Calibration behaviour (rebuild loop, S₀ ∈ V, masked T_n) | **deferred** | v2 HQ-STAGES-2 |
| 10. Partition law for adaptive packing | **deferred** (W7-PART Thm B covers g ≤ B < 2g only; CE2) | v2 HQ-GEN |
| 11. Floating point at production size | **limitation** (VAL-FP measured at p ≤ 40; ε scales with R/4) | V1 remark |
| 12. Exactness of the start sampler; V5 reversibility | **closed by writing it down** (routine) | HQ-VALID first step |

v1 covers: objective (1) by Theorems V, H, Z, Z𝒯, PIP-P1; objective (2) by Theorems D, STG, CD and Props W/P; objective
(3) by Theorems 1, 3, 4, 5 and Prop 1; the parallel claim by V2/V3 (bitwise concurrency; R-scaling of the Ẑ-weighted
PIP); the correlation contrast by Theorem SL. **Dropped from the registry for the paper and why:** Prop M / FD-NM (ERROR;
known phenomenon; replaced by SEP + Lemma KL); literal T37/TD and H24 (COUNTEREXAMPLEs; replaced by Theorem A); F2 (GAP,
Lemma 3.4 ERROR); general LH locking (FALSE, A-REV7); DIL-DM(i) (ERROR); WS6e/WS8d and the ORTH-only weight-stability
results (supplement at most); T39 (contingency not needed: (b1-LH) exists); T26 as a headline (remark); the T32(i)
displayed rate (GAP; "polynomial" stands); the "first finite-n" wording (Hou–Wang–Atchadé); any "3/3 designs bitwise"
claim (1/1 + smoke until HQ's runs finish); any claim that cites F-MASKPIP M3 (XF ERROR) or METH-AUDIT §6's measured
table (placeholder in the branch file).

## 6. Proofs or sketches (only for the NEW-SYNTH items; everything else is cited by registry ID)

**Lemma KL.** Data processing for the partition {S₀, Ω∖S₀}: KL(π‖π₀) ≥ kl(1−δ₁ ‖ π₀(S₀)) = (1−δ₁)log((1−δ₁)/π₀(S₀)) +
δ₁ log(δ₁/(1−π₀(S₀))) ≥ (1−δ₁)log(1/π₀(S₀)) + (1−δ₁)log(1−δ₁) + δ₁ log δ₁ ≥ (1−δ₁)log(1/π₀(S₀)) − log 2, since
−δ₁ log(1 − π₀(S₀)) ≥ 0 and the binary entropy is ≤ log 2. ∎ (Numerically checked on 20,000 random/adversarial pairs:
min(KL − bound) = 2.2·10⁻⁶ ≥ 0.) Corollary with T27(i) and CD18 Thms 1.1–1.2: the one-shot sample size exp(KL) is
≥ ½(p^c n^{c/2})^{1−δ₁}e^{O_P(1)}, matching SEP-B's Q*.

**Theorem H(a), plain average.** ĥ_r = N⁻¹Σ_i h(S_i) over the measured population; |ĥ_r − h(S₀)| ≤ N⁻¹Σ_i 1{S_i ≠ S₀}
since h ∈ [0,1]. The island identity for the bounded function 1{S ≠ S₀} gives E[W_r·N⁻¹Σ_i 1{S_i ≠ S₀} | 𝓒] = π(S ≠ S₀) = δ₁.
**Crux:** that identity for the measured-round average (W2-T26 Lemma 3 / T15 at a terminal-round prefix) must be checked
for general h; for h = 1{j ∈ S} it is Prop 2's. (b) is Prop P(iii) verbatim. (d) composes with T03♯ (δ₁ → 0 in P₀-prob.)
and the R_n hypothesis. ∎ (sketch)

**Theorem SL.** (a) For a uniformly random equipartition, the subset of item j is a uniformly random (s−1)-subset of the
other P−1 items; the sharing probability with a given item is (s−1)/(P−1), and P(isolated from g given items) =
C(P−1−g, s−1)/C(P−1, s−1) (hypergeometric; checked exactly and by Monte Carlo). (b) On E_n, in j_b's subset s every other
column is uncorrelated with x_{j_b} (its only nonzero correlations are ρ with its group and ψ with j_a, all absent), and
x_{j_b}′μ = (n−1)[θ_{j_b} + ψθ_{j_a}] = 0 under the exact Gram. So x_{j_b}′y = x_{j_b}′ε and x_{j_b} ⟂ X_{s∖j_b}: under SL's
Gaussian prior with known σ² the model posterior factorises over j_b with inclusion odds λ_s/(1−λ_s)·BF_null where
BF_null = (1 + nv)^{−1/2}exp{½·(x′ε)²/(σ²‖x‖²)·nv/(1+nv)} = O_P(n^{−1/2}); with σ² ~ IG the same bound holds up to a factor
bounded in probability (one-page Laplace/ratio argument: **the one proof obligation of HQ-SL**). Hence PIP(j_b | D_s) → 0,
so j_b fails any fixed threshold w.p. → 1 and is not selected at any iteration (the iterative step changes nothing for an
orthogonal null column); j_b ∉ S̃, and SL's Stage-2 prior puts mass 0 on models containing j_b. (c) W1-EXP Thm 5(d).
(d) T38 (b1-LH), (b2-LH), Theorem V, Theorem H. (e) direct computation: β₀ = Σ_bb^{−1}cov(x_group, μ) with cov = (0, −ρψβ, …),
hub entry ψβ([Σ_bb^{−1}]₁₁ − 1) = ψβρ²(g−1)/((1−ρ)(1+(g−1)ρ)) > 0 for g ≥ 2 (checked). ∎ (sketch)

## 7. Evidence
`scripts/check_lemmas.py` (output in `scripts/check_lemmas.out`): (1) Lemma KL on 20,000 cases, PASS; (2) isolation
probabilities exact vs Monte Carlo for (P, K, g) ∈ {(16,2,1): 0.533, (16,2,4): 0.051, (64,8,4): 0.617, (1024,32,9): 0.757},
PASS; (3) hub projection coefficient 0 iff isolated, cov(x_hub, μ) = 0 always, PASS. The inherited numerical seed for
Theorem SL is LIT-PAR note 09 (5/318 vs 20/20 at β = 1; 0/318 at β = 0.6), on a g = 1 design. No other computation.

## 8. What fails and why
- **"Song–Liang loses the masked hub whenever the split separates the pair"** (LIT-PAR's sketch) fails on the W1-EXP LH
  family with g ≥ 2: the hub's group members carry the marginal signal −ρψβ, so with its group present the hub has a
  nonzero projection coefficient and Stage 1 retains it. The correct event is isolation (THEOREM_LIST C1(a)); at K = 2,
  g = 4 its probability is 0.05, so at fixed small K the failure is rare though nonzero; "→ 1" needs K_n → ∞.
- **A two-sided masked Ẑ theorem** cannot be assembled from existing pieces: E1/E2 are one-sided, O-PW2 Thm C is vacuous
  without an L² mixing input, and V11 is a conjecture. Replaced in v1 by Z𝒯 (different reported quantity) and the certificate.
- **"R → ∞ fixes everything"** fails as an efficiency claim: E[W²|𝓒] is not bounded above; the paper must print the
  lower bound ≳ 1/P(crossing).
- **Using F-MASKPIP M3** for that lower bound fails (XF ERROR); Cauchy–Schwarz + M2 is used instead.
- **The depth claim without the Θ(p) factor** fails (LIT-PAR §3.3, METH-AUDIT Prop D); the honest statement carries m = p + B + 2.
- **Citing METH-AUDIT §6's measured table** fails: in the branch file it is a placeholder ("[filled in after the runs]");
  HQ-DEPTH must fill it or drop every measured sentence.

## 9. Needs escalation
1. **Theorem H's island identity for the measured-round average of a general bounded h** (crux of A1): a referee-level
   check against locked T12/T15 and W2-T26 Lemma 3 before HQ-ISLAND builds on it.
2. **Theorem SL's PIP → 0 step under SL's IG prior and FDR rule**; obtain SL's supplement (Theorem S) if the FDR variant is
   wanted; decide the Stage-1 rule in the theorem.
3. **The Thm 5 headline decision** (LS0 route (b1-LH) vs no-LS0 (b2-LH) subfamily) and the output convention: HQ/Felipe.
4. **D1 wording** (§4.1) needs one independent reader; **D9** needs a bibliography pass; CDG 2011 Thm 1.4 and
   Mathews–Schmidler Thm 1 reductions need reading.
5. **METH-AUDIT §6** must be filled from the actual replay logs before any measured parallel claim is printed.
6. **Prop W-cal** bitwise replay (not executed) and the independent code check of Prop W's two facts.

## 10. Outside scope
- METH-AUDIT §9's spec/code gap (the Ẑ-weighted PIP is not computed by `v3_run.R`) is now layer part (e); the study's
  reported "secondary PIP", if any, must come from a post hoc script — check before citing.
- API-AUDIT's `fit$log_Z` hazard on stopped fits (layer part (g)) has not been applied in code as far as these sources say.
- The 6 `resource_limit` fits are the cheapest way to remove the P(U) caveat (re-run with concurrent islands on NOTS).
- LIT-PAR's recommendation to check ZYVR Condition 1 on S1–S6 for the paper's prior (a strong baseline if it holds).

## 11. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| G1 Validity (Theorem V, Props W/P) | fixed-data exactness for any declared R; bitwise concurrency; Ẑ-weighted PIP consistent in R | high | high (cite + candidates done) | V5 lemma unwritten; W-cal replay | no |
| G2 Theorem H (bounded h, joint inclusion) | islandwise Ẑ-weighted error ≤ δ₁ (+ RB terms); pooled bound with E[W²]; n → ∞ with R_n hypothesis | high for (a)(b)(c)(e); medium for the usefulness of (d) | high for (a)–(c),(e); low for an E[W²] upper bound | measured-round identity for general h; E[W²\|𝓒] in the masked regime | no |
| G2 Theorem Z / Z𝒯 | one-sided masked Ẑ + certificate; two-sided Z𝒯 when S₀ ∈ 𝒯 | high | high (done, candidates) | CDG novelty check; V11 for two-sided Ẑ (v2) | no |
| G3 Theorems D/STG/CD | depth (I+2)(T+L+4)m free of N,H,R; T ≤ T_e; T* = log₂A₀ + O(1) ideal grid | high (counting; ideal grid) | high as stated; low–medium for the as-coded masked law | Conjecture P; Θ(p) per round | no (C6 streams are law-preserving) |
| G4 Thm 2 / SEP / Lemma KL | masking law; Q* = p^c n^{c/2}; exp(KL) ≥ ½Q*^{1−δ₁} | high | high | none (Lemma KL elementary) | no |
| G5 Theorem SL | SaM loses an isolated masked hub w.p. → 1 under K_n → ∞; v3.1 recovers S₀ | high for the mechanism; medium for the exact SL rule (FDR, IG prior) | medium–high (one page of proof + re-run) | orthogonal-null PIP → 0 under SL's prior; FDR threshold | no |
| G6 Thm 5 (T38) for v3.1 | (b1-LH) with LS0; (b2-LH) subfamily without LS0 | high on LH; low beyond | high (done, XF VERIFIED) for LH; low for the study generator | partition law; DELIV; LH-iid GAP | LS0 is already in v3.1 |
| Thesis sentence (Theorem CD) | as §3.1, in the scope of §3.2 | high within scope | high within scope; the full-strength version (as-coded depth law + bounded E[W²]) low–medium | A1 identity; Conjecture P; E[W²] | no |

# THM-SYNTH — THEOREM_LIST: the final theorem list for paper 1 (v3.1)

Run THM-SYNTH (Opus 5.5), branch `theory/THM-SYNTH`, 2026-11-03. **No new proofs.** Every status word is copied from
its source and never upgraded; "candidate" means AI-proved and not adopted. Where I propose a *new* statement (marked
**NEW-SYNTH**), its status is what I could establish while writing it (PROOF SKETCH at most), and it is a proposal for
an HQ, not a result. Registry IDs are those of `T38-RECORD · REGISTRY_v2.md`; paper labels in [ ] follow its §F.

Method: **v3.1** = v3 unchanged as a statistical method + the parallel execution layer of METH-AUDIT §5 (a)–(e), **with
LS0** (task file, fixed input). "v3 as run" = the same without LS0 (the 2,400 study fits).

Tier: **v1** = Biometrika paper, provable within the campaign with a credible route now; **v2** = later.
Novelty words: **NEW** (no precedent found), **NEW-COMP** (components known, composition and the BVS constants new),
**KNOWN—CITE** (textbook or published: becomes a *cited lemma*, not a theorem), **MODEST** (modest extension).

---

## 0. Summary table

| # | Paper item | Group | One-line guarantee | Status (verbatim, source) | Novelty | Tier | Lean |
|---|---|---|---|---|---|---|---|
| V1 | Thm V (validity of v3.1 under parallel execution) | G1 | For any R fixed before final randomness and any data, each island's Ẑ_r is unbiased, the islandwise product identity holds, 0.05Ẑ is a 95% lower bound, and Ẑ-weighted pooled estimates are consistent as R → ∞ at fixed N and as N → ∞ | T12, T31(i) PROVED-LOCKED; Prop P(ii),(v) PROVED (METH-AUDIT, candidate); ADRAFT-ThmA PROVED (Astra only) | KNOWN—CITE (Del Moral et al. 2006; Whiteley–Lee–Heine 2016 §5.1; Dai et al. 2022 (4.8)); method-specific hypotheses ours | v1 (cited lemma + Prop.) | T12Core partial (hstep hypothesis); island identity feasible under abstract resample–move |
| V2 | Prop W / W-cal / Lemma S (worker equivalence, bitwise) | G1 | Concurrent islands, diagnostic islands and scans reproduce the serial run bit for bit; the study's 2,394 fits are v3.1 fits | Lemma S, Prop W PROVED (code reading; 1/1 design + smoke executed); W-cal PROVED (code reading only) | engineering fact | v1 (supplement) | Lemma S: yes (finite order-independence of top-c stores) |
| V3 | Prop P (pooling rules; R fixed in advance) | G1 | Equal-weight PIP keeps the single-island bias; Ẑ-weighted PIP is consistent in R with a regime-free non-asymptotic bound; adaptive R breaks unbiasedness | PROVED (candidate, elementary; (iii) uses F-MASKPIP M1, XF VERIFIED A-REV9) | (i),(ii) KNOWN—CITE (Vergé et al. 2015; WLH 2016); (iii),(iv),(v) ours, elementary | v1 | (iv) identity: yes; (iii) finite part: yes; Maurer cited |
| V4 | Lemma RO + CEX-guard (run/output split) | G1 | A stopped fit is no output; path-dependent stopping would bias Ẑ | Lemma RO PROVED, XF VERIFIED; CEX-guard COUNTEREXAMPLE | elementary | v1 (supplement) | yes (finite) |
| A1 | Thm H (Ẑ-weighted estimates of bounded functionals; joint inclusion) **NEW-SYNTH** | G2 | For any bounded h, the Ẑ-weighted pooled estimate is within O(δ₁‖h‖) of h(S₀) in Ẑ-weighted mean on every island and every regime; with T03♯ and R_n ≫ M_𝓒 it converges to the truth as n → ∞ | PROOF SKETCH (this run; it is M1 + Prop P(iii) with h in place of the PIP) | NEW-COMP (M1 mechanism ours; SLLN part KNOWN—CITE) | v1 | finite inequality: yes |
| A2 | Thm Z (evidence: what Ẑ can and cannot do) | G2 | E Ẑ = Z; exact variance identity; masked regime: Ẑ errs only downward, by the log-odds overshoot of a late crossing; a run certificate Ẑ < Z_𝒯 detects it; favourable regime: Ẑ/Z → 1 under (P1) | T12 PROVED-LOCKED; O-PW2 ThmA PROVED, XF VERIFIED; MASKZPIP E1/E2, C1 PROVED (candidate); T26-ThmA PROVED, XF VERIFIED*; Thm 6 overall CONJECTURE | E1/E2/C1 NEW; ThmA "same kind as Cérou et al. 2011 Thm 1.4" (unchecked); T26 standard pattern | v1 (i)–(iv); two-sided masked Ẑ **v2** | identities (ii),(iv): yes |
| A3 | Thm Z𝒯 (top-store evidence and PIPs) | G2 | 1 − δ₁ ≤ Z_𝒯/Z ≤ 1 and \|PIP^𝒯_j − PIP_j\| ≤ δ₁ whenever S₀ ∈ 𝒯; two-sided and deterministic | MASKZPIP P3 PROVED (candidate, deterministic) | NEW (reported-quantity trick), elementary | v1 | yes (finite) |
| A4 | Thm PIP (equal-weight PIP accuracy) | G2 | Bias ≤ TV of the delivered population; after locking ≤ δ₁; masked consistency reduces to population delivery + repair (Theorem R) | MASKZPIP P1 PROVED; P2 PROVED (composition, LH fixed p); F-MASKPIP Thm R PROVED as composition, CONDITIONAL on DELIV-POP (OPEN) | NEW-COMP | P1 v1; Thm R **v2** (DELIV-POP OPEN) | P1: yes |
| D1 | Thm D (work, depth, width of v3.1) | G3 | Depth (I+2)(T+L+4)(p+B+2) score evaluations, free of N, H, R with particle-parallel islands; work O(N·m·(ℓ+2)·T_e); same order in p as Song–Liang §6 at α = 1 up to logs | Prop D PROVED (counting); T32(i) PROVED (rate GAP; polynomial stands) | accounting; cost-model style KNOWN (TCS work/depth) | v1 | counting: yes |
| D2 | Thm STG (stage laws) | G3 | Greedy grid is optimal and ≤ T_e; T* = O(1) favourable; T* = log₂A₀ + O(1) for a masked crossing (A₀ = start masking depth); √c·T* → L (fine grid) | Theorem G PROVED (deterministic, as coded); STG-F PROVED; STG-M PROVED (ideal two-state grid), XF VERIFIED*; families PROOF SKETCH; as-coded masked T_n: Conjecture P OPEN | G(i) KNOWN—CITE (Štefankovič–Vempala–Vigoda 2009); item 4 KNOWN—CITE (Syed et al. 2024 Thm 3); STG-M NEW | v1 (ideal grid + T_e cap); as-coded masked law **v2** | Lemma RS identity and Theorem G: yes (finite convexity/greedy) |
| D3 | Thm CD (the thesis sentence) | G3 | Correlation changes the target of no stage and no identity (never correctness); it enters only through depth (T via A₀) and islands/particles (R ≍ E[W²\|𝓒]) | assembled from V1, V3(iii), D1, D2; see §3 below | NEW-COMP | v1 in the scope stated in §3 | — |
| D4 | Cor V (R vs N trade-off) | G3 | Same total particles ⇒ same leading-order Var(Ẑ_pooled); equal-weight PIP bias is set by N, Ẑ-weighted by R | PROOF SKETCH (METH-AUDIT) | partly KNOWN (WLH 1/R identity) | **v2** (v1 states the two PROVED halves from V3) | — |
| S1 | Thm 2 (the start: deterministic mass, favourable rate, masking law, dilution) | G4 | π₀ carries mass ≥ (1−q)^{s+1}/(1+e)^s on a reference; favourable 1 − π₀(S₀) → 0 at a rate; masked π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}; −log π₀(S₀) = V + C − log A exactly | T22(i)(ii)(iv) PROVED-LOCKED; T22(iii) PROVED-LOCKED CONDITIONAL; T27(i) PROVED-LOCKED CONDITIONAL, Thm3/4-EXP XF VERIFIED; DIL-E/E1/R/N PROVED, XF VERIFIED | NEW ("strongest novelty claim", LIT-STAT); block start KNOWN (Papaspiliopoulos–Rossell 2017) | v1 | DIL identity, T22(i): yes |
| S2 | Thm SEP + Lemma KL (why the merge alone fails; one-shot cost scale) | G4 | iid π₀ draws need Q* = p^c n^{c/2}; one-shot importance correction has 1 + χ² ≥ Q*e^{O_P(1)}; KL(π‖π₀) ≥ (1−δ₁)log(1/π₀(S₀)) − log 2, so the Chatterjee–Diaconis sample size exp(KL) is ≥ Q*^{1−δ₁}e^{O_P(1)}/2 | SEP-A/B PROVED, XF VERIFIED; Lemma KL PROOF SKETCH **NEW-SYNTH** (elementary) | SEP NEW; exp(KL) scale KNOWN—CITE (Chatterjee–Diaconis 2018 Thm 1.1/1.2) | v1 | Lemma KL: yes (log-sum inequality) |
| S3 | Prop M (naive merge fails) | G4 | — | SHARE-M(b) ERROR; FD-NM ERROR, repair pending | KNOWN phenomenon (LIT-STAT) | **dropped**; replaced by S2 + Prop M-LH as a remark | — |
| C1 | Thm SL (correlation robustness vs split-and-merge) **NEW-SYNTH** | G5 | On LH with c linked pairs, Song–Liang's procedure loses every masked hub w.p. → 1 over random splits (Condition 5 fails exactly; eq. (19) gives β₀ = 0 on the hub's group), while v3.1 targets π exactly and its reported HPM equals S₀ w.p. → 1 − limsup P(U) | COUNTEREXAMPLE (numerical, LIT-PAR G4) + PROOF SKETCH (this run; crux in §C1) | NEW (no analytic SaM failure published) | v1 (exact-Gram LH); LH-iid **v2** | split probability and the eq. (19) zero identity: yes; selection consistency cited |
| R1 | Thm 1 (posterior consistency, T03♯) | G6 | Posterior mass off S₀ is O_P(√(log n/n)); HPM, MPM of π equal S₀ w.p. → 1; large signals get PIP → 1 without beta-min | T01–T03 PROVED-LOCKED; T03♯ PROVED, SF + XF VERIFIED | MODEST (Rossell 2022; Moreno–Girón–Casella 2015); T03♯(3) KNOWN—CITE (Rossell Prop 1) | v1 (main text, asymptotic; disclose n ≳ 2·10⁶) | T02(i♯) tail: partly; rest cited |
| R2 | Prop 1 (Bayes rules; size-prior ceiling) | G6 | HPM = 0–1 Bayes rule; MPM = Hamming; no size-only prior repairs a same-size swap | PROVED-LOCKED; XF VERIFIED* | FOLKLORE (Barbieri–Berger 2004) except (iii) ceiling | v1 remark | sorry-free (T07Bayes.lean) |
| R3 | Thm 3 (exact greedy repair, Theorem A; LS-score) | G6 | From any centre in Lat(S°) under TD′, the production local search reaches and scores S₀ in Φ moves; LS0 scores S₀ within max{Φ(S°)−1,0} moves | Theorem A PROVED, XF VERIFIED*; LS-score PROVED, XF VERIFIED (A-REV8) | "unsurprising given YWJ/ZYVR"; deterministic exact finite-n form is the difference | v1 | sorry-free (T37Greedy/Lattice.lean); fidelity GREEN (Astra r2) |
| R4 | Thm 4 (composition, every n: T21(C1), T38(0), N200) | G6 | P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n; P(U ∪ {Ŝ ≠ S₀}) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮), with a matching lower bound | T21(C1) PROVED-LOCKED; T38(0) PROVED, XF VERIFIED; N200 PROVED (author only); Lemma RO XF VERIFIED | elementary; the 2E₀δ₁ term KNOWN—CITE; Hou–Wang–Atchadé threatens "first finite-n" | v1 | sorry-free (T21HPM.lean); N200 Lemma 1: yes |
| R5 | Thm 5 (two-regime consistency of the reported HPM, T38) | G6 | D_n → 0: favourable (iid draws); masked with LS0 on LH (b1-LH); masked without LS0 on A-REV7's LH subfamily (b2-LH); polynomial cost | (0) PROVED XF VERIFIED; (a) PROVED-UNDER (F); (b1) PROVED-UNDER (M1)–(M3) XF VERIFIED; (b1-LH) PROVED (candidate) XF VERIFIED; (b2-LH) PROVED-UNDER STAB-LH XF VERIFIED (conditional); (b1-LH-iid) XF GAP; (c) PROVED-UNDER T32(i) | NEW for the paper's target and method; "a corollary of YWJ/ZYVR under *their* prior" (LIT-MCMC) | v1: (0),(a),(b1-LH),(b2-LH subfamily),(c); **v2**: LH-iid, study generator, general DELIV | composition sorry-free; LS-score and Lat moves: feasible |
| R6 | Delivery P(U) → 0 | G6 | — | NONE (THM-INV §5.4) | — | **limitation** in v1 (report 6/2,400; v3.1 lowers wall-time stops, Prop W) | — |
| R7 | Finite-n upper bound on Π(X) | G6 | — | OPEN (API-N200) | — | **v2** | — |

Cited lemmas (not theorems), named as such in the paper: Del Moral–Doucet–Jasra 2006 (SMC invariance/consistency),
Whiteley–Lee–Heine 2016 §5.1 and Dai–Heng–Jacob–Whiteley 2022 (4.8) (Ẑ-weighted pooling), Grosse–Ghahramani–Adams 2015
(Markov lower bound), Vergé et al. 2015 (plain averaging keeps the O(1/N) bias), Štefankovič–Vempala–Vigoda 2009
(greedy-schedule optimality, G(i)), Syed et al. 2024 Thm 3 (fine-grid length law), Chatterjee–Diaconis 2018 Thms 1.1–1.2
(exp(KL) sample size), Rossell 2022 Prop. 1 (the 2E₀δ₁ term), Barbieri–Berger 2004 Thm 1 (MPM), Maurer 2003 (lower tail).

---

## G1. Validity under parallel execution

### V1. Theorem V (fixed-data validity of v3.1 for any island count)

**(i) Statement.** Fix data (X, y), a seed-independent calibration 𝓒 (grid 0 = φ₀ < … < φ_T = 1, L, N = N_e, V,
tier) produced on streams 0–9 (CAL), and an island count R and stacking schedule declared before any final-run
randomness. Assume EX-A and EX-S. Islands r = 1, …, R run N iid π₀ draws through the frozen bridge with multinomial
resampling and the q_t-invariant round kernels K_t (reversibility of each elementary move and self-adjointness of the
random-order round: METHODOLOGY_v3 §6.5, V5). Let W_r := Ẑ_r/Z and let ĥ_r be island r's measured-round estimate of a
bounded h: Ω → ℝ (for h = 1{j ∈ S} the Rao–Blackwellised PIP̂_rj). Then, conditionally on 𝓒:
(a) E[W_r] = 1 and E[W_r ĥ_r] = π(h) for every N ≥ 1 and every r (islandwise identities);
(b) E[Ẑ] = Z for Ẑ = R⁻¹Σ_r Ẑ_r, and P(0.05·Ẑ > Z) ≤ 0.05;
(c) for fixed N, Σ_r Ẑ_r ĥ_r / Σ_r Ẑ_r → π(h) a.s. as R → ∞; for fixed R, each ĥ_r → π(h) in probability as N → ∞;
(d) the pooled product Ẑ·(R⁻¹Σ_r ĥ_r) is *not* unbiased: its bias is −(1 − 1/R)Cov(Ẑ_1, ĥ_1 | 𝓒).
Hypotheses named: EX-A, EX-S, CAL, V5 (kernel invariance), R fixed in advance (Prop P(v)).

**(ii) Guarantee, plainly.** Whatever the correlation in X, the final stage targets π exactly and the island
estimates are unbiased or consistent; running more islands in parallel never changes this. A referee needs it because
it is the "never correctness" half of the thesis; the paper needs the *hypotheses* (frozen 𝓒, R declared) to be
visible, because the CEX-guard and Prop P(v) show how easily they are broken.

**(iii) Status and components.** (a),(b): T12 and T31(i) PROVED-LOCKED (wave 1); Prop 2(a,b,d,e) PROVED-LOCKED; XF
A-REV4 GAP only on the "output Markov" wording. (c): ADRAFT-ThmA PROVED (Astra author, Astra check only); Prop P(ii)
PROVED (candidate). (d): Prop 2(c) PROVED-LOCKED, generalised to R by Prop P(iv) PROVED (candidate). V5 (reversibility
and self-adjointness) holds by construction, consultant-checked, but has **no registry row** (THM-INV §5.12). Components:
THM-INV §1 rows 6 (V), 8, 9, 10 (V).

**(iv) Novelty.** KNOWN—CITE. (a)–(c) are Del Moral et al. 2006, Whiteley–Lee–Heine 2016 §5.1, Dai et al. 2022 (4.8),
Grosse et al. 2015 (Markov). LIT-SMC: only the negative items, (d) and E[Ẑ | completed] ≠ Z, are "genuinely
non-standard". The paper presents V1 as a *Proposition with cited proof*, whose only method-specific content is the
hypothesis list (frozen 𝓒; the round kernel is q_t-invariant; R declared) and the two negative clauses.

**(v) Difficulty and route.** S. Restate T12/T31(i) in the R-island form; write the one-page V5 lemma (each
elementary kernel is γ_φ-reversible; a uniformly random order of reversible kernels is self-adjoint) so that the paper
does not rely on an unrecorded fact; cite the rest.

**(vi) Lean.** T12Core.lean proves `unbiased_of_step` with the resample–move recursion as a hypothesis (`hstep`). The
island identities (a) and the finite identity (d) are certifiable on an abstract finite probability space once `hstep`
is discharged for the multinomial resample + invariant kernel step (L-LEAN `T12_PLAN.md`); the a.s. limits (c) rest on
the cited SLLN and SMC theory and should stay cited.

**(vii) Depends on.** Nothing. Everything else in G2–G3 depends on it.

### V2. Proposition W, Proposition W-cal, Lemma S (worker equivalence)

**(i) Statement.** Lemma S: a bounded store of capacity c under a strict total order returns top_c(M) regardless of
the offer order, and top_c(M) = top_c(∪_r top_c(M_r)) for any partition. Prop W: with fixed data, seed and 𝓒, running
the R final islands in separate workers (own cache, own ledger, stream σ_r = 9 + r) and merging by Lemma S gives
**bitwise** the serial run's Ẑ_r, PIP̂_r, per-stage ESS, HPM, stores, local-search path, pooled Ẑ, both PIPs and flags
E1–E3 (only counters and time stamps differ). Prop W-cal: the same for the calibration's 4 diagnostic islands with
persistent per-worker stream state. Cor W-R: stacking R′ > 4 islands on fresh streams leaves islands 1–4 bitwise
unchanged and makes the pre-local-search HPM ⪰ the R = 4 one.

**(ii) Plainly.** The parallel layer changes no number: the 2,394 completed study fits *are* v3.1 fits at R′ = 4. A
referee needs it to accept that the study validates the shipped method.

**(iii) Status.** Lemma S PROVED; Prop W PROVED (code reading) with the executed check PASSED on the smoke problem and
on **1/1 completed design** (p0500_S1_r001; the task file says treat METH-AUDIT's "3/3" as 1/1 + smoke); W-cal PROVED by
code reading, **not executed**. Components: THM-INV row 8 (V), row 14.

**(iv) Novelty.** None (engineering). Supplement material.

**(v) Difficulty.** S. Needs the independent code check METH-AUDIT §8.1 asks for (scorer statelessness; ledger
write-only inside an island) and the W-cal bitwise replay.

**(vi) Lean.** Lemma S is pure finite combinatorics (sets, strict orders, top-c): certifiable. Prop W is a statement
about code and stays a code-audit fact.

**(vii) Depends on.** IND-T (stream separation; PROVED, XF VERIFIED* A-REV1).

### V3. Proposition P (pooling rules; R fixed in advance)

**(i) Statement.** Setting of V1. (i) PIP^eq_j := R⁻¹Σ_r PIP̂_rj → E[PIP̂_1j | 𝓒] a.s. as R → ∞: the equal-weight PIP
keeps the single-island bias b_j(N). (ii) PIP^zw_j := Σ_r W_r PIP̂_rj/Σ_r W_r → PIP_j a.s. (iii) For e_r ∈ [0,1] any
island error, ε := E[W_r e_r | 𝓒], s ∈ (0,1), t > 0:
P(max_j |PIP^zw_j − 1{j∈S₀}| > t | 𝓒) ≤ exp{−R(1−s)²/(2E[W_1² | 𝓒])} + ε/(st), and with F-MASKPIP M1, ε ≤ δ₁ + ρ̄ + u_π in
every regime and for every frozen grid. (iv) E[Ẑ·PIP^eq_j | 𝓒] − Z·PIP_j = −(1 − 1/R)Cov(Ẑ_1, PIP̂_1j | 𝓒). (v) Pooled
Ẑ is conditionally unbiased for every R declared before final randomness; an adaptive R ("add islands until the SE is
small") can break it (same mechanism as CEX-guard).

**(ii) Plainly.** More islands fix the Ẑ-weighted PIP, never the equal-weight one; the price is R ≳ 2E[W²]log(1/η)
islands; R must be declared. This is the precise sense of "correlation costs islands, never correctness" (METH-AUDIT
§1.3), and the reason the paper reports the Ẑ-weighted PIP next to the equal-weight one (layer part (e)).

**(iii) Status.** PROVED (candidate, elementary; METH-AUDIT PROOFS.md). Inputs: island identities (V1(a)); M1 PROVED
(Fable), XF VERIFIED (A-REV9); Maurer 2003. Honest caveat (METH-AUDIT): E[W²|𝓒] can be exponentially large in the masked
regime, so (iii) is a correctness statement, not an efficiency statement, until E[W²] is bounded (A2/v2).

**(iv) Novelty.** (i) is Vergé et al. 2015's observation; (ii) is WLH/Dai (KNOWN—CITE). (iii)–(v) are ours but
elementary. Settles THM-INV D4: cite Vergé for (i), WLH for (ii); both are right about different poolings.

**(v) Difficulty.** S (done). Route for the paper: fold (iii) into Thm H (A1) with general h.

**(vi) Lean.** (iv) is a finite algebraic identity: yes. (iii)'s deterministic step (convex combination of deviations
≤ the same combination of maxima; Markov) is finite: yes. Maurer's inequality: cite.

**(vii) Depends on.** V1; M1 (F-MASKPIP).

### V4. Lemma RO, GUARD (G1)/(G2), CEX-guard

**(i) Statement.** Lemma RO: on 𝒢ᶜ = {not resource_limit} the statistical outputs, scored sets, decisions and status
equal those of the potential uninterrupted run R̄ (GUARD (G1): the guard reads only the clock, consumes no random number,
changes no setting). CEX-guard: a stopping rule that depends on the path (e.g. stop when Ẑ looks large) makes
E[Ẑ | output] ≠ Z. Prop P(v) is the island-count analogue.

**(ii) Plainly.** "A stopped fit is no output" is what makes every identity conditional on nothing but 𝓒. Under v3.1
the guard must check the run's wall clock and a stop in any worker must stop the run before output (METH-AUDIT §3).

**(iii) Status.** Lemma RO PROVED, XF VERIFIED (A-REV6, conditional implication); GUARD implementation fact HOLDS, literal
"every output equals" wording ERROR (A-REV8: statistical scope only); CEX-guard COUNTEREXAMPLE (W2-BOOK).

**(iv)–(vii).** Elementary; supplement; Lean: the finite coupling statement is certifiable; depends on nothing.

**Group G1 remark (the "R fixed in advance" rule, for the paper).** State once: "R, the stacking schedule, N_e and 𝓒
are fixed before the final streams are read. Nothing in this paper conditions on observed completion or on observed
estimates." Cite CEX-guard and Prop P(v) as the two counterexamples that motivate it.

---

## G2. Posterior accuracy (objective 1; proposal §13.1)

### A1. Theorem H (Ẑ-weighted estimates of bounded functionals, including joint inclusion) — NEW-SYNTH

**(i) Statement (proposed).** Setting of V1. Let h: Ω → [0, 1] (any bounded h after an affine rescaling), and let ĥ_r be
island r's estimate of π(h) built from the measured rounds (the plain population average, or the Rao–Blackwellised
version when h is a product of inclusion indicators). Write δ₁ = 1 − π(S₀), ρ̄ and u_π as in 00_COMMON §2.
(a) *Islandwise, every regime, every frozen grid:* E[W_r·|ĥ_r − h(S₀)| | 𝓒] ≤ 2δ₁ + c_h(ρ̄ + u_π), where c_h = 0 for
the plain average and c_h ≤ 1 for the RB version (the RB-specific terms are those of M1).
(b) *Pooled, non-asymptotic:* for ĥ^zw := Σ_r W_r ĥ_r/Σ_r W_r, s ∈ (0,1), t > 0,
P(|ĥ^zw − h(S₀)| > t | 𝓒) ≤ exp{−R(1−s)²/(2E[W_1²|𝓒])} + (2δ₁ + c_h(ρ̄+u_π))/(st).
A second-moment-free version replaces E[W²] by the truncation level M_𝓒(ε) := inf{M : E[W 1{W > M}] ≤ ε} and Maurer by
Hoeffding on W ∧ M: P(W̄_R ≤ s) ≤ exp{−2R(1 − ε − s)²/M²}.
(c) *Joint inclusion:* for A ⊆ [p], h_A(S) = 1{A ⊆ S}; (a)–(b) give the joint inclusion probabilities, with
h_A(S₀) = 1{A ⊆ S₀}.
(d) *n → ∞ (R1, T03♯ hypotheses):* with δ₁ → 0 in P₀-probability and R_n such that R_n(1−s)²/E[W²|𝓒_n] → ∞ in
probability, ĥ^zw → h(S₀) in probability, jointly with "output exists". Since π(h) → h(S₀) under T03♯, this is
proposal §13.1's "the estimate of E_π[h] converges to the truth".
(e) *Fixed data:* ĥ^zw → π(h) a.s. as R → ∞ at fixed N (V1(c); cited).

**(ii) Plainly.** Any posterior summary the method reports (PIPs, joint inclusions, model-size probabilities, any
bounded functional) is right on the islands that carry evidence weight, in every regime, and pooling enough islands
by Ẑ makes it right. Objective (1) and THM-INV gap §5.1 have **no** theorem today; this is the cheapest one that
covers them, and it is regime-free. The referee's question "what does R buy you" is answered by (b).

**(iii) Status.** PROOF SKETCH (this run). The proof is M1's with h in place of 1{j ∈ S}: for the plain average,
|ĥ_r − h(S₀)| ≤ (fraction of measured particles off S₀) because |h(S) − h(S₀)| ≤ 1 and the average is over particles,
so E[W_r |ĥ_r − h(S₀)|] ≤ E[W_r · frac_off_r] = π(S ≠ S₀) = δ₁ by the island identity for the indicator 1{S ≠ S₀}
(the factor 2 covers the rescaling of a general bounded h to [0,1]). For the RB version the measured-round drift terms
are M1's. (b) is Prop P(iii) verbatim with e_r = |ĥ_r − h(S₀)|. (c) is a special case. (d) composes with T03♯ as M2 /
Prop P do. **Crux not verified:** the island identity E[W_r ĥ_r] = π(h) for the *measured-round average* (T12(i.b)-type,
W2-T26 Lemma 3: "T15 at a terminal-round prefix") must be checked for general h; and the RB terms. Components: THM-INV
rows 9, 10 (A), the empty "joint inclusion" cell.

**(iv) Novelty.** NEW-COMP. The mechanism (evidence weight sits on correct realisations) is F-MASKPIP's; the SLLN part is
WLH. LIT-SMC: masked-regime Ẑ/PIP results "sit where the general bounds are vacuous".

**(v) Difficulty and route.** M. Steps: (1) write the islandwise identity for the measured-round average of a bounded
h from the locked T12/T15 statements; (2) copy M1's proof with h; (3) Prop P(iii) with the truncation variant; (4)
compose with T03♯ for (d). Risk: (d)'s R_n condition is uncheckable without an upper bound on E[W²|𝓒_n] (or on
M_𝓒(ε)). Lower bound (PROOF SKETCH, this run): by Cauchy–Schwarz E[W²|𝓒] ≥ (E[W·1_cross|𝓒])²/P_𝓒(cross), and E[W·1_cross|𝓒] → 1 whenever the non-crossing islands' evidence is negligible (F-MASKPIP M2: Ẑ_r ≤ √δ₁Z there except w.p. 2√δ₁), so R_n must at least exceed the reciprocal crossing probability. Do **not** cite F-MASKPIP M3 for this: THM-INV records M3 as XF ERROR. The
v1 paper states (a)–(c), (e) as theorems and (d) with R_n as a hypothesis, disclosing the lower bound.

**(vi) Lean.** (a)'s deterministic step and (b)'s finite inequality: certifiable on a finite state space with abstract
weights; Maurer/Hoeffding and the SLLN: cited probability.

**(vii) Depends on.** V1, V3, M1; T03♯ (R1) for (d).

### A2. Theorem Z (the evidence: what Ẑ can and cannot do)

**(i) Statement.** Setting of V1, one island (pooling by V1).
(i) E[Ẑ_r | 𝓒] = Z; E[log Ẑ_r] ≤ log Z; P(0.05Ẑ > Z) ≤ 0.05 (regime-free).
(ii) *Exact variance identity* (O-PW2 Thm A): N·Var(W_T | 𝓒) = Σ_{s<T}(1 − 1/N)^{T−1−s}(E[W_s² μ_s(h²_{s,T})] − 1), for
any q_t-invariant round kernels; pooled variance = this/R.
(iii) *Masked regime, lower tail* (MASKZPIP E1/E2): for any kernel, grid and N, with A the truth's basin, τ_A the first
stage with a particle in A and D_A the d-gap, P(W > (T/η)[π₀(Aᶜ)/π₀(x_m)]e^{−φ_{τ_A}D_A}) ≤ η + Nπ₀(A); on a frozen path
log W = (a + Λ)(φ* − φ_τ) + O(1): Ẑ underestimates by the log-odds overshoot of a late crossing. F-MASKPIP N(a): if the
terminal population is off S₀ at stage T with probability ≥ κ, Ẑ_r ≤ √δ₁·Z there.
(iv) *Run certificate* (MASKZPIP C1): Ẑ/Z ≤ Ẑ/Z_𝒯 on every run, so Ẑ < Z_𝒯 certifies underestimation; island agreement
certifies nothing (E1c).
(v) *Favourable regime* (W2-T26 Thm A): under EX-A, EX-S, CAL, START, OUT and (P1) (T_n + 1)Δ_n → 0, Ẑ/Z → 1 in
probability on the output event.

**(ii) Plainly.** Ẑ is unbiased everywhere, two-sided accurate in the favourable regime, and in the masked regime it
can only fail *downward*, by an amount the run can partly certify. A referee asks "is Ẑ meaningful under masking"
(F-REFEREE M7); this is the honest answer. Two-sided masked accuracy is **not** claimed in v1.

**(iii) Status.** (i) T12/T31(i) PROVED-LOCKED (KNOWN—CITE). (ii) O-PW2 Thm A PROVED (candidate), XF VERIFIED (A-REV9);
Thm B/C PROVED (candidate), vacuous at study scale without an L² mixing input. (iii) E1/E2 PROVED (candidate), N(a)
PROVED. (iv) C1 PROVED (deterministic); E1c PROVED. (v) T26-ThmA PROVED, XF VERIFIED* (actual statement; the
single-premise shorthand GAP); Thm 6 overall CONJECTURE; (P1) held in 1/56 runs at n ≤ 3,200. Components: THM-INV row 9.

**(iv) Novelty.** (i) KNOWN—CITE. (ii) "same kind as Cérou–Del Moral–Guyader 2011 Thm 1.4", unchecked (LIT-SMC): must be
checked before claiming. (iii),(iv) NEW ("outside all general bounds", LIT-SMC). (v) standard pattern (D6, settled in
REPORT §4: present as a remark whose only new content is the stage-count input).

**(v) Difficulty.** S for assembly. The two-sided masked statement (V11 "resolved grid ⇒ O_P(√(T/N))") is CONJECTURE,
OPEN for c ≥ 2, and is **v2** (HQ-VAR). Route there: O-PW2 Thm C with an L² mixing constant for the φ = 1 round
restricted to V (not the full space), plus the E3/Lemma J resolved-grid mechanism.

**(vi) Lean.** (ii) and (iv) are identities/inequalities on a finite space: certifiable (ii needs the particle system as
a finite Markov chain, as in T12_PLAN). (iii) finite but long. (v) cited.

**(vii) Depends on.** V1; D2 (stage count enters (v) through (P1)).

### A3. Theorem Z𝒯 (top-store evidence and PIPs: two-sided, deterministic)

**(i) Statement.** Let 𝒯 be the reported top store (40p + 1 best models by F, Lemma S), Z_𝒯 := Σ_{S∈𝒯} ϖ(S)m(S) and
PIP^𝒯_j := Σ_{S∈𝒯, j∈S} ϖ(S)m(S)/Z_𝒯. If S₀ ∈ 𝒯 then 1 − δ₁ ≤ Z_𝒯/Z ≤ 1 and |PIP^𝒯_j − PIP_j| ≤ δ₁ for every j; the same
for any bounded h: |Σ_𝒯 h π_𝒯 − π(h)| ≤ 2δ₁‖h‖_∞. Under T03♯ and discovery (R5), Z_𝒯/Z → 1 at rate δ₁ on the masked
family.

**(ii) Plainly.** The one reported evidence quantity that is two-sided and consistent in the masked regime is the
top-store sum, not Ẑ; it needs no grid, mixing or second-moment hypothesis, only that the truth was scored. It
decouples "evidence accuracy" from "importance-sampling accuracy" (Prop W4's split made concrete).

**(iii) Status.** MASKZPIP P3 PROVED (candidate, deterministic). Composition with T03♯ + discovery: same status as R5.

**(iv) Novelty.** NEW in kind (the reported-quantity trick); elementary. (v) S. (vi) Lean: yes, finite (sum over a
finite store; the bound is a two-line inequality). (vii) Depends on R5 (S₀ ∈ 𝒯) and R1.

### A4. Theorem PIP (equal-weight PIP accuracy; delivery + repair reduction)

**(i) Statement.** (P1) |E[PIP̂_rj] − PIP_j| ≤ TV(law of the delivered population, π) with no L, B, ρ̄ term; after locking
(all particles at S₀) the bias is ≤ δ₁ and the L¹ error ≤ (L+4)ρ̄ + u_π + δ₁ = O_P(log n √(log n/n)) under T03 (P2,
composition; locking = BG3, LH fixed p). Theorem R (F-MASKPIP): E max_j|PIP̂_rj − 1{j∈S₀}| ≤ δ_𝔛 + β_H + (L+4)ρ̄ + u_π,
with δ_𝔛 the expected stage-T population fraction outside a repair basin and β_H the H-round entrance failure; masked
PIP/MPM consistency reduces to DELIV-POP and REP.

**(ii) Plainly.** The equal-weight PIP is right iff the population is delivered and repaired; it does not improve with
R (V3(i)). This is why the Ẑ-weighted PIP is reported alongside.

**(iii) Status.** P1 PROVED; P2 PROVED (composition, needs locking: LH fixed p); Thm R PROVED as composition, CONDITIONAL
on DELIV-POP (OPEN, stronger than T38's one-particle DELIV) and REP (ThmB-T24, PROVED, vacuous at n = 200).

**(iv) Novelty.** NEW-COMP. **(v)** P1 S; Thm R's inputs are the hard part (v2, HQ-DELIV). **(vi)** P1: certifiable
(finite TV bound). **(vii)** Depends on V1; R5(b2) for DELIV.

**Group G2 tiering note.** v1 proves: V1 (cited), A1(a)(b)(c)(e) + (d) with R_n as a hypothesis, A2(i)–(v), A3, A4-P1.
v1 states as limitations: no two-sided masked Ẑ (A2); equal-weight PIP accuracy in the masked regime needs delivery (A4);
the island count R_n needed in (d) is not bounded above. v2: HQ-VAR, HQ-DELIV.

---

## G3. Parallel work and depth (objective 2)

### D1. Theorem D (work, depth and width of v3.1; comparison with Song–Liang §6)

**(i) Statement.** Units: one score evaluation s(k) at model size k (s̄ its mean on the path). Let m = p + B + 2 (steps
per round), ℓ = ⌈log₂(n+p+1)⌉, L = max(4, ⌈log₂(n+1)⌉), I_e ≤ ℓ rebuild iterations, T_pil, T^{(i)}, T the stage counts,
T ≤ T_e = max(1000, ℓ²)·4^e on success (deterministic, Theorem G), N = N_e, R islands.
(a) *Work:* W = J·2^B·s(B) + Σ_e[H_e(T_pil + L + 4) + 4H_e Σ_i(T^{(i)} + L + 4)]·m·s̄ + R·N·(T + L + 4)·m·s̄
+ n_LS(ℓ+1)(p + k̄(p − k̄))s̄ + O(np²) + O(p²)–O(p³). Under the v3 budgets W is polynomial in n (T32(i); the displayed rate
is a GAP, Astra's candidate O(max(n,p)·p·log³(n+p) + p²log²(n+p))).
(b) *Depth, island-parallel (layer (a)–(c)):* D_PEL = D_setup + Σ_e[H_e(T_pil + L + 4) + H_e Σ_i(T^{(i)} + L + 4)]·m·s̄
+ N(T + L + 4)·m·s̄ + n_LS(ℓ+1)s̄, with width R (islands) and p + k̄(p−k̄) (scans).
(c) *Depth, particle-parallel (declared v3.2 path, law-preserving):* D_PP = D_setup + [(T_pil + L + 4) + Σ_i(T^{(i)} + L + 4)
+ (T + L + 4)]·m·s̄ + O(ΣT·log N) + local searches; **free of N, H and R**; worst case on success O(m·ℓ·T_e) =
O(p log³(n+p)) score evaluations; width R·N.
(d) *Comparison, same units:* Song–Liang §6 with K_n = √p processors has wall time O(p^{(1+α)/2}) + O(np) with
T = O((p/K)^α) SAMC iterations per subset, α a choice (α = 1 in the paper), total work O(p^{1+α/2} + np^{3/2}), width √p,
output = posterior restricted to the merged set. v3.1: depth O(p(ℓ+2)(T+L+4)) with T from D2, work O(N·p·(ℓ+2)·T_e),
width R·N, output = π exactly (V1). At α = 1 the depths have the same order in p up to log factors; ours needs far more
width and work; what is bought is correctness under correlation.

**(ii) Plainly.** The parallel claim in the units a referee expects (work/depth/width; LIT-PAR §3.3), with the per-round
factor m = Θ(p) stated honestly (it is 2–3 ms per round at p = 500; METH-AUDIT §6) and no claim "faster than SaM".

**(iii) Status.** Prop D PROVED (counting, given the code's structure; METH-AUDIT); T32(i) PROVED (W5-LOCKBOOK), rate GAP
(A-REV6); SL §6 figures from the JRSS-B text (SL digest §4). Components: THM-INV rows 8 (C), 11 (C), 14.

**(iv) Novelty.** Accounting. The work/depth reporting style is TCS-standard (LIT-PAR §2.3); Lindsten et al. / Kuntz et
al. report D&C-SMC depth the same way. SL's §6 analysis is "cost only, no accuracy trade-off, T assumed without a mixing
proof" (SL digest).

**(v) Difficulty.** S. Route: copy Prop D; add the measured table (METH-AUDIT §6, when its "[filled in after the runs]"
placeholder is actually filled: **check before citing**); add the SL column.

**(vi) Lean.** The counting identity (c) is a finite sum over the code's loop structure: certifiable as an abstract
"depth of a composition of stages" lemma, but of low value; the Θ(p) per-round factor is a definitional fact.

**(vii) Depends on.** D2 (T bounds); V2 (concurrency is bitwise, so the depth claim is about the same estimator).

### D2. Theorem STG (stage laws of the v3 grid)

**(i) Statement.** Grid rule as coded (O-STAGES §2), Φ_V(u, v) = D₂(q_v‖q_u) on the candidate set V, threshold
c = log(10/9).
(a) *Structure* (Theorem G, Lemma RS): for any finite V the ESS criterion is monotone in both endpoints, so the bisection
finds the exact frontier; the greedy grid is the shortest valid grid; max(T*_V, T_P) ≤ T_grid ≤ T*_V + T_P; T ≤ T_e
always on success.
(b) *Favourable* (STG-F, Theorem F): T* is bounded two-sided through q_w(S₀), w ∈ [1, 2]; T* = O(1) on BO with p ≤ n^A;
with Theorem W's layer law |T* − ⌈log₂(1 + 1/g)⌉| ≤ 1.
(c) *Masked crossing* (STG-M): on the ideal exact-frontier two-state grid, T* = log₂A₀ + O(1), A₀ := log[π₀(S°)/π₀(S₀)]
the start's masking depth; numerically T* = log₂A₀ + 7.7 ± 0.4. Hence proxy masking (A₀ = Θ(n)) costs log₂n + O(1)
stages and LH/T27 masking (A₀ = c log p + (c/2)log n) costs O(log log n) stages.
(d) *Fine grid* (item 4): √c·T*(c) → L = ∫₀¹ sd_{q_φ}(d)dφ as c → 0 (= Syed et al.'s Λ); at the production c, L ≤ π while
T* → ∞ on the two-state family, so path length does not determine T_n.

**(ii) Plainly.** Correlation enters the depth only through A₀, a functional of the start built from correlation blocks
(LIT-PAR G3): "correlation costs depth" with the depth named. This is the "stage law" the thesis needs and SL lacks.

**(iii) Status.** (a) Theorem G PROVED (deterministic, as-coded rule; API-T26BUD candidate); Lemma RS PROVED. (b) STG-F
PROVED; W′ PROVED conditional on the layer law (PROOF SKETCH in F-DRAFT). (c) STG-M PROVED on the two-state ideal grid,
XF VERIFIED* (A-REV9); families PROOF SKETCH; **the as-coded grid's realised T_n in the masked regime is Conjecture P,
OPEN** (THM-INV §5.9). (d) PROVED (two-sided κ-regularity). Components: THM-INV rows 5, 7 (C).

**(iv) Novelty.** (a)(i) KNOWN—CITE (Štefankovič–Vempala–Vigoda 2009, J. ACM 56(3)); (d) KNOWN—CITE (Syed et al.
arXiv:2408.12057 Thm 3; Gelman–Meng 1998); (b),(c) NEW ("plausibly new, elementary", LIT-SMC; "clean new observation"
LIT-PAR G2).

**(v) Difficulty.** v1: S (state (a)–(d) as they stand, with (c) on the ideal grid and the T_e cap as the as-coded
guarantee). v2: M–L for Conjecture P (the candidate grid refines the pilot points and uses V, not Ω; needs COVER(V) and the
pilot's H → ∞ idealisation removed).

**(vi) Lean.** Lemma RS (log-affinity ⇒ ρ = q_u q_w/q_v²) and Lemma 1 (convexity ⇒ monotonicity) and Theorem G(i)–(ii)
(greedy optimality for a monotone feasibility predicate on intervals) are finite/real-analytic and certifiable; the
two-state asymptotics (c) are real analysis, feasible but longer; (d) cited.

**(vii) Depends on.** S1 (A₀ from T27(i) / DIL); V1.

### D3. Theorem CD (the thesis sentence as a theorem) — see REPORT §3 for scope and wording

**(i) Statement (assembled; v1 scope).** Fix any design X (any correlation) and data, EX-A, EX-S, CAL, R declared.
(a) [*never correctness*] The final stage of every island targets π exactly; E[Ẑ_r|𝓒] = Z; the Ẑ-weighted pooled
estimate of any bounded h converges to π(h) as R → ∞ at fixed N and as N → ∞ (V1); the islandwise Ẑ-weighted error of
any bounded h is ≤ 2δ₁ + c_h(ρ̄ + u_π) on every island (A1(a)), with no premise on the start or on X.
(b) [*costs depth*] The critical path is (I + 2)(T + L + 4)·m score evaluations, free of N, H, R (D1(c)); T ≤ T_e
deterministically, and on the ideal grid T = O(1) (favourable) or log₂A₀ + O(1) (masked crossing), where A₀ is the start's
masking depth, a functional of X through the blocks (D2).
(c) [*costs particles/islands*] The Ẑ-weighted pooled error exceeds t with probability ≤ exp{−R(1−s)²/(2E[W²|𝓒])} +
(2δ₁ + …)/(st) (A1(b)); E[W²|𝓒] ≳ 1/P_𝓒(crossing) (Cauchy–Schwarz + M2, PROOF SKETCH in A1(v)), so the island count needed
grows with the masking depth through the crossing probability; the equal-weight PIP's bias is set by N alone (V3(i)).
(d) [*selection*] On LH (exact Gram) the reported HPM equals S₀ w.p. → 1 − limsup P(U) (R5), while a feature-splitting
procedure loses the masked hub (C1).

**(ii) Plainly.** The only places correlation enters are T (through A₀), R and N; it never enters the target, the
identities or the limit. Correlation is a cost, not a correctness condition. Compare SL's Condition 5, which is a
correctness condition.

**(iii) Status.** Assembly of V1 (KNOWN—CITE + locked), A1 (PROOF SKETCH), D1 (PROVED counting), D2 (PROVED ideal grid /
OPEN as-coded), M3 (PROVED), R5 (PROVED candidate, XF VERIFIED on LH), C1 (COUNTEREXAMPLE + PROOF SKETCH). The weakest
links are A1 and C1 (PROOF SKETCH) and the as-coded T_n law (OPEN).

**(iv) Novelty.** NEW-COMP: LIT-PAR S-GAP (no published method has (i) exact target with unbiased Ẑ, (ii)
communication-free width, (iii) a proved depth bound under a correlated masked start).

**(v)–(vii).** Difficulty = that of A1 + C1; Lean: none beyond the parts; depends on everything above.

### D4. Corollary V (R versus N at fixed total particles)

**(i) Statement.** For R islands of N_r = N/R particles, N·Var(Ẑ_pooled/Z | 𝓒) = Σ_s(1 − R/N)^{T−1−s}σ²_{s,T} +
O((R/N)^{1/2})·(…): the leading constant does not increase with R; the remainder grows as N_r shrinks; in the exact-refresh
idealisation Var(W) = Π_t(1 + χ²_t/N_r) − 1 so R·N_r fixed is neutral while Σ_tχ²_t ≪ N_r.

**(ii) Plainly.** Splitting a fixed budget over more islands is neutral for Ẑ to first order but hurts the equal-weight
PIP (V3(i)); hence layer part (d) stacks islands at fixed N_e instead of splitting.

**(iii) Status.** PROOF SKETCH (METH-AUDIT; the O-PW2 Thm B quantities not re-derived; DELIV under a split OPEN).
**(iv)** partly KNOWN (WLH: pooled relative variance = single-island/R). **(v)** M; **v2**. v1 states only the two PROVED
halves (V3(i),(ii)) and the design decision. **(vi)** no. **(vii)** O-PW2 Thm B; A2(ii).

**Group G3 tiering note.** v1 proves D1(a)–(d), D2(a),(b),(c on the ideal grid),(d), D3 in the scope of REPORT §3. v1
states as limitations: the as-coded masked T_n law (Conjecture P), the per-round Θ(p) depth factor, the absence of an
upper bound on E[W²|𝓒]. v2: Conjecture P (HQ-STAGES-2), Cor V, a masked E[W²] bound (HQ-VAR).

*(continued in Part B: G4, G5, G6.)*

---

## G4. Why the bridge; why the merge alone fails

### S1. Theorem 2 (the start: deterministic mass, favourable rate, masking law, dilution identity)

**(i) Statement.** Blocks C₁..C_J (complete linkage, cut, next-fit packing; |C_b| ≤ B), tables r_b, π₀ = γ₀/Z̄₀.
(a) *Deterministic* (T22(i)(ii)(iv)): for any feasible reference S° with AGG quantities (q, e), π₀(S°) ≥ (1−q)^{s+1}/(1+e)^s;
the odds π₀(S₀)/π₀(S°) are exact (product of table ratios); the bridge never puts less mass on S₀ than min(π₀(S₀), π(S₀)).
(b) *Favourable* (T22(iii), EXP′): under EXP′, VIS, NL_η, NL_avg(κ), 1 − π₀(S₀) = O_P(2^B √(log n) n^{−κ}); FAV-ThmA/B give a
2^B-free rate on iid block-diagonal designs.
(c) *Masked* (T27(i), Thm3/4-EXP): if c true variables mask each other along an addition chain (H2, H3), then
π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}. On LH exact Gram this holds with no open hypothesis (W1-EXP Thm 5).
(d) *Dilution identity* (DIL-E): for any data and partition, −log π₀(S₀) = V + C − log A with V = Σ_b softplus(−λ_b) ≥ 0
(truths invisible to their own table), C ≥ 0 (table mass on sub-models other than ∅ and S₀∩C_b), A the non-product part
of BB(1,p); the exact joint law of (#truths, #non-truths) under π₀ (Thm R) gives π₀(𝓡_d) by a two-variable convolution.
On 480 regenerated study fits V carries 83% of the deficit; median π₀(S₀) = 10^{−15.7}, median π₀(𝓡₂) = 0.79.

**(ii) Plainly.** The merge (= π₀, Song–Liang's "merged" object) is exactly computable, carries the truth when blocks
see it, and provably loses it by a polynomial factor when true variables cancel; at n = 200 it loses it by σ²-dilution
(7 of 14 truths invisible). This is why a correction step exists at all, in two sentences, and it is the input A₀ to D2.

**(iii) Status.** (a) PROVED-LOCKED (wave 1). (b) PROVED-LOCKED CONDITIONAL (EXP′ XF VERIFIED* fixed design; FAV author
only). (c) PROVED-LOCKED CONDITIONAL (H2, H3); Thm3/4-EXP XF VERIFIED; on LH no open hypothesis. (d) DIL-E/E1/R/N PROVED,
XF VERIFIED (A-REV9); DIL-DM(i) ERROR (do not cite). Components: THM-INV row 4.

**(iv) Novelty.** (c),(d): NEW ("strongest novelty claim", LIT-STAT; "nobody proves a natural exactly-sampleable start
fails and then which moves fix it", LIT-VENUE G3). (a): block start KNOWN (Papaspiliopoulos–Rossell 2017, exact only
for block-diagonal XᵀX); cite as the precedent. Framing citation: Woodard–Schmidler–Huber 2009 (low persistence).

**(v) Difficulty.** S (restatement). Never combine (b) and (c) on one sequence. Put (b) in the supplement: the study is
favourable in 1/2,394 fits and the T22(iii) rate is vacuous at n = 200.

**(vi) Lean.** (a) is finite algebra on tables: certifiable (T22(i) is a product inequality). (d) is an exact identity on
a finite partition: certifiable and a good first Lean target of G4. (b),(c): Gaussian probability, cited/prose.

**(vii) Depends on.** Nothing; feeds D2 (A₀), S2, C1, R5.

### S2. Theorem SEP and Lemma KL (why the merge alone, or a one-shot correction, fails; the exp(KL) cost scale)

**(i) Statement.** LH exact Gram with cancellation depth c; Q* := p^c n^{c/2}; Mstat := log π₀(S₀) + log Q*.
(a) *SEP-A (iid discovery):* P₀(S₀ scored by Q iid π₀ draws plus the tables) → 0 if Q/Q* → 0 and → 1 if Q/Q* → ∞. With
p ≍ n^a, a polynomial budget n^α fails iff α < c(a + ½); the iid exponent exceeds v3's polynomial ceiling exponent
a + max(1, a) iff c ≥ 2.
(b) *SEP-B (one-shot importance correction from π₀ to π):* 1 + χ²(π‖π₀) ≥ Q*e^{O_P(1)}; the relative variance of the
self-normalised estimator with Q draws is (Q*/Q)e^{O_P(1)}, and its estimate of π(S₀) is exactly 0 w.p. → 1 below Q*.
(c) *Lemma KL (NEW-SYNTH, elementary):* for any π, π₀ on Ω with δ₁ = 1 − π(S₀),
KL(π‖π₀) ≥ (1 − δ₁)·log(1/π₀(S₀)) − log 2.
Proof: data processing on the partition {S₀, Ω∖S₀} gives KL(π‖π₀) ≥ kl(1−δ₁ ‖ π₀(S₀)) ≥ (1−δ₁)log((1−δ₁)/π₀(S₀)) +
δ₁ log δ₁ ≥ (1−δ₁)log(1/π₀(S₀)) − h(δ₁) with h ≤ log 2. ∎ (PROOF SKETCH only because unreviewed; the inequality is
two lines.) Consequently, under T27(i), the Chatterjee–Diaconis sample size exp(KL(π‖π₀)) for importance sampling from
π₀ to π is ≥ ½·Q*^{1−δ₁}·e^{O_P(1)}: the exp(KL) scale and SEP-B's Q* agree (THM-INV §4b B1 called this identification
"my inference, unproved"; Lemma KL makes it a one-line corollary).
(d) *What is not separated* (W7-SEP items 1, 4): on LH, one greedy search from the start mode already scores S₀ (R3 +
R5(b1-LH)); there is no super-polynomial separation between the bridge and a greedy search in the frozen setting (c ≤ s₀
fixed). The paper may say "moving off the start is needed", **not** "tempering is needed" (E-SPINE decision).

**(ii) Plainly.** Keeping the merge as the answer (SL's Stage-1 object, or a product-of-blocks posterior) or correcting
it in one importance-sampling shot costs p^c n^{c/2} draws; the exp(KL) law says this is necessary and sufficient for any
one-shot scheme. The bridge's job is to make the correction's cost logarithmic in A₀ (D2) instead of exponential in it.

**(iii) Status.** SEP-A/B PROVED, XF VERIFIED (A-REV9). Lemma KL PROOF SKETCH (this run; checked numerically in
`scripts/check_lemmas.py`). Chatterjee–Diaconis 2018 Thms 1.1/1.2 KNOWN—CITE. (d) PROVED (candidate, W7-SEP), with its
COUNTEREXAMPLE to the task's own claim (a). Components: THM-INV row 4 (F).

**(iv) Novelty.** SEP NEW (LIT-SMC G2, LIT-MCMC Θ4: no BVS tempering separation exists in the literature); Lemma KL
elementary; the composition with Chatterjee–Diaconis is the paper's "why one-shot fails" sentence.

**(v) Difficulty.** S. Route: restate SEP-A/B; add Lemma KL with its proof; cite CD18.

**(vi) Lean.** Lemma KL: yes (finite KL on a finite set, log-sum inequality; Mathlib has `klDiv`/`Real.log` tools), a
model Lean target. SEP: Gaussian probability, prose.

**(vii) Depends on.** S1(c).

### S3. Proposition M (naive merge of block fits fails) — DROPPED as a theorem

**Status.** A-DRAFT Prop M / SHARE-M(b): ERROR (A-REV3/A-REV6); FD-NM ERROR, repair pending. LIT-STAT: "known phenomenon
... for motivation, not a contribution; refutes a naive union, not Song–Liang". **Decision:** drop. What survives: W5-B2ENV
Prop M-LH (XF VERIFIED as a restricted fixed-coefficient replacement) as a one-sentence remark, and S2 as the quantitative
statement. The Song–Liang comparison is C1, not this.

### S4. Weight stability (proposal §5.3) — supplement remark only

O-WSTAB WS1–WS8 PROVED (no review), W(a–f) XF VERIFIED under H-ORTH and an ideal grid; WS6e CONJECTURE, WS8d OPEN; FD-W(a)
PROVED-UNDER, (b) PROOF SKETCH, (c) CONJECTURE. Proposal §5.3's "weak cross-block dependence ⇒ bounded weight variance"
is matched only in the orthogonal-type idealisation (THM-INV §3a). **v2**; v1 cites Frazier et al. 2023 Assumption
6(iv) (χ²-type proposal condition) as the generic precedent and gives the ESS-0.9 schedule as the method's answer.

**Group G4 tiering note.** v1: S1(a),(c),(d) in the main text (Thm 2), S1(b) in the supplement, S2(a)–(c) as Theorem SEP +
Lemma KL + a cited CD18 corollary, S2(d) as wording discipline. Dropped: S3. v2: S4.

---

## G5. Correlation robustness versus split-and-merge

### C1. Theorem SL (an analytic separation from Song–Liang's split-and-merge on a masked family) — NEW-SYNTH

**Setting (from the JRSS-B text; SL digest, THM-INV D10).** Song–Liang's procedure (SL §3.1): uniformly random
partition of the P_n predictors into K_n subsets of size s_n = P_n/K_n (recommended K_n = O(√P_n), SL §6); Stage 1 per
subset: BVS on D_n^{s} = (y, X_s) with priors σ² ~ IG(a₀,b₀), β_ξ | ξ ~ N(0, σ²V_ξ), π(ξ) ∝ λ_s^{|ξ|}(1−λ_s)^{|s|−|ξ|}1{|ξ| ≤ s̄},
λ_s = |s|^{−γ}; selection of predictors whose marginal inclusion probability passes a threshold (FDR rule at level α₁);
iterative re-selection on the remainder (justified by Condition 5: |cov(x_t, y)| > 0 for every true predictor; capped at 2
iterations); merge S̃ = ∪ s̃_i; Stage 2: BVS on (y, X_S̃) with prior r_n/p_n. Theorem 4 / Corollary 2 with eq. (19): for a
fixed subset s, the subset posterior concentrates on the KL projection f₀ with β₀ = Σ_s^{−1}cov(x_s, y), and a true
predictor t ∈ s is asymptotically selected iff β_{0,t} ≠ 0 (the "only if" direction is stated in the text after Cor 2, not
proved there; see crux (ii)). SL's output is the posterior restricted to S̃ (prior mass 0 outside S̃; SL §7).

**Our family.** LH exact Gram (W1-EXP §4): independent equicorrelated groups of size g (correlation ρ), c linked pairs of
hubs (j_{a_i}, j_{b_i}) with corr(j_{a_i}, j_{b_i}) = ψ_i, 0 < |ψ_i| < ρ, θ_{j_{b_i}} = −ψ_iθ_{j_{a_i}}, visible hubs
θ_{j_h} = β_h, null groups; X′X = (n−1)Σ_LH, p ≤ n − 1. Masked hubs M = {j_{b_i}}; S° = S₀ ∖ M.

**(i) Statement (proposed).** Let E_n be the event that, for some i, the masked hub j_{b_i} is *isolated* in its subset:
its subset contains neither j_{a_i} nor any other member of j_{b_i}'s group.
(a) *Isolation probability (finite combinatorics):* for a uniformly random equipartition, P(a given other column shares
j_{b_i}'s subset) = (s_n − 1)/(P_n − 1), so P(E_nᶜ) ≤ c·g·(s_n − 1)/(P_n − 1) ≤ c·g/K_n, and P(E_n) → 1 whenever K_n → ∞
(in particular under SL's K_n = O(√P_n)). Exactly, P(j_{b_i} isolated from g given columns) = C(P_n−1−g, s_n−1)/C(P_n−1, s_n−1); the union bound is vacuous at small K_n: at K_n = 2, P(isolated) = 0.53 for g = 1 (LIT-PAR's design, P = 16) but 0.05 for g = 4 (`scripts/check_lemmas.py`). So at fixed K_n the failure probability is bounded away from 0 but can be small; the "→ 1" needs K_n → ∞.
(b) *Loss of the hub on E_n (exact-Gram orthogonal-null lemma):* on E_n, x_{j_{b_i}} is orthogonal to every other
column of its subset and x_{j_{b_i}}′μ = (n−1)(θ_{j_{b_i}} + ψ_iθ_{j_{a_i}}) = 0 exactly, so in its subset x_{j_{b_i}}
is an orthogonal null column: Condition 5 fails exactly (cov = 0), β_{0,j_{b_i}} = 0 in every iteration, and under SL's
priors π(j_{b_i} ∈ ξ | D_n^{s}) = O_P(λ_s·n^{−1/2}) → 0. Hence P(j_{b_i} ∈ S̃ | E_n) → 0 and SL's output cannot contain
j_{b_i}: P(SL output = S₀) ≤ P(E_nᶜ) + o(1).
(c) *The exact posterior is not the problem:* on the same family 1 − π(S₀) → 0 (W1-EXP Thm 5(d) / T03♯), and SL's own
Theorem 3 (sure screening of identifiable predictors) applies to the full posterior: the failure is the split.
(d) *v3.1 on the same family:* the final stage targets π exactly and all of V1 holds; with LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0
(R5 (b1-LH), XF VERIFIED); without LS0, the same on A-REV7's STAB-LH subfamily (R5 (b2-LH)); the Ẑ-weighted PIPs and joint
inclusions satisfy A1.
(e) *Remark (clustered splits):* if the split keeps j_{b_i} with its group, β_{0,j_{b_i}} = ψ_iθ_{j_{a_i}}([Σ_bb^{−1}]₁₁ − 1) ≠ 0
(the members carry the marginal signal −ρψβ), so Stage 1 retains the hub: SL's theory does not analyse clustering, and
a clustered split still loses power (LIT-PAR note 09: 3/20 at β = 0.6). Our blocks are used only for the start.

**(ii) Plainly.** The thesis sentence's first half as a theorem: "in split-and-merge, correlation breaks correctness":
SL's correctness condition (Condition 5 / β_{0,t} ≠ 0) is violated *exactly* by a cancelling pair, and random splitting
isolates the masked variable with probability → 1 under SL's own K_n, after which no later stage can recover it (prior
mass 0). v3.1's correctness has no such condition. A referee will ask for exactly this (the task's G5).

**(iii) Status.** COUNTEREXAMPLE (numerical, reproducible: LIT-PAR G4, p = 16, n = 200, 5/318 separated splits vs 20/20 for
the exact posterior at β = 1; 0/318 at β = 0.6) + PROOF SKETCH (this run, (a)–(e) above; the isolation argument is new and
differs from LIT-PAR's sketch, which did not consider the hub's group). The numerical seed used a singleton masked
variable (g = 1) and Liang's slides; it should be re-run on the W1-EXP LH family with g ≥ 2 and K ∈ {2, 4, √p} to show
(a)'s dependence on K (first step of HQ-SL). Components: THM-INV §3b rows "Thm 4/Cor 2" and "UQ of the merged output".

**(iv) Novelty.** NEW. No analytic SaM failure is published (LIT-PAR; SL digest: SL has no theorem for the composed
procedure). Cite SL Thm 4 / Cor 2 + eq. (19) + Condition 5 from the JRSS-B text, never "Thm 5" from slides.

**(v) Difficulty and route.** M. Crux (ii): the orthogonal-null PIP → 0 under SL's IG + Gaussian + λ_s prior. With known
σ² the inclusion posterior of an orthogonal column factorises exactly and the Bayes factor of a null column is O_P(1)·
(1 + nV)^{−1/2}; with σ² integrated, use the standard Laplace/ratio bound (one page). The FDR rule: a variable whose PIP
→ 0 is not selected provided the data-driven threshold is bounded away from 0, which holds when S̃ ≠ ∅ w.p. → 1 (the
visible hubs give PIPs → 1); otherwise state the theorem for a fixed threshold q ∈ (0,1) and add the FDR rule as an
escalation. Also to check: SL's cap s̄ and the iteration cap do not matter (an orthogonal null column is never selected at
any iteration). The LH-iid (random design) version replaces the exact orthogonality by population orthogonality plus
concentration (mirror W3-PXN): **v2**.

**(vi) Lean.** (a) is finite combinatorics (hypergeometric sharing probability for a uniform equipartition): certifiable.
(b)'s identity x′μ = 0 and the orthogonality are finite linear algebra on Σ_LH: certifiable. (e)'s coefficient formula is
a 2×2-type inverse of an equicorrelation matrix: certifiable. The PIP → 0 step rests on cited probability.

**(vii) Depends on.** S1(c) (LH masking), R1 (c), R5 (d), A1 (d), V1.

**Group G5 tiering note.** v1: C1(a)–(e) on exact-Gram LH, with (b)'s PIP step as the one proof obligation; the numerical
counterexample re-run on the LH family. v2: LH-iid; the study's dilution designs (where SL's Condition 5 holds but the
within-split projection coefficients are small; no analytic statement yet).

---

## G6. Selection accuracy of the reported output (objective 3)

### R1. Theorem 1 (posterior consistency: T03♯ with T02(i♯), T02(ii♯))

**(i) Statement.** R1 (s₀ fixed, p ≤ n^A), G, R, SE_λ(j₀), SE_w(m♯_n; g₀) with g₀ fixed, BM-∞ or BM(c > c₀), fixed design.
Then 1 − π(S₀) = O_P(√(log n/n)); PIP_j is within that distance of 1{j ∈ S₀}; the HPM and MPM of π equal S₀ w.p. → 1;
P(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)]; without beta-min, large signals still get PIP → 1. T02(i♯): the exact BB(1,p) size tail
replaces the 2^{−m} tail (m_n ≈ s₀ + O(s₀ log n/log p)).

**(ii) Plainly.** The target is right: with enough data the exact posterior concentrates on the truth. Without it,
scoring the truth would not help (THEORY_PRIORITIES story (a)).

**(iii) Status.** T01–T03 PROVED-LOCKED (wave 3; external review queued); T03♯ PROVED, SF W2-VT03R + XF A-REV2 VERIFIED;
the onset sentence ERROR (repaired, W6-FIXREV2 §1.2). Thresholds n ≳ 2·10⁶; beta-min ≥ 43× above the study's signals; SE
impossible at n = 200. Components: THM-INV row 1.

**(iv) Novelty.** MODEST extension of Rossell 2022 (Bayesian Anal. 17(2)) and Moreno–Girón–Casella 2015; T03♯(3) is
Rossell's Prop. 1 verbatim: KNOWN—CITE. LIT-VENUE: "do not sell it". **(v)** S (restatement; disclosure sentence).
**(vi)** Lean: T02(i♯)'s exact tail is a finite combinatorial inequality on binomial coefficients: certifiable; the rest
is Gaussian probability, prose. **(vii)** Depends on nothing; feeds R4, R5, A1(d), A3, C1(c).

### R2. Proposition 1 (Bayes rules; size-prior ceiling; ties)

**(i)** T07: HPM minimises 0–1 loss, MPM Hamming loss; PIP error bounds the excess MPM risk; no size-only prior repairs a
same-size swap; T06(i): two supports tie for every y iff their projections agree. **(ii)** Justifies reporting the HPM and
names the within-size swap as the one error no size prior fixes (the c = 0.5 study misses). **(iii)** PROVED-LOCKED; XF
A-REV4 VERIFIED* (data paragraph ERROR, relabel pending). **(iv)** FOLKLORE (Barbieri–Berger 2004 Thm 1; Scott–Berger
2010): cite; only the sharp ceiling (iii′) is ours. **(v)** S; remark. **(vi)** Lean: sorry-free (T07Bayes.lean, 28
declarations). **(vii)** none.

### R3. Theorem 3 (exact greedy repair: Theorem A; LS-score; Lemma M)

**(i) Statement.** EX-A; completed scans; production tie-broken greedy map. (A1)–(A4): under TD′_∞ on Lat(S°) (every
progress move strictly improves F and no non-progress move beats the best progress move), the local search from any
C ∈ Lat(S°) with ℓ ≥ τ(C) reaches, scores and certifies S₀ in τ(C) ≤ Φ(C) moves; (A4) necessity with its quantifier;
LS-score: LS0 (centre S̃₀ = S° emitted, scans completed) scores S₀ within max{Φ(S°) − 1, 0} moves; Lemma M (= Lemma SC):
the score-comparison margin m_n ≥ M_n√(log n/n) makes TD′ hold w.p. → 1 under SE on the compared sets.

**(ii) Plainly.** From a near-truth centre the deterministic local search finds the truth in finitely many moves; with
LS0 the centre is the start mode, which the masking law puts in Lat(S°). It is the paper's one exact finite-n statement
about the search.

**(iii) Status.** Theorem A PROVED, SF VERIFIED, XF A-REV2 VERIFIED*; cap-free lattice restatement ERROR (A-REV5): keep the
capped lattice; LS-score PROVED, XF VERIFIED (A-REV8; move count repaired V17); Lemma M PROVED, XF VERIFIED (A-REV8).
Literal T37/TD retired (Prop1-TD, CEX1/2 COUNTEREXAMPLE); H24 retired (CE1/CE2). Data: LS0 changed 0/2,394 HPMs; the
final local search repaired 0 fits (all misses are posterior misses). Components: THM-INV rows 11, 12.

**(iv) Novelty.** "Unsurprising given YWJ/ZYVR" (LIT-SMC); must cite Gamarnik–Zadik Thm 2.7 and YWJ Lemma 4 (LIT-MCMC);
the deterministic exact finite-n form is the difference. **(v)** S (done). **(vi)** Lean: sorry-free (T37Greedy.lean,
T37Lattice.lean; Astra round 2 GREEN); LS-score's move count is a short addition. **(vii)** feeds R5(b1).

### R4. Theorem 4 (composition for every n: T21(C1), T38(0), N200, Lemma RO)

**(i) Statement.** EX-A; Ŝ the ≻-maximum of the scored set 𝒮 on the output event 𝒪; S† the ≻-maximum of Ω.
(a) T21(C1)/T38(0): P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n, D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}); (0_H) adds D_n^{sl} under the HPM convention.
(b) N200: P(U ∪ {Ŝ ≠ S₀}) = P(U) + P(𝒪, Ŝ ≻ S₀) + P(𝒪, S₀ ≻ Ŝ) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮), and ≥ P(U) + P(𝒪, S† ≠ S₀) −
P(𝒪, S† ∉ 𝒮), with Π(X) := P₀(S† ≠ S₀ | X) the design's posterior-miss probability; Π(X) ≤ 2E₀δ₁; lower bracket
max_e p_e ≤ P₀(L | X) ≤ Π(X).
(c) Lemma RO: on 𝒢ᶜ the outputs equal the potential run's.

**(ii) Plainly.** Wrong report ⇒ no output, or the posterior itself is wrong, or the truth was never scored. At n = 200
the three terms are: 6/2,400 (measured), 5–75% per cell (computed lower bracket), 0/2,394 (measured). It is the
story's spine and the only inequality that is non-vacuous at n = 200.

**(iii) Status.** T21(C1) PROVED-LOCKED (CONDITIONAL in its routes; (C1) itself is unconditional); T38(0) PROVED, XF
VERIFIED (A-REV1/5/8); N200 PROVED (elementary, author only); Π(X) upper bound OPEN; Lemma RO XF VERIFIED. Components:
THM-INV rows 1 (F), 11, 14.

**(iv) Novelty.** Elementary; the 2E₀δ₁ term KNOWN—CITE (Rossell 2022 Prop 1); the "never scored" split is informally in
García-Donato & Martínez-Beneito 2013 §4; Hou–Wang–Atchadé arXiv:2407.20580 Thm 2 threatens "first finite-n" wording
(LIT-VENUE): do not use it. **(v)** S. **(vi)** Lean: t21_C1 sorry-free (fidelity GREEN); N200 Lemma 1 and (b) are the
same finite set argument: certifiable in an afternoon. **(vii)** R1 (δ₁), R5 (D_n), R6 (P(U)).

### R5. Theorem 5 (two-regime consistency of the reported HPM: T38)

**(i) Statement.** As in `T38_STATEMENT.md` v3 Part I.C, with v3.1 = v3 + LS0 as *the method* and "v3 as run" as the
no-LS0 variant. Assume EX-A, EX-S, CAL, SR, GUARD, (P) on R1. (0) as R4(a). (a) Favourable: under (F), D_n → 0. (b1) LS0
route: under (M1) P₀(π₀(S°) > ½) → 1, (M2) POP-LAT(S°, m_n), (M3) eigenvalue floor, G, OP-LS0: D_n → 0. (b1-LH): on LH
exact Gram with S° = S₀ ∖ M all of (P), (M1)–(M3) hold, so with LS0 P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 with no open statistical
hypothesis; iid final draws miss S₀ when n^{1−c/2}p^{−c}log²n → 0. (b2-LH): no LS0, every c, any frozen grid, under
STAB-LH: P(S₀ ∉ 𝒮 | 𝓒) ≤ Nπ₀(𝒩ᶜ) + NT_e a_n + (1 − c₀ + o(1))^N → 0; explicit Astra subfamily g = 9, c = 2, ρ = 0.4, ψ = 0.2
with STAB margin ≥ 0.4032 and π₀(S₀) = (p√n)^{−2}e^{O_P(1)}. (c) Cost: score evaluations ≤ T32(i)'s ceiling + the LS0 term
1 + (ℓ+1)max_k[p + k(p−k)]: polynomial in n.

**(ii) Plainly.** The reported model is the truth w.p. → 1 − limsup P(U) in both regimes, for the shipped method, on an
explicit correlated family where the start is masked; and also without LS0 on a subfamily. This is the output theorem
no SMC-BVS paper has (LIT-VENUE G1), and with LS0 in the shipped method (task (f)) the XF-verified (b1) route is a
theorem about the method as shipped.

**(iii) Status.** (0) PROVED XF VERIFIED; (0_H) PROVED XF VERIFIED; (a) PROVED-UNDER (F) (ORTH joint family PROOF SKETCH);
(b1) PROVED-UNDER (M1)–(M3), XF VERIFIED (A-REV8); (b1′) PROVED (implication) XF VERIFIED; (b2) PROVED (implication),
DELIV OPEN in general; (b1-LH) PROVED (candidate), SF W5-VMASK, XF VERIFIED (A-REV8); (b1′-LH) PROVED-UNDER, XF VERIFIED
qualitative, rate GAP; (b2-LH) PROVED-UNDER STAB-LH, XF VERIFIED conditional (A-REV7), STAB certificate Astra-authored,
Claude-VERIFIED (API-VSTAB); (b1-LH-iid) PROVED (candidate), XF GAP (A-REV3/6/8); (c) PROVED-UNDER T32(i), displayed rate
GAP. Not covered: the study's generator (groups of 5, p ≫ n), LH-iid, general DELIV, P(U) → 0. Components: THM-INV
rows 6, 11, 12.

**(iv) Novelty.** NEW for the paper's target and method; "a corollary of YWJ/ZYVR/Chang–Zhou under *their* prior"
(LIT-MCMC; D1 settled in REPORT §4: say both). Mathews–Schmidler 2024 template for (a) (LIT-PAR TH6: check whether (a)
reduces to their Thm 1; if so, say so).

**(v) Difficulty.** v1: S for assembly (statement of record exists). Decision needed (HQ/Felipe): headline (b1-LH) with
LS0 (the shipped method) and (b2-LH) on the subfamily as the no-LS0 corollary; the c = 2 clause stays as repaired (V18).
v2: LH-iid (close the Λ(a)/Tr(c) GAP), the study generator (needs a partition law for 2g ≤ B packing: W7-PART CE2 says
unequal groups are not merged), DELIV general.

**(vi) Lean.** The composition (0) is sorry-free; LS-score and the Lat move table are finite (T37Lattice): feasible;
(M1)–(M3) and (b2-LH)'s population bounds are probability: prose. **(vii)** R1, R3, S1(c); feeds R4, A3, C1(d).

### R6. Delivery of output: P(U) → 0 — stated as a limitation in v1

No theorem bounds P(resource_limit), P(schedule_limit), P(numerical_failure), P(grid_unconverged) (THM-INV §5.4). Every
consistency statement is joint with "output exists" and is **not** P(wrong | output). v1 reports P(U) = 6/2,400 (all S5
wall-time stops on one CPU with serial islands) and notes that under v3.1 (concurrent islands, Prop W) the same
allocation gives ≈ 4× headroom, so these are the only fits v3.1 can change; re-running them is the cheapest way to
remove the caveat (METH-AUDIT §9). v2: HQ-DELIV.

### R7. Finite-n upper bound on Π(X) — v2

OPEN (API-N200). v1 gives the lower bracket and the measured remainder (≤ 1.1 points per cell). The convexity "shell"
sketch (API-N200 PROOF §3) is the route.

**Group G6 tiering note.** v1: R1 (asymptotic, disclosed), R2 (remark), R3, R4, R5 (0),(a),(b1-LH),(b2-LH subfamily),(c);
limitations: R6, R7, study generator, LH-iid. v2: R5 extensions, R6, R7, the YWJ-style mixing statement (REPORT §4 D1).

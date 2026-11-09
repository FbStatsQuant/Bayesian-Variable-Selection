# Informed critique of the SMC-BVS theory program (Claude Fable 5.2)

Date: 2026-11-09. Role: informed critic for the strategy review. Written for Felipe and Theory HQ.

**What I read.** The three blind proposals (`BLIND_fable.md` and `BLIND_astra2.md` in full; `BLIND_astra.md` §2–§4);
`W2-UNI/STATEMENT.md` (v1.1.3) and `W2-UNI/REPORT.md` (draft, council pending) in full; headers of the W2-UNI R05a/R05b
sweeps; the `W2-FAC-PK` flags; two spot checks in `Wave1C/FINAL/sections/` (s3, s4); one code check
(`Scripts/SMC_BVS/core/v3_run.R:162`). The chapter v1.0, `07_theory_loop.tex`, the other Wave 2 reports and the HQ audits
B1–B4 were read by two Opus helpers, who returned inventories; I rely on those inventories for statements and statuses.

**What I did not do.** I did not re-check any proof. Statuses below are the files' own. Items marked **[S]** are my own
reasoning in this document and are unchecked. Effort figures are my estimates in agent-days (one prover seat plus the
usual check and council loop).

---

## 0. Bottom line

1. **The posterior theorem is in good shape and ahead of all three proposals.** T03♯ / UNI-P is proved for the coded
   prior and cap, under weaker design conditions than any proposal asks for. Both Astra proposals call this step the
   highest-risk item of the whole package; we have it. It also has the lightest verification trail of our main results,
   so it deserves one independent adversarial re-check.
2. **The reported-model program has drifted from the binding goals.** The goals say design-agnostic and p ≫ n. Yet
   every positive factor-design result (FAC-A, FAC-B, FAC-X, FAC-S5, UNI-1) needs p < n/2, and the general one (UNI-1)
   needs p = o(n^{1/6}). In the target regime p ≫ n the factor program has no positive result and one negative result
   (Theorem NEG). About two thirds of the Wave 2 tickets are spent in a regime the paper does not aim at.
3. **The theory gives the SMC sampler no role.** Reported-model consistency is carried entirely by the deterministic
   LS0 search. For the reported PIPs, MPM and evidence as coded (R′ = 4, equal-weight pooling) there is no
   in-probability statement at all. A referee of an SMC paper will ask about this first.
4. **Three cheap additions from the proposals close most of the gap:** BLIND_fable's concentrated-bridge theorem
   (sampler outputs as coded), its certified-screening theorem (holds for every design with a sparse eigenvalue floor,
   including factors at p ≫ n), and Astra's draw-discovery bound. I add a fourth, a five-line consequence of Lemma N1
   (§4, "Lemma LT") that turns the sampler-accuracy question into one scalar, one-sided premise.
5. **The contradiction on factor designs is a difference of regime.** W2-FAC is right for p < n/2 with one factor.
   BLIND_fable's advice (do not claim reported-HPM consistency under pervasive leakage) is right for the paper's
   headline regime. Details in §2.3.
6. **Recommendation.** Freeze the factor frontier now. Present five theorems (§5): posterior; start and
   misspecification; reported model under two primitive conditions on X (visibility, bounded leakage); sampler outputs;
   certified screening. Design classes, including the one-factor result, become examples. Negative results (GEN C6,
   NEG, SHARP) go in a short "limits" section.

---

## 1. Theorem-by-theorem comparison

Abbreviations: F = BLIND_fable, A1 = BLIND_astra, A2 = BLIND_astra2. "Ours" = chapter v1.0 plus Wave 2.

| Topic (Song–Liang analog) | Ours | Proposals | Verdict |
|---|---|---|---|
| **Posterior concentration** (S–L Thm 1–3, S) | T03♯ (fixed design): normalised floor φ₀² only on S₀ ∪ J with \|J\| ≤ j₀ = ⌈(2A+1)s₀⌉+1; unnormalised floor g₀ up to the data-free prior-tail cutoff m♯_n; beta-min at the log n / n scale; rate O_P(√(log n/n)). UNI-P / APP POST: Gaussian rows, population floor, λ_max free. Proved. | F Thm 1: floor κ on sets of size s + O(log n); Lemma A for the size tail. A1/A2 Thm 1: two-sided sparse eigenvalues on a log sieve; the tail above the sieve is an open gate "(Tail)"; beta-min at log² n / n. | **Ours is stronger and done.** |
| **Size tail above the sieve** (replaces S–L's cap condition, which K = ⌊n/2⌋ violates) | Inside T03♯ as the cutoff m♯_n. Not stated as a separate result. | F Lemma A: design-free, via "expected Bayes factor under the prior predictive equals 1". A1/A2: unresolved. | Same substance. **We lack the presentation**: a standalone design-free lemma is the one new idea relative to Song–Liang and should be visible. |
| **Exact HPM / MPM / PIPs** (Thm S, Thm 3) | SL0, SL1, instances. Proved. Without beta-min: π(S ⊉ J_n(c)) small. | F Cor 1.1; A Thm 2. | Equal. |
| **Hellinger / predictive contraction** (Thm 1–2) | Not proved (scope item 7, frontier F7). | F Cor 1.1(v) and A1 Thm 2: a corollary of π(S₀) → 1 plus fixed-dimensional theory on S₀. | **Missing analog; cheap.** |
| **Start under misspecification** (Thm 4, Cor 2) | C-MIS: projected support under Gaussian residual (GR) or exact projection (EP). Proved-checked. Start sandwich S₀ ⊆ S̃₀ ⊆ Q in GROW / UNI-0. | F Thm 2: "exact reduction" of each block table to a correctly specified regression with inflated variance; screening and consistent-start statements. A Thm 6: fixed-subset projection target. | Ours ahead. F's "exact" holds only under Gaussian rows (see §2.3). **We lack** a start-*mass* statement π₀(S₀) ≥ 1 − n^{-c} (F Thm 2(c)); needed for the sampler theorem. |
| **Reported HPM via LS0** (no S–L analog) | GROW: fixed design, primitive conditions (G1)–(G4), \|Q\| ≤ C log n. PLR / UNI-0: Gaussian rows, \|Q\| ≤ (log n)^κ, locality class, any A. GEN, PXN: masked truths. All proved-checked except UNI-0 (council pending). | F Thm 3: visibility B1 + leakage budget B2 with \|𝓛\| ≤ (1−ε) log n; sketch. A Thm 4: abstract potential-descent theorem; primitive conditions left open and rated high risk. | **Ours well ahead.** F's B1–B2 are close to GROW's (G3b), (G3c), (G1) with a smaller budget. |
| **Reported HPM via start draws / proposals** | None. M5(0) + [OP] bound the discovery failure only by LS0. | A1 Thm 3(a), A2 Thm 3 (D): every π₀ draw and every independence proposal is scored, accepted or not, so P(miss) ≤ E[(1 − π₀(S₀))^{D_n}], D_n = 4N_e(1+T+L+4). | **We lack it.** Cheap; needs ideal uniforms. |
| **Reported PIPs, MPM, evidence as coded** | N1 (unbiasedness, any design). Cor. E: evidence-weighted, in expectation, and by the chapter's own words "not the study's `pip_primary`". M1(i): needs stacking R′_n ≈ 4 log₂(n+p) and osc d = O_P(1); not the coded R′ = 4. | F Thm 4(b): if T²·δ̄_n → 0 (odds off S₀ at both ends of the bridge), then Ẑ/Z → 1, PIPs and MPM consistent, for every N_e, R′ and frozen calibration. A Thm 5: minorisation L/M_n → ∞ or global oscillation; strong. | **We lack an as-coded statement.** F Thm 4(b) is the best value. |
| **Design-free safety net** | None found (grep-level check for a certificate-based screening result). | F Thm 5(a): a sparse, locally certified reported model contains S₀, for any design with a floor on sets of size q_n + s. | **We lack it.** It is the only proposed result that says something about the reported model for factor designs at p ≫ n. |
| **Negative results** | GEN (C6), FAC-A SHARP, FAC-PK NEG, APP VN, OBS-k. Proved. | F Appendix A2 (heuristic multimodality threshold cond < 1 + 1/(2A)). | **Ours only.** Valuable for the paper. |
| **Delivery, implementation premises** | Thm D, Prop. F, Lemma CAP, N3; premise e4 ("LS0 centre is a start-mode maximiser") open. | All three: state P(𝒪 ∩ ·); delivery separate. | Ours ahead; proposals confirm the convention. |

### 1.1 What the proposals have that we lack (ranked by value)

1. **F Thm 4(b), sampler outputs for any frozen schedule.** Three elementary facts (a deterministic lower bound on
   Ẑ/Z, unbiasedness, a Hölder bound on bridge odds). It is about the estimator the code actually reports. Its regime
   is narrow (the start already concentrates on S₀) and F says so.
2. **F Thm 5(a), certified screening.** Deterministic argument plus one uniform noise bound. I re-derived the key
   inequality: a q-sparse model missing a truth has an addition with noiseless gain ≥ nκ²b²_min, against noise
   ≤ Cσ²q log p **[S]**. It needs the floor on sets of size up to q_n + s, which holds for Gaussian rows when
   λ_min(Σ) ≥ c, so compound symmetry and factor designs qualify at any A.
3. **Astra's discovery bound (D).** It gives a reported-model route with no path geometry. Its premise
   N_e·L·π₀(S₀) → ∞ is far weaker than π₀(S₀) → 1, since N_e ≥ max(2500, n, p). It covers many weak leaks of arbitrary
   geometry; LS0 covers few strong ones. The two are complementary **[S]**.
4. **Hellinger / predictive corollary.** Both proposers treat it as routine.
5. **F Lemma A as a named result**, and F's EBIC reading (Appendix A1: penalty/noise = 1 + 1/(2A)). Good exposition
   for the paper; no new mathematics for us.
6. **Astra's reminder about the reported estimator.** `pip_primary` is the equal-weight island mean
   (`v3_run.R:162`). Any theorem about evidence-weighted PIPs describes a different estimator.

### 1.2 What we have that they lack

- A proved posterior theorem for the coded prior, cap and standardisation, with weaker design conditions.
- Leakage sets of polylogarithmic size (PLR, UNI-0), against log n in F and nothing primitive in Astra.
- Masked truths (PXN, GEN, FAC-B FS′), misspecification theorems, the cap-monotonicity lemma, delivery analysis.
- Proved negative results. F only conjectured multimodality; we have GEN (C6) and NEG.
- A dense-start theory for one-factor designs with p < n/2 (see §2.3 for what it is worth).

### 1.3 Contradictions and how they resolve

**(a) Factor designs: "do not claim" (F §5.2) versus W2-FAC-A/B/X and UNI-1.**

Both sides agree on the facts: under a pervasive factor every null is visible to its block, the start mode is dense
(S̃₀ ≈ [p] when p ≤ K), and F's leakage budget B2 fails. They disagree on whether LS0 can still be controlled.

- **W2-FAC is right when the full lattice is feasible.** If p ≤ K = ⌊n/2⌋, the start is a superset of S₀ and LS0 is
  backward elimination from it. Nulls then carry no signal, and the coded cap ℓ_n + |S̃₀| allows paths of length p.
  Proved: one factor with local idiosyncratic part and log p / log n < α₀(κ̄) ≤ 1/6 (FAC-A, UNI-1, Gaussian rows);
  exact-Gram compound symmetry up to p ≤ n/2 (FAC-B); iid compound symmetry up to log p / log n < 1/2 (FAC-X).
  All need k = 1 and non-masking. In this regime F's statement "nothing is controlled" is wrong as mathematics. F saw
  the larger cap in the code but its proof device (one χ² variable of dimension ≤ log n) cannot use it.
- **F's advice is right for the paper's headline regime.** With p > K the start saturates at size K, cannot hold all
  visible nulls, and may exclude truths. Theorem NEG proves that LS0 with the shipped cap never scores S₀ for
  exact-Gram compound symmetry with K < p ≤ n − 1 (liminf p/K > 16/15). For p ≫ n nothing is proved either way; for
  k ≥ 2 nothing is proved at any p, and OBS-k blocks the current technique. NEG is about LS0, not the full method:
  the full-method numerics (P6) are still pending.
- **Resolution for the paper.** "Reported-model consistency under strong factors" is a theorem only for one factor
  and p < n/2, and in design-agnostic form only for p = o(n^{1/6}). It cannot sit under a headline that says
  p ≤ n^A with p ≫ n. Posterior concentration does hold for these designs at every A (UNI-P; both sides agree).

**(b) F Thm 2(a) "exact reduction" versus C-MIS's Gaussian-residual hypothesis.** For a fixed design the unexplained
signal makes ‖(I − P_{C_b})y‖² a noncentral χ², so the block table is not exactly that of a correctly specified
regression **[S]**. It is exact under Gaussian rows, which is C-MIS's (GR). Ours is the correct statement.

**(c) Astra's "(Tail) is unresolved, high risk" versus T03♯ "PROVED".** No contradiction: Astra had not seen T03♯. But
note the asymmetry in §2.1.

---

## 2. Weaknesses of the current program

### 2.1 The spine has the lightest verification

T03♯ carries every other theorem. Its status line is "PROVED; SF/XF VERIFIED; cited archive card", with no council
score; APP L1_POST is "PROVED (by this seat, unchecked)" with one review. Two independent proposers single out exactly
this step (size tail above the sieve, response standardisation, the IG(0.01, 0.01) term, rank-deficient models where
the unit ridge gives less than the full Occam penalty) as the place the package could fail. The middle range
j₀ < |J| ≤ m♯_n, where only the unnormalised floor g₀ is assumed, is where I would look first. Also, the chapter says
Song–Liang's Theorem S "was not inspected"; a paper built on their template must read it.

### 2.2 Assumptions that are not mild or not general

- **Gaussian rows in every Wave 2 reported-model theorem** (PLR, UNI-0, UNI-1, FAC-X). Song–Liang assume moment
  conditions, and all three proposals state fixed-design theorems. GROW already has a fixed-design theorem under
  primitive conditions; Wave 2 moved away from that form.
- **UNI-0's class is a design family with a general name.** Spectrum in [c, C] plus exponential decay along a
  geometry of polynomial growth is a large class (banded, spatial, bounded blocks, graphs of polynomial growth). It
  excludes sparse correlation without geometry (random or expander-like graphs), any diverging eigenvalue, and
  polynomial decay below α = 17/2. It is a good corollary class. It is not an assumption a reader would call
  design-agnostic.
- **UNI-1 fails the dimension goal.** log p / log n < 1/(2κ̄(κ̄+2)) means p = o(n^{1/6}) at best. For heterogeneous
  signed loadings the report's own illustrations give exponents 0.007–0.03. FAC-GL's exponent is about 0.002.
- **PLR is conditional on the algorithm.** Its hypotheses include P(Sand_n(Q)) → 1, a statement about the start mode,
  and the reference/atom conditions (R1)–(R3), which nobody can check for a given X. As Astra put it, a conditional
  interface does not become a mild-design theorem by assuming its hard premises. PLR is a fine engine; it is a poor
  headline.
- **Exact-Gram designs** (FAC-B, FAC-PK, FAC-S5) are deterministic constructions with X′X/(n−1) exactly compound
  symmetric. They are not sampling models, and FAC-B's proof needs log log n ≳ 400.
- **Signal conditions differ across units** for the same design: (TV)/(GC-CS) in FAC-A, (FS)/(FS′) in FAC-B/X,
  (FS-BCS) in FAC-S5, PTV in UNI. "S5 is covered" means different things in different files.
- **The open premise e4** (the emitted LS0 centre is a maximiser of the start law) sits under every reported-model
  theorem and is still open.

### 2.3 Conclusions weaker than achievable

- Nothing in probability about the coded PIPs, MPM or evidence (§1, row 8). Achievable now in the concentrated-bridge
  regime, and conditionally in general (§3).
- No statement at all about the reported model outside the proved classes. Certified screening is achievable for
  every design with a sparse floor.
- No predictive / Hellinger statement.
- The discovery bound uses only LS0, although every proposal and every particle state is also scored.

### 2.4 Routes likely to dead-end

- **Lemma KL for FAC-S5.** Research-grade; the unconditional exponent it would improve (0.104) is already below
  FAC-A's 1/6.
- **k ≥ 2 by the full-lattice route.** OBS-k shows the needed uniform subset information does not exist.
- **Path proofs beyond 1/6 for general loadings** (FAC-XA, S5F). Same global-centre obstruction as S5; one key result
  is "PROVED-CONDITIONAL", another open.
- **Shipped-calibration delivery** (Conjecture P on pilot stage counts) and **M1(i) with stacking**. Neither describes
  the method as coded after the fallback was merged.

### 2.5 Theorems not worth further cost

Already paid, keep as examples in a supplement: PXN (one parametric family with 9 ≤ g ≤ 16), polynomial decay
α > 17/2, LOC-BF, FAC-B, FAC-X Target 1. Not worth finishing: FAC-GL, FAC-S5/S5F, FAC-XA, FAC-K2, FAC-PKA (its
partitions are explicitly non-production). Each would add one row to an examples table, in the regime p < n/2.

### 2.6 The structural weakness

The reported-model guarantee rests on a greedy path. Whether a greedy path reaches S₀ depends on the geometry of
(X, θ*) relative to the method's blocks. That is why each new design needed a new ticket, a new signal condition and a
new exponent ceiling. Continuing by families will not converge to a design-agnostic theorem; GEN (C6) and NEG are
proofs of that.

---

## 3. The sampler-accuracy question

**Question.** Can a sampler-output theorem make reported-model consistency design-agnostic, or is search-based
discovery unavoidable?

**Answer in three parts.**

**(1) Unconditionally, no.** Ŝ⁺ is the best model scored, so Ŝ⁺ = S₀ needs S₀ to be the global maximiser (design-
agnostic, done) and S₀ to be scored. Under a sparse eigenvalue floor alone the second fact is false in general for
this method: GEN (C6) gives P(LS0 misses S₀) → 1 while π(S₀) → 1, NEG gives the same on compound symmetry with p > K,
and F's Appendix A2 predicts stable spurious local maxima whenever the sparse condition number exceeds 1 + 1/(2A).
Tempering does not repair this without a transport argument, and for this prior the available rapid-mixing theory
does not transfer (F §3). So some condition tying X to the method is unavoidable.

**(2) Conditionally, yes, and almost for free [S].** Lemma N1 is proved-checked and has no design assumption:
E[Ẑ_r · (1/N_e) Σ_i h(S_i) | 𝒞] = Z·π(h) for bounded h. Take h = 1{S ≠ S₀} and let A_r be the fraction of island r's
measured particles at S₀. Then E[(Ẑ_r/Z)(1 − A_r) | data, 𝒞] = δ_n := 1 − π(S₀). On {A_r ≤ 1/2} the integrand is at
least Ẑ_r/(2Z), so for any η > 0

> **Lemma LT (lower-tail transfer).** P(A_r ≤ 1/2 | data, 𝒞) ≤ 2δ_n/η + P(Ẑ_r/Z < η | data, 𝒞).

With δ_n = O_P(√(log n/n)) from UNI-P and η_n = n^{-1/2} log n, this gives: **if the evidence estimate does not fall
below n^{-1/2} log n times the true evidence, then with probability → 1 most particles sit at S₀.** That one event
implies S₀ is scored (reported HPM correct), the particle and Rao–Blackwell PIPs are within 1 − A_r of the truth, and
the MPM is S₀, for every N_e, every R′ and every frozen schedule. The premise is scalar, one-sided, and much weaker
than relative consistency of Ẑ. Notes:

- F Thm 4(b) is the special case where the premise is proved, by the deterministic bound
  Ẑ_r/Z ≥ (π(S₀)/π₀(S₀))·Π_t A_{t−1}.
- For a single importance step the premise is equivalent to N_e·π₀(S₀) → ∞ up to logs, which is Astra's condition.
  So LT, F 4(b) and Astra (D) are one family of results.
- The premise has a computable necessary check: Z ≥ Σ over scored models of e^{F}, so Ẑ_r far below the ledger sum
  flags a failed run. This is a diagnostic, not a guarantee.
- Proving the premise from conditions on X beyond the concentrated bridge is the SMC stability problem. I would fund
  at most a three-day exploratory ticket for the sandwich regime (bridge confined to supersets inside Q), not more.

**(3) So what carries the paper.** Search remains the only route to an *unconditional* reported-model theorem with
primitive conditions, and those conditions must be stated relative to the method's blocks (visibility and leakage).
The sampler gets a real place through LT and F 4(b). The paper then states one transfer identity and three sufficient
discovery mechanisms: LS0 (few leaks of any strength, deterministic), draws and proposals (start mass ≥ n^{-1+ε}, no
geometry), and non-collapsing evidence (general, conditional).

---

## 4. Recommended theorem package

Presentation rule: assumptions are conditions on (X, θ*); no design family appears in a theorem statement. Families
appear only in an examples table.

| # | Theorem (sketch) | Assumptions | Status | Effort |
|---|---|---|---|---|
| **1** | **Posterior concentration.** 1 − π(S₀) = O_P(√(log n/n)); exact HPM = MPM = S₀; PIPs consistent. Without beta-min: no false positives and recovery of strong signals. Random-design version under a population floor (λ_max free). | Gaussian errors, fixed s₀, p ≤ n^A, bounded signal, sparse floor on S₀ ∪ J (\|J\| ≤ j₀ normalised; up to m♯_n unnormalised), beta-min ≍ log n / n. | Proved (T03♯, UNI-P, SL0/SL1). Needs one independent adversarial re-check. | 2–3 |
| 1a | **Size-tail lemma**, stated on its own: models above the cutoff m♯_n carry negligible posterior mass with no condition on X. | Model, p ≤ n^A, bounded signal. | Inside T03♯; extract and state. Compare with F Lemma A's martingale route. | 1 |
| 1b | **Predictive / Hellinger corollary** (S–L Thm 1–2). | As Thm 1. | New; low risk. | 2–3 |
| 1c | **Enumeration branch**: every output is exact when the coded enumeration test passes. | Coded inequality (EXB). | Proved (APP ENUM). | 0 |
| **2** | **Start and misspecification** (S–L Thm 4, Cor 2). Block tables learn the projection of the mean on the block, with diluted noise; the start mode satisfies S₀ ⊆ S̃₀ ⊆ Q; with no leakage, π₀(S₀) ≥ 1 − n^{-c}. | Visibility (V); leakage set Q (L); Gaussian residual for the exact projection statement. | Proved: C-MIS, sandwich (GROW C3, UNI-0). **New: the start-mass rate.** | 2–3 |
| **3** | **Reported model.** P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, for every seed, N_e, R′ and calibration outcome; LS0 deletes the leaks one at a time. | Thm 1 plus two primitive conditions on (X, θ*): **(V)** no truth is masked by ≤ 15 conditioning variables; **(L)** a deterministic set Q ⊇ S₀ of size ≤ C log n (fixed design) or (log n)^κ (Gaussian rows) outside which no column gains more than η σ² log n. | Proved: GROW (fixed design, log n), PLR / UNI-0 (Gaussian rows, polylog; council pending). **Work: restate in the (V)+(L) form, partition-free where possible; close premise e4.** | 4–5 |
| **4** | **Sampler outputs as coded.** (a) Unbiasedness for any design. (b) Lemma LT: non-collapsing evidence ⇒ reported HPM, PIPs, MPM consistent. (c) Concentrated bridge (F Thm 4(b)): under Thm 2 with no leakage, Ẑ/Z → 1 and `pip_primary`, MPM consistent, any frozen schedule. (d) Draw discovery (Astra (D)): P(miss) ≤ E[(1 − π₀(S₀))^{D_n}]. | Ideal uniforms, invariant kernels (N1 premises); (c) needs the start-mass rate of Thm 2. | (a) proved-checked. (b) new, very low risk. (c) new, low–medium. (d) new, low; needs a code check that rejected proposals reach the ledger. | 5–6 |
| **5** | **Certified screening.** P(𝒪 ∩ {certified} ∩ {\|Ŝ⁺\| ≤ q_n} ∩ {S₀ ⊄ Ŝ⁺}) → 0. Both conditions are printed by the method. | Floor on sets of size q_n + s₀, q_n = o(n/log n); fixed coefficients. No condition on the start or on leakage. | New (F Thm 5(a)); low–medium. Must match the coded meaning of `local_certified` and which model it refers to. | 3–4 |
| **6** | **Limits.** GEN (C6): LS0 can miss S₀ while π(S₀) → 1. NEG: on exact-Gram compound symmetry with K < p ≤ n − 1 the shipped LS0 never scores S₀ (a statement about LS0, not the full method). SHARP and OBS-k as remarks. | As in sources. | Proved. | 1 |
| Ex. | **Examples table.** Local designs (AR, banded, spatial, bounded blocks) verify (V)+(L) at every A (UNI-0). One factor with p < n/2: FAC-A / UNI-1 (p = o(n^{1/6})), FAC-B, FAC-X. Masked hubs: PXN. Each with its own signal condition named. | — | Proved (UNI-1 council pending). | 2 |

**Keep:** T03♯/UNI-P, SL0/SL1, C-MIS, GROW, PLR, UNI-0, N1, Lemma CAP, the negative results, ENUM.
**Demote to examples:** UNI-1, FAC-A, FAC-B, FAC-X Target 1, PXN, LOC-BF, polynomial decay.
**Replace:** M1(i) with stacking and Cor. E as the PIP statement → Thm 4(b)–(c). PLR as the headline → Thm 3 in the
(V)+(L) form with PLR as its engine. Delivery theorems → one remark: results are stated as P(𝒪 ∩ ·); unconditional
versions hold under the fallback and a growing resource allocation.
**Drop from the paper:** FAC-GL, FAC-S5 reduction, SL2 store-restricted PIPs (supplement at most), the shipped-
calibration delivery analysis.
**Add:** 1a, 1b, the start-mass rate, 4(b)–(d), 5, 6.

The one-sentence scope the paper can then defend: *for sparse Gaussian regression with p ≤ n^A and a sparse eigenvalue
floor, the coded posterior concentrates on the true model; if no truth is masked and all but polylogarithmically many
columns are negligible to the method's blocks, the reported model is the true model for every seed; if in addition
nothing leaks, the reported PIPs, MPM and evidence are consistent; for any other design with the floor, a sparse
certified reported model contains the true model.* This is F's sentence with our stronger middle clause.

---

## 5. Order of work (three weeks) and stop list

**Week 1 — close and de-risk.**
1. Finish the W2-UNI council as locked. Do not widen it.
2. Independent adversarial re-check of T03♯, with the focus list of §2.1. Read Song–Liang's Theorem S.
3. Lemma LT and the draw-discovery bound (Thm 4(b), 4(d)): statement, proof, code check of the ledger.
4. Run P6: the full method on compound symmetry and a two-factor design at p > K and at p ≫ n. This is the only open
   item that can change a paper claim (decision D1).

**Week 2 — the new theorems.**
5. Start-mass rate (Thm 2) and the concentrated-bridge theorem (Thm 4(c)).
6. Certified screening (Thm 5).
7. Predictive / Hellinger corollary (1b); size-tail lemma extracted (1a).
8. Close premise e4 by a code-level proof for the tie-aware start-mode DP.

**Week 3 — assemble.**
9. Rewrite the reported-model theorem in the (V)+(L) form; examples table with one signal condition per row; limits
   section.
10. Chapter v2.0 through council. Optional three-day exploratory ticket: evidence lower tail in the sandwich regime.

Total new proving effort ≈ 20–25 agent-days; nothing in it is research-grade.

**Stop now.**
- FAC-S5 (Lemma KL), FAC-S5F, FAC-XA, FAC-K2, FAC-PKA, FAC-X Target 2 (FAC-GL).
- Any work to raise exponents in the regime p ≤ K (1/6, 1/2, 0.104).
- Polynomial-decay and LOC-BF extensions.
- Shipped-calibration delivery (Conjecture P) and M1(i) stacking.
- New design-family tickets of any kind until D1 and D2 are decided.

Keep running: W2-SIM and P6 only.

---

## 6. Decisions for Felipe

Only items that change what the paper claims.

**D1. Strong-factor designs at p ≫ n.** Options:
- (a) *Recommended now.* Claim posterior concentration and certified screening for them; show the one-factor,
  p < n/2 results as examples; state NEG as a limit.
- (b) Change the cap to ℓ_n + 2|S̃₀| (the FAC-PK proposal). It is proved only for exact-Gram compound symmetry with
  K < p ≤ n − 1, doubles LS0's worst-case charge (already ≈ 146 h at n = 600, p = 450 in the preflight), and leaves
  p ≫ n open. I would not adopt it before P6 shows the full method actually fails.
- (c) Change the method to remove estimated factors before selection, so the residual design is local and UNI-0
  applies for any number of factors and any A **[S]**. This is a real method change with its own theory.

**D2. Form of the headline reported-model theorem.** Primitive conditions on a fixed design (visibility + bounded
leakage, with locality as the main example), or structural classes for Gaussian rows (UNI-0, UNI-1) as "the main
theorem". I recommend the first; the second reads as two design families.

**D3. Claims about PIPs, MPM and evidence.** Today the paper can claim none in probability for the coded estimator.
Adding Thm 4 lets it claim consistency (i) where the start already concentrates on S₀, labelled honestly, and
(ii) conditionally on non-collapsing evidence. Decide whether the paper makes these claims and whether the ledger-sum
check is reported as a diagnostic.

**D4. Certified screening and one optional method change.** Thm 5 makes a guarantee conditional on two printed flags.
F notes that if the method also *reported* the best subset of a sparse certified Ŝ (its certificate already
enumerates them), exact selection would follow for every design with the floor, on that printed event. That is a
method change.

**D5. UNI-1's place.** It was commissioned as half of the design-agnostic main theorem. I recommend presenting it as an
example with its exponent stated plainly (p = o(n^{1/6})), not as a main theorem.

---

## 7. Limits of this critique

- I verified no proof. Where I call something "proved" I am quoting its status file.
- Lemma LT, the re-derivation behind Thm 5, the complementarity claim for draw discovery, the remark on F Thm 2(a),
  and option D1(c) are mine and unchecked.
- I read the chapter and most Wave 2 reports through helper inventories, so a qualification in those files may have
  been lost. The claims that matter most for the recommendation (UNI-1's exponent, NEG's scope, the PIP gap, T03♯'s
  status) I confirmed in the source files myself.
- BLIND_fable was written by the same model as this critique. I have tried to weigh it as I did the others; where I
  side with it (Thm 4(b), Thm 5(a)) the reason is given, and where it is wrong (§1.3(a), (b)) I say so.

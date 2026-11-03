# THM-INV: inventory of the method and its theory, against the goal and the literature

Branch `theory/THM-INV`. Run on 2026-11-03 (Opus 5.5; digest workers Sonnet). **No new proofs.** This is a stock-take.
Every status below is copied from its source and is never upgraded. "Candidate" means AI-proved, not reviewed for adoption, and not adopted.
Working material is in `digests/`: REG (registry, T38, architecture), API (nine API reports), AREV (Astra A-REV5..9), LIT (five LIT reports + API-POS), SL (Song–Liang 2015), LITGAP (new primary-source pass).
Those digests were written by worker agents and spot-checked by me, not line-checked. Where this report and a digest differ, the source branch file is authoritative.

## 0. Headline

1. **Selection accuracy has the most theory.**
   - The statistical half is PROVED-LOCKED, but only asymptotically: T01–T03, plus T03♯ VERIFIED cross-family.
   - The composition is PROVED-LOCKED: T21 (CONDITIONAL), with Thm N200 PROVED for the algorithm as run at every n.
   - The masked-regime consistency of the *reported* HPM has two verified routes:
     - with LS0 (Thm 5(b1), A-REV8 VERIFIED), which is a method change absent from the production core;
     - with no LS0, but only on an exact-Gram LH subfamily (B2-LH + STAB-LH, A-REV7 + API-VSTAB VERIFIED).
   - Neither covers the study's generator (groups of 5), finite n, or P(no output) → 0.
2. **Posterior accuracy (objective 1) is thin.**
   - Ẑ has unbiasedness, the islandwise identity and the Markov lower bound. These are PROVED-LOCKED, but the LIT reports say they are textbook (KNOWN—CITE).
   - Ẑ's relative accuracy is a CONJECTURE (favourable regime only); in the masked regime only a lower-tail mechanism is PROVED.
   - PIP accuracy is CONJECTURE (T26) or holds only on LH at fixed p.
   - **Joint inclusion probabilities and general posterior expectations E_π[h(S)] as n grows have no theorem at all.** Proposal §13.1 asks for exactly this.
3. **Parallel scalability (objective 2) has no theorem.**
   - There are cost bounds: T32(i) gives a polynomial score count, and Theorem G and O-STAGES bound the stage count.
   - There is no statement of work/depth versus p and correlation, no island-count theory beyond standard pooling, and no comparison of depth with sequential MCMC.
   - **The thesis sentence ("correlation costs only depth and particles, never correctness") is not a theorem yet.** Its "never correctness" half is fixed-data Monte Carlo validity (KNOWN—CITE), and its "costs only depth" half is unproved.
4. **Against Song–Liang we exceed on every theorem type except the parallel-cost analysis (§6), which we lack in comparable form.** We also lack their weak-condition posterior contraction in Hellinger distance.
5. **Literature.**
   - Of the proposal's five themes, *composite likelihood / posterior calibration* and *diagnostics for scalable computation* had no LIT coverage.
   - A primary-source pass (10 works, all verified) finds no precedent for using a composite/block-product posterior as an *SMC start that is then corrected exactly*.
   - Chatterjee–Diaconis (2018) supplies the right cost scale exp(KL(π‖π₀)) for a one-shot correction.

## 1. Component map

Legend: **V** = validity (the target is right / the estimator is unbiased or invariant), **A** = accuracy (error → 0 or bounded), **C** = cost, **F** = failure-mode characterisation.
Status words as in the sources (registry/REG digest, API, AREV). **NONE** = no theorem of any status. "Idealised" = holds for a variant (frozen calibration, iid final draws, LS0, exact Gram, fixed p, ideal grid), not the production run.

| # | Component (METHODOLOGY_v3 §) | V | A | C | F | Properties with NO theorem |
|---|---|---|---|---|---|---|
| 1 | Target posterior (§5; g = n, IG(.01,.01), BB(1,p), cap ⌊n/2⌋) | Reduction V1 / T01 PROVED-LOCKED | T02, T03 PROVED-LOCKED; T03♯ PROVED, XF A-REV2 VERIFIED; asymptotic (onset n ≳ 2·10⁶; SE impossible at n = 200). N200 Prop 2: lower bracket on Π(X) PROVED | — | T07 (size-only prior cannot fix a same-size swap) PROVED-LOCKED; API-POS Prop U (no underfitted local modes on LH) PROOF SKETCH | **Finite-n upper bound on Π(X)** (OPEN, API-N200); posterior contraction / coefficient rates (V3) NONE; growing s₀ NONE |
| 2 | Exact branch (§6.2) | by construction (enumeration) | V2–V4 apply directly | branch threshold is explicit | W2-T26 exact-branch remark ERROR (A-REV5) | — |
| 3 | Blocks / partition (§6.3: complete linkage, cut, next-fit packing) | — | W7-PART Thm B (partition = groups on SIZE g ≤ B < 2g, LH-iid) PROVED, VERIFIED* A-REV6/A-REV9; explicit constants GAP | tables ≤ p·2^B/B scores (by count) | PART-CE2: unequal groups not merged (COUNTEREXAMPLE) | **Partition law for the study's packing (groups of 5, 2g ≤ B)** NONE (A-REV6); correlation-adaptive blocking; random/overlapping partitions NONE |
| 4 | Composite start π₀ (exact Z̄₀, iid draws) | exact sampler and normaliser: by construction (V5 target; no registry theorem found (?)) | T22(i)(ii)(iv) PROVED-LOCKED (deterministic mass on a reference); T22(iii) favourable rate CONDITIONAL (EXP′ PROVED, XF VERIFIED* fixed design); FAV-ThmB PROVED (author only) | — | T27(i) masking law PROVED-LOCKED, CONDITIONAL (Thm3/4-EXP XF VERIFIED); DIL-E/E1/R/N (dilution, the study's actual mechanism) PROVED, XF VERIFIED; SEP-A/B (start-only / one-shot reweighting needs p^c n^{c/2} draws) PROVED, XF VERIFIED | Start quality for random designs with adaptive packing; backfit start (API-RESID) NONE |
| 5 | Bridge γ_φ = γ₀e^{φd} and schedule (§6.3, 6.6) | each stage targets γ_φ exactly (by construction) | T22(iv) (bridge never loses S₀ mass below the smaller endpoint) PROVED-LOCKED; OWS weight-stability WS1–WS8 PROVED (no review), W(a–f) XF VERIFIED under H-ORTH | Theorem G (stage count = pilot + ⌈log₂1/η⌉) PROVED, deterministic, as-run rule (API-T26BUD, candidate); STG-M (log₂A₀ stages for a crossing, ideal two-state grid) PROVED, XF VERIFIED*; one-stage regime Thm 1 PROVED (favourable only) | Lemma J (an ESS-0.9 step cannot be blind to a mode) PROVED | **Realised stage count T_n in the masked regime** (O_P(1) OPEN; Conjecture P); depth as a function of correlation NONE |
| 6 | Move kernel (Gibbs, swaps, neighbour swaps, independence; random order) | reversibility and self-adjointness: by construction, consultant-checked (V5), no registry row (?) | Masked discovery: Thm B-T24 PROVED (vacuous at n = 200); BG3 PROVED, XF VERIFIED (fixed p); B2-LH PROVED-UNDER STAB-LH, XF VERIFIED (exact-Gram LH subfamily, no LS0) | — | General LH locking FALSE (A-REV7 counterexample); H24 retired (CE1/CE2 COUNTEREXAMPLE) | **Mixing / spectral gap of the φ = 1 round (V10)** NONE; YWJ/ZYVR do not apply to the paper's prior (API-POS PROOF SKETCH; LIT-MCMC Prop OB sketch) |
| 7 | Calibration, candidate set V, grid rebuilds, tiers, escalation (§6.7–6.9) | final run independent of calibration (frozen before final randomness): T12 frozen-run identities; IND-T PROVED, XF VERIFIED* (A-REV1 only) | Masked Ẑ lower tail decided by the crossing temperature: MASKZPIP E1/E2 PROVED (candidate); "resolved grid ⇒ O_P(√(T/N))" (V11) CONJECTURE, OPEN for c ≥ 2 | Theorem G; Rule CAP (method change) PROVED | E1c: island agreement uninformative when the grid is blind (PROVED) | **Rebuild-loop convergence** NONE; probability of `schedule_limit` / `grid_unconverged` NONE; whether V contains the competing pair NONE |
| 8 | Islands and pooling (R = 4 final; independent streams) | Prop 2(a,b,d,e) islandwise E[Ẑ_r PIP̂_rj] = Z·PIP_j PROVED (XF A-REV4 GAP on output Markov wording); Prop 2(c) pooled product is not an identity PROVED; IND-T audit HOLDS | Ẑ-weighted pooling is consistent as R → ∞ at fixed N: standard (Dai et al. 2022; LIT-PAR TH2) | — | — | **Parallel speed-up / work–depth theorem** NONE; choice of R vs N NONE; island variance vs correlation NONE |
| 9 | Ẑ and 0.05·Ẑ lower bound (§6.12) | T12 E[Ẑ_r] = Z PROVED-LOCKED; T31(i) Markov bound PROVED-LOCKED; OPW2-ThmA/B relative variance PROVED, XF VERIFIED* (frozen calibration) | Favourable: T26-ThmA/B PROVED / PROVED-UNDER (realised T_n not controlled); Thm 6 overall CONJECTURE. Masked: only the lower-tail mechanism E1/E2; top-store Z_T sandwich P3 PROVED | — | Ẑ underestimates by the log-odds overshoot of a late switch (E1a PROVED); per-fit certificate Ẑ < Z_T ⇒ underestimate (C1 PROVED) | **Two-sided relative accuracy of Ẑ in the masked regime** NONE (an upper bound on Z is impossible from a run, MASKZPIP); floating point: VAL-FP MEASURED at p ≤ 40 only |
| 10 | PIPs (Rao–Blackwellised; equal-weight primary, Ẑ-weighted secondary), MPM (§6.11) | islandwise identity (T12/Prop 2); ADRAFT-ThmA/uniPIP (fixed-data N → ∞ consistency) PROVED (Astra author, Astra check) | T26(ii) CONJECTURE (favourable); MASKZPIP P1 (bias ≤ TV) PROVED; P2 composition PROVED (needs locking, LH fixed p); P3 top-store PIP^T PROVED (deterministic) | — | O-CERT: π(S₀) ≤ 0.37 even on correct fits at n = 200 (empirical) | **Joint inclusion probabilities** NONE; **equal-weight PIP accuracy at fixed R** NONE; credible-set / coverage NONE (rejected as a target) |
| 11 | HPM (best ever scored), near ties, decision (§6.10) | T07 Bayes rules PROVED-LOCKED; T21(C1) PROVED-LOCKED, CONDITIONAL; N200 (every n, as run) PROVED | T38(0) composition PROVED, XF VERIFIED; Thm 5(a) PROVED-UNDER (favourable, iid draws); (b1) LS0 PROVED-UNDER, XF VERIFIED; (b1-LH-iid) p ≫ n PROVED (candidate), XF GAP; (b2-LH) no LS0 PROVED-UNDER STAB-LH, XF VERIFIED | T32(i) polynomial score count PROVED (XF GAP on qualification) | N200 lower bound; OSWAP posterior-miss theory (T4, P5 PROVED; P1–P3 XF GAP) | **P(U) → 0 (output delivered)** NONE; **finite-n discovery bound for the Gibbs route** OPEN; study generator (groups of 5) NONE |
| 12 | Local search, `local_certified` (§6.10) | Theorem A (exact greedy repair) PROVED, XF VERIFIED*, Lean sorry-free; LS-score (with LS0) PROVED, XF VERIFIED* | ThmB-T37(incl) finite-n union bound PROVED; ThmW PROVED (candidate) | ≤ (ℓ+1)(p + K(p−K)) scores (count) | Literal T37/TD fails generically (Prop1-TD, CEX1/2); region-form Theorem W fails on masked LH c ≥ 2; data: 0 moves in 2,394/2,394 | Meaning of `local_certified` beyond "no improving neighbour" (V12) NONE positive; LS0 absent from production (API-AUDIT) |
| 13 | Flags and diagnostics (E1–E3, ESS, grid flags) | — | — | — | V12 (checks fail to fire with non-crossing kernels) is the only theory, all negative; MASKZPIP E1c; O-CERT C1–C6 per-fit certificates (some XF ERROR) | **Any positive power result (a flag fires when the output is wrong)** NONE; ESS/k̂/coupling diagnostics not analysed (§4) |
| 14 | Resource limits, statuses, GUARD, numerics (§2, §6.13, §8) | Lemma RO run/output split PROVED, XF VERIFIED; GUARD implementation fact HOLDS (literal "every output equals" ERROR, A-REV8) | — | T32(i); Cost-T38 PROVED-UNDER | CEX-guard COUNTEREXAMPLE (path-dependent stopping biases Ẑ); `fit$log_Z` hazard on stopped fits (API-AUDIT) | **P(resource_limit), P(schedule_limit), P(numerical_failure)** NONE (V13); floating-point error theorem NONE |

**Observations.**
- Nearly every positive theorem about the *algorithm* (rows 5–12) is either idealised or about a design the study did not use. The idealisations are a frozen calibration, iid final draws, an ideal grid, LS0, exact-Gram LH and fixed p. The study's designs (groups of 5, p ≫ n) are uncovered.
- The only results that hold for the algorithm exactly as run, at every n, are bookkeeping:
  - T07, T21(C1), N200 Lemma 1 and Thm N200, Theorem G;
  - the T12/T31 identities, given the frozen calibration;
  - Lemma RO and the per-fit certificates.

## 2. Theorem ledger

Columns:
- **Status:** as in REGISTRY_v2 / THEORY_PRIORITIES / API reports. XF = cross-family (Astra) verdict; SF = same-family.
- **Run:** AR = for the algorithm as run (under exact arithmetic, EX-A, and the potential-run convention); ID = idealisation, with the variant named.
- **Lit:** the verdict from the LIT reports (see `digests/LIT.md` §1), with the citing source. ⚑ = novelty challenged by a LIT report; ⚔ = the reports disagree.

| Paper slot | Result | Status (verbatim) | Key hypotheses | Run | Lit verdict (source) |
|---|---|---|---|---|---|
| Thm 1 | T01–T03 / T03♯ selection consistency; T02(i♯) BB(1,p) exact tail | T01–T03 PROVED-LOCKED; T03♯ PROVED, SF W2-VT03R + XF A-REV2 VERIFIED; onset sentence ERROR (repaired) | G, R, SE, BM-∞ (or BM-C), s₀ fixed, p ≤ n^A | algorithm-free (true posterior) | ⚑ MODEST EXTENSION of Rossell 2022 (Bayesian Anal. 17(2)) and Moreno–Girón–Casella 2015 (LIT-STAT). ⚔ LIT-VENUE: "standard in kind … do not sell it" (YWJ 2016 Thm 1; Shin–Bhattacharya–Johnson 2018) |
| Thm 1 / Thm 4 | T03♯(3): P(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] (the 2E₀δ₁ term) | PROVED | as T03 | algorithm-free | ⚑ KNOWN—CITE: "Rossell (2022) Proposition 1 verbatim" (LIT-STAT) |
| Thm 1 (remark) | Prop D (duplicate columns; cut-off growth lower bound) | PROVED (author = verifier) | — | algorithm-free | no analogue found (LIT-STAT) |
| Prop 1 | T07 HPM / MPM Bayes rules; size-only prior ceiling; T06(i) ties | PROVED-LOCKED; XF A-REV4 VERIFIED* (data paragraph ERROR, relabel pending) | true posterior | algorithm-free | ⚑ STANDARD OR FOLKLORE: Barbieri–Berger 2004 Thm 1; Scott–Berger 2010 (LIT-STAT) |
| Thm 2 | T22(i)(ii)(iv) deterministic start mass, odds, bridge mass | PROVED-LOCKED | none (deterministic) | AR (production start) | block start: Papaspiliopoulos–Rossell 2017 (Biometrika) is the nearest precedent, a "threat to novelty of the start"; it is exact only for block-diagonal XᵀX (LIT-PAR, LIT-VENUE) |
| Thm 2 | T22(iii) favourable rate (EXP′, Thm6-EXP; FAV-ThmA/B 2^B-free) | PROVED-LOCKED, CONDITIONAL; EXP′ XF VERIFIED* (fixed design; random design/packing GAP); FAV-* PROVED (author only) | EXP′, VIS, NL_η, NL_avg | AR start, but needs favourable design (1/2,394 study fits) | NEW: "no prior art found" (LIT-STAT G2) |
| Thm 2 | T27(i) masking law π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (Thm3/4-EXP); DIL-* dilution; SEP-A/B | T27(i) PROVED-LOCKED, CONDITIONAL (H2, H3); Thm3/4-EXP XF VERIFIED; DIL-E/E1/R/N XF VERIFIED, DIL-DM(i) ERROR; SEP-A/B XF VERIFIED | LH chain (H2, H3); study tables (DIL) | AR start law (iid start draws only, "not a lower bound for the method") | NEW: "strongest novelty claim" (LIT-STAT); "nobody proves a natural exactly-sampleable start fails and then which moves fix it" (LIT-VENUE G3). Framing: Woodard–Schmidler–Huber 2009 low persistence (LIT-SMC) |
| Thm 2 / Thm 5 input | W7-PART Thm A/B partition = groups | PROVED (author only); XF A-REV6 VERIFIED* on SIZE, A-REV9 B-exact VERIFIED, explicit constants GAP; CE2 COUNTEREXAMPLE | LH-iid, g ≤ B < 2g | AR clustering rule, ID design | not assessed |
| Thm 3 | Theorem A (exact greedy repair, T37(i) refined) | PROVED; SF VERIFIED; XF A-REV2 VERIFIED*; cap-free lattice restatement ERROR (A-REV5); Lean sorry-free | TD′ / D_S margins | AR local search (centre = HPM) | ⚑ "unsurprising given YWJ/ZYVR" (LIT-SMC); must cite Gamarnik–Zadik Thm 2.7 and YWJ Lemma 4 (LIT-MCMC); deterministic exact finite-n is the difference |
| Thm 3 | literal T37 / TD; H24 (T24 route (e)) | Prop1-TD, CEX1/2 COUNTEREXAMPLE (retires literal T37); CE1/CE2 COUNTEREXAMPLE (retires H24) | — | — | — |
| Thm 3 (alt.) | Thm B-T24 Gibbs-path repair; ThmW / PGD family; LH-LAT | ThmB PROVED, XF VERIFIED(*) (vacuous at n = 200); ThmW PROVED (candidate), region form fails on masked LH c ≥ 2; LH-LAT PROVED, XF VERIFIED* | terminal Gibbs rounds; exact Gram | ID (asymptotic) | "outside that literature" (LIT-SMC G1); a hitting-time theorem under (1b)/(1c) only is not published: CONJECTURE (literature), medium (LIT-MCMC) |
| Thm 4 | T21(C1) composition; Lemma RO; GUARD | T21 PROVED-LOCKED, CONDITIONAL; Lemma RO XF VERIFIED; GUARD implementation fact (literal claim ERROR) | H03, H10, exposure; SR, GUARD | AR | split: the 2E₀δ₁ term KNOWN (Rossell Prop 1); the "never scored" term is elementary, not stated for best-ever-scored HPM (LIT-STAT); idea informally in García-Donato & Martínez-Beneito 2013 §4 (LIT-VENUE) |
| Thm 4 (finite n) | Thm N200 and Lemma 1 (posterior miss Π(X) + search miss) | PROVED (elementary, author only); Π(X) upper bound OPEN | EX-A only | **AR, every n** | MEDIUM threat (LIT-VENUE); Hou–Wang–Atchadé arXiv:2407.20580 Thm 2 threatens "first finite-n" wording |
| Thm 5 | T38(0) composition, (0_H) | PROVED; XF A-REV1/5/8 VERIFIED | strict output 𝒪 | AR | — |
| Thm 5 | T38(a) favourable | PROVED-UNDER (F) | iid final draws, EXP′ | ID (iid draws) | TH6: a BVS instance of the Mathews–Schmidler 2024 (AAP 34(1B)) template; "cite it" (LIT-PAR) |
| Thm 5 | T38(b1) LS0 route; (b1-LH) exact Gram; (b1-LH-iid) p ≫ n (API-PXNGAP) | (b1) PROVED-UNDER (M1)–(M3), XF A-REV8 VERIFIED; (b1-LH) PROVED (candidate), XF VERIFIED; (b1-LH-iid) PROVED (candidate), XF GAP (A-REV3/6/8) | LS0; LH; g ≤ B < 2g | **ID: LS0 is not in production** (API-AUDIT) | ⚑⚔ "Novel for the paper's target and method; a corollary of YWJ/ZYVR/Chang–Zhou under *their* prior" (LIT-MCMC); "no SMC-BVS paper has an output theorem" (LIT-VENUE G1). API-POS vs LIT-MCMC: see note D1 |
| Thm 5 | T38(b2-LH) no-LS0 masked consistency (B2-LH + STAB-LH) | PROVED-UNDER STAB-LH; XF A-REV7 VERIFIED; STAB certificate Astra-authored, Claude-VERIFIED (API-VSTAB) | exact-Gram LH subfamily, p ≤ n − 1, g ≤ B < 2g, frozen grid | **AR method (no LS0)**, ID design | as above |
| Thm 5 | BG3 (abstract lock), LH-lock; F1/F2; SEP-GU | BG3 PROVED, XF VERIFIED; LH-lock XF VERIFIED conditional fixed p; **general LH locking FALSE** (A-REV7); F2 GAP, Lemma 3.4 ERROR; GU XF VERIFIED* as a greedy theorem | fixed p; strict C1–C3 | AR method, fixed-p component (production enumerates at fixed p) | — |
| Thm 5(c) | T32(i) score count; Cost-T38 | PROVED; XF A-REV5 GAP (keep qualification); Cost-T38 PROVED-UNDER | — | AR (code-to-count) | ⚑ "not a selling point; do not headline cost" (LIT-VENUE); "polynomial-time recovery on LH is not new" under their priors (API-POS) |
| Thm 6 | T26-ThmA/B, Lemmas 1–3 (Ẑ, PIP consistency, favourable) | T26 overall CONJECTURE; ThmA PROVED, XF VERIFIED*; ThmB PROVED-UNDER; PropC PROOF SKETCH | (T_n+1)Δ_n → 0 (holds in 1/56 runs at n ≤ 3,200), EXP, SE | ID: frozen run; favourable only | ⚔ LIT-SMC: "no analogue"; LIT-VENUE: "standard pattern" (Dau–Chopin 2022 CLTs + concentration) |
| Thm 6 (P1) | Theorem G stage count; Thm 1 one-stage; Rule CAP (API-T26BUD) | Theorem G PROVED (deterministic, as coded); Thm 1 PROVED given inputs; Prop O PROOF SKETCH; Conjecture P | S₀ ∈ V | AR rule | ⚑ G(i)/Lemma 1 = Štefankovič–Vempala–Vigoda 2009 (J. ACM 56(3)): "present G(i) as known" (LIT-SMC; this is for O-STAGES G(i), and applies to T26BUD's count by analogy (?)) |
| Thm 6 / Prop 2 | O-STAGES STG-M (masked crossing T* = log₂A₀ + O(1)), STG-F; item 4 dense limit | STG-M PROVED, XF VERIFIED* (ideal two-state grid) | ideal exact-frontier grid | ID | STG-M: "plausibly new, elementary" (LIT-SMC); item 4 KNOWN: Syed–Bouchard-Côté–Chern–Doucet arXiv:2408.12057 Thm 3 (LIT-SMC, LIT-PAR agree) |
| Prop 2 | T12 E[Ẑ_r] = Z, islandwise E[Ẑ_r PIP̂_rj] = Z·PIP_j; T31(i) Markov 0.05·Ẑ | PROVED-LOCKED (wave 1); XF A-REV4 GAP on output-Markov wording | frozen calibration, potential run | ID: frozen calibration (the method freezes it by design) | ⚑ KNOWN—CITE: Whiteley–Lee–Heine 2016 §5.1; Dai–Heng–Jacob–Whiteley 2022 eq. (4.8); Grosse–Ghahramani–Adams 2015 (Markov). Only the negative items (pooled × pooled is not an identity; E[Ẑ \| completed] ≠ Z) are "genuinely non-standard" (LIT-SMC) |
| Prop 2 | Prop 2(f) VAL-FP | PROVED-UNDER; XF A-REV4 GAP; API-AUDIT MEASURED (p ≤ 40) | floating-point contract | AR, small p | — |
| Prop 2 / Thm 6 | O-PW2 Thm A (exact variance identity), B, C | A PROVED, XF VERIFIED; B, C PROVED (B XF VERIFIED* with fixed inputs only) | frozen calibration | ID | ⚑ A: "same kind as Cérou–Del Moral–Guyader 2011 Thm 1.4" (AIHP 47(3)), unchecked; B/C "may carry novelty" (LIT-SMC) |
| Masked Ẑ / PIP | MASKZPIP E1/E2 (lower tail), E4 dichotomy, P1–P3, C1–C3; F-MASKPIP M1–M3 | E1/E2, P1, P3, C1 PROVED (candidate); E4 resolved half CONJECTURE; M1/M2 XF VERIFIED, M3 ERROR | frozen calibration, one island | ID (frozen) / per-fit AR (C1, P3) | "outside all general bounds (μ⋆, mixing)" (LIT-SMC) |
| Remark | Prop M (naive merge of block fits fails); FD-NM | Prop M: SHARE-M(b) ERROR (A-REV3/6); FD-NM ERROR, repair pending | — | — | ⚑ "known phenomenon … for motivation, not a contribution"; refutes a naive union, **not** Song–Liang (LIT-STAT) |
| Remark | O-WSTAB WS1–WS8 weight stability; FD-W1, FD-W(a–c) | WS PROVED (no review); W(a–f) XF VERIFIED under H-ORTH; WS6e CONJECTURE; WS8d OPEN; FD-W1 XF VERIFIED | H-ORTH, ideal grid, IID idealisation for WS8 | ID | not assessed by any LIT report |
| Suppl. | O-CERT C1–C6, Lemma M (per-fit certificates) | Lemma M, C3, C4 PROVED, XF VERIFIED; C1 ERROR as quantified; C5 ERROR (tie prose) | — | AR (scored set) | NEW "in kind", medium; BVS stochastic-search literature not searched (LIT-SMC G5) |
| Suppl. | ADRAFT-ThmA/CorA1/uniPIP (fixed-data N → ∞ consistency of SMC estimators) | PROVED (Astra author; Astra check only) | EX-A, EX-S | ID: frozen | standard (Del Moral et al. 2006; proposal §5.2 says so itself) |
| Suppl. | IND-T; T05, T33, T34 remarks | IND-T PROVED, XF VERIFIED* (A-REV1 only); T05/T33 PROVED (author only) | stream implementation fact | AR | — |
| (LIT-PAR) | G4: Song–Liang-type splitting fails on an LH-like masked pair | COUNTEREXAMPLE (numerical, reproducible) + PROOF SKETCH | p = 16, n = 200 | — | LIT-PAR's own result; its theorem reference ("Thm 5") should read Thm 4 / Cor 2 + eq. (19) in the JRSS-B text (SL digest) |

**Disagreements to resolve (flagged).**
- **D1: API-POS vs LIT-MCMC on rapid mixing.** The two reports agree that no published rapid-mixing theorem covers *our* prior and target as stated. They differ on why:
  - API-POS puts the obstruction on the prior side (g = n, κ, cap ⌊n/2⌋). It expects a YWJ-style proof for our prior to "very likely succeed", and calls the gap "formal, not substantive".
  - LIT-MCMC computes that the sufficient condition R > M fails at n = 200 and 1,600 on LH, and at study scale in 12/12 data sets (by a factor ≥ p^0.87). It concludes the unimodal-ratio route *cannot* certify our target.
  - LIT-VENUE §1.3 says "R > M … since on LH S₀ is the unique local mode". LIT-MCMC's computation contradicts this: unimodality (R > 1) does not give R > M.
  - **Reading:** both can be right. LIT-MCMC refutes a *sufficient condition*, not fast mixing, and API-POS's claim is a CONJECTURE. The paper should not say either "covered" or "not coverable". It needs an independent check (§6).
- **D4: LIT-SMC vs LIT-PAR on island pooling.** LIT-SMC cites Vergé et al. as covering our identities; LIT-PAR calls Vergé "plain averaging" and contrasts it with Ẑ-weighted pooling. Both call T31(i) standard.
- **D5: the size of μ⋆ under a masked start.** LIT-SMC and LIT-MCMC say "polynomially small"; LIT-PAR says "exponentially small" (Mathews–Schmidler).
- **D6: Thm 6 / T26 novelty.** LIT-SMC says "no analogue"; LIT-VENUE says "standard pattern".
- **D9: citation details that differ across reports.**
  - Shin–Bhattacharya–Johnson venue: JASA (LIT-STAT) vs Statistica Sinica (LIT-VENUE).
  - Le Fay–Chopin–Vihola theorem number: Thm 3.2 vs Thm 3.4.
  - YWJ's size-cap constant is quoted three ways.
  - All of these should be checked against the primary sources before printing.
- **D10: Song–Liang's correlation condition.**
  - Settled against the text (SL digest). Condition 5 ("|cov(x_t, y)| > 0 for any true predictor") justifies the iterative stage-1 step. Theorem 4 / Corollary 2 with eq. (19) is what retains a true predictor: it is retained only if its population projection coefficient β₀,t on the subset is nonzero.
  - Masking can break both: cov(x_t, y) = 0 for a cancelled pair, and β₀,t = 0 when its partner sits in another split.
  - LIT-PAR's "Thm 5" label and "read from slides" caveat should be replaced by this citation.

## 3. Coverage against the goal

### 3a. Proposal theory targets (Local-to-Global proposal §5, §13.1)

| Proposal target | What we have | Verdict |
|---|---|---|
| §5.1 / Prop 1: exactness under MH correction (π invariant) | Each move reversible for γ_φ; the random-order round is self-adjoint. This is by construction (METHODOLOGY_v3 §6.5, V5) and checked by three consultants; I found no registry row for it (?). It is standard (proposal: "standard detailed balance") | **MATCH** (textbook; state it, cite it) |
| §5.2: SMC consistency as N → ∞ for the specified local-to-global sequence | ADRAFT-ThmA/CorA1 (fixed-data convergence of SMC estimators) PROVED, Astra author with Astra check only. T12/T31 unbiasedness PROVED-LOCKED. All standard (Del Moral et al. 2006; LIT-SMC/LIT-PAR call T12/T31 KNOWN—CITE) | **MATCH** (needs a cross-family check of ADRAFT-ThmA, or just cite) |
| §5.3: weight stability under weak cross-block dependence (Thm 1 "possible direction") | O-WSTAB WS1–WS8 PROVED (no review), W(a–f) XF VERIFIED under H-ORTH, ideal grid; WS6e CONJECTURE, WS8d OPEN. FD-W(a) PROVED-UNDER, (b) PROOF SKETCH, (c) CONJECTURE. T22(iii)/EXP′ (favourable start) is the selection-side analogue | **PARTLY MATCHED** (orthogonal-type idealisation only; nothing for the actual partition) |
| §5.4: approximation error when exact correction is unavailable (KL, TV, PIP and joint-PIP error) | Inverted in our design: correction is always exact, so the "approximation" is π₀ itself. T27(i), DIL-*, SEP-A/B quantify how far π₀ is from π (π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}). FD-NM (naive merge fails) ERROR, repair pending (A-REV4/A-REV6) | **EXCEEDED in kind** (lower bounds on the merge's error); the naive-merge proposition itself is still unrepaired |
| §13.1: estimates of E_π[h(θ)] converge to the truth | Fixed data, N → ∞: ADRAFT-ThmA (standard). Truth as n → ∞ at n-indexed budgets: only h = 1{S = S₀} (T38/N200), h = Z (T26(i), favourable, CONJECTURE), and h = 1{j ∈ S} (T26(ii) CONJECTURE; P1–P3 on LH at fixed p). General h (joint inclusion, β-functionals, predictions) NONE | **LACK** (the single most visible gap against the proposal) |
| §4.4 / §8.2: diagnostics (ESS, local–global discrepancy) as a new device | Only negative results (V12, E1c); no positive diagnostic theorem | **LACK** |

### 3b. Song & Liang (2015) theorem types (digest `SL.md`)

| SL result (type) | SL scope | Our counterpart | Verdict |
|---|---|---|---|
| Thms 1–2, Cor 1, eq. (16): posterior consistency (Hellinger contraction, rates) | exact full posterior; bounded predictors; P_n < e^{Cn^α} | T03/T03♯: selection consistency, 1 − π(S₀) = O_P(√(log n / n)), with p ≤ n^A. Coefficient/prediction contraction (V3) NONE | **MATCH for selection; LACK for contraction rates and p up to e^{Cn^α}** (we have p ≤ n^A only) |
| Thm 3: sure screening of identifiable true predictors (marginal inclusion → 1) | exact posterior | T03 ("large signals get PIPs → 1 without beta-min") PROVED-LOCKED | **MATCH** (about the exact posterior; our estimated PIPs are only covered in the favourable regime, T26 CONJECTURE) |
| Thm S (supplement): MAP consistency | exact posterior | T03 (HPM/MPM of the true posterior) **plus** the reported HPM of the algorithm: T38(0)/(a)/(b1)/(b2-LH), N200 | **EXCEED**: SL never prove anything about the merged output ("SAM is consistent" is informal; SL digest §2) |
| Thm 4, Cor 2: misspecified-subset posterior concentrates on the KL projection | fixed subset, n → ∞ | Our blocks *are* misspecified subset posteriors. T22 and T27 and DIL-* describe exactly when the block-product start does and does not hold the truth (a lower bound: π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} under masking), and the SMC removes the dependence | **EXCEED** (we quantify the failure, and correctness does not depend on it); their Condition 5 (|cov(x_t, y)| > 0) is exactly what masking violates |
| §6: complexity, K_n = O(√P_n), parallel O(P_n^{(1+α)/2}) + O(nP_n) | heuristic, no accuracy trade-off | T32(i) total score count (polynomial, 2.7·10¹¹ at (200, 500)); Theorem G; STG-M; table cost p·2^B/B, embarrassingly parallel | **LACK of a comparable parallel-cost statement**: we have total work, not work/depth/speed-up versus p, R and correlation |
| UQ of the merged output | none (SL: "only provides an approximate quantification of uncertainty") | Fixed-data exactness (T12, ADRAFT-ThmA); n-indexed accuracy only favourable/LH | **EXCEED at fixed data; LACK as n grows in correlated (masked) designs** |

### 3c. The three objectives (Felipe, 2026-11-03)

| Objective | Covered by | Missing |
|---|---|---|
| (1) Posterior accuracy: Ẑ | T12, T31(i) (KNOWN—CITE); OPW2 Thm A/B (relative variance, frozen; possibly Cérou et al. 2011, unchecked); T26(i) favourable CONJECTURE; masked E1/E2 lower tail | two-sided masked-regime accuracy; finite-n precision at study budgets |
| (1) PIPs | Prop 2 islandwise; T26(ii) CONJECTURE; P1–P3 (LH, fixed p) | equal-weight pooled PIP accuracy; masked p ≫ n |
| (1) Joint inclusion | — | **everything** |
| (2) Parallel scalability | T32(i) total work; table cost; Theorem G / STG-M stage counts (sequential depth, favourable or ideal) | work–depth theorem; islands-vs-particles trade-off; "correlation costs depth, never correctness" |
| (3) Selection accuracy | T03, T07, T21, N200, T38(0)/(a)/(b1)/(b2-LH) | study generator; P(U) → 0; finite-n discovery; upper bound on Π(X) |

## 4. Literature gaps against the proposal's five themes

### 4a. Coverage by the existing LIT reports (digest `digests/LIT.md` §4)

| Theme (proposal §7.1) | Covered by | Read at primary-source level | Missing before this run |
|---|---|---|---|
| 1. Split-and-merge BVS | LIT-PAR (main), LIT-STAT (one row) | Gutierrez–Guhaniyogi technical report; DECO; Papaspiliopoulos–Rossell 2017; Ma 2015 | **The Song–Liang paper itself** (LIT-PAR used Liang's slides, LIT-STAT second-hand). Now covered by `digests/SL.md`, read from the PDF in `theory_campaign/inputs/` |
| 2. Composite likelihood and approximate posterior calibration | **none** (no LIT file mentions Ribatet, Frazier, Pauli, Varin or "composite likelihood") | — | entire theme; now covered by §4b |
| 3. Divide-and-conquer Bayes | LIT-PAR (main), LIT-SMC | WASP, M-posterior, Zhang–Lam–Lin; Lindsten et al. 2017 abstract only | consensus MC full text; embarrassingly parallel MCMC (Neiswanger et al.) not named; Lindsten/Kuntz theorem statements. Not pursued: LIT-PAR already concludes that data-splitting guarantees are fixed-p and say nothing about discrete model spaces |
| 4. Importance tempering and SMC samplers | LIT-SMC, LIT-MCMC, LIT-PAR, LIT-VENUE | Del Moral et al. 2006; Zanella–Roberts 2019; Zhou–Smith 2022; SVV; Syed et al.; Mathews–Schmidler 2024 | **Gramacy–Samworth–King 2010** (importance tempering); now covered by §4b |
| 5. Diagnostics for scalable computation | LIT-VENUE (rows C2–C4), LIT-SMC/LIT-PAR (Ẑ variance) | Jacob–O'Leary–Atchadé 2020; Biswas–Jacob–Vanetti (Thm 2.5); R-hat header only | ESS theory, PSIS, R-hat in full, importance-sampling sample size; now covered by §4b |

### 4b. Primary-source pass (10 works; details, quotes and URLs in `digests/LITGAP.md`)

Every citation below was checked against Crossref and/or the publisher or journal page. Full text was read on arXiv for all except A2 and A3, where only the abstract was read. Equation numbers refer to the arXiv versions named in the digest.
I spot-checked these citations against my own knowledge of the literature; the digest is the record.

| # | Work | Key statement (quoted in LITGAP) | Bearing on our method |
|---|---|---|---|
| A1 | Ribatet, Cooley & Davison (2012), *Statistica Sinica* 22(2), 813–845 | Composite-likelihood posteriors are mis-calibrated; magnitude and curvature adjustments are needed before use as a posterior | Our π₀ is a block-product (composite) posterior used **only as a start**; φ = 1 is the exact posterior, so no calibration is needed for the reported output. It becomes relevant only if the π₀ marginals are ever reported as a cheap answer |
| A2 | Pauli, Racugno & Ventura (2011), *Statistica Sinica* 21(1), 149–164 | Bayesian composite marginal likelihoods require a calibration (abstract only) | As A1 |
| A3 | Varin, Reid & Firth (2011), *Statistica Sinica* 21(1), 5–42 | Overview of composite likelihood (abstract only) | Background citation for "local likelihoods" |
| A4 | Frazier, Nott, Drovandi & Kohn (2023), *JASA* 118(544), 2821–2832 | Theorem 2 with Assumption 6(iv): the approximate posterior can serve as an IS / rejection proposal, given a finite second moment of the proposal-to-target density ratio | The nearest precedent for "approximate posterior as proposal". Its condition is χ²-type, the same quantity as our ESS / weight-stability (O-WSTAB) conditions. It is parametric and n → ∞, not model space |
| A5 | Syring & Martin (2019), *Biometrika* 106(2), 479–486 | Generalised posterior Π_{n,ω} ∝ e^{−ωnR_n}Π; ω chosen by bootstrap so credible regions attain nominal coverage | Same: calibration is needed only when there is no exact target. We have one |
| B1 | Chatterjee & Diaconis (2018), *Ann. Appl. Probab.* 28(2), 1099–1135 | Thms 1.1/1.2: importance sampling from π₀ to π needs a sample size of about exp(KL(π‖π₀)), which is necessary and sufficient. Thm 2.1 warns that variance-type diagnostics built from the same weights can certify too early | **The right cost scale for "one-shot correction of the merge" and hence for why a bridge is needed.** In the masked regime, KL(π‖π₀) ≳ c(log p + ½ log n) by T27(i), so one-shot needs ≳ p^c n^{c/2} draws. This matches SEP-A/B; the identification is my inference, unproved (no new proof here) |
| B2 | Vehtari, Simpson, Gelman, Yao & Gabry (2024), *JMLR* 25(72), 1–58 (PSIS) | Pareto k̂ diagnostic; thresholds 0.5 and 0.7 | A candidate per-stage weight diagnostic; B2 §6.4 says k̂ for SMC weights is unstudied |
| B3 | Vehtari, Gelman, Simpson, Carpenter & Bürkner (2021), *Bayesian Analysis* 16(2), 667–718 | Rank-normalised split-R̂ < 1.01 | A candidate formalisation of our island-agreement flag. But MASKZPIP E1c PROVES that island agreement is uninformative under a blind grid, so R̂ inherits this limit |
| B4 | Elvira, Martino & Robert (2022), *Int. Statist. Rev.* 90(3), 525–550 | Critique of 1/Σw̄²; alternatives such as 1/max w̄ | Our schedule uses 1/Σw̄² (ESS 0.90); a max-weight companion is cheap |
| B5 | Biswas, Jacob & Vanetti (2019), NeurIPS 32 | eq. (7): d_TV(q^(N), π) ≤ an expression depending only on the law of Ẑ (via PIMH L-lag couplings), "estimated using independent runs of the SMC sampler" | Our independent islands produce exactly this input. It gives an *estimated* (not certified) TV bound for one particle's law, not for PIPs. It is the best fit for a positive diagnostic |
| C1 | Gramacy, Samworth & King (2010), *Stat. Comput.* 20(1), 1–7 | Importance tempering = simulated tempering + IS reweighting of all rungs; Prop 2.1: the ESS-optimal combination of IS estimators | A different algorithm (MCMC over temperatures, not an SMC bridge). Prop 2.1 might combine intermediate-stage estimates; not needed for correctness |

**Gap conclusions** (within the works read; not an exhaustive search):
1. No work found uses a composite or block-product posterior as an **SMC start that is then corrected exactly**. The composite-likelihood literature corrects by *calibration* because it has no exact target. The nearest positioning is: "Papaspiliopoulos–Rossell 2017 (block start) + Ribatet et al. 2012 (why the composite posterior alone is wrong) + Del Moral et al. 2006 (exact correction)".
2. Diagnostics: no published diagnostic certifies accuracy of an SMC model-space posterior. B5 gives an estimated TV bound from the law of Ẑ. B1 explains why weight-variance diagnostics can certify too early, which matches our negative results (V12, E1c).

## 5. Properties of our method with no guarantee yet (ordered by importance to the goal)

1. **Accuracy of posterior expectations E_π[h(S)] as n grows, in the masked (study) regime.** This covers joint inclusion probabilities, functionals, and PIPs at p ≫ n. Nothing exists beyond the favourable-regime CONJECTURE (T26) and LH at fixed p (P1–P3). This is proposal §13.1 and Felipe's objective (1).
2. **Two-sided relative accuracy of Ẑ in the masked regime.** Only the lower-tail mechanism is PROVED; the resolved-grid half is a CONJECTURE (OPEN for c ≥ 2). LIT-PAR calls the single-island relative variance "the theorem a referee will ask for".
3. **A parallel work/depth theorem.** We need depth as a function of p, correlation and masking, and an R-versus-N trade-off. This is the formal content of "correlation costs depth and particles, never correctness". Today we have only total work (T32(i)) and stage counts in the favourable or ideal-grid cases (Theorem G, STG-M). Note LIT-PAR's warning that per-round depth is Θ(p).
4. **Delivery of output: P(U) → 0.** No theorem bounds P(resource_limit), P(schedule_limit), P(numerical_failure) or P(grid_unconverged). Every consistency statement is joint with "output exists".
5. **Masked-regime selection consistency for the production method on non-LH or random designs, including the study's own generator** (groups of 5 packed by next-fit, p ≫ n). The verified routes are only (b1) with LS0, which is not in production, and (b2-LH), an exact-Gram subfamily.
6. **Finite-n guarantees.** These are an upper bound on Π(X) (OPEN) and a finite-n discovery bound for the Gibbs route (OPEN). All asymptotic results are vacuous at n = 200.
7. **Mixing of the φ = 1 move round (V10).** No published or project theorem covers our prior. The rapid-mixing route is blocked as stated (D1).
8. **Positive power of the diagnostics and flags.** Is there any condition under which a flag fires when the output is wrong? All theory is negative (V12, E1c).
9. **Calibration behaviour.** Nothing covers convergence of the rebuild loop, the probability that V contains the competing pair, or the stage count T_n in the masked regime (Conjecture P OPEN).
10. **Partition law for the actual adaptive packing**, and the effect of block construction (B, linkage, overlap or random partitions) on cost.
11. **Floating-point accuracy at production size.** VAL-FP was measured at p ≤ 40 only, and there is no floating-point theorem.
12. **Exactness of the composite start sampler, and reversibility and self-adjointness of the move round (V5).** These hold by construction and were consultant-checked, but I found no registry theorem (?). They are routine, but a paper claim needs a written proof or a citation.

## 6. Needs escalation

- **D1 (API-POS vs LIT-MCMC).** An independent reader should settle what the paper may say about YWJ/ZYVR/Chang–Zhou/Zhou–Smith for our prior. Specifically: is R > M failing a real obstruction or only a failed sufficient condition?
- **Song–Liang citation details** for any claim that "SaM breaks under correlation". Use Theorem 4 / Corollary 2 + eq. (19) and Condition 5 from the JRSS-B text (SL digest), not "Thm 5" from slides. LIT-PAR's G4 counterexample relies on this reading.
- **Citation clashes** (D9: SBJ venue, Le Fay et al. theorem number, YWJ constants) need a primary-source check before printing.
- **Novelty of O-PW2 Thm A vs Cérou–Del Moral–Guyader 2011 Thm 1.4** is unchecked (LIT-SMC).
- **ADRAFT-ThmA** (fixed-data SMC consistency) has only Astra-on-Astra review. Either cite Del Moral et al. or get a Claude check.
- **The (?) items in this report:** I did not find registry rows for V5 (start-sampler exactness, move reversibility). A registry search by someone with the full T38-RECORD context should confirm.

## 7. Outside scope

- API-AUDIT hazard: `fit$log_Z` on a stopped fit silently returns `log_Zbar0`. The recommended fix (set it to NA when `estimates_available` is not TRUE) has not been applied.
- LIT-PAR self-critique: v3's per-round depth is Θ(p) score evaluations. Option B (informed/tempered-Gibbs moves that score all p neighbours at once) is a method decision with direct bearing on objective (2).
- API-RESID: the backfit start is favourable on 78.7–91.8% of study fits but has no theorem and no SMC evidence. It would make T22(iii)/T26 relevant to the study.

## 8. Confidence card (per goal-level target; refined statements are inventory readings, not new conjectures)

| Target | Refined statement (as inventoried) | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Fixed-data exactness ("never correctness") | For any data and frozen calibration, Ẑ_r is unbiased, and SMC estimators of E_π[h] converge as N → ∞ (or R → ∞ with Ẑ-weighted pooling) | high | high (standard; cite) | none; it is KNOWN—CITE, so it is not a contribution | no |
| E_π[h] accuracy as n grows, masked regime (proposal §13.1) | For bounded h and n-indexed budgets, |Ê[h] − E_π[h]| → 0 in probability on a masked family | medium | low–medium | single-island relative variance through a masked crossing; resolved-grid V11 | possibly (grid resolution; LS0-type centre emission) |
| Parallel depth ("costs only depth and particles") | Depth = O(T_n·L·(p+B+2)) with T_n = O(log₂A₀) on masked families; width R·N with error O(1/√(RN)) | medium | medium on ideal grids (STG-M exists); low for the as-coded grid | T_n for the coded schedule in the masked regime (Conjecture P); per-round Θ(p) | maybe (LIT-PAR option B) |
| Selection consistency of the reported HPM, production method, realistic designs | T38(b) without LS0 beyond exact-Gram LH | medium | low–medium | general LH locking is false; adaptive packing; DELIV | maybe (LS0 is cheap: 0/2,394 HPM changes, but needs code merge) |
| Comparison with Song–Liang | SL's merged output has no theorem; ours has fixed-data exactness and HPM consistency on masked families, where SL's Condition 5 / eq. (19) fails | high | high for a counterexample (LIT-PAR G4 numerical + sketch) | an analytic SL failure on a masked pair, checked against the JRSS-B text | no |

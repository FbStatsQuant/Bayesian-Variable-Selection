# G2 digest: waves 3–5 (12 branches)

Source: scratchpad `src/<ID>/` = `theory_campaign/<ID>/` on `origin/theory/<ID>`. Statuses are copied verbatim and never upgraded. Every campaign result is a **candidate**: not reviewed cross-family and not adopted. "Same-family" means Claude-on-Claude.
Abbreviations: S₀ = truth; S° = reference (for LH, S₀ minus the masked hubs); π₀ = start law; π = posterior; 𝒮/𝒮⁺ = scored set without/with LS0; D_n = discovery term P(𝒪̄, S₀ ∉ 𝒮̄⁺); LH = W1-EXP linked-hub family (exact Gram, p ≤ n−1); LH-iid = its iid-Gaussian version (n^a ≤ p ≤ n^A, p ≫ n allowed).

**Cross-cutting facts (read first)**
- **The only masked-regime theorem with every premise proved needs LS0.** The no-LS0 routes were later closed, as single runs, on LH for c = 1 (W5-B2ENV exact Gram; W5-VMASK R1 LH-iid) and for every c under STAB-LH (W5-B2ENV).
- **Unfinished deliverables.** W5-FAVIID REPORT.md still has the literal placeholders `__HEADLINE__`, `__PILOT__` and `__CARD__`, so it has no headline, no §4.5 pilot table and no confidence card. W5-VPGD REPORT.md §5.3 still has `REALISED_TABLE_PLACEHOLDER`.
- **Timing inconsistency.** W5-VPGD (c214ca9, 19:56) calls W3-PGD's REPORT a "stub" and says W3-PGD's `n200_check.py` "has no result file". W3-PGD's head (76f0fbd, 20:09) is *later* and has a full REPORT with n = 200 results. The two branches' S2/S5 η numbers use different regions (see §W5-VPGD).
- **n = 200 relevance (unanimous).** At n = 200 the start is *dilution-masked*: tables score against the full y, so each truth sees noise v ≈ 7–26σ² (W3-VEXP Prop D; W3-PXN Prop W; W5-FAVIID). The misses are posterior misses. T38 explains the mechanism, not the n = 200 numbers. W4-T38FULL's confidence card gives "T38 explains n = 200" P(true) = 0.1.
- **Common σ².** None of these 12 branches analyses a common-σ̂² variant (that is F-SIGMA, outside this group). The relevant point here is the noise scale: start tables use v_T = σ² + (signal outside the block), while the posterior uses σ². W3-VEXP: "The parametrisation that matters is θ_j²/v, not θ_j²/σ²". In T38_PROOF, "σ = σ* noted".

---

## W3-PGD — head 76f0fbd (2026-11-02 20:09)
**Task.** Find the weakest checkable design conditions implying PGD and LD (the asymptotic hypotheses of refined T37) and prove TD′ w.p. → 1.
Files: REPORT.md (final), PROOF.md, PLAN.md. Header: "Everything here is a **candidate**: not reviewed, not adopted."

**Named results (PROOF.md labels; REPORT §2)**
- **Theorem W (refined T37(iii)).** PROOF §4. "Status: PROVED (candidate)."
  - Hypotheses: regime R1 with s₀, a ≤ s₀ and d fixed; EX-A, G, R, anchored SE_λ(d+1), BM-∞, PGD(η) on R_{a,d}(𝒟) with fixed η > 0.
  - Plus one of: (H1) d ≤ 1; (H2) (|𝒟|+1)^{d−1} ≤ n^{1/2−ε}; (H3) LD♭ with (★) (1+ρ*√d)²/(1−ρ*²) < 1 + 1/(2A).
  - Conclusion: P₀(TD′_P(R_{a,d}(𝒟))) → 1, and P(search from S_c fails to return S₀ certified) ≤ P(S_c ∉ R_{a,d}(𝒟)) + o(1).
  - Needs **no LS0** ("no (pairs with LS0)"); fixed design (G); noise σ² = σ*².
- **Lemma 1.1** (move algebra), **1.2** (best truth addition), **1.3** (ERC controls null leakage): PROVED.
- **Prop P1** (GERC + TRC ⇒ PGD), **Remarks on GERC**, **Prop P2** (block-orthogonality iff (B1)–(B3)), **Cor P2′** (equicorrelated closed form η*(d)), **Prop P3** (TRC sufficient conditions), **Prop P4** (PGD is sharp: a reverse margin ⇒ TD′_P fails w.p. → 1), **Lemma P5** (stability): all PROVED.
- **Cor P6** (random Gaussian designs): "PROVED given a cited concentration bound" (Bickel–Levina, not re-derived).
- Noise side: **Lemma Q** "PROVED (standard)"; **Lemma R** (score = −ν log RSS − pen + O(1)), **Lemma G** (population-gap comparisons), **Lemma U** (supersets of S₀): PROVED.
- **Definition LD♭**; **Lemma LD** (local/far decomposition) PROVED; **Lemma S** (superset states under H1/H2/H3) PROVED. *Name clash:* this is not W1-T38E's Lemma S (the ESS share lemma).
- **Lemma A′** PROVED. **Corollary W′** (GERC+TRC, or BO with (B1)–(B3), replaces PGD) "PROVED (composition)".
- **Prop C-LD.** "Status: COUNTEREXAMPLE (proof + script)". s₀ = 1, equicorrelated nulls with r > ½, p = n − 2: G, R, SE, BM-∞, PGD(1), GERC and TRC all hold, yet TD′_P(R_{0,2}) fails w.p. → 1.

**Numerics**
- Population PGD holds in S1–S6: η from 0.003 (S5, R_{14,·}) to 0.198. The binding move is the truth→truth swap. Max ERC is 0.5–0.94.
- **At n = 200 the hypotheses fail at sample level:** spurious correlations ≈ 0.32, sample GERC 1.29–1.68, sample PGD negative on far states in S3/S4/S6.
- Yet the greedy repair reached S₀ from every tested centre whenever S₀ was a local maximum (31/36 datasets). The 5 failures (all at c = 0.5) are posterior misses.
- "at n = 200 TD′_P is not even true without noise far from S₀; it is a near-truth property."
- C-LD convergence is logarithmically slow (r = 0.55: 1.7–3.5% failure even at n = 2·10⁵).

**What fails.** LD as in W1-T37R is needlessly strong. Dropping LD fails for d ≥ 2 with unrestricted extras (C-LD). A θ-free sufficient condition for PGD is impossible. Using PGD at n = 200 is wrong in its finite-n reading.

**Needs escalation.**
- Independent check of Lemmas R and G.
- Lemma S (H3) uniformity.
- Explicit reference for Cor P6.
- Sharp LD threshold: "(★) is off from C-LD's 1/(2A) by a factor of about 3–4". W5-VPGD calls this "misleading".
- Soussen/Tropp precedent cited from memory.

**Outside scope.**
- For T38(b1)+LS0 "the start mode must be near S₀ (m ≤ 2), or the repair input should be TD′_∞".
- (H2) with 𝒟 = truth-block nulls pairs with LS0, but eligibility is not proved.
- S5 has near-masking far from S₀ (TRC ≈ 1e-4).

**Confidence card.**
- Theorem W: (H1) 0.9, (H2) 0.85, (H3) 0.8.
- P1 0.95; P2 0.95; P4 0.9; C-LD 0.9.
- PGD/GERC/LD at n = 200: "the theorem is asymptotic only; disclose".

---

## W3-PXN — head 4aebea3 (2026-11-02 18:13)
**Task.** Find a p ≫ n family carrying all of T38(b)'s premises jointly on the actual X-dependent partition, and say whether the n = 200 masking matches W1-EXP's "weak-signal masking".
Statuses (REPORT §2 table; PROOF §§): "candidate pending cross-family review".

**Family LH-iid (PROOF §0).**
- Rows are iid N(0, Σ_LH): equicorrelated groups of size g with g ≤ B < 2g, so 9 ≤ g ≤ 16 asymptotically.
- c linked pairs with 0 < |ψ_i| < ρ and suppressor coefficient θ_{j_b} = −ψβ; v visible groups.
- n^a ≤ p ≤ n^A; noise ε ~ N(0, σ²I).
- S° = S₀ ∖ M, with M the masked hubs.

**Named results**

| Label | Statement | Status (verbatim) |
|---|---|---|
| P1 (Lemma P1) | v3 partition = groups w.p. → 1 | PROVED (given C1) |
| P2 | G; R; locked SE at size m_n + s₀; SE-blk; anchored SE_λ, SE_w; BM-∞ | PROVED (given C1) |
| Lemma C2, C3 | concentration | PROVED |
| B (Lemma B) | exact Beta laws of the start statistics at S°, independent of y | PROVED |
| Lemma Tr | truncated moment E[(1−X)^{−ν}1{X ≤ τ}] | PROVED |
| P3 | 1 − π₀(S°) = O_P(√(log n/n)), so b_n := π₀(𝓡_d) → 1; no 2^B, NL_η or VIS-lin needed | PROVED |
| P4 | Mstat →_d Σlog((s+i)/2) + ½χ²_c, so π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (T27 masking, CL(L) rate) | PROVED |
| P5 | S̃₀ = S° w.p. → 1 (eligibility for LS0) | PROVED |
| P6 (+ Lemma U, Lemma Λ) | TD′ lattice condition at S°: (L) and D_S on Lat(S°); LS0 certifies S₀ in c moves | PROVED |
| P7 | D2 for c = 1, no tweak: D2-a, b, c (Dep = O_P(√(log n/n))) | "PROVED / PROOF SKETCH" (D2-d (NB) is the PROOF SKETCH) |
| P8 (+ de-randomisation lemma) | 1 − π(S₀) = O_P(√(log n/n)) via locked T03 | PROVED |
| Cor (§12) | (b1) via LS0, every c: liminf P(Uᶜ, Ŝ⁺ = S₀) ≥ 1 − limsup P(U); (b1′) without a tweak, c = 1 | "PROVED (b1); PROVED modulo NB sketch (b1′)" |
| Q | if 2g ≤ B, linked pairs are co-blocked and LH masking disappears | PROOF SKETCH |
| W | dilution masking (LO₀ formula); under s₀ fixed + BM-∞, every block-orthogonal family is favourable | PROOF SKETCH |
| W′ | fixed-s₀ dilution family with π₀(S₀) → 0 | CONJECTURE |

- **LS0 dependence.** (b1) needs LS0; (b1′) needs no tweak but only covers c = 1. "For c ≥ 2 the no-tweak route stays OPEN, because it needs delivery (b2)."

**Numerics.**
- Exact π₀ by convolution, n = 200–1600, p up to 10,120.
- S̃₀ = S° in 174/186 replicates. LS0 scored S₀ in 185/186. T22(i) bound held in 186/186. √(n/log n)(1 − π₀(S°)) ≈ 1.5–2.6.
- NB d-range ≈ 10–40 nats against a 655 threshold.
- (L) certification fails ≈ (s₀+1)/√(2π(n+1)t_n): "4% at n = 200 and 1.2% at n = 1600". W5-VMASK R4: these numbers are for s₀ = 5.

**n = 200 study.** "The study's n = 200 masking is not the masking of T27/LH. It is *dilution masking*."
- Masked truths have L² ≈ 50–200, not O(1).
- The CL(0) prediction overshoots log₁₀π₀(S₀) by 17–29 orders of magnitude.
- It is scale-free and gone by n ≈ 1600.
- W1-EXP's "bounded L" version is rejected.
- LS0 on study data scored S₀ in 113/128 fits when |S̃₀ Δ S₀| ≤ ℓ + 1, and in 13/32 otherwise. S4/S6 start modes are 12–14 moves away, beyond ℓ = 10–11.

**What fails.**
- D2 for c ≥ 2.
- The study's group size g = 5 is outside the family (Prop Q).
- LH-iid at n = 200 is "near the edge".
- The dilution regime has no fixed-s₀ BM-∞ theorem.
- Certification is slow but scoring is not.

**Needs escalation.**
- Independent check of Lemma B and P3.
- W1-EXP Lemmas 1.1/1.2/1.4 at full generality.
- P7 NB bookkeeping.
- HQ wording: "the paper must **not** present it as the explanation of the n = 200 masking".
- Felipe: consider letting LS0 run to certification (a cost change that needs validation).

**Outside scope.**
- Correction to W1-EXP: 96–100% of start-masked truths have LO₁ > 0.
- π₀(𝓡₂) is only 0.1–0.3 in S4.
- A sharpened T22(iii) for iid favourable designs (later done in W5-FAVIID).

**Confidence card.**
- Joint family 0.93; b_n 0.95; T27 0.97; ELIG 0.97; TD′ 0.93.
- D2 c = 1: 0.88 / 0.85. No-tweak c ≥ 2: 0.6 / 0.15.
- π(S₀) 0.97; Prop Q 0.9; Prop W 0.9 / 0.85; W′ 0.7 / 0.3.

---

## W3-VEXP (verifier of W1-EXP) — head 7970fa0 (17:50)
**Task.** Adversarial referee of W1-EXP: Thm 1 (EXP′), Thm 2/6, Prop 2.1, Thm 3/4, Thm 5 (LH), and the population favourability of S1/S3/S4/S6.

**Verdict line.** "**No mathematical ERROR in any W1 theorem.** … All are VERIFIED. … Four wording errors need fixing (REPAIRS R4); none is load-bearing."

**Per-claim verdicts (REPORT §2, rows 1–27)**

| Row(s) | W1-EXP claim | Verdict |
|---|---|---|
| 1–4 | Lemmas 1.1–1.4 | V |
| 5 | **Thm 1, EXP′** (PROVED) | V; κ_EXP is loose (27 on LH, 100–1,700 nats at study SNR) |
| 6 | §1.5 | V (sketch) / E (minor: "κ₁₇ ≥ 0.15" false for S6, 0.1) |
| 7 | Prop 2.1 | V |
| 8 | Prop 2.2 | V |
| 9 | Lemma 2.3 | V |
| 10 | **Thm 2** (W1 status PROOF SKETCH) | V; "verbatim corollary of the locked T22(iii) … its PROOF SKETCH label is conservative" |
| 11 | **Thm 6** | V |
| 12 | **Thm 3** | V (needs a deterministic chain) |
| 13 | **Thm 4** | "V / E (wording)" ("iff … sufficient" is self-contradictory) |
| 14 | limit law | V (sketch) |
| 15 | Prop 2.1 escalation | V |
| 16, 17 | Lemmas 4.1, 4.2 | V; **boundary found**: at ψ ≥ ρ the hub pair forms its own block and π₀(S°), π₀(S₀) → e^{−Θ(n)} |
| 18–21 | Thm 5(a)–(e) | V |
| 22 | §4.3 LH-iid | **G → repaired** (R3, PROOF SKETCH) |
| 23 | S1/S3/S4/S6 block-orthogonal at population level | V (λ_b(S₀) = 0 exactly on the actual partition; S2/S5 positive) |
| 24 | "favourable regime asymptotically" in-sample | **G (not fixable here)**; CONJECTURE, high confidence |
| 25 | SE-blk at n = 200 | V (repro) |
| 26 | "EXP′ applies at study size" | G (fixed by R1) |
| 27 | W1 escalation 3 "weak-signal masking" | "Evidence against" |

**Repairs (REPAIRS.md)**
- **R1.** "Data-computable EXP′ remainder certificate (any n, any data). Status: **PROVED**." It gives 0.59–1.52 nats on study designs; the actual max |R| ≤ 0.145.
- **R2.** Thm 2 is a verbatim corollary of locked T22(iii). "I do not change W1's status word."
- **R3.** LH-iid part (a): **PROOF SKETCH**, with the "routine uniform-LLN step not written out". The partition-noise decoupling does not extend to S3/S4/S6 (GAP).
- **R4.** Wording corrections: κ₁₇ ≥ 0.1; "η < 1/2.02 suffices"; the fixed-p constant; deterministic chain for H1; replace κ_EXP by R1; Config B exact-branch rows.
- **Prop D** (deterministic start-mass ceiling) **PROVED**.
- **Dilution threshold:** PROOF SKETCH for the population limit; numerically confirmed.

**Status changes.** No W1 status word was changed. Row 22 moved G → repaired (sketch).

**n = 200.**
- The start is dilution-masked at every signal scale: it misses 6–12 of 14 truths, strong ones included.
- It becomes favourable only for n ≈ 800–1600 (S3, p = 500).
- π₀(R₂) ≈ 0.8 sits on small subsets of S₀ that are 6–11 additions away; ℓ = 10 < 11.
- "Any T37/T38 repair statement must count missing truths, not only extras."
- §8: "R_d's definition makes ∅ 'near-truth'". T38FULL adopted this by using Lat(S°).

**Fidelity.** Faithful. One minor omission: W1 does not say that the exact branch applies at p = 20, n ≥ 10,435.

**Needs escalation.**
- Locked-register edits proposed by W1 (EXP′ removed from T22(iii); NL_η → NL_C) need Felipe's decision.
- R3 and Thm 6 uniform-LLN write-up.
- The in-sample favourable regime (partition stability).
- For HQ: the n = 200 start is dilution-masked.
- Check Prop D's population threshold against the ANALYSIS-H2 fits.

**Confidence card.**
- EXP′ 0.98; Thm 2 0.97; Thm 6 0.95; T27 0.97.
- LH exact Gram 0.95 ("the ψ ≥ ρ cliff must be disclosed"); LH-iid 0.9 / 0.8.
- S1/S3/S4/S6 in-sample 0.85 / 0.4.
- Dilution 0.9.
- W1 weak-signal conjecture 0.15.

---

## W3-VT37R (verifier of W1-T37R, commit d492f22) — head 4988b96 (17:49)
**Task.** Adversarial referee of W1-T37R: Prop 1, Lemma 0, Theorem A, Theorems B/C, and the C3 counterexample.

**Branch-quality notes.** "W1's REPORT.md is an unfinished draft." W1's Exp 1 result JSON files are 0 bytes.

**Headline verdicts (quoted)**
- "**Theorem A (A1–A4), Lemma 2, Lemma 3, Prop 1 and the Lemma 0 inclusions: VERIFIED**", with 720 exhaustive designs and 0 violations.
- "**ERROR, with COUNTEREXAMPLE (CEX-1), in A5(a):** literal TD(d,0) strict does **not** imply TD′_P … **the original T37(i) is false even at d = 0**." Repaired by R1 (adds POS), which is PROVED.
- "**ERROR, with COUNTEREXAMPLE (CEX-2), in Lemma 0(b)'s 'in particular on every posterior miss'** … '0/541 is forced by monotonicity' is therefore unproven." At production scale, 233/234 non-repaired centres had F(S₀) > F(S_c). R2 is PROVED; the data question stays OPEN.
- Theorem B: VERIFIED; its headline is a GAP (R6). C1/C2 are sketches with errors, repaired at PROOF SKETCH (R4, R5). "**C3 (SE + BM-∞ ⇏ PGD): COUNTEREXAMPLE confirmed**".
- The "weakest" prose has a COUNTEREXAMPLE in 23/360 designs (R3).

**Verdict table**

| # | Claim | Verdict |
|---|---|---|
| 1, 1b | Prop 1; swap identity (SW) | VERIFIED |
| 2, 2b | Lemma 0(a), 0(b) delivery | VERIFIED |
| 2c | Lemma 0(b) "on every posterior miss" | **ERROR** |
| 2d | Remark (ii) "0/541 forced" | **GAP** (fixable only with data) |
| 2e | Lemma 0(c) | VERIFIED |
| 3 | Lemma 2 | VERIFIED |
| 4 | Lemma 3 | VERIFIED |
| 5, 6, 8 | A1, A2, A4 | VERIFIED |
| 7 | A3 | VERIFIED; "ℓ ≥ a+d suffices", the exact need is ℓ ≥ τ |
| 9 | A5(a) | **ERROR** |
| 10 | A5(b) | VERIFIED |
| 11 | "Weakest" prose | **ERROR** |
| 12 | Thm B | VERIFIED |
| 12b | Thm B headline | GAP (presentation) |
| 13 | C1 TL | PROOF SKETCH, plausible |
| 13b | C1 containment | GAP, fixable |
| 13c | C1 exceptional nulls | GAP |
| 14 | C2 | **ERROR** in the inequality (ratios 201 and 1,896); PROOF SKETCH after repair |
| 15 | C3 | COUNTEREXAMPLE, VERIFIED |
| 16 | C4 | CONJECTURE (not assessed) |

**Repairs (REPAIRS.md)**
- R1: POS added to A5. PROVED (repair); COUNTEREXAMPLE to the original.
- R2: Lemma 0(b′) dichotomy. PROVED.
- R3: "weakest" prose. COUNTEREXAMPLE; A4 VERIFIED.
- R4: LD weakened to κ_n ≤ κ̄(A,d); LD* for exceptional nulls. PROOF SKETCH.
- R5: union-model bound ‖(P_A − P_B)μ‖² ≤ 2(n−1)[…]. PROVED; C2 is a PROOF SKETCH.
- R6: 2^{Φ} states only for a data-independent centre; otherwise C(s₀, ≤a)p^d. GAP (presentation).

**Numerics.**
- EXP3-R: TD′_∞(R_{2,1}) held in 198/200 draws at n = 3000; TD′_P in 0/200.
- PROD (n = 200, p = 500): centres reached S₀ in 630/630 runs when S₀ was a local max, and 0/234 when it was not. S₀ was a local max in 35/48 datasets.
- EXH: 720 designs, 0 violations.

**Needs escalation.**
1. Extract F(S₀) − F(S_c) per fit for the 541 fits.
2. C2/C1 uniform linearisation, which is T01 material.
3. PGD not verified on S1–S6 (later done in W3-PGD / W5-VPGD).

**Outside scope.** At production scale the binding issue is the statistical half (S₀ beaten by a neighbour), not the search.

**Confidence card.**
- T37(i) refined: high (VERIFIED). Original T37(i): false.
- T37(ii): high. T37(iii): medium-high / medium.
- C3: high. Lemma 0 data remark: OPEN.

---

## W3-VT38E (verifier of W1-T38E, commit 436a712) — head 3e4b732 (17:55)
**Task.** Adversarial referee of W1-T38E: T38(b)-R composition, C1, D1/D3, D2 (with Lemma S), E3 (LS0), E1/CF2, and CF(c).

**Branch-quality note.** W1's `*.out` evidence files are gitignored, so W1's numbers are reproducible only by rerunning its scripts.

**Headline (quoted).**
- "**No fatal error found.** … Everything here is **PROVED given its stated inputs**, but several results are close to restatements of their inputs."
- "**One ERROR, cosmetic and repaired.** D2's no-blow-up event uses the ratio 1.925, but 4r/(1+r)² = 0.899993 < 0.9 … r* = (11 + 2√10)/9 ≈ 1.924951."

**Verdict table**

| Claim | Verdict |
|---|---|
| **T38(b)-R** composition (liminf form, routes b1/b1′/b2) | **VERIFIED** (PROVED given inputs) |
| Cost corollary | VERIFIED as an upper bound, conditional on unlocked T32(i) |
| **Lemma A** | VERIFIED (2,048,000 cases) |
| **C0** | VERIFIED (COUNTEREXAMPLE) |
| **Lemma B** | VERIFIED (deterministic) |
| **Lemma S** (ESS share) | VERIFIED |
| Kantorovich 1.925 | **ERROR (cosmetic, repaired)** |
| **Theorem D2** | **VERIFIED after the constant repair** (PROVED) |
| D2 numbers 3·10⁻⁹ / 1·10⁻⁶ | **GAP (reporting)**: these are one of three terms; the full bound is 2.2·10⁻⁷ / 1.6·10⁻⁵ |
| "D2 covers one-cancellation masking…" | **GAP (overstated)**: the CF(1) instances are not masked |
| **D1** | VERIFIED |
| **C1** | **VERIFIED (COUNTEREXAMPLE) after kernel repair**. W1's kernel was not reversible; with a reversible kernel, extinction was 0.56 at N = 10⁵ and 1.00 at N = 10⁶ |
| **Prop D3** | VERIFIED (PROVED, conditional); "SHARE is nearly the conclusion" |
| **Prop E1** | VERIFIED; its consequence: deterministic part VERIFIED, margin PROOF SKETCH |
| **Theorem E3** (LS0 eligibility) | VERIFIED (PROVED) |
| TD(d,0) fails | "**VERIFIED and strengthened**" |
| GP(d) / TD′ in CF | VERIFIED numerically (finite n) |
| CF(c) construction | VERIFIED |
| CF masking numbers | GAP (qualification): miss 0.64–0.86 at tier 0, ≤ 0.09 at tier 1 |
| "CF satisfies jointly…" | **GAP (status)**: asymptotic H3/ELIG/TD′ are CONJECTURE |
| "No obstruction for (b1)+LS0" | VERIFIED as "no obstruction found"; not a proof |

**New or repaired results**
- §3.1: D2 with **NB′** := {S₀ among the initial draws} ∪ {ESS(e^{d/T_e}) ≥ 0.9H}. PROVED.
- §3.2: C1 with a valid kernel. COUNTEREXAMPLE.
- §3.4 **Proposition V1**: TD(d,m) fails for every d ≥ 1 on {π(S₀) > ½}, so "T37(iii) is false for every d ≥ 1". PROVED.
- §3.5: GP(d) ⇒ TD′(𝓡_d, ℓ) when ℓ+1 ≥ s₀+d. PROVED.

**Status changes.** D2 moved ERROR → PROVED after repair. The CF joint claim was demoted to CONJECTURE (asymptotic).

**LS0 caveat (§4).** "An LS0 implementation must call it with `emit_centre = true`." Also fix the argmax-π₀ tie rule.

**§5 "What is weaker than it looks".**
- (b1) "is nearly a restatement of TD′".
- SHARE is close to the conclusion of D3.
- D2's asymptotic instance needs four unproved inputs. P(NB′ᶜ) → 0 is "a CONJECTURE".

**Needs escalation.** V1 means T37 must be restated with TD′/GP(d). The D2 statistical instance is "the most valuable open item: it is the only no-tweak masked-regime route". LS0 implementation. Independent check of the CF asymptotics.

**Confidence card.**
- Composition 0.97; D2 corrected 0.97; D2 instance 0.6 / 0.4.
- Lemmas A/B/S, D1, D3, E1, E3: 0.99. C0/C1: 0.99. V1: 0.99.
- CF asymptotic 0.8 / 0.6. (b2) delivery 0.5 / 0.15.

---

## W4-SHARE — head 0d3f3fe (18:34)
**Task.** Route (b2): prove SHARE or LT, or find the right particle-survival hypothesis.
Statuses (PROOF.md): candidates.

**Named results**

| Label | Statement | Status |
|---|---|---|
| **Theorem D4** (§1) | Space-time potential envelope. Under (TRACK) K_t h_t ≥ (1−η_t)h_{t−1}: P(n_T(W) = 0 ∣ 𝓒) ≤ P(envelope fails) + (1 − π₀(h₀)(1−e^{−θ₀}))^N | PROVED |
| **Corollary D5** (§2) | Fitness oscillation Γ = Σ_tΔ_tκ_t; delivery holds whenever Γ − Σlog(1−η) ≤ log(Nπ₀(h₀)/T) − ω(1) | PROVED |
| **Proposition G** | Γ ≤ max κ for every grid; an ESS/T13 grid condition "cannot imply SHARE" | PROVED |
| **Proposition SH** | log N threshold is sharp up to a factor 2 | PROVED |
| **Proposition X** | Gate obstruction: P(ever in U) ≤ Nπ₀(U) + NΣa_k | PROVED |
| §5 C1 branching | 0.066/0.493/0.999 predicted vs 0.060/0.465/0.995 simulated | PROOF SKETCH |
| **Proposition M** | (a) max_jδ²_{T,j} ≥ (n−1)λ²θ²_min; (b) under G, R, SE, BM-∞, addition odds ≥ 1 for φ ≥ φ_n → 0 | "(a) PROVED, (b) PROOF SKETCH" |
| **Lemma PD** | log γ₀ + d = F − log m(∅) | PROVED |
| **Theorem B2-W4** (§7) | (TRACK)+(OSC)+confinement+REPAIR ⇒ P(S₀ ∉ 𝒮 ∣ 𝓒) ≤ […]⁴ + ε_rep | "PROVED given inputs" |

**Counterexample PB (posterior barrier, finite n).** λ_min = 0.004 and π(S₀) = 0.94–0.97. Delivery succeeded in 200/200 islands, LT failed, and LS0 cannot score S₀. "Outside that regime route (b2) fails through REPAIR, not through delivery (COUNTEREXAMPLE, finite n, reproducible)." "No method change closes posterior-barrier designs: LS0, (b2) and T39 all fail there."

**Numerics.** Five start-masked designs (p = 16, π(S₀) ≥ 0.66). "S₀ was scored during the bridge in 500/500 islands … never scored in the terminal rounds and never missed." LT and delivery held in every island. Route (b2) "is closable there, but it is **not needed**".

**What fails.**
- SHARE as a per-stage hypothesis.
- LT is not necessary.
- Grid-based conditions.
- Sup-exit control on 𝓡_d.
- The asymptotic BVS instance of (TRACK)/(OSC) was not completed.
- No BVS realisation of C1 with valid REPAIR was found.

**Needs escalation.**
1. **Bridge-Gibbs discovery theorem** (multi-flip D2): CONJECTURE; P 0.8, provable 0.55. "the most valuable item".
2. Prop M(b) gain expansion.
3. Independent check of D4.

**Outside scope.**
- T38(b) should be phrased around bridge-Gibbs discovery, not terminal repair. This matches n = 200 (98% of fresh scores come from Gibbs; the local search repaired 0 fits).
- Posterior barriers are a ceiling for any local method.
- The drift term T/N is not negligible at N = 2500, T ≈ 1000.

**Confidence card.**
- D4 0.97; D5+G 0.97; SH 0.99; X 0.99; M(a)/(b) 0.99 / 0.9; PD 0.99; B2-W4 0.95 given inputs.
- (TRACK)+(OSC) for BVS: CONJECTURE, 0.75 / 0.4.
- Bridge-Gibbs discovery: 0.8 / 0.55.
- PB: COUNTEREXAMPLE.
- SHARE/LT: "superseded by D4; LT not necessary".

---

## W4-T38FULL — head a0f9cb5 (18:15) — THE MAIN THEOREM T38 (paper Thm 5)
**Task.** Assemble T38 paper-ready from verified pieces.
Files: T38_STATEMENT.md, T38_PROOF.md, REPORT.md, NOTES.md. It started before W4-SHARE pushed: "W4-SHARE: not pushed at start of run."

### Precise current statement (T38_STATEMENT Part I, "Theorem 5 (T38). Two-regime consistency of the reported HPM")

**Standing assumptions.**
- Idealisations: EX-A, EX-S, CAL.
- Implementation facts: SR and GUARD (IMPL).
- (P) H-T03: δ₁ = 1 − π(S₀) → 0, via locked T03 (G, R, SE, BM-C/BM-∞) or T03♯.
- Triangular array R1 (s₀ fixed, p ≤ n^A) with the v3 budgets.

**Parts**
- **(0) Composition, every n.** P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}). Hence P(𝒪, Ŝ⁺ ≠ S₀) → 0 and liminf P(𝒪, Ŝ⁺ = S₀) ≥ 1 − limsup P(U). "The first form is the stronger one."
  - **PROVED.** Inputs: locked T21 / W1-T38E §7 (VERIFIED by W3-VT38E), W2-BOOK Lemma RO, GUARD (IMPL).
- **(a) Favourable regime.** Under (F): 1 − π₀(S₀) → 0, the final run's Q_f iid π₀ draws score S₀ (T11(iii)), with or without LS0.
  - Sufficient conditions: (F1) locked T22(iii) hypotheses with EXP′ discharged: G, R, SE-blk, VIS, NL_η, NL_avg(κ). (F2) G, R, SE-blk, BO, BM-blk. (F3) G, R-lite, SE-blk, ZL(S₀), SPREAD, VIS-lin(S₀).
  - Status: "**PROVED-UNDER (F)**".
  - Joint family ORTH (X′X = (n−1)I, p ≤ n−1): "PROVED-UNDER the verified a3", a new unreviewed composition.
  - a4 (W1 Thm 2) keeps W1's word "PROOF SKETCH (kept, not upgraded)".
  - a8: in-sample favourable for iid S1/S3/S4/S6 is "GAP; CONJECTURE". W5-FAVIID later claims to close it.
- **(b1) LS0 route (method change).** Hypotheses for a deterministic S° with Φ(S°) bounded:
  - (M1) ELIG: P₀(π₀(S°) > ½) → 1.
  - (M2) POP-LAT(S°, m_n): on Lat(S°) ∩ {Φ ≥ 2}, some progress neighbour beats every non-progress neighbour and the state itself by m_n ≥ M_n√(log n/n) in Δ.
  - (M3) λ_min(R_{S°∪S₀}) ≥ φ₀² and ‖μ‖²/n ≤ M.
  - (OP-LS0) LS0 is run with its centre emitted.
  - Then LS0 scores S₀ in ≤ Φ(S°) − 1 moves (cap ℓ_n ≥ Φ(S°) − 1).
  - **Theorem b1: "PROVED-UNDER (M1)–(M3)".**
- **(b1-LH).** On LH exact Gram (p ≤ n−1, 0 < |ψ_i| < ρ, g ≤ B < 2g): (P), (M1), (M2) with fixed m₀ > 0, and (M3) all hold, and π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}.
  - Q_fπ₀(S₀) → 0 when c ≥ 2 and p → ∞, or c = 1 and p/(√n log²n) → ∞.
  - "With LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, with no statistical hypothesis left open."
  - Status of Prop LH-LAT and Cor b1-LH: **PROVED** (new; same-family referee VERIFIED).
- **(b1′) D2, no method change.** π₀(S₀ ⊕ j) ≥ b > 1/10; Dep ≤ 1 − c₁ off a bounded set; P(NB′ᶜ) → 0 with r* = (11+2√10)/9. Then "the *first stage of the tier-0 pilot* scores S₀".
  - D2 itself: **PROVED** ("VERIFIED after the repair").
  - Statistical instance on LH, c = 1 (§4.2): "**PROOF SKETCH**"; the NB step is unfinished. c ≥ 2: OPEN.
- **(b2) Gibbs path, no method change.** Under (DELIV) and (REP) (sup β_{L+5} → 0, H′ = L+5).
  - "**PROVED-UNDER DELIV and REP**". **DELIV (SHARE/LT) stays OPEN**; C1 shows it is a genuine particle-level property.
  - REP on LH: PROOF SKETCH (W2-PREM Thm B♯ / Thm L, unverified).
- **(c) Cost.** Scores ≤ T32(i) ceiling + (ℓ+1)max_k[p + k(p−k)] = O((n+p)(p+B)log²n + p²log²n).
  - "PROVED-UNDER T32(i), which is a CONJECTURE". W5-LOCKBOOK later proves T32(i). W5-VMASK R7 adds "+1" for the emitted centre.

**"Not claimed."**
- Evidence or PIP accuracy in the masked regime.
- Anything given completion.
- Superiority over other methods.
- Any finite-n error rate at n = 200.
- A masked p ≫ n family "on the strength of this run" (W3-PXN's LH-iid "single unverified run"; later verified by W5-VMASK).
- "Masked-regime consistency **without LS0** on any explicit family; that is OPEN."

### New results proved here (T38_PROOF §3)

| Label | Statement | Status |
|---|---|---|
| **Lemma LS-score** (§3.1) | D_S on Lat(C₀) ∩ {Φ ≥ 2} + ℓ ≥ Φ(C₀) − 1 + centre emitted or C₀ ≠ S₀ ⇒ search scores S₀. Drops (L) and the Φ = 1 states versus W1-T37R Thm A(A3) | PROVED |
| **Lemma M** (§3.2) | Uniform comparison: F(A) > F(B) when λ_min(R_A) ≥ φ₀² and Δ(B) − Δ(A) ≥ m_n ≥ M_n√(log n/n) | PROVED |
| **Theorem b1** (§3.3) | (M1)–(M3) + OP-LS0 ⇒ D_n → 0 | PROVED-UNDER (M1)–(M3) |
| **Proposition LH-LAT, Corollary b1-LH** (§3.4) | POP-LAT on LH with m₀ = min{(1−κ_max)R_min, min β_i²(1−ψ_i²)², min θ_h²}, R_i = β_i²ψ_i²(1−ψ_i²) | PROVED |
| §6a same-family subagent check | "Verdict: all four VERIFIED, with no errors" | cosmetic fixes applied |

- §6a referee remark: "the population algebra needs only |ψ| < 1. The condition |ψ| < ρ is used only for the partition and for (M1)."
- §3.3 alternative for (M2): W1-T37R Thm C (PGD + LD*): "PROOF SKETCH"; "PGD can fail under SE + BM-∞ (COUNTEREXAMPLE C3)".

### Dependence on LS0 (verbatim)
- "**Without LS0, the paper has no masked-regime consistency theorem whose premises are all proved on an explicit family.** LS0 is the method-change dependency. It must emit its centre as a score event."
- II.9 lists what holds without LS0: (0) in full; (a); (b1′) conditional; (b2) conditional on OPEN DELIV; finite-n inequalities (Thm B′, Cor P1, Thm A, Lemma S, T21); and the negative results.
- II.8: LS0 requirements are emit_centre = true, a fixed tie rule, labelled fits, and the investment rule. "(v) at n = 200, LS0 cannot fix posterior misses".

**Numerics (`lh_ls0_check.py`).**
- LH exact Gram, p = 108, c ∈ {1,2,3}, n ∈ {200,800,3200}.
- S̃₀ = S° in 90/90 runs; LS0 scored S₀ in 90/90.
- Minimum lattice margin 11 → 58 → 266 nats (c = 1).
- At n = 200 the margin was negative (−1.1 for c = 2, −2.9 for c = 3), yet S₀ was still scored.
- The partition was assumed to equal the groups (W5-VMASK later confirmed 90/90 with the actual partition).

**n = 200 (Remark 4).** "At n = 200 the theorem is a statement about mechanism … the start is dilution-masked … the misses are posterior misses … the deterministic thresholds of the T03 proof start near n ≈ 2×10⁶ (W2-VT03R R1)." Confidence card: "T38 explains n = 200": 0.1.

**What fails.**
- TD′ as a black box at S̃₀ (a restatement).
- Thm A(A3) as the repair input.
- Literal TD(d,0).
- Eligibility without LS0 (OPEN; E1 negative).
- (b2) from start mass + bridge mass + exits is false by C1.
- The H24 route is retired.
- Joint family for (b1′)/(b2): none had every premise proved at the time (later changed by W5-B2ENV/W5-VMASK).

**Needs escalation.**
1. Cross-family check of Lemma M, LS-score and LH-LAT.
2. HQ/Felipe decision on LS0.
3. Verify W3-PXN.
4. GUARD code check; SR confirmation.
5. T32(i).

**Open items ranked (§9).**
1. Cross-family review.
2. LS0 decision.
3. p ≫ n masked family.
4. NB for D2.
5. DELIV.
6. Eligibility without LS0.
7. REP outside LH.
8. T32(i), GUARD.
9. In-sample favourable regime.
10. n = 200 relevance ("must be disclosed").

**Confidence card.**
- (0) 0.98; (a) 0.95; (b1) 0.93; (b1-LH) 0.9; (b1) on LH-iid 0.8 / 0.7.
- (b1′) 0.9 / 0.75; (b2) 0.95 as an implication, 0.5 that DELIV holds, 0.15 provable.
- (c) 0.95 / 0.7.
- "T38 explains n = 200": 0.1.

**Outside scope.**
- LS0 cannot fix study posterior misses; S4/S6 start modes are 12–14 moves away.
- The LH-LAT formula (1−κ)R could replace T37's informal margin.
- W2-PREM found a counterexample to W1-T24G's repair family on LH, so cite B♯.

---

## W5-B2ENV — head 053511d (19:30)
**Task.**
1. Finish D2's NB′ on LH (exact Gram, c = 1).
2. Instantiate route (b2) on LH via W4-SHARE D5 / Prop M.
3. Referee W4-SHARE.

### Named results (PROOF.md)

| Label | Statement | Status |
|---|---|---|
| **Lemma OF** (§1) | orthogonal factorisation of d | PROVED |
| **Lemma 2.1** | aggregation rates | "PROVED (given [E-T1], [E-T6])" |
| **Lemma 2.2** | start tails | PROVED |
| **Theorem NB′-LH** (§2.2) | c = 1, any v: P(NB′ᶜ ∣ data) = O_P(√n/p + n^{−1/2}) | "PROVED (given [E-T1], [E-T6], [E-L4])" |
| **Corollary D2-LH** (§2.3) | c = 1, p/√n → ∞ (with p ≤ n−1): P(S₀ ∉ 𝒮_cal) = O(√n/p) + o(1) → 0, so liminf P(Uᶜ ∩ {Ŝ = S₀}) ≥ 1 − limsup P(U) for the **original method** | "PROVED (given [D2], [E-T1], [E-L4], [E-T5d])" |
| **Proposition M-LH** (§3) | M(b) on LH, any c | "PROVED (given [E-T1])" |
| **STAB-LH** | finite population inequality m_STAB > 0 | hypothesis |
| **Lemma J** | junk and proxy inclusion odds | PROVED (given (U1)–(U3)) |
| **Lemma T** | truth retention | "PROVED under STAB-LH" |
| **(G)** | hub gain | PROVED |
| **Prop CONF** (§4.3), **Cor CONF-run** | one-round confinement, uniform in φ and state; any frozen grid; rate O(log^{3.5}n/√n) | "PROVED under STAB-LH" |
| **Lemma R1** (§4.4) | one-round repair at φ = 1 with c₀(x) = g^{−c_x}/C(\|Λ_x\|+B+2, B+2) | "PROVED under the deletion part of STAB-LH" |
| **Theorem B2-LH** (§4.5) | route (b2) on LH, **every c, original method, any grid**: P(S₀ ∉ 𝒮 ∣ 𝓒) ≤ Nπ₀(𝒩ᶜ) + NT_ea_n + (1−c₀+o(1))^N → 0 | "PROVED under STAB-LH" |
| §4.6(b) lattice-indicator potential | "cannot certify delivery at any budget" (Γ ≳ log NT) | PROOF SKETCH |
| §4.7 (b2) when STAB-LH fails | — | OPEN |
| §5 LH-iid remarks (NB′ on p ≫ n) | — | CONJECTURE (not written) |

- **Theorem NB′-LH headline:** "This upgrades Thm 5(b1′) on LH, c = 1, from PROOF SKETCH to PROVED: the paper's first masked instance **without LS0**."
- **Theorem B2-LH** uses "No masking condition, no grid condition, no SHARE/LT/envelope, no occupancy, no T24/B♯ premises."

**STAB-LH is a real restriction.** It holds in config A and in 38/46 c = 2 settings. It **fails** at (ρ, ψ) = (0.85, 0.5) for every g tested, and in config B.

**Referee of W4-SHARE (REFEREE.md).** "No ERROR. D4, D5 and B2-W4 are correct as stated (D4 should cite IND-T for the conditional iid step)."

| Item | Verdict |
|---|---|
| D4 Step 1 | VERIFIED, with a citation GAP |
| D4 Steps 2–5 | VERIFIED |
| D5 | VERIFIED |
| Prop G | VERIFIED as stated; **GAP (wording)**: it is an upper bound, not grid independence |
| SH (i), (ii) | VERIFIED |
| SH (iii) | transition location is a heuristic (GAP: label it) |
| Prop X main inequality | VERIFIED |
| Prop X "Moreover" | **GAP (two missing terms)**: the mid-round visit rate and the independence-proposal term |
| Prop X "Use" | GAP (scope) |
| C1 mechanism | PROOF SKETCH as labelled |
| M(a) | VERIFIED |
| M(b) | PROOF SKETCH as labelled; "Upgraded on LH to PROVED" (Prop M-LH) |
| PD | VERIFIED |
| B2-W4 | VERIFIED given its inputs; L+5 rounds |

**Numerics.**
- p = 16 is not masked (S₀ is drawn in 65–100% of pilots).
- Large p (4,000 / 20,000, n = 10⁴ / 4·10⁴) gives a masked pilot. P(NB′ᶜ) = 0/20 and 0/10; Dep = 0.027 / 0.015. This run uses the group partition, not the v3 partition.
- (b2) final runs: 0 confinement exits in 100 islands (also at A85, where STAB fails). 94–99.5% of particles score S₀ at stage T.
- Lattice-potential realised Γ = 6.2–9.9 against an allowance of 0.9–1.9.

**What fails.**
- Lattice-indicator potentials.
- Uniform confinement without STAB.
- Sup-type repair constants: c₀ ≈ 10⁻⁵ at g = B = 4 and ≈ 10⁻¹¹ at g = B = 16, so the result is "asymptotic only".
- NB′ needs p ≫ √n.

**Needs escalation.**
1. Cross-family check of CONF and R1 (load-bearing).
2. Lemma J uniformity.
3. NB′-LH is cheap to verify.
4. HQ: "Theorem B2-LH makes LS0 unnecessary for a masked consistency theorem on LH whenever STAB-LH holds (and D2-LH does so for c = 1 unconditionally). This changes the investment-rule calculus for LS0."

**Outside scope.**
- The Lemma R1 order-event argument may simplify T24/Thm 3-B′.
- CONF also holds for calibration runs, giving a second no-tweak route for every c (not written).
- "At the study size (n = 200) nothing here applies (dilution masking)".

**Confidence card.**
- (b1′) LH c = 1: 0.93, done.
- NB′ on LH-iid: 0.8 / 0.7.
- B2-LH: 0.85, "done modulo independent check of CONF/R1".
- (b2) without STAB: 0.75 / 0.4.
- Lattice-potential negative: 0.85 / 0.6.
- M(b): 0.97. W4-SHARE: 0.97 (VERIFIED, same family).

---

## W5-FAVIID — head 5bf4dee (19:51) — REPORT INCOMPLETE
**Task.** Give a 2^B-free favourable start rate on iid block-diagonal designs with the actual partition, and T26's premise (P1) on study-like designs.
**Deliverable defect.** REPORT.md lines 9, 142 and 198 are the literal `__HEADLINE__`, `__PILOT__` and `__CARD__`. There is no headline, no §4.5 pilot results and no confidence card. Statuses are taken from REPORT §2 and PROOF.md.

**Family FAV.**
- Rows iid N(0, Σ_n), with Σ_n block-diagonal over groups of size ≤ g ≤ 16 and λ_min ≥ λ₀.
- p ≤ n^A; fixed S₀ and β.
- S1, S3, S4 and S6 are instances; S2 (AR(1)) and S5 (factor) are not.

**Named results (REPORT §2 table, PROOF §§)**

| Label | Statement | Status |
|---|---|---|
| **Lemma X⁺** (§1) | the EXP′ remainder is ≤ O(1/n) *from above* | PROVED |
| **Lemma X⁻** | — | PROVED |
| **Lemma B′** (§2) | exact Beta law for any fixed group union / outside conditioning set | PROVED |
| **Lemma Tr′** | — | PROVED |
| **Lemma M** (§4) | Mittag-Leffler aggregation, constant 3.8311; "this is where 2^B disappears" | PROVED |
| **Lemma S** (§5) | projection onto nearly orthogonal subspaces | PROVED |
| **Lemma G** | — | "PROVED (given [C1])" |
| **Theorem A** (§7) | fixed partition: on P_n, 1 − π₀(S₀) = O_P((s₀+1)√(log n/n)), constant 3.83(s₀+1)√((1+ε₀)A), "no 2^B, no g" | "PROVED (given [C1], [T22i], [W1-L1.1–1.2])" |
| **Lemma P1′** | blocks are unions of whole groups w.p. → 1 | PROVED given [C1] |
| **Proposition N** | no deterministic limit partition for groups of 5 | PROOF SKETCH (+ numerics) |
| **Theorem B** (§9) | actual noise-dependent packing; partition-free Q̄_n; "**For S3/S4/S6, P(Q_n(3)) → 1, so 1 − π₀(S₀) = O_P(√(log n/n)) unconditionally** (constant ×≤106; ×15 while B = 14)" | PROVED |
| **B′-conj** | Theorem B without the \|𝒲(m)\| factor | CONJECTURE |
| **Proposition B1** (S1) | context-free bound | PROVED (given [C1], [T22i]) |
| §10 | sharp first-order law 1 − π₀ ≈ 1 − exp(−N_add) | CONJECTURE (PROOF SKETCH of the mechanism) |
| **Proposition F** | one-change ceiling; sharpens W3-VEXP Prop D | PROVED |
| §11 thresholds | n*_null, n*_del, n*_half, n*_hit | CONJECTURE |
| **Corollary C1** | δ₁ = O_P(√(log n/n)) on FAV | "PROVED (composition)" |
| **Corollary C2** | Thm 6's (P1) on S3/S4/S6 | "PROVED (composition)"; inputs W2-T26 (candidates), EX-A, EX-S, CAL, START, OUT |
| **Corollary C3** | **Thm 5(a) (T38(a)) on S3/S4/S6**: liminf P(Ŝ = S₀) ≥ 1 − limsup P(U) | "PROVED (composition)" |

- Theorem B: "This closes W3-VEXP's GAP (row 24 …) without a leave-one-column-out lemma". It also discharges T38 a8 / W2-T26 Theorem B's CONDITIONAL input for these designs.
- Corollary C3 uses route (a), so it needs **no LS0**.

**Numerics.** 1,600 design-scale rows: S1/S3/S4/S6 × p ∈ {500, 1000} × scale × n ∈ {200,…,3200}.
- The T22(i) bound held in 1,600/1,600 but is "**vacuous (> 1) in every S3/S4/S6 cell up to n = 3,200**".
- q/ξ_n = 0.60–0.82. Q₀/Q_real = 0.999–1.050.
- Median log₁₀π₀(S₀) at n = 200 is −10.7 to −13.6.
- The empirical first n with median π₀(S₀) > ½ is 1,600 (S1, S3 p = 500) or 3,200 (others).
- "**The favourable threshold is set by the null-addition mass, not by dilution.**"
- Discovery (route (a)) needs only n ≳ 330–440.

**What fails.**
- A fixed limit partition for groups of 5 (W3-VEXP R3's device works only for g ≤ B < 2g).
- Removing the |𝒲(m)| factor.
- The S1 constant.
- T22(i) as a finite-n certificate.
- "(P1) with T^max … needs … n ≈ 10¹⁰ at s₀ = 14".
- T_n = O_P(1): OPEN.

**Needs escalation.**
1. Independent check of X⁺, M and Theorem B's factorisation.
2. [C1] perturbation constants.
3. HQ: "The paper must not claim finite-n relevance: n*_half ≈ 1,050–1,450 … (P1) with the realised grid needs n of order 10³–10⁴".
4. The dominant finite-n defect is the null-addition mass (s₀+1)M(p,n)/(2√n). Only a change to the start would move it.

**Outside scope.**
- W3-PXN P3's constant improves the same way.
- The locked T22(i) e-quantity is pessimistic.
- Δ_n ≈ (s₀+1)√(log p/(πn)) is a floor.
- n*_hit is about 3× below n*_half.

**No confidence card** (placeholder).

---

## W5-LOCKBOOK — head a65392b (19:00)
**Task.**
- Lock the low-risk half: T32(i).
- GUARD/OUT/SR code audit.
- Referee W2-BOOK and W2-T26.
- STATEMENTS.tex for Prop 1, Prop 2, Thm 4, Thm 6.

"Every PROVED is a candidate that I checked line by line; this is a same-family (Claude-on-Claude) referee."

**Code audit (AUDIT.md).** Read, not executed; source fingerprints at 9db8748.
- Every lemma is "**PROVED by code reading**": IMPL-GUARD, IMPL-OUT, IMPL-SR, IMPL-STREAM, IMPL-LS (scan-before-limit), IMPL-EMIT, IMPL-T, IMPL-LOOP.
- **Lemma STREAM** (strong Markov, under EX-S): **PROVED**.
- New caveats:
  - (G1) a stopped fit returns an incomplete HPM, so Thm 4 needs **𝒢 ⊆ U** ("false if a stopped fit's HPM is counted as output").
  - (G2) `partial_final` archive fields.
  - (G3) exceptions are no-output events.
  - (G4) the guard is shared between calibration and the final run.
- SR holds with the reading "both *feasible* configurations".
- **IMPL-EMIT, stronger than earlier caveats.** With `emit_centre = false`, LS0's centre is cached unoffered, so "the HPM can miss the start mode for the rest of the run". `emit_centre = true` is "mandatory, not cosmetic".
- The reported MPM is **uncapped** (`v3_run.R:130`).

**Named results**
- **Theorem T32(i)** (PROOF §T32): a deterministic count C_eval ≤ Σ_b2^{|C_b|} + Σ_e(1+4ℓ)H_e[1+m(T_e+L+4)] + 4N₁[1+m(T₁+L+4)] + (2ℓ+3)[1+(ℓ+1)M_p] + 2(ℓ+1)(40p+1) + 80p+1. **PROVED** (uses EX-A only for pilot stages ≤ T_e).
- **Corollary T32(i-lit):** the conjectured form holds for C_eval; not established for C_log. PROVED.
- **Corollary T32(c):** C_eval = O(max(n,p)·p·log²(n+p) + p²log²(n+p)). PROVED. "**Thm 5(c) … is now a theorem.**"
- STATEMENTS.tex (not compiled):
  - Lemma RO.
  - Prop 1 (decision rules).
  - Prop 2 (frozen-run identities) with the VAL-FP repair.
  - **Thm 4** (composition; routes (a), (d), (d⁺), (e′), (e-M)), requiring 𝒢 ⊆ U and with cap term 1{ℓ < s₀+d−1}.
  - **Thm 6** (evidence/PIP consistency, favourable only), with (P1) stated using the **realised** T_n.

**Referee of W2-BOOK.** "no errors in the mathematics; three fixable gaps, one sharpening".

| Claim | Verdict |
|---|---|
| Lemma RO | CORRECT |
| Guard COUNTEREXAMPLE | CONFIRMED (reproduced exactly; also under engine costs, where the bias can be upward: 1.0014Z) |
| Prop 2 (a)–(e) | CORRECT |
| Prop 2 (f) VAL-FP | GAP (wording) |
| Prop 1 (i′) | CORRECT |
| Prop 1 (iii′) | CORRECT, with amendment |
| Thm 4 (C1′)/(a)/(d)/(e′)/(e-M) | CORRECT |
| Thm 4 (d⁺) | CORRECT, sharpened |
| T23(ii-d) output corollary | GAP (scope: false on the exact branch) |
| Split edits | CORRECT |
| 541-fit reading | not checked |

**Referee of W2-T26.** "Lemmas 1–3 and Theorem A are CORRECT", including Lemma 3's use of T15 at a terminal-round prefix (= T12(i.b)). Theorem B is "CORRECT, CONDITIONAL". Prop C (ORTH) stays a "PROOF SKETCH (kept)". The p = 18 scan was reproduced (5/66 rows use non-production packing).

**Numerics.**
- The frozen-run law was reproduced at 60 digits.
- The masked design gives Δ_n → 1.
- T32 bound: 2.68·10¹¹ (n = 200, p = 500).
- Stops: 6/2,400 = 0.25% [0.11%, 0.54%], all in S5.

**n = 200 disclosure sentences (STATEMENTS.tex).**
- Stops are counted as failures.
- "we bound Pr(reported and wrong), not Pr(wrong | reported)".
- The PIP is not unbiased.
- "At n = 200 the premises of Theorem 6 fail (Delta_n is essentially 1 …)".
- T32 bound value.

**What fails.**
- "Every partial output is hidden" is literally false (G1, G2).
- T32 for C_log is not obtained.
- VAL-FP is unmeasured (no R/C++).

**Needs escalation.**
1. Cross-family read of the stop-site list and IMPL-SR(d); a D61 replay.
2. W1-T24G Theorem B′ is still unreviewed.
3. LS0 `emit_centre = true`.
4. Felipe to confirm 𝒢 ⊆ U, "reported = estimate fields", and SR.

**Confidence card.**
- IMPL lemmas 0.95; Prop 1 0.98; Prop 2 0.97.
- Thm 4 (C1)/(a)/(d)/(d⁺) 0.97; (e′)/(e-M) 0.9.
- Thm 6 0.95; T32(i) / Thm 5(c) 0.97.

---

## W5-VMASK (verifier of W3-PXN and W4-T38FULL) — head 4e41b97 (19:11)
**Task.** Adversarial verification of the masked-regime instance: PXN Lemma B, Lemma Tr, P1–P8, and T38FULL LS-score, Lemma M, Theorem b1, LH-LAT.

**Headline verdict (quoted).** "**Thm 5(b1-LH-iid) survives adversarial verification.** It can be cited as **PROVED (candidate), verified by a second same-family run, pending cross-family review** … The defects found are cosmetic … None affects a conclusion."

**Verdict table (rows 1–26)**

| Row | Claim | Verdict |
|---|---|---|
| 1, 2, 3 | Lemma B(i), (ii), (iii) | VERIFIED |
| 3′ | Lemma B needs only the LH identities, not \|ψ\| < ρ | VERIFIED (new) |
| 4, 5 | Lemma Tr(a), (b), (c) | VERIFIED |
| 6 | W1-EXP L1.1/1.2/1.4 never use block membership | VERIFIED |
| 7 | **P3** | VERIFIED |
| 8 | **P1** | VERIFIED (given cited C1) |
| 8′ | margin condition | VERIFIED (sufficient, not necessary) |
| 9 | P2 | VERIFIED (given C1) |
| 10, 11 | P4, P5 | VERIFIED |
| 12 | Lemma U | VERIFIED; **ERROR (cosmetic)** in (U1) |
| 13, 14 | Lemma Λ, **P6** | VERIFIED |
| 15 | (L) failure rate | VERIFIED; labelling note |
| 16 | P7 D2-a, b, c | VERIFIED |
| 17 | **P7 D2-d (NB)** | "**GAP (fixable) → repaired, R1**" |
| 18 | P8 | VERIFIED |
| 19 | PXN Cor (b1) | VERIFIED (composition) |
| 20 | **LS-score** | VERIFIED |
| 21 | **Lemma M** | VERIFIED |
| 22 | **Theorem b1** | VERIFIED (under M1–M3) |
| 23 | **LH-LAT** validity | VERIFIED |
| 23′ | "m₀ is sharp" | **GAP (overstatement)** |
| 23″ | \|ψ\| < 1 suffices | VERIFIED |
| 24 | P6 vs LH-LAT margins | Consistent (202/202) |
| 25 | LS0 as modelled | VERIFIED with two IMPL caveats |
| 26 | start mode | VERIFIED |

**Repairs (REPAIRS.md)**
- **R1:** D2-d (NB) on LH-iid, c = 1: "PROVED (candidate, this run)". Remark: the NB proof covers c ≥ 2 verbatim, but D2 itself does not apply there.
- **R2:** (U1) constant "≤ 1" is false; replaced by "≤ 0.52/c_* + o(1)". ERROR (cosmetic), repaired.
- **R3:** NB constant r*. Repaired.
- **R4:** (L)-failure numbers are for s₀ = 5. VERIFIED, label added.
- **R5:** LH-LAT "sharp" only for homogeneous pairs (m₀/true down to 0.002); exact m₀^♯ given. Restated.
- **R6:** Lemma B(i′) stated.
- **R7:** LS0 cost 1 + (ℓ+1)max_k[…]. Corrected.

**Statements as they should be cited (§3)**
- **Thm 5(b1-LH-iid):** LS0 with centre emitted. "**Status: PROVED (candidate). Verified line by line by W5-VMASK (same family). Pending cross-family review.**"
  - Extension, VERIFIED numerically only: heterogeneous ρ_h with min ρ_h > max|ψ|.
- **Thm 5(b1′) on LH-iid, c = 1, no LS0:** "**Status: PROVED (candidate).** D2-a, D2-b and D2-c are PXN's proofs, VERIFIED here. D2-d is R1 of this run, and is **unverified**: a single run." For c ≥ 2: OPEN.

**Status changes.**
- PXN's P7 / (b1′) D2-d moved PROOF SKETCH → PROVED (candidate, single-run R1).
- (b1-LH-iid) moved from single run to verified by a second same-family run.
- LH-LAT's "sharp" is downgraded to a qualified claim.

**Numerics.** Independent code: own scorer, own partition port, own generator.
- LH-iid reproduced within replicate noise.
- n = 1600, p = 10,120 with the **actual** partition: 3/3 for A and B.
- 236 replicates: partition = groups 213/216, LS0 scored S₀ 212/216.
- LH exact Gram: partition = groups in 90/90.

**Adversarial designs.**
- ψ = 0.69 vs ρ = 0.7: partition ≠ groups in 2/10 at n = 200.
- Null groups at ρ = 0.95: harmless.
- ψ = 0.8 > ρ: "**the masking disappears**". It is a transition to the favourable regime, "not a failure of the method".

**What fails.** Lemma B, P1 and P6 could not be broken. Heterogeneous designs have tiny margins (3.1e-4), so Lemma M is vacuous at n ≤ 10⁴ there.

**Needs escalation.**
1. Cross-family review of R1 (Step 1's E1 bound across the K cap).
2. Cross-family review of PXN P3 and Lemma B.
3. Lemma C1 constant (Bickel–Levina).
4. HQ wording: cite (b1-LH-iid) as "PROVED (candidate; verified by W5-VMASK)" and (b1′) LH-iid c = 1 as "PROVED (candidate; NB closed by W5-VMASK R1, unverified)". Drop or qualify "sharp"; label s₀ = 5.

**Outside scope.**
- Beyond the cliff the method is not hurt.
- Heterogeneous margins are tiny.
- P1's sufficient margin condition is far from necessary.

**Confidence card.**
- (b1-LH-iid) 0.95; (b1-LH) 0.97.
- (b1′) LH-iid c = 1: 0.9 (0.85 that R1 holds).
- (b1′) c ≥ 2: 0.6 / 0.15.
- P3 0.97; LH-LAT sharp m₀^♯ 0.95 / 0.9; heterogeneous ρ_h 0.9 / 0.85.

---

## W5-VPGD (verifier of W3-PGD) — head c214ca9 (19:56)
**Task.** Verify and complete Theorem W (Thm 3(iii)), the (★) constant, and PGD on the study designs.
It describes itself as "also the **completed REPORT for W3-PGD's results** (its own REPORT.md is a stub)". W3-PGD's later head contradicts this; see the inconsistencies section.

**Headline (quoted).**
- "**Theorem W VERIFIED** (no ERROR in any step). Four minor GAPs, all repaired … Status after repair: **PROVED (candidate)**, same-family referee."
- "**Discrepancy: the region form does not cover the masked regime (COUNTEREXAMPLE, R6.1).**" On LH with ≥ 2 pairs, population PGD on R_{2,0} fails with an exact tie (η = 0 in 20/20 cases), and TD′_P(R_{2,0}) fails w.p. → 1 (200/200 fits).

**REFEREE.md verdicts.** "**no ERROR in any proof step.** Four GAPs, all minor or presentational (G1–G4)".

| Item | Verdict |
|---|---|
| Lemmas 1.1–1.3, P1, Remarks (a)–(c), P2 (+ brute force), P2′, P3, P4, P5(i)–(iii) | VERIFIED |
| P5 LD♭ stability sentence | GAP (G3) |
| Cor P6 | VERIFIED given the citation, with GAP (G2) |
| Lemma Q, R, G, U, chain rule, LD, S (α)(β)(γ) | VERIFIED |
| (H1) ⊂ (H2) | G1, presentational |
| (★) | "correct but loose" |
| Lemma A′ | VERIFIED |
| **Theorem W** | **VERIFIED** (scope warning R6) |
| Cor W′ | VERIFIED; random-design clause after R2/R3 |
| C-LD | VERIFIED (A = 1) |
| A > 1 sentence | GAP (G4) → CONJECTURE (R4) |
| "factor 3–4" | "misleading" |

**Repairs (REPAIRS.md)**
- **R0:** vanishing η_n allowed if η_n²nθ²_min/log n → ∞. PROVED.
- **R1:** (H1) is (H2) with d = 1. PROVED (presentational).
- **R2:** uniform form of Theorem W. PROVED (by inspection).
- **R3:** LD♭ stability |Δρ²| ≤ 8ε/φ₀⁸. PROVED.
- **R4:** C-LD for A > 1 downgraded to CONJECTURE.
- **R5:** "factor 3–4" sentence replaced.
- **R6.1 Proposition T (tie).** A present truth that is worthless at S + j makes PGD fail for every η > 0. PROVED.
- **R6.2 Theorem W_Lat (lattice form).** For deterministic S° = U° ∪ P° with |P°| ≤ d: PGD(η) on Lat(S°) + G, R, SE_λ(d+1), BM-∞ ⇒ (L) ∧ ⋂D_S w.p. → 1, and certified repair from any centre in Lat(S°). "**No LD condition is needed.**" PROVED (candidate).
- **R6.3 Proposition LH-PGD.** η_LH = min{1, 1−κ_max, D_min/R_max}, and POP-LAT(S°, m₀) ⇒ PGD(m₀/R_max). "PROVED (candidate); sharpness numerical" (20/20 cases).

**STAR.md**
- **Proposition S′:** (★′a) (τ_{d−1}²−1)A < ½ ∧ (★′b) (τ_{d−1}²+τ_d²−2)A < 1, or a counting condition. (★) ⇒ (★′). PROVED (candidate).
- **Proposition G** (grouped equicorrelated nulls, A = 1): TD′_P(R_{0,2}) fails for r > 1/3, whereas C-LD needs r > 1/2. "COUNTEREXAMPLE (construction + proof for d = 2; d ≥ 3 PROOF SKETCH)".
- **β-removal:** CONJECTURE.
- Certified/failing gap at A = 1, d = 2: 0.333/0.143 = 2.3× (was 4.5×).

**How to cite (quoted).** "Thm 3(iii) can cite Theorem W (VERIFIED, candidate) … For the masked regime (T38(b1), LH) it must cite Theorem W_Lat with Prop. LH-PGD, not the region form." The gap is in F-REFINE's ARCHITECTURE/CARDS describing Theorem W as "the general sufficient condition for (M2)". W3 itself never claimed LH coverage.

**Numerics.**
- Population PGD on R_{2,2}(truth-block mates), p = 500: η = 0.198 (S1), 0.148 (S2), 0.084 (S3), 0.043 (S4), 0.108 (S5), 0.057 (S6). The binding move is the truth→truth swap. Cor P2′ = (B1)–(B3) = brute force.
- "Cor P6's sufficient condition is vacuous at every feasible n (it needs n ≈ 10^15–10^22)."
- §5.3 realised-design table: **`REALISED_TABLE_PLACEHOLDER` (not filled)**.

**n = 200 (Outside scope).** The guaranteed gap for S4 at c = 0.5 is ≈ 0.03 against penalties of ≈ 9 nats, so "the proof's lower bound says nothing at n = 200". "Nothing in this asymptotic statement explains n = 200 behaviour."

**Needs escalation.**
1. Cross-family review of Theorem W, R2 and R6.2 (Lemma R ridge bookkeeping; Lemma G pair counting).
2. β-removal conjecture.
3. Random-design versions of Props G and C-LD for A > 1.
4. GERC = Tropp ERC citation.
5. Bickel–Levina correlation version.

**Confidence card.**
- Theorem W (region form) 0.95, done; 0.9 that cross-family review passes.
- W_Lat 0.95; LH-PGD 0.97; S′ 0.95.
- β-removal 0.7 / 0.4.
- Prop G 0.95.
- Realised transfer: empirical only.

---

## Inconsistencies and cross-branch tensions noticed

1. **W3-PGD REPORT vs W5-VPGD.** W5-VPGD (19:56) treats W3-PGD's REPORT as a stub and its n = 200 numerics as missing. W3-PGD at 76f0fbd (20:09) has a full REPORT with E1/E2 tables.
   - Their η values differ by region and 𝒟. S5: W3 gives 0.003 on R_{14,0} and 0.087 on R_{3,2} (𝒟 = all nulls); VPGD gives 0.108 on R_{2,2}(truth-block mates). S2: W3 gives 0.119 on R_{3,2}; VPGD gives 0.148 on R_{2,2}.
   - W5-VPGD's verdicts cover W3-PGD's PROOF.md only, not the late REPORT numerics.
2. **Two incomplete REPORTs.** W5-FAVIID has three template placeholders, so no headline or card. W5-VPGD has its §5.3 placeholder.
3. **W4-T38FULL statuses are superseded by wave 5. The T38 file has not been updated.**
   - (c): W5-LOCKBOOK proves T32(i), so Thm 5(c) "is now a theorem".
   - (b1′) on LH c = 1: PROOF SKETCH → PROVED in two separate single runs on *different* families. W5-B2ENV's NB′-LH is on exact Gram with p/√n → ∞ and p ≤ n−1. W5-VMASK R1's NB is on LH-iid.
   - (b2): "DELIV OPEN" in T38FULL, but W5-B2ENV gives Theorem B2-LH (every c, original method) "PROVED under STAB-LH". STAB-LH fails at (ρ, ψ) = (0.85, 0.5) and in config B.
   - The "p ≫ n LH-iid unverified" item is now verified by W5-VMASK (same family).
   - The (a) a8 GAP (in-sample favourable for S3/S4/S6) is closed by W5-FAVIID Theorem B / Cor C3 (unreviewed).
   - Consequence: T38FULL's headline 6 / II.9 claim "no masked-regime consistency theorem without LS0 on an explicit family" is contradicted by W5-B2ENV and W5-VMASK as single runs. Their own text says so: "the paper's first masked instance **without LS0**"; "changes the investment-rule calculus for LS0".
4. **Theorem W region form vs masked regime.** T38FULL §3.3 lists Thm C/PGD as an alternative for (M2). W5-VPGD R6.1 shows the region form fails with exact ties on LH with c ≥ 2, so only W_Lat applies.
5. **Lemma S name clash.** W1-T38E Lemma S (ESS share, used by D2) differs from W3-PGD Lemma S (superset states) and W5-FAVIID Lemma S (projection onto a subspace sum). Lemma M also has three meanings: T38FULL (uniform score comparison), W5-FAVIID (Mittag-Leffler), and W4-SHARE Proposition M.
6. **The (L)-failure "4% / 1.2%" in W3-PXN** is for s₀ = 5 (W5-VMASK R4). PXN's P7 used the faulty 1.925 constant (R3).
7. **LH-LAT "sharp"** (T38FULL) is overstated for heterogeneous pairs (W5-VMASK R5).
8. **LS0 `emit_centre`.** W3-VT38E, T38FULL and W5-VMASK call it an implementation caveat. W5-LOCKBOOK shows it is mandatory, because the cache would permanently hide S̃₀ from the HPM.
9. **ψ ≥ ρ boundary.** W3-VEXP and T38FULL read it as a "cliff" / (M1) failure. W5-VMASK reads it as a transition to the favourable regime: masking disappears and the method is not hurt.
10. **W1-EXP "weak-signal masking" conjecture.** Rejected independently by W3-VEXP (Prop D; P = 0.15) and W3-PXN (Prop W). The mechanism is dilution. W5-FAVIID adds that the favourable threshold is driven mainly by null-addition mass, not dilution.
11. **"0/541 repairs forced by monotonicity"** (W1-T37R) remains unestablished (W3-VT37R R2). W5-LOCKBOOK also did not check the 541-fit reading. This needs ledger data.

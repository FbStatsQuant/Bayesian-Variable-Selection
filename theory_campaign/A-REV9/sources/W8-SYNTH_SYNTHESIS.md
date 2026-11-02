# SMC-BVS theory campaign 2026-11: synthesis

**For:** Felipe (PI). **By:** W8-SYNTH, branch `theory/W8-SYNTH`. **Snapshot:** every `origin/theory/*` branch as fetched on 2026-11-02 between 20:15 and 20:40 UTC. Head hashes are in `SNAPSHOT.md`.

**How to read this.**
- Nothing here is adopted. Every "PROVED" is a **candidate**: an author's proof, sometimes checked by a second run.
- *Same-family (SF)* means a Claude run (Opus or Fable) checked a Claude run. *Cross-family (XF)* means one of the Astra reviews A-REV1 to A-REV4 checked it.
- Status words are copied from the source and **never upgraded**. When the registry (`theory/S-REGISTRY`) and a later report disagree, I say so.
- Citations have the form `branch · file · label`.
- I recomputed nothing mathematical. I read the reports, the registry and the cards. Five reading helpers digested the ~50 branches; I checked the load-bearing quotes myself (S-ELS, SR_AUDIT, T32(i), BG3, W6-FIXREV1 (c), L-LEAN status).

---

## 1. One-page summary

### The story (unchanged, and still the right one)
The reported HPM is the best model the run ever scored. So it is right when two things hold: **the posterior ranks the truth first**, and **the run scores the truth at least once**. Theorem 4 (T21) turns this into one inequality for every n:

  P(output and Ŝ ≠ S₀) ≤ 2·E[1 − π(S₀)] + P(output-potential run never scores S₀).

The first term is statistics (Thm 1). The second term is computation (Thms 2, 3, 5). The campaign has made both halves concrete. It has also shown, with data, that **at the study size (n = 200) every error is in the first term**:
- 565 of the 2,394 completed fits are posterior misses;
- there are 0 search misses;
- S₀ was scored in all 2,394 completed fits;
- the final local search never moved.

Source: `S-ELS · REPORT.md §1, §3`, from the actual PROD-H ledgers.

### What is proved: candidates, mostly checked twice
- **Thm 1 (T03♯).** The posterior concentrates on S₀ under anchored sparse-eigenvalue and beta-min conditions, with the exact beta-binomial size tail. Status: PROVED; SF verified; XF verified.
- **Prop 1 (T07).** The HPM and MPM are the Bayes rules, and no size prior can fix a same-size swap. Status: locked plus PROVED additions; formalised in Lean.
- **Thm 2 (start), deterministic and EXP′ parts.**
  - EXP′ (the block-table expansion) is now a theorem.
  - The chain-masking law CL(L) ⇒ T27(i) is proved.
  - One explicit family (LH, "linked hubs") realises masking and near-truth start mass together.
  - Status: PROVED; SF verified; XF verified, except the LH theorem, which has had no XF review.
- **Thm 3 (repair).**
  - Theorem A: the production greedy search repairs from a centre **iff** TD′ holds. It is exact at finite n.
  - Theorem W: the asymptotic sufficient condition.
  - Theorem B′/B♯: the Gibbs-path version of T24.
  - Status: A and B are XF verified after repairs; W is SF only.
- **Thm 4 (T21).** The composition inequality. Locked, reproved in W2-BOOK, and formalised in Lean.
- **Thm 5 (T38).**
  - Part (0), the composition: PROVED.
  - Part (a), the favourable regime: PROVED-UNDER the start-concentration premise.
  - Part (c), cost: T32(i) is now PROVED by W5-LOCKBOOK and re-checked by W7-SEC.
- **Thm 6 (T26).** Ẑ and PIP consistency in the favourable regime, under one premise (T_n+1)Δ_n → 0. Status: PROVED; SF and XF verified.
- **Prop 2 (T12, T31(i)).** Islandwise unbiasedness and the 95% Markov bound. Locked; the bookkeeping additions are PROVED. The XF review left GAPs that are not yet repaired.

### What is proved only with LS0
**Thm 5(b1) / (b1-LH) / (b1-LH-iid).** Masked-regime consistency of the reported HPM, with every statistical premise proved on an explicit family, holds **if LS0 is added**. LS0 is one extra local search from the exact start mode, with its centre emitted as a score event.
- Status: PROVED-UNDER (M1)–(M3); on LH it is PROVED.
- SF verified by W5-VMASK.
- **Not XF reviewed:** Lemma M, LS-score and LH-LAT.
- A-REV3 rates the p ≫ n version (W3-PXN P6/P7) a **GAP**.
- Sources: `W6-FIXREV1 · T38_STATEMENT.md · Theorem 5 (b1), (b1-LH)`; `W5-VMASK · REPORT.md §3`.

### New since the registry: the masked regime may not need LS0
Several runs now give a **no-LS0** masked theorem on the LH family. All are candidates, none is XF reviewed, and each has a soft spot:

| Route | Status | Soft spot |
|---|---|---|
| D2-LH, c = 1 (`W5-B2ENV · PROOF.md §2.3 · Cor. D2-LH`) | "PROVED (given [D2], [E-T1], [E-L4], [E-T5d])" | single run |
| W5-VMASK R1 on LH-iid, c = 1 | PROVED (candidate) | single run |
| B2-LH, every c (`W5-B2ENV · Thm B2-LH`) | "PROVED under STAB-LH" | STAB-LH is a numerical premise; it fails at (ρ, ψ) = (0.85, 0.5) |
| BG3 + LH-lock, every fixed c, p fixed (`O-BGIBBS · REPORT.md · Theorem BG3, Prop. LH-lock`) | BG3 PROVED, LH-lock PROOF SKETCH | the LH-lock sketch |
| F1/F2 (`F-SHARE · REPORT.md · Theorem F1, F2`) | F1 PROVED, F2 PROOF SKETCH | F2 sketch |
| Prop. GU (`W7-SEP · REPORT.md`) | PROVED, candidate | needs a start already inside the relevant set |

So the sentence "without LS0 the paper has no masked-regime theorem" (W4-T38FULL, W6-FIXREV1 "Not claimed") is **out of date**. The accurate version: there are no-LS0 candidates on LH, and none is closed beyond a single run or a sketch.

### What is open
- Delivery (DELIV) for any family other than LH.
- Masked-regime accuracy of Ẑ and the PIPs. It needs population delivery, DELIV-POP (`F-MASKPIP`); only the one-sided statements M1–M3 are proved.
- Anything quantitative at n = 200. Every theorem with a rate is vacuous there:
  - T03 thresholds are about 2·10⁶ (`W2-VT03R R1`, confirmed by A-REV2 and W6-FIXREV2);
  - the 2^B factor is at least 10³;
  - Δ_n ≈ 1.
- The dilution masking the study actually has. It is in no theorem: O-DILUTE gives exact identities and a population sketch only.
- XF review of everything that landed after A-REV4 (the whole of waves 5–7 and the O-/F- runs).

### The three decisions Felipe must take
1. **LS0.**
   - **Where it stands.** HQ recorded "LS0: APPROVED by Felipe (2026-11-02), conditional on O-LS0's data check" (`theory/campaign · theory_campaign/HQ/SR_AUDIT.md`). **That check has not landed:** `theory/O-LS0` holds scripts only, and an O-LS0-WRAP run is due to write the report (LEDGER 20:16 UTC).
   - **What changed.**
     - The referee's main objection (M2) is that the headline theorem is about an algorithm the simulations did not run.
     - S-ELS shows that LS0 cannot turn any study miss into a correct report: S₀ is already scored in every completed fit and loses to the HPM, so the only way LS0 can change a report is by finding a model that beats the current HPM (a posterior-mode correction). That can only turn a correct report into a wrong one, never the reverse. This is exactly what the O-LS0 condition asks to measure.
     - The no-LS0 LH routes above now exist.
   - **My recommendation.** Keep the conditional approval. Make the paper's headline the **no-LS0** theorem on LH **if** the XF verification task (§8, task 1) passes. Then present LS0 as a remark with its cost. If task 1 fails, LS0 stays the headline, and the paper must say plainly that the theorem covers v3 + LS0.
2. **Common-σ² start.**
   - **Evidence.** Three runs looked at it. Two reject it for study-like designs:
     - `O-DILUTE · REPORT.md §5`: "Do not adopt it." With the true σ², the median log₁₀π₀(S₀) is −690 and π₀(R₂) drops to 0.
     - `F-SIGMA · REPORT.md · Theorem S6`: "No single σ̂² serves truths and nulls at once"; "should **not** be deployed as specified".
   - O-MIX's support comes from an exactly block-orthogonal toy only.
   - **My recommendation.** Reject it.
   - **Residualised (backfit) tables** are a different change. They come out of both rejecting runs, and O-DILUTE's pilot gives 378/480 favourable fits. Run F-SIGMA's free "Step 0" post hoc check before considering a start change under the investment rule.
3. **The n = 200 disclosure wording.** The numbers have moved; the paper needs one corrected paragraph. My draft:

   > At the study's size (n = 200, p ∈ {500, 1000}, s₀ = 14) the theorems describe mechanism, not the reported numbers.
   > (i) Of 2,400 fits, 6 stopped on a resource limit (counted as failures), 1,829 recovered S₀ exactly and 565 were posterior misses — S₀ was scored by the run but another scored model had a higher posterior; there were no search misses, and the final local search never changed the HPM.
   > (ii) The start is masked by *dilution* (each block's table treats the other blocks' signal as noise): the median start mass on S₀ is 10⁻¹¹–10⁻²⁶ per cell, while about 0.8 of the start mass lies within two extras of a subset of S₀.
   > (iii) Theorem 1's proof thresholds hold only from n ≈ 2·10⁶, its beta-min constant exceeds the executed signals by at least 43×, and its eigenvalue premise is unverified on the realised designs.
   > (iv) The start-rate bounds carry a 2^B factor that is ≥ 10³ at B = 14.
   > (v) The HPM at this size is delivered by Gibbs flips during the bridge.
   > We bound P(reported and wrong), not P(wrong | reported).

   **Where the numbers come from.**
   - (i): S-ELS.
   - (ii): O-DILUTE §7.
   - (iii): W2-VT03R R1 and F-REFINE ARCHITECTURE §7.
   - (iv): F-REFINE.
   - The last sentence: W5-LOCKBOOK STATEMENTS.tex.

   **What Felipe must decide.**
   - Whether to quote a "favourable from n ≈ …" threshold at all. The sources disagree: 590–730 (O-DILUTE, c → ∞ ceiling), 800–1,600 (W3-VEXP), and 1,050–3,200 (W5-FAVIID). I recommend omitting it, or quoting the W5-FAVIID empirical first-n with its source.
   - Whether to say "dilution" in the main text.
   - Whether to keep the "98% of fresh scores come from Gibbs flips" figure. It is from THEORY_PRIORITIES §5, preliminary, and no campaign run re-derived it.

---

## 2. Theorem by theorem: the eight paper targets

Columns: best current statement; status (the author's word); same-family check; cross-family check; repairs applied; premises that remain; source.

| # | Best current statement (one line) | Status | SF verification | XF verification (A-REV1–4) | Repairs applied | Remaining premises / caveats | Source |
|---|---|---|---|---|---|---|---|
| **Thm 1** (T03♯; T01, T02 lemmas) | 1 − π(S₀) = O_P(√(log n/n)); PIP/MPM consistency; P(global HPM ≠ S₀) ≤ 2E[1−π(S₀)] → 0; exact BB(1,p) tail T02(i♯) cuts the cutoff to m♯ ≈ s₀ log n | PROVED | VERIFIED (`W2-VT03R · REPORT.md` rows 1–26; no math GAP or ERROR) | VERIFIED under exactly its hypotheses (`A-REV2 · REVIEW.md §2 S03`) | Disclosure threshold corrected from 1.2·10⁵ to ≈ 2–2.5·10⁶ (`W2-VT03R R1`; `W6-FIXREV2 · STATEMENTS.md §1.2`); quantifiers sup_m P, g₀ fixed, "posterior, not reported HPM" | R1 (X fixed, s₀ fixed, p ≤ n^A), G, R, SE_λ(j₀), SE_w(m♯; g₀), BM-∞ or BM(c). Asymptotic only; "relevance at n = 200 nil" (W6-FIXREV2 card). The hoped-for m_n = s₀ + O(s₀ log n/log p) is **false** without SE (`W1-T03R · Prop. D`, COUNTEREXAMPLE) | `W1-T03R · REPORT.md §1 · Theorem T03♯`; statement of record `W6-FIXREV2 · STATEMENTS.md §1.2` |
| **Prop 1** (T07 + T06(i)) | HPM minimises 0-1 loss, MPM minimises Hamming loss; sharp size-prior ceiling (iff S*_{s₀} = S₀); a same-size swap cannot be fixed by any size prior; tie criterion | locked + PROVED additions (i′), (iii′) | VERIFIED* (`W5-LOCKBOOK · REPORT.md`: (i′) CORRECT, (iii′) CORRECT with amendment) | VERIFIED* for the sharp ceiling (`A-REV4 · BOOK_CHECK.md`); **ERROR B5** on the data paragraph "a wrong HPM implies a posterior miss" | B5 has no written repair. S-ELS now supplies the audit B5 asked for: 565 strict posterior misses, 201/488 strict same-size swaps at c = 0.5 (`S-ELS §3, §5`). Cite the data, not the implication | Within-size errors only. Formalised in Lean (`L-LEAN · T07Bayes.lean`, Fable fidelity GREEN) | `W2-BOOK · REPORT.md §2 · Prop. 1`; `W5-LOCKBOOK · STATEMENTS.tex` |
| **Thm 2** (T22 + T27, the start) | (i) deterministic start bounds [locked]; (ii) **EXP′ is a theorem**: every within-block addition log-BF = −½ log(n+1) − ν log(1−x) + bounded remainder, plus a data-computable certificate R1; (iii) favourable start at any reference S° under ZL/BO/F1–F3; (iv) CL(L) chain leakage ⇒ T27 masking rate p^{−c}n^{−c/2}; (v) LH realises masking + near-truth mass jointly; LH-iid at p ≫ n | (ii) PROVED; (iii) Thm 6-EXP PROVED, Thm 2-BO "PROOF SKETCH" (label only; W3-VEXP calls it a verbatim corollary of locked T22(iii)); (iv) PROVED; (v) PROVED | EXP′, Thm 3, Thm 4, Thm 5 (LH), Thm 6 VERIFIED (`W3-VEXP · REPORT.md` rows 1–21: "No mathematical ERROR in any W1 theorem"); LH-iid P1–P8 VERIFIED (`W5-VMASK`) | EXP′ VERIFIED*; Thm 3, Thm 4 VERIFIED (`A-REV2 §2 SEX`); W3-PXN P1–P5, Lemma B, P8 VERIFIED, **P6 GAP** (`A-REV3 · REVIEW.md`); LH exact-Gram Thm 5 **not XF reviewed** | Limit 0.52/c_* → 0.51/c_* (`W6-FIXREV1 §7`, `W6-FIXREV2 §3`); Thm 4 "iff" → sufficiency; deterministic chain required (H1-det); U1 constant (`W5-VMASK R2`) | H3 stays a premise of Thm 4. In-sample favourable regime for S3/S4/S6: W5-FAVIID Theorem B claims it, "2^B-free" (PROVED, author only; its REPORT still has template placeholders). Partition = groups is now a lemma (`W7-PART · Theorem B`, PROVED). Rates vacuous at n = 200 | `W1-EXP · REPORT.md · Thms 1–6`; `W3-PXN · REPORT.md §2`; `W5-FAVIID · PROOF.md §9`; `W7-PART` |
| **Thm 3** (repair: T37 → Theorem A + W; T24 → B′/B♯) | **A (exact, finite n):** the production search from S_c returns S₀ certified iff ℓ ≥ τ(S_c) and TD′ holds on the path, up to exact ties; A5 needs POS. **W (asymptotic):** PGD(η) + SE + BM-∞ (+ H1/H2/H3) ⇒ TD′_P w.p. → 1; masked LH needs the lattice form W_Lat. **B′/B♯ (Gibbs path):** P(S₀ not scored in H terminal rounds) ≤ P(Bin(H,c_*) < v) + Hη. **GU:** on isolated-R exact-Gram families every C ⊆ R repairs, no PGD needed | A: PROVED. W: PROVED (candidate). W_Lat: PROVED. B′: PROVED. GU: PROVED (candidate). Literal T37 TD(d,m): false (COUNTEREXAMPLE, `W1-T37R · Prop. 1`; `W3-VT37R · CEX-1`) | A VERIFIED (720 designs, 0 violations; `W3-VT37R`); W VERIFIED (`W5-VPGD · REFEREE.md`); B VERIFIED* (`W2-VT24G`) | A (A1)–(A4) VERIFIED* (`A-REV2 §2 S37`); A5(a), Lemma 0(b), D_S-iff, "weakest" prose ERROR; B VERIFIED* after F′, Prop U ERROR (`A-REV1`); **W, W_Lat, GU not XF reviewed** | POS added (R1-POS, XF VERIFIED); Lemma 0(b′) + three-way Prop F; Lemma T / Lemma NT for ties; Prop U′ (`W6-FIXREV1 §1`, `W6-FIXREV2 §2`; same-family, not re-reviewed) | Theorem C (C1, C2) stays PROOF SKETCH; C4 CONJECTURE (GU proves "a version" of it). **At n = 200 the search never moved (S-ELS)**, so the theorem explains no study fit. Lean: A1–A4, Lemma 0(a)(c), lattice Lemma 2(a) formalised; A5, B, C not | `W6-FIXREV2 · STATEMENTS.md §2.3 · Theorem A`; `W3-PGD · PROOF.md §4 · Theorem W`; `W5-VPGD · REPAIRS.md R6.2 · W_Lat`; `W1-T24G · REPORT.md · Theorem B`; `W7-SEP · PROOF.md · Prop. GU` |
| **Thm 4** (T21) | P(𝒪 ∩ {Ŝ ≠ S₀}) ≤ 2E₀δ₁ + P(𝒪̄ ∩ {S₀ ∉ 𝒮̄}) for every n, on the potential run under GUARD; routes (a), (d)/(d⁺), (e′) via Theorem B, (e-M); H24 retired | locked + PROVED (W2-BOOK Thm 4 C1) | VERIFIED* (`W5-LOCKBOOK`: (C1′)/(a)/(d)/(e′)/(e-M) CORRECT, (d⁺) sharpened) | No direct verdict; A-REV1 §7.4 verifies the same set inclusion inside T38; GUARD literal claim ERROR (`A-REV4`) | Needs 𝒢 ⊆ U (a stopped fit's partial HPM must count as a failure; `W5-LOCKBOOK · AUDIT.md G1`) | GUARD and SR are code facts read by HQ and W5-LOCKBOOK (same family). **Output convention is undecided:** strict 𝒪 vs HPM convention 𝒪_H (`W6-FIXREV1 §3`). Lean `t21_C1` formalised, GREEN | `W2-BOOK · REPORT.md §2 · Theorem 4`; `W5-LOCKBOOK · STATEMENTS.tex` |
| **Thm 5** (T38, main) | (0) composition; (a) favourable via iid draws; (b1) LS0 route, (M1)–(M3); (b1-LH)/(b1-LH-iid) all premises proved, with LS0; (b1′) D2 pilot discovery (no LS0); (b2) Gibbs path (no LS0): DELIV + REP; (c) polynomial cost | (0) PROVED; (a) PROVED-UNDER (F); (b1) PROVED-UNDER (M1)–(M3); (b1-LH) PROVED; (b1′) "PROVED (implication)"; (b2) "PROVED (implication)", **DELIV OPEN** in general; (c) PROVED-UNDER T32(i), see conflict §4.1 | (0) VERIFIED (`W3-VT38E`); (b1-LH), (b1-LH-iid), Lemma M, LS-score, Theorem b1 VERIFIED (`W5-VMASK`); D2 VERIFIED after constant repair | (0) VERIFIED* (`A-REV1 §7.4`); whole T38(b)-R as supplied **GAP** (`A-REV1`); D2 VERIFIED; W3-PXN joint LS0 route GAP (`A-REV3`); W4-SHARE M(b) **ERROR** (`A-REV3`) | All A-REV1 items repaired in `W6-FIXREV1 · T38_STATEMENT.md` (same family, **not re-reviewed**); LS0 must emit its centre **first** (`W6-FIXREV1`; `W5-LOCKBOOK` IMPL-EMIT: "mandatory, not cosmetic"); LS0 cost 1 + (ℓ+1)max_k[p + k(p−k)] | (b1) needs LS0 (a method change). No-LS0 LH routes: D2-LH (c = 1), B2-LH (STAB-LH), BG3 + LH-lock (sketch), F-SHARE F2 (sketch); none XF reviewed. (a) on S3/S4/S6: `W5-FAVIID · Cor. C3` (author only). "T38 explains n = 200": 0.1 (`W4-T38FULL` card) | statement of record `W6-FIXREV1 · T38_STATEMENT.md · Theorem 5 (T38)`; `W4-T38FULL`; `W5-VMASK §3`; `W5-B2ENV`; `O-BGIBBS` |
| **Thm 6** (T26 (i)–(ii)) | Ẑ/Z → 1 and PIPs → 0/1 truth in the favourable regime under one premise (P1): (T_n + 1)Δ_n → 0 with the **realised** T_n; output form; never conditioned on completion | Theorem A PROVED; Theorem B PROVED-UNDER T03 + T22(iii); Prop C (ORTH) PROOF SKETCH | Lemmas 1–3, Theorem A CORRECT; Theorem B CORRECT, CONDITIONAL; Prop C kept as sketch (`W5-LOCKBOOK`) | Theorem A VERIFIED*, Theorem B VERIFIED*; Prop C GAP; the "exact branch fails for p ≥ 18, n ≥ 22" aside is an **ERROR** (`A-REV4`) | ERROR aside: no repair written (PENDING) | At n = 200, Δ_n ≈ 1: the premise fails (W5-LOCKBOOK). Masked regime: O-STAGES `Theorem M` gives T* = log₂ A₀ + O(1), so (P1) fails there. (P1) on S3/S4/S6 via `W5-FAVIID · Cor. C2` (author only). F-DRAFT's W″ "O(1) stages" is false (`O-STAGES`, COUNTEREXAMPLE) | `W2-T26 · REPORT.md §2`; `W5-LOCKBOOK · STATEMENTS.tex` |
| **Prop 2** (T12 + T31(i)) | Frozen run: E[Ẑ] = Z; islandwise E[Ẑ_r PIP̂_rj] = Z·PIP_j; pooled × pooled is **not** an identity (bias −¾Cov); 0.05Ẑ is a one-sided 95% lower bound at output level; E[Ẑ \| completed] ≠ Z (COUNTEREXAMPLE) | locked + PROVED (a)–(e); (f) VAL-FP PROVED-UNDER | (a)–(e) CORRECT; (f) GAP (wording) (`W5-LOCKBOOK`) | (c) VERIFIED; (a,b,d,e) **GAP** (fixed-data scope); (f) GAP; GUARD literal claim **ERROR** (`A-REV4`) | GAPs and GUARD ERROR: PENDING (A-REV4 proposes restricting to statistical fields) | VAL-FP floating-point tolerance unmeasured (needs an R/C++ replay; `W7-SEC · T33` gives η but ε stays OPEN). O-PW2 adds a two-sided variance bound, vacuous at study scale with locked inputs only. Lean: T12(i.a) partial, with `hstep` as an explicit hypothesis | `W2-BOOK · REPORT.md §2 · Prop. 2`; `O-PW2 · REPORT.md` |

**What the table shows.**
- The posterior half (Thm 1, Prop 1) and the exact finite-n results (Thm 3 A, Thm 4) are the most reviewed.
- The main theorem (Thm 5) has a composition everyone accepts, but its masked part is reviewed only in the same family.
- The XF review of T38 (A-REV1) was of an older statement, and its repairs (W6-FIXREV1) have not been re-reviewed by Astra.

---

## 3. New results beyond the frozen list

| Result | Best statement (one line) | Status | SF verification | XF verification | Repairs | Remaining premises / caveats | Source |
|---|---|---|---|---|---|---|---|
| **Finite-n a posteriori certificates** | Per-fit, data-computable: Lemma M (Q_S decreasing, D_S increasing in S); C1 a one-sided global certificate; C3 exact relative certificates on any fully scored region; C4 box certificate; C5 posterior-miss certificate; C6 per-fit card. Upper bounds on π(Ŝ); **no** lower bound without PW2 or enumeration | PROVED (C2 PROVED-UNDER PW2) | `O-VCERT · REPORT.md §1`: Lemma M, C3, C4 VERIFIED (0 violations in 285,712 boxes); C1 VERIFIED conditional on W2-BOOK; C6 GAP → VERIFIED after R1, R2 | none | O-VCERT R1 (unscored-mass sentence, which had a counterexample), R2 (floating-point clause) | O-CERT §4 illustration is empty and no results were committed, so its numbers are unsupported. C6 final bound: O-CERT drops the P(𝒜) factor that O-VCERT keeps | `O-CERT · REPORT.md §3`; `O-VCERT` |
| **Predicted miss rates** | Exact finite-n laws for swap, superset and subset posterior misses, under a projection approximation (PA). One-move check on the study's own y reproduces observed misses within ±1 in 24/24 cells. Predictor T2: c = 1 43/40 vs 40/37 observed; c = 0.5 251/271 vs 230/259 | L0, T4, P5 PROVED; P1–P3 PROVED-UNDER PA | none | none | — | PA is an approximation; rigorous bracket OPEN. Says "4 no-output fits" vs 6 elsewhere (minor inconsistency) | `O-SWAP · REPORT.md §3` |
| **Dilution masking** | Exact start decomposition −log π₀(S₀) = visibility + competition − size (Thm E, Cor E1); exact law of #truths/#nulls under π₀ (Thm R); null score law is exactly Beta, as in pure noise (Lemma N); ranking ceiling for v3 **and any common σ²** (Prop S); population dilution formula (Prop D′) | Thm E, R, Lemma N, Prop S PROVED; Prop D′ PROOF SKETCH; Prop DM: (i)–(iii) PROVED, dilution clause SKETCH; Conj DM-asy CONJECTURE | none | none | — | Numerics on 480 regenerated fits, equal in law but not bit-identical to the study (numpy RNG): median π₀(S₀) 10^−15.7, π₀(R₂) 0.79, 0/480 favourable. Earlier: `W3-VEXP · Prop. D` (PROVED), `W3-PXN · Prop. W` (SKETCH) | `O-DILUTE · THEORY.md §1–7`, `REPORT.md` |
| **Weight stability, Theorem W** (draft's §5.3) | ORTH: two-sided χ²(π‖π₀) law; both ends concentrate; KL, TV → 0 always; χ² bounded iff 2Ar < 1 (divergent side lower bound e^{(L_n−C)/r}); ideal grid needs ≤ 2 stages (W′) | Theorem W (a)–(g) PROVED (d upper half restricted after review); W′ PROVED for the ideal grid; WS7 (masked: "reweighting cannot create the truth") PROVED | `O-WSTAB · review/CHECK_SEP_W.md` (independent same-family checker): verified except W(d) upper half (restricted by author) and F8 scope | none | F1 accepted, statement restricted | General BO: SKETCH; p ≍ n OPEN; method's restricted grid OPEN. **COUNTEREXAMPLE to F-DRAFT Theorem W(c) and W(b) on the divergent side** | `O-WSTAB · REPORT.md`, `PROOF.md WS1–WS8` |
| **Separation theorem** | SEP(A): iid start draws need Q ≍ p^c n^{c/2} (sharp); SEP(B): one-shot importance correction needs the same; SEP(C): start + one greedy search succeeds at O(p² log n) on LH; **no super-polynomial separation and no bridge-vs-search separation** in the frozen setting | SEP (A)(B)(C) PROVED; task clause (a) COUNTEREXAMPLE; Prop. GU PROVED (candidate) | none | none | — | Supports "moving off the start is needed", **not** "tempering is needed" (an HQ decision on the paper's spine). LH-iid parts rest on W3-PXN | `W7-SEP · REPORT.md`, `PROOF.md` (head 858004e) |
| **Partition lemma** | For iid Gaussian designs with within-group \|Σ\| ≥ ρ > ψ̄ ≥ cross-group and g_max ≤ B < 2g_min: P(v3 blocks ≠ groups) ≤ (2/(√π(1−ρ)))p²√n e^{−(n−4)I*}; exact structural theorem for complete linkage; partition never reads y | Theorem A, B, C PROVED; CE1–CE3 COUNTEREXAMPLE | none | none | — | At n = 200 the LH linked-pair rigorous bound is only 0.17 (Monte Carlo 1.5e-4). Which groups share a block when 2g ≤ B (the study's g = 5): OPEN | `W7-PART · REPORT.md §1` (head b2aa940) |
| **Stage-count theorem** | Greedy grid is the shortest valid grid; favourable sandwich N(w₊) ≤ T* ≤ N(w₋); masked two-state crossing T* = log₂ A₀ + O(1) (Theorem M) | Lemma 0, 1, Theorem G, L, F, M PROVED; Cor. W′ PROVED conditional on (LL); W‴ PROVED given PAIR | none | none | — | F-DRAFT's W″ "O(1)" is a COUNTEREXAMPLE. (LL) is undercut by O-WSTAB's counterexample for 2Ar > 1. No per-fit stage counts were exported from the study | `O-STAGES · REPORT.md` |
| **Naive-merge proposition** | Identifiable p = 2 cross-block proxy: local block posteriors and their product put mass → 1 on {1,2} while the full posterior puts mass → 1 on {1}; TV → 1; actual v3 is consistent on this family | Prop M COUNTEREXAMPLE (complete proof); v3 consistency PROVED | none | none (Astra-authored; A-REV4 uses it as the valid version) | — | F-DRAFT's own NM is **ERROR** per A-REV4 (O_P(1) remainder false); use A-DRAFT's. It refutes naive union, **not** Song–Liang's full method (comparison OPEN) | `A-DRAFT · REPORT.md §3.1 · Proposition M` |
| **E[h] consistency** | Fixed data, N → ∞: every §2.1 estimator → μ_h, Ẑ_r/Z → 1, uniform PIPs (Theorem A); n-indexed budgets under (P1) (Theorem D, no factor L); bounded-h-to-generating-value is false (COUNTEREXAMPLE) | Theorem A, D PROVED (candidate); Cor A1 PROVED from locked T12 | Astra-on-Astra: VERIFIED* (`A-REV4`) | (author is Astra; no Claude check) | — | v3 has no general h-estimator implemented; (P1) unproved on masked designs | `A-DRAFT · REPORT.md §2` |
| **PW2 / evidence variance** | Exact variance identity for the island evidence ratio (Theorem A, no mixing assumption); two-sided non-asymptotic bound N·V_T ≈ Σσ²_{s,T} (Theorem B) that removes PW2 as a hypothesis; PW2 holds with a_t = (S_t − S_{t−1})₊ | A, B, C PROVED (candidate); "PW2 with a_t = χ²_t" COUNTEREXAMPLE (p = 6 exact) | none | none | — | Valid but vacuous at study N, T with locked inputs only; needs an L² mixing premise. Consistent with O-WSTAB WS8 (PW2 under IID idealisation PROVED; actual system OPEN) | `O-PW2 · REPORT.md §1` |
| **Masked-regime meaning of Ẑ and PIPs** | E[(Ẑ_r/Z)·PIP error] ≤ δ₁ + ρ̄ + u_π in every regime (M1): wrong PIPs cannot come with accurate evidence; accurate PIPs with collapsed evidence can and do (N-a); no first-moment evidence restart (M3); PIP restart theorem R/R′ conditional on DELIV-POP | M1, M2, M3, N-a PROVED; R PROVED as composition; R′ conditional; DELIV-POP OPEN; N-b, N-c SKETCH | none | none | — | DELIV-POP is strictly stronger than T38's DELIV | `F-MASKPIP · REPORT.md §3` |
| **No-LS0 masked discovery** | BG3: final run alone scores S₀ if the start set is "locked" (supersets of S°) and the terminal rounds go downhill; LH-lock supplies the premises for p fixed, every c. F1: closed-class delivery; F2 its LH instance | BG3, BG1, BG2, Lemma R PROVED; LH-lock PROOF SKETCH (γ₁ gaps checked by enumeration only); F1 PROVED; F2 PROOF SKETCH | none | none | — | Same "superset class" idea found independently by both runs. Fails on posterior-barrier designs (W4-SHARE PB) | `O-BGIBBS · REPORT.md §2, §3.7`; `F-SHARE · REPORT.md` |
| **Start-law fixes** | Mixture of two partitions (B-merge) gives π₀(S₀) ≥ ½ − o_P(1) on LH and T38(b) via route (a) **without LS0** (Thm B3); common σ̂² removes dilution only under in-sample BO (Thm C1, Lemma S1, Thm S2) and floods the start in random designs (Thm S6) | B1, C0, C1, C2, C3 PROVED; B3 PROVED-UNDER; S0, S1, S2, S3, S6 PROVED; S4 PROVED-UNDER | none | none | — | See §6 | `O-MIX · REPORT.md`; `F-SIGMA · REPORT.md` |
| **Secondary lemmas** | T05 (oracle gap under ORTH; "loses a √log n factor" is false multiplicatively at p = n^a); T33 (numerical_failure impossible at n = 200; engine `error_bound()` is not a bound for n ≥ 10⁵); T32(i) re-checked | all PROVED (same-family check) | W7-SEC re-checked W5-LOCKBOOK's T32(i): "no error in the count" | none | — | `error_bound` fix recommended (implementation, not method) | `W7-SEC · REPORT.md` |
| **Data fact: E_LS ledger** | On the 2,400 PROD-H fits: final LS 0 moves (2,394/2,394); S₀ scored in all completed fits; 565 strict posterior misses, 0 search misses; the 541 "unrepaired" centres are all forced by Lemma 0 | data (not a theorem) | — | — | — | Says nothing about whether repair works, because repair never ran | `S-ELS · REPORT.md` |

---

## 4. Conflicts and open disputes

Each entry gives both positions and what would settle it.

### 4.1 T32(i) status (affects Thm 5(c))
- **For PROVED:** `W5-LOCKBOOK · REPORT.md` item 4 ("T32(i) is PROVED"). `W7-SEC · REPORT.md` re-counted it and found "no error in the count".
- **Still CONJECTURE:** `W6-FIXREV1 · T38_STATEMENT.md` dependency k1 ("CONJECTURE (checked as a valid loose bound by W3-VT38E)"), and `W7-SEP` input I11.
- The registry records it as PROVED (moved by W5-LOCKBOOK).
- **To settle:** HQ updates the T38 statement of record. An XF check of the count is cheap.

### 4.2 Is there a masked theorem without LS0?
- **"OPEN":** `W4-T38FULL` ("Without LS0, the paper has no masked-regime consistency theorem…") and `W6-FIXREV1` ("Not claimed: Masked-regime consistency without LS0 on an explicit family (OPEN)").
- **Candidates exist:**
  - `W5-B2ENV` NB′-LH / D2-LH: "the paper's first masked instance **without LS0**";
  - `W5-VMASK R1`;
  - `W5-B2ENV` B2-LH under STAB-LH;
  - `O-BGIBBS` BG3 + LH-lock;
  - `F-SHARE` F1/F2.
- **To settle:** XF verification (§8, task 1 = F-REFEREE R1).

### 4.3 W4-SHARE Prop. M(b) (no posterior barrier near the truth)
- **SF:** `W5-B2ENV · REFEREE.md`: M(b) is a PROOF SKETCH as labelled, "Upgraded on LH to PROVED" (Prop M-LH).
- **XF:** `A-REV3 · REVIEW.md` gives **ERROR**:
  - the quadratic equality is used as an expansion (exact gain/n → ½ log 2, not ¼);
  - "vanishing crossing temperature" is false under BM-C;
  - the §7 exit-loss simplification is an ERROR (two-state counterexample).
- A-REV3 did not read W5-B2ENV. Nobody has checked whether M-LH, which uses EXP′ rather than the quadratic expansion, is affected.
- M(b) is also an input to F-MASKPIP N-c and F-REFEREE R1.
- **To settle:** include M-LH in task 1, and apply A-REV3's suggested repair (exact RSS expansion, BM-∞ only).

### 4.4 W3-PXN P6/P7 (the p ≫ n masked instance)
- **SF:** `W5-VMASK`: VERIFIED, cosmetic errors only.
- **XF:** `A-REV3`: P6 **GAP** (Lemma Tr used beyond its stated range; Beta shape (n−2−s)/2 vs (n−3−s)/2), P7 GAP, the joint LS0 route GAP.
- Both agree on the U1 constant error. Neither side has a counterexample to the lattice conclusion.
- **To settle:** Astra re-review with W5-VMASK's repairs in hand (§8, task 4).

### 4.5 The common-σ² start
- **O-MIX §1/§10:** (C) "is the right tool for the n = 200 dilution masking".
- **Against:** `O-DILUTE` and `F-SIGMA` show it floods the start in random designs, even with the oracle σ².
- O-MIX's evidence is an exactly block-orthogonal toy (BO-D).
- **To settle:** already settled on the evidence; I side with O-DILUTE and F-SIGMA. The free post hoc Step 0 (`F-SIGMA §10`) would confirm on the real fits.

### 4.6 Lemma 0(b): "every unrepaired centre is a posterior miss"
- **W1-T37R:** "0/541 is forced by monotonicity".
- **Against:**
  - `W3-VT37R` gives **ERROR** (CEX-2, plus "233 of 234 non-repaired sampled centres ended at a model with F ≥ F(S₀)" in its production rerun from *sampled* centres);
  - `A-REV2` gives ERROR on the claim and on W3-VT37R's own repair R2;
  - `W6-FIXREV2` replaces them with Lemma 0(b′) and the three-way Prop. F.
- **Data:** `S-ELS` finds that on the actual fits all 541 are forced by Lemma 0, and that "the referee's sampled F(S₀) > F(S_c) cannot be reproduced".
- **Reading.** The logical claim is false in general, but true on the study data. The 233/234 figure refers to W3-VT37R's sampled centres on regenerated data, not to the fits' own centres. That is a likely but unconfirmed explanation.
- **To settle:** have W3-VT37R's script rerun on PROD-H, with case IDs.

### 4.7 Astra versus same-family verifiers (settled toward Astra; repairs not re-reviewed)

| Item | Same-family position | Astra position | Resolution |
|---|---|---|---|
| Prop U | VERIFIED as bookkeeping (`W2-VT24G`) | ERROR (`A-REV1`) | W6-FIXREV1 agrees with Astra, Prop U′; Theorem B unaffected |
| Lemma S attainment | "tight" (W1-T38E, W3-VT38E) | ERROR for f ≤ 1−e (A-REV1) | Lemma S′ |
| E3(ii) | VERIFIED (W3-VT38E) | ERROR, needs q < 1 (A-REV1) | E3′; unused downstream |
| EXP′ limit constant | 0.52/c_* (W3-VEXP did not flag) | 0.51/c_* (A-REV1, A-REV2) | corrected |
| TD′_P ⇔ (L) ∧ D_S | VERIFIED (W3-VT37R) | ERROR with exact ties (A-REV2) | Lemma T, Lemma NT |
| T38(b)-R whole | VERIFIED (W3-VT38E) | GAP (A-REV1) | W6-FIXREV1 rewrite; whether it matches A-REV1 §7 is unchecked |
| T03 threshold | 1.2·10⁵ (W1-T03R) | ERROR (A-REV2, agreeing with W2-VT03R) | 2·10⁶ |
| W3-VT37R repair R2 | PROVED | ERROR (A-REV2) | Prop F |

The only disagreement **with** Astra: `W6-FIXREV2 §3.1` disputes A-REV2's table wording "initial centre is the truth = trivial success". A search started at S₀ moves away unless (L) holds at S₀; CEX-2 shows +7.21 nats. A-REV2's own §4.2 text is consistent with W6.

### 4.8 Same-family internal disputes
- **Theorem W, region form, on masked LH.** F-REFINE ARCHITECTURE/CARDS call it "the general sufficient condition for (M2)". `W5-VPGD · REPAIRS.md R6.1 · Prop. T` shows it fails with an exact tie on LH with c ≥ 2 (20/20; D_S fails in 200/200 fits). Settled: cite W_Lat with Prop. LH-PGD.
- **LH-LAT margin "m₀ is sharp".** `W4-T38FULL` says it is. `W5-VMASK R5` shows it is not sharp on 32/94 heterogeneous settings, with ratios down to 0.002. Settled: use the exact m₀♯.
- **ORTH joint family.** `W2-T26 · Prop. C` is a PROOF SKETCH, but `W4-T38FULL` writes "no open statistical input". A-REV4 rates it GAP. Keep it as PROOF SKETCH.
- **The ψ ≥ ρ boundary of LH.** W3-VEXP and W4 call it a "cliff". W5-VMASK calls it a transition to the favourable regime: "the masking disappears", and the method is not hurt. Both are true; the paper should say it is a transition.
- **LH-iid "single unverified run".** `W6-FIXREV1` still says this. W5-VMASK verified it (same family). The XF verdict is GAP (4.4).
- **Lemma M (T38FULL) vs DOM in F-SHARE.** F-SHARE saw a sample-level DOM failure (LH20, n = 1600, +4.7 nats), while O-BGIBBS's population gap C2 is positive (0.030). This is a finite-n fragility, not a contradiction.

### 4.9 Fable (F-DRAFT) versus later runs
- **F-DRAFT W2 and NM:** "PROVED modulo …" versus **ERROR** (`A-REV4`, with explicit counterexamples).
- **F-DRAFT W4:** PROOF SKETCH versus GAP.
- **F-DRAFT W(c), and W(b) on the divergent side:** COUNTEREXAMPLE (`O-WSTAB`).
- **F-DRAFT W″ "O(1) stages":** COUNTEREXAMPLE (`O-STAGES`).
- **A-DRAFT vs F-DRAFT on Song–Liang.** F-DRAFT says NM "disposes of" it; A-DRAFT says the counterexample "refutes naive union, not Song–Liang's second selection stage".
- No settlement is needed: use A-DRAFT Prop M, O-WSTAB Theorem W and O-STAGES Theorem M.

### 4.10 Agents versus their own task specs
- **W7-SEP:** the task's claim that start-only methods fail is false on LH (Prop. GU). "Tempering is needed" is not supported. This is a decision for HQ and Felipe on how the paper motivates the bridge.
- **W7-PART:** the task's "9 ≤ g ≤ 16" is false at n = 200 (B = 14).

### 4.11 F-REFEREE versus the cross-family record
F-REFEREE used only A-REV1 and A-REV2. Its M5, M8 and R6 call W3-PXN, W4-SHARE, W2-T26 and W2-BOOK unreviewed, but A-REV3 and A-REV4 had reviewed them, some with ERROR/GAP verdicts. Its rebuttals also lean on two claims Astra flagged:
- "all 565 misses are posterior misses" as a logical consequence (A-REV4 B5 ERROR; now true *empirically* via S-ELS);
- F-DRAFT Theorem W for χ² → ∞ (W2 ERROR). O-WSTAB Theorem W(e) can replace it, for ORTH only.

### 4.12 Output convention
- W2-BOOK and A-REV1 use 𝒪_H ("usable HPM").
- W4 uses the strict 𝒪 = {exact, completed}.
- W6-FIXREV1 proves both and leaves the choice to HQ. Under 𝒪_H, routes (a) and (b2) carry an extra term P(SMC ∩ 𝒜ᶜ) that no result controls.
- **To settle:** HQ and Felipe choose. I recommend the strict 𝒪, because it needs no extra term.

### 4.13 Numerical inconsistencies the paper must reconcile
| Quantity | Values found | Sources |
|---|---|---|
| Start mode at n = 200 | "misses 6–12 of 14 truths" | W3-VEXP, F-REFINE, S-PAPER |
| | "holds 2.5–6 of 14" | O-DILUTE |
| | 7 of 14 masked | F-SIGMA |
| n where the start turns favourable | 590–730 | O-DILUTE (c → ∞ ceiling) |
| | 800–1,600 | W3-VEXP |
| | 1,050–3,200 | W5-FAVIID (empirical first n with median π₀(S₀) > ½: 1,600 or 3,200) |
| Beta-min shortfall | ≥ 43× | F-REFINE, W6-FIXREV2, F-REFEREE |
| | "about 100×" | THEORY_PRIORITIES; predates T03♯ |
| SE columns at n = 200 | ≤ 114 | cap K binds; F-REFINE |
| | 215–229 | THEORY_PRIORITIES; old cutoff |
| Stopped fits | 6 | S-ELS, W5-LOCKBOOK, THEORY_PRIORITIES |
| | 4 | O-SWAP |
| LS0 cost | "about ℓ·p" | THEORY_PRIORITIES |
| | 1 + (ℓ+1)·max_k[p + k(p−k)] | A-REV1, W6-FIXREV1, W5-VMASK R7; ≈ 1.7·10⁵ at p = 1,000 |
| Terminal segment | L+4 | W1-T24G, W1-T38E |
| | L+5 after resampling | W2-PREM, W2-BOOK, W6-FIXREV1 (resolved: both are right for different boundaries) |

**Recommendation.** Use S-ELS for counts; O-DILUTE for start masses (with its regenerated-data caveat); W6-FIXREV1 for the LS0 cost; drop the "favourable from n ≈ …" threshold or attribute it.

### 4.14 Registry versus reports
`S-REGISTRY · REGISTRY.md` (head 3d88da6) predates a lot of work. These landed after it or were only partly read:
- W7-SEP, W7-PART and W7-SEC (the registry saw notes only);
- O-DILUTE, O-STAGES, F-SIGMA, F-REFEREE, O-VCERT, S-ELS, L-LEAN;
- the F-SHARE REPORT (the registry saw BRIEF only);
- O-BGIBBS BG3 (the registry lists BG1 and LH as the headline);
- the W3-PGD final REPORT (the registry calls it a stub).

The registry marks `Lemma0(b)` "per-fit data … still unextracted (OPEN)"; S-ELS has now extracted it. Its LOCKABLE list (48 strict candidates) is still the right starting point. It needs one rebuild before Felipe uses it for adoption.

### 4.15 Label collisions (fix before the paper)
- "Theorem A/B/C" each name results in W6-FIXREV2, W1-T24G, O-PW2, W7-PART and W2-T26.
- "Lemma S" names three different lemmas; "Lemma M" three; "Prop M" four (A-DRAFT, W4-SHARE, F-MASKPIP M1–M3, O-CERT Lemma M).
- "Lemma U" (W2-PREM vs W3-PXN), "Lemma 0" (W6-FIXREV2, O-STAGES, O-WSTAB) and "Lemma P" collide.
- "CE1" means three things; "W′" two; "Theorem W" two (W3-PGD repair vs F-DRAFT/O-WSTAB weight stability).
- "(e′)" means T37 in FABLE_REVIEW and Theorem B elsewhere.

---

## 5. The referee's view (`F-REFEREE · REFEREE_REPORT.md`, `RESPONSE_PLAN.md`)

**Recommendation (verbatim):** "**major revision.** The theory section is unusually candid, internally consistent, and the composition inequality (Theorem 4) is exactly the right organising principle. But … its headline theorem (Theorem 5(b1)) is about an algorithm (v3 + LS0) that the reported simulations did not run."

**The one change it asks for:** "*Make Theorem 5(b) a theorem about the algorithm that produced the tables, on the explicit family LH, and show its predicted transition with the production code at growing n.*"

The tags below are mine, as of this snapshot:
- *done*: the response's evidence exists and has had at least one independent check;
- *in progress*: candidate material exists but is unverified;
- *open*: nothing yet.

| # | Objection (short) | Planned response | Tag | What exists now |
|---|---|---|---|---|
| M1 | All theory is asymptotic; thresholds ≈ 2·10⁶; simulations at n = 200 | Say so once, up front; LH scaling study (R2); explicit first-n table (R9) | **open** (R2, R9 not started) | Partial: S-ELS supplies the decomposition of the 2,400 fits; O-SWAP predicts miss rates (unverified); O-CERT certificates (SF verified). None quantifies a theorem at n = 200 |
| M2 | Headline needs LS0, which the simulations did not run | Restate 5(b) for v3 without LS0 on LH (R1); LS0 as remark; O-LS0 diff (R12) | **in progress** | No-LS0 candidates: D2-LH, W5-VMASK R1, B2-LH, BG3 + LH-lock, F2, GU. None XF reviewed. O-LS0 report not landed |
| M3 | No-LS0 routes (b1′), (b2) are hypotheses-as-conclusions | One explicit family LH (R1); routes to supplement; S-ELS | **in progress** | S-ELS landed (done as data). R1 not run |
| M4 | Favourable regime is where the sampler is unnecessary; need a separation theorem and a masked Ẑ/PIP statement | W7-SEP as spine; F-MASKPIP M1/M2 | **in progress, with a twist** | W7-SEP landed but **refutes** "tempering is needed"; it supports "moving off the start is needed". F-MASKPIP M1–M3 PROVED (unreviewed). The rebuttal's χ² → ∞ citation must switch from F-DRAFT W (ERROR in W2) to O-WSTAB Theorem W(e) / WS7 |
| M5 | 2^B factor; (P1) circular; ORTH sketch | 2^B-free rate (R6); stage-count theorem (R5) | **in progress** | W3-PXN P3 (2^B-free on LH-iid) is XF VERIFIED by A-REV3. W5-FAVIID Theorem B (2^B-free on S3/S4/S6) is author only, with an unfinished REPORT. O-STAGES gives T_n theory: favourable O(1), masked log₂ A₀ + O(1) |
| M6 | No positioning vs Yang–Wainwright–Jordan 2016, Zhou–Yang–Vats–Roberts 2022 | Relation paragraph (R3); adopt A-DRAFT wording | **open** | A-DRAFT §1 audit of six works exists; it does not cover these two |
| M7 | Ẑ/PIPs meaningless in the masked regime; only Markov bound | F-MASKPIP M1/M2 (R8); one-sided 0.05Ẑ; islandwise product | **in progress** | F-MASKPIP landed. O-PW2 two-sided bound landed but vacuous at study scale. O-CERT/O-VCERT certificates landed |
| M8 | All verification is same-family; T32(i) conjecture; SR/GUARD as hypotheses | T32(i) (W7-SEC); code audit (R10); self-contained supplement (R11) | **in progress** | T32(i) PROVED + re-checked (**done** at SF level). W5-LOCKBOOK code audit by reading (same family). A-REV3 and A-REV4 had already reviewed four of the "unreviewed" items. Still no XF review of Lemma M, LS-score, LH-LAT, Theorem W, or anything from waves 5–7 / O / F |
| m1–m20 | Notation clashes, self-contained statements, branch names in text, etc. | All accepted; R11 and R7; edits | **open** | R11 not started; label collisions now listed in §4.15 |

---

## 6. Method-change evidence

The O-LS0 data have **not landed** (`theory/O-LS0`: scripts only; `data_hash_check.csv` shows 5/7 `match=FALSE`, which nobody has interpreted).

| Change | What it buys (theory) | What it fixes at n = 200 | Cost | Risk | Evidence | Recommendation (source) |
|---|---|---|---|---|---|---|
| **None (v3 as run)** | Thm 5 (0), (a); masked LH via D2-LH (c = 1), B2-LH (STAB-LH), BG3 + LH-lock (sketch) | nothing to fix in search: 0 search misses (S-ELS) | 0 | the no-LS0 masked routes are unverified | S-ELS; LH simulations in O-BGIBBS, F-SHARE, W5-B2ENV, W7-SEP (S₀ always scored) | F-REFEREE: make this the headline if R1 passes |
| **LS0** (local search from the exact start mode, centre emitted first) | Thm 5 (b1)/(b1-LH): every premise proved on LH, SF verified | **cannot fix posterior misses**, which are all of the misses; start mode is 8–14 moves away in S4/S6 with ℓ = 10–11 | 1 + (ℓ+1)max_k[p + k(p−k)] ≈ 1.7·10⁵ scores at p = 1,000, about 1–3 s per fit (O-MIX §5); post hoc | none to locked results; `emit_centre = true` is mandatory (W5-LOCKBOOK) | W3-PXN post hoc on study designs: S₀ scored 113/128 when \|S̃₀ Δ S₀\| ≤ ℓ+1, 13/32 beyond; LH 90/90 (W4), 386/386 (W7-SEP). **O-LS0 data check: missing** | Approved conditional on O-LS0 (SR_AUDIT); O-MIX: "Keep LS0 as the main theorem's route" |
| **Mixture of block starts (B-merge)** | Thm B3: T38(b) on LH without LS0, through route (a), the strongest route; also helps Ẑ/PIPs in the masked regime | does nothing for dilution (O-MIX: "(B) on dilution" fails) | ≤ \|E\|·2^{2B} extra table scores (capped at 16); < 5% of SMC scoring; S5 degenerates to base | T22(ii-a) becomes a sandwich; downside bounded by log 2 | exact p = 16/20 toys: π₀(S₀) 10^−0.3…−0.4 vs base 10^−2.2…−5.5 | O-MIX: "If one start change is made, choose (B-merge)" (needs a performance pilot and new runs) |
| **Common σ̂² tables** | Route (a) without LS0 only under in-sample BO (F-SIGMA Thm S4: "vacuous as an improvement" over v3); nothing for cancellation (Thm S3, O-MIX C3) | **makes it worse**: oracle σ² gives median log₁₀π₀(S₀) −690 and π₀(R₂) = 0 (O-DILUTE, 480 fits); −1,303 in F-SIGMA IID500 | ≈ 0 extra scores; HPM must ingest log m(U) | floods the start; re-derive T22(iii), T27, EXP′, W1-EXP Thms 3–6 | only BO toys favour it (O-MIX BO-D −0.27 vs −1.51) | O-DILUTE: "Do not adopt it." F-SIGMA: "should **not** be deployed as specified." **Reject** |
| **Residualised / backfit tables** | none proved yet; validity via F-DRAFT Prop P(i) / F-SIGMA Lemma S0; T22(iii) must be restated | the only candidate that attacks dilution: O-DILUTE pilot median π₀(S₀) 10^−1.0, 378/480 favourable, π₀(R₂) 0.71; weak in S5 and in S4 at c = 0.5 | (sweeps + 1) × table work; about 3 s per fit to recompute (F-SIGMA Step 2) | unknown; changes the start; needs a full-sampler pilot | pilot on regenerated data only | O-DILUTE, F-SIGMA: flag for HQ and Felipe; run F-SIGMA Step 0 (free, post hoc) first |
| **(B) + (C) combined** | both mechanisms | — | sum of re-derivations | sum | none | O-MIX: "coherent", but costly. Superseded now that (C) is rejected |
| **Reporting-only diagnostics** | F-MASKPIP path-departure diagnostic; O-CERT per-fit card | honest per-fit uncertainty | free / about 2·10⁴ scores post hoc | none | none committed (O-CERT §4 empty) | worth adding to the paper's supplement |

**Bottom line.**
- No method change improves the study's numbers through *search*, because there are no search misses.
- The only change that might help the study's numbers is a start change aimed at dilution. That means residualised tables, which are unproven and piloted only on regenerated data.
- For the *theorem*, LS0 is the cheapest certain route. The no-change LH routes are close, pending XF review.

---

## 7. Lean (`theory/L-LEAN`, head d9c2f2c)

**Formalised, with a green build.** Per `STATUS.md` and `DECL_STATUS.md` (87 declarations, 87 proved, 0 with `sorry`) and `AXIOMS_RECORD.txt` (only `propext`, `Classical.choice`, `Quot.sound`). I did not rebuild it: no Lean toolchain here. The grep agrees: 0 `sorry`, 0 `axiom`, 0 `admit` in the live sources.

| Target | Lean names (main) | Scope and caveats |
|---|---|---|
| T21 (C1) and the decomposition forms | `t21_C1`, `t21_decomposition`, `t21_decomposition'`, `hpm_eq_truth`, `markov_half` | Abstract probability space; Ŝ any maximiser over 𝒮 on Uᶜ. **Routes (a)–(f) and the H03 asymptotics are not formalised** |
| T07 (i), (i′), (ii)(a)(b)(c), (iii)(a)(b)(c), Lemma psi | `ceiling`, `no_size_prior_repairs`, `ceiling_sharp`, `hpm_min_risk01`, `mpm_min_riskH`, `capped_mpm_min_riskH`, `reported_truth_needs_unscored`, `excess_riskH_le`, … | Tie order as an injective rank; complete |
| T11(iii) | `t11_miss_pi`, `t11_miss_iid`, `t11_miss_iid_real` | Conditional-on-𝓒 statement read pointwise |
| T37 Theorem A | `theoremA1` (+ converse), `theoremA2`, `theoremA3`, `theoremA3_hpm` (added after review), `pd_of_reach`, `lemma2a`, `theoremA2_lattice`, `theoremA3_lattice`, `card_le_of_mem_Rad` | TD′ as a hypothesis (it is the theorem's assumption). **Not formalised:** A5, Theorems B and C, the move-count identity τ = m + e − σ |
| T12(i.a) | `invariance_step`, `resample_move_step`, `unbiased_of_step` | **Partial:** the resample–move recursion `hstep` is an explicit hypothesis; the island's probability model is not formalised (`T12_PLAN.md`, "one focused session") |

**Fidelity.**
- **Fable** (same family): "OVERALL: GREEN", with no objections. Its 12 minor remarks are mostly adopted (`fidelity/FABLE.md`, `ADVISER_DECISIONS.md`).
- **Astra** (cross family): the run **did not finish**. `ASTRA_raw.md` is empty. Its partial log (`ASTRA_stderr.txt`) says it "found a substantive coverage gap in T37: the A2 statements omit the exact move-count identity and lower bound. The A3 statements establish return and certification, but omit the source's conclusion about the reported HPM." The second point was fixed afterwards (`theoremA3_hpm`). The first is now documented as not formalised.
- So the fidelity check has passed once in the same family. Cross-family fidelity is **incomplete**.

---

## 8. Next 10 tasks, ranked

These are ready-to-run specs. Each follows `theory_campaign/PROTOCOL.md` (branch `theory/<ID>`, write only under `theory_campaign/<ID>/`, push after each step, protocol status words, Python only, fixed seeds). The ranking is value to the paper per unit cost. Tasks 1, 3 and 4 decide the headline.

### 1. XV-NOTWEAK: cross-family verification of the no-LS0 masked theorem on LH (Astra; = F-REFEREE R1)
- **Goal:** decide whether Thm 5(b) can be stated for v3 as run.
- **Read:**
  - `W5-B2ENV · PROOF.md` §2 (Lemma OF, Lemma 2.1–2.2, Theorem NB′-LH, Cor. D2-LH), §3 (Prop. M-LH), §4 (Lemma J, Lemma T, Prop. CONF, Lemma R1, Theorem B2-LH, STAB-LH);
  - `W5-VMASK · REPAIRS.md R1`;
  - `O-BGIBBS · REPORT.md` §2–3 (Lemma R, BG1, BG2, BG3, Prop. LH-lock, §3.7);
  - `F-SHARE · PROOF.md` (F1, Lemma 1.2, F2);
  - `W1-T38E` D2 with `W6-FIXREV1 · CONSOLIDATED.md §5` (D2-∞).
- **Must answer:**
  - (a) D2-LH for c = 1: VERIFIED / GAP / ERROR.
  - (b) Is Prop. M-LH affected by A-REV3's ERROR on W4-SHARE M(b) (quadratic expansion; BM-C scope)?
  - (c) BG3 as a deterministic statement, and whether LH-lock's γ₁ gaps can be proved in general.
  - (d) B2-LH's dependence on STAB-LH: where exactly STAB-LH fails, for example (ρ, ψ) = (0.85, 0.5).
- **Deliverable:** `REVIEW.md` with a verdict table and reproduction scripts.
- **Success:** at least one no-LS0 route VERIFIED on an explicit family.

### 2. LH-LOCK: prove BG3's premises on LH in general (Opus, high)
- **Goal:** upgrade `O-BGIBBS · Prop. LH-lock` from PROOF SKETCH, and close F-SHARE F2.
- **Read:** O-BGIBBS §3.7, F-SHARE §3–4, W7-SEP Prop. GU (Lemma GU-1, GU-2), W1-EXP Thm 5, W4-T38FULL Lemma M.
- **Tasks:**
  - prove the γ₁ population gaps (C1) deletion, (C2) swap and (C3) hub addition for all (ρ, ψ, g, c) with |ψ| < ρ;
  - give a polynomial order constant;
  - extend from p fixed to p ≤ (1−c₀)n;
  - unify the "superset class" arguments of BG3, F1/F2 and GU into one lemma.
- **Deliverable:** `PROOF.md` and `REPORT.md`, with exact checks at p ≤ 20.
- **Run alongside task 1:** task 1 checks what exists; this task closes what is sketched.

### 3. O-LS0-FINISH + LEDGER-CHECKS (data, Owls/R; extends the O-LS0-WRAP run HQ already launched)
- **Goal:** meet the condition on Felipe's LS0 approval.
- **Tasks:**
  - report LS0 post hoc on the 2,400 regenerated datasets: scored/certified by scenario, split by |S̃₀ Δ S₀| ≤ ℓ+1, every HPM change, cost;
  - **interpret the 5/7 `match=FALSE` rows** in `data_hash_check.csv` before using any result;
  - add two small checks:
    - rerun W3-VT37R's `PROD` sampled-centre experiment on PROD-H with case IDs, to settle §4.6;
    - export per-fit stage counts (`length(frozen$grid) − 1`, pilot count) for O-STAGES.
- **Success:** a yes/no on the approval condition ("changes few or no reported HPMs, never turns correct into incorrect beyond posterior-mode corrections, negligible compute").

### 4. XV-MASKED-LS0: cross-family review of the LS0 route (Astra)
- **Read:**
  - `W4-T38FULL · T38_PROOF.md §3` (Lemma LS-score, Lemma M, Theorem b1, Prop. LH-LAT), with `W5-VMASK` R1–R7;
  - `W3-PXN` P6/P7 re-reviewed **with** W5-VMASK's repairs (A-REV3 did not read them);
  - `W5-VPGD · REPAIRS.md R6.2–R6.3` (W_Lat, LH-PGD);
  - check that `W6-FIXREV1 · T38_STATEMENT.md` matches A-REV1 §7's repaired formulation.
- **Deliverable:** `REVIEW.md` verdict table.
- **Why:** Thm 5(b1) is the current headline, and its new lemmas have never been seen by a second family.

### 5. LH-SCALE: the production code on LH at growing n (compute, NOTS; = F-REFEREE R2)
- **Design:** 3 × 4 × 2 × 100 fits; n ∈ {400, 1600, 6400, 25600}; g = 9; ρ ∈ {0.6, 0.85}; ψ ∈ {0.3, 0.5}; s₀ = 2c + 4; v3 as run, plus LS0 post hoc with `emit_centre = true`.
- **Report:**
  - P(Ŝ = S₀), and which mechanism first scored S₀ (pilot, bridge Gibbs, terminal, LS0);
  - π₀(S₀) against the T27 rate;
  - stage counts.
- **Why:** it is the referee's single compute ask, and the only way to show the predicted transition.
- **Note:** (ρ, ψ) = (0.85, 0.5) is where STAB-LH fails, so it doubles as a stress test.

### 6. T38-RECORD: one statement of record for Thm 5 and a registry rebuild (Opus, medium)
- **Goal:** produce `T38_STATEMENT.md` v3, merging:
  - W6-FIXREV1;
  - T32(i) PROVED (W5-LOCKBOOK, W7-SEC), which removes the CONJECTURE dependency of (c), leaving the same-family status of T32(i) and W7-SEC's fp-pilot addendum;
  - the no-LS0 candidates with honest statuses;
  - W5-VPGD (cite W_Lat, not the region form);
  - W5-VMASK R5 (m₀♯);
  - the output-convention options.
- **Also:**
  - rebuild `S-REGISTRY` with every branch in `SNAPSHOT.md`;
  - rename the colliding labels (§4.15);
  - update S-PAPER's source comments and disclosure items 5–6 from S-ELS.
- **No new mathematics.** It is hygiene, but every downstream reader needs it.

### 7. XV-NEW: cross-family review of the new results (Astra, split in two if needed)
- **Items:**
  - O-CERT C1–C6 with O-VCERT's repairs;
  - F-MASKPIP M1–M3 and N-a;
  - O-PW2 Theorems A and B;
  - O-DILUTE Thm E, Thm R, Lemma N, Prop S;
  - W7-SEP Prop. GU and SEP(A)/(B);
  - W7-PART Theorems A and B (L2 density convention);
  - O-STAGES Theorem M;
  - O-WSTAB Theorem W(a)–(f).
- **Why:** these are the paper's new supplement material, and all are author-only or same-family.

### 8. RESID-STEP0: the free post hoc start-table check (data, Owls/R; from F-SIGMA §10)
- **Step 0:** recompute the start tables from the saved fits of the 2,400 PROD-H datasets for:
  - common σ̂² ∈ {σ̃²_{S̃₀}, C-fix, s_y²}. Expect flooding; stop if seen.
  - residualised/backfit tables (O-DILUTE `resid`).
- **Report:** π₀(S₀), π₀(R₂), the start mode, per cell.
- **No SMC runs.**
- **Why:** it settles §4.5 on the real fits, and tells Felipe whether a start change aimed at dilution is worth an investment-rule pilot.

### 9. FAVIID-CLOSE: finish and verify the 2^B-free favourable rate (Opus to finish the report, then Astra to verify)
- **Part 1:** fill `W5-FAVIID · REPORT.md`, which still has the placeholders `__HEADLINE__`, `__PILOT__`, `__CARD__`, and its §4.5 pilot table.
- **Part 2:** XF-verify Lemma X⁺, Lemma M (Mittag-Leffler), Theorem B's factorisation, and Cor. C1–C3. This is F-REFEREE R6 for the part A-REV3 did not cover.
- **Why:** it closes M5 and gives Thm 5(a) and Thm 6 on study-like designs.

### 10. POSITIONING: related-work and condition check (reading; Astra or Fable; = F-REFEREE R3)
- **Read:**
  - Yang–Wainwright–Jordan (2016);
  - Zhou–Yang–Vats–Roberts (2022);
  - Zanella–Roberts (2019);
  - Griffin–Łatuszyński–Steel (2021);
  - Song–Liang (2015), the full method;
  - Lindsten et al. (2017).
- **For each:**
  - its conditions, and whether LH and the study designs satisfy them;
  - what v3's theorems add or do not add.
- **Deliverable:** a one-page "relation to computational guarantees" paragraph, plus a table.
- **Verify every exact title and page against the source;** the referee itself was unsure.

**Not ranked; do when convenient:**
- T12 `hstep` in Lean (one session);
- finish the Astra Lean fidelity run;
- `error_bound()` implementation fix (W7-SEC);
- VAL-FP replay on 10 fits (W7-SEC/T33 ε);
- the A-REV4 pending repairs (GUARD literal claim, Prop 2 GAPs, T26 exact-branch aside, Prop 1 B5 data paragraph): one small Opus task.

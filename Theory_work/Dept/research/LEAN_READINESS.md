# Lean readiness of the consistency results: deterministic cores and Level-2 skeletons

Research note for the Theory Dept manager (child helper, read-only, 2026-11-15 ~21:30 CT). Input to `NEXT_CAMPAIGN.md` §(b).
Scope as in `Lean/BRIEF.md:32-53`: Level 1 = deterministic cores with no `sorry` and only the three core axioms; Level 2 =
skeletons whose standard facts are named axioms; fidelity check per statement (`:49-53`).

**Conventions.** `tsv:N` = line N of `Theory_work/INFRA/registry/claims.tsv`. **Status** = the registry `status` field
quoted verbatim; a council record that follows the first `;` is cut and marked "(+council)". `ROOT:` =
`/home/fb31/Bayesian-Variable-Selection/` (W3-DIST lives there, uncommitted v1.4; it has no registry rows yet, so its ids
are `DEPS.tsv` ids). **Det** = deterministic: an inequality or identity on a finite model space or on fixed matrices, with no
probability. **Mathlib** is from memory: **verify** every line. **Effort**: S ≤ 1 lead-day, M 1–3 days, L > 3 days.
**Ready**: *now* / *rCP3* (after the rider CP3, Wed 11-18 18:00 CT, `Dept/QUEUE.md:5`) / *dCP3* (after W3-DIST CP3, targeted
this week, `Dept/NEXT_CAMPAIGN.md:11`) / *later*. Final freeze Fri 11-20 (`NEXT_CAMPAIGN.md:21`, `Wave3/HQ_NOW.md:86`).

**What the riders change.** I read each rider's delta STATEMENT.
- W3-START2-R keeps FLOOR, AGG, ASM and LEAK-0 "unchanged" (`BVS-wt/W3-START2-R/…/W3-START2-R/STATEMENT.md:27-28,41-42`).
  The only LEAK-0 change is the wording of a remark (`:25`).
- W3-PSHARP-R: "S, Corollary B and Proposition C stand as recorded" (`…/W3-PSHARP-R/STATEMENT.md:27`). Only the expectation
  readings change (`W3-PSHARP/STATEMENT.md:84-88,109`, per the brief `…/W3-PSHARP-R/BRIEF.md:15-18`).
- W3-RM2-R:
  - RM-0 is superseded by **RM0-plus**, which keeps RM-0(a) "unchanged" (`…/W3-RM2-R/STATEMENT.md:19,102`) and replaces
    RM-0(b)'s event {π(S₀) ≤ ½} by the mode event.
  - **DLV-0** is new (`:20`).
  - TL-F^b becomes **TL-F-c** (`:23`).
- W3-MISR-R has not started: it waits for the first free slot (`Dept/QUEUE.md:25`) and has no STATEMENT yet. Its CP3 on
  Wednesday is therefore at risk.

**Prior art to reuse.** There is a sorry-free snapshot built on the **same toolchain and Mathlib rev** as BVSCert:
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/L-LEAN/` (`STATUS.md:3-11`). It contains:
- `T21HPM.lean`: `hpm_eq_truth`, `markov_half`, `t21_C1`. This is RM-0(b)'s pattern.
- `T37Lattice.lean`: the LS0 lattice descent, Theorem A. This is RM-0(a)'s pattern.
- `T07Bayes.lean`: HPM/MPM risk facts.
- `T12Core.lean`: N1's step reduction, with `hstep` as a hypothesis.
- `MATHLIB_NOTES.md`: deprecations and import advice.

## 1. Level-1 readiness table (recommended order)

| # | Target (core) | id@ver (registry line) | Status (verbatim) | Statement | Det? | Depends on (status) | Stable this week? | Mathlib (verify) | Eff. | Ready |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **SL0**: \|PIP_j − 1{j∈S₀}\| ≤ 1−π(S₀); osc/TV form; δ<½ ⇒ MPM = HPM = S₀ | C-PACK:SL0@1.0.0 (tsv:71) | "PROVED; XF-checked (R34 ERROR-as-written → 9 fixes; core re-derived valid), R38/R39, council" | `Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:20-30` | Det: any probability on a finite Ω | none | yes: no ticket | Finset sums and PMF exist; T07Bayes already has the MPM/HPM machinery | S | **now** |
| 2 | **DIST C-0 / Lemma P6**: Q ≤ Lπ ⇒ QΠ(B) ≤ LΠ(B\|D); π{S : Π(B\|S) > a} ≤ Π(B)/a | no registry row; DEPS `P6`, `TC/DIST-C` | DEPS: "UNCHECKED (proof written; pre-check … VERIFIED; cross-family line check pending)" (`ROOT:…/W3-DIST/DEPS.tsv:12`) | `ROOT:Theory_work/Wave3/W3-DIST/STATEMENT.md:290-291, 364-365` | Det: finite mixture of kernels; Markov on Ω | none | DIST CP3 this week. v1.4 says the "deterministic transfers [are] unchanged" (`STATEMENT.md:466`) | finite sums only; `Kernel` not needed | S | now (provisional; pin the version at dCP3) |
| 3 | **LT♯ (LT-d) core**: ‖Σ_r w_r p̂_r − 1_{S₀}‖_∞ ≤ max_r ‖p̂_r − 1_{S₀}‖_∞; plus Ŝ = S₀ on {δ<½, S₀ ∈ 𝓜} | W3-SAMP:LT#@2.0.1 (tsv:353) | "PROVED-CHECKED" | `Wave3/W3-SAMP/STATEMENT.md:134-135` | Det: convex combination; the second part is SL0(iv) + store order. Rest of LT♯ is probabilistic | W3-SAMP:PC@2.1.1 (tsv:349) "PROVED-CHECKED"; CC3 (code fact, used as a hypothesis) | yes | trivial; reuse `hpm_eq_truth` | S | **now** |
| 4 | **Prior counting** `lem:prior`(a)–(e): Σ C(p,k)w(k)=1; ratio of consecutive weights; π(\|S\|>m) ≤ 2^{1−m}; C(p−s₀,j)w(s₀+j)/w(s₀) ≤ 2(j+1)^{s₀}2^{−j} | SOP:TH09@1.0.0 (tsv:11; locked T01) | "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). … T01–T03: PROVED-LOCKED …" | `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:113-120` | Det: combinatorics | none | yes (locked) | `Nat.choose` and products exist. Prove (a) by Vandermonde, not by the Beta integral | S–M | **now** |
| 5 | **DIST Lemma H** (= POST2 **D0** pointwise): H² ≤ (v/σ²−1)² + min{1, Δ²/(4σ²)}, then averaged over ν_x (H) or over i (D0) | H: DEPS `H` (no registry row). D0 sits inside W3-POST2:D@1.1.0 (tsv:363) | H: "OK", line check "VERIFIED, no findings" (`DEPS.tsv:6`). D: "PROVED (by this seat, unchecked)" | `ROOT:…/W3-DIST/STATEMENT.md:317-321`; `Wave3/W3-POST2/lemmas/D_hellinger.md:14-18` | Det (a real inequality, then integration against a fixed law) | uses the 1-D Gaussian closed form H² = 1 − AB (`D_hellinger.md:12`) | H: yes, already checked. D: diff round in progress (`ROOT:…/STATEMENT.md:405`) | `gaussianReal`, `gaussianPDFReal`, `integral_gaussian` exist; **no Hellinger distance** in Mathlib; proving the closed form needs completing the square | S (given the closed form) / M (with it) | now (H) |
| 6 | **Score foundation**: `lem:spec`(b),(d),(e) (smoother ⪯ projection; Q decreases under nesting; D = ∏f(λ_i), 1 ≤ D ≤ (n+1)^k); PSHARP **Lemma S**(1),(2) (one-step D ratio ≤ n by Schur; fit gain) | SOP:TH09@1.0.0 (tsv:11); W3-PSHARP:S@1.0.0 (tsv:408) | SOP:TH09 as row 4. S: "PROVED-CHECKED; council R2, …" (+council) | `PROOF_v3.tex:90-97`; `Wave3/W3-PSHARP/STATEMENT.md:32-44` | Det: fixed matrices | none | yes (S stands, rider `:27`) | `det_fromBlocks₁₁` (Schur), `PosDef`, `IsHermitian.eigenvalues`, det = ∏ eigenvalues exist. **Cauchy interlacing and Loewner monotonicity of the inverse are probably missing**: use the Schur and induction route instead | M–L | **now** (shared base for rows 7–11) |
| 7 | **PSHARP Cor B / (B1)**: π(S₀) ≤ [1 + (s₀+1)/(3√n)]⁻¹ on every design | W3-PSHARP:B@1.0.0 (tsv:410) | "PROVED-CHECKED; council R2, …" (+council) | `Wave3/W3-PSHARP/STATEMENT.md:92-101` (display :94, (B1) :99) | Det: no law, no truth | W3-PSHARP:S@1.0.0 "PROVED-CHECKED" (+council); rows 4, 6 | display and (B1) stable. The rider edits (B3) at `:109` and Prop A's expectation readings | rows 4 and 6, plus real analysis for c(p,s₀) ≥ (s₀+1)/3 | M | **now** (core); (B3) at rCP3 |
| 8 | **Occam converse, POST2 A2**: δ ≥ 𝒪⁰/(1+𝒪⁰); **A0**(i),(ii) ((F_w) ⇒ (DG) ⇒ (ADG)); **E3.1** ((F_λ) ∧ BM ⇒ ID) | W3-POST2:A2@1.0.0 (tsv:360), A0@1.0.0 (tsv:358), E3.1@1.0.0 (tsv:364) | each: "PROVED (by this seat, unchecked)". The file itself records a K-AE line check, VERIFIED-WITH-AMENDMENTS (`lemmas/A_occam.md:3`) | `Wave3/W3-POST2/STATEMENT.md:58-62`; `lemmas/A_occam.md:14-15`; `lemmas/E_visibility.md:76-78` | Det | A0(i) uses `lem:spec`(e) (SOP:TH09); E3.1 uses [P3] `lem:signal` | no ticket. The recorder's POST2 task is on hold (`QUEUE.md:20`) | rows 4, 6 | S (A2, A0(ii)); M (A0(i), E3.1) | now. A certificate would come before the registry check: say so in CERTIFICATES |
| 9 | **MISR R′(a),(a′)**: π invariant under y ↦ a1 + cy; Π equivariant under (S, θ, v) ↦ (S, cθ, c²v) | W3-MISR:R'@1.0.0 (tsv:412) | "PROVED-CHECKED; council R2, …" (+council) | `Wave3/W3-MISR/STATEMENT.md:70-80` | Det (algebra of the score; (a′) is a push-forward) | none. DIST bridge B0 consumes it (`ROOT:…/STATEMENT.md:368-373`) | yes: W3-MISR-R touches only Cor-G(a) and Cor-H | needs the score definition from row 6 | M | now |
| 10 | **START FLOOR**: m(S∪{l})/m(S) ≥ (n+1)^{−1/2}; 1 − π₀(S) ≥ f_n/(1+f_n) ≥ ⅓(n+1)^{−1/2}. Then **AGG** (lattice factorisation over blocks) | W3-START:FLOOR@1.0.0 (tsv:420); AGG@1.0.0 (tsv:419) | "PROVED-CHECKED" (both) | `Wave3/W3-START/STATEMENT.md:241-243` (and AGG-FLOOR `:207-209`); AGG `:197-211` | Det (start law π₀ on fixed X, y) | FLOOR uses AGG@proof; rows 4, 6 | yes ("unchanged", START2-R `:27-28`) | rows 4 and 6; the block-table definitions of π₀ are new work | M (FLOOR); L (AGG) | now |
| 11 | **SCR L1** score algebra (L1.1–L1.6: ridge operator, 1 ≤ D(t\|S) ≤ n+1, one-step change of F, D-add/D-del) and the **Lemma B bridges** B1–B3 | W3-SCR:L1@1.0.0 (tsv:388); B1–B3 (tsv:396-400) | "PROVED-CHECKED" | `Wave3/W3-SCR/lemmas/L1_score.md:7-72`; `Wave3/W3-SCR/STATEMENT.md:146-155` | Det. SCR-A and A1 themselves are probabilistic (they need L2, Model G) | A1@1.0.0 (tsv:401) "PROVED-CHECKED" rests on A-inf, B2d, B3 | yes: no ticket | row 6 | M | now. A1 itself only at Level 2 |
| 12 | **RM-0(a)**: on Sand ∩ NA ∩ TL, LS0 makes exactly \|S̃₀∖S₀\| deletions and ends at S₀, certified. **RM-0(b) → RM0-plus(b)**: pathwise inclusion of 𝒪 ∩ {Ŝ⁺≠S₀}, then Markov | W3-RM:RM-0@1.0.0 (tsv:368) | "PROVED-CHECKED" | `Wave3/W3-RM/STATEMENT.md:160-176` | Det, pathwise for every seed. Uses code premises E4 and EX-A as hypotheses | W3-RM:E4@1.0.0 (tsv:371) "PROVED-CHECKED"; C-GROW L1.1/L1.2 "PROVED-CHECKED" | (a) unchanged (`W3-RM2-R/STATEMENT.md:102`), widened to down-closed 𝓛′. (b) is restated (`:19`) | reuse `T37Lattice` (A2/A3) and `t21_C1`/`markov_half` | L (a); S (b) | (a) now; (b) at rCP3 |
| 13 | **RM2 counting and identities**: exact identity RSS_A − RSS_T = (θ*_i‖(I−P_A)x_i‖ + σZ)² − σ²Z² (TL step); block counts (≤ 2¹⁶p sets of size ≤ 16; ≤ 2¹⁵ conditioning sets per column) | W3-RM2:TL-F-b@1.0.0 (tsv:453); W3-START:TK@1.0.0 (tsv:421) | "PROVED-CHECKED; council R1, …" (+council); TK "PROVED-CHECKED" | `Wave3/W3-RM2/STATEMENT.md:249`; `Wave3/W3-START/STATEMENT.md:232-234` | Det (projection algebra; finite counting). Toolkit-b, NA-W and W-conv are probabilistic (Gaussian tails) | TL-F-b uses Toolkit-b (tsv:451) | **no**: T4 replaces TL-F^b by TL-F-c (`W3-RM2-R/STATEMENT.md:23`) | projections `orthogonalProjection` and `Finset.card` bounds exist | S–M | rCP3 |
| 14 | **DLV Lemma 3.1** ρ(u,v) = q_u(M) q_{2v−u}(M)/q_v(M)² and **3.2** (log-sum-exp convexity; Peano bound) | C-DLV:L3-3.1@1.0.0 (tsv:127), L3-3.2 (tsv:128) | "PROVED-CHECKED" | `Wave1C/C-DLV/lemmas/L3_grid.md:15-28` | Det | none | yes | `Real.exp`/`log` and derivatives exist; log-sum-exp convexity is probably not a named lemma | S (3.1); M (3.2) | now (optional: delivery, not consistency) |
| 15 | **N1 unbiasedness** E[Ẑ_r H_r(h) \| 𝓒] = Zπ(h) | W1-N1:Thm-N1@1.0.0 (tsv:31); W1-N1:P (tsv:34) | "PROVED-CHECKED"; P "PROVED-LOCKED" | `Wave1/W1-N1/STATEMENT.md:98-104` | **Probabilistic** (expectation over the SMC streams). Only its step algebra is deterministic | P: EXT:T12 | yes | the step algebra exists as `T12Core` (with `hstep` as a hypothesis). Mathlib has no `PMF.pi`: the product-law plumbing is 300–600 lines (L-LEAN `REPORT.md:86`) | L | later |
| 16 | **DLV-0** (new): every valid input and every seed returns output | none yet (W3-RM2-R T2(a)) | — | `W3-RM2-R/STATEMENT.md:20` | Det in the seeds, but it is a **code-audit** claim (Lemma R plus code reading) | C-DLV:Thm-D (tsv:122) "PROVED-CHECKED (relative to the P1/P3 audits)" | new this week; must be re-audited at the v3.2 freeze (brief `W3-RM2-R/BRIEF.md:26-27`) | at most the resource arithmetic; the code link cannot be formalised | — | **not a Lean target** |

Missing pieces:
- **MISR has no counting bound.** I found none in `W3-MISR/STATEMENT.md`. MISR's deterministic content is R′ (row 9).
- **Cor-G(a) and Cor-H are Level 2 only.** Cor-G(a) is Gaussian conditioning; Cor-H is conditional on W3-POST2:D and C
  (tsv:416, 418). Both are being restated by W3-MISR-R, so not before its CP3.
- **SCR A1 is Level 2 only.** Its deterministic part is row 11.

## 2. Level-2 skeleton targets

Every inherited input from the locked T01 can enter as a **named axiom**:
- the conjugate Normal–IG evidence and posterior formulas, `AX-Conj` (`lem:num`, `thm:Ta`, `lem:den`, `lem:slab`);
- or these formulas are proved later as Level 1.

Every code premise is an **explicit hypothesis**, not an axiom.

**(S1) DIST-1 → Theorem A(i),(ii)**. This is the expected first target (`Lean/BRIEF.md:45-46`).
- **Structure**: Lemma X (in-sample) + Lemma T (sample to population) + Lemma H (row 5) ⇒ (1.1); then bridges B0–B2 ⇒
  Theorem A.
  - (1.1): `ROOT:…/STATEMENT.md:74-91`.
  - Theorem A: `:184-201`.
  - Lemma X: `:349-358`.
  - Lemma T: `:323-334`.
  - Bridges: `:367-399`.
- **Named axioms**:
  - `AX-ChiSq`: Laurent–Massart (2000), Lemma 1, χ² tails (X1, `lem:chi`).
  - `AX-GaussQF`: E exp(eᵀAe/2) = det(I−A)^{−1/2} for 0 ⪯ A ≺ I (Lemma V(b), Occam moments).
  - `AX-Hoeffding`: may already be in Mathlib, verify.
  - `AX-Cantelli` (one-sided Chebyshev).
  - `AX-Growth`: Sauer–Shelah plus the VC dimension of half-spaces, giving the growth bound in Lemma T. Mathlib may have
    `Finset.vcDim` and Sauer–Shelah in `Combinatorics/SetFamily/Shatter` (verify). The ghost-sample step is missing from
    Mathlib, but T proves it itself (`:330-331`).
  - `AX-Bernstein`: Vershynin HDP Thm 2.8.1.
  - `AX-Net`: Vershynin Cor. 4.2.13 (both for B2-core).
  - `AX-SubG-scale`: for B1.
- **Readiness**: H, T, X, X′ are OK (`DEPS.tsv:6,7,10,11`). S, V, P6, B0–B2 and TC/DIST-1 are UNCHECKED (`:2,8,9,12,21-24`).
  **Ready after dCP3.** Effort L (skeleton ~1 week, with rows 4–6 done first).

**(S2) W3-POST:Thm-1, items 1–5, fixed design (= SOP:TH09 root)**.
- **Claim**: W3-POST:Thm-1@1.0.0 (tsv:344), status "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)",
  statement `Wave3/W3-POST/STATEMENT.md:61-100`.
- **Structure**:
  - the T03R chain;
  - the Lemma-1a size tail;
  - items 2–4 are SL0/SL1 (row 1, Level 1).
- **Named axioms**:
  - `AX-ChiSq`;
  - `AX-GaussTail` (Mills ratio, union over the lattice);
  - `AX-Conj`.
- **Readiness**: the statement is stable. Acceptance H is staged (`NEXT_CAMPAIGN.md:18`).
- **Leave out item 6** (the random-design transfer through W2-APP:POST@1.0.1, tsv:153: "PROVED (by this seat, unchecked);
  R02 VERIFIED-WITH-AMENDMENTS, applied"; acceptance C failed PC1, same line).
- It is the premise of DIST Theorem B and of RM2-F, so certifying it first serves both.
- **Ready now** for a skeleton, though it is second in priority. Effort L.

**(S3) RM2-F⁺, after W3-RM2-R CP3** (RM2-F@1.0.0, tsv:449, "PROVED-CHECKED, conditional on SOP:TH09; …" (+council);
`Wave3/W3-RM2/STATEMENT.md:206-214`).
- **Structure**:
  - RM0-plus, pathwise (row 12, Level 1);
  - [MODE] from [POST] by Markov, where [POST] = S2, or S2 as a named hypothesis;
  - the SAND, NA and TL events.
- **Named axioms**:
  - `AX-ChiSq`;
  - `AX-GaussConc` (Borell–TIS or Lipschitz Gaussian concentration, for the lattice maximum in NA-W);
  - `AX-GaussTail`.
- **Hypotheses**: the code premises E4, EX-A and the implementation premises.
- **Why RM2-F and not RM2-R**: RM2-R@1.0.0 (tsv:450) is "conditional on W2-APP:POST" (PC1 FAIL). It adds Gaussian-row
  bridges (spherical tail, median–mean), and its aggregated leak is a named open item (`QUEUE.md:33`).
- **Ready at rCP3**; best after S2. Effort L.

## 3. Recommendation

**Can start now** (stable this week and deterministic):
- **Batch A, no score needed (≈ 3–4 lead-days):**
  - **SL0** (row 1);
  - **LT-d** (row 3);
  - **prior counting** (row 4);
  - **DIST Lemma H / D0** (row 5);
  - **DIST C-0 / P6** (row 2): small, but pin it to the DIST CP3 version.
- **Batch B, the score foundation (≈ 1–1.5 weeks):**
  - `lem:spec` and PSHARP Lemma S through the Schur and induction route, not interlacing (row 6);
  - then **PSHARP Cor B/(B1)** (row 7), **POST2 A2/A0/E3.1** (row 8), **MISR R′** (row 9), **START FLOOR** (row 10), and
    **SCR L1** with bridges B1–B3 (row 11);
  - **RM-0(a)** (row 12), reusing `T37Lattice`.
- Most of these rows are already checked; the exceptions are the POST2 rows and C-0. Reusing the L-LEAN snapshot, which
  has the same toolchain and Mathlib, saves the HPM, Markov and lattice layers.

**Waits for the rider CP3 (Wed 11-18):**
- RM0-plus(b) (row 12);
- the RM2 TL identity and counts (row 13);
- the (B3) wording of PSHARP (row 7);
- MISR Cor-G(a) and Cor-H at Level 2. W3-MISR-R has not started, so Wednesday is at risk.

**Waits for DIST CP3:** the DIST-1/Theorem A skeleton (S1) and DIST-C (C-i)–(C-iii).

**Not Lean targets this semester:** DLV-0 (a code audit) and full N1 (product-law plumbing; Level 3 in practice).

**Suggested launch date.**
- **Thu 11-19 (GO): Phase 0 and Batch A.** By then every rider statement is frozen (CP3 Wed 18:00), so the Phase-0
  inventory is not invalidated by Wednesday's restatements. This assumes HQ and the owner can spare one lead from BNP Lean
  (`Lean/BRIEF.md:8-9`).
- **Mon 11-23: Level 2 begins with S1 (DIST-1)**, provided DIST CP3 lands by Fri 11-20; otherwise start with S2.
- The owner's guidance ("earliest after the theory freeze / W3-DIST CP3", `Wave3/HQ_NOW.md:27`) is also met if HQ prefers
  a single launch on **Mon 11-23**, with Batch A as the first day's work.

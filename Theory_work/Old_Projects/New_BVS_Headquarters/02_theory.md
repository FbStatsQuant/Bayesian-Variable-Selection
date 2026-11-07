# 02 · Theory: SMC-BVS v3.1 and the paper-1 theorems (setup, statements, statuses, dependencies)

This file is the theory record of the "New BVS Headquarters" thread. It has two parts:

- **Part A (this file, below):** the FINAL STATE. It gives the method as shipped (v3.1): model, priors, start, bridge, kernel, islands, evidence, PIP rules, HPM, LS0, certificate card and reporting amendments, with verbatim definitions from `branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md` and `branch_snapshots/main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md`. It also gives the **final paper-1 list** from the theorem meeting (MEET-THM): main cards M1–M8 = **TH01–TH08**, supplement cards = **TH09–TH20**, future work FW1–FW27 = **CJ01–CJ27**, drops **DR01–DR06**, inherent limitations **LIM01–LIM09**, obligations **OB01–OB17**, the HQ rulings Q1–Q5 = **RL**, method-meeting decisions **MD**, and the coverage matrix.
- **Part B (`02b_theory_campaign_history.md`, ≈2.7 MB):** the CAMPAIGN HISTORY. It covers every result, conjecture, refutation and counterexample from the pre-campaign set T01–T39 and the hypotheses H24, EXP′, PW2…, through Waves W1–W8, the F-/O-/A-REV/S-/L-/API-/LIT- runs and the T38 statement of record. It uses IDs **TH101+, LM101+, CJ101+, RF101+, CE101+**, with each item's verbatim statement, status history, checkers, dependencies and the final card it feeds. It has 14 themes, each ending in "Dead ends and corrections", followed by Part II "Conflicts and UNCERTAIN items".

**Lookup:** `ID_REGISTRY.md` lists every ID with its native name(s), kind, status (exact words), defining file and positions. Part B of the registry ends with an alias index from native names to IDs. K-numbers (K01…K108) are the theorem meeting's inherited-result IDs (`branch_snapshots/MEET-THM/REGISTRY_PAPER1.md`). Each card names its K-numbers, and Part B's "feeds" column maps campaign results onto them.

**Status vocabulary (copied, never upgraded):**

| Term | Meaning |
|---|---|
| PROVED-LOCKED | pre-campaign locked proof |
| PROVED (candidate) | AI-proved, not adopted |
| PROVED (by this seat, unchecked) | a meeting seat's own argument |
| PROOF SKETCH | argument incomplete |
| VERIFIED / VERIFIED* / VERIFIED WITH AMENDMENT | referee verdict |
| SF | same-family (Claude) check |
| XF | cross-family check (Astra A-REV1–9, or Sol PC1 in the meetings) |
| GAP / ERROR | referee found a gap / an error |
| COUNTEREXAMPLE, REFUTED, OPEN | as stated |

Nothing in this archive is adopted or locked. Adoption is Felipe's decision.

**Approval state at thread end:**
- The method v3.1 was approved by HQ ([pos 1557], [pos 1584]).
- The theorem package closed with no open questions [pos 1626] and was approved by HQ with one change [pos 1639].
- **The theorem list was awaiting Felipe's approval** [pos 1650], [pos 1673].

**Fidelity of quotations:** 
- Part A marks verbatim blocks with `<!-- BEGIN VERBATIM <source>:<lines> -->`. The archive check found 97 of 99 blocks byte-identical to the snapshots; the other 2 are an explanatory line and one quote marked as elided with "[…]".
- In Part B, of 1,091 blockquoted statements:
  - 925 are byte-identical and 54 match line by line;
  - 55 are notation transliterations (Unicode ↔ LaTeX, 4-gram coverage ≥ 0.98), marked with an HTML comment;
  - 57 are flagged in place with "⚠ FIDELITY FLAG": they are abridged or reformatted relative to the source.
- For any flagged or transliterated quote, the snapshot file is authoritative.

**Main dependencies (Summary; full cards below):**
- **TH01 (M1)** rests on T12/T31(i) (PROVED-LOCKED), the N9 kernel facts (TH12, S-KERNEL), the obligation N1 (OB01, PROOF SKETCH, binding §13.1), and the GUARD-W/IND-T audits for its output-event clauses.
- **TH05 (M5)** composes the Thm4-C1 / T38-(0) inequality (T21 in Lean) with N200, Theorem A (Lean, sorry-free), LS-score and LS0 on LH.
- **TH02 (M2)** uses the OWS-WS results (O-WSTAB) with the Q1/Q5 readings (RL01–RL05).
- **TH07 (M7)** uses the stage laws STG-G/STG-L/STG-M and T26BUD-G (K28 cited).
- **TH06 (M6)** uses SEP (W7-SEP) and Lemma KL.
- **TH08 (M8)** uses METH-AUDIT Prop D, T32(i) and the calibration share.

See each card's "Depends on" and K-list.

> **Archive note.** In this archive, "02a" means `02_theory.md` (final state), "02b" means `02b_theory_campaign_history.md` (campaign history), and "REG-A"/"REG-B" or "registry A/B" mean parts A and B of `ID_REGISTRY.md`. Paths like `branch_snapshots/...` and `transcript/...` are relative to this folder.

# Part A · FINAL STATE: method v3.1 and the paper-1 theorem list (MEET-THM)

Archive draft 02a (agent A). Scope: the method as shipped (v3.1) and the final paper-1 theorem list from the theorem meeting MEET-THM. The earlier campaign history (T01–T39, waves, Theorems A/B, …) is covered by another draft that uses IDs 101 upward; this draft only touches it where a final card inherits it.

Companion files: `notation_and_conventions.md` (symbols, settings table, convention changes) and `ID_REGISTRY.md (part A)` (one row per ID).

## A0 · How to read this file

### A0.1 Rules followed
- **Verbatim blocks.** Everything between `<!-- BEGIN VERBATIM <source>:<lines> -->` and `<!-- END VERBATIM … -->` is copied unchanged from the named source (path relative to `branch_snapshots/`, line numbers of the snapshot file; for transcript messages, `[pos N]`). Everything outside such blocks is editor text and is labelled "Summary:" or is a header. The snapshot files use `\( … \)` LaTeX in some cards; they are left as filed.
- **Statuses** are copied from the source and never upgraded. "SF" = same-family check, "XF" = cross-family check, as in the cards.
- **UNCERTAIN:** marks a conflict between sources, or something the sources do not settle. They are collected in §A7.
- The cards in `THEOREM_LIST_FINAL.md` (called TLF below) were "assembled by the clerk" from the Round-3 cards R3_A…R3_D with chair's integration notes; the final audit of the package is `MEET-THM/CLOSE_AUDIT.md` (PASS WITH CORRECTIONS, all applied by the chair). Where an integration note changes a card (M1 K-ID header, M5 δ₁, M7 K33/K30/K29, M4 masked clause lettering), the note is printed above the card and governs.

### A0.2 Approval state at the end of the thread (important)
- The theorem meeting closed with "Open questions: none" ([pos 1626]; `MEET-THM/MINUTES.md` header). HQ reviewed and approved the package with one change (growth rate (ii), §A4.6) ([pos 1639]) and wrote the plain-language list for Felipe ([pos 1650]; `MEET-THM/FOR_FELIPE_THEOREM_LIST.md`).
- **Felipe had not yet approved the theorem list** when the archived thread ends: at [pos 1673] he says "I will take a look at the theorems and give you feedback / questions later so we can keep working." The method v3.1 itself was approved by HQ ([pos 1557], [pos 1584]) after Felipe approved the four decisions of [pos 1302] (recorded at [pos 1304] with the comment "All approved" and at [pos 1316]).
- Statuses of the proofs themselves: most card ingredients are "PROVED (candidate)" or weaker; no main card is Lean-certified as a whole; the cards name Lean cores to be written, and M5 cites existing sorry-free Lean files for parts (`T37Greedy.lean`, `T37Lattice.lean`, `T21HPM.lean` with `t21_C1`). The per-theorem HQs had not been launched ([pos 1650]: "Once you approve, wave 1 of the per-theorem HQs launches").

### A0.3 ID scheme used in this draft
| Range | Meaning | Source of native names |
|---|---|---|
| TH01–TH08 | main cards M1–M8, in M order | TLF Part I |
| TH09–TH20 | the 12 supplement cards, in the order of the TLF header table (S-T, S-TARGET, S-BLOCKS, S-KERNEL, S-IDENT, S-CERT, S-OUT, S-Z, S-POOL, S-LIM, S-REP, S-LEAK) | TLF Part II |
| TH21 | S-STGI (dissolved; not a list item) | TLF Part II |
| TH22 | Thesis CD (K96), scoped remark | TLF Part III |
| CJ01–CJ27 | FUTURE_WORK FW1–FW27 | `MEET-THM/FUTURE_WORK.md` |
| DR01–DR06 | the 6 drops (K12, K34, K66, K67, K91, K98) | `MEET-THM/FUTURE_WORK.md` "Dropped" |
| LIM01–LIM09 | the 9 inherent limitations of the method meeting | `MEET-v31/MINUTES.md` §5 items 1–9 |
| OB01–OB17 | obligations N1–N17 | `MEET-v31/THEOREM_REVISION_INPUTS.md` §3 |
| DF01–DF25 | definitions/premises of the final state | METHOD_v3.1_FINAL, METHODOLOGY_v3, TLF shared defs |
| RL01–RL06 | HQ rulings Q1–Q5 and the approval amendment | `MEET-THM/evidence/`, `MEET-v31/AMENDMENT_HQ_02.md` |
| MD01–MD13 | the 13 decisions of the method meeting | `MEET-v31/MINUTES.md` §2 |
| DS01–DS06 | recorded dissents | `MEET-THM/MINUTES.md` §2.2, §2.3 |
| CL01–CL23 | cited lemmas of TLF Part III | TLF Part III table |
The other agent uses IDs from 101 upward; no ID in this draft is ≥ 101.

### A0.4 Transcript position key (positions ≥ 1040 used here)
| pos | what |
|---|---|
| 1040, 1044 | Felipe's big-picture message; HQ restates the problem and the thesis sentence "In split-and-merge, correlation breaks correctness. In local-to-global SMC, correlation costs only sequential depth and particles, never correctness." |
| 1055, 1061 | Felipe asks for (1) the final method and (2) a specific theorem list; "full authority" |
| 1107 | HQ's v3.1 decision: "ship v3 unchanged, plus a parallel execution layer" |
| 1128–1162 | meta-questions: no open method questions before proving; selection rule; every proposal goal is mandatory; "extract until the last drop"; burden of proof on any change |
| 1171, 1201 | Felipe commissions the Methodology meeting; HQ launches it |
| 1214, 1226 | Felipe's rule: the method must apply for any (n, p), no arbitrary choices; HQ adds it as ground rule 9 / agenda item |
| 1251, 1263, 1280, 1286 | meeting status and result (v3.1, nine inherent limitations, seventeen obligations) |
| 1296, 1302, 1304, 1316 | v3 → v3.1 change size; parameter audit; Felipe's approval of four decisions |
| 1341–1361 | Felipe asks for a well-specified theorem list; HQ estimates ~22 theorems, ~14 for paper 1; Biometrika level; format of the theorem meeting |
| 1363–1373 | fresh-eyes Fable and raw Astra added |
| 1467–1480, 1512 | Sol audit/proof check, AMENDMENT_HQ_01 (73 findings: 45 changed, 28 no change) |
| 1550, 1557, 1584, 1593 | N9 gate passed; method approved by HQ; FOR_FELIPE_FINAL_METHOD |
| 1608, 1614 | chair's Q1–Q4; HQ rulings |
| 1621, 1624 | chair's Q5; HQ ruling |
| 1626 | MEET-THM closed |
| 1631, 1639 | HQ review; approval with one change (growth rate (ii)) |
| 1650 | theorem list ready for Felipe |
| 1669 | ABL-CONF (confirmatory start test) result |
| 1673 | Felipe will review the theorems later; remaining credits |


---

# A1 · Setup: the method as shipped (v3.1) and the objects the theorems talk about

Sources, in order of authority for the final state:
1. `MEET-v31/METHOD_v3.1_FINAL.md` (called METH31): "SMC-BVS v3.1: final method of paper 1, written as a diff against METHODOLOGY_v3", amended by AMENDMENT_HQ_01 and AMENDMENT_HQ_02. Its header says: "v3.1 is v3 unchanged as a statistical method, plus a list of additions."
2. `main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md` (called METH3): the baseline that METH31 diffs against. **The model, priors, start, moves, calibration, PIP/HPM/evidence rules are defined there**; METH31 §1 lists them as unchanged ("Unless §2 lists a change, each section stays verbatim").
3. `MEET-THM/THEOREM_LIST_FINAL.md` "Shared definitions and premises used by the final cards" (D0, G, LH, W, MC contract, output contract; EX-A … 𝒪) and `MEET-THM/NOTATION.md` (symbol table; in `notation_and_conventions_A.md`).
4. Reporting amendments: `MEET-THM/AMENDMENT_HQ_02_DEFINITIONS.md` and the HQ decision `MEET-v31/AMENDMENT_HQ_02.md`.

Summary: METH31 §0 says what stays: "the target posterior (M §5); the blocks, tables and composite start (M §6.3); the neighbour graph (M §6.4); the move round (M §6.5) and resampling (M §6.6); the calibration law (M §6.6–6.9); the budgets (M §3); the HPM decision (M §6.10); the evidence estimator (M §6.12)." The additions: parallel execution layer; optional stacking R′ = 4k; LS0; reporting changes (Ẑ-weighted primary PIP, general-h accumulator, certificate card, NA fields); wording and classification fixes. Position: [pos 1107] (decision), [pos 1280], [pos 1296] (change list), [pos 1584] (approval).

## A1.1 Method summary, inputs, outputs, statuses (METH3 §1–§2, verbatim)

Summary: METH3 §1 (one-paragraph description) and §2 (inputs X, y, seed, allocation; outputs HPM with provenance, near-tie list, PIPs, MPM, evidence, flags, diagnostics; statuses `exact`, `completed`, `schedule_limit`, `numerical_failure`, `resource_limit`, `y_constant`, `no_predictors`, `invalid_input`, to which v3.1 adds `degenerate_n` and `unsupported_size`) are in `main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md` lines 23–59 and are not re-quoted (METH31 §1: unchanged except as §2 lists).

## A1.2 Preprocessing (METH3 §4, verbatim; METH31 §1 table row "§4 Preprocessing": rules 2–6 unchanged, rule 1 changed by e3)

<!-- BEGIN VERBATIM METHODOLOGY_v3.md §4:78-94 -->
## 4. Preprocessing

1. Stop with `invalid_input` if any entry of X or y is not finite, or n < 3, or p < 1.
2. Drop column j only if all its entries are **exactly** equal; record it; it is never selected. p := number kept. If p = 0,
   return Ŝ = ∅, PIPs and evidence unavailable, status `no_predictors`.
3. If all entries of y are exactly equal, return Ŝ = ∅ (the exact HPM: every Q_S = 0, D_S ≥ 1 and w is decreasing), PIPs and
   evidence unavailable, status `y_constant`. (The exact PIPs are not 0; they are not computed.)
4. Standardise stably: for each column, divide by its maximum absolute value, compute the mean, centre, then divide by the
   sample SD (denominator n − 1), so ‖x_j‖² = n − 1. Same for y, recording s_y² = ‖Cy‖²/(n − 1) with C = I − 11ᵀ/n.
   Original indices, means and scales are kept for reporting and back-transformation.
5. Report connected components of {|r_jl| ≥ 1 − 10⁻¹⁰} (duplicates are kept; they split PIP mass, and the MPM may exclude
   both members).
6. Resource preflight (§8.6).

These rules make the target invariant to affine maps of y (a ≠ 0) and of each column of X, and to column permutation (up to
index-based tie-breaks in clustering and decisions, which are deterministic).

<!-- END VERBATIM METHODOLOGY_v3.md §4:78-94 -->

## A1.3 Likelihood, g-prior, σ² prior, BB(1,p) size prior, cap K, evidence (METH3 §5, verbatim)

METH31 §1: "§5 Target posterior and reduction statement | g = n, τ = 1, IG(0.01, 0.01), BB(1, p), cap ⌊n/2⌋ | **unchanged** (Felipe's model)". The same objects as used in the final cards (TLF shared definition "D0"/"Score"/"Prior"):

<!-- BEGIN VERBATIM METHODOLOGY_v3.md §5:95-127 -->
## 5. Target posterior (Felipe's model, unchanged)

On the standardised data (X, y), for S ⊆ {1, …, p} with k = |S| ≤ K, G_S = X_SᵀX_S, z_S = X_Sᵀy:

```text
y | β_S, σ², S ~ N_n(X_S β_S, σ² I_n)                   (no intercept; y is centred)
β_S | σ², S    ~ N_k(0, n σ² (G_S + I_k)⁻¹)              g = n (unit information), τ = 1 (one pseudo-observation)
σ²             ~ IG(a₀, b₀),  a₀ = b₀ = 0.01
ϖ(S)           = w(k) 1{k ≤ K} / W_K,   w(k) = B(1+k, 2p−k)/B(1, p) = ½ / C(2p−1, k),   W_K = Σ_{j≤K} C(p, j) w(j)

H_S = (n + 1) G_S + I_k,   Q_S = yᵀy − n z_Sᵀ H_S⁻¹ z_S,
log m(S) = log C_n − ½ [log det H_S − log det(G_S + I_k)] − (a₀ + n/2) log(2b₀ + Q_S),
C_n = (2b₀)^{a₀} Γ(a₀ + n/2) / (π^{n/2} Γ(a₀)),
π(S | y) = ϖ(S) m(S) / Z,   Z = Σ_{|S|≤K} ϖ(S) m(S).
```

Reasons (accepted by Felipe; defended in the audit):
- g = n: unit information. τ = 1: one pseudo-observation on the standardised scale; keeps every m(S) finite for collinear X_S.
- IG(0.01, 0.01): proper, as the project proofs require. Its effect on comparing two models is at most n·b₀·|1/Q₁ − 1/Q₂|:
  negligible near a decision boundary (Q₁ ≈ Q₂) and dominated by the gap otherwise. With y standardised, Q_S ≥ yᵀy/(n+1).
- BB(1, p): depends on p only; prior mean size p/(p+1) ≈ 1; each extra variable costs log((2p−k−1)/(k+1)) nats; the project's
  existing theory is for this prior. Its extra cost over a uniform-on-size prior is log((2p−k−1)/(p−k)) per variable, ≈ log 2
  only when k ≪ p.
- Cap K = min(p, ⌊n/2⌋): keeps near-interpolating models out of the space; the ½ is a declared restriction, not needed for
  propriety. The project's dimension result (T6) says the cap does not bind in the regimes it covers.

**Reduction statement (consensus of the three consultants; to be proved, V1).** Write raw data X^r, y^r, D_x = diag(column
SDs), X = C X^r D_x⁻¹, and U ∈ ℝ^{n×(n−1)} orthonormal with UUᵀ = C. With θ = s_y β and v = s_y² σ², the posterior above is
the posterior of the contrast regression of Uᵀy^r on UᵀX with n − 1 Gaussian errors (Uᵀε ~ N(0, σ*² I_{n−1}) exactly, before
standardisation of y), slab θ_S | v, S ~ N(0, n v (G_S + I)⁻¹) and v ~ IG(0.51, 0.01 s_y²). So the exponent a₀ + n/2 is the
integrated-intercept model with IG shape a₀ + ½, and the response scale enters only through the data-dependent IG rate.
This is not a claim that the working evidence equals a raw-data marginal likelihood; "evidence" below always means the
evidence of this working model.
<!-- END VERBATIM METHODOLOGY_v3.md §5:95-127 -->

Shared definitions D0, Score, Prior, Start/bridge, G, LH, W, EX-A, MC contract, Output contract (TLF, printed once here; they are "used by M3, M6 and S-REP (and by the other cards where they cite LH, W, G, EX-A)"), and the implementation premises of R3_D ("used by M5 and Prop D"):

## Shared definitions and premises used by the final cards

### R3_C shared definitions (D0, score, prior, start/bridge, G, LH, W, EX-A, MC contract, output contract)

Used by M3, M6 and S-REP (and by the other cards where they cite LH, W, G, EX-A).


**Source:** `theory_campaign/MEET-THM/R3_C.md:130–142` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:130-142 -->
| Shared definition | Exact scope |
|---|---|
| D0: data/target | \(n\ge3,p\ge1\); nonconstant columns and response, centered and standardized. \(K=\min(p,\lfloor n/2\rfloor)\), \(\Omega=\{S:|S|\le K\}\). Use the shipped \(g=n,\tau=1,a_0=b_0=.01\) score and normalized capped BB\((1,p)\) prior. |
| Score | \(G_U=X_U^\top X_U,\ z_U=X_U^\top y,\ H_U=(n+1)G_U+I,\ Q_U=y^\top y-nz_U^\top H_U^{-1}z_U,\ \nu=.01+n/2\). \(m(U)=c_n[\det H_U/\det(G_U+I)]^{-1/2}(.02+Q_U)^{-\nu}\). The common positive \(c_n\) cancels from posterior ratios. |
| Prior | \(w(k)=[2\binom{2p-1}{k}]^{-1}\), \(W_K=\sum_{k\le K}\binom pk w(k)\), \(\varpi(S)=w(|S|)/W_K\). |
| Start/bridge | Actual blocks \(C_b\), \(r_b(U)=m(U)/m(\varnothing)>0\). \(\gamma_0(S)=\varpi(S)\prod_b r_b(S_b)\), \(\pi_0=\gamma_0/\bar Z_0\), \(\pi=\varpi m/Z\), \(d=\log BF-\sum_b\log r_b\), \(q_t\propto\gamma_0e^{td}\). |
| G: sampling model | Fixed raw design; \(y^r=\alpha\mathbf1+X^r\beta+\epsilon\), \(\epsilon\sim N(0,\sigma^2I)\), fixed \(\sigma^2>0\). Standardize afterwards. Standardized errors are not assumed independently Gaussian. |
| LH: design | \(p=9\lfloor n^{1/3}/9\rfloor\), groups of nine, within-group correlation \(0.4\). Two disjoint cross-group links have correlation \(0.2\); remaining cross-group correlations vanish. Each linked pair has coefficients \((1,-0.2)\); others zero; \(\sigma^2=1\). Centered Gram: \(X^\top X=(n-1)\Sigma\). |
| LH: non-vacuity | \(\lambda_{\min}(\Sigma)\ge0.4\), \(p<n\), support size four. For \(n\ge9^6\), \(9\le B\le16<18\); separation and SIZE give actual blocks equal groups. Two true coordinates have zero population marginal covariance with the response. W1P2 “Shared · LH family”; W2P2 C5/C11. |
| W: reporting exhibit | Same \(p\), groups of nine; within correlation \(1/4\), cross correlation \(\varepsilon_n=1/(np)>0\). Two coefficients \(n^{-1/4}\) in different groups; \(\sigma^2=1\). Also retain the checked stronger exhibit \(\varepsilon_n=n^{-1/2}/p\). Actual blocks equal groups for \(n\ge9^6\); \(D_*=O_P(1)\). W2P2 §1, IC3/scale rows. |
| EX-A | Exact mathematical scores, arithmetic, sums and comparisons. This is an idealisation, not a validated floating-point property. |
| MC contract | Exact iid start draws, multinomial resampling, actual invariant move rounds, independent ideal uniforms; successful full calibration \(\mathcal C\) frozen before final randomness; independent final islands; common \(N\); \(R'=4k\) declared in advance. These are computational premises. |
| Output contract | Potential uninterrupted final run first. GUARD-W identifies delivered statistical records with potential records on \(\mathcal O\). Its integrated audit remains open. Bounds transfer by intersection with \(\mathcal O\), never by conditioning on delivery. |
<!-- END VERBATIM -->


### R3_D shared implementation premises (EX-A, EX-S, CAL, IND-T, GUARD-W, SR, OP-LS0, e4, complete scans, 𝒪)

Used by M5 and Prop D.


**Source:** `theory_campaign/MEET-THM/R3_D.md:139` (verbatim)

<!-- BEGIN VERBATIM R3_D.md:139-139 -->
Shared implementation premises (named once, used by both cards): **EX-A** exact scores and arithmetic; **EX-S** fresh independent ideal uniforms (H-U); **CAL** a successful frozen calibration record 𝒞 on streams 0–9; **IND-T** final streams 10..9+R′ independent of 𝒞 and of each other, R′ = 4k declared before stream 10; **GUARD-W** stop-only guard (operational interruption ⇒ no output); **SR** the method's stop/return rule as in the T38 hypotheses; **OP-LS0** LS0 integrated as specified (METHOD §2 #8); **e4** emitted LS0 centre = the prescribed smallest-size, lexicographically smallest start-mode maximiser (DP invariant N3 OPEN); **complete scans** no operational interruption of any search. 𝒪 is the output event; statements are P{𝒪 ∩ ·}; D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) in potential-run notation (the overbar is the potential run, not set complement; W2PC1:122).
<!-- END VERBATIM -->


## A1.4 Execution order, exact branch (METH3 §6.1–§6.2, verbatim)

<!-- BEGIN VERBATIM METHODOLOGY_v3.md §6.1:131-152 -->
### 6.1 Execution order

```text
preprocess, preflight
if exact-branch condition: enumerate (6.2), local certification, report
else:
  build blocks, tables, start (6.3); neighbour graph (6.4)
  CALIBRATION, tier e = 0 (streams 0 and 1–4):
     pilot (H_e particles, adaptive ESS schedule, 6.6) → polish + local search on the pilot
     candidate set V; preliminary grid (6.7)
     repeat ≤ ℓ times: 4 diagnostic islands (H_e each) on the current grid, with burn-in and measured rounds
                       → local search → update V → rebuild grid; stop when the rebuilt grid equals the previous one
     checks (6.9)
  if any trigger and e = 0: repeat CALIBRATION at tier 1 (streams 5 and 6–9), keeping the score leaders
  freeze: grid, budgets (N_e), V-independent settings
  FINAL (streams 10–13): 4 fresh islands × N_e, new iid start draws, frozen grid, burn-in L rounds, 4 measured rounds
  final local search; final checks (flags only)
  report (6.11–6.13)
```

Final observations never revise the schedule and never select replacement estimates. Calibration estimates are archived and
labelled; they are never reported as the estimate.
<!-- END VERBATIM METHODOLOGY_v3.md §6.1:131-152 -->
§6.2 (exact branch: enumerate when E = Σ_{k≤K} C(p, k) ≤ (5H₀ + 4N₀)·p, status `exact`) is at METHODOLOGY_v3.md lines 154–160; v3.1 wording fix w2 'all p at n ≤ 5'.

## A1.5 Block partition, tables, start π₀, discrepancy and tempering bridge; neighbour graph (METH3 §6.3–§6.4, verbatim)

METH31 (row 0, `#4`, `w3`, `w5`): the start is unchanged; item 1 closed as "Outcome 2 (keep, reframe)": "the start is presented as the exactly computable, theorem-bearing local step … plus the parallel table stage, with **no depth or speed claim**." "The dendrogram is cut by node size only (≤ B). There is no correlation-height threshold." Positions: [pos 1280], [pos 1669] (ABL-CONF).

<!-- BEGIN VERBATIM METHODOLOGY_v3.md §6.3–6.4:162-184 -->
### 6.3 Blocks, tables and the composite start

- **Clustering:** complete linkage on the distance 1 − |r_jl| computed from X; ties between candidate merges broken
  lexicographically on the sorted original-index lists.
- **Cut:** top-down from the root; any node with more than B members is split into its two children (visited smallest index
  first) until every retained cluster has at most B members.
- **Packing:** next-fit in dendrogram leaf order, whole clusters only (a retained cluster is never split), into blocks
  C₁, …, C_J of at most B members. J ≥ ⌈p/B⌉ (packing leaves gaps).
- **Tables:** for each block, every sub-model U ⊆ C_b is scored against the full y; r_b(U) = m(U)/m(∅) (table exponent 1).
  Since B ≤ K for n ≥ 3, no sub-model exceeds the cap. Every table score counts for the HPM. Table scores are not inserted in
  the score cache.
- **Start:** γ₀(S) = ϖ(S) ∏_b r_b(S ∩ C_b), π₀ = γ₀/Z̄₀. Z̄₀ is computed exactly by convolving the block size profiles
  e_b(j) = Σ_{|U|=j} r_b(U) up to K with the size prior (valid because ϖ depends on S only through |S|). Exact iid draws:
  draw the total size, then block sizes backwards, then each block's sub-model within its size class.
- **Discrepancy:** d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b), BF(S) = m(S)/m(∅); bridge γ_φ(S) = γ₀(S) e^{φ d(S)}, φ ∈ [0, 1];
  γ₁ ∝ the posterior; Z = m(∅) Σ_S γ₁(S).

### 6.4 Neighbour graph

r_n = √(2 log p / n) (about the largest correlation p unrelated columns reach by chance). For each j: the partners l ≠ j with
|r_jl| > r_n, always including j's single largest-|r| partner, keeping at most the B largest (ties by original index); then the
symmetric union N(j) (l ∈ N(j) ⇔ j ∈ N(l); degrees may exceed B). No edges when p = 1. Accepted by Felipe for now.

<!-- END VERBATIM METHODOLOGY_v3.md §6.3–6.4:162-184 -->

### Row 0 and the block-table stage of METH31 §2 (verbatim)

<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md §2 row 0:114-125 -->
### Row 0: start (item 1, closed: Outcome 2)

| # | change | M § | spec text | class | 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 0 | **Composite block start** | §6.3, §1 | "The v3 block start is retained in every outcome of the agreed ABL-START rule (SYNTH_R2 §2). Item 1 closed as **Outcome 2 (keep, reframe)**: the start is presented as the exactly computable, theorem-bearing local step (S1/S2) plus the parallel table stage, with **no depth or speed claim**. The ablation may be printed as exploratory (12 designs × 1 seed)." | none (start unchanged) | none | S2 §2 (rule); S3 R3-6 (procedure); `ITEM1_ABL_START.md` (outcome) |

For the record, the agreed rule allows exactly three outcomes (S2 §2, S3 R3-6). The result was **Outcome 2**: 9 of 12 designs were complete for arms A–C, and all 9 were inconclusive because arm C's log Ẑ was 2.6–13.3 nats below A and B (`ITEM1_ABL_START.md` §2–3). Certified count: arm C's log Ẑ is below the best score found by any arm on 10/12 designs, so Ẑ < Z in exact arithmetic; arms A and B on 0 (`evidence/item1_scripts/HQ_NOTE_v2.md`). The three outcomes:
- **Outcome 1:** keep the start, depth claim allowed.
- **Outcome 2:** keep the start and reframe it as the exactly computable, theorem-bearing local step plus the parallel table stage, with no depth or speed claim. This is also the result when fewer than 9 designs are conclusive. The committed v1 script (`apply_rule.py`) lacked this absolute gate; HQ's corrected `evidence/item1_scripts/apply_rule_v2.py` enforces need = max(9, ⌈0.75·complete⌉) and reproduces Outcome 2 (`HQ_NOTE_v2.md`, commit 8f6051b).
- **Outcome 3:** a real issue is flagged. v3.1 still ships the block start; the ablation is reported; a ≤ 20-seed paired check runs on the two worst designs; a WORKHORSE candidate goes to Felipe only if that check confirms.

No outcome reopens item 1 in this meeting (S3 R3-6). The backfit start is rejected regardless (§4).
<!-- END VERBATIM METHOD_v3.1_FINAL.md §2 row 0:114-125 -->
<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md §2 #4:134-134 -->
| 4 | **(h) Block-table stage as the explicit parallel local step** | §6.3, §8.2 | "Block tables are scored in parallel over blocks and sub-models; each score is independent. No floating-point summation order may change under a bitwise claim. Parallel convolution and other reductions need a separately specified order, or a narrower numerical-equivalence claim." | ADDITIVE (bitwise) | none. No re-run. | S2 D3e; R2_C D3e; R2_A D3e; R2_B D3e |
<!-- END VERBATIM METHOD_v3.1_FINAL.md §2 #4:134-134 -->

## A1.6 Kernel moves and the move round (METH3 §6.5, verbatim) and the N9 facts

Moves: p Gibbs coordinate updates, one uniform swap, B neighbour swaps, one independence proposal (π₀ proposal), in a uniformly random order drawn independently of the particle's state, afresh per particle and round; m = p + B + 2 steps. The validity facts (N9) are the supplement card TH12 (S-KERNEL) and clause (a) of TH01 (M1); `N9-KERNEL` was verified "VERIFIED WITH AMENDMENT" by the cross-family inherited-proof check (`MEET-THM/evidence/CHK_INHERITED/REPORT.md`, gpt-6.1-sol) and passed against the production code (HQ at [pos 1550], [pos 1593]).

<!-- BEGIN VERBATIM METHODOLOGY_v3.md §6.5:185-202 -->
### 6.5 The move round at temperature φ

A round is the list of m = p + B + 2 labelled elementary steps — the p Gibbs coordinate updates, one uniform swap, B neighbour
swaps, one independence proposal — applied **in a uniformly random order drawn independently of the particle's state, afresh
for every particle and every round**.

- **Gibbs coordinate j:** draw j's inclusion from its conditional under γ_φ, with an addition at |S| = K excluded. Record the
  conditional inclusion probability o_j immediately before the draw (used for PIPs in measured rounds).
- **Uniform swap:** skipped (self-loop) if |S| ∈ {0, p}; delete j uniformly from S, add l uniformly from outside; accept with
  1 ∧ γ_φ(S′)/γ_φ(S).
- **Neighbour swap:** skipped if S = ∅; delete j uniformly from S; if N(j) \ S = ∅ reject; else add l uniformly from N(j) \ S;
  accept with 1 ∧ [γ_φ(S′)/γ_φ(S)]·|N(j)\S| / |N(l)\S′|.
- **Independence proposal:** S′ ~ π₀ (exact draw), accepted with 1 ∧ e^{φ[d(S′) − d(S)]}. Every proposal is scored, accepted or
  not.

Each step is reversible with respect to γ_φ; the composition in a random order whose law is invariant under reversal is
self-adjoint (checked by all three consultants; V5). An individual realised order is not.

<!-- END VERBATIM METHODOLOGY_v3.md §6.5:185-202 -->

## A1.7 Resampling, pilot, candidate set V, grid, islands, calibration and final runs, checks (METH3 §6.6–§6.9, verbatim) and the v3.1 additions to them

"Islands" are the independent final runs (default R = 4; stacking R′ = 4k) and the 4 diagnostic islands per calibration rebuild; each island's Ẑ_r is unbiased given the frozen calibration record 𝒞.

<!-- BEGIN VERBATIM METHODOLOGY_v3.md §6.6–6.9:203-255 -->
### 6.6 Resampling and the pilot schedule

- **Resampling:** fresh multinomial resampling after every reweighting, including the terminal stage (O(N) per stage with a
  linear-time categorical sampler).
- **Pilot:** H_e particles from π₀; at each stage the next temperature is the largest φ′ with population ESS of the weights
  e^{(φ′−φ)d} at least 0.90·H_e (weight CV² ≤ 1/9), found by 60 bisection halvings; exploratory floor 1/T_e (forced steps
  counted as `forced_pilot_steps`); ends exactly at φ = 1; then L burn-in rounds, 4 measured rounds and a local search.

### 6.7 Candidate set and candidate grid

- **V:** the union of the top 20p scored models by log γ₀, the top 20p scored models by log γ₁ (the target), and ∅;
  deduplicated; list ties lexicographic; frozen during each construction.
- **Restricted log-normaliser:** F_V(t) = log Σ_{S∈V} γ₀(S) e^{t d(S)}.
- **Restricted ESS** between temperatures u < v: ρ_V(u, v) = exp{2F_V(v) − F_V(u) − F_V(2v − u)}, the population ESS fraction
  of the weights e^{(v−u)d} under the restricted law q_u(· | V) (evaluating F_V beyond 1 is a finite-sum moment, not a
  production temperature).
- **Construction:** start at u = 0 with the pilot temperatures as targets. For the next pilot temperature b: if
  ρ_V(u, b) ≥ 0.90 append b; otherwise bisect on (u, b] with u fixed, at most 60 halvings, and append the largest tested
  endpoint that passes; continue from the appended point. Validate strict numerical progress and the inequality at every
  appended point. Non-progress, failed validation, or more than T_e intervals → the construction fails.
- **Rebuild loop:** after each set of diagnostic islands, update V and rebuild; stop when the rebuilt grid equals the
  previous one; at most ℓ iterations (lead's ruling: convergence is judged on the grid, not on V, because with a flat
  posterior the top list keeps changing by Monte Carlo noise; Fable-T3 proposed judging it on V). If not converged: flag `grid_unconverged` (a calibration trigger); at tier 1 the last
  grid is used and the flag is reported. If a construction fails: trigger escalation at tier 0; status `schedule_limit` at
  tier 1.
- **Purpose:** the pilot cannot see a mode it has not sampled, so its schedule may jump across the point where a competing
  model takes over. The grid inserts temperatures exactly where models already scored would make the bridge jump. Fable-T3's
  two-state analysis (to be proved, V11): if the competing pair is in V and the bridge is pair-dominated, the final-run relative
  evidence error is O_P(√(cT/N)) at fixed N. Without it, the evidence can be off by n^{−1/2} (proxy deletion) or e^{−Θ(n)}
  (proxy block plus a near-cancelled true variable), while every self-check passes.
- **Limits:** the grid controls restricted one-step weight dispersion only; it does not control full-space ESS, particle
  occupancy, mixing, or modes never scored; |V| ≤ 40p + 1 may truncate when many near-equivalent models matter. Cost per
  construction ≤ 60·|V|·T_e scalar log-sum-exp evaluations (≈ 2.4·10⁹ at p = 1,000, T_e = 1,000 in the worst case; the
  consultants differ on whether this is negligible against scoring; it is measured, not assumed).

### 6.8 Calibration and final runs

- **Calibration** (tier e): the pilot (§6.6) and, per rebuild iteration, 4 diagnostic islands of H_e particles on the current
  grid, each followed by L burn-in rounds, 4 measured rounds and a local search. Streams 0 and 1–4 (tier 0), 5 and 6–9 (tier 1).
  Score leaders are kept across tiers.
- **Final:** 4 islands × N_e particles from fresh iid π₀ draws, the frozen grid, multinomial resampling, one move round per
  stage, then L burn-in rounds and 4 measured rounds at φ = 1, then a local search. Streams 10–13, independent of all
  calibration randomness. No forced steps.

### 6.9 Checks and escalation

Calibration triggers (any one ⇒ at most one escalation to tier 1, decided before any final randomness):
E1 some diagnostic island's best score is more than 1 nat below the overall best (a missed mode worth a factor e in odds);
E2 the SD of the 4 diagnostic log Ẑ exceeds 1 nat (evidence not known within a factor e); E3 a local search improved the best;
forced pilot steps; `grid_unconverged`; a failed grid construction; `local_limit`.
Forced pilot steps trigger tier 1 but do not invalidate a successfully constructed grid. After the final run, E1–E3 and the
empirical-ESS check are recomputed as flags only.

<!-- END VERBATIM METHODOLOGY_v3.md §6.6–6.9:203-255 -->

### v3.1 additions: parallel layer, GUARD-W, stacking, LS0 (METH31 §2 #1–#10, verbatim)

<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md §2 #1–#10:127-152 -->
### Parallel execution layer

| # | change | M § | exact new spec text (short) | class | effect on the 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 1 | **(a) Concurrent final islands** | §6.1, §6.8, §7, §8.6 ("Islands may run sequentially") | "The R′ final islands run as concurrent **process** workers, each with its own score cache and ledger. Their stores and running HPM are merged by Lemma S before the final local search. Output is bitwise-identical to serial execution (Prop W). 'Bitwise' is scoped to one binary (`Makevars.v3`: `-ffp-contract=off -march=x86-64-v2`), single-thread BLAS and process workers." | ADDITIVE (bitwise) | none. Executed bitwise on smoke + 3/3 study designs (CONC; S1 §0.1). Serial study output = v3.1 output. No re-run. | DOSSIER §2(a); S1 item 3; R2_B D3f; MA §4 C1 |
| 2 | **(b) Concurrent diagnostic islands** | §6.7–6.8 | "In each rebuild iteration the 4 diagnostic islands run as concurrent process workers (persistent per tier), merged before each local search and before V is rebuilt (Prop W-cal). 'Bitwise' may **not** be claimed for (b) until W-cal has been executed (§6)." | ADDITIVE (bitwise) **claimed from code reading only**. If W-cal fails, it becomes LAW-PRESERVING and the wall-clock claim is capped at the D4 numbers (R2_B §5 item 4). | none. The study ran calibration serially, so its calibration is the reference that W-cal must reproduce. No re-run. | DOSSIER §2(b); S1 item 3; S3 R3-7 note; MA §4 C2 |
| 3 | **(c) Parallel local-search scans** | §6.10 | "Each scan's candidates (p + k(p − k) flips and swaps) may be scored in parallel. The best strict improvement is chosen by a max-reduction that keeps the lexicographic tie rule, so the search path equals the serial one." | ADDITIVE (bitwise if the reduction keeps the tie rule) | none. No re-run. | DOSSIER §2(c); S1 item 3; MA §4 C3 |
| 4 | **(h) Block-table stage as the explicit parallel local step** | §6.3, §8.2 | "Block tables are scored in parallel over blocks and sub-models; each score is independent. No floating-point summation order may change under a bitwise claim. Parallel convolution and other reductions need a separately specified order, or a narrower numerical-equivalence claim." | ADDITIVE (bitwise) | none. No re-run. | S2 D3e; R2_C D3e; R2_A D3e; R2_B D3e |
| 5 | **Process workers; counter rule** | §6.1 (new sentence) | "Workers are processes. If threads ever share `Data`, the mutable diagnostic counters (`cpp/v3_score.h:20–21, 231–236`) must become per-worker private counters, merged deterministically." | ADDITIVE (engineering) | none | S2 D3f; S1 §0.4 [chair-checked] |
| 6 | **GUARD-W semantics** | §2 statuses, §8.6, §6.1 | "Any worker stop, LS0 stop or guard stop ⇒ no output. The fit returns the corresponding unavailable status with all estimate fields NA (#15), never a partial estimate." Here an LS0 stop is an operational interruption (worker, guard or resource stop) before LS0 completes. A completed LS0 that ends on its move cap is not a stop: it returns output with `local_limit`, and L1 = "n/a" (#10). Lemma RO (a guard that reads no uniforms is stop-only) stays as recorded (XF VERIFIED). That the v3.1 worker, merge and LS0 code satisfy GUARD-W is a **code-audit obligation** (§6), not a mathematical gap. | ADDITIVE (spec) | none on completed fits. The 6 `resource_limit` fits stay stops. | S1 item 3; S3 R3-1 (B), R3-5(ii); R3_B R3-1 amendment 1 |

### Stacking

| # | change | M § | exact new spec text (short) | class | effect on the 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 7 | **Optional stacking R′ = 4k at N_e** | §3 (R), §6.1, §6.8, §6.9, §7 | <ul><li>"R′ = 4 by default. Optionally R′ = 4k, at **unchanged N_e**, declared before final randomness (before stream 10)."</li><li>"Final islands use streams 10, …, 9 + R′. Islands 1–4 keep streams 10–13. **N_e is never split** across more islands."</li><li>"With R′ > 4, an **extra local search runs from the islands-1–4 centre c₄**, besides the search from the expanded centre. The post-search scored set is then nested and HPM(R′) ⪰ HPM(4) (Cor W-R with the extra search, PC1 claim 6)."</li><li>"Two records are kept. The **expanded record** covers all R′ islands, pooled Ẑ over R′ and the expanded store; it carries the run's reported flags. The **baseline record** covers islands 1–4, with its own baseline HPM, the search from c₄ and its own E1–E3, low-ESS and `local_certified`. It is kept whenever baseline reproducibility is claimed."</li><li>"Each record has its own certificate card (#13)."</li></ul> | ADDITIVE (nested) | none. The study is R′ = 4, and each study fit is its own baseline record. No re-run. | DOSSIER §2(d); S2 D3a, D3b, P-9 w7; S3 R3-4 (w7); PC1 claim 6; THEOREM_REVISION_INPUTS M7 |

PC1 claim 6 notes that E1, E2 and low-ESS on islands 1–4 match the v3 run. E3 and `local_certified` match only when they are evaluated on the search from c₄. The baseline record therefore holds both of those.

### LS0

| # | change | M § | exact new spec text (short) | class | effect on the 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 8 | **LS0: local search from the start mode** | §6.10, §6.1, §7, §2 (provenance) | <ul><li>"After the final local search (and after the extra search from c₄ when R′ > 4), run one local search with the §6.10 rules from the start mode S̃₀ = argmax γ₀. S̃₀ is computed exactly by the block DP, with the size-then-lexicographic tie rule."</li><li>"LS0 reads no uniforms. Every model it scores joins the all-scored set and the stores."</li><li>"Models first scored by LS0 have provenance `ls0`. The flag `ls0_improved` is set if LS0 raised the best score."</li><li>"**An LS0 improvement does not fire E3.** E3 refers only to the final local search from the HPM centre."</li><li>"An operational LS0 interruption means no complete output (GUARD-W, #6). A completed LS0 capped at `local_limit` still returns output (#10)."</li><li>"Start-mode ties: keep the enumeration fast path (cap 10⁶, `cpp/v3_start.h:183`). On truncation, use a deterministic tie-aware DP that returns the prescribed smallest-size, lexicographically smallest maximiser without enumerating ties (e4, #29)."</li></ul> | ADDITIVE | Production had no LS0. In the O-LS0 test export LS0 changed **0 of 2,394** HPMs, which implies `ls0_improved` = FALSE on all 2,394. 0/2,400 tie truncations; all 2,400 had a single tie (`/home/fb31/ls0_work/agg_final/ls0_per_fit.csv`, R2_C §4.2 E2). The merged-core replay is pending (§6). No re-run. | DOSSIER §2(f); S1 item 2, D3c; S2 D3c; R2_B D3c; S2 P-9 e4; S3 R3-4 (e4) |
| 9 | **D3c wording for LS0** | paper / §12 | "Appending LS0 preserves the preceding sampler computation. Island outputs, Ẑ and PIPs are unchanged. The all-scored set is enlarged (nested) and the best score cannot fall. The bounded top store is **𝒯_new = top_c(𝒯_old ∪ 𝒮_added)**, not a superset of 𝒯_old, because of eviction (`cpp/v3_ledger.h:41`). Near ties, provenance, flags and certificates are recomputed for the returned model. HPM unchanged on 2,394/2,394 (test export)." The sentences "stores nested" and "bitwise fit" are **struck**. | spec text | none | S2 D3c (C's correction + B's flag); R2_C D3c |
| 10 | **Certificate attaches to the returned Ŝ** | §6.10, card | "`local_certified` and card item L1 are evaluated on the finally returned Ŝ, from whichever search ended on it (final search, extra search from c₄, or LS0). A completed LS0 that ends on its move cap (`local_limit`) gives L1 = 'n/a'; the fit's output is still returned. An operational LS0 interruption is a GUARD-W stop (#6)." | ADDITIVE (spec) | none (LS0 changed no HPM) | S3 R3-1 (A); R3_A R3-1 addition 2 |
<!-- END VERBATIM METHOD_v3.1_FINAL.md §2 #1–#10:127-152 -->

## A1.8 Local search, HPM rule (METH3 §6.10, verbatim); LS0 (above, METH31 #8–#10)

<!-- BEGIN VERBATIM METHODOLOGY_v3.md §6.10:256-268 -->
### 6.10 Local search and the decision rule

- **Local search:** from the current best scored model (the centre), scan every feasible flip and swap (additions beyond K
  excluded) with the centre frozen during the scan; move to the best strict improvement (lexicographic ties); at most ℓ moves,
  then one further scan; stop earlier when a scan finds no improvement. Every evaluated model updates the global best. If the
  last scan still improves, set `local_limit` (no restart). `local_certified` only when the returned model is a scanned centre
  with no improving neighbour. The search never alters particles.
- **HPM:** the strict maximum of log ϖ(S) + log m(S) over every model ever scored (tables, pilot, calibration, final rounds,
  rejected proposals, independence proposals, local searches), kept as a running best that survives cache eviction. Only
  exactly equal scores invoke the tie rule: smallest |S|, then lexicographically smallest index set. A near-tie list (models
  within 10⁻⁹ nat of the best, drawn from the stored top 40p + 1) is reported; it never reorders, and `near_tie_truncated` is set
  if the list may be incomplete.

<!-- END VERBATIM METHODOLOGY_v3.md §6.10:256-268 -->

## A1.9 PIP rules (primary/secondary), Ẑ and evidence, MPM, general-h accumulator, certificate and output conventions

METH3 §6.11–§6.12 are the base; METH31 #11 swaps primary and secondary pooling ("Primary: PIP̂_j = Σ_r Ẑ_r PIP̂_rj / Σ_r Ẑ_r"; MPM threshold ½; R_eff). Position of the change: [pos 1107] ("The Ẑ-weighted PIP is reported"), [pos 1251] ("The Ẑ-weighted PIP becomes primary"), `MEET-v31/MINUTES.md` §2 decision 8.

### Base rules (METH3 §6.11–§6.12, verbatim)

<!-- BEGIN VERBATIM METHODOLOGY_v3.md §6.11–6.12:269-283 -->
### 6.11 PIPs

In the 4 measured final rounds, average the recorded conditional inclusion probabilities o_j (Rao–Blackwellisation) over
particles and rounds within each island. **Primary:** equal-weight mean over the 4 islands. **Secondary:**
Σ_r Ẑ_r PIP̂_{rj} / Σ_r Ẑ_r (consistent as the number of islands grows at fixed N, because Ẑ_r·PIP̂_{rj} is unbiased for
Z·PIP_j; to be proved, V6). Neither normalised estimate is unbiased at finite budgets. MPM = {j : primary PIP̂_j > ½}; it may
exceed K and is reported as computed.

### 6.12 Evidence

Final island r: Ẑ_r = m(∅) Z̄₀ ∏_t (1/N_e) Σ_i exp{(φ_t − φ_{t−1}) d(S_i^{(t−1)})}, with W_K inside γ₀ exactly once.
Pooled Ẑ = (1/4) Σ_r Ẑ_r via log-sum-exp; 95% lower bound 0.05·Ẑ (Markov; one-sided, not an accuracy interval). Reported on
the full working scale and relative to m(∅). Given the frozen calibration, each Ẑ_r is unbiased (existing project results P6,
P7); log Ẑ is not.

<!-- END VERBATIM METHODOLOGY_v3.md §6.11–6.12:269-283 -->

### v3.1 reporting changes #11–#21 (METH31 §2, verbatim)

Contains: primary/secondary PIP (#11), general-h accumulator 𝓗 (#12), certificate card (#13), Z_𝒯 and the underestimation certificate (#14), NA outputs (#15), output convention (#16), card probability sentence (#17), calibration contract (#18), depth and cost statement (#19), memory wording (#20), §9 limitation wordings (#21).

<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md §2 #11–#12:158-159 -->
| 11 | **Ẑ-weighted PIP primary; equal-weight secondary; both MPMs; R_eff** | §6.11, §2 outputs, §11 V6 | <ul><li>"**Primary:** PIP̂_j = Σ_r Ẑ_r PIP̂_rj / Σ_r Ẑ_r over the R′ final islands."</li><li>"**Secondary (named):** the equal-weight mean over islands."</li><li>"Report MPM_Ẑ = {j : primary PIP̂_j > ½} and MPM_eq. Either may exceed K and is reported as computed."</li><li>"Report R_eff = (Σ_r W_r)² / Σ_r W_r² with W_r ∝ Ẑ_r."</li><li>"Neither normalised estimate is generally unbiased at a finite budget."</li><li>"The R-scaling guarantee is stated for the primary PIP; the equal-weight PIP keeps its single-island bias for every R (Prop P(i))."</li></ul> | POST HOC | No refit. The study's equal-weight PIPs and MPM_eq stay valid as the secondary. The primary and MPM_Ẑ need the full rescoring from the NOTS bundles. Done so far on 3 designs: MPMs never differ, max\|ΔPIP\| ≤ 1.3·10⁻³, island ESS 1.88 on S5 r002 (S2 §0.2). | DOSSIER §2(e); S1 item 5; S2 D5; R2_B D5 (R_eff); MA §4 C5 |
| 12 | **General-h accumulator** (adopted text) | new §6.11b | **Declaration.** "𝓗 is a finite list of bounded model-space functions. The default list is fixed from (X, y): model-size indicators, and joint inclusion on neighbour-graph edges (≤ 2pB pairs). A user may also declare h measurable in (X, y, 𝓒), fixed before stream 10. An h defined from other calibration information (streams 0–9) is covered only if that information is included in 𝓒 before it is frozen (enlarge 𝓒 when necessary); measurability in streams 0–9 need not imply measurability in the compressed 𝓒. No final-run selection." **Accumulation.** "H_r(h) = (4N_e)⁻¹ Σ_{q=1..4} Σ_i h(S_rqi), taken after each complete measured round (φ = 1, equal weights after multinomial resampling). Report μ̂(h) = Σ_r Ẑ_r H_r(h) / Σ_r Ẑ_r and the equal-weight version." **Not allowed.** "Products of marginal RB-PIPs are not joint estimates. v3.1 ships plain measured-round particle averages for joint h (c_h = 0). Rao–Blackwellisation is used only for the marginal PIPs. No RB joint estimator ships." **Archive (optional).** "The measured-round populations as a key → count multiset. An h chosen adaptively after the run does not inherit the fixed-h guarantee." **Continuous parameters.** "Use h̄(S) = E[h \| S, X, y]." **Descriptive only.** "The measured-round frequency of the returned HPM is **not** in 𝓗. It may be printed as a descriptive diagnostic with no theorem, next to e^{F(Ŝ)}/Ẑ." Placement in code: `cpp/v3_engine.h:351–359`. The identity for general h is a PROOF SKETCH (N1). | ADDITIVE (reads no uniforms) | none. Not recoverable for the study, so **no joint-summary claims** for the 2,400 fits. | S2 D7, P-D7; S3 R3-3 (adopted text); R3_A, R3_B, R3_C R3-3 |
<!-- END VERBATIM METHOD_v3.1_FINAL.md §2 #11–#12:158-159 -->
<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md §2 #14–#15:161-162 -->
| 14 | **Z_𝒯 and the underestimation certificate** | §6.12 | "Report Z_𝒯 = Σ_{S∈𝒯} e^{F(S)} over the deduplicated reported store. Ẑ < Z_𝒯 implies Ẑ < Z." This is part of G1 and ships in any case. | POST HOC | as #13 | S1 item 6; PC2 G1; THEOREM_REVISION_INPUTS M10 |
| 15 | **Unavailable output = explicit NA** | §2 statuses, §7 | "On every return without complete output (`resource_limit`, `schedule_limit`, `numerical_failure`, GUARD-W stops, LS0 stop, degenerate statuses), `fit$log_Z` and **every estimate field** (Ẑ_r, Ẑ, bounds, PIPs, MPMs, μ̂(h), card) are NA by exact name. Partial calibration or island values may be archived under their own labels; they never masquerade as final estimates." This fixes the partial-match hazard, where `fit$log_Z` silently returned `log_Zbar0` (API-AUDIT §2b). | ADDITIVE (interface) | Completed fits are untouched. Only the 6 stopped fits' records change: a consumer can no longer print a wrong evidence for them. | DOSSIER §2(g); S1 item 8; R1_B §2.8.1; R1_C:256 |
<!-- END VERBATIM METHOD_v3.1_FINAL.md §2 #14–#15:161-162 -->
<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md §2 #16:168-168 -->
| 16 | **Output convention** | Requirements (1), §2, §9 | "Every estimate on the output event 𝒪 is a function of (X, y, seed, binary). The allocation and hardware decide **delivery only** (stop-only guard, Lemma RO). Guarantees are stated for the potential (uninterrupted) run and as **P{𝒪, ·}** (joint with output), never as P(· \| 𝒪). P(no output) is an operational frequency that depends on the allocation and hardware, and is reported with them (V13)." | spec text | none. The 6 stops are delivery events. | S2 P-9 e8; S3 R3-4; R2_A §4; R2_C §4.4; PC2 C6 item 4 |
<!-- END VERBATIM METHOD_v3.1_FINAL.md §2 #16:168-168 -->
<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md §2 #18:170-170 -->
| 18 | **Calibration contract** | §6.7–6.9 (new paragraph) | "The calibration output 𝓒 (grid, budgets N_e, tier, R′, V-independent settings) is frozen before any final randomness. Validity of the final estimates (unbiased Ẑ_r, PIP identities) holds conditionally on **any** frozen 𝓒, whatever happened in calibration. The grid satisfies Theorem G's cap. There are ≤ ℓ rebuilds per tier (≤ 2ℓ in total with escalation, `v3_calib.R:85, 141–149`). The restricted ESS controls one-step weight dispersion on V only. The statuses `schedule_limit`, `grid_unconverged` and `escalated` are distinguished. Rebuild convergence, P(S₀ ∈ V) and P(schedule_limit) are **OPEN theorem obligations, not inherent limitations**. Rebuilds, tier, T and convergence are tabulated POST HOC from saved fits." | spec text | none. The tabulation is POST HOC (§6). | S1 item 4; S2 D4; THEOREM_REVISION_INPUTS M8 |
<!-- END VERBATIM METHOD_v3.1_FINAL.md §2 #18:170-170 -->
Rows #13 (certificate card), #17 (paper sentence on the card's probability), #19 (depth and cost statement), #20 (D6(i) memory wording) and #21 (§9 limitation wordings) are at METHOD_v3.1_FINAL.md lines 160, 169, 171, 172, 173; #13 is reproduced in full in §2.1 below; #19 is quoted in TH08's card (Prop D) and in `notation_and_conventions_A.md`.

### Certificate card: spec text (METH31 §2.1, verbatim)

G1 (deterministic), G2 (one-sided, output-level), L1, L2, L3, R (optional); header labels "numerical implementation of an exact-arithmetic certificate". This is the "certificate card" that TH04 (M4) states theorems about.

<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md §2.1:212-255 -->
### 2.1 Certificate card: spec text (PC2 minimal card + S3 R3-1 additions)

**Header (applies to every item).**
- Every line is stated in exact arithmetic.
- Until SC(η_F) is established by validated arithmetic and VAL-FP holds at production size, every computed number carries the label **"numerical implementation of an exact-arithmetic certificate"**, with η printed (`v3_score.h:242–246`).
- **L1, L2 and R run under one declared certificate budget** (scores and B&B nodes, printed with the card). On exhaustion the item reports "unresolved". A failed or unfinished certificate never changes the fit's status (A).
- The card is computed after the run and never feeds back into calibration (S1 item 6).
- **Under stacking there is one card per reported record** (baseline and expanded), each with its own 𝒯 and Z_𝒯 (B).

**G1 (deterministic).** 𝒯 is the deduplicated reported store and Z_𝒯 = Σ_{S∈𝒯} e^{F(S)}. Then:
- Z_𝒯 ≤ Z;
- π(S) ≤ e^{F(S)}/Z_𝒯 for every S;
- π(A) ≤ Σ_A e^F / Z_𝒯 for every A ⊆ 𝒯;
- π(S)/π(Ŝ) ≤ e^{−g} on 𝒯 ∖ {Ŝ}, with g = F(Ŝ) − max_{𝒯∖{Ŝ}} F;
- Ẑ < Z_𝒯 ⇒ Ẑ < Z.

**G2 (one-sided, output-level).** Simultaneously for all S:
- π(S) ≤ min{1, e^{F(S)}/max(Z_𝒯, 0.05Ẑ)};
- π(Ω ∖ 𝒯) ≥ 1 − Z_𝒯/(0.05Ẑ). This is mass **outside the reported store** (never scored, or scored and evicted). It is **not** a bound on never-scored mass.

G2 fails only on {Z < 0.05Ẑ}, and P(run returns output and G2 is false) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05. This is a probability **joint with output, never conditional on completion** (C). Premises are PC1 claim 2 (i)–(iv). Premise (i) reads: "Lemma RO (XF VERIFIED) plus GUARD-W, the implementation fact 'any worker stop, LS0 stop or guard stop ⇒ no output' for v3.1 code: a code-audit obligation, not a mathematical gap" (B). If Z_𝒯 ≥ 0.05Ẑ, G2 holds surely (C6′).

**L1 (local).** Evaluated on the finally returned Ŝ, from whichever search ended on it. A completed LS0 that ends on its move cap (`local_limit`) gives "n/a" (A); an operational LS0 interruption gives no output (GUARD-W). If `local_certified`, then F(S) ≤ F(Ŝ) for every feasible flip or swap. Report:
- g_add, with +∞ if |Ŝ| = K;
- g_del, with +∞ if Ŝ = ∅;
- g_swap, with +∞ if there are no swaps;
- ρ_loc = π(Ŝ | {Ŝ} ∪ 𝒩(Ŝ)).

**L2 (subsets).** g_sub = F(Ŝ) − max_{S⊊Ŝ} F(S) and Σ_{S⊊Ŝ} π(S)/π(Ŝ). With max ∅ = −∞: when Ŝ = ∅, g_sub = +∞ and the relative subset mass is 0.

**L3 (best-of-scored).** If 𝒯 = top-(40p+1) of the realised scored set 𝒮 and |𝒯| ≥ 2, then π(S) ≤ e^{−g}π(Ŝ) for all S ∈ 𝒮 ∖ {Ŝ}, with g = F(Ŝ) − F(top[2]). This holds under LS0 because 𝒯_new = top_c(𝒯_old ∪ 𝒮_added) (R3_B R3-1).

**R (optional).** A declared region rule U(X, y, Ŝ) ∋ Ŝ, with node budget and τ printed. B&B on [∅, U] ∩ Ω, dropping leaves with |L| > K, gives (a)–(c) as in PC2. "Unresolved" on budget exhaustion. In floating point, (a) needs Φ̃ ≤ F̃(Ŝ) − 2η_F.

**Card-level statement.** "The probability that a run returns a card with a false G2, L or R claim is at most 5%", in exact arithmetic. G1, L and R are true surely. The floating-point version (≤ 0.05e^η + ε) needs validated SC **and** VAL-FP, neither of which is established, so it carries the numerical label (C).

**Excluded:**
- C2 (conditional on PW2);
- C5 (needs S₀);
- the "unscored mass" wording;
- the B&B cost remark;
- any rigorous reading of `global_certified`.

Sources: PC2 lines 194–235; S3 R3-1.
<!-- END VERBATIM METHOD_v3.1_FINAL.md §2.1:212-255 -->

## A1.10 Reporting amendments (AMENDMENT_HQ_02)

### Definitions sent by the theorem meeting chair (`MEET-THM/AMENDMENT_HQ_02_DEFINITIONS.md`, verbatim, whole file)

<!-- BEGIN VERBATIM MEET-THM/AMENDMENT_HQ_02_DEFINITIONS.md:1-72 -->
# MEET-THM → HQ · Definitions for AMENDMENT_HQ_02 (reporting and growth-rate amendment to METHOD_v3.1_FINAL)

Chair, 2026-11-04. HQ asked for these at close (ruling Q4, `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`).

The full theorem card is S-REP in `THEOREM_LIST_FINAL.md`, copied verbatim from `R3_C.md` §S2 "S-REP". Decisions are in `MINUTES.md` §2.2–§2.3.

Nothing below changes the method's law, its random numbers, its calibration, its schedule or its decision.

## A. Reporting fields (POST HOC; HQ Q4 conditions)

The conditions, all met by every field below:
- inputs are only quantities the run already computes;
- no random numbers are read;
- nothing feeds back into the run.

### A1. Ĵ: the Jeffreys-divergence estimate (decided: the B/C/D form, unanimous in Round 3)

**Inputs, from the final islands r = 1…R′:**
- **Initial records.** A_r = N⁻¹ Σ_{i=1}^{N} d(S^{(0)}_{ri}), over each final island's initial iid start particles. These are not reweighted.
- **Endpoint records.** B_r = (4N)⁻¹ Σ_{k=1}^{4} Σ_{i=1}^{N} d(S^{(k)}_{ri}), at the four prescribed measured endpoints. These are plain discrepancy means, not RB records.
- **The potential d.** d(S) = log BF(S) − Σ_b log r_b(S_b) is the bridge potential the run already evaluates. It is fixed from (X, y, blocks, tables) before final randomness.

**Estimator:**

  Ĵ = Σ_r Ẑ_r·B_r / Σ_r Ẑ_r − (1/R′)·Σ_r A_r,

reported in nats, with its signed value preserved.

**Target and statement:**
- J = KL(π‖π₀) + KL(π₀‖π) = E_π d − E_{π₀} d.
- For ε > 0: P(|Ĵ − J| > ε | 𝒞) ≤ min{1, 4(M₂ − 1)/R′ + 16D²M₂/(R′ε²) + D²/(R′Nε²)}, where D = max_Ω d − min_Ω d.
- The bound can equal 1 at the default R′ = 4. There is no default-budget accuracy claim.

**Label:** "Post hoc Monte Carlo estimate of Jeffreys divergence; not a certificate; floating-point error unvalidated." The exact branch may report NA.

**Implementation:**
- A read-only accumulator of d at initialisation and at the four measured endpoints. Per-particle d values exist during execution but are not retained today.
- No new draws, transitions or scores.
- Historical fits report NA. Absent records are not reconstructed.

**Declared list:** d becomes a default member of the declared summary list 𝓗 (METHOD §6.11b). It is fixed before stream 10 and reads no uniforms (Seats A and B: R3_A §S5, R3_B §S5). Because 𝓗 is defined as [0,1]-valued, **raw d is recorded**, and theorems (M1) apply to the globally range-scaled (d − min_Ω d)/D, with D = max_Ω d − min_Ω d > 0. If D = 0, then Ĵ = J = 0 (S-REP card).

### A2. ε̂_×: the cross-block correlation proxy, with companions

- **ε̂_×** = max over b ≠ c, j ∈ C_b, k ∈ C_c of |X_jᵀX_k|/(n − 1), on the standardised columns and the built blocks. The empty maximum is 0.
  - Field: `cross_block_rmax`.
  - Label: "Descriptive maximum cross-block correlation proxy; not signal leakage or a confidence bound; floating-point error unvalidated."
- **Companions:**
  - κ̂ = min_b λ_min(G_{C_b}/(n − 1));
  - if κ̂ > 0, δ̂ = (K − 1)·ε̂_×/κ̂;
  - ū̂ = Σ_b max_{U⊆C_b} x_b(U), from the block tables. This is a global envelope, **not** a maximum over V (MINUTES §2.2, C's objection adopted).
- **Domain:** κ̂ > 0, δ̂ < 1, ū̂ < 1 and δ̂·ū̂ < (1 − δ̂)(1 − ū̂). Outside it, η̂ is printed **"n/a"**.
- **Derived envelope:**
  - r̂ = δ̂ū̂/[(1 − δ̂)(1 − ū̂)];
  - η̂ = K·log(1/(1 − δ̂)) + ν·log(1/(1 − r̂)).
  - On the domain: sup_{S∈Ω} |d(S) − d_σ(S)| ≤ η̂.
  - For nonempty S: ε_S ≤ (|S| − 1)·ε̂_×/κ̂.
- **Not claimed:** no lower bound of order n·ε̂_×·|β_jβ_k| (refuted in check wave 2), and no global rescaling from V.

## B. Growth-rate edit (ground rule 5: growth rates as explicit functions of (n, p) only)

**Two optional stacking configurations** for the number of final islands R′. They are used on families where D_* = O_P(1), with D_* as defined in M2(a):
- **(i)** R′_n = 4⌈log₂(n + p + 1)⌉, for consistency of any fixed finite set of declared summaries;
- **(ii)** R′_n = 4⌈(n + p)⁶/4⌉, for simultaneous control of ≤ (n + p)² declared summaries.

**Unchanged:**
- The shipped default R′ = 4 is unchanged. It carries only the fixed-R′ statements.
- ℓ = ⌈log₂(n + p + 1)⌉, L = max{4, ⌈log₂(n + 1)⌉} and N need no edit.

**Basis:**
- `SYNTH_R2.md` §2.6, confirmed by all four seats in Round 3.
- Check wave 2 found both rates TRUE-AS-WRITTEN on the exhibited family: W2_PC1 item 6; W2_PC2 §6.
<!-- END VERBATIM MEET-THM/AMENDMENT_HQ_02_DEFINITIONS.md:1-72 -->

### HQ's adoption decision (`MEET-v31/AMENDMENT_HQ_02.md`, verbatim, whole file) — [pos 1639]

<!-- BEGIN VERBATIM MEET-v31/AMENDMENT_HQ_02.md:1-15 -->
# AMENDMENT_HQ_02 (HQ, 2026-11-04): reporting fields and growth rates from the theorem meeting

Source: MEET-THM close (`theory/MEET-THM` @ 514c8fc), `AMENDMENT_HQ_02_DEFINITIONS.md` (copied here verbatim as `AMENDMENT_HQ_02_DEFINITIONS_from_MEET-THM.md`), HQ ruling Q4. Nothing below changes the method's law, its random numbers, calibration, schedule or decision.

## Adopted
1. **Ĵ (Jeffreys-divergence estimate)**, field `J_hat`, exactly as defined in A1, with its label "Post hoc Monte Carlo estimate of Jeffreys divergence; not a certificate; floating-point error unvalidated". Implementation: a read-only accumulator of the bridge potential d at initialisation and at the four measured endpoints (no new draws, transitions or scores). Historical fits report NA.
2. **d joins the default declared list 𝓗** (§6.11b), recorded raw; theorems use the range-scaled version.
3. **ε̂_× (`cross_block_rmax`) with companions κ̂, δ̂, ū̂ (global block-table envelope), r̂, η̂**, exactly as defined in A2, with its label and its "n/a" domain rule.
4. **Optional stacking configuration (i): R′_n = 4⌈log₂(n + p + 1)⌉**, for consistency of any fixed finite set of declared summaries on families with D_* = O_P(1). The shipped default stays R′ = 4.

## Not adopted as a method configuration
- **Configuration (ii), R′_n = 4⌈(n + p)⁶/4⌉.** HQ keeps it **only as a sufficient rate inside the theorem** (M1's simultaneous-control clause: "for any R′_n ≥ 4⌈(n + p)⁶/4⌉"), not as a runnable configuration of the method. Reason: at study sizes (n + p ≈ 700) it is about 10¹⁷ islands, so listing it as a method setting would misrepresent what the method can run. The theorem is unaffected.

## Status
Reporting fields 1–3 are specified, not yet coded (engineering, with the other v3.1 additions). Every field is POST HOC: it reads no uniforms and never feeds back into the run.
<!-- END VERBATIM MEET-v31/AMENDMENT_HQ_02.md:1-15 -->

### Note appended to METH31 (verbatim)

<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md "Amendment HQ_02":423-425 -->
## Amendment HQ_02 (2026-11-04): reporting fields and growth rate from the theorem meeting

See `AMENDMENT_HQ_02.md`. Adopted: Ĵ (`J_hat`), d in the default 𝓗, ε̂_× (`cross_block_rmax`) with companions κ̂, δ̂, ū̂, r̂, η̂ (all POST HOC, no uniforms, no feedback), and the optional stacking configuration R′_n = 4⌈log₂(n + p + 1)⌉ (default stays R′ = 4). The rate 4⌈(n + p)⁶/4⌉ is a sufficient rate inside theorem M1 only, not a method configuration.
<!-- END VERBATIM METHOD_v3.1_FINAL.md "Amendment HQ_02":423-425 -->

Summary: the reporting fields (Ĵ = `J_hat`, d in the default 𝓗, ε̂_× = `cross_block_rmax` with κ̂, δ̂, ū̂, r̂, η̂) are POST HOC, read no uniforms, never feed back. Statement: "Reporting fields 1–3 are specified, not yet coded". The stacking configuration (i) R′_n = 4⌈log₂(n + p + 1)⌉ is the only one adopted as a method configuration; see the conflict note U1 in §A7 about configuration (ii).

## A1.11 Settings table and (n, p)-generality

The full 49-row settings table of METH31 §5 (class (a)–(e), reason, behaviour as n and p grow, action), the per-regime notes (§5.1), the theory-scope text (§5.2), and item-9 resolutions e1–e8, w1–w7 are reproduced verbatim in `notation_and_conventions.md` §N3–§N5. Headline values (copied verbatim there): g = n, τ = 1; IG(0.01, 0.01); BB(1, p) with w(k) = ½/C(2p−1, k); K = min(p, ⌊n/2⌋); B = min(⌊√n⌋, ⌊√p⌋, B*), B* = 16; ℓ = ⌈log₂(n + p + 1)⌉; L = max(4, ⌈log₂(n + 1)⌉); N₀ = max(2,500, n, p); H₀ = ⌈512·N₀/2,500⌉; T₀ = max(1,000, ℓ²); R = 4; ESS threshold 0.90; V = top 20p by γ₀ ∪ top 20p by γ₁ ∪ {∅}; top store 40p + 1.

## A1.12 Engineering/audit checks that gate claims (METH31 §6, verbatim) and points settled by the chair

<!-- BEGIN VERBATIM METHOD_v3.1_FINAL.md §6 and "Points settled":392-419 -->
## 6. Engineering checks before the paper's claims (not method changes)

None of these can change a method decision taken in MEET-v31 (S3 R3-7; R3_A R3-7). Each one gates only the **claim** named.

| # | Check | Gates which claim | Source |
|---|---|---|---|
| 1 | **W-cal**: bitwise replay of `v3_calibrate` with concurrent diagnostic islands on the 3 replay designs (S1 r001, S4 r001, S5 r002). About 1 h on Owls with the METH-AUDIT harness. | "bitwise" for (b); any wall-clock claim (calibration is on the critical path) | DOSSIER §4.5; MA §4 C2; S1 item 3; S3 R3-7 |
| 2 | **Merged-LS0 replay**: integrated core versus the O-LS0 export on the 3 designs. Covers HPM, stores, flags, E3 unchanged, `ls0_improved`, stream endpoints, and a deterministic eviction/tie example. | "LS0 is in the shipped core"; T38(b1-LH) as a theorem about the shipped method | S2 D3c; R2_B §5 item 5; R2_C D3c |
| 3 | **GUARD-W audit**: code audit that the v3.1 worker, merge and LS0 paths satisfy "any worker stop, LS0 stop or guard stop ⇒ no output" (OP-LS0 included). Plus API-AUDIT's forced-stop table (10 fits) after the `log_Z` NA fix. | premise (i) of G2 and of every P{𝒪, ·} statement | S3 R3-1 (B), R3-5(ii); R1_B §2.8.1 |
| 4 | **IND-T for streams 10..9+R′**: independence of the final streams from calibration streams for every declared R′ | stacking (#7) theorems; the frozen-𝓒 contract | S3 R3-7; THEOREM_REVISION_INPUTS M12 |
| 5 | **VAL-FP at production size**: long-double replay on 2 study designs at p = 500 (measured so far only at p ≤ 40; ε scales with R′/4) | the floating-point card statement (with validated SC). Removing the numerical label needs validated arithmetic (SC) **and** VAL-FP; a long-double replay alone is not enough | R1_A §2 item 2, Q10; PC2 C6 item 5 |
| 6 | **Preflight fixes** (e6) and an allocation audit of concurrent peak memory and stop behaviour | `resource_limit` estimates labelled "estimate" | S2 P-9 e6; R2_C §4.2 E4 |
| 7 | **Checked arithmetic** (e7): boundary tests for integer, stream-id and allocation overflow | support at huge (n, p) | S2 P-9 e7 |
| 8 | **Full POST HOC PIP rescoring** on the NOTS/laptop bundles (`pip_rescore.R`), with R_eff per fit; A's D5 reversal criterion is read against it by HQ | Ẑ-weighted primary PIP and MPM_Ẑ for the 2,400 fits | S2 §0.2; S3 R3-7; R3_A R3-7 |
| 9 | **Calibration timing tabulation**: `timings$calibration` and `timings$final` (`v3_fit.R:124, 136`) plus rebuilds, tier, T and convergence from the saved fits | the cost wording (§2 #19); calibration contract tabulation | R2_B D4, §5 item 3; S1 item 4 |
| 10 | Also listed by seats: the e4 tie-DP invariant (N3, a proof obligation) and the n = 2 boundary tests (e3) | LS0 under truncation; n = 2 support | S3 R3-4 |

---

## Points settled by the chair after drafting

1. **Item 1:** Outcome 2 under the pre-registered rule (`ITEM1_ABL_START.md`).
2. **ESS 0.90:** class (c) with Seat B's caveat; B's preference for (a) is a recorded label difference (MINUTES §4), not an open method question.
3. **Names:** e7 status `unsupported_size`; `global_certified` keeps its field name and is documented as heuristic (e5).
4. **HPM terminal frequency:** not in 𝓗; descriptive only (SYNTH_R3 R3-3).
5. **Calibration-cost ratio 0.0512 + 0.2048·I (single tier; rounded 0.05 + 0.2·I):** seat-derived, unchecked; quoted as such; matches the three logged designs.
6. **Certificate card on the study fits:** computable wherever the saved top store exists (NOTS bundles; HQ action), otherwise not claimed.
7. **A2 wording:** a THEOREM_LIST edit (PC1 claim 4); no METHODOLOGY_v3 sentence needs deleting.
<!-- END VERBATIM METHOD_v3.1_FINAL.md §6 and "Points settled":392-419 -->


---

# A2 · The final paper-1 list: main cards M1–M8 (TH01–TH08)

Source of all eight cards: `MEET-THM/THEOREM_LIST_FINAL.md` Part I, assembled from `MEET-THM/MINUTES.md` §2.1 ("Main text: 8 theorems (unanimous in Round 3)"). Selection history in one line: Round 0 → 108 candidates K01–K108 (`R0_DIFF.md`); Round 1; HQ Q1–Q4; check wave 1; inherited-proof check; synthesis 1; Round 2; check wave 2; HQ Q5; synthesis 2; Round 3 (`MEET-THM/MINUTES.md` §1). Seats: A (Fable 5.1), B (Fable 5.1), C (gpt-6-astra), D (Fable 5.1, the fresh-eyes seat). Checkers: PC1 = gpt-6.1-sol (cross-family on A, B, D), PC2 = Opus 5.5 (cross-family on C); inherited-proof checker CHK_INHERITED = PC1.

**What "checked" means in these cards.** (i) Clause verdict rows such as "W1PC1:109–110 TRUE" or "W2PC2 TRUE-AS-WRITTEN" are statement-sanity checks (counterexample search, non-vacuity), "not a proof" (check-wave briefs); they never upgrade a status. (ii) "SF"/"XF" in a status are proof checks of the ingredient proofs recorded in the registry. (iii) "(by this seat, unchecked)" is the only status a seat may give its own argument.

**Binding goals and safeguards (`MEET-THM/MINUTES.md` §2.3 §2.7, verbatim):**

<!-- BEGIN VERBATIM MEET-THM/MINUTES.md §2.3:89-90 -->
| §2.7, safeguards | §13.1: if N1's general record identity fails, the narrower theorem ships and §13.1 escalates. §5.3: if both the D_* route and the correlated-family route fail, it escalates. Also: loss of the masked statement without an approved replacement escalates (C §S5) | — |
| Audit obligations | N2(b), N2(c), N2(e), N14(c), the N3 DP invariant, and the integrated streams/LS0/GUARD-W/execution-DAG audits are **named implementation premises in the charters** and are recorded in `REGISTRY_PAPER1.md` (B's "missing" item 2, adopted) | — |
<!-- END VERBATIM MEET-THM/MINUTES.md §2.3:89-90 -->

**Waves and HQ charters** (`MEET-THM/MINUTES.md` §2.5; charters in `MEET-THM/HQ_CHARTERS/`, one file per main theorem M1.md…M8.md, plus LP-FOUND, LP-IDENT, LP-AUDIT, LP-REST, LP-REP):

### 2.5 HQ plan (agenda 12): waves

The chair merged the seats' proposals (A §S3(b), B §S3(b), C §S3, D §S3(b)) as a procedural decision. B and D nearly coincide, and A differs only in placing M1 in wave 2. Supplement cards are bundled into lemma-pack HQs, as D proposed.

| Wave | HQs | Reason |
|---|---|---|
| 1 | **M1** V/H; **M3** START; **LP-FOUND** = S-TARGET + S-BLOCKS + S-KERNEL (+ S-T cited) | Foundations. N1 (binding §13.1) is the longest pole and starts first (B, D) |
| 2 | **M2** WS (binding §5.3); **M7** STG; **M6** SEP + KL; **LP-IDENT** = S-IDENT | The §5.3 package and its inputs (d_σ from M3, the count from M7, the lower bound from M6) |
| 3 | **M5** HPM; **M4** Z𝒯 + masked statement; **M8** Prop D; **LP-AUDIT** = S-CERT + S-OUT | Code-audit wave: N2, N3, LS0, GUARD-W and the DAG serve M5, M4 and M8 together. M4(f) needs M5 |
| 4 | **LP-REST** = S-Z + S-POOL + S-LIM; **LP-REP** = S-REP + S-LEAK | Consequences and reporting corollaries. Nothing binding waits on them |

**Dependency graph:** the union of the seats' edge lists (A §S3(a), B §S3(a), C §S3, D §S3(a)), consolidated in `REGISTRY_PAPER1.md` §dependencies.


---

## TH01 (M1 Theorem V/H (validity of v3.1 and accuracy of reported bounded functionals))

| Field | Value |
|---|---|
| Archive ID | **TH01** |
| Native name | M1 · Theorem V/H (validity of v3.1 and accuracy of reported bounded functionals) |
| K-IDs (MINUTES §2.1) | K46, K32, K86, K35, K36, K50, K51, K52, K48, K62; cited K20, K21, K08, K47 (the card's own header lists a different K-set; see the integration note and U4 in §A7) |
| Authoring seat / final card source | Seat A (Fable 5.1) · `R3_A.md:112–137` |
| HQ charter | `branch_snapshots/MEET-THM/HQ_CHARTERS/M1.md` (wave 1, `MEET-THM/MINUTES.md` §2.5) |
| Binding goal / escalation | Binding: proposal §13.1 ("E_π[h] → truth"). Safeguard: "if N1's general record identity fails, the narrower theorem ships (marginal records, fixed finite classes) and §13.1 escalates to HQ; it is never dropped" (charter M1; MINUTES §2.3). Also §5.1 (with TH12) and §5.2. |
| Who checked (Summary, from the card's own verdict/status rows and `MEET-THM/MINUTES.md` §1) | Cross-family PC1 (gpt-6.1-sol) verdict rows W1PC1 (check wave 1) and W2PC1 (check wave 2) on Seat A's clauses; inherited-proof check CHK_INHERITED (gpt-6.1-sol, line by line): N9-KERNEL §§0–3 "VERIFIED WITH AMENDMENT" (amendments adopted); T12, T31(i) PROVED-LOCKED (inherited; locked inputs were checked for statement/hypothesis compatibility only); N1 = PROOF SKETCH (unchecked); clauses (h),(i) "PROVED (by this seat, unchecked)"; MA-PropP author-only; final audit CLOSE_AUDIT #2 (block matches R3_A range) and #6 (N14(c) label). N9 also tested against the production code (`theory/N9-KERNEL`, [pos 1550], [pos 1593]). |
| Dependencies (Summary of the card's Dependencies row) | K20, K21, K08, K47 (cited); S-KERNEL TH12 (N9); S-OUT TH15 (Lemma RO, GUARD-W, IND-T extension, K63, K86); S-TARGET TH10 (propriety); M2(b)(iv) TH02 and S-T TH09 (T03♯) for clause (i); feeds S-POOL TH17, S-REP TH19, M4(d) TH04, M8 TH08. |
| Source positions | [pos 1348] (HQ's early list: "Validity under parallel execution", "Posterior accuracy"), [pos 1626] (close), [pos 1639] (HQ approval with the growth-rate change), [pos 1650] |
| Statement location | `MEET-THM/THEOREM_LIST_FINAL.md` lines 94–129 (verbatim block below, including the card's own Hypotheses/premises, Statement, Status and Dependencies rows) |

**Chair's integration note(s) and verbatim card:**

**Chair's integration note.**
1. K-ID header: the card's own header line lists "K46, K32, K86, K85, K36, K78, K51, K52, K48, K62; cited K20, K21, K08, K35, K47"; MINUTES §2.1 lists K46, K32, K86, K35, K36, K50, K51, K52, K48, K62; cited K20, K21, K08, K47. The registry (`REGISTRY_PAPER1.md`) follows MINUTES. The card body is unchanged.
2. Growth rates (MINUTES §2.3 §2.6, confirmed by all four): clause (i) is the first stacking configuration, R′_n = 4⌈log₂(n + p + 1)⌉, for a fixed finite set of declared summaries on families with D_* = O_P(1); the second optional configuration R′_n = 4⌈(n + p)⁶/4⌉ for simultaneous control over ≤ (n + p)² declared summaries is added to the statement of (i). ℓ, L and N need no edit; shipped R′ = 4 carries only the fixed-R statements. d is a default member of the declared list 𝓗 (A, B; AMENDMENT_HQ_02).
3. Binding §13.1: if N1's general record identity fails, the narrower theorem ships and §13.1 escalates (MINUTES §2.3 §2.7; the card's own fallback agrees). K63 (worker equivalence) and K86 (IND-T) are named premises here and proved in S-OUT (R3-4).

<!-- BEGIN VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:100-129 -->
**Source:** `theory_campaign/MEET-THM/R3_A.md:112–137` (verbatim)

<!-- BEGIN VERBATIM R3_A.md:112-137 -->
### M1 · Theorem V/H (validity of v3.1 and accuracy of reported bounded functionals)

K-IDs: K46, K32, K86, K85, K36, K78, K51, K52, K48, K62; cited K20, K21, K08, K35, K47.

| Field | Content |
|---|---|
| Model/design hypotheses | Admissible standardised (X, y), n ≥ 3; h ∈ 𝓗 with 0 ≤ h ≤ 1, measurable in (X, y, 𝓒), declared before stream 10 (M9). For (i) only: T03♯'s hypotheses (R1, G, R, SE_λ, SE_w, BM-∞ or BM(c)) on a family with osc d ≤ D_* = O_P(1) (M2(a)), p ≤ n^A. |
| Implementation premises (named) | EX-A exact arithmetic; H-U/EX-S exact iid uniforms and exact start sampler (N9); CAL: 𝓒 frozen on streams 0–9; IND-T: streams 10..9+R′ independent (audited for R′ = 4; extension audit pending, S-OUT); R′ = 4k declared before stream 10; multinomial resampling; GUARD-W and Lemma RO for (d); M9 accumulator; stacking configuration R′_n for (i). |
| Statement | (a) Validity [cited]: each elementary move is γ_φ-reversible, the uniformly random-order round q_φ-invariant and self-adjoint under N9's sufficient conditions, draw_pi0 and Z̄₀ exact; each island is a Feynman–Kac model, so E[Ẑ_r \| 𝓒] = Z and E[Ẑ_r PIP̂_rj \| 𝓒] = Z·PIP_j with the RB record before the Gibbs draw (weighted identity; no terminal stationarity claimed). (b) Lemma N1: E[Ẑ_r H_r(h) \| 𝓒] = Z·π(h), H_r the plain measured-endpoint average. (c) Contract: (a),(b) hold conditionally on any successful frozen 𝓒; any R′ declared before stream 10 keeps them; adaptive R′ or conditioning on completion **need not** preserve them (CEX-guard). (d) Output event: P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05, never conditional on 𝒪. (e) Islandwise, every regime and frozen grid: E[W_r·\|H_r(h) − h(S₀)\| \| 𝓒] ≤ 2δ₁, δ₁ = 1 − π(S₀). (f) Finite R′, M₂ = E[W_r² \| 𝓒]: P(\|μ̂(h) − π(h)\| > ε \| 𝓒) ≤ min{1, 4(M₂−1)/R′ + 4M₂/(R′ε²)}; P(\|μ̂(h) − h(S₀)\| > t \| 𝓒) ≤ exp{−R′(1−s)²/(2M₂)} + 2δ₁/(st); vacuous at R′ = 4, informative under stacking; fixed data: μ̂(h) → π(h) a.s. as R′ → ∞ [cited]. (g) Declared classes: joint inclusions h_A = 1{A ⊆ S} on ≤ 2pB declared pairs (plain averages); interval probabilities h_I(S) = P(β_j ∈ I \| S, X, y) for a finite declared list, union bound; posterior-content error only, no quantile claim (HQ Q2). (h) Decision transfer: exact PIPs ≥ δ from ½ and uniform error < δ ⇒ reported MPM = exact MPM. (i) Asymptotic, with R′_n = 4⌈log₂(n+p+1)⌉: μ̂(h) → h(S₀) in probability, jointly with output; liminf P(𝒪 ∩ correct) = 1 − limsup P(U_n). |
| Verdict rows per clause | (a) W1PC1:109–110 TRUE; W2PC1:92 TRUE; CHK:94, 140–142 (N9 amendments adopted); RB wording per W2PC1:106. (b) W1PC1:110, W2PC1:92 TRUE; N1 PROOF SKETCH. (c) W1PC1:127 AMBIGUOUS → "need not" (W2PC1:92 REPAIRED). (d) W1PC1:126 TRUE. (e),(f),(g),(h) W1PC1:118, 120; W2PC1:93 TRUE (interval claim narrowed, W1PC1:263); W1PC1:240 (0 ≤ h ≤ 1); (h) W1PC1:302 TRUE. (i) W2PC1:94 TRUE on C's family; liminf form W1PC1:170. |
| Guarantee | Whatever the correlation, every island's unnormalised outputs are exactly unbiased given any frozen calibration, every reported bounded summary is right on the islands that carry evidence weight, and pooling enough declared islands by Ẑ makes it right. |
| Serves | Objective (1); proposal §5.1, §5.2, §5.4 (PIP, joint-PIP, posterior-content error), §13.1 (binding); Song–Liang Thm 3 (reported PIPs), UQ of merged output; INV rows 4, 6, 8, 10. |
| Status (verbatim) | T12, T31(i): PROVED-LOCKED; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); N9K: PROVED (candidate), code-checked; CHK_INHERITED: VERIFIED WITH AMENDMENT; N1: PROOF SKETCH; A1new: PROOF SKETCH (NEW-SYNTH); FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9)); PC1c3: PROVED (PC1 claim 3), 'E[W_r ĥ_r] = π(h) is still a premise'; MA-PropP: PROVED (elementary), author-only; IND-T: PROVED (SF: none; XF: VERIFIED* (A-REV1)); LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)); CEX-guard: COUNTEREXAMPLE; N6(a): PROVED (potential run; output form CORRECT WITH AMENDMENT); T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); (h), (i): PROVED (by this seat, unchecked). |
| Fidelity to v3.1 | (a)–(h) as shipped (LS0 alters no particle; any frozen grid; Ẑ-weighted primary). (i) uses the optional stacking configuration (AMENDMENT_HQ_02), not the default four islands. |
| Self-checked flag | N1 unchecked (PROOF SKETCH, numerically TRUE-AS-WRITTEN); MA-PropP author-only; N9 candidate plus cross-family CHK. |
| Novelty | (a), (f) fixed-data limits KNOWN—CITE: Del Moral 2004; Del Moral–Doucet–Jasra 2006; Whiteley–Lee–Heine 2016; Dai et al. 2022 (LIT-SMC rows 1, 21–22). (d) Markov KNOWN—CITE Grosse et al. 2015; the output-event discipline "genuinely non-standard" (LIT-SMC). (b), (e), (g), (h): NEW-COMP (M9 mechanism, measured-record identity). Checked against LIT-SMC/LIT-PAR digests only; citation checker to confirm volumes. |
| Route / key lemma | N1: finite-state resample–move recursion; the state before each measured record is Zπ-weighted because the prefix of a uniformly random order is state-independent (terminal-round prefix identity, N9 §3). (e): \|H_r − h(S₀)\| ≤ fraction of measured particles off S₀, then N1 on 1{S ≠ S₀}. (f): Chebyshev with the denominator event ≥ ½ (PC1 claim 3); Maurer/Hoeffding. (i): M₂ ≤ e^{D_*} (M2(b)) and R′_n → ∞. Key lemma: N1. |
| Difficulty | M (N1 one page; the rest assembly). |
| Lean core | T12Core `unbiased_of_step` with `hstep` discharged for multinomial resampling + an invariant kernel; detailed balance of the four kernels (finite matrices); (e) deterministic step; (f) finite inequality on abstract nonnegative weights; (h) finite; CEX-guard as a two-point example. |
| Dependencies | S-KERNEL (N9), S-OUT (Lemma RO, GUARD-W, IND-T extension), S-TARGET (propriety), M2(b)(iv) and S-T (T03♯) for (i); feeds S-POOL, S-REP, M4(d), M8. |
| Risk | N1 fails (binding §13.1); GUARD-W or IND-T extension audit fails (then (c),(d) stay potential-run statements). |
| Fallback + stop rule | Fallback: (a), (c), (d) plus (e)–(i) for marginal PIPs only (locked RB identity; no general h). Stop: one HQ wave on N1; if not closed, ship the fallback and **escalate §13.1 to HQ** (never dropped). |
| IC3 design, exhibited | (a)–(h): any admissible X, including duplicate columns (W1PC1 D0/E1 finite enumeration, W1PC1:69, 110). (i): C's family W (within 1/4, ε_n = 1/(np) > 0, two n^{−1/4} signals, blocks = groups for n ≥ 9⁶), D_* = O_P(1), checked with the method's own partition (W2PC2:53–58); also at ε = n^{−1/2}/p. |
| Numerical companion (≤ 20 seeds) | N9-KERNEL CHECK (DB ≤ 2.3·10⁻¹²); PC1 E1 two-state exact enumeration (exists). For the HQ: exact enumeration on p ≤ 8 of E[Ẑ_r H_r(h)] against Z·π(h) and of E[W_r\|H_r − h(S₀)\|] against 2δ₁ on a coded-grid replica, 10 seeds. |

Split note (if R3-1 (ii) were chosen instead): Proposition V+ = clauses (a)–(d) with the same premises; Theorem H = (e)–(i) with "Setting V+". Nothing else changes.
<!-- END VERBATIM -->
<!-- END VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:100-129 -->

**Growth-rate clause (i) and the HQ amendment.** The card prints clause (i) with R′_n = 4⌈log₂(n+p+1)⌉. The chair's note 2 says the second optional configuration R′_n = 4⌈(n + p)⁶/4⌉ "is added to the statement of (i)". HQ then decided ([pos 1639]; `MEET-v31/AMENDMENT_HQ_02.md`): configuration (ii) is "kept only as a sufficient rate inside the theorem (M1's simultaneous-control clause: "for any R′_n ≥ 4⌈(n + p)⁶/4⌉"), not as a runnable configuration of the method." **UNCERTAIN (U1):** the exact final wording of M1 clause (i) with the second rate is not printed anywhere in the snapshots.



---

## TH02 (M2 Theorem WS, the §5.3 package: (a) discrepancy; (b) bridge-form stability with Q5 content; (c) Proposition ONE-SHOT)

| Field | Value |
|---|---|
| Archive ID | **TH02** |
| Native name | M2 · Theorem WS, the §5.3 package: (a) discrepancy; (b) bridge-form stability with Q5 content; (c) Proposition ONE-SHOT |
| K-IDs (MINUTES §2.1) | K102, K10, K11, K25, K53; K103/K104 as used; K27 cited for the count |
| Authoring seat / final card source | Seat B (Fable 5.1) · `R3_B.md:151–187` (contains Seat C's D_* decomposition and actual-grid moment) |
| HQ charter | `branch_snapshots/MEET-THM/HQ_CHARTERS/M2.md` (wave 2, `MEET-THM/MINUTES.md` §2.5) |
| Binding goal / escalation | Binding: proposal §5.3 (HQ Q1 (a)(b)(c) with Q5's two conditions). Safeguard: "if both the D_* route and the correlated-family route fail, it escalates"; "Every fallback keeps (a), a stage-count clause and (c)". Charter escalation evidence: a counterexample to (a1) on the matrix domain and failure of the direct W-family proof; or a design in the domain with a successful coded grid violating (b5). |
| Who checked (Summary, from the card's own verdict/status rows and `MEET-THM/MINUTES.md` §1) | Inherited-proof check CHK_INHERITED (gpt-6.1-sol, cross-family, line by line): OWS-WS3 VERIFIED; OWS-WS4 VERIFIED; OWS-WS6(d) VERIFIED WITH AMENDMENT; OWS-WS7 VERIFIED WITH AMENDMENT — this meets HQ Q1(c) ("Q1(c) noted as met", Q5 ruling; [pos 1624]). W2PC2/W1PC2 (PC2 = Opus 5.5, cross-family to Astra's Seat C material): TRUE-AS-WRITTEN = statement sanity, not proof; W2PC1 (Sol on A/B/D assemblies): TRUE-AS-WRITTEN. Check wave 2 PC1 found COUNTEREXAMPLEs to the necessity propositions, the jump corollary etc. (removed/reworded: card row "Removed from my R2 card"). (a1) D_* route: PROOF SKETCH; (b7): "PROVED (by this seat, unchecked)"; pilot extension (b6′): PROOF SKETCH, unchecked. |
| Dependencies (Summary of the card's Dependencies row) | M3 TH03 (d_σ, WS3, FD-W1; T27(i) masking law); M7 TH07 (grid rule, Theorem G count, K25 coverage identity); M1 TH01 (E W_r = 1 for (b5)); S-KERNEL TH12 (N9 amendments); S-T TH09 (T03 concentration in (c1)); M6 TH06 (Lemma KL in (c2)); S-BLOCKS TH11 (blocks = groups on W); S-REP TH19 (η̂, ε̂_×, Ĵ report the constants). |
| Source positions | [pos 1608]/[pos 1614] (Q1 ruling), [pos 1621]/[pos 1624] (Q5 ruling), [pos 1626], [pos 1650]; user wording of the goal: [pos 1348] ("Proposal §5.3 … has no theorem in the draft list"), [pos 1441] (correction: O-WSTAB orthogonal idealisation) |
| Statement location | `MEET-THM/THEOREM_LIST_FINAL.md` lines 136–180 (verbatim block below, including the card's own Hypotheses/premises, Statement, Status and Dependencies rows) |

**Chair's integration note(s) and verbatim card:**

**Chair's integration note.** No change.
(B's leakage clauses (F), (S) are already outside this card; they are the supplement S-LEAK, R3-5. The §5.3 escalation safeguard of MINUTES §2.3 §2.7 matches the card's fallback row.)

<!-- BEGIN VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:140-180 -->
**Source:** `theory_campaign/MEET-THM/R3_B.md:151–187` (verbatim)

<!-- BEGIN VERBATIM R3_B.md:151-187 -->
### Card M2 · Theorem WS, the §5.3 package · K102, K10, K11, K25, K53; K103/K104 as used; K27 cited for the count; part (c) = Proposition ONE-SHOT (OWS-WS6(d), OWS-WS7)

| Field | Content |
|---|---|
| Setting (model/design; everything computed from (X, y) and the built blocks) | Standardised X, centred nonconstant y, n ≥ 3, p ≥ 1; shipped target (g = n, IG(a₀, b₀), capped BB(1,p), K = min(p, ⌊n/2⌋)); blocks C₁..C_J as built by the method from X; tables r_b from the same (X, y); Ω = {\|S\| ≤ K}; d = log BF − Σ_b log r_b; q_t ∝ γ₀e^{td}; G = XᵀX, G_D its block-diagonal part, E = G − G_D, A_D = G_D + I, H_D = (n+1)G_D + I, z = Xᵀy, Q̄ = 2b₀ + yᵀy, ν = a₀ + n/2 (C:50, 63). |
| H-DOM (matrix domain) | a := nzᵀH_D⁻¹z/Q̄ < 1; δ_A := ‖A_D^{−1/2}EA_D^{−1/2}‖ < 1; δ_H := ‖(n+1)H_D^{−1/2}EH_D^{−1/2}‖ < 1; r := δ_Ha/[(1−δ_H)(1−a)] < 1. C_σ := νa²/[2(1−a)]; b_X := (K/2)[−log(1−δ_A) − log(1−δ_H)] − ν log(1−r); D_* := C_σ + 2b_X; x_b, d_σ(S) := ν[Σ_b log(1−x_b) − log(1−Σ_b x_b)] (C:64–65). |
| Implementation premises (named, not model conditions) | EX-A exact arithmetic; EX-S/H-U exact start sampler and ideal uniforms (for (b3), (b5)); CAL: a successful calibration record 𝒞 frozen on streams 0–9; R′ = 4k declared before stream 10; kernels as coded under N9's sufficient conditions; for (b5)–(b6): ESS .9 for pilot and grid, 2⁻⁶⁰ bisection, 10⁻¹² snap/validation, a successful grid (no ceiling/snap failure), 2⁻⁶⁰ ≤ h/2. No output clause, so GUARD-W is not used. |
| (a1) Decomposition | Under H-DOM, for every S ∈ Ω: d(S) = d_σ(S) + d_X(S) with 0 ≤ d_σ(S) ≤ C_σ and \|d_X(S)\| ≤ b_X; hence osc_Ω d ≤ D_*. The σ²-coupling term C_σ survives E = 0. [W2PC2 C2(a)·split TRUE-AS-WRITTEN, 104 domain designs; W1PC2 D14·deterministic bound; W2PC1 B.R3(a) TRUE-AS-WRITTEN] |
| (a2) Divergences | Under H-DOM: KL(π‖π₀) ≤ D_*, KL(π₀‖π) ≤ D_*, J := KL(π‖π₀) + KL(π₀‖π) = E_π d − E_{π₀} d ≤ D_*; TV(π, π₀) ≤ tanh(osc d/2); 1 + χ²(π‖π₀) ≤ e^{osc d}. [W2PC2 C2(a)·divergences; W1PC1 §16 KL/TV rows TRUE-AS-WRITTEN] |
| (a3) Block-orthogonal case and per-model η-form | If E = 0: d = d_σ ≥ 0, zero iff at most one block has positive fit fraction; with known σ² (tables recomputed under known precision) d ≡ 0. For S with A_S ≻ 0 and ε_S < 1 − x̄_S: \|d_X(S)\| ≤ η_S := νε_Sx̄_S/(1−ε_S−x̄_S) + F_S/(4(1−ε_S)). [CHK §3 WS3 VERIFIED; FD-W1; W1PC1 §5 zero case; CHK §4 WS4 VERIFIED; W2PC1 D.R3(a)] |
| (b1) Per-stage χ² | Under H-DOM, for 0 ≤ u < u+Δ ≤ 1: χ²(q_{u+Δ}‖q_u) ≤ e^{ΔD_*} − 1. [W2PC2 C2(b)·increments TRUE-AS-WRITTEN; W1PC2 D14·one-shot/increment] |
| (b2) Four-normaliser transfer (same data, fixed partition) | With q^σ_t ∝ γ₀e^{td_σ}: e^{−4vb_X} ≤ [1+χ²(q_v‖q_u)]/[1+χ²(q^σ_v‖q^σ_u)] ≤ e^{4vb_X}, 0 ≤ u < v ≤ 1. On any nonempty W ⊆ Ω with η_W := max_W η_S: the same with e^{±4vη_W}, and TV(q_v^W, q_v^{σ,W}) ≤ 1 − e^{−2vη_W}. [W2PC2 C2(b)·continuity; W2PC1 B.R3(b)(1)–(4); CHK §4 WS4(e)] |
| (b3) First stage | Particles iid π₀: 1 + N_e·Var(Ẑ_{stage 1}/(Z̄_{φ₁}/Z̄₀)) = 1 + χ²(q_{φ₁}‖π₀) exactly, and this quantity is within e^{±4φ₁η} of its block-orthogonal value. Transfer of 1 + N_e Var, never of Var. [W2PC1 B.R3(b)(1)–(4); A.R3(b)(i),(ii),(v); W2PC2 C2·variance transfer] |
| (b4) Doeblin constants | M_φ := max_S q_φ(S)/π₀(S) ≤ e^{2φη}M^σ_φ, so the coded round minorises q_φ with constant ≥ e^{−2φη}/M^σ_φ. [W2PC1 B.R3(b)(1)–(4); D.R3(b)(i),(ii),(iv)] |
| (b5) Pathwise island moment | On every successful coded grid, with the kernels as coded: W_r := Ẑ_r/Z ∈ [e^{−osc d}, e^{osc d}] ⊆ [e^{−D_*}, e^{D_*}] pathwise and E[W_r \| 𝒞] = 1, hence M₂ := E[W_r² \| 𝒞] ≤ e^{D_*}. An upper bound only; no comparison to the block-orthogonal M₂. [W2PC2 C2(b)·weights; W1PC2 D14·actual-grid moment (1,600 islands, poor V included); W2PC1 B.R3(b)(5),(6); SYNTH §3 A.R3(b)(iv)] |
| (b6) Stage count: the sandwich | For exact-frontier greedy ESS-.9 grids on a fixed common nonempty V with common pilot targets, same-data block-diagonal baseline d_σ on the fixed partition, and .9e^{4η} < 1: T_bd(.9e^{−4η}) ≤ T ≤ T_bd(.9e^{4η}); for the coded grid add the 2⁻⁶⁰ bisection and 10⁻¹² snap/validation qualifications. [W2PC1 B.R3(b)(1)–(4); A.R3(b)(iii)·sandwich; D.R3(b)(iii)·sandwich; E-pilot 16 cases, 0 violations] |
| (b6′) Local constancy, integer bound, envelope | If the baseline is not at a critical threshold, T = T_bd(.9) for all small ε. Under the pilot premises (global range bound D_*, 2⁻⁶⁰ ≤ h/2, h = 2c_ρ/D_*, c_ρ = √log(10/9)): P ≤ ⌈2/h⌉ + 1 and T ≤ 2⌈D_*/c_ρ⌉ + 2 ≤ 4 + 2D_*/c_ρ, a continuous envelope; D_* = 0 ⇒ T = 1. Checked fallback: T ≤ P + ⌈D_*/c_ρ⌉ + 1. [W2PC1 B.R3(b) continuity verdict (local constancy); W2PC2 C2(b)·stage count, C8·pilot extension, 600 adversarial runs] |
| (b7) Q5 condition (1): continuity and Lipschitz statements in ε | On the fixed-partition, same-data family E = εE₁ (E₁ a fixed cross-block pattern): δ_A(ε) = εδ_A(1) =: c_Aε and δ_H(ε) = c_Hε exactly. Hence on [0, ε₁] with c_Aε₁, c_Hε₁ < 1 and r(ε₁) < 1, the functions b_X(ε), D_*(ε), e^{±4vb_X(ε)}, e^{ΔD_*(ε)} − 1, e^{D_*(ε)} and the Doeblin factor are continuous with b_X(0) = 0 and Lipschitz with constant L(ε₁) := (K/2)[c_A/(1−c_Aε₁) + c_H/(1−c_Hε₁)] + νc_Ha/[(1−a)(1−c_Hε₁)²(1−r(ε₁))] (for b_X; e^{·} factors by the chain rule). Per-stage χ²: \|log(1+χ²(q_v‖q_u))(ε) − (·)(ε′)\| ≤ 4v·sup_S\|d(S;ε) − d(S;ε′)\| ≤ 4v[b_X(ε) + b_X(ε′)], so at the baseline the modulus is 4vLε. Status: PROVED (by this seat, unchecked), elementary calculus on the checked formulas; local check above, 0 violations. |
| (b8) Q5 condition (2), verbatim in the theorem | "T(ε) is a step function of ε. It can jump at critical thresholds: PC1 exhibits an actual design (n = 40, p = 2, B = 1) with one-sided baseline counts {2, 4} and T = 3 at ε = 10⁻⁵. 'Stable stage count' means the sandwich (b6), and nothing more." [W2PC1 D.R3(b)(iii)·jump corollary; E-jump] |
| (c1) Zero-dependence obstruction (WS6(d) with CHK amendment) | Under G (Gaussian noise, fixed σ² > 0), ORTH (XᵀX = (n−1)I, p ≤ n−1), fixed nonempty S₀ with fixed nonzero coefficients, the shipped score/prior/state space, partition fixed in X, truth-free null count m → ∞ with log m = O(log n), m ≥ p/2 and p^{(α−1)R̄²}/[√n(log p)^{(1+(α−1)R̄²)/2}] → ∞: D_α(π‖π₀) → ∞ in probability; for α = 2, χ²(π‖π₀) → ∞ and ESS_∞ → 0, while in the bounded-block setting (shipped B ≤ 16) or assuming π₀(S₀) → 1, TV(π, π₀) → 0. Instance: p = n−1, one coefficient 2, σ² = 1. [CHK §1, §6 VERIFIED WITH AMENDMENT; W2PC1 B.R3(c)] |
| (c2) Masked obstruction (WS7 with CHK amendments) | If π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (T27(i)'s conclusion; H3 and the joint-ratio law are non-design premises, instantiated on LH) and π(S₀) → 1: ESS_∞ ≤ π₀(S₀)/π(S₀)² → 0, KL(π‖π₀) ≥ π(S₀)log(1/π₀(S₀)) − log 2 → ∞, TV → 1; the initial population holds S₀ with probability 1 − (1−π₀(S₀))^N ≤ Nπ₀(S₀), later stages only "≤"; restricted-grid lower bounds with the set-mass (log π₀(V) = o_P(c log p + (c/2)log n)) and singleton-endpoint amendments. Neither (c1) nor (c2) refutes the multistage sampler or (b). [CHK §2, §6; W2PC1 B.R3(c)] |
| Scale disclosure (not a theorem) | Useful (O(1)) constants need signal energy O(√n) (νa² = O(1)) and ε ≲ n^{−1/2}/p on the exhibited family; at fixed ε, D_* grows (534 → 6.45·10⁴ on W at ε = .01) and the domain fails. η-form constants are O(1) iff ε = O(1/(nx̄)). A sharp necessity statement is FUTURE_WORK (all three seat forms COUNTEREXAMPLE; C's is a range obstruction only). [W2PC2 C2·ε-scale; W2PC1 B.R3·scale; CHK §4 scale remark] |
| Removed from my R2 card | Prop NEC (W2PC1 B.R3 NEC COUNTEREXAMPLE); "every constant in (b1)–(b5), including T, tends to its BO value" (replaced by (b6′), (b8)); the q₂ tilt-tail route (W1PC1 IMPLAUSIBLE); the m-form of (S) and (F) (to the leakage corollary, R3-5). |
| Guarantee (one sentence) | On the method's own partition, the gap between the block-product start and the posterior, and every bridge quantity (per-stage χ², island weight moments, Doeblin constants, and the stage count through its sandwich and envelope), is controlled by two data-computable terms, the σ²-coupling term and the cross-block term, continuously in the cross-block correlation; and the one-shot importance-weight reading of §5.3 is false even at zero correlation. |
| Objective / goal / Song–Liang | Objective (1); objective (2) through (b5) (island count via M₂ ≤ e^{D_*}) and (b6′) (depth envelope); proposal §5.3 (binding; HQ Q1 (a)(b)(c), Q5); Song–Liang Thm 4/Cor 2 as "specific start-distortion analysis, compared not exceeded" (d_σ quantifies the block-start distortion). |
| Status (verbatim, with qualifiers) | OWS-WS3, OWS-WS4: PROVED (SF: none; XF: none) + CHK "VERIFIED (PC1, cross-family, line by line)". OWS-WS6d, OWS-WS7: PROVED (SF: none; XF: none) + CHK "VERIFIED WITH AMENDMENT". OWS-WS1: PROVED, AUTHOR-ONLY. FD-W1: PROVED, XF VERIFIED (A-REV4). AREV9-OWSTAB: "VERIFIED under H-ORTH exactly as stated" (not used beyond H-ORTH). Seat C's D_* decomposition and actual-grid moment: PROOF SKETCH (NEW-COMP); W1PC2/W2PC2 TRUE-AS-WRITTEN (statement sanity, not a proof). (b2)–(b4), (b6) assemblies: PROVED (by Seats A/B/D, unchecked), W2PC1 TRUE-AS-WRITTEN. C8 pilot extension: PROOF SKETCH, unchecked (W2PC2 PLAUSIBLE); T26BUD-G: PROVED, deterministic, AUTHOR-ONLY. (b7): PROVED (by this seat, unchecked). T03: PROVED-LOCKED; T27(i): PROVED-LOCKED, CONDITIONAL. OWS-WS6e: CONJECTURE; OWS-WS8d: OPEN (neither used). |
| Fidelity to v3.1 as shipped | Partition: the method's own (verified computed on W). Kernels: as coded (b5). Grid: coded rule for (b5), (b6′); (b6)'s exact-frontier comparison is a labelled comparison object. (c) concerns the start/target laws, not the sampler. LS0 n/a; pooling n/a; stacking n/a. |
| Self-checked flag | Mixed: WS3/4/6d/7 cross-family checked (CHK); C's D_* route PC2-checked (cross-family to C) but no filed proof; (b7) seat-only; A/B/D's (b) assemblies statement-checked by PC1 only. |
| Novelty, citations checked | NEW-COMP. Nearest predecessor OWS-WS4 (internal; PC2 novelty note). Generic χ² precedent: Frazier et al. 2023, Assumption 6(iv) (via THM-INV §4b; not re-fetched by me, to the citation checker). Cérou–Del Moral–Guyader 2011 Thms 1.4–1.5 (variance theorems; not re-sold). Chatterjee–Diaconis 2018 Thms 1.1–1.3 (exp(KL) scale behind (c2)). Štefankovič–Vempala–Vigoda 2009 (greedy-schedule optimality behind (b6); LIT-SMC #9). Gelman–Meng 1998 (J identity). YWJ/ZYVR not touched. |
| Proof route and key lemma | (a1)–(a2): PC2 Appendix A's four steps (exact split; d_D ∈ [0, νx²/(2(1−x))]; eigenvalues of I + M in [1−δ, 1+δ]; resolvent bound \|t − t_D\| ≤ δ_Ht_D/(1−δ_H)). **Key lemma:** restriction monotonicity of zᵀH⁻¹z and of relative operator norms. (b2): WS1(a) cumulant identity and \|log Z_t − log Z^σ_t\| ≤ \|t\|b_X. (b5): product of stage averages in [e^{Δ_t d_min}, e^{Δ_t d_max}], ΣΔ_t = 1, E W = 1 (T12/N9). (b6): feasibility inclusion plus constrained greedy optimality (Theorem G). (b6′): empirical ESS monotone in Δ (convex log-MGF), Popoviciu, bisection invariant. (b7): homogeneity and chain rule. |
| Difficulty | (a) M; (b1)–(b5), (b7) S; (b6)–(b6′) M (the pilot interface); (c) done (cited). |
| Lean core | Finite-space: WS1(a) cumulant identity; the four-normaliser bound given sup\|d − d′\| ≤ η; the product-of-averages pathwise bound; the scalar log inequalities defining b_X and the Lipschitz algebra of (b7). Not Lean: (c) and the probability-in-the-design clauses. |
| Dependencies (card IDs) | M3 (d_σ, WS3, FD-W1; T27(i) masking law for (c2)); M7 (grid rule, Theorem G count, K25 coverage identity for V ≠ Ω); M1 (T12/N9 E W_r = 1 for (b5)); S-KERNEL (N9 amendments); S-T (T03 concentration in (c1)); M6 (Lemma KL in (c2)); S-BLOCKS (blocks = groups on W); S-REP (η̂, ε̂_×, Ĵ report the constants). |
| Risk | D_* route is a PROOF SKETCH: if the general matrix route stalls, prove on W directly (C's fallback). The useful scale is perturbative (ε ≲ n^{−1/2}/p): disclosed. Pilot-extension envelope unchecked as a proof: the checked fallback count stands. CAL/EX-S premises. |
| Fallback statement and stop rule | If (a1) (D_*) fails: ship (a3) η-form (VERIFIED) with (b2)–(b4) in η_W form, (b5) with osc d, (b6) sandwich, (c); the scale shrinks to ε = O(1/(nx̄)). If (b6′) fails: ship (b1)–(b6) plus the checked count T ≤ P + ⌈D_*/c_ρ⌉ + 1 and (b8). Every fallback keeps (a), a stage-count clause and (c) (PC1: omitting the count would not meet Q1(b)). If both the D_* route and the direct W-family route fail: escalate to HQ as unmet binding §5.3; never dropped (§2.7). Stop: one check wave per half; one HQ cycle for the pilot-extension lemma. |
| IC3 design, exhibited, where checked | **W** (SMC-dispatched): p = 9⌊n^{1/3}/9⌋, groups of 9 at ¼, every cross correlation ε_n = 1/(np) > 0, two n^{−1/4} signals in two groups, σ² = 1, n ≥ 9⁶; own partition computed, blocks = groups for n ∈ {9⁶, 10⁶, 2·10⁷, 10⁸}, H-DOM 10/10 seeds per n, D_* median 1.08 → 1.04, b_X ≈ 5·10⁻⁴ to 3·10⁻⁵ (W2PC2 §0 item 3, `w_family.py`). **W at ε = n^{−1/2}/p**: b_X ≈ 0.35, D_* ≈ 1.73–1.90, blocks = groups, domain 10/10 (W2PC2 §0 item 3). Component checks (exact branch dispatches): Dε, n = 40, p = 8, B = 2 (W1PC1 "Dε"; my R2 check 1, 40/40; W2PC1 B.R3·scale); A's n = 64, p = 16, B = 4. (c1): CHK §6 example XᵀX = (n−1)I, p = n−1, coefficient 2. (c2): LH (W1PC2 shared LH). |
| Numerical companion (≤ 20 seeds) | Existing: W2PC2 `r3_clauses.py` (104 domain designs, 0 violations), `w_family.py` (10 seeds per n), `c8_pilot.py`, W1PC2 `smc_coded.py` (1,600 islands), W2PC1 E-pilot (16 cases), my R2 check 1 (10 seeds × 4 ε), today's Lipschitz check (5 seeds, 75 pairs). For the HQ: ≤ 20 seeds on W at n = 9⁶, reporting (a, δ_A, δ_H, r, b_X, D_*), the sandwich at ε ∈ {1/(np), n^{−1/2}/p}, M₂ on four coded islands, and L(ε₁) against the observed b_X increments. |
<!-- END VERBATIM -->
<!-- END VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:140-180 -->


---

## TH03 (M3 Theorem START)

| Field | Value |
|---|---|
| Archive ID | **TH03** |
| Native name | M3 · Theorem START |
| K-IDs (MINUTES §2.1) | K15, K17, K18, K10 (K16 supplementary conditional lemma) |
| Authoring seat / final card source | Seat C (gpt-6-astra) · `R3_C.md:144–177` |
| HQ charter | `branch_snapshots/MEET-THM/HQ_CHARTERS/M3.md` (wave 1, `MEET-THM/MINUTES.md` §2.5) |
| Binding goal / escalation | No binding goal rests on M3 alone. Charter escalation evidence: "A failed LH premise affecting M5/M6 or the retained masked requirement; any failure leaving Q1(c) without its independently checked obstruction." |
| Who checked (Summary, from the card's own verdict/status rows and `MEET-THM/MINUTES.md` §1) | PC2 (Opus 5.5) checks of Seat C material (W1P2/W2P2 rows cited in the card: cluster 5, C5/C11); ingredient statuses are in the card (T22(i)(ii)(iv) PROVED-LOCKED; DIL-E XF VERIFIED (A-REV9); Thm3/4-EXP SF VERIFIED (W3-VEXP) XF VERIFIED (A-REV2); Thm5-LH SF VERIFIED (W3-VEXP), XF none, SAME-FAMILY-ONLY; OWS-WS3 CHK "VERIFIED (PC1, cross-family, line by line)"); final assembly "PROOF SKETCH, unchecked". |
| Dependencies (Summary of the card's Dependencies row) | S-TARGET TH10; S-BLOCKS TH11; S-T TH09 for π(S₀)→1. M2 perturbation clause is a cross-reference. Feeds M2(a) TH02, M5 TH05 (start centre), M6 TH06 (π₀(S₀) law), M7(d) TH07 (A₀), S-Z TH16, S-LEAK TH20, S-REP TH19. |
| Source positions | [pos 1348] ("Start laws"), [pos 1626], [pos 1650] |
| Statement location | `MEET-THM/THEOREM_LIST_FINAL.md` lines 187–227 (verbatim block below, including the card's own Hypotheses/premises, Statement, Status and Dependencies rows) |

**Chair's integration note(s) and verbatim card:**

**Chair's integration note.** No change. (K16 stays a supplementary conditional lemma, as the card states.)

<!-- BEGIN VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:190-227 -->
**Source:** `theory_campaign/MEET-THM/R3_C.md:144–177` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:144-177 -->
### M3 — START

| Card field | Final content |
|---|---|
| IDs | **M3: K15, K17, K18, K10**; K16 is an attributed supplementary conditional lemma. |
| Hypotheses | D0 and EX-A. Deterministic clauses allow any fixed partition with \(|C_b|\le K\) and the stated positive tables. Score-coupling clauses require production tables. The masked clause additionally uses G on the exhibited LH family. |
| Implementation premises | Tables, size cap and prior are those specified above. No calibration, random-number, LS0, pooling or delivery premise is needed for the mathematical start-law claims. Actual execution fidelity remains distinct from these identities. |
| AGG definitions I | For feasible reference \(S^\circ\), \(s=|S^\circ|\), \(U_b^*=S^\circ\cap C_b\), define \(a_{bj}=\sum_{U\supseteq U_b^*,\,|U\setminus U_b^*|=j}r_b(U)/r_b(U_b^*)\), \(D_b=\max_{j\ge1}(j!a_{bj})^{1/j}\), empty maximum zero. |
| AGG definitions II | Set \(q=(p-s)^{-1}\sum_bD_b\) for \(s<p\), otherwise zero. Set \(e=2p\max_{b,U:\,a=|U_b^*\setminus U|>0}[r_b(U)/r_b(U\cup U_b^*)]^{1/a}\), empty maximum zero. |
| M3(a): deterministic mass | If \(q<1\), \(\pi_0(S^\circ)\ge(1-q)^{s+1}/(1+e)^s\). For feasible \(S_0\), \(\pi_0(S_0)/\pi_0(S^\circ)=[w(|S_0|)/w(s)]\prod_b r_b(S_{0b})/r_b(U_b^*)\). **Evidence:** W1P1 §5, A.C8(a–e)/B.D4/D.M6; source T22(i),(ii). |
| M3(b): bridge mass | For feasible \(S_0\), \(\inf_{0\le t\le1}q_t(S_0)\ge\min\{\pi_0(S_0),\pi(S_0)\}\). This is a finite-law mass bound, not a particle-discovery assertion. **Evidence:** same W1P1 §5 row; T22(iv). |
| M3(c): exact factorization | \(B_b=\sum_{U\subseteq C_b}r_b(U)\), \(q_b(U)=r_b(U)/B_b\), \(A(k)=\varpi(k)\prod_bB_b/\bar Z_0\). Then \(\pi_0(S)=A(|S|)\prod_bq_b(S_b)\). **Evidence:** W1P2 cluster 5, “D2 · exact factorisation”; W2P2 §2, C5. |
| Dilution definitions | For nonempty \(S_{0b}\), let \(\lambda_b=\log r_b(S_{0b})\), \(\eta_b=[B_b-1-r_b(S_{0b})]/[1+r_b(S_{0b})]\). For empty \(S_{0b}\), let \(\eta_b=B_b-1\). Production tables have \(r_b(\varnothing)=1\), so \(\eta_b\ge0\). |
| M3(d): dilution | \(V=\sum_{b:S_{0b}\ne\varnothing}\log(1+e^{-\lambda_b})\), \(C=\sum_b\log(1+\eta_b)\). Then \(-\log\pi_0(S_0)=V+C-\log A(|S_0|)\). **Evidence:** W1P1 §5, dilution clause; DIL-E/E1, here at tilt \(t=1\). No sign claim for \(-\log A\). |
| Coupling definitions | Let \(\bar Q=.02+y^\top y\), \(x_b=nz_{S_b}^\top H_{S_b}^{-1}z_{S_b}/\bar Q\), \(x=\sum_bx_b\). Define \(d_\sigma(S)=\nu[\sum_b\log(1-x_b)-\log(1-x)]\) when \(x<1\), and \(d_X=d-d_\sigma\). |
| M3(e): shared variance | Under block orthogonality, \(x<1\), \(d_X=0\), and \(0\le d_\sigma\le\nu\sum_{b<c}x_bx_c/(1-x)\). Equality \(d_\sigma=0\) holds exactly when at most one block has positive fit fraction. **Evidence:** CHK §3, WS3(b),(c); W2P1 D.M6. |
| Correlated extension interface | On M2’s matrix domain, the same split satisfies \(0\le d_\sigma\le C_\sigma\), \(|d_X|\le b_X\). The quantitative perturbation theorem belongs to M2. **Evidence:** W2P2 §1, “C2(a) · split”. |
| M3(f): masked law | Under G on LH, \(\log\pi_0(S_0)+2\log p+\log n=O_P(1)\), whereas \(\pi(S_0)\to1\). **Evidence:** W1P2 cluster 5, “D2 · LH masking law”; W2P2 §2, C5. Posterior concentration uses S-T. |
| Conditional-law safeguards | T27(i) retains a fixed feasible completion chain, jointly two-sided tight successive log-table ratios and a normalized reference-mass lower bound. LH supplies the application; cancellation alone does not discharge these premises on another design. |
| K16 placement | Cite T22(iii), **PROVED-LOCKED CONDITIONAL**, with G, R, within-block SE, EXP′, VIS, NL\(_\eta\), NL\(_{\rm avg}(\kappa)\) retained. Its favourable rate is a separate regime. It is not an additional unconditional assertion in M3. |
| Guarantee | The shipped start has an exact mass decomposition and can assign vanishing mass to truth on a correlated family whose full posterior concentrates on truth. |
| Goals | Objectives (1), (3); proposal §5.3 discrepancy and §5.4 start approximation; Song–Liang Thm 4 comparison only, plus statistical context for Thm S. No identification of \(\pi_0\) with Song–Liang’s final output. |
| Status: deterministic | T22(i)(ii)(iv): **PROVED-LOCKED**. DIL-E: **PROVED; SF: none; XF: VERIFIED (A-REV9)**. DIL-E1: **PROVED; SF: none; XF: VERIFIED* (A-REV9)**. |
| Status: statistical | T27(i): **PROVED-LOCKED, CONDITIONAL**. Thm3/4-EXP: **PROVED; SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)**. Thm5-LH: **PROVED; SF: VERIFIED (W3-VEXP); XF: none; SAME-FAMILY-ONLY**. |
| Status: coupling/assembly | OWS-WS3: **PROVED; SF: none; XF: none; AUTHOR-ONLY** in the inherited ledger; CHK separately records **VERIFIED (PC1, cross-family, line by line)**. Final assembly: **PROOF SKETCH, unchecked**. |
| Fidelity/self-check flag | Actual v3.1 target, tables, cap and partition. No altered start or known-variance substitution. Not self-check-only at the ingredient level; Thm5-LH’s qualification and the absence of a full assembly proof check remain explicit. |
| Novelty/citation | **NEW-COMP**, centered on this start’s masking and shared-variance distortion. Block computation is established precedent: [Papaspiliopoulos–Rossell (2017), §§3.1–3.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC5975653/). DIL-E/E1 and OWS-WS3 are the internal predecessors. |
| Proof route/key lemma | Import T22 and DIL identities; match production normalization. For LH, verify actual partition equality, then import the joint ratio/reference-mass application of Thm5-LH and S-T. Shared-variance algebra is CHK WS3. |
| Difficulty/Lean core | Moderate assembly; substantial qualification audit. Lean: finite products, prior ratios, logarithmic dilution identity, endpoint Hölder inequality and scalar shared-variance bounds. Gaussian asymptotics remain cited prose. |
| Dependencies | S-TARGET; S-BLOCKS; S-T for \(\pi(S_0)\to1\). The M2 perturbation clause is a cross-reference, not a prerequisite for the BO or LH clauses. |
| Risk | Losing normalized reference mass; treating the capped start as independent blocks; confusing sample and population cancellation; exporting exact-Gram results to adaptive random packing. |
| Fallback/stop rule | Retain deterministic mass, factorization, dilution and BO coupling if the LH application fails its full check. After one proof-and-repair cycle, move the failed statistical extension to FUTURE_WORK. Notify M5/M6 and HQ of any resulting loss of required masked accuracy or Q1(c) coverage. |
| IC3 exhibit/check | LH above supplies genuine cross-block correlation and the masked conclusion; W1P2 shared-family/cluster-5 rows and W2P2 C5/C11 verify the stated scope. BO components allow correlated columns within blocks; CHK §3 checks them. |
| Numerical companion | None newly run. Proposed companion: at most ten Gaussian seeds; compute exact start mass by block convolution on LH and compare its log scaling. Use small enumerable component cases for factorization; label forced/component dispatch explicitly. |
<!-- END VERBATIM -->
<!-- END VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:190-227 -->


---

## TH04 (M4 Theorem Z𝒯 and the certificate card, with the masked-regime statement (HQ Q3))

| Field | Value |
|---|---|
| Archive ID | **TH04** |
| Native name | M4 · Theorem Z𝒯 and the certificate card, with the masked-regime statement (HQ Q3) |
| K-IDs (MINUTES §2.1) | K42, K43, K45, K44; K36, K78 (output-event clauses); K95 cited from S-TARGET |
| Authoring seat / final card source | Seat B (Fable 5.1) · `R3_B.md:189–216` (Seat D's lettering "M4(e)" = final (f)) |
| HQ charter | `branch_snapshots/MEET-THM/HQ_CHARTERS/M4.md` (wave 3, `MEET-THM/MINUTES.md` §2.5) |
| Binding goal / escalation | Binding: proposal §5.4 masked-regime accuracy (HQ Q3 requires "at least one masked-regime accuracy statement that paper 1 actually proves"; the statement is clause (f)). Safeguard: "loss of the masked statement without an approved replacement escalates (C §S5)". M4(f) needs M5 TH05. |
| Who checked (Summary, from the card's own verdict/status rows and `MEET-THM/MINUTES.md` §1) | W1PC1 §3 / W2PC1 B.M5, B.R4 (Sol): TRUE-AS-WRITTEN (statement sanity); W2PC2 §3 (Opus 5.5) assembly TRUE-AS-WRITTEN; N13, N17: PC1/PC2 checked; MZ-P3 AUTHOR-ONLY; GUARD-W un-audited; (f): PROOF SKETCH (seat-assembled); T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)); Thm5-LH SAME-FAMILY-ONLY. |
| Dependencies (Summary of the card's Dependencies row) | M5 TH05 (b1-LH) for (f); S-T TH09 (T03♯, Thm5-LH) for π(S₀)→1; S-OUT TH15 (Lemma RO, GUARD-W) for (e); S-TARGET TH10 (N17) for (d); S-CERT TH14 (G2/L/R item semantics); M1 TH01 (T12 E[Ẑ_r|𝒞] = Z); S-BLOCKS TH11 (SIZE on LH). |
| Source positions | [pos 1608]/[pos 1614] (Q3 ruling), [pos 1626], [pos 1650] |
| Statement location | `MEET-THM/THEOREM_LIST_FINAL.md` lines 235–271 (verbatim block below, including the card's own Hypotheses/premises, Statement, Status and Dependencies rows) |

**Chair's integration note(s) and verbatim card:**

1. K95 (the odds certificate, η < 1) lives in S-TARGET (R3-4, unanimous); M4 cites it. No clause of this card changes.
2. The masked statement is clause (f) of this card (Seat D's lettering "M4(e)" in R3_D is the same statement). Per MINUTES §2.3 §2.7 and R3_C §S5, loss of the masked statement without an approved replacement **escalates**; the card's fallback row says HQ "is told … (never silently)", which is to be read as an escalation.
3. N2(e) GUARD-W, the LS0 retention rule/OP-LS0 integration and the N3 DP invariant are named implementation premises of this card (MINUTES §2.3, "Audit obligations").


<!-- BEGIN VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:240-271 -->
**Source:** `theory_campaign/MEET-THM/R3_B.md:189–216` (verbatim)

<!-- BEGIN VERBATIM R3_B.md:189-216 -->
### Card M4 · Theorem Z𝒯 and the certificate card, with the masked-regime statement · K42, K43, K45, K44; K36, K78 (output-event clauses); K95 cited from S-TARGET

| Field | Content |
|---|---|
| Setting (model/design) | Finite Ω, shipped target π(S) = ϖ(S)m(S)/Z; 𝒯 ⊆ Ω the nonempty deduplicated reported store, Z_𝒯 := Σ_𝒯 ϖm, π_𝒯 := π(·\|𝒯); δ₁ := 1 − π(S₀); h: Ω → [0, 1] (or bounded, scaled by ‖h‖_∞); 𝒮 the set of scored models; 𝒯_new = top_c(𝒯_old ∪ 𝒮_added), c ≥ 1 (the LS0 union-then-top-c rule, METHOD #9). For (f): the LH family (W1PC2 shared LH): p = 9⌊n^{1/3}/9⌋, groups of 9 at .4, two disjoint hub links .2, coefficients (1, −.2), σ² = 1, exact Gram, n ≥ 9⁶, SIZE 9 ≤ B ≤ 16 < 18; G; T03♯'s hypotheses hold on LH (Thm5-LH, SAME-FAMILY-ONLY). |
| Implementation premises (named) | EX-A (exact arithmetic; the card is "numerical" until SC + VAL-FP, N16); SR (all scored candidates enter the winner comparison; union-then-top-c storage); Lemma S and the inheritance merge (PC2 code facts); for (e): Lemma RO + GUARD-W (stop-only coupling, audit N2(e) open), CAL, EX-S, Ẑ = Z on the exact branch, E[Ẑ_r \| 𝒞] = Z; for (f): OP-LS0 (completed scans), the e4 centre rule (tie-aware DP invariant N3 OPEN, carried as hypothesis), ℓ ≥ max{Φ(S°) − 1, 0} (= 1 on LH; shipped ℓ suffices). |
| (a) Deterministic identities | Z_𝒯 ≤ Z; π(S) ≤ ϖ(S)m(S)/Z_𝒯 for every S; TV(π_𝒯, π) = 1 − Z_𝒯/Z; KL(π_𝒯‖π) = log(Z/Z_𝒯); KL(π‖π_𝒯) = ∞ iff π(𝒯ᶜ) > 0; Ẑ < Z_𝒯 ⇒ Ẑ < Z. [W1PC1 §3 A.C7/B.D3(a–d) TRUE-AS-WRITTEN; W1PC1 §16 reverse KL repaired with π(𝒯ᶜ) > 0; W1PC2 D5·TV certificate, D5·underestimation; W2PC1 A.M5, B.M5] |
| (b) Brackets when the truth is stored | If S₀ ∈ 𝒯: 1 − δ₁ ≤ Z_𝒯/Z ≤ 1; TV(π_𝒯, π) ≤ δ₁; \|PIP^𝒯_j − PIP_j\| ≤ δ₁ for all j; \|π_𝒯(h) − π(h)\| ≤ 2δ₁‖h‖_∞; joint inclusions likewise. [W1PC1 §3 B.D3(b) COUNTEREXAMPLE repaired with ‖h‖_∞; W2PC1 B.M5 TRUE-AS-WRITTEN] |
| (c) Retention (N13) | If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 and MPM^𝒯 = S₀; ½ is sharp; holds under LS0 with 𝒯_new = top_c(𝒯_old ∪ 𝒮_added). Unqualified retention is false. [N13 PROVED (PC1 claim 5); W1PC1 §3; W2PC2 C4·retention TRUE-AS-WRITTEN; W2PC1 B.M5] |
| (d) Analytic envelope (N17) | m(S) ≤ U_m := C_n(2b₀ + yᵀy/(n+1))^{−ν} for every S; hence Z ≤ U := Z_𝒯 + U_m[1 − Σ_𝒯 ϖ] and TV(π_𝒯, π) ≤ 1 − Z_𝒯/U, a computable bound (loose, reported as such). [N17 PROVED (PC1 claim 1; PC2 C1(c)); W1PC2 D5·envelope, 40 designs × 5 stores; W2PC1 A.M5] |
| (e) Output-event certificate | Under Lemma RO + GUARD-W: P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05; island-minimum bound 0.05^{1/R′}min_r Ẑ_r at the same level; card level P(𝒪 ∩ {some G2/L/R item false}) ≤ 0.05. Never conditional on completion: P(B \| 𝒪, 𝒞) ≤ α does not follow (CEX-guard). [W1PC1 §3 A.C3(a,b,c)/B.D3(e) TRUE-AS-WRITTEN; W1PC2 D5·LCB, D12; W2PC1 B.M5] |
| (f) Masked-regime statement (HQ Q3) | On LH under M5's hypotheses (b1-LH): for every ε > 0, P(𝒪 ∩ {TV(π_𝒯, π) > ε}) → 0; P(𝒪 ∩ {max_j\|PIP^𝒯_j − PIP_j\| > 1 − π(S₀)}) ≤ P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) + P(π(S₀) ≤ ½) → 0; P(𝒪 ∩ {MPM^𝒯 ≠ S₀}) → 0; and surely Ẑ < Z_𝒯 ⇒ Ẑ < Z. Reading: vanishing P(output and error); not conditional success, and not P(𝒪) → 1. Non-vacuous on a masked family: π₀(S₀) = p^{−2}n^{−1}e^{O_P(1)} → 0 while π(S₀) → 1. [W2PC1 B.R4·Z𝒯/CARD TRUE-AS-WRITTEN; D.R4; W2PC2 §3 §R4 named guarantee TRUE-AS-WRITTEN (assembly)] |
| (g) Definitional facts | For a proper store (π(𝒯ᶜ) > 0), KL(π‖π_𝒯) = ∞; any positive-mass state absent from the records makes KL(π‖π̂) = ∞, surely when \|Ω\| > 4N_eR′. The masked final-estimate TV/KL bound is FW2. [W1PC1 §16; W2PC2 C15-KL] |
| Removed from my R2 card | The M₂ aside "masking forces the actual M₂ to diverge" (W2PC1 B.R4 NEEDS-HYPOTHESIS). |
| Guarantee (one sentence) | The run's own stored record gives deterministic two-sided brackets on the evidence and on every reported probability whenever the truth was scored, a 95% certificate jointly with output, and, on a masked family where the start misses the truth polynomially, the reported restricted posterior is still within δ₁ of the exact one jointly with output. |
| Objective / goal / Song–Liang | Objective (1); proposal §5.4 (PIP/joint-PIP error, deterministic TV, HQ Q3's required masked statement); §4.4/§8.2 diagnostics (what the certificate proves); Song–Liang Thm 3 (estimated PIPs via the restricted store) and Thm S (reported MPM/HPM on LH, additional to the exact-posterior counterpart). |
| Status (verbatim) | MZ-P3: "PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery"; "candidate: not reviewed, not adopted"; AUTHOR-ONLY. N13: PROVED (PC1 claim 5). PC1c5: (a) PROVED, ½ sharp. N17: PROVED (PC1 claim 1; PC2 C1(c)). PC1c2: PROVED for the potential run; N6(a) output form CORRECT WITH AMENDMENT; N6(b) PROVED modulo premise (i) (GUARD-W not audited). LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)). CEX-guard: COUNTEREXAMPLE (XF VERIFIED*). OCERT-C1: XF ERROR as quantified (O-VCERT R1 wording used). T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)). Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none), SAME-FAMILY-ONLY. T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)). (f) assembly: PROOF SKETCH (seat-assembled; W2PC1/W2PC2 TRUE-AS-WRITTEN as an assembly). |
| Fidelity to v3.1 as shipped | LS0: yes (the union-then-top-c rule); coded grid: yes (no grid hypothesis); pooling: n/a; exact arithmetic premise, numerical label until N16; (f) uses v3.1 with LS0 as shipped, integration audit open. |
| Self-checked flag | MZ-P3 AUTHOR-ONLY; (f) seat-assembled; GUARD-W un-audited; N13, N17 PC1/PC2 checked. |
| Novelty, citations checked | NEW in kind (certificates on reported quantities), elementary; Markov lower bound KNOWN—CITE (Grosse–Ghahramani–Adams 2015); the restricted-measure TV identity is elementary (no citation claimed). (f) NEW-COMP (composition with T38-b1-LH), worded "for the paper's own target and start"; Hou–Wang–Atchadé arXiv:2407.20580: never "first finite-n"; YWJ 2016 / ZYVR 2022 cited next to M5. |
| Proof route and key lemma | Finite sums and π_𝒯 = π/π(𝒯) for (a), (b), (d); Lemma S plus the inheritance merge for (c); Markov + Lemma RO + GUARD-W for (e); event containment for (f): {𝒪, TV > ε} ⊆ {𝒪, Ŝ⁺ ≠ S₀} ∪ {π(S₀) ≤ max(½, 1−ε)}. **Key lemma:** N13 retention. |
| Difficulty | S. |
| Lean core | (a)–(d): finite inequalities on a finite Ω; (e): finite event algebra given Lemma RO; (f): the containment is finite; the limits are prose. |
| Dependencies (card IDs) | M5 (b1-LH) for (f); S-T (T03♯, Thm5-LH) for π(S₀) → 1; S-OUT (Lemma RO, GUARD-W) for (e); S-TARGET (N17) for (d); S-CERT (G2/L/R item semantics); M1 (T12 E[Ẑ_r\|𝒞] = Z for Markov); S-BLOCKS (SIZE on LH). |
| Risk | GUARD-W audit (N2(e)); N16 floating point; N3 (e4 DP) hypothesis in (f); SAME-FAMILY-ONLY on LH; MZ-P3 AUTHOR-ONLY. |
| Fallback statement and stop rule | (a)–(d) always ship (deterministic). If the GUARD-W audit fails: (e) in potential-run form only; the output form is withheld and CEX-guard disclosed (engineering fix, not a theorem fix). If LS0 integration (N3/OP-LS0) stays open: (f) ships under the named premises, as now. If (f) were lost altogether: the deterministic (b) plus Ẑ < Z_𝒯 ⇒ Ẑ < Z remain and HQ is told that Q3's named masked statement has shrunk (never silently). Stop: none for (a)–(d); one HQ cycle for the GUARD-W audit; (f) follows M5's stop rule. |
| IC3 design, exhibited, where checked | (a)–(e): any design (W1PC1 D0/E2 finite stores incl. the h = (0, 100) repair; W1PC2 40 designs × 5 random stores incl. duplicate columns). (f): LH exact Gram as above, verified W1PC2 shared LH (λ_min(Σ) = .4212, cov(x_hub, y) = 0 exactly, strict separation .6 < .8, LH-LAT margin m₀ = .0325, B ∈ [9, 16] for n ≥ 9⁶): a genuinely masked family. |
| Numerical companion (≤ 20 seeds) | Existing: W1PC2 `misc_checks.py` (D5U, D5TV); PC2's exact-rational card test (60 cases). For the HQ: ≤ 20 seeds on LH at n = 10⁴ (p = 18) with forced SMC dispatch plus one run at n = 9⁶, recording S₀ ∈ 𝒮, S₀ ∈ 𝒯, 1 − Z_𝒯/Z, max_j\|PIP^𝒯_j − PIP_j\|, MPM^𝒯 = S₀, and the Ẑ < Z_𝒯 flag. |
<!-- END VERBATIM -->
<!-- END VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:240-271 -->


---

## TH05 (M5 Theorem HPM (composition at every n; reported HPM with LS0 on LH; Theorem A))

| Field | Value |
|---|---|
| Archive ID | **TH05** |
| Native name | M5 · Theorem HPM (composition at every n; reported HPM with LS0 on LH; Theorem A) |
| K-IDs (MINUTES §2.1) | K72, K69, K65, K68; K63 hypothesis; K70 labelled no-LS0 variant; K82 remark |
| Authoring seat / final card source | Seat D (Fable 5.1, fresh-eyes) · `R3_D.md:141–158` |
| HQ charter | `branch_snapshots/MEET-THM/HQ_CHARTERS/M5.md` (wave 3, `MEET-THM/MINUTES.md` §2.5) |
| Binding goal / escalation | No binding goal rests on M5 alone, but M5 feeds M4(f) (binding masked statement). Charter escalation evidence: "a counterexample to T38-b1-LH on LH; the integrated LS0 differing from the specified LS0; N3 failing outright." |
| Who checked (Summary, from the card's own verdict/status rows and `MEET-THM/MINUTES.md` §1) | W1PC1 §6, §7 (E1: 1,440 cases), W2PC1:122 (Sol): TRUE-AS-WRITTEN / REPAIRED; W1PC2 D4, W2PC2:126–127 (Opus 5.5): DESIGN-VERIFIED / TRUE-AS-WRITTEN; ingredients: Thm4-C1 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none); T38-(0) PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5)); TheoremA PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2)); LS-score and T38-b1-LH XF VERIFIED* (A-REV8); N3 OPEN; assembly PROOF SKETCH, unchecked. Lean: `T37Greedy.lean`, `T37Lattice.lean`, `T21HPM.lean` (sorry-free per card). |
| Dependencies (Summary of the card's Dependencies row) | S-T TH09 (δ₁ → 0); M3 TH03 (start-mode centre, π₀(S₀) law); S-BLOCKS TH11 (SIZE); S-CERT TH14 (K64); S-OUT TH15 (K77, K78, K84, K63). Used by M4(e)/(f) TH04, M8 TH08. |
| Source positions | [pos 1348] ("Selection accuracy of the reported HPM"), [pos 1142] (HPM stays primary rule), [pos 1626], [pos 1650] |
| Statement location | `MEET-THM/THEOREM_LIST_FINAL.md` lines 279–306 (verbatim block below, including the card's own Hypotheses/premises, Statement, Status and Dependencies rows) |

**Chair's integration note(s) and verbatim card:**

1. K70 stays in this card as the labelled no-LS0 variant clause (b2-LH) (A, B, D: clause; C: supplementary attributed variant; MINUTES §2.1 follows the clause form). K63 is a hypothesis here, proved in S-OUT.
2. N2(c) (integrated LS0 replay), the N3 DP invariant (e4 centre), GUARD-W, N14(c) (IND-T extension for R′ > 4) and K84/N14(a) (extra search at R′ > 4) are named implementation premises (MINUTES §2.3, "Audit obligations").
3. If (b1-LH) falls, the §5.4 masked statement rests on M4's regime-free certificate; that loss escalates (MINUTES §2.3 §2.7).
4. **δ₁ correction (final audit #7).** In the deterministic clause, read δ₁ := 1 − π(S₀), pointwise, as in M4: "if S₀ ∈ 𝒮⁺ and 1 − π(S₀) < ½, then Ŝ⁺ = S₀". The probability bound keeps its expectation, written 2E₀[1 − π(S₀)] + D_n. The card's single symbol "δ₁ := E₀[1 − π(S₀)]" conflates the two; the HQ uses this reading.


<!-- BEGIN VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:285-306 -->
**Source:** `theory_campaign/MEET-THM/R3_D.md:141–158` (verbatim)

<!-- BEGIN VERBATIM R3_D.md:141-158 -->
### Card M5 · Theorem HPM (composition at every n; reported HPM with LS0 on LH; Theorem A) — K72, K69, K65, K68; K63 hypothesis; K70 labelled variant; K82 remark

| Field | Content |
|---|---|
| Final statement | **Hypotheses (model/design):** standardised X, the shipped prior and hyperparameters (ridge/BB(1,p)/cap, IG(a₀, b₀)); for (b1-LH) and (b2-LH): LH exact Gram with p ≤ n − 1, c linked pairs, group size g, within-correlation ρ, link ψ with |ψ| < ρ, fixed β; the T03♯ hypotheses on LH (G, R, SE_λ(j₀), SE_w(m♯; g₀), BM) and SIZE g_max ≤ B < 2g_min (holds on LH for n ≥ 9⁶ with g = 9, W1PC2 D4). **Implementation premises:** EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, e4, complete scans, ℓ ≥ τ(C) with a completed final scan; IND-T when R′ > 4. **(0) Composition at every n, any X.** Ŝ⁺ the ≻-maximum of the all-scored set 𝒮⁺ under (F, −|S|, lex) (K63). P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n, δ₁ := E₀[1 − π(S₀)]. If S₀ ∈ 𝒮⁺ and δ₁ < ½ then Ŝ⁺ = S₀. N200 bracket: P(U ∪ {Ŝ ≠ S₀}) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮), with the matching lower bracket, Π(X) measured, not bounded. Transfer to R′ > 4 only with the extra search from c₄ (nested scored set). **(a) Theorem A / LS-score.** Under TD′_∞ on Lat(S°), local search from C ∈ Lat(S°) with ℓ ≥ τ(C) and a completed final scan reaches and certifies S₀ within Φ(C) moves; LS0 scores S₀ within max{Φ(S°) − 1, 0} moves (scoring, not certification). **(b1-LH).** On LH with LS0: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; hence liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n). No delivery claim (K82 remark). **(a-fav) labelled variant:** under (F) with iid π₀ draws, D_n → 0. **(b2-LH) labelled variant (K70):** without LS0 on STAB-LH (g = 9, c = 2, ρ = 0.4, ψ = 0.2), any frozen grid, the same conclusion. |
| Guarantee | A wrong reported model means no output, a posterior miss, or a never-scored truth; on an explicit correlated family where the start misses the truth polynomially, the shipped method still reports it, jointly with output. |
| Serves | Objective (3); Song–Liang Thm S ("exact-HPM counterpart plus a separate reported-HPM result on LH"); THM-INV rows 11, 12; feeds M4(e) for §5.4's masked statement (HQ Q3). |
| Status (verbatim) | Thm4-C1 "PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none)"; T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; N200 "PROVED (elementary, every n); Π(X) upper bound OPEN" (author-only); TheoremA "PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2))"; LS-score "PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8))"; T38-b1-LH "PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8))" (registry ⚑ CONFLICT on the iid sub-claim, excluded); Thm-b1 "PROVED-UNDER (SF: VERIFIED (W5-VMASK); XF: VERIFIED (A-REV8))"; T38-(a) "PROVED-UNDER (SF: VERIFIED* (inputs); XF: none)"; B2E-B2LH "PROVED-UNDER (SF: none; XF: VERIFIED* (A-REV7))"; STAB-cert(A7) "REFEREE (Astra-authored)"; PART-ThmA "PROVED (XF: VERIFIED* (A-REV9))"; N3 "OPEN"; Thm5-LH (input via M3) "PROVED (SF: VERIFIED (W3-VEXP); XF: none)" SAME-FAMILY-ONLY. Assembly: PROOF SKETCH (by this seat, unchecked). **Fidelity:** v3.1 with LS0 (METHOD #8) for (0), (a), (b1-LH); any frozen grid; pooling not involved (scored-set maximum); (b2-LH) is v3 without LS0, labelled; (a-fav) is an iid-draw variant, labelled. |
| Verdict rows used | (0): W1PC1 §7 TRUE-AS-WRITTEN (E1, 1,440 cases), W2PC1:122 TRUE-AS-WRITTEN; R′ transfer W1PC1 §7 TRUE. (a): W1PC1 §6 NEEDS-HYPOTHESIS repaired to ℓ ≥ τ(C) + final scan, W2PC1:122 REPAIRED; W2PC2:127 (scoring vs certification) TRUE-AS-WRITTEN. (b1-LH): W1PC1 §6 TRUE-AS-WRITTEN, W1PC2 D4 TRUE as cited, W2PC1:122, W2PC2:126; liminf form W1PC1 §6. SIZE: W1PC1 §6 (PART-CE2), W2PC2:158. Variants: W1PC1 §6 TRUE-AS-WRITTEN as labelled variants. |
| Self-checked flag | N200 author-only; T38-(a) XF none; Thm5-LH SAME-FAMILY-ONLY; STAB-cert Astra-authored, Claude-verified. Integrated LS0 / emitted-centre / GUARD-W audits open (W2PC2:39; W2PC1:122 GAP). |
| Novelty | NEW for this target and method (NEW-COMP). Checked: Yang–Wainwright–Jordan, AoS 44(6) 2016 Thm 2, Lemma 4 (LIT-MCMC #1); Zhou–Yang–Vats–Roberts–Rosenthal, JRSSB 84(5) 2022 Thm 1 (LIT-MCMC #2): write "with their priors LH is covered by rapid mixing; ours is for the paper's own target and start". Hou–Wang–Atchadé arXiv:2407.20580 Thm 2 (LIT-STAT #19): never "first finite-n". Rossell 2022 Prop 1: the 2E₀δ₁ term is KNOWN—CITE. Barbieri–Berger 2004: HPM/MPM facts (K60, K61 cited lemmas). |
| Route / key lemma | (0) finite-set argument. (a) TD′ lattice descent (TheoremA) with the capped-scan interface. (b1-LH): LH centre law (M3) + LH-LAT margin m₀ > 0 + LS-score with the e4 centre + T03♯ (S-T) + retention (M4(b)). **Key lemma:** LS-score with the emitted centre equal to the prescribed start mode (N3). Difficulty: S (assembly); M for the N3 DP invariant. |
| Lean core | `T37Greedy.lean`, `T37Lattice.lean` (sorry-free); `T21HPM.lean` (`t21_C1` sorry-free). To add: the capped-scan certification interface (ℓ ≥ τ(C), completed scan ⇒ certified return) and (0) as a finite Boolean lemma with the output event. Cited probability: T03♯ (S-T), Thm5-LH masking law (M3). |
| Dependencies | Uses: S-T (δ₁ → 0), M3 (start-mode centre, π₀(S₀) law), S-BLOCKS (SIZE ⇒ blocks = groups, K07/K06), S-CERT (K64 search semantics and scan bound), S-OUT (K77 Lemma RO, K78 GUARD-W, K84 stacking nesting, K63 order). Used by: M4(e), Prop D (search cost term), COVERAGE_MATRIX Thm S row. |
| Risk | N3 OPEN (DP invariant); integrated-LS0 replay (N2(c)) pending; Π(X) only measured (K94 FW); study generator N8 uncovered (the g = 5 study is not the LH exhibit). |
| Fallback + stop rule | Fallback: (0) + (a) + (b2-LH) ship unconditionally; (b1-LH) labelled "conditional on N3" if the DP invariant is unproved after one HQ cycle. Stop: the merged-LS0 replay contradicting LS-score's centre rule, or a counterexample to T38-b1-LH on LH ⇒ (b1-LH) withdrawn, objective (3) coverage reported as (b2-LH) only; the §5.4 masked statement then rests on M4(d) + M4(b) (no binding goal dropped). |
| IC3 design (exhibited) | LH exact Gram, g = 9, c = 2, ρ = 0.4, ψ = 0.2, n ≥ 9⁶ (blocks = groups, SIZE, LH-LAT m₀ = 0.0325 > 0): W1PC2 D4 DESIGN-VERIFIED (`lh_family.py`), W2PC2:126 DESIGN-VERIFIED. (0): any X (W1PC1 §7 DESIGN-VERIFIED, Dε exact branch). |
| Numerical companion (≤ 20 seeds) | Filed: 0/2,394 HPM changes by LS0 (O-LS0 test export). New: forced-dispatch LH replica (PC2's `lh_family.py` + `smc_coded.py`) with LS0 at component size, ≤ 20 seeds, reporting the frequency of Ŝ⁺ = S₀, of S₀ ∈ 𝒮⁺, and of the D_n event; a component check, since production dispatches the exact branch at that size. |
<!-- END VERBATIM -->
<!-- END VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:285-306 -->


---

## TH06 (M6 Theorem SEP + Lemma KL)

| Field | Value |
|---|---|
| Archive ID | **TH06** |
| Native name | M6 · Theorem SEP + Lemma KL |
| K-IDs (MINUTES §2.1) | K19, K106, K105 |
| Authoring seat / final card source | Seat C (gpt-6-astra) · `R3_C.md:179–206` |
| HQ charter | `branch_snapshots/MEET-THM/HQ_CHARTERS/M6.md` (wave 2, `MEET-THM/MINUTES.md` §2.5) |
| Binding goal / escalation | No binding goal rests on M6 alone; it supplies M2(a)'s lower bound and M2(c2) (Lemma KL). Escalation evidence: refutation of a claimed production-law instantiation, or failure of the checked Q1(c) obstruction. |
| Who checked (Summary, from the card's own verdict/status rows and `MEET-THM/MINUTES.md` §1) | SEP-A/SEP-B: PROVED; SF: none; XF: VERIFIED (A-REV9). Lemma KL: PROOF SKETCH (NEW-SYNTH), AUTHOR-ONLY in IDX. CHK §2(a),(b) cross-family; PC2 (Opus 5.5) statement checks TRUE-AS-WRITTEN "do not upgrade KL". Final assembly PROOF SKETCH, unchecked. |
| Dependencies (Summary of the card's Dependencies row) | M3 TH03; S-T TH09; S-TARGET TH10. No dependence on M7, a production mixing theorem or Proposition D. Feeds M2(a),(c2) TH02. |
| Source positions | [pos 1348] ("Why the merge alone fails"), [pos 1626], [pos 1650] |
| Statement location | `MEET-THM/THEOREM_LIST_FINAL.md` lines 313–347 (verbatim block below, including the card's own Hypotheses/premises, Statement, Status and Dependencies rows) |

**Chair's integration note(s) and verbatim card:**

**Chair's integration note.** No change.

<!-- BEGIN VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:316-347 -->
**Source:** `theory_campaign/MEET-THM/R3_C.md:179–206` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:179-206 -->
### M6 — SEP + Lemma KL

| Card field | Final content |
|---|---|
| IDs | **M6: K19, K106, K105**. Generic finite-law inequalities are supporting lemmas; the LH consequence is the method-specific package. |
| Hypotheses | Finite \(\Omega\), strictly positive normalized \(\pi,\pi_0\), feasible distinguished \(S_0\). Write \(a=\pi_0(S_0)\), \(b=\pi(S_0)\). Statistical consequences use D0, EX-A and G on LH, with M3(f) and S-T. |
| Implementation premises | Comparison experiment: \(Q\ge1\) exact iid draws from \(\pi_0\), conditionally on data. One-shot estimation uses exact weights. No production-grid, mutation, LS0 or delivery premise enters these comparisons. |
| M6(a): discovery | Conditional on data, \(P(S_0\text{ absent from all }Q\text{ draws})=(1-a)^Q\le e^{-Qa}\). **Evidence:** W1P2 cluster 8, “D3 · miss probability”; W2P2 §2, C6. |
| M6(b): LH threshold | Let \(Q_n^\star=p^2n\). Under LH, \(Q_n/Q_n^\star\to0\) gives miss probability tending to one; \(Q_n/Q_n^\star\to\infty\) gives miss probability tending to zero, over data and comparison draws. **Evidence:** W2P2 §2, “C6 · Q* scale”. |
| Tables qualification | On LH, truth spans several actual blocks, so no block table evaluates the full truth. Adding existing block-table evaluations to this start-only comparison does not change its discovery event. **Evidence:** W1P1 §8, SEP-A scope; checked LH partition. |
| M6(c): singleton second moment | \(1+\chi^2(\pi\Vert\pi_0)\ge b^2/a\). On LH this yields an inverse-start-mass lower bound \(p^2n\exp\{O_P(1)\}\), with a two-sided tight positive multiplier. **Evidence:** W1P2 cluster 8, “D3 · χ² bound”; CHK §2(a),(b). |
| Evidence estimator | Let \(f(S)=\varpi(S)m(S)\), \(Z=\sum_Sf(S)\), and \(\widehat Z_Q^{IS}=Q^{-1}\sum_{i=1}^Qf(S_i)/\pi_0(S_i)\). Then \(\operatorname{Var}(\widehat Z_Q^{IS}\mid X,y)/Z^2=\chi^2(\pi\Vert\pi_0)/Q\). **Evidence:** W1P2 cluster 8, “D3 · IS variance”. |
| Interpretation of variance | Consequently, below the LH discovery scale the one-shot evidence estimator’s relative variance diverges in probability. This is an \(L^2\) obstruction; large variance alone is not a high-probability error lower bound. No matching upper bound is asserted. |
| Lemma KL | \(KL(\pi\Vert\pi_0)\ge b\log(1/a)-\log2\). **Evidence:** W1P2 cluster 8, “D3 · KL bound”; CHK §2(a). |
| KL consequence | On LH, \(KL(\pi\Vert\pi_0)\ge b\log Q_n^\star+O_P(1)-\log2\), hence diverges in probability. The finite singleton bound is the retained theorem; no universal sample-complexity conclusion for arbitrary functionals is attached. |
| Scope boundary | This is not a lower bound for production SMC, start-plus-search, or every one-shot estimator. SEP-taska remains a **COUNTEREXAMPLE**. Ideal logarithmic crossing counts do not imply logarithmic total work. |
| Guarantee | The specified iid start-only comparison needs the LH inverse-mass scale for discovery, while one-shot evidence correction inherits a corresponding second-moment obstruction. |
| Goals | Objective (1), with motivation for objectives (2), (3); proposal §5.3 one-shot obstruction and §5.4 start KL. Song–Liang Thm 4 is contextual comparison only; no analytic SL/FDR separation. |
| Status | SEP-A/SEP-B: **PROVED; SF: none; XF: VERIFIED (A-REV9)**. KL: **PROOF SKETCH (NEW-SYNTH)**, **AUTHOR-ONLY** in IDX. Statement checks remain TRUE-AS-WRITTEN; they do not upgrade KL. Final assembly: **PROOF SKETCH, unchecked**. |
| Fidelity/self-check flag | Actual shipped \(\pi_0,\pi\); explicitly different comparison algorithms. SEP ingredients have filed cross-family checks. KL and the final assembly lack a full proof certificate. SEP-A-iid and broader exponent claims are not imported. |
| Novelty/citation | **NEW-COMP** for the explicit LH start-mass mechanism. [Chatterjee–Diaconis, Thms 1.1–1.3](https://arxiv.org/html/1511.01437v3) supplies the established KL-scale context, with log-weight-tail and estimand qualifications. Finite coarsening and iid variance identities are not novelty claims. |
| Proof route/key lemma | M3 supplies two-sided tightness of \(Q_n^\star a_n\); apply the exact miss formula. Retain the singleton term in the second-moment sum. Binary KL data processing and binary entropy \(\le\log2\) prove Lemma KL. |
| Difficulty/Lean core | Routine after M3. Lean: iid miss probability, singleton second-moment inequality, binary coarsening/log-sum inequality and entropy bound. Probability tightness arguments remain prose unless separately formalized. |
| Dependencies | M3; S-T; S-TARGET. No dependence on M7, a production mixing theorem or Proposition D. |
| Risk | Replacing a lower bound by an asymptotic equality; confusing evidence variance with self-normalized variance; claiming probability failure from variance alone; claiming universal necessity of tempering. |
| Fallback/stop rule | Ship the exact discovery formula and finite singleton/KL/variance statements. If the LH application fails, withhold its scale claim until M3 is repaired. After one repair cycle, classify the extension FUTURE_WORK and notify M2; preserve CHK’s independently verified orthogonal Q1(c) obstruction. |
| IC3 exhibit/check | LH, with actual blocks and \(n\ge9^6\). W1P2 shared-family/cluster-8 rows, W2P2 C6, and CHK §2 supply the checked instantiation and finite inequalities. |
| Numerical companion | None newly run. Proposed: at most ten LH data seeds; compute \(a_n\) by exact convolution and evaluate \((1-a_n)^Q\) analytically. Avoid simulating \(p^2n\) draws. Enumerate small correlated component cases for KL/second-moment inequalities. |
<!-- END VERBATIM -->
<!-- END VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:316-347 -->


---

## TH07 (M7 Theorem STG (stage laws as coded; coverage identity))

| Field | Value |
|---|---|
| Archive ID | **TH07** |
| Native name | M7 · Theorem STG (stage laws as coded; coverage identity) |
| K-IDs (MINUTES §2.1) | K26, K25, K27, K30, K33 (deterministic termination/count form); K28 cited |
| Authoring seat / final card source | Seat A (Fable 5.1) · `R3_A.md:139–162` |
| HQ charter | `branch_snapshots/MEET-THM/HQ_CHARTERS/M7.md` (wave 2, `MEET-THM/MINUTES.md` §2.5) |
| Binding goal / escalation | No binding goal rests on STG alone: M2(b)'s stage-count clause has its own checked fallback T ≤ P + ⌈D_*/c_ρ⌉ + 1. Wave 2 because M2 consumes the count (c′) and the coverage identity (b). |
| Who checked (Summary, from the card's own verdict/status rows and `MEET-THM/MINUTES.md` §1) | W1PC1:190–198 and W2PC1:99 (Sol) TRUE / COUNTEREXAMPLE repaired (exact/minimal; count form); W2PC2:105,156 (Opus 5.5) TRUE-AS-WRITTEN (600 coded-pilot runs); CHK:91 (WS7 amendments); STG-M PROVED (SF: none; XF: VERIFIED* (A-REV9)); STG-G/L0/L1/L author-only; (c′) PROOF SKETCH (Seat C), unchecked; ConjP OPEN. Python translation of the coded rule checked, "no compiled bitwise replay". |
| Dependencies (Summary of the card's Dependencies row) | S-TARGET TH10 (Lemma 0: d finite); M3 TH03 (A₀); M1(c) TH01 (frozen 𝓒); S-IDENT TH13 (K25 lemma, K104). Feeds M2(b) TH02, M8 TH08. |
| Source positions | [pos 1348] ("Stage laws"), [pos 1624] (Q5: stage count a step function), [pos 1626], [pos 1650] |
| Statement location | `MEET-THM/THEOREM_LIST_FINAL.md` lines 355–387 (verbatim block below, including the card's own Hypotheses/premises, Statement, Status and Dependencies rows) |

**Chair's integration note(s) and verbatim card:**

1. K33 enters in its deterministic termination/count form only: the card's clause (a) (termination, ρ_V ≥ 0.9 per appended point, ≤ ℓ rebuilds per tier, T ≤ T_e) and clause (c) (the count). Rebuild convergence N5(b), P(S₀ ∈ V) and P(schedule_limit) → FUTURE_WORK (K31) in either case; Seat D's dissent (K33 in S-IDENT, R3_D §S1) is recorded in MINUTES §2.3.
2. K30 is clause (d), labelled ideal two-state grid, and is stated only here (S-STGI is dissolved). K29 is FUTURE_WORK FW23; its conditional implication may be cited as an attributed lemma.
3. The card's escalation statement: no binding goal rests on STG alone; M2(b) has its own checked fallback T ≤ P + ⌈D_*/c_ρ⌉ + 1.


<!-- BEGIN VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:360-387 -->
**Source:** `theory_campaign/MEET-THM/R3_A.md:139–162` (verbatim)

<!-- BEGIN VERBATIM R3_A.md:139-162 -->
### M7 · Theorem STG (stage laws as coded; coverage identity)

K-IDs: K26, K25, K27, K33, K30 (labelled ideal); K28 cited.

| Field | Content |
|---|---|
| Model/design hypotheses | Admissible (X, y) with positive finite tables, so γ₀ > 0 on Ω; a fixed nonempty V ⊆ Ω; D_V := osc_V d; for (d) a two-state restriction with initial log-odds −A₀ and terminal log-odds bounded away from 0 on the positive side. |
| Implementation premises (named) | EX-A; the coded grid rule (`v3_calib.h`: ESS threshold 0.9 for pilot and grid, P retained pilot targets, 60 halvings, 10⁻¹² snap/validation, T_e cap) equal to its mathematical rule (Python translation checked, no compiled bitwise replay: W1PC1:61); bisection resolution ≤ h_V/2 (2⁻⁶⁰ ≤ h_V/2); "success" is a reported status, with ceiling/snap failures excluded. |
| Statement | (a) Monotonicity and construction: ρ_V(u,v) is nondecreasing in u and nonincreasing in v; bisection accepts only intervals with ρ_V ≥ 0.9; build_grid terminates, every appended point has ρ_V ≥ 0.9, ≤ ℓ rebuilds per tier; T ≤ T_e on success; at exact frontiers the greedy grid is shortest among refinements of the retained pilot targets, up to the 2⁻⁶⁰ slack (no "exact/minimal"). (b) Coverage identity: ρ_full(u,v) = ρ_V(u,v)·a_u a_w/a_v², w = 2v−u, a_t = q_t(V); a_u, a_w ≥ 1−η ⇒ ρ_full ≥ 0.9(1−η)². (c) Interval inequality and count: every accepted interval has (v−u)²·Var_{q_ξ\|V}(d) ≤ log(10/9) for some ξ ∈ [u, 2v−u]; if D_V > 0 every increment ≤ h_V := 2c_ρ/D_V passes (c_ρ = √log(10/9)); with resolution ≤ h_V/2 and absent ceiling/snap failure, T ≤ P + ⌈2/h_V⌉ + 1 = P + ⌈D_V/c_ρ⌉ + 1; a uniform full-space grid (W = Ω) with max{1, ⌈osc_Ω d/(2c_ρ)⌉} stages has full ESS ≥ 0.9 (existence). (c′) Pilot-count clause, cited from M2(b): under a global range bound D_* and 2⁻⁶⁰ ≤ h/2, P ≤ ⌈2/h⌉ + 1, hence T ≤ 2⌈D_*/c_ρ⌉ + 2 ≤ 4 + 2D_*/c_ρ; D_* = 0 ⇒ T = 1 (PROOF SKETCH, Seat C). (d) Ideal grid, labelled, not the coded grid: on the exact-frontier two-state ESS-0.9 grid a dominance crossing of gap A₀ costs log₂A₀ + O(1) stages; separated pair-dominant crossings add; restricted ESS alone forces only log₂(9.5ℓ₀) stages (WS7(d) with the set-mass and endpoint amendments). (e) [cited] √c·T*(c) → Λ_len := ∫₀¹ sd_{q_φ}(d)dφ ≤ √J as c → 0. (f) The as-coded masked stage count T_n is Conjecture P, OPEN → FUTURE_WORK (K31); the shipped guarantee is T ≤ T_e. Favourable O(1) (K29) → FUTURE_WORK. |
| Verdict rows per clause | (a) W1PC1:190 TRUE; exact/minimal W1PC1:191 COUNTEREXAMPLE repaired; termination/rebuilds W1PC1:198 TRUE; W2PC1:99 TRUE. (b) W1PC1:192 TRUE; PC2 D7 to 10⁻⁸. (c) interval W1PC1:193 TRUE; count W1PC1:194 COUNTEREXAMPLE repaired to P + …; range/resolution W1PC1:195 NEEDS-HYPOTHESIS repaired; W = Ω W1PC1:140; zero range W2PC1:56 repaired max{1,·}. (c′) W2PC2:105, 156 TRUE-AS-WRITTEN (600 coded-pilot runs). (d) W1PC1:197 TRUE; CHK:91 (WS7 amendments). (e) W1PC1:257 (Λ_len renamed). |
| Guarantee | Every accepted stage of the coded grid is certified by an exact restricted-ESS inequality whose full-bridge meaning is the coverage factor; the stage count is bounded by the pilot targets plus the spread of d on V; and on the ideal grid correlation enters depth only through the crossing gap, as log₂A₀. |
| Serves | Objective (2) (island depth); proposal §4.4/§8.2 (what ESS 0.9 certifies); input to M2(b) (sandwich, envelope) and M8 (T); INV rows 5, 7 × C. |
| Status (verbatim) | STG-G, STG-L0, STG-L1: PROVED (SF: none; XF: none); T26BUD-G: PROVED, deterministic (AUTHOR-ONLY, W2PC2:155); STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)), explicit decimal constants GAP (W2PC2 C14); STG-L: PROVED (SF: none; XF: none); ConjP: OPEN; STG-cexW2: COUNTEREXAMPLE; OWS-WS7(d): PROVED (SF: none; XF: none) + CHK VERIFIED WITH AMENDMENT; (b), (c): D/E proposals, TRUE-AS-WRITTEN (W1PC1:192–193); (c′): PROOF SKETCH (Seat C, unchecked), W2PC2 TRUE-AS-WRITTEN; STG-F: PROVED (SF: none; XF: none), cited only (K29 FW). |
| Fidelity to v3.1 | (a)–(c), (c′): the coded rule (translation-checked). (d), (e): ideal exact-frontier / fine grid, labelled comparison objects; the gap to the coded grid is K31 (FUTURE_WORK). |
| Self-checked flag | Yes for STG-G/L0/L1/L (author-only) and (b), (c) (statement sanity only); STG-M cross-family VERIFIED*; (c′) unchecked. |
| Novelty | (a)(i) greedy optimality KNOWN—CITE Štefankovič–Vempala–Vigoda 2009 (LIT-SMC row 9); (e) KNOWN—CITE Syed et al. 2024 Thm 3, Gelman–Meng 1998 (LIT-SMC row 15); (b), (c), (d) NEW, elementary (checked LIT-SMC digest; no published restricted-ESS coverage identity found). |
| Route / key lemma | Lemma RS (ρ_V(u,v) = Z_V(u)Z_V(w)/Z_V(v)², convex log-MGF ⇒ monotonicity); second-order mean value for log-sum-exp gives (c); Popoviciu Var ≤ D_V²/4 gives the passing step; bisection invariant keeps the lower endpoint passing; two-point algebra for (d). Key lemma: Lemma RS. |
| Difficulty | S for (a)–(e); (c′) S–M. |
| Lean core | Lemma RS identity; Theorem G optimality among refinements of fixed targets; (b) identity; (c) finite inequality with the Popoviciu step; (d) two-state recurrence bound. |
| Dependencies | S-TARGET (Lemma 0: d finite); M3 (A₀ through π₀(S₀) for (d)); M1(c) (frozen 𝓒); S-IDENT (K25 lemma, K104 for (e)). Feeds M2(b), M8. |
| Risk | The resolution/snap premises; the (c′) pilot-progress lemma unchecked; no compiled replay of the coded rule. |
| Fallback + stop rule | (a), (b), (d), (e) with T ≤ T_e and the interval inequality of (c); drop the counts if the resolution/progress lemma fails. Stop: one wave on (c)/(c′). No binding goal rests on STG alone: M2(b)'s stage-count clause has its own checked fallback T ≤ P + ⌈D_*/c_ρ⌉ + 1. |
| IC3 design, exhibited | (a)–(c): Dε (n = 40, p = 8, built pairs, cross 10⁻⁵–10⁻⁴; W1PC1:71) and my p = 16 exhibit (W2PC1:61), component checks (production dispatches exact); C's family W with the coded pilot replica, 600 adversarial runs (W2PC2:50, 156), SMC-dispatched for n ≥ 9⁶. (d): the truth/start-mode two-state restriction of LH (c = 2), masked (A₀ → ∞). |
| Numerical companion (≤ 20 seeds) | O-STAGES numerics log₂A₀ + 7.7 ± 0.4 (exists); PC2 `c8_pilot.py` (exists); E-pilot 16 cases (W2PC1:55). For the HQ: coded-grid replica on W at n = 9⁶, 10 seeds, T against P + ⌈D_V/c_ρ⌉ + 1 and 2⌈D_*/c_ρ⌉ + 2. |
<!-- END VERBATIM -->
<!-- END VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:360-387 -->


---

## TH08 (M8 Proposition D (work, depth and width at the island level))

| Field | Value |
|---|---|
| Archive ID | **TH08** |
| Native name | M8 · Proposition D (work, depth and width at the island level) |
| K-IDs (MINUTES §2.1) | K87, K88, K89, K06, K64; K90 remark |
| Authoring seat / final card source | Seat D (Fable 5.1, fresh-eyes) · `R3_D.md:160–177` |
| HQ charter | `branch_snapshots/MEET-THM/HQ_CHARTERS/M8.md` (wave 3, `MEET-THM/MINUTES.md` §2.5) |
| Binding goal / escalation | No binding goal is involved. Placement in the main text rests on objective (2). Seat D's alternative for Felipe: "if objective (2) is to be served by a sentence in the introduction citing the supplement instead, Prop D moves to the supplement and main = 7" (MINUTES §2.1; FOR_FELIPE decision 3). |
| Who checked (Summary, from the card's own verdict/status rows and `MEET-THM/MINUTES.md` §1) | W1PC2 D6 (Opus 5.5) TRUE as counting; W2PC2:133 TRUE-AS-WRITTEN; W1PC1 §13 / W2PC1:205 (Sol) NEEDS-HYPOTHESIS repaired to a remark; MA-PropD PROVED (counting, given the code's structure) AUTHOR-ONLY; T32(i) PROVED (SF: VERIFIED (W7-SEC); XF: none), displayed rate GAP (A-REV5); calibration share "seat-derived, unchecked"; assembly PROOF SKETCH. Execution-DAG audit open (named premise). |
| Dependencies (Summary of the card's Dependencies row) | M7 TH07 (T ≤ T_e; on C's family the M2(b) envelope); S-CERT TH14 (K64 search bound); S-OUT TH15 (K83 worker equivalence, K84 nesting). Used by the CD remark TH22 and COVERAGE_MATRIX Song–Liang §6 row. |
| Source positions | [pos 1304] (Felipe approved "island-level depth only"; recorded in METH31 §3 C6 and MINUTES decision 6), [pos 1263], [pos 1348] ("Work and depth"), [pos 1626], [pos 1650] (decision 3: Prop D main or supplement) |
| Statement location | `MEET-THM/THEOREM_LIST_FINAL.md` lines 395–421 (verbatim block below, including the card's own Hypotheses/premises, Statement, Status and Dependencies rows) |

**Chair's integration note(s) and verbatim card:**

1. K90 is a remark (the card has it as a remark); the Song–Liang §6 comparison is in the same units with no speed claim (MINUTES §2.1).
2. Seat D's note for Felipe (R3_D §S5, MINUTES §2.1): if objective (2) is served by a sentence in the introduction citing the supplement, Prop D moves to the supplement and main = 7. Nothing else changes.
3. The execution-DAG audit (N15) and N14(c) are named implementation premises (MINUTES §2.3).


<!-- BEGIN VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:400-421 -->
**Source:** `theory_campaign/MEET-THM/R3_D.md:160–177` (verbatim)

<!-- BEGIN VERBATIM R3_D.md:160-177 -->
### Card Prop D · Proposition D (work, depth and width at the island level) — K87, K88, K89, K06, K64; K90 remark

| Field | Content |
|---|---|
| Final statement | **Units:** sequential elementary-step slots (METHOD §2 #19); score evaluations and memory counted separately. **Hypotheses (design/budget, all explicit functions of (n, p)):** the shipped budgets N₀ = max{2,500, n, p}, H₀ = ⌈512N₀/2,500⌉, L = max{4, ⌈log₂(n + 1)⌉}, ℓ = ⌈log₂(n + p + 1)⌉, T ≤ T_e on success, B = min{⌊√n⌋, ⌊√p⌋, 16}, K; m := p + B + 2; k* := min(K, ⌊p/2⌋); R′ = 4k declared; w island workers. **Implementation premise:** the execution DAG as specified (METHOD §6.8, §8; AMENDMENT_HQ_01 #18, #19, #42); the integrated DAG audit is open. **(a) Final run.** Work = R′·N_e·(T + L + 4)·m slots; island depth = N_e·(T + L + 4)·m, in ⌈R′/w⌉ waves; width R′. With w ≥ R′ the depth does not depend on R′. **(b) Calibration.** Work = Σ_i N_i(T_i + L_i + 4)m over the executed pilot, diagnostic and rebuild trajectories, each with its own grid; per tier at most (1 + 4I_e)H_e trajectories enter work and (1 + I_e)H_e sequential trajectory equivalents enter four-worker depth, I_e ≤ ℓ rebuilds per tier (≤ 2ℓ with escalation). **(c) Searches.** Each local search (final, extra from c₄ when R′ > 4, LS0) scores at most (ℓ + 1)[p + k*(p − k*)] models; each is counted separately. **(d) Polynomial work and scheduling.** For p ≤ n^A, under the budgets above and any permitted polynomial R′, total work is polynomial in n; on w workers, time ≤ W/w + D (Brent). **(e) Ceilings.** Θ(p) slots per round and Θ(p²) Gram memory are not removed by islands or particles. **Remarks (not clauses):** the SL §6 comparison in the same units states worker counts, n-vs-p scaling, T, score cost and the loss criterion, with no same-order, exact-output or speed claim; the single-tier calibration share 0.0512 + 0.2048·I is seat-derived, unchecked; on C's family M7 + M2(b) give T ≤ 4 + 2D_*/c_ρ = O_P(1), so the island depth is O_P(N_e(L + D_*/c_ρ)(p + B)). |
| Guarantee | In a referee's units, islands add width without adding depth; the work is polynomial; accuracy grows with width through M1(b),(d′) at fixed depth; no speed-up over sequential MCMC is claimed. |
| Serves | Objective (2); Song–Liang §6 ("same-unit accounting; speed comparison not established"); THM-INV row 8 (work–depth), I1/I2/I9 ceilings. |
| Status (verbatim) | MA-PropD "PROVED (counting, given the code's structure)" AUTHOR-ONLY; T32(i) "PROVED (SF: VERIFIED (W7-SEC); XF: none)", displayed rate GAP (A-REV5), registry ⚑ CONFLICT marker carried; Cost-T38 "PROVED-UNDER (SF: VERIFIED (W3-VT38E); XF: GAP (A-REV5))"; calibration share "seat-derived, unchecked" (N15); assembly PROOF SKETCH (by this seat, unchecked). **Fidelity:** island level, v3.1 as shipped; "depth free of N, H, R" struck (MEET-v31 decision 6); K88's particle-parallel critical path is v3.2 and not claimed. |
| Verdict rows used | (a): W1PC2 D6 "final run" TRUE as counting; W2PC2:133 TRUE-AS-WRITTEN (m = p + B + 2; waves); W2PC1:205 TRUE-AS-WRITTEN as corrected accounting. (b): W1PC2 D6 "calibration and LS" TRUE (amendments #18, #42); W2PC2:133; per-trajectory sums repair W1PC1 §13 AMBIGUOUS → REPAIRED (W2PC1:205). (c): W1PC2 D6 TRUE. (d): W1PC1 §13 "polynomial/Brent" TRUE-AS-WRITTEN. (e): W1PC1 §13 first row (memory, block count) DESIGN-VERIFIED on Dε. SL remark: W1PC1 §13 NEEDS-HYPOTHESIS, repaired to a remark (W2PC1:205). |
| Self-checked flag | MA-PropD author-only; T32(i) XF none; calibration share unchecked. Route to a cross-family code read in the charter. |
| Novelty | MODEST (accounting, TCS-standard). Checked: Brent 1974 (cited for W/w + D); Zhou–Yang–Vats–Roberts–Rosenthal 2022 §3 (LIT-MCMC #2): different kernel and per-step cost, no comparison made; Song–Liang 2015 §6 (`theory_campaign/inputs/`): K_n = √P_n, O(P_n^{(1+α)/2}) + O(nP_n), quoted in the remark only. |
| Route / key lemma | Counting over the execution DAG. **Key lemma:** the trajectory inventory (every executed trajectory with its own (N_i, T_i, L_i); every completed search), which is exactly the W1PC1 §13 repair. Difficulty: S (mathematics), M (code audit). |
| Lean core | The counting identity (sum of products over the inventory), the scan bound p + k*(p − k*) ≤ p + p²/4, and Brent's inequality as finite lemmas; low value but certifiable. Nothing rests on probability theory. |
| Dependencies | Uses: M7 (T ≤ T_e; on C's family the M2(b) envelope), S-CERT (K64 search bound), S-OUT (K83 worker equivalence, K84 stacking nesting for the extra search). Used by: the CD remark, COVERAGE_MATRIX §6 row. |
| Risk | The DAG audit finds an uncounted serial component (e.g. a reduction across islands that is not trivially O(R′)), or a calibration path that is not a trajectory sum; then (a)/(b) are restated, not dropped. |
| Fallback + stop rule | Fallback: W and D_PEL as symbolic sums without rates and without the calibration-share remark. Stop: simplification stops at any unaudited component; if the audit shows depth growing with R′ at w ≥ R′, clause (a)'s last sentence is withdrawn and HQ is told (objective (2) wording changes). No binding goal is involved; a p > 2,500 demonstration would fire the C6 trigger and go to HQ. |
| IC3 design (exhibited) | Any admissible input. Checked on Dε (J = 4 blocks, Σ2^{|C_b|} = 16 = p2^B/B; W1PC1 §13 DESIGN-VERIFIED) and on C's family W (W2PC2:133 DESIGN-VERIFIED, any input). |
| Numerical companion (≤ 20 seeds) | Filed: calibration/final ratio predicted 0.46/0.67/1.69 vs observed 0.45/0.62/1.76 on 3 designs. New: the timing tabulation of AMENDMENT_HQ_01 §4 item 9 (`timings$calibration`, `timings$final`, rebuilds, tier, T) on ≤ 20 saved study fits, compared with (a)–(b) evaluated from the saved budgets; Owls ≤ 8 cores, read-only. |
<!-- END VERBATIM -->
<!-- END VERBATIM MEET-THM/THEOREM_LIST_FINAL.md:400-421 -->


---

# A3 · The 12 supplement cards (TH09–TH20)

Source: `MEET-THM/THEOREM_LIST_FINAL.md` Part II ("For each card: the decision note from MINUTES §2.2, then the statement copied verbatim from the seat card(s) that carry it"). Each section below reproduces the TLF section **in full, verbatim** (every statement is ≤ 40 lines, so the 40-line rule never needs a headline-plus-pointer); seat variants are all kept, and the card the chair calls "fullest" is named in the decision note inside. Supplement-card HQs are the lemma packs (LP-FOUND: TH09–TH12 with S-T cited only; LP-IDENT: TH13; LP-AUDIT: TH14–TH15; LP-REST: TH16–TH18; LP-REP: TH19–TH20), whose chair\'s generic rule IC7 reads: "the card ships in the narrowest form its filed checks support. A clause whose proof or cross-family check fails after one repair cycle moves to `FUTURE_WORK.md` with the reason. It is never relabelled as a limitation, and no status is upgraded." (e.g. `HQ_CHARTERS/LP-FOUND.md` Charter table, Fallback row).

Chair-specified fallbacks (CLOSE_AUDIT #8, `HQ_CHARTERS/LP-AUDIT.md`): S-CERT: "the deterministic perturbation lemma K108 (Z̃/Z ∈ [e^{−ε}, e^{ε}], TV ≤ tanh ε, and gap > 2ε preserves the winner). Also the exact semantics of the local-search flags (K64, a weak local maximum, with ties allowed). No B&B-soundness, rounding or region-certification claim."

Index (ID · native name · K-IDs · lemma-pack charter · wave · key status words, all copied from the sections below · key dependencies · positions):

| ID | Native | Name | K-IDs | Lemma pack (wave) | Status words (verbatim from the section) | Dependencies (Summary of charter edge lists) | Positions | TLF lines |
|---|---|---|---|---|---|---|---|---|
| TH09 | S-T | Theorem 1, target consistency T03♯ | K93, K04 | LP-FOUND (cited, no HQ work) (wave 1) | T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY | cited by M1(i) TH01, M2(c1) TH02, M3 TH03, M4(f) TH04, M5 TH05, M6 TH06, S-LEAK TH20 | [pos 1626] | 434–499 |
| TH10 | S-TARGET | Propriety, invariance, envelopes, exact branch, odds certificate | K01–K05, K76, K95 | LP-FOUND (wave 1) | N17: PROVED. T01: PROVED-LOCKED (wave 3; external review queued); SAME-FAMILY-ONLY. Remaining assembly: PROOF SKETCH, unchecked. N12 eventual dispatch: seat-proved, unchecked; T26-exact-branch-paren: XF ERROR (corrected) | → M1 TH01, M2 TH02 (Lemma 0), M3 TH03, M4(d) TH04 (N17), M7 TH07, S-REP TH19, S-Z TH16, S-T TH09 | [pos 1626] | 504–577 |
| TH11 | S-BLOCKS | Separation ⇒ groups kept; SIZE ⇒ equality | K07, K14, K06 | LP-FOUND (wave 1) | PART-ThmA: PROVED; SF none; XF VERIFIED*. Counting/graph assembly: PROOF SKETCH, unchecked. PART-pairing remains OPEN, excluded. PART-CE2: COUNTEREXAMPLE | → M2 TH02 (IC3 partition), M3 TH03, M5 TH05, M8 TH08, M4(f) TH04 (SIZE on LH) | [pos 1626] | 581–630 |
| TH12 | S-KERNEL | N9 kernel facts, graph (p ≥ 2), start sampler, minorisation | K20, K21, K08, K09, K22, K103 | LP-FOUND (wave 1) | N9K: PROVED (candidate), N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT (PC1, cross-family); T09: PROVED-LOCKED (wave 1); N3: OPEN; K22, K23, K103: PROVED (by this seat, unchecked), PC1 §19 TRUE-AS-WRITTEN. K09 (C10): PROOF SKETCH, unchecked; N3 "remains OPEN" | → M1(a) TH01, M3 TH03, M2(b4) TH02, S-IDENT TH13, S-REP TH19; K09/N3 carried as hypothesis in M5 TH05 and M4(f) TH04 | [pos 1550], [pos 1593] (N9 vs production code), [pos 1626] | 634–721 |
| TH13 | S-IDENT | Restricted-ESS coverage identity, TI/KL/TV calculus, C15-CI clause | K25 lemma, K104, K55, K103 | LP-IDENT (wave 2) | C15-TV, C15-KL, C15-CI: PROOF SKETCH, unchecked (assembly); Independence-sampler foundation: KNOWN—CITE; S9: PROVED (by this seat, unchecked); OWS-WS1: PROVED (SF: none; XF: none) | ← S-KERNEL TH12 (K103), M1 TH01, M2 TH02 (W rates), M7 TH07; → M2(b) TH02, M6 TH06, M7(e) TH07, S-REP TH19 | [pos 1614] (Q2 posterior-content reading), [pos 1626] | 725–827 |
| TH14 | S-CERT | Local search, certificate semantics, B&B soundness, perturbation lemma | K64, K73 (without the region-certification clause), K74, K05, K108 | LP-AUDIT (wave 3) | N7 L1: CORRECT WITH AMENDMENT; OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9)); OCERT-C4: PROVED (XF: VERIFIED*). K107 (rounding bound) FUTURE_WORK (N16 OPEN; T33-errbound COUNTEREXAMPLE) | → M4 TH04 (card semantics), M5 TH05 (Theorem A, LS-score, scan bound), M8 TH08 (search cost) | [pos 1626] | 930–965 |
| TH15 | S-OUT | Output-event validity, worker equivalence, stacking | K77, K78, K83–K86, K63 | LP-AUDIT (wave 3) | LemmaRO: PROVED; SF VERIFIED; XF VERIFIED*. CEX-guard: COUNTEREXAMPLE; XF VERIFIED*. N6 potential-run: PROVED; output form: CORRECT WITH AMENDMENT. GUARD-W: not audited | → M1(c,d) TH01, M4(e) TH04, M5 TH05, M8 TH08, S-REP TH19 | [pos 1626] | 968–1009 |
| TH16 | S-Z | Evidence variance, masked tails | K37–K41, K53 | LP-REST (wave 4) | OPW2-ThmA: PROVED (SF: none; XF: VERIFIED (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; FMP-Na: PROVED (SF: none; XF: GAP (A-REV9)); PC1c4: PROVED; T26-ThmA: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)); T26 overall CONJECTURE. Both variance bounds ship (TLF "Chair's choices" item 3) | ← M2(a) TH02 (D), M3 TH03, M4 TH04 (envelope), S-TARGET TH10 | [pos 1626] | 1012–1047 |
| TH17 | S-POOL | Pooling rules, the checked recording-marginal equal-weight bias comparison P1, R_eff | K49, K50, K54, K56, K57-P1 | LP-REST (wave 4) | MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); MZ-P1P2: P1 PROVED; MA-CorV: PROOF SKETCH; ADRAFT-ThmA Astra-only, cite Del Moral; OBG-LH-lock-general: XF ERROR. General K57 accuracy → FUTURE_WORK (CJ08 / FW8) | ← M1 TH01, M3 TH03 | [pos 1626] | 1050–1099 |
| TH18 | S-LIM | Limitations as theorems; K99 qualitative remark | K79, K81, K100, K101 (K74 per seat B) | LP-REST (wave 4) | CEX-localmax(A2), CEX2, CEX-ESSneutral(A3), PropD-T03, SHARE-PB: COUNTEREXAMPLE (constructions); INP I5 PROVED | ← M4 TH04 (cited) | [pos 1280], [pos 1626] | 1103–1138 |
| TH19 | S-REP | Run-card reporting corollary: Ĵ (B/C/D form) and ε̂_× with companions | K104/K11 reporting corollary (using K46/K52/K102) | LP-REP (wave 4) | Reporting assembly: PROOF SKETCH, unchecked. N1: PROOF SKETCH. PC1c3: PROVED, with N1 as premise. W2P2 C16 and repaired W2P1 T4/T5 are statement/route checks, not a full proof upgrade | Dependencies row: M1; M2 for informative W rates; M3 for discrepancy definitions; S-KERNEL for exact initialization; S-OUT for delivered-event transfer | [pos 1608]/[pos 1614] (Q4: reporting allowed), [pos 1626], [pos 1639] | 1195–1244 |
| TH20 | S-LEAK | B's leakage clauses (F), (S) as a supplementary corollary to M2 | Seat B (b5)(b6) fragments | LP-REP (wave 4) | OWS-WS6(b): PROVED (SF: none; XF: none), PC1 B.D6(S) TRUE; the m lower bound: PROVED (by this seat, unchecked; q₂(S₀)/π₀(S₀) = e^{2d(S₀)}/E_{π₀}e^{2d}); (b6) OWS-WS53F: PROVED-UNDER (SF: none; XF: none); PC1 B.D6(F) TRUE / DESIGN-VERIFIED (D_B) | ← M2 TH02, M3 TH03, S-T TH09 | [pos 1626] | 1141–1192 |


---

## TH09 (S-T · Theorem 1, target consistency T03♯)

Archive ID **TH09**; native **S-T**; K-IDs K93, K04; lemma pack LP-FOUND (cited, no HQ work), wave 1; positions [pos 1626]. Verbatim TLF section (lines 434–499):

## S-T · Theorem 1, target consistency T03♯ (K93, K04)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:60`):** content = Theorem 1, target consistency T03♯ (K93, K04). Notes and decisions = Unanimous since Round 2; cited in the main text

Registered here as a cited supplement; no HQ work (registered with LP-FOUND). A, B and D file the statement as "unchanged from R1" with scope notes; C filed the full self-contained statement (C9 with its hypotheses table). Compatible; no choice needed.


#### Seat C (R2_C): hypotheses table

**Source:** `theory_campaign/MEET-THM/R2_C.md:148–153` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:148-153 -->
| §R2 — Statistical hypotheses for C9 | Definition |
|---|---|
| R1, R | Fixed-design triangular array, fixed \(s_0\ge1\), \(p\le n^A\) for fixed \(A\), \(s_0\le K\) eventually; G; \(\mu=X\theta^*\), \(\Vert\mu\Vert^2\le Mn\), and normalized truth Gram eigenvalue at least fixed \(\phi_0^2>0\). |
| Tail cutoff | With per-model prior weight \(w(k)\), \(R_m=\sum_{k=\max(m+1,0)}^K\binom pk w(k)/w(s_0)\), and \(m_n^\sharp=\min\{m\ge s_0:R_m\le n^{-(s_0+2)/2}\}\). It is deterministic and data-free. |
| Anchored eigenvalues | \(j_0=\lceil(2A+1)s_0\rceil+1\). SE\(_\lambda(j_0)\): every \(S_0\cup J\), \(\lvert J\rvert\le j_0\), has normalized minimum eigenvalue at least \(\phi_0^2\). SE\(_w(m_n^\sharp;g_0)\): every \(S_0\cup J\), \(\lvert J\rvert\le m_n^\sharp\), has unnormalized minimum eigenvalue at least fixed \(g_0>0\). |
| Signal thresholds | BM-∞: \(\theta_{\min}^{*2}n\phi_0^2/(\sigma^2\log n)\to\infty\). Alternatively BM\((c)\) uses a fixed \(c>c_0(s_0,A)\), with \(c_0=\max\{4C_*,32[s_0(A+1)+2]\}\), \(C_*\) the locked T03 proof constant, exactly as FIX §1.1. |
<!-- END VERBATIM -->


#### Seat C (R2_C): final card C9

**Source:** `theory_campaign/MEET-THM/R2_C.md:155–164` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:155-164 -->
| C9 — K93 | Final card |
|---|---|
| Final statement | Under R1, G, R, SE\(_\lambda(j_0)\), SE\(_w(m_n^\sharp;g_0)\), and BM-∞ or BM\((c>c_0)\), \(1-\pi(S_0)=O_P(\sqrt{\log n/n})\); exact HPM and MPM are consistent. Without beta-min, for \(J_n(c)=\{j\in S_0:\theta_j^{*2}\ge c\sigma^2\log n/(n\phi_0^2)\}\), \(c>c_0\), \(\pi(S\not\supseteq J_n(c))=O_P(\sqrt{\log n/n})\), hence all corresponding exact PIPs converge to one. Empty \(J_n(c)\) gives a vacuous inclusion statement. |
| Repairs | PC1/PC2 statistical clauses: no expectation rate inferred from \(O_P\), no universal onset \(n_0\), no random-design or growing-sparsity extension. |
| Status | T03♯: **PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)**. T02(i♯), T02(ii♯): **PROVED; SF/XF VERIFIED**. |
| Placement | Supplement. |
| Route / key lemma | Cite FIX §1 and the filed exact-prior-tail/selection checks; no re-derivation. |
| Lean core | Finite prior-tail and posterior-to-decision inequalities; Gaussian asymptotics remain prose. |
| Fallback / stop | Fixed-\(p\), uniformly nonsingular correlated design; narrow scope if hypotheses cannot be matched. |
| IC3 | LH satisfies fixed sparsity, bounded energy, positive full Gram eigenvalue and BM-∞. Otherwise unchanged from R1 §D D8. |
<!-- END VERBATIM -->


#### Seat A (R2_A) S1

**Source:** `theory_campaign/MEET-THM/R2_A.md:127` (verbatim) — base statement: R1_A C15 `theory_campaign/MEET-THM/R1_A.md:413`

<!-- BEGIN VERBATIM R2_A.md:127-127 -->
**S1 · Theorem T (K93; K61 remark).** Statement unchanged from R1 §D C15 with the scope sentence (p ≤ n^A from prior and technique; e^{Cn^α} OPEN) and onset n ≳ 2·10⁶. Status: T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY. Supplement; cited in the main setup. Rest unchanged.
<!-- END VERBATIM -->


#### Seat B (R2_B) S2

**Source:** `theory_campaign/MEET-THM/R2_B.md:165–167` (verbatim) — base statement: R1_B D13 `theory_campaign/MEET-THM/R1_B.md:374`

<!-- BEGIN VERBATIM R2_B.md:165-167 -->
### S2 · Theorem 1, target consistency (K93) · supplement (short)

Final statement unchanged from R1 §D D13 (R1 fixed s₀, p ≤ n^A; G, R, SE_λ, SE_w, BM-∞ or BM(c > c₀); 1 − π(S₀) = O_P(√(log n/n)); HPM/MPM consistent; large-signal inclusion without beta-min). Status: T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); T01–T03: PROVED-LOCKED (wave 3; external review queued) SAME-FAMILY-ONLY; onset n ≳ 2·10⁶ disclosed. Repairs: none needed (PC1 §12 TRUE). Rest unchanged.
<!-- END VERBATIM -->


#### Seat D (R2_D) M12 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:102` (verbatim) — base statement: R1_D M12 `theory_campaign/MEET-THM/R1_D.md:342`

<!-- BEGIN VERBATIM R2_D.md:102-102 -->
| M12 Theorem 1 (T03♯) — K93, K04 | Unchanged from R1 §D M12; supplement, cited in main text. | "PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2))"; T01-T03 "PROVED-LOCKED (wave 3; external review queued)" |
<!-- END VERBATIM -->


---

## TH10 (S-TARGET · Propriety, invariance, envelopes, exact branch, odds certificate)

Archive ID **TH10**; native **S-TARGET**; K-IDs K01–K05, K76, K95; lemma pack LP-FOUND, wave 1; positions [pos 1626]. Verbatim TLF section (lines 504–577):

## S-TARGET · Propriety, invariance, envelopes, exact branch, odds certificate (K01–K05, K76, K95)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:62`):** content = Propriety, invariance, envelopes, exact branch, odds certificate (K01–K05, K76, K95). Notes and decisions = K95 here (R3-4 unanimous)

K95 is here (R3-4, unanimous). Seat statements below are complementary (same content, different packaging).


#### Seat C (R2_C): C12

**Source:** `theory_campaign/MEET-THM/R2_C.md:193–202` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:193-202 -->
| C12 — K01/K02/K03/K04/K05/K76 | Final card |
|---|---|
| Final statement | For finite nonconstant standardized data, \(n\ge3,p\ge1\), the shipped ridge/IG target is proper, including rank-deficient submodels. With \(H_S=(n+1)G_S+I\), \(Q_S=Y-nz_S'H_S^{-1}z_S\), \(Q_S\ge Y/(n+1)\), and \(1\le\det H_S/\det(G_S+I)\le(n+1)^{\lvert S\rvert}\). Thus \(m(S),Z\le U_m=C_n(2b_0+Y/(n+1))^{-\nu}\), where \(C_n\) is the shipped score’s common prefactor. |
| Other clauses | Use the normalized capped prior once. Target probabilities are invariant under admissible affine rescaling and equivariant under column permutation. The contrast reduction uses IG shape \(a_0+1/2\), rate \(b_0s_y^2\). Real-arithmetic exact enumeration returns exact summaries; every fixed-\(p\) sequence eventually enters that branch. |
| Repairs | PC2 status repair; target equivariance only. The pairwise IG perturbation coefficient is \(2\nu b_0\), not universally \(nb_0\). |
| Status | N17: **PROVED**. T01: **PROVED-LOCKED (wave 3; external review queued); SAME-FAMILY-ONLY**. Remaining assembly: **PROOF SKETCH, unchecked**. |
| Placement | Supplement. |
| Route / Lean | Checked spectral envelope and reduction; finite normalization/enumeration. |
| Fallback / stop | Proper target and exact-arithmetic enumeration; no machine-certification claim. |
| IC3 | C10’s duplicated, rank-deficient correlated design. |
<!-- END VERBATIM -->


#### Seat A (R2_A) S5

**Source:** `theory_campaign/MEET-THM/R2_A.md:135` (verbatim) — base: R1_A C1 `theory_campaign/MEET-THM/R1_A.md:162`

<!-- BEGIN VERBATIM R2_A.md:135-135 -->
**S5 · Proposition TARGET (K01–K05, K76).** As R1 §D C1 with (ii) restricted to the target (affine invariance, permutation equivariance); algorithmic equivariance in law only for a tie-free partition and decision structure (PC1:301); K05 superset bound; K76 eventual exact dispatch (N12 seat-proved, unchecked); (iii) constant 2νb₀ (PC2:216; PC1:300). Status: N17 PROVED; rest D/E proposals, TRUE-AS-WRITTEN (PC1:300); T01 reduction PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY. Supplement.
<!-- END VERBATIM -->


#### Seat A (R2_A): K95 odds-certificate clause (from A's Z𝒯 card, clause (f))

**Source:** `theory_campaign/MEET-THM/R2_A.md:89` (verbatim fragments of the line; the line carries other clauses not reproduced here, marked […])

<!-- BEGIN VERBATIM FRAGMENT R2_A.md:89 -->
(f) odds certificate: π(S₀) = 1/(1+A(S₀)); A ≤ η < 1 ⇒ HPM = MPM = S₀ (PC1:130).
<!-- END VERBATIM -->


#### Seat B (R2_B) S7

**Source:** `theory_campaign/MEET-THM/R2_B.md:185–187` (verbatim) — base: R1_B D17 `theory_campaign/MEET-THM/R1_B.md:438`

<!-- BEGIN VERBATIM R2_B.md:185-187 -->
### S7 · Proposition TARGET (K01, K02, K03, K04, K95, K76) · supplement

Final statement as R1 §D D17 with: target affine-invariant and permutation-equivariant; algorithmic output need not be equivariant, even in law, under index ties (PC1 §20); A(S₀) ≤ η < 1 ⇒ HPM = MPM = S₀ (PC1 §20 NEEDS-HYPOTHESIS conceded); 2νb₀ as the exact pairwise IG constant (PC2 cluster 20). Status: N17: PROVED (PC1 claim 1); T01 reduction: PROVED-LOCKED (wave 3; external review queued); N12 eventual dispatch: seat-proved, unchecked; T26-exact-branch-paren: XF ERROR (corrected). Rest unchanged.
<!-- END VERBATIM -->


#### Seat D (R2_D) S1 and S3 rows (K95 with "η < 1 stated"), S12 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:105` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:105-105 -->
| S1 target lemmas — K01–K04 (+K76, K95 via S3/S12) | Target invariance and permutation equivariance; algorithmic equivariance in law only without partition/decision ties (cluster 20). | unchanged |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_D.md:107` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:107-107 -->
| S3 decision rules — K62 moved to H′(f); K60, K61 cited; K95, K101 | η < 1 stated (cluster 20). | unchanged |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_D.md:116` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:116-116 -->
| S12 fixed p/tiny n — K76, K02 | unchanged | N12 "seat-proved, unchecked" |
<!-- END VERBATIM -->



---

## TH11 (S-BLOCKS · Separation ⇒ groups kept; SIZE ⇒ equality)

Archive ID **TH11**; native **S-BLOCKS**; K-IDs K07, K14, K06; lemma pack LP-FOUND, wave 1; positions [pos 1626]. Verbatim TLF section (lines 581–630):

## S-BLOCKS · Separation ⇒ groups kept; SIZE ⇒ equality (K07, K14, K06)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:68`):** content = Separation ⇒ groups kept; SIZE ⇒ equality (K07, K14, K06). Notes and decisions = —

Seats agree; C11 is the fullest. A files it inside S10 (BLOCKS part), D inside the S2 row.


#### Seat C (R2_C): C11

**Source:** `theory_campaign/MEET-THM/R2_C.md:183–191` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:183-191 -->
| C11 — K07/K06/K22 | Final card |
|---|---|
| Final statement | Suppose every within-group distance is strictly smaller than every between-group distance and every group has size at most \(B\). Complete linkage forms each group before cross-group merging; cutting and whole-cluster packing preserve groups. If additionally \(B<2g_{\min}\), output blocks equal groups. For actual blocks, \(\lceil p/B\rceil\le J\le2\lceil p/B\rceil\), \(\sum_b2^{\lvert C_b\rvert}\le p2^B/B\); the symmetrized capped graph has at most \(pB\) edges and no isolated vertex when \(p>1\). |
| Repairs | PC2 Shared objects and cluster 4: replace unqualified eventual recovery by \(n\ge9^6\) for both nine-variable exhibits. PC1 cluster 6: explicit SIZE. |
| Status | PART-ThmA: **PROVED; SF none; XF VERIFIED***. Counting/graph assembly: **PROOF SKETCH, unchecked**. PART-pairing remains **OPEN**, excluded. |
| Placement | Supplement. |
| Route / Lean | Cite checked separation/packing result; finite partition, bin-count and graph-union arguments. |
| Fallback / stop | Group preservation and deterministic counts only; no size-five pairing law. |
| IC3 | W and LH satisfy strict separation and \(9\le B\le16<18\) for \(n\ge9^6\). Otherwise unchanged from R1 §D D10. |
<!-- END VERBATIM -->


#### Seat B (R2_B) S11

**Source:** `theory_campaign/MEET-THM/R2_B.md:201–205` (verbatim) — base: R1_B D21 `theory_campaign/MEET-THM/R1_B.md:484`

<!-- BEGIN VERBATIM R2_B.md:201-205 -->
### S11 · Proposition BLOCKS (K07, K14, K06) · supplement

Unchanged from R1 §D D21 (PC1 §19 B.D21 TRUE-AS-WRITTEN; preservation only, equality needs SIZE). Status: PART-ThmA: PROVED (SF: none; XF: VERIFIED* (A-REV9)); PART-pairing: OPEN; PART-CE2: COUNTEREXAMPLE.

Dropped from the list since R1: D10 (CD → remark), D20 (K94 → FUTURE_WORK).
<!-- END VERBATIM -->


#### Seat A (R2_A) S10 (KL/TV and BLOCKS; the BLOCKS part is the last clauses)

Reproduced verbatim once, under **S-IDENT** below (`theory_campaign/MEET-THM/R2_A.md:145`).


#### Seat D (R2_D) S2 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:106` (verbatim) — base: R1_D S2 `theory_campaign/MEET-THM/R1_D.md:391`

<!-- BEGIN VERBATIM R2_D.md:106-106 -->
| S2 start machinery — K06, K07, K09, K14, K22 | Graph "no isolated vertex" for p ≥ 2 (cluster 19); K07 preservation only, equality under SIZE. | unchanged |
<!-- END VERBATIM -->



---

## TH12 (S-KERNEL · N9 kernel facts, graph (p ≥ 2), start sampler, minorisation)

Archive ID **TH12**; native **S-KERNEL**; K-IDs K20, K21, K08, K09, K22, K103; lemma pack LP-FOUND, wave 1; positions [pos 1550], [pos 1593] (N9 vs production code), [pos 1626]. Verbatim TLF section (lines 634–721):

## S-KERNEL · N9 kernel facts, graph (p ≥ 2), start sampler, minorisation (K20, K21, K08, K09, K22, K103)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:63`):** content = N9 kernel facts, graph (p ≥ 2), start sampler, minorisation (K20, K21, K08, K09, K22, K103). Notes and decisions = N9 with CHK amendments. K09 is the tie-DP proposition (C10)

N9 with the CHK amendments (`evidence/CHK_INHERITED/REPORT.md` §5, VERIFIED WITH AMENDMENT). K09 is the tie-DP proposition, C10 (MINUTES). **K23 (R3-4):** FUTURE_WORK (A, B, D); C dissents and would keep the finite squared-kernel Dirichlet comparison as an attributed lemma in S-KERNEL (R3_C §S1, `theory_campaign/MEET-THM/R3_C.md:59`). Recorded; the HQ of S-KERNEL may cite it as an attributed lemma without a theorem number. The Dirichlet-form clause ℰ_Q ≥ ½ℰ_{R₂} appears in seats A (S10) and B (S5) as filed; it is K23 and is not a numbered supplement claim.


#### Seat B (R2_B) S5

**Source:** `theory_campaign/MEET-THM/R2_B.md:177–179` (verbatim) — base: R1_B D16 `theory_campaign/MEET-THM/R1_B.md:422`

<!-- BEGIN VERBATIM R2_B.md:177-179 -->
### S5 · Proposition KERNEL (K20, K21, K08, K09, K22, K23, K103) · supplement, cited lemma + Lean

Final statement as R1 §D D16 with: reversibility under the sufficient conditions of N9 (a fixed order need not be self-adjoint); the graph clause for p ≥ 2 (PC1 §19); Q_φ(S,·) ≥ π_φ/M_φ (E's constant 1/M_φ, PC1 §19 TRUE; 1/(mM_φ) also valid) and ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1 − 1/M_φ)^k with M_φ ≤ exp{φ·osc d}; ℰ_Q ≥ ½ℰ_{R₂}, R₂ = (1/m)ΣP_j²; tie-aware DP returns the prescribed maximiser (N3 OPEN, hypothesis). Status: N9K: PROVED (candidate), N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT (PC1, cross-family); T09: PROVED-LOCKED (wave 1); N3: OPEN; K22, K23, K103: PROVED (by this seat, unchecked), PC1 §19 TRUE-AS-WRITTEN. Rest unchanged.
<!-- END VERBATIM -->


#### Seat C (R2_C): C10 (K09, tie-DP proposition)

**Source:** `theory_campaign/MEET-THM/R2_C.md:166–175` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:166-175 -->
| C10 — K09 | Final card |
|---|---|
| Final statement | For positive finite block tables, size-only capped prior and exact comparisons, max-plus convolution gives the best start score at each size. Choose the smallest maximizing size. In ascending index order, include an index exactly when an optimal completion of that size consistent with the existing prefix remains possible. The result is the prescribed lexicographically smallest start maximizer. |
| Repairs | PC2 §0/D9: the new duplicate-column exhibit below puts the tie at the global start mode, not merely somewhere in a table. |
| Status | Proposed finite mathematical proposition: **PROOF SKETCH, unchecked**. Registry N3’s integrated tie-DP invariant remains **OPEN**; it is not being listed as a proved implementation theorem. |
| Placement | Supplement. |
| Route / key lemma | Optimal-completion invariant and prefix induction. |
| Lean core | Finite constrained maximization and lexicographic order. |
| Fallback / stop | Unique-maximizer instances. If the prefix invariant fails, drop the tie proposition and retain the integration gap. |
| IC3 | \(n=40,p=20\); columns 1 and 2 identical; remaining columns mutually orthogonal and orthogonal to them. Standardized \(y\) has squared correlation \(1/2\) with the duplicate direction and zero with other columns. Complete linkage keeps the duplicate pair together; adding zero-score columns decreases the start score. The two singleton duplicates are tied global modes; SMC dispatch holds. |
<!-- END VERBATIM -->


#### Seat C (R2_C): C10 allowed scratch check (reproduction, as filed)

**Source:** `theory_campaign/MEET-THM/R2_C.md:177–181` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:177-181 -->
| C10 — Allowed scratch check | Reproduction |
|---|---|
| Script, Python, `/tmp`, no seeds | `import math`<br>`n,p,Y=40,20,39`<br>`nu=.01+n/2`<br>`z2=Y*Y*.5`<br>`for k in (0,1,2):`<br>`    gain=0 if not k else n*k*z2/(1+(n+1)*k*(n-1))`<br>`    det=1 if not k else (1+(n+1)*k*(n-1))/(1+k*(n-1))`<br>`    logbf=-.5*math.log(det)-nu*math.log1p(-gain/(.02+Y))`<br>`    prior=math.lgamma(k+1)+math.lgamma(2*p-k)-math.lgamma(2*p)`<br>`    print(k, 'log_start_relative_to_empty=', round(logbf+prior,9))`<br>`print('models=',2**p,'dispatch_cutoff=',200000+64*n*p)` |
| Output | `0 log_start_relative_to_empty= 0.0`<br>`1 log_start_relative_to_empty= 7.858020937`<br>`2 log_start_relative_to_empty= 4.91339373`<br>`models= 1048576 dispatch_cutoff= 251200` |
| Interpretation | Scalar sanity check of the exhibit, not a DP implementation audit or an exact floating-point certificate. The singleton equality follows from identical columns. |
<!-- END VERBATIM -->


#### Seat C (R2_C): C15-TV (K103 minorisation / terminal-law TV)

Reproduced verbatim once, under **S-IDENT** below (`theory_campaign/MEET-THM/R2_C.md:224`–`232`).


#### Seat A (R2_A) S6 (PAR incl. K09) and S10 (minorisation, graph, Dirichlet form)

**Source:** `theory_campaign/MEET-THM/R2_A.md:137` (verbatim) — base: R1_A S1 `theory_campaign/MEET-THM/R1_A.md:489`

<!-- BEGIN VERBATIM R2_A.md:137-137 -->
**S6 · Proposition PAR (K63, K83, K84, K86, K09).** Unchanged from R1 §D S1 (Lemma S candidate; MA-PropW: PROVED (code reading; executed check); MA-Wcal: PROVED (code reading only; not executed); IND-T extension audit pending; tie-DP invariant N3 OPEN; PC2:198 TRUE-AS-WRITTEN on random instances, DESIGN-ASSERTED). Supplement.
<!-- END VERBATIM -->

A's S10 is reproduced verbatim once, under **S-IDENT** below (`theory_campaign/MEET-THM/R2_A.md:145`).


#### Seat D (R2_D) S2 and S8 rows

**Source:** `theory_campaign/MEET-THM/R2_D.md:106` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:106-106 -->
| S2 start machinery — K06, K07, K09, K14, K22 | Graph "no isolated vertex" for p ≥ 2 (cluster 19); K07 preservation only, equality under SIZE. | unchanged |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_D.md:112` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:112-112 -->
| S8 Doeblin/calculus — K103, K104, K108 | TV ≤ (1 − 1/M_φ)^L with the shipped L = max(4, ⌈log₂(n+1)⌉) → ∞; useful iff M₁ = O(1). | PC2 D15-TV TRUE |
<!-- END VERBATIM -->


#### Seat D (R2_D) validity statement (the N9 statement, H′(a))

**Source:** `theory_campaign/MEET-THM/R2_D.md:56` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:56-56 -->
- Statement. Under EX-A, EX-S, CAL, GUARD-W, R′ declared. (a) Validity: each Gibbs flip, uniform swap, neighbour swap and independence move is γ_φ-reversible, the uniformly random-order round is γ_φ-invariant and self-adjoint, draw_pi0 and Z̄₀ are exact (N9, cited); conditionally on frozen 𝓒, E[Ẑ_r] = Z, E[Ẑ_r PIP̂_rj] = Z·PIP_j (locked), and E[Ẑ_r H_r(h)] = Z·π(h) for h ∈ 𝓗 measurable in (X, y, 𝓒) (N1). Potential-run statements; the intersection inequalities P(𝒪 ∩ B) ≤ P_pot(B) transfer by Lemma RO + GUARD-W; expectations do not (D.M1(c) repair). (b) For 0 ≤ h ≤ 1, M₂ = E[W_r²|𝓒]: P(|μ̂(h) − π(h)| > ε | 𝓒) ≤ min{1, 4(M₂−1)/R′ + 4M₂/(R′ε²)} (PC1c3). (c) Joint inclusions h_A = 1{A ⊆ S} (plain averages, c_h = 0); predeclared h_I(S) = P(β_j ∈ I | S, X, y) for a finite endpoint grid, with a union bound over the grid (cluster 16 repair: no "any interval"). (d′) Growth clause: on any family with osc d = O_P(1) (model/design condition) and R′(n,p) = 4ℓ(n,p), ℓ = ⌈log₂(n+p+1)⌉, under T03♯: μ̂(h) → h(S₀) jointly with output. (e) Fixed data: μ̂(h) → π(h) a.s. as R′ → ∞ (cited). (f) MPM margin: if every exact PIP is ≥ δ from ½ and the estimated PIPs err < δ, the reported MPM equals the exact MPM (K62).
<!-- END VERBATIM -->



---

## TH13 (S-IDENT · Restricted-ESS coverage identity, TI/KL/TV calculus, C15-CI clause)

Archive ID **TH13**; native **S-IDENT**; K-IDs K25 lemma, K104, K55, K103; lemma pack LP-IDENT, wave 2; positions [pos 1614] (Q2 posterior-content reading), [pos 1626]. Verbatim TLF section (lines 725–827):

## S-IDENT · Restricted-ESS coverage identity, TI/KL/TV calculus, C15-CI clause (K25 lemma, K104, K55, K103)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:67`):** content = Restricted-ESS coverage identity, TI/KL/TV calculus, **C15-CI posterior-content credible-set clause, named** (K25 lemma, K104, K55, K103). Notes and decisions = Seat B's "missing" item 1 (R3_B §S4) adopted: HQ Q2's posterior-content reading needs a named clause

**C15-CI is named as a clause of this card** (MINUTES; B's "missing" item 1, R3_B `theory_campaign/MEET-THM/R3_B.md:314`; C's required correction, R3_C `theory_campaign/MEET-THM/R3_C.md:318`). It is the HQ Q2 deliverable: posterior-content error, not frequentist coverage (FW1). K33 is not here (M7; D's dissent recorded in MINUTES §2.3). The minorisation constant is 1/M_φ in A, B, C and D (B notes 1/(mM_φ) is also valid); compatible.


#### Seat C (R2_C): C15-TV

**Source:** `theory_campaign/MEET-THM/R2_C.md:224–232` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:224-232 -->
| C15-TV — K103 | Final card |
|---|---|
| Final statement | Under A, \(M_\phi=\max_Sq_\phi(S)/\pi_0(S)\). The complete production round minorizes \(q_\phi\) by \(1/M_\phi\), without a \(1/m\) factor. Thus a terminal particle’s marginal law after \(L\) terminal rounds has TV at most \(q^L\), \(q=1-1/M_1\). For a predeclared partition into \(d_0\) cells, \(P(TV(\widehat\pi_{\rm cell},\pi_{\rm cell})>\epsilon\mid\mathcal C)\le\min\{1,4(M_2-1)/R'+4d_0M_2/(R'\epsilon^2)\}\). |
| Repairs | PC2 cluster 16 and §0 item 4: distinguish marginal law from realized empirical law; label default-\(4\) bound vacuous. Full-state TV uses singleton cells and may be useless. |
| Status | Production-round/record assembly: **PROOF SKETCH, unchecked**. Independence-sampler foundation: **KNOWN—CITE**. |
| Placement | Supplement, one package with C15-KL/CI. |
| Route / Lean | Cite PC2’s checked minorization/vector-ratio clauses; compose minorization through invariant kernels. |
| Fallback / stop | Coarsened TV and bounded-functional error; no useful masked full-TV claim. |
| IC3 | W gives \(M_1\le e^{D_*}=O_P(1)\); §R6 supplies explicit \(L,R'\). |
<!-- END VERBATIM -->


#### Seat C (R2_C): C15-KL

**Source:** `theory_campaign/MEET-THM/R2_C.md:234–242` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:234-242 -->
| C15-KL — K103/K104 | Final card |
|---|---|
| Final statement | Under C15-TV, \(\lambda_L=(1-q^L)\pi+q^L\nu_L\). Consequently \(KL(\pi\Vert\lambda_L)\le-\log(1-q^L)\) and \(KL(\lambda_L\Vert\pi)\le q^L\log(1/\pi_{\min})\). Also \(KL(\widehat\pi\Vert\pi)\le4TV(\widehat\pi,\pi)^2/\pi_{\min}\), with the corresponding minimum cell mass for coarsenings. If any positive-posterior state is absent, \(KL(\pi\Vert\widehat\pi)=\infty\); in particular this occurs surely when \(\lvert\Omega\rvert>4NR'\). |
| Repairs | PC2 cluster 16; HQ Q3: reverse empirical KL obstruction retained, useful masked final-TV/KL not claimed. |
| Status | **PROOF SKETCH, unchecked** assembly; elementary divergence foundations cited. |
| Placement | Supplement, C15 package. |
| Route / Lean | Cite checked mixture/log-sum clauses; finite support and convexity. |
| Fallback / stop | Fixed-data directional bounds. No forward-KL convergence rate without controlling \(\pi_{\min}\); no silent smoothing. |
| IC3 | Every finite admissible correlated design for inequalities; W for terminal reverse-KL convergence. Otherwise unchanged from R1 §F D15-KL. |
<!-- END VERBATIM -->


#### Seat C (R2_C): C15-CI (the named posterior-content credible-set clause)

**Source:** `theory_campaign/MEET-THM/R2_C.md:244–253` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:244-253 -->
| C15-CI — K103 | Final card |
|---|---|
| Final statement | Under C15-TV, for any possibly output-selected union \(C\) of the chosen cells and nominal content \(1-\alpha\), \(\lvert\pi(C)-(1-\alpha)\rvert\le TV(\widehat\pi_{\rm cell},\pi_{\rm cell})+\lvert\widehat\pi(C)-(1-\alpha)\rvert\). Therefore the probability, jointly with \(\mathcal O\) under GUARD-W, that the left side exceeds \(\epsilon\) plus the observed nominal-content discrepancy is bounded by C15-TV’s tail bound. |
| Available interval | Use model-size cells, \(d_0=K+1\), and an interval selected from the existing size distribution. Discrete overshoot is retained explicitly; estimated content need not equal nominal content. |
| Repairs | HQ Q2 and PC1/PC2 cluster 16: absolute posterior-content deviation, not frequentist coverage. A pointwise fixed-\(h\) bound does not validate arbitrary selected sets. |
| Status | **PROOF SKETCH, unchecked**. |
| Placement | Supplement, C15 package. |
| Route / Lean | Simultaneous cell-law control and deterministic set-mass inequality. |
| Fallback / stop | Predeclared interval endpoints with simultaneous CDF bounds; unavailable historical records remain unavailable. |
| IC3 | W with §R6’s stacking rate and actual size-distribution records. |
<!-- END VERBATIM -->


#### Seat C (R2_C): C15 empirical TV/content and terminal-law rows (agenda 7)

**Source:** `theory_campaign/MEET-THM/R2_C.md:324` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:324-324 -->
| C15 empirical TV/content | The same \(R'_n\) handles any predeclared coarsening with \(d_0\le s^2\), including model size. It does not make singleton full-state TV informative when \(\lvert\Omega\rvert\) is exponential. |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_C.md:325` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:325-325 -->
| C15 terminal law | On W, \(M_1\le e^{D_*}=O_P(1)\); the existing logarithmic \(L\) gives terminal marginal TV and reverse-KL convergence in probability. Forward-KL convergence additionally needs control of \(\log(1/\pi_{\min})\), which is not supplied. |
<!-- END VERBATIM -->


#### Seat B (R2_B) S9

**Source:** `theory_campaign/MEET-THM/R2_B.md:193–195` (verbatim) — base: R1_B D19 `theory_campaign/MEET-THM/R1_B.md:460`

<!-- BEGIN VERBATIM R2_B.md:193-195 -->
### S9 · Proposition IDENT (K25, K104, K54, K55) · supplement

Final statement as R1 §D D19 with Λ_len := ∫₀¹ sd_{q_φ}(d)dφ ≤ √J (the length, not the cumulant Λ(1); PC1 §16 AMBIGUOUS). Status: PROVED (by this seat, unchecked); OWS-WS1: PROVED (SF: none; XF: none); PC1 §14, §16 TRUE-AS-WRITTEN. Rest unchanged.
<!-- END VERBATIM -->


#### Seat A (R2_A) S10 (exponential-family identities, Λ_len, minorisation, Dirichlet form)

**Source:** `theory_campaign/MEET-THM/R2_A.md:145` (verbatim) — base: R1_A S4 `theory_campaign/MEET-THM/R1_A.md:546`

<!-- BEGIN VERBATIM R2_A.md:145-145 -->
**S10 · Proposition KL/TV and BLOCKS (K104, K103, K07, K14, K22).** Exponential-family identities with the length Λ_len := ∫sd_{q_φ}(d)dφ ≤ √J (renamed; PC1:257); minorisation Q_φ(S,·) ≥ π_φ/M_φ (constant 1/M_φ, PC1:290; PC2:184), vacuous under masking; Dirichlet form ℰ_Q ≥ ½ℰ_{R₂} with R₂ = (1/m)ΣP_j² (PC1:289); graph: ≤ pB edges, no isolated vertex for p ≥ 2 (PC1:291); strict-gap preservation (PART-ThmA) and the SIZE equality clause; every block sub-model is scored. Supplement. Status: D/E proposals TRUE-AS-WRITTEN at the cited rows; OWS-WS1 PROVED (no review).
<!-- END VERBATIM -->


#### Seat D (R2_D) S8 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:112` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:112-112 -->
| S8 Doeblin/calculus — K103, K104, K108 | TV ≤ (1 − 1/M_φ)^L with the shipped L = max(4, ⌈log₂(n+1)⌉) → ∞; useful iff M₁ = O(1). | PC2 D15-TV TRUE |
<!-- END VERBATIM -->




---

## TH14 (S-CERT · Local search, certificate semantics, B&B soundness, perturbation lemma)

Archive ID **TH14**; native **S-CERT**; K-IDs K64, K73 (without the region-certification clause), K74, K05, K108; lemma pack LP-AUDIT, wave 3; positions [pos 1626]. Verbatim TLF section (lines 930–965):

## S-CERT · Local search, certificate semantics, B&B soundness, perturbation lemma (K64, K73 without region-certification clause, K74, K05, K108)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:64`):** content = Local search (weak local maximum, ties allowed), certificate semantics, B&B soundness, perturbation lemma (K64, K73 without the region-certification clause, K74, K05, K108). Notes and decisions = K73 per C's withdrawal (R3-8)

K73 per C's withdrawal of the operational region certification (R3-8). K107 (rounding bound) is FUTURE_WORK (N16 OPEN); K108 (deterministic perturbation lemma) stays. Seats A and B state the same card; D files it as the S9 row.


#### Seat B (R2_B) S8

**Source:** `theory_campaign/MEET-THM/R2_B.md:189–191` (verbatim) — base: R1_B D18 `theory_campaign/MEET-THM/R1_B.md:449`

<!-- BEGIN VERBATIM R2_B.md:189-191 -->
### S8 · Proposition CERT (K64, K73, K05, K108) · supplement

Final statement as R1 §D D18 with: `local_certified` = no strictly improving feasible flip or swap at the scanned centre (weak local maximum; ties allowed) (PC1 §17 COUNTEREXAMPLE conceded); B&B exact when it completes, "unresolved" otherwise, in exact arithmetic; log-mass perturbation ε ⇒ Z̃/Z ∈ [e^{−ε}, e^{ε}], TV ≤ tanh ε, winners with gap > 2ε unchanged. The rounding bound (K107) is withdrawn to FUTURE_WORK (N16 OPEN; T33-errbound COUNTEREXAMPLE). Status: N7 L1: CORRECT WITH AMENDMENT; OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9)); OCERT-C4: PROVED (XF: VERIFIED*). Rest unchanged.
<!-- END VERBATIM -->


#### Seat A (R2_A) S8

**Source:** `theory_campaign/MEET-THM/R2_A.md:141` (verbatim) — base: R1_A C16 `theory_campaign/MEET-THM/R1_A.md:432`

<!-- BEGIN VERBATIM R2_A.md:141-141 -->
**S8 · Proposition CERT (K64, K73, K74, K05, K108).** `local_certified` = no strictly improving feasible flip/swap neighbour at the scanned centre (weak local maximum; ties allowed; PC1:272); ≤ (ℓ+1) scans of ≤ p + k*(p−k*) models per search; card R (OCERT-C4 + Lemma M) exact on completion, "unresolved" on exhaustion, nothing outside U; perturbation lemma (Z̃/Z ∈ e^{±ε}, TV ≤ tanh ε, winner gap > 2ε); limitation CEX-localmax(A2), CEX2. K107 → FUTURE_WORK (N16 OPEN; T33-errbound COUNTEREXAMPLE). Status unchanged from R1 §D C16/S4. Supplement.
<!-- END VERBATIM -->


#### Seat D (R2_D) S9 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:113` (verbatim) — base: R1_D S9 `theory_campaign/MEET-THM/R1_D.md:475`

<!-- BEGIN VERBATIM R2_D.md:113-113 -->
| S9 search/certificates — K64, K73, K74, K05, K108 | K107 rounding bound → FUTURE_WORK (cluster 17); K108 deterministic perturbation lemma stays. | N16 "OPEN" |
<!-- END VERBATIM -->




---

## TH15 (S-OUT · Output-event validity, worker equivalence, stacking)

Archive ID **TH15**; native **S-OUT**; K-IDs K77, K78, K83–K86, K63; lemma pack LP-AUDIT, wave 3; positions [pos 1626]. Verbatim TLF section (lines 968–1009):

## S-OUT · Output-event validity, worker equivalence, stacking (K77, K78, K83–K86, K63)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:69`):** content = Output-event validity, worker equivalence, stacking (K77, K78, K83–K86, K63). Notes and decisions = K63/K86 are also named as premises in M1/M5

K63/K86 are also named as premises in M1 and M5. Seat B has no S-OUT card in Round 2 (R3_B places K63/K86 in hypotheses, `theory_campaign/MEET-THM/R3_B.md:60`). Cards below are complementary.


#### Seat C (R2_C): C13

**Source:** `theory_campaign/MEET-THM/R2_C.md:204–212` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:204-212 -->
| C13 — K77/K78 | Final card |
|---|---|
| Final statement | Under A and stop-only statistical coupling GUARD-W, a potential-run event \(B\) satisfying \(P(B\mid\mathcal C)\le\alpha\) gives \(P(\mathcal O\cap B\mid\mathcal C)\le\alpha\). It does not imply \(P(B\mid\mathcal O,\mathcal C)\le\alpha\). |
| Repairs | PC2 cluster 3; preserve actual statistical-output scope and the unaudited integrated coupling. |
| Status | LemmaRO: **PROVED; SF VERIFIED; XF VERIFIED***. CEX-guard: **COUNTEREXAMPLE; XF VERIFIED***. N6 potential-run: **PROVED**; output form: **CORRECT WITH AMENDMENT**. GUARD-W: **not audited**. |
| Placement | Supplement. |
| Route / Lean | Cite filed coupling/event-containment result; finite probability core. |
| Fallback / stop | Potential-run theorem while the audit remains open. Never replace it with completion-conditioned validity. |
| IC3 | Any admissible correlated input; unchanged from R1 §D D12 apart from explicit audit qualification. |
<!-- END VERBATIM -->


#### Seat D (R2_D) S4 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:108` (verbatim) — base: R1_D S4 `theory_campaign/MEET-THM/R1_D.md:420`

<!-- BEGIN VERBATIM R2_D.md:108-108 -->
| S4 worker/stacking/output — K63, K83–K86, K77, K78 | "Adaptive R′ need not preserve the bounds" (cluster 3). | unchanged |
<!-- END VERBATIM -->


#### Seat A (R2_A) S6 (PAR)

**Source:** `theory_campaign/MEET-THM/R2_A.md:137` (verbatim) — base: R1_A S1 `theory_campaign/MEET-THM/R1_A.md:489`

<!-- BEGIN VERBATIM R2_A.md:137-137 -->
**S6 · Proposition PAR (K63, K83, K84, K86, K09).** Unchanged from R1 §D S1 (Lemma S candidate; MA-PropW: PROVED (code reading; executed check); MA-Wcal: PROVED (code reading only; not executed); IND-T extension audit pending; tie-DP invariant N3 OPEN; PC2:198 TRUE-AS-WRITTEN on random instances, DESIGN-ASSERTED). Supplement.
<!-- END VERBATIM -->




---

## TH16 (S-Z · Evidence variance, masked tails)

Archive ID **TH16**; native **S-Z**; K-IDs K37–K41, K53; lemma pack LP-REST, wave 4; positions [pos 1626]. Verbatim TLF section (lines 1012–1047):

## S-Z · Evidence variance, masked tails (K37–K41, K53)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:61`):** content = Evidence variance, masked tails (K37–K41, K53). Notes and decisions = Terminal-off clause only in the exception-probability form

The seats differ on the variance clause: A (clause (vii)) and B (clause (vi)) state Var(Ẑ_r/Z | 𝒞) ≤ (T+1)e^{2D}/N with D = osc_Ω d; D (S6 row) states Var(W_r|𝓒) ≤ e^{2·osc_Ω d} − 1 (pathwise bound, PC2 D14), "replaces the (T+1)e^{2D}/N form". R3_D §S1 confirms D's form (`theory_campaign/MEET-THM/R3_D.md:36`); R3_B §S1 keeps "(vii) with D = osc_Ω d ≤ D_*" (`theory_campaign/MEET-THM/R3_B.md:52`). Wording: see "Chair's choices" item 3 (both bounds ship). The terminal-off clause is in the exception-probability form in all three (MINUTES).


#### Seat A (R2_A) S4

**Source:** `theory_campaign/MEET-THM/R2_A.md:133` (verbatim) — base: R1_A C6 `theory_campaign/MEET-THM/R1_A.md:257`

<!-- BEGIN VERBATIM R2_A.md:133-133 -->
**S4 · Proposition Z (K37–K41, K53).** (i) E[Ẑ_r \| 𝓒] = Z, E[log Ẑ_r] ≤ log Z, P(0.05Ẑ > Z) ≤ 0.05 (cited). (ii) exact variance identity (OPW2 Thm A, as a specialisation of CDG 2011 Thm 1.4 in kind); the exact-refresh product never substituted (OPW2-cex). (iii) masked lower tail: islands whose terminal population is off S₀ have Ẑ_r ≤ √δ₁Z **except on an event of probability ≤ 2√δ₁** (source form, PC1:247; divided by κ if conditioned on an off-event of probability κ); PC1 claim 4 wording mandatory. (iv) Ẑ < Z_𝒯 ⇒ Ẑ < Z. (vi) favourable Ẑ/Z → 1 under (P1) (remark). (vii) Var(Ẑ_r/Z \| 𝓒) ≤ (T+1)e^{2D}/N with D := osc_Ω(d), deterministic, bounded by §R3(a) (PC1:249). Status unchanged from R1 §D C6 (FMP-Na: PROVED (XF: GAP (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; (vii) E proposal unchecked). Supplement.
<!-- END VERBATIM -->


#### Seat B (R2_B) S4

**Source:** `theory_campaign/MEET-THM/R2_B.md:173–175` (verbatim) — base: R1_B D12 `theory_campaign/MEET-THM/R1_B.md:355`

<!-- BEGIN VERBATIM R2_B.md:173-175 -->
### S4 · Theorem Z, evidence variance (K39, K40, K38, K37, K41, K53) · supplement

Final statement as R1 §D D12 with: (ii) in the exception-probability form, P(Ẑ_r > √δ₁Z on a terminal-off island) ≤ 2√δ₁ (÷κ if conditioned on an off event of probability κ) (PC1 §15 COUNTEREXAMPLE conceded); the E1/E2 path-tail clause imported with its full hypotheses (A, x_m, τ_A, D_A, exceptions) or omitted; (vi) Var(Ẑ_r/Z\|𝓒) ≤ (T+1)e^{2D}/N with D a deterministic full-space range bound (D = osc d ≤ D_* under §R3(a)). Status: OPW2-ThmA: PROVED (SF: none; XF: VERIFIED (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; FMP-Na: PROVED (SF: none; XF: GAP (A-REV9)); PC1c4: PROVED; T26-ThmA: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)); T26 overall CONJECTURE. Novelty of (i) vs Cérou–Del Moral–Guyader Thm 1.4 unchecked (LIT-SMC §3A: "needs escalation"). Rest unchanged.
<!-- END VERBATIM -->


#### Seat D (R2_D) S6 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:110` (verbatim) — base: R1_D S6 `theory_campaign/MEET-THM/R1_D.md:446`

<!-- BEGIN VERBATIM R2_D.md:110-110 -->
| S6 evidence variance — K37–K41, K53 | Terminal-off clause in exception-probability form; Var(W_r|𝓒) ≤ e^{2·osc_Ω d} − 1 (pathwise bound, PC2 D14) replaces the (T+1)e^{2D}/N form; envelope per M3′(d). | OPW2-ThmA "PROVED (SF: none; XF: VERIFIED (A-REV9))"; MZ-E1E2 "PROVED (E1, E2)" candidate |
<!-- END VERBATIM -->




---

## TH17 (S-POOL · Pooling rules, the checked recording-marginal equal-weight bias comparison P1, R_eff)

Archive ID **TH17**; native **S-POOL**; K-IDs K49, K50, K54, K56, K57-P1; lemma pack LP-REST, wave 4; positions [pos 1626]. Verbatim TLF section (lines 1050–1099):

## S-POOL · Pooling rules, the checked recording-marginal equal-weight bias comparison P1, R_eff (K49, K50, K54, K56, K57-P1)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:66`):** content = Pooling rules, the checked recording-marginal equal-weight bias comparison P1, R_eff (K49, K50, K54, K56, K57-P1). Notes and decisions = General K57 accuracy → FW (B, C; R3-8)

General K57 accuracy → FUTURE_WORK (B, C; R3-8). C has no R2 card (cites). Seats are compatible; P1 is stated for the uniformly sampled recording-state / one-record marginal in all three.


#### Seat B (R2_B) S10

**Source:** `theory_campaign/MEET-THM/R2_B.md:197–199` (verbatim) — base: R1_B D14 `theory_campaign/MEET-THM/R1_B.md:393`

<!-- BEGIN VERBATIM R2_B.md:197-199 -->
### S10 · Proposition PIP-eq (K49, K50, K57; K59 FUTURE_WORK) · supplement

Final statement as R1 §D D14 with the TV clause on the uniformly sampled one-record marginal of the delivered population (PC1 §14 AMBIGUOUS) and the splitting clause labelled exact-refresh idealisation. Status: MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); MZ-P1P2: P1 PROVED; MA-CorV: PROOF SKETCH. Rest unchanged.
<!-- END VERBATIM -->


#### Seat A (R2_A) S7

**Source:** `theory_campaign/MEET-THM/R2_A.md:139` (verbatim) — base: R1_A C4 `theory_campaign/MEET-THM/R1_A.md:219`; S2 `theory_campaign/MEET-THM/R1_A.md:508`

<!-- BEGIN VERBATIM R2_A.md:139-139 -->
**S7 · Proposition POOL (K49, K50, K54, K56, K57; K47, K55 cited).** As R1 §D C4 (i), (iii)–(vi) and S2 P1, with (ii) moved to M2(b) and 0 ≤ h ≤ 1 (PC1:240); P1 stated for the uniformly sampled recording-state marginal (PC1:237); "iff delivered" dropped. Status unchanged (MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); ADRAFT-ThmA Astra-only, cite Del Moral; MZ-P1P2: P1 PROVED; OBG-LH-lock-general: XF ERROR). Supplement.
<!-- END VERBATIM -->


#### Seat D (R2_D) S5 and S7 rows

**Source:** `theory_campaign/MEET-THM/R2_D.md:109` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:109-109 -->
| S5 pooling — K47 cited, K48–K50, K54, K56 | unchanged | unchanged |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_D.md:111` (verbatim) — base: R1_D S5 `theory_campaign/MEET-THM/R1_D.md:434`, S7 `theory_campaign/MEET-THM/R1_D.md:457`

<!-- BEGIN VERBATIM R2_D.md:111-111 -->
| S7 equal-weight P1 — K57 | unchanged (bias ≤ TV of the one-record marginal, cluster 14) | MZ-P1P2 "P1 PROVED; P2 PROVED as a composition" |
<!-- END VERBATIM -->


#### Seat C (R3_C §S1) objection to unrestricted K57 accuracy (for the record)

**Source:** `theory_campaign/MEET-THM/R3_C.md:36` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:36-36 -->
| §2.2 S-POOL | Object to unrestricted K57 accuracy | Retain the checked recording-marginal bias comparison; general fixed-budget equal-weight accuracy remains FUTURE_WORK. W2P1 B.S10 verifies that narrower scope. | A checked estimator-level theorem for the actual records and budgets. |
<!-- END VERBATIM -->



---

## TH18 (S-LIM · Limitations as theorems; K99 qualitative remark)

Archive ID **TH18**; native **S-LIM**; K-IDs K79, K81, K100, K101 (K74 per seat B); lemma pack LP-REST, wave 4; positions [pos 1280], [pos 1626]. Verbatim TLF section (lines 1103–1138):

## S-LIM · Limitations as theorems (K79, K81, K100, K101); K99 qualitative remark

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:65`):** content = Limitations as theorems (K79, K81, K100, K101); K99 qualitative remark. Notes and decisions = Duplicates: PIP = E[# selected in group]/d; numeric limits only with their p qualification

Duplicates clause (MINUTES; SYNTH_R2 §3): PIP = E[# selected in group]/d; the numeric limit 2/3 only for p = 2; with an orthogonal null it is 3/5; numeric limits only with their p qualification. The seats distribute clauses differently (A puts the weak-local-maximum limitation CEX-localmax in S-CERT; B has it as (b) here and K74 here; MINUTES places K74 in S-CERT); the duplicates clause is identical. C cites these.


#### Seat B (R2_B) S6

**Source:** `theory_campaign/MEET-THM/R2_B.md:181–183` (verbatim) — base: R1_B D15 `theory_campaign/MEET-THM/R1_B.md:406`

<!-- BEGIN VERBATIM R2_B.md:181-183 -->
### S6 · Proposition LIM (K79, K74, K81, K100, K101; K99 remark) · supplement

Final statement: (a) no transcript diagnostic certifies absence of an unqueried mode; (b) a certified weak local maximum can be far below the mode; (c) ESS = N throughout is compatible with genealogical collapse; (e) d exact duplicates: by symmetry PIP = E[number selected in the group]/d; the limit is 1/d only if exactly one is included asymptotically; under the ridge/BB target with two duplicates and fixed noise it is 2/3, group inclusion → 1; (f) MPM may exceed K; (g′) qualitative barrier: SHARE-PB's k-way contrast construction, as a remark. Repairs: (e) corrected (PC1 §18 COUNTEREXAMPLE conceded); (d) withdrawn (IMPLAUSIBLE); (g) withdrawn with K80 (FUTURE_WORK). Status: CEX-localmax(A2), CEX2, CEX-ESSneutral(A3), PropD-T03, SHARE-PB: COUNTEREXAMPLE (constructions); INP I5 PROVED. Rest unchanged from R1 §D D15.
<!-- END VERBATIM -->


#### Seat A (R2_A) S9

**Source:** `theory_campaign/MEET-THM/R2_A.md:143` (verbatim) — base: R1_A S3 `theory_campaign/MEET-THM/R1_A.md:527`

<!-- BEGIN VERBATIM R2_A.md:143-143 -->
**S9 · Proposition LIM (K79, K81, K100, K101).** (a), (b), (d) unchanged from R1 §D S3. (c) duplicates: d interchangeable columns have equal PIPs with PIP = E[number selected in the group]/d; the limit is 1/d only if exactly one is included asymptotically; under the ridge/BB target with two duplicates and fixed noise the limit is 2/3 (PC1:281); group inclusion → 1. Supplement.
<!-- END VERBATIM -->


#### Seat D (R2_D) S11 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:115` (verbatim) — base: R1_D S11 `theory_campaign/MEET-THM/R1_D.md:493`

<!-- BEGIN VERBATIM R2_D.md:115-115 -->
| S11 limitations — K79, K81, K99 (qualitative), K100 (corrected) | Duplicates: PIP = E[#selected in group]/d (cluster 18). | unchanged |
<!-- END VERBATIM -->




---

## TH19 (S-REP · Run-card reporting corollary: Ĵ (B/C/D form) and ε̂_× with companions)

Archive ID **TH19**; native **S-REP**; K-IDs K104/K11 reporting corollary (using K46/K52/K102); lemma pack LP-REP, wave 4; positions [pos 1608]/[pos 1614] (Q4: reporting allowed), [pos 1626], [pos 1639]. Verbatim TLF section (lines 1195–1244):

## S-REP · Run-card reporting corollary: Ĵ (B/C/D form) and ε̂_× with companions

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:72`):** content = Run-card reporting corollary: Ĵ (B/C/D form) and ε̂_× with companions. Notes and decisions = Final card `R3_C.md` §S2 S-REP. **ū̂ is D's global block-table envelope ū̂ = Σ_b max_{U⊆C_b} x_b(U)**, not a maximum over V (C's objection, R3_C §S1, adopted, since a maximum over V ⊊ Ω does not bound all fits)

Final card is R3_C §S2 S-REP (R3-6, unanimous: A withdrew its TI form). **ū̂ is D's global block-table envelope** ū̂ = Σ_b max_{U⊆C_b} x_b(U), not a maximum over V (C's objection, R3_C §S1, adopted; a maximum over V ⊊ Ω does not bound all fits). The card below already states the global envelope ("a conservative global envelope, not a maximum over V"); the earlier R2 wording "maximal fit fraction on V" (SYNTH_R2 §2.5; D:182) is withdrawn. Growth rates for the informative regime: the two stacking configurations of MINUTES §2.3 §2.6. d is a default member of 𝓗 (AMENDMENT_HQ_02). The accumulator is read-only (HQ Q4).


#### Final card (R3_C §S2 S-REP)

**Source:** `theory_campaign/MEET-THM/R3_C.md:208–243` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:208-243 -->
### S-REP — run-card reporting corollary

| Card field | Final content |
|---|---|
| IDs | **S-REP: K104/K11 reporting corollary**, using M1/K46/K52 and M2/K102. |
| Hypotheses | D0, EX-A and the MC contract. \(d\) is fixed from data, blocks and tables before final randomness. Let \(D=\max_\Omega d-\min_\Omega d\), \(W_r=\widehat Z_r/Z\), \(M_2=E(W_r^2\mid\mathcal C)\). |
| Implementation premises | Read-only initial and measured-endpoint discrepancy accumulators; no new draws, transitions or scores; no feedback. Existing values are read when available. Missing historical records yield NA. Integrated accumulator and extended-stream fidelity require audit. |
| Initial records | \(A_r=N^{-1}\sum_{i=1}^Nd(S^{(0)}_{ri})\), using each final island’s initial iid start particles. Initial particles are not reweighted by final island evidence. |
| Endpoint records | \(B_r=(4N)^{-1}\sum_{k=1}^4\sum_{i=1}^Nd(S^{(k)}_{ri})\), at the four prescribed measured endpoints. These are plain discrepancies, not marginal RB PIP records. |
| Estimator | \(\displaystyle\widehat J=\frac{\sum_{r=1}^{R'}\widehat Z_rB_r}{\sum_{r=1}^{R'}\widehat Z_r}-\frac1{R'}\sum_{r=1}^{R'}A_r.\) Preserve its signed value. **Evidence:** W2P2 §4, “§R5 · Ĵ definition”, COMPLIANT; W2P1 B.R5(i), T1–T4. |
| Target identity | \(J=KL(\pi\Vert\pi_0)+KL(\pi_0\Vert\pi)=E_\pi d-E_{\pi_0}d\). **Evidence:** W2P2 §4, “C16 · Ĵ theorem”; W1P1 §16. |
| Finite-\(R'\) statement | For \(\epsilon>0\), \(P(|\widehat J-J|>\epsilon\mid\mathcal C)\le\min\{1,4(M_2-1)/R'+16D^2M_2/(R'\epsilon^2)+D^2/(R'N\epsilon^2)\}\). **Evidence:** W2P2 §4, C16 theorem; W2P1 D.R5(i), T1–T3. |
| Limits and zero range | Fixed data/calibration: \(\widehat J\to J\) almost surely under independent stacking. If \(D=0\), both equal zero. On W, the adopted explicit stacking configurations yield consistency using \(D\le D_*=O_P(1)\), \(M_2\le e^{D_*}\). **Evidence:** W2P2 §4 and §6, C16. |
| Bound disclosure | The bound can equal one at default \(R'=4\), as in W2P2’s check; there is no default-budget accuracy or diagnostic-power promise. A large true \(J\) does not ensure a large observed \(\widehat J\). |
| Output form | Under GUARD-W, replace the failure event by \(\mathcal O\cap\{|\widehat J-J|>\epsilon\}\) with the same upper bound. **Evidence:** W1P2 cluster 3, D12; W2P2 §6, C16. |
| Numerical label | **“Post hoc Monte Carlo estimate of Jeffreys divergence; not a certificate; floating-point error unvalidated.”** Report nats. The exact branch may report NA for this bridge diagnostic. |
| Correlation proxy | \(\displaystyle\widehat\varepsilon_\times=\max_{b\ne c,\ j\in C_b,\ k\in C_c}|X_j^\top X_k|/(n-1)\), empty maximum zero; field `cross_block_rmax`. **Evidence:** W2P2 §4, proxy definition, COMPLIANT. |
| Proxy label | **“Descriptive maximum cross-block correlation proxy; not signal leakage or a confidence bound; floating-point error unvalidated.”** |
| Global companions | \(\widehat\kappa=\min_b\lambda_{\min}(G_{C_b}/(n-1))\). If positive, \(\widehat\delta=(K-1)\widehat\varepsilon_\times/\widehat\kappa\). Let \(\widehat{\bar u}=\sum_b\max_{U\subseteq C_b}x_b(U)\), using already available block-score gains. This is a conservative global envelope, not a maximum over \(V\). |
| Companion domain | Require \(\widehat\kappa>0,\ \widehat\delta<1,\ \widehat{\bar u}<1,\ \widehat\delta\widehat{\bar u}<(1-\widehat\delta)(1-\widehat{\bar u})\). Otherwise print derived \(\widehat\eta\) as **“n/a”**. **Evidence:** W2P1 D.R5(ii), T4/T5; B.R5(ii) repair; SYNTH_R2 §3. |
| Derived envelope | Put \(\widehat r=\widehat\delta\widehat{\bar u}/[(1-\widehat\delta)(1-\widehat{\bar u})]\), \(\widehat\eta=K\log(1/(1-\widehat\delta))+\nu\log(1/(1-\widehat r))\). On the domain, \(\sup_{S\in\Omega}|d(S)-d_\sigma(S)|\le\widehat\eta\). **Evidence:** W2P1 D.R5(ii), T4/T5. |
| Per-model norm clause | For nonempty \(S\), the standardized cross-block relative norm obeys \(\varepsilon_S\le(|S|-1)\widehat\varepsilon_\times/\widehat\kappa\). Treat the empty model separately with norm zero. **Evidence:** W2P1 D.R5(ii), T4/T5. |
| Regularized proxy bounds | With \(G_D\) block diagonal, \(E=G-G_D\), \(A_D=G_D+I\), \(H_D=(n+1)G_D+I\): \(\delta_A\le\frac{(n-1)(p-1)\widehat\varepsilon_\times}{1+(n-1)\widehat\kappa}\), \(\delta_H\le\frac{(n^2-1)(p-1)\widehat\varepsilon_\times}{1+(n^2-1)\widehat\kappa}\). **Evidence:** W2P2 §4, C16 proxy theorem. |
| Scope of derived bounds | M2 still requires its full matrix/residual domain. Restricted-set calculations remain restricted-set calculations. Neither a lower bound of order \(n\widehat\varepsilon_\times|\beta_j\beta_k|\) nor global rescaling from \(V\) survives W2P1. |
| Guarantee | The permitted reporting fields have precise mathematical targets and qualified error bounds without influencing the sampling procedure. |
| Goals | Objective (1); proposal §5.3 discrepancy reporting, §5.4 approximation and §13.1 bounded expectations; HQ Q4. No separate Song–Liang theorem-equivalence claim. |
| Status/self-check flag | Reporting assembly: **PROOF SKETCH, unchecked**. N1: **PROOF SKETCH**. PC1c3: **PROVED**, with N1 as premise. W2P2 C16 and repaired W2P1 T4/T5 are statement/route checks, not a full proof upgrade. |
| Fidelity | Reporting amendment authorized by Q4, to be recorded in AMENDMENT_HQ_02. Per-particle \(d\) values exist during execution but are not currently retained. Historical availability is not inferred. No machine-certified bound is claimed. |
| Novelty/citation | **MODEST/NEW-COMP** reporting consequence. Independent-system evidence weighting is established in [Dai–Heng–Jacob–Whiteley, §4.2](https://arxiv.org/html/2007.11936v3). The Jeffreys identity and norm inequalities are foundations; matching the prescribed initial and endpoint records is the contribution. |
| Proof route/key lemma | Apply M1 to globally range-scaled \(d\); split the error between endpoint ratio and initial mean. Use Popoviciu, Chebyshev and a union bound without assuming independence between those two estimates. Proxy bounds use row sums and block eigenvalues. |
| Difficulty/Lean core | Routine mathematics; moderate accumulator audit. Lean: finite ratio bound, variance/union inequalities, range scaling, empty-set conventions and row-sum norm bounds. |
| Dependencies | M1; M2 for informative W rates; M3 for discrepancy definitions; S-KERNEL for exact initialization; S-OUT for delivered-event transfer. |
| Risk | Wrong endpoint timing; final-evidence weighting of initial particles; using \(V\)-range globally; invalid residual domain; interpreting a descriptive proxy as coefficient leakage or flag power. |
| Fallback/stop rule | Retain precisely labelled descriptive fields if quantitative proof closure fails. If records are unavailable, report NA. Stop after one failed proof/audit repair cycle; remove quantitative reporting claims. Failure inherited from N1 or M2 triggers their binding-goal escalation, not a silent waiver. |
| IC3 exhibit/check | W has \(\widehat\kappa=3/4\), bounded discrepancy/moments and actual SMC dispatch. W2P2 `w_family.py` checks its proxy bounds; `jhat_mc.py` checks the estimator on a coded-grid component replica. W2P1 T4/T5 checks the global-envelope version. |
| Numerical companion | None newly run. Proposed: at most ten seeds on enumerable correlated component designs; compare exact \(J\), accumulated endpoint/start means and analytic proxy bounds. Replay identical streams with reporting enabled/disabled to test zero feedback. Report NA rather than reconstruct absent historical accumulators. |
<!-- END VERBATIM -->



---

## TH20 (S-LEAK · B's leakage clauses (F), (S) as a supplementary corollary to M2)

Archive ID **TH20**; native **S-LEAK**; K-IDs Seat B (b5)(b6) fragments; lemma pack LP-REP, wave 4; positions [pos 1626]. Verbatim TLF section (lines 1141–1192):

## S-LEAK · B's leakage clauses (F), (S) as a supplementary corollary to M2

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:71`):** content = B's leakage clauses (F), (S) as a supplementary corollary to M2. Notes and decisions = R3-5, unanimous

R3-5, unanimous. (F), (S) are non-perturbative / different scale; they are not part of HQ's (a)(b)(c); (b5)'s pathwise bound stays in M2 (R3_B `theory_campaign/MEET-THM/R3_B.md:142`). R3_C: "Preserve all inherited hypotheses; no positive uniform q₂(S₀) conclusion" (`theory_campaign/MEET-THM/R3_C.md:123`). Seats B and D state (S) differently: B adds the lower bound m ≥ π₀(S₀)e^{−2·osc d}; D states the exact identity 1 + χ²(π‖π₀) = π(S₀)²/(π₀(S₀)q₂(S₀)) and that m has no design-uniform lower bound. Only B states (F). See "Chair's choices" item 4 (compatible; both ship).


#### Seat B (R2_B): clause (S) — the m-form, a fragment of the (b5) clause in the §R3 card

**Source:** `theory_campaign/MEET-THM/R2_B.md:216` (verbatim fragments of the line; the line carries other clauses not reproduced here, marked […])

<!-- BEGIN VERBATIM FRAGMENT R2_B.md:216 -->
and max_t χ²(q_{φ_t}‖q_{φ_{t−1}}) ≤ 1/m² − 1, m := min{π₀(S₀), q₂(S₀)} ≥ π₀(S₀)e^{−2·osc d}.
<!-- END VERBATIM -->


#### Seat B (R2_B): clause (F) — fragment (b6) of the same row

**Source:** `theory_campaign/MEET-THM/R2_B.md:216` (verbatim fragments of the line; the line carries other clauses not reproduced here, marked […])

<!-- BEGIN VERBATIM FRAGMENT R2_B.md:216 -->
(b6) Favourable start under leakage: G, R, SE-blk(φ₀), EBM(M_n), CBL(η), η < η_A ⇒ 1 − π₀(S₀) = O_P(2^B√log n·n^{−κ}).
<!-- END VERBATIM -->


#### Seat B (R2_B): status fragments for (S), (F), m-bound (third column of the same row)

**Source:** `theory_campaign/MEET-THM/R2_B.md:216` (verbatim fragments of the line; the line carries other clauses not reproduced here, marked […])

<!-- BEGIN VERBATIM FRAGMENT R2_B.md:216 -->
OWS-WS6(b): PROVED (SF: none; XF: none), PC1 B.D6(S) TRUE; […] the m lower bound: PROVED (by this seat, unchecked; q₂(S₀)/π₀(S₀) = e^{2d(S₀)}/E_{π₀}e^{2d}). […] (b6) OWS-WS53F: PROVED-UNDER (SF: none; XF: none); PC1 B.D6(F) TRUE / DESIGN-VERIFIED (D_B).
<!-- END VERBATIM -->


#### Seat D (R2_D): the non-perturbative layer (its form of (S))

**Source:** `theory_campaign/MEET-THM/R2_D.md:136` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:136-136 -->
Non-perturbative layer (any ε, every grid; Seat B's (S), PC1 TRUE-AS-WRITTEN): χ²(q_{φ_t}‖q_{φ_{t−1}}) ≤ 1/m² − 1 with m = min{π₀(S₀), q₂(S₀)}, exact 1 + χ²(π‖π₀) = π(S₀)²/(π₀(S₀)q₂(S₀)); m has no design-uniform lower bound (q₂ route IMPLAUSIBLE uniformly, PC1).
<!-- END VERBATIM -->


#### Seat A (R2_A) D4 row (A places B's (F),(S) in a leakage supplement; states no clause)

**Source:** `theory_campaign/MEET-THM/R2_A.md:20` (verbatim)

<!-- BEGIN VERBATIM R2_A.md:20-20 -->
| D4 | amend | One merged package (§R3): WS3/WS4 route, now VERIFIED cross-family (CHK:13–14), with C's pathwise M₂ ≤ e^{osc d} clause (PC2:125) and B's (F),(S) clauses as a leakage supplement. Concede A.C9(c) "hence within" (PC1:138), the exhibit (PC1:142), the (e) "iff" (PC1:141). B's (N) and q₂ lemma not adopted (PC1:145, 147). | A proof of B's q₂ tilt-tail lemma would add a non-perturbative clause. |
<!-- END VERBATIM -->




---

## TH21 (S-STGI · DISSOLVED, not a list item)

Header table row (TLF line 37): "**Dissolved** (MINUTES §2.2): K30 = M7(d); K29 → FW23 (its conditional implication is citable as an attributed lemma)". MINUTES §2.2 (corrected 2026-11-04 after the registrar's cross-check): **A (R3_A:43, "object: dissolve"), B (FW) and C (R3_C §S1) prevail; dissent: D ("confirm K29 here")**; reason: "(LL) is not a model/design condition, and no family exhibits it (W2PC1 A.S11, DESIGN-ASSERTED/GAP). v1 of these minutes misreported A's position". Seat texts for K29/K30 are kept in TLF lines 830–926 "for reference only; they are not list claims" (not reproduced here; the K30 clause lives in M7(d), TH07). Status of the dissolved item: K29 = FUTURE_WORK CJ23 (FW23); K30 = clause (d) of TH07.

---

## TH22 (Thesis CD, K96 · scoped remark after the main theorems)

Verbatim TLF Part III (lines 1250–1294) and the chair's choice (item 5 of "Chair's choices": "Use **Seat C's** scoped wording"). MINUTES §2.1: "Thesis CD (K96): a scoped remark after the main theorems, unanimous since Round 2."

## Thesis CD (K96): scoped remark after the main theorems

MINUTES §2.1: "a scoped remark after the main theorems, unanimous since Round 2." The R3 files only reconfirm (R3_A:26; R3_B:44; R3_C:28; R3_D:28). The scoped wording is in the Round 2 files; four wordings, labelled by seat. See "Chair's choices" item 5 (C's wording).

### Seat A (R2_A, agenda item 6)


**Source:** `theory_campaign/MEET-THM/R2_A.md:204` (verbatim)

<!-- BEGIN VERBATIM R2_A.md:204-204 -->
**Item 6, thesis scope (CD).** Fixed data: M1 identities, M2(a)–(f), M5, M3(b) (all finite inequalities). Asymptotic: M2(g), M6(b1-LH), S1, S2, the ideal-grid depth laws. Favourable vs masked: M1, M2(a), M3, M5 are regime-free; depth laws differ by regime (M7(d) vs S11); selection is proved only on masked LH (M6). The sentence not a corollary of other cards: none. CD is a **remark** ("correlation enters the guarantees only through (δ₁, osc d_σ, η_Ω, A₀), each computable from (X, y); it enters no identity and no limit"), placed after M8.
<!-- END VERBATIM -->


### Seat B (R2_B, agenda item 6)

**Source:** `theory_campaign/MEET-THM/R2_B.md:252` (verbatim)

<!-- BEGIN VERBATIM R2_B.md:252-252 -->
**Item 6, thesis scope.** Remark only (concede D2). Scope of the remark: fixed data for (a) identities and (c) particle cost (M₂ ≤ e^{osc d}, R′ ≍ e^{osc d}/ε²), both for every X; depth (b) is a fixed-data bound T ≤ P + ⌈osc_V d/0.3246⌉ + 1 plus the ideal-grid crossing law log₂A₀ + O(1); selection (d) is asymptotic, favourable (b6 start, T03♯) or masked (HPM b1-LH) on separate sequences. Candidate non-corollary sentence "correlation increases depth and M₂" is false (non-monotone: R1 check, PC1 §11); the true non-monotone sentence is Proposition NEC's cancellation point. So: no theorem.
<!-- END VERBATIM -->


### Seat C (R2_C, §R6 agenda 6 table)

**Source:** `theory_campaign/MEET-THM/R2_C.md:312–317` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:312-317 -->
| §R6 — Agenda 6: thesis scope | Final wording |
|---|---|
| K96 disposition | **Remark only.** There is no retained non-corollary thesis sentence. |
| Fixed data | For each admissible finite input and successful frozen calibration, the idealized start, kernels and unnormalized identities target the specified posterior. Normalized finite-run posterior estimates are not generally unbiased or exact. Independent stacking gives fixed-data consistency for the stated records. |
| Asymptotic accuracy | Exact-target selection uses C9’s model/design conditions. Growing-dimensional summary accuracy is established by the proposed C1/C2 assembly on W with explicit stacking. Masked output/store accuracy uses LH and LS0 with output/retention premises. These are separate scopes. |
| Correlation and cost | Dependence affects the start discrepancy, available bounds and search difficulty. The results do not prove that correlation only increases cost, that all correlated designs admit polynomial accuracy budgets, or that the posterior itself remains statistically consistent under arbitrary correlation. |
<!-- END VERBATIM -->


### Seat D (R2_D, agenda item 6)

**Source:** `theory_campaign/MEET-THM/R2_D.md:186` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:186-186 -->
**Item 6, thesis theorem.** Scope: fixed data for the identities and finite-R′ bounds (H′(a),(b)); asymptotic for depth and selection (STG′(c), Theorem 5(b1-LH), SL′), with favourable and masked families kept on separate sequences. There is no sentence of CD that is not a corollary of H′, STG′, WS′, Theorem 5 and SL′ (the candidate "ε ↦ (d, χ²_t, T, M_φ) is continuous at 0 while ε ↦ P(𝒪 ∩ {Ŝ ≠ S₀}) is bounded through the same quantities" is WS′(b) plus Theorem 5(0)). **Remark only**, placed as the organising paragraph of the main text. "Never correctness" = H′(a); "costs depth" = STG′ + WS′(b)(iii); "costs particles/islands" = H′(b) with M₂ ≥ 1/P_𝓒(cross) disclosed and M₂ ≤ e^{osc d} where (a) applies; not monotone in correlation, never conditional on output.
<!-- END VERBATIM -->


**Chair's choices (TLF lines 1333–1349, verbatim)**

## Chair's choices (editorial; MINUTES §2 decides content, these fix wording only)

The chair does not vote. Each choice below keeps every clause the checks found TRUE-AS-WRITTEN. Where two seats' forms are compatible, both ship. Where they say the same thing, one wording is chosen and the other is kept in the cited R2 file.

1. **K29.** Superseded by the corrected MINUTES §2.2: S-STGI is dissolved and K29 is FUTURE_WORK FW23. Its conditional implication, under (LL) or the over-tilted q_w bound, may be cited as an attributed lemma. B's STG(f) wording is the reference text. Dissent: D.
2. **K30.** Stated once, as M7(d) in the final M7 card (`R3_A.md` M7, labelled ideal two-state grid). The other seats' wordings (C14, A S11, D STG′(c)) are references for the M7 HQ.
3. **S-Z, variance.** **Both bounds ship**, as two clauses:
   - (vii-a) Var(Ẑ_r/Z | 𝒞) ≤ (T+1)·e^{2D}/N, with D = osc_Ω d, the deterministic full-space range (A S4(vii), B S4(vi); wave-1 repair);
   - (vii-b) Var(W_r | 𝒞) ≤ e^{2·osc_Ω d} − 1 (D S6; it follows from the pathwise bound W_r ∈ [e^{−osc d}, e^{osc d}] checked by PC2, W2_PC2 C2 rows).

   Their minimum is the reported bound. (vii-b) is the checked fallback if (vii-a)'s 1/N route fails in the LP-REST HQ.
4. **S-LEAK, (F) and (S).** Ship:
   - (F) as B states it (`R2_B.md` §R3 (b));
   - (S) as D's exact identity 1 + χ²(π‖π₀) = π(S₀)² / (π₀(S₀)·q₂(S₀)), **plus** B's data-dependent bound m ≥ π₀(S₀)·e^{−2·osc d}, **with** D's caveat that m has no design-uniform lower bound.

   These are compatible. W2_PC1 B.R3(b)(5),(6) finds the m bound TRUE pointwise, and the q₂ route withdrawn. No uniform positive q₂(S₀) conclusion is made (R3_C).
5. **Thesis CD (K96), remark wording.** Use **Seat C's** scoped wording (`R2_C.md` §R6 agenda 6 table): "Remark only; there is no retained non-corollary thesis sentence", with its fixed-data / asymptotic / not-claimed scopes. All seats conceded D2 to C's position. The other three wordings are kept above for the paper's authors.

Related transcript statement of the thesis sentence: [pos 1044] (see §A0.4). FOR_FELIPE ([pos 1650]): "The thesis sentence ('correlation costs depth and particles, never correctness') appears as a remark scoped to exactly what M1, M2, M7 and M8 prove."

## Cited lemmas of TLF Part III (CL01–CL23)
The 23 rows of the table "Cited lemmas (not numbered claims of paper 1)" (TLF lines 1297–1325) are registered as CL01–CL23 in order; verbatim table:

## Cited lemmas (not numbered claims of paper 1)

Collected from the final cards and Round 3 files. Each is cited in the main text or inside a card; none is a theorem number of paper 1 unless said so.

| Cited result | Used in | Source (path:line) |
|---|---|---|
| N9 kernel facts: γ_φ-reversibility of each elementary move, q_φ-invariance and self-adjointness of the uniformly random-order round, exact draw_pi0 and Z̄₀ (K08, K20, K21), with the CHK amendments (VERIFIED WITH AMENDMENT) | M1(a), S-KERNEL | `R3_A.md:114,120`; `MINUTES.md:39,64` |
| K47 (pooling, cited) | M1; S-POOL | `MINUTES.md:39`; `R3_A.md:114` |
| SMC identities and fixed-data limits: Del Moral 2004; Del Moral–Doucet–Jasra 2006; Whiteley–Lee–Heine 2016; Dai et al. 2022 | M1(a), (f) | `R3_A.md:127`; `R3_D.md:183` |
| Markov lower bound: Grosse–Ghahramani–Adams 2015 | M1(d), M4(e) | `R3_A.md:127`; `R3_B.md:208` |
| Greedy-schedule optimality: Štefankovič–Vempala–Vigoda 2009 | M7(a), M2(b6) | `R3_A.md:154`; `R3_B.md:179` |
| K28: √c·T*(c) → Λ_len (Syed et al. 2024 Thm 3; Gelman–Meng 1998) | M7(e) (cited) | `R3_A.md:147,154`; `MINUTES.md:45` |
| Chatterjee–Diaconis 2018 Thms 1.1–1.3 (exp(KL) scale; with log-weight-tail qualifications) | M6, M2(c2) | `R3_C.md:199`; `R3_B.md:179`; `R3_D.md:183` |
| Cérou–Del Moral–Guyader 2011 Thms 1.4–1.5 (variance theorems; novelty of S-Z (i) to the citation checker) | M2, S-Z | `R3_B.md:179`; `R2_B.md` S4 |
| Frazier et al. 2023, Assumption 6(iv) (generic χ² precedent; not re-fetched) | M2 | `R3_B.md:179` |
| Papaspiliopoulos–Rossell 2017 §§3.1–3.2 (block computation precedent) | M3 | `R3_C.md:170` |
| Dai–Heng–Jacob–Whiteley §4.2 (independent-system evidence weighting) | S-REP | `R3_C.md:236` |
| K60, K61: Barbieri–Berger 2004 HPM/MPM facts (cited lemmas) | M5, S-TARGET | `R3_D.md:151,183`; `R2_D.md:46` |
| Rossell 2022 Prop 1 (the 2E₀δ₁ term) | M5(0) | `R3_D.md:151` |
| Yang–Wainwright–Jordan 2016; Zhou–Yang–Vats–Roberts–Rosenthal 2022 (context next to M5; "with their priors LH is covered by rapid mixing; ours is for the paper's own target and start") | M5, M4 | `R3_D.md:151`; `R3_B.md:208` |
| Hou–Wang–Atchadé arXiv:2407.20580 (never "first finite-n") | M5, M4 | `R3_D.md:151`; `R3_B.md:208` |
| Brent 1974 (W/w + D scheduling) | M8(d) | `R3_D.md:170,183` |
| T22(iii) (K16) PROVED-LOCKED CONDITIONAL, with G, R, within-block SE, EXP′, VIS, NL_η, NL_avg(κ) retained | M3 (supplementary clause) | `R3_C.md:163` |
| CHK-verified WS3, WS4 (M2(a), M3(e)); WS6(d), WS7 with amendments (M2(c)) | M2, M3 | `R3_B.md:160,170–171`; `MINUTES.md:23` |
| T03♯ (S-T) target consistency, T01–T03 PROVED-LOCKED (external review queued) | M1(i), M3, M4(f), M5, M6 | `R2_C.md` C9; `MINUTES.md:60` |
| Lemma RO (event containment), GUARD-W (stop-only coupling; audit open) | M1(d), M4(e), S-OUT | `R3_B.md:194`; `R2_C.md` C13 |
| Furnival–Wilson 1974 (leaps-and-bounds superset bound, K05) | S-CERT | `R0_DIFF.md` K05 row (line 74) |
| K23 squared-kernel Dirichlet comparison, as an attributed lemma without theorem number (C's dissent; optional for the S-KERNEL HQ) | S-KERNEL | `MINUTES.md:79`; `R3_C.md:59` |
| LIT-PAR G4 (Song–Liang numerical comparison), cited as labelled numerical evidence; the analytic separation K97 is FUTURE_WORK | Coverage Cor 2 | `MINUTES.md:78,84` |

Registrar notes (TLF lines 1327–1331, verbatim):

## Notes for the registrar/chair (not choices)

- N2 sub-labels: the R3 files identify N2(c) = integrated LS0 replay (`R3_D.md:155`) and N2(e) = GUARD-W stop-only coupling (`R3_B.md:213`). The label N2(b) is used in MINUTES §2.3 and R3_B §S4 (`R3_B.md:315`) but is not defined in any R3 file; its definition is in `THEOREM_REVISION_INPUTS.md` (N2), which is not on this branch. The charters name it as MINUTES does.
- M1 K-ID header: see the integration note under M1.



---

# A4 · HQ rulings that change how goals are read

These are readings of Felipe's proposal goals that HQ made on its own authority; Felipe "may overrule them" (`MEET-THM/MINUTES.md` §3 item 1; [pos 1614]; FOR_FELIPE item 4). As of [pos 1673] Felipe had not commented.

## A4.1 Q1–Q4 rulings (RL01–RL04), verbatim file `MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`
Request: [pos 1608] (chair → HQ, commit 517bffa). HQ answer: [pos 1614].

<!-- BEGIN VERBATIM MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md:1-24 -->
HQ → chair: rulings on HQ_QUESTIONS Q1–Q4 (2026-11-04). Please commit this message verbatim as `theory_campaign/MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md` and apply it. HQ will report these readings to Felipe with the final list; he may overrule them.

**Q1 (§5.3): ACCEPTED, with three conditions.** The proposal frames §5.3 as a "possible direction" whose purpose is to "formalize when local variable-selection proposals are useful"; in a method whose correction is a bridge, not one-shot IS, the bridge form is the faithful reading. To count as meeting §5.3, paper 1 must ship ALL of:
 (a) the **discrepancy half** of the proposal's sentence, in our method's terms: the divergence between π₀ and π (e.g. the d = d_σ + d_X decomposition / Jeffreys J / KL) is controlled by the cross-block dependence terms plus the explicit σ²-coupling term, on a genuinely correlated family (ε > 0), with constants;
 (b) the **bridge-form stability theorem**: per-stage χ²/weights, stage count and constants continuous in ε around the block-orthogonal baseline, again on a genuinely correlated family (IC3 must be exhibited, not asserted);
 (c) the **refutation of the one-shot form** (OWS-WS6(d), WS7) as a stated proposition, but only after an independent cross-family check passes. If the check fails, the one-shot question reopens and comes back to HQ.
 If (a) or (b) cannot be given a credible route by close, it escalates to HQ as an unmet binding goal. It is not dropped.

**Q2 (§5.4 credible-interval coverage): the posterior-content / Monte Carlo reading is ACCEPTED.** §5.4 is about the approximation error of the computed posterior against the exact one. "Coverage error" therefore means |π(C(π̂)) − nominal| for the credible quantities the method reports, plus their Monte Carlo error. Frequentist coverage of the exact posterior is a target-theory question outside §5.4. List it in FUTURE_WORK.md with that reason.

**Q3 (§5.4 TV/KL of the final pooled estimate under masking): NOT binding; carry it as an obligation with a fallback.** §5.4 says "possible metrics include", so the binding part is "quantify the approximation error". That is met by:
 - the shipped PIP and joint-inclusion error bounds;
 - the deterministic reported-posterior TV = 1 − Z_𝒯/Z;
 - the start TV/KL and Lemma KL;
 - the terminal-law and favourable-regime TV results.
 State the reverse-KL obstruction (infinite on missed support) as a definitional fact. The masked final-estimate TV/KL bound goes to FUTURE_WORK.md, citing V11/N10 as OPEN. One requirement: the list must still contain at least one masked-regime accuracy statement that paper 1 actually proves, for example the certificate card's detection of underestimation or a PIP bound conditional on delivery. Say which one.

**Q4 (Ĵ and the cross-block leakage proxy): REPORTING, allowed.** Conditions:
 - computed only from quantities the run already has (X, the blocks, the bridge's existing particles and weights);
 - read no random numbers, never feed back into calibration, the schedule or the decision (POST HOC, like the certificate card);
 - specified precisely enough to state theorems about them, including the estimator's definition and its numerical label.
 HQ will add them to METHOD_v3.1_FINAL as a reporting amendment (AMENDMENT_HQ_02) when you send the exact definitions at close.

**Chair decisions noted:** sending N9 to the cross-family checker in wave 2 is right; R_n in H(f) is yours to settle.
<!-- END VERBATIM MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md:1-24 -->

Question texts Q1–Q4 are in `MEET-THM/HQ_QUESTIONS.md` lines 5–41 (not re-quoted); the application table ("how the meeting applies them") and the Q1(c) check record are lines 48–66 of the same file. The Q1(c) check record in one line (verbatim, line 66): "**Consequence:** the Q1(c) condition is met, so (c) can ship as a stated proposition with these amendments. It does not reopen with HQ."


Transcript messages: chair's request [pos 1608] and HQ's reply [pos 1614] (verbatim):

<!-- BEGIN VERBATIM transcript [pos 1608] -->
MEET-THM chair → HQ. Round 1 is done (R1_A–R1_D) and check wave 1 is running. I need 4 HQ decisions, written up in `theory_campaign/MEET-THM/HQ_QUESTIONS.md` (branch theory/MEET-THM, commit 517bffa):

- **Q1, §5.3.** Does the bridge-form weight-stability theorem meet the goal? The one-shot form is refuted for the shipped method (WS6(d) and WS7, both author-only).
- **Q2, §5.4.** Can "credible-interval coverage" mean the Monte Carlo / posterior-content error rather than frequentist coverage?
- **Q3, §5.4.** Is TV/KL of the final estimate under masking a binding goal, or an obligation with a fallback?
- **Q4.** Do the run-card additions Ĵ and the cross-block leakage proxy count as reporting or as a method change?

The meeting continues on both readings until you rule.
<!-- END VERBATIM transcript [pos 1608] -->

<!-- BEGIN VERBATIM transcript [pos 1614] -->
I've sent the chair my rulings on all four questions, with a request to file them in the meeting record. You can overrule any of them when I bring you the final list.

1. **§5.3 weight stability: the bridge form counts, with three conditions.** The literal reading, where weights from the start alone stay bounded, has been refuted for our method, though that refutation hasn't had an independent check yet. It fails even when the blocks are exactly orthogonal. Since the method corrects the start through the tempering bridge, the bridge form is the faithful reading. To count, paper 1 must deliver all three:
   - a theorem that the distance between the start and the true posterior is controlled by the cross-block correlation terms (plus the shared noise-variance term);
   - stability of the bridge as cross-block correlation grows from zero, shown on a genuinely correlated design family;
   - the refutation of the literal form, once it passes an independent check.

   If any part has no credible proof route by the end of the meeting, it comes back to me as an unmet goal. It doesn't get dropped.
2. **§5.4 "credible-interval coverage error": read as how far the computed credible quantities are from the exact posterior's.** That means how much exact-posterior probability they actually carry, plus their Monte Carlo error. That's what §5.4 is about: the computed posterior against the exact one. Frequentist coverage is a different question and goes to future work.
3. **§5.4 TV/KL error of the final estimate in masked designs: not mandatory.** §5.4 says "possible metrics include", so it is listed as an open obligation. The goal itself is still met by the PIP and joint-inclusion error bounds, the exact TV of the reported posterior, and the start's TV/KL results. I added one requirement: paper 1 must still prove at least one accuracy result for masked designs.
4. **Two new run-card numbers: allowed as reporting.** These are a Jeffreys-divergence estimate and a cross-block correlation measure. They count as reporting provided they reuse what the run already computed, draw no new random numbers, and never feed back into the run. I'll add them to the method spec as a second reporting amendment.

The meeting is in check wave 1 after Round 1, with all four seats' positions in.
<!-- END VERBATIM transcript [pos 1614] -->

## A4.2 Q5 ruling (RL05), verbatim `MEET-THM/evidence/2026-11-04_HQ_RULING_Q5.md`
Request: [pos 1621]. HQ answer: [pos 1624].

<!-- BEGIN VERBATIM MEET-THM/evidence/2026-11-04_HQ_RULING_Q5.md:1-12 -->
HQ → chair: ruling on Q5 (2026-11-04). Please commit it verbatim as `theory_campaign/MEET-THM/evidence/2026-11-04_HQ_RULING_Q5.md`.

**Q5: ACCEPTED.** "Continuous in ε" was my wording for a quantity that is integer-valued, so it cannot apply literally to T. The right formal content of Q1(b) for the stage count is exactly what was checked:
- the sandwich T_bd(.9e^{−4η}) ≤ T ≤ T_bd(.9e^{4η}) with η → 0 as ε → 0;
- local constancy at non-critical thresholds;
- a continuous upper envelope.

Two conditions:
(1) The real-valued parts of Q1(b) must still be stated as genuine continuity or Lipschitz statements in ε, on the genuinely correlated family: the per-stage χ² and weight-dispersion bounds and the constants.
(2) The theorem and the paper must say plainly that T is a step function of ε, which can jump at critical thresholds (cite the PC1 example: T = 3 between baseline counts {2, 4} at ε = 10⁻⁵). "Stable stage count" means the sandwich, nothing more.

Q1(c) noted as met. Proceed to synthesis 2.
<!-- END VERBATIM MEET-THM/evidence/2026-11-04_HQ_RULING_Q5.md:1-12 -->

Question text: `HQ_QUESTIONS.md` §Q5 (lines 68–91, not re-quoted). Transcript messages:

<!-- BEGIN VERBATIM transcript [pos 1621] -->
MEET-THM chair → HQ. I need one more decision, Q5, written up in `theory_campaign/MEET-THM/HQ_QUESTIONS.md` §Q5 (commit 421edb8).

Your Q1(b) ruling asks for the "stage count continuous in ε". The coded grid's stage count T is an integer, so it jumps at threshold crossings: PC1 found T = 3 between baseline counts {2, 4} at ε = 10⁻⁵. What has been checked as true is:
- the sandwich T_bd(.9e^{−4η}) ≤ T ≤ T_bd(.9e^{4η}), with η → 0 as ε → 0;
- local constancy at non-critical thresholds;
- a continuous upper envelope.

Do you accept this as meeting Q1(b)? The meeting proceeds on that reading unless you rule otherwise.

Q1(c) is met: the cross-family check passed WS6(d)/WS7 with amendments.

Status: Round 2 and check wave 2 are done. Synthesis 2 is next.
<!-- END VERBATIM transcript [pos 1621] -->

<!-- BEGIN VERBATIM transcript [pos 1624] -->
The chair asked for a ruling on Q5. I accepted the meeting's reading of how the theorem should treat the stage count, and the meeting continues.

My earlier wording said the stage count should be "continuous in ε", where ε is the strength of the cross-block correlation. That can't hold literally, because the stage count is a whole number and jumps at thresholds. The meeting had already found such a jump in a checked example.

What I accepted instead, all of it already checked:
- the stage count stays within bounds on both sides that tighten to the uncorrelated count as ε → 0;
- away from those thresholds, small changes in ε leave it unchanged;
- a continuous upper limit on it.

I added two conditions:
- The bounds on weight variability at each stage, and the constants, are ordinary numbers, so they must still be proved continuous in ε on a correlated design family.
- The paper must state plainly that the stage count can jump. "Stable stage count" means the two-sided bounds, nothing more.

The literal one-shot form of §5.3 has now passed its independent check from a different model family, with amendments, so condition (c) of my §5.3 ruling is met.

Round 2 and the second round of proof checks are done, and the chair is now writing the Round 2 synthesis.
<!-- END VERBATIM transcript [pos 1624] -->

Where these rulings are applied in the final cards: Q1 (a)(b)(c) → TH02 (a), (b), (c); Q2 → TH13 clause C15-CI and TH01 (g); Q3 → TH04 (f) + CJ02 (FW2); Q4 → TH19 and AMENDMENT_HQ_02; Q5 → TH02 (b6), (b6′), (b7), (b8) and TH07.

## A4.3 Closing message of the chair and HQ's review (verbatim)

<!-- BEGIN VERBATIM transcript [pos 1626] -->
MEET-THM chair → HQ: CLOSED. Package on branch `theory/MEET-THM` (commit 514c8fc), folder `theory_campaign/MEET-THM/`. Start with `MINUTES.md`. Open questions: none.

**Paper-1 list.** 8 main theorems, unanimous in Round 3. Full cards are in `THEOREM_LIST_FINAL.md`.
- M1 V/H: validity plus accuracy of reported functionals; binding §13.1 via N1.
- M2 WS: the §5.3 package (a)(b)(c), meeting your Q1 + Q5 conditions.
- M3 START.
- M4 Z𝒯 + certificate card + the masked-regime statement (Q3).
- M5 HPM: composition, and reported HPM with LS0 on LH.
- M6 SEP + Lemma KL.
- M7 STG: stage laws.
- M8 Prop D: island-level work/depth, for objective (2).

**Rest of the package:**
- 12 supplement cards.
- `FUTURE_WORK.md`: FW1–FW27 and 6 drops, each with a reason.
- `COVERAGE_MATRIX.md`: proposal goals, Song–Liang, THM-INV and N1–N17.
- `HQ_CHARTERS/`: 8 theorem HQs + 5 lemma packs, in 4 waves (MINUTES §2.5).
- `REGISTRY_PAPER1.md` and `NOTATION.md`.
- `FORMAT_NOTES.md`.

**Checks.**
- Two cross-family check waves.
- An inherited-proof check: OWS-WS3/4 VERIFIED; WS6(d), WS7 and N9 VERIFIED WITH AMENDMENT.
- The auditor after each synthesis and at close: PASS WITH CORRECTIONS, all applied (`CLOSE_AUDIT.md`).

**For you:**
1. `AMENDMENT_HQ_02_DEFINITIONS.md`, ready to record:
   - the Ĵ estimator;
   - the cross-block proxy ε̂_× and its companions;
   - d added to 𝓗;
   - a read-only accumulator;
   - two optional R′ growth rates.
2. `REGISTRY_PAPER1.md` §9: five recommended registry updates for the registry owner.
3. Items to carry to Felipe (MINUTES §3):
   - your readings Q1–Q5;
   - the disclosed §5.3 scale (useful constants need ε ≲ n^{−1/2}/p);
   - Prop D in main, with Seat D's alternative of main = 7;
   - the Song–Liang separation deferred to FUTURE_WORK, with paper 1 comparing rather than exceeding SL Thms 1, 2 and 4.
<!-- END VERBATIM transcript [pos 1626] -->

<!-- BEGIN VERBATIM transcript [pos 1631] -->
The meeting produced 8 main theorems and 12 supplement cards, covering all 108 candidates. Before approving, I'm checking the start-test status and the parts of the package I have concerns about.


<!-- END VERBATIM transcript [pos 1631] -->

## A4.4 HQ's approval amendment (RL06): [pos 1639]

<!-- BEGIN VERBATIM transcript [pos 1639] -->
I've approved the package with one change: the second optional growth rate, about 10¹⁷ islands at study sizes, will be kept only as a sufficient rate inside the theorem, not as a method configuration, and I'm recording AMENDMENT_HQ_02 on that basis.


<!-- END VERBATIM transcript [pos 1639] -->

Recorded in `MEET-v31/AMENDMENT_HQ_02.md` (verbatim above, §A1.10): "**Configuration (ii), R′_n = 4⌈(n + p)⁶/4⌉.** HQ keeps it **only as a sufficient rate inside the theorem** (M1's simultaneous-control clause: "for any R′_n ≥ 4⌈(n + p)⁶/4⌉"), not as a runnable configuration of the method. Reason: at study sizes (n + p ≈ 700) it is about 10¹⁷ islands, so listing it as a method setting would misrepresent what the method can run. The theorem is unaffected." (The constant c in "R′ ≥ c(n+p)⁶" used informally corresponds to the source's 4⌈(n + p)⁶/4⌉; see U1.)

## A4.5 Plain-language list for Felipe ([pos 1650]) and file `FOR_FELIPE_THEOREM_LIST.md`

<!-- BEGIN VERBATIM transcript [pos 1650] -->
The theorem list is ready for your approval. The meeting closed with no open questions, and I've reviewed and approved the package on my side. The full version is in [FOR_FELIPE_THEOREM_LIST.md](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/theory-MEET-THM/theory_campaign/MEET-THM/FOR_FELIPE_THEOREM_LIST.md). Full statements are in `THEOREM_LIST_FINAL.md` on branch `theory/MEET-THM`, and the final method is in [FOR_FELIPE_FINAL_METHOD.md](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/theory-MEET-v31/theory_campaign/MEET-v31/FOR_FELIPE_FINAL_METHOD.md).

**Main theorems (8, all four seats agreed):**

| # | Theorem | Your goal |
|---|---|---|
| M1 | Validity under any correlation, plus error bounds for PIPs, joint inclusions and general summaries | §5.1, §5.2, §13.1 |
| M2 | Weight stability: start-to-posterior distance controlled by cross-block correlation; bridge stable as correlation grows; the literal one-shot form proved false | §5.3 |
| M3 | Laws for the start: guaranteed mass, error decomposition, masking, dilution | local-to-global |
| M4 | Evidence brackets, a sound certificate card, and a proved accuracy result for masked designs | §5.4 |
| M5 | Selection by the reported best model: finite-n bound; consistency with LS0 on masked designs | objective 3 |
| M6 | Why the merge alone fails: one-shot correction needs polynomially many draws | thesis |
| M7 | Stage laws: correlation costs about log₂(masking depth) sequential stages | objective 2 |
| M8 | Work, depth and width at the island level, compared with Song–Liang §6 | objective 2 |

There are also **12 supplement cards**, including target consistency and kernel validity. The meeting considered 108 candidates. Every one ended up on the list, in future work (27, each with a reason), as a cited published result, or dropped (6, with reasons). Two rounds of proof checks by a different model family found 20 counterexamples in draft statements, and all were repaired or removed.

**Decisions for you:**
1. **Approve the list:** 8 main theorems plus 12 supplement cards.
2. **The Song–Liang separation is not proved.** The meeting couldn't get a sound proof that their split-and-merge loses true predictors under correlation. The paper compares with their results and cites the numerical counterexample as labelled evidence; our side, validity under any correlation, is proved (M1). I recommend one small scout HQ on the separation alongside wave 1. If it succeeds it becomes a ninth main theorem; nothing else waits on it.
3. **Prop D (M8) in the main text or the supplement.** I recommend main, for parallel scalability. The alternative leaves 7 main theorems.
4. **My readings of your goals, which you can overrule:**
   - §5.3 is met by the bridge form. One caveat: the example family gives useful constants only for very weak cross-block correlation, of order ε ≲ n^(−1/2)/p.
   - §5.4 "coverage" means distance from the exact posterior's credible quantities, not frequentist coverage.
   - TV/KL of the final estimate under masking is future work.
   - The stage count is a step function of correlation strength, held within two-sided bounds.

**Things I did on my own authority:**
- **Two new run-card numbers added to the method as reporting only:** a Jeffreys-divergence estimate and a cross-block correlation measure. The method's law is unchanged.
- **One proposed growth rate kept only inside a theorem, not as a method setting:** it would mean about 10¹⁷ islands at study sizes.
- **Overnight problem, fixed:** the confirmatory start-test jobs died at 01:25 UTC. I found the cause: T3 kills everything an agent started when that agent's session ends. I relaunched them as independent system services, so that can't happen again. They're 54 of 118 done and should finish late morning UTC.

Once you approve, wave 1 of the per-theorem HQs launches: M1, M3 and the foundations pack.
<!-- END VERBATIM transcript [pos 1650] -->

## A4.6 Other HQ authority decisions in the final state
- Felipe's four approved decisions (recorded [pos 1304], text [pos 1302]): (1) budget growth rates may become explicit functions of (n, p) "limited to growth rates only, with no other method change"; (2) paper 1 claims island-level depth only; (3) confirmatory local-to-global test; (4) same three seats. Also [pos 1324]–[pos 1326]: "no API", subscriptions (Claude Work, Claude Personal) — later changed at [pos 1673] ("we will use Claude through the remaining $19 of cloud and the remaining $121 of the other credit").
- HQ's C6 trigger (union): METH31 §3 C6; MINUTES (v31) decision 6; [pos 1467].
- AMENDMENT_HQ_01 (HQ dispositions after the Sol reviews): [pos 1480], [pos 1512]; file `MEET-v31/AMENDMENT_HQ_01.md`.



---

# A5 · Future work (CJ01–CJ27), drops (DR01–DR06), inherent limitations (LIM01–LIM09), obligations (OB01–OB17)

## A5.1 FUTURE_WORK FW1–FW27 as CJ01–CJ27
Source `MEET-THM/FUTURE_WORK.md` (header: "FW1 and FW2 are unchanged. FW3–FW27 were added by the clerk from MINUTES §2.3/§2.4, SYNTH_R2 §2.4 and R3_C §S4 'Required additions'; reasons are as the sources give them."). Each entry: item, reason, source, all verbatim cell texts. Position: package announced at [pos 1626] ("FUTURE_WORK.md: FW1–FW27 and 6 drops, each with a reason").


**CJ01 (native FW1)**
- Item (verbatim): Frequentist coverage of the exact posterior's credible intervals
- Reason (verbatim): A target-theory question outside proposal §5.4, which concerns the computed vs the exact posterior (HQ ruling Q2, 2026-11-04)
- Source (verbatim): `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`

**CJ02 (native FW2)**
- Item (verbatim): TV/KL error bound for the final pooled estimate in the masked regime
- Reason (verbatim): Not binding (§5.4 lists "possible metrics"; HQ ruling Q3); needs V11 or N10, both OPEN
- Source (verbatim): `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`; R1_D:602; R1_A:645–646

**CJ03 (native FW3)**
- Item (verbatim): K13: start-mode consistency under orthogonal blocks and a σ²-inflated beta-min margin
- Reason (verbatim): Needs TG4-type probability bounds not supplied
- Source (verbatim): `SYNTH_R2.md:173` (R0_DIFF K13)

**CJ04 (native FW4)**
- Item (verbatim): K24: polynomial mixing of the φ = 1 round (Yang–Wainwright–Jordan transfer); also useful general production mixing and masked population accuracy (N10)
- Reason (verbatim): N10 OPEN; the YWJ/ZYVR route is blocked as stated
- Source (verbatim): `SYNTH_R2.md:174`; `R3_C.md:385`

**CJ05 (native FW5)**
- Item (verbatim): K23: Dirichlet/spectral comparison of the random-order round with the random-scan mixture
- Reason (verbatim): Its only consumer, K24, is deferred (A, B, D, R3-4). Seat C dissents: it would keep the finite squared-kernel Dirichlet comparison as an attributed lemma in S-KERNEL; MINUTES allows the S-KERNEL HQ to cite it without a theorem number
- Source (verbatim): `SYNTH_R2.md:175`; `MINUTES.md:79`; `R3_C.md:59`

**CJ06 (native FW6)**
- Item (verbatim): K31: as-coded masked stage count (realised T_n; Conjecture P OPEN); N5(b): rebuild convergence within ℓ rebuilds, candidate-pair coverage / P(S₀ ∈ V), P(schedule_limit) and calibration-failure probabilities
- Reason (verbatim): Conjecture P OPEN; V's complement is never inspected (I9(d)); only T ≤ T_e and the coverage identity are provable; successful-grid properties do not prove successful calibration. Rebuild convergence is FW in either placement of K33
- Source (verbatim): `SYNTH_R2.md:176`; `MINUTES.md:82`; `R3_C.md:325`; `R3_D.md:247`

**CJ07 (native FW7)**
- Item (verbatim): K58: masked consistency of the equal-weight PIP/MPM
- Reason (verbatim): Reduces to population delivery; FMP-DELIVPOP is OPEN
- Source (verbatim): `SYNTH_R2.md:177`

**CJ08 (native FW8)**
- Item (verbatim): K57, general fixed-budget equal-weight accuracy (only the recording-marginal bias comparison P1 ships in S-POOL)
- Reason (verbatim): A recording-marginal bias bound does not close estimator accuracy or DELIV-POP; needs a checked estimator-level theorem for the actual records and budgets
- Source (verbatim): `MINUTES.md:66`; `R3_C.md:323`; `R3_C.md:36`; `R3_B.md:86`

**CJ09 (native FW9)**
- Item (verbatim): K59: R vs N at fixed total particles (allocation)
- Reason (verbatim): PROOF SKETCH only
- Source (verbatim): `SYNTH_R2.md:178`

**CJ10 (native FW10)**
- Item (verbatim): K71: (b1-LH-iid) on LH with iid final draws, also under general DELIV
- Reason (verbatim): (b1-LH-iid) GAP; T38-b1-LH-iidfail XF ERROR
- Source (verbatim): `SYNTH_R2.md:179` (R0_DIFF K71)

**CJ11 (native FW11)**
- Item (verbatim): K75: NP-completeness of the global-certificate decision problem for the fixed prior and penalty
- Reason (verbatim): Needs a score-specific reduction that has not been supplied
- Source (verbatim): `SYNTH_R2.md:180`

**CJ12 (native FW12)**
- Item (verbatim): K92: separation from single-chain flip/swap MCMC (moat construction)
- Reason (verbatim): The moat construction and the accuracy-matched comparator are unproved; speed-up claims are empirical by decision
- Source (verbatim): `SYNTH_R2.md:181`

**CJ13 (native FW13)**
- Item (verbatim): K82: delivery, P(U) → 0 (also delivery/resource-failure laws, P(resource_limit))
- Reason (verbatim): No route; every output theorem is stated jointly with the output event in liminf form
- Source (verbatim): `SYNTH_R2.md:182`; `R3_C.md:372`

**CJ14 (native FW14)**
- Item (verbatim): K94: finite-n bound on the posterior-miss probability Π(X)
- Reason (verbatim): Envelope GAP
- Source (verbatim): `SYNTH_R2.md:183`

**CJ15 (native FW15)**
- Item (verbatim): K99 quantitative: k-way barrier for cross-block masked contrasts
- Reason (verbatim): k-way barrier unproved (the qualitative remark ships in S-LIM)
- Source (verbatim): `SYNTH_R2.md:184`

**CJ16 (native FW16)**
- Item (verbatim): K107: validated arithmetic / rounding-error bound; production validated numerics (N16)
- Reason (verbatim): N16 OPEN; T33-errbound COUNTEREXAMPLE; exact-arithmetic bounds do not validate rounded production computations. K108 (deterministic perturbation lemma) stays in S-CERT
- Source (verbatim): `SYNTH_R2.md:185`; `R3_C.md:331`

**CJ17 (native FW17)**
- Item (verbatim): K80: positive power of the E1/E2/E3 and low_empirical_ESS flags
- Reason (verbatim): Flags are heuristics by decision; no sampling law for the flags
- Source (verbatim): `SYNTH_R2.md:186`; `MINUTES.md:80`

**CJ18 (native FW18)**
- Item (verbatim): N12 / exponential p: exponential-dimension contraction and selection (Song–Liang Cor 1)
- Reason (verbatim): No completed prior-tail/contraction route; p ≤ n^A stays in scope
- Source (verbatim): `SYNTH_R2.md:188`; `R3_C.md:352,387`

**CJ19 (native FW19)**
- Item (verbatim): Growing support and cap non-binding (N11/N12)
- Reason (verbatim): Fixed-support LH does not discharge these extensions
- Source (verbatim): `R3_C.md:328`

**CJ20 (native FW20)**
- Item (verbatim): Hellinger / predictive contraction (Song–Liang Thm 1)
- Reason (verbatim): Not delivered; selection counterpart in S-T only
- Source (verbatim): `SYNTH_R2.md:189`

**CJ21 (native FW21)**
- Item (verbatim): K97: Song–Liang analytic separation (null-exclusion/FDR)
- Reason (verbatim): The iteration-uniform null-BF/prior-odds step is NOT REPAIRED (W2PC1) and is an unproved hypothesis about SL's algorithm, not a model/design condition. LIT-PAR G4 is cited in the paper as labelled numerical evidence
- Source (verbatim): `MINUTES.md:78,84`; `SYNTH_R2.md:191`

**CJ22 (native FW22)**
- Item (verbatim): Sharp ε-scale necessity statement for §5.3
- Reason (verbatim): All three seat forms are COUNTEREXAMPLEs; C's is a range obstruction for the D_* route only. The scale disclosure ships (not a theorem)
- Source (verbatim): `SYNTH_R2.md:192`

**CJ23 (native FW23)**
- Item (verbatim): K29: favourable O(1) stage law, unconditional application
- Reason (verbatim): The (LL)/over-tilted q_w input is not a model/design condition and no family exhibits it (W2PC1:187 DESIGN-ASSERTED, GAP). Only the conditional implication is cited in S-STGI
- Source (verbatim): `MINUTES.md:70`; `R3_C.md:324`; `R3_A.md:43,67`; `R3_B.md:61`

**CJ24 (native FW24)**
- Item (verbatim): Useful two-sided masked evidence precision (N4(iii)/V11)
- Reason (verbatim): Distinct from FW2's final-estimate TV/KL and from one-shot variance failure; V11 OPEN
- Source (verbatim): `R3_C.md:326`

**CJ25 (native FW25)**
- Item (verbatim): Random/adaptive partition quality and study packing (N8; K71 as C pairs them), including the study generator (PART-pairing, g = 5, 2g ≤ B)
- Reason (verbatim): SIZE does not determine pairings when two groups fit in one block; PART-pairing OPEN; the study design is not the LH exhibit
- Source (verbatim): `R3_C.md:327`; `R3_D.md:246`

**CJ26 (native FW26)**
- Item (verbatim): Finite-n Gibbs discovery (HPM residual)
- Reason (verbatim): Existing asymptotic or vacuous bounds do not supply useful finite-n discovery (ThmB-T24 vacuous at n = 200; no route)
- Source (verbatim): `R3_C.md:329`; `R3_B.md:303`; `R3_D.md:248`

**CJ27 (native FW27)**
- Item (verbatim): Unbounded functionals: integrability extensions of M1 (§13.1)
- Reason (verbatim): M1 is stated for bounded h ∈ [0, 1]; unbounded functionals require integrability extensions (from C's coverage table, not its "Required additions" table)
- Source (verbatim): `R3_C.md:344`

Footer of the file (verbatim): 
Items recorded as "outside the fixed method" (adaptive/overlapping partitions; backfit start) are dispositions in `COVERAGE_MATRIX.md`, not FUTURE_WORK. The audit obligations (N2(b),(c),(e), N14(c), the N3 DP invariant, the integrated streams/LS0/GUARD-W/DAG audits) are named implementation premises in `HQ_CHARTERS/`, not FUTURE_WORK (MINUTES §2.3).

## A5.2 The 6 drops as DR01–DR06 (verbatim; `FUTURE_WORK.md` "Dropped (MINUTES §2.4; not FUTURE_WORK)")


**DR01 (native K12)**
- Reason (verbatim): A test oracle, not a guarantee
- Source (verbatim): `MINUTES.md:94`; `SYNTH_R2.md:195`

**DR02 (native K34)**
- Reason (verbatim): TI evidence is not in the method (the Ĵ half ships as reporting, S-REP)
- Source (verbatim): `MINUTES.md:95`; `SYNTH_R2.md:196`

**DR03 (native K66)**
- Reason (verbatim): PARTLY-FALSE (C3-PGD, CEX-localmax(A2))
- Source (verbatim): `MINUTES.md:96`; `SYNTH_R2.md:197`

**DR04 (native K67)**
- Reason (verbatim): Relies on K66
- Source (verbatim): `MINUTES.md:97`; `SYNTH_R2.md:198`

**DR05 (native K91)**
- Reason (verbatim): No accuracy-matched comparator; OPW2-cex
- Source (verbatim): `MINUTES.md:98`; `SYNTH_R2.md:199`

**DR06 (native K98)**
- Reason (verbatim): KNOWN-FALSE (SHARE-M(b), FD-NM)
- Source (verbatim): `MINUTES.md:99`; `SYNTH_R2.md:200`

(In the MEET-THM snapshot `MINUTES.md` §2.4 the same drops sit at lines 98–103, not 94–99 as `FUTURE_WORK.md` cites: harmless line-number drift, noted as U9.)

MINUTES §2.4 (verbatim) and the Round-3 votes (`MINUTES.md` §2.3 row "R3-4, K12, K34": "Drop (A, B, C, D in Round 3)"):

### 2.4 FUTURE_WORK and drops

Complete in `FUTURE_WORK.md`, which adds C's residual obligations (R3_C §S4) to SYNTH_R2 §2.4.

**Drops, with reasons:**
- K12: a test oracle, not a guarantee.
- K34: TI evidence is not in the method.
- K66: PARTLY-FALSE (C3-PGD, CEX-localmax(A2)).
- K67: relies on K66.
- K91: no accuracy-matched comparator; OPW2-cex.
- K98: KNOWN-FALSE (SHARE-M(b), FD-NM).


## A5.3 The method meeting's 9 inherent limitations (LIM01–LIM09), verbatim `MEET-v31/MINUTES.md` §5

Numbering LIM0n = item n of the list. Positions: [pos 1280] ("Nine inherent limitations are listed, each proved or true by definition"), [pos 1302] ("9 inherent limitations, each proved impossible or true by definition, with a separate list of what is *not* inherent"), [pos 1128]/[pos 1130] (HQ's early list of limitations to state rather than fix).

## 5. Inherent limitations, and why each is inherent

Each is either PROVED impossible or true by definition (rule: SYNTH_R1 §3 as amended by the seats). Re-checked under HQ amendment 01: items that do not meet this rule were moved to the "Not inherent" list below.

1. **Per-round sequential factor m = p + B + 2.** True by definition of a random-scan full-coordinate Gibbs round: each update conditions on the previous one. This is inherent to the chosen kernel, not to SMC or BVS. Removing it (C10) is WORKHORSE and breaks the Gibbs-path theorems (T38(b2), BG3, V5).
2. **Every worker needs scoring access to all predictors** (X or sufficient statistics, 8np bytes, local or shared/distributed at a communication cost). True by definition of a full-coordinate round. A private 8p² Gram per worker is **not** inherent (C7).
3. **Masking of the product-of-blocks start built from block-local scores against the full y, under T27(i)'s hypotheses (H2, H3; verified on LH).** T27(i), PROVED-LOCKED (conditional, in its design class). This is a law for that construction and design class; it does not say that every product start is masked on every design. The bridge exists to correct it (SEP-B).
4. **No diagnostic from the observed record (the run's own weights or islands) has a universal detection guarantee for never-visited modes.** V12 and E1c PROVED; Chatterjee–Diaconis Thm 2.1. This does not rule out alerts on particular runs: positive one-sided certificates (decision 10, e.g. Ẑ < Z_𝒯) can still detect some failures.
5. **The properties of Ẑ behind the 95% bound imply no two-sided relative-error bound** (positive, finitely many values, mean Z, iid islands: some such law has P(Ẑ < c₀Z) ≥ 1 − η for any c₀ > 0, η ∈ (0, 1), so {Z ≥ αẐ} places no upper limit on Z/Ẑ) (T31(c), PROVED-LOCKED; PC2 C1(c), PROVED relative to it). This is a non-implication from the estimator's law, not a data-specific impossibility; it excludes neither structural nor record-based bounds. A finite analytic bound exists (PC1 claim 1, PROVED): Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}. Its gap to Z is data-dependent; there is no universal looseness figure. The literal "no run can upper-bound Z" was FALSE, and the blanket "no useful upper bound on Z from the run's record alone" is withdrawn as an inherent limitation.
6. *(Moved by HQ amendment 01.)* Markov sharpness ("0.05Ẑ is sharp given only nonnegativity and the mean") is Seat C's argument, **seat-derived, unchecked** (not covered by PC1), so it is no longer listed as inherent; see the list below. Unchanged and PROVED: the assumption-free probabilistic lower bound max{Z_𝒯, 0.05Ẑ} keeps ≥ 95% coverage (PC1 claim 2). Sharper bounds need information beyond positivity and the mean (not necessarily a variance hypothesis).
7. **Posterior misses at n = 200** (565 strict competitor defeats of S₀ among the 2,394 completed fits, with six stops: at least 565 target-mode misses, not the exact count of global-posterior misses on all 2,400 data sets). True by definition of the fixed target: no search can make the HPM equal S₀ when F(S₀) < F(Ŝ) (N200, T07). This is a fact about these data and this prior, not a universal error rate.
8. **The cap K excludes truths with s₀ > K,** by definition of the prior. **A fixed allocation cannot support unrestricted growth of (n, p),** by definition (V13).
9. **The restricted ESS on V cannot bound mass outside V** without further assumptions, by definition of a restricted diagnostic.

**Not inherent (OPEN; must not be presented as limitations):**
- the severity of weight variance through a masked crossing on the production grid (V11);
- rebuild convergence, P(S₀ ∈ V) and P(schedule_limit) → 0;
- the as-coded masked T_n law;
- DELIV-POP;
- weak-dependence stability (proposal §5.3; a binding goal, so the escalation rule of §9 applies);
- subexponential-p theory under our prior;
- the study generator's g = 5 partition theorem;
- the measured-round identity for general h (proposal §13.1; a binding goal, so the escalation rule of §9 applies);
- Markov sharpness of the assumption-free lower bound on Z (moved from item 6: seat-derived, unchecked);
- the blanket "no useful upper bound on Z from the run's record alone" (withdrawn from item 5: "useful" is undefined and the claim is not proved; only T31(c) and PC1 claim 1 stand).

These are theorem obligations in `THEOREM_REVISION_INPUTS.md`, each with the decision it supports and what happens if the obligation fails. Where a failure would leave a binding proposal goal unmet (general h, §13.1; weight stability, §5.3; N9, §5.1), the goal is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change (§9).

Cross-map to `THEOREM_REVISION_INPUTS.md` §4.A (I-numbers; Summary): LIM01 = I1; LIM02 = I2; LIM03 = I3; LIM04 = I5; LIM05 = I7; LIM06 = I8 (moved to "NOT inherent", AMENDMENT_HQ_01 Q1 and HQ answer 1); LIM07 = I6; LIM08 = I9(a),(e); LIM09 = I9(d). I4, I10, I11 of THEOREM_REVISION_INPUTS have no number in the MINUTES list (see U3). FOR_FELIPE_FINAL_METHOD §4 lists 7 limitations. The I-table (verbatim):

(`THEOREM_REVISION_INPUTS.md` lines 261–284: the I-table I1–I11 with 'Why inherent' and sources, and §4.B 'NOT inherent' list; not re-quoted. The 'NOT inherent' list is quoted above inside MINUTES §5.)

## A5.4 The 17 obligations N1–N17 as OB01–OB17

Source: `MEET-v31/THEOREM_REVISION_INPUTS.md` §3 "New theorem obligations" (each: statement; hypotheses; status; decision supported; if it fails; INV §1 cell). Position: [pos 1280] ("Seventeen unproved properties go to the theorem meeting as obligations"), [pos 1290]. N18 existed only under item-1 Outcome 1 and was "not opened" (TLF/COVERAGE_MATRIX: "N18 was not opened (`R3_D.md:250`)"); item 1 closed as Outcome 2, so there are 17. OBnn = Nn.

Disposition of each in the final package (`COVERAGE_MATRIX.md` §(d), verbatim):

## (d) Obligations N1–N17

Texts: B `R3_B.md:308`; A `R3_A.md:224`; C `R3_C.md:376–392`; D `R3_D.md:250`. N18 was not opened (`R3_D.md:250`).

| N | B | A / C / D (differences marked) | Final |
|---|---|---|---|
| N1 | M1 (binding safeguard) | A: M1(b) (escalation rule). C: M1/L-N1; S-REP and S-IDENT consume it; failure escalates §13.1. D: M1(a) in D's lettering. | M1 (Lemma N1, final (b)); binding §13.1 safeguard. |
| N2 | Implementation premises in the M1, M4, M5 charters | A: S-OUT implementation premises, named in M1, M5, M8. C: S-OUT/M5/M8 audits; GUARD-W gap preserved. D: named in M1, M4, M5, Prop D charters; S-OUT (K83, K84) states what is proved. | Named implementation premises in the charters (M1, M4, M5, M8; LP-AUDIT) and recorded in `REGISTRY_PAPER1.md` (MINUTES §2.3). |
| N3 | Hypothesis in M5; DP invariant FW | **Differs:** A: M5 hypothesis (e4) + S-KERNEL K09 tie proposition. C: S-KERNEL/L-TIE mathematical proposition + M5 emitted-centre audit; registry OPEN retained. D: M5 hypothesis e4; first lemma of the M5 charter; fallback K70. | Named premise (MINUTES §2.3) + K09 proposition C10 in S-KERNEL; not FW. |
| N4 | (i) M1; (ii) S-POOL; (iii) M2(b5) on the domain, masked FW | **Differs on (iii):** A: masked M → FW2. D: V11 → FW2. C: M1 finite-R′, M2 design-derived moments, masked V11 FW (separate). | (i) M1(f); (ii) S-POOL; (iii) M2(b5) on the domain; masked precision = FW24 (separate from FW2). |
| N5 | (a) M1; (b) FW | A: N5(a) → M1(c); N5(b) → FW (K31). C: frozen contract M1/S-OUT; coded geometry M7; convergence FW. **D:** CAL hypothesis + K33 in S-IDENT + FW line. | (a) M1(c); coded finite geometry and K33 count form M7 (D's S-IDENT placement recorded as dissent, MINUTES §2.3); (b) FW6. |
| N6 | M4(e) | A: M1(d), M4(d) [A's lettering]. C: S-OUT/M4 joint-output bounds. D: M4(c), S-OUT [D's lettering]. | M1(d), M4(e), S-OUT. |
| N7 | S-CERT and M4(e) | A: S-CERT; N16 sub-obligation FW. C: M4/S-CERT exact card semantics; K73 region certification withheld. D: M4 + S-CERT (K64, K73 w/o region, K74). | S-CERT (K73 without region clause) + M4(e); N16 = FW16. |
| N8 | FW; S-BLOCKS conditional | A: FW (S-BLOCKS states SIZE). C: S-BLOCKS strict separation/SIZE; study/random pairing FW. D: FW line. | S-BLOCKS (preservation, SIZE equality); FW25. |
| N9 | S-KERNEL | A, C, D: same; CHK VERIFIED WITH AMENDMENT. | S-KERNEL (cited N9 with CHK amendments). |
| N10 | FW | A: FW (K24). C: S-IDENT named terminal-law bounds; useful general production mixing and masked population accuracy FW. D: K24 FW. | FW4 (K24); S-IDENT minorisation/terminal-law TV ship. |
| N11 | M5 hypothesis (ℓ ≥ 1 on LH); growing s₀ FW | A: M5 hypothesis ℓ ≥ max{Φ(S°) − 1, 0}. C: M5 capped scoring vs certification; growing support and cap nonbinding FW. D: M5(a) (ℓ ≥ τ(C)) + S-CERT. | M5 hypothesis (+ S-CERT); growing support / cap nonbinding = FW19. |
| N12 | FW; S-TARGET eventual exact dispatch | A: scope sentences in S-T, M5, M1(i); exponential p FW. C: S-T/S-TARGET scope; exponential dimension, growing support, broader random-design transfer FW. D: FW (exponential p); p ≤ n^A in scope. | FW18; FW19; S-TARGET K76. |
| N13 | M4(c) | A: M4(c). C: M4 retention lemma. D: M4(b) [D's lettering]. | M4(c). |
| N14 | (a),(b) S-OUT; (c) audit; (d) card per record | A: M1(c), M5(0) (R′ > 4 with extra search), S-OUT audit. C: S-OUT/M1/M8 declared stacking, baseline search retention and extended-stream audit. D: S-OUT (K84–K86) + M1 contract. | S-OUT + M1(c); N14(c) = named audit premise (MINUTES §2.3). |
| N15 | M8 | A, C, D: M8 (C: M7 supplies calibration simplifications; integrated DAG remains an audit premise). | M8; DAG audit named premise. |
| N16 | FW (K107); K108 in S-CERT | A: FW K107; S-CERT K108. C: FW K107; conditional K108. D: K107 FW; K108 S-CERT. | FW16; K108 in S-CERT. |
| N17 | M4(d) | A: M4(e)/S-TARGET [A's lettering]. C: M4/S-TARGET analytic and residual envelopes. D: M4(d). | M4(d) (final letter) and S-TARGET (K44). |

MINUTES §2.3 row on audit obligations (verbatim): 
| Audit obligations | N2(b), N2(c), N2(e), N14(c), the N3 DP invariant, and the integrated streams/LS0/GUARD-W/execution-DAG audits are **named implementation premises in the charters** and are recorded in `REGISTRY_PAPER1.md` (B's "missing" item 2, adopted) | — |

The obligations themselves, verbatim (`THEOREM_REVISION_INPUTS.md` lines 127–256):

<!-- BEGIN VERBATIM MEET-v31/THEOREM_REVISION_INPUTS.md §3:125-257 -->
Each: statement; hypotheses; status; decision supported; if it fails; INV §1 cell(s), row × column.

**N1. Measured-round island identity for general bounded h (Theorem H crux; V1(a2)).**
- *Statement.* Conditional on a successful frozen 𝓒, for each final island r and each h ∈ 𝓗 with 0 ≤ h ≤ 1, measurable in (X, y, 𝓒): E[Ẑ_r·H_r(h) \| 𝓒] = Z·π(h), with H_r(h) as in M9.
- *Hypotheses.* EX-A, EX-S, CAL, V5 (each φ = 1 round π-invariant), multinomial resampling, R′ declared before stream 10.
- *Route* (R2C `:200–204`): the finite-state resample–move recursion gives E[Ẑ_r η_{r,T}(f)] = Zπ(f); terminal rounds preserve π, so the identity holds at each measured endpoint and for their average. R3A (unchecked): the base case of the locked terminal-round lemma.
- *Status:* **PROOF SKETCH**; PC1 claim 3 takes it as a premise.
- *Supports:* M9, A1, C1(d) joint clause, D3(a) for general h.
- *If it fails:* the binding goal is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change (proposal §13.1, binding). Until that decision: μ̂(h) carries no theorem; A1 shrinks to marginal PIPs (locked); M4 survives (Prop P(ii) for PIPs).
- *Cell:* row 8 × V (islandwise identity, extended); row 10 × "NONE: joint inclusion probabilities".

**N2. Integrated v3.1 core: Prop W, W-cal, LS0, stacking, GUARD-W.** Code-audit facts plus executed replays, not mathematical theorems (TL:119).
- *Statement.* For fixed (X, y, seed, binary), process workers, Lemma S merges: (a) final islands bitwise equal to serial (Prop W); (b) the 4 diagnostic islands, with persistent per-worker stream state, bitwise equal to serial (W-cal); (c) LS0 leaves island outputs, Ẑ, PIPs bitwise unchanged, gives 𝒯_new = top_c(𝒯_old ∪ 𝒮_added), fires no E3; (d) R′ = 4k with the extra search leaves islands 1–4 unchanged and nests the post-search scored set; (e) **GUARD-W:** v3.1 worker, merge and LS0 code satisfy "any worker, LS0 or guard stop ⇒ no output" (an LS0 stop is an operational interruption; a completed capped LS0 returns `local_limit`) (new code-audit obligation, class (iv); S3 R3-5(ii)).
- *Status.* Lemma S PROVED. (a) PROVED by code reading, executed on smoke + 3/3 designs. (b) PROVED by code reading, **not executed**. (c) not in the production core. (d) PROVED (PC1 claim 6, deterministic). (e) **not audited** (API-AUDIT covered the serial v3 guard only).
- *Supports:* M2, M5, M6, M7, card G2 premise (i), "the 2,394 study fits' saved sampler estimates are reusable as v3.1" (full v3.1 records pending: LS0 integration and flags, NA interface, certificates, primary rescoring).
- *If it fails:* (b) → LAW-PRESERVING, wall-clock claims capped at the D4 table, "bitwise" claims narrow; (e) → CEX-guard applies to v3.1 (N6); fixes are engineering; decisions survive.
- *Cell:* row 8 × V; row 7 × V; row 12 × "NONE: LS0 absent from production"; row 14 × V.

**N3. LS0-based T38(b1-LH) about the shipped method; e4 tie-DP invariant.**
- *Statement.* For v3.1 with LS0, on LH exact Gram (p ≤ n − 1, c linked pairs, g_max ≤ B < 2g_min): P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, with no open statistical hypothesis. Sub-obligation: on truncation the tie-aware DP returns the prescribed smallest-size, lexicographically smallest maximiser.
- *Hypotheses.* EX-A, EX-S, CAL, SR, GUARD + GUARD-W, (P), (M1)–(M3) (verified on LH), **OP-LS0**, the **LS0 centre rule** (e4), **ℓ ≥ max{Φ(S°) − 1, 0}** (N11).
- *Status.* (b1-LH) PROVED (candidate), XF VERIFIED (A-REV8) for "v3 + LS0"; bridge to code = N2(c), not done. DP invariant **OPEN**. R3A and R3B sketch the same route (unchecked): greedy choice j = 1..p, keeping j iff some size-k_min maximiser consistent with earlier choices contains j, each test a max-plus feasibility DP over (block, remaining size) (`v3_start.h:179–200`); polynomial, no tie enumeration. Study: 0/2,400 truncated; all had one tie.
- *Supports:* M2, M12 e4.
- *If it fails:* headline falls back to (b2-LH) on STAB-LH without LS0; M2 survives (ADDITIVE; HPM unchanged 2,394/2,394) without theorem motivation.
- *Cell:* row 11 × A; row 12 × V/A.

**N4. Finite-R accuracy of the Ẑ-weighted PIP and μ̂(h); the constant M under masking (V11).**
- (i) PC1 claim 3: P(\|μ̂ − μ\| > ε) ≤ min{1, 4(M−1)/R + 4M/(Rε²)}, M = E[(Ẑ_r/Z)² \| 𝓒]. **PROVED**, given N1 for general h or the locked identity for PIPs.
- (ii) Prop P(iii) with M1 (PROVED, candidate): regime-free distance to 1{j ∈ S₀}.
- (iii) **Obligation:** an upper bound on M on the production grid through a masked crossing (V11, "resolved grid ⇒ O_P(√(T/N))": CONJECTURE, OPEN for c ≥ 2). Known lower bound M ≳ 1/P_𝓒(cross), PROOF SKETCH (TL A1(v)); do not cite F-MASKPIP M3 (XF ERROR).
- *Supports:* M4; M7's R′ guidance; R_eff reporting.
- *If (iii) fails:* M4 survives (R-consistency holds; equal-weight has none); the paper claims correctness, not efficiency.
- *Cells:* row 10 × A; row 9 × "NONE: two-sided relative accuracy of Ẑ (masked)"; row 8 × "NONE: island variance vs correlation"; row 7 × A.

**N5. Calibration contract.**
- *(a) Validity for any frozen 𝓒:* every final-run identity (V1, N1, N6) holds conditional on any successful 𝓒 on streams 0–9, final streams ≥ 10 independent. Status: assembly of T12/T31(i) (PROVED-LOCKED, conditional on 𝓒), IND-T (PROVED, XF VERIFIED*, A-REV1 only), Lemma RO; IND-T for streams 10..9+R′ is a code-audit item. ESS 0.90 (pilot = grid) is a hypothesis.
- *(b) OPEN* (all NONE in INV row 7 and §5 item 9): (b1) rebuild-loop convergence within ≤ ℓ rebuilds; (b2) P(S₀ ∈ V), "V contains the competing pair"; (b3) P(schedule_limit), P(grid_unconverged) → 0, incl. as-coded masked T_n (Conjecture P).
- *If (b) fails:* M8 **survives** (validity conditional on any frozen 𝓒); only delivery and efficiency suffer. Each is stated OPEN beside the POST HOC tabulation of rebuilds, tier, T, convergence.
- *Cells:* row 7 × V (a); row 7 × "NONE" (b1–b3 stay empty); row 14 × "NONE: P(schedule_limit)"; row 5 × "NONE: realised T_n".

**N6. Output-event coverage statements.**
- (a) P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05; {L > Z} = {0.05Ẑ > Z}.
- (b) Card level: P(𝒪 ∩ {some G2, L or R item false}) ≤ 0.05·P(SMC ∩ 𝒜).
- (c) Every result is joint with 𝒪, never conditional on it: "the probability that a run returns a card with a false claim is at most 5%".
- *Hypotheses* (PC1 claim 2): (i) Lemma RO + GUARD-W; (ii) successful 𝓒 with E[Ẑ̄ \| 𝓒] ≤ Z; (iii) CAL, EX-S; (iv) Ẑ = Z on the exact branch; plus EX-A and distinct store entries. Rigorous fp coverage also needs validated SC and VAL-FP (N16).
- *Status:* (a) **PROVED** (potential run; output form CORRECT WITH AMENDMENT). (b) **PROVED modulo premise (i)**, whose GUARD-W part is the code-audit obligation N2(e).
- *Supports:* M10, M11.
- *If premise (i) fails:* CEX-guard applies and the output-event statements fail for v3.1; fix is engineering.
- *Cells:* row 9 × V; row 14 × V.

**N7. Certificate card G1/G2/L/R (PC2 verdicts; card as adopted in M10).**
- *By item:* **G1** (C1(a) amended, excl. Ŝ) PROVED, deterministic. **G2** (C1(b)) PROVED, output event, joint. **L1** (C3(a); empty maxima +∞; fp margin 2η_F) CORRECT WITH AMENDMENT; on the finally returned Ŝ. **L2** (C3(b)) PROVED. **L3** (C3(c), realised 𝒮, \|𝒯\| ≥ 2) amended form PROVED; premise holds under LS0. **R** (C4 + Lemma M) PROVED with amendments (drop \|L\| > K leaves; S ⊆ U, \|S\| ≤ K; SC covers Φ and M); C4(b) PROVED as written (isolating {Ŝ} is sharpness only; R3C withdrew). Card bound (C6) PROVED modulo premise (i). C6′ PROVED.
- Budget and per-record clauses: as M10.
- *FALSE or not a theorem:* C1(a) third clause; C1(b) "unscored mass" (COUNTEREXAMPLE `t4b`); the conditional C6 reading; "SC checkable by replay"; rigorous `global_certified` (η uses a *lower* condition-number estimate); the C4 cost remark.
- *Excluded from the output:* C2 (conditional on PW2), C5 (needs S₀; a study-level item).
- *Open sub-obligation:* SC(η_F) by validated arithmetic and VAL-FP(η, ε) at production size (N16); until then, labelled numerical.
- *Supports:* M10. *If SC is never validated:* the label stays (POST HOC).
- *Cells:* row 13 × F (per-fit certificates, **not** flag power); row 9 × F; row 12 × "NONE: meaning of `local_certified`" (L1, deterministic); row 11 × F.

**N8. PART-pairing for the study generator g = 5 (2g ≤ B).**
- *Statement (as far as sources go):* a partition law for complete linkage + size cut + next-fit packing with equal groups 2g ≤ B (study g = 5, B = 14): which groups are co-blocked, and does that remove masking (Prop Q)?
- *Status:* **OPEN**; Prop Q **PROOF SKETCH** (R2B row 6′); W7-PART CE2 COUNTEREXAMPLE (unequal groups not merged).
- *Supports:* M12 e1. *If it fails:* e1 survives (changing B or the cut is WORKHORSE); the study generator is disclosed as outside every selection theorem.
- *Cells:* row 3 × "NONE: partition law for the study's packing"; row 11 × "NONE: study generator".

**N9. V5: kernel reversibility, self-adjointness, exact start sampler.**
- *Statement:* each elementary move (Gibbs flip, uniform swap, neighbour swap, independence move with π₀ proposal) is γ_φ-reversible; a uniformly random order of reversible kernels is self-adjoint; the start sampler draws exactly from π₀ with exact Z̄₀.
- *Status:* by construction, consultant-checked, **no registry row** (INV §5 item 12; TL:77); one-page route (TL V1(v)).
- *Closure gate (HQ, 2026-11-04):* N9 is a closure gate, not an ordinary obligation; it is being checked against the code (branch `theory/N9-KERNEL`). Open method questions: none, **conditional on N9** (running). If N9 fails, the method question reopens before the theorem meeting. Status words above unchanged.
- *Supports:* M1, V1, N1, rejection of C10. *If it fails:* V1 fails; the method question reopens before the theorem meeting. The binding goal (proposal §5.1) is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change.
- *Cells:* row 6 × V; row 4 × V.

**N10. V10: L versus t_mix.**
- *Statement:* do L = max(4, ⌈log₂(n+1)⌉) terminal φ = 1 rounds give populations close to π?
- *Status:* **NONE / OPEN** (INV row 6); YWJ/ZYVR route blocked as stated (INV §2 D1). Validity (V1, N1) holds at any L; L affects accuracy and variance.
- *Supports:* M1. *If it fails:* theorems needing mixing carry L as a hypothesis.
- *Cell:* row 6 × "NONE: mixing / spectral gap".

**N11. ℓ versus the moves needed.**
- *Statement:* ℓ = ⌈log₂(n+p+1)⌉ ≥ max{Φ(S°) − 1, 0} (moves LS0 needs, LS-score), and the caps on the final local search and rebuilds are not binding w.p. → 1.
- *Status:* on LH with c ≤ s₀ fixed, "eventually true" (R2B row 7; elementary, unchecked); growing s₀: **OPEN**.
- *Supports:* M2. *If it fails:* R3/R5 carry ℓ as a hypothesis; growing support would need a bigger budget (method-induced).
- *Cells:* row 12 × C/A; row 7 × C (rebuild cap).

**N12. General (n, p) scope, per regime** (S2 P-9 theory scope; R2A–R2C §4).

| Regime | What theory may claim | Cause of any restriction |
|---|---|---|
| Tiny n | No asymptotic claim. n ≤ 5 exact for **all p** (chair-checked). n = 2 extension (e3, proposed; current code rejects n < 3): PROOF SKETCH (R2C E1); its p-fold-tie output statement (M12) is R3B's, elementary, **seat-derived, unchecked**; duplicates kept (chair-checked), which is a code fact, not a proof of the n = 2 output. n = 1 → `degenerate_n`; zero predictors → `no_predictors`; n = 0 rejected. | None from the method. |
| Fixed p, n → ∞ | Eventually exact dispatch (R2C §4.4, seat-proved, unchecked), so V2–V4 apply. | — |
| Growing p ≪ n | Polynomial-p target results under their assumptions; logarithmic L, ℓ may be short (N10, N11). | Method budgets (theorem hypotheses). |
| p ≈ n | Exact-Gram LH needs p ≤ n − 1; centred designs have rank ≤ n − 1. | Proof family's geometry, not the target. |
| Polynomial p ≫ n (p ≤ n^A) | T03/T03♯; T38(b1-LH-iid) XF GAP; study generator N8. | **Prior and proof technique** (INV §3b), not the sampler. |
| p ≤ e^{Cn^α} | No theorem; whether our prior admits it is **OPEN**, not impossible. | — |
| Joint growth | Budgets polynomial; by-definition limits: fixed allocation, Θ(p) round; w4 boundary n + p ≥ 2³¹. | Method-induced: K excludes s₀ > K; fixed B limits whole-group recovery to g ≤ B ("recovery as a single block", R3C); bounded stores; log ℓ and L; N₀ ≥ p. |

w1 and w3 affect proposal efficiency only; validity rests on the Hastings ratio.
- *Cells:* row 1 × A and row 1 × "NONE: growing s₀"; INV §3b "p up to e^{Cn^α}: LACK".

**N13. Retention lemma.** If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 = top_{40p+1}(𝒮), and the HPM and MPM^𝒯 certificates are equivalent.
- *Status:* **PROVED** (PC1 claim 5; R2C D7); premises Lemma S and the inheritance merge (PC2 code facts). Unqualified retention stays false.
- *Supports:* A3 ∘ R5, card L3, M2's eviction wording. *Cell:* row 11 × A.

**N14. Stacking statements.**
- (a) Cor W-R(b): post-search nesting, HPM(R′) ⪰ HPM(4) with the extra search. PROVED (PC1 claim 6).
- (b) Every listed bound holds per run for any R′ declared before final randomness (PC1 claim-6 table).
- (c) IND-T for streams 10..9+R′: code audit, not done.
- (d) One certificate card per record (M7, M10).
- *Supports:* M7. *Without the extra search:* PC1's three uses (monotonicity, D_n(R′) ≤ D_n(4), transfer of R = 4 measurements) go; no listed theorem affected.
- *Cell:* row 8 × V; row 8 × "NONE: choice of R vs N" (D4 PROOF SKETCH, v2).

**N15. Work and depth at the implemented level** (D1(b) restated).
- *Statement:* depth and work for island-parallel v3.1: setup, (h) tables, calibration ((1+4I_e)·H_e work and (1+I_e)·H_e depth per tier; ≤ ℓ rebuilds per tier, ≤ 2ℓ with escalation), final run N_e(T+L+4)m sequential step slots (not scorer operations or seconds; add score costs and finite-worker scheduling; R′ above the worker count runs in waves), LS0, extra search, population reductions.
- *Status:* Prop D PROVED (counting); calibration share seat-derived (R2A, R2B), not proof-checked.
- *Supports:* M5, M8, M13. *If it fails:* recount.
- *Cells:* row 8 × "NONE: work–depth theorem" (filled as counting; speed-up vs sequential MCMC stays empty, empirical); row 7 × C; row 5 × "NONE: depth vs correlation" (ideal grid via A₀ only).

**N16. Floating-point contract.** Validated SC(η_F) for scores, Φ, M, Z_𝒯⁻, and VAL-FP(η, ε) for Ẑ at production size.
- *Status:* **OPEN.** VAL-FP MEASURED at p ≤ 40 only; η a documented heuristic (`v3_score.h:240`); PC2's exact-rational test found no violation in 60 cases (max \|error\|/η = 0.069): not a proof.
- *Supports:* M10 labels, G2 fp coverage, e2, e5. *If never done:* labels stay "numerical".
- *Cells:* row 14 × "NONE: floating-point error theorem"; row 9 × "VAL-FP MEASURED at p ≤ 40 only".

**N17. Analytic bounds on Z and π(Ŝ).** Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}; equivalently π(Ŝ) ≥ e^{F(Ŝ)}(2b₀ + yᵀy/(n+1))^{ν}/C_n.
- *Status:* **PROVED** (PC1 claim 1; PC2 C1(c)). Its gap to Z is data-dependent: the ≈ 530-nat figure at n = 200 compares against m(∅), not against Z, and is not a universal looseness (n = 200, p = 1, y = x₁ gives log(U/Z) = 3.83; review check, SOL1 #27). Supports M14(ii).
- *Cell:* row 9 × "NONE … an upper bound on Z is impossible from a run": **INV's wording is literally false**; correct to what is proved (T31(c)'s non-implication plus this bound), not to a blanket "no useful upper bound".

**N18 (only under item-1 Outcome 1). Depth comparison between starts.** Under stated conditions, the block start's A₀ (or realised T) ≤ that of the singleton or prior start.
- *Status:* **OPEN**, no route in the sources. *If not attempted:* the depth claim stays empirical.
- *Cells:* row 4 × "NONE"; row 5 × "NONE: depth vs correlation".

**Carried over unchanged (already in TL):** DELIV-POP (A4, OPEN); Conjecture P (in N5(b3)); Π(X) upper bound (R7); LH-iid XF GAP (R5); S4 weight stability (§5.3).

**Not obligations:** the HPM terminal frequency (descriptive, M9); an RB joint estimator (not shipped; as a v3.2 option it would need its own identity, R3A/R3B).
<!-- END VERBATIM MEET-v31/THEOREM_REVISION_INPUTS.md §3:125-257 -->


---

# A6 · Coverage: proposal goals and Song–Liang items → IDs (condensed)

Full file: `MEET-THM/COVERAGE_MATRIX.md` (every proposal goal, Song–Liang item, THM-INV §1 cell and obligation N1–N17 → list item / FW / cited lemma; with the four seats' references and differences; also "Items the seats named as missing"). Final-card lettering governs: M1 (a)–(i); M4 (a)–(g); M2 (a1)–(c2); M5 (0), (a), (b1-LH), (a-fav), (b2-LH); M7 (a)–(f).

## A6.1 Proposal goals (condensed; "Final" column of COVERAGE_MATRIX §(a))
| Goal | IDs (native in parentheses) |
|---|---|
| §5.1 exactness under MH correction | TH01 (M1(a), cited validity); TH12 (S-KERNEL, N9 with CHK amendments); TH10 (S-TARGET). Numerical fidelity = CJ16 (FW16, K107/N16). "Failure of foundational correction escalates." |
| §5.2 SMC consistency | TH01 (M1(a),(f),(i): cited fixed-data limits Del Moral 2004; Del Moral–Doucet–Jasra 2006; Whiteley–Lee–Heine 2016; finite-R′ bound; asymptotic with R′_n); TH17 (S-POOL) |
| §5.3 weight stability (binding) | TH02 (M2 (a)(b)(c) with scale disclosure); TH03 (M3, d_σ); TH07 (M7, count and coverage identity); TH06 (M6, Lemma KL); TH20 (S-LEAK); CJ22 (FW22, sharp ε-scale necessity). Safeguard: both routes fail ⇒ escalates |
| §5.4 PIP error | TH01 (M1 (e),(f),(h)) for marginal PIPs (RB record); TH04 (M4(b)) reported-store PIP bracket |
| §5.4 joint-PIP error | TH01 (M1(g): h_A = 1{A ⊆ S} on ≤ 2pB declared pairs, plain averages); TH04 (M4(b)) joint inclusions in the store |
| §5.4 TV | TH04 (M4(a) deterministic TV(π_𝒯, π) = 1 − Z_𝒯/Z; (b),(d)); TH02 (M2(a) start TV ≤ tanh(osc d/2)); TH12/TH13 terminal-law TV (C15-TV); TH17 (P1); TH03/TH06. Masked final-estimate TV = CJ02 (FW2, not binding) |
| §5.4 KL | TH02 (M2(a): KL(π‖π₀), KL(π₀‖π), J ≤ D_*); TH06 (Lemma KL, K105); TH04 (M4(a),(g)); TH13 (C15-KL). Masked final-estimate KL = CJ02 |
| §5.4 credible-interval coverage (HQ Q2: posterior-content error) | TH13 (S-IDENT clause **C15-CI**, named); TH01 (M1(g): h_I, union bound, "posterior-content error only, no quantile claim"). Frequentist coverage of the exact posterior = CJ01 (FW1) |
| §5.4 masked accuracy (HQ Q3) | TH04 (M4(f)) composed with TH05 (M5 (b1-LH)) and retention M4(c); regime-free brackets M4(b),(d) and Ẑ < Z_𝒯 ⇒ Ẑ < Z; CJ02 (FW2) not binding; "Loss of the statement without approved replacement escalates" |
| §13.1 E_π[h] → truth (binding) | TH01 (M1 (b),(e),(i) with the growth-rate configurations); TH19 (S-REP) is an application; unbounded functionals = CJ27 (FW27); "N1 fails ⇒ narrower theorem ships and §13.1 escalates" |
| §4.4/§8.2 diagnostics | TH07 (M7(b) coverage identity); TH04 certificate card; TH14 (S-CERT); TH19 (S-REP); TH18 (S-LIM, K79). Flag power K80 = CJ17 (FW17) |

## A6.2 Song–Liang (2015) items
Wording for Thm 2 and Cor 2 is MINUTES §2.3 R3-7 (binding), verbatim: 
| R3-7, Song–Liang wording | **Thm 2:** "fixed-design, fixed-sparsity selection counterpart only; SL's predictor-tail and prior hypotheses are not transferred". **Cor 2:** "no analytic null-exclusion/FDR separation established; LIT-PAR G4 numerical evidence" (C's wording; adopted by B and D) | — |

| SL item | Final disposition (IDs) |
|---|---|
| Thm 1 | TH09 (S-T) supplies the target-selection counterpart; Hellinger/predictive contraction = CJ20 (FW20). "No claim of domination." |
| Thm 2 | TH09 (S-T): "fixed-design, fixed-sparsity selection counterpart only; SL's predictor-tail and prior hypotheses are not transferred" |
| Thm 3 | TH09 (S-T) large-signal inclusion; reported PIPs TH01 (M1(e),(f),(g)) and TH04 (M4(b)) restricted store |
| Thm 4 | TH03 (M3) with TH02 (M2(a)): "specific start-distortion analysis; compared, not exceeded"; TH06 context |
| Cor 1 | CJ18 (FW18): exponential-p contraction/selection (N12 = OB12) |
| Cor 2 | CJ21 (FW21, K97): analytic separation. "no analytic null-exclusion/FDR separation established; LIT-PAR G4 numerical evidence" (cited as labelled numerical evidence) |
| Thm S (supplementary) | TH09 exact-HPM counterpart; TH05 (M5) reported-HPM on LH (additional) |
| §6 complexity | TH08 (M8): same-unit island work/depth accounting; "no same-order, exact-output or speed claim"; accuracy-matched comparison = CJ12 (FW12, K92); K91 dropped = DR05 |

## A6.3 THM-INV §1 rows 1–14 (condensed)
Row 1 Target → TH10/TH09; CJ14, CJ20, CJ18/CJ19. Row 2 Exact branch → TH10 (K76); CJ16. Row 3 Partition → TH11 (SIZE); CJ25. Row 4 Start → TH03/TH12; CJ25; backfit start outside the method. Row 5 Bridge/grid → TH07 (a)–(d), TH02(b); CJ06. Row 6 Moves → TH12/TH13; CJ04, CJ05. Row 7 Calibration → TH01(c), TH07; CJ06. Row 8 Islands → TH08, TH02(b5), TH16; CJ09, CJ24; DR05. Row 9 Evidence → CJ24 (FW24, separate from CJ02); CJ16; TH14 (K108). Row 10 PIPs/MPM/UQ → TH01(g), TH17, TH13 (C15-CI); CJ07, CJ08, CJ01, CJ02, CJ27. Row 11 HPM → CJ13, CJ26, CJ25. Row 12 Local search → TH14 (K64), N2(c) premise of TH05, N3 (OB03) with K09 in TH12. Row 13 Flags → CJ17. Row 14 Resources/numerics → CJ13, CJ06, CJ16; CEX-guard cited in TH01(c).

## A6.4 Obligations N1–N17 → final placement
OB01 (N1) TH01 Lemma N1 (binding §13.1); OB02 (N2) named implementation premises in TH01, TH04, TH05, TH08 and LP-AUDIT; OB03 (N3) named premise (e4) + K09 proposition in TH12; OB04 (N4) (i) TH01(f), (ii) TH17, (iii) TH02(b5) on the domain, masked precision CJ24; OB05 (N5) (a) TH01(c), (b) CJ06; OB06 (N6) TH01(d), TH04(e), TH15; OB07 (N7) TH14 + TH04(e), N16→CJ16; OB08 (N8) TH11 + CJ25; OB09 (N9) TH12; OB10 (N10) CJ04; OB11 (N11) M5 hypothesis + CJ19; OB12 (N12) CJ18, CJ19, TH10 (K76); OB13 (N13) TH04(c); OB14 (N14) TH15 + TH01(c); OB15 (N15) TH08; OB16 (N16) CJ16; OB17 (N17) TH04(d) and TH10 (K44).



---

# A7 · Conflicts and uncertainties found between sources

- **U1 — second growth rate (ii).** MINUTES §2.3 row "§2.6, growth rates" and `AMENDMENT_HQ_02_DEFINITIONS.md` §B list "Two optional stacking configurations" (i) R′_n = 4⌈log₂(n + p + 1)⌉ and (ii) R′_n = 4⌈(n + p)⁶/4⌉; TLF M1 integration note 2 and the S-REP decision note repeat "the two stacking configurations"; NOTATION.md row R′ says "AMEND:63–64 fix the two optional rates". HQ's decision ([pos 1639]; `MEET-v31/AMENDMENT_HQ_02.md`; METH31 last paragraph) adopts only (i) as a method configuration and keeps (ii) "only as a sufficient rate inside the theorem (M1's simultaneous-control clause)". The M1 card text as printed (TLF 111) has only the log rate in (i); how the final M1 states (ii) is not recorded. The user task text paraphrases (ii) as "R′ ≥ c(n+p)^6"; the sources say 4⌈(n + p)⁶/4⌉.
- **U2 — size of the early draft list.** HQ quotes "19 items" ([pos 1280], [pos 1302]; "a draft list of 19 items in six groups", [pos 1201]) and then corrects to "The draft list has 24 entries, not 19" ([pos 1492]); `MEET-THM/MINUTES.md` §1 uses 24.
- **U3 — which "inherent limitations".** Three counts coexist: MEET-v31 MINUTES §5 has 9 numbered items (item 6 is a "moved" stub); THEOREM_REVISION_INPUTS §4.A has I1–I7, I9–I11 (I8 moved), including I4 (one-shot IS needs ≈ Q*), I10 (equal-weight bias), I11 (sequential rebuilds) that are absent from the MINUTES nine; FOR_FELIPE_FINAL_METHOD §4 lists 7. This draft registers the MINUTES nine (HQ also says "nine" at [pos 1280]).
- **U4 — M1 K-ID header.** The card line reads "K46, K32, K86, K85, K36, K78, K51, K52, K48, K62; cited K20, K21, K08, K35, K47"; MINUTES §2.1 reads "K46, K32, K86, K35, K36, K50, K51, K52, K48, K62; cited K20, K21, K08, K47"; the registry follows MINUTES (TLF integration note 1).
- **U5 — M5 δ₁.** The card writes "δ₁ := E₀[1 − π(S₀)]" and then uses it pointwise; TLF integration note 4 (CLOSE_AUDIT #7) fixes: read δ₁ := 1 − π(S₀) pointwise in the deterministic clause and keep 2E₀[1 − π(S₀)] + D_n in the probability bound. The verbatim card block is unchanged.
- **U6 — number of N9 sub-claims.** HQ [pos 1550]: "All 7 sub-claims are PROVED (candidate)"; [pos 1593]: "All 8 sub-claims are PROVED (candidate)"; MEET-v31 MINUTES §9: "all seven sub-claims". Not reconciled in the snapshots.
- **U7 — S-STGI/K29/K30 propagation.** The v1 minutes misreported A's vote; CLOSE_AUDIT #4 says old vote text survived in TLF 831/833, the registry and charters; the snapshot of TLF has the corrected heading (line 830), M2 charter wave row is corrected, but this draft did not re-audit REGISTRY_PAPER1.md. Treat "K30 = M7(d); K29 = FW23 (CJ23)" as final.
- **U8 — N2(b).** TLF registrar note says the label N2(b) "is not defined in any R3 file; its definition is in THEOREM_REVISION_INPUTS.md (N2), which is not on this branch". It is on MEET-v31 (N2(b) = W-cal: the 4 diagnostic islands bitwise equal to serial; see OB02 above).
- **U9 — line-number drift.** FUTURE_WORK.md cites `MINUTES.md:94–99` for the drops, `MINUTES.md:78,84` etc.; in the snapshot the drops are at lines 98–103. Content is identical.
- **U10 — order of supplement cards.** MINUTES §2.2 lists S-T, S-Z, S-TARGET, S-KERNEL, S-CERT, S-LIM, S-POOL, S-IDENT, S-BLOCKS, S-OUT, S-STGI, S-LEAK, S-REP; TLF header table order (used for TH09–TH20) differs. IDs follow the TLF order.
- **U11 — "Seat D".** Seat D is called "fresh-eyes Fable" in FOR_FELIPE and [pos 1584]; NOTATION lists the seats as A (Fable 5.1), B (Fable 5.1), C (gpt-6-astra), D (Fable 5.1). Not otherwise contradicted.
- **U12 — status of the method approval.** METH31 header says "Not yet approved by HQ or Felipe" (text written before the approvals); HQ approved at [pos 1557]/[pos 1584] and Felipe approved the four decisions at [pos 1304]; FOR_FELIPE_FINAL_METHOD says "Approved by HQ after the method meeting". Felipe's approval of the theorem list: not recorded (see §A0.2).
- **U14 — date of Felipe's island-level-depth decision.** METH31 §3 and MEET-v31 MINUTES say "Felipe decided (2026-11-03) that paper 1 claims island-level depth only". In the transcript HQ proposes it at [pos 1263] (2026-11-03T19:41Z) and as decision 2 at [pos 1302] (2026-11-04T00:01Z); the recorded approval ("All approved") is at [pos 1304] (2026-11-04T00:05Z). No content conflict.
- **U13 — seat-checker mapping.** The task description calls the cross-family waves "Sol" and "Opus"; the files call them PC1 (gpt-6.1-sol, on Seats A, B, D) and PC2 (Opus 5.5, on Seat C); inherited-proof check = PC1 ("CHK").

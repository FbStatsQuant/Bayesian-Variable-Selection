# G4 digest — cross-family (Astra) reviews, draft track (A-DRAFT, F-DRAFT), and F-REFEREE

Sources: `src/<ID>/` snapshots of `origin/theory/<ID>:theory_campaign/<ID>/`. Context: `Docs/THEORY_PRIORITIES.md`,
`theory_campaign/LEDGER.md`. Statuses are quoted verbatim and never upgraded. "Astra" = GPT-6 Astra (A-REV1–4, A-DRAFT).
"Opus" = the W1–W6 / O-* authors and same-family verifiers. F-DRAFT and F-REFEREE are **Fable 5.1**, not Opus or Astra.

| Branch | Head (`_HEAD`) | Author | Base / snapshot | Reviewed-version check |
|---|---|---|---|---|
| A-REV1 | `26815e8` 2026-11-02T12:44:28-06:00 | GPT-6 Astra | campaign base `00c7b340622f…` | All six pins equal the current source heads (not stale) |
| A-REV2 | `09dc230` 2026-11-02T12:45:24-06:00 | GPT-6 Astra | baseline `00c7b34`; SOURCES.md | All seven pins equal current heads (not stale) |
| A-REV3 | `522d83d` 2026-11-02T13:29:23-06:00 | GPT-6 Astra | local baseline `816ec72`; text says "Evidence checkpoint head SHA: ae97136" | Both pins equal current heads (not stale) |
| A-REV4 | `b95948c` 2026-11-02T13:25:47-06:00 | GPT-6 Astra (+ "Sol helpers" for BOOK_CHECK/DRAFTS_CHECK) | base `816ec72`; text says "Reviewed-content checkpoint head SHA: 34e4f48…" | All four pins equal current heads (not stale) |
| A-DRAFT | `dbf47f7` 2026-11-02T12:57:16-06:00 | GPT-6 Astra | base `325b0d8`; W snapshots in `results/campaign_refs.txt` (not in my snapshot) | — |
| F-DRAFT | `4de6e4c` 2026-11-02T12:57:16-06:00 | Fable 5.1 | — | — |
| F-REFEREE | `fae6b7f` 2026-11-02T13:51:52-06:00 | Fable 5.1 | parent `6ca6165` (Ledger: Wave 7) | Reviewed only A-REV1/A-REV2 as cross-family input; **did not use A-REV3/A-REV4** although those were pushed ~20 min earlier (see §8) |

LEDGER cross-check: "Draft track done: F-DRAFT @ 4de6e4c, A-DRAFT @ dbf47f7. S-PAPER @ 556be30. A-REV1 @ 26815e8, A-REV2 @
09dc230 (repairs in W6-FIXREV1/2, cloud)." LEDGER scopes: A-REV1 "Theorem B, T38(b)-R, Lemma S, D2, E3"; A-REV2 "T03♯,
refined T37, EXP′"; A-REV3 "W3-PXN, W4-SHARE, Prop M" (the Prop M is **W4-SHARE's Proposition M**, reviewed as "W4 M(a)/M(b)";
not A-DRAFT's Proposition M); A-REV4 "W2-T26, W2-BOOK/Lemma RO, F-DRAFT, A-DRAFT §2". Credit repairs: "W6-FIXREV1 (A-REV1),
W6-FIXREV2 (A-REV2)" — those repair branches are not in this digest's sources.

---

## 1. A-REV1 (head `26815e8`)

Reviewer line: "Reviewer: GPT-6 Astra; date: 2026-11-02; branch: `theory/A-REV1`."

**Pinned sources (§1 table, full SHAs):**
- theory/W1-T24G `9e210a3fafbc074cfbbcae18dafc5c8547e81af1`
- theory/W2-VT24G `dba6ff4c12e0510c5a48bf733b1623834aa21c64`
- theory/W2-PREM `988c5f55c0fb0fbd6050b6a4d0c75f14159716e3`
- theory/W1-T38E `436a7125ace4853eb9d2507513f53db9c47b3825`
- theory/W3-VT38E `3e4b732aff517140a124ac1f380410ee95a0d705`
- theory/W1-EXP, "only the imported Lemmas 1.1–1.4", `722bd18e51fcc3b485c07590097e137dac71a5aa`
- Campaign base `00c7b340622faeb4466c93d92f91c830e4ccdaff`. All equal the current heads in `src/` → **not stale**.

**Headline (verbatim):** "**The finite Gibbs-path bound survives independent review after the F′ repair. The supplied package is
not ready for an unqualified verification: Proposition U, Lemma S's attainment sentence, E3(ii), and Lemma U's printed limit
contain errors; the T38 composition needs explicit rate, eligibility, and execution qualifications.** The corrected D2 constant
is right."

Convention: "**VERIFIED** means the specified implication or step checks under the qualifications in its row. **GAP** means an
absent premise, inference, or operational bridge… **ERROR** means a false assertion, with a counterexample or exact calculation".

### 1.1 Verdict table (verbatim verdict words)

| Claim / step | Verdict | Qualification (abridged quote) |
|---|---|---|
| Theorem B, restated T24, finite inequality | **VERIFIED after F′ repair** | "use the full definition of bad, feasible families, and executed or potential uninterrupted rounds" |
| Lemma F standalone | VERIFIED | |
| W1's invocation of F in B2's slot argument | GAP, repaired | "Nonfailure need not keep the state in the restricted family… F′ supplies the required union bound." |
| Lemma F′ | VERIFIED | |
| Lemma O(i)–(iii) | VERIFIED | |
| Lemma C and block bound | VERIFIED | "for integer k≥1" |
| Lemma P exact formula + single-target bound | VERIFIED | |
| Lemma P informal multiple-target sentence | GAP, fixable | explicit version in §4 |
| **Proposition U, as written** | **ERROR** | "Independence moves can remove a truth without raising V or leaving the family. Also, an extra-for-extra swap need not stay in the phase-1 family." |
| B1 phase-1 progress | VERIFIED | |
| B2 phase-2 progress | VERIFIED after F′ | |
| c₂≥1/(B+3)−ε_del | VERIFIED | |
| B1′/B2′ (W2-VT24G) | VERIFIED with empty-supremum convention | |
| Corollary P1 | VERIFIED | |
| Corollary B-M | VERIFIED under IND-T | "does not prove the presence of eligible particles" |
| **IND-T** | **VERIFIED for the uninterrupted process** | "Completion conditioning or globally fresh-score sets are not covered." |
| **Lemma U, finite uniform expansion** | **VERIFIED** | family-count convention §5 |
| Lemma U, κ_n→0.52/c_E | ERROR | "Its displayed formula tends to 0.51/c_E." |
| CE1 deterministic exit lower bound | VERIFIED | "independent small BVS example has an exit lower bound above 0.14" |
| CE1 broad asymptotic wording for correlated designs | GAP as a blanket claim | narrow repair §5 |
| W1 §6 premises imply Hη→0 | GAP | "sup of a sum is not the sum of sups used in η. W2-PREM corrects NL0's quantifiers but adds genuine assumptions." |
| **Lemma S, ESS share inequality** | **VERIFIED** | |
| Lemma S "attained by two-level weights" on full domain | ERROR | "Positive equality weights require f>1−e… At f=0.05,e=0.9 the proposed low weight is negative." |
| **Theorem D2 with r*=(11+2√10)/9** | **VERIFIED as a finite uninterrupted-pilot bound** | |
| D2-∞ | VERIFIED under its additional uniform hypotheses | "Fixed b>0.1, bounded dangerous set, Dep bounded below 1, and vanishing NB failure are required." |
| **Theorem E3, TD′ + eligibility ⇒ LS0 scoring, and (i)/(iii)** | **VERIFIED with centre scoring and completed scans** | "T27-H3 remains a premise. LS0 is a method extension." |
| **E3(ii), as printed without q<1** | **ERROR** | "drops an explicit hypothesis of locked T22(i-a)" |
| E3 computation and scan budget | VERIFIED with accounting clarification | "Add one initial centre evaluation when counting all LS0 score calls." |
| **T38(b)-R, entire supplied statement** | **GAP** | "Route (b1′) omits asymptotic rate margins; route (b2)'s use of B needs an eligible set and the binomial bound; operational qualification must cover pilot and terminal execution." |
| T38(b)-R route (b1), direct ELIG+TD′+OP | VERIFIED | "Do not use the erroneous unrestricted E3(ii) shortcut." |
| T38(b)-R route (b2), given uniform REPAIR and actual execution | VERIFIED as an implication | |
| T38(b)-R repaired formulation §7 | VERIFIED as a conditional implication | "Does not establish DELIV, statistical repair premises, or vanishing operational failures." |

Overall (verbatim): "the **overall finite Theorem B verdict is VERIFIED after the existing F′ repair**; its unconditional
statistical application remains GAP. The **overall corrected finite D2 verdict is VERIFIED** under its operational idealisation.
The **overall E3 package as printed is ERROR because of clause (ii)**, while the core deterministic implication is VERIFIED. The
**overall T38(b)-R verdict is GAP**, with a complete conditional repair below. The **overall ESS Lemma S package is ERROR only in
its global attainment claim**… The **overall finite Lemma U and IND-T conclusions are VERIFIED**…; U's printed limiting constant
is ERROR."

### 1.2 Specific errors / gaps (with severity as I read it)

1. **Prop U (W1-T24G PROOF §3, lines 145–157) — ERROR, bookkeeping; does not refute Theorem B.** §0 defines bad = leaves family,
   raises V, **or removes a present truth**; §3's independence-move "iff" drops the third. Counterexample S₀={1,2}, x=∅, A=∅,
   c=a=0, W={1}→W′={2}. Second counterexample: S₀={1}, A={2}, W={2}, swap 2→3 leaves the phase-1 family. Repair: define Bad(W) by
   all three tests; extra-for-extra neutral only when it stays in the family. "Theorem B already uses the full §0 definition, so
   these errors do not refute its finite inequality."
2. **Lemma S attainment (W1-T38E PROOF §3; also W3-VT38E's unqualified "tight") — ERROR, ancillary.** w_A = 1 − sqrt(c(1−f)/f)
   positive iff f>1−e; at e=0.9, f=1/20 bound −0.0226483157, w_A=−0.4529663145. Repair: ω(A) ≥ max(0, f − sqrt(f(1−f)(1/e−1)));
   equality only for 1−e<f<1. "D2 uses f>0.1 and e=0.9, entirely inside the valid equality range."
   r* confirmed: witness 77 weights 1 and 40 weights 1.925, ESS/H=0.89999269486449; r*=(11+2√10)/9=1.924950591148529. "The
   user's corrected constant is therefore VERIFIED."
3. **E3(ii) (W1-T38E PROOF §6.3 line 134) — ERROR, substantive (missing hypothesis q<1 of locked T22(i-a)).** Counterexample n=20,
   p=2, orthogonal columns ‖x‖²=19, y=x₂, B=1, x°={1}: r₁≈0.2236068, r₂≈1.935517816213×10¹², claimed bound
   (1−q)²/(1+e)≈1.983334052945×10²³ vs π₀({1})≈9.441607620478×10⁻¹⁴. Repair: insert 0≤q<1. "This missing condition also applies
   to any T38 shortcut that tries to establish ELIG through E3(ii)."
4. **Lemma U limiting constant (W2-PREM PROOF §2, lines 135–137, inherited from W1-EXP) — ERROR, arithmetic only.** κ_n→0.51/c_E,
   not 0.52/c_E (AR example 18.4314 vs 18.7928). "No finite inequality needs to change."
5. **W1 §6 asymptotic premise — GAP.** NL0 written with sup_W Σ_l, η is Σ_l sup_W; array a_l(W_j)=1/p·1{l=j} gives 1/p vs 1. W2-PREM
   §0 redefines correctly. "Neither uniform repair on all R_d nor Hη→0 follows from the finite theorem alone."
6. **CE1 blanket correlated-design claim — GAP;** narrow explicit sequence given: p_n=ceil(n^(1/3)), S₀={1}, corr(x₁,x₂)=r,
   Y={3}, gives η_n ≥ (1−o_P(1))/21, so (L+4)η_n cannot vanish. "It does not promote W1/W2's broader sketches. It also does not
   refute Theorem B… it refutes the vanishing uniform-exit premise on the original R_d."
7. **Lemma P multi-target sentence — GAP, fixable:** P*(x) ≥ s_min|C|/(|C|+|D|)·[1 − Q/(|C|+|D|+1)].
8. **Boundary conventions for Theorem B** (H=0, a=0, c*≤0): define β_H(x)=min(1, P(Bin(H,c*)<v)+Hη). "An undefined negative
   binomial parameter is not a 'trivial' distribution." B-M: "The phrase 'no η→0 needed' is valid for a fixed H and sufficiently
   small fixed η; if H grows, beta<1 already requires Hη<1."
9. **IND-T scope:** "globally first-ever fresh evaluations" are not a per-particle independent output; H′=L+5 only before stage-T
   move round, H=L+4 after; "conditioning on observed completion or diagnostics is not a repair for an abort issue" (fair-bit
   example P(00|equal)=1/2 vs 1/4).
10. **T38(b)-R gaps (§7):** 7.1 route (b1′) lacks rate margins ("Finite D2 imposes no Dep<1 condition: Dep≥1 gives beta=0");
    repair via D2-∞ with fixed b₀>0.1, bounded k_D, Dep≤1−c₀, P(NB′ᶜ)→0. 7.2 "The new B is not uniform REPAIR on every R_d";
    define a data-measurable eligible set X_n; "D3 requires the *sum* of its SHARE and EXIT-end terms to vanish". 7.3
    "Completion and launch cannot be hidden in U"; "U means **no usable HPM**, not every failure to execute a planned segment";
    "Use K=min(p,floor(n/2)), not floor(n/2) alone as written in the T38 setting." 7.4 repaired composition
    P(U or wrong HPM) ≤ P(U) + 2E₀[δ₁] + P(Uᶜ∩M), plus the A/E execution decomposition; "Recovery tending to one additionally
    requires P(U)→0. This is a conditional composition result; no delivery or completion probability has been established".
11. **Citation fix:** "T38's incidental 'T11(vii)' citation should be replaced by the directly applicable locked T21(C1)".
12. **LS0 implementation detail (§6):** `local_search` evaluates its centre with `emit_centre`; "LS0 starts at a new centre, so
    its first evaluation must be offered to the HPM (`emit_centre=true`…)… Reusing that default for a new mode can miss S₀ when
    the mode itself is truth." Score budget: "allow **1+(ℓ+1)max_{k≤K}[p+k(p−k)]** for the initial centre as well." "None of this
    implements LS0 in the production method; adoption remains a separate decision."
13. **D2 pilot caveat:** "NB′… is a valid weaker hypothesis than the corrected discrepancy-range condition. The candidate-grid
    **restricted** ESS rule is a different object and supplies no substitute for this empirical pilot step."

### 1.3 Reproductions (§9)
Wrapper `owls_run -j 2`; local venv NumPy 2.0.2 (first system-Python attempt lacked NumPy). Seed 20261102. Script
`scripts/check_review.py`, outputs `results/independent_checks.json`.
- ESS share: 2,000 random cases, worst slack −3.72×10⁻¹⁵. r* and 1.925 witness as above.
- Shared-stream independence: all 256 length-8 binary streams, residual 0 ("not a PRNG audit").
- Lemma U: p=8, k=3, 232 additions at n=200 and 800; max |remainder| 0.6166, 0.6324 vs κ=18.7244, 18.5046.
- Exact small round p=4, B=2, all 40,320 orders (DP, no Monte Carlo).
- Theorem B: 45 start/horizon checks, 12 bounds below one, no violations (H=1,2,4).
- P1: four distance-one starts, a₁ ∈ [0.2763, 0.4970] — "not presented as production B=14/16 constants."
- D2 round ingredient beta=0.1620095 below exact hits at φ=0,0.3,1.
- Kernel balance residual 2.35×10⁻¹⁵. CE1 exit bounds 0.1525 (n=200), 0.1506 (n=800), Lemma E ≈1/7.
- E3(ii) counterexample as above.
- Non-independent reruns of prior referee code: CF(1) D2 (n=400, p=89, B=9): b=0.9278, Dep=0.0910, beta=0.0454; "The full
  two-exponential bound is **2.244×10⁻⁷ plus P(NBᶜ)**, whereas 3.133×10⁻⁹ is only the last exponential with t=0. Three pilot
  replications all scored truth and none violated NB. Three successes do not establish a small NB-failure probability."
  LS0 reproduction CF(2) seed 1 n=400 p=89 B=9: start-mode mass 0.8521410, path {1}→{1,2}→{1,2,3}, truth scored.
- "I did not compile the Rcpp engine."

Disposition (verbatim): "Retain the repaired finite Theorem B and corrected finite D2 as conditional candidates. Correct
Proposition U's two bookkeeping shortcuts, restrict Lemma S's attainment assertion, restore q<1 in E3(ii), and correct Lemma
U's limiting constant. Rewrite T38's pilot rates, eligible-set interface, and execution terms as in §7 before giving the
complete package a VERIFIED verdict."

---

## 2. A-REV2 (head `09dc230`) + SOURCES.md

Reviewer: "GPT-6 Astra, 2026-11-02." SOURCES.md: "Review baseline: `00c7b34`… These are the remote heads fetched on 2026-11-02;
findings refer to these versions, not the older heads sometimes named in the first referee's report."

| Alias | Branch | Commit (SOURCES.md) |
|---|---|---|
| S03 | theory/W1-T03R | `7e14d6f090bef91861455f45c69017e2a5774198` |
| V03 | theory/W2-VT03R | `b9f6d9b8f6507dd1053d6b916d7a68e1f7b4aa5e` |
| S37 | theory/W1-T37R | `3bcc42958f9d7373178ebab931f62ad38538c8f3` |
| V37 | theory/W3-VT37R | `4988b966f2aafa9c61077e6002146297f0df0dd7` |
| SEX | theory/W1-EXP | `722bd18e51fcc3b485c07590097e137dac71a5aa` |
| VEX | theory/W3-VEXP | `7970fa0b00dd07c70d2670d17fcb44ba3748b52a` |
| SU | theory/W2-PREM (§2) | `988c5f55c0fb0fbd6050b6a4d0c75f14159716e3` |

All equal current heads → **not stale**. Staleness note *inside* the review: "The first T37 referee reviewed an older W1 head.
Its statements that the report was unfinished and the small-experiment files were empty are not descriptions of the pinned W1
head reviewed here." (i.e. the Opus verifier W3-VT37R's first-pass report was based on a stale W1-T37R.) Locked-proof SHA-256
for T01/T02, T03, T22(i)(ii)(iv), T22(iii), T27(i) "match the locked register exactly".

**Headline (verbatim):** "**Overall package verdict: GAP.** The T03♯ conditional theorem, the core refined greedy-repair
theorem, EXP′, and the bounded deterministic-chain mass law survive this audit. The submitted package cannot be accepted
unchanged: several auxiliary statements are **ERROR**, including two missed by the first referees and one error in a referee's
proposed repair."

### 2.1 Verdict table (verbatim verdicts)

| Claim | Verdict |
|---|---|
| S03 Lemma E1(a)–(d) | **VERIFIED** |
| S03 Lemma E2(i)–(iii) | **VERIFIED** ("Keep the stated `s0>=1` restrictions and `n>=5` null-truth exception.") |
| S03 Proposition E3 | **VERIFIED** ("A barrier for the defined exact-tail cutoff… not a posterior lower bound or a universal impossibility theorem") |
| S03 den′ and T02(i♯) | **VERIFIED** |
| S03 Lemmas I/B and T02(ii♯) | **VERIFIED** |
| S03 T03♯(i)–(v), under its SE and BM hypotheses | **VERIFIED** ("C1–C10 checked against both locked proofs") |
| S03 Proposition D | **VERIFIED** (duplicate-design counterexample outside SE) |
| S03 reported proof-onset claim near `1.2e5` | **ERROR** ("V03's correction is confirmed") |
| S37 Proposition 1 and swap identity | **VERIFIED** ("Strict literal TD is contradictory for `d>=1`") |
| S37 Lemma 0(a), (c) | **VERIFIED** |
| S37 Lemma 0(b) as written | **ERROR** ("post-search 'posterior miss' inference does not" survive) |
| V37 R2 proposed exhaustive failure dichotomy | **ERROR** ("omits an inferior local maximum") |
| S37 Theorem A(A1)–(A4) | **VERIFIED** |
| S37 Theorem A(A5), literal TD ⇒ TD′_P without POS | **ERROR** ("Suppressor counterexample; V37 R1's POS repair is **VERIFIED**") |
| S37 TD′_P ⇒ TD′_inf; converse fails | **VERIFIED** |
| S37 definition `TD′_P iff (L) and all D_S` | **ERROR** ("Strict separation is sufficient, not necessary with exact ties") |
| S37 "weakest among at-most-Phi-move conditions" prose | **ERROR** ("retain V37 R3's correction") |
| S37 Theorem B union-bound / Theorem C extensions | **VERIFIED** / **GAP** |
| SEX Theorem 1 EXP′, exact remainder and stated bound | **VERIFIED** |
| SEX/SU displayed `kappa -> 0.52/c_*` | **ERROR** ("Actual limit is `0.51/c_*`") |
| VEX R1 data-computable EXP′ certificate | **VERIFIED** |
| SEX Theorem 3, deterministic fixed-length chain | **VERIFIED** |
| SEX Theorem 4, fixed CL(L) and normalized H3 | **VERIFIED** |
| SEX Theorem 4 growing-leakage bound / "iff" gloss | **VERIFIED** / **ERROR** |
| SU Lemma U, expansion (U) on the declared family | **VERIFIED** |
| SU Lemma U's additional "every V ... used below" quantifier | **GAP** |
| SU C3 zero-leakage upper bound | **VERIFIED** |
| SU C3 matching lower bound under merely `delta=0` | **ERROR** ("Add `mu in span(X_T)`") |
| VEX random-design / actual-packing extensions | **GAP** ("Preserve sketch status") |

Section-level verdicts (verbatim): "**Overall T03♯ verdict: VERIFIED under exactly its stated fixed-design, fixed-sparsity,
anchored SE and BM hypotheses.** This is posterior/global-HPM theory, not reported-HPM discovery." — "**Overall refined
deterministic Theorem A verdict: VERIFIED for A1–A4 and the POS-repaired literal-TD implication. The original A5(a) remains
ERROR.**" — "**Overall Theorems 3/4 verdict: VERIFIED with deterministic fixed-length chain, fixed CL(L), and normalized H3
explicitly retained.**" — "**Overall Lemma U verdict: VERIFIED for (U) and its events on an explicitly budgeted family; GAP for
the extra-family wording as submitted.**"

### 2.2 Specific errors / gaps
1. **T03 proof-onset (S03) — ERROR, disclosure-level.** "with `s0=14`, `p=round(n^A)`… at the previously reported `n=130328`, q
   is about `5.53e22` for `A=log(500)/log(200)` and `7.86e28` for `A=log(1000)/log(200)`, not at most 1/2. At V03's respective
   points `2116048` and `2457025`, q is approximately 0.5. The explicit `exp(2 epsilon_n)<=4` condition occurs much later, around
   the reported `25571897` and `29755302`… These are checks of the named conditions, **not** a universal n0". **n=200:** "At
   `(n,p)=(200,500)` and `(200,1000)`, `m♯=100`, whereas the locked cutoffs are 201 and 215. The cap removes the dimension-tail
   term there. It does not verify the anchored eigenvalue hypotheses or make the asymptotic rate numerically informative."
   T02(i♯): "The quantifier is `sup_m P(Theta_nm>L)`, **not** `P(sup_m Theta_nm>L)`"; constant c♯=κ²/(c_IG σ²) "with no
   surviving factor 4"; "A sequence `g0_n -> 0` is **not** covered".
2. **S37 A5(a) — ERROR (substantive for T37's literal-TD route).** V37 CEX-1 reproduced: n=100, p=12, corr(x1,x2)=.95, signal
   3x1−2.8x2: best addition from empty has gain −2.2977998984; truth gain 20.9899772288, posterior mass 0.8645494125; search from
   empty certifies empty. POS repair VERIFIED; "POS does not rescue the contradictory `d>=1` literal-TD premise."
3. **S37 Lemma 0(b) — ERROR, and V37 R2 (Opus verifier's repair) — ERROR.** V37 CEX-2: F({1,3})−F({1,2})=−2.2862503005,
   F({1,2,3})−F({1,2})=7.2109846558; "This refutes the inference used to explain all 541 benchmark failures by initial
   monotonicity. The per-fit initial scores are still required; this review did not obtain those data." R2 dichotomy omits an
   inferior local maximum; production-table-compatible variant n=100, p=20, B=4 (two groups of four, within .99, hub cross .95).
   Replacement three-way partition by F_pre / F_post vs F(S0) (categories 1–3).
4. **D_S equivalence — ERROR.** n=100, p=2, x1=x2, response .5x1+e, ‖e‖²=99: singleton gain 7.6308489425, duplicate add gain
   −0.0018640607; TD′_P(R0) holds, D_empty false. Repair: D_S sufficient only, or D_S^lex.
5. **"Weakest" prose — ERROR;** path {5,6,12}→{2,5,12}→{2,5,13}→{2,6,13} with a neutral first step.
6. **Theorem C / V37 R4/R5 — GAP retained;** R4 printed `p P(|Z|>=u)` does not follow ("grows like `sqrt(n/log n)`"); "put the
   original t, not the excess u, in the Gaussian tail".
7. **Random centres:** "one cannot replace that union by `2^Phi(S_c)` unconditional single-state probabilities."
8. **EXP′ constant — ERROR (minor):** σ²=1, M=1, φ²=1 gives limit 12.24 not 12.48; "`4.16` multiplier should be `4.08`". VEX R1:
   "Neither the asymptotic theorem nor its loose constant proves that a particular n=200 dataset is on the probabilistic floor
   event."
9. **Theorem 3 quantifier boundary:** "SEX Theorem 3 discharges H2 only for its more restrictive deterministic chain… Do not apply
   this theorem to a selected trajectory without a uniform bound."
10. **Theorem 4 "iff" — ERROR;** VEX R4's "p^-c alone forces vanishing mass 'whatever eta'" "is not justified" (disagreement with
    W3-VEXP). Replacement: "the displayed bound ensures the n-dependent masking factor decays if eta<1/2.02"; with p≥n^a,
    sufficient `a+1/2-1.01 eta>0`.
11. **Random X:** universal study-covariance lower bound .15 false for .9 equicorrelation (min eigenvalue .1, "as VEX noted");
    SEX §4.3's exact-normal claim for the masked projection delta is incorrect ("direction is spherical, not Gaussian"); B≥2g
    packing remains **GAP**.
12. **Lemma U extra-family quantifier — GAP:** counterexample p=n−1 orthogonal, k=1, A′=.1, L=.5 (max of chi-square(1) ~2 log n).
    Repair: deterministic auxiliary family H with |H|≤Cn^{a_H}, L>4max(A′,a_H); for all-k use, L=4kA+1 suffices.
13. **C3 matching lower bound — ERROR:** n=1,000,000, p=2, μ=x1, T=∅, l=2, Z²=65: κ_n=12.2400132448, ϑ′_n=0.7028313369, actual
    16.2502645682 < claimed 19.5571554183. Repair: require μ∈span(X_T). "SU §3.4 uses the lower corollary at precisely such
    supersets, so this finding does not itself refute that later construction."

### 2.3 Reproductions (§7)
Script `scripts/check_review.py` (independent of author/referee code), outputs `results/checks.json`; NumPy+SciPy venv (system
Python lacked both). E1/E2: 6,190 cases zero violations. T03 B1/B3/C6(a): 384 comparisons, residual 5.72e-15. Prop D at
n=p=200/800/3200 cutoffs 4/5/6. T37 core: 448 centres on 16 datasets, 224 capped certifications. EXP′/Lemma U: 696 additions,
p=8 AR(.5), max decomposition error 1.39e-13, largest |R| .9213 vs κ>15. Theorems 3/4: p=12, n=100/400/1600, log-mass medians
.432/.549/.582. C3 counterexample from a 2×2 Gram. "They do not estimate the actual benchmark's 541-fit failure decomposition".

Required disposition (verbatim items 1–5): "1. Retain the T03♯ proof with its exact hypotheses; correct the finite-n disclosure
and describe E3 as a barrier for this cutoff/envelope route only. 2. Retain Theorem A(A1)–(A4), apply POS to the literal-TD
implication, replace the D_S equivalence…, and replace both the original posterior-miss explanation and V37 R2's incomplete
dichotomy. 3. Retain EXP′ and Theorems 3/4 within their fixed-design and deterministic-chain scope; correct the limiting
constant and the necessary/sufficient wording. Keep H3 explicit. 4. Specify Lemma U's full event family and cardinality budget.
Restrict its matching lower corollary… 5. Leave all random-partition and T37 asymptotic extensions at their source status."

---

## 3. A-REV3 (head `522d83d`) + STATUS.md

Referee: "GPT-6 Astra, 2026-11-02." Scope pins: "W3-PXN head `4aebea3bf003f5f3c0c7239a24c824ec2d2aa574`; W4-SHARE head
`0d3f3fe581b72186c0c9bffe701950044cc7a464`. W5-VMASK was pushed at `4e41b974e0b8f954eb6adaf6be76d351821fdab0`; only `git ls-remote`
was used for it." "No W5-VMASK report or helper verdict was consulted." Candidate dependencies inspected: W1-EXP `722bd18…`,
W1-T38E `436a712…`, W1-T37R `3bcc429…`, W1-T03R `7e14d6f…`. Local baseline `816ec72ed40a35a0bff620ccb3170d947008cebe`. All
equal current heads → **not stale**. Internal: "Evidence checkpoint head SHA: ae97136; final review head is supplied in the
delivery message" (final = `522d83d`).

**Headline (verbatim):** "**Overall W3-PXN: GAP as written. Overall W4-SHARE: GAP, with ERROR findings in the score-expansion
and assembly claims.** The central LH construction is credible; the D4/D5 conditional inequalities survive review."

Implementation anchor relevant to LS0: "`v3_core.cpp:447,610,657` starts production local search from the scored HPM, **not
automatically from the start mode**. Thus LS0 remains an explicit modification, as W3 §12 correctly specifies."

### 3.1 Verdict table (verbatim)

| Result | Verdict | Scope / finding |
|---|---|---|
| W3 P1, actual blocks = groups | VERIFIED | "`g <= B < 2g`; packing is essential." |
| W3 P2: G, R, SE, SE-blk, anchored variants, BM-infinity | VERIFIED | |
| W3 Lemma B(i)–(iii) | VERIFIED | "not conditioning on partition recovery" |
| W3 Lemma Tr | VERIFIED | "In its stated bounded-dimension and family-cardinality range." |
| W3 P3 / Beta-truncation start mass | VERIFIED | "no untruncated exponential moment is used" |
| W3 P4, mask mass and limit law | VERIFIED | locked T27 "retains its polynomial-equivalence scaling/operational wording" |
| W3 P5, start mode = reference | VERIFIED | |
| W3 P6, TD-prime / lattice proof | GAP | "Uniformity lemma invokes Tr beyond its stated range; constants need correction." |
| W3 P7, original-method no-tweak route | GAP | "D2(d) is explicitly only a sketch" |
| W3 P8, posterior concentration | VERIFIED | |
| W3 joint T38(b), LS0 route | GAP | "finish P6 bookkeeping and retain operational assumptions" |
| W4 D4 | VERIFIED | |
| W4 D5 | VERIFIED | |
| W4 SH(i),(ii), exact formula in (iii) | VERIFIED | "converse includes the crucial `pi0(a)^N -> 0` condition" |
| W4 SH universal sharp-transition prose | GAP | |
| W4 G weighted-oscillation identity; ESS alone | VERIFIED | |
| W4 G unrestricted "no grid condition" / BVS extrapolation | GAP | |
| W4 M(a), deterministic core | VERIFIED | |
| W4 M(b), quadratic equality used as an expansion | ERROR | "Fixed orthogonal signal leaves a remainder of order n." |
| W4 M(b), fixed-d BM-infinity gain/path implication | GAP | |
| W4 M(b), vanishing crossing temperature under all T03 hypotheses | ERROR | "BM-C permits fixed logarithmic signal strength" |
| W4 §7 conditional B2-W4 inequality | VERIFIED | |
| W4 §7 replacement of exact exit loss by sum eta | ERROR | |

### 3.2 Specific errors / gaps
1. **W3 P6 — GAP (two bookkeeping defects):** (1) "Lemma Lambda(a) calls Tr(c) over *all* sets of size at most s0+2. Their number
   is of order `p^(s0+2)`, not bounded by the `n^(A+1) 2^17` family"; projection dimension can exceed 16; repair with general J
   and threshold C log(n)/n, C>4[A(s0+2)+2]. (2) "Lemma U(U1) writes `nu*(1.02+1/(n phi0^2))/(c_* n) <= 1`. This arithmetic
   inequality is false: with sigma squared=1 and M=3, W1-EXP's c_*=1/40, and the left side tends to 20.4." Strict-margin sentence
   must exclude other progress additions. "Neither step proves that the original C++ chooses the LS0 center; the explicit LS0
   tweak must remain."
2. **W3 P7 — GAP:** Beta second shape "`(n-2-s)/2`, not `(n-3-s)/2`"; missing-reference peeling and uniform discrepancy-family
   argument unwritten; "H0 grows like p, so a generic o_P(1) bad-draw mass is insufficient. Leave the original-method route at GAP."
3. **W3 P8 / assembly:** VERIFIED; "This does not establish schedule completion. W3's T38(b) statement retains U and the LS0
   operational setting".
4. **W4 D4:** VERIFIED; "The monotone-envelope constant is `g(1)=1/(e-1)`, not one half." D5: "a genuine replacement of SHARE by
   another stochastic control condition; it does not establish that condition for the BVS particle system."
5. **W4 SH (iii) — GAP:** π₀(o)=1/N, no outsider w.p. (1−1/N)^N→e⁻¹; at κ=3 log N extinction → 1−e⁻¹. Repair: N π₀(o)→∞ and
   N π₀(a)→∞.
6. **W4 G — GAP:** two-state neutral-resampling example shows "an ESS condition alone is not a delivery theorem"; "A universal
   impossibility statement… needs a quantified theorem and a BVS counterexample; C1 does not supply that missing step."
7. **W4 M(b) expansion — ERROR:** p=n−1 orthogonal, θ=1, σ²=1, T=∅: exact gain/n → log(2)/2 = .34657359 vs quadratic 1/4;
   remainder ".09657359 n + o_P(n)". "00_COMMON's EXP is an open input with an upper-bound formulation… W1-EXP proves EXP-prime,
   which does not validate this Taylor replacement for fixed nonzero x." Repair: gain ≥ c M_n log n − C log n under BM-∞, fixed d.
8. **W4 M(b) BM-C scope — ERROR:** θ²=C log n/n, C=1024: crossing-temperature ratio → 3/C>0. Repair: restrict to BM-∞.
9. **W4 M(b) path — GAP:** additions from U∪P end at S₀∪P, do not delete extras; "'Proposition X cannot bite' and 'only outsider
   competition plus exits remains' overstate".
10. **W4 §7 exit-loss — ERROR:** two-state absorbing chain, survival 1/2, T=floor(1.6 log N): Σ eta=.8 log N satisfies the stated
    condition but E n_T(a)=N 2^(−T)→0. Repair: keep −Σ log(1−η_t); if η≤1/2, `2 sum eta` suffices.

### 3.3 Reproductions / STATUS.md
Run on owls.stat.rice.edu `/home/fb31/theory_campaign/A-REV3`, one BLAS thread. First PID 2507588 failed (system python3 lacked
NumPy; `results_failed_system_python_run.txt` and exit "w4=1 w3=1 validate=1" preserved). Second PID 2508171 succeeded but runner
had CRLF error; clean LF rerun PID 2509198 completed ~19:21 UTC, exits w4=0, w3=0, validate=0, independent=0. Env Python
3.12.15, NumPy 2.5.4, SciPy 1.18.1. Imported scripts are "frozen reproductions, not an independent C++ execution".
- D4: 200 exact finite-count chains, largest exact/bound .999043. M(a): 3,000 cases, min LHS/RHS 1.00000000.
- Lemma B: 400 replicates per statistic, KS p .171–.622 ("diagnostics, not proofs").
- P6 population enumeration: 81 cases, smallest non-progress margin .002743.
- **LH at n=200, p=750, g=10:** partition and reference start mode recovered in all three seeds 22868155–22868157; log reference
  masses −.254658, −.321040, −.424955; "LS0 scored truth in all three; its endpoint was truth in two. In the first, truth loses
  to the reference by .135324 nats… scoring, certification of the returned model, and recovery cannot be conflated."
- SH rare-outsider extinction → .63212. SVD vs Gram 18 scores, max diff 1.62e-13; n=10000 fixed signal gain/n .345653 vs
  quadratic .249564.

Eight-line disposition (verbatim items): "1. W3-PXN overall: GAP; preserve the conditional LS0 scope. 2. Lemma B, Beta
truncation, masking law, start mode and posterior transfer: VERIFIED. 3. P6 needs dimension/cardinality/constants repaired; P7
remains GAP. 4. W4 D4 and D5: VERIFIED with exact retention product and confinement. 5. SH exact bounds: VERIFIED; universal
transition wording: GAP. 6. G's identity: VERIFIED; unrestricted BVS impossibility claim: GAP. 7. M(a): VERIFIED; M(b)
expansion/BM-C scope and exit-loss simplification: ERROR."

---

## 4. A-REV4 (head `b95948c`): REVIEW, BOOK_CHECK, DRAFTS_CHECK, NUMERICS

Reviewer: "GPT-6 Astra; 2026-11-02. Sol helpers supplied mechanical independent checks in BOOK_CHECK.md and DRAFTS_CHECK.md;
the verdicts below are the primary referee's." Pins (from `git show origin/theory/A-REV4:…/SOURCE_MANIFEST.json`, not in the
src snapshot): W2-T26 `0e4f1e7f5efd…`, W2-BOOK `57eb3d0f6699…`, F-DRAFT `4de6e4c7fab6…`, A-DRAFT `dbf47f7abfe9…`; base `816ec72…`.
All equal current heads → **not stale**. Internal: "Reviewed-content checkpoint head SHA: 34e4f48da014…; final delivery head is
reported in chat."

**Headline (verbatim):** "**Overall: GAP.** The favourable-start and posterior-functional compositions are defensible
conditional mathematics. F-DRAFT contains two explicit false formulas, and its sharp weight-divergence claims are not proved."

### 4.1 Verdict table (verbatim)

| Result | Verdict | Scope |
|---|---|---|
| W2-T26 Lemma 1 | VERIFIED | |
| W2-T26 Lemmas 2 and 3 | VERIFIED | "remove the L factor" |
| W2-T26 Theorem A, actual written statement | VERIFIED | "Includes EX-A/EX-S/CAL/START/OUT, feasibility, P1 and P1-ex; output-intersected conclusion only." |
| W2-T26 advertised single-premise shorthand | GAP | "P1 restricted to successful SMC says nothing on the exact branch." |
| W2-T26 Theorem B | VERIFIED | "EXP'/VIS/NL remain assumptions." |
| W2-T26 Proposition C | GAP | "Retain PROOF SKETCH" |
| W2-BOOK RO | VERIFIED | "P(output)>0 when dividing" |
| W2-BOOK GUARD literal full-output claim | ERROR | "Timing/allocation metadata differ on successful same-seed executions." |
| W2-BOOK completion-selection counterexample | VERIFIED | "Stylised component example" |
| W2-BOOK Proposition 2 island identity and covariance | VERIFIED | |
| W2-BOOK output Markov bound | VERIFIED | |
| W2-BOOK VAL-FP | GAP | "no validated eta/epsilon for production is supplied" |
| W2-BOOK package | GAP | "additional HPM overstatement is ERROR" |
| F-DRAFT NM | ERROR | "false O_P(1) remainder" |
| F-DRAFT W1 | VERIFIED | |
| F-DRAFT W2 | ERROR | "Ordinary partial R² is not the exact v3 score fraction" |
| F-DRAFT W4 | GAP | "KL omits positive layers; sharp chi-square rate imports a conjecture" |
| A-DRAFT §2 Theorem A and A1 | VERIFIED | "no CLT upgrade" |
| A-DRAFT §2 Theorem D and D1 | VERIFIED | |

Additional §7 (verbatim): "**Additional T26 exact-branch ERROR** — The repeated parenthetical assertion that the exact branch
fails whenever p>=18 and n>=22 is false under the actual budgets. Counterexample: p=18, n=2^18… The exact branch is therefore
taken." Does not invalidate Theorem A (P1-ex retained) or Theorem B.

### 4.2 Specific errors / gaps
- **W2-T26 Theorem A proof audit** (steps 1–7 VERIFIED): Δ = max(1−π₀(S0),1−π(S0)) exactly; ρ̄ ≤ (B+3)u_π; constants 27x PIP and
  108x/ε valid. Step 6: fixed-p θ_n=n⁻¹ example "illustrates why SMC-restricted P1 can be vacuous while exact posterior
  truth-PIPs fail".
- **Prop C (ORTH) — GAP, repair offered** (chi-square block residual bound, c=(log 2)/2−1/4); "ORTH excludes p>n-1."
- **GUARD (W2-BOOK) — ERROR literal:** v3_fit.R returns allocation, timing, peak-memory metadata; "Project both records onto
  statistical estimates, scores, discrete records and statuses".
- **B3 probability convention — GAP:** E[1_O Ẑ] ≤ Z P(A) is fixed-data only; joint form E[1_A Z(data)]; counterexample Z∈{1,2}
  gives 1.5.
- **B4 exact-branch extension — GAP.** **VAL-FP — GAP** (implication VERIFIED). **B6 numerical provenance — GAP** (BOOK_CHECK did
  not rerun; "50-digit numerical enumeration" not exact certification).
- **B5 / "Additional ERROR": BOOK's "every completed wrong HPM is a posterior miss" — ERROR.** "Let F(S0)=1,F(S1)=0 and scored
  set={S1}. A completed search reports S1… Completion does not imply discovery… It is not a consequence of locked T07."
- **F-DRAFT W2 — ERROR:** n=20, p=4, G=19I, blocks {1,3},{2,4}, S°={1}, l=2, z² = (100,30,0,0): actual v3 log-odds 0.310405538698
  vs RSS-partial-R² 0.353784569589, discrepancy 0.043379030891. Repair h_{T,l}=(t_{T+l}−t_T)/(.02+Q_T); require |S°|<K. Uniform
  multiplicative equivalence "is a separate GAP".
- **F-DRAFT NM — ERROR and scope GAP:** b=σ=1, r=1/2: "nondegenerate sqrt(n) fluctuation of log BF about n log(8/7)/2, not a tight
  remainder"; repair to O_P(√n). "The odds… prove only pi0({j})->0"; worst-case independence-MH bound is not failure for every
  start ("starting at truth is a counterexample"); "The O(1) discrete ideal-grid assertion is not proved by a thermodynamic-length
  heuristic. A safe repair is the explicit fixed-p two-column family with a direct four-state comparison (as in A-DRAFT §3)".
- **F-DRAFT W4 — GAP:** exact KL ≤ −log π₀(S0) + Σ_{S≠S0} π(S)[d(S)−d(S0)]; dropping multi-extra layers "does not prove an upper
  bound"; sharp χ² law is W(c), "explicitly a CONJECTURE". Abstract example π=(1−1/k,1/k), π₀=(1−1/k³,1/k³).
- **F-DRAFT W1 — VERIFIED** "BO algebra and known-common-variance comparison"; "Keep the global capped prior in the start; this is
  not a product of independent local posteriors."
- **A-DRAFT §2:** Theorem A "verifies the LLN/MSE, not the conjectured T16 CLT"; Theorem D constants "8Mx and 24x check. This
  independently confirms the lack of an L factor"; D1 equality-indicator counterexample correct. "No missing masked-start or
  completion guarantee is supplied by these arguments."

### 4.3 BOOK_CHECK.md (Sol helper; W2-BOOK `57eb3d0`)
Verbatim overall: "**Overall: GAP for a literal paper/deployment claim; VERIFIED for the central fixed-data, exact-arithmetic
mathematical implications after the scope qualifications below.** No error was found in the minus-three-quarters covariance
coefficient." Items: RO VERIFIED; Island identity VERIFIED (bias = −(3/4)Cov_C; strict bound −0.1275 Z from locked <−0.17);
Markov/Jensen VERIFIED; VAL-FP "VERIFIED as an assumed contract, not a measured guarantee". Guard: "VERIFIED by static inspection
for statistical quantities in the ideal stop-only interpretation; replay validation remains a GAP." GAP B1 (GUARD too broad), GAP
B2 (ideal vs implementation arithmetic), GAP B3 (probability convention), GAP B4 (exact-branch), **ERROR B5** (wrong HPM ⇏
posterior miss), GAP B6 (provenance; "BOOK supplies no inspected remote job provenance… launch command, process/job ID"). "No
numerical workload was executed" by the helper.

### 4.4 DRAFTS_CHECK.md (Sol helper; F-DRAFT `4de6e4c`, A-DRAFT `dbf47f7`)
"F-DRAFT W1: VERIFIED"; "F-DRAFT W2: ERROR in the purported exact identity; GAP in the uniform conclusion" (v3 explained quantity
is (n−1)/n × LS for G=n−1; "Source conditional PROVED label is not independently verified as written"); "F-DRAFT W4: VERIFIED TV
bound; GAP for KL rate and chi-square assertion" (abstract π₀=(1−ε, εe^{−1/√ε})); "F-DRAFT NM: ERROR/GAP as a general
proposition; valid fixed-p repair" — items 1–4 (O_P(√n); π₀({j})→0 only; "The assumptions do not explicitly provide uniform
global SE/BM hypotheses of locked T03"; part (v) "needs occupancy of the stated mode when its Gibbs label is executed");
"A-DRAFT §2: VERIFIED under the stated potential-run and premise qualifications".

### 4.5 NUMERICS.md
All on Owls `/home/fb31/theory_campaign/A-REV4`; Python 3.9.25; seed 20261102.
| Job | PID | Exit |
|---|---|---|
| Independent algebraic checks (`checks.py`) | 2507523 | 0 |
| BOOK initial attempt | 2508065 | 1 ("missing mpmath") |
| BOOK 50-digit reproduction (mpmath==1.3.0) | 2508546 | 0 ("ALL CHECKS PASSED") |
| Independent proxy experiment (`nm_check.py`) | 2508672 | 0 |
| Raw-statistic rerun (`nm_raw_check.py`, 768 replicates) | 2511056 | 0 |
BOOK: primary PIP bias −0.1739741778498905; pooled-product relative bias −0.13171639499258733; covariance residual 5.13e-49.
Checks: W2 discrepancy −0.04337903089108747; four-island pooled bias 0.1875 = −3Cov/4; W1 min d −8.9e-16 (rounding). Proxy
experiment n∈{64,256,1024}, 256 reps each, "corroborate the analytic non-tight remainder counterexample". "No production guard
replay or VAL-FP validation was attempted."

Eight-line summary (verbatim items 1–6): "1. Overall verdict: GAP; no candidate, sketch or conjecture status is upgraded. 2. T26
A/B and Lemmas 1–3: VERIFIED under their full stated hypotheses. 3. T26 exact-branch parenthetical: ERROR; Proposition C retains
a GAP/sketch disposition. 4. BOOK core identities: VERIFIED; literal GUARD and completed-HPM statements contain ERRORs. 5.
F-DRAFT: W1 VERIFIED; NM/W2 ERROR; W4 GAP. 6. A-DRAFT §2: VERIFIED conditional posterior-expectation results."

---

## 5. A-DRAFT (head `dbf47f7`; Astra research report, self-checked, base `325b0d8`)

Status line: "This is an independent research report, not an adoption or amendment of the locked register. **PROVED** below means
a complete argument is supplied here or an explicitly identified source labels its result PROVED; campaign results remain
candidates." Note at end: "The proofs here have been self-checked but have not received independent review." (A-REV4 later
VERIFIED §2; §3 Prop M has **no** cross-family review in these sources.)

### 5.1 Novelty audit (§1)
Six works compared (availability): Song & Liang 2015 (**Not in `Papers/`**; publisher text), Zanella & Roberts 2019 (repo PDF),
Lindsten et al. 2017 (**Not in `Papers/`**; arXiv v2), Schäfer & Chopin 2013 (repo PDF), Del Moral–Doucet–Jasra 2006 (repo PDF),
Gutierrez & Guhaniyogi 2022 (**Not in `Papers/`**; NSF PDF; supplement not retrieved). "This is a comparison against the six
specified works, not proof of worldwide priority." `W3-PGD/REPORT.md` at its snapshot "has only a draft header and an empty
headline".
Findings:
- Song–Liang: "it is inaccurate to describe their complete algorithm as merely a naive union"; "the §3 counterexample below refutes
  naive union, **not Song–Liang's second selection stage**. A comparative uncertainty claim about their complete method remains
  OPEN here."
- Zanella–Roberts: TGS consistency, RB PIPs already present; "No superiority over TGS follows from any v3 theorem listed here."
- Lindsten et al.: "the closest conceptual antecedent"; v3 is "a concrete BVS construction, not a new local-to-global paradigm";
  "T31 is Markov's inequality applied to a nonnegative unbiased estimator".
- Schäfer–Chopin: "the ordinary geometric bridge and even ESS bisection are not novel. Restricted candidate-set ESS does not by
  itself certify unseen-mode coverage".
- DMDJ 2006: "re-proving the finite-state LLN is useful validation, but should not be sold as a main novelty".
- Gutierrez–Guhaniyogi: "'partition then regain global uncertainty' already has close relatives".
Theorem-set table statuses (verbatim): T03 "**PROVED**, locked… They do **not** reduce the SE-free cutoff… proof thresholds remain
far beyond the study scale"; T21 "**PROVED**, locked conditional composition… not a strong standalone novelty"; T38 "Campaign
**PROVED** conditional compositions; not a new locked entry. W4's fully instantiated masked LS0 route changes the method. W3-PXN's
p≫n joint-family claim remains a candidate; the no-tweak one-mask NB step is **PROOF SKETCH**. W4-SHARE… BVS TRACK/OSC instances
are **CONJECTURE/OPEN**"; Theorem B "Campaign **PROVED** candidate inequality after W2-VT24G's first-failure repair… A finite
inequality alone is not useful finite-budget consistency"; T12/T31(i) "**PROVED**, locked under EX-A/EX-S/CAL"; T26(i)–(ii)
"W2-T26 labels its composition **PROVED**, candidate; its ORTH compatibility proposition is **PROOF SKETCH**… Favourable-start
theory only."
Referee verdict (verbatim): "A safe paper claim is 'a BVS-specific construction and analysis within established SMC principles.'
'First local-to-global Bayesian correction,' 'new generic SMC consistency,' and 'all uncertainty estimates are unbiased' are not
defensible claims." Three plausible contributions: (i) start law with exact global prior/cap, (ii) a jointly verified masked
family with budgeted correction, (iii) quantitative weight control — "(iii) in the masked regime remains OPEN".
**Does not cite** Yang–Wainwright–Jordan 2016 or Zhou–Yang–Vats–Roberts 2022 (F-REFEREE M6 objection).

### 5.2 E[h] consistency (§2)
Estimators: self-normalised terminal pre-resampling, optional joint draws, RB K_j f_h; "For `h_j=1{j∈S}`, `K_jf_{h_j}=o_j`; this is
**exactly v3's recorded island PIP**." "v3 currently specifies HPM, evidence and PIPs, **not an implemented general-purpose
h-estimator**."
- **Theorem A — fixed-data particle consistency (PROVED, candidate).** EX-A, EX-S, START, CAL; potential uninterrupted run; N→∞:
  all §2.1 estimators → μ_h in probability and L², TV convergence of support laws, Ẑ_r/Z→1, max_j|PIP̂_j−PIP_j|→0, MSE
  O_{data,c,h}(N⁻¹). "not an accuracy rate claimed for the two production tiers". Bounded-stage N-dependent calibration bound
  a_t ≤ (t+1)2^t e^D sqrt(m/N), "not uniform in growing n,p".
- **Corollary A1 (PROVED from locked T12):** E_c[Ẑ_r μ̂_r(h)] = Zμ_h; E_cμ̂_r − μ_h = −Cov_c(Ẑ_r,μ̂_r)/Z; pooled
  E_c[Ẑ μ̄] − Zμ_h = −¾ Cov_c(Ẑ_1, μ̂_1). Equal pooling over infinitely many fixed-N islands converges to the biased mean.
- **Theorem D — n-indexed budgets, conditional on T26's premise (PROVED, candidate).** Actual budgets (N_e=4^e max(2500,n,p),
  T ≤ 4max(1000, ceil(log2(n+p+1))²), L = max(4, ceil(log2(n+1)))); assumes EX-A, EX-S, START, CAL, OUT and (P1) incl. exact-branch
  clause; conclusions (D1) P{O_n∩|μ̂_n−μ_n|>ε}→0, evidence, (D2) uniform PIP → truth indicator, P(O_n, MPM≠S0)→0. "No assertion
  that `P(O_n)→1` is included." Key bounds (D4) E_c|W_r−1| ≤ 2(T+1)Δ/(1−Δ); (D5) E_c η_r(S0ᶜ) ≤ δ + b_c; (D6) ≤ 2M(2δ+b_c);
  (D7) ρ̄ ≤ (B+3)u_π; (D8); constants 8Mx and 24x. "no factor L appears… independently justifies W2-T26's removal of the older
  `(L+4)ρ*→0` premise". Weighted draws: Σw_i² ≤ 1/m_0 + v_out² → 0 under (P1).
- **Corollary D1 (PROVED, conditional statistical implication):** generating-value consistency under uniform local continuity and
  posterior contraction. **COUNTEREXAMPLE** to unrestricted bounded h: h=1{θ_j=θ_j*}. Suggested replacement wording for draft
  §13.1 provided.
- Relation: "T16(i)… is marked **CONJECTURE**… Theorem A… does **not** prove or upgrade T16's joint CLT."

### 5.3 Naive merge (§3)
- **Proposition M — identifiable cross-block proxy (COUNTEREXAMPLE; proof complete).** p=2, X'X=(n−1)[[1,ρ],[ρ,1]], 0<|ρ|<1,
  y_raw=b x1+ε, S0={1}, local blocks {1},{2}: in probability l_{n,1}→1, l_{n,2}→1, π_n(S0)→1; q_n(2∈S)→1, q_n({1,2}⊂S)→1,
  π_n(2∈S)→0, π_n({1,2}⊂S)→0 (M1); P(U^H=U^M={1,2})→1; ‖q_n−π_n‖_TV→1. Composite start "is **not** the product q_n, but it too
  concentrates on `{1,2}`". Rates (M2) c₁=½log((b²+σ*²)/σ*²), c₂=½log((b²+σ*²)/(σ*²+b²(1−ρ²))); (M3) log m({1,2})/m({1}) =
  −½ log n + O_P(1).
- §3.2: "**PROVED — actual small-p v3.** For p=2 and n≥4, v3 takes its exact branch"; "**PROVED — SMC component, different
  limit**" (first N then n); "**T26 boundary.** On this family, `π0,n(S0)→0`, so `Δ_n→1`; T26's favourable-start SMC premise
  fails… The forced-SMC production-budget claim is **OPEN here**".
- §3.3 numerics (`scripts/naive_merge.py`, p=2, ρ=0.8, b=σ*=1, seed 20261102, exact four-model sums, owls_run -j 2):
  | n | Full proxy PIP | Product proxy PIP | Full joint | Product joint | Full truth mass |
  |---:|---:|---:|---:|---:|---:|
  | 40 | 0.169997 | 0.998530 | 0.169972 | 0.998530 | 0.830003 |
  | 100 | 0.254240 | 0.999995 | 0.254240 | 0.999995 | 0.745760 |
  | 400 | 0.067198 | 1.000000 | 0.067198 | 1.000000 | 0.932802 |
  | 1,600 | 0.045383 | 1.000000 | 0.045383 | 1.000000 | 0.954617 |
  | 6,400 | 0.016079 | 1.000000 | 0.016079 | 1.000000 | 0.983921 |
  | 25,600 | 0.006214 | 1.000000 | 0.006214 | 1.000000 | 0.993786 |
  Local HPM/MPM unions {1,2} every row; full HPM {1} every row; log-BF cross-check discrepancy < 10⁻¹¹; first system-Python launch
  lacked NumPy.
- Confidence card (verbatim statuses): Theorem A "**PROVED**, candidate"; islandwise identity "**PROVED** from locked T12";
  Theorem D "**PROVED**, candidate"; uniform PIPs without (L+4)ρ* "**PROVED**, candidate"; all bounded h → generating value
  "**COUNTEREXAMPLE**"; Prop M "**COUNTEREXAMPLE**, complete proof"; actual v3 consistent on the counterexample "**PROVED**";
  generic novelty "**OPEN** as a priority claim; adverse evidence strong"; superiority over Song–Liang "**OPEN**"; masked-regime
  PIP/evidence for unmodified v3 "**OPEN**".

---

## 6. F-DRAFT (head `4de6e4c`; Fable 5.1; "Nothing here is reviewed or adopted")

One exact p=12 check in base R (`scripts/wstab_check.R`, 10 s via `owls_run -j 1`, seed 20261102).
Verdict sentence (verbatim, abridged): "The draft's design is realised by v3 exactly… Every validity target of the draft (Prop 1,
Prop 2, the frozen-run estimates) is locked. The draft's one substantive theory target, §5.3 'weight stability under weak
cross-block dependence', is **not** covered and, as drafted, is **false for v3's tables**: under *exact* block orthogonality the
composite start still differs from the posterior by a Θ(n) term coming from the per-block integration of σ² against the full
response".

### 6.1 Crosswalk (draft target → class → v3 coverage)
| Draft target | Class | Coverage / addition |
|---|---|---|
| Prop 1 MH exactness | (a) | T09(ii) PROVED-LOCKED; add W0(iv) remark |
| Prop 2 SMC consistency | (a)/(b) | T09, T12, T31(i), T14(i), T15 locked; W2-T26 Thm A candidate PROVED; T16 "CONJECTURED and *dropped*" |
| §5.3 Thm 1 weight stability | **(b) + (d)** | Ingredients T13(i), T22(i)(ii)(iv), EXP′ ("candidate PROVED, verified by W3-VEXP"), BO benchmark, T27(i); add W1, W2, Theorem W, W3, W′, W″ |
| §5.4 approximation error | (b) | T12/T31(i), T14(i)/T15, T23(ii), W2-T26 Thm A, T07(iii)(c); add Prop W4, Remark H; coverage (d) |
| §3.2 naive union merge | **(c)** | Add **Prop NM**; "Not implied by T06/T07/T27 as statements; corollary of T22(ii-a) + T03" |
| §13.1 E[h(θ)] | (a)/(b) | T12, T23(ii), W2-T26 Thm A; Remark H |
| §13.2 Song & Liang UQ | (c) | "Prop NM is the precise statement of the UQ defect of a split-and-merge *selection* rule" |
| §13.3 partition random | (c) | Prop P (PROVED, elementary); (ii) mixture start "a method extension… investment rule" |
| §4.4 stability/ESS/blocks | (b) | T13, T31; Theorem W, Prop P(i), Remark W5 |
| §8.2 novelty devices | (a)/(b) | "Theorem W + W′ are the 'theory for stable correction weights'" |
| §3.3 overlapping blocks | (d) | none ("Overlap would destroy the exact start") |
| §4.3 delayed acceptance | (d) | none |
| §6 comparators | (c), empirical | report π₀'s HPM/PIPs and restricted one-step ESS ρ_V(0,1) per fit |

### 6.2 New targets (NEW_TARGETS.md "Summary of statuses", verbatim) with Astra verdicts where reviewed
| Label | Statement | F-DRAFT status | A-REV4 verdict |
|---|---|---|---|
| W0 | three faces of π/π₀ (χ², sup ratio, π₀(S₀)) | PROVED | not reviewed |
| W1 | exact d under BO; known σ² ⇒ π₀ = π | PROVED | **VERIFIED** |
| W2 | LR_l = κ_b·G_l | PROVED modulo EXP′ (candidate) | **ERROR** (exact identity) + GAP (uniform) |
| W3 | cross-block covariance term | PROOF SKETCH | not reviewed |
| W(a) | 1 + χ² ≥ p^{R²−ε}/√n | PROVED modulo W2 | not reviewed directly (depends on W2, which is ERROR) |
| W(b) | 1 + χ² ≤ 1 + p^{R²+ε}/√n + o(1) | PROOF SKETCH (crux: second-moment aggregation) | not reviewed |
| W(c) | sharp log log form | CONJECTURE | cited by A-REV4 as CONJECTURE |
| W′ | ideal grid stage count ⌈log₂(1 + 1/g)⌉ + O(1) | CONJECTURE (skeleton) | not reviewed |
| W″ | crossing costs ≈ 3π stages | two-state PROVED; window CONJECTURE | not reviewed (DRAFTS_CHECK: NM(v)'s O(1) grid claim "not established by W″'s thermodynamic-length calculation") |
| W4 | KL, TV small while χ² large | PROOF SKETCH | **GAP** |
| W5 | dilution vs leakage trade-off | remark | — |
| NM | naive merge overcovers; start inherits; posterior does not; correction is one flip | PROVED modulo T03/EXP′/Cor. P1 | **ERROR** (O_P(1) remainder) + scope GAP |
| P | partition: validity-free, mixture start, stochastic scheduling | PROVED | not reviewed |
| H | general h | PROVED | not reviewed (consistent with A-DRAFT A1) |
Key numerics: W1 check d(S₀)=57.1 (n=200), 254.1 (n=800) nats with one truth per block; W2 check at n=800 LR 0.620 vs κG 0.621,
1.050 vs 1.050, 0.429 vs 0.437; Theorem W finite n: p=12, n=200, π(S₀)=0.21, 1+χ²=19.6 (ESS 5%); n=800 all BO runs 1+χ² ≤ 1.03;
NM proxy-split: argmax π₀={1,7}, argmax π={1}, π₀({1})=1.7·10⁻⁴¹ (n=200), 1.0·10⁻¹⁴⁶ (n=800), π({1})=0.86/0.95, TV 0.985/0.996,
1+χ²=4.9·10⁴⁰, T_ideal=14/16. Study design (R²≈0.9, p=500, n=200): bracket "5.5 − 2.6 = 2.9 nats"; "the actual start is
dilution-masked, adding ≈ 28 nats (W3-VEXP)" (CROSSWALK gives π₀(S₀) ≈ 10⁻¹²).
Confidence card P(true)/P(provable): W1 0.99/done; W2 0.95/0.95; W(a) 0.95/0.9; W(b) 0.85/0.6; W′ 0.75/0.4; W″ 0.99/done, 0.7/0.5;
NM 0.97/0.95; P 0.97/done; method note §6 0.6/"pilot question".
Recommendations: NM as main-text Proposition 0; Theorem W remark after Thm 2 with W(a)+W1 in supplement; W0 as T13 clause (v);
supplement remarks W4, W5, P, H; do not add delayed acceptance, overlapping blocks, coverage, generic Del Moral theorem.
W′ payoff claim: "W′ is exactly the input W2-T26 Theorem B lacks: with T_n = O(1), (T_n + 1)Δ_n → 0 follows".

---

## 7. F-REFEREE (head `fae6b7f`; Fable 5.1): objections and planned responses

Object reviewed: `theory/S-PAPER:theory_section.tex` (744 lines, Theorems 1–6, Propositions 1–2, the n = 200 disclosure),
F-REFINE, W4-T38FULL, W6-FIXREV1, THEORY_PRIORITIES, "the cross-family reviews `theory/A-REV1`, `theory/A-REV2`", A-DRAFT §1,
HEADLINE_TABLES. In-flight branches looked at "only to judge what a response could honestly promise".

**Overall recommendation (verbatim):** "**Recommendation: major revision.** The theory section is unusually candid, internally
consistent, and the composition inequality (Theorem 4) is exactly the right organising principle. But in its present form the
section does not support the paper's empirical claims, and its headline theorem (Theorem 5(b1)) is about an algorithm (v3 + LS0)
that the reported simulations did not run." §3: "**Verdict.** Major revision. Not reject: … Not minor: the headline theorem is
about an unrun algorithm, the masked regime for the run algorithm is open, the computational-guarantee literature is unaddressed,
and the connection between the theorems and the tables is absent."
**The one change (verbatim):** "*Make Theorem 5(b) a theorem about the algorithm that produced the tables, on the explicit family
LH, and show its predicted transition with the production code at growing n.*" "If only one *theory* task can be run, run the
verification of BG1 / B2-LH (RESPONSE_PLAN task R1). If only one *compute* task can be run, run the LH scaling study (task R2)."

Severity: majors M1–M8 ("Major points"), minors m1–m20. No individual severity scale beyond major/minor. The three "structural
problems [that] decide the tier" are M1, M2/M3, M6. Task ranking: "R1–R3 are load-bearing; R4–R8 raise the tier further; R9–R12
are hygiene". **No task is marked done**; status words in RESPONSE_PLAN: "running" (W7-SEP, W7-SEC, S-ELS, O-LS0), "in progress"
(O-PW2), candidates "unreviewed".

### 7.1 Major points → response (RESPONSE_PLAN §1) → tasks / dependencies
| # | Objection (statement attacked; core) | Planned response | Tasks / dependency / state |
|---|---|---|---|
| M1 (major) | "All theory is asymptotic, the thresholds are at n ≈ 2·10⁶, and the simulations are at n = 200". Items (a) q_n ≤ ½ only from n≈2.1·10⁶; (b) beta-min ≥43× executed signal; (c) 2^B rates vacuous below n≈10⁹; (d) dilution masking in no theorem; (e) HPM found by Gibbs flips, no theorem. Sub-point: SE_w ≤114 columns at n=200 only because K=100 binds; λ_min(G) ≤ 0.22 in S4. | "We agree that no theorem quantifies the n = 200 numbers, and we now say so once, before the theorems"; LH scaling study; explicit c₀(s₀,A) and first-n table; "we do not claim the theorem bites at n = 200"; posterior term "which we observe (565/2,394 posterior misses, 0 discovery misses) and do not prove to be small"; O-SWAP only if it survives review. Fix also: move n = 200 disclosure to a remark after Theorem 4 + simulation paragraph. | R2 LH-SCALE (compute, NOTS; not started), R9 T03-CONST; O-SWAP "candidate". Open. |
| M2 (major) | "The main theorem requires a method tweak (LS0) that the reported simulations did not run"; also (b1) "is the favourable regime in disguise, one lattice away". Evidence: LS0 on all 2,400 fits with diff, or masked theorem for A. | Theorem 5(b) restated for v3 without LS0 on LH via O-BGIBBS BG1 or W5-B2ENV B2-LH "whichever survives cross-family verification"; LS0 becomes a remark costing ≤ 1 + (ℓ+1)max_k[p + k(p−k)] scores; O-LS0 diff reported; "LS0 can only reveal posterior misses, never create discovery misses". | R1 V-NOTWEAK (depends on O-BGIBBS/W5-B2ENV/O-MIX being cross-family VERIFIED), R12 LS0-DIFF (O-LS0 "is running it"). Open. Fallback §4.6: if R1 fails "Theorem 5(b) stays an LS0 theorem… a lower tier". |
| M3 (major) | No-LS0 routes (b1′),(b2) are "hypotheses-as-conclusions" (DELIV, REP OPEN); C1 shows bridge mass insufficient; β_H vacuous at n=200 (Hη ≈ 4–16); "A-REV1 classified the whole supplied T38(b)-R statement as GAP; W6-FIXREV1 repaired it to 'PROVED as a conditional theorem'… The paper must not call that a consistency theorem for the masked regime." | "Agreed as to the draft." One explicit family LH for unmodified method (R1); (b1′)/(b2) to supplement; C1 kept; "For the study's own designs we claim no theorem"; S-ELS ledger extraction "running". | R1; S-ELS running. Open. |
| M4 (major) | "The favourable regime is where the sampler is unnecessary"; Thm 5(a) is T11(iii); Thm 6 needs (T_n+1)Δ_n→0; "1 of 2,394 fits is favourable at n = 200". Demands separation theorem + masked-regime Ẑ/PIP statement. | Separation Theorem (W7-SEP) as spine; Thm 5(a) becomes corollary; F-MASKPIP Prop M1/M2. Rebuttal cites "importance weights have χ² → ∞ by F-DRAFT Theorem W". | R4 V-SEP ("Depends on W7-SEP delivering"; W7-SEP "running"); R8 V-MASKPIP (M1 "candidate PROVED"). Open. |
| M5 (major) | 2^B factor: 2^B√(log n/n)=2.7·10³ at n=200, 497 at 10⁴, 61 at 10⁶; (P1) on realised T_n circular; ORTH PROOF SKETCH with (T^max+1)Δ_n ≥ 44 at n=163,840. Notes "W3-PXN claims O_P(√(log n/n)) without 2^B for iid rows, unverified; W5-FAVIID… unverified". | 2^B-free rate primary after R6; R5 to prove T_n ≤ C log(1/Δ_n)-type; "If R5 fails, Theorem 6 is stated with the realised T_n and labelled as such." Rebuttal: realised T_n is 1–2, exact p = 18 scans give (T+1)Δ_n ≈ 0.02. | R6 V-FAVIID, R5 T26-BUDGET (related O-STAGES in LEDGER). Open. |
| M6 (major) | No positioning vs Yang–Wainwright–Jordan 2016 (AoS 44(6)) and Zhou–Yang–Vats–Roberts 2022 (JRSS-B 84(5)); also Zanella–Roberts 2019, Griffin–Łatuszyński–Steel 2021; "The novelty audit on `theory/A-DRAFT` does not mention these papers." Referee unsure of page numbers ("Check exact titles… before quoting"). | "Relation to computational guarantees" paragraph; adopt A-DRAFT wording "a BVS-specific construction and analysis within established SMC principles"; check whether LH satisfies their conditions. | R3 MIX-POS (reading only; not started). Open. |
| M7 (major) | Ẑ/PIPs mean nothing in masked regime; 95% bound is Markov; O-CERT shows no upper bound; pooled PIP biased by −Cov/Z. | Add Prop M1/M2 (Theorem 6′); state 0.05Ẑ one-sided; report islandwise product; "We do not promise a two-sided band (PW2) unless O-PW2 delivers." | R8 V-MASKPIP; O-PW2 "in progress". Open. |
| M8 (major) | Verification status: "all verification by the campaign is same-family"; Thm 5(c) conditional on T32(i) CONJECTURE; SR, GUARD as hypotheses; cross-family unreviewed list: "Lemma M, LS-score, LH-LAT, Theorem W, W3-PXN, W4-SHARE, W2-T26, W2-BOOK". Rebuttal: "two cross-family reviews found real errors (Prop. U, Lemma S attainment, E3(ii), Lemma U's constant, Lemma 0(b), the 1.2·10⁵ threshold) and all were repaired and re-checked". | T32(i) proved (W7-SEC "running"); SR/GUARD into algorithm definition; W5-LOCKBOOK code audit (R10); self-contained supplement (R11); no verdict word in paper. | R7 U-MODEL, R10 CODE-AUDIT, R11 SUPP-WRITE. Open. |

### 7.2 Minor points (verbatim gist) → response
RESPONSE_PLAN: "**Minor points.** All twenty are accepted; m1, m2 (notation clashes), m3–m5 (self-contained statements), m7, m8
(no campaign bookkeeping in theorem text), m14 (P(U) not a model probability) and m20 (§6 too long) are handled by task R11 and
R7; the rest are edits."
- m1 notation clash m(S) (marginal likelihood vs |S₀∖S|) → R11. m2 clash D_S (determinant ratio vs progress event) → R11.
- m3 Theorem 2 never stated as one theorem → R11. m4 undefined constants (q, e, κ, ε in (H2), B′, ρ*, LD♭, c_*(x), v(x), η(x),
  ε_del) → R11. m5 hypotheses defined by file reference (VIS, NL_η, NL_avg(κ), EXP′) → R11.
- m6 "Not claimed" lists inside theorems → edit. m7 branch names / verdict words in typeset text → R11. m8 Theorem 5 clause about
  unverified single LH-iid run → R11.
- m9 s₀ fixed vs s₀=⌊√n⌋=14 at n=200 → edit (state once in simulation section). m10 K=min(p,⌊n/2⌋) consistency ("W6 correction
  S3") → edit. m11 Theorem 1(iv)/(v) to corollary/remark → edit. m12 Lemma 0 and literal-TD lemma placement → edit.
- m13 EX-A vs floating point, VAL-FP unmeasured → edit (R10 includes a VAL-FP replay on 10 fits). m14 "P(U) is not a probability in
  the model" → R7. m15 (P1) on realised T_n → edit/R5. m16 recovery requires P(U)→0 "which this theorem does not provide" → edit.
- m17 Prop 1(iv) wording → edit. m18 Thm 2(v)(a) "for every d" delete → edit. m19 |ψ|<ρ cliff and g ≤ B < 2g into hypothesis
  line → edit. m20 §6 too long → R11.
Move-to-supplement list: Thm 2(ii) EXP′, literal-TD lemma, Theorem B′, Lemma RO, Prop 2(c)–(d), Thm 5(c) until T32(i), Remark
"Conditional routes" unless one route is proved, §6 items 4–9.

### 7.3 Task specs (RESPONSE_PLAN §3) — dependencies, none done
R1 V-NOTWEAK (verify O-BGIBBS BG1 → W5-B2ENV B2-LH/D2-LH → O-MIX B3 "fallback only"; inputs include "W4-SHARE Prop. M and Lemma PD;
W1-T38E D2"); R2 LH-SCALE (NOTS, 3×4×2×100 fits, n∈{400,1600,6400,25600}, g=9, ρ∈{0.6,0.85}, ψ∈{0.3,0.5}, s₀=2c+4; LS0 post hoc with
emit_centre=true); R3 MIX-POS; R4 V-SEP (depends on W7-SEP); R5 T26-BUDGET; R6 V-FAVIID ("W5-VMASK has a same-family check of
W3-PXN; this task is the cross-family one"); R7 U-MODEL; R8 V-MASKPIP; R9 T03-CONST (reproduce W2-VT03R R1); R10 CODE-AUDIT (reuse
W5-LOCKBOOK); R11 SUPP-WRITE (S.7 "T38 (W6-FIXREV1 version)"); R12 LS0-DIFF (O-LS0 running on Owls).
§4 Concessions with no task: no theorem for n=200 dilution masking ("a sharp-constant T03 for growing s₀ is CONJECTURE W′ at
P(provable) ≈ 0.3" — note label clash with F-DRAFT's W′); Theorem 1 constants stay far from signal; route (b2) in general OPEN;
masked Ẑ/PIP consistency not claimed; no superiority over SuSiE/SSL/informed MH; if R1 fails, LS0 theorem, lower tier.
Empirical paragraph (§4 of report): c=0.5 SMC-BVS 370/600 and 340/600 vs SuSiE 220/205, SSL 303/255; c=1 559/560 vs SuSiE
585/582; "the comparison with SuSiE/SSL is a comparison of *targets* as much as of *algorithms*".

---

## 8. Disagreements (Astra vs Opus; plus Astra vs Fable and Fable vs Astra, labelled)

Astra vs Opus (author/verifier position → Astra position):
1. **Prop U (W1-T24G):** Opus: independence move bad "iff" it leaves the family or raises V; extra-for-extra swaps neutral. Astra:
   ERROR (truth-removal omitted; swap may leave phase-1 family); Theorem B unaffected.
2. **Lemma S attainment (W1-T38E; W3-VT38E called it "tight"):** Opus: bound attained by two-level weights on full domain. Astra:
   ERROR for f ≤ 1−e; D2 unaffected.
3. **E3(ii) (W1-T38E):** Opus: aggregation lower bound without q<1. Astra: ERROR (p=2 counterexample 1.98×10²³ vs 9.44×10⁻¹⁴).
4. **Lemma U / EXP′ limit (W1-EXP, W2-PREM; W3-VEXP did not flag):** Opus 0.52/c_*. Astra (A-REV1, A-REV2): 0.51/c_*; A-REV3: W3's
   U1 inequality "≤ 1" false (→20.4).
5. **T38(b)-R (W1-T38E, verified W3-VT38E; repaired W6-FIXREV1 to "PROVED as a conditional theorem" per F-REFEREE):** Astra A-REV1:
   "**GAP**" as supplied; only the §7 repaired formulation "VERIFIED as a conditional implication". Whether W6-FIXREV1 matches §7 is
   not checked in these sources.
6. **NL0 quantifiers (W1 §6):** Opus wrote sup_W Σ_l; Astra: GAP, η is Σ_l sup_W; W2-PREM already corrected (agreement with W2-PREM).
7. **CE1 (W1/W2):** Opus blanket correlated-design asymptotic; Astra GAP, narrow explicit repair only.
8. **CF(1) D2 number (prior Opus referee):** reported 3.133×10⁻⁹; Astra: that is only the last exponential, full bound 2.244×10⁻⁷ +
   P(NBᶜ).
9. **T03 proof onset (W1-T03R):** Opus ≈1.2·10⁵; Astra ERROR, agrees with Opus verifier W2-VT03R (2116048 / 2457025).
10. **T37 A5(a), Lemma 0(b), D_S equivalence, "weakest" prose (W1-T37R):** Astra ERROR on each (A5(a) and "weakest" agree with
    verifier W3-VT37R's R1/R3).
11. **V37 R2 (Opus verifier W3-VT37R's repair):** Opus: failures split into E_LS^c or E_LS with terminal ≥ F(S0). Astra: ERROR,
    omits inferior local maximum. Astra also: "This refutes the inference used to explain all 541 benchmark failures by initial
    monotonicity."
12. **V37 R4 (W3-VT37R):** printed `p P(|Z|>=u)`; Astra: does not follow.
13. **W1-EXP Theorem 4 "iff" / W3-VEXP R4 "p^-c alone… whatever eta":** Astra ERROR / "not justified".
14. **W1-EXP §4.3 exact-normal delta:** Astra: incorrect (spherical direction), conclusion survives.
15. **W2-PREM Lemma U extra quantifier and C3 lower bound:** Astra GAP / ERROR (μ∈span(X_T) needed).
16. **W3-PXN P6, P7, joint T38(b) LS0 route:** Opus PROVED-candidate; Astra GAP (Tr beyond range; Beta shape (n−2−s)/2 not
    (n−3−s)/2; NB obligations).
17. **W4-SHARE M(b), BM-C scope, §7 exit-loss, SH(iii) prose, G extrapolation, D4 constant:** Astra ERROR/ERROR/ERROR/GAP/GAP; D4
    constant g(1)=1/(e−1) not ½.
18. **W2-T26:** Opus "single premise" shorthand and "exact branch fails whenever p ≥ 18 and n ≥ 22"; Astra GAP and ERROR (p=18,
    n=2^18 enumerates). Prop C: Opus PROOF SKETCH, Astra GAP (consistent).
19. **W2-BOOK:** Opus GUARD "every reported output" equals R̄ component; Astra ERROR (metadata). Opus "Every completed wrong HPM is
    a posterior miss"; Astra ERROR B5. Opus E[1_O Ẑ] ≤ Z P(A) unconditional; Astra GAP B3 (fixed-data only). Opus Remark 3 exact
    branch trivial; Astra GAP B4. Opus "exact" 50-digit numerics; Astra GAP B6.

Astra vs Fable (F-DRAFT): W2 "PROVED modulo EXP′" vs **ERROR**; NM "PROVED modulo T03/EXP′/Cor. P1" vs **ERROR** + scope GAP (and
NM(v)'s O(1) grid claim not proved by W″); W4 "PROOF SKETCH" vs **GAP** (KL layer omission); W1 agreed (PROVED / VERIFIED).
A-DRAFT vs F-DRAFT: F-DRAFT says NM "disposes of §13.2 (Song–Liang) in one sentence" and is "the precise statement of the UQ
defect of a split-and-merge *selection* rule"; A-DRAFT: the counterexample "refutes naive union, **not Song–Liang's second
selection stage**", comparison OPEN. F-DRAFT says §13.1 covered ("extends in one line"); A-DRAFT: §13.1 "false for arbitrary
bounded functions if 'ground truth' means the value at the generating parameter".
Fable F-REFEREE vs Astra: (a) M6 faults A-DRAFT's novelty audit for omitting Yang–Wainwright–Jordan and Zhou et al. (A-DRAFT was
scoped to six named works). (b) M5 calls W3-PXN's 2^B-free rate "unverified" and R6 asks for cross-family verification — A-REV3
already VERIFIED W3 P1–P5/Lemma B/P3 (W5-FAVIID still unreviewed). (c) M8 lists W3-PXN, W4-SHARE, W2-T26, W2-BOOK as "unreviewed
cross-family" — A-REV3/A-REV4 had reviewed them (Theorem W itself, Lemma M, LS-score, LH-LAT remain unreviewed cross-family). (d)
M8 rebuttal "all were repaired and re-checked" lists only six errors; A-REV2 found more (V37 R2, D_S, A5(a), Thm 4 iff, C3, Lemma U
quantifier) — repair status not verifiable here. (e) M1/M7 lean on "all 565 misses are posterior misses"/"0 discovery misses";
A-REV4 B5 says the BOOK logical claim is ERROR and A-REV2 refutes explaining the (541) failures by initial monotonicity. (f) M4
rebuttal relies on "χ² → ∞ by F-DRAFT Theorem W" — W(a) is "PROVED modulo W2", and W2's exact identity is ERROR per A-REV4.

---

## 9. LS0, common σ², n = 200 disclosure — every mention

**LS0.**
- A-REV1: E3 "VERIFIED with centre scoring and completed scans… LS0 is a method extension"; emit_centre=true required; budget
  1+(ℓ+1)max_{k≤K}[p+k(p−k)]; "None of this implements LS0 in the production method; adoption remains a separate decision"; LS0
  reproduction CF(2) n=400 truth scored.
- A-REV3: production LS starts "from the scored HPM, **not automatically from the start mode**. Thus LS0 remains an explicit
  modification"; W3 joint T38(b) LS0 route GAP; LH n=200 p=750: LS0 scored truth 3/3, endpoint truth 2/3.
- A-DRAFT: "W4's fully instantiated masked LS0 route changes the method"; "W4-T38FULL distinguishes LS0 from unmodified v3".
- F-REFEREE M2 (headline about v3+LS0, 2,400 fits run without LS0; draft §6 item 6: 113/128 scored S₀ when |S̃₀ Δ S₀| ≤ ℓ+1, 13/32
  beyond); R1, R2 (post hoc, emit_centre=true), R10, R12 LS0-DIFF; concession 6.
- THEORY_PRIORITIES: LS0 "deterministic, about ℓ·p extra scores, addable after the fact" (inconsistent with A-REV1's
  1+(ℓ+1)max[p+k(p−k)] count adopted by F-REFEREE). LEDGER: O-LS0 on Owls (running); O-MIX "LS0 vs mixture-of-block-starts vs
  common σ²".
**Common σ².**
- F-DRAFT Lemma W1: "with a *known* σ² the same tables give d ≡ 0 and π₀ = π exactly" (PROVED); A-REV4: W1 **VERIFIED** ("known
  common variance… additive across blocks"). F-DRAFT §6 method note: "with a common noise scale (known σ², or a single plug-in σ̂²
  from a preliminary fit used in *all* tables) the tables would give d ≡ 0 under BO… A plug-in-σ² table is therefore the one cheap
  method change that attacks the n = 200 masking at its cause… I flag it; I do not recommend acting on it inside this campaign";
  confidence P(true) 0.6, "pilot question", method change "yes". Caveat: Astra verified only the **known**-σ² statement; the
  plug-in σ̂² (data-dependent) variant was not reviewed. Only EXP′-dependent results (T22(iii), W1-EXP) "would need redoing" per
  F-DRAFT.
- F-REFEREE: no mention of common σ² (mentions dilution only). LEDGER: F-SIGMA "theory of the common-σ² start (validity, start mass,
  T38 route (a) without LS0, pilot design)"; O-MIX.
**n = 200 disclosure.**
- F-REFEREE M1 (whole point), m9, m20; draft facts quoted: thresholds n≈2.1·10⁶, beta-min ≥ 43×, 2^B vacuous below 10⁹, dilution
  "6–12 of 14 truths missing", SE_w ≤ 114 columns because K=100, λ_min ≤ 0.22 in S4, 98% fresh scores from Gibbs flips, local search
  repaired 0 fits, Hη ≈ 4–16, Δ_n ≈ 1, 1 of 2,394 fits favourable, 565 posterior misses. Fix: move disclosure "to a short remark
  after Theorem 4 and a short paragraph in the simulation section".
- A-REV2 §3.5: m♯=100 vs locked 201/215 at (200,500)/(200,1000); onset correction 2116048/2457025; "make the asymptotic rate
  numerically informative" — not. A-REV2 §5.1: no proof a particular n=200 dataset is on the floor event.
- A-REV1: Lemma U checks at n=200/800; P1 a₁ not production constants. A-REV3: LH at n=200, p=750.
- F-DRAFT: study design bracket 2.9 nats, π₀(S₀) ≈ 10⁻¹², +28 nats masking; NM a₁ ≥ 0.14 at n=200 (p=20 designs).
- A-DRAFT: "proof thresholds remain far beyond the study scale".
- THEORY_PRIORITIES: "At n = 200, SE is *impossible* (rank ≤ 199 against subsets of 215–229 columns), and beta-min fails by about
  100× in squared signal… the risk to *relevance* at n = 200 is accepted and must be disclosed"; T22(iii) rate vacuous at n=200
  (≥ 2,667); ℓ = 10 < s₀ + d = 15. (F-REFEREE says beta-min ≥ 43× and SE_w ≤ 114 columns — different figures from the
  THEORY_PRIORITIES "100×"/"215–229 columns", the latter predating the T03♯ restatement.)

---

## 10. Inconsistencies noticed
1. F-REFEREE (13:47–13:51 CST) treats W3-PXN, W4-SHARE, W2-T26, W2-BOOK as unreviewed cross-family; A-REV3 (13:29) and A-REV4
   (13:25) had already reviewed them. R6's W3-PXN part is largely done (VERIFIED), and R1's input "W4-SHARE Prop. M" has M(b) ERROR.
2. "541" (A-REV2, benchmark failures) vs "565/2,394" (F-REFEREE posterior misses) — different counts; and the "all misses are
   posterior misses" claim is a logical ERROR in W2-BOOK (A-REV4 B5) unless backed by audit data.
3. "Prop M" is overloaded: A-DRAFT Prop M (naive merge, COUNTEREXAMPLE, not cross-family reviewed), W4-SHARE Prop M (A-REV3 M(a)
   VERIFIED / M(b) ERROR; this is LEDGER's "Prop M" for A-REV3), F-MASKPIP Prop M1–M3, O-CERT Lemma M. "W′" is also overloaded
   (F-DRAFT stage-count conjecture vs RESPONSE_PLAN "sharp-constant T03 … CONJECTURE W′").
4. "Theorem B" is overloaded (T24 Gibbs-path vs W2-T26 Theorem B); A-DRAFT flags it.
5. LS0 cost: THEORY_PRIORITIES "about ℓ·p" vs A-REV1/F-REFEREE 1+(ℓ+1)max_k[p+k(p−k)].
6. F-DRAFT crosswalk calls EXP′ "verified by W3-VEXP" (same-family); cross-family A-REV2 VERIFIED it with the 0.51 correction.
7. A-REV3 W3 P4 VERIFIED but notes locked T27's literal premise (p comparable to one fixed power of n) is not met by an
   oscillating exponent sequence.

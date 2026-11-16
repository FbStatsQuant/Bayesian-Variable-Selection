# W3-AUDIT track A — assumption inventory of the core theorems (Opus helper, mechanical)

Author: W3-AUDIT track A inventory helper (Opus 5.5, high), for the Theory Dept manager and the audit Fable.
Date: 2026-11-16 (started 16:06 CST). Base: branch `theory/W3-AUDIT` at `a7fc5093`; registry
`Theory_work/INFRA/registry/claims.tsv` (516 rows) and `assumptions.tsv` (131 rows) **of this worktree**; card
`/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/CLAIMS_CARD.md` v1.6 (W3-READER worktree @ `7eb818e6`).
Scope: BRIEF.md "Scope: the core theorems" — card rows 1.1, 1.2, 2.1, 3.1, 3.6 + 3.5, 1.3. Mechanical: nothing here is
proved; statuses are quoted, never upgraded; the bucket words (proved-and-checked / proved-unchecked / missing) are this
helper's reading of the quoted status and are open to the Fable's track-A classification check.

## 0. How the tables were built

1. **Masters per row** = the claim ids the card cites for that row (listed above each table).
2. **Closure** = every claim reachable from the masters along the registry `depends_on` column, to the leaves (script
   output reproduced in each table's "carried by" column). Each assumption/premise id is taken from the `assumptions`
   and `consumes` columns of every claim in the closure.
3. **Tier** (per row): **D** = on a master claim itself; **S** = reached through statement-level edges (`@stmt`, `@hyp`, or
   untyped); **R** = reached only through an `@proof` edge — i.e. a hypothesis of a cited *parent* theorem whose sub-step
   is used (mostly the historical routes `W1-GEN:Thm-GEN`, `C-GROW:Thm-GROW`, `W2-FAC-A:Prop-F-FAC`). R items are listed for
   completeness; they are **not** hypotheses of the core theorem unless the proof uses the whole parent theorem.
   Exception noted under row 3.6 (the start premises of Thm 10 sit behind an `@proof` edge).
4. **Composite ids are expanded** (rows `↳…`): `A:OP`, `A:N1-KERNEL` and `A:DELIVERY-ALLOC` bundle components with
   different statuses (e.g. GUARD-W vs MEAS). Components inherit the composite's tier. `W3-RM:E4`'s code-level hypotheses
   (`↳E4.*`, from its statement text, not the registry) are added to row 3.1; row 3.5 adds CAL and EX-A/H-U from
   `W1-N1/STATEMENT.md` §2 (premises of Thm-N1 not listed in its registry row).
5. **Kind**: **A** = mathematical object — distribution (start law, posterior), divergence, prior property, kernel or
   algorithm property (including code facts the theory needs); **B** = design or data (law of the rows, noise law,
   coefficients, eigenvalue/visibility/leakage conditions, dimension); **M** = method premise, idealisation or allocation
   that is *stated, not provable* (exact arithmetic, ideal uniforms, machine, allocation). Borderline calls: notes †, ‡.
6. **Status** (A only): the claim that discharges the item, its registry status verbatim, and a bucket.
   **Source** = definition site (`file:line`, repo-relative); where the registry `source` was blank or a range, the line of
   the definition found by grep is given.
7. **Lean target** (A only): *yes* = a self-contained finite or analytic statement (code correspondence excluded).

## 1. Registry and card drift found while building (for the recorder; no edits made)

- **D1 (row 3.6).** The card cites `W3-START2:IF-START@1.0.0`; the registry has it at `@1.1.0`, state
  `SUPERSEDED-VALID`; the ACTIVE successor is `W3-START2-R:IF-START@1.0.0` ("PROVED-CHECKED; council R2, MANIFEST
  12bb52cd…, sol=9.0 PASS, opus=9.3 PASS"), whose chain (`W3-START2-R:START-R`, `:BR`) carries `A:START2R-R-L`,
  `A:START2R-R-L0` instead of `A:START2-R-L`. The 3.6 table follows the card's cited input.
- **D2 (row 2.1).** Card: `W3-DIST:DIST-C` is "delivery statements, not used by Cor 9C". Registry: `W3-DIST:Cor-C`
  `depends_on` contains `W3-DIST:DIST-C@stmt`, which pulls all `W3-SAMP` premises (N1 contract, CAL, P-MAP, P-OVL, NC-R,
  P-START, IND-T, …) into row 2.1's closure (tier S). If the card is right, that edge should be `@proof`/removed; if the
  registry is right, Cor 9C carries the sampler contract.
- **D3 (row 1.1).** Registry `W3-POST2:C@1.0.5` status reads "PROVED-CHECKED, conditional on W3-POST:Prop-LB, [L1a′],
  W2-APP:POST, W3-POST:Thm-1" (SOP:TH09, SOP:TH128 no longer listed); the card quotes `@1.0.4` with them. Same for
  `W3-POST2:E@1.0.5`. `SOP:TH09@1.0.2` is now "PROVED-CHECKED (T03♯ only: …)", so Form A applies; `W3-POST:Thm-1@1.0.0`
  still carries the old label "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)".
- **D4 (row 3.1).** `W2-UNI:F-UNI@2.1.0` is "PROVED-CHECKED" in the registry, but the file header
  `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:3` still says "PROVED (by this seat, unchecked)". The registry source of
  `A:IDEAL-W+` (`Theory_work/Dept/research/FUNI_NARROW/A_IDEALW_PLUS.md@fc30c749`) does not exist in this worktree; the
  definition used here is `L5_delivery.md:19`.
- **D5 (row 3.5).** `W3-READER:PoolZ` is not in this worktree's `claims.tsv`.
- **D6.** `W1-N1:Thm-N1`'s registry row lists `A:OP` (LS0 premises) but not CAL / EX-A / H-U, which its statement
  §2 names (`W1-N1/STATEMENT.md:70-79`). `A:N1-KERNEL`'s registry source is `:64`; §2 starts at `:68`.
- **D7.** `A:BLOCK-LE-16` bridge column is "MISSING" in `assumptions.tsv`; `A:IID-GAUSS-ROWS` bridge "MISSING" (per family
  bridges exist; noted, B-kind).

## 2. Per-theorem tables


### Row 1.1 — Core 1 — the posterior finds the true model (fixed design)

Masters (registry `claims.tsv`, status verbatim, council suffix cut at "; council" where marked …):
- `W3-POST2:C@1.0.5` (ACTIVE; `Theory_work/Wave3/W3-POST2/STATEMENT.md:83-94`): "PROVED-CHECKED, conditional on W3-POST:Prop-LB, [L1a′], W2-APP:POST, W3-POST:Thm-1"
- `W3-POST2:E@1.0.5` (ACTIVE; `Theory_work/Wave3/W3-POST2/STATEMENT.md:126-133`): "PROVED-CHECKED, conditional on W2-APP:POST, W3-POST:Thm-1"
- `W3-POST:Thm-1@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-POST/STATEMENT.md:61-100`): "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"

Notes. The O_P form (abstract) is `W3-POST:Thm-1` = `SOP:TH09`; tiers D/S of the expectation form add (F0), (OS), (ID^M),
the alternatives C-ALT and the inputs of Prop-LB / L1a′ (EXT-FEAS, COEF-REP). Tier R items come from `W2-APP:POST`
(Thm-1 item 6 diagonal transfer, `@proof`) and from `W1-GEN:Thm-GEN` reached via `W3-POST:Thm-1 →(@proof) C-PACK:SL1 →
SL1.I-c → W1-GEN:Thm-GEN(C4) → W1-GEN:Thm-GEN` (instance list of SL1); none of the R items is a hypothesis of Thm 1 / 1′. No track-A item is
at tier D or S for this row: **every D/S assumption of row 1.1 is kind B.**

| id | tier | plain statement | source (file:line) | kind | status (A only; registry/statement text verbatim) | carried by | core theorems | Lean target |
|---|---|---|---|---|---|---|---|---|
| `A:BETAMIN` | D | Beta-min: smallest true coefficient ≫ √(log n / n) (BM-inf) or above a constant multiple (BM(c)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:11` | B | — | W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:ENERGY` | D | Bounded signal energy ‖Xθ*‖² ≤ Mn | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8` | B | — | W3-POST2:C, W3-POST2:E, W3-POST:Thm-1, W3-POST:Lemma-1a', SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) 1.3(D) | — |
| `A:FIXED-S0` | D | True model size s₀ ≥ 1 fixed in n; s₀ ≤ K eventually | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | W3-POST2:C, W3-POST2:E, W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) | — |
| `A:GAUSS-NOISE` | D | Noise N(0, σ²I) independent of the design, σ² fixed (data law; see note †) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:29` | B | — | W3-POST2:C, W3-POST2:E, W3-POST:Thm-1, W3-POST:Lemma-1a', SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) 1.3(D) | — |
| `A:P-POLY` | D | Polynomial dimension p ≤ n^A (p ≫ n allowed) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | W3-POST2:C, W3-POST2:E, W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(D) 3.6(D) | — |
| `A:POST2-C-ALT` | D | One of three alternatives: (F_λ),(F_w),BM(c) / (F_λ),(OS),BM(c) / (OS),(ID^M;c) | `Theory_work/Wave3/W3-POST2/STATEMENT.md:86-88` | B | — | W3-POST2:C | 1.1(D) | — |
| `A:POST2-F0` | D | Floor on the true model only: λ_min(X_{S₀}ᵀX_{S₀}/(n−1)) ≥ φ₀² | `Theory_work/Wave3/W3-POST2/STATEMENT.md:25` | B | — | W3-POST2:C, W3-POST2:E | 1.1(D) | — |
| `A:POST2-IDM` | D | Identifiability margin: every small model missing a truth leaves residual ≥ cσ*² log n | `Theory_work/Wave3/W3-POST2/STATEMENT.md:41` | B | — | W3-POST2:E | 1.1(D) | — |
| `A:POST2-OS` | D | Superset Occam-sum bound on supersets of S₀ (mixes prior Occam factors and design; see note ‡) | `Theory_work/Wave3/W3-POST2/STATEMENT.md:35` | B | — | W3-POST2:E | 1.1(D) | — |
| `A:SPARSE-EIG` | D | Anchored sparse eigenvalue floors on S₀ ∪ J (bounded \|J\|, and O(log n) \|J\| unnormalised) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8-10` | B | — | W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:COEF-REP` | S | Mean has a representation X_Tθ = μ with ‖θ‖² ≤ nM′ (implied by SPARSE-EIG at S₀ + ENERGY) | `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:11` | B | — | W3-POST:Lemma-1a' | 1.1(S) 2.1(S) | — |
| `A:EXT-FEAS` | S | 1 ≤ s₀ < p and s₀+1 ≤ K (a one-variable extension of S₀ is in the model space) | `Theory_work/Wave3/W3-POST/lemmas/LB_rate_lower_bound.md:11` | B | — | W3-POST:Prop-LB | 1.1(S) | — |
| `A:BLOCK-LE-16` | R | Method partition is X-measurable with every block of size ≤ B = min(⌊√n⌋, ⌊√p⌋, 16) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:61` | A | missing (partial): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" gives only B ≤ 16 (CC7); "every block ≤ B" has no claim; registry bridge "MISSING" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | yes (packing invariant: complete-linkage cut at B + next-fit packing ⇒ \|C_b\| ≤ B; finite) / code half no |
| `A:CAL` | R | Calibration record 𝓒 is a function of the data and streams 0–9 only (frozen before the final run) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:42` | A | missing: named premise (W1-N1/STATEMENT.md:79; W3-SAMP/STATEMENT.md:64-65); no code-reading claim in the closure | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(S) 3.1(S) 3.6(D) 3.5(D) | no (code fact) |
| `A:OP` | R | LS0 implementation premises: EX-A, EX-S, SR, GUARD-W, OP-LS0, e4/e4′, complete scans (composite; ↳ below) | `Theory_work/Wave1/W1-PXN/STATEMENT.md:45` | A | see components ↳OP.* | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | see components |
| `P:DERANDOMISE` | R | Fixed-design conclusions with common constants on design events ⇒ joint-law conclusion | `Theory_work/Wave1/W1-GEN/STATEMENT.md:115` | A | proved-and-checked: C-MIS:LemDR "R02 VERIFIED; council R07/R08 PASS" | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | yes (pure probability lemma) |
| `P:LS0-DISCOVERY` | R | Deterministic capped LS0 from the start mode scores S₀ (lattice descent) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:98` | A | proved-and-checked: C-GROW:L1.2 "PROVED-CHECKED" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | yes (deterministic descent on a finite lattice) |
| `P:M5-COMPOSITION` | R | P(output ∩ reported ≠ S₀) ≤ 2E[1−π(S₀)] + D_n; S₀ scored and π(S₀) > ½ ⇒ reported = S₀ | `Theory_work/Wave1/W1-GEN/STATEMENT.md:21` | A | proved-and-checked: SOP:TH05.0 T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (elementary inequality) |
| `P:POST-CONC` | R | Posterior concentration 1 − π(S₀\|y) = O_P(√(log n/n)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:13` | A | proved-and-checked: SOP:TH09 "PROVED-CHECKED (T03♯ only: …)" (fixed design); W2-APP:POST "PROVED-CHECKED" (Gaussian rows) | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | no |
| `P:SCORE-EXP` | R | Uniform expansion of score differences over polynomial families of models | `Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md:30` | A | proved-unchecked (route only): W1-GEN:L1 "PROVED (by this seat, unchecked)"; checked variant C-GROW:L0.1 "PROVED-CHECKED" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (Gaussian/χ² tail + union bound; analytic) |
| `P:START-CENTRE` | R | Start mode equals / sandwiches the reference model | `Theory_work/Wave1/W1-GEN/lemmas/L2_centre.md:12` | A | proved-unchecked (route only): W1-GEN:L2 "PROVED (by this seat, unchecked)" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | no |
| `↳OP.GUARD-W` | R | Stop-only guard: reads only the clock, consumes no uniform, changes no setting; a stop returns no output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | missing: "audit open, not discharged here" (W1-N1/STATEMENT.md:86-88); W3-SAMP/STATEMENT.md §3 "The full GUARD-W delivery audit" not claimed | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) 3.5(D) | no (code fact) |
| `↳OP.OP-LS0` | R | LS0 executed from the start mode, centre emitted, scans completed on every fit with output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-unchecked: W1-GEN:L5 ([OP] operational closure) "PROVED (by this seat, unchecked)"; centre-emission part inside W3-RM:E4 "PROVED-CHECKED" | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.SR` | R | Stop/return rule: every scored candidate enters the winner comparison; reported HPM = best scored model | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (final-run ledger half): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" (CC2); the stop half rests on GUARD-W (missing) | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.e4` | R | Emitted LS0 centre is a maximiser of the start law γ₀ | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (as replaced in row 3.1): W3-RM:E4 "PROVED-CHECKED" (code level, under ↳E4.H1+, EX-A, ↳E4.H4); still a bare premise on the W1-GEN route | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no |
| `↳OP.EX-S` | R | Fresh independent ideal uniforms (H-U) | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `↳OP.SCANS` | R | Complete scans: no operational interruption of any search | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `A:BLOCK-VIS` | R | Truths visible inside blocks given any ≤15 other columns (no masking) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:92` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:COEF-BOUNDED` | R | True coefficients in [θ_lo, θ_hi] in absolute value, fixed constants | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:11` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | — |
| `A:GRAM-FLOOR-LATTICE` | R | Gram floor φ₀² on Q ∪ {l} for every column l | `Theory_work/Wave1C/C-GROW/STATEMENT.md:91` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:IID-GAUSS-ROWS` | R | Raw rows i.i.d. N(m_n, Σ_n), noise independent of rows | `Theory_work/Wave2/W2-UNI/STATEMENT.md:38` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:LSF` | R | Population sparse floor: φ² on (s₀+j₀)-sets and ψ_n (vanishing slowly) on O(log n)-sets | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:23` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:POST2-FLAMBDA` | R | Anchored floor φ₀² on S₀ ∪ J, \|J\| ≤ j₀ (bounded size) | `Theory_work/Wave3/W3-POST/STATEMENT.md:68` | B | — | W3-POST2:A1 | 1.1(R) | — |
| `A:RELEVANCE-SIZE` | R | Deterministic relevance set Q ⊇ S₀ of bounded / O(log n) / polylog size | `Theory_work/Wave1C/C-GROW/STATEMENT.md:89` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | — |

Count (1.1): AR=13, BD=10, BR=7, BS=2, MR=2

### Row 1.2 — Core 1 — the posterior finds the true model (Gaussian rows)

Masters (registry `claims.tsv`, status verbatim, council suffix cut at "; council" where marked …):
- `W2-APP:POST@1.0.7` (ACTIVE; `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:27-33`): "PROVED-CHECKED"
- `W3-POST:Thm-1@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-POST/STATEMENT.md:61-100`): "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"

Notes. Row 1.2 = Thm-1 item 6 + `W2-APP:POST`. The only A item at tier D is `P:DERANDOMISE` (consumed by `W2-APP:POST`).

| id | tier | plain statement | source (file:line) | kind | status (A only; registry/statement text verbatim) | carried by | core theorems | Lean target |
|---|---|---|---|---|---|---|---|---|
| `P:DERANDOMISE` | D | Fixed-design conclusions with common constants on design events ⇒ joint-law conclusion | `Theory_work/Wave1/W1-GEN/STATEMENT.md:115` | A | proved-and-checked: C-MIS:LemDR "R02 VERIFIED; council R07/R08 PASS" | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | yes (pure probability lemma) |
| `A:BETAMIN` | D | Beta-min: smallest true coefficient ≫ √(log n / n) (BM-inf) or above a constant multiple (BM(c)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:11` | B | — | W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:COEF-BOUNDED` | D | True coefficients in [θ_lo, θ_hi] in absolute value, fixed constants | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:11` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | — |
| `A:ENERGY` | D | Bounded signal energy ‖Xθ*‖² ≤ Mn | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8` | B | — | W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) 1.3(D) | — |
| `A:FIXED-S0` | D | True model size s₀ ≥ 1 fixed in n; s₀ ≤ K eventually | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | W2-APP:POST, W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) | — |
| `A:GAUSS-NOISE` | D | Noise N(0, σ²I) independent of the design, σ² fixed (data law; see note †) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:29` | B | — | W2-APP:POST, W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) 1.3(D) | — |
| `A:IID-GAUSS-ROWS` | D | Raw rows i.i.d. N(m_n, Σ_n), noise independent of rows | `Theory_work/Wave2/W2-UNI/STATEMENT.md:38` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:LSF` | D | Population sparse floor: φ² on (s₀+j₀)-sets and ψ_n (vanishing slowly) on O(log n)-sets | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:23` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:P-POLY` | D | Polynomial dimension p ≤ n^A (p ≫ n allowed) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | W2-APP:POST, W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(D) 3.6(D) | — |
| `A:SPARSE-EIG` | D | Anchored sparse eigenvalue floors on S₀ ∪ J (bounded \|J\|, and O(log n) \|J\| unnormalised) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8-10` | B | — | W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:BLOCK-LE-16` | R | Method partition is X-measurable with every block of size ≤ B = min(⌊√n⌋, ⌊√p⌋, 16) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:61` | A | missing (partial): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" gives only B ≤ 16 (CC7); "every block ≤ B" has no claim; registry bridge "MISSING" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | yes (packing invariant: complete-linkage cut at B + next-fit packing ⇒ \|C_b\| ≤ B; finite) / code half no |
| `A:CAL` | R | Calibration record 𝓒 is a function of the data and streams 0–9 only (frozen before the final run) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:42` | A | missing: named premise (W1-N1/STATEMENT.md:79; W3-SAMP/STATEMENT.md:64-65); no code-reading claim in the closure | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(S) 3.1(S) 3.6(D) 3.5(D) | no (code fact) |
| `A:OP` | R | LS0 implementation premises: EX-A, EX-S, SR, GUARD-W, OP-LS0, e4/e4′, complete scans (composite; ↳ below) | `Theory_work/Wave1/W1-PXN/STATEMENT.md:45` | A | see components ↳OP.* | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | see components |
| `P:LS0-DISCOVERY` | R | Deterministic capped LS0 from the start mode scores S₀ (lattice descent) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:98` | A | proved-and-checked: C-GROW:L1.2 "PROVED-CHECKED" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | yes (deterministic descent on a finite lattice) |
| `P:M5-COMPOSITION` | R | P(output ∩ reported ≠ S₀) ≤ 2E[1−π(S₀)] + D_n; S₀ scored and π(S₀) > ½ ⇒ reported = S₀ | `Theory_work/Wave1/W1-GEN/STATEMENT.md:21` | A | proved-and-checked: SOP:TH05.0 T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (elementary inequality) |
| `P:POST-CONC` | R | Posterior concentration 1 − π(S₀\|y) = O_P(√(log n/n)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:13` | A | proved-and-checked: SOP:TH09 "PROVED-CHECKED (T03♯ only: …)" (fixed design); W2-APP:POST "PROVED-CHECKED" (Gaussian rows) | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | no |
| `P:SCORE-EXP` | R | Uniform expansion of score differences over polynomial families of models | `Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md:30` | A | proved-unchecked (route only): W1-GEN:L1 "PROVED (by this seat, unchecked)"; checked variant C-GROW:L0.1 "PROVED-CHECKED" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (Gaussian/χ² tail + union bound; analytic) |
| `P:START-CENTRE` | R | Start mode equals / sandwiches the reference model | `Theory_work/Wave1/W1-GEN/lemmas/L2_centre.md:12` | A | proved-unchecked (route only): W1-GEN:L2 "PROVED (by this seat, unchecked)" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | no |
| `↳OP.GUARD-W` | R | Stop-only guard: reads only the clock, consumes no uniform, changes no setting; a stop returns no output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | missing: "audit open, not discharged here" (W1-N1/STATEMENT.md:86-88); W3-SAMP/STATEMENT.md §3 "The full GUARD-W delivery audit" not claimed | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) 3.5(D) | no (code fact) |
| `↳OP.OP-LS0` | R | LS0 executed from the start mode, centre emitted, scans completed on every fit with output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-unchecked: W1-GEN:L5 ([OP] operational closure) "PROVED (by this seat, unchecked)"; centre-emission part inside W3-RM:E4 "PROVED-CHECKED" | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.SR` | R | Stop/return rule: every scored candidate enters the winner comparison; reported HPM = best scored model | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (final-run ledger half): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" (CC2); the stop half rests on GUARD-W (missing) | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.e4` | R | Emitted LS0 centre is a maximiser of the start law γ₀ | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (as replaced in row 3.1): W3-RM:E4 "PROVED-CHECKED" (code level, under ↳E4.H1+, EX-A, ↳E4.H4); still a bare premise on the W1-GEN route | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no |
| `↳OP.EX-S` | R | Fresh independent ideal uniforms (H-U) | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `↳OP.SCANS` | R | Complete scans: no operational interruption of any search | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `A:BLOCK-VIS` | R | Truths visible inside blocks given any ≤15 other columns (no masking) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:92` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:GRAM-FLOOR-LATTICE` | R | Gram floor φ₀² on Q ∪ {l} for every column l | `Theory_work/Wave1C/C-GROW/STATEMENT.md:91` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:RELEVANCE-SIZE` | R | Deterministic relevance set Q ⊇ S₀ of bounded / O(log n) / polylog size | `Theory_work/Wave1C/C-GROW/STATEMENT.md:89` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | — |

Count (1.2): AD=1, AR=12, BD=9, BR=3, MR=2

### Row 2.1 — Core 2 — the posterior finds the true distribution (Thm 9)

Masters (registry `claims.tsv`, status verbatim, council suffix cut at "; council" where marked …):
- `W3-DIST:Thm-A@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-DIST/STATEMENT.md:185-207`): "PROVED-CHECKED; council …"
- `W3-DIST:Thm-B@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-DIST/STATEMENT.md:209-215`): "PROVED-CHECKED, conditional on W3-POST:Thm-1; council …"
- `W3-DIST:Cor-C@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-DIST/STATEMENT.md:217-238`): "PROVED-CHECKED, conditional on EX-A (exact arithmetic); council …"

Notes. Display (i) (abstract) is `W3-DIST:Thm-A`: its D/S assumptions are all kind B (A1–A5, and the inner premises RD,
SPARSE, DOM, ND, L0, TR0, COEF-REP, MISR-GRC that the PROVED-CHECKED bridges B0–B3 discharge from A1–A6). All tier-S A and
M items of this row enter through `W3-DIST:Cor-C → W3-DIST:DIST-C@stmt → W3-SAMP:*` (drift D2) except `A:EX-A` (on Cor-C
itself, "conditional on EX-A (exact arithmetic)"). Tier-R items come from `W3-POST:Thm-1` (input of Thm-B/B3) and its routes.

| id | tier | plain statement | source (file:line) | kind | status (A only; registry/statement text verbatim) | carried by | core theorems | Lean target |
|---|---|---|---|---|---|---|---|---|
| `A:EX-A` | D | Exact scores and arithmetic (named idealisation; no numerical margin) | `Theory_work/Wave1/W1-N1/STATEMENT.md:70` | M | — | W3-DIST:Cor-C, W3-DIST:DIST-C | 2.1(D) 3.1(S) 3.6(D) | — |
| `A:DIST-A1` | D | Gaussian linear model y = α* + xᵀβ* + ε, ε normal independent of x, any σ*² > 0 | `Theory_work/Wave3/W3-DIST/STATEMENT.md:174` | B | — | W3-DIST:Thm-A, W3-DIST:Thm-B, W3-DIST:Cor-C | 2.1(D) | — |
| `A:DIST-A2` | D | At most s nonzero coefficients, 2 ≤ p ≤ n^A | `Theory_work/Wave3/W3-DIST/STATEMENT.md:176` | B | — | W3-DIST:Thm-A, W3-DIST:Thm-B, W3-DIST:Cor-C | 2.1(D) | — |
| `A:DIST-A3` | D | Predictors sub-Gaussian along directions with ≤ q_n nonzero entries | `Theory_work/Wave3/W3-DIST/STATEMENT.md:177` | B | — | W3-DIST:Thm-A, W3-DIST:Thm-B, W3-DIST:Cor-C, W3-DIST:B1, W3-DIST:B2, W3-DIST:B3, W3-DIST:B2core | 2.1(D) | — |
| `A:DIST-A4` | D | No near-exact collinearity: λ_min(Corr(x_T)) ≥ c_ψ/n for \|T\| ≤ q_n | `Theory_work/Wave3/W3-DIST/STATEMENT.md:179` | B | — | W3-DIST:Thm-A, W3-DIST:Thm-B, W3-DIST:Cor-C, W3-DIST:B2, W3-DIST:B3 | 2.1(D) | — |
| `A:DIST-A5` | D | Bounded signal per predictor: \|β*_j\|·sd(x_j) ≤ b̄σ* | `Theory_work/Wave3/W3-DIST/STATEMENT.md:180` | B | — | W3-DIST:Thm-A, W3-DIST:Thm-B, W3-DIST:Cor-C, W3-DIST:B1, W3-DIST:B3 | 2.1(D) | — |
| `A:DIST-A6` | D | Detectable signal: fixed eigenvalue floor on (2A+3)s+2 sets + beta-min b_n²n/log n → ∞ | `Theory_work/Wave3/W3-DIST/STATEMENT.md:211` | B | — | W3-DIST:Thm-B, W3-DIST:B3 | 2.1(D) | — |
| `A:BLOCK-LE-16` | S | Method partition is X-measurable with every block of size ≤ B = min(⌊√n⌋, ⌊√p⌋, 16) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:61` | A | missing (partial): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" gives only B ≤ 16 (CC7); "every block ≤ B" has no claim; registry bridge "MISSING" | W3-SAMP:LT# | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | yes (packing invariant: complete-linkage cut at B + next-fit packing ⇒ \|C_b\| ≤ B; finite) / code half no |
| `A:CAL` | S | Calibration record 𝓒 is a function of the data and streams 0–9 only (frozen before the final run) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:42` | A | missing: named premise (W1-N1/STATEMENT.md:79; W3-SAMP/STATEMENT.md:64-65); no code-reading claim in the closure | W3-SAMP:D, W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR | 1.1(R) 1.2(R) 2.1(S) 3.1(S) 3.6(D) 3.5(D) | no (code fact) |
| `A:N1-KERNEL` | S | Sampler contract: START, KERNEL, MEAS, SI, potential run, worker equivalence (composite; ↳ below) | `Theory_work/Wave1/W1-N1/STATEMENT.md:68` | A | see components ↳N1.* | W3-SAMP:D, W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR | 2.1(S) 3.6(D) 3.5(D) | see components |
| `A:NC-R` | S | Non-collapse: lim_{η↓0} limsup_n P(𝒜 ∩ {W_r < η}) = 0 (particle weights) | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:84` | A | proved-and-checked (on the C-v route): W3-SAMP:C "PROVED-CHECKED" (C-v: "and NC_r holds") | W3-SAMP:LT# | 2.1(S) 3.6(D) | no |
| `A:P-MAP` | S | The F-maximiser over Ω equals S₀ w.p. → 1 (implied by posterior concentration) | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:78` | A | proved-and-checked: via P:POST-CONC + C-PACK:SL0 "PROVED-CHECKED" (HPM exact for δ < ½) | W3-SAMP:D | 2.1(S) 3.6(D) | yes (SL0 part: deterministic δ < ½ ⇒ argmax = S₀) |
| `A:P-OVL` | S | Computational overlap: D_r·π₀(S₀) → ∞ in probability on 𝒜 | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:82` | A | missing (one line): W3-SAMP:D "PROVED-CHECKED" (D-iv production corollary) reduces it to max(n,p)·log₂(n+1)·π₀(S₀) → ∞, which P-START gives; that implication is not registered | W3-SAMP:D | 2.1(S) 3.6(D) | yes (trivial real-analysis step) |
| `A:P-OVL-INF` | S | Global overlap: L / max_S π(S)/π₀(S) → ∞ on 𝒜 (Theorem TR only) | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:79` | A | missing: W3-SAMP/STATEMENT.md §3 "That NC_r, P-OVL or P-OVL∞ follows from primitive conditions on (X, θ*)" is not claimed | W3-SAMP:TR | 2.1(S) 3.6(D) | no |
| `A:P-START` | S | Start law concentrates: 1_𝒜(1−π₀(S₀))/π₀(S₀) → 0 in probability | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:76` | A | proved-and-checked: W3-START2:IF-START "PROVED-CHECKED" (state SUPERSEDED-VALID; successor W3-START2-R:IF-START "PROVED-CHECKED; council R2, MANIFEST 12bb52cd…, sol=9.0 PASS, opus=9.3 PASS") | W3-SAMP:C | 2.1(S) 3.6(D) | no |
| `P:POST-CONC` | S | Posterior concentration 1 − π(S₀\|y) = O_P(√(log n/n)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:13` | A | proved-and-checked: SOP:TH09 "PROVED-CHECKED (T03♯ only: …)" (fixed design); W2-APP:POST "PROVED-CHECKED" (Gaussian rows) | W3-SAMP:D, W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | no |
| `↳N1.KERNEL` | S | Coded step functions + random order realise the T12 kernels (π-invariant), order uniform and state-independent | `Theory_work/Wave1/W1-N1/STATEMENT.md:76` | A | proved-unchecked*: "PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT" (W1-N1/STATEMENT.md:76-78; no registry claim) — * an inherited check exists; Fable to rule | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | yes (math half: each coded move kernel is π-reversible on the finite Ω; code half no) |
| `↳N1.MEAS` | S | Realisation map (calibration, stream) → island record is jointly measurable | `Theory_work/Wave1/W1-N1/STATEMENT.md:83` | A | proved-and-checked: W1-N1:B "PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08." | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | no |
| `↳N1.POT` | S | Statements are about the potential (uninterrupted) run; identified with printed fields on completed runs | `Theory_work/Wave1/W1-N1/STATEMENT.md:86` | A | proved-and-checked for the completed-run identification: W3-SAMP:PC "PROVED-CHECKED" ("a limited comparison, not the full GUARD-W audit"); the GUARD-W half is missing (row ↳OP.GUARD-W) | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | no |
| `↳N1.START` | S | Coded start sampler draws exactly from π₀ and reports Z̄₀ = Σ_Ω γ₀ | `Theory_work/Wave1/W1-N1/STATEMENT.md:75` | A | proved-unchecked: N9 Claims S, Z "PROVED (candidate)" (W1-N1/STATEMENT.md:75; no registry claim) | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | yes (algorithm-level: block sampler is exact for the product-form π₀ under the size cap; finite) |
| `↳OP.GUARD-W` | S | Stop-only guard: reads only the clock, consumes no uniform, changes no setting; a stop returns no output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | missing: "audit open, not discharged here" (W1-N1/STATEMENT.md:86-88); W3-SAMP/STATEMENT.md §3 "The full GUARD-W delivery audit" not claimed | ↳ of A:N1-KERNEL | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) 3.5(D) | no (code fact) |
| `A:EX-A-HU` | S | EX-A plus ideal i.i.d. U[0,1) uniforms within each stream (H-U) | `Theory_work/Wave1/W1-N1/STATEMENT.md:70-71` | M | — | W3-SAMP:D, W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR | 2.1(S) 3.6(D) 3.5(D) | — |
| `A:IND-T` | S | Final streams 10–13 mutually independent and independent of streams 0–9 (D-ii only) | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:65` | M | — | W3-SAMP:D | 2.1(S) 3.6(D) | — |
| `↳N1.SI` | S | Final stream 9+r independent of streams 0–9 (single-island; RNG idealisation) | `Theory_work/Wave1/W1-N1/STATEMENT.md:80` | M | — | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | — |
| `↳N1.WORKER` | S | Worker equivalence for concurrent islands (v3.1 only; frozen core is serial) | `Theory_work/Wave1/W1-N1/STATEMENT.md:89` | M | — | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | — |
| `A:BETAMIN` | S | Beta-min: smallest true coefficient ≫ √(log n / n) (BM-inf) or above a constant multiple (BM(c)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:11` | B | — | SOP:TH09, W3-POST:Thm-1 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:COEF-REP` | S | Mean has a representation X_Tθ = μ with ‖θ‖² ≤ nM′ (implied by SPARSE-EIG at S₀ + ENERGY) | `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:11` | B | — | W3-DIST:DIST-1, W3-DIST:DIST-2, W3-DIST:DIST-C, W3-DIST:X, W3-DIST:X' | 1.1(S) 2.1(S) | — |
| `A:DIST-DOM` | S | At least two retained (non-constant) columns, p_ret ≥ 2 | `Theory_work/Wave3/W3-DIST/STATEMENT.md:31` | B | — | W3-DIST:DIST-1, W3-DIST:DIST-2, W3-DIST:DIST-3, W3-DIST:DIST-C | 2.1(S) | — |
| `A:DIST-L0` | S | Bounded ridge loss of the true model, L_{S₀} ≤ B (discharged by B1 from A1–A5) | `Theory_work/Wave3/W3-DIST/STATEMENT.md:57` | B | — | W3-DIST:DIST-3 | 2.1(S) | — |
| `A:DIST-ND` | S | No degeneracy on average (ADG) over supersets of S₀ (discharged by B2 from A3–A4) | `Theory_work/Wave3/W3-DIST/STATEMENT.md:60` | B | — | W3-DIST:DIST-1, W3-DIST:DIST-C, W3-DIST:X | 2.1(S) | — |
| `A:DIST-RD` | S | Rows i.i.d. from an arbitrary law; Gaussian noise independent of the design, σ*² fixed | `Theory_work/Wave3/W3-DIST/STATEMENT.md:19` | B | — | W3-DIST:DIST-1, W3-DIST:DIST-2, W3-DIST:DIST-3, W3-DIST:DIST-C | 2.1(S) | — |
| `A:DIST-SPARSE` | S | True support of fixed size s₀ ≥ 0 (null truth allowed) | `Theory_work/Wave3/W3-DIST/STATEMENT.md:19` | B | — | W3-DIST:DIST-1, W3-DIST:DIST-2, W3-DIST:DIST-3, W3-DIST:DIST-C | 2.1(S) | — |
| `A:DIST-TR0` | S | Population vs sample second moments comparable on the true support (discharged by B3) | `Theory_work/Wave3/W3-DIST/STATEMENT.md:101` | B | — | W3-DIST:DIST-3 | 2.1(S) | — |
| `A:ENERGY` | S | Bounded signal energy ‖Xθ*‖² ≤ Mn | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8` | B | — | W3-DIST:DIST-1, W3-DIST:DIST-2, SOP:TH09, W3-DIST:DIST-3, W3-DIST:DIST-C, W3-DIST:X, W3-DIST:X', W3-POST:Thm-1 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) 1.3(D) | — |
| `A:FIXED-S0` | S | True model size s₀ ≥ 1 fixed in n; s₀ ≤ K eventually | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | SOP:TH09, W3-POST:Thm-1 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) | — |
| `A:GAUSS-NOISE` | S | Noise N(0, σ²I) independent of the design, σ² fixed (data law; see note †) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:29` | B | — | SOP:TH09, W3-DIST:X, W3-DIST:X', W3-POST:Thm-1 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) 1.3(D) | — |
| `A:MISR-GRC` | S | Contrast-law Gaussian residual U′(y − xβ) ~ N(0, vI) (discharged by W3-DIST:B0 from DIST-A1) | `Theory_work/Wave3/W3-MISR/STATEMENT.md:36-43` | B | — | W3-MISR:R' | 2.1(S) | — |
| `A:P-POLY` | S | Polynomial dimension p ≤ n^A (p ≫ n allowed) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | W3-DIST:DIST-1, W3-DIST:DIST-2, SOP:TH09, W3-DIST:DIST-C, W3-DIST:X, W3-DIST:X', W3-POST:Thm-1 | 1.1(D) 1.2(D) 2.1(S) 3.1(D) 3.6(D) | — |
| `A:SPARSE-EIG` | S | Anchored sparse eigenvalue floors on S₀ ∪ J (bounded \|J\|, and O(log n) \|J\| unnormalised) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8-10` | B | — | SOP:TH09, W3-POST:Thm-1 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:OP` | R | LS0 implementation premises: EX-A, EX-S, SR, GUARD-W, OP-LS0, e4/e4′, complete scans (composite; ↳ below) | `Theory_work/Wave1/W1-PXN/STATEMENT.md:45` | A | see components ↳OP.* | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | see components |
| `P:DERANDOMISE` | R | Fixed-design conclusions with common constants on design events ⇒ joint-law conclusion | `Theory_work/Wave1/W1-GEN/STATEMENT.md:115` | A | proved-and-checked: C-MIS:LemDR "R02 VERIFIED; council R07/R08 PASS" | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | yes (pure probability lemma) |
| `P:LS0-DISCOVERY` | R | Deterministic capped LS0 from the start mode scores S₀ (lattice descent) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:98` | A | proved-and-checked: C-GROW:L1.2 "PROVED-CHECKED" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | yes (deterministic descent on a finite lattice) |
| `P:M5-COMPOSITION` | R | P(output ∩ reported ≠ S₀) ≤ 2E[1−π(S₀)] + D_n; S₀ scored and π(S₀) > ½ ⇒ reported = S₀ | `Theory_work/Wave1/W1-GEN/STATEMENT.md:21` | A | proved-and-checked: SOP:TH05.0 T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (elementary inequality) |
| `P:SCORE-EXP` | R | Uniform expansion of score differences over polynomial families of models | `Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md:30` | A | proved-unchecked (route only): W1-GEN:L1 "PROVED (by this seat, unchecked)"; checked variant C-GROW:L0.1 "PROVED-CHECKED" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (Gaussian/χ² tail + union bound; analytic) |
| `P:START-CENTRE` | R | Start mode equals / sandwiches the reference model | `Theory_work/Wave1/W1-GEN/lemmas/L2_centre.md:12` | A | proved-unchecked (route only): W1-GEN:L2 "PROVED (by this seat, unchecked)" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | no |
| `↳OP.OP-LS0` | R | LS0 executed from the start mode, centre emitted, scans completed on every fit with output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-unchecked: W1-GEN:L5 ([OP] operational closure) "PROVED (by this seat, unchecked)"; centre-emission part inside W3-RM:E4 "PROVED-CHECKED" | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.SR` | R | Stop/return rule: every scored candidate enters the winner comparison; reported HPM = best scored model | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (final-run ledger half): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" (CC2); the stop half rests on GUARD-W (missing) | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.e4` | R | Emitted LS0 centre is a maximiser of the start law γ₀ | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (as replaced in row 3.1): W3-RM:E4 "PROVED-CHECKED" (code level, under ↳E4.H1+, EX-A, ↳E4.H4); still a bare premise on the W1-GEN route | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no |
| `↳OP.EX-S` | R | Fresh independent ideal uniforms (H-U) | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `↳OP.SCANS` | R | Complete scans: no operational interruption of any search | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `A:BLOCK-VIS` | R | Truths visible inside blocks given any ≤15 other columns (no masking) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:92` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:COEF-BOUNDED` | R | True coefficients in [θ_lo, θ_hi] in absolute value, fixed constants | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:11` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | — |
| `A:GRAM-FLOOR-LATTICE` | R | Gram floor φ₀² on Q ∪ {l} for every column l | `Theory_work/Wave1C/C-GROW/STATEMENT.md:91` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:IID-GAUSS-ROWS` | R | Raw rows i.i.d. N(m_n, Σ_n), noise independent of rows | `Theory_work/Wave2/W2-UNI/STATEMENT.md:38` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:LSF` | R | Population sparse floor: φ² on (s₀+j₀)-sets and ψ_n (vanishing slowly) on O(log n)-sets | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:23` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:RELEVANCE-SIZE` | R | Deterministic relevance set Q ⊇ S₀ of bounded / O(log n) / polylog size | `Theory_work/Wave1C/C-GROW/STATEMENT.md:89` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | — |

Count (2.1): AR=9, AS=14, BD=6, BR=6, BS=14, MD=1, MR=2, MS=4

### Row 3.1 — Core 3 — the coded algorithm reports the true model (Thm 6)

Masters (registry `claims.tsv`, status verbatim, council suffix cut at "; council" where marked …):
- `W3-RM2:RM2-R@1.0.3` (ACTIVE; `Theory_work/Wave3/W3-RM2/STATEMENT.md:216-218`): "PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council …"
- `W3-RM:RM-0@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-RM/STATEMENT.md:160-176`): "PROVED-CHECKED"
- `W2-UNI:F-UNI@2.1.0` (ACTIVE; `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:15-21`): "PROVED-CHECKED"

Notes. Every A item of the reported-model clause sits on the three masters (tier D): `A:OP` (RM2-R, RM-0, F-UNI) with
its components, the interface properties P:POST-CONC, P:SAND, P:NA-TL consumed by RM-0, and the delivery clause's
`A:DELIVERY-ALLOC`, `A:MR1-CAP`, P:NO-OUTPUT-ZERO, P:LS0-DISCOVERY (F-UNI). Premise e4 is replaced by `W3-RM:E4`
(hence `↳E4.*`). Tier-S items carried by `W1-GEN:Thm-GEN` arrive through the untyped edges `W2-UNI:F-UNI → C-DLV:Cor-Dp →
W1-GEN:Thm-GEN`; they are hypotheses of the historical GEN route, not of F-UNI (whose (S),(P) interface replaces them;
`L5_delivery.md:15-19`). CAL enters only there (W3-RM uses CAL "only where M5(0) is cited in its D_n form",
`W3-RM/STATEMENT.md:55-58`).

| id | tier | plain statement | source (file:line) | kind | status (A only; registry/statement text verbatim) | carried by | core theorems | Lean target |
|---|---|---|---|---|---|---|---|---|
| `A:BLOCK-LE-16` | D | Method partition is X-measurable with every block of size ≤ B = min(⌊√n⌋, ⌊√p⌋, 16) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:61` | A | missing (partial): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" gives only B ≤ 16 (CC7); "every block ≤ B" has no claim; registry bridge "MISSING" | W3-RM2:RM2-R, W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | yes (packing invariant: complete-linkage cut at B + next-fit packing ⇒ \|C_b\| ≤ B; finite) / code half no |
| `A:MR1-CAP` | D | LS0 move cap = ℓ_n + \|S̃₀\| (merged main 4676af6) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:76` | A | proved-and-checked (code): C-ENG:Impl-GROW-MR1 "DONE (implemented, tested, every production change reviewed; final reviews APPROVE)"; cap line cited in W3-RM:E4 "PROVED-CHECKED" | W2-UNI:F-UNI | 3.1(D) | no (code fact) |
| `A:OP` | D | LS0 implementation premises: EX-A, EX-S, SR, GUARD-W, OP-LS0, e4/e4′, complete scans (composite; ↳ below) | `Theory_work/Wave1/W1-PXN/STATEMENT.md:45` | A | see components ↳OP.* | W3-RM2:RM2-R, W3-RM:RM-0, W2-UNI:F-UNI, W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | see components |
| `P:LS0-DISCOVERY` | D | Deterministic capped LS0 from the start mode scores S₀ (lattice descent) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:98` | A | proved-and-checked: C-GROW:L1.2 "PROVED-CHECKED" | W2-UNI:F-UNI, W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | yes (deterministic descent on a finite lattice) |
| `P:NA-TL` | D | Lattice events: additions from the lattice lose; neighbours missing a truth score lower, w.p. → 1 | `Theory_work/Wave1C/C-GROW/STATEMENT.md:98` | A | proved-and-checked: W3-RM2:NA-W, W3-RM2:TL-F-b "PROVED-CHECKED; council R1, MANIFEST 00bbeab8…" (row 3.1); C-GROW:L2.1 "PROVED-CHECKED" (routes) | W3-RM:RM-0, W2-UNI:F-UNI | 3.1(D) | no |
| `P:NO-OUTPUT-ZERO` | D | With the total fallback, P(no output) = 0 for all n ≥ 3 | `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:79` | A | proved-and-checked: C-DLV:Prop-F "PROVED-CHECKED for the patched calibration law (R04; council round 2)" | W2-UNI:F-UNI | 3.1(D) | no |
| `P:POST-CONC` | D | Posterior concentration 1 − π(S₀\|y) = O_P(√(log n/n)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:13` | A | proved-and-checked: SOP:TH09 "PROVED-CHECKED (T03♯ only: …)" (fixed design); W2-APP:POST "PROVED-CHECKED" (Gaussian rows) | W3-RM:RM-0, W2-UNI:F-UNI, W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | no |
| `P:SAND` | D | Start-law maximisers sandwiched: S₀ ⊆ S̃ ⊆ Q for every maximiser, w.p. → 1 | `Theory_work/Wave1C/C-GROW/STATEMENT.md:103` | A | proved-and-checked: W3-RM2:SAND-R-b "PROVED-CHECKED; council R1, MANIFEST 00bbeab8…" (row 3.1); C-GROW:L3 "PROVED-CHECKED" (routes) | W3-RM:RM-0, W2-UNI:F-UNI | 3.1(D) | no |
| `↳DLV.FALLBACK` | D | Total tier-1 fallback with complete fallback-grid freezing ⇒ P(no output) = 0 | `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:8-10` | A | proved-and-checked: C-DLV:Prop-F "PROVED-CHECKED for the patched calibration law (R04; council round 2)"; implementation C-ENG:Impl-DLV-B "DONE (implemented, tested, every production change reviewed; final reviews APPROVE)" | ↳ of A:DELIVERY-ALLOC | 3.1(D) | no |
| `↳DLV.P1-S3` | D | Code inventory P1 and degenerate-case S.3 hold for the code of record | `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:12-13` | A | proved-unchecked: C-DLV:P1-Inventory "AUDITED (code reading)"; C-DLV:L2-S3 "AUDITED (code reading)" | ↳ of A:DELIVERY-ALLOC | 3.1(D) | no (code fact) |
| `↳DLV.TDP-IMPL` | D | e4 tie-aware fallback implemented as W1-N3's TDP with the stated operation/storage bounds | `Theory_work/Wave1C/C-DLV/STATEMENT.md:38` | A | proved-unchecked: C-ENG:TDP_E "PROVED (by this seat, unchecked)" | ↳ of A:DELIVERY-ALLOC | 3.1(D) | yes (DP returns the lex-min maximiser of a block-separable score under a size cap; finite) |
| `↳OP.GUARD-W` | D | Stop-only guard: reads only the clock, consumes no uniform, changes no setting; a stop returns no output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | missing: "audit open, not discharged here" (W1-N1/STATEMENT.md:86-88); W3-SAMP/STATEMENT.md §3 "The full GUARD-W delivery audit" not claimed | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) 3.5(D) | no (code fact) |
| `↳OP.OP-LS0` | D | LS0 executed from the start mode, centre emitted, scans completed on every fit with output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-unchecked: W1-GEN:L5 ([OP] operational closure) "PROVED (by this seat, unchecked)"; centre-emission part inside W3-RM:E4 "PROVED-CHECKED" | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.SR` | D | Stop/return rule: every scored candidate enters the winner comparison; reported HPM = best scored model | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (final-run ledger half): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" (CC2); the stop half rests on GUARD-W (missing) | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.e4` | D | Emitted LS0 centre is a maximiser of the start law γ₀ | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (as replaced in row 3.1): W3-RM:E4 "PROVED-CHECKED" (code level, under ↳E4.H1+, EX-A, ↳E4.H4); still a bare premise on the W1-GEN route | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no |
| `A:DELIVERY-ALLOC` | D | Delivery premises + declared allocation of Prop F (composite; components ↳ below) | `Theory_work/Wave2/W2-FAC-A/STATEMENT.md:128` | M | — | W2-UNI:F-UNI | 3.1(D) | — |
| `A:IDEAL-W+` | D | Idealised machine (IDEAL-W) with the two shipped LS0 cap ceilings lifted | `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:19` | M | — | W2-UNI:F-UNI | 3.1(D) | — |
| `↳DLV.CONFIG` | D | Covered configuration: core + LS0 + e4 fallback, default summaries, fixed workers | `Theory_work/Wave1C/C-DLV/STATEMENT.md:32` | M | — | ↳ of A:DELIVERY-ALLOC | 3.1(D) | — |
| `↳DLV.EXA-COST` | D | EX-A as a unit-cost model for exact real arithmetic | `Theory_work/Wave1C/C-DLV/STATEMENT.md:26` | M | — | ↳ of A:DELIVERY-ALLOC | 3.1(D) | — |
| `↳DLV.IDEAL-W` | D | No integer/index/allocation overflow (unbounded-word machine) | `Theory_work/Wave1C/C-DLV/STATEMENT.md:24` | M | — | ↳ of A:DELIVERY-ALLOC | 3.1(D) | — |
| `↳DLV.MACH` | D | Wall time and memory proportional to counts; allocations succeed; no crash/interruption | `Theory_work/Wave1C/C-DLV/STATEMENT.md:28` | M | — | ↳ of A:DELIVERY-ALLOC | 3.1(D) | — |
| `↳DLV.SEED-ALLOC` | D | Valid seed in [1, 2³¹−1] and declared mem/time ≥ the polynomial envelopes (A1, A4 preflight) | `Theory_work/Wave1C/C-DLV/STATEMENT.md:43-45` | M | — | ↳ of A:DELIVERY-ALLOC | 3.1(D) | — |
| `↳OP.EX-S` | D | Fresh independent ideal uniforms (H-U) | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `↳OP.SCANS` | D | Complete scans: no operational interruption of any search | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `A:GRAM-OP-BOUND` | D | Sample Gram within δ_n of population Gram in operator norm, δ_n√(p log log n) → 0 | `Theory_work/Wave2/W2-FAC-A/STATEMENT.md:90` | B | — | W2-UNI:F-UNI | 3.1(D) | — |
| `A:IID-GAUSS-ROWS` | D | Raw rows i.i.d. N(m_n, Σ_n), noise independent of rows | `Theory_work/Wave2/W2-UNI/STATEMENT.md:38` | B | — | W3-RM2:RM2-R, W2-UNI:F-UNI, W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:LSF` | D | Population sparse floor: φ² on (s₀+j₀)-sets and ψ_n (vanishing slowly) on O(log n)-sets | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:23` | B | — | W3-RM2:RM2-R, W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:P-POLY` | D | Polynomial dimension p ≤ n^A (p ≫ n allowed) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | W2-UNI:F-UNI, W2-APP:POST, SOP:TH09, W1-GEN:Thm-GEN | 1.1(D) 1.2(D) 2.1(S) 3.1(D) 3.6(D) | — |
| `A:PTV` | D | Population visibility: \|partial cov of each truth with the signal given ≤15 columns\| ≥ a₀ | `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:28` | B | — | W3-RM2:RM2-R | 3.1(D) | — |
| `A:RELEVANCE-SIZE` | D | Deterministic relevance set Q ⊇ S₀ of bounded / O(log n) / polylog size | `Theory_work/Wave1C/C-GROW/STATEMENT.md:89` | B | — | W2-UNI:F-UNI, W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | — |
| `A:RM-FLR` | D | Population floor c on sets of size ≤ 16+s₀ and on Q ∪ {l} | `Theory_work/Wave3/W3-RM/STATEMENT.md:134` | B | — | W3-RM2:RM2-R | 3.1(D) | — |
| `A:RM2-HSIZE-RHO` | D | Reference neighbourhoods \|H_l\| ≤ n^ρ with 15ρ + b < ½ | `Theory_work/Wave3/W3-RM2/STATEMENT.md:182-184` | B | — | W3-RM2:RM2-R | 3.1(D) | — |
| `A:RM2-LFEAS` | D | (L-feas) with leakage set \|Q\| ≤ n^b | `Theory_work/Wave3/W3-RM2/STATEMENT.md:176-177` | B | — | W3-RM2:RM2-R | 3.1(D) | — |
| `A:RM2-LGAIN-R` | D | Leak bound: \|Cov(W_l, W_j \| W_U)\| ≤ ϖ_n = o(√(log n/n)) for l ∉ Q | `Theory_work/Wave3/W3-RM2/STATEMENT.md:176-181` | B | — | W3-RM2:RM2-R | 3.1(D) | — |
| `A:RM2-LLOC-R` | D | Localisation: conditional covariances with columns outside H_l at most r_n → 0 | `Theory_work/Wave3/W3-RM2/STATEMENT.md:182-184` | B | — | W3-RM2:RM2-R | 3.1(D) | — |
| `A:RM2-LSIZE-B-R` | D | Leakage set size \|Q\| ≤ n^b, b < ½ | `Theory_work/Wave3/W3-RM2/STATEMENT.md:176-177` | B | — | W3-RM2:RM2-R | 3.1(D) | — |
| `A:RM2-W-R` | D | Lattice width on the realised design: deterministic t_n → ∞ with P(𝒲⁰_n ∩ {𝔴⁰_n ≤ −t_n}) → 1 | `Theory_work/Wave3/W3-RM2/STATEMENT.md:194-197` | B | — | W3-RM2:RM2-R | 3.1(D) | — |
| `A:CAL` | S | Calibration record 𝓒 is a function of the data and streams 0–9 only (frozen before the final run) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:42` | A | missing: named premise (W1-N1/STATEMENT.md:79; W3-SAMP/STATEMENT.md:64-65); no code-reading claim in the closure | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(S) 3.1(S) 3.6(D) 3.5(D) | no (code fact) |
| `P:DERANDOMISE` | S | Fixed-design conclusions with common constants on design events ⇒ joint-law conclusion | `Theory_work/Wave1/W1-GEN/STATEMENT.md:115` | A | proved-and-checked: C-MIS:LemDR "R02 VERIFIED; council R07/R08 PASS" | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | yes (pure probability lemma) |
| `P:M5-COMPOSITION` | S | P(output ∩ reported ≠ S₀) ≤ 2E[1−π(S₀)] + D_n; S₀ scored and π(S₀) > ½ ⇒ reported = S₀ | `Theory_work/Wave1/W1-GEN/STATEMENT.md:21` | A | proved-and-checked: SOP:TH05.0 T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (elementary inequality) |
| `P:SCORE-EXP` | S | Uniform expansion of score differences over polynomial families of models | `Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md:30` | A | proved-unchecked (route only): W1-GEN:L1 "PROVED (by this seat, unchecked)"; checked variant C-GROW:L0.1 "PROVED-CHECKED" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (Gaussian/χ² tail + union bound; analytic) |
| `P:START-CENTRE` | S | Start mode equals / sandwiches the reference model | `Theory_work/Wave1/W1-GEN/lemmas/L2_centre.md:12` | A | proved-unchecked (route only): W1-GEN:L2 "PROVED (by this seat, unchecked)" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | no |
| `↳E4.H1+` | S | start_mode input encodes the ordered partition, block tables, prior and K; blk/pos are inverse maps | `Theory_work/Wave3/W3-RM/STATEMENT.md:220-222` | A | proved-unchecked: code-reading remark inside W1-N3 (H1) (W1-N3/STATEMENT.md:92-98, part of W1-N3:Thm-N3-code(a-d) "PROVED; XF-checked"); the inverse-map strengthening cites C-ENG:TDP_E "PROVED (by this seat, unchecked)" | W3-RM:E4 (statement text) | 3.1(S) | no (code fact) |
| `A:EX-A` | S | Exact scores and arithmetic (named idealisation; no numerical margin) | `Theory_work/Wave1/W1-N1/STATEMENT.md:70` | M | — | W3-RM:E4 (H2) | 2.1(D) 3.1(S) 3.6(D) | — |
| `↳E4.H4` | S | Execution bounds for start_mode: integer counters fit, allocations succeed | `Theory_work/Wave1/W1-N3/STATEMENT.md:106` | M | — | W3-RM:E4 (statement text) | 3.1(S) | — |
| `A:BETAMIN` | S | Beta-min: smallest true coefficient ≫ √(log n / n) (BM-inf) or above a constant multiple (BM(c)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:11` | B | — | SOP:TH09, W1-GEN:Thm-GEN | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:BLOCK-VIS` | S | Truths visible inside blocks given any ≤15 other columns (no masking) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:92` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:COEF-BOUNDED` | S | True coefficients in [θ_lo, θ_hi] in absolute value, fixed constants | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:11` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | — |
| `A:ENERGY` | S | Bounded signal energy ‖Xθ*‖² ≤ Mn | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8` | B | — | SOP:TH09, W1-GEN:Thm-GEN | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) 1.3(D) | — |
| `A:FIXED-S0` | S | True model size s₀ ≥ 1 fixed in n; s₀ ≤ K eventually | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | W2-APP:POST, SOP:TH09, W1-GEN:Thm-GEN | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) | — |
| `A:GAUSS-NOISE` | S | Noise N(0, σ²I) independent of the design, σ² fixed (data law; see note †) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:29` | B | — | W2-APP:POST, SOP:TH09, W1-GEN:Thm-GEN | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) 1.3(D) | — |
| `A:GRAM-FLOOR-LATTICE` | S | Gram floor φ₀² on Q ∪ {l} for every column l | `Theory_work/Wave1C/C-GROW/STATEMENT.md:91` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:SPARSE-EIG` | S | Anchored sparse eigenvalue floors on S₀ ∪ J (bounded \|J\|, and O(log n) \|J\| unnormalised) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8-10` | B | — | SOP:TH09, W1-GEN:Thm-GEN | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:EXACT-GRAM` | R | Sample Gram equals population Gram exactly (p ≤ n−1) | `Theory_work/Wave2/W2-FAC-A/STATEMENT.md:90` | B | — | W2-FAC-A:Prop-F-FAC | 3.1(R) | — |
| `A:INST-FACTOR` | R | One-factor Gram with bounded exposure ratio κ ≤ κ̄ | `Theory_work/Wave2/W2-FAC-A/STATEMENT.md:62` | B | — | W2-FAC-A:Prop-F-FAC | 3.1(R) | — |
| `A:P-ALPHA0` | R | Growth limsup log p / log n < α₀(κ̄) = 1/(2κ̄(κ̄+2)) | `Theory_work/Wave2/W2-FAC-A/STATEMENT.md:92` | B | — | W2-FAC-A:Prop-F-FAC | 3.1(R) | — |

Count (3.1): AD=15, AS=6, BD=13, BR=3, BS=8, MD=9, MS=2

### Row 3.6 — Core 4 — the run's estimates are consistent (Thm 10)

Masters (registry `claims.tsv`, status verbatim, council suffix cut at "; council" where marked …):
- `W3-SAMP:C@1.1.4` (ACTIVE; `Theory_work/Wave3/W3-SAMP/STATEMENT.md:149-163`): "PROVED-CHECKED"
- `W3-SAMP:TR@2.1.4` (ACTIVE; `Theory_work/Wave3/W3-SAMP/STATEMENT.md:165-177`): "PROVED-CHECKED"
- `W3-SAMP:LT#@2.0.4` (ACTIVE; `Theory_work/Wave3/W3-SAMP/STATEMENT.md:126-140`): "PROVED-CHECKED"
- `W3-SAMP:D@2.1.4` (ACTIVE; `Theory_work/Wave3/W3-SAMP/STATEMENT.md:97-105`): "PROVED-CHECKED"
- `W3-START2:IF-START@1.1.0` (SUPERSEDED-VALID; `Theory_work/Wave3/W3-START2/STATEMENT.md:176-180`): "PROVED-CHECKED"
- `W2-APP:POST@1.0.7` (ACTIVE; `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:27-33`): "PROVED-CHECKED"

Notes. Thm 10 (card row 3.6) is `W3-SAMP:C` clause (C-v) + start input `W3-START2:IF-START` + posterior input
`W2-APP:POST` (`READER_VERSIONS.md` §10 "Master theorem"). C-v needs only P-CONC and P-START, and **itself proves NC_r**
and the HPM clause; `W3-SAMP:TR` (P-OVL-INF) is the remark's alternative route, `W3-SAMP:D` (P-MAP, P-OVL, IND-T) and
`W3-SAMP:LT#` (NC-R) are listed as masters by the card but are not needed on the C-v route. **Tier exception:** Thm 10
is the Gaussian-rows case, so the start premises it actually uses are `A:START-R-FL`, `A:START-R-V`, `A:START2-R-L`
(Thm 10 (A3)–(A5); `READER_VERSIONS.md` §10), which sit behind the `@proof` edge `W3-START2:IF-START → W3-START2:START-R`
and therefore show as tier R; the tier-D START-E/GF/V/AL are IF-START's fixed-design branch.

| id | tier | plain statement | source (file:line) | kind | status (A only; registry/statement text verbatim) | carried by | core theorems | Lean target |
|---|---|---|---|---|---|---|---|---|
| `A:BLOCK-LE-16` | D | Method partition is X-measurable with every block of size ≤ B = min(⌊√n⌋, ⌊√p⌋, 16) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:61` | A | missing (partial): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" gives only B ≤ 16 (CC7); "every block ≤ B" has no claim; registry bridge "MISSING" | W3-SAMP:LT#, W3-START2:IF-START | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | yes (packing invariant: complete-linkage cut at B + next-fit packing ⇒ \|C_b\| ≤ B; finite) / code half no |
| `A:CAL` | D | Calibration record 𝓒 is a function of the data and streams 0–9 only (frozen before the final run) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:42` | A | missing: named premise (W1-N1/STATEMENT.md:79; W3-SAMP/STATEMENT.md:64-65); no code-reading claim in the closure | W3-SAMP:C, W3-SAMP:TR, W3-SAMP:LT#, W3-SAMP:D | 1.1(R) 1.2(R) 2.1(S) 3.1(S) 3.6(D) 3.5(D) | no (code fact) |
| `A:N1-KERNEL` | D | Sampler contract: START, KERNEL, MEAS, SI, potential run, worker equivalence (composite; ↳ below) | `Theory_work/Wave1/W1-N1/STATEMENT.md:68` | A | see components ↳N1.* | W3-SAMP:C, W3-SAMP:TR, W3-SAMP:LT#, W3-SAMP:D | 2.1(S) 3.6(D) 3.5(D) | see components |
| `A:NC-R` | D | Non-collapse: lim_{η↓0} limsup_n P(𝒜 ∩ {W_r < η}) = 0 (particle weights) | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:84` | A | proved-and-checked (on the C-v route): W3-SAMP:C "PROVED-CHECKED" (C-v: "and NC_r holds") | W3-SAMP:LT# | 2.1(S) 3.6(D) | no |
| `A:P-MAP` | D | The F-maximiser over Ω equals S₀ w.p. → 1 (implied by posterior concentration) | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:78` | A | proved-and-checked: via P:POST-CONC + C-PACK:SL0 "PROVED-CHECKED" (HPM exact for δ < ½) | W3-SAMP:D | 2.1(S) 3.6(D) | yes (SL0 part: deterministic δ < ½ ⇒ argmax = S₀) |
| `A:P-OVL` | D | Computational overlap: D_r·π₀(S₀) → ∞ in probability on 𝒜 | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:82` | A | missing (one line): W3-SAMP:D "PROVED-CHECKED" (D-iv production corollary) reduces it to max(n,p)·log₂(n+1)·π₀(S₀) → ∞, which P-START gives; that implication is not registered | W3-SAMP:D | 2.1(S) 3.6(D) | yes (trivial real-analysis step) |
| `A:P-OVL-INF` | D | Global overlap: L / max_S π(S)/π₀(S) → ∞ on 𝒜 (Theorem TR only) | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:79` | A | missing: W3-SAMP/STATEMENT.md §3 "That NC_r, P-OVL or P-OVL∞ follows from primitive conditions on (X, θ*)" is not claimed | W3-SAMP:TR | 2.1(S) 3.6(D) | no |
| `A:P-START` | D | Start law concentrates: 1_𝒜(1−π₀(S₀))/π₀(S₀) → 0 in probability | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:76` | A | proved-and-checked: W3-START2:IF-START "PROVED-CHECKED" (state SUPERSEDED-VALID; successor W3-START2-R:IF-START "PROVED-CHECKED; council R2, MANIFEST 12bb52cd…, sol=9.0 PASS, opus=9.3 PASS") | W3-SAMP:C | 2.1(S) 3.6(D) | no |
| `P:DERANDOMISE` | D | Fixed-design conclusions with common constants on design events ⇒ joint-law conclusion | `Theory_work/Wave1/W1-GEN/STATEMENT.md:115` | A | proved-and-checked: C-MIS:LemDR "R02 VERIFIED; council R07/R08 PASS" | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | yes (pure probability lemma) |
| `P:POST-CONC` | D | Posterior concentration 1 − π(S₀\|y) = O_P(√(log n/n)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:13` | A | proved-and-checked: SOP:TH09 "PROVED-CHECKED (T03♯ only: …)" (fixed design); W2-APP:POST "PROVED-CHECKED" (Gaussian rows) | W3-SAMP:C, W3-SAMP:TR, W3-SAMP:LT#, W3-SAMP:D | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) | no |
| `↳N1.KERNEL` | D | Coded step functions + random order realise the T12 kernels (π-invariant), order uniform and state-independent | `Theory_work/Wave1/W1-N1/STATEMENT.md:76` | A | proved-unchecked*: "PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT" (W1-N1/STATEMENT.md:76-78; no registry claim) — * an inherited check exists; Fable to rule | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | yes (math half: each coded move kernel is π-reversible on the finite Ω; code half no) |
| `↳N1.MEAS` | D | Realisation map (calibration, stream) → island record is jointly measurable | `Theory_work/Wave1/W1-N1/STATEMENT.md:83` | A | proved-and-checked: W1-N1:B "PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08." | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | no |
| `↳N1.POT` | D | Statements are about the potential (uninterrupted) run; identified with printed fields on completed runs | `Theory_work/Wave1/W1-N1/STATEMENT.md:86` | A | proved-and-checked for the completed-run identification: W3-SAMP:PC "PROVED-CHECKED" ("a limited comparison, not the full GUARD-W audit"); the GUARD-W half is missing (row ↳OP.GUARD-W) | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | no |
| `↳N1.START` | D | Coded start sampler draws exactly from π₀ and reports Z̄₀ = Σ_Ω γ₀ | `Theory_work/Wave1/W1-N1/STATEMENT.md:75` | A | proved-unchecked: N9 Claims S, Z "PROVED (candidate)" (W1-N1/STATEMENT.md:75; no registry claim) | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | yes (algorithm-level: block sampler is exact for the product-form π₀ under the size cap; finite) |
| `↳OP.GUARD-W` | D | Stop-only guard: reads only the clock, consumes no uniform, changes no setting; a stop returns no output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | missing: "audit open, not discharged here" (W1-N1/STATEMENT.md:86-88); W3-SAMP/STATEMENT.md §3 "The full GUARD-W delivery audit" not claimed | ↳ of A:N1-KERNEL | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) 3.5(D) | no (code fact) |
| `A:EX-A` | D | Exact scores and arithmetic (named idealisation; no numerical margin) | `Theory_work/Wave1/W1-N1/STATEMENT.md:70` | M | — | W3-START2:IF-START | 2.1(D) 3.1(S) 3.6(D) | — |
| `A:EX-A-HU` | D | EX-A plus ideal i.i.d. U[0,1) uniforms within each stream (H-U) | `Theory_work/Wave1/W1-N1/STATEMENT.md:70-71` | M | — | W3-SAMP:C, W3-SAMP:TR, W3-SAMP:LT#, W3-SAMP:D | 2.1(S) 3.6(D) 3.5(D) | — |
| `A:IND-T` | D | Final streams 10–13 mutually independent and independent of streams 0–9 (D-ii only) | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:65` | M | — | W3-SAMP:D | 2.1(S) 3.6(D) | — |
| `↳N1.SI` | D | Final stream 9+r independent of streams 0–9 (single-island; RNG idealisation) | `Theory_work/Wave1/W1-N1/STATEMENT.md:80` | M | — | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | — |
| `↳N1.WORKER` | D | Worker equivalence for concurrent islands (v3.1 only; frozen core is serial) | `Theory_work/Wave1/W1-N1/STATEMENT.md:89` | M | — | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | — |
| `A:COEF-BOUNDED` | D | True coefficients in [θ_lo, θ_hi] in absolute value, fixed constants | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:11` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(S) 3.6(D) | — |
| `A:FIXED-S0` | D | True model size s₀ ≥ 1 fixed in n; s₀ ≤ K eventually | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | W2-APP:POST, W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) | — |
| `A:GAUSS-NOISE` | D | Noise N(0, σ²I) independent of the design, σ² fixed (data law; see note †) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:29` | B | — | W2-APP:POST, W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) 1.3(D) | — |
| `A:IID-GAUSS-ROWS` | D | Raw rows i.i.d. N(m_n, Σ_n), noise independent of rows | `Theory_work/Wave2/W2-UNI/STATEMENT.md:38` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:LSF` | D | Population sparse floor: φ² on (s₀+j₀)-sets and ψ_n (vanishing slowly) on O(log n)-sets | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:23` | B | — | W2-APP:POST | 1.1(R) 1.2(D) 2.1(R) 3.1(D) 3.6(D) | — |
| `A:P-POLY` | D | Polynomial dimension p ≤ n^A (p ≫ n allowed) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6` | B | — | W2-APP:POST, W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(D) 3.6(D) | — |
| `A:START-AL` | D | Averaged leakage with a level vector: tail budget and ρ_n(Q;h) → 0 | `Theory_work/Wave3/W3-START/STATEMENT.md:152` | B | — | W3-START2:IF-START | 3.6(D) | — |
| `A:START-E` | D | Energy bound + p ≤ n^A, s₀ fixed, p > s₀ | `Theory_work/Wave3/W3-START/STATEMENT.md:135` | B | — | W3-START2:IF-START | 3.6(D) | — |
| `A:START-GF` | D | Unnormalised Gram floor g_* on all sets of size 1–16 | `Theory_work/Wave3/W3-START/STATEMENT.md:136` | B | — | W3-START2:IF-START | 3.6(D) | — |
| `A:START-V` | D | Visibility of the truths, constant level (V-c) or margin form (V-m) | `Theory_work/Wave3/W3-START/STATEMENT.md:140` | B | — | W3-START2:IF-START | 3.6(D) | — |
| `A:BETAMIN` | S | Beta-min: smallest true coefficient ≫ √(log n / n) (BM-inf) or above a constant multiple (BM(c)) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:11` | B | — | W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:ENERGY` | S | Bounded signal energy ‖Xθ*‖² ≤ Mn | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8` | B | — | W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) 1.3(D) | — |
| `A:SPARSE-EIG` | S | Anchored sparse eigenvalue floors on S₀ ∪ J (bounded \|J\|, and O(log n) \|J\| unnormalised) | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8-10` | B | — | W3-POST:Thm-1, SOP:TH09 | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) | — |
| `A:OP` | R | LS0 implementation premises: EX-A, EX-S, SR, GUARD-W, OP-LS0, e4/e4′, complete scans (composite; ↳ below) | `Theory_work/Wave1/W1-PXN/STATEMENT.md:45` | A | see components ↳OP.* | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | see components |
| `P:LS0-DISCOVERY` | R | Deterministic capped LS0 from the start mode scores S₀ (lattice descent) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:98` | A | proved-and-checked: C-GROW:L1.2 "PROVED-CHECKED" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | yes (deterministic descent on a finite lattice) |
| `P:M5-COMPOSITION` | R | P(output ∩ reported ≠ S₀) ≤ 2E[1−π(S₀)] + D_n; S₀ scored and π(S₀) > ½ ⇒ reported = S₀ | `Theory_work/Wave1/W1-GEN/STATEMENT.md:21` | A | proved-and-checked: SOP:TH05.0 T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (elementary inequality) |
| `P:SCORE-EXP` | R | Uniform expansion of score differences over polynomial families of models | `Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md:30` | A | proved-unchecked (route only): W1-GEN:L1 "PROVED (by this seat, unchecked)"; checked variant C-GROW:L0.1 "PROVED-CHECKED" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | yes (Gaussian/χ² tail + union bound; analytic) |
| `P:START-CENTRE` | R | Start mode equals / sandwiches the reference model | `Theory_work/Wave1/W1-GEN/lemmas/L2_centre.md:12` | A | proved-unchecked (route only): W1-GEN:L2 "PROVED (by this seat, unchecked)" | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | no |
| `↳OP.OP-LS0` | R | LS0 executed from the start mode, centre emitted, scans completed on every fit with output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-unchecked: W1-GEN:L5 ([OP] operational closure) "PROVED (by this seat, unchecked)"; centre-emission part inside W3-RM:E4 "PROVED-CHECKED" | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.SR` | R | Stop/return rule: every scored candidate enters the winner comparison; reported HPM = best scored model | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (final-run ledger half): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" (CC2); the stop half rests on GUARD-W (missing) | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.e4` | R | Emitted LS0 centre is a maximiser of the start law γ₀ | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (as replaced in row 3.1): W3-RM:E4 "PROVED-CHECKED" (code level, under ↳E4.H1+, EX-A, ↳E4.H4); still a bare premise on the W1-GEN route | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no |
| `↳OP.EX-S` | R | Fresh independent ideal uniforms (H-U) | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `↳OP.SCANS` | R | Complete scans: no operational interruption of any search | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `A:BLOCK-VIS` | R | Truths visible inside blocks given any ≤15 other columns (no masking) | `Theory_work/Wave1C/C-GROW/STATEMENT.md:92` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:GRAM-FLOOR-LATTICE` | R | Gram floor φ₀² on Q ∪ {l} for every column l | `Theory_work/Wave1C/C-GROW/STATEMENT.md:91` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(S) 3.6(R) | — |
| `A:RELEVANCE-SIZE` | R | Deterministic relevance set Q ⊇ S₀ of bounded / O(log n) / polylog size | `Theory_work/Wave1C/C-GROW/STATEMENT.md:89` | B | — | W1-GEN:Thm-GEN | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) | — |
| `A:START-R-FL` | R | Population floor c_Σ on principal submatrices of size ≤ 16+s₀ | `Theory_work/Wave3/W3-START/STATEMENT.md:160` | B | — | W3-START2:START-R, W3-START2:BR, W3-START:START-R, W3-START:BR | 3.6(R) | — |
| `A:START-R-L` | R | Localised bounded population leakage (polylog Q, H_l) | `Theory_work/Wave3/W3-START/STATEMENT.md:163` | B | — | W3-START:START-R, W3-START:BR | 3.6(R) | — |
| `A:START-R-V` | R | Population visibility PTV(a_V) given any 15 other columns | `Theory_work/Wave3/W3-START/STATEMENT.md:162` | B | — | W3-START2:START-R, W3-START2:BR, W3-START:START-R, W3-START:BR | 3.6(R) | — |
| `A:START2-R-L` | R | Localised bounded leakage, leakage set of any size ≤ K (H_l polylog) | `Theory_work/Wave3/W3-START2/STATEMENT.md:63-73` | B | — | W3-START2:START-R, W3-START2:BR | 3.6(R) | — |

Count (3.6): AD=15, AR=8, BD=10, BR=7, BS=3, MD=5, MR=2

### Row 3.5 — Core 4 — the evidence estimate is unbiased (row 3.5)

Masters (registry `claims.tsv`, status verbatim, council suffix cut at "; council" where marked …):
- `W1-N1:Thm-N1@1.0.0` (ACTIVE; `Theory_work/Wave1/W1-N1/STATEMENT.md:98-104`): "PROVED-CHECKED"
- `W3-READER:PoolZ` (not in this worktree's `claims.tsv`; `W3-READER` worktree `Theory_work/Wave3/W3-READER/STATEMENT.md:12-13`): "PROVED (by this seat, unchecked)"

Notes. Row 3.5 = `W1-N1:Thm-N1` (+ `W3-READER:PoolZ`, linearity over the four islands). Design-free: no B item.

| id | tier | plain statement | source (file:line) | kind | status (A only; registry/statement text verbatim) | carried by | core theorems | Lean target |
|---|---|---|---|---|---|---|---|---|
| `A:CAL` | D | Calibration record 𝓒 is a function of the data and streams 0–9 only (frozen before the final run) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:42` | A | missing: named premise (W1-N1/STATEMENT.md:79; W3-SAMP/STATEMENT.md:64-65); no code-reading claim in the closure | W1-N1:Thm-N1 (STATEMENT.md:79; not in its registry row), W3-READER:PoolZ (not in registry) | 1.1(R) 1.2(R) 2.1(S) 3.1(S) 3.6(D) 3.5(D) | no (code fact) |
| `A:N1-KERNEL` | D | Sampler contract: START, KERNEL, MEAS, SI, potential run, worker equivalence (composite; ↳ below) | `Theory_work/Wave1/W1-N1/STATEMENT.md:68` | A | see components ↳N1.* | W1-N1:Thm-N1 | 2.1(S) 3.6(D) 3.5(D) | see components |
| `A:OP` | D | LS0 implementation premises: EX-A, EX-S, SR, GUARD-W, OP-LS0, e4/e4′, complete scans (composite; ↳ below) | `Theory_work/Wave1/W1-PXN/STATEMENT.md:45` | A | see components ↳OP.* | W1-N1:Thm-N1 | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | see components |
| `↳N1.KERNEL` | D | Coded step functions + random order realise the T12 kernels (π-invariant), order uniform and state-independent | `Theory_work/Wave1/W1-N1/STATEMENT.md:76` | A | proved-unchecked*: "PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT" (W1-N1/STATEMENT.md:76-78; no registry claim) — * an inherited check exists; Fable to rule | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | yes (math half: each coded move kernel is π-reversible on the finite Ω; code half no) |
| `↳N1.MEAS` | D | Realisation map (calibration, stream) → island record is jointly measurable | `Theory_work/Wave1/W1-N1/STATEMENT.md:83` | A | proved-and-checked: W1-N1:B "PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08." | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | no |
| `↳N1.POT` | D | Statements are about the potential (uninterrupted) run; identified with printed fields on completed runs | `Theory_work/Wave1/W1-N1/STATEMENT.md:86` | A | proved-and-checked for the completed-run identification: W3-SAMP:PC "PROVED-CHECKED" ("a limited comparison, not the full GUARD-W audit"); the GUARD-W half is missing (row ↳OP.GUARD-W) | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | no |
| `↳N1.START` | D | Coded start sampler draws exactly from π₀ and reports Z̄₀ = Σ_Ω γ₀ | `Theory_work/Wave1/W1-N1/STATEMENT.md:75` | A | proved-unchecked: N9 Claims S, Z "PROVED (candidate)" (W1-N1/STATEMENT.md:75; no registry claim) | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | yes (algorithm-level: block sampler is exact for the product-form π₀ under the size cap; finite) |
| `↳OP.GUARD-W` | D | Stop-only guard: reads only the clock, consumes no uniform, changes no setting; a stop returns no output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | missing: "audit open, not discharged here" (W1-N1/STATEMENT.md:86-88); W3-SAMP/STATEMENT.md §3 "The full GUARD-W delivery audit" not claimed | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(S) 3.1(D) 3.6(D) 3.5(D) | no (code fact) |
| `↳OP.OP-LS0` | D | LS0 executed from the start mode, centre emitted, scans completed on every fit with output | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-unchecked: W1-GEN:L5 ([OP] operational closure) "PROVED (by this seat, unchecked)"; centre-emission part inside W3-RM:E4 "PROVED-CHECKED" | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.SR` | D | Stop/return rule: every scored candidate enters the winner comparison; reported HPM = best scored model | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (final-run ledger half): W3-SAMP:CC "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" (CC2); the stop half rests on GUARD-W (missing) | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no (code fact) |
| `↳OP.e4` | D | Emitted LS0 centre is a maximiser of the start law γ₀ | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | A | proved-and-checked (as replaced in row 3.1): W3-RM:E4 "PROVED-CHECKED" (code level, under ↳E4.H1+, EX-A, ↳E4.H4); still a bare premise on the W1-GEN route | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | no |
| `A:EX-A-HU` | D | EX-A plus ideal i.i.d. U[0,1) uniforms within each stream (H-U) | `Theory_work/Wave1/W1-N1/STATEMENT.md:70-71` | M | — | W1-N1:Thm-N1 (STATEMENT.md:70-71; not in its registry row), W3-READER:PoolZ | 2.1(S) 3.6(D) 3.5(D) | — |
| `↳N1.SI` | D | Final stream 9+r independent of streams 0–9 (single-island; RNG idealisation) | `Theory_work/Wave1/W1-N1/STATEMENT.md:80` | M | — | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | — |
| `↳N1.WORKER` | D | Worker equivalence for concurrent islands (v3.1 only; frozen core is serial) | `Theory_work/Wave1/W1-N1/STATEMENT.md:89` | M | — | ↳ of A:N1-KERNEL | 2.1(S) 3.6(D) 3.5(D) | — |
| `↳OP.EX-S` | D | Fresh independent ideal uniforms (H-U) | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |
| `↳OP.SCANS` | D | Complete scans: no operational interruption of any search | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86` | M | — | ↳ of A:OP | 1.1(R) 1.2(R) 2.1(R) 3.1(D) 3.6(R) 3.5(D) | — |

Count (3.5): AD=11, MD=5

### Row 1.3 — Core 5 — the rate cannot be improved (Thm 3)

Masters (registry `claims.tsv`, status verbatim, council suffix cut at "; council" where marked …):
- `W3-PSHARP:A@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:46-77`): "PROVED-CHECKED; council …"
- `W3-PSHARP:B@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:90-114`): "PROVED-CHECKED; council …"
- `W3-PSHARP-R:AE@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:61-92`): "PROVED-CHECKED; council …"
- `W3-PSHARP-R:A2C@1.0.0` (ACTIVE; `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:94-100`): "PROVED-CHECKED; council …"

Notes. Lower bounds: the B items define the witness designs on which the bound is exhibited (they restrict where the
bound is shown, not where it is valid); `W3-PSHARP:B` (every design, order n^{-1/2}) has no assumption. No A or M item.

| id | tier | plain statement | source (file:line) | kind | status (A only; registry/statement text verbatim) | carried by | core theorems | Lean target |
|---|---|---|---|---|---|---|---|---|
| `A:ENERGY` | D | Bounded signal energy ‖Xθ*‖² ≤ Mn | `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:8` | B | — | W3-PSHARP:A, W3-PSHARP-R:AE, W3-PSHARP-R:A2C | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(S) 1.3(D) | — |
| `A:GAUSS-NOISE` | D | Noise N(0, σ²I) independent of the design, σ² fixed (data law; see note †) | `Theory_work/Wave1/W1-GEN/STATEMENT.md:29` | B | — | W3-PSHARP:A, W3-PSHARP-R:AE, W3-PSHARP-R:A2C | 1.1(D) 1.2(D) 2.1(S) 3.1(S) 3.6(D) 1.3(D) | — |
| `A:PSHARP-COEF` | D | ‖θ*‖² ≤ nM′ on S₀ | `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:50` | B | — | W3-PSHARP:A, W3-PSHARP-R:AE, W3-PSHARP-R:A2C | 1.3(D) | — |
| `A:PSHARP-WORTH` | D | Witness: null columns mutually orthogonal and orthogonal to col X_{S₀} | `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:54-55` | B | — | W3-PSHARP:A, W3-PSHARP-R:A2C | 1.3(D) | — |
| `A:PSHARP-WORTH-E` | D | Witness (expectation form): PSHARP-WORTH and (log p)² = o(n) | `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:49-50` | B | — | W3-PSHARP-R:AE | 1.3(D) | — |
| `A:PSHARP-WSPH` | D | Witness: null directions i.i.d. uniform on the sphere of 1^⊥; (log N)² = o(n), (rank+1)log N = o(n) | `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:56-60` | B | — | W3-PSHARP:A | 1.3(D) | — |
| `A:PSHARP-WSPH-E` | D | Witness (expectation form): spherical nulls; (log p)² = o(n), (rank+1)log(pn) = o(n) | `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:52-57` | B | — | W3-PSHARP-R:AE | 1.3(D) | — |

Count (1.3): BD=7

UNIQUE all tiers: {'B': 57, 'A': 31, 'M': 15}; UNIQUE excluding route-only: {'B': 49, 'A': 31, 'M': 15}; total ids 103

Counting rule: an id is counted once however many rows use it; `↳` components count as ids (22 of them; 81 registry
ids). Composite headers (`A:OP`, `A:N1-KERNEL` counted under A; `A:DELIVERY-ALLOC` under M) are included in the counts.

## 3. Totals

| kind | unique ids (all tiers) | of which atomic (composite headers removed) | used at tier D or S in ≥ 1 core row |
|---|---|---|---|
| A (mathematical object) | 31 | 29 | 31 |
| M (method premise / idealisation / allocation) | 15 | 14 | 15 |
| B (design or data) | 57 | 57 | 49 (8 are route-only, tier R everywhere) |
| total | 103 | 100 | 95 |

Status buckets of the 29 atomic A items: **proved-and-checked 16** (MEAS, POT, SR, e4, DLV.FALLBACK, MR1-CAP, P-START,
P-MAP, NC-R, P:POST-CONC, P:SAND, P:NA-TL, P:LS0-DISCOVERY, P:NO-OUTPUT-ZERO, P:M5-COMPOSITION, P:DERANDOMISE);
**proved-unchecked 8** (N1.START, N1.KERNEL*, OP-LS0, E4.H1+, DLV.TDP-IMPL, DLV.P1-S3, P:SCORE-EXP route-only,
P:START-CENTRE route-only); **missing 5** (GUARD-W, CAL, BLOCK-LE-16 partial, P-OVL one-line, P-OVL-INF).

Where the A items live: rows **1.1, 1.2, 2.1 (display (i)) and 1.3 have no A item at tier D/S except
`P:DERANDOMISE` (1.2) and the sampler contract that drift D2 pulls into 2.1**. Track A is concentrated in rows **3.1,
3.5 and 3.6** (code and sampler premises).

## 4. Track-A gaps (missing or proved-unchecked), smallest closing lemma, tier guess, Lean tag

Tier per `Theory_work/Wave3/PROTOCOL_v4.md` §2 (:60-62): **A** = new key lemma; **B** = rider / restatement / re-check,
no new key lemma, ≤ about five lemmas. Code-reading lemmas are B (no key lemma); "re-check" = a second seat on an
existing proof. Ordered by how many core rows they touch at tier D/S.

| # | item (bucket) | core rows (tier) | smallest lemma that closes it (statement · 1-line route) | tier | Lean |
|---|---|---|---|---|---|
| G1 | `↳OP.GUARD-W` (missing) | 3.1 (D), 3.5 (D), 3.6 (D); 2.1 (S, via D2) | **Lemma GW.** In the code of record every guard check (i) reads only the clock, draws no uniform and changes no setting, and (ii) a run no check stops performs exactly the potential computation; a stopped run returns no estimates. · Code reading of every guard site (the island guard at `v3_engine.h:336-339` as cited in `W1-N1/STATEMENT.md:86`, and the run-level guards), extending `W3-SAMP:PC`'s comparison to all sites. | B | no |
| G2 | `A:CAL` (missing) | 3.5 (D), 3.6 (D); 2.1 (S); 3.1 (S, GEN route only) | **Lemma CAL-C.** The calibration record 𝓒 returned by `v3_calibrate` is a measurable function of (X, y) and streams 0–9; no final stream (10..9+R′) is read before 𝓒 is frozen. · Code reading of `v3_calib.R:144-183`, `v3_fit.R:154` and the stream assignment of `run_island` to stream 9+r (`v3_core.cpp:468-471` as cited in `W1-N1/STATEMENT.md:37-38`). | B | no |
| G3 | `A:BLOCK-LE-16` (missing, partial) | 3.1 (D), 3.6 (D); 2.1 (S) | **Lemma BLK.** The coded partition (complete linkage on 1−\|r̂\| cut at B, then next-fit packing with capacity B) is a function of X only and every block has size ≤ B = min(⌊√n⌋, ⌊√p⌋, 16) ≤ 16. · Next-fit never fills a bin beyond its capacity + CC7 (`W3-SAMP:CC`) for B ≤ 16; code reading of the partition routine. | B | yes (packing invariant only) |
| G4 | `↳N1.START` (proved-unchecked) | 3.5 (D), 3.6 (D); 2.1 (S) | **Lemma START-X.** Under EX-A/H-U, `draw_pi0` returns S with law γ₀/Z̄₀ on Ω and the reported normaliser equals Σ_Ω γ₀. · Re-check N9 Claims S, Z: backward sampling from the (block, size) DP table is exact for a block-product weight under a global size cap. | B | yes (algorithm level) |
| G5 | `↳N1.KERNEL` (proved-unchecked*) | 3.5 (D), 3.6 (D); 2.1 (S) | **Lemma KER.** Each coded move (Gibbs-j and the within-block swap/add/delete steps) is a π_φ-reversible kernel on Ω, and the round order is uniform and independent of the state. · Detailed balance per move type + the N9 rows 1–5 code reading; register the existing CHK_INHERITED verification as a claim. | B | yes (math half) |
| G6 | `↳OP.OP-LS0` (proved-unchecked) | 3.1 (D); routes elsewhere | **Lemma OPC.** In the shipped configuration (`ls0 = TRUE`, `ls0_cap = "ell_n_plus_mode"`, `ls0_tie_dp = TRUE`) every completed SMC run executes LS0 from `start_mode(...).S` with complete scans, and every LS0-scored model enters the final comparison. · Re-check `W1-GEN:L5` against `cpp/v3_core.cpp:394-404, 465-479` (the lines `W3-RM:E4` already cites). | B | no |
| G7 | `↳E4.H1+` (proved-unchecked) | 3.1 (S) | **Lemma ENC.** `build_tables`/`build_start` set `st.blocks`, `st.blk`, `st.pos` (inverse maps), `st.logr`, `codes_by_size`, `D->logprior` exactly as W1-N3 (H1) strengthened requires. · Code reading of `cpp/v3_start.h:76-151` (already quoted in `W1-N3/STATEMENT.md:92-98`); register as a code-check claim. | B | no |
| G8 | `↳DLV.TDP-IMPL` (proved-unchecked) | 3.1 (D; delivery clause only) | **Lemma TDP.** TDP-E returns lex_min of the maximiser set of the block-separable start score under the size cap (EX-A: returns S*), within the stated operation and storage bounds. · Second-seat re-check of `C-ENG/lemmas/TDP_E.md` (DP over (block, size) with tie-aware backtracking). | B | yes (DP correctness, finite) |
| G9 | `↳DLV.P1-S3` (proved-unchecked) | 3.1 (D; delivery clause only) | **Re-audit P1/S.3.** The P1 code inventory and degenerate case S.3 hold for the code of record. · Second-seat code reading of `C-DLV/STATEMENT.md:52-53` and `C-DLV/lemmas/L2_degenerate.md:37-67`. | B | no |
| G10 | `A:P-OVL` (missing, one line) | 3.6 (D; Thm D only, not on the C-v route); 2.1 (S) | **Lemma OVL.** Under production budgets and P-START, D_r·π₀(S₀) → ∞ in probability on 𝒜. · D_r ≥ max(2500, n, p)(L+6) deterministically (`W3-SAMP/STATEMENT.md` D-iii) and 1_𝒜π₀(S₀) → 1. | B | yes |
| G11 | `A:P-OVL-INF` (missing) | 3.6 (D; Thm TR only, the remark's alternative route); 2.1 (S) | **Lemma OVL∞.** Under Thm 10 (A2)–(A5), max_S π(S)/π₀(S) = o_P(log n) on 𝒜. · Needs a uniform bound on d(S) − d(S₀) over Ω relative to the start law — a new key lemma. **Cheaper close:** drop `W3-SAMP:TR` from row 3.6's master list (C-v already gives every conclusion). | A (or drop) | no |
| G12 | `P:SCORE-EXP`, `P:START-CENTRE` (proved-unchecked, route-only) | tier R in 1.1, 1.2, 2.1, 3.6; tier S in 3.1 via the GEN route | No action needed while `W1-GEN` stays a historical route: they are lemmas inside `W1-GEN:Thm-GEN` ("PROVED-CHECKED"); the checked variant `C-GROW:L0.1` covers SCORE-EXP. Otherwise: register L1/L2 as checked with Thm-GEN's check. | B | SCORE-EXP yes; START-CENTRE no |

Lean-department candidates (A items tagged yes, smallest first): G10 OVL, P:M5-COMPOSITION (checked), P:DERANDOMISE
(checked), P:LS0-DISCOVERY (checked), A:P-MAP's SL0 part (checked), G3 packing invariant, G8 TDP, G4 start sampler
exactness, G5 kernel reversibility, P:SCORE-EXP.

**Unchecked inputs on core paths that are claims, not assumptions** (outside track A's list, for the record):
`W3-POST:Prop-LB@1.0.0` and `W3-POST:Lemma-1a'@1.0.0` "PROVED (by this seat, unchecked)" (`W3-POST2:C` is conditional on
them: row 1.1 expectation form); `W3-READER:PoolZ` "PROVED (by this seat, unchecked)" (row 3.5); `W1-GEN:L1`–`L5`
"PROVED (by this seat, unchecked)" inside the checked `W1-GEN:Thm-GEN` (routes); `C-ENG:TDP_E` (G8).

## 5. Notes on borderline kinds

- **†** Data-law items `A:GAUSS-NOISE`, `A:DIST-A1`, `A:DIST-RD`, `A:IID-GAUSS-ROWS`, `A:DIST-A3`, `A:MISR-GRC` are
  distributions, but of the data; classified **B** per the brief ("not the data"). The Fable may move the noise law to A
  if "distribution" is read as the sampling model.
- **‡** `A:POST2-OS` (superset Occam sum) mixes the prior's Occam factors with design determinants; classified **B**
  because the prior is fixed by the method and the condition binds on the design (card open item O1). `A:EXT-FEAS`
  (s₀+1 ≤ K, K the prior's size cap) is B and holds eventually under FIXED-S0 and p > s₀.
- **No prior-property assumption appears in any closure**: the shipped prior is part of every row's setting; prior facts
  used are proved lemmas (e.g. inside `SOP:TH09`, `W3-DIST`). No divergence assumption appears either (Hellinger facts
  are proved: `W3-DIST:H` "PROVED-CHECKED; council …").
- **M items are not provable by design** (exact arithmetic, ideal uniforms, unbounded machine, allocation, worker
  equivalence, complete scans, IND-T); they need disclosure, not lemmas. `A:IDEAL-W+` is only needed for every-n delivery.


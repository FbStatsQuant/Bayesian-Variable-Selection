# W3-AUDIT — track D: could we do better? (v1, one pass, 2026-11-16)

Author: audit Fable. No proving. Statuses verbatim from `claims.tsv` of this worktree. Lines marked [audit calc] are my
own short computations, unchecked. Labels: **NECESSARY** (counterexample or lower bound cited), **LIKELY WEAKENABLE**
(route given), **UNKNOWN**. Constants are not a target (HQ ruling 2); a constant is mentioned only where it hides a
qualitatively worse dependence. Inputs used: `W3-DIST/reviews/UNHARVESTED_STRENGTH.md` (items 1–11),
`API_AUDIT/sharp2/TRIAGE.md`, `W3-READER/TRIAGE_SHARP3.md`, the check X sketch
(`W3-MISR-R/reviews/post_cp3/CHECK_X_sketch.md`), the post-freeze queue (`Theory_work/Dept/QUEUE.md:60-78`, dept/theory),
and tracks A and B of this audit.

---

## 0. Candidate #1 (fixed by HQ): "leaks inside a method block are harmless" — scoped first

**Short answer.** The candidate is sound and cheap for designs with **bounded groups**, and most of its proof is already
recorded. **It does not lift row 3.6 to AR, and it does not reach the BLK design of the 1M plan.** On AR with a fixed
ρ, a recorded result says the start mass on S₀ is destroyed, so no theorem that goes through "the start law concentrates
on S₀" can cover AR. HQ's stated purpose (AR, the primary 1M design) needs candidate #5 instead.

**What is already recorded.**
- The start-mass assembly is block-relative: `W3-START:ASM@1.0.0` "PROVED-CHECKED" (`W3-START/STATEMENT.md:213-219`): with
  Q = S₀, 1 − π₀(S₀) is controlled by the leakage functionals computed **on the method's own partition** (𝔏^b). The
  partition-free form in Theorem 5 is a presentation choice; bridge (B1) (`:232`) says it dominates the block-relative one.
- The same idea is recorded for the reported-model theorem: the block-relative leak condition (L_b) asks the gain bound
  only for U ⊇ S₀ ∩ C_{b(l)} (`W3-RM/STATEMENT.md:118-125`): "it lets Q omit a column whose only gain is un-conditioned on
  a truth that the method happens to place in the same block".
- The exact failure criterion is recorded too: `W3-START:NEC-b@1.0.0` "PROVED-CHECKED" (`W3-START/STATEMENT.md:221-226`),
  (C2)(i): if some null l has gain δ²_{U,l} ≥ c·τ²_U·log n **given the truths of its own block**, c > 1 + 2Ā, then
  P(π₀(S₀) ≤ n^{−κ′}) → 1.

**Why AR and BLK stay outside** [audit calc; verdict-bearing — please route a check].
- AR(ρ), ρ fixed: a column at distance k from a truth j has marginal gain ≍ nρ^{2k}θ_j²; this exceeds (1 + 2A) log n for
  every k ≤ k_n ≍ log n / (2 log(1/ρ)). A method block has at most 16 columns, so for large n some such column lies in a
  block that does not contain j. NEC-b (C2)(i) then gives π₀(S₀) → 0. (At n = 200–800, p = 10⁶, ρ = 0.6 and θ_j/σ = 1 the radius is only
  k_n = 1 to 3, so a truth whose near neighbours fall in its own block is fine and a truth at a block boundary is not.)
- BLK of the 1M plan: groups of 20 columns exceed the block cap 16, so every truth has group-mates (correlation 0.5) in
  a block without it: same conclusion.
- Pervasive factors (S5, P6, FAC): every null leaks from every truth; same conclusion.

**Gain.** Row 3.6 (Theorem 10) and row 3.3 (Theorem 5): assumption (A5) "no leakage" is replaced by "no leakage **given the
truths of the column's own group**". Designs that come inside: block designs with groups no larger than the block cap
B = min(⌊√n⌋, ⌊√p⌋, 16) and one or more truths per group — **S3, S4, S6 of the 2,400-fit study**. Still inside: S1, IND.
Still outside, with the recorded reason above: S2 and AR, BLK (groups of 20), S5, P6, FAC. Clauses that change: the
assumption line (A5) of Theorems 5 and 10; conclusions unchanged (rate √(log n/n) when the leak given the group's truths
is exactly zero, by `W3-START2-R:START-R` (iii)).

**Route (lemma chain).**
1. *Restatement (fixed design).* State Theorem START-F and IF-START with the block-relative functionals of Lemma ASM on
   the realised partition. Reuses `W3-START:ASM`, `W3-START:LEAK`, `W3-START:VIS-c` (each "PROVED-CHECKED") and the
   START2-R sharpenings unchanged. No new mathematics; a sample-level theorem of the kind of Theorem 7.
2. *Group containment (new, small; the key lemma).* Gaussian rows; a deterministic partition of [p] into groups of size
   ≤ g ≤ B with |Σ_jk| ≥ r₀ inside groups and |Σ_jk| ≤ r₁ < r₀ across groups (fixed r₀, r₁). Then with probability → 1
   every group lies inside one method block. Route: entrywise concentration of sample correlations (as in
   `C-GROW:L6.2`, "PROVED-CHECKED"); in complete linkage all within-group merges precede every across-group merge, so
   each group is a node of the tree; the top-down cut does not split a node of size ≤ B; packing keeps clusters whole.
   The last two facts are code readings of `cpp/v3_blocks.h` and extend track-A item T2. Model: partition recovery in
   `W1-PXN:Thm-PXN(R)` ("XF VERIFIED").
3. *Gaussian-row bridge, restricted family.* Population condition (A5′): for every null l with group G(l), every U with
   S₀ ∩ G(l) ⊆ U, |U| ≤ 15, and every truth j ∉ U: |Cov(W_l, W_j | W_U)| ≤ C n^{-1/2}, with the locality clause of (A5)
   kept. On the event of step 2 every conditioning set the method uses has this form. Route: the proof of
   `W3-START2-R:BR` ("PROVED-CHECKED; council R2, …") with its reference family restricted to such U.
4. *Assembly.* Steps 1–3 give P-START; `W3-SAMP:C` (C-v) and Theorem 10 are unchanged. P-START is not replaced: it is
   delivered on more designs. Reader version: one new assumption line and a primitive corollary (block-diagonal Σ with
   groups ≤ g ≤ B, λ_min ≥ c, fixed nonzero coefficients).

**Cost.** One Opus lead, about 3 days; Tier A with one small key lemma (step 2); steps 1, 3, 4 are riders on checked
proofs. Reviews per PROTOCOL_v4 Tier A (the key-lemma break review is on step 2 only).
**Kill budget.** Step 2: two proof attempts, or one code reading showing that the cut or the packing can split a group
of size ≤ B. If it is killed, deliver step 1 alone (Tier B, about 1 day): a correct fixed-design theorem under
block-relative no-leakage, with S3, S4, S6 as numerical examples only.
**What it does not buy, to say in the ticket:** AR, the primary 1M design.

---

## 1. Sharpness records, one per core theorem

### Core 1 — the posterior finds the true model (rows 1.1, 1.2)
| Assumption | Label | Evidence or route |
|---|---|---|
| Gaussian errors | UNKNOWN | no result either way; every comparable Bayesian selection theorem assumes it |
| p ≤ n^A | UNKNOWN | registry A:P-POLY: exponential p "OPEN" |
| s₀ fixed | NECESSARY up to √log n | `W3-PSHARP:B`: rate needs s₀ = O(√log n); π(S₀ \| y) → 1 needs s₀ = o(√n), on every design. Flag: the beta-min constant c₀ grows linearly in s₀(A + 1) (`assumptions.tsv` A:BETAMIN), which would become a rate factor if s₀ grew |
| Bounded coefficients | NECESSARY in some form; LIKELY WEAKENABLE in level | explicit counterexample for the size-tail step (Thm 1 why-lines); sub-linear energy growth believed enough |
| Floor on bounded sets off S₀ (A4) | LIKELY WEAKENABLE — done | Thm 1′ (`W3-POST2:E`) replaces it by a residual-signal margin |
| Floor on S₀ | UNKNOWN | card open item O3 (route: a bounded ridge cost) |
| No near-collinearity on O(log n) sets (A5) | LIKELY WEAKENABLE | superset Occam-sum condition (`W3-POST2:A1`, remark (o)); whether it holds with no eigenvalue condition is open (O1) |
| Beta-min order √(log n/n) | UNKNOWN (numerical evidence that it is necessary) | numerics and a leading-order heuristic, no proof (Thm 1 why-lines) |
| Gaussian rows (Thm 2) | LIKELY WEAKENABLE | candidate #3 |
| Floor fixed, on sets of 5(A + 1)(s₀ + 1) log n (Thm 2) | LIKELY WEAKENABLE | the master already lets it vanish on the O(log n) sets; check X (candidate #2) asks it on smaller sets |

**Conclusion.** Rate √(log n/n): **OPTIMAL on the witness designs, in expectation, for every p** (Theorem 3; exact order
on fully orthogonal designs). On a general design the proved lower bound is n^{-1/2}: a **GAP of √log n** (rider POST2-R1,
open). Random designs: the upper bound is in probability only: a **GAP** that candidate #2 would close. Against
Song–Liang: they give screening with an exponential bound in nε_n²; we give exact selection at a polynomial rate that
no design can beat for this prior by more than √log n (Theorem 3(a)). The polynomial rate is a property of the coded
prior, not of the proof.

### Core 2 — the posterior finds the true distribution (row 2.1)
| Assumption | Label | Evidence or route |
|---|---|---|
| Gaussian linear model | UNKNOWN | — |
| At most s nonzero coefficients, s fixed | LIKELY WEAKENABLE (uniform in s) | UNHARVESTED item 9: track n₀(s). **Flag (hidden dependence):** display (iii) has squared radius of order (1 + s)³, against Song–Liang's linear s; display (i) is already linear in s through the level |
| p ≤ n^A | LIKELY WEAKENABLE in form | items 8(a) + 10: write the level in log(p ∨ n) with A explicit; a constant free of A (8(b)) may be false |
| Sub-Gaussian sparse directions (A3) | UNKNOWN | used only for sample-to-population tracking |
| No near-exact collinearity (A4) | NECESSARY in some form for the fixed-design interface; LIKELY WEAKENABLE in window | `W3-DIST:NEC` ("PROVED-CHECKED; council R2, …"): without it the distance clause of the interface lemma fails; item 1: fewer set sizes and an averaged form. Whether a random-design theorem needs it is open |
| Bounded standardised signal (A5) | UNKNOWN | excludes large cancelling coefficients |

**Conclusion.** Radius √(M log n/n): better than Song–Liang's at polynomial p (their ε_n² ≻ r̄_n log P_n / n with r̄_n → ∞,
(10) and Theorem 2, pp. 952–953); written in log n, not log p: a **GAP in form only** (candidate #4). Theorem 9B's rate
M_n/√n is parametric: **OPTIMAL**. Corollary 9C: its premise on the list is not certified by the output (UNHARVESTED item
11 would widen the retention sentence; no headline change).

### Core 3 — the coded algorithm reports the true model (row 3.1)
| Assumption | Label | Evidence or route |
|---|---|---|
| Gaussian rows | UNKNOWN | conditional covariances are used structurally; no cheap route |
| Visibility at a fixed level (A3) | NECESSARY for the start route; not for the conclusion | `W3-START2-R:NEC` (N3⁺⁺): the level cannot be lowered for the start mass; masked designs are covered by a separate theorem (W1-PXN). Constant-level forms are already harvested (W3-RM2-R, accepted, not yet in this registry) |
| Leak level outside Q, ϖ_n = o(√(log n/n)) per truth | LIKELY WEAKENABLE | aggregated leak \|Cov(W_l, Σθ*_kW_k \| W_U)\| (sharp2 triage, RM2-R row, class D: half a day with a proof agent) |
| \|Q\| ≤ n^b, b < ½ | UNKNOWN beyond the route | the route's events are expected to fail past ½ (heuristic); pervasive factors: the start-mode search alone fails (`W2-FAC-PK:Thm-NEG`, "PROVED-CHECKED"), the full method is open (P6) |
| Floor on Q ∪ {l} | UNKNOWN | necessity not asserted |
| Local regressions in Q (A6) | NECESSARY for the route, in its width form | `W3-RM2:W-conv` ("PROVED-CHECKED; council R1, …"); the equicorrelated group is verified for b < 3/10, sketched to 3/8 (queue item O4′) |

**Conclusion.** "Every admissible run that produces output reports S₀ on one data event": no rate is claimed (a **GAP**;
the search-event rate is recorded in the proof, sharp2 triage). No published comparator. Verdict: **near-optimal for
this route**; the open question is the scope (factors), which is decision D1, not a sharpening.

### Core 4 — the run's estimates are consistent (rows 3.6, 3.5)
| Assumption | Label | Evidence or route |
|---|---|---|
| No leakage (A5), partition-free | LIKELY WEAKENABLE to the group-relative form | candidate #1 |
| No leakage given the truths of the block | NECESSARY for start concentration | `W3-START:NEC-b` (C2)(i), "PROVED-CHECKED" |
| Start concentration (P-START) itself | NECESSARY for the evidence clause in Theorem C's stated scope (any frozen parameters); not known to be needed at production budgets | sharp3 triage C1–C2: E\|W_r − 1\| ≤ 2·TV(π, π₀), attained at N_e = T = 1 |
| Global overlap (P-OVL∞) as an alternative | fails on leaky designs [audit calc; verdict-bearing] | where a fixed-level leak sits outside the truth's block, π₀(S₀) is exponentially small while π(S₀) → 1, so max π/π₀ is exponentially large; route TR cannot reach AR either |
| Visibility, floors, Gaussian rows | as core 3 | — |

**Conclusion.** Rate n^{-1/2}e^{C√log n} in the reader version: a **GAP**; √(log n/n) is already proved when nulls are
uncorrelated with truths (`W3-START2-R:IF-START`, "PROVED-CHECKED; council R2, …") and only needs the reader swap; the
floor ½(n + 1)^{-1/2} makes that optimal up to √log n. Scope: the conclusion is believed true far beyond the assumption
(card row 4.3: PIPs agree across islands to ≤ 5×10⁻⁴ on a block design of type S3, which is outside (A5)), but both recorded routes need π₀ close to π. Row
3.5: no design assumption, an identity: **OPTIMAL**.

### Core 5 — the rate cannot be improved (row 1.3)
Part (a) has no assumption. Part (b)'s witnesses are not claimed necessary. **Open, not ranked** (no assumption or
headline clause changes for the paper as planned): a lower bound √(log n/n) on every design under a floor on S₀ ∪ {j}
(POST2-R1); the in-probability form when log p = o(log n); whether the constant of the expectation display is attained.

---

## 2. Ranked improvement candidates (≤ 5)

| # | Candidate | Gain (headline clause) | Route | Cost | Kill budget |
|---|---|---|---|---|---|
| 1 | Group-relative no-leakage (HQ) | Rows 3.6, 3.3: bounded-group designs inside (S3, S4, S6). **Not AR, not BLK** | §0 | Opus lead ≈ 3 days; Tier A (one small key lemma) | 2 attempts on group containment; fallback = fixed-design restatement, Tier B, 1 day |
| 2 | Check X: Theorem 2 from the omitted-variables master | Row 1.2: expectation rate on Gaussian designs (closes the random-design gap of core 1), Σ, β, σ² free to vary with n, floor on smaller sets; also the posterior input of row 3.1 | Read-only alignment note: do Theorem 2's assumptions imply (A0)–(A3) of `W3-MISR-R:CorGb-plus` ("PROVED-CHECKED, conditional on W3-POST2:C, …")? Sketch exists, unchecked. Then a recorder decision | 1 Opus day; Tier B (no new lemma) | stop if any of (A0)–(A3) is not implied; record the missing hypothesis |
| 3 | Sub-Gaussian rows for Theorem 2 | Row 1.2: "Gaussian rows" → Theorem 9's (A3); removes one of the three items that are stronger than Song–Liang (B7) for the model-selection row | Replace the Gaussian entrywise step of `W2-APP:POST` by the sample-floor bridge `W3-DIST:B2core` / `B2` ("PROVED-CHECKED; council R2, …"); the fixed-design theorem and the transfer lemma are unchanged | Opus lead ≈ 2 days; Tier B | 2 attempts; stop if the energy or beta-min events need more than (A3) on sparse directions |
| 4 | Theorem 9 sharpness bundle (order already set, card 13) | Row 2.1: (A4) on a smaller window, averaged (item 1); level in log(p ∨ n) with A explicit (8(a) + 10); radius linear in s in display (iii) (item 9, the s³ flag) | As costed in `UNHARVESTED_STRENGTH.md`; each is constant or restatement work in `lemmas/X.md`, `DIST12.md` | Opus lead ≈ 3 days in all; Tier B; statement-change checks | item 8(b) (constant free of A) excluded: it may be false; item 9: 2 attempts |
| 5 | Printed estimates on leaky designs (what AR needs) | Row 3.6 on AR and BLK: PIP and MPM clauses without start concentration | New key lemma: non-collapse of the evidence weight (NC_r) for the tempered sampler when the start law sits on the lattice of a small leakage set, then `W3-SAMP:LT#` (LT-e) as recorded. No recorded route; sharp3 lists it as open (C9, L10, T5) | Opus lead ≥ 5 days, Fable for the key lemma with HQ's OK; Tier A; high risk | 3 attempts on the key lemma (STUCK rule); go only after a half-day feasibility note |

**Order (recorded 2026-11-16).**

| | Order | Notes |
|---|---|---|
| **HQ decision** | **#2 → #3 → #1**; #4 deferred; #5 decided on the note in §5a | at most 3 tickets, post-freeze from Sat 11-21, and only after the Opus check confirms the [audit calc] lines. Kill budgets set by HQ: #2 1.5 days (estimate 1), #3 3 days (estimate ≈ 2), #1 4 days (estimate ≈ 3). #5 may replace #1 only if §5a shows a realistic route to a printed-output clause on AR; otherwise row 3.6 stays scoped as worded and AR coverage stays with Theorem 6 and row 3.5 |
| My value-per-cost order | 2, 3, 1, 4, 5 | the same first three; the table above keeps the numbering of the first pass (HQ's #1 scoped first) |

**Considered, not ranked.** Aggregated leak for row 3.1 (real, small, but no design of ours moves); the equicorrelated
group up to b = 3/8; SAMP-R1 and the row 3.6 rate swap to √(log n/n) (already queued riders; restatements); POST2-R1;
O1–O3 of row 1.1 (no route); exponential p (no route).

## 3. X1–X5 (queued after the 13 items)

| Item | Kind | Note |
|---|---|---|
| X1 frozen-run identities T12 ("PROVED-LOCKED") | **lemma (Tier B)** | one line check of T12 (i.a)–(i.c), (ii), (R3) for the code of record; the label change follows |
| X2 `W3-POST:Prop-LB` | **relabelling (recorder)** | an implication note exists (`Theory_work/Dept/research/IMPL_PSHARPB_PROPLB_opus.md`, dept/theory); record Prop-LB as implied by `W3-PSHARP:B` if that note is accepted |
| X3 `W3-POST:Lemma-1a'` | **lemma (Tier B)** | one line check |
| X4 edge `W3-DIST:Cor-C → DIST-C` | **relabelling (recorder)** | retype to clauses (C-0), (C-i) threshold form, (C-ii)(α) |
| X5 `W3-READER:PoolZ` | **lemma (Tier B)** | two-line proof; line check and registry row |

## 4. The [audit calc] lines: which verdicts depend on them (HQ ruling 5)

| Where | Calculation | A verdict depends on it? |
|---|---|---|
| TRACK_B B3 | bounds 0.74 / 0.81 / 0.88 from Theorem 3(a) | no (illustration) |
| TRACK_B B5 | per-observation margin of Thm 1′ against Song–Liang's level | no (the verdict rests on the quoted Condition 3) |
| TRACK_B B5 | λ_min(Σ) of the 13 designs | **yes**: every "inside" entry of B5, B6 and the sentence "all our designs are inside cores 1 and 2" |
| TRACK_B B7 | Thm 9 (A3) ⇒ Song–Liang Condition 1 | **yes**: the verdict "stronger than Condition 1 (implies it)" |
| TRACK_B B8 | visibility on S1–S4, S6, IND, AR, BLK, cs | **yes**: those "inside" entries (the Song–Liang verdict does not depend on it) |
| TRACK_B B9 | partial covariance under cs(ρ); the same claim for fac2 and s5 without a displayed formula | **yes**: the "outside" entries for S5, P6, FAC |
| TRACK_B B11 | a truth's AR neighbour or block-mate has fixed covariance | **yes**, but immediate from Σ |
| TRACK_D §0 | start mass destroyed on AR and on BLK (via NEC-b) | **yes**: the scope of candidate #1 and the need for #5 |
| TRACK_D core 4 | P-OVL∞ fails on leaky designs | **yes**: "route TR cannot reach AR" |

Suggested routing: one Opus read (half a day) of the six "yes" rows; the two TRACK_D rows first.

---

## 5a. Feasibility note for candidate #5 — printed estimates on AR(ρ) without start concentration (2026-11-16)

Everything here is a sketch [audit sketch, unchecked]; nothing is proved. Setting: Theorem 6's assumptions (AR(ρ)
satisfies them with a leakage set Q of O(log n) columns around the truths), production budgets, the sampler branch.
𝓛(Q) is the lattice {S₀ ⊆ T ⊆ Q}; q_φ ∝ γ₀^{1−φ}γ₁^{φ} is the tempered target (q₀ = π₀, q₁ = π).

**What a lemma would have to state.** Two forms, the second weaker.
- *(NC) Evidence form.* 1_𝒜·|Ẑ_r/Z − 1| → 0 in probability. This is NC_r with a rate; with `W3-SAMP:LT#` (LT-e) it gives
  every clause of Theorem 10 (PIPs, MPM, Ẑ) with (A5) replaced by Theorem 6's leakage set.
- *(OCC) Occupancy form.* At the end of the bridge the fraction of island r's particles in 𝓛(Q) tends to 1 in
  probability on 𝒜. It says where the particles are, not what the weights are. It would give the PIP and MPM clauses
  only: after the bridge the code runs L = max(4, ⌈log₂(n + 1)⌉) rounds at φ = 1 (`W3-SAMP/STATEMENT.md:103`), each round
  contains a Gibbs step for every column (`:56-57`), and from a lattice state one such round deletes every extra with
  probability → 1 on the no-addition event; `W3-SAMP:ST` then keeps the particle at S₀.

**Recorded pieces it could reuse.** The start law is on 𝓛(Q) with a rate (`W3-START2-R:START-R` (i), "PROVED-CHECKED;
council R2, …"). The events at φ = 1 on the lattice: sandwich, no-addition, truth-removal (`W3-RM2:SAND-R-b`, `NA-W`,
`TL-F-b`). The transfer from non-collapse to the printed fields (`W3-SAMP:LT#`), the staying lemma (`W3-SAMP:ST`), the
path identities (`W3-SAMP:MR`). The grid lemmas and the two-model closed forms of `C-DLV` (`L3-3.3`, `L3-3.5a`, `L5-5.1`,
`L5-5.2`, each "PROVED-CHECKED"). From `W3-DIST`: the domination transfer and the retention fact of DIST-C (C-0),
(C-ii)(α), for the weaker statement below.

**First obstruction.** π₀ and π are nearly singular on AR (π₀(S₀) is exponentially small). Every recorded identity about
the particles carries the factor Ẑ_r/Z (`W3-SAMP:MR`), so it says nothing unless non-collapse is already known; and the
record contains no mixing or variance statement for the coded sampler (`W3-SAMP/STATEMENT.md:183`). A proof must
therefore follow the population forward, stage by stage, through resampling. The step most likely to fail is the
resampling step: a lower bound on the normalised mean incremental weight of the lattice particles under the frozen,
calibrated grid, together with control of rare off-lattice particles whose weights can be large.

**Cheapest route (three steps).**
1. *Interpolation for single moves.* For T ∈ 𝓛(Q) and any single flip or swap that leaves 𝓛(Q), the q_φ-odds of the move
   equal (odds at φ = 0)^{1−φ}·(odds at φ = 1)^{φ}, hence are at most the larger endpoint odds. The endpoint bounds are
   the recorded ones (leak and visibility bounds at φ = 0; no-addition and truth-removal at φ = 1). This gives "tempered"
   versions of those events with no new estimate, provided the φ = 0 bounds hold uniformly over lattice states.
2. *Near-product structure on the lattice.* Under Theorem 6's local-regression condition the inclusion odds of an extra
   depend little on the other extras, so one Gibbs round nearly refreshes the lattice coordinates; the relative variance
   of the stage weights on the lattice is then the χ²-distance between consecutive targets, which the grid rule controls.
3. *Assembly.* Induction over the stages for (OCC); a second-moment bound of order T/N_e for (NC).

**Go / no-go (kill budget).** A gate of at most 2 Opus days before any Tier A ticket:
- **G1.** Write step 1 as a lemma and check that the φ = 0 bounds are uniform over lattice states, including additions
  inside a block that already holds lattice extras. **No-go** if they are not.
- **G2.** Exact computation on a toy lattice (one truth, m independent leaking columns, the coded resampling and grid
  rule): is Var(Ẑ_r/Z) ≤ C·T/N_e at production N_e? **No-go** if the weights degenerate.
If both pass: Tier A, Fable for the key lemma with HQ's OK, 3 attempts (STUCK rule). If G2 fails but G1 passes, only
(OCC) is worth a ticket.

**A weaker statement on AR that needs none of this — yes, a store-restricted clause; no for the printed MPM.**
- On Theorem 6's data event every completed run scores S₀ (its final search ends there), so the returned list 𝒯 contains
  S₀ and S₀ is the reported model (DIST-C (C-ii)(α)). Then, deterministically and in exact arithmetic: the PIPs computed
  from the returned list satisfy max_j |PIP^𝒯_j − 1{j ∈ S₀}| ≤ 1 − π(S₀ | y); their median model is S₀; the sum of the
  list's weights Z^𝒯 satisfies π(S₀ | y)·Z ≤ Z^𝒯 ≤ Z; and Corollary 9C's bound holds with π(𝒯) > ½. With Theorem 2 the
  errors are O_P(√(log n/n)). A store-restricted PIP corollary already exists unchecked (`C-PACK` Corollary SL2,
  `I4_SL_corollaries.md:90`).
- Reach: every design inside Theorem 6 — S2–S4, S6, AR, BLK — with no start or leakage-free condition.
- Cost: Tier B, 1–2 Opus days. Two links are named as unchecked in the record and must be closed
  (`W3-DIST/STATEMENT.md:297-303`): that Theorem 6's output event covers "completed", and that its reported model is
  the printed field `hpm`.
- Limit, to state plainly: these are functions of the output that the method does not print; the printed PIPs, MPM
  and Ẑ are sampler averages. Printing the list-based quantities would be a code change (Engineering and HQ).
- The printed MPM alone is **not** reachable without at least (OCC): it depends on where the final particles are.

**Answer to HQ's question: does this note show a realistic route to a printed-output clause on AR?**
- For the **printed fields** (the sampler's PIPs, MPM and Ẑ): **no, not today.** The route above is a plan with two
  untested steps (G1, G2), no recorded mixing or variance result to stand on, and a new key lemma after that. It is
  plausible, not realistic within a kill budget of a few days.
- The printed **reported model** on AR is already covered (Theorem 6), and the printed evidence is unbiased (row 3.5).
- The store-restricted clause is realistic (Tier B, 1–2 days) but it is a statement about quantities computed from the
  returned list, **not** about printed fields. It is a separate cheap item (#5′), not a substitute for #1.

**Go / no-go (one line): NO-GO for #5 replacing #1 — there is no realistic route to a clause on the printed PIPs, MPM or
Ẑ on AR; keep row 3.6 scoped as worded, with AR covered by Theorem 6 and row 3.5; optional: #5′ (store-restricted
clause) and, only if HQ wants to keep the question alive, the 2-day G1/G2 gate.**

# W3-AUDIT — are our assumptions reasonable? AUDIT v1.4 (conditional-comparison format, 2026-11-16)

Author: audit Fable (Claude Fable 5.2, high). Branch `theory/W3-AUDIT`. Steps 1 (assumptions) and 2 (track D) of the brief, after
one revision round. v1.1 applies the independent check of my own computations (`reviews/AUDITCALC_check_opus.md`, 2d7c2b90: none
refuted, four corrected) and cites track C (`track_C/RESULTS.md` @ 4f0f9a82, internal, Owls part).

**Sources.** Theorem statements: reader versions `W3-READER/READER_VERSIONS.md` §1, §2, §3, §6, §9, §10 (W3-READER worktree
@ 7eb818e6; **READER pre-freeze**, to be re-pinned to the READER commit of the CP3 freeze) and their masters. Statuses: `Theory_work/INFRA/registry/claims.tsv` of this worktree (main a7fc5093), quoted
verbatim; council suffixes cut and marked "…". Track-A inventory: `work/A_inventory.md` (Opus helper, 2e6c7d86), checked in
§6. Song and Liang (2015): the paper itself (JRSS-B 77(5), 947–972; `/home/fb31/SMC_Theory_Department/refs/Song_Liang_2015.pdf`,
sha256 `315c247c236b5f33…`), journal pages; the supplement (`Song_Liang_2015_supplement.pdf`, same folder, sha256 `a584b328c859c087…`) was read
for v1.3 (pp. 13–16 as images; pp. 1, 4, 5, 6, 12, 17 as text), cited as "supp p.". Track-B dossiers B1–B12: `TRACK_B.md`.

**Columns.** *Track*: **A** = mathematical object (prior, distribution, divergence, kernel or algorithm property; must be
proved), **B** = design or data (must be explained), **M** = stated idealisation of the machine or the random numbers (not
provable; disclosed). *Status or dossier*: for A, the claim that discharges it and its registry status; for B, the dossier.

**One-paragraph answer.** Our theorems use the same kinds of assumptions as Song–Liang's. On the designs we study the
assumptions of the two posterior theorems hold, strong factors included. Where the two papers differ, the direction
depends on the regime — their model-size cap r̄_n, centring, the reading of their β*, and which of their theorems is the
comparator — and is given assumption by assumption in the summary table of `TRACK_B.md`; no overall "stronger" or
"weaker" is claimed, and conclusions are compared per theorem (`TRACK_B.md` §S).

**Format rule (HQ, v1.4).** In the tables below the last column names the Song–Liang counterpart (page and equation;
"supp" = their supplement). A one-word comparison appears only where it holds in every regime; otherwise the column
points to the dossier, which gives the comparison as a conditional sentence. The reported-model theorem adds two method-specific
design conditions with Song–Liang counterparts (their Condition 5 and their remark (a), p. 958); it excludes pervasive
factors at p ≫ √n. The printed-estimates theorem (row 3.6) is correct as stated and has a narrow reach: its "no leakage"
condition holds on independent designs only (B11; §9). On the mathematical side, rows 1.x and 2.1 have no open item; rows 3.1, 3.5
and 3.6 rest on 13 code-level items that are named but not yet checked (§6).

---

## 1. Core theorem 1 — the posterior finds the true model (rows 1.1, 1.2; Thm 1, 1′, 2)

Masters: `SOP:TH09@1.0.2` "PROVED-CHECKED (T03♯ only: the conjunction of W3-T03ACC:T03S.1–T03S.4, clause map CHECKPOINT_4.md
§2; council R1, …)"; `W3-POST:Thm-1@1.0.0` "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (label not yet
refreshed); expectation form `W3-POST2:C@1.0.5` "PROVED-CHECKED, conditional on W3-POST:Prop-LB, [L1a′], W2-APP:POST,
W3-POST:Thm-1"; Thm 1′ `W3-POST2:E@1.0.5` "PROVED-CHECKED, conditional on W2-APP:POST, W3-POST:Thm-1"; random design
`W2-APP:POST@1.0.7` "PROVED-CHECKED".

| Assumption | Track | Status or dossier | Song–Liang (2015) |
|---|---|---|---|
| Gaussian errors, fixed variance (S1) | B | B1 | model (1), density (2), p. 950: the same in every regime |
| p ≤ n^A (S2) | B | B2 | Cor 1, p. 954 (Hellinger); condition 2 of Theorem S, supp p. 13, and Cor S₁, supp p. 16 (selection); P_n ≻ n^θ, p. 950. By regime: B2 |
| The prior as coded (a setting, not an assumption) | A | prior facts are proved inside `SOP:TH09` (status above); no open item | their prior (6), p. 951, with cap r̄_n and conditions (9)–(14), p. 952; Theorem S ties r_n to n and P_n (supp p. 13). Ours has no condition on hyperparameters; the posteriors differ |
| s₀ fixed (Thm 1 (A2), Thm 2 (A2)) | B | B3 | strict sparsity (4), p. 950: the same (their Thms 2, 3, S); their Thm 1 also allows (3) |
| Bounded coefficients (Thm 1 (A3)) | B | B4 | (3) and (8), pp. 950, 952 (their Thm 1); none stated under (4). By reading of β*: B4 |
| Sparse eigenvalue floor on bounded sets (Thm 1 (A4)); floor on S₀ + residual-signal margin (Thm 1′ (A4′)); population floor (Thm 2 (A3)) | B | B5 | Condition 3, p. 955; (22)–(23), supp p. 13. By regime of r̄_n: B5 |
| No near-collinearity among O(log n) columns (Thm 1 (A5)) | B | B6 | Condition 3, p. 955; (22), supp p. 13. By regime of r̄_n: B6 |
| Beta-min at √(log n/n) (Thm 1 (A6)); fixed nonzero signals (Thm 2 (A2)) | B | B4 | no lower bound stated; proof rates at supp pp. 6, 15. By reading of β*: B4 |
| Rows i.i.d. Gaussian (Thm 2) | B | B7 | Condition 1, p. 953; \|x_i\| ≤ 1, p. 952. By centring: B7 |
| Fixed-to-random design transfer | A | `C-MIS:LemDR@1.0.0` "R02 VERIFIED; council R07/R08 PASS", used inside `W2-APP:POST` | not needed (random design throughout) |
| HPM, MPM, PIPs from 1 − π(S₀ \| y) | A | `C-PACK:SL0@1.0.1` "PROVED-CHECKED"; `W3-T03ACC:T03S.2`, `T03S.3` "PROVED-CHECKED; council R1, …" | Thm 3, p. 956: sensitivity only, exponentially small error. Theorem S, (24), supp p. 13: the mode of their posterior (7), no rate. Per-theorem comparison: `TRACK_B.md` §S |

Open on the mathematical side (claims, not assumptions): the expectation display of Thm 1 is conditional on
`W3-POST:Prop-LB@1.0.0` and `W3-POST:Lemma-1a'@1.0.0`, both "PROVED (by this seat, unchecked)" (§6, items X2, X3).

## 2. Core theorem 2 — the posterior finds the true distribution (row 2.1; Thm 9, 9B, Cor 9C)

Masters: `W3-DIST:Thm-A@1.0.0` "PROVED-CHECKED; council R2, …"; `W3-DIST:Thm-B@1.0.0` "PROVED-CHECKED, conditional on
W3-POST:Thm-1; council R2, …"; `W3-DIST:Cor-C@1.0.0` "PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2, …".

| Assumption | Track | Status or dossier | Song–Liang (2015) |
|---|---|---|---|
| (A1) Gaussian linear model, any noise level | B | B1 | model (1), density (2), p. 950: the same in every regime |
| (A2) at most s nonzero coefficients; p ≤ n^A | B | B3, B2 | (4), p. 950 (their Thm 2): the same; (3) in their Thm 1; range of p: B2 |
| (A3) sub-Gaussian predictors on sparse directions | B | B7 | Condition 1, p. 953; \|x_i\| ≤ 1, p. 952; Condition 2, p. 954. By centring: B7 |
| (A4) no near-exact collinearity, floor c_ψ/n on O(log n) sets | B | B6 | none in their Thms 1–2 in any regime ((11), (14), p. 952, are on V_ξ); their ridge example c_n ∝ 1/n, p. 953: B6 |
| (A5) bounded standardised signal | B | B4 | (3) and (8), pp. 950, 952 (their Thm 1); none stated under (4): B4 |
| (A6) of Thm 9B: fixed floor on bounded sets; beta-min | B | B5, B4 | no parametric-rate result in Song–Liang |
| Hellinger distance facts (averaged conditional = joint; d² = 2d_H²) | A | `W3-DIST:H@1.0.0` "PROVED-CHECKED; council R2, …" | same distance (§2.1.2, p. 952) |
| Cor 9C: returned list and its log-weights are as described | A | code facts `W3-SAMP:CC@1.1.2` "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)"; Cor 9C uses only the deterministic clauses of `W3-DIST:DIST-C` (§6, X4) | their sampler statements are limits as N → ∞ at fixed data (supp pp. 9–10, 12–13, 16–17); neither theirs nor ours implies the other (`TRACK_B.md` §S) |
| Cor 9C: exact arithmetic (EX-A) | M | disclosed in the status | — |

## 3. Core theorem 3 — the coded algorithm reports the true model (row 3.1; Thm 6)

Masters: `W3-RM2:RM2-R@1.0.3` "PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, …"
(its input `W2-APP:POST@1.0.7` now reads "PROVED-CHECKED"); `W3-RM:RM-0@1.0.0` "PROVED-CHECKED"; `W3-RM:E4@1.0.0`
"PROVED-CHECKED"; delivery `W2-UNI:F-UNI@2.1.0` "PROVED-CHECKED".

| Assumption | Track | Status or dossier | Song–Liang (2015) |
|---|---|---|---|
| Rows i.i.d. Gaussian; (S1), (S2) | B | B7, B1, B2 | Condition 1, p. 953. By centring: B7 |
| (A2) s₀ fixed, fixed nonzero signals | B | B3, B4 | sparsity: (4), p. 950, the same; signal size: by reading of β*, B4 |
| (A3) visibility given ≤ 15 columns | B | B8 | Condition 5, p. 958: ours implies it in every regime (their case is U = ∅ without the margin) |
| (A4) leakage set \|Q\| ≤ n^b, no leak outside, locality | B | B9 | no hypothesis; informal remark (a), p. 958: B9 |
| (A5) population floor on O(log n) sets and on Q ∪ {l} | B | B5, B10 | Condition 3, p. 955; (22), supp p. 13. By regime: B5, B10 |
| (A6) local regressions inside Q | B | B10 | no condition of this kind |
| Blocks of at most 16 columns, a function of X only | A | **missing (partial)**: `W3-SAMP:CC` (CC7) gives B ≤ 16 only; `assumptions.tsv` A:BLOCK-LE-16 bridge "MISSING" (§6, T2) | — |
| Start mode: the emitted centre maximises the start law | A | `W3-RM:E4@1.0.0` "PROVED-CHECKED", under code hypothesis (H1) strengthened, which is unchecked (§6, T4) | — |
| LS0 is executed from the start mode with complete scans; its models enter the final comparison (OP-LS0) | A | **unchecked**: `W1-GEN:L5@1.0.0` "PROVED (by this seat, unchecked)" (§6, T3) | — |
| A stopped run returns no estimates; a completed run equals the potential run (GUARD-W) | A | **missing**: "audit open, not discharged here" (`W1-N1/STATEMENT.md:86-88`); `W3-SAMP:PC@2.1.1` "PROVED-CHECKED" is "a limited comparison, not the full GUARD-W audit" (§6, T1) | — |
| Sandwich, no-addition, truth-removal events; posterior input | A | `W3-RM2:SAND-R-b`, `NA-W`, `TL-F-b`, `D-to-W`, `F-to-R` "PROVED-CHECKED; council R1, …"; `W3-RM2:POST-R` "PROVED-CHECKED, conditional on W2-APP:POST; …" | — |
| Exact arithmetic, ideal uniforms (S3) | M | disclosed | — |
| Delivery clause (S4): fallback, allocation, machine, IDEAL-W⁺ | M, with two A items | `C-DLV:Prop-F@1.0.0` "PROVED-CHECKED for the patched calibration law (R04; council round 2)"; **unchecked**: start-mode DP implementation `C-ENG:TDP_E` "PROVED (by this seat, unchecked)" and `C-DLV:P1-Inventory`, `C-DLV:L2-S3` "AUDITED (code reading)" (§6, T9, T10) | — |

## 4. Core theorem 4 — the run's estimates are consistent (rows 3.6 and 3.5; Thm 10 and its remark)

Masters: `W3-SAMP:C@1.1.4`, `W3-SAMP:LT#@2.0.4`, `W3-SAMP:D@2.1.4`, `W3-SAMP:TR@2.1.4` "PROVED-CHECKED" (each); start input
`W3-START2-R:IF-START@1.0.0` "PROVED-CHECKED; council R2, …" (the card still cites `W3-START2:IF-START`, now
SUPERSEDED-VALID); `W1-N1:Thm-N1@1.0.0` "PROVED-CHECKED".

| Assumption | Track | Status or dossier | Song–Liang (2015) |
|---|---|---|---|
| Rows i.i.d. Gaussian; (S1), (S2); (A2) fixed signals; (A3) population floor | B | B7, B1, B2, B4, B5 | as rows 1.2 and 3.1 |
| (A4) visibility | B | B8 | Condition 5, p. 958: ours implies it in every regime |
| **(A5) no leakage** | B | **B11 — narrow; flagged** | no condition of this kind |
| Start law is sampled exactly and its normaliser is exact (START) | A | **unchecked**: "PROVED (candidate)" (`W1-N1/STATEMENT.md:75`); no registry claim (§6, T6) | — |
| Coded moves realise the stated kernels; order uniform, state-independent (KERNEL) | A | **unchecked**: "PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT" (`W1-N1/STATEMENT.md:76-78`); `SOP:OB09` gate "PROVED (candidate)" (§6, T7) | — |
| Calibration record is a function of the data and the calibration streams (CAL) | A | **missing**: named premise, no code-reading claim (§6, T5) | — |
| Frozen-run identities (T12) behind the unbiasedness and the round path law | A | `W1-N1:P@1.0.0` "PROVED-LOCKED"; `SOP:TH110@1.0.0` "PROVED-LOCKED (all parts (i)-(iv), wave 1); not adopted …" — below the current label (§6, X1) | Del Moral's identity is classical; SL do not use it |
| GUARD-W; blocks ≤ 16 | A | as row 3.1 (§6, T1, T2) | — |
| Start mass → 1 on S₀ (P-START); non-collapse (NC_r) | A | `W3-START2-R:IF-START` (above) and `W3-SAMP:C` (C-v) — **both only under (A5)** | — |
| D_r·π₀(S₀) → ∞ (P-OVL; Thm D clause) | A | **missing (one line)** from P-START and the production budget (§6, T8) | — |
| Global overlap max π/π₀ = o(log n) (P-OVL∞; alternative route TR only) | A | **missing**: `W3-SAMP/STATEMENT.md:183` does not claim it from conditions on (X, θ*) (§6, T11) | — |
| Exact arithmetic, ideal uniforms, stream independence, measurability (S5) | M (MEAS: A) | MEAS: `W1-N1:B@1.0.0` "PROVED under the named premises of STATEMENT §2 — cross-family checked … and council-passed …" | — |
| Row 3.5: pooled evidence unbiased | A | `W1-N1:Thm-N1` (above); `W3-READER:PoolZ` "PROVED (by this seat, unchecked)", **not in this registry** (§6, X5) | no statement of this kind |

## 5. Core theorem 5 — the rate cannot be improved (row 1.3; Thm 3)

Masters: `W3-PSHARP:B@1.0.0`, `W3-PSHARP:A@1.0.0` "PROVED-CHECKED; council R2, …"; `W3-PSHARP-R:AE@1.0.0`,
`W3-PSHARP-R:A2C@1.0.0` "PROVED-CHECKED; council R2, …".

| Assumption | Track | Status or dossier | Song–Liang (2015) |
|---|---|---|---|
| Part (a): none (every design, every response) | — | deterministic property of the prior and the Occam factor, proved in `W3-PSHARP:B` | no lower bound in SL |
| Part (b): Gaussian errors, s₀ fixed, energy and coefficient bounds | B | B1, B3, B4 | — |
| Part (b): orthogonal or i.i.d. N(0, 1) null columns | B (witness) | B12: a lower bound needs one design; nothing to defend | — |

---

## 6. Track A — check of the helper's inventory, gaps, and the Tier B order

**Check.** I compared `work/A_inventory.md` with the statements and the registry for every A item of rows 3.1, 3.5, 3.6 and
for the edges it flags. The A / B / M classification is right, including its two borderline calls (data laws are B; the
superset Occam-sum condition is B). The quoted statuses match the sources. Four corrections:
1. **Two buckets read higher than the quoted status.** `P:M5-COMPOSITION` (`SOP:TH05.0`: 'T38-(0) "PROVED (SF: VERIFIED
   (W3-VT38E); XF: VERIFIED* (A-REV5))"; …') and `P:DERANDOMISE` (`C-MIS:LemDR`: "R02 VERIFIED; council R07/R08 PASS") are
   bucketed "proved-and-checked" but carry older labels, not "PROVED-CHECKED". No mathematical concern; a relabelling
   question for the recorder.
2. **P-START and NC_r are "proved-and-checked" only under the design condition (A5) (no leakage).** The track-A chain of
   row 3.6 is therefore closed only on designs inside B11.
3. **Drift D2 (row 2.1) resolved.** Cor 9C does use `W3-DIST:DIST-C`, but only its deterministic clauses (C-0), the
   threshold form of (C-i) and (C-ii)(α) (`W3-DIST/STATEMENT.md:291-303`; "Corollary C = DIST-C (C-0), (C-i), …", `:131`), which "need no sampler premise" (`:314`). So row
   2.1 carries EX-A and the ledger code fact, not the sampler contract. The registry edge `Cor-C → DIST-C@stmt` should
   name those clauses; the card's "not used by Cor 9C" should read "delivery clauses not used".
4. **One object is missing from the inventory** because it is a claim, not an assumption id: the frozen-run identities
   T12 (item X1 below).

**Tier B tickets: the 13 unchecked or missing items, ordered by the core row they block** (HQ ruling 3). "Blocks" = the
row cannot be called fully checked while the item is open. Lemma statements are the helper's (§4 there), which I
endorse unless noted.

| # | Item (bucket) | Blocks | Smallest lemma (statement · route) | Lean |
|---|---|---|---|---|
| T1 | GUARD-W (missing) | 3.1, 3.5, 3.6 | **GW.** Every guard check reads only the clock, draws no uniform and changes no setting; a run that no check stops performs exactly the potential computation; a stopped run returns no estimates. · Code reading of all guard sites, extending `W3-SAMP:PC`. | no |
| T2 | Blocks ≤ 16 (missing, partial) | 3.1, 3.6 | **BLK.** The coded partition is a function of X only and every block has at most B = min(⌊√n⌋, ⌊√p⌋, 16) columns. · Packing invariant + CC7; code reading. | packing part |
| T3 | OP-LS0 (unchecked) | 3.1 | **OPC.** In the shipped configuration every completed sampler run executes LS0 from the returned start mode with complete scans, and every LS0-scored model enters the final comparison. · Re-check `W1-GEN:L5` against `cpp/v3_core.cpp:394-404, 465-479`. | no |
| T4 | Start-table encoding, (H1) strengthened (unchecked) | 3.1 | **ENC.** The start tables and index maps are built as Lemma E4 assumes. · Code reading of `cpp/v3_start.h:76-151`; register as a code-check claim. | no |
| T5 | CAL (missing) | 3.5, 3.6 | **CAL-C.** The calibration record is a measurable function of the data and streams 0–9; no final stream is read before it is frozen. · Code reading of `v3_calib.R:144-183`, `v3_fit.R:154`. | no |
| T6 | START (unchecked) | 3.5, 3.6 | **START-X.** Under exact arithmetic and ideal uniforms, the start sampler returns S with law γ₀/Z̄₀ on Ω and reports Z̄₀ = Σ_Ω γ₀. · Backward sampling from the (block, size) table is exact for a block-product weight under a global size cap; re-check N9 Claims S, Z. | yes |
| T7 | KERNEL (unchecked) | 3.5, 3.6 | **KER.** Each coded move is a π_φ-reversible kernel on Ω and the round order is uniform and state-independent. · Detailed balance per move type + the N9 code reading. | math half |
| T8 | P-OVL (missing, one line) | 3.6 (Thm D clause) | **OVL.** Under the production budget and P-START, D_r·π₀(S₀) → ∞ in probability on 𝒜. · D_r ≥ max(2500, n, p)(L + 6) and π₀(S₀) → 1. | yes |
| T9 | Start-mode DP implementation (unchecked) | 3.1, delivery clause | **TDP.** The tie-aware DP returns the lexicographically first maximiser of the start law under the size cap, within its stated cost. · Second-seat re-check of `C-ENG/lemmas/TDP_E.md`. | yes |
| T10 | P1 inventory and case S.3 (audited by reading only) | 3.1, delivery clause | **Re-audit.** Second-seat code reading of `C-DLV/STATEMENT.md:52-53`, `lemmas/L2_degenerate.md:37-67`. | no |
| T11 | P-OVL∞ (missing) | 3.6, remark route (TR) only | Not a Tier B item: it needs a new key lemma (a bound on max π/π₀). **My recommendation differs from the helper's:** keep Thm TR in the remark with P-OVL∞ named as an open premise, because TR is the only recorded route to the printed PIPs that does not need (A5) (HQ agreed, 11-16). Track D adds a caution (checked, AUDITCALC_check_opus.md §2): as n → ∞, P-OVL∞ fails where a null leaks given the truths of its own block (π₀(S₀) is then below every power of n), and TR's finite bound is empty there too; TR does not reach AR or BLK. | no |
| T12, T13 | `P:SCORE-EXP`, `P:START-CENTRE` (unchecked, route only) | none (reached only through the historical route `W1-GEN`) | No proof ticket. Bookkeeping: record that the core rows do not use them. | — |

**Further open inputs that are claims** (not among the 13; same Tier B treatment suggested, after T1–T8):
- **X1. Frozen-run identities.** `W1-N1:P` "PROVED-LOCKED", `SOP:TH110` "PROVED-LOCKED (all parts (i)-(iv), wave 1); not
  adopted …". Used by the unbiasedness theorem (row 3.5) and by the round path law in `W3-SAMP` (ST-c, TR). Lemma: restate
  T12 (i.a)–(i.c), (ii) and (R3) for the code of record and line-check once under the current protocol. Lean: yes.
- **X2. `W3-POST:Prop-LB`** "PROVED (by this seat, unchecked)" (row 1.1, expectation display). Lemma: Prop-LB follows from
  the checked `W3-PSHARP:B` (one line; the reader version already says so).
- **X3. `W3-POST:Lemma-1a'`** "PROVED (by this seat, unchecked)" (row 1.1, expectation display). One line check.
- **X4. Registry edge `W3-DIST:Cor-C → DIST-C`** (row 2.1): retype to the deterministic clauses (correction 3).
- **X5. `W3-READER:PoolZ`** (row 3.5): two-line proof by linearity; line check and registry row.

**Lean targets (my ranking, smallest first):** deterministic posterior summaries (`C-PACK:SL0`); the prior-odds lower
bound of Thm 3(a) (`W3-PSHARP:B`); T8; the staying lemma `W3-SAMP:ST` (a)–(b); the minorization (TR-a); T2's packing
invariant; T6; X1; T9.

## 7. Track B — summary

Twelve dossiers and the summary table (assumption × Song–Liang × our designs) are in `TRACK_B.md`. Verdict counts:
the comparisons are stated by regime (v1.4). Uniform in every regime: B1 and B3 are the same as theirs; B8 implies
their Condition 5; they have no condition of the kind of B9 (only an informal remark), of B10's local regressions, or
of B11. Regime-dependent: B2 (two ranges, two comparators), B4 (reading of their β*), B5 and B6 (their cap r̄_n), B7
(centring), B10's floor. None of the differences matters for our designs in cores 1–2. Record of the three blind
reviews behind this: `TRACK_B.md` §T (audit 1), §T2 (supplement), §T3 (audit 2). Two short implications are proposed as
lemmas for the report: Thm 9 (A3) ⇒ their Condition 1, for every r, with δ = √(3/8)/L and M = log 2 on standardised
predictors (dossier B7; checked, AUDITCALC_check_opus.md §4);
Thm 6 (A3) ⇒ their Condition 5 (dossier B8). Candidate corollaries in primitive terms: Thm 2 and Thm 9 already are (their
"for instance" and "Example" lines); Thm 6 for block-diagonal Σ with one truth per block (B9, short proof expected);
Thm 10 for Σ = diag(Σ_{S₀}, Σ_N) (B11).

**Track C (internal; `track_C/RESULTS.md` @ 4f0f9a82, Owls part, 19 designs).** No inside/outside verdict of `TRACK_B.md` is
contradicted. Confirmed: floors inside and rising with n everywhere (B5, B6); beta-min and Occam proxies inside (B4,
B6); leak set bounded for IND, AR ≤ 0.8, fixed blocks and S6, and the whole design for S5 and fixed-correlation factors
(B9). Added: visibility fails at the population level for a pervasive factor with mixed-sign truths and for a
riboflavin-like real-data design (B8), so a typical real-data user may be outside core 3 while inside cores 1 and 2;
at (n, p) = (200, 2000) the sample proxies of visibility and of the O(log n)-set floor are near 0, trend pending (NOTS).

## 8. Method version per study (HQ alignment item)

Registry method pin of the core theorems: rows 3.1, 3.5, 3.6 — "v3.1 as merged, main 4676af6" (`W2-APP:POST`,
`W2-UNI:F-UNI`, `W3-SAMP:C`), code read at main 2252d57 (`W3-RM:RM-0`), with `ls0 = TRUE`, `ls0_cap = "ell_n_plus_mode"`,
`ls0_tie_dp = TRUE` (`W3-RM2/STATEMENT.md:57-58`). Rows 1.x and 2.1 (Thm 9, 9B) have no method pin: they are about the
posterior, not the code. Engineering's report was checked against the files below.

| Study | Method as run (evidence) | Verdict |
|---|---|---|
| 2,400-fit study | v2.2.1, frozen (`Docs/PLAN.md:38`; core `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/`). No LS0: no file in that tree contains "ls0" (grep, this worktree). Preflight memory-only (`…/v2_2_1/core/v3_fit.R:16`). **Engineering's report confirmed.** | **APPLIES UP TO** no LS0, no tie-aware start mode, no tier-1 grid fallback (`Theory_work/Pause_2026-11/RERUN_SPEC.md:22`). Rows 1.x, 2.1: unaffected (same target; score files byte-identical, `RERUN_SPEC.md:23`). Row 3.1: not covered (its reported model is the post-LS0 one). Rows 3.5, 3.6: island code unchanged, but identity of Ẑ and PIPs with v3.1 is "expected" from a diff, not from a run (`:24`); the study's headline MPM uses plain PIPs (`:13`), which Thm 10 does not describe. |
| P6 | v3.1 core, `git archive` of main 2252d57 (`W3-P6/DESIGN.md:10-12`; `LOG.md:14-15`). **LS0 on**, wide base cap `options(v3.ls0_ell = ell + K)` (`scripts/p6_fit.R:55`); hours = 22.5 (`configs/b1_tasks.tsv:1`); LS0 worst-case charge active (`p6_fit.R:108`). `smoke_v3_tasks.tsv` is the v3 driver smoke test (`LOG.md:40`). **Engineering's report not confirmed for P6 (Engineering reconciliation pending).** | **APPLIES UP TO** the wide LS0 cap, a documented testing option; the shipped-cap outcome is re-derived and validated on paired fits (`DESIGN.md:25-33`). The P6 designs are outside row 3.1's leakage assumption (B9): P6 tests beyond the theorem, by design. |
| SCR N1 | Core copied from main 2252d57 (`W3-SCR/LOG.md:6`) = the pin of `W3-SCR:A1`. Default settings (not verified line by line). | **APPLIES as run** (row 3.7, not a core row). |
| W3-SCALE | v3.1 records against revision D = 6866f57 (`origin/theory/W3-SCALE:…/CHECKPOINT_2.md:20-22`); revision D charges the LS0 preflight after setup (`:13`, `:30-31`). | v3.1 records: **APPLIES as run**. Revision D: **APPLIES UP TO** the output-identity note (card row 4.2: "no theorem, no registry row") and the preflight change, which touches only the allocation premise of the delivery clause. |
| Overlap rung (10⁴) | Planned, not run: "v3.1 law (N = p = 10⁴, R′ = 4) against fixed N = 2,500 (R′ = 16)" (`…/P1M/EXPERIMENT_PLAN.md:109`). With the default 24 h, the v3.1 preflight refuses at p = 10⁴ (`Theory_work/Wave3/HQ_NOW.md:33`), so the arm must record its `hours` and LS0 preflight setting. | v3.1 arm: **APPLIES as run** once that setting is recorded. Fixed-N arm: **APPLIES UP TO** N_e and R′: rows 1.x, 2.1 unaffected; row 3.1 holds for every N_e and R′ (`W3-RM:RM-0` scope); rows 3.5, 3.6 hold for any N_e (`W3-SAMP/STATEMENT.md:43-46`) but are stated for R′ = 4 (`:42`). |
| 1M | Planned, not run. The plan changes the law: fixed N per island (`EXPERIMENT_PLAN.md:39`) and a new block rule above about 150k columns (`:232`). | Rows 1.x, 2.1: **APPLY** (prior and score unchanged). Row 3.1: **APPLIES UP TO** the block rule, if it stays a function of X with blocks ≤ 16 (`W3-RM2/STATEMENT.md:216-217`; plan item T-PART, `:244`). Rows 3.5, 3.6: **DO NOT APPLY as recorded** until T6, T7 are re-established for the modified engine. |

**Recommendation on a v3.x rerun of the 2,400-fit study: partial, and only if the paper reports the method's reported
model.** (1) No rerun is needed for any theorem, nor for the posterior rows 1.x and 2.1. (2) To report "the model the
coded method prints", LS0 has to be added: it is deterministic and reads no uniforms (`W3-P6/DESIGN.md:26`), so it can be
computed after the fact on the 1,200 data sets and combined with the stored pre-LS0 model; no sampler rerun.
(3) A full rerun is needed only if the paper states that every reported number is v3.x output, since the equality of
Ẑ and PIPs across versions is an expectation from a diff. (4) Independently of the version, the study's designs S2–S6 are
outside Thm 10 (B11), so the study illustrates rows 1.x, 2.1 and 3.1, not row 3.6. (5) P6 needs no rerun.

## 9. Reach of the printed-estimates theorem (row 3.6) — presentation, not a correctness event (HQ ruling)

The card row names "Theorem 5's visibility and no-leakage conditions", so the statement is correct and does not
overclaim. Its reach, plainly:
- **Covered by Theorem 10 (printed PIPs, MPM, Ẑ consistent):** designs in which every null column is uncorrelated with
  every true column up to C n^{-1/2}, given any ≤ 15 others. Of ours: **S1 and IND.**
- **Not covered by Theorem 10:** S2–S6 of the 2,400-fit study, all of P6, and AR, BLK, FAC of the 1M plan.
- **What still holds there:** Theorem 6 (the reported model is S₀) on S2–S4, S6, AR, BLK; row 3.5 (the evidence estimate
  is unbiased) on every design; the posterior theorems (cores 1, 2) on every design. What has no theorem there: that the
  printed PIPs, MPM and Ẑ are close to the exact posterior quantities.
- **Why this is not a proof artefact everywhere:** on AR and BLK, as n → ∞, the start mass on S₀ falls below every power
  of n (`W3-START:NEC-b`, "PROVED-CHECKED"; `TRACK_D.md` §0; checked, AUDITCALC_check_opus.md §1), so the present route
  cannot be stretched to them. At the 1M plan's sizes (n ≤ 400, p = 10⁶) that result is silent.

Nothing else looks false or unreasonable. Explicit constants from the proofs are conservative; the audit judges the
qualitative conditions only (HQ ruling 1).

## D. Track D — sharpness and improvement candidates (summary; full text in `TRACK_D.md`)

| Core | Assumptions | Conclusion |
|---|---|---|
| 1 | s₀ fixed is NECESSARY up to √log n; the floor off S₀ is already replaced (Thm 1′); Gaussian rows and the floor's set size are LIKELY WEAKENABLE; the rest UNKNOWN | rate OPTIMAL on the witness designs; GAP of √log n on a general design; GAP on random designs (in probability only) |
| 2 | (A4) NECESSARY in some form for the fixed-design interface (`W3-DIST:NEC`), LIKELY WEAKENABLE in window; display (iii) hides an s³ | radius better than Song–Liang's at polynomial p; GAP in form (log n, not log p); Thm 9B OPTIMAL |
| 3 | visibility NECESSARY for the start route; per-truth leak level LIKELY WEAKENABLE; \|Q\| ≤ n^b UNKNOWN beyond the route | near-optimal for this route; scope (factors) is decision D1 |
| 4 | no leakage LIKELY WEAKENABLE to a group-relative form, which is NECESSARY for start concentration | rate GAP closed by a recorded result (reader swap); reach is the open issue |
| 5 | none (a) / witnesses (b) | lower bound on every design: open rider, not ranked |

Ranked candidates (gain · cost · kill budget in `TRACK_D.md` §2):
1. **Group-relative no-leakage** (HQ's #1): rows 3.6 and 3.3 gain bounded-group designs (S3, S4, S6). **It does not
   reach AR or BLK.** Opus ≈ 3 days, Tier A with one small key lemma; fallback Tier B.
2. **Check X**: Theorem 2 from the omitted-variables master — expectation rate on Gaussian designs, parameters free to
   vary with n. Opus 1 day, Tier B.
3. **Sub-Gaussian rows for Theorem 2**, reusing `W3-DIST:B2`. Opus ≈ 2 days, Tier B.
4. **Theorem 9 bundle** (items 1, 8(a) + 10, 9 of the unharvested list; order set by card 13). Opus ≈ 3 days, Tier B.
5. **Printed estimates on leaky designs** (what AR needs): a non-collapse lemma for the tempered sampler. Tier A, high
   risk; feasibility note first.

**HQ final order (2026-11-16; supersedes the earlier #2 → #3 → #1):** #2 check X (kill 1.5 days) → #3 sub-Gaussian
rows for Theorem 2 (kill 3 days) → **#5′ store-restricted clause (kill 3 days), which replaces #1.** All post-freeze, from
Sat 11-21; the independent check of my computations has confirmed them (none refuted), so the three are unblocked.
#1 and #4 are deferred. No G1/G2 gate: the printed
PIPs, MPM and Ẑ on AR stay NO-GO and scoped as worded, with AR covered by Theorem 6 and row 3.5.
- **#5′** (`TRACK_D.md` §5a): on every design inside Theorem 6 (S2–S4, S6, AR, BLK), the PIPs, median model and evidence
  sum computed from the returned list are within 1 − π(S₀ | y) of the truth. Tier B, 1–2 Opus days; two named links to
  close. These are functions of the output, not printed fields.
- **Alignment (HQ):** once #5′ is proved, Engineering's overlap-rung and 1M analysis reports these store-derived
  summaries next to the printed fields. Post-processing only, no algorithm change, so the theorem covers numbers
  reported on AR and BLK.

X1–X5: X1, X3, X5 are lemmas (Tier B); X2, X4 are relabellings (recorder). The computations on which a verdict
depends, with the checker's result for each, are listed in `TRACK_D.md` §4.

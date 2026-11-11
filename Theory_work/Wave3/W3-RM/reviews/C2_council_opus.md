# C2 — Council round 2, seat B (Claude seat) — W3-RM, STATEMENT v1.2.1

Reviewer: Claude Opus 5.5, effort high, no subagents, 2026-11-09. Brief: `reviews/COUNCIL_BRIEF_R2.md`.

**Process.**
* I did not read REPORT.md or LOG.md.
* I did not run `citecheck.py`. I read the script's output, `reviews/CITECHECK.txt:1`: "280 extracted citation ranges,
  0 failures …; 32 token assertions, 0 failures; 10 quoted statuses, 0 not found verbatim". I treat this as a range and
  token audit only.
* I did not read the parallel seat's round-2 reply (`reviews/C2_council_astra.md`).
* I read every file of the package, the reused source lines named in the brief, and the code, and re-derived each new
  step myself. Only after that did I consult R01–R08 and the round-1 replies.

**Concurrency note.** `STATEMENT.md` was modified at 19:07, while I was reviewing. One line changed: §6, line 269,
marker [C2-A2]. I review the file as it now stands. That edit resolves an inconsistency I had noted on first reading
(see §5 below).

## 1. Gate verdicts

**G1 Correctness of every step — PASS.** I re-derived every new step and found no false one.

* **RM-0(a)** (`lemmas/L0_core.md:28-37`), checked against `cpp/v3_engine.h:379-415`.
  * The centre lies in 𝓛. At T ∈ 𝓛 ∖ {S₀}, NA at T ∖ {e} gives F(T ∖ e) > F(T), so a strict improvement exists.
  * Every swap that keeps S₀, (T ∖ e) ∪ l, is beaten by T ∖ e (NA, |T ∖ e| < K).
  * Every move that removes a truth is beaten by T (TL).
  * So the best neighbour is a deletion of an extra, strictly. At S₀ there is no strict improvement, so the code takes
    the else branch at `v3_engine.h:413-415`.
  * The cap test `A.moves >= ell` (:409) cannot fire, because ell = ℓ_n + |S̃₀| ≥ |S̃₀ ∖ S₀|.
  * The archive corollary reads off :407-415 correctly.
* **RM-0(b)** (`L0_core.md:39-57`).
  * The pathwise inclusion holds and the common good event 𝒢_n is well defined.
  * The step "π(S₀) > ½ ⇒ S₀ is the strict F-maximiser on Ω" is correct, because π is the posterior on Ω.
  * The Markov step is correct.
  * Run parameters enter LS0 only as labels: tier is used for event labels, and ls0_ell = b$ell is a function of (n, p).
    So the LS0-scored set is a data function, as claimed.
* **Lemma NA-F** (`lemmas/L2_NAF.md:97-129`).
  * (2.1) holds because w ∈ V_l ⊆ 1^⊥.
  * P(E₁ᶜ) ≤ |𝒰|·2e^{−a²/2} = 1/log n.
  * E₂ ranges over at most p distinct projectors (one Π_Q plus p − q others), with 2d + 3x ≥ d + 2√(dx) + 2x.
  * The cross term is 2√(a²·ρ²G) = o(log n).
  * Margin: c_n − (2 log p + 2h log n + o(log n)) ≥ (1 − 2h) log n − 2κ log log n − O(1) > 0.
  * The score conversion goes through LOC2 L0′ (`W2-LOC2/lemmas/L1_toolkit.md:37-42`), whose rate condition
    ω_n log n → 0 holds for polylogarithmic q.
  * N-loc: a ⊥ b, ‖u_T − u_N‖² = 2 − 2(1 + t²)^{−1/2} ≤ t², and |𝒰_n| ≤ p2^{ν_n}.
  * Special case (c) checked: P_T x_l = P_{S₀} x_l for l ∉ Q, and (I − P_T)x_l = (I − P_{S₀})x_l for l ∈ Q ∖ T.
* **Lemma τ** (`lemmas/L1b_rss.md:21-34`), from [GEN-L1] (1.1).
  * AM–GM gives 2σ√(n−1)√Λ ≤ (n−1)τ².
  * σ²(2√((n−1)n^{1/3}) + 2n^{1/3}) ≤ 4τ²n^{2/3}.
  * The ratio bound follows from log u ≤ u − 1 with the τ-floor at A′.
* **Lemma B2τ** (`L1b_rss.md:36-67`). I read the whole of GROW `L3_sandwich.md`: NEG enters only at (3.3) (:40-52)
  and at Step 2(b) (:86-93). The new facts needed all hold:
  * Λ_U − Λ_{Ũ_b} = ‖Πμ‖², so τ²_{Ũ_b} ≥ τ²_U(1 − 16η log n/(n−1)).
  * Each U_{s−1} has size ≤ 15 and contains S₀ ∩ C_b, so (L_b^τ) applies, with τ² non-increasing along nested sets.
  * ‖Πε‖² ≤ σ²dW_b ≤ τ²_U dW_b, which is the correct direction for an upper bound.
  * σ/τ_U ≤ 1 in the junk step.
  * ϑ″_n log n → 0.
* **Lemma B2's |Q| delta** (`lemmas/L1_fixed.md:126-138`). |Q| enters GROW L3 only at :36-38, :64-72, :78-79 and
  :88-93. The ladder bound discards k₀^{−ε₂/(1+ε₂)} ≤ 1. Junk exclusion needs only log k̃ = o(log n).
* **Lemma B3** (`L1_fixed.md:146-164`).
  * The bound t_n + h_n² ≤ C₁(A, s₀)(q + log n) follows from the actual-cardinality definitions of LOC2 L0′.
  * Λ ≥ 4σ²(2h² + t) is exactly what Λ − 2σh√Λ − σ²t ≥ Λ/4 requires.
  * (BM-Q) supplies it. This correctly addresses LOC2's own caveat that BM-∞ is not enough at polylogarithmic size
    (`W2-LOC2/lemmas/L1_toolkit.md:33-36`).
* **SAND-R** (`lemmas/L3_SANDR.md` §§3–7), checked line by line against GROW `L6_random_AR1.md:169-389` and UNI
  `L2_k0.md:79-133`.
  * Selection removal: population a, d = O(n^{−2}) (L3b: O(r_n)), z₀ = O(n^{−1/2}) via (L-gain-R), and ‖R⁻¹‖ ≤ C from
    the Schur floor alone. The recursion gives |z_U − z₀| ≤ Cg², hence |h_U − h_{U₀}| ≤ Cng²(h + g²).
  * Spherical tail: conditioning is on (W_D, ε), and the innovation is independent of (W_D, ε). ‖α‖ ≤ Cn^{−1/2} and
    ‖β_j‖ ≤ √15/c, so ‖m‖ ≤ C on CN_D.
  * Counting: p·N_ref·(k/p)n^{−1/2}e^{C√log n} = k n^{−1/2+o(1)}.
  * Ladder: k ≤ k₀ + 16J(t_n(k)), J > m_i/32, O(log n) rungs.
  * Truth inclusion uses TV δ² ≥ Na₀²/4. Junk exclusion has margin ¼ log n − log 2k₀ > 0.
  * The construction matches the source exactly; the only change is that the geometric inputs are replaced by
    (L-gain-R), (L-loc-R) and N_ref = n^{o(1)}.
* **SAND-R′** (`lemmas/L3b_rate.md:17-33`). ω_n = C[√(n log n)r_n² + (log n)^{3/2}n^{−1/2} + nr_n⁴ + (log n)²/n] → 0 if
  and only if r_n(n log n)^{1/4} → 0, as stated.
* **D-loc** (`lemmas/L4_formR.md:62-74`), checked against LOC2 `L2_NAR.md:22-36`.
  * Frames: ψ_{N,l}, at most p2^{ν_n} of them, so log N_n ≤ log p + o(log n).
  * Atoms: e_v for v ∈ Q, with Var = 1.
  * With λ = β̄_T − β̄_N, r − Σλ_vW_v = e_{T,l}.
  * (R3) is the variance hypothesis.
* **p = 1 branch** (`L4_formR.md:88-95`).
  * D_A = n²/n = n.
  * Q_A = (n − 1)(1 − r̂²(n − 1)/n).
  * w(1)/w(0) = 1/(2p − 1) = 1.
  * r̂² → θ²/(θ² + σ²).
* **E4** (`lemmas/L5_E4.md`), checked against `cpp/v3_start.h:195-304`.
  * mb, arg, M and kbest are as claimed.
  * Leaves accept only r = 0, and `trunc` is set only after `bestS` has been set (:290).
  * The per-block IN/OUT masks in `mode_tie_dp` give (4.2), and the invariant argument ends at S = IN.
  * `st.blk`/`st.pos` are set as inverse maps (:79-80).
  * Integration: `v3_core.cpp:400-404` (option parsing), :465 (gate), :469 (call), :473 (cap) and :476 (search).
    `v3_engine.h:379-382` emits the centre. `v3_run.R:88-101` holds the defaults. `v3_fit.R:120-131` is the exact branch.
* **GEN (C6) satisfies RM-F** (`SHARPNESS.md:69-86`), checked against GEN `L7_counterexample.md:14-36`.
  * (W1) gives the floors, η = 0 and special case (c) of NA-F.
  * BM-Q holds with |Q| = s₀ + d_n.
  * One intermediate justification for (V) is mis-worded, though the conclusion is right (finding 1).
* **Numerics recount.** Every figure in SHARPNESS §6 matches SUMMARY_SHARPNESS:
  * 296/300; 59 + 1 and 58/60;
  * 138/140, 89/140 and 169/180;
  * 418/420, 354/420, 240/240, 7/33/109/60 and 208/209;
  * 179/180, 90/180, 178/180, 171/180 and 95/180.

**G2 Hypotheses used = hypotheses stated — PASS.** For each bridge lemma, the hypotheses it lists are those its proof
uses:
* B1/B1′: three conditions with identical quantifiers.
* B2τ: (G3a), (V_b) with M_n → ∞, (L_b^τ) with η < η_A, (L-feas), log|Q| = o(log n), energy, and p ≤ n^A.
* B3: (FL-Q), (BM-Q), polylogarithmic q and q ≤ K.
* B4: (N-χ) and (FL-Q).
* NA-F: (FL-Q), (N-D)(i) and polylogarithmic q.
* SAND-R: (FL-R) on sets of size ≤ 16 + s₀, (V-R), (L-gain-R), (L-loc-R) at rate r_n, (L-size) and (L-feas).
* B8a: (N0), (N1) and (D-R). B8b: the floor on Q ∪ {l} and fixed θ_lo. B9: (T1-R), with p = 1 handled directly.

The input map (`STATEMENT.md:207-217`) now carries the (T1-F) component edges and the (L-feas) → |Q| ≤ K edges added
after round 1. Surpluses are declared: the Q ∪ {l} part of (FL-R) is unused by B7, and η is unused in Form R. One small
surplus remains in the bridge table: row (B2) lists (FL_b), which includes (FL-Q), although B2/B2τ consume only (G3a)
(finding 4).

**G3 No hidden assumptions — PASS.**
* The partition enters only as "X-measurable, blocks ≤ 16", and in Form F as a deterministic function of the fixed X.
* EX-A, the strengthened encoding premise (H1⁺) and the LS0 configuration are named.
* σ² is fixed in Setting R (`STATEMENT.md:43`).
* No upper spectral bound and no growing-set floor is used by SAND-R.
* The noise-independence conditioning is explicit: SAND-R §3 [R04-F1] and §5.
* Edge cases are covered by conventions: Q = S₀ = [p], Q = [p] with K = p, η = 0, ρ_n = 0, and p = 1
  (`STATEMENT.md:116-117`; `L2_NAF.md:93-95`; `L3_SANDR.md:227, 287-301`; `L4_formR.md:88`).

**G4 Cited lemmas have adequate status — PASS.**
* Statuses are quoted verbatim, and I spot-checked them against their sources:
  * GROW L2 "VERIFIED-WITH-AMENDMENTS (2)", L3 "VERIFIED", L6 "R07 VERIFIED / R06 VERIFIED-WITH-AMENDMENTS".
  * LOC2 L1 and L2 "VERIFIED-WITH-AMENDMENTS".
  * UNI L2 "PROVED (by this seat, unchecked)" with R02 "VERIFIED-WITH-AMENDMENTS".
  * DLV "PROVED (by this seat); R04 VERIFIED-WITH-AMENDMENTS", now quoted in `STATEMENT.md:256-258` and
    `L0_core.md:17-18`.
  * FAC-PK "PARTIAL relative to the brief; (P1)–(P5) on the exact-Gram stage: PROVED-CHECKED".
* Nothing is upgraded: ticket-level lemmas remain "PROVED (by this seat, unchecked)", each with its check record.
* Every new lemma has a cross-family check on file:

  | lemma | author | cross-family check |
  |---|---|---|
  | RM-0, B1–B4, NA-F | Claude lead | R03 (Codex) |
  | Lemma τ, B2τ, B1′, D-loc, B8, L7 | Claude lead | R06 (Codex) |
  | SAND-R | Codex | R04 (Claude) |
  | SAND-R′ | Claude lead | R07, R08 (Codex Astra), which re-derive the four error terms (`L3b_rate.md:3-7`) |
  | E4 | Claude lead | R05 (Codex), with numerics |
  | h < ½ budget, p = 1 branch | Claude lead | R08 |

**G5 Constants and rates tracked — PASS.**
* NA-F: n₀ = n₀(A, κ, h, ρ-envelope) and C₂ = C₂(A).
* B3: C₁ = C₁(A, s₀).
* Lemma τ: ω^τ_n, ϑ^τ_n and ϑ″_n are explicit, with their log n products → 0.
* SAND-R′: ω_n has all four terms.
* SAND-R tail: the slack exp(C√log n) is explicit, and the §8 limit on relaxing (L-gain-R) is correctly argued.
* Ladder: O(log n) rungs, independent of q.
* The junk margins are explicit in Form F ([½ − η/2 − √(2Aη)] log n) and in Form R (¼ log n).
* The constants are carried through every bridge into the interface properties that RM-0 consumes.

**G6 Fidelity to the method as coded and to the binding program — PASS.**
* The theorem is stated for the shipped configuration (`ls0 = TRUE`, `ls0_cap = "ell_n_plus_mode"`, `ls0_tie_dp`,
  cap 10⁶), and I verified each element in the code above.
* e4 is closed by a code-level lemma under a named, strengthened encoding premise, which `build_tables` actually
  satisfies.
* No design family appears in (C0)–(C2). Families appear only in `L7_examples.md` and `SHARPNESS.md`. Form F is
  partition-free; Form R holds for any X-measurable partition.
* The examples table is honest, and §7.3 explicitly disclaims family-level violation claims.
* The sharpness record keeps (P), (S), (F) and (O) apart, and the round-1 G6 defect is fixed:
  * L2 is now "exploratory; nominal population strength" everywhere: `SHARPNESS.md:51, 166, 169-180`;
    `numerics/SUMMARY_SHARPNESS.md:12-17, 82-84, 123`; `numerics/build_summary.py:131-163`.
  * The four reasons are stated: population vs sample, τ²_∅ = 2, cellwise A, and the Form R leak rate.
* Residual wording NITs remain (findings 2, 3). None makes the record dishonest.
* The one place the result falls short of PROGRAM item 3's "(V) + (L)" is the lattice condition (N)/(D-R). It is
  stated openly (STATEMENT §0, last sentence; §6) and explained (SHARPNESS §4). I count it in the score, not as a gate
  failure.

## 2. Score: **9.1 / 10** (uncapped)

| deduction | reason |
|---|---|
| −0.5 | Beyond \|Q ∖ S₀\| ≈ log n, both forms need a non-primitive lattice / direction-complexity condition, (N-D) or (D-R). It is honestly flagged and its necessity is open, but it is the gap between the target "(V) + (L)" and what is proved. |
| −0.2 | Form R's leakage is fixed-scale: a leak of O(n^{−1/2}) plus a localisation clause, needed only because the partition is data-selected. Form R's entropy budget for (R1) is still o(log n), whereas Form F was widened to h < ½. Both widenings are recorded but not adopted. |
| −0.2 | Residual record and wording NITs: findings 1–6, none affecting a proof. |

Nothing is deducted for correctness, for asymptotic scope, or for the absence of a delivery claim.

## 3. Findings

No FATAL. No MAJOR. No MINOR. **No finding is REQUIRED for a pass.**

1. **NIT (G1/G6, record wording) — `SHARPNESS.md:77-79`.** The (V) verification for GEN (C6) says u_{U,j} is
   orthogonal to every truth k ≠ j "(either k ∈ U, or x_k ⊥ span(x_j, X_U) …)".
   * **Where the stated reason fails.** For j = x′_m, k = 0 (the truth with proxies), and U containing proxies of x₀
     but not x₀ itself, x₀ is **not** orthogonal to span(x_j, X_U), because the proxies are correlated with x₀.
   * **Why the conclusion still holds.** x′_m is orthogonal to every other column, so P_U x′_m = 0 and
     u_{U,j} = x′_m/‖x′_m‖. This is orthogonal to all other truths, and δ²_{U,j} = θ²(n − 1).
   * For j = 0 the stated reason is correct: every other truth is orthogonal to x₀, to the proxies, to the nulls and to
     the other truths.
   * **Fix:** "for j ≠ 0, x_j ⊥ every other column, so u_{U,j} = x_j/‖x_j‖; for j = 0, every other truth x_k ∉ U is
     orthogonal to span(x₀, X_U)."

2. **NIT (G6, sharpness record) — `SHARPNESS.md:166, 182-183`; `numerics/SUMMARY_SHARPNESS.md:123`.**
   * The 2η_A cells (120 runs) are still counted under "nominal η > nominal η_A" and "nominally outside".
   * The file's own note (ii) (`SHARPNESS.md:175-176`) says that in the τ-normalisation of v1.2 those cells sit at
     the nominal boundary, not outside it.
   * The note makes the record honest, but the table and the reading paragraph still pool those cells as outside.
   * **Fix:** label the column "nominal σ-normalised η > cellwise η_A", or report η ∈ {0.5, 1, 2} separately (299/300)
     from 2η_A (119/120). No count changes.

3. **NIT (record) — `numerics/l2_eta.py:1, 11`; `numerics/SPEC.md:3, 40`.**
   * The script docstring still reads "sharpness probe L2: gain just above the threshold eta_A (assumption (L-gain))".
   * SPEC (the pre-registration) reads "simulate just outside each assumption" and "L2 — gain just above the threshold
     η_A".
   * SPEC can stay as the record of intent. **Fix:** add one line in each file pointing to the relabelling note in
     `SUMMARY_SHARPNESS.md:12-17` and `SHARPNESS.md:169-180`.

4. **NIT (G2, table) — `STATEMENT.md:196`.**
   * Bridge row (B2) lists "(FL_b)" among the inputs. (FL_b) = (G3a) + (FL-Q), but Lemmas B2/B2τ use only (G3a)
     (`L1_fixed.md:121-123`; `L1b_rss.md:37-39`).
   * This is a stated-but-unused hypothesis in that row. (FL-Q) is consumed by B3–B5.
   * The same row also leaves "M_n → ∞" and "η < η_A" implicit.
   * **Fix:** write "(G3a), (V_b) with M_n → ∞, (L_b) with η < η_A".

5. **NIT (G6, completeness of the numerics record) — `SHARPNESS.md:167`.** The N1 row reports only the runs outside
   (N-χ). The summary also records one finite-n NA(F) violation **inside** (N-χ): NA(F) held in 59/60, the failure at
   C = 0.5, n = 6400, m = 5 < log n (`numerics/SUMMARY_SHARPNESS.md:135, 152`). This is consistent with an asymptotic
   statement. **Fix:** add "(inside (N-χ): NA(F) held in 59/60)" for completeness.

6. **NIT (consistency) — `lemmas/L5_E4.md:131`.**
   * L5_E4 says "Runs with … `ls0_cap = "ell_n"` are outside the configuration".
   * STATEMENT (C1)'s remark [C1-B4] (`:183-185`) and §6 [C2-A2] (`:268-269`) now cover old-cap runs in the (N-χ)
     sub-case. The coverage is correct: GROW L1.2 with ℓ = ℓ_n ≥ (1 − δ₀) log n ≥ |S̃₀ ∖ S₀|, and the same coded
     centre is used at `v3_core.cpp:469-476` under either cap rule.
   * **Fix:** add "(except as in the (N-χ) remark of STATEMENT (C1))", so that all three places agree.

## 4. Verification of the round-1 findings in the current files

| round-1 finding | fixed? | evidence |
|---|---|---|
| A1 (MAJOR, REQUIRED) L2 mislabelled as (L-gain) violations | **yes** | `SHARPNESS.md:51, 162, 166, 169-180`; `SUMMARY_SHARPNESS.md:12-17, 82-84, 123-125`; `build_summary.py:131-163`. Counts are unchanged and I recounted them. Wording residues are NITs 2 and 3. |
| A2 input map omits T1-F components | yes | `STATEMENT.md:207-209`; `ASSUMPTION_MAP.md:19` |
| A3 L2 seed-count note | yes | `SUMMARY_SHARPNESS.md:6, 84` agree with `l2_eta.py:28-36` |
| B1 DLV status not quoted | yes | `STATEMENT.md:256-258`; `L0_core.md:17-18` |
| B2 FAC-PK PATH read as a success of the shipped LS0 | yes | `SHARPNESS.md:132-135` |
| B3 (T1-F)/(L-feas) edges | yes | `STATEMENT.md:207-211`; `ASSUMPTION_MAP.md:19, 31` |
| B4 old cap under (N-χ); ℓ_n undefined | yes | `STATEMENT.md:45, 183-185`; §6 made consistent at :269 [C2-A2] |
| B5 SAND-R′ cross-family record | yes | `L3b_rate.md:3-7` |
| B6 "fails in general" heuristic; "just outside"; p > n | yes | `STATEMENT.md:270-272`; `ASSUMPTION_MAP.md:52`; `L1b_rss.md:72-76`; `SHARPNESS.md:182-184` |
| B7 σ² fixed in Setting R; η unused by Form R | yes | `STATEMENT.md:43, 85-86` |
| B8 FAC-PK status and its proposed cap change | yes | `SHARPNESS.md:87-98`; `L7_examples.md:90` |

## 5. Observed and resolved during this review

On first reading, `STATEMENT.md` §6 listed `ls0_cap = "ell_n"` runs as unconditionally "not claimed", which
contradicted the (C1) remark [C1-B4]. The edit at 19:07 ([C2-A2], `:268-269`) resolved this. No finding is raised, and
the remaining echo in `L5_E4.md` is finding 6.

## 6. Fitness as the paper's main reported-model theorem

Theorem 3 as stated in v1.2.1 is fit to be the paper's main reported-model theorem.

**What it delivers.**
* A deterministic core: on one common data event of probability → 1, *every* admissible output run reports S₀,
  whatever its seed, N_e, R′ or calibration outcome. The core is cleanly separated from delivery and from the public
  `local_certified` flag.
* Two primitive forms. Form F is partition-free, on (X, θ*) only. Form R is stated for any X-measurable partition, on
  (Σ_n, θ*) only.
* No design family appears in the theorems.
* Premise e4 is discharged at the code level.

**Correctness.** I re-derived every new step and checked the code. All are correct. The examples and the sharpness
record are honest after the round-1 fixes.

**Main limitation.** It is visible and stated: beyond |Q ∖ S₀| ≈ log n the theorem carries the whole-lattice
direction-complexity condition (N-D)/(D-R), not just (V) + (L).

**Most valuable strengthening still missing.** A *path-level* replacement of the whole-lattice event NA(𝓛). LS0 needs
only that, at each set it actually visits, the best deletion of an extra beats the best swap and the best addition.
The N1 probe shows whole-lattice NA failing in half the runs while the greedy path still reaches S₀ in 178/180. That
suggests the proof route, not the method, is the binding constraint. Removing (N), even for |Q| ≤ C log n with
arbitrary C, would make RM-F literally "Theorem 1 + floors + (V) + (L)". The polynomial-|Q| extension (R02 P5,
SHARPNESS §3.2) is the natural second item.

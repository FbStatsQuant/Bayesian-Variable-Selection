# C1 — Council round 1, seat B (Claude seat) — W3-RM, STATEMENT v1.2

Reviewer: Claude Opus 5.5, effort high, no subagents, 2026-11-09. Brief: `reviews/COUNCIL_BRIEF.md`. I did not read
REPORT.md or LOG.md. I read every file of the package, the reused source lines named in the brief, and the code, and
re-derived the new steps myself. Earlier reviews (R01–R08) were consulted only after forming my own view, to avoid
re-raising settled points. Source statuses are quoted, not upgraded. All results are asymptotic by owner decision.

**Process disclosure.** To re-verify the citation check I ran `py -3.13 citecheck.py`. That script **rewrites**
`reviews/CITECHECK.txt` (citecheck.py:227-228); I had not realised this when I ran it. Its output has no timestamp and
was regenerated from unchanged inputs: "274 extracted citation ranges, 0 failures …; 32 token assertions, 0 failures;
8 quoted statuses, 0 not found verbatim", the same counts as the file it replaced. I edited nothing else. The lead may
want to re-run it to restore the file's provenance.

## 1. Gate verdicts

**G1 Correctness of every step — PASS.** I re-derived each new step and found no false step:
* **RM-0(a)** (`lemmas/L0_core.md:26-35`): checked against the code. Because the centre is in 𝓛, NA applied at T ∖ {e}
  gives F(T) < F(T ∖ {e}) for every extra e, so a strict improvement exists at every T ≠ S₀. Every swap that keeps S₀,
  (T ∖ e) ∪ l, is beaten by T ∖ e (NA at T ∖ e). Every move that removes a truth is beaten by T (TL). The best
  neighbour is therefore always a deletion of an extra. With the cap ℓ_n + |S̃₀| ≥ |S̃₀ ∖ S₀| the cap branch
  (`v3_engine.h:408-411`) is never reached before S₀, and at S₀ the else branch certifies (`:413-415`).
* **RM-0(b)** (`L0_core.md:37-55`): the pathwise inclusion, the common good event 𝒢_n and the Markov step are correct.
* **Lemma NA-F** (`lemmas/L2_NAF.md:25-53`), re-derived:
  * (2.1) holds because w = u − v ∈ V_l.
  * The tail bound on E₁ is |𝒰|·2e^{−a²/2} = 1/log n.
  * On E₂, Laurent–Massart with d + 2√(dx) + 2x ≤ 2d + 3x, and at most p distinct projectors.
  * The cross term is 2√(O(log n)·o(log n)) = o(log n).
  * The margin is c_n − 2 log p ≥ log n − 2κ log log n − O(1) > 2h log n + o(log n) because h < ½.
  * Lemma N-loc: ‖u_T − u_N‖² = 2(1 − (1 + t²)^{−1/2}) ≤ t², and |𝒰_n| ≤ p·2^{ν_n}.
* **Lemma τ** (`lemmas/L1b_rss.md:22-34`): the AM–GM step 2σ√(n−1)√Λ ≤ (n−1)τ² and the log u ≤ u − 1 step are correct.
* **Lemma B2τ** (`L1b_rss.md:41-67`): the two places where NEG enters, (3.3) and step 2(b), are the only ones in GROW
  L3 (`C-GROW/lemmas/L3_sandwich.md:40-52, 86-93`; I read the whole file). The facts this needs all hold: τ² decreases
  along nested sets, τ²_{Ũ_b} ≥ τ²_U(1 − 16η log n/(n−1)), ‖Πε‖² ≤ τ²_U·d·W_b, and σ/τ_U ≤ 1. The RSS-normalised
  (t-type) score really does pay for the τ-normalised leak.
* **Lemma B2's delta** (`L1_fixed.md:50-62`): I confirmed in L3_sandwich.md that |Q| enters only at :36-38, :64-72
  (the factor k₀^{−ε₂/(1+ε₂)} ≤ 1 is discarded), :78-79 and :88-93.
* **Lemma B3** (`L1_fixed.md:73-88`): Λ_A ≥ 4σ²(2h_n² + t_n) is exactly what Λ − 2σh√Λ − σ²t ≥ Λ/4 needs.
* **SAND-R / SAND-R′** (`L3_SANDR.md` §§3–7, `L3b_rate.md`): checked line by line against
  `C-GROW/lemmas/L6_random_AR1.md:169-389`.
  * Selection removal (G6:194-215): the population inputs are replaced exactly by (L-gain-R) and (L-loc-R). ‖R⁻¹‖
    needs only the Schur floor on U.
  * Rate (L3b): |h_U − h_{U₀}| ≤ C n g_n²(h_n + g_n²). With g_n = r_n + h_n this is o(1) exactly when
    √(n log n) r_n² → 0, and then n r_n⁴ → 0 as well.
  * Spherical tail (G6:245-294): it conditions on (W_D, ε). The true-column scales are W_D-measurable, and the
    innovation is independent of them. ‖m‖ = O(1) from ‖α‖ = O(n^{−1/2}).
  * Counting: p·N_ref·e^{−t_n(k)/2}·e^{C√log n} = k n^{−1/2+o(1)} because N_ref = (1 + (log n)^κ)^{15} = n^{o(1)}.
  * Ladder: k ≤ k₀ + 16J, and the number of rungs is O(log n) independently of q.
  * Junk margin: ¼ log n − log(2k₀) > 0.
* **B8a, D-loc, B8b, B9 and the p = 1 branch** (`L4_formR.md`):
  * The D0 algebra at p = 1 is right: D_A = n²/n, and Q_A = (n − 1)(1 − r̂²(n − 1)/n).
  * D-loc → (R1)–(R3) matches `W2-LOC2/lemmas/L2_NAR.md:22-36`.
* **E4** (`lemmas/L5_E4.md`), against `v3_start.h:195-305`:
  * (4.1) and Claim T are right.
  * The enumeration accepts only tight leaves, and `trunc` is set only at an accepted leaf (:290).
  * The `mode_tie_dp` invariant (4.2) is right: the per-block IN/OUT masks give exactly "a tight set exists".
  * Integration: `v3_core.cpp:392, 400-404, 465-476`, `v3_engine.h:379-382, 89-100` and `v3_run.R:88-101` say what
    E4 says. The code is unchanged since commit 2252d57 (`git diff --stat` is empty).
* **GEN (C6) satisfies RM-F** (`SHARPNESS.md:69-86`), re-derived from `W1-GEN/lemmas/L7_counterexample.md:14-36`:
  * (V): x′_k is orthogonal to everything else. For x₀, u_{U,0} ∈ span(x₀, X_U) is orthogonal to every truth k ≠ 0.
  * η = 0 for the orthogonal nulls.
  * Special case (c) of NA-F holds, because the proxies' residuals given S₀ are mutually orthogonal.
  * (BM-Q) holds with |Q| = s₀ + d_n = O(log n).
* **Numerics**: I recounted every figure quoted in SHARPNESS §6 from SUMMARY_SHARPNESS. They are all exact: 296/300;
  138/140 and 89/140; 418/420, 209 = 7 + 33 + 109 + 60 and 208/209; 90/180, 178/180, 171/180, 95/180 and 179/180.

The remaining issues are wording (findings 2 and 6), not steps.

**G2 Hypotheses used = hypotheses stated — PASS.** For each bridge lemma, the hypotheses it lists match what its proof
uses:
* B1 and B1′: the three conditions, including the τ-form.
* B2τ: (G3a), (V_b), (L_b^τ) with η < η_A, (L-feas) and log|Q| = o(log n).
* B3: (FL-Q), (BM-Q) and the polylogarithmic size.
* NA-F: (FL-Q), (N-D)(i) and the polylogarithmic size.
* SAND-R: (FL-R) only on sets of size ≤ 16 + s₀, (V-R), (L-gain-R), (L-loc-R) with rate r_n, (L-size) and (L-feas).
* B8a: (D-R) and the floor on Q ∪ {l}. B8b: the floor and fixed θ_lo.

The surpluses are honestly recorded: the (FL-R) floor on Q ∪ {l} is unused by B7, and η is unused in Form R. The one
mismatch is documentary: the input map in STATEMENT §4 omits that (T1-F) supplies ‖μ‖² ≤ Mn, p ≤ n^A and BM-∞ to
B2–B5. It also omits that (L-feas) supplies |Q| ≤ K to B3–B5, B8 and RM-0 (finding 3). The lemmas themselves state
these inputs correctly.

**G3 No hidden assumptions — PASS.**
* The partition is used only as an X-measurable partition with blocks of size ≤ 16. The Form F proof uses it as a
  deterministic function of the fixed X (`L1_fixed.md:113`).
* Exact arithmetic (EX-A), the encoding premise (H1⁺) and the configuration are named.
* No upper spectral bound and no floor on growing sets is used in SAND-R. The (T1-R)-only H0 checks are separated out
  (`L3_SANDR.md:82, 141-151`).
* One small omission: Setting R in STATEMENT §1 (:40-42) does not say that σ² is fixed. SAND-R §1 does, and Setting F
  does (finding 7).

**G4 Cited lemmas have adequate status — PASS.**
* I spot-checked the quoted statuses against their sources: GROW L3 "VERIFIED", LOC2 L1 and L2, APP, N3, ENG TDP-E,
  T03♯ and M5(0). None is upgraded, and the citecheck lists 8 statuses found verbatim.
* Each new lemma has a cross-family check on file:
  * B1, B2, B3, B4, NA-F and RM-0: R03 (Codex).
  * B1′ and B2τ: R06 (Codex).
  * SAND-R (written by Codex): R04 (Claude).
  * SAND-R′ (written by the lead): R07 (Astra) checks the rate delta (`reviews/R07_midpoint_astra.md:21, 30`), in
    addition to R04.
  * D-loc, B8a/b, B9 and L7: R06.
  * E4: R05, with falsification numerics.
  * The h < ½ budget and the p = 1 branch: R08.
* Two record defects remain (finding 1 and finding 5).

**G5 Constants and rates tracked — PASS.**
* NA-F: n₀ depends on (A, κ, h, the ρ_n envelope), and C₂ = C₂(A).
* B3: C₁ = C₁(A, s₀).
* Lemma τ: ω^τ_n and ϑ^τ_n are explicit, with ϑ″_n log n → 0 checked.
* SAND-R′: ω_n is explicit, with all four terms.
* Ladder: the O(log n) rung count is explicit.
* SAND-R tail: the slack exp(C√log n) is explicit, and §8's limit on relaxing (L-gain-R) is correctly argued.
* The constants are carried through every bridge into the interface properties consumed by RM-0.

**G6 Fidelity to the method as coded and to the binding program — PASS.**
* The theorem is stated for the shipped configuration, and every element of it is verified in code: `ls0 = TRUE`,
  `ls0_cap = "ell_n_plus_mode"` mapping to `ls0_cap_plus_mode`, the tie DP, cap 10⁶, the emitted centre and GUARD-W.
* e4 is closed by a code-level lemma under an explicitly strengthened encoding premise.
* No design family appears in (C0)–(C2). The block-relative variant names the method's partition, not a family.
* Examples and limits sit only in L7 and SHARPNESS, and after R06/R08 they are honest. In particular, (C6) is
  correctly recast as an obstruction of the *old* cap, as PROGRAM item 6 requires.
* The one place the delivered theorem falls short of PROGRAM item 3's "two primitive conditions" is the extra lattice
  condition (N)/(D-R). It is stated openly (STATEMENT §0 last sentence, §6), and the reason it is needed is explained
  (SHARPNESS §4). I count this in the score, not as a gate failure.
* Wording issues (findings 2, 6) remain.

## 2. Score: **8.9 / 10** (uncapped)

Deductions:
* **−0.5:** the main fixed-design and Gaussian-row forms both need a lattice/direction-complexity condition, (N-D) or
  (D-R), once |Q ∖ S₀| > (1 − δ₀) log n. This is a non-primitive condition on the design. It is honestly flagged and
  its necessity is open, but it is the gap between what was asked (V + L) and what is proved.
* **−0.2:** Form R's leakage is strong and fixed-scale: an O(n^{−1/2}) population leak, plus a localisation clause
  needed only because the partition is data-selected. Form F, by contrast, has the η log n budget. P3b is recorded but
  not adopted.
* **−0.3:** documentation-level MINORs: findings 1, 2, 3 and 6. None affects a proof.
* **−0.1:** the NITs (findings 4, 5, 7, 8).

Nothing was deducted for correctness.

## 3. Findings

No FATAL. No MAJOR. **No finding is REQUIRED for a pass.** Findings 1–3 are recommended before the paper text is
frozen.

1. **MINOR (G4) — `STATEMENT.md:172, 249`; `lemmas/L0_core.md:15-16`.** DLV's pathwise Claim / Corollary D′ is cited
   with no status. STATEMENT §5 says only "DLV Corollary D′ claim inside C-DLV". The source records "PROVED (by this
   seat); R04 VERIFIED-WITH-AMENDMENTS" (`Wave1C/C-DLV/lemmas/L4_delivery.md:3-4`) and "PROVED-CHECKED (pathwise
   argument supplied by R04; council round 2)" (`C-DLV/REPORT.md`, row C2). Nothing is upgraded, and L0 re-proves the
   inclusion with E4, so the citation is not load-bearing. Still, the verbatim-status rule is not met for this one
   input. **Fix:** quote both strings in §5 and in L0's input list.

2. **MINOR (G1/G6, wording) — `SHARPNESS.md:127-128`.** "(S) FAC-PK Theorem PATH … is a proved example in which LS0
   reaches S₀ along a path that is not deletion-only." PATH is about the *uncapped* path. That the path is not
   deletion-only comes from NEG ("the first ⌊n^β⌋ moves are swaps", `W2-FAC-PK/REPORT.md:24-31`). NEG also proves that
   the *shipped* LS0 never scores S₀ on that class, as §3.2 (F) of the same file says. As written, (S) reads as a
   success of the shipped LS0. **Fix:** "the uncapped LS0 path (Theorem PATH) reaches S₀; by Theorem NEG its first
   moves are swaps, so it is not deletion-only; with the shipped cap it does not reach S₀."

3. **MINOR (G2, map consistency) — `STATEMENT.md:201-203`.** The input map routes (T1) only to B6/B9. In fact, RM-F's
   proof takes ‖μ‖² ≤ Mn, p ≤ n^A and BM-∞ from (T1-F) and feeds them to B2τ, B3/B3′, B4 and B5
   (`lemmas/L1_fixed.md:111`). (L-feas) supplies |Q| ≤ K to B3–B5, B8a/b and RM-0, not only to B1, B2 and B7.
   **Fix:** add these edges (e.g. "(T1-F) ⊇ energy, p ≤ n^A, BM-∞ → B2–B5"; "(L-feas) → B2–B5, B7, B8, RM-0").

4. **NIT (optional strengthening) — `STATEMENT.md:178-179, 257-258`.** Under (N-χ) the move count is
   |S̃₀ ∖ S₀| ≤ (1 − δ₀) log n. The coded ℓ_n = ⌈log₂(n + p + 1)⌉ (`Scripts/SMC_BVS/core/v3_preprocess.R:23`) is
   larger than log n. So [L1.2] applies with the *old* cap ℓ_n too, and RM-F under (N-χ) also covers runs with
   `ls0_cap = "ell_n"`. This also places GEN (C6), which needs |Q ∖ S₀| ≫ log n, exactly outside that sub-case.
   **Suggestion:** state it as a remark. Also define ℓ_n in §1, since it is used but never defined in STATEMENT.

5. **NIT (G4 record) — `lemmas/L3b_rate.md:3`; `lemmas/L3_SANDR.md:5`.** The status lines cite only R04 (Claude Opus)
   as the check of SAND-R′. SAND-R′ was written by the Claude lead, so that check is same-provider. The cross-family
   check is R07 (Astra), which explicitly verifies the four error terms. **Fix:** record R07, and R08's sweep, there.

6. **NIT (wording) — `STATEMENT.md:259-260`; `ASSUMPTION_MAP.md:51-55`; `lemmas/L1b_rss.md:72-75`.** "The sample
   version of (L-gain) with the constant η < η_A fails in general" rests on an order-of-magnitude heuristic (the
   maximum of p Gaussian projections), not on a proof. **Fix:** "is not expected to hold in general (heuristic: …)".
   Similarly, SHARPNESS §6's "observed just outside the corresponding assumption" (:162) is loose. L1 at g = 128 and
   L2 at η = 2 ≈ 13–20 η_A are far outside. Say "outside". No cell has p > n, the regime PROGRAM calls most
   important; noting this costs one line.

7. **NIT (G3) — `STATEMENT.md:40-42, 82-83`.** Add "σ² > 0 fixed" to Setting R, or to its constants list. η is listed
   among the fixed constants used by both forms, but Form R never uses it; say so.

8. **NIT (G4) — `lemmas/L7_examples.md:90`; `SHARPNESS.md:87-93`.** FAC-PK is used without its verbatim status:
   "PARTIAL relative to the brief; (P1)–(P5) on the exact-Gram stage: PROVED-CHECKED" (`W2-FAC-PK/REPORT.md:18-19`).
   That report also *recommends a method change* for this very class: the cap ℓ_n + 2|S̃₀| (`REPORT.md:4-5`). The
   limits record should mention the recommendation and its HQ status, since it bears directly on the shipped cap that
   Theorem 3 assumes.

## 4. Fitness as the paper's main reported-model theorem

Theorem 3 as stated in v1.2 is fit to be the paper's main reported-model theorem.

**What it delivers.**
* A clean, design-agnostic chain: a deterministic core (RM-0) that holds on one common good data event for every seed,
  N_e, R′ and calibration outcome, fed by bridge lemmas each of which consumes one interface property.
* A fixed-design form whose hypotheses are partition-free and on (X, θ*) alone.
* A Gaussian-row form that covers UNI-0 and LOC-BF as examples, not hypotheses.
* Premise e4 closed at the code level.

**Correctness.** Every new step I re-derived is correct. The statuses and the examples are honest.

**Main limitation.** It is visible and stated: beyond |Q ∖ S₀| ≈ log n, the theorem carries the whole-lattice
condition (N-D)/(D-R). That is a statement about the geometry of residual directions, not a primitive "visibility +
leakage" condition.

**Most valuable strengthening still missing.** I differ mildly from SHARPNESS, which ranks polynomial |Q| (R02 P5)
first. I would rank first a **path-level replacement of the whole-lattice NA event**. NA is needed only along the
greedy deletion path that LS0 actually visits (plus the swap comparison at each visited set). That would remove (N)
at least for |Q| ≤ C log n with arbitrary C, and make RM-F literally "Theorem 1 + floors + (V) + (L)". N1's
observations (whole-lattice NA fails while the path still reaches S₀ in 178/180 runs) suggest that this is where the
present proof route, rather than the method, is the binding constraint.

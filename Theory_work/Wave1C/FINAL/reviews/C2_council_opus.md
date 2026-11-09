# Final council round 2 — Claude seat (opus)

Object: `Theory_work/Wave1C/FINAL/consistency.tex` + `sections/*.tex`, draft v2 at e95adc2. I wrote this review before
reading any round-1 council file. I read `C1_disposition.md` only afterwards, to check the fixes.

**Sources read.** COUNCIL_BRIEF(_R2); all nine sections; HQ_AUDIT A1, A2, A3; C-DLV `lemmas/L4_delivery.md`,
`L1_resources.md` (Lemma R, Corollary R) and `L2_degenerate.md` §S.1; C-GROW `STATEMENT.md:84-156` and
`METHOD_REQUIREMENTS.md`; W1-GEN `STATEMENT.md:84-120`; W1-N3 `REPORT.md:1-40`; C-PACK `SONG_LIANG_MAP.md`; the
Song–Liang PDF (pdftotext; I checked page numbers by counting form feeds from p. 947).

Branch code, all read with `git show origin/w1c/ls0-merge:…` (head 8a27652):
- `cpp/v3_core.cpp:395-500`
- `cpp/v3_engine.h` (`local_search`, `LocalArchive`)
- `cpp/v3_ledger.h`
- `v3_calib.R:40-185`
- the `ls0` / fallback lines of `v3_run.R` and `v3_fit.R`

## Gate verdicts

- **G1 — PASS.** Spot-checked against source text: Prop. F against A1:60-75, Prop. F-GROW against A2:7-35 with A3's five amendments, and GROW (G1)–(G4) and (C1)–(C5) against C-GROW STATEMENT:84-149. I also checked GEN (C1)–(C4), Theorem D against L4:13-22, and Corollary D′ against L4:51-77. The statements match. The only deviations are two dropped qualifiers (findings 4–5), and neither changes a hypothesis or a conclusion.
- **G2 — PASS.** Statuses are verbatim and nothing is upgraded. Three results are clearly marked as not council-passed: the corrected Prop. F ("HOLDS-WITH-AMENDMENTS, not councilled"), Prop. F-GROW ("PROVED (A2), checked by A3, not council-passed") and Lemma CAP ("PROVED (by this seat)"). PROVED-CHECKED is used only for ticket results whose review trails support it.
- **G3 — PASS.** I checked each of the three un-councilled items in full (see below). All three are correct. One precision gap in the delivery clause for random-design members of the GEN class (finding 1) is inherited from the scope of Lemma S. It is fixable with one sentence and is not a mathematical error in the assembly.
- **G4 — PASS.** I re-checked page numbers and content against the PDF:
  - Thm 1 p. 952, |x_i| ≤ 1; Thm 2 p. 953; Cor 1 p. 954.
  - Thm 3 p. 956: sensitivity-only form, exponent c₁nε_n².
  - The ξ_q sentence and "Theorem S … establishes the consistency of MAP models", both p. 956.
  - Condition 4 and Thm 4 (18) p. 957; Cor 2 p. 957; Condition 5 p. 958; the √P_n processors remark p. 968.
  - The "withdrawn under a binding cap" note in the Cor 2 row is traceable to C-PACK map row 11 (SL p. 958(c)).

  Theorem S is correctly marked NOT INSPECTED.
- **G5 — PASS.** Every required item is present: asymptotics and onsets, polynomial p, S5/factor designs, finite n, delivery for the shipped calibration, pooled PIPs, misspecification EP, Θ(p²) memory, EX-A/FP, and LS0 not shipped. Two wording issues remain: the plain map paragraph and the Thm S row say "unconditionally" (finding 2), and e4/N3 is missing from the scope list of open premises (finding 6).
- **G6 — PASS.** The two MR1 labels, e4 → e4′ (with GROW's "some maximiser"), cap ℓ_n versus a_n, and the CONFIG / OP-LS0 cap wording are consistent across §§1, 5, 6, 7 and 8. Cross-references resolve. Only nits remain (findings 7–10).

## Full checks of the three un-councilled items

### 1. Lemma CAP (§7.1) and its transfer list

**(L3) against the branch code.** `local_search` in branch `cpp/v3_engine.h` matches (L3) line for line:
- The centre is evaluated and emitted.
- Each loop runs a complete scan: flips j = 0..p−1, skipping additions at |C| = K, then swaps (j ∈ C) × (l ∉ C).
- The best neighbour has the largest F, with exact ties broken by `lex_less`.
- If `best.F > C.F` and `A.moves >= ell`, the search ends with `local_limit` and returns `best`. If there is no strict improvement, it ends with `local_certified` and returns C. Otherwise it moves.

The cap enters only in `A.moves >= ell`. Nothing in the scan depends on history: there is no tabu list and no dedupe against earlier scans. Scores are exact under EX-A whatever the cache state. So the scan from C_k is a function of (C_k, F) alone, which is what the induction in (a) needs.

**(L1) and (L2).** Both match `v3_core.cpp:453-481`. The order is: final islands; then the final local search and its guard; then `if (o.ls0 && status == "completed")`; then `start_mode(st, 1e6, tie_dp)`; then `cap_ll = ls0_ell + |m.S|`; then LS0; then the LS0 guard. The cap is computed after the start mode returns, and nothing before LS0 reads it. The branch preflight formula does not contain the cap, which is consistent with "M(a) differs only in LS0's cap".

**The proof.**
- (a): min(a, m*) moves and min(a, m*) + 1 scans. When m* > a, the a-th scan finds an improvement and the search returns C_{a+1} ∈ N(C_a) with `local_limit`. The scored set {C₀} ∪ ⋃_{k ≤ min(a,m*)} N(C_k), monotonicity in a, and identity when certified all follow.
- (b): the potential status is fixed before LS0, and LS0 changes neither particles nor calibration. The bookkeeping for the exact branch and the `schedule_limit` branch is right.
- (c): from π(S₀) > ½ we get F(S₀) > F(S) for every S ≠ S₀, because π ∝ e^F on Ω. With S₀ in the delivered all-scored set, the ≻-maximum is S₀. Markov's inequality then gives the factor 2. [OP] is used in the correct direction, as an upper bound on D_n(ℓ_n).
- The hypothesis a ≥ ℓ_n is not needed for (a)–(b); it is needed only for (c) and the transfers. That is harmless.

**Transfer list.** All correct:
- PXN (T) clause 2 and the on-event clause of (K): on 𝒯_n the cap-ℓ_n search is certified, so the cap-a_n search is identical.
- GEN, C-MIS D/D′, M5(b1-LH), the pathwise part of D′, and SL2's discovery input.

**Non-transfers.** Also correct and complete:
- Worst-case cost.
- Flags and metadata. The branch's `local_certified = cert_final || cert_ls0`, `ls0_improved` and `ls0_hpm_changed` (`v3_run.R:189-199`) do change with the cap.
- Stores are not monotone because of `top_c` eviction.
- GEN (C6) is about cap ℓ_n.
- U_n depends on the cap.

**Verdict: correct.** One code fact is missing from the (L1)–(L3) check (finding 3).

### 2. Proposition F (A1's corrected form)

**Delivery.** I re-derived Theorem D's walk with the total fallback:
- Within a tier, `fail()` is reached only through numerical failure (excluded by EX-A / Lemma S.2) or a resource limit (excluded by Corollary R with W_G, M_G).
- A tier-0 grid failure forces escalation. The escalation preflight is a deterministic function of (n, p) and the allocation, so it does not fire.
- In tier 1 the pilot always completes under EX-A: a forced step gives an increment of at least 1/T₁, so there are at most T₁ intervals, ending at 1 (A1:39).
- At the first failed construction the fallback is either the last successful construction or the pilot, and both pass `v3_check_grid`. So 𝒮ℒ_n = ∅.

**Resource increment.**
- LS0 runs at most a_n + 1 ≤ ℓ_n + K + 1 scans of at most q(p) = p + p²/4 models, which adds at most K·q(p) requests. Each costs at most κ + ω ≤ C[n³ + p(n+2)] (L1 R.2).
- The extra archive is at most about 2K² words: `LocalArchive` stores only the path and the scanned centres, not every scanned model.
- The ledger keeps aggregate counts and fixed-capacity stores (`v3_ledger.h:1`), so extra score events add no stored state.
- So W_G and M_G are sufficient. The guard bound is elapsed + `sec_ls0` ≤ 2(τW_G + τ₀) ≤ time_n.
- A1's order comparison also checks out: at p ∝ n, Σ̄·n³ = n⁵log³n against K·q(p)·n³ = n⁶.

**Consistency.**
- P(Ŝ ≠ S₀) ≤ P(𝒰_n) + 2E[1 − π(S₀)] + P(𝒦_n(a_n)ᶜ), with P(𝒰_n) = 0.
- 𝒦_n(a_n) ⊇ 𝒦_n(ℓ_n) by Lemma CAP (a) applied to the deterministic search.
- P(𝒦_n(ℓ_n)ᶜ) → 0 by GEN (C1)+(C2) and PXN (T). The posterior input is T03♯ / PXN (P) / the diagonal argument.
- No CAL anywhere.

**Branch implementation.** It matches A1's precision (`v3_calib.R:120-125, 162-170`):
- The fallback is tier 1 only.
- It uses `g` if `g$ok`, else `pil$schedule`; a failed or partial grid is never used.
- It goes through `v3_check_grid` and the ordinary freeze.
- `schedule_limit` remains only if that check fails, which is impossible in exact arithmetic.

Note that `v3_fit.R:127` enables the fallback only when `ls0 = TRUE`, which is consistent with "ls0 = FALSE reproduces v3".

**Verdict: correct**, apart from finding 1.

### 3. Proposition F-GROW

**Delivery.** It is identical to Prop. F. The only class-dependent input is Lemma S, and A2 correctly re-proves A4 and A5 for the iid AR(1) instance, where the raw β is X-measurable. For class (i), Lemma S.1 covers fixed standardised designs.

**Consistency.**
- On Sand ∩ NA ∩ TL, the e4 centre is a maximiser of γ₀ and lies in 𝓛.
- I re-derived the descent. Every non-deletion neighbour is beaten:
  - additions, by NA;
  - anything that drops a truth, by TL;
  - a swap T − j + l with j ∉ S₀, by NA at T − j, so it is beaten by the deletion T − j, which strictly improves F(T) by NA.
- So exactly |C ∖ S₀| moves are needed, and S₀ is scored once a_n ≥ |S̃₀ ∖ S₀| − 1. MR1 guarantees this.

**Posterior input.** T03♯ under (H0), or L6.2 plus the diagonal argument (as cited). The proof correctly refuses to derive this from D_n → 0. The fixed-p caveat (eventual enumeration at n ≳ 2.5·10²⁷ for p = 100) is right: 2¹⁰⁰ / (5.024·n) per column with p = 100 gives n ≈ 2.52·10²⁷.

**Verdict: correct.**

## Round-1 disposition check (read after the above)

I located every S1–S5, O1–O14 change in the text, and each is present as described. These include:
- S2: Theorem F's contrast coordinates and the m^T_n cutoff;
- S3: the favourable branch of GEN (C4);
- S4: the Allocation paragraph;
- O1: cap-ℓ_n wording in §6 and the CONFIG line;
- O4: the "some maximiser" wording;
- O7: MR1 labels;
- O13: the PXN (C) addition.

No round-1 finding is left unfixed.

## Findings

1. **MINOR (G3 precision) — P(no output) = 0 "for every n" on the GEN class relies on a Lemma S input that is proved only for fixed designs and nonsingular-Gaussian rows.**
   - **Where:** `sections/s6_delivery.tex:39` (and the classes at `:6`).
   - **Problem:** Lemma S.1 (`C-DLV/lemmas/L2_degenerate.md:12-15`) proves "no column is dropped" only for fixed standardised designs and random designs with a nonsingular Gaussian row law. GEN (C4) admits any random X^r independent of ε, with hypotheses imposed only on events 𝒜_n where P(𝒜_n) → 1. Off 𝒜_n nothing stops, for example, all columns being constant with positive probability (`no_predictors`). In that case P(no output) = 0 at that n fails, and only P(no output) → 0 survives.
   - **Why it is only MINOR:** §1's model G says "raw design … with nonconstant columns" also for random designs, which covers the gap if read as a standing assumption. But the statement should say so.
   - **Replacement:** after "under the respective statistical hypotheses and inherited dependency qualifications used in Corollary~\ref{cor:Dprime}", insert: "(for random-design members of the GEN class, model G is assumed on every realisation: $X^r$ has nonconstant columns almost surely; Lemma S.1 proves this for fixed standardised designs and nonsingular Gaussian rows)".

2. **MINOR (G5) — "unconditionally" is ambiguous in the paper-facing map.**
   - **Where:** `sections/s2_map.tex:31` and `:18`.
   - **Problem:** the word means "not jointly with output". A reader can take it as "without premises", but Props. F and F-GROW hold only under IDEAL-W, MACH, EX-A, the e4/TDP-IMPL premises and the amended allocation.
   - **Replacement at :31:** "…with a total tier-1 calibration fallback, also without the output qualifier, on an ideal unit-cost machine with a declared polynomial allocation (Props.~F and F-GROW: IDEAL-W, MACH, amended allocation; not checked for the C-MIS setting)".
   - **Replacement at :18:** "without the output qualifier (ideal machine, amended allocation) $\PP(\Shat=S_0)\to1$ for the patched calibration on …".

3. **MINOR (G3/G6) — the branch adds a cap-dependent no-output exit that the (L1)–(L3) check does not mention.**
   - **Where:** `sections/s7_impl.tex:39` (L2), with the code at branch `v3_core.cpp:474`.
   - **Problem:** the branch has `if (o.ls0_ell < 0 || cap_ll > INT_MAX) stop("LS0 move cap out of range")`. This stop depends on the cap (through |S̃₀|), sits inside the LS0 block, and is not a `NumericalFailure`. So it escapes the catch at :483 as an R error, with no fit object. For the specified method (finite integer caps) and under IDEAL-W it cannot fire. Lemma CAP's "$\bar\Ocal$ does not depend on the cap" is therefore a statement about the specified method, not about the 32-bit build at $n>2\cdot2^{31}$.
   - **Replacement:** at the end of (L2), add: "The branch also checks the cap range (\texttt{stop("LS0 move cap out of range")} if $\ell_n+|\tilde S_0|$ exceeds \texttt{INT\_MAX}); this cap-dependent exit is excluded by IDEAL-W and does not exist in the specified method, to which the lemma refers."

4. **NIT (G1) — Prop. F drops A1's "and concurrency".**
   - **Where:** `sections/s6_delivery.tex:33`.
   - **Problem:** A1:66 requires constants "large enough for the fixed implementation and concurrency". Lemma R's workspace term is multiplied by the worker count w (L1 R.3′).
   - **Replacement:** "$C$ a large enough constant for the fixed implementation and concurrency (fixed worker count)".

5. **NIT (G1) — Prop. F-GROW drops "and the algorithm's randomness".**
   - **Where:** `sections/s6_delivery.tex:47`.
   - **Source:** A2:35.
   - **Replacement:** "under the original unconditioned noise law (fixed designs) or the original joint design/noise law (iid rows), together with the algorithm's randomness."

6. **MINOR (G5) — the scope list of open implementation premises omits e4/N3, which the delivery results keep.**
   - **Where:** `sections/s8_scope.tex:15`.
   - **Problem:** Props. F and F-GROW assume e4 with TDP-IMPL. W1-N3 records "e4 for integrated LS0 stays OPEN". TDP-E on the branch is supported by tests and code review, not by a theory check.
   - **Replacement:** add after "N9 START/KERNEL (candidate)": ", e4 for the integrated LS0 centre (W1-N3: OPEN; used by the delivery results through TDP-IMPL, while the consistency results need only e4′ or `some maximiser')".

7. **NIT (G6) — confusing parenthesis.**
   - **Where:** `sections/s7_impl.tex:74`.
   - **Replacement:** replace "a cap below $\ell_n$ (e.g.\ $|\tilde S_0|<\ell_n$)" with "a cap below $\ell_n$ (e.g.\ the cap $|\tilde S_0|$ when $|\tilde S_0|<\ell_n$)".

8. **NIT (G6) — "only" reads as a necessity claim.**
   - **Where:** `sections/s7_impl.tex:25`.
   - **Replacement:** "\textbf{all results are established simultaneously for caps $\ge\max(\ell_n,|\tilde S_0|)$ (and $\le\ell_n+K$ for the delivery envelopes); none is claimed for smaller caps}".

9. **NIT (G6) — the provenance commit for Lemma CAP is stale.**
   - **Where:** `sections/s9_prov.tex:28`.
   - **Problem:** the lemma's (L1)–(L3) branch citations and wording changed in e95adc2.
   - **Replacement:** "\texttt{5bcde3b} (draft v1), \texttt{e95adc2} (v2)".

10. **NIT (G6) — the title-page source commit predates the disposition file the chapter cites.**
    - **Where:** `consistency.tex:7`.
    - **Problem:** the title page says "main at commit 7481194", but the chapter cites `C1_disposition.md`, which first appears in e95adc2.
    - **Replacement:** "… at commit \texttt{7481194} (Wave 1C tickets, HQ audits A1--A3, council round 1; disposition in \texttt{e95adc2}) …".

**Optional, not a finding.** I audited the branch fallback code (finding-free; see check 2). Remark (5)'s last sentence ("The writer has not audited the branch code …") could cite `BR/Scripts/SMC_BVS/core/v3_calib.R:120-125,162-170` if the writer re-checks those lines.

## Assessment

The three un-councilled items are mathematically sound: Lemma CAP, the corrected Proposition F and Proposition F-GROW. Their premises are stated honestly, their statuses are not upgraded, and the transfer and non-transfer lists are precise. Every structural fact the chapter attributes to the branch matches the code. Every round-1 finding is fixed.

What remains is precision:
- one inherited scope gap in the delivery clause for random GEN designs (finding 1);
- one ambiguous adverb in the map (finding 2);
- one branch exit outside the specification (finding 3);
- one omitted open premise in the scope list (finding 6);
- nits.

None of these blocks adoption. All are one-sentence fixes.

SCORE: 8.8/10; GATES: G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS

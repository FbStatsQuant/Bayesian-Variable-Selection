# W3-RM — REPORT to Theory HQ (Theorem 3: the reported model under visibility (V) and bounded leakage (L))

> **Flags (read first).**
> 1. **The plain "(V) + (L) ⇒ reported model" is not what is proved.** A third, explicit condition remains: a lattice
>    condition **(N)** (fixed design) / **(D-R)** (Gaussian rows) on the directions of the leakage lattice. It is
>    automatic when |Q ∖ S₀| ≤ (1 − δ₀) log n (and by a direct union when |Q| < 0.72 log n). Whether it can be dropped
>    is open (no proof, no counterexample). ADJ_astra's warning was correct.
> 2. **Gaussian rows need a localisation clause inside (L)** (each outside column, and the truths, nearly uncorrelated
>    with everything outside a polylogarithmic neighbourhood), because the method's partition is X-measurable. The
>    Gaussian-row form is not the fixed-design form conditional on X.
> 3. **Statement changed after the lock (v1.1 → v1.2), by the lead, without an HQ decision** (PROTOCOL item 3 leaves
>    strengthening to HQ): three *weaker hypotheses* adopted from the "better theorem" review — leakage measured
>    against the residual variance τ²_U instead of σ²; direction budget p·n^h, h < ½, instead of p·n^{o(1)};
>    localisation rate o((n log n)^{−1/4}) instead of n^{−2} — plus an archive-level corollary. Each v1.1 hypothesis
>    implies its v1.2 form, so HQ can revert to the v1.1 wording at no cost.
> 4. **Premise e4 is closed** as Lemma E4 (code-level, under exact arithmetic EX-A and the encoding/execution
>    conditions): on main, `start_mode` returns a maximiser of the start law on every path, and LS0 starts from exactly
>    that set. Not a binary64 statement.
> 5. Conditional, as every reported-model theorem, on the named implementation premises (EX-A, EX-S, SR, GUARD-W,
>    OP-LS0 in the shipped configuration, complete scans) and on the inherited inputs with their recorded statuses
>    (T03♯, [OP], GROW, LOC2 NA-R, APP L1_POST). No delivery claim. No method change requested.
> 6. Recommended follow-up (highest value first): a design-agnostic extension to **polynomial leakage sets**
>    |Q| ≤ n^b (R02 P5); a path-level replacement of the lattice condition (open, high risk).

## 1. RESULT

**PROVED-CHECKED** — Theorem RM-0 (core), Theorem RM-F (fixed design), Theorem RM-R (Gaussian rows, polylogarithmic
leakage set), Lemma E4 (premise e4 closed under EX-A), the examples and the sharpness record, as stated in
`STATEMENT.md` v1.2.1. Every lemma cross-family checked; mid-point CONTINUE; sweep 0 FATAL (6 MAJOR, none against the
theorems, all fixed); **council round 2 PASSED: gpt-6-astra 9.8, Claude Opus 5.5 9.1, all six gates PASS in both seats**
(round 1: 8.8 with G6 FAIL on the sharpness record / 8.9 all PASS — not passed, fixed). What is proved is "(V) + (L) +
a lattice condition", not "(V) + (L)" alone (flag 1): relative to the brief's wording the target is met in the form
ADJ_astra/ADJ_opus predicted, and the unconditional form is recorded as open.

## 2. The statement as proved (`STATEMENT.md` v1.2.1; proof files in `lemmas/`)

**Theorem RM-0 (core; any design).** For a deterministic Q ⊇ S₀ with |Q| ≤ K: on Sand(Q) ∩ NA(Q) ∩ TL(Q) the coded LS0
(cap ℓ_n + |S̃₀|) deletes the start mode's extras one per move and ends at S₀ (its archive: `returned` = S₀,
`local_certified`, |S̃₀ ∖ S₀| moves). Pathwise, for every seed, N_e, R′ and calibration outcome,
𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ, a data event; hence
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E[1 − π(S₀)] + P(Sandᶜ) + P(NAᶜ) + P(TLᶜ), and there is one data event of probability → 1 on which
every output run reports S₀.

**Theorem RM-F (fixed design; GROW's form made primitive).** Under Theorem 1's conditions (T1-F) and, for a
deterministic Q ⊇ S₀ with |Q| ≤ (log n)^κ and the feasibility clause:
(FL) eigenvalue floors on all sets of size ≤ 16 and on Q ∪ {l};
**(V)** δ²_{U,j} ≥ M_n log n for every truth j and every U ∌ j with |U| ≤ 15;
**(L)** δ²_{U,l} ≤ ητ²_U log n for every l ∉ Q and every U ∌ l with |U| ≤ 15 (η < η_A, τ²_U = residual variance);
**(N)** either |Q ∖ S₀| ≤ (1 − δ₀) log n, or the lattice directions are ρ_n-approximated by ≤ p·n^h unit vectors
(h < ½, ρ_n²(|Q| + log n) = o(log n)) and the signal dominates |Q| + log n:
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 for every seed, N_e, R′ and calibration outcome. No block, partition or design family appears;
the partition-free (V), (L) are equivalent to GROW's block-relative conditions holding for every partition (Lemmas
B1, B1′), and the block-relative variant (on the method's blocks only) is also proved.

**Theorem RM-R (Gaussian rows, polylogarithmic Q).** Under Theorem 1's conditions (T1-R), population floors on sets
of size ≤ 16 + s₀ and on Q ∪ {l}, **(V-R)** = PTV(a₀), **(L-R)**: for l ∉ Q a neighbourhood H_l of polylogarithmic
size with leak |Cov(W_l, W_j | W_{U∩H_l})| ≤ C_L n^{−1/2} to the truths and localisation rate r_n = o((n log n)^{−1/4}),
and **(D-R)** = the reference/atom conditions (R1)–(R3) of Lemma NA-R (sufficient: (D-loc)): the same conclusion
under the joint law, for any X-measurable partition with blocks ≤ 16.

**Lemma E4.** Closes e4 (flag 4). **Examples** (`lemmas/L7_examples.md`): metric-local designs = UNI-0's class (PTV)
and block-diagonal designs with growing one-factor groups = LOC-BF's class (≤ one truth per group) verify RM-R;
exact-Gram AR(1) (separation), exact-Gram orthogonal bounded groups, S5's population covariance at fixed p
(block-relative, illustration) verify RM-F; GEN (C6)'s design verifies RM-F under the shipped cap. Under the small-leakage
condition |Q ∖ S₀| ≤ (1 − δ₀) log n the old cap ℓ_n also suffices (remark in (C1)).

**Change vs the brief.** (i) delivered with the third condition (N)/(D-R) (flag 1) and the localisation clause (flag
2); fixed-design size reaches (log n)^κ, not only C log n, under (N-D). (ii) Bridges: GROW ⇒ RM-F (B1–B4, B2τ),
NA-R/PLR ⇒ RM-R (B8), UNI-0 and LOC-BF as instances (B10); new steps: Lemma NA-F, Lemma B2τ, Lemma SAND-R/SAND-R′,
(D-loc), TL under BM-Q. (iii) e4 closed. (iv) examples table. (v) sharpness record.

## 3. Status per clause

| Clause | Content | File | Evidence (reviewer, file) |
|---|---|---|---|
| (C0) RM-0 + archive corollary | core, pathwise reporting | `lemmas/L0_core.md` | R03 Sol VERIFIED; corollary R06 Sol VERIFIED |
| (B1), (B1′) | partition-free ⇔ block-relative for every partition | `lemmas/L1_fixed.md` | R03 VERIFIED; B1′ R06 V-W-A |
| (B2), (B2τ) | fixed-design sandwich, log\|Q\| = o(log n), τ-normalised leakage | `lemmas/L1_fixed.md`, `L1b_rss.md` | R03 VERIFIED; R06 V-W-A (2 MINOR applied) |
| (B3) | TL under BM-Q | `lemmas/L1_fixed.md` | R03 VERIFIED |
| (B4) | NA under (N-χ) | GROW L2.2–L2.3(a) | R03 VERIFIED (citation) |
| (B5) NA-F, N-loc | new: no-addition on a polylog lattice, fixed design | `lemmas/L2_NAF.md` | R03 V-W-A (1 MINOR applied); [P1] R06 VERIFIED; numerics `f1_naf_check.py` (0 violations / 60 runs) |
| (C1) RM-F | assembly | `lemmas/L1_fixed.md` | R03 VERIFIED |
| (B7) SAND-R, SAND-R′ | new abstraction: Gaussian-row sandwich from (V-R), (L-R) | `lemmas/L3_SANDR.md` (parallel prover, Sol), `L3b_rate.md` | R04 Opus (cross-family) V-W-A / VERIFIED |
| (B8a), (D-loc), (B8b), (B9) | NA-R, TL-R, POST-R | `lemmas/L4_formR.md` | R06 V-W-A; p = 1 branch added after R07 |
| (C2) RM-R | assembly | `lemmas/L4_formR.md` | R06 V-W-A; R07 traced |
| (C3) Lemma E4 | e4 closed at code level | `lemmas/L5_E4.md` | R05 Sol V-W-A; 84,000 calls on the production header, 0 failures |
| (C4) examples | (B10), table | `lemmas/L7_examples.md` | R06: WRONG as first written (4 MAJOR in examples), corrected; R07, R08 re-read |
| (C5) sharpness | record + numerics | `SHARPNESS.md`, `numerics/SUMMARY_SHARPNESS.md` | R08: v1 overstated (5 MAJOR), rewritten v2 |
All lemma statuses are "PROVED (by this seat, unchecked)" + the check record above; inherited inputs keep their
recorded statuses (STATEMENT §5).

## 4. Review trail (all replies verbatim in `reviews/`, each with a disposition file)

* R01 statement lock (Codex gpt-6.1-sol high): LOCK-WITH-CHANGES, 5 required + 4 optional, all applied → v1.1 locked.
* Sharpness gate: `ASSUMPTION_MAP.md`; boundary-violation numerics (§6 below); R02 "better theorem" (gpt-6-astra
  high): 8 proposals, no counterexample; 3 weakenings + 1 corollary adopted (flag 3), the rest recommended.
* Lemma checks: R03 (Sol; L0, L1, L2): VERIFIED / V-W-A; R05 (Sol; E4 vs code): V-W-A; R04 (Opus 5.5 on claudeAgent,
  cross-family to the Sol prover; SAND-R): V-W-A; R06 (Sol; everything written after R03): V-W-A, examples WRONG →
  fixed. No FATAL; no MAJOR against RM-F/RM-R.
* R07 mid-point (fresh gpt-6-astra high; statement + lemmas only): **CONTINUE**, 3 MINOR + 1 NIT applied.
* R08 exhaustive sweep (gpt-6-astra high): 0 FATAL, 6 MAJOR, 11 MINOR, 4 EDITORIAL — none against (C1)/(C2); all 21
  fixed (sharpness record and assumption map rewritten; citation checker rewritten).
* Citation check (`citecheck.py` v2 → `reviews/CITECHECK.txt`, last run after the final edits): 280 extracted ranges,
  0 failures; 32 token assertions, 0 failures; 10 quoted statuses verbatim. It is a range check plus listed tokens;
  semantic agreement was sampled by R08 (73 ranges) and the council seats.
* Council round 1 (`reviews/C1_*`): seat A gpt-6-astra high **8.8**, G1–G5 PASS, **G6 FAIL** (the η experiment was
  labelled as a violation of the leakage assumption although it sets a population proxy strength); seat B Claude Opus
  5.5 high (claudeAgent) **8.9**, all gates PASS, no required finding. Not passed; all findings fixed (v1.2.1: wording
  and record only).
* Council round 2 (two fresh seats, `reviews/C2_*`): seat A **9.8**, seat B **9.1**, all six gates PASS in both, no
  required finding → **PASSED**. Their 8 optional items (1 MINOR, 7 NIT) were applied afterwards (editorial/record;
  `reviews/C2_disposition.md`). Both seats name the same two missing strengthenings (flag 6); seat B ranks the
  path-level replacement of (N) first, seat A and R02 the polynomial leakage sets.
* Models: lead Claude Fable 5.2 (claude-personal, high); Codex gpt-6.1-sol high (R01, R03, R05, R06, parallel prover);
  gpt-6-astra high (R02, R07, R08, council seat); Claude Opus 5.5 high on claudeAgent (R04, council seat); Claude
  Sonnet 5.5 high on claudeAgent (numerics helper; cancelled after the server restart, the lead finished the runs).

## 5. Registry items (PROTOCOL item 7)

**Assumption ids:** T1-F, T1-R, FL-16, FL-Q, FL-R, V, V-R, V_b, L-gain (σ- and τ-form), L_b, L-size, L-feas, L-gain-R,
L-loc-R, N-χ, N-D(i), N-loc, BM-Q, D-R, D-loc, E4 hypotheses (H1⁺, H2, H3, H4); interface properties [POST], [SAND(Q)],
[TL(Q)], [NA(Q)], [E4]. Where each enters: `ASSUMPTION_MAP.md`.
**`implies`:** (L-gain^σ) ⇒ (L-gain^τ); (N-loc) ⇒ (N-D)(i); (D-loc) ⇒ (D-R); BM-∞ ∧ |Q| = O(log n) ⇒ BM-Q;
(FL-16) ∧ (V) ∧ (L-gain) ⇔ block-relative conditions for every partition; GROW's hypotheses ⇒ RM-F (block-relative
variant); RM-R's hypotheses ⇒ PLR's hypotheses (Sand supplied by SAND-R); UNI-0's class ⇒ RM-R; LOC-BF's class ⇒
RM-R; GROW (C5)(a), GEN (C6)'s design ⇒ RM-F; RM-F / RM-R ⇒ GROW's / UNI-0's reported-model conclusions with e4
discharged.
**Sharpness record** (`SHARPNESS.md`; observations only where numerics are quoted):
* "15" = block cap − 1; the partition-free form is equivalent to the block-relative form for every partition; no
  necessity claim.
* (V): sufficient; not necessary for masked designs covered by GEN/PXN; observed with population visibility zero:
  conclusion in 296/300.
* (L) constant η_A: sufficient; converse heuristic only. Exploratory runs on leak strength (nominal population
  strength; no assumption certified violated): a proxy entered the start mode in 209/420 runs with nominal η > η_A
  and LS0 still ended at S₀ in 418/420.
* (L) size: polylogarithmic is the engines' range; larger sets succeed in special structures (LOC2 L6, UNI-1);
  FAC-PK NEG is a failing class for LS0 with saturated starts (K < p); GEN (C6) is an obstruction of the old cap only
  (its design satisfies RM-F under the shipped cap); observed with ≫ log n visible nulls: 138/140 (old cap 89/140).
* (N): sufficient; not established from (V) + (L); observed: whole-lattice no-addition violated in 90/180 runs of a
  heuristic design while LS0 from the top of the lattice still reached S₀ in 178/180. **Open.**

## 6. Open items and recommended next steps
1. **Polynomial leakage sets, design-agnostic** (R02 P5: |Q| ≤ n^b, b < ¼; MEDIUM, 3–5 proof days) — would absorb
   LOC2's polynomial-decay result into the theorem's form.
2. **Dropping (N)/(D-R)** — path-level control of LS0 (R02 P6; HIGH, open research). Meanwhile: entropy budget h < ½
   for (R1) of NA-R (re-opens LOC2's proof; LOW).
3. Form R leakage of order √(log n/n) with the constant η_A (R02 P3b; MEDIUM); joint block visibility (R02 P4; LOW,
   needs K ≥ 2|Q| + 33s₀); removing localisation (HIGH).
4. HQ decision on flag 3 (keep v1.2 or revert to v1.1 wording).
5. Inherited: T03♯'s independent re-check (PROGRAM item 1) — RM-F/RM-R consume it; binary64 version of E4 (N3 (e)).

## 7. Files (`Theory_work/Wave3/W3-RM/`)
STATEMENT.md (v1.2.1), PLAN.md, LOG.md, ASSUMPTION_MAP.md (v2), SHARPNESS.md (v2), REPORT.md, citecheck.py;
lemmas/: L0_core.md, L1_fixed.md, L1b_rss.md, L2_NAF.md, L3_SANDR.md, L3b_rate.md, L4_formR.md, L5_E4.md,
L7_examples.md; numerics/: SPEC.md, rm_common.py, v1_masked.py, l1_groupsize.py, l2_eta.py, n1_lattice.py,
build_summary.py, f1_naf_check.py, raw CSVs and logs, SUMMARY_SHARPNESS.md; reviews/: R01–R08 and council replies
(verbatim) with dispositions, CITECHECK.txt, scratch folders of R04/R05/R06.

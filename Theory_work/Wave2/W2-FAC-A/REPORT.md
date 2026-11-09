# W2-FAC-A — REPORT to Theory HQ

> **Flags (read first).**
> 1. **Narrowing vs the brief.** Proved for **one global factor + bounded-size local blocks** (compound symmetry, block
>    compound symmetry, study S5), under the strict growth condition **limsup log p/log n < α₀(κ̄)**, which equals
>    **1/6 for every block compound symmetry (incl. CS and S5)** — not for p ≤ n^A with fixed k. Part II proves 1/6 is
>    optimal *for the full-lattice route* on exact-Gram CS, so this route cannot go further. The path route beyond 1/6,
>    p > K, and k ≥ 2 global factors remain open (Part III, evidence only).
> 2. **No new method requirement.** The method as merged (v3.1, main 4676af6: LS0 cap ℓ_n + |S̃₀|, tie-aware start DP,
>    tier-1 fallback) is used unchanged. The merged cap is needed: the start mode tends to all of [p].
> 3. **Scope strengthening (L6).** Proposition SHARP does not use p ≤ K (its witness has size O(log p)); the proof covers
>    all p ≤ n − 1.
> 4. **Instance gap.** The compound-symmetry instances need the genericity condition (GC-CS). It holds for the study's
>    coefficient patterns at a = 0.1, 0.3, 0.7, 0.9 but **fails exactly at a = 1/2** (a truth with zero marginal
>    signal, (1−a)θ_j + aΘ = 0); those configurations are not covered.
> 5. **Everything is asymptotic** (binding scope rule). No finite-n claim is made.

## 1. RESULT

**PROVED-CHECKED** (for the narrowed, flagged target STATEMENT.md v1.2) — Theorem FAC-L (Part I: (L1)–(L5), delivery
(D), instances (I)) and Proposition SHARP (Part II). Statement lock R01 (LOCK-WITH-CHANGES, applied); key lemma R02 Sol
xhigh VERIFIED-WITH-AMENDMENTS; lemma checks R03, R04 (no FATAL); mid-point R05 **CONTINUE**; sweep R06 0 FATAL / 0 MAJOR /
13 MINOR / 4 EDITORIAL, all fixed; **council round 1 PASSED: Codex Sol 9.2, Claude Opus 8.9, all six gates PASS in both
seats.** CITECHECK: 28 citations, 0 misses. The brief's full target (p ≤ n^A, fixed k) is **not** proved (see flag 1).

## 2. The statement as proved (STATEMENT.md v1.2; proof map lemmas/00_MAIN.md)

**Class 𝔉(γ̄, ψ₀, κ̄).** Correlation matrices Σ = λλᵀ + Ψ, Ψ block-diagonal over groups of size ≤ γ̄ with
λ_min(Ψ) ≥ ψ₀, all λ_l ≠ 0, and κ := max_{l,U}|λ̃_{l|U}|/√(ψ_{l|U}c_min) ≤ κ̄ (κ ≥ 1 always; **κ = 1 for every block
compound symmetry**). Growth exponent α₀(κ̄) = 1/(2κ̄(κ̄ + 2)); α₀(1) = 1/6.

**Theorem FAC-L.** Model G (Gaussian noise), fixed s₀, method v3.1 as merged with GROW's named premises. Assume (H0)
(T03♯ with BM-∞), (AG) ‖R̂ − Σ_n‖_op ≤ δ_n with Σ_n ∈ 𝔉 and δ_n√(p log log n) → 0 (exact Gram: δ_n = 0),
(P) limsup log p/log n < α₀(κ̄), and (TV) block visibility of the truths on the method's actual blocks. Then
P(Sand_n), P(NA(𝓛)), P(TL(𝓛)) → 1 on the **full lattice 𝓛 = [S₀, [p]]**, D_n → 0, **P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0**, and
liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n); LS0 reaches S₀ after exactly |S̃₀ ∖ S₀| deletions (within the merged cap).
(L5) The same under the **joint law for iid Gaussian rows** with Σ_n ∈ 𝔉, (P) and a population visibility condition
(TV-pop). **(D) Proposition F-FAC:** with Proposition F's premises, total tier-1 fallback and A1+A4 allocation (CAL not
assumed): P(no output) = 0 and **P(Ŝ⁺ = S₀) → 1** on these classes.
**Instances:** (a) exact-Gram CS, any fixed a, p ≤ n − 1 with limsup log p/log n < 1/6, under (GC-CS); (b) iid rows with
CS covariance, same; (c) **S5 (study scenario 5) exact Gram and iid rows**, both the C-GROW diagnostic layout and the
study's 14-truth high-p layouts, with exact rational visibility certificates τ₀ = c²·2023/32500 resp. c²·7/2080 (blocks
are unions of whole groups, Lemma P5); (d) general block CS.
**Proposition SHARP (Part II).** Exact-Gram CS, fixed a, s₀, θ*, σ²: if liminf log p/log n > 1/6 then P(NA(𝓛)) → 0
(explicit noise-selected witness with Z² ≥ (8 − o(1)) log p). A route-level necessity statement, not a method
inconsistency.

**Mechanism (route A as briefed).** Key lemma U: the add statistic depends on the design only through the Gram matrix;
for one factor + local blocks it splits *exactly* (Gaussian Pythagoras along the residual factor direction) into an
idiosyncratic innovation depending on T only through T ∩ g(l) (≤ p·2^{γ̄} normals) plus **one residual-factor statistic
per T**, bounded uniformly over all 2^p sets T by Cauchy–Schwarz in the Ψ-metric; the "direction count" is controlled
by the groups and k = 1, not by the lattice. With the exact BB prior ratio this gives NA on the whole lattice up to α₀.
The sandwich holds with the polynomial Q = [p] (start mode ⊇ S₀; no size ladder needed), and C-GROW's descent lemma
(needs only |Q| ≤ K) does the rest.

**Change vs the brief:** see flag 1 (narrowed class and exponent). Under the brief's own diagnosis the start mode has
order-p extras; this report confirms that (exact-Gram simulator: S̃₀ = [p] at large n) and shows that the whole-lattice
route is limited to 1/6 by an explicit witness.

## 3. Status per clause (evidence)

| Clause | File | Check |
|---|---|---|
| (L1) key lemma U | lemmas/L1_uniform_add.md | R02 Sol xhigh V-W-A (5 MINOR, applied); FU_out.txt (identity 8.9e-15, 0/53,003 violations), FU5_out.txt (0/39,895); R07/R08 reran exhaustive checks |
| (L2) sandwich Q = [p] | L2_sandwich.md | R03 Sol V-W-A (1 MINOR, applied) |
| (L3) NA, TL; α₀ | L3_NA_TL.md | R03 Sol V-W-A (2 MINOR, applied); FNA_summary.md |
| (L4) assembly | L4_assembly.md | R03 Sol VERIFIED |
| (L5) random design, instances, Lemma κ, P5, TVF | L5_random_instances.md | R04 Sol V-W-A (applied); R05 MAJOR (exact certificate) fixed: tv_cert_exact.py → TV_cert_exact_out.txt, independently reproduced by R04, R07, R08 |
| (D) Proposition F-FAC | L7_delivery.md | R04 Sol V-W-A (applied) |
| Part II SHARP | L6_sharp.md | R04 Sol V-W-A (applied); FNA_summary.md |
| Part III tools (CS-1D, GAP), Conjecture PATH-CS | L8_frontier.md | not claimed; R06 wording fixes |

Inputs (statuses verbatim): M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; T03♯ "PROVED; SF
VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside GEN "PROVED-CHECKED"; C-GROW
L1.2 (R03 VERIFIED) inside "PROVED-CHECKED"; Lemma CR/[CONC′] "PROVED (by this seat); XF VERIFIED (R19)"; Proposition F
"PROVED-CHECKED for the patched calibration law", A1 (final council round 3 PASSED), A4 "OK-WITH-FIXES", A2 "PROVED (A2),
checked by A3"; inherited: e4/N3 OPEN (only "some maximiser" used for consistency), P1/S.3 AUDITED (code reading).

## 4. Review trail

* Statement lock R01 (Codex Sol high): LOCK-WITH-CHANGES, 10 changes applied → v1.1 locked (reviews/R01_*).
* Key lemma R02 (Sol xhigh): VERIFIED-WITH-AMENDMENTS (5 MINOR) (reviews/R02_*).
* Lemma checks: R03 (Sol high) L2/L3 V-W-A, L4 VERIFIED; R04 (Sol high) L5–L7 V-W-A, 1 MAJOR (bounded-p GC-CS
  feasibility) fixed.
* Mid-point R05 (fresh Sol xhigh): **CONTINUE**; 1 MAJOR (exact S5 certificate) fixed with Lemma TVF + rational
  enumeration.
* Sweep R06 (Sol xhigh): 0 FATAL / 0 MAJOR / 13 MINOR / 4 EDITORIAL — all fixed (STATEMENT v1.2, wording only).
* **Council round 1: R07 Codex Sol xhigh 9.2, R08 Claude Opus 5.5 high 8.9; all six gates PASS in both → PASSED.**
  Post-council: R08's 2 editorial fixes and optional suggestions applied (reviews/R07_R08_disposition.md); no hypothesis
  or conclusion changed. CITECHECK reviews/CITECHECK.txt: 28 citations, 0 misses.
* Astra / Fable: not used. Helpers: none (numerics written by the lead).

## 5. Diagnosis numerics (observations, not proofs)

* D1 (iid rows, n ≤ 3200; D1a/D1b_summary.md): MR1 reached S₀ in every run (S5, CS, two-factor); NA fails along the path
  in a minority of runs and on up to 30% of random lattice sets; start mode contains 2–42% of nulls (finite n).
* D2 (exact-Gram simulator, n up to 10⁷; D2_summary.md, D2_lattice.md): S̃₀ = [p] in every CS3/CS5/S5 run at n ≥ 10⁶;
  pure-deletion LS0 paths in all CS3/CS5/S5/F2 rows at n ≥ 10⁵ (F2r one swap); MR1 reached S₀ in every run; NA fails on
  one-sided lattice sets at log p/log n > 1/6.
* D3 (exact 1-D CS LS0 from [p], 720 runs, log p/log n up to 0.75, a up to 0.9; D3_summary.md): 720/720 pure deletion
  paths, 718/720 ending at S₀ — strong evidence for the path route (Part III).
* FNA (exact CS, n up to 10¹²): one-sided NA witnesses grow with n at log p/log n = 0.30, none at ≤ 0.14 for n ≥ 10⁹.

## 6. Open items and recommended next step

1. **Path route for exact-Gram CS beyond 1/6 (Conjecture PATH-CS, L8).** Tools proved here: exact 1-D reduction of the
   score (Lemma CS-1D) and the gap invariant of the deletion path (Lemma GAP). The remaining step is the late stage with
   all remaining kept nulls on one side of the gap. Numerics (D3: 720/720 pure deletions) suggest the claim holds for all
   p ≤ K. **Recommended follow-up ticket.** It would lift the exponent from 1/6 to any p ≤ K for CS (then S5 by
   extending CS-1D to block exchangeability).
2. **p > K** (start mode capped at K): a swap phase longer than the MR1 slack is conceivable (heuristic, untested at
   asymptotic sizes). This concerns the study's p ≫ n S5 regime, which this report does not cover.
3. **k ≥ 2 global factors:** the scalar residual-factor step does not extend directly; a matrix version needs a loading
   condition on T-restricted Grams (conjectural obstruction).
4. **a = 1/2 CS with the study patterns:** a masked truth violates (GC-CS); covering it needs a GEN-type masked-truth
   argument combined with growing p.
5. For the paper: state Theorem FAC-L with the S5 instance next to GEN and GROW (S5 moves from "frontier" to "covered for
   log p/log n < 1/6"), with Proposition SHARP and the D2/D3 evidence as the frontier.

## 7. Files produced (Theory_work/Wave2/W2-FAC-A/)

STATEMENT.md (v1.2, locked), PLAN.md, LOG.md, CHECKPOINT.md, REPORT.md; lemmas/00_MAIN.md, L1_uniform_add.md,
L2_sandwich.md, L3_NA_TL.md, L4_assembly.md, L5_random_instances.md, L6_sharp.md, L7_delivery.md, L8_frontier.md;
reviews/R01–R08 (verbatim) + dispositions R01–R06, R07_R08, COUNCIL_BRIEF.md, citecheck.py, CITECHECK.txt;
numerics/ (fac_common.py fast exact local search; fac_exact.py exact-Gram simulator; cs1d.py exact 1-D CS; d_run.py,
d_exact.py, d_summ.py, d2_lattice.py diagnosis; fu_check.py, fu5_check.py (L1); fna_check.py (L3/L6); kappa.py;
tv_cert.py, tv_cert_exact.py (certificates); raw JSONL outputs and summaries D1a, D1b, D2, D2_lattice, D3, FNA, FU, FU5,
kappa, TV_cert, TV_cert_exact). No files outside this folder were modified; no git state changes.

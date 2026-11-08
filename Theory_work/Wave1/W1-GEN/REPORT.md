# W1-GEN — REPORT to Theory HQ

> **Flags (read first).**
> 1. **Statement changes after lock** (all logged in LOG.md, none weakens the main theorem): v2.1 — the (C6)
>    counterexample design was changed (v1's singleton truth was scored trivially by a block table, so the full method's
>    D_n was 0 there); v2.2 — claim (C1′) added (canonical certificate, a sufficient condition; no hypothesis changed);
>    v2.3 — (C5)(d) restricted to the study's actual 14-signal layouts (step 7 / step 13) as a theoretical sequence, and
>    (C1′) given its bounded-energy assumption.
> 2. **(C6) is a counterexample for the LS0 route, not for the full method**: removing the bounded relevance/centre
>    size breaks every universal LS0-discovery guarantee (P(LS0 misses S₀) → 1 while π(S₀) → 1), but it is not shown
>    that the full method's D_n fails to vanish (SMC or the final search may still score S₀).
> 3. **Everything is asymptotic.** At the study's own size (n = 200, p = 500) the visibility margins of the covered
>    scenarios are 0.16–0.94 (< 1): the σ²-dilution masking of the study is exactly VIS failing at finite n
>    (numerics/SUMMARY.md, E6 real size). No finite-n claim about the study is made.
> 4. The result is about **v3.1 + LS0 as specified** (LS0 is not in production code), under the named implementation
>    premises, incl. e4 (N3 OPEN as a general invariant).

## 1. RESULT

**PROVED-CHECKED** — Theorem GEN (STATEMENT.md v2.3, lemmas/00_MAIN.md): on a general, checkable class of correlated
fixed designs (masking allowed, p ≤ n^A with any A), P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; instances LH (exact Gram), LH-iid
(conditional on the candidate W7-PART Theorem B), W, and the study generator's scenarios S1/S3/S4/S6; S2/S5 shown to lie
outside the class; a counterexample shows the bounded-size conditions cannot be dropped from the LS0 route. Every
lemma had a cross-family check (Codex gpt-6.1-sol); mid-point CONTINUE; sweep 0 fatal; council passed in round 1
(Sol 9.0, Opus 8.9, all gates PASS).

## 2. The statement as proved (STATEMENT.md v2.3; proof map lemmas/00_MAIN.md)

**Theorem GEN.** Fixed-design Gaussian model, standardized design, s₀ ≥ 1 fixed, p ≤ n^A; method v3.1 + LS0 with the
named premises (EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, e4, complete scans; IND-T and the c₄ search when R′ > 4). If
* **(H0)** the hypotheses of S-T/T03♯ hold (R, SE_λ(j₀), SE_w(m♯_n; g₀), BM-∞);
* **(H1) bounded separated relevance set:** some 𝒱 ⊇ S₀ with |𝒱| ≤ v̄ has a Gram floor on 𝒱 ∪ {l} for every l, and no
  variable outside 𝒱 reduces the residual signal Λ_S by more than c_S(n − 1)φ₀⁴θ*²_min, for every S ⊆ 𝒱 (c_S < 1);
* **(H2) centre certificate on the actual blocks:** some S* ⊆ 𝒱, s* ≤ v̄, with within-block SE, VIS(S*) (order-
  M_n log n block-level gains for the reference variables) and NL(S*) (O(log n) leakage plus an averaged-leakage bound)
  — e.g. the **canonical certificate (C1′, L8)**: the block regression coefficients γ_b of μ on each block's own
  columns satisfy a beta-min dichotomy (each entry either ≥ √(M_n(σ² + 2M) log n/((n − 1)φ₀²)) plus slack, or
  collectively negligible); then S* = ∪ supp(large part);
then **D_n ≤ P(S̃₀ ≠ S*) + O(1/log n) → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n)** (no
delivery claim). If S* = S₀ (favourable case), (H1) is not needed. Random designs: the same holds under the joint law
when the hypotheses hold, with fixed constants and envelopes, on X-events of probability → 1 (C4).

Mechanism: (C1) the start mode equals S* w.p. → 1 (the locked T22(iii) argument re-run with a general reference,
EXP′ proved); (C2) from **any** centre inside 𝒱 the greedy search keeps its centres in 2^𝒱 and reaches S₀ within
2^{v̄} − 1 moves — states missing a truth always have an order-L_n improving truth addition that beats every outside
move (SEP), supersets of S₀ always improve by deleting an extra; no progress/non-progress margin is needed inside 𝒱
(this is why RF176's failure of region-form greedy dominance on masked LH does not bite). **Masking** = true variables
with zero (or negligible) block-level regression coefficient; they are recovered by the descent. This is the per-block
analogue of Song–Liang's Condition 5, with violations allowed.

**Change vs the card/brief.** The brief's target (a Song–Liang-type reported-HPM theorem on a general class) is met in
the form above. Not reached: designs whose relevance set grows (fixed-ρ AR(1), common-factor designs), and any
finite-n statement.

## 3. Status per clause (statuses of external inputs verbatim, nothing upgraded)

| Clause | Content | Evidence |
|---|---|---|
| L1 (EXP′, contrasts) | uniform score expansion on polynomial families | lemmas/L1_lemmaE.md; R02 Sol VERIFIED-WITH-AMENDMENTS (applied); numerics E1 |
| (C1) centre law | S̃₀ = S* w.p. → 1 | L2_centre.md; R03 Sol VERIFIED-WITH-AMENDMENTS (applied); inputs T22(i) "PROVED-LOCKED", T22(iii) proof "PROVED-LOCKED CONDITIONAL" (re-run, EXP′ proved); E2/E3/E6 start = S* |
| (C1′) certificate | block beta-min ⇒ (H2b)–(H2c) | L8_certificate.md; checked inside sweep R10 (4 items fixed) and by the council |
| (C2) descent | paths in 2^𝒱, τ ≤ 2^{v̄} − 1, local max at S₀ | L3_descent.md, L4_search.md; R04 Sol VERIFIED-WITH-AMENDMENTS (applied); E2–E4 sweeps over centres |
| (C3), (C3-fav), (C4) | assembly, favourable case, random designs | L5_assembly.md; R06 Sol VERIFIED-WITH-AMENDMENTS (applied); inputs M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))", T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; [OP] PROVED (by this seat, unchecked) from the named premises, corroborated by [W6] (candidate) |
| (C5)(a) LH exact Gram | S* = S₀ ∖ M, 𝒱 = signal units | L6(a); R07 VERIFIED-WITH-AMENDMENTS; input blocks = groups (W1-EXP Lemma 4.2 via Thm5-LH, SAME-FAMILY-ONLY); E2 |
| (C5)(b) LH-iid | via (C4) | L6(b); R07 VERIFIED-WITH-AMENDMENTS; **conditional on W7-PART Theorem B (candidate)** and [CONC]; E3 |
| (C5)(c) W | favourable, S* = S₀ — new: W layer (iii) was "not covered" | L6(c); R07 VERIFIED-WITH-AMENDMENTS; partition proved inline |
| (C5)(d) study S1/S3/S4/S6 | favourable asymptotically (start mode = S₀) | L6(d) Lemma SEL (selection-uniform leakage under data-dependent packing): R07 GAP on v1 → v2, checked only inside sweep R10 (one minor fix) and by the council; E6 |
| (C5)(d) study S2, S5 | no bounded certificate exists (outside the class) | L6(d); R07 corrections applied; E5/E6 (S5: LS0 fails at n = 3200 by the cap; S2: S* grows) |
| (C6) | bounded 𝒱/S* cannot be dropped from the LS0 route | L7_counterexample.md v3; R06 GAP, R08 GAP, R09 **VERIFIED**; mechanism seen in E7 (v1 design) and in study S5 (E5) |

## 4. Review trail

* Statement lock R01 (Sol): LOCK-WITH-CHANGES, 9 required changes, all applied → v2 locked.
* Lemma checks (Sol): R02 L1, R03 L2, R04 L3+L4, R06 L5 — VERIFIED-WITH-AMENDMENTS; R07 L6 (a)–(c) V-W-A, (d) GAP →
  repaired (Lemma SEL); L7: R06 GAP, R08 GAP, R09 VERIFIED (third attempt).
* Numerics (Sonnet helper, numerics/SUMMARY.md): E1 unit tests pass; at n = 3200 all route flags hold in E2 80/80,
  E3 160/160, E4(i) 40/40, E4(ii) 20/20; finite-n failures only at n ≤ 800 (incl. one combination-look-alike trap at
  n = 200); centre law converges slowly (median 1 − π₀(S*) ≈ 0.04–0.09 at n = 3200).
* Mid-point R05 (Sol, independent): **CONTINUE** (majors: study NL_avg under selection → Lemma SEL; scope/checkability →
  L8 certificate).
* Exhaustive sweep R10 (Sol): 0 fatal, 1 major, 6 minor, 1 editorial — all fixed.
* Council round 1: **Sol 9.0, Opus 8.9; all six gates PASS for both → PASSED.** Opus's minor required fixes applied
  afterwards (no hypothesis/conclusion change).
* Astra/Fable: not used.

## 5. Open items and recommended next step

1. **Frontier: growing relevance sets.** Fixed-ρ AR(1) (study S2) and common-factor designs (S5) need 𝒱/S* growing
   like log n or p; the 2^{v̄} move count and the finite extras family are the obstacles (E5: the uncapped search still
   reaches S₀; the cap ℓ_n binds). Next step: a growing-family descent with a Φ-type move count and an NA-type control
   of noise-chosen extras (Theorem C (C1) of W1-T37R's LD condition is the natural tool).
2. **Finite-n.** All margins are asymptotic; at n = 200 VIS fails for the study (dilution). A finite-n version would
   need path-wise rather than worst-case union bounds.
3. Lemma SEL (L6(d)) and L8 had no dedicated lemma check (sweep + council only) — a dedicated cross-family check is
   cheap if HQ wants (C5)(d) and (C1′) at the same level as L1–L5.
4. Numerics for the final (C6) design (s₀ ≥ 17 orthogonal truths, weak proxies) were not run; E7 used the v1 design.
5. Premises: e4/N3 (W1-N3 clause (c) covers the unique-maximiser case that is all this proof uses, for the coded
   start_mode; LS0 integration remains), GUARD-W/OP-LS0 audits, W7-PART Theorem B for LH-iid.
6. Recommended for the paper: state Theorem GEN with the canonical certificate (C1′) as the headline condition
   ("block-level beta-min dichotomy + bounded separated relevance set"), LH/W/LH-iid/study S1-S3-S4-S6 as corollaries,
   and (C6) + S2/S5 as the frontier.

## 6. Files produced (all in Theory_work/Wave1/W1-GEN/)

STATEMENT.md (v2.3), PLAN.md, LOG.md, REPORT.md; lemmas/00_MAIN.md, L1_lemmaE.md, L2_centre.md, L3_descent.md,
L4_search.md, L5_assembly.md, L6_instances.md, L7_counterexample.md, L8_certificate.md; reviews/R01–R12 (verbatim
reviewer outputs) with dispositions R01, R02_R04, R05, R06, R07, R10, R11_R12 and COUNCIL_BRIEF.md;
numerics/ (bvs_core.py, experiment scripts e1–e7b, raw CSV/JSON outputs, per-experiment summaries, SUMMARY.md).

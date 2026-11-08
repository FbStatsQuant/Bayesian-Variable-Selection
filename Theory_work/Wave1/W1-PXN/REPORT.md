# W1-PXN — REPORT to Theory HQ (FR01, candidate API-PXNGAP = TH161), 2026-11-08

## 1. RESULT
**PROVED-CHECKED** — the p ≫ n masked reported-HPM theorem (TH161, as repaired here) is cross-family VERIFIED on PROOF §§1–10
by Codex gpt-6.1-sol, and the council passed in round 1 (Codex 8.6, Opus 8.3, all gates PASS). Proposed status wording
(HQ's call): "PROVED (API-PXNGAP candidate + W1-PXN repairs); XF VERIFIED (Codex gpt-6.1-sol: R11–R17, R19, R21, sweep R30,
council C1); council C1 Claude Opus 8.3; under (OP); not adopted". It is a theorem about v3 + LS0 under the operational
premises, asymptotic, for each fixed A ≥ 1.

**Flags (statement changes vs the card, none weakening the headline):** (a) the input of (P) is changed from locked T03
(which needs the unproved H-T02) to T03♯ (TH128) plus a new random-design step; (b) (R)'s display is split, because the
source's "for every t" chain is false; (c) an exact-branch convention is added for very slowly growing p; (d) (T)'s
"exactly c moves" and (K)'s sharp cost now hold on an explicit joint event with ℓ_n ≥ c; (e) the source's "sharp in order"
and failure-rate remarks are not claimed.

## 2. Statement as proved
`STATEMENT.md` (locked v2; §5 lists post-review changes and takes precedence). Definitive proof map: `FINAL_PROOF.md`.
Headline: on LH-iid (c linked hub pairs, equicorrelated groups, |ψ_i| < ρ) with SIZE g ≤ B_n < 2g and 18 ≤ p_n ≤ n^A,
p_n → ∞, for v3 + LS0 (one production local search from the exact start mode, centre emitted), under EX-A, EX-S, CAL, SR,
GUARD, OP-LS0:
- (P) 1 − π(S₀) = O_P(√(log n/n)) under the joint law of (X, ε);
- (C) for every n, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n with D_n ≤ P(LS0 misses S₀) → 0. Hence
  P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U_n)) → 0 and liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n).
Also (R) partition recovery (explicit W7 constant, summable, ≤ p^{−C} eventually), (S) start mass and masking law,
(E) start mode = S°, (T) LS0 scores and certifies S₀, (K) cost.
Not claimed: delivery P(U) → 0; the method without LS0; the production core as shipped (LS0 is not merged); the study's
groups of 5; superpolynomial p; any finite-n guarantee (vacuous at n = 200).

**A > 1: confirmed.** No step uses p ≤ n or a lower growth bound on p; only Gram matrices of size O(log n) are inverted.
Rates do not depend on A. A enters constants and onsets: Tr-J / Lemma E family exponents D = A (start) and A(s₀+2) (search);
δ_n = 32√(2(A+1) log n/(n−1)); the eigenvalue range L_n = O(log n) with cutoff m♯_n ≤ s₀ + ⌈1 + (As₀ + (s₀+2)/2) log₂ n⌉ and
j₀ = ⌈(2A+1)s₀⌉+1; the search penalty (2A+1) log n, so (D_S) needs (n/2) log(1 + c₂/(4(σ²+M))) > (2A+1) log n + 2κ_E + 2;
the (L) remainder O(A n^{−1/3} log n); recovery onset ((2+C)A + ½) log n ≤ (n−4)I*; the P3′ constant ∝ √(A+1). A sufficient
envelope is n/(log n)³ ≥ C(A, fixed parameters), plus the SIZE onset. No uniformity over growing A.

## 3. Status per clause, with evidence
| clause / item | status | evidence |
|---|---|---|
| Report item 1: Tr-J(c) constants (x = t′/2 − √(jt′), t′ ≥ 6j, exponent D+1, family counts D = A, A(s₀+2)) | XF VERIFIED (minor wording fixes E-5, E-6) | R11; N1 (0 violations) |
| Report item 2: Lemma E (E2), (E3) | XF VERIFIED (minor fixes E-1..E-4) | R12; N2 |
| Report item 3: Lemma Λ(a) Haar-span step | XF VERIFIED (full derivation in R13 #2); Lemma B(ii) was an ERROR (false for |A| ≥ n−2), unused downstream, repaired (E-7) | R13, R21; N3 |
| Report item 4: Theorem R (= W7 Thm B) | XF VERIFIED incl. Hotelling density, W7 Lemma 2 and the Corollary B constant, after splitting the false "every t" display (E-15); W7 A0(c) bypassed by a direct margin argument (E-17); independent cruder route (R′) XF VERIFIED | R14, R19, R21; N4 |
| Report item 5: operational closure OP-LS0 + GUARD | XF VERIFIED as a theorem under (OP) (GUARD (G2) / Lemma RO + definition of R̄⁺); Lemma LS(i) and P6′ cost were ERRORs, repaired (E-8, E-9); production bridge remains an implementation obligation | R15, R21; N6, N8 |
| Report item 6 (HQ brief): dependency statuses | see ledger below; locked T03 inadequate (H-T02) → replaced by T03♯ | R16, R19 |
| FR01 item "Lean-readiness" | assessment only: (C) and Lemma LS covered in abstract form by sorry-free T21HPM / T37Lattice; wrappers missing; probability layer not Lean-ready | lemmas/I8_lean_readiness.md (unchecked) |
| (S) P3′, P4 | XF VERIFIED (sharpness remark deleted E-19; E-20) | R16 |
| (E) P5 | XF VERIFIED (bypasses, does not prove, N3 tie-DP invariant; EX-A incl. exact DP) | R15, R21 |
| (T) key lemma P6′: Lemma U, (D_S) case list, (L) | XF VERIFIED; original (L) step was an ERROR, repaired via (E5) | R17, R19; N5 (c₂, c₅ attained, 0 violations) |
| (P) via T03♯ + design event + de-randomisation | XF VERIFIED | R19 (lemmas/P8_T03sharp.md) |
| (C), (K) | XF VERIFIED (exact-branch cases E-18) | R15, R21, R30 |
| Mid-point | CONTINUE | R20 |
| Whole proof | sweep: 1 ERROR, 2 GAP, 4 MINOR, all fixed; council PASS round 1 | R30, C1 |

**Dependency ledger (statuses verbatim; R16):**
- T22(i), (ii): "PARTLY PROVED: (i), (ii), (iv) PROVED-LOCKED (wave 1; ...)", "same-family and cross-family (Astra); not
  adopted" (NBH/ID_REGISTRY.md:264). Adequate (deterministic, any partition, any reference S° ∈ Ω).
- Locked T03 (TH123): "PROVED-LOCKED (wave 3; ...); MEET-THM flag SAME-FAMILY-ONLY; ...; conditional on H-T02 which T02(i)
  closes" (ID_REGISTRY.md:271). **Not adequate as cited** (H-T02 not discharged) — no longer used.
- T03♯ (TH128): "PROVED (S03 §6; ...); V03 and A-REV2: VERIFIED under exactly these hypotheses" (W6-FIXREV2/STATEMENTS.md:51-52);
  final card "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)". Adequate as a fixed-design theorem; the
  random-design extension is this ticket's lemmas/P8_T03sharp.md (XF VERIFIED R19).
- [CONC]: archive source "Lemma C1 [CONC] (cited, standard)" (W3-PXN/PROOF.md:61; Bickel–Levina 2008 Lemma A.3). Replaced
  by the self-contained [CONC′] (lemmas/CR_corr_tails.md, XF VERIFIED R19).
- W7 Thm A (TH162): "PROVED (W7-PART); XF VERIFIED* (A-REV9: A1-A4 VERIFIED, A2 extra premise; A-REV6: A0(c) GAP)". Used
  only via the direct strict-margin argument (XF VERIFIED R14, R21).
- W7 Thm B / Cor B (TH163): "PROVED (W7-PART); Theorem B XF VERIFIED* (A-REV6 restricted scope; A-REV9 B-exact VERIFIED);
  Corollary B XF GAP (A-REV9, L2 constants)". The Corollary B constant is now independently XF VERIFIED (R14, re-derived by
  R21 and both council seats); the registry row itself is HQ's to update.
- PXN P1 (TH148): "PROVED given C1 (W3-PXN); SF VERIFIED* (...); XF VERIFIED (A-REV3; A-REV6 via W7 Thm B)". C1 supplied by [CONC′].

## 4. Review trail
- Statement lock R00 (Codex): LOCK WITH CHANGES, 8 findings (6 MAJOR), all applied → STATEMENT v2 locked.
- Item checks (fresh Codex each): R11 I1 VERIFIED w/ minor; R12 I2 VERIFIED w/ minor; R13 I3 ERROR (B(ii) domain); R14 I4 ERROR
  (display, A0(c), exact branch); R15 I5 ERROR ×2 (LS move cap, cost); R16 I6 GAP (= D1, D2, sharpness remark); R17 I7 key lemma
  VERIFIED w/ minor (original (L) step ERROR, repair VERIFIED); R19 repairs (CR, P8♯, L) VERIFIED w/ minor; R21 new-reviewer
  re-check of all later repairs VERIFIED w/ minor.
- Numerics: N1–N7 (Sonnet helper) 0 violations; N8 end-to-end p > n with SIZE (g = 9; (150,270), (300,540); 100 fits):
  recovery 100/100, S₀ scored 46/50 → 50/50, certified 34/50 → 49/50 — consistent with an asymptotic theorem, no counterexample.
- Mid-point R20 (fresh Codex, proof files only): CONTINUE.
- Exhaustive sweep R30: 1 ERROR, 2 GAP, 4 MINOR — all fixed, no objection recorded.
- Council round 1: Codex gpt-6.1-sol 8.6 (all gates PASS); Claude Opus 5.5 8.3 (all gates PASS). Passed in round 1.
- Not used: gpt-6-astra, Fable 5.1.

## 5. Open items and recommended next step
1. **Consolidated supplement text** (C1 Opus MAJOR, non-blocking): one proof document applying E-1..E-22 and the lemma files
   in place, without line cross-references to the candidate. Recommended next step (Sonnet transcription + one Codex
   fidelity check).
2. **Production bridge** (implementation, not proof): merge LS0 = `local_search(S̃₀, ell_n, tier, emit_centre = true)` and
   replay (OB02(c), OB03, DF16, ENG02); the current core does not call it.
3. Registry: TH161 status and TH163's "Corollary B XF GAP" are HQ's to update on this evidence.
4. Out of scope, unchanged: delivery P(U) → 0; groups of 5 (FR02); superpolynomial p; finite-n margins (proven bound
   vacuous at n = 200; N8 shows the route visibly fragile at n = 150, mostly clean at n = 300).

## 6. Files produced (all in Theory_work/Wave1/W1-PXN/)
STATEMENT.md, PLAN.md, LOG.md, FINAL_PROOF.md, REPORT.md;
lemmas/: ERRATA.md, P8_T03sharp.md, CR_corr_tails.md, L_strict_localmax.md, LS_P6_repair.md, R_branch_repair.md,
B_ii_domain.md, I8_lean_readiness.md;
numerics/: n1–n7 scripts + outputs, lhcommon.py, enumlib.py, SUMMARY.md; numerics/n8/ (n8_route.py/.txt, n8_selfcheck.py, SUMMARY.md);
reviews/: R00, R11–R17, R19, R20, R21, R30, C1_council_codex.md, C1_council_opus.md (verbatim, each with disposition),
_COMMON_BRIEF.md, _COUNCIL_BRIEF.md.

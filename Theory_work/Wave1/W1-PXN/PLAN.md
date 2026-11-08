# W1-PXN — PLAN (v2, 2026-11-08; revised after statement-lock review R00)

Goal: a cross-family (Codex gpt-6.1-sol) VERIFIED on API-PXNGAP PROOF §§1–10 (`NBH/branch_snapshots/API-PXNGAP/PROOF.md`),
with explicit verdicts on the six items of REPORT.md:133-144, repairs by this seat where a reviewer finds a gap, each
repair re-checked by a NEW cross-family reviewer. Target statement: `STATEMENT.md`.

## Decomposition into check items (each = one fresh Codex reviewer + one numerical falsification attempt)

| item | PROOF § (lines) | content | report item | numerics |
|---|---|---|---|---|
| I1 | §3 (123-156) | Lemma Tr-J (a)(b)(c); constants x = t′/2 − √(jt′), t′ ≥ 6j, exponent D+1; family-count table (D = A, A(s₀+2)) | #1 | N1 |
| I2 | §4 (160-207) | Lemma E (E1)–(E6), esp. (E2) G⁻¹ − nH⁻¹ = G⁻¹(G+I)H⁻¹, ‖P_Ay‖² ≤ n−1; (E3) quadratic minimisation, RSS floor | #2 | N2 |
| I3 | §5 (211-234), §8.2 (307-326) | Lemma P2, Lemma B, Lemma Λ(a)–(c); the Haar-span step with equicorrelated null groups | #3 | N3 |
| I4 | §1 (77-100), §2 (104-119) | Theorem R = W7-PART Theorem B + Lemma 2 (Hotelling density) + Corollary B; Lemma T | #4 | N4 |
| I5 | §7 P5 (286-288), §8.4 (372-393), §8.5, §10 (421-457) | Lemma LS; P5; composition (C); OP-LS0 + GUARD ⇒ 𝒪 ∩ {S₀ ∉ 𝒮⁺} ⊆ {LS0 does not score S₀}; check against W6-FIXREV1 and the engine's local search / ledger code | #5 | N6 |
| I6 | §6 (238-271), §7 P4 (277-284), §9 (403-417) | P3′ and P4 as uses of T22(i-a),(ii-a); P8′ (T03 / T03♯ + de-randomisation); [CONC]; exact statuses of T22(i),(ii), T03, T03♯, CONC, W7 Thm B | #6 | N7 |
| I7 | §8.1 (296-305), §8.3 (328-370) | Lemma U (U3); lattice margins (D_S) case list; (L) strict local maximum | key lemma (P6′) | N5 |

| I8 | — | Lean-readiness of the finite deterministic cores (Lemma LS, (C), Tr-J(a), (E1), (E2)) and outstanding formalisation obligations: short assessment by this seat (FR01 lists it; HQ's brief for this ticket replaced it by "dependencies have adequate status", which is covered by I6; both are reported) | #6 (FR01) | — |
| I9 | repair files | `lemmas/CR_corr_tails.md` (Lemma CR, [CONC′], (R′)), `lemmas/P8_T03sharp.md` (D1 repair: T03♯ + design event + de-randomisation), `lemmas/L_strict_localmax.md` ((L) via (E5)) | D1, D2, CONC | N4, N7 |

Final assembly depends on the verified D1/D2 repairs and the revised statement (STATEMENT v2), not on the original
§1/§9 citations.

## Numerical falsification specs (given to the numerics helper; outputs in `numerics/*.txt`, summary `numerics/SUMMARY.md`)
Failure criterion everywhere: any instance where a proved inequality/identity is violated beyond floating tolerance
(relative 1e-8 for identities, exact comparison for inequalities) is reported as a violation and stops use of the lemma.
Distribution checks (N3, N7) are diagnostics, never proofs of laws or rates.
- N1 Tr-J: exact Beta quadrature of the truncated moment (a) vs bound, j = 1..24 (beyond 16), u ∈ {0,1,5,20},
  n ∈ {50,100,200,800}, τ ∈ {.01,.05,.2,.5}; (b) Beta tail vs bound; (c-core) P(χ²_j > t′) ≤ e^{−t′/2+√(jt′)} for t′ ≥ 6j,
  j ≤ 30, and the empirical slack of t′ ≥ 6j.
- N2 Lemma E on LH-iid (g = 10, ρ = .7, ψ = .5, c = v = 1) at (n,p) ∈ {(100,60),(200,120),(400,200)}: (E1)–(E4) per set.
- N3 Haar/Beta laws (Lemma Λ(a) null part with an equicorrelated null group; Lemma B(i′)): KS diagnostics.
- N4 Hotelling density: normalisation, MC cross-check, W7 Lemma 2 (U)/(L) on a grid of n, r ∈ [−.9,.9] (both signs), t;
  Corollary B vs exact union sum for LH pair counts.
- N5 population lattice margins (c ≤ 3, v ∈ {0,1,2}, unequal ψ_i, β_i) vs closed-form c₂, c₅; Lemma Λ(c) closed forms.
- N6 Lemma LS and (C) logic on exact enumeration p = 10 (production LS, ties, move cap, final scan).
- N7 miniature (P): exact posterior p = 10, n ∈ {100,…,6400}, 20 seeds (diagnostic).
- N8 feasible-SIZE end-to-end with p > n: g = 9 (SIZE needs B = min(⌊√n⌋,⌊√p⌋,16) ∈ [9,17]);
  (n,p) ∈ {(150,270) [B = 12], (300,540) [B = 16]}, c ∈ {1,2}, v ∈ {0,1}, ≤ 10 seeds: partition recovery, start mode = S°, LS0 scores /
  certifies S₀, observed (D_S) margins. Exact block tables and start-mode DP; no full enumeration.

## Known points to resolve (from my read; see STATEMENT §4)
- D1: (P) cites locked T03 without its H-T02 hypothesis → re-route through T03♯ (TH128/TH09) with a design event over all
  sets of size L_n = s₀ + max{m_n, m♯_n, j₀, g, s₀+2} = O(log n). Repair file `lemmas/P8_T03sharp.md`.
- D2: Theorem R's explicit constant rests on W7 Corollary B (XF GAP, A-REV9, "L2 constants"). I4 reviewer checks W7
  Lemma 2; N4 compares the bound with exact Hotelling tails. Fallback written: `lemmas/CR_corr_tails.md` (R′).
- Minor (to be confirmed): (L) uses RSS_{S₀} = nσ²(1+o(1)), i.e. (E5), not only (E3); Lemma E's P(𝒟ᶜ) bound lists
  e^{−n^{1/3}} where (d1) gives 2e^{−n^{1/3}}; the symbol b₀ is used both for the IG hyperparameter 0.01 and for the
  beta-min constant of P2(c).
- P5 sidesteps the N3 tie-DP invariant (the maximiser is unique when π₀(S°) > ½) but still assumes the exact start-mode
  DP returns the argmax (EX-A); to be stated.

## Pipeline (PROTOCOL.md)
1. Statement lock: one Codex gpt-6.1-sol (high) reviewer on STATEMENT.md + PLAN.md vs sources. Fix, lock.
2. Numerics N1–N7 (local, ≤ 20 seeds, exact enumeration p ≤ 10 where exact). Scripts + outputs in `numerics/`.
3. Per-item checks I1–I7: one fresh Codex gpt-6.1-sol (high) reviewer each, run in parallel (items are independent
   given their stated inputs). Replies verbatim in `reviews/`, with disposition.
4. Repairs by this seat in `lemmas/`; each repair re-checked by a NEW Codex reviewer. A lemma failing 3 attempts → STUCK.
5. Mid-point review after I7 (key lemma P6′) is VERIFIED: fresh Codex reviewer with STATEMENT.md + proof files only;
   CONTINUE / REDIRECT / STOP.
6. Exhaustive sweep (one Codex reviewer, full proof + repairs), fix all.
7. Council: Codex gpt-6.1-sol high + Claude Opus 5.5 high (claude-personal), ≥ 8.0 both, ≤ 3 rounds.
8. REPORT.md.
Budget notes: gpt-6-astra at most once (only if Sol reviewers disagree on a step); Fable 5.1 only for a hard step Opus fails.

# W3-DIST — disposition of line check L6 (Sol, `lemmas/DIST12.md` v0.1, sha c05fb3f082fcb938)

Written by the lead, 2026-11-15 22:04 CT. Review file: `reviews/L6_sol_DIST12.md`.

## What the reviewer found

- D.1 (deterministic levels and Lemma T), D.2 (intercept event), D.3 (pointwise bound): VERIFIED.
- D.4: display (1.1) and consequences (a), (b), (d), (e): VERIFIED. D.6 / display (1.2): VERIFIED.
- **L6-01 (MAJOR).** Consequence (c) of DIST-1 (target clause TC3) said "M₀ of order (1 + s₀^r)(A + 1)" and "(1 + s₀) log p/n".
  The proof files did not give this: (i) M₀ = max{16, (A+1)s, log C₅} with C₅ ∝ K_s = Σ_i(1+i)^s2^{−i}, and log K_s ≳ s log s;
  (ii) the radius constant C grew with s through C_d = s + 33 and C_T ∝ (2s + 33); (iii) the sentence mixed the raw sparsity
  s₀^r and the retained one s₀. Overall verdict: NOT VERIFIED as written, for this sentence only.

## Disposition: ACCEPTED; repaired by constants, target clause kept as fixed (no WEAKER change)

The reviewer offered two repairs: weaken (c) to "of order log n/n for fixed parameters", or supply the quantitative
argument. The second is taken; nothing in the argument changes, only three constants.

1. `lemmas/X.md` v0.4, §3 Step 3: since 1 + i ≤ e^i, (j+1)^{s₀}q^j ≤ (e^{s₀}q)^{j₁+1}(e^{s₀}q)^i and e^{s₀}q ≤ ½ by (d), so the
   sum is ≤ 2(e^{s₀}q)^{j₁+1}: **K_s is replaced by 2**, C₅ := 2·4^{s+1}e^{3B/(2σ²)}(8A+4)^{s/2}, and
   **M₀ ≤ 16 + 4(1 + s)(A + 1) + 3B/(2σ²)**.
2. `lemmas/X.md` v0.4, (E4): (s₀ + 1) log n ≤ 2t because M₀ ≥ max{16, (A+1)s} ≥ (s₀ + 1)/2, so **C_d := 34** (was s + 33).
   C_x, C_P, Λ, C_Q, C_β, C_v, C then depend on (A, σ², M, M′) only.
3. `lemmas/DIST12.md` v0.2, D.1: 2s log n ≤ t (M₀ ≥ (A+1)s ≥ 2s), so d₁ log n ≤ 34t and **C_T := 4[34(A + 7) + 8]** (no s);
   a paragraph after D.4 states the dependence: C = C(A, σ², M, M′); ε_n² ≤ C²[16 + 4(1 + s₀^r)(A + 1) + 3(M + M′)/(2σ²)] log n/n.
4. `STATEMENT.md` v1.4.7, DIST-1 (c): rewritten with the explicit bound and the raw sparsity s₀^r throughout; TARGET §2
   row P3 synced. TC3 itself ("M₀ = O((1 + s₀^r)(A + 1))") is unchanged and is now proved as written, the O being for fixed
   (σ*², M, M′). Changelog tag: **EQUAL** on TC3 (pending the diff check).

Lemma X′ and DIST-2 keep their constants (C_m, C_T′ depend on s); no claim is made there about the dependence on s.

## Consequences for the record

- `lemmas/X.md` was line-checked at v0.3 (L1, Astra) and is now edited: rows X, X′ are **STALE** until re-checked.
  `lemmas/DIST12.md`: rows TC/DIST-1, TC/DIST-2 **STALE**.
- Re-check: by a new Sol agent (the finder's family), inside the diff check D1, with the exact diffs of both files.
- If the re-check does not confirm the repair, the fallback is the reviewer's minimal repair, which is a WEAKER change to
  TC3 and therefore an early checkpoint.

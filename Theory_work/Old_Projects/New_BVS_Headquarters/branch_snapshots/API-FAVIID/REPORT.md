# API-FAVIID — REPORT (synthesis task 9, FAVIID-CLOSE, Part 1)

Run of 2026-11-02, branch `theory/API-FAVIID`. Source audited: `origin/theory/W5-FAVIID` at commit `31695b1`.

Files in this directory:
- `W5-FAVIID_REPORT_AMENDED.md`: the finished W5-FAVIID report, with marked errata;
- `REFEREE_HANDOFF.md`: the Part 2 brief for the cross-family referee;
- `scripts/`: deterministic, no randomness;
- `results/`: outputs of the scripts.

## 1. Headline

1. **Part 1 is done, but the placeholders were already filled.** The synthesis said `W5-FAVIID · REPORT.md` still contained
   `__HEADLINE__`, `__PILOT__`, `__CARD__` and an empty §4.5. That is true at `5bf4dee`. It is not true at the branch tip
   `31695b1`, where W5-FAVIID itself filled all four (74 pilot runs, n up to 12,800). The synthesis read the earlier snapshot.
2. **Audit.** I recomputed every number in the filled report from the raw results (1,600 sweep rows and 74 pilot rows).
   - §4.5's pilot table, the §4.4 tables and the threshold columns reproduce exactly.
   - There is **one factual error**: headline item 5 says "(T_n+1)Δ_n < 1 in 0/56 runs at n ≤ 3,200"; the data give **1/56**
     (S3, p = 500, n = 3,200, value 0.997).
   - **Three claims hold only at the cell median**, and single designs are much more spread:
     - the truth-context effect on Q̄ (the evidence for Conjecture B′);
     - the "factor ≈ 5 to spare" in Theorem A's moment check;
     - "T22(i) vacuous at every n ≤ 3,200".
   - All are corrected, and marked, in `W5-FAVIID_REPORT_AMENDED.md`. No statement, proof or status word changes.
3. **Same-family read of the R6 items** (Lemma X⁺, Lemma M, Theorem B's factorisation, C1–C3): **no error found**.
   - c_ML = 3.83114 is confirmed independently.
   - This is not verification. All four items stay **PROVED (candidate, author only)** pending the cross-family referee.
4. **Hand-off written** (`REFEREE_HANDOFF.md`): a step list with line numbers, plus three points to watch:
   - the uniform Lipschitz claim in (G3);
   - the "verbatim" transfer of W3-PXN P2 to equicorrelated Σ in C1;
   - Lemma P1′, which is load-bearing for "unconditional on S3/S4/S6" but is not on the R6 list.

## 2. Statements

I propose no new statements. The W5-FAVIID statement table (§2 of its REPORT) is unchanged. Two notes for the statement of record:
- **Theorem B's "unconditional" clause for S3/S4/S6** depends on Lemma P1′ (PROVED given [C1], author only). Without it, the
  statement reads 1_{Q_n(3)}(1 − π₀(S₀)) = O_P(√(log n/n)).
- **"2^B-free"** is a statement about the constant. B_n ≤ 16, so 2^B is bounded anyway. The gain is the leading constant: 3.83(s₀+1)
  times |𝒲| (Theorem B) or times 1 (Theorem A), instead of a 2^B·poly(g) factor. The rate √(log n/n) is unchanged.

## 3. Proofs or sketches

None of my own. Same-family read notes are in `REFEREE_HANDOFF.md` §§1–4. Steps I re-derived:
- the cross-multiplication in X⁺;
- the Lemma M inequality and its constant;
- Lemma S;
- the Tr′ exponent e₁;
- the ζ_n order;
- the multinomial step and the (p−s₀)⁻¹ normalisation against locked T22(i);
- the order of the deletion term.

## 4. Evidence

Scripts:
- `scripts/audit_w5faviid.py` → `results/audit_out.txt`
- `scripts/audit_tails.py` → `results/audit_tails.txt`
- `scripts/check_cML.py` → `results/check_cML.txt`

All three run on the frozen W5-FAVIID results:
`git archive 31695b1 theory_campaign/W5-FAVIID | tar -x -C <dir>`, then pass `<dir>/theory_campaign/W5-FAVIID/results`.
`scripts/amend_report.py` makes the amended copy from `git show 31695b1:theory_campaign/W5-FAVIID/REPORT.md`.

**Reproduced exactly:**
- the §4.5 table (T_pilot, T_grid, Δ medians; counts 0/16, 0/20, 1/20, 3/16, 1/2);
- the per-scenario n = 6,400 ranges;
- the §4.4 log₁₀π₀ table and the fractions above ½;
- the empirical first n (1,600 for S1 at both p and S3 at p = 500; 3,200 otherwise, on both scales);
- T22(i) valid in 1,600/1,600 rows;
- Q_n in 1,598/1,600 rows (failures: S6 at n = 200);
- max q/Q_real = 0.9957;
- max m_real = 3 (S3/S4/S6) and 5 (S1);
- median q at n = 3,200 between 0.044 and 0.059;
- the ratio to the null-addition prediction (0.86–1.11 at n = 3,200, from `threshold.txt`);
- first-stage ESS pinned at 0.90 in all 74 runs, with no forced stages.

**Corrected** (marked `[API-FAVIID]` in the amended copy):

| Claim (W5-FAVIID) | Data | Correction |
|---|---|---|
| (T_n+1)Δ_n < 1 in 0/56 runs at n ≤ 3,200 (§1.5) | 1/56: S3 p=500 n=3,200 rep 1, value 0.997 | 1/56; the median is 1.5 at 6,400 and 1.6 at 12,800 (the original said "≈ 1.5 at 12,800") |
| Truth context changes Q̄ by ≤ 4–5% (§1.2, §2, §4.1, §5) | Cell medians of Q₀/Q_real: 0.999–1.050. Single rows: 0.31–5.1, with 197/1,200 outside [0.9, 1.1] | "In cell medians"; the evidence for Conjecture B′ is weaker than stated |
| q/ξ_n = 0.60–0.82 "in every cell", factor ≈ 5 to spare (§4.1) | True for cell medians at n ≥ 800. Cell means are 0.65–2.23; 20 rows exceed 3.83 (max 30) | Factor ≈ 5 at the median, ≥ 1.7 at the mean. No contradiction with (A1), which bounds E[q1_𝒢] asymptotically |
| T22(i) bound "medians 10²–10⁵", vacuous at every n ≤ 3,200 in S3/S4/S6 | Cell medians 2.1 to 7.2·10⁵; 5/80 S3 designs at n = 3,200 have bound ≤ 1 | "Vacuous in the cell median" |
| δ̂₁ ≈ 0.99(1 − π₀) at n ≥ 3,200 (§4.5) | Median 0.985, range 0.26–2.19; δ̂₁ sets Δ in 24/74 runs | Add the range. Sensitivity: with the rigorous lower bound u₁/(1+u₁) in place of δ̂₁, the counts become 0/16, 0/20, 3/20, 4/16, 1/2 |

Computation: four single-core jobs of a few seconds each, run through `owls_run`.

## 5. What fails and why

Nothing was attempted beyond Part 1. The synthesis's description of Part 1 was stale (§1, item 1), so Part 1 became an audit and
amendment of an already-filled report. I could not edit `theory_campaign/W5-FAVIID/REPORT.md` itself, because the protocol restricts
writes to this directory. HQ should adopt `W5-FAVIID_REPORT_AMENDED.md` in its place, or apply the five marked errata.

## 6. Needs escalation

1. **Part 2 (XF referee):** follow `REFEREE_HANDOFF.md`. The highest-risk step is the uniform Lipschitz/[C1] argument in (G3),
   which carries the whole factorisation. The next are C1's transfer of W3-PXN P2, and Lemma P1′ (add it to the referee's list).
2. **HQ / SYNTHESIS update:**
   - mark M5's "unfinished REPORT" as done (with errata);
   - the synthesis's threshold row (n = 1,050–3,200 from W5-FAVIID) is consistent with the audit;
   - in the Thm 6 row, the finite-n (P1) evidence is 1/56 runs at n ≤ 3,200 and 3/16 at n = 6,400.

## 7. Outside scope

- W5-FAVIID's pilot estimate of δ₁ uses a product-form estimate (1 − e^{−u₁}). The rigorous lower bound changes the n ≥ 3,200 counts
  slightly (see the table above). An exact δ₁ is not computable at p ≥ 500. Any paper sentence quoting "first n with (T_n+1)Δ_n < 1"
  should say which δ₁ it uses.

## 8. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| M5 / Thm 2(iii) favourable branch, S3/S4/S6 (W5-FAVIID Thm B) | 1_{Q_n(3)}(1−π₀(S₀)) = O_P(\|𝒲(3)\|(s₀+1)√(log n/n)); unconditional given Lemma P1′ | 0.9 | 0.85 (written; awaits XF check) | (G3) uniform angle bound plus Lemma S | No |
| Lemma X⁺ | as stated (κ⁺ = O(1/n) on the RSS floor) | 0.95 | 0.95 | [W1-L1.1]–[W1-L1.2] forms | No |
| Lemma M | as stated, c_ML = 3.8311 | 0.98 | 0.98 | none (elementary; constant re-checked) | No |
| Thm 6 (P1) on S3/S4/S6 (C2) | asymptotic (T^max+1)Δ_n → 0 | 0.9 | 0.85 | C1's transfer of W3-PXN P2; W2-T26 idealisations | No |
| Thm 5(a) on S3/S4/S6 (C3) | liminf P(Ŝ = S₀) ≥ 1 − limsup P(U) | 0.9 | 0.9 | inherits Thm B and C1 | No |
| (P1) at finite n | (T_n+1)Δ_n < 1 in 1/56 runs at n ≤ 3,200 and 3/16 at 6,400 (numerical only) | 0.8 | numerical only | T_n = O_P(1) stays OPEN | No |
| Conjecture B′ (no \|𝒲\| factor) | CONJECTURE | 0.75 (down from 0.85: per-design context effects reach ×5) | 0.3 | decoupling the X-measurable context from y | No |

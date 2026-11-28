# COUNCIL R3 — OPUS seat (TH-SONG-ASSUMPTIONS; scoped fix-verification, POLICIES §1b)

Package v1.3 at `4bacc09d` (branch dept/theory), compared with v1.2 at `7c7ca30f`. Reviewer: Opus 5.5, high effort.
- **Read:** the R3 brief; R2_SOL, R2_NEON and R2_OPUS; RESPONSE_R2; R2_TO_R3.diff (all 693 lines). In the full files I read only
  context around changed passages, plus targeted greps for leftover v1.2 wording at every location the R2 seats listed.
- **Checked:** the new `scripts/e9b_width_mc_ext.py`, the `widths`/`R_pop` code it imports from `e9_width_mc.py`, and
  `tables/e9b_width_ext_s1.tsv` (108 rows, re-aggregated).
- **Writes:** none apart from this file. No scratch files, no fits, no numerics. I ran one stdlib-only Python parse of the
  TSV, without numpy or BLAS. It was not run under `nice`, which is a small procedural deviation.

## 1. Fix verification: one row per R2 substantive/blocking point

| # | R2 point (seat) | verdict | reason |
|---|---|---|---|
| 1 | Step-3 rate bound; display omitted −γ log n and linearised over an unrestricted residual (Sol 1 BLOCKER; Neon S2; Opus S-1) | **fixed** | See §1a. The coded-likelihood form is correct: H_Dm = B_Dm − γ log n, W, V_n, and termwise comparison against U followed by summing the containing-model odds. Both dispatches (B ≤ 0 via W = 0; B > 0 via monotonicity at W = 2(1+δ)B) give −γ log n + O_P(1). The linearisation paragraph is aligned with it, and DEFINITIONS and DOSSIER list it as an obligation. |
| 2a | E9 scope: zero-slack diagnostic, m = 2 at p = 5,000 and m ≥ 3/4 not evaluated, Markov argument (Sol 2 BLOCKER; Neon S3) | **not fixed (one location)** | Fixed in DEFINITIONS TS-b and SL-6/7, in ASSUMPTIONS A-MARGIN-U (b), item 7 and the w_Dm bullets, in SIMULATION (synthesis, E9 reading, E9b) and in DOSSIER (score card, Q1, Q4, weak point 7). **But the ASSUMPTIONS decision row D4 (l. 31) is unchanged v1.2 text:** "for mixed rivals with d = 1, m ≤ 2 … so the margin holds there with surplus ≥ 3.3 at SNR 2". Sol 2 named "Paths decision D4", and RESPONSE_R2 item 2 says D4 was done. |
| 2b | Population minimum over the 40 nearest nulls (Sol 2) | **fixed** | The AR(1) Markov screening argument replaces "uncorrelated far nulls" in ASSUMPTIONS and SIMULATION. It also covers E9b's d = 2, 3, because S0 = 1..10 lies at one end of the chain. |
| 3 | The active-m example and E9 surpluses assume C = 1; C ≍ (s0+1)² (Opus S-3) | **fixed** | The m*(d) cap is labelled asymptotic, and "at C ≈ 121 every m ≤ J is active" is stated in all four files. E9b reports C = 1, C = 121 and no credit. "On S1's AR(1) designs" replaces "realistic/typical designs" in DOSSIER Q1 and the DEFINITIONS plain English. |
| 4 | A-NEC "smaller than each" contradicts NH14 (Sol 4 / B-3; Neon S1; Opus S-2) | **fixed** | Replaced by "No blanket ordering" in ASSUMPTIONS and DOSSIER. DEFINITIONS SL-6/7 matches. The ordering statements are correct: c_ψ/n is below l_n eventually, because l_n ≫ r̄_n log P_n/n ≫ 1/n. SL (26) is now described with a vanishing lower and a growing upper threshold. NH14's exact-dependence allowance is stated. |
| 4b | SBJ: do not assert that it expressly allows duplicates (Sol 4) | **not fixed (one location)** | ASSUMPTIONS l. 107 is fixed ("we do not claim it expressly allows duplicates"). **DOSSIER A-NEC Q3, l. 110, still reads "SBJ Assumption 4 … and NH14 … so they allow exact duplicates".** It now contradicts ASSUMPTIONS and the new last bullet of the same Q3. RESPONSE_R2 item 3 says this was fixed. |
| 5 | Exact all-deletion κ_n; 40/41 vs 39/41; E K₁ is an HPM event (Sol 3) | **fixed** | 0.626–0.693 / 2.505–2.771, 1.1–1.7% below the proxy, with the minima at d = 6 / d = 3. This appears in SIMULATION (price note), ASSUMPTIONS, DOSSIER Q4 and the DEFINITIONS converse. The proxy κ is kept and labelled. Evidence-against item 4 and the E K₁ wording are corrected in all files. |
| 6 | TD′ exact conjecture, (s+1), TS-b′, SL Cor 1 wording, TD-A proxy (Sol 5) | **fixed** | DEFINITIONS §4.1 gives an exact display: q_n = min{p, ⌈C′(s+1)M log(p∨n)⌉}, tail exp(−cM log(p∨n)), M log(p∨n) ≤ c√n, consistent with TD's window. (s+1) appears in DEFINITIONS l. 126 and ASSUMPTIONS ll. 81 and 243. TS-b′ is removed. The text now says "stretched-exponential" and "overlapping envelopes". TD-A has a centred tail with a variance **proxy**. |
| 7 | Conventions: b₀ units, A-BS fixed-endpoint, raw p in TS-b, ν(dx)dy, candidate rule, full rank (Sol 6) | **fixed** | Each is present in the cited locations. "Fixed before the analysis sample, or on independent data" is consistent across ASSUMPTIONS A-MIS(iii), §3.5 and DOSSIER Q1. The sparse-projection relaxation is recorded as such, and the fixed-rank form stays the headline. |
| 8 | SL-0 EBIC heuristic; TM-b with S0^C ≠ ∅; invariance qualified (Sol 7) | **fixed** | SL-0 is now "heuristic only … does not transfer consistency". TM-b assumes S0^C ≠ ∅ and says the forward ∅ case is not claimed, in both DEFINITIONS and ASSUMPTIONS §3.5. The "form only" caveat appears in DEFINITIONS §5 and below the ASSUMPTIONS §5 table. |
| 9 | thm:omitted is an analogue, not "the special case" (Neon S4; Sol 7) | **fixed** | ASSUMPTIONS §3.5 and DEFINITIONS SL-9 both say "previously delivered analogue (… expectation bound)". |
| 10 | Numbers and labels: 6.70/6.696, SD 0.12, 1.17 (1.175), E2 9/136 label, min(p, s0+J) (Sol 8) | **fixed** | All are in the diff. The E2 residual ratio and the fixed-variance squared Hellinger ratio (max 0.21, never ≥ 1) are now distinguished in ASSUMPTIONS, DOSSIER and SIMULATION. |

### 1a. Check of the new step-3 bound (ASSUMPTIONS §3.3 step 3)

The bound follows from the factorisation odds(S:T) = odds(S:U)·odds(U:T).

1. **Likelihood part of odds(S:U).** It equals [(2b+Q_U)/(2b+Q_S)]^{n/2+a₀}, where 2b = 2b₀s_y².
   - Q_S ≥ RSS_S, and the Gaussian-concentration event gives RSS_S ≥ RSS_U + σ²W. So this part is at most
     [(2b+Q_U)/(2b+RSS_U)]^{n/2+a₀} · (1 + σ²W/(2b+RSS_U))^{−(n/2+a₀)}.
   - The first factor is O_P(1). This uses Q_U − RSS_U = O_P(σ²) (A-NEC) and RSS_U ≳ nσ² on the superset truncation event.
   - The second factor is at most (1+W/V_n)^{−(n/2+a₀)}, because RSS_U ≤ RSS_T gives 2b + RSS_U ≤ σ²V_n.
   - Hence **RSS_U ≤ RSS_T is used in the right direction.**
2. **Prior × determinant part of odds(S:U).** It is at most exp(Pr_n(d)).
3. **Sum over N.** Because W uses min_N, the sum Σ_N odds(U_N:T) can be factored out, and it gives the (C log p/n)^{m/2} credit.
4. **B_Dm > 0.** The step (n/2+a₀)log(1+2(1+δ)B/V_n) = (1+δ)B(1−o_P(1)) needs B = O(log n). This holds under A-DIM, which is
   TS-b's setting. The R-transfer gives W ≥ 2(1+δ)B from A-MARGIN-U.
5. **m = 0.** The bound reduces to step 1, with U = T and w_D0 = 0.
6. **Remaining O_P(1) terms.** There are finitely many classes at fixed M, so the O_P(1) terms are uniform.

**No error found.**

## 2. New substantive flaws or regressions introduced by the v1.3 edits

**None introduced by the edits themselves.** The two items below are not new flaws. They are R2 fixes that were not carried
to one location each, and the RESPONSE wrongly reports them as done. I list them here with their fixes so they can be
applied mechanically.

1. **ASSUMPTIONS_AND_PROOF_PATHS.md l. 31 (D4 row, last cell).** Replace "for mixed rivals with d = 1, m ≤ 2 the conditional
   width on S1 designs is 0.1–0.6 (E9), so the margin holds there with surplus ≥ 3.3 at SNR 2" with:
   > "for mixed rivals, an E9/E9b zero-slack diagnostic (mean widths 0.1–0.6 on S1's AR(1) designs) gives a positive
   > estimated surplus for d ≤ 3, m = 1 and m = 2 at p = 500 (≥ 2.39 at SNR 2 with C = 121 or no credit); m = 2 at
   > p = 5,000 and m ≥ 3 are not evaluated."
2. **OWNER_DEFENSIBILITY_DOSSIER.md l. 110 (A-NEC Q3, first bullet).** Split it as ASSUMPTIONS ll. 106–107 already does:
   > "NH14 Cond. 4.5 … bounds the minimum nonzero sample eigenvalue and expressly allows exact dependence (p. 17), which
   > A-NEC excludes; …"

   and move SBJ to its own clause with no duplicates claim (its ν_{k*} indexing is already in the last bullet).

**Checked and found sound:**
- **E9b code.** The binding D are ranked by population min_N R at unit SNR, which is SNR-free because R scales with SNR².
  The widths are computed over all nulls. B is computed under each of the three credit conventions.
- **E9b numbers.** I re-aggregated the TSV, and every printed number matches it:
  - SNR 2, minimum surplus at C = 1 / C = 121 / no credit:

    | (d, m) | C = 1 | C = 121 | no credit |
    |---|---|---|---|
    | (1, 1) | 3.29 | 2.63 | 2.66 |
    | (1, 2) | 3.84 | 2.39 | 2.49 |
    | (2, 1) | 4.27 | 3.83 | 3.80 |
    | (2, 2) | 4.55 | 3.62 | 3.69 |
    | (3, 1) | 4.30 | 3.95 | 3.93 |
    | (3, 2) | 4.54 | 3.80 | 3.79 |
  - SNR 3: minima 6.71 / 5.81 / 5.91.
  - All 54 classes are active at C = 121 (counting the SNR 3 rows as well: 108/108).
  - The quoted range of my R2 rerun (2.40–3.87) is correct.
  - "≥ 2.39 … even without credit" (DEFINITIONS) is true, since no credit gives 2.49.
  - ASSUMPTIONS "2.39 (with C = 121 or no credit)" is the minimum over both conventions. That reading is acceptable.
- **Disclosed limits.** "The non-binding D for d ≥ 2 are not evaluated" is stated. The selection of the three binding D
  ignores w, but w varies by only about 0.4 while the R gaps between D are larger. This is disclosed, so I do not count it
  as a flaw.

## 3. Gate verdict: **NOT CLEAR** (as the text stands at 4bacc09d)

- Point 2a is the residue of an R2 **BLOCKER** (Sol 2). The D4 row still asserts "the margin holds there" for "d = 1, m ≤ 2",
  which is the overclaim Sol 2 targeted.
- Point 4b is a residue of Sol 4.
- Both are one-line edits with the replacement text given in §2. **Once these two lines are edited as in §2, I would
  CLEAR without a further review round.** The fix can be verified by grep: l. 31 must no longer contain "margin holds there",
  and DOSSIER l. 110 must no longer attribute "allow exact duplicates" to SBJ.
- Everything else from R2 is genuinely fixed, and the v1.3 edits introduce no new substantive flaw.

## 4. Scores for the assumptions touched by the diff (D / R; the two §2 edits assumed applied)

| assumption | D | R | note |
|---|---|---|---|
| A-MARGIN-U | 9 | 9 | The step-3 bound is now correct. E9/E9b scope is honest everywhere except D4 (8.5 R until D4 is fixed). |
| A-NEC | 9 | 9 | There is no blanket ordering, and the precedent descriptions are accurate (8.5 D until DOSSIER l. 110 is fixed). |
| A-DIM′ (conj.) | 9 | 9 | The exact conjecture statement and window are now consistent across files. |
| A-MARGIN-H | 9 | 9 | The E2 labels are separated, and min(p, ·) covers bounded p. |
| A-BS | 9 | 9 | The fixed-endpoint "Used in" is stated, and the 1.175 is rounded honestly. |
| A-MIS(iii) | 9 | 9 | The candidate-rule quantifier is correct. The full-rank relaxation is recorded but not adopted. |
| A-GL | 9 | 9 | The coded vs raw b₀ is now explicit. |

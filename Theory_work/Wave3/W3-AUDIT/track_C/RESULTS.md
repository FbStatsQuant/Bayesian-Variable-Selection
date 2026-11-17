# W3-AUDIT track C — RESULTS (internal; not for the paper) — final

## Final findings
1. **Sparse floors (P1–P3) are inside and rise with n in all 19 designs**, both at p = n and at p = 10n. The floor at the size cutoff m♯ is ≈ 0.001–0.006 at (n, p) = (200, 2000) and recovers in every design (0.014–0.22 at n = 1600, slopes +1.1 to +1.8). Population floors are certified by λ_min(Σ) > 0.
2. **Visibility at p = 10n recovers by n = 800–1600 in 16 of 19 designs (spread truth) and 18 of 19 (clustered).** It does not recover for the strong factor with the mixed-sign spread truth (D14 v̂ 0.10 at n = 1600, D15 ≈ 0; population value 0) or for the riboflavin-like design (D18, ≈ 0 in both placements). AR(0.95) spread recovers only at n = 1600 (small margin). Larger p/n (the p = 2·10⁴ cells) delays the recovery.
3. **Leakage-set size:** bounded or ≈ log-growing for IND, AR(≤ 0.95), fixed blocks, Toeplitz α = 2, S6 and FRED-like tiles; ≈ n^0.4–0.5 for Toeplitz α = 1 and growing blocks; the whole design for factors with a ≥ 0.75, S5 and riboflavin-like. Weak factors (a = 0.5) give Q̂ = S₀ once the common correlation falls below √(log n/n) (from n = 200 at p = 10n).
4. **Local regressions and lattice width follow the leakage split**: inside where Q̂ is small, outside where Q̂ = [p].
5. **β_min rate, identifiability margin and the Occam term are inside in every design and both p/n ratios.** The (AG) operator bound is outside in every design (pre-announced).
6. **No NOTS cell contradicts a TRACK_B inside/outside verdict.** Two Track-C sentences cited in TRACK_B are corrected: AR(0.95) leakage grows only ≈ n^0.1 (n^0.5 at p = n was an artefact of p = n = 200); and Q̂ = S₀ also for weak factors, not only for IND.

Lead: Opus 5.5 (high), 2026-11-16. Plan `work/C_PLAN.md` v3 (HQ rule 11-16: qualitative conditions and their trend
in n; explicit constants from the proof are conservative and are not tested). Proxy computations only, no SMC fits.
**Data.** Owls part: 95 tasks (p ≤ 2000), 0.30 core-h. NOTS part: Engineering, jobs 2754535–2754540, 114/114 tasks rc 0,
46.86 core-h billed (23.3 core-h inside the tasks). Outputs: `/home/fb31/SMC_Theory_Department/helpers/W3-AUDIT-C/`
`owls_out/` and `nots_out/` (sha256 re-verified by the lead, 231/231 OK; package checksums match the frozen copy
`nots_pkg/`, commit 8ad91fab). Combined: `collect_all/{summary,trend}.csv`; copies `track_C/all_summary.csv`,
`track_C/all_trend.csv` (209 task files, 19 designs × 11 cells × 10 replicates × 2 placements).

## How to read
Two n-series: **p = n** (n = 200, 400, 800, 1600) and **p = 10n** (2000, 4000, 8000, 16000); the cap p = 2·10⁴ at
n = 200, 400, 800 gives the p/n comparison. Values are medians over 10 replicates; "a → b" = n = 200 → 1600 on the
p = 10n series unless marked. **IN↑** inside, improving; **IN** inside, bounded; **UNCL↑** unclear, moving toward inside;
**UNCL** unclear; **OUT** outside. Searches give upper bounds on minima (they refute, never certify); population floors are
certified by λ_min(Σ); leak sets are subsets of the true ones ("IN" for P5 means "not refuted"). sp = spread truth (study
positions, signs + − + −); cl = clustered (four adjacent columns, aligned signs). Visibility v̂ = δ̂²/log n (sample),
pop = min δ² in the population (n-free).

## Table: design × proxy × n trend (final)
| D | design | P1–P3 floors (sample φ̂²(16); m♯ floor; pop λ_min(Σ)) | P4 visibility sp (sample; pop) | P4 visibility cl | P5 leak \|Q̂\| sp / cl | P6 ℓ¹ tail, P9 width (sp / cl) | P7 rate, margin | P8 Occam | P10 |
|---|---|---|---|---|---|---|---|---|---|
| 01 | IND | IN↑ .15→.54; .006→.22; 1 | IN↑ .37→145; 1 | IN↑ .006→151 | IN 4 / 4 | IN 0; −.55→−.68 / −.54→−.71 | IN↑ | IN | OUT |
| 02 | AR0.5 | IN↑ .12→.29; .005→.14; .33 | IN↑ ≈0→4.6→28→80; .6 | IN↑ 1.1→102 | IN 32→46 / 8→10 | IN↑ 2.5→1.2, +.01→−.17 / IN | IN↑ | IN | OUT |
| 03 | AR0.8 | IN↑ .05→.10; .003→.056; .11 | IN↑ ≈0→.01→5.6→21; .22 | IN↑ .26→40 | IN 109→137 / 19→23 | UNCL↑ 18.6→6.5, +.50→+.005 / IN | IN↑ | IN | OUT |
| 04 | AR0.95 | IN↑ small .013→.023; .001→.014; .026 | UNCL↑ ≈0 to n=800, .45 at 1600; .05 | IN↑ .41→8.8 | IN (slow) 466→585 [n^0.11] / 70→87 | sp UNCL 26→39, +.57→+.42 / cl IN↑ 23→8.5, −.01→−.26 | IN↑ (margin small) | IN | OUT |
| 05 | BLK5-0.7 | IN↑ .08→.21; .004→.11; .3 | IN↑ ≈0→.9→12→40; .37 | IN↑ 7.4→73 | IN 20 / 5 | IN↑ 1.8→.6, −.20→−.45 / IN | IN↑ | IN | OUT |
| 06 | BLK5-0.85 | IN↑ .04→.11; .003→.057; .15 | IN↑ ≈0→≈0→4.8→14; .19 | IN↑ 3.9→37 | IN 20 / 5 | IN↑ 2.5→.84, −.28→−.54 / IN | IN↑ | IN | OUT |
| 07 | BLK√p-0.5 | IN↑ .10→.31; .006→.14; .5 | IN↑ ≈0→.4→14→55; .53 | IN↑ 10→104 | UNCL 180→508 / 45→127 [n^0.5 = √p block, by design] | sp UNCL 12→14, +.57→+.47 / cl IN 4.2→3.9, +.05→−.05 | IN↑ | IN | OUT |
| 08 | TOEP α=1 | IN↑ .12→.32; .005→.15; .39 | IN↑ ≈0→7.5→27→80; .61 | IN↑ 5.4→120 | UNCL 207→508 [n^0.43] / 33→76 [n^0.40] | sp UNCL 10.6→12, +.67→+.57 / cl IN 2.6→2.1, +.04→−.06 | IN↑ | IN | OUT |
| 09 | TOEP α=2 | IN↑ .15→.48; .005→.20; .65 | IN↑ ≈0→11→47→131; .88 | IN↑ 7.4→172 | IN 32→53 [n^0.24] / 8→11 | IN↑ 2.1→1.2, −.01→−.22 / IN | IN↑ | IN | OUT |
| 10 | FAC a=.5 k=1 | IN↑ .15→.54; .006→.22; .97–.99 | IN↑ .003→139; .93→.97 | IN↑ ≈0→12→147 | IN 4 / 4 (= S₀ at every n at p = 10n; at p = n from n = 800) | IN 0; −.63→−.71 / IN | IN↑ | IN | OUT |
| 11 | FAC a=.5 k=3 | IN↑ .15→.54; .006→.22; .97–.99 | IN↑ .08→149; .93→.97 | IN↑ ≈0→13→154 | IN 4 / 4 (as D10) | IN 0; −.61→−.74 / IN | IN↑ | IN | OUT |
| 12 | FAC a=.75 k=1 | IN↑ .14→.52; .006→.21; .87–.92 | IN↑ ≈0→5.8→51→120; .60→.74 | IN↑ .39→169 | OUT [p] / [p] | OUT ≈9–17 flat, +.79→+.81 / OUT | IN↑ | IN | OUT |
| 13 | FAC a=.75 k=3 | IN↑ .15→.52; .006→.21; .87–.92 | IN↑ ≈0→8.5→40→113; .60→.74 | IN↑ ≈0→7.8→57→156 | OUT 600→16000 (= p at 1600) / [p] | OUT / OUT | IN↑ | IN | OUT |
| 14 | FAC a=1 k=1 (cs .5) | IN↑ .08→.27; .003→.11; .5 | **OUT** 5e-7→.012→.019→.10; pop 0 | IN↑ 2.9→100 | OUT [p] / [p] | OUT / OUT | IN↑ | IN | OUT |
| 15 | FAC a=1 k=3 | IN↑ .09→.28; .003→.12; .5 | **OUT** ≈1e-11 at every n; pop 0 | IN↑ ≈0→1.5→13→51 | OUT [p] / [p] | OUT / OUT | IN↑ | IN | OUT |
| 16 | S5 (0.3 global + blocks) | IN↑ .07→.21; .003→.10; .3 | IN↑ (small margin) ≈0→.9→6.9→16; .062 | IN↑ 7.8→72 | OUT [p] / [p] | OUT / OUT | IN↑ | IN | OUT |
| 17 | S6 (blocks ρ .4–.9) | IN↑ .05→.09; .002→.044; .1 | IN↑ ≈0→5.7→5.0→67; .25–.49 | IN↑ 14→136 | IN 20 / 5 | IN↑ 1.5→.5, −.18→−.47 / IN | IN↑ | IN | OUT |
| 18 | riboflavin-like | IN↑ small .04→.09; .002→.039; .1 | **OUT** ≈0 at every n; pop ≈0 | **OUT** ≈0 at every n; pop ≈0 | OUT [p] / [p] → one copy (4088) | OUT 13→25, +.74→+.77 / OUT | IN↑ (margin smaller) | IN | OUT |
| 19 | FRED-QD-like | IN↑ small .05→.09; .002→.048; .1 | UNCL↑ ≈0→.19→5.2→42; pop .24–.30 | IN↑ (small margin) .11→14; pop .076 | IN (bounded by tiles) 628→679 / 170 | sp UNCL 14→19, +.77→+.60 / cl UNCL↑ 18→8.3, +.52→+.04 | IN↑ | IN | OUT |

Notes. P3 (floor on Q̂ ∪ {l}, computed where Q̂ fits the lattice cap) rises with n wherever computed (p = 10n slopes +0.07
to +0.83). P7: the BM rate θ_min²nφ̂₀²/log n and the margin Δ̂/log n grow like n^1.1–1.4 along p = 10n and n^0.7–1.15
along p = n, in every design and placement; M̂ is bounded. P8: 𝒪¹_n/r_n (j = 1, 2 terms) = 1.085 → 0.920 at p = 10n and
1.08 → 0.92 at p = n, the same in every design; bounded and decreasing. P10: δ̂_n√(p log log n) grows like n^0.55–1.1.
The p = n series agrees with the table on every verdict except where noted in the cells (D10/D11 leak set, which at
p = n is [p] at n ≤ 400 and S₀ from n = 800; D19 spread, whose population visibility at p = n is ≈ 0 at n = 200 and
0.15 at n = 1600, because the truths fall in one or several 170-column tiles depending on p).

## The open question from the pilot: does visibility / the m♯ floor recover at p = 10n?
- **m♯ floor: yes, in all 19 designs.** p = 10n: 0.001–0.006 at n = 200 → 0.014–0.22 at n = 1600 (log-log slopes
  +1.1 to +1.8). Smallest at n = 1600: AR(0.95) 0.014, riboflavin-like 0.039, S6 0.044, FRED-like 0.048. Cap
  p = 2·10⁴: 4e-5–3e-4 at n = 200 → 0.008–0.08 at n = 800, rising in every design.
- **Visibility, spread truth: yes by n = 800 in 15 designs** (v̂ ≥ 4.8 at n = 800 and 14–149 at n = 1600: IND, AR(0.5),
  AR(0.8), both fixed blocks, growing blocks, both Toeplitz, all four weak/medium factors, S5, S6, FRED-like), and at
  n = 1600 only for AR(0.95) (0.45; population margin 0.05). **No for D14 and D15** (strong factor, mixed signs: 0.10
  and ≈ 0 at n = 1600; population value 0, a masking set cancels the truth's covariance with the signal) **and D18**
  (riboflavin-like; population ≈ 0).
- **Visibility, clustered (aligned) truth: yes in 18 of 19** (including the strong factors, D14 2.9 → 100, D15 → 51);
  **no for D18**.
- **p/n matters for the onset.** At the cap p = 2·10⁴ (p/n = 100, 50, 25), spread v̂ is still < 0.05 at n = 400 in
  10 designs (AR(0.8), AR(0.95), both fixed blocks, growing blocks, both strong factors, S6, riboflavin- and FRED-like),
  and < 1 at n = 800 in AR(0.95), FAC a=1 k=1/k=3 and riboflavin-like. The mechanism at small n (checked by explicit projections, pilot): with p ≫ n, a greedy masking
  set of ≤ 15 columns can cancel the gain ‖(P_{U∪j} − P_U)μ‖²; this sample effect fades as n grows unless the population
  visibility is itself 0.

## Pre-announced items (plan §2)
- Global CS / strong factors give Q̂ = [p]: **confirmed** (D12–D16, D18).
- (AG) outside for p ≥ n: **confirmed** (outside in every design, at p = n as well).
- Floors fail at the smallest n and recover with n: **confirmed** for the m♯ floor at p = 10n and at the cap.

## Track B cross-check (lines handed to the audit Fable; also appended at the end of `TRACK_B.md`)
- B5 floor: **confirms** "all inside" (sample floors rise with n at p = 10n and at the cap in all 19 designs).
- B6 collinearity: **confirms** "all inside" (Occam term bounded and decreasing at p = 10n).
- B8 visibility: **confirms** inside for IND, AR, blocks, S6, aligned factors; outside for mixed-sign strong factors and
  riboflavin-like. Refines two "unclear" entries: S5-type (D16, 4 mixed-sign truths) has a small positive population
  margin (0.06) and rising sample v̂; FRED-like is inside with tiled copies (population 0.08–0.30, sample rising).
- B9 leakage: **confirms** inside/outside for every design it lists. **Corrects** the Track-C sentence on AR(0.95): at
  p = 10n the leak set grows ≈ n^0.1 (466 → 585), not n^0.4–0.5 (that p = n value was capped by p = n = 200). Toeplitz
  α = 1 (n^0.4) and growing blocks (n^0.5) are confirmed.
- B10 floor on Q ∪ {l}, local regressions: **confirms** inside for IND, AR(0.5), blocks, S6; AR(0.8) spread unclear and
  improving (width +0.50 → +0.005).
- B11 no leakage: **confirms** inside only where Q̂ = S₀. **Corrects** "the leak set equals S₀ for IND only": it also
  equals S₀ for the weak factors (a = 0.5; common correlation 0.5 p^{-1/2}) once that correlation is below √(log n/n)
  (every n at p = 10n). None of the study, P6 or 1M designs is of that kind, so no design verdict changes.

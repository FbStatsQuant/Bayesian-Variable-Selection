# W3-AUDIT track C — RESULTS (internal; not for the paper)

Lead: Opus 5.5 (high), 2026-11-16. Plan `work/C_PLAN.md` v3 (HQ rule 11-16: qualitative conditions and their trend
in n; explicit constants from the proof are conservative and are not tested). Proxy computations only, no SMC fits.
**Status: Owls part complete** (p ≤ 2000: cells (n, p) = (200,200), (400,400), (800,800), (1600,1600), (200,2000);
19 designs × 10 replicates × 2 truth placements; 0.30 core-h). **NOTS part pending** (p ≥ 4000, 6 cells; package
`track_C/nots/`). The p = 10n trend columns are filled from NOTS later; pilot single-replicate hints are marked *(pilot)*.

Data: `/home/fb31/SMC_Theory_Department/helpers/W3-AUDIT-C/owls_out/` (95 task CSVs) →
`collect_owls/summary.csv` (median, q10, q90 over replicates) and `collect_owls/trend.csv` (log-log slope in n).
Copies of both CSVs: `track_C/owls_summary.csv`, `track_C/owls_trend.csv`.

## How to read
Trend is along the p = n series, n = 200 → 1600 (log-log slope in brackets). **IN↑** = inside, improving with n;
**IN** = inside, bounded/flat; **UNCL↑** = unclear now, moving toward inside; **UNCL** = unclear; **OUT** = outside.
Search-based floors and visibility are upper bounds (they can refute, not certify); population floors are certified by
λ_min(Σ) > 0; P5 leak sets are subsets (never "inside", only "not refuted"; written IN for brevity). sp = spread truth
(study positions, signs + − + −), cl = clustered (four adjacent columns, aligned signs).

## Table (Owls part)
| D | design | P1–P3 floors: sample φ̂²(k=16) at n=1600 [slope]; pop λ_min(Σ) | P4 visibility v̂ = δ̂²/log n (sample) / pop | P5 leak size \|Q̂\| (pop, ε=0.2), n=200→1600 | P6 local-regression ℓ¹ tail (ν=4, q99) | P9 width 𝔴̂⁰ | P7 BM rate, margin/log n | P8 𝒪¹/r_n | P10 |
|---|---|---|---|---|---|---|---|---|---|
| 01 | IND | IN↑ 0.60 [+.42]; 1 | IN↑ both [+1.5] / 1 | IN 4 → 4 | IN 0 | IN −0.77 | IN↑ | IN | OUT |
| 02 | AR0.5 | IN↑ 0.29 [+.28]; 0.33 | IN↑ both / 0.6 | IN sp 32→46, cl 8→10 (slow) | IN↑ 2.5→1.2 | IN↑ sp +.02→−.19 | IN↑ | IN | OUT |
| 03 | AR0.8 | IN↑ 0.10 [+.19]; 0.11 | IN↑ (sp 0.005→26) / 0.22 | IN sp 109→137, cl 19→23 (slow) | IN↑ 18→6.5 | sp UNCL↑ +.54→+.02; cl IN | IN↑ | IN | OUT |
| 04 | AR0.95 | IN↑ but small 0.024 [+.23]; 0.026 | sp UNCL↑ (≈0 to n=800, 0.7 at 1600); cl IN↑ / 0.05 | sp UNCL 200→585 (n^0.5); cl IN 70→87 | sp UNCL; cl IN↑ 22→8 | sp UNCL↑ +.79→+.52; cl IN↑ | IN↑ (margin small, 1.6→10) | IN | OUT |
| 05 | BLK5-0.7 | IN↑ 0.22 [+.33]; 0.3 | IN↑ both / 0.37 | IN 20, 5 (bounded) | IN↑ 1.8→0.6 | IN | IN↑ | IN | OUT |
| 06 | BLK5-0.85 | IN↑ 0.11 [+.33]; 0.15 | IN↑ both / 0.19 | IN 20, 5 | IN↑ | IN | IN↑ | IN | OUT |
| 07 | BLK√p-0.5 | IN↑ 0.34 [+.39]; 0.5 | IN↑ both / 0.53 | UNCL sp 60→160, cl 15→40 (n^0.5 = block size √p, by design) | IN (flat ≈5 sp, ≈1 cl) | sp UNCL↑ +.26→+.07; cl IN | IN↑ | IN | OUT |
| 08 | TOEP α=1 | IN↑ 0.34 [+.30]; 0.39 | IN↑ both / 0.61 | UNCL sp 180→508 (n^0.5), cl 33→76 (n^0.4) | sp UNCL ≈10–20; cl IN 2.6→2.1 | sp UNCL +.77→+.61; cl IN weak (−.02→−.11) | IN↑ | IN | OUT |
| 09 | TOEP α=2 | IN↑ 0.52 [+.37]; 0.65 | IN↑ both / 0.88 | IN sp 32→53 (n^0.24), cl 8→11 | IN↑ | IN↑ | IN↑ | IN | OUT |
| 10 | FAC a=.5 k=1 | IN↑ 0.59 [+.43]; 0.97–0.99 | IN↑ both / 0.79–0.99 | IN↑ Q̂ = [p] at n ≤ 400, = S₀ from n = 800 (weak factor falls below √(log n/n)) | IN (0 from n = 800) | IN from n = 800 | IN↑ | IN | OUT |
| 11 | FAC a=.5 k=3 | IN↑ 0.59; 0.97–0.99 | IN↑ both / 0.79–0.99 | IN↑ as D10 | IN from n = 800 | IN from n = 800 | IN↑ | IN | OUT |
| 12 | FAC a=.75 k=1 | IN↑ 0.56 [+.44]; 0.87–0.92 | IN↑ both / sp 0.38→0.58 | OUT Q̂ = [p] | OUT (≈9–17, flat) | OUT +0.84 flat | IN↑ | IN | OUT |
| 13 | FAC a=.75 k=3 | IN↑ 0.56; 0.87–0.92 | IN↑ both / sp 0.38→0.58 | OUT Q̂ = [p] | OUT | OUT +0.83 | IN↑ | IN | OUT |
| 14 | FAC a=1 k=1 (cs .5) | IN↑ 0.30 [+.40]; 0.5 | **sp OUT** (pop 0; sample 4e-4→0.13); cl IN↑ / 0.53 | OUT Q̂ = [p] | OUT | OUT +0.85 | IN↑ | IN | OUT |
| 15 | FAC a=1 k=3 | IN↑ 0.32 [+.42]; 0.5 | **sp OUT** (pop 0; sample ≈1e-10, falling); cl IN↑ / 0.54 | OUT Q̂ = [p] | OUT | OUT +0.86 | IN↑ | IN | OUT |
| 16 | S5 (0.3 global + block) | IN↑ 0.22 [+.32]; 0.3 | IN↑ both (sp 0.55→18) / sp 0.06, cl 0.36 | OUT Q̂ = [p] (global factor) | OUT | OUT +0.84 | IN↑ | IN | OUT |
| 17 | S6 (blocks ρ .4–.9) | IN↑ 0.16 [+.34]; 0.1 | IN↑ both (sp ≈0 at n = 200 only) / 0.25–0.71 | IN 20, 5 | IN↑ 1.5→0.5 | IN | IN↑ | IN | OUT |
| 18 | riboflavin-like | IN↑ but small 0.09 [+.21]; 0.1 | **OUT both** (pop ≈0; sample ≈0 at every n) | OUT Q̂ = [p] | OUT (≈13–21) | OUT +0.85 | IN↑ (margin 4→35) | IN | OUT |
| 19 | FRED-QD-like | IN↑ but small 0.09 [+.23]; 0.1 | sp UNCL↑ (≈0 to n = 400, 10.7 at 1600; pop 0.15); cl IN↑ / 0.08 | UNCL whole 170-blocks: sp 170→672 (= 4 tiles × 170, then bounded), cl 170 | sp UNCL ≈17–19; cl IN↑ 17→8 | sp UNCL +.73→+.61; cl UNCL↑ +.75→+.13 | IN↑ | IN | OUT |

Rows P2 (unanchored floor at the size cutoff m♯_n, m♯ = 49–80) and P3 (FL-Q, where Q̂ fits the lattice cap) follow
the P1 column: rising in n in all 19 designs (P2 slopes +0.46 to +0.68), at levels 0.017–0.35 at n = 1600.
P7: BM rate θ_min²nφ̂₀²/log n and margin Δ̂/log n grow like n^0.7–1.15 in every design and placement; M̂ is bounded.
P8: 𝒪¹_n/r_n (j = 1 and 2 terms) = 1.08 → 0.92, the same in every design (the j = 1 term is design-insensitive at
p = n); bounded and decreasing, not refuted. P10: δ̂_n√(p log log n) grows like n^0.55–1.1 everywhere (pre-announced).

## p = 10n (Owls only n = 200; NOTS gives n = 400–1600)
At (n, p) = (200, 2000) the sample visibility v̂ collapses to ≈ 0 (< 1e-4) in most designs (spread: 16 of 19; clustered: 5 of
19), and the m♯-size floor is ≈ 0.001–0.006 in every design. Checked by explicit projections: a greedy masking set of
≤ 15 columns from p ≫ n candidates cancels the truth column's gain ‖(P_{U∪j} − P_U)μ‖² (not a numerical artefact).
*(pilot, 1 replicate)* At large p this recovers with n for IND (v̂ ≈ 0 → 67 → 180 at (n, p) = (200, 2·10⁴),
(800, 2·10⁴), (1600, 16000); m♯ floor 0.0002 → 0.08 → 0.21) and block D05 (v̂ 38 at n = 1600), but not for the strong factor with the spread truth
(D14: v̂ 0.012 at n = 1600). The NOTS cells settle this trend.

## Top findings (Owls part)
1. **Sparse floors are inside and improve with n in all 19 designs** (anchored k ≤ 16, at the size cutoff m♯, and Q̂ ∪ {l});
   population floors are certified by λ_min(Σ) ≥ 0.026. Levels are small for AR(0.95), riboflavin- and FRED-like
   designs (≈ 0.02–0.09 at n = 1600) but rising.
2. **Visibility (V)/(V-R) = PTV fails at the population level for the strong-factor designs with the spread (mixed-sign)
   truth (D14, D15) and for the riboflavin-like design (both placements):** a masking set drives the truth column's
   conditional covariance with μ to 0 (sign cancellation), and the sample v̂ does not grow. Clustered aligned truths in
   factor designs are inside. Same mechanism as the NEG regime of W3-P6.
3. **Leakage size:** bounded for IND, fixed blocks, AR(≤ 0.8), Toeplitz α = 2, S6; growing like n^0.4–0.5 for
   AR(0.95) spread, Toeplitz α = 1 and growing blocks; Q̂ = [p] for factors with a ≥ 0.75, S5 (global factor) and
   riboflavin-like (pre-announced: global CS and strong factors). Weak factors (a = 0.5) move inside by n = 800.
   The width (P9) and local regressions (P6) follow the same split.
4. **β_min rate, margins, Occam term: inside everywhere** (rates grow ≈ n/log n; 𝒪¹/r_n bounded and decreasing).
5. **(AG) operator bound is outside in every design** (pre-announced; ‖R̂ − Σ‖_op ≳ √(p/n)).
6. **p ≫ n at small n:** visibility and the m♯ floor collapse at (200, 2000); pilot cells suggest recovery by
   n = 800–1600 except in strong-factor spread designs. Pending NOTS.

## Pre-announced items (plan §2)
- Global CS / strong factors give Q̂ = [p]: **confirmed** (D12–D16, D18; also the medium factor a = 0.75).
- (AG) outside for p ≥ n: **confirmed** (outside even at p = n).
- Floors fail at the smallest n and recover: **confirmed for p = 10n at n = 200 (m♯ floor ≈ 0)**; at p = n they are positive
  from n = 200.

## NOTS cells (pending)
Rows to add when Engineering returns `/scratch/fb31/SMC_Theory_Department/W3-AUDIT-C/out/`: p = 10n series
(n = 400, 800, 1600) and the p = 2·10⁴ cap at n = 200, 400, 800. Collect with
`python3 scripts/c_collect.py <owls_out> <nots_out> --to <dest>`.

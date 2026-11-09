# N_T2 — Target 2 numerics: exact-Gram one-factor designs with r = 1, 2, 3 loading classes

All runs: exact Gram X'X = (n − 1)Σ, Σ = λλᵀ + diag(1 − λ²), uncapped production LS0 path (best strict improvement,
exact ties → lexicographically smallest set) from the full set [p], closed-form scorer `eg_core.py` (T2/L4r_path.md
§L4r.0). σ = 1.

## 0. Validation of the closed form (`eg_selftest.py` → `eg_selftest_out.txt`)

* F_closed(U) = F_direct(U) (matrix slogdet/solve) to relative 1.3·10⁻¹⁴ (n ≤ 10⁷, 4 designs, 240 random U).
* First-move gains equal the direct best neighbour gain to 1.4·10⁻⁹.
* Full paths: **32/32 identical move sequences** between `eg_path` (closed form, swaps maximised per class via outside
  extremes) and the general production-path code `../../numerics/iid_core.ls0_path` run on the explicit matrix
  X'X = (n − 1)Σ (n ∈ {10⁴, 10⁶}, p ∈ {40, 120}, loadings {0.2, 0.95}, {0.3, 0.9}, {0.2, 0.6, 0.95}, CS); max gain
  difference 2·10⁻¹⁰.

## 1. Main grid (`run_t2.py T2_raw.jsonl main`, 216 runs) and stress grid (`run_t2.py T2_stress_raw.jsonl stress`, 150 runs)

Main: 9 designs × truths {s1lo (one truth in the lowest class), s1hi, s3mix} × n ∈ {10⁶, 10¹⁰} × p ∈ {300, 1500} × 2 seeds.
Stress: {0.1, 0.98}, {0.2, 0.95} with 90/10 and 80/20 class shares, {0.2, 0.6, 0.95}, CS × 3 truths ×
(n, p) ∈ {(10⁴, 10³), (10⁴, 3000), (10⁵, 3000), (10⁸, 4000), (10¹⁴, 4000)} × 2 seeds (log p/log n up to 0.87).
Tables: `py -3.13 summarize.py T2_raw.jsonl T2_stress_raw.jsonl` (verbatim below; cr := max_c ℓ_c|X_T|/H̄ over the
path, H̄ = max null |ξ|; "bulk" = steps with m ≥ 30 kept nulls; Δ_c = per-class hole asymmetry |R_c − L_c|).

```
== T2_raw.jsonl 216 runs; pure deletion 216 ; final S0 216 ; runs with interval-hole violation 0 ; ties 0
design         R     A_S     max lp/ln  S0/runs  max add/ln  min del/ln  max sw-del  max truth  viol  max cr  bulk max|X|/H  bulk max D_c/(2l_c H)  bulk 1-sided steps
cs05             1.0 0.1667  0.53       24/24   -0.398     +0.398     -6.62     -1.7e+05  0     0.40    0.066          0.044                  0
r2_02_095       14.9 0.0020  0.53       24/24   -0.177     +0.177     -3.11     -3.8e+04  0     1.07    0.032          0.243                  0
r2_02_095_lo    14.9 0.0020  0.53       24/24   -0.292     +0.292     -4.12     -3.8e+04  0     1.67    0.039          0.140                  0
r2_02_095_hi    14.9 0.0020  0.53       24/24   -0.216     +0.216     -3.21     -3.8e+04  0     0.96    0.024          0.695                  30
r2_03_09         6.6 0.0089  0.53       24/24   -0.353     +0.353     -5.66     -7.2e+04  0     1.37    0.043          0.183                  0
r2_05_095        5.3 0.0131  0.53       24/24   -0.271     +0.271     -4.58     -3.8e+04  0     1.33    0.025          0.107                  0
r2_06_08         1.8 0.0744  0.53       24/24   -0.377     +0.377     -6.53     -1.3e+05  0     0.49    0.072          0.102                  0
r3_02_06_095    14.9 0.0020  0.53       24/24   -0.287     +0.287     -5.41     -6.5e+04  0     1.55    0.045          0.343                  2
r3_03_05_09      6.6 0.0089  0.53       24/24   -0.434     +0.434     -6.15     -1.2e+05  0     1.20    0.074          0.349                  21
== T2_stress_raw.jsonl 150 runs; pure deletion 150 ; final S0 150 ; runs with interval-hole violation 0 ; ties 0
r2_01_098       49.0 0.0002  0.87       30/30   -0.153     +0.153     -1.71     -1.5e+02  0     1.75    0.020          0.374                  0
r2_02_095_vlo   14.9 0.0020  0.87       30/30   -0.381     +0.381     -4.61     -4.1e+02  0     1.62    0.060          0.122                  17
r2_02_095_lo    14.9 0.0020  0.87       30/30   -0.319     +0.319     -3.12     -3.9e+02  0     1.20    0.032          0.086                  0
r3_02_06_095    14.9 0.0020  0.87       30/30   -0.062     +0.062     -0.78     -6.4e+02  0     1.61    0.032          0.227                  0
cs05             1.0 0.1667  0.87       30/30   -0.345     +0.345     -3.74     -1.7e+03  0     0.32    0.055          0.036                  0
```

**Findings.** (i) **366/366 paths are pure null deletions ending at S₀**, no ties, every addition negative, every
null-out swap below the chosen deletion, every truth move hugely negative — including λ ∈ {0.1, 0.98} (R = 49) and
log p/log n = 0.87, far outside the proved range A_S (0.0002–0.17). (ii) **Per-class interval holes hold exactly at
every step of every run** (0 violations: each class's deleted set is an interval of that class's sorted ξ's containing
the class centre ℓ_cX_T) — consistent with L4r.4 (the crossing criterion needs an O(n^{−1/2}) near-coincidence in the
bulk). (iii) **The FACB bulk invariants fail per class**: classes become one-sided during the bulk (up to 30 steps with
m ≥ 30 in r2_02_095_hi; per-class B1 false), and the per-class asymmetry Δ_c/(2ℓ_c) reaches 0.70H̄ while |X_T| ≤ 0.074H̄
— the static per-class B3 bound X ≤ max_c Δ_c/(2ℓ_c) (L4r.5) is valid but off by an order of magnitude.
(iv) **No centre-ratio invariant**: cr = max_c ℓ_c|X_T|/H̄ reaches 1.75 in the end phase (the high-loading class's
centre lies beyond all its points); additions still lose because their statistic carries the factor
D'_T/(D'_T + ℓ_c²) (L4r.0(c)).

## 2. Adversarial sets T (`adversarial_T.py` → `adversarial_T_out.txt`)

T_m = S₀ ∪ {the m lowest-class nulls with the largest positive ξ}: sets the path never visits. Lemma L4r.2(a) (a kept
null with |τ| ≤ H̄ + |ϱ|/ℓ'_lo) and L4r.2(b) (centre bound) hold on all of them. The best addition gain at these sets is
**positive** whenever log p/log n is well above A_S (e.g. CS at 0.33: +0.083 log n; {0.2, 0.95} at 0.155: +0.115 log n;
at 0.55: +8.7 log n), and negative for CS at 0.155 < 1/6 (−0.384 log n). So the uniform-over-T route of Theorem T2-S
**cannot** be pushed past (roughly) A_S: beyond it, any proof must use where the path goes.

## 3. End phase versus FACB (E-side) (`end_phase_detail.py` → `end_phase_detail_out.txt`)

Over the last 40 kept nulls (4 seeds, n = 10⁶, p = 1500): "minority deletions" (deleted null on the opposite side of the
centre shift, |X_T| > 0.05H̄) occur **0 times in CS and up to 13/160 times in two-class designs** (r2_02_095_lo,
r2_06_08). Detail (r2_02_095_lo): near balance the lowest-loading class is deleted on both sides alternately,
irrespective of sign(X_T) — the smallest-(1 + γ'_c) class goes first (L4r.6). FACB's monotone imbalance argument
(|I_{i+1}| ≤ |I_i|) has no direct analogue; nevertheless every path ends at S₀.

## Files

eg_core.py, eg_selftest.py (+_out), run_t2.py, summarize.py, T2_raw.jsonl, T2_stress_raw.jsonl, run_t2_log.txt,
run_t2_stress_log.txt, adversarial_T.py (+_out), end_phase_detail.py (+_out).

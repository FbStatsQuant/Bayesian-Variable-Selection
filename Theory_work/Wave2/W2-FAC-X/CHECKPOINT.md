# W2-FAC-X — CHECKPOINT (key lemma checked), 2026-11-09 ~09:45 CST

Scope (after HQ update 09:22): Target 1 (iid Gaussian rows, compound symmetry, largest exponent) and Target 2
(general one-factor loadings). k ≥ 2 moved to W2-FAC-K2.

## Target 1 — Theorem FAC-CS-iid (STATEMENT v3, LOCKED)
Model: rows iid N(m, Υ[(1 − ρ)I + ρ11ᵀ]Υ), fixed raw coefficients, s₀ ≥ 1 fixed, (FS), **limsup log p/log n < 1/2**
(3× FAC-A's 1/6). Claims: (C1) start mode = [p] ∖ N₀; (C2) LS0 path from S*(N) is a pure null deletion of
ϖ-approximate argmins with band-controlled holes (width 4.3ϖ_n, ϖ_n = C H̄√(p log n/n) + n^{−1/3}), ends certified at S₀,
for all |N| ≤ 15 simultaneously; (C3) D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 under the joint law; (C4) delivery P(Ŝ⁺ = S₀) → 1.
Method unchanged (merged v3.1, MR1 cap essential, as in FAC-B).

Mechanism: exact rotation representation (X1): noise coordinates ξ iid N(0,1) **independent** of the idiosyncratic
Wishart W; the iid score = FAC-B's 1-D scan + perturbation δ; X2 bounds δ on band-structured sets (union bounds only
over ξ-defined intervals, crude bounds on band/N₀ points); X3 (deterministic) shows ϖ-approximate argmin deletions with
the exact drift identity keep the hole an interval up to a 4.3ϖ band (crossings only while the hole is < 4ϖ wide, a
phase of ≤ Q steps under a density hypothesis); X4 runs FAC-B's L4 by induction on established prefixes. A < 1/2 enters
only through absorbing the band term p H̄√(log n/n)·ϖ into ϖ.

| lemma | status | check |
|---|---|---|
| X1 representation, gains | PROVED (by this seat, unchecked) | R03 V-W-A (minor, applied) |
| X2 perturbation, event | PROVED (by this seat, unchecked) | R03 V-W-A (4 minor, applied) |
| X3 soft gap (deterministic) | PROVED (by this seat, unchecked) | R03 FAILED on (iii) as written (MAJOR) → repaired per R03; re-check R03b running |
| X4 path (key lemma) | PROVED (by this seat, unchecked) | R04 Sol xhigh V-W-A, no FATAL/MAJOR (7 minor, applied) |
| X5 start mode | PROVED (by this seat, unchecked) | R05 V-W-A (2 MAJOR: raw-design conditioning, two-sided event — applied) |
| X6 assembly, delivery | PROVED (by this seat, unchecked) | R05 V-W-A (applied) |
Statement lock: R01 REJECT → R02 LOCK-WITH-CHANGES → v3 locked. Numerics: N1X 121/121 paths (up to A = 0.75), N3X 0
violations (480 adversarial runs), N5X 48/48 start modes, iid self-test ≤ 4·10⁻⁸.

Next: R03b → independent mid-point (fresh Sol xhigh) → exhaustive sweep → citation check → council.
Estimate: Target 1 should close (PROVED-CHECKED) if mid-point/sweep find nothing structural.

## Target 2 — general one-factor loadings (not yet locked)
Diagnosis N2X (64/64 paths fine, exact reference and iid): the path is the argmin of the **variable-centre** statistic
|ξ_j − ℓ_jX_T|/norm_j (ℓ_j = λ_j/√(1 − λ_j²), one scalar X_T); a common centre does not describe it. Plan: (a) a
corollary of the Target-1 machinery for near-equal loadings (max_j|λ_j − λ̄| ≤ n^{−c}: the dispersion enters δ as
O(Δλ·H̄) and is absorbed in ϖ); (b) finitely many loading classes, exact Gram — a parallel Opus prover is working on it
(per-class interval holes are exact; the open steps are the per-class centre bound and the weighted end-phase
dynamics, which may need a condition on ℓ_max/ℓ_min); (c) otherwise the exact obstruction for fixed dispersion: the
variable centres create a band of width ≍ Δℓ·|X_T| ≍ Δℓ·ε_bH, too wide for the balance argument.
Requested from W2-SIM (numerics/SIM_REQUEST.md): frontier A ∈ [0.5, 0.9] for CS and fixed-dispersion loadings at large p.

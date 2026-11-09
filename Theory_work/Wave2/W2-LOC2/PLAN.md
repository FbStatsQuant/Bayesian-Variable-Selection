# W2-LOC2 — PLAN

## Diagnosis (done, numerics/D1_SUMMARY.md)
74 component-port runs (observations only, not proof; R01-5) (2-D exponential grid, 2-D separable AR(1), polynomial Toeplitz α = 1.5, 3, middle-regime
equicorrelated blocks): start modes grow faster than log n (d = 2, middle regime); LS0 deletes extras one per move and
ends certified at S₀ in every run; estimated whole-lattice NA supremum exceeds the path maximum only by a bounded amount.
Conclusion: whole-lattice NA is plausible with a bound sup_T Z_{T,l} ≤ √(2 log p) + O(√log|Q|) — no path restriction needed.

## Mechanism (the new idea)
GROW/LOC NA routes pay for the lattice: (G4-χ) adds χ²_{|𝒫|}; LOC's window route (APP L3.6) controls the far part of
the residual by a χ² union bound over 2^{|Q|} sets, which costs √|Q| — fine for |Q| = O(log n), fatal for (log n)^d.
NA-R instead writes the population residual e_{T,l} = (reference in a ≤ m₀-dim frame from a small family) −
(ℓ¹-bounded combination of ATOMS from a polylog set). The noise inner product of the atom part is bounded by
‖λ‖₁ · max over atoms, a union over |𝒜| (not 2^{|Q|}) terms: cost L√(2 log|𝒜|) = O(√log log n). The sample-vs-
population error is (|Q| + log p)/√n (exact identity (I − P_T)x_l ∝ (I − P_T)Ce_{T,l}; χ² with |Q| d.o.f.).
* LOC_d: reference = residual on the window T ∩ B(l, log log n) (2^{polyloglog} frames), atoms = the columns W_v, v ∈ Q,
  ℓ¹ bound from CT_d applied to principal submatrices (regression coefficients decay exponentially, summable in ℝ^d by
  the packing bound).
* One-factor groups: reference frame (F_G, ξ_l), atoms ξ_v, ‖β‖₁ ≤ 1/b_lo by Sherman–Morrison.
Everything else (sandwich, TL, regularity) is APP L3 / GROW L6 bookkeeping with (log n)^κ in place of log n, plus L0′.

## Steps
1. STATEMENT lock (Sol high) — R01.
2. Lemma files: L1 toolkit (L0′), L2 NA-R (key), L3 CT_d/CD_d (+ ℓ¹ regression bound), L4 LOC-d / LOC-BF (sandwich delta +
   verification of (R1)–(R3)), L5 assembly (Theorem PLR), L7 delivery. Falsification numerics per lemma
   (n4_nar_check.py: NA-R bound components on simulated designs; ct_d_check.py: CT_d constant vs exact inverses on 2-D grids).
3. Lemma checks: R02 (L1+L3, Sol high), R03 (L2 NA-R key, Sol xhigh), R04 (L4+L5+L7, Sol high).
4. CHECKPOINT.md after the key lemma check.
5. Mid-point (fresh Sol xhigh) R05. Sweep (Sol xhigh) R06. Citation check. Council (Sol xhigh + Opus high), ≤ 3 rounds.
6. Stretch (b) polynomial decay: L6_poly.md — lossy polynomial CT via banded approximation + CT; sandwich with
   polynomial reference families; target explicit α₀; delegate a parallel attempt to a Sol prover after L2 is checked.

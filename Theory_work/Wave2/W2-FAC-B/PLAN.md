# W2-FAC-B — PLAN

1. **Diagnosis (done, ≤ 1.5 h).** numerics/N1 (exact-Gram S5, one-/two-factor, p ≤ 400, n up to 10⁸), N2
   (saturated start p > n/2), N3 (compound symmetry, closed form, p up to 2·10⁴).
2. **Statement lock** (Codex gpt-6.1-sol high): STATEMENT.md + PLAN.md.
3. **Lemmas** (one file each in lemmas/):
   * L1 — CS reduction: exact closed forms of F for every set, of every neighbour's gain, the common centre x_T,
     data representation z_j = κ₀ + κ₁ξ_j (+ truth signal). Pure algebra; numerically checked (cs_selftest.py).
   * L2 — start mode (C1): population block increments under (FS), uniform sample control over the
     ≤ p·2¹⁶·16 (block, U, l) triples, one-flip improvement argument ⇒ unique maximiser S*.
   * L3 — the event E_n: order statistics of |ξ| (uniform m-th largest bound), extreme gaps, symmetric tail sums
     (sign symmetry + Hoeffding, uniform over thresholds), scale/RSS bounds, finitely many fixed coordinates
     (truths, N₀, η); P(E_n) → 1.
   * L4 — deterministic path lemma on E_n (key lemma): interval-hole invariant, asymmetry invariant (self-correcting
     drift), bulk bound on |x_T| (symmetric tail sums), end-phase balance (|N₊ − N₋| ≤ 1), margins for deletion
     improvement, NA, swaps, truth moves; S₀ certified.
   * L5 — assembly: (H0) on CS, [OP] + M5(0) + T03♯ ⇒ (C3); necessity of a cap ≳ |S̃₀|; Lemma CAP; delivery (C4)
     via Proposition F / A2 (Lemma S for CS designs, the K_n-route of A2 step 3).
4. **Falsification numerics per lemma** before downstream use (L1: cs_selftest; L2: start-mode = S* on N1/N3-type
   runs incl. a truth-complete block; L3: event components at moderate n; L4: N3 grid incl. s₀ = 1, ρ = 0.95,
   p = n/2 − 1, aligned and mixed signs).
4b. **Regimes in L4**: crude regime p ≤ n^{1/200} (includes bounded p; no balance argument) and growing regime.
4c. **Direct invariant test** (R02 item 4): numerics/n6_gap.py asserts the extended-gap invariant (C2)(iii) at every
   pre-move set incl. T_0 and one/two-extra states, and runs truth-complete-block cases started at S* with N₀ ≠ ∅
   (N₀ eligible for additions/swaps).
5. **Lemma checks** (cross-family, Codex Sol; xhigh for L4), **CHECKPOINT.md** after L4 is proved or after ~3 hours, whichever is first, **mid-point** (fresh Sol
   xhigh), **exhaustive sweep** (Sol xhigh), **council** (Sol xhigh + Opus high, both ≥ 8.0, all six gates),
   **citation check** script → reviews/CITECHECK.txt (before the council).
6. **Frontier**: REPORT section with the precise obstruction for S5 / general loadings / iid rows / p > n/2 and the
   method suggestion for p > n/2 (an LS0 cap allowing the swap phase), with N2 evidence, flagged as a finding.

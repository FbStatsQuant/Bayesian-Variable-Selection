# W1-T37R — REPORT (T37 truth dominance and greedy repair, restated)

All statements are candidates pending cross-family review. Long proofs: `PROOF.md`. Scripts: `scripts/`,
raw outputs: `results/`. (DRAFT — numerical sections are filled in below as runs finish.)

## 1. Headline

* PROVED (Prop 1): literal TD(d, m) is **unsatisfiable for every d ≥ 1** (on every design, every y up to a null
  set): at S = S₀ − j + l, TD(1) needs F(S₀+l) ≥ F(S₀) + m while TD(3) needs F(S₀+l) ≤ F(S₀) − m. D18 is not
  "generic failure" but an internal contradiction; T37(iii) as stated is false for d ≥ 1, T37(i) vacuous.
* PROVED (Lemma 0): the search is F-monotone and starts at the running best, so it can deliver S₀ only on
  E_LS = {S₀ unscored, F(S₀) > F(Ŝ_pre)}; on any posterior miss it cannot. The 0/541 repair count is forced.
* PROVED (Theorem A): refined T37(i) with TD′_∞ (no spurious local max + closure; iff) and TD′_P (every greedy
  move is progress, i.e. decreases |S Δ S₀|; swaps extra→truth count) on R_{a,d}; ≤ Φ(S) ≤ a + d moves, so the
  cap needs ℓ ≥ a + d, not s₀ + d; after certification Ŝ = S₀ without π(S₀) > ½.
* PROVED/PROOF SKETCH (Theorems B, C): lattice/path-wise finite-n bound with 2^{Φ(S_c)} states (no 2^{s₀});
  asymptotics need two named extra hypotheses (PGD: population greedy dominance; LD: local dependence of nulls).
  COUNTEREXAMPLE: SE + BM-∞ do not imply PGD (combination look-alike).

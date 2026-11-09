# W2-FAC-S5F — PLAN

Route: exact design-general tools + block-CS structure + level/centre bounds at the level scale (bulk), explicit
end-phase hypothesis (CC_θ) as the obstruction. Independent of W2-FAC-S5 (two-level gap invariant; not read).

## Lemma map (lemmas/)
* **L0 — exact general tools** (any exact-Gram design with λ_min(Σ) ≥ c_min > 0, T ⊇ S₀): gain reduction to RSS
  increments with O(1) error (L0.1); Pythagoras identity and jump inequality (L0.2); swap domination via one-below NA
  (L0.3); truth moves negative by order n (L0.4); size terms Δ_k (L0.5). Falsification: numerics/n3_tools.py.
* **L1 — block-CS structure**: ANOVA split of the fit; closed forms of add/deletion statistics (local part + global
  centre), variances; the centre as a posterior mean; the drift identity with explicit κ; the identity
  ỹ_G(U) ∝ Σ_{j∈U} Z^{loc}_j(U); local statistics as the a = 0 design's statistics (so L0.2 applies to them).
  Falsification: n3_tools.py (identities to machine precision), bcs_selftest.py.
* **L2 — start mode (C1)**: FAC-B L2 transplanted; population increments c(U, l) under (FS-B); zero pairs.
  Falsification: n4_start.py (bvs_core tables on exact-Gram S5).
* **L3 — probability events**: Gaussian maxima over configurations (p·2^q), order statistics (E4-type) of the
  configuration means, Laurent–Massart for RSS, independence across groups; P(E_n) → 1.
* **L4 — key lemma (C2), bulk**: level lemma (counting fully-large configurations; Chernoff across groups); centre
  bound at the level scale (top-#hit order statistics); hole bound via L0.2 within the group plus the centre; the four
  gain comparisons with margins c₂ log n; the regime split k ≤ n/log³n vs larger (M_T); definition of C₀, c₀.
  Falsification: n2_centre.py / n3_tools.py (level, centre and hole bounds monitored along paths).
* **L5 — end phase (C3)**: structural lemmas (mates of retained singletons harmless; group-level CS form; no
  all-extreme multi-member configurations); the conditional completion under (CC_θ) with the explicit A*(θ); swap
  analysis via L0.3 at the one-below sets. Numerics: n2_centre.py (θ observed), n5_end.py (end-phase configurations).
* **L6 — assembly (C4)**: as FAC-B L5 (H0; 𝒦_n; D_n; delivery), conditional on (C3) or unconditional for small p.

## Review pipeline
Lock (Codex Sol high) → L0–L1 check (Sol high) → L2–L3 check (Sol high) → L4 key-lemma check (Sol xhigh) → mid-point
(fresh Sol xhigh) → L5–L6 check → sweep (Sol xhigh) → council (Sol xhigh + Opus high). Citation check script before
the council. Every lemma: falsification numerics before downstream use.

## Numerics (numerics/)
bcs_core.py (+selftest) · n1_s5_paths.py (N1) · n2_centre.py (N2) · n3_tools.py (N3: identities, inequalities, level
and centre bounds) · n4_start.py (N4: start mode) · n5_end.py (N5: end-phase structure). SIM_REQUEST.md for W2-SIM
(large-p paths with the closed-form scanner).

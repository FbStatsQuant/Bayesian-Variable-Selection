# W3-SCR — PLAN

## Idea of the proof (SCR-A)
A locally optimal model has no strictly improving addition. If S (|S| ≤ q < K) misses a truth, the best missing truth
t has noiseless gain ≥ Γ_n(q) in the method's own quadratic form; the noise in that one-dimensional statistic is a
Gaussian with variance ≤ σ², and there are at most s₀N_q pairs (S, t), so uniformly the observed gain is
≥ (√Γ_n(q) − σ r_n)². One addition improves F as soon as its gain (in the units of the standardised response) exceeds
T_n ≈ 2 log p + log n: the prior ratio costs ≤ log(2p−1), the determinant ratio ≤ ½ log(n+1), and
ν log(1 + gain/RSS) ≥ gain/2 in those units. MC(q, x) makes the first exceed the second. Nothing about the search path.

## Lemma files
| File | Content | Used by |
|---|---|---|
| `lemmas/L1_score.md` | One-step identities for F (ridge/augmented geometry); bounds on prior and determinant ratios; D-add (sufficient condition for an improving addition), D-del (necessary condition for a non-improving deletion) | all |
| `lemmas/L2_noise.md` | Events: E1 (uniform one-dimensional noise bound), E2 (τ̂ two-sided), E3 (uniform χ² bounds over sparse subspaces) | A, C, R, N |
| `lemmas/L3_screening.md` | Proof of SCR-A, (A∞), Corollary A1 with explicit c₁ | — |
| `lemmas/L4_bridges.md` | Lemma B (B1, B2) | A1 |
| `lemmas/L5_exact.md` | L5.1 non-asymptotic exactness inequality; SCR-C; SCR-R | — |
| `lemmas/L6_sharp.md` | SCR-N | sharpness record |

## Numerics
- N0 fidelity (done): Python score vs core F; certified HPM is LO under the Python scan.
- N1 frequency: production core fits (`numerics/scr_fit.R`, core copy of main), designs iid / AR / equicorrelated /
  3-factor at p = 4n and p = 5n, strong and weak signals: how often {certified, |Ŝ| small}; S₀ ⊆ Ŝ on that event.
- N2 boundary violations (`numerics/n2_boundary.py`, own implementation of the coded search): hunt LO models from many
  starts; violate each assumption in turn (visibility by weak signal, by a masked pair; identifiability by a twin of a
  truth; the sparse floor by duplicated noise columns and by strong factors at p ≫ n; the size condition by large
  starts; the near-orthogonality floor of SCR-C by correlation).
- N3 lemma falsification (`numerics/n3_lemmas.py`): the identities and inequalities of L1, L4, L5 on random instances;
  empirical frequency of the events of L2 against their bounds.

## Reviews (Wave 3 protocol)
R01 statement lock (gpt-6.1-sol high) → ASSUMPTION_MAP.md + N2 + R02 "better theorem" (gpt-6-astra high) → proof →
R03 lemma checks L1-L4 (sol high) and R04 L5-L6 (sol high) → R05 mid-point (fresh, astra high; statement + proofs
only) → R06 sweep (astra high) → council C1 (gpt-6-astra high + Claude Opus 5.5 high on claudeAgent), max 3 rounds.

## Risks
- SCR-C needs first-order constants (2 log p vs 2 log p + log n); every o(1) must be explicit. If it does not survive
  review it is dropped without affecting SCR-A.
- The certificate may be rare in strong-factor designs at p ≫ n (LS0 from a dense start can end on its move cap);
  N1 measures it. The theorem is still valid, but its practical value there depends on that frequency.

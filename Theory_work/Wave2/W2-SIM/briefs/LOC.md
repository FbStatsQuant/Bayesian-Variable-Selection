# Family LOC — open local frontiers (informs a possible follow-up to W2-LOC2)
Family tag: `LOC` (RUN_ID prefix `loc_`). Concurrency allotment: **20** tasks. Folder `W2-SIM/LOC/`.

Read: `Theory_work/Wave2/W2-LOC2/` (REPORT.md — open: polynomial decay 1 < α ≤ 17/2 and long memory α ≤ 1; LOC-BF
covers one-factor groups of size up to (log n)^κ with ≤ one truth per group; polynomially growing groups not claimed —,
STATEMENT.md, lemmas/ headers, numerics/ incl. the component port and its runs), `W2-APP/REPORT.md` (Lemma VN),
`Theory_work/Wave2/W2-FAC-B/numerics/bvs_core.py` (general-design scorer, partition, start mode, local search).

## Questions
1. **Polynomial-decay Toeplitz** Σ_jk = (1 + |j − k|)^{−α} (and a positive-definite variant if this is not PD for small α —
   check the minimum eigenvalue and state the construction), α ∈ {1.5, 2.5, 4, 6, 8.5} and **long memory** α ∈ {0.5, 0.8}
   (e.g. fractional Gaussian noise / ARFIMA(0, d, 0) correlations, d ∈ {0.1, 0.25, 0.4}); iid Gaussian rows; n increasing
   (e.g. 500 → 2·10⁴ or as far as the general scorer allows; p = n/4 or p = n^{0.6}); truths spread out and truths
   adjacent. Per run: start-mode size |S̃₀| (and |S̃₀ ∖ S₀| as a function of n: polylog? polynomial n^{1/(2α)}?), LS0
   moves vs the MR1 cap ℓ_n + |S̃₀|, path type (pure deletion?), final == S₀, worst addition margin.
2. **Growing one-factor groups** g_n = n^b, b ∈ {0.2, 0.35, 0.5} (block-diagonal, within-group CS ρ ∈ {0.5, 0.8}, one and
   two truths per group): same statistics. Theorem LOC-BF covers g_n ≤ (log n)^κ with ≤ one truth per group; does the
   method still recover S₀ when g_n is polynomial, and when two truths share a group?
3. **Does the production method recover S₀** as n grows (subset of cells from 1 and 2, n ∈ {500, 2000, 8000} or as
   feasible): copy `W2-SIM/scripts/prod_fit.R` into your scripts dir (record sha256), add the designs (do not change the
   fit call or recorded fields), allocation large enough for the preflight (record it), 10 seeds. Pilot first; drop cells
   that cannot finish in 24 h (state which).

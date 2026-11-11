# W3-RM numerics — SPEC (sharpness gate: boundary-violation numerics)

Purpose (PROTOCOL item 3): simulate **just outside** each assumption of `../STATEMENT.md` and record whether the
theorem's *conclusion* still holds. If it does, the assumption is flagged `improvable`. These are falsification /
sharpness probes: **observations only, never proofs**; all theorems are asymptotic.

## Tools (import, do not edit)
Ported method objects (Python): `Theory_work/Wave1C/C-GROW/numerics/bvs_core.py` (score F, prior, `partition`,
`block_tables`, `start_mode`, `local_search` with complete scans, `ell_cap`, `exact_gram_design`, `iid_design_raw`,
`standardize_X`, `make_y_std`, `hpm_of`), helpers in `Theory_work/Wave1C/C-GROW/numerics/d_common.py`. A full worked
pipeline (start mode → LS0 with cap `ell_cap(n,p) + |start|` → endpoint/certified flags) is in
`Theory_work/Wave2/W2-UNI/numerics/n4_r2_pseudo.py` (and `W2-APP/numerics/n0_common.py`); copy its structure.
Write new scripts only in `Theory_work/Wave3/W3-RM/numerics/`. Local compute only; each experiment must finish in
≤ 15 minutes; ≤ 20 seeds per cell; seeds fixed and printed.

## Per-run record (every experiment)
n, p, seed, design parameters; start mode S̃ (size, S₀ ⊆ S̃?, |S̃ ∖ S₀|, list of extras by type); LS0 from S̃ with
cap ℓ + |S̃| (complete scans): number of moves by type (deletion of an extra / addition / swap / truth-removing),
endpoint == S₀?, certified (final scan finds no strict improvement)?, S₀ scored?; the same with the OLD cap ℓ alone;
is F(S₀) the largest F among all models scored by LS0 (reported-model proxy)? Output: one CSV per experiment + a
summary `.md` with counts per cell. State exact definitions in the script docstring.

## Experiments
Common: σ = 1, Gaussian rows unless stated, columns centred and standardised by the port, y via `make_y_std`.

**V1 — visibility violated (a truth masked inside its block).** Truths j (θ = 1), k (θ = 2), plus a third far truth
t (θ = 1.5, independent of everything). Corr(W_j, W_k) = −0.5, so Cov(W_j, θ_jW_j + θ_kW_k) = 0 (j marginally masked).
(V1a) j has 15 "decoys" d_i = 0.9·W_j + √(1 − 0.81)·e_i and k has 15 decoys of its own built the same way from W_k
(so j and k should land in different blocks, each with its decoys; verify and report the realised blocks); then
Cov(W_j, m | W_U) = 0 for every U ⊆ decoys of j. (V1b) no decoys, and check whether j and k land in the same block.
Remaining columns iid N(0, 1). p ∈ {200, 400}, n ∈ {400, 1600, 6400}, 20 seeds. Questions: is j in the start mode?
does LS0 reach S₀ (by an addition)? Report the population quantity min_U |Cov(W_j, m | W_U)| over U ⊆ realised
block ∖ {j} (≈ 0 means (V) and its block form fail).

**L1 — leakage far beyond log n (count of visible nulls).** One truth j (θ = 1) inside an equicorrelated group of
size g (within-group correlation 0.5), two more truths (θ = −0.8, 1.2) alone; other columns iid. g ∈ {8, 32, 128},
p = 400, n ∈ {400, 1600, 6400}, 20 seeds. Questions: |S̃ ∖ S₀| vs log n; LS0 with the shipped cap reaches S₀? with the
old cap? move types (all deletions?).

**L2 — gain just above the threshold η_A.** [Note added after council round 1: as run, L2 sets the *population*
proxy strength n r² = η log n with σ²-normalisation and a cellwise A; it is an exploratory experiment on leak strength
and does not certify violation or satisfaction of the sample condition (L-gain) of STATEMENT v1.2; see
`SUMMARY_SHARPNESS.md` and `../SHARPNESS.md` §6.] One truth j (θ = 1); EVERY other column l is a weak proxy
W_l = r·W_j + √(1 − r²)·e_l with r chosen so that n r² = η log n (population gain ≈ η σ² log n, U = ∅), for
η ∈ {0, 0.5 η_A, 2 η_A, 0.5, 1.0, 2.0}, η_A = (√(2A+1) − √(2A))², A = log p / log n. p ∈ {200, 400},
n ∈ {400, 1600, 6400}, 20 seeds. Questions: number of proxies in the start mode (sandwich with Q = S₀ fails iff
> 0); LS0 reaches S₀? how many moves? Report η_A per cell.

**N1 — the lattice condition (N): whole-lattice NA versus the path.** Fixed design with EXACT Gram
(`exact_gram_design`; p ≤ n − 1). Build the population correlation: S₀ = 2 truths (θ = (1, −1)), orthogonal to
everything; 𝒫 = m columns, mutually orthogonal and orthogonal to S₀; every other column l:
x_l = cos(a)·w_l + sin(a)·m^{−1/2} Σ_{t∈𝒫} x_t with w_l orthonormal innovations (so Corr(x_l, x_t) = sin(a)/√m,
Corr(x_l, x_{l′}) = sin²(a)); choose tan(a) = 0.64·√m / √(2 log p). Q := S₀ ∪ 𝒫, 𝓛 = [S₀, Q].
m = ⌈C log n⌉ for C ∈ {0.5, 1, 2, 4, 8}; p = 300; n ∈ {400, 1600, 6400}; 20 seeds. (This design has no signal leakage;
the start mode is expected to be S₀. The probe is about the lattice, so LS0 is ALSO started from forced centres.)
Compute per run:
 (i) lattice sup of the add statistic: Z_{T,l} = u_{T,l}ᵀε/σ, u_{T,l} = normalised residual of x_l on X_T. For
     l ∉ Q use the adversarial family T_τ := S₀ ∪ {t ∈ 𝒫 : s·ε̂_t ≤ τ} for both signs s and a grid of τ, where
     ε̂_t := x_tᵀε/‖x_t‖ (removing from T the 𝒫-columns whose noise coordinate is large and aligned), plus 2000 random
     T; report max Z² and compare with c_n′ := log(n+1) + 2 log p − 2 log(|Q|+1); also the direct check: is there
     (T, l) in the searched family with F(T ∪ {l}) > F(T) (true NA violation, by the port's F)?
 (ii) LS0 (complete scans, cap ℓ + |centre|) from the centres Q, and from the 3 adversarial sets T_τ with the largest
     Z²: moves by type, endpoint == S₀?
 Questions: for which C does NA(𝓛) fail on the lattice; does the greedy path from Q (and from adversarial centres)
 still reach S₀ by deletions only?

## Deliverables
Scripts `v1_masked.py`, `l1_groupsize.py`, `l2_eta.py`, `n1_lattice.py`; raw CSVs; `SUMMARY_SHARPNESS.md` with one
table per experiment and, per assumption, the line: "conclusion held in x/y runs outside the assumption".
No interpretation beyond the counts; no claim about asymptotics.

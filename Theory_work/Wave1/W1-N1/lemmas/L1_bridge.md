# Lemma B (code bridge): the coded final island is T12's frozen run I(c)

Status: PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08. Inherits the premise statuses START/KERNEL (N9: PROVED (candidate), code-checked; CHK_INHERITED: VERIFIED WITH AMENDMENT) and T12 (PROVED-LOCKED). v3 (v2 → v3: council C1 non-blocking items; `reviews/C1_disposition.md`).
Notation: STATEMENT.md v2 (locked). CODE = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`;
T12 = `Docs/Theory/proofs/T12_T8_frozen_run_identities/` (STATEMENT.md, PROOF_v6.tex; status PROVED-LOCKED on card TH01);
N9 = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/N9-KERNEL/` (status PROVED (candidate), code-checked).

## Statement

Fix the data and a calibration value c in the success set (so c carries a grid 0 = φ₀ < … < φ_T = 1, integers N_e ≥ 1,
L ≥ 0). Let u = (u₁, u₂, …) be an iid U[0,1) sequence (H-U), the island's stream, and run
`Engine::run_island(r, N_e, grid(c), L, 4, tier, nullptr)` driven by u, without guard stop (potential run).

**Record convention.** Φ(c, u) denotes the **statistical record** of this run: the evidence log Ẑ_r; the population (vector
of particle states) after the initial draws, after each stage-t resampling and after each stage-t round (t = 1..T), after
each of the L burn-in rounds and after each of the 4 measured rounds; and, for each particle and each round, its order and
within-round path. It is a projection/augmentation of the computation (the measured populations are the latent `P` read
at `v3_engine.h:360`, not fields of the returned `IslandResult`). It **excludes** wall-clock fields (`seconds_*`, from
`steady_clock` reads at `v3_engine.h:285, 299, 305, 342, 349, 366`), guard records, move statistics, `distinct` counts, and
the contents and counters of the score cache and ledger, which `cpp_final_run` shares across islands (`v3_core.cpp:430-436`).
For c outside the success set, Φ(c, u) := a fixed dummy record o† (used only to define functions globally; Lemma F).

**Success set.** A_s ⊆ E denotes the set of calibration values c whose grid is 0 = φ₀ < … < φ_T = 1 with integer T ≥ 1, and
with integers N_e ≥ 1, L ≥ 0, R′ = 4k (k ≥ 1); the maps c ↦ (T, grid, N_e, L, R′) are 𝓔-measurable, and on the success event
𝓒 ∈ A_s (by the production grid construction, `v3_calib.h:71-95`, and CAL). Below, "c in the success set" means c ∈ A_s.

**Code version.** N9 was code-checked on `Scripts/SMC_BVS/core/cpp/` @ 39db138 (N9 REPORT:3); this lemma applies it to the
frozen v2.2.1 core. `diff --strip-trailing-cr` of the two trees (checked 2026-11-08): `v3_start.h`, `v3_score.h`,
`v3_blocks.h` identical; `v3_engine.h` differs only by the write-only plain-PIP lines (v2.2.1 `:39-40, 352, 359-361, 370-371`);
`v3_ledger.h` differs only by the read-only registry hook (`:30-31` include, `:69` pointer, `:107` `reg->insert`). N9's
engine line numbers are v2.1 numbers (shifted by +1 or more after v2.2.1 line 40).

Under EX-A, START and KERNEL (STATEMENT §2):

(B-a) **Structure.** Φ(c, u) is a realisation of T12's frozen island I(c) (T12 STATEMENT §2) with N = N_e, M = 4,
L′ = L and the stage-0 flag unset; in particular log Ẑ_r = log Ẑ_T of I(c).

(B-b) **Randomness.** The coded execution satisfies T12's (R1), (R2), (R3).

(B-c) **Endpoints.** For q = 1..4, the population (S_{rq1}, …, S_{rqN_e}) read at `CODE/cpp/v3_engine.h:360` is T12's
population after the (L + q)-th post-terminal operation, each such operation being a round at φ = 1.

(B-d) **Measurability (MEAS).** (c, u) ↦ Φ(c, u) is jointly measurable, with values in a Polish space.

## Proof

**(B-a) Control flow.** The final island is called with `init_states = nullptr` (`CODE/cpp/v3_core.cpp:471`), so each of
the N_e particles is initialised by `draw_start`, i.e. `draw_pi0` (`v3_engine.h:290`, `:109`). `run_island` sets only
`sch.grid` (`:268-273`), so `sch.adaptive = false` and T = grid.size() − 1 (`:281`). The stage loop (`:304-341`) does, for
t = 1, …, T: φ_{t−1} = grid[t−1], φ_t = grid[t] (`:308-309`); log-weights lw_i = (φ_t − φ_{t−1})·d(S_i) of the current
population (`:318`); inc_t = LSE(lw) − log N (`:319-320`), added to logZ (`:323`); ancestors a = resample(lw) (`:325`) and
Pn[i] = P[a[i]] (`:327-328`); one `population_round` at φ_t (`:332`). There is no round before the first reweighting
(flag unset). After the loop: L rounds at φ = 1 (`:344-346`), then 4 rounds at φ = 1 (`:353-357`, Hm = 4 from
`measured_rounds = 4L`, `CODE/v3_run.R:87`). No resampling occurs after stage T. logZ starts at log m(∅) + log Z̄₀
(`:300`; `D.logm0` = log m(∅), `st.logZbar0` = log Z̄₀ by START). Under EX-A, LSE(lw) − log N = log((1/N)Σ_i e^{Δ_t d(S_i)}),
so Ẑ_r = e^{logZ} = m(∅)Z̄₀∏_t (1/N)Σ_i G_t(S_i^{(t−1)}) = T12's Ẑ_T with Z₀ = m(∅)Z̄₀ and G_t = e^{Δ_t d} (T12 STATEMENT §2).
The d and γ_φ the code uses are T12's: `eval` sets lg0 = log ϖ(|S|) + Σ_b log r_b, d = (log m − log m(∅)) − Σ_b log r_b
(`v3_engine.h:98`), `lgphi(φ) = lg0 + φ d` (`:14`), matching T12 STATEMENT §0. On the success set the grid starts at 0
(`CODE/cpp/v3_calib.h:71`), increases strictly (`:90`, validated `:91-92`), and ends exactly at 1 (`:73` loop while u < 1, `:89` snap), so
T ≥ 1 and q_{φ_T} = π; this is T12's grid hypothesis.

**(B-0) The statistical record is a function of (c, u).** Every quantity that feeds a state transition, a weight or log Ẑ
is one of: the frozen c (grid, N_e, L), the fixed data (through `eval`'s log m(S), lg0, d), and uniforms read from u. The
clock reads only set `seconds_*` and the guard argument; the guard is absent in the potential run. Scores: `eval`
(`v3_engine.h:90-102`) takes log m(S) either from the scorer or from the cache; a cache hit requires equal hash **and** equal
model (`v3_score.h:277`, helper `:271-272`), insertion stores the scorer's value for that model (`:283-290`), and an
eviction (`:284`) only causes a later miss, i.e. a fresh scorer call. Under EX-A the scorer is a deterministic function of
S, so the cache returns that value whatever its history (in particular whatever earlier islands left in it). The ledger
only records events and never feeds a proposal or acceptance (`v3_engine.h:99-105`; `v3_ledger.h:105-114`). The RB
accumulation `if (rb_on) rb_acc[j] += oj` (`:129`) writes `rb_acc` only; it neither changes the particle nor reads a
uniform. Engine members that persist across steps and islands (one `Engine` serves all islands, `v3_core.cpp:435`) carry
no information between steps: `tmpQ` is written before it is read in every step (in `step_gibbs` it is read only when
`include != in`, which requires the branch `in || add_ok` that wrote it, `v3_engine.h:119-131`; the swaps and the
independence step write it before reading it); `rb_acc` is reset before the measured rounds (`:351`); `scratch` is workspace
for `st.comp`; `ms`, `ev` are bookkeeping. Hence Φ(c, u) is determined by (c, u) (the data being fixed).

**(B-b) Randomness.** Write F_k = σ(u₁, …, u_k). By (B-0) the record's variables are computed by reading uniforms one at a
time through `vs->u(·)`; whether and how many uniforms an operation reads is decided by the values already read and by the
fixed data and c. Hence the index τ at which any given operation (an initial draw, a resampling, a particle's round, an
elementary step) starts is a stopping time of (F_k). Each operation reads a bounded number of uniforms: `draw_pi0`
≤ 1 + 2J (`v3_start.h:160, 163-170`); a resampling N_e; a particle's round at most
κ_max := (m − 1) + p + 3(B + 1) + (2 + 2J) (order m − 1; Gibbs 1 each; uniform swap ≤ 3; B neighbour swaps ≤ 3 each;
independence ≤ (1 + 2J) + 1). So τ < ∞. By the strong Markov property of an iid sequence, (u_{τ+1}, u_{τ+2}, …) is iid
U[0,1) and independent of F_τ. Every statistical-record variable produced before the operation (states, weights, Ẑ so far,
earlier orders and paths) is F_τ-measurable. Therefore, conditionally on F_τ, the operation acts on its F_τ-measurable
inputs through fresh iid uniforms. Applying this to each operation:
- (R1) Each initial `draw_pi0` call, given F_τ, has law π₀ by START (N9 Claim S: the sampler maps fresh iid uniforms to an
  exact π₀ draw); the N_e draws are therefore iid π₀.
- (R2) `resample` (`v3_engine.h:235-260`) reads N fresh uniforms u_i. With W_k the normalised cumulative weights
  (W_{N−1} := 1), it returns the smallest k with W_k ≥ u_i for u_i > 0: `guide[b]` is the smallest k with W_k ≥ b/N (or N − 1)
  (`:243-247`); with b = ⌊u_i N⌋ we have b/N ≤ u_i, so `guide[b]` ≤ k* := min{k : W_k ≥ u_i}; the forward loop (`:255`) stops
  exactly at k* (all indices in [guide[b], k*) have W < u_i, and W_{k*} ≥ u_i), and the backward loop (`:256`) does not move
  because W_{k*−1} < u_i. The event u_i = 0 has probability 0. Under EX-A, P(a_i = k | F_τ) = W_k − W_{k−1} = w_k/Σ_l w_l,
  and the a_i are conditionally iid given F_τ (disjoint fresh uniforms). This is (R2).
- (R3) `population_round` (`:216-219`) runs `one_round` for particles i = 1, …, N_e in turn. The entering states are fixed
  before the round. Particle i's round starts at a stopping time τ_i; its order is drawn from m − 1 fresh uniforms by
  Fisher–Yates (`:196-201`): the choices ⌊u·(i + 1)⌋ are independent and uniform on {0, …, i}, so each of the m! choice
  vectors has probability 1/m!, and the map to permutations of the canonical label list is a bijection (N9 row 5); hence
  σ_i is uniform and independent of F_{τ_i}. Each subsequent step reads fresh uniforms and, by
  KERNEL (N9 rows 1–4; T12 STATEMENT §1), moves the particle's current state according to K_{σ_i(k)}, given everything
  before it. Particle i's (order, path) depends on the past only through its entering state X̃^i. Let H be the σ-field of
  everything before the round. By the chain rule over i = 1, …, N_e, the conditional law of the N_e pairs given H is the
  product of the laws Q(X̃^i, ·), where Q(x, ·) is "σ uniform; path Markov from x with kernels K_{σ(1)}, …, K_{σ(m)}".
  Here H := F_{τ_1}, the stream σ-field at the round's first uniform; σ(record before the round) ⊆ H, and T12's statements
  for that smaller σ-field follow by the tower property. Explicitly: for bounded f_i of (order, path), conditioning on
  F_{τ_i} (which contains H and particles 1..i−1's pairs)
  gives E[f_i(σ_i, path_i) | F_{τ_i}] = (Q f_i)(X̃^i), and iterated conditioning gives E[∏_i f_i | H] = ∏_i (Q f_i)(X̃^i).
  This is (R3). The labels are p Gibbs labels, one U, B labels N (all calling the same `step_nswap`, whose argument b is used
  only for a label string, `:163-165`), and one I; m = p + B + 2 (`:73`), as in T12 STATEMENT §1.

  Side effects that neither change states nor consume uniforms (B-0): the RB accumulation (writes `rb_acc` only),
  `ev`/`ms` bookkeeping, `distinct`, the score cache, the ledger, the clock. They do not affect (R1)–(R3).

**(B-c) Endpoints.** In the measured loop (`:353-362`), `population_round(P, 1.0)` is called, then the counts are read from
P (`:360`) before the next round. The populations read are therefore those after post-terminal operations L + 1, …, L + 4,
all rounds at φ = 1, with no resampling in between. With the order of (B-a), this is T12's I(c) after its L′ = L burn-in
rounds and its M = 4 measured rounds.

**(B-d) Measurability.** For fixed (T, N_e, L), by (B-0) and (B-b) the statistical record is computed by a finite program
whose branches are comparisons of finitely many Borel functions of (grid values, data constants, u₁, …, u_k), with k bounded
by a constant κ(T, N_e, L) (initial draws, T resamplings and T + L + 4 population rounds, each with the bounds of (B-b));
hence it is a Borel function of (grid, u₁, …, u_κ) on each cell {T(c) = T, N_e(c) = N, L(c) = L}. These cells, with the
complement of the success set (where Φ ≡ o†), form a countable measurable partition, so Φ is jointly measurable. Its values
(finitely many reals and finite sequences of subsets of [p] and of permutations) lie in a countable disjoint union of
Euclidean spaces times finite sets, a Polish space. (The calibration space E need not be Polish.) ∎

## What this lemma uses and does not use

Uses: EX-A, H-U, START (N9 Claims S, Z), KERNEL (N9 rows 1–5, PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH
AMENDMENT), the production code at the cited lines. Does not use: any property of X; reversibility (only the identification
of each step's kernel); the guard (potential run).

## Numerical falsification (numerics/RESULTS.md)

- Elementary kernels: every transition probability is obtained by running the production step functions on scripted
  uniforms (thresholds by bisection to adjacent doubles; the π₀ law from the production sampler tables, each script
  validated on production `draw_pi0`, 0 failures); every row sums to 1 within 2.1e-15 (RESULTS §1); the production `draw_pi0` law sums to 1 and matches
  γ₀/Z̄₀ within RESULTS §1 (relative, floating point). Round kernels (exact order average): RESULTS §2.
- Endpoints: the measured-endpoint hook equals the production `pip_plain` output for every marginal indicator over all
  simulated islands (RESULTS §5, column "hook diff").
- End-to-end: the exact replica built from those kernels satisfies N1 to floating-point precision (RESULTS §3) and the
  production engine agrees within Monte Carlo error (RESULTS §5).

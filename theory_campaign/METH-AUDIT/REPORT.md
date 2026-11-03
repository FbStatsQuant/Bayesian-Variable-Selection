# METH-AUDIT — REPORT: is v3 parallel-friendly enough to ship?

Run METH-AUDIT (Opus 5.5), branch `theory/METH-AUDIT`, 2026-11-03. Everything here is a **candidate**: not reviewed, not
adopted. Status words follow `theory_campaign/PROTOCOL.md`. Proofs are in `PROOFS.md`. Scripts are in `scripts/`
(fixed seeds; all computation went through `owls_run -j 2`), and outputs are in `results/`.

## 1. Headline

1. **Ship v3 unchanged as the statistical method; add a parallel execution layer. Call the result v3.1.** No theorem the
   paper relies on breaks under parallel execution, and nothing in the spec blocks it. The obstacles are all in the
   *execution* of the code: islands, diagnostic islands, particles and local-search scans all run serially on one CPU.
   None of the candidate changes needed for parallel execution is WORKHORSE.
2. **Concurrent islands give bitwise-identical estimates (Proposition W: PROVED by code reading, executed check
   PASSED).** Run the 4 final islands as independent workers, each with its own score cache and ledger, then merge the
   ledgers. This reproduces the serial production run's log Ẑ_r, PIP_r, HPM, stores and flags bit for bit, on the smoke
   problem and on 3/3 study designs (§6). The same argument covers the calibration's diagnostic islands (Proposition
   W-cal: PROVED by code reading, not executed). So "run the islands concurrently" is ADDITIVE in the strongest sense: the
   2,394 completed study fits are unchanged. The 6 `resource_limit` stops (all S5, wall-time guard, one CPU, islands
   serial) are the only fits it can change.
3. **More islands: stack them at the same N_e; do not split N_e (Proposition P: PROVED; Corollary V: PROOF SKETCH).**
   Islands 1–4 on streams 10–13 plus extra islands on new streams is ADDITIVE: islands 1–4 are bitwise unchanged, and
   the scored set and the pre-local-search HPM can only improve. Splitting a fixed total into R ≫ 4 islands of smaller N
   is neutral for Ẑ to first order, but it makes the **equal-weight (primary) PIP worse**, because that PIP's bias is the
   single-island bias, fixed by N and not by R. The **Ẑ-weighted (secondary) PIP is consistent as R → ∞ at fixed N**, with a
   non-asymptotic, regime-free bound (Proposition P(iii) with F-MASKPIP M1). That is the precise form of "correlation
   costs islands, never correctness". **Gap found:** the spec's secondary PIP (§6.11) is *not computed* by the core
   (`v3_run.R`). It can be computed post hoc from the saved `log_Z_r` and `pip_r`.
4. **Depth.** With islands concurrent (width R), the critical path is ∝ N_e·(T+L+4)·(p+B+2) score evaluations. With
   particle-parallel islands (width R·N), it is ∝ (I+2)·(T+L+4)·(p+B+2), *independent of N, H and R* (Proposition D).
   Particle-level parallelism needs per-particle random streams. That is a LAW-PRESERVING change: same kernels, same
   law, different seed-to-uniform map, so not bitwise. It is needed only when N₀ = max(2500, n, p) grows with p. The
   factor p + B + 2 per round (LIT-PAR's self-critique) is real in score units, but it costs about 2–3 ms of wall time
   per round at p = 500. Removing it would be a WORKHORSE kernel change, and it is not recommended.

## 2. Work/depth map

See §2.1 (per component) and §2.2 (totals at study size, measured). Symbols: n, p; B the block size; J ≥ ⌈p/B⌉ blocks;
K = min(p, ⌊n/2⌋); m = p + B + 2 steps per round; N = N_e final particles per island; H = H_e calibration particles;
R islands; T the final grid's stage count; T_pil the pilot's stage count; I_e ≤ ℓ the rebuild iterations; L burn-in rounds;
4 measured rounds; ℓ = ⌈log₂(n+p+1)⌉; s(k) the cost of one score at size k (O(k³) from the Gram); s̄ its mean along the
path; k̄ the typical model size.

### 2.1 Per component

"Spec" says what the spec allows to run in parallel. "Code" says what the production code actually parallelises:
nothing. Every loop is serial, and the study ran one CPU per fit with the islands one after another.

| # | Component | Work | Sequential depth if parallelised (PEL / particle-parallel) | Sync points | Memory per worker; needs all of X? | Spec | Code |
|---|---|---|---|---|---|---|---|
| 1 | Checks, standardisation | O(np) | O(n) (columns independent) | 1 | 8np | silent | serial R |
| 2 | Gram G = XᵀX, z = Xᵀy | O(np²) | O(n) with p² workers (BLAS) | 1 | 8p² + 8np; yes | silent | serial (single-thread BLAS by policy) |
| 3 | Correlations, complete linkage (R13 ties), cut, packing | O(p²) memory; O(p²)–O(p³) time (explicit algorithm with row minima, `v3_blocks.h`) | p − 1 merges, inherently sequential; each merge O(p) parallel | 1 | 16p² transient (r and distance) | silent | serial |
| 4 | Block tables r_b(U) | Σ_b 2^{\|C_b\|} ≤ J·2^B scores at size ≤ B: O(J 2^B B³) | s(B) (blocks × sub-models independent) | 1 (before Z̄₀) | **only X_{C_b} (or G_{C_b,C_b}) and y**: the one truly local stage, as in Song–Liang | implicit | serial |
| 5 | Z̄₀ by convolution; π₀ sampler | O(J K B) | J sequential (log J as a tree) | 1 | O(Σ_b 2^{\|C_b\|}) doubles (the tables), shared read-only | silent | serial |
| 6 | Neighbour graph | O(p² log p) | O(p log p) (rows independent) | 1 | O(pB) | silent | serial |
| 7 | Pilot (adaptive ESS schedule) | H (T_pil + L + 4) m s̄ + 60·H·T_pil bisection | PEL: same as work (one island). Particle-parallel: (T_pil + L + 4) m s̄ + T_pil·O(log H) | T_pil (global ESS bisection per stage) | G, tables, cache 500p entries; yes | single island | serial |
| 8 | Candidate set V, grid construction | V: O(p log p) from the stores; grid ≤ 60 \|V\| T_e log-sum-exps | sequential bisection; each F_V a \|V\|-term sum (log depth) | 1 per rebuild | \|V\| ≤ 40p + 1 models | sequential | serial |
| 9 | Diagnostic islands (calibration) | Σ_{i ≤ I_e} 4 H (T^(i) + L + 4) m s̄ | PEL: H (T^(i) + L + 4) m s̄ per iteration, 4 islands concurrent, **bitwise** (Prop. W-cal). Particle-parallel: (T^(i) + L + 4) m s̄ | per iteration: merge ledgers → local search → V → grid | as 7; yes | "4 islands" | serial |
| 10 | Rebuild loop | ≤ ℓ iterations of 9 + 11 + 8 | **I_e sequential iterations** (each grid depends on the previous diagnostics) | I_e | — | sequential by design | serial |
| 11 | Local searches (pilot, each rebuild, final; LS0 if adopted) | ≤ (ℓ + 1)(p + k̄(p − k̄)) scores each | ℓ + 1 sequential scans; each scan fully parallel (O(1) score + max-reduction) | ℓ + 1 per search | G; yes | silent | serial |
| 12 | Escalation (tier 1) | 7–11 again at 4H and 4T_e | after tier 0, sequential | 1 | as 7 | sequential | serial |
| 13 | Final islands | R N (T + L + 4) m s̄ + R N initial π₀ draws | PEL: N (T + L + 4) m s̄ (R concurrent, **bitwise**, Prop. W). Particle-parallel: (T + L + 4) m s̄ + T·O(log N) | T per island; none across islands until pooling | G + tables + cache + population (N (p/8 + 4k̄ + 40) B, ×2 while resampling); yes | "islands may run sequentially" (§8.6) | serial |
| 14 | Bridge stage: reweight + multinomial resampling | O(N) per stage | O(log N) (log-sum-exp + prefix sum) | 1 per stage | O(N) | — | serial (one stream per island) |
| 15 | Move round (Gibbs ×p, uniform swap, B neighbour swaps, independence) | m scores + one π₀ draw O(J + K) | **m sequential steps** inside a particle (inherent to the kernel) | none | particle state | — | serial |
| 16 | Burn-in L + 4 measured rounds | (L + 4) N m s̄ per island | (L + 4) m s̄ | none | — | — | serial |
| 17 | Pooling (Ẑ, PIPs, MPM), ledger merge | O(R p) + R stores of ≤ 40p+1 + 40p models | O(log R) | 1 | O(R p) | — | serial |
| 18 | Flags (E1, E2, E3, lowESS) | O(R T) | O(1) | 1 | — | — | serial |

**Memory per worker** at n = 200, p = 500 (B = 14): X 0.8 MB, G 2 MB, tables ≈ J·2^B·8 B ≈ 5 MB, cache ≈ 250,000 entries
× (29 + 4k̄) B ≈ 20 MB, population < 1 MB. That is about 30 MB, so dozens of workers fit on any node. Each worker needs
the full G (or X), because every Gibbs round touches every coordinate. This is the price of targeting the exact
posterior, against Song–Liang, where a worker holds n × p/K. Mitigation: G is read-only and shared by threads or by
forked processes (copy-on-write), so a node holds one copy. Across nodes, 8p² bytes is 0.8 GB at p = 10⁴ and 80 GB at
p = 10⁵. Beyond about p ≈ 3·10⁴ a Gram-free scorer (G_S from X at O(n k²) per score; the `chol_refactor` route already
does this) would be needed. That change is LAW-PRESERVING up to floating point, and it is not needed at study size.

### 2.2 Totals

Score-evaluation units:

- **Work**: W ≈ J 2^B s(B) + Σ_e [H_e (T_pil + L + 4) + 4 H_e Σ_i (T^(i) + L + 4)] m s̄ + R N_e (T + L + 4) m s̄
  + n_LS (ℓ+1)(p + k̄(p−k̄)) s̄ + O(np²) + O(p²)–O(p³).
- **Depth, v3 as coded** (serial): D = W.
- **Depth, v3.1 PEL** (islands, diagnostic islands and scans concurrent; particles serial within an island):
  D_PEL ≈ D_setup + Σ_e [H_e (T_pil + L + 4) + H_e Σ_i (T^(i) + L + 4)] m s̄ + N_e (T + L + 4) m s̄ + n_LS (ℓ+1) s̄.
- **Depth, particle-parallel** (Proposition D): D_PP ≈ D_setup + [(T_pil + L + 4) + Σ_i (T^(i) + L + 4) + (T + L + 4)] m s̄
  + O(ΣT·log N). This is free of N, H and R. Worst case on success: O(p log³(n+p)).

Measured at study size: §6 Table 6.2.

**Comparison with Song–Liang §6.** Their wall-time bound, with K_n = √p processors, is O(p^{(1+α)/2}) + O(np). The first
term comes from T = O((p/K)^α) SAMC iterations per subset, each costing O(p/K). That α is a *choice* (α = 1 in the paper),
not a mixing guarantee: their sampler theory is "by citing SAMC convergence" (METHODOLOGY §11). Their total work is
O(p^{1+α/2} + n p^{3/2}) on √p workers, and the output is a posterior restricted to the merged set. Ours, on width R·N:
- depth O(p·(ℓ+2)(T+L+4)) score evaluations, with T bounded by proved grid results: O(1) favourable, log₂n + O(1) under
  proxy masking, O(log log n) on LH (O-STAGES, Theorem G), and ≤ T_e always;
- work O(N p (ℓ+2) T_e);
- output: the exact posterior (Ẑ unbiased, Ẑ-weighted PIPs consistent in R).

So **our depth is of the same order in p as theirs at α = 1, up to logarithmic factors**. We need far more width
(R·N ≈ 10⁴ particles, against √p ≈ 22 subsets) and far more total work. What we gain is correctness under correlation.
That is an honest trade, and the paper should state it in exactly these units. Do not claim "faster than SaM".

## 3. Theorem robustness under parallel execution

Columns:
- (i) the final run uses R ≫ 4 islands. Two readings: (i-a) *stacked*, with N_e per island unchanged; (i-b) *split*, with
  smaller N and R·N fixed.
- (ii) islands run concurrently with independent streams.
- (iii) calibration is shared or shortened.
- (iv) Ẑ-weighted versus equal pooling.

✓ = holds verbatim. ✓R = holds with "4" read as R. ⚠ = a hypothesis changes (stated).

| Result (registry ID) | (i-a) stacked | (i-b) split | (ii) concurrent | (iii) calibration shared/shortened | (iv) pooling |
|---|---|---|---|---|---|
| **Prop 2(a,b,d,e) / T12(iii)**: islandwise and pooled unbiasedness of Ẑ; 0.05·Ẑ 95% lower bound (W2-BOOK; XF GAP on conventions only) | ✓R | ✓R (any N ≥ 1) | ✓ (Prop. W: bitwise) | ✓ for *any* 𝓒 fixed before the final streams. Sharing one 𝓒 across several final runs is fine. ⚠ R must be fixed in advance: an adaptive "add islands until the SE is small" rule breaks conditional unbiasedness (same mechanism as CEX-guard; Prop. P(v)) | Ẑ unaffected |
| **Prop 2(c)**: pooled Ẑ × equal PIP bias −¾Cov | ✓ with ¾ → 1 − 1/R (Prop. P(iv)) | same | ✓ | ✓ | n/a for Ẑ-weighted (that pairing is unbiased by the island identity) |
| **Prop 2(f) / VAL-FP** (η ≤ 2.6e-13, ε ≤ 2.2e-6 per final run; API-AUDIT) | ⚠ ε scales with the number of compared thresholds: ≈ (R/4)·ε | ✓ (same total) | ✓ (bitwise) | — | — |
| **T31(i)**: Ẑ-weighted pooling consistent as R → ∞ at fixed N (standard: Whiteley–Lee–Heine) | ✓, and it *is* this regime | ✓ | ✓ | ✓ | **only for Ẑ-weighted**; equal pooling converges to the single-island mean (Prop. P(i)) |
| **T26 / Thm 6 (A)**: evidence and PIP consistency, favourable regime, premise (P1) (T_n+1)Δ_n → 0 | ✓ (per-island bound, no N in the premises; registry-level reading) | ✓ (any N_r ≥ 1) | ✓ | ⚠ T_n is the calibration's grid count. A shortened calibration (fewer rebuilds, smaller H) changes the law of T_n and P(S₀ ∈ V), but (P1) is still a premise on T_n, so the theorem stands. API-T26BUD Thm 1 (T_n = 1 eventually) uses only the iid first pilot stage, so it is robust to fewer rebuilds | Thm 6's PIP part is per island, so it holds for both poolings |
| **T38 (0), (0_H)**: P(𝒪 ∩ Ŝ⁺ ≠ S₀) ≤ 2E₀δ₁ + D_n | ✓ (D_n can only fall: nested scored set; Cor. W-R) | ✓ form; D_n changes (see b2) | ✓ (identical 𝒮; Prop. W) | ⚠ (0_H)'s D_n^{sl} involves 𝒮_cal: shortening calibration can raise it | n/a (HPM) |
| **T38 (a)** favourable (D_n → 0 under (F)) | ✓ | ✓ (iid-draw discovery uses Q_f = R N (1 + T + L + 4), unchanged at fixed R·N) | ✓ | ✓ | n/a |
| **T38 (b1)/(b1-LH)**, LS0 route | ✓ (LS0 is a deterministic scan) | ✓ | ✓ | ✓ | n/a |
| **T38 (b1′)**, D2 route, v3 as run (pilot first stage scores S₀ or ESS ≥ 0.9H₀) | ✓ | ✓ | ✓ | ⚠ **depends on the pilot's H₀**. A smaller pilot weakens NB′. Do not shrink H | n/a |
| **T38 (b2)/(b2-LH)**: DELIV(𝔛_n) "no final-run particle of any island" + REP | ✓ (union over more islands) | ⚠ DELIV is a union over islands, but delivery *inside* an island depends on its population size through resampling. At fixed R·N it is not monotone in R; it needs re-checking (OPEN) | ✓ | ✓ | n/a |
| **T38 (c)** cost (T32(i); XF GAP on the displayed rate) | ✓R (work ∝ R N) | ✓ | depth, not work, changes; add Prop. D's depth statement | ✓ | — |
| **O-STAGES / Theorem G** (stage count of the grid; API-T26BUD Thm G) | ✓ (a calibration object; final R and N do not enter) | ✓ | ✓ (Prop. W-cal: identical grid) | ⚠ needs S₀ ∈ V and a successful construction. Shortened rebuilds lower P(S₀ ∈ V); a shared calibration is fine | — |
| **MASKZPIP E1, E2, P1, P3, C1** (per island; any kernel, grid, N) | ✓. E2's union term Nπ₀(A) per island sums to R N π₀(A) | ✓ (same total) | ✓ | ✓ (statements are conditional on 𝓒) | P1 (RB-PIP bias ≤ TV of the delivered population) is per island. With masking, only Ẑ-weighting removes non-crossing islands' bias as R grows (Prop. P(iii)) |
| **F-MASKPIP M1/M2** (E[(Ẑ_r/Z)·err_r] ≤ δ₁ + ρ̄ + u_π) | ✓ | ✓ | ✓ | ✓ | **the input that makes the Ẑ-weighted PIP regime-free in R** (Prop. P(iii)) |
| **O-PW2 Thm A/B** (variance of W_T) | ✓: Var(pooled) = Var(W)/R | ✓ to leading order, with remainder growing as N_r ↓ (Cor. V, PROOF SKETCH) | ✓ | ✓ (conditional on 𝓒) | — |
| **Thm 4 / N200**: P(U ∪ {Ŝ ≠ S₀}) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮) | ✓; discovery term can only fall | ✓ form | ✓, and **P(U) falls**: the 6 stops were wall-time stops on one CPU | ⚠ shortening calibration changes P(U) and 𝒮 | n/a |
| **Lemma RO / GUARD** (stop-only coupling; no RNG in the guard) | ✓ | ✓ | ✓ *provided* the guard checks the run's wall clock, and a stop in any worker stops the run before any output (keeps "a stopped fit is no output") | ✓ | — |
| **IND-T** (one stream per island, read sequentially; API-AUDIT fact 5) | ✓ (new islands get new streams) | ✓ | ✓ (exactly this) | — | — |

**Which hypotheses change, in one list.**
1. Every "4 islands" becomes "R islands, R fixed before final randomness".
2. Prop 2(c)'s ¾ becomes 1 − 1/R.
3. VAL-FP's ε scales with total work.
4. Under a split, DELIV inside an island depends on N_r (OPEN).
5. A shortened calibration touches (b1′) (through H₀), Theorem G and (0_H) (through P(S₀ ∈ V) and 𝒮_cal), and nothing
   else.
6. Particle-level parallelism (not needed for (i)–(iv)) would restate IND-T as "uniforms of distinct (island, stage,
   particle) triples are independent". The REP product form uses exactly this, so the theorems are unaffected.

## 4. Candidate changes

Classes:
- **ADDITIVE**: outputs on completed fits are unchanged or nested; re-run once at the end.
- **POST HOC**: computable from saved fits; no re-run.
- **LAW-PRESERVING**: same law, different seed-to-uniform map. Study fits stay valid draws of the same procedure, but are
  not bitwise reproducible.
- **WORKHORSE**: as defined in the task.

| # | Change | Real issue it fixes | Class | Expected effect on existing results | Cheapest test |
|---|---|---|---|---|---|
| C0 | **No change**: ship v3 exactly as coded (serial) | — | — | none | — |
| C1 | **Concurrent final islands** (Prop. W): workers with own cache and ledger; merge stores and HPM; final local search after the merge | Parallel bottleneck: final-run wall time = 4 × island time on one CPU. It also lowers P(U) (Thm 4/N200, T38(0)), since the 6 S5 stops were wall-time stops | ADDITIVE (bitwise) | none on the 2,394 completed fits; can only rescue the 6 stopped fits | **done**: bitwise on smoke and 3/3 designs (§6) |
| C2 | **Concurrent diagnostic islands** (Prop. W-cal): 4 persistent workers per tier; merge before the local search and V | Calibration depth: (1 + I_e) island-depths, serial | ADDITIVE (bitwise) | none | bitwise replay of `v3_calibrate` on 3 designs (not run; same harness, about 1 h on Owls) |
| C3 | **Parallel local-search scans** | each scan has (p + k̄(p−k̄)) independent scores | ADDITIVE (bitwise if the max-reduction keeps the lexicographic tie rule) | none | bitwise path comparison |
| C4 | **Stacked islands**: R′ = 4k islands at N_e; streams 10–13 kept, then 14, …; flags on islands 1–4; extra local search from the R = 4 centre (Cor. W-R) | Objective 1 (accuracy) at fixed depth: variance of Ẑ and of both PIPs ∝ 1/R′ | ADDITIVE (nested) | islands 1–4 bitwise unchanged; HPM ⪰; Ẑ and PIPs refine | re-run with R′ = 8 or 16 on a few designs; check nesting |
| C5 | **Compute and report the Ẑ-weighted (secondary) PIP**, which is already in the spec (§6.11) but missing from `v3_run.R` | Spec/code gap; the only PIP with an R-consistency theorem (T31(i), Prop. P) | POST HOC | none on HPM, Ẑ or the primary PIP; adds a column. Computable for all 2,400 fits from `log_Z_r`, `pip_r` | one line in `v3_assemble_final`; recompute on saved fits |
| C6 | **Per-particle random streams** (counter-based, e.g. stream = f(seed, island, stage, particle)), enabling particle-parallel islands | Depth ∝ N_e under C1–C4. N₀ = max(2500, n, p) grows with p, so depth grows like p²·T without this. A genuine obstacle **only beyond study size** | LAW-PRESERVING | none in law; individual fits not bitwise. Keep the serial map as the default reproducibility mode | law check: R = 4, the two stream maps, 20 seeds, compare log Ẑ and PIP distributions |
| C7 | **Gram-free scorer** for p ≳ 3·10⁴ | per-worker memory 8p² | LAW-PRESERVING up to floating point (VAL-FP-type η) | none at study size | VAL-FP replay |
| C8 | **Split total particles into R ≫ 4 smaller islands** | none: neutral for Ẑ to first order (Cor. V) | WORKHORSE in effect (changes N_e, a declared budget) | equal-weight PIP bias grows ∝ R/N_tot; masked-regime delivery per island may fall | measured in §6 (R = 32 × 312) |
| C9 | **Shortened or shared calibration** (fewer rebuilds, smaller H) | none found: calibration depth is (1 + I_e) island-depths, made small by C2/C6 | WORKHORSE (schedule rule) | touches T38(b1′), Theorem G, (0_H) | not recommended |
| C10 | **Parallel-in-particle kernel** (informed or tempered-Gibbs moves scoring all p flips at once) | the depth factor m = p + B + 2 per round (LIT-PAR §3.3) | WORKHORSE (move kernel) | breaks the Gibbs-path theorems (T38(b2), BG3, V5's self-adjointness proof would need redoing) | not recommended; the factor costs about 2–3 ms per round (§6) |
| C11 | **Faster exact complete linkage** (nearest-neighbour chain, O(p²)) | clustering time O(p²)–O(p³), sequential, at p ≳ 10⁴ | ADDITIVE if the blocks are reproduced exactly (R13 tie rule must be kept) | none | block identity on the 2,400 designs |

**Arguing C0 (no change).** As a *statistical method*, v3 needs no change: no registry result breaks under (i-a), (ii),
(iii-shared) or (iv), and the spec already allows parallel islands (§8.6). As *code*, C0 does not support the paper's
parallel claim. The production core is serial throughout, so any wall-clock or scaling statement would be about code
that does not exist. C0 is therefore right for the method and wrong for the paper.

## 5. RECOMMENDATION

**Ship v3.1 = v3 (unchanged statistical method: start, bridge, kernel, schedule rule, budgets N_e = max(2500, n, p), H_e,
T_e, HPM decision, flags) + a parallel execution layer.** The layer has five parts:
- **(a)** final islands as concurrent workers, each with its own cache and ledger, merged by Lemma S before the final
  local search (C1);
- **(b)** the calibration's 4 diagnostic islands as persistent concurrent workers, merged before each local search and V
  build (C2);
- **(c)** local-search scans evaluated in parallel with the lexicographic max-reduction (C3);
- **(d)** optional island stacking R′ = 4k at N_e. Islands 1–4 stay on streams 10–13 and define v3's flags. R′ is fixed
  before final randomness, and an extra local search runs from the islands-1–4 centre (C4);
- **(e)** the Ẑ-weighted PIP computed and reported next to the equal-weight PIP (C5). The R-scaling guarantee is
  stated for it.

Parts (a)–(c) are bitwise-neutral on completed fits, (d) is nested, and (e) is post hoc. So the 2,400-fit study stands
as v3.1's study at R′ = 4, with no re-run. (A final run with stacked islands, re-run once at the end, can only improve
it.) Per-particle streams (C6) and the Gram-free scorer (C7) are a declared v3.2 path for p well beyond the study. They
preserve the law and change no theorem. Do not split N_e across more islands (C8), do not shorten calibration (C9), and
do not change the kernel for depth (C10).

## 6. Evidence

[filled in after the runs; see results/]

## 7. What fails and why

- **"Depth = T stages" without the round factor fails.** The kernel is a p-step random-order Gibbs round, so per-stage
  depth is m = p + B + 2 sequential score evaluations at best (Proposition D; LIT-PAR §3.3). The only fix is a kernel
  change (C10), which breaks the Gibbs-path theorems. Rejected. The honest statement is
  depth = (I + 2)(T + L + 4)·m score evaluations with T bounded by O-STAGES/Theorem G.
- **"More islands always helps" fails for the equal-weight PIP under a split.** Proposition P(i): its limit is the
  single-island mean, so its bias is set by N per island. Shrinking N to add islands (C8) makes it worse. The measured
  difference at R = 32 × 312 (§6) is small on these designs, but the theorem gives no protection.
- **Island-level parallelism alone does not scale p.** Depth under C1–C4 is ∝ N_e, and N₀ = max(2500, n, p). So for
  p > 2500 the depth grows like p²·T. Particle-level parallelism (C6) is needed there, and it cannot be bitwise-identical
  to the serial stream map. This is why C6 is LAW-PRESERVING, not ADDITIVE.
- **Shortening calibration is not a parallel fix.** Calibration depth is (1 + I_e) island-depths. C2 cuts it 4-fold
  bitwise, and C6 makes it N-free. Cutting rebuilds or H would touch T38(b1′) (H₀ in NB′), Theorem G (S₀ ∈ V) and (0_H)
  (𝒮_cal), so C9 is rejected.
- **A per-fit adaptive R is not allowed.** "Stack islands until the SE is small" breaks conditional unbiasedness
  (Prop. P(v)), so R′ must be declared in advance.
- **Not done:** the bitwise replay of the calibration (W-cal is code reading only), the law check for C6, and the full
  10-design test (NOTS script provided, not run).

## 8. Needs escalation

1. **Proposition W / W-cal** need an independent code check of the claim that "the ledger is write-only during an
   island" and of the claim that the scorer has no state between calls. My evidence is code reading plus 4/4 bitwise
   executions (smoke + 3 designs), and the calibration version is not executed. API-AUDIT-style referee: cheap.
2. **Corollary V** (split neutrality to first order) is a PROOF SKETCH. It needs O-PW2 Theorem B's V_s and H_{s,T} written
   out, and a check that the full-space χ²_t stays small at N_r ≈ 300.
3. **DELIV under a split** (T38(b2) with smaller islands): OPEN. It is relevant only if C8 is ever adopted.
4. **Prop. P(iii)'s practical scope:** in the masked regime E[W²] can be exponentially large. A referee should judge
   whether the paper may phrase the Ẑ-weighted PIP result as "correctness at a cost in islands" without a bound on E[W²].

## 9. Outside scope

- **Spec/code gap:** the Ẑ-weighted (secondary) PIP of METHODOLOGY §6.11 is not computed by the core (`v3_run.R`
  assembles only `pip_primary` and `pip_r`). The study's reported "secondary PIP", if any, must come from a post hoc
  script. Check before citing it.
- **LS0 is not in the production core** (API-AUDIT fact 3). If v3.1 = v3 + LS0 + PEL, LS0 is one more deterministic
  local search, parallel by scans (C3), and it is theorem-neutral for every row of §3.
- **The 6 `resource_limit` stops** were wall-time stops (6,300 s at p = 500, 24,000 s at p = 1000, one CPU, islands
  serial; BRIEFING_20261028 §Compute). Under C1 + C2 the same allocation gives about 4× more headroom for the final run
  and the diagnostics. Re-running those 6 fits with PEL is the cheapest way to remove the P(U) caveat from the paper (6
  fits × ≤ 2 h on 4 cores, NOTS).
- The measured per-particle-round cost (§6) gives a direct estimate of what particle-parallel islands (C6) would take:
  about (I + 2)(T + L + 4) rounds × a few ms, i.e. under a second of island depth at p = 500.

## 10. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change needed? |
|---|---|---|---|---|---|
| Parallel execution of v3 (final islands) | Prop. W: worker islands with their own caches and ledgers give bitwise the serial outputs after merging by Lemma S | high (proved by reading, 4/4 executed) | done (PROVED, candidate) | scorer statelessness; ledger write-only in islands | no (ADDITIVE layer) |
| Parallel calibration diagnostics | Prop. W-cal | high | done by reading; execution check cheap | stream persistence per diagnostic worker | no |
| Pooling as R grows | Prop. P: Ẑ-weighted PIP consistent in R with a regime-free bound (via M1); equal-weight PIP keeps single-island bias | high | done (PROVED, elementary) | Maurer lower tail; M1 | no; report the secondary PIP (POST HOC) |
| Split neutrality for Ẑ | Cor. V: same total particles ⇒ same leading variance | medium | medium | O-PW2 Thm B remainder at small N_r; full-space χ² | no (and C8 not recommended) |
| Depth | Prop. D: depth (I+2)(T+L+4)(p+B+2) score evaluations, free of N, H, R with particle-parallel islands | high (counting) | done | needs per-particle streams (C6) to realise | LAW-PRESERVING stream map only |
| Theorem robustness (§3) | all listed results hold under (i-a), (ii), (iv) and a shared calibration; the listed hypotheses change under (i-b) and a shortened calibration | medium-high (registry-level reading of T26 Theorem A and T38 parts; not re-proved) | yes (bookkeeping) | DELIV under a split | no |

# METH-AUDIT — PROOFS.md: statements and proofs for the parallel execution layer

Run METH-AUDIT, 2026-11-03. Every item is a **candidate**: not reviewed, not adopted. Status words follow
`theory_campaign/PROTOCOL.md`. Code references are to `Scripts/SMC_BVS/core/` at the branch base. The code version was
last changed at 39db138, the same files API-AUDIT audited.

Notation. 𝓒 is the frozen calibration (grid, tier e, N_e, L, inherited models). Island r of the final run reads stream
σ_r: σ_r = 9 + r in production. W_r := Ẑ_r/Z. PIP̂_rj is island r's Rao–Blackwellised PIP. ≻ is the HPM total order:
larger F, then smaller |S|, then lexicographic (`hpm_better`, `TopCmp`). A *worker* is any execution context (thread,
forked process, Slurm task) that holds its own `Engine`, `ScoreCache` and `Ledger` and reads only its own stream.

---

## Lemma S (order independence of the bounded stores). PROVED

**Statement.** Let `TopStore` have capacity c and strict total order ≺ on pairs (v, S), where v = v(S) is a deterministic
function of S. Whatever the order in which a finite multiset M of pairs is offered, the final content is the set of the
c ≺-best distinct pairs of M. Hence for any partition M = M₁ ∪ … ∪ M_R, top_c(M) = top_c(top_c(M₁) ∪ … ∪ top_c(M_R)).

**Proof.** Code: `v3_ledger.h:41–56`. Invariant: after each offer, the store equals top_c(M_seen), the set of the c best
distinct pairs offered so far. This holds for the empty store. Offer e:
- e is already stored. Then `s.count(e)` rejects it. Since v is a function of S, duplicates are identical pairs.
- The store is full and e is not ≺-better than its worst element. Then c distinct seen pairs beat e, so e ∉ top_c(M_seen ∪ {e}).
  This covers a pair that was evicted earlier and is offered again: the worst stored element only improves over time.
- Otherwise e is inserted, and if the size exceeds c the worst element is erased. The result is top_c(M_seen ∪ {e}).

The partition identity follows because top_c(M) ⊆ ∪_r top_c(M_r): an element among the c best of M is among the c best of
any M_r that contains it. ∎

The running HPM (`offer_hpm`) is the case c = 1 under ≻, so it is order independent too. Its *provenance* label is not;
see Proposition W(c).

## Proposition W (worker equivalence of the final run). PROVED (code reading; executed check in REPORT §6)

**Setting.** Fixed data, seed s and 𝓒. The *serial run* is `cpp_final_run`: islands r = 1..R in order, one shared
`ScoreCache` (capacity 500p, cleared when full) and one shared `Ledger` (tables ingested, then inherited models), then
the final local search from the ledger's HPM. The *worker run* executes island r in worker r, in any order and with any
overlap in time. Worker r uses stream σ_r, its own cache of the same capacity, and its own ledger with the tables ingested.
Then it merges:
- HPM := the ≻-maximum of the worker HPMs and the inherited HPM;
- each store := top_c of the union of the worker stores and the inherited models;
- the final local search runs from the merged HPM with `emit_centre = false`.

**Claims.**
(a) For every r, Ẑ_r, PIP̂_r·, the per-stage ESS, phi, log-increments, move counts and the terminal table are **bitwise**
equal in the two runs.
(b) The merged HPM and the merged stores (top 40p+1 by F, top 20p by log γ₀, top 20p by log γ₁) equal the serial
ledger's just before the final local search. So the local-search path, the final HPM, the near-tie list, the MPM, the
pooled Ẑ, the primary and Ẑ-weighted PIPs, and the final flags E1, E2, E3 and low_empirical_ESS are equal too.
(c) Not equal: the cache counters, the fresh/logical score counters, and the time stamps. The HPM provenance is equal if
the merge takes it from the inherited record when the HPM is inherited, and otherwise from the lowest-index worker whose
HPM equals the merged HPM.

**Proof.**
(a) Island r is `Engine::run_island_s` (`v3_engine.h:274–368`). Its reads are:
- the setup (read-only `Data`, `Start`, the neighbour graph);
- the grid and N, L, Hm, tier;
- uniforms from `E.vs`. In the serial run this is a fresh `RngSource` seeded `seed_stream(s, 9+r)` per island
  (`v3_core.cpp:434–437`). In the worker run it is the same seeding.
- score values from `eval` (`v3_engine.h:89–100`).

`eval` returns the cached log m(S) on a hit and a fresh `Scorer::score(S)` on a miss. The scorer is a deterministic
function of the sorted model: it fills G_S from the stored Gram, with no state carried between calls (`v3_score.h:139–247`).
The cache stores exactly the returned double (`v3_score.h:249–255`, comment and code). So the score sequence seen by
island r does not depend on the cache's contents, and hence not on other islands. The ledger is write-only during an
island. Its only reads are `led->hpmS` at local-search start, the stores at V construction, export and `hpm_now`
(`v3_core.cpp:586, 610, 630, 654, 657, 675–676, 699–701`). All of these are outside `run_island_s`. The runtime guard
reads no RNG and changes no setting (API-AUDIT fact 2), and the worker run passes `guard = nullptr`. So the whole
island computation, including every uniform consumed, is the same function of the same inputs. Its floating-point
outputs are bitwise equal, provided compiler flags and environment are equal (pinned by `Makevars.v3`).

(b) A model is offered to a ledger's stores iff it has a fresh evaluation in that ledger's run (`v3_ledger.h:110`). In
both runs every model a run scores has at least one fresh evaluation: its first evaluation is a cache miss, or it is
re-scored fresh after a clear. Every cache insertion happens inside an emitting `eval`, except the local-search centre,
which is the current HPM and so already offered (API-AUDIT §1). So the serial ledger before the final local search has
been offered exactly the union of the tables, the inherited models and ∪_r(models scored by island r). Worker r's ledger
has been offered the tables and the models scored by island r, and the merge adds the inherited models. By Lemma S, the
stores and the HPM agree. The final local search (`v3_engine.h:378–418`) is a deterministic function of its centre, ℓ
and the scores, and uses no RNG. With equal centres its path, returned model and archive are equal, and every model it
evaluates is offered in both versions. The remaining outputs are functions of these objects and of (a):
- E1 uses `island_best`, which is per island (`v3_ledger.h:107–109`);
- E2 uses the log Ẑ_r;
- E3 compares the global best before and after the local search;
- lowESS uses the per-stage ESS.

(c) Provenance is the event at which the model first became the running best in a ledger (`offer_hpm`). The HPM is
the ≻-maximum of everything scored, so it is the running best from its first fresh evaluation on, in every ledger that
scores it. In the serial run that first evaluation is the inherited offer if the HPM is inherited, because inherited
models are offered before any island. Otherwise it is in the lowest-index island that scores it, because islands run in
index order. ∎

**Corollary W-R (stacking).** Run R′ > 4 final islands, where islands 1–4 use streams 10–13 and island r > 4 uses a
stream disjoint from 0–13, all with the same N_e and the same 𝓒. Then islands 1–4 are bitwise those of the R = 4 run. The
scored set before the final local search contains that of the R = 4 run, and so the pre-local-search HPM is ⪰ the R = 4
one. Flags computed on islands 1–4 are identical to v3's.
*Caveat:* the final local search then starts from a centre ⪰ the R = 4 centre. It returns a model ⪰ that centre, but not
necessarily ⪰ the R = 4 run's *post*-local-search HPM. To make the reported HPM exactly monotone in R′, also run the
local search from the R = 4 pre-local-search HPM (one extra search of ≤ (ℓ+1) scans). PROVED by Proposition W(a, b)
and the definition of the HPM.

## Proposition W-cal (worker equivalence of the calibration's diagnostic islands). PROVED (code reading only; not executed)

In `cpp_cal_diag` (`v3_core.cpp:625–668`) the 4 diagnostic islands of iteration `it` read streams 1–4 (or 6–9 at tier 1).
These streams *continue* across iterations (`CalState::stream`, `v3_core.cpp:562–566`). Give each diagnostic island a
persistent worker that owns its stream state across iterations, its own cache, and its own ledger. Before the local
search and before V is built, merge the stores and the HPM into the calibration ledger, which also holds the pilot's
offers. Then:
- the island outputs are bitwise equal, by the argument of W(a);
- V, the grid, the local search, the triggers E1–E3, `grid_unconverged`, the escalation decision and the exported
  inherited set are equal, by W(b). V reads only `lead0`/`lead1` (`v3_core.cpp:675–676`), and the export reads the three
  stores (`:699–701`).

The pilot is a single island, so it is unchanged. Only the score counters differ. ∎

## Proposition P (pooling as R grows at fixed N). PROVED (elementary)

**Setting.** Fixed data and 𝓒 fixed before the final streams. Islands are conditionally iid given 𝓒 (distinct streams,
modelled as independent uniforms: EX-S). The island identities E[W_r | 𝓒] = 1 and
E[W_r·PIP̂_rj | 𝓒] = PIP_j hold for every N ≥ 1 (P6/P7; W2-BOOK Prop. 2(a); the island identity of Prop. 2(c), VERIFIED
by A-REV4). W_r ≤ c_N almost surely for a finite constant, because the state space is finite and the weights are bounded.

(i) **Equal pooling does not improve its bias with R.** PIP^eq_j := R⁻¹ Σ_r PIP̂_rj → E[PIP̂_1j | 𝓒] a.s. as R → ∞
(SLLN). So its limit error is the single-island bias b_j(N) := E[PIP̂_1j | 𝓒] − PIP_j. This bias depends on N and the
regime, not on R.

(ii) **Ẑ-weighted pooling is consistent in R.** PIP^zw_j := Σ_r W_r PIP̂_rj / Σ_r W_r → PIP_j a.s. as R → ∞ (SLLN on
numerator and denominator). This is T31(i). [Literature: Whiteley–Lee–Heine 2016 §5.1; Dai et al. 2022 (4.8); cite as
standard (LIT-PAR).]

(iii) **Non-asymptotic form with a regime-free numerator.** Let e_r ∈ [0, 1] be any island error, for example
e_r = max_j |PIP̂_rj − 1{j ∈ S₀}|, and let ε := E[W_r e_r | 𝓒]. Then for s ∈ (0, 1) and t > 0:

  P(max_j |PIP^zw_j − 1{j∈S₀}| > t | 𝓒) ≤ exp{−R(1−s)²/(2E[W_1² | 𝓒])} + ε/(s t).

*Proof.* max_j |PIP^zw_j − 1{j∈S₀}| ≤ Σ_r W_r e_r / Σ_r W_r, because a convex combination of deviations is bounded by
the same combination of their maxima. On {W̄_R ≥ s} this is ≤ (R⁻¹ Σ W_r e_r)/s, and Markov's inequality gives
P(R⁻¹ Σ W_r e_r > s t) ≤ ε/(s t). For the lower tail of W̄_R, use Maurer's (2003) inequality for iid nonnegative
variables: P(E W − W̄_R ≥ u) ≤ exp{−R u²/(2 E W²)}, here with E W = 1 and u = 1 − s. ∎

With F-MASKPIP M1, ε ≤ δ₁ + ρ̄ + u_π for every island, every regime and every frozen grid (VERIFIED by A-REV9). So the
**Ẑ-weighted PIP is accurate in the masked regime once R ≳ 2 E[W²] log(1/η)/(1−s)²**. The number of islands needed
scales with the single-island relative second moment E[W²] = 1 + Var(Ẑ_r/Z | 𝓒). This is the precise sense of
"correlation costs islands, never correctness". For the equal-weight PIP no such statement holds: by (i), its limit
keeps the single-island bias. In the masked regime that bias is bounded away from 0 whenever a non-crossing island has
probability ≥ κ > 0 (F-MASKPIP N(a)).

*Caveat (honest).* E[W²] can be exponentially large in the masked regime. Then the R needed is impractical, and
Proposition P is a correctness statement, not an efficiency statement. It does not replace DELIV-POP.

(iv) **Pooled-product bias with R islands.** E[Ẑ·PIP^eq_j | 𝓒] − Z·PIP_j = −(1 − 1/R)·Cov(Ẑ_1, PIP̂_1j | 𝓒). This
is Prop. 2(c) with ¾ replaced by 1 − 1/R. *Proof:* expand E[(R⁻¹ Σ_r Ẑ_r)(R⁻¹ Σ_s PIP̂_sj)] over the R diagonal and
R(R−1) off-diagonal terms, using independence and the island identity. ∎

(v) **Unbiasedness, the 95% bound and fixed R.** Pooled Ẑ = R⁻¹ Σ Ẑ_r is conditionally unbiased for every R fixed
before the final randomness, and P(0.05·Ẑ > Z | 𝓒) ≤ 0.05 by Markov. If R is chosen *adaptively* from final-run outputs,
for example "add islands until the SE is small", unbiasedness can fail. This is the same mechanism as W2-BOOK's
CEX-guard, where data-dependent stopping biases E[Ẑ | output]. **Rule: R (or the stacking schedule) must be fixed
before any final-run randomness.**

## Corollary V (same total particles, R islands). PROOF SKETCH

From O-PW2 Theorem A (exact; VERIFIED by A-REV9): N_r·Var(W | 𝓒) = Σ_{s<T} (1 − 1/N_r)^{T−1−s} (E[W_s² μ_s(h²_{s,T})] − 1)
for an island of N_r particles. The pooled variance with R islands of N_r = N/R particles is Var(W)/R. Then:
- To leading order in 1/N_r (O-PW2 Theorem B), N·Var(Ẑ_pooled/Z) = Σ_s (1 − R/N)^{T−1−s} σ²_{s,T} + O(R/N)^{1/2}·(…).
- The leading constant does not increase with R.
- The remainder grows as N_r shrinks.
- In the exact-refresh idealisation, Var(W) = Π_t(1 + χ²_t/N_r) − 1, so R·N_r fixed is neutral while Σ_t χ²_t ≪ N_r.
  With the grid's restricted χ²_t ≈ 1/9 and T ≈ 25, Σ χ²_t ≈ 3 ≪ 312 = 10,000/32.

**Crux not verified:** the stage quantities V_s and H_{s,T} of O-PW2 Theorem B are not re-derived here. The
full-space χ²_t can exceed the restricted value the grid controls (METHODOLOGY §6.7 "Limits"). The masked regime is
outside the leading-order regime.

## Proposition D (depth with particle-parallel islands). PROVED (counting, given the code's structure)

Let m = p + B + 2, s̄ be the mean score cost, I_e ≤ ℓ the rebuild iterations, T_pil and T the pilot and final stage
counts, and T^(i) the stage count of the grid used at rebuild i. Assume one worker per particle per island, with
synchronisation only at reweight/resample, at the end of an island, and between calibration phases. Then the critical
path, in score evaluations, is

  D = D_setup + Σ_{tiers e} [ (T_pil + L + 4) + Σ_{i=1}^{I_e} (T^(i) + L + 4) ] m + (T + L + 4) m
      + (number of local searches)·(ℓ + 1)·⌈scan / width⌉ + O((T_pil + Σ_i T^(i) + T) log N)

plus the grid constructions (≤ 60 |V| T_e log-sum-exps each, scalar and sequential, or log-depth if parallelised over V).
Here D_setup is the depth of the Gram, the clustering, the tables and the convolution. **D does not depend on N, H or R.**
With T ≤ T_e = max(1000, ℓ²), I_e ≤ ℓ and L = O(log n), this gives D = O(m·ℓ·T_e) = O(p log³(n + p)) score evaluations
as the worst case on success. The work W = O(N·m·(ℓ + 2)·T_e) matches the A-REV6 candidate cost bound
O(max(n,p)·p·log³(n+p) + p² log²(n+p)) (V19) when N ∝ max(n, p).

*Proof.* Within a stage the N particle rounds are independent given the resampled population and their uniforms
(IND-T(a) / EX-S). Each round is m sequential elementary steps, each with at most one fresh score, plus a π₀ draw of
O(J + K) operations. Reweighting is an N-term log-sum-exp, and multinomial resampling is a prefix sum plus N
lookups: O(log N) depth each. The calibration phases are sequential by construction: the pilot schedule feeds V and the
grid, and each rebuild's grid feeds the next diagnostics. A local-search scan's evaluations are independent given the
centre. Summing the stages gives D. ∎

*Remark (honest, after LIT-PAR §3.3).* Measured in score evaluations, the depth carries the factor m = p + B + 2 per
round. Removing it needs a different kernel, which is a WORKHORSE change. In wall-clock terms m·s̄ ≈ 2–3 ms at p = 500
(REPORT §6), so the factor is not a practical obstacle at study scale or far beyond it.

# L1 — Lemma R: deterministic polynomial bounds on work and memory; the resource paths never fire

Status: PROVED (by this seat), v2 after R02 (GAP; amendments applied: cache probing, tie DP, allocation term,
memory reconciliation, timing size). Code = production core `Scripts/SMC_BVS/core/` (paths below relative to it).
Premises: EX-A (unit-cost exact arithmetic), IDEAL-W (no overflow), MACH(τ, τ₀, β, β₀) (STATEMENT.md v2 §1).

## R.0 Budgets (deterministic functions of (n, p); `v3_preprocess.R:19-33`)
K = min(p, ⌊n/2⌋) ≤ n/2; B = min(⌊√n⌋, ⌊√p⌋, 16) ≤ 16; ℓ = ⌈log₂(n+p+1)⌉; L = max(4, ⌈log₂(n+1)⌉) ≤ ℓ + 4;
N₀ = max(2500, n, p); H₀ = ⌈512N₀/2500⌉ ≤ N₀; T₀ = max(1000, ℓ²); tier e ∈ {0,1}: (N_e, H_e, T_e) = 4^e(N₀, H₀, T₀).
Write N̄ := 4N₀, T̄ := 4T₀, W := ⌈p/64⌉ (words per bit-set), J ≤ p (number of blocks; packing leaves gaps, so J ≥ ⌈p/B⌉
but always J ≤ p), R′ = 4k declared (k fixed), m := p + B + 2 (labels per particle-round: p Gibbs coordinates, one
uniform swap, B neighbour swaps, one independence step; `cpp/v3_engine.h:202-212`).

## R.1 Every loop is capped (no unbounded loop exists)
| loop | cap | code |
|---|---|---|
| pilot stages | ≤ T_e (L3, Lemma 3.3) | cpp/v3_engine.h:303-341, cpp/v3_calib.h:30-46 |
| diagnostic / final bridge stages | = #grid intervals ≤ T_e (grid built with the `too_many_intervals` cap; frozen grid = a successful construction) | cpp/v3_engine.h:306-308; cpp/v3_calib.h:94 |
| burn-in + measured rounds | L + 4 | cpp/v3_engine.h:342-360 |
| rebuild iterations | ≤ ℓ per tier | v3_calib.R:85 |
| tiers | ≤ 2 (one escalation) | v3_calib.R:141-150 |
| bisection | 60 halvings per call | cpp/v3_calib.h:34-37, :83-85 |
| grid construction | ≤ T_e + 1 appended points, each with ≤ 62 ρ_V evaluations (3 F_V each) | cpp/v3_calib.h:68-98 |
| local search | ≤ ℓ moves, ≤ ℓ + 1 scans, each scan ≤ p + k*(p − k*) models, k* = min(K, ⌊p/2⌋) | cpp/v3_engine.h:378-421 |
| LS0 (spec) | same rules from S̃₀, cap ℓ_n = ℓ (OP-LS0; W1-PXN (K)) | SoP/02_method.tex:490-501 |
| resampling lookup | backward/forward adjustment ≤ N steps per draw | cpp/v3_engine.h:234-260 |
| start-mode ties (spec e4) | fast path: ≤ 10⁶ completed maximisers (recursion depth J; the arg lists store maximisers only, `cpp/v3_start.h:190-194`, so every visited node lies on a completed maximiser: ≤ J·10⁶ nodes); on truncation the tie-aware DP, required here to be W1-N3's reference algorithm TDP or any algorithm within its bound O(p·Σ_b(2^{|C_b|} + (K+1)²)) operations (W1-N3 REPORT (f); `Theory_work/Wave1/W1-N3/lemmas/L7_tie_aware_dp.md`; METHOD_REQUIREMENTS A.2) | SoP/02_method.tex:499-500; cpp/v3_start.h:217-239 (fast path only; the fallback is not in code) |
| other on-call-graph work (Opus C1 #5): `cpp_dup_components` (`v3_fit.R:92`) and `cpp_cut_group` (`v3_fit.R:114`), O(p²) scans + union-find; R-level assembly (`v3_bind_records`, the `order()` in `v3_V_snapshot`, `identical()` grid checks), polynomial in the archive sizes; the integer loops of `v3_isqrt`/`v3_ceil_log2` (`v3_preprocess.R:14-15`), O(√n + log(n+p)) | all ≤ C(p² + archive size·log) — dominated by the np² + p³ + Σ̄ terms | code audit (council C1 Opus #5) |
| exact branch | E ≤ (5H₀ + 4N₀)p models | v3_preprocess.R:28; cpp/v3_core.cpp:69-81, 504-530 |

## R.2 Score evaluations (each is one call of `Scorer::score`, or a cache hit)
Let κ(n, k) be the cost of one score of a size-k model: Gram sub-block O(k²) (or O(nk²) on the refactor route), two
Cholesky O(k³), solves O(k²), the Q fallback O(nk), the QR route O((n+k)k²) (`cpp/v3_score.h:162-238`); so
κ(n,k) ≤ C_s (n + k)k² + C_s ≤ C_s(n³ + 1) for k ≤ K ≤ n/2. Per request there is also a deterministic overhead
ω(n,p): the score cache uses linear probing over ≤ 2^{⌈log₂(1000p)⌉} ≤ 2000p slots with key comparisons of ≤ K + 1
words (`cpp/v3_score.h:264-289`; fixed Zobrist hashes, no hashing assumption), the occasional full-table clear O(p)
(:284), the start component `Start::comp` with a sort O(K log K + J) (`cpp/v3_start.h:52-64`), and the store offers
(three ordered sets of ≤ 40p+1 entries, comparisons of ≤ K ints: O(K log p), `cpp/v3_ledger.h:33-53`); so
ω(n,p) ≤ C_o [p(K + 1) + J + K log(Kp)] ≤ C_o′ p(n + 2). Number of score requests:
- tables: Σ_b 2^{|C_b|} ≤ J·2^B ≤ 2¹⁶ p;
- one island with N particles and T stages: N (initial draws) + N(T + L + 4)·2m (each label scores ≤ 2 models: Gibbs
  both configurations, a swap proposal and the current state, an independence proposal);
- one local search: ≤ (ℓ + 1)(p + p²/4) + 1;
- one V construction: ≤ |V| ≤ 40p + 1 rescorings (`cpp/v3_core.cpp:671-690`; stores of size 20p, 20p, plus ∅);
- calibration tier e: pilot (N = H_e, T ≤ T_e) + local search + ≤ ℓ × [4 islands (H_e, T ≤ T_e) + local search]
  + ≤ ℓ + 1 V constructions;
- final run: inherited models (≤ (40p+1) + 20p + 20p + 1) + R′ islands (N_e, T ≤ T_e) + final search (+ c₄ search when
  R′ > 4) + LS0.
Hence the total number of score requests is at most
  Σ̄(n,p) := 2¹⁶p + 2[(1 + 4ℓ)(4H₀)(1 + (T̄ + ℓ + 8)·2m) + (ℓ + 1)²(p + p²/4 + 1) + (ℓ + 1)(40p + 1)]
            + (80p + 2) + R′·N̄(1 + (T̄ + ℓ + 8)·2m) + 3(ℓ + 1)(p + p²/4 + 1)
           = O((n + p)·p·ℓ·T₀) = O((n + p)·p·log³(n + p))   (T₀ = max(1000, ℓ²)).
On the exact branch the count is E + 200 (timing) ≤ (5H₀ + 4N₀)p + 200.

## R.3 Non-score work (per item, then multiplied by the counts above)
Resampling: O(N) guide table + ≤ O(N²) worst-case lookups per stage; `distinct()`: ≤ O(N²W) per call (hash buckets,
worst case), two calls per stage and one per terminal round; pilot next-φ: 61 ESS evaluations of O(H) per stage; grid:
≤ (T_e + 1)·62·3·|V| operations for the ρ_V evaluations, plus target processing — the sort of the k ≤ T_e pilot
targets and the rescan of the target list at every trial (`cpp/v3_calib.h:70, :74-75`): O(k log k + (T_e + 1)k) =
O(T̄²) per construction, ≤ 2(ℓ + 1) constructions (R05 #2); Fisher–Yates order O(m) per particle-round; π₀ draws (independence step and initial
draws) O(J·B + K log(K+1)) each (incl. the final sort of the emitted indices, `cpp/v3_start.h:174`; charged within ω, R2 Codex #1); RB accumulation O(1) per Gibbs step and O(p) per measured round; V construction O(|V|(K + J)).
Setup: standardisation O(np), Gram O(np²), correlations/distances O(p²), complete linkage ≤ O(p³) (`cpp/v3_blocks.h:
12, 54-61`), neighbour graph O(p² log p) (`cpp/v3_blocks.h:151-170`), tables (above), start DP and convolution
O(J(K + 1)(B + 1) + J2^B). Start-mode ties (LS0 centre, spec): fast path ≤ 10⁶(J + K log K) operations (R.1), and the
TDP fallback ≤ C p·J(2^B + (K + 1)²) ≤ C p²(2¹⁶ + n²). Exact-branch timing (`v3_fit.R:10-14`): a context on
m_t = min(p, max(64, k_t)) columns with k_t = min(K, ⌈p/2⌉) (`v3_fit.R:22`; NOT ⌊p/2⌋), Gram O(n m_t²), then 200
timed scores of size min(k_t, K_t), each with model construction O(k_t log k_t) (`cpp/v3_core.cpp:120-133`): total
U₂₀₀ ≤ C[n m_t² + 200(κ̄ + ω̄ + k_t log k_t)].

## Lemma R (within CONFIG, STATEMENT §1). There are absolute (implementation-dependent, not instantiated) constants
C_W, C_M such that for every valid input (R.4) with n ≥ 3,
every seed and every realisation of the uniforms, the total number of elementary operations of 𝔐 is at most
  W̄(n,p) := C_W [ Σ̄(n,p)·(n³ + p(n + 2)) + (N̄²W + N̄H₀)(T̄ + ℓ + 8)(R′ + 8ℓ + 8) + T̄·p·ℓ + np² + p³
               + p²(2¹⁶ + n²) + 10⁶(p + n log n) + U₂₀₀ + (ℓ + 1)T̄²·(40p + 2)
               + (R′ + 8ℓ + 2)·4N̄·2pB + Cert(n,p) ]
          = O( (n+p)·p·(n³ + pn)·log³(n+p) + (n+p)²·p·log³(n+p) + p²n² + p³ + Cert(n,p) ),
and the number of words held at any time is at most
  M̄(n,p) := 2·C_M [ np + p² + 2¹⁶p + J(K+1)(B+1) + N̄(W + K) + R′·(500p(W + K) + (80p + 1)(K + 4)) + (40p+1)(K + 3)
               + (R′ + 8ℓ + 2)(T̄ + ℓ + 8 + 6p) + K(ℓ + 3)² + 2(ℓ + 1)·min(40p + 1, 10⁴)(K + 3)
               + (R′ + 8ℓ + 2)(T̄ + 1) + 2(ℓ + 1)(T̄ + 1) + (n + K)K·w + 10⁶(K + 1) + n·max(64, k_t) + m_t² + 2pB·(R′ + 8ℓ + 2) + Cert_M(n,p) ]
          = O((n + p)² + Cert_M(n,p)).
*Proof.* Every loop is capped (R.1); the work is the sum over R.2–R.3 of (count) × (cost per item, including ω per
score request), each a polynomial in (n,p) independent of the data, seed and uniforms. The words held at any time are
bounded by the sum of the following, each with its term in M̄: X and the stored Gram (np + p²); correlation and
distance matrices (p²); dendrogram arrays (O(p)); block tables and size profiles (2¹⁶p, J(K+1)(B+1)); the score
cache (500p entries of ≤ W + K words, `v3_calib.R:138`, `v3_run.R:89`) and the three stores (≤ 80p + 1 models of
≤ K + 4 words), per worker when R′ > 4 (factor R′, also covering the merge state); V (≤ 40p + 1 models with 3 doubles);
the population and its resampled copy (N̄(W + K)); the island archives kept in R (pilot ≤ 2, diagnostics ≤ 8ℓ, final
R′ islands; each with O(1) words per stage and per terminal round, the RB rounds 4p, the PIP and RB accumulators 2p:
(R′ + 8ℓ + 2)(T̄ + ℓ + 8 + 6p); `v3_calib.R:49-56, :85-99, :125`); local-search archives (≤ 2(ℓ + 1) + 3 searches,
each ≤ ℓ + 1 scanned models of ≤ K ints: K(ℓ + 3)²); the V snapshots (≤ 2(ℓ + 1) constructions, each ≤ min(40p + 1,
10⁴) models with 2 doubles, `v3_calib.R:17-21`); the guard's checkpoint records (one per bridge stage, per search and
per build, O(1) words each); the stored grids; the scorer workspaces (O((n + K)K) for the QR route); the
tie-enumeration store (≤ 10⁶ models of ≤ K + 1 words) and the TDP tables (≤ J(K + 1) + 2¹⁶p, already counted); the
exact-branch timing context (n·max(64, k_t) + m_t²); and the R-level copies and the serialised fit (at most one more
copy of all of the above: the factor 2). Recursion stacks (exact enumeration, depth ≤ K, `cpp/v3_core.cpp:505-524`;
start-mode enumeration and TDP, depth ≤ J) are O(p) words, covered by MACH's stack clause. Each term is O((n + p)²); the least obvious are 2(ℓ + 1)·10⁴(K + 3) =
O(n log(n + p)) and (R′ + 8ℓ + 2)(T̄ + 6p) = O(log³(n + p) + p log(n + p)). ∎

## R.3′ CONFIG items (R06 #1–#2)
- General-h accumulator, default 𝓗 (size indicators; joint inclusion on neighbour-graph edges, ≤ 2pB pairs,
  SoP/02_method.tex:514-525): O(pB) per particle per measured round, i.e. ≤ (R′ + 8ℓ + 2)·4N̄·2pB operations and
  2pB(R′ + 8ℓ + 2) words (d is already computed per particle). User-declared functions are NOT covered by Lemma R
  (CONFIG; council C1 Codex #1).
- Certificate card (SoP/02_method.tex:540-569, :656): computed under a declared budget; CONFIG requires that budget, Cert(n,p)
  operations and Cert_M(n,p) words, to be polynomial; it never changes the status.
- Concurrency: with w concurrent workers/scorers each holds its own scorer workspace and (when R′ > 4) cache/stores;
  the workspace term is multiplied by w (the cache/stores by R′, already in M̄). w is a declared constant (CONFIG).

## R.4 Raw dimension and inputs (R01 #5)
Lemma R is stated for **valid inputs**: an n × p_raw finite numeric matrix and a finite vector, n ≥ 3, p_raw ≥ 1, valid
declared seed and allocation. Preprocessing touches every raw column (O(n·p_raw) work and memory, `v3_preprocess.R:
97-121`); everything after it depends on the retained p ≤ p_raw. Replace p by p_raw in W̄ and M̄ below (all bounds are
monotone in p). On the classes p_raw = p a.s. (L2 S.1). Exact branch: it is entered only when the saturating count
E = Σ_{k≤K} C(p,k) satisfies E ≤ (5H₀ + 4N₀)p (`v3_preprocess.R:28`, `cpp/v3_core.cpp:69-81`), so its enumeration is
≤ (5H₀ + 4N₀)p ≤ 9N₀p models, polynomial by the branch rule (not by bounding 2^p).

## R.5 Envelopes by unit (R01 #4)
- operations: W̄(n, p_raw) as in Lemma R;
- words held: M̄(n, p_raw) as in Lemma R (timing context, snapshots, guard records, island and search archives, worker
  caches and serialisation are reconciled there);
- bytes: Bytes(n, p_raw) := β M̄ + β₀ (MACH), and the preflight bytes P₀, P₁ at tiers 0, 1, which are the explicit
  sums at `v3_fit.R:27-32` (SMC) and `:23-24` (exact): P_e ≤ 8(3np + 3p²) + 16⌈p/B⌉2^B + 8⌈p/B⌉(K+1)(B+1)
  + 29·2^{⌈log₂(1000p)⌉} + 2000pK + (80p + 1)(4K + 64) + 2·4^e N₀(8W + 4K + 96) = O((n + p)²);
- seconds: Time(n, p_raw) := τ W̄ + τ₀ (MACH), and the exact-branch preflight estimate
  P_t := E·s(k_t), where s(k_t) is the measured seconds of the timed loop divided by 200 (`v3_fit.R:10-14, :22, :25`);
  under MACH the timed loop takes ≤ τU₂₀₀ + τ₀ seconds, so P_t ≤ 9N₀p(τU₂₀₀ + τ₀)/200 =: P̄_t.

## Corollary R (resource paths). Under MACH(τ, τ₀, β, β₀) and a declared allocation with
  mem_n ≥ max{ β M̄(n,p_raw) + β₀, P₀, P₁ } bytes,  time_n ≥ max{ 2(τ W̄(n,p_raw) + τ₀), P̄_t } seconds,
none of B1–B3, E1–E5, X1, X5 of INVENTORY.md fires, for every realisation:
- B1, B3: the preflight bytes are a deterministic function of (n,p) (the exact-branch bytes 8(3np + p²) + 8(40p + 1)
  (k* + 8) + 32p, `v3_fit.R:23-24`, are ≤ P₀ term by term) (`v3_fit.R:17-46`) and are ≤ mem_n by declaration;
- B2: the exact-branch time estimate is P_t ≤ P̄_t ≤ time_n (R.5);
- E1–E5: the guard stops iff elapsed + (just-completed operation) > allocation (`cpp/v3_runtime.h:21-27`); both terms
  are ≤ τW̄ + τ₀ under MACH, so their sum ≤ time_n;
- X1 and X5: peak bytes ≤ β M̄ + β₀ ≤ mem_n, so neither an OOM kill nor an allocation exception occurs (MACH).
The preflight byte formulas are themselves O((n + p)²) (with Cert_M polynomial), and P̄_t = O(N₀p(n³ + pn + n m_t²)), so a sufficient declared
allocation is (allocation$mem_gb = mem_n/2³⁰, allocation$hours = time_n/3600; R06 #6), with an absolute constant C (machine constants τ, τ₀, β, β₀ absorbed), p = p_raw:
  mem_n = C·[ (n + p)² + Cert_M(n,p) ] bytes,
  time_n = C·[ (n+p)·p·(n³ + pn)·log³(n+p) + (n+p)²·p·log³(n+p) + p²n² + p³ + Cert(n,p) ] seconds —
polynomial, as required (R02 #2: the (n+p)²p log³ term is kept); a fixed allocation fails for large n by definition
(SoP/02_method.tex:658).

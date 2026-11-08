# W1-N3 — STATEMENT (target statement for the e4 tie-DP invariant N3)

Ticket: frontier card FR05 / obligation OB03 (`Theory_work/State_of_Project/sections/06_open_and_plan.tex:119-127`).
Lock status: **LOCKED v1.3 (2026-11-08)**; v1.3 = post-council wording fixes (R07); v1.2 = wording/hypothesis-precision fixes from the exhaustive sweep R06 (no clause content changed in either). Previously LOCKED v1.1 after the statement-lock review (`reviews/R01_statement_lock_raw.md`,
disposition `reviews/R01_statement_lock.md`). Changes v1.0 → v1.1 are listed at the end.

Path aliases: `SoP/` = `Theory_work/State_of_Project/sections/`; `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`;
`CODE/` = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`.

## 0. What the specification asks, what the code contains, and the scope of this target

* Specification. LS0 starts "from the start mode S̃₀ = argmax γ₀. S̃₀ is computed exactly by the block DP, with the
  size-then-lexicographic tie rule" and "Start-mode ties: keep the enumeration fast path (cap 10⁶,
  `cpp/v3_start.h:183`). On truncation, use a deterministic tie-aware DP that returns the prescribed smallest-size,
  lexicographically smallest maximiser without enumerating ties (e4, #29)" (`NBH/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md:150`,
  item #8). "The invariant 'DP output = the prescribed choice' is an OPEN obligation (N3)" (same file, line 183, item #26).
  Premise e4: "emitted LS0 centre = the prescribed smallest-size, lexicographically smallest start-mode maximiser (DP
  invariant N3 OPEN)" (`SoP/04_theory.tex:84`).
* Code. The only start-mode routine in the repository is `start_mode`, `CODE/cpp/v3_start.h:178-240` (the copy
  `.../v2_2/core/cpp/v3_start.h` is byte-identical; `Scripts/SMC_BVS/{core,reference/prototype_core}/cpp/v3_start.h`
  are identical modulo line endings). It is a max-plus DP over per-block per-size maxima followed by an enumeration
  of all optimal choices, capped at `cap = 1000000` with a flag. The State-of-Project implementation table records it as
  "present, unused in production; e4 tie-aware DP spec only" (`SoP/02_method.tex:789`), and LS0 itself is not in the
  production core (`SoP/02_method.tex:830-838`). Hence "the DP as coded" = `start_mode`; the e4 fallback DP has no code.
* **Scope (what this target does and does not deliver).** It is (i) a characterisation of what the frozen `start_mode`
  returns, with conditional correctness (under exact arithmetic for its operations, N3 holds for the code whenever
  the number of smallest-size maximisers is ≤ cap), (ii) a precise deviation from the specification under truncation, shown on abstract tables, and (iii) a
  supplementary reference algorithm for the missing fallback, with proof. It does **not** close premise e4 for the
  emitted LS0 centre of an integrated v3.1: LS0 and the fallback are not in production code, and the integration /
  replay (N2(c), ENG02) and its tests (ENG10) remain open. The abstract-table deviation is **not** a counterexample on
  data-generated tables, on LH, or to T38-b1-LH: whether ≥ 10⁶ exact smallest-size ties of the start can arise from
  data is not decided here. (Exact table ties arise from data e.g. through duplicated columns, which the method keeps
  and reports rather than collapses ("Duplicates are kept and reported, not collapsed", `METHOD_v3.1_FINAL.md:182`;
  duplicate report `dup_components`, `CODE/v3_preprocess.R:73-93,128`); a data deviation would
  need N > cap smallest-size maximisers *and* S* outside the ≺_DFS-first cap of them.)
* **Callers.** In the repository `start_mode` is called only by the reference prototype, with the default cap
  (`Scripts/SMC_BVS/reference/prototype_core/cpp/v3_core.cpp:274,710`). The O-LS0 study runs used an export
  `cpp_ls0_start_mode` ("a max-plus convolution over block tables") that is not in the repository, and report that
  S̃₀ "was unique in all 2,400 fits" (`NBH/branch_snapshots/O-LS0/REPORT.md:102-103`); that export's code is not covered
  by this theorem.

## 1. Setting (abstract instance = the inputs `start_mode` reads)

An **instance** is I = (p, K, C, λ, ρ):

* p ≥ 1; internal indices {0, …, p−1}. Internal index a is the a-th retained column in increasing original order
  (`CODE/v3_preprocess.R:112` `kept <- which(!constant)`, passed as `orig` in `CODE/v3_fit.R:123`;
  `CODE/cpp/v3_score.h:18,39-43`), so the map internal → original is strictly increasing and lexicographic order on
  sorted internal index lists equals lexicographic order on sorted original index lists.
* C = (C_0, …, C_{J−1}), J ≥ 1: an ordered partition of {0,…,p−1} into nonempty blocks, each an increasing list,
  |C_b| ≤ 31 (codes are `uint32_t` bitmasks over positions in the block; in the method |C_b| ≤ B ≤ B* = 16). The
  block order is the code's packing order (`st.blocks`, `CODE/cpp/v3_start.h:37`); **no relation between block order and
  index order is assumed.**
* K ∈ {0, …, p} (the method has K = min(p, ⌊n/2⌋), `CODE/cpp/v3_score.h:40`; K = 1 at n ∈ {2, 3}).
* λ : {0,…,K} → ℝ (code: `D.logprior[k]` = log ϖ(k)).
* ρ_b(U) ∈ ℝ for every U ⊆ C_b with |U| ≤ min(|C_b|, K), with ρ_b(∅) = 0 (code: `st.logr[b][code(U)]`,
  `CODE/cpp/v3_start.h:89-96`, where code(U) = Σ_{x∈U} 2^{pos(x)} and pos(x) is x's position in the increasing list C_b).
  Entries with |U| > K (NaN in the code) are never read by `start_mode`.

**Domain enlargement.** λ and ρ are arbitrary reals. In the method λ is the capped BB(1,p) log-prior
(`CODE/cpp/v3_score.h:63-70`) and ρ_b are log Bayes-factor tables from the scorer (`CODE/cpp/v3_start.h:93-95`); the
theorem covers these as a special case. So (a)–(c) apply to production tables with the subsequent arithmetic of
`start_mode` idealised under (H2), and (e) applies to production tables provided (H2-FP) holds for the run; the deviation
instances in (d) use tables that are not shown to be producible by the scorer.

For S ⊆ {0,…,p−1} write S_b := S ∩ C_b. Feasible set Ω_K := {S : |S| ≤ K}. Objective
f(S) := λ(|S|) + Σ_b ρ_b(S_b),  S ∈ Ω_K.

For an abstract instance define γ₀(S) := exp f(S), Z̄₀ := Σ_{S∈Ω_K} γ₀(S), π₀ := γ₀/Z̄₀ on Ω_K, so
log π₀(S) = f(S) − log Z̄₀ and argmax_{Ω_K} π₀ = argmax_{Ω_K} f =: 𝒜. In the method specialisation (λ = log ϖ,
ρ_b = log r_b) these are the D0 objects ("Start/bridge" row, `SoP/04_theory.tex:73`; code `CODE/cpp/v3_start.h:68-70`).
(The M3(c) factorisation, `SoP/04_theory.tex:299`, is stated for blocks of size ≤ K and is not used here.)

**Exact scores vs exact tables.** Shared EX-A asserts exact mathematical scores *and* exact arithmetic
(`SoP/04_theory.tex:78`). The theorem is a statement about the table-defined objective f: under full EX-A, f is log γ₀
of the mathematical scores; when the tables are the scorer's doubles, (a)–(d) are statements about f built from those
doubles with subsequent arithmetic idealised (a weaker idealisation than EX-A), and (e) is the native-double statement.

**Prescribed start mode** (method's tie rule "smallest |S|, then lexicographically smallest index set",
`SoP/02_method.tex:470`; `lex_less`, `CODE/cpp/v3_util.h:117-119`):
k* := min{|S| : S ∈ 𝒜},  𝒜* := {S ∈ 𝒜 : |S| = k*},  N := |𝒜*|,  S* := the lex_less-minimum of 𝒜* (sorted index vectors).
𝒜 ≠ ∅ since Ω_K is finite and nonempty; lex_less restricted to distinct sorted vectors of a common length is a strict
total order, so S* is well defined.

**DFS order.** For S ⊆ {0,…,p−1} define its key
κ(S) = ( |S_{J−1}|, code(S_{J−1}), |S_{J−2}|, code(S_{J−2}), …, |S_0|, code(S_0) ),
and S ≺_DFS S' iff κ(S) < κ(S') lexicographically (numeric comparison in each coordinate). κ is injective, so ≺_DFS is a
strict total order on sets.

## 2. Hypotheses

* (H1) **Encoding.** I is an instance as in §1 and `start_mode(st, cap)` is called with: `st.D` a valid pointer to a
  `Data` with `D->K = K` and `D->logprior` of length K+1 equal to λ; `st.J = J`; `st.blocks[b]` = C_b (increasing);
  `st.logr[b]` of length 2^{|C_b|} with `st.logr[b][code(U)] = ρ_b(U)` for |U| ≤ min(|C_b|,K) and `st.logr[b][0] = 0`;
  `st.logprof[b]` of length min(|C_b|,K)+1 (only its length is read); `st.codes_by_size[b][j]`, j ≤ min(|C_b|,K), the
  size-j codes in increasing numeric order. These are exactly the fields set by `build_tables`/`build_start`
  (`CODE/cpp/v3_start.h:76-151`). For (e) additionally `st.blk`, `st.pos` are the inverse of `st.blocks`
  (x = `blocks[blk[x]][pos[x]]`), as set at `CODE/cpp/v3_start.h:79-80`, because `comp` reads them.
* (H2) **EX-A for start_mode's arithmetic**: every addition and comparison on `double`s inside `start_mode` is read as
  exact real arithmetic on the reals λ, ρ; NEG_INF (`CODE/cpp/v3_util.h:22`) is −∞ with −∞ + x = −∞ and −∞ < x for real x.
  (Clause (e) replaces (H2) by (H2-FP).)
* (H2-FP) (for (e) only) IEEE-754 binary64 arithmetic with round-to-nearest-even, each source-level `+` and comparison
  executed as written (no extended precision, no reassociation/contraction/fast-math), all λ(k) and read ρ_b(U) finite,
  and **every intermediate sum formed by `start_mode` and by `log_gamma0` finite** (no overflow).
* (H3) cap ≥ 1 (the method uses the default cap = 10⁶).
* (H4) **Execution** (for the claims about the frozen C++ only): cap is representable as a positive `long`; K + 1,
  J + 1 and the loop counters of `start_mode` are representable as `int`; |C_b| ≤ 31; all allocations succeed and the
  recursion (depth J) and enumeration complete. (Integer arithmetic is not covered by (H2).) The mathematical
  statements about the algorithm, the family D_m and TDP (f) do not need (H4).

## 3. Theorem N3-code (what the frozen `start_mode` returns)

Let `res = start_mode(st, cap)`. Under (H1), (H2), (H3), (H4):

* **(a) Value and membership.** `res.lg0` = max_{Ω_K} f, and `res.S` ∈ 𝒜*: the returned set is always a maximiser of π₀
  of the smallest maximising size, truncated or not.
* **(b) Counting and flag.** The enumeration visits elements of 𝒜* only, in increasing ≺_DFS order, each at most once,
  and it visits exactly the ≺_DFS-first min(N, cap) elements of 𝒜*. `res.ties` = min(N, cap) and
  `res.truncated` = [N ≥ cap] (true also at N = cap, when every element has been visited).
* **(c) Invariant N3 for the code (conditional).** If N ≤ cap, then `res.S` = S*. In particular `res.truncated == false`
  ⇒ `res.S` = S*. With the default cap this holds whenever the start has fewer than 10⁶ + 1 smallest-size maximisers
  (N ≤ C(p, k*) ≤ max_{k≤K} C(p, k); so always when max_{k≤K} C(p, k) ≤ 10⁶, in particular for p ≤ 22).
* **(d) Deviation under truncation.** If N > cap, `res.S` = the lex_less-minimum of the ≺_DFS-first cap elements of 𝒜*,
  which in general differs from S*. For every cap ≥ 1 there is an instance (abstract tables) with N > cap on which the
  algorithm returns a set ≠ S* (the family D_m of L6 with any cap ≤ 2^m; the frozen code returns that set whenever (H4)
  holds for (D_m, cap)); for cap = 10⁶ an explicit instance has p = 44, K = 22. The frozen code has no tie-aware fallback, so the
  specification's e4 sentence "On truncation, use a deterministic tie-aware DP …" is not implemented.
* **(e) Floating point.** Under (H1), (H2-FP), (H3), (H4), with ĝ(S) := `st.log_gamma0(S)` (the code's own evaluation,
  `CODE/cpp/v3_start.h:54-69`): `res.lg0` = max_{Ω_K} ĝ, ĝ(`res.S`) = `res.lg0` exactly, and
  |`res.S`| = min{|S| : ĝ(S) = max ĝ}. The lexicographic part of (c) can fail in floating point relative to ĝ (explicit
  examples), because rounding can create ĝ-ties that the enumeration, which follows per-block exact maximisers and exact
  prefix equalities, does not visit.

## 4. Supplementary result (the e4 fallback as specified; reference algorithm, not frozen code)

* **(f) Tie-aware DP.** The algorithm TDP of `lemmas/L7_tie_aware_dp.md` (fix V* and k* by the max-plus DP; then for
  i = 0,…,p−1 force i in if some element of 𝒜* is consistent with the decisions so far plus i ∈ S, else force i out;
  feasibility by a constrained max-plus DP) returns S* for every instance under exact arithmetic, without enumerating
  ties, using O(p · Σ_b (2^{|C_b|} + (K+1)²)) arithmetic operations and comparisons. It is not implemented in any code
  path of the method; integrating it is engineering work (ENG10/ENG02).

## 5. Boundary cases covered

K binding (K < p with k* = K, and K < |C_b| for some b); K = 0; K = 1 (n ∈ {2,3}; at n = 2 the method's B = 1 so blocks
are singletons); N ∈ {cap−1, cap, cap+1}; ties within a block whose code order differs from lex order; ties between size
allocations across blocks; ties across sizes. n = 2 is exercised only by direct calls of the routine on standardised
data: the public preprocessing rejects n < 3 (`CODE/v3_preprocess.R:106`), and n = 2 admission is the unimplemented
proposal e3 (`NBH/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md:182`).

## Changes v1.0 → v1.1 (statement-lock fixes R01 #1–#5)
1. §0 Scope paragraph: what is delivered vs what stays OPEN (e4 for the integrated emitted centre); abstract-table
   deviation ≠ data/LH counterexample.
2. (H1) spells out the `Start` encoding invariants (incl. `st.J`, `st.D`, `blk`/`pos` for (e)); domain-enlargement and
   exact-score vs exact-table paragraphs; source pointers corrected (`04_theory.tex:73`, `:78`; full path aliases).
3. (H2-FP): execution model (round-to-nearest-even, no reassociation/contraction/extended precision) and finite
   intermediates (no overflow). (e) text: rounding-created ties also at prefix/prior additions.
4. (b)/(c) wording at N = cap made explicit; complexity in (f) stated per block.
5. §5 n = 2 scope (routine test vs preprocessing rejection).

## Changes v1.1 → v1.2 (exhaustive-sweep fixes R06 #1–#4, #11; no clause content changed)
1. Production-input sentence qualified by (H2) / (H2-FP); scope conditional qualified by exact arithmetic (R06 #1).
2. New (H4) execution hypothesis (positive `long` cap, `int`-representable dimensions/counters, allocation and
   completion) for the frozen-C++ claims; (d) separates the mathematical family from its execution (R06 #2).
3. Abstract γ₀, Z̄₀, π₀ defined directly; D0 only in the method specialisation (R06 #3).
4. M3(c) factorisation sentence restricted to its source domain (blocks ≤ K) and marked unused (R06 #4).
5. "byte-identical" used only for the v2_2 copy (R06 #11).

## Changes v1.2 → v1.3 (council round 1 minor points, R07; no clause content changed)
1. (c): explicit bound N ≤ C(p,k*) ≤ max_{k≤K} C(p,k) (Opus #6).
2. (d): the "frozen code does so" sentence restricted to D_m with cap ≤ 2^m under (H4) (Opus #3).
3. §0: duplicated columns as the known source of exact ties and what a data deviation needs (Opus #6); new "Callers"
   paragraph (prototype with default cap; O-LS0's `cpp_ls0_start_mode` not in repo, mode unique in 2,400 fits) (Opus #4).

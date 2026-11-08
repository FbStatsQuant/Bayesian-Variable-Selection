# W1-N3 — PLAN

Target: `STATEMENT.md` (Theorem N3-code (a)–(e), supplementary (f)).

## Lemmas (one file each in `lemmas/`)

| id | content | used for | route |
|---|---|---|---|
| L1 | Reduction: argmax π₀ = argmax f on Ω_K; the prescribed choice is the (size, lex)-least element of 𝒜; lex_less on internal indices = lex on original indices | all | definitions (D0, `v3_start.h:68-70`), strictly increasing `kept` map |
| L2 | Per-block maxima: `mb[b][j]` = max{ρ_b(U): U⊆C_b, |U|=j}; `arg[b][j]` = all maximisers, increasing code order; `mb[b][0]=0`, `arg[b][0]={0}` | (a)–(d) | read `v3_start.h:186-197` under EX-A |
| L3 | Max-plus DP: `M[b][k]` = V_b(k) := max of Σ_{c<b} ρ_c(U_c) over choices of total size k (−∞ iff infeasible) | (a)–(d) | induction on b |
| L4 | Size selection: `vbest` = max f, `kbest` = k* | (a) | from L3, strict `>` scan in increasing k |
| L5 | Tightness characterisation + enumeration: S of size k has Σ_b ρ_b(S_b) = V_J(k) iff every prefix is tight and every block choice is a per-block maximiser; `rec(J,kbest)` visits exactly 𝒜* in ≺_DFS order, each once; the `r != 0` branch is dead | (a), (b) | backward induction; DFS loop order j ascending, codes ascending |
| L6 | Selection and truncation: `bestS` = lex-min of visited; count/flag semantics; cap-dependence; counterexample family (any cap; explicit p = 44 instance for cap = 10⁶) | (b)–(d) | read lines 214-238; construct instance with a within-block tie whose code order ≠ lex order in the DFS-outermost block plus 20 inner binary ties |
| L-FP | Floating-point version: monotonicity of round-to-nearest addition ⇒ DP max = max of the code's fold ĝ; size selection; FP counterexample to the lex part | (e) | monotone rounding; explicit example |
| L7 | Tie-aware DP TDP (spec e4): greedy inclusion of indices 0..p−1 with a constrained max-plus feasibility DP; returns S* | (f) | lex-min of a family of equal-size sets is greedy-inclusive (min of symmetric difference) |

## Numerics (`numerics/`)

1. `sm_harness.cpp`: includes the frozen header `v3_start.h` read-only by path; compiled with `-msse2 -mfpmath=sse -ffp-contract=off`. Modes: TABLE (direct λ, ρ, blocks, K, cap) and DATA (X, y, B → `data_init`, `make_blocks`, `Scorer`, `build_tables`, `build_start`, `start_mode`; prints the code's own tables).
2. `brute.py`: enumerate Ω_K exactly (Python ints for integer tables; `fractions.Fraction` of the doubles for data tables = EX-A reading); compute 𝒜, k*, 𝒜*, S*, ≺_DFS order; check (a)–(d) clause by clause, and (e) with an exact replica of the code's float fold.
3. Instance families (p ≤ 12): random integer tables with heavy ties (values in small ranges), random interleaved partitions and block orders, K over its range incl. 0, 1 and binding; constructed ties (all-equal tables, allocation ties, code≠lex within-block ties, cross-size ties); truncation with cap ∈ {1,2,3,5}; DATA mode with Gaussian X incl. duplicated columns, n ∈ {2,3,4,6,10,20}; exhaustive small family (p ≤ 3, all ordered partitions, all K, tables/prior in a small value set).
4. Default-cap counterexample (p = 44) run through the frozen code; S* computed by TDP and by the construction's closed form.
5. TDP (`tdp.py`) checked against brute force on all the above.

## Reviews (protocol)
Statement lock (Codex Sol) → per-lemma: falsification (numerics) + Sol line-by-line check → mid-point review after L5 (fresh Sol, STATEMENT + lemmas only) → exhaustive sweep (Sol) → council (Sol high + Opus 5.5 high), ≤ 3 rounds.
Sequencing (after R01): batch 1 = L1–L5 (falsification in `numerics/` + one Sol line-by-line check with a verdict per lemma) before anything uses them; then the mid-point review (fresh Sol, STATEMENT + L1–L5 only), stop on REDIRECT/STOP; batch 2 = L6, L-FP, L7 (falsification + Sol check); then exhaustive sweep and council. Compute: 2 declared seeds; exhaustive p ≤ 12 per the ticket's explicit request; p = 44 instance proved analytically, run only as confirmation. FR05's assembly / LH replica are not in this thread's scope.

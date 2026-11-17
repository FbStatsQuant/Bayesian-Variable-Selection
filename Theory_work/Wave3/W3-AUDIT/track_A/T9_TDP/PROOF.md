# T9 · Lemma TDP — PROOF v3 (second seat on `C-ENG/lemmas/TDP_E.md`; code `Scripts/SMC_BVS/core/cpp/v3_start.h`)

v2 → v3 (council R1, Sol #3): every step below that speaks of what the compiled routine returns assumes (H4) of the
STATEMENT (counters and cap representable, allocations succeed, recursion completes); the algorithmic arguments do not
need it.

Each step of TDP_E is checked against the code; deviations are noted. Paths below are relative to `Scripts/SMC_BVS/core/`.

## Objects (TDP_E lines 6–13)
`mode_dp` (`cpp/v3_start.h:195-226`): `mb[b][j]` = max of `logr[b][c]` over the size-j codes, `arg[b][j]` the codes
attaining it, in increasing code order (`cpp/v3_start.h:201-209`; a strictly larger value resets the list, an equal one
appends); `top = logprof[b].size() − 1 = t_b` (T4). For j = 0 the only code is 0 with `logr[b][0] = 0`, so
`mb[b][0] = 0`, `arg[b][0] = {0}`. `M[0][0] = 0`, `M[0][k] = −∞`, `M[b][k]` = max over j ≤ min(t_{b−1}, k) with
`M[b−1][k−j] ≠ −∞` of v(b, k, j) (`cpp/v3_start.h:211-219`). k̂ = first k with `logprior[k] + M[J][k]` maximal (strict
`>`, `cpp/v3_start.h:220-224`). `mode_tight` (`cpp/v3_start.h:229-233`) is TDP_E's tight edge, with the same expression
as `rec` (`cpp/v3_start.h:294-296`). Matches TDP_E.

## (TDP-a)
`rec(b, r)` (`cpp/v3_start.h:281-300`) at b = 0 accepts only r = 0 and builds S from `choice`; at b ≥ 1 it follows
exactly the tight edges (b, r, j) and, for each, every code in `arg[b−1][j]`. So the leaves visited are the elements of E
reached in DFS order, with their path and codes. Two leaves give different sets: S determines U_b = S ∩ C_b, hence
j_b = |U_b| and code(U_b) (the code ↔ set map is T4's). Every element of E is reached unless the recursion stops at
`count ≥ cap` (`cpp/v3_start.h:290, 282, 297`). `res.S` = lex_less-minimum of the visited sets (`cpp/v3_start.h:289`).
Without truncation, `res.S` = lex_min E. Every element has size Σ j_b = k̂.

## (TDP-b)
*E ≠ ∅* (TDP_E (2)). M[b][0] = 0 for every b (only j = 0 is allowed at k = 0), so k̂ ≥ 0 exists. Every finite M[b][r]
(b ≥ 1) was assigned some v(b, r, j), and the comparison at `cpp/v3_start.h:218` stores that exact double, so a tight
edge into (b − 1, r − j) with M finite exists; M[0][r] is finite only for r = 0; and `arg[b][j] ≠ ∅` whenever `mb[b][j]`
is finite. Following tight edges from (J, k̂) therefore reaches (0, 0). With IN = OUT = ∅ every nonempty `arg[b][j]` is allowed
(`arg[b][0] = {0}`; `arg[b][j] ≠ ∅` for finite `mb[b][j]`, and all entries are finite by T4), so the root
`feasible()` returns true and `cpp/v3_start.h:261` does not fire: this is (TDP-e).
*Feasibility* (TDP_E (1)). `allowed[b][j]` = ∃ c ∈ `arg[b][j]` with (IN ∩ C_b) ⊆ U(c) and U(c) ∩ OUT = ∅, coded with
per-block position masks (`cpp/v3_start.h:240-246`; `(c & inm) == inm`, `(c & outm) == 0`). `reach` is computed forward
from (0, 0) over tight, allowed edges (`cpp/v3_start.h:249-257`), so `reach[J][k̂]` holds iff some tight path from
(J, k̂) to (0, 0) has an allowed code at every block, iff some S ∈ E satisfies IN ⊆ S and S ∩ OUT = ∅ (the blocks
partition the index set, so the constraint splits by block). TDP_E's (⇐)/(⇒) argument is this, and is correct.
*Greedy* (TDP_E (3)). The loop runs i = 0..p − 1 in internal order (`cpp/v3_start.h:263-268`; internal indices are the
kept columns in increasing original order, `v3_setup.R:8`, so lex on internal = lex on original); it tentatively adds
i to IN (`inm`, via `st.blk[i]`, `st.pos[i]` — the inverse maps of T4), keeps it if feasible, else moves it to OUT.
Invariant Inv(i): IN = S_E ∩ {0..i−1}, OUT = {0..i−1} ∖ S_E, S_E := lex_min E. If i ∈ S_E, S_E witnesses feasibility.
If i ∉ S_E and some S ∈ E were feasible with i added, S and S_E agree below i, i ∈ S, and the next element of S_E after
the common prefix is > i (it exists because |S| = |S_E| = k̂); so S is lex-smaller than S_E — a contradiction. Hence
Inv(p): the returned S = S_E. The check at `cpp/v3_start.h:261` never fires (E ≠ ∅). TDP_E's step (3) is this.
*In `start_mode`*: if `trunc` (`count ≥ cap`) and `tie_dp`, `res.S` is replaced by `mode_tie_dp` (`cpp/v3_start.h:303`);
otherwise `rec` saw all of E (`count < cap`). Either way `res.S` = lex_min E (TDP_E (4)). The arithmetic is only the
expressions v(b, r, j) and `logprior[k] + M[J][k]`, compared consistently in `mode_dp`, `rec` and `mode_tight`; so the
statement holds for the computed doubles under (H2-FP) (`Scripts/SMC_BVS/core/cpp/Makevars.v3`, as TDP_E cites) and
a fortiori under EX-A.

## (TDP-c) E = 𝒜* under EX-A (direct, for the code at the pin)
Under EX-A the DP values are exact: `mb[b][j]` = max_{U⊆C_b, |U|=j} ρ_b(U); M[b][r] = the maximum of Σ_{c<b} ρ_c(U_c) over
(U_c)_{c<b}, U_c ⊆ C_c, Σ_c |U_c| = r (max-plus convolution; `cpp/v3_start.h:211-219`), −∞ if no such tuple. For S ∈ Ω of
size k with U_b = S ∩ C_b, f(S) = λ(k) + Σ_b ρ_b(U_b) ≤ λ(k) + M[J][k], with equality for some S of size k; so
max_Ω f = max_k (λ(k) + M[J][k]) and the smallest maximising size is k̂ (strict `>` scan, `cpp/v3_start.h:220-224`), i.e.
k* = k̂. Now let |S| = k̂, j_b := |U_b|, r_b := Σ_{c<b} j_c. Then Σ_b ρ_b(U_b) ≤ Σ_b mb[b][j_b], and each slack
d_b := M[b][r_b] − M[b−1][r_{b−1}] − mb[b−1][j_{b−1}] is ≥ 0 by the definition of M (for j = 0, mb = 0 and v = M[b−1][r]),
with Σ_b d_b = M[J][k̂] − Σ_b mb[b][j_b] (telescoping, M[0][0] = 0). So Σ_b ρ_b(U_b) = M[J][k̂] — i.e. S ∈ 𝒜* — iff every
code(U_b) ∈ `arg[b][j_b]` and every d_b = 0, i.e. every edge (b, r_b, j_{b−1}) is tight: iff S ∈ E. Hence E = 𝒜* and
lex_min E = S*. (This does not use W1-N3's proof of N3-code (b), which concerns an earlier copy of `start_mode`; at the
pin the DP and enumeration arithmetic is the same but has been moved into `ModeDP`.) ∎

## (TDP-d) cost and storage
`feasible()` loops over b ≤ J, r ≤ K, j ≤ t_{b−1} with O(1) work per triple (`mode_tight` is O(1)):
O(Σ_b (K + 1)(t_b + 1)). Each loop iteration of the greedy calls `refresh(b)` at most twice, O(Σ_j |arg[b][j]|) ≤
O(2^{|C_b|}), and `feasible()` once; plus one initial `refresh` of every block and one root `feasible()`. Total
O(Σ_b 2^{|C_b|} + p·(Σ_b (K + 1)(t_b + 1) + max_b 2^{|C_b|})). Since t_b + 1 ≤ K + 1 and max_b 2^{|C_b|} ≤ Σ_b 2^{|C_b|},
this is within O(p·Σ_b(2^{|C_b|} + (K + 1)²)). Storage: `M` and `reach` (J + 1)(K + 1); `mb`, `allowed` Σ_b (t_b + 1);
`arg` ≤ Σ_b 2^{|C_b|} codes; masks 2J: O(Σ_b 2^{|C_b|} + J(K + 1)). TDP_E's own cost line (`Theory_work/Wave1C/C-ENG/lemmas/TDP_E.md:62-64`) states the same operations bound with
J(K + 1)(B + 1) for Σ_b (K + 1)(t_b + 1); it states no storage bound, supplied here.
*Enumeration fast path.* Every node (b, r) that `rec` enters has M[b][r] finite, hence a tight edge to a node with finite
M (the argument of (TDP-b)), down to (0, 0); so every branch ends at a leaf, and each leaf has at most J internal ancestors.
An internal node costs O(t_b + 1) plus one call per child; a leaf costs O(p log p) (building, sorting and comparing S,
`cpp/v3_start.h:285-289`). With at most min(|E|, cap) leaves the fast path costs O(min(|E|, cap)·(J(B + 2) + p log p)).

## Re-check verdict on `C-ENG:TDP_E`
Its mathematics is correct. Points to record: (i) the tight-edge equality tests are exact because `mode_tight` and `rec`
recompute the same expression on the same doubles, which is deterministic under (H2-FP) with `-ffp-contract=off`
(`Scripts/SMC_BVS/core/cpp/Makevars.v3`), and the stored M[b][r] is one such value; (ii) its claim (4) "for every cap ≥ 1"
holds at the pin only for cap ≥ 2 with `tie_dp = true`: `start_mode` rejects cap < 2 (`cpp/v3_start.h:272`; C-PACK MR2,
`cpp/v3_start.h:185-186`) — the shipped call uses 10⁶; (iii) its line references to `v3_start.h` are stale (e.g. `rec`
"v3_start.h:217-237", now `cpp/v3_start.h:281-300`); (iv) the storage bound required by TDP-IMPL and the fast-path cost
were not in TDP_E and are added in (TDP-d).

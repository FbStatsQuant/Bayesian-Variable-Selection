# L-FP — Clause (e): what `start_mode` returns in binary64

Status: PROVED; cross-family check: R05 CORRECT-WITH-MINOR-FIXES (Sol; monotonicity wording, fixed). (iv) indexing repaired after R04 (mid-point). Uses only (H1), (H2-FP), (H3), (H4) and the code; it does not
use L2–L5 (which assume EX-A), but repeats their structure with ≤ in place of = where rounding enters.

## Setting
⊕ = binary64 addition with round-to-nearest-even; all score-addition operands and results considered below are finite
by (H2-FP); −∞ (NEG_INF) remains the sentinel for infeasible cells and initial maxima, and enters only comparisons and the
skip tests. Comparisons (`>`, `==`,
`!=`) are exact on doubles. **Monotonicity:** if x ≤ x′ then x ⊕ y ≤ x′ ⊕ y (and symmetrically), because exact addition
is monotone and the rounding map rn (round-to-nearest, ties-to-even) is nondecreasing: for u < u′, if r := rn(u) > r′ :=
rn(u′), then r being at least as near to u as r′ gives u ≥ (r + r′)/2, and r′ being at least as near to u′ as r gives
(r + r′)/2 ≥ u′, so u ≥ u′, a contradiction; for u = u′ the deterministic ties-to-even rule gives identical outputs. (Both
r, r′ are finite by (H2-FP).) ⊕ is commutative.
Write x ⊕′_j y := x if j = 0, x ⊕ y if j > 0.

For a tuple (U_0,…,U_{b−1}) define the fold F_0 := 0, F_{c+1} := F_c ⊕′_{|U_c|} ρ_c(U_c). For a set S with tuple (S_c),
F_J(S) is exactly the value s of `Start::comp` (`CODE/cpp/v3_start.h:54-66`): s starts at 0 and adds `logr[b][code(S_b)]`
for the blocks met by S in increasing b (H1 gives blk/pos inverse to blocks, so the codes are code(S_b)); blocks with
S_b = ∅ are skipped, which is the identity step of ⊕′_0. Hence ĝ(S) = `log_gamma0(S)` = λ(|S|) ⊕ F_J(S)
(`CODE/cpp/v3_start.h:69`).

## Statement
Under (H1), (H2-FP), (H3), (H4): (i) `mb[b][j]` = max{ρ_b(U) : |U| = j} and `arg[b][j]` = all codes attaining it (ascending);
(ii) `M[b][k]` = max{F_b(U_0..U_{b−1}) : tuple in Ch_b(k)} (−∞ iff Ch_b(k) = ∅); (iii) `res.lg0` = vbest = max_{Ω_K} ĝ and
kbest = min{|S| : ĝ(S) = max ĝ}; (iv) every processed leaf builds S with F_J(S) = M[J][kbest], hence ĝ(S) = `res.lg0`;
at least one leaf is processed; so ĝ(`res.S`) = `res.lg0` exactly and |`res.S`| = kbest. (v) The lex part of clause (c)
can fail relative to ĝ.

## Proof
(i) L2's proof uses only exact comparisons of the stored doubles; it applies verbatim.

(ii) Induction on b; b = 0 as in L3. Step: by the code (lines 200–206), M[b][k] = max over j ∈ {0..min(t_{b−1},k)} with
M[b−1][k−j] ≠ −∞ of M[b−1][k−j] ⊕′_j mb[b−1][j] (−∞ if no such j). Upper bound: for a tuple in Ch_b(k) with
j = |U_{b−1}|, F_{b−1} ≤ M[b−1][k−j] (induction; in particular M[b−1][k−j] ≠ −∞) and ρ_{b−1}(U_{b−1}) ≤ mb[b−1][j] (i);
by monotonicity in both arguments F_b = F_{b−1} ⊕′_j ρ_{b−1}(U_{b−1}) ≤ M[b−1][k−j] ⊕′_j mb[b−1][j] ≤ M[b][k].
Attainment: if M[b][k] ≠ −∞ it equals the term of some j*; by induction some tuple in Ch_{b−1}(k−j*) has
F_{b−1} = M[b−1][k−j*]; append any U with code in arg[b−1][j*]; its fold is M[b−1][k−j*] ⊕′_{j*} mb[b−1][j*] = M[b][k].
If M[b][k] = −∞, no j has M[b−1][k−j] ≠ −∞, so all Ch_{b−1}(k−j) are empty (induction) and Ch_b(k) = ∅.

(iii) As in L3, Ch_J(k) ≅ {S : |S| = k} ≠ ∅ for k ≤ K, so M[J][k] = max_{|S|=k} F_J(S) is finite. By monotonicity,
max_{|S|=k} ĝ(S) = max_{|S|=k} (λ(k) ⊕ F_J(S)) = λ(k) ⊕ M[J][k] = the code's v at line 210 (operands
`D.logprior[k] + M[J][k]`, the same operation as `log_gamma0`'s `D->logprior[S.size()] + comp(S)` up to commutativity).
The strict scan (lines 208–212) returns vbest = max_k v_k = max ĝ and the smallest k attaining it, exactly as in L4.

(iv) Along a root-to-call path write q_b for the remainder argument of the call rec(b, q_b) (q_J = kbest) and c_c for
the code chosen at level c+1 (so q_c = q_{c+1} − popcount(c_c)). Every call rec(b, q_b) satisfies (I_FP):
M[b][q_b] ≠ −∞, q_b + Σ_{c≥b} popcount(c_c) = kbest, and for each c ≥ b
M[c+1][q_{c+1}] = M[c][q_c] ⊕′_{popcount(c_c)} mb[c][popcount(c_c)] and ρ_c(c_c) = mb[c][popcount(c_c)]
(the checks at lines 230, 232 and c_c ∈ arg[c][·]). At a leaf, q_0 = 0 (M[0][q_0] ≠ −∞); the built set S has S_c = the
subset with code c_c, and R_b := Σ_{c<b}|S_c| equals q_b (by q_0 = 0 and q_{c+1} = q_c + |S_c|), so the recorded
equalities read M[c+1][R_{c+1}] = M[c][R_c] ⊕′_{|S_c|} ρ_c(S_c) for c = 0..J−1. Forward induction:
F_0 = 0 = M[0][0]; F_{c+1} = F_c ⊕′ ρ_c(S_c) = M[c][R_c] ⊕′ ρ_c(S_c) = M[c+1][R_{c+1}]. So F_J(S) = M[J][kbest], and
ĝ(S) = λ(kbest) ⊕ M[J][kbest] = vbest.
At least one leaf: rec(J, kbest) has M[J][kbest] ≠ −∞; for any call rec(b, r), b ≥ 1, with M[b][r] ≠ −∞, M[b][r] is the
maximum of finitely many candidate values v_j, so some j attains it, passes lines 230 and 232, and arg[b−1][j] ≠ ∅; its
child rec(b−1, r−j) has M[b−1][r−j] ≠ −∞. Descending, the first such path reaches a leaf; it is processed because trunc
is false until the first leaf is processed. bestS is set at the first leaf and later only replaced by other processed
leaves, so `res.S` is a processed leaf. (The ordering and counting statements of L5 are not claimed here: in floating
point the visited family is the set of "exactly tight" paths, which may be a proper subset of the ĝ-maximisers of size
kbest.)

(v) Examples (`numerics/fp_example.py`, run through the frozen code):
1. Blocks C_0 = {0} with ρ = 1000.0, C_1 = {1,2} with ρ{1} = 10⁻¹⁴, ρ{2} = 2·10⁻¹⁴, ρ{1,2} = −5; K = 2;
   λ = (0, −1, 0). Since 2·10⁻¹⁴ < ½ ulp(1000) = 2⁻⁴⁴, 1000 ⊕ 10⁻¹⁴ = 1000 ⊕ 2·10⁻¹⁴ = 1000, so ĝ({0,1}) = ĝ({0,2}) =
   1000 = max ĝ (other sets: ĝ(∅) = 0, ĝ({0}) = 999, ĝ({1,2}) < 0, singletons {1},{2} ≈ −1). The size-then-lex choice under
   ĝ is {0,1}; arg[1][1] = {code of {2}} only, so the code returns {0,2}. (Rounding at a prefix addition.)
2. One block {0,1}, K = 1, λ = (0, 2⁵⁴), ρ{0} = 1, ρ{1} = 2: 2⁵⁴ ⊕ 1 = 2⁵⁴ ⊕ 2 = 2⁵⁴ (ulp(2⁵⁴) = 4, ties to even), so
   ĝ({0}) = ĝ({1}) = max ĝ; the ĝ-lex choice is {0}; the code returns {1}. (Rounding at the prior addition.)
In both, (iii)–(iv) hold: ĝ(`res.S`) = `res.lg0` = max ĝ and |`res.S`| = kbest. ∎

## Consequence for the e4 fallback (R04 point 2)
In both examples N_ĝ (the number of ĝ-maximisers of size kbest) is 2, the run is **not** truncated, and the output is
still not the ĝ-size-then-lex choice. So a fallback triggered only by `res.truncated` (as the e4 sentence prescribes)
cannot repair the floating-point lexicographic failures; L5's completeness (every maximiser is visited) is an
exact-arithmetic statement and does not transfer to native doubles. A native-double implementation of the prescribed
choice needs its own rounded-feasibility argument (e.g. TDP of L7 with Φ evaluated by the same fold as ĝ, which is not
proved here). Under EX-A the issue does not arise.

## Falsification
`numerics/run_checks.py` family `fp_stress(e only)` (3,000 instances per seed, magnitudes 1 to 2⁵², sub-ulp
perturbations; 429 / 411 instances (seeds 20261108 / 7) with more than one smallest-size ĝ-maximiser — not classified
as rounding-created by the script) and the DATA family (coded scorer, 400 per seed): (iii)–(iv)
held in all; the float lex choice differed from `res.S` in ≈30 fp_stress instances per seed, as (v) allows.

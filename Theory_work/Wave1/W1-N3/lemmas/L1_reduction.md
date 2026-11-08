# L1 — Reduction and order facts

Status: PROVED; cross-family check: R03 CORRECT (Sol). Attempt 2 (2026-11-08) after R02 (attempt 1: GAP — `comp` identity used the
(e)-only inverse-map clause; abstract λ, ρ were identified with the method's prior/scores); re-checked R03: CORRECT.
Notation and hypotheses: `STATEMENT.md` v1.3 §1–§2 (aliases `SoP/`, `CODE/`).

## Statement
(i) For an abstract instance put γ₀(S) := exp f(S) and Z̄₀ := Σ_{S∈Ω_K} γ₀(S), π₀ := γ₀/Z̄₀ on Ω_K. Then log Z̄₀ ∈ ℝ,
log π₀(S) = f(S) − log Z̄₀, and argmax_{Ω_K} π₀ = argmax_{Ω_K} f = 𝒜. In the method specialisation (λ = log ϖ,
ρ_b = log r_b from the scorer) these γ₀, Z̄₀, π₀ are exactly the D0 objects, so the prescribed start mode (smallest
size, then lex_less-smallest maximiser of π₀) is S* of STATEMENT §1.

(ii) For every S ∈ Ω_K, Σ_b ρ_b(S_b) = Σ_{b : S_b ≠ ∅} ρ_b(S_b). If moreover `st.blk`, `st.pos` invert `st.blocks`
(x = `blocks[blk[x]][pos[x]]`, as set by `build_tables`, `CODE/cpp/v3_start.h:79-80`; this is the extra (H1) clause
stated for (e)), then under EX-A `Start::comp(S)` returns this sum and `log_gamma0(S)` returns f(S). Without that clause
`comp` need not compute it (e.g. `blk = [1,0]` on two singleton blocks reads the wrong table). L2–L6 do not use `comp`;
only (e)/L-FP and the interpretation of `log_gamma0` do.

(iii) (Union-order fact.) For distinct X, Y ⊆ {0,…,p−1} with |X| = |Y|, writing sorted(·) for the increasing list:
lex_less(sorted X, sorted Y) ⇔ min(X Δ Y) ∈ X. In particular lex_less is a strict total order on the sets of a fixed size.

(iv) If φ : {0,…,p−1} → ℕ is strictly increasing, then for all X, Y (in particular for equal-size X ≠ Y), lex_less(sorted X, sorted Y) ⇔
lex_less(sorted φ(X), sorted φ(Y)). With φ = internal → original index (`CODE/v3_preprocess.R:112`, `CODE/v3_fit.R:123`),
"lexicographically smallest" is the same on internal and on original indices.

## Proof
(i) Abstract part: Ω_K is finite and nonempty and every f(S) is real, so Z̄₀ is a finite sum of positive reals,
log Z̄₀ ∈ ℝ, and log π₀(S) = f(S) − log Z̄₀; since x ↦ x − log Z̄₀ is strictly increasing, π₀ and f have the same
maximisers and the same tie-breaking (size, then lex_less) is applied to the same set 𝒜.
Method specialisation: by the D0 "Start/bridge" row (`SoP/04_theory.tex:73`), γ₀(S) = ϖ(S) ∏_b r_b(S_b), π₀ = γ₀/Z̄₀ on Ω_K, r_b > 0,
ϖ(S) = w(|S|)/W_K > 0 (`SoP/04_theory.tex:72`). Z̄₀ = Σ_{S∈Ω_K} γ₀(S) is a finite sum of positive reals, so log Z̄₀ ∈ ℝ.
Taking logs, log π₀(S) = log ϖ(|S|) + Σ_b log r_b(S_b) − log Z̄₀ = λ(|S|) + Σ_b ρ_b(S_b) − log Z̄₀ = f(S) − log Z̄₀, with
λ = log ϖ (`CODE/cpp/v3_score.h:69-70`), ρ_b = log r_b = log m(U) − log m(∅) (`CODE/cpp/v3_start.h:95`), and
ρ_b(∅) = log r_b(∅) = 0. (The code states the same identity, paraphrased: `log_pi0(S) = log_gamma0(S) − logZbar0` and
`log_gamma0(S) = logprior[|S|] + comp(S)`, `CODE/cpp/v3_start.h:68-70`.) So the abstract γ₀, Z̄₀, π₀ coincide with D0's.

(ii) ρ_b(∅) = 0, so the terms with S_b = ∅ vanish. Under the inverse-map clause, `comp` (`CODE/cpp/v3_start.h:54-66`) sorts the pairs (blk[x], pos[x])
of x ∈ S, and for each block b met by S ORs 2^{pos[x]} into a code, which by the inverse-map clause equals code(S_b), and adds
`logr[b][code]` = ρ_b(S_b) to s, starting from s = 0. Under EX-A, s = Σ_{b: S_b≠∅} ρ_b(S_b).

(iii) Let t = min(X Δ Y) (exists since X ≠ Y). Every element < t lies in both or in neither set, so sorted X and sorted
Y begin with the same r elements (those < t). Suppose t ∈ X. Then X contains those r elements and t, so
|Y| = |X| ≥ r + 1. Then the (r+1)-th element of
sorted X is t (t is the smallest element of X not < t). Y has |Y| = |X| ≥ r+1 elements, and its (r+1)-th element y is
the smallest element of Y that is not < t; y ≠ t because t ∉ Y; hence y > t. The two lists first differ at position
r+1, with t < y, so lex_less(sorted X, sorted Y) (`std::lexicographical_compare`, `CODE/cpp/v3_util.h:117-119`).
If t ∈ Y the same argument gives lex_less(sorted Y, sorted X), and lex_less is asymmetric. Hence the equivalence.
Totality/transitivity on sets of a fixed size: lexicographic order on sequences of a fixed length over a totally ordered
alphabet is a strict total order.

(iv) φ is a bijection onto its image preserving < ; it maps X Δ Y to φ(X) Δ φ(Y) and min to min. Apply (iii) twice.
(For sets of any sizes: sorted φ(X) is φ applied entrywise to sorted X, φ preserves the outcome of every entry comparison,
and lengths are unchanged, so `std::lexicographical_compare` — including its proper-prefix rule — returns the same
result on (sorted φ(X), sorted φ(Y)) as on (sorted X, sorted Y).)
`kept <- which(!constant)` is increasing (R's `which` returns indices in increasing order) and is passed as `orig`
(1-based original index of internal column a), `CODE/cpp/v3_score.h:18`. ∎

## Falsification
(i)–(ii): `numerics/run_checks.py` DATA family (coded scorer, real prior, 400 instances per seed) compares the frozen
code's (res.S, ties, truncated) with the prediction from the exact-table f built from the code's own tables (no
mismatch), and separately checks the native clause (e) against the Python replica ĝ of `log_gamma0` (0 failures).
(iii): checked exhaustively for p ≤ 8 by `numerics/check_union_order.py` (all pairs of equal-size subsets).

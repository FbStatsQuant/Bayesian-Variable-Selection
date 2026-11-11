# L2 — Lemma NA-F: no-addition on a polylogarithmic lattice in fixed design (bridge (B5)) — NEW

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex gpt-6.1-sol high,
`../reviews/R03_L0L1L2_check_sol.md`): VERIFIED-WITH-AMENDMENTS (1 MINOR: empty family), applied [R03-1]; the entropy
budget h < ½ [P1] was adopted afterwards from R02 and is re-checked in the sweep. Setting F; notation `../STATEMENT.md` §1, §3.1 and GROW
`lemmas/L2_NA_TL.md` §L2.0. This is the fixed-design counterpart of LOC2 Lemma NA-R; it contains GROW L2.3(b)
((G4-dir), `L2_NA_TL.md:51-66`) as the case ρ_n = 0, |Q| ≤ C log n.

## Hypotheses
(F0) Setting F, ‖μ‖² ≤ Mn, p ≤ n^A; deterministic Q ⊇ S₀, q := |Q| ≤ K, q ≤ (log n)^κ; 𝓛 := {T : S₀ ⊆ T ⊆ Q},
𝔓 := {(T, l) : T ∈ 𝓛, l ∈ [p] ∖ T}.
(FL-Q) λ_min(R̂_{Q∪{l}}) ≥ φ₀² for every l ∈ [p].
(N-D)(i) There are a deterministic finite set 𝒰_n of unit vectors of ℝⁿ and a deterministic ρ_n ≥ 0 with
  log|𝒰_n| ≤ log p + h log n for a fixed h ∈ [0, ½)  and  ρ_n²(q + log n)/log n → 0,
such that for every (T, l) ∈ 𝔓 there is v_{T,l} ∈ 𝒰_n ∩ span(X_{Q∪{l}}) with ‖u_{T,l} − v_{T,l}‖ ≤ ρ_n.
[P1] (The locked form "log|𝒰_n| ≤ log p + o(log n)" is the special case of every h > 0. The budget h < ½ is what the
threshold c_n − 2 log p = log n − O(log log n) can pay for; R02 P1.) [R03-1] If 𝔓 = ∅ (i.e. Q = S₀ = [p]) there is
nothing to prove — NA(𝓛) quantifies over no pair — and 𝒰_n may be any deterministic nonempty finite set; below 𝔓 ≠ ∅
and 𝒰_n ≠ ∅.

## Lemma NA-F
Under (F0), (FL-Q), (N-D)(i): with c_n := log(n + 1) + 2 log p − 2 log(q + 1) − 4κ_E − 2 (GROW L2.2),
P(max_{(T,l)∈𝔓} Z²_{T,l} ≤ c_n) → 1 (vacuous if 𝔓 = ∅), and P(NA(𝓛)) → 1.

*Proof.* Step 0 (definitions). For (T, l) ∈ 𝔓, T ∪ {l} ⊆ Q ∪ {l}, so by (FL-Q) and Cauchy interlacing X_{T∪{l}} has
full column rank, (I − P_T)x_l ≠ 0, and u_{T,l}, Z_{T,l} = u_{T,l}ᵀε/σ are defined (GROW L2.0 (F2),
`L2_NA_TL.md:19-22`). u_{T,l} ∈ span(X_{T∪{l}}) ⊆ span(X_{Q∪{l}}).

Step 1 (decomposition). Fix (T, l) ∈ 𝔓, v := v_{T,l}, w := u_{T,l} − v. Both u_{T,l} and v lie in the subspace
V_l := span(X_{Q∪{l}}), hence w ∈ V_l and, with Π_l the orthogonal projector onto V_l,
  u_{T,l}ᵀε = vᵀε + wᵀΠ_lε,  so  |Z_{T,l}| ≤ |vᵀε|/σ + ρ_n‖Π_lε‖/σ.                                      (2.1)
(If l ∈ Q then V_l = span X_Q.)

Step 2 (two events). 𝒰_n is deterministic, so vᵀε/σ ~ N(0, 1) for each v ∈ 𝒰_n. With
a_n² := 2 log(2|𝒰_n|) + 2 log log n:
  P(E₁ᶜ) ≤ |𝒰_n|·2 exp(−a_n²/2) = 1/log n,  E₁ := {max_{v∈𝒰_n}(vᵀε/σ)² ≤ a_n²}.
The projectors Π_l, l ∈ [p], are deterministic of rank d_l ≤ q + 1, and there are at most p distinct ones (all l ∈ Q
give Π_Q; q ≥ s₀ ≥ 1). ‖Π_lε‖²/σ² ~ χ²_{d_l}; by Laurent–Massart, P(χ²_d ≥ d + 2√(dx) + 2x) ≤ e^{−x}, and
d + 2√(dx) + 2x ≤ 2d + 3x. With x := log p + log log n and G_n := 2(q + 1) + 3 log p + 3 log log n:
  P(E₂ᶜ) ≤ p e^{−x} = 1/log n,  E₂ := {max_l ‖Π_lε‖²/σ² ≤ G_n}.

Step 3 (the bound). On E₁ ∩ E₂, by (2.1), for every (T, l) ∈ 𝔓:
  Z²_{T,l} ≤ a_n² + 2a_nρ_n√G_n + ρ_n²G_n.
Here a_n² ≤ 2 log p + 2h log n + 2 log 2 + 2 log log n; G_n ≤ C₂(q + log n) with C₂ = C₂(A); so
ρ_n²G_n = o(log n) by the rate in (N-D)(i), and 2a_nρ_n√G_n = 2√(a_n²·ρ_n²G_n) = 2√(O(log n)·o(log n)) = o(log n)
(a_n² ≤ (2A + 1) log n for n ≥ n₀, because 2h < 1). Hence max_𝔓 Z²_{T,l} ≤ 2 log p + 2h log n + o(log n). Since
c_n = 2 log p + log(n + 1) − 2 log(q + 1) − 4κ_E − 2 ≥ 2 log p + log n − 2κ log log n − O(1) and 2h < 1, the right side
is ≤ c_n for n ≥ n₀ (n₀ depends on the fixed constants, on h and on the rate envelope of ρ_n; it is common to all
pairs). So P(max_𝔓 Z² ≤ c_n) ≥ 1 − 2/log n for n ≥ n₀.

Step 4 (score conversion). By LOC2 `L1_toolkit.md:28-32, 37-42` (Lemma L0′ applied to the lattice family of GROW
L2.0, with q ≤ (log n)^κ, the Gram floor of (FL-Q) and ‖μ‖² ≤ Mn), GROW Lemma L2.2 holds on
𝓔_n ∩ {max_𝔓 Z²_{T,l} ≤ c_n} for n ≥ n₀, and P(𝓔_n) → 1. Hence P(NA(𝓛)) → 1. ∎

**Remarks.** (1) No independence between approximants, or between the Π_lε, is used. (2) The requirement
v_{T,l} ∈ span(X_{Q∪{l}}) is what lets the remainder be charged to a χ² of dimension ≤ q + 1; without it the remainder
would have to be charged to ‖ε‖ ≈ σ√n. (3) The rate ρ_n²(q + log n) = o(log n) reads: ρ_n → 0 when q = O(log n);
ρ_n = o(√(log n/q)) when q ≫ log n.

## Lemma N-loc ⇒ (N-D)(i)
Assume (FL-Q) and: for every l ∈ [p] a deterministic N_l ⊆ Q ∖ {l} with |N_l| ≤ ν_n, where
ν_n log 2 ≤ h log n for a fixed h < ½ (i.e. limsup ν_n/log n < 1/(2 log 2); in particular ν_n = o(log n)) [P1], and a
deterministic ρ_n ≥ 0 with ρ_n²(q + log n)/log n → 0 such that
  ‖(P_T − P_{T∩N_l})x_l‖ ≤ ρ_n‖(I − P_T)x_l‖  for all (T, l) ∈ 𝔓.
Then (N-D)(i) holds with 𝒰_n := {u_{T∩N_l,l} : (T, l) ∈ 𝔓} and the same ρ_n and h (if 𝔓 = ∅ take any
deterministic singleton [R03-1]).

*Proof.* Fix (T, l) ∈ 𝔓, N := T ∩ N_l ⊆ T. Put a := (I − P_T)x_l ≠ 0 and b := (P_T − P_N)x_l. Since N ⊆ T,
P_T − P_N is the orthogonal projector onto span X_T ⊖ span X_N, so b ∈ span X_T and a ⊥ b, and (I − P_N)x_l = a + b,
with ‖a + b‖ ≥ ‖a‖ > 0. So u_{N,l} = (a + b)/‖a + b‖ is defined, and with t := ‖b‖/‖a‖ ≤ ρ_n:
  ‖u_{T,l} − u_{N,l}‖² = 2 − 2⟨a, a + b⟩/(‖a‖‖a + b‖) = 2(1 − (1 + t²)^{−1/2}) ≤ t² ≤ ρ_n²
(because (1 + t²)^{−1/2} ≥ 1 − t²/2). u_{N,l} ∈ span(X_{N∪{l}}) ⊆ span(X_{Q∪{l}}). u_{N,l} depends only on (l, N) with
N ⊆ N_l, so |𝒰_n| ≤ p·2^{ν_n} and log|𝒰_n| ≤ log p + ν_n log 2 ≤ log p + h log n. 𝒰_n is deterministic. ∎

**Special cases.** (a) q ≤ h log n/log 2 with h < ½ (in particular q = o(log n)): N_l := Q ∖ {l}, T ∩ N_l = T,
ρ_n = 0. (So |Q| < 0.72 log n needs no design condition by this route; (N-χ) covers |Q ∖ S₀| ≤ (1 − δ₀) log n.) (b) GROW (G4-dir): 𝒰_n := {u_{T,l}},
ρ_n = 0, |𝒰_n| ≤ pN_n with log N_n = o(log n) — this is (N-D)(i) itself, not (N-loc). (c) If every column outside Q
is orthogonal to span(X_Q) ⊖ span(X_{S₀}) and the columns of Q ∖ S₀ are mutually orthogonal given S₀, then
u_{T,l} = u_{S₀,l} for all T ∈ 𝓛: p directions, ρ_n = 0.

## Relation of (N-D)(i) to (V), (L) [R08-4]
(N-D)(i) is **not established from** (V), (L) and the floors: those conditions constrain the correlation of outside
columns with the *signal*, not with the columns of Q ∖ S₀, and no argument is known that produces a small approximating
family from them. No proof that (N-D)(i) can fail under them is given either (a heuristic design is described in
`../SHARPNESS.md` §4). Whether the *conclusion* needs any such condition is open.

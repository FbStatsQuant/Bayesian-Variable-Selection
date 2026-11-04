# W6-FIXREV2 — corrected, paper-ready statements after A-REV2

Run W6-FIXREV2, 2026-11-02. Notation: `Docs/Theory/theorems/00_COMMON.md`, W1-T03R `PROOF.md`, W1-T37R `PROOF.md`,
W1-EXP `PROOF.md`, W2-PREM `PROOF.md` §2. Every status word is the protocol's. **Every PROVED here is a candidate**:
not reviewed by another family after this run, not adopted. A-REV2 "VERIFIED" is a referee verdict on the source
statement; it is quoted as such and is never converted into a status upgrade.

Source aliases (as in A-REV2): S03 = W1-T03R, V03 = W2-VT03R, S37 = W1-T37R, V37 = W3-VT37R, SEX = W1-EXP,
VEX = W3-VEXP, SU = W2-PREM §2. New items proved in this run are marked **[new]**.

Scripts: `scripts/` (fixed seeds), outputs in `results/`; see REPORT §4.

---

## 1. T03♯ — posterior selection consistency under anchored, size-restricted eigenvalue conditions

### 1.1 Setting and hypotheses

- **R1.** Triangular array, n → ∞; X = X_n fixed (non-random); s₀ ≥ 1 fixed; p = p_n ≤ n^A with A fixed; s₀ ≤ K = min(p, ⌊n/2⌋) for all large n.
- **G.** y^r = α*1 + X^rβ* + ε, ε ~ N_n(0, σ*²I), σ*² > 0 fixed; μ = Xθ*, S₀ = supp β*.
- **R.** ‖μ‖² ≤ Mn and λ_min(R_{S₀}) ≥ φ₀² > 0, with M, φ₀ fixed.
- **Size tail objects (data-free).** q_k := C(p,k)w(k). For every integer m,
  R_m := Σ_{k = max(m+1, 0)}^{K} q_k / w(s₀)  (empty sum = 0; so R_m = 0 for m ≥ K).
  For real ω, m♯_n(ω) := min{m ∈ ℤ : m ≥ s₀, R_m ≤ n^{−(s₀+1)/2}e^{−ω}} (it exists and is ≤ K); m♯_n := m♯_n(½ log n).
  m♯_n is a deterministic function of (n, p, s₀); it is never selected from the response.
- **SE_λ(j₀)** (normalised, anchored, bounded size): j₀ := ⌈(2A+1)s₀⌉ + 1, and λ_min(R_{S₀∪J}) ≥ φ₀² for every
  J ⊆ [p]∖S₀ with |J| ≤ j₀.
- **SE_w(m♯_n; g₀)** (unnormalised, anchored): g₀ > 0 is a **fixed constant** (a sequence g₀,n → 0 is not covered), and
  λ_min(G_{S₀∪J}) ≥ g₀ for every J ⊆ [p]∖S₀ with |J| ≤ m♯_n.
  *Equivalent forms* (V03 Lemma A1, PROVED; interlacing): SE_λ(j₀) ⇔ λ_min(R_T) ≥ φ₀² for every nonempty T with
  |T∖S₀| ≤ j₀; SE_w(m♯_n; g₀) ⇔ λ_min(G_T) ≥ g₀ for every nonempty T with |T∖S₀| ≤ m♯_n. In particular SE_w(m♯_n; g₀)
  forces every m♯_n columns of X to be linearly independent. "Anchoring" is therefore not a restriction to a hand-picked
  list of sets; the substantive savings are the size cutoff m♯_n and the unnormalised constant for large sets.
- **Beta-min** (for (i)–(iii)): **BM-∞**: min_{j∈S₀} θ*_j² ≥ M_nσ*² log n/(nφ₀²) with M_n → ∞; or **BM(c)**: the same with a
  fixed c > c₀(s₀, A) := L_* = max{4C_*, 32[s₀(A+1)+2]} (C_* of the locked T03 proof; a proof artefact, not sharp).

### 1.2 Statements

**Theorem T02(i♯) (exact Beta-Binomial size tail; no eigenvalue condition beyond R).** Status: PROVED (S03 §2);
A-REV2: VERIFIED. Assume G, R, s₀ ≤ K. Define Θ♯_{n,m} ≥ 0 by Π(|S| > m | y) = R_m(n+1)^{s₀/2}√n·Θ♯_{n,m} if R_m > 0, and
Θ♯_{n,m} := 0 if R_m = 0. With c♯ := κ²/(c_IG σ*²) (constants of S03 §2), for every L > (c♯)² and every n,

  sup_m P₀(Θ♯_{n,m} > L) ≤ (8 + 24M/σ*²)/(n − 1) + L^{−1/2} + C_Λ / log(√L/c♯).

The quantifier is sup_m P₀(·), **not** P₀(sup_m ·). Consequently, for every **deterministic** real sequence ω_n,
Π(|S| > m♯_n(ω_n) | y) ≤ (1 + 1/n)^{s₀/2} e^{−ω_n} Θ♯_{n, m♯_n(ω_n)} = O_{P₀}(e^{−ω_n}).

**Theorem T02(ii♯).** Status: PROVED (S03 §5); A-REV2: VERIFIED. Under R1, G, R and SE_w(m♯_n; g₀):
Π(S ⊋ S₀ | y) = O_{P₀}(r_n), r_n = √(log n/n).

**Theorem T03♯.** Status: PROVED (S03 §6; changed steps C1–C10 written in full there); V03 and A-REV2: VERIFIED under exactly
these hypotheses. Assume R1, G, R, SE_λ(j₀) and SE_w(m♯_n; g₀); for (i)–(iii) also BM-∞ or BM(c) with c > c₀(s₀, A).
1. 1 − π(S₀) = O_{P₀}(r_n).
2. For every data set, max_j |PIP_j − 1{j ∈ S₀}| ≤ 1 − π(S₀); hence P₀(MPM = S₀) → 1.
3. P₀(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] → 0, where S† is the global HPM. (Only convergence is claimed: boundedness of 1 − π(S₀)
   turns convergence in probability into convergence of the expectation, not into an O(r_n) bound on it.) On the event
   {π(S₀) > ½}, S₀ is the strict global maximiser of F, so no tie rule is used.
4. (No beta-min.) For fixed c > c₀(s₀, A) let J_n(c) := {j ∈ S₀ : θ*_j² ≥ cσ*² log n/(nφ₀²)}. Then
   Π(S ⊉ J_n(c) | y) = O_{P₀}(r_n) and 1 − min_{j∈J_n(c)} PIP_j = O_{P₀}(r_n), with the convention min_∅ := 1 (the claim is
   vacuous when J_n(c) = ∅). The same holds for J_n^∞ = {j : θ*_j² ≥ M_nσ*² log n/(nφ₀²)} with any M_n → ∞.
5. Scale invariance as in the locked T03.

**Scope (must accompany the theorem).**
- This is posterior / global-HPM theory. It says nothing about the reported HPM Ŝ (discovery by the sampler).
- Prop. E3 (S03, PROVED): for this route — a Markov numerator over an S₀-denominator with the exact-tail cutoff — the
  cutoff cannot be s₀ + O(s₀ log n/log p). It is a barrier for this proof route only, not a lower bound for the posterior.
- Prop. D (S03, COUNTEREXAMPLE): under G and R alone (duplicate columns), Π(|S| > m | y) ≥ 2^{−(m+4)}e^{−m(m−1)/(4(p−m))}
  on an event of probability → 1, so some growth m_n ≳ ½ log₂ n is needed in general. It violates size-2 SE and does not
  contradict T03♯ (under T03♯, Π(|S| > s₀ | y) ≤ 1 − π(S₀) = O_P(r_n), V03 Prop. D′).
- **Finite-n disclosure (corrected; replaces S03's "≈ 1.2·10⁵").** With s₀ = 14, p = round(n^A), 1/g₀ → 0 (most
  favourable) and exact m♯_n, the proof as written needs δ_n ≤ ½ (first n = 115,150 / 130,328 for A = log 500/log 200 /
  log 1000/log 200), the geometric-series condition q_n ≤ ½ (first n = **2,116,048 / 2,457,025**), and, only to fix the
  displayed constant c_q, e^{2ε_n} ≤ 4 (first n = 25,571,897 / 29,755,302). At S03's n = 130,328, q_n ≈ 5.53·10²² (A = 1.17)
  and 7.86·10²⁸ (A = 1.30). These are checks of named conditions, **not a universal n₀**: other thresholds involve the signal,
  variance and eigenvalue constants and the BM sequence. At (n, p) = (200, 500) and (200, 1000), m♯_n = K = 100 (the cap
  binds; uncapped m♯_n would be 146 and 168, locked m_n = 201 and 215); the cap removes the dimension-tail term there but
  does not verify SE_λ, SE_w or BM, and the O_P rate is not numerically informative.
  Replacement sentence for the disclosure: "…and the proof's own deterministic thresholds (as written) hold only from
  n ≈ 2×10⁶ (p = n^{1.17}) to 2.5×10⁶ (p = n^{1.30}); the O_P constants are unspecified."
  (Independent recomputation: `scripts/t03_thresholds.py`, `results/t03_thresholds.txt`; it agrees with V03 R1 and A-REV2 §3.5
  to the integer.)

---

## 2. Theorem A — refined T37(i): deterministic greedy repair, exact-ties-aware

### 2.1 Setting and definitions

EX-A; X, y fixed (no probability in §2.1–2.4). S₀ ∈ Ω. N(S) := the feasible flips and swaps of S (additions only if
|S| < K). ≺ is the engine's tie order `lex_less` on sorted index vectors (element-wise, proper prefix first;
`v3_engine.h::local_search`). For S with N(S) ≠ ∅:

- best(S) := the ≺-least element of argmax_{T ∈ N(S)} F(T);
- **M(S)** := best(S) if F(best(S)) > F(S), and M(S) := ⊥ otherwise. (This is exactly the engine: the scan keeps the
  maximum with ≺ tie-break over all neighbours, then moves only on strict improvement.)

m(S) = |S₀∖S|, e(S) = |S∖S₀|, Φ(S) = |S Δ S₀|; 𝒫(S) := {T ∈ N(S) : Φ(T) < Φ(S)} (add a truth, delete an extra,
swap extra→truth); the other neighbours are neutral or regressive. R_{a,d} := {U ∪ P : U ⊆ S₀, |S₀∖U| ≤ a, P ⊆ S₀ᶜ,
|P| ≤ d, |U ∪ P| ≤ K}; Lat(S) := {U′ ∪ P′ : U ⊆ U′ ⊆ S₀, P′ ⊆ P} for S = U ∪ P.

- **(L)**: M(S₀) = ⊥.
- **TD′_∞(𝓡)**: (L), and for every S ∈ 𝓡∖{S₀}: M(S) ≠ ⊥ and M(S) ∈ 𝓡.
- **TD′_P(𝓡)**: (L), and for every S ∈ 𝓡∖{S₀}: M(S) ≠ ⊥ and M(S) ∈ 𝒫(S). (Defined through M; this is S37's definition.)
- **D_S^lex** [A-REV2's repair]: best(S) ∈ 𝒫(S) and F(best(S)) > F(S).
- **D_S** (strict, S37): 𝒫(S) ≠ ∅ and max_{T∈𝒫(S)} F(T) > max{F(S), max_{T ∈ N(S)∖𝒫(S)} F(T)} (max ∅ := −∞).

### 2.2 The tie lemma (replaces S37's "TD′_P ⟺ (L) ∧ ⋂ D_S")

**Lemma T.** Status: PROVED [new write-up of A-REV2 §4.3].
(a) D_S^lex ⟺ [M(S) ≠ ⊥ and M(S) ∈ 𝒫(S)]. Hence TD′_P(𝓡) ⟺ (L) ∧ ⋂_{S∈𝓡∖S₀} D_S^lex, **exactly**, with ties.
(b) D_S ⇒ D_S^lex.
(c) If D_S^lex holds and D_S fails, there is an exact top tie between a progress and a non-progress neighbour:
    max_{𝒫(S)} F = max_{N(S)∖𝒫(S)} F = max_{N(S)} F > F(S).
(d) The converse of (b) is false: n = 100, p = 2, x₁ = x₂, S₀ = {1}, y^r = 0.5x₁ + e with e ⟂ x₁, ‖e‖² = 99. TD′_P(R₀) holds
    (M(∅) = {1}, M({1}) = ⊥), while D_∅ fails because F({1}) = F({2}) exactly. Gains: ∅ → {1}: 7.6308489425; adding the
    duplicate at the truth: −0.0018640607 (`results/t37_checks.txt`, identical to A-REV2).

*Proof.* (a) If D_S^lex holds, best(S) strictly improves, so M(S) = best(S) ∈ 𝒫(S). Conversely M(S) ≠ ⊥ means M(S) = best(S)
and F(best(S)) > F(S). (b) Under D_S every maximiser of F over N(S) lies in 𝒫(S) (non-progress values are strictly
smaller), so best(S) ∈ 𝒫(S), and F(best(S)) = max_{𝒫(S)} F > F(S). (c) D_S^lex gives max_{N(S)} F = F(best(S)) =
max_{𝒫(S)} F > F(S); failure of D_S then forces max_{N(S)∖𝒫(S)} F ≥ max_{𝒫(S)} F, hence equality. (d) Computation. ∎

**Lemma NT (exact ties are null events when the compared sets are jointly non-degenerate).** Status: PROVED [new].
Assume G and n ≥ 3. Let T′ ≠ T″ ∈ Ω with |T′| + |T″| < n − 1 and λ_min(G_{T′∪T″}) > 0. Then P₀(F(T′) = F(T″)) = 0.

*Proof.* Write y = √(n−1)·Cy^r/‖Cy^r‖ and A_T := X_T H_T^{−1} X_Tᵀ, so F(T) = c_T − ν log(0.02 + (n−1) − n yᵀA_T y) with
c_T = log w(|T|) − ½ log D_T (+ a common constant). On the open connected set {Cy^r ≠ 0} (n − 1 ≥ 2) the difference
F(T′) − F(T″) is real-analytic in y^r; y^r has a Lebesgue density under G; so its zero set is null unless the
difference vanishes identically. Suppose it does. As y^r ranges over {Cy^r ≠ 0}, y ranges over the whole sphere of
radius √(n−1) in range(C). With k := e^{(c_{T′} − c_{T″})/ν}, identity of the scores gives, for all such y,
n yᵀ(A_{T′} − kA_{T″})y = (n − 0.98)(1 − k). A quadratic form constant on the sphere of the (n−1)-dimensional space
range(C) is a multiple of the identity there: A_{T′} − kA_{T″} = αP_C with α = (n − 0.98)(1 − k)/(n(n − 1)). The left
side has rank ≤ |T′| + |T″| < n − 1, so α = 0, hence k = 1 and A_{T′} = A_{T″}. Then col X_{T′} = col A_{T′} =
col A_{T″} = col X_{T″}, so rank X_{T′∪T″} = rank X_{T′} ≤ |T′| < |T′ ∪ T″| (because T′ ≠ T″ and, if T′ ⊂ T″,
|T″| > |T′|; symmetrically). This contradicts λ_min(G_{T′∪T″}) > 0. ∎

**Corollary NT.** If every union of two members of N(S) ∪ {S} has λ_min(G) > 0 and 2|S| + 2 < n − 1, then under G,
P₀-a.s. D_S ⟺ D_S^lex. So S37's equivalence "TD′_P(𝓡) ⟺ (L) ∧ ⋂ D_S" holds **almost surely** under such
non-degeneracy (finitely many comparisons), but **not deterministically** (Lemma T(d)); A-REV2's counterexample uses a
duplicate column, which violates the non-degeneracy. Status: PROVED (finite union of null sets).

### 2.3 Theorem A

**Theorem A (refined T37(i)).** Status: PROVED (S37 §Theorem A for A1–A4; V37 R1 for the POS repair; tie-aware
reformulation and the quantifier corrections here). A-REV2: A1–A4 and POS-repaired A5 VERIFIED; original A5(a) ERROR.

- **(A1) Characterisation.** For a finite family 𝓡 ∋ S₀: TD′_∞(𝓡) holds iff for every S ∈ 𝓡 the uncapped greedy path
  S, M(S), M(M(S)), … stays in 𝓡 and terminates at S₀. Then the path from S has at most
  r_𝓡(S) := #{S′ ∈ 𝓡 : F(S′) > F(S)} moves.
- **(A2) Progress paths.** If TD′_P(R_{a,d}) holds, then from every S ∈ R_{a,d} the greedy path stays in Lat(S) ⊆ R_{a,d},
  Φ strictly decreases at each move, and S₀ is reached after exactly τ(S) = m(S) + e(S) − σ(S) moves, where σ(S) is the
  number of extra→truth swaps used; max{m(S), e(S)} ≤ τ(S) ≤ Φ(S).
- **(A3) Production search.** If TD′_P(R_{a,d}) holds and S_c ∈ R_{a,d}, the production local search from S_c returns S₀
  with `local_certified` (and without `local_limit`) **iff ℓ ≥ τ(S_c)**; ℓ ≥ a + d suffices. If it does, Ŝ = S₀ after the
  search up to exact HPM ties (Lemma 0(c)); no π(S₀) > ½ premise is needed. *Lattice version:* the same holds for one
  centre S_c under (L) ∧ ⋂_{S ∈ Lat(S_c)∖S₀} D_S^lex (2^{Φ(S_c)} states), and a fortiori under (L) ∧ ⋂ D_S (strict).
- **(A4) Necessity (quantifiers as stated).**
  (i) If the greedy path from **every** S ∈ 𝓡 terminates at S₀, then F(S₀) > F(S) for all S ∈ 𝓡∖{S₀} (posterior score
  dominance PD(𝓡)), and TD′_∞(𝓡) holds when the paths also stay in 𝓡.
  (ii) If the path from **one** centre S_c terminates at S₀, then F(S₀) > F(S) only for the states S ≠ S₀ on that path.
  (iii) If every greedy path from 𝓡 terminates at S₀ and decreases Φ at **every** move, then TD′_P(𝓡) holds.
- **(A5, repaired) Relation to literal TD.** Let POS(R_d) be: at every S ∈ R_d∖{S₀}, the move designated by literal TD (the
  best missing-truth addition if S ⊉ S₀, the designated extra deletion if S ⊋ S₀) has strictly positive gain. Then
  literal strict TD(d, 0) ∧ POS(R_d) ⇒ TD′_P(R_d). For d ≥ 1 the literal premise is never satisfied (S37 Prop. 1); at
  d = 0 it is satisfiable. **Without POS the implication is false** (CEX-1 below), so the original T37(i) is false at d = 0
  too. TD′_P(𝓡) ⇒ TD′_∞(𝓡) for progress-closed 𝓡; the converse fails (combination proxy, S37 Exp 3; A-REV2 §4.1).

*Proof of the changed parts.* (A3) "iff": under TD′_P every state of the path other than S₀ has M ≠ ⊥ (Lemma T(a)); the
engine moves while the count is < ℓ and then scans once more. If τ(S_c) ≤ ℓ the centre is S₀ after τ moves and the next
scan finds no strict improvement by (L): `local_certified`. If τ(S_c) > ℓ, the centre after ℓ moves is a state ≠ S₀ with
M ≠ ⊥, so the extra scan finds a strict improvement: `local_limit`. Lattice version: Lat(S_c) is closed under progress
moves (S37 Lemma 2(a)), and D_S^lex on Lat(S_c)∖S₀ gives M(S) ∈ 𝒫(S) ∩ Lat(S_c) there (Lemma T(a)); strict D_S implies
D_S^lex (Lemma T(b)). (A4)(iii): for S ∈ 𝓡∖{S₀} the path ends at S₀ ≠ S, so M(S) ≠ ⊥, and its first move decreases Φ,
i.e. M(S) ∈ 𝒫(S); the path from S₀ ends at S₀ and F strictly increases along paths, so it is trivial: M(S₀) = ⊥. (A4)(ii):
Lemma 0(a) along the one path; a state off the path is not compared. (A5): literal strict TD makes the designated move the
unique maximiser of F over N(S) (strict inequality against every other move), so best(S) is that move; POS makes it
strictly improving; it is a progress move; the S₀-clause gives (L). Other parts: S37 PROOF.md, verbatim. ∎

### 2.4 Lemma 0 and the failure partition (replaces S37 Lemma 0(b) and V37 R2)

Notation: 𝒮_pre is the scored set before the final local search; S_c := HPM(𝒮_pre) (the HPM tie rule: max F, then
smallest size, then lexicographic); F_pre := F(S_c) = max_{𝒮_pre} F. The search scores 𝒮_LS; 𝒮_post := 𝒮_pre ∪ 𝒮_LS;
F_post := max_{𝒮_post} F; Ŝ := HPM(𝒮_post). (The final local search is the last scoring event of a fit.) F_post may be
attained at the neighbour returned with `local_limit`, which is scanned but whose own neighbourhood is not.

**Lemma 0 (corrected).** Status: PROVED ((a), (c): S37, VERIFIED by V37 and A-REV2; (b′): this write-up).
(a) Along the search path S_c = S⁰, S¹, …, F strictly increases.
(b′) *Delivery inclusion.* {Ŝ = S₀} ⊆ {S₀ ∈ 𝒮_pre} ∪ {F(S₀) > F_pre} ∪ {F(S₀) = F_pre and S₀ wins the HPM tie rule}.
In particular a **new** delivery (S₀ ∉ 𝒮_pre) with no exact tie requires E_LS := {S₀ ∉ 𝒮_pre, F(S₀) > F_pre}.
If S_c = S₀ no new delivery is needed, but the fit is **not** automatically a success: the search from S₀ certifies S₀
iff M(S₀) = ⊥; if M(S₀) ≠ ⊥ it moves to a strictly better model and Ŝ ≠ S₀ (e.g. the CEX-2 design, where
F(S₀ + x₃) − F(S₀) = 7.21).
(c) If the search ends `local_certified` with returned centre S₀, then every model in 𝒮_post has F ≤ F(S₀), and Ŝ = S₀
unless another model has exactly the same score and wins the HPM tie rule. No π(S₀) > ½ premise is used.

*Proof of (b′).* Ŝ = S₀ forces S₀ ∈ 𝒮_post and F(S₀) = F_post ≥ F_pre. If S₀ ∉ 𝒮_pre, either F(S₀) > F_pre, or
F(S₀) = F_pre, in which case S₀ beats S_c only through the tie rule. For S_c = S₀: Lemma 0(a) and the definition of M. ∎

**Proposition F (exhaustive failure partition).** Status: PROVED (immediate; the categories are A-REV2 §4.2's).
Every fit with Ŝ ≠ S₀ lies in exactly one of
- **I** — F_pre ≥ F(S₀). This is exactly E_LSᶜ (S₀ ∈ 𝒮_pre implies F_pre ≥ F(S₀)). The search cannot deliver S₀
  except through an exact tie.
- **II** — F_pre < F(S₀) and F_post < F(S₀). S₀ ∉ 𝒮_post (a *search miss*). Sub-cases: **IIa** the search ended
  `local_certified` at an inferior local maximum; **IIb** it ended `local_limit` (move cap).
- **III** — F_pre < F(S₀) ≤ F_post. An explored competitor scores at least F(S₀) (strictly: a posterior miss among the
  explored models; with equality: an HPM tie lost).
A fit is a *posterior miss* (F(Ŝ) ≥ F(S₀)) iff it is in I ∪ III, and a *search miss* iff it is in II.

*Proof.* Since F_post ≥ F_pre, the three conditions on (F_pre, F_post) relative to F(S₀) partition all fits; I = E_LSᶜ
because S₀ ∈ 𝒮_pre implies F_pre ≥ F(S₀), and S₀ ∉ 𝒮_pre with F_pre < F(S₀) is E_LS. In II, S₀ ∈ 𝒮_post would give
F_post ≥ F(S₀). The search ends either certified or at the cap. F(Ŝ) = F_post. ∎

What this replaces. S37's "(b) … in particular on every posterior miss F(S₀) ≤ F(Ŝ) no local search delivers S₀" is
false as an inference (CEX-2 is in III). V37 R2's two-way split "E_LSᶜ, or E_LS with the search ending at S* with
F(S*) ≥ F(S₀)" omits II (CEX-1 from the empty centre is IIa: E_LS true, certified at ∅, F_post − F(S₀) = −20.99). Both
are now special cases of Proposition F.

**Data reading (not a theorem).** THEORY_PRIORITIES §5 / F-REFINE report that all 565 completed wrong HPMs in the p ≫ n
study are posterior misses (0 search misses). If that classification used F(Ŝ) ≥ F(S₀) on the final ledger, then
category II is empty on that data and every miss is in I ∪ III. The split I vs III (whether "0/541 repairs" is forced by
monotonicity) still needs F_pre per fit: **OPEN** (one ledger extraction). The engine already records it:
`v3_core.cpp` stores `hpm_before = (led.hpmS, led.hpmF)` immediately before `E.local_search(led.hpmS, …)`, which is the
last scoring call of a completed fit (read 2026-11-02). So the split needs only `hpm_before$F` and one extra score F(S₀)
per failed fit.

### 2.5 Corrected prose (replaces S37's "What is weakest")

- TD′_∞(𝓡) is necessary and sufficient for: "from every centre in 𝓡 the uncapped greedy path stays in 𝓡 and ends at S₀" (A1).
- For a progress-closed 𝓡 (such as R_{a,d}), TD′_P(𝓡) is necessary and sufficient for: "every greedy move from 𝓡 decreases
  Φ and every path ends at S₀" (A2, A4(iii)).
- For "every path from 𝓡 reaches S₀ within Φ(S) moves" (PHI-REACH), TD′_P is sufficient but **not necessary**: a neutral
  move can be paid back by an extra→truth swap (ΔΦ = −2). Examples: V37 R3 (path {5,6,12} → {2,5,12} → {2,5,13} →
  {2,6,13}, Φ = 4, 3 moves) and an independent one here (`results/t37_extra.txt`: S₀ = {0,1,2}, path {2,5} → {1,5} →
  {0,1,5} → {0,1,2}, Φ along the path 3, 3, 2, 0).
- The lattice condition of (A3) is a sufficient condition for one centre that does not require simulating the path. No
  class of certificates has been defined in which a minimality ("weakest") theorem was proved; do not use the word.
- "ℓ ≥ a + d" is sufficient; the exact requirement under TD′_P is ℓ ≥ τ(S_c), with max(m, e) ≤ τ ≤ Φ.

### 2.6 Theorems B and C (status unchanged; two corrections carried)

- **Theorem B** (S37; A-REV2: inclusions VERIFIED). The union bound must run over a **data-independent** family
  Lat(𝒞), 𝒞 ⊆ R_{a,d}. For the production centre (the running HPM, response-selected) the count 2^{Φ(S_c)} is not
  available; for 𝒞 = R_{a,d}, |{S ∈ R_{a,d} : m(S) ≥ 1}| = Σ_{i=1}^{a} C(s₀,i) Σ_{e≤d} C(p−s₀,e). The deterministic lattice
  implication itself remains usable after selection. Strict D_S events in (B1)–(B2) are sufficient events; replacing them
  by D_S^lex keeps the inclusion valid.
- **Theorem C** stays PROOF SKETCH (C1–C2), COUNTEREXAMPLE (C3), CONJECTURE (C4). In V37 R4, after writing t² = 2 log p + u²,
  the bound is p·P(|Z| ≥ t) ≲ e^{−u²/2}; the printed p·P(|Z| ≥ u) is wrong (with t² ≈ 3 log n, p = n it grows like
  √(n/log n)). Put the original threshold t, not the excess u, in the Gaussian tail.

### 2.7 Counterexamples used (reproduced independently in this run)

| Name | Design | Shows | Numbers (`results/t37_checks.txt`, `t37_extra.txt`) |
|---|---|---|---|
| CEX-1 | n=100, p=12, corr(x₁,x₂)=.95, μ = 3x₁ − 2.8x₂, 10 orthogonal nulls, noise ⟂ columns, ‖e‖²=99 | A5 false without POS; Prop. F category IIa | literal TD(0,0) strict: 0 failing clauses; best gain at ∅ −2.2977998984; F(S₀)−F(∅) = 20.9899772288; π(S₀) = 0.8645494125; search from ∅ certifies ∅ |
| CEX-2 | V37's construction, rebuilt | posterior miss with E_LS true (category III) | F(S_c)−F(S₀) = −2.2862503005; F(S₀+x₃)−F(S₀) = 7.2109846558; path S_c → S₀+x₃, certified |
| TIE | x₁ = x₂, see Lemma T(d) | S37 "iff" false deterministically | as Lemma T(d) |
| VAR | A-REV2's p = 20, B = 4 suppressor-hub variant, exact Gram, noise ⟂ columns (my choice of noise) | category II with the **production start**: blocks = groups, every nonempty table model below ∅, start mode argmax π₀ = ∅, all flips at ∅ non-improving, F({x₀,x₄}) − F(∅) = 19.92; search certifies ∅ | max table-model gain over ∅ = −2.83 |

---

## 3. EXP′ and the chain laws (fixed design, deterministic blocks / chains)

### 3.1 Theorem 1 (EXP′)

Status: PROVED (SEX §1); A-REV2: exact remainder and stated bound VERIFIED; displayed limiting constant ERROR (corrected here).

**Hypotheses.** G (fixed X); **R-lite(A, M)**: p ≤ n^A, ‖μ‖² ≤ Mn; blocks C_b deterministic in X with |C_b| ≤ B ≤ 16;
**SE-blk(φ₀)**: λ_min(R_U) ≥ φ₀² for every nonempty U ⊆ C_b and every b (equivalently, by interlacing,
min_b λ_min(R_{C_b}) ≥ φ₀²). Not used: cross-block structure (BO), beta-min, VIS, NL, λ_min(R_{S₀}).

**Conclusion.** Let c_* := σ²/(8(M + 2σ²)) and

  κ_EXP(n) := (1 + φ₀^{−2})/(2φ₀²(n−1)) + (n/2 + 0.01)(1.02 + 1/(nφ₀²))/(c_* n).

On an event E_n with P₀(E_n) → 1 (uniformly over fixed designs with the same (A, M, σ², φ₀)), every within-block
addition (b, T, l) satisfies

  log[r_b(T+l)/r_b(T)] = −½ log(n+1) − ν log(1 − x_{T,l}) + R_{n,b,T,l},   |R_{n,b,T,l}| ≤ κ_EXP(n).

**Corrected constant.** κ_EXP(n) decreases strictly to **0.51/c_* = 4.08(M + 2σ²)/σ²** (not 0.52/c_* = 4.16(M+2σ²)/σ²),
from above: κ_EXP(n) > 0.51/c_* for every n. The bound κ_EXP(n) ≤ 0.52/c_* holds for all n ≥ n₁(φ₀, c_*) (e.g. n ≥ 56
when σ² = M = φ₀² = 1, where the limit is 12.24, not 12.48). Under the weaker λ_min ≥ φ_n² with n^{1/2}φ_n² → ∞,
|R| ≤ 0.51/c_* + o(1). (`results/lemmaU_checks.txt`, `check_kappa`.)

**Corollary R1 (data-computable certificate; VEX R1).** Status: PROVED; A-REV2: VERIFIED. For any data set and any
partition with min_b λ_min(R_{C_b}) ≥ φ² > 0 and y ∉ span X_{C_b} for every b, every within-block addition satisfies
|R| ≤ (1 + φ^{−2})/(2φ²(n−1)) + ν(1.02 + 1/(nφ²))/min_b RSS^y_{C_b}. Deterministic; no probability event is needed. The
asymptotic κ_EXP does not prove that a given n = 200 data set lies on E_n; the certificate is the finite-n statement.

### 3.2 Theorem 3 (two-sided ratio law along a deterministic chain)

Status: PROVED (SEX §3); A-REV2: VERIFIED with the deterministic chain retained.

**Hypotheses.** G, R-lite(A, M); **H1-det**: a chain S^{(0)} ⊂ … ⊂ S^{(c)} = S₀, S^{(i+1)} = S^{(i)} + l_i, that is
**deterministic** (X-measurable, chosen without the response; an independently chosen chain with uniform conditions is
also admissible), fixed s = |S^{(0)}|, fixed c ≥ 1, all sets feasible; T_i := S^{(i)} ∩ C_{b(l_i)}; **SE-chain(φ₀)**:
λ_min(R_{T_i+l_i}) ≥ φ₀² (i < c); **CL(L_n)**: max_i |δ_{T_i,l_i}| ≤ L_nσ.

**Conclusion.** On an event of probability → 1, for all i < c and n ≥ 400 (n ≥ 103 suffices for the 1.01):
−1 − κ_EXP(n) ≤ E_{n,i} := log[r_{b_i}(T_i+l_i)/r_{b_i}(T_i)] + ½ log n ≤ κ_EXP(n) + 1.01(L_n + |Z_i|)², with
Z_i = Z_{T_i,l_i} exactly N(0,1). With fixed L, max_i |E_{n,i}| = O_{P₀}(1) (this is H2). For growing L_n the upper side
is O_P(1) + 1.01(L_n + O_P(1))² and the lower side stays −O_P(1).
**Quantifier boundary.** Locked T27(i) allows a data-measurable chain but **assumes** H2 for it; Theorem 3 discharges H2
only for H1-det. Do not apply it to a response-selected trajectory without a separate uniform bound.

### 3.3 Theorem 4 (T27(i) mass law from bounded chain leakage)

Status: PROVED given H3 (SEX §3); PROOF SKETCH when H3 is discharged through reference transfer (SEX Prop. 2.2). A-REV2:
VERIFIED with fixed-length deterministic chain, fixed CL(L) and normalised H3 explicitly retained.

**Hypotheses.** Those of Theorem 3 with L_n = L fixed; **H3** (normalised start mass at the chain's base):
P₀(π₀(S^{(0)}) ≥ c₀) → 1 for a fixed c₀ > 0 (π₀ is the normalised, capped start law); p ≥ 2(s + c).

**Conclusion.** log π₀(S₀) + c log p + (c/2) log n = O_{P₀}(1); i.e. π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (both directions
tight). No independence between chain remainders is used.

**Growing leakage (sufficiency only; replaces the "iff" and VEX R4's "whatever η").** Under CL(L_n) with L_n² ≤ η log n,
  log π₀(S₀) ≤ −c log p − c(½ − 1.01η) log n + O_P(√(log n)).
Hence π₀(S₀) → 0 in probability if η < 1/2.02 (any p), or, when p ≥ n^a, if a + ½ − 1.01η > 0. This is an upper envelope:
it gives no necessary threshold, and p^{−c} alone does not force π₀(S₀) → 0 for large η, because the factor
e^{1.01c(L_n+O_P(1))²} is an upper bound only. (A-REV2 §5.3: a masked sequence with exact zero leakage satisfies
CL(√(log n)) with η = 1 and CL(0) simultaneously.)

**Optional limit law.** PROOF SKETCH (unchanged). If stated as convergence to one law, also assume convergence of the
signal variance v; otherwise use subsequences. Fixed-p and p → ∞ prior constants differ (VEX R4).

### 3.4 Random designs and random partitions (status kept)

- SEX §1.5 (random X ⇒ SE-blk w.p. → 1): PROOF SKETCH; the "κ₁₇ ≥ 0.15 for all six study covariances" is false for
  S6 (0.1; VEX R4).
- SEX §4.3: the claim that δ_{∅,j_b} is exactly N(0, ‖μ‖²/(n−1)) given μ is false (after normalisation the column
  direction is spherical, not Gaussian). What is needed, δ = O_P(1), follows from its conditional second moment.
- VEX R3 (LH-iid, g ≤ B < 2g, fixed-partition surrogate): PROOF SKETCH; sound in that regime (the surrogate is defined
  before X is observed; the unconditional Beta law is used before intersecting the partition event).
- B ≥ 2g (group packing depends on the predictor directions used in the statistic): **GAP**, not a consequence of
  Theorem 1.

---

## 4. Lemma U — one uniform log-BF expansion on an explicitly budgeted family

Status: PROVED (SU §2 proof, restated with the corrected quantifiers and corollaries) [the budgeted statement and
C3-low′ are new]. A-REV2: (U) and its events VERIFIED on an explicitly budgeted family; the extra-family wording GAP;
C3 upper bound VERIFIED; C3 matching lower bound under δ = 0 alone ERROR.

### 4.1 Statement

**Lemma U(𝔉, 𝓗).** Fix k ≥ 1. Let
- 𝔉 be a family of pairs (T, l), l ∉ T, |T + l| ≤ k, determined by X (fixed design: deterministic);
- 𝓗 be a family of nonempty sets V with |V| ≤ k, determined by X, that contains every nonempty T and T + l with
  (T, l) ∈ 𝔉 **and every further set at which (E1) or (E2) below is invoked**, with **budget** |𝓗| ≤ C_H n^{a_H}
  (C_H, a_H fixed).

Assume G with μ = Xθ* ∈ span X_{S₀}, s₀ fixed; R-lite(A, M); and λ_min(R_V) ≥ φ₀² for every nonempty
V ∈ {T, T + l : (T, l) ∈ 𝔉} (no eigenvalue condition on the other sets of 𝓗 or on any V ∪ S₀). Fix L > 4a_H. Put
C_R := 2M + 4σ², c_E := σ²/(8(M + 2σ²)), ϑ_n := n^{−1/3} + L log n/(n−1), ϑ′_n := L log n·(ϑ_n + 3/n)/(1 − ϑ_n), and

  κ_n := (1 + φ₀^{−2})/(2φ₀²(n−1)) + ν(1.02 + 1/(nφ₀²))/(c_E n)   (↓ 0.51/c_E = 4.08(M + 2σ²)/σ²).

Then there is an event E_n = E_n(𝔉, 𝓗) with P₀(E_n) ≥ 1 − (C_H + 1)(2^{k/2} + 2^{(k+s₀)/2}) n^{a_H − L/4} − 2n^{2/3}/(n − 1)
→ 0 on which:

- **(U)** for every (T, l) ∈ 𝔉: log[BF(T+l)/BF(T)] = −½ log(n+1) − ν log(1 − x_{T,l}) + R_{T,l}, |R_{T,l}| ≤ κ_n, with
  x_{T,l} = (RSS_T − RSS_{T+l})/RSS_T = (δ_{T,l} + σZ_{T,l})²/RSS_T;
- **(E1)** ‖P_Vε‖² ≤ Lσ² log n for every V ∈ 𝓗; hence Z²_{T,l} ≤ L log n for every (T, l) ∈ 𝔉 (u_{T,l} ∈ span X_{T+l});
- **(E2)** RSS_V ≥ ‖(I − P_{V∪S₀})Cε‖² ≥ σ²(n−1)(1 − ϑ_n) for every V ∈ 𝓗 ∪ {∅};
- **(E3)** σ²(n−1)(1 − n^{−1/3}) ≤ ‖Cε‖² ≤ σ²(n−1)(1 + n^{−1/3});
- **(E4)** ‖Y‖² ≤ C_R n.

**Instances.** (i) **EXP′**: 𝔉_blk = {(T, l) : T + l ⊆ C_b for some b}, 𝓗_blk = {nonempty U ⊆ C_b}, |𝓗_blk| ≤ 2^{16} n^A
(a_H = A), SE = SE-blk; r_b(U) = BF(U) for U ⊆ C_b. (ii) **All small sets**: 𝔉_k = {(T, l) : |T + l| ≤ k},
𝓗_k = {V : 1 ≤ |V| ≤ k}, |𝓗_k| ≤ Σ_{j≤k} C(p, j) ≤ k n^{kA} (a_H = kA, e.g. L = 4kA + 1), SE(k). For 𝔉_k the extra
quantifier is vacuous: every set of size ≤ k is already in 𝓗_k. So **every W2-PREM §3 use (k = s₀ + a + 2, all sets of
size ≤ k) is covered as written**; the GAP concerns only the general statement.

**Why the budget is necessary (A-REV2 §6.2; reproduced).** p = n − 1 orthogonal columns, k = 1, 𝔉 = {(∅, 2)}, a_H = 0.1,
L = 0.5 > 4a_H for the original pair family; if (E1) were also asserted for all singletons, their projected noise energies
are independent χ²₁ with maximum ≈ 2 log n > 0.5 log n. In simulation the event fails in 100% of draws at
n = 10³ … 10⁶ (`results/lemmaU_checks.txt`, `quantifier_cex`).

*Proof.* Lemmas 1.1–1.3 of SEX are deterministic and use only λ_min(G_{T+l}) ≥ φ₀²(n−1) (and, by interlacing, for T);
they give |R_{T,l}| ≤ (1 + φ₀^{−2})/(2φ₀²(n−1)) + ν(1.02 + 1/(nφ₀²))/min_{U∈{T,T+l}} RSS^y_U (exact decomposition
re-checked: max error 2.1·10⁻¹³ over 9,280 pairs, `remainder_identity`). Probability: for V ∈ 𝓗,
‖P_Vε‖²/σ² ~ χ²_r with r ≤ k and E exp(χ²_r/4) = 2^{r/2}, so Markov and a union bound give P(max_{V∈𝓗} ‖P_Vε‖² > Lσ² log n)
≤ C_H n^{a_H} 2^{k/2} n^{−L/4}: (E1). The same with rank ≤ k + s₀ for the (|𝓗| + 1) spaces span X_{V∪S₀} gives
max ‖P_{V∪S₀}ε‖² ≤ Lσ² log n. Chebyshev for χ²_{n−1} gives (E3) with failure probability ≤ 2n^{2/3}/(n−1). Since
μ ∈ span X_{S₀}, (C − P_{V∪S₀})(C − P_V) = C − P_{V∪S₀} is a contraction applied to (C − P_V)Y, so
RSS_V ≥ ‖(C − P_{V∪S₀})Cε‖² = ‖Cε‖² − ‖P_{V∪S₀}ε‖² ≥ σ²(n−1)(1 − ϑ_n): (E2). (E4): ‖Y‖² ≤ 2Mn + 2σ²(n−1)(1 + n^{−1/3}) ≤ C_R n.
For U ∈ {T, T+l} ⊆ 𝓗 ∪ {∅} and n large (ϑ_n ≤ ½, n ≥ 4): RSS^y_U = (n−1)RSS_U/‖Y‖² ≥ (n−1)²σ²/(2C_R n) ≥ c_E n. Insert. ∎

### 4.2 Corollaries (on E_n; W, l with W ∪ {l} ∈ 𝓗 and (W∖l, l) ∈ 𝔉; k′ := |W∖l|)

odds_l(W) := γ₁(W ∪ l)/γ₁(W∖l), prior ratio (k′+1)/(2p − k′ − 1); q := (δ + σZ)², δ := δ_{W∖l,l}, Z := Z_{W∖l,l}.

- **(C1) Gibbs odds**, **(C2) floor** (or the locked deterministic T10 floor), **(C4) signal gain**, **(C5) gain from a signal
  gap**: as in SU §2, unchanged (A-REV2: VERIFIED).
- **(C6) Multi-step**: as in SU, **provided every single addition of the telescoping chain from V to V′ is a pair of 𝔉**
  (automatic for 𝔉_k when |V′| ≤ k).
- **(C3-up) zero-leakage ceiling.** If δ = 0 (W need not contain S₀):
  odds_l(W) ≤ [(k′+1)/(2p−k′−1)](n+1)^{−1/2} e^{κ_n + ϑ′_n} e^{Z²/2}.
  (A-REV2: VERIFIED. In fact e^{ϑ′_n/2} suffices: νσ²Z²/RSS_{W∪l} ≤ (Z²/2)(1 + 3/n)/(1 − ϑ_n) by (E2).)
- **(C3-low) matching floor, signal fully inside W∖l.** If **μ ∈ span X_{W∖l}** (e.g. W∖l ⊇ S₀; then δ = 0):
  odds_l(W) ≥ [(k′+1)/(2p−k′−1)](n+1)^{−1/2} e^{−κ_n − ϑ′_n} e^{Z²/2}.
  *Proof.* −ν log(1 − x) ≥ νx with x = σ²Z²/RSS_{W∖l}; RSS_{W∖l} = ‖(C − P_{W∖l})Cε‖² ≤ ‖Cε‖² ≤ σ²(n−1)(1 + n^{−1/3})
  (E3); so νx ≥ (Z²/2)/(1 + n^{−1/3}) ≥ Z²/2 − (Z²/2)n^{−1/3} ≥ Z²/2 − ϑ′_n using Z² ≤ L log n (E1). Then (U). ∎
- **(C3-low′) floor under zero leakage only** [new]. If δ = 0 (signal may lie outside W):
  odds_l(W) ≥ [(k′+1)/(2p−k′−1)](n+1)^{−1/2} e^{−κ_n} exp{σ²Z²/(2C_R)}.
  *Proof.* νx ≥ (n/2)σ²Z²/RSS_{W∖l} and RSS_{W∖l} ≤ ‖Y‖² ≤ C_R n (E4). ∎ Since C_R ≥ 4σ², the exponent coefficient is at
  most Z²/8: this is a valid but weak floor. The sharp coefficient is σ²/(2v_{W∖l}) with v_T = σ² + Δ_T, which needs an
  additional uniform event of the type |RSS_U − (n−1)v_U| ≤ n^{3/4} (SEX Theorem 6, Step 0 (ii)); not claimed here.

**COUNTEREXAMPLE to SU's "matching lower bound" under δ = 0 alone** (A-REV2 §6.3; reproduced exactly from 2×2 sufficient
statistics). n = 10⁶, p = 2, G = (n−1)I, S₀ = {1}, μ = x₁, σ² = M = φ₀² = 1, W = {2}, T = ∅, noise ⟂ x₁ with
u₂ᵀε = √65 and ‖ε‖² = n − 1, L = 5: (E1)–(E4) hold; κ_n = 12.2400132448, ϑ′_n = 0.7028313369; actual
log BF({2}) + ½ log(n+1) = 16.2502645682 < claimed Z²/2 − κ_n − ϑ′_n = 19.5571554183. Along these designs the statistic
tends to Z²/4 (the omitted signal doubles RSS_∅), so the claimed floor fails whenever Z² > 4·0.51/c_E ≈ 49: a fixed
positive (here ≈ 2·10⁻¹² per comparison, because κ is loose) probability, and a certain failure on the stated event.
The ERROR is in the statement; no downstream use relies on it (REPORT §2.4).

---

## 5. What is not changed

Locked results, adoption decisions and source status words are unchanged. In particular: T03♯ stays PROVED (candidate)
with S03's hypotheses; Theorem A A1–A4 PROVED; Theorems B (inclusions) PROVED, C sketches; EXP′ Theorem 1 PROVED;
Theorems 3–4 PROVED given H3; reference transfer and random-design extensions PROOF SKETCH / GAP; Lemma U PROVED (budgeted).

# Proposition NEC — the non-degeneracy hypothesis cannot be dropped from Lemma X (W3-DIST; sharpness result, not a target clause)

Status: **DRAFT**. v0.3, 2026-11-15 (v0.2: three presentation amendments marked [amended, L7-0x]; v0.3: the numerical remark §8(d) reworded per D2-01; no change to the
Proposition, the Corollary, their constants or their proofs). Provenance: §1–§6 are the API proof attempt `../work/api_attempts/dist1b/F-b-r2.md`
(Fable batch run by HQ; proof material), reproduced with three clarifications marked [amended]; §0 and §7–§8 are rewritten
by the lead (the attempt's own commentary overstated what follows from the Proposition). Notation: `../API_CARDS.md`
"Common definitions"; Lemma X: `../STATEMENT.md` §3. [P1] = the locked T01 proof file.

## 0. Statement
**Proposition NEC (fixed design, in-sample).** For every n large enough there is a standardised design X = X^{(n)} with
p = ⌊√n⌋ + 1 columns (so p ≤ n^A for every A ≥ 1) and K = p, such that for the null truth θ* = 0 (s₀ = 0, μ = 0; hence (E; M)
and (C; M′) hold for **every** M, M′ ≥ 0) and Gaussian noise of variance σ*²: for every integer k ≥ 1 there are c₄(k) > 0 and
n₄(k) with, for all n ≥ n₄(k),
  P_e[ Π( ‖μ̂ − μ‖² ≥ (k/24)σ*² log n | y ) ≥ c₄(k)/(2n) ] ≥ 0.6.
**Corollary NEC (Lemma X without (ND) is false).** There are no constants c ∈ (0, 1], C, M₀, n₀ — whatever they are allowed
to depend on among (s₀^r, A, σ*², M, M′, κ₀) — such that for all n ≥ n₀, all M₀ log n ≤ t ≤ n^{1−κ₀} and all fixed designs with
p ≤ n^A satisfying (E; M) and (C; M′):  P_e[Π(‖μ̂ − μ‖² > Cσ*²t | y) > e^{−ct}] ≤ 2e^{−ct}. The same holds if the outer bound 2e^{−ct}
is replaced by any sequence tending to 0. So the distance clause of Lemma X (not only its size clause) needs (ND) or a
substitute.
**What this does not say.** (1) It does not contradict Lemma X, Theorem DIST-1 or any target clause: the design violates
(ND) (already at j = 2), so the remainder of (1.1) equals 1 on it. (2) It does not contradict Lemma X′ or (1.2): Lemma X′ has the
squared in-sample radius Cσ*²tℓ_n with t ≥ M₀ log n (§8), and (1.2) is a random-design statement in the Hellinger distance, with
radius C√(tℓ_n/n), for which this fixed-design in-sample bound supplies no counterexample [amended, L7-01]. (3) It is a fixed-design, in-sample statement: it does not by itself refute a
random-design Hellinger statement without the non-degeneracy condition (that would need a law of x realising the design
and a population lower bound; not done). (4) It says nothing against the in-probability form (§8).

## 1. Design

Take σ* = 1. (π is invariant under y_c ↦ σ*y_c, since b and Q^c_S both scale by σ*², and μ̂ scales by σ*.)

- p′ := ⌊√n⌋, p := p′ + 1, columns indexed 0, 1, …, p′; L := log p′; β := 256; d := 1 + βL.
- u₀, u₁, …, u_{p′} orthonormal in ℝ^N (possible since p ≤ N). The design is defined for n so large that d < n + 1 (it does
  not exist, e.g., at n = 400); the regime of interest Nτ² ≪ 1 needs n ≫ 256 log n.
- τ² defined by Nτ² = (d − 1)/(n + 1 − d), so τ² ≍ log n/n²; a := √(1 − τ²).
- **Anchor:** x_{c,0} = √N u₀. **Near-copies:** x_{c,j} = √N(a u₀ + τ u_j), 1 ≤ j ≤ p′. X := U X_c.

Columns are centred with ‖x_j‖² = N. Truth: θ* = 0, so S₀ = ∅, μ = 0, y_c = e, and (E; 0), (C; 0) hold. For large n, K = p, so Ω is all subsets.

Write z_j := u_jᵀe, iid N(0, 1) for j = 0, …, p′. With f(λ) = ((n+1)λ + 1)/(λ + 1) and h(λ) = nλ/((n+1)λ + 1) as in [P1] `lem:spec`:

- f(Nτ²) = d by the choice of τ; h := h(Nτ²) satisfies 1 − h = 1/d and 1/h = 1 + 1/n + 1/(nNτ²);
- f(N) = ((n+1)(n−1) + 1)/n = n;
- nNτ² ≥ n(d − 1)/(n + 1) ≥ ¾βL.

## 2. Exact spectra and determinants

**(a) S = J ⊆ {1..p′}, |J| = k ≥ 1.** G_S = N(a²11ᵀ + τ²I), with eigenvalues N(ka² + τ²) ≥ N (once) and Nτ² (k − 1 times). Hence D_S = f(N(ka² + τ²))·d^{k−1} ≥ n d^{k−1}.

**(b) S = {0} ∪ J, |J| = k ≥ 1.** G_S = N[[1, a1ᵀ], [a1, a²11ᵀ + τ²I]].
- Vectors (0, c) with c ⊥ 1 are eigenvectors with eigenvalue Nτ² (multiplicity k − 1).
- On span{(1, 0), (0, 1/√k)} the matrix is N[[1, a√k], [a√k, a²k + τ²]], with determinant N²τ² and largest eigenvalue λ₊ ∈ [N, N(k+1)]
  (upper end from the trace N(1 + k − (k−1)τ²) ≤ N(k+1); only f(λ₊) < n + 1 is used). So λ₋ = N²τ²/λ₊ ∈ (0, Nτ²].
- Hence D_S = f(λ₊)f(λ₋)d^{k−1}, and since f is increasing with 1 ≤ f ≤ n + 1:
  **n d^{k−1} ≤ D_S ≤ (n + 1) d^k.**

**(c) S = {0}.** D_S = n.

In all cases, for S ≠ ∅:

  D_S^{−1/2} ≤ n^{−1/2}·d·d^{−|S|/2}.  (2.1)

Also col X_{c,S} ⊆ span(u₀, u_j : j ∈ S∖{0}). With M_S ⪯ P_S ([P1] `lem:spec`(b)), this gives

  0 ≤ Q_∅ − Q_S = eᵀM_Se ≤ ‖P_Se‖² ≤ z₀² + Σ_{j∈S∖{0}} z_j²,  Q_S ≥ ‖e‖² − z₀² − Σ_{j≤p′} z_j².  (2.2)

**Plug-in bound for anchored models.** Let S = {0} ∪ J. In Q_S = min_φ{‖e − X_{c,S}φ‖² + (‖X_{c,S}φ‖² + ‖φ‖²)/n} take φ_j = h z_j/(√N τ) for j ∈ J and φ₀ = −a Σ_J φ_j. Then X_{c,S}φ = Σ_J h z_j u_j, and

  Q_S ≤ ‖e‖² − Σ_J z_j² + Σ_J z_j²[(1 − h)² + h²(1/n + 1/(nNτ²))] + φ₀²/n.

The bracket equals (1 − h)² + h(1 − h) = 1 − h, so

  Q_S ≤ ‖e‖² − hΣ_J z_j² + a²h²(Σ_J z_j)²/(nNτ²).

Therefore, if z_j² ≤ L for all j ∈ J, then with W_J := Σ_J z_j² ≤ kL and (Σ_J z_j)² ≤ k²L:

  Q_∅ − Q_S ≥ W_J − kL/d − k²L/(¾βL) ≥ W_J − c_k,  c_k := k/β + 4k²/(3β).  (2.3)

## 3. Good event

Fix an integer k ≥ 1. Put ε := 8/√n and 𝒢 := {1 ≤ j ≤ p′ : L/4 ≤ z_j² ≤ L}. Define

- a_j := e^{z_j²/2}1{j ∈ 𝒢}, A := Σ_j a_j, m₁ := E a_j;
- ã₀ := d^{−1/2}, ã_j := d^{−1/2}e^{(1+ε)z_j²/2} for j ≥ 1, Ã := Σ_{j=0}^{p′} ã_j.

Since e^{z²/2}φ(z) ≡ 1/√(2π): m₁ = 2(√L − √L/2)/√(2π) = √L/√(2π), and E a_j² = (2/√(2π))∫_{√L/2}^{√L} e^{z²/2}dz ≤ m₁e^{L/2} = m₁√p′.

Let 𝓔 be the intersection of the following events.

| event | definition | failure probability |
|---|---|---|
| 𝓔₀ | \|z₀\| ≤ 2 | ≤ 0.046 |
| 𝓔₁ | \|‖e‖² − N\| ≤ 4√N | ≤ 2N/(16N) = 1/8 (Chebyshev) |
| 𝓔₂ | Σ_{j≤p′} z_j² ≤ 2p′ | ≤ 2/p′ (Chebyshev) |
| 𝒯 | max_{j≤p′} z_j² ≤ 2L | ≤ p′·2φ(√(2L))/√(2L) = 1/√(πL) |
| 𝓔₃ | Ã ≤ p/2 | see below |
| 𝓔₄ | A ≥ p′m₁/2 | ≤ 4Var(A)/(p′m₁)² ≤ 4/(√p′ m₁) |

For 𝓔₃: on 𝒯, Ã equals the truncated sum Ã′ := d^{−1/2}(1 + Σ_j e^{(1+ε)z_j²/2}1{z_j² ≤ 2L}). Its mean satisfies

  E Ã′ ≤ d^{−1/2}(1 + p′·(2/√(2π))∫₀^{√(2L)} e^{εz²/2}dz) ≤ 1 + p′·2√(L/π)e^{εL}/√(βL) = 1 + (2/√(πβ))·p′·e^{εL} ≤ 1 + 0.0706·p′·e^{εL} ≤ 0.08p [amended, L7-02: 2/√(256π) = 0.07052… ≤ 0.0706]

for large n (εL → 0). By Markov, P(Ã′ > p/2) ≤ 0.16.

Total: P(𝓔ᶜ) ≤ 0.046 + 0.125 + 0.16 + o(1), so **P(𝓔) ≥ 0.6 for n ≥ n₁**.

On 𝓔, for large n:

- (i) By (2.2), every S ∈ Ω has Q_S ≥ N − 4√N − 4 − 2p′ ≥ n − 7√n, hence ν/(2b + Q_S) ≤ ν/Q_S ≤ (1 + ε)/2.
- (ii) B := 2b + Q_∅ = (1 + 0.02/N)‖e‖² ≤ n(1 + 5/√n), hence ν/B ≥ ½(1 − 5/√n).

## 4. Step A — on 𝓔, π(∅) ≥ ½ for large n

For S ≠ ∅ with |S| = k′, using (1 + x)^ν ≤ e^{νx}, then (i), (2.2) and (2.1):

  π(S)/π(∅) = [w(k′)/w(0)]·D_S^{−1/2}·(1 + (Q_∅ − Q_S)/(2b + Q_S))^ν
       ≤ [w(k′)/w(0)]·n^{−1/2}·d·e^{(1+ε)z₀²/2}·∏_{j∈S} ã_j.

Summing over |S| = k′: Σ_{|S|=k′}∏_{j∈S}ã_j ≤ Ã^{k′}/k′!. Also [w(k′)/w(0)]/k′! = ∏_{i<k′}(2p − 1 − i)^{−1} ≤ p^{−k′} for k′ ≤ p. Hence on 𝓔:

  Σ_{S≠∅} π(S)/π(∅) ≤ n^{−1/2}·d·e^{(1+ε)·2}·Σ_{k′≥1}(Ã/p)^{k′} ≤ e³(1 + βL)/√n → 0.

So π(∅) ≥ ½ for n ≥ n₂. (The design is "consistent": π(∅) is close to 1 on 𝓔.)

## 5. Step B — mass of anchored models built on 𝒢

Let 𝒮_k := {S = {0} ∪ J : J ⊆ 𝒢, |J| = k}. For such S, using (1 − x)^{−ν} ≥ e^{νx} with x = (Q_∅ − Q_S)/B, then (ii), (2.3) and Q_∅ − Q_S ≤ 4 + kL:

  ((2b + Q_∅)/(2b + Q_S))^ν ≥ exp(ν(Q_∅ − Q_S)/B) ≥ exp(½(W_J − c_k) − (5/(2√n))(4 + kL)) ≥ e^{−c_k/2 − 1}·∏_{j∈J} a_j

for large n. With D_S ≤ (n + 1)d^k and w(k+1)/w(0) = 1/C(2p − 1, k + 1) ≥ (k + 1)!/(2p)^{k+1}:

  Σ_{S∈𝒮_k} π(S)/π(∅) ≥ [(k + 1)!/(2p)^{k+1}]·(n + 1)^{−1/2}·d^{−k/2}·e^{−c_k/2 − 1}·e_k(a),

where e_k(a) is the k-th elementary symmetric polynomial of (a_j).

**Lower bound on e_k(a).** Expanding A^k over k-tuples, tuples with a repeated index contribute at most C(k, 2)·(max_j a_j)·A^{k−1}. So k!·e_k(a) ≥ A^k(1 − k² max_j a_j/(2A)). Here max_j a_j ≤ e^{L/2} = √p′ and, on 𝓔₄, A ≥ p′m₁/2. So e_k(a) ≥ A^k/(2·k!) ≥ (p′m₁/2)^k/(2·k!) for large n.

With m₁/√d ≥ 1/√(2π(β + 1)) and p′/p ≥ ½:

  Σ_{S∈𝒮_k} π(S)/π(∅) ≥ [(k + 1)e^{−c_k/2 − 1}/(4p√(n + 1))]·c₃^k,  c₃ := 1/(8√(2π(β + 1))) > 0.

Since p√(n + 1) ≤ 2n and π(∅) ≥ ½ (Step A), on 𝓔 for n ≥ n₃(k):

  **π(𝒮_k) ≥ c₄(k)/n,  c₄(k) := (k + 1)e^{−c_k/2 − 1}c₃^k/16.**  (5.1)

## 6. Step C — every S ∈ 𝒮_k is far, with conditional probability ≥ ½

Given (S, v, y): X_{c,S}θ ~ N(M_Se, vM_S), and ‖μ̂ − μ‖ = ‖X_Sθ‖ = ‖X_{c,S}θ‖. Write X_{c,S}θ = m + ω with m = M_Se and ω symmetric about 0. Then ‖m + ω‖² ≥ ‖m‖² whenever mᵀω ≥ 0, which has probability ≥ ½. So

  Π(‖μ̂ − μ‖² ≥ ‖M_Se‖² | S, y) ≥ ½.

By Cauchy–Schwarz, eᵀM_Se = (P_Se)ᵀ(M_Se) ≤ ‖P_Se‖·‖M_Se‖. With (2.2), (2.3), on 𝓔₀, for S ∈ 𝒮_k (W_J ≥ kL/4):

  ‖M_Se‖² ≥ (W_J − c_k)²/(W_J + z₀²) ≥ W_J − 2c_k − z₀² ≥ kL/4 − 2c_k − 4 ≥ kL/8 ≥ (k/24) log n

for large n, using L = log⌊√n⌋ ≥ (log n)/3. Combining with (5.1):

**Proposition (counterexample).** For every integer k ≥ 1 there is n₄(k) such that, for the design of §1 and n ≥ n₄(k), with P_e-probability ≥ 0.6:

  Π(‖μ̂ − μ‖² ≥ (k/24)σ*² log n | y) ≥ c₄(k)/(2n).

## 7. Proof of Corollary NEC
Suppose such constants existed. Let T := max(M₀, 2/c), t := T log n (in the range for n large) and k := ⌈24CT⌉ + 1, so that
(k/24)σ*² log n > Cσ*²t. The design of §1 satisfies (E; M), (C; M′) for the given M, M′ (indeed for all M, M′ ≥ 0) and p ≤ n^A.
By the Proposition, for n ≥ n₄(k), with probability ≥ 0.6 the posterior mass of {‖μ̂ − μ‖² > Cσ*²t} is ≥ c₄(k)/(2n) > n^{−2} ≥ n^{−cT} =
e^{−ct} for n large (c₄(k) is a fixed positive number), while 2e^{−ct} ≤ 2n^{−2} < 0.6: a contradiction. The same argument applies
with any outer bound tending to 0. ∎ [amended: the multiplier is called T, not M, to avoid the clash with (E; M).]
The design violates (ND): for |J| = 2 among the near-copies, D_J/D_∅ ≤ (n + 1)d with d = 1 + 256 log⌊√n⌋ ≪ c_D²(n + 1)².

## 8. Remarks (lead)
(a) *Lemma X′ and (1.2) are not contradicted.* Lemma X′ bounds the mass of {‖μ̂ − μ‖² > Cσ*²tℓ_n} for t ≥ M₀′ log n, i.e. at radius
≥ CM₀′σ*² log² n; the Proposition is for a fixed k (radius of order log n), with c₄(k) = e^{−Θ(k²)} once k is large, so it gives
nothing at k of order log n.
(b) *Whether the extra logarithm of Lemma X′ is necessary is open* (it would need the Proposition uniformly in k up to
order log n without the k² loss in c_k).
(c) *In-probability form.* On this design Π(‖μ̂‖² > 0 | y) ≤ 1 − π(∅) → 0 in probability (Step A with the events 𝓔₀, 𝓔₁
replaced by windows ω_n → ∞ slowly and 𝓔₃ controlled by Chebyshev's inequality); so the design does not break the
in-probability form. Whether Π(‖μ̂ − μ‖² > M_n σ*² log n | y) → 0 holds for every design under (E), (C) alone is open.
(d) The threshold n₁ implicit in P(𝓔) ≥ 0.6 is large with the stated bounds (the term P(𝒯ᶜ) ≤ 1/√(πL)); explicit constants,
not optimised. A numerical check on the posterior restricted to the models of size ≤ 4 (that is, conditional on |S| ≤ 4, computed
exactly; larger models are not summed, so these conditional family masses are upper bounds on their full-posterior
counterparts [amended, L7-03, D2-01]; n = 1600, 6400, 25600; 200 noise draws each) shows n·π(𝒮₁ | |S| ≤ 4) ≈ 2·10⁻²,
n·π(𝒮₂ | |S| ≤ 4) ≈ 5·10⁻⁴, flat in n, and the corresponding posterior-threshold check under the restricted posterior in every draw
for k = 1, 2; this does not verify the full-posterior event, which is what the proof establishes
(`../reviews/P7_opus_precheck_NEC.md` §3; evidence, not proof).

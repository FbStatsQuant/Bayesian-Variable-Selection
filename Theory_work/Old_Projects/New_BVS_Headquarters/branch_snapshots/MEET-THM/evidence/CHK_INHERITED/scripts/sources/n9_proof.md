# N9 (V5): kernel reversibility, self-adjointness of the round, exact start sampler: proofs against the production code

Branch `theory/N9-KERNEL`, from `origin/theory/campaign`. Code: `Scripts/SMC_BVS/core/cpp/` at commit `39db138`, the only
commit that touches `core/`. The v3.1 method decision (LEDGER: "v3.1 = v3 + PEL (C1–C5) + LS0 + log_Z NA fix") does not
touch the step functions, the round or the start sampler, so this audit covers v3.1 as well.
Every file:line below refers to `Scripts/SMC_BVS/core/cpp/` unless another path is given.
Status words follow `theory_campaign/PROTOCOL.md`. Each **PROVED** below is a *candidate*: it has not been reviewed.

## 0. Objects, hypotheses, and what "the code's γ_φ" is

**State space.** 𝒮_K = {S ⊆ {0,…,p−1} : |S| ≤ K}, K = min(p, ⌊n/2⌋) (`v3_score.h:40`). A particle stores S sorted,
a bitset, a Zobrist hash and the four numbers (log m, lg0, d, F) (`v3_engine.h:11-15`).

**The code's target.** `Engine::eval` (`v3_engine.h:89-101`) sets, for the sorted model S with k = |S|,

```
c(S)   = Σ_b log r_b(S ∩ C_b)              Start::comp, v3_start.h:54-66 (blocks met by S, increasing block order)
lg0(S) = logprior[k] + c(S)                v3_engine.h:97
d(S)   = (log m(S) − log m(∅)) − c(S)      v3_engine.h:97
log γ_φ(S) = lg0(S) + φ·d(S)               Particle::lgphi, v3_engine.h:14
```

with logprior[k] = log w(k) − log W_K (`v3_score.h:61-70`), log r_b(U) = log m(U) − log m(∅) for U ≠ ∅ and exactly 0 for
U = ∅ (`v3_start.h:95`). In exact arithmetic

  γ_φ(S) = ϖ(S) · BF(S)^φ · ∏_b r_b(S∩C_b)^{1−φ} ∝ (ϖ(S) m(S))^φ · π₀(S)^{1−φ},  S ∈ 𝒮_K,

which is M §6.3 ("γ_φ = γ₀ e^{φd}"). It equals π₀ at φ = 0 and the posterior of M §5 (up to the constant m(∅)) at φ = 1.

*Notation remark (not a code issue).* The task text writes γ_φ ∝ prior(S)·m(S)^φ·π₀(S)^{1−φ}. Read literally this has an
extra factor ϖ(S)^{1−φ}; the spec and the code use ϖ(S)·m(S)^φ·(∏_b r_b)^{1−φ} = (ϖ m)^φ π₀^{1−φ} × const. All statements
below are for the code/spec γ_φ. CHECK.md §2 confirms numerically that the code's lgphi equals the spec formula built from
an independent long-double implementation of M §5, up to a constant, to ≤ 1e-13.

**Hypotheses used throughout.**
- **(H-U) ideal uniforms.** Every call `vs->u(·)` returns a fresh U[0,1) variable independent of everything drawn before.
  In production the source is one xoshiro256** stream per island (`v3_engine.h:20-23`, `v3_util.h:44-60`) shared by all
  particles of the island, and the number of uniforms a step consumes depends on the state (self-loops consume none, an
  empty neighbour candidate set consumes one). Under (H-U) this is harmless: the index at which a step starts reading is a
  stopping time of the iid sequence, so the uniforms it reads are iid U[0,1) and independent of the past (strong Markov
  property of an iid sequence). The deviations of the real generator (53-bit grid) are quantified in §5.
- **(H-A) exact arithmetic** for the proofs; floating-point effects are listed in §5 and measured in CHECK.md.
- **(H-D) determinism of the score.** log m(S) is a function of the sorted S only. True in the code: `Scorer` is stateless
  apart from scratch buffers that are fully overwritten (`v3_score.h:145-237`; route choice Cholesky → refactor → QR is
  a deterministic function of S), and the cache returns the stored bits of the first evaluation (`v3_score.h:239-296`).
  Table scores are computed by the same scorer (`v3_start.h:93`). Hence lg0, d and γ_φ are functions of S. A
  `NumericalFailure` (`v3_score.h:235`) aborts the run; it is not a kernel event.

Everything the kernels use besides S and fresh uniforms is fixed before any island runs: the blocks, tables and π₀ tables
(`cpp_setup`, `v3_core.cpp:269-300`, built once per setup), the neighbour graph N (same place), B, K, φ. They depend on
the data (X, y) but not on any particle or population. Point (e) of the task is answered by this: no step conditions on
a population-dependent quantity; the only state-dependent quantities are the feasibility of a Gibbs addition, the
self-loop rules, and |N(j)∖S|, all handled below.

The standard criterion used: a Markov kernel P on the finite set 𝒮_K is γ-reversible iff γ(S)P(S,S′) = γ(S′)P(S′,S) for all
S ≠ S′. Self-loops never matter. For a Metropolis–Hastings step with proposal q and acceptance a(S,S′) = 1 ∧ ρ(S,S′), it
suffices that ρ(S,S′) = γ(S′)q(S′,S)/(γ(S)q(S,S′)) whenever q(S,S′) > 0, and that q(S,S′) > 0 ⇔ q(S′,S) > 0.

## 1. The four elementary moves

### 1.1 Gibbs coordinate j

Code (`v3_engine.h:113-132`):
```
113  void step_gibbs(Particle& P, int j, double phi) {
115    bool in = bit_get(P.bits, j);
116    bool add_ok = in || (int)P.S.size() < D.K;
119    if (in || add_ok) {
120      tmpQ = P;
121      if (in) del_var(tmpQ, j); else add_var(tmpQ, j);
122      eval(tmpQ, ME_GIBBS_FLIP);
124      double lw = in ? P.lgphi(phi) : tmpQ.lgphi(phi);
125      double lo = in ? tmpQ.lgphi(phi) : P.lgphi(phi);
126      oj = plogis_log(lw - lo);
127    }
128    if (rb_on) rb_acc[j] += oj;  // R8: recorded before the draw
129    double u = vs->u("gibbs");
130    bool include = u < oj;
131    if (include != in) { P = tmpQ; m.gibbs_change++; }
```
with `plogis_log(x) = 1/(1+e^{−x})` (`v3_util.h:89-93`).

**Kernel.** Write S⁺ = S ∪ {j}, S⁻ = S ∖ {j}. If S⁺ ∈ 𝒮_K: P_j(S, S⁺) = γ_φ(S⁺)/(γ_φ(S⁺)+γ_φ(S⁻)), P_j(S, S⁻) = the
complement (heat bath; one of S⁺, S⁻ is S). If S⁺ ∉ 𝒮_K, i.e. j ∉ S and |S| = K, then `add_ok` is false, o_j = 0, and
P_j(S,S) = 1 (the addition at the cap is excluded, M §6.5 / ruling R1).

**Claim G.** P_j is γ_φ-reversible on 𝒮_K for every φ ∈ [0,1].

*Proof.* P_j(S,S′) > 0 with S′ ≠ S only if {S,S′} = {T∖{j}, T} for some T ∋ j. If T ∈ 𝒮_K, then both T and T∖{j} take the
branch `in || add_ok` (from T, `in` holds; from T∖{j}, |T∖{j}| ≤ K−1 so `add_ok` holds), and
γ(T∖j)·P_j(T∖j, T) = γ(T∖j)γ(T)/(γ(T)+γ(T∖j)) = γ(T)·P_j(T, T∖j). If T ∉ 𝒮_K (|T| = K+1), T is not a state and
P_j(T∖j, T) = 0 by the cap rule, so no pair arises. The move never leaves 𝒮_K. ∎

Boundary cases: at S = ∅ with j: addition allowed if K ≥ 1 (always, since n ≥ 2 and p ≥ 1); at |S| = K: deletions follow
the heat bath, additions are self-loops. Note o_j is computed **before** the draw and is a function of S only (H-D), so
the RB record does not affect the kernel.

### 1.2 Uniform swap

Code (`v3_engine.h:146-159`, `nth_nonmember` `:134-144`):
```
148    if (k == 0 || k == p) { ms.us_self++; return; }
150    int j = P.S[(int)std::floor(vs->u("uswap_j") * k)];
151    int l = nth_nonmember(P.bits, (int)std::floor(vs->u("uswap_l") * (p - k)));
152    tmpQ = P; del_var(tmpQ, j); add_var(tmpQ, l);
154    double la = tmpQ.lgphi(phi) - P.lgphi(phi);
155    double alpha = (la >= 0) ? 1.0 : std::exp(la);
157    bool acc = u < alpha;
```
**Proposal.** For 1 ≤ k = |S| ≤ p−1: j uniform on S (prob 1/k), l uniform on the complement (prob 1/(p−k); `nth_nonmember`
returns the m-th non-member in increasing order, a bijection {0,…,p−k−1} → S^c). The map (j,l) ↦ S′ = S−j+l is
injective (S∖S′ = {j}, S′∖S = {l}), so q(S,S′) = 1/(k(p−k)) for every S′ with |S′ △ S| = 2, |S′| = |S|, and 0 otherwise.
Acceptance a = 1 ∧ γ_φ(S′)/γ_φ(S). For k ∈ {0, p}: self-loop, no uniform consumed.
(floor(u·k) ≤ k−1 for every u on the generator's grid, since u ≤ 1 − 2⁻⁵³; `v3_util.h:60`.)

**Claim U.** The uniform swap is γ_φ-reversible on 𝒮_K.

*Proof.* q(S,S′) = q(S′,S) = 1/(k(p−k)) because |S′| = |S| = k; the MH ratio is γ(S′)/γ(S), which is what is coded. The
size is preserved, so S′ ∈ 𝒮_K whenever S ∈ 𝒮_K: no proposal leaves the support and the cap needs no rule. At |S| ∈ {0,p}
the step is the identity, which is reversible; such S have no swap neighbours, so no pair with q > 0 involves them. ∎

(|S| = p is reachable only when K = p, i.e. p ≤ ⌊n/2⌋.)

### 1.3 Neighbour swap

Graph (`v3_blocks.h:149-173`): for each j, the candidates l ≠ j sorted by |r_jl| descending (ties by index); keep the
`above` ones with |r_jl| > r_n, at least 1, at most B (`:165-168`); then
```
170  for (int j = 0; j < p; ++j) for (int l : chosen[j]) { N[j].push_back(l); N[l].push_back(j); }
171  for (int j = 0; j < p; ++j) { std::sort(N[j].begin(), N[j].end()); N[j].erase(std::unique(...), N[j].end()); }
```
So N is **symmetric by construction** (l ∈ N(j) ⇔ j ∈ N(l)), **loop-free** (l ≠ j, `:159`) and **duplicate-free**
(`:171`). Degrees are not capped after the union (the cap B applies to `chosen[j]` only), and they differ between
vertices in general. None of this depends on floating-point symmetry of r: the symmetry comes from the union.

Step (`v3_engine.h:162-180`):
```
165    if (k == 0) { ms.ns_self++; return; }
167    int j = P.S[(int)std::floor(vs->u("nswap_j") * k)];
169    for (int l : Nb[j]) if (!bit_get(P.bits, l)) cand.push_back(l);
170    if (cand.empty()) { ms.ns_noscore++; return; }
171    int l = cand[(int)std::floor(vs->u("nswap_l") * cand.size())];
172    tmpQ = P; del_var(tmpQ, j); add_var(tmpQ, l);
173    int back = 0; for (int x : Nb[l]) if (!bit_get(tmpQ.bits, x)) ++back;  // |N(l) \ S'| >= 1 (j is in it)
175    double la = tmpQ.lgphi(phi) - P.lgphi(phi) + std::log((double)cand.size()) - std::log((double)back);
176    double alpha = (la >= 0) ? 1.0 : std::exp(la);
178    bool acc = u < alpha;
```
**Proposal.** For S ≠ ∅, k = |S|: j uniform on S; if N(j)∖S = ∅ the step is a self-loop; otherwise l uniform on N(j)∖S.
Since the pair (j,l) is determined by S′ = S−j+l, q(S,S′) = (1/k)·(1/|N(j)∖S|) if l ∈ N(j)∖S, else 0. The acceptance is
1 ∧ [γ_φ(S′)/γ_φ(S)]·|N(j)∖S|/|N(l)∖S′| (`back` = |N(l)∖S′|, computed on the bitset of S′).

**Claim N.** The neighbour swap is γ_φ-reversible on 𝒮_K, for every symmetric loop-free duplicate-free graph N, whatever
the degrees.

*Proof.* Let q(S,S′) > 0, S′ = S−j+l, l ∈ N(j)∖S. The reverse move from S′ (|S′| = k ≥ 1) must delete l (prob 1/k) and
add j. Symmetry gives j ∈ N(l); j ∉ S′; so j ∈ N(l)∖S′, this set is non-empty (`back` ≥ 1, the comment at `:173` is
right), and q(S′,S) = (1/k)(1/|N(l)∖S′|) > 0. Hence q(S,S′) > 0 ⇔ q(S′,S) > 0 and
  q(S′,S)/q(S,S′) = |N(j)∖S| / |N(l)∖S′|,
which is exactly the factor in `:175`. The MH criterion gives reversibility. The size is preserved, so no proposal leaves
𝒮_K. ∎

Points (a) of the task: (i) **different degrees**: handled by the Hastings factor, which depends on the *available*
degrees |N(j)∖S| and |N(l)∖S′|, not on deg(j), deg(l); CHECK.md counts the proposals where it differs from 1. (ii)
**non-symmetric graph**: impossible by `:170`; if it were not symmetric, a proposal S→S′ with j ∉ N(l) would have
q(S′,S) = 0 and the step would not be reversible (and not invariant in general). (iii) **capped degrees**: the cap acts
before the symmetric union; any degree pattern is covered by the proof. Duplicates would bias the uniform choice in
`cand`; `:171` removes them. The B labels N1..NB run the same kernel (the label index `b` only names the event, `:164`).

### 1.4 Independence move with π₀ proposal

Code (`v3_engine.h:182-192`):
```
184    std::vector<int> S; draw_start(S);          // draw_pi0(st, *vs, S), :108
185    set_model(tmpQ, S);
186    eval(tmpQ, ME_INDEP);
187    double la = phi * (tmpQ.d - P.d);
188    double alpha = (la >= 0) ? 1.0 : std::exp(la);
190    bool acc = u < alpha;
```
**Kernel.** S′ ~ π̂₀, the law implemented by `draw_pi0`, independent of S (it reads only fresh uniforms and the fixed
tables). Accept with 1 ∧ e^{φ(d(S′)−d(S))}.

**Claim I.** If π̂₀ = π₀ := γ₀/Z̄₀ on 𝒮_K (proved in §3), the step is γ_φ-reversible.

*Proof.* The MH ratio for an independence proposal is
  γ_φ(S′)π₀(S) / (γ_φ(S)π₀(S′)) = [γ₀(S′)e^{φd(S′)} γ₀(S)/Z̄₀] / [γ₀(S)e^{φd(S)} γ₀(S′)/Z̄₀] = e^{φ(d(S′)−d(S))},
which is `:187`. Equivalently γ_φ(S)P(S,S′) = Z̄₀ π₀(S)π₀(S′)·min(e^{φd(S)}, e^{φd(S′)}), symmetric in (S,S′). ∎

Point (d): **the acceptance ratio does not involve Z̄₀ at all** (it cancels), so the exactness of Z̄₀ matters for the
evidence estimator (M §6.12, `v3_engine.h:299`), not for this step. What the step needs is that the sampler's law is
exactly proportional to the *same* γ₀ = exp(lg0) that enters d. Both are built from the same `logprior` and the same
`logr` table (lg0 via `Start::comp`, the sampler via `logprof`/`sub_cum` from `logr`), so this holds in exact arithmetic;
§5 gives the floating-point size. Support: π₀ charges only 𝒮_K (sizes ≤ K by construction, §3), so no proposal leaves
the support, and π₀(S) > 0 on all of 𝒮_K as long as every log m is finite. At φ = 0 every proposal is accepted (the step is
an exact π₀ draw).

## 2. The round

Code (`v3_engine.h:193-214`):
```
195  void draw_order(std::vector<int>& ord) {
196    int m = nlabels();                                  // p + B + 2, :72
198    for (int i = 0; i < m; ++i) ord[i] = i;
199    for (int i = m - 1; i >= 1; --i) { int jj = (int)std::floor(vs->u("order") * (i + 1)); std::swap(ord[i], ord[jj]); }
200  }
202  void one_round(Particle& P, int i, double phi) {
203    std::vector<int> ord; draw_order(ord);
205    for (size_t pos = 0; pos < ord.size(); ++pos) {
208      if (lab < p) { step_gibbs(P, lab, phi); ... }
209      else if (lab == p) { step_uswap(P, phi); ... }
210      else if (lab <= p + B) { step_nswap(P, phi, lab - p); ... }
211      else { step_indep(P, phi); ... }
```
**How the order is drawn.** Before the first step of the round, from m−1 fresh uniforms, by Fisher–Yates
(i = m−1,…,1; position i swapped with a uniform position in {0,…,i}). The labels are fixed: p Gibbs labels (one per
coordinate), one U, B labels N, one I; the count per type is fixed (m = p + B + 2), never state- or φ-dependent. Under (H-U)
the m−1 uniforms are independent of P's state (they are read before any step of the round, at a stopping time of the
stream), and Fisher–Yates maps the (m−1)-tuple of choices bijectively onto the m! permutations (CHECK.md §4 verifies the
bijection on the production `draw_order` for m ≤ 8). So σ is uniform on S_m and independent of the state.

**Claim R.** Let K_1,…,K_m be γ-reversible Markov kernels on a finite set (repetitions allowed), and let σ be a random
permutation, independent of the chain, whose law μ satisfies μ(σ) = μ(σ∘ϱ) where ϱ is the reversal i ↦ m+1−i. Then
R = Σ_σ μ(σ) K_{σ(1)}K_{σ(2)}⋯K_{σ(m)} is γ-reversible (self-adjoint on L²(γ)). The uniform law on S_m satisfies the
hypothesis, so the production round kernel is γ_φ-reversible.

*Proof.* In L²(γ) each K_i is self-adjoint (reversibility). The adjoint of a product is the product of the adjoints in
reverse order: (K_{σ(1)}⋯K_{σ(m)})* = K_{σ(m)}⋯K_{σ(1)} = K_{(σ∘ϱ)(1)}⋯K_{(σ∘ϱ)(m)}. Hence
R* = Σ_σ μ(σ) K_{σ∘ϱ(1)}⋯K_{σ∘ϱ(m)} = Σ_τ μ(τ∘ϱ) K_{τ(1)}⋯K_{τ(m)} = Σ_τ μ(τ) K_{τ(1)}⋯K_{τ(m)} = R, using τ = σ∘ϱ
(a bijection, ϱ∘ϱ = id) and the reversal invariance of μ. The kernel of `one_round` is R because the order is drawn
independently of the state and each step then uses only fresh uniforms (H-U). ∎

**The exact condition, and what would break it.** Self-adjointness needs (i) every K_i γ_φ-reversible (§1, all at the
same φ: `one_round` passes one φ to all steps, `:202-211`), (ii) the law of the label sequence reversal-invariant, and
(iii) the sequence independent of the state. A varying number of steps per type is harmless as long as the law of the
whole label sequence (including its length) is reversal-invariant and state-independent, e.g. any exchangeable law. It
fails if the order or the step counts depend on the state, or if the order law is not reversal-invariant (e.g. a fixed
order; CHECK.md shows the canonical fixed order is γ_φ-invariant but not self-adjoint, as M §6.5 says). In the code m is
fixed and the order is uniform, so (ii) and (iii) hold.

*Invariance is weaker and is what the estimators use.* Each step is γ_φ-invariant (reversible ⇒ invariant), so every
realised order is γ_φ-invariant, and so is the round. The state immediately before any Gibbs step j of a round started
from γ_φ is γ_φ-distributed, whatever the order (the order is independent of the state); this is what the RB identity
E[o_j] = π_φ(j ∈ S) needs. Self-adjointness is needed only where a reversible kernel is required (spectral/variance
arguments; the rejection of C10).

## 3. The start sampler and Z̄₀

Spec (M §6.3): γ₀(S) = ϖ(S)∏_b r_b(S∩C_b), π₀ = γ₀/Z̄₀, Z̄₀ = Σ_{S∈𝒮_K} γ₀(S), ϖ(S) = w(|S|)/W_K.

Code (`v3_start.h:101-176`): for each block b with m_b members, top_b = min(m_b, K):
- `logprof[b][j]` = log e_b(j), e_b(j) = Σ_{U⊆C_b, |U|=j} r_b(U), j = 0..top_b (`:115-119`); `sub_cum[b][j]` is the
  cumulative of r_b(U)/e_b(j) over the size-j codes in increasing code order (`:118`);
- `logF[b][k]` = log F_b(k), F_0 = 1{k=0}, F_b(k) = Σ_{j ≤ min(k, top_{b−1})} e_{b−1}(j) F_{b−1}(k−j), k = 0..K (`:122-131`);
  so F_b is the size profile of the first b blocks (indices 0..b−1), truncated at K;
- `logZbar0` = log Σ_{k≤K} ϖ(k) F_J(k) (`:133-135`), `size_cum` its normalised cumulative (`:138`);
- `cond_cum[b][r]` ∝ e_b(j) F_b(r−j), j = 0..min(top_b, r) (`:141-149`): the law of block b's size given that blocks
  0..b carry r variables in total.

`draw_pi0` (`:158-176`): k ~ size_cum; then for b = J−1 down to 0 while r > 0, k_b ~ cond_cum[b][r], r −= k_b; blocks
not visited get k_b = 0; then for each block with k_b > 0 a code ~ sub_cum[b][k_b]; S = union, sorted.
Categorical draws use the smallest index with cumulative > u (`cat_draw_gt`, `:18-20`); the cumulative is normalised in
long double and set to exactly 1 from the last positive-mass category on (`:21-32`), so a zero-mass category is never
returned and P(index = i) = C_i − C_{i−1}.

**Claim Z.** F_J(k) = Σ_{S: |S| = k} ∏_b r_b(S∩C_b) for k ≤ K, and Z̄₀ = Σ_{k≤K} ϖ(k)F_J(k) = Σ_{S∈𝒮_K} γ₀(S).

*Proof.* A set S with |S| = k corresponds bijectively to (U_b)_b with U_b ⊆ C_b disjointly, Σ|U_b| = k, and
∏_b r_b(S∩C_b) factorises. Summing over U_b of size j_b gives Σ_{(j_b): Σ j_b = k} ∏_b e_b(j_b), the J-fold convolution.
Truncating each convolution at K is exact for indices ≤ K, because the k-th term of a convolution of non-negative
sequences involves only indices ≤ k. Each e_b is needed only up to min(m_b, K) for the same reason, and the table
entries with |U| > K (left NaN, `:92`) are never used (`codes_by_size` stops at top_b, `:111`). ϖ depends on S only
through |S| (M §6.3), so Σ_{S∈𝒮_K} γ₀(S) = Σ_{k≤K} ϖ(k) Σ_{|S|=k} ∏_b r_b(S∩C_b) = Σ_{k≤K} ϖ(k)F_J(k). ∎

**Claim S.** `draw_pi0` returns S with probability exactly π₀(S) for every S ∈ 𝒮_K (and never a set outside 𝒮_K).

*Proof.* Fix S ∈ 𝒮_K, k = |S|, k_b = |S∩C_b|, U_b = S∩C_b. The sampler returns S iff it draws k, then the block sizes
k_{J−1},…,k_0 (any block reached after r has become 0 must have k_b = 0, which matches the code's early stop because
cond_cum[b][0] puts mass 1 on j = 0), then U_b within each size class. With r_b := Σ_{c≤b} k_c,
  P(S) = [ϖ(k)F_J(k)/Z̄₀] · ∏_{b=J−1}^{0} [e_b(k_b)F_b(r_b − k_b)/F_{b+1}(r_b)] · ∏_{b: k_b>0} [r_b(U_b)/e_b(k_b)].
Since r_b − k_b = r_{b−1} and r_{J−1} = k, the middle product telescopes to ∏_b e_b(k_b)·F_0(0)/F_J(k) = ∏_b e_b(k_b)/F_J(k)
(F_0(0) = 1, and r_{−1} = 0). Blocks with k_b = 0 contribute e_b(0) = r_b(∅) = 1 to both products. Therefore
P(S) = ϖ(k)∏_b r_b(U_b)/Z̄₀ = π₀(S). Every denominator is positive along any path the sampler follows (a size or block size
of zero mass is never returned). The total size never exceeds K (size_cum ranges over 0..K), and k_b ≤ min(m_b, r). ∎

**Ties.** Ties among table values r_b(U), among block-size probabilities, or between sizes play no role in sampling: the
law is defined by the probabilities, not by an argmax. (Ties matter only for `start_mode`, `v3_start.h:178-240`, the
argmax S̃₀ of π₀, which is not part of N9.) Point 3 of the task is therefore answered without exception.

**Exactness of Z̄₀.** In exact arithmetic Claim Z is an identity. In floating point, logprof and logF are log-sum-exps
with long-double accumulation (`v3_util.h:74-81`): each log is computed with relative error O(ε·#terms) in the sum,
i.e. absolute error in log Z̄₀ of order J·(B + K)·ε. CHECK.md compares with an independent long-double brute force.

## 4. Summary of the proof status (exact arithmetic, (H-U), (H-D))

| Sub-claim | Status |
|---|---|
| Gibbs flip γ_φ-reversible, cap rule included | PROVED (candidate) |
| Uniform swap γ_φ-reversible, |S| ∈ {0,p} self-loop | PROVED (candidate) |
| Neighbour swap γ_φ-reversible (symmetric graph, any degrees, cap before union) | PROVED (candidate) |
| Independence move γ_φ-reversible (given Claim S) | PROVED (candidate) |
| Uniform random order of reversible kernels is self-adjoint; the code's order is uniform and state-independent | PROVED (candidate) |
| draw_pi0 draws exactly from π₀ (capped size prior, convolution, backward block sizes) | PROVED (candidate) |
| Z̄₀ = Σ_{𝒮_K} γ₀ exactly (truncated convolution) | PROVED (candidate) |

## 5. Departures of the implementation from the exact statements (all at floating-point / RNG-grid level)

1. **53-bit uniforms.** u = i·2⁻⁵³ (`v3_util.h:60`). (a) A comparison `u < α` accepts with probability ⌈α·2⁵³⌉/2⁵³,
   not α: a relative error ≤ 2⁻⁵³/α, and for α < 2⁻⁵³ (log-acceptance below −36.7) the implemented probability is 2⁻⁵³
   instead of α. This breaks detailed balance *in relative terms* on pairs with astronomically small flow, with
   absolute error ≤ 2⁻⁵³ per step and pair weight. (b) floor(u·k) is uniform on {0,…,k−1} only up to relative
   deviation ≤ k·2⁻⁵³ (CHECK.md §4). (c) Categorical draws in `draw_pi0` have probabilities that are differences of
   doubles on the 2⁻⁵³ grid; a category of probability < 2⁻⁵³ can get probability 0 or 2⁻⁵³. Consequence: the
   implemented π̂₀ satisfies TV(π̂₀, π₀) ≤ (number of categorical draws per sample ≤ 2J+1) × (max categories) × O(2⁻⁵³);
   CHECK.md measures it. Through π̂₀ ≠ π₀ the independence step is reversible w.r.t. γ_φ only up to the same order.
2. **Rounding of lg0, d.** lg0 + φd is computed as (logprior + c) + φ((logm − logm0) − c); the composite c does not
   cancel exactly at φ = 1, so γ₁ equals ϖ·m/m(∅) up to a relative error of a few ε·|c|. This changes the *target*
   (by a factor 1 + O(ε)), not the reversibility: every step uses the same lgphi function of S.
3. **One shared stream per island.** The order uniforms and the step uniforms of all particles of an island come from
   one stream; under (H-U) this is irrelevant (§0). It matters only for reproducibility claims (the v3.2 "per-particle
   streams" item in the LEDGER), not for N9.

None of these is a modelling or algebraic error; each is of the order of the machine epsilon or of 2⁻⁵³ per uniform,
and none can be fixed by a code change other than a higher-precision generator (not recommended).

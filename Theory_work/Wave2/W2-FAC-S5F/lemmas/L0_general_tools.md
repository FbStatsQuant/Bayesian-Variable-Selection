# L0 — Exact design-general tools for the LS0 scan (gains, Pythagoras, swap domination, truth moves)

Status: **PROVED (by this seat, unchecked)** (v1, 2026-11-09). Falsification numerics: numerics/n3_tools.py →
N3_out.txt (Part A: Pythagoras identity and jump inequality on explicit n × p designs; Part B1: swap identity on the
exact-Gram scanner). Lemma check: pending (reviews/R02).

Setting: STATEMENT §1 (D0, G, method) and the exact-Gram hypothesis in the **general** form

  (EG)  XᵀX = (n − 1)Σ with Σ a correlation matrix, λ_min(Σ) ≥ c_min > 0, p ≤ ⌊n/2⌋ (so K = p),

which contains (BCS) with c_min = c. Notation: for A ⊆ [p], P_A := projector onto span X_A, RSS_A := ‖(I − P_A)Y‖²,
Y = μ + e, e := Cε, μ = Xθ* ∈ span X_{S₀}; y := Y/s, s² := ‖Y‖²/(n − 1); G_A := X_AᵀX_A, H_A := (n + 1)G_A + I,
ψ_A := 0.02 + Q_A, Q_A := (n − 1) − n z_AᵀH_A⁻¹z_A, F(A) := log w(|A|) + log m(A) (D0). L_n := log log n.
**Statistics (exact).** For l ∉ T: Z²(l; T) := (RSS_T − RSS_{T∪l})/σ² ≥ 0; for j ∈ T: Z²(j; T) := Z²(j; T∖j) =
(RSS_{T∖j} − RSS_T)/σ². Equivalently Z²(l; T) = (x̃_lᵀY)²/(σ²‖x̃_l‖²) with x̃_l := (I − P_T)x_l (one-step Gram–Schmidt).

## L0.1 Q versus RSS (FAC-B L1.5(b) with c_min)

For every A ⊆ [p]: RSS_A/s² ≤ Q_A ≤ RSS_A/s² + 1 + 1/((n − 1)c_min).
*Proof.* Identical to FAC-B L1.5(b): (n − 1) − z_AᵀG_A⁻¹z_A = RSS_A/s²; nH_A⁻¹ ⪯ G_A⁻¹ gives the lower bound;
(G + I/(n+1))⁻¹ ⪰ G⁻¹ − G⁻²/(n+1) and λ_min(G_A) ≥ (n − 1)c_min give the upper bound (for A = ∅ both sides equal n − 1). ∎

## L0.2 The probability event and the multiplier

Let r := ‖(I − P_X)e‖²/σ² ~ χ²_{n−1−p} and define E⁰_n := {r ≥ (n − 1 − p)(1 − n^{−1/3}); ‖e‖²/σ² ≤ n − 1 + n^{2/3};
|θ*ᵀXᵀe| ≤ L_n σ‖μ‖}. P(E⁰_n) → 1 (Laurent–Massart as FAC-B L3 E2; the last is a N(0, σ²‖μ‖²) variable). On E⁰_n,
s² = (‖μ‖² + 2θ*ᵀXᵀe + ‖e‖²)/(n − 1) ∈ [s²_min, s²_max] := [σ²/2, 2(‖μ‖²/(n−1) + σ²)] for n ≥ n₀, and for every A:
σ² r ≤ RSS_A ≤ ‖Y‖² ... more precisely for A ⊇ S₀: RSS_A = ‖(I − P_A)e‖² ∈ [σ²r, ‖e‖²].
**Multiplier.** M_A := nσ²/(2 RSS_A). For A ⊇ S₀ on E⁰_n: ½(1 − n^{−1/3}) ≤ M_A ≤ 1 + 3n^{−1/3} (using p ≤ n/2). If
moreover Φ(A) := ‖P_A e‖²/σ² ≤ n/log n then M_A ≤ ½(1 + 2/log n) (since RSS_A = ‖e‖² − σ²Φ(A)). (As FAC-B L4.0(d).)

## L0.3 Every gain is a size term plus a likelihood term in the exact RSS increment, up to O(1)

Let c_Q := 1.02 + 1/((n − 1)c_min) and C_Q := (n/2 + 0.01) c_Q s²_max/(σ²(n − 1 − p)(1 − n^{−1/3})) (= O(1); for S5 and
n ≥ n₀, C_Q ≤ 2.1 s²_max/σ²). On E⁰_n, for every T ⊆ [p] with 1 ≤ k = |T| ≤ p, j ∈ T, l ∉ T:

  G_del(j; T) := F(T∖j) − F(T) = Δ_k(T, j) − ν log(RSS_{T∖j}/RSS_T) + E₁,
  G_add(l; T) := F(T∪l) − F(T) = −Δ_{k+1}(T∪l, l) + ν log(RSS_T/RSS_{T∪l}) + E₂,
  G_sw(j, l; T) := F(T∖j∪l) − F(T) = −½[Λ(T∖j∪l) − Λ(T)] + ν log(RSS_T/RSS_{T∖j∪l}) + E₃,

with |E_i| ≤ C_Q, Λ(A) := log det H_A − log det(G_A + I), and the **size term**
Δ_k(T, j) := log[(2p − k)/k] + ½[Λ(T) − Λ(T∖j)] = log[(2p − k)/k] + ½ log(n + 1) + δ(T, j), |δ(T, j)| ≤ 2/((n − 1)c_min).

*Proof.* F(T∖j) − F(T) = log[w(k−1)/w(k)] − ½[Λ(T∖j) − Λ(T)] − ν log(ψ_{T∖j}/ψ_T), and w(k−1)/w(k) = (2p − k)/k (D0).
*Size term.* Λ(T) − Λ(T∖j) = log(det H_T/det H_{T∖j}) − log(det(G_T+I)/det(G_{T∖j}+I)); by the Schur-complement formula
det H_T/det H_{T∖j} = (n² − 1)v_j + 1 and det(G_T + I)/det(G_{T∖j} + I) = (n − 1)v_j + 1, where v_j := Σ_jj −
Σ_{j,T∖j}Σ_{T∖j,T∖j}⁻¹Σ_{T∖j,j} ∈ [c_min, 1] (conditional variance; v_j = 1 if T = {j}). Hence ½[Λ(T) − Λ(T∖j)] =
½ log(n + 1) + ½ log[(v_j + 1/(n² − 1))/(v_j + 1/(n − 1))], and the last ratio lies in [1 − 1/((n − 1)v_j + 1), 1] ⊆
[1 − 1/((n−1)c_min), 1], so |δ| ≤ ½·2/((n − 1)c_min) for n ≥ n₀ (log(1 − x) ≥ −2x for x ≤ ½).
*Likelihood term.* By L0.1, ψ_{T∖j}/ψ_T ∈ [(RSS_{T∖j}/s² + 0.02)/(RSS_T/s² + c_Q), (RSS_{T∖j}/s² + c_Q)/(RSS_T/s² + 0.02)].
For A ≥ B > 0 and e₁, e₂ ∈ [0, c_Q]: |log((A + e₁)/(B + e₂)) − log(A/B)| ≤ c_Q/B. With B = RSS_T/s² ≥ σ²r/s²_max ≥
σ²(n − 1 − p)(1 − n^{−1/3})/s²_max, |ν log(ψ_{T∖j}/ψ_T) − ν log(RSS_{T∖j}/RSS_T)| ≤ ν c_Q s²_max/(σ²(n−1−p)(1−n^{−1/3}))
= C_Q. The addition and swap cases are identical (for the swap the prior ratio is 1 and the size term is
½[Λ(T) − Λ(T∖j∪l)], which by the two Schur steps T ↔ T∖j and T∖j∪l ↔ T∖j equals ½ log[((n²−1)v_j + 1)((n−1)v′_l + 1)/
(((n−1)v_j + 1)((n²−1)v′_l + 1))] with v_j, v′_l ∈ [c_min, 1], hence |½[Λ(T∖j∪l) − Λ(T)]| ≤ 2/((n − 1)c_min)). ∎

**Corollary L0.3′ (standardized form).** For T ⊇ S₀ (so RSS_T − RSS_{T∖j} etc. are pure noise quantities) on E⁰_n:
  G_del(j; T) ≥ Δ_k(T,j) − (1 + 1/n) M_T Z²(j; T) − C_Q;   G_del(j; T) ≤ Δ_k(T,j) − M_T Z²(j;T)(1 − σ²Z²/RSS_T) + C_Q;
  G_add(l; T) ≤ −Δ_{k+1}(T∪l, l) + (1 + 1/n) M_T Z²(l; T)(1 + 2σ²Z²(l;T)/RSS_T) + C_Q;
using log(1 + x) ≤ x, log(1 + x) ≥ x − x²/2, RSS_{T∪l} = RSS_T − σ²Z²(l;T) and ν/n ≤ ½(1 + 1/n). In all uses Z² = O(log n)
so σ²Z²/RSS_T = O(log n/n) and the corrections are o(1).

## L0.4 Pythagoras identity, monotonicity and the jump inequality (exact, any design, any sets)

For T ⊆ [p], j ∈ T, l ∉ T:
  (P)  Z²(j; T) + Z²(l; T) = Z²(l; T∖j) + Z²(j; T∖j ∪ l)   (both sides = (RSS_{T∖j} − RSS_{T∪l})/σ²),
  (J)  Z²(l; T∖j) ≤ Z²(l; T) + Z²(j; T)   (jump inequality),
  (M)  Z²(l; T) ≥ 0, i.e. RSS is non-increasing in the set.
*Proof.* RSS_{T∖j} − RSS_{T∪l} telescopes in two ways: via T (= σ²[Z²(j;T) + Z²(l;T)]) and via T∖j∪l (= σ²[Z²(l;T∖j)
+ Z²(j; T∖j∪l)]); (J) follows from (P) and Z²(j; T∖j∪l) ≥ 0 = (M), which holds because span X_{T} ⊆ span X_{T∪l}. ∎
**Ridge version.** The score uses Φ_λ(A) := z_Aᵀ(G_A + λI)⁻¹z_A, λ := 1/(n + 1), through Q_A = (n − 1) − (n/(n+1))Φ_λ(A)
(indeed z_AᵀH_A⁻¹z_A = Φ_λ(A)/(n + 1)). Φ_λ is also non-decreasing in A (Φ_λ(A) = ‖y‖² − min_β(‖y − X_Aβ‖² + λ‖β‖²)),
so (P), (J), (M) hold verbatim for the ridge increments Φ_λ(T∪l) − Φ_λ(T) in place of Z². L0.3 is the bridge between
the two: the gains are written in RSS and the error is absorbed in E_i.

**Corollary L0.4′ (sum of levels).** Along a sequence of deletions T₀ ⊃ T₁ ⊃ … ⊃ T_t (T_{i+1} = T_i ∖ j_i), for every
l ∈ T₀ ∖ T_t deleted at step t_l (j_{t_l} = l): Z²(l; T_t) ≤ Σ_{i=t_l}^{t−1} Z²(j_i; T_i), i.e. the add statistic of a
hole element is at most the sum of the deletion statistics of all elements deleted since (and including) itself.
*Proof.* Induction on t with (J): Z²(l; T_{i+1}) = Z²(l; T_i∖j_i) ≤ Z²(l; T_i) + Z²(j_i; T_i), starting from
Z²(l; T_{t_l + 1}) = Z²(l; T_{t_l} ∖ l) = Z²(l; T_{t_l}) — the deletion statistic of l at its deletion. ∎
(The bound is only useful when most terms vanish; in L1 it is applied to the *local* statistics of a block design,
where only the deletions from l's own group contribute.)

## L0.5 Swap domination through the one-below sets (exact)

For every T, j ∈ T, l ∉ T:  F(T∖j∪l) − F(T) = [F(T∖j∪l) − F(T∖j)] + [F(T∖j) − F(T)] = G_add(l; T∖j) + G_del(j; T).
Hence, if **(NA⁻)** G_add(l; T∖j) < 0 for every j ∈ T and l ∉ T (no addition improves at any one-below set T∖j), then
every swap neighbour of T has F strictly smaller than the best deletion neighbour: G_sw(j, l; T) < G_del(j; T) ≤
max_{j′∈T} G_del(j′; T). In particular, under (NA⁻) and "the best deletion has positive gain", the production rule (best
strictly improving scanned neighbour) never selects a swap, and if additionally G_add(l; T) < 0 for all l (NA at T),
the selected move is a deletion. ∎ (Exact; no approximation. The tie rule is irrelevant: strict inequalities.)

## L0.6 Truth moves are negative by order n (given a residual-noise bound)

Assume (EG), (θ) and, for the visited sets, the **truth residual-noise bound**
  (TR)  |⟨(I − P_A)x_j, e⟩| ≤ σ‖(I − P_A)x_j‖·R_n  for every truth j ∈ S₀ and every A ⊆ [p]∖{j} that occurs below,
with R_n = O(√log p) (verified for (BCS) in L1.6 for **all** A, using only the trivial centre bound). Then on E⁰_n, for
n ≥ n₀, for every T ⊇ S₀ with |T| ≤ p, every truth j ∈ S₀ and every null l ∉ T:
  (a) G_del(j; T) ≤ −(n/2) log(1 + c_θ) + log(2p) + ½ log(n + 1) + C_Q + o(1) < 0,  c_θ := |ϑ|²_min c_min/(3σ²);
  (b) G_sw(j, l; T) < G_del(j*; T) for the best null deletion j* whenever that deletion has gain ≥ −log n (in particular
      whenever it is positive); moreover G_sw(j, l; T) < 0.
*Proof.* (a) With x̃_j := (I − P_{T∖j})x_j and T∖j ⊇ S₀∖{j}: x̃_jᵀμ = θ*_j‖x̃_j‖² (the other truth columns lie in span
X_{T∖j}), so RSS_{T∖j} − RSS_T = (x̃_jᵀY)²/‖x̃_j‖² = (θ*_j‖x̃_j‖ + x̃_jᵀe/‖x̃_j‖)² ≥ (|ϑ|_min√((n−1)c_min) − σR_n)² ≥
|ϑ|²_min c_min(n − 1)/2 for n ≥ n₀ (‖x̃_j‖² = (n − 1)v_j ≥ (n − 1)c_min; (TR)). Divide by RSS_T ≤ ‖e‖² ≤ σ²(n − 1 + n^{2/3})
(L0.2): RSS_{T∖j}/RSS_T ≥ 1 + c_θ with c_θ := |ϑ|²_min c_min/(3σ²) for n ≥ n₀. By L0.3, G_del(j;T) ≤ Δ_k − ν log(1 + c_θ) +
C_Q ≤ log(2p) + ½ log(n+1) + o(1) − (n/2) log(1 + c_θ) + C_Q < 0.
(b) Let A := T∖j∪l ⊉ S₀. Since the truths other than j lie in span X_A, (I − P_A)μ = θ*_j(I − P_A)x_j, and
  RSS_A = θ*_j²‖(I − P_A)x_j‖² + 2θ*_j⟨(I − P_A)x_j, e⟩ + ‖(I − P_A)e‖².
Here ‖(I − P_A)x_j‖² = (n − 1)v′_j ≥ (n − 1)c_min, |⟨(I − P_A)x_j, e⟩| ≤ σ‖(I − P_A)x_j‖R_n by (TR), and, because
A ∪ {j} = T ∪ {l} ⊇ T ⊇ S₀, ‖(I − P_A)e‖² ≥ ‖(I − P_{T∪l})e‖² = RSS_{T∪l} = RSS_T − σ²Z²(l; T). Hence
  RSS_A − RSS_T ≥ |ϑ|²_min c_min(n − 1) − 2|ϑ|_max σ√(n − 1) R_n − σ²Z²(l; T) ≥ |ϑ|²_min c_min (n − 1)/2   (n ≥ n₀),
provided Z²(l; T) ≤ R′_n² with R′_n = O(√log p) — the **null residual-noise bound (TR′)**, which for (BCS) holds for
every T ⊇ S₀ and every null l by the configuration union bound plus the trivial centre bound (L1.6), i.e. without any
path information. So RSS_A/RSS_T ≥ 1 + c_θ (RSS_T ≤ ‖e‖² ≤ σ²(n − 1 + n^{2/3})), and by L0.3
  G_sw(j, l; T) = −½[Λ(A) − Λ(T)] − ν log(RSS_A/RSS_T) + E₃ ≤ o(1) − (n/2) log(1 + c_θ) + C_Q < −log n ≤ G_del(j*; T). ∎

**Remark.** Truths are never added (S₀ ⊆ T throughout). Truth-in swaps do not exist. So under (NA), (NA⁻) and L0.6, at
every visited T ≠ S₀ the production rule selects a null deletion, and at S₀ (where only additions and truth moves
exist) no move improves if (NA) holds at S₀ — this is how L4/L5 conclude.

## L0.7 Size-term bounds used downstream

For 1 ≤ k ≤ p: Δ_k ≥ ½ log(n + 1) − o(1); for k ≤ p/2: Δ_k ≥ ½ log n + log(p/k) − o(1); for k + 1 ≤ p, Δ_{k+1} ≥ ½ log(n+1)
+ log((2p − k − 1)/(k + 1)) − o(1) ≥ ½ log n + log(p/(k+1)) − o(1) when k + 1 ≤ p/2 … (as FAC-B L4.0(c)). Deletion
thresholds: by L0.3′, a null deletion is improving as soon as (1 + 1/n)M_T Z²(j; T) ≤ Δ_k − C_Q − 1; an addition is
non-improving as soon as (1 + 1/n)(1 + o(1)) M_T Z²(l; T) ≤ Δ_{k+1} − C_Q − 1. In standardized units (M_T ≤ 1 + o(1) always;
M_T ≤ ½(1 + 2/log n) when Φ(T) ≤ n/log n): **deletion improves if Z² ≤ Θ⁻_k := (Δ_k − C_Q − 1)/((1+1/n)M_T)** and
**addition fails if Z² ≤ Θ⁺_k := (Δ_{k+1} − C_Q − 1)/((1 + 1/n)(1+o(1))M_T)**, where Θ⁺_k ≥ (½ log n − O(1))·1 in general
and Θ⁺_k ≥ (1 − o(1))[log n + 2 log((2p − k − 1)/(k + 1))] − O(1) when Φ(T) ≤ n/log n.

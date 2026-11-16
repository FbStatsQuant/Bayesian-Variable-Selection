# R3 — Gaussian rows: bridge (B-R⁺⁺), Theorem START-R (T3⁺⁺)(b), IF-START⁺⁺

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Citations: BASE `path:lines` is a file of `Theory_work/Wave3/W3-START/` (v1.3.4); PARENT `path:lines` a file of
`Theory_work/Wave3/W3-START2/` (v1.4.1); a short citation `:a-b` continues the file cited last before it; `STATEMENT.md`
without prefix is this ticket's v1.5.
Statement proved: `STATEMENT.md` §2 (D4) (the remark "(L-R⁺) implies (L-R⁺⁺)"), (D5) (the remark on C₀ = 0); §3.2
[BR] (B-R⁺⁺) (i)–(iii) (`STATEMENT.md:217-225`), [START-R] (T3⁺⁺)(b) (i)–(iii) (`:226-240`), [IF-START] (T5⁺⁺) (`:241-246`).
Uses: BASE `lemmas/L9_BR.md` (L9.0–L9.6; changed steps copied below and marked [R-#]), BASE `lemmas/L8_TRANSFER.md`
(L8.0, Proposition L8.2), BASE `lemmas/L6_COROLLARIES.md` (Corollary L6.0′), BASE `lemmas/L10_INTERFACES.md` (L10.1),
PARENT `lemmas/P4_BR.md` (P4.1–P4.3; changed steps copied below), PARENT `lemmas/P1_LEADING.md` (P1.7, P1.8), and, for
the fixed-design clause of IF-START⁺⁺ only, `lemmas/R1_VIS.md` ((T1⁺⁺)(b)).
No registry claim is consumed beyond `STATEMENT.md` §5.

## R3.0 Setting, constants, and the two remarks of §2

Setting R (BASE `STATEMENT.md:69-72`) with p > s₀ for all large n (so s₀ ≥ 1 and p ≤ n^A). Notation and constants of
BASE `lemmas/L9_BR.md:12-20`: N := n − 1; M = Δ_hi := s₀²θ_hi²; Δ_lo := (c_Σ/2)θ_lo²; a̲ := σ²/(σ² + Δ_hi);
z̄_n² := 2 log(2^{21}) + 2A log n + 2 log log n ≥ z_n²; pc(·); F(g, a) and (F1), (F2) of BASE `:65-70`. "For n large"
means n ≥ a threshold depending only on the fixed constants (A, θ_lo, θ_hi, σ², c_Σ, a_V, s₀, C_L, κ_H, C₀), on the
sequence r_n and — wherever the envelope of (D4) is used — on **n_H**, an index such that log H̄_n ≤ κ_H√log n for every
n ≥ n_H ((D4) asks this only for all large n, so n_H depends on the sequence H̄_n) [R-10]; never on Q, and never on ε
unless ε is displayed. The constants (C_B, C_R, C₇, C₈, C₉) do not depend on n_H.

**(D4) remark.** (L-R⁺) (PARENT `STATEMENT.md:63-73`) asks |H_l| ≤ (log n)^{κ_Q}, κ_Q ≥ 1 fixed. Put H̄_n := (log n)^{κ_Q}.
For any κ_H > 0, κ_Q log log n ≤ κ_H√log n for all large n, i.e. log H̄_n ≤ κ_H√log n. The other requirements of
(L-R⁺⁺) are those of (L-R⁺) word for word. So (L-R⁺) implies (L-R⁺⁺) with this H̄_n and any κ_H > 0. ∎
**(D5) remark.** Let C₀ = 0. If (L-gain-0) holds, take U = ∅ (∅ ⊊ S₀, as s₀ ≥ 1): Cov(W_l, W_j) = 0 for l ∉ S₀, j ∈ S₀.
Conversely, if Cov(W_l, W_j) = 0 for all l ∉ S₀, j ∈ S₀, then for U ⊊ S₀ (Σ_{UU} invertible by (FL-R16)):
Cov(W_l, W_j | W_U) = Σ_{lj} − Σ_{lU}Σ_{UU}⁻¹Σ_{Uj} = 0 − 0, since Σ_{lU} = 0 (U ⊆ S₀). If (L-R⁺⁺) holds with Q = S₀ and
C_L = 0, then for l ∉ S₀ and U ⊊ S₀ we have U ⊆ S₀ ⊆ H_l, so U₀ = U ∩ H_l = U, and (L-gain-R) gives
Cov(W_l, W_j | W_U) = 0 for j ∈ S₀ ∖ U: (L-gain-0) with C₀ = 0. ∎

**N̄_n.** N̄_n := (1 + H̄_n)^{15}. A set H_l with |H_l| ≤ H̄_n has at most Σ_{k≤15}C(|H_l| − 1, k) ≤ (1 + H̄_n)^{15} subsets
U₀ ⊆ H_l ∖ {l} with |U₀| ≤ 15; so the reference family I_l of BASE `lemmas/L9_BR.md:94` has |I_l| ≤ N̄_n. Since H_l ⊇ {l} ∪ S₀,
H̄_n ≥ 2 whenever Q ≠ [p], and then N̄_n ≤ (2H̄_n)^{15} ≤ 2^{15}exp(15κ_H√log n) for every n ≥ n_H. (If Q = [p] the sums over
l ∉ Q below are empty and 𝔏_n(Q) = 0.)

## R3.1 (B-R⁺⁺)(i): BASE L9.1–L9.6 under (L-R⁺⁺)

PARENT `lemmas/P4_BR.md:16-34` lists, step by step, what BASE L9.1–L9.6 use of Q and (H_l): the bound |H_l| ≤ (log n)^{κ_Q}
enters only through the count N_ref of BASE `lemmas/L9_BR.md:95`, in P(Eᶜ) (`:130`) and in E Ψ_n ≤ N_refΦ_n (`:138`); the
cardinality of Q enters nowhere. Every other step (L9.1 covariance event and (c1)–(c4); L9.2 energy, floors, (V-c);
L9.3; L9.4 localisation, which uses only S₀ ⊆ H_l and (L-loc-R); L9.5, which uses S₀ ⊆ H_l and (L-gain-R) for a fixed
reference pair) holds under (L-R⁺⁺) verbatim, with the same thresholds. The changed lines:

**[R-1]** (replaces BASE `:95`, second line) |I_l| ≤ N̄_n.
**[R-2]** (replaces BASE `:130`) E := E_cov ∩ ⋂{E_R(l, U₀) ∩ E_ξ(l, U₀) : l ∉ Q, U₀ ∈ I_l};
  P(Eᶜ) ≤ 4n^{−2} + p·N̄_n·3n^{−(A+2)} ≤ (4 + 3N̄_n)n^{−2} → 0,
because N̄_n ≤ 2^{15}e^{15κ_H√log n} = n^{o(1)}.
**[R-3]** (replaces BASE `:138`, last clause) E Ψ_n ≤ N̄_n·Φ_n (L9.5 for each of the ≤ p·N̄_n pairs, divided by p).
**[R-4]** (replaces BASE `:140`) for every λ > 0 and n large: P(𝔏_n(Q) > √(2/π)z̄_n + e·λ·N̄_n·Φ_n) ≤ P(Eᶜ) + 1/λ.   (R3.1)
**[R-5]** (replaces BASE `:141-143`) *General C_L.* z̄_n² ≤ (2A + 1) log n for n large, so
Φ_n = √(2/a̲)√(2/π)z̄_n·exp(η_nz̄_n²/a̲ + 2d̄z̄_n/a̲ + d̄²/a̲) ≤ exp((2d̄√(2A + 1)/a̲)√log n)·B_n, B_n := √(2/a̲)√(2/π)z̄_n·e^{η_nz̄_n²/a̲ + d̄²/a̲}
= O(√log n) (η_nz̄_n² → 0). Take λ = log n in (R3.1). Then
√(2/π)z̄_n + e·log n·N̄_n·Φ_n ≤ √(2/π)z̄_n + exp((2d̄√(2A + 1)/a̲ + 15κ_H)√log n)·e·2^{15}·log n·B_n ≤ exp(C_B√log n),
  **C_B := 2d̄√(2A + 1)/a̲ + 15κ_H + 1,**
for n large (e·2^{15}·log n·B_n ≤ ½e^{√log n} and √(2/π)z̄_n ≤ ½e^{√log n} eventually). Hence
  **P(𝔏_n(Q) > exp(C_B√log n)) ≤ (4 + 3N̄_n)n^{−2} + 1/log n → 0**   (n large).                                (R3.2)
C_B depends only on the fixed constants and κ_H (d̄ = √2s₀C_L/c_Σ^{3/2}, BASE `:102`, `:107`).
Together with BASE L9.1–L9.2 (E, floor λ_min(R̂_T) ≥ φ₀² := c_Σ/2 for 1 ≤ |T| ≤ 16, hence (GF-16); (V-c) for every fixed
c_V — hence (V-cp) of (D3) for every fixed c_V, since δ²_{U,j} ≥ (c_V + 2A)τ²_U log n ≥ τ²_U(c_V log n + 2 log p)) this is
(B-R⁺⁺)(i). ∎

## R3.2 (B-R⁺⁺)(ii): C_L = 0

**[R-6]** (replaces BASE `:144-146`) If C_L = 0 then d̄ = 0 and, for n large, Φ_n ≤ 2√(2/a̲)√(2/π)z̄_n (η_nz̄_n²/a̲ ≤ log 2).
By (R3.1), for every λ ≥ 1 and n large:
  √(2/π)z̄_n + eλN̄_nΦ_n ≤ √((2A + 1) log n)·(1 + 2e√2/√a̲)·λN̄_n ≤ C₇·λ·N̄_n·√log n,   C₇ := 9√((2A + 1)/a̲)
(√(2/π) < 1, λN̄_n ≥ 1, a̲ ≤ 1, 1 + 2e√2 < 9). So
  **P(𝔏_n(Q) > C₇λN̄_n√log n) ≤ (4 + 3N̄_n)n^{−2} + 1/λ**   for every λ ≥ 1 and n large,                      (R3.3)
i.e. 𝔏_n(Q) = O_P(N̄_n√log n) (a tightness statement, from a first moment and Markov's inequality, as BASE `:146-148`). ∎

## R3.3 (B-R⁺⁺)(iii): the sharp leading functional with 2^{s₀} reference sets (new step)

Hypotheses here: Setting R, p > s₀ (for the n considered), (FL-R16), (L-gain-0) with constant C₀. Neither (V-R) nor
(L-R⁺⁺) is used, nor E_cov. Default levels; 𝔏^♯_n = p⁻¹Σ_{l∉S₀}max{J_{z_n}(δ_{U,l}, τ_U) : U ⊊ S₀, |U| ≤ 15} (PARENT
`STATEMENT.md:53-55`).

**Step 1 (representation; deterministic).** Fix l ∉ S₀ and U ⊊ S₀ with |U| ≤ 15. Put μ̃ := (I − P_U)μ. If μ̃ = 0 then
δ_{U,l} = u_{U,l}ᵀμ̃ = 0 and τ_U = σ, so J_{z_n}(δ_{U,l}, τ_U) = √(2/π)z_n ((J3), BASE `lemmas/L3_LEAK.md:20`); put g_{U,l} := 0,
a_U := 1, so that J_{z_n} = F(0, 1). If μ̃ ≠ 0 and (I − P_U)x_l ≠ 0, the identities of BASE `lemmas/L9_BR.md:62-65` hold as
algebra (they use no event): with Δ_U = ‖μ̃‖²/N, ρ̂_{U,l} := ⟨(I − P_U)x_l, μ̃⟩/(‖(I − P_U)x_l‖‖μ̃‖), g_{U,l} := √Nρ̂_{U,l} and
a_U := σ²/τ²_U: δ_{U,l} = ‖μ̃‖ρ̂_{U,l} = √Δ_U·g_{U,l}, (δ_{U,l} + σZ)/τ_U = √(1 − a_U)g_{U,l} + √a_UZ, and
**J_{z_n}(δ_{U,l}, τ_U) = F(g_{U,l}, a_U).** Always a_U ≥ a̲, since Δ_U ≤ ‖μ‖²/N ≤ Δ_hi (‖μ‖ ≤ Σ_{j∈S₀}|θ*_j|‖x_j‖ ≤ s₀θ_hi√N).
(The event (I − P_U)x_l = 0 has probability 0: the rows of (CW_{U∪{l}}) span a space of dimension |U| + 1 ≤ 16 a.s. once
N ≥ 16, by λ_min(Σ_{U∪{l}}) ≥ c_Σ > 0; on it δ_{U,l} := 0 and the term is again √(2/π)z_n ≤ F-bound below.)

**Step 2 (conditional law; BASE L9.5 with U₀ = U, D = S₀).** [R-7] In BASE `lemmas/L9_BR.md:94-123` take the reference
pair (l, U₀) with U₀ := U ⊊ S₀; then D := U₀ ∪ S₀ = S₀, l ∉ D, |D ∪ {l}| = s₀ + 1 ≤ 16 + s₀. Every step of BASE `:96-123`
applies verbatim with one change in the bound on γ²: the population regression
W_l − m_l1 = (W_U − 1m_Uᵀ)γ¹ + (W_{S₀∖U} − 1m_{S₀∖U}ᵀ)γ² + e, e with iid N(0, τ_e²) entries independent of W_{S₀},
τ_e² = Var(W_l | W_{S₀}) ∈ [c_Σ, 1] ((FL-R16) on S₀ ∪ {l}), and γ² = Cov(W_{S₀∖U} | W_U)⁻¹Cov(W_{S₀∖U}, W_l | W_U). By (L-gain-0)
each coordinate of Cov(W_{S₀∖U}, W_l | W_U) is at most C₀(n log n)^{−1/2} in absolute value, and
λ_min(Cov(W_{S₀∖U} | W_U)) ≥ c_Σ ((FL-R16): a Schur complement in Σ_{S₀}). Hence
  **‖γ²‖ ≤ √s₀·C₀/(c_Σ√(n log n)),**   and on CN := {‖CW_j‖² ≤ 2N for all j ∈ S₀}:
  ‖m‖ ≤ ‖γ²‖√s₀√(2N) ≤ m̄⁰_n := √2·s₀C₀/(c_Σ√log n),   |d₀| ≤ d̄⁰_n := m̄⁰_n/√c_Σ
(m := ΠW_{S₀∖U}γ², d₀ := ⟨m, v⟩/τ_e as in BASE `:101-107`; N ≤ n). The conditioning σ-field is 𝒲 := σ(W_{S₀}) for every pair
(l, U) with U ⊊ S₀; the innovation e is independent of it (BASE `:125-126`). The events E_R(l, U) := {R ≥ N(1 − η_n)} and
the bounds P(E_R(l, U)ᶜ | 𝒲) ≤ n^{−(A+2)} are those of BASE `:110-112`. Lemma L9.5 (BASE `:114-123`, whose proof uses only
a ≥ a̲, (F1), (9.1), η_n ≤ a̲/2 and |d₀| ≤ d̄ on CN) gives, with d̄⁰_n in place of d̄:
  **E[F(g_{U,l}, a_U)·1_{E_R(l,U)}·1_{CN}] ≤ Φ⁰_n := √(2/a̲)·√(2/π)·z̄_n·exp(η_nz̄_n²/a̲ + 2d̄⁰_nz̄_n/a̲ + (d̄⁰_n)²/a̲).**
(On {μ̃ = 0} the integrand is F(0, 1) = √(2/π)z_n ≤ Φ⁰_n.) Since z̄_n ≤ √((2A + 1) log n) for n large,
2d̄⁰_nz̄_n/a̲ ≤ C₈ := 2√2·s₀C₀√(2A + 1)/(c_Σ^{3/2}a̲), and η_nz̄_n²/a̲ + (d̄⁰_n)²/a̲ ≤ 1 for n large. So
  **Φ⁰_n ≤ C₉·√log n,   C₉ := √(2/a̲)·√(2A + 1)·e^{C₈+1}**   (n large).

**Step 3 (event and Markov).** E⁰ := CN ∩ ⋂{E_R(l, U) : l ∉ S₀, U ⊊ S₀, |U| ≤ 15}. ‖CW_j‖²/1 ~ χ²_N (unit variances), and
by Laurent–Massart with x = N/8 (2√(N·N/8) + N/4 < N), P(‖CW_j‖² > 2N) ≤ e^{−N/8}; with at most p·2^{s₀} pairs,
  P((E⁰)ᶜ) ≤ s₀e^{−(n−1)/8} + 2^{s₀}·p·n^{−(A+2)} ≤ s₀e^{−(n−1)/8} + 2^{s₀}n^{−2} → 0.
Put Ψ⁰_n := p⁻¹Σ_{l∉S₀}Σ_{U⊊S₀, |U|≤15}F(g_{U,l}, a_U)1_{E_R(l,U)}1_{CN} (convention of Step 1 on {μ̃ = 0}). All terms are ≥ 0
and there are at most 2^{s₀} − 1 sets U, so on E⁰: 𝔏^♯_n ≤ Ψ⁰_n (a maximum over U is at most the sum), and
E Ψ⁰_n ≤ 2^{s₀}Φ⁰_n ≤ 2^{s₀}C₉√log n. By Markov's inequality, for every λ ≥ 1 and n large:
  **P(𝔏^♯_n > λ·2^{s₀}C₉·√log n) ≤ s₀e^{−(n−1)/8} + 2^{s₀}n^{−2} + 1/λ.**                                         (R3.4)
So 𝔏^♯_n = O_P(√log n) (tightness). This is (B-R⁺⁺)(iii). ∎
*Where the count N_ref disappears.* The leading functional maximises over proper subsets of S₀ only, so no
localisation (BASE L9.4) is needed — the maximisation already ranges only over proper subsets of S₀ — and the
reference family is the 2^{s₀} − 1 sets U ⊊ S₀ themselves (triage row
W3-START:START-R, `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md:57`). The shift d̄⁰_n = O(1/√log n) costs only the constant e^{C₈}.

## R3.4 (T3⁺⁺)(b)(i): the main display

PARENT `lemmas/P4_BR.md:47-69` (P4.2), with these changes:
**[R-8]** C_R := C_B + 1 with C_B of [R-5]; the design set 𝒳_n uses 𝔏_n(Q) ≤ exp(C_B√log n) with this C_B, and
P(X^r ∉ 𝒳_n) → 0 by BASE L9.1, L9.2 and (R3.2) in place of PARENT (4.2).
Everything else is verbatim: the fixed constants for (T1)(d) (A, M = s₀²θ_hi², g_* = c_Σ/2, s₀, (V-c) with c_V := 2A + 4,
κ_V = 3/2) are those of the version-1.3.4 bridge, so BASE Proposition L8.2(i) in the form of Corollary L6.0′ with κ = 1
(BASE `lemmas/L8_TRANSFER.md:37-50`, BASE `lemmas/L6_COROLLARIES.md:19-26`) applies at each n as in PARENT `lemmas/P4_BR.md:59-67`; the threshold
n_R depends only on the fixed constants, κ_H (through C_B) and n_H, not on Q. So
  **P(1 − π₀(𝓛(Q)) > (|Q| + 1)n^{−1/2}exp(C_R√log n)) ≤ 4/log n + 1/(32 log n) + P(X^r ∉ 𝒳_n) → 0.**
The consequences for Q = S₀ and for |Q| ≤ n^{1/2−ε_Q} are PARENT `lemmas/P4_BR.md:71-74` verbatim. ∎
(The designs of 𝒳_n satisfy (V-c) at c_V = 2A + 4, hence also (V-cp); no result of `lemmas/R1_VIS.md` is needed here.)

## R3.5 (T3⁺⁺)(b)(ii): C_L = 0

PARENT `lemmas/P4_BR.md:78-90` (P4.3), with: **[R-9]** b^Q_n := (|Q_n| + 1)·N̄_n·n^{−1/2}·√log n; D_ε := C₇λ with
λ := 4/ε (C₇ of [R-6]); 𝒳_n^ε := 𝒳_n with its last condition replaced by 𝔏_n(Q) ≤ D_εN̄_n√log n. By BASE L9.1, L9.2 and
(R3.3): limsup P(X^r ∉ 𝒳_n^ε) ≤ 1/λ = ε/4 ((4 + 3N̄_n)n^{−2} → 0). On 𝒳_n^ε: ϱ_n(Q) ≤ D_ε·b^Q_n. For n ≥ 3,
b^Q_n ≥ n^{−1/2} ≥ n^{−1} (N̄_n ≥ 1, √log n ≥ 1). The rest — T_ε := max(D_ε/c₀, C·D_ε + 1) with C, c₀, n₀ of BASE
Proposition L5.2 for (ε/4, κ = 1), the two cases T_εb^Q_n ≥ 1 (empty event) and < 1 (BASE L8.2(i)) — is PARENT `:84-90`
verbatim. Hence 1 − π₀(𝓛(Q)) = O_P((|Q| + 1)·N̄_n·√(log n/n)). With H̄_n = (log n)^{κ_Q}: N̄_n ≤ 2^{15}(log n)^{15κ_Q}
(for n with (log n)^{κ_Q} ≥ 1), which is the clause C_L = 0 of PARENT `STATEMENT.md:138-139`. ∎

## R3.6 (T3⁺⁺)(b)(iii): o₀ = O_P(√(log n/n))

Hypotheses: Setting R, p > s₀ for all large n, (FL-R16), (V-R), (L-R⁺⁺) with Q = S₀, and (L-gain-0). Default levels
(b_n ≤ 1/(32 log n), BASE `lemmas/L3_LEAK.md:31`).
Fix ε ∈ (0, 1); put λ := 8/ε and D⁰_ε := λ·2^{s₀}C₉. Let **𝒳⁰_n** be the set of designs with: (c1)–(c4) of BASE L9.1; (V-c) at
level c_V := 2A + 4; 𝔏_n(S₀) ≤ exp(C_B√log n); and 𝔏^♯_n ≤ D⁰_ε√log n. By BASE L9.1–L9.2 (P(E_covᶜ) ≤ 4n^{−2}; (V-c) on
E_cov for n large), (R3.2) with Q = S₀, and (R3.4):
  limsup_n P(X^r ∉ 𝒳⁰_n) ≤ 1/λ = ε/8.
Every design of 𝒳⁰_n is admissible at n in the sense of BASE `lemmas/L8_TRANSFER.md:22-25` with the constants
(A, M = s₀²θ_hi², g_* = c_Σ/2, s₀, c_V = 2A + 4) (BASE `lemmas/L9_BR.md:158-160`; Q = S₀ deterministic, |S₀| = s₀ < p ≤ n^A,
S₀ ⊆ Q, |Q| = s₀ ≤ K for n large), with the default h. On 𝒳⁰_n:
  ϱ_n(S₀) = (s₀ + 1)n^{−1/2}𝔏_n(S₀) ≤ ϱ̄_n := (s₀ + 1)n^{−1/2}e^{C_B√log n} → 0,
  n^{−1/2}𝔏^♯_n + n^{−1}𝔏_n(S₀)² ≤ D⁰_ε√(log n/n) + n^{−1}e^{2C_B√log n} ≤ r̄_n := (D⁰_ε + 1)√(log n/n)
for n large (n^{−1/2}e^{2C_B√log n} ≤ √log n eventually; the threshold depends on C_B only).
Let C^♯ := C^♯(ε/8), c₀ := c₀(ε/8), n₀ := n₀(ε/8, 1) be the constants of PARENT Proposition P1.4 (PARENT
`lemmas/P1_LEADING.md:82`) for (ε/8, κ = 1) (κ = 1 < κ_V = 3/2). For n ≥ n₀ with ϱ̄_n ≤ c₀ (all large n), PARENT P1.7
(`:147-151`: BASE Proposition L8.2(ii) with 𝔏^♯_n) applied with 𝒳 := 𝒳⁰_n, ϱ̄ := ϱ̄_n, b̄ := 1/(32 log n), r̄ := r̄_n gives
  P(o₀ > C^♯·r̄_n + n^{−1}) ≤ ε/8 + 1/(32 log n) + P(X^r ∉ 𝒳⁰_n),
whose limsup is ≤ ε/4 < ε. Since C^♯r̄_n + n^{−1} ≤ T⁰_ε√(log n/n) with T⁰_ε := C^♯(D⁰_ε + 1) + 1, we get
limsup_n P(o₀ > T⁰_ε√(log n/n)) ≤ ε for every ε ∈ (0, 1):
  **o₀ = O_P(√(log n/n)),   and 1 − π₀(S₀) = o₀/(1 + o₀) ≤ o₀ = O_P(√(log n/n)).** ∎
(Optimality up to √log n: o₀ ≥ ½(n + 1)^{−1/2} on every data set with s₀ < K, by (T0), BASE `STATEMENT.md:241-243`.)
*Where each hypothesis is used.* (L-gain-0): only (R3.4). (L-R⁺⁺) with Q = S₀ (any C_L): only 𝔏_n(S₀) ≤ e^{C_B√log n}, which
controls the second-order term n^{−1}𝔏_n(S₀)² and the smallness ϱ_n(S₀) ≤ c₀. (V-R): (V-c) on the design set. (FL-R16):
floors, τ_e², ‖γ²‖.

## R3.7 IF-START⁺⁺

**(a) Fixed design.** PARENT `lemmas/P1_LEADING.md:155-158` (P1.8(a)) with (T1⁺⁺)(b) (`lemmas/R1_VIS.md`) in place of
(T1⁺)(b): the argument uses only the conclusion o₀ = O_P(n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)²) + o_P(n^{−κ₁}) for some
κ₁ ∈ (κ, κ_V), and 0 ≤ 1_𝒜o₀ ≤ o₀.
**(b) Gaussian rows, (T3⁺⁺)(b) with Q = S₀.** BASE `lemmas/L10_INTERFACES.md:16-18` with (T3⁺⁺)(b)(i) (R3.4) in place of
(T3)(b): with probability → 1, 1 − π₀(S₀) ≤ ρ_n := (s₀ + 1)n^{−1/2}e^{C_R√log n} → 0, and on that event, for ρ_n ≤ ½,
o₀ ≤ 2ρ_n; so 1_𝒜o₀ = O_P(n^{−1/2}e^{C_R√log n}).
**(c) Under (T3⁺⁺)(b)(iii).** 0 ≤ 1_𝒜o₀ ≤ o₀ = O_P(√(log n/n)) by R3.6: r_n := √(log n/n).
**(d) What the consumer gets.** BASE `:19-24`, unchanged (with these deterministic rates r_n ↓ 0). ∎

## R3.8 Changed lines, summary
[R-1]–[R-6]: BASE `lemmas/L9_BR.md:95`, `:130`, `:138`, `:140`, `:141-143`, `:144-146` (N̄_n for N_ref; C_B with 15κ_H; C₇).
[R-7]: BASE `:94-123` instantiated at U₀ = U ⊊ S₀ with (L-gain-0) (new step R3.3). [R-8]: PARENT `lemmas/P4_BR.md:47-69`
(C_R, (R3.2)). [R-9]: PARENT `:78-90` (b^Q_n with N̄_n). R3.6 and R3.7(c) are new compositions of cited results.

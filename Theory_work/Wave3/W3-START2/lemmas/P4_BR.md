# P4 — Gaussian rows with a leakage set of any size ≤ K: bridge (B-R⁺) and Theorem START-R (T3⁺)(b)

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Citations: BASE `path:lines` is a file of the base ticket; a short citation `:a-b` continues the file cited last before it.
Statement proved: `STATEMENT.md` §2 (D2) (the remark "(L-R) implies (L-R⁺)"); §3.2 (B-R⁺) and (T3⁺)(b). BASE :=
`Theory_work/Wave3/W3-START/`. Uses: BASE `lemmas/L9_BR.md` (L9.0–L9.6, every step; L9.7 is replaced by P4.2–P4.3 below),
BASE `lemmas/L8_TRANSFER.md` (L8.0, Proposition L8.2), BASE `lemmas/L6_COROLLARIES.md` (Corollary L6.0′), and
`lemmas/P1_LEADING.md` Proposition P1.4(i) (= BASE Proposition L5.2(i), the first display of (T1⁺)(d)).

Setting R with p > s₀ for all large n; (FL-R16), (V-R), (L-R⁺) with Q = Q_n, (H_l)_{l∉Q}, C_L, r_n, κ_Q. Notation and
constants of BASE `lemmas/L9_BR.md:12-20`. (L-R) is (L-R⁺) together with |Q| ≤ (log n)^{κ_Q} (BASE `STATEMENT.md:163-167`),
so (L-R) implies (L-R⁺).

## P4.1 The bridge (B-R⁺): where BASE L9.1–L9.6 use the leakage set

**Claim.** Every statement of BASE L9.1–L9.6 (BASE `lemmas/L9_BR.md:22-152`) holds under (L-R⁺) in place of (L-R), with the
same constants and the same thresholds; none of the thresholds depends on Q.

*Proof.* (L-R) and (L-R⁺) differ only in the requirement |Q| ≤ (log n)^{κ_Q}. Each step of L9.1–L9.6 is listed with
what it uses of Q.
| step (BASE `lemmas/L9_BR.md`) | what it uses of Q and (H_l) |
|---|---|
| L9.1, covariance event and (c1)–(c4) (`:24-42`) | nothing (p ≤ n^A; sets of size ≤ 16 + s₀) |
| L9.2, (E), floors, (V-c) (`:46-55`) | nothing (j ∈ S₀; (V-R)) |
| L9.3, the terms as functions of g_{U,l}, a_U (`:59-70`) | l ∉ Q only |
| L9.4, localisation (`:74-90`) | l ∉ Q; S₀ ⊆ H_l; (L-loc-R) |
| L9.5, reference pairs (`:94-123`) | l ∉ Q; \|H_l\| ≤ (log n)^{κ_Q} (the count N_ref, `:95`); S₀ ⊆ H_l; (L-gain-R) |
| L9.6, the event E and its probability (`:130`) | the number of columns l ∉ Q is at most p |
| L9.6, averaging over l ∉ Q (`:136-140`) | at most p terms, each divided by p: E Ψ_n ≤ N_ref·Φ_n |
| L9.6 (a), (b) (`:141-148`) | nothing (z̄_n, Φ_n, N_ref, λ) |
The cardinality of Q is not used in any of them. "For n large" in these steps is a threshold depending only on the
fixed constants and on the sequence r_n (`:20`): the conditions are h_n ≤ ¼ and (17 + s₀)·3h_n ≤ c_Σ/2 (`:32`), the
visibility level (`:55`), q_a, q_d ≤ ¼ and ι_n ≤ 1 (`:86`, `:132`), η_n ≤ a̲/2 (`:114`), ς′_n ≤ 1 and z̄_n² ≤ (2A + 1) log n
(`:139-141`). If Q = [p] the sums over l ∉ Q are empty and 𝔏_n(Q) = 0. ∎

**Consequence: (B-R⁺).** As in BASE `lemmas/L9_BR.md:150-152`: with probability → 1 the design satisfies (E) (energy
bound with M = s₀²θ_hi²; the other parts by assumption), λ_min(R̂_T) ≥ φ₀² := c_Σ/2 for 1 ≤ |T| ≤ 16 (hence (GF-16)), (V-c)
for every fixed c_V, and 𝔏_n(Q) ≤ exp(C_B√log n), C_B := 2d̄√(2A + 1)/a̲ + 1. If C_L = 0:
𝔏_n(Q) = O_P((log n)^{15κ_Q+1/2}) in the form (BASE `:144-145`)
  P(𝔏_n(Q) > C₆·λ·(log n)^{15κ_Q+1/2}) ≤ P(Eᶜ) + 1/λ for every λ ≥ 1 and n large,   P(Eᶜ) ≤ (4 + 3N_ref)n^{−2}.          (4.1)
More precisely, by (9.2) with λ = log n (BASE `:140-143`), for n large:
  P(𝔏_n(Q) > exp(C_B√log n)) ≤ (4 + 3N_ref)n^{−2} + 1/log n.                                                          (4.2)
The right sides of (4.1), (4.2) do not depend on Q. ∎

## P4.2 Theorem START-R (T3⁺)(b): the main display

**Claim.** With **C_R := C_B + 1** and a_n := (|Q_n| + 1)·n^{−1/2}·exp(C_R√log n): P(1 − π₀(𝓛(Q)) ≤ a_n) → 1.

*Proof.* Default levels: b_n(h) ≤ 1/(32 log n) (BASE `lemmas/L3_LEAK.md:31`).
*Design set* (as BASE `lemmas/L9_BR.md:158-160`). Fixed constants for (T1⁺)(d): A, M = s₀²θ_hi², g_* = c_Σ/2, s₀, and (V-c)
with c_V := 2A + 4, so κ_V = 3/2. 𝒳_n := {designs with: (c1)–(c4) of L9.1; (V-c) at level c_V; 𝔏_n(Q) ≤ exp(C_B√log n)}.
By L9.1, L9.2 and (4.2): P(X^r ∉ 𝒳_n) → 0. Every design of 𝒳_n is admissible at n in the sense of BASE
`lemmas/L8_TRANSFER.md:22-25` (p ≤ n^A; s₀ < p; S₀ ⊆ Q and |Q| ≤ K by (L-R⁺); ‖μ‖² ≤ Mn; (GF-16); (V-c); θ*, Q, h
deterministic). On 𝒳_n, by the definition of ϱ_n (BASE `STATEMENT.md:120`):
  ϱ_n(Q) = (|Q| + 1)·n^{−1/2}·𝔏_n(Q) ≤ (|Q| + 1)·n^{−1/2}·exp(C_B√log n) = a_n·e^{−√log n}.                                  (4.3)
*Threshold.* Let c_{0,n}, C_n, n**(κ) be those of BASE Corollary L6.0′ (BASE `lemmas/L6_COROLLARIES.md:19-26`; C_n = 43s₀′c_L log n,
1/c_{0,n} = 64s₀′c_L log n). Let n_R be such that for all n ≥ n_R: n ≥ n**(1), e^{−√log n} ≤ c_{0,n}, and
C_n·e^{−√log n} + n^{−1/2} ≤ 1. n_R depends only on the fixed constants (not on the sequence Q_n).
*Two cases at a fixed n ≥ n_R.*
(i) a_n ≥ 1. Then {1 − π₀(𝓛(Q)) > a_n} is empty, because 1 − π₀(𝓛(Q)) ≤ 1 (also under the convention of BASE
`lemmas/L8_TRANSFER.md:16-20`).
(ii) a_n < 1. Put ϱ̄ := a_n·e^{−√log n} < e^{−√log n} ≤ c_{0,n}. By (4.3), ϱ_n(Q) ≤ ϱ̄ on 𝒳_n. BASE Proposition L8.2(i) in the form
of Corollary L6.0′ with κ = 1 < κ_V (BASE `lemmas/L8_TRANSFER.md:37-50`; an inequality at the fixed n) gives
  P(1 − π₀(𝓛(Q)) > C_n·ϱ̄ + n^{−1}) ≤ 4/log n + 1/(32 log n) + P(X^r ∉ 𝒳_n).
Since a_n ≥ n^{−1/2}: C_n·ϱ̄ + n^{−1} ≤ a_n·[C_n·e^{−√log n} + n^{−1/2}] ≤ a_n.
In both cases, for every n ≥ n_R:
  **P(1 − π₀(𝓛(Q)) > a_n) ≤ 4/log n + 1/(32 log n) + P(X^r ∉ 𝒳_n) → 0.** ∎

No assumption is made on how the two cases alternate along the sequence: the bound holds at each n.

**Consequences.** (1) Q = S₀: a_n = (s₀ + 1)n^{−1/2}exp(C_R√log n) ≤ n^{−c} eventually for every c < ½, so
P(π₀(S₀) ≥ 1 − n^{−c}) → 1; p ≤ n^A is the only restriction on p (BASE `lemmas/L9_BR.md:166-167`). (2) If |Q| ≤ n^{1/2−ε_Q}
with a fixed ε_Q ∈ (0, ½): a_n ≤ 2n^{−ε_Q}exp(C_R√log n) ≤ n^{−c} eventually for every c < ε_Q, so
P(π₀(𝓛(Q)) ≥ 1 − n^{−c}) → 1.

## P4.3 The clause C_L = 0

**Claim.** If C_L = 0: 1 − π₀(𝓛(Q)) = O_P(b^Q_n), b^Q_n := (|Q_n| + 1)·n^{−1/2}·(log n)^{15κ_Q+1/2}; that is, for every ε ∈ (0, 1)
there is T_ε < ∞ with limsup_n P(1 − π₀(𝓛(Q)) > T_ε·b^Q_n) ≤ ε.

*Proof.* Fix ε ∈ (0, 1), λ := 4/ε, D_ε := C₆λ. Let 𝒳_n^ε be 𝒳_n with its last condition replaced by
𝔏_n(Q) ≤ D_ε(log n)^{15κ_Q+1/2}. By L9.1, L9.2 and (4.1): limsup P(X^r ∉ 𝒳_n^ε) ≤ 1/λ = ε/4. Designs of 𝒳_n^ε are admissible,
and on 𝒳_n^ε: ϱ_n(Q) ≤ D_ε·b^Q_n.
Let C := C(ε/4), c₀ := c₀(ε/4), n₀ := n₀(ε/4, 1) be the constants of BASE Proposition L5.2 for (ε/4, κ = 1), and
  **T_ε := max(D_ε/c₀, C·D_ε + 1).**
Fix n ≥ max(n₀, 3) (so b^Q_n ≥ n^{−1/2} ≥ n^{−1}).
(i) T_ε·b^Q_n ≥ 1: the event {1 − π₀(𝓛(Q)) > T_ε·b^Q_n} is empty.
(ii) T_ε·b^Q_n < 1: put ϱ̄ := D_ε·b^Q_n < D_ε/T_ε ≤ c₀. BASE Proposition L8.2(i) with (ε/4, κ = 1) at this n:
P(1 − π₀(𝓛(Q)) > C·ϱ̄ + n^{−1}) ≤ ε/4 + 1/(32 log n) + P(X^r ∉ 𝒳_n^ε), and C·ϱ̄ + n^{−1} ≤ (C·D_ε + 1)·b^Q_n ≤ T_ε·b^Q_n.
In both cases P(1 − π₀(𝓛(Q)) > T_ε·b^Q_n) ≤ ε/4 + 1/(32 log n) + P(X^r ∉ 𝒳_n^ε), whose limsup is ≤ ε/2 < ε. ∎

(The rate b^Q_n need not tend to zero. The right side of the main display can be ≥ 1 at indices where b^Q_n is small;
the two displays are separate statements, each with its own split.)

## P4.4 Where the size of Q matters
BASE L9.7 used |Q| ≤ (log n)^{κ_Q} at one place: to have ϱ̄_n → 0, hence ϱ̄_n ≤ c_{0,n} eventually (BASE
`lemmas/L9_BR.md:161-162`, and `:170` for the clause C_L = 0). P4.2–P4.3 replace "eventually" by a case distinction at
each n: where the claimed bound is ≥ 1 it is trivial, and where it is < 1 the smallness needed by (T1⁺)(d) follows
from it. The first display of (T1⁺)(d) is uniform over all Q with S₀ ⊆ Q, |Q| ≤ K: the factor |Q| + 1 is inside
ϱ_n(Q; h) and the constants of BASE L5.2 depend only on (ε, κ) and the fixed constants (BASE
`lemmas/L8_TRANSFER.md:52-53`). The bound on the reference sets, |H_l| ≤ (log n)^{κ_Q}, is still used (N_ref). ∎

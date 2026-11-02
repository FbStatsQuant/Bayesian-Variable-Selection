# W2-T26 — T26 (i)–(ii) restated: evidence and PIP consistency in the favourable regime

Candidate proof, written by cloud run W2-T26 (2026-11-02). Not reviewed, not adopted. Status words as in
`theory_campaign/PROTOCOL.md`. Notation of `Docs/Theory/theorems/00_COMMON.md`; new symbols are defined in §0.

---

## 0. Setting, new symbols, standing idealisations

Everything is indexed by n (regime R1/R4 of 00_COMMON §2: n → ∞, s₀ fixed, p = p_n ≤ n^A, actual budgets).
Index n is suppressed when harmless.

**Data-level quantities** (functions of (X, y) only; defined when S₀ ∈ Ω, i.e. s₀ ≤ K):
- π₀, q_φ = γ_φ/Z̄_φ, π = q₁ (00_COMMON §2).
- δ₁ = 1 − π(S₀); u_π = δ₁/π(S₀); ρ* = min{1, (B+3)u_π} (00_COMMON §2).
- **Δ_n := 1 − inf_{φ∈[0,1]} q_φ(S₀)** (the bridge's worst-case deficit at the truth; as in the T26 theorem file).
- **ρ̄ := whole-round departure probability at the truth**: the probability that one φ = 1 round K₁ started at S₀
  has a state ≠ S₀ on its path X⁽¹⁾,…,X⁽ᵐ⁾ (this is the "ρ" of T23's BASIN, reading 1 of T23 STATEMENT §5).
- Conventions off Ω: if S₀ ∉ Ω put Δ_n := 1, ρ* := 1, ρ̄ := 1.

**Run-level objects.**
- 𝓒 = calibration output (streams 0–9), with T = T(𝓒) stages of the frozen grid, L = max(4, ⌈log₂(n+1)⌉),
  N = N_e; E_𝓒, P_𝓒 = expectation/probability over final streams 10–13 given (data, 𝓒).
- **𝒢_n** = the event that the SMC branch is taken and calibration succeeds (a grid is constructed at tier 0 or tier 1,
  i.e. status is not `schedule_limit`, and the final run is launched). 𝒢_n is (data, 𝓒)-measurable.
- **ℰ_n** = the exact-enumeration branch (deterministic in (n, p): Σ_{k≤K} C(p,k) ≤ (5H₀+4N₀)p).
- **Potential uninterrupted run.** On 𝒢_n, under EX-A, EX-S, CAL, the final run (4 islands, T stages, L+4 terminal
  rounds) is a well-defined random object whether or not the real job would finish within its resource allocation.
  Its outputs are written Ẑ°_r, Ẑ° = ¼Σ_rẐ°_r, PIP̂°_{rj}, primary PIP̂°_j = ¼Σ_r PIP̂°_{rj}, MPM̂° = {j: PIP̂°_j > ½}.
- **𝒪_n (output-available)** = the event that the method returns evidence and PIPs (status `exact` or `completed`).
  Reported outputs are written Ẑ, Ẑ_r, PIP̂, MPM̂ and exist only on 𝒪_n.
- **T^max_n := 4T₀ = 4 max(1000, ℓ²)**, ℓ = ⌈log₂(n+p+1)⌉. By METHODOLOGY §6.7 a construction with more than T_e intervals
  fails, and e ≤ 1, so T ≤ T^max on 𝒢_n (deterministic cap).
- **b(𝓒) := 2(T+1)Δ_n / (1 − Δ_n)** (finite: Δ_n < 1 when S₀ ∈ Ω, see Lemma 1).

**Standing idealisations / bookkeeping hypotheses** (declared, not proved):
- EX-A, EX-S, CAL (00_COMMON §3); START = exact iid π₀ draws (T09(i), locked).
- **OUT** (output bookkeeping): 𝒪_n ⊆ ℰ_n ∪ 𝒢_n; on 𝒪_n ∩ 𝒢_n the reported outputs equal the potential run's outputs
  (an interruption can remove outputs, never alter them); on 𝒪_n ∩ ℰ_n, Ẑ = Z and PIP̂_j = PIP_j (exact enumeration
  under EX-A). This is the "potential-uninterrupted-run / output-available split". **Nothing below conditions on 𝒪_n**;
  every probabilistic conclusion is of the form P(𝒪_n ∩ {error > ε}) → 0, and P(𝒪_n) itself is not claimed to → 1.

---

## 1. Statements

### Theorem A (T26(i)–(ii), premise form; composition of locked results)

*Hypotheses:* EX-A, EX-S, CAL, START, OUT, and

- **(Ω)** P₀(s₀ ≤ K_n) → 1;
- **(P1)** for every ε > 0, P(𝒢_n ∩ {(T_n + 1)Δ_n > ε}) → 0 (joint probability over data and calibration streams;
  T_n the realised stage count). Sufficient deterministic-budget form: (T^max_n + 1)Δ_n → 0 in P₀-probability.
- **(P2)** (L_n + 4)ρ*_n → 0 in P₀-probability.

No statistical assumption (G, R, SE, BM, EXP, VIS, NL) is used in Theorem A.

*Conclusions.*

**(A-0) Finite-n, calibration-conditional bounds.** Fix n, the data, and 𝓒 ∈ 𝒢_n with S₀ ∈ Ω. Then for every island r:

- (a) E_𝓒|Ẑ°_r/Z − 1| ≤ b(𝓒) and E_𝓒|Ẑ°/Z − 1| ≤ b(𝓒);
- (b) the fraction f_r of island r's particles ≠ S₀ at the end of stage T satisfies E_𝓒 f_r ≤ min{1, 2δ₁ + 2b(𝓒)};
- (c) E_𝓒 max_j |PIP̂°_{rj} − 1{j∈S₀}| ≤ min{1, 2δ₁ + 2b(𝓒)} + (L + 5/2)ρ̄ + u_π, and the same bound holds for the
  primary PIP̂°_j;
- (d) P_𝓒(MPM̂° ≠ S₀) ≤ 2[min{1, 2δ₁ + 2b(𝓒)} + (L + 5/2)ρ̄ + u_π];
- (e) ρ̄ ≤ Σ_e K_e(S₀, Ω∖{S₀}) ≤ (B+3)u_π, hence ρ̄ ≤ ρ*; and Δ_n = max{1 − π₀(S₀), δ₁} exactly.

**(A-i) Evidence consistency.** For every ε > 0:
P(𝒪_n ∩ {|Ẑ/Z − 1| > ε}) → 0, P(𝒪_n ∩ {max_r |Ẑ_r/Z − 1| > ε}) → 0, P(𝒪_n ∩ {|log Ẑ − log Z| > ε}) → 0;
and for the potential run, P(𝒢_n ∩ {|Ẑ°/Z − 1| > ε}) → 0.

**(A-ii) PIP and MPM consistency.** For every ε > 0:
P(𝒪_n ∩ {max_j |PIP̂_j − 1{j∈S₀}| > ε}) → 0 (also islandwise, max over r), and P(𝒪_n ∩ {MPM̂ ≠ S₀}) → 0.
The same holds for the potential run on 𝒢_n.

**(A-iii) Limits (not claimed).** P(𝒪_n) → 1 (operational completion, OP-s); a bounded stage count; any statement in the
masked regime; the secondary (Ẑ_r-weighted) PIP; any uniform Monte Carlo rate in N (none of the bounds depend on N);
anything about runs selected by their flags or their completion.

### Theorem B (T26(i)–(ii), discharged form; where EXP enters)

*Hypotheses:* EX-A, EX-S, CAL, START, OUT, and in R1:
- **G, R, SE, BM-C** (or **BM-∞**) — the hypotheses of T03 (H-T02 closed by T02(i), wave 3);
- **EXP′** (strict, ρ_n = O_P(1); or the weak variant ρ_n = o_P(log n)), **VIS**, **NL_η**, **NL_avg(κ)** for a
  fixed κ > 0 — the hypotheses of T22(iii) (wave 2), with blocks = the method's partition.

*Conclusions.* (P1) holds in its deterministic-budget form and (P2) holds; quantitatively

- (T^max_n + 1)Δ_n = O_P( log²n · [2^B √(log n) n^{−κ} + √(log n / n)] ) → 0 (strict EXP′; weak EXP′: on events of
  probability → 1, ≤ log²n · [2^B√(log n) n^{−κ/2} + s₀e_n] + O_P(log^{2.5}n/√n) → 0);
- (L_n + 4)ρ*_n = O_P( log n · √(log n / n) ) → 0, **without EXP**.

Hence all conclusions of Theorem A hold.

*Where EXP enters, exactly.* By Lemma 1, Δ_n = max{1 − π₀(S₀), δ₁}. The term δ₁ and the whole of (P2) are
discharged by T03 alone (G, R, SE, BM; no EXP). EXP′ (with VIS, NL_η, NL_avg) is used **only** to show
(T^max_n + 1)(1 − π₀(S₀)) → 0, i.e. 1 − π₀(S₀) = o_P(1/log² n), via T22(iii). Any other route to
(T_n+1)(1 − π₀(S₀)) → 0 replaces EXP′ in Theorem B without changing anything else.

---

## 2. Lemmas

### Lemma 1 (Δ identity). PROVED.
If S₀ ∈ Ω then Δ_n = max{1 − π₀(S₀), 1 − π(S₀)} < 1.

*Proof.* T22(iv-b) (locked, deterministic, needs only S₀ ∈ Ω) gives
sup_{φ∈[0,1]}[1 − q_φ(S₀)] ≤ max{1 − π₀(S₀), 1 − π(S₀)}. Conversely φ = 0 and φ = 1 are in [0,1] and q₀ = π₀,
q₁ = π, so the sup is ≥ each endpoint value. Hence equality. Both endpoint masses are > 0 (γ₀ > 0, γ₁ > 0 on Ω), so
Δ_n < 1. ∎

Consequence: the premise (P1) is equivalent to (T_n+1)(1 − π₀(S₀)) → 0 together with (T_n+1)δ₁ → 0 (on 𝒢_n);
the bridge interior (0 < φ < 1) never adds anything. This is the "n-indexed Δ_n(T_n+1) → 0 via T22(iv)".

### Lemma 2 (departure from the truth). PROVED.
Assume S₀ ∈ Ω. Let K_e (e ranging over the m = p + B + 2 labels: Gibbs j = 1..p, one uniform swap, B neighbour
swaps, one independence proposal) be the elementary kernels at φ = 1. Then

  ρ̄ ≤ Σ_e K_e(S₀, Ω∖{S₀}) ≤ Σ_{j=1}^p π(S₀ Δ {j})/π(S₀) + (B+2)·u_π ≤ (B+3)u_π,

and since ρ̄ ≤ 1, ρ̄ ≤ ρ*.

*Proof.* (1) *Kernel bound.* T09(ii) (locked): each K_e is π-reversible on Ω (q₁ = π). For x, y ∈ Ω,
π(x)K_e(x,y) = π(y)K_e(y,x) ≤ π(y), so K_e(x,y) ≤ π(y)/π(x). (Invariance alone also suffices:
π(y) = Σ_z π(z)K_e(z,y) ≥ π(x)K_e(x,y).)
(2) *Gibbs labels.* The Gibbs step for j changes only coordinate j, so K_{Gj}(S₀, ·) is supported on {S₀, S₀Δ{j}}
(the second point only if feasible). Hence K_{Gj}(S₀, Ω∖{S₀}) ≤ π(S₀Δ{j})/π(S₀) (0 if S₀Δ{j} ∉ Ω). The models
S₀Δ{j}, j = 1..p, are distinct and ≠ S₀, so Σ_j π(S₀Δ{j}) ≤ π(Ω∖{S₀}) = δ₁ and the Gibbs sum is ≤ δ₁/π(S₀) = u_π.
(3) *Other labels.* For each of the B + 2 other labels, K_e(S₀, Ω∖{S₀}) = Σ_{y≠S₀}K_e(S₀,y) ≤ π(Ω∖{S₀})/π(S₀) = u_π.
(4) *Round.* Fix an order σ (a permutation of the m labels). Started at X⁽⁰⁾ = S₀, the path has a state ≠ S₀ iff there
is a first k with X⁽ᵏ⁾ ≠ S₀; then X⁽ᵏ⁻¹⁾ = S₀. Given σ and X⁽ᵏ⁻¹⁾ = S₀, step k is a draw from K_{σ(k)}(S₀, ·) using
fresh randomness (EX-S). So P(first departure at k | σ) ≤ K_{σ(k)}(S₀, Ω∖{S₀}), and summing over k (each label occurs
exactly once in σ) gives P(depart | σ) ≤ Σ_e K_e(S₀, Ω∖{S₀}). Averaging over the uniformly random σ (drawn
independently of the state) gives the bound for ρ̄. ∎

Remark. (B+3)u_π is the 00_COMMON definition of ρ* (before the min with 1). Lemma 2 is the missing link that makes
"(L+4)ρ*" the right premise: it bounds the T23 truth-departure constant ρ by ρ*.

### Lemma 3 (terminal-round prefix bound). PROVED.
Fix 𝓒 ∈ 𝒢_n with S₀ ∈ Ω and an island r. With B̄_r the bad-round fraction of T23 STATEMENT §1 and f_r the fraction of
island-r particles ≠ S₀ at the end of stage T (X_{i,0} ≠ S₀),

  E_𝓒 B̄_r ≤ E_𝓒 f_r + (L + 5/2) ρ̄.

*Proof.* Fix particle i and measured round h ∈ {1,..,4} (terminal round L+h). For k = 1..L+h let D_{i,k} be the event
"X_{i,k−1} = S₀ and the path of terminal round k contains a state ≠ S₀". If X_{i,0} = S₀ and none of D_{i,1},…,D_{i,L+h}
occurs then, by induction on k, X_{i,k} = S₀ and every state on the paths of rounds 1..L+h equals S₀; in particular
B_{i,h} = 0 (B_{i,h} looks at X_{i,L+h−1} and the path of round L+h). Hence
B_{i,h} ≤ 1{X_{i,0} ≠ S₀} + Σ_{k=1}^{L+h} 1_{D_{i,k}}.
In the terminal rounds there is no reweighting or resampling (T23 reading 3), and each round of each particle uses a
fresh uniformly random order and fresh step randomness, independent of the past (EX-S, CAL; METHODOLOGY §6.5). Hence,
conditionally on the history up to the start of round k, on {X_{i,k−1} = S₀} the round-k path has the law of a round
started at S₀, and P_𝓒(D_{i,k}) ≤ ρ̄. Taking E_𝓒 and averaging over i and h:
E_𝓒 B̄_r ≤ E_𝓒 f_r + ρ̄ · ¼Σ_{h=1}^4 (L+h) = E_𝓒 f_r + (L + 5/2)ρ̄. ∎

(Fully-locked alternative: T23(ii-c) with BASIN({S₀}, r₀ = 1, a = 1 − ρ̄, η = ρ̄, ρ = ρ̄, δ = min{1, 2δ₁+2b}); the entrance
condition K₁(S₀,{S₀}) ≥ 1 − ρ̄ holds because an end state ≠ S₀ is a path state ≠ S₀. It gives the slightly weaker
E_𝓒 max_j|PIP̂°_j − 1{j∈S₀}| ≤ δ + ρ̄^L + 2(L+4)ρ̄ + u_π, which also → 0 under (P2). Lemma 3 is used only to get the
sharper constant and the islandwise version.)

---

## 3. Proof of Theorem A

### (A-0) — finite n, calibration-conditional. PROVED (composition; inputs locked).

Fix data with S₀ ∈ Ω and 𝓒 ∈ 𝒢_n. Under EX-A, EX-S, CAL, START the final islands satisfy the setting of T14(i)
(exact start, multinomial resampling after every reweighting, one q_t-invariant round per stage — T09(iii) — no forced
steps in the final run, METHODOLOGY §6.8).

(a) Apply **T14(i-b), (i-c)** with reference S° = S₀. S₀ is deterministic, so it is fixed given 𝓒, and S₀ ∈ Ω.
Then η_t = 1 − q_t(S₀) ≤ Δ_n for t = 0..T, so Σ_{t=0}^T η_t ≤ (T+1)Δ_n and ε_* = max_t η_t ≤ Δ_n < 1 (Lemma 1).
Hence E_𝓒|Ẑ°_r/Z − 1| ≤ (2/(1−ε_*))(T+1)Δ_n ≤ b(𝓒), and the same for Ẑ° by (i-c).

(b) Apply **T15(iii)** (hypothesis H-T12 closed by T12(i), locked) at position τ = "end of stage T", with 𝔄 = {S₀}
(fixed given 𝓒), c = ½ and B = b(𝓒) from (a): P_𝓒(W_r < ½) ≤ 2b(𝓒), and by T15(i)
E_𝓒 f_r ≤ min{1, π(Ω∖{S₀})/½ + 2b(𝓒)} = min{1, 2δ₁ + 2b(𝓒)}.

(c) **T23(ii-a), (ii-b)** (locked; pathwise; S₀ ∈ Ω): max_j|PIP̂°_{rj} − 1{j∈S₀}| ≤ B̄_r + u_π on every realisation.
Take E_𝓒, use Lemma 3 and (b). For the primary PIP, |¼Σ_r(PIP̂°_{rj} − 1{j∈S₀})| ≤ ¼Σ_r max_j|PIP̂°_{rj} − 1{j∈S₀}|,
so the same bound holds.

(d) If MPM̂° ≠ S₀ then some j has |PIP̂°_j − 1{j∈S₀}| ≥ ½. Markov's inequality on (c).

(e) Lemmas 1 and 2. ∎

### (A-i), (A-ii) — n-indexed conversion. PROVED.

Fix ε ∈ (0, ½) and write W° = Ẑ°/Z. Split according to ℰ_n, S₀ ∈ Ω.

*Exact branch.* On 𝒪_n ∩ ℰ_n, Ẑ = Z (OUT), so the evidence events are empty. PIP̂ = PIP and
max_j|PIP_j − 1{j∈S₀}| ≤ δ₁ (each PIP_j and 1{j∈S₀} differ by at most π(Ω∖{S₀}); T03(ii)'s deterministic part).
If ρ* < 1 then u_π = ρ*/(B+3), and δ₁ ≤ u_π ≤ ρ*. So the PIP and MPM events on ℰ_n are contained in
{ρ* ≥ min(ε, ½)} ∪ {S₀ ∉ Ω}, whose probabilities → 0 by (P2) and (Ω).

*SMC branch.* By OUT, 𝒪_n ∩ ℰ_nᶜ ⊆ 𝒢_n and on it the reported outputs equal the potential ones. So it suffices to
treat the potential run on 𝒢_n ∩ {S₀ ∈ Ω}.

Evidence. Fix x ∈ (0, ¼]. On the (data, 𝓒)-event A_x = 𝒢_n ∩ {S₀∈Ω} ∩ {(T+1)Δ_n ≤ x}: Δ_n ≤ x ≤ ¼, so
b(𝓒) ≤ 2x/(1 − ¼) < 3x, and by (A-0)(a) and Markov, P_𝓒(|W°−1| > ε) ≤ 3x/ε. Therefore
P(𝒢_n ∩ {|W° − 1| > ε}) ≤ 3x/ε + P(𝒢_n ∩ {(T+1)Δ_n > x}) + P₀(S₀ ∉ Ω).
By (P1) and (Ω), limsup_n ≤ 3x/ε; x is arbitrary, so the limit is 0. The same argument applies to each Ẑ°_r
(a union over r = 1..4 costs a factor 4). For logs: on {|W° − 1| ≤ ε}, |log W°| ≤ ε/(1−ε) ≤ 2ε.

PIPs. On A_x ∩ {ρ* ≤ x}, (A-0)(c) and Lemma 2 give
E_𝓒 max_j|PIP̂°_j − 1{j∈S₀}| ≤ 2δ₁ + 6x + (L+5/2)ρ* + u_π.
Here δ₁ ≤ Δ_n ≤ x, and, since ρ* ≤ x < 1, u_π = ρ*/(B+3) ≤ x. Also use the event {(L+4)ρ* ≤ x} instead of
{ρ* ≤ x} (it is smaller since L+4 ≥ 1): then (L+5/2)ρ* ≤ x. Altogether the conditional mean is ≤ 10x on
A_x ∩ {(L+4)ρ* ≤ x}, and
P(𝒢_n ∩ {max_j|PIP̂°_j − 1{j∈S₀}| > ε}) ≤ 10x/ε + P(𝒢_n ∩ {(T+1)Δ_n > x}) + P₀((L+4)ρ* > x) + P₀(S₀ ∉ Ω),
whose limsup is ≤ 10x/ε by (P1), (P2), (Ω); let x ↓ 0. Islandwise: the same with (A-0)(c) per island and a union
over r. MPM: (A-0)(d) gives P_𝓒(MPM̂° ≠ S₀) ≤ 20x on the same event; conclude identically.

Combining the two branches with OUT gives (A-i) and (A-ii). ∎

Notes on the proof.
- At no point is any probability conditioned on 𝒪_n or on completion. 𝒪_n only appears as an intersecting event.
- The calibration enters only through T(𝓒) ≤ T^max (and 𝒢_n); no property of the grid's ESS (T13) is needed, and the
  final particle count N never enters. Increasing N_n does not help (Astra's remark is confirmed by the form of the
  bound).
- T25(iv) (variance under PW2) is not used; PW2 is not assumed.
- The secondary PIP is not claimed. (It would need the joint behaviour of all four Ẑ_r; dropped per FROZEN_LIST.)

---

## 4. Proof of Theorem B. PROVED (composition; T03 and T22(iii) locked, the latter CONDITIONAL on EXP′ etc.)

(Ω) is part of R ("eventually s₀ ≤ K").

*Budget growth.* ℓ = ⌈log₂(n+p+1)⌉ ≤ log₂(n + n^A + 1) + 1 ≤ (A+1)log₂ n + 2 for n ≥ 2, so
T^max = 4 max(1000, ℓ²) = O(log² n); L + 4 = O(log n); B ≤ 16.

*T03(i)* (G, R, SE, BM-C or BM-∞; H-T02 closed by T02(i)): δ₁ = O_P(r_n), r_n = √(log n/n). Hence
π(S₀) → 1 in probability and u_π = δ₁/π(S₀) = O_P(r_n).

*T22(iii)* needs G, R, within-block SE, VIS, NL_η, NL_avg(κ), EXP′ and the method's blocks. Within-block SE follows
from SE for n large: blocks have |T| ≤ B ≤ min(p, 16) and m_n + s₀ ≥ (log n)/(2 log 2) ≥ 16 eventually, so every
nonempty T inside a block has |T| ≤ min(p, m_n + s₀) and SE applies with the same φ₀. T22(iii) item 3 gives
1 − π₀(S₀) = O_P(2^B √(log n) n^{−κ} + e_n) with e_n = o_P(n^{−m}) for every m (strict EXP′); under weak EXP′,
1 − π₀(S₀) ≤ 2^B √(log n) n^{−κ+ζ_n} + s₀e_n with ζ_n = o_P(1) on events of probability → 1.

*(P1).* By Lemma 1, (T^max+1)Δ_n ≤ (T^max+1)[(1 − π₀(S₀)) + δ₁]
= O(log²n)·O_P(2^B√(log n)n^{−κ} + e_n + r_n) → 0, because 2^B ≤ 2^16 and log^{2.5}n · n^{−min(κ,1/2)} → 0.
Weak variant: on {ζ_n ≤ κ/2} (probability → 1), log²n · 2^B√(log n)n^{−κ/2} → 0. Since T_n ≤ T^max on 𝒢_n, the
joint-probability form of (P1) follows.

*(P2).* (L+4)ρ* ≤ (L+4)(B+3)u_π = O(log n)·19·O_P(r_n) = O_P(log^{1.5} n / √n) → 0. No EXP-type hypothesis is used.

Apply Theorem A. ∎

**Status of Theorem B.** PROVED as a composition, but CONDITIONAL in the register's sense: its conclusions are only as
good as T22(iii)'s hypotheses EXP′, VIS, NL_η, NL_avg(κ) (open; not proved for the actual partition) and T03's SE and
beta-min (SE is impossible at n = 200, p ≥ 500). The combined statement T03 + T02(i) without H-T02 was "not separately
reviewed" (LOCKED_PROOFS.md, scope notes).

---

## 5. Which premises are genuinely new

| Premise in Theorem A | Discharged by | New? |
|---|---|---|
| (Ω) s₀ ≤ K eventually | R | no |
| (T_n+1)·δ₁ → 0 (half of P1, via Lemma 1) | T03(i) + T^max = O(log²n) | no (needs only G, R, SE, BM) |
| (T_n+1)·(1−π₀(S₀)) → 0 (other half of P1) | T22(iii) — CONDITIONAL on EXP′, VIS, NL_η, NL_avg(κ) | **yes: the only genuinely open input**; it is exactly "start concentration at rate o(1/T_n)" |
| (L_n+4)ρ*_n → 0 (P2) | T03(i) + L = O(log n), B ≤ 16 | no |
| ρ̄ ≤ ρ* (link between T23's ρ and P2) | Lemma 2 (new, from T09(ii)) | new lemma, elementary, PROVED here |
| OUT | method construction + EX-A, EX-S | bookkeeping, declared |
| P(𝒪_n) → 1 | — | not claimed |

So the "longest hypothesis list in the pool" collapses: the composition itself needs only (Ω), (P1), (P2) and the
standing idealisations. All statistical content sits in two places: T03 (posterior concentration) and the start
concentration 1 − π₀(S₀) = o_P(1/T_n), which is the favourable-regime definition.

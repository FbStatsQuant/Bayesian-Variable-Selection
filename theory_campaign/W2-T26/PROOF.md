# W2-T26 — T26 (i)–(ii) restated: evidence and PIP consistency in the favourable regime

Candidate proof, written by cloud run W2-T26 (2026-11-02). **Not reviewed, not adopted.** Status words as in
`theory_campaign/PROTOCOL.md`. Notation of `Docs/Theory/theorems/00_COMMON.md`; new symbols are defined in §0.
Locked inputs are cited by their STATEMENT.md in `Docs/Theory/proofs/` (register `LOCKED_PROOFS.md`).

---

## 0. Setting, new symbols, standing idealisations

Everything is indexed by n (regime R1/R4 of 00_COMMON §2: n → ∞, s₀ fixed, p = p_n ≤ n^A, actual budgets).
The index n is suppressed when harmless.

**Data-level quantities** (functions of (X, y) only; defined when S₀ ∈ Ω, i.e. s₀ ≤ K):
- π₀, q_φ = γ_φ/Z̄_φ, π = q₁; δ₁ = 1 − π(S₀); u_π = δ₁/π(S₀); ρ* = min{1, (B+3)u_π} (00_COMMON §2).
- **Δ_n := 1 − inf_{φ∈[0,1]} q_φ(S₀)** (the bridge's worst-case deficit at the truth, as in the T26 theorem file).
- **ρ̄ := whole-round departure probability at the truth**: the probability that one φ = 1 round K₁ started at S₀
  has a state ≠ S₀ on its path X⁽¹⁾,…,X⁽ᵐ⁾ (the ρ of T23's BASIN; T23 STATEMENT §5 reading 1).
- Conventions off Ω: if S₀ ∉ Ω put Δ_n := 1, ρ̄ := 1, u_π := ∞.

**Run-level objects.**
- 𝓒 = calibration output (streams 0–9), with T = T(𝓒) stages of the frozen grid, L = max(4, ⌈log₂(n+1)⌉),
  N = N_e. E_𝓒, P_𝓒 = expectation/probability over the final streams 10–13 given (data, 𝓒).
- **𝒢_n** = the event that the SMC branch is taken and calibration succeeds (a grid is constructed at the final tier,
  so the status is not `schedule_limit` and the final run executes). It is the event 𝒜 of T12 STATEMENT; it is
  (data, 𝓒)-measurable.
- **ℰ_n** = the exact-enumeration branch (deterministic in (n, p): Σ_{k≤K} C(p,k) ≤ (5H₀+4N₀)p).
- **Potential uninterrupted run.** On 𝒢_n, under EX-A, EX-S, CAL, START, the final run (4 islands, T stages, L burn-in
  and 4 measured rounds) is a well-defined random object (T12's I(𝓒)), whether or not the real job would finish within
  its resource allocation. Its outputs: Ẑ°_r, Ẑ° = ¼Σ_rẐ°_r, PIP̂°_{rj}, primary PIP̂°_j = ¼Σ_r PIP̂°_{rj},
  MPM̂° = {j : PIP̂°_j > ½}. W_r := Ẑ°_r/Z.
- **𝒪_n (output-available)** = the event that the method returns evidence and PIPs (status `exact` or `completed`).
  The reported Ẑ, Ẑ_r, PIP̂, MPM̂ exist only on 𝒪_n.
- **T^max_n := 4T₀ = 4 max(1000, ℓ²)**, ℓ = ⌈log₂(n+p+1)⌉. A construction with more than T_e intervals fails
  (METHODOLOGY §6.7) and e ≤ 1, so T ≤ T^max on 𝒢_n (a deterministic cap).
- **b(𝓒) := 2(T+1)Δ_n / (1 − Δ_n)**, finite because Δ_n < 1 when S₀ ∈ Ω (Lemma 1).

**Standing idealisations and bookkeeping** (declared, not proved):
- EX-A, EX-S, CAL (00_COMMON §3); START = exact iid π₀ draws and exact Z̄₀ (T09(i), locked).
- **OUT (output bookkeeping).** 𝒪_n ⊆ ℰ_n ∪ 𝒢_n; on 𝒪_n ∩ 𝒢_n the reported outputs equal the potential run's outputs
  (an interruption, e.g. `resource_limit`, can remove outputs but never alters a reported value); on 𝒪_n ∩ ℰ_n,
  Ẑ = Z and PIP̂_j = PIP_j (exact enumeration under EX-A).
  This is the potential-uninterrupted-run / output-available split. **Nothing below conditions on 𝒪_n.** Every
  probabilistic conclusion has the form P(𝒪_n ∩ {error > ε}) → 0, and P(𝒪_n) → 1 is not claimed.

---

## 1. Statements

### Theorem A (T26(i)–(ii), premise form: composition of locked results)

*Hypotheses.* EX-A, EX-S, CAL, START, OUT, and
- **(Ω)** P₀(s₀ ≤ K_n) → 1;
- **(P1)** for every ε > 0, P(𝒢_n ∩ {(T_n + 1)Δ_n > ε}) → 0 (joint probability over data and calibration streams;
  T_n the realised stage count). Sufficient deterministic-budget form: (T^max_n + 1)Δ_n → 0 in P₀-probability.

No statistical assumption (G, R, SE, BM, EXP, VIS, NL) is used in Theorem A. The frozen second premise
(L_n + 4)ρ*_n → 0 is **not needed** (Lemma 3, Remark 3.2).

*Conclusions.*

**(A-0) Finite n, calibration-conditional.** Fix n, the data with S₀ ∈ Ω, and 𝓒 ∈ 𝒢_n. For every island r:
- (a) E_𝓒|Ẑ°_r/Z − 1| ≤ b(𝓒) and E_𝓒|Ẑ°/Z − 1| ≤ b(𝓒).
- (b) For f = the fraction of island r's particles ≠ S₀ at the end of stage T, or at the start of any measured round
  (after L + h − 1 terminal rounds, h = 1..4): E_𝓒 f ≤ min{1, 2δ₁ + 2b(𝓒)}.
- (c) E_𝓒 max_j |PIP̂°_{rj} − 1{j∈S₀}| ≤ min{1, 2δ₁ + 2b(𝓒)} + ρ̄ + u_π ≤ min{1, 2δ₁ + 2b(𝓒)} + (B+4)u_π; the same
  bound holds for the primary PIP̂°_j.
- (d) P_𝓒(MPM̂° ≠ S₀) ≤ 2[min{1, 2δ₁ + 2b(𝓒)} + ρ̄ + u_π].
- (e) Δ_n = max{1 − π₀(S₀), δ₁} exactly, and ρ̄ ≤ Σ_e K_e(S₀, Ω∖{S₀}) ≤ (B+3)u_π.

**(A-i) Evidence consistency.** For every ε > 0, each of
P(𝒪_n ∩ {|Ẑ/Z − 1| > ε}), P(𝒪_n ∩ {max_r |Ẑ_r/Z − 1| > ε}), P(𝒪_n ∩ {|log Ẑ − log Z| > ε})
tends to 0; and for the potential run, P(𝒢_n ∩ {max_r |Ẑ°_r/Z − 1| > ε}) → 0.

**(A-ii) PIP and MPM consistency.** For every ε > 0,
P(𝒪_n ∩ {max_j |PIP̂_j − 1{j∈S₀}| > ε}) → 0 (also with max over islands r of the islandwise PIPs) and
P(𝒪_n ∩ {MPM̂ ≠ S₀}) → 0. The same holds for the potential run on 𝒢_n.

**(A-iii) Not claimed.** P(𝒪_n) → 1 (operational completion; OP-s); any statement in the masked regime; the secondary
(Ẑ_r-weighted) PIP; the HPM (T38 replaces old T26(iii)); any uniform Monte Carlo rate in N (none of the bounds depend
on N); anything about runs selected by their flags or by their completion; floating-point validity (EX-A).

### Theorem B (T26(i)–(ii), discharged form: where EXP enters)

*Hypotheses.* EX-A, EX-S, CAL, START, OUT, and in R1:
- **G, R, SE, BM-C** (or **BM-∞**): the hypotheses of T03 (H-T02 closed by T02(i), wave 3);
- **EXP′** (strict: ρ_n = O_P(1); or the weak variant ρ_n = o_P(log n)), **VIS**, **NL_η**, **NL_avg(κ)** for a fixed
  κ > 0, with the method's blocks: the hypotheses of T22(iii) (wave 2).

*Conclusions.* (Ω) holds and (P1) holds in its deterministic-budget form:
- strict EXP′: (T^max_n + 1)Δ_n = O_P( log²n · [2^B √(log n) n^{−κ} + e_n + √(log n / n)] ) → 0, e_n = o_P(n^{−m}) ∀m;
- weak EXP′: on events of probability → 1, (T^max_n+1)Δ_n ≤ C log²n · [2^B √(log n) n^{−κ/2} + s₀e_n] + O_P(log^{2.5}n/√n) → 0.

Hence all conclusions of Theorem A hold. (The frozen (L_n+4)ρ*_n → 0 also holds: it is O_P(log^{1.5}n/√n).)

*Where EXP enters, exactly.* Δ_n = max{1 − π₀(S₀), δ₁} (Lemma 1). The δ₁ part is discharged by T03 alone (no EXP).
EXP′ (with VIS, NL_η, NL_avg) is used **only** to show (T^max_n + 1)(1 − π₀(S₀)) → 0, i.e. 1 − π₀(S₀) = o_P(1/log²n),
through T22(iii). Any other proof of (T_n+1)(1 − π₀(S₀)) → 0 replaces EXP′ and nothing else changes.

---

## 2. Lemmas

### Lemma 1 (Δ identity). PROVED.
If S₀ ∈ Ω then Δ_n = max{1 − π₀(S₀), 1 − π(S₀)} < 1.

*Proof.* T22(iv-b) (locked, deterministic, assumes only S₀ ∈ Ω) gives
sup_{φ∈[0,1]}[1 − q_φ(S₀)] ≤ max{1 − π₀(S₀), 1 − π(S₀)}. Conversely φ = 0 and φ = 1 belong to [0,1] and q₀ = π₀,
q₁ = π, so the sup is at least each endpoint value. Both endpoint masses are > 0 (γ₀, γ₁ > 0 on Ω), so Δ_n < 1. ∎

So (P1) ⇔ [(T_n+1)(1 − π₀(S₀)) → 0 and (T_n+1)δ₁ → 0] (on 𝒢_n): the bridge interior 0 < φ < 1 adds nothing.
This is the n-indexed form of "Δ_n(T_n+1) → 0 via T22(iv)".

### Lemma 2 (departure from the truth). PROVED.
Assume S₀ ∈ Ω. Let K_e, over the m = p + B + 2 labels (Gibbs j = 1..p, one uniform swap, B neighbour swaps, one
independence proposal), be the elementary kernels at φ = 1. Then

  ρ̄ ≤ Σ_e K_e(S₀, Ω∖{S₀}) ≤ Σ_{j=1}^p π(S₀Δ{j})/π(S₀) + (B+2)u_π ≤ (B+3)u_π;  in particular ρ̄ ≤ ρ*.

*Proof.* (1) *Kernel bound.* By T09(ii) (locked) each K_e is π-reversible on Ω. For x, y ∈ Ω,
π(x)K_e(x,y) = π(y)K_e(y,x) ≤ π(y), so K_e(x,y) ≤ π(y)/π(x). (π-invariance alone also gives it:
π(y) = Σ_z π(z)K_e(z,y) ≥ π(x)K_e(x,y).)
(2) *Gibbs labels.* The Gibbs-j step changes at most coordinate j, so K_{Gj}(S₀, ·) is carried by {S₀, S₀Δ{j}}
(the second point only if feasible). Hence K_{Gj}(S₀, Ω∖{S₀}) ≤ π(S₀Δ{j})/π(S₀). The models S₀Δ{j}, j = 1..p, are
distinct and differ from S₀, so the Gibbs sum is ≤ π(Ω∖{S₀})/π(S₀) = u_π.
(3) *Other labels.* For each of the other B + 2 labels, K_e(S₀, Ω∖{S₀}) = Σ_{y≠S₀}K_e(S₀,y) ≤ u_π.
(4) *Round.* Condition on the order σ (uniform, independent of the state; T12 STATEMENT (R3)). Started at S₀, the
path has a state ≠ S₀ iff there is a first k with X⁽ᵏ⁾ ≠ S₀, and then X⁽ᵏ⁻¹⁾ = S₀. Given σ, the path is a Markov chain
with kernels K_{σ(1)},…,K_{σ(m)} (R3), so P(first departure at step k | σ) ≤ K_{σ(k)}(S₀, Ω∖{S₀}). Summing over k
(each label occurs once in σ) gives P(depart | σ) ≤ Σ_e K_e(S₀, Ω∖{S₀}); average over σ. Finally ρ̄ ≤ 1. ∎

### Lemma 3 (round-start occupancy controls the bad-round fraction). PROVED.
Fix data with S₀ ∈ Ω, 𝓒 ∈ 𝒢_n and an island r. Let B̄_r be the bad-round fraction of T23 STATEMENT §1 and g_{r,h} the
fraction of island r's particles ≠ S₀ at the start of measured round h (= terminal round L + h). Then

  E_𝓒 B̄_r ≤ ¼ Σ_{h=1}^{4} E_𝓒 g_{r,h} + ρ̄.

*Proof.* B_{i,h} = 1 iff the start X_{i,L+h−1} or a later state on the path of round L+h differs from S₀. So
B_{i,h} ≤ 1{X_{i,L+h−1} ≠ S₀} + 1{X_{i,L+h−1} = S₀, the path of round L+h has a state ≠ S₀}.
By T12 STATEMENT (R3) (a consequence of EX-S and the method's construction; terminal rounds have no reweighting or
resampling), given the σ-field H of everything before round L+h, particle i's (order, path) in that round is uniform
order and a Markov path started at X_{i,L+h−1}. Hence the conditional probability of the second event given H is
1{X_{i,L+h−1} = S₀}·ρ̄ ≤ ρ̄. Take E_𝓒, average over i (giving E_𝓒 g_{r,h} + ρ̄ for each h) and over h. ∎

**Remark 3.1 (what the frozen premise came from).** If occupancy is controlled only at the end of stage T (T23(ii-c)'s
"initial occupancy" δ), one must also pay for departures in all L + h rounds: with 𝓡 = {S₀}, T23(ii-c) applies with
BASIN({S₀}, r₀ = 1, a = 1 − ρ̄, η = ρ̄, ρ = ρ̄, δ) and gives δ + ρ̄^L + 2(L+4)ρ̄ + u_π; a direct union bound gives
δ + (L + 5/2)ρ̄ + u_π. That is the origin of the premise (L_n+4)ρ*_n → 0.

**Remark 3.2 (why it is not needed).** T15 is stated at every recording position τ ∈ 𝒯, including (b) "any fixed
elementary prefix within the L + 4 terminal rounds", because its hypothesis H-T12 is T12(i.b), which holds after any
fixed finite sequence of φ = 1 rounds. So occupancy is controlled afresh at the start of each measured round, and only
one round's departure ρ̄ is paid. This removes the (L+4) factor, and with it the premise.

---

## 3. Proof of Theorem A

### (A-0): finite n, calibration-conditional. PROVED (composition; all inputs locked).

Fix data with S₀ ∈ Ω and 𝓒 ∈ 𝒢_n. Under EX-A, EX-S, CAL, START each final island is an instance of the setting of
T14(i), T15 and T23(ii) (exact start; multinomial resampling after every reweighting; one q_t-invariant round per stage
(T09(iii)); no forced steps in the final run (METHODOLOGY §6.8); L burn-in and 4 measured rounds at φ = 1).

(a) **T14(i-b), (i-c)** with reference S° = S₀. S₀ is deterministic, hence fixed given 𝓒, and S₀ ∈ Ω. For t = 0..T,
η_t = 1 − q_t(S₀) ≤ Δ_n, so Σ_{t=0}^T η_t ≤ (T+1)Δ_n and ε_* = max_t η_t ≤ Δ_n < 1 (Lemma 1). Hence
E_𝓒|W_r − 1| ≤ (2/(1−ε_*))(T+1)Δ_n ≤ b(𝓒), and the same for Ẑ°/Z by (i-c).

(b) **T15(iii) and (i)** (hypothesis H-T12 closed by T12(i.a), (i.b), locked), with 𝔄 = {S₀} (fixed given 𝓒), c = ½,
B = b(𝓒) from (a), at τ = "end of stage T" (position (a) of 𝒯) or τ = "after L + h − 1 terminal rounds" (position (b),
a fixed elementary prefix of (L+h−1)m steps). T15(iii) gives P_𝓒(W_r < ½) ≤ b(𝓒)/(1 − ½) = 2b(𝓒), and T15(i) gives
E_𝓒 f ≤ min{1, π(Ω∖{S₀})/½ + 2b(𝓒)} = min{1, 2δ₁ + 2b(𝓒)}. (W_r is the same random variable at all these positions:
the terminal rounds contribute no evidence factor.)

(c) **T23(ii-a), (ii-b)** (locked; pathwise; S₀ ∈ Ω): on every realisation, max_j|PIP̂°_{rj} − 1{j∈S₀}| ≤ B̄_r + u_π.
Take E_𝓒 and apply Lemma 3 with (b): E_𝓒 B̄_r ≤ min{1, 2δ₁ + 2b(𝓒)} + ρ̄. Lemma 2 gives ρ̄ ≤ (B+3)u_π. For the primary
PIP, |¼Σ_r(PIP̂°_{rj} − 1{j∈S₀})| ≤ ¼Σ_r max_{j′}|PIP̂°_{rj′} − 1{j′∈S₀}| for each j, so the same bound holds.

(d) If MPM̂° ≠ S₀ then |PIP̂°_j − 1{j∈S₀}| ≥ ½ for some j (j ∈ S₀ with PIP̂°_j ≤ ½, or j ∉ S₀ with PIP̂°_j > ½).
Markov's inequality on (c).

(e) Lemmas 1 and 2. ∎

### (A-i), (A-ii): n-indexed conversion. PROVED.

Fix ε ∈ (0, ½). Split by branch.

*Exact branch.* On 𝒪_n ∩ ℰ_n, Ẑ = Z (OUT), so the evidence events are empty. PIP̂ = PIP, and for every j,
|PIP_j − 1{j∈S₀}| ≤ π(Ω∖{S₀}) = δ₁ (if j ∈ S₀, PIP_j ≥ π(S₀); if j ∉ S₀, PIP_j ≤ 1 − π(S₀)). Also δ₁ ≤ Δ_n.
On ℰ_n the event 𝒢_n is empty, so (P1) says nothing there. We therefore need δ₁ → 0 on ℰ_n separately; see the
**caveat** below. With δ₁ → 0 in P₀-probability, the PIP and MPM events on 𝒪_n ∩ ℰ_n have probability ≤
P₀(δ₁ ≥ min(ε, ½)) + P₀(S₀ ∉ Ω) → 0 (MPM = S₀ when δ₁ < ½).

*Caveat (exact branch).* (P1) only concerns 𝒢_n. To cover ℰ_n, Theorem A adds
**(P1-ex)** P₀(ℰ_n ∩ {δ₁ > ε}) → 0 for every ε > 0.
It is implied by the deterministic-budget form of (P1) (since δ₁ ≤ Δ_n ≤ (T^max+1)Δ_n), by T03(i), and it is vacuous
when ℰ_n eventually fails (p_n → ∞ fast enough; at p ≥ 18 and n ≥ 22, ℰ_n fails).

*SMC branch.* By OUT, 𝒪_n ∖ ℰ_n ⊆ 𝒢_n and on it the reported outputs equal the potential ones. It suffices to bound
the potential run on 𝒢_n ∩ {S₀ ∈ Ω}.

Fix x ∈ (0, ¼] and let A_x = 𝒢_n ∩ {S₀ ∈ Ω} ∩ {(T+1)Δ_n ≤ x} (a (data, 𝓒)-event). On A_x:
Δ_n ≤ x/2 ≤ ⅛ (T ≥ 1), so b(𝓒) ≤ 2x/(1 − ⅛) < 3x; δ₁ ≤ Δ_n ≤ x/2; u_π = δ₁/(1−δ₁) ≤ x; ρ̄ ≤ (B+3)u_π ≤ 19x (B ≤ 16).

Evidence. By (A-0)(a) and Markov, on A_x, P_𝓒(|W_r − 1| > ε) ≤ 3x/ε for each r. Hence
P(𝒢_n ∩ {max_r|W_r − 1| > ε}) ≤ 12x/ε + P(𝒢_n ∩ {(T+1)Δ_n > x}) + P₀(S₀ ∉ Ω),
whose limsup is ≤ 12x/ε by (P1) and (Ω); x is arbitrary. Pooled: same with 3x/ε. Logs: on {|Ẑ°/Z − 1| ≤ ε},
|log(Ẑ°/Z)| ≤ ε/(1−ε) ≤ 2ε.

PIPs. On A_x, (A-0)(c) gives E_𝓒 max_j|PIP̂°_{rj} − 1{j∈S₀}| ≤ 2δ₁ + 2b + ρ̄ + u_π ≤ x + 6x + 19x + x = 27x for each r,
and the same for the primary PIP. Hence
P(𝒢_n ∩ {max_r max_j|PIP̂°_{rj} − 1{j∈S₀}| > ε}) ≤ 108x/ε + P(𝒢_n ∩ {(T+1)Δ_n > x}) + P₀(S₀ ∉ Ω),
with limsup ≤ 108x/ε; let x ↓ 0. MPM: by (A-0)(d), P_𝓒(MPM̂° ≠ S₀) ≤ 54x on A_x; conclude identically.

Combining the branches with OUT gives (A-i) and (A-ii). ∎

**Correction to the statement of Theorem A.** Add (P1-ex) to its hypotheses (it is automatic under the
deterministic-budget form of (P1), under T03, or when the exact branch eventually does not apply).

Notes on the proof.
- No probability is conditioned on 𝒪_n or on completion. 𝒪_n only appears as an intersected event.
- The calibration enters only through T(𝓒) ≤ T^max and through 𝒢_n. No property of the grid's ESS (T13) is needed,
  and N never enters: increasing N_n does not help (consistent with Astra's review remark).
- T25(iv) (variance under PW2) is not used; PW2 is not assumed.
- The secondary PIP is not claimed and not needed.

---

## 4. Proof of Theorem B. PROVED as a composition (T03, T22(iii) locked; T22(iii) is CONDITIONAL on its hypotheses)

(Ω) is part of R ("eventually s₀ ≤ K").

*Budget growth.* ℓ = ⌈log₂(n+p+1)⌉ ≤ log₂(n + n^A + 1) + 1 ≤ (A+1)log₂ n + 2 for n ≥ 2, so
T^max = 4 max(1000, ℓ²) = O(log²n); B ≤ 16.

*T03(i)* (G, R, SE, BM-C or BM-∞; H-T02 closed by T02(i)): δ₁ = O_P(r_n), r_n = √(log n/n). This also gives (P1-ex).

*T22(iii)* needs G, R, within-block SE, VIS, NL_η, NL_avg(κ), EXP′ and the method's blocks. Within-block SE follows
from SE for large n: blocks have |T| ≤ B ≤ min(p, 16), and m_n + s₀ ≥ (log n)/(2 log 2) ≥ 16 eventually, so every
nonempty T inside a block has |T| ≤ min(p, m_n + s₀) and SE applies with the same φ₀. T22(iii) item 3:
1 − π₀(S₀) = O_P(2^B √(log n) n^{−κ} + e_n), e_n = o_P(n^{−m}) for every m (strict EXP′); under weak EXP′,
1 − π₀(S₀) ≤ 2^B √(log n) n^{−κ+ζ_n} + s₀e_n with ζ_n = o_P(1), on events of probability → 1.

*(P1).* By Lemma 1, (T^max+1)Δ_n ≤ (T^max+1)[(1 − π₀(S₀)) + δ₁] = O(log²n)·O_P(2^B√(log n) n^{−κ} + e_n + r_n) → 0,
since 2^B ≤ 2^16 and log^{2.5}n · n^{−min(κ,½)} → 0. Weak variant: on {ζ_n ≤ κ/2}, whose probability → 1,
log²n · 2^B √(log n) n^{−κ/2} → 0. Since T_n ≤ T^max on 𝒢_n, the joint form of (P1) follows.

*(Frozen P2, for completeness.)* (L+4)ρ* ≤ (L+4)(B+3)u_π = O(log n)·19·O_P(r_n) → 0, from T03 alone.

Apply Theorem A. ∎

**Status of Theorem B.** PROVED as a composition, but CONDITIONAL in the register's sense: it is only as strong as
T22(iii)'s open hypotheses EXP′, VIS, NL_η, NL_avg(κ) (not proved for the actual X-dependent partition) and T03's SE and
beta-min (SE is impossible at n = 200, p ≥ 500). The combination T03 + T02(i) without H-T02 was "not separately
reviewed" (LOCKED_PROOFS.md scope notes).

---

## 5. Which premises are genuinely new

| Premise | Discharged by | New? |
|---|---|---|
| (Ω) s₀ ≤ K eventually | R | no |
| (T_n+1)δ₁ → 0 (half of P1, via Lemma 1) | T03(i) + T^max = O(log²n) | no (G, R, SE, BM only) |
| (T_n+1)(1 − π₀(S₀)) → 0 (other half of P1) | T22(iii), CONDITIONAL on EXP′, VIS, NL_η, NL_avg(κ) | **yes: the only genuinely open input.** It is "start concentration at rate o(1/T_n)", i.e. the definition of the favourable regime with a polylog margin |
| (L_n+4)ρ*_n → 0 (frozen P2) | not needed (Lemma 3, Remark 3.2); also implied by T03 | **redundant** |
| (P1-ex) δ₁ → 0 on the exact branch | T03(i), or deterministic-budget (P1) | no |
| ρ̄ ≤ (B+3)u_π (T23's ρ vs ρ*) | Lemma 2 (new, elementary, from T09(ii)) | new lemma, PROVED |
| round-start occupancy | T15 at position (b) + T12(i.b) | no (locked), new use |
| OUT | method construction + EX-A, EX-S | bookkeeping, declared |
| P(𝒪_n) → 1 | — | not claimed |

So the longest hypothesis list in the pool collapses: the composition needs only (Ω), (P1), (P1-ex) and the standing
idealisations. All statistical content sits in two places: T03 (posterior concentration, which gives δ₁ → 0) and the
start concentration 1 − π₀(S₀) = o_P(1/T_n), which is where EXP′ is used.

---

## 6. Proposition C: Theorem B's hypotheses are jointly satisfiable (ORTH family). PROOF SKETCH

Astra's rule ("prove compatible premises jointly") asks for one family satisfying every hypothesis of Theorem B.

**Family ORTH-F.** For each n: standardised design with XᵀX = (n−1)I_p (00_COMMON ORTH), p = p_n ≤ min(n−1, n^A),
G with σ*² fixed, s₀ fixed, θ*_j = θ_j fixed and nonzero for j ∈ S₀ (so ‖μ‖²/(n−1) = Σθ_j² =: M fixed), blocks = any
partition into blocks of size ≤ B (with exact orthogonality all distances 1 − |r_jl| tie, so the method's partition is
fixed by its tie rule; the argument below holds for every partition).

**Claim.** On ORTH-F, G, R, SE, BM-C (eventually), VIS, NL_η (η = 0), NL_avg(κ) (every κ ∈ (0, ½]) and strict EXP′
all hold. Hence Theorem B applies: T26(i)–(ii) holds on ORTH-F, conditional only on EX-A, EX-S, CAL, START, OUT.

*Checks.* R, SE: every R_T = I, φ₀ = 1. BM-C: θ_min² fixed > M_*σ*² log n/n eventually. VIS: for U_b* ⊄ T,
(P_{T∪U*} − P_T)μ = Σ_{j∈U*∖T} θ_j x_j, with squared norm ≥ (n−1)θ_min², while v_T ≤ σ*² + M; take
M_n^V = (n−1)θ_min²/((σ*²+M) log n) → ∞. NL_η: for l ∉ S₀, u_{T,l} = x_l/√(n−1) and x_lᵀμ = (n−1)θ_l = 0, so
δ_{T,l} = 0 on the whole leakage family; η = 0. NL_avg(κ): all E_{T,l} = 0, the average of e^{E} is 1 ≤ n^{½−κ}.

*EXP′ (the only non-trivial check).* For T ⊆ C_b, |T| = k: H_T = ((n+1)(n−1)+1)I = n²I and G_T + I = nI, so
D_T = n^k; z_T = X_Tᵀy and Q_T = yᵀy − ‖z_T‖²/n. The standardised residual sum of squares is
ρ_T := RSS_T/s_y² = yᵀy − ‖z_T‖²/(n−1) (since P_Ty = X_Tz_T/(n−1)), and 1 − x_{T,l} = ρ_{T∪l}/ρ_T (x is
scale-free). Therefore
  log r_b(T∪l)/r_b(T) = −½ log n − ν log[(0.02 + Q_{T∪l})/(0.02 + Q_T)],
  R_{n,b,T,l} = ½ log((n+1)/n) − ν{log(1 + a_{T∪l}/ρ_{T∪l}) − log(1 + a_T/ρ_T)},  a_T := 0.02 + ‖z_T‖²/(n(n−1)).
Since ‖z_T‖²/(n−1) = ‖P_Ty‖² ≤ ‖y‖² = n − 1, a_T ∈ [0.02, 1.02]. For u, v ≥ 0, |log(1+u) − log(1+v)| ≤ max(u, v). So
  max_{b,T,l} |R| ≤ 1/(2n) + (0.01 + n/2)·1.02/ρ_min,  ρ_min := min_b ρ_{C_b}  (ρ_T is decreasing in T).
ρ_{C_b} = ‖(C − P_{C_b})Y‖²/s_y² with (C − P_{C_b}) a projection of rank n − 1 − |C_b| ≥ n − 1 − B; its numerator
stochastically dominates σ*²χ²_{n−1−B}, so a χ² lower-tail bound and a union over J ≤ p ≤ n blocks give
min_b ‖(C − P_{C_b})Y‖² ≥ σ*²(n−1−B)/2 with probability → 1. And s_y² = ‖Y‖²/(n−1) = O_P(1). Hence ρ_min ≥ c n with
probability → 1, and max|R| = O_P(1): strict EXP′ holds. ∎ (sketch)

*Why only a sketch.* The steps are elementary but have not been checked line by line by an independent reader; in
particular the χ² lower-tail constant and the union bound are stated, not written out, and the method's exact tie rule
for the partition under exact orthogonality was not traced (the argument does not depend on it).

*Numerical check* (`scripts/orth_check.py`, `results/orth_check.csv`): with p = n/2, s₀ = 3, θ = 0.6, the maximum of
|R| over **every** within-block addition is 0.11–0.16 for n = 200…6400 (bounded, as claimed).

*Scope.* ORTH requires p ≤ n − 1, so this family does not touch the p ≫ n study design. It shows that Theorem B is not
vacuous, not that its hypotheses hold where the paper's simulations live. This overlaps the W1-EXP task
("EXP in the block-orthogonal benchmark"); HQ should reconcile the two.

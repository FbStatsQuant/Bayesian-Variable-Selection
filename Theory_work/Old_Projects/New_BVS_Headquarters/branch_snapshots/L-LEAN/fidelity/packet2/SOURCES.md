# Source statements for the fidelity check (verbatim excerpts)

## 1. T21 — Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md (excerpts)

### §1 objects (paragraph on F, π, δ1, tie order, scored set, U, Ŝ)
Empty matrices give D_empty=1 and Q_empty=y'y. Let w(k)=1/[2 binom(2p-1,k)], W_K=sum_{k=0}^K binom(p,k)w(k), varpi(S)=w(|S|)/W_K, F(S)=log(varpi(S)m(S)), Z=sum_Omega exp(F(S)), pi(S)=exp(F(S))/Z, delta1=1-pi(S0). A larger F is preferred; exactly equal scores are ordered by smaller size, then lexicographically smaller sorted index list. Sdagger is the unique model selected by this total order on Omega.

The cumulative scored set Sscr contains every model scored in tables, pilot, diagnostics, final initialisations, Gibbs evaluations under SR, accepted and rejected proposals, and local scans. Scores retained for the HPM are never lost through cache eviction. Scal is the subset scored before final randomness (including the tables); Sscr contains Scal. U is the event that no usable HPM output is produced. On U^c, Shat is the total-order maximum of the nonempty Sscr. Expressions 'U or Shat != S0' mean U union {U^c, Shat != S0}, so no output is needed on U.


### §3 (C1)
**(C1)** For every such n and data law,

    P(U or Shat != S0) <= P(U) + 2 E0 delta1 + P(U^c, S0 not in Sscr).

Under H03 the middle term tends to zero. If P(U)->0 and any applicable discovery bound below tends to zero, recovery probability tends to one. The finite bounds, and not merely the name of a route, specify the needed occurrence/exposure conditions.


### Proof of C1 (PROOF_v3.tex lines 52-86)
\begin{theorem}[C1]
For every valid problem and every such joint law,
\begin{equation}\label{eq:C1}
 \Pp\{U\text{ or }\widehat S\ne S_0\}
 \le \Pp(U)+2E_0\delta_1+\Pp\{U^c,S_0\notin\Sc\}.
\end{equation}
Under H03, \(2E_0\delta_1\to0\). Consequently, if \(\Pp(U)\to0\)
and the discovery term tends to zero under one of the conditions established
below, \(\Pp\{U^c,\widehat S=S_0\}\to1\).
\end{theorem}

\begin{proof}
On \(\{\pi(S_0)>1/2\}\), every \(S\ne S_0\) satisfies
\[
 \pi(S)\le1-\pi(S_0)<\pi(S_0).
\]
Thus \(S_0\) is the strict score maximum, with no tie. If it has also been
scored and the output is usable, the method must return it. Hence
\[
 \{U^c,\widehat S\ne S_0\}
 \subseteq\{\delta_1\ge1/2\}\cup\{U^c,S_0\notin\Sc\}.
\]
The first event depends only on the data, and
\(\Pp(\delta_1\ge1/2)=P_0(\delta_1\ge1/2)\le2E_0\delta_1\).
Add \(\Pp(U)\) to get \eqref{eq:C1}.

H03 gives \(\delta_1\to0\) in \(P_0\)-probability, since
\(\sqrt{\log n/n}\to0\). For every \(\epsilon>0\), using
\(0\le\delta_1\le1\),
\[
 E_0\delta_1\le\epsilon+P_0(\delta_1>\epsilon).
\]
Taking a limsup, then \(\epsilon\downarrow0\), proves the asserted mean limit.
This does not assert an \(O(\sqrt{\log n/n})\) frequentist error rate.
\end{proof}

### Form requested in the L-LEAN brief
For events U (no output), the scored set 𝒮, the truth S₀ and the reported Ŝ = argmax of F over 𝒮 with a fixed tie rule, P(U ∨ Ŝ ≠ S₀) ≤ P(U) + P(S₀ ∉ 𝒮) + P(Uᶜ ∧ S₀ ∈ 𝒮 ∧ π(S₀) ≤ ½) and the 2E₀δ₁ form via Markov. Formalise over a finite type of models with a real-valued score and a probability measure.

## 2. T07 — Docs/Theory/proofs/T06_T07_identifiability_size_prior/STATEMENT.md §0 (tie order, scored set) and §2 (all)
- Tie order (method §6.10): ≺ orders models by smaller size, then by the lexicographically smaller sorted index list. S† is the ≺-least element of argmax_Ω F.
- 𝒮 ⊆ Ω is the nonempty set of all scored models. Ŝ is the ≺-least element of argmax_𝒮 F.
## 2. T07: size-only ranking ceiling and Bayes decisions

Setting. m is the marginal likelihood (only m > 0 is used). ≺ is the tie order above; any fixed total order on subsets of [p] works. For a positive size-only prior on Ω, w̃(k) > 0 for 0 ≤ k ≤ K and ϖ_w̃(S) = w̃(|S|)/Σ_{k≤K} C(p,k) w̃(k). S†_w̃ is the ≺-least element of argmax_{S∈Ω} ϖ_w̃(S)m(S). For 0 ≤ k ≤ p, S*_k is the ≺-least element of argmax_{|S|=k} m(S).

**(i) Ceiling.** For every response and every positive size-only prior w̃, {S†_w̃ = S₀} ⊆ {S*_{s₀} = S₀}. Here s₀ ≤ K on the left event, which is empty when s₀ > K. Equivalently: on {S*_{s₀} ≠ S₀} (a within-size ranking error, S₀ beaten or ≺-preceded within its size by m), S†_w̃ ≠ S₀ for every positive size-only prior. No size-only prior repairs it.

**(ii) Bayes decisions.** π is the target posterior on Ω. J₊ = {j : PIP_j > ½} and N₊ = |J₊|. The posterior risk of an action a under a loss L is ρ_L(a) = Σ_S π(S) L(a, S).

(a) For the 0–1 loss on supports, L(a, S) = 1{a ≠ S} with a ⊆ [p]: ρ(a) = 1 − π(a) (with π(a) = 0 for a ∉ Ω). The minimisers over all a ⊆ [p] are exactly argmax_Ω F, and S† is one of them.

(b) For the Hamming loss, L(a, S) = |a △ S| with a ⊆ [p]: MPM = J₊ minimises ρ_H over all subsets of [p]. It is the unique minimiser if and only if no PIP_j equals ½.

(c) Capped. Put ℓ = min(K, N₊). Let a* ⊆ J₊ be the ℓ elements of J₊ with the largest PIPs, with ties at the boundary broken by a fixed deterministic rule. Then a* minimises ρ_H over Ω = {a : |a| ≤ K}.

**(iii) Target versus reported decisions.** (i)–(ii) concern S†, π and PIP. (Interpretation, not a separate claim: for the reported objects they hold only through scoring and estimation events.)

(a) Ŝ = S† if and only if S† ∈ 𝒮. Ŝ minimises the posterior 0–1 loss if and only if 𝒮 ∩ argmax_Ω F ≠ ∅.

(b) {Ŝ = S₀} ∩ {S*_{s₀} ≠ S₀} ⊆ {S*_{s₀} ∉ 𝒮}. (Interpretation, not a separate claim: the ceiling of (i) is a statement about S†; for Ŝ the corresponding event depends on 𝒮.)

(c) Let p̂ ∈ [0,1]^p be any PIP estimate and 𝒜 the action class: all subsets for the MPM rule, Ω for the capped rule. Let â minimise Σ_{j∈a}(1 − 2p̂_j) over 𝒜 (MPM̂ = {j : p̂_j > ½}, or the capped rule of (ii)(c) applied to p̂). For any minimiser a_opt of ρ_H over 𝒜,

  0 ≤ ρ_H(â) − ρ_H(a_opt) ≤ 2 Σ_{j ∈ â △ a_opt} |p̂_j − PIP_j| ≤ 2‖p̂ − PIP‖₁.

MPM̂ = MPM if and only if, for every j, p̂_j > ½ ⇔ PIP_j > ½.

Interpretation (not a separate claim): the scoring events and estimation errors in (a)–(c) are not controlled by (i)–(ii). Their control is the subject of computational results (T21, T23, T26), which this document neither uses nor proves.


### PROOF_v2.tex Lemma psi (b) statement (the capped rule, precise form)
\begin{lemma}[minimising $\psi_q$]\label{lem:psi}
(a) $J_+(q)$ minimises $\psi_q$ over all subsets of $[p]$; it is the unique minimiser iff no $q_j=\tfrac12$.
(b) Let $0\le K'\le p$, $\ell=\min(K',|J_+(q)|)$, and let $a^*\subseteq J_+(q)$ with $|a^*|=\ell$ and $\min_{j\in a^*}q_j\ge\max_{j\in J_+(q)\setminus a^*}q_j$ (conventions $\min\emptyset=+\infty$, $\max\emptyset=-\infty$; such $a^*$ exist, and any deterministic tie-breaking rule at the boundary selects one). Then $a^*$ minimises $\psi_q$ over $\{a:|a|\le K'\}$.
\end{lemma}

### Sharpness (i′) — branch theory/W2-BOOK, theory_campaign/W2-BOOK/PROOF.md §3
**(i′) Sharpness of the ceiling. PROVED.** Assume s₀ ≤ K. Then there is a positive size-only prior w̃ with
S†_w̃ = S₀ if and only if S*_{s₀} = S₀.


## 3. T11(iii) — Docs/Theory/proofs/T11_LLED_scoring_ledger/STATEMENT.md
# STATEMENT — T11(iii): iid π₀ draws of the final run

Source: `theorems/T11_LLED_scoring_ledger.md`, part (iii) only. Method: SMC-BVS v3.0, METHODOLOGY_v3.md
(SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c). Shared definitions: `theorems/00_COMMON.md`.

Original wording (the file's preamble to all parts): "Fix S* ∈ Ω measurable w.r.t. data and 𝓒 (before final
randomness)." Original wording of (iii): "P(S* absent from the final iid draws | 𝓒) = (1 − π₀(S*))^{Q_f} ≤ e^{−Q_fπ₀(S*)}.
The adaptive calibration draw count is never a fixed exponent."

Statement changes: **none.** The items under "Setting" make explicit what the original wording leaves implicit;
none adds a hypothesis beyond the file's assumptions (EX-A, EX-S, CAL) and the method's own specification (item 5
transcribes the method's description of the final run; aborts imposed by the computing environment are outside the
idealised model, as everywhere in this theory).

## Setting

1. **Data.** The data (X, y) are fixed (all probabilities are over the algorithm's randomness given the data). p, n, K,
   the blocks C_1, …, C_J, the tables r_b, γ₀, Z̄₀ and π₀ = γ₀/Z̄₀ on Ω = {S ⊆ [p] : |S| ≤ K} are then fixed
   (they are functions of the data only; METHODOLOGY §6.3). The definitions (00_COMMON §§1–2, METHODOLOGY §5, §6.3):
   - K = min(p, ⌊n/2⌋); the blocks C_1, …, C_J partition [p];
   - size prior ϖ(S) = w(|S|)/W_K for |S| ≤ K, with w(k) = ½/C(2p−1, k) > 0 and W_K = Σ_{k≤K} C(p,k) w(k);
   - tables r_b(U) = m(U)/m(∅) for U ⊆ C_b, where m(·) > 0 is the marginal likelihood, so every r_b(U) > 0;
   - γ₀(S) = ϖ(S) ∏_b r_b(S ∩ C_b) for S ∈ Ω, Z̄₀ = Σ_{S∈Ω} γ₀(S), π₀ = γ₀/Z̄₀.
   Hence π₀(S) > 0 for every S ∈ Ω.
2. **Randomness (EX-S).** The algorithm's randomness is a countable family of independent streams, each an iid sequence
   of Uniform(0,1) variables, with the method's stream separation: the calibration uses streams 0–9 only and the final
   run uses streams 10–13 only. Every random choice of the algorithm is made by reading not-yet-read values from the
   streams; which value is read next is determined by the data and the values read so far. Random operations are
   executed one at a time (each, e.g. one call of the π₀ sampler, completes before the next begins). All maps are Borel
   measurable.
3. **Exactness (EX-A).** Scores, convolutions, probabilities and comparisons are exact. In particular, each call of the
   π₀ sampler (METHODOLOGY §6.3: total size, then block sizes backwards, then each block's sub-model within its size
   class) maps the values it reads to its output by a measurable map (which may depend on the run's state when the
   call starts), and, when the values it reads are iid Uniform(0,1), its output has law exactly π₀.
4. **Calibration output (CAL).** 𝓒 := (grid 0 = φ₀ < … < φ_T = 1, T, L, N_e, tier e, candidate set V, every
   V-independent setting) is a measurable function of the data and streams 0–9; it includes the indicator of the event
   Λ = {the final run is launched} (SMC branch, preflight passed, a grid was produced; all decided before any final
   randomness). On Λ, T ≥ 1 is finite.
5. **Final run** (on Λ; METHODOLOGY §6.8, §6.5). 4 islands, each with N_e particles started from π₀ draws; the frozen
   grid; one move round per stage t = 1, …, T, then L burn-in rounds and 4 measured rounds at φ = 1; so each particle of
   each island goes through T + L + 4 rounds, and each round contains exactly one independence step, whose proposal is a
   π₀ draw (accepted or not). The **final iid draws** are these 4N_e initial draws and 4N_e(T + L + 4) independence
   proposals, in total
   Q_f := 4N_e(T + L + 5),
   a function of 𝓒. A launched final run executes all these rounds (no early stop; aborts imposed by the computing
   environment, such as wall time, are outside the idealised model).
6. **Target model.** S* is an Ω-valued random variable that is a measurable function of the data and 𝓒 (the file's
   "measurable w.r.t. data and 𝓒 (before final randomness)").

## Claim (iii)

On Λ, almost surely,

  P(S* is not among the Q_f final iid draws | 𝓒) = (1 − π₀(S*))^{Q_f} ≤ exp(−Q_f π₀(S*)).

## Scope note (the clause "the adaptive calibration draw count is never a fixed exponent")

The identity is asserted only for the final draws, with the 𝓒-measurable exponent Q_f. Nothing is asserted about the
calibration's π₀ draws: their number is adaptive (it depends on the calibration's own randomness, e.g. through the
rebuild loop and the escalation decision), so the identity is **not** claimed with the calibration draw count in place
of Q_f.


## 4. T37(i) / Theorem A — branch theory/W1-T37R, theory_campaign/W1-T37R/PROOF.md (excerpts)
# W1-T37R — PROOF.md (long proofs and sketches)

Notation: 00_COMMON.md. Throughout, EX-A (exact scores and comparisons), X and S₀ fixed, s₀ ≥ 1.
Neighbourhood N(S) = all *feasible* flips and swaps of S (additions only if |S| < K). The production local
search (METHODOLOGY_v3 §6.10; engine `v3_core.cpp`, `E.local_search(led.hpmS, ell, …)`) is the map

  M(S) = argmax{F(S′) : S′ ∈ N(S), F(S′) > F(S)} (lexicographic tie rule on S′), M(S) = ⊥ if the set is empty,

iterated at most ℓ times from the centre S_c = the current global best scored model, followed by one scan.
For S ∈ Ω write m(S) = |S₀∖S| (missing truths), e(S) = |S∖S₀| (extras), Φ(S) = m(S) + e(S) = |S Δ S₀|.
Region R_{a,d} := {S ∈ R_d : m(S) ≤ a} (so R_d = R_{s₀,d}). Move classes, by the change (Δm, Δe):

| class | moves | (Δm, Δe) | ΔΦ |
|---|---|---|---|
| progress 𝒫 | add truth; delete extra; swap extra→truth | (−1,0), (0,−1), (−1,−1) | −1, −1, −2 |
| neutral 𝒩 | swap truth→truth; swap null→null | (0,0) | 0 |
| regressive ℛ | add null; delete truth; swap truth→null | (0,+1), (+1,0), (+1,+1) | +1, +1, +2 |

## Lemma 0 (monotonicity obstruction; Ŝ after a certified repair). Status: PROVED.

**Statement.** Let S_c be the local-search centre and S_c = S⁰, S¹, …, S^r its path. Then
(a) F(S⁰) < F(S¹) < … < F(S^r); in particular S₀ ∈ {S¹,…,S^r} implies F(S₀) > F(S_c).
(b) In production S_c is the running global best over the pre-search scored set 𝒮_pre. Hence the local search
can make S₀ a centre, or make Ŝ = S₀ (up to exact ties), only on the event E_LS := {S₀ ∉ 𝒮_pre, F(S₀) >
max_{𝒮_pre} F}. On the complement — in particular on every posterior miss F(S₀) ≤ F(Ŝ) — no local search,
with any move cap, delivers S₀ (it may still *score* S₀ as a scanned neighbour, which changes nothing in Ŝ).
(c) If the path reaches S₀ and the search stops there with local_certified (S₀ is the returned scanned centre with
no improving neighbour), then every model scored during the search has F ≤ F(S₀), and Ŝ = S₀ after the
search, except for exact score ties (then the tie rule decides). No condition π(S₀) > ½ is needed.

## Definitions for the refined statement

For a finite family 𝓡 ∋ S₀ of feasible models:

* **TD′_∞(𝓡)** (no spurious local maximum + closure):
  (L) M(S₀) = ⊥ (S₀ has no strictly improving feasible flip or swap);
  (N) for every S ∈ 𝓡∖{S₀}: M(S) ≠ ⊥ and M(S) ∈ 𝓡.
* **TD′_P(𝓡)** (progress): (L), and for every S ∈ 𝓡∖{S₀}: M(S) ≠ ⊥ and M(S) is a progress move
  (equivalently Φ(M(S)) < Φ(S); by the class table ΔΦ < 0 exactly on 𝒫).
* **TD′_path(S_c)**: the capped production search from the centre S_c returns S₀ with local_certified.
* **D_S** (one-state progress event), S ∈ Ω∖{S₀}: max_{S′∈𝒫(S)} F(S′) > max{F(S), max_{S″∈𝒩(S)∪ℛ(S)} F(S″)},
  where 𝒫(S), 𝒩(S), ℛ(S) are the feasible progress/neutral/regressive neighbours of S.
  (TD′_P(𝓡) ⟺ (L) ∧ ⋂_{S∈𝓡∖S₀} D_S, ties among top progress moves allowed.)
* **Lattice of a centre.** For S = U ∪ P (U ⊆ S₀, P ∩ S₀ = ∅): Lat(S) := {U′ ∪ P′ : U ⊆ U′ ⊆ S₀, P′ ⊆ P},
  |Lat(S)| = 2^{Φ(S)}. For a class 𝒞: Lat(𝒞) = ⋃_{S∈𝒞} Lat(S). R_{a,d} is a union of lattices.
* **NA_d** (no addable null over the superset tree): for all P′ ⊆ S₀ᶜ with |P′| ≤ d and |S₀ ∪ P′| < K and all
  nulls l ∉ S₀ ∪ P′: F(S₀ ∪ P′ ∪ {l}) < F(S₀ ∪ P′).
* **TL_d** (truths locked once covered): for all P′ with |P′| ≤ d, every feasible move from S₀ ∪ P′ that removes a
  truth (deletion of a truth or swap with a truth going out) has strictly negative gain.

## Lemma 2 (lattice closure; superset reduction). Status: PROVED.

(a) Progress moves map Lat(S) into Lat(S); R_{a,d} is closed under progress moves; Φ ≤ m(S) + e(S) on Lat(S).
(b) On NA_d ∩ TL_d: M(S₀) = ⊥, and for every S = S₀ ∪ P with 1 ≤ |P| ≤ d, M(S) is the deletion of an extra
(so D_S holds and M(S) ∈ R_{0,d}).

**Proof.** (a) S′ = U′ ∪ P′ ∈ Lat(S). Add truth j ∈ S₀∖U′: U′+j ⊇ U, ⊆ S₀. Delete extra l ∈ P′: P′−l ⊆ P.
Swap extra l → truth j: both. Membership in R_{a,d}: m and e do not increase and |S′| ≤ s₀ + d ≤ K.
(b) At S₀: an addition is a null addition, gain < 0 by NA_d with P′ = ∅; any deletion or swap removes a truth
(S₀ contains only truths), gain < 0 by TL_d. So M(S₀) = ⊥. At S = S₀ ∪ P, e = |P| ≥ 1: for l ∈ P, with
P′ = P − l (|P′| = e − 1 ≤ d − 1, |S₀ ∪ P′| = s₀ + e − 1 < K), NA_d gives F(S) < F(S − l), i.e. h(S, l) > 0. A
null addition l′ ∉ S (if |S| < K) has g(S, l′) < 0 by NA_d with P′ = P. A null→null swap l → l′ has gain
h(S, l) + g(S − l, l′) < h(S, l) by (SW) and NA_d at P − l. Truth-removing moves have negative gain (TL_d).
Hence the best gain is max_{l∈P} h(S, l) > 0, attained only by extra deletions; the lexicographic rule picks one of
them. ∎

## Theorem A (refined T37(i): deterministic greedy repair). Status: PROVED.

Assume EX-A; X, y fixed; ℓ the production move cap.
(A1) *Characterisation.* TD′_∞(𝓡) holds iff for every S ∈ 𝓡 the uncapped greedy path from S stays in 𝓡 and
terminates at S₀. Under TD′_∞(𝓡) the path from S has at most r_𝓡(S) := #{S′ ∈ 𝓡 : F(S′) > F(S)} moves.
(A2) *Progress version.* Under TD′_P(R_{a,d}), from every S ∈ R_{a,d} the greedy path stays in Lat(S) ⊆ R_{a,d},
Φ strictly decreases at each move, and S₀ is reached after τ(S) = m(S) + e(S) − σ(S) ≤ Φ(S) moves, where σ(S) is
the number of extra→truth swaps used (τ(S) ≥ max{m(S), e(S)}).
(A3) *Production search.* If TD′_P(R_{a,d}) holds and ℓ ≥ a + d (or merely ℓ ≥ τ(S_c)), then from any centre
S_c ∈ R_{a,d} the production local search returns S₀ with local_certified, without local_limit, and after it
Ŝ = S₀ up to exact ties (Lemma 0(c)). The same holds with TD′_P(R_{a,d}) replaced by the *lattice* condition
(L) ∧ ⋂_{S′∈Lat(S_c)∖S₀} D_{S′}, which involves 2^{Φ(S_c)} states only.
(A4) *Necessity.* Each of the conclusions implies PD on the respective set (F(S₀) > F(S) for S ≠ S₀ in 𝓡,
resp. in Lat(S_c) along the path); the conclusion of (A1) for all S ∈ 𝓡 implies TD′_∞(𝓡); the conclusion
"every greedy path from R_{a,d} decreases Φ at each step and ends at S₀" implies TD′_P(R_{a,d}).
(A5) *Relation to literal TD.* Literal TD(d,0) strict ⇒ TD′_P(R_d); for d ≥ 1 the premise is never satisfied
(Prop 1), for d = 0 it is satisfiable. TD′_P(R_{a,d}) ⇒ TD′_∞(R_{a,d}); the converse fails (Exp 3).


### Repair R3 — branch theory/W3-VT37R, REPAIRS.md
## R3. "What is weakest" (prose after Theorem A). Status: COUNTEREXAMPLE to the prose; A4 itself VERIFIED.

W1 claims that, among statements keeping the move count ≤ Φ, TD′_P is necessary and sufficient. A4 proves necessity only
for the statement "every greedy move decreases Φ". The weaker property PHI-REACH(R) says that every greedy path from every
S ∈ R ends at S₀ within Φ(S) moves. On the exhaustive designs (`scripts/phi_reach_vs_TDP.py`) it held **without TD′_P in 23
of 360 datasets**.
- Example: scenario 2, n = 40, c = 1, rep 7, S₀ = {2,6,13}, centre {5,6,12}, so Φ = 4.
- The path is {5,6,12} → {2,5,12} → {2,5,13} → {2,6,13}: 3 moves ≤ Φ.
- Its first move is a neutral truth→truth swap.

The −2 swaps buy back the neutral move. **Correct prose:** TD′_P is necessary and sufficient for "every greedy move from R
decreases Φ" (A4). For "reach S₀ within Φ moves", TD′_P is sufficient but not necessary.

The phrase "the cap needs ℓ ≥ a + d" should also read "ℓ ≥ a + d suffices". The exact requirement is ℓ ≥ τ(S_c), and
max(m, e) ≤ τ ≤ Φ.


## 5. T12(i.a) — Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md §3
**(i) Evidence identities.**
- (i.a) For every c, t ∈ {0, …, T} and f : Ω → ℝ: E_c[Ẑ_t q̂_t(f)] = Z_t q_t(f). In particular E_c[Ẑ] = Z.
(Only a partial formalisation is claimed for T12(i.a): see the docstring of T12Core.lean. Judge whether the partial results are correctly described and whether the reduction theorem's hypotheses are an honest rendering of the remaining step.)

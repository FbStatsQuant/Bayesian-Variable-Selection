# Independent Claude audit of T21 and T25(iv)

Auditor: Claude Opus 5.5 (review sub-agent). Date: 2026-10-22. Read-only audit, run locally. I compiled nothing new; the existing LaTeX logs `PROOF_v2.log` (T21) and `PROOF_v1.log` (T25iv) show 0 errors. I ran one inline numerical check (no files written), described under T21 finding E2.

**Bottom line.**
- **T21: correct, with exposition fixes.** No fatal flaw and no gap. Two small wording fixes are suggested. Separately, I found that one hypothesis, H10, seems to follow from the score formula itself, so it could probably be removed.
- **T25(iv): correct, with exposition fixes.** No fatal flaw and no gap. Felipe should know that the result follows almost immediately from its assumption PW2. All of the difficulty lies in proving PW2, which nobody has done yet.

## 0. What I read, and in what order

Blind phase (Step 1), for each theorem: `STATEMENT.md`, the proof (`PROOF_v2.tex` for T21, `PROOF_v1.tex` for T25iv), and the original conjecture in `theorems/`. I also read the allowed context files: `theorems/00_COMMON.md` (definitions of SR, HIT, PX, ONE, PW2), `THEORY_BRIEF.md` (grep only), `METHODOLOGY_v3.md` §§3 and 6.1–6.13, and the cited chapters of `COLLECTED_PROOFS_v2.tex`: T09(i)–(iii), T11(iii) with its reading-scheme proposition, T12 statement and Lemmas "elementary steps are q_φ-reversible" and "state-independent prefixes", and T20(ii-A).

Only after writing down my blind findings did I read the two `CLAIMS_OF_FATAL_FLAWS.md` files and `WAVE2_REVIEW/REVIEW.md` (Step 2).

I did not open the conjecture files for T03, T10 or T24, because they are not among my listed inputs. So H03, H10 and H24 are checked against the T21 conjecture text, `00_COMMON.md`, and (for H03) the wording of H03 inside wave-1 T20(ii-C). They are not checked against the T03, T10 and T24 files themselves.

---

## 1. T21: blind audit

### 1.1 Statement fidelity

| Original (T21 conjecture) | STATEMENT.md | Judgement |
|---|---|---|
| C1 bound; "middle term → 0 by T03" | Same bound; T03 replaced by hypothesis H03 (δ₁ = O_P(√(log n/n))) | Faithful. H03 has the same form as the H03 used in wave-1 T20(ii-C), line 3230 of the collection. |
| (a) fresh-iid bound; "Q_fπ₀(S₀) → ∞ on launched runs"; one-deletion corollary "T10 gives π₀(S₀) ≥ c·r_{s₀−1}" | Same bound. "→ ∞ on launched runs" is made precise as P(F, Q_fπ₀(S₀) ≤ M) → 0 for every M. T10 is replaced by H10. | Faithful. The precise form is the natural reading. |
| (b) Gibbs execution; round-start occupancy is not enough | Same, with the event E_G made explicit | Faithful |
| (c) swap hazard b = 1/[k(p−k)]; stopped bound δ + (1−b)^D; PX; neighbour-swap formula | Same. PX is written as P(no hit, O < ⌈ω_n k(p−k)⌉) → 0. The neighbour-swap extension is limited to a deterministic b_* (or a conditional random b_*). | Faithful. The b_* restriction makes precise a claim the original left vague; it does not weaken the theorem. |
| (d) tables and completed scans (T20(ii)) | Same, with the event E_TS made explicit | Faithful |
| (e) "Under T24 … ≤ (1−a_n)^H + Hη_n"; availability; nonlaunch term; pilot filtration | H24 assumes T24(i)'s one-round inputs (K₁(x,{S₀}) ≥ a_n and one-round exit ≤ η_n, uniformly on R_d). The H-round bound is then **proved**. For the asymptotic claim, H24 also assumes T24's conclusions a_n ≥ c_n/2 and (L+4)η_n → 0. | Faithful, and slightly stronger than needed, because the H-round bound is derived rather than assumed. T24 appears only as a hypothesis, as Felipe required. |
| (f) exact branch; fixed p eventually enumerated | Same | Faithful |

Assumptions: EX-A, EX-S, CAL, SR, operational availability, and the route-specific conditions all appear explicitly. G/R/SE/BM-C appear only as background to H03; they are never used. OP-s is correctly marked as unnecessary when tables or calibration supply the score.

**Requirement "T03, T10, T24 only as explicit hypotheses": met.** I searched the proof for any use of T03/T10/T24 beyond H03/H10/H24 and found none. The ledger facts that the original takes from T11 (iv) and (vii), which are not proved in wave 1, are proved directly in the text (C1 proof; route (c) proof).

### 1.2 Step-by-step check, with my own algebra

**C1.** Suppose π(S₀) > 1/2. Every S ≠ S₀ then has π(S) ≤ 1 − π(S₀) < 1/2 < π(S₀). Since π ∝ e^F, S₀ is the strict maximiser of F, so the tie-break rule never applies. On U^c the method returns the maximum of 𝒮 in the total order, so S₀ ∈ 𝒮 gives Ŝ = S₀. Hence {U^c, Ŝ ≠ S₀} ⊆ {δ₁ ≥ 1/2} ∪ {U^c, S₀ ∉ 𝒮}. By Markov's inequality, P₀(δ₁ ≥ 1/2) ≤ E₀δ₁/(1/2) = 2E₀δ₁. Adding P(U) gives C1. Under H03, δ₁ → 0 in probability. Because 0 ≤ δ₁ ≤ 1, E₀δ₁ ≤ ε + P₀(δ₁ > ε) → ε, so E₀δ₁ → 0. **Correct.**

**(a).** The method (§6.8) runs 4 islands of N_e particles each. Each particle makes T stage rounds, then L burn-in rounds, then 4 measured rounds, so T+L+4 rounds. Each round contains exactly one independence proposal drawn from π₀, and every proposal is scored (§6.5). Hence Q_f = 4N_e + 4N_e(T+L+4) = 4N_e(T+L+5). This count is fixed by the pre-final history.

The wave-1 proposition "final run is a reading scheme" (collection, lines 793–839) fixes the whole value υ of streams 0–9. So it conditions on the entire pre-final history, not just on 𝒞, which is exactly what T21 uses. Under that conditioning the designated draws are iid π₀. Therefore P(S₀ ∉ 𝒟_f | ℋ_cal) = (1−π₀(S₀))^{Q_f}, and 1{S₀ ∉ 𝒮_cal} is ℋ_cal-measurable. The event inclusion is

{S₀ ∉ 𝒮} ⊆ {F^c, S₀ ∉ 𝒮_cal} ∪ {F, S₀ ∉ 𝒮_cal, S₀ ∉ 𝒟_f}.

The tower property then gives the displayed bound. Using 1−x ≤ e^{−x} and E[1_F e^{−Qπ₀}] ≤ P(F, Qπ₀ ≤ M) + e^{−M} finishes the asymptotic statement. **Correct.**

One-deletion corollary. With k = s₀−1, r_k = (k+1)/[(2p−k−1)√(n+1)] = s₀/[(2p−s₀)√(n+1)]. The addition is feasible because k = s₀−1 < s₀ ≤ K. Therefore Q_fπ₀(S₀) ≥ 4cs₀N_e(T+L+5)/[(2p−s₀)√(n+1)].

If p ≤ C√n, then N_e ≥ N₀ ≥ n, 2p − s₀ ≤ 2C√n, and T ≥ 1, so the right side is at least (2cs₀/C)·√(n/(n+1))·(L+6) → ∞, because L ≥ ⌈log₂(n+1)⌉. **Correct.**

**(b).** At the execution, A = X_pre−j ∖ {j} = S₀ ∖ {j}. If j ∈ S₀, then A ∪ {j} = S₀. If j ∉ S₀, then A = S₀. In both cases S₀ is a feasible configuration (|S₀| ≤ K), so SR scores it. One cap case needs a separate look: j ∉ S₀ with |S₀| = K. Then X_pre−j cannot contain j, because that state would have size K+1. So X_pre−j = S₀ is the current state, and SR counts the current configuration as scored. **Correct.**

**(c).** From the proxy S = (S₀∖{l}) ∪ {j}, the uniform swap deletes a uniform element of S (probability 1/k for j) and inserts a uniform element of [p]∖S (probability 1/(p−k) for l, since l ∉ S). This matches §6.5, where the swap is skipped only at |S| ∈ {0, p}. So b = 1/[k(p−k)].

Stopped bound. Let τ_i be the i-th counted execution, which is a stopping time for the chronological history. Let A_i be the event that τ_i < ∞ and the i-th proposal misses S₀. Then {τ_i < ∞} ⊆ A_{i−1}, because a hit stops the counting. Also P(A_i) = Σ_m E[1{τ_i = m}(1−b)] = (1−b)P(τ_i < ∞) ≤ (1−b)P(A_{i−1}). Induction gives P(A_i) ≤ (1−b)^i. If no hit occurs and O ≥ D, then A_D occurs. So P(S₀ ∉ 𝒮) ≤ δ + (1−b)^D. For PX, take D = ⌈ω_n k(p−k)⌉; then (1−b)^D ≤ e^{−bD} ≤ e^{−ω_n}. **Correct.** The neighbour swap hit probability is (1/k)(1/|N(j)∖S|) when l ∈ N(j), which matches §6.5. **Correct.**

**(d).** First, B ≤ K. For n ≥ 4, √n ≤ n/2, so ⌊√n⌋ ≤ ⌊n/2⌋; for n = 3 both equal 1. Also ⌊√p⌋ ≤ p. So every block sub-model is feasible, and §6.3 says "Every table score counts for the HPM". Second, the feasible flip/swap neighbourhood is symmetric. The reverse of an addition is a deletion. The reverse of a deletion is an addition back to S₀, which is feasible because |S₀| ≤ K. A swap is reversed by the opposite swap. §6.10 scans every feasible flip and swap, including "one further scan" at the move cap. So a completed scan centred at a neighbour of S₀ scores S₀. This matches T20(ii-A) step 1 (collection, line 3225). That step does not need T20's strict-optimality event E_n, which wave-1 T20 uses only for steps 2–4. **Correct.**

**(e).** Fix the past at selection. Let B_h be the event: no exit from R_d through round h, and no round end so far equals S₀. On B_{h−1}, round h starts in R_d. The future order and uniforms are fresh, and there is no resampling at φ = 1 after stage T (§6.8; T12's island definition). So P(B_h) ≤ E[1_{B_{h−1}}(1 − K₁(X_{h−1},{S₀}))] ≤ (1−a)P(B_{h−1}).

The first-exit union bound gives P(J) ≤ Hη. Without an exit, every round starts in R_d, so {no truth endpoint} ⊆ J ∪ B_H. A round that ends at S₀ scores S₀ during that round: the step that moves into S₀ scores it, and if the particle sits at S₀ during a Gibbs step, SR re-scores it. So P(no truth score) ≤ (1−a)^H + Hη.

The bounds for an availability event A, and for the final run with A_F, follow by splitting the event and taking expectations. Asymptotically, Ha_n ≥ (L+4)c_n/2 with c_n ≥ 1/(s₀+d+18)!, which is a fixed positive constant, and L → ∞. So Ha_n → ∞ and (1−a_n)^H ≤ e^{−Ha_n} → 0. The capped expectation then tends to 0 by bounded convergence. **Correct.**

**(f).** §6.2 enumerates all of Ω with the same strict order as §6.10, accumulating Z and the PIP numerators. Under EX-A these sums are exact, so 𝒮 = Ω, Ŝ = S†, the evidence is Z, and each PIP is Z_j/Z. For fixed p, Σ_{k≤K} C(p,k) ≤ 2^p, while (5H₀+4N₀)p ≥ 4np → ∞. **Correct.**

### 1.3 Cited wave-1 results

| Citation | What the collection proves | Match? |
|---|---|---|
| T11(iii) and its reading-scheme proposition | iid π₀ for any class of designated calls with a fixed count Q, given a fixed υ (all of streams 0–9); Q_f = 4N_e(T+L+5) (lines 629–640, 793–839) | Yes. Conditioning on the full pre-final history is covered, because υ is fixed. |
| T20(ii-A), step 1 | "scan k scores S₀ (S₀ ∈ 𝒩(c_k))" on E_n (line 3225) | Yes. T21 proves this step directly without E_n, and the argument is valid. |
| T09(i) | exact Z̄₀ and iid π₀ sampler | Yes. As T21 says, it is not needed for route (f). |

### 1.4 Blind findings for T21

**E1.** Location: STATEMENT §3(e), first display, and proof eq. (repair). Severity: **exposition**. Claim: the event "no truth score in those H rounds" is ambiguous when the selected state already is S₀, or when S₀ was scored earlier. Evidence: the proof handles the case x = S₀ by saying that "the whole-run miss event is empty". That argues about a different event from the one in the display. The bound holds under either reading (see 1.2(e)), but the event should be named precisely. Exact wording, replacing "P(no truth score in those H rounds | available past) <= (1-a_n)^H+H eta_n.":

> Let M_H be the event that S₀ ∉ 𝒮 when those H rounds end. Then P(M_H | available past) ≤ (1−a_n)^H + Hη_n.

In the proof, use M_H in place of "no truth score in the next H rounds" in eq. (repair), and in the sentence after it.

**E2.** Location: STATEMENT §2, H10, and §3(a). Severity: **exposition, an optional strengthening, not a defect**. Claim: H10 seems to be a deterministic fact about the method's score, so it may not need to be a hypothesis.

Derivation. Let |S| = k < K, j ∉ S, b the block of j, and U = S ∩ C_b. Then

π₀(S+j)/π₀(S) = [w(k+1)/w(k)]·r_b(U+j)/r_b(U) = [(k+1)/(2p−1−k)]·m(U+j)/m(U).

The prior part comes from w(k+1)/w(k) = C(2p−1,k)/C(2p−1,k+1) = (k+1)/(2p−1−k). For the likelihood ratio m(U+j)/m(U), take the Schur complement in j. Write G = G_U, g = X_U'x_j, γ = x_j'x_j and ε = 1/(n+1). Then

D_{U+j}/D_U = {(n+1)[γ − g'(G+εI)⁻¹g] + 1} / {γ + 1 − g'(G+I)⁻¹g}.

This is at most n+1 if and only if (n+1)g'[(G+I)⁻¹ − (G+εI)⁻¹]g ≤ n. That holds because the left side is ≤ 0: ε ≤ 1 implies (G+εI)⁻¹ ⪰ (G+I)⁻¹.

Next, Q_U = min_β {y'y − 2β'z_U + β'A_Uβ}, with A_U = ((n+1)G_U + I)/n positive definite. A_U is the principal submatrix of A_{U+j}, so Q_{U+j} ≤ Q_U, and Q ≥ 0 by §6.13. Hence m(U+j)/m(U) ≥ (n+1)^{−1/2}, and π₀(S+j) ≥ r_kπ₀(S) for every feasible addition. That is H10.

Numerical check (inline Python, not saved): over 3000 random cases with n ∈ [3,40) and p ∈ [2,10), including near-collinear and exactly duplicated columns, the minimum of log[m(S+j)/m(S)] + ½log(n+1) was +0.0132, never negative.

I have not seen the T10 file, which may claim more than this inequality. Recommendation: have a reviewer confirm this short lemma; then H10 can be dropped from T21(a). No change is required for T21 to be correct as stated.

**E3.** Location: STATEMENT §3(a), "the start mode Stilde0=S0 minus {i}". Severity: **exposition**. Claim: the proof says, correctly, that being the start mode is not needed. Exact wording:

> If s₀ ≥ 1 is fixed, i ∈ S₀, and S̃₀ = S₀∖{i} has π₀(S̃₀) ≥ c > 0 (S̃₀ need not be the start mode), …

**E4.** Location: STATEMENT §1 (swap definitions) and §3(c). Severity: **exposition, cosmetic**. Claim: the letters j and l are used both for the generic swap (delete j, add l) and for the proxy (l ∈ S₀ removed, j ∉ S₀ added). The two uses agree in meaning, but a reader new to the field may stumble. Optionally add after the proxy definition: "the swap that produces S₀ deletes j and inserts l."

No fatal flaw and no gap.

---

## 2. T25(iv): blind audit

### 2.1 Statement fidelity

- The original asserts the Var_𝒞(W_T) bound under PW2, "divided by four under island pooling". STATEMENT gives the single-island bound B_T with N = N_e particles per island (§3 of the method: "N₀ final particles per island"), and Var_c(W_pool) ≤ B_T/4 for W_pool = ¼Σ_r W_{r,T} = Ẑ/Z. This matches §6.12, where the pooled Ẑ is the arithmetic mean of the four islands. **Faithful.**
- STATEMENT requires a_t, ν_t ≥ 0. The original does not state a sign. The proof uses only α_t = 1 + a_t/N ≥ 0, so this is a mild narrowing that does not matter in practice (see E6).
- The island description (multinomial resampling at every stage including T, then one round per stage, then L+4 rounds at φ = 1 that leave Ẑ unchanged) matches §6.6, §6.8 and §6.12 of the method.

### 2.2 My re-derivation

*Evidence recursion.* From Ẑ_t = Ẑ_{t−1}q̂_{t−1}(G_t) and Z_t = Z_{t−1}c_t with c_t = q_{t−1}(G_t), we get

W_t = Ẑ_t/Z_t = W_{t−1}·q̂_{t−1}(G_t)/c_t = W_{t−1}q̂_{t−1}(g_t).

*First moment.* Each child picks a parent with probability ∝ G_t and then moves by the order-averaged round kernel K_t. Hence E[q̂_t(f) | ℱ_{t−1}] = q̂_{t−1}(G_tK_tf)/q̂_{t−1}(G_t). Multiplying by the ℱ_{t−1}-measurable W_t = W_{t−1}q̂_{t−1}(G_t)/c_t gives E[W_tq̂_t(f) | ℱ_{t−1}] = W_{t−1}q̂_{t−1}(g_tK_tf).

By induction, E_c[W_tq̂_t(f)] = q_{t−1}(g_tK_tf) = q_t(K_tf) = q_t(f). The step q_{t−1}(g_t h) = q_t(h) holds because g_t q_{t−1} = q_t. The last equality uses q_t-invariance (T12, reversibility and prefix lemmas). With f ≡ 1, E_cW_t = 1. **Correct.**

*Variance recursion.* W_t² − W_{t−1}² = W_{t−1}²[(q̂_{t−1}(g_t))² − 1] holds pathwise. Taking E_c gives M_t − M_{t−1} = E_c[W_{t−1}²{(q̂_{t−1}g_t)² − 1}], **with equality**. So PW2 says exactly that M_t ≤ α_tM_{t−1} + ν_t, where α_t = 1 + a_t/N.

Unrolling from M₀ = 1 gives M_T ≤ ∏_{t≤T}α_t + Σ_s ν_s∏_{t>s}α_t. Then Var_c(W_T) = M_T − 1 ≤ B_T. Check at T = 1: M₁ ≤ α₁ + ν₁, so Var ≤ a₁/N + ν₁ = B₁. **Correct.**

*Pooling factor.* Given c, the four islands are independent (T12(iv.c), statement line 1240). So Var_c(¼Σ_r W_{r,T}) = (1/16)Σ_r Var_c(W_{r,T}) ≤ (1/16)·4B_T = B_T/4. The whole bound, including the slack sum, is divided by 4, and N stays N_e. Replacing N_e by 4N_e would be wrong: it divides only the a_t/N part, not the slack terms ν_s. **Correct.**

*Finiteness.* Each factor q̂(G_t) lies in [e^{Δ_t d₋}, e^{Δ_t d₊}], so W_t is bounded given c. **Correct.**

### 2.3 Cited wave-1 results

T12(i.a) is E_c[Ẑ_tq̂_t(f)] = Z_tq_t(f) (line 1225). T12(iii) is the conditional-on-𝒞 version. T12(iv.c) is independence of the islands given 𝒞, which is not claimed after averaging over 𝒞 (the proof uses it given c, which is correct). Invariance is proved in the T12 lemmas at lines 1303–1329. All match.

### 2.4 Blind findings for T25(iv)

**E5.** Location: proof §3, eq. (increment), and STATEMENT "PW2 hypothesis and conclusion". Severity: **exposition, important for interpretation**. Claim: PW2 is not a side condition. It *is* the second-moment step, because the left side of PW2 equals M_t − M_{t−1} exactly. So T25(iv) is a discrete Grönwall (unrolled recursion) bound with no further probabilistic content, apart from E_cW_T = 1 and island independence. This is correct and is what the original asks for ("Establishing PW2 with useful constants is the missing task"), but a reader could mistake the theorem for progress on evidence accuracy. Exact wording to add after eq. (rec) in the proof:

> By (increment), PW2 is equivalent to the recursion M_t ≤ (1 + a_t/N)M_{t−1} + ν_t. The theorem therefore adds no control of the evidence beyond PW2 itself; all of its substance lies in establishing PW2 with useful constants, which is not done here.

**E6.** Location: STATEMENT, "Let a_t and nu_t … be finite nonnegative". Severity: **exposition, optional**. Claim: the proof needs only a_t ≥ −N, and ν_t may be any real number. The restriction is harmless and can be kept. If it is kept, add "(nonnegativity is not needed by the proof beyond a_t ≥ −N)".

**E7.** Location: STATEMENT, "When PW2 holds with the same bounds for each island". Severity: **exposition, cosmetic**. Claim: given c the islands are identically distributed, so PW2 for one island implies it for all four. Suggested wording: "Since the four islands are iid given c, PW2 for one island holds for each."

No fatal flaw and no gap.

---

## 3. Comparison with the OpenAI review record (Step 2)

**T21, `CLAIMS_OF_FATAL_FLAWS.md`.** The only logged item is the statement checker's round-1 objection: a "predictable" random b_* cannot be inserted unchanged into the unconditional scalar bound δ + (1−b_*)^D. **I agree** with the objection and with the fix (a deterministic b_* for the unconditional version; a conditional random b_* followed by averaging). The final proof implements it, and my check of route (c) confirms it. I also agree with the checker's six affirmative scope readings. Both Sol reviewers reported no findings, which is consistent with my audit: none of my findings is fatal or a gap.

**T25(iv), `CLAIMS_OF_FATAL_FLAWS.md`.** No findings from either reviewer. **I agree** that there is no fatal flaw or gap.

**`WAVE2_REVIEW/REVIEW.md`** (T21 and T25(iv) sections, the R1 ruling, and the citation table):
- **Agree** with "verified" for both theorems, with the route-by-route table for T21, and with the citation cross-checks: T11(iii) with full-υ conditioning, T20(ii-A) step 1 without E_n, T12(i.a)/(iii)/(iv.c), and invariance in the T12 lemmas. I checked each of these against the collection myself.
- **Agree** with R1 ("gap in superseded wording, resolved"). It concerned the proposed statement, not the final one.
- **Mild disagreement on emphasis, T25(iv).** REVIEW says the proof "applies PW2 to obtain" the recursion, as if that were a substantive step. It is an identity (E5 above). This is not an error in REVIEW, but its summary could leave the impression that T25(iv) advances evidence control. It does not, without PW2.
- **Addition not in REVIEW, T21.** REVIEW treats H10 as an irreducible conditional input. My E2 shows it seems to be a deterministic lemma. This does not affect correctness.
- **Small addition, T21.** REVIEW does not flag the event ambiguity in E1. It is exposition only.
- REVIEW's claim of acyclic dependencies is consistent with what I saw: T21 uses no T27 conclusion, and T25(iv) uses no T15/T23 conclusion.

---

## 4. Verdicts

| Theorem | Verdict | Exact wording fixes |
|---|---|---|
| **T21** (C1, routes (a)–(f)) | **Correct, with exposition fixes** | E1 (name the event M_H in route (e)); E3 ("S̃₀ need not be the start mode"). Optional: E4. Recommended follow-up: E2 (prove H10 as a lemma, then drop it). |
| **T25(iv)** | **Correct, with exposition fixes** | E5 (add the sentence saying PW2 is equivalent to the recursion). Optional: E6, E7. |

In plain words for Felipe:
- **T21** is a careful bookkeeping theorem. The method fails to report the true model only if (i) no output is produced, (ii) the posterior does not put more than half its mass on the truth, or (iii) the truth was never scored. Each "route" is a separate way to bound (iii). All the steps are right. The real difficulty sits in the assumed inputs (H03, H24, and the exposure conditions such as PX), which remain unproved.
- **T25(iv)** is correct but contains little beyond its assumption PW2. Once you assume PW2, the variance bound follows by unrolling a one-line recursion. The four-island factor 1/4 is right and applies to the whole bound. The open research problem is to prove PW2 for the actual method.

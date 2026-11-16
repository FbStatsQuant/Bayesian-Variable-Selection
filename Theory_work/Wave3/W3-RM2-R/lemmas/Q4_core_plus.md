# Q4 — Theorem RM0-plus (core): sub-lattice form, mode form, and the delivery form (claim W3-RM2-R:RM0-plus; STATEMENT (C0⁺))

Status: **PROVED (by this seat, unchecked)** — 2026-11-16, lead Claude Opus 5.5. Ticket W3-RM2-R; statement:
`../STATEMENT.md` v1.0 §2 (𝓜_n, [MODE], St_n(𝓛′), NA(𝓛′), TL(𝓛′), Sand_n(𝓛′), (D)), §3 (C0⁺).
**This file is a copy** of RM `Theory_work/Wave3/W3-RM/lemmas/L0_core.md` (claim W3-RM:RM-0@1.0.0, "PROVED-CHECKED";
sha256 prefix 51676910b103dac6 in `../DEPS.tsv`); **changed lines are marked [R-#]**; unmarked lines are the parent's.
RM := `Theory_work/Wave3/W3-RM/`; file references below that start with `../` in the parent text are relative to RM
(`RM/lemmas/`) [R-0]. New: (a′) [R-2], (b⁺) [R-3], (c⁺) [R-4]. Part (a), the archive corollary and the remarks are the
parent's.

Inputs (statuses verbatim):
* [L1.2] GROW `lemmas/L1_descent.md:42-57` (Lemma L1.2; "PROVED (by this seat, unchecked)"; R03 "VERIFIED"), a
  deterministic statement: on NA(𝓛) ∩ TL(𝓛), for every centre C ∈ 𝓛, the uncapped greedy path deletes one element of
  C ∖ S₀ per move and reaches S₀ after exactly |C ∖ S₀| moves; the capped search with cap ℓ scores S₀ if
  ℓ ≥ |C ∖ S₀| − 1 and, if ℓ ≥ |C ∖ S₀|, ends at S₀ with a completed scan finding no strict improvement, without
  `local_limit`. Its hypotheses: S₀ ⊆ Q ⊆ [p], |Q| ≤ K (GROW `lemmas/L1_descent.md:9-11`); "no bound on |Q| enters
  this lemma" (GROW `lemmas/L1_descent.md:57-61`, Remark (1)) [R08-16].
* [DLV] DLV `lemmas/L4_delivery.md:65-70`, Claim: 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ (for n with |S₀| ≤ K), proved
  pathwise from OP-LS0, e4 and the absence of interruption; "CAL is not used" (DLV `lemmas/L4_delivery.md:75`). Status
  (verbatim): "PROVED (by this seat); R04 VERIFIED-WITH-AMENDMENTS" (DLV `lemmas/L4_delivery.md:3-4`); DLV report row C2
  "PROVED-CHECKED (pathwise argument supplied by R04; council round 2)" [C1-B1]. Not load-bearing: (b) below re-proves it.
* [OP] GEN `lemmas/L5_assembly.md:11-16` ("PROVED (by this seat, unchecked)" inside GEN "PROVED-CHECKED").
* [E4] RM `lemmas/L5_E4.md` (W3-RM:E4@1.0.0, "PROVED-CHECKED") [R-0].
* [DLV-0] `Q5_dlv0.md` of this folder (claim W3-RM2-R:DLV-0) — used in (c⁺) only [R-1].
* [M5-0] T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" — cited for the D_n form only.

## Theorem RM-0

Any design (fixed or random). Let Q ⊇ S₀ be deterministic with |Q| ≤ K, 𝓛 = {T : S₀ ⊆ T ⊆ Q}. Assume the
implementation premises and configuration of STATEMENT §1 and the hypotheses of Lemma E4.

**(a)** On Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛), the deterministic LS0 (complete scans) from the coded start mode S̃₀ with cap
ℓ_n + |S̃₀| performs exactly |S̃₀ ∖ S₀| moves, each deleting one element of S̃₀ ∖ S₀, stays in 𝓛, and ends at S₀ with a
completed scan that finds no strict improvement; the cap is not binding. In particular
𝒦_nᶜ ⊆ Sand_n(Q)ᶜ ∪ NA(𝓛)ᶜ ∪ TL(𝓛)ᶜ.

*Proof.* By Lemma E4 the coded centre S̃₀ is a maximiser of γ₀ on Ω. Sand_n(Q) is a statement about every maximiser,
so on it S₀ ⊆ S̃₀ ⊆ Q, i.e. S̃₀ ∈ 𝓛 (and 𝓛 ⊆ Ω because |Q| ≤ K). Apply [L1.2] with C := S̃₀ and ℓ := ℓ_n + |S̃₀|:
ℓ ≥ |S̃₀| ≥ |S̃₀ ∖ S₀| = τ(C), so (ii) gives the endpoint S₀, reached after τ(C) moves, with a completed scan and no
`local_limit`; (i) gives the move types. If S̃₀ = S₀ the centre itself is S₀ and it is scored because the centre is
emitted (E4, integration clause). The complement inclusion is the contrapositive. ∎

**(a′)** [R-2] Let 𝓛′ ⊆ 𝓛 be deterministic and down-closed in 𝓛 (T ∈ 𝓛′, S₀ ⊆ T′ ⊆ T ⇒ T′ ∈ 𝓛′), and
St_n(𝓛′) := {S̃₀ ∈ 𝓛′}, NA(𝓛′), TL(𝓛′) as in STATEMENT §2. On St_n(𝓛′) ∩ NA(𝓛′) ∩ TL(𝓛′), the deterministic LS0
(complete scans) from the coded start mode S̃₀ with cap ℓ_n + |S̃₀| performs exactly |S̃₀ ∖ S₀| moves, each deleting one
element of S̃₀ ∖ S₀, visits only sets T with S₀ ⊆ T ⊆ S̃₀ (all in 𝓛′), and ends at S₀ with a completed scan that finds no
strict improvement; the cap is not binding; and the archive statement of the Corollary below holds. In particular
𝒦_nᶜ ⊆ St_n(𝓛′)ᶜ ∪ NA(𝓛′)ᶜ ∪ TL(𝓛′)ᶜ, and Sand_n(𝓛′) ⊆ St_n(𝓛′).

*Proof.* (1) *Lemma L1.1 on 𝓛′.* Re-read GROW `lemmas/L1_descent.md:20-41` with 𝓛′ in place of 𝓛: for C ∈ 𝓛′, its proof
of (a) uses NA at (C ∖ {e}, e) and at (C ∖ {e}, l) for e ∈ C ∖ S₀ (T := C ∖ {e} satisfies S₀ ⊆ T ⊆ C, so T ∈ 𝓛′ by
down-closure; |T| < K because |T| < |C| ≤ |Q| ≤ K), NA at (C, l) (only when |C| < K), and TL at C; its proof of (b), for
C = S₀, uses NA at (S₀, l) and TL at S₀. No other set is used. Hence: on NA(𝓛′) ∩ TL(𝓛′), for every C ∈ 𝓛′, L1.1(a)
and (b) hold with "lies in 𝓛" replaced by "lies in 𝓛′" (each scan maximiser C ∖ {e} is in 𝓛′ by down-closure).
(2) *Lemma L1.2 on 𝓛′.* Its proof (GROW `lemmas/L1_descent.md:51-57`) is an induction that applies L1.1 at the current
state S^t only, and the states are S^t = C ∖ {e₀, …, e_{t−1}} ⊇ S₀; so it holds verbatim for every centre C ∈ 𝓛′ on
NA(𝓛′) ∩ TL(𝓛′): the path deletes one extra per move, reaches S₀ after |C ∖ S₀| moves, every state lies in [S₀, C] ⊆ 𝓛′,
and the capped search with cap ℓ ≥ |C ∖ S₀| ends at S₀ with a completed scan finding no strict improvement, without
`local_limit`. The parts of L1.2 that concern the cap and the scan semantics (GEN L4.1(iii)) do not involve 𝓛.
(3) *The centre.* By Lemma E4 the coded centre S̃₀ is a maximiser of γ₀ on Ω, a function of the data; on St_n(𝓛′) it lies
in 𝓛′ ⊆ 𝓛 ⊆ Ω. Apply (2) with C := S̃₀ and ℓ := ℓ_n + |S̃₀| ≥ |S̃₀ ∖ S₀|. If S̃₀ = S₀ the centre is emitted and scored as
in (a). The archive statement follows from the code exactly as in the Corollary's proof (it uses only that the LS0
path from S̃₀ ends at S₀ with moves = |S̃₀ ∖ S₀| below the cap).
(4) Sand_n(𝓛′) ⊆ St_n(𝓛′) because S̃₀ is one of the maximisers quantified over in Sand_n(𝓛′) (E4). With 𝓛′ = 𝓛,
Sand_n(Q) = Sand_n(𝓛) ⊆ St_n(𝓛), so (a′) recovers (a). ∎

**(b)** (the parent's statement, kept; it is the special case of (b⁺) below through {π(S₀) > ½} ⊆ 𝓜_n [R-3]) Let n be such that s₀ ≤ K. For every admissible run (every seed, N_e, R′ and calibration outcome):
𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ, and the right side is a data event (it does not depend on the run parameters).
Consequently, with 𝒢_n := 𝒦_n ∩ {π(S₀) > ½}: on 𝒢_n every admissible run that returns output reports Ŝ⁺ = S₀, and

  P(𝒢_nᶜ) ≤ 2E[1 − π(S₀)] + P(Sand_n(Q)ᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ).

Hence P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝒢_nᶜ) uniformly over the run parameters; under [POST], [SAND(Q)], [NA(Q)], [TL(Q)],
P(𝒢_n) → 1, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = P(𝒪) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) = 1 − P(U_n) − o(1).

*Proof.* The inclusion is [DLV]'s Claim; we repeat its argument with E4 in place of premise e4. On a completed SMC
output run in the configuration of STATEMENT §1, GUARD-W excludes an interrupted LS0, OP-LS0 gives execution of LS0
with complete scans from the emitted coded centre (E4 identifies that centre as `start_mode(...).S`, a maximiser of
γ₀), and every model LS0 scores joins the all-scored set; LS0 reads no uniforms, so the set of models it scores is a
function of the data only — the same for every seed, N_e, R′ and calibration outcome. On the exact branch every feasible
model is scored, and S₀ is feasible because s₀ ≤ K. So on 𝒪 ∩ 𝒦_n the model S₀ is scored. If moreover π(S₀) > ½, then
F(S₀) > F(S) for every S ≠ S₀ in Ω (π(S) ∝ exp F(S) and π(S) ≤ 1 − π(S₀) < π(S₀)); under EX-A/EX-S/SR the reported
model is the F-maximum of the scored set, hence Ŝ⁺ = S₀. This proves the inclusion and that 𝒢_n is a common good data
event for all admissible runs. Markov: P(π(S₀) ≤ ½) = P(1 − π(S₀) ≥ ½) ≤ 2E[1 − π(S₀)]; with (a),
P(𝒦_nᶜ) ≤ P(Sandᶜ) + P(NAᶜ) + P(TLᶜ). The last sentence is algebra. ∎

**(b⁺)** [R-3] Let n be such that s₀ ≤ K and 𝓜_n := {S₀ is the unique maximiser of F on Ω}. For every admissible run
(every seed, N_e, R′ and calibration outcome):
  𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ ∪ 𝒦_nᶜ,
and the right side is a data event. With 𝒢⁺_n := 𝓜_n ∩ 𝒦_n, every admissible output run reports Ŝ⁺ = S₀ on 𝒢⁺_n;
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝒢⁺_nᶜ) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) uniformly over the run parameters; {π(S₀) > ½} ⊆ 𝓜_n, so
P(𝓜_nᶜ) ≤ 2E[1 − π(S₀)]; and for every 𝓛′ as in (a′), P(𝒦_nᶜ) ≤ P(St_n(𝓛′)ᶜ) + P(NA(𝓛′)ᶜ) + P(TL(𝓛′)ᶜ). Hence under
[MODE] (P(𝓜_n) → 1) and P(St_n(𝓛′) ∩ NA(𝓛′) ∩ TL(𝓛′)) → 1 for some such 𝓛′ (in particular under [SAND(Q)], [NA(Q)],
[TL(Q)], using Sand_n(Q) ⊆ St_n(𝓛)): P(𝒢⁺_n) → 1 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1). On enumeration branches
𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ.

*Proof.* Repeat the proof of (b) up to "So on 𝒪 ∩ 𝒦_n the model S₀ is scored" (on the exact branch every feasible model,
S₀ included, is scored, whether or not 𝒦_n holds). On 𝓜_n, F(S₀) > F(S) for every S ∈ Ω ∖ {S₀}; under EX-A/EX-S/SR the
reported model is the F-maximum of the scored set (the same step as in (b)), and S₀ is in the scored set and strictly
beats every other scored model, so Ŝ⁺ = S₀. This is the inclusion (and, on the exact branch, the inclusion without
𝒦_nᶜ). The proof of (b) used π(S₀) > ½ only to derive "F(S₀) > F(S) for every S ≠ S₀ in Ω", i.e. 𝓜_n; so (b) follows
from (b⁺) and {π(S₀) > ½} ⊆ 𝓜_n (π(S) ∝ exp F(S) on Ω: if π(S₀) > ½ then π(S) ≤ 1 − π(S₀) < π(S₀) for S ≠ S₀). The data-event
property is as in (b) (𝓜_n is a function of the data, 𝒦_n as there). Markov: P(𝓜_nᶜ) ≤ P(1 − π(S₀) ≥ ½) ≤ 2E[1 − π(S₀)].
The bound on P(𝒦_nᶜ) is (a′). The limits are algebra: P(𝒪 ∩ {Ŝ⁺ = S₀}) = P(𝒪) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}). ∎

**(c⁺)** [R-4] Assume in addition the delivery premises (D) of STATEMENT §2 (including IDEAL-W⁺). Then for every valid
non-degenerate input every admissible run returns output, and for every admissible run
  {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ ∪ 𝒦_nᶜ on the set of valid non-degenerate inputs.
For any law of the data under which the input is valid and non-degenerate with probability one,
P(Ŝ⁺ ≠ S₀) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) uniformly over seeds, N_e, R′ and calibration outcomes, and under the conditions of (b⁺)
P(Ŝ⁺ = S₀) → 1. In Setting F (model G, fixed X^r with non-constant columns) and in Setting R the input is valid and
non-degenerate with probability one (given a valid declared seed and allocation).

*Proof.* DLV-0 (`Q5_dlv0.md`) gives 𝒪 for every valid non-degenerate input, every seed and every realisation of the
uniforms; intersect the inclusion of (b⁺) with that set. If the input is valid and non-degenerate a.s., P(U_n) = 0 and
P(Ŝ⁺ ≠ S₀) = P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ). *Validity a.s.* The input is (X^r, y^r) with n ≥ 3 rows, y^r of
length n, and the declared seed and allocation. Setting F: X^r is a fixed finite matrix whose columns are non-constant
(X is its centred and standardised version, RM `STATEMENT.md:34-37`); y^r = α1 + X^rβ + ε with ε ~ N(0, σ²I_n) is finite a.s.,
and it is constant only if ε lies in the affine line {c1 − α1 − X^rβ : c ∈ ℝ}, a Lebesgue-null set for n ≥ 2. Setting R:
raw rows iid N(m_n, Σ_n) with unit diagonal (RM `STATEMENT.md:41-44`), so each raw column has iid N(m_{n,j}, 1) entries and is
non-constant a.s., and all entries are finite a.s.; the response is Y = Xθ* + Cε with ε ~ N(0, σ²I_n) independent of
the raw design (RM `STATEMENT.md:42-43`; the method uses the response only after centring, so "y^r not constant" is
"Y ≠ 0"), and conditionally on X^r, Cε has a non-degenerate Gaussian law on 1^⊥ (dimension n − 1 ≥ 2), so
P(Cε = −Xθ* | X^r) = 0; integrate over X^r. Validity of the
seed and allocation is declared. ∎
(DLV-0 is a statement about delivery only; it is not used for (a), (a′), (b), (b⁺).)

**Corollary (archive form; adopted from R02 P7).** On Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛), on every completed SMC output run
in the configuration of STATEMENT §1, LS0's own archive has `returned` = S₀, `local_certified` = true,
`local_limit` = false, `moves` = |S̃₀ ∖ S₀| and `moves` + 1 completed scans.
*Proof.* (a) and the code: each loop iteration of `local_search` pushes one completed scan
(ENGINE:407); a move is made on a strict improvement while `moves < ell` (ENGINE:408-412); at S₀ no strict
improvement exists, and the else-branch sets `termination = "no_improvement"`, `local_certified = true`,
`returned = C.S` (ENGINE:413-415); `local_limit` is set only in the cap branch (ENGINE:409-411), which is not reached
because the cap ℓ_n + |S̃₀| exceeds the number of moves (ENGINE = `Scripts/SMC_BVS/core/cpp/v3_engine.h`). ∎
(This is a statement about LS0's archive, hence about the hypothetical search on enumeration branches; the public flag
`local_certified` of the finally reported model is a different object and is not claimed.)

**Remarks.** (1) "For every seed, N_e, R′ and calibration outcome" is meant in the common-good-event sense: one data
event 𝒢_n, of probability → 1, on which no admissible output run reports a model other than S₀. No measurability
question over the calibration space arises, and CAL is not used. (2) No delivery claim in (a), (a′), (b), (b⁺): P(U_n) → 0 is not asserted there; (c⁺) adds delivery under (D) through DLV-0 [R-5].
(3) In the D_n notation of M5(0): D_n ≤ P(𝒦_nᶜ) by [OP], which gives the same bound through [M5-0]; that form lists CAL
among its premises, the pathwise form does not. (4) On enumeration branches 𝒦_n refers to the hypothetical
deterministic search; the conclusion there needs only π(S₀) > ½. (5) The certified-endpoint statement in (a) is about
LS0's own archive; the public flag `local_certified` refers to the finally reported model and is not claimed here.

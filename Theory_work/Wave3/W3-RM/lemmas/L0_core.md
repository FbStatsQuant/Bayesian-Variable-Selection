# L0 — Theorem RM-0 (core): from the three lattice events to the reported model (claim (C0))

Status: **PROVED (by this seat, unchecked)**, given the cited inputs with their recorded statuses; lemma check R03
(Codex gpt-6.1-sol high, `../reviews/R03_L0L1L2_check_sol.md`): RM-0(a), (b) VERIFIED. No new mathematics:
this file assembles GROW L1 (descent), DLV's pathwise claim and Lemma E4 (`L5_E4.md`), and makes the quantifiers over
run parameters explicit. Notation: `../STATEMENT.md` §1.

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
* [E4] `L5_E4.md` of this folder.
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

**(b)** Let n be such that s₀ ≤ K. For every admissible run (every seed, N_e, R′ and calibration outcome):
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
question over the calibration space arises, and CAL is not used. (2) No delivery claim: P(U_n) → 0 is not asserted.
(3) In the D_n notation of M5(0): D_n ≤ P(𝒦_nᶜ) by [OP], which gives the same bound through [M5-0]; that form lists CAL
among its premises, the pathwise form does not. (4) On enumeration branches 𝒦_n refers to the hypothetical
deterministic search; the conclusion there needs only π(S₀) > ½. (5) The certified-endpoint statement in (a) is about
LS0's own archive; the public flag `local_certified` refers to the finally reported model and is not claimed here.

# W3-SAMP · STATEMENT (v3 = locked v2 + sharpness-gate amendments, 2026-11-09)

**v2 → v3 (sharpness gate, `reviews/BT1_better_theorem_astra.md`, `reviews/BT1_disposition.md`; every change is a
strengthening, none weakens a v2 claim; flagged for HQ):** Theorem C's evidence bound is T-free (E|W_r − 1| ≤ 2δ̄), so
C-v needs only 1_𝒜δ̄ → 0 (P-START loses its T and any rate); C-iv gives O(δ̄) expected uniform PIP error and the bias bound;
new Theorem TR (terminal repair) replaces NC_r by the global-overlap premise L/M → ∞ (no particle statistic); LT-b′ and LT-e′ (vanishing
threshold) added; Theorem D uses the MAP premise S† = S₀ instead of δ < ½.

Lock record: statement-lock review SL1 by Codex gpt-6.1-sol (high), verdict LOCK WITH CHANGES
(`reviews/SL1_statement_lock_sol.md`); all five required changes applied (`reviews/SL1_disposition.md`). v1 → v2:
localisation to 𝒜 and to completed runs; admissible-h class restored in MR and the imported extension identified; Ẑ_r vs
`log_Z_r`; component theorems vs production-calibration corollaries; dependency statuses verbatim; Lemma PC (completed vs
potential records) added; CC text corrections.

Ticket: PROGRAM item 4 (`Theory_work/Wave3/PROGRAM.md`, "Sampler outputs as coded, honestly labelled conditional"):
(a) unbiasedness (W1-N1, done); (b) Lemma LT, corrected; (c) concentrated bridge; (d) draw discovery with a code check.
Sources (sketches, not checked proofs): `Theory_work/Wave2/SR/CRITIQUE_fable.md` §3 (LT), `ADJ_opus.md` §1(c)–(d) and
`ADJ_astra.md` §1(c)–(d) (the corrections), `BLIND_fable.md` Thm 4(b), `BLIND_astra2.md` Thm 3 (D).

## 0. Objects and conventions

**Data and target.** As in T12 §0 (`Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md:5-22`) and W1-N1 §0:
admissible (X, y); K = min(p, ⌊n/2⌋); Ω = {S ⊆ [p] : |S| ≤ K}; Z = Σ_Ω ϖm; π = ϖm/Z; block start γ₀, Z̄₀, π₀ = γ₀/Z̄₀;
d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b); γ_φ = γ₀e^{φd}; q_φ = γ_φ/Z̄_φ (q₀ = π₀, q₁ = π); Z_t := m(∅)Z̄_{φ_t}.

**Truth.** A fixed model S₀ ⊆ [p] with s₀ := |S₀| ≤ K. δ := 1 − π(S₀), δ₀ := 1 − π₀(S₀); odds o₁ := δ/(1 − δ),
o₀ := δ₀/(1 − δ₀); **δ̄ := max(o₀, o₁)**. Ω∖S₀ abbreviates Ω ∖ {S₀}.

**Two probability levels.** §2's finite-sample claims are conditional on the data and on 𝓒 (fixed data; probability over
the final streams), in W1-N1's **localised form**: island-r quantities are defined on E₀ := 𝒜 ∩ {r ≤ R′} ∈ σ(𝓒) (here
R′ = 4), and "given 𝓒 on 𝒜" means E[1_𝒜 Y | 𝓒] = 1_𝒜·(right side) for an arbitrary extension Y off 𝒜
(`Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md:13-16`). The asymptotic claims (marked "asymptotic") are under the
**joint data/algorithm law** along n → ∞ and are always intersected with 𝒜 (potential quantities) or with
{completed} ⊆ 𝒜 (reported outputs); a conditional finite-sample bound with a random right side ρ is integrated as
E[min(1, ρ)]. No claim is conditional on 𝒜 or on completion, and P(𝒜) → 1 is neither assumed nor claimed.

**The method as coded.** Production core on main = 4676af6, `Scripts/SMC_BVS/core/`; code facts in
`lemmas/CC_code_check.md` (CC1–CC7). Calibration record 𝓒, success event 𝒜 ∈ σ(𝓒); on 𝒜 a frozen grid
0 = φ₀ < … < φ_T = 1, N_e ≥ 1, L ≥ 0 (σ(𝓒)-measurable), Hm = 4, R′ = 4 islands, island r on stream 9 + r.
**Component vs production.** §2's Lemma ST and the finite-sample parts of Theorems D, LT♯, C and TR hold for **any**
frozen parameters (any valid grid, any N_e ≥ 1, L ≥ 0) of the engine component `Engine::run_island(r, N, grid, L, 4, …)`
(`cpp/v3_engine.h:269-273`). Through the public wrapper, an arbitrary valid grid reaches the engine unchanged
(`v3_frozen`, `v3_run.R:68-82`; `cpp/v3_core.cpp:446`), but N_e and L are always the production budgets
(`v3_run_settings`, `v3_run.R:88-92`), not `frozen$N`/`frozen$L` (LC1 issue 1). In every claim, N_e and L denote the
values actually executed. The ceiling T ≤ T_e and the deterministic draw-count lower bound hold only for **production
calibration** (budgets `v3_preprocess.R:21-30`); claims that use them are labelled "production corollary".
For island r on 𝒜 (potential, uninterrupted record):
- Ẑ_r := exp(`log_Z_r`[r]) (the code stores log Ẑ_r: `cpp/v3_engine.h:299, 322, 365`); W_r := Ẑ_r/Z; reported evidence
  `log_Z` = log Ẑ, Ẑ := ¼Σ_r Ẑ_r (`v3_run.R:150-154`).
- Bridge fractions A^{br}_{r,t} (fraction of island r's particles at S₀ after the stage-t round, t = 1..T; t = 0: the
  N_e initial draws). Terminal fractions A_{r,q}: after L + q rounds at φ = 1, q = 0..4.
- RB PIP p̂_r(j) := (4N_e)⁻¹ Σ_{q=1}^{4} Σ_i o_j(Y^i_{q,j}), Y^i_{q,j} = particle i's state immediately before its Gibbs-j
  step in measured round q; o_j(S) = γ₁(S∪j)/(γ₁(S∪j) + γ₁(S∖j)), and 0 if j ∉ S, |S| = K (CC3; T12 §2 item 3).
- pip_primary := ¼Σ_r p̂_r; MPM := {j : pip_primary(j) > ½}; on completed runs these are the reported fields
  (`v3_run.R:159-163`) and Ŝ is the reported HPM (CC2). 𝓜_r := models evaluated by island r; 𝓜 := all models offered to
  the final-run ledger.

## 1. Premises (ids for the registry) and dependency statuses

Inherited from W1-N1 (`Theory_work/Wave1/W1-N1/STATEMENT.md` §2), same meaning: **EX-A**, **H-U**, **START**,
**KERNEL**, **CAL**, **SI**, **MEAS**, **POT**. **IND-T** (streams 10–13 mutually independent and independent of
streams 0–9): only in D-ii. Statuses (verbatim): W1-N1 "PROVED-CHECKED" (council round 1, Codex 9.3 / Opus 8.9;
`Theory_work/Wave1/W1-N1/REPORT.md:11-12`), under START/KERNEL whose inherited status is "PROVED (candidate),
code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT" (`W1-N1/STATEMENT.md` §2). T12: `STATUS.md` "Result label now:
proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not
adopted."; the theory card reports "T12, T31(i): PROVED-LOCKED" (as quoted at `W1-N1/lemmas/L2_post_terminal.md:3-5`).

Interface properties consumed (Wave 3 protocol rule 5; each enters through one bridge result outside this ticket):
- **P-CONC**: δ_n → 0 in probability. Source example: W3-POST Theorem 1 clause 1 "(Rate) Under (BM): δ_n = 1 − π(S₀) =
  O_P(r_n)" (`Theory_work/Wave3/W3-POST/STATEMENT.md:79-80`, with its antecedents R1, G, (E), (F_λ), (F_w), (BM) in
  its §2; status per that ticket). Since o₁ = δ/(1 − δ), δ_n = O_P(r_n) with r_n → 0 gives o₁ = O_P(r_n).
- **P-START**: 1_𝒜·o₀ → 0 in probability, i.e. π₀(S₀) → 1 on 𝒜 — no rate (PROGRAM item 2's start-mass rate
  π₀(S₀) ≥ 1 − n^{−c} implies it; an input, not proved here).
- **P-MAP**: P(S† ≠ S₀) → 0, S† := the hpm_better-maximum of Ω (implied by P-CONC).
- **P-OVL∞**: P(𝒜 ∩ {L/M ≤ c}) → 0 for every finite c > 0 (equivalently Q → ∞ in probability with Q := L/M on 𝒜,
  Q := ∞ off 𝒜), M := max_{S∈Ω} π(S)/π₀(S) (global overlap relative to the executed terminal budget L; it involves no
  final-particle statistic; no calibration-success probability is implied — MP1 issue 1).
- **P-OVL**: 1_𝒜·D_r·π₀(S₀) → ∞ in probability, D_r := N_e(1 + T + L + 4) (computational overlap; on 𝒜ᶜ read as ∞).
- **NC_r** (computational): lim_{η↓0} limsup_n P(𝒜 ∩ {W_r < η}) = 0.

## 2. Claims

**Lemma CC (code facts).** CC1–CC7 of `lemmas/CC_code_check.md` hold for the code of record.

**Lemma PC (completed vs potential records).** Under EX-A: on {completed}, (i) each final island's statistical record
(Ẑ_r, all populations, the RB accumulator) equals the potential uninterrupted record computed from the same stream;
(ii) the reported HPM, pip_primary, MPM and log Z are the functions of these records given in §0; (iii) 𝓜 ⊇ ∪_r 𝓜_r and
Ŝ is the hpm_better-maximum of 𝓜 ⊆ Ω. (A limited comparison, not the full GUARD-W audit.)

**Theorem D (draw discovery).** Under EX-A, H-U, START, CAL, SI, MEAS, given 𝓒 on 𝒜, for the potential run:
- (D-i) island r's D_r π₀ draws are iid π₀; P(no π₀ draw of island r equals S₀ | 𝓒) = (1 − π₀(S₀))^{D_r} (equality),
  so P(S₀ ∉ 𝓜_r | 𝓒) ≤ (1 − π₀(S₀))^{D_r};
- (D-ii) under IND-T: P(S₀ ∉ ∪_r 𝓜_r | 𝓒) ≤ (1 − π₀(S₀))^{4D_r};
- (D-iii) with Lemma PC, unconditionally: P(completed ∩ {Ŝ ≠ S₀}) ≤ P(S† ≠ S₀) + E[1_𝒜 (1 − π₀(S₀))^{D_r}] (exponent
  4D_r under IND-T), and P(S† ≠ S₀) ≤ P(δ ≥ ½); production corollary: D_r ≥ max(2500, n, p)·(L + 6), L = max(4, ⌈log₂(n+1)⌉);
- (D-iv, asymptotic) under P-MAP (or P-CONC) and P-OVL: P(completed ∩ {Ŝ ≠ S₀}) → 0; production corollary: P-OVL may be replaced by
  max(n, p)·log₂(n+1)·π₀(S₀) → ∞ in probability. No condition on mixing, the bridge or Ẑ.

**Lemma MR (measured identities; imported + short extension).** Let h : Ω × E_𝓒 → ℝ be jointly measurable with a
deterministic bound sup_{S,c}|h(S; c)| ≤ B_h, evaluated at c = 𝓒, with no dependence on the final streams (W1-N1's class,
`W1-N1/STATEMENT.md` §1). Under the N1 premises, given 𝓒 on 𝒜:
- (MR-a) bridge: E[(Ẑ_{r,t}/Z_t)·(1/N_e)Σ_i h(X^{(t),i}) | 𝓒] = q_t(h) for each t ≤ T (t = 0: initial draws);
- (MR-b) terminal endpoints: E[W_r·(1/N_e)Σ_i h(X^{(s),i}) | 𝓒] = π(h) for every fixed s ∈ {0, …, L + 4};
- (MR-c) pre-step states: E[W_r·(1/N_e)Σ_i h(Y^i_{q,ℓ}) | 𝓒] = π(h) for each measured round q and each label ℓ (the
  prefix is a deterministic function of the particle's order); in particular E[W_r p̂_r(j) | 𝓒] = π(j ∈ S).
For fixed c these are T12 (i.a) (`STATEMENT.md:59`), (i.b) (`:60`), (i.c) (`:61`) and (ii) (`:64`); the conditioning on 𝓒
extends W1-N1's freezing lemma (L3) from endpoints to the augmented path record of its code bridge (L1); this extension is
proved in `lemmas/MR_identities.md` (W1-N1 alone covers only full-round endpoints).

**Lemma ST (staying at S₀).** Under KERNEL, at φ = 1:
- (ST-a) every kernel K on Ω with πK = π satisfies K(S₀, Ω∖S₀) ≤ o₁;
- (ST-b) K_{G_j}(S₀, Ω∖S₀) = |o_j(S₀) − 1{j ∈ S₀}| for every j, and Σ_j K_{G_j}(S₀, Ω∖S₀) ≤ o₁;
- (ST-c) a particle entering a round at φ = 1 at S₀ (any order law independent of the state) is away from S₀ at some time
  of the round with probability ≤ λ₀ := Σ_ℓ K_ℓ(S₀, Ω∖S₀) ≤ (B + 3)·o₁ ≤ 19·o₁ (B ≤ 16, CC7).

**Theorem LT♯ (corrected lower-tail transfer, coded outputs).** Under the N1 premises, given 𝓒 on 𝒜, for each island r and
all ε, η > 0, with κ₀ := max_j |o_j(S₀) − 1{j ∈ S₀}| ≤ o₁:
- (LT-a) for each q ∈ {0..4}: P(1 − A_{r,q} ≥ ε | 𝓒) ≤ δ/(εη) + P(W_r < η | 𝓒);
- (LT-b) P(max_j |p̂_r(j) − 1{j ∈ S₀}| ≥ κ₀ + 2ε | 𝓒) ≤ δ/(εη) + 19·o₁/ε + P(W_r < η | 𝓒);
- (LT-b′) with g := min{1, κ₀ + δ + (1 − δ)λ₀} ≤ 21·o₁: E[W_r‖p̂_r − 1_{S₀}‖_∞ | 𝓒] ≤ g, hence
  P(‖p̂_r − 1_{S₀}‖_∞ ≥ u | 𝓒) ≤ g/(uη) + P(W_r < η | 𝓒) for u > 0;
- (LT-c) P(S₀ ∉ 𝓜_r | 𝓒) ≤ δ/η + P(W_r < η | 𝓒);
- (LT-d) ‖pip_primary − 1_{S₀}‖_∞ ≤ max_r ‖p̂_r − 1_{S₀}‖_∞; if o₁ ≤ ¼: P(MPM ≠ S₀ | 𝓒) ≤ Σ_{r≤4}[8δ/η + 152·o₁ +
  P(W_r < η | 𝓒)]; with Lemma PC, on {completed} ∩ {δ < ½} ∩ {S₀ ∈ 𝓜}, Ŝ = S₀;
- (LT-e, asymptotic) under P-CONC and NC_r for every r ≤ 4, for every ε > 0: P(𝒜 ∩ {‖pip_primary − 1_{S₀}‖_∞ > ε}) → 0,
  P(𝒜 ∩ {MPM ≠ S₀}) → 0, P(𝒜 ∩ {1 − A_{r,q} > ε}) → 0, and P(completed ∩ {Ŝ ≠ S₀}) → 0 — for any frozen parameters;
  no rate for δ and no posterior size control. (The same holds for the reported fields on {completed}.)
  (LT-e′) The same conclusions hold if NC_r is replaced by: σ(data, 𝓒)-measurable η_n > 0 with 1_𝒜o₁/η_n → 0 in
  probability and P(𝒜 ∩ {W_r < η_n}) → 0 (collapse slower than the posterior error is allowed).
- (LT-f) honest label: NC_r is a premise about the particle system, not about (X, θ*). Whether it can be dropped or is
  necessary is **not settled** here: finite-n probes (`ASSUMPTION_MAP.md`) only illustrate a collapsed-evidence failure
  and a collapsed-evidence success; they are not asymptotic witnesses (LC1 issue 3). It is discharged by Theorem C,
  replaced by P-OVL∞ in Theorem TR; it is one-sidedly falsifiable (under EX-A,
  Ẑ_r < η·Σ_{S in the ledger's top store} e^{F(S)} implies W_r < η) and certified by no output. LT♯ says nothing about Ẑ/Z.

**Theorem C (concentrated bridge).** Under the N1 premises, given 𝓒 on 𝒜, for each island r and any frozen parameters
(any valid grid, any T ≥ 1, any N_e ≥ 1, any L ≥ 0):
- (C-i) deterministically W_r ≥ (π(S₀)/π₀(S₀))·Π_{t=0}^{T−1} A^{br}_{r,t};
- (C-ii) bridge occupation: with U_r := Σ_{t=0}^{T}(1 − A^{br}_{r,t}), E[min(U_r, 1) | 𝓒] ≤ 4(T + 1)δ̄;
- (C-iii) **T-free evidence bound**: E[|W_r − 1| | 𝓒] ≤ β ≤ 2·max{δ, (1 − δ)o₀} ≤ 2δ̄, where β := 2max(b₋, b₊)/c,
  a := d − d(S₀), b₋ := Σ_Sπ₀(S)(1 − e^{a(S)})⁺, b₊ := Σ_Sπ₀(S)(e^{a(S)} − 1)⁺, c := π₀(S₀)/π(S₀); hence
  E[|Ẑ/Z − 1| | 𝓒] ≤ β and P(|log Ẑ − log Z| > u | 𝓒) ≤ min{1, β/(1 − e^{−u})} for u > 0;
- (C-iv) with g as in LT-b′: E[‖p̂_r − 1_{S₀}‖_∞ | 𝓒] ≤ g + β/2 ≤ 22δ̄; E[‖pip_primary − 1_{S₀}‖_∞ | 𝓒] ≤ g + β/2;
  P(MPM ≠ S₀ | 𝓒) ≤ 2g + β ≤ 44δ̄; P(S₀ ∉ 𝓜_r | 𝓒) ≤ δ̄; and |E[p̂_r(j) | 𝓒] − π(j ∈ S)| ≤ β/2 for every j;
- (C-v, asymptotic) if 1_𝒜·δ̄ → 0 in probability (⇔ 1_𝒜o₁ → 0 and P-START; implied by P-CONC + P-START) then, for every ε > 0:
  P(𝒜 ∩ {|Ẑ/Z − 1| > ε}) → 0, P(𝒜 ∩ {|log Ẑ − log Z| > ε}) → 0, P(𝒜 ∩ {‖pip_primary − 1_{S₀}‖_∞ > ε}) → 0,
  P(𝒜 ∩ {MPM ≠ S₀}) → 0, P(completed ∩ {Ŝ ≠ S₀}) → 0, and NC_r holds; if moreover 1_𝒜δ̄ = O_P(r_n) (deterministic
  r_n ↓ 0) then, localised to 𝒜, Ẑ/Z − 1, log Ẑ − log Z and ‖pip_primary − 1_{S₀}‖_∞ are O_P(r_n). No rate for the start
  mass and no relation to the schedule length T are needed.
- Honest label: the regime in which the start already concentrates on S₀; the bridge has no mass to transport.

**Theorem TR (terminal repair; alternative to NC_r).** Under the N1 premises, given 𝓒 on 𝒜, any frozen parameters and any
bridge outcome, with M := max_S π(S)/π₀(S), e_0 := 1 and e_L := (1 − 1/M)^L for L ≥ 1:
- (TR-a) every round kernel at φ = 1 (any fixed order) satisfies K(x, ·) ≥ M⁻¹π(·); hence ‖K₁^L(x, ·) − π‖_TV ≤ e_L for all x;
- (TR-b) E[‖p̂_r − 1_{S₀}‖_∞ | 𝓒] ≤ g + e_L and E[1 − A_{r,q} | 𝓒] ≤ δ + e_L (q = 0..4);
- (TR-c) E[‖pip_primary − 1_{S₀}‖_∞ | 𝓒] ≤ g + e_L; P(MPM ≠ S₀ | 𝓒) ≤ 2(g + e_L); P(S₀ ∉ 𝓜_r | 𝓒) ≤ δ + e_L;
- (TR-d, asymptotic) under P-CONC and P-OVL∞: P(𝒜 ∩ {‖pip_primary − 1_{S₀}‖_∞ > ε}) → 0, P(𝒜 ∩ {MPM ≠ S₀}) → 0,
  P(completed ∩ {Ŝ ≠ S₀}) → 0 — with no condition on Ẑ, the bridge, N_e or the grid. Production corollary:
  L = max(4, ⌈log₂(n+1)⌉), so P-OVL∞ reads P(𝒜 ∩ {M > ε log n}) → 0 for every ε > 0 — a rate condition on the pair
  (π, π₀) alone.
- Honest label: P-OVL∞ is a global-overlap condition relative to the executed burn-in L (a condition on (π, π₀) alone once L
  is the production budget), involving no final-particle statistic and not certified by any output; it is not implied by
  π₀(S₀) → 1 (three-state example, `lemmas/TR_theorem.md`), and does not imply it. TR does not repair Ẑ.

## 3. Not claimed

- Anything conditional on 𝒜, on completion or on a favourable diagnostic (T12 (iv.e)); P(𝒜) → 1 or P(completed) → 1.
- The full GUARD-W delivery audit (only Lemma PC's comparison); floating point and the 2⁻⁵³ grid (EX-A, H-U).
- That NC_r, P-OVL or P-OVL∞ follows from primitive conditions on (X, θ*); any mixing statement beyond TR's minorization.
- P-START (PROGRAM item 2) and P-CONC (PROGRAM item 1) themselves.
- Relative consistency of Ẑ outside Theorem C; growing R′.
- The exact-enumeration branch (`v3_fit.R:120-127`), where HPM, PIPs and MPM are exact and W3-POST applies directly.

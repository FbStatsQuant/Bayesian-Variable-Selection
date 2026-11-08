# W1-N1 · STATEMENT (v2, LOCKED 2026-11-08)

Lock record: statement-lock review by Codex gpt-6.1-sol (high), verdict LOCK WITH CHANGES (`reviews/SL1_statement_lock_codex.md`);
required changes 1, 2, 4 applied here and in PLAN.md v2; change 3 (Lean) recorded as an objection (HQ ticket: Lean out of scope
unless trivial; no Lean toolchain on this machine) — see `reviews/SL1_disposition.md`. v1 → v2 changes: bounded h with a
deterministic bound; data fixed; parameter domains; r ≤ R′ event; single-island independence labelled as such; joint
measurability of the realisation map; citation for completion corrected.

Ticket: frontier card FR04, obligation OB01 (`Theory_work/State_of_Project/sections/06_open_and_plan.tex:109-117`).
Target: Lemma N1 = clause M1(b) (`TH01.b`) of Theorem V/H (`Theory_work/State_of_Project/sections/04_theory.tex:99-180`),
card text "(b) Lemma N1: E[Ẑ_r H_r(h) | 𝓒] = Z·π(h), H_r the plain measured-endpoint average"
(`NBH/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:111`). Current status (verbatim): "N1: PROOF SKETCH".
Corollary in scope: clause M1(e) (`TH01.e`).

NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`. CODE = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`
(the frozen production core; `02_method.tex` cites it as the code of record).

## 0. Data, state space, target

**The data are fixed** (a deterministic admissible input); every probability below is over the algorithm's randomness
only (streams 0–9 for 𝓒, the final streams for the islands). As in the locked T12 statement (`Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md` §0) and the TLF shared
definitions (`NBH/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:60-75`): a valid (admissible, standardised) input (X, y),
n ≥ 3, p ≥ 1, K = min(p, ⌊n/2⌋), Ω = {S ⊆ [p] : |S| ≤ K}; marginal likelihood m(S) > 0 (g = n score), capped BB(1, p)
prior ϖ(S) > 0, Z = Σ_{S∈Ω} ϖ(S)m(S), π(S) = ϖ(S)m(S)/Z on Ω. Blocks, tables r_b, γ₀, π₀ = γ₀/Z̄₀, d, γ_φ = γ₀e^{φd},
q_φ = γ_φ/Z̄_φ as in T12 §0 (so q₀ = π₀, q₁ = π, m(∅)Z̄₁ = Z).

## 1. The method as coded: one final island and its measured endpoints

Calibration record 𝓒 (grid, tier, N_e, L, R′ and every other setting the final run uses), with success event 𝒜 ∈ σ(𝓒).
Parameter domains: N_e ≥ 1 and L ≥ 0 integers; R′ = 4k with k ≥ 1 an integer (finite); all are σ(𝓒)-measurable and frozen
before stream 10 (R′ = 4 is the production value). The number of measured rounds is the literal constant 4 and the
production island count is the literal constant 4 (`measured_rounds = 4L, islands = 4L` at `CODE/v3_run.R:87-88`: `4L` is
the R integer literal 4, unrelated to the burn-in parameter L).
On 𝒜 the frozen grid satisfies 0 = φ₀ < φ₁ < … < φ_T = 1, T ≥ 1 (`CODE/cpp/v3_calib.h:71` starts at 0.0, `:73` loops while
u < 1, `:89` snaps to exactly 1).

Final island r ∈ {1, …, R′} is `Engine::run_island(r, N_e, grid, L, Hm = 4, tier, nullptr)` on stream 9 + r
(`CODE/cpp/v3_core.cpp:468-471`; `measured_rounds = 4L`, `islands = 4L` at `CODE/v3_run.R:87-88`; v3.1 allows R′ = 4k on
streams 10..9+R′, `NBH/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md:142`). Inside `run_island_s`
(`CODE/cpp/v3_engine.h:275-375`):
- N_e iid π₀ starts by `draw_start` (`:290`); log Ẑ initialised to log m(∅) + log Z̄₀ (`:300`);
- for t = 1..T (`:308-309`): log weights Δ_t·d(S_i) of the current population, increment
  inc_t = log((1/N)Σ_i e^{Δ_t d(S_i)}) computed at `:318-320` and added to log Ẑ at `:323`, multinomial resampling (`:325`, sampler `:235-260`),
  one random-order round at φ_t per particle (`population_round`, `:332`; round `:203-214`; order `:196-201`);
- L burn-in rounds at φ = 1 (`:344-346`), then Hm = 4 measured rounds at φ = 1 (`:353-357`).

**Measured endpoints.** S_{rqi} := the state of particle i of island r immediately after the q-th measured
`population_round(P, 1.0)` returns (`:357`), q = 1..4, i = 1..N_e. This is where the code records the plain counts
(`:360`, `for (const auto& q : P) for (int j : q.S) plain[j]++`).

**H_r(h).** H_r(h) := (4N_e)^{-1} Σ_{q=1}^{4} Σ_{i=1}^{N_e} h(S_{rqi}) — the v3.1 accumulator
"H_r(h)=(4N_e)^{-1}Σ_{q=1..4}Σ_i h(S_{rqi}), taken after each complete measured round (φ=1, equal weights after multinomial
resampling)" (`NBH/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md:159`; placement in code `cpp/v3_engine.h:351-359` per the same
line; those are v2.1-tree line numbers of the measured loop, `Scripts/SMC_BVS/core/cpp/v3_engine.h:351-360`; the v2.1 and v2.2.1
engines differ only by the plain-PIP lines). The frozen core implements it only for h = 1{j ∈ S}: then H_r(h) = `pip_plain[j]` exactly (`CODE/cpp/v3_engine.h:360, 371`);
for other h the accumulator is spec-only (divergence box "reporting fields not coded", `02_method.tex`), and H_r(h) is the same
average over the same coded endpoints S_{rqi}.

**Ẑ_r.** Ẑ_r := exp(log Ẑ) at the end of island r = m(∅)·Z̄₀·∏_{t=1}^{T} (1/N_e)Σ_i e^{Δ_t d(S^{(t−1)}_i)}
(`CODE/cpp/v3_engine.h:300` initialisation, `:318-320` increment, `:323` accumulation; T12 §2).

**Summaries h.** h : Ω × E_𝓒 → ℝ, (S, c) ↦ h(S; c) (E_𝓒 the measurable space of calibration values; the fixed data enter as
constants), jointly measurable, with a **deterministic uniform bound** sup_{S,c} |h(S; c)| ≤ B_h < ∞, evaluated at c = 𝓒; it
is fixed before stream 10 (no dependence on any final stream). Calibration information used to choose h must be part of 𝓒
(measurability in streams 0–9 alone is not enough, `METHOD_v3.1_FINAL.md:159`). The card's class (h ∈ 𝓗, 0 ≤ h ≤ 1,
M9 declaration) is the special case B_h = 1. π(h) := Σ_{S∈Ω} π(S)h(S; 𝓒).

## 2. Premises (named, as on the card)

- **EX-A** exact scores and arithmetic (TLF:72).
- **EX-S / H-U** fresh independent ideal U[0,1) uniforms within each stream; streams independent (TLF:86). The coded
  uniforms are on the 2⁻⁵³ grid (`CODE/cpp/v3_util.h:60`); H-U idealises this. *[Post-lock exposition note, MP1: the proof
  uses EX-S only for the within-stream law (iid U[0,1) on stream 9 + r); the only cross-stream property it uses is SI
  below. The card's full EX-S/IND-T is stronger than needed and is not discharged here.]*
- **START** `draw_pi0` returns exact π₀ draws and the reported Z̄₀ = Σ_Ω γ₀ (N9 Claims S, Z; status PROVED (candidate)).
- **KERNEL** the four coded step functions and the order realise the T12 §1 kernels and a uniform state-independent order
  (N9 rows 1–5, `NBH/branch_snapshots/N9-KERNEL/REPORT.md` §2; status PROVED (candidate), code-checked; CHK_INHERITED
  VERIFIED WITH AMENDMENT).
- **CAL** 𝓒 is a function of the (fixed) data and streams 0–9.
- **SI (single-island independence; a sufficient premise for N1, weaker than the card's IND-T).** Final stream 9 + r is
  independent of streams 0–9, for each r. For r ≤ 4 this is part of T12's CAL; for r > 4 it is implied by IND-T, whose
  extension audit is pending and is **not** discharged by this ticket. N1 uses no independence between islands.
- **MEAS** the realisation map (c, u) ↦ Φ(c, u) from (calibration value, stream) to the island record (including the four
  measured populations) is jointly measurable with values in a Polish space (as in T12 STATEMENT §2, EX-S); discharged for
  the coded island in the code bridge (Lemma B).
- **Potential run.** The identity is about the potential uninterrupted island record (no guard stop at `:336-339`);
  delivered records are identified with potential ones on 𝒪 by GUARD-W (TLF:86; audit open, not discharged here). No
  statement conditional on completion is made (clause (c), CEX-guard, `04_theory.tex:117,124`).
- **Worker equivalence (v3.1 only).** For v3.1's concurrent island workers, island r's record is the one `run_island`
  computes on stream 9 + r (K63 / Prop W, named premise). The frozen core is serial.

## 3. Statement N1 (target)

*[Post-lock exposition note, council C1: island-r quantities are defined only on E₀ := 𝒜 ∩ {r ≤ R′} ∈ σ(𝓒);
"a.s. on E₀" means the localised form E[1_{E₀}Y | 𝓒] = 1_{E₀}·(right side) a.s., Y the island-r integrand
(`lemmas/L3_freezing.md`). No change of claim.]*

Under §2, for every fixed index r ≥ 1, every q ∈ {1, …, 4} and every h as in §1, almost surely on 𝒜 ∩ {r ≤ R′}
(outside this event island r is not run and nothing is asserted):

  (N1-q) E[Ẑ_r · (1/N_e)Σ_i h(S_{rqi}) | 𝓒] = Z · π(h);
  (N1)   E[Ẑ_r · H_r(h) | 𝓒] = Z · π(h).

In particular, with W_r := Ẑ_r/Z, E[W_r | 𝓒] = 1 and E[W_r H_r(h) | 𝓒] = π(h). No regime assumption on X is made.

## 4. Corollary E (clause M1(e))

Let S₀ ⊆ [p] be any fixed model (the true model), δ₁ := 1 − π(S₀) (π(S₀) := 0 if |S₀| > K), and let h take values in
[0, 1], be as in §1 and be defined on Ω ∪ {S₀}. Under §2, a.s. on 𝒜 ∩ {r ≤ R′}:

  E[W_r · |H_r(h) − h(S₀)| | 𝓒] ≤ E[W_r · H_r(1{S ≠ S₀}) | 𝓒] = δ₁ ≤ 2δ₁.

(The card prints the bound 2δ₁, `THEOREM_LIST_FINAL.md:111`; the plain-average version δ₁ is the NEW-SYNTH form,
`NBH/ID_REGISTRY.md` TH412 (a).)

## 5. Not claimed

- Anything conditional on completion or on 𝒪 (clause (c), CEX-guard), or on a favourable final diagnostic (T12 (iv.e)).
- Unbounded or random-data h; the IND-T extension, GUARD-W and concurrency audits.
- Any h chosen after seeing final randomness (e.g. the measured-round frequency of the returned HPM, excluded by
  `METHOD_v3.1_FINAL.md:159`).
- Rao–Blackwellised records (clause (a), T12 (ii)); finite-R′ tail bounds (clause (f)); normalised estimators.
- Floating-point and 2⁻⁵³-grid effects (EX-A, H-U are idealisations).
- The full method at p ≤ 8 takes the exact-enumeration branch; the numerical companion tests the SMC component (same
  scope remark as T12 (iv.b)).

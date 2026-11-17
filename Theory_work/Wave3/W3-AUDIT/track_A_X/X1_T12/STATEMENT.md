# X1 · Lemma FR (T12 frozen-run identities, at the code of record) — STATEMENT v1 (draft, not locked)

Track A item X1 (`AUDIT.md` §6 "Further open inputs", X1; TRACK_D §3: "lemma (Tier B) — one line check of T12
(i.a)–(i.c), (ii), (R3) for the code of record; the label change follows"). Tier B (re-check of an existing proof; no
key lemma). **Lean target: yes** for the mathematics (finite-state Feynman–Kac identities: bridge identity, detailed
balance, prefix invariance, resampling and round means); no for the code identification. Blocks rows 3.5, 3.6.

## Sources
- T12 statement: island I(c), (R1)–(R3), hypotheses, claims (i.a)–(i.c), (ii)
  (`Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md:23-62`); proof
  (`Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:40-153`). Status: `W1-N1:P` "PROVED-LOCKED" (T12 (i.b));
  `SOP:TH110` "PROVED-LOCKED (all parts (i)-(iv), wave 1); not adopted" (registry); T12 `STATUS.md` "proved (Opus 5.5
  lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted"
  (`Docs/Theory/proofs/T12_T8_frozen_run_identities/STATUS.md:19-20`).
- Consumers: `W1-N1:Thm-N1` (row 3.5) through `W1-N1:P` and the code bridge `W1-N1:B`
  (`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:33-43`, "PROVED under the named premises … council-passed"); `W3-SAMP:MR`
  ((MR-a)–(MR-c), `Theory_work/Wave3/W3-SAMP/STATEMENT.md:107-116`) and the round path law (R3) used in (ST-c) and TR.

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core). The final island is
`Engine::run_island(r, N_e, grid, L, 4, tier, nullptr)` on stream 9 + r (`cpp/v3_core.cpp:443-446`).

## Lemma FR
Fix the data and a calibration value c in the success set (grid 0 = φ₀ < … < φ_T = 1, T ≥ 1, integers N_e ≥ 1, L ≥ 0).
Assume EX-A, H-U for the island's stream, START (T6) and KERNEL (T7). Consider the uninterrupted run of the final island
(T1: P°).
- **(FR-a) The code is I(c) with (R1)–(R3).** The island's statistical record is a realisation of T12's I(c) with
  N = N_e, M = 4, L′ = L and the stage-0 flag unset, and the coded execution satisfies (R1), (R2), (R3). (This is
  `W1-N1:B` (B-a), (B-b), whose code reading was done on the v2.2.1 core; it holds at the pin with the line numbers given
  in PROOF.)
- **(FR-b) (i.a)–(i.c).** For every t ∈ {0, …, T} and f : Ω → ℝ, E_c[Ẑ_t q̂_t(f)] = Z_t q_t(f), in particular E_c[Ẑ] = Z;
  after stage T, for the population after any of the L + 4 rounds at φ = 1, E_c[Ẑ q̂(f)] = Z π(f); and for any round and
  any prefix length κ_i = κ(σ_i) that is a fixed function of particle i's order alone, E_c[Ẑ_t (1/N)Σ_i f(X^i_{[κ_i]})] =
  Z_t q_t(f) (Z_T = Z, q_T = π for post-terminal rounds).
- **(FR-c) (ii).** For every j ∈ [p], E_c[Ẑ·PIP̂_j] = Z·PIP_j, where PIP̂_j is the code's `res.pip[j]`
  = `rb_acc[j]/(N·Hm)` with Hm = 4, i.e. T12's (MN)⁻¹ΣΣ o_j(Y^i_{u,j}, 1).

## Not claimed
- T12 (i.d), (iii), (iv) (not re-checked here; (iii) is used through W1-N1/W3-SAMP's own freezing lemmas).
- Binary64, the 2⁻⁵³ grid (EX-A, H-U).
- Interrupted runs (T1 GW: on 𝒪 the record equals the uninterrupted one).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (re-states T12 (i.a)–(i.c), (ii), (R1)–(R3) for the pin) | track A X1 | `AUDIT.md` §6 X1; manager GO 11-16 | `CHECK.md` |

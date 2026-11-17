# W1 · Lemma ISL (island control flow, stopping times, MEAS at the pin) — STATEMENT v1 (draft, not locked)

Track A_W item W1 (manager 11-17; D97 edge verdicts, recorder package §2 edges 2 and 3). Tier B (line check of the cited
steps of `W1-N1:B` at the code of record). **Lean target: yes** for (ISL-st) in abstract form ("a program that reads an
i.i.d. U[0, 1) sequence one value at a time, with bounded reads per operation: every operation starts at a bounded
stopping time and, given the past, reads fresh i.i.d. uniforms"; finite program, strong Markov property of i.i.d.
sequences); no for the code correspondence.

## Steps under check (the conditions to discharge)
- `W1-N1:B` (registry: `Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:33-43`, proof `:45-125`), written for the v2.2.1
  core, as used by
  - **`W3-SAMP:D`** (D-i, "used only through the control-flow clause of W1-N1 Lemma B (B-b)"; its freezing step uses
    (B-0), (B-d)): `Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md:6-31`;
  - **`W3-SAMP:MR`** Step 2 (measurability of the augmented record, (B-d)): `Theory_work/Wave3/W3-SAMP/lemmas/MR_identities.md:57-65`.
  (B-a), (B-b)'s law statements (R1)–(R3) at the pin are `W3-AUDIT-AX:FR` (FR-a) (`Theory_work/Wave3/W3-AUDIT/track_A_X/X1_T12/STATEMENT.md:27-42`)
  and are not re-checked here.
- The three steps: **(B-0)** the record is a function of (c, u) (`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:65-78`);
  the **control-flow clause of (B-b)** — stopping times, bounded reads, fresh uniforms (`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:78-86`);
  **(B-d)** MEAS (`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:115-122`).

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core); paths relative to it. Final island r:
`E.run_island(r, o.N, g, o.L, o.Hm, o.tier, nullptr)` on a fresh `RngSource` seeded `seed_stream(seed, 9 + r)`
(`cpp/v3_core.cpp:443-446`).

## Setting
Fixed valid data on the SMC branch, `setup` built (T2 BLK, T4 ENC). A calibration value c in the success set A_s: grid
0 = φ₀ < … < φ_T = 1 (T ≥ 1), integers N_e ≥ 1, L ≥ 0, Hm = 4, the tier (the final-run settings are functions of c and
(n, p): T5 CAL-c). u = (u₁, u₂, …) ∈ Υ := [0, 1)^ℕ the island's stream; 𝓕_k := σ(u₁, …, u_k). The **potential run**
(T1: every guard Boolean FALSE). EX-A. The **statistical record** Φ(c, u) is `W1-N1:B`'s (`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:14-21`):
log Ẑ_r, the population after the initial draws, after each stage-t resampling and each stage-t round, after each of the
L + 4 rounds at φ = 1, and for each particle and round its order and within-round path; the **augmented record** Φ̃(c, u)
adds every π₀ draw in execution order (initial draws and independence proposals, accepted or not; `W3-SAMP:D`'s
augmentation). Off A_s, Φ := Φ̃ := a fixed dummy record o†.

## Lemma ISL
For every c ∈ A_s, on the potential run of final island r:
- **(ISL-0) Function of (c, u).** Every value that feeds a state transition, an accept decision, a weight, a resampling
  or log Ẑ is a function of c, the fixed data and uniforms read from u; no other source (clock, guard, cache history,
  ledger, other islands' streams, persistent engine members) influences Φ̃(c, u). Uniforms are read only through the
  island's `vs->u(·)`, sequentially.
- **(ISL-st) Stopping times and fresh uniforms.** The island's operations — each initial draw, each resampling, each
  particle-round, each elementary step, and each `draw_pi0` call — run in an order and read a number of uniforms that
  are decided by c, the data and the uniforms already read. Hence the index τ at which an operation starts is an
  (𝓕_k)-stopping time, bounded by a constant κ(c) (below); (u_{τ+1}, u_{τ+2}, …) is i.i.d. U[0, 1) and independent of
  𝓕_τ (under H-U); and every record variable produced before the operation is 𝓕_τ-measurable. Bounds: `draw_pi0`
  ≤ 1 + 2J uniforms; a resampling N_e; a particle-round ≤ κ_max := (m − 1) + p + 3 + 3B + (2 + 2J), m = p + B + 2; so
  κ(c) := N_e(1 + 2J) + T·N_e + (T + L + 4)·N_e·κ_max. The number of π₀ draws is D_r(c) = N_e(1 + T + L + 4).
- **(ISL-d) MEAS.** (c, u) ↦ Φ̃(c, u) (hence Φ) is 𝓔 ⊗ 𝓤-measurable, where 𝓔 is any σ-field on the calibration space
  for which c ↦ (T, grid, N_e, L, tier) is measurable and A_s ∈ 𝓔, and 𝓤 is the Borel σ-field of Υ; its values lie in a
  Polish space (a countable disjoint union of Euclidean spaces times finite sets). Every coordinate used by
  `W3-SAMP:MR` Step 2 (stage-t populations, post-terminal populations, Y^i_{q,ℓ} = particle i's state before its ℓ-step
  in measured round q) and by `W3-SAMP:D` (the D_r(c) draws) is a measurable function of Φ̃.

## Use
(ISL-0) + (ISL-st) are the "control-flow clause of (B-b)" and (B-0) as `W3-SAMP:D` (D-i) uses them; (ISL-d) is (B-d) as
`W3-SAMP:D`'s freezing step and `W3-SAMP:MR` Step 2 use it — all at the pin, for the record conventions those proofs use.

## Not claimed
- The laws (R1)–(R3) and the identification with T12's I(c) (that is FR-a).
- Binary64 / the 2⁻⁵³ grid (EX-A, H-U); interrupted runs (T1 GW).
- Calibration-time islands (pilot, diagnostics), which run on streams 0–9 (T5 CAL-a).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (line check of `W1-N1:B` (B-0), (B-b) control flow, (B-d) at the pin) | track A_W W1 | manager 11-17; D97 edges 2, 3 | `CHECK.md` |

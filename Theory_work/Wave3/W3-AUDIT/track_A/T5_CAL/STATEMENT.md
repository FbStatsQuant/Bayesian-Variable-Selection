# T5 · Lemma CAL-C (the calibration record depends on the data and streams 0–9 only) — STATEMENT v2 (draft, not locked)

Track A item T5 (`AUDIT.md` §6; CHECKPOINT_1 annex order 5). Tier B (code reading; no key lemma). **Lean target: no**
(code fact). Blocks rows 3.5, 3.6.

## Source of the premise
- "**CAL** a successful frozen calibration record 𝒞 on streams 0–9"
  (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86`).
- "**CAL** 𝓒 is a function of the (fixed) data and streams 0–9" (`Theory_work/Wave1/W1-N1/STATEMENT.md:79`); 𝓒 holds
  "grid, tier, N_e, L, R′ and every other setting the final run uses", "σ(𝓒)-measurable and frozen before stream 10"
  (`Theory_work/Wave1/W1-N1/STATEMENT.md:29-31`).
- Used by `W3-SAMP` (C, LT♯, D, TR; `Theory_work/Wave3/W3-SAMP/STATEMENT.md:64-65`), whose 𝒜 is "{SMC branch and
  `v3_calibrate` returns status "ok"}", "𝒜 ∈ σ(𝓒)" (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:39-41`), and by row 3.5
  (`W1-N1:Thm-N1`).

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core); paths relative to it. Shipped `v3_fit`, default options.

## Objects
- **Streams.** For k ≥ 0, U^{(k)} := the sequence of uniforms produced by `Xoshiro256ss::seed_stream(seed, k)`
  (`cpp/v3_util.h:43-61`). Under H-U (`Theory_work/Wave1/W1-N1/STATEMENT.md:71-72`) these are idealised as independent
  i.i.d. U[0, 1) sequences.
- **Potential fit** P°, operational fields, statistical state: as in T1 (GW) (`T1_GW/STATEMENT.md`). 𝓒° := the
  statistical fields of P°'s `v3_calibrate` output (status, tiers, tier_final, frozen object incl. grid, tier, N, L,
  inherited models and HPM), 𝓒° := ⊥ if P° does not call `v3_calibrate`; 𝒜° := {𝓒° ≠ ⊥, status "ok"}.
- The **final run's inputs**: `v3_final_run(setup, frozen, seed, runtime, ls0)` (`v3_fit.R:162`).

## Lemma CAL-C
Assume EX-A. For every valid input (X, y, seed, allocation) of the shipped `v3_fit`:
- **(CAL-a) Streams 0–9 only.** Until `v3_calibrate` returns, the only streams created or read are U^{(k)}, k ∈ {0, …, 9}
  (pilot: k = 0 at tier 0, k = 5 at tier 1; diagnostic islands: k = 1, …, 4 at tier 0, k = 6, …, 9 at tier 1); no
  stream k ≥ 10 exists before `cpp_final_run` starts.
- **(CAL-b) Function of the data and streams 0–9.** 𝓒° = Ψ(X, y, seed, U^{(0)}, …, U^{(9)}) for a map Ψ (the options fixed), in which the seed
  enters only as the label `calibration_seed` (its other role is to fix the streams);
  Ψ is measurable (each argument enters through a computation of bounded length — see PROOF Step 3); and
  𝒜° ∈ σ(𝓒°).
- **(CAL-c) Frozen before stream 10.** Every setting the final run uses — grid, tier, N_e, L, measured rounds Hm = 4,
  islands R′ = 4, ℓ_n, the cache capacity, the inherited models and HPM, and the LS0 options — is a function of 𝓒° and
  (n, p, options); the final run's randomness is U^{(10)}, …, U^{(13)} (island r on stream 9 + r), created inside
  `cpp_final_run`; and its remaining inputs are `setup` (a function of (X, y)), the seed, and the guard `runtime`, which is operational
  (T1: its Boolean is FALSE in P°).
- **(CAL-d) The actual fit.** With G as in T1 (GW-iv): 𝒜 = 𝒜° ∩ G ⊆ 𝒜°, and on G — hence on 𝒜 — the statistical fields of
  the actual `v3_calibrate` output equal 𝓒° (T1's induction run to the return of `v3_calibrate`, T1 PROOF Step 4 (⊇)). Hence CAL holds for 𝓒°, and for the actual record on 𝒜.

## Where the T1 flag bites (carried, per the manager 11-16)
`W3-SAMP` conditions on 𝓒 "on 𝒜" and writes interface premises with 1_𝒜. By (CAL-b) the conditioning is valid for the
potential pair (𝒜°, 𝓒°), not for the actual 𝒜 (which depends on the clock through G). Reading: W3-SAMP's conditional
claims hold with (𝒜°, 𝓒°); **upper bounds** on P(𝒜° ∩ A°), P(𝒪° ∩ A°), for events A defined by statistical state, transfer to P(𝒜 ∩ A),
P(𝒪 ∩ A) since 𝒜 ⊆ 𝒜° and 𝒪 ⊆ 𝒪° (T1 GW-iv) — lower bounds and statements conditional on 𝒜 do not, and W3-SAMP makes
none ("No claim is conditional on 𝒜 or on completion, and P(𝒜) → 1 is neither assumed nor claimed",
`Theory_work/Wave3/W3-SAMP/STATEMENT.md:35`); and its
interface premises must hold with 1_𝒜° in place of 1_𝒜:
- **P-START** ("1_𝒜·o₀ → 0", proved only under (A5)): `W3-START2-R:IF-START` gives 1_𝒜o₀ = O_P(r_n) "for every event 𝒜"
  (`Theory_work/Wave3/W3-START2-R/STATEMENT.md:241-244`), in particular for 𝒜°. **No loss.**
- **P-OVL** (Theorem D's clause): its 𝒜° form is T8 (OVL).
- **P-OVL∞** (Theorem TR, kept as a named open premise): to be read with 𝒜°; nothing to check here.

## Not claimed
- H-U / SI / IND-T (independence of the streams; method premises, kind M) and EX-A.
- Anything about the probability of 𝒜° or 𝒜.
- Inputs off the shipped path (`v3_calibrate` called directly with another `tier` or `grid_fallback`).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM | track A T5 | `AUDIT.md` §6 T5 | `CHECK.md` |
| v2 | (CAL-b) seed label; (CAL-c) inputs; (CAL-d) citation; flag paragraph: upper bounds only | EQUAL in substance (wording made exact) | LC2 #9–#12 | `reviews/LC2_reply_opus.md` | pending (gate) |

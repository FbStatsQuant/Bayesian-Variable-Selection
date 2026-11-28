# T8 · Lemma OVL (P-START and the production budget give P-OVL) — STATEMENT v4 (draft, not locked)

Track A item T8 (`AUDIT.md` §6; CHECKPOINT_1 annex order 8). Tier B (a one-line consequence of checked results; no key
lemma). **Lean target: yes** (an elementary limit argument). Blocks row 3.6, Theorem D clause only.

## Source of the premise
- **P-OVL**: "Q_D → ∞ in probability, where Q_D := D_r·π₀(S₀) on 𝒜 and Q_D := ∞ off 𝒜, D_r := N_e(1 + T + L + 4)
  (… equivalently P(𝒜 ∩ {D_rπ₀(S₀) ≤ c}) → 0 for every c)" (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:82-83`); consumed
  by Theorem D (D-iv) (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:104-105`).
- Route named but not written as a lemma: "P-OVL | … | P-START; Proposition OVL | SAMP Theorem D"
  (`Theory_work/Wave3/W3-START/STATEMENT.md:185`).
- **P-START**: "1_𝒜·o₀ → 0 in probability, i.e. π₀(S₀) → 1 on 𝒜" (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:76-77`),
  o₀ = δ₀/(1 − δ₀), δ₀ = 1 − π₀(S₀). Supplied by `W3-START2-R:IF-START` ("PROVED-CHECKED; council R2, …"; registry row in `STATUS_EXTRACT.md`), stated there "for every event 𝒜" under
  "(T1⁺⁺) with (AL) at Q = S₀" (or (T3⁺⁺)(b) with Q = S₀) (`Theory_work/Wave3/W3-START2-R/STATEMENT.md:241-244`).
- **(A5)** in this file means the leakage hypothesis inside IF-START's hypotheses: (AL) at Q = S₀ in fixed design, (L-R⁺⁺) with
  Q = S₀ in Gaussian rows (the reader's (A5), bridge B5.1′); in fixed design (AL) bounds an average over the nulls, not
  every null. It is the reader version's "no leakage" condition of Theorem 10 (`AUDIT.md` §4 row
  "(A5) no leakage"; correction 2 of §6: P-START is proved only under it).
- Production budget: `W3-SAMP:D` (D-iii) production corollary, D_r ≥ max(2500, n, p)·(L + 6),
  L = max(4, ⌈log₂(n + 1)⌉) (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:103`; proof
  `Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md:53-54`), "PROVED-CHECKED".

## The success event (T1/T5 flag, stated where it bites)
By T1 (GW-iv) and T5 (CAL-d), W3-SAMP's conditional arguments hold for the potential success event 𝒜° (𝒜 ⊆ 𝒜°). The
lemma is therefore stated with 𝒜°; the actual-𝒜 form follows because 𝒜 ⊆ 𝒜° makes every probability below smaller.

## Lemma OVL
Production calibration (shipped `v3_fit`), EX-A. Let 𝒜° be the potential calibration-success event (T5) and, on 𝒜°,
D_r := N_e(1 + T + L + 4) with the frozen N_e, T, L (those of 𝓒°, i.e. of the uninterrupted run; an actual final run
stopped by the guard may execute fewer stages).
- **(OVL-a) Budget.** On 𝒜°, D_r ≥ max(2500, n, p)·(L + 6) ≥ 10n, deterministically.
- **(OVL-b) P-START ⇒ P-OVL.** If 1_𝒜°·o₀ → 0 in probability (P-START on 𝒜°), then for every c > 0,
  P(𝒜° ∩ {D_r·π₀(S₀) ≤ c}) ≤ P(𝒜° ∩ {π₀(S₀) ≤ ½}) as soon as 10n ≥ 2c, and the right side → 0. Hence P-OVL holds
  with 𝒜° (and with any 𝒜 ⊆ 𝒜°).
- **(OVL-c) Status.** P-START on 𝒜° holds under the hypotheses of `W3-START2-R:IF-START`, which include (A5); so
  P-OVL is proved by this route **only under IF-START's hypotheses, in particular (A5)**. Without (A5), P-OVL's production form also follows from `W3-START2-R:OVL` ("PROVED-CHECKED")
  under its own hypotheses — OVL⁺ of `Theory_work/Wave3/W3-START2/STATEMENT.md:181-189` (setting F, (E), (GF-16),
  visibility, a deterministic Q ⊇ S₀ with |Q| ≤ K and |Q ∖ S₀| ≤ q̄, (AL) for Q, bounded levels a_{n,l}) with the
  substitutions of `Theory_work/Wave3/W3-START2-R/STATEMENT.md:212-213` — whenever
  limsup_n(E_n − max(1, log p/log n)) < 0 (note log max(n, p)/log n = max(1, log p/log n)); quoted, not re-proved.

- **(OVL-d) Both premises hold for the uninterrupted run (HQ check, 11-16).** With 𝒜° the potential (uninterrupted)
  success event of T1/T5: (i) **P-START holds with 1_𝒜°** under IF-START's hypotheses (in particular (A5)): o₀ is a
  function of (X, y) alone, and IF-START's proof is 0 ≤ 1_𝒜o₀ ≤ o₀ = O_P(r_n) for an arbitrary event 𝒜
  (`Theory_work/Wave3/W3-START/lemmas/L10_INTERFACES.md:14-15`); 𝒜° is an event by T5 (CAL-b). (ii) **P-OVL holds with
  𝒜°** by (OVL-b), D_r being the uninterrupted run's frozen budget (a function of 𝓒°, T5 CAL-c); without (A5), the
  OVL route's conclusion P(π₀(S₀) ≥ n^{−E_n−ε}) → 1 is event-free and (OVL-a) holds on 𝒜°, so its production form holds
  with 𝒜° as well. No premise fails for the uninterrupted version. (P-OVL∞, Theorem TR, stays a named open premise.)

## Consequence for Theorem D (D-iv)
Pathwise, completed ∩ {Ŝ ≠ S₀} ⊆ {S† ≠ S₀} ∪ (𝒜° ∩ {S₀ ∉ 𝓜°_r}) for any fixed r ≤ 4, where 𝓜°_r is the set of
models the uninterrupted island r evaluates. Hence, by D-i for the uninterrupted island given (data, 𝓒°) (valid on 𝒜°
by T5 CAL-b), P(completed ∩ {Ŝ ≠ S₀}) ≤ P(S† ≠ S₀) + E[1_𝒜°·(1 − π₀(S₀))^{D_r}], with no premise on the clock; and
(1 − π₀(S₀))^{D_r} ≤ e^{−D_rπ₀(S₀)}; under (OVL-b) and P-MAP the right side → 0. (This replaces W3-SAMP's (D-iii)
step, which integrates over the actual 𝒜.)

## Not claimed
- P-START itself, or anything about designs outside (A5) beyond the cited OVL route.
- P-OVL∞ (Theorem TR; kept as a named open premise, manager 11-16).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM | track A T8 | `AUDIT.md` §6 T8 | `CHECK.md` |
| v2 | (A5) defined; (OVL-c) hypotheses stated in full | EQUAL (exact wording; no claim changed) | LC3 T8 #1–#3 | `reviews/LC3_reply_opus.md` | pending (gate) |
| v2.1 | (A5) gloss | EQUAL (editorial) | LC4 E2 | `reviews/LC4_reply_opus.md` | — |
| v3 | (OVL-d) uninterrupted-run check | STRONGER (makes explicit what (OVL-b), (OVL-c) and T5 give) | HQ 11-16 ruling (c) | manager message 11-16 | council R1 |
| v4 | Consequence for (D-iv): proof via the pathwise inclusion with 𝒜° and D-i for the uninterrupted island (no actual-𝒜 step); "executed" → "frozen" budget | EQUAL (same final bound; the invalid intermediate step removed) | R1 Sol #2 (C); R1 Opus E2, E3 | `reviews/R1_council_sol.md`, `reviews/R1_council_opus.md` | diff round R1d |

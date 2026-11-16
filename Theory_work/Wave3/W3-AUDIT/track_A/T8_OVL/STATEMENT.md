# T8 · Lemma OVL (P-START and the production budget give P-OVL) — STATEMENT v1 (draft, not locked)

Track A item T8 (`AUDIT.md` §6; CHECKPOINT_1 annex order 8). Tier B (a one-line consequence of checked results; no key
lemma). **Lean target: yes** (an elementary limit argument). Blocks row 3.6, Theorem D clause only.

## Source of the premise
- **P-OVL**: "Q_D → ∞ in probability, where Q_D := D_r·π₀(S₀) on 𝒜 and Q_D := ∞ off 𝒜, D_r := N_e(1 + T + L + 4)
  (… equivalently P(𝒜 ∩ {D_rπ₀(S₀) ≤ c}) → 0 for every c)" (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:82-83`); consumed
  by Theorem D (D-iv) (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:104-105`).
- Route named but not written as a lemma: "P-OVL | … | P-START; Proposition OVL | SAMP Theorem D"
  (`Theory_work/Wave3/W3-START/STATEMENT.md:185`).
- **P-START**: "1_𝒜·o₀ → 0 in probability, i.e. π₀(S₀) → 1 on 𝒜" (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:76-77`),
  o₀ = δ₀/(1 − δ₀), δ₀ = 1 − π₀(S₀). Supplied by `W3-START2-R:IF-START` ("PROVED-CHECKED; council R2, …") **only under
  the no-leakage condition (A5)** (AUDIT.md §6 correction 2), and stated there "for every event 𝒜"
  (`Theory_work/Wave3/W3-START2-R/STATEMENT.md:241-244`).
- Production budget: `W3-SAMP:D` (D-iii) production corollary, D_r ≥ max(2500, n, p)·(L + 6),
  L = max(4, ⌈log₂(n + 1)⌉) (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:103`; proof
  `Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md:53-54`), "PROVED-CHECKED".

## The success event (T1/T5 flag, stated where it bites)
By T1 (GW-iv) and T5 (CAL-d), W3-SAMP's conditional arguments hold for the potential success event 𝒜° (𝒜 ⊆ 𝒜°). The
lemma is therefore stated with 𝒜°; the actual-𝒜 form follows because 𝒜 ⊆ 𝒜° makes every probability below smaller.

## Lemma OVL
Production calibration (shipped `v3_fit`), EX-A. Let 𝒜° be the potential calibration-success event (T5) and, on 𝒜°,
D_r := N_e(1 + T + L + 4) with the executed N_e, T, L.
- **(OVL-a) Budget.** On 𝒜°, D_r ≥ max(2500, n, p)·(L + 6) ≥ 10n, deterministically.
- **(OVL-b) P-START ⇒ P-OVL.** If 1_𝒜°·o₀ → 0 in probability (P-START on 𝒜°), then for every c > 0,
  P(𝒜° ∩ {D_r·π₀(S₀) ≤ c}) ≤ P(𝒜° ∩ {π₀(S₀) ≤ ½}) as soon as 10n ≥ 2c, and the right side → 0. Hence P-OVL holds
  with 𝒜° (and with any 𝒜 ⊆ 𝒜°).
- **(OVL-c) Status.** P-START on 𝒜° holds under the hypotheses of `W3-START2-R:IF-START`, i.e. **only under (A5)**; so
  P-OVL is proved under (A5). Without (A5), P-OVL's production form also follows from `W3-START2-R:OVL` ("PROVED-CHECKED")
  whenever limsup_n(E_n − max(1, log p/log n)) < 0 (`Theory_work/Wave3/W3-START2/STATEMENT.md:181-187`, word for word
  in `Theory_work/Wave3/W3-START2-R/STATEMENT.md:212-213`), with no change here.

## Consequence for Theorem D (D-iv)
P(completed ∩ {Ŝ ≠ S₀}) ≤ P(S† ≠ S₀) + E[1_𝒜°·(1 − π₀(S₀))^{D_r}] (D-iii, with 𝒜 ⊆ 𝒜°), and
(1 − π₀(S₀))^{D_r} ≤ e^{−D_rπ₀(S₀)}; under (OVL-b) and P-MAP the right side → 0.

## Not claimed
- P-START itself, or anything about designs outside (A5) beyond the cited OVL route.
- P-OVL∞ (Theorem TR; kept as a named open premise, manager 11-16).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM | track A T8 | `AUDIT.md` §6 T8 | `CHECK.md` |

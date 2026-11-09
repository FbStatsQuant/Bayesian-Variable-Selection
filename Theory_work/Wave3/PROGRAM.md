# Theory Wave 3 — the adopted program (binding)

Adopted by Theory HQ on 2026-11-09 with Felipe Bedoya's approval ("Deploy"), from the strategy review
`Theory_work/Wave2/SR/` (blind proposals BLIND_fable, BLIND_astra(2); informed critique CRITIQUE_fable.md §4–§5;
adjudications ADJ_astra.md and ADJ_opus.md — both chose package B with corrections).

## Presentation rule
Theorems are stated under conditions on (X, θ*) only — **no design family appears in a theorem statement**. Families
(AR, banded, spatial, blocks, one-factor, masked hubs, ...) appear only in an examples table. All results asymptotic;
p ≤ n^A for any fixed A, p ≫ n the regime that matters most; about the method as coded (main).

## The package (CRITIQUE_fable.md §4, with the adjudicators' fixes)
1. **Posterior concentration** (T03♯/UNI-P, SL0/SL1) — proved; needs an independent adversarial re-check (it never had
   a council pass) and a sharpness check. 1a: size-tail lemma stated on its own. 1b: predictive/Hellinger corollary
   (Song–Liang Thm 1–2 analog). 1c: enumeration branch (APP ENUM).
2. **Start and misspecification** (C-MIS, sandwich) + **new start-mass rate** (with no leakage, π₀(S₀) ≥ 1 − n^{−c}).
3. **Reported model under two primitive conditions** (V) visibility (no truth masked by ≤ 15 conditioning variables)
   and (L) bounded leakage (a deterministic Q ⊇ S₀ of size ≤ C log n / (log n)^κ outside which no column gains more
   than ησ² log n): restated **in GROW's form**, with UNI-0 (council-passed, Theory_work/Wave2/W2-UNI) as the main
   example; the general (V)+(L) form at polylog size is new work (ADJ_opus); partition-free where possible; close
   premise e4.
4. **Sampler outputs as coded**, honestly labelled conditional: (a) unbiasedness (N1); (b) Lemma LT, **corrected**
   (ADJ_opus: as written it does not deliver `pip_primary` — Rao–Blackwell PIPs recorded mid-round — nor the MPM, and its
   premise is near-circular); (c) concentrated bridge (BLIND_fable Thm 4(b)) under no leakage; (d) draw discovery
   (Astra): P(miss) ≤ E[(1 − π₀(S₀))^{D_n}], with a code check that rejected proposals reach the ledger.
5. **Certified screening** (BLIND_fable Thm 5(a)): P(𝒪 ∩ {certified} ∩ {|Ŝ⁺| ≤ q_n} ∩ {S₀ ⊄ Ŝ⁺}) → 0 under a floor
   on sets of size q_n + s₀; no start/leakage condition; must match the coded meaning of `local_certified`.
6. **Limits:** GEN (C6) (holds for the **old** LS0 cap only — ADJ_opus correction), NEG (LS0 only, not the full method),
   SHARP, OBS-k as remarks.
Examples table: UNI-0 families; one-factor p < n/2 (FAC-A, UNI-1, FAC-B, FAC-X); masked hubs (PXN).

## Decision D1 (strong factors at p ≫ n) — pending experiment P6
Run the full method (not just LS0) on factor designs at p > K and p ≫ n. If it recovers S₀, a proof ticket follows
(possibly with an LS0-cap or other method change); if not, the paper claims screening + limits there.

## Stop list
No further exponent-raising for p ≤ K; no exact-Gram factor tickets; FAC-S5/S5F/XA/K2/PKA/FAC-GL stay stopped;
no shipped-calibration delivery or M1(i) stacking work; no new design-family tickets.

## Tie-break (owner may veto)
Incomparable theorems: design-agnosticism > range of p > rate > constants.

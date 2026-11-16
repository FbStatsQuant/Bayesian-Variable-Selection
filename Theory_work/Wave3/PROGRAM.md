# Theory Wave 3 — the adopted program (binding)

Adopted by Theory HQ on 2026-11-09 with Felipe Bedoya's approval ("Deploy"), from the strategy review
`Theory_work/Wave2/SR/` (blind proposals BLIND_fable, BLIND_astra(2); informed critique CRITIQUE_fable.md §4–§5;
adjudications ADJ_astra.md and ADJ_opus.md — both chose package B with corrections).

## Presentation rule
Theorems are stated under conditions on (X, θ*) only — **no design family appears in a theorem statement**. Families
(AR, banded, spatial, blocks, one-factor, masked hubs, ...) appear only in an examples table. All results asymptotic;
p ≤ n^A for any fixed A, p ≫ n the regime that matters most; about the method as coded (main).

**Readability (owner, 2026-11-15; binding for every headline theorem, the chapter and the paper).** "They must be true
but, as much as possible, they should not be weird-looking statements. They have to be presented in a way that makes
clear to the reader what the assumptions are and what the proven statements are." Song–Liang (2015) Theorems 1–2 are an
*example* of statements a reader understands from the statement alone. They are not a template to copy (owner). The owner again: "I don't want a bunch of alien-looking theorems. The proof might be as tough as needed, I don't care."
Proof difficulty and length are free; **statement clarity is not negotiable**.
**The standard (owner, 2026-11-15; "do we have an agreement").** What the method does and what each statement says
must be clear and intelligible to peers. Proof complexity is fair game, provided the proof can be checked (in Lean
where we certify). Song–Liang (2015) and the owner's own papers were cited only as *examples* of meeting this standard.
**Nothing is to be taken from them**: no template, no structure, no wording.

Every headline theorem therefore has a **reader version**:
- the assumptions are a short numbered list (A1)–(Ak), each in standard, primitive terms a reader recognises: i.i.d.
  rows with sub-Gaussian tails, strict sparsity, p ≤ n^A, a sparse eigenvalue bound, a beta-min level. Technical
  sample-level interfaces (events such as (E), (ND), (F_w), visibility or leakage objects) do not appear there. They
  live in a "master theorem" or in lemmas, with bridges from (A1)–(Ak) to them;
- the conclusion is one display, or at most three, in whatever form is clearest for this result, with the rate written
  explicitly;
- each assumption gets one line on why it is there and whether it is necessary (from TARGET.md);
- constants and secondary clauses go to remarks; no new notation in the statement beyond what the setup defines.
- **notation (owner, 2026-11-15): intelligible to peers.** Every document a reader sees (paper, chapter, claims
  card, advisor report) opens with a complete setup and notation section: model, prior as coded, the posterior, the
  output of the method, and every symbol, index set, norm, asymptotic notation (O_P, ≍, ≪) and constant used later.
  Every symbol is defined before its first use. A notation table goes at the end. No internal ids (ticket names, claim
  ids, interface tags such as (ND), (F_w), LS0, R′) in the main text; where a code object matters, it is described in
  words. A peer in Bayesian high-dimensional statistics must be able to read each theorem without our files.

The master (interface) version stays as the checked result. The reader version is a corollary with its bridges checked,
and **both** pass review. The reader version is the one in the paper's main text, the chapter, the claims card and the
advisor report. At CP1 the lead proposes the reader version; council gate F (faithfulness) covers reader version =
master + bridges; HQ and the consultant check readability on the headline cards (PROTOCOL_v4 H5).

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

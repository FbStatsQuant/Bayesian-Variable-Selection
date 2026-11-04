# W5-B2ENV: A no-method-change masked theorem. (1) Finish D2's NB′ on LH, c = 1. (2) Instantiate the envelope route (b2) on LH via W4-SHARE's D5 and Prop. M

**Paper role:** Thm 5(b1′) and (b2). Without LS0 the masked regime is conditional. Two routes avoid the method
change: the pilot's first stage (D2) for one masked variable, and the Gibbs path after envelope-controlled
delivery (W4-SHARE D4/D5). Part (1) has a guaranteed deliverable; part (2) is the research part.

Fetch and read: `origin/theory/W4-SHARE` (PROOF.md §§0–7: D4, D5, Prop G, SH, X, M, Theorem B2-W4; NOTES;
scripts), `origin/theory/W1-T38E` (PROOF §§3–5: Lemma A, Lemma S, Theorem D2, C1; §7), `origin/theory/W3-VT38E`
(REPORT §3.1 NB′ and r*, §3.2 reversible C1, §5.3), `origin/theory/W3-PXN` (PROOF §12: P7, the NB sketch;
REPORT §6), `origin/theory/W4-T38FULL` (`T38_PROOF.md` §4.2: the second NB sketch; §5), `origin/theory/W1-T24G`
and `origin/theory/W2-PREM` (Theorem B♯, Theorem L on LH, IND-T), `origin/theory/W1-EXP` (PROOF §4: LH).
Also METHODOLOGY_v3 §§6.5–6.8 and `v3_engine.h` (`pilot_next_phi`, `run_island_s`, `resample`).

Goals, in order:
1. **Referee W4-SHARE** (it has no verifier): D4's supermartingale (the predictable stopping time τ, the convexity
   step, the monotonicity of P ↦ P(1 − e^{−θ/P})), D5's fitness-ratio bound (2.1) and Prop G (grid independence),
   Prop SH, Prop X, Prop M(a) (deterministic), Theorem B2-W4 (islands, REPAIR on W). Record verdicts; repair gaps.
2. **Finish NB′ for D2 on LH exact Gram, c = 1** (and on LH-iid if time permits). Both existing sketches reduce to:
   the H₀ = max(n, p, 2500)-ish initial pilot draws have d-range ≤ 2T_e·(something) with probability → 1, or S₀ is
   drawn. Prove P(NB′ᶜ) → 0 by bounding (a) the probability that any pilot draw contains a proxy of the masked hub
   or an outsider with d higher by Θ(n) (peeling bound on π₀(S ⊉ S°)), (b) the uniform d-range on the good set
   (O(log n) against the threshold ≈ 2T_e). State the rate. This upgrades Thm 5(b1′) on LH (c = 1) from PROOF SKETCH
   to PROVED, giving the paper its first masked instance **without LS0**.
3. **Envelope route on LH, c = 1 first.** Build the potentials: h_t = indicator (or a smoothed version) of the
   lattice state that is γ_{φ_t}-optimal on Lat(S°) (Prop M(b): the within-lattice path is downhill for
   φ ≥ φ_n → 0), with W = {S₀} ∪ (lattice states at distance one) at the end. Bound: (TRACK) exits η_t by Lemma A
   endpoint odds and the gain expansions (W1-EXP Lemma U); the oscillation κ_t against outsiders (states outside
   the lattice with higher d: proxies of hubs, S° + null, S₀ + null) using F- and π₀-gaps; confinement 𝔛_t by
   Prop X-type gates. Target: Γ + Σ_t η_t ≤ log(Nπ₀(h₀)/T_e) − ω(1) with N = N_e and T ≤ T_e = 1000 under the v3
   budgets. If it fails, say exactly which outsider class or which exit term is too large, and whether a larger N_e
   schedule (a budget sequence, allowed by Felipe's premise) repairs it. Then REP on W from Theorem B♯ / Cor P1
   (distance one) with IND-T.
4. **Prove Prop M(b)** (score gain along the lattice; currently PROOF SKETCH) as a lemma, since (3) needs it.
5. **Numerics** (exact scores, p ≤ 30, LH config A of W1-EXP, production packing from `v3_blocks.h`, the method's
   pilot/final-run rules): simulate the potential uninterrupted final run and measure Γ, the η_t, the envelope
   breach frequency, and delivery, against the bound; and the pilot-stage scoring frequency for D2.

Deliverable: `theory_campaign/W5-B2ENV/REPORT.md` with statements, proofs (PROOF.md), numerics, what fails and why,
escalation, confidence card. A clean negative on (3) ("the envelope needs N ≫ T e^Γ with Γ ≍ … on LH, so (b2) needs
a budget sequence N_n = …") is a valuable result.

---

_Source: theory_campaign/F-REFINE/NEXT_TASKS.md on branch theory/F-REFINE (Fable, 2026-11-02). Read F-REFINE's CARDS.md and ARCHITECTURE.md first: `git fetch origin theory/F-REFINE`._

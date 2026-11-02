# F-SHARE — REPORT: the delivery theorem for route (b2) in the masked regime

Run of 2026-11-02 (Fable 5.1, Felipe's laptop; two Opus 5.5 helpers for the exact checks and the simulation), branch `theory/F-SHARE`. Proofs in `PROOF.md`; scripts and their saved outputs in `scripts/` and `results/`. Every result is a **candidate**: not reviewed, not adopted. Status words follow `theory_campaign/PROTOCOL.md` and are never upgraded.

## 1. Headline

1. **The right delivery theorem is a closure theorem, not an envelope theorem (Theorem F1, PROVED).** If the near-truth class is the *superset class* W(S°) = {x : S° ⊆ x} of the start reference S°, and if deleting a member of S° is unfavourable at **both** endpoints (start table and posterior), uniformly over supersets — hypothesis KEEP(W, η) with η = e^{−Θ(n)} — then with probability ≥ 1 − N[π₀(Ω∖W) + (T + L + 4)η] **no particle of the final run ever leaves W**. Delivery to W is then automatic, with the whole population eligible at the terminal boundary; the realised D4 envelope is deterministic (P_t = ∏(1 − η_s)); and the C1 extinction mechanism cannot start (Corollary F3, PROVED). KEEP is a single-state, single-round, two-endpoint condition: block-table ratios and score differences, no SHARE, no LT, no particle-system quantity.
2. **On the linked-hub family (LH, exact Gram, p ≤ (1 − c₀)n) the superset class is closed, so route (b2)'s delivery step is closed there for the method as it is (Theorem F2: structure PROVED, Gaussian estimates PROOF SKETCH).** The unit structure of LH (Lemma 3.1) makes every residual statistic a function of the state's intersection with one unit, so the supremum over the 2^{p−s} supersets is a maximum over ≤ s·2^{2g} Gaussians, and the keep margins are Θ(n) uniformly. The single population condition PK (proxy keep) is checked exactly at p = 16, 20 (§4). Masked hubs are added *inside* W after the crossing temperature φ_hub = O(log(p√n)/n) → 0 (Prop. M of W4-SHARE in this family).
3. **What remains is repair on W, not delivery (§4 of PROOF, PROOF SKETCH).** Extras are fast variables (re-drawn at their own Gibbs label every round, odds ≤ (2p√n)^{−ε_n}); hubs are slow (uphill before φ_hub, downhill after). S₀ is scored at the first stage with φ_t ≥ 2φ_hub by any extra-free particle, and in the terminal rounds otherwise. The one non-routine input is the extras bookkeeping across resampling (CONJECTURE 4.3). The numerics (§4) show S₀ scored in every island during the bridge, never in the terminal rounds, with no particle ever outside W.
4. **Counterexamples and the no-go side.** C1 (W1-T38E) needs an outsider class that is drawn at the start (Nπ₀(o) ≳ 1) and fitter by ≥ log N; both are excluded by KEEP's two endpoints, and Proposition SH shows the second is the sharp threshold. The posterior-barrier design PB (W4-SHARE) has a closed class too; there delivery holds and repair fails, so Theorem F1 locates (b2)'s failure outside T03's regime exactly where W4 found it. **No method change is needed on LH**; LS0 and T39 are compared in §7: on LH all three deliver, and only the closed-class route needs no tweak.
5. **The genuinely open case is the random design (LH-iid, p ≫ n).** Lemma 3.1 holds only approximately, the class must be cut at bounded extras, and the leak through the (d+1)-st extra is O_P(n^{−1/2}polylog) per round, so N(T+L+4)η ↛ 0 and F1 does not apply; the reversible-leak version F1′ (D4 with a discounted leak potential) is the tool (CONJECTURE F2-iid, §2). The sharp question is uniform null leakage over the bounded-extras supersets a particle can visit.

## 2. Statements

Setting: one final-run island given a successful 𝓒; EX-A, EX-S, CAL, SR; T ≤ T_e stages, then L + 5 rounds at φ = 1; S° a data-measurable reference; W(S°) := {x ∈ Ω : S° ⊆ x}; K_φ the one-round kernel.

- **KEEP(W, η).** W 𝓒-measurable and sup_{x∈W} K_φ(x, Ω∖W) ≤ η for every φ ∈ {φ₁, …, φ_T, 1}.
- **Theorem F1 (PROVED).** Under EX-A, EX-S, CAL and KEEP(W, η): P(some particle is ever outside W | 𝓒) ≤ Nπ₀(Ω∖W) + N(T + L + 4)η per island. On the complement every particle is in W at every stage, at 𝔉_T and through the terminal rounds (DELIV(W) with the whole population eligible).
- **Lemma 1.2 (PROVED).** For W = W(S°), K_φ(x, Ω∖W) ≤ Σ_{j∈S°}max{κ₀, κ₁}(x, j) + (B+1)Σ_{j∈S°}max{ρ₀, ρ₁}(x, j) + π₀(Ω∖W), with κ_e the endpoint deletion odds and ρ_e the endpoint swap-out odds (maximised over the added label).
- **Corollary F3 (PROVED).** Under KEEP with Nπ₀(Ω∖W) + N(T+L+4)η → 0, the W-count is N at every stage w.p. → 1, the D4 envelope for h = 1_W equals ∏(1 − η_s) deterministically, and no outsider lineage exists: the C1 mechanism cannot start.
- **Lemma 3.1 (PROVED, LH exact Gram).** The unit residual u_{x,j} depends on x only through x ∩ unit(j) and is orthogonal to every column of another unit. **Lemma 3.2 (PROVED).** For x ∈ W(S°), b ∈ M∖x: δ_{x,b} = θ_b‖(I − P_x)x_b‖, δ²_{x,b} ≥ θ_b²(n−1)λ_min(Σ_LH).
- **PK(d*)** (population proxy-keep, §3.1 of PROOF): finitely many inequalities in (ρ, ψ, g); checked exactly for (0.7, 0.5, 4) at every proxy configuration (§4); CONJECTURE in general for |ψ| < ρ < 1.
- **Lemma 3.3 (PROVED given W1-EXP Thm 1 and PK).** Start keep odds κ₀(x, j) ≤ 2p e^{−c₁n} uniformly over x ∈ W(S°), j ∈ S°; swap-out odds ρ₀ ≤ 2p e^{−c_Kc₁n}.
- **Lemma 3.4 (PROOF SKETCH).** Posterior keep margins F(x) − F(x − j) ≥ c₂n and swap margins F(x) − F(x − j + l) ≥ c₂n uniformly over x ∈ W(S°), |x| ≤ K, j ∈ S°, l ∉ x, except for l a masked hub of another pair (handled by the enlarged class W⁺, Remark 3.6).
- **Theorem F2 (PROOF SKETCH; structure PROVED).** LH exact Gram, p ≤ (1 − c₀)n, PK(g−1): with W = W⁺(S°), (a) π₀(Ω∖W), π(Ω∖W) ≤ Cpe^{−cn}; (b) KEEP(W, η) with η ≤ Cp²e^{−cn}; (c) P(some particle of some island is ever outside W) ≤ C′NT_ep²e^{−cn} → 0; (d) DELIV(W) with every particle eligible.
- **§4 (PROOF SKETCH).** Crossing temperature φ_hub = O(log(p√n)/n); extras deleted w.p. ≥ 1 − (2p√n)^{−ε_n/3} per label and added at expected rate (2p√n)^{−2/3+o(1)} per round (finite Z-families + truncated moment); S₀ scored at the first stage with φ_t ≥ 2φ_hub or in the terminal rounds; CONJECTURE 4.3 (extras count across resampling) is the only non-routine step.
- **Theorem F1′ (CONJECTURE, routine from D4).** Reversible leaks: a class whose exits land in a less-fit set 𝓛 from which the kernel returns w.p. ≥ 1 − η′, with Tη + Tη′ → 0, is delivered (h = 1_W + ρ1_𝓛 in D4).
- **CONJECTURE F2-iid.** On LH-iid (W3-PXN) with blocks = groups, W_d(S°) := W(S°) ∩ {≤ d extras} satisfies the hypotheses of F1′ with 𝓛 = states with d + 1 extras, η = O_P(n^{−1/2}polylog), hence DELIV(W_d) → 1, for every fixed d ≥ 1; the crux is the uniformity of the null leakage over the ≤ p^d·2^c states of W_d (W3-PXN Lemma B gives the per-state Beta laws).

## 3. Proofs

`PROOF.md`: §1 F1 and Lemma 1.2; §2 F3; §3 the LH family (Lemmas 3.1–3.4, PK, Theorem F2, Remark 3.6 on W⁺); §4 extras, crossing, scoring (sketch); §5 failure modes (PB, leaky classes, the random-design obstruction).

The crux of F1 is trivial (resampling copies states); the content is in the choice of W: a class closed under the kernel at the e^{−cn} level, which the *superset* class is whenever truths are kept at both endpoints, because additions never leave it. The crux of F2 is Lemma 3.1 (finite Gaussian families), which is exact-Gram-specific.

## 4. Evidence

(All scripts in `scripts/`, outputs in `results/`; engine `bvs_core.py` copied verbatim from W4-SHARE: exact scores, v3 blocks and tables, exact π₀, full random-order round with heat-bath Gibbs (SR), uniform and neighbour swaps with Hastings factors, independence proposal, multinomial resampling, the method's idealised grid. Design `lh_design.py`: LH16 (p = 16, c = 1) and LH20 (p = 20, c = 2), ρ = 0.7, ψ = 0.5, β = 1, σ = 1, g = B = 4, blocks = groups.)

NUMERICS_PLACEHOLDER

## 5. What fails and why

- **D4/D5 as the primary tool.** On a closed class the envelope is deterministic and D5's oscillation κ is irrelevant; on a non-closed class with *fitter* leaks D5 is sharp (SH) and the leaks are C1. The envelope is the right tool only for *reversible* leaks (F1′), i.e. exits to less-fit states that return. The three cases (closed / reversible leak / fitter leak) are the classification; W4-SHARE's (TRACK)+(OSC) is the middle one with the oscillation measured against the leak set only.
- **W = 𝓡_d (bounded extras) as the class.** It leaks through the (d+1)-st extra at rate n^{−1/2}polylog per round; N T_e n^{−1/2} → ∞. That is why W1/W4's sup-exit bounds on 𝓡_d were useless. The superset class fixes it in the exact Gram; in random designs the cut is forced (Remark 3.5) and F1′ is needed.
- **Uniform keep margins over all supersets in general designs.** They need the truth's partial signal to survive conditioning on any set of extras; with p close to n the ridge residual Q_x can be small (Q_x ≥ RSS_{[p]} ≈ σ²(n − p)), which is why Theorem F2 assumes p ≤ (1 − c₀)n. For p ≥ n only bounded-extras classes make sense.
- **PK in general.** For (ρ, ψ, g) with ρ close to 1 and many proxies present, the swap a_i → proxy can become posterior-favourable at states that miss b_i (PROOF §3.1 computation); such states have start mass (2p√n)^{−(g−1)} and are never visited, but a sup-over-W statement must exclude them by hand (cut W at d* proxies and treat the rest as a reversible leak).
- **Extras across resampling (CONJECTURE 4.3).** The re-weighting multiplies an extra-carrying particle by up to (2p√n)^{Δ_t(1−ε_n)} per extra; the Gibbs round re-equilibrates each null at its label, but the B + 1 swap labels and the independence proposal can re-insert extras after their label. The finite-constant bookkeeping is not written.

## 6. Needs escalation

1. **Lemma 3.4 with explicit remainders** (ridge Schur-complement step, the finite union of Lemma 3.1, the W⁺ bookkeeping of Remark 3.6): routine, should be written by a stronger prover and checked cross-family.
2. **CONJECTURE 4.3 and §4.4** (extras across resampling; one-round scoring constant c₀ via Lemma R of O-BGIBBS): this is REP(W⁺) on LH. Either W1-T24G's Theorem B is instantiated on W⁺ with bounded extras (the certificates are the proxies), or §4.4 is completed.
3. **PK(g − 1) as a theorem** for |ψ| < ρ < 1 (a finite population computation; the one-proxy cases are done).
4. **CONJECTURE F2-iid** (random design): the uniform null-leakage bound over W_d. This is the only thing standing between the present result and a p ≫ n delivery theorem; W3-PXN's exact Beta laws are the input.
5. **Independent check of the reading of C1** (Corollary F3): that KEEP's two-endpoint form is exactly what C1 violates (π₀(o) > 0 with Nπ₀(o) ≳ 1), and that no BVS design can realise C1 inside a closed superset class (Lemma PD argument, PROOF §5.3).

## 7. Outside scope

- **Minimal method change, compared with LS0 and T39.** On LH none is needed for delivery: F2 delivers every particle. LS0 (deterministic search from S̃₀ = S°) delivers eligibility for free but needs TD′; T39 (scoring tracks) delivers through start mass b_n and fails on posterior barriers like (b2). The closed-class route is the only one that uses the bridge, and it is the one consistent with the n = 200 data (98 % of fresh scores from Gibbs, local search repaired 0 fits).
- **Paper text.** T38(b2) should read: DELIV(W⁺(S°)) by Theorem F2 (every particle eligible) + REP(W⁺). The hypothesis list is: LH exact Gram (or any family with two-endpoint keep margins, i.e. VIS-lin(S°) on the start side and a uniform posterior keep margin), PK, p ≤ (1 − c₀)n. The ESS grid plays no role (consistent with W4's Proposition G).
- **The n = 200 study.** W3-PXN showed the study's masking is dilution, not LH-type cancellation; nothing here speaks to n = 200 (the constants in §4.2 need n > 4^g).
- **O-BGIBBS overlap.** BG1 proves pilot first-stage discovery when φ₁ ≥ φ_hub; F2 + §4 is the multi-stage complement: when φ₁ < φ_hub the particles wait in W⁺ (closed) until the grid passes φ_hub, then score S₀. Together they cover the final run on LH with no floor on the grid.

## 8. Confidence card

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| Theorem F1 (closed-class delivery) | PROOF §1 | 0.99 | done (candidate) | — | no |
| Corollary F3 (no C1 under KEEP) | PROOF §2 | 0.98 | done | — | no |
| Lemmas 3.1–3.2 (unit structure) | PROOF §3.1 | 0.99 | done | — | — |
| PK(g−1) for (0.7, 0.5, 4) | exact check | 0.98 | done numerically; general CONJECTURE 0.8 | ρ → 1 with many proxies | — |
| Lemma 3.3 (start keep, via EXP′) | PROOF §3.2 | 0.95 | 0.9 | VIS-lin at all block configs | no |
| Lemma 3.4 (posterior keep, uniform over supersets) | PROOF §3.2 | 0.9 | 0.8 | ridge remainders; W⁺ bookkeeping | no |
| Theorem F2 (LH exact Gram, DELIV(W⁺) with all particles) | PROOF §3.3 | 0.9 | 0.75 | Lemma 3.4 | **no** |
| §4 scoring on W⁺ (REP) | PROOF §4 | 0.85 | 0.5 | extras across resampling (Conj. 4.3) | no |
| T38(b2) on LH exact Gram, no tweak, every fixed c | F2 + §4 + T38(0) | 0.85 | 0.5 | as above | **no** |
| F1′ (reversible leaks) | PROOF §5.2 | 0.9 | 0.85 | D4 with a two-level potential | no |
| F2-iid (p ≫ n) | §2 | 0.75 | 0.4 | uniform null leakage over W_d | no |
| Route (b2) outside T03's regime | fails through REPAIR (W4 PB) | 0.95 | — | ceiling for local methods | none helps |

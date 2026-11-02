# W5-B2ENV — REPORT: no-method-change masked theorems on LH

Branch `theory/W5-B2ENV` (from `theory/campaign` @ 9db8748). Files: `PROOF.md` (statements and proofs), `REFEREE.md`
(verdicts on W4-SHARE), `NOTES.md`, `scripts/` (fixed seed 20261102; outputs `*.txt`). Every result is a candidate:
same-family work, not reviewed, not adopted.

## 1. Headline

1. **NB′ is PROVED on LH (exact Gram), c = 1** (Theorem NB′-LH): P(NB′ᶜ) = O(√n/p + n^{−1/2}), so the tier-0 pilot's
   first stage scores S₀ whenever p/√n → ∞ (Corollary D2-LH, **PROVED** given cited candidates). This upgrades
   Thm 5(b1′) on LH, c = 1, from PROOF SKETCH to PROVED: the paper's first masked instance **without LS0**. The crux was
   an exact factorisation of d on states that avoid the masked group (Lemma OF).
2. **Route (b2) is PROVED on LH for every c ≥ 1, no method change, any grid**, under a finite population inequality
   STAB-LH (Theorem B2-LH). The proof does not use the envelope: the delivery region is chosen closed under the
   favourable moves (all states ⊇ S° with any subset of the masked groups and ≤ 19 junk variables); junk is
   non-persistent, so the whole particle system stays there (Prop. CONF, rate O(log^{3.5}n/√n)), and at φ = 1 every such
   state scores S₀ in one round with a fixed probability c₀ (Lemma R1). In D5's terms this is h ≡ 1_𝒩, Γ = 0.
3. **STAB-LH is a real restriction**: it holds in configuration A and in many (g, ρ, ψ) settings including 38/46 c = 2
   settings (all with ψ ≤ 0.2 or ρ = 0.4); it **fails** e.g. at (ρ, ψ) = (0.85, 0.5) for every g tested and in configuration B
   (`s1_stab*.txt`). Where it fails, (b2) on LH is OPEN (§4.7 of PROOF; numerically the run is unaffected).
4. **The envelope with lattice-indicator potentials cannot work at any budget** (PROOF SKETCH, numerically confirmed):
   its oscillation Γ grows like log(N·T) because early crossers multiply with N, while D5 allows log(N/T). A budget
   sequence N_n does not repair it; the fix is the choice of potential (item 2).
5. **Referee of W4-SHARE**: no ERROR; D4, D5, SH, M(a), PD, B2-W4 VERIFIED. Two GAPs: Prop X's scoring clause needs the
   mid-round "visit" gate rate plus an independence-proposal term; Prop G is an upper bound, not grid independence.
   Prop M(b) upgraded to PROVED on LH (Prop. M-LH).

## 2. Statements (full versions in PROOF.md)

**Setting LH (exact Gram).** Groups of size g, within-group correlation ρ_h ∈ [ρ₋, ρ₊] ⊂ (0,1), c linked pairs with
0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i}), v visible groups, null groups; X′X = (n−1)Σ_LH, p ≤ n − 1, g ≤ B_n < 2g; fixed
coefficients θ_{j_a} = β, θ_{j_b} = −ψβ, θ_{j_h} = β_h; σ² > 0 fixed. S° = S₀ ∖ {masked hubs}. EX-A, EX-S, SR, CAL.

- **Lemma OF (PROVED).** If S meets only mutually orthogonal blocks, d(S) = ν[−log(1 − Σ_he_h) + Σ_h log(1 − e_h)],
  e_h = n z_{U_h}ᵀH_{U_h}⁻¹z_{U_h}/(2b₀ + yᵀy); d is monotone in each e_h and
  0 ≤ d(S′) − d(S) ≤ ν(Q_S − Q_{S′})/(2b₀ + Q_{S′}) for S ⊆ S′.
- **Lemma 2.1/2.2 (PROVED).** Start aggregation q, D_b = O_P(g n^{−1/2}), e_n exponentially small; start tails
  π₀(⊇S°, ≥ k extras) ≤ 2e^s(eq)^k, null-extras tail, missing-reference tail, masked-group tail ≤ e(s+k)D_b/p.
- **Theorem NB′-LH (PROVED, given W1-EXP Thm 1/Lemmas 1.1–1.4/Thm 6, Lemma 4.1–4.2).** c = 1, any v.
  P(NB′ᶜ | data) ≤ H₀[2e^{u₀}(eq̃)³ + 2^{s+1}e_n + 2e^s(eq)³ + e(s+2)D_b/p] = O_P(√n/p + n^{−1/2}).
  The d-range over the good draws is ≤ 12 log n (1 + o(1)) ≤ T₀ log r* for all n ≥ n₀.
- **Corollary D2-LH (PROVED, given D2 [W1-T38E, repaired by W3-VT38E] and the above).** c = 1, p/√n → ∞:
  P(S₀ ∉ 𝒮_cal) = O(√n/p) + o(1) → 0, Dep = O_P(n^{−1/2}) with 𝒟 = proxies of j_b; hence
  liminf P(Uᶜ ∩ {Ŝ = S₀}) ≥ 1 − limsup P(U) for the original method.
- **Proposition M-LH (PROVED).** Any c: on Lat(S°) every edge toward S₀ has log κ₀ ∈ −log(2p/s) − ½log n ± O(log log n)
  and log κ₁ ≥ n g_*/2 (1 − o(1)), so γ_φ increases along the lattice for φ ≥ φ_n = O(log n/n).
- **STAB-LH (hypothesis, finite and checkable).** m_STAB := min over S° ⊆ V ⊆ (signal units), t ∈ S°, l ∉ V of
  min{Δ(V − t) − Δ(V), Δ(V − t + l) − Δ(V)} > 0 (Δ = population residual variance).
- **Lemma J, Lemma T, (G) (PROVED; T under STAB-LH).** Junk inclusion odds summed: ε_n = O_P(4^g√(log n/n)); single:
  O_P(4^g log n/√n); truths of S° are removed with probability ≤ 2p²e^{−c₆n} per step at every φ; missing masked hubs
  have posterior addition odds ≥ e^{c₇n} from every state ⊇ S°.
- **Prop. CONF (PROVED under STAB-LH).** For every φ and every x ∈ 𝒩 := {S ⊇ S°, ≤ 19 neutral extras}:
  P_x(round ends outside 𝒩) ≤ a_n = O_P((log n/n)^{3/2}·4^{3g}). Hence P(some final particle leaves 𝒩 before stage T)
  ≤ Nπ₀(𝒩ᶜ) + NT_ea_n = O_P(log^{3.5}n/√n), for **any** frozen grid.
- **Lemma R1 (PROVED under the deletion part of STAB-LH).** For x ∈ 𝒩, P_x(S₀ scored in one round at φ = 1)
  ≥ c₀(x) − o(1), c₀(x) = g^{−c_x}/C(|Λ_x| + B + 2, B + 2) (an order event: missing hubs before their proxies, all
  relevant Gibbs labels before the non-Gibbs labels).
- **Theorem B2-LH (PROVED under STAB-LH).** For every successful 𝓒 and one final island:
  P(S₀ ∉ 𝒮 | 𝓒) ≤ Nπ₀(𝒩ᶜ) + NT_ea_n + (1 − c₀ + o(1))^N → 0; with T38(b)-R and (P) (W1-EXP Thm 5(d)):
  liminf P(Uᶜ ∩ {Ŝ = S₀}) ≥ 1 − limsup P(U), **every c**, original method. No masking condition, no grid condition, no
  SHARE/LT/envelope, no occupancy, no T24/B♯ premises.

## 3. Proofs
All in `PROOF.md`: §1 Lemma OF; §2 NB′ (Lemmas 2.1–2.2, Theorem NB′-LH, Corollary D2-LH); §3 Prop. M-LH; §4 route (b2)
(uniform estimates U1–U3, Lemmas J and T, (G), Prop. CONF, Lemma R1, Theorem B2-LH, relation to D4/D5, the lattice
negative, what is open without STAB); §5 LH-iid remarks. `REFEREE.md` has the W4-SHARE verdicts.

## 4. Evidence

| check | result | file |
|---|---|---|
| D4 Step 5 constants; SH(iii) transition; Prop M(a) | g increasing ½→1, g(1) = 1/(e−1); 1/θ₀ ≤ Σ1/P̲ (worst ratio 1.000); SH 50% point 7.3/9.6/14.2 vs heuristic 6.9/9.2/13.8; M(a) 0 violations in 20,000 | `r0_referee_checks.txt` |
| STAB/GAIN/ZJL/PZL, c = 1 | A: m_STAB = 0.305 (OK); A85: −0.005 (FAIL); B: −0.18 (FAIL); ZJL, PZL = 0 to 1e−16; sweep 66/300 fail; type-based g ∈ {4,9,16}: fails only at (ρ, ψ) = (0.85, 0.5) among those tested | `s1_stab.txt`, `s1_stab_types.txt` |
| STAB, c = 2 | 38/46 settings OK (g ∈ {4, 9}): every ψ ≤ 0.2 and every ρ = 0.4; the 8 failures all have ψ ≥ 0.35 and ρ ≥ 0.7 (cross-pair truth→hub swap) | `s1b_stab_c2.txt` |
| NB′, p = 16 (config A, exact enumeration) | not masked at this p: S₀ drawn in 65–100% of pilots; P(NB′ᶜ) = 0 in all 1,180 pilots; C_b-touching term H·π₀ grows ≈ √n/p (13.8 at n = 200, 20.9 at n = 102,400); d-range on 𝒢 ≤ 2.8 vs T₀ log r* = 655; S₀ scored by end of stage 1 in 100% | `s2_nbprime.txt` |
| NB′, p = 4,000 / 20,000 (exact Gram, n = 10⁴ / 4·10⁴, group partition) | masked pilot: H·π₀(S₀) = 0.008 / 0.004, S₀ never drawn; P(NB′ᶜ) = 0/20, 0/10; φ₁ = 1 (no forced step); weighted share of S° ≥ 0.96; Dep = 0.027 / 0.015; D2 bound (excl. NB′) 2·10⁻²⁹ / 10⁻¹¹⁸ | `s2b_nbprime_largep.txt` |
| (b2) final runs, configs A and A85, n ∈ {400, 1600, 6400}, method grid | 0 confinement exits in 100 islands (also A85, where STAB fails); stage-T round at φ = 1: 94–99.5% of particles score S₀, every island scores; one-round scoring from S°: 0.39–0.43, from S° + proxies + non-hubs + null: 0.24–0.28 (vs c₀(x) = 10⁻³–10⁻⁵) | `s3_b2_run.txt` |
| lattice-potential envelope (same runs) | realised Γ = 6.2–9.9 vs D5 allowance log(N/T_e) = 0.9–1.9 and log(NT) = 10.5–11.5; min_t log P_t ≥ −0.31; Γ for h = 1_𝒩: 0 | `s3_b2_run.txt` |

Honest limits of the evidence: at p = 16 the start is not masked (S₀ is often an initial draw), so s2/s3 show
mechanisms, not masked delivery; the large-p check (s2b) is masked for the pilot but uses the group partition (with
g = 4 and B = 16 the method would pack four groups per block; the LH theorem needs g ≥ 9 at B = 16) and simulates only
the pilot's first stage.

## 5. What fails and why
- **Lattice-indicator potentials (task brief's suggestion).** Γ ≥ log(NT) − O(1): the S₀-side particles appear as soon as
  N·T·κ_φ(S°, j_b) ≳ 1, i.e. log(NT)/(λ_n + ng_*/2) before the lattice crossing, and they are Θ(n) fitter than the
  S°-insiders; junk carriers add ϰ log p. D5 needs ≤ log(N/T): fails for every N (PROOF §4.6(b)).
- **Uniform confinement without STAB.** A swap "truth t → masked hub" is posterior-favourable at states holding all
  non-hubs of t's group (A85, B); the uniform swap reaches such moves with probability O(g/p) per round, which is not
  summable over N·T ≍ n log²n rounds when p ≤ n. Exits are transient (t is re-added at φ = 1), and the runs never visit
  those states, but the uniform argument breaks.
- **Sup-type repair constants.** c₀ uniform over 𝒩 is ≈ 10⁻⁵ at g = B = 4 and ≈ 10⁻¹¹ or less at g = B = 16: the theorem
  is asymptotic only (needs N ≫ 1/c₀). Measured constants are ≈ 0.25–0.85.
- **NB′ needs p ≫ √n.** A proxy draw has d-jump Θ(n) (2,422 at n = 4·10⁴) ≫ T₀ log r* ≈ 655, so one such draw breaks the
  first-stage ESS. The rate √n/p is sharp in mechanism. On LH-iid (p ≥ n) this term is ≍ g/√n automatically (CONJECTURE).

## 6. Needs escalation
1. **Cross-family check of Prop. CONF and Lemma R1** (PROOF §4.3–4.4): the bookkeeping of neutral inclusions (NGI) vs
   swap additions vs the independence step, and the sequential (chain-rule) bounds with the order drawn first. This is
   load-bearing for Theorem B2-LH and is new; a mistake here would sink the "(b2) on LH" claim.
2. **Lemma J's uniformity** (sup over states inside a sum, truncation at z_n² = 2 log(p4^g) + 2 log log n): standard but
   written tersely.
3. **Theorem NB′-LH** is the guaranteed deliverable; its only new ingredient is Lemma OF (two lines of linear algebra)
   and the threshold arithmetic 12.1 log n ≤ 0.6549·max(1000, log₂²n). Cheap to verify.
4. **HQ decision:** Theorem B2-LH makes LS0 unnecessary for a masked consistency theorem on LH whenever STAB-LH holds
   (and D2-LH does so for c = 1 unconditionally). This changes the investment-rule calculus for LS0
   (F-REFINE ARCHITECTURE §4 item 14).

## 7. Outside scope
- The repair argument (Lemma R1) uses an **order event**, not Theorem B/B♯'s progress accounting, and needs only the
  hub gain (G) and junk non-persistence: it replaces W2-PREM's FS-gap and ULR numerics for any start family that is
  closed in the sense of §4.0. This may simplify T24/Thm 3-B′ (route e′) on LH.
- Prop. CONF holds verbatim for the **calibration** runs (pilot and diagnostic islands use the same kernel), so on LH
  under STAB-LH every pilot particle also stays in 𝒩; combined with Lemma R1 at the pilot's last stage (φ = 1) this gives
  S₀ ∈ 𝒮_cal for every c — a second no-tweak route not written here.
- At the study size (n = 200) nothing here applies (dilution masking, W3-PXN Prop. W).

## 8. Confidence card

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| Thm 5(b1′) on LH, c = 1 | Corollary D2-LH: p/√n → ∞ ⇒ P(S₀ ∉ 𝒮_cal) = O(√n/p) + o(1); HPM consistency of the original method | 0.93 | done (PROVED here; review pending) | Lemma OF + start tails | no |
| NB′ on LH-iid (p ≫ n) | P(NB′ᶜ) = O(g n^{−1/2}) | 0.8 | 0.7 | approximate orthogonality of S°-side groups in the d-range | no |
| Thm 5(b2) on LH, every c | Theorem B2-LH under STAB-LH | 0.85 | done modulo independent check of CONF/R1 | junk non-persistence + closed region | no |
| (b2) on LH without STAB | same conclusion for all LH parameters | 0.75 | 0.4 | transient truth-for-hub swaps at states with many non-hubs (§4.7) | no |
| D5 with lattice potentials | cannot certify delivery for any N (Γ ≳ log NT) | 0.85 | 0.6 (PROOF SKETCH now) | lower bound on early-crosser occupancy | — |
| Prop M(b) | Prop. M-LH | 0.97 | done | — | no |
| W4-SHARE D4/D5/B2-W4 | as stated (D4 citing IND-T) | 0.97 | done (VERIFIED, same family) | — | no |

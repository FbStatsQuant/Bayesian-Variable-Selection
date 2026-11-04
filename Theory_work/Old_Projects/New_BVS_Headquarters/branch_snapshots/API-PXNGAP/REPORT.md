# API-PXNGAP — REPORT: closing A-REV3's p ≫ n GAP for Thm 5(b1) (LS0 route) on LH-iid

Run API-PXNGAP (Fable 5.1), 2026-11-02, branch `theory/API-PXNGAP`. All results are **candidates**: not reviewed, not
adopted. Full proofs: `PROOF.md`. Scripts: `scripts/`; outputs: `results/`. Status words per `PROTOCOL.md`.

## 1. Headline

- **PROVED (candidate), given the locked [T22i], [T22ii], [T03], the classical [CONC], and W7-PART Theorem B:** Thm 5(b1)
  with LS0 holds on LH-iid for every polynomial p ≤ n^A (p ≫ n included), with **every premise discharged on the random
  design**: partition recovery with an explicit probability (Theorem R), uniform control of the start mass with an explicit
  moment bound (P3′), eligibility of the start mode (P5), TD′ for LS0 with repaired lemmas (P6′), π(S₀) → 1 under the joint
  law (P8′), and the composition inequality P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n → 0 (PROOF §10).
- **Each A-REV3 / A-REV6 objection is answered by a specific lemma** (§2 below): the out-of-range Tr(c) use is replaced by
  Lemma Tr-J (any fixed dimension, u ≤ n/4, polynomial families); the false "≤ 1" and the RSS-error omission in Lemma U are
  replaced by the self-contained Lemma E with explicit κ_E and a halved signal margin; the random-partition quantifier is
  isolated in Lemma T; progress-move ties are excluded from D_S; the production search is analysed directly (Lemma LS).
- **What genuinely fails and is stated as an obstruction (COUNTEREXAMPLE, deterministic):** the family needs (SIZE)
  g ≤ B_n < 2g; with the study's groups of 5 (2g ≤ B) the partition packs ≥ 2 groups per block and LH masking is not
  available, so the theorem does not describe the study's own generator (PROOF §11 (O1)). The p-range needs no restriction
  beyond p ≤ n^A (any A).
- **Numerical evidence** (exact objects, small sizes, through `owls_run`): see §4.
- **Not claimed:** P(U) → 0; the original method without LS0 (P7 / W5-R1 remain GAP, c = 1 only); masked PIP/evidence
  accuracy; anything about adaptive packing of groups of 5.

## 2. Point-by-point answer to A-REV3's GAP (and A-REV6's re-review)

| # | Objection (A-REV3 §"P6: GAP and repairs", A-REV6 PARTITION) | Answer | Where |
|---|---|---|---|
| 1 | Lemma Λ(a) calls Tr(c) over all sets of size ≤ s₀+2 (≈ p^{s₀+2} of them, not ≤ n^{A+1}2^{17}), and the projection dimension s₀+2 and u can exceed 16 | **Lemma Tr-J**: Beta(j/2,(m−j)/2) truncated moment (a) for any j, u; uniform tail (c) for any fixed J, any u ≤ n/4, any family of ≤ C n^D variables, with threshold t_n = 8(D+1) log n. Proof: Laurent–Massart plus a union bound; the Γ-ratio step uses Wendel for every real a > 0. Lemma Λ(a) is re-proved with J = s₀+2, u ≤ s₀+2, D = A(s₀+2) | PROOF §3, §8.2 |
| 2 | Lemma U(U1) writes ν(1.02 + 1/(nφ₀²))/(c_*n) ≤ 1, false (≈ 20 with W1-EXP's c_*) | **Lemma E** (self-contained, no W1-EXP citation): on a polynomial family of bounded-size sets with λ_min(R̂_A) ≥ φ₀², F(A) = log w(|A|) − ½|A|log(n+1) − ν log RSS_A + c_n + R_A with |R_A| ≤ κ_E := 0.52/c_E + 1, c_E := σ²/(12(M+σ²)); the RSS floor RSS_A ≥ nσ²/2 is proved with explicit failure probability | PROOF §4 (E1)–(E4) |
| 3 | U3 must account for the RSS error by first shrinking the signal margin | Lemma U(U3): if Λ_{A′}/n ≥ Λ_A/n + c′ then F(A) − F(A′) ≥ (n/2)log(1 + c′/(2(σ²+M))) − (2A+1)log n − 2κ_E − 2; the error C₂n^{2/3} of (E5) is absorbed by halving c′ | PROOF §8.1 |
| 4 | "strict margin over every other neighbour" must exclude other progress additions (ties) | D_S is stated for S itself and **non-progress** neighbours only; progress ties are allowed, and Lemma LS shows a tie among missing-hub additions does not obstruct the path | PROOF §8.3, §8.4 |
| 5 | Random-partition quantifier: fixed-group laws must be established unconditionally and only then intersected with the recovery event; do not condition Beta laws on recovery | **Lemma T** states the rule once: every block object has a group version; on 𝒜_n they coincide; P(E) ≤ P(Ẽ) + P(𝒜_nᶜ). All Beta laws (Lemma B) are unconditional and 𝒜_n is intersected last | PROOF §2, used in §6, §7, §8.5 |
| 6 | P1 verified only on the restricted family; recovery needs an explicit probability | **Theorem R** = W7 Theorem B on (SIZE): P(blocks ≠ groups) ≤ (2/(√π(1−ρ))) p²√n e^{−(n−4)I*}, ≤ p^{−C} eventually | PROOF §1 |
| 7 | EXP′ (W1-EXP, candidate) is cited for the start tables | Replaced by Lemma E on the family of all within-group subsets (J = g, D = A); the remainder telescopes to a single 2κ_E (sharper than PXN's e^{jκ}) | PROOF §4 Rem. 2, §6 (6.1) |
| 8 | The lattice route must be written: each preferred move adds a missing hub, ≤ c moves, final scan certifies on the local-maximum event; scoring ≠ certification ≠ recovery | **Lemma LS** (from M §6.10 directly): c moves, S₀ scored iff ℓ ≥ c − 1, certified iff (L) and ℓ ≥ c; (L) failures are posterior misses charged to 2E₀δ₁, not discovery misses | PROOF §8.4, §11 (O3) |
| 9 | LS0 is a method change; the C++ does not choose the start-mode centre; operational assumptions must stay | Kept verbatim from [W6]: OP-LS0 (centre emitted, scans completed, post hoc allowed, stopped LS0 ∈ U), GUARD, EX-A, EX-S, CAL, SR | PROOF §10 |
| 10 | P7 (no-tweak, c = 1): W5 R1 Step 2 calls Tr(c) with u ≤ s+k₀ and exponent A(k₀+1) | Not used by the theorem. Lemma Tr-J(c) with J = 1, u ≤ s + k₀, D = A(k₀+1)+1 covers exactly that call (table in PROOF §3); the c = 1 restriction stays. Recorded under Outside scope | §7 below |
| 11 | P8 verified; retain T03 and the joint-family hypotheses; no conditioning on diagnostics | Restated as P8′ with the de-randomisation lemma; nothing conditions on completion or diagnostics | PROOF §9 |
| 12 | W7 Lemma 3 (full-vector conditioning) is wrong; Theorem C needs it; study groups of five are outside | Only Theorem B is used (A-REV6: VERIFIED on SIZE); Lemma 3/Theorem C are not cited. Groups of five: obstruction (O1) | PROOF §1, §11 |

## 3. The theorem (PROOF §10)

**Hypotheses.** (F) LH-iid (PROOF §0): fixed g, c ≥ 1, v ≥ 0, ρ, |ψ_i| < ρ, nonzero β's, σ²; rows iid N(0, Σ_LH); truth
θ_{j_a} = β_i, θ_{j_b} = −ψ_iβ_i; (SIZE) g ≤ B_n < 2g; 18 ≤ p_n ≤ n^A, p_n → ∞; s₀ = 2c + v fixed. (OP) EX-A, EX-S, CAL, SR,
GUARD, OP-LS0 as in W6-FIXREV1; v3 budgets indexed by n.

**Conclusions.** (R) P(blocks ≠ groups) ≤ (2/(√π(1−ρ)))p²√n e^{−(n−4)I*}. (S) 1 − π₀(S°) = O_P(√(log n/n)) with an explicit
moment bound; π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} → 0 (masked regime). (E) P(S̃₀ = S°) → 1. (T) P(LS0 scores S₀) → 1 and
P(LS0 certifies S₀) → 1. (P) 1 − π(S₀) = O_P(√(log n/n)) under the joint law. (C) For every n,
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n with D_n ≤ P(LS0 does not score S₀) → 0; hence liminf P(𝒪, Ŝ⁺ = S₀) = 1 − limsup P(U).
(K) LS0 costs ≤ 1 + (ℓ_n+1)max_k[p + k(p−k)] scores, c + 1 scans on the event of (T).

**Status: PROVED (candidate)** given [T22i], [T22ii], [T03] (locked), [CONC] (classical) and [W7-B] (candidate; VERIFIED on
SIZE by A-REV6, and re-derived in PROOF §1 from W7's Lemma 2 and the PXN P1 margin argument). Every other step is proved in
PROOF.md and was checked line by line in this run. The proof is **asymptotic**: the proven (D_S) margin is negative at
n = 200 for typical parameters (PROOF §11 (O5)); the exact checks (§4) show the route succeeding at n ∈ {100, 200, 400}
because the actual margins are much larger than the proven lower bound.

## 4. Evidence (exact small-scale checks; all through `owls_run -j 2`)

All runs: one `owls_run -j 2` job (`scripts/run_all.sh`), numpy/scipy, fixed seeds, exact objects (EX-A) via the W3-PXN
scorer `scripts/pxn_core.py` (unchanged copy) and the LH-iid generator `scripts/lh_gen.py`.

**4.1 Lemma Tr-J (`scripts/check_trJ.py` → `results/check_trJ.txt`).** (a) truncated-moment bound vs exact quadrature for
j ∈ {1,…,18}, u ∈ {0,1,5,20}, n ∈ {100,200,800} (beyond PXN's j, u ≤ 16): max exact/bound = 0.436, no violation.
(c) exact Beta tails at τ_n = 8(D+1)log n/n vs the Laurent–Massart bound for (J, D) = (16, 2) [P3 row] and (5, 10)
[Lemma Λ row with s₀ = 3, A = 2], n ∈ {200,…,3200}: 0 violations in 2·3·J·5 cases. Note that the *explicit* bound
C n^D n^{−(D+1)}e^{√(2J(D+1)log n)} is > 1 at these n (it is asymptotic), while the exact union bounds are ≤ 10⁻¹⁷; for
D = 10, τ_n > 1 until n ≈ 10⁴ — the lemma is a limit statement, as used.

**4.2 Population margins (`scripts/check_margins.py` → `results/check_margins.txt`).** 60 random LH settings (seed
20261102; c ≤ 3, v ≤ 2, g ∈ {3,4,5}, ρ ∈ (0.3, 0.9), |ψ| < ρ): brute-force minimum of λ(A) − λ(P*) over every lattice state
and every non-progress neighbour is ≥ c₂ in 60/60 (ratio 1.00–1.12 at the tightest), and the (L) minimum over deletions and
swaps of S₀ is ≥ c₅ in 60/60. The closed forms of PROOF §8.3 are valid lower bounds and sharp in most settings.

**4.3 Lemma E (`scripts/check_lemmaE.py` → `results/check_lemmaE.txt`).** LH-iid, g = 10, ρ = .7, ψ = .5, c = v = 1, at
(n, p) = (200, 500) and (400, 1000), family = all subsets of 6 groups + 3000 random sets of size ≤ s₀+2 (9,139 sets):
(E1) η_A ∈ [−0.18, 0] within the bound; (E2) a_A ∈ [0.020, 0.43] within [0.02, 1.05]; (E3) min RSS_A/(nσ²) = 1.61 (≥ ½),
‖Y‖²/(3(M+σ²)n) = 0.32 (≤ 1), min RSS^y_A/(c_E n) = 20 (≥ 1); (E4) the remainder R_A ranges over 0.41 nats (n = 200) and
0.31 (n = 400), against the proven 2κ_E ≈ 38 — the bound holds and is loose by ~100×; (E5) max |RSS_A − nσ² − Λ_A|/n^{2/3}
= 1.6 and 2.3; (4.1) within-group single-addition remainders over 10,926 additions range over 0.15–0.20 nats.

**4.4 LS0 route end to end (`scripts/check_route.py` → `results/route.jsonl`, `results/route_table.txt`).** g = 10, ρ = .7,
ψ = .5, β = 1, σ = 1; c ∈ {1, 2}, v = 1; B = ⌊√n⌋ (10 at n = 100, 14 at 200, 16 at 400), so (SIZE) holds at every cell.

| cfg | n | p | reps | blocks = groups | S̃₀ = S° | 1 − π₀(S°) (min/med/max) | med log π₀(S₀) | LS0 scored S₀ | certified at S₀ | min D_S margin | (L) fail | D_S fail |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c=1 | 100 | 300 | 10 | 10/10 | 8/10 | .27/.44/1.00 | −8.0 | 9/10 | 6/10 | −3.3 | 4 | 3 |
| c=1 | 200 | 500 | 10 | 10/10 | 10/10 | .19/.31/.56 | −8.7 | 10/10 | 9/10 | −0.1 | 1 | 1 |
| c=1 | 200 | 1000 | 6 | 6/6 | 6/6 | .21/.34/.53 | −9.4 | 6/6 | 6/6 | +1.1 | 0 | 0 |
| c=1 | 400 | 1500 | 4 | 4/4 | 4/4 | .17/.19/.24 | −8.7 | 4/4 | 4/4 | +5.8 | 0 | 0 |
| c=2 | 100 | 300 | 10 | 10/10 | 0/10 | .81/.98/1.00 | −16.4 | 8/10 | 5/10 | −4.4 | 4 | 4 |
| c=2 | 200 | 500 | 10 | 10/10 | 8/10 | .28/.49/.93 | −16.3 | 10/10 | 10/10 | +2.5 | 0 | 0 |
| c=2 | 200 | 1000 | 6 | 6/6 | 5/6 | .39/.56/.77 | −18.0 | 5/6 | 4/6 | −2.4 | 2 | 2 |
| c=2 | 400 | 1500 | 4 | 4/4 | 4/4 | .19/.27/.28 | −18.6 | 4/4 | 4/4 | +5.7 | 0 | 0 |

Reading. (i) Partition recovery: 60/60, consistent with Theorem R (W7's MC rate ≤ 1.5·10⁻⁴ at (200, 500)). (ii) Masking:
log π₀(S₀) ≈ −c(log p + ½ log n) + O(1) as P4 says (−8.7 vs −c(6.2 + 2.6) = −8.8 at (200, 500, c = 1)). (iii) The start
mass on S° is far from 1 at these n (1 − π₀(S°) ≈ 0.2–0.5 at n ∈ {200, 400}; q ≈ 0.16–0.29, so the T22 bound
(s+1)q/(1−q) + se is often > 1 and vacuous): the √(log n/n) rate is an asymptotic statement, and eligibility relies on
π₀(S°) > ½, which holds in 33/36 cells at n ≥ 200 and fails at n = 100 for c = 2 (0/10: the mode is S° plus extras or with
a proxy). (iv) LS0 scores S₀ in 56/60 overall and in 35/36 at n ≥ 200; the one failure at n ≥ 200 (c = 2, p = 1000, rep 5) is
a genuine D_S failure at a lattice state (first move non-progress, path leaves the lattice) — the finite-n boundary of
P6′, not a counterexample to the limit. (v) Certification fails more often than scoring: (L) failures (some S₀ ± neighbour
beats S₀) are 11/60 overall, 3/36 at n ≥ 200, consistent in order with the (s₀+1)/√(2πn t_n) ≈ 2–4% addition-part formula
plus finite-n swap failures; these are posterior misses charged to 2E₀δ₁ (PROOF §11 (O3)). (vi) The proven (D_S) margin
is negative at every cell (PROOF §11 (O5)); the observed minimum lattice margins (−4 to +11 nats) are what decides at
these n. Everything is consistent with an asymptotic theorem whose finite-n reach starts around n ≈ 200 for c ≤ 2 on this
family.

## 5. What fails and why (routes tried and abandoned)

- **Keeping PXN's Lemma Tr as stated and only re-counting the family.** Not enough: A-REV3's objection is to the dimension
  (j, u ≤ 16) as much as to the family count. The dimension restriction in PXN's Tr was never needed: the Γ-ratio bound
  Γ(y+a)/Γ(y) ≤ (y+a)^a holds for every real a > 0 (Wendel), and the χ² tail is dimension-free up to the √(jt′) term. Hence
  Lemma Tr-J with no dimension cap.
- **Citing W1-EXP (candidate) for the score expansion.** Abandoned: the needed statements (E1)–(E4) are three lines of
  linear algebra plus a χ²/Gaussian union bound, and proving them removes a candidate dependency and fixes the U1 constant
  at the source.
- **Citing W1-T37R Theorem A(A3) for the lattice route.** Abandoned in favour of Lemma LS proved from M §6.10: the centre
  has no extras, so progress moves are exactly missing-hub additions and the argument is five lines.
- **Extending the theorem to superpolynomial p (log p = o(n)).** Not pursued: the discovery half plausibly survives with
  t_n ∝ log|family|, but [T03] is locked for p ≤ n^A only, so (P) would be unavailable. CONJECTURE, recorded in (O2).
- **Covering the study's groups of 5.** Impossible on this family: with 2g ≤ B next-fit packs two groups per block
  deterministically (W7 CE2) and, by PXN Prop. Q (sketch), the linked pair is co-blocked and masking disappears. The right
  object for the study regime is a different family (dilution masking, PXN §14, CONJECTURE), outside this task.
- **Making the (D_S) bound non-vacuous at n = 200.** Not attempted; the (2A+1)log n prior/determinant penalty against
  (n/2)log(1 + c₂/(4(σ²+M))) is intrinsic to a worst-case union over 𝔉_n. A path-wise finite-n bound would need the
  actual (not worst-case) prior differences, which are O(1) on the lattice (sizes differ by 1); this would improve the
  log n term but not the worst-case c₂ (W5 R5's sharper m₀♯ is the relevant object). Left as an improvement, not a gap.

## 6. Needs escalation / independent check

1. **Lemma Tr-J(c) constants** (PROOF §3): the choice x = t′/2 − √(jt′) and the condition t′ ≥ 6j; a referee should re-derive
   the exponent (D+1) and confirm the family counts in the table of §3 (in particular D = A(s₀+2) for Lemma Λ(a)).
2. **Lemma E (E2)**: the commuting-matrix identity G⁻¹ − nH⁻¹ = G⁻¹(G+I)H⁻¹ and the bound ‖P_Ay‖² ≤ n − 1; and (E3)'s
   quadratic-in-√Λ minimisation. These are elementary but they carry the U1 repair.
3. **Lemma Λ(a)**: that the null columns' span is Haar given X_{𝒮𝒱} even though null groups are equicorrelated (the span of
   Π^⊥GΣ^{1/2} equals that of Π^⊥G). Same argument as Lemma B, which A-REV3 verified; worth a one-line confirmation.
4. **Theorem R**: used as W7 Theorem B; its Hotelling-density bound (W7 Lemma 2) is cited, not re-proved here.
5. **The operational closure** (OP-LS0 + GUARD ⇒ 𝒪 ∩ {S₀ ∉ 𝒮⁺} ⊆ {LS0 does not score S₀}) is taken from [W6]; a referee
   should confirm it against the engine's ledger behaviour (centre emission).
6. **Lean-readiness**: Lemma LS and (C) are finite and deterministic; Tr-J(a), (E1), (E2) are finite inequalities.

## 7. Outside scope (recorded, not pursued)

- **W5 R1 (no-tweak route, c = 1) range objection.** A-REV6 keeps P7 at GAP because R1 Step 2 calls PXN Tr(c) with
  u ≤ s + k₀ and family exponent A(k₀+1). Lemma Tr-J(c) with J = 1, u ≤ s + k₀ (fixed), D = A(k₀+1) + 1 is exactly that
  call. With this substitution R1's Step 2 has no range problem; the c = 1 restriction and D2's exactness premises remain.
  Not re-verified here beyond the lemma substitution.
- **Lemma E as a general tool.** It gives EXP′ (W1-EXP Thm 1) and PXN Lemma U on any polynomial family of bounded-size sets
  with a Gram lower bound, with explicit constants; it could replace the W1-EXP citations in W3/W4/W5 wherever they are
  used on such families.
- **Finite-n (D_S) margins.** The observed lattice margins at n = 200 (§4) are 1–2 orders of magnitude above the proven
  bound; a path-wise bound using O(1) prior differences on the lattice would be the natural finite-n statement for T37.

## 8. Confidence card (Thm 5(b1), masked regime, LS0 route, LH-iid, p ≫ n)

| item | value |
|---|---|
| Refined statement | PROOF §10: LH-iid with (SIZE), p ≤ n^A; (R)(S)(E)(T)(P)(C)(K) |
| Confidence it is true | **high** (every step is either locked, classical, or proved here with explicit constants; the only candidate input is W7-B, verified by A-REV6 on exactly this scope) |
| Confidence it is provable at reasonable cost | **high** — it is written; what remains is cross-family review |
| Crux | (i) Lemma Tr-J's range (closes objection 1); (ii) Lemma E's explicit constants (closes objection 2–3); (iii) Lemma T's quantifier discipline (objection 5); (iv) (SIZE), which excludes the study's generator |
| Data evidence | §4: exact route at n ∈ {100, 200, 400}: partition recovered 60/60; start mode = S° in 33/36 at n ≥ 200 (0/10 at n = 100, c = 2); LS0 scores S₀ in 35/36 at n ≥ 200, certifies in 33/36; all four lemma-level checks pass with no violation |
| Risk | relevance: LH-iid with groups of 9–16 is not the study's design (groups of 5); the proven margins are vacuous at n = 200 (asymptotic theorem) |
| Method change needed | **yes, LS0** (as in all (b1) statements): one deterministic local search from the start mode, ≈ (c+1)(1+s₀)p scores, addable post hoc. No change to the sampler |

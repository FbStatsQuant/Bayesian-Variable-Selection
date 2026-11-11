# W3-START — PLAN (lead: Claude Fable 5.2, effort high)

Ticket: PROGRAM item 2, start-mass rate. Brief: `BRIEF.md`. Protocol: `Theory_work/Wave3/PROTOCOL.md` (rules 9–16).
Leg A ended at CP1 (target fixed); leg B runs to CP2 (key lemma and mid-point review). No git state is changed by the lead.

## 1. What the object is
`π₀(S) = γ₀(S)/Z̄₀`, `γ₀(S) = ϖ(|S|)∏_b r_b(S ∩ C_b)`, `r_b(U) = m(U)/m(∅)`, exactly as `main` computes it (pins in
`STATEMENT.md` §1). Write `o₀ := (1 − π₀(S₀))/π₀(S₀) = Σ_{S≠S₀} γ₀(S)/γ₀(S₀)` (the start odds against S₀; W3-SAMP's o₀).

## 2. Route (three layers)
1. **Deterministic aggregation (Lemma AGG).** For any data and any deterministic Q ⊇ S₀: the mass outside the lattice
   𝓛(Q) = {S₀ ⊆ T ⊆ Q} is bounded by two table functionals — an averaged null-addition ratio `U_Q` and a truth-block
   functional `Ξ(Q)` — and, with `T₁` the sum of the single-null block Bayes factors: for Q = S₀, s₀ < K and U < 1,
   `o₀ ≤ T₁ + R₂ + [∏_b(1 + Ξ_b) − 1](1 − U)^{−(16s₀+1)}` and `o₀ ≥ T₁`; if moreover s₀ + 16 ≤ K, also `o₀ ≥ c_sΞ`
   (the truth-block functional Ξ refines the cruder truth-deletion ratio e_n of T22). A second deterministic fact gives a floor: every one-variable table ratio is
   ≥ (n + 1)^{−1/2}, so `1 − π₀(S) ≥ c·n^{−1/2}` for every **unsaturated** model (|S| < K) and every data set.
   Predecessor: T22(i) (SOP:TH116). Re-proved here (short), in lattice form and with the leading term isolated.
2. **Fixed design (Theorem START-F).** On a toolkit event proved in this ticket under a constant unnormalised Gram
   floor (Lemma TK; the argument of C-GROW L0 / GEN L1 with the floor-dependent bounds redone), each block-table step is
   `(n + 1)^{−1/2}·(RSS_T/RSS_{T∪l})^ν·e^{O(1)}`; in the **small-gain regime** that the averaged leakage condition forces
   (gains O(τ² log n), so partial R² = O(log n/n)), this is `(n + 1)^{−1/2}·exp(gain/(2τ²) + O(1))` — the linearisation
   is not used outside that regime. Taking a truncated expectation over the noise turns `U_Q` into a deterministic
   **averaged leakage functional** `𝔏_n(Q; h)` of (X, θ*), with a truncation level h_l per null column inside a summable
   tail budget; a visibility condition (constant level, or margin form) makes
   the truth-block functional Ξ polynomially small. Predecessor: T22(iii), which assumed the expansion (EXP′) and a
   uniform leakage bound; both are removed.
3. **Random design (Theorem START-R).** The fixed-design theorem is uniform over its class, so it transfers to any
   random design — with coefficients, support and leakage set measurable in the design and Gaussian noise given the
   design — once the sample-level hypotheses hold with probability → 1. For Gaussian rows
   the sample-level hypotheses follow from W3-RM's population conditions (V-R), (L-R) with Q = S₀, (FL-R): the averaged
   functional absorbs the Gaussian fluctuations of the off-block signal, which a uniform leakage bound cannot.

Additional clauses: necessity/limits (floor; one leaking null; one invisible truth; masked and strong-factor designs
not covered); interface corollaries (P-START with rate, a deterministic inequality for P-OVL); misspecified candidate
sets (C-MIS) by the exact reduction.

## 3. Steps of leg A (to CP1; done)
| step | output | reviewer |
|---|---|---|
| 1 | PLAN.md, STATEMENT.md v1.0, LOG.md | — |
| 2 | statement-lock review (frozen manifest; blind first read; a later round adds a reconciliation reviewer) | Sol (codex gpt-6.1-sol, high), blind |
| 3 | boundary-violation numerics on the production core (`numerics/`) | lead |
| 4 | ASSUMPTION_MAP.md; "better theorem" review BT1 (frozen MANIFEST_BT1) | Astra (codex gpt-6-astra, high), blind |
| 5 | dispositions; CHECKPOINT_1.md; stop | HQ |

## 4. Proof obligations
Leg B (to CP2), files in `lemmas/`: L1 AGG + FLOOR (deterministic) · L2 Lemma TK: toolkit under (GF-16), τ-form RSS
bounds, score expansion · L3 Lemma J and bridge (B-L) with column levels · L4 visibility bridges (B-V1), (B-V2) ·
L5 assembly (C1) and Theorem START-F (T1)(a)–(d). Each lemma: falsification numerics (`numerics/lemmas/`) and a
cross-family line check; then the independent mid-point review (CP2).
After CP2 (to CP3): L6 corollaries F1–F4 · L7 necessity (C2), (T4) · L8 random-design transfer (T3)(a) · L9
Gaussian-row bridge (B-R) · L10 interface, OVL and MIS corollaries · sweep · council.

## 5. Consumed claims (registry id @ version)
None. (C-GROW:L0.1@1.0.0, C-GROW:L0.2@1.0.0 are stated with the normalised Gram floor; the toolkit is re-proved locally
as Lemma TK under the constant unnormalised floor. C-MIS:LemR is not consumed; its Gaussian-sum reduction is re-proved
locally as Lemma R′.)
Consumers addressed: W3-SAMP:C@1.1.1, W3-SAMP:D@2.1.1 (premises P-START, P-OVL). Cited as limits, not consumed:
W1-PXN:Thm-PXN(S)@1.0.0. Predecessors re-proved or superseded in strength, not consumed: SOP:TH116@1.0.0 (T22(i),(iii)),
W3-RM:B1@1.0.0, W3-RM:B2tau@1.0.0 (author-only status).

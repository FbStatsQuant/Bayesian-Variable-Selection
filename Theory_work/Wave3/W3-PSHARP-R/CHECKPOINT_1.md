# CHECKPOINT 1 — W3-PSHARP-R (T12; Tier B, NORMAL mode) — 2026-11-15

**Plain words (for HQ's H5 card).** The paper's "the rate cannot be improved" theorem currently says the posterior
error 1 − π(S₀ | y) is at least (s₀+1)√(log p/(πn)) **in probability**, and only for p → ∞. This rider adds an
**expectation** lower bound that holds for **every p**, bounded p included:
E[1 − π(S₀ | y)] ≥ (1 − o(1))(s₀+1)·[2(p−s₀)/(2p−1−s₀)]·√(log(p√n/(s₀+1))/(πn)). For p = n^a the constant
√((a+½)/π) replaces √(a/π). So the √(log n) loss in the posterior mean is present even with a handful of
variables. It comes from rare large gains of a single extra variable, not from the number of competitors. Two
readings of the parent must change: "no claim when log p = o(log n)" now holds **in probability only**. Bonus:
at the critical sparsity scale on orthogonal nulls, π(S₀) ≤ e^{−λ} + o_P(1) in place of 1/(1+λ). Nothing in the
parent is weakened.

## Locked statement
`STATEMENT.md` **v1.1, locked** (delta over W3-PSHARP; sha256 6123714c…). Lock: Sol L01, `reviews/L01_statement_lock_sol.md`:
LOCK-WITH-AMENDMENTS, FATAL 0 / MAJOR 1 (summary overclaim in §0 row R1) / MINOR 3. The reviewer found no counterexample
and derived every claim item analytically. All four findings were accepted (`reviews/L01_disposition.md`). Two of them
are free strengthenings adopted before the lock: A2-E without the spherical rank condition, and an expectation corollary
of A2C.

## Target clauses (for HQ's decision)
| clause | STATEMENT | headline? | tag vs parent |
|---|---|---|---|
| Prop A-E: E δ_n ≥ (1 − ϵ − Λ^E_n)Λ^E_n for n ≥ n₀(ϵ, …), every null-block size N_n ≥ 1, both witnesses | §3.1 | feeds headline | NEW-CLAIM |
| Cor A1-E: liminf E δ_n / [(s₀+1)(2(p−s₀)/(2p−1−s₀))√(ℓ_n/(πn))] ≥ 1; (a) √((a+½)/π) r_n; (b) fixed p | §3.2 | **yes (PSHARP Cor A1)** | **STRONGER** (implies parent :72) |
| Cor A2-E: E δ_n = O(r_n) ⇒ s₀ = O(1), every p | §3.3 | changes reading of B3 | NEW-CLAIM |
| Prop A2C: π(S₀) ≤ e^{−λ} + o_P(1) on (W-orth) at Λ_n → λ (+ expectation form) | §3.4 | no (Cor A2 rider) | STRONGER on its slice |
| readings A3′ (:84-88), B3′ (:109) | §4 | yes (headline remark) | corrections, not claims |
Hypotheses that move: N_n → ∞ dropped (N_n ≥ 1); (log p)² = o(n) added for a general orthogonal block (automatic
when all nulls are used); (W-sph) growth conditions are stated in log(pn) in place of log N_n.

## Evidence and files
- `TARGET.md`: assumption map, parity table (beats the parent on every changed clause; A2C is short on scope, a named open
  item), better-theorem input = the sharp2/f02 audit (dispositions in TARGET §4).
- Numerics N1 (`numerics/ae_fixed_p_out.txt`): exact orthogonal design with p ∈ {2, 3, 5} fixed, n up to 10⁶:
  E δ_n/Λ^E_n = 0.99–1.03. Against the parent's normaliser the ratio grows like √log n.
- `READER_DELTA.md` v0.2: new Theorem 3(b) text with two displays (expectation for every p; in probability for p → ∞),
  and bridges B3.3–B3.7. No internal ids in the reader text.
- `PLAN.md` v1.1, `DEPS.tsv`, `LOG.md`. HOLDS.md (origin/main): no hold. No lemma written yet (v4 §3.2).

## Plan after a go (about 3.5 lead hours; CP3 target Tue 11-17, latest Wed 11-18 18:00 CT)
1. `lemmas/AE_expectation.md`, about 1 h: Lemma T (truncation at ϵ/c_n, E U² ≤ T·E U), the two witnesses, and the
   corollaries by sub-block.
2. `lemmas/A2C_critical.md`, about 0.75 h; it drops to a named open item if it stops being a restatement.
3. One Sol line-check batch for both lemmas, then citecheck.
4. REPORT, then council R1 (Sol + Opus seats), then CP3.
Kill budget 3 per lemma.
Asks: none. No Fable, no helper needed (an optional Sonnet numerics helper for N2, p = n − 1).

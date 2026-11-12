# SL1 disposition (lead) — statement lock of STATEMENT v1.4.0

Review: `reviews/SL1_statement_lock_sol.md` (Codex gpt-6.1-sol, high, blind), manifest
b86651a97d64237b6602df284fd2590f759eaabca4db9e6fd2642fe97a43fbda. Verdict: **LOCK WITH CHANGES** — 0 CRITICAL, 0 MAJOR,
4 MINOR, 2 optional. All six are applied; the result is `STATEMENT.md` **v1.4.1**. No definition, hypothesis or claim
changes. The previous text is kept at `reviews/prev/STATEMENT_v1.4.0.md` (sha256 0128495d…a029, the row of the SL1
manifest).

| # | finding (SL1) | disposition | where (v1.4.1) |
|---|---|---|---|
| R1 | MINOR — the header said the changed proofs are supplied and author-proved; (D1) said "proved in"; (N2⁺) said P3 "gives a design"; none is written at the lock | **Applied, in a status-neutral form.** The header now reads: the file fixes target statements only and asserts no proof status; the proofs belong in `lemmas/P1`–`P4` (sketches: `PLAN.md` §3); whether a proof is written or checked is recorded outside the file. (D1): "Elementary facts (proof file: …)". (N2⁺): "a design: sketched in `PLAN.md` §3 under P3; proof file `lemmas/P3_NEC.md`". The reviewer's wording ("planned", "to be proved", "will be supplied") would have had to be edited again once the proofs exist; the neutral wording removes the false status claim and stays true afterwards. The header also adopts the reviewer's description of version 1.4 ((D1) added, (L-R) replaced by (D2), eight superseding claims, Lemma LEAK-0 added). | `:9-14`, `:58`, `:161-162` |
| R2 | MINOR — "every hypothesis other than (L-R)" contradicts the removed F2 growth hypothesis | **Applied, with a complete list.** The reviewer lists three changed hypotheses; the sentence now lists all five: (L-R) → (L-R⁺); the F2 growth condition (removed); the visibility condition admitted in OVL; the premise of (N2); the functional that r̄_n bounds in the Q = S₀ clause of (T3)(a). "its rate" → "its Gaussian-row rate", as required. | `:25-28` |
| R3 | MINOR — "the same holds for the O_P bound" is wrong as an explanation: the exponential right side can be ≥ 1 while the polylogarithmic rate tends to 0 | **Applied** (the reviewer's text; the rate is named b^Q_n because b_n(h) is the tail budget). The claim is unchanged. The constant-dependent split is the proof to be given in `lemmas/P4_BR.md`. | `:140-144` |
| R4 | MINOR — "the leading term of the odds … has no first moment" is false for the coded odds at fixed n | **Applied** (the reviewer's sentence about the cut-off and its Gaussian envelope). | `:198-199` |
| O1 | `PLAN.md:25`: 16 − s₀ is negative for s₀ > 16 | **Applied**: \|𝒩_exc\| ≤ max(0, 16 − s₀) ≤ 15. The proof file will prove it in this form (S₀ ∪ 𝒩_exc lies in one block only when 𝒩_exc ≠ ∅). | `PLAN.md:25` |
| O2 | `STATEMENT.md:56`: make "hence 1/p ≤ 4𝔏^♯" subject to s₀ ≥ 1, p > s₀ | **Applied**: "hence, still for s₀ ≥ 1 and p > s₀, …". | `:59` |

Other changes in v1.4.1: the version line (`:4`); one paragraph of (N2⁺) re-wrapped (`:161-166`, no word changed
except the item R1 above).

Used from the reviewer's "Checks performed" (not findings; taken into the proof plan):
* check 9 — a non-vacuity design for every s₀ ∈ {1, …, 15} (p = 17, equal truth coefficients, cross-correlation ρ_n
  between truths and nulls). `lemmas/P3_NEC.md` will give this family, verified independently, instead of the s₀ = 1
  sketch only.
* check 11 — the split for the clause C_L = 0 with a threshold T_ε; `lemmas/P4_BR.md` will prove the clause this way.

Next: one Sol diff check (round SC1) of v1.4.0 → v1.4.1 — each finding resolved, and "editorial only" (PROTOCOL rule 15).

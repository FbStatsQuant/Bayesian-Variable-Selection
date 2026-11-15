# W3-RM2 — SHARPNESS record (claim (C6))

Per assumption: what is **proved** (always about the route — the events the proof uses), what is **observed**
(finite-n probes of the validated LS0 re-implementation started from the start mode; `numerics/RESULTS.md`; nominal
classification; the sampler, the posterior input and the full method's reported model were not tested), and what is
**open**. No statement below asserts that an assumption is necessary for the conclusion Ŝ⁺ = S₀. The parent record
`Theory_work/Wave3/W3-RM/SHARPNESS.md` (§1 the conditioning size 15, §2 visibility, §3.1 the constant η_A) applies
unchanged to (V), the floors and the Form F leak level and is not repeated.

## 1. The size of the leak set: |Q| ≤ n^b

* **Proved.** In each sandwich proof b is paid at exactly one line, the junk-exclusion margin (in Form R, b < ½ is
  also used by the sample floors (S2) and by P9a Step 4 — last sentence of this bullet) [C1-F7]. Form F: [β(η, A) − b] log n,
  β(η, A) = ½ − η/2 − √(2Aη) (`lemmas/L1_sandF_b.md` Step 2(b); LC1-A confirmed that the bound on log k̃ is the only
  use of |Q| in the sandwich). Form R: (ε*/2) log n with ε* = (1 − 2b − 30ρ)/2 (`lemmas/L4_sandR_b.md` §6(b)). The size
  ladder improves with |Q|; truth inclusion needs feasibility only; the toolkit and the lattice lemmas need
  q log n/n → 0 (any b < 1); under Gaussian rows the sample floors on Q ∪ {l} need q√(log n/n) → 0
  (`lemmas/L5_formR.md` (S2)) and the sample/population comparison (q + log n)/√n → 0 (P9a Step 4) [SW1-6].
* **Reading.** With a start mode of size k ≈ n^b, deleting an outside column gains log(p/k) + ½ log n in prior and
  determinant and loses at most about log p in fit (the best of p noise columns): the margin vanishes at k ≈ √n. This
  is the budget of the argument, not a boundary theorem.
* **Observed (B1).** b = 0.5, 0.625, 0.75: LS0 ended at S₀ in 48/48 runs, although an outside column sat in the start
  mode in 5/12 runs and path-level no-addition failed in up to 4/6 (n = 1600); at most 4 non-deletion moves per run.
* **Open (O1).** The conclusion for b ≥ ½ (and with no lattice condition): needs path-level control of LS0 with cap
  accounting. Status of the assumption: ARTEFACT of the route (sufficient budget; necessity open).

## 2. The leak level

* **Form F.** As in W3-RM: (L-gain) with η < η_A, now coupled to b through b < β(η, A). **Observed (B4):** near the
  frontier (η ≤ 0.2) outside columns enter the start mode and LS0 deletes them (32/32); at nominal η = 1, n = 1600,
  the LS0 probe stopped at its shipped move cap before S₀ in 4 of 6 runs (start sizes 522–743; 19, 24, 35, 73 swaps
  against cap slack 15), 10/10 fine at n = 400. So far outside the condition the cap is an obstruction for the LS0
  probe; no asymptotic failure follows (limits remark of the statement).
* **Form R [P3].** (L-gain-R) with ϖ_n = o(√(log n/n)): **proved sufficient** (`lemmas/L4_sandR_b.md`; the parent had
  C_Ln^{−1/2}). The leak enters as a mean shift of norm ≤ C√n ϖ_n in the spherical tail; its cost is
  exp(C√(n log n) ϖ_n) = n^{o(1)}. **Open (O3′):** a leak at the exact scale κ√(log n/n): the same proof gives a
  frontier "15ρ + b + C(κ) < ½" with a non-sharp C(κ); the Gaussian-row analogue of β(η, A) is not derived.

## 3. The localisation clause (Form R)

* **Proved [T6].** (L-loc-R) is needed only with r_n → 0, no rate (the parent needed r_n(n log n)^{1/4} → 0, W2-LOC2's
  polynomial class a reference radius n^ρ with ρ > 1/(4α)). Mechanism: the selection-removal cross term
  c_lᵀS_VV⁻¹c_y is *equal* to the difference of the leak covariances at U₀ and at U (`lemmas/L4_sandR_b.md` (★)), so it
  is small because the leak bound holds at every conditioning set — the same quantifier as Form F's (L-gain) — and
  the localisation covariances only have to make the sample error r_nh_n of that term negligible.
* **What remains of it.** The count n^{15ρ} of reference sets (budget 15ρ + b < ½). With decaying correlations
  |H_l| = n^{o(1)} and the budget is b < ½, as in Form F at η = 0.
* **Open.** Whether any localisation is needed for the conclusion. In this proof, without r_n → 0 the sample error of
  the cross term is of the order h_n of the statistic itself and the reduction to deterministic reference sets
  fails. The exponent 15 (the conditioning size) and hence "15ρ": artefact of counting reference sets.

## 4. The lattice width condition (W) / (W-R)

* **Proved** (`lemmas/L2_width.md`). 𝔴⁰_n → −∞ ⇒ whole-lattice no-addition with probability ≥ 1 − exp(−(𝔴⁰_n)²/8) − o(1)
  ((C3)(a)); 𝔴⁰_n → +∞ ⇒ whole-lattice no-addition has probability → 0 ((C3)(b)). So for the event the route uses, the
  condition is sufficient when the gap diverges negatively and obstructed when it diverges positively; **a bounded
  gap is undetermined**. Neither statement is about the reported model.
* **Sufficient forms and their reach.** (W-χ) (|Q ∖ S₀| ≤ (1 − δ₁) log n: the parent's (N-χ)); (W-ref) (frames + ℓ¹
  atoms + ℓ² remainder, h + b < ½); (W-loc) (local regressions); in Form R (D-R^b), (D-loc^b). Verified instances at
  polynomial |Q|: polynomial decay α > 2 (both forms), one truth with n^b weak proxies (every b < ½), one
  equicorrelated group (b < 3/10, by a direct bound) — `lemmas/L6_examples.md`.
* **Observed (B2).** In the nominal width-stress design B2 (heuristic: (W) is not certified to fail on it, and its
  leak is small but not exactly zero [SW1-2]) an improving addition was found at a probed
  lattice set in 6/6 runs (b = 0.5, n = 1600) and never along the path; the LS0 probe ended at S₀ in 48/48. Finite-n
  LS0 success despite observed NA violations — not a proof that (W) is unnecessary for asymptotic reporting.
* **Open.** (O5) the bounded-gap regime; (O1) the theorem without any lattice condition; (O4′) the equicorrelated
  group for 3/10 ≤ b < ½: the direct bound (5.1) of L6 is crude. The check LC2-C (`reviews/LC2C_L6_check_opus.md`,
  finding 1) sketches that a size-by-size comparison gives (W) for b < 3/8 and that the width gap is positive for
  b > 3/8 — if so, for 3/8 < b < ½ the whole-lattice route fails on this design by (C3)(b) while nothing suggests the
  conclusion does: a concrete instance for O1. Both halves are sketches, not proved;
  (W) is not derived from (V), (L) and the floors.

## 5. The signal floor (BM-W)

* **Proved.** nθ*²_min ≫ d_n² + log n suffices for truth removal on the lattice, through the exact two-square
  identity (4.1) of `lemmas/L2_width.md`; (BM-Q) ⇒ (BM-W) (d_n² ≤ 2(|Q| + 1) + 4 log(2p)); when d_n² = O(log n) it is BM-∞,
  already in Theorem 1's conditions. In Form R signals are fixed and (BM-W) is automatic for b < 1.
* **Observed (B3).** A weak truth is missing from the start mode in 32/32 runs and LS0 adds it: no information on
  the floor itself. **Open:** necessity not studied; θ*_min → 0 in Form R is a non-claim.

## 6. The polynomial-decay cutoff in the examples

α > 2 in both forms. The leak and size budgets need only α > 1 (b ≥ 1/(2α), b < ½); α > 2 is what the available
inverse-decay bound (W2-LOC2:Lemma-IR, summable regression tails) needs for (W-loc)/(D-loc^b). **Open (O6):**
α ∈ (1, 2] (a Jaffard-type inverse-decay bound would be the tool; not attempted). The older cutoff α > 17/2
(W2-LOC2:Thm-Poly) came from the reference radius n^ρ, ρ > 1/(4α), that the norm bound on the cross term required;
§3 removes that requirement.

## 7. Open items (names used in REPORT.md)

| id | item | kind |
|---|---|---|
| O1 | the reported model with no lattice condition and for b ≥ ½: path-level control of LS0, with cap accounting (input: the η = 1 probes; f19's remark that a Gram floor gives an improving deletion at every lattice set) | separate ticket (hard) |
| O2 | counting (leak-profile) form of (L), with RM-0 on a down-closed sub-lattice (rider T2(c)) | deferred |
| O3′ | Form R leak at the exact scale κ√(log n/n): a non-sharp frontier b + 15ρ + Dκ < ½ is sketched (`reviews/BT2_better_theorem_astra.md` P6); the sharp one is open | open, moderate |
| O4′ | equicorrelated group, 3/10 ≤ b < ½ (threshold of (W) at b = 3/8 sketched independently by two reviewers: LC2-C finding 1, BT2 P7) | open, cheap to settle |
| O5 | bounded width gap | open |
| O6 | polynomial decay α ∈ (1, 2] | open, needs a sharper inverse-decay lemma |

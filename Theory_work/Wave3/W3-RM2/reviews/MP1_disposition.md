# MP1 disposition (lead) — independent mid-point review by Codex gpt-6-astra (high), blind first read

Review: `MP1_midpoint_astra.md`, manifest 960c9069b362a251403f6aed9cd804c96870fd63775a72ebf307588b45a10730 (quoted;
the reviewer verified all 52 file hashes). The texts it read are kept in `as_reviewed_by_MP1/` (ASSUMPTION_MAP,
PLAN, L0–L3; their sha256 are the rows of `MANIFEST_MP1.txt`). The prover's family is Claude; the reviewer is OpenAI.

Verdict: **CONTINUE WITH CHANGES.** "The key lemma stands. I found no FATAL or MAJOR mathematical gap in L0–L3 or
in (C1), read with its explicitly conditional posterior input in STATEMENT §5. … The required changes below correct
supporting records; they do not require strengthening (C1)'s assumptions or changing L2's argument."

## Findings and actions (all accepted; markers [MP1-#])

| # | class | finding | action |
|---|---|---|---|
| 1 | MINOR | ASSUMPTION_MAP row A:FL-Q: "holds for Gaussian rows iff b < ½-type" is false as a necessity assertion (iid Gaussian columns keep their floors for b < 1) | replaced by the reviewer's text: "supplied here by the sufficient entrywise bound q√(log n/n) → 0 (in particular b < ½); necessity is not asserted" [MP1-1] |
| 2 | MINOR | PLAN §1 (two table rows), PLAN §4, ASSUMPTION_MAP row A:W and row B2: "survives iff", "exact complexity condition", "route cannot do with less", unqualified "Not necessary for the conclusion" exceed what is proved | β(η, A) − b described as the positive margin of this proof; (W) as a sufficient negative-gap condition with a positive-gap obstruction (W-conv) and an unresolved bounded-gap regime; B2 as finite-n LS0 success despite observed NA violations, not a proof that (W) is unnecessary for asymptotic reporting [MP1-2] |
| 3 | MINOR | ASSUMPTION_MAP numerics record stale (207/204, 3 of 5, "n ≤ 3200"); "Inside every assumption" stronger than the nominal classification | counts updated to 208 runs / 204, the η = 1, n = 1600 cell to 4 failures of 6 with swaps 19, 24, 35, 73; completed sizes 400 and 1600 (no n = 3200 run); "Nominal baseline cells (B1 at b ≤ 0.375)"; LS0-probe scope stated [MP1-3] |
| 4 | NIT | L3 [POST] bullet: "bounded convergence" imprecise for convergence in probability | replaced by the explicit bound E[1 − π(S₀)] ≤ ε + P(1 − π(S₀) > ε), n → ∞ then ε → 0 [MP1-4]; no stronger posterior input |

Other hunks made with these (record only): in ASSUMPTION_MAP row B3 the stale v1.2 name "A:BM-Q" reads "A:BM-W" /
"the signal floor" (v1.3 naming); the status headers of L0–L3 now cite the lemma checks LC1-A/LC1-B and MP1 (they
were left neutral for the blind mid-point read); L3's line endings were normalised to those of the reviewed copy.
STATEMENT.md, L0–L2 bodies, numerics and INPUTS are unchanged by this round. **No hypothesis, claim, bridge
statement, proof step other than the wording of [MP1-4], constant or code pin changes.** Per PROTOCOL rule 15 the
diff is attested by an independent Sol reviewer (RC4).

## What the reviewer verified independently (its own derivations)
Toolkit at actual lattice cardinalities, including the size-(K + 1) auxiliary additions and the absence of a hidden
O(q) remainder; NA-conv with the exact cancellation (−½); NA-W: the 1-Lipschitz maximum, factor 1/8, s ≤ a_min, the
squaring step, c* = δ₀²/(32(2A + 2)); W-conv (a converse for no-addition, not for reporting); all five sufficient
forms with constants; truth removal — identity (4.1), the sign of θ_i, the role of 𝒵⁺_n and the cap endpoint
|T| = K; the sandwich ("every maximiser", common event); the import of RM-0 at arbitrary q, the pinned LS0 scan and
cap; [POST] and the pathwise reporting argument; n₀ dependences; containment of RM-F.

## Recorded for later legs (not findings)
* **A fixed-design witness at polynomial size** (reviewer's construction): p = ⌊n/3⌋, s₀ = 1, q = ⌊n^b⌋, 0 < b < ½,
  proxies x_j = √(n − 1)(r_n e₁ + √(1 − r_n²) e_j) with r_n² = C log n/n, orthogonal outside columns, Q = {1, …, q}:
  η = 0, (W-loc) with N_l = {1}, L = 0, (BM-Q). A genuine polynomial family of weak signal proxies, so (W) is not
  vacuous at polynomial |Q|. **Candidate for the examples table (C5); to be verified at the examples stage** — the
  reviewer's check is a sketch, and it does not replace the p ≫ n examples (Form R).
* **Form R obligations named by the reviewer** (adopted as the checklist for L4–L6):
  (P7, highest risk) an X-measurable selected block must not be treated as fixed under the spherical tail —
  selection removal uniformly over all small conditioning sets through the deterministic H_l references; count
  n^{15ρ}; the full t-range of the spherical bound; the localisation remainder
  √(n log n) r_n² + (log n)^{3/2}/√n + n r_n⁴ + (log n)²/n = o(1) (r_n(n log n)^{1/4} → 0 suffices); ladder 15ρ < ½,
  junk exclusion 15ρ + b < ½; response standardisation uniform in the coefficient box; citing the polylog theorem
  does not discharge it.
  (P8) routine with deterministic envelopes. (P9) the passage from a joint crossing bound to the conditional mean
  must be written: Markov on the conditional failure probability, then concentration / median–mean for the
  conditional 1-Lipschitz maximum, with the deterministic slack of order √(log n). (P10) keep the conditional status
  of the posterior input and the p = 1 endpoint.
* Not checked by MP1 (its own list): C2, C5, C6 (not written); SOP:TH09 and E4 (consumed, not re-proved); production
  score code / start-mode DP beyond the LS0 pins; re-execution of the numerics; literature priority.

## Status after this round
Form F key lemma: attempt 1 of 3, **not failed**; checked line by line by LC1-A/LC1-B (Sol, blind) and judged
independently by MP1 (Astra, blind): stands. Statuses in the lemma files stay "PROVED (by this seat, unchecked)"
with the review record; no PROVED-CHECKED label before the sweep and the council (CP3).

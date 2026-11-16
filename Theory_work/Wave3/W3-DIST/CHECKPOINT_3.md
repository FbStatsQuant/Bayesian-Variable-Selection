# W3-DIST — CHECKPOINT 3 (council passed in the diff round; for the SMC - Theory Department manager and HQ)

Lead: Claude Fable 5.2 (Claude Third, effort high). Written 2026-11-16 05:19 CT. Ticket folder
`Theory_work/Wave3/W3-DIST/`. Passing manifest: **MANIFEST c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc**
(`reviews/MANIFEST_R2.txt`; STATEMENT v1.4.10). Nothing in that manifest has been edited since the freeze.

## 1. Outcome
**The council passed in the diff round R2.** Both seats: all six gates PASS, all 20 claims ACCEPT, no C, S or F finding.

```
COUNCIL-VERDICT round=R2 manifest=c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc seat=astra score=9.3 gates=PASS
COUNCIL-VERDICT round=R2 manifest=c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc seat=opus score=9.2 gates=PASS
```
`manifest.py verify`: OK. `manifest.py bind`: OK. Council cell for the registry:
`R2; MANIFEST c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc; astra=9.3 PASS(reviews/R2_council_astra.md); opus=9.2 PASS(reviews/R2_council_opus.md)`.

Round R1 (blind, MANIFEST c7d74e49…) was not a pass: astra 7.9 and opus 8.6, each with gates=FAIL on one finding of its
own, and no correctness finding from either. R1-astra-01 (F): the statuses of Lemmas S, X, X′ lacked "conditional on
SOP:TH09". R1-opus-01 (S): a gloss on the rate in DIST-1 (c) let A vary. Both were repaired, checked by Sol (D5, D6) and
confirmed resolved by both seats in R2. Cap used: R1 and one diff round; no full re-round.

## 2. What is proved (the goal: a Song–Liang (2015) Theorems 1–2 analog for the coded method)
- **Theorem A (reader version, TC9).** Under (A1) a Gaussian linear model with any noise level, (A2) at most s nonzero
  coefficients and 2 ≤ p ≤ n^A, (A3) sub-Gaussian predictors on sparse directions, (A4) no near-exact collinearity
  (smallest eigenvalue of the correlation of at most q_n predictors at least c_ψ/n), (A5) bounded signal, and for every
  M₀ ≤ M ≤ √n/log n: on one data event of probability at least 1 − n^{−cM}, the exact coded posterior, prior as coded,
  puts mass at most n^{−cM} outside the Hellinger ball of radius √(M log n/n) around the true joint law of (x, y), and
  at most n^{−cM} on models larger than s + C₁M. Without (A4): the same with one more logarithm in the radius.
- **Master theorems.** DIST-1 (display (1.1): exponential form, radius C√(t/n), for M₀ log n ≤ t ≤ n^{1−κ₀}), DIST-2 (no
  non-degeneracy interface, radius C√(tℓ_n/n)), DIST-3 (oracle bound with an additive selection error, parametric
  rate).
- **What the sampler returns.** DIST-C (domination transfer to any law built from the output; the returned list) and
  Corollary C (the list of at most 40r + 1 models of a completed run).
- **Companions.** Theorem B (parametric rate under a fixed eigenvalue floor and beta-min b_n > 0); Lemmas H, T, S, V,
  X, X′, P6; bridges B0, B1, B2-core, B2, B3; Proposition NEC.

## 3. Target clauses
- **TC1–TC9: each proved as fixed at CP1.** The sweep and both council seats say so claim by claim.
- **No WEAKER change to a target clause.** Two tags next to target clauses were each confirmed EQUAL by reviewers:
  - **TC3** (rate constant): first after the L6-01 constant repair (D1), then after R1-opus-01 (D5 and both R2 seats, by
    name): TC3's text is unchanged and proved as written, with M₀ ≤ 16 + 4(1 + s₀^r)(A + 1) + 3(M + M′)/(2σ*²) and a radius
    constant free of the sparsity.
  - **TC8** (DIST-C): the event of the predictive sentence written out (D3), and its display for the DIST-2 reading
    (D4).
- **Proposition NEC touches no target clause.** It is a fixed-design, in-sample example whose design violates the
  non-degeneracy interface (ND). It shows that Lemma X's conclusion fails without (ND); Lemma X, display (1.1), DIST-2
  and TC1–TC9 are untouched. It says nothing about a random-design statement or about the in-probability form.

## 4. Changes of strength to report (changelog at the foot of STATEMENT)
- **WEAKER, non-target** (all confirmed by reviewers):
  - Theorem B gains b_n > 0 (companion; the statement was false without it);
  - bridge remarks: B0's domain, B3's b_n > 0, the capped window in B2 and B3, the range M ≤ √n/log n of the last bridge
    bullet;
  - Remark (1) of the reader section needs the window at the level of its radius;
  - the gloss on the rate in DIST-1 (c): A is now held fixed and log p_raw became log n ("for fixed (A, σ*², M, M′), ε_n²
    is of order (1 + s₀^r) log n/n"). HQ's reading: not a WEAKER change to a headline clause.
- **STRONGER since CP1, with HQ's go of 2026-11-16:** Corollary C's conclusion that a true model scored by a completed
  run, with posterior probability above ½, is the model the method reports as most probable. Verified by D3, by the
  sweep and by both seats against the code.
- **STRONGER, non-target:** bridge B2's implication covers every m with min{p, s₀ + m} ≤ q_n.

## 5. Premises not verified by a reviewer of this ticket (carried as conditions)
- **conditional on SOP:TH09** (its T01 part: the coded posterior is the contrast-model posterior, and the locked lemmas
  of [P1]): DIST-1, DIST-2, DIST-3, DIST-C, Theorem A, Theorem B, Corollary C, and Lemmas S, V, X, X′, NEC. The registry
  edges are `SOP:TH09@hyp`; `DEPS.tsv` names the exact [P1] items each proof uses.
- **conditional on W3-POST:Thm-1:** Theorem B, and the last sentence of bridge B3.
- **conditional on W3-SAMP:D, PC, LT#, C, TR** under their own premises: the delivery statements of DIST-C.
- **Exact arithmetic (EX-A):** DIST-C and Corollary C.
- Consumed as checked: W3-MISR:R′ (bridge B0). The frozen copy of its statement is the one with the Cor-H correction
  (sha256 84eb0f27…, commit 213e2115); W3-DIST does not use the corrected sentence.

## 6. Review trail (all in `reviews/`; REPORT §2 has the table)
- Blind reads S1 (Astra), S2 (Sol); line checks L1–L7 (Astra, Sol); break review BR1 (Astra, CP2): NOT BROKEN.
- Diff checks D1–D6 (Sol); sweep SW1 (Astra): 0 CRITICAL, 0 MAJOR, 9 MINOR, all repaired.
- Council R1 and diff round R2 (Astra seat, Opus 5.5 seat).
- One MAJOR finding in the proof leg: L6-01, the sparsity dependence of the rate constant, repaired by three constants
  with no change to the argument, and re-verified.
- `DEPS.tsv`: every row under a claim is OK (hash checked = hash frozen). Citation check: 0 MISS. Staged registry ingest
  of `REPORT.md` on main d2b600ba: 20 claims, 0 problems, acceptance PASS. HOLDS.md: empty throughout.

## 7. Open items and things HQ should know
- **Not re-checked by a separate diff check:** three record edits made after D4 (one sentence of TARGET §1, the pin
  record `PINS.md`, one sentence of REPORT §4), applied with the reviewer's own wording. Both councils read them.
- **ERRATA.md (E1–E8)**, editorial, for one later batch: stale line pins inside proof files (mapped in `PINS.md`), status
  quotes of W3-SAMP to refresh, four wording points, one numerics caption.
- **One erratum to add in that batch** (the passing manifest cannot be edited): the Opus seat's non-scoring note in R2,
  that DIST-2's "best rate ≍ (1 + s₀^r) log n·ℓ_n/n" does not track the sparsity factor (TC6 fixes no sparsity
  dependence; the theorem says its constants depend on s₀^r).
- **Stretch items.** S-FIT: the exponential fixed-design form is false without (ND) (Proposition NEC); the
  in-probability form and a random-design counterexample remain open. S-APX and S-EXP were not pursued. No kill budget
  was spent on a target.
- **Better-theorem proposals, not adopted** (statements stay as fixed at CP1): seven from the sweep, two from the Opus
  seat, and HQ's question on a constant independent of A. One page with gain and cost for each:
  `reviews/UNHARVESTED_STRENGTH.md`.
- **Internal note:** explicit constants, not optimised.

## 8. For HQ
CP3 acceptance (PROTOCOL_v4 §7), the H5 card for the headline status of DIST-1 / Theorem A (and Corollary C's
strengthened conclusion), the registry ingest of `REPORT.md` and the merge of `theory/W3-DIST` are HQ's. From my side the
ticket is complete; I made no git state change beyond pulls of main.

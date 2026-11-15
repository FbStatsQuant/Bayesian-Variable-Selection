# MP1 disposition (lead, 2026-11-11) — independent mid-point review `reviews/MP1_midpoint_astra.md`

Reviewer: Codex gpt-6-astra, reasoningEffort high, blind first read (brief `BRIEF_MP1_astra.md`). Manifest
`8e08c10991fbe4adfda0b7213dd089f54a223f0ae9edb47b5832f60a1d972fe7` quoted; `manifest.py bind` OK; `manifest.py verify`
OK on the current tree (nothing in the manifest was edited after the freeze).

**Verdict: CONTINUE.** Status given by the reviewer, per claim: (C0), (T0), [TK]/(B-TK), [LEAK]/(B-L), [VIS]/(B-V1),
[VIS]/(B-V2), (C1), (T1)(a), (T1)(b), (T1)(c), (T1)(d) — each "proved as stated". No CRITICAL or MAJOR finding.

| # | class | finding | lead's disposition (HQ decides at CP2; the statement is LOCKED and is not edited before HQ's go) |
|---|---|---|---|
| 1 | MINOR | (N2) of (T4) is vacuous when s₀ ≤ 15: its quantifier includes V = S₀, where δ_{S₀,l} = 0 for every null. The implication is true but gives no partition-free sharpness example in that regime; the working statement is the component diagnostic (C2)(i) | **ACCEPT.** Checked by the lead: μ ∈ span X_{S₀}, so (I − P_{S₀})μ = 0 and δ_{S₀,l} = 0. Proposed edit for STATEMENT v1.3.1: record the vacuity under (N2); attribute the one-column failure threshold to (C2)(i) (actual partition); make the F4 comparison and §0 (iv) refer to (C2)(i), with (N2) as its partition-free form for s₀ ≥ 16. V = S₀ is not deleted from (N2) (a null can share a block with all truths, where it is harmless). This narrows what the headline may say about necessity of the leakage level; it does not touch (T1) |
| 2 | MINOR | the bridge table abbreviates the inputs of (B-L), (B-V1), (B-V2) as [TK], while their proofs use the quantitative toolkit of L2 (events and uniform constants) | **ACCEPT.** Proposed edit for v1.3.1: one sentence in §4 saying that (B-L)/(B-V) use the quantitative form of [TK] delivered by Lemma TK under (E), (GF-16), and that (C1) needs only the qualitative interfaces. No hypothesis changes |

Reviewer's notes for the second half, taken into the plan:
* (B-R) is the main technical risk; localise to U ∩ H_l before taking maxima; condition on the columns of U₀ ∪ S₀ only
  (not on a sample-covariance event) so that the innovation stays spherical; a bound on the largest partial
  correlation is not a bound on the averaged functional — an integration/truncation step is needed.
* (T3)(b), clause C_L = 0: an expectation bound gives O_P at the rate (log n)^{15κ_Q+1/2}, not a fixed-constant bound with
  probability → 1; either prove the stronger form or state the bridge as a tightness statement.
* (N2), (N3): use (f1) from below for (N2) (no linearisation from above), (f3) for (N3); one Gaussian per witness.
* OVL: plausibly short (bounded number of columns, noise level √(log log n)).
* Optional: (AGG-a) holds in the stronger form 1 − 1/F (already in L1.2); not adopted as a statement change.

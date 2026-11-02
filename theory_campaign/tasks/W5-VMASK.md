# W5-VMASK: Adversarial verification of the masked-regime instance of T38 (W3-PXN and W4-T38FULL's new lemmas)

**Paper role:** Thm 5(b1), (b1-LH), (b1-LH-iid): the only masked-regime consistency instance with every premise
proved. Today it rests on two single runs with same-family checks only.

Fetch and read: `origin/theory/W3-PXN` (`theory_campaign/W3-PXN/`: REPORT, PROOF §§0–14, scripts, results),
`origin/theory/W4-T38FULL` (`T38_STATEMENT.md`, `T38_PROOF.md` §§1–3, `scripts/`), and the inputs they cite:
`origin/theory/W1-EXP` (PROOF §§1, 4: Lemmas 1.1–1.4, 4.1–4.2, Thms 5–6), `origin/theory/W3-VEXP` (REPAIRS R3),
`origin/theory/W1-T37R` (PROOF: Lemma 2(a), Theorem A(A3) lattice form), `origin/theory/W1-T38E` (PROOF: E1(a)(b),
E3). Also `Docs/Theory/theorems/00_COMMON.md`, `Docs/Methodology/METHODOLOGY_v3.md` §§6.3, 6.10, and
`Scripts/SMC_BVS/core/cpp/v3_blocks.h`, `v3_engine.h::local_search`.

You are an **independent referee**. Try to break the claims. For each step record VERIFIED, GAP (fixable or not) or
ERROR (with a counterexample). Claims to check, in this order:
1. **W3-PXN Lemma B** (exact Beta laws of the start statistics at the reference S°, independent of y, through the
   conditional-independence identities F1–F3 and the Grassmannian step after standardisation) and **Lemma Tr** (the
   truncated moment E[(1−X)^{−ν}1{X ≤ τ}] bound). These two carry the 2^B-free rate 1 − π₀(S°) = O_P(√(log n/n)) at
   p ≫ n. Check that W1-EXP Lemmas 1.1, 1.2, 1.4 really never use block membership (PXN uses them for arbitrary sets
   of size ≤ s₀ + 2).
2. **W3-PXN P1** (partition = groups w.p. → 1 under the cited correlation concentration; the R13 tie rule; the
   margin condition used when p > 4300), **P3**, **P4** (limit law), **P5**, **P6** (the TD′ lattice condition at
   S° from the component decomposition Lemma Λ and the margin table §9.3; the (L) margin and its failure probability
   (s₀+1)/√(2π(n+1)t_n)), **P7** (D2-a,b,c proved; D2-d NB is a sketch: say exactly what is missing), **P8** (the
   design de-randomisation lemma for T03).
3. **W4-T38FULL Lemma LS-score** (scoring without certification; the scan-before-limit engine fact; the emitted
   centre), **Lemma M** (uniform score comparison under a population margin m_n ≥ M_n√(log n/n): the χ²/Gaussian
   union over all sets of size ≤ k + s₀, the RSS floor through span(A ∪ S₀), the deterministic E1 bounds), **Theorem
   b1** ((M1)–(M3) + OP-LS0 ⇒ D_n → 0), **Proposition LH-LAT** (unit additivity of Δ on LH; the neighbour case list;
   the explicit sharp margin m₀; the referee's remark that only |ψ| < 1 is needed for the algebra).
4. Consistency between the two runs: PXN's P6 (lattice condition via its own margins) and T38FULL's LH-LAT (margins
   via unit additivity) must agree on LH exact Gram. Compute both margins on the same parameter grid and report
   any discrepancy.
5. Reproduce independently, with your own scorer and your own port of the partition (do not import their code):
   the LH-iid table at n ∈ {200, 400, 800} (config A and B), the LH exact-Gram LS0 check (G = 12, g = 9), the
   KS tests of Lemma B, and the (L)-failure rate. Add one adversarial design: |ψ| close to ρ, and a null group with
   within-group correlation above ρ, to probe P1 and the (M1) margin.
6. Method faithfulness: LS0 as modelled (centre emitted, tie rule for argmax π₀, cost) versus `local_search`; the
   start mode by max-plus convolution versus `v3_start.h`.

Deliverable: `theory_campaign/W5-VMASK/REPORT.md` with the verdict table (claim | verdict | evidence), complete
repairs of fixable GAPs in `REPAIRS.md`, your scripts and outputs, and the confidence card. State plainly whether
Thm 5(b1-LH-iid) can be cited as PROVED (pending cross-family review) or must stay a single-run claim.

---

_Source: theory_campaign/F-REFINE/NEXT_TASKS.md on branch theory/F-REFINE (Fable, 2026-11-02). Read F-REFINE's CARDS.md and ARCHITECTURE.md first: `git fetch origin theory/F-REFINE`._

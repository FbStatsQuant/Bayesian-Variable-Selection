# W4-SHARE: Delivery to the terminal rounds (route b2): prove SHARE or LT, or find the right hypothesis

W1-T38E (branch `theory/W1-T38E`) and its referee W3-VT38E established three things about route (b2), Gibbs-path repair via the restated T24 (Theorem B, branch `theory/W1-T24G`, checked by W2-VT24G):
- route (b2) needs a near-truth particle to *survive to the terminal rounds*;
- **counterexample C1** (confirmed with a reversible kernel) shows that start mass, bridge mass and zero exits do not suffice: every particle in A goes extinct in 56–100% of islands;
- the route needs a particle-level hypothesis, **SHARE** (Prop. D3) or the evidence lower tail **LT** (Thm D1), and these fail exactly in the masked, late-crossing case.

**Goal:**
1. Characterise when near-truth particles survive the tempering bridge with resampling. Use the actual ESS/resampling rule and move kernels of `Docs/Methodology/METHODOLOGY_v3.md` and `Scripts/SMC_BVS/core/cpp/`. Find a checkable sufficient condition that implies SHARE or LT, for example on how quickly π_φ(𝓡_d) rises along the bridge relative to the ESS-driven φ-grid, or on within-𝓡_d mixing.
2. Prove it, or give a sharp counterexample showing that no condition of the form you consider can work.
3. Using the restricted ESS identity T13 and the occupancy lemma T15 (locked), turn the condition into a statement about the actual run, with N, the number of islands and the stage count explicit.
4. Check numerically with an exact or faithful small-p SMC simulation, written from the spec. W3-VT38E's validated scripts can be reused as a reference, but write your own core.
5. If route (b2) cannot be closed for the original method, say plainly what minimal change would close it, compared with LS0 (route b1) and T39 (repair tracks).

**Deliverable:** `theory_campaign/W4-SHARE/REPORT.md` with statements, proofs, numerics and the confidence card.

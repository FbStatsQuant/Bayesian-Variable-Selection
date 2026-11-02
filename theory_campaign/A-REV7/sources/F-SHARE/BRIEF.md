# BRIEF — F-SHARE (task prompt, saved at run start 2026-11-02 ~18:50 UTC)

Research sub-agent F-SHARE (Fable 5.1) of the SMC-BVS theory campaign. Worktree of FbStatsQuant/Bayesian-Variable-Selection based on theory/campaign; branch theory/F-SHARE; work only under theory_campaign/F-SHARE/.

Owls rule: any numerical computation through `~/.config/bvs-hq/owls/owls_run -j 2 -- <cmd>`; keep computations small (exact small-p, seconds to minutes); one compute job at a time.

Context. Paper story: SMC-BVS v3's reported HPM (best model ever scored) is consistent because the truth gets SCORED. In T38's masked regime the truth has vanishing start mass but the near-truth region R_d has large start mass. A near-truth particle must be DELIVERED and then REPAIRED.
- Repair via Gibbs moves is proved (Theorem B, theory/W1-T24G; verified with repairs on theory/W2-VT24G; premises discharged further on theory/W2-PREM).
- theory/W3-PXN proved a p >> n family (LH-iid) on which T38(b) holds via LS0.
- The open crux is delivery to the terminal rounds (route b2) for the method WITHOUT LS0. W1-T38E (verified by W3-VT38E) proved the composition and showed with counterexample C1 (confirmed with a reversible kernel) that start mass, bridge mass and zero exits do NOT prevent extinction of all near-truth particles through ESS-driven reweighting and resampling. Route b2 needs a particle-level hypothesis, SHARE (Prop D3) or the evidence lower tail LT (Thm D1).
- An Opus cloud run, theory/W4-SHARE, attacks the same problem in parallel. Work independently, then compare near the end.

Read: branches theory/W1-T38E, W3-VT38E, W1-T24G, W2-VT24G, W2-PREM, W3-PXN, W1-EXP; Docs/Methodology/METHODOLOGY_v3.md; Scripts/SMC_BVS/core/cpp/; locked T13 and T15.

GOAL. Find the RIGHT delivery theorem in the masked regime for the method as it is. Give a checkable condition under which near-truth particles survive the tempered bridge with resampling, and prove it. Directions: the rise of pi_phi(R_d) relative to the ESS-adaptive phi grid; within-R_d mixing; genealogical or branching arguments over the N particles; multi-island amplification; delivered at the terminal rounds only. If delivery fails under natural conditions, give the sharpest counterexample family and the minimal method change, compared with LS0 and T39.

DELIVERABLE: theory_campaign/F-SHARE/REPORT.md (headline, statements, PROOF.md, numerics, confidence card). Push it. Final message: 10-line summary with branch name and head SHA.

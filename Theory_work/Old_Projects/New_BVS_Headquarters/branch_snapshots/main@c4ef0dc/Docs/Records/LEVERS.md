# LEVERS — candidate changes for the SMC-BVS methodology campaign

Inputs to `campaign.md` cycles. Each lever needs the person's sign-off before it becomes a direction.

## From the DMDJ 2006 quick study (2026-10-20)

Source: `C:\Users\felip\OneDrive\Documents\Library\digests\DelMoral_Doucet_Jasra_2006\digest.pdf`, Section 8 (full change / rationale / effect / risk / test for each). Triage by one Fable lever review, adopted by the lead (`agent_notes\fable_levers\LEVER_REVIEW.md`).

| ID | Lever | Campaign | Reason |
|---|---|---|---|
| V4 | Compute allocation: ESS target 0.95N vs two Gibbs sweeps per stage, matched runtime | yes | Config only; only lever raising move effort per unit φ |
| V5 | Path-sampling cross-check of log Zhat | yes | Free diagnostic; detects coarse spacing, not mode loss |
| V6 | Perfect-mixing reference SD for island spread of log Zhat (~0.025 at p=500) | yes | Free; separates spacing from mixing |
| V7 | Block refresh from start tables, independence-MH form | yes | One score, invariant, re-injects lost block sub-models |
| V8 | Flatten the start: block-table exponent α < 1 | yes | Only lever acting on start-induced mode loss |
| V9 | Genealogy diagnostic: distinct stage-1 ancestors and distinct models per stage/island | yes | Only mode-loss flag not based on ESS |
| V1b | Block Rao–Blackwellised weight + exact block Gibbs | later | Value is as the I.6 block-Gibbs move |
| V10 | Cross-block pair proposals | later | Own reasoning, not in DMDJ |
| V1 | Single-coordinate RB weight | no | Weight variance not binding |
| V2 | Backward kernel (25) for random-scan Gibbs | no | Cost for little gain on near-even weights |
| V3 | ESS-triggered resampling | no | Raises stage variance in our step order |

Open item for the master doc: I.4 relies on unbiasedness of Zhat; DMDJ never states it. A verified source is needed.

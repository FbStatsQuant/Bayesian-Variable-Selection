# WSL1 reply (Codex gpt-6.1-sol high, blind, delegate 639add55; 2026-11-17) — verbatim

**C — Consumer scope:** D and MR are supported at the pin with the potential pair (𝒜°, 𝓒°). Their literal actual-pair reading is not established; W2 correctly preserves this restriction.

**Part 1 — Statement lock**

- **W1: LOCK.** Covers the required control flow, stopping times, augmented-record measurability, and consumer coordinates.
- **W2: LOCK.** Covers general-calibration freezing and the stage/prefix extension, with the potential-pair restriction explicit.

**Part 2 — Line check**

- **W1: VERIFIED.** Uniform sites, adaptive read counts, stopping-time argument, κ_max, κ(c), and D_r(c) agree with the code. No additional input influencing transitions or weights was found.
- **W2: VERIFIED.** Stream isolation, measurable A_0, record identification, monotone-class proof, evidence bounds, and the consumer integrands check out under the stated assumptions.

Both the prescribed HEAD comparison and the working-tree comparison against core pin `4676af6` exited successfully.

1. **C — Preserve the potential-pair reading in consumers.** W3-SAMP/STATEMENT.md:39 defines the actual calibration-success event, while D_theorem.md:28 and MR_identities.md:64 invoke independence and freezing. Those uses are justified for (𝒜°, 𝓒°); they do not establish the corresponding actual-pair conditional identities. **Fix:** carry W2's explicit potential-pair convention into the consumer statements when discharging these edges, retaining T5's transfer restrictions. This restriction is already correctly stated in W2_FRZ/STATEMENT.md:41; no W1/W2 amendment is required.

No further S, F, or E findings.

WSL1-VERDICT: W1 lock=LOCK, check=VERIFIED; W2 lock=LOCK, check=VERIFIED

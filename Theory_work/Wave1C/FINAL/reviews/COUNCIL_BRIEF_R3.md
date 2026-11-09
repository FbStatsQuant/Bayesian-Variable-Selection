# Final council — consistency chapter (Wave 1C), round 3

You are a **fresh** council seat: you have not seen this chapter before. Do not read any round-1 council file
(`C1_council_*.md`, `C2_council_*.md`) before writing your own verdict; you MAY read `C1_disposition.md` and `C2_disposition.md` afterwards to check that the
round-1 findings were really fixed (report any that were not).

**Object.** `Theory_work/Wave1C/FINAL/consistency.tex` (+ `sections/*.tex`, compiled `consistency.pdf`, 25 pp,
"draft v3"), committed at COMMIT_PLACEHOLDER. Final product of Theory Waves 1 + 1C for the SMC-BVS paper.

**Sources it must match.** As in `COUNCIL_BRIEF.md` (same folder), plus: `Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md`,
`A2_propF_GROW.md`, `A3_check_A2.md`; and the engineering branch `origin/w1c/ls0-merge` (head 8a27652; read with
read-only `git show origin/w1c/ls0-merge:<path>`, e.g. `Theory_work/Wave1C/C-ENG/REPORT.md`,
`Scripts/SMC_BVS/core/cpp/v3_core.cpp`, `Scripts/SMC_BVS/core/v3_calib.R`).

**Three items were checked mathematically by both round-2 seats; check them again independently** — check each mathematically, in full:
1. **Lemma CAP** (§7.1) and its transfer list, against the LS0 rules and the branch code.
2. **Proposition F** (A1's corrected form, §6) — delivery P(no output) = 0 with the total tier-1 calibration fallback
   and the amended allocation; P(Ŝ⁺ = S₀) → 1 on LH, LH-iid, the W1-GEN class.
3. **Proposition F-GROW** (§6.3, A2 + A3 amendments) — the same on the C-GROW class (AR(1) exact Gram; AR(1) iid rows
   = study S2).

**Gates** G1–G6 exactly as defined in `COUNCIL_BRIEF.md`. Output: write only `FINAL/reviews/C3_council_<seat>.md`
(seat = sol or opus): gate verdicts; numbered findings (BLOCKING / MAJOR / MINOR / NIT, path:line evidence, exact
replacement text); then a final line `SCORE: x.x/10; GATES: G1 … G6` (uncapped). Pass = both seats ≥ 8.0, all gates
PASS, same round. No git commands that change state; do not edit the chapter; try to break it.

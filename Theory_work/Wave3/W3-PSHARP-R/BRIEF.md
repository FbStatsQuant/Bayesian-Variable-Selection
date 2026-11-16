# W3-PSHARP-R — T12: PSHARP Prop A in expectation for every p (Theory Department, 2026-11-15)

Lead: Claude Opus 5.5, effort high, Claude Third, on Owls. **Tier B**, NORMAL mode. Worktree
`/home/fb31/BVS-wt/W3-PSHARP-R`, branch `theory/W3-PSHARP-R`, folder `Theory_work/Wave3/W3-PSHARP-R/`.
Read first, in full: `RIDER_RULES.md` (this folder; binding), then `Theory_work/Wave3/PROTOCOL_v4.md`,
`Theory_work/Wave3/PROGRAM.md` (presentation rule + Readability).

## Parent (read-only)
`Theory_work/Wave3/W3-PSHARP/` v1.2.1 (recorded on main, 4 claims). Its pending editorial batch E1–E9
(`reviews/R2_disposition.md`) belongs to the editorial ticket, not to you; do not re-litigate it.
Motivation: `API_AUDIT/sharp2/TRIAGE.md` row W3-PSHARP:A and §2 row T12 (the triage reviewer re-derived the truncated
second-moment bound).

## Targets
1. **Prop A / Cor A1 in expectation, every p.** Truncate at T = ε/c_n (not W ≤ N) with Var ≤ c·T·E to get
   liminf E δ_n / [(s₀+1)√(log(p√n/(s₀+1))/(πn))] ≥ 1 for every N ≥ 1, fixed p included, with constant √((a+½)/π)
   in place of √(a/π) (`W3-PSHARP/lemmas/A_log_factor.md:15-25,64-68,119`). Correct the expectation readings at
   `W3-PSHARP/STATEMENT.md:84-88,109` in your delta ("no claim when log p = o(log n)" becomes in-probability only).
2. A2 with e^λ − 1 on (W-orth) (K01-P1 analogue), +1 h, if it stays a restatement.
Parked (named, no work): dropping G under (W-sph); a coherence witness.

Headline effect: PSHARP Cor A1 is a headline sharpness statement → `READER_DELTA.md` required; CHECKPOINT_1 in plain
words for HQ's H5 card. Needed **before the chapter v2.0 sharpness section** is assembled: speed matters.

## Budget and agents
~3–4 Opus hours. No helper needed (1 allowed, for numerics). Sol: lock, one line-check batch, council seat. One small
numerics check of the new constant (exact orthogonal case) is welcome. Kill budget 3.

## Start
`cd /home/fb31/BVS-wt/W3-PSHARP-R`, write `PLAN.md` and the delta `STATEMENT.md`, launch the Sol statement lock, then
`CHECKPOINT_1.md` and end your run.

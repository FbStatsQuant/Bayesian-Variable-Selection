# MEET-THM · Inherited-proof check (cross-family), brief

Chair, 2026-11-04. The check is independent of the Round 2 statements. It was moved forward from wave 2 because:
- HQ ruling Q1(c) (`evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`) needs it;
- every seat's rank-1 theorem (validity, Theorem V) rests on N9;
- the §5.3 package rests on OWS-WS3/WS4.

All of these are author-only and Claude-authored (O-WSTAB by Opus 5.5; N9-KERNEL by a Claude run). The checker is gpt-6.1-sol.

**Checker:** proof checker 1 (gpt-6.1-sol, Codex), a full line-by-line proof check. Working directory: `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/theory-MEET-THM`. Run `git fetch origin`.

## Items, in this order
1. **OWS-WS6(d)**, the noise-chasing obstruction under ORTH: `git show origin/theory/O-WSTAB:theory_campaign/O-WSTAB/PROOF.md` §6 (with §0–§2 for the definitions and WS1/WS2 it uses).
2. **OWS-WS7**, weights in the masked regime: the same file, §7.
3. **OWS-WS3** (block-orthogonal case) and **OWS-WS4** (perturbation in the standardised cross-block Gram): the same file, §3–§4.
4. **N9-KERNEL**, kernel reversibility, self-adjoint round and exact start sampler, against the code: `git show origin/theory/N9-KERNEL:theory_campaign/N9-KERNEL/PROOF.md` §0–§3 (and REPORT.md, CHECK.md). The code is `Scripts/SMC_BVS/core/cpp/` at the commit the proof names; v3.1 does not change the step functions.

Context:
- registry rows in `origin/theory/MEET-THM-REG:theory_campaign/MEET-THM/evidence/REGISTRY_INDEX.md` lines 402–423 (OWS-*) and §5.B B2 (N9);
- the method: `origin/theory/MEET-v31:theory_campaign/MEET-v31/METHOD_v3.1_FINAL.md`, with `AMENDMENT_HQ_01.md`.

## For each item
- **Verdict**, exactly one of:
  - `VERIFIED` (every step checked; no error);
  - `VERIFIED WITH AMENDMENT` (true after the stated, minimal correction);
  - `GAP` (name the step; say whether the statement is still believed true);
  - `ERROR` (the statement is false: give a counterexample, with a script).
- **Hypotheses:** list every one the proof actually uses, and flag any that is not a model/design condition.
- **Scope:** the exact scope the proof covers: ORTH / H-ORTH, ideal vs coded grid, growth conditions (p = n^A, null counts), asymptotic vs finite.
- **Numerical sanity check:** where cheap (Python, fixed seeds, ≤ 20 seeds, each < 5 min, local only).
- **For WS6(d) and WS7 specifically:** does the pair establish that the **one-shot** form of proposal §5.3 fails for the shipped method? The one-shot form reads: "the variance of importance weights from the block-product start π₀ to π stays bounded when cross-block dependence is weak". State precisely under which hypotheses it fails.

## Rules
- Never upgrade. Your verdicts are a cross-family check. Write "VERIFIED (PC1, cross-family, line by line)" only if you checked every line.
- Write only under `theory_campaign/MEET-THM/evidence/CHK_INHERITED/` (REPORT.md written progressively, scripts/). Do not commit or push.
- Tables per item, ≤ 60 words per cell, plus a per-step table for any GAP or ERROR.
- Your final message is the full REPORT.md content.

# W3-FAMC lead brief (owner GO via HQ, 2026-11-17 night; consultant Q1 (iii))

**Ticket:** W3-FAMC is a design-family corollary for core 3, the paper's Result 3 (Theorem 6 and its uses in Theorems 5 and 10). It states "core 3 holds for block correlation and for moderate AR correlation" as a corollary with *primitive* assumptions: the correlation structure, coefficients off Lemma VIS's bad set B (or sign-aligned), and the signal floors. These replace the visibility and leakage conditions for those two families.

**Scope:** no theorem changes; additive only; not a Lean target. The work list is otherwise closed (D107): add nothing beyond this corollary.

## Step 0: check whether this is already recorded. If it is, report and stop.
Search main's registry (`Theory_work/INFRA/registry/claims.tsv`) and these sources for an existing family-level corollary:
- W2-APP: `Theory_work/Wave2/W2-APP/STATEMENT.md` and `lemmas/L4_families.md`, especially the family map at about :165, "PTV automatic if ≤ 1 truth/block";
- the W3-RM2 examples: `Theory_work/Wave3/W3-RM2/` (Ex-Equi, Ex-PolyR/F, Ex-Proxy, ASSUMPTION_MAP.md);
- TRACK_B B9/B10: `Theory_work/Wave3/W3-AUDIT/TRACK_B.md` :237 and :263.

Report what exists, with registry ids and statuses, and what is missing.

## Route: assembly only, no new theory
- **Visibility:** use Lemma VIS (W3-AUDIT-V:VIS, PROVED-CHECKED; `Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/STATEMENT.md` :29-59, v1.5, and PROOF.md). For block designs, use one truth per block or (VIS-a) aligned signs. For AR designs, use (VIS-e) aligned signs, or ϑ ∉ B via (VIS-b). Note that adjacent mixed-sign AR truths (ρ = 0.5, θ = (1, −2)) lie on B; see `Theory_work/Dept/writing_answers/AR1_VIS_NOTE_2026-11-17.md` and TRACK_B B8:216.
- **Leakage and local regressions, block side:** use the TRACK_B B9 computation (leakage set = the block, zero leakage terms) and B10 (local regressions inside Q).
- **AR side:** use the RM2 decaying-correlation examples.
- **Kill rule for AR:** if the AR side needs a new lemma, drop the AR half. Prove only the block corollary, and present AR as "inside by the track C checks" (evidence, not a theorem).

## Standards
- **D106:** maximal quality, independently checked, paper- and Lean-ready wording.
- **D109:** every assumption must be class 1 (SL or a BVS-for-linear-regression precedent), class 2a (a proved artefact), or class 2b (reasonable in typical cases). State the class for each assumption.
- **Owner rule:** the statement must be true *and readable from the statement alone*. A reader must see the families, the coefficient condition and the floors without opening proofs.
- **Statuses:** quote every input's current status from main's registry. Use the expansion rule (D126) for conditions.

## Staffing and fuel
- **You:** an Opus lead on claudeAgent_personal at high, writing the statement and doing the assembly.
- **Helpers:** Sonnet subagents for mechanical parts only (pointer checks, citecheck, table building).
- **Not allowed:** no Fable. Every subagent must be explicitly on claudeAgent_personal; never Claude Third or Work.

## Process (PROTOCOL_v4; use W3-D3 as the folder template: STATEMENT.md, PLAN.md, TARGET.md, DEPS.tsv, citecheck, LOG.md, reviews/)
1. Work on branch `theory/W3-FAMC`, created from `origin/main` in your worktree, in folder `Theory_work/Wave3/W3-FAMC/`.
2. Run Step 0. **Send the manager the Step 0 result.** If it is already recorded, stop there.
3. Write **STATEMENT.md v1.0** (the corollary in readable form, with assumption classes) and **PLAN.md**. **Send the manager the STATEMENT draft before any review round.** HQ wants to see it.
4. **Tier B review, after the manager's release.**
   - **Line check:** one Sol line check on gpt-6.2-sol (provider codex, reasoningEffort high), with a model-id header.
   - **Diff round:** one diff round after you fix what it finds.
   - **Triage:** 6.2 verdicts are *input, never decisions*. Triage each point against the acceptance filter: genuine flaws only, no nitpicks, and probability-zero caveats do not block.
   - **Logging:** log each 6.2 review as one line in `Theory_work/Dept/SOL62_QUALITY.md` (send the line to the manager).
   - **Recording:** to be recordable, the review needs two distinct council seats bound to the same manifest (Sol plus an Opus seat that did not author the text).
   - **Labels:** round labels must be `R<digits>`.
5. Freeze the manifest with manifest.py v2: no registry files and no live logs. Run citecheck, then CHECKPOINT. The recorder then dry-runs; the real run happens on HQ's GO only.

## Budget
Budget is 1–2 lead-days. **KILL at 3 days.** Report to the manager at each step above, at most 10 lines each.

## Don'ts
- Never push to main.
- Never edit registry files.
- Never edit other tickets' files. Report needed changes elsewhere instead of making them.

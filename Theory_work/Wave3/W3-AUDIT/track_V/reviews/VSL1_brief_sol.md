# VSL1 brief — statement lock + line check of track-V item V1 (Lemma VIS) (Codex gpt-6.1-sol, high)

The gate read (PROTOCOL_v4 §2, Tier B, NORMAL: Sol lock + Sol line check in one read; key lemma). **Blind first read:**
read only the files below. Do not open any LOG, CHECKPOINT, INDEX, CHECK or `reviews/` file. Read only; write no files;
change no git state; start no subagents.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT` (branch `theory/W3-AUDIT`).
- Item: `Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/{STATEMENT,PROOF}.md` (v1.1).
- Context (what the lemma is for): `git -C /home/fb31/BVS-wt/W3-AUDIT show origin/main:Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
  lines 565-600 (Theorem 5), 660-700 (Theorem 6), 1282-1295 (Theorem 10); `git ... show origin/main:Theory_work/Wave3/W3-READER/NOTATION.md`
  lines 155-175; `Theory_work/Wave3/W3-AUDIT/TRACK_B.md:209-233` (dossier B8); `Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md:60-70`.

Binding requirement (owner + consultant): a lower bound a > 0 on |Cov(W_j, Wᵀθ* | W_U)| that is **uniform in n** and over
all U with |U| ≤ 15, for designs with finitely (or countably) many local patterns (block designs with finitely many block
structures; AR(ρ) with fixed ρ; stationary/banded), for θ under a stated sign condition or in a stated open set — **not**
merely "nonzero for almost every θ" (which does not survive p → ∞).

**Part 1 — statement lock.** Does the lemma meet the requirement (is B independent of n; is "δ > 0" the right uniform
condition; is the good set open and generic; is the sign route's constant explicit)? Faithful to the theorems' visibility
hypotheses and partial-covariance notation? Every hypothesis explicit (floors, positive definiteness, n ≥ n₀)? No clause
stronger than proved? Verdict: LOCK / LOCK WITH CHANGES (list) / DO NOT LOCK.
**Part 2 — line check.** Every step; try to break it with small explicit matrices: F1, F2 (Stieltjes inverse ≥ 0), (VIS-0),
(VIS-a) (components, signs), (VIS-b) (closedness, distance bound, attained minimum), (VIS-c), (VIS-d) (locality,
continuity, compactness, the one-point compactification), (VIS-e) (inverse formulas and floors, AR with ρ < 0).
Verdict: VERIFIED / VERIFIED WITH AMENDMENTS / NOT VERIFIED. If a clause is false, say so first and tag it **C**.

**Reply format** (plain markdown, as your final message): Part 1; Part 2; numbered findings tagged **C**, **S**, **F** or
**E** with file:line, what fails, and the fix. Last line: `VSL1-VERDICT: V1 lock=<…>, check=<…>`.

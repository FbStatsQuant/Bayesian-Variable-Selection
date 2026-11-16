# W3-T03ACC — council acceptance of T03♯ (SOP:TH09) on its existing proof (Theory Department, 2026-11-15; HQ-ordered)

Lead: Claude Opus 5.5, effort high, Claude Third, child agent of the Theory Department. **Tier B (re-check of an
existing proof; no new mathematics).** Worktree `/home/fb31/BVS-wt/W3-T03ACC`, branch `theory/W3-T03ACC`, folder
`Theory_work/Wave3/W3-T03ACC/`. Read first: `RIDER_RULES.md` (this folder; binding, except §1's "delta statement":
here the statement is T03♯ as recorded, restated verbatim with sources), `POLICIES.md`, `PROTOCOL_v4.md`, `PROGRAM.md`.

## Why
SOP:TH09 = T03♯ (posterior concentration 1 − π(S₀) = O_P(√(log n/n)), exact HPM/MPM consistency, large-signal inclusion
without beta-min; fixed design) is the root input of headline rows 1.1 (via W3-POST Thm-1 → W3-POST2 A1/C), 1.2
(W2-APP:POST) and 3.1 (RM2-R via POST). It has same-family (SF, W2-VT03R) and cross-family (XF, A-REV2) verifications
but **no council record**, so every consumer is recorded "conditional on SOP:TH09". Card condition (i): an abstract row
cannot rest on an unchecked conditional unless the abstract says so. Target: **CP3 by Thu 2026-11-19 18:00 CT**.

## The object
- Statement: registry `SOP:TH09` (`Theory_work/State_of_Project/registry/theory_main.tsv:68`, status verbatim
  "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2) …"); hypotheses R1 (fixed s₀, p ≤ n^A), G, R, SE_λ, SE_w, BM.
  Find the exact statement text in the State_of_Project sources (sections/*.tex, theorems/) and in the proof.
- Proof as written: `git show 7e14d6f:theory_campaign/W1-T03R/PROOF.md` (branch origin/theory/W1-T03R; REPORT.md, NOTES.md,
  scripts), which builds on the locked proofs **[P1]** `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex` and
  **[P3]** `Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex` (with STATEMENT.md, FINAL_REPORT.md, review/).
- Prior verifications (context for you, **not** inputs for the blind seats): SF `origin/theory/W2-VT03R` REPORT.md (b9f6d9b),
  XF `origin/theory/A-REV2` REVIEW.md (and the snapshots under Theory_work/Old_Projects/.../branch_snapshots/{W2-VT03R,A-REV2}/).
Copy the needed source files into `sources/` (with their commit ids in `sources/PINS.md`) so the manifest can freeze them.

## Chain (Tier B, NORMAL)
1. `STATEMENT.md`: T03♯ restated verbatim from its sources, with every hypothesis defined and file:line; a consumes table
   (T01/T02 locked results it uses, their statuses verbatim). `PLAN.md`. **Sol statement lock** (fresh, blind): is the
   restatement faithful to the sources, and are all hypotheses explicit? → `CHECKPOINT_1.md` and end your run (manager answers).
2. Line checks of the proof **as written** (no new proof): split into 2–3 Sol batches (e.g. C1–C5, C6–C10 + assembly, the
   [P1]/[P3] steps it consumes). Any GAP → repair in a `lemmas/` copy with [R-#] marks, re-checked by a new Sol agent;
   a gap that needs a new argument = early checkpoint (Tier A) — tell the manager at once.
3. `DEPS.tsv` all OK → `REPORT.md` with the registry block (status source = this ticket) → citecheck 0 MISS.
4. Freeze `reviews/MANIFEST_R1.txt`; council R1 = **Astra seat** (OpenAI; HQ's choice for this acceptance) + **Opus seat**
   (Claude Third, Opus 5.5 high), fresh, blind, briefs per `Theory_work/INFRA/templates/COUNCIL_BRIEF.md` with per-claim
   tables, C/S/F/E tags, the sweep duties, and the "gates=FAIL on your own C/S/F" sentence. Diff round if needed.
5. `CHECKPOINT_3.md`: the passing round, bind output, staged ingest output. End. HQ accepts and records.

## Agents and limits
Sol / Astra on codex (high); Codex is congested until ~midday 11-16 (BNP push) — queue the lock now, line checks after.
Up to 2 helpers (Opus/Sonnet/Haiku 5.5, Claude Third). Never cancel agents; settle your own finished reviewers. Temp:
`/home/fb31/SMC_Theory_Department/tmp/<YYYYMMDD>-W3-T03ACC-<what>`. Timestamps from `date`. HQ runs a separate blind API
Fable audit of the T03♯ proof (proof material / extra read only, not a review layer, v4 H3); the manager passes it to you.
If CP3 cannot make Thu 18:00, say so at the earliest checkpoint: row 1.1 then goes to the abstract with its condition stated.

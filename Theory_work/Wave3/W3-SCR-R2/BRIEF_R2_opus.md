# BRIEF_R2_opus — W3-SCR council round R2, Opus seat (Claude Opus 5.5, effort high, fresh)

Coordinator: W3-SCR-R2 (Theory Department). Written 2026-11-16 before launch. Targeted second round (HQ + consultant,
H5 card 7): the post-C1 v3.4 edits to W3-SCR were never re-scored, and headline row A1 (abstract, row 3.7) rests on them.

## Seat task (Opus)
You may read `Theory_work/Wave3/W3-SCR-R2/reviews/PC_SCR_sol.md`: an independent post-change (PC) read that found the
v3.4 A1 edit SUBSTANTIVE (adds fixed-in-n κ, b, M) but the current proof valid. Do not take its conclusions on trust.

**Task 1 — the SUBSTANTIVE hunks.** For each hunk PC_SCR_sol.md classes SUBSTANTIVE, CONFIRM or REJECT, on the current
text, that (a) the current text is correct and its proof complete with the hypotheses as now stated, and (b) every
statement / lemma / derived text that consumes it states the same hypotheses (no S or F mismatch):
- **A1**: STATEMENT.md:158–163 and its proof lemmas/L3_screening.md:65–76 (fixed κ, b, M, σ; c₁ = κ²b²/[200(M²+σ²)];
  the large-n step; the polynomial-p consequence), with the bridge chain L4 (L4.0, B2, B2d, B3), L1, L2, L3:6–35.
- **SCR-G**: STATEMENT.md:132–145 and lemmas/L7_master.md M2, M4, M5 (fixed κ, b, M, σ; c₂ = κ²b²/[104(M²+σ²)]).
- **M4**: lemmas/L7_master.md:97–109 (do the "for large n" steps need, and use only, the stated fixed parameters?).
- **M6 prose**: STATEMENT.md:120–129 and L7 M6 (is the corrected statement about b_𝓗 now true as written?).
- **ASSUMPTION_MAP construction**: ASSUMPTION_MAP.md:20 (is the two-truth κ² attainment construction feasible and the
  computation of Γ_n(0) correct?).
Also check whether the derived texts (REPORT.md A1 summary, ASSUMPTION_MAP rows, the STATEMENT status paragraph lines
3–8) state A1 / SCR-G faithfully to the current statement.

**Task 2 — per-claim table for all 21 rows.** Decide ACCEPT / REJECT / NOT-EXAMINED for every claim. Re-derive at least
what you need for each ACCEPT; rows you could only skim are NOT-EXAMINED. Priority if time is short: A1, SCR-G, SCR-M,
SCR-A, A-inf, B-lemmas, L1–L3, CC; then the rest.

## Common part (both seats)

**Repository and limits.** Worktree `/home/fb31/BVS-wt/W3-SCR-R2` (branch `theory/W3-SCR-R2`), on Owls. Read-only for
you, except two places: your report file `/home/fb31/BVS-wt/W3-SCR-R2/Theory_work/Wave3/W3-SCR-R2/reviews/R2_council_opus.md` and your scratch
folder `/home/fb31/SMC_Theory_Department/tmp/20261116-W3-SCR-R2-opus/`. Run no git command that changes state (no
commit, checkout, stash, fetch, push); the coordinator commits your report. Edit no other file. Do not start subagents.
If you run Python or R: `nice`, OMP_NUM_THREADS=1, at most 4 cores, short runs only (Owls is shared). Use `date` for
any timestamp you write.

**What W3-SCR is.** Theory ticket W3-SCR (certified screening, PROGRAM item 5) proves, for any fixed standardised
design and any search start, that a sparse **certified** model reported by the SMC-BVS method contains the true support
with high probability under a visibility condition, plus refinements (SCR-A°, master gap SCR-M, uncertified runs
SCR-G, bridges B1–B3, A1/A1°, excess set L5.1/L5.2, exact recovery SCR-C, refit SCR-R, sharpness SCR-N), and the code
facts CC1–CC6. It passed council C1 on its v3.3 text; post-pass v3.4 edits were never re-scored. **This round R2 scores
the current tree** (v3.4), as frozen in the manifest below.

**The frozen package (manifest `Theory_work/Wave3/W3-SCR/reviews/MANIFEST_R2.txt`, digest `96488f34902506d5cecf92b85aa257627ca396cdd7d3e60b86db32f688300b93`).** All paths under
`Theory_work/Wave3/W3-SCR/`: STATEMENT.md (v3.4; the 21 claims), CODE_CHECK.md, lemmas/L1_score.md … L7_master.md,
ASSUMPTION_MAP.md, REPORT.md, PLAN.md, numerics/ (supporting evidence, not proof). Before you start, run
`cd /home/fb31/BVS-wt/W3-SCR-R2 && python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-SCR Theory_work/Wave3/W3-SCR/reviews/MANIFEST_R2.txt`
and record its output in your report; if it fails, stop and give `gates=FAIL`. Production code (for CC checks and
EX-A): `Scripts/SMC_BVS/core/` (v3_fit.R, v3_run.R, v3_exact.R, v3_preprocess.R, cpp/v3_engine.h, cpp/v3_core.cpp,
cpp/v3_ledger.h, cpp/v3_score.h). Binding context: `Theory_work/Wave3/PROGRAM.md` item 5 (target card; results are
about the method as coded; design-agnostic statements; "asymptotic only" is not a limitation).
Do not read W3-SCR/reviews/ (earlier reviews, dispositions, scores), except what your seat section allows below.

**The 21 claims (registry ids `W3-SCR:<id>`; STATEMENT.md is authoritative for their text):**
CC, L1, L2, SCR-A, A-inf, SCR-Ao, Ao-inf, SCR-M, SCR-G, B1, B2, B2o, B2d, B3, A1, A1o, SCR-C, L5.1, L5.2, SCR-R, SCR-N.

**Rules of the round (PROTOCOL_v4 §5, principle 1).**
- A finding blocks only if it is **C** (correctness: a step is wrong or unproved), **S** (strength: the text claims
  more than is proved, or uses a hypothesis it does not state) or **F** (faithfulness: to the code as pinned, to cited
  sources, or to STATEMENT in any derived text such as REPORT or ASSUMPTION_MAP). Everything else is **E** (editorial:
  wording, notation, record, citation form, presentation of numerics); E never blocks and never lowers the score.
  Each C/S/F finding must name the clause or line and say exactly what fails.
- **You must give `gates=FAIL` if you hold any C, S or F finding of your own, whatever severity you would give it.**
- "A stronger theorem is provable" is not a finding; list it separately as a better-theorem note.
- A claim you did not check gets NOT-EXAMINED (it receives no checked label); do not ACCEPT what you did not check.
- Judge the **current text** on its own terms. That the v3.3 → v3.4 history is not recoverable byte-for-byte is a
  record matter (E), not a defect of the current proof; but a hypothesis the current proof uses and the current
  statement does not state is S.

**Report format (mandatory), in `reviews/R2_council_opus.md`:**
1. Manifest verify output.
2. Seat task results (see your seat section).
3. Per-claim table with exactly 21 rows: `| id | decision |` (ACCEPT / REJECT / NOT-EXAMINED), with a one-line
   reason or the lines checked in a third column if you wish.
4. Findings, numbered, each tagged C / S / F / E, with file:line, quoted text, what fails, and the fix you require.
5. Gates G1–G6, PASS/FAIL each with one line: G1 every step correct; G2 hypotheses used = hypotheses stated; G3 no
   hidden assumptions; G4 cited results have adequate status; G5 constants and rates tracked; G6 fidelity to the code.
6. Score (0.0–10.0, one decimal; reflects C, S, F only; ≥ 8.0 means correct and complete).
7. The verdict line below, last.

Then reply with: the verdict line, the per-claim table, and one line per finding (at most 20 lines).

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 96488f34902506d5cecf92b85aa257627ca396cdd7d3e60b86db32f688300b93` (round R2, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R2 manifest=96488f34902506d5cecf92b85aa257627ca396cdd7d3e60b86db32f688300b93 seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---

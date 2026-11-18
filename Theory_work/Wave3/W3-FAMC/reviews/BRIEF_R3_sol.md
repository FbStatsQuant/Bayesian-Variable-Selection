# BRIEF R3 — council seat `sol`, W3-FAMC (saved before launch)

Seat: gpt-6.2-sol (provider codex, reasoningEffort high). Manifest: `reviews/MANIFEST_R3.txt` = MANIFEST 68cb694453011ae4ffadfefe921ea5d62f92e8aa25c7a3d8ce281c4b433e498a. Commit 9862c933, branch theory/W3-FAMC.

---

Start your reply with the header line: `model: gpt-6.2-sol (provider codex, reasoningEffort high); round=R3; seat=sol; manifest=68cb694453011ae4ffadfefe921ea5d62f92e8aa25c7a3d8ce281c4b433e498a`.

You are the `sol` seat of council round R3 for ticket W3-FAMC (Tier B), checkout `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3fadba7-ec4a2133fdcc2bcf` (read-only for you except the
one reply file named below). You line-checked this ticket in rounds R1 and R2 (as a different Sol session); this is a council read of the frozen manifest. Judge the content as it is now.

**Files.** Write no file anywhere except your reply file. No git state changes. Do not start sub-agents. Read long files in
chunks of at most 120 lines. Do not read `LOG.md` or anything in `Theory_work/Wave3/W3-FAMC/reviews/` other than this brief,
`reviews/MANIFEST_R3.txt`, `reviews/INPUTS_R3.txt`, `reviews/CITECHECK.txt` and `reviews/E2_check_opus_R1.md` (the
independent E2 check the AR half rests on per HQ; read it as evidence, and check its conclusions where FAMC uses them).

**What the ticket claims.** One corollary, `W3-FAMC:Cor-FAMC` (STATEMENT.md §1, lines 48-80; reader version §1R; remarks
§1b are outside the claim): the conclusion of reader Theorem 6 (core 3; card row 3.1) — a common data event of
probability → 1 on which every admissible output run reports Ŝ = S₀, and under (S4) delivery with P(Ŝ = S₀) → 1 — holds
for (BLK) Gaussian rows with block-diagonal correlation (groups of fixed size ≤ g, λ_min(Σ_n) ≥ c) and for (AR)
Σ_lk = ρ^|l−k| with fixed ρ ∈ (−1, 1), under a coefficient condition (one truth per group / aligned signs / AR separation /
generic position off Lemma VIS's bad set B). Assembly only: no theorem change, no new lemma. The proof
(`lemmas/A_assembly.md`) verifies the hypotheses of the master `W3-RM2-R:RM2-R-plus` directly — the block side by explicit
linear algebra (B.0–B.4), the AR side by instantiating RM2 Example E2 (α = 3, b = 1/4, ϱ = 1/120) — with visibility from
Lemma VIS and C-GROW (G3b).

**Read (the frozen content).** `Theory_work/Wave3/W3-FAMC/`: STATEMENT.md, lemmas/A_assembly.md, REPORT.md, TARGET.md,
PLAN.md, DEPS.tsv, citecheck.py, deps_hand.py. Sources (`reviews/INPUTS_R3.txt`): reader Theorem 6 READER_VERSIONS.md
:660-813; RM2-R-plus W3-RM2-R/STATEMENT.md :118-182; RM2 hypotheses W3-RM2/STATEMENT.md :130-202; RM W3-RM/STATEMENT.md
:95-156; Lemma VIS W3-AUDIT/track_V/V1_VIS/STATEMENT.md (all); RM2 L6_examples.md §0 and §E2 (:33-263); C-GROW
L5_instances.md :8-66; TRACK_B B8–B11. Registry rows: quoted verbatim in STATEMENT §4 (verified by citecheck against
claims.tsv at main a779c1df; do not open registry files). Take the consumed claims as true as stated; check that their
hypotheses hold where used.

**Break it.** Check every step against STATEMENT and the sources: B.0 (cross-group partial covariances; localisation to a
group), B.2 (visibility on each route, incl. the reduction of (BLK-s) to VIS-a on one group, and VIS-b's constants), B.3
(feasibility against K = min(p, ⌊n/2⌋); H_l sizes; ϖ_n = r_n = 0), B.4 (regression identity; (D-loc)/(D-loc^b) as the
RM2 implication consumes them); A.0 (AR is in E2's class), A.1 (parameters admissible; E2's list matches RM2-R's
hypotheses), A.2 (VIS-e path graph, ρ = 0, C-GROW (G3b) and the sign reduction, VIS-b); that the conclusion in §1 is
exactly what RM2-R-plus + RM0-plus + DLV-0 give and nothing more; that §1R says nothing beyond §1 and omits no hypothesis;
D109 classes (§2) and D126 expansion (§4); whether any hypothesis is used but not stated. Sweep duties (Tier B): REPORT and
its registry block vs STATEMENT (REPORT must claim nothing beyond STATEMENT; the registry block's spans, assumptions,
conclusion and depends_on); DEPS rows; TARGET's parity tags; the changelog tags. **Interpretive sentences:** list every
"hence …", "so …", "in particular …", "this is …" sentence inside the registered span (STATEMENT §1, lines 48-80) and give
each a verdict (checked / must move out / false).

**Acceptance filter.** Genuine flaws only. "A stronger theorem is provable" is not a finding (list it separately).
Probability-zero / null-set caveats never block.

**Return.** (a) per-claim table `| id | decision |` (ACCEPT / REJECT / NOT-EXAMINED) for W3-FAMC:Cor-FAMC; (b) findings,
each tagged **C** (a step is wrong or unproved), **S** (claims more than proved, or uses an unstated hypothesis), **F**
(unfaithful to a cited source or STATEMENT) or **E** (editorial; never blocks), with `file:line` and what fails; (c) the
interpretive-sentence list; (d) the six gates — correct, strength, faithful, statuses, sweep, reader — PASS/FAIL with one
line each; (e) a score 0.0–10.0 (reflecting C, S and F only) and the verdict line below.
**You must give `gates=FAIL` if you hold any C, S or F finding of your own, whatever severity you would give it.**

Write your full reply to `Theory_work/Wave3/W3-FAMC/reviews/R3_council_sol.md` (create it; write nothing else anywhere),
and return a ≤ 10-line summary as your final message.

## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 68cb694453011ae4ffadfefe921ea5d62f92e8aa25c7a3d8ce281c4b433e498a` (round R3, seat `sol`). End your review with exactly ONE line of
its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R3 manifest=68cb694453011ae4ffadfefe921ea5d62f92e8aa25c7a3d8ce281c4b433e498a seat=sol score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this manifest;
  otherwise `gates=FAIL`. First run `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-FAMC
  Theory_work/Wave3/W3-FAMC/reviews/MANIFEST_R3.txt` from the repo root; if it does not print OK, write `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for another manifest, not as an example, not in prose).

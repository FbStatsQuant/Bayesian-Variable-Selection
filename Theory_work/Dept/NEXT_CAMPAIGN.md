# Next campaign — consistency results and their Lean certificates (Theory Department proposal to HQ; DRAFT v1, 2026-11-15)

Final version due Thu 11-19. v0 (parallel-SMC theory) is superseded by the owner's priority (2026-11-15 evening):
**"first we do all consistency results and even their lean parts."** The parallel-method theory is not a priority
now: T-MERGE parked; EVAR / POOL stay in the scaling paper; premise tickets are Engineering's choice (D18).
Sources: `QUEUE.md`, `DECISIONS.md` D1–D23, `research/LEAN_READINESS.md` (in preparation), `Lean/BRIEF.md`.

## (a) Finish all consistency results
| item | owner | state (11-15) | gate / date |
|---|---|---|---|
| **W3-DIST** (distribution consistency, top priority) | Fable lead (top-level thread) | CP1 GO; key Lemma X/X′ line-checked VERIFIED; CP2 break review running; other line checks running | CP2 → sweep → council → **CP3 this week** (target: chapter v2.0) |
| W3-START2-R (START2 v1.5: T10 rate, T8 visibility, START restatements) | Opus lead | statement lock (Sol) | CP3 Wed 11-18 18:00 CT |
| W3-RM2-R (T4 constant-level signals, T2 delivery + mode interface) | Opus lead | statement lock (Sol) | CP3 Wed 18:00 |
| W3-PSHARP-R (T12 expectation bound for every p) | Opus lead | statement lock (Sol) | CP3 Wed 18:00 |
| W3-MISR-R (T13 Cor-G(a), Cor-H) | child agent | queued (first free slot) | CP3 Wed 18:00 |
| Strength gates, five-pillar rows (lit / necessity / better) | W3-READER leg 2; better-gate for uncovered rows via HQ's API Fable batch (SHARP3 list by Wed 12:00) | after READER CP1 | Thu 11-19 18:00 |
| Reader versions + claims card | W3-READER | CP1 waits on Sol S1 | CP1 → H5 card via HQ; rider READER_DELTAs absorbed by Thu |
| Acceptance backlog: W3-POST2 (D), W2-APP (C/C′), W3-POST:Thm-1 = SOP:TH09 root (H), Engineering entries (E) | recorder (dry runs) → HQ real runs | D, E clean; C PC1 FAIL (proposal: C3 snapshot); H staged | before the Fri freeze |
| W3-EDIT editorial pass | Opus lead | citation fixes done (PR #10 path via recorder task G) | CP1 Wed 18:00 |

After the Fri 11-20 freeze, anything unproved goes to the open-problems section (named open items in QUEUE.md).

## (b) Lean certificates of the consistency results
To be filled from `research/LEAN_READINESS.md`:
- Level 1 (deterministic cores): which are checked and stable **now**, which wait for a rider's CP3 (Wed) or for
  W3-DIST CP3, with an effort estimate each.
- Level 2 skeletons (2–3 headline consistency theorems; DIST-1 expected first): the named axioms each needs.
- Proposed Lean launch date and order, for HQ's decision. Fidelity check per statement (Sol), per `Lean/BRIEF.md`.

## (c) Parked (owner, 11-15)
T-MERGE (convex pooling) · EVAR / POOL (evidence variance; scaling paper) · T-N, T-PART, T-STREAM, T-CAL
(Engineering's design choices; PSMC-S0 Part 1 delivered as Engineering-facing notes) · approximate sparsity and
exponential p for W3-DIST (stretch, after DIST closes).

## (d) Found while scoping (for HQ)
- Pooled PIP: method text vs code (02_method.tex:440-451 vs v3_run.R:154,162). Routed (D13): READER fixed; W3-EDIT
  item 7; Writing queue row.
- W3-SCALE O1(c) ("N1 does not cover the shipped Rao–Blackwellised PIP") looks closed by T12(ii) (digest §4); parked
  with T-MERGE.

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

## (b) Lean certificates of the consistency results (from `research/LEAN_READINESS.md`, 2026-11-15)
- **Ready now (Level 1, deterministic, stable this week):** SL0; LT♯ (LT-d) sup-norm core; prior counting (T01
  `lem:prior`, locked); DIST Lemma H (= POST2 D0 averaged over x). ≈ 3–4 lead-days. DIST C-0 / P6: small, pin to the
  DIST CP3 version.
- **Shared score base** (T01 `lem:spec` + PSHARP Lemma S; Schur-complement route; ≈ 1–1.5 weeks), then on top:
  PSHARP Cor B / (B1), POST2 A2 / A0 / E3.1, MISR R′, START FLOOR, SCR L1 + bridges B1–B3, RM-0(a). The riders do not
  change these (checked against their delta statements).
- **After the rider CP3s (Wed 11-18):** RM0⁺(b), RM2 TL identity + counting bounds, PSHARP (B3) wording, MISR
  Cor-G(a)/Cor-H (Level 2 only).
- **Level 2 skeletons, in order:** DIST-1 (after its CP3; named axioms: χ² tails, Gaussian quadratic-form MGF,
  Hoeffding, Cantelli, half-space growth, Bernstein, ε-net, sub-Gaussian scale) → W3-POST:Thm-1 items 1–5 (χ²/Gaussian
  tails, conjugate formulas; item 6 excluded while W2-APP:POST is unrecorded) → RM2-F after its rider.
- **Not Lean targets:** DLV-0 (code audit), full N1 (product-measure plumbing). Reuse: an old sorry-free snapshot
  (`Old_Projects/.../L-LEAN`, same toolchain + Mathlib rev) has HPM / Markov / lattice-descent steps for RM-0.
- **Launch proposal:** GO Thu 11-19 for the inventory + first batch (statements frozen by then), or one launch Mon 11-23
  after the freeze; Level 2 from Mon 11-23 with DIST-1 if its CP3 lands by Fri, else W3-POST:Thm-1. Caveats: Mathlib
  coverage to verify in the Lean inventory; certificates of rows still unchecked in the registry must say so.

## (c) Parked (owner, 11-15)
T-MERGE (convex pooling) · EVAR / POOL (evidence variance; scaling paper) · T-N, T-PART, T-STREAM, T-CAL
(Engineering's design choices; PSMC-S0 Part 1 delivered as Engineering-facing notes) · approximate sparsity and
exponential p for W3-DIST (stretch, after DIST closes).

## (e) Protocol variant
Sent with this proposal for approval: `PROTOCOL.md` (POLICIES §13), deviations B1–B10.

## (d) Found while scoping (for HQ)
- Pooled PIP: method text vs code (02_method.tex:440-451 vs v3_run.R:154,162). Routed (D13): READER fixed; W3-EDIT
  item 7; Writing queue row.
- W3-SCALE O1(c) ("N1 does not cover the shipped Rao–Blackwellised PIP") looks closed by T12(ii) (digest §4); parked
  with T-MERGE.

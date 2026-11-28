# BRIEF R4 — council seat `sol`, W3-FAMC (diff check; saved before launch)

Seat: gpt-6.2-sol (provider codex, reasoningEffort high). Manifest: `reviews/MANIFEST_R4.txt` = MANIFEST 7fab398c7efd556e3b4b25914e9273b30a25ffcd39be24b47d25d8e3ba9d29f7. Commit cf0fc37c, branch theory/W3-FAMC. Previous
round: R3 = MANIFEST 68cb694453011ae4ffadfefe921ea5d62f92e8aa25c7a3d8ce281c4b433e498a (commit 9862c933).

---

Start your reply with the header line: `model: gpt-6.2-sol (provider codex, reasoningEffort high); round=R4; seat=sol; manifest=7fab398c7efd556e3b4b25914e9273b30a25ffcd39be24b47d25d8e3ba9d29f7`.

You are the `sol` seat of council round R4 (diff check) for ticket W3-FAMC (Tier B), checkout `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3fadba7-ec4a2133fdcc2bcf` (read-only except
your one reply file). Write no other file, make no git changes and start no sub-agents. Read long files in chunks of at
most 120 lines.

**Background.** In R3 both seats checked the mathematics of `W3-FAMC:Cor-FAMC` (STATEMENT.md §1) and its proof
(lemmas/A_assembly.md) and found no C or S finding. Both gave gates=FAIL on F-level provenance/registry points. Read
`reviews/R3_council_sol.md`, `reviews/R3_council_opus.md` and the lead's `reviews/R3_disposition.md`. The registered claim §1
is byte-identical to R3 (only shifted one line, 48-80 → 49-81).

**Task.** Run `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-FAMC
Theory_work/Wave3/W3-FAMC/reviews/MANIFEST_R4.txt` from the repo root (it must print OK, else gates=FAIL). Run
`git diff 9862c933 cf0fc37c -- Theory_work/Wave3/W3-FAMC ':!Theory_work/Wave3/W3-FAMC/reviews'` and diff
`reviews/MANIFEST_R3.txt` against `reviews/MANIFEST_R4.txt`. Then:
(1) for every R3 finding of BOTH seats (sol F1–F4, E1–E3; opus F-1, E-1–E-8) give RESOLVED / PARTIAL / NOT RESOLVED with one
line of reason. In particular, check that the E2 report `reviews/E2_check_opus_R1.md` is now bound (an EXT line in
MANIFEST_R4 with the sha256 named in STATEMENT §4), and that the REPORT registry block (spans, A:FAMC-COEF, A:DELIV-D,
conclusion, depends_on) is exact against STATEMENT §1 v1.4;
(2) check that the changed text introduces no new error, and that §1 is unchanged (compare the spans);
(3) re-affirm or revise your per-claim decision for W3-FAMC:Cor-FAMC and the six gates (correct, strength, faithful,
statuses, sweep, reader), on exactly this manifest.
Acceptance filter: genuine flaws only; no nitpicks; null-set caveats never block. Tag new findings C / S / F / E as in R3.
**You must give gates=FAIL if you hold any C, S or F finding of your own.**

Write your reply to `Theory_work/Wave3/W3-FAMC/reviews/R4_council_sol.md`. Final message: ≤ 8 lines.

## Verdict line (mandatory, machine-checked)

End your review with exactly ONE line of its own, in exactly this form (backticks allowed, nothing else on the line):

```
COUNCIL-VERDICT round=R4 manifest=7fab398c7efd556e3b4b25914e9273b30a25ffcd39be24b47d25d8e3ba9d29f7 seat=sol score=<x.y> gates=PASS|FAIL
```

Write no other line containing `COUNCIL-VERDICT` (not for R3's manifest, not as an example, not in prose).

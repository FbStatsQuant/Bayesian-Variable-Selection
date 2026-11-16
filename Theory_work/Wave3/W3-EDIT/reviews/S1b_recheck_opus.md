# S1b re-check: Opus 5.5, high (wording only)

Scope: the single repair in commit `c870ccc` to `Theory_work/Wave3/W3-MISR/ASSUMPTION_MAP.md:17` (Sol finding S1,
`reviews/S1_editorial_check_sol.md:41–43`). This was read-only. The only file written is this reply.

## What was checked

- `reviews/S1b_diff.patch` matches `git diff c870ccc~1 c870ccc -- Theory_work/Wave3/W3-MISR/` byte for byte. Outside
  `W3-EDIT/`, the commit touches exactly one file, `W3-MISR/ASSUMPTION_MAP.md`: 1 insertion and 1 deletion, all on line 17.
  `git diff c870ccc HEAD -- Theory_work/Wave3/W3-MISR` is empty, so line 17 at HEAD is the repaired line.
- A word diff of the hunk shows that only the closing bold phrase changed:
  `**weakenable, not removable**` → `**numerical evidence compatible with weakening; non-removability suggested, not proved**`.
  Everything else in the row is unchanged.
- Sol's proposed replacement, extracted mechanically from `S1_editorial_check_sol.md:43`, was compared with the
  `— **…**` segment cut from line 17. `cmp` reports them identical, em dash and bold markers included.
- Sources read: `STATEMENT.md:250–264` (§9 "Not claimed"), `REPORT.md:62` and `REPORT.md:76`, `numerics/N5_out.txt`
  (all 20 lines), the docstring of `numerics/N5_energy_obstruction.py` (for the arm and constant claims on the row), and
  `reviews/R2_council_sol.md:31`.

## Findings

**C: none.** The commit leaves every hypothesis, conclusion, quantifier, constant and proof step of every W3-MISR claim
untouched. The one changed span is the evidence/status cell of an assumption-map row. It is not a statement span.
No STATEMENT, lemma, proof or numerics file in W3-MISR differs between `c870ccc~1` and HEAD.

**S: none remaining. S1 is resolved.**
- (Q1) The replacement is exactly Sol's text. It removes the categorical "not removable", which was the whole of
  finding S1.
- (Q2) Line 17 as it now reads matches its sources:
  - *"non-removability suggested, not proved"* agrees with `STATEMENT.md:260–264` ("evidence that it cannot simply be
    dropped — numerical, with an analytic sketch; not a checked proof"), with `REPORT.md:62` and `REPORT.md:76`, and with
    R2 Sol :31, which forbids promoting finitely many posterior-mass estimates to a proved asymptotic failure.
    `N5_out.txt:14–19` shows only that E π(S₀) falls over the sampled n (0.8702 → 0.0031 for n = 100 … 102400), and the
    row reports exactly those values.
  - *"numerical evidence compatible with weakening"* agrees with `REPORT.md:76` ("weakenable (N4)") and with the row's
    own N4 citation (energy/(nv) ≍ n^b, δ/r_n 0.47–1.22, HPM ≥ 0.98), which the row already calls "finite-sample
    behaviour compatible with the conclusion". The new wording is weaker than the old "weakenable": it claims
    compatibility, not that the assumption can be weakened.
  - The repaired ending is now consistent with the qualifier at the head of the same row ("finite-sample N5
    observations with an analytic sketch, not a checked asymptotic proof"). The row no longer contradicts itself.
  - The rest of the row is unchanged and was already checked under I4-S1/I4-S2. On a spot check against the sources it
    is consistent: the N5 values match `N5_out.txt:2–19`. The arm description, "(OS) void", "(F₀) holds", the ridge-loss
    expression and c₁(2, 1) ≈ 258.9 match the N5 docstring and `STATEMENT.md:261–263`. The control arms are described as
    "numerical controls, not verified instances of the margin class", which matches the docstring.

**F: none.**

**E: none.**

Not a finding, and outside the S1b scope: `ASSUMPTION_MAP.md:54` and `REPORT.md:76` still use the unqualified word
"weakenable" in summary lists. Both now come after the "not a checked asymptotic proof" qualifier, and neither claims
non-removability. Sol S1 was limited to line 17, so this is noted only for HQ's information.

RECHECK verdict=PASS S1=RESOLVED math_changed=NO

# W3-EDIT item 6: citation fixes are done (2026-11-15 ~19:55 CST)

Fix commit: `1a198e6` on `theory/W3-EDIT`. Ledger rows C6-01 to C6-11 (`LEDGER.tsv`). Wording and citations only.

## What changed
1. **C-MIS.** SoP v1.1 (`dd60e09`) added lines to `04_theory.tex`: +3 after line 181 and +3 after line 537. So
   seven cites in C-MIS now point to the wrong lines. Each is re-pointed to the same content:
   - `STATEMENT.md:59`: 774-782 → 780-788
   - `STATEMENT.md:174`: 811 → 817
   - `lemmas/L1_reduction.md:10`: 776-782 → 782-788
   - `lemmas/L1_reduction.md:16`: 776-779 → 782-785
   - `lemmas/L1_reduction.md:45`: 775 → 781
   - `lemmas/L1_reduction.md:62`: 811 → 817
   - `lemmas/L3_hpm.md:6`: 466 → 469

   The six matching CHECKS rows in `numerics/citecheck.py` are updated, and `reviews/CITECHECK.txt` is regenerated.
2. **W2-FAC-X.** `reviews/citecheck.py` gets the path prefix `'Theory_work/Wave2/'`, in the same position as in
   `citecheck_final.py:15`. It now resolves `W2-FAC-B/REPORT.md:30` and `W2-FAC-A/REPORT.md:20`, cited at
   `STATEMENT.md:118,122`. The other 5 cites resolve to the same files as before. `reviews/CITECHECK.txt` is
   regenerated; its hand-appended status-string section is kept verbatim. `citecheck_final.py` was rerun: 7/7, 11/11
   and 7/7 OK.

## Citecheck outputs (python 3.13.16, from the worktree root)
- `Theory_work/Wave1C/C-MIS/numerics/citecheck.py`: 34 OK, 0 MISS, `ALL OK`.
- `Theory_work/Wave2/W2-FAC-X/reviews/citecheck.py`: `TOTAL ok=7 miss=0` (was ok=5 miss=2).

## CI (`run_ci.py --steps check,paper,cite`, committed HEAD)
- Run on this branch: cite PASS for C-MIS (0→0) and W2-FAC-X (0→0). C-PACK shows 0→2. That is the baseline-lookup
  gap PR #10's change 1 fixes; this branch does not cause it.
- Run on a throwaway merge of this branch with PR #10's head `84eec64`: **cite PASS** (C-MIS 0→0, C-PACK 2→2,
  W2-FAC-X 0→0), paper PASS. check FAIL, on exactly the 3 expected rows below.

## Needed together with the merge (HQ recorder)
`check.py --quiet` has exactly 3 new findings, all `C2-changed`. In each row, the edited line `STATEMENT.md:59` lies
in the premise `STATEMENT.md:54-62`. Until these rows are rehashed, CI `check` stays red. So the rehash goes into
the same merge as `1a198e6`; then PR #10 can go green.

| claim id | file | old sha256 (claims.tsv) | new sha256 | lines touched | ledger |
|---|---|---|---|---|---|
| C-MIS:Thm-MIS(i) | Wave1C/C-MIS/STATEMENT.md:65-69 | ea3faa22001a2dcb… | b555b89d49e7512e… | 59 (premise) | C6-01 |
| C-MIS:Thm-MIS(ii) | Wave1C/C-MIS/STATEMENT.md:73-78 | c7142232e0a44555… | da5008a078e6937d… | 59 (premise) | C6-01 |
| C-MIS:Cor-N | Wave1C/C-MIS/lemmas/L1_reduction.md:65-74 | 119c08d809e71be2… | 66c3346b8cbe0972… | 59 (premise) | C6-01 |

Command for each row: `registry.py rehash <id> --bump patch` (1.0.0 → 1.0.1). I did not run it.

**Note.** The accepted manifests of W3-MISR (`MANIFEST_R1/R2`) and W3-START list C-MIS `STATEMENT.md` and
`L1_reduction.md` as frozen extras. Those manifests still verify at their recorded commits, but `manifest.py verify`
at the new HEAD will report the C-MIS files as changed. This is the usual effect of a patch bump; no open council
manifest is affected.

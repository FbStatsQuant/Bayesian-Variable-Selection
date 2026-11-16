# PC — C-MIS citation-fix: is it citation-only? (independent review, Opus 5.5)

Date: 2026-11-15. Scope: this was a read-only check. I ran `git fetch origin` (origin/main 8efc627..5ab981e) and no other git command changed anything. No subagents were used. This file is the only output.

## What I checked

- **Commits.** 66b67f7 (merge of theory/W3-EDIT-citefix) contains cherry-pick 3c6062e (`git merge-base --is-ancestor 3c6062e 66b67f7` succeeds).
  - `git diff 3c6062e 66b67f7 -- C-MIS/{STATEMENT.md,lemmas/}` is empty, so the merge adds nothing beyond the cherry-pick for these files.
  - `git diff 66b67f7 origin/main` is empty for `Theory_work/Wave1C/C-MIS/` and for `04_theory.tex`.
- **Diff examined.** `git diff 3c6062e^ 66b67f7` on `Theory_work/Wave1C/C-MIS/STATEMENT.md`, `lemmas/L1_reduction.md` and `lemmas/L3_hpm.md`. It has 7 changed lines (2 + 4 + 1), and each `-`/`+` pair differs only inside a backticked `04_theory.tex:N[-M]` token. I confirmed this with `--word-diff=porcelain`.
- **SoP versions.** "Old" is `dd60e09^:Theory_work/State_of_Project/sections/04_theory.tex`. "New" is the same file at `66b67f7`, which is also unchanged at origin/main. The only commit in `dd60e09^..66b67f7` that touches it is dd60e09 (SoP v1.1).
- **Span check.** For each pair, I compared the old line range in the old file with the new line range in the new file using `diff`. **All 6 distinct span pairs are byte-identical.** Each moved by +6 lines, except 466→469, which moved by +3.
- **Byte check.** I took each file at 66b67f7, reverted only the 7 cite tokens with `sed`, and ran `diff` against the file at `3c6062e^`. All three files come out byte-identical. Byte counts are also unchanged: 18463, 11058 and 7186. So there is no whitespace, EOL, math, hypothesis, conclusion or status change.
- **Completeness.** At 66b67f7 these three files contain exactly 7 `04_theory.tex:` cites, and all 7 are the re-pointed ones. No cite into 04_theory.tex was left stale.

## Table

| file:line | old cite | new cite | old content (short), old 04_theory.tex | new content (short), current 04_theory.tex | same? |
|---|---|---|---|---|---|
| C-MIS/STATEMENT.md:59 | `04_theory.tex:774-782` | `04_theory.tex:780-788` | 774 `\begin{stmt}{…THEOREM_LIST_FINAL.md:448-451}`; 775 "**R1, R.** Fixed-design triangular array, fixed s₀≥1, p≤n^A…"; …; 782 "**Final statement.** Under R1, G, R, SE_λ(j₀), SE_w(m♯_n;g₀), and BM-∞ or BM(c>c₀), 1−π(S₀)=O_P(√(log n/n))…" | 780 `\begin{stmt}{…:448-451}`; 781 "**R1, R.** Fixed-design triangular array, fixed s₀≥1…"; …; 788 "**Final statement.** Under R1, G, R, …" | YES (byte-identical 9 lines) |
| C-MIS/STATEMENT.md:174 | `04_theory.tex:811` | `04_theory.tex:817` | "\item Asymptotic only, onset n≳2·10⁶ (…q_n≤½ first holds at n≈2.1·10⁶/2.5·10⁶; the earlier "1.2e5" claim was an ERROR)…" | same text at 817 | YES (byte-identical) |
| C-MIS/lemmas/L1_reduction.md:10 | `04_theory.tex:776-782` | `04_theory.tex:782-788` | 776 "**Tail cutoff.** … m♯_n=min{m≥s₀: R_m≤n^{-(s₀+2)/2}}…" through 782 "**Final statement.** Under R1, G, R, …" | 782 "**Tail cutoff.** …" through 788 "**Final statement.** …" | YES (byte-identical 7 lines) |
| C-MIS/lemmas/L1_reduction.md:16 | `04_theory.tex:776-779` | `04_theory.tex:782-785` | 776 "**Tail cutoff.**…"; 777 "**Anchored eigenvalues.** j₀=⌈(2A+1)s₀⌉+1. SE_λ(j₀)…SE_w(m♯_n;g₀)…"; 778 "**Signal thresholds.** BM-∞ … BM(c), c>c₀(s₀,A)…"; 779 `\end{stmt}` | 782 Tail cutoff; 783 Anchored eigenvalues; 784 Signal thresholds; 785 `\end{stmt}` | YES (byte-identical 4 lines) |
| C-MIS/lemmas/L1_reduction.md:45 | `04_theory.tex:775` | `04_theory.tex:781` | "**R1, R.** Fixed-design triangular array, fixed s₀≥1, p≤n^A…" | same text at 781 | YES (byte-identical) |
| C-MIS/lemmas/L1_reduction.md:62 | `04_theory.tex:811` | `04_theory.tex:817` | "\item Asymptotic only, onset n≳2·10⁶ …" | same text at 817 | YES (byte-identical) |
| C-MIS/lemmas/L3_hpm.md:6 | `04_theory.tex:466` | `04_theory.tex:469` | TH05 card "**Status (registry, verbatim):** … T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" …" | same text at 469 | YES (byte-identical) |

Line numbers in the first column are at 66b67f7. Before the change they were STATEMENT.md:59/174, L1:10/16/45/62 and L3:6. The diff adds no lines, so the numbers are the same before and after.

## Non-blocking observation (pre-existing; the fix neither introduced nor resolved it)

- **L1_reduction.md:16** cites `776-779` (now `782-785`) for "R1, R, SE_λ(j₀), SE_w(m♯_n; g₀), BM-∞ or BM(c > c₀)". That range begins at the *Tail cutoff* line. The **R1, R** line itself is old 775 / new 781, so it falls just outside the range.
- **L1_reduction.md:10** has the same feature (`776-782` → `782-788`): the range starts after the R1/R line.
- The re-point shifted both ranges by +6 and kept them exactly as they were, which is the right behaviour for a citation-only fix. Whether to widen the ranges to `781-785` / `780-788` is a separate wording question. It does not affect this verdict.
- The L3_hpm.md change is outside the two manifest-frozen files. It also checks out as citation-only.

PC-VERDICT: CITATION-ONLY

# FAILED_ATTEMPTS (L-LEAN)

Approaches tried and abandoned, with the reason for each. Read this before retrying anything.

1. **`import Mathlib` in project modules.** The first build sat in the Mathlib load for more than 30 min, at about 0.6 GB working set, while the machine had only about 3.5 GB of free RAM. Abandoned in favour of targeted imports, which compile a module in 20–30 s.
2. **`codex exec "<prompt>"` without closing stdin.** codex printed "Reading additional input from stdin..." and hung. Fix: append `< /dev/null`.
3. **Writing several Lean blocks in one Git Bash heredoc command.** It failed with a bash quote-parsing error. Fix: write each block with the Write tool, then insert it with a small Python script.

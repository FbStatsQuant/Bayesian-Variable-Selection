# Engineering branch sweep — 2026-11-17 (HQ "everything to main, no long tail")

## LIVE (4 on origin)
| branch | role | path to main |
|---|---|---|
| core/v3.1-listpip | #69 core → main (list-PIP fields) | Sol fixes (WP4) → HQ merges + tags `method-v3.1-listpip` |
| exp/P1M-list-pip | #68 → exp/P1M-engine | Sol fixes + merge engine in (README.md conflict only) → merge into engine |
| exp/P1M-engine | frozen campaign engine (Scripts/SMC_BVS/engine_v4 + tests + driver + docs) | ONE freeze PR → main, Wed–Thu, CI green; `git merge-tree` against main is clean today |
| exp/P1M | P1M docs branch (Docs/Experiments/P1M only, 152 files) | ONE docs PR → main at freeze; merge-tree clean today |
Builder 7 P-6 (test polish) will open one branch, exp/P1M-polish-p6, with one PR into the engine before the freeze.

## DONE: 67 branches, every commit already in exp/P1M-engine or main (git cherry = 0), deleted from origin
- exp/P1M-* merged via #11–#67, #70–#73 into exp/P1M-engine (wp1-*, wp2-*, wp3-* except arch/m3, wp4-*, wp5-*, wp6-*, wp7-*, manifest-h9/h10, mgr-*, polish*, driver-*)
- infra/actions-ci (#10), infra/P1M-offload (#35), infra/ci-cite-cwd, infra/accept-identity-case-v2/-nb, infra/R05-ckpt-status, infra/R06-eol, infra/R07-accept-form: all on main

## OBSOLETE: 3, deleted (archived as tags where they held unique code)
- exp/P1M-wp3-arch: WP3 architect prototypes and bench, not production (the review is in WP3_ARCH_REVIEW.md) → tag `archive/P1M-wp3-arch`
- exp/P1M-wp3-m3 (local only): merge-path prototype, superseded by #43 (wp3-m3fix) → tag `archive/P1M-wp3-m3`
- infra/accept-identity-case: first cut, superseded by -v2 (on main)

Local copies of 21 DONE/OBSOLETE branches stay only because finished agents' worktrees still check them out. They are not on GitHub.

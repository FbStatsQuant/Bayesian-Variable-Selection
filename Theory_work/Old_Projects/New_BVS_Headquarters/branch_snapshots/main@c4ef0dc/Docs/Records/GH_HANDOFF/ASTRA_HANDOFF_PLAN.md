# SMC-BVS: later GitHub and HQ handoff

**For Felipe — design advice, 2026-10-29. No migration is authorized by this document.**

**Recommendation:** finish the entire New Campaign empirical phase, then transfer its complete working context and all unique research source into the existing repository. Keep heavy artifacts in their verified external stores. Use `/home/fb31/BVS_GH` as the new HQ workspace, with one active HQ and one watchdog. “Total transfer” means every research item is accounted for and the new HQ can continue without relying on the old working folder; it does not mean putting raw simulations or agent databases in Git.

Scope of this inspection: the named project documents; root CODE_LEDGER (skim); campaign code/conformance/ops/tests inventories and progress; Claude memory index and relevant linked notes; local repository files/Git metadata; read-only Owls inspection; HQ thread metadata and scheduled-task listing. NOTS facts below come from saved OPS inventories and cleanup receipts, not a new live NOTS audit. No simulations, copies, moves, deletions, thread messages, schedule changes or repo edits were performed. Only this plan and its containing folder were created.

Path abbreviations: **OLD** = `<OLD_ROOT>`; **NEW-PC** = `<PC_REPO_CLONE>`; **I** = `OLD/02_Experiments/I_2026-10-28_New_Campaign`; **NB** = `<PC_NB_ARCHIVE>`. Proposed repo paths below are relative to `/home/fb31/BVS_GH`.

## A. Inventory: what must survive HQ

### Observed state, not a completion certificate

- NEW-PC and Owls `/home/fb31/BVS_GH` are on `main`, clean in the inspected status, at `eb75737813105f496c23112060cf26d28846bee0` (five commits). Origin is `FbStatsQuant/Bayesian-Variable-Selection`. No fetch/pull was performed; this is observed clone state, not a fresh GitHub-head check.
- Owls also contains **a separate nested clone**, `/home/fb31/BVS_GH/Bayesian-Variable-Selection`, at `39db138170e7bde0f3ebedef8b38fd76d1444ae3`. Do not bootstrap there or recursively import it. `/home/fb31/AGENTS.md` is empty; no AGENTS.md/CLAUDE.md was found at the outer repo root. The second PC was not inspected.
- The repo already has v2.1 code, eight benchmark implementations, exact-reference tools, theory, reports and final tables. The campaign is developing **v2.2.1**; these are different releases, not duplicate filenames to overwrite indiscriminately.
- The live board still says CONF-2b is running and pilot/production/analysis are pending. Its finer-grained progress file records clean PROD-H tests and Sol review 3 launched at 23:30Z. D23 allows throttled PROD-H after bundle review, with PROD-L after the pilot; the board's generic “production waits on pilot” is less precise. Reconcile both at freeze.
- Older HQ/memory entries are historical: 7 GiB campaign ceiling, loginx3, pending P5, pending identity gate, and 1,500/5,400-second production limits are superseded. Current D7/D8 specify **0.5 GiB campaign home / 9.6 GiB total home**, loginx2 through `ssh nots`; D11 adopts P5, D20 accepts the identity gate with an amendment. Use the final approved job bundle for limits.

### Responsibility and record transfer

| What old HQ does/holds | Source to preserve | New form and owner |
|---|---|---|
| Chooses work order, gates deployment, assigns scoped workers, integrates reviews, gives Felipe short results | `00_Admin/HQ_CAMPAIGNS.md`, campaign charter/decisions, HQ decisions | `Docs/HQ/CHARTER.md`, `STATUS.md`, `DECISIONS.md`; HQ alone owns live boards |
| Maintains project map and code provenance | `README.md`, `PATH_MAP.md`, root `CODE_LEDGER.md`, `tools/ledger_check.py`, campaign `code/CODE_LEDGER.md` | Root README links to `Docs/Records/PATH_MAP.md` and provenance indexes; original ledgers retained unchanged; checker under `Scripts/Tools/` |
| Runs empirical gates and recovery | `I/{CHARTER,DECISIONS,STATUS}.md`; `conformance/{CONFORMANCE,PATCHES,REGRESSION,OUTPUT_FIELDS,CONF2B_PROGRESS}.md`; reviews, job bundles, code manifests, tests | `Docs/Campaigns/2026-10-28_New_Campaign/`; final approved code/bundles under `Scripts/`; final tables under `Results/` |
| Coordinates NOTS, quotas, transfers, cleanup and failures | `I/ops/{NOTS_INVENTORY,NOTS_ENV,OPS_LOG,DISK_LOG,CLEANUP_PLAN,CLEANUP_LOG}.md`, transfer scripts, evidence/receipts | `Docs/HQ/OPERATIONS.md`, immutable campaign records; shared tooling under `Scripts/Ops/` |
| Owns methodology, theorem status and future decisions | Master, METHODOLOGY_v3, theory map/rulings/failed attempts, locked proofs, inventory, frozen paper selection, campaign plan, `LEVERS.md` | `Docs/{Methodology,Theory,Manuscripts,Records}/`; preserve “proved”, “reviewed”, “locked” and “adopted” as distinct statuses |
| Holds cross-session preferences, pitfalls and history | Claude memory directory described below; project `.claude/`, `.codex/`; user protocol references | Portable approved rules in root `AGENTS.md`; thin `CLAUDE.md` instructing Claude to read it; curated memory under `Docs/HQ/Memory/`; sanitized protocol dependencies under `Docs/HQ/Protocols/` |
| Recovers crashed delegates and advances approved waves | Enabled HQ watchdog, task IDs and thread references on board | `Docs/HQ/WATCHDOG.md` (definition, guardrails, installation receipt); new host-bound schedule only after cutover |
| Supplies evidence for past actions | Reorganization/migration logs, approvals, checksums, old reports and relevant thread decisions | `Docs/Records/Migrations/`, `Docs/History/`, external-artifact catalog; preserve historical paths inside evidence |

**HQ identity and watchdog.** Inspected HQ: <<thread-link>> (Claude Opus 5.5). Its latest run is completed; that does **not** mean the campaign is complete. Scheduled task `<scheduled-task>`, “HQ agent watchdog (New Campaign)”, is enabled every 1,800,000 ms, bound to old project `<uuid>`; last reported run succeeded. It reads STATUS → DECISIONS → CHARTER, checks crashes/queued >20 min/idle >60 min, resumes or replaces failed delegates after checking existing work, updates boards and advances approved gates. It forbids Fable/Astra launches, methodology changes and unapproved NOTS submissions. Archive its exact definition at freeze. **Do not blindly replay it:** its old task IDs, host bindings and launch sequence expire at handoff; recreate compatible behavior using the then-current T3 APIs and delegation lifecycle rules.

**Memory.** Source is `<PC_CLAUDE_CONFIG>\projects\C--Users-felip-OneDrive-Documents-Local-to-global-Bayesian\memory\MEMORY.md` and its linked notes. Preserve a sanitized, dated historical snapshot, then make a short current index with source/date/supersedes fields. Particularly important: `hq-thread-and-review-panel`, `model-roles-default`, `nots-ssh-via-owls`, `nots-no-hefty-data`, all `new-campaign-*`, `lowp-build`, `gh-bvs-migration`, theory/proof notes and benchmark history. Rewrite links in the current index only. Old memory is evidence, not a command to restart completed work. Do not copy credentials, OAuth state, `.t3`/Claude/Codex databases or entire global config trees. `.codex/smc_bvs_research` contains research scripts and notes as well as vendor/scratch content: classify it file by file, not as disposable tool state.

**Portable standing rules.** One dated area per campaign; few named reports; explicit writer ownership; exact-path briefs and acceptance checks; independent review of substantive work; no cache/library crawling. OPS alone accesses NOTS, serially through the configured alias, with batched commands and 15-minute backoff after failure. Keep the pinned login node; never modify live T3 recovery/state directories. Use Sapphire Rapids for timing comparisons, explicit Slurm memory, initialized modules, persistent jobs and saved logs/exit statuses. Preserve seeds, source/config hashes, launch commands, job IDs, environments and transfer receipts. Never expose sealed truth to fitting. Benchmark freeze remains until its own release condition is met. No method change through migration; no arbitrary tuning constants; LEVERS directions require Felipe's assent. The quantile Gamma(1, sqrt(n)) default belongs to quantile work and must not replace SMC-BVS's BB(1,p) model-size prior.

**Roles and authority.** Preserve the campaign's Opus manager, Sonnet/Haiku clerical/implementation, Sol independent-review and Terra skilled-worker roles; Astra for bounded adversarial/final review, Fable for delicate statements. Preserve the historical panel preference (Fable CP + CW and Astra reviewers), task-specific cost caps and cross-family proof review; do not automatically convene a full panel for file copying. General Codex preferences and older Claude-only pauses must be reconciled with the latest explicit campaign instructions, rather than silently carried forward as universal bans. HQ keeps the current 2–3 concurrent campaign-thread cap unless revised. Refer to protocol files actually used; `<PC_HOME>\.claude\CLAUDE.md` and `protocols/misc.md` are external dependencies today. File copying does not install providers, protocols or authentication on Owls.

**Unfinished scientific context to carry, not decide during migration:** empirical completion/reviews and any benchmark audit; final Part I wording; T37 literal versus toward-truth TD; theory adoption, venue and hard-target gates; G5/G9 and scoring disclosures wherever still unresolved; LEVERS approvals. P5 is already decided, not an open question. The meeting brief requested for Oct 30 is an HQ deliverable whose final disposition should be recorded. Future theory/Lean work need not finish before this migration; all current empirical work does.

## B. Target repository layout

Keep the five established top-level folders; add `Data/` for explicitly small inputs and minimal root entrypoints. Organize by purpose, then campaign/version. `Others/` becomes a documented legacy holding area, not the default destination. Preserve the existing five Git commits; no history rewrite or forced push.

```text
README.md                    navigation, current release, external data locations
AGENTS.md / CLAUDE.md         shared rules / Claude entrypoint
.gitignore / .gitattributes  lean storage; byte-preserving historical snapshots
Docs/
  HQ/                        CHARTER, STATUS, DECISIONS, BOOTSTRAP, WATCHDOG,
                             OPERATIONS, Memory/, Protocols/
  Methodology/               existing spec/master, with dated revisions
  Theory/                    existing proofs + missing reviews, inventories, selection
  Manuscripts/               paper/proposal sources, bibliography, selected final PDFs
  Campaigns/<date_name>/     charter, decisions, final status, run index, reviews
  Records/                   PATH_MAP, provenance/, Migrations/, existing records
  History/                   older campaign narratives and superseded unique documents
  Literature/                existing literature notes and bibliography index
Scripts/
  SMC_BVS/                   existing v2.1 retained; new releases/<version>/
  Benchmarks/                existing methods/scoring; distinct versioned additions
  Data_generators/            existing generators and dated extensions
  Exact/                     existing exact references
  Campaigns/<date_name>/     approved runner/job bundles, pilots, tests, scoring adapters
  Ops/                       quota, transfer, deployment and recovery tools
  Tools/                     ledger/manifest checks and relocation resolver
  Archive/<campaign>/<version_or_hash>/   every other unique deployed source version
Data/small/<dataset_id>/     explicitly approved small inputs/fixtures + provenance
Results/<campaign>/         final tables, figures, concise report + run references
Papers/                     existing subjects; curated licensed/open papers + index
Others/                     existing legacy content; no new catch-all material
```

Do not refactor frozen release internals during import. Preserve their relative paths. A bundle manifest can reconstruct a complete original tree from shared source files when exact-byte deduplication is worthwhile. Add portable wrappers separately; never “fix” a historical script in place. The existing v2.1 path stays valid, and the README names the accepted new release explicitly.

### Mapping and inclusion policy

**Include** = Git stores the bytes; **pointer-only** = Git stores location/hash/receipt and retrieval instructions; **exclude** = no repo content required (source retained externally, disposition recorded). A mixed folder gets per-file rows at execution; exclusions never authorize deletion.

| Source | Target | Decision and reason |
|---|---|---|
| OLD root README/PATH_MAP/CODE_LEDGER/LEVERS + `tools/` | `Docs/Records/{Migrations,provenance}/`, `Scripts/Tools/`; merged root README | Include originals and translated indexes; preserve old ledger claims |
| `00_Admin/` | `Docs/Records/Migrations/`, `Docs/History/HQ/`; current charter distilled into `Docs/HQ/` | Include approvals, boards, this plan and verification evidence; distinguish history from live state |
| `01_Methodology_and_Theory/Methodology`, master | `Docs/Methodology/` | Include unique sources, evidence and selected final PDFs; hash-match existing files before merging |
| `Theory_architecture_v3/`, `Next_steps_theory_20261013/` | `Docs/Theory/` and dated history | Include statements, proofs, reviews, rulings, failed attempts, inventories, selection and Lean source; exclude rebuildable caches |
| `Proposed_project/`, status manuscripts | `Docs/Manuscripts/`, `Docs/History/` | Include unique drafts/sources, bibliographies and substantive reviews; clearly mark superseded versions |
| `02_Experiments/A_*` through `F_*`, `H_*` | `Scripts/Archive/<campaign>/`, `Docs/{Campaigns,History}/`, `Results/<campaign>/` | Include all unique scripts/configs/pilots/tests and lightweight evidence; exact matches point to existing canonical repo bytes |
| `I/code/` including both ledgers, v2.2/v2.2.1, lowp, bench_lowp, scoring | `Scripts/SMC_BVS/releases/`, `Scripts/Campaigns/2026-10-28_New_Campaign/`, provenance | Include final and historically deployed variants; freeze accepted version before mapping |
| `I/conformance/`, `I/tests/`, `I/ops/`, future analysis/bench_audit | `Docs/Campaigns/2026-10-28_New_Campaign/`, `Scripts/{Campaigns,Ops}/`, `Results/2026-10-28_New_Campaign/` | Include reviews, job bundles, pilot recipe, tests and essential small evidence; bulk fixture/output trees pointer-only |
| `03_Literature/` | `Docs/Literature/`, `Papers/`, `Scripts/Archive/` | Include notes and unique research/precheck code; select key shareable PDFs; remaining library pointer-only; upstream code pinned by URL/commit/license, local patches included |
| `04_Reports_and_Presentations/`, actual root `Presentations/` | `Results/<campaign>/`, `Docs/History/` | Include lightweight reports/slides and sources; bulky media pointer-only |
| `90_Archive/` | `Docs/History/`, `Scripts/Archive/`, artifact catalog | Include unique research source/docs, dedupe exact copies; bulk archives pointer-only; not automatically discardable |
| Claude memory; `.claude/`, `.codex/` | `Docs/HQ/Memory/`, shared rule files, research tools/history | Include sanitized relevant content; exclude credentials, caches, tool databases and vendor installations |
| NOTS `/home/fb31/projects/BVS/New_Campaign/` | campaign scripts/bundles and records above | Include every deployed source/config/pilot; outputs pointer-only, keep existing NOTS paths |
| NOTS `/home/fb31/projects/BVS/SMC_BVS_v3/{core,deploy,prototype_profiling}` | existing Scripts when identical; otherwise `Scripts/Archive/SMC_BVS_v3/` | Include all unique source versions, regression/oracle/ops code and pilot recipes |
| NOTS `/home/fb31/projects/BVS/Benchmarks/`, `/projects/ml75/fb31/BVS/bench20261019/` | `Scripts/Benchmarks/`, `Scripts/Archive/bench20261019/`, campaign records | Include source, Slurm, scoring, manifests and pilots including dev/verify/run snapshots; frozen origins untouched |
| NOTS `/home/fb31/projects/BVS/releases/`, former `Others/`, `/projects/.../v3_profiling_20261020/` and old deploy | `Scripts/Archive/<campaign>/<version>/`, corresponding Docs | Include via surviving originals or verified NB mirrors; G/profiling cannot be recovered by scanning OLD alone |
| NOTS `/scratch/fb31/{BVS,New_Campaign,smcbvs_v3_deploy_20261022}/` and BVS MOVED pointers | campaign archive scripts + external artifact catalog | Include embedded source/pilots wherever still present; heavy results pointer-only; scratch never the sole preserved copy |
| NB `{NOTS_home,NOTS_projects_ml75,NOTS_scratch,Owls_home,_from_project_20261023,smcbvs_v3_deploy_20261022,v3_profiling_20261020}` | archive source/docs plus catalog | Include recoverable unique deployed code and lightweight records; bulk remains here |
| `<PC_NOTS_DATA>\New_Campaign` | artifact catalog; embedded source harvested | Pointer-only for bulk; this is the live campaign's actual download location, not NB |
| `<PC_HOME>\Documents\NOTS_Archives\old_owls`, other research tarballs | catalog; selected source members into archive | Pointer-only containers; inspect their member lists for missing scripts before declaring harvest complete |
| Libraries, environments, compiled caches, `.git`, tool state, unrelated Quant_Reg data | dependency/version recipes only | Exclude binaries/caches from import; preserve any project-specific dependency patches separately |

**Size rule and budget.** “Lightweight” means useful source/documentation or a curated small artifact, normally **≤5 MiB per file**, **≤25 MiB per small dataset**, with a declared purpose, provenance and no uncontrolled per-seed growth. Extension alone is not a size policy. Necessary unique source is never silently omitted for exceeding a threshold: audit embedded generated data, then resolve a recorded exception before acceptance.

Measured NEW-PC content is 637 files / **82.8 MB decimal (~79.0 MiB)** outside `.git`; Papers accounts for 65.6 MB and 53 files. Git's pack is ~59.7 MiB, explaining the roughly 141 MB overall footprint. Proposed total tracked-file budget: **250 MiB**: scripts/configs/tests 70, Docs/manuscripts/history 60, Papers 70, curated Results 30, small data 15, reserve 5. Include existing material in these allowances. Target `.git` below **500 MiB** after import; audit growth before accepting exceptions. These are planning limits, not measured post-dedup sizes. Retain existing paper history; additions should be a few key papers, with DOI/URL entries for the rest. Check repository visibility and redistribution permission before adding PDFs/private research records.

GitHub warns for files over 50 MiB and blocks files over 100 MiB; its guidance favors repos below 1 GB. Our budget is deliberately smaller ([GitHub limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), checked 2026-10-29).

**Proposed `.gitignore` additions** (merge with current rules; audit tracked files separately):

```gitignore
# Generated/runtime content
**/__pycache__/
*.py[cod]
**/.cpp_cache/
*.o
*.so
*.dll
**/.venv/
**/venv/
**/.Rproj.user/
**/.lake/
.Rhistory
.RData
*.rds
*.rda
*.tar
*.tar.gz
*.tgz
*.zip
*.7z
*.aux
*.toc
*.fls
*.fdb_latexmk
*.synctex.gz
*.log
*.out
!scenario_check.out
!scenario_check_lowp.out
/Data/raw/
/Results/raw/
/_staging/
/_runtime/
.env
.env.*
!.env.example
config.local.*
```

Do not ignore every `runs/`, `pilot/`, `build/`, `*.csv` or `*.json`: these already contain required scripts, run recipes and evidence. Explicitly allow reviewed small logs/fixtures at their exact paths when needed. A staged-file validator enforces size, credentials checks, allowed bulk locations and manifest coverage; `.gitignore` neither removes tracked files nor enforces size. Keep executable bits and LF for new shell scripts; set `-text` on byte-preserved historical source/evidence so Git/Windows normalization cannot change their recorded hashes. Never normalize the archived originals.

**LFS:** off by default. All scripts and pilot recipes use ordinary Git. LFS is not a route for simulation dumps, environments or run tarballs. Consider it only for an indispensable versioned binary after Felipe approves its storage/bandwidth cost and all clones support it. Otherwise use external artifacts plus hashes. Do not retroactively rewrite history merely to shrink existing PDFs.

## C. Harvest every NOTS script and pilot

“Ever deployed” requires historical evidence, not just current NOTS contents. Files already overwritten or deleted without a preserved version cannot be reconstructed from a checksum. Record such gaps explicitly; do not certify completeness while they remain unexplained.

1. **Build a source register after empirical completion.** Sonnet derives a root list from both ledgers, all `RUNS.md`/job bundles/Slurm scripts, PATH_MAP, relocation logs/MOVED pointers, NB manifests and memory. Include all roots in B, earlier benchmark runs such as `bench_20261008T020340Z`, release d2cc7bc2/v2, `v3_profiling_20261020`, and both old home and scratch layouts. Root aliases and relocation generations remain separate rows. Follow referenced BVS paths outside these roots explicitly; no whole-home/cache scan. Record missing, inaccessible and relocated roots, not an empty successful inventory.
2. **OPS makes one batched read-only inventory per session.** Read applicable remote AGENTS first. Enumerate approved BVS roots with caches/libraries pruned, but inspect their dependency patches/recipes. Capture path, bytes, mtime UTC, mode, symlink target, full SHA-256 and origin host. Never dereference arbitrary links into other projects; inspect targets within scope separately. No stage files in the 10 GB NOTS home: stream metadata and later selected bytes to Owls. Reading/copying frozen benchmarks is allowed; no rename/chmod/delete there.
3. **Find source by contents and references, not only suffix.** Include `.R/.r/.py/.sh/.bash/.sbatch/.slurm/.cpp/.h/.hpp/.stan/.jl/.lean`, notebooks, extensionless shebangs, Makefiles/Makevars, configuration, seed/unit tables, module/package records, JOB.md, acceptance/tests and submission helpers. Inspect every `runs/*/code`, `snapshots`, `release`, `dev_test`, `verify`, `pilot`, `smoke`, scoring and archived bundle. A pilot includes its complete executable recipe, settings, inputs or generator, resource requests, seed list, acceptance evidence and result pointer; failed pilots count too. Large pilot outputs remain external.
4. **Recover moved material before deduping.** OPS cleanup records say `v3_profiling_20261020`, home `Others`, and old deployment scratch were removed after verified laptop copies. Check NB's corresponding trees and `Owls_home/_migration_20261022` manifests. Inspect tar/zip member lists, then extract only needed members into a bounded Owls staging area after checking paths/symlinks for traversal. Check archives inside archives where deployment records refer to them. `OWLS_MIGRATION.md` records 2,805 `AUDIT_CLAUDE/A_CODE` scratch files deleted before archival: classify them as a known historical gap/duplicate claim, not recovered bytes, and verify whether any unique source is actually missing.
5. **Dedupe against bytes, then reconcile claims.** Compute SHA-256 of original bytes and compare against existing Git blobs, harvested files, root CODE_LEDGER, campaign ledger and SHA256SUMS/source manifests. Exact identical files can share canonical storage with many provenance rows. Same path/name with different hashes stays as separate versions. Truncated ledger hashes are hints only; retrieve the full original manifest or mark unresolved. Existing `ledger_check.py` accepts prefix/suffix matches and skips some remote/uncheckable rows: its exit 0 alone is insufficient. Preserve reported historical mismatches and review status; do not rewrite a ledger to make it green. No scientific equivalence inference from near-identical source.
6. **Write a machine-readable coverage manifest**, one row per source occurrence, including duplicate occurrences. Suggested `Docs/Records/provenance/nots_harvest.tsv` columns:

   `source_host, original_path, retrieved_from, archive_member, campaign, run_id, job_id, source_mtime_utc, observed_utc, bytes, mode, symlink_target, sha256, repo_path, repo_commit, ledger_ref, ledger_expected_hash, ledger_match, disposition, duplicate_of, review_ref, external_artifact_id, missing_reason`.

   Record manifests' own hashes in a separate import receipt (avoid a self-referential hash/commit). Keep full 64-hex digests. `repo_path` must resolve to stored bytes, not just a NOTS pointer, for every recovered script/pilot source. If deduplication changes physical layout, store a per-bundle path map and a deterministic reconstruction recipe; verify reconstructed bundle hashes on Owls without running the scientific workload.
7. **Close coverage independently.** Haiku enumerates inventory/count totals; Sol checks classification, archive coverage, full hashes and version collisions; Terra independently checks reconstructed bundles and source-to-run links. Every registered deployment must resolve to code, configuration, pilot, environment and evidence, or a specifically disclosed missing item. Reconcile counts as imported unique + duplicate aliases + external artifact pointers + excluded reproducible content + unresolved. Required unique source cannot be waived merely to fit the size budget. Astra reviews material residual gaps before Felipe accepts the handoff.

**After migration:** before each NOTS submission, commit/push the approved script/config bundle from Owls and record commit + source manifest in JOB.md and the run receipt. OPS verifies deployed hashes before `sbatch`. If emergency on-NOTS edits are unavoidable, capture every changed version back into Git with provenance before calling the run accepted. NOTS remains a deployment/compute location; Git is the durable source record.

## D. Cutover sequence — later only

Roles below are recommendations for a later execution, not agents launched by this advisor. **Felipe sign-offs are concrete acceptance gates**, not repeated permission for routine copying within an approved cutover.

| Step | Action and acceptance evidence | Lead / independent check / sign-off |
|---|---|---|
| 1. Close empirical work | Old HQ certifies conformance, final release freeze, pilot, PROD-L, PROD-H, P5 sensitivities, required repeats/analysis and any necessary benchmark audit complete. Match approved unit counts and failure accounting; accepted final reports/reviews; downloads and hashes verified; cleanup policy satisfied. No relevant queued/running Slurm job or writer remains. Preserve all open theory decisions separately. | Old HQ + OPS; Sol checks evidence, Terra ties counts; **Felipe confirms the break and transfer scope** |
| 2. Quiesce orchestration | Export schedule definitions/bindings/history and final task register; disable old watchdog and confirm no in-flight wake or auto-resume is executing. Settle finished delegates only after outputs are saved. Finalize boards, pending decisions and an explicit “frozen for migration” timestamp. Inventory other project schedules so a second watcher cannot restart work. | HQ; Haiku inventory; Sol checks no remaining writer |
| 3. Freeze source and rollback point | Snapshot manifests of OLD, memory, approved NOTS source and external data receipts. Record base commit/branch/dirty state for all three clones; preserve any uncommitted work without reset. Check second PC, Owls nested clone and any unpublished changes. Take an external read-only backup and Git bundle/tag as appropriate; use a migration branch in the correct Owls repo. | Sonnet execution, Haiku manifests; Sol checks baseline |
| 4. Harvest, classify, copy | Execute C; import allowlisted source/docs into staging and merge by full hashes. Every OLD file gets a disposition. Keep old evidence byte-identical; write translated path indexes and portable wrappers separately. Inventory external artifact accessibility, sizes, hashes, backups and custodians. No NOTS relocation is needed. | Sonnet; Haiku clerical; Sol reviews manifest/conflicts |
| 5. Verify the complete candidate | Compare original→staging→Git-blob hashes; count all dispositions and check omitted/oversized files. Verify papers/privacy, link resolution, case collisions, spaces, executable bits and LF behavior. Resolve stale absolute paths in active wrappers only. Run necessary portability/smoke checks on Owls with saved logs, environment and exit status; any substantive numerical workload stays remote under its existing rules, never on PCs. Use recorded evidence for large runs. | Sol + Terra independent of importer; Astra final judgment on gaps |
| 6. Commit and publish accepted import | Produce a short acceptance report with coverage totals, missing items, repo size, changed paths, test results and exact commit. **Felipe approves this concrete package**, including any exceptions. Commit/push migration branch, integrate normally without force, tag the accepted handoff and verify remote ref equals the accepted commit. Record final commit and receipt hashes. | HQ + Sonnet; Sol verifies remote ref; **Felipe package acceptance** |
| 7. Sync PCs | On each PC inspect branch/status first, preserve local-only work, fetch and fast-forward to accepted main/tag; reconcile divergent work explicitly. Verify HEAD and selected/full manifest checks as appropriate. Do not use OneDrive as synchronization for `.git`; only one Git writer per checkout. Check Windows case/path and shell behavior without running simulations. | Sonnet/Haiku; Terra compares receipts from both PCs |
| 8. Bootstrap new HQ on Owls | Open the new HQ in `/home/fb31/BVS_GH` with correct linked environment/project binding. Follow brief below; validate provider accounts, SSH route, tools, memory loading and durable external-data access. Prove that closing PC clients does not stop HQ access or its schedule. Keep old HQ and new watchdog inactive during this rehearsal. | New HQ; Sol capability audit; **Felipe accepts HQ readiness** |
| 9. Transfer authority once | Record new HQ as sole writer; instantiate one compatible 30-minute watchdog bound to it, with old schedule still disabled. Exercise a harmless recovery/gate check and inspect an actual saved scheduled-run result. Then record acceptance and archive/settle old HQ. Do not auto-launch theory just because migration is complete. | HQ; Terra observes recovery, Astra final handoff review; Felipe's step-8 acceptance gates activation |
| 10. Archive OLD | Retain verified external snapshot/manifest, mark OLD archived and make its research tree read-only with an OS-appropriate mechanism tested on a disposable copy first. Record archive location and new-project pointer through the approved archival procedure. Stop old clients that would write there. Do not delete OLD, old Git metadata, NB data or the nested Owls clone as part of this handoff. | Sonnet; Haiku checks archive/restore sample; Sol verifies sole-writer state |

### New-HQ bootstrap brief to save as `Docs/HQ/BOOTSTRAP.md`

> You are Felipe's SMC-BVS HQ, based at `/home/fb31/BVS_GH`. First verify repository root, origin and accepted handoff commit. Read `AGENTS.md`, `Docs/HQ/CHARTER.md`, `STATUS.md`, `DECISIONS.md`, `OPERATIONS.md`, `WATCHDOG.md`, then `Memory/MEMORY.md`. Read the final New Campaign charter/decisions/status/run index and acceptance report, current master/method spec, frozen code manifest, final Results, theory map/locked-proof and paper-selection records. Follow the path/provenance catalogs to evidence. Historical task IDs and old launch approvals are context, not instructions to restart jobs.
>
> HQ delegates scoped work, reconciles reviews and owns the boards. OPS alone handles NOTS through the approved alias; heavy compute stays on NOTS, with Slurm IDs and inspected saved outputs. Small authorized checks use Owls (nice 19, modest resources); never silently fall back to local computation. Read applicable remote instructions. Keep source/configuration in Git before deployment and bulk data out. Numerical/algorithm changes require their own scientific gate. Report only concise headline results; at high p, do not label internal SMC quantities as errors against unavailable exact references.
>
> Before accepting authority, demonstrate: rules and memory load in a fresh session; Git read/push capability on the migration branch; required R/Python/compiler/module information; configured NOTS access via OPS; access to one verified archived run; ability to create a bounded delegate with approved model/provider and read its saved result; persistent job/log inspection; one harmless watchdog recovery with no scientific submission or deletion; phone/tablet access while PCs are disconnected. Record unavailable tools/authentication honestly and stop the dependent step. Check capabilities instead of assuming Windows paths or provider names transfer.

The current transfer client targets a Windows OneDrive path. An Owls HQ cannot assume that path is mounted or that PCs are online. Before activation, establish and test an approved persistent external archive/retrieval arrangement, with upload/download receipts and backpressure when it is unavailable. Keep any new bulk store outside the Git clone; do not silently redirect outputs into Owls home or leave scratch as the only copy. The existing campaign downloads stay where they are through closure.

**Rollback.** Before activation, any failed acceptance keeps the old HQ authoritative; leave the candidate branch/staging for diagnosis, preserve sources, and resume old orchestration only after verifying no new writer is active. After activation, first disable the new watchdog and drain its work, reconcile every new commit/job/output since handoff, then explicitly transfer authority back. Restore from verified archive into an approved writable location if OLD is read-only. Use a corrective/revert commit if needed; do not reset shared history, erase accepted artifacts or resurrect old launch IDs. Never enable both watchdogs. Keep the old archive until Felipe separately approves its retirement.

## E. Safe preparation now versus work that must wait

**Safe now, with a narrowly scoped brief:** draft the new charter/bootstrap/rules and manifest schema inside this planning document; review current maps, saved receipts and Git metadata; identify historical roots, path dependencies, provider/tool prerequisites and size exclusions; dry-run classification that reads sources and writes only to an explicitly allowed planning output. A read-only NOTS listing is permitted by Felipe, but was unnecessary here: use existing OPS evidence and coordinate any later live inventory through OPS so it does not compete with the campaign. Do not treat a live inventory as a frozen acceptance manifest.

**This advisor's write authorization is only this file.** Separate draft files, harvest programs, test fixtures, hashes/log exports or charters must be authorized as later work; none were created in this turn.

**Must wait for all empirical work:** source/pilot harvest copies, any file move or archive packing, repo edits/branches/commits/pushes for the migration, changing code paths, rewriting memory, disabling the watchdog, final manifests, clone synchronization, new HQ activation, permissions changes or cleanup. Do not repair the nested clone, stale board wording, old memory or running campaign as a side effect of planning.

## F. Risks and questions for Felipe (eight)

1. **Offline data:** where may the always-on HQ durably retrieve/archive bulk data when both PCs are off? The present Windows transfer client needs a tested replacement route.
2. **Visibility:** is the GitHub repo intended to be private or public, and which manuscripts, reviews and paper PDFs may be pushed?
3. **Owls workspace:** approve `/home/fb31/BVS_GH` as authoritative; leave its older nested clone untouched pending a separate decision.
4. **Second PC:** confirm its clone path and preserve unpublished work before syncing; it was not inspected here.
5. **Missing history:** “ever deployed” may expose overwritten/deleted scripts. Require recovery or an explicitly accepted gap list, never a silent completeness claim.
6. **Budget:** accept the proposed 250 MiB tracked / 500 MiB Git targets, with specific exceptions if unique source cannot fit after deduplication?
7. **HQ capability:** provider authentication recently failed for Claude workers; validate both accounts/tools and the Owls→NOTS route before retiring old HQ.
8. **Authority and retention:** confirm the final HQ model/role policy and archive retention at acceptance; keep exactly one active HQ/watchdog and no automatic theory restart.

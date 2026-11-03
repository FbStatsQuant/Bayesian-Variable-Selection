# Push checklist (for Felipe, before `git push`)

Prepared 2026-11-02 by GH-PACK. Agents did **not** commit or push anything. **The repo is PUBLIC**: everything you commit is world-readable.

> **State on Owls at 2026-11-03 (after the post-campaign refresh).** HEAD is still `c4ef0dc` ("Transfer", the first snapshot, pushed 2026-11-02). Everything below is **uncommitted** in the working tree, about 278 files vs `c4ef0dc` (33 modified, 245 new). Commit and push them together (§5).
>
> **A. The reviewed fixes from 2026-11-02 (Sol R1/R2):**
> - 12 docs: `README.md`, `Docs/PLAN.md`, `Docs/THEORY.md`, `Docs/THEORY_PRIORITIES.md`, `Docs/SYNC_LATER.md`, `Docs/HQ/BOOTSTRAP.md`, `Docs/HQ/RULES.md`, and the one-pagers T01, T12, T21, T25, T26;
> - this checklist;
> - `Scripts/Tools/{prepush_scan.sh, PINNED_PATH_ALLOWLIST.txt, PREPUSH_REVIEWED.tsv}`.
>
> **B. The post-campaign refresh (2026-11-03, HQ D94; the empirical campaign is complete):**
> - **Results** (`Results/2026-10-28_New_Campaign/`, 118 new files): the final reports `L_20261102/{HEADLINE_L,EVIDENCE_L}.md` and `H2_20261102/{HEADLINE_H,EVIDENCE_H}.md`, the `H_existing_20261030` reports, aggregated tables, evidence tables, tie-outs (Terra), Sol reviews, and the PROD_L_BENCH acceptance summary. No per-fit or per-case data rows: Sol's narrow check removed 18 case-level files from the first refresh pack, and they are listed in `Docs/Records/DATA_INDEX.md`.
> - **Code** (`Scripts/Campaigns/2026-10-28_New_Campaign/`, 122 new + 15 modified):
>   - PROD_L_BENCH rev 2: ledger `da08f38c…`, the real-probe tests, Sol's D82 check;
>   - the analysis scripts (`analysis/…`, incl. `score_f3.R`, the pass-C merge, the ABESS exact-size check);
>   - the final ops records (`ops/FINAL_NOTS_STATE.md`, the PROD-H and F3 PROD completion reports, the deletion lists, the final OPS logs) and the Sol ops reviews (`review/`);
>   - new run-chain scripts and updated sshlock/pull tools;
>   - `verify_manifests.sh`, which now expects the PROD_L_BENCH rev-2 ledger.
>   - BENCH_F3_PROD is unchanged since the first snapshot.
> - **Docs:** the final `Docs/HQ/DECISIONS.md` (D1–D94) and the campaign records, `Docs/HQ/STATUS.md` (results summary), PLAN (empirical phase DONE), BOOTSTRAP (campaign closed; where the data lives), RULES/OPS_FACTS (the D76 two-lane SSH rule and closing lessons), THEORY_PRIORITIES §5 (the final evidence, replacing the preliminary section), the new `Docs/Records/DATA_INDEX.md`, and SYNC_LATER (marked done).
> - **Excluded on purpose:** one local VPN-watcher script that contained internal and home-network IP addresses.
>
> **Hygiene of the already-pushed content.** `PREPUSH_BASE=eb75737 bash Scripts/Tools/prepush_scan.sh` scanned everything this import added (1,287 blobs, through a temporary index). It printed **PASS**, so the pushed snapshot contains no secrets, e-mail addresses, private IPs or T3 ids, and no unlisted Windows paths. The only review issues in `c4ef0dc` were wording and accuracy fixes in the docs, which the second commit supersedes.

## 1. What the first import added (2026-11-02; most of it is already in `c4ef0dc`)

The 2026-11-03 refresh adds about 2 MB on top of this (part B above). Its verification is recorded at the end of §5.

| Area | Files | Size |
|---|---|---|
| `Scripts/Campaigns/2026-10-28_New_Campaign/` (vetted code, bundles, review records, verifier) | 948 | ≈ 9.4 MiB |
| `Scripts/Benchmarks/…` (16 missing ledgered files of the n = 200 study) + `Scripts/Archive/bench20261019/…` (20 earlier ledgered versions) | 36 | ≈ 0.2 MiB |
| `Scripts/Tools/prepush_scan.sh` + `PINNED_PATH_ALLOWLIST.txt` + `PREPUSH_REVIEWED.tsv` (the pre-push hygiene scanner, §2) | 3 | < 0.03 MiB |
| `Docs/` new documents (PLAN, THEORY, THEORY_PRIORITIES, SYNC_LATER, this file, HQ/, Campaigns/, Records/, History/HQ/) | ≈ 20 | < 0.5 MiB |
| `Docs/Theory/` imports (wave-1 proof sources, review records, paper selection, inventory, legacy pre-v3 proofs) + 39 one-pagers | ≈ 275 | ≈ 2.4 MiB |
| Modified | `README.md` (new short map; the old text is kept in `Docs/Records/README_v2_1_layout.md`) and `.gitignore` (additions only) | — |
| New | `.gitattributes` (`-text` on frozen trees so no clone rewrites line endings) | — |

**Size check (2026-11-02, after the import):** tracked 82.7 MB + new 12.8 MB ≈ **95.5 MB**, against the 250 MiB budget. The largest new file is 1.9 MiB (`jobs/PROD_L_BENCH/review/SOL_REVIEW_PRODLB_R2.md`), so no file comes near GitHub's 50 MiB warning.

**Integrity check (on Owls):**
- all 1,283 files are byte-identical to the stage (sha256);
- `sh Scripts/Campaigns/2026-10-28_New_Campaign/verify_manifests.sh` gives **23 PASS, 0 FAIL**.

Re-run it right before you push.

## 2. Hygiene scan (three independent scans: code inventory, theory drafter, manager)
- **Real secrets: none found.** That covers passwords, tokens, API keys, private keys, `ghp_`/`sk-`/`AKIA` patterns, email addresses and rice.edu addresses.
  - The only "password" hits are rules ("never store a password") and the security note in `Docs/PLAN.md` §4 item 18.
  - Key auth is mentioned by filename only (`~/.ssh/id_rice`); no key material.
- **Internal IPs.** One private login-node IP, in a non-pinned review record, was redacted. None remain.
- **T3 identifiers** (thread ids, task ids, scheduled-task ids, thread links) were removed from every non-pinned document.
- **Redaction.** Non-pinned Markdown documents were copied through a redaction step. It replaces personal Windows user paths with placeholders (`<OLD_ROOT>`, `<PC_NOTS_DATA>`, `<PC_NB_ARCHIVE>`, `<PC_HOME>`, `<PC_TEMP_PATH>`, `<PC_CLAUDE_CONFIG>`), removes T3 identifiers, private IPs and e-mail addresses, and shortens the Owls host name.
  - **All redactions together** across the three copy receipts: 477 replacements in 132 files (records 49/9, theory 165/66, code 263/57). This is the total over every category, not a count of Windows paths alone.
  - Code (`.R`, `.sh`, `.py`, …), manifests, `.tex` proof sources and every manifest-covered file were copied **byte-exact**, never edited.
- **What still exposes personal details, by design:**
  - **190 byte-exact files still contain Windows user paths** (username `felip`).
    - 63 of them are covered by a run-time manifest, so editing them would break the verification.
    - The other 127 are frozen-tree code and evidence (44 `.R`, 35 `.sh`, 23 `.ps1`, 19 `.py`, 3 `.txt`, 2 `.json`, 1 `.patch`) that are not hashed by a manifest; editing them would change what ran.
    - All 190 are listed in `Scripts/Tools/PINNED_PATH_ALLOWLIST.txt`.
  - **NOTS cluster paths** (`/home/fb31/…`, `/scratch/fb31/…`, `/projects/ml75/…`) appear in two kinds of file, and both expose your NetID `fb31` and the cluster layout:
    - about 214 frozen scripts, which need them to run;
    - 12 editable operational documents (`Docs/HQ/RULES.md`, `OPS_FACTS.md`, `BOOTSTRAP.md`, the campaign records), which keep them on purpose so the plan stays executable.

    The NetID is already public in the pushed v2.1 code (commit `eb75737`), and login-node names (`loginx2`) appear in the ops docs. Only the manifest-covered bytes are truly unredactable. The editable docs could be generalised, but any such change must be reviewed for usability.
  - If any of this is unacceptable, make the repo private.

**Re-run the scan before any push.** It checks exactly what the commit will publish:

```sh
cd /home/fb31/BVS_GH
git add -A                                   # define the commit boundary first
bash Scripts/Tools/prepush_scan.sh           # must end with: PASS  prepush_scan
```

What the scanner (v2) does. It needs bash, GNU grep/coreutils and git.
- **It reads only the git index, never the working tree:**
  - the staged blobs of every added, copied, modified or renamed file (`git diff --cached --name-only --diff-filter=ACMR -z`, NUL-delimited), including the scanner's own file;
  - the allowlist and the reviewed-exceptions file, from their index blobs;
  - index blob sizes, for every index entry.
- **It fails on:**
  - private-key blocks; GitHub, OpenAI or AWS key shapes; Authorization headers; Bearer tokens of 16 or more characters; password/secret/token/api-key assignments with **any** non-empty value;
  - e-mail addresses;
  - private IPv4 addresses (10/8, 172.16/12, 192.168/16);
  - T3 identifiers;
  - a Windows user path in a file not on `Scripts/Tools/PINNED_PATH_ALLOWLIST.txt`;
  - a changed blob containing NUL bytes (binary, so not text-scannable);
  - a changed blob over 5 MiB, any index blob over 50 MiB, or an index total over 250 MiB (262,144,000 bytes);
  - unmerged index entries;
  - any read or tool error, which counts as a failure, never as clean.
- **Reviewed exceptions** live in `Scripts/Tools/PREPUSH_REVIEWED.tsv`. Each line is a path, the sha256 of the exact staged bytes, the category (SECRET or BINARY) and a reason. Any change to the file re-triggers the check. This import has 8:
  - the 7 synthetic `.rds` test fixtures (BINARY). They were decompressed and checked: no paths, e-mail addresses or IDs;
  - 1 false positive (SECRET), the prose "checked token by token", followed by a colon and a count, in a T03 review summary.
- **Limit.** Binary formats are not content-scanned; they must be reviewed and listed. Adding an allowlist or exception line is a review decision, so check it against the byte-exact-copy policy.
- **NOTS paths** are only reported.
- If the index changes, run the scanner again.

The redaction tool for the SYNC_LATER refresh is the one this import used (old project, `GH_PACK/tools/redact_copy.py`; it writes a receipt with replacement counts). After a refresh, regenerate the allowlist only for files that are byte-exact frozen copies.

## 3. Excluded, and why

| Excluded | Why |
|---|---|
| `conformance/work/` (154 MB regression harness + outputs), `bench_audit/work_*`, `scratch`, `mgr_checks` | Bulk evidence; the verdicts are kept (REGRESSION.md, reviews) |
| `code/bench_v2/` generated data (`repro` `.rds`, `controlled_*` data, logs, Sol fixture mirrors), ≈ 62 MB | Generated outputs; code, specs, tests and reviews are kept |
| `code/core/v2_1_baseline/` | Byte-identical to the repo's `Scripts/SMC_BVS/` (24/24) |
| `ops/evidence/`, `ops/transfer/receipts/`, transient run logs and outputs, `__pycache__`, `.cpp_cache` | Bulk, run receipts, caches |
| Live OPS progress logs (`OPS*_PROGRESS.md`, `OPS_LOG.md`, `DISK_LOG.md`) and the analysis folders | Being written by running threads; see `Docs/SYNC_LATER.md` |
| Bulk production data and results (inputs, fits, enumerations, benchmark outputs) | Never in Git. They go to the git-ignored `_data/` on Owls after the campaign |

**Small exceptions that are included on purpose,** because they are manifest inputs or vetting evidence:
- 7 tiny `.rds` test fixtures (BENCH_F3_PROD tests);
- 17 enumerator test logs and 2 `.out` files (ledgered in the LOWP block);
- 3 CONF_NOTS_IDENTITY gate logs;
- the pilot summary CSV/MD files;
- the test fixtures of each bundle.

`.gitignore` re-includes the first three groups by narrow negation rules.
| Claude memory, `.claude/`, `.codex/`, T3 state, thread transcripts | Private tool state. Distilled into `Docs/HQ/RULES.md` and `OPS_FACTS.md`. Thread text may contain secrets (§4) |
| Superseded proof drafts, LaTeX build files | Clutter; the final versions and review records are kept |

Full per-file lists are kept off-repo in the old project's `00_Admin/GH_HANDOFF_20261029/GH_PACK/` (`code_inventory/EXCLUDED.tsv`, `COPY_LIST.tsv`, `tools/*_RECEIPT.tsv`).

## 4. Your decisions before pushing
1. **Public visibility.** This adds unpublished material to a public repo:
   - unpublished proofs and their reviews;
   - consultant reviews of the paper plan;
   - the status briefing;
   - decision logs.

   The earlier commits already published the v3 theorem statements and some proofs. Either push as is, drop some folders, or make the repo private (open decision, handoff gap list E13).
2. **Security.** A NOTS password appeared in an old HQ transcript (2026-10-22). Change it if you have not; nothing in this import contains it.
3. **Optional `Scripts/Archive/bench20261019/`** (20 earlier ledgered benchmark file versions, for provenance). Keep or drop.

## 5. Push steps (run yourself on Owls or a PC clone)
```sh
cd /home/fb31/BVS_GH
sh Scripts/Campaigns/2026-10-28_New_Campaign/verify_manifests.sh   # expect: SUMMARY: 23 PASS, 0 FAIL
git status --short | head -40                                       # only the additions above + README/.gitignore
git add -A
bash Scripts/Tools/prepush_scan.sh                                  # expect: PASS; also prints the index total (≈ 95.5 MB)
git commit -m "GH-PACK: reviewed doc fixes + pre-push scanner; post-campaign refresh (final results, records D1-D94, PROD_L_BENCH rev2, analysis scripts)"
git push origin main
```
The nested older clone `Bayesian-Variable-Selection/` is excluded through `.git/info/exclude` and is not added.

**Windows PCs.** The longest repo path is 153 characters, which fits under Windows' 260-character limit at the current PC clone location. If a clone fails with "Filename too long", run `git config --global core.longpaths true` once and pull again. `.gitattributes` keeps the frozen trees byte-exact, so `verify_manifests.sh` passes on every clone.

**Scanner tested** (2026-11-02, scratch repos; see the old project's `GH_PACK/review/SCANNER_TEST.md`):
- the clean tree passes;
- planted canaries are caught: secrets, e-mail, IP, T3 id, Windows path;
- each of Sol's narrow-check bypass cases (B1–B5) now fails as it should:
  - a secret in the scanner itself;
  - an unstaged allowlist edit;
  - an oversized index blob with a small working copy;
  - a short password and a NUL-containing blob;
  - an injected grep error.

The v2 fixes were tested by the manager. Under the D53 two-round limit they were not re-reviewed by Sol, so run the scanner on Owls before pushing; it must print PASS.

**Post-campaign refresh: verification (2026-11-03, on Owls).** It was transferred as a delta pack of 288 files, then corrected after Sol's narrow check (`SOL_SYNC`: ACCEPT WITH FIXES). The correction removed 18 case- and fit-level files and rewrote four statements. The final refresh is 270 files (29 replaced, 241 new), then checked on Owls; the results (sha256 match, `verify_manifests.sh`, the scanner with a temporary index) are recorded in GH-PACK's verification log, `transfer/owls_verify_5.txt`. Final result: all 270 files match by sha256; `verify_manifests` 23 PASS, 0 FAIL; the scanner PASSES on all 278 pending files; the index total would be 97,073,850 bytes. The `Docs/SYNC_LATER.md` refresh is therefore done. A single commit of everything pending (§5) brings GitHub up to date.

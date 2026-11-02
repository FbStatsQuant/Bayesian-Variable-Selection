# Independent review: D31 /home/fb31/backups

**Verdict: ACCEPT WITH FIXES. Erasure remains blocked until the findings below are resolved.**

Reviewer: Sol 6.1, independent reviewer. Local verification completed 2026-10-30T18:15:30Z. Scope: review only; no SSH, no remote execution, no deletion. Only this review file was written.

Authority reviewed: HQ D31 as supplied by Felipe permits archive, verification, independent review, then erasure; excludes program installs in use, credentials, configuration, and open files. This review covers only the two named tarballs and removal of their empty parent directory.

## 1. Archive completeness and identity: PASS

Archive root: `<PC_NOTS_DATA>\NOTS_home_archive\backups_20261030`.

I independently read both complete local files with PowerShell `Get-FileHash -Algorithm SHA256`. The recursive inventory under `backups` contains exactly two regular files, no additional entries, and no reparse points. Both filenames, byte sizes, and SHA-256 values agree with the remote listing; both hashes and relative paths also agree with the two-line `REMOTE_SHA256.txt`.

| Filename | Bytes | Independently computed SHA-256 |
|---|---:|---|
| Extreme_individual_pkgs_before_tau90_93_20261021.tar.gz | 47,930,054 | c9d0f4614ea15cb70f78a2981d5b6e9584251b83c0fec189f96177927c2327d2 |
| Extreme_Joint_Sampler_before_b0005_15k3k_20261022.tar.gz | 46,774 | c56bb68ccf6a5181ded7c4aff747cb920096f7d68989c17cc3655dec59b3ce9e |

Total: 47,976,828 bytes. Exact inventory and manifest assertions completed successfully (exit 0). The listing reports 46,860 KB on disk, exceeding the stated approximately 25 MB requirement; actual guard headroom must still be checked after any authorized erasure.

Read-only `tar -tzf` succeeded for each archive: 4,348 and 27 members respectively. Member names show historical Extreme_Individual / Extreme_Joint_Sampler source, scripts, and experiment artifacts. These are backup containers rather than active installed package directories. The joint backup includes a historical `config.R`; preserving it inside the verified laptop backup does not constitute deleting the active configuration file. A narrow credential-name screen returned no candidates; this is not a content-level secret audit.

The archive script streams the entire `backups` directory to the laptop and verifies the manifest there. Independent verification above establishes completeness against the supplied remote inventory despite the script's limited error handling in its listing stage.

## 2. D31 category: backup category PASS; open-file exclusion UNRESOLVED

The recorded remote inventory at 2026-10-30T18:13:46Z contains exactly the two regular tarballs, owned by fb31, and zero symlinks. Names, ages, and archive members support the stated historical package/experiment backup category. There is no evidence these two container files are program installs, active credential files, or active configuration files.

**F1 — Blocking: the supplied open-file check does not establish the full exclusion.** The listing's empty `== open (this node)` section supports only that no matching descriptor was reported by its loginx2 scan. The script suppresses errors from process ownership and descriptor inspection, so unreadable inspections are not distinguished from absence. It also does not establish absence of open references on other NFS clients. The previous reviews recorded in CLEANUP_LOG.md identify this same shared-home limitation; no explicit D31 exception accepting it was supplied here. The scan is also a point-in-time observation, not a delete-time check.

Required fix: before erasure, provide a fresh, fail-closed open-file assessment covering relevant clients, with inspection failures accounted for and continued non-use through unlink, or obtain explicit authority accepting the stated residual limitation. A failed or unreadable inspection must not be recorded as a negative result. This reviewer made no remote probes.

## 3. Planned erase: bounded design, incomplete executable specification

**F2 — Blocking: the log contains a command template, not the exact planned command.** Its text is `printf '<sha>  <file>\n' x2` and `rm -- <file1> <file2>`. Therefore the concrete hash inputs and deletion operands cannot be independently checked as an executable command. The literal template must not be treated as reviewed execution text.

Required fix: record the final literal command or executor before erasure, containing exactly the two filenames and two hashes in the table above. Retain `&&` between successful directory change, verification of both hashes, and deletion; use a fixed two-file `rm --` operand list without globs, recursion, or paths derived from unvalidated output. Bind execution to the intended real `/home/fb31/backups` directory and confirm the targets remain regular, non-symlink files. The old inventory does not establish those properties at execution time. Address F1 in the same pre-unlink procedure. Any changed executor requires review of its concrete text.

For the intended structure, both hashes must pass before either unlink; fixed filename operands bound `rm` to those two directory entries. `cd / && rmdir /home/fb31/backups` cannot recursively remove contents and fails if additional entries remain. A failed `rmdir` after successful file deletion is a partial result to report, not a reason to broaden deletion. Hash gating alone does not prove a file is closed or prevent concurrent path replacement; this review makes no such guarantee.

## Evidence binding

SHA-256 of files read during this review:

| Evidence | SHA-256 |
|---|---|
| evidence/ops6_d31_backups_listing.txt | 657cdd1967b8a0535b1345f74cd7755b2870f2b3e23beb0d79a02cf71fa22834 |
| scaffold/d31_backups_archive.sh | 4c6e4059ecdcb08b895463a7314f5cf78f862c02575f04c0daafdf34703e6fdb |
| CLEANUP_LOG.md at review time | 970a0d36bf76eaf33349117a3853363df806c63f09b7de754792ee91c4c9ff6e |
| Laptop REMOTE_SHA256.txt | 373affa5dd77420b7da9c65fc1b4ee4d4c4547503b5e1734a4bca2a37a781f5d |

Archive identity is accepted. Unconditional deletion approval is withheld pending F1 and F2; no broader deletion is covered.

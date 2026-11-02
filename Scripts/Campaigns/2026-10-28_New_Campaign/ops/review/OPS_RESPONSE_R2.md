# OPS response to Sol review round 2 (`SOL_REVIEW_CLASS_A_R2.md`, APPROVE WITH FIXES)

Date: 2026-10-29 02:02Z.

## F1 / N1: manifest failure propagation (fixed)
- `remote_pack.sh` now builds the manifest in a **separate bash process** (`bash remote_pack.sh _inner …`) under `set -euo pipefail`. This keeps errexit active even though the caller tests the status.
- Every enumeration (other types, owners, mount comparison, bad names, file list, links, sizes) goes to a temp file, so no producer runs inside a command substitution. The file count must equal the hash count.
- Delete mode checks explicitly:
  - the temp-dir creation;
  - the manifest digest;
  - the file and link list builds (`grep` exit 1, meaning no lines, is accepted);
  - `du`, `cd`, each `rm`, directory pruning, the final enumeration and `rmdir`.
- Any failure gives exit 4 (nothing deleted yet) or exit 5 (partial; leftovers kept).

## F2 / N2: failed squeue (fixed)
- `remote_pack.sh` captures `squeue`'s own exit status. A non-zero status refuses deletion (exit 4), and only an empty, successful result is accepted.
- `verified_delete.sh` is unchanged. Its standalone assignment under errexit already exits on failure, and the test confirms rc 1 with the target kept.
- **Fault-injection evidence** (`evidence/tooltest4.sh`, `evidence/tooltest4_raw.txt`, 2026-10-29 02:01Z, tools re-staged; the remote `sha256sum -c` against `evidence/staged_tools.sha256` is OK for all three):

| Case | Result |
|---|---|
| failing squeue → delete | rc 4, target kept (5 entries) |
| failing find → manifest | rc 2, 0 stdout bytes |
| failing find → delete | rc 4, kept |
| failing sha256sum → manifest | rc 2, 0 bytes |
| unreadable file → manifest | rc 2, 0 bytes |
| unreadable file → delete | rc 4, kept |
| empty dir → manifest + delete | rc 0 |
| normal delete | rc 0, gone |
| verified_delete with failing squeue | rc 1, kept |

- After that, a third dummy end-to-end `nots_pull.py --delete` with the final `remote_pack.sh` passed: 2/2 files verified, 1 link, remote deleted (`OPS_LOG.md`).
- Final staged sha256: remote_pack.sh `16d21e07…1965`, verified_delete.sh `aeb43c40…a6a`, guard.sh `53103663…de3e`.

## F3: host authorisation (OPS decision, flagged to HQ)
- Felipe's brief to OPS says: "Use `ssh nots`, which is pinned to loginx3 with key auth."
- The `Host nots` entry in `~/.ssh/config` was deliberately re-pinned on 2026-10-28 to **loginx2** (<internal-ip>). That is where the only live T3 server runs. All login nodes share `~/.t3` over NFS, and the config warns that pointing at another node caused repeated `ServerAlreadyRunningError`.
- The charter's purpose for the pin is a single login node, the same one T3 uses. That node is now loginx2.
- Switching OPS to loginx3 would split our sessions across two nodes and goes against the config's own warning. Editing `~/.ssh/config` is outside OPS's remit.
- **Decision:** OPS keeps using `ssh nots` exactly as configured, as the brief instructs. That is one node (loginx2), and nothing else is changed.
- **HQ action:** update CHARTER §3 to say "`Host nots` (currently loginx2, the T3 node)", or tell OPS otherwise.

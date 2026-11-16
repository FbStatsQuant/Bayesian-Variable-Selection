# OFFLOAD — continuous transfer crew: NOTS → Owls → desktop (primary) + laptop (mirror)

v0.1 design, 2026-11-15. Owner rule (via HQ): pump data off NOTS all the time; each PC has 1 TB; keep our data under
~70% of each PC's disk; calm connections (§12.7); volumes in the daily machines line. Owned by the Engineering
transfer crew.

## Principles
1. **Results of record leave NOTS scratch within 24 h of a run finishing** (the hard limit stays 7 days; the CRC purge is
   14 days on atime).
2. **Checksums travel with the data.** SHA-256 manifests are computed on NOTS, verified at every hop, and logged.
3. **NOTS scratch is freed only after a verified copy exists on Owls AND on the primary PC (desktop).** The laptop mirror
   does not gate freeing. Freeing is done by the Engineering crew from Owls, never by a PC script.
4. **One transfer at a time**, over the one multiplexed connection; `nice`; no parallel streams.
5. **Pull model**: the PCs initiate their copies, because NOTS and Owls cannot reach the PCs.

## Flow per run
| step | where | what | record |
|---|---|---|---|
| 1 | NOTS job (last step of every job script) | write `SHA256SUMS` over the run's outputs of record, then `OFFLOAD_READY` (run_id, bytes, file count, manifest hash) in `scratch/runs/<batch>/<run_id>/` | job log |
| 2 | Owls crew (hourly, one ssh call) | list `OFFLOAD_READY` runs not yet in the ledger; `rsync -a` each into `SMC_Engineering_Department/records/<batch>/<run_id>/`; verify with `sha256sum -c`; ledger row `owls_verified` | `crews/offload/ledger.tsv` |
| 3 | desktop (primary) | `pull.ps1 -SshHost owls -Remote …/records/<batch>/<run_id> -DestRoot <desktop path>` (scheduled, or triggered by the crew). Verify with Get-FileHash; write `verified.json` | PC log + ledger `desktop_verified`, read back by the crew |
| 4 | laptop (mirror, when online) | the same as step 3 with the laptop's `-DestRoot` | ledger `laptop_verified` |
| 5 | Owls crew | when `owls_verified ∧ desktop_verified`: `rm -rf` the run's outputs of record on NOTS scratch (one ssh call); keep a tombstone `OFFLOADED` file with the manifest hash and destinations; INDEX row | ledger `nots_freed` |
| 6 | Owls crew | Owls staging is trimmed when `desktop_verified ∧ laptop_verified` (or 30 days after `desktop_verified`), so Owls NFS holds a bounded working set (target ≤ 200 GB) | ledger `owls_trimmed` |

Never offloaded or freed:
- run directories of queued or running jobs;
- frozen code;
- inputs that a resume needs (checkpoints of an unfinished run).

## Disk guards
- **PCs.** Before each pull, the script reads the destination drive's free space. It refuses if our data would exceed 70%
  of the drive (≈ 700 GB of 1 TB) or leave < 15% free. It logs the refusal; the crew reports it.
- **Owls staging.** At most 200 GB; above that, pulls to the PCs are prioritised and new NOTS offloads wait (scratch
  still has 7 days of room).
- **NOTS.** The daily crew lists every run of record older than 24 h not yet freed, and alerts at 5 days.

## Volumes (planning)
- G0 ≈ 1 GB.
- Rung A ≈ 50–100 GB (stores and RB arrays per fit; laws and summaries are small).
- 10⁵ ≈ 50 GB.
- 10⁶ ≈ 5–8 GB per fit (merged store + law + PIPs + RB arrays). Island files are not kept: they are rebuilt from
  manifests if needed.
- Total ≈ 200–300 GB, i.e. ≈ 25% of one PC.

## Daily machines line (added)
`offload: N runs / X GB off NOTS today; pending K (oldest h); desktop D GB (u%); laptop L GB (v%, last seen …); Owls
staging S GB.`

## To build (crew, Engineering)
- `crews/offload/offload.sh` (Owls; steps 2, 5, 6; the ledger) and an hourly schedule on Owls.
- The job-script epilogue (step 1), added to every Engineering sbatch template (WP5 driver).
- `pull.ps1` with `-DestRoot`, `-SshHost owls|nots-transfer` and the disk guard (laptop: in setup now; desktop: when its
  path arrives).
- **Owner OK needed for:** a scheduled task on the desktop, and on the laptop, that runs `pull.ps1` hourly (a Windows
  Task Scheduler entry is a settings change on his machines). Alternative: the crew triggers a pull through T3 when a run
  is ready.

# New_Campaign (NOTS home): layout

Owner: New Campaign OPS thread (2026-10-28). Charter: laptop `ROOT/02_Experiments/I_2026-10-28_New_Campaign/CHARTER.md`.
This folder holds code, inputs, manifests, logs and small summaries only. Hard ceiling: 7 GB, checked by `code/ops/guard.sh` before every submission.
Bulky outputs go to `/scratch/fb31/New_Campaign/` (transient), are downloaded and sha256-verified, then deleted.

| Folder | Holds |
|---|---|
| code/ | the campaign code tree as deployed; `code/ops/` has guard.sh and the transfer helper |
| inputs/ | generated datasets and designs that runs read |
| manifests/ | run manifests (unit lists, seeds, hashes) |
| runs/ | one folder per run_id: job scripts, JOB.md, slurm settings |
| results/ | small per-run summaries only (bulky outputs live in scratch) |
| logs/ | slurm and runner logs, pruned once a run is downloaded |

Mirrors: `/scratch/fb31/New_Campaign/` and laptop `<PC_NOTS_DATA>\New_Campaign\` use the same subfolder names.
Nothing else may be created under `/home/fb31/projects/BVS/`.

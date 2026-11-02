# Remote execution record

All numerical workloads ran at `/home/fb31/theory_campaign/A-REV8` on Owls. Local Python was used only to export Git sources and hash files, not to compute numerical results.

Before writing remotely, checked `/AGENTS.md`, `/home/AGENTS.md`, `/home/fb31/AGENTS.md` and searched `/home/fb31/theory_campaign` and `/home/fb31/BVS_GH` for AGENTS.md; none were found in these locations. A broad initial home-parent search was unnecessary and was not used as evidence of repository instructions.

Launch (each attempt):

```sh
cd /home/fb31/theory_campaign/A-REV8
nohup bash scripts/run.sh > results/launcher.log 2>&1 < /dev/null &
echo $! > results/pid.txt
```

Persistent process IDs and inspected outcomes:

- 2575511: system Python lacked numpy, exit 1; logs retained under `results/failed_system_python/`.
- 2576043: scientific interpreter ran the calculations but JSON serialization rejected numpy int64, exit 1; source, raw outputs and logs retained under `results/failed_serialization/`.
- 2576341: serialization fixed; all calculations rerun with the same seed; exit 0. Saved `results/environment.txt`, `finished.txt`, `run.log`, `exit_status.txt`, `pid.txt` and `SHA256SUMS` inspected. Python 3.12.15 via `/home/fb31/envs/dl/bin/python`; one thread. No scheduler was used: this modest job was a detached process.

`results/input_*.npz` store exact sufficient statistics and signal configuration; `population.json` stores all heterogeneous population parameters. The script fixes seed 20261102, all dimensions and all simulation settings. `sources/manifest.json` preserves source heads and hashes. `results/SHA256SUMS` is the remote output manifest. Run timestamps and environment are recorded by the launcher, not inferred from this report.

The system-Python failure did not trigger local fallback. The second failure did not count as a successful run. Only the final saved exit-zero outputs support REVIEW.md.

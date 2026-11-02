# A-REV3 review record

Independent referee: GPT-6 Astra. No helper or W5-VMASK findings were used.
Review writes are confined to this directory. No locked result is edited or promoted.

Input heads inspected:
- W3-PXN: 4aebea3bf003f5f3c0c7239a24c824ec2d2aa574
- W4-SHARE: 0d3f3fe581b72186c0c9bffe701950044cc7a464
- W5-VMASK was pushed at 4e41b974e0b8f954eb6adaf6be76d351821fdab0; only its ref was read.
- Local baseline: 816ec72ed40a35a0bff620ccb3170d947008cebe

Remote execution: /home/fb31/theory_campaign/A-REV3 on owls.stat.rice.edu.
Read /home/fb31/AGENTS.md (empty); no instructions in /AGENTS.md,
/home/AGENTS.md or /home/fb31/theory_campaign/AGENTS.md were found.
No local numerical workloads. All numerical jobs use one BLAS/OpenMP thread.

Launch: ssh owls 'cd /home/fb31/theory_campaign/A-REV3; nohup bash scripts/run.sh </dev/null >launch.log 2>&1 & echo $!'
First PID 2507588: system python3 missing NumPy; all three programs exited 1.
Second PID 2508171: /home/fb31/envs/dl/bin/python; all three programs exited 0.
The second shell runner ended with a CRLF blank-line error after saving successful
program exit statuses. Its original log is retained; a clean LF rerun follows.
The reproducibility scripts imported from W3/W4 are identified by name in REVIEW.md;
validate.py is referee-authored. Snapshots are UTF-8 text exports, not byte-identical git blobs.

Clean LF runner PID 2509198 completed on 2026-11-02 at approximately 19:21 UTC.
Inspected process status: PID no longer present. Saved component exit statuses:
w4=0, w3=0, validate=0, independent=0; the runner exits their bitwise OR (0).
Environment: Python 3.12.15, NumPy 2.5.4, SciPy 1.18.1, Linux x86_64.
`results/run.txt` is the complete successful log; `run_crlf.txt` preserves the
preceding runner's log. `results_failed_system_python/run.txt` preserves the failure.
`results/source_snapshot.tar.gz` preserves exact executed source bytes, including
line endings, independently of git text normalization. `independent.py` is also
referee-authored; its SVD score check is separate from the original Gram solver.

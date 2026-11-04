# ABL-CONF operational deviations (not rule changes)

- 2026-11-04 01:25 UTC: all three worker jobs were killed (rc 143) when the launching agent's session ended: T3 stops the agent's systemd scope, and `setsid` does not escape it. 4 reference fits had completed; 6 in-progress reference fits were released and re-run. No test fit had started.
- 01:29 UTC (HQ): `scripts/launch.sh` patched to launch each job as its own `systemd-run --user` unit (original kept as `scripts/launch_setsid_orig.sh`); `relaunch.sh` + one extra `launch.sh 1` restarted 3 jobs × 2 workers. Queue, seeds, cap, reference and rule unchanged. New ETA ≈ 11:30–12:00 UTC.

# Numerical audit record

All computation ran on owls.stat.rice.edu under /home/fb31/theory_campaign/A-REV4. The local laptop extracted source and computed file hashes only. Jobs were launched with nohup and independent log/exit/timestamp files; no scheduler was used. At most two single-process workloads overlapped. Each completed PID was checked with ps and the saved exit status read. No run remains active.

| Job | PID | Exit | Inspected evidence |
|---|---:|---:|---|
| Independent algebraic checks | 2507523 | 0 | results/results.json, remote_sha256.txt, start/end/environment.txt |
| BOOK initial attempt | 2508065 | 1 | book_stderr.txt: missing mpmath; empty result retained |
| BOOK 50-digit reproduction | 2508546 | 0 | book_retry_results.txt ends ALL CHECKS PASSED; mpmath==1.3.0 |
| Independent proxy experiment | 2508672 | 0 | nm_results.txt, nm_sha256.txt, nm_start/end.txt |

Launch commands (run after SSH into the recorded directory):

```sh
nohup sh run.sh > launch.log 2>&1 < /dev/null & echo $! > pid.txt
nohup sh -c 'date -u > book_start.txt; sha256sum book_reproduction.py > book_sha256.txt; python3 book_reproduction.py > book_results.txt 2> book_stderr.txt; echo $? > book_exit.txt; date -u > book_end.txt' > book_launch.log 2>&1 < /dev/null & echo $! > book_pid.txt
python3 -m venv venv
venv/bin/pip install mpmath==1.3.0 > dependency_install.log 2>&1
nohup sh -c 'date -u > book_retry_start.txt; venv/bin/pip freeze > book_environment.txt; venv/bin/python book_reproduction.py > book_retry_results.txt 2> book_retry_stderr.txt; echo $? > book_retry_exit.txt; date -u > book_retry_end.txt' > book_retry_launch.log 2>&1 < /dev/null & echo $! > book_retry_pid.txt
nohup sh -c 'date -u > nm_start.txt; sha256sum nm_check.py > nm_sha256.txt; python3 nm_check.py > nm_results.txt 2> nm_stderr.txt; echo $? > nm_exit.txt; date -u > nm_end.txt' > nm_launch.log 2>&1 < /dev/null & echo $! > nm_pid.txt
```

The uploaded run.sh had its Windows CRLF removed before launch. Python source and original reference snapshots were not edited remotely. SOURCE_MANIFEST.json records source SHA-256; remote_sha256.txt records uploaded copies. book_sha256.txt and nm_sha256.txt pin the additional scripts. Python is 3.9.25, with OS details in environment.txt. Seeds: 20261102 for independent checks/proxy draws; BOOK is deterministic finite-law propagation (its source records seed 0).

BOOK reproduction: primary PIP bias -0.1739741778498905; pooled-product relative bias -0.13171639499258733; covariance closed-form residual 5.13e-49. Evidence and island-product identity residuals are approximately 2.11e-50 and 1.60e-50. These match the claimed mechanism; machine-small residuals are not rigorous intervals. The guard threshold table is fully retained. No production guard replay or VAL-FP validation was attempted.

The independent checks reproduce the W2 counterexample with discrepancy -0.04337903089108747, and the four-island covariance law has pooled bias 0.1875=-3 Cov/4. The 101-temperature finite grid agrees with the endpoint deficit; the proof, rather than this grid, establishes the continuum identity. W1's minimum d is within floating-point rounding of zero.

The proxy experiment uses exact two-dimensional sufficient-statistic formulas and 256 Gaussian replicates per n. Its saved aggregate outputs corroborate the analytic non-tight remainder counterexample and the local-proxy/global-posterior distinction. No confidence claim or asymptotic theorem is inferred from those finite runs. Individual original replicates were not retained by that first script; a provenance-complete rerun with saved replicate statistics is recorded below if present. The proof of ERROR does not depend on the simulation.

Raw-statistic rerun: PID 2511056, exit 0, process confirmed finished. nm_raw_check.py repeats the same seed/formulas and saves all 768 replicate posterior/start probabilities and proxy log Bayes factors to results/nm_raw.json; timestamp, hash, stderr and summary files are retained. Launch:

```sh
nohup sh -c 'date -u > nm_raw_start.txt; sha256sum nm_raw_check.py > nm_raw_sha256.txt; python3 nm_raw_check.py > nm_raw_summary.txt 2> nm_raw_stderr.txt; echo $? > nm_raw_exit.txt; date -u > nm_raw_end.txt' > nm_raw_launch.log 2>&1 < /dev/null & echo $! > nm_raw_pid.txt
```

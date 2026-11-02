D63 — RESOLVED

Independent Sol narrow re-check, 2026-11-02. Scope: HQ D53/D63 only; no new full review and no reopening of N1/N2 or other dispositions. PL below means CAMP/jobs/PROD_L. The bundle was read-only; this verdict is the only campaign write. No SSH/network or sealed campaign truth/holdout content was accessed.

Evidence: retry-record bound

- PL/make_p5_list.sh:56–81 selects eligible resource_limit units from a completed scan, maps them to the primary list by (base_piece, unit), and rejects unknown or duplicate selected units. Lines 88–104 load the existing expected.tsv, retain all existing rows, and append only previously absent keys. A later rN/finalN scan can extend the inventory without dropping earlier units; an empty selection does not truncate it. JOB.md:43,116 prescribes this flow and forbids overwriting the inventory.
- PL/make_p5_list.sh:36–53 creates each p5/p5rN wave list exclusively from expected.tsv. Verified retries are skipped; previously attempted units become exceptions; only never-started inventory units are selected. Thus a later primary fitting wave may create new primaries, but cannot itself create a P5 retry outside the inventory. Its new eligible units must be appended before their P5 wave.
- PL/submit_prodl.sh:43–48 uses units_<wave>.tsv for P5 waves, and slurm/s4_p5.sbatch sets P5=1 before sourcing batch_runner.sh. PL/batch_runner.sh:23–24 reads those rows; :64–83 creates an exclusive, persistent p5_attempts/<unit> marker before invoking run_case.R with --p5-retry and the row's base run/repeat identity. A deferred, never-started unit can be listed again; a started unit cannot gain another supported P5 attempt.
- code/core/v2_2_1/study/adapter.R:413–439 maps that identity to the single fixed prefix <case>/P5_retry/{SMCBVS|SMCBVS_rep<m>}_p5retry. Lines 452–465 return an already valid record, acquire a prefix lock, and repeat the checks under that lock; :360–365 writes the RDS/CSV/sidecars at that prefix. Multiple artifacts are one logical retry record, not multiple records.
- code/core/v2_2_1/tools/p5_scan.R:64–80 visits each primary prefix and checks at most that one fixed retry prefix. It does not recursively deserialize a history of retries. Invalid/incomplete retry artifacts also cause at most one status_of call at that prefix. Therefore every retry record read by a legitimate final/rN scan is covered by an existing inventory row, and expected.tsv can over-reserve for unstarted attempts but cannot under-count retries created by the supported workflow. New inventory additions precede their P5 writes; PL/submit_prodl.sh:19–24 refuses scanning while run jobs are active. No assumption that only a small fraction is retried is needed. Manual inventory deletion or out-of-flow CLI writes are not supported transitions of this proof.

Evidence: arithmetic and margin

PL/prodl.env:43–51 sets base=600 s, rate=2,000 ms per logical record, floor=7,200 s. PL/submit_prodl.sh:98–106 counts smc+smcrep primary data rows plus every nonempty data row of expected.tsv if present, then computes:

    max(7200, 600 + (records * 2000 + 999) / 1000)

Shell integer division implements the ceiling for nonnegative millisecond totals; the floor is applied afterward. The formatter retains hours/minutes/seconds. submit():87–90 supplies the computed value explicitly as --time, overriding the batch default.

14,400 primaries and no inventory: 600 + 28,800 = 29,400 s = 08:10:00. With 14,400 listed retries: 600 + 57,600 = 58,200 s = 16:10:00. With 100 listed retries: 29,600 s = 08:13:20. At 3,300 primaries the value equals the 7,200 s floor; one listed retry raises it to 7,202 s.

The supplied 0.75 s smc observation scaled by the measured p=30 smcrep/smc size ratio gives 0.75 * 711/588 = about 0.907 s; twice that is about 1.814 s. The selected 2 s rate rounds this allowance upward and applies it to BOTH primaries and possible retries, with another 600 s base. The 588/711 KiB values are in ops/PROD_L_SIZING_20261030.md:36–37. This is a reasonable provisional sizing margin for D63, not a newly measured throughput upper bound or a guarantee against slower storage/larger future records. No real scan benchmark was claimed or run.

slurm/s5_p5scan.sbatch:10–12, JOB.md section 6 (:72), tests/vec_check.py:124 and tests/TESTS.md:40–41 agree on the initial default and retry-aware override.

Evidence: tests and independent reruns

Inspected the supplied TEST_DRIVER_d63b.out (384 passed, 0 failed) and TEST_P5_d63b.out (152 passed, 0 failed). Independently reran both unchanged suites in fresh permitted work folders, with saved stdout/stderr:

- <PC_TEMP_PATH> 384 passed, 0 failed; process exit 0. UTC log interval 12:09:14–12:13:34.
- <PC_TEMP_PATH> 152 passed, 0 failed; process exit 0. UTC log interval 12:09:50–12:12:45.

Launches (one simple command per shell call; corresponding .out files captured stdout/stderr):

    & 'C:\Program Files\Git\bin\bash.exe' '<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/jobs/PROD_L/tests/test_driver.sh' '<PC_TEMP_PATH>'
    & 'C:\Program Files\Git\bin\bash.exe' '<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/jobs/PROD_L/tests/test_p5.sh' '<PC_TEMP_PATH>'

Both paths were confirmed absent before launch. Suites create their own synthetic fixtures and staged source copies in these work folders; they use scheduler/Rscript stubs, with no actual R fitting processes. No campaign truth folder or truth manifest was opened.

The inspected test_driver.sh:120–163 D40–D53 block checks the initial real-list workload with no expected inventory, final with a header-only inventory, final with 100 retries, and the heavily retried final with one retry per primary (28,800 logical records), plus the base/floor boundaries, enum exclusion, printed counts, explicit sbatch times and list restoration. D51/D52 directly exercise the prior residual. These are submission-sizing tests with synthetic inventory rows, not a throughput benchmark. test_p5.sh L120–L127 independently checks byte-preserving inventory extension, idempotence and subsequent wave selection; L160–L172 checks recovery/extension from rN/finalN phases. Source inspection above supplies the fixed-prefix/record-bound argument.

SHA-256 of principal reviewed files (relative to PL; raw local bytes):

    71D5BCB49D389798459667B15E838DE261E7649172243BE7F4BD503F4271CB78  prodl.env
    81273D47278769C2D94BCC6AD83268B3AF19A6636130703CB51198596DBE376B  submit_prodl.sh
    615B054BF3B324625541706A47B28ADC3959355A6FBE4AF8C88375AC30E56BD2  make_p5_list.sh
    36B8A7EFBD2BA698C7DF8315159388DA51D874D6C79E5779462C85337DF05853  tests/test_driver.sh
    E8F90690E7EF1461345517D2BF9BFB394EC25EB28260C991A58FFB76DECE7C8B  tests/test_p5.sh

Findings classified

(i) Blocking: none remaining for D63.
(ii) Document-only / minor: none requiring correction for this narrow disposition. The comment's 2,000 ms allowance should be understood as rounding upward from the approximately 1,814 ms size-adjusted double baseline.

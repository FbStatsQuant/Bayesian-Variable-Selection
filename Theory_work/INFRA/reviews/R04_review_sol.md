REJECT
Score: 6.5/10

Reviewed `67879c275206f15f8606a10d84301349a65412ca` on `theory/infra`. Narrow R03 confirmation only. Lifecycle suite: **21/21 PASS**; `check.py --quiet`: **276 claims, 0 ERROR, 21 WARN, 143 INFO**. Additional probes used actual functions with in-memory fixtures/mocked persistence; the Job probe launched and cleaned up only its own processes. No CI/calibration run; timing columns ignored. Only this reply file written in the live worktree; the explicitly permitted lifecycle suite used its disposable worktree.

| R03 item | Result | Reason / adversarial check |
|---|---|---|
| N1 | FIXED | Actual downgrade, retract and deprecate with mocked persistence all saved `OPEN` together with `new.md:1`; suite also verifies saved downgrade provenance. |
| N2 | FIXED | Full-id, ticket-local and alias self-bindings all produce `Graph.self_edges`; C3-self consumes that list. |
| F2 | PARTLY | Assigned descendants are job-contained, but a real pre-assignment child survived Job close; failed snapshot enumeration still returns `{}` (findings 1, 4). |
| F5/F6 | PARTLY | C10, propagate, registry add/correct-status share the locator; original `Not yet` and next-line borrowing probes fail correctly, but negative compound statuses pass (finding 3). |
| F8 | PARTLY | Single-binding confirmation and latest-valid/no-valid-source reverts work; independent target binding is deleted on revert (finding 2). |
| F10 | FIXED | `README.md:1`, `./README.md:01 note`, and `README.md:1-1` canonicalize identically; actual freeze check rejects the duplicated routes. |
| W2-LOC2:Lemma-BC | FIXED | Graph input now names CT's block-inverse/Rayleigh proof pattern, matching source lines 108?109; erroneous CD use removed. |
| W2-FAC-S5:L1 | PARTLY | Added 44?67 is hashed, but L1.1?L1.2 at 22?42 remain uncovered: mutations at 26 and 35 leave the hash unchanged. |
| W1-GEN:L8 | PARTLY | H2 definitions 64?75 are hashed; referenced notation at STATEMENT 32?36 remains uncovered: mutations at 32 and 34 leave the hash unchanged. |
| W2-FAC-XA:L1 | FIXED | Both added L1b/L1c spans are hashed: mutations at 35, 42, 56 and 77 each change the hash. |
| LIFECYCLE ?5.3 | FIXED | Wording matches latest-valid restoration; bound-consumes chain X?Y?Z with dead Y restores X, and with no valid predecessor retains Z for invalidation. |

The two partial coverage rows are remaining R03 coverage requests, not new findings. Deferred clause splits and ?5.5 human attestations are not counted as defects.

Findings (new reproducible cases within the requested fixes):

1. **MAJOR ? F2: Job assignment races script execution.** `ci/run_ci.py:run_in` starts a runnable process before `job.add(p)`. Reproduction: start a Python parent that spawns a sleeping child and prints its PID; read that PID, then call actual `Job.add(parent); Job.close()`. Parent dies, child remains in `_process_table()` (`True`); explicitly killed the child afterward. This forces a legal scheduling interleaving in run_in. Job membership is inherited only by children born after assignment; post-exit `kill_tree(parent.pid)` cannot recover an orphan through a vanished intermediate parent. Assign before execution, using a suspended launch/resume or equivalent atomic job placement.

2. **MAJOR ? F8: reverting consumes erases an independent target obligation.** Actual `confirm-repoint` with mocked persistence, D consuming `P:X@X; P:X@Y`, proposal X?Y / `proof:P:X`, saves `P:X@Y; P:X@Y` and `preexisting=no` (`propagate.py:272?280`). Actual `plan_reverts` + `apply_revert` then produces `P:X@X; P:X@X`; Graph has only X. Retraction of Y therefore misses D's independent Y obligation and its downstream invalidation. Detect pre-existing target bindings and preserve one on revert, as already done for depends_on.

3. **MAJOR ? F5/F6: substring matching still certifies a negated status.** With `read_lines` returning `['Status: NOT-PROVED-CHECKED']`, actual `status_at('PROVED-CHECKED', 'fixture:1')` returns `ok`; `PROVED-CHECKEDNESS` also returns `ok`. `bvsreg.py:245?250` has neither token boundaries nor punctuation-aware negation. Every shared caller consequently accepts these sources as positive provenance. Require complete status-token matches and handle negation joined by punctuation. These are text-validation failures, not mathematical attestations.

4. **MINOR ? F2: snapshot enumeration does not fail closed.** Mock kernel32 with valid snapshot handle 123 and failing `Process32First=0`: actual `_process_table()` returns `{}` without raising. A failed `Process32Next` likewise ends enumeration without inspecting the error. `pid_alive` interprets missing owners as dead during stale cleanup. Declare HANDLE signatures and distinguish ERROR_NO_MORE_FILES from enumeration failure; propagate other errors.

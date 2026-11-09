# R02 disposition (review: R02_review_astra.md, REJECT 6/4/7)

All findings accepted. `tools/test_lifecycle.py` now has 16 scenarios, all PASS. It runs in a disposable worktree
holding a copy of INFRA and never touches the live registry. The previous version did touch it: a run that was
killed left a TEST row, which was found and removed from the pre-test backup. This incident is why the harness
changed.

| # | sev | finding | disposition |
|---|---|---|---|
| F1 | FATAL | stale-sandbox cleanup force-removes any worktree whose path contains `bvs-ci-` | Fixed. Sandboxes live only under `<temp>/bvs-ci-sandboxes/`, each with an owner file (pid). Cleanup considers only worktrees whose real path is inside that root and whose owner process is dead. Worktrees outside the root are never touched. |
| F2 | MAJOR | process lifetime / path escape / unchecked reset | Fixed. Script paths must be relative, contain no `..`, and resolve inside the sandbox (else REFUSED). The process tree is killed in a `finally` after every run: normal exit, timeout, error or KeyboardInterrupt. Descendants are found by parent pid through a Toolhelp32 snapshot, so orphaned workers are caught (verified: a 4-process multiprocessing tree is fully killed). Kills are verified and survivors raise. Reset is checked: a failed `checkout`/`clean`, or a non-clean status afterwards, aborts the step. The README states the boundary: relative writes only, not a security sandbox. |
| F3 | MAJOR | rollback not compositional (chains, dead predecessor, transitive) | Fixed. `plan_reverts` undoes a confirmed re-point only if the dependent still uses the retracted claim through it; a moved-on link becomes MOVED-ON. The restore target is the latest VALID source in that dependent's re-point chain. With no valid source, the edge to the retracted claim is kept, so the dependent and all its users are invalidated transitively. Impact is computed on the planned post-revert graph before the report. Both reviewer sequences are regression scenarios (PASS). |
| F4 | MAJOR | clear defeats invariants | Fixed. `clear` refuses while any input is SUSPECT/NARROWED/RETRACTED/DEPRECATED/CANDIDATE (unless acked) or a re-point proposal is open. A repaired claim with a valid replacement returns to SUPERSEDED-VALID, not ACTIVE. Scenario PASS. |
| F5 | MAJOR | status / parity / freeze bypasses | Fixed. `--status` is accepted only for downgrade/retract/deprecate, must occur verbatim at `--status-source`, and may never be stronger. Coexist requires every axis declared and a verdict of exactly incomparable, plus gate parity. Supersede, promote and coexist share one evidence-bearing gate parser. While frozen, a headline can be promoted only as a free replacement. `registry.py add` requires `--status` to be verbatim at `--source`. Scenarios PASS. |
| F6 | MAJOR | C10 accepts negated / borrowed status | Fixed. The window is now the stated line plus the next 3 (no look-back). A status preceded by not/no/never/un is an ERROR. Not-found and found-elsewhere are ERRORs (they were WARNs). The reviewer's PKA:L0 case (`Not PROVED-CHECKED`) is caught by the negation rule. Residual: substring matching within that window; exact cell extraction needs structured reports (Wave 3 REPORT registry block). |
| F7 | MAJOR | headline domains / bindings | Fixed for the cited cases. POST's span ends before clause (c); its scope note excludes the inclusion clause. PLR uses A:COEF-BOUNDED (fixed θ_lo) and is marked split-needed (C-i/C-ii). F-LOC2 lists only the hypotheses common to its alternative classes, with a note to register class claims. The unrelated Lemma-LS bindings are now TO BE DETERMINED. The optimizer skips DRAFT and TO-BE-DETERMINED bindings, so nothing unverified is recommended. |
| F8 | MAJOR | implicit property edges not family-specific / not repairable | Fixed. Plain `consumes P:X` creates no edge. A consumer binds its actual bridge as `P:X@<claim id>`, which creates a `proof:P:X` edge to that claim. |
| F9 | MAJOR | incomplete definitions; LaTeX non-blocking | Sample defects fixed: Cor-D span; S5 CC definitions as premises; Cor-M FS′ definitions; FAC-A L1 constant line. Transcription: a changed `tex` is now an ERROR, a never-reviewed one is a WARN for headlines, and the generated paper block carries a visible flag until `rehash --tex`. Residual: complete definition coverage for every claim is a continuing curation task. |
| F10 | MAJOR | freeze fabricable | Fixed. FAILED-REMOVAL evidence must be a readable `path:line` (distinct by path:line; `fail-route` enforces the format). Each review file must contain the attested line `FREEZE-OUTCOME: no headline-changing candidate`. LIFECYCLE narrows the claim: the outcome is a human attestation the tool only checks is recorded. |
| F11 | MINOR | version policy inconsistent | Fixed. One policy is stated in LIFECYCLE §1 and in the propagate help. Supersede of X and deprecate bump minor; coverage corrections bump patch. |
| F12 | EDITORIAL | stale help | Fixed (propagate coexist help; run_ci falsify/cite docstrings). |

## Per-id defects (R02 table)

| ID | Fix |
|---|---|
| C-MIS:Cor-D | Span set to 116–120, so the qualification is included. |
| W2-FAC-B:Cor-M | L2 statement edge replaced by `L2@proof:L2.4 argument under FS'`; FS′ and FS-b definitions hashed as premises. |
| W2-APP:VN-routes | Aggregate Thm-GEN edge replaced by `W1-GEN:L2@stmt` and `C-GROW:L3@stmt`. |
| W2-FAC-S5:Thm-FAC-BCS-R, W2-FAC-S5:KL | STATEMENT:81–95 definitions added as premises. On BCS-R, the FAC-B theorem edge is replaced by the L1.5 and L5 proof-pattern uses. |
| C-MIS:LemZ | `Cor-H@stmt` added. |
| W1-GEN:L2 | e4 premise added (STATEMENT:42–44). |
| W2-APP:VN, C-GROW:L3 | Now target the newly registered `C-GROW:L0.2`. |
| W2-FAC-A:L1 | Constant line added as a premise; split-needed recorded. |
| C-DLV:Cor-3.2p | Spurious L3-3.2 edge removed. |
| W2-LOC2:PLR, W2-LOC2:F-LOC2 | See F7 above. |

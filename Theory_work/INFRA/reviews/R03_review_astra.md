REJECT
Scores (0?10): registry 6.5; scripts 6; protocol 7.5.

Reviewed HEAD `e32dfd6cb1af5601c50a93460595f9d50d78ce3d`, worktree `C:/Users/felip/BVS-infra`. Only this reply file written; no CI/calibration, live registry mutations, state-changing git commands, or subagents. Timing columns ignored. Ran `python -B .../check.py --quiet`: **276 claims, 0 ERROR, 21 WARN, 143 INFO**. Used read-only source inspection and in-memory mocks of actual functions/C10 code; did not run the disposable lifecycle suite. Gate-review currency, independence, mathematical implication and binding mechanisms are treated as human attestations under ?5.5, not machine-verifiable defects.

## R02 findings confirmation

| ID | Result | Verified reason |
|---|---|---|
| F1 | FIXED | `Sandbox.__enter__` confines stale removal to the dedicated real-path root and tests owner PID; unrelated substring-matching worktrees are no longer selected. Enumeration failure remains an F2 concern. |
| F2 | PARTLY | Relative-path guard, checked reset and finally cleanup exist; actual `_process_table()` found this process. But `descendants(100)` with surviving table `{300:200}` returns `[]`: an exited intermediate parent loses the grandchild. Snapshot errors also return an empty table, interpreted as dead owners; cleanup/removal return codes remain unchecked. |
| F3 | FIXED | Original sequences work in memory: dead X leaves D?Y and graph impact includes E?D; X?Y?Z with dead Y restores D?X. Moved-on links are skipped and planned graph drives impact. |
| F4 | FIXED | `clear` rejects invalid unacknowledged inputs and open proposals; repaired replaced claims return to SUPERSEDED-VALID when the replacement is valid. |
| F5 | PARTLY | Status strength restriction, coexist parity/freeze, promotion freeze and shared PASS parser exist. `status_ok_at` still accepts `Not PROVED-CHECKED`; status provenance is not persisted (N1). Evidence contents remain permitted attestations. |
| F6 | PARTLY | Exact `Not PROVED-CHECKED` now errors; actual C10 block still accepts `Not yet PROVED-CHECKED` and source line `X: OPEN` followed by `Y: PROVED-CHECKED`. These contradict ?5.5's negation/verbatim enforcement claim. |
| F7 | PARTLY | Irrelevant fixed-sparsity bindings are withdrawn and optimizer filters drafts/unresolved mechanisms. POST 27?33 still includes the supposedly excluded inclusion clause at :33; PLR remains unsplit with conjunctive strength fields. F-LOC2 now records common assumptions, but class splitting remains deferred. |
| F8 | PARTLY | Plain consumes no longer invents generic bridges; bound consumes creates family-specific edges. Actual dry-run confirmation of D consuming `P:X@X` is refused: `D no longer uses X@proof:P:X`, because confirmation/revert still inspect only depends_on. |
| F9 | PARTLY | Several spans repaired and changed reviewed TeX is ERROR. FAC-A U(a)?(d)/constants remain unregistered/unhashed; new sample has analogous omissions below. Never-reviewed TeX remains publishable with a flag rather than a blocking gate. |
| F10 | PARTLY | Readable routes and explicit outcome attestations are checked. In-memory `README.md:1` and `README.md:01` count as two distinct routes and pass freeze; canonicalize path/span before deduplication. No objection to the expressly human-attested outcome itself. |
| F11 | FIXED | Supersede/deprecate bump minor; premise coverage corrections bump patch; help and ?1 state that policy. |
| F12 | FIXED | Coexist help says parallel theorems; CI help describes disposable worktrees. |

F2 repair: use a Windows Job Object (or continuously retained descendant identity), fail closed on snapshot errors, and check removal results. A one-time post-exit parent-PID snapshot cannot reconstruct a vanished intermediate process. This is a remaining R02 issue, not a new finding. Both absolute and `../` script-path probes were refused.

## R02 per-id defects

Only rows marked defective in R02 are repeated; previous OK rows are not claimed to have been re-audited.

| ID | Result | Verification |
|---|---|---|
| C-MIS:Cor-D | FIXED | Span 116?120 now includes measurable coefficients/certificates. |
| W2-FAC-B:Cor-M | FIXED | L2 is a proof-pattern use; premises 89?90 and 33?34 include FS? and its component formulas. |
| W2-APP:VN-routes | FIXED | GEN L2 and GROW L3 statement uses added; diagonal proof use retained. |
| W2-FAC-S5:Thm-FAC-BCS-R | FIXED | Definitions 81?95 hashed; FAC-B edges now L1.5/L5 proof patterns. |
| W2-FAC-S5:KL | FIXED | Definitions 81?95 included; lowercase open status retained. |
| C-MIS:LemZ | FIXED | Cor-H statement edge added. |
| W1-GEN:L2 | FIXED | STATEMENT 42?44 now hashes e4. |
| W2-APP:VN | FIXED | Actual edge now targets registered GROW L0.2. |
| W2-LOC2:F-LOC2 | PARTLY | Alternative classes no longer conjunctively listed, unrelated generic edges removed; class-specific strength claims remain deferred. |
| W2-LOC2:PLR | PARTLY | Fixed coefficient assumption corrected; clause split still only a note, and premises remain STATEMENT 19?31. |
| C-GROW:L3 | FIXED | Actual L0.2 statement edge added; GEN proof/event input retained. |
| W2-FAC-A:L1 | PARTLY | Constant line :77 added; row itself acknowledges missing nu_n/L_kappa coverage and unregistered U(a)?(d). |
| C-DLV:Cor-3.2p | FIXED | Spurious L3-3.2 dependency removed. |

## R03 sample: 15 IDs

Status and kind are appropriate for all 15. Status text occurs at the stated line after markup normalization, except XA:L1 where it legitimately continues onto the next line. ?OK? is a registry spot check, not a new proof certification. Paths below are the claim's registered source unless specified.

| ID | Result | Statement/premises and use-level check |
|---|---|---|
| C-ENG:Impl-Merge | OK | REPORT 11?33 captures implementation/switch scope; TDP_E is an actual algorithm input; implementation kind and DONE provenance fit. |
| C-MIS:Prop-P | OK | L2_gaussian 7?38 covers Gaussian/marginal-vector setting, triangular-array and fixed-variance qualifications; direct conditioning/block algebra needs no extra registered theorem. |
| C-GROW:L6.4 | OK | 223?243 covers all three tail conclusions; setting and reference-statistic premises present; L6.2/L6.3 and population P4 are actual proof inputs (:253, :296). |
| W1-N3:Cex-N3-Dm | OK | Explicit D_m construction/cap conditions and abstract-table limitations captured; L1 lexicographic and L5 traversal inputs match proof. |
| C-ENG:Impl-GROW-MR1 | OK | REPORT :53 records cap implementation; absence of a theorem edge is appropriate for implementing a requirement. |
| C-GROW:L1.1 | OK | NA/TL and lattice/neighbour definitions 9?17 included; 19?25 complete; direct case proof 27?38. |
| W2-LOC2:Lemma-BC | defect (MINOR) | BC 78?84 and decay setting covered; `W2-APP:CD@proof:CD(b)` is not the cited proof use. :108?109 cites CT's block-inverse/Rayleigh argument (`L2_CT.md:55`), also rederived here. Remove CD or bind the actual CT proof pattern. |
| W2-FAC-S5:L1 | defect | Span 69?101 is only L1.4; L1.3 residual/Gaussian statistics 44?67 are omitted despite the short description and downstream use. Those definitions also feed L1.4 itself. Hash/register L1.1?L1.3 and distinguish their proof uses. |
| W2-FAC-B:L4 | OK | Full path conclusion, CS/P/theta and E1?E7 included; event notation 11?18 is covered transitively by registered L3 premises 7?30. L1/L3 are real proof inputs. |
| W1-N1:B | OK | Statistical-record/success-set and EX-A/START/KERNEL premises covered; T12/N9 are actual structure/kernel inputs; all B-a?d captured. |
| W1-GEN:L8 | defect | Both certificate statements captured, but H2a/H2b/H2c and leakage-family definitions are only named in premises 7?13. Add STATEMENT 64?75 and the referenced notation definitions; no missing external proof theorem identified. |
| W2-FAC-XA:L1 | defect | Registered name/short covers L1a?c, while span 11?14 covers only L1a; residual comparison 35?42 and conditional coupling 56?77 remain outside coverage. Existing split-needed note does not register them. |
| W1-PXN:Thm-PXN(P) | OK | LH-iid/score premises and complete rate/expectation clause included; P8 is the appropriate posterior input. |
| SOP:TH128 | OK (external anchor) | Exactly preserves history row :94, including qualified status; external kind is honest. Row is a truncated pointer to W6-FIXREV2, not a complete theorem transcription or independently certified statement. |
| W1C-FINAL:Lemma-CAP | OK | L1?L4 setting, exact-branch qualification and all three clauses captured; implementation and operational-closure inputs match proof :58?60. |

The coverage defects are additional instances of R02 F9, not separately numbered new blocking findings.

## NEW blocking findings beyond R02

**N1 ? MAJOR: a validated status change saves stale provenance.** `tools/propagate.py:status_ok_at` validates the supplied `--status-source`, but the downgrade/retract/deprecate mutation branch assigns only `status`, never `status_source`. Thus changing a checked claim to a source-backed `OPEN` at a new report line saves `OPEN` with its old checked-status source; C10 then fails (or borrows unrelated nearby text). Persist the validated source with the status in the same mutation, using the same negation-aware extraction as C10. This is separate from R02's status-upgrade bypass.

**N2 ? MAJOR: self-bound property obligations disappear from the graph.** `tools/bvsreg.py:369?377` silently skips a consumes binding resolving to the consumer itself. Actual in-memory `Graph([X with consumes=P:X@X])` has no self_edges and no cycle: a circular proof obligation passes the graph check and cannot propagate invalidation. Explicit depends_on self-edges correctly error; apply the same handling to consumes and test aliases as well. This is introduced by the new binding representation, distinct from R02's generic-bridge problem.

Minor documentation/robustness items: ?5.3 still promises exact restoration of the recorded before edge, whereas the new planner deliberately restores the latest valid predecessor; synchronize it with ?5.5. `fail-route` validates the first whitespace-delimited token but saves the entire route string, while freeze validates the entire string as a span, so an accepted `path:line description` route later fails freeze. Snapshot HANDLE argument signatures/error checks should be explicit even though the actual process-table smoke check succeeded here.

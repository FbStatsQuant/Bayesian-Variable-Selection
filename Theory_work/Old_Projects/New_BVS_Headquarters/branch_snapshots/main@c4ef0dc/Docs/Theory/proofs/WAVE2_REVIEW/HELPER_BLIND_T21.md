# Blind correctness review: T21

Reviewed on 2026-10-22. Assigned proof: `T21_T14H_HPM_composition/proof/PROOF_v2.tex`.

Scope: independent correctness review of C1 and discovery routes (a)--(f), including the operational conditioning, exact branch, correspondence to the original theorem, and every cited wave-1 input. No proof was edited, no numerical workload was run, and no further delegation was used. Only the permitted source files were opened; no separate reviewer, helper, fatal-flaw, or final-report file was opened. This file is the only written artifact.

Line references below use the source files as read. Abbreviations: **P** = assigned `PROOF_v2.tex`; **S** = assigned `STATEMENT.md`; **O** = `../theorems/T21_T14H_HPM_composition.md`; **C** = `COLLECTED/COLLECTED_PROOFS_v2.tex`; **M** = the specified `METHODOLOGY_v3.md`. Other theorem references are to the original files in `../theorems`.

## Findings

No findings of severity **fatal**, **gap**, or **exposition** requiring correction were identified. No replacement wording is required.

The positive verification below records the claims and the evidence checked. It does not certify the unproved hypotheses H03, H10, or H24.

## C1 and statistical input

**Locations:** S:42--46; P:52--85; O:14; original T03:14--20.

On `pi(S0)>1/2`, truth strictly beats every other model, so a usable all-scored HPM can fail only if truth was not scored. The inclusion at P:71--72 and Markov bound at P:74--76 give precisely C1, with unavailable output handled separately. The argument does not require a particular data law beyond the statement's definitions.

The passage from H03 to `E0 delta1 -> 0` is valid because `0<=delta1<=1`: P:78--84 explicitly proves the needed bounded-variable argument. It does not incorrectly turn an `O_P` posterior rate into the same frequentist selection-error rate. Exact-equality tie breaking is harmless because the event used has a strict truth maximum.

**C1: verified.**

## Route (a): fresh final draws and the one-deletion corollary

**Locations:** S:19,25,48--60; P:92--178; O:15; M:187--198,238--245.

The fixed pre-final history determines launch, tier, grid, and `Q_f`. There are `4N_e` initial draws and `4N_e(T+L+4)` independence proposals, giving `Q_f=4N_e(T+L+5)`. Resampling does not change these call counts. All these models are scored regardless of acceptance.

Conditioning on the entire pre-final history is justified, not merely asserted as a consequence of conditioning on the smaller calibration record: P:103--118 invokes the collected fixed-stream proposition and supplies the fresh-uniform reasoning. The previous absence of truth is pre-final measurable. Consequently P:125--129 follows by the tower property without an unjustified independence assumption about calibration success and earlier discovery. The nonlaunch term is retained.

The criterion `P(Fcal, Q_f*pi0(S0)<=M)->0` for each fixed finite `M` suffices by P:136--142. The statement does not use an outcome-selected calibration draw count as a fixed exponent.

H10 is applied only to the feasible addition from `S0\{i}`. Substituting `k=s0-1` gives denominator `2p-s0`, as at P:154--160. For fixed positive `s0,c`, the guaranteed lower bound has the stated scale. The inequality at P:169--170 proves divergence for `p<=C sqrt(n)`, including the boundary through `L->infinity`. This intensity assertion concerns launched runs, as P:157 explicitly states. No negative conclusion outside that sufficient range is inferred from a lower bound.

**Route (a): verified.**

## Route (b): Gibbs execution

**Locations:** S:21,62; P:180--194; O:16.

For the execution-time base `A=X_pre-j\{j}=S0\{j}`, truth is one of the two configurations. If `j` is true, the addition is feasible because `s0<=K`; if `j` is not true, the exclusion configuration is truth even if the alternative addition is infeasible. SR therefore supplies a score independently of the Gibbs outcome. The event inclusion and the `U^c` discovery bound follow directly. The proof correctly refuses to replace the execution-time equality by round-start occupancy.

**Route (b): verified.**

## Route (c): stopped swap opportunities

**Locations:** S:64--71; P:196--253; O:17; M:193--198.

The useful deletion/insertion pair at the stated proxy is unique, with conditional probability `1/[k(p-k)]`. Counting actual opportunities before discovery is predictable from the pre-draw history. The argument at P:212--224 uses this history rather than conditioning on a future opportunity count: occurrence of opportunity `i` entails that opportunity `i-1` missed, and fresh proposal probabilities give the recursive bound. On whole-run failure with `O>=D`, the first `D` opportunities all miss, which yields the claimed split. The conventions for `D=0`, including `b=1`, are covered.

PX supplies a deterministic threshold with `b D_n>=omega_n`, so the geometric term vanishes. ONE alone supplies no exposure count. The neighbour-swap formula uses the actual edge and actual insertion-set size; a missing edge gives zero. The extension with a deterministic lower bound is valid. The stated random-bound extension appropriately requires measurability at a conditioning boundary, preservation of the proposal laws, and subsequent averaging of the geometric term.

**Route (c): verified.**

## Route (d): tables and completed scans

**Locations:** S:17,21,73; P:255--278; O:18; M:170--175,258--265.

The check `B<=K` includes the small case `n=3`. Thus every block-table subset is feasible, and a completed table containing truth supplies its full-response score. The feasible flip-or-swap neighbourhood is symmetric, so a completed scan centred at a neighbour of truth scores truth. This uses only the scoring implication, not a strict-mode assumption or a remaining move budget. The last extra scan is included. HPM score retention makes later schedule success unnecessary when the output is usable; C1 still accounts for unavailability.

**Route (d): verified.**

## Route (e): terminal repair

**Locations:** S:31--36,75--85; P:280--368; O:19; original T24:8--18.

H24 supplies two uniform bounds on the actual hybrid round: endpoint truth probability at least `a_n`, and one-round elementary-state exit probability at most `eta_n`. These bounds are fixed after conditioning on the data and selection past. Selection based on that past is permitted because the bounds are uniform before selection. Fresh future randomness, temperature one, execution of the chosen rounds, and absence of intervening resampling are explicit assumptions.

The first-exit split gives `P(J|past)<=H eta_n`. For the no-exit/no-truth-endpoint events, the next round starts inside `R_d`, and its truth endpoint probability is at least `a_n`; hence `P(B_h|past)<=(1-a_n)P(B_{h-1}|past)`. This does not require conditioning on future survival or dividing by a survival probability. Every truth endpoint implies a truth score under the ledger and SR rules, giving the stated union bound. The case `H=0` is explicitly covered.

The availability split and sharper final-run bound retain the correct nonlaunch-and-no-earlier-hit term. Pilot use is expressly based on its forward filtration, not on its subsequently constructed grid. For `H=L+4`, fixed `s0,d` and `B<=16` give the positive constant lower bound on `c_n`; the assumed high-probability bound `a_n>=c_n/2` and assumed `H eta_n->0` therefore suffice. Neither the displayed candidate formulas nor LK/EXIT/GAIN are presented as a proof of these hypotheses.

**Route (e): verified conditionally on H24 and the stated operational/availability assumptions.**

## Route (f): exact branch

**Locations:** S:17,19,87; P:370--396; O:20; M:154--160.

Completed enumeration scores exactly the feasible finite state space. The same total order gives the global HPM, and direct finite sums give `Z` and the primary PIPs. The normalised capped prior is included exactly once. The proof does not use an SMC evidence identity for this branch.

For fixed `p`, the model count is at most `2^p`, whereas the branch threshold is at least `4np`, so eventual branch selection is established. Completion remains a separate operational requirement. Eventual branch selection alone is not claimed to provide completion or posterior concentration. The mathematical definitions of start components do not require the exact-branch implementation to construct blocks.

**Route (f): verified.**

## Audit of every wave-1 citation

1. **T11(iii), used at P:103--118 and identified at P:405--406.** C:629--633 states the independent-stream, exact-sampler, frozen-calibration, and full-execution conditions. C:788--839 proves the stronger fixed-entire-calibration-stream assertion, with exactly the initial and independence calls used here. C:844--864 gives the conditional miss identity. T21's use with fixed truth is a permitted specialization; integrating over data preserves the result. No unproved T11 scoring-ledger clause is used as an input.

2. **T20(ii), used at P:269--270 and identified at P:406--407.** C:3356--3366 proves the local-search conclusions under strict truth optimality. Its first scoring step, C:3358, uses only neighbourhood symmetry and completed execution. T21 both proves this narrower implication directly and explicitly disclaims using the later move/certificate conclusions without their strict-mode hypothesis. This extraction is justified; it does not adopt T20's conditional statistical conclusion as unconditional.

3. **T09(i), cited at P:387--389 and identified at P:407--408.** C:331--355 proves the exact convolution normaliser and backward sampler, including iid draws from fresh randomness. T21 describes exactly this component result and explicitly says it is unnecessary for the direct enumeration identities. It does not miscite T09 as an exact-branch evidence theorem.

T03, T10, and T24 are not among the proved chapters of the supplied wave-1 collection. T21 correctly labels their needed conclusions as H03, H10, and H24 instead. In particular, the T23(ii) chapter is not used to infer a proved terminal-repair minorisation.

## Faithfulness and scope

S:29 matches the posterior concentration conclusion of original T03(i); S:30 uses exactly the start-addition inequality in original T10(i); S:31--36 uses the one-round inputs and required asymptotic consequences of original T24(i). P:24--25,293--294,367--368,411--416 maintains that dependency boundary.

Relative to O:14--20, the proof preserves C1, all six finite discovery routes, the actual budgets, the target/prior, and the exact branch. The replacement of conjectural dependencies by explicit hypotheses is recorded as the user's required correction at S:91. This is a conditional composition result, not a verification that G/R/SE/BM-C imply H03 or that LK/EXIT/GAIN imply H24. No expansion, cluster-separation, no-switch, SMC-PIP accuracy, or SMC-evidence accuracy assertion is silently imported.

**T21: verified for exactly the conditional statement in the assigned STATEMENT.md.**

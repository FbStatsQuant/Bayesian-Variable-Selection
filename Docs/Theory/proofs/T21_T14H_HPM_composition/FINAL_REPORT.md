# FINAL REPORT — T21

**Outcome: proved (Astra lead; reviewed by Sol 6.1 x2); not adopted.**

Scope: the composition bound (C1) and discovery routes (a)-(f). The final proof is [PROOF_v2.pdf](proof/PROOF_v2.pdf), with source [PROOF_v2.tex](proof/PROOF_v2.tex). The exact statement is [STATEMENT.md](STATEMENT.md).

The result separates three reasons the method may fail to report the true model: no usable output, insufficient posterior concentration, and failure to score the truth. It proves the stated bounds for each discovery route. It does not prove that T03, T10 or T24 hold under their proposed primitive conditions.

## Statement changes and clarifications

The user's required hypothesis boundary is explicit:

- H03 assumes T03's posterior concentration conclusion. T21 proves the bounded-expectation implication and selection-error decomposition, without claiming a proof of posterior concentration.
- H10 assumes the feasible-addition lower bound needed for the one-deletion start-mass corollary.
- H24 assumes the uniform terminal-round truth-entrance and exit bounds. Its asymptotic constants/rates are also explicit hypotheses when used. T21 derives the conditional survival bound and incorporates availability and nonlaunch.

Operational and probability scopes are explicit: the iid exponent counts all executed final draws under full execution; Gibbs and swap opportunities are defined at execution time; tables/scans must actually execute; eligible-particle selection uses the available past; pilot repair does not condition on later calibration information. The dimension range p <= C sqrt(n) is sufficient, with no negative conclusion above it.

One narrow wording correction was required during statement checking. A fixed deterministic neighbour-swap lower bound may enter an unconditional scalar bound directly; a random bound requires conditioning and averaging. The first Astra xhigh checker rejected the overly broad word “predictable.” The lead accepted the correction, reanalysed the original source, and a fresh Astra xhigh checker approved the corrected statement. One statement-analysis restart; no counterexamples.

The source theorem, method, budgets and prior were not edited. No other v3 conjecture is used as a proved result. EXP' and cluster separation are not needed here because no block expansion or no-switch result is claimed. Only the primary PIP is considered, and its exactness is claimed only on completed enumeration.

## Independent proof review

Two fresh GPT-6.1 Sol agents at high effort started in the same parallel delegation batch. Each had a separate packet outside the project containing only STATEMENT.md, PROOF_v1.tex, PROOF_v1.pdf, and the report format. They received neither the statement-check exchange nor a lead verdict, and neither saw the other report.

- Reviewer 1: **verified**, no findings. Full report: [SOL_REVIEWER1_ROUND1.md](review/SOL_REVIEWER1_ROUND1.md).
- Reviewer 2: **verified**, no findings. Full report: [SOL_REVIEWER2_ROUND1.md](review/SOL_REVIEWER2_ROUND1.md).

The lead inspected both reports and accepts their assessments. There were no fatal, gap, or exposition findings from the proof reviewers. No proof review rounds beyond round 1 were needed. [CLAIMS_OF_FATAL_FLAWS.md](CLAIMS_OF_FATAL_FLAWS.md) preserves the statement-check issue verbatim, its resolution, and the absence of outstanding proof findings.

Judge used: **no**. There was no unresolved disagreement.

## Final artifact validation

The reviewers verified PROOF_v1. PROOF_v2 changes only its author/status metadata to record the completed reviews and required result label. A direct source comparison confirmed no mathematical change.

TinyTeX compiled the final PDF twice with exit status 0. The six-page final document has no LaTeX warnings or overfull/underfull boxes in the last build. All six rendered pages were visually inspected; no clipping, overlap or malformed displayed equations was observed. Logs and rendered pages are retained under proof/. Source snapshots, hashes, tool/environment information and validation notes are under helpers/ and review/.

No simulations, benchmarks or numerical mathematical validation were performed. There were therefore no Owls workloads, scheduler IDs or seeds to report; local work consisted of proof writing, document compilation/rendering and file audit.

## Agent and call counts

- Primary lead: 1 GPT-6 Astra session, high.
- Statement checkers: 2 fresh GPT-6 Astra sessions, xhigh; 2 delegated calls.
- Proof reviewers: exactly 2 GPT-6.1 Sol sessions, high; 2 delegated calls, both verified in round 1.
- Helpers: 0. Counterexample referees: 0. Judges: 0.

Total: **5 agent sessions including the lead; 4 delegated calls**, all OpenAI. Task IDs and launch records are saved in review/TASK_REGISTRY.json; terminal results are in review/TASK_RESULTS.json.

Adoption remains Felipe's decision. No adoption or integration into the theorem collection was performed.



## Claude audit wording fixes (2026-10-23)

Source: WAVE2_CLAUDE_AUDIT/AUDIT_T21_T25iv.md. Wording only; no mathematical content changed. Final proof is now proof/PROOF_v3.tex (copy of PROOF_v2.tex) and its PDF proof/PROOF_v3.pdf; PROOF_v2.* are superseded and kept.
- E1 (required): the event M_H = {S0 not in Sscr when those H rounds end} is named in STATEMENT.md section 3(e) (first display) and in PROOF_v3.tex route (e): the sentence before eq. (repair), eq. (repair) itself, and the sentence after it ("M_H is empty" replaces "the whole-run miss event is empty").
- E3 (required): STATEMENT.md section 3(a) now reads "Stilde0=S0 minus {i} has pi0(Stilde0)>=c>0 (Stilde0 need not be the start mode)". The proof already said this.
- Skipped by instruction: E2 (observation on H10), E4 (optional).
- STATEMENT.md backed up to helpers/STATEMENT_before_claude_audit_fix.md (SHA-256 of the previous file 18046c65d8419d9a39bd13d88e610765c7730875f5443cb7e007bc1067c3fad5).
- New SHA-256: STATEMENT.md 5a1adaa48c7d7dcafdc8cddde4d3d410f7f96243e76236e8c47759b3bc779b11; PROOF_v3.tex 2dbd523465a605afdab51bcc52947d7501de9b4d58057aaad12460772c680f49; PROOF_v3.pdf 018085679832b865cc139611039ef0f669a5ff6592ad45f5f4c6eb52bc2a2bb1.
- pdflatex (TinyTeX), two passes: 0 errors, 0 undefined references, 6 pages. Build logs proof/build_PROOF_v3_pass1.txt, pass2.txt.
- Line diff PROOF_v2.tex -> PROOF_v3.tex touches only the lines named above.

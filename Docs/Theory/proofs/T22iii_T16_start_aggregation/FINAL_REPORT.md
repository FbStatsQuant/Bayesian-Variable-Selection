# T22(iii): final report

**proved (Astra lead; reviewed by Sol 6.1 x2); not adopted**

Completed 2026-10-22. Only part (iii) was proved in this run. Felipe retains the adoption decision.

The final proof is [PROOF_v1.pdf](proof/PROOF_v1.pdf), seven pages, with [LaTeX source](proof/PROOF_v1.tex). The final files are byte-for-byte identical to the files verified by both reviewers.

## Result

Under the stated Gaussian fixed-design assumptions, bounded signal energy, fixed true-support size, polynomial p, within-block eigenvalue bounds, VIS, EXP′, and NL_η, the exact start distribution concentrates on the true support:

    q_n ≤ u_n = O_{P₀}(2^B √(log n) n^(−κ)),
    e_n = o_{P₀}(n^(−m)) for every fixed m>0,
    1−π₀(S₀) = O_{P₀}(2^B √(log n) n^(−κ)+e_n).

Here κ satisfies the explicit NL_avg condition in [STATEMENT.md](STATEMENT.md). NL_η supplies every positive κ strictly below 1/2−η/2−√(2Aη) when η>0; exact zero leakage permits κ=1/2. The statement also gives the precise bound with the truncation slack ε₀. The weaker o_{P₀}(log n) remainder gives the stated n^(−κ+o_{P₀}(1)) exponent form and still gives concentration.

In plain language: the probability that an exact draw from the starting distribution misses the true support tends to zero, at the displayed rate. The theorem is conditional on its assumptions, including EXP′; it does not claim that all designs satisfy them.

## Statement change and fidelity check

The sole substantive change is the **approved Decision Point 2 change** mandated by Felipe: replace EXP by EXP′ and work together with NL_η on the leakage family. This is recorded explicitly in STATEMENT.md. EXP′ retains the logarithmic partial-R² term uniformly over actual-block additions. The proof derives its quadratic specialization only on the leakage family and derives the visibility lower bound directly from its logarithmic form. Neither bound was added as a new hypothesis.

The separate GPT-6 Astra xhigh checker returned **APPROVED**, with no fidelity corrections. Its full reply and submitted source packet are in [review/statement_check](review/statement_check/REPLY.md). The weaker remainder variant, the NL_avg rate condition, and empty-family conventions faithfully retain the source theorem's content. No statement-analysis restart was needed.

## Proof and review

The proof first controls residual sums of squares uniformly over the actual block tables. NL_η then makes the leakage partial R² small enough for the quadratic specialization of EXP′. A truncated Gaussian integral and averaging give the noise-addition rate without requiring independence between comparisons. For missing true variables, the logarithmic increments telescope along a completion path; VIS makes the completion penalty smaller than any fixed inverse power of n. The previously proved T22(i) converts these two bounds into start concentration.

The sole previously proved theorem used is T22(i), read in the wave-1 proof and the T22 chapter of COLLECTED_PROOFS_v2. Parts (ii) and (iv) remain read-only and are not reproved or used here. No unproved v3 conjecture is invoked as a theorem.

Exactly two fresh GPT-6.1 Sol high reviewers were launched simultaneously through T3 delegate_task, provider `codex`. Each received a separate temporary packet containing only STATEMENT.md, PROOF_v1.tex, PROOF_v1.pdf, and the report format. They received no lead deliberations or proof verdict, and neither could inspect the other packet under its instructions.

- [Reviewer 1, round 1](review/round_1/review_1/REPLY.md): **verified**; no fatal, gap, or exposition findings.
- [Reviewer 2, round 1](review/round_1/review_2/REPLY.md): **verified**; no fatal, gap, or exposition findings.

Both complete reports were inspected and processed. There were no findings to repair or reject, so no revision or further review round was necessary. [CLAIMS_OF_FATAL_FLAWS.md](CLAIMS_OF_FATAL_FLAWS.md) records the empty findings log and the lead's disposition. No Astra judge or counterexample referee was used.

## Validation and audit trail

TinyTeX compiled the final LaTeX successfully with exit code 0. The final log has no warnings, undefined references, or overfull/underfull boxes. All seven pages were rendered and visually inspected. Logs and rendered pages are retained beside the proof; [helpers/VALIDATION.md](helpers/VALIDATION.md) records the commands and checks.

All ten snapshotted project source files were unchanged at the final integrity check. The reviewed statement, LaTeX and PDF hashes also match their final copies. Source snapshots and manifests are under `helpers/`; isolated packet copies, task IDs, full replies, and orchestration results are under `review/`. The source method's SHA-256 matches the prescribed 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c.

No simulations, benchmarks, numerical experiments, or mathematical computational validation were needed or run. Local execution was limited to file operations, hashes, and the expressly requested LaTeX/PDF preparation. No remote job was launched. All new project files are inside this run's assigned folder; the external reviewer packets are at the temporary paths required by the brief.

SHA-256 of the final reviewed artifacts:

    STATEMENT.md   30C4580B5396B83E4FB507C8D75BB4B55AA52D3752DB5C07BD948F389AFB277E
    PROOF_v1.tex   36D2F98A64B5DC94D7127E4CA14235349C5B26B9ECB26A3349FE10119767CB19
    PROOF_v1.pdf   F6D6BC61ED6BA707C60952A7999AD90CE5890E5B6F5783E8F4293745D916A2E5

## Counts and scope

Four agents including the lead: one GPT-6 Astra high lead; one separate GPT-6 Astra xhigh statement checker (one call); two GPT-6.1 Sol high proof reviewers (one call each). Three delegated calls in total; one simultaneous proof-review round. Helpers: zero. Judges: zero. Counterexample referees: zero. Failed agent calls: zero.

D7/NL design constructions, cut groups, T22(v), endpoint propagation, schedule completion, and evidence or algorithm-output guarantees are outside this result. No theorem source, method file, THEORY.tex, README, or other proof folder was edited. The result remains **not adopted**.


## Claude audit wording fixes (2026-10-23)

Source: WAVE2_CLAUDE_AUDIT/AUDIT_T22iii_T27i.md (optional fix E-T22-1, applied). Wording only; no mathematical content changed. Final proof is now proof/PROOF_v2.tex (copy of PROOF_v1.tex) and its PDF proof/PROOF_v2.pdf; PROOF_v1.* are superseded and kept. STATEMENT.md unchanged.
- E-T22-1: in section 6 (Aggregation), after "with the cap included;", added "the actual blocks satisfy |C_b| <= B <= K, since floor(sqrt n) <= floor(n/2) for n >= 3 and floor(sqrt p) <= p, so the wave-1 hypotheses hold verbatim." followed by "Its source is ..." (sentence split).
- SHA-256: STATEMENT.md 30c4580b5396b83e4fb507c8d75bb4b55aa52d3752db5c07bd948f389afb277e; PROOF_v2.tex 72cedcae732c05c99646d368fa27c568dc80adc5434a1ff9f412aa50e54714bb; PROOF_v2.pdf 4c495b6d7cb0de6dd5b4e5baa85617fa3a45305a1fb069954dcbd1ab9289c3cf.
- pdflatex (TinyTeX), two passes: 0 errors, 0 undefined references, 7 pages. Build logs proof/build_PROOF_v2_pass1.txt, pass2.txt.

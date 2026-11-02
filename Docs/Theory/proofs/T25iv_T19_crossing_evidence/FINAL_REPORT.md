# T25(iv): final report

**Outcome: proved (Astra lead; reviewed by Sol 6.1 x2); not adopted.**

Only the conditional variance assertion of T25(iv) is proved. PW2 remains its explicit hypothesis. Both reviewers verified the unchanged `proof/PROOF_v1.tex` and `proof/PROOF_v1.pdf` in the first round, with no findings. Adoption remains Felipe's decision.

## What was proved

Given the data and successful frozen calibration, set N=N_e, W_t=Zhat_t/Z_t, and assume PW2 at every stage with nonnegative calibration-measurable rate constants a_t and slacks nu_t. Then

\[
\operatorname{Var}_{\mathcal C}(W_T)
\le B_T:=\prod_{t=1}^T(1+a_t/N_e)-1
+\sum_{s=1}^T\nu_s\prod_{t=s+1}^T(1+a_t/N_e).
\]

For the equally weighted average of four conditionally independent final islands,

\[
\operatorname{Var}_{\mathcal C}(\widehat Z/Z)\le B_T/4.
\]

The whole bound, including its slack sum, is divided by four. The particle count inside B_T remains the count per island. The result is conditional on calibration, not on passing final diagnostics.

In plain language: PW2 bounds how much each stage can increase the second moment of the evidence ratio. Accumulating those increases with their later amplification gives the stated bound. Independent island averaging reduces the variance by four.

## Statement changes and dependencies

No mathematical statement changes. `STATEMENT.md` makes the definitions, usual nonnegative rate/slack convention, conditioning, exact start, and pooling explicit. No additional hypothesis intended to establish PW2 was inserted. No statement-checker or counterexample referee was needed.

Wave-1 T12(i.a), (iii), and (iv.c) were read in `COLLECTED_PROOFS_v2.tex` and cited as proved, not adopted. They give stagewise unbiasedness and conditional independence. The proof also reproduces the first-moment induction. No unproved v3 conjecture is used as a result. T14(i) was inspected but is not needed for the reviewed proof. T09(iv) is used only in the optional investigation, with its elementary argument reproduced there.

The authoritative method's SHA-256 matches the brief:
`93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c`.
Decision Point 2 does not change this evidence recursion or pooling. The theorem files, method file, THEORY.tex, READMEs and other proof folders were not edited.

## Independent review and disposition

Exactly two fresh GPT-6.1 Sol agents, high reasoning effort, were launched together through T3 `delegate_task`, provider instance `codex`. Each received only its own isolated packet: `STATEMENT.md`, `PROOF_v1.tex`, `PROOF_v1.pdf`, and the report format. Neither received the optional investigation, proof-route hint, lead notes, lead verdict, or the other report. Both reports were back before they were archived in the project.

- Reviewer 1: **verified**, no findings. It checked finiteness, the first-moment induction without a martingale assumption, the recursion and slack indexing, and the full factor 1/4.
- Reviewer 2: **verified**, no findings. It independently checked the same conclusions and their conditional scope.

The lead inspected both reports. Fatal findings: 0; gaps: 0; exposition findings: 0. No revision and no further round were needed. `CLAIMS_OF_FATAL_FLAWS.md` records the empty finding history. No judge was used.

Exact replies: `review/REVIEWER_1_r1.md`, `review/REVIEWER_2_r1.md`. Task IDs, model settings and result metadata are in `review/LAUNCHES_r1.json` and the reviewer metadata files. Packet archives are in `review/packets/round_1/`; SHA-256 manifests are in `review/`.

## Optional PW2 investigation — partial; outside review

The derivation and limitations are in [helpers/OPTIONAL_PW2.md](helpers/OPTIONAL_PW2.md). This material was not given to the reviewers and does not share the reviewed proof's verification label.

For the actual mutation kernels, a sufficient condition at t>=2 is

\[
K_{t-1}g_t(x)\le1+\epsilon_t,\qquad
K_{t-1}(g_t^2)(x)\le1+b_t\quad\text{for every }x.
\]

Conditional iid children after multinomial resampling and mutation then imply PW2 with

\[
a_t=b_t+(N_e-1)(2\epsilon_t+\epsilon_t^2),\qquad\nu_t=0.
\]

At the first stage a_1=chi_1^2 and nu_1=0 exactly. If b_t is bounded and epsilon_t<=kappa/N_e for bounded kappa, these constants are bounded and the variance bound has the useful T/N_e scale. The note also derives explicit conservative constants from the actual independence-step minorisation, and a version with slack charged to squared-evidence-weighted exceptional histories.

These sufficient-condition implications are derived analytically in the note. Verifying their assumptions with useful constants on the profiled inputs was **not achieved**. In particular the global minorisation formula can be too conservative at a crossing. No universal useful PW2 bound for v3 is claimed.

The archived profiling report states empirical max-over-stage a_t with median **2.74** and 90th percentile **4.78**, giving a reported variance-bound scale approximately **3T/N, approximately 0.02**. It also says a_t and nu_t cannot be separated at N=2,500. Those findings support investigating PW2; they do not certify it or zero slack. They were read from the report, not recalculated here. Copies of that report and DP2 decisions and their hashes are in `helpers/source_snapshots/`.

## Validation and audit trail

The proof compiled successfully with the requested TinyTeX `pdflatex.exe`. The final build has three pages and no warnings, undefined references, or overfull/underfull boxes in its log. All three rendered pages were visually inspected for legibility and layout. The reviewers confirmed that the PDF and TeX present the same mathematical argument. The reviewed proof and statement were not edited after review.

Build command, run from `proof/`:

```text
<PC_TEMP_PATH> -interaction=nonstopmode -halt-on-error PROOF_v1.tex
```

Three successful passes resolved references after a PDF-anchor formatting correction made before review. Final compiler exit status: 0. Logs: `proof/PROOF_v1.log` and `proof/compile_stdout.txt`. Renders: `proof/page-1.png` through `proof/page-3.png`. Input/output hashes, review metadata, and packet snapshots preserve the inspected versions.

No simulation, benchmark, numerical experiment, or computational proof validation was run locally or remotely. Local operations were reading, writing, hashing, LaTeX compilation and PDF inspection. An SSH read attempt to NOTS failed with `Connection timed out during banner exchange` and `Connection to UNKNOWN port 65535 timed out`; a later read-only Owls connection succeeded. The local archived DP2/profiling reports supplied the evidence discussed above. Raw profiling runs were not revalidated.

Agent counts: 1 GPT-6 Astra high lead; 2 GPT-6.1 Sol high reviewers, 2 delegated calls total; 0 helpers; 0 statement checkers; 0 counterexample referees; 0 judges. Review rounds: 1.

Final proof: [PDF](proof/PROOF_v1.pdf), [LaTeX](proof/PROOF_v1.tex). Precise statement: [STATEMENT.md](STATEMENT.md). Run complete; no unresolved review findings.


## Claude audit wording fixes (2026-10-23)

Source: WAVE2_CLAUDE_AUDIT/AUDIT_T21_T25iv.md. Wording only; no mathematical content changed. Final proof is now proof/PROOF_v2.tex (copy of PROOF_v1.tex) and its PDF proof/PROOF_v2.pdf; PROOF_v1.* are superseded and kept. STATEMENT.md unchanged.
- E5 (required): after eq. (rec) in section 3 of the proof, added: "By (increment), PW2 is equivalent to the recursion M_t <= (1+a_t/N)M_{t-1}+nu_t. The theorem therefore adds no control of the evidence beyond PW2 itself; all of its substance lies in establishing PW2 with useful constants, which is not done here."
- Skipped by instruction: E6, E7 (optional).
- SHA-256: STATEMENT.md f0f793adc40c4491d1f0460e6d580d267ee17775c91bcece70c04156811802dd; PROOF_v2.tex 4f8d827f1d8a4ab10f44d87488fadf358da4654c737d50798512562044a3a1ca; PROOF_v2.pdf a9a75ebad8be57c103da2d51dcbc738a593c8b4600fdbedc70ad8a46b6e18823.
- pdflatex (TinyTeX), two passes: 0 errors, 0 undefined references, 3 pages. Build logs proof/build_PROOF_v2_pass1.txt, pass2.txt.
- Line diff PROOF_v1.tex -> PROOF_v2.tex is four added lines only.

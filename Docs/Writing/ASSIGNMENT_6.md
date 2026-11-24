# Writing Department: Assignment 6, the owner-review edition (HQ, 2026-11-23; owner's request)

## Purpose (owner, binding)
The owner will review this document **himself**: "I need to review myself that the assumptions make sense and that
the theorems look natural and intelligible." Write it for that reader. Every assumption should let him judge
"does this make sense?", and every theorem should let him judge "is this natural, and can I follow it?" Clarity
rules from ASSIGNMENT_1 (plain words first, symbols second, one idea per paragraph, no internal ids) still bind.

## Base
Update the unified manuscript: `manuscript/manuscript.tex` at main 193ede8a (= `manuscript_A5final_famc` plus the
Result 3 scope rider). Don't start from scratch. Keep its notation and numbering where possible.

## Contents (in this order)
1. **The model and the priors.** What we set and why: the likelihood, the prior on the coefficients, the
   model-size prior (including the cap at K), and every hyperparameter with its default value. Give a short reason for
   each choice, and a pointer to the code location (keep this in the appendix table).
2. **The sampler.**
   - The SMC-BVS algorithm as coded: the stages and moves, and how to read the outputs (HPM, MPM, PIPs, evidence).
   - A short, clearly separated subsection on the parallel 1M engine as frozen (tag `p1m-freeze-F2`: N, refine_m,
     I_max, R′, the islands). Get it from `Docs/Experiments/P1M/` and `exp/P1M/GC_PREREG`.
   - Say plainly which parts the theorems cover and which are engineering.
3. **The assumptions.** Give one table, and for each assumption:
   - (a) the statement;
   - (b) what it means in plain words;
   - (c) what it rules out;
   - (d) **a short comment on whether it is reasonable**, for real designs, with an example where one exists;
   - (e) **the comparison with Song & Liang (2015), the split-and-merge paper.** Is our assumption the same as theirs,
     weaker, stronger, or without an analogue? Cite their condition number and page, verified on the PDF.

   Reuse §5 and the precedent notes from Assignment 5; don't rewrite them.
4. **The theorems: the most important first.**
   - **Ordering:** what is proved comes before what is planned.
   - **What to give for each theorem:** a plain-words version, the formal statement, a status line (outside the
     theorem environment), and one sentence on why it is natural or what it says that a statistician would expect.
   - **Planned results:** list each in its own clearly labelled section. Mark them PLANNED, not claimed, so that
     nothing planned reads as proved. The list:
     - the trap theorem: a mixing lower bound for single-flip MCMC (and wTGS) on a multimodal design, plus our
       consistency on the same design;
     - coverage at p = 10⁷;
     - Lean certificates of the key results;
     - the named open items in `Theory_work/Dept/QUEUE.md`.
   - **Minor results:** keep them in the supplement, with one line each.
5. **Statuses:** current. Diff the registry on main against the freeze tag `theory-v2026-11-freeze`, and quote any
   change since 11-17. Theory is on hold, so read their files and don't wake their threads. If something is unclear,
   write it down as an open question for HQ.

**Not in scope:** the 1M results and the benchmarks (they belong to the regroup), and new theory.

**Length:** the owner's reading time matters more than the page limit. Aim for a main text of about 20 pp or less,
with the supplement behind it.

## Staffing and checks (token-lean; owner rule)
- The Opus manager writes, merges and decides; Sonnet helpers do the requotes, the status diff and the table filling.
- One fresh Opus clarity read before delivery (the ASSIGNMENT_1 procedure), aimed at the owner's two questions.
- One scoped gpt-6.2-sol fidelity read at the end. Its scope: the theorem statements, the statuses, the Song–Liang
  sentences, and the parameter table against the code. Log it in SOL62_QUALITY.md.
- Use no Fable unless the manager hits a real wording problem; that would be one call, reported to HQ.

## Reporting
- To HQ (thread 647bfd65, environment 1fde6176): one start line with an ETA, then one delivery line with the
  PDF path. Nothing in between unless you are blocked.
- Push to main when done, with the PDF named `manuscript/manuscript_owner_review_<date>.pdf`.

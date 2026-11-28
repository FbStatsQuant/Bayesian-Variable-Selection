# Writing Department: Assignment 7, the formal specification (HQ, 2026-11-24; owner's request)

## Purpose (owner, binding)
The owner asked for "a very organized pdf where we define the model, the distributions, the sampler, all
assumptions, and then we write all official statements of the theorems we are planning on proving."

This is a **reference specification**, not a paper and not a review edition. Write it definitions-first and in
mathematical form, with a fixed order and numbering and nothing extra. It is the single place where every object
and every official statement is written down once.

## Base
- Take the content from the A6 owner-review edition (main 248c452a, `manuscript/owner_review.tex`)
  and from the registry on main.
- Don't re-derive anything, and use the notation of A6.
- Keep it as a separate document: `manuscript/spec/spec.tex`.

## Contents (in this order, numbered sections)
1. **Notation and setting.** The data and the design, model indices γ, |γ|, X_γ, the asymptotic regime (n, p = p_n,
   with every rate parameter named), and the true model S₀.
2. **The model.** The likelihood and the parameters, as definitions.
3. **The distributions.** Each one is a numbered definition with its density or mass function written out:
   - the coefficient prior and the variance prior, if any;
   - the model-size prior with the cap K;
   - the marginal likelihood and the posterior over models;
   - the tempered target sequence the SMC sampler uses (the schedule, as coded);
   - the hyperparameter table with the default values.
4. **The sampler.**
   - SMC-BVS as coded, written in `algorithm` environments: initialisation, reweighting, the adaptive tempering rule,
     resampling, and the move kernels with their acceptance probabilities.
   - The outputs, as definitions: HPM, MPM, PIPs and the evidence estimate.
   - The 1M parallel engine (tag `p1m-freeze-F2`) gets a short separate subsection. It is marked as engineering, not
     covered by the theorems, and lists only its differences from the algorithm above.
5. **The assumptions.**
   - Every assumption used by any theorem in §6, in a numbered `assumption` environment, with its exact formal
     statement. Give each one stable labels, with A6's labels kept.
   - Close with one table: each assumption against the theorems that use it.
   - No commentary: the reasonableness and Song–Liang discussion stays in A6.
6. **The official theorem statements.**
   - Every headline theorem of the program in one `theorem` environment each, with the assumptions it uses cited by
     label.
   - Each theorem gets one status tag outside the environment: PROVED (with its registry id) or PLANNED.
   - The order is proved first, then planned, and within each group from the most important down.
   - The PLANNED ones get an official statement where the target is fixed:
     - the trap theorem;
     - coverage at p = 10⁷;
     - the open items in `Theory_work/Dept/QUEUE.md` that are headline-level.
   - Where a choice is still open (A6 §8.2: the trap design family and its target result; what "coverage at
     p = 10⁷" means; the leakage set Q), give the candidate statement and mark the open choice in a box. Don't pick
     it silently.
   - The supplementary results go in a final section, as statements only.
   - **No proofs and no proof sketches.**

**Not in scope:** proofs, the reasonableness comments, the Song–Liang comparisons, results and benchmarks, and new
theory. Theory is on hold: read their files, don't wake their threads, and put open questions in an appendix for HQ.

**Length:** whatever the content needs. Clarity of structure matters more than page count.

## Staffing and checks (token-lean; owner rule)
- The Opus manager writes and decides; Sonnet helpers transcribe definitions and statements from the A6 tex and the
  registry.
- Run one scoped gpt-6.2-sol fidelity read at the end. Its scope: every definition and algorithm step against the code,
  and every theorem and assumption statement against the registry, verbatim. Log it in SOL62_QUALITY.md.
- No Opus clarity read; no Fable.

## Reporting
- To HQ (thread mcp:4f1a2e12-7ac4-4619-9128-1469ea92eb2e, environment 1fde6176): one start line with an ETA, then one
  delivery line with the PDF path. Nothing in between unless you are blocked.
- Push to main when done, with the PDF named `manuscript/spec/smc_bvs_spec_<date>.pdf`.

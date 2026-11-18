# Brief: Sol diff check of the FINAL §6 in-place erratum (IDEAL-W⁺ batch)

Prepared 2026-11-16 06:25 CST by the Theory Dept implementation sub-agent (Claude Opus 5.5).
Reviewer: gpt-6.1-sol, reasoning high. This is one fresh review of one patch.

## Rules
- You are a **fresh, read-only** reviewer. Edit no file except your one reply file below.
  - Do not commit, and do not touch any other worktree.
  - Do not change the registry.
  - Do not apply the patch to the real files.
- **D62 (verbatim):** "Do not write any file outside the worktree and set no TMPDIR. Scratch only in /home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/, deleted at the end."
- Write your reply to `Theory_work/Dept/research/IDEALW_BATCH/DIFF3_sol.md`, inside the worktree
  `/home/fb31/BVS-wt/THEORY-DEPT`.
- The last line of the reply is `DIFF: PASS` or `DIFF: FAIL`. Use FAIL only for a concrete defect in this patch, and give a
  concrete repair with it: the exact replacement text, keeping the same line count for in-place lines.

## Background
The shipped code has two LS0 cap rejection validators:
- `le > 1e6`, at `Scripts/SMC_BVS/core/v3_run.R:96`;
- `cap_ll > numeric_limits<int>::max()` with cap_ll = ℓ_n + |S̃₀|, at `Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`.

IDEAL-W does not exclude them, so every-n delivery claims about shipped code are false under plain IDEAL-W (Sol TR1). The
batch, which you do not re-review, narrowed 19 registry claims to two clauses:
- (a) P(no output)=0 on the bounded domain 𝔇 under IDEAL-W;
- (b) every n, and every asymptotic delivery conclusion, under A:IDEAL-W⁺.

The FINAL chapter's §6 states two propositions that are **not** registry rows:
- Proposition F in its corrected form (cap a_n = ℓ_n + |S̃₀|, with the allocation addition for head `493579a`);
- Proposition F-GROW.

HQ ordered an in-place FINAL erratum for these. The C-DLV-form Proposition F (cap ℓ_n, the specified method) is meant to stay
unchanged as spec-level.

## Inputs
1. **The patch.** `Theory_work/Dept/research/IDEALW_BATCH/patches/ERRATUM__FINAL__s6_delivery.tex.patch`. It is a unified
   diff against origin/main `8431b575` and touches `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex` and `s8_scope.tex`.
   Read the base with `git show origin/main:<path>`.
2. **The prep note.** `Theory_work/Dept/research/IDEALW_BATCH/ERRATUM_FINAL_s6.md`. It gives the before/after text, the list of
   FINAL sentences checked and the registry-span check. Judge it independently.
3. **The defect finding.** `Theory_work/Dept/research/FUNI_transfer/TR1_sol.md`; read all of it. §1 gives the failing
   inference and the counterexample; §2 gives the supported claims and 𝔇.
4. **The assumption.** `Theory_work/Dept/research/FUNI_NARROW/A_IDEALW_PLUS.md:10`, the final text, to be used verbatim
   (LaTeX transcription only). IDEAL-W itself is `Theory_work/Wave1C/C-DLV/STATEMENT.md:24-25` and is unchanged.
5. **The form precedent.** `Theory_work/Dept/research/IDEALW_BATCH/DIFF2_sol.md` (PASS), and in particular its treatment of
   `patches/HQ_AUDIT-W1C__A2_propF_GROW.md.patch`. That patch is A2, the source of Proposition F-GROW; its (a)/(b) wording
   is the wording to match.
6. **The FINAL proof chain** for the two propositions:
   - `Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md` (corrected statement `:60-75`);
   - `A2_propF_GROW.md` and `A3_check_A2.md`;
   - `A4_postcouncil_check.md:7-25`;
   - `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md` and `L1_resources.md`.
7. **The code.**
   - `Scripts/SMC_BVS/core/v3_run.R:93-101`.
   - `Scripts/SMC_BVS/core/cpp/v3_core.cpp:465-476`.
   - `Scripts/SMC_BVS/core/v3_fit.R:120-131`, where the exact branch returns first.
   - The lines are the same at `493579a` (`git show 493579a:<path>`).
8. **The registry, for the span check.** `Theory_work/INFRA/registry/claims.tsv` on origin/main, with its `file`, `lines`,
   `premises`, `status_source` and `tex` columns. W1C-FINAL:Lemma-CAP is at `s7_impl.tex:45-56`.

## Questions
(a) **Truth and support.** For each restricted sentence, is it true, and is it supported by the FINAL proof chain under
clause (a) on 𝔇 with IDEAL-W, and under clause (b) with A:IDEAL-W⁺? The restricted sentences are:
- `s6:4`, the summary;
- `s6:46`, Proposition F in its corrected form;
- `s6:54`, Proposition F-GROW;
- `s6:56`, the proof outline, steps (2) and (3);
- `s8:9`, the scope item.

In particular:
- Does every asymptotic conclusion, P(Ŝ=S₀)→1 included, sit only under (b)?
- Is the 𝔇 bound argument in the appended erratum correct for the shipped cap ℓ_n + |S̃₀|?
- Is the definition verbatim?

(b) **Anything else.** Did anything else change, or is anything missing?
- Is there another every-n delivery sentence about shipped code in `Theory_work/Wave1C/FINAL/` that the patch misses?
  Section 3 of the prep note lists what was checked.
- Is anything changed that should not be? The C-DLV-form Proposition F, Theorem D and Corollary D′ are meant to be unchanged.
- Does the erratum paragraph contain the required sentence "IDEAL-W never covered the application-level rejection
  predicates; IDEAL-W⁺ is the explicit form", dated 2026-11-16, and cite the two code lines?

(c) **Spans.** Does any registry span move? Is the prep note's account of C-DLV:Prop-F's `tex` pointer (`s6:28-47`, no
`tex_sha256`, content changed at `:46`) accurate? Is it acceptable as a flagged re-check item rather than a defect?

End with the single line `DIFF: PASS` or `DIFF: FAIL`.

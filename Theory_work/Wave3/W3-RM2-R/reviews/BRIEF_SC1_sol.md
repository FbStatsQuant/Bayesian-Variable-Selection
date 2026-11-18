# BRIEF SC1 — statement-change check, W3-RM2-R (Sol, gpt-6.1-sol, reasoningEffort high; new agent)

You check one change to a delta statement (PROTOCOL_v4 §4.2). Work read-only in `/home/fb31/BVS-wt/W3-RM2-R` (paths
relative to it); write nothing; do not change git state. Do not read `LOG.md` or other files under
`Theory_work/Wave3/W3-RM2-R/reviews/` than those named here.

## Material
- The diff: `Theory_work/Wave3/W3-RM2-R/reviews/SC1_diff_v0.1_v0.2.diff` (STATEMENT v0.1 at commit c0b61cb → v0.2 on disk).
- The finding list that triggered it: `Theory_work/Wave3/W3-RM2-R/reviews/SL1_statement_lock_sol.md` §2 (findings 1–5 only)
  and the lead's disposition `Theory_work/Wave3/W3-RM2-R/reviews/SL1_disposition.md`.
- The statement as it now stands: `Theory_work/Wave3/W3-RM2-R/STATEMENT.md` (v0.2); `PLAN.md` row Q5.
- Sources for the changed parts: `Scripts/SMC_BVS/core/v3_fit.R` (input validators ~85-100), `v3_preprocess.R:1-20, 95-120`,
  `v3_run.R:85-110`, `cpp/v3_core.cpp:460-480`; `Theory_work/Wave1C/C-DLV/STATEMENT.md:10-45`, `lemmas/L4_delivery.md`;
  `Theory_work/Wave3/API_AUDIT/pass1/R-AUD1_sol.md`, `API_AUDIT/pass1/TRIAGE.md:23-28`; RM `Theory_work/Wave3/W3-RM/STATEMENT.md:160-176`
  and `Theory_work/Wave3/W3-RM/lemmas/L0_core.md`; Lemma E4 at RM `STATEMENT.md:219-230`.

## Questions
1. Is each of SL1 findings 1–5 resolved by the diff? If not, what remains.
2. Does the diff break anything else in the statement (dependents: (C0⁺)(a′)/(b⁺)/(c⁺), (C-D), (C1⁺), (C2⁺), the
   dependency table)? In particular: is St_n(𝓛′) = {[S₀, S̃₀] ⊆ 𝓛′} correct, and is Sand_n(𝓛′) ⊆ St_n(𝓛′) correct
   given E4? Is IDEAL-W⁺ stated precisely enough to be audited (is "representability guard" well defined; are the two
   named guards the right lines; is the supported domain 𝔇 correctly computed from them)? Are there other explicit
   code guards on the `v3_fit` call graph at the pin that compare a size-derived quantity with a fixed limit and are
   neither input validators nor covered by MACH/allocation? (A list with file:line is the most useful answer.)
3. Tag each change STRONGER / WEAKER / EQUAL / NEW-CLAIM relative to v0.1, per clause.
4. Findings tagged C/S/F/E with line and fix. Verdict: ACCEPT / ACCEPT WITH CHANGES / REJECT.

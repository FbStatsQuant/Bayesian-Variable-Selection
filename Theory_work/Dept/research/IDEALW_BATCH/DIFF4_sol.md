# FINAL §6 erratum — independent R1 re-check

**PASS. R1 fully repairs the two omitted §2 consistency summaries. I found no new concrete defect in the complete proposed patch.** This verdict retains the proof chain's existing statistical, implementation and audit qualifications.

I first ran `git fetch -q origin`. Fetched `origin/main` is `8431b57532c979903138021f9ed8eb57cec7a650`; the worktree is on `dept/theory`. I read BRIEF_DIFF4, BRIEF_DIFF3 and their required inputs, including all of TR1, the final assumption paragraph, DIFF2 and its A2 precedent, A1–A4, and C-DLV L1/L4. I read DIFF3 but independently checked its prior PASS findings. All patch reconstruction and checks used memory against `git show origin/main:<path>`; no patch was applied.

In the references below, s2, s6 and s8 denote [s2_map.tex](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/FINAL/sections/s2_map.tex), [s6_delivery.tex](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/FINAL/sections/s6_delivery.tex) and [s8_scope.tex](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/FINAL/sections/s8_scope.tex). Line numbers describe the reconstructed result.

**(a) Truth and support — PASS.** Clause (a) supplies delivery on the sufficient bounded domain 𝔇 under IDEAL-W, with all other premises retained. Clause (b) supplies every-admissible-n delivery under A:IDEAL-W⁺; unconditional asymptotic consistency additionally uses the stated class hypotheses.

| Restricted location | Independent assessment |
|---|---|
| s6:4, summary | Correctly distinguishes bounded-domain delivery from every-admissible-n delivery, retaining the total-fallback qualification and references to the propositions. |
| s6:46, corrected Proposition F | Both delivery clauses follow after excluding the two extra validators. The unconditional consistency limit is expressly under (b), with the class hypotheses, probability law and inherited qualifications preserved. The original-cap sentence is an unchanged resource statement. |
| s6:54, Proposition F-GROW | Matches the accepted A2 (a)/(b) form. Its consistency limit is in (b), and it inherits FINAL's complete strengthened allocation. The erratum's express restriction of every asymptotic delivery/consistency conclusion above it also covers the preceding fixed-p enumeration sentence. |
| s6:56, proof steps (2)–(3) | Correctly repairs the failed exit-walk inference: the two additional validators must be excluded separately, by 𝔇 or A:IDEAL-W⁺. The use of P(𝒪)=1 for unrestricted consistency is explicitly marked “every n; clause (b)”. The data-event and posterior limits retain their own statistical hypotheses. |
| s8:9, scope item | Accurately summarizes the two delivery domains and retains the fallback, allocation and class restrictions. |

The deterministic bound is valid for the shipped cap, including the start-mode addition:

```text
le = ℓ_n ≤ ℓ_raw ≤ 10⁶,
cap_ll = ℓ_n + |S̃₀| ≤ ℓ_raw + K
       ≤ ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1.
```

Here p ≤ p_raw and feasibility gives |S̃₀| ≤ K = min(p,⌊n/2⌋). Both upper rejection tests are strict, so equality passes. I checked [v3_run.R:93](/home/fb31/BVS-wt/THEORY-DEPT/Scripts/SMC_BVS/core/v3_run.R:93), [v3_core.cpp:465](/home/fb31/BVS-wt/THEORY-DEPT/Scripts/SMC_BVS/core/cpp/v3_core.cpp:465), and the earlier exact-branch return at [v3_fit.R:120](/home/fb31/BVS-wt/THEORY-DEPT/Scripts/SMC_BVS/core/v3_fit.R:120); these ranges agree at origin/main and `493579a`. The exact branch reaches neither validator. Thus 𝔇 is sufficient, not necessary. Its integer dimension bounds make it bounded, so (a) supplies no general n→∞ conclusion.

Under (b), the two predicates are false by the explicit idealisation, not by increased resources. The full appended definition matches [A_IDEALW_PLUS.md:10](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/FUNI_NARROW/A_IDEALW_PLUS.md:10) verbatim modulo LaTeX transcription and mathematical spacing. It retains the lower/type/finiteness/integrality conditions, all other validators, the distinct 10⁶-maximiser enumeration cap and tie-aware DP fallback, and all other method/fallback caps. Original IDEAL-W is unchanged.

The proof support survives independent inspection. [A1](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md) charges at most Kq(p) extra LS0 score requests and the extra archive through W_G/M_G. [L1](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/C-DLV/lemmas/L1_resources.md) and [L4](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md) supply resource exclusion and the complete frozen fallback argument. FINAL already includes [A4's](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/HQ_AUDIT/A4_postcouncil_check.md:7) extra shipped preflight bounds P_e+A and P̄_LS0. In particular, MACH bounds the entire timed interval, giving ŝ_K ≤ (τU_K+τ₀)/200 and 2sq(p)ŝ_K ≤ P̄_LS0; memory is checked before benchmarking. This covers the specification-versus-shipped allocation limitation flagged for A2 in DIFF2.

For F, the longer deterministic LS0 search contains the smaller-cap scored set, preserving discovery. For F-GROW, [A2](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/HQ_AUDIT/A2_propF_GROW.md) and [A3](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/HQ_AUDIT/A3_check_A2.md) give discovery directly on Sand ∩ NA ∩ TL, and T03♯ or the iid design-event/diagonal argument supplies E[1−π(S₀)]→0. D′ then gives

```text
P(output and Ŝ≠S₀) ≤ 2E[1−π(S₀)] + P(𝒦_nᶜ) → 0.
```

Combining this with every-n delivery in (b) yields unconditional consistency. The patch neither infers discovery from D_n→0 in the wrong direction nor introduces CAL or a fallback-probability bound. Existing dependency and code-reading qualifications remain essential.

**(b) Scope and completeness — PASS.** The only existing-line changes are s6:4,46,54,56; s8:9; and s2:18,31. Four new physical lines occur after old s6:63, containing the dated erratum and full assumption definition. No status token changes. Theorem D, Corollary D′, their setting/allocation, and the C-DLV-form Proposition F remain unchanged as requested; the erratum explicitly identifies their specified-method scope. The required sentence “IDEAL-W never covered the application-level rejection predicates; IDEAL-W⁺ is the explicit form” appears in LaTeX, dated 2026-11-16, with the correct two code-line citations.

I independently searched all ten requested TeX files, including `consistency.tex` and every section, for delivery/no-output/fallback wording, IDEAL-W, output qualifiers, consistency wording and limits to 1 or 0, and inspected the relevant claims in context. I found no further unrestricted every-n or general asymptotic shipped-delivery summary missed by this patch. The separate §7 cap-guard correction is discussed under (d).

**(c) Spans and metadata — PASS.** Every unified-diff hunk matches its base context and declared counts. The reconstructed line counts are s6 63→67, s8 19→19 and s2 32→32; every surviving original line keeps its position. I reproduced the prep note's patch hash, `785ce861222bb4a9c28a983e535f5da2112750ea3fa738e7d5879fb8a26f08af`, and all three before/after whole-file hash pairs.

I checked origin/main's registry references, including the `file`, `lines`, `premises`, `status_source`, `tex` and `tex_sha256` fields of [claims.tsv](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/INFRA/registry/claims.tsv). Only C-DLV:Thm-D and C-DLV:Prop-F point into the touched files, through `tex`; the corresponding events.log entries are historical. No registry file references s2. W1C-FINAL:Lemma-CAP's statement 45–56, premises 36–43 and status source 64 remain in untouched s7. No registered span moves.

C-DLV:Thm-D's s6:11–13 transcription is byte-identical. C-DLV:Prop-F's s6:28–47 span retains its position but changes at :46: its computed hash changes from `fbaef3a19ee505f9859b83f35bbc17d721ba174e6ebf187c616cb729fea74f43` to `2c01f75dd9be259ef61c4e757901b9fafdbd240f27232221383b918393cc5b2a`. Its stored `tex_sha256` is empty; no stored transcription hash becomes stale, and [check.py:388](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/INFRA/tools/check.py:388) continues to flag the unreviewed transcription. The registered Markdown statement and premises are unchanged. The prep note's “no hash changes” is accurate for stored registry hashes, not the computed TeX-span hash. The pre-existing C-DLV-form/corrected-form pointer mismatch is acceptable as the explicitly flagged HQ transcription re-check item, not a defect of this patch.

**(d) R1 and remaining chapter summaries — PASS.** Both replacement lines in s2 match DIFF3's exact repair blocks verbatim. Line 18 now puts P(Ŝ=S₀)→1 under A:IDEAL-W⁺ and clause (b) of §6; line 31 likewise replaces the old IDEAL-W premise description with A:IDEAL-W⁺ and clause (b). Their other claims and statuses are preserved. The added s6:65 clause accurately records that repair and introduces no new claim or defect.

The independent search found the remaining hits to be scoped references, questions, necessary conditions, status/provenance records, exact-posterior results, or results still intersected with output. Specifically, s1:32 lists premises and :35 poses delivery as a question; s2:24 and s5:95 point to the now-restricted propositions; s5's reported-model conclusions remain joint with output; s7:72 refers to Proposition F's consistency clause and states a necessary allocation condition, and :81 likewise states necessity; s8:6 preserves the proposition's stated scope and :14 states the still-necessary IDEAL-W premise. None asserts that these listed conditions alone prove unrestricted shipped delivery.

The unpatched base does still say at [s7_impl.tex:39](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/FINAL/sections/s7_impl.tex:39) that IDEAL-W excludes the cap-range exit. As the brief specifies, that distinct error is already repaired by the separate [E4 patch](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/IDEALW_BATCH/patches/ERRATUM__W1C-FINAL__sections_s7_impl.tex.patch), accepted in DIFF2. I inspected that correction and did not count it as a newly missed summary or require duplicating it here. This PASS concerns the proposed §6/R1 diff in that stated batch context, not the untouched base as a finished corrected chapter.

No repair text is required: no concrete defect remains in this review's scope. Only this reply file was written. No source/patch or registry was edited, no other worktree was touched, no commit was made, and no subagent was started. No scratch files or directory were created and no TMPDIR was set.

DIFF: PASS

# FINAL §6 erratum — fresh diff review

**One concrete scope defect remains: the patch leaves two explicit asymptotic consistency summaries in §2 under the old machine-premise wording.** The five edited lines themselves pass the truth/support check. No defect was found in the domain bound, assumption transcription, allocation or span preservation.

I ran `git fetch -q origin` first; fetched `origin/main` is `8431b57532c979903138021f9ed8eb57cec7a650`. I read all required inputs, including the complete TR1 finding and the A2 precedent accepted in DIFF2. I reconstructed this patch in memory against `git show origin/main:<path>`, without applying it to any real file.

**(a) Truth and support of the restricted sentences — PASS, with the inherited qualifications.** Here `s6` denotes [s6_delivery.tex](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/FINAL/sections/s6_delivery.tex), and `s8` denotes [s8_scope.tex](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/FINAL/sections/s8_scope.tex).

| Patched location | Independent assessment |
|---|---|
| `s6:4`, summary | Correctly limits plain IDEAL-W delivery to 𝔇 and every-admissible-n delivery to A:IDEAL-W⁺, with the total fallback and the propositions' other premises retained. |
| `s6:46`, corrected Proposition F | Both delivery clauses are supported. The unconditional consistency assertion is explicitly under (b), with the original class hypotheses, probability law and dependency qualifications preserved. The original-cap sentence remains a resource statement. |
| `s6:54`, Proposition F-GROW | Matches A2's accepted (a)/(b) form. Both delivery clauses follow with FINAL's imported allocation, and the displayed consistency limit is within (b). The appended erratum also places every asymptotic delivery/consistency conclusion above it in §6 under (b), including the preceding fixed-p enumeration sentence; clause (a) supplies no asymptotic conclusion. |
| `s6:56`, proof steps (2)–(3) | The exit-walk inference is now conditional on excluding the two additional validators, on 𝔇 or by A:IDEAL-W⁺. The use of P(𝒪)=1 for unrestricted consistency is explicitly assigned to (b). The data-event and posterior limits retain their own statistical hypotheses. |
| `s8:9`, scope item | Correctly summarizes the two delivery clauses and preserves the fallback, allocation and class restrictions. |

The shipped-domain calculation is correct, including the added start-mode term:

```text
le = ℓ_n ≤ ℓ_raw ≤ 10⁶,
cap_ll = ℓ_n + |S̃₀| ≤ ℓ_raw + K
       ≤ ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1.
```

This uses p ≤ p_raw, feasibility |S̃₀| ≤ K and K = min(p,⌊n/2⌋). Both upper tests are strict, so equality passes. The code at [v3_run.R:93–101](/home/fb31/BVS-wt/THEORY-DEPT/Scripts/SMC_BVS/core/v3_run.R:93) and [v3_core.cpp:465–476](/home/fb31/BVS-wt/THEORY-DEPT/Scripts/SMC_BVS/core/cpp/v3_core.cpp:465) agrees at origin/main and `493579a`. The exact branch returns first at [v3_fit.R:120–131](/home/fb31/BVS-wt/THEORY-DEPT/Scripts/SMC_BVS/core/v3_fit.R:120). Consequently 𝔇 is sufficient, not necessary. Its integer dimension bounds make it bounded; it cannot justify a general n→∞ conclusion.

Under (b), the two rejection predicates are false by assumption, rather than by more allocation. The full appended definition matches [A_IDEALW_PLUS.md:10](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/FUNI_NARROW/A_IDEALW_PLUS.md:10) verbatim modulo LaTeX transcription and mathematical spacing. I checked the complete paragraph after reversing its LaTeX formatting. It preserves the other validator conditions, the start-mode enumeration-to-DP fallback, and every other method/fallback cap. Original IDEAL-W is unchanged.

The proof support is substantive: [A1](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md) adds at most Kq(p) LS0 score requests and supplies W_G/M_G; [L1](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/C-DLV/lemmas/L1_resources.md) and [L4](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md) provide the resource exclusion, total-fallback grid argument and pathwise scored-set inequality. FINAL already includes [A4's](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/HQ_AUDIT/A4_postcouncil_check.md:7) additional head-code preflight bounds P_e+A and P̄_LS0. In particular, ŝ_K ≤ (τU_K+τ₀)/200 makes 2sqŝ_K ≤ P̄_LS0, and the memory allocation covers the archive before benchmarking. Thus the pre-existing A2 specification-versus-shipped allocation limitation identified in DIFF2 is covered here by FINAL's explicit stronger allocation, also inherited by F-GROW.

For consistency, A1 preserves the smaller-cap discovery event through the longer search's prefix property. [A2](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/HQ_AUDIT/A2_propF_GROW.md) and [A3](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/HQ_AUDIT/A3_check_A2.md) instead supply GROW's direct Sand ∩ NA ∩ TL discovery argument, plus T03♯ or the iid design-event/diagonal argument for E[1−π(S₀)]→0. D′ gives

```text
P(output and Ŝ≠S₀) ≤ 2E[1−π(S₀)] + P(𝒦_nᶜ) → 0.
```

Adding every-n delivery under (b) gives unconditional consistency. No inference from D_n→0 in the wrong direction, CAL premise, or fallback-probability bound is introduced. The existing code-reading and dependency qualifications remain essential.

**(b) Completeness — FAIL for one omitted-summary issue at two locations.** The prep note's §3 inventory misses both [s2_map.tex:18](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/FINAL/sections/s2_map.tex:18) and [s2_map.tex:31](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave1C/FINAL/sections/s2_map.tex:31):

- Line 18 directly asserts P(Ŝ=S₀)→1 “without the output qualifier (ideal machine, amended allocation)” for the patched calibration and the F/F-GROW classes.
- Line 31 again asserts consistency without the output qualifier, expressly listing “Props. F and F-GROW: IDEAL-W, MACH, amended allocation”.

These are affirmative asymptotic, delivery-dependent summaries, not merely a question, status record or theorem pointer. The latter still names the insufficient original idealisation. The §6 erratum qualifies the conclusions above it in that section; it does not expressly repair the separate §2 summaries. Referencing F/F-GROW while retaining their old premise description leaves a contradictory summary of the narrowed guarantees. For admissible sequences that continue to use SMC, ℓ_n eventually exceeds 10⁶, so the original IDEAL-W and ample resources cannot supply the delivery needed by these unconditional limits (TR1 §1–§2). Thus not every asymptotic delivery conclusion in FINAL is clearly restricted to (b).

I found no additional literal every-n shipped-delivery sentence beyond the five edited locations and the separate s7 cap-range erratum already covered by E4/DIFF2. The other hits in s1, s5, s7, s8 and the provenance/front matter are questions, joint-with-output claims, necessary allocation conditions, scoped references or status records. Theorem D, Corollary D′ and the C-DLV-form Proposition F remain unchanged as requested. No status token is added or altered. The appended paragraph is dated 2026-11-16, contains “IDEAL-W never covered the application-level rejection predicates; IDEAL-W⁺ is the explicit form” in LaTeX, and cites both required code lines correctly.

**Exact repair.** Add two line-for-line replacement hunks to the proposed patch for `Theory_work/Wave1C/FINAL/sections/s2_map.tex`. Each block below is exactly one physical replacement line; leave every other line unchanged.

Replace line 18 with:

```latex
Thm S, MAP (supplement) & ``establishes the consistency of MAP models'' — exact hypotheses \textbf{NOT INSPECTED} & exact HPM: SL0(iv), SL1(c). \textbf{Reported} $\Shat$, jointly with output: LH-iid (Thm~\ref{thm:PXN}), GEN class (Thm~\ref{thm:GEN}), growing relevance sets incl.\ study S2 (Thm~\ref{thm:GROW}), misspecified candidate sets (Cor.~\ref{cor:MISD}); without the output qualifier (ideal machine with A:IDEAL-W$^{+}$, amended allocation; clause (b) of §\ref{sec:delivery}) $\PP(\Shat=S_0)\to1$ for the patched calibration on LH, LH-iid, GEN class (Prop.~\ref{prop:F}) and the GROW class (Prop.~\ref{prop:FG}) & W1-PXN, W1-GEN, C-GROW, C-MIS \st{PROVED-CHECKED}; C-DLV \st{PARTIAL}; Prop.~F with cap $\ell_n$ (C-DLV form): \st{PROVED-CHECKED for the patched calibration law}; corrected form with cap $a_n$ (Prop.~\ref{prop:F}): A1 \st{HOLDS-WITH-AMENDMENTS}; checked in full by the final council, round 3 PASSED (Sol 9.3, Opus 8.6); GROW extension (Prop.~\ref{prop:FG}): \st{PROVED (A2), checked by A3}; checked in full by the final council, round 3 PASSED (Sol 9.3, Opus 8.6) \\
```

Replace line 31 with:

```latex
Every correctly specified Song--Liang \emph{selection} result (Thm~3, $\xi_q$, MAP) has an exact-posterior analog that is a one-line consequence of $1-\pi(S_0)\to0$ (Lemma SL0, deterministic), with rate $\sqrt{\log n/n}$ for $p\le n^A$ and with specificity added. Beyond Song--Liang, the method's \emph{reported} model is proved consistent jointly with output on a general correlated class (GEN), on growing relevance sets including the study's AR(1) design (GROW), and under misspecification (C-MIS Cor.~D), and, on LH, LH-iid, the GEN class and the GROW class, with a total tier-1 calibration fallback, also without the output qualifier, on an ideal unit-cost machine with a declared polynomial allocation (Props.~F and F-GROW, clause (b): A:IDEAL-W$^{+}$, MACH, amended allocation; not checked for the C-MIS setting). Gaps: Hellinger/predictive contraction and exponential rates; exponential $p$; shipped pooled $R'=4$ PIPs; Theorem~S's hypotheses not inspected; density-level misspecification.
```

These replacements put both unconditional consistency summaries explicitly under (b), preserve their other conclusions/statuses, and retain the file's line count. Refresh the prep note's changed-location inventory and patch metadata when incorporating them. I have not made these repairs to any source or patch file.

**(c) Spans — PASS; retain the flagged transcription re-check.** All hunk counts and contexts match origin/main. The reconstructed s6 grows from 63 to 67 lines, with additions only after old line 63; its only replaced existing lines are 4, 46, 54 and 56. The reconstructed s8 retains 19 lines and changes only line 9. Every other existing line retains its content and position. I reproduced the prep note's patch hash and both before/after whole-file hash pairs.

I checked the `file`, `lines`, `premises`, `status_source` and `tex` fields of origin/main's [claims.tsv](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/INFRA/registry/claims.tsv), and searched the other registry files for s6/s8 references. Only C-DLV:Thm-D and C-DLV:Prop-F point into these files, both through `tex`; the matching events.log entries are historical records. No registered span moves. W1C-FINAL:Lemma-CAP's statement 45–56, premises 36–43 and status source 64 are all in untouched s7.

C-DLV:Thm-D's `tex` span 11–13 is byte-identical. C-DLV:Prop-F's `tex` span 28–47 stays at the same position but changes at line 46; its computed span hash changes from `fbaef3a19ee505f9859b83f35bbc17d721ba174e6ebf187c616cb729fea74f43` to `2c01f75dd9be259ef61c4e757901b9fafdbd240f27232221383b918393cc5b2a`. Its stored `tex_sha256` field is empty, so no stored transcription hash becomes stale; [check.py](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/INFRA/tools/check.py:388) continues to flag the unreviewed transcription. The Markdown statement/premises and registered claim hash are unchanged. The prep note's account is accurate when “no hash changes” means no stored registry hash, rather than the computed hash of the edited TeX span. The pre-existing C-DLV-form/corrected-form pointer mismatch is acceptable as an explicit HQ re-check item, not a defect of this patch. The proposed s2 repairs also move no line and intersect no registry span.

Only this reply file was written. No patch was applied, no registry or other worktree was modified, no commit was made, and no subagent was started. All reconstruction used memory; no scratch files/directory were created and no TMPDIR was set.

DIFF: FAIL

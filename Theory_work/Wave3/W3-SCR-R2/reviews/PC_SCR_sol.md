# PC review — W3-SCR post-C1 changes

Independent, read-only review, 2026-11-16. Audited `origin/main` at **7a19a78c2fb523ef15c05dc91cd31a59e84cd3bd**; the ref advanced during the session, so the findings below use this pinned snapshot. Only this report was written; no checkout, index, branch, registry, or acceptance record was changed. `git fetch origin` was the sole state-changing git operation.

**Finding:** the available evidence does not support an editorial-only sign-off for A1. The post-pass text explicitly adds fixed-in-n hypotheses on κ, b, M. The present fixed-parameter proof is sound on inspection, but that does not make the change of stated scope editorial. In addition, the repository does not retain the complete v3.3 working-tree snapshot needed for an exhaustive historical hunk comparison.

## 1. What the seats reviewed, and what git actually preserves

Both requested path histories give the same single commit:

```text
git log --format='%h %ad %s' -- Theory_work/Wave3/W3-SCR/reviews/C1_council_astra.md
925aa8d5 Mon Nov 9 20:40:58 2026 -0600 Theory Wave 3: W3-SCR (certified screening, design-free; SCR-A/A°/M/G/C/R/N; council Astra 9.3 / Opus 8.9)
```

The Opus path has the identical result. The full commit is `925aa8d574362b2623b4a733330ebaef5d871f61`, parent `d34478fc8f19c351bb900eccafc2c7820a039326`. This commit **first adds** the entire W3-SCR directory, including v3.4, both C1 reports, the disposition, and REPORT. The directory is absent in the parent and at the earlier `2ac3896` mentioned by the reviewers. Consequently, neither the report-writing commit nor its parent supplies the seats' actual v3.3 proof text. Taking `925aa8d5` as a pre-edit council baseline would silently use the already-edited version.

The [C1 brief](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/reviews/C1_brief.md:20), lines 20–35, specified:

- STATEMENT **v3.3**, CODE_CHECK, all seven lemma files L1–L7, and ASSUMPTION_MAP as the proof package.
- Production sources `v3_fit.R`, `v3_run.R`, `v3_exact.R`, `v3_preprocess.R`, `cpp/v3_engine.h`, `cpp/v3_core.cpp`, `cpp/v3_ledger.h`, `cpp/v3_score.h`; PROGRAM item 5 and PROTOCOL as binding context.
- Numerics, CITECHECK, and R01–R07 reviews as supporting material, expressly not independently scored proof. REPORT was **not** in the scored file list.

[Astra's report](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/reviews/C1_council_astra.md:3) explicitly says it reviewed v3.3 working-tree sources. [Opus's report](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/reviews/C1_council_opus.md:3) also identifies v3.3; its finding 1 quotes A1 with only “σ fixed” and says κ, b, M were not declared fixed (lines 28–44). Those contemporaneous quotations establish the relevant before-text even though they cannot recover every byte of v3.3. [LOG](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/LOG.md:46), lines 46–53, records council, post-pass edits, final numerics closure, and then REPORT being written.

Actual subsequent ticket history:

```text
git log 925aa8d5..7a19a78c --format='%h %s' -- Theory_work/Wave3/W3-SCR
# no output

git diff --exit-code 925aa8d5 7a19a78c -- Theory_work/Wave3/W3-SCR
# no output; exit 0
```

This includes STATEMENT, every lemma, and REPORT. `--full-history` additionally displays merge `c81fbf6c3741e970e7379cac264776b51411a290` (2026-11-11). It is not a later edit: its first-parent ticket diff is empty. The W3-SCR subtree object at `925aa8d5`, that merge's first parent, that merge, and the pinned tip is identically **cb2afce8df5e2c92994312fcdd96f9c23fd0e3bc**. The merge's second-parent comparison shows the directory being brought across from main, not modifications to its contents.

Thus there are **no committed post-925aa8d5 W3-SCR diff hunks to display**. The v3.3→v3.4 edits occurred before the initial ticket commit, after council in working-tree time. The next sections display and classify every edit recoverable from the two reports, disposition, and surviving text. These are explicitly evidence-based reconstructions, not a fabricated `git diff`; exact historical hunk boundaries and completeness cannot be certified without the missing v3.3 snapshot.

## 2. Hunk catalogue and classification

All ticket paths below are under `Theory_work/Wave3/W3-SCR/`; line numbers refer to the pinned snapshot. `925aa8d5 (pre-commit)` means an edit recorded by C1's trail and bundled into that initial commit, not an individually recoverable edit commit. EDITORIAL means no changed hypothesis, mathematical conclusion, constant, or proof step. The stricter definition in the review request is applied even where the original seats called an item MINOR or NOTE.

| commit | file:lines | hunk summary | class |
|---|---|---|---|
| 925aa8d5 (pre-commit) | [STATEMENT.md:3–8](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/STATEMENT.md:3) | v3.4/council/post-pass status paragraph; says fixed parameters were “made explicit” and no conclusion or constant changed. Exact prior paragraph unavailable. | EDITORIAL — status text; its editorial-only implication is not established. |
| 925aa8d5 (pre-commit) | [STATEMENT.md:104–108](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/STATEMENT.md:104) | SCR-M model count `M` → `M_𝓗` in definition and both counting bounds. | EDITORIAL — consistent renaming, unchanged cardinality and formula. |
| 925aa8d5 (pre-commit) | [STATEMENT.md:124–126](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/STATEMENT.md:124) | M6's literal assertion that b_𝓗 is independent of model count → only a geometric upper bound is independent; minimum formula retained. | SUBSTANTIVE — corrects a literal mathematical prose conclusion, although the displayed bound and gap theorem do not change. |
| 925aa8d5 (pre-commit) | [STATEMENT.md:133–135](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/STATEMENT.md:133) | SCR-G now explicitly imports A1 with “κ, b, M, σ fixed.” Existing c₂ and the meaning of coefficient bound M retained. Exact old parenthetical unavailable. | SUBSTANTIVE — explicit restriction of asymptotic hypotheses. |
| 925aa8d5 (pre-commit) | [STATEMENT.md:158–163](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/STATEMENT.md:158) | A1: “σ fixed” → “with κ, b, M, σ fixed (not depending on n).” No reported change to c₁ = κ²b²/[200(M²+σ²)] or the probability conclusion. | SUBSTANTIVE — adds fixed-in-n hypotheses on κ, b, M. |
| 925aa8d5 (pre-commit) | [lemmas/L3_screening.md:66–68](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L3_screening.md:66) | A1 proof's premise now also declares κ, b, M, σ fixed, not depending on n. | SUBSTANTIVE — same hypothesis restriction, supporting the large-n step at lines 70–72. |
| 925aa8d5 (pre-commit) | [lemmas/L7_master.md:9](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L7_master.md:9) | Missing-truth model count `M` → `M_𝓗`. | EDITORIAL — definition unchanged. |
| 925aa8d5 (pre-commit) | [lemmas/L7_master.md:18–20](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L7_master.md:18) | Rename propagated through b_𝓗, c_𝓗 and `M_𝓗 ≤ N_q`. | EDITORIAL — formulas unchanged. |
| 925aa8d5 (pre-commit) | [lemmas/L7_master.md:38–40](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L7_master.md:38) | Rename propagated through the union-bound threshold, denominator and model count. | EDITORIAL — same probability budget. |
| 925aa8d5 (pre-commit) | [lemmas/L7_master.md:97–99](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L7_master.md:97) | M4 now states κ, b, M, σ fixed and explains that its large-n steps use this. | SUBSTANTIVE — explicit proof hypotheses, used at lines 100–106; c₂ = κ²b²/[104(M²+σ²)] unchanged. |
| 925aa8d5 (pre-commit) | [lemmas/L5_exact.md:93–95](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L5_exact.md:93) | Local SCR-C proof constant `c₂` → `c₄` in definition and lower bound. | EDITORIAL — same expression 2 log(s₀+1)+log(1/ε)+1. |
| 925aa8d5 (pre-commit) | [lemmas/L5_exact.md:101](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L5_exact.md:101) | Same constant rename in the final comparison. | EDITORIAL — no changed inequality. |
| 925aa8d5 (pre-commit) | [ASSUMPTION_MAP.md:20](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/ASSUMPTION_MAP.md:20) | Previously unsupported κ²-attainment assertion gains an explicit negatively correlated two-truth construction and calculation. | SUBSTANTIVE — new mathematical proof evidence under the requested proof-step criterion; not used by A1. |
| 925aa8d5 (pre-commit) | [CODE_CHECK.md:3–5](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/CODE_CHECK.md:3) | Add unchanged-core/hash-verification provenance at 2ac3896; original read commit 2252d57 retained. | EDITORIAL — provenance only. |
| 925aa8d5 (pre-commit) | [CODE_CHECK.md:57–59](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/CODE_CHECK.md:57) | Document Q recomputation and Cholesky/refactor/QR routes as returning the same Q and determinants under EX-A. | EDITORIAL — documentation of existing algebraically equivalent routes; EX-A, score and certificate unchanged. |
| 925aa8d5 (pre-commit) | [reviews/C1_disposition.md:1–21](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/reviews/C1_disposition.md:1) | Newly recorded outcome and six findings; says no conclusion or constant changes. | EDITORIAL — review/status record; not an independent verification of its claim. |
| 925aa8d5 (pre-commit) | [LOG.md:46–53](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/LOG.md:46) | Council outcome, post-pass edits, numerics closure, REPORT written. | EDITORIAL — chronology/status; exact pre-C1 log ending unavailable. |
| 925aa8d5 (pre-commit) | [REPORT.md:7–11, 61, 80, 162–164](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/REPORT.md:7) | Newly written report's council/v3.4 status and evidence summaries; calls all six applications wording edits. REPORT was outside the scored file list. | EDITORIAL — status/reporting, with an overbroad description of the fixed-parameter change; no recoverable earlier REPORT to diff. |
| 24b0b8938e282194785435919745a3b313a46601 | [claims.tsv:401, column 35](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/INFRA/registry/claims.tsv:401) | Later actual A1 registry diff: normalize the correctness-gate evidence string to three relative report paths. Statement, hash and version unchanged. | EDITORIAL — evidence formatting only. |

The split rows for renames enumerate every surviving affected occurrence in those formula/proof blocks; they do not purport to recover the original unified-diff grouping. There is no evidence of a post-pass change to L1, L2, L4, or L6 in the disposition, and their entire committed contents are unchanged since `925aa8d5`. Absence of a v3.3 snapshot prevents the stronger claim that an exact byte comparison established their identity to the reviewed working tree.

## 3. Display of the recoverable changes

The following are **reconstructed excerpts**, not git-generated hunks. A minus line is exact only where quoted by a C1 seat; where the source does not preserve exact old wording, that limitation is stated.

**A1, statement and L3 premise.** Opus finding 1 quotes the old statement ending; the disposition records applying the same fixed-parameter addition to L3:

```diff
- … θ_min ≥ b > 0, ‖θ*‖₁ ≤ M, σ fixed …
+ … θ_min ≥ b > 0, ‖θ*‖₁ ≤ M, with κ, b, M, σ fixed (not
+ depending on n) …
```

Current statement lines 159–160 and L3 lines 66–67 contain that addition. Neither source attributes a change to c₁ or the probability formula. SCR-G's before-text is quoted as “Assume the hypotheses of Corollary A1 …”; its after-text, statement line 133, is:

```text
Assume the hypotheses of Corollary A1 below (κ, b, M, σ fixed) and (q_n + 1) log p + log n = o(n), and let
```

M4's exact complete old sentence is unavailable. Its after-text, L7 lines 97–98, now explicitly says:

```text
Assume the hypotheses of Corollary A1 (with φ^d_n(q_n) ≥ κ; κ, b, M, σ fixed, not
depending on n — the "for large n" steps below use this) and 𝐋_n := (q_n + 1) log p + log n = o(n).
```

**M6 prose.** Astra quotes the before-clause; the current text at statement lines 124–126 reads:

```diff
- b_𝓗 depends on the geometry of the witness directions, not on the number of models
+ b_𝓗 has an upper bound that involves
+ only the geometry of the witness directions and not the number of models: b_𝓗(x) ≤ √(dim span{d_S}) + √(2x) (b_𝓗 itself
+ is the smaller of this kind of geometric bound and the counting bound).
```

The definition still takes a minimum with a counting branch. Astra gives a concrete example where changing the number of models with identical directions changes that minimum. Under a strict semantic criterion, repairing this false prose assertion is a conclusion correction, even though it does not change the displayed mathematical theorem. This classification does not suggest a new defect in the surviving formula.

**M and c₂ renames.** Opus finding 4 identifies both old definitions; the surviving replacements are:

```diff
- M := |𝓗⁻|; √(2 log M + 2x); M ≤ N_q; e^{-x}/M; sum over M sets
+ M_𝓗 := |𝓗⁻|; √(2 log M_𝓗 + 2x); M_𝓗 ≤ N_q; e^{-x}/M_𝓗; sum over M_𝓗 sets
- c₂ := 2 log(s₀+1) + log(1/ε) + 1; … − c₂ …
+ c₄ := 2 log(s₀+1) + log(1/ε) + 1; … − c₄ …
```

These are schematic occurrence-level replacements, not whole original source lines. The coefficient bound M in A1 and gap constant c₂ in SCR-G/M4 retain their original meanings and expressions.

**Sharpness construction, ASSUMPTION_MAP line 20.** Opus quotes the original unsupported attainment claim. The added explanation is:

```diff
+ for S₀ = {1, 2}, x_1ᵀx_2 = −(1−κ)(n−1), θ* = (b, b), the pair Gram has smallest eigenvalue κ(n−1), μ = b(x_1 + x_2), x_tᵀμ = b(n−1)κ, so Γ_n(0) = γ(t, ∅) = b²κ²(n−1)²(n+1)/n² ≍ κ²nb² (C1 Opus note 2).
```

For 0<κ≤1 and n≥3 this construction is feasible in the centred subspace. Since a(t|∅)=n²/(n+1), the displayed gain follows directly. The new proof supports an existing sharpness assertion; it changes no A1 bridge, hypothesis, constant, or conclusion.

**CC5 route documentation, CODE_CHECK lines 57–59.** The disposition and Opus finding 3 identify the newly added sentence:

```diff
+ The scorer has numerical branches (Q recomputed in a
+ non-negative form when Q < 1e-8·y′y, `cpp/v3_score.h:218-219`; Cholesky / refactor / QR routes, `cpp/v3_score.h:231-234`);
+ under EX-A they return the same Q and determinants, so they do not change F.
```

Checked against the [scorer](/home/fb31/BVS-wt/THEORY-DEPT/Scripts/SMC_BVS/core/cpp/v3_score.h:175), including its factor and fallback branches. For β=nH⁻¹z, Hβ=nz gives ((n+1)βᵀGβ+‖β‖²)/n=zᵀβ. Thus RSS+(‖Xβ‖²+‖β‖²)/n=yᵀy−zᵀβ=Q. The augmented QR matrices have Gram matrices H and G+I. This is explanation of the existing score under the existing EX-A premise.

**Provenance, CODE_CHECK lines 4–5.** Added record:

```diff
+ The core files were last changed at commit 72785fe and are byte-identical
+ at the later HEAD 2ac3896 (hashes re-verified by the lead and by the Opus council seat).
```

This reports the earlier hash checks; it is not a change of score or an independently established v3.3 proof snapshot. The exact old surrounding wrapping is unavailable.

**Status and REPORT.** Exact old status/log text is unavailable. The surviving statement now labels itself v3.4, LOG records applying post-pass edits, and REPORT lines 7–9 explicitly say v3.3 was scored and v3.4 was not re-scored. REPORT was first written after those edits (LOG line 53), so presenting a v3.3→v3.4 REPORT diff would be false. Its A1 summary, lines 27–29, says “fixed coefficients,” but does not itself enumerate all the fixed κ, b, M, σ requirements; the full current statement must govern any abstract use. The report's “wording edits” characterization is what this PC check rejects for the hypothesis addition.

**Actual later registry diff.** At `24b0b893`, the only changed A1 field is column 35 (other claims in that commit are outside this ticket):

```diff
- correct:PASS(council C1: gpt-6-astra 9.3 / Claude Opus 5.5 8.9, all six gates; Theory_work/Wave3/W3-SCR/reviews/C1_council_astra.md, C1_council_opus.md, C1_disposition.md); lit:PENDING; necessity:PENDING; better:PENDING
+ correct:PASS(reviews/C1_council_astra.md, reviews/C1_council_opus.md, reviews/C1_disposition.md) ; lit:PENDING ; necessity:PENDING ; better:PENDING
```

This actual field comparison is editorial. The pinned A1 row still points to statement lines 158–163, version 1.0.0, hash `ebe949b727b00fed64ab2ff0441f8c721efacbe72c2d0c14a76c350f9bf3719f`, and evidence acknowledging that v3.4 was not re-scored. Those metadata do not independently establish that v3.4 equals the reviewed scope.

## 4. A1 and every load-bearing part of its proof

**A1 specifically:** [STATEMENT lines 158–163](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/STATEMENT.md:158) now imposes fixed positive κ and b, a fixed finite M, and fixed σ. Opus's contemporaneous finding expressly records the absence of fixed κ, b, M in the reviewed text. Adding these requirements changes a hypothesis under the requested PC criterion, even though it leaves c₁ and the conclusion formula unchanged and makes the existing proof's large-n wording safe. This is a scope restriction, not evidence that the current A1 is false. Opus also explicitly says “A1 itself is not affected” and proposes an alternative proof for varying bounds; the disposition's broader statement that A1 needs the fixed bounds should therefore not be treated as a conclusion shared by both seats. Without a frozen v3.3 snapshot or an explicit pre-existing fixed-constant convention, an editorial-only certification is unjustified.

The scope distinction can be exhibited without simulation. Let p=2, q_n=0, σ=1, use centred orthogonal standardised columns, S₀={1}, θ*₁=n^{-1/4}, and θ*₂=0. Then φ^d_n(0)=1, κ=1, M=1, and b_n=n^{-1/4}. On the reading that permits n-dependent b, all old displayed inequalities hold eventually:

```text
θ_min = b_n,  ‖θ*‖₁ ≤ 1,
(q_n+1)log p + log n = log 2 + log n ≤ √n/400 = c₁,n n.
```

No fixed b>0 can bound these signals from below. The new A1 excludes this array, while its old displayed conditions with b_n admit it. This example demonstrates the changed hypothesis, not failure of screening. If fixed constants were always intended, the edit resolves an ambiguity; that intention is insufficient to prove a wording-only historical diff.

I checked the current proof chain as follows; line references enumerate all blocks used by A1, including dependencies of the cited lemmas:

| proof component | inspected lines | check and post-pass relevance |
|---|---|---|
| Setting and definitions | [STATEMENT:14–21, 25–47, 51–75](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/STATEMENT.md:14) | Gaussian fixed-design triangular array, centring/normalisation, exact F, q≤K−1, Γ, τ, directional floor. The general setting allows triangular arrays and explicitly states exceptions when fixed quantities are required. |
| A1 premise and complete derivation | [L3:65–76](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L3_screening.md:65) | Lines 70–71 use fixed M, κ, b to choose n with √(κ(n−1))b≥2M/√(n+1). Line 72 yields Γ≥κ²b²n/16. Lines 73–75 bound the squared denominator by 4(M²+σ²)c₁n, giving ρ²≥200/64>2. Line 76's polynomial-p consequence uses c₁>0 fixed. Current argument is valid. |
| Directional bridge and primitive variants | [L4:3–33, 49–64](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L4_bridges.md:3) | L4.0 lines 5–17 derives the per-model bound using augmentation and Cauchy–Schwarz; B2 lines 24–33 uses Δ(S)≥φ(n−1)‖θ_T‖² and ‖θ_T‖₁²≤|T|‖θ_T‖₂². B2d lines 49–55 replaces the anchored floor by its directional counterpart through exactly the same lower bound. B3 lines 59–64 supports the sparse-floor special case by a Schur complement. B1 lines 19–22 is consistent but is not needed as a separate step in A1. No reported C1 edit here. |
| Algebra underlying the bridge | [L1:7–39, 73–82](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L1_score.md:7) | R positive contraction, a>0 and a<n, rank-one/Schur identities, augmented projector and bias norm c_θ=‖θ*‖₂/√(n+1). These justify every L4.0 step; no rank assumption on all noise columns is introduced. No reported post-pass edit. |
| Asymptotic reduction | [L3:26–35](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L3_screening.md:26) | x_n=√log n; T_n≤(2log p+log n)(1+o(1)), τ̄/τ→1, N_q≤(p+1)^q, q/p≤1. The remaining noise term is o(√log n), so ρ>1 gives MC and failure ≤3e^{-√log n}→0. This reduction itself does not require fixed κ, b, M. |
| Screening claim and transfer to reported output | [L3:6–24](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L3_screening.md:6) | On E1∩E2⁺ every truth-missing model of size≤q has a strictly improving truth addition. Lines 20–24 transfer this uniform event to every certified endpoint, without conditioning on a certificate occurring. |
| Events used by SCR-A | [L2:3–20, 28–39](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L2_noise.md:3) | Deterministic maximising witness: one Gaussian per model. R²≤R gives E1 failure≤e^{-x}; χ² and Gaussian bounds give E2⁺ failure≤2e^{-x} and τ̂≤τ̄. No union over s₀ and no data-selected witness assumption. E4 and E3 are not needed by A1's direct proof. |
| Strictly improving score addition | [L1:35–56](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L1_score.md:35) | L1.3 bounds D≤n+1, L1.4 gives the exact prior/determinant/residual change, L1.5 uses Q≤n−1 and ν>n/2 to dominate the penalty at g_y≥T_n. Strict improvement and q≤K−1 are correctly tracked. |
| Certificate and exact-score interface | [CODE_CHECK:20–59, 80–83](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/CODE_CHECK.md:20) | CC2–CC3 map top-level and archive certificates to LO; CC4 ensures additions are scanned below K; EX-A identifies coded comparisons with F. Post-pass CC5 prose describes equivalent existing score routes, as checked above. |
| Other lemmas | [L5:93–101](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L5_exact.md:93), [L6](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L6_sharp.md:1), [L7:97–109](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-SCR/lemmas/L7_master.md:97) | L5 and L6 do not enter A1's direct proof. L7 M4 consumes A1 for SCR-G; A1 does not consume M4. Its fixed-parameter addition is relevant to SCR-G's linear gap, not a missing dependency of A1. |

For M4 specifically, fixed κb/(M²+σ²)^{1/2}>0 makes σr_n=o(κb√n) and B_S=o(nu*) for u*=κ²b²/[26(M²+σ²)]. Those are mathematical uses of the newly explicit restriction, not just notation. The numerical constants 200 and 104 were not changed in the documented edits.

## 5. Disposition check and implication for the headline claim

The six findings and their applications are accounted for. The disposition's narrow phrase “none changes a conclusion or a constant” does not even address changes to hypotheses. Its treatment of the fixed-parameter insertion as harmless wording is too strong under this task's criterion. With the same strict criterion, M6 corrects a false literal descriptive conclusion and the map adds proof evidence; neither is load-bearing for A1. The notation and code-documentation changes are editorial. There is no evidence here of a changed numerical constant or a broken current fixed-parameter A1 proof.

An abstract may describe the present A1 only with its fixed-parameter scope, EX-A and Gaussian fixed-design setting, and its event formulation: the probability of a **certified, size≤q_n output missing a truth** tends to zero. A1 does not assert that a sparse certificate occurs with probability tending to one. C1's two scores are evidence for the identified v3.3 review, not an independent re-score of every v3.4 hypothesis. A complete historical hunk certificate would require the missing v3.3 proof snapshot; this report supplies the strongest check available from origin/main and the contemporaneous reports and does not create an acceptance or registry update.

PC-VERDICT: A1-SUBSTANTIVE (adds fixed-in-n κ, b, M hypotheses)

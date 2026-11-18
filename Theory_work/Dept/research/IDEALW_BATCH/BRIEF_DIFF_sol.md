# Brief — Sol diff check of the IDEAL-W⁺ batch NARROW (19 claims) and errata (v4: statement change by an OpenAI reviewer)

Prepared 2026-11-16 06:05 CST by the Theory Dept implementation sub-agent (Claude Opus 5.5). Reviewer: gpt-6.1-sol, reasoning high.
One review over the whole batch.

## Rules
- You are a **fresh, read-only** reviewer. Edit no file except your one reply file below. Do not commit to, or touch,
  any other worktree. Do not change the registry. Do not apply the patches to the real files.
- **D62 (verbatim):** "Do not write any file outside the worktree and set no TMPDIR. Scratch only in /home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/, deleted at the end."
- Write your reply to `Theory_work/Dept/research/IDEALW_BATCH/DIFF_sol.md` (inside the worktree `/home/fb31/BVS-wt/THEORY-DEPT`).
  Last line: `DIFF: PASS` or `DIFF: FAIL`. Use FAIL only for a concrete defect in the batch, and give a concrete repair with it
  (exact replacement text, same line count).

## Inputs
1. **The patches:** `Theory_work/Dept/research/IDEALW_BATCH/patches/*.patch` (20 files). Each is a unified diff against origin/main
   (967313dd); read the base with `git show origin/main:<path>`.
   - 16 NARROW patches, one per touched file of the 19 claims.
   - 4 `ERRATUM__*` patches: C-DLV `INVENTORY.md`, `lemmas/L2_degenerate.md`, `STATEMENT.md`, FINAL `sections/s7_impl.tex`.

   Every in-place edit replaces one line by one line. Each narrowing note or erratum is **appended** after the old last line.
   The line accounting is in `LINES_CHECK.md` (same folder): table 0 lists the changed lines per file, and tables A/B list the
   hashes. `IMPACT.md` and `CASCADE.md` are context only; you need not review them.
2. **The defect finding:** `Theory_work/Dept/research/FUNI_transfer/TR1_sol.md`. Read all of it: §1 is the failing inference and the
   counterexample; §2 gives the supported claims (𝔇 under IDEAL-W; every n under IDEAL-W⁺ with the shipped-cap allocation).
3. **The assumption** (final, use verbatim): `Theory_work/Dept/research/FUNI_NARROW/A_IDEALW_PLUS.md:10`. IDEAL-W itself is
   `Theory_work/Wave1C/C-DLV/STATEMENT.md:24-25`, unchanged. No widening of IDEAL-W is allowed.
4. **The code:**
   - `Scripts/SMC_BVS/core/v3_run.R:93-101`: `le > 1e6`; le defaults to ℓ_n.
   - `Scripts/SMC_BVS/core/cpp/v3_core.cpp:465-476`: cap_ll = ls0_ell + |S̃₀|, then the `numeric_limits<int>::max()` stop.
   - `Scripts/SMC_BVS/core/v3_fit.R:120-131`: the exact branch returns first.

   These lines are identical at the method pin `4676af6` and at `493579a`.
5. **The form precedent** (already PASSED): F-UNI v2, `Theory_work/Dept/research/FUNI_NARROW/L5_delivery_F-UNI_v2.patch` and
   `DIFF_sol.md`. Its form: (a) under plain IDEAL-W, P(no output) = 0 on 𝔇; (b) under A:IDEAL-W⁺, every n and every
   asymptotic delivery conclusion.

## The 19 claims, the form used, and the proposed tag
Every row adds hypotheses or restricts the domain; none changes another hypothesis or a non-delivery conclusion. Proposed tag:
**WEAKER**, major bump.

| # | id (version) | statement span (origin/main) | edit | form |
|---|---|---|---|---|
| 1 | W2-FAC-A:Prop-F-FAC (1.0.0) | `W2-FAC-A/lemmas/L7_delivery.md:22-24` | :22-23 | (a) 𝔇 + (b) IDEAL-W⁺ |
| 2 | W2-FAC-A:Thm-FAC-L (1.0.0) | `W2-FAC-A/STATEMENT.md:102-152` | :133, claim (D) | (a)+(b) |
| 3–5 | W2-LOC2:F-LOC2, .exp, .poly (1.0.0) | `W2-LOC2/STATEMENT.md:100-102` (+ premise `lemmas/L7_delivery.md:17-19`) | STATEMENT :101; L7 :17 | (a)+(b) |
| 6 | W2-FAC-B:Thm-FAC-CS (1.0.0) | `W2-FAC-B/STATEMENT.md:105-134` | :131, (C4) | (a)+(b) |
| 7 | W2-FAC-B:L5 (1.0.0) | `W2-FAC-B/lemmas/L5_assembly.md:44-45` | **span unchanged.** It is the (C3) theorem, with no delivery sentence. The delivery text L5.4 (outside every span) is edited in place at :61 | (a)+(b) in L5.4 |
| 8 | W2-FAC-PK:Thm-FAC-PK (1.0.0) | `W2-FAC-PK/STATEMENT.md:73-87` | :82, (iii) | (a) on **𝔇_PK** (caps ≤ ℓ_n + 2K) + (b) IDEAL-W⁺ with its INT_MAX disjunct read at the plumbed cap value — **see Q(e)** |
| 9 | W2-FAC-S5:Thm-FAC-BCS-R (1.0.1) | `W2-FAC-S5/STATEMENT.md:112-124` | :124, (C4-R) | (a)+(b) |
| 10 | W2-FAC-S5:L5 (1.0.0) | `W2-FAC-S5/lemmas/L5_assembly.md:33-37` | **span unchanged** ((C3-R) only); delivery is row 11 | — |
| 11 | W2-FAC-S5:L5.C4-R (1.0.0) | same file `:39-43` | :41 | (a)+(b) |
| 12 | W2-FAC-X:Thm-FAC-CS-iid (1.0.0) | `W2-FAC-X/STATEMENT.md:76-95` | :94, (C4) | (a)+(b) |
| 13 | W2-FAC-X:Thm-FAC-GL (1.0.0) | `W2-FAC-X/STATEMENT_T2.md:49-62` | :62, (G4) | (a)+(b) |
| 14 | W2-FAC-X:X10 (1.0.0) | `W2-FAC-X/lemmas/X10_assembly_T2.md:1-1` (title); premise `STATEMENT_T2.md:61-62` | premise changes via #13; (G4) text :21 edited in place | (a)+(b) |
| 15 | W2-FAC-XA:X4 (1.0.0) | `W2-FAC-XA/STATEMENT.md:85-86` | :86 | (b) only: asymptotic, no every-n sentence |
| 16 | W2-UNI:UNI-0 (1.1.2) | `W2-UNI/STATEMENT.md:103-110` | :109 | (a)+(b) |
| 17 | W2-UNI:UNI-1 (2.0.0) | `W2-UNI/STATEMENT.md:112-131` | :123 | (b) only: asymptotic, no every-n sentence |
| 18 | HQ_AUDIT-W1C:A2 (1.0.0) | `Wave1C/HQ_AUDIT/A2_propF_GROW.md:5-35` | :27 | (a)+(b) — **see Q(f)** |
| 19 | HQ_AUDIT-W1C:A3 (1.0.0) | `Wave1C/HQ_AUDIT/A3_check_A2.md:5-5` | :5 | (a)+(b), re-stating A2 as narrowed — **see Q(f)** |

The common inserted text (verbatim in each span) is:
- 𝔇 := {ℓ_raw ≤ 10⁶ and ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1}, ℓ_raw := ⌈log₂(n + p_raw + 1)⌉;
- "A:IDEAL-W⁺ in place of IDEAL-W (IDEAL-W, and the two shipped rejection predicates `le > 10⁶` (…v3_run.R:96) and
  `ℓ + |S̃₀| > INT_MAX` (…v3_core.cpp:474) are false; definition at the end of this file)".

The appended note in each file gives the reason (TR1), the 𝔇 argument, the statement that the proof's no-output step is
otherwise unchanged, and the verbatim A:IDEAL-W⁺ paragraph.

## Errata (no statement change intended)
- (E1) C-DLV `INVENTORY.md`: Summary line :80 is edited in place; new section X′ is appended with rows X7 (`le > 1e6`) and
  X8 (`cap_ll > INT_MAX`), class (d) A:IDEAL-W⁺ / 𝔇. Precedent: R02 #5 `nth_nonmember`.
- (E2) C-DLV `lemmas/L2_degenerate.md`: an addition (viii)/(ix) to S.3's X2 list, **appended**. The registered span C-DLV:L2-S3
  `:37-67` is kept byte-identical.
- (E3) C-DLV `STATEMENT.md`: amendment note appended: "IDEAL-W never covered the application-level rejection predicates; IDEAL-W⁺
  is the explicit form". It adds that C-DLV's own method (LS0 as specified, cap ℓ_n) has no such validators, so C-DLV's claims
  are unchanged.
- (E4) FINAL `sections/s7_impl.tex:39`: "excluded by IDEAL-W" becomes "*not* excluded by IDEAL-W …; it is excluded by …
  A:IDEAL-W⁺ …". Line :39 lies in the premise span `:36-43` of W1C-FINAL:Lemma-CAP, so that row's claim hash changes
  (erratum, patch bump).

## Questions
(a) **Truth and proof.** For each of the 19, is the narrowed statement true and proved by its *own* chain? That is: Theorem D's exit
    walk, the total fallback, the claim's stated allocation, Lemma S inputs, and 𝒦_n with D′ for the asymptotic part.
    - Clause (a) is under plain IDEAL-W on 𝔇.
    - Clause (b) is under A:IDEAL-W⁺.
    - Check especially that every asymptotic conclusion (P(Ŝ⁺ = S₀) → 1, S5's bound on P(Ŝ⁺ ≠ S₀)) sits under (b) only.
    - Check that the allocation each chain states covers the shipped preflight where (b) claims every n. FAC-A, LOC2, FAC-B, S5,
      X, XA and UNI cite A4's P_e + A / P̄_LS0.
(b) **Scope.** Did nothing else change?
    - Each in-place edit only adds the clause split and the assumption; no other hypothesis or conclusion changes.
    - Appended notes add no claim beyond explanation.
    - The line accounting in LINES_CHECK is right: no span moves; hash changes = 17 batch rows + Lemma-CAP; FAC-B:L5 and S5:L5 are
      unchanged.
(c) **Tag.** WEAKER for each of the 19 (major bump). Do you agree, per claim?
(d) **Errata.** Are E1–E4 accurate, with code lines, classes, the C-DLV "not exposed" sentence and the s7 wording? Is E2's
    choice to append rather than edit inside L2-S3's span acceptable?
(e) **FAC-PK (iii)** is about the head code *plus* not-yet-made plumbing for caps up to ℓ_n + 2K. The patch states two premises
    explicitly:
    - the plumbing range-checks the cap only through the shipped guard, evaluated at cap_ll = a(data);
    - for (b), A:IDEAL-W⁺'s INT_MAX disjunct is "that guard at cap_ll = a(data)".

    Is this an admissible use of the registered assumption, or a widening? If it is a widening, give the minimal repair (e.g. an
    explicit extra premise instead).
(f) **A2/A3.** Their method paragraph is spec-level (A2 `:9` "the method and premises of A1:62–75", the specified v3.1 + LS0). Their
    allocation (A2 `:16-23`) has Corollary R's preflight bounds but not A4's LS0 preflight terms; the appended note says so and
    leaves it to HQ. HQ listed both claims as exposed, so they are narrowed.
    - Is the narrowed A2/A3 true as stated?
    - Is anything in the patch itself wrong?

    The pre-existing spec-vs-shipped question is HQ's to decide; report it, but it is not by itself a FAIL of this diff.

Answer each with a verdict and a short reason. Include a **per-claim table** (id | (a) true & proved? | (b) scope OK? | (c) tag).
End with the single line `DIFF: PASS` or `DIFF: FAIL`.

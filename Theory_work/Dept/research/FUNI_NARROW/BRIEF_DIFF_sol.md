# Brief — Sol diff check of the W2-UNI:F-UNI delivery narrowing (v4: statement change by an OpenAI reviewer)

Prepared 2026-11-16 05:49 CST by the Theory Dept implementation sub-agent (Claude Opus 5.5). Reviewer: gpt-6.1-sol, reasoning high.

## Rules
- You are a **fresh, read-only** reviewer. Edit no file except your one reply file below. Do not commit to, or touch,
  any other worktree. Do not change the registry. Do not apply the patch to the real file.
- **D62 (verbatim):** "Do not write any file outside the worktree and set no TMPDIR. Scratch only in /home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/, deleted at the end."
- Write your reply to `Theory_work/Dept/research/FUNI_NARROW/DIFF_sol.md` (inside the worktree
  `/home/fb31/BVS-wt/THEORY-DEPT`). Last line: `DIFF: PASS` or `DIFF: FAIL`. Use FAIL only for a concrete defect, and give
  a concrete repair with it.

## Inputs (read these; nothing else is needed)
1. **The patch:** `Theory_work/Dept/research/FUNI_NARROW/L5_delivery_F-UNI_v2.patch`. It is a unified diff against
   `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md` as on origin/main
   (`git show origin/main:Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md`). What it does:
   - changes line 1 in place (a title changelog);
   - rewrites the statement span 15–21 in place, keeping 7 lines;
   - appends a remark as new lines 41–49 after the old last line 40.

   No other line changes. Line accounting is in `LINES_CHECK.md` in the same folder.
2. **The original claim** W2-UNI:F-UNI@1.1.0 = `L5_delivery.md:15-21` (origin/main). Its premises (method, premises,
   allocation) are `:8-13`, and its proof is `:23-34`. The proof cites:
   - W2-FAC-A `lemmas/L7_delivery.md` Steps 1–2 (`:26-38`);
   - C-DLV `lemmas/L4_delivery.md` (Theorem D's exit walk `:13-42`; Proposition F `:79-91`; Corollary D′ `:65-77`);
   - the allocation of `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:28-46`
     (W_G, M_G, P_e + A, P̄_LS0; HQ audit A4 `Theory_work/Wave1C/HQ_AUDIT/A4_postcouncil_check.md:7-25`).

   IDEAL-W is defined at `Theory_work/Wave1C/C-DLV/STATEMENT.md:24-25`.
3. **The defect finding:** `Theory_work/Dept/research/FUNI_transfer/TR1_sol.md`. Read all of it: §1 is the table and the
   counterexample, §2 gives the supported claims (𝔇 / D_K under IDEAL-W; every n under IDEAL-W⁺ with the shipped-cap allocation).
4. **The code lines:**
   - `Scripts/SMC_BVS/core/v3_run.R:93-101` (`le > 1e6` validator; le defaults to ℓ_n);
   - `Scripts/SMC_BVS/core/cpp/v3_core.cpp:465-476` (cap_ll = ls0_ell + |S̃₀|; `cap_ll > numeric_limits<int>::max()` stop);
   - `Scripts/SMC_BVS/core/v3_fit.R:120-131` (exact branch returns before the final settings/LS0 call).
5. **The assumption definition** (HQ form decision): `Theory_work/Dept/research/FUNI_NARROW/A_IDEALW_PLUS.md`.
   A:IDEAL-W⁺ := IDEAL-W, plus the two shipped rejection predicates `le > 10⁶` (v3_run.R:96) and `ℓ + |S̃₀| > INT_MAX`
   (v3_core.cpp:474) are false; nothing else is lifted.
6. **Alignment target:** W3-RM2-R Lemma DLV-0, `/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/STATEMENT.md:72-90, 144-150`.
   It is read-only; it is another worktree, so do not write there.

## The change (for convenience; the patch file is authoritative)
Old `:15-21`:
```
**Proposition F-UNI.** Let a design sequence satisfy:
 (V) input validity: (R) with λ_min(Σ_n) > 0 for every n, or (E) with nonconstant raw columns;
 (S) for a deterministic Q_n ⊇ S₀ with 𝓛_n := {T : S₀ ⊆ T ⊆ Q_n} ⊆ Ω (|Q_n| ≤ K_n):
     P(Sand_n(Q_n) ∩ NA(𝓛_n) ∩ TL(𝓛_n)) → 1;
 (P) E[1 − π(S₀)] → 0 (under the law of the setting).
Then, under the method, premises and allocation above: for every admissible n ≥ 3, P(no output) = 0; and P(Ŝ⁺ = S₀) → 1
(joint design/noise law under (R), noise law under (E)), together with the algorithm's randomness.
```
New `:15-21`:
```
**Proposition F-UNI.** Let a design sequence satisfy: (V) input validity: (R) with λ_min(Σ_n) > 0 for every n, or (E) with nonconstant raw columns;
 (S) for a deterministic Q_n ⊇ S₀ with 𝓛_n := {T : S₀ ⊆ T ⊆ Q_n} ⊆ Ω (|Q_n| ≤ K_n): P(Sand_n(Q_n) ∩ NA(𝓛_n) ∩ TL(𝓛_n)) → 1;
 (P) E[1 − π(S₀)] → 0 (under the law of the setting).
Then, under the method, premises and allocation above: (a) for every admissible n ≥ 3 with (n, p_raw) ∈ 𝔇 := {ℓ_raw ≤ 10⁶ and ℓ_raw + ⌊n/2⌋ ≤
2³¹ − 1}, ℓ_raw := ⌈log₂(n + p_raw + 1)⌉, P(no output) = 0; (b) under A:IDEAL-W⁺ in place of IDEAL-W (IDEAL-W, and the two shipped rejection predicates
`le > 10⁶` (Scripts/SMC_BVS/core/v3_run.R:96) and `ℓ + |S̃₀| > INT_MAX` (Scripts/SMC_BVS/core/cpp/v3_core.cpp:474) are false): for every admissible n ≥ 3,
P(no output) = 0; and P(Ŝ⁺ = S₀) → 1 (joint design/noise law under (R), noise law under (E)), together with the algorithm's randomness.
```
The other changes are line 1 (title changelog) and the appended remark at 41–49. That remark explains the reading of Step 2
on 𝔇 and under A:IDEAL-W⁺, says the TR1 §2 allocation is already the premise at :11-12, notes that 𝔇 is sufficient but not
necessary and is bounded, and records the alignment with DLV-0.

## Questions
(a) **Truth and proof.** Is the narrowed statement true? Is it proved by F-UNI's existing chain (L5 Steps 1–3 +
    FAC-A L7 Steps 1–2 + C-DLV L4, restricted as TR1 says), with **no** input from DLV-0's re-derived allocation?
    Check in particular:
    - (i) On 𝔇 under bare IDEAL-W, neither validator fires on the SMC branch, so Theorem D's exit walk plus the
      fallback leaves only null exits. Here ℓ_n ≤ ℓ_raw because p ≤ p_raw, |S̃₀| ≤ K ≤ ⌊n/2⌋, and le = ℓ_n under the stated
      method/CONFIG.
    - (ii) Under A:IDEAL-W⁺, the allocation that F-UNI's premises :8-13 already require (FIN s6 Prop F with A1's W_G, M_G and
      A4's P_e + A, P̄_LS0; LS0 count ≤ 1 + (ℓ_n + K + 1)q(p)) is exactly what TR1 §2 requires. Then every-n delivery and the
      consistency sentence follow from Steps 1–3 unchanged. Name the TR1 step or row that decides this.
    - (iii) The remark's claims are accurate.
(b) **Scope of change.** Does the patch change anything beyond the narrowing? Check each of these:
    - the rewrap of (V) onto line 15 and of (S) onto line 16 is content-neutral;
    - the hypotheses (V), (S), (P) and the law/randomness clause are unchanged;
    - nothing in :2-14 or :22-40 changes (premises, proof, Instances, Qualifications);
    - line 1 is a changelog only;
    - no registered or cited line number moves (see LINES_CHECK.md).
(c) **Tag.** The proposed tag is WEAKER, with a major bump 1.1.0 → 2.0.0: clause (a) restricts the domain under the old
    premises, and clause (b) strengthens the premises for the old conclusion. Do you agree? If not, which tag, and why?
(d) **Anything else** that makes the patch unfit to apply. Examples:
    - wording ambiguity in 𝔇 or in the A:IDEAL-W⁺ parenthesis, against `A_IDEALW_PLUS.md`;
    - whether "INT_MAX" and "ℓ + |S̃₀|" match the coded predicate `cap_ll = ls0_ell + |S̃₀| > numeric_limits<int>::max()`
      under the configuration;
    - line wrap or Markdown.

Answer each question with a verdict and a short reason. End with the single line `DIFF: PASS` or `DIFF: FAIL`.

# Staged V edits (W3-READER, 2026-11-16)

`V_edits.patch` = the post-V edit set, prepared against branch commit 7d24291a and applied after the V signal with
`git apply --3way Theory_work/Wave3/W3-READER/staged/V_edits.patch` (after the last merge of main), then requote.

Contents:
1. Rows 3.1/3.2 (Theorems 6, 7) and (S4) from W3-RM2-R READER_DELTA v-next (e78a1055, `reviews/post_cp3/`), 3-way merged
   onto this branch: thm6 v0.8, thm7 v0.6, (S4) item (v) folded into (i) (IDEAL-W⁺) and (iv) (valid input) per the delta;
   card v1.8 (row 3.1 keeps the [SL-card] comparison). Statuses are the delta's CP3 placeholders "requote verbatim once
   recorded"; after V they are replaced with the claims.tsv labels.
2. IF-START repin (and START-R in R4/REPORT) to W3-START2-R@1.0.0 (main b48fd0a1) in thm10 (v1.0, B10.2), card row 3.6,
   lemma R4 (status, input, claim, proof step 2), REPORT depends_on. Tag STRONGER for thm10 / card 3.6 / R4: since the
   row 3.3 swap (a33d890d), Theorem 10's (A5) = Theorem 5's (A5) = (L-R⁺⁺) (sets up to e^{κ√log n}), which only
   IF-START⁺⁺ covers; old IF-START⁺ needs (L-R⁺). REPORT: EQUAL (depends_on ids).
3. Thm10 honest-limits completion remark: refers to (S4) as amended (EQUAL).

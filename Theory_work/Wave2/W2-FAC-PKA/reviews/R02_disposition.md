# R02 disposition

Verbatim review and addendum: R02_lemmas_claude.md. L0 VERIFIED; L1 VERIFIED; numerical evidence INADEQUATE as filed. No status upgraded to PROVED-CHECKED.

F1: numerics/n5_review_repairs.py imports an explicitly attributed verbatim copy of reviewer DP in numerics/r02_start_dp_reference.py. Output N5_saturation.json directly tests maximizing start size, the size-K margin and population increment predictions, including p=n-1 and small total signal. n=800 controls compare the independent DP against the source capped DP. Large n rows reproduce the review's examples; small-total-signal unsaturated rows are retained. The review's n=100000 addendum remains reviewer evidence, not claimed as lead recomputation.

F2: patched only the ticket adapter's empty boolean mask; original source untouched.
F3: each source replacement asserts exactly one match. N5_adapter_controls.json contains 24 dense-reference comparisons including empty, K-1 and K starts, with all final sets, move counts and intermediate scores matching. These are new lead runs, not copied reviewer output.
F4: reran N1 with K, ell and full partition saved. Old output preserved as N1_exact_grid_preR02.jsonl. F5: added move_details distinguishing truth-in/out for every move, retaining legacy tags for compatibility.
L1-a/b: explicit variance lower bound and prior-cost note inserted. W1–W3: exact tie order, sign frame and raw-data reduction/source citation inserted in STATEMENT. Optional hardcoded rank metadata left as descriptive values, not claimed computed tests.

No proof step was rejected; independent key-lemma review is separate. Downstream use of L1 may now cite the proof review together with the repaired falsification artifacts. Final sweep/council must assess all changes.

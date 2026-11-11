# R06 disposition (lemma check batch 2, Codex gpt-6.1-sol high)

Reviewer reply verbatim: `reviews/R06_batch2_check_sol.md`. Verdicts: item 1 (Lemma tau, B2tau) VERIFIED-WITH-AMENDMENTS;
item 2 (B1', RM-F paragraph) VERIFIED-WITH-AMENDMENTS; item 3 ([P1], [R03-1] in NA-F) VERIFIED; item 4 (archive
corollary) VERIFIED; item 5 (Form R bridges and assembly) VERIFIED-WITH-AMENDMENTS; item 6 (examples) WRONG as written;
item 7 (consistency) VERIFIED-WITH-AMENDMENTS. No FATAL. The four MAJOR findings are all in the examples file and none
touches RM-F or RM-R ("These do not refute RM-F or RM-R under their full listed hypotheses").

| # | sev. | finding | disposition |
|---|---|---|---|
| 1 | MINOR | tau^2 is not literally E[RSS]/(n-1) | wording fixed in `lemmas/L1b_rss.md` [R06-1] |
| 2 | MINOR | "strict whenever energy is unexplained" too categorical | reworded: weakly weaker, can be strictly weaker [R06-2] |
| 3 | MINOR | names (L-gain)/(L_b) now mean the tau-form but L1_fixed still equated them with GROW G3c | sigma-forms renamed (L-gain^sigma), (L_b^sigma) in L1_fixed/L1b; B1, B1' stated for both; "B2 applies" replaced [R06-3] |
| 4 | NIT | citation drift (UNI L2_k0 154-155; UNI STATEMENT 182-184) | fixed |
| 5 | MAJOR | (E-F2): BM-inf alone does not give the energy bound of (T1-F) | signal condition now "BM-inf and ||mu||^2 <= Mn"; table row updated [R06-5] |
| 6 | MAJOR | polynomial-decay row turned a proof envelope into a necessary size (Sigma = I is a member with bounded Q) | section 7.3 retitled and rewritten: rows describe what the cited PROOFS use, not class membership [R06-6] |
| 7 | MAJOR | one-factor row: "p < n^alpha0" is not UNI-1's hypothesis (limsup log p/log n < alpha0); STATEMENT (C4) advertised p < n/2 | row and STATEMENT (C4) corrected; FAC-B exact-CS named as a separate family-specific result [R06-7] |
| 8 | MAJOR | FAC-PK row omitted NEG's hypotheses (exact Gram, K < p <= n-1, (PK), (PB), ...) | row rewritten with the full qualifications; "LS0 only; nothing about the full method; p >> n open" [R06-8] |
| 9 | MINOR | negative membership claims (LOC-BF "not (D-loc)"; S5 "not partition-free") overreach | reworded as "not needed / not established" [R06-9] |
| 10 | MINOR | ASSUMPTION_MAP still in v1.1 terms | updated to v1.2 with the v1.1 forms marked as sufficient cases |

# Council brief — W2-FAC-X, Theorem FAC-CS-iid (final council under the updated Wave-2 protocol)

Repository: C:\Users\felip\Bayesian-Variable-Selection (branch main). Ticket folder: Theory_work/Wave2/W2-FAC-X/ (below: ".").
Protocols: Theory_work/Wave2/PROTOCOL.md, which extends Theory_work/Wave1C/PROTOCOL.md and Theory_work/Wave1/PROTOCOL.md.

**Deliverable under review:** Theorem FAC-CS-iid = claims (C1)–(C4) of ./STATEMENT.md (v3, locked), proved in
./lemmas/X1_representation.md, X2_perturbation.md, X3_softgap.md, X4_path.md, X5_start.md and X6_assembly.md. It is
summarised in ./REPORT.md §1–§4 and §6. §6 is the list of general-assumption ingredients the proof uses, which a
design-agnostic main theorem (ticket W2-UNI) will rely on. Its claims about what the proof needs must be accurate.

**Not under review:** Target 2 material: REPORT §5, ./STATEMENT_T2.md, ./T2/, lemmas X7–X10.

**Context.** The setting is iid Gaussian rows with compound-symmetric covariance and limsup log p/log n < 1/2. The method
is SMC-BVS as merged on main at commit 4676af6. Its specification is FAC-B STATEMENT §1
(Theory_work/Wave2/W2-FAC-B/STATEMENT.md); State_of_Project sections 02_method.tex and 04_theory.tex
(Theory_work/State_of_Project/sections/); and Theory_work/Wave1C/FINAL/sections/s7_impl.tex. The proofs reuse
FAC-B's L1–L5 (Theory_work/Wave2/W2-FAC-B/lemmas/) as templates. The cited upstream results are listed with their
verbatim statuses in STATEMENT §7 and REPORT §3. Citation check: ./reviews/CITECHECK.txt (script ./reviews/citecheck.py).

**Reading rules (independence).** You may read the statement-lock, lemma-check, mid-point and sweep reviews R01–R07
(including R03b) and their dispositions. Do not trust their fixes: re-verify every one. Do **not** read earlier council
seats or their dispositions (reviews/R08*, R09_council*, R13*, R14_council*, R17*, R08_R09_disposition.md,
R13_R14_disposition.md). Exception: the numerical outputs that REPORT §3 cites in reviews/R09_scratch/ and
reviews/R14_scratch/ may be read as evidence. You must reach your verdict independently.

**Your task: try to break the result.** Look for:
* false steps;
* hypotheses that are used but not stated;
* constants or rates that do not track;
* status upgrades;
* any mismatch with the method as coded.

Re-derive the load-bearing steps yourself. Small falsification numerics are welcome: local, minutes, and run only inside
your scratch folder. ./numerics/iid_core.py simulates the exact iid-row sufficient statistics and the exact production
LS0 path.

**Binding scope rule.** All results are asymptotic. Do not treat "asymptotic only", finite-n behaviour or the size of
the onset n₀ as a limitation or defect.

**Score on six gates.** Give each gate PASS/FAIL with reasons:
* G1 — correctness of every step;
* G2 — hypotheses used = hypotheses stated;
* G3 — no hidden assumptions;
* G4 — cited lemmas have adequate status, with statuses quoted verbatim (check CITECHECK.txt and the sources);
* G5 — constants and rates tracked;
* G6 — fidelity to the method as coded/specified.

Then give an **uncapped overall score from 0 to 10**, and number your issues. Mark each issue REQUIRED (it blocks a
pass), MINOR or EDITORIAL, and give a location and a concrete fix for each.

**Pass rule.** Both seats score ≥ 8.0 and all six gates PASS, in the same round.

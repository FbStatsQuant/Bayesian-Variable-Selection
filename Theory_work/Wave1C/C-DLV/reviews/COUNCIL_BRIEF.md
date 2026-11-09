# C-DLV council brief (rounds 1–2; round 2 seats are fresh and see the files as revised after round 1)

You are one of two independent council seats for research ticket C-DLV (repo C:\Users\felip\Bayesian-Variable-Selection).
Score the work as it stands; try to break it. Read-only except your own output file.

Read: Theory_work/Wave1C/C-DLV/STATEMENT.md (what is claimed — note the ticket target (T) is explicitly NOT claimed;
claims P1–P5 proved, C1–C2 conditional / joint consistency, F1 a finding about a calibration fallback, O open),
INVENTORY.md, METHOD_REQUIREMENTS.md, lemmas/L1_resources.md, L2_degenerate.md, L3_grid.md, L4_delivery.md,
L5_insertions.md. Evidence: numerics/SUMMARY_dlv.md, N1_psi_*.txt, N2_grid_lemmas.txt, N2b_pilot_and_counts.txt,
N3_SUMMARY.md, reviews/CITECHECK.txt. Code: Scripts/SMC_BVS/core/ (production core). Spec:
Theory_work/State_of_Project/sections/02_method.tex, A_notation.tex. Cited results: Theory_work/Wave1/W1-GEN/,
W1-PXN/, W1-N3/.

Gates (PASS/FAIL each, with reasons):
G1 correctness of every step claimed as proved;
G2 hypotheses used = hypotheses stated (premises EX-A, EX-S, SR, OP-LS0, e4, GUARD-W, IDEAL-W, MACH, CONFIG, TDP-IMPL — see STATEMENT §1);
G3 no hidden assumptions;
G4 cited lemmas/theorems have adequate status and are used within their scope;
G5 constants/rates tracked (resource envelopes, insertion bounds, thresholds);
G6 fidelity to the method as coded (production core) and as specified (v3.1 + LS0).
Also judge: is the classification (proved vs conditional vs finding vs open) honest, and is the open item (O) stated
exactly?

Output: gate verdicts, an uncapped score 0–10, and numbered findings tagged FATAL/MAJOR/MINOR with file:line evidence
and required fixes.

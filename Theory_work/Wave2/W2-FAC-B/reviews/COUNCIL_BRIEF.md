# W2-FAC-B — Council brief (round 1)

You are one of two independent council seats for ticket W2-FAC-B of Theory Wave 2 (repo
C:\Users\felip\Bayesian-Variable-Selection). Judge the deliverable on its own; you are briefed to break it.

**Deliverable.** Theorem FAC-CS and its proof:
* Theory_work/Wave2/W2-FAC-B/STATEMENT.md (v3.1, locked; read §0–§6, including the flagged post-lock addition (C1-M));
* lemmas/L1_cs_reduction.md, L2_start.md (incl. L2.5 Corollary M), L3_event.md, L4_path.md (key lemma), L5_assembly.md;
* METHOD_REQUIREMENTS.md; numerics summaries numerics/N1–N7 (diagnostics only, never proofs).
* Review history (you may read it after forming your own view): reviews/R01–R07 and their dispositions; citation check
  reviews/CITECHECK.txt (script reviews/citecheck.py).

**Sources for cited results and the method:** Theory_work/State_of_Project/sections/02_method.tex, 04_theory.tex;
Theory_work/Wave1C/FINAL/sections/s3_posterior.tex, s5_hpm.tex, s6_delivery.tex, s7_impl.tex;
Theory_work/Wave1C/HQ_AUDIT/A1–A4; Theory_work/Wave1/W1-GEN/STATEMENT.md; Theory_work/Wave1C/C-GROW/lemmas/L4_assembly.md.
Python with numpy for independent checks: C:/Users/felip/AppData/Local/Programs/Python/Python313/python (scratch files
only under Theory_work/Wave2/W2-FAC-B/reviews/<your seat>_scratch/).

**Scope rule (binding, from Theory_work/Wave2/PROTOCOL.md):** all target results are asymptotic; "asymptotic only / not at
n = 200" is not a limitation and must not be penalised.

**Six gates** — return PASS / FAIL for each, with reasons:
1. correctness of every step;
2. hypotheses used = hypotheses stated;
3. no hidden assumptions;
4. cited lemmas have adequate status (statuses quoted verbatim and correctly);
5. constants / rates tracked (uniformity of all o(log n) and probability bounds along the path and over p_n ≤ n/2);
6. fidelity to the method as coded/specified (LS0 cap ℓ_n + |S̃₀|, extra scan, scored set, tie rules, K, exact branch,
   delivery premises).

Return also an **uncapped score 0–10** for the deliverable as a whole, the list of required fixes (if any) with
location and reason, and optional suggestions. Pass = both seats ≥ 8.0 with all six gates PASS.

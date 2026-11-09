# Council brief — W2-FAC-A (Theory Wave 2), round 1

You are one of two independent council reviewers (the other is from a different model family). Score the work; do not
coordinate. Repo: C:\Users\felip\Bayesian-Variable-Selection. Read-only except your output file. No state-changing git.

**Read:** Theory_work/Wave2/W2-FAC-A/STATEMENT.md (locked target, v1.2) and all proof files in
Theory_work/Wave2/W2-FAC-A/lemmas/ (00_MAIN.md, L1–L8). Check citations against the sources they name
(Theory_work/Wave1C/C-GROW/lemmas/*, Theory_work/Wave1/W1-GEN/lemmas/*, Theory_work/Wave1/W1-PXN/lemmas/CR_corr_tails.md,
Theory_work/Wave1C/FINAL/sections/*.tex, Theory_work/Wave1C/HQ_AUDIT/A1–A4, Theory_work/Wave1C/C-DLV/lemmas/*). Numerics
(evidence only): Theory_work/Wave2/W2-FAC-A/numerics/*.md, *_out.txt and scripts. The review trail is in reviews/R01–R06
and their dispositions — you may read it AFTER forming your own view, to check that findings were dispositioned
honestly. Do not read LOG.md before scoring. Scope rule (binding): all results are asymptotic; finite-n is not a
limitation and must not be scored as one.

**Method as merged (main 4676af6):** v3.1; LS0 from the start mode with move cap ℓ_n + |S̃₀|; reported model Ŝ⁺ = max
of the all-scored set; tier-1 calibration fallback (delivery claim).

**Six gates (PASS/FAIL each, with reasons):**
1. Correctness of every step.
2. Hypotheses used = hypotheses stated (per clause).
3. No hidden assumptions (method, implementation premises, design, noise).
4. Cited lemmas have adequate status (statuses quoted verbatim; nothing upgraded).
5. Constants/rates tracked (uniformity over the exponentially large lattice; the exponent α₀; o(·) terms).
6. Fidelity to the method as coded/specified.

Also judge honesty of scope: the narrowing vs the original brief (p ≤ n^A, fixed k) to limsup log p/log n < α₀ (= 1/6 on
block compound symmetry incl. S5) with one global factor, Part II's necessity claim (exact-Gram CS, full-lattice route
only), and Part III marked as not claimed.

**Output:** for each gate PASS/FAIL with reasons; an uncapped score 0–10; a numbered list of required fixes (if any) and
optional suggestions. Pass = both reviewers ≥ 8.0 with all gates PASS in the same round.

# Case 1 — KNOWN ANSWER (known-true finding)

**Reviewed object.** W3-MISR-R `STATEMENT.md` v1.0 @ 01873c40, §4 KL reading (ii), lines 124–127 (in INPUTS.md): "(ii) In the setting of §2(b) (with α a function of the design): the conditional law of y^r given the candidate design is N_n((α+a)1 + X^r_𝒞β^𝒞, σ²_𝒞 I_n) … hence the Kullback–Leibler minimiser …; **for jointly Gaussian rows this is BASE's row-wise reading** (SL's f₀, centred rows)."

**The answer.** The row-wise reading is FALSE when the intercept is a function of the design (non-deterministic α); TRUE for deterministic α. Full-design conditional statement is fine. Counterexample: iid N(0,1) candidate rows, no omitted columns, independent N(0,1) noise, α := (X^r_𝒞)²_{2,1}; then y_1 | x_{𝒞,1} is Gaussian plus an independent χ²₁ shift, not Gaussian. Expected finding: MAJOR (L1-1) at STATEMENT.md:124 (esp. 126–127), fix = restrict the row-wise sentence to deterministic α.

**Secondary real findings in the stored 6.1 reply (accepted by the lead, repaired, later passed council R3):** L1-2 (STATEMENT §2(d) "neither … can be non-Gaussian" overstated: only conditionally on the candidate design), L1-3 (conditional-mean remark needs a convention without moments), L1-4 (PLAN H2 (RD): g_n domain/zero-contrast formulation). Count a 6.2 hit on these as "real, secondary".

**How we know (evidence).**
1. The counterexample is a one-line fact (non-Gaussian marginal of Gaussian + independent χ²₁ shift).
2. Second blind 6.1 reviewer re-found it independently on the child's v1.1→v1.2 text: `W3-MISR-R/reviews/K1_linecheck_sol.md` K1-1 (α(X)=X₁²).
3. Lead (Opus 5.5) verdict "FALSE as stated for a non-deterministic intercept; TRUE for deterministic": `W3-MISR-R/reviews/post_cp3/BASE_KL_VERDICT.md`; erratum draft `reviews/post_cp3/ERRATUM_W3-MISR_KL.md` (ERR-W3-MISR-KL1; parent W3-MISR STATEMENT.md:191-195, G_corollaries.md:91-93 — present in INPUTS.md as the parent Cor-H text and G.3 line "y_i | x_{𝒞,i} ~ N(α + a + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞)").
4. The corrected deterministic-intercept reading passed council R3 (sol=10.0, opus=9.6).

**Scoring rubric for the 6.2 reply.** Caught = a finding that names the row-wise KL reading (STATEMENT §4 KL(ii), ~:124-127) and says it fails for design-dependent α (with any valid counterexample). Partial = flags the KL reading as "needs scope" without a counterexample. Missed = otherwise. Count separately: L1-2/3/4 matches; findings that are false or pure nitpicks (manager adjudicates; a finding is "false" if its claimed failure does not occur, "nitpick" if only wording with no mathematical content).
**Not supplied to the 6.2 (listed in the brief but omitted for size):** POST2 / POST statements and lemmas, parent M_misr.md, R_reduction.md, TRIAGE.md. Q3 (a′ from POST2 D(a)) and parts of Q4/Q5 are therefore unanswerable for 6.2; ignore them in scoring (a "not supplied" answer is correct behaviour).

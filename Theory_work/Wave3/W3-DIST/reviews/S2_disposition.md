# W3-DIST — disposition of blind read S2 (`reviews/S2_sol.md`; gpt-6.1-sol, codex, high; manifest 54cf9123…206f)

Object: STATEMENT v1.3.1 §1R (reader versions), §3 bridges, and the changelog tags. Verdict: **REPAIR REQUIRED**.
3 MAJOR, 4 MINOR. Per clause: Theorem A REPAIRABLE (no counterexample to its displays); **Theorem B FALSE-AS-STATED**
(missing b_n > 0); Corollary C REPAIRABLE; B0, B2 REPAIRABLE; B1, B2-core SOUND-AS-STATED; **B3 FALSE-AS-STATED** (same
positivity gap, and a window inequality). All findings accepted; edits in STATEMENT v1.4 and TARGET §6.
| id | sev. | finding | disposition |
|---|---|---|---|
| S2-01 | MAJOR | Theorem B (A6)(b) and B3 never require b_n > 0; with b_n = −1 the written assumption holds and the conclusion fails (explicit counterexample, p = 2) | **ADOPT**: "b_n > 0 and b_n²·n/log n → ∞" in (A6)(b), the notation table and B3. Theorem B is a companion result (TC10), not one of TC1–TC9 |
| S2-02 | MAJOR | B2 and B3 assert q_n ≥ m_n(M log n) + s (resp. m♯_n + s ≤ q_n), false when the window saturates at p (p = 2, s = 1) | **ADOPT** (also stream E's own change request and P5 E-08): the needed and true condition is min{p, s₀ + m} ≤ q_n; ⌈C_qM log n⌉ ≥ m_n(M log n) + s for all n ≥ 2, M ≥ 1. Theorem A's statement is unchanged; the false inequalities were in bridge remarks |
| S2-03 | MAJOR | reader Setup writes the prior with p (raw), the code uses the retained count; a different prior on data sets with a dropped column | **ADOPT**: r := number of predictors not constant in the sample; BB(1, r), cap min(r, ⌊n/2⌋), list of at most 40r + 1 models; posterior undefined when r < 2 or the response is constant, counted in the exceptional probability. Tag: EQUAL for TC9's mathematics (assumptions, displays, constants unchanged) — a faithfulness repair of the description of the method. **Reported to the department manager at once** because it edits the Setup of the headline reader theorem |
| S2-04 | MINOR | general-radii remark lacks its window; "of order log n" only for fixed M; "on the same data sets" needs the joint event; constant renaming; notation (sample means, uniform over models given size, size of I, K clash) | **ADOPT** all: Remark (1), (4), (9); Setup wording; "the two exceptional sets can be taken to be the same set" |
| S2-05 | MINOR | B0's "for every data set" exceeds Lemma R′'s domain; "the posterior does not change" is true for the model posterior, the parameter posterior is equivariant | **ADOPT** |
| S2-06 | MINOR | Corollary C: final-run scope; the list stores log scores | **ADOPT** (with stream D's and P3's wording) |
| S2-07 | MINOR | "no identifiability condition" is misleading: (A4) makes sparse coefficient vectors distinguishable; necessity lines (A2), (A3), (A5) need their qualifications | **ADOPT**: sentence replaced by "no beta-min and no fixed lower bound on eigenvalues", with a note; TARGET §6 lines requalified. (For the master DIST-1 the phrase stays: (ND) is an average determinant condition and DIST-2 has no such condition at all.) |
**Part 2 (statement-change check).** Recorded in the changelog (row "Statement-change check of v1.1–v1.3"): tags
CONFIRMED where S2 could assess them; several EQUAL or mixed tags CONTESTED as literal tags or not assessable without
the old wording (all before the CP1 baseline). S2's explicit audit: the 1.1 domain-remainder row and the 1.3 M-range row
did weaken (1.1)/(1.2) and reader Theorem A historically, before CP1; the footer now says so. No weakening of the joint
metric, of the rate of (1.1) or of (1.2), or of the coded prior.
**Effect on targets fixed at CP1.** TC1–TC8: none. TC9 (reader Theorem A): Setup's description of the prior corrected
(p → r) and one descriptive sentence withdrawn; (A1)–(A5), displays (i), (ii), the sentence without (A4), the constants
and the rate are unchanged. TC10 (companions): Theorem B gains b_n > 0; Corollary C's wording made faithful to the code.
**Still owed:** a cross-family diff check of the v1.3.1 → v1.4 changes (PROTOCOL_v4 §4.2) before the next freeze.

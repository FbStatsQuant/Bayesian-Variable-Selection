# Sol read of X1, X3, X5 v1.1 (lock + line check + re-check) — Codex gpt-6.1-sol (high), delegate ff889fd4, 2026-11-16 (verbatim)

Part A was completed before opening LC2 or the X-item changelogs. No files or git state were changed; no sub-agents were started.

**Part A — independent verdicts**

| Item | Lock | Line check |
|---|---|---|
| X1 | **LOCK** | **VERIFIED** |
| X3 | **LOCK** | **VERIFIED WITH AMENDMENTS** |
| X5 | **LOCK WITH CHANGES** | **VERIFIED WITH AMENDMENTS** |

**X1.** The target is correct: T12 (i.a)–(i.c), (ii), and (R1)–(R3) for the code of record. The core has no diff against 4676af6. I checked the initialization, fixed-grid stages, evidence increments, resampling, rounds, stream consumption, and RB recording against the cited code. The bridge, reversibility, prefix invariance, conditional means, induction, and RB identity are correct. The valid-input hypothesis and statistical-record convention are explicit. No amendment remains.

**X3.** The referenced claim is W3-POST:Lemma-1a′. The variational substitution gives the stated deterministic bound on \(Q_T^c\), including \(t=0\). The exponent bound, determinant bound, expectation of \(\Lambda'_n\), numerator normalization, zero-tail case, Markov assembly, and cutoff conclusion are correct. No eigenvalue assumption is introduced. The claim can lock; the citation amendment below remains.

**X5.** N1 and linearity establish the pooled identity for the potential pair \((\mathcal A^\circ,\mathcal C^\circ)\). The joint-law argument is valid with MEAS-J and the stated joint independence, and the expectation equality can be interpreted in \([0,\infty]\). The correction concerning actual guarded success is also correct: CAL fails for the actual calibration record, and equality does not transfer merely from \(\mathcal A\subseteq\mathcal A^\circ\).

The remaining amendment is to make this corrected scope govern the verification label explicitly. The original PoolZ wording is not verified without the qualifications already identified in X5-b.

**Part B — LC2 repair check**

Here “RESOLVED” concerns the specific LC2 finding; the remaining findings follow the table.

| LC2 finding | v1.1 result | Evidence and regression check |
|---|---|---|
| X1 #1 — T12 proof ranges | **RESOLVED** | Proof:43, lines 47, 50, 71 now identify the correct lemmas and post-terminal paragraph. |
| X1 #2 — statement range omitted (ii) | **RESOLVED** | Statement:10 includes line 64. |
| X1 #3 — actual arguments and budgets | **RESOLVED** | Statement:22 gives the variable call, Hm chain, and executed-budget convention. |
| X1 #4 — scope of code changes | **RESOLVED** | Proof:83 limits the assertion to the island path and identifies the other changes. |
| X1 #5 — valid input | **RESOLVED** | Statement:28 states the hypothesis. |
| X1 #6 — statistical record | **RESOLVED** | Statement:32 points to the record convention. |
| X1 #7 — bridge proof/status citations | **RESOLVED** | Proof:9 includes the full proof; statement:16 locates the status. |
| X3 #1 — prior check history | **RESOLVED** | Statement:4 distinguishes the registry label from prior checks. See finding 3 for citation precision. |
| X3 #2 — division by zero | **RESOLVED** | Proof:37 splits off \(R_m^T=0\) before dividing by \(v_m\). |
| X3 #3 — corrected prior-tail definition | **RESOLVED** | Proof:34 attributes the corrected form to W3-POST and limits the T03R equivalence appropriately. |
| X3 #4 — summary hypotheses/conclusion | **RESOLVED** | Statement:14 includes G, \(n\ge3\), and the cutoff conclusion. |
| X3 #5 — P1 proof ranges | **RESOLVED** | Statement:21 includes the complete cited proofs. |
| X5 #1 — joint measurability/independence | **RESOLVED** | Statement:23, proposed premises at line 39, and proof:15 supply the missing qualifications and nonnegative-expectation interpretation. |
| X5 #2 — PoolZ proof range | **RESOLVED** | Proof:3 correctly gives lines 25–33. |
| X5 #3 — wrong failing premise | **RESOLVED** | Statement:28 correctly identifies CAL, while retaining actual-record success measurability. |
| X5 #4 — clock independence | **RESOLVED** | Proof:28 requires joint independence and explicitly rejects pairwise independence as sufficient. |

No repair introduced a mathematical regression.

**Remaining findings**

1. **S — qualify X5’s verification label.** X5 statement:21 says “VERIFIED. The proof is correct,” while lines 28–35 establish a corrected reading of the source claim. Proof:27 correctly states what was proved. **Fix:** label the source check **VERIFIED WITH AMENDMENTS**, and state directly that the verified identities use \((\mathcal A^\circ,\mathcal C^\circ,\widehat Z^\circ)\), with MEAS-J and joint independence for the joint-law form. Retain actual-\(\mathcal A\) equality only under the additional clock-independence premise. This requires wording alignment, not another mathematical argument.

2. **F — X3’s variational-form citation stops one line early.** X3 proof:9 cites P1 lines 68–72 for the minimum representation. That representation appears at P1:73. **Fix:** cite 68–73, or 68–81 to include the proof. The calculation is correct.

3. **F — distinguish the sources of X3’s check history.** X3 statement:5 includes council C3 `correct:PASS` under the citation to lemma-header lines 3–5. Those lines record R01, R02, and C1; C3 is recorded in the registry row (claims.tsv:343). **Fix:** cite the registry row separately for C3. The reported history is supported; its attribution needs precision.

No C finding.

X-SOL-VERDICT: X1 lock=LOCK, check=VERIFIED; X3 lock=LOCK, check=VERIFIED WITH AMENDMENTS; X5 lock=LOCK WITH CHANGES, check=VERIFIED WITH AMENDMENTS

# SL1 — reply of the Sol statement-lock reviewer (gpt-6.1-sol, reasoningEffort high), verbatim
<!-- received 2026-11-17 via delegate_task (T3 child thread, codex); brief: reviews/SL1_brief_sol.md; reviewed STATEMENT v0.1 @ e2d57d44 -->

SL1-VERDICT: LOCK WITH CHANGES

Reviewed the latest draft, including the expanded C3(i)–(iii). The code supports both previously unchecked DIST links. The remaining changes concern qualifications in C3(ii).

1. **SL1-1 — MAJOR: missing exact-branch NA qualification.**  
   [STATEMENT.md:109](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/STATEMENT.md:109) asserts `|log_Z_list − log Z| ≤ 2t_n` for every output run. Section 1 expressly permits `log_Z_list = NA` on the exact branch; this makes the displayed inequality undefined. The probability statement at lines 111–113 inherits the omission.

   **Fix:** qualify both evidence assertions with “when `log_Z_list` is not NA,” as already done in C3(i). Define the evidence bad event explicitly as `{log_Z_list is available and |log_Z_list − log Z| > 2t}`.

2. **SL1-2 — MINOR: the median-model endpoint needs justification.**  
   [STATEMENT.md:106](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/STATEMENT.md:106) allows `t_n = ½` and concludes median recovery from `ε_n ≤ t_n`. LIST-K(c) proves recovery only for `ε_n < ½`. The same gap occurs in the median failure bound for `t = ½`.

   The boundary matters algebraically: with Ω = `{∅, {1}, {2}}`, posterior masses `(0.3, 0.5, 0.2)` and S₀ = `{1}`, S₀ is the unique mode but the strict-threshold MPM is empty. Additional eventual properties of the coded model space might exclude this boundary, but the planned argument does not establish them.

   **Fix:** use `t_n ∈ (0, ½)` and `t ∈ (0, ½)`. This preserves the intended asymptotic result without another argument.

3. **SL1-3 — MINOR: propagate the rate hypothesis.**  
   [STATEMENT.md:104](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/STATEMENT.md:104) correctly qualifies `ε_n = O_P(r_n)` by eventual `p ≥ 2`, but the following “Hence” paragraph does not explicitly retain that hypothesis. POST omits `p = 1` at [L1_POST.md:10](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:10).

   **Fix:** begin the threshold-sequence conclusion “Under this eventual `p ≥ 2` condition, …”, or supply the separate scalar argument.

The interpretive sentences and clauses inside C1–C3 have the following dispositions:

| Location | Interpretation | Verdict |
|---|---|---|
| C1(a) | Maximum over retained columns | Correct definition clarification. |
| C1(b) | “in particular” the PIP comparison | True; apply the TV bound to `{S : j ∈ S}`. Include this step in L1. |
| C1(d) | “hence” the evidence inequalities | True; use `π(𝒯) ≥ π(S₀)` and `−log(1−ε) ≤ ε/(1−ε)`. |
| C1(e) | Full-list quantities are exact; (a), (c) apply without a list | True by substitution `𝒯 = Ω`. |
| C2(i) | Completed ⇔ estimates available ⇔ output | Supported by `v3_run.R:143–149,218` and the fit wrapper’s return paths. |
| C2(i) | Actual LS0 has the hypothetical search’s evaluation sequence | True under the imported configuration and exact-score premises; L2 must spell out cache invariance and deterministic scan/tie rules. |
| C2(i) | “in particular” S₀ belongs to the offered set on 𝒦_n | Follows from the preceding identity and CC2’s cache/offer argument. |
| C2(ii) | `hpm` is RM/RM2R’s reported model | Supported by the reporting assignment and imported reported-model definition. |
| C2(v) | “Consequently” unique mode plus discovery gives list membership and `hpm = S₀` | True from (ii)–(iv); the top-store and HPM orders coincide completely. |
| C3 preamble | “in reader form” Theorem 6(A1)–(A6) | Valid coverage statement. The reader assumptions are sufficient forms of the master assumptions, rather than a literal equivalence. |
| C3 preamble | “so that” P(𝒢⁺_n) → 1 | Supplied by RM2-R-plus/RM0-plus. |
| C3(ii) | T1-R is POST’s LSF hypothesis; posterior rate follows | Supported, with eventual `p ≥ 2`. |
| C3(ii) | “Hence” the common threshold events and simultaneous conclusions | Valid after SL1-1–SL1-3. No independence or union over seeds is needed. |
| C3(ii) | “the same bound holds” for the remaining errors | Valid after those fixes; name the events individually instead of “other three errors.” |
| C3(iii) | Delivery removes “on output” and yields consistency/rates | Supported by DLV-0, C3(i) and POST; retain the evidence-availability qualification. |

Plan viability: the proposed route is sound and contains no hidden new key lemma. LIST-K is elementary finite-posterior algebra; LIST-CODE needs a careful but direct code argument, especially that cache hits were previously offered and that `top.offer` preserves the HPM maximum. The common-event quantifier and either-branch coverage follow from the imported theorem and these deterministic facts. The cited registry inputs are RM2-R-plus/RM0-plus/DLV-0@1.0.1 and RM-0@1.0.0, “PROVED-CHECKED”; CC@1.1.2, “CODE-CHECKED”; and POST@1.0.7, “PROVED-CHECKED.” IMPL-LIST appropriately remains a named implementation premise until the method commit is checked.

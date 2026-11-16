## W3-RM2-R council R1 review (seat sol; codex gpt-6.1-sol, reasoningEffort high; fresh, blind). Reply verbatim below (link targets shortened).

| id | decision |
|---|---|
| W3-RM2-R:RM0-plus | ACCEPT |
| W3-RM2-R:DLV-0 | ACCEPT |
| W3-RM2-R:RM2-F-plus | ACCEPT |
| W3-RM2-R:RM2-R-plus | ACCEPT |
| W3-RM2-R:SAND-F-c | ACCEPT |
| W3-RM2-R:TL-F-c | ACCEPT |
| W3-RM2-R:Ex-Proxy-d | ACCEPT |
| W3-RM2-R:Cont-plus | ACCEPT |

These decisions retain the brief’s explicit conditions: SOP:TH09 for Form F, W2-APP:POST for Form R, and the inherited code-reading audits for DLV-0. The theorem proofs pass; two documentation findings block the overall gates.

Findings:

1. **F — Incorrect literature comparator.** [TARGET.md:24] attributes a constant-level beta-min selection guarantee of the same order to “Song–Liang (2015) Thm 1–2.” For the split-and-merge paper identified by the inherited literature map, those theorems establish posterior contraction in Hellinger distance. They do not state the attributed beta-min support-recovery guarantee. Sure screening is addressed separately in Theorem 3, and MAP consistency in supplementary Theorem S. Thus the assertion about all three comparators having the stated constant-level selection form is unsupported. **Fix:** identify the paper explicitly and remove this attribution, or give the correct selection theorem and derive the comparison under its actual assumptions. The Yang–Wainwright–Jordan comparison can remain independently. [Song–Liang, §§2.1–2.2](https://academic.oup.com/jrsssb/article/77/5/947/7040600).

2. **S — Necessity wording exceeds the evidence supplied.** [TARGET.md:10] says the beta-min order is “necessary by numerics/heuristic.” Neither numerical observations nor a heuristic establish necessity. The cited W3-POST statement supplies a sufficient beta-min theorem; its posterior-rate lower bound is a different assertion. This also conflicts with this ticket’s express numerical limitation that the sweep establishes no asymptotic necessity. **Fix:** say explicitly, “HEURISTIC: suggests this order; necessity is not proved here,” or supply a properly scoped necessity proposition and proof. This does not invalidate RM2-F-plus as a sufficient theorem.

3. **E — “Only competitor” should mean “binding competitor.”** [numerics/RESULTS.md:158] calls the empty set the only truth-removing competitor when \(S_0=\{1\}\). Swapping truth 1 for any other column also removes the truth. The implementation correctly includes those swaps. I independently recomputed \(F(S_0)-F(\varnothing)\) for all 224 P runs; it agrees with the recorded full truth-removal margin to approximately \(1.4\times10^{-12}\). **Fix:** write “the empty set is the binding truth-removing competitor in these runs.” The recorded results need no correction.

4. **E — Make R7.2’s constant choice explicit.** [READER_DELTA.md:61] writes \(D=2+4A+o(1)\), although the master’s sufficient form uses a fixed \(D\). Its coefficient threshold is also expressed using \(n\), whereas \(\lambda_n\) contains \(n-1\). **Fix:** choose a fixed \(D>2+4A\) and a strict coefficient margin above the displayed maximum. This makes the advertised “large enough” implication immediate and absorbs \((n-1)/n\). I accept that qualified bridge conclusion.

5. **E — Stale planning text.** [TARGET.md:3] still names statement v0.1; [TARGET.md:32] describes completed numerics as planned. **Fix:** name v1.0 and point to the completed sweep through \(\kappa=32\), retaining its limited mode-margin interpretation.

The existing ERRATA E1 concerning Q1 Remark 3 remains appropriate.

Sweep duties:

**(1) Statement copies against lemmas.** I matched RM0-plus to Q4, DLV-0 to Q5, the two assemblies and containment to Q6, SAND-F-c to Q1, TL-F-c and POST/MODE-F to Q2, and Ex-Proxy-d to Q7. The changed visibility margin is positive precisely under the stated strict bound on \(M_V\). The truth-removal score margin gives exactly the stated \(c_{\mathrm{TL}}^0\). The block-relative variants retain the required lattice floor. No mathematical statement/proof mismatch found.

**(2) Quantifiers and uniformity.** The reporting argument supplies one common data event; it does not interchange a limit with a supremum over run parameters. Down-closure supplies the intermediate deletion sets needed by NA. The onset thresholds retain their dependence on constants, hypothesis onsets and deterministic rate envelopes. DLV-0 explicitly restricts inputs, configuration, allocation and machine premises; the bounded domain without the two lifts is correctly separated from asymptotic delivery.

**(3) Lemma scopes and downstream uses.** Q4 uses Q5 only for its delivery clause. Q6 supplies Q1’s block hypotheses, Q2’s \(q\log n/n\to0\), floor and addition-event hypotheses, and the posterior condition separately. Form R uses the unchanged parent bridges under their original scope. Q7 verifies the signal-dependent clauses for decaying \(\theta_n\), including the strict separation between BM-W and BM-Q. No downstream use exceeds the supplying lemma.

**(4) REPORT and REGISTRY.** Claim IDs, statement pointers, proof pointers and substantive statuses agree with STATEMENT. The posterior conditions remain explicit, and DLV-0’s audit qualification is retained. No withdrawn DLV-0 implication edge reappears. Cont-plus distinguishes its implication targets from the parent containment results consumed for composition. The TL-F-c record groups Q2’s posterior subsection with its truth-removal subsection, but expressly qualifies §6; this does not strengthen the mathematical claim.

**(5) DEPS and manifest.** All 20 DEPS records match their recorded SHA-256 prefixes, including statement-range hashes, parent-file hashes and lemma hashes; `sha` and `checked_sha` agree throughout. Manifest verification passed before and after the review. I did not inspect the prohibited review files, LOG or CHECKPOINT files, and made no filesystem or git-state changes.

**(6) Reader bridges.** R7.1 correctly converts the coefficient threshold to BM(c). R7.3 is the master’s sufficient BM-Q♭ form; R7.4 reproduces V♭. R7.2 supports the explicitly qualified “large enough” conclusion, with the editorial clarification in finding 4. The conclusion bridge retains the delivery conventions, two lifted ceilings and sufficient allocation.

The six gates:

- **correct — PASS:** all eight claims have valid proofs under the stated conditions.
- **strength — FAIL:** TARGET’s necessity assertion exceeds the supplied evidence.
- **faithfulness — FAIL:** the Song–Liang theorem attribution is inaccurate.
- **lit — FAIL:** the beta-min parity row requires correction.
- **necessity — FAIL:** finding 2 remains in the frozen TARGET.
- **better — PASS:** the adopted improvements and deferred quantile, equicorrelation and aggregated-leak proposals have dispositions; I found no additional undispositioned improvement requiring this rider to expand.

COUNCIL-VERDICT round=R1 manifest=4c2183ce4a87dfa35cdf95977a06a85915d0c96b65b43f327de69102558cd402 seat=sol score=8.5 gates=FAIL

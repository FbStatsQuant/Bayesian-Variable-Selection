# R03 (Astra, break review of DESIGN_v1) — disposition by the lead, 2026-11-11

Review: `R03_design_astra.md` (Codex gpt-6-astra, reasoningEffort high), on DESIGN_v1 revision 1 (commit c4b6bb6).
Verdict received: **UNSOUND** (5 findings labelled CRITICAL, 12 MAJOR, 1 MINOR). All 18 are accepted. DESIGN_v1 was
rewritten (revision 2). No second Astra round was run in leg A; revision 2 is therefore **not re-reviewed**, and
CHECKPOINT_1 says so.

| # | finding | disposition in revision 2 |
|---|---|---|
| 1 | Cross-fitted identity stated with the normalised weights W_r: false (take h = 1) | Fixed. §4.3 separates ω_r = Ẑ_r / Z from W_r; O1(e) states the identity for ω_r only and says it gives no orthogonality of normalised contributions or of mutually dependent leave-one-out errors. |
| 2 | "within 5%" contradicted by the common constants; "one third of v0" wrong | Fixed. §1 reports the residuals −3.2%, −10.8%, +6.3% and the ratio 0.41. |
| 3 | N = p costs did not follow the stated formula; I range unstated; escalation multiplier too coarse | Fixed. §2 uses one convention (T = 35, I = 8 … 13): 0.39 / 1.57 / 6.3 h per island, 4.2–5.9 / 17–23 / 68–94 h per fit; escalation described, not multiplied. |
| 4 | MiB reported as GB; resident peak equated with 24 p² | Fixed. All memory in GiB; resident peaks (9.24, 6.26 GiB) are shown next to the dense-array sizes (8.94, 5.96 GiB). `analysis/units_and_setup_tables.R` writes GiB. |
| 5 | R_eff / R ≥ 0.60 false (0.5975); "invisible" not justified (up to 1.33 SE) | Fixed. §4.4 gives 0.597; §7(ii) gives the difference in absolute terms and in standard errors. |
| 6 | 1/√N scaling not established | Fixed. §4.4 says "compatible with, does not establish", lists the reasons and the counterexample, and names the needed experiment. The κ fit is removed. |
| 7 | "far from degenerate", the tail explanation and "T grows slowly" generalise beyond the data | Fixed. The evidence base and its limits open the document; the causal sentence is removed; §4.4 ends with what is not known. |
| 8 | W3-P6 counts had no auditable source | Fixed. `analysis/p6_e2_table.py` and `results/p6_E2_by_np.tsv` (source path, inclusion rule, runs and designs per cell); the caveats are in §4.4. |
| 9 | O1/O3 route needed qualifications | Fixed. O1 (a)–(e) and O3 carry them (independence argument rather than tower; integrability; stage-t identities; the Rao–Blackwell bridge; what an R′ → ∞ statement needs). |
| 10 | Finite-R ratio bias and the right CLT variance missing; "only" consistency too categorical | Fixed. §4.3. |
| 11 | No worker or census stream contract | Fixed as a specification of what must be built (§4.1) and obligation O18; nothing is implemented. |
| 12 | Union stores do not define a merge; long double misattributed | Fixed. §4.1 merge rules, the output-equivalence class and O17; log-sum-exp stays R double. |
| 13 | Merge and serial tail not budgeted; unsourced 1–2 GB claim | Fixed. §4.1 "serial tail" with the measured scan cost and the record sizes; the unsourced claim is removed. |
| 14 | Census rule and diagnostics unspecified | Accepted as open: §4.5 lists what must be declared and adopts no rule. |
| 15 | Missing obligations (Markov bound, retries, flags, card; deferred v0 items) | Fixed. O6 extended; O19, O20, O21 added; v0 O8/O11/O13/O15/O16 listed as deferred. |
| 16 | §7 steered | Fixed. Two neutral tables with "what is not known" rows; the header states that nothing is decided and that the measurements do not settle either question. |
| 17 | Alternatives omitted | Fixed. Streaming reducer adopted in the merge rule; the correct effect of parallel diagnostic islands in §4.2; independent calibration groups and island-level resampling listed in §8 as not adopted. |
| 18 | Source audit | Fixed. New source tables `results/leg_a_units_calibration*.tsv`, `leg_a_setup_compare_round{A,C}.tsv`; every number in §1–§3 names its table; the 25k refusal point is replaced by "between 20k and 30k, depending on the timed score". |

Numbers the reviewer recomputed and that revision 2 quotes on the reviewer's authority: the per-fit range of the
diagnostic-to-final ratio (0.3 to 13).

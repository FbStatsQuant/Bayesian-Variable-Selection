# A6 Sol fidelity read: disposition (Writing manager, 2026-11-23)

Read: `reviews/A6_sol_fidelity.md` (gpt-6.2-sol, high; snapshot of commit ff259612). Verdict NOT-FAITHFUL, 56 findings:
C 11 / S 17 / F 27 / E 1. Every finding was checked against its cited source. **All 56 accepted and fixed; none rejected.**
Sol's registry and code claims were re-derived independently: the registry has 16 first-parent commits and 22 changed
shared rows (by `status` column); `v3_engine.h:405-414` returns the best improving neighbour at the move cap;
`v3_fit.R:173-176` adds the list fields for completed runs.

| ID | Fix |
|---|---|
| A01–A03 | Result 1 "In words" now lists every hypothesis (sub-Gaussian rows, polynomial p, fixed size, bounded-away coefficients, population floor); "at most of order". |
| A04, A06, A08, A10, A12–A14, A16 | Table tab:results rows completed: PIP bound (R1); the level-M probability form (R2); "every design meeting its hypotheses", admissible runs, delivery under C2+ (R3); GL, budget inequality, C1 (R4); per-island vs pooled, uninterrupted run, nothing given completion (R5); size restriction for (a), hypotheses for (b), in-probability form (R6). |
| A05, A07 | Result 2 "In words": level fixed first, n large with M ≤ √n/log n; sub-Gaussian on sparse directions, polynomial p, signal bound in noise units. |
| A09, A10 | Result 3 "In words": Gaussian rows, fixed signals, floor, full Assumption 4, admissible runs, delivery under C2+. |
| A11 | Result 4 "In words": budget k_n < K, θ_lo, M_1, the inequality (k_n may be a small multiple of n/log p). |
| A13 | Result 5 "In words": each island unbiased; pooled on a successful calibration, uninterrupted run; nothing given completion. |
| A15 | The two consequence sentences of Result 6(a), dropped in this edition, restored inside the statement. |
| A17 | Exact-order note: "σ0 < p ≤ n−1, at least one null predictor". |
| B01–B03 | Status boxes say the registry strings still read "conditional on" inputs that are themselves proved and checked (housekeeping, App. E). |
| B04–B06 | §8.1: 16 commits (two citation/manifest re-freezes), 22 changed rows + one added row re-frozen; "no change is a downgrade" (rewrites included); Table tab:status-diff gains the locality-lemma row. |
| B07, B08 | Verbatim table: the five MISR rows split with their exact tag strings; Cor-G(b) notes the omitted input-version clause; header count 22 + 1. |
| B09 | "are to be retired". |
| C01 | Their Theorems 1–3 (not "their theorems") need λ_n → 0 / force P_n → ∞; P_n ≻ n^θ called their standing choice. |
| C02 | (SP) vs SL: Theorems 2–3 use (4); Theorem S assumes a sparse model without citing (4). |
| C03 | Short answer: SL have visibility only in marginal form (Condition 5, screening); ours is conditional with a uniform margin. |
| C04, C05 | (SGR) vs Condition 1: their cap within our window 5(A+1)(s0+1) log n; centred unit-variance Gaussian rows. Table cell updated. |
| C06–C08 | (EFS) vs SL rewritten by theorem: Condition 3 (stronger when our window covers its sets); Theorem 1 (no Gram floor: not comparable); Theorem S (22)–(23) two-sided, (26) both tails: not comparable. Short verdict and table cell updated. |
| C09 | Assumption 3(e) has no direct SL counterpart (upper bound only). |
| C10 | SL Theorem 3 described as a per-identifiable-predictor bound; sensitivity after thresholding when all are identifiable (Results 1 and 4). |
| C11 | SL sampler limits: under convergence conditions they cite rather than verify. |
| C12 | Larger radii: ours holds by monotonicity with the exponent of a level M ≤ √n/log n. |
| D01 | tab:prior likelihood row: raw-scale intercept; centred model scored with no intercept parameter. |
| D02 | Stage 1: the resource check runs on both branches. |
| D03 | 90% ESS is the main construction's target on candidate models; fallback need not; not a bound on the final run. |
| D04 | Stage 6: at the cap an improving scan returns the best neighbour, uncertified; scanned models count towards the best. |
| D05 | Outputs: completed runs report list-renormalised PIPs/MPM/evidence; tab:engine row rewritten ("outputs from the list"). |
| D06 | 10^4 particles for the rung and pilot runs at 10^5 (two continuity runs at 2,500). |
| D07 | Engine calibration: candidate grid from the pilot, pilot schedule as fallback; I_max = 0 = no diagnostic rebuilds; m = 1 leaves the selected grid unrefined (text and table). |
| D08, D09 | tab:engine: next-fit packing by smallest index; rolling admission of kernel passes. |
| D10–D13 | Checking paragraph: exact pre-declared criteria (HPM ≥ 9/10; MPM 20/20; max(0.01, 3 s.e.); 3 combined s.e. with yardstick/floor); registered script not clean (defect), amended script governs; HPM 10/10 is a result; the I_max = 0 re-score used 14 rerun fits. |
| D14, D15 | §7 intro: post-1M work conditional and not committed, paused until the owner restarts it; 10^7 engine bit-identical at default settings on the overlap and 10^6 fixtures. |
| D16 | Open problem 1: Corollary 6L's pathwise hypotheses stated (truth in list, small miss). |
| D17, D18 | Open problem 7: identity on the data sets tested only; secondary evidence-weighted pooling named. |

Not re-checked by a second reader (brief: one Sol read; no Fable). The C fixes restore or narrow wording to the checked
statements and the sources; none adds a claim.

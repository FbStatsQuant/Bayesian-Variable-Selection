# C-DLV council review — Codex seat, round 1

SCORE: **7.6 / 10.0** (uncapped)

**Verdict: changes required.** The deterministic grid analysis and the pathwise consistency argument withstand review. The resource theorem does not yet cover all configurations admitted by CONFIG with the bounds actually displayed. Two localized resource-accounting fixes are needed before accepting P2 and its downstream resource-elimination conclusions at their advertised scope. I do not count the explicitly unclaimed target (T) as a missing proved theorem.

## Gate verdicts

| Gate | Verdict | Reason |
|---|---|---|
| G1 — correctness of every proved step | **FAIL** | L1's work/memory envelopes omit the costs of the allowed custom-h extension, and its simplified sufficient allocation drops certificate memory. See findings 1–2. I found no error in L2, L3, L5, or the delivery/consistency arguments once a valid resource envelope is supplied. |
| G2 — hypotheses used equal hypotheses stated | **FAIL** | R.3′ and the displayed accumulator terms use the default list's O(pB) cardinality and O(1) evaluation cost, whereas CONFIG also admits declared functions of arbitrary polynomial evaluation cost. The final quadratic memory allocation additionally needs a restriction on certificate memory that CONFIG does not impose. |
| G3 — no hidden assumptions | **FAIL** | Polynomial cardinality and representation size of the custom function list, its aggregate evaluation cost, and its workspace bound are missing. A polynomial cost for each individual function does not supply these assumptions. |
| G4 — adequate citations and use within scope | **PASS** | The GEN/PXN inputs have the recorded PROVED-CHECKED status; L4 uses their data/search conclusions through an explicit pathwise argument, without conditioning on delivery. W1-N3's TDP is correctly treated as a proved reference algorithm, with its implementation and storage guarantee separately assumed. The LH-iid route can use the repaired W1-PXN result rather than silently upgrading GEN's conditional LH-iid instance. |
| G5 — constants and rates tracked | **FAIL** | The grid thresholds, finite bisection depth, insertion constants and shorter-range correction are tracked correctly. Resource rates cease to be valid at the CONFIG extensions identified in findings 1–2. |
| G6 — fidelity to production core and v3.1 + LS0 specification | **PASS** | The calibration call graph, escalation rule, failed-rebuild behavior, runtime guard and unavailable-output convention are represented faithfully at the level relevant to delivery. LS0, the e4 fallback and stacking are explicitly specification/premise components; their absence from the production core is not disguised as implemented behavior. F1 is correctly identified as a change to calibration. |

## Numbered findings

1. **[MAJOR] CONFIG's custom-h branch is outside the proved work and memory envelopes.**

   **Evidence:** `Theory_work/Wave1C/C-DLV/STATEMENT.md:31–35` admits the default list **or declared functions of polynomial evaluation cost**. However, `Theory_work/Wave1C/C-DLV/lemmas/L1_resources.md:72–79` charges the accumulator using the default-list terms involving `2pB`; `L1_resources.md:98–101` gives only the default-list calculation and then says polynomial-cost user functions are covered. It supplies no corresponding multiplier or workspace term. The specification permits a finite declared list of bounded functions, rather than imposing the needed asymptotic size/cost restriction (`Theory_work/State_of_Project/sections/02_method.tex:514–519`).

   **Why this breaks the claim:** Even a single bounded function with an evaluation algorithm taking Θ((n+p)^10) operations satisfies the stated polynomial-cost condition. On p=n, the current default-work asymptotic is O(n^5 log³ n), while evaluating that function at Θ(N_e) measured endpoints already exceeds it. A polynomial-size temporary workspace can likewise exceed the displayed memory envelope. Separately, a list of 2^p distinct O(1)-cost functions is finite at each n and satisfies the per-function condition, but prevents even the general polynomial-resource conclusion. MACH bounds time and bytes in terms of actual operations and words; it does not bound these omitted quantities.

   **Required fix:** Either restrict CONFIG to the explicitly costed default accumulator, or declare polynomial envelopes for list cardinality/representation, aggregate evaluation cost per particle, evaluation workspace, and retained accumulators. Add the corresponding terms to W̄, M̄ and Corollary R, and propagate the resulting allocation to P2, P4, C1, C2 and F1. For example, if E_H bounds the sum of evaluation costs over the list, the work contribution must include the number of measured endpoints times E_H. A per-function polynomial-cost sentence alone is insufficient.

2. **[MAJOR] The simplified resource rates discard certificate terms that the full envelopes explicitly retain.**

   **Evidence:** `Theory_work/Wave1C/C-DLV/lemmas/L1_resources.md:74–75` includes `Cert(n,p)` in W̄ but omits it from the asserted big-O equality. `L1_resources.md:79–80` correctly retains `Cert_M(n,p)` in the memory bound, and `L1_resources.md:102–103` requires only that the certificate budgets be polynomial. Nevertheless, `L1_resources.md:134–137` advertises `mem_n = C·(n+p)²` as a sufficient allocation throughout CONFIG. `Theory_work/Wave1C/C-DLV/STATEMENT.md:43–44` makes Corollary R's polynomial envelopes the declared allocation used downstream.

   **Why this breaks the claim:** Polynomial does not mean quadratic. A certificate computation holding Θ((n+p)^3) words, with a polynomial operation budget, is compatible with the stated CONFIG premise. No fixed C makes the advertised quadratic memory allocation cover it. Similarly, a certificate operation budget of degree above the core-work envelope invalidates the displayed work big-O equality. This is not an objection to the full max-based allocation at `L1_resources.md:126–133`: that form correctly retains M̄ and W̄. The error is the later claim that the simplified shapes suffice under the same hypotheses.

   **Required fix:** Retain `+ Cert(n,p)` in every work-rate display and `+ Cert_M(n,p)` in the sufficient memory allocation, along with any custom-h terms introduced for finding 1. Alternatively, explicitly restrict the certificate budgets to orders dominated by the displayed core envelopes. Make STATEMENT's allocation reference unambiguous so that the invalid simplified memory formula cannot be used to discharge resource paths.

## Classification and the open item

The classification is substantively honest. T is expressly unclaimed; P1–P5 are reductions/deterministic results under named premises; C1 is a sufficient condition rather than a demonstrated high-probability event on the classes; C2 is joint with delivery; and F1 concerns a modified calibration law. Findings 1–2 require repair of the scope of the P2 proof, rather than promotion of T or a new statistical premise.

O identifies the correct remaining **statistical** obstruction: show that the probability of any failed realized tier-1 construction tends to zero, accounting jointly for interval overflow, finite-depth non-progress and failed post-snap validation. The realized candidate sets and pilot stage counts must be controlled across all actual preliminary/rebuild calls. Pilot slack alone is insufficient; the candidate-family conditions and snap event still need treatment. This is exactly the residual obstruction after valid resource envelopes are supplied. I found no additional missing statistical obstruction in the reduction.

The treatment of numerical evidence is appropriately limited. N1 does not justify the proposed uniform dominance/variance route; N3's selected pairs do not establish the two-model hypothesis, and alternative pairs were not searched. The successful finite production runs do not prove asymptotic delivery or control the tier-1 failure probability.

## Verification performed

Read the requested statement, inventory, method requirements, all five lemma files, numerical summaries/outputs and CITECHECK; traced the relevant production R/C++ paths; checked the method/notation specification and the cited GEN/PXN/N3 statements, reports and proof passages. CITECHECK was treated as a location aid, not as proof of a citation's mathematical applicability.

Independent read-only 80-digit decimal probes reproduced the two-model snap counterexample (`validation_failed`) and a high-d-range example (`non_progress`), confirmed θ = 0.9182736455463728, s_θ = 0.5881436871152899, λ_θ = 2.4191189092499972 and the phase-count ratio 20.45257077307228, and found no insertion-bound violation in 12 additional families with an analytically controlled remainder. The installed Python lacks mpmath, so the repository's mpmath suites were not rerun; their saved outputs were inspected. These finite probes support the code reading and constants, not an asymptotic probability claim.

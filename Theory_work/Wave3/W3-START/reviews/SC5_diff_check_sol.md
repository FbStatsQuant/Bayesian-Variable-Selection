MANIFEST e6d594199cb7f0c527c091cfdb5785ec155ba7b5dc17ecaa88debfee9e19415c
Verdict: EDITORIAL ONLY WITH CHANGES

Findings

1. MINOR — numerics/RESULTS.md:130–132. The revised observation still says that U decreases over the sizes run for both C_L = 2 and 4. For C_L = 2, the displayed sequence is 5.1, 6.4, 2.6, 3.4; summary.csv confirms 5.1141, 6.4204, 2.6132, 3.3483. It decreases overall, but is not decreasing over the sequence. Required replacement for the sentence beginning “For C_L = 2 and 4”: “For C_L = 2, U fluctuates with n and is smaller at the largest size than at the smallest; for C_L = 4, U decreases over the sizes run. U remains above 1 in both cases. The theorem gives an asymptotic bound n^{−1/2}e^{C_R√log n}, not monotonicity at given sizes.” This is an editorial repair to an observation, not a change to a theorem or numerical result.

2. MINOR — ASSUMPTION_MAP.md:18,30–31. The map retains the old shorthand that the interface [VIS] is necessary. The deterministic bound o₀ ≥ c_sΞ proves that Ξ → 0 in probability is necessary for π₀(S₀) → 1 when s₀ + 16 ≤ K. It does not establish the stronger interface P(Ξ > n^{−κ}) → 0 for some positive κ; arbitrarily slow convergence is not excluded by that lower bound. The binding-map bullet also omits the feasibility qualification. Required replacement of the necessity clause in row 18: “(AGG-b): when s₀ + 16 ≤ K, π₀(S₀) → 1 forces Ξ → 0 in probability; this does not by itself force the polynomial-rate interface [VIS(κ)]. (C2)(ii) treats D = {j}, N = ∅.” Replace the opening of the bullet at lines 30–31 by “Ξ → 0 in probability is necessary for concentration when s₀ + 16 ≤ K, by o₀ ≥ c_sΞ; the one-truth failure threshold is given by (C2)(ii) on the actual partition and (N3) partition-free.” This overstatement was already present in HEAD's map; the rewrite should clarify it rather than perpetuate it. No underlying statement or proof changes are required.

No CRITICAL or MAJOR finding. No substantive change to the reviewed theorem/proof content was found. The two required wording repairs above prevent an unqualified EDITORIAL ONLY verdict.

Per-change table

Paths and line numbers below are relative to Theory_work/Wave3/W3-START unless stated otherwise. The full filtered HEAD diff has six modified content files and INPUTS.txt, no other tracked differences, and no untracked content files in scope. All differences are covered by the seven intended items in the brief.

| Difference (working-tree location) | Classification | Reason |
|---|---|---|
| STATEMENT.md:4, v1.3.3 → v1.3.4 | editorial | Version metadata. |
| STATEMENT.md:29, “for some constant C” | editorial | Makes the existing existential constant explicit; T3(b) already states it. |
| STATEMENT.md:46–47, replace main/fe9a066 wording by CORE as of 72785fe, retaining d6da494 comparison | editorial | The referenced CORE contents are identical; no code pin changes in meaning. |
| STATEMENT.md:65–68, explicitly allow A > 0 as well as s₀ ≥ 0 and describe GROW's restrictions | editorial | These are already the local setting and proof scope; no extension beyond the reviewed content. |
| STATEMENT.md:317, repeat κ_V > ½ in N1 | editorial | Restores the qualification already explicit in F2 and L7.3/L6.2(v); no new hypothesis for those results. |
| lemmas/L3_LEAK.md:53–55, display e^{2κ_E+ς_n} before the existing e^{2κ_E+1}, add explanation | editorial | The unchanged proof already establishes the smaller constant, with ς_n ≤ 1. |
| REPORT.md:3,176, version references | editorial | Metadata only. |
| REPORT.md:27, “for some constant C” | editorial | Accurate existential reading of T3(b), including absorption of fixed s₀ + 1. |
| REPORT.md:138, map reference §5 → §2 | editorial | Follows relocation of the sufficiency/necessity discussion. |
| numerics/RESULTS.md:94–96, replace “(AL) tracks the truth” by observed block-relative leading functional tracking T₁ | editorial | Correctly identifies what pred computes and limits the claim to these runs. |
| numerics/RESULTS.md:130–132, replace convergence/monotonicity language by observations and an asymptotic-bound caveat | editorial, repair required | The C_L = 1 observation and theorem caveat are accurate; C_L = 2 wording needs finding 1. |
| citecheck.py:14–18, usage and sys import | editorial (checking infrastructure) | Documents and supports output destination selection; no citation algorithm changes. |
| citecheck.py:66–69, optional argv output path, directory creation and write target | editorial (checking infrastructure) | Only the report destination changes; the default remains reviews/CITECHECK.txt. |
| reviews/INPUTS.txt:1–3, header/comment updates | editorial | Describes proofs rather than planned proofs and explains the exclusion rule. |
| reviews/INPUTS.txt:10 onward, delete PROGRAM, PROTOCOL, LIFECYCLE, template, registry; relabel premise-source section | editorial | Removes administrative context rather than mathematical premises; all 18 code/source/consumer entries remain. |
| ASSUMPTION_MAP.md:1–6, title, target version, claim-id reference, add lemma numerics, final-map framing | editorial | Replaces historical framing by final-statement framing. |
| ASSUMPTION_MAP.md:10, column headings | editorial | Removes provisional “so far”/“early” language. |
| ASSUMPTION_MAP.md:12, energy row | editorial | Locates energy use at TK-b and replaces a premature removability suggestion by the actual toolkit limitation. |
| ASSUMPTION_MAP.md:13, p-growth row | editorial | Corrects event bookkeeping and cites actual-partition diagnostics, incorporating the old corrections. |
| ASSUMPTION_MAP.md:14, fixed-s₀ row | editorial | Replaces early numerical details by final constants and O3. |
| ASSUMPTION_MAP.md:15, p > s₀ row | editorial | Identifies the null-column/ratio requirement and final claim locations. |
| ASSUMPTION_MAP.md:16, FL → GF row | editorial | Integrates HEAD's appended GF-16 correction, including near-twins being inside the revised floor. |
| ASSUMPTION_MAP.md:17, V-c row | editorial | Uses the final proof mechanism and the verified F-2 example rather than provisional numerical evidence alone. |
| ASSUMPTION_MAP.md:18, V-m row | editorial, repair required | Accurately locates the two RSS comparisons; inherited necessity shorthand needs finding 2. |
| ASSUMPTION_MAP.md:19, AL row | editorial | Integrates the old correction: T₁ → 0 is necessary, the specific functional only sufficient for this route; F4 handles bounded isolated leakers. |
| ASSUMPTION_MAP.md:20, Gaussian-noise row | editorial | Updates mechanism/property labels to include TK. |
| ASSUMPTION_MAP.md:21–22, split random-design floor and visibility rows | editorial | Separates L9.1/L9.5 floor uses from L9.2 visibility. |
| ASSUMPTION_MAP.md:23, random leakage/gain row | editorial | Locates the bounded shift and records the previously appended C_L = 0 tightness qualification. |
| ASSUMPTION_MAP.md:24, localisation row | editorial | States the proved o(1/√log n) perturbation and reference-family count. |
| ASSUMPTION_MAP.md:25–26, block and exact-arithmetic rows | editorial | Updates AGG naming, hypothesis prefix and wording only. |
| ASSUMPTION_MAP.md:28–37, binding map | editorial, repair required | Integrates corrected AL and N2 readings; visibility bullet needs finding 2. |
| ASSUMPTION_MAP.md:39–46, level/rate/scope | editorial | Incorporates the zero-gain versus Q = S₀ distinction and the existing transfer scope. |
| ASSUMPTION_MAP.md:48–51, unharvested conclusions, add 1 − 1/F | editorial | Retains prior items and records the inequality already proved in L1.2/L1.6. |
| ASSUMPTION_MAP.md:53–61, consolidated numerical limitations and section index | editorial | Preserves the appended block-relative/partition-free caveat and separates lemma falsification evidence. |
| ASSUMPTION_MAP.md:63–69, relocated literature paragraph; PENDING until CP3 → open | editorial | Comparison text is retained; gate wording is administrative, not a changed proof premise or new literature claim. |
| ASSUMPTION_MAP.md:71–73, final open-item list; remove the three historical correction sections | editorial | Integrates their mathematical corrections into the body; O1–O3 are unchanged. |

Checks performed

* Frozen content: the permitted manifest verifier returned “verify: OK MANIFEST e6d594199cb7f0c527c091cfdb5785ec155ba7b5dc17ecaa88debfee9e19415c”.
* Completeness: read the full filtered git diff against HEAD, including INPUTS.txt; checked name/status and scoped untracked-file enumeration. No additional in-scope change was found. The large map rewrite is item 3, not a hidden theorem edit.
* N1: F2 already requires η′ = 0 and κ_V > ½ for exact order. L6.2(v) chooses κ between ½ and κ_V; L7.3 repeats the same condition. Thus the edited N1 is the accurate summary of the unchanged claim and proof.
* Setting F: GROW STATEMENT.md:51–64 explicitly has s₀ ≥ 1 and A ≥ 1. The local statement already has s₀ ≥ 0 and A > 0. Checked the local L1–L11 proof text: no A ≥ 1 requirement is used. The toolkit does not use s₀; L3 explicitly handles s₀ = 0; visibility is then trivial; L5 uses max(s₀,1) and the sure event for empty truth. Positive s₀ in F2, Gaussian rows, and particular examples remains an explicit restriction of those claims, not a restriction of all Setting F results.
* Code pin: git log -1 -- Scripts/SMC_BVS/core returned 72785fe8f3e7983369a5beacb4a3042513641494. CORE diffs from 72785fe to HEAD and from HEAD to the working tree were empty; the comparison with branch base d6da494 was also empty. Read the cited preprocessing, prior/score, partition, table and convolution ranges: they continue to describe the cited implementation. There is no formula, branch or line-pin change in this round.
* L3.3: write v = (δ + σZ)²/(2τ²_T). The unchanged proof gives v ≤ g_n/2 and ν log(RSS_T/RSS_{T∪l}) ≤ (1 + ϑ̄_n)(1 + x̄_n)v ≤ v + ς_n. Its definitions give ς_n = O(n^{−1/3}log n) → 0, and n₂ ensures ς_n ≤ 1 and x̄_n ≤ ½. The new display follows directly. L3.4 still uses c_L = 2^{15}e^{2κ_E+1}; the constants and Markov bounds in L5.2 and L10.2 are unchanged.
* Assumption map: checked the rewritten rows against TK, leakage, visibility, assembly, corollaries, NEC, transfer, Gaussian-row and interface proofs and the numerical reports. The corrected AL necessity reading is supported; N2 remains empty for s₀ ≤ 15 because V = S₀ forces δ = 0. Zero gains give the stated upper bound on the leading functional via J3. The 1 − 1/F addition is already proved. Numerical scripts compute Lb0/pred on the actual partition; they do not compute the all-conditioning-set maximum of AL. The η = 0 satellite design has fixed nonzero unconditional signal gain in its satellites, so it is outside partition-free AL despite its good block-relative behaviour. Finding 2 is the remaining visibility-necessity imprecision.
* Map omissions: historical notes on “consumed: none”, quantitative TK, design-measurable transfer targets, verified versus expected examples, and proved OVL with uniformly bounded levels are no longer separately repeated as amendment bullets. These statements remain explicit in STATEMENT.md/REPORT.md and the unchanged proofs. Their removal from this assumption index does not remove or reverse a hypothesis, claim, proof step or premise. In particular the scope phrase “through the transfer” does not authorise response-selected targets. The correct mathematical content of the old correction sections is otherwise integrated, rather than discarded.
* REPORT wording: the changed Gaussian-row summary follows L9.7/T3(b); absorb fixed s₀ + 1 into a slightly larger constant C for large n. The map cross-reference resolves to the correct discussion.
* Numerical wording: checked the changed sentences against the displayed tables, summary.csv, and the definition of pred in start_common.R. The block-relative wording is accurate. C_L = 1 has increasing observed mass. Finding 1 identifies the remaining inaccurate C_L = 2 observation.
* External inputs: INPUTS.txt retains six CORE files and twelve argument-source/consumer/limit statement or proof files. It covers the direct pins, GROW/GEN argument sources, RM sources, SAMP's consumer statement, MIS reduction sources, PXN limit statement and T22 predecessor. No remaining entry is a wave administrative document or registry table. Protocol rule 15 expressly excludes the five removed administrative entries. Context and literature mentions are not newly consumed proof premises.
* Citations: ran python -B Theory_work/Wave3/W3-START/citecheck.py with its output in the system temporary directory, outside the repository. Count line: “W3-START CITECHECK: 203 citations (53 with line ranges, 150 path-only); MISSING/OUT-OF-RANGE: 0”. The checker only checks existence for the mentioned LOG/review paths; their contents were not read.

Not checked

This is a diff review, not a fresh independent acceptance of every unchanged theorem. Did not rerun the R simulations, compile CORE, verify binary64 behaviour, independently check the cited literature or its gate status, inspect registry acceptance history, or inspect excluded review/log/checkpoint content. The literary comparison is unchanged; its external source is outside the permitted read set. Mechanical citation success is not an assertion that every unchanged citation is semantically sufficient. No git state was changed, no subagents were started, and the only repository file written by this review is this file (the explicitly requested citation output was written outside the repository).

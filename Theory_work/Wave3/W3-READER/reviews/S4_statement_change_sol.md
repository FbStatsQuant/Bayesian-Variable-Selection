Integrity: PASS — all 26 entries of `S4_frozen/MANIFEST_S4.txt` verified before review. Reviewed on `theory/W3-READER`, HEAD `c219065b5bdd680c50109927c9e536776c610f37`. The supplied READER_VERSIONS/R3/R4 patches reconstruct their frozen targets in memory; the other nonempty diffs agree with regenerated diffs. R1, R2 and STATEMENT have empty S3→S4 diffs. No scratch, subagents, git mutations or writes other than this review file.

Fresh independent Sol statement-change review, one pass. References below are relative to `reviews/S4_frozen/` unless a source is explicitly named. Reviewed the S2/S3 reports and dispositions, all S4 diffs, the complete changed statements, both Song–Liang check notes, and the proposal and its A/B application diffs. The three swap sources were read and verified byte-identical to their specified pins: PSHARP-R `8e22c756`, MISR-R `93e50640`, SCR-R2 `048b6b23`. Registry comparisons used HEAD and the expressly quoted commits `f526e45b`, `33e1f0f5`, `2b54cb3c`, `d2b600ba`. The published local PDF was independently spot-checked at journal pp. 955–957 for card rows 1.1 and 1.4, including Condition 3, Theorem 3, (17)–(18), Condition 4 and Corollary 2.

## Findings and repairs

### S1 [S] — Remaining unqualified delivery assertion in Theorem 10

**Location:** `READER_VERSIONS.md:1038–1039`.

“Under the delivery conventions (S4) runs always complete” survives the FUNI-N narrowing. (S4)(v) describes two alternatives; it does not impose IDEAL-W⁺ on every invocation of (S4). Thus this sentence still leaves unrestricted delivery under the original machine conventions apparently available, although neither a domain restriction nor the added plus assumption is stated. The revised R4 remark at `lemmas/R4_printed_outputs.md:46–47` supplies the distinction correctly. Saying the link is unused does not make the assertion faithful.

**Repair:** replace the parenthesis by “under (S4)(i)–(iv), completion holds on 𝔇; under those conventions and A:IDEAL-W⁺ it holds for every admissible n; that link is not used here.” This is WEAKER, following F-UNI's narrowed clauses (a)/(b), `FUNI_NARROW/L5_delivery_F-UNI_v2.patch:15–21` in the target numbering, and its appended remark. The main delivery clauses of Theorems 6–7, the R3 target/assembly, NOTATION and REPORT otherwise preserve this distinction. The pending F-UNI `2.1.0` requotation is expected and is not a finding.

### C1 [C, S] — Changed card row 2.2 still confuses distance with squared distance and omits its mathematical premises

**Location:** `CLAIMS_CARD.md:52`.

The result cell retains “Hellinger contraction … rate M_n/√n with selection, log n/n without beta-min.” The second rate is for **squared** average Hellinger distance. The distance radius is of order √(log n/n). Also, “without beta-min” alone is not the premise of D(b): it needs R1, G, (E), (F₀), (OS). D(a) needs R1, G, (E), (F₀) and posterior selection in probability. The newly quoted checked status does not supply these hypotheses. This defect predates S4 in the result cell, but remains in the row whose status/comparison S4 changes; it is already correctly repaired in the separate, unapplied proposal.

**Source:** `W3-POST2/STATEMENT.md:103–115`, especially :107–111 and :112–115. **Repair:** use the proposal's row 2.2 at `proposal/DELTA_row21_thm9_DIST.md:303` (the row beginning “Body remark”), retaining fallback/body placement as appropriate to the unapplied DIST swap. Explicitly distinguish h̄_n from h̄_n², state the premises and probability mode. Restoring (OS), (E) and (F₀) weakens the overbroad literal paraphrase to the master's scope; correcting the metric does not change the master.

### F1 [F] — Status refresh is incomplete and some condition lists are still elided

**Locations:** `CLAIMS_CARD.md:45, 125–128`; `lemmas/R4_printed_outputs.md:11, 23–24`; related `READER_VERSIONS.md:715, 1064`; `REPORT.md:38, 46`.

- Card 1.4 quotes both CorH-plus and CorH-U as “PROVED-CHECKED, conditional on W3-POST2:D, …”. The permitted council-suffix abbreviation must not swallow conditions. CorH-plus also requires SOP:TH09 and SOP:TH128. CorH-U additionally requires POST2:C, POST2:A0 and C-MIS:Prop-P, and its (G) clause additionally POST2:E, POST2:A1 and C-MIS:GDb (with the SOP inputs retained). Its POST2 input quote also replaces the entire condition list by “…”. The complete correct quotations already appear at `READER_VERSIONS.md:508–513` and :190–193.
- R4's new header correctly quotes C@1.1.3 and APP@1.0.6, each conditional on SOP:TH09, but its operative “Inputs (statuses verbatim, registry)” list still gives C@1.1.1 as unconditionally checked and APP@1.0.1 as unchecked. Neither is labelled a historical quotation at a specified commit. Update that list to agree with the header and HEAD/33e1f0f5; update the R4 REPORT dependency pins too. Likewise update REPORT's RM2-R/F pins to 1.0.2. Preserve the explicit deferred F-UNI pin/requotation arrangement.
- B6.5 still calls B2.2 EXISTS-UNCHECKED after B2.2 was refreshed to EXISTS-CHECKED, conditional. This understates rather than inflates its status, but is contradictory.
- “The single remaining root is T03♯” at card :127 is true of the selected abstract route, not of the whole card. POST2:C still explicitly lists Prop-LB, [L1a′], SOP:TH128 and other inputs; MISR retains its additional conditions. The last column of the bridge summary at RV :1064 also over-compresses these to W3-T03ACC, despite the accurate “and others” in its mark.

**Repair:** carry each full conditional prefix, abbreviate only the subsequent council evidence, scope the “single root” sentence to abstract rows 1.1 in O_P form, 1.2 and 3.1, and synchronize the input/dependency lists. These are EQUAL mathematical changes. This does not find a defect in the actual refreshed POST2, APP, SAMP, PSHARP-R, MISR-R or SCR registry quotations at the main theorem-source paragraphs: those match the stated commits.

### S2 [S] — The new comparison sentence drops the retained off-truth floor

**Location:** `CLAIMS_CARD.md:42`, “Buys vs the literature” cell.

“Thm 1′ replaces eigenvalue floors off the truth by a residual-signal identifiability margin” is unqualified. It conflicts with the same row's correct result cell and the newly added H5-7 explanation: (A5) remains an eigenvalue condition on O(log n)-sets, including null-only sets and duplicated null columns. The Song–Liang check note expressly assessed the SL content only; it does not validate this description of our theorem.

**Repair:** “Thm 1′ replaces the bounded-size floor (A4) off the truth and beta-min by an identifiability margin, while retaining the vanishing floor (A5).” The source is `READER_VERSIONS.md:125–140, 238–243` and POST2:E `STATEMENT.md:126–133` with the reader's stronger retained (A5). This restores a master/reader premise and is WEAKER as a literal comparison claim. The corrected Song–Liang assertions themselves pass: Theorem 3 is screening, Condition 3 is population identifiability, and the exponential dimension specialization comes through Corollary 1/(10).

### F2 [F] — Certification count is promoted to an unsupported count of small models

**Location:** `READER_VERSIONS.md:920–922`.

“Certified a small reported model in every completed run: 2,394 of 2,394” is not supported by the cited SCR-R2 evidence table. At the specified pin, `W3-SCR-R2/reviews/READER_DELTA.md` §5 says the production study has **no per-fit size**, and documents a ≤28 size bound for **2,194**, not all 2,394, fits. It establishes certification for all completed fits. The same source's proposed narrative overstates its own evidence; verbatim copying that narrative does not establish the stronger empirical assertion. The 376/376 and 71/71 small-model statements have separate size evidence in that table, and the 61/122, 18/20, 30/30 containment counts match the supplied source.

**Repair:** say “certified the reported model in every completed run” for the three certification counts, then state smallness separately only where size evidence exists, with a defined cutoff. Do not infer individual sizes from means. WEAKER: restores the scope of the cited measurements. Omitting the delta's sample-size-threshold sentence follows the owner's rule and is not a finding.

### E1 [E] — Superseded abstract instructions and stale source spans

**Locations:** `CLAIMS_CARD.md:100, 104`; `REPORT.md:34`; `READER_VERSIONS.md:70`.

The card's old abstract bullet still says “expectation form once POST2 is recorded”; the immediately preceding, newer HQ decision expressly keeps that form and Theorem 1′ in the body, even after recording. Likewise the omitted-variables bullet says its conditionality lasts only until recording; the recorded masters still have conditions. **Repair:** delete the old expectation-promotion instruction; state the O_P Form A/B choice consistently; retain row 1.4's actual conditional inputs until discharged, rather than until recorded.

REPORT still identifies R3's statement as `:1–47`; the revised assembly finishes at :49 and the file at :54. **Repair:** extend the cited span through the complete assembly, or through :54. R4's :1–44 span covers its claim/proof; its added delivery remark is outside that span and should be separately cited if used. The START source pointer “N1:73” at RV :70 should be :75 in the current source (the quoted candidate status is correct). These are EQUAL editorial repairs.

### S3 [S] — Swap tags need an explicit baseline and separate new consequences

**Locations:** `READER_VERSIONS.md:430–435, 551–554`; `CLAIMS_CARD.md:4`; detailed table below.

Theorem 3's “STRONGER: new expectation display …; EQUAL elsewhere” is not correct if “elsewhere” is compared with S3: the growing-s₀ expectation obstruction and the e^{-λ} critical-scale bound are also new stronger conclusions. Theorem 4's overall STRONGER tag is correct, but “same conclusion” describes only its main two-display result; the Hellinger/KL and uniform-selection remarks are newly stated conclusions. For card 3.7, EQUAL is appropriate **to the SCR-R2 delta**, while its replacement of an apparent recovery/screening probability claim by an intersection-event bound is WEAKER **relative to S3**.

**Repair:** either tag these individual statements against S3 as in the table, or explicitly declare a delta-relative baseline for every clause of a swap and record its S3 strength change separately. Do not mix the baselines inside an unqualified “EQUAL elsewhere.” All three swaps' mathematical text remains faithful to the supplied deltas, subject to F2's empirical evidence issue. The WEAKER card 3.7 reading restores SCR-A `STATEMENT.md:80–89` and A1 :158–163.

## Statement-change tag table

E = EQUAL, W = WEAKER, S = STRONGER. Default comparison is S3-frozen. For a direct swap, “E/Δ” means EQUAL to the named delta, the alternative baseline allowed by the brief; the S3 comparison is given as well. “New” in a lead-tag cell is a description, not a substitute strength tag. Rows about statuses/placements are E mathematically even where a factual/editorial repair is needed. Unchanged R1, R2, STATEMENT, Theorem 5 and unchanged mathematical clauses are not reclassified as new statements.

| Location / changed statement | Lead's tag | Reviewer's tag and source |
|---|---|---|
| RV :46–49, (S4)(v), delivery on 𝔇 | W | W; F-UNI narrowed (a), 𝔇 sufficient only |
| RV :49–60, every-n delivery with IDEAL-W⁺ | W | W; F-UNI narrowed (b), frozen A_IDEALW_PLUS definition |
| RV :64, final streams independent of data | W (thm10 log) | W; restores SAMP :39–41 / N1 joint-law premise |
| RV :70–71, START/KERNEL statuses separated | E | E; N1 :75–78 |
| RV :149–153, rate witness/open-expectation scope | E | E; S3-N4/N5, PSHARP A/B and PSHARP-R AE |
| RV :238–243, retained A5 and O1/O3 explanation | E | E; no displayed theorem change; A5 and POST2 E retained |
| RV :190–196, POST2 conditional status refresh | E | E; registry f526e45b |
| RV :198–204, Form A O_P route; expectation/1′ body | E | E; selects existing clauses, conditions retained |
| RV :205–214, B1 conditional abstract and B2 disposition | E | E; existing theorem under disclosed shared input |
| RV :225, B1.7 checked-conditional label | E | E; A0@1.0.4 conditional on SOP:TH09 |
| RV :297–309, Theorem 2 master/bridge statuses | E | E; APP@1.0.6, 33e1f0f5 |
| RV :336–348, p→∞ retained only for in-probability display | S / E elsewhere | E for original probability claim; E/Δ for full swap |
| RV :342–345, every-p expectation lower bound | S | S vs S3; E/Δ; AE :74–84 |
| RV :351–354, expectation headline | S | S vs S3; E/Δ; AE plus B3.5/B3.8 |
| RV :357–361, old size-domain and probability consequences | E elsewhere | E; original PSHARP B/A, domain retained |
| RV :363–366, fully orthogonal every-p expectation exactness | E elsewhere | S vs S3; E/Δ; AE + B3.8 + conditional Theorem 1 |
| RV :367–368, named probability exactness cases | E elsewhere | E; original witnesses, E/Δ |
| RV :370–371, bounded-p rare-gain mechanism | E elsewhere | E/Δ; explanation of AE proof, no extra theorem |
| RV :373–376, growing-s₀ expectation obstruction | E elsewhere | S vs S3; E/Δ; AE :86–92 |
| RV :378–380, orthogonal critical-scale e^{-λ} | E elsewhere | S vs S3; E/Δ; A2C :94–100 |
| RV :382–387, open probability/expectation/constant scope | E elsewhere | E/Δ; matches delta and distinguishes unproved upper bounds |
| RV :390–395, truncated-sum mechanism, not maximum | E elsewhere | E/Δ; PSHARP-R delta §3 |
| RV :401–416, AE/A2C statuses and B3.3–B3.8 | S / E elsewhere | E/Δ; bridges support the stronger S3-relative claims above |
| RV :446–451, candidate-only conditional Gaussian A0 | S | S vs S3; E/Δ; CorGb-plus §3 via q=0 |
| RV :453–454, correlation floor, no marginal-variance bound | S | S vs S3; E/Δ; CorGb-plus :96–107 |
| RV :455–462, relative signal and two O-rate conclusions | S overall | E for these formulas (renamed covariance); E/Δ |
| RV :464–472, Gaussian/pseudoinverse/linear-plus-noise examples | S overall | S in the new example scope; E/Δ; CorG-min (E1)/(E2) |
| RV :473–477, centred fitted-law Hellinger/KL rates | S overall, “same conclusion” | S vs S3; E/Δ; CorH-plus (a′)/(KL), CorH-U (G) |
| RV :478–481, fixed-design selection-only/uniform forms | S overall | S vs S3; E/Δ; CorH-U (U-a)/(RD), MIS(i) |
| RV :482–484, Theorem 2 non-implication/open comparison | E presentation | E/Δ; does not claim an unproved implication |
| RV :487–499, contrast-law sufficiency, necessity, invariance | S overall | E/Δ; CorG-min :63–79, delta §3 |
| RV :508–537, new masters/statuses/bridges | S overall / E refresh | E/Δ mathematically; registered conditional prefixes match |
| RV :541–543, scope outside Gaussian-linear contrast law | S overall | E/Δ; scope disclosure, not an added theorem |
| RV :658–662, Theorem 6 delivery | W | W; F-UNI (a)/(b); statistical/common-event clause E |
| RV :783–787, Theorem 7 delivery | W | W; same master narrowing; statistical clauses E |
| RV :664, 789, mandated RM2R-5 sentence | W delivery | E to source §7; explains W delivery without broadening it |
| RV :688–692, RM2/APP status refresh | E | E; RM2-R@1.0.2 and APP@1.0.6 retain conditions |
| RV :701–706, pending F-UNI narrowing/abstract placement | W / E placement | W theorem scope, E metadata; expected requotation pending |
| RV :848–852, Theorem 8 constants fixed in n | E to master | E/Δ and E precision vs S3's “fixed signals”; A1 :158–163 |
| RV :856, certifies = flag; :860, n-varying signals excluded | E | E/Δ; meaning of coded event / fixed-constant scope |
| RV :864–870, abstract includes q_n<K, names c1 | E | E/Δ; explicit master premise, no inference from other premises |
| RV :873–884, new Theorem 8′ | New; E to master | S as addition vs S3; E to A-inf :87–90 |
| RV :888–895, four fixed constants / separate A1° | E | E/Δ; A1 and separate A1° :165–169 |
| RV :900–903, A1/SCR-G checked status | E | E; d2b600ba; SCR-G expressly separate |
| RV :910–917, intersection/certification/one-sided remarks | E | E/Δ; A1, SCR :217–218, SCR-C; theorem event unchanged |
| RV :920–924, certification/containment observations | E | E/Δ narrative, but NOT faithful to size evidence (F2) |
| RV :1005, withdrawal of exact-branch consistency claim | W | W; restores SAMP :186 sampler scope; S3-N3 |
| RV :1014–1016, moderate-n claim about π only | E | E descriptive correction; S3-N9/D-17, no π0 assertion |
| RV :1021–1026, 1031, SAMP/APP status refresh | E | E; C/TR and APP conditional on SOP:TH09 |
| RV :1038–1039, residual completion assertion | implicit E | Requires W repair S1; restore F-UNI domain/plus premise |
| R3 :6–15, narrowed target | W | W; F-UNI (a)/(b), no asymptotic conclusion from bounded 𝔇 |
| R3 :31, IDEAL-W premise row | W | W inference scope; A:IDEAL-W⁺ or 𝔇 now required |
| R3 :45–49, assembly | W | W; F-UNI narrowed statement; common event remains independent of S4 |
| R4 :3–8, per-input status header | E | E; accurate new header, stale list remains F1 |
| R4 :46–49, delivery as an added hypothesis | W | W; restored F-UNI premise; no change to localized C-v assembly |
| REPORT :37, R3 conclusion | W | W; matches narrowed assembly |
| REPORT :50–51, R4 conditionality note | E | E; 33e1f0f5 |
| Card :42, row 1.1 result wording/margin constant | E | E precision via expressly named Thm 1′; no theorem changed |
| Card :42, row 1.1 SL screening/identifiability/dimension | W/precision | E for accurate SL precision; off-truth comparison needs W repair S2 |
| Card :43, row 1.2 status | E | E; APP@1.0.6 conditional |
| Card :44, row 1.3 expectation result | S | S vs S3; E/Δ; probability clause's p→∞ explicit |
| Card :44, row 1.3 witness/open-item comparison | W / E precision | E vs S3's existing witness restriction; historical W vs pre-restriction text retained |
| Card :45, row 1.4 conditional-Gaussian result | S | S vs S3; E/Δ; correlation floor and candidate law |
| Card :45, row 1.4 SL comparison | W/precision | E for corrected SL attribution; no transfer of their moment-only setting to our theorem |
| Card :52, row 2.2 status/comparison | E / W precision | E for accurate comparison/status; retained result needs C1 repair |
| Card :58–59, rows 3.1/3.2 delivery | W | W; narrowed F-UNI, row 3.2 refers to same conclusion |
| Card :58, row 3.1 SL selection-output comparison | W/precision | E precision; SL p.959 computational discussion, no selection-output theorem |
| Card :58, row 3.1 APP conditionality | E | E; shared abstract input only, not full-card dependency collapse |
| Card :63, row 3.6 status and body placement | E | E; C/TR/LT#/D all conditional on SOP:TH09; unchanged result localization |
| Card :64, row 3.7 intersection and fixed-constant scope | E (swap) | E/Δ; W vs literal S3 card, restores SCR-A/A1 premises/event |
| Card :64, row 3.7 no-visibility comparison | E | E/Δ; assumptions can hold, no finite-run success assertion |
| Card :87–98, Form A/B and common-data-event abstract | E | E; no new seed/calibration quantifier; body delivery narrowed |
| Card :101–103, abstract Theorem 1′ wording | E | E; accurately retains A5 |
| Card :109–110, row 3.6 moved to body | E | E placement |
| Card :114–120, O1/O3/O2/rider descriptions | E | E; no unproved strengthening asserted |
| Card :137–140, D-17 source annotation | E | E descriptive content; provenance qualification below |
| NOTATION :145–149, bounded/plus delivery distinction | W | W guarantee scope; F-UNI and A_IDEALW_PLUS |
| METHOD_INTUITION :69–72, no-imitator vs growing-set exponents | E | E descriptive repair; START2 T3⁺ and Theorem 5 |

Historical tags added for S2 repairs are consistent with S3's adopted convention: added operational premises weaken Theorems 6–7's delivery clauses; restored N1 premises and sampler scope weaken Theorem 10; restored standardised-signal/localized scope weakens card 3.6. They are not new S4 mathematical changes. The old “STRONGER convention list” log entries should be read as historical descriptions of hypotheses, not as the current statement-strength tag.

## D71 inventory: changed interpretive sentences

Each entry identifies the sentence(s), judges the actual assertion, and names the source. Adjacent sentences with the same source are itemized within one row; source/status tables and administrative changelog sentences are audited above rather than treated as paper interpretation. Unchanged S3 prose is not silently re-reviewed as new. “NOT” means NOT-FAITHFUL as written, including an unsupported empirical qualifier.

| Location and interpretive sentence(s) | Judgment / source |
|---|---|
| RV :46–52: two fixed cap rejections; bounded-domain delivery; every-n only with plus; other validators/fallback/caps retained; plain IDEAL-W insufficient; operational assumptions not statistical deductions | FAITHFUL — frozen A_IDEALW_PLUS :9–10, F-UNI narrowing and FUNI_NARROW/DIFF_sol |
| RV :57–60: 𝔇 sufficient rather than necessary; pending narrowed F-UNI version | FAITHFUL — same definition/patch; no recorded acceptance claimed |
| RV :149–153: witness attainment; unknown other-design factor; expectation lower-bound open item; probability factor when log p≈log n | FAITHFUL — PSHARP A/B, PSHARP-R AE, S3-N4/N5; “on other designs not known” describes general scope, not a prohibition on further examples |
| RV :198–204: Form A uses existing O_P theorem; expectation/1′ have additional body conditions | FAITHFUL — registry POST/POST2/APP prefixes and the explicit distinction between the routes |
| RV :205–214: shared conditional sentence; same/different-family verification; conditional presentation avoids removing the three shared-input rows | FAITHFUL — POST/TH09/APP/RM2 status chain; presentation, not an additional mathematical assertion |
| RV :238–243: A5 excludes exact dependence/duplicated nulls; design-agnostic description forbidden; OS without eigenvalue conditions open | FAITHFUL — A5, POST2 E/A0/A1, H5-7; no design-free theorem asserted |
| RV :351–354: rate cannot improve in expectation on named null-column witnesses, every p; c's sparsity dependence; only n^{-1/2} universally proved | FAITHFUL — AE :74–84, B3.5/B3.8, PSHARP B; not every-design sharpness |
| RV :357–359: universal probability/sparsity consequences under the size domain; counterexample without that domain | FAITHFUL — PSHARP B; domain preserved |
| RV :359–366: expectation factor for every p, polynomial-p constant, probability factor when log p≈log n, fully orthogonal expectation exactness | FAITHFUL — AE :76–84 and checked B3.8; upper bound remains conditional on Theorem 1 |
| RV :367–368: two named in-probability exactness sequences | FAITHFUL — original PSHARP witness statements plus Theorems 1/2; not a Gaussian expectation upper bound |
| RV :370–371: bounded-p factor arises from rare large single-variable gains | FAITHFUL — PSHARP-R delta §3 and AE mechanism |
| RV :373–376: growing-sparsity expectation rate forces bounded s0 | FAITHFUL — AE :86–92, under the stated retained witness/energy/coefficient conditions |
| RV :378–380: critical-scale orthogonal posterior upper bound | FAITHFUL — A2C :94–100 |
| RV :382–387: general-design expectation lower bound open; probability statement only gives √(log p/n) at slower p; Gaussian expectation upper bound open; sharp constant unproved | FAITHFUL — PSHARP-R delta §3 / AE/A2C; “nothing claimed” read with its immediately stated weaker probability bound |
| RV :390–395: deterministic prior/Occam mechanism; independent-competitor description; single-gain expectation mechanism; truncated-sum probability mechanism; energy keeps variance on scale; witnesses not necessary hypotheses | FAITHFUL — PSHARP B/A, PSHARP-R delta §3; “behave as” is the witness mechanism, not an exact Gaussian law assertion for spherical finite-n scores |
| RV :459: parameters may vary with n | FAITHFUL — CorGb-plus :99–107, subject to the displayed common-constant/relative-signal conditions |
| RV :464–472: joint-Gaussian omitted-variable example; covariance/pseudoinverse formulas; linear-plus-noise example | FAITHFUL — CorG-min (E1)/(E2); singular example does not waive the theorem's separate correlation floor |
| RV :473–477: conditional law is its own KL projection; best-candidate support; posterior fitted-law contraction with centred mean; Hellinger and KL rates | FAITHFUL — CorH-plus :114–130, CorH-U (G), its centred reference and sets H^a/K^a |
| RV :478–481: selection-only fixed-design contraction; uniformity requires uniform selection/common constants/bounded support; residual-variance-uniform fixed-design version | FAITHFUL — CorH-plus (a′), CorH-U (U-a)/(RD), BASE MIS(i) |
| RV :482–484: Theorem 2 does not establish the broader theorem; reverse coverage not asserted; different conditional masters | FAITHFUL as a non-implication/scope disclosure — MISR-R delta v0.4 §2; no claim that the open comparison is proved |
| RV :487–494: full-vector A0 sufficient; only Gaussian contrast law needed; sample mean unrestricted; omitted-part Gaussian contrast characterization under independent Gaussian noise; examples; candidate law used for transfer | FAITHFUL — CorG-min :63–86 and CorGb-plus proof/§3 |
| RV :496–499: standardisation makes correlations relevant; response invariance/relative variance; energy evidence; fixed-liminf beta-min suffices in master | FAITHFUL — CorGb-plus :99–107, CorG-min/BASE invariance and the source delta's numerical qualification |
| RV :514–517: coexistence/supersession; KL sentence uses centred-reference CorH-plus rather than unrestricted BASE Cor-H | FAITHFUL — MISR-R master §4/§8 and recorded claim states; no unchecked input called checked |
| RV :541–543: no general non-Gaussian conditional response result beyond contrast form | FAITHFUL — CorG-min/CorGb-plus scope |
| RV :664 and :789: RM2R-5 integer-limit explanation and 𝔇/plus alternatives | FAITHFUL — verbatim RM2-R v-next §7, validators and frozen plus definition; authorized exception to the threshold-wording rule |
| RV :690–692: row 3.1's shared remaining posterior condition; distinct extra condition on RM-R special case | FAITHFUL — registry 33e1f0f5; this statement is scoped to that route |
| RV :701–706: every-n versus bounded-domain F-UNI narrowing; requote later; common-event abstract independent of delivery | FAITHFUL — F-UNI narrowing, RM-0(b); deferred recording is explicit |
| RV :856: certification means the reported model's local-optimality flag is set | FAITHFUL — SCR coded event definitions, delta §3 |
| RV :860–862: n-varying constants outside Theorem 8; no start/leakage/block/visibility or polynomial-dimension premise beyond displayed conditions; full floor constrains null correlations | FAITHFUL — SCR A1/directional-floor sufficient case; this does not restrict Theorem 8′ |
| RV :864–870: abstract fixed constants/cap/budget and intersection event; c1 named, formula stays in body | FAITHFUL — SCR A1 and supplied SCR-R2 clause |
| RV :874–883: gain described as quadratic-form decrease; Γ is worst-model best-missing-variable gain; no p/s0/start/null-collinearity restriction | FAITHFUL at statement strength — SCR :54–60, :87–90. Literal master γ is (n+1)/n times that decrease; replacing it by the decrease multiplies Γ by n/(n+1), leaving this strict asymptotic liminf condition equivalent. No finite-n SCR-A margin is asserted for the altered normalization. Naming the factor would improve exact notation |
| RV :888–895: weaker directional floor; fixed constants; A1° separate, different hypotheses; budget from union bound | FAITHFUL — SCR :158–169 and master proof; source delta |
| RV :910–917: intersection rather than conditional guarantee; no promised frequent certification; one-sided rather than exact recovery; SCR-C needs its stronger floor | FAITHFUL — SCR-A/A1, :217–218, SCR-C |
| RV :920–922: every completed run certified **small**, including all 2,394 production fits | NOT — F2; source table establishes all-fit certification but lacks all-fit size evidence |
| RV :922–924: strong-factor/screening certification counts and strong-factor containment counts | FAITHFUL — SCR-R2 delta §5 at 048b6b23, with empirical rather than theorem status |
| RV :1005: exact enumeration outside Theorem 10 | FAITHFUL — SAMP :186; removes S3's mis-cited extension |
| RV :1014–1016: start transports vanishing mass in the theorem's regime; moderate-n mixture now asserted only for posterior π | FAITHFUL — START2 IF-START/C-v, D-17 descriptive context; no new π0 shape theorem |
| RV :1037–1039: event localization and no success-probability lower bound; delivery conventions alone imply always completion | First assertion FAITHFUL — SAMP C-v; last assertion NOT — S1, omitted plus/domain qualifier |
| RV :1040–1041: start rate versus posterior rate and inherited posterior condition | FAITHFUL as rate-order comparison — START2 :176–180, APP/C registry prefixes; no new exact ratio claim |
| Card :42: full-model consistency versus SL screening; MAP in supplement; SL Condition 3; dimension specialization | FAITHFUL SL attribution — PDF pp.954–956, (10), Corollary 1, Theorem 3, Condition 3; supplement itself not independently re-proved here |
| Card :42: Thm 1′ replaces eigenvalue floors off truth | NOT — S2; bounded-size qualifier/A5 omitted |
| Card :44: expectation sharpness on witnesses; only universal n^{-1/2}; scoped open item | FAITHFUL — PSHARP A/B, AE, checked B3.8; conditional upper-bound route retained in body |
| Card :45: SL fixed misspecified subset, second moments, fixed-ε a.s. Hellinger consistency, conditional no-collinearity screening statement | FAITHFUL — independently read PDF pp.956–957, (17)/(18), Condition 4, Corollary 2; no Gaussian attribution to SL remains |
| Card :45: our conditional-Gaussian assumption; exact selection/rate; growing candidates; parameter variation; invariance | FAITHFUL — CorGb-plus/CorG-min and Theorem 4, relative-signal hypotheses by that theorem reference |
| Card :52: fixed-design in-sample counterpart, parity in kind only | FAITHFUL comparison — PDF joint-distance definitions / POST2 D. The unchanged result-cell rate/premises fail C1 |
| Card :58: bounded/plus delivery and RM2R-5 | FAITHFUL — F-UNI narrowing and mandated source sentence |
| Card :58: known-to-us selection-output comparison; SL uses Liang et al.'s SAMC, citing properties, no selection-output theorem | FAITHFUL as an SL comparison — PDF p.959; “known to us” is not treated as an exhaustive literature-search theorem |
| Card :64: no visibility/leakage/start/block requirement; its assumptions can hold where 3.1/3.2's do not | FAITHFUL — SCR-A/A1; no claim that finite numerical examples meet all fixed-constant inequalities |
| Card :87–99: A/B shared-condition abstract; common-data-event first; delivery in body; same ordering for fixed design | FAITHFUL — RM-0(b), RM2 and F-UNI; preserves seed/calibration quantifiers |
| Card :100–104: expectation promoted once recorded; 1′ retains A5; MISR condition only until recorded | Floor sentence FAITHFUL; promotion/discharge instructions NOT current — E1 |
| Card :109–120: printed-output row in body; O1/O3 ranking and open OS condition; O2 explicit/not optimized; named rider aspirations | FAITHFUL — existing theorem hypotheses and H5-7 instructions; no open strengthening presented as proved |
| Card :125–128: registry refresh; single remaining root for the full card | Refresh prefixes FAITHFUL where fully stated; unrestricted single-root gloss NOT — F1 |
| Card :137–140: moderate-n posterior/store-law mixture, individually light supersets collectively substantial; not a point mass | FAITHFUL as an empirical description — D-17 in the supplied repository's main-workspace file on disk, :83. Provenance precision: `git show f237bfa3:Docs/Experiments/P1M/DECISIONS.md` does not resolve; neither does local `main` for that path. Thus “on main at f237bfa3 or later” is not independently verified as a committed-file pin; cite the actual evidence file/revision if a reproducible git pin is intended |
| NOTATION :145–149: bounded-domain / plus-only every-n delivery, operational rather than statistical | FAITHFUL — narrowed F-UNI, frozen plus definition |
| METHOD_INTUITION :69–72: no imitators gives exponent c<1/2; set of size n^{1/2−ε} gives c<ε on intervening lattice | FAITHFUL in Theorem 5's stated setting — START2 T3⁺/IF-START and reader Theorem 5; “puts mass” is the theorem's high-probability concentration description, not a deterministic finite-n equality |
| R3 :6–15, :31, :45–49: plain IDEAL-W does not remove cap guards; plus/domain is a hypothesis; narrowed delivery assembly; common event needs no S4 | FAITHFUL — F-UNI patch/DIFF_sol, A_IDEALW_PLUS, RM-0(b) |
| R4 :3–8: assembly, no new probability, individual statuses, potential versus printed scope | FAITHFUL new header — registry and SAMP PC/C-v; stale detailed list separately fails F1 |
| R4 :46–49: plus/domain completion only as an added hypothesis, not used in localized proof; posterior-PIP comparison only by triangle inequality | FAITHFUL — F-UNI narrowing and Theorem 2/C-v |
| REPORT :37, :50–51: bounded/plus R3 implication and inherited R4 conditionality | FAITHFUL conclusions — R3/R4 and registry; stale pins/span require F1/E1 |

House-rule check: no new asymptotic statement is presented as a limitation merely because it is asymptotic. No new “huge constants” or onset-size warning is added. The RM2R-5 sentence is the expressly mandated code-limit exception. The SCR delta's numerical sample-size threshold was omitted as instructed. “Explicit constant, not optimised” is retained. Interpretive/provenance defects above must be repaired even when they occur outside a display.

## Card-13 proposal: fidelity only, not applied

FAITHFUL to DIST `STATEMENT.md` v1.4.10 §1R and its cited interfaces, with prospective A/B statuses explicitly subject to requotation on application. Both application diffs carry the same mathematics; their differences are precisely the proposed discharge/retention of the T01 input and consequent status blocks. Neither was applied.

- The sample-mean intercept, true x-marginal and averaged conditional Hellinger identity at proposal :89–100 preserve DIST :140–159 and §0 :42–52. The √2 normalization difference from SL is stated.
- The raw/retained predictor renaming, q_n(M), (A1)–(A5), constants, fixed-level (i), n≥n0 and M≤√n/log n, subsequent uniform level-M form, (ii), shared exceptional event and (iii) match master :164–202. The card now states q_n(M); its abstract uses the fixed-level specialization, rather than claiming all levels under a fixed logarithmic window.
- Without (A4), the radius gains √log(p_raw∨n) and the size threshold becomes s+C1 M log n. B9.5 remains VERIFIED: nε_n²/log(p_raw∨n)=M log n. Both inner and outer probabilities have the preserved exponent.
- 9B retains the M=1 window, exactly s≥1, floor, positive divergent beta-min envelope, every M_n→∞ and convergence in data probability (master :209–215). 9C retains exact arithmetic, completed-sampler scope, the list-mass premise, every-run quantifier, reconstructed restricted posterior, and the absence of discovery/completion/list-mass certification guarantees (master :217–238). The code-checked sentence concerns the computational output description, not a floating-point or list-mass certificate.
- The F9/F9c/F9d repairs are present: squared versus unsquared row 2.2, its premises, M-dependent window, weaker fallback size bound, both fixed-interface sparsity qualifiers, and repaired control characters. Both A/B diffs have no nonprinting controls/tabs. Interface energy/cost held fixed is essential: the reader (A5) bounds grow with s, so neither an s-independent reader constant nor a growing-s theorem is inferred.
- New/changed D71 proposal sentences at :89–100 (“what is estimated”), :102–106 (level/window), :124–125 (no beta-min/fixed floor), :134–151 (rate/size/uniformity/fallback), :161–179 (sampler description and conditional guarantee), :181–194 (examples and fixed-level placement), :198–227 (SL comparison, two interface-form qualifications and incomparable scope), :231–246 (why-lines) and :271–274 (limits) are FAITHFUL to DIST §0/§1R/bridges/TARGET §6 and the PDF checks. The six HQ edits and all earlier fidelity repairs remain implemented.

The unapplied proposal's correct row 2.2 does not repair the applied card by implication. Its anticipated statuses are not accepted here as current registry quotations, and its output-description check is not promoted to a theorem guaranteeing adequate sampled mass.

Main findings: remaining unqualified completion assertion; card 2.2 distance/premise defect; truncated/stale conditional statuses; off-truth-floor comparison; unsupported all-fit smallness; stale abstract instructions/source span; inconsistent S3-versus-delta tag baseline. The core swapped theorem displays and the card-13 proposal otherwise preserve their sources.

TAGS: CORRECTED (Theorem 3 new expectation-exactness, growing-s₀ and critical-scale consequences are STRONGER vs S3; card 3.7 localization is WEAKER vs S3, EQUAL to its delta; declare swap baselines explicitly)
FIDELITY (applied text): NOT-FAITHFUL
FIDELITY (card-13 proposal): FAITHFUL
OMITTED-PREMISE: A:IDEAL-W⁺ or 𝔇 in Theorem 10's completion remark; retained (A5) in card 1.1's comparison; R1/G/(E)/(F₀) and selection or (OS) in applied card 2.2; elided conditional-input lists in card 1.4
VERDICT: FIXES-NEEDED

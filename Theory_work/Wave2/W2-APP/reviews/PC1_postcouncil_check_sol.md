# W2-APP — PC1 post-council check, Sol

Manifest reviewed: `72ac86f9fd0ca9fef850562ca9680d328de7dcef451c907bb693b925a2b31460` (126 files). I verified the stored header, file inventory and content hashes using `manifest.py`'s read-only `verify_problems` function, supplying the repository root explicitly so that no git command was run: **zero differences**. I read both C3 reviews, their disposition, the current STATEMENT/REPORT/EMPIRICAL, all six lemma files and LEAD_READING, and the FAC-A source material identified below. Only this review file was written; no git operations or subagents were used.

**Answer to the brief's main question: mathematical content did change after C3.** The FAC-A addition changes the applicability map's positive coverage outside enumeration. It is not merely transcription of a status label. Some requested corrections also change the explicit hypotheses/scope of summary sentences, while leaving the underlying already-reviewed theorems intact. I found no detectable mathematical change to the ten non-map registry claims and no defect in their checked proof steps. The current family map has source/provenance inconsistencies, detailed below, so this manifest does not pass this check.

There is no surviving C3 input snapshot. Accordingly, “no detectable change” means agreement with what the two reviews actually quote, derive or describe; it does not assert a bytewise reconstruction of their inputs. I did not rerun scripts that would write additional files.

## (a) Audit of every disposition item

The classifications below use the brief's definition, including changes to hypotheses, scope and what the map asserts is covered. A mathematically substantive summary correction can be valid and already justified by the reviewed lemma; it need not change that lemma's proof.

| Disposition item | Current location and comparison with the seat request | Classification |
|---|---|---|
| Sol 1: FAC-A landed; FAC-B provisional | STATEMENT:94; REPORT:38–41, 78–79, 129–131; L4:149; EMPIRICAL:89–90. The detailed REPORT/L4 text adds FAC-L, the named class, exponent, TV-pop and GC-CS. This implements Sol's request to **add the qualified FAC-L subregion**, rather than just replacing a status word. FAC-B is provisional as requested. However, L4:167–168 still say FAC pending; the GC-CS failure sentence loses the study-pattern qualification. See F1–F3. | **MATHEMATICAL** for the new positive coverage, class, growth and visibility restrictions; the isolated verbatim status transcription is **EDITORIAL**. The disposition's blanket editorial classification is false. |
| Sol 2 / Opus 5: statement-change summary, RESULT and council record | REPORT:3–9, 54–58, 124–126 now record r3 and the earlier failed rounds, name the LOC-B enlargement and substantive post-r1 ENUM addition, and close the RESULT parenthesis. This answers both seats' housekeeping requests. The newly added claim that all post-C3 edits are editorial is itself inaccurate (F1). | **EDITORIAL** for the requested history/version corrections. |
| Sol 3 / Opus 4: coefficient sum | LEAD_READING:28 now says `Σ_kθ*_k = 0`. Both seats requested a scalar coefficient sum in place of ambiguous matrix-vector notation. The cancellation computation has not changed. | **EDITORIAL**. |
| Opus 1: fixed-p reading for all eight designs and iid-Gaussian caveat | REPORT:46–51 and EMPIRICAL:90–93 explicitly cover all eight fixed-p models, assuming a positive population floor and iid Gaussian rows; EMPIRICAL:61–64 qualifies iclaims and states serial dependence. Tecator's fixed-p case is included at EMPIRICAL:91–92. This answers the mathematical substance of Opus's request, although the sentences were placed in the headline/HQ summary rather than the requested Nature/REPORT §4 notes, and the local tecator paragraph itself remains unchanged. | **MATHEMATICAL at the summary-scope level**: coverage is explicitly extended to all eight and the iid-Gaussian qualification restored. It is a direct restatement of the already-reviewed universal fixed-p ENUM consequence, with no new theorem or proof. |
| Opus 2: Small-p headline names LSF | REPORT:23 adds “with POST's sparse floor LSF”, as requested. ENUM and its existing table row already imposed POST/LSF. | **MATHEMATICAL at the headline-hypothesis level**: it narrows the previously unqualified assertion. No change to POST or ENUM. |
| Opus 3: iclaims lower bound | EMPIRICAL:61 literally matches the disposition's “every pair ≥ 0.698”. It does **not** implement the safe bound requested by the seat: C3 Opus issue 3 says minimum 0.6978 and recommends ≥ 0.69. See F4. | **EDITORIAL/descriptive-number correction**, with a remaining factual/source mismatch; no theorem constant changes. |
| Opus 6: riboflavin null maximum | EMPIRICAL:66–67 now gives ≈0.6–0.67, typical ≈0.59, and identifies 0.67 as a crude upper reference. This carries the distinction requested by Opus; C3_scratch_opus/checks_out.txt gives median 0.585, approximately 99% quantile 0.646 and tail probability ≈0.0014 at 0.67. The 0.6–0.67 wording is looser than the seat's proposed wording but no new applicability conclusion is drawn. | **EDITORIAL/descriptive context**, not a proof or theorem change. |
| Opus 7: resource_limit on exact branch | L6_ENUM:13–14 now explicitly puts resource_limit in U_n and retains the conclusion jointly with output. The pinned copy v3_fit.R:26–60, 115–117 confirms an exact-branch preflight can stop before enumeration; :120–131 shows the exact branch returns before LS0. | **EDITORIAL clarification** of the existing no-delivery convention; no change to ENUM's hypotheses or conclusion. |

The unnumbered “Gate verdicts” footer in C3_disposition contains no additional edit to audit. All eight substantive disposition entries above have identifiable edits; the FAC synchronization and iclaims numerical repair are incomplete as specified.

## (b) FAC-A synchronization against its source

Source: W2-FAC-A/REPORT:20–53, supplemented only where necessary by its flags at :4–15 and the cited STATEMENT/instance lemma. This is a source-faithfulness check, not a fresh proof review of FAC-A.

| Source requirement/result | Current APP text | Assessment |
|---|---|---|
| :20–24: “PROVED-CHECKED” **for the narrowed, flagged target**, not the brief's full p ≤ n^A/fixed-k target | REPORT:39 and L4:149 repeat the status string and its narrowing; STATEMENT:94 also says narrowed class. | Status string and narrowing are faithful in these locations. L4 summary :167–168 is not synchronized (F2). |
| :28–30: correlation class 𝔉(γ̄, ψ₀, κ̄), one factor, bounded-size idiosyncratic groups, fixed floor, nonzero loadings and bounded κ | REPORT:39 and L4:149 name the exact class and describe one global factor plus bounded blocks. STATEMENT:94 delegates to FAC. | Faithful as a reference to the named class; “one factor + bounded blocks” alone must not replace all class conditions. |
| :30, 33–34: strict limsup log p/log n < 1/(2κ̄(κ̄+2)); 1/6 when κ = 1 | REPORT:39, 78–79 and L4:149 give the correct strict exponent/formula. | Correct. EMPIRICAL:89's `p ≲ n^{1/6}` is imprecise shorthand, saved from a boundary assertion by “where it applies”; use the strict condition instead (E1). |
| :32–35: deterministic-Gram FAC-L uses H0, AG, growth and actual-block TV, with the named method premises | Detailed synchronization expressly cites FAC-L/source rather than re-proving it. | No additional exact-Gram theorem is proved in APP. The source hypotheses remain part of the cited result. |
| :37–38: iid-Gaussian joint-law version requires TV-pop | REPORT:39 and L4:149 explicitly say “iid-row version (L5) under (TV-pop)”. | Correct; the existing iid-Gaussian setting and method premises remain in force. REPORT:79 is compressed and should repeat TV-pop, but its named-source/L4 reference provides the condition; I do not hold a separate S finding for that compression. |
| :40–44: CS requires GC-CS; S5 has certificates for the specified diagnostic/study layouts; general block CS retains analogous visibility | REPORT:39, 78 and L4:149 retain GC-CS/TV-pop and include S5. | Correct positive inclusion when read with these source conditions. However, “GC-CS … fails at a = 1/2” drops **which coefficient patterns** fail (F3); that is not a faithful universal exception. |
| :45–47: SHARP is a full-lattice NA obstruction above 1/6, not method inconsistency | REPORT:129 says route-optimal for the full lattice; :130 says beyond 1/6 is open for the path route. | Faithful route/method distinction. |
| :24 and flags :4–8: general factor/polynomial-dimension target, multiple factors, path beyond 1/6 and p > K remain open | REPORT:40, 129–131 and L4:149 retain these open regions; FAC-B is provisional. | Faithful. The source's separate delivery theorem is not imported; APP consistently retains its no-delivery convention. |

**What was examined at C3?** Sol issue 1 actually examined the newly landed FAC-A report: it names FAC-L, one factor/bounded blocks, strict 1/6, visibility/genericity and an off-enumeration CS example p_n = floor(n^{1/10}). It explicitly asks the lead to add that subregion. The Opus review lists the prior APP files and sources, derives the existing family facts F1–F4/STAR/VN/ENUM, and gives no FAC-L, 𝔉, α₀, 1/6, TV-pop or GC-CS examination. Nothing in its text establishes review of the new FAC-A assertion. Its review of L4 v2 cannot be treated as review of a later addition merely because the version label stayed v2.

For example, fixed-ρ CS with a single truth and p_n = floor(n^{1/10}) is eventually off ENUM, because 2^p grows faster than any polynomial budget while K = p. It was route-obstructed/open under the earlier VN map, but is now positively covered by FAC-A subject to its hypotheses. This is an actual change to the map's conclusion on a nonempty class, even though the external theorem was independently council-passed and Sol requested the addition.

## (c) Other detectable mathematical differences and limits

The headline restoration of LSF and the all-eight fixed-p summary are the two other explicit scope/hypothesis changes recoverable from the old sentences quoted by C3 Opus (issues 1–2). Both are justified by mathematical content that the seats already examined: POST/ENUM. They do not require rejecting those unchanged registry statements.

I compared the current core statements and proof landmarks with both reviews' actual re-derivations. The cutoff/prior ratio, sparse-floor rate, common-constant diagonal transfer; CT's t* and 2/α; CD's uncompressed-position double inverse argument; LOC's enlarged relevance set, radii and window comparison; LOC-B's post-enlargement logarithmic bound; VN's F16, nκ_n/log n floor, increment and two route regimes; STAR's spectrum, visibility scale and non-LOC count; and ENUM's full coded inequality and sufficient inequality all match the C3 descriptions. No additional mathematical change is detectable there. In particular, the new resource_limit sentence does not strengthen delivery.

The version labels remain STATEMENT v1.3.1, L4 v2 and ENUM v2, as in Opus's C3 scope list, despite the later map addition. Thus these labels are not evidence that the family-map contents are unchanged. The present manifest does establish the exact current text, but cannot establish an unavailable historical snapshot.

## (d) Per-claim decision table

| id | decision |
|---|---|
| W2-APP:POST | ACCEPT |
| W2-APP:CT | ACCEPT |
| W2-APP:CD | ACCEPT |
| W2-APP:Thm-LOC | ACCEPT |
| W2-APP:L3.6 | ACCEPT |
| W2-APP:LOC-B | ACCEPT |
| W2-APP:VN | ACCEPT |
| W2-APP:VN-routes | ACCEPT |
| W2-APP:Ex-STAR | ACCEPT |
| W2-APP:Family-map | REJECT |
| W2-APP:ENUM | ACCEPT |

Evidence for acceptance, using the reviews' own text rather than inferring examination from a PASS label:

- **POST** (L1:27–33): Sol G1/G5 and Opus G1/G2 explicitly check the cutoff, sparse-floor perturbation, diagonal tightness transfer and posterior conclusion. Current statement/proof matches those calculations.
- **CT** (L2:9–13) and **CD** (L2:41–50): Sol G1/G5/independent verification and Opus G1 separately derive CT's constant and Schur test, and CD's inverse-of-principal-precision formula, spectra and inherited positions. Current formulas agree.
- **Thm-LOC** (L3:34–38): both G1–G3 and Opus's detailed delta-proof audit examine the sandwich, NA/TL assembly and hypotheses. The stated events, output-joint conclusion and premises agree.
- **L3.6** (L3:99): both seats explicitly re-derive the new window argument, including the cᵀM⁻¹c variance, sample projection tail, polynomial lattice/polylog window counts, η_n and NA threshold margin. The current proof preserves those steps.
- **LOC-B** (L3:169–178): both G1/G2 explicitly verify exact conditional zeros and the enlarged-Q bound required by GROW L2.3(a). Both clauses remain present.
- **VN** (L5:23–26): both G1/G2/G5 examine the uniform visible-null floor, block-table increment and simultaneous maximizer argument. The statement matches the recorded count.
- **VN-routes** (L5:28–34): Sol G2/G5 explicitly distinguishes bounded-centre and logarithmic-sandwich obstruction; Opus G1/G2 derives VN/V1–V4 and its G1/G3 audit retains route-only conclusions and growing-null regimes. Current corollary uses those same two regimes and no method-failure conclusion.
- **Ex-STAR** (L5:64–72): Sol's G1/G2 and independent STAR/Schur checks, and Opus G1's explicit spectrum, covariance and non-LOC counting re-derivations cover the current example.
- **Family-map** (L4:152–171, read with its :7–17 conventions and :132–150 detailed entry): both seats examined the old map, but positive FAC-L coverage is a mathematical addition with no examination recorded by Opus; the current registered summary also contradicts that addition. This is **REJECT** because I found an actual mathematical map change and defects, rather than merely being unable to settle an unchanged claim. It is not a rejection of FAC-A's theorem.
- **ENUM** (L6:16–22): Sol G1/G4/G5/G6 and Opus G1/G2/G6 explicitly re-derive the full coded override, sufficient bound, posterior-majority implication and liminf identity against the code. The current lemma matches; the preflight clarification is faithful.

These are claim-specific transfers of the C3 examination plus this current-text check, not a claim that I have conducted a new full independent proof review of every upstream dependency.

## (e) Findings

**F1 — The post-council mathematical coverage change is falsely represented as editorial-only.** C3_disposition's opening says “no claim, hypothesis or proof changed”; REPORT:5 and :126 say the later edits are editorial/status-sync only. But C3 Sol issue 1 asks for a newly covered FAC-L subregion, and REPORT:39–40, 78–79 / L4:149 / STATEMENT:94 now import it. The off-ENUM CS example above demonstrates the changed mathematical conclusion. Opus's C3 text does not examine that new assertion. The unchanged version labels and earlier two-seat PASS do not support describing all current map content as unchanged reviewed text. **Repair:** record the FAC-L incorporation as a substantive cited coverage addition, with its exact conditions and review provenance; remove the blanket editorial-only assertion. This finding concerns the account of what the cited council reviews cover, not the correctness of FAC-L itself.

**F2 — The registered Family-map summary is not faithful to its detailed entry, STATEMENT or the cited source.** L4:167 says **“per FAC (pending)”**, and :168 says **“per FAC (pending) / LOC if local”**. Yet L4:149, STATEMENT:94 and REPORT:78–79 record FAC-A PROVED-CHECKED and a proved nonlocal subregion. W2-FAC-A/REPORT:20–44 explicitly supplies that result. These are the conclusion cells of the registered summary, not merely an obsolete date in a historical log. **Repair:** synchronize both rows with qualified FAC-A coverage (named class, strict exponent and TV-pop/GC-CS as appropriate), retain FAC-B provisional, and reserve open/pending for the remaining regions. The numerical exponent/visibility conditions must survive the synchronization.

**F3 — The new GC-CS caveat overgeneralizes a coefficient-pattern-specific failure.** REPORT:39 and L4:149 say “(GC-CS), which fails at a = 1/2” without specifying the study's coefficient patterns. The source REPORT flag :13–15 limits this exception to those patterns; FAC-A/L5_random_instances:146–159 gives their exact certificates and says “with these patterns”. FAC-A/STATEMENT:140–142 defines GC-CS through the coefficients. A counterexample to the unqualified failure assertion is s₀ = 1, θ₁ = 1, a = 1/2: for every null-only U of size u ≤ 15, its GC-CS expression is 1 + 1/(1+u) > 0, and the partial covariance is at least 17/32. Thus a = 1/2 is not a universal exclusion from FAC-A. **Repair:** say that GC-CS fails at a = 1/2 **for the specified study coefficient patterns**; retain the general coefficient-dependent condition. No FAC-A proof repair is indicated.

**F4 — The iclaims edit does not faithfully implement the recorded numerical correction.** EMPIRICAL:61 asserts the literal bound “every pair ≥ 0.698”. C3 Opus issue 3 reports minimum 0.6978 and recommends ≥0.69 (or >0.69); rounding a minimum upward does not establish the asserted lower bound. The disposition accurately describes the text that was inserted, but that text does not fix the seat's issue as stated. **Repair:** use ≥0.69, or explicitly state an approximate minimum ≈0.698. This is a small descriptive numerical defect and changes none of the ten accepted lemmas. The raw iclaims.rds is absent from this worktree, so I have not independently recomputed the correlation minimum; the discrepancy is directly against the supplied C3 numerical finding, not a claimed new raw-data calculation.

**E1 — Compressed growth notation and placement.** EMPIRICAL:89 should use limsup log p/log n < α₀(κ̄), specializing to <1/6 for block CS, rather than `p ≲ n^{1/6}`. Its “where it applies” reference and the exact detailed source condition prevent me from holding a separate strength finding. Repeating TV-pop in REPORT's factor row, putting the all-eight fixed-p sentence in the requested Nature/§4 notes, and adding the fixed-p sentence directly to the tecator paragraph would improve standalone readings. These are additional presentation repairs, not reasons to reject ENUM or LOC.

I hold **four F findings, no additional C or S finding**, and one E finding. The score reflects the limited map/provenance/source defects; no deduction is made for asymptotic scope, absent finite-n guarantees or lack of delivery. Because an F finding blocks under the brief, **gates=FAIL**, irrespective of the numerical score. The ten non-map ACCEPT decisions remain valid at the reviewed current text; Family-map needs correction and review of its substantive addition.

COUNCIL-VERDICT round=R3 manifest=72ac86f9fd0ca9fef850562ca9680d328de7dcef451c907bb693b925a2b31460 seat=pc1-sol score=8.4 gates=FAIL

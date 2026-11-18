# S5 — Independent Sol diff read of the S4 repairs

**Verdict: FIXES-NEEDED.** Six S4 findings are resolved; S3 is partly resolved because its new tag explanation incorrectly calls (A3) weaker. The required global grep also finds an unchanged, unqualified delivery assertion in METHOD_INTUITION. The repaired theorem statements, conditional-status prefixes and empirical counts otherwise follow their sources.

Reviewed once on `theory/W3-READER`, HEAD `4d08ca79c5ef7b4e1264e856ebb19a6dc28f4d35`. References below are at this HEAD and relative to `Theory_work/Wave3/W3-READER/`, unless another source is named.

## Integrity and scope

- Ran `sha256sum -c MANIFEST_S5.txt` from `reviews/S5_input/`: **OK**, SHA-256 `0653a251750943956eb28af00a9236ef1370d1c7bcad754d5881ef4f98f88434`.
- The supplied 227-line diff is byte-identical to `git diff c219065b 8676f5f9 --` restricted to its four files: CLAIMS_CARD, READER_VERSIONS, REPORT and R4. All four files, and the unchanged R3, are byte-identical at the repair commit and reviewed HEAD. The later reader-directory changes are LOG and the S5 brief/input artifacts.
- Read S4's seven findings; every added/changed line of the supplied repair diff; the complete R3/R4 files; the relevant current reader/source passages; and the S3-frozen baselines for the repaired strength tags.
- Compared the status quotations with `Theory_work/INFRA/registry/claims.tsv` at HEAD. Verified the on-disk SCR-R2 delta against `048b6b23`, PSHARP-R's `reviews/post_cp3/READER_DELTA_v0.4.md` against `8e22c756`, and MISR-R's corresponding post-CP3 delta against `93e50640`: byte-identical in each case. Read the named FUNI_NARROW patch and plus-assumption definition.
- Only this review file was written. No scratch, TMPDIR changes, sub-agents or git mutations.

## S4 findings: individual dispositions

| S4 finding | Disposition | Evidence and source check |
|---|---|---|
| **S1 — Theorem 10 completion remark** | **RESOLVED** | `READER_VERSIONS.md:1052–1053` now gives completion on 𝔇 under (S4)(i)–(iv), and for every admissible n only with A:IDEAL-W⁺; the unused-link qualification remains. Its tag at `:1069–1070` is WEAKER. This matches FUNI_NARROW's narrowed clauses (a)/(b), and `lemmas/R4_printed_outputs.md:47–49`. The separate global grep finding G1 below is outside this repaired remark. |
| **C1 — Card 2.2 metric and premises** | **RESOLVED** | `CLAIMS_CARD.md:53` restores G, fixed s₀≥1, R1, E and F₀ for both parts, posterior selection in probability for (a), and OS for (b). Both conclusions explicitly converge in probability. It distinguishes the distance bound Mₙ/√n from the squared-distance bound C′H log n/n and its square-root radius. This is the proposed S4-frozen row `proposal/DELTA_row21_thm9_DIST.md:303`, with the fallback placement retained because the DIST swap remains unapplied, and follows `Theory_work/Wave3/W3-POST2/STATEMENT.md:103–115`. |
| **F1 — Conditional statuses, stale pins and root scope** | **RESOLVED** | `CLAIMS_CARD.md:46` now quotes the complete conditional prefixes for CorH-plus, CorH-U (including its extra (G) conditions), and POST2 C/E/A1/A0. They match registry rows 475–476 and 358–365; ellipses abbreviate subsequent evidence, not conditions. `lemmas/R4_printed_outputs.md:11–12,24–25` now agrees with its header and registry C@1.1.3 / APP@1.0.6, each conditional on SOP:TH09. `REPORT.md:38,46` updates RM2-R/F to 1.0.2 and R4's input pins, retaining the expressly deferred F-UNI requotation. `READER_VERSIONS.md:723` corrects B2.2's label; `CLAIMS_CARD.md:130–131` scopes the single-root note to abstract rows 1.1 in O_P form, 1.2 and 3.1; `READER_VERSIONS.md:1080` retains the additional POST2 conditions. |
| **S2 — Off-truth floor in the comparison** | **RESOLVED** | `CLAIMS_CARD.md:43` now says the margin replaces the bounded-size floor (A4) off the truth and beta-min, while retaining (A5). This agrees with `READER_VERSIONS.md:127–140` and the reader's retained logarithmic-size floor; it does not import the master's more general OS form while dropping that reader premise. WEAKER is correct for the literal comparison repair. |
| **F2 — Certification versus model size** | **RESOLVED** | `READER_VERSIONS.md:928–935` attributes certification, without an all-fit smallness claim, to 2,394/2,394 production fits, 376/376 strong-factor fits and 71/71 screening fits. Size evidence is separated: ≤2s₀ for all 376 and ≤5 for all 71, with no per-fit production sizes claimed. These statements and the unchanged containment counts match the SCR-R2 delta at `048b6b23:108–112,138–146`. The omitted production-study bound for 2,194 fits is optional; it is not promoted to an all-fit bound. |
| **E1 — Placement instructions and pointers** | **RESOLVED** | `CLAIMS_CARD.md:101–107` keeps the O_P Form A/B1 choice and expectation/1′ body placement, and retains omitted-variable conditions until discharged rather than merely recorded. `REPORT.md:34` reaches R3's complete assembly/file at :54. Its expanded R4 span at `:42` covers the claim/proof and the delivery qualification at R4 :47–49. `READER_VERSIONS.md:72` correctly points to START at `Theory_work/Wave1/W1-N1/STATEMENT.md:75`. The additional D-17 provenance repair at `CLAIMS_CARD.md:143–144` also checks: the main-checkout working file exists, is untracked there, and its D-17 row is :83. |
| **S3 — Swap baseline and separate consequences** | **PARTLY** | `CLAIMS_CARD.md:3`, `READER_VERSIONS.md:5–6,438–440,560–562,955–958` now declare the delta-relative baseline and separately record S3-relative changes. Theorem 3's added expectation-exactness, growing-s₀ and critical-scale conclusions, and card 3.7's weakening, are correctly distinguished. However, the new Theorem 4 explanation at `:561` wrongly includes unchanged (A3) among weakened hypotheses; see N1. |

## Findings requiring repair

### G1 [S] — Global delivery grep fails in the intuitive overview (pre-existing)

**Location:** [METHOD_INTUITION.md:81](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/METHOD_INTUITION.md:81), sentence continuing through :82.

> Together with the fallback ladder, freezing guarantees that a run with enough computing allocation always produces output (the delivery result used in Theorems 6–7).

This reader-facing assertion supplies neither 𝔇 nor IDEAL-W⁺. It therefore still promises completion without the additional hypothesis even if the ordinary ideal-machine conventions are understood. “Enough computing allocation” cannot rule out the shipped rejection predicates. The FUNI_NARROW patch, narrowed clauses (a)/(b) and appended remark, and `A_IDEALW_PLUS.md`'s definition explicitly separate these conditions; the definition expressly says a larger allocation does not imply the plus assumption. A parenthetical theorem reference does not state either alternative.

This sentence is already present at `c219065b` and METHOD_INTUITION is unchanged by the supplied diff: it is a newly detected residual defect, **not introduced by these repairs**. It nevertheless fails task 3's explicit whole-reader check. Theorem 10's repaired sentence passes independently.

**Repair:** give the overview sentence the same delivery conventions and 𝔇/IDEAL-W⁺ alternatives as Theorems 6–7, in reader words. Its restored hypothesis is WEAKER relative to the current unconditional wording. No new numerical onset discussion is needed. The local calibration-stage statement at METHOD_INTUITION :78 describes the fallback proceeding; the table question at :119 is not itself another completion theorem.

### N1 [F] — The new Theorem 4 tag explanation incorrectly weakens (A3)

**Location:** [READER_VERSIONS.md:561](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:561), in the new S4 tag record :560–562.

The parenthesis says “weaker hypotheses (A0), (A2), (A3)”. The S3-frozen (A3) at `reviews/S3_frozen/READER_VERSIONS.md:348–350` and current (A3) at `READER_VERSIONS.md:460–462` impose the same relative-energy bound and divergent beta-min condition. The covariance notation is renamed from Σ𝒞𝒞 to Σ; the hypothesis is not weakened. The pinned MISR-R delta itself says **“unchanged in the reader text”** in its (A3) row (:15), and gives the same formulas at :32–34. The source's weaker fixed-liminf alternative remains a remark, not the reader's (A3).

The main theorem's overall STRONGER tag is correct because its model assumption and correlation-floor condition are weaker. The repair's clause-level explanation is not faithful and therefore does not fully settle S3. Also distinguish the added example scope from the already-present invertible jointly Gaussian example: S3 :335–342 already contains its model and projection formulas; the pseudoinverse/linear-plus-noise additions are the new scope. The new wording “the examples are new (STRONGER) statements” at :562 should refer specifically to those additions.

**Repair:** change the explanation to “weaker model assumption (A0) and floor (A2); (A3) unchanged, with the same two displayed conclusions”, and identify the expanded example scope as new. This corrects the tag record only; it requires no theorem change.

## D71 inventory: every added/changed line

The supplied diff adds or replaces 44 lines. The following inventory covers all of them, including complete changed table rows. The unchanged literature sentences within those rows retain the S4 assessment; this repair introduces no further literature interpretation.

| HEAD location | Changed assertion(s): judgment and source |
|---|---|
| `CLAIMS_CARD.md:1,3` | Version/title and repair inventory; **FAITHFUL** as bookkeeping, subject to N1's qualification of the claimed S3 tag repair. The stated WEAKER/EQUAL classifications for the other repairs are correct. |
| `CLAIMS_CARD.md:43` | Bounded-size off-truth floor and beta-min replaced, (A5) retained: **FAITHFUL**, reader Theorem 1′ :127–140 and POST2 E with the reader's retained premises. The carried-over SL attribution is unchanged. |
| `CLAIMS_CARD.md:46` | Separate CorH-plus/U statuses, extra (G) conditions, and separate C/E/A1/A0 prefixes: **FAITHFUL**, HEAD registry rows 358–365,475–476. Existing result/comparison text is unchanged. |
| `CLAIMS_CARD.md:53` | Metric, common premises, probability mode, selection/OS alternatives and both radii: **FAITHFUL**, POST2 D :103–115 and S4's proposed row :303. |
| `CLAIMS_CARD.md:101–102` | O_P abstract; expectation/1′ body with conditions: **FAITHFUL**, HQ decision already recorded in READER_VERSIONS :211–215 and card :88–94. |
| `CLAIMS_CARD.md:106–107` | Omitted-variable conditions persist until discharged: **FAITHFUL**, full conditional prefixes at card :46. These are editorial placement instructions, not a proposed reader sentence containing registry identifiers. |
| `CLAIMS_CARD.md:130–131` | Single root limited to the selected abstract route; other rows retain further inputs: **FAITHFUL**, registry prefixes and READER_VERSIONS :192–215. |
| `CLAIMS_CARD.md:143–144` | D-17 is a main-checkout untracked working-file source, without a commit pin: **FAITHFUL**, direct file/`git ls-files` check. The descriptive measurement is unchanged. |
| `READER_VERSIONS.md:5–6` | Declared swap baseline and separate S3-relative records: **FAITHFUL** as a convention; N1 corrects one record under it. |
| `READER_VERSIONS.md:72` | START pointer :75: **FAITHFUL**, current N1 :75. Status wording is unchanged. |
| `READER_VERSIONS.md:438–440` | Every-p expectation lower bound, orthogonal expectation exactness, growing-s₀ obstruction and critical-scale bound are STRONGER vs S3; original probability/domain clauses EQUAL: **FAITHFUL**, S3 frozen §3 and pinned PSHARP-R delta :23–32,37–80. EQUAL to the delta is explicitly a different baseline. |
| `READER_VERSIONS.md:560–562` | Main theorem STRONGER; two displays unchanged; new contraction/uniform statements STRONGER; EQUAL to delta: **FAITHFUL in these respects**. Inclusion of (A3) among weakened hypotheses and blanket novelty of the examples: **NOT-FAITHFUL as written**, N1 and pinned MISR-R delta :13–19,32–58. |
| `READER_VERSIONS.md:723` | B2.2 checked and conditional on SOP:TH09: **FAITHFUL**, APP@1.0.6, registry :153. POST-R's retained conditional prefix matches registry :461. |
| `READER_VERSIONS.md:928,930–932` | All-completed-fit certification separated from the two studies with all-fit size evidence; production per-fit size unavailable: **FAITHFUL**, pinned SCR-R2 delta :108–112. Certification counts and containment observations remain empirical. |
| `READER_VERSIONS.md:955–958` | SCR swap EQUAL to delta; card 3.7 WEAKER vs S3; Theorem 8′ a STRONGER addition; empirical smallness correction WEAKER: **FAITHFUL**, S3 frozen card :52 / reader §8, SCR-A/A1/A-inf and pinned SCR-R2 delta §§3,5. |
| `READER_VERSIONS.md:1052–1053,1069–1070` | Completion on 𝔇, every admissible n with plus, unused link and WEAKER tag: **FAITHFUL**, FUNI_NARROW clauses (a)/(b) and definition. Existing localization/rate claims are unchanged. |
| `READER_VERSIONS.md:1080` | POST2 bridge dependencies include more than T03♯, referring to their full quotations in §1 and listing C's further inputs: **FAITHFUL**, registry C/E/A1/A0 prefixes. This summary does not pretend to be a shortened verbatim status quote. |
| `REPORT.md:34,38,42,46` | R3 span includes the whole assembly; R4 span includes its delivery qualification; current RM2-R/F and C/APP pins; deferred F-UNI repin: **FAITHFUL**, current R3/R4 and HEAD registry. The claim/proof statements and gate labels are unchanged. |
| `lemmas/R4_printed_outputs.md:11–12,24–25` | Operative input versions and full conditional statuses synchronized with the header: **FAITHFUL**, registry C :355, APP :153 and Thm-1 :344. No probabilistic claim is changed. |

No changed reader sentence adds an internal claim identifier as mathematical content; status, source, placement and change-log blocks remain administrative. Named mathematical premises in card 2.2 are accompanied by their reader descriptions. The required plus-assumption name is retained. No changed passage frames asymptotic validity as a limitation, and no numerical n₀-size warning is added. The pre-existing mandated RM2R-5 code-limit sentence is unchanged. The empirical sample sizes are observations, not onset claims.

## Grep check: whole-reader delivery/completion

Ran this broad grep from the worktree root, then read each hit in its surrounding sentence/paragraph:

```bash
rg -n -i 'IDEAL-W|every.*(admissible|output|complet)|always|no[ _\\-]?output|complet|terminat' Theory_work/Wave3/W3-READER/{READER_VERSIONS,CLAIMS_CARD,NOTATION,METHOD_INTUITION,REPORT}.md Theory_work/Wave3/W3-READER/lemmas/*.md
```

It returns **77 matching lines**, listed completely below; these are lexical hits, not 77 violations. An initial narrower delivery grep and a supplemental `for all|always|complet|terminat` search were also inspected. Including `always` independently matters: the failing sentence splits “always produces” and “output” across two lines.

| File | All matching HEAD line numbers | Assessment |
|---|---|---|
| `READER_VERSIONS.md` | 9, 32, 50, 51, 55, 60, 62, 71, 665, 666, 668, 670, 672, 710, 713, 724, 750, 754, 759, 789, 790, 791, 793, 795, 797, 840, 843, 929, 1003, 1005, 1013, 1015, 1017, 1052, 1053, 1061, 1069, 1070 | Delivery assertions carry 𝔇/plus in the full sentence or preceding display hypothesis; other hits describe output-event intersections, completed-run localization, numerics or historical logs. No plain-IDEAL-W every-n assertion. |
| `CLAIMS_CARD.md` | 4, 59, 64, 96, 97, 99 | Row 3.1 and abstract-placement instructions state the bounded/plus alternatives; row 3.6 uses intersections. No violation. |
| `NOTATION.md` | 110, 119, 124, 139, 141, 147, 244 | Delivery conventions :140–148 explicitly distinguish bounded delivery and plus-only every-n delivery. Other hits concern complete linkage/scans or seed quantifiers. No violation. |
| `METHOD_INTUITION.md` | 58, 78, **81**, 119, 167, 182, 187 | **G1 at :81–82** is an unqualified universal delivery claim. :78 is local fallback continuation; :119 asks a question. Other hits are algorithm/code descriptions. |
| `REPORT.md` | 37, 45 | R3 has bounded/plus alternatives; R4 concerns intersections. No violation. |
| `lemmas/R3_delivery_assembly.md` | 6, 7, 10, 11, 12, 17, 27, 29, 31, 36, 40, 46, 47 | Target/assembly explicitly carry 𝔇/plus; the shortened Step-2 quotation at :17 is read under the file's narrowing header :6–8. Remaining hits concern premises/scans/stop rules. No violation. |
| `lemmas/R4_printed_outputs.md` | 8, 17, 21, 48 | Completed-run localization or explicitly additional plus/domain premise :47–49. No violation. |
| `lemmas/R1_set_sizes.md`, `lemmas/R2_local_regression.md` | none | No delivery assertion; supplementary “for all” matches concern coefficients/lattice models. |

**Plain-IDEAL-W every-n check: NOT CLEAN — METHOD_INTUITION.md:81–82 (G1).** Sufficient allocation alone does not supply the missing plus/domain condition.

## Statement-change tags confirmed

| Repaired statement or record | Correct tag and baseline |
|---|---|
| Theorem 10 completion remark | **WEAKER vs pre-repair**: restores 𝔇 or plus; EQUAL to narrowed F-UNI's scope. |
| Card 2.2 | **WEAKER vs pre-repair** for restored premises; metric correction is faithful to the unchanged master. |
| Card 1.1 comparison | **WEAKER vs pre-repair**: restores the retained (A5). |
| Statuses, input pins, scoped root note, source spans, START pointer, abstract placement and D-17 provenance | **EQUAL mathematically**. |
| Certification versus smallness | **WEAKER vs pre-repair empirical assertion**; evidence is no longer promoted to all-fit smallness. |
| Theorem 3 swap | **EQUAL to its delta**. **STRONGER vs S3** for the every-p expectation display, fully orthogonal expectation exactness, growing-s₀ expectation obstruction and critical-scale bound; **EQUAL** for old probability clauses and size-domain consequences. |
| Theorem 4 swap | **EQUAL to its delta**. **STRONGER vs S3** overall through the model/floor relaxation and added explicit contraction/uniform conclusions; **EQUAL** for (A3) and the two original conclusion displays. The old invertible Gaussian example's formulas are retained; its expanded example scope is new. **N1 requires correcting the new record.** |
| SCR swap | **EQUAL to its delta**. Card 3.7 is **WEAKER vs S3** through restored intersection-event/fixed-constant scope; Theorem 8′ is a **STRONGER addition vs S3**, EQUAL to A-inf. |

The new per-row records supply the requested baseline separation; earlier log summaries are historical and must be read subject to these records. N1 is the only new defect introduced by the supplied repair diff. G1 is a separate pre-existing failure of the required global check. No other defect was found in the changed lines.

S4 FINDINGS: S3 PARTLY (N1); S1, C1, F1, S2, F2, E1 RESOLVED
NEW DEFECTS: N1 — Theorem 4 tag record calls unchanged (A3) weaker and overstates example novelty
PLAIN-IDEAL-W EVERY-n: METHOD_INTUITION.md:81–82 (G1, pre-existing unqualified allocation-only delivery assertion)
FIDELITY: NOT-FAITHFUL
VERDICT: FIXES-NEEDED

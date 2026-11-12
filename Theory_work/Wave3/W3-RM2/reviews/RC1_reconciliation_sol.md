MANIFEST 94c0349e10ddd9354fe9317803559f78d8d05f1682bf8e5d2d10e3f1a863c735

Per-finding verdicts

Evidence below uses worktree-relative paths. S denotes Theory_work/Wave3/W3-RM2/STATEMENT.md. R1–R6 and O1–O4 follow the numbering in reviews/SL1_statement_lock_sol.md.

R1 — RESOLVED.
S:85–88 separates Form F's b < beta(eta,A) from Form R's b < 1/2 and 15rho+b < 1/2. S:141–148 and S:196 now quantify D-R^b => W-R for every fixed delta0 in (0,1-2b); S:179 makes the same choice in containment. C2 at S:162–164 can still assume W-R directly for any fixed delta0 in (0,1). W-unif at S:105–106 has its own parameter delta in (0,(1-2b)/2), making its radicand positive. The explicit choice in C3(c), S:173–175, is consistent. See the constant checks below. No further change required for this finding.

R2 — RESOLVED.
S:53–55 defines beta_{B,l} on every B subset Q minus {l}, with the invertible-Gram qualification, the empty-set value, P_empty=0 and zero-padding to R^Q. FL-Q supplies the requisite principal-submatrix inverses. S:125 explicitly covers the sets used by W-loc, including the empty set. No further change required.

R3 — RESOLVED.
P0 at S:187 specifies a deterministic nonempty finite vector set VV containing every r_A and r_A-r_A', and defines r_A=(I-P_A)mu. Thus log|VV| is defined. It explicitly defines the toolkit events with the new t_n and h_n and states their corresponding failure bounds. These are the inherited premises in Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:10–22 and Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md:42,92–96. No additional size budget or new hypothesis has been introduced.

R4 — PARTIALLY RESOLVED; remaining MAJOR (registry dependency completeness).
The main hypothesis repair is correct: S:262 lists W alone for C1; S:274 lists W-R alone for C2. Within their stated settings/premises these lists match C1 and C2 at S:152–164. The alternatives appear separately, expressly marked as alternatives, at S:299–302 and S:309–311. The size restrictions are now ARTEFACT/sufficient budgets at S:256,267–280; W's necessity is limited to the whole-lattice route and slack. Conditional headline statuses correctly retain SOP:TH09/W2-APP:POST and W1-GEN:L1 at S:261,273. The central assembly now has explicit edges for Toolkit-b, SAND, TL and NA at S:265,277, with the conditional F-to-R chain at S:308. Direct SOP:TH09 and W2-APP:POST edges cover the inherited POST interfaces in principle; separate new registry ids for those unchanged implications are not essential.

However, the assertion at S:255 that every used bridge is an explicit edge is still false:
* RM2-F's containment field at S:266 expressly uses W-suff, and its sharpness/binding fields at S:267–268 expressly use W-conv. Neither occurs in its depends_on at S:265.
* RM2-R's containment field at S:278 expressly uses D-to-W, absent from S:277. Its route-sharpness assertion at S:279 also needs W-conv (applied conditionally on the design).
* W-suff's declared source engine at S:191 is C-GROW:L2.3, but its row at S:299–302 has no corresponding edge. D-to-W at S:196 uses the NA-R proof and the D-loc construction, but its row at S:309–311 likewise has no source edges. These are proof-template dependencies; recording them need not consume the old conclusions outside their stated size range.
* P10 at S:197 explicitly says POST-R is obtained through RM Lemma B9; S:277 records W2-APP:POST, but no B9 edge. B9 is a distinct bridge (including the p=1 endpoint), not just another name for the APP statement; see Theory_work/Wave3/W3-RM/lemmas/L4_formR.md:49–58 and registry/claims.tsv:386.

Exact required additions to S's registry block (append the entries to the indicated depends_on lists, and add the missing lists):
- S:265: `; W3-RM2:W-suff@stmt ; W3-RM2:W-conv@stmt` (containment and route-sharpness fields).
- S:277: `; W3-RM2:D-to-W@stmt ; W3-RM2:W-conv@stmt ; W3-RM:B9@stmt` (containment, route-sharpness and P10).
- W-suff row, after S:302: `depends_on: C-GROW:L2.3@proof`.
- D-to-W row, after S:311: `depends_on: W2-LOC2:NA-R@proof ; W3-RM:D-loc@proof`.

Retain the qualification that these old-size proofs are re-run at the new sizes. Because B9's registered status is below PROVED-CHECKED, append `; conditional on W3-RM:B9@1.0.0 for (P10) unless that bridge is re-proved self-contained here` to the RM2-R target status at S:273, and disclose the same condition in section 5. An alternative to the B9 addition is to replace P10's `through RM Lemma B9` by an explicit self-contained POST-R target covering the APP p>=2 case and its p=1 endpoint, register that bridge and bind it in S:277. Do not silently retain B9's result while omitting its edge/status.

These changes complete the requested records; they do not add assumptions to C1 or C2 or propose a different theorem. PROTOCOL.md:157–160 requires explicit edges, and LIFECYCLE.md:69–73 says plain consumes labels are informational. Creating registry ids without binding their actual uses is insufficient.

R5 — RESOLVED in the example; one related stale cross-reference remains as new defect N1 below.
C5 at S:206–209 now distinguishes the construction exponent rho* from the registering exponent rho, takes b>1/(2alpha), rho>rho*>1/(4alpha), and requires 15rho+b<1/2. This absorbs both fixed multiplicative constants from Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md:43–53,233–242. If alpha>17/2, the limiting total 15/(4alpha)+1/(2alpha)=17/(4alpha) is strictly below 1/2, so both exponent enlargements can be chosen. The Form F example likewise takes b>1/(2alpha) at S:202. No further example change required.

R6 — RESOLVED.
S:225–229 gives the full SOP:TH09@1.0.0 and W2-APP:POST@1.0.1 statuses, matching Theory_work/INFRA/registry/claims.tsv:11,153 (allowing line wrapping). S:224–232 retains their conditional-use treatment and the separate GEN condition. No assurance level was upgraded.

O1 — RESOLVED.
S:64–66 calls the width the expected maximum of shifted absolute Gaussian projections and explains the offsets. The introductory Gaussian-process wording at S:21 is informal; the defining passage now makes the precise object clear. No change required.

O2 — RESOLVED.
S:120,127 states nu_n <= h log n/log 2 and h<1/2-b, without the rounded 0.72. S:128 qualifies log(q+1) comparable to log n by an explicit polynomial lower bound q>=n^{b'} with fixed b'>0. Merely q<=n^b no longer purports to imply it. No change required.

O3 — RESOLVED.
S:63 exempts the empty pair set from supplying references and sets both widths to minus infinity. S:141–143 defines the realised width on the floor event W_n^0 and the good event as its subset. Read the second event there on W_n^0, as the immediately preceding text specifies; no width value on bad designs is needed. No change required.

O4 — RESOLVED.
S:199–204 makes verification a later proof obligation and explicitly defers the fixed-design truth-separation/coefficient conditions to that verification. S:204–205 labels the equicorrelated example a candidate, not verified, with only a heuristic range. It is not promoted to a proved example. No change required.

New defects

N1 — MINOR: stale exponent equality in the summary of the polynomial-decay budget.
Location: S:246–247. After the repair in C5, the theorem's exponent is strictly greater than 1/(2alpha); the parenthesis here still states `b = 1/(2alpha)`. This contradicts the coefficient-one bound as now instantiated and can direct a reader back to the unabsorbed constant.
Exact change: replace `15rho + b < 1/2 with rho > 1/(4alpha), b = 1/(2alpha)` (in the file's mathematical typography) by `15rho + b < 1/2 with b > 1/(2alpha) and rho > rho* > 1/(4alpha), choosing both enlargements with strict slack as in (C5)`.

No new mathematical defect found in the revised width constants, regression domain, toolkit premises or example exponent choices. The remaining MAJOR requirement is residual R4 above, rather than a newly introduced theorem failure.

Lock verdict: LOCK WITH CHANGES

Required before lock: finish R4's explicit dependency/status records (MAJOR) and correct N1's stale equality (MINOR). No CRITICAL issue found. This verdict concerns a target statement; it does not certify its unproved bridges.

Checks performed / not checked

- Read the RC1 brief first. Ran the permitted manifest verifier from C:/Users/felip/BVS-wt/W3-RM2; result: `verify: OK MANIFEST 94c0349e10ddd9354fe9317803559f78d8d05f1682bf8e5d2d10e3f1a863c735`.
- Independently checked W-unif => W: k+1<=n^b+1, so a_{n,delta}(k)^2 is at least 2log p+(1-delta-2b)log n-2log(1+n^{-b}). Its squared gap above the W-unif threshold is at least delta log n-2log(1+n^{-b})>0 eventually. Thus E max(|u'g|-a(k))<=E max|u'g|-min a(k)<=0. Empty pairs are vacuous.
- Independently checked the W-ref chain: its expected maximum is bounded by sqrt(2log p+2h log n)+o(sqrt(log n)), using fixed reference dimension, the atom budget and the remainder budget. At delta=(1-2b-2h)/4>0, the W-unif squared threshold exceeds 2log p+2h log n by (1/2-b-h)log n=2delta log n. Since log p=O(log n), this leaves a positive gap of order sqrt(log n). Also delta<(1-2b)/2. This establishes the stated constants for W-ref => W-unif => W with delta0=delta; delta1 is separately the W-chi/converse slack.
- Checked the D-R^b slack against the population reference formulation and the previous review: its intended re-run yields a joint-law bound B_n^2<=2log p+o(log n). Conditional probability at least 1/2 for most designs, followed by the median/mean bound for a 1-Lipschitz Gaussian maximum, gives conditional mean <=B_n+O(1). The minimum a-level squared is at least 2log p+(1-delta0-2b)log n-O(1); every fixed delta0<1-2b supplies the needed positive gap. Sample floors follow under N1 with q sqrt(log n/n)->0. C2 can assume W-R directly for larger delta0; C4 chooses b,rho small and delta0 in the sufficient interval. No hidden Form F eta restriction is inherited by Form R.
- Compared the ten requested repairs against SL1 and its disposition; checked the altered definitions against the permitted source passages, full status strings against the frozen registry, and the explicit registry graph against PROTOCOL rule 16. The C1/C2 hypothesis bundles and the route-only/sufficient-budget limitations are preserved, subject to the record repairs identified above.
- Did not prove P0–P10, run simulations, certify the examples, inspect git metadata, or re-audit the unchanged code/core proof. Did not consult any LOG.md, CHECKPOINT, excluded review folder, external memo worktree, live hold record or unlisted source. The manifest tool was executed only in its permitted verify mode. No git command/state change or subagent was used. Wrote only this review file.

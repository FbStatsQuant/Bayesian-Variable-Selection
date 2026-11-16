D5 diff check — 8cd03b526f11877f a786d3fc80069520 9c1149461e2f1f43 16c388ef38aae225 201ef734074d38bf

Hashes above are recomputed SHA-256 prefixes, in the order STATEMENT.md, lemmas/DIST12.md, TARGET.md, REPORT_extra.md, mkreport.py. All five match reviews/D5_hashes.txt.

Read the complete brief, the two named council findings, the disposition and the exact patch. An inline, nice Python check reversed every explicit unified diff against the current file and recovered the full R1 manifest hash for STATEMENT.md, lemmas/DIST12.md, TARGET.md, REPORT_extra.md, mkreport.py and DEPS.tsv. Thus the conclusions about unchanged text do not rely only on the patch's description. The twelve supporting proof files inspected for constants, imports and status conditions also match their R1 manifest hashes.

Finding D5-01 — MINOR.

Place: lemmas/DIST12.md:72, the newly inserted phrase “A = log p_raw/log n”.

Error: the setting assumes p_raw <= n^A, with fixed A >= 1; it does not assume equality. Consequently log p_raw/log n <= A, and the displayed identification can be false. For example p_raw = 2 and A = 1 satisfy the dimension assumption for every n >= 2, but log 2/log n differs from 1 when n > 2. The earlier wording explicitly restricted the identification to “when p_raw = n^A”; the replacement loses that restriction. This is an error in the explanatory parenthesis, not in the fixed-A rate, the constants, or either theorem's proof.

Minimal repair: replace “gives no rate linear in A = log p_raw/log n” by “gives no rate linear in A (equivalently, in log p_raw when p_raw = n^A)”, or simply “gives no rate linear in A”. No constant or mathematical conclusion needs changing.

Item 1(a): the revised rate and both quoted constant facts are correct. In X.md §0, C_d = 34 and C_x = 34(A + 1) + 2. Its Lambda >= 32 C_x and C_X = max{4(2 C_d + 4 + C_P + Lambda), C_v} imply

    C_X >= 4 Lambda >= 128[34(A + 1) + 2].

DIST12.md D.1 defines C_T = 4[34(A + 7) + 8] exactly. Both depend on A and are independent of the raw sparsity s. D.4 takes C^2 = C_X^2 + C_X/2 + 1 + C_T, so C depends only on (A, sigma*^2, M, M'). X.md defines M_0 = max{16, (A + 1)s, log C_5} and proves the quoted upper bound. For integer s >= 0 and A >= 1, M_0 >= 1 + s (including s = 0). Together with that upper bound, this gives M_0 of order 1 + s for fixed (A, sigma*^2, M, M'), and hence epsilon_n^2 = C^2 M_0 log n/n of order (1 + s) log n/n. Thus even the two-sided interpretation of “of order” holds for the selected radius. D5-01 concerns only the subsequent identification of A with the actual dimension exponent.

Item 1(b): target clause **TC3 (DIST-1, rate)** is unchanged, byte for byte, between the reconstructed frozen TARGET.md and the current TARGET.md:53:

    Best radius epsilon_n^2 = C^2 M_0 log n/n with M_0 = O((1 + s_0^r)(A + 1)).

It is still proved as written: the displayed upper bound on M_0 supplies this O bound for fixed (sigma*^2, M, M'), while the separate C may depend on A. TC3 does not assert that the entire radius is linear in A.

Item 1(c): CONFIRMED. “EQUAL on TC3” correctly records an unchanged, proved target clause. “WEAKER on a descriptive sentence of consequence (c), not a target clause” correctly records removal of the free-A reading. For fixed A >= 1, log p_raw = A log n when p_raw = n^A, so replacing log p_raw by log n under that additional restriction does not change the n-order. Holding A fixed is the substantive narrowing of the gloss. The tag does not pretend that the former free-A rate had been proved.

Item 1(d): searched STATEMENT.md, TARGET.md, REPORT_extra.md and lemmas/DIST12.md for rate/order, log-p and linear-in-A wording. No other operative sentence repeats the free-A rate assertion. The remaining linear-in-A assertion about M_0 is the upper bound permitted by TC3, not an assertion about C^2 M_0. TARGET.md's general sparsity discussion of “a rate of order log p/n” does not assert the disputed dependence of DIST-1's constant on A. The old rate wording in changelog row 1.4.10 is explicitly quoted as superseded. REPORT_extra.md's DIST-1 registry conclusion now fixes A and discloses C's parameters. Apart from the version header, the patch changes only the indicated explanatory sentence after D.4 in lemmas/DIST12.md. D5-01 is the one remaining local wording amendment.

Item 2: the assurance repair is present for all five claims. Evaluating only the status-data assignments of mkreport.py in memory gives “PROVED (by this seat), line-checked, conditional on SOP:TH09” for S, V, X, X' and NEC. Each registry block in REPORT_extra.md uses the corresponding @@st:name@@ substitution and has depends_on: SOP:TH09@hyp. REPORT_extra.md §5 explicitly extends the qualification to these five lemmas/propositions; SOP:TH09 is not promoted.

The proof-file evidence supports the qualification:

- S: work/C_size/S.md's setting uses thm:T01i; Step 1 imports lem:num, thm:Ta and the slab/integral representation from lem:slab and the proof of lem:den. These are substantive locked-P1 inputs.
- V: work/C_size/V.md identifies the slab minimum and spectral/determinant formulas with [P1] lem:slab and lem:spec in Steps 0 and 2. Many of these algebraic identities are re-derived locally, so the blanket qualification is conservative; it cannot overstate assurance.
- X: lemmas/X.md §0 explicitly lists locked-P1 inputs; §4 actually uses lem:num, lem:slab, the proof of lem:den and thm:Ta. The conditional status is required.
- X': §9 reuses §4's numerator/denominator step and the conditional posterior calculations. Removing ND does not remove the locked-P1 input.
- NEC: lemmas/NEC.md §§1–2 use [P1] lem:spec for the determinant and fitted-mean matrices; its posterior calculations use the locked slab representation. The conditional status is appropriate.

No additional missing SOP:TH09 qualification was found for H, T, P6, B0, B1, B2-core, B2 or B3 under the same rule. H is a deterministic normal-density calculation, T proves its transfer bound, and P6 is a measure-theoretic domination/convexity lemma for any posterior decomposition. B1 and B2-core prove their concentration bounds; B2 re-derives its determinant argument and expressly does not consume unchecked A0. B0 consumes W3-MISR:R', whose registry status is PROVED-CHECKED without an SOP:TH09 condition. B3 uses those bridges and carries its W3-POST:Thm-1 qualification in the status and registry dependency; its source for the m-sharp bound is expressly recorded as part of that consumed premise. No claim in this list needs an additional locked-P1 condition merely because the posterior occurs in its notation.

Item 3: all explicit hunks answer the two findings or maintain their records. The DIST-1 registry-rate clarification answers R1-opus-01. The DEPS.tsv hash updates and temporary STALE states accurately record the changed proof-file hash pending this check; they do not certify the new hash prematurely. The other exceptions are the version, changelog, review-trail, ERRATA and PINS changes named in the brief. No hunk changes a theorem display, lemma statement, selected constant or proof step. The added constant formulas are quotations of existing definitions/inequalities. D.0–D.6's proof steps, including the DIST-2 assembly, are unchanged.

Limits: this is the requested diff check, not a fresh audit of locked SOP:TH09, the sampler, all earlier reviews, or the Song–Liang comparison. I read DIST12.md in full and checked its repaired paragraph against X.md §0; I inspected the supporting proof passages for dependencies without claiming a new complete verification of each supporting lemma. I did not regenerate REPORT.md or execute mkreport.py's write path. No git command, agent, cluster job, scratch file or file outside the single authorized output was used.

R1-opus-01 RESOLVED.
Item 1(a) VERIFIED.
Item 1(b) VERIFIED — TC3 unchanged and proved as written.
Item 1(c) CONFIRMED — EQUAL on TC3; WEAKER on the descriptive sentence only.
Item 1(d) VERIFIED — no surviving free-A rate assertion; D5-01 records the separate local exponent-identification error.
R1-astra-01 RESOLVED.
Item 3 VERIFIED.
lemmas/DIST12.md as it now stands (DIST-1, DIST-2): VERIFIED-WITH-AMENDMENTS — D5-01, explanatory wording only.
Overall verdict: VERIFIED-WITH-AMENDMENTS; both council findings resolved; one MINOR finding, no CRITICAL or MAJOR findings.

MANIFEST 90c988397325835d176455ad7673506964a507e0ac1c004f477d1472e34ba5bd

Hunks: per file, classified (a)/(b)/(c).

The ranges below are exhaustive zero-context content-diff ranges, LC2 snapshot -> current (inclusive lines; an insertion is identified by its current lines). Line endings are normalised. Category (a) means a faithful review correction, including the three proof repairs independently checked below; (b) means a record/editorial change. There is no category (c) change requiring fresh mathematical review. In particular, a faithful correction to a proof's presentation is not being passed off as an unexamined proof change.

STATEMENT.md

1. 6-8 -> 6-10: (a), SC2-4's two opening corrections: the sufficient form generalises v1.3, and the unchanged conclusions are (C1)-(C4), with (C5)/dependencies updated. (b), append the SC2 check/disposition record. The correction has the meaning and scope requested by SC2, with no additional mathematical claim.
2. 114 -> 116; 167 -> 169-170; 170 -> 173; the symbol substitutions within 179-182 -> 182-185: (a), SC2-1, globally rename the Gaussian-row leak and its localised counterpart to varpi_n and varpi'_n (rendered in the source as the Greek symbols). The added explanation reserves ell_n for the method cap. Explicit nonnegativity at 169 is a convention already present in reviewed L4, not a restriction on the class: absolute-covariance upper envelopes may always be replaced by their absolute values, including when the relevant family is empty. The rates are preserved.
3. Remaining changes in 179-182 -> 182-185: (a), SC2-4's generalisation label and SC2-3's pointer to L4 section 7, item 1. The formula still has exactly 15r_n^2/c and the same rates.
4. 248 -> 251-252: (a)/(b), LC2-C finding 6 (the outside-object status nit): replace the unqualified example verification label by a pointer to each example's own status and conditions; add the check citation. This faithfully carries rather than upgrades those statuses.
5. 257 -> 261-262: (a)/(b), LC2C-1's permitted alternative: keep the proved range b<3/10 and record the reviewer's b=3/8 threshold sketch, pointing to SHARPNESS section 4. No extension or converse is asserted as proved.
6. 292-293 -> 297-298: (a), SC2-2's exact condition summary, apart from wrapping and the marker: (C1) conditional on SOP:TH09 only; (C2) on W2-APP:POST only; (C3) has no remaining below-PROVED-CHECKED external condition.

These six entries cover all eight zero-context hunks. The rename is complete: remaining ell_n occurrences are method-cap uses or the explicit historical/reservation explanation. Direct section-content equality checks confirm that section 1, (C1), and (C6), including all cap occurrences and code pins there, are unchanged.

ASSUMPTION_MAP.md

1. 33 -> 33: (b), the declared v1.4 record rewrite of A:L-gain-R / A:L-loc-R / A:H-size-rho. It records the already-reviewed all-conditioning-set leak, the product-form covariance difference, localisation's sample-error role, the unchanged reference-count budget, the harvested rate improvement, and the unresolved exact-scale leak. These agree with reviewed L4 sections 2, 3, 4 and 7 after the symbol substitution. Removing the obsolete 17/2-cutoff description from this row does not change a hypothesis or claim.

lemmas/L4_sandR_b.md

1. 3 -> 3-8: (b), the LC2-A verdict/stress-test record, and (a)/(b), SC2-1's notation explanation. Status remains PROVED (by this seat, unchecked); no mathematical promotion.
2. (a), complete SC2-1 leak rename, including the localised counterpart, at these old -> current ranges: 27 -> 32; 31-32 -> 36-37; 42 -> 47; 45 -> 50; 100 -> 105; 102 -> 107; 108 -> 113; 113 -> 118; 115 -> 120; 122 -> 127; 125 -> 130; 130 -> 135; 142-143 -> 147-148; 149 -> 154; 154 -> 159; 170 -> 176; 183 -> 189; 240-241 -> 246-247; 244-247 -> 250-253; 258 -> 264. Every such change is a symbol substitution only. The sole remaining old-symbol text is the historical explanation at line 7. In particular, no rate, coefficient, tail constant, lemma statement apart from alpha-renaming, or proof inequality changes.
3. 158-159 -> 163-165: (a), LC2A-1. The reviewer-requested independent innovation z=e/tau and conditional projected law replace the incorrect ambient independence assertion. This is a correct proof of the same spherical-tail step under the same hypotheses. See the proof check below.

These entries cover all 22 zero-context hunks.

lemmas/L5_formR.md

1. 3 -> 3-6: (b), LC2-B verdict/status record; the existing posterior condition is retained.
2. Insertion at current 50-53: (a), LC2B-1. It adopts the reviewer's mean-zero reduction, with synonymous wording for interpreting the latent extension on the centred row law. The statistics and population regression/covariance hypotheses are unchanged.
3. 59 -> 66-67: (a), LC2B-2. It discharges the empty pair family before log|P+|, takes the sure event and zero deterministic error, and then runs the original construction only in the nonempty case. The added parenthetical identifies the empty endpoint; it does not impose a new condition.
4. 148-149 -> 156-157: (a), SC2-1, all leak/localised-leak symbols renamed in the containment argument. The formula and rates are identical. No old leak symbol remains.

These are all four zero-context hunks.

lemmas/L6_examples.md

1. Insertion at current 3-6: (b), LC2-C check/status record, and (a)/(b), SC2-1's ASCII notation explanation. No example status is upgraded.
2. 9 -> 13; 20-24 -> 24-26; 128 -> 134; 474 -> 489-490: (a)/(b), LC2C-2. Replace stale STATEMENT line references by sections/claim labels, remove the stale 17/2 verification sentence, and replace the false v1.3 quote by the actual v1.4 status wording. Section pointers are accurate; the quoted status phrase agrees with current STATEMENT lines 4-5.
3. Insertion at current 67-69: (a)/(b), LC2C-5's requested finiteness explanation: D needs alpha>1, J needs alpha>2. It does not replace the existing proof or adopt the optional alternative 1+L0 bound. The series defining J has tail of order (log d/d)^(alpha-1), giving the stated cutoff; D has the ordinary alpha-series cutoff.
4. 104 -> 109-110: (a), LC2C-4's exact qualification: BM-infinity under N-chi, or BM-Q under N-D, implies BM-W. This restores the intended inherited-example record; no stronger example is claimed.
5. 155 -> 161-163; 253 -> 261-263; 462-463 -> 477-478: (a)/(b), LC2C-3. Both E2/E3 status lines now name BC and IR, their source locations, and their unchecked status; both table rows expressly say conditional on BC, IR. Their respective RM2-R/RM2-F conditions remain in place.
6. 186 -> 194; 188 -> 196; 191 -> 199: (a), SC2-1, complete ell_n -> varpi_n rename in E2. No formula, rate or radius changes. Remaining ell_n text is historical notation only.
7. Insertion at current 464-468: (a)/(b), LC2C-1, retain the proved range and record both halves of the reviewer's sketch as unproved, with an open-item pointer. This adopts the reviewer's explicit alternative of retaining 3/10 and recording the suggested threshold, rather than adopting the extension as a theorem.

These entries cover all 14 zero-context hunks. SHARPNESS.md is new, excluded from the five-pair diff as instructed.

Proof-text checks

- LC2A-1: e has iid centred Gaussian entries and is independent of (W_D, epsilon) by the already-reviewed population regression construction. Thus z=e/tau is independent of G-script. Given G-script, Pi is a fixed orthogonal projector of rank d, so Pi z has covariance Pi, squared norm chi-square_d, and projection N(0,1) along any G-script-measurable unit vector of its range. The following lower-norm event and scalar normal-tail bound require no independence between these statistics. Conditioning is not on E_cov; its use remains through the measurable CN_D bound. The same union bound and integration give the same (3.1), with unchanged constants and hypotheses. The replacement faithfully implements the exact correction.
- LC2B-1: C1=0, so subtracting the deterministic raw mean leaves CW and all standardised columns, sample projectors and Z statistics unchanged. Population covariances, regression coefficients and variances are translation invariant. The latent Gaussian representation is read on the centred row law as requested; its covariance/functionals contract is preserved. Population residuals then literally have the centred iid Gaussian law used in the existing chi-square calculations. No mean-zero design assumption is added.
- LC2B-2: on the empty family, every asserted memberwise inequality and definedness requirement is vacuous, so the sure event and error zero prove the same assertion. Otherwise log|P+| is defined and the original Steps 1-5 apply. No changed exponent or hypothesis is needed.

SC2-1 symbol deviation

Accept. L2_width.md section 4, line 185, already defines lambda_n=(n-1)phi_0^2 theta_min*^2/sigma^2 as the signal-floor quantity. Choosing varpi_n avoids that collision as well as the original method-cap collision. STATEMENT, L4 and L5 use the same Greek symbol and L6 uses its ASCII name; the primed localised counterpart and the sufficient formula are consistent. The historical notes identify the old draft notation. This is solely an alpha-renaming, with no method option or code pin change.

LC2C-1 scope

The E5 insertion explicitly calls the b<3/8 extension and b>3/8 positive-gap statement sketches and says neither is proved here. STATEMENT (C5) still verifies only 0<b<3/10, calls 3/10<=b<1/2 not verified, and attributes the suggested threshold to a reviewer's sketch. The table and unchanged not-claimed record do not promote that sketch. The wording accurately distinguishes the proved sufficient range from both unproved directions; no claim at b=3/8 is made. RESOLVED means the requested record action is complete, not that the open mathematical problem is solved.

Verdicts: one line per item.

The 13-item accounting uses LC2-A's two findings (its second duplicates SC2-3), LC2-B's two, LC2-C's five within-object findings, and SC2's four. LC2-C finding 6 is the supplementary outside-object nit, also implemented as recorded above.

LC2A-1: RESOLVED — exact conditional-law repair; same tail step, hypotheses and bound.
LC2A-2: RESOLVED — STATEMENT sufficient-form pointer is L4 section 7, item 1 (also SC2-3).
LC2B-1: RESOLVED — invariant centring reduction explicitly stated before the residual argument.
LC2B-2: RESOLVED — empty pair family discharged before logarithms.
LC2C-1: RESOLVED — optional record route adopted faithfully; wider range/converse remain sketches and open.
LC2C-2: RESOLVED — stale section references, historical sentence and false status quotation corrected.
LC2C-3: RESOLVED — BC/IR conditions and statuses carried by E2/E3 and both table rows.
LC2C-4: RESOLVED — BM-infinity implication explicitly restricted to N-chi; BM-Q under N-D.
LC2C-5: RESOLVED — D/J finiteness thresholds explained; optional alternative proof not required.
SC2-1: RESOLVED — complete consistent leak rename; varpi accepted instead of lambda for the verified collision reason; method caps untouched.
SC2-2: RESOLVED — exact corrected external-condition summary.
SC2-3: RESOLVED — corrected L4 section 7, item 1 pointer.
SC2-4: RESOLVED — all three historical/generalisation corrections applied faithfully.

ATTESTATION: editorial/record only — L4–L6 and STATEMENT v1.4 stand as reviewed in round LC2

Remaining required change: none.

Checks performed / not checked.

Performed: read the assigned brief first; read the four specified LC2/SC2 reviews and disposition; byte-level SHA256 verification of all five archived texts against their corresponding MANIFEST_LC2 rows (all match); SHA256 verification of the five current texts plus SHARPNESS against MANIFEST_SW1 (all match); exhaustive line-ending-normalised content diffs of all five pairs; review-item mapping for every changed hunk; independent checks of the three proof-text corrections; complete old/new leak-symbol occurrence checks; exact section-content comparisons for STATEMENT section 1, (C1), and (C6); L2 section 4 check of the existing lambda_n use. The manifest digest quoted above is the supplied first line, not a claim to have rehashed every manifest entry.

Not checked: a fresh proof review of unchanged material, proofs of external inputs, source code or numerics, REPORT/registry migrations, the full manifest outside the permitted source set, or a proof of either b=3/8 sketch. SHARPNESS was hash-checked only and is not certified here. No LOG, CHECKPOINT, unlisted review, or external source was read. No git command or git-state mutation was performed. No subagents were started. All work stayed inside the designated worktree, and only this review file was written.

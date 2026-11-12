MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a

Hunks: per file, classified (a)/(b)/(c).

Compared all ten archived/current pairs with GNU diff --strip-trailing-cr -u. Below, hunk headers are old (SW1) to new (R1), with three context lines. All ten archived SHA-256 values match their MANIFEST_SW1.txt rows; all ten current SHA-256 values match their MANIFEST_R1.txt rows. The archive is flat: lemma/numerics basenames map to the corresponding manifest paths.

Classification: (a) faithfully implements an exact SW1 correction; (b) record/editorial; (c) additional substantive change requiring a fresh review. A mixed physical hunk is broken into its logical changes below. The energy repair is (a), with mathematical content explicitly examined below; it must not be described as literally leaving the printed M range unchanged. No additional (c) change was found beyond that expressly requested, scale-equivalent repair.

STATEMENT.md - 2 hunks
- @@ -111,10 +111,18 @@: (a), SW1-1. Separates M > 0 from phi_0 in (0,1] and adds the requested response-rescaling argument, including the imported posterior hypothesis, unchanged method, invariant ratios and rescaled visibility sequence. The APP sentence supplies context for the existing use of an energy bound above 1.
- @@ -296,7 +304,7 @@: (b). Adds LOC2 before the L6_poly citation. No target line range, dependency status or mathematical assertion changes.

REPORT.md - 4 hunks
- @@ -21,22 +21,26 @@: (a), SW1-2, replaces the flag's asserted width violation with nominal width stress; (b), records SW1 findings/verification, BT2 recommendations and headline-strength-pending status; (b), adds CORE before the two code citations in section 2. Neither code pin changes.
- @@ -96,7 +100,10 @@: (b). Adds the RC5/SW1/BT2 rows and reserves the council row. SW1 counts and claim qualifications agree with the permitted sweep; RC5's attestation is reported in SW1_disposition, not independently authenticated from RC5 itself.
- @@ -112,8 +119,8 @@: (a), SW1-2. The registry discussion now reports nominal width stress and an observed improving addition, retaining 48/48 LS0 success.
- @@ -130,8 +137,10 @@: (b). Records recommended v1.5 work: BT2 P1-P5, P7 conditional on its proof closing, plus T2/T4. These remain recommendations, not adopted claims. This matches BT2_disposition; P6 remains deferred.

SHARPNESS.md - 3 hunks
- @@ -13,7 +13,8 @@: (a), SW1-6. Separates q sqrt(log n/n) -> 0 for entrywise sample floors from (q + log n)/sqrt(n) -> 0 for the additive comparison, with their separate sources.
- @@ -57,7 +58,8 @@: (a), SW1-2. Replaces certified width failure with a nominal design, explicitly uncertified (W) failure and nonzero leakage; the actual observation remains an improving addition at a probed set, with unchanged counts and LS0 scope.
- @@ -89,7 +91,7 @@: (b). O3-prime records BT2's non-sharp frontier sketch and leaves the sharp frontier open; O4-prime records the sketched 3/8 threshold. Neither is promoted to a theorem. The descriptions agree with BT2_disposition P6/P7; the two-reviewer provenance is a disposition record, not independently re-audited here.

ASSUMPTION_MAP.md - 4 hunks
- @@ -1,11 +1,11 @@: (a), SW1-4. Updates v1.3 to v1.4, distinguishes historical updates from current proof/status records, and removes "Nothing is proved yet." Implementation and posterior qualifications are retained.
- @@ -13,7 +13,7 @@: (a), SW1-4. Replaces the obsolete TL toolkit description with the exact two-square identity and truth-removal width in L2 section 4. The adjacent NA sentence and existing (W) requirement remain; the row does not claim TL without the supplied addition envelope.
- @@ -36,7 +36,7 @@: (a), SW1-4. Replaces the W-conv "target" with the completed lemma reference.
- @@ -61,7 +61,7 @@: (b), also consistent with SW1-4. Removes stale "planned."

lemmas/L1_sandF_b.md - 1 hunk
- @@ -18,7 +18,8 @@: (a), SW1-1. Changes the energy constant's declared range to M > 0 while retaining phi_0 in (0,1]. No proof line changes. See the scaling check below.

lemmas/L5_formR.md - 2 hunks
- @@ -49,7 +49,7 @@: (b). Gives LOC2 and the lemmas/ prefix for the centering-template citation.
- @@ -83,8 +83,8 @@: (b). Gives LOC2 and full paths for both Step 5 template ranges, including the formerly abbreviated continuation. Every inequality, range and proof step is unchanged.

lemmas/L6_examples.md - 3 hunks
- @@ -25,6 +25,11 @@: (a), SW1-1. Points E3-E5's M > 1 choices to the new scaling argument, retaining the advertised fixed signal ranges.
- @@ -448,7 +453,7 @@: (a), SW1-7. Changes "unshifted width" to "width gap"; the displayed shifted bound and b < 3/10 range are unchanged.
- @@ -489,11 +494,12 @@: (a), SW1-5. Removes the obsolete numerical pin in favor of section 5, states that B9 is not consumed and identifies the local p=1 proof. The ledger retains the conditional imports through the respective theorem. Together with E2's explicit RM2-R + BC/IR status, E3's RM2-F + BC/IR status, and REPORT's named posterior conditions, this correctly means E2 depends on APP:POST + BC/IR, E3 on SOP:TH09 + BC/IR. A section reference instead of another brittle numerical pin is sufficient.

numerics/SPEC.md - 2 hunks
- @@ -10,7 +10,12 @@: (a), SW1-3. Discloses tolerance, cap return and tie departures; labels capped final_size as the current centre's size and disclaims validation of these branches.
- @@ -31,7 +36,7 @@: (a), SW1-2. Replaces an isolated certified width failure/untouched-leakage assertion with a heuristic design, uncertified realized width failure, the correct conditional covariance and a non-isolation disclaimer.

numerics/RESULTS.md - 1 hunk
- @@ -92,7 +92,14 @@: (a), SW1-3 and SW1-2. States the three simulator departures, the capped-centre interpretation and one-neighbour size observation; adds the nominal-width and nonzero-leakage qualification and defines observed NA violation. No table, outcome or numerical value changes.

numerics/rm2_common.R - 2 hunks
- @@ -6,7 +6,7 @@: (a), SW1-3. Comment replaces "exactly as coded" with re-implementation and the SPEC departure reference.
- @@ -108,7 +108,8 @@: (a), SW1-3. Comment states the tolerance and cap-return distinction. All added/deleted lines in both hunks are comments. Independently removing full-line comments from both versions leaves identical line sequences, including all executable code and numeric literals.

There are 24 physical diff hunks. These account for all ten pairs; no further changed hunk was found.

Energy check (SW1-1)

Take a fixed a > 0, with a = B^(-1/2) when B > 1, and couple eps' = a eps, Y' = aY, theta' = a theta*, sigma' = a sigma. Then s_y' = a s_y and y' = y almost surely. L0 section 0 defines the D0 score using X, y and n; its 0.02 term is in standardized-response units and does not spoil this invariance. Model-common likelihood constants do not affect score comparisons or normalized posterior probabilities. The prior and feasible model space depend on p, n, size alone. Thus block ratios r_b, gamma_0, all its maximizers and normalized start law are identical. With the same run randomness and configuration, the method's score-based choices, LS0 comparisons/ties, path, cap and reporting objects agree. The X-measurable partition is unchanged. This is an exact mathematical invariance under the retained implementation premises, not a new numerical floating-point guarantee.

For every U,l: mu' = a mu, delta' = a delta, Lambda' = a^2 Lambda, tau_U'^2 = a^2 tau_U^2 and Z' = Z. Therefore:
- (V) and its block version hold with M_n' = a^2 M_n -> infinity. They are preserved as existential sequence conditions, rather than with the same numerical witness.
- (L-gain), its block version and eta are unchanged since delta^2/tau_U^2 is unchanged.
- (BM-W), (BM-Q), BM-infinity and theta_min^2/sigma^2 are invariant.
- Support, s0, X, Q, feasibility, Gram floors, widths d_n and w_n, and all size/entropy budgets are unchanged.
- The energy bound becomes ||mu'||^2 <= a^2 B n <= n. The noise variance remains fixed and strictly positive.

In the permitted GROW lines 84-88, the other H0/T1-F requirements are R1, the truth Gram floor, SE_lambda(j0), SE_w(m_sharp;g0), and BM-infinity. The first four depend on X, support, n, p and the size prior only; the last is the invariant signal/noise ratio above. There is no further absolute response scale requirement there. APP lines 28-29 do use M = s0^2 theta_hi^2 + 1, as the remark says. Choosing energy envelope M' = a^2 M also keeps L0's c_E and kappa_E unchanged, while C_R scales by a^2.

Domain qualification: the printed hypothesis M <= 1 is literally broadened to M > 0 in STATEMENT and L1. It would be inaccurate to call that merely a typographical edit with no domain effect in raw units. However, it introduces no new standardized-data or signal/noise case: every newly admitted sequence is the inverse image of a restricted-energy sequence under the exact fixed scaling above. This is precisely SW1 finding 1's explicit correction, including its requested justification, checked here rather than silently assumed. Accordingly it is classified (a), not an additional unreviewed substantive revision (c). The attestation below uses "stands as swept" subject to this expressly requested and now verified repair, not a claim that the literal M domain is unchanged.

Numerical-record checks (SW1-2, SW1-3)

For independent unit Gaussian H, E_t, W, set P_t = rH + sqrt(1-r^2) E_t and O = sqrt(1-s) W + sqrt(s/m) sum E_t. Var(P_t)=1, Cov(O,H)=0, Cov(O,P_t)=sqrt(s(1-r^2)/m), Cov(P_t,H)=r. Gaussian conditioning gives

    Cov(O,H | P_t) = 0 - sqrt(s(1-r^2)/m) r,

exactly the displayed expression. It is nonzero for the probe's nondegenerate parameters and vanishes with growing m (r is bounded). This demonstrates failure of exact zero population leakage. It does not certify the full conditional leak budget over every allowed U or a sample-design/asymptotic width violation. SPEC's "positive leak" is read as a positive leakage magnitude, not the sign of that negative covariance. The express "nominal" and "not isolated" qualifications, reinforced in RESULTS, SHARPNESS and REPORT, are sufficient. RESULTS section 2's retained whole-lattice-event failures are observed finite-sample NA failures, not certifications that (W) fails. Counts, LS0-only scope and the historical 207-to-208 reconciliation are unchanged.

Production v3_engine.h:392 gives lexicographic equal-score ties, :394-406 the complete feasible scan, :408 strict improvement, :409-410 return of the best improving neighbour at the cap, :413-414 certification otherwise. R's current lines 135-147 use which.max/category priority, improvement > tol (default 1e-9), and break at the cap before modifying S, returning S. Thus all three documented departures are accurate. "First maximum" describes the simulator's ordering, not production lexicographic ordering. The four recorded capped centres (SW1 reports sizes 60,22,11,6, s0=2) cannot reach S0 in one flip/swap because a neighbour reduces size by at most one. This is a size observation, not a claim that a full production rerun follows the identical earlier path.

Verdicts: one line per item.

SW1-1: RESOLVED - requested scale-equivalent energy extension justified; literal-domain qualification above.
SW1-2: RESOLVED - nominal width stress, observed NA failures and nonzero conditional leakage correctly distinguished.
SW1-3: RESOLVED - all three implementation departures and capped-centre sizes disclosed; executable R unchanged.
SW1-4: RESOLVED - assumption map describes current proofs while retaining conditional statuses.
SW1-5: RESOLVED - stale pin and consumed-B9 record removed; respective posterior and BC/IR conditions retained.
SW1-6: RESOLVED - sample-floor and additive-comparison rates separated correctly; both vanish for fixed b < 1/2.
SW1-7: RESOLVED - shifted quantity correctly called a width gap.

ATTESTATION: editorial/record only — the package stands as swept in round SW1

Checks performed / not checked.

Performed: read the assigned brief first; verified the twenty scoped text hashes against the two manifests; diffed all ten pairs with --strip-trailing-cr; reconciled every changed hunk with the exact sweep corrections and permitted dispositions; checked the energy argument against L0 section 0 and the permitted GROW/APP lines; derived the B2 covariance; compared the LS0 disclosures with the permitted production lines and unchanged R code; checked the two Gaussian-row rates against permitted L5; checked BT2 record wording against BT2_disposition. No remaining required text correction.

Ran from the worktree root: python Theory_work/Wave3/W3-RM2/citecheck.py (exit 0). First line:

    W3-RM2 citecheck: 92 citations extracted from 12 files; 0 MISS

This is syntactic citation resolution/range checking, not certification of every citation's meaning. The authorized checker overwrote reviews/CITECHECK.txt; its own source-reading scope is broader than the manually inspected corpus. No logs, checkpoints or unpermitted review texts were manually read. No external source, simulation, production build, or full proof re-sweep was attempted. The unchanged numbers were compared through the diff and the permitted sweep, not re-aggregated from the unpermitted CSV. Transitive posterior proofs and implementation premises retain their recorded conditional status. No git command or git-state change, no subagent, and no effort setting above high was used. Apart from the explicitly authorized citecheck output, this review is the only file written.

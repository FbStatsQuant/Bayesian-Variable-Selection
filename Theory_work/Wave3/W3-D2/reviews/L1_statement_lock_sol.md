LOCK-WITH-AMENDMENTS

Fresh, blind statement-lock review of STATEMENT v1.0. I read the brief and its requested inputs, including the proof route, PROGRAM's Readability rule, and the inherited rider rules. To resolve the vanishing-floor wording I also checked W2-APP/lemmas/L1_POST.md:20–25. I did not read LOG.md or open the registry. Registry statuses below are taken from the brief. No mathematical obstruction to Theorem 2X or Corollary 2X was found. Amend the reader presentation and qualify the old-master comparison before locking.

## Findings

**L1-1 [E] — The headline theorem still contains proof-interface notation and internal references.** STATEMENT.md:26, 39–43 (also the setup's file-based posterior definition at 22–24). The primitive assumptions (A1)–(A3) and the single display at 35–38 are a clean core reader statement. However, the following “Explicitly” paragraph introduces k_n, j_0 and m-sharp through an internal file reference, although these are proof cutoffs rather than quantities needed to understand the result. The title also contains a ticket/claim id. PROGRAM.md:23–37 expressly sends constants and secondary clauses to remarks, disallows new notation beyond the setup, and excludes internal ids from reader text. The current theorem therefore does not fully meet the requested reader standard.

Fix: keep (A1)–(A3), the probability-law clause, and the four bounds in the single conclusion display. Move lines 39–43 unchanged in mathematical substance to a technical remark or master-bound paragraph outside the registered reader span; retain the checked constant-dependence statement there. Remove the ticket/claim id and “from the omitted-variables master” from the reader-facing title. For a standalone reader copy, define the coded posterior in ordinary setup text (or use the existing reader setup) rather than requiring access to [W3P]. In §2, “four bounds” is more accurate than “four displays.” This is a presentation amendment, not a defect in those bounds.

**L1-2 [F] — The vanishing-floor caveat omits the old master's separate fixed small-set floor.** STATEMENT.md:64–65 and 91–92; corresponding compressed comparison in TARGET.md:20. The caveat correctly says that the new result does not retain the old master's vanishing floor on its larger sets. But read on its own it does not give the complete old hypothesis: LSF(i) still requires a fixed positive floor on every set of size at most min(p, s_0+j_0), while only LSF(ii), on sets up to k-bar_n, permits the slowly vanishing psi_n. Thus “the old master allows a vanishing floor” must not be read as allowing the floor to vanish on all required sets.

Fix: replace remark (b) by wording such as: “The old master retains a fixed positive floor on sets of size at most min(p,s_0+j_0), but permits the floor psi_n on the larger range |S| <= k-bar_n to vanish provided psi_n sqrt(n)/(log n)^(3/2) tends to infinity. Theorem 2X instead requires a fixed positive floor throughout its required range |T| <= k_n (and (A2) imposes it through the convenient 3(A+1)(s_0+1) log n upper bound). Neither master dominates the other solely on these floor hypotheses.” Carry this qualification into §7 and the TARGET comparison. The STRONGER tag remains correct against the specified constant-floor reader statement, not against every extension in its master.

## Hypothesis audit and q = 0

Every hypothesis of CorGb-plus is supplied by STATEMENT §0 and (A1)–(A3), eventually in n; no extra substantive assumption is needed.

- Use candidate set [p], q=0, the n-by-0 omitted matrix and the empty coefficient vector. Their product is the zero vector. Constant maps a=0, gamma=0, tau-squared=0 satisfy (OV), because its conditional law is the point mass N_n(0,0). This is explicitly admissible: MISR-R:52 allows q >= 0 and :31 defines the degenerate Gaussian. Noise independence in (N) is exactly the independence in §0. The effective coefficient and variance are beta and sigma-squared.
- Gaussian candidate rows, positive marginal variances, deterministic coefficients and positive deterministic noise variance are stated in §0. Dependence of these parameters on n is permitted by the master. The intercept causes no additional restriction.
- A1 supplies polynomial dimension and fixed positive support size. Since s_0 <= p and s_0 is fixed, s_0 <= K eventually (n >= 2s_0). This eventual restriction belongs in n*, not in an additional asymptotic assumption.
- R1 B4.1 then gives k_n <= 3(A+1)(s_0+1) log n, so A2 covers every nonempty principal block used by the master. Empty-set eigenvalues need no convention in the new statement: the master's proof only uses nonempty sets (G2_corr.md:29–34).
- A3 is exactly the relative energy bound and the divergent relative beta-min branch. Divergence implies the master's required strict liminf threshold for any fixed c > 0. The setting already says s_0 is the actual support size; the fixed-s_0 clause in §1 overrides the general permission for parameters to vary with n.

## Conclusions, quantifiers and explicit constants

All four asymptotic bounds and all four explicit inequalities are valid. Write d_n=(2+2k_n)n^(-2)+n^(-1). CorGb-plus gives E delta_n <= C r_n+d_n and HPM error probability <= 2C r_n+d_n. The proposed b_n=C r_n+d_n therefore gives its asserted HPM bound 2b_n, with harmless slack. Pointwise PIP error <= delta_n gives the PIP expectation bound. Each selection error implies delta_n >= 1/2, so Markov gives both selection error bounds <= 2b_n, including arbitrary measurable HPM tie selection and the stated strict-threshold MPM convention.

The constant dependence is correct on the divergent branch: choose the master's beta-min constant c_0(s_0,A)+1. Its MIS-R constant then depends only on (s_0,A,M_0,c), with C_OS depending only on (s_0,A). The onset n* can depend on the sequence, including how late the beta-min condition takes effect. No uniform onset over all such sequences is asserted. R1 gives k_n=O(log n), and d_n=o(r_n), proving the advertised rate. There is no unstated fixed-variance or bounded-diagonal assumption.

## Corollary fidelity and deterministic parameters

The recorded hypotheses at RV:263–270 and S1–S2 at :28–29 are faithfully reproduced. With unit diagonal R=Sigma_n, the size-5 floor implies the size-3 floor. For the active correlation block, lambda_max <= trace = s_0 and ||beta||^2 <= s_0 b_hi^2, whence beta-transpose Sigma_n beta <= s_0^2 b_hi^2. This proves the stated M_0; the beta-min lower bound also follows exactly. No upper eigenvalue bound beyond this elementary active-block bound is needed.

The recorded model uses alpha-star and beta-star as nonrandom parameters. NOTATION.md:15–27 presents a parametric Gaussian linear model; :37–43 identifies the standardized coefficient's randomness as coming through the sample scaling D. It does not literally use the word “deterministic” for the raw parameters, so PROOF.md:59 is a reading of that model convention, not a verbatim quotation. That reading is consistent with the recorded fixed-signal setting and its old-master raw-slope convention (L1_POST.md:12–15). It introduces no new hypothesis relative to that setting. Markov and a union bound give all three recorded conclusions. Replacing 5 by 3 in the corollary's floor hypothesis leaves this argument intact.

## Strength and status comparison

STRONGER is correct against precisely RV:263–275 / card row 1.2's reader statement: its hypotheses imply the new ones; the new conclusion includes expectation bounds and explicit selection-error rates; the required set range is smaller. General marginal variances and n-dependent relative signal/noise sequences also enlarge the permitted setting. The recorded coefficient bounds already allow a conventional sequence of bounded nonrandom coefficients; do not describe the gain as merely allowing any n-dependence in beta. The substantive gain is replacing the fixed absolute lower/upper signal restrictions with A3's relative conditions.

No other loss against that reader statement was found. Fixed s_0, Gaussian rows, polynomial p, and positive noise variance are shared. The new conditional proof status must remain visible, as must the incomparability with the old master's vanishing-floor extension, qualified by L1-2. The brief's quoted conditional input statuses and the unchecked Prop-LB ancestor are accurately carried in §5; a statement-strength tag does not discharge them. The new result does not claim every ancillary conclusion of the old master, nor does §7 assert that it does.

## Interpretive sentences inside §§1–2

The inferential text was checked as part of the claimed spans:

1. §1:39–42, “Explicitly: there are C ... and n* ...” plus the b_n inequalities — **CHECKED**, by the constant and deterministic-bound audit above; move outside the reader span for L1-1.
2. §1:43, “and k_n = O(log n), so b_n = O(r_n)” — **CHECKED**, by B4.1 and d_n=o(r_n); move with the explicit paragraph.
3. §2:50–51, “Then (A1)–(A3) ... hold with c := ... M_0 := ... and rho_n >= ...” — **CHECKED**, by the correlation-block energy and beta-min calculations above.
4. §2:51–52, “Hence the four displays ... hold, and with them the three conclusions ...” — **CHECKED**, by Theorem 2X, Markov, and the union bound. Change “displays” to “bounds.”
5. §2:53, “The same holds with the floor asked only on ... 3 ...” — **CHECKED**; under that replacement the floor is directly A2. It may stay in the corollary.

The remaining prose in these spans states the assumptions, probability law, or named conclusion, rather than adding an unchecked interpretation. No additional “this means” or necessity reading occurs there.

No scratch directory was created; no scratch cleanup was needed. Only this review file was written. No git state-changing command was run.

LOCK-WITH-AMENDMENTS — 2 findings: C=0, S=0, F=1, E=1.

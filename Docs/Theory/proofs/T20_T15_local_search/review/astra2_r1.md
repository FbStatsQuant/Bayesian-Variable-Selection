The proof establishes STATEMENT.md §§3–4 under the stated hypotheses. I found no fatal errors or gaps.

The verification is as follows:

- **Basic invariant.** Each centre has already been scored and attains the largest score seen before its scan. Selecting the highest-scoring strict improvement preserves this invariant and strictly increases centre scores. The conclusions for NOIMP and LIMIT follow correctly.

- **Certificate semantics, (i-a).** A certified returned model must be the final centre of a NOIMP execution. The converse holds. The argument concerning centres of earlier searches correctly uses the cumulative scored set and the HPM total order. Exact ties are handled correctly.

- **Unscored scores, (i-b).** The induction establishes that changing scores outside the final scored set leaves the local execution and both flags unchanged, with the input and tie rules fixed. The nonglobal-maximality argument correctly requires an unscored model. If every model has been scored, global maximality follows separately from the exhaustive ledger; this does not contradict the certificate’s general local meaning.

- **Ledger, final scan, and uniqueness, (i-c)–(i-e).** Every scanned candidate enters the HPM comparison. On LIMIT, every final score maximiser strictly exceeds all scores recorded before the final scan. Consequently the returned model is newly scored, has never been a centre, and is uncertified. Uniqueness of the scored maximum gives the claimed equivalence between certification and NOIMP.

- **One-neighbour result, (ii-A).** Neighbourhood symmetry ensures that the scan scores \(S_0\). On \(E_n\), its strict global superiority forces its selection whenever a move remains. The subsequent scan terminates with certification. At the move limit, \(S_0\) becomes the returned HPM without certification. Its subsequent persistence as HPM is also justified.

- **Margin and statistical results, (ii-B)–(ii-C).** The positivity argument for the marginal scores remains valid for rank-deficient designs. Comparing total posterior mass outside \(S_0\) with the largest competing posterior mass gives \(\Delta_n\ge\lambda_n\) in the correct direction. H03 yields both \(P_0(E_n)\to1\) and the stated positive-part tightness bound. The simultaneous algorithmic conclusion follows pathwise on \(E_n\), without independence between data and algorithm randomness.

The final inner-probability parenthetical is unnecessary for the usual measurable randomized-algorithm interpretation: the scan conclusions involve Borel score comparisons and countably many transcript coordinates, so their simultaneous event is measurable. It does not invalidate the ordinary probability conclusion.

STATEMENT.md §§3–4 is a faithful precise reading of the quoted original clauses using the interpretations recorded in §5. In particular, it distinguishes the returned running HPM from the last centre and preserves the distinction between weak local maximality and strict improvement. The statistical conclusion is explicitly conditional on H03; the proof does not claim to establish H03 or the referenced T03 from the underlying statistical assumptions.

**Verdict: verified**

MANIFEST d09644f5cb8d319a54bd11ae80aedfa97fd1d91f06daac635083f9301a4935f1
Verdict: LOCKED (editorial only; all findings resolved)

Paths below: S = Theory_work/Wave3/W3-START2/STATEMENT.md; B = Theory_work/Wave3/W3-START/STATEMENT.md; PLAN and reviews are under W3-START2. Line numbers refer to the current files unless explicitly marked old.

Findings table:

| SL1 item | Verdict | Evidence and assessment |
|---|---|---|
| R1 | RESOLVED | S:10?14,58,161?162. The header expressly asserts no proof status, identifies sketches and proof destinations, and replaces the claims that proofs are supplied/author-proved. ?Proof file? identifies a destination without certifying existence or completion. Read under that explicit convention, the P1?P4 references (including S:208) do not certify supplied or author-proved changed proofs. The non-vacuity construction is identified as a sketch. |
| R2 | RESOLVED | S:25?28 correctly lists five changes: L-R (B:163?167 versus S:63?73); F2 growth (B:272?275 versus S:112?117); OVL visibility (B:339?344 versus S:181?189); N2 premise (B:318?324 versus S:156?166); and the transfer rate-envelope hypothesis (B:298 versus S:127?133). Each is a changed hypothesis, not merely a changed conclusion. No additional changed hypothesis of a replacement claim was found. In particular, OVL's explicit cardinality bound S:182 was already required by AL and the lattice domain (B:80?81,152?153); IF-START's changed rate is a conclusion, not an extra premise. LEAK-0 is new, not a replacement with an unlisted changed hypothesis. ?Gaussian-row rate? avoids incorrectly preserving the fixed-design leading rate. |
| R3 | RESOLVED | S:140?144 supplies a separate, constant-dependent split for the polynomial-logarithmic rate, without identifying it with the exponential rate. It works at each index of any deterministic sequence with cardinality at most K; see the calculation below. |
| R4 | RESOLVED | S:198?199 restricts the infinite-expectation assertion to the Gaussian envelope. Indeed E exp(Z?/2) = (2?)^{-1/2} integral_R 1 dz = infinity. It no longer asserts an infinite first moment for finite-n coded odds. |
| O1 | RESOLVED | PLAN.md:25 uses max(0,16?s?), retains the at-most-15 bound for s? ? 1, and correctly states emptiness for s? ? 16. |
| O2 | RESOLVED | S:59 explicitly repeats s? ? 1 and p > s? for the implication 1/p ? 4??^?_n(h). |

For R3, fix a probability tolerance ?. The base bridge gives a design set with failure limsup at most ?/4 and ?_n(Q) ? D_? b^Q_n (BASE lemmas/L9_BR.md:144?145,168?169; S:147?152). Apply S:101?105 with tolerance ?/4 and ? = 1, using the Gaussian bridge's visibility exponent 3/2 (BASE lemmas/L9_BR.md:158). Choose T_? ? max(2,D_?/c?(?/4),2C(?/4)D_?). At indices T_? b^Q_n ? 1 the tail event is empty. At the other indices ?_n(Q) < D_?/T_? ? c?, and C?_n(Q)+n^{-1} ? T_? b^Q_n eventually, since n^{-1}/b^Q_n ? n^{-1/2}(log n)^{?15?_Q?1/2} ? 0. The conditional error, vanishing default tail budget, and design failure give tightness. No eventual dichotomy or convergence of b^Q_n is assumed. The symbol b^Q_n also avoids collision with the imported tail budget b_n(h).

Differences (exhaustive, grouping adjacent wording/reflow edits):

1. Editorial ? S:4: v1.4.0 becomes v1.4.1.
2. Editorial ? S:10?14 (old:10?13): accurate delta inventory, including replacement of L-R and addition of LEAK-0; supplied/author-proved wording replaced by the status-neutral convention and sketch/status locations.
3. Editorial ? S:25?28 (old:24?25): ?its rate? becomes ?its Gaussian-row rate?; the incorrect blanket hypothesis-preservation assertion becomes the five-item inventory checked in R2.
4. Editorial ? S:58?61 (old:55?57): ?proved in? becomes ?proof file?; the qualification on 1/p is repeated; the final sentence is reflowed. Its inequalities and factors are unchanged.
5. Editorial ? S:140?144 (old:136?138): the incorrect shared-triviality explanation becomes the per-index exponential observation and separate C_L=0 threshold argument. The new local rate abbreviation changes no theorem rate or constant.
6. Editorial ? S:161?166 (old:155?159): the assertion that P3 gives a design becomes a PLAN sketch reference and proof destination; the remaining scope explanation is reflowed without changed substance.
7. Editorial ? S:198?199 (old:191): the false first-moment explanation is replaced by the correct Gaussian-envelope explanation. The ? dependence and scope exclusion are unchanged.
8. Editorial ? PLAN.md:25: the supplied previous inequality 16?s? ? 15 becomes max(0,16?s?) ? 15. This repairs the sketch for s? > 16; the statement already had the valid at-most-15 bound (S:87).

Attestation: editorial only. None of these differences changes a definition, assumption, hypothesis, conclusion, constant, or scope of any claim in ?2??5. The hypothesis changes described in item 3 were already present in v1.4.0. No new wrong reference, symbol clash, or false sentence was found in the edits. No substantive re-review is required by this diff.

Required changes: None.

Verification: the expressly permitted manifest command returned `verify: OK MANIFEST d09644f5cb8d319a54bd11ae80aedfa97fd1d91f06daac635083f9301a4935f1`. The archived v1.4.0 SHA256 is `0128495d8955383ef23f068008c5750f7a528d03084598769cc795a1bc22a029`, matching the brief. Compared the complete archived/current statements with Python difflib. No git command or subagent was used; this report is the only file written.

Not checked:

- Completed P1?P4 proofs, which are outside this statement reconciliation.
- Independent re-proving of unchanged base claims, implementation/code pins, or floating-point behavior.
- Lifecycle/acceptance records, LOG, CHECKPOINT files, base reviews, or other prohibited material. Status references are not independently certified.
- A full manifest-content audit beyond the authorized verifier; the PLAN comparison uses the previous line supplied in the brief.

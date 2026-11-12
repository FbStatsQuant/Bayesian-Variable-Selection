MANIFEST b643f323a2ac2948975e3f01e54d30c0e64cf6643eebe911d1475fac270c3dc6
Verdict: ACCEPT WITH CHANGES

The intended weakening passes: the old Form R assumptions imply the new ones, with the stated constant 15/c. No Form F hypothesis, code pin, or conclusion of (C1)–(C4) changes. Acceptance requires findings 1–4 below. In particular, the leak sequence must not share the globally defined LS0-cap symbol. This is a statement-change check, not certification of the lemma proofs.

Hunks: numbered, classified (a)/(b)/(c).

Ranges below are the exhaustive zero-context diff hunks, written old -> new. Classification (c) explicitly flags changes beyond the leak inequality itself, even where justified by the permitted records.

1. Lines 4 -> 4–9: (b), version/history and proof-status introduction. It records P3/T6, examples, dependencies and REPORT pointers. Two phrases overstate literal identity: the sufficient form generalizes rather than reproduces v1.3, and (C5) does change. See finding 4.
2. Lines 108–109 -> 113–114: (a), replace C_L by a leak sequence; (c), change the constant range from rho >= 0 to rho > 0. The latter is harmless asymptotically but is a real change and should be acknowledged. If l outside Q exists, H_l contains at least l and one truth, so rho = 0 was impossible already. If Q = [p], the leakage conditions are vacuous and any sufficiently small positive rho satisfies the strict budget. There is no lost design case when constants can be chosen anew. The new leak symbol collides with the cap symbol: finding 1.
3. Lines 161–165 -> 166–182: (a), replace localised leak O(n^(-1/2)) and the strong localisation rate by all-conditioning-set leak o(sqrt(log n/n)) and r_n -> 0; add explanation and the sufficient localised form. The implication and 15/c are correct. The description and cross-reference need findings 3–4; notation needs finding 1.
4. Line 211 -> 228: (b), (C4) explicitly supplies the parent RM-R leakage hypothesis through the sufficient form. This changes the explanation, not the containment conclusion. The parent conditions do imply the replacement; see derivation below.
5. Line 226 -> 243: (b), append the P7 proof-mechanism record: covariance-difference/product form, comparison on sqrt(h), and o(sqrt(log n)) mean shift. It matches L4 section 7 items 2–3. The bridge's interface and numeric budget are otherwise unchanged; its imported L-R^b changes as in hunk 3.
6. Lines 229–241 -> 246–262: (c), P10 changes its source from RM B9 to W2-APP:POST for p >= 2 plus an internal p = 1 argument. This is a substantive dependency/bridge-source change, supported by L5 sections 3 and 5, with no changed POST conclusion. (b), the rest of the hunk replaces the (C5) example record: corrected polynomial-decay radius, explicit separation and fixed signals, a new weak-proxy witness, equicorrelation verified only for b < 3/10, and Form R cutoff reduced to alpha > 2 with logarithmic H_l. These are substantive changes to the example record, expressly within the assigned record update; they are not additional assumptions of (C1)–(C4). They match the L6 examples table, including the unverified range.
7. Lines 269–274 -> 290–294: (c), remove B9 and W1-GEN:L1 as external conditions, add Lemma-BC to the source list. These dependency changes are supported, respectively, by L5 sections 3/5 and the L0 self-contained header. SOP:TH09 remains a condition of C1 and W2-APP:POST remains a condition of C2; neither is a condition of C3. The written sentence contradicts itself on C3: finding 2. The new BC input concerns examples only.
8. Line 276 -> 296–297: (b), distinguish proof templates from the IR/BC conclusions consumed by examples E2/E3; carry their statuses rather than silently upgrading them. This matches L6's sources/statuses record.
9. Lines 289–290 -> 310–314: (b), update the not-claimed record to alpha <= 2, removal of localisation, exact-scale leak, reducing reference exponent 15, and equicorrelation beyond b < 3/10. Consistent with L4 section 7 and the L6 table. No stronger sharpness or necessity claim is added.
10. Lines 295–362 -> 319–324: (b), replace the draft registry block by a REPORT pointer, retain the old block in the CP2 snapshot, and describe the intended migration. This is a relocation/status record, not new theorem content. Actual REPORT content and preservation of every migrated edge are not checked: REPORT is outside this brief's permitted inputs.

There are no other diff hunks. In particular, section 3.1, the statements of C1–C3, all numeric width/signal constants there, and section 1's code pins are unchanged. C4 has only the containment explanation added in hunk 4. The endpoint rho change and the dependency-source changes are the additional substantive changes flagged above; none invalidates the intended extension.

Derivation of v1.3 => v1.4.

To avoid the symbol collision in the source, write lambda_n for the NEW leak sequence, retaining ell_n for the LS0 cap. Fix l outside Q and U subset [p] minus {l}, |U| <= 15. Let U0 = U intersect H_l and V = U minus H_l. Since S0 is a subset of H_l,

    S0 minus U = S0 minus U0.

Thus U may contain other truths; the tested j is any member of S0 minus U. Every such j is also in S0 minus U0, exactly the domain of the old localised bound. If all truths are already conditioned on, this quantification over j is empty, as it should be.

For V nonempty put

    A = Cov(W_V, W_V | W_U0),
    a_l = Cov(W_V, W_l | W_U0),
    a_j = Cov(W_V, W_j | W_U0).

The FL-R floor applies to Sigma_U (|U| <= 15). Its Schur complement A has lambda_min(A) >= c: for any z, z'Az is the minimum of (x,z)'Sigma_U(x,z) over x, which is at least c||z||^2. Consequently ||A^(-1)||op <= 1/c. The old localisation inequalities give ||a_l||2, ||a_j||2 <= sqrt(|V|) r_n. The Gaussian conditioning identity yields

    Cov(W_l,W_j | W_U)
      = Cov(W_l,W_j | W_U0) - a_l' A^(-1) a_j,

and therefore

    |Cov(W_l,W_j | W_U)| <= ell'_n + |V| r_n^2/c
                             <= ell'_n + 15 r_n^2/c = lambda_n.

For V empty the correction is zero, so the same bound holds. This proves the sufficient form with exactly the advertised constant, not an unspecified multiple.

Under the stated sufficient rates,

    lambda_n sqrt(n/log n)
      = ell'_n sqrt(n/log n)
        + (15/c) [r_n (n/log n)^(1/4)]^2 -> 0.

Also r_n -> 0, so L-loc-R holds with the same H_l and sequence. The sufficient form must retain the displayed localisation inequalities, the neighbourhood-size requirement, size/feasibility and the floors; read as a replacement of the leak/rate clauses within L-R^b, it does so.

For literal v1.3 take ell'_n = C_L n^(-1/2). Its scaled value is C_L/sqrt(log n) -> 0. Write d_n = r_n(n log n)^(1/4) -> 0 (this d_n is local to this calculation, not the truth-removal width). Then

    r_n^2 sqrt(n/log n) = d_n^2/log n -> 0,
    r_n(n/log n)^(1/4) = d_n/sqrt(log n) -> 0.

Hence v1.3 implies the sufficient form and then both new leak/localisation clauses. Q, H_l, feasibility and b are unchanged; rho may be taken positive as explained in hunk 2. Every other assumption of C2 is unchanged. Thus the v1.3 C2 is a special case of the intended v1.4 C2.

The same reasoning proves the new explanation in C4: parent RM section 3.2 has precisely the old localised leak and stronger r_n rate, and polylogarithmic Q/H_l fit n^b/n^rho for small positive constants with 15rho+b < 1/2. The W-R containment route is unchanged and is recorded in L5 section 4.

Findings: numbered; CRITICAL / MAJOR / MINOR, each with the exact correction.

1. MAJOR — Colliding leak and method-cap sequences (STATEMENT lines 52, 114, 167–181). Section 1 globally defines ell_n = ceil(log2(n+p+1)) and uses it in the method configuration and C1. Section 3.2 then requires the same symbol to satisfy ell_n sqrt(n/log n) -> 0. Those properties cannot hold simultaneously. Even if intended as local shadowing, it makes the C2 reference to C1's cap ambiguous. Exact correction: reserve ell_n throughout STATEMENT for the LS0 cap. Rename the Form R leak sequence to lambda_n in the section 3 constant note, L-R^b, L-gain-R and the sufficient formula; rename its localised counterpart to lambda'_n. The sufficient formula must read lambda_n = lambda'_n + 15r_n^2/c. Explicitly identify this lambda_n with the leak sequence denoted ell_n in L4. No cap, code option or code pin changes. With this correction the mathematical extension passes; without it C2 has a contradictory literal reading.
2. MINOR — Contradictory condition summary (lines 292–293). The sentence says both C1 and C3 are conditional on SOP:TH09, then immediately says C3 is conditional on nothing. Exact correction: replace that sentence by: "So (C1) is conditional on SOP:TH09@1.0.0 only, (C2) on W2-APP:POST@1.0.1 only, and (C3) has no remaining below-PROVED-CHECKED external condition." This agrees with the dependency removal and avoids suggesting an unqualified absence of proved inputs.
3. MINOR — Wrong sufficient-form location (line 182). The explicit sufficient-form result is L4 section 7 item 1, not section 6. Exact correction: replace "lemmas/L4_sandR_b.md section 6" in that parenthetical pointer by "lemmas/L4_sandR_b.md section 7, item 1".
4. MINOR — Historical identity overstated (lines 6–8 and 179–181). The sufficient form has a weaker rate and more general leak sequence than literal v1.3, and C5's claims/examples do change. Exact corrections: in the opening, replace "the v1.3 hypothesis is kept as the sufficient form" by "a generalisation of the v1.3 hypothesis is retained as the sufficient form"; replace "No Form F hypothesis and no claim of v1.3 changes" by "No Form F hypothesis or conclusion of (C1)–(C4) changes; (C5) and the dependency records are updated." In section 3.2 replace "Sufficient — the v1.3 form" by "Sufficient — a generalisation of the v1.3 localised form". The RM parenthetical correctly identifies the old rates; no rate or constant needs changing.

Well-posedness and record checks.

- Apart from finding 1, the quantifiers are well posed: Q and H_l are deterministic; the sequences are uniform over l,U,j,v; l and the tested truth j are outside the conditioning set; and U may contain other truths. Since all truths lie in H_l, S0 minus U0 equals S0 minus U. Empty outside-Q or tested-truth families are correctly vacuous. Nonnegative leak/rate sequences, as explicit in L4, may be adopted without loss.
- Positive rho is consistent with H_l containing {l} union S0: a fixed s0+1 is eventually below n^rho, and any b<1/2 permits 0<rho<(1/2-b)/15. This does not assert that every design admits neighbourhoods at every such rho.
- The "in words" paragraph is accurate as an asymptotic summary with "any 15" understood as "any at most 15" and with the displayed conditioning/truth exclusions retained. "H_l only has to capture correlations that do not vanish" concerns conditional covariances at U0, not merely marginal correlations. It does not remove uniformity or the neighbourhood budget. The claim about smaller rho is qualified by what the design allows.
- P7 matches L4 section 0 and section 7: same hypotheses and reference budget, any X-measurable partition, product-form removal and mean-shift scales. I have not rechecked its probabilistic argument.
- P10 matches L5 sections 3/5: APP only for p>=2, an internal p=1 endpoint, B9 not consumed. C4(R) matches L5 section 4 and the allowed parent hypotheses.
- C5 matches each L6 table row: inherited RM-F examples; UNI-0; LOC-BF; Gaussian polynomial decay alpha>2; exact-Gram decay alpha>2 with fixed signals/separation; weak proxies for 0<b<1/2; positive equicorrelation for 0<b<3/10; and the unverified remaining equicorrelation range. The radius and b endpoint in the new record agree with the recorded classes. These are summaries of the complete L6 constructions, including p<n for exact Gram and p=floor(n/3) with orthogonal remainder for the proxy/group constructions; they are not assertions for arbitrary p or arbitrary unspecified remainder. Source status is PROVED (by this seat, unchecked), conditional on theorem/input statuses, not independently checked proof status. The alpha>2 cutoff is the available IR route's cutoff, not a necessity claim. The old alpha>17/2 theorem is not applied below its range.
- Section 5's two dependency removals have the stated support in L5 and the L0 header. The external posterior conditions remain; IR/BC are example inputs only. Finding 2 corrects the conflicting C3 summary.
- Section 6 agrees with the permitted records: localisation still required at r_n->0, no exact-scale frontier, no smaller reference exponent, and no larger verified equicorrelation range.
- Section 7 is only a pointer. Its assertion that all old registry content was carried into REPORT is not independently verified here.

Checks performed / not checked.

Performed: complete diff of current STATEMENT versus the allowed CP2 snapshot; snapshot equality with git show c2257ab:Theory_work/Wave3/W3-RM2/STATEMENT.md after normalising line endings/final newline; manifest first-line comparison; independent Schur-complement derivation and rates; statement/record comparison against the permitted lemma sections, L6 table/status lines, L0 header, and parent STATEMENT lines 127–156. No git state was changed. Only this review file was written; no subagents were started.

Not checked: lemma proofs, code implementation, REPORT/registry migration, other reviews, logs or checkpoints, source papers, and full manifest file hashes. One L4 extraction accidentally displayed section 1 in addition to the allowed section 0; section 1 was not used as review evidence. No other unlisted source was consulted.

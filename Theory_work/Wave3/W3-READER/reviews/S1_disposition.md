# S1 disposition — Sol fidelity read (gpt-6.1-sol, high) of READER_VERSIONS / NOTATION / CLAIMS_CARD v0.1

Review: `reviews/S1_fidelity_sol.md` on the frozen manifest `reviews/S1_frozen/MANIFEST_S1.txt` (hashes matched).
Verdict: **"S1-VERDICT: NOT-FAITHFUL AS WRITTEN — repair F1–F7 before acceptance; the set-size arithmetic and B6.3 are
valid, and the remaining mathematical reductions pass subject to the explicitly identified premises and inherited
statuses."**
Lead: all 12 findings ACCEPTED and applied (READER_VERSIONS v0.2, NOTATION v0.2, CLAIMS_CARD v0.3; markers [S1-F#]).
No finding touches a master theorem or a registry status; none is a counterexample to a target (F1 and F5 are false
*literal* statements in the reader text and the card, repaired by restoring the master's restriction).

| # | Sev. | Where | Disposition | Tag |
|---|---|---|---|---|
| F1 | FATAL | Thm 1 (A6): $C_\beta$ may be negative | ACCEPT. "$C_\beta>0$" added. | hypothesis corrected (STRONGER, now = master) |
| F2 | MAJOR | Thms 6–7: delivery's operational premises not discharged | ACCEPT. New standing convention (S4) "delivery conventions" (idealised machine, covered configuration, valid seed, declared allocation ≥ polynomial envelopes incl. preflight), stated in words in READER_VERSIONS and NOTATION §5; conclusions split: common data event for admissible output runs (no (S4)) + "always output, $P(\hat S=S_0)\to1$, every admissible $n\ge3$" under (S4). B6.6/B7.4 now say (V)/(S)/(P) are derived and the F-UNI paragraph is carried, not derived. Premise table → proof leg (`lemmas/R3_delivery_assembly.md`). | unconditional clause WEAKER (now faithful) |
| F3 | MAJOR | Thm 6 (A4)(ii), (A6): no common envelopes | ACCEPT. Deterministic $\varpi_n$, $r_n\to0$ bounding all covariances for all $l,U,v,j$; deterministic $\nu_n=o(\log n)$ with $|N_l|\le\nu_n$ for all $l$. | hypotheses STRONGER (= master) |
| F4 | MAJOR | Thm 5 floor "for every data set" | ACCEPT. "for every valid data set with $n\ge4$ and $s_0<K$ (hence for all large $n$)". | clause WEAKER (= master) |
| F5 | FATAL | Card row (Thm 3): domain $|S|\le\min(K-1,p/2)$ dropped; RV remarks overgeneral | ACCEPT. Domain restored in the card; RV consequences prefixed with the domain, with the $S=[p]$ counter-remark. | EQUAL to master |
| F6 | MINOR | Thm 3 remark: "these designs satisfy Thms 1–2" | ACCEPT. Named the two witness sequences (fully orthogonal; i.i.d. $N(0,1)$ raw), fixed nonzero coefficients. | EQUAL |
| F7 | MAJOR | Card row (Thm 5): $c<\tfrac12$ attached to growing $Q$ | ACCEPT. Separated: $c<\tfrac12$ for $Q=S_0$; $c<\epsilon$ for $|Q|\le n^{1/2-\epsilon}$. | EQUAL to master |
| F8 | MINOR | Thm 8: "no condition on null correlations"; $q_n$ range | ACCEPT. Wording "beyond (A1)–(A3)" + remark on the master's directional floor; $q_n\in\{0,\dots,K-1\}$. | EQUAL |
| F9 | MINOR | Thm 1/4 statuses: TH09 truncated, TH128 missing | ACCEPT. Both quoted in full, attributed separately. | — |
| F10 | MINOR | NOTATION: "flat intercept prior" equivalence | ACCEPT. Parenthetical replaced: centring + $n$-dimensional working likelihood ($\nu=a_0+n/2$), with the note that a flat prior would give $a_0+(n-1)/2$. | — |
| F11 | MINOR | NOTATION: certificate omits exact branch | ACCEPT. Certified = public flag: exact-enumeration maximiser, or certified local-search end point; LS0's own archive certificate kept distinct. | — |
| F12 | MINOR | Thm 4 listed as depending on `W2-APP:POST` | ACCEPT. Removed from RV B2.2, the bridge summary, the card notes and CP1 rank 1. | — |

Positive checks recorded by S1 (kept as evidence for CP3): Theorem 2 FAITHFUL; set-size arithmetic B1.2, B1.3, B2.1,
B4.1, B6.1 verified analytically (not only on the numeric grid); B6.3 variance bound passes; B6.6/B7.4 pass for
(V)/(S)/(P); every other master-to-reader reduction passes subject to the repaired items.

Post-fix state: Theorems 1, 3, 4, 5, 8 FAITHFUL after the stated fixes (one-line repairs restoring the master's own
restrictions); Theorems 6–7 FAITHFUL with (S4) carried. **Not re-reviewed**: under PROTOCOL_v4 the v0.2 text is
unchecked until the CP3 council diff round (gate F) or a Sol diff check, as the manager decides.

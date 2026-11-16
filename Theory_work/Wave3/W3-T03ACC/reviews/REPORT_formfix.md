# W3-T03ACC — REPORT registry block, FORM-FIXED copy (proposed record fix for HQ, v4 §7; not part of any manifest)

`REPORT.md` is frozen in the passing round (MANIFEST 9714aea4…), so v4 §5.9 forbids editing it. The staged ingest of
`REPORT.md` raised 7 form problems (status_source not verbatim; `implies TH128` not a registry id; `kind: remark` not
allowed). This copy differs from `REPORT.md` §4 only in: repo-relative paths; status = CHECKPOINT_3.md:3 verbatim
with status_source there; `SOP:TH128`; T03S.5 kind `proposition`; `correct:PASS(...)` and the `council:` cell from
`manifest.py bind`. No statement, premise, conclusion or scope changes.

```
REGISTRY
claim: W3-T03ACC:T03S.1 | kind: theorem | statement: Theory_work/Wave3/W3-T03ACC/STATEMENT.md:64 | premises: Theory_work/Wave3/W3-T03ACC/STATEMENT.md:43-60
name: T03♯(i) posterior concentration (= SOP:TH09, TH128 clause 1)
status: PROVED (candidate) (W1-T03R); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PASS (astra 9.5, opus 9.4) | status_source: Theory_work/Wave3/W3-T03ACC/CHECKPOINT_3.md:3
conclusion: posterior: 1 − π(S₀) = O_P(r_n) | rate: √(log n/n) | scope: fixed design, s₀ ≥ 1 fixed, p ≤ n^A (A fixed), asymptotic
implies: SOP:TH09 (same statement, clause 1) ; SOP:TH128 (same statement, clause 1)
gates: correct:PASS(Theory_work/Wave3/W3-T03ACC/reviews/R1_council_astra.md, Theory_work/Wave3/W3-T03ACC/reviews/R1_council_opus.md)
council: R1; MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6; astra=9.5 PASS(reviews/R1_council_astra.md); opus=9.4 PASS(reviews/R1_council_opus.md)

REGISTRY
claim: W3-T03ACC:T03S.2 | kind: theorem | statement: Theory_work/Wave3/W3-T03ACC/STATEMENT.md:65 | premises: Theory_work/Wave3/W3-T03ACC/STATEMENT.md:43-60
name: T03♯(ii) PIP bound and MPM consistency
status: PROVED (candidate) (W1-T03R); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PASS (astra 9.5, opus 9.4) | status_source: Theory_work/Wave3/W3-T03ACC/CHECKPOINT_3.md:3
conclusion: posterior: max_j |PIP_j − 1{j ∈ S₀}| ≤ 1 − π(S₀) for every data set; P₀(MPM = S₀) → 1 | scope: as T03S.1
depends_on: W3-T03ACC:T03S.1@stmt
implies: SOP:TH09 (clause 2)
gates: correct:PASS(Theory_work/Wave3/W3-T03ACC/reviews/R1_council_astra.md, Theory_work/Wave3/W3-T03ACC/reviews/R1_council_opus.md)
council: R1; MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6; astra=9.5 PASS(reviews/R1_council_astra.md); opus=9.4 PASS(reviews/R1_council_opus.md)

REGISTRY
claim: W3-T03ACC:T03S.3 | kind: theorem | statement: Theory_work/Wave3/W3-T03ACC/STATEMENT.md:66-69 | premises: Theory_work/Wave3/W3-T03ACC/STATEMENT.md:43-60
name: T03♯(iii) global-HPM consistency
status: PROVED (candidate) (W1-T03R); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PASS (astra 9.5, opus 9.4) | status_source: Theory_work/Wave3/W3-T03ACC/CHECKPOINT_3.md:3
conclusion: posterior: P₀(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] → 0; S₀ strict maximiser of F on {π(S₀) > ½} | scope: as T03S.1; no expectation rate
depends_on: W3-T03ACC:T03S.1@stmt
implies: SOP:TH09 (clause 3)
gates: correct:PASS(Theory_work/Wave3/W3-T03ACC/reviews/R1_council_astra.md, Theory_work/Wave3/W3-T03ACC/reviews/R1_council_opus.md)
council: R1; MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6; astra=9.5 PASS(reviews/R1_council_astra.md); opus=9.4 PASS(reviews/R1_council_opus.md)

REGISTRY
claim: W3-T03ACC:T03S.4 | kind: theorem | statement: Theory_work/Wave3/W3-T03ACC/STATEMENT.md:70-73 | premises: Theory_work/Wave3/W3-T03ACC/STATEMENT.md:43-56
name: T03♯(iv) large-signal inclusion without beta-min
status: PROVED (candidate) (W1-T03R); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PASS (astra 9.5, opus 9.4) | status_source: Theory_work/Wave3/W3-T03ACC/CHECKPOINT_3.md:3
conclusion: posterior: Π(S ⊉ J_n(c) | y) = O_P(r_n) and 1 − min_{J_n(c)} PIP_j = O_P(r_n), c > c₀; same for J_n^∞ | scope: as T03S.1, no beta-min
implies: SOP:TH09 (clause 4)
gates: correct:PASS(Theory_work/Wave3/W3-T03ACC/reviews/R1_council_astra.md, Theory_work/Wave3/W3-T03ACC/reviews/R1_council_opus.md)
council: R1; MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6; astra=9.5 PASS(reviews/R1_council_astra.md); opus=9.4 PASS(reviews/R1_council_opus.md)

REGISTRY
claim: W3-T03ACC:T03S.5 | kind: proposition | statement: Theory_work/Wave3/W3-T03ACC/STATEMENT.md:74-77 | premises: none (deterministic)
name: T03♯(v) scale invariance of the beta-min conditions and J_n
status: PROVED (candidate) (W1-T03R); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PASS (astra 9.5, opus 9.4) | status_source: Theory_work/Wave3/W3-T03ACC/CHECKPOINT_3.md:3
conclusion: identity: the BM inequalities and J_n(c), J_n^∞ are invariant under (θ*, σ*²) → (θ*/d, σ*²/d²) | scope: any n
implies: SOP:TH09 (clause 5)
gates: correct:PASS(Theory_work/Wave3/W3-T03ACC/reviews/R1_council_astra.md, Theory_work/Wave3/W3-T03ACC/reviews/R1_council_opus.md)
council: R1; MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6; astra=9.5 PASS(reviews/R1_council_astra.md); opus=9.4 PASS(reviews/R1_council_opus.md)
```

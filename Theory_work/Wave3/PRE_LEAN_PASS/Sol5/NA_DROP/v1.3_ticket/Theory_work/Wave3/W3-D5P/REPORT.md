# W3-D5P — REPORT (track D ticket #5′: the list-restricted outputs on every Theorem 6 design)

Lead: Claude Opus 5.5 (effort high). Branch theory/W3-D5P (off main 029bb748). Protocol: PROTOCOL_v4 + RIDER_RULES
(dept/theory). **This file restates nothing**: statements are in `STATEMENT.md` (v1.0 LOCKED, changelog v1.1–v1.3), proofs in `lemmas/`.
Statuses below are as of this draft; the council result goes in §4 and in the REGISTRY blocks.

## 1. What the ticket delivers
The three claims of `STATEMENT.md` §0 table (`STATEMENT.md:22-24`). Hypotheses of the corollary: those of Theorem 6
(card row 3.1), with nothing added (D109): `STATEMENT.md:100-102`. Implementation premise IMPL-LIST (discharged at
`method-v3.1.1-listpip`, main 7100bb3b): `STATEMENT.md:60-64`. The two links of `Theory_work/Wave3/W3-DIST/STATEMENT.md:297-303` are LIST-CODE (i)–(ii),
`STATEMENT.md:83-89`.

## 2. Claims and where they are

| claim id | statement | proof | status |
|---|---|---|---|
| W3-D5P:LIST-K | `STATEMENT.md:68-76` | `lemmas/L1_listK.md` | PROVED (by this seat); LC1 VERIFIED-WITH-AMENDMENTS, applied; LC1R VERIFIED-WITH-AMENDMENTS (E only), applied |
| W3-D5P:LIST-CODE | `STATEMENT.md:80-96` | `lemmas/L2_listCODE.md` | CODE-READ (by this seat); LC1 VERIFIED-WITH-AMENDMENTS, applied; LC1R VERIFIED-WITH-AMENDMENTS (E only), applied |
| W3-D5P:LIST-R | `STATEMENT.md:100-128` | `lemmas/L3_listR.md` | PROVED (by this seat); IMPL-LIST discharged at method-v3.1.1-listpip (7100bb3b); LC1 VERIFIED-WITH-AMENDMENTS, applied; LC1R VERIFIED-WITH-AMENDMENTS (E only), applied; Step 0′ (v1.2) checked by NA_check_opus (ACCEPT-WITH-CHANGES, applied); Sol-5 (b) points b-1 to b-4 applied in v1.3 (review of v1.3 pending) |

## 3. Evidence, limits, open items
- Statement lock: `reviews/SL1_statement_lock_sol.md` (LOCK WITH CHANGES), `reviews/SL1_disposition.md`.
- Numerics (falsification only; HEURISTIC as evidence): `numerics/listk_check_out.txt` (LIST-K, 20 000 random cases,
  0 violations); `numerics/e2e_small_out.txt` (27 small AR(ρ) cases through the core of record, sampler path vs exact
  enumeration: S₀ ∈ `top_store` 27/27; every LIST-K bound holds).
- IMPL-LIST: discharged at `method-v3.1.1-listpip` (main 7100bb3b) by the code reading `reviews/IMPL_LIST_codeprint.md` §5
  (a premise discharge, not a new council).
- Limits (`STATEMENT.md` §5, not claims): the printed sampler averages on AR/BLK stay out of scope (card row 3.6);
  binary64 is not covered (EX-A).
- Proposal for HQ (not claimed here): the Corollary 9C consequence, `STATEMENT.md` §5 remark 3.

## 4. Council
None yet.

## 5. REGISTRY

```
REGISTRY
claim: W3-D5P:LIST-K | kind: lemma | statement: STATEMENT.md:68-76 | premises: STATEMENT.md:39-47
status: PROVED (by this seat); LC1 VERIFIED-WITH-AMENDMENTS, applied; LC1R VERIFIED-WITH-AMENDMENTS (E only), applied | status_source: REPORT.md:17
conclusion: identity: deterministic: for any list T of models containing S0, the list-renormalised PIPs are within 1 - pi(T) <= 1 - pi(S0|y) of the exact PIPs and within 1 - pi_T(S0) <= 1 - pi(S0|y) of the indicator of S0; the list median model is S0 when 1 - pi(S0|y) < 1/2; log Z_T = log Z + log pi(T)
rate: none (deterministic)
scope: any finite set of models Omega and any real-valued F on Omega (as (C1)); applied with Omega = {|S| <= K} and the coded F [R1-opus-4]
depends_on: none
council: none yet
```

```
REGISTRY
claim: W3-D5P:LIST-CODE | kind: lemma | statement: STATEMENT.md:80-96 | premises: STATEMENT.md:29-38 ; STATEMENT.md:49-58
status: CODE-READ (by this seat); LC1 VERIFIED-WITH-AMENDMENTS, applied; LC1R VERIFIED-WITH-AMENDMENTS (E only), applied | status_source: REPORT.md:18
assumptions: A:OP ; A:EX-A
conclusion: identity: code fact at core 4676af6: on the sampler branch status completed iff estimates available (the output event), and LS0 ran in the final run with the evaluation sequence of the search in K_n; printed hpm = the HPM-order maximum of the models offered to the final-run ledger (= the reported model of RM/RM2R); top_store holds distinct offered models with their exact scores and contains that maximum; exact branch: the enumeration's store contains the HPM-order maximum of Omega, pip_primary/mpm are exact
rate: none
scope: the method as coded (shipped configuration)
depends_on: W3-SAMP:CC@stmt
method: production core on main = 4676af6 | method_commit: 4676af6
council: none yet
```

```
REGISTRY
claim: W3-D5P:LIST-R | kind: corollary | statement: STATEMENT.md:100-128 | premises: STATEMENT.md:29-64
status: PROVED (by this seat); IMPL-LIST discharged at method-v3.1.1-listpip (7100bb3b); LC1 VERIFIED-WITH-AMENDMENTS, applied; LC1R VERIFIED-WITH-AMENDMENTS (E only), applied; Step 0′ (v1.2) checked by NA_check_opus (ACCEPT-WITH-CHANGES, applied); Sol-5 (b) points b-1 to b-4 applied in v1.3 (review of v1.3 pending) | status_source: REPORT.md:19
assumptions: A:LSF ; A:IID-GAUSS-ROWS ; A:RM-FLR ; A:PTV ; A:RM2-LFEAS ; A:RM2-LGAIN-R ; A:RM2-LLOC-R ; A:RM2-LSIZE-B-R ; A:RM2-HSIZE-RHO ; A:RM2-W-R ; A:OP ; A:BLOCK-LE-16 ; A:DELIV-D ; A:EX-A ; A:IMPL-LIST (new | list-field implementation conformance | the printed pip_list, mpm_list, log_Z_list are computed as SPEC_LIST_PIP §2 and §4 prescribe from the returned list of the same run (exact-branch row: log_Z_list from fit$exact$top [NA-1]), and no other field or state changes | STATEMENT.md:60-64 | shared no | bridge W3-D5P:LIST-R)
conclusion: (o) every admissible output run, on either branch and for every data set, prints pip_list, mpm_list and a finite log_Z_list [NA-b4]; reported-model: on Theorem 6's data event every admissible output run has S0 in its returned list (exact branch: in the enumeration's store), hpm = S0, pip_list within 1 - pi(S0|y) of the truth and of the exact PIPs (sampler: list-renormalised; exact branch: exact PIPs), log Z + log pi(S0|y) <= log_Z_list <= log Z, mpm_list = S0 when 1 - pi(S0|y) < 1/2; under (D) without "on output" [R1-sol-1, R1-sol-3, R1-opus-2]
rate: O_P(sqrt(log n / n)) for the two PIP errors and |log_Z_list - log Z| (p >= 2)
scope: Gaussian rows; every design inside Theorem 6 (AR and block designs included when they satisfy it); the list fields only (not the printed sampler averages)
depends_on: W3-D5P:LIST-K@stmt ; W3-D5P:LIST-CODE@stmt ; W3-RM2-R:RM2-R-plus@stmt ; W3-RM2-R:RM0-plus@stmt ; W3-RM2-R:DLV-0@stmt ; W2-APP:POST@stmt
method: production core on main = 4676af6, plus the list fields of SPEC_LIST_PIP (IMPL-LIST discharged at method-v3.1.1-listpip, 7100bb3b)
council: none yet
```

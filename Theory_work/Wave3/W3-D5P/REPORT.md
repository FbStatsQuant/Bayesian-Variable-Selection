# W3-D5P — REPORT (track D ticket #5′: the list-restricted outputs on every Theorem 6 design)

Lead: Claude Opus 5.5 (effort high). Branch theory/W3-D5P (off main 029bb748). Protocol: PROTOCOL_v4 + RIDER_RULES
(dept/theory). **This file restates nothing**: statements are in `STATEMENT.md` (v1.0 LOCKED), proofs in `lemmas/`.
Statuses below are as of this draft; the council result goes in §4 and in the REGISTRY blocks.

## 1. What the ticket delivers
The three claims of `STATEMENT.md` §0 table (`STATEMENT.md:21-24`). Hypotheses of the corollary: those of Theorem 6
(card row 3.1), with nothing added (D109): `STATEMENT.md:95-97`. Implementation premise IMPL-LIST (method commit
pending): `STATEMENT.md:56-60`. The two links of `Theory_work/Wave3/W3-DIST/STATEMENT.md:297-303` are LIST-CODE (i)–(ii),
`STATEMENT.md:78-84`.

## 2. Claims and where they are

| claim id | statement | proof | status |
|---|---|---|---|
| W3-D5P:LIST-K | `STATEMENT.md:64-71` | `lemmas/L1_listK.md` | PROVED (by this seat, unchecked); LC1 pending |
| W3-D5P:LIST-CODE | `STATEMENT.md:75-91` | `lemmas/L2_listCODE.md` | CODE-READ (by this seat, unchecked); LC1 pending |
| W3-D5P:LIST-R | `STATEMENT.md:95-120` | `lemmas/L3_listR.md` | PROVED (by this seat, unchecked); conditional on IMPL-LIST; LC1 pending |

## 3. Evidence, limits, open items
- Statement lock: `reviews/SL1_statement_lock_sol.md` (LOCK WITH CHANGES), `reviews/SL1_disposition.md`.
- Numerics (falsification only; HEURISTIC as evidence): `numerics/listk_check_out.txt` (LIST-K, 20 000 random cases,
  0 violations); `numerics/e2e_small_out.txt` (27 small AR(ρ) cases through the core of record, sampler path vs exact
  enumeration: S₀ ∈ `top_store` 27/27; every LIST-K bound holds).
- Open item IMPL-LIST: discharged by a code reading of Engineering's method commit when it lands (manager: a
  premise discharge, not a new council).
- Limits (`STATEMENT.md` §5, not claims): the printed sampler averages on AR/BLK stay out of scope (card row 3.6);
  binary64 is not covered (EX-A).
- Proposal for HQ (not claimed here): the Corollary 9C consequence, `STATEMENT.md` §5 remark 3.

## 4. Council
None yet.

## 5. REGISTRY

```
REGISTRY
claim: W3-D5P:LIST-K | kind: lemma | statement: STATEMENT.md:64-71 | premises: STATEMENT.md:39-44
status: PROVED (by this seat, unchecked); LC1 pending | status_source: REPORT.md:17
conclusion: deterministic: for any list T of models containing S0, the list-renormalised PIPs are within 1 - pi(T) <= 1 - pi(S0|y) of the exact PIPs and within 1 - pi_T(S0) <= 1 - pi(S0|y) of the indicator of S0; the list median model is S0 when 1 - pi(S0|y) < 1/2; log Z_T = log Z + log pi(T)
rate: none (deterministic)
scope: any finite model space and any score
depends_on: none
council: none yet
```

```
REGISTRY
claim: W3-D5P:LIST-CODE | kind: lemma | statement: STATEMENT.md:75-91 | premises: STATEMENT.md:29-37
status: CODE-READ (by this seat, unchecked); LC1 pending | status_source: REPORT.md:18
assumptions: A:OP ; A:EX-A
conclusion: code fact at core 4676af6: on the sampler branch status completed iff estimates available (the output event), and LS0 ran in the final run with the evaluation sequence of the search in K_n; printed hpm = the HPM-order maximum of the models offered to the final-run ledger (= the reported model of RM/RM2R); top_store holds distinct offered models with their exact scores and contains that maximum; exact branch: the enumeration's store contains the HPM-order maximum of Omega, pip_primary/mpm are exact
rate: none
scope: the method as coded (shipped configuration)
depends_on: W3-SAMP:CC@stmt
method: SMC-BVS v3.1 core | method_commit: 4676af6 (top_store); the list fields: pending (Engineering)
council: none yet
```

```
REGISTRY
claim: W3-D5P:LIST-R | kind: corollary | statement: STATEMENT.md:95-120 | premises: STATEMENT.md:29-60
status: PROVED (by this seat, unchecked); conditional on IMPL-LIST; LC1 pending | status_source: REPORT.md:19
assumptions: the hypotheses of W3-RM2-R:RM2-R-plus (= Theorem 6, card row 3.1), nothing added ; A:OP ; A:EX-A ; IMPL-LIST (new | the printed list fields are computed as SPEC_LIST_PIP §2, §4 prescribe | code fact of the pending method commit | STATEMENT.md:56-60 | shared no | discharge: code reading) ; A:DELIV-D (clause (iii) only)
conclusion: on Theorem 6's data event every admissible output run has S0 in its returned list, hpm = S0, list PIPs within 1 - pi(S0|y) of the truth and of the exact PIPs, log Z + log pi(S0|y) <= log_Z_list <= log Z, mpm_list = S0 when 1 - pi(S0|y) < 1/2; under (D) without "on output"
rate: O_P(sqrt(log n / n)) (p >= 2)
scope: Gaussian rows; every design inside Theorem 6 (AR and block designs included when they satisfy it); the list fields only (not the printed sampler averages)
depends_on: W3-D5P:LIST-K@stmt ; W3-D5P:LIST-CODE@stmt ; W3-RM2-R:RM2-R-plus@stmt ; W3-RM2-R:RM0-plus@stmt ; W3-RM2-R:DLV-0@stmt ; W2-APP:POST@stmt
method: SMC-BVS v3.1 core + list fields | method_commit: pending (Engineering; D105)
council: none yet
```

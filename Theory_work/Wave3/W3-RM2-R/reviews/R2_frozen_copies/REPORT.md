# W3-RM2-R — REPORT to Theory HQ (rider on W3-RM2: constant-level signals T4, mode interface and delivery T2)

> **Flags (read first).**
> 1. **Headline changes (H5).** RM2-F-plus weakens three hypotheses of RM2-F (visibility, Theorem 1's beta-min, the
>    truth-removal floor) to the constant level; RM2-F-plus and RM2-R-plus add, under the delivery premises (D), the
>    conclusion P(Ŝ⁺ = S₀) → 1 without "on output", with the error split into mode failure + search failure. Both are
>    STRONGER than the recorded RM2-F / RM2-R (Cont-plus). Statement: `STATEMENT.md` v1.0 (locked; changelog at its foot).
> 2. **Delivery needs IDEAL-W⁺**: two fixed upper bounds of the shipped code are treated as lifted (`STATEMENT.md` §2;
>    engineering note in `H5_SUMMARY.md`). Without the lift, delivery holds on the bounded domain 𝔇 only.
> 3. **Conditional**, as the parents: (C1⁺) and Ex-Proxy-d on SOP:TH09@1.0.0; (C2⁺) on W2-APP:POST@1.0.1. DLV-0 rests on
>    the inherited code-reading audits (C-DLV P1, S.3) plus this ticket's re-reading of the C-ENG changes.
> 4. Not claimed here: O-Wq (quantile form of (W)), O4′ (Ex-Equi b = 3/8), the Form R aggregated leak; RM2's Ex-PolyR,
>    Ex-PolyF are not re-examined (manager, CP1).

## 1. RESULT

Every claim of `STATEMENT.md` v1.0 has a proof in `lemmas/` (Q1, Q2, Q4, Q5, Q6, Q7). Review record: statement lock
SL1 + statement-change check SC1 (Sol, `reviews/SL1_statement_lock_sol.md`, `reviews/SC1_statement_change_sol.md`);
line checks LC-A (Q1, Q2, Q7: `reviews/LCA_line_check_sol.md`) and LC-B (Q4, Q5, Q6: `reviews/LCB_line_check_sol.md`),
the Q5 repair re-checked by RC1 (`reviews/RC1_recheck_sol.md`); all Sol (codex gpt-6.1-sol high), NORMAL mode; no C/S
finding; three F findings on Q5, repaired and re-checked; one E finding in `ERRATA.md`. DEPS: every row OK. Council R1 (§4).
Statuses below are as of this draft; the council result is recorded in §4 and in the REGISTRY block.

## 2. Claims and where they are (statements are in STATEMENT; this file restates nothing)

| claim id | statement | proof | status |
|---|---|---|---|
| W3-RM2-R:RM0-plus | `STATEMENT.md:118-143` | `lemmas/Q4_core_plus.md` | PROVED (by this seat, unchecked); LC-B VERIFIED |
| W3-RM2-R:DLV-0 | `STATEMENT.md:144-163` | `lemmas/Q5_dlv0.md` | PROVED (by this seat, unchecked), relative to the C-DLV P1/S.3 audits; LC-B VERIFIED-WITH-AMENDMENTS, applied; RC1 VERIFIED |
| W3-RM2-R:RM2-F-plus | `STATEMENT.md:166-176` | `lemmas/Q6_assembly.md` §1 | PROVED (by this seat, unchecked); conditional on SOP:TH09@1.0.0; LC-B VERIFIED |
| W3-RM2-R:RM2-R-plus | `STATEMENT.md:177-182` | `lemmas/Q6_assembly.md` §2 | PROVED (by this seat, unchecked); conditional on W2-APP:POST@1.0.1; LC-B VERIFIED |
| W3-RM2-R:SAND-F-c | `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:188` (Q1 row) | `lemmas/Q1_sandF_c.md` | PROVED (by this seat, unchecked); LC-A VERIFIED-WITH-AMENDMENTS (1 E → ERRATA E1) |
| W3-RM2-R:TL-F-c | `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:189` (Q2 row) | `lemmas/Q2_TL_c.md` §4 | PROVED (by this seat, unchecked); LC-A VERIFIED |
| W3-RM2-R:Ex-Proxy-d | `STATEMENT.md:197-205` | `lemmas/Q7_proxy_d.md` | PROVED (by this seat, unchecked); conditional on SOP:TH09@1.0.0; LC-A VERIFIED |
| W3-RM2-R:Cont-plus | `STATEMENT.md:206-213` | `lemmas/Q6_assembly.md` §3 | PROVED (by this seat, unchecked); LC-B VERIFIED |

## 3. Sharpness and open items (HEURISTIC where not proved)

* Constants M_V⁰, c_TL⁰, c₀, κ₀ are proof artefacts (`TARGET.md` §1). Boundary numerics: `numerics/RESULTS.md`
  (finite-n observations of the validated LS0 re-implementation; not evidence about necessity).
* Open items: O-Wq (quantile (W)); O4′ (Ex-Equi b = 3/8); Form R aggregated leak; and those of PARENT `SHARPNESS.md` §7.
* v3.2: Lemma R and the allocation 𝒜_n must be re-audited when v3.2 freezes (`STATEMENT.md` (C-D) scope note).

## 4. Council

R1 (manifest `reviews/MANIFEST_R1.txt`, MANIFEST 4c2183ce…cd402): both seats ACCEPT every claim and pass the
correctness gate; both FAIL other gates on findings in derived texts only — Opus 8.7 (`reviews/R1_council_opus.md`:
F1 REPORT conditions vs STATEMENT, F2 READER bridge R7.2), Sol 8.5 (`reviews/R1_council_sol.md`: F1 Song–Liang
attribution in TARGET, S2 TARGET necessity wording). Dispositions: `reviews/R1_disposition.md`. Diff round R2:
manifest `reviews/MANIFEST_R2.txt`; result recorded here when complete.

## 5. REGISTRY

One block per claim. Cont-plus records its targets under `implies`, not `depends_on` (HQ ruling at CP1); its
`depends_on` on W3-RM2:Cont-F/Cont-R is for clause (iv) (reported to the manager).

```
REGISTRY
claim: W3-RM2-R:RM2-F-plus | kind: theorem | statement: STATEMENT.md:166-176 | premises: STATEMENT.md:52-115
status: PROVED (by this seat, unchecked); conditional on SOP:TH09@1.0.0; LC-B VERIFIED | status_source: REPORT.md:30
assumptions: A:T1F-FLAT (new | Theorem 1 conditions with BM-inf or BM(c) | (H0) of GROW with the beta-min clause BM-inf or BM(c), c > c0(s0,A), of SOP:TH09 | STATEMENT.md:95-99 | shared yes | bridge W3-RM2-R:TL-F-c) ; A:RM-FL ; A:RM2-V-FLAT (new | visibility at a constant level | delta^2_{U,j} >= M_V log n with fixed M_V > (sigma sqrt(2A) + sqrt((2A+1) C_R))^2, C_R = 3(M + sigma^2) | STATEMENT.md:101-105 | shared no | bridge W3-RM2-R:SAND-F-c) ; A:RM2-LFEAS-GAIN ; A:RM2-LSIZE-B ; A:RM2-BM-W-PLUS (new | additive truth-removal floor at the constant level | sqrt(lambda_n) >= 2(d_n + sqrt(2 log n)) and lambda_n >= c_TL log n, c_TL > 8(A+1) + 4(2A+1) C_R/sigma^2 | STATEMENT.md:107-112 | shared no | bridge W3-RM2-R:TL-F-c) ; A:RM2-W ; A:OP ; A:BLOCK-LE-16 ; A:DELIV-D (new | delivery premises (D) with IDEAL-W-plus, for the unconditional clause only | EX-A unit cost, IDEAL-W with two lifted upper-bound predicates, MACH, CONFIG at the shipped configuration, TDP-IMPL, declared allocation A_n, valid non-degenerate input | STATEMENT.md:71-93 | shared yes | bridge W3-RM2-R:DLV-0)
conclusion: reported-model: one data event of probability -> 1 on which every admissible output run reports S0; under (D) every run returns output and P(S-hat = S0) -> 1 with P(S-hat != S0) <= P(mode failure) + P(search failure)
rate: none claimed
scope: fixed design; s0 fixed; p <= n^A (p >> n allowed); |Q| <= n^b
depends_on: W3-RM2-R:RM0-plus@stmt ; W3-RM2-R:DLV-0@stmt ; W3-RM2-R:SAND-F-c@stmt ; W3-RM2-R:TL-F-c@stmt ; W3-RM2:NA-W@stmt ; W3-RM:E4@stmt ; SOP:TH09@hyp
notes: the posterior/mode step POST/MODE-F (Theorem RM2-F-plus input; Theory_work/Wave3/W3-RM2-R/STATEMENT.md:190, bridge (Q3); proof lemmas/Q2_TL_c.md §6) is recorded under this claim, which carries its condition SOP:TH09 [R1-opus-F1]
implies: W3-RM2:RM2-F (weaker hypotheses, conclusions contain; proved in W3-RM2-R:Cont-plus)
sharpness: A:RM2-V-FLAT = ARTEFACT (evidence: lemmas/Q1_sandF_c.md:158) ; A:RM2-BM-W-PLUS = ARTEFACT (evidence: lemmas/Q2_TL_c.md:113)
gates: correct:PENDING(reviews/LCB_line_check_sol.md) ; lit:PENDING(TARGET.md) ; necessity:PENDING(TARGET.md) ; better:PENDING(TARGET.md)
council: none yet
```

```
REGISTRY
claim: W3-RM2-R:RM2-R-plus | kind: theorem | statement: STATEMENT.md:177-182 | premises: STATEMENT.md:52-115
status: PROVED (by this seat, unchecked); conditional on W2-APP:POST@1.0.1; LC-B VERIFIED | status_source: REPORT.md:31
assumptions: A:LSF ; A:IID-GAUSS-ROWS ; A:RM-FLR ; A:PTV ; A:RM2-LFEAS ; A:RM2-LGAIN-R ; A:RM2-LLOC-R ; A:RM2-LSIZE-B-R ; A:RM2-HSIZE-RHO ; A:RM2-W-R ; A:OP ; A:BLOCK-LE-16 ; A:DELIV-D
conclusion: reported-model: as RM2-F-plus under the joint law of (X, eps)
rate: none claimed
scope: Gaussian rows; s0 fixed; p <= n^A; |Q| <= n^b, |H_l| <= n^rho
depends_on: W3-RM2-R:RM0-plus@stmt ; W3-RM2-R:DLV-0@stmt ; W3-RM2:SAND-R-b@stmt ; W3-RM2:F-to-R@stmt ; W3-RM2:POST-R@stmt ; W3-RM:E4@stmt ; W2-APP:POST@hyp
implies: W3-RM2:RM2-R (same hypotheses, conclusions contain; proved in W3-RM2-R:Cont-plus)
gates: correct:PENDING(reviews/LCB_line_check_sol.md) ; lit:PENDING(TARGET.md) ; necessity:PENDING(TARGET.md) ; better:PENDING(TARGET.md)
council: none yet
```

```
REGISTRY
claim: W3-RM2-R:RM0-plus | kind: theorem | statement: STATEMENT.md:118-143 | premises: STATEMENT.md:52-93
status: PROVED (by this seat, unchecked); LC-B VERIFIED | status_source: REPORT.md:28
depends_on: W3-RM:RM-0@proof ; W3-RM:E4@stmt ; C-GROW:L1.1@proof ; C-GROW:L1.2@proof ; W3-RM2-R:DLV-0@stmt
implies: W3-RM:RM-0 (pi(S0) > 1/2 implies the mode event; part (a) identical)
council: none yet
```

```
REGISTRY
claim: W3-RM2-R:DLV-0 | kind: lemma | statement: STATEMENT.md:144-163 | premises: STATEMENT.md:71-93
status: PROVED (by this seat, unchecked), relative to the C-DLV P1/S.3 audits; LC-B VERIFIED-WITH-AMENDMENTS, applied; RC1 VERIFIED | status_source: REPORT.md:29
depends_on: C-DLV:Thm-D@proof ; C-DLV:L2-S2@stmt ; C-DLV:L1-R@stmt ; C-DLV:Cor-R@stmt ; C-DLV:L3-3.3@stmt ; C-DLV:L3-3.4@stmt ; C-DLV:Prop-F@proof ; C-DLV:P1-Inventory@stmt ; C-DLV:L2-S3@stmt ; W2-UNI:F-UNI@proof ; W3-RM:E4@stmt
notes: the allocation A_n is taken from FINAL s6_delivery.tex:33-44 (HQ audits A1/A4; not a registry claim); C-DLV:Prop-F is used for its delivery half only (R-AUD1 restatement) [R1-opus-E3]
council: none yet
```

```
REGISTRY
claim: W3-RM2-R:SAND-F-c | kind: lemma | statement: STATEMENT.md:188 | premises: STATEMENT.md:52-115
status: PROVED (by this seat, unchecked); LC-A VERIFIED-WITH-AMENDMENTS (1 E → ERRATA E1) | status_source: REPORT.md:32
depends_on: W3-RM2:SAND-F-b@proof ; W3-RM2:Toolkit-b@stmt
implies: W3-RM2:SAND-F-b ((V_b) implies (V_b-flat))
council: none yet
```

```
REGISTRY
claim: W3-RM2-R:TL-F-c | kind: lemma | statement: STATEMENT.md:189 | premises: STATEMENT.md:52-115
status: PROVED (by this seat, unchecked); LC-A VERIFIED | status_source: REPORT.md:33
depends_on: W3-RM2:TL-F-b@proof ; W3-RM2:Toolkit-b@stmt ; W3-RM2:NA-W@stmt
implies: W3-RM2:TL-F-b ((BM-W) implies (BM-W-plus))
council: none yet
```

```
REGISTRY
claim: W3-RM2-R:Ex-Proxy-d | kind: proposition | statement: STATEMENT.md:197-205 | premises: STATEMENT.md:52-115
status: PROVED (by this seat, unchecked); conditional on SOP:TH09@1.0.0; LC-A VERIFIED | status_source: REPORT.md:34
depends_on: W3-RM2:Ex-Proxy@proof ; SOP:TH09@hyp
implies: W3-RM2:Ex-Proxy (constant theta is a special case of part (b))
council: none yet
```

```
REGISTRY
claim: W3-RM2-R:Cont-plus | kind: lemma | statement: STATEMENT.md:206-213 | premises: STATEMENT.md:52-115
status: PROVED (by this seat, unchecked); LC-B VERIFIED | status_source: REPORT.md:35
depends_on: W3-RM2-R:RM2-F-plus@stmt ; W3-RM2-R:RM2-R-plus@stmt ; W3-RM2-R:RM0-plus@stmt ; W3-RM2-R:Ex-Proxy-d@stmt ; W3-RM2:Cont-F@stmt ; W3-RM2:Cont-R@stmt
implies: W3-RM2:RM2-F ; W3-RM2:RM2-R ; W3-RM:RM-0 ; W3-RM:RM-F ; W3-RM:RM-R ; W3-RM2:Ex-Proxy
council: none yet
```

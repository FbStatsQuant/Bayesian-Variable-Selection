# Council R1, seat opus — reply of Claude Opus 5.5 (effort high, Claude Third), verbatim
# Brief: reviews/BRIEF_R1_opus.md; manifest reviews/MANIFEST_R1.txt.

**Verdict summary.** I re-derived every new step of the five proof files against the parent lines they cite. That covers R3.3 (the conditional law at U ⊊ S₀, the shift d̄⁰_n, the event E⁰ and Markov), R3.6 (composition with PARENT P1.4/P1.7), R3.1–R3.2 and R3.5 (N̄_n, C_B with 15κ_H, the index n_H), R1.2–R1.3 (exact price π_n of either sign, log(2p) kept), R1.5, R2.1–R2.8, R4.1–R4.4 and R5.1–R5.4. I found no wrong or unproved step, no hypothesis used that is not stated, and no parent result used beyond what its cited lines say. Every supersession row of `STATEMENT.md` §5 holds; for IF-START and START-R this is because C_R is existential (see E2). The manifest verifies (OK, digest 1834d1c0…). `citecheck.py` reports 438 citations with 0 MISSING/OUT-OF-RANGE. I spot-checked the DEPS hashes and they match. Every consumed W3-START and W3-START2 claim is PROVED-CHECKED/ACTIVE in `claims.tsv`. All my findings are editorial (E): record gaps, one over-strong wording in a proof remark, and loose wording in REPORT and READER_DELTA. The package is acceptable as checked mathematics as it stands.

**Gate table**

| gate | result | what I re-derived |
|---|---|---|
| G1 | PASS | **R3.3:** regression of W_l on W_{S₀}; γ² as a Schur-complement coefficient; ‖γ²‖ ≤ √s₀C₀/(c_Σ√(n log n)); ‖m‖ ≤ ‖γ²‖₁√(2N) on CN; d̄⁰_n; the 𝒲 = σ(W_{S₀}) conditioning fixes P_U, Π, μ̃, m for every U ⊊ S₀; (9.1); every line of the L9.5 proof (only a ≥ a̲, η_n ≤ a̲/2 and \|d₀\| ≤ d̄ are used) with d̄⁰_n, giving Φ⁰_n ≤ C₉√log n; Laurent–Massart at x = N/8 (2√(N²/8) + N/4 < N); P((E⁰)ᶜ); max ≤ sum over ≤ 2^{s₀} − 1 sets; Markov. **R3.1/R3.2:** P(Eᶜ) with N̄_n = n^{o(1)}; the absorption into C_B = 2d̄√(2A+1)/a̲ + 15κ_H + 1; C₇ = 9√((2A+1)/a̲). **R3.5:** b^Q_n and T_ε. **R3.6:** the admissibility of 𝒳⁰_n; r̄_n; P1.7 at (ε/8, κ = 1 < 3/2); limsup ≤ ε/4. **R1.2:** ε₁ inequalities; Step 4 needs no sign of π + c_m log n; Π ≤ ½π + C₂ in both cases; F split by the sign of π (π ≥ 0 forces π ≤ 16(1+2A)log n via (R1.0) at n ≥ 256s₀²); final −(c_m+2κ)/4. **R1.3:** G/2 = (c_V/2)log n + log(2p) − log 2 cancels the 2p in e_n; threshold with 17 log 2. **R2.1–R2.4:** log-p cancellations; the Case A/B split; t − 2M√t monotone for t ≥ M²; (f3) with x̄_n, ς_n. **R2.5:** P3.1 pigeonhole. **R2.6:** θ_n² gives δ²/τ² = G*_n exactly; Vershynin Cor. 5.35 with r = √m/4, m ≥ 256; union count. **R2.7:** e^{G_n/2} = p·n^{c_n/2}; the n_F = 16 inequality. **R4.1:** (a1)–(a3) and the A_n/B_n split. **R4.4:** the Gaussian conditional law gives (GR). **R5.2:** a = 0, 1, ≥ 2 instances; (1 − c_n)/2 → (1+2A)/10; n^{0.3−0.4A}. |
| G2 | PASS | Claim by claim, the hypotheses used equal those stated. (B-R⁺⁺)(iii) uses only Setting R, (FL-R16) and (L-gain-0). (T3⁺⁺)(b)(iii) uses (L-R⁺⁺) at Q = S₀ only for 𝔏_n(S₀) ≤ e^{C_B√log n}. VIS-c⁺⁺, VIS-m⁺⁺ and NEC-b⁺⁺ use [TK] in quantitative form plus p ≤ n^A, \|Q\| ≤ K ≤ p from Setting F. |
| G3 | PASS | No independence across columns (Markov on a sum). No p → ∞ (bounded p allowed in F2⁺⁺; R2.6 holds for every 2 ≤ p_n ≤ n^A). The n_H dependence is explicit in R3.0. Drifting witnesses start at an explicit n₅. Conditioning is on W_{S₀} or the design only. s₀ = 0 is covered: P1.4, R1.0(c), TRANSFER s ∈ {0, …, s̄}. |
| G4 | PASS | Opened every cited parent range used as a premise: L9 :94-140, L8 :37-50, L6 :11-26, L4 :22-73, L7 :12-65, L3 :95-105, L1 :15-16, :103-109, L2 :32-98, L5 :37-89, L10 :16-24, :63-87, L11 :17-100, P1 :80-158, P3 :13-75, P4 :16-90, P2 :45-58, C-MIS :54-56. Each says what is taken. Supersession rows all verified (incl. F4 via the diagonal η_n ↓ 0). Record gaps: E3, E4. |
| G5 | PASS | The constants C, c₀, C^♯ of (T1⁺⁺)(d) are unchanged. n₃ ≥ 256s₀² and n₃, n₄ are independent of Q. C_B, C_R, C₇–C₉ do not depend on n_H; the thresholds do, as declared. TRANSFER takes max/min over s ≤ s̄. |
| G6 | PASS | No new property of the coded start is used. citecheck is clean, and the parent ranges I opened say what is claimed. READER_DELTA Theorem 5 and Theorem 5F follow from (T3⁺⁺)(b)(i)/(iii), F3⁺⁺/F1⁺⁺ (η = 0) at Q = S₀, and (N3⁺⁺) via the named bridges (B5.1′, B5.3 = (D5) remark). Wording points in E9 and E10. REPORT numerics match `numerics/RESULTS.md` and `summary.csv`. |

**Per-claim table**

| id | decision |
|---|---|
| VIS-c | ACCEPT |
| VIS-m | ACCEPT |
| START-F | ACCEPT |
| F1–F3 | ACCEPT |
| F4 | ACCEPT |
| NEC-b | ACCEPT |
| NEC | ACCEPT |
| TRANSFER | ACCEPT |
| MIS | ACCEPT |
| EX | ACCEPT |
| OVL | ACCEPT |
| BR | ACCEPT |
| START-R | ACCEPT |
| IF-START | ACCEPT |

**Findings** (all E; none blocks)

1. **E** — `lemmas/R1_VIS.md:40-42` (R1.0(d)(iii)).
   - *What fails:* "At every n with p < n^A … both forms ask no more than the version-1.4 forms". For (V-mp) at instances with a > d this needs n ≥ 256s₀². At smaller n, π_n = −(a−d)(log n + 2 log(p/c_Q)) can be positive, while the (V-m) price there is 0.
   - *Why only E:* the STATEMENT remark it serves (`STATEMENT.md:68`) is asymptotic and true, and the supersession rows use the correctly restricted R1.0(c).
   - *Repair:* add "and n ≥ 256s₀² (R1.0)".
2. **E** — `STATEMENT.md:283` (supersession row IF-START, "each rate is at most the old one"), and the same spirit in row START-R.
   - *What fails:* the new C_R = C_B + 1 has C_B larger by 15κ_H than PARENT's. The implication still holds because C_R is existential: under (L-R⁺), take κ_H = 1.
   - *Repair:* reword to "each rate is of the old form n^{−1/2}e^{C√log n} (some C) or smaller".
3. **E** — `STATEMENT.md:260-264` versus `REPORT.md` §4 and §9.
   - *What fails:* §5 says consumed statuses are "to be quoted verbatim in REPORT", and REPORT does not quote them. Also, the REPORT `depends_on` fields name W3-START:ASM@stmt, :BR@proof and :TRANSFER@proof, which are absent from the §5 consumed-claim list; they are covered only by "BASE lemmas/L1–L11" and §1 (ASM). R3 uses BASE L9 and L8, so these are really consumed through proof files. All of them are PROVED-CHECKED/ACTIVE in `claims.tsv`.
   - *Repair:* add the ids to §5 and quote the statuses in REPORT §4.
4. **E** — `REPORT.md:119`, `:191`, `:220`.
   - *What fails:* VIS-c `depends_on` omits W3-START:LEAK and :AGG, which R1.3–R1.4 use ((AGG-d), [LEAK(Q)]). EX omits W3-START2-R:BR. START-R omits W3-START:BR@proof, :TRANSFER (BASE L8.2(i)) and W3-START2:BR, though R3.4–R3.5 use them. DEPS row S:EX does not list S:F1-F3, though R5.1 uses F2⁺⁺.
   - *Repair:* complete the edges.
5. **E** — `REPORT.md:24-27` and `lemmas/R3_RATE.md:118`.
   - *What fails:* the "Honest reading" sentence is not labelled HEURISTIC and cites `API_AUDIT/sharp2/TRIAGE.md`, which is outside the frozen content. The content is correct: 𝔏⁰ − 𝔏^♯ = 15√(2/π)z_n/p and 𝔏^♯ ≥ (p−s₀)/(4p).
   - *Repair:* derive it in one line from PARENT `STATEMENT.md:57-61`, or label it.
6. **E** — `REPORT.md:83`.
   - *What fails:* "the predicted approach is like n^{−0.06}". R5.2 gives only an upper bound n^{3/10−2A/5+o(1)} on one remainder term, not a predicted rate of approach.
   - *Repair:* "the upper bound used decays like n^{−0.06}".
7. **E** — `lemmas/R4_TRANSFER_COR.md:51-53`.
   - *What fails:* PARENT's "for Q = S₀" is read as Q ≡ S₀. The reading "Q = S₀ on 𝒳_n" also follows, since P(Q = S₀) ≥ P(X^r ∈ 𝒳_n) → 1.
   - *Repair:* say so.
8. **E** — `lemmas/R1_VIS.md:18-22`, `lemmas/R2_NEC.md:20-25`, `:125-129`.
   - *What fails:* the "ISSUES FOR THE LEAD" remarks are stale; the citecheck pattern is now {2,6}. R2.5(N1) uses workflow wording ("the lead's file R4 (PLAN §2)").
   - *Repair:* drop or neutralise.
9. **E** — `READER_DELTA.md:12` and `:41`.
   - *What fails:* "1 − n^{−c} for every c < ½ (equivalently n^{−1/2}e^{C√log n})" is not an equivalence. The inherited sentence "in all cases 1 − π₀(S₀) ≥ ⅓(n+1)^{−1/2} for every data set" needs s₀ < K, i.e. n ≥ 2s₀+2 ((T0)). That sentence is unchanged by this delta.
   - *Repair:* "comparable to"; "for n ≥ 2s₀ + 2".
10. **E** — `READER_DELTA.md:82`.
    - *What fails:* "Master: W3-START2-R:F3 and :F1", while the registry has one row, W3-START2-R:F1, covering F1–F3 (`REPORT.md:234`).
    - *Repair:* cite W3-START2-R:F1 (F3 and F1 clauses).

**Better-theorem proposals**

- (B-R⁺⁺)(iii) interpolates. If \|Cov(W_l, W_j \| W_U)\| ≤ C·b_n·n^{−1/2} for U ⊊ S₀ with any b_n ≤ 1, the same proof gives 𝔏^♯_n = O_P(√log n·e^{C′b_n√log n}). This connects (iii) (b_n = 1/√log n) to (i) (b_n = 1) and yields intermediate rates in (T3⁺⁺)(b)(iii).
- (T3⁺⁺)(b)(iii) uses (L-R⁺⁺) at Q = S₀ only to get 𝔏_n(S₀) = O_P(e^{C√log n}). Any bridge giving 𝔏_n(S₀) = O_P(n^{1/4}(log n)^{1/4}) would do. A version under (FL-R16), (V-R), (L-gain-0) plus such a functional bound would separate the leading-term and second-order hypotheses.
- EX F-2: the A > 3/4 threshold for (T1⁺⁺)(c) comes from the crude F4⁺⁺ bound on 𝔏_n(S₀; h). A per-column bound on the fifteen correlates (their gains are explicit in BASE L11.3) may lower it.

**Overall score: 9.3 / 10.** There are no C, S or F findings; the deduction reflects only the record and wording items above.

**Checks performed**
- Manifest verify: OK.
- Full read of STATEMENT, R1–R5, REPORT, READER_DELTA, TARGET, PLAN, BRIEF, RIDER_RULES, DEPS and the numerics RESULTS.
- Line-by-line re-derivation of the steps listed under G1.
- Opened every parent range cited as a premise (listed under G4).
- Ran `citecheck.py` (scratch output only): 438 citations, 0 bad.
- DEPS sha recomputed for 4 STATEMENT ranges and all 5 lemma files, plus REPORT: all match.
- `claims.tsv` statuses of the 30 consumed W3-START and W3-START2 rows: all PROVED-CHECKED/ACTIVE.
- Numerics paragraph checked against `summary.csv` (g1, lg0a, lg0b medians) and RESULTS tables.
- Scratch folder `.rc_tmp/` deleted. No git state changed; the working-tree changes now showing (LOG.md, `reviews/R1_council_sol.md`) are not mine, and I did not read them.

**Not checked**
- I did not re-run the numerics scripts.
- I did not read `READER_VERSIONS.md` (outside the allowed inputs), so I could not confirm that its (S1), (S2) encode p ≤ n^A and σ² fixed for Theorem 5/5F.
- I relied on BASE and PARENT proof steps as given, per the brief: L9.1–L9.4, the TK lemma, (AGG-a)–(AGG-d) and (T0).
- I did not independently verify the Vershynin Cor. 5.35 statement beyond its standard form.

`COUNCIL-VERDICT round=R1 manifest=1834d1c0941f297eef629337b02361097a0d2f02ae1596afeaa4bf322ebbab19 seat=opus score=9.3 gates=PASS`

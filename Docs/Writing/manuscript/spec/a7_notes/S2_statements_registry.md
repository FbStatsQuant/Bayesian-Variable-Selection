# S2 — Statements ↔ registry map (A6 owner-review edition)

Assignment 7, official-statements section of the specification. Transcriber: Sonnet sub-agent for the Writing manager. Read-only on Theory; no new mathematics.

**Pin.** Worktree `/home/fb31/BVS-wt/WRITING`, HEAD `0f814f19`; registry `Theory_work/INFRA/registry/claims.tsv` (553 rows; assumptions in `assumptions.tsv`, 142 rows). Status strings are quoted verbatim from the registry, cut before “; council”. The registry is at the state of its last change (commit 97f9c8c3, 11-18) per `a6_notes/H1_status_and_pins.md`.

**Sources.** A6 sections `or3_model`, `or5_assumptions`, `or6_theorems`, `supplement_or`, `appendices_or` (all under `Docs/Writing/manuscript/sections/`); `a6_notes/H1_status_and_pins.md`, `a6_notes/H2_planned_and_1M.md` §B; `Theory_work/Dept/QUEUE.md`; for statement texts the registry `file:lines` and `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` (the reader forms the A6 theorems are written from).

**Verdict key.** MATCH = the A6 statement says the same as the registry master or, where the registry row is a master in registry-internal form, the reader statement that cites it (a note records where the master is stronger or phrased differently). DIFF = A6 and the registry/reader text differ in hypotheses, conclusion, scope or target in a way the specification must settle; each DIFF is marked “A6 safe” (A6 is a consequence of the registry statement) or “A6 gap” (A6 says less than, or something not in, the registry).

**Tally.** 24 A6 statements mapped: **18 MATCH, 6 DIFF** (statements 6, 10, 14, 20, 21, 23). Items with no registry row (not results): 5 listed at the end of section A.

---

## A. Statement map

Ledger row numbers are those of A6 `app:status` (freeze ledger). `Reader` = the section of READER_VERSIONS.md the A6 text follows.

### A1. Lemma `lem:summaries` (posterior miss controls the summaries) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/or3_model.tex:87-90`; ledger row: —.
- **Reader form:** none (not a reader theorem).
- **Registry rows:**
  - `C-PACK:SL0` v1.0.1 (lemma) — `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:20-30` — status: “PROVED-CHECKED”
  - `C-PACK:SL1` v1.0.0 (corollary) — `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:39-48` — status: “PROVED; XF-checked (R34 ERROR-as-written → 9 fixes; core re-derived valid), R38/R39”
- **Comparison:**
  - SL0(i): |PIP_j − 1{j∈S0}| ≤ δ; SL0(iii): δ<½ ⇒ MPM=S0; SL0(iv): δ<½ ⇒ S0 is the unique maximiser, so HPM=S0 for every tie rule. A6 states these with δ=1−π(S0) (δ<½ ⇔ π(S0)>½).
  - Not in A6 text: the registry convention π(S0):=0 when s0>K (S0∉Ω), and the “every tie rule” clause. Both are harmless (S0∉Ω gives π(S0)=0, the hypothesis π(S0)>1/2 fails).
  - Registry row SL1 (corollary, MPM/HPM form) carries the status “PROVED; XF-checked (R34 ERROR-as-written → 9 fixes; core re-derived valid), R38/R39”, a different string from SL0; the lemma is SL0.

### A2. Theorem `thm:post-random` (posterior concentration, sub-Gaussian rows) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/or6_theorems.tex:71`; ledger row: 1.2 (Gaussian L=1 case).
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 2 (§2, lines 257-323).
- **Registry rows:**
  - `W3-D3:Thm2SG` v1.0.0 (theorem) — `Theory_work/Wave3/W3-D3/STATEMENT.md:41-57` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:P-POLY; A:FIXED-S0; A:COEF-BOUNDED; A:POP-FLOOR-5LOG; A:SUBG-SPARSE-ROWS
  - `W3-D3:B3w` v1.0.0 (lemma) — `Theory_work/Wave3/W3-D3/STATEMENT.md:59-80` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:P-POLY; A:FIXED-S0; A:COEF-BOUNDED; A:POP-FLOOR-5LOG; A:SUBG-SPARSE-ROWS
  - `W3-POST:Thm-1` v1.0.2 (theorem) — `Theory_work/Wave3/W3-POST/STATEMENT.md:61-100` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:SPARSE-EIG; A:FIXED-S0; A:P-POLY; A:BETAMIN
  - `W2-APP:POST` v1.0.7 (lemma) — `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:27-33` — status: “PROVED-CHECKED” — registry assumptions: A:LSF; A:IID-GAUSS-ROWS; A:P-POLY; A:FIXED-S0; A:GAUSS-NOISE; A:COEF-BOUNDED
  - `W3-READER:R1` v1.0.5 (lemma) — `Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md:1-59` — status: “PROVED-CHECKED”
- **Comparison:**
  - Registry Thm2SG hypotheses A1–A4 = A6 GL+DIM, SP+FSb, EFS, SGR; constants identical (5(A+1)(s0+1) log n, φ∈(0,1], L>0). The conventions for a removed column, S0∉Ω and “no column retained” (STATEMENT.md:36-38) are in A6 Appendix conventions.
  - Conclusions match (δ_n=O_P(r_n), P(HPM=MPM=S0)→1, expected max PIP error). Registry says “any tie rule” for HPM; A6 does not mention ties.
  - The ledger row 1.2 (Gaussian, L=1) is carried by the coexisting rows W3-POST:Thm-1 v1.0.2, W2-APP:POST v1.0.7, W3-READER:R1 v1.0.5 (all plain PROVED-CHECKED on main); the sub-Gaussian form is Thm2SG (new since the freeze).

### A3. Theorem `thm:dist` (distribution-level posterior contraction) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/or6_theorems.tex:125`; ledger row: 2.1.
- **Reader form:** none (W3-DIST has its own statement; READER row 2.1 cites it).
- **Registry rows:**
  - `W3-DIST:Thm-A` v1.0.3 (theorem) — `Theory_work/Wave3/W3-DIST/STATEMENT.md:185-207` — status: “PROVED-CHECKED” — registry assumptions: A:DIST-A1; A:DIST-A2; A:DIST-A3; A:DIST-A4; A:DIST-A5
- **Comparison:**
  - Registry premises A1–A5 = A6 `asm:dist` (a)–(e) (renaming: registry K → A6 L (sub-Gaussian constant), registry c → A6 c_H). Range M0≤M≤√n/log n, n≥n0, and window q_n=min{p,⌈C_q M log n⌉} with C_q=2(s(A+2)+4)/log 2 match.
  - Registry conclusion (ii), P*[Π(|S|>s+C1 M log n | Dn) > n^{−cM}] ≤ n^{−cM}, is stated in A6 `prop:dist`, not in Theorem 3; so C1 does not appear in Theorem 3. Placement only.
  - Registry notes: the posterior is read as 1 when undefined, and the exceptional set also contains the event r<p (r = retained predictors). A6 states the convention in Appendix conventions.

### A4. Proposition `prop:dist` (distribution-level, without the no-collinearity item; size bound) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:168`; ledger row: 2.1.
- **Reader form:** none.
- **Registry rows:**
  - `W3-DIST:Thm-A` v1.0.3 (theorem) — `Theory_work/Wave3/W3-DIST/STATEMENT.md:185-207` — status: “PROVED-CHECKED” — registry assumptions: A:DIST-A1; A:DIST-A2; A:DIST-A3; A:DIST-A4; A:DIST-A5
- **Comparison:**
  - Matches Theorem A (i)+(ii) and the paragraph “Without (A4)” (STATEMENT.md:200-202): radius √(M log n · log(p∨n)/n), size s+C1 M log n.
  - A6 adds the words “M may depend on n”. The registry text says “whenever n≥n0, M0≤M≤√n/log n” (a non-asymptotic statement, so any M=M_n in range is covered); this is an interpretive reading, not a separate clause.

### A5. Theorem `thm:dist-param` (parametric rate under a detectable signal) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:188`; ledger row: 2.1.
- **Reader form:** none.
- **Registry rows:**
  - `W3-DIST:Thm-B` v1.0.3 (theorem) — `Theory_work/Wave3/W3-DIST/STATEMENT.md:209-215` — status: “PROVED-CHECKED” — registry assumptions: A:DIST-A1; A:DIST-A2; A:DIST-A3; A:DIST-A4; A:DIST-A5; A:DIST-A6
- **Comparison:**
  - Theorem B (STATEMENT.md:209-215) adds A:DIST-A6 (detectable signal, 211-212); A6 states it in the same form.

### A6. Remark `cor:dist-output` (output of the sampler, conditionally on the list mass) — **DIFF**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:206`; ledger row: 2.1 (the ledger row 2.1 also carries “dist-output”).
- **Reader form:** none.
- **Registry rows:**
  - `W3-DIST:Cor-C` v1.0.3 (theorem) — `Theory_work/Wave3/W3-DIST/STATEMENT.md:217-238` — status: “PROVED-CHECKED, conditional on EX-A (exact arithmetic)” — registry assumptions: A:EX-A; A:DIST-A1; A:DIST-A2; A:DIST-A3; A:DIST-A4; A:DIST-A5
  - `W3-DIST:DIST-C` v1.0.2 (theorem) — `Theory_work/Wave3/W3-DIST/STATEMENT.md:289-318` — status: “PROVED-CHECKED, conditional on EX-A (exact arithmetic)” — registry assumptions: A:EX-A; A:DIST-RD; A:DIST-SPARSE; A:P-POLY; A:DIST-DOM; A:ENERGY; A:COEF-REP; A:DIST-ND
- **Comparison:**
  - DIFF 1 (A6 demotes it): registry Cor-C is a corollary-level theorem “under the conditions of Theorem A”; A6 states it as a Remark and says the list-mass premise is not proved. The registry premise is the same (list mass); no mathematical difference, but the status label differs.
  - DIFF 2 (A6 gap, minor): the registry excludes the small problems solved by exact enumeration; A6’s remark does not say so. A6 does say “completed run” (sampler branch), which excludes enumeration, so the exclusion is implicit.
  - DIFF 3 (notation): the registry writes “at most 40r+1 distinct models” with r the number of retained predictors; A6 writes 40p+1 with p. Equal when p is read as the retained count (A6 Section 1 setup); LIST-CODE (iii) also writes 40p+1.
  - DIFF 4 (phrasing): registry “it is the model the method reports as most probable”; A6 writes Ŝ=S0. Same content (Ŝ=hpm).
  - The A6 status string (“conditional on exact arithmetic only”) equals the registry string.

### A7. Theorem `thm:post-fixed` (posterior concentration, fixed design) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:33`; ledger row: 1.1.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 1 (§1, lines 94-230; statement 99-122).
- **Registry rows:**
  - `W3-POST:Thm-1` v1.0.2 (theorem) — `Theory_work/Wave3/W3-POST/STATEMENT.md:61-100` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:SPARSE-EIG; A:FIXED-S0; A:P-POLY; A:BETAMIN
  - `W3-POST2:C` v1.0.7 (proposition) — `Theory_work/Wave3/W3-POST2/STATEMENT.md:83-94` — status: “PROVED-CHECKED, conditional on W2-APP:POST” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:POST2-F0; A:FIXED-S0; A:P-POLY; A:POST2-C-ALT
  - `SOP:TH09` v1.0.2 (external) — `Theory_work/Wave3/W3-T03ACC/sources/statement/registry_theory_main_L68.tsv:1-1` — status: “PROVED-CHECKED (T03♯ only: the conjunction of W3-T03ACC:T03S.1–T03S.4, clause map CHECKPOINT_4.md §2” — registry assumptions: A:P-POLY; A:BETAMIN; A:ENERGY; A:SPARSE-EIG; A:FIXED-S0; A:GAUSS-NOISE
  - `W3-POST:Prop-LB` v1.0.1 (proposition) — `Theory_work/Wave3/W3-POST/lemmas/LB_rate_lower_bound.md:9-17` — status: “PROVED-CHECKED” — registry assumptions: A:EXT-FEAS
  - `W3-POST:Lemma-1a'` v1.0.1 (lemma) — `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:9-19` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:COEF-REP
- **Comparison:**
  - A6 EF = reader (A4) with |S| ≤ 2(A+1)s0+2; NC = (A5) with 3(A+1)(s0+1) log n; BC = (A3); constants (s0, A, σ*², θ̄, φ0, g0, Cβ) match.
  - A6 BM(b): “t_min √(n/log n) → ∞” vs reader “θmin ≥ σ* √(M_n log n/n)/φ0 for a fixed sequence M_n→∞”: equivalent for fixed σ*, φ0 (a rewrite).
  - A6 status box says the registry strings still read “conditional on” a posterior input; this is true of W3-POST2:C and SOP:TH09 and is consistent with the list below.

### A8. Theorem `thm:post-margin` (posterior concentration with a margin instead of beta-min) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:103`; ledger row: 1.1.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 1′ (lines 124-131).
- **Registry rows:**
  - `W3-POST2:E` v1.0.7 (theorem) — `Theory_work/Wave3/W3-POST2/STATEMENT.md:126-133` — status: “PROVED-CHECKED, conditional on W2-APP:POST” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:POST2-F0; A:POST2-OS; A:POST2-IDM; A:FIXED-S0; A:P-POLY
  - `W3-POST2:D` v1.1.7 (corollary) — `Theory_work/Wave3/W3-POST2/STATEMENT.md:99-119` — status: “PROVED-CHECKED, conditional on W2-APP:POST” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:POST2-F0; A:FIXED-S0; A:P-POLY
- **Comparison:**
  - Registry premises A:POST2-F0 / -OS / -IDM = A6 `asm:margin`. A6 sentence “under EF and BM(a) the margin holds with c_id = Cβ²φ0²(1−1/n)” matches the reader remark.

### A9. Remark `rem:no-betamin` (no beta-min needed for the in-probability form / lower bound) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:82`; ledger row: 1.1.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md remark (ii), lines 142-144.
- **Registry rows:**
  - `W3-POST:Thm-1` v1.0.2 (theorem) — `Theory_work/Wave3/W3-POST/STATEMENT.md:61-100` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:SPARSE-EIG; A:FIXED-S0; A:P-POLY; A:BETAMIN
  - `W3-POST:Thm-1(5-spec)` v1.0.0 (counterexample) — `Theory_work/Wave3/W3-POST/STATEMENT.md:90-94` — status: “COUNTEREXAMPLE (numerical, E5; leading-order analytic sketch, unchecked)”
  - `C-PACK:SL1'` v1.0.0 (corollary) — `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:65-66` — status: “PROVED; XF-checked (R34 ERROR-as-written → 9 fixes; core re-derived valid), R38/R39”
- **Comparison:**
  - Matches Theorem 1 item 5 (a)(b) and the reader remark. The counterexample row W3-POST:Thm-1(5-spec) is “numerical, unchecked” in the registry; A6 does not rest a result on it.

### A10. Theorem 6 `rem:sharp` (the rate cannot be improved), parts (a) and (b) — **DIFF**

- **A6 location:** `Docs/Writing/manuscript/sections/or6_theorems.tex:277`; ledger row: 1.3.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 3 (lines 324-442; statement 330-348).
- **Registry rows:**
  - `W3-PSHARP:B` v1.0.1 (corollary) — `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:90-114` — status: “PROVED-CHECKED”
  - `W3-PSHARP:A` v1.0.0 (proposition) — `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:46-77` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:PSHARP-COEF; A:PSHARP-WORTH; A:PSHARP-WSPH
  - `W3-PSHARP-R:AE` v1.0.0 (proposition) — `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:61-92` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:PSHARP-COEF; A:PSHARP-WORTH-E; A:PSHARP-WSPH-E
  - `W3-PSHARP-R:A2C` v1.0.0 (proposition) — `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:94-100` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:ENERGY; A:PSHARP-COEF; A:PSHARP-WORTH
- **Comparison:**
  - (a) every-design bound π(S) ≤ (1+(|S|+1)/(3√n))⁻¹: MATCH (Prop A / Cor B).
  - (b) DIFF (A6 gap): (i) A6 attaches “with p ≤ n^A” grammatically to both alternatives (orthogonal nulls or Gaussian nulls); the reader attaches it to the Gaussian alternative only. (ii) The master (W-sph-E) requires (log p)² = o(n) and (r0+1) log(pn) = o(n) and takes X_{S0} and θ* deterministic, handling the random case by conditioning on events of probability → 1. A6 says “independent of the true predictors” and does not state X_{S0}, θ* deterministic.
  - The expectation display (sharp-b) matches Cor A1-E; the in-probability display matches Cor A1. The registry rows are PROVED-CHECKED.

### A11. Theorem `thm:omitted` (posterior concentration with omitted predictors) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:139`; ledger row: 1.4.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 4 (lines 443-567; statement 449-466).
- **Registry rows:**
  - `W3-MISR-R:CorGb-plus` v1.0.3 (corollary) — `Theory_work/Wave3/W3-MISR-R/STATEMENT.md:94-108` — status: “PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P” — registry assumptions: A:MISR-OVC; A:MISR-POP-SNR; A:GAUSS-CAND-ROWS; A:MISR-OV; A:CORR-FLOOR; A:FIXED-S0; A:P-POLY
  - `W3-MISR:MIS(i)` v1.0.2 (theorem) — `Theory_work/Wave3/W3-MISR/STATEMENT.md:110-123` — status: “PROVED-CHECKED, conditional on W2-APP:POST” — registry assumptions: A:MISR-GRC; A:MISR-ESNR; A:MISR-IDM-SNR; A:POST2-F0; A:POST2-OS; A:FIXED-S0; A:P-POLY
- **Comparison:**
  - Compared against the reader statement only (the master text W3-MISR-R/STATEMENT.md:48-108 was not re-read in full). A6 asm:omitted (a)–(c) + DIM + sC≥1 = reader (A0)–(A3); constants and conclusions match.
  - Status string still reads “conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P”, matching A6’s statement that the registry strings still read “conditional on”.
  - A6 `ex:omitted` is an example, not a result, and has no registry row.

### A12. Theorem `thm:start` (the start law) + the unlabelled leakage paragraph — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:227 (leakage paragraph 236-238)`; ledger row: 3.3.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 5 (lines 568-659; statement 574-605).
- **Registry rows:**
  - `W3-START2-R:START-R` v1.0.1 (theorem) — `Theory_work/Wave3/W3-START2-R/STATEMENT.md:226-240` — status: “PROVED-CHECKED” — registry assumptions: A:START-R-FL; A:START-R-V; A:START2R-R-L; A:START2R-R-L0
  - `W3-START2-R:BR` v1.0.0 (lemma) — `Theory_work/Wave3/W3-START2-R/STATEMENT.md:217-225` — status: “PROVED-CHECKED” — registry assumptions: A:START-R-FL; A:START-R-V; A:START2R-R-L; A:START2R-R-L0
  - `W3-START:FLOOR` v1.0.0 (theorem) — `Theory_work/Wave3/W3-START/STATEMENT.md:241-243` — status: “PROVED-CHECKED” — registry assumptions: A:EX-A; A:BLOCK-LE-16
- **Comparison:**
  - NL with |H_l| ≤ e^{κ_H √log n}, C_L n^{−1/2}, r°_n (n log n)^{1/4} → 0 matches. FLOOR (T0): 1−π0(S) ≥ f_n(|S|)/(1+f_n(|S|)) ≥ ⅓(n+1)^{−1/2} for n ≥ 4, |S|<K, is stated in A6 for S0 with s0<K. START-R(iii) gives o0 = O_P(√(log n/n)), hence 1−π0(S0) = O_P(...). The leakage paragraph matches the reader’s second display.

### A13. Theorem `thm:reported` (the reported model equals the true model) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/or6_theorems.tex:161`; ledger row: 3.1.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 6 (lines 660-814; statement 665-697).
- **Registry rows:**
  - `W3-RM2-R:RM2-R-plus` v1.0.2 (theorem) — `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:177-182` — status: “PROVED-CHECKED” — registry assumptions: A:LSF; A:IID-GAUSS-ROWS; A:RM-FLR; A:PTV; A:RM2-LFEAS; A:RM2-LGAIN-R; A:RM2-LLOC-R; A:RM2-LSIZE-B-R; A:RM2-HSIZE-RHO; A:RM2-W-R; A:OP; A:BLOCK-LE-16; A:DELIV-D
  - `W3-RM2-R:RM0-plus` v1.0.2 (theorem) — `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:118-143` — status: “PROVED-CHECKED”
  - `W3-RM2-R:DLV-0` v1.0.2 (lemma) — `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:144-163` — status: “PROVED-CHECKED”
  - `W3-RM2:RM2-R` v1.0.3 (theorem) — `Theory_work/Wave3/W3-RM2/STATEMENT.md:216-218` — status: “PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1” — registry assumptions: A:LSF; A:IID-GAUSS-ROWS; A:RM-FLR; A:PTV; A:RM2-LFEAS; A:RM2-LGAIN-R; A:RM2-LLOC-R; A:RM2-LSIZE-B-R; A:RM2-HSIZE-RHO; A:RM2-W-R; A:OP; A:BLOCK-LE-16
- **Comparison:**
  - MATCH to the reader form. A6 `asm:reported` (a)(b)(c) = reader (A4), (A5) second part, (A6); EFS+(b) = (A5); V = (A3); FSt+GR = model + (A2); b_H=ρ with 15 b_H+b<½. Conclusion, eq:reported and eq:delivery match.
  - The registry master RM2-R-plus is a delta statement (STATEMENT.md:177-182) whose hypotheses are RM2-R’s (W3-RM2/STATEMENT.md:172-202) and is stronger than the reader form: it adds [MODE] and the error split. It is written in registry-internal hypothesis names (T1-R, FL-R, V-R, L-R^b), not the reader’s. The A6 statement is a consequence of the master.
  - A6 adds “Convention C1” where the reader uses (S3)/(S4). The registry master W3-RM2:RM2-R still reads “conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1”; the plus-forms (RM2-R-plus, RM0-plus, DLV-0) are plain PROVED-CHECKED, which is what A6’s “no open condition” relies on.
  - Code-side rows C-DLV:L2-S3 and C-DLV:P1-Inventory read “CODE-CHECKED (second seat, code reading; holds at pin 4676af6 after amendments A-1–A-7)”; they are code readings, not proofs.

### A14. Theorem `thm:reported-fixed` (the reported model, fixed design) — **DIFF**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:266`; ledger row: 3.2.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 7 (lines 815-931; statement 821-857).
- **Registry rows:**
  - `W3-RM2-R:RM2-F-plus` v1.0.2 (theorem) — `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:166-176` — status: “PROVED-CHECKED” — registry assumptions: A:T1F-FLAT; A:RM-FL; A:RM2-V-FLAT; A:RM2-LFEAS-GAIN; A:RM2-LSIZE-B; A:RM2-BM-W-PLUS; A:RM2-W; A:OP; A:BLOCK-LE-16; A:DELIV-D
  - `W3-RM2:RM2-F` v1.0.3 (theorem) — `Theory_work/Wave3/W3-RM2/STATEMENT.md:206-214` — status: “PROVED-CHECKED” — registry assumptions: A:T03-HYP; A:RM-FL; A:RM-V; A:RM2-LFEAS-GAIN; A:RM2-LSIZE-B; A:RM2-BM-W; A:RM2-W; A:OP; A:BLOCK-LE-16
- **Comparison:**
  - DIFF (A6 safe direction: A6 hypotheses are stronger than the reader’s, so the A6 statement follows from the reader/master statement).
  - (i) Visibility: A6 `rf-vis` asks a deterministic ω_n → ∞ with δ²_{U,j} ≥ ω_n log n; the reader (A3) asks a fixed M_V larger than an explicit constant (Remark (a)) with δ²_{U,j} ≥ M_V log n. The master’s (V♭) is at constant level.
  - (ii) Beta-min: A6 takes BM(b) (θmin √(n/log n) → ∞), i.e. the reader’s second alternative θmin ≥ σ*√(M_n log n/n)/φ0, M_n → ∞. The reader also allows a fixed C_β above an explicit constant (first alternative).
  - (iii) Leakage-set size (d2): A6 asks θ*²_min n/(|Q|+log n) → ∞; the reader (A5)(b) asks θ*²_min ≥ C_Q σ*²(|Q|+log n)/(n φ0²) for a fixed C_Q above an explicit constant. A6’s form implies the reader’s for large n.
  - Lat(Q) = {T : S0 ⊆ T ⊆ Q} (or5_assumptions.tex:228) is the reader’s “S0 ⊆ T ⊆ Q”. The floors, bounded leakage, (d1) and the local-regression clauses are the same.
  - Registry status: both the plus-form RM2-F-plus (STATEMENT.md:166-176) and RM2-F are plain PROVED-CHECKED (no conditional string), as A6’s “no open condition” says.

### A15. Theorem `thm:screen` (certified screening) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/or6_theorems.tex:208`; ledger row: 3.7.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 8 (lines 932-1050; statement 938-953).
- **Registry rows:**
  - `W3-SCR:A1` v1.0.0 (corollary) — `Theory_work/Wave3/W3-SCR/STATEMENT.md:158-163` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:EX-A; A:SCR-DF; A:SCR-A1-COND
  - `W3-SCR:A-inf` v1.0.0 (theorem) — `Theory_work/Wave3/W3-SCR/STATEMENT.md:87-90` — status: “PROVED-CHECKED”
  - `W3-SCR:SCR-A` v1.0.0 (theorem) — `Theory_work/Wave3/W3-SCR/STATEMENT.md:79-85` — status: “PROVED-CHECKED” — registry assumptions: A:GAUSS-NOISE; A:EX-A; A:SCR-SV
- **Comparison:**
  - MATCH to the reader form: floor λmin(R̂_S) ≥ κ for |S| ≤ q_n+s0, θ*_min ≥ b0, ‖θ*‖₁ ≤ M, (q_n+1) log p + log n ≤ c1 n with c1 = κ²b0²/(200(M²+σ*²)); A6 names k_n, t_low, M1, c_SB.
  - The master A1 needs only the weaker directional floor φ^d_n(q_n) ≥ κ (registry short: “Directional floor κ”); A6 and the reader assume the full floor on |S| ≤ q_n + s0. A6 hypotheses are therefore stronger than the master’s, and A6 says “SP is not assumed”, which agrees with the master (no bound on s0).
  - The master A-inf (STATEMENT.md:87-90) is the non-asymptotic form with no p ≤ n^A. A6 does not state A-inf.

### A16. Proposition `prop:unbiased` (each island’s evidence estimate is unbiased) + the pooled sentence (or6_theorems.tex:253) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/or6_theorems.tex:248 (pooled sentence :253)`; ledger row: 3.5.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md §10 remark (row 3.5).
- **Registry rows:**
  - `W1-N1:Thm-N1` v1.0.0 (theorem) — `Theory_work/Wave1/W1-N1/STATEMENT.md:98-104` — status: “PROVED-CHECKED” — registry assumptions: A:OP; A:N1-KERNEL; A:EX-A-HU; A:CAL
  - `W3-READER:PoolZ` v1.0.3 (corollary) — `Theory_work/Wave3/W3-READER/STATEMENT.md:12-39` — status: “PROVED-CHECKED”
  - `W3-AUDIT-AX:FR` v1.0.0 (lemma) — `Theory_work/Wave3/W3-AUDIT/track_A_X/X1_T12/STATEMENT.md:27-42` — status: “PROVED-CHECKED”
  - `W1-N1:B` v1.0.0 (lemma) — `Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:33-43` — status: “PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08.”
  - `W1-N1:F` v1.0.0 (lemma) — `Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md:21-23` — status: “PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08.”
- **Comparison:**
  - Thm-N1 (N1): E[Ẑ_r · H_r(h) | 𝓒] = Z·π(h) a.s. on 𝒜∩{r ≤ R′}; its “in particular” clause (STATEMENT.md:104) is E[W_r | 𝓒] = 1. A6 states the case h ≡ 1 and the pooled form E[Ẑ | calibration] = Z on 𝒜 (PoolZ, by linearity, R′ = 4). Premises of N1: EX-A, EX-S/H-U, START, KERNEL, CAL, SI, MEAS, potential run; A6 collects them in Convention C3.
  - N1 is stated for the frozen v2.2.1 core; for the core of record the same identity is W3-SAMP:MR (MR-b) with h ≡ 1 (STATEMENT.md:107-111), with the code bridge carried by W3-SAMP:CC.
  - W1-N1:B and W1-N1:F carry the old string (quoted above); the line checks are in W3-AUDIT-AW:ISL and :FRZ (PROVED-CHECKED). The registry row PoolZ is PROVED-CHECKED, while the claim file `Theory_work/Wave3/W3-READER/STATEMENT.md:13` still shows “PROVED (by this seat, unchecked)” in its own header (file-header stale, not the registry).

### A17. Corollary `cor:famc` (block and autoregressive designs) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:280`; ledger row: — (no ledger row; registry id W3-FAMC:Cor-FAMC).
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md §1R / FAMC (W3-FAMC/STATEMENT.md:25-81).
- **Registry rows:**
  - `W3-FAMC:Cor-FAMC` v1.0.0 (corollary) — `Theory_work/Wave3/W3-FAMC/STATEMENT.md:49-81` — status: “PROVED-CHECKED” — registry assumptions: A:IID-GAUSS-ROWS; A:GAUSS-NOISE; A:P-POLY; A:FIXED-S0; A:COEF-BOUNDED; A:OP; A:BLOCK-LE-16; A:DELIV-D; A:FAMC-DESIGN; A:FAMC-COEF
- **Comparison:**
  - A6 (a)–(d) = BLK-1/BLK-s/AR-s/AR-sep/BLK-g/AR-g; “bounded block size, uniformly well conditioned” = (BLK) g≥1, λmin(Σn) ≥ c > 0. B null for AR, possibly not null for block designs [R1-S2]: matches. Conclusion and qualifications (integer limits, bounded domain, time guard) match.
  - A6 status (“recorded on main at 8b4d3101”) is a commit reference; the registry has the same row id.

### A18. Corollary `cor:list` (list-renormalised estimates) + follow-on sentence (supplement_or.tex:338-340) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:314`; ledger row: 3.1 (list outputs).
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 6L (≈1443).
- **Registry rows:**
  - `W3-D5P:LIST-R` v1.0.0 (corollary) — `Theory_work/Wave3/W3-D5P/STATEMENT.md:99-125` — status: “PROVED-CHECKED” — registry assumptions: A:LSF; A:IID-GAUSS-ROWS; A:RM-FLR; A:PTV; A:RM2-LFEAS; A:RM2-LGAIN-R; A:RM2-LLOC-R; A:RM2-LSIZE-B-R; A:RM2-HSIZE-RHO; A:RM2-W-R; A:OP; A:BLOCK-LE-16; A:DELIV-D; A:EX-A; A:IMPL-LIST
  - `W3-D5P:LIST-K` v1.0.0 (lemma) — `Theory_work/Wave3/W3-D5P/STATEMENT.md:67-75` — status: “PROVED-CHECKED”
  - `W3-D5P:LIST-CODE` v1.0.0 (implementation) — `Theory_work/Wave3/W3-D5P/STATEMENT.md:79-95` — status: “CODE-CHECKED (code reading at core 4676af6)” — registry assumptions: A:OP; A:EX-A
- **Comparison:**
  - Displays eq:list-pip, eq:list-z, eq:list-mpm match LIST-K (a)–(d) and LIST-R (i)–(iii): max_j|pip_T(j)−1{j∈S0}| ≤ ε_n; |pip_T(j) − PIP_j| ≤ ε_n; log Z + log(1−ε_n) ≤ logZ_T ≤ log Z ⇒ 1−ε_n ≤ Z_T/Z ≤ 1; mpm_T = S0 when ε_n<½. The rate ε_n = O_P(r_n) needs p ≥ 2 for all large n (registry [SL1-3]); A6 DIM has p ≥ 2.
  - STATUS WORDING NOTE: A6’s status box says “Proved and independently checked … no condition”. The registry rows are LIST-K and LIST-R PROVED-CHECKED, but the code-conformance row LIST-CODE (premise IMPL-LIST) is “CODE-CHECKED (code reading at core 4676af6)”, i.e. a code reading pinned at an earlier core commit, not a proof; A6 says this correctly (“pinned at an earlier core commit; its re-pin … is a later step”).
  - The follow-on sentence (pathwise list-mass premise supplied; probability form needs an open raw-scale bridge) is the same fact as READER_VERSIONS.md:1443 (“Relation to Corollary 9C (D121)”) and the QUEUE “Named open items” raw-scale bridge (Section C).

### A19. Remark `thm:outputs` (the reported estimates are consistent, on designs without leakage) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:364`; ledger row: 3.6.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 10 (§10, lines 1282-≈1345).
- **Registry rows:**
  - `W3-SAMP:C` v1.1.6 (theorem) — `Theory_work/Wave3/W3-SAMP/STATEMENT.md:149-163` — status: “PROVED-CHECKED” — registry assumptions: A:N1-KERNEL; A:CAL; A:EX-A-HU; P:POST-CONC; A:P-START
  - `W3-SAMP:LT#` v2.0.6 (theorem) — `Theory_work/Wave3/W3-SAMP/STATEMENT.md:126-140` — status: “PROVED-CHECKED” — registry assumptions: A:N1-KERNEL; A:CAL; A:EX-A-HU; P:POST-CONC; A:NC-R; A:BLOCK-LE-16
  - `W3-SAMP:D` v2.1.6 (theorem) — `Theory_work/Wave3/W3-SAMP/STATEMENT.md:97-105` — status: “PROVED-CHECKED” — registry assumptions: A:N1-KERNEL; A:CAL; A:EX-A-HU; A:P-MAP; A:P-OVL; A:IND-T
  - `W3-READER:R4` v1.0.3 (lemma) — `Theory_work/Wave3/W3-READER/lemmas/R4_printed_outputs.md:1-48` — status: “PROVED-CHECKED”
  - `W3-START2-R:IF-START` v1.0.0 (corollary) — `Theory_work/Wave3/W3-START2-R/STATEMENT.md:241-246` — status: “PROVED-CHECKED”
- **Comparison:**
  - A6 states it as a Remark; the reader states it as Theorem 10. Hypotheses: A6 GR, DIM (p>s0), FSt, EFS, V, NL, C1, C3 = reader (A1)–(A5) with (A4)(A5) the visibility and no-leakage of Thm 5. ρ_n := n^{−1/2} e^{C√log n}; eq:outputs-rate and eq:outputs-sel match; scope (sampler branch only; enumeration not covered) matches; “no lower bound on P(𝒜)” matches.
  - The master C (C-v) is PLAIN PROVED-CHECKED on main (its “conditional on W1-N1:B, W1-N1:F” was discharged at main 20d01e52).
  - A6’s “What is not claimed” (i)–(iii) are not new statements except (iii), listed separately as statement 20.

### A20. Item (iii) of “What is not claimed” (pooling cannot make things worse; ledger row 4.1) — **DIFF**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:388-390`; ledger row: 4.1.
- **Reader form:** READER R4 (lemmas/R4_printed_outputs.md:1-48).
- **Registry rows:**
  - `W3-SAMP:LT#` v2.0.6 (theorem) — `Theory_work/Wave3/W3-SAMP/STATEMENT.md:126-140` — status: “PROVED-CHECKED” — registry assumptions: A:N1-KERNEL; A:CAL; A:EX-A-HU; P:POST-CONC; A:NC-R; A:BLOCK-LE-16
- **Comparison:**
  - DIFF (target): registry LT-d states ‖pip_primary − 1_{S0}‖∞ ≤ max_r ‖p̂_r − 1_{S0}‖∞ (distance to the truth indicator). A6 says “never farther from the exact ones [exact PIPs], in the largest coordinate, than those of the worst island”. The A6 claim follows by the same convexity step (the pooled PIP is the equal-weight mean of the islands’ PIPs: ‖mean − x‖∞ ≤ max_r ‖p̂_r − x‖∞ for any x), but the registry text records it for 1_{S0}, not for the exact PIPs. Either re-target the sentence to 1_{S0} or cite the one-line convexity proof.
  - LT# status: plain PROVED-CHECKED on main.

### A21. Remark `rem:alt-route` (an alternative route for the PIPs, MPM, HPM) — **DIFF**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:411`; ledger row: 3.6.
- **Reader form:** Theory_work/Wave3/W3-READER/READER_VERSIONS.md Thm 10 “alternative route (remark)”.
- **Registry rows:**
  - `W3-SAMP:TR` v2.1.6 (theorem) — `Theory_work/Wave3/W3-SAMP/STATEMENT.md:165-177` — status: “PROVED-CHECKED” — registry assumptions: A:N1-KERNEL; A:CAL; A:EX-A-HU; P:POST-CONC; A:P-OVL-INF
  - `W3-AUDIT-A:OVL` v1.0.3 (lemma) — `Theory_work/Wave3/W3-AUDIT/track_A/T8_OVL/STATEMENT.md:27-48` — status: “PROVED-CHECKED”
- **Comparison:**
  - DIFF (A6 gap): A6 does not state the result: “under a global-overlap condition (stated in full with the proof)”, but the proof and the condition are not in the document. The registry statement is Theorem TR (STATEMENT.md:165-177): with M := max_S π(S)/π0(S), e_L := (1−1/M)^L, E‖p̂_r − 1_{S0}‖∞ ≤ g + e_L; P(MPM ≠ S0) ≤ 2(g+e_L); P(S0 ∉ 𝓜_r) ≤ δ+e_L; (TR-d) under P-CONC and P-OVL∞, P(𝒜 ∩ {‖pip_primary − 1_{S0}‖∞ > ε}) → 0, P(𝒜 ∩ {MPM ≠ S0}) → 0, P(completed ∩ {Ŝ ≠ S0}) → 0; production corollary P-OVL∞ ⇔ P(𝒜 ∩ {M > ε log n}) → 0 for every ε > 0.
  - The registry itself labels P-OVL∞ as “not certified by any output” and not implied by (or implying) π0(S0) → 1; A6’s “named open premise” is consistent.
  - W3-AUDIT-A:OVL is the audit of the overlap lemma (PROVED-CHECKED).

### A22. Remark `rem:thm2x` (smaller sets, in expectation) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:518`; ledger row: 1.2 (extension).
- **Reader form:** none.
- **Registry rows:**
  - `W3-D2:Thm2X` v1.0.3 (theorem) — `Theory_work/Wave3/W3-D2/STATEMENT.md:29-48` — status: “PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P” — registry assumptions: A:IID-GAUSS-ROWS; A:GAUSS-NOISE; A:P-POLY; A:FIXED-S0; A:CORR-FLOOR-LOG; A:POP-SNR
  - `W3-D2:Cor2X` v1.0.0 (corollary) — `Theory_work/Wave3/W3-D2/STATEMENT.md:50-58` — status: “PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P” — registry assumptions: A:IID-GAUSS-ROWS; A:GAUSS-NOISE; A:P-POLY; A:FIXED-S0; A:COEF-BOUNDED; A:CORR-FLOOR-LOG
- **Comparison:**
  - A6: i.i.d. Gaussian rows, floor on |T| ≤ 3(A+1)(s0+1) log n on the row correlation matrix, σ² = σ_n², β*ᵀΣβ* ≤ M0 σ², n min_j Σ_jj β_j²/(σ² log n) → ∞, then E[1−π(S0)], P(HPM≠S0), P(MPM≠S0), E max_j|PIP_j−1{j∈S0}| all O(r_n): = Thm2X (A1)–(A3) and display. Cor2X shows the recorded Thm 2 hypotheses give Thm 2X with c := φ², M0 := s0² b_hi²/σ*², ρ_n ≥ n b_lo²/(σ*² log n).
  - Status string equals A6’s (conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P).

### A23. Remark `rem:vis` (when visibility holds) — **DIFF**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:531`; ledger row: —.
- **Reader form:** Lemma VIS (track V, V1_VIS).
- **Registry rows:**
  - `W3-AUDIT-V:VIS` v1.0.1 (lemma) — `Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/STATEMENT.md:29-59` — status: “PROVED-CHECKED”
- **Comparison:**
  - DIFF (A6 gap, minor): A6 says visibility holds “with a margin that does not depend on n” for aligned signs and generic position, but does not state the uniformity conditions of Lemma VIS: Σ positive definite for the sign route; fixed θ_lo and a floor c̲ := inf_n c16(Σ_n) > 0 (VIS-a: margin ≥ θ_lo c16); for the generic route δ := inf_n dist(ϑ_n, B) > 0 and a = c̲ δ (VIS-b). “autoregressive correlation (moderate or not)” is true only for a fixed ρ (c16 ≥ (1−|ρ|)/(1+|ρ|)).
  - A6’s riboflavin example (four true predictors spread apart, four tiles once p ≥ 16,352, margin ≥ 0.1 min_k|θ*_k|) is the D18 computation (track V LOG 14:05 / CHECKPOINT_2 line 47 / PROOF.md:108), recorded in the proof remark and not as a registry statement row; “clustered in one tile … no usable margin” corresponds to “clustered bound |Cov| ≤ 6.9e-9” in the same LOG.
  - The “Not covered” examples (strong factor with mixed signs; coefficients 1 and −2 at correlation 0.5) match the “Not claimed” list of V1_VIS/STATEMENT.md.

### A24. Remark `rem:dist-asm` (on the assumptions of the distribution-level result) — **MATCH**

- **A6 location:** `Docs/Writing/manuscript/sections/supplement_or.tex:548`; ledger row: 2.1.
- **Reader form:** none.
- **Registry rows:**
  - `W3-DIST:Thm-A` v1.0.3 (theorem) — `Theory_work/Wave3/W3-DIST/STATEMENT.md:185-207` — status: “PROVED-CHECKED” — registry assumptions: A:DIST-A1; A:DIST-A2; A:DIST-A3; A:DIST-A4; A:DIST-A5
  - `W3-DIST:Cor-C` v1.0.3 (theorem) — `Theory_work/Wave3/W3-DIST/STATEMENT.md:217-238` — status: “PROVED-CHECKED, conditional on EX-A (exact arithmetic)” — registry assumptions: A:EX-A; A:DIST-A1; A:DIST-A2; A:DIST-A3; A:DIST-A4; A:DIST-A5
- **Comparison:**
  - A summary remark: no beta-min condition, no fixed lower bound on eigenvalues (A4 asks only c_ψ/n); Gaussian predictors satisfy (c) with L = 1; without (d) the radius gains a factor √log(p∨n) (prop:dist); display (dist-i) with (d) carries over to the list when the list holds mass ≥ n^{−c_H M/2} (rem cor:dist-output). Consistent with the registry statements of statements 3, 4 and 6.

**Items with no registry row (not results):**

- `rem:screen` (or6_theorems.tex:228): “not claimed” plus numerics; no result.
- `rem:moderate-n` (supplement_or.tex:69): heuristic, not a theorem; no registry row.
- `ex:omitted` (supplement_or.tex:155): an example.
- Algorithm 1 (calibration) and the Markov moves (supplement_or.tex:421-515): method description; not results.
- `cor:famc`’s “Not covered” paragraph; `cor:list` list-renormalised definitions: definitions / scope statements.

---

## B. Assumptions ↔ statements ↔ registry premise ids

Registry premise ids are the `A:*`/`P:*` rows of `assumptions.tsv` (id, source) and the `assumptions` column of the master claim rows. The pairing of an A6 label with an id is made from the clause text; “verified” = clause-by-clause against the registry statement (Thm2SG, Thm-A); “by name” = by the id’s name and its source line, not re-read clause by clause.

| A6 assumption (location) | statement | used by (A6 statements) | registry premise id(s) | pairing |
|---|---|---|---|---|
| GL Gaussian linear model, fixed σ*² (or5:78) | Data = linear + independent Gaussian noise; σ*²>0 fixed | 2, 7, 8, 15, 10(b), 14 | A:GAUSS-NOISE (`Wave1/W1-GEN/STATEMENT.md:29`) | verified (Thm2SG) |
| DIM 2 ≤ p ≤ n^A (or5:90) | Dimension | 2, 7, 8, 11, 13, 14, 12 (p>s0), 19 (p>s0), 10(b) | A:P-POLY (`Wave1C/FINAL/sections/s3_posterior.tex:6`) | verified (Thm2SG) |
| SP s0 ≥ 1 fixed (or5:103) | Sparsity | 2, 7, 8, 14 | A:FIXED-S0 (`s3_posterior.tex:6`) | verified (Thm2SG) |
| GR i.i.d. Gaussian rows, correlation matrix (or5:120) | Row law | 13, 12, 19, 17, 22 | A:IID-GAUSS-ROWS (`Wave2/W2-UNI/STATEMENT.md:38`) | by name (Cor2X, FAMC list it) |
| SGR sub-Gaussian rows on sparse directions (or5:123) | Row law | 2 | A:SUBG-SPARSE-ROWS (`Wave3/W3-D3/STATEMENT.md:41-57`) | verified (Thm2SG) |
| FSb raw-scale signal bounds b_lo ≤ |β*_j| ≤ b_hi (or5:144) | Signals | 2 | A:COEF-BOUNDED (`Wave2/W2-APP/lemmas/L1_POST.md:11`) | verified (Thm2SG) |
| FSt standardised signals, fixed σ*², θ_lo ≤ |θ*_j| ≤ θ_hi (or5:147) | Signals | 13, 12, 19 | A:COEF-BOUNDED; A:GAUSS-NOISE; A:FIXED-S0 (reader Setting R) | by name |
| EFS population floor on |S| ≤ 5(A+1)(s0+1) log n (or5:167) | Floor | 2, 13, 19 | A:POP-FLOOR-5LOG (`Wave3/W3-D3/STATEMENT.md:41-57`); for 22 A:CORR-FLOOR-LOG (`Wave3/W3-D2/STATEMENT.md:35-36`, 3(A+1)(s0+1) log n) | verified (Thm2SG) |
| V visibility, |Cov(W_j, Wᵀθ* | W_U)| ≥ a, |U| ≤ 15 (or5:233) | Visibility | 13, 12, 19 | A:RM-V; A:START-R-V PTV(a_V) (`Wave3/W3-START/STATEMENT.md:162`); A:PTV (`Wave2/W2-APP/lemmas/L3_LOC.md:28`); A:RM2-V-FLAT at constant level (`Wave3/W3-RM2-R/STATEMENT.md:101-105`) | by name |
| NL no leakage as seen by the start law (supp:349) | Start law | 12, 19 | A:START2R-R-L, A:START2R-R-L0 (`Wave3/W3-START2-R/STATEMENT.md:70-87`); A:START-R-L (`W3-START/STATEMENT.md:163`) | by name; A:START-R-FL for the floor |
| `asm:dist` (a)–(e) (or5:191) | Distribution-level setting | 3, 4, 5, 6, 24 | A:DIST-A1 … A:DIST-A5 (`Wave3/W3-DIST/STATEMENT.md:136-183`); (f) detectable signal: A:DIST-A6 (:209-215); EX-A for 6: A:EX-A | verified (Thm-A) |
| `asm:reported` (a)(b)(c) (or5:259) | Leakage set, floor, local regressions | 13, 17, 18 (14 uses the fixed-design analogue below) | A:RM2-LLOC-R, A:RM2-LGAIN-R, A:RM2-LSIZE-B-R, A:RM2-HSIZE-RHO, A:RM2-LFEAS, A:RM2-W-R (`Wave3/W3-RM2/STATEMENT.md:176-197`) | by name |
| `asm:reported-fixed` (supp:247) | Fixed-design visibility and leakage | 14 | A:RM2-V-FLAT, A:RM2-BM-W-PLUS, A:RM2-LFEAS-GAIN, A:RM2-LSIZE-B, A:RM2-BM-W, A:RM2-W (`Wave3/W3-RM2/STATEMENT.md:131-145`; `W3-RM2-R/STATEMENT.md:101-112`) | by name |
| BC, EF, NC, BM(a)(b) (supp:15–28) | Fixed-design conditions | 7, 8, 14 | A:T03-HYP (`s3_posterior.tex:5-13`), A:SPARSE-EIG, A:BETAMIN (BM-inf or BM(c)), A:ENERGY | by name |
| `asm:margin` (supp:94) | Identifiability margin | 8 | A:POST2-F0, A:POST2-OS, A:POST2-IDM | by name |
| `asm:omitted` (supp:126) | Omitted-part conditions | 11, 22 | A:MISR-OVC, A:MISR-OV, A:MISR-POP-SNR, A:GAUSS-CAND-ROWS, A:CORR-FLOOR; (for 22) A:POP-SNR, A:CORR-FLOOR-LOG | registry side verified (ids from the `assumptions` column of CorGb-plus and Thm2X); pairing to the A6 items by name |
| Screening assumptions (in text, or5:313–327) | Floor of budget size, signal bounds, budget inequality | 15 | A:SCR-DF, A:SCR-A1-COND, A:SCR-SV, A:GAUSS-NOISE, A:EX-A (master A1); A:SCR-SVINF for A-inf | by name; master floor is the weaker directional one |
| Conventions C1, C2, C2p, C3 (or5:335–345; appendices app:conventions) | Conventions: the method as coded, delivery, calibration | 13, 14, 16, 18, 19, 12 | A:EX-A; A:EX-A-HU; A:OP; A:N1-KERNEL; A:CAL (`Wave1/W1-N1/STATEMENT.md:68`); A:DELIV-D; A:IDEAL-W+ (`Theory_work/Dept/research/FUNI_transfer/TR1_sol.md §2`); A:IMPL-LIST (`Wave3/W3-D5P/STATEMENT.md:59-63`) | by name |
| Witness-design conditions (rem:sharp(b)) (or6:277) | Energy bounds, orthogonal or spherical null block | 10 | A:ENERGY; A:PSHARP-COEF; A:PSHARP-WORTH(-E); A:PSHARP-WSPH(-E) (`Wave3/W3-PSHARP/STATEMENT.md:50-60`; `W3-PSHARP-R/STATEMENT.md:49-57`) | verified (see A10) |
| FAMC family conditions (supp:280) | Block or AR design; no cancellation | 17 | A:FAMC-DESIGN, A:FAMC-COEF (`Wave3/W3-FAMC/STATEMENT.md:53-76`); also A:BLOCK-LE-16, A:DELIV-D | verified (Cor-FAMC assumptions column) |

Gaps in this table: the registry’s `assumptions` column for the plus-forms RM2-R-plus and RM2-F-plus is empty or in registry-internal names; their A6 pairings are by name only (marked). A6 hypotheses that have no registry premise id: the “Convention C1/C2/C2p” wording as such (the registry splits it over A:EX-A, A:OP, A:DELIV-D, A:IDEAL-W+).

---

## C. Items that are planned or open — the statement text that exists

For each item: the file and line where the item is named, and whether any statement text exists. Quotes are exact. The worktree copy of `QUEUE.md` (HEAD `0f814f19`) has the section “Named open items” at lines 110–112; the copy on `origin/dept/theory` has the same text at lines 115–117 (header line 115). Text is identical; line numbers differ by 5.

| Item | Named at | Statement text that exists | Status |
|---|---|---|---|
| Raw-scale search bridge (READER B6.7, D121) | `Theory_work/Dept/QUEUE.md:111` (origin copy :116): “READER B6.7, raw-scale search bridge: needed for the probability form of ‘Cor 6L supplies Cor 9C’s list-mass premise’. Follow-up paper / open item; not a ticket.” | `Theory_work/Wave3/W3-READER/READER_VERSIONS.md:761`: “The masters take θ* deterministic (Setting R). A raw-scale version (fixed β*) would need a NEW bridge (medium; the population conditions involve θ*). Not proposed for CP1.” and `:1443` (“Relation to Corollary 9C (D121)”). No theorem statement. | Open; no statement. |
| RM2-R aggregated leak | `QUEUE.md:112` (origin :117) | `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:30-31`: “Not targeted in this file (named open items, PLAN §4): … the aggregated Form R leak; T6 (already in PARENT v1.4).” No statement text. | Open; named only. |
| START MIS with a general μ (W3-START2R-O1) | `QUEUE.md:112` | `Theory_work/Wave3/W3-START2-R/STATEMENT.md:253-254`: “MIS for a general deterministic μ ∉ span X_𝒞 without (GR) (named open item W3-START2R-O1)”; `W3-START2-R/REPORT.md:89`. No statement text. | Open; named only. |
| Ex-Equi b < 3/8 (O4′) | `QUEUE.md:112` | `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:30-31`: “the equicorrelated threshold b = 3/8 and its converse (O4′)”. No statement text. | Open; named only. |
| START2-O1 count (17 − s0) | `QUEUE.md:112` | No separate open-item text. The count r(s0) := max(1, 17 − s0) appears in the statement (N2⁺⁺) at `Theory_work/Wave3/W3-START2-R/STATEMENT.md:156`. | Named only; the count itself is in a statement. |
| The trap theorem (mixing lower bound for single-flip MCMC and wTGS on a multimodal design, plus our consistency on the same design) | `Docs/Writing/ASSIGNMENT_6.md:37` (the only wording): “the trap theorem: a mixing lower bound for single-flip MCMC (and wTGS) on a multimodal design, plus our consistency on the same design;” and `Theory_work/Wave3/HQ_DECISIONS.md:849` (“Theory plan for later: (c) the trap theorem first, then 10^7 coverage”). | No statement or plan file found anywhere in the repository. (`Wave2/W2-FAC-K2/numerics/N1_A_trap_indep.jsonl`, `N1_C_trap_corr.jsonl` use “trap” for a different purpose.) The text “no statement text exists” applies. | Planned; no text exists. |
| Coverage at p = 10^7 | `Docs/Writing/ASSIGNMENT_6.md:38` and `Theory_work/Wave3/HQ_DECISIONS.md:840-849` (the 10^7 plan: a single-shot showcase, one fit, one seed, simulated AR-strong n = 200) | No definition of “coverage at 10^7” as a statement; the lines describe an engineering plan (Phase 0 desk study paused). DEC H-35 to H-37 and the PHASE0_NOTES draft concern the engine. No statement text exists. | Planned; no text exists. |
| Lean certification | H2 §B: scaffold only (`origin/lean/BVSCert`, BRIEF.md, a smoke lemma) | No theorem is certified; no statement text to map. | Scaffold only. |
| Further items named in the registry/READER notes (not in QUEUE “Named open items”) | H2 §B; `CLAIMS_CARD.md:93-101` | T9/T11 (START2, not adopted); T12 (SOP:TH110, adopted 11-18, landing pending; the registry row still reads “not adopted”); POST2-R1/O1–O3; SAMP-R1; SCR-R1; the post-freeze DIST sharpness review; MISR riders; pillars 4.2/4.3. Statement texts live in the respective `STATEMENT.md` files; not mapped here. | Open or pending. |

Open items that A6 itself names (for cross-reference): the global-overlap premise of `rem:alt-route` (statement A21: P-OVL∞); the raw-scale bridge (A18, above); the “weaker, group-relative form of NL” for S3, S4, S6, “a candidate; not proved” (`supplement_or.tex`, “Is the no-leakage condition reasonable?”, no statement text); the registry housekeeping “about twenty rows still read ‘conditional on’ a posterior-concentration input” (`appendices_or.tex:330`); the approximate-Gram condition question (`appendices_or.tex:320-322`).

---

## D. Proved theorems and corollaries in the registry that A6 does not map

Registry rows with kind theorem or corollary and a status that starts with “PROVED”, not cited in section A (the A6 map cites 56 registry ids). **103 rows.** “Not mapped” means the id is not one of the master/bridge rows cited in A1–A24; it does not mean the result is unused by A6 (many are inputs to cited masters). Short = the registry `short` field, cut at 110 characters.

| id | kind | v | status | short |
|---|---|---|---|---|
| `W1-PXN:Thm-PXN` | theorem | 1.0.0 | PROVED-CHECKED | On LH-iid with SIZE, 18<=p<=n^A: P(O & S+!=S0)->0 and liminf P(O & S+=S0)=1-limsup P(U) for v3+LS0 under (OP);… |
| `W1-N1:Cor-E` | corollary | 1.0.0 | PROVED under the same premises | E[W_r/H_r(h)-h(S0)//C] <= E[W_r H_r(1{S!=S0})/C] = delta1 <= 2 delta1 for h in [0,1]. |
| `W1-N3:Thm-N3-code(a-d)` | theorem | 1.0.0 | PROVED; XF-checked | start_mode returns max pi0-objective and a smallest-size maximiser; visits DFS-first min(N,cap); N<=cap => res… |
| `W1-N3:Thm-N3-code(e)` | theorem | 1.0.0 | PROVED; XF-checked | In binary64 value, membership and smallest size hold for log_gamma0; lex choice can fail even without truncati… |
| `W1-N3:Thm-N3-code(f)` | theorem | 1.0.0 | PROVED; XF-checked (reference algorithm, not in code) | Reference algorithm TDP returns S* for every instance in exact arithmetic without enumerating ties, O(p*sum_b(… |
| `W1-GEN:Thm-GEN` | theorem | 1.0.0 | PROVED-CHECKED | Reported-HPM consistency on general correlated fixed designs (bounded separated relevance set + block-level ce… |
| `W1-GEN:Thm-GEN(C3-fav)` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | If S*=S0, (H1) not needed: D_n<=P(S~0!=S0)->0 under (H0),(H2) and the premises. |
| `W1-GEN:Thm-GEN(C4)` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | Theorem GEN conclusions hold under the joint law of (X,eps) when (H0)-(H2) hold with fixed constants on X-even… |
| `W1-GEN:L2` | theorem | 1.0.1 | PROVED (by this seat, unchecked) | Start mode equals S* w.p.->1: 1-pi0(S*)=O_P(a_n), unique maximiser of gamma0 on {pi0(S*)>1/2} (T22(iii) re-run… |
| `W1-GEN:L3` | corollary | 1.0.0 | PROVED (by this seat, unchecked) | On Omega_n every maximiser over neighbours of S⊆V, S!=S0 lies in V and improves; S0 has no improving neighbour… |
| `W1-GEN:L5` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | D_n<=P(S~0!=S*)+P(Omega_n^c); with M5(0), T03♯ and [OP] gives D_n->0 and the reported-HPM conclusions. |
| `W1-GEN:Thm-GEN(C5a)` | theorem | 1.0.1 | PROVED (by this seat, unchecked) | On LH exact Gram, (H0)-(H2) hold with S*=S0\M, V=signal units, c_S=0, eta=0. |
| `W1-GEN:Thm-GEN(C5b)` | theorem | 1.0.1 | PROVED (by this seat, unchecked), conditional on W7-PART The… | LH-iid with SIZE, p<=n^A: Theorem GEN via (C4), conditional on W7-PART Theorem B (candidate) and [CONC]. |
| `W1-GEN:Thm-GEN(C5c)` | theorem | 1.0.1 | PROVED (by this seat, unchecked) | W design (groups of 9 at 1/4, two n^-1/4 signals): (H0) verified directly and (C3-fav) with S*=S0. |
| `W1-GEN:Thm-GEN(C5d-S1346)` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | Study scenarios S1,S3,S4,S6 (s0=14 asymptotic sequence) covered by (C3-fav) via (C4); asymptotic, nothing at n… |
| `C-PACK:SL2` | corollary | 1.0.0 | PROVED; XF-checked (R34 ERROR-as-written → 9 fixes; core re-… | Conditional on M4(b),(c), EX-A, positive-capacity store, truth discovery: P(O∩{max_j/PIP^T_j-1{j∈S0}/>2δ_n})→0… |
| `C-GROW:Thm-GROW` | theorem | 1.0.0 | PROVED-CHECKED | Under (H0),(G1)-(G4), v3.1+LS0 with MR1, D_n -> 0, P(O and S+ != S0)->0, liminf P(O and S+=S0)=1-limsup P(U_n)… |
| `C-GROW:C5a` | corollary | 1.0.0 | PROVED-CHECKED | AR(1) exact Gram, fixed rho!=0, separated truths, any p<=n-1: hypotheses of Theorem GROW hold with relevance e… |
| `C-GROW:C5b` | corollary | 1.0.0 | PROVED-CHECKED | S5 population covariance at fixed p=100, diagnostic layout: hypotheses hold for large n; tau0=4/25 (c=1), 1/25… |
| `C-GROW:C5c` | corollary | 1.0.0 | PROVED-CHECKED | Under the joint law of (X,eps): sandwich, NA, TL hold w.p.->1, hence Theorem GROW conclusion; study S2 layouts… |
| `C-GROW:Cor-L6.8` | corollary | 1.0.0 | PROVED-CHECKED | For rho=1/2 the p=500 and p=1000 truth layouts of gen_dev_data.R satisfy the separation condition for every si… |
| `C-DLV:Cor-R` | corollary | 1.0.0 | PROVED-CHECKED (council round 2) | Under MACH and a declared allocation mem_n/time_n (explicit polynomial sufficient shapes), none of B1-B3, E1-E… |
| `C-DLV:Thm-D` | theorem | 1.0.0 | PROVED-CHECKED (relative to the P1/P3 audits) | U_n = SL_n up to a null set; schedule_limit = tier-1 construction fails via (alpha) too many intervals, (beta)… |
| `C-DLV:Cor-Dp` | corollary | 1.0.0 | PROVED-CHECKED (pathwise argument supplied by R04 | P(O and S+=S0) >= 1-o(1)-P(SL_n) on LH, LH-iid, GEN via W1-GEN (C1)+(C2), T03#, W1-PXN (T),(P); pathwise, no C… |
| `C-DLV:Cor-3.2p` | corollary | 1.0.0 | PROVED-CHECKED | For c in (1/2,1) the set {t: q_t(M)>=c} is a (possibly empty) interval. |
| `C-DLV:Cor-5.3` | corollary | 1.0.0 | PROVED-CHECKED | Under 5.2/5.2', k+N<=T_e excludes too_many_intervals; non_progress excluded if D<=s 2^60; post-snap validation… |
| `W2-APP:Thm-LOC` | theorem | 1.0.6 | PROVED-CHECKED, conditional on SOP:TH05.0 | Reported-model consistency for random Gaussian designs with exponentially local correlation (spectrum in [c,C]… |
| `W2-APP:LOC-B` | theorem | 1.0.5 | PROVED-CHECKED, conditional on SOP:TH05.0 | Block-diagonal Sigma, growing blocks g_n (lambda_min>=c, <=1 truth/block, PTV), s0(g_n-1)<=(1-d0)log n incl. p… |
| `W2-APP:VN-routes` | corollary | 1.0.5 | PROVED-CHECKED, conditional on W1-GEN:L5, W1-GEN:L2 | If /N_n/->inf the GEN route fails; if min(K,/N_n/)/log n->inf no O(log n) sandwich/GROW-LOC route exists. |
| `W2-FAC-A:Thm-FAC-L` | theorem | 2.1.0 | PROVED-CHECKED | Reported-model consistency + delivery for one global factor + bounded local blocks (CS, block CS, S5), exact G… |
| `W2-FAC-A:L1` | corollary | 1.0.1 | PROVED (by this seat, unchecked) | Add statistic Z_{T,l} splits exactly along residual factor direction; uniform bound over all T on event of pro… |
| `W2-FAC-A:L4` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | D_n -> 0, P(O ∩ {S+≠S0}) -> 0; LS0 from S̃0 reaches S0 after /S̃0∖S0/ deletions on Sand ∩ NA ∩ TL |
| `W2-FAC-B:Thm-FAC-CS` | theorem | 2.1.0 | PROVED-CHECKED | Exact-Gram CS, any p_n<=floor(n/2): start mode S*, LS0 pure backward elimination to S0, D_n->0, consistency, d… |
| `W2-FAC-B:Thm-FAC-CS(C1-M)` | corollary | 1.1.0 | PROVED (by this seat, unchecked) | (C1)-(C4) also hold with (FS) replaced by (FS'): masked truths ((1-rho)θ_j+ρθ(S0)=0) allowed if their block al… |
| `W2-FAC-B:Cor-M` | corollary | 1.0.1 | PROVED (by this seat, unchecked) | Lemma L2 holds with (FS) replaced by (FS') |
| `W2-FAC-B:L5` | theorem | 1.1.0 | PROVED (by this seat, unchecked) | (H0) automatic, D_n<=P(K_n^c)->0, consistency, and delivery (new Prop F class extension); delivery is under A:… |
| `W2-FAC-PK:Thm-NEG` | theorem | 1.0.0 | PROVED-CHECKED | Under (PK),(PB): first floor(n^β) LS0 moves are swaps (β<1/2), so LS0 with cap <=/S̃0/-s0-2+n^β never scores S… |
| `W2-FAC-PK:Thm-PATH` | theorem | 1.0.0 | PROVED-CHECKED | For p>=K+16s0+1, blocks<=16, every δ>0: uncapped LS0 path ends at S0 (strict local max) in <=(1+δ)/S̃0/ moves … |
| `W2-FAC-PK:Thm-FAC-PK` | theorem | 2.1.0 | PROVED-CHECKED | Cap rules >= max(l_n,ceil((1+δ)/S̃0/)): (H0), D_n->0, consistency (with CAL); delivery P(no output)=0, P(S+=S0… |
| `W2-FAC-S5:Thm-FAC-BCS-R` | theorem | 2.1.0 | PROVED-CHECKED | Block CS (S5), p<=n/2 start mode S*; for log p/log n<alpha<1/2 LS0 path = best-null-deletion to S0 on event CC… |
| `W2-FAC-X:Thm-FAC-CS-iid` | theorem | 2.0.0 | PROVED-CHECKED | iid Gaussian rows, CS covariance rho fixed, limsup log p/log n<1/2, fixed s0: start mode, uniform pure-null-de… |
| `W2-FAC-X:Thm-FAC-GL` | theorem | 2.0.0 | PROVED (by this seat, unchecked) | One factor, arbitrary loadings in [lam_lo,lam_hi]⊂(0,1), exact Gram or iid rows, log p/log n<A_S=1/(2(R^2+2R))… |
| `W2-FAC-X:Cor-FAC-NCS` | corollary | 1.0.0 | PROVED (by this seat, unchecked) | Nearly equal loadings Delta_n H_n<=n^{-1/3}, iid rows, log p/log n<1/2, (FS) at rho=lambda_bar^2: claims (C1)-… |
| `W2-FAC-XA:L8-T` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | Uniformly over deterministic centered standardized designs with R>=gI, p=o(n): all truth deletions and truth-o… |
| `W2-LOC2:PLR` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | Polylog relevance assembly: sandwich on deterministic Q (/Q/<=(log n)^k) gives NA, TL, D_n->0; with LSF also p… |
| `W2-LOC2:LOC-d` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | Reported-model consistency for iid Gaussian rows with correlation/precision decaying exponentially in Euclidea… |
| `W2-LOC2:LOC-BF` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | Block-diagonal designs with bounded or one-factor groups of size <=(log n)^kappa (incl. compound symmetry), <=… |
| `W2-LOC2:Thm-Poly` | theorem | 1.0.1 | PROVED (by this seat, unchecked) | /Sigma_jk/<=K(1+/pi(j)-pi(k)/)^-alpha on a line, spectrum in [c,C], PTV, alpha>17/2: reported-model consistenc… |
| `W2-UNI:UNI-P` | theorem | 1.0.0 | PROVED (by this seat, unchecked) | Posterior rate 1-pi(S0)=O_P(sqrt(log n/n)) for Gaussian rows, any k, any p<=n^A under LSF + fixed sparsity/bet… |
| `W2-UNI:UNI-0` | theorem | 2.1.0 | PROVED-CHECKED, conditional on SOP:TH05.0 | k=0: Sigma metric-local (exp. decay, any polynomial-growth pseudometric), PTV, any p<=n^A: reported HPM = S0 w… |
| `W2-UNI:UNI-1` | theorem | 3.1.0 | PROVED-CHECKED | k=1, Sigma=lambda lambda^T+Psi, Psi metric-local, subset-exposure ratio kappa<=kbar, TV-pop, limsup log p/log … |
| `W2-UNI:U-LOC-Cor` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `C-PACK:SL1.core` | corollary | 1.0.1 | PROVED-CHECKED |  |
| `W3-POST:Cor-1R` | corollary | 1.0.0 | PROVED (by this seat, unchecked) | Iid N(m,Σ_n) rows, ε independent of design, LSF floors, coefficient bounds => events of Thm 1 item 6 exist so … |
| `W3-POST2:A1` | theorem | 1.0.7 | PROVED-CHECKED, conditional on W2-APP:POST | R1, under G, (E), (F_λ), (OS) in place of (F_w): all conclusions 1–6 of W3-POST Theorem 1; 5(a) needs only G, … |
| `W3-POST2:D.D(a)` | corollary | 1.0.7 | PROVED-CHECKED, conditional on W2-APP:POST |  |
| `W3-POST2:D.D(b)` | corollary | 1.2.7 | PROVED-CHECKED, conditional on W2-APP:POST |  |
| `W3-RM:RM-0` | theorem | 1.0.0 | PROVED-CHECKED | Any design, deterministic Q⊇S0, /Q/≤K: on Sand∩NA∩TL LS0 deletes the start mode's extras and ends at S0; pathw… |
| `W3-RM:RM-F` | theorem | 1.1.0 | PROVED-CHECKED | Fixed design: (T1-F), floors (FL), visibility (V), bounded leakage (L) with polylog Q, lattice condition (N) ⇒… |
| `W3-RM:RM-R` | theorem | 1.2.0 | PROVED-CHECKED, conditional on SOP:TH05.0 | Gaussian rows: (T1-R), (FL-R), (V-R)=PTV, localised leakage (L-R), lattice (D-R) ⇒ same reported-model conclus… |
| `W3-RM:B3p` | corollary | 1.0.0 | PROVED (by this seat, unchecked) | If q ≤ C log n (in particular under (N-χ)), BM-∞ implies (BM-Q), and Lemma B3 is GROW L2.1. |
| `W3-SCR:SCR-Ao` | theorem | 1.0.0 | PROVED-CHECKED | Model G, EX-A, MC°(q,x): w.p. ≥ 1−4e^{-x} every LO model of size ≤ q contains S0; each missing truth competes … |
| `W3-SCR:Ao-inf` | theorem | 1.0.0 | PROVED-CHECKED | q_n log p = o(n), ‖μ‖ = o(nσ) and liminf √Ψ_n(q_n)/[√(2 log p+log n)+√(2q_n log p)] > 1 ⇒ the (A∞) probabiliti… |
| `W3-SCR:SCR-M` | theorem | 1.0.0 | PROVED-CHECKED | Deterministic family 𝓗: on an event of prob ≥ 1−4e^{-x}, F(S∪t(S))−F(S) ≥ δ_S for all S ∈ 𝓗⁻; (M1) screening o… |
| `W3-SCR:SCR-G` | corollary | 1.0.0 | PROVED-CHECKED | Under A1's hypotheses and (q_n+1) log p+log n = o(n): w.p.→1, near-best scanned centres (gap ≤ c2 n) of size ≤… |
| `W3-SCR:A1o` | corollary | 1.0.0 | PROVED-CHECKED | Directional floor κ, θ_min ≥ 16σκ⁻¹√(𝐋_n/n), s0𝐋_n ≤ κn/576, ‖θ*‖₂ ≤ ½√(κ(n²−1))θ_min, ‖μ‖ = o(nσ) ⇒ same conc… |
| `W3-SCR:SCR-C` | theorem | 1.0.0 | PROVED-CHECKED | (A∞) or (A°∞), s0 = O(1), ‖θ*‖₂ = O(σ√n), q_n log p = o(n), superset floor φ_n(q_n) ≥ 2 log p/(2 log p+log n)+… |
| `W3-SCR:L5.2` | corollary | 1.0.0 | PROVED-CHECKED | Under MC(q,x_A) (or MC°), if (EC′) is violated for every strict superset of size ≤ q, then on an explicit even… |
| `W3-SCR:SCR-R` | corollary | 1.0.0 | PROVED-CHECKED | Under (A∞) or (A°∞): w.p.→1 every certified C with 1 ≤ /C/ ≤ q_n has ‖P_Cy_c − μ‖² ≤ σ²(√/C/ + √(2/C/ log(ep//… |
| `W3-MISR:MIS(i')` | theorem | 1.0.2 | PROVED-CHECKED, conditional on W2-APP:POST |  |
| `W3-MISR:MIS(ii)` | theorem | 1.0.2 | PROVED-CHECKED, conditional on W2-APP:POST |  |
| `W3-MISR:Cor-G(a)` | corollary | 1.1.2 | PROVED-CHECKED, conditional on C-MIS:Prop-P; input versions … |  |
| `W3-MISR:Cor-G(b)` | corollary | 1.0.2 | PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:Prop-P, C-… |  |
| `W3-MISR:Cor-H` | corollary | 2.1.2 | PROVED-CHECKED, conditional on W2-APP:POST |  |
| `W3-START:START-F` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-START:F1` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `W3-START:F2` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `W3-START:F3` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `W3-START:F4` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `W3-START:TRANSFER` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-START:START-R` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-START:IF-START` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `W3-START:MIS` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `W3-START2:START-F` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-START2:F2` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `W3-START2:TRANSFER` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-START2:IF-START` | corollary | 1.1.0 | PROVED-CHECKED |  |
| `W3-START2:START-R` | theorem | 1.1.0 | PROVED-CHECKED |  |
| `W3-MISR-R:CorG-min` | corollary | 1.0.3 | PROVED-CHECKED |  |
| `W3-MISR-R:CorH-plus` | corollary | 1.0.3 | PROVED-CHECKED, conditional on W2-APP:POST |  |
| `W3-MISR-R:CorH-U` | corollary | 1.0.3 | PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:Prop-P; cl… |  |
| `W3-T03ACC:T03S.1` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-T03ACC:T03S.2` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-T03ACC:T03S.3` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-T03ACC:T03S.4` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-DIST:DIST-1` | theorem | 1.0.3 | PROVED-CHECKED |  |
| `W3-DIST:DIST-2` | theorem | 1.0.3 | PROVED-CHECKED |  |
| `W3-DIST:DIST-3` | theorem | 1.0.2 | PROVED-CHECKED |  |
| `W3-START2-R:START-F` | theorem | 1.0.0 | PROVED-CHECKED |  |
| `W3-START2-R:F1` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `W3-START2-R:F4` | corollary | 1.0.0 | PROVED-CHECKED |  |
| `W3-START2-R:TRANSFER` | theorem | 1.0.1 | PROVED-CHECKED |  |
| `W3-START2-R:MIS` | corollary | 1.0.1 | PROVED-CHECKED |  |


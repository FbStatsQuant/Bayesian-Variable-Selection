# W3-T03ACC — council round R1, seat `opus` (Claude Opus 5.5, Claude Third, effort high) — blind first read

Reviewed content: `reviews/MANIFEST_R1.txt`, first line `MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6`;
`python3 -B Theory_work/Wave3/tools/manifest.py verify …` returned `verify: OK` before I read anything. Files read: those the
brief permits (STATEMENT, REPORT, DEPS, ERRATA, PLAN, TARGET, READER_DELTA, BRIEF, RIDER_RULES, citecheck.py, deps_hash.py,
`sources/` except the two FINAL_REPORT files, `reviews/INPUTS.txt` and its two code files, and rows TH121–TH128 of the
NBH ID_REGISTRY). I did not open any other `reviews/` file, LOG, CHECKPOINT, FINAL_REPORT, earlier verification, git history or
the web.

## Verdict summary
I re-derived every changed step of the proof under review (`sources/W1-T03R/PROOF.md` §§1, 2, 4, 6) and every [P1]/[P3]
step it consumes, line by line against the pinned copies. I tried hardest to break the five points the brief names:
(1) den′ as extracted from the body of [P1] `lem:den`;
(2) the `sup_m P₀` quantifier in T02(i♯);
(3) the restriction of every normalised-eigenvalue use to |J′(S)| ≤ j₀, with the crude bound (C6)(a) on the large-J′ branch;
(4) the exponent count in (C8);
(5) the beta-min constant in (C10) and the three-way split.
None of them breaks. Every eigenvalue or rank fact is supplied by R, SE_λ(j₀) (through (B2)), SE_w(m♯_n; g₀) (through
(B1)) or interlacing, on exactly the sets where it is used. No use of the locked full SE or of H-T02 survives. Nothing
needs A ≥ 1: A ≥ 0 is forced by 1 ≤ p ≤ n^A, and every A-dependent inequality holds for any A ≥ 0. The only randomness
in any cutoff, set or threshold is the bounded quantity κ_n(𝒰). The p = 1 case goes through as STATEMENT §4 item 4 says.
STATEMENT v1.1 is faithful to the record and the card, its §1 matches the coded score, prior and standardisation, and
the quoted statuses are verbatim. I hold no C, S or F finding. My findings are editorial only (E1–E6). T03♯ as stated
in STATEMENT v1.1 is proved by the proof as written and can be accepted as checked mathematics.

## Per-claim table
| id | decision |
|---|---|
| W3-T03ACC:T03S.1 | ACCEPT |
| W3-T03ACC:T03S.2 | ACCEPT |
| W3-T03ACC:T03S.3 | ACCEPT |
| W3-T03ACC:T03S.4 | ACCEPT |
| W3-T03ACC:T03S.5 | ACCEPT |

## Gate table
| gate | result | what I re-derived |
|---|---|---|
| G1 correctness | PASS | See the step-by-step record below. Each step was re-derived independently, not sampled. |
| G2 hypotheses used = stated | PASS | The full inventory is in the paragraph after this table. |
| G3 no hidden assumptions | PASS | Every eigenvalue, rank or full-column-rank use, and its source, is listed below; nothing else is used. |
| G4 imports and statuses | PASS | Each [P1]/[P3] result is used as stated. den′ is exactly what the body of `lem:den` proves (`PROOF_v3.tex:337-359`). The statuses in STATEMENT §5 are verbatim: TH121, TH122, TH123 and TH125 against the permitted NBH rows, and the SOP:TH09 fragment against `registry_theory_main_L68.tsv`. The label list misses a few [P3] labels that are consumed (E2); this is record form, not mathematics. |
| G5 constants, rates, uniformity | PASS | See the constants and uniformity record below. |
| G6 fidelity | PASS | See the fidelity record below. |

**G1 — step-by-step record.**
- **E1(a).** q_{i+1}/q_i = ρ_i.
- **E1(b).** I checked ρ_i ≤ ½e^{−(i−1)/(2p−2)} for i ≥ 1 and for i = 0. I checked Σ(i−1) = ½[(k−1)(k−2) − (s₀−1)(s₀−2)], and that t(t−1) is monotone for k − 1 ≥ m ≥ 0.
- **E1(d).** γ_m ≥ 0 for m ≥ s₀ ≥ 1.
- **E2(i).** C(p,s₀)2^{s₀} ≤ (2p)^{s₀}, so R_{m_n(ω)} ≤ n^{−(s₀+1)/2}e^{−ω}.
- **den′.** The bound Q^c_{S₀} ≤ σ*²E′ + R_n, via `lem:spec`(c) with g = (n−1)φ₀². The exponent chain: log u ≤ u − 1, 1/u ≥ 2 − u, 0 ≤ u − 1 ≤ n^{−1/2}. The window [σ*², σ*²(1+n^{−1/2})] ⊆ [σ*², 2σ*²], and D_{S₀} ≤ (n+1)^{s₀}. Also E₀Λ_n ≤ C_Λ.
- **T02(i♯).** v_m = R_mϖ(S₀). E₀Θ^{(1)} = 1 via `lem:num` at the data-free rate b₋. The display on 𝓑_n via `thm:Ta`. The three-event union for L > c♯². The bound P₀(𝓑ₙᶜ) ≤ (8 + 24M/σ*²)/(n−1) from `thm:T01iii`. No term depends on m.
- **Lemma I and Lemma B (B1)–(B3).** Lemma I is the padding argument. For (B3): M_T ⪯ (n/(n+1))P_T, M_S ⪰ (1−η_n)(n/(n+1))P_S, and P_T − P_S is a projection whenever col(S) ⊆ col(T), with no rank needed.
- **(C1)–(C10) against [P3].** Every place [P3] invokes SE is replaced: `sec:good`, `lem:Gprob`, `lem:ongood`(c), `lem:onesup` (det and `cor:diff`), `prop:sup` (exact χ²), `lem:SvsSp`, `lem:signal`, `lem:assemble` (large-J′ branch), Step 1 and (iv).
- **(C6)(a).** Deterministic: the prior factor by `lem:prior`(a), the determinant by `lem:det` (first part, unconditional), and Q^c_{S′} ≤ Q^c_S.
- **(C8) exponent.** j₀ + 1 ≥ (2A+1)s₀ + 2, so n^{As₀}(n+1)^{s₀/2}n^{−(j₀+1)/2} ≤ 2^{s₀/2}/n.
- **(C10).** (1 − 1/n)c ≥ L* for n ≥ c/(c − L*). Also L*/32 ≥ s₀(A+1) + 2, which gives κ_n ≤ e^{ρ_n}n^{−2}.
- **Assembly.** The three-way split covers Ω∖{S₀}: |S| > m♯, or a superset with |S| ≤ m♯, or in 𝒰. Each part is O_P(r_n) with P₀(𝒢ₙᶜ) ≤ 5/n. Paragraphs (ii), (iii) and (v) hold deterministically.
- **Consumed [P1] steps.** `lem:slab`, `lem:IGint`, `prop:closed`, `thm:T01i` (change of variables and the constant c_n(s)), `thm:T01ii`, `thm:T01iii` (Chebyshev and the inclusion 𝓑ₙᶜ ⊆ {|Δ_n| > σ*²/2}), `thm:Ta`, `lem:num`, `lem:spec`(a)–(e), `lem:prior`(a)–(d) and `lem:chi`(b).
- **Consumed [P3] steps.** `lem:red`, `lem:smoother`, `cor:diff`, `lem:det`, `lem:prior`(a),(b), `lem:signal`, `lem:chi`, the counts in `lem:Gprob` (G1)–(G4), `lem:ongood`(a)–(d), `lem:onesup`, `prop:sup`, `lem:SvsSp` (both inequalities, including n ≥ 4 and δ″ ≤ 1), `lem:signalgain` (log 2 + ½log(n+1) ≤ log n for n ≥ 5), `lem:assemble` and §`sec:main`.

**G2 — inventory of hypotheses used.**
- **R1.** s₀ fixed (C_m, K_{s₀,j}, 2^{s₀}); p ≤ n^A (union bounds, j₀, eq:mn, (C8)); s₀ ≤ K eventually (S₀ ∈ Ω, T02(i♯)); fixed X.
- **G.** Exact Gaussian laws.
- **R.** ‖μ‖² ≤ Mn (𝓑_n, C_Λ, `lem:ongood`(a)) and λ_min(R_{S₀}) ≥ φ₀² (den′, (B3) on S₀, η_n).
- **SE_λ(j₀).** Used through (B2).
- **SE_w(m♯_n; g₀).** Used through (B1).
- **BM.** Used through (C10).
- **s₀ ≥ 1.** Used in E2(i) and makes S₀ ∪ J ≠ ∅ automatic.
- **Fixed constants and deterministic sequences.** Fixed g₀, φ₀, M and σ*² enter n₀ and the constants. M_n and c are deterministic, so BM-∞ gives BM(L*+1) eventually, and J_n(c), J_n^∞ are deterministic sets.

Nothing in STATEMENT §2 goes unused. SE_λ at J = ∅ duplicates R's eigenvalue part, which STATEMENT §4 item 2 says.

**G3 — sources of every eigenvalue, rank or full-rank fact.**
- **R.** λ_min(G_{S₀}) ≥ Nφ₀², used in den′ and (B3) with S = S₀.
- **(B1) from SE_w.** Full rank of S₀ ∪ J for 1 ≤ |J| ≤ m♯_n; exact χ²_{|J|}; the determinant ratio. Used in (C2), (C4) and (C5).
- **(B2) from SE_λ(j₀) plus interlacing.** λ_min(G_{S′}) and λ_min(G_S) ≥ Nφ₀², and N_S/σ*² ∼ χ²_{|J(S)|}, only when |J′(S)| ≤ j₀. Used in (C3), (C6)(b), (C7) and (C10).
- **Rank only.** (G2) and the probability part of (G4) use only rank ≤ |T| (resp. ≤ |J(S)|, since adding |J| columns raises the dimension by at most |J|).
- **Independence.** Used only in `lem:chi`(a), last claim (χ²_{d′} = χ²_d plus an independent χ²), which holds.

**G5 — constants and uniformity record.**
- **T02(i♯) constants.** c♯ = κ²/(c_IG σ*²) depends on (σ*², M); C_Λ on (φ₀, σ*², M).
- **(C5).** c_q = √(eC_A(1 + 1/g₀)), with C_A = 8 + 3A from [P3]. [P1]'s C_A = 10 + 4A is not mixed in.
- **(C8).** K_{s₀,j₀} depends on (s₀, A).
- **Thresholds.** n₀ depends on (s₀, A, φ₀, σ*², M, g₀), on c under BM(c), and on (M_n) under BM-∞. This matches PROOF.md:170 and STATEMENT §4 item 7.
- **Uniformity in m.** sup_m in T02(i♯), used only at the single deterministic m = m♯_n.
- **Uniformity over J.** Through expectations of sums with deterministic weights and exact χ²_j.
- **Uniformity over S.** Deterministic bounds on 𝒢_n (κ_n is a maximum bounded pointwise on 𝒢_n).
- **Uniformity over j ∈ J_n(c).** The bound on Π(𝒰_j | y) on 𝒢_n does not depend on j, and |J_n| ≤ s₀.

**G6 — fidelity record.**
- **Record and card.** STATEMENT §2–§3 against W6-FIXREV2:19-35, 51-61 and the card (TLF:15-18, 29): clause by clause equal, with the readings in §4. The m♯_n "≤ K" qualifier and A without "≥ 1" are correct.
- **§1 against the code.** `v3_score.h`: log C_n, H = (n+1)G + I, A = G + I, Q = y′y − n z′H⁻¹z, log w(k) = −log 2 − log C(2p−1, k), K = min(p, ⌊n/2⌋), ν = a₀ + n/2, a₀ = b₀ = 0.01. `v3_preprocess.R`: centring and SD with denominator n − 1 for X and y, constant columns dropped (consistent with "no constant column").
- **Citations.** `citecheck.py` reports 69 citations and 0 MISSING/OUT-OF-RANGE (output in my scratch folder).

## Findings
All findings are tagged **E**. None blocks.

1. **E — den′ citation scope.** At `sources/W1-T03R/PROOF.md:91`, den′ says it is what "the first two sentences of 'Assembling'" in the proof of [P1] `lem:den` establish. The second sentence of that paragraph (`sources/P1/PROOF_v3.tex:357`) uses both D_{S₀} ≤ (n+1)^{s₀} and ϖ(S₀) ≥ ½(2p)^{−s₀}, and den′ uses only the first half. The proof does say afterwards that the ϖ factor is not used, so the mathematics is correct. Repair: "…the first sentence of 'Assembling' and its use of `lem:spec`(e) (not of `lem:prior`(d))".
2. **E — consumed-label list incomplete.** The [P3] row of `STATEMENT.md:126` omits some labels that the Assembly consumes "verbatim": `eq:ratio` (`PROOF_v2.tex:40-42`), `eq:supsum` (`:228-230`), `eq:assemble` (`:320-322`), the Step 1 paragraph (`:342-350`; (C10) says "From here Step 1 is verbatim"), and the three elementary facts at the head of §`sec:main` (`:334`). All of these lie inside DEPS rows P3.set, P3.sup, P3.under and P3.main, which are OK. Repair: add them to the label list.
3. **E — unlisted reading.** At `STATEMENT.md:58, 73`, STATEMENT writes "deterministic M_n" in BM-∞ and in J_n^∞. The record (`W6-FIXREV2_STATEMENTS.md:34, 60`) says only "M_n → ∞". This is the intended reading: M_n is a function of the deterministic θ* in the card form, see §4 item 5. It is not listed among the §4 readings. Repair: add a §4 item "M_n is a deterministic sequence (as in the card form)".
4. **E — DEPS bookkeeping.**
   - No DEPS row hashes `PROOF.md:9` (conventions, p ≥ 2, m_n(ω)) or `PROOF.md:15-17` (definition of q_k, R_m). R_m is restated in STATEMENT §2, which the STMT row covers.
   - The STMT row hashes `STATEMENT.md:1-132` of a 141-line file; the changelog is not hashed.
   - The `checked_by` cell of P3.det contains a `#…` annotation naming a second file. `deps_hash.py` checks only the part before `#`.

   Repair: add a row for `PROOF.md:9-17` and normalise the P3.det cell.
5. **E — p = 1.** At `PROOF.md:9`, "for p = 1 every statement below is trivial or void" is loose. I agree with ERRATA E2 and with STATEMENT §4 item 4: for p = 1, m♯_n = K = 1 ≤ C_m log n directly, R_1 = 0, and the only competitor ∅ is handled by (B2) with S′ = S₀ and the signal argument. I also concur with ERRATA E1 and E3 (J_n^∞ without "j ∈ S₀"; the lower limit of R_m).
6. **E — status wording.** REPORT's registry block (`REPORT.md:44` and the like) writes "PROVED (W1-T03R, proof as written)", while NBH TH128 reads "PROVED (candidate) (W1-T03R)". It matches the SOP:TH09 registry wording and states "council R1 PENDING", so it is not overstated. If the CP3 text quotes TH128, keep "(candidate)".

Proposal, not a finding: (C6)(a) shows that the e^{ρ_n} factor in the large-J′ term of `eq:assemble` is unnecessary. The locked [P3] carries e^{2ρ_n} there; (C8) correctly writes e^{ρ_n}.

## Sweep duties
1. **Statement copies vs proof statements.**
   - **Hypotheses.** STATEMENT §2 against PROOF.md:162-164 (R1, G, R, SE_λ(j₀), SE_w(m♯_n; g₀) with fixed g₀, BM-∞/BM(c) with c₀ = L*), against :127-132 (SE_λ, SE_w; the side condition S₀ ∪ J ≠ ∅ is automatic for s₀ ≥ 1, §4 item 1), and against :44-47 (m♯_n(ω) and m♯_n). STATEMENT's R_m has lower limit max(m+1, 0), which is the record's form and better than the proof's (ERRATA E3).
   - **Conclusions.** STATEMENT §3 clauses 1–5 against PROOF.md:168 (i)–(v) and the record :53-61. They are equal; clause 5 is expanded from [P3] (v) with the letter d.
   - **Card.** "exact HPM and MPM are consistent" is clauses 2–3, and the inclusion sentence is clause 4.
   - No discrepancy beyond E3 (deterministic M_n).
2. **Quantifiers and uniformity.**
   - **Fixed.** s₀, A, M, φ₀, σ*², g₀, c.
   - **Deterministic.** m♯_n, j₀, J_n(c), J_n^∞, 𝒰, 𝒰_j and the sequence M_n.
   - **Random but bounded on 𝒢_n.** κ_n(𝒰).
   - **T02(i♯).** Holds at every n with s₀ ≤ K, as sup_m P₀(·), not P₀(sup_m ·), and is applied at one deterministic m per n.
   - **"For n ≥ n₀".** Converted to O_P over all n by [P3]'s second elementary fact (posterior masses lie in [0,1]).
   - The O_P claims in clauses 1 and 4 are uniform in exactly the sense used.
   - Clause 3's expectation statement claims only → 0, which is what the bounded-convergence argument gives.
3. **Lemma scope vs downstream use.**
   - (C3) is used only by (C6)(b), which is only for |J′(S)| ≤ j₀.
   - (C6)(b), `lem:signal` and `lem:signalgain` enter only through κ_n(𝒰), which is a maximum over |J′(S)| ≤ j₀.
   - The large-J′ branch uses only the unconditional (C6)(a).
   - (C4)/(C5) are applied to J with |J| ≤ m♯_n, including comparison models S₀ ∪ J outside Ω, which enter only as nonnegative upper-bound devices; (B1) and (G2) are not restricted to Ω.
   - (G4) is imposed only for |J′| ≤ j₀.
   - E1(b),(d) and E2(i) are used only for p ≥ 2, and only in (C1); for p = 1, (C1) holds directly.
   - T02(i♯) needs only G, R and s₀ ≤ K; its Remark (PROOF.md:99) is accurate.
4. **REPORT and REGISTRY block vs STATEMENT.**
   - REPORT.md's claim pointers resolve to the right clauses: :64 is clause 1, :65 clause 2, :66-69 clause 3, :70-73 clause 4, :74-77 clause 5 (line 77 is blank).
   - Premise ranges: :43-60 is R1 to BM, and :43-56 for T03S.4 correctly omits BM.
   - Other pointers: definitions :22-41, readings :92-117, consumes :118-131.
   - REPORT restates nothing beyond STATEMENT. The scope fields ("s₀ ≥ 1 fixed, p ≤ n^A (A fixed)"; T03S.3 "no expectation rate"; T03S.5 "any n") match.
   - Statuses carry "council R1 PENDING" and are not overstated (E6).
5. **DEPS.tsv spot check.**
   - `python3 -B deps_hash.py` (stdout only): all 36 rows have sha = checked_sha and state OK.
   - Every `checked_by` file exists: `reviews/SL1_disposition.md`, `reviews/LC_A_line_check_sol.md`, `reviews/LC_B_line_check_sol.md`, `reviews/LC_C_line_check_sol.md`. I checked existence only and did not open them.
   - The rows cover every changed step: E1, MSHARP, E2i, DENp, T02is, SE, LemI, LemB, C1–C10, ASM and ASM2.
   - They cover every consumed block: P1.set, P1.prelim, P1.T01i, P1.T01ii, P1.T01iii, P1.Ta and P1.T02i (which contains `lem:num` and `lem:den`); P3.set through P3.main.
   - The uncovered lines are irrelevant to T03♯: [P1] `thm:T01iv`, (b1), (b2) and §T02(ii).
   - Small omissions are in E4.

## Score
**9.4 / 10.** No C, S or F finding. The deduction is for the record-form items E2–E4 only.

## Checks performed
- **Manifest.** `manifest.py verify` returned OK. The CRLF copies are hashed LF-normalised, which explains why `sources/P1/PROOF_v3.tex` and `sources/P1/STATEMENT.md` show manifest hashes that differ from their raw sha256 (626137f4…, 3aa33d44…, as pinned in PINS.md).
- **DEPS.** `deps_hash.py` (stdout only): all rows OK.
- **Citations.** `citecheck.py` with output at `/home/fb31/SMC_Theory_Department/tmp/20261116-W3-T03ACC-R1-opus/CITECHECK.txt`: 0 MISSING/OUT-OF-RANGE.
- **Statuses.** Verbatim comparison of the STATEMENT §5 status quotes against NBH ID_REGISTRY rows TH121, TH122, TH123 and TH125 (I read only TH121–TH128) and against `registry_theory_main_L68.tsv`.
- **Code.** Read `v3_score.h` (Data construction, score formula, prior) and `v3_preprocess.R` (standardisation) for G6.
- **Mathematics.** Full re-derivation of every step listed under G1, including the consumed [P1]/[P3] steps.
- **Numerics.** A small sanity script (`nice`, 1 core, `/home/fb31/SMC_Theory_Department/tmp/20261116-W3-T03ACC-R1-opus/e1e2.py`) checked E1(b) (R_m ≤ C(p,s₀)2^{−(m−s₀)}e^{−γ_m}) and E2(i) (m♯_n(ω) ≤ min{K, m_n(ω)}) exactly on n ∈ {5, 7, 12, 30, 61, 200}, p ∈ {2, …, 500}, s₀ ≤ 6, ω ∈ {0, ½log n, 3}: 3,486 checks, 0 failures. This is a sanity check only; the verdict rests on the derivations.

## Not checked
- The content of the SL1, LC-A, LC-B and LC-C review files and dispositions (forbidden to open), including whether the verdicts quoted in REPORT §2 are verbatim.
- Out-of-scope parts of the proof: Prop. D, Prop. E3, E1(c), E2(ii),(iii) and §5 T02(ii♯).
- Parts of [P1] not consumed: `thm:T01iv`, `thm:Tb1`, `thm:Tb` and §T02(ii).
- The W1-T03R scripts and outputs (not re-run).
- The record's Scope paragraph (W6-FIXREV2:63-81; not under review).
- The finite-n thresholds (not scored, by convention).
- Whether the code's numerical routes (QR fallback, Q recomputation) compute the formula exactly. I checked only that the coded formula equals the STATEMENT §1 target.

`COUNCIL-VERDICT round=R1 manifest=9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6 seat=opus score=9.4 gates=PASS`

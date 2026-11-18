# W3-D2 — Council R1, seat `opus` (blind first read)

Seat: Opus 5.5 (claude-opus-5-5), fresh agent. Brief: `reviews/BRIEF_R1_opus.md`. Manifest under review:
`MANIFEST 6f8c05aa83e3063f9b48d8cf42c52c3f49261e0db36b6268419159bc95f06243`.

**Manifest binding.** I recomputed the sha256 of all 10 ticket files and all 10 `EXT:` inputs listed in
`reviews/MANIFEST_R1.txt`. All 20 match, so this review is of exactly the manifest's content.

**Concurrent working-tree drift (not mine).** At about 13:06, while I was finishing this review, another session
modified REPORT.md, TARGET.md, numerics/N1_floor_and_e2e.py and numerics/N1_out.txt in this worktree (uncommitted).
- I read all four files, and re-ran N1, before those edits.
- The HEAD (934a2b43) blobs of all four still hash to the manifest values.
- This review therefore applies to the manifest content, not to the edited working tree.
- After my findings were written I glanced at `git diff` to identify the drift. I saw that it carries "[R1-sol-…]"
  tags and changes the N1 grid maximum from 0.3942 to 0.3928. I have not used it in any finding, decision or score
  above or below.

**What I read.** STATEMENT (v1.3), PROOF (v1.2), REPORT, TARGET, READER_DELTA, DEPS.tsv, PLAN, API_CARD,
api_request_build.py, citecheck.py, deps_hand.py, numerics/ (script and output). Inputs: W3-MISR-R STATEMENT
:1-120 (§§0–3) and `lemmas/G2_corr.md` (whole); W3-MISR STATEMENT :14-200 (§0, Lemma R′, MIS-R (i), (i′), (ii), Cor-G,
Cor-H); W3-POST STATEMENT :1-45; R1_set_sizes.md (whole); READER_VERSIONS :20-32, :255-284, :445-468; NOTATION :1-40;
CLAIMS_CARD :50-58; L1_POST.md :1-40. From `reviews/` I read only the brief, MANIFEST_R1, INPUTS_R1 and CITECHECK. I did
not open LOG, CHECKPOINT or any other review file.

**What I re-ran (scratch in `.rc_tmp/`, deleted at the end).**
- `numerics/N1_floor_and_e2e.py 300`: its output is byte-identical to `numerics/N1_out.txt`.
- `api_request_build.py .rc_tmp/api`: 0 lines dropped except PROOF.md:3. The request text contains none of PROVED,
  CHECKED, council, PASS, unchecked or VERIFIED. This matches the claim at API_CARD:12-13.
- DEPS span hashes, recomputed with my own code (I did not run `deps_hand.py`, because it rewrites DEPS.tsv): all ten
  `sha` values equal the `checked_sha` values in DEPS.tsv, so every row is OK.
- `citecheck.py`: 70 checks, 0 failures.
  **Disclosure:** this script rewrites `reviews/CITECHECK.txt` in place and reads the registry TSV. The rewrite was
  byte-identical: `git status` and `git diff` show no change to that file. The registry was read by the script only,
  and I saw only its OK lines. I made no other writes outside `.rc_tmp/` and this reply file.
- An independent arithmetic grid for the STATEMENT §7 / REPORT §2(b) claim "k̄_n ≤ 3(A+1)(s₀+1) log n for every n ≥ 3".
  Grid: A ∈ [1,10] in steps of 0.05; s₀ ≤ 199; n ∈ 3..199 and 10³..10¹⁵; p = ⌊n^A⌋. Result: 7,426,052 cases,
  0 violations.

---

## (a) Per-claim decisions

| id | decision |
|---|---|
| W3-D2:Thm2X | ACCEPT |
| W3-D2:Cor2X | ACCEPT |

## (b) Findings

I hold **no C, S or F finding**. Editorial findings follow; none of them blocks.

**E1 — STATEMENT.md:108 (§7 caveat (b)) and REPORT.md:20.** The inequality "k̄_n ≤ 3(A+1)(s₀+1) log n for every n ≥ 3"
is stated with no proof or pointer anywhere in the package. B2.1 of [R1] gives only the 5(…) bound.
- **It is true.** My grid above found 0 violations, and a short analytic proof exists:
  - With d = 1/log(3/2), the ceiling gives s + m̄_n ≤ d(As + s/2 + 1)t + (1 + d log 2)(s+1), where t = log n.
  - So s + m̄_n ≤ 3(A+1)(s+1)t as soon as t ≥ 2.7095(s+1)/(0.5337As + 3A + 1.7668s + 0.5337).
  - At A = 1 the right-hand side is < 1.178 for every s, so the bound holds for every n ≥ 4.
  - At n = 3 the cap k̄_n ≤ p ≤ 3^A settles the remaining small-A cases.
  - The j₀ branch is B4.1's.
- **Why it does not block:** the sentence sits outside the registered spans and only weakens the tag.
- **Suggested fix:** add a two-line proof or a pointer.

**E2 — STATEMENT.md:98 (§7 STRONGER list), READER_DELTA.md:32, TARGET.md:25.** "Σ need not be a correlation matrix"
is listed as a gain, and N1 (ii) is described as "outside the recorded Theorem 2". Literally, the reader statement does
say "Σ_n a correlation matrix" (READER_VERSIONS :265), so the tag is not false. But NOTATION.md §1 (the recorded model)
says "we may and do take Σ_n to be a correlation matrix" (WLOG, because the method standardises). Against that
convention the item is cosmetic, and N1 (ii)'s genuine departure from Theorem 2 is σ_n² → ∞, not Σ_jj ≠ 1.
**Suggested fix:** soften to "Σ is not normalised (the floor and the signal are stated on the correlation scale)".

**E3 — STATEMENT.md:63.** The parenthetical "(As [MISR] MIS-R (i) consequence 1, :118-119 …)" follows all three
deterministic facts. Consequence 1 covers the PIP inequality (and sup_{T≠S₀} π(T) ≤ δ), but not the HPM/MPM inclusions
literally; MPM needs the P0.3 argument. PROOF.md:15 attributes correctly ("Item 1 is …"). **Suggested fix:** align
STATEMENT:63 with PROOF:15. All three facts are proved in P0, so nothing is unproved.

**E4 — PROOF.md:64 and PROOF.md:79.** "α* may even be random" and "even that is not used" are true of the master:
CorGb-plus's setting allows any real random α ([MISR-R] :52-53), and U kills α1 in GR^c. They are not true of
Theorem 2X as stated, whose §0 (:19) requires α deterministic. Read inside the proof of Cor2X, "α* may even be random"
invites the question of whether §0 is then met. **Suggested fix:** mark both as remarks about the master, not about
Thm2X, or drop them. This is a better-theorem item (see below), not a gap.

**E5 — REPORT.md:29-31 (card sentence).** "Conditional on the inputs of Theorem 4's master, one of which … has not yet
had an independent check" is accurate under the card's convention: row 1.4 marks CorGb-plus clean modulo POST2. But
REPORT §3a itself says C-MIS:GDb and C-MIS:Prop-P are "wave-1 labels, not PROVED-CHECKED". A reader of the card sentence
could infer that every other input is PROVED-CHECKED. **Suggested fix (HQ's wording call):** "one of which … has not yet
had an independent check; two others are wave-1 results".

**E6 — REPORT.md:26-29, READER_DELTA.md:38.** Two wording points:
- "Under the same model … (Σ, β, σ² may vary with n)" combined with (S1)'s *fixed* σ*² reads as a contradiction.
  READER_DELTA's "(S1) with any σ² > 0" has the same problem. **Suggested fix:** "(S1) with σ² > 0 allowed to depend
  on n".
- READER_DELTA:40's floor "for every T with |T| ≤ …" drops the "1 ≤ |T|" of STATEMENT:36. This is harmless: the empty
  set is never used (PROOF:39-40).

**E7 — READER_DELTA.md:46, REPORT.md:29, STATEMENT.md:67.** "This is Theorem 4 with no omitted predictors." The
hypotheses do coincide with Theorem 4's (A0)–(A3) at 𝒞 = [p], which I checked against READER_VERSIONS :449-466. But
Thm2X's conclusions add the MPM and PIP displays (via §3), which Theorem 4's reader display lacks. **Suggested fix:**
"… plus the deterministic PIP/MPM consequences". The remark sits outside the spans.

**E8 — numerics/N1_floor_and_e2e.py:2.** The docstring refers to "Lemma D2-B1", which does not exist in the package.
The arithmetic it checks is [R1] B4.1. Cosmetic.

## (c) Interpretive sentences inside the registered spans

| location | sentence | verdict |
|---|---|---|
| STATEMENT:31 | "the reader statement below together with the technical clause (E)" | checked: a scope label; REPORT:65 registers 29-48, which includes (E) |
| STATEMENT:44 | "(technical clause; not part of the reader statement)" | checked: a label, consistent with :31 |
| STATEMENT:48 | "and k_n = O(log n), so b_n = O(r_n)" | checked: P2 (PROOF:57-58), via B4.1 for n ≥ max(3, 2s₀) |
| STATEMENT:56-57 | "Hence the four bounds of Theorem 2X's display hold, and with them the three conclusions of the recorded Theorem 2" | checked: P3 (PROOF:73-75); Markov for O_P; P(HPM ≠ S₀) + P(MPM ≠ S₀) → 0 |
| STATEMENT:58 | "The same holds with the floor asked only on \|S\| ≤ 3(A+1)(s₀+1) log n" | checked: PROOF:67-68 |
| STATEMENT:63 | "(As [MISR] MIS-R (i) consequence 1, `:118-119`, "for every data set".)" | checked as an attribution for the PIP fact; over-broad placement (E3), no move needed |

There are no "this means", "reading" or "interpretation" sentences in the spans. STATEMENT:16-17 ("so every column is
non-constant almost surely …") is in the premise span, not a claim span; I checked it (Σ_jj > 0, n ≥ 3).

## Step-by-step check (summary of what I verified)

- **q = 0 instance (P1).** CorGb-plus's setting allows q = q_n ≥ 0 ([MISR-R] :52).
  - The n × 0 matrix times β_𝓜 ∈ ℝ⁰ is 0 ∈ ℝⁿ.
  - (OV) with constant a = 0, γ = 0, τ² = 0 holds via N_k(m, 0) := δ_m (:31). These are deterministic Borel maps, as
    :97-98 requires, and τ² = 0 is allowed by (OV^c)'s range [0, ∞).
  - (N) holds: deterministic σ² > 0, ε independent of (X^r, empty).
  - α deterministic is a special case of the master's "real random variable".
  - Hence β^𝒞 = β, σ²_𝒞 = σ² > 0, supp β^𝒞 = S₀.
- **Identity of posteriors.**
  - [MISR] :19-25 defines π_𝒞(· | x, y^r) as the coded target of [W3P] §0 computed from (x, y^r). With x = X^r this is
    STATEMENT §0's π.
  - The conventions agree: π(T) := 0 off Ω ([MISR] :28 and STATEMENT:26), HPM is a measurable selection of a mode, and
    S₀ = supp β = supp D_xβ.
  - STATEMENT §0's gloss of the prior (N(0, nv(G_S + I)⁻¹), IG(0.01, 0.01), capped BB) matches [W3P] :21-28. The
    posterior precision ((n+1)G + I)/(nv) agrees with H_S.
- **Floor step.**
  - B4.1 ([R1] :43-45) needs s ≤ K, s ≥ 1, A ≥ 1, n ≥ 3, and p ≤ n^A through B1.3's log C(p,s) ≤ Ast.
  - s₀ ≤ K holds for n ≥ 2s₀ because s₀ ≤ p.
  - So k_n ≤ 3(A+1)(s₀+1) log n, and (A2) covers every non-empty T with |T| ≤ k_n. T ⊆ [p] caps T at p if k_n > p.
  - The master's proof uses only non-empty T (G2_corr step 2) and the support S₀ (step 3), whose size is s₀ ≤ k_n.
  - The "n-by-n" legitimacy argument (PROOF:49-52) is right. In G2_corr every class-membership event (steps 1–5) is at
    the current n; only the beta-min enters through liminf / n_BM; and k_n is undefined for s > K, so the master's floor
    hypothesis is not even meaningful below 2s₀.
- **Energy and beta-min.** They map identically: Σ_𝒞𝒞 = Σ, σ²_𝒞 = σ², and ρ_n^{BM} = ρ_n. The → ∞ branch is named
  explicitly at [MISR-R] :104.
- **Constants of (E).**
  - From G2_corr :22-24 and :50, C is MIS-R (i)'s constant on 𝒦^λ_n(s, A, 2M₀+1, (c/8)^{1/2}, C_OS(s, A), c₀(s, A)+1).
  - That constant is [POST2] Claim C (ii) at σ*² = 1 ([MISR] :63-64, :110-113), so C depends only on (s₀, A, M₀, c).
  - φ₀ = (c/8)^{1/2} ≤ 1 holds because c ≤ 1 (λ_min of a correlation block is ≤ 1).
  - n* depends on the sequence through n_BM.
  - HPM: 2Cr_n + … ≤ 2b_n.
- **Deterministic facts (P0).** These are correct, including the case S₀ ∉ Ω (δ = 1). y^r is non-constant almost
  surely because ε has a density.
- **Markov steps.**
  - P(MPM ≠ S₀) ≤ P(δ_n ≥ ½) ≤ 2Eδ_n.
  - O_P from Eδ_n = O(r_n): P(δ_n > Lr_n) ≤ Eδ_n/(Lr_n). The finitely many n < n* are handled because δ_n ≤ 1 and r_n > 0.
- **Cor2X.**
  - The quotation of [RV] :263-275 and (S1)/(S2) (:28-29) is faithful.
  - Σ_n correlation gives R = Σ_n and Σ_jj = 1.
  - Energy: β_{S₀}ᵀΣ_{S₀S₀}β_{S₀} ≤ tr(Σ_{S₀S₀})·s₀b_hi² = s₀²b_hi², via λ_max ≤ trace for a PSD matrix.
  - Beta-min: ρ_n ≥ nb_lo²/(σ*² log n) → ∞.
  - (A2): the 5(…) range contains the 3(…) range.
  - The three recorded conclusions follow.
- **Unstated hypotheses.** None found.
  - m, Σ and p are parameters; s₀ ≤ p is automatic.
  - n ≥ 3 is in §0.
  - σ² > 0 and independence are in §0.
  - Fixed M₀ and c are in the §1 preamble.
- **REPORT vs STATEMENT.**
  - REPORT §1–§2 restate only STATEMENT §§1, 2, 4, 7 content. §5's vanishing-floor item is labelled OPEN.
  - The registry blocks match STATEMENT. Spans: 29-48, 50-58 and premises 14-27, 60-63, 77-84. The status line is
    PROOF:3 verbatim, with conditions identical to CorGb-plus's.
  - The conclusion fields match (E): b_n for Eδ_n and the PIP error, 2b_n for HPM and MPM.
  - Cor2X's empty `implies` with the explanatory note is consistent with STATEMENT §6 (conclusion-level only).
- **DEPS.** All sha values match (recomputed). The named checker files exist (`K1_linecheck_opus.md`,
  `K3_recheck_opus.md`, `K3_disposition.md`). Per the read restriction of my brief I did not open them, so the "spot
  check" is limited to hash currency and existence.
- **STRONGER tag and caveats.**
  - Every Thm2X hypothesis is implied by the recorded one (Cor2X).
  - The conclusions are at least as strong (expectation ⇒ O_P and w.p. → 1).
  - The 3(…) vs 5(…) gain is real.
  - Caveat (a) is complete: the conditions are CorGb-plus's, plus Prop-LB through POST2:C.
  - Caveat (b): the incomparability with LSF is right. m♯_n ≤ m̄_n gives min(p, k_n) ≤ k̄_n, but LSF allows ψ_n → 0;
    and m♯_n < m̄_n strictly in practice (e.g. 17 vs 32 at n = 100, A = s₀ = 1), so LSF asks for sets CorGb-plus never
    touches. "(A2) stronger than LSF" is true (E1).
  - The tag is correctly scoped to "against the constant-floor reader statement only".

## (d) Gates

- **correct — PASS.** Every step of P0–P3 checks against STATEMENT and the cited sources. The q = 0 instance,
  object identity, floor domain and thresholds, constants and Markov steps are all right.
- **strength — PASS.** The claims assert exactly what the master plus B4.1 deliver. STRONGER is correctly scoped, with
  both caveats attached. Better-theorem items are listed separately below.
- **faithful — PASS.** The quotations of CorGb-plus, B4.1, [W3P] §0, [MISR] §0 and recorded Theorem 2 are faithful.
  Citecheck shows 0 failures and N1 reproduces byte-for-byte. E2, E3 and E7 are wording only.
- **statuses — PASS.** PROOF:3 is "PROVED (by this seat, unchecked), conditional on …", carrying CorGb-plus's six
  conditions. The §5 statuses are quoted verbatim (citecheck). Nothing is called checked that is not.
- **sweep — PASS.** The STATEMENT copies in PROOF and REPORT are consistent. DEPS hashes are current. The REPORT
  registry blocks equal STATEMENT. The OPEN label is present.
- **reader — PASS.** The card sentence and the READER_DELTA proposal match Thm2X and keep the conditional mark and the
  COEXIST decision. E5 and E6 are suggested wording improvements.

## Better-theorem proposals (not findings)

1. **Beta-min at a fixed level.** CorGb-plus allows liminf ρ_n^{BM} > 16c₀(s₀, A)/c instead of ρ_n → ∞ ([MISR-R] :103;
   G2_corr [R-3]). Thm2X could state that branch, with C then also depending on the liminf.
2. **Random intercept.** α may be any real random variable (master §2 setting), since GR^c sees only contrasts.
3. **Free extra conclusions.** The same deterministic route gives P(ξ_q ≠ S₀) ≤ Eδ_n/min(q, 1 − q) and
   E sup_{T≠S₀} π(T) ≤ b_n ([MISR] :119-120).
4. **Hypotheses only for large n.** (A1)–(A2) are needed only for n ≥ max(3, 2s₀) (all large n), not at every n ≥ 3.

## (e) Score

**9.6.** There are no C, S or F findings, and the derivation is short, fully cited and correct. The score reflects only
C/S/F, so the editorial items do not lower it; I hold back 0.4 for residual uncertainty, since the result is a pure
instance-of-master proof whose weight rests on consumed claims taken as true.

COUNCIL-VERDICT round=R1 manifest=6f8c05aa83e3063f9b48d8cf42c52c3f49261e0db36b6268419159bc95f06243 seat=opus score=9.6 gates=PASS

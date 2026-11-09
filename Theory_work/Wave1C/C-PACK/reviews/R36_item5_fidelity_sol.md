# R36 — independent fidelity review of item 5

VERDICT: FAITHFUL-WITH-FIXES

The seven proof files preserve the council-passed theorem and its substantive repairs. I found no FATAL or MAJOR discrepancy. The fixes below concern incomplete definitions, two overstatements in recovery-proof bookkeeping, one dropped out-of-scope qualification, and two editorial assertions. They do not require changing the theorem's hypotheses, constants, rates, or headline.

This was a read-only review of the sources; only this report was written. No git state changes were made. This is a fidelity verdict for the W1-PXN result, not a review of the newer C-PACK theorem.

Path conventions for all citations below (paths are relative to the repository):

- `C/` = `Theory_work/Wave1C/C-PACK/item5_PXN_consolidated/`.
- `B/` = `Theory_work/Wave1/W1-PXN/`.
- `N/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`.
- `P` = `N/branch_snapshots/API-PXNGAP/PROOF.md`.

Line numbers refer to the files as read for this review. Findings quote the actual consolidated text, not APPLIED_ERRATA's description of it.

## Numbered findings

### 1. MINOR — the all-data start law and actual-block aggregation quantities need definitions

**Consolidated locations:** `C/00_statement_and_conventions.md:56`, `:59`, `:130-132`; `C/03_start.md:38-45`.

**Baseline:** `P:240-241` explicitly specifies “with q, e the T22(i) aggregation quantities of S° on the actual blocks”; `B/reviews/R16_I6_P3_P4_deps_codex.md:14`, `:23-25` distinguishes their general definitions from the recovered-group specialization. The cited baseline input defines the normalized start and general quantities at `N/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md:19-25`.

**Exact consolidated text:**

> Block tables: r_b(U) = m(U)/m(∅) for U ⊆ block b.

> On 𝒜_n these equal the aggregation quantities q, e of the cited result T22(i-a) on the actual blocks (Lemma T).

> **Statement.** On LH-iid: q = O_P(√(log n/n)), e = O_P(p√n e^{−c₆n}) (c₆ > 0 fixed), and, on {q < 1},

The text gives the group formulas but never writes the normalized law π₀ or the general actual-block q,e definitions. Its all-data probability statements thus require consulting the definitions of the external T22 input. The recovered-group deletion formula is not the definition on unrecovered blocks: a block may contain several reference variables, and the general deletion quantity has a 1/a power. This is a completeness omission, not evidence that the proof used the wrong formula or a changed theorem.

**Exact fix text:** insert after the block-table sentence in Part 0:

```text
For S ∈ Ω, define γ₀(S) := [w(|S|)/W_K]∏_b r_b(S ∩ C_b),
Z̄₀ := Σ_{S∈Ω} γ₀(S), and π₀(S) := γ₀(S)/Z̄₀; set π₀(S) := 0 outside Ω.
Here C_b denotes a method block; the group version uses the population groups instead.
For a feasible reference S° let U_b° := S° ∩ C_b and s := |S°|. Define
a_bj := Σ_{U_b°⊆U⊆C_b, |U∖U_b°|=j} r_b(U)/r_b(U_b°),
D_b := max_{1≤j≤|C_b∖U_b°|}(j!a_bj)^{1/j}, with an empty maximum equal to 0,
q := (p−s)^{−1}Σ_b D_b if s < p, and q := 0 if s = p,
e := 2p max{[r_b(U)/r_b(U ∪ U_b°)]^{1/a} : b, U ⊆ C_b,
           a := |U_b°∖U| > 0}, with an empty maximum equal to 0.
These are the actual-block T22(i) quantities on every data set. On 𝒜_n they equal
the group versions in §3.2; there each nonempty U_h° is a singleton, so a = 1.
```

These are definitions from the already-cited T22 input, not an additional theorem or premise. As elsewhere, uses requiring S° ∈ Ω are after the standing feasibility onset.

### 2. MINOR — “holds at t = t* only” strengthens the repaired bound into an exclusivity assertion

**Consolidated locations:** `C/02_design_events.md:58-59`; repeated in `C/APPLIED_ERRATA.md:25`.

**Baseline:** `B/lemmas/R_branch_repair.md:9-15`; `B/reviews/R14_I4_TheoremR_codex.md:22`; `B/reviews/R21_repair_recheck_codex.md:13` says precisely “This bound is asserted only at t*.”

**Exact consolidated text:**

> (The display (R-a)/(R-b) is not a single chain over all t: S(t) ≤ K_n holds at t = t* only; for t near ρ a within-pair term of S(t)
> is close to ½.)

The baseline rejects a bound uniformly over every t. It does not assert that t* is the unique point satisfying the inequality. That stronger assertion is false, for example whenever K_n exceeds the number of pairs: S(t) is then bounded by K_n at every threshold. The primary (R-a)/(R-b) displays themselves are correct.

**Exact fix text:** replace the parenthesis by:

```text
(The display (R-a)/(R-b) is not a single chain over all t: S(t) ≤ K_n is asserted
here only at t = t*. A uniform assertion over all t is false; for t near ρ a
within-pair term of S(t) can be close to ½.)
```

In `APPLIED_ERRATA.md:25`, replace `S(t) ≤ K_n holds at t = t* only` by `S(t) ≤ K_n is asserted here only at t = t*`.

### 3. MINOR — the assembly treats (R′) as an alternative proof of the entire quantitative clause (R)

**Consolidated location:** `C/05_posterior_output.md:76`.

**Baseline:** `B/STATEMENT.md:54-57`, `:107-108`; `B/FINAL_PROOF.md:40-41`; `B/lemmas/CR_corr_tails.md:48-55`; `B/reviews/R20_midpoint_codex.md:7`, `:26-28`. The baseline explicitly distinguishes the sharper constant from the independent cruder route.

**Exact consolidated text:**

> (R) is Theorem R (§2.3), or its alternative (R′) (§2.4).

The alternative proves summability and eventual p^{−C}, but does not prove the I* exponent or the prefactor in the theorem's explicit display. Those are proved separately in §2.3. Thus this is incorrect proof-routing language, not an absent proof of (R-b).

**Exact fix text:** replace that sentence by:

```text
(R), including its explicit constant and exponent, is Theorem R (§2.3).
The independent route (R′) (§2.4) also proves summability and eventual p^{−C};
it supplies a weaker explicit bound and does not replace (R-b).
```

Leave the following sentences assembling (S) through (C) unchanged.

### 4. MINOR — the excluded no-tweak route loses its recorded GAP qualification

**Consolidated locations:** `C/06_A_dependence_and_scope.md:39-40`; deletion expressly acknowledged at `C/APPLIED_ERRATA.md:69`.

**Baseline:** `P:479-481`; `B/lemmas/ERRATA.md:8-29` contains no erratum removing this qualification. `B/REPORT.md:26-27` continues to exclude the method without LS0.

**Exact consolidated text:**

> anything about the original method without LS0 (the earlier no-tweak route is restricted to c = 1 and is
> not claimed)

**Exact baseline text:**

> (the no-tweak route P7/W5-R1 is c = 1 only and remains GAP as reviewed; Lemma Tr-J removes its
> range objection, see REPORT "Outside scope")

Dropping the obsolete file pointer is appropriate; dropping “remains GAP as reviewed” loses a substantive status qualification. “Not claimed” preserves the theorem's exclusion but does not preserve that status.

**Exact fix text:** replace the consolidated parenthesis by:

```text
(the earlier no-tweak route is restricted to c = 1 and remains GAP as reviewed;
Lemma Tr-J removes its range objection only; it is not claimed here)
```

In `APPLIED_ERRATA.md:69`, replace the replacement description by:

```text
obsolete cross-reference removed; c = 1 restriction, reviewed GAP status, and
the limited effect of Lemma Tr-J retained in the replacement parenthesis
```

### 5. NIT — the blanket “verbatim archive” description also covers descriptive entries

**Consolidated locations:** `C/00_statement_and_conventions.md:150`, `:152`, `:154`, `:160-162`; `C/OPEN_QUESTIONS.md:13-15` itself acknowledges the distinction.

**Baseline:** `B/REPORT.md:54-69` labels its quoted dependency ledger; `B/FINAL_PROOF.md:26` supplies the LM citation; `B/reviews/C1_council_codex.md:22` supplies the RO wording; `B/reviews/C1_council_opus.md:13` gives its qualified verification status.

**Exact consolidated text:**

> Statuses are copied verbatim from the archive records.

The T22, T03♯ and W7 quotations are faithful. The LM entry “published inequality (citation checked in review)”, OP entry “candidate premises of the theorem, taken as hypotheses”, and W3 entry “cited for computations only” are descriptive provenance, not verbatim registry statuses. The RO “SF/XF-reviewed” wording is genuinely present in the Codex council baseline; it is not an invented unqualified XF VERIFIED verdict. The defect is the blanket description, not a substantive status upgrade.

**Exact fix text:** replace line 150 by:

```text
Quoted archive statuses are reproduced verbatim where given; other entries
explicitly describe provenance or the role of an assumed input and do not assign
a new verification status. NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`.
```

Replace the table heading `Status (verbatim)` by `Status quotation or descriptive provenance`.

### 6. NIT — the introduction points to the group-version section for external inputs

**Consolidated location:** `C/00_statement_and_conventions.md:4-5`.

**Baseline:** `B/FINAL_PROOF.md:25-34`, `:67-71`; `B/REPORT.md:54-69` distinguish probability tools and external inputs. In the consolidation the external-input section is actually §0.7 at line 148; §0.6 at line 128 is Lemma T.

**Exact consolidated text:**

> external results listed in §0.6

**Exact fix text:**

```text
external results listed in §0.7
```

## Answers to Q1–Q4 and Q6

### Q1. The theorem, hypotheses, constants, exclusions

Subject to the local findings above, **yes**: the target clauses are preserved. No theorem premise is dropped, and no new hypothesis is imposed.

| Clause / scope | Consolidated evidence | Baseline evidence / fidelity result |
|---|---|---|
| LH-iid, fixed A ≥ 1, p ≤ n^A, p → ∞, no lower growth bound | `C/00_statement_and_conventions.md:10-27`, `:84` | `B/STATEMENT.md:13-20`; identical family and SIZE onset; A > 1 retained |
| Exact v3 posterior, prior, constants | `C/00_statement_and_conventions.md:52-56` | `B/STATEMENT.md:22-27`; same K, H, D, Q, a₀ = b₀ = .01, ν, w, W_K; start-law definition completeness is finding 1 |
| LS0 and operational premises | `C/00_statement_and_conventions.md:58-80` | `B/STATEMENT.md:29-48`; EX-A, EX-S, CAL, SR, GUARD G1/G2 and OP-LS0 remain assumptions; emitted centre, completed scans, stopped-LS0-in-U, exact DP, move budget and production obligation retained |
| (R) | `C/00_statement_and_conventions.md:87-89`; `C/02_design_events.md:51-78` | `B/STATEMENT.md:54-57`, `:107-108`; same prefactor, t*, I*, n ≥ 5/SIZE condition, p^{−C} onset and exponential summability; findings 2–3 concern commentary/assembly |
| (S) | `C/00_statement_and_conventions.md:90-92`; `C/03_start.md:45-108` | `B/STATEMENT.md:58-60`, `:112`; same truncated moment, tail, rate, masking normalization and χ² constant; no sharpness restored |
| (E) | `C/00_statement_and_conventions.md:93`; `C/03_start.md:117-124` | `B/STATEMENT.md:61`; no extras, Φ = c, exact-mode eligibility; N3 bypass qualification preserved |
| (T) | `C/00_statement_and_conventions.md:94`; `C/04_search.md:139-176` | `B/STATEMENT.md:62`, `:110-111`; scoring, arrival and certification separated with the correct cap thresholds |
| (P) | `C/00_statement_and_conventions.md:95`; `C/05_posterior_output.md:5-39` | `B/STATEMENT.md:63`, `:109`; T03♯, enlarged design event and deterministic-sequence transfer, same joint-law O_P rate; only convergence of Eδ₁, no expectation rate added |
| (C) | `C/00_statement_and_conventions.md:96-98`; `C/05_posterior_output.md:45-72` | `B/STATEMENT.md:64-66`; same every-n composition, D_n, limits, liminf, strict output; s₀ > K zero extension and feasibility-qualified exact-branch bound preserved |
| (K) and joint event | `C/00_statement_and_conventions.md:99-100`; `C/04_search.md:159-176` | `B/STATEMENT.md:67-68`, `:110-111`; `B/lemmas/LS_P6_repair.md:30-36`; identical general and sharp score counts; 𝒯_n includes Ω_n, 𝒵_n and correct centre; conclusions explicitly require n ≥ n₀ with ℓ_n ≥ c |
| Exact branch, group transfer and onsets | `C/00_statement_and_conventions.md:113-146` | `B/STATEMENT.md:103-106`; `B/FINAL_PROOF.md:12-23`; no lower p bound, branch conditioning, or independence of the joint events introduced |
| Separate start/search events and thresholds | `C/01_tools.md:158-164`; `C/03_start.md:50-55`; `C/04_search.md:3-5`, `:83` | `B/FINAL_PROOF.md:30-34`, `:45`, `:59-65`; R30 event separation retained; family exponents D = A and A(s₀+2) and Mills u_n distinguished |
| Exclusions and A-dependence | `C/00_statement_and_conventions.md:104-107`; `C/06_A_dependence_and_scope.md:5-49` | `B/STATEMENT.md:72-88`; `B/REPORT.md:26-34`; no delivery, no method-without-LS0 guarantee, no masked PIP/evidence accuracy, no groups-of-5 theorem, no superpolynomial theorem, no finite-n guarantee, no uniformity in A; finding 4 restores an ancillary GAP status |

The notation changes are transparent and harmless: 𝓜 for the masked set, q_R for the recovery threshold parameter, mar_n for the score margin, b_min for the beta minimum, u_n for the Mills threshold, and family-indexed truncation thresholds. Enlarging the SE range using k_n is the prescribed replacement, not a new premise. The added Haar and deletion-covariance explanations come from the baseline reviews, not a newer result.

### Q2. E-1 through E-22, checked against the actual proof files

All 22 mathematical corrections are applied at the required places. APPLIED_ERRATA is accurate about their substantive implementation. Its exclusivity gloss for E-15 needs finding 2's wording fix; its deletion log also exposes finding 4. No superseded erroneous (L), LS(i), P6′ maximum inequality, arbitrary-t chain, or unrestricted B(ii) remains in the seven proof files.

| Erratum | Actual consolidated location | Check against baseline ERRATA / replacement |
|---|---|---|
| E-1 | `01_tools.md:103`, `:130`, `:162` | Factor 2 on exp(−n^{1/3}) retained |
| E-2 | `01_tools.md:95-105`, `:158-164`; `02_design_events.md:37-40` | X-measurable family, fixed φ₀, norm intersection, eventual scope, correct application events |
| E-3 | `01_tools.md:149-150` | Signal-norm remark replaced as specified |
| E-4 | `01_tools.md:111`, `:145-146` | Exact admissible C₂ retained |
| E-5 | `04_search.md:25-30` | Empty/zero increments removed before Tr-J; deterministic remaining indices justified |
| E-6 | `01_tools.md:88-91` | Correct P3′ reference and uniformly bounded u |
| E-7 | `03_start.md:5-14`, `:29-30` | Deterministic sets, |A| ≤ n−3 and general Haar dimension restriction; unused status retained |
| E-8 | `04_search.md:139-149` | min(c,ℓ), first-arrival meaning and ℓ ≥ c retained |
| E-9 | `04_search.md:159-176`; `00_statement_and_conventions.md:99-100` | Correct joint event/onset and sum over actual lattice sizes; separate arbitrary-data maximum |
| E-10 | `03_start.md:120-127` | N3 bypass, not proof; exact arithmetic qualification |
| E-11 | `05_posterior_output.md:51-55` | GUARD G2 / RO, definition of augmented potential run, implementation obligation |
| E-12 | `04_search.md:102-124` | Original E3-only estimate completely replaced by E5; relative RSS accuracy and uniform additive o(1) |
| E-13 | `04_search.md:75-77` | Correct incomplete-destination versus zero-gain component split |
| E-14 | `04_search.md:58`, `:127-129`; `00_statement_and_conventions.md:36-37` | Empty minima and heuristic-only failure language retained |
| E-15 | `02_design_events.md:51-56` | Correct split displays and onset/summability; only the subsequent “only” gloss is too strong (finding 2) |
| E-16 | `02_design_events.md:80-82` | .17 removed; vacuous ≈1.13·10⁶ substituted |
| E-17 | `02_design_events.md:61-75` | Direct strict-global-margin proof; no defective A0(c) or A2 premise imported |
| E-18 | `00_statement_and_conventions.md:113-119`; `05_posterior_output.md:57-61` | Hypothetical data functions on every branch; exact-branch feasibility cases and zero extension retained |
| E-19 | `03_start.md:90-91`; `00_statement_and_conventions.md:107`; `06_A_dependence_and_scope.md:40` | Unsupported sharpness removed; slow-p observation is supported by R16:50 |
| E-20 | `03_start.md:45-47`, `:66-74`, `:86-88` | q < 1 condition and global indicator inequality both present |
| E-21 | `06_A_dependence_and_scope.md:36-37` | Ancillary order explicitly heuristic; only vanishing failure is proved |
| E-22 | `06_A_dependence_and_scope.md:42-45` | Correct η, c₂, stated σ², M, denominator 14 and .775 / .904 values; inherited ≈20 comparison discussed below |

Later sweep/council changes also appear: two Lemma E events (R30 #2), eventual versus every-n separation (R30 #4), distinct thresholds (R30 #5), resolved D1/D2, corrected onset envelope with SIZE onset, and concrete LS0 call. The optional finite-n centring sentence at `03_start.md:110` is copied from `B/reviews/C1_council_opus.md:50`; it is not a new transcriber claim imported from C-PACK.

### Q3. Old-candidate references and silent reliance

No internal reference to `API-PXNGAP/PROOF.md`, `PROOF:nnn`, its step/line numbers, or a replacement lemma file remains in the seven proof files. The remaining `PROOF.md` citations are explicitly to external W7-PART, W2-BOOK and W3-PXN inputs; the W3 heuristic citation at `04_search.md:128` is permitted external provenance, not a candidate-proof dependency. MAP and APPLIED_ERRATA intentionally contain the old correspondence.

No proof step was found that silently needs the candidate for a missing derivation: the condensed Haar argument, the F1-dependent deletion calculation, de-randomisation and output closure are now in the text. Finding 1 concerns missing definitions from the cited external T22 input, rather than an untranscribed candidate proof step. The selfcheck's narrow claim about absence of candidate line references is corroborated; it is not by itself a proof-fidelity check.

### Q4. External inputs and statuses

No substantive status upgrade was found. The answer to the literal question “are all entries verbatim ledger statuses?” is **no**, because several entries are descriptive, and REPORT §3 has no separate LM/RO/OP status string to copy. Finding 5 makes that distinction explicit.

- **T22:** the longer quote at `00_statement_and_conventions.md:155` agrees with `B/reviews/R16_I6_P3_P4_deps_codex.md:31`; the abbreviated ledger is `B/REPORT.md:55-56`. “Not adopted” remains. The uses are deterministic (i-a)/(ii-a), with q < 1 and eventual feasibility, not conditional T22(iii).
- **T03♯:** `00_statement_and_conventions.md:157` preserves the exact statement-record quote and SF/XF qualifications of `B/REPORT.md:59-61` / R16:34. Part 5 separately proves the random-design passage; it does not attribute an unconditional LH-iid theorem to TH128. Locked T03 is excluded with H-T02 and same-family qualifications at `06_A_dependence_and_scope.md:47-48`.
- **W7 A/B:** both registry strings at `00_statement_and_conventions.md:158-159` preserve the stars, A2 premise warning, A0(c) GAP, restricted B scope and Corollary-B GAP in `B/REPORT.md:64-68`. The direct R0 argument bypasses A0(c)/A2. For clarity, retain REPORT's separate explanation that the explicit constant was independently checked in W1-PXN (R14, R21 and council); that is a local verification record, not an update of the quoted registry status.
- **RO / GUARD:** the consolidated “PROVED” / “SF/XF-reviewed” phrase is supported verbatim by `B/reviews/C1_council_codex.md:22`. The more precise council status is “PROVED, SF VERIFIED, XF VERIFIED*” (`B/reviews/C1_council_opus.md:13`). No unconditional XF VERIFIED claim or discharged implementation claim is made. The closure is also proved directly from G2, as required by `B/REPORT.md:43` and R15:16,32-38.
- **W3-PXN:** F2–F5 and the heuristic are identified as computations; no reviewed theorem status is invented. The historical PXN P1 row in `B/REPORT.md:69` is not reproduced, because R0 now proves its deterministic implication in place. If a historical dependency ledger is retained, quote that row as “PROVED given C1 (W3-PXN); SF VERIFIED* (...); XF VERIFIED (A-REV3; A-REV6 via W7 Thm B)”, and state C1 is supplied by CONC′. Do not turn “computations only” into a claim that all W3 results are verified.
- **LM:** the formulas and citation match `B/FINAL_PROOF.md:26`, `P:26`, and `B/reviews/R11_I1_TrJ_codex.md:20`. “Published inequality (citation checked in review)” is an accurate description, not a copied registry verdict. Wendel and Mills also occur in the baseline derivations (`P:137-139`; `B/lemmas/L_strict_localmax.md:28-30`); they are not new dependencies introduced by the transcriber.
- **CONC:** the old cited-standard/Bickel–Levina entry in `B/REPORT.md:62-63` is replaced by the complete CONC′ proof, as prescribed; omission of that unused historical citation is not a status upgrade.

### Q6. Newer C-PACK content

None found. In particular, Part 1 retains the original corrected (E4) expansion with the bounded R_A remainder, and Part 4 retains the E5-based (L) repair. There is no newer e4 replacement, Song–Liang replacement argument, or claim that OP/delivery/production premises have been discharged by an “LH-iid unconditional” result. Ordinary statements about unconditional group laws and the joint data law are already in the W1-PXN baseline and must not be mistaken for newer-ticket contamination.

## Q5 — faithful disposition of every OPEN_QUESTIONS item

1. **Algorithm definitions / R0:** keep the direct margin argument. It is precisely the adopted repair (`B/lemmas/R_branch_repair.md:20-26`; R21:16). Inlining a short method definition is permitted but not required to change the theorem. A faithful insertion is: “The top-down cut recursively splits a dendrogram node while its size exceeds B_n; retained clusters are packed whole by next-fit with capacity B_n.” This behavior is checked in `B/reviews/C1_council_opus.md:18-20` and R14:9. Do not import A2 or the false unrestricted A0(c).

2. **Explicit W7 constant:** keep (R-b) with exactly its current constant and n ≥ 5/SIZE scope; D2 was resolved, not left open. The premise that the derivation is absent from the supplied sources is too strong: R14:30-40 and R21:13-14 give the bounding chain, and both council seats rechecked it (`B/reviews/C1_council_codex.md:22`; Opus:14). It is faithful to cite the external W7 result and separately record those checks. Inlining that same derivation is optional; no different bound or registry upgrade is authorized. R′ cannot replace the full explicit clause (finding 3).

3. **Unavailable verbatim statuses:** distinguish quoted statuses from descriptions (finding 5). Keep the existing exact T22/T03♯/W7 quotes. For RO, the current phrase is a real Codex council quote; if giving a verification status, use the Opus council's qualified “PROVED, SF VERIFIED, XF VERIFIED*”, not an unstarred XF VERIFIED. LM is a checked classical citation and OP is assumed. I compared the local T22 statement (`.../T22_T16_start_aggregation/STATEMENT.md:19-41`) and TH128 statement (`N/branch_snapshots/W6-FIXREV2/STATEMENTS.md:19-35`, `:51-57`): the used aggregation/odds formulas and the fixed-design hypotheses match, with the missing T22 definitions addressed in finding 1. No internet lookup or new theorem status is needed.

4. **F1 / deletion covariance:** keep the inlined explanation. It is exactly supported by `B/reviews/R16_I6_P3_P4_deps_codex.md:25` and the adopted nonzero-partial-correlation check. Removing an undefined F1 pointer while retaining its derivation is faithful.

5. **Haar expansion:** keep it. `B/reviews/R13_I3_P2_B_Lambda_codex.md:22-26` supplies the covariance-factor/scaling argument and `:14` supplies the independent Beta singleton laws. This is baseline verification detail, not foreign content. Preserve deterministic indices, the dimension restriction and the unconditional-law rule; the consolidation does.

6. **U3 constants/onset:** keep the sharper bookkeeping exactly as written. `B/reviews/R17_I7_margins_codex.md:27` explicitly supplies both e_n ≤ c′H/(4H+c′) and 2 log 2 + log(1+1/n) < 2. No statement constant changes.

7. **O2 labels:** keep T03♯ and CONC′, as the definitive proof map prescribes. Keep the discovery extension labelled “CONJECTURE, not written”; do not claim superpolynomial-p coverage. This is a faithful propagation of the input replacements, not a new extension.

8. **O5 ≈20:** E-22 and the council correction retain it as a rough comparison (`B/lemmas/ERRATA.md:29`; `B/reviews/C1_council_opus.md:46`). Faithful transcription may keep it with the question's A-dependence noted. If precision is desired, replace only that illustrative comparison by “against (2A+1) log 200, which is approximately 15.9 already for A = 1”; this is arithmetic clarification, not a changed theorem or a new onset guarantee. The corrected positive term remains .775 for σ² = 1.

9. **Small glosses:** (i) “budget constants” does not alter the exact-branch threshold (`B/lemmas/R_branch_repair.md:29-30`). (ii) The per-scan decomposition is an upper bound: at k = K there may be fewer than p feasible flips (`B/reviews/R21_repair_recheck_codex.md:10`); “at most p flips” is the clearest wording. (iii) One scan at sizes s through s₀ is precisely that same baseline review and the repaired cost sum. (iv) The lattice definition is correct: W6 defines Lat(S°) = {U′ ∪ P′ : U° ⊆ U′ ⊆ S₀, P′ ⊆ P°} (`N/branch_snapshots/W6-FIXREV1/T38_STATEMENT.md:52-54`); here P° = ∅ and S₀∖S° = 𝓜, giving exactly the displayed specialized lattice. Keep these glosses.

10. **Implementation pointers:** keep them as source pointers, not proof that production satisfies OP. Their mathematical uses and cited locations were checked in baseline R14:9,26; R15:9-20,30-38; R21:9-18; council Opus:18-25. The production obligation is preserved. The opening description of W6 conventions at `00_statement_and_conventions.md:160` is a loose line range (the objects actually span W6:32-51); the specific LS0 and G2 citations in the closure are correct.

11. **Notation:** keep the disclosed collision-removing changes. No full generic-subset rename is needed for fidelity; A's dual meaning is explicitly flagged. Preserve the distinction between the SE cutoff and score margin, and between Mills and family-truncation thresholds.

12. **L_n / k_n:** keep the replacement lemma's larger range. `B/lemmas/P8_T03sharp.md:32-35` and `B/FINAL_PROOF.md:37-39` are definitive here; k_n is a proved deterministic upper bound for m♯_n. This supplies every original design-event use without strengthening LH-iid's assumptions.

13. **C_q:** keep a fixed dominating constant with the recorded proportional dependence; do not silently identify an asymptotic equivalent with an exact finite-n constant. `B/reviews/R16_I6_P3_P4_deps_codex.md:12`, `:52` explicitly allows that choice. The displayed 2.3 C_e g ξ_n calculation, and C_q proportional to C_e g e^{2κ_E}√(A+1), are faithful; computing a sharper numeric constant is unnecessary.

VERDICT: FAITHFUL-WITH-FIXES — FATAL 0; MAJOR 0; MINOR 4; NIT 2.

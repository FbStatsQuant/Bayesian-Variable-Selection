# W3-D2 — K2 re-check of the K1 repairs, the STATEMENT v1.1 → v1.2 diff and the REPORT registry blocks (Claude Opus 5.5, high, fresh; 2026-11-17)

Brief: `reviews/K2_brief.md`. Read: `reviews/K1_linecheck_opus.md`, `reviews/K1_disposition.md`, `reviews/K1_repair.diff`,
`reviews/STATEMENT_v1.1_to_v1.2.diff`, `PROOF.md` (v1.1), `STATEMENT.md` (v1.2), `REPORT.md`. Sources read at the cited lines:
[MISR-R] `:48-58`, `:94-108`; `W3-MISR-R/lemmas/G2_corr.md:20-50`; [W3P] `:16-45`, `:60-118` (Theorem 1, Corollary 1R);
[R1] `:23-27`; [RV] `:255-285`, `:445-520`; `W3-READER/NOTATION.md:15-20`, `:41-43`; `W2-APP/lemmas/L1_POST.md:18-25`;
registry rows (`INFRA/registry/claims.tsv`, `assumptions.tsv`) for W3-POST:Cor-1R, A:LSF, A:GAUSS-NOISE, C-MIS:GD(b),
C-MIS:Prop-P, W3-POST2:*, W3-POST:Prop-LB. Not read: LOG.md. No scratch files were created.
Tags as in K1: **C** = false or does not follow; **S** = true, but a needed justification is missing; **F** = a citation,
attribution or restatement is not exact; **E** = editorial.

## 1. K1-1 … K1-4 against `reviews/K1_repair.diff`

| finding | resolved? | check |
|---|---|---|
| K1-1 [S] (floor only for n ≥ max(3, 2s₀)) | **RESOLVED** | PROOF `:49-52` adds the reason. The reason is correct: the master's floor is stated with k_n, and k_n is undefined for s > K. G2 uses the floor and energy hypotheses only at the current n (steps 2–3, for n ≥ n₀), and beta-min only through a liminf (step 4). Its conclusion holds for n ≥ n* with the class membership checked at each n. One wording point is E-1 below. |
| K1-2 [F] (B4.1's domain omits p ≤ n^A) | **RESOLVED** | PROOF `:38`. [R1] `:25` is "binom(p,s) ≤ p^s ≤ n^{As}", as cited. The stray "with p = \|𝒞\| = p" from v1.0 is also gone. |
| K1-3 [F] (determinism attributions) | **RESOLVED** | P1 `:23`: §0 `:19`/`:21` support the reading. P3 `:63-64`: [MISR-R] `:52-53` reads "a real random variable α (any dependence on everything)", and (N) at `:56` asks independence of ε from the designs only, so "α* may even be random" is right. P4 `:79` is right for the same reason. |
| K1-4 [E] ([MISR] `:21-22`) | **RESOLVED** | PROOF `:30`. |

**Does the diff break anything?** No. No step changed. The line references into STATEMENT (§0 `:19`, `:21`) are
unchanged in v1.2, because the §0 gloss still takes three lines (`:23-25`) and the v1.2 additions in §7 come after §§0–3.
PROOF's references to [MISR-R] (`:51-54`, `:52-53`, `:56`, `:67-68`, `:31`, `:96-107`) still point to the stated content.
One stale header remains: E-2.

## 2. STATEMENT v1.1 → v1.2

**§0 posterior gloss vs [W3P] `:16-29`.** The coded target is the posterior under the working likelihood
y | S, β_S, σ² ~ N_n(X_Sβ_S, σ²I), with β_S | S, σ² ~ N(0, nσ²(G_S + I)⁻¹), G_S = X_SᵀX_S, and σ² ~ IG(0.01, 0.01),
**on the standardised scale** ([W3P] `:20`, `:26-28`). The model prior is ϖ(S) = w(|S|)/W_K with w(k) = ½/C(2p − 1, k).
I checked that C(p, k)·½/C(2p − 1, k) is the BB(1, p) mass p·C(p, k)B(k + 1, 2p − k), restricted to k ≤ K. So the four
components of the gloss match: standardisation, the coefficient prior, the inverse-gamma prior and the capped
beta-binomial size prior. The ridge form is also more exact than v1.1's "g-prior with g = n". **But the gloss reuses two
symbols that §0 has already defined differently.** This is finding F-1 below.
**Tag EQUAL: right.** The definition is still the pointer "as defined in [W3P] §0 `:16-29`", and the object is unchanged.

**§7 caveat (a) vs §5.** This caveat is faithful. The six conditions of CorGb-plus are those of §5 `:79-80`, verbatim
and in the same order. "Through W3-POST2:C … `W3-POST:Prop-LB` … 'PROVED (by this seat, unchecked)'" matches §5
`:83-84`. Leaving out W2-APP:POST (W3-POST2:C's other condition, which is PROVED-CHECKED) is harmless.

**§7 caveat (b) vs §4(b).** This caveat is faithful in substance: the old master allows ψ_n → 0 on |S| ≤ k̄_n, and
Theorem 2X needs a fixed floor. The incomparability sentence, however, has changed its subject. This is F-2 below.
**Tag EQUAL: right.** §7 lies outside the registered spans (REPORT §6 uses `:29-48`, `:50-58`, `:14-27`, `:60-63`,
`:76-84`), and both caveats only spell out what §4(b) and §5 already say.

## 3. REPORT §6 registry blocks and the §3 card sentence

**Spans.** `W3-D2:Thm2X` uses `:29-48` (§1 heading through (E)) and `W3-D2:Cor2X` uses `:50-58` (§2 through its last
sentence); both are right. The premise spans `:14-27` (§0), `:60-63` (§3) and `:29-48` (Cor2X → Thm2X) are right.
`:76-84` starts at a blank line, but it contains §5: E-3. The **assumption line references are off by one**: F-3.
**Status.** Both blocks give `status_source: PROOF.md:3`. They write the condition list out as in §5 `:79-80` (CorGb-plus's
six conditions). That agrees with PROOF `:3`, "conditional as carried from CorGb-plus@1.0.1 (STATEMENT §5)". Right.
**Conclusions.** Thm2X's conclusion field matches §1, apart from a small imprecision in "explicit bound" (E-4). Cor2X's
conclusion field matches §2. Two fields claim more than §§1–2 and §6, or encode a different hypothesis: Cor2X's
`assumptions` (F-4) and Cor2X's `implies` (F-5).
**Card sentence (§3)** vs STATEMENT §1. The hypotheses (smaller floor range, correlation matrix of a row, relative energy
and beta-min, Σ, β, σ² varying with n) and the four O(r_n) conclusions match §1 and add no strength. "This is Theorem 4
with no omitted predictors" is §4(a), and I checked it against [RV] thm4 (A0)–(A3) with 𝒞 = [p]. The master of
Theorem 4's reader version is CorGb-plus ([RV] `:504-511`). Among CorGb-plus's inputs, only Prop-LB is unchecked:
C-MIS:GD(b) and C-MIS:Prop-P are both "R02 VERIFIED(-WITH-AMENDMENTS); council PASS" in the registry. So "one of which
… has not yet had an independent check" is accurate. There is one wording point: E-5.

## Findings

- **F-1 [F] STATEMENT `:23-24` — the gloss uses σ² and X_S, which §0 has already defined differently.** In §0, σ² is the
  *true* noise variance (`:19`), the σ² of (A3). In the gloss, "N(0, nσ²(X_SᵀX_S + I)⁻¹) given (S, σ²)" uses σ² for
  the working variance on the standardised scale, the variable that gets the IG prior. Read with §0's symbols, the
  sentence says that the prior scale is the true σ², which is not [W3P]. [W3P] avoids the clash by writing σ*² for the
  truth. Likewise, STATEMENT defines only X^r, so a reader can take X_S to be the raw columns; [W3P]'s G_S uses the
  standardised X (`:20`). The pointer still governs, so the tag stays EQUAL; this is a wording fix. *Fix:* "…(columns
  and response standardised, X the standardised design of [W3P] `:20`; coefficients N(0, nv(X_SᵀX_S + I)⁻¹) given
  (S, v), with an inverse-gamma prior IG(0.01, 0.01) on the working variance v on the standardised scale; …)". Any
  letter other than σ² will do.
- **F-2 [F] STATEMENT `:105-107` (caveat (b)) — "the two are incomparable on the floor hypotheses".** §4(b) `:73`
  compares the **masters**: CorGb-plus needs a fixed floor on |T| ≤ k_n, and LSF needs a fixed floor on
  |S| ≤ s₀ + j₀ and ψ_n on |S| ≤ k̄_n. Caveat (b) makes "the two" the old master and **Theorem 2X**. As stated,
  Theorem 2X's (A2) is a fixed c on |T| ≤ 3(A + 1)(s₀ + 1) log n, and that range contains k̄_n: 3(A + 1)(s₀ + 1) log n
  ≥ s₀ + max(j₀, m̄_n) for every n ≥ 4, s₀ ≤ 20 and A ∈ {1, 1.5, 2, 3, 5, 10} (I checked this numerically). The
  log n coefficients compare as 3(s₀A + s₀ + A + 1) against (s₀A + s₀/2 + 1)/log(3/2). When Σ is a correlation matrix
  (R = Σ_n), (A2) therefore **implies** LSF (i)–(ii) with φ² = ψ_n = c. On the floor hypotheses alone, Theorem 2X as
  stated is dominated by the old master; it is not incomparable with it. Overall the two are still incomparable,
  because Theorem 2X's signal and σ² conditions and its general Σ are weaker. Nothing in the tag changes: Theorem 2X
  still covers no case with ψ_n → 0. *Fix:* "…Theorem 2X needs a fixed floor on all its sets. Its master CorGb-plus
  (fixed floor on |T| ≤ k_n) and the old master are incomparable on the floor hypotheses (remark (b)); Theorem 2X's
  own (A2) is stronger than LSF on the floor. STRONGER holds against the constant-floor reader statement only."
  (§4(b)'s own sentence, "Neither master dominates…", is right as written.)
- **F-3 [F] REPORT `:63` — the assumption line references are one line early.** A:CORR-FLOOR-LOG cites
  `STATEMENT.md:34-35`, but (A2) is at `:35-36` (`:34` is (A1)). A:POP-SNR cites `:36-37`, but (A3) is at `:37`
  (`:36` is the second line of (A2)). *Fix:* `:35-36` and `:37`.
- **F-4 [F] REPORT `:71` — Cor2X is tagged `A:LSF`.** In the registry, A:LSF (`assumptions.tsv:9`) is the old master's
  floor, including the vanishing ψ_n on |S| ≤ k̄_n. Cor2X does not hold under LSF; that is caveat (b). Its floor
  hypothesis is a **fixed** φ² on |S| ≤ 5(A + 1)(s₀ + 1) log n, or on 3(·) (§2 `:54`, `:58`). As written, the tag makes
  Cor2X look as if it covers the vanishing-floor case. *Fix:* replace `A:LSF` with `A:CORR-FLOOR-LOG` (with Σ_n a
  correlation matrix, R = Σ_n and c = φ²; §2 `:58` says the 3(·) range suffices), or with a new constant-floor
  assumption on the 5(·) range. Do not use A:LSF.
- **F-5 [F] REPORT `:74` — `implies: W3-POST:Cor-1R` claims more than STATEMENT §2 and §6.** STATEMENT §6 `:91-92`
  says that Cor2X *implies the reader statement of row 1.2* and *coexists* with W3-POST:Thm-1 item 6 + W2-APP:POST.
  W3-POST:Cor-1R ([W3P] `:106-118`) assumes LSF with vanishing ψ_n. Even with a constant floor, it asks the floor only
  on |S| ≤ k̄_n, which is smaller than Cor2X's 3(·) or 5(·) range for n ≥ 4 (see F-2). Its part (b) drops b_lo. Its
  conclusions are Theorem 1's items 1–4, which include ξ_{q_n}, π(|S| = s₀) and sup_h |π(h) − h(S₀)|; STATEMENT §2
  does not state them. Those items do follow elementarily from E δ_n = O(r_n) under Cor2X's hypotheses, but that is
  new text, not STATEMENT. As a claim-level edge, "Cor2X implies Cor-1R" is false, and the parenthetical hedge does not
  remove it from the `implies` field. *Fix:* leave `implies:` empty, matching §6. If wanted, record the relation as a
  note ("conclusion-level: Cor2X ⇒ the reader statement of row 1.2 ([RV] `:263-275`); not an edge to W3-POST:Cor-1R",
  in the style of W3-RM:RM-R's note).
- **E-1 [E] PROOF `:50` — "CorGb-plus's hypotheses … are required only for all large n".** The master's statement
  (`:100-103`) does not say this; it is a reading supported by its proof. The second half of the sentence carries the
  argument. *Fix (optional):* "CorGb-plus's floor and energy hypotheses are used only at the current n ≥ n* (and
  beta-min only through a liminf; k_n is undefined for s > K), and its bounds at n concern the n-th law only (…)".
- **E-2 [E] PROOF `:4` — "Statement: `STATEMENT.md` v1.1 (locked)".** STATEMENT is now v1.2. The v1.2 changes are
  EQUAL and leave §§0–3 lines intact. *Fix:* "v1.2 (v1.1 locked; v1.2 EQUAL)". Also, STATEMENT `:1`'s v1.2 note mentions
  only §7; add "and §0 gloss".
- **E-3 [E] REPORT `:61` — premise span `STATEMENT.md:76-84`** starts at a blank line, and `:77` is the heading. Use `:77-84`, or `:79-84`.
- **E-4 [E] REPORT `:64` — "explicit bound C r_n + (2 + 2 k_n) n^-2 + n^-1".** This reads as one bound for all four
  quantities. In (E) the HPM and MPM bounds are 2b_n, and the bounds hold for n ≥ n*. *Fix:* "explicit bounds b_n
  (E delta_n, E PIP error) and 2 b_n (HPM, MPM) for n >= n*, b_n = C r_n + (2 + 2 k_n) n^-2 + n^-1".
- **E-5 [E] REPORT `:24` (card) — "on sets of size 3(A+1)(s₀+1) log n".** Write "of size at most", as in (A2) `:36`.
- **E-6 [E] STATEMENT `:117` — changelog check cell "K1/council read".** K1 read v1.1 (K1 header), so the §0 gloss
  edit was not in front of K1. *Fix:* cite this re-check (`reviews/K2_recheck_opus.md`) and the council.

No C findings. K1-1 … K1-4 are resolved, and the PROOF diff breaks nothing. The STATEMENT diff tags (EQUAL, EQUAL) are
right. The amendments are wording: F-1 and F-2 in STATEMENT §0/§7, outside the claim spans, and F-3, F-4 and F-5 in
REPORT §6. F-4 and F-5 should be fixed before the blocks go to the recorder.

K2-VERDICT: RESOLVED-WITH-AMENDMENTS

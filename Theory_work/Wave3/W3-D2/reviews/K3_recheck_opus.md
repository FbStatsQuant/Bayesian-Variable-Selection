# W3-D2 — K3 re-check of the K2 repairs (Claude Opus 5.5, high, fresh; 2026-11-17)

Brief: `reviews/K3_brief.md`. Read: `reviews/K2_recheck_opus.md`, `reviews/K2_disposition.md`, `reviews/K2_repair.diff`,
current `STATEMENT.md` (v1.3), `PROOF.md` (v1.2, `:1-12`, `:44-54`), `REPORT.md`. Sources: [W3P] `:16-39`,
`W2-APP/lemmas/L1_POST.md:8-33`, [MISR-R] `:94-108`, `INFRA/registry/assumptions.tsv` (rows A:LSF, A:COEF-BOUNDED,
A:CORR-FLOOR). Not read: LOG.md. The repair diff is byte-identical (apart from `index` lines) to `git diff HEAD` (564f151f) of
the three files, so it is exactly the change since the K2 read. Scratch: `.rc_tmp/` (one numeric sweep; deleted).
Tags: **C** = false or does not follow; **S** = true, but a needed justification is missing; **F** = a citation,
attribution or restatement is not exact; **E** = editorial.

## 1. K2 findings

| finding | resolved? | check |
|---|---|---|
| F-1 [F] §0 gloss σ², X_S | **RESOLVED** | STATEMENT `:23-25`: "X the standardised design, response standardised; N(0, nv(X_SᵀX_S + I)⁻¹) given (S, v), IG(0.01, 0.01) on the working variance v". Matches [W3P] `:20`, `:26-28` (G_S = X_SᵀX_S on the standardised X; σ² ~ IG(0.01, 0.01) on the standardised scale). The letter v is used nowhere else in STATEMENT; X is used nowhere else either, so there is no clash. |
| F-2 [F] caveat (b) subject | **RESOLVED** in STATEMENT `:105-110`. The REPORT copy has a leftover heading: F-1 below. |
| F-3 [F] assumption line refs | **RESOLVED**. REPORT `:65`: `STATEMENT.md:35-36` = (A2), `:37` = (A3). |
| F-4 [F] Cor2X tagged A:LSF | **RESOLVED**. REPORT `:73` uses A:CORR-FLOOR-LOG; `:77` note gives R = Σ_n, c = φ², 5(·) ⇒ 3(·). This is right: Cor2X's last sentence (`:58`) makes the 3(·) floor sufficient. |
| F-5 [F] `implies: W3-POST:Cor-1R` | **RESOLVED**. `implies:` is empty (`:76`). The note (`:77`) states the conclusion-level relation in the words of STATEMENT §6 `:91` and gives the reasons for no edge. "Smaller range" is right for every n ≥ 3 (see §2). |
| E-1 PROOF `:50` | **RESOLVED** (the reviewer's wording, `:50-51`). |
| E-2 PROOF `:4`; STATEMENT `:1` | **RESOLVED** (PROOF `:4` says v1.3 with "v1.1 locked; v1.2–v1.3 EQUAL"; STATEMENT `:1` names the §0 gloss). |
| E-3 premise `:77-84` | **RESOLVED** (REPORT `:63`). |
| E-4 explicit bounds | **RESOLVED** (REPORT `:66` matches (E) `:44-48`). |
| E-5 card "at most" | **RESOLVED** (REPORT `:26`). |
| E-6 changelog check cell | **RESOLVED** (STATEMENT `:120`). |

## 2. Does the diff break anything?

**Claim spans.** The STATEMENT hunks are `:1`, `:22-25` (4 lines replaced by 4), `:105-110` and `:120-121`. Nothing in
§1 `:29-48`, §2 `:50-58`, §3 `:60-63` or §5 `:77-84` changed, in content or in line position. The §0 premise span
`:14-27` changed only in the verbal gloss. The definition is still the [W3P] pointer, so the change is EQUAL, as tagged.
PROOF changed only in `:1`, `:3-4` and `:50-51`; no step changed. REPORT changed only in §2(b), §3 ("at most") and §6.

**New caveat (b) sentence: "Theorem 2X's own (A2) is stronger than LSF on the floor (its range 3(A+1)(s₀+1) log n
contains k̄_n)".** I checked this against `L1_POST.md:20-25`. **It is true for every n ≥ 3, not only for n ≥ 4.** At
n = 3 it needs the cap p in k̄_n = min(p, ·) together with p ≤ n^A. Proof, with L = log n and λ = log(3/2):
- *j₀ branch.* s₀ + j₀ ≤ (2A + 2)s₀ + 2 < 3(A + 1)(s₀ + 1)L, because 3L ≥ 3.29.
- *m̄_n branch.* s₀ + m̄_n ≤ s₀ + 1 + [s₀(AL + log 2) + log 2 + (s₀ + 2)L/2]/λ. Subtract this from 3(A + 1)(s₀ + 1)L.
  The difference is affine in s₀. Its constant term is 3AL + (3 − 1/λ)L − 1 − (log 2)/λ ≈ 3AL + 0.534L − 2.71, which
  is > 0 for A ≥ 1 and L ≥ log 3. Its s₀-coefficient is (3 − 1/λ)AL + (3 − 1/(2λ))L − 1 − (log 2)/λ
  ≈ 0.534AL + 1.767L − 2.71. This coefficient is > 0 for all A ≥ 1 when n ≥ 4 (L ≥ 1.386), and at n = 3 when
  A ≥ 1.31. So the inequality holds for every s₀ ≥ 1 in those cases.
- *n = 3, 1 ≤ A < 1.31.* Here p ≤ ⌊3^A⌋ ≤ 4, so k̄_n ≤ p ≤ 4 < 13.1 ≤ 3(A + 1)(s₀ + 1) log 3.
  (Without the cap, the bound fails at n = 3 only for s₀ ≥ 9, which is impossible because s₀ ≤ p ≤ 4.)

Numeric confirmation (exact ceilings, s₀ ≤ min(p, 400), A ∈ [1, 12] in steps of 0.01, n = 3,…,60, 10², 10³, 10⁴, 10⁶): 0 failures.
The smallest margin is 7.27, at n = 3, A = 2.53, s₀ = 1.
LSF (i) on |S| ≤ min(p, s₀ + j₀) ⊆ {|S| ≤ k̄_n} follows. φ := √c ∈ (0, 1] because R has unit diagonal.
ψ_n := c satisfies ψ_n√n/(log n)^{3/2} → ∞. So with R = Σ_n, (A2) ⇒ LSF (i)–(ii) at every n ≥ 3. The wording needs no
change. An optional precision is E-1 below.

The rest of caveat (b) is consistent with remark (b) `:69-73` and §7 `:97`. Its parts are: "the masters are incomparable",
"Theorem 2X needs a fixed floor on all its sets" and "smaller sets" measured against 5(·). The "smaller range" clause in
REPORT `:77` follows from the same inequality.

## 3. PROOF `:3` vs the REPORT registry blocks

- **Status.** The REPORT `status:` strings at `:64` and `:72` equal PROOF `:3` with its `**` markup removed, character for
  character (I checked this by script). Both blocks give `status_source: PROOF.md:3`. They agree with STATEMENT §5 `:79-80`.
- **Spans.** Thm2X: statement `:29-48`; premises `:14-27`, `:60-63`, `:77-84`. Cor2X: statement `:50-58`; premises
  `:14-27`, `:29-48`. All are right for v1.3.
- **Assumptions.** The line references are right. The A:POP-SNR text is not exact: F-2 below.
- **implies / notes.** Both `implies:` fields are empty, which matches STATEMENT §6 (no claim-level edge). The Cor2X
  `notes:` field is accurate.

## Findings

- **F-1 [F] REPORT `:18` — the heading of caveat (b), "Incomparable with the old master on the large-set floor", keeps the
  subject that K2-F2 corrected.** The body (`:19-22`) now says that the *masters* are incomparable and that Theorem 2X's
  own (A2) is *stronger* than LSF. The heading, read with §2's subject "the claims", says the opposite. *Fix:*
  "**(b) Fixed floor on the large sets.**" Alternatively: "**(b) No vanishing floor (masters incomparable on the
  large-set floor).**"
- **F-2 [F] REPORT `:65` — A:POP-SNR's text "n min_j Sigma_jj beta_j^2 / (sigma^2 log n) -> infinity" drops "j ∈ S₀".**
  Read literally, with min over j ∈ [p] and β_j = 0 off S₀, the quantity is 0 whenever p > s₀, so the assumption could never
  hold. STATEMENT `:37` has min_{j∈S₀}. This error was already present before K2; K2 did not flag it. The text is new
  registry text (`new | … | shared no`), so it should be exact before ingest. *Fix:* "n min_{j in S0} Sigma_jj beta_j^2 /
  (sigma^2 log n) -> infinity".
- **E-1 [E] STATEMENT `:107-108` and REPORT `:20` — "(its range … contains k̄_n)".** This is true as written for every
  n ≥ 3 (§2). Two points are left implicit: the comparison is on R = Σ_n (LSF is stated for a correlation matrix), and
  "contains" means k̄_n ≤ 3(A + 1)(s₀ + 1) log n. *Optional fix:* "(for every n ≥ 3, k̄_n ≤ 3(A + 1)(s₀ + 1) log n; so
  with R = Σ_n, (A2) gives LSF (i)–(ii) with φ² = ψ_n = c)".
- **E-2 [E] PROOF `:1` — the v1.2 note names [K2-E1] and [K2-E2] only.** `:3` was also rewritten (the full conditional
  status, as status_source). *Fix:* add "; status line written out in full (status_source)".
- **E-3 [E] STATEMENT `:121` — the check cell reads "K3 re-check".** *Fix:* `reviews/K3_recheck_opus.md`.
- **E-4 [E] REPORT `:47-48` (§4 chain record) — K2 is missing.** *Fix:* add "Re-checks K2, K3 (Opus 5.5 high, fresh):
  `reviews/K2_recheck_opus.md`, `reviews/K2_disposition.md`, `reviews/K3_recheck_opus.md`."

No C or S findings. All of K2's F-1 … F-5 and E-1 … E-6 are resolved. The diff leaves the claim spans §1–§3 (and §5)
unchanged in content and position. The new caveat (b) sentence is true for every n ≥ 3 (at n = 3 through k̄_n ≤ p ≤ n^A).
PROOF `:3` and both registry blocks agree. F-1 and F-2 are one-line REPORT fixes; F-2 should be made before ingest.

K3-VERDICT: RESOLVED-WITH-AMENDMENTS

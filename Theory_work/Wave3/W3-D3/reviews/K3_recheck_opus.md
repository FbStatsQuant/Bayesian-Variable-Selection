# W3-D3 — K3 re-check of the K2 repairs (Opus 5.5, high; new agent) — 2026-11-17

**Verdict: RESOLVED-WITH-AMENDMENTS** (one E finding and one bookkeeping note; no C, S or F finding).

Scope: `reviews/K3_brief.md`. I read `reviews/K2_recheck_opus.md`, `reviews/K2_disposition.md` and `reviews/K2_repair.diff`,
and the current `STATEMENT.md` (v1.2; §2, §9), `lemmas/B3w.md` (all of it), `lemmas/ASSEMBLY.md` (header and Theorem 2SG
Steps 1–4), `REPORT.md` §§4, 6, `DEPS.tsv` and `deps_hand.py`. I checked them against [W3P] `W3-POST/STATEMENT.md:61-100`
(R1, (E), (F_λ), (F_w), (BM), item 6) and against `INFRA/registry/assumptions.tsv:125` (A:DIST-A3). I did not read LOG.md
or CHECKPOINT files, and I did not change git state. I recomputed every DEPS span hash with a copy of `deps_hand.py`'s span
rule that writes nothing. No scratch directory was created.

## 1. Per-finding table (K2 → repaired text)

| K2 | verdict | check of the repaired text |
|---|---|---|
| K2-1 [S] | **RESOLVED** | `B3w.md:34-40` now uses the v1.2 completion: θ⁰ with supp θ⁰ = S₀, "Then supp θ° = S₀ on every outcome", and '\|supp θ°\| = s₀' is dropped from 𝒜′_n. The three mismatches from K2 are gone. (i) (c) matches its stated target (`:3`, v1.2). (ii) Step 6 (`:105-122`) proves (c) as now stated, for a completion with supp θ⁰ = S₀. (iii) ASSEMBLY Step 3's citation of B3w (c) for supp θ° = S₀ (`ASSEMBLY.md:39-41`) is now accurate. A content difference that predates the repair is K3-1 below (the Borel-function clause). |
| K2-2 [E] | **RESOLVED** | `ASSEMBLY.md:4` reads "v1.2 [K2-2]". |
| K2-3 [E] | **RESOLVED** | `B3w.md:74`: "(SG₁) of B1 with K := L [K2-3]". |
| K2-4 [S] | **RESOLVED** | The row is retagged as proposed (`STATEMENT.md:191`). It is confirmed in §3 below. |
| K2-5 [E] | **RESOLVED** | `REPORT.md:67`: "(F_lambda; phi0^2 = phi^2/4), (F_w; g0 = phi^2/8)" now follows STATEMENT's parameter convention (φ₀ for (F_λ); the floor g₀ itself for (F_w)). The interface clause now reads "(X°, θ°)-measurable events A'_n ⊇ A_n of the completed pair on which the hypotheses of W3-POST Theorem 1 item 6 hold (regime R1)". The optional note is added: "variant of A:DIST-A3 on the window 5(A+1)(s0+1) log n" (`:66`). The note is accurate. A:DIST-A3 (`assumptions.tsv:125`) is "E exp(lambda u'z) <= exp(K^2 lambda^2 Var(u'z)/2) for u with at most q_n nonzero entries". With z = x − m_n and Var(uᵀz) = uᵀΣ_nu, this is the same form, with window q_n instead of 5(A+1)(s₀+1) log n and the constant named K instead of L. |
| K2-6 [E] | **RESOLVED** | `B3w.md:106-107`: "(possible since β* is deterministic and S₀ ⊆ [p]; X⁰ and the nonzero values of θ⁰ are otherwise arbitrary, and the interface conditions need not hold for (X⁰, θ⁰))". The fallback reading is gone. |

## 2. B3w (c) against STATEMENT §2 (c); Step 6; ASSEMBLY Step 3 (task 2)

I compared the two texts clause by clause (`STATEMENT.md:73-79` against `B3w.md:34-40`).

| clause | STATEMENT §2 (c) | B3w (c) | match |
|---|---|---|---|
| completion | (X, θ̃*) on {p_ret = p}; outside it a fixed deterministic centred standardised n × p matrix with a fixed truth θ⁰, supp θ⁰ = S₀ | same, given by reference to Step 6 | yes |
| support | supp θ° = S₀ on every outcome | same | yes |
| Borel / independence | "(X°, θ°) is a Borel function of the raw design, hence independent of ε" | only "ε is independent of (X°, θ°)" | **partial: K3-1** |
| 𝒜′_n | ‖X°θ°‖² ≤ nM_E, (F_λ; φ₀), (F_w; g₀) (m♯_n from (n, p, s₀)), θ°²_min nφ₀²/log n ≥ M_n | same | yes |
| measurability, inclusion | 𝒜′_n is (X°, θ°)-measurable; 𝒜_n ⊆ 𝒜′_n ∩ {p_ret = p} | same | yes |
| item 6 | "Moreover (with (b): P(𝒜′_nᶜ) ≤ P(𝒜_nᶜ) → 0) the hypotheses … hold … in R1 with the events 𝒜′_n, common constants, common envelope" | "the hypotheses … (`:95-100`) hold … in R1 …"; the bound P(𝒜′_nᶜ) ≤ P(𝒜_nᶜ) is in the closing parenthesis, and (b) is part (b) of the same lemma | same content (the appeal to (b) is implicit; see K3-1, optional part) |

**Step 6 proves exactly (c).** It proves each clause above, the Borel clause included (`:108-110`). The support clause is
at `:111`. 𝒜′_n is anchored at S₀ = supp θ° (`:112-113`), and min_{j∈S₀}θ°_j² = θ°²_min because supp θ° = S₀. Measurability
is at `:114-116`; with the support fixed, finitely many Gram blocks and coordinates are involved. The inclusion is at
`:116-117`. R1 is at `:118-119`: s₀ ≥ 1 fixed, 2 ≤ p ≤ n^A, s₀ ≤ min(p, ⌊n/2⌋) for n ≥ 2s₀, σ*² = 1, and G. The item 6
hypotheses are closed through (b) at `:119-124`. I checked them against [W3P] `:63-75, 95-100`. The constants satisfy
0 < φ₀ ≤ ½ ≤ 1, g₀ > 0 and M_E ≥ 0. Item 6's "|supp θ*| = s₀" holds on every outcome. Its BM-∞ envelope form, with σ*² = 1,
is θ°²_min nφ₀²/log n ≥ M_n → ∞. The order of proof is not circular: (c) uses only "P(𝒜′_n) → 1 by (b)", and (b) uses only
𝒜_n ⊆ 𝒜′_n from the *Events* paragraph. Step 6 proves nothing beyond (c).

**ASSEMBLY Step 3** (`:36-43`) cites B3w (c) twice: for the completed pair "(equal to (X, θ̃*) on {p_ret = p})", and for
"supp θ° = S₀ on every outcome". Both statements are now in B3w (c), so both citations are accurate. **ASSEMBLY Step 2**
(`:31-34`) cites "B3w (b), (c)" for "(X°, θ°) is a Borel function of the raw design". That clause is in STATEMENT §2 (c) and
in B3w Step 6, but not in the B3w (c) statement block (K3-1). Only "Borel" is affected. The independence that Step 3 uses is
in B3w (c).

## 3. Retagged changelog row (task 3)

| row | tag now | verdict | reason |
|---|---|---|---|
| `STATEMENT.md:191` (1.2, §2 (c)) | "EQUAL for Theorem 2SG (…); on the companion claim B3w (c) the completion is specialised (supp θ⁰ = S₀ instead of any support of size s₀): **WEAKER in form, EQUAL in use** (ASSEMBLY needs one completion; the broader v1.1 completion is no longer claimed); 𝒜′_n drops '\|supp θ°\| = s₀', now automatic [K2-4]" | **CONFIRMED** | Theorem 2SG: the §1 text is unchanged, so EQUAL. B3w (c): the hypotheses (A1)–(A4) are unchanged. The constructed object is restricted to a subclass of the v1.1 completions. The added conclusion "supp θ° = S₀" is immediate from that restriction, because supp θ̃* = S₀ on {p_ret = p} for every v1.1 completion. So it adds no information beyond the narrowing, and WEAKER in form is the right tag, not INCOMPARABLE or STRONGER. For each admissible completion, 𝒜′_n is the same event as in v1.1, since the dropped condition holds identically. Its only consumer is ASSEMBLY Steps 2–3, which needs one completion: EQUAL in use. Each claim is tagged separately, as the K1-8 rule requires. |

The check cell of that row still reads "`reviews/K2_recheck_opus.md` (tag per K2-4)". See note N1.

## 4. REPORT §6 B3w block against STATEMENT §2 (task 4)

`REPORT.md:64-69`. The statement span is 59-79, and the premises are 23-39 and 41-57. All three are correct: STATEMENT's
line numbers did not move, because the K2 repair changed only §9. The assumption descriptions match (A3) (`:50-51`) and
(A4) (`:52-54`). The conclusion lists only parts of STATEMENT §2:
- (a): no column is constant, (E; M_E), (F_λ; φ₀² = φ²/4), (F_w; g₀ = φ²/8), and BM-∞ with envelope b_lo²nφ²/(8σ*² log n).
- (b): the probability bound.
- (c): the 𝒜′_n ⊇ 𝒜_n interface clause.

"|supp θ̃*| = s₀ ≤ K_cap" is omitted. That omission is allowed, and **nothing goes beyond STATEMENT**. The scope "n >= n1(s0, A, L)"
matches. The block writes "sigma^2" for σ*², which is the registry's convention elsewhere. Wording I accept: "events …
on which the hypotheses of … item 6 hold" follows item 6's own phrasing ("events 𝒜_n … on which … hold"), and no change
is needed. Non-ASCII "°"/"θ" in the block is acceptable: `claims.tsv` already contains 18 lines with "°" and many with "θ".

## 5. Anything else the repair diff broke (task 5)

- DEPS (recomputed, nothing written):

  | row | span | hash |
  |---|---|---|
  | S:setting | 23-39 | 9d4cd72f9d19ff89 |
  | S:Thm2SG | 41-57 | 243b77e0796f16e0 |
  | S:B3w | 59-79 | 3287fafe4da3041d |
  | S:ExSG | 81-88 | 6b83f9d40ce7fef1 |
  | S:class | 111-141 | 4da143855dff15dd |
  | S:inputs | 143-158 | 4da0091979c82106 |
  | P:B3w | 12-134 | 7156440ecd5666d2 |
  | P:Thm2SG | 21-52 | 5db2fe6b2eca4beb |
  | P:ExSG | 54-83 | 0cd0673df06dbe0e |
  | R:registry | 60-87 | 34ef8bbe5ce1b247 |

  All ten equal the `sha` column of `DEPS.tsv`. P:B3w and R:registry are UNCHECKED there. Both are verified by this
  re-check at those hashes, with the single amendment K3-1 to P:B3w. The REPORT span moved from 59-86 to 60-87 because §4
  gained a line. No file cites REPORT line numbers, so nothing else goes stale. The ASSEMBLY header edit (`:4`) is outside
  the P:Thm2SG span, whose hash is unchanged.
- REPORT §4 (`:46-47`): "(RESOLVED-WITH-AMENDMENTS; 2 S, 4 E)". This is correct: K2-1 and K2-4 are S; K2-2, K2-3, K2-5 and K2-6 are E.
- The diff broke nothing else. I checked that no other text in STATEMENT §§1–3, B3w Steps 0–5 or ASSEMBLY Step 4 was
  touched or relies on the old B3w (c) wording ('|supp θ°| = s₀' as a condition of 𝒜′_n). Step 6's parenthesis "(|supp θ°| = s₀
  holds on every outcome)" (`:113`) is consistent with the new (c).

## 6. New findings

**K3-1 (E; B3w (c) omits the Borel clause of STATEMENT §2 (c)).** `lemmas/B3w.md:36-37`. STATEMENT §2 (c) (`:75`) asserts
"(X°, θ°) is a Borel function of the raw design, hence independent of ε". B3w (c) states only "ε is independent of
(X°, θ°)". Step 6 (`:108-110`) proves the Borel clause, and ASSEMBLY Step 2 (`:31-32`) cites "B3w (b), (c)" for it. This
omission predates K2 (v1.1 had the same split) and is not mathematical, but it is the only content gap between the two
statements of (c). *Fix:* at `B3w.md:36` change "Then supp θ° = S₀ on every outcome." to "Then supp θ° = S₀ on every outcome,
and (X°, θ°) is a Borel function of the raw design, hence independent of ε." At `:37`, delete ", ε is independent of
(X°, θ°)". *Optional, same edit:* write "Moreover (with (b)) the hypotheses …" at `:37-38` to mirror STATEMENT's K1-3 wording.
Also rewrap `:37`, which is 169 characters against the file's ~125. Afterwards P:B3w must be re-hashed (wording only).

**N1 (bookkeeping; not a finding against the text).** If K3 is accepted, the check cell of `STATEMENT.md:191` can read
"`reviews/K3_recheck_opus.md`: CONFIRMED". This line is outside the spans and has no DEPS effect. Then mark P:B3w (after K3-1)
and R:registry checked with `deps_hand.py P:B3w=reviews/K3_recheck_opus.md R:registry=reviews/K3_recheck_opus.md`.

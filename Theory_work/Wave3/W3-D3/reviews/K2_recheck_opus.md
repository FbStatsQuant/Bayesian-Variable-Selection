# W3-D3 — K2 re-check of the K1 repairs (Opus 5.5, high; new agent) — 2026-11-17

**Verdict: RESOLVED-WITH-AMENDMENTS.**

Scope: `reviews/K2_brief.md`. I read `reviews/K1_linecheck_opus.md`, `reviews/K1_disposition.md`, `reviews/K1_repair.diff`,
the current `STATEMENT.md` (v1.2), `lemmas/B3w.md`, `lemmas/ASSEMBLY.md`, `REPORT.md` §6 and `DEPS.tsv`. I checked them
against these sources: [W3P] `W3-POST/STATEMENT.md:16-100`; [EB] `B0.md` (a), (e), (f); `B1.md:8-24`; `B2core.md:7-25`;
`B2.md:40-56`; `B3.md:96-104` (A-1, A-2); [R1] `R1_set_sizes.md:15-28`; [RV] `READER_VERSIONS.md:26-30, 255-276`; and
`Theory_work/INFRA/registry/claims.tsv` and `assumptions.tsv`. I did not read LOG.md or CHECKPOINT files, and I did not
change git state. I recomputed the DEPS span hashes with a copy of `deps_hand.py`'s span rule that does not write anything.
All ten (line range, sha) pairs in `DEPS.tsv` match the current files. Scratch `.rc_tmp/` has been deleted.

None of the findings below changes a hypothesis, a constant or a conclusion of Theorem 2SG. One finding (K2-1) concerns
alignment between the B3w statement and its proof file. One (K2-4) asks for clearer wording of a changelog tag. The rest are editorial.

## 1. Per-finding table (K1 → repaired text)

| K1 | verdict | check of the repaired text |
|---|---|---|
| K1-1 [C] | **RESOLVED-WITH-NEW-ISSUE** (K2-1) | The mathematics is now correct and consistent across STATEMENT §2 (c) (`:73-79`), B3w Step 6 (`B3w.md:105-117`) and ASSEMBLY Steps 2–4 (`ASSEMBLY.md:31-49`). (i) **supp θ° = S₀ on every outcome.** On {p_ret = p}, every ŝ_j > 0 and θ̃*_j = ŝ_jβ*_j/σ* ([EB] B0 (f)), so supp θ̃* = supp β* = S₀. Off that event, θ° = θ⁰ with supp θ⁰ = S₀. Such a θ⁰ exists and is deterministic because β* is deterministic and S₀ ⊆ [p]. (ii) **𝒜′_n is measurable.** With the support fixed at S₀, each condition is a finite collection of inequalities between continuous functions of (X°, θ°): ‖X°θ°‖², λ_min of the finitely many Gram blocks on S₀ ∪ J with \|J\| ≤ j₀ or \|J\| ≤ m♯_n(n, p, s₀) (deterministic), and the coordinates θ°_j for j ∈ S₀. (X°, θ°) is Borel in the raw design. (iii) **Item 6's outputs refer to S₀.** [W3P] `:31-32` sets S₀ := supp θ*, which equals S₀ here. So δ°_n = 1 − π°(S₀), and (F_λ), (F_w) in 𝒜′_n are anchored at S₀ (`ASSEMBLY.md:39-41`). (iv) **The transfer error is at most P(𝒜_nᶜ).** ASSEMBLY Step 4 adds P(p_ret ≠ p), and Step 2 bounds it by P(𝒜_nᶜ) because 𝒜_n ⊆ 𝓔₁ ⊆ {p_ret = p}. **New issue:** the *statement* block of `B3w.md` (c) (`:34-40`) still has the v1.1 wording ("a fixed truth of support size s₀", with "\|supp θ°\| = s₀" listed among the conditions defining 𝒜′_n). It does not state supp θ° = S₀. Yet ASSEMBLY Step 3 (`:39`) cites "B3w (c)" for that fact. See K2-1. |
| K1-2 [F] | **RESOLVED** | `B3w.md:46` and `:50` now read K⁴ inside the quotation marks, verbatim with `B1.md:13` and `B2core.md:15`, and `:51-52` add "read with K := L". |
| K1-3 [S] | **RESOLVED** | `STATEMENT.md:77-79`: "Moreover (with (b): P(𝒜′_nᶜ) ≤ P(𝒜_nᶜ) → 0) … in regime R1 with the events 𝒜′_n …". The appeal to (b) and to R1 is now explicit, and the parenthetical inference follows from 𝒜_n ⊆ 𝒜′_n (`:77`) together with (b). The R1 check itself is in B3w Step 6 (`:118-122`). |
| K1-4 [E] | **RESOLVED** | `B3w.md:66-67`: "\|S₀ ∪ J\| is an integer ≤ W̄_n, hence \|S₀ ∪ J\| ≤ ⌊W̄_n⌋ = q_n". |
| K1-5 [E] | **RESOLVED** | `B3w.md:3` now says "(v1.2)", and `ASSEMBLY.md:23` says "Fix n ≥ 3". (Separately, ASSEMBLY's own header still names v1.1; see K2-2.) |
| K1-6 [E] | **RESOLVED** | `B3w.md:112-116`: the support is fixed at S₀, and the measurability wording is now accurate. |
| K1-7 [E] | **RESOLVED** | `STATEMENT.md:190` adds the row as proposed. The tag is confirmed in §3 below. |
| K1-8 [S] | **RESOLVED** | `STATEMENT.md:185` now reads "STRONGER on the companion claim B3w (added conclusion (c) …); EQUAL for Theorem 2SG". Confirmed. |
| K1-9 [E] | **RESOLVED** | `STATEMENT.md:131-132`. The note is true: Corr(z₁, z₂) = E B = 1 − 2ε → 1, so the 2 × 2 block has λ_min = 2ε → 0, which is below any fixed φ² once ε < φ²/2. \|S\| = 2 ≤ W̄_n. |
| K1-10 [E] | **RESOLVED** | `STATEMENT.md:50-51` now matches [RV] `:268-269` verbatim, including "(for instance, λ_min(Σ_n) ≥ φ²)". §5 `:113` notes the restoration. |
| K1-11 [E] | **RESOLVED** | The span sentence is gone from §2. It now appears as §4 (f) (`STATEMENT.md:108-109`), outside the spans, and is true as stated. |
| K1-12 [E] | **RESOLVED** | `STATEMENT.md:139-140`: "'qualify' means 'satisfy (A4)'; Theorem 2SG also needs (A3)". |

## 2. Findings

**K2-1 (S, minor; the B3w statement block does not match its proof).** In `lemmas/B3w.md:34-40`, statement (c) still
describes the completion as "a fixed deterministic centred standardised n × p matrix with a fixed truth of support size s₀".
It also lists "|supp θ°| = s₀" and "θ°²_min" among the conditions defining 𝒜′_n. Since K1-1, Step 6 (`:105-117`) fixes
supp θ⁰ = S₀ and proves the v1.2 statement, including "supp θ° = S₀ on every outcome" (`STATEMENT.md:74-75`). Step 6's
measurability argument now relies on that fixed support. This leaves three mismatches. (i) The file's own (c) no longer
matches the target it names (`:3`, v1.2). (ii) If (c) is read universally ("any truth of support size s₀"), Step 6 no
longer proves it: K1-6's finite-union argument was removed, although the claim remains true. (iii) ASSEMBLY Step 3
(`ASSEMBLY.md:39-40`) cites "B3w (c)" for supp θ° = S₀, which only Step 6 states. *Fix:* replace `B3w.md:34-36` with the
v1.2 wording of STATEMENT §2 (c): "(… on {p_ret = p}; outside it a fixed deterministic centred standardised n × p matrix
with a fixed truth θ⁰ with supp θ⁰ = S₀). Then supp θ° = S₀ on every outcome. Let 𝒜′_n be the set of outcomes on which
(X°, θ°) satisfies ‖X°θ°‖² ≤ nM_E, (F_λ; φ₀), (F_w; g₀) (m♯_n computed from (n, p, s₀)) and θ°²_min nφ₀²/log n ≥ M_n."
Keep the rest of (c). If you prefer to leave B3w (c) unchanged, change the citation at `ASSEMBLY.md:39` to "(B3w Step 6;
`STATEMENT.md` §2 (c))" instead. The first fix is better.

**K2-2 (E).** The header at `lemmas/ASSEMBLY.md:3-4` still says "Targets: `STATEMENT.md` §1 … and §3 …, v1.1". The
statement is now v1.2: §1 (A3) gained the restored parenthetical, and the B3w (c) consumed in Step 3 changed. *Fix:* "v1.2".
(This line is outside the P:Thm2SG span, so it has no effect on DEPS.)

**K2-3 (E).** At `lemmas/B3w.md:74`, "(A4) with u = e_j … is (SG₁) of B1 **with the same K**" predates [L1-1]. In this
file K is not the sub-Gaussian constant. *Fix:* "… is (SG₁) of B1 with K := L". The next sentence already says this for
B2-core.

**K2-4 (S, tag wording; statement-change table).** Changelog row 1.2 §2 (c) (`STATEMENT.md:191`) is tagged EQUAL. That is
correct for Theorem 2SG, whose §1 text did not change and whose proof is now consistent. For the companion claim B3w (c),
however, v1.2 does not say the same thing as v1.1. The v1.1 completion allowed "a fixed truth supported on a set of size
s₀", and v1.1's B3w Step 6 said "(any choice …)". v1.2 fixes supp θ⁰ = S₀. Read universally, (c) therefore now asserts
its conclusions for a narrower class of completions, which is WEAKER in form. The added identity supp θ° = S₀ follows
immediately from the choice. In use the change is EQUAL: the only consumer, ASSEMBLY Step 3, needs one admissible
completion, and v1.1's broader version, though true by the K1-1 finite-union argument, was never consumed or registered.
The reason cell ("the v1.1 conclusion with an arbitrary θ⁰ was stated for supp θ° …") describes the problem K1-1 found
but does not record the narrowing. *Fix:* tag cell "EQUAL for Theorem 2SG; on the companion claim B3w (c) the completion
is specialised (supp θ⁰ = S₀ instead of any support of size s₀): WEAKER in form, EQUAL in use (ASSEMBLY needs one
completion; the broader v1.1 completion is no longer claimed); 𝒜′_n drops '|supp θ°| = s₀', now automatic". The same
rule as K1-8 applies: tag each claim separately.

**K2-5 (E; REPORT §6).** There are two small notation points in the W3-D3:B3w block (`REPORT.md:66`). (i) The block
writes "(F_lambda; phi^2/4), (F_w; phi^2/8)". STATEMENT's parameter for (F_λ) is φ₀, with floor φ₀² = φ²/4, whereas the
parameter for (F_w) is the floor g₀ itself. Read in STATEMENT's convention, "(F_lambda; phi^2/4)" would mean φ₀ = φ²/4.
That reading is weaker than what is proved, not stronger, so nothing beyond STATEMENT is claimed, but the two are
inconsistent. *Fix:* "(F_lambda; phi0^2 = phi^2/4), (F_w; g0 = phi^2/8)". (ii) "completed-pair (X, theta)-measurable
events" should read "(X°, θ°)-measurable events A'_n ⊇ A_n on which the hypotheses of W3-POST Theorem 1 item 6 hold
(regime R1)". This is what STATEMENT §2 (c) asserts. *Optional:* the new id A:SUBG-SPARSE-ROWS is a variant of the
registered A:DIST-A3 (`assumptions.tsv`: the same sub-Gaussian condition on the window q_n, with constant K). A note
"variant of A:DIST-A3 on the window 5(A+1)(s0+1) log n" would help the registry's assumption map.

**K2-6 (E, optional).** At `lemmas/B3w.md:106-107`, "(possible: β* is deterministic and |S₀| = s₀ ≤ p; otherwise any
choice — the interface conditions need not hold for it)" can be misread: "otherwise" sounds like a fallback for when the
choice is impossible, but it never is. *Fix:* "(possible since β* is deterministic and S₀ ⊆ [p]; X⁰ and the nonzero
values of θ⁰ are otherwise arbitrary, and the interface conditions need not hold for (X⁰, θ⁰))".

## 3. Statement-change table (v1.1 → v1.2, and the retagged v1.1 rows)

| row (`STATEMENT.md`) | tag claimed | verdict | reason |
|---|---|---|---|
| :185 (1.1, §2 interface / completed pair / part (c); retagged per K1-8) | STRONGER on B3w; EQUAL for Theorem 2SG | **CONFIRMED** | (c) is an added conclusion of B3w relative to v1.0's (i)–(vi). §1 is unchanged, and the interface is the one B3 Step 6 / A-2 already used. |
| :190 (1.1, §2 bookkeeping; §4 (a), (b), (d); §6; §7; §8; K1-7) | EQUAL | **CONFIRMED** | 𝓔₂(q_n) = 𝓔₂(w_n) as events in ℝ^p (`B3w.md:22-23`). m♯_n with p_ret equals m♯_n with p on 𝒜_n. n₁ ≥ max(3, 2s₀) is a threshold, not a hypothesis. θ̃* is a renaming. The rest lies outside the spans, and the consumed scope narrowed from items 1–4 to items 1–3. |
| :191 (1.2, §2 (c): supp θ⁰ = S₀; "and so" → appeal to (b) and R1; remark → §4 (f)) | EQUAL | **CONFIRMED for Theorem 2SG; CONTESTED (wording) for B3w (c)** | See K2-4: for B3w (c) it is WEAKER in form (narrowed completion) and EQUAL in use. The "Moreover" rewording and moving the remark out are EQUAL. |
| :192 (1.2, §1 (A3) parenthetical restored) | EQUAL | **CONFIRMED** | It is an example: λ_min(Σ_{n,S}) ≥ λ_min(Σ_n) by interlacing. It is now verbatim with [RV] `:268-269`. |
| :193 (1.2, §5, §6 outside spans) | EQUAL (outside spans) | **CONFIRMED** | §6's B3 status now matches `claims.tsv` exactly, and the §5 notes are true (K1-9, K1-12 above). |
| (coverage) | — | **complete** | Every v1.2 change in the diff (header `:1, 9-10`, §1 `:51`, §2 (c), §4 (f), §5 `:113, 129-132, 139-140`, §6 `:151-154`, §9) has a row, or is an editorial header line. |

## 4. Interpretive sentences newly introduced inside the claimed spans (§§1–3)

| `STATEMENT.md` line | sentence | verdict |
|---|---|---|
| :51 | "(for instance, λ_min(Σ_n) ≥ φ²)" | **checked**: by interlacing it implies (A3), and it is verbatim from [RV]. |
| :74-75 | "Then supp θ° = S₀ on every outcome" | **checked**: ŝ_j > 0 on {p_ret = p} gives supp θ̃* = S₀, and off that event it holds by the choice of θ⁰. This is a stated conclusion, proved in B3w Step 6 `:111`. |
| :77-78 | "Moreover (with (b): P(𝒜′_nᶜ) ≤ P(𝒜_nᶜ) → 0) the hypotheses of [W3P] Theorem 1 item 6 hold …" | **checked**: the bound follows from 𝒜_n ⊆ 𝒜′_n plus (b), and the R1 check is in B3w Step 6 `:118-122`. |
| :75 | "(X°, θ°) is a Borel function of the raw design, hence independent of ε" | carried over from v1.1, not new; **checked** again by ε ⫫ X^r ((S1)). |

§1 contains no other new interpretive sentence, and §3 is unchanged.

## 5. DEPS rows re-checked

| DEPS row | span | verdict | notes |
|---|---|---|---|
| S:Thm2SG | `STATEMENT.md:41-57` | **VERIFIED** | (A1)–(A3) and the conclusions match [RV] `:263-275` verbatim, with the Gaussian row law replaced by "mean m_n, covariance Σ_n a correlation matrix" plus (A4). |
| S:B3w | `STATEMENT.md:59-79` | **VERIFIED** | (a) and (b) are unchanged from K1. (c) as repaired is correct and is proved by B3w Step 6 (item 6's hypotheses checked against [W3P] `:63-75, 95-100`: \|supp θ°\| = s₀; (E), (F_λ), (F_w) with fixed 0 < φ₀ ≤ ½ ≤ 1, g₀ > 0, M_E ≥ 0; BM-∞ with envelope M_n → ∞, σ*² = 1; R1 with K = min(p, ⌊n/2⌋) ≥ s₀ for n ≥ 2s₀; G; independence). |
| S:class | `STATEMENT.md:111-141` | **VERIFIED** (mathematical relations) | NH14 ⊂ (A4) at Σ = I (centred rows, L a fixed multiple of their ψ₂ constant). (A4) at e_j ⇒ Condition 1 for every r. The converse fails, and the example also violates (A3) (true; see K1-9). The 2b sentence is true for (A4) via ExSG (a), (b) (interval [−K, K] of length 2K ⇒ L = K). "(A1)–(A3) verbatim" is now literally true. |
| S:inputs | `STATEMENT.md:143-158` | **VERIFIED** | Every quoted status equals `claims.tsv` (both at main 029bb748 and in the worktree; checked by hash) for W3-POST:Thm-1@1.0.1, W3-DIST:B0/B1/B2core/B2@1.0.1, W3-DIST:B3@1.0.1 (now quoted in full) and W3-READER:R1@1.0.2. The line ranges match the registry: [W3P] 61-100; [DIST] 385-390/391-395/396-399/400-408, written as `:385-408`; 409-414. [R1] B1.2 `:15-17` and B1.3 `:19-31` are correct. |
| P:B3w | `lemmas/B3w.md:12-134` | **VERIFIED-WITH-AMENDMENTS** | K2-1 (statement (c) is stale against Step 6 and the target), K2-3, K2-6. Steps 0–6 and (b) are re-read in full and correct. The repaired Step 6 is verified (see the K1-1 row above). |
| P:Thm2SG | `lemmas/ASSEMBLY.md:21-52` | **VERIFIED-WITH-AMENDMENTS** | Steps 1–4 and the constants are correct. Step 3's new sentence (`:39-41`) is correct, but its citation "B3w (c)" should point to a statement that contains supp θ° = S₀ (K2-1). |
| R:registry | `REPORT.md:59-86` | **VERIFIED-WITH-AMENDMENTS** | Statement and premise ranges are correct: B3w 59-79 with premises 23-39 and 41-57; ExSG 81-88 with 23-39; Thm2SG 41-57 with 23-39. The new assumptions point at 41-57, where (A3) is `:50-51` and (A4) is `:52-54`. The assumption statements match (A3) and (A4). The Thm2SG conclusion and scope match §1; depends_on matches §7; notes cite [RV] `:263-275` correctly. No block claims more than STATEMENT. The B3w block needs the K2-5 wording fixes. A:COEF-BOUNDED is used here with the raw-scale reading, as in its source `W2-APP/lemmas/L1_POST.md:11-13`, so that use is accepted. |

DEPS span hashes recomputed without writing: S:Thm2SG 243b77e0796f16e0, S:B3w 3287fafe4da3041d, S:class 4da143855dff15dd,
S:inputs 4da0091979c82106, P:B3w 05df235f65064abb, P:Thm2SG 5db2fe6b2eca4beb, R:registry 5171aab785a78444. All equal
`DEPS.tsv`. The K1-checked rows S:setting, S:ExSG and P:ExSG are unchanged (their shas equal checked_sha). After the
K2-1, K2-3 and K2-5 edits, P:B3w and R:registry (and P:Thm2SG, if you take the alternative K2-1 fix) will need re-hashing.
These are wording-only edits.

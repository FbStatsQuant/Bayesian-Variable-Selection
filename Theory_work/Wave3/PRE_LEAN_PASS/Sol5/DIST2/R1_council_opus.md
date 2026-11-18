# R1 council review (Opus seat): W3-DIST:DIST-2 delta (T5-R1, changelog 1.4.11 WEAKER)

**Finding kinds held:** WORDING and QUALIFIER only. There is no GENUINE GAP: every step and constant I recomputed holds.

**Manifest verify:** I built a scratch git repo at `.rc_tmp/opus_dist2_verify/` with the 4 EXT files copied from the clone at 330b87b4, plus `Sol5/DIST2/ticket/` at the same relative path. Then `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/PRE_LEAN_PASS/Sol5/DIST2/ticket MANIFEST_DIST2.txt` printed `verify: OK MANIFEST a230f90922614d35a913e46c26e3cfb1c1d376017d8491e2f912b06cc7a9cb67`, exit 0. The ticket's `STATEMENT.md` (500 lines) and `TARGET.md` (214 lines) are byte-identical (`cmp`) to the batch-tree copies.

**Registry pin (batch tree):** `claims.tsv:485` W3-DIST:DIST-2 is now at version 1.0.3 (it was 1.0.2 at HEAD~1) with sha256 `7de66dbc…`. I recomputed `claim_hash` (span 93-98 plus premises span 17-70) on the batch tree and it matches. The status text is unchanged.

**Hygiene:** I changed no tracked file in either tree, committed nothing and started no subagents. Scratch was used only under `.rc_tmp/` (git-ignored).

## 1. Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1a | ACCEPT | `STATEMENT.md:96-97`: "for fixed s₀^r: ε_n² ≍ log n·ℓ_n/n". In D.6 (`DIST12.md:84-90`) the smallest admissible level t = M₀′ log n gives squared radius C₂²M₀′·log n·ℓ_n/n. For fixed (s₀^r, A, σ*², M, M′) this is exactly of order log n·ℓ_n/n, so ≍ is right as a description of the display's best radius. It is stated as "Best rate" of (1.2), not as a lower bound on contraction (no lower bound is proved, and the text claims none). "One logarithm slower than DIST-1": ℓ_n ∈ [log n, A log n + …] under p_raw ≤ n^A, so ℓ_n ≍_A log n. Correct. |
| 1b | ACCEPT | Cubic upper bound, recomputed. C_m = 2s + 1 + (s(A+2)+5)/log 2 is linear in s (`X.md:34`). From it, C_P′ = C_A′C_m + 4, C_x′ = C_m(A+2) + 2, Λ′ = max{32C_x′, 8C_P′, 8B/σ², 48/log 2}, C_Q′, C_v′, C₁′ and C_{X′} = max{C₁′, C_v′} are all ≲_{A,σ²,M,M′} (1+s) (`X.md:202-216`). C_T′ = 4[(A+7)(s+1+C_m)+8] ≲ (1+s) (`DIST12.md:36`). So C₂² = C_{X′}² + 1 + C_{X′}/2 + C_T′ ≲ (1+s)² (`DIST12.md:88`). M₀′ = max{16, (A+1)s} ≲ (1+s) (`X.md:217`). The product is ≲ (1+s)³. **A** enters polynomially (C_x′ ~ A²s, so roughly A⁵s³ overall); the sentence holds A fixed, so this is fine. **κ₀** enters only n₀′ (conditions (f′), √(t/n)·log n ≤ 1, Λ′t log n ≤ 8n at t = n^{1−κ₀}; `X.md:218-221`), never C₂ or M₀′. **c_D** does not enter. s = 0 is covered (every constant is positive at s = 0). |
| 1c | ACCEPT | "An upper bound, not known to be tight" is true, and it is not an unproved claim: no lower bound in s is asserted. See observation O-1 below: the proof even gives (1+s)² cheaply, which supports "not known to be tight". |
| 2 | ACCEPT (with E1, E2, E3) | **WEAKER is the right tag.** The old sentence asserted a squared radius ≍ (1+s₀^r) log n·ℓ_n/n. The new one asserts order log n·ℓ_n/n for fixed s₀^r and a cubic upper bound on the constant. The old literal claim implies the new one ((1+s) ≤ (1+s)³), so the new text claims less. Displays (1.1) and (1.2) are unchanged (diff HEAD~1..HEAD of the batch tree). TC6 (`TARGET.md:58`) fixes only the display, radius and hypotheses, so no target clause moves and no early checkpoint is triggered. DIST-1 (c) is a separate sentence (`:84-87`, row 1.4.10) and is untouched by this patch. **Proof places:** `X.md` §9 and `DIST12.md` D.6 are correct; the linear-in-s constant C_m lives in `X.md` §0 (:34), see E3. **Position:** the row is at `:497`, the last row of the table, before the closing paragraph `:498-500`. The highest registered span is B3 409-414 and the highest premises span is 381-382, so the +1 line shifts no span. Line count went 499 → 500, as `BATCH_READY_v2.md:8` says. |
| 3 | ACCEPT | **Grep, staged tree:** no other sentence makes DIST-2's rate or constant linear in (1+s₀^r). `STATEMENT.md:84-86` is DIST-1 (c) (correct: C_X and C_T are free of s). `TARGET.md:12` "M₀ ∝ (1 + s₀^r)(A + 1)" is DIST-1's M₀ and TC3, not DIST-2's radius. `STATEMENT.md:200-202` (Thm A "without (A4)") and `:266` (C₁, the size clause) state no sparsity order for the radius. **Reader:** `CLAIMS_CARD.md:63` row 2.1 gives no s-order for the "without collinearity" radius. `READER_VERSIONS.md:1195-1197` (display (i): radius constant free of s, M₀ at most linear) is DIST-1. `READER_VERSIONS.md:1208-1211` and B9.8 (`:1256`) already say cubic, "as proved … an upper bound". **Wider sweep** of `Theory_work` (excluding reviews and PRE_LEAN_PASS): the only other hits are historical log or decision entries (`Dept/LOG.md:231,235`, `Dept/QUEUE.md:96`, `HQ_DECISIONS.md:599,606`, `W3-DIST/CHECKPOINT_3.md:87`) that quote the old sentence as the defect. Nothing is left to fix. |
| 4 | ACCEPT (with F1, E1) | **No stale cross-reference.** `lemmas/X.md` §9 (:197, constants at :216) and `lemmas/DIST12.md` D.6 (:83) exist at those relative paths from both W3-DIST files, and "TARGET.md §2" at `:98` is still the parity table. **No contradiction with DIST-1 (c):** DIST-1's constants use d_t with C_d = 34, free of s; DIST-2's use m_n(t) with C_m ~ s. **No contradiction with Thm A or B at reader level:** the reader already says cubic. **One mismatch between `STATEMENT.md:97` and `TARGET.md:30`:** the TARGET cell drops "for fixed (A, σ*², M, M′)" and "not known to be tight" (F1). **One repair-introduced inconsistency:** the header `STATEMENT.md:1` still reads "v1.4.10, 2026-11-16" although the changelog now ends at 1.4.11 (E1). |
| 5 | — | Every finding is classified below. |

## 2. Findings

**F1 (QUALIFIER, apply as written): `TARGET.md:30`, P3 rate row, DIST-2 cell.**
- **Problem:** the cubic bound is printed without the fixed-(A, σ*², M, M′) qualifier that `STATEMENT.md:97` carries and that the DIST-1 entry of the same cell carries. Without it the cell reads as uniform in A, and the proved constant grows polynomially in A (C_x′ = C_m(A+2) + 2 with C_m ∝ sA).
- **Replace:** `DIST-2: log n·ℓ_n/n for fixed s₀^r (constant at most of order (1 + s₀^r)³ as proved, an upper bound; `lemmas/X.md` §9, `lemmas/DIST12.md` D.6)`
- **With:** `DIST-2: log n·ℓ_n/n for fixed s₀^r (as proved, constant at most of order (1 + s₀^r)³ for fixed (A, σ*², M, M′), an upper bound not known to be tight; `lemmas/X.md` §9, `lemmas/DIST12.md` D.6)`
- `TARGET.md` is in no registered span, so this needs no rehash.

**E1 (WORDING, apply as written): `STATEMENT.md:1`, header version.**
- **Problem:** row 1.4.10 bumped the header to v1.4.10; row 1.4.11 did not bump it.
- **Replace:** `(v1.4.10, 2026-11-16;` **with:** `(v1.4.11, 2026-11-18;`
- Line 1 is in no span and no premises span, so this needs no rehash.

**E2 (WORDING, apply as written): `STATEMENT.md:497`, row 1.4.11, "change" column.**
- **Problem:** the text in quotation marks is not verbatim from either `:97` or `TARGET.md:30`.
- **Replace:** `with the constant "at most of order (1 + s₀^r)³ as proved (an upper bound, not known to be tight)"`
- **With:** `with "As proved, its constant is at most of order (1 + s₀^r)³ for fixed (A, σ*², M, M′) (an upper bound, not known to be tight; …)"`

**E3 (WORDING, apply as written): `STATEMENT.md:497`, row 1.4.11, tag and reason columns.**
- **Problem 1:** DIST-1's linear claim needs both C_X and C_T to be free of s, because C = (C_X² + C_X/2 + 1 + C_T)^{1/2} (`DIST12.md:56,67-68`).
- **Replace:** `DIST-1's own linear claim (c) is unaffected because C_X does not depend on s`
- **With:** `DIST-1's own linear claim (c) is unaffected because its radius constant C = (C_X² + C_X/2 + 1 + C_T)^{1/2} does not depend on s (`lemmas/X.md` §0, `lemmas/DIST12.md` D.1, D.4)`
- **Problem 2:** the s-linear constant behind the cubic count is defined in §0, not §9.
- **Replace:** `the proof constants (`lemmas/X.md` §9, `lemmas/DIST12.md` D.6) give (1 + s₀^r)³`
- **With:** `the proof constants (`lemmas/X.md` §0 (C_m) and §9, `lemmas/DIST12.md` D.1 (C_T′) and D.6) give only an upper bound of order (1 + s₀^r)³`
- The row is outside every span, so this needs no rehash.

## Observations (not findings; no change requested)

- **O-1 (supports "not known to be tight"):** in D.6 the squared term C_{X′}² multiplies t/n, not tℓ_n/n. Since n₀′ already depends on s, one may take n ≥ exp(C_{X′}²), so that C_{X′}²t/n ≤ tℓ_n/n. Then C₂² ≲ (1+s) and the constant is ≲ (1+s)². The cubic statement stays true as an upper bound. This is a possible sharpening for the sharpness review (`UNHARVESTED_STRENGTH` item 9), not a defect.
- **O-2 (tag under the other reading):** HQ's earlier RT1 ruling (`HQ_DECISIONS.md:606`, "LOOSE, in span") read the old sentence under the fixed-s convention of §0. Under that reading the first clause is EQUAL, and the added "as proved" sentence is a true descriptive addition. Under the literal reading the change is WEAKER. WEAKER is the conservative tag and is what the row records. No target clause is affected under either reading.
- **O-3 (outside this delta, for HQ):** the same batch edits `STATEMENT.md:78` (T5-R2, DIST-1 span) and `:152` (T5-R4, Thm-A premises span). Neither has a changelog row. Earlier EQUAL editorial edits did get rows (1.3.1, 1.4.4), so a 1.4.12 row for these two may be wanted. This does not affect DIST-2.

## 3. Gates

- **G1 correctness: PASS.** The ≍ order, the cubic upper bound (with its dependence on A, κ₀ and c_D) and the "not known to be tight" clause were all recomputed from `X.md` §0 and §9 and `DIST12.md` D.1 and D.6, and all hold.
- **G3 faithfulness and scope: PASS.** The new sentence claims no more than D.6 proves and adds no lower-bound claim. Displays and TC1–TC9 are unchanged. The one scope mismatch, F1, is in `TARGET.md`, is QUALIFIER-level and is to be applied as written.
- **G4 statuses and pins: PASS.** The DIST-2 row was re-pointed to 1.0.3, and its hash matches my recomputation. The status text is unchanged. The row's check column names the Fable card ruling and claims no diff-round confirmation it does not have. The header version is stale (E1, WORDING).
- **G5 registration form: PASS.** Row 1.4.11 is at the foot (:497), after every registered span (max 409-414) and every premises span (max 381-382), with no shift and line counts 500/214. The WEAKER tag is right, and the reason and proof places are correct up to E2 and E3.

gates=PASS: only WORDING and QUALIFIER findings, all to be applied as written.

## 4. Score

**9.3.** The repair is mathematically correct and suitably conservative. The deductions are for the dropped qualifier in TARGET.md:30 (F1), the stale header version (E1) and two imprecisions in the changelog row (E2, E3).

COUNCIL-VERDICT round=R1 manifest=a230f90922614d35a913e46c26e3cfb1c1d376017d8491e2f912b06cc7a9cb67 seat=opus score=9.3 gates=PASS

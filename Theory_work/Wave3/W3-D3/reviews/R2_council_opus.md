# W3-D3 — council diff round R2, seat `opus` (Claude Opus 5.5, high; fresh agent)

Manifest reviewed: `MANIFEST f559960469015b9c993e17cc82b3955ceee2890db189b8ae23e2aa2f1f4840a6`.
`Theory_work/Wave3/tools/manifest.py verify` on the worktree gives "verify: OK" for this digest. `git status` is clean.

**Files changed since R1** (MANIFEST_R1 vs MANIFEST_R2): DEPS.tsv, PLAN.md, READER_DELTA.md, REPORT.md, STATEMENT.md,
TARGET.md, citecheck.py, lemmas/ASSEMBLY.md, lemmas/B3w.md, numerics/N2_subgauss_rows.py. The external inputs, N1_*,
N2_out.txt, API_CARD.md, api_request_build.py and deps_hand.py are unchanged.

**What I read.** The brief; both R1 reviews; `reviews/R2_diff_since_R1.txt` in full; STATEMENT.md v1.3 in full;
lemmas/B3w.md in full; lemmas/ASSEMBLY.md (Proposition ExSG and its context); REPORT.md, READER_DELTA.md and TARGET.md
in full; PLAN.md :28-56; deps_hand.py; DEPS.tsv; N2 :1-8 and :80-100; N1 :1-8.
To check E1 I also read `reviews/K1_linecheck_opus.md` :73, :130-144. I did not read LOG.md, CHECKPOINT files or
disposition files.

**What I ran.**
- I recomputed all 10 DEPS span hashes in memory with deps_hand.py's rule. Every `sha` and line range in DEPS.tsv
  reproduces.
- I re-ran citecheck.py from a temporary copy that wrote to `.rc_tmp/`. The output is byte-identical to
  `reviews/CITECHECK.txt` (70 checks, 0 failures). `.rc_tmp/` was deleted afterwards. No other file was written, and git
  state is unchanged.

## (a) R1 findings

| finding | verdict | reason |
|---|---|---|
| Sol S1 (centring qualifier: REPORT :35-36, :23-24; READER_DELTA :34-35) | **RESOLVED** | Each sentence now carries the qualifier. REPORT :23-24 says "for the centred predictors z = x − m_n, implies"; the card at REPORT :37-38 says "for the centred predictors x − m_n it implies"; READER_DELTA :35 says "[for the centred predictors z = x − m_n]". The other sentences of the same kind were fixed too: TARGET :21 (formerly "weaker than (A4)") and PLAN :44. Sol's counterexample with mean (n, n) no longer contradicts any sentence. |
| Opus S1 (i) (the card's "each sub-Gaussian" had no common constant) | **RESOLVED** | REPORT :34-36 now reads "independent mean-zero, unit-variance features that are sub-Gaussian with one common constant L, for instance features confined to K standard deviations of their mean with one common K, giving L = K". This is exactly ExSG (a) plus (b) (STATEMENT :86-90). Mean zero and unit variance with \|ξ_k\| ≤ K give an interval of length 2K, hence L = K. The Bernoulli(p_n → 0) counterexample is excluded, because no common L exists for it. |
| Opus S1 (ii) (NH14 sentence without centring; Song–Liang sentence without centring) | **RESOLVED** | REPORT :36-37 reads "For centred rows this contains the isotropic sub-Gaussian rows of NH14, the case Σ_n = I"; the Song–Liang sentence is fixed as in Sol S1. The card leaves out STATEMENT §5's further bracket "L a fixed multiple of their sub-Gaussian constant". This is not a defect: the card's (A4) already demands "a fixed L", NH14's ψ₂ constant is fixed, and for centred rows the ψ₂ ⇔ MGF equivalence gives L = Cα. My R1 fix asked only for the centring. |
| Opus E1 (stale check cell, STATEMENT :188) | **RESOLVED** | The cell (now :190) reads "`reviews/K1_linecheck_opus.md`: CONFIRMED (STRONGER on ExSG)". K1 :138 and :144 do confirm STRONGER on ExSG. |
| Opus E2 (TARGET :9 "proposed") | **RESOLVED** | Now "1 (HQ ruling D114; …)", which agrees with STATEMENT §5 :113. |
| Opus E3 (TARGET :14 numerics description; K for L in the N2 docstring) | **RESOLVED** | TARGET :14 now says "AR(0.5) mixtures of independent Rademacher or uniform features", which matches N2 :84-98 (Σ_jk = 0.5^\|j−k\|, Cholesky mixing of i.i.d. ξ). The N2 docstring now says L = 1. The change is docstring-only, and N2_out.txt is unchanged. |
| Opus E4 (ExSG (b), common K) | **RESOLVED** | STATEMENT :89-90 and ASSEMBLY :59-60 now read "every ξ_k … the same K for all k". The proof of (b) (ASSEMBLY :73-81) works coordinate by coordinate, so it gives exactly this. |
| Opus E5 (𝒜′_n undefined for n < n₁) | **RESOLVED** | STATEMENT :79-80 and B3w :40 now say "For n < n₁ put 𝒜′_n := ∅; item 6 needs only P(𝒜′_n) → 1". The events are now defined for every n. Item 6's hypotheses hold vacuously on ∅, and P(𝒜′_n) → 1 still follows from (b). |
| Opus E6 (citecheck docstring §5 → §6) | **RESOLVED** | citecheck.py :8 now says §6. The change is docstring-only, and the citecheck output is reproduced (above). |

## (b) New C, S or F findings introduced by the diff

**None.**

**Claim span STATEMENT §1 is unchanged.** S:Thm2SG (STATEMENT :41-57) has sha 243b77e0796f16e0, equal to its checked
sha, and the diff has no hunk in :41-57.

**The 1.3 changelog rows (STATEMENT :196-198).**

| row | lead's tag | my verdict |
|---|---|---|
| §3 ExSG (b), "every ξ_k … the same K > 0 for all k" | EQUAL | **CONFIRMED.** In v1.2, (b) asserted "the scalar hypothesis of (a)", which is a statement about every k with one constant. The only well-formed reading of "holds with L = K" was therefore a common K. The proof is unchanged and per coordinate. Neither the conclusion nor its use (2b sentence, card, registry :79) changes. |
| §2 (c), "for n < n₁ put 𝒜′_n := ∅" | EQUAL | **CONFIRMED.** Every assertion for n ≥ n₁ is word-for-word unchanged. The sentence only completes the definition of the event sequence that item 6 consumes, and no conclusion is strengthened or weakened. |
| §9 check cell of the ExSG (b) row | EQUAL | **CONFIRMED** (bookkeeping only; it names the K1 file that confirms the tag). |

**The STALE DEPS rows, each re-checked in full.**
- **S:B3w (STATEMENT :59-80).** This is the v1.2 text plus the E5 sentence. I compared it with B3w :12-40, and the
  objects, constants (M_E, φ₀², g₀, M_n, c₁, c₂), n₁ ≥ max(3, 2s₀), (a)(i)–(v), (b) and (c) all agree. B3w's statement
  is slightly stronger (p ≥ 2, φ₀ ≤ ½, the 5n^A bound, ε ⟂ (X°, θ°) restated), as at R1. The proof (B3w Steps 0–6) is
  unchanged and still covers every item, including the new n < n₁ convention.
- **S:ExSG (STATEMENT :82-90).** This is the v1.2 text with the E4 wording. ASSEMBLY's *Claim* (:56-60) is a faithful
  copy, with "every ξ_k … the same K for all k" on both sides.
- **P:B3w (B3w :12-134).** The only change is the parenthetical at :40. Nothing else in Steps 0–6 or the Remarks
  changed, and no step refers to n < n₁.
- **P:ExSG (ASSEMBLY :54-83).** The only change is the claim wording at :59-60. The proofs of (a) and (b), including
  Hoeffding's lemma proved in place, are unchanged and give the stated claim.
- **R:registry (REPORT :64-91).**
  - The statement spans are updated: B3w → STATEMENT.md:59-80 and ExSG → :82-90. Both match the current section
    boundaries (header line to last non-blank line, the same convention as :41-57 and :23-39).
  - The premises (:23-39, :41-57) are unchanged and correct.
  - The status lines quote B3w.md:3 and ASSEMBLY.md:3 verbatim: "PROVED (by this seat, unchecked)".
  - The conclusion lines match STATEMENT. The ExSG line, "independent mean-zero unit-variance L-sub-Gaussian
    coordinates … L = K for coordinates in an interval of length 2K", uses one L and one K. It therefore agrees with the
    E4 wording.
  - depends_on and the scope fields are unchanged and still correct.
- **Line shifts.** STATEMENT gained two lines after :79 and REPORT gained two after :36. The only line citations into
  ticket files are the registry spans (correct), DEPS (correct) and N1 :5's `W3-POST/STATEMENT.md:36-37` (external,
  unchanged). citecheck reproduces with 0 failures.

**Sweep of the whole frozen ticket for the Song–Liang implication, the NH14 relation and the feature-mixture
examples.** I grepped every manifest file for Song, Liang, Condition 1, Narisetty, NH14, mixture, bounded, Rademacher,
uniform, Hoeffding, "standard deviation", isotropic and L = K. Each hit is listed below.
- *Song–Liang.* These places carry the centring qualifier: STATEMENT :119, :130; REPORT :23-24, :37-38;
  READER_DELTA :35; TARGET :21; PLAN :44.
  Three further places compare the conditions only by reference:
  - STATEMENT :137 "Song–Liang's weaker Condition 1": within STATEMENT §5, which itself sets the z = x − m_n reading at
    :119 and :130.
  - TARGET :9 "between NH14 Lemma 6.1 and SL Condition 1 (… STATEMENT §5)": a class-column pointer to §5.
  - PLAN :45, :50 "weaker condition": a planning paragraph that summarises the qualified :44 two to six lines above. It is
    not reader-facing and not card text.

  None of the three asserts an unqualified raw-predictor implication on its own. I hold no finding on them.
- *NH14.* These places carry the centring (and, where the constant is discussed, the fixed-multiple) qualifier:
  STATEMENT :118; REPORT :23; READER_DELTA :34; PLAN :41; the card at REPORT :36-37 (centring; see (a)).
  TARGET :21 and PLAN :36-38, :47 describe NH14's own hypothesis (isotropic, identity covariance) rather than a
  containment claim.
- *Feature mixtures.*
  - REPORT :34-36 (card): common L, mean zero, unit variance, common K.
  - READER_DELTA :18-21: "independent, mean-zero, unit-variance coordinates that are sub-Gaussian with constant L"
    (one L), and "confined to an interval of K standard deviations … (L = K)" (one K).
  - STATEMENT :139-141 and READER_DELTA :36-38 (the HQ 2b sentence, verbatim and identical in both): "independent
    features each confined to an interval of K standard deviations", with one K; ExSG (a), (b) is cited, and (A3) is
    noted as still needed (STATEMENT :141-142).
  - REPORT :79 (registry): one L and one K.
  - TARGET :14 and PLAN :31, :52: descriptions of the numerics and the plan; Rademacher at L = 1 is correct.

  None of these drops the common-constant or independence qualifier.

## (c) Per-claim decisions

| id | decision |
|---|---|
| W3-D3:Thm2SG | ACCEPT |
| W3-D3:B3w | ACCEPT |
| W3-D3:ExSG | ACCEPT |

Thm2SG's span and proof (P:Thm2SG sha 5db2fe6b2eca4beb, unchanged) are as accepted at R1 by both seats. The changes to
B3w and ExSG are the EQUAL clarifications confirmed above, and their proofs cover them.

## (d) Gates on manifest R2

- **correct: PASS.** The proofs are unchanged and accepted at R1. The two clarifications (common K; 𝒜′_n := ∅ for
  n < n₁) are covered by the proofs as written.
- **strength: PASS.** No sentence in the ticket now claims more than STATEMENT. The card, REPORT §2, READER_DELTA, TARGET
  and PLAN carry the centring and common-constant qualifiers. The 1.3 tags are correct (EQUAL ×3), and §1 is unchanged.
- **faithful: PASS.** The STATEMENT ↔ lemma copies agree (B3w :12-40, ASSEMBLY :56-60). The registry spans and quotations
  match. The external inputs are unchanged under the manifest.
- **statuses: PASS.** The registry status lines quote B3w.md:3 and ASSEMBLY.md:3 verbatim. The §6 input statuses are
  unchanged, and citecheck reproduces with 0 failures. Nothing is called checked that is not.
- **sweep: PASS.** I swept the whole frozen ticket for the Song–Liang, NH14 and feature-mixture statements; no
  unqualified instance remains. All 10 DEPS hashes reproduce, the five STALE rows were re-verified in full above, and the
  line shifts break no citation.
- **reader: PASS.** READER_DELTA's class-1 sentence now carries both brackets. Theorem 2′ and its remarks were correct at
  R1 and are unchanged. The card sentence is correct and matches STATEMENT §§3–5.

## (e) Score

**9.3.** I hold no C, S or F finding. Both R1 S findings are repaired in every affected place, including two places that
neither R1 seat had listed (TARGET :21, PLAN :44). The E fixes are accurate, and the bookkeeping (DEPS, registry spans,
citecheck) reproduces exactly.

COUNCIL-VERDICT round=R2 manifest=f559960469015b9c993e17cc82b3955ceee2890db189b8ae23e2aa2f1f4840a6 seat=opus score=9.3 gates=PASS

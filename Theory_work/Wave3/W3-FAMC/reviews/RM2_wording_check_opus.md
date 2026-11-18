model: claude-opus-5-5 (claudeAgent_personal, high); round=R1; seat=Opus PURE check; target=reviews/RM2_wording.patch

# PURE check of `reviews/RM2_wording.patch` (wording only)

Base: origin/main `a1d55cef` (= `git rev-parse origin/main`). Checkout `theory/W3-FAMC` @ `9d4d15dd`; both target files
are byte-identical between `a1d55cef` and the working tree. The patch was applied only to scratch copies under
`/tmp/claude-71711/rm2check` (deleted afterwards); the tree was not touched.

## 1. Hashes, line counts, BOM

| item | expected (`RM2_wording.sha256`) | computed | result |
|---|---|---|---|
| patch file | `885ad8c4…66cd20` | `885ad8c48b4152115ea894e5afa4519c68f9a810d717654113fdd9aae366cd20` | MATCH |
| pre `W2-LOC2/lemmas/L6_poly.md` (`git show a1d55cef:`) | `01a38806…0690b4` | `01a3880694e54586fab7f60eaba49af3b7246fed1efff61021126af1ad0690b4` | MATCH (tree copy identical) |
| pre `W3-RM2/lemmas/L6_examples.md` (`git show a1d55cef:`) | `84bb0239…bcc92c` | `84bb02399fbe6468c187c688661f0e9dfb994e6bdd16b593a9488dd4b6bcc92c` | MATCH (tree copy identical) |
| post `L6_poly.md` (`patch -p1`) | `b898acf5…c1635` | `b898acf5683ce2e22a102850bc953f2a73e47e5b32fda2bf3de45dab44f1c635` | MATCH |
| post `L6_examples.md` (`patch -p1`) | `b9f47482…e1df` | `b9f47482659c8f69aef06a947864b57bfe7e291c1270313b5d90be0f8dc8e1df` | MATCH |

`patch -p1` applied both hunks cleanly (no fuzz, no offset, no .rej/.orig). Line counts: L6_poly 477 → 477,
L6_examples 573 → 573. `diff --stat`: exactly 1 and 2 lines changed. First bytes of post L6_examples.md: `ef bb bf`
(UTF-8 BOM preserved).

## 2. Changed lines

| file:line | old | new | verdict | reason |
|---|---|---|---|---|
| `W2-LOC2/lemmas/L6_poly.md:107` | `of Sigma^-1, so its spectrum lies in [c,C]; conditional variance is at most` | `of (Sigma_{U union V})^-1 (the V-block, V the unconditioned variables; a submatrix of Sigma^-1 only if U union V=[p]), so its spectrum lies in [c,C]; conditional variance is at most` | **PURE** | Corrects a description. Cov(W_V given W_U) = Sigma_VV − Sigma_VU Sigma_UU^-1 Sigma_UV = ([(Sigma_{U∪V})^-1]_VV)^-1, so the new text is the correct identity; the old text holds only when U∪V=[p]. The conclusion is unchanged and still follows: Sigma_{U∪V} is a principal submatrix of Sigma, spectrum in [c,C]; its inverse has spectrum in [1/C,1/c]; a principal submatrix of that also has spectrum in [1/C,1/c] (Cauchy interlacing); inverting gives [c,C]. The variance bound ≤ 1 and the cross-reference to `L2_CT.md:55` are untouched. No hypothesis, bound or status changes. |
| `W3-RM2/lemmas/L6_examples.md:77` | `N_l={v in Q\{l}:d(l,v)<=r}, A=T intersect N_l and E=T\A, the normal equations give` | `N_l={v in Q\{l}:d(l,v)<=r}, T in the lattice (so T subset Q, RM2 STATEMENT.md:70; hence d(l,v)>r for v in E), A=T intersect N_l and E=T\A, the normal equations give` | **PURE** | States a condition already in force at every use. The step `||beta_T(l)_E||_1 <= F(r)` in (0.1) needs every v in E to satisfy d(l,v)>r, i.e. T ⊆ Q (otherwise a v in T∖Q near l lies in E). Q is already in scope on the pre-image line (N_l ⊆ Q). §0 is consumed in exactly two places, and both quantify T over the lattice: E2 (W-R) via (D-loc^b) (L6:233-245), where (D-loc) is "for all T ∈ 𝓛, l ∉ T" (RM `STATEMENT.md:154-156`, made polynomial by RM2 `STATEMENT.md:200-202`); and E3 (W)/(W-loc) (L6:321-325), where (W-loc) is "for every (T, l) ∈ 𝔓", with 𝔓 ⊆ 𝓛 × [p] (RM2 `STATEMENT.md:70`, `:159-161`). 𝓛 := {T : S₀ ⊆ T ⊆ Q} is at RM2 `STATEMENT.md:70`, so the cited line is correct. No use of (0.1)/(0.2) has a T outside the lattice: E1, E4 and E5 do not use §0; FAMC's A.4 (A6) uses "E2's (0.1)" with the same lattice N_l; no other ticket cites L6:75-102 except Astra's council text (descriptive). So the phrase is a reminder, not a restriction. The IR sentence at L6:65 ("uniformly over all subsets T excluding l") is a separate statement about (P3) and is unchanged. Nit: "T in the lattice" also assumes S₀ ⊆ T, which (0.1) does not need; "T subset Q" would be the minimal condition, but the extra assumption costs nothing at any use. |
| `W3-RM2/lemmas/L6_examples.md:168` | `unchecked)" [LC2C-3].` | `unchecked)" [LC2C-3]. (Check record: E2 was line-checked in LC2-C, file header :3-6; claims.tsv governs the status.)` | **PURE** | Pointer only. Header L6:3-6 does record LC2-C and lists "E1, E2, E3 … VERIFIED-WITH-AMENDMENTS" (`:3` "Check: LC2-C …" through `:6` "… [SC2-1])."), so ":3-6" is exact (the source note's "L6:1-5" was looser). The "Status: PROVED (by this seat, unchecked), conditional on …" text on L6:166-168 is unchanged; the parenthesis adds no status and claims no upgrade, and it defers to the registry, whose `status` for W3-RM2:Ex-PolyR already reads "PROVED; line-checked LC2-C; …". |

Non-blocking wording nits (none affects the verdict):
- POLY:107: "a submatrix of Sigma^-1 only if U union V=[p]" overstates the general case. The V-block of
  (Sigma_{U∪V})^-1 can equal the V-block of Sigma^-1 in special cases, e.g. when Sigma_{U∪V, rest} = 0. "in general"
  or "generally not … unless" would be exact. The source note (E2_check:61) has the same imprecision. It is a side
  remark that no argument uses.
- POLY:107: "V the unconditioned variables" could be misread as [p]∖U, which would make the parenthesis empty. "V the
  variables whose conditional covariance is taken (V={j,k} above)" is unambiguous.
- All three lines become long (181, 164 and 116 chars) in files hard-wrapped at about 80 columns. This is cosmetic.

## 3. Registry spans (`git show a1d55cef:Theory_work/INFRA/registry/claims.tsv`)

The table lists every row whose `file`/`lines`, `premises` or `status_source` points into either file. It also
includes the one row with a `notes` pointer.

| claim | version | statement span (`file:lines`) | premises | status_source |
|---|---|---|---|---|
| W2-LOC2:Lemma-BC | 1.0.0 | `L6_poly.md:78-84` | `L6_poly.md:33-41` | `W2-LOC2/REPORT.md:61` |
| W2-LOC2:Lemma-IR | 1.0.0 | `L6_poly.md:118-129` | `L6_poly.md:33-41` | `W2-LOC2/REPORT.md:61` |
| W3-RM2:Ex-PolyR | 1.0.3 | `W3-RM2/STATEMENT.md:259-275` | **`L6_examples.md:164-263`** | `W3-RM2/CHECKPOINT_7.md:26` |
| W3-RM2:Ex-PolyF | 1.0.3 | `W3-RM2/STATEMENT.md:259-275` | `L6_examples.md:264-329` | `W3-RM2/CHECKPOINT_7.md:27` |
| W3-RM2:Ex-Proxy | 1.0.3 | `W3-RM2/STATEMENT.md:259-275` | `L6_examples.md:330-384` | `W3-RM2/CHECKPOINT_7.md:28` |
| W3-RM2:Ex-Equi | 1.0.3 | `W3-RM2/STATEMENT.md:259-275` | `L6_examples.md:385-474` | `W3-RM2/CHECKPOINT_7.md:29` |
| (W2-LOC2:F-LOC2.poly) | — | — | — | `notes` cites `L6_poly.md:55-65` only |

- **Statement spans.** No changed line falls inside any statement span. POLY:107 is in Lemma BC's proof (85-109),
  outside 78-84 and 118-129. No claim has L6_examples.md as its statement file. The sha256 file's
  "registered statement spans untouched" line is correct.
- **Premises spans.** POLY:107 is outside 33-41. L6_examples:77 is in no premises span; §0 (33-102) is not
  registered. **L6_examples:168 lies inside W3-RM2:Ex-PolyR's premises span 164-263.**
- **status_source.** None points at a changed line or into either file; all point at REPORT/CHECKPOINT files.
- **Does the premises hit matter?** It does not affect purity. Line 168 is a pointer with no mathematical content, and
  it lies in the status line, not in the hypothesis text of E2. It does matter for the registry mechanics.
  `bvsreg.claim_hash` hashes the statement span **plus every premise span**. I recomputed it with the repository's own
  `bvsreg.py`, with ROOT pointed at the scratch pre/post trees:
  - Pre-image: all six rows match their stored sha256.
  - Post-image: W3-RM2:Ex-PolyR changes from `f28f7b50ec03…` to `4c3e392184a9…`. Lemma-BC, Lemma-IR, Ex-PolyF,
    Ex-Proxy and Ex-Equi are unchanged.
  - Consequence: after landing, `check.py` C2 would raise **C2-changed ERROR** for W3-RM2:Ex-PolyR. It is not
    downgraded to C2-moved because the row has premises. Fix: `registry.py rehash W3-RM2:Ex-PolyR --bump patch`
    (1.0.3 → 1.0.4) with a CORRECTION-ONLY reason.

### Downstream pins to update when the patch lands (bookkeeping, not purity)

- W3-FAMC cites `W3-RM2:Ex-PolyR@1.0.3` in `STATEMENT.md:178`, `REPORT.md:34` and `PLAN.md:12`.
- `W3-FAMC/reviews/MANIFEST_R5.txt:28,30` pins both pre-image shas as EXT entries. This is a frozen manifest; per
  the re-point rule it needs a recorded EXT re-point/version bump, not an edit to the manifest.
- `W3-RM2-R/DEPS.tsv:14` pins L6_examples.md at `84bb02399fbe6468` (state "OK (parent, read-only)") and will show
  drift.
- No claims.tsv row pins `Ex-PolyR@<version>` in a structured column (grep is empty).

## Verdict

All three changed lines are wording only. POLY:107 corrects a description and leaves its conclusion intact.
L6:77 states a condition (T ⊆ Q) that is in force at every use of (0.1). L6:168 is a bookkeeping pointer that leaves
the Status claim unchanged. The hashes, line counts and BOM all check out, and no statement span is touched.
Landing the patch does change one registry hash: W3-RM2:Ex-PolyR, through its premises span. That needs a PATCH
rehash and pin updates, but it is not a purity defect.

VERDICT: PURE

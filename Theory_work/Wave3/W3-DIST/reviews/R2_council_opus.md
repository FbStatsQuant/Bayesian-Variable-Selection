# W3-DIST — council diff round R2, seat `opus` (Claude Opus 5.5, Claude Third, effort high)

Frozen content reviewed: `reviews/MANIFEST_R2.txt`, first line `MANIFEST c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc`.
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-DIST Theory_work/Wave3/W3-DIST/reviews/MANIFEST_R2.txt`
returned `verify: OK MANIFEST c5cd9cdd…` before I read anything. I read: my own R1 review; the findings section of the astra R1 review;
`reviews/R1_disposition.md`; the whole diff `reviews/DIFFS_R1_to_R2.patch`; and, as needed for dependents, the current text of the
changed passages and of the passages they rest on. I changed no git state and wrote no file other than this one.

## Verdict summary

The diff resolves my only counted R1 finding (R1-opus-01). The gloss on the rate now holds A fixed, in all three places that
carried it: STATEMENT (c), `lemmas/DIST12.md` D.4 and the P3 row of TARGET. It also states that C depends on A, which is
what the proof gives. The text of TC3 is unchanged and is still proved as written. The new gloss "for fixed (A, σ*², M, M′),
ε_n² is of order (1 + s₀^r) log n/n" is exactly what is proved. I recomputed the constants of `X.md` §0 and `DIST12.md`
D.1: C² is free of s and M₀ ∈ [max(16, s), 16 + 4(1+s)(A+1) + 3B/(2σ²)], so the order holds in both directions. My six R1
editorial findings are all recorded in `ERRATA.md` (E3–E8).

The other seat's finding R1-astra-01 is repaired correctly. S, V, X, X′ and NEC now carry "conditional on SOP:TH09", with the
dependency `SOP:TH09@hyp`. For V and NEC the condition is conservative, which is harmless. The claims left unconditional (H, T,
P6, B0, B1, B2-core, B2, and B3 apart from its W3-POST condition) use no T01 result according to `DEPS.tsv`.

`REPORT.md` is byte-identical to what `mkreport.py` generates from the frozen inputs (regenerated in memory). The external
change to W3-MISR leaves every line that B0 quotes byte-identical, and R′@1.0.0 is still PROVED-CHECKED. Nothing in the diff
breaks a dependent. I hold no C, S or F finding. All six gates pass.

## My R1 findings

| id | kind | state | why |
|---|---|---|---|
| R1-opus-01 | S | **RESOLVED** | Repair (a), applied in all three places. **STATEMENT.md:84-87** (c): "for fixed (A, σ*², M, M′), ε_n² is of order (1 + s₀^r) log n/n … The radius constant C depends on A, so nothing is claimed about how the rate depends on A beyond the factor in M₀". **`lemmas/DIST12.md:70-72`**: the same, with a correct reason: C_X ≥ 4Λ ≥ 128[34(A+1)+2] (Λ ≥ 32C_x, C_x = 34(A+1)+2, `X.md:34-36`), and C_T = 4[34(A+7)+8] (`DIST12.md:34`). **TARGET.md:30** (P3 row): "ε_n² of order (1 + s₀^r) log n/n for fixed (A, σ*², M, M′) … the radius constant depends on A". The REPORT registry block of DIST-1 (rate field) now names the fixed parameters too. I searched the frozen operative files (STATEMENT, TARGET, REPORT, `lemmas/`, `work/` outside `api_attempts`) for the old free-A wording ("log p_raw/n", "log p/n", "(A + 1) log n"). The remaining hits are planning or history documents (ROUTES, ASSUMPTION_MAP, CHECKPOINT_1), a general sentence in TARGET §6 (A2) that makes no claim about DIST-1's constant, and the derivation `log(ep_raw/d) ≤ (A+1) log n` inside D.1. None asserts a rate linear in A. |
| E-01 | E | recorded | `ERRATA.md` E3 |
| E-02 | E | recorded | `ERRATA.md` E4 |
| E-03 | E | recorded | `ERRATA.md` E5 |
| E-04 | E | recorded | `ERRATA.md` E6 |
| E-05 | E | recorded | `ERRATA.md` E7 |
| E-06 | E | recorded | `ERRATA.md` E8 |

My two better-theorem proposals are listed at the foot of `ERRATA.md` as recorded for HQ, not adopted. That is consistent with
the disposition.

## Does the diff break anything

**Group 1: STATEMENT v1.4.10, DIST12 v0.3, TARGET row P3 (R1-opus-01).**
- *STATEMENT hunks.* There are two. One replaces three lines of (c) by three lines, so no line pointer moves (DIST-1 is still
  lines 74-91; REPORT's pointers are filled from anchors and regenerate identically). The other appends one changelog row (line
  496). The display (1.1), the equivalent ε_n form, the constants list and consequences (a), (b), (d), (e) are unchanged.
- *DIST12 hunks.* They change the header (version label) and one sentence of the paragraph "Dependence on the sparsity". D.0–D.3,
  Steps 1–3 of D.4, D.5, D.6 and D.7 are untouched, so the proofs of (1.1) and of (1.2) are byte-identical to what I checked in
  R1. I re-read the bracket after its D5-01 correction. It now claims only "gives no rate linear in A", which is correct: both C_X
  and C_T are increasing affine functions of A, so C² ≍ (A+1)² with the other parameters fixed.
- *DIST-2 (same proof file).* Unaffected: D.6 and the statement (1.2) are unchanged.
- *Reader Theorem A, Corollary C, DIST-C.* They consume (1.1)/(1.2) as displays, with constants "depending only on (s, A, K, c_ψ,
  b̄)" (STATEMENT:186-187). None of them uses the gloss in (c), so none is affected. DIST-C's predictive display uses ε_n² = C²t/n,
  which is unchanged.
- *TARGET P3 row.* Only the DIST-1 cell changed. The verdict "beats both (constant × log n/n …)" stays correct for fixed A,
  which is the setting of [SL] Theorem 2 at polynomial p. The other cells and the verdict columns are unchanged.
- *REPORT.* The DIST-1 registry block gains "(C depends on A, sigma*^2, M, M') … for fixed (A, sigma*^2, M, M') of order
  sqrt((1 + s0^r) log n / n)". This matches (c).

**Group 2: REPORT / REPORT_extra / mkreport.py (R1-astra-01, and the rate field).**
- *The five rows.* §1 rows 20-24 (S, V, X, X′, NEC) read "PROVED (by this seat), line-checked, conditional on SOP:TH09". The
  registry status lines match, with `status_source` REPORT.md:20-24, which are the correct rows. Each `depends_on` is
  `SOP:TH09@hyp`. §5 extends the T01 sentence to these five and points to the `uses` column of `DEPS.tsv`.
- *Is the repair correct and complete?* Yes. Per `DEPS.tsv`, S, X and X′ use substantive locked [P1] results: `thm:T01i`,
  `thm:Ta`, `lem:num`, the proof of `lem:den`, `lem:slab`. I verified this for X myself in R1 (`X.md` §4 and §0, "From [P1]").
  V and NEC use `lem:spec`/`lem:slab` identities, partly re-derived. Conditioning them is conservative and cannot overstate
  assurance. The claims that stay unconditional have no T01 use in their `uses` cells: H (D0 re-derived), T (self-contained),
  P6 (—), B0 (W3-MISR:R′, PROVED-CHECKED), B1 (—), B2-core (standard Bernstein and net), B2 (B1, B2-core, W3-POST2:A0
  re-derived). B3 is conditional on W3-POST:Thm-1 for its last sentence, as before. Every theorem-level claim already carried
  SOP:TH09, so no effective status changes. SOP:TH09 is not promoted.
- *Review trail (§2).* The rows for R1 and D5/D6 describe those rounds accurately: they match `R1_disposition.md` and my R1 file.
- *Regeneration.* I ran `mkreport.py` in memory, with its final write replaced by a comparison. The generated text equals the
  frozen `REPORT.md` byte for byte (35 929 characters), so the frozen REPORT is the generator's output on the frozen inputs.

**Group 3: DEPS.tsv, ERRATA.md, PINS.md.**
- *DEPS.tsv hashes.* The DIST-1 and DIST-2 rows carry `111c31af7990b881`, which equals the first 16 hex characters of the
  SHA-256 of the frozen `lemmas/DIST12.md`. The stretch rows carry `70b367001c7509ab`, the frozen `STATEMENT.md`.
- *DEPS.tsv `uses` cells.* They are refined for DIST-3, S, V, X, X′ and NEC. They list the [P1] lemmas used, which agrees with
  `X.md` §0 ("From [P1]: thm:T01i, lem:slab, lem:spec(b),(d),(e), lem:prior(b),(c),(e), lem:num, thm:Ta, the proof of lem:den")
  plus `lem:chi`(a) (F2). The check column stays OK and reflects the D5/D6 records.
- *ERRATA.md.* It is a record only and changes no claim.
- *PINS.md.* Only the version label changes, which is consistent with no line moving.

**Group 4: the external input W3-MISR/STATEMENT.md.**
- *What changed.* The frozen file hashes to `84eb0f27000da51c…` (manifest line 227). The R1 version (`git show 213e2115~1:…`,
  read-only) hashes to `797bca0e29ae2726…`, as the patch says. The diff has two hunks, @@ -1,4 +1,4 @@ and @@ -188,11 +188,11 @@,
  each replacing lines one for one. Both versions have 272 lines.
- *What B0 quotes.* I compared lines 60-90 of the two versions: they are identical. So `W3-MISR/STATEMENT.md:70-72` (R′ (a)) and
  `:75-77` (R′ (a′)), the lines quoted by `work/E_bridges/B0.md:44-51`, are byte-identical. The current text matches B0's
  quotation. The scope lines 20-22 that B0 also cites lie outside both hunks.
- *Status of R′.* `claims.tsv:412` (W3-MISR:R′@1.0.0, statement range 70-106) still reads "PROVED-CHECKED; council R2, MANIFEST
  217d6708…", status ACTIVE.
- *Relevance of the changed sentence.* It is Corollary H's KL reading, now limited to a deterministic intercept. W3-DIST does not
  consume it, and in any case the truth in W3-DIST has a deterministic intercept. No effect.

## Named confirmations

**3(a): CONFIRMED.**
- *Unchanged.* `TARGET.md:53` reads "**TC3 (DIST-1, rate).** Best radius ε_n² = C²M₀ log n/n with M₀ = O((1 + s₀^r)(A + 1))". The
  TARGET hunk touches only line 30 (the P3 row), and the manifest fixes the rest of the file, so TC3's text is unchanged since R1.
- *Proved as written.* `X.md` §0 defines M₀ := max{16, (A+1)s, log C₅} with log C₅ ≤ 4(1+s)(A+1) + 3B/(2σ²), where s = s₀^r. So
  M₀ ≤ 16 + 4(1+s)(A+1) + 3B/(2σ²) = O((1+s₀^r)(A+1)) for fixed (σ², M, M′). `DIST12.md` D.1 gives C_T, free of s. D.4 gives
  C = (C_X² + C_X/2 + 1 + C_T)^{1/2}, free of s, and the radius C√(t/n) at t = M₀ log n, that is ε_n² = C²M₀ log n/n. These
  passages are unchanged since R1, where I re-derived them.

**3(b): CONFIRMED, both "no more" and "no less".**
- *No more.* For fixed (A, σ*², M, M′), C² is a fixed positive number and M₀ ≤ 16 + 4(1+s)(A+1) + 3B/(2σ²) ≤ K(1+s). Hence
  ε_n² ≤ K′(1+s₀^r) log n/n. The sentence claims nothing about A beyond "M₀ of order (1 + s₀^r)(A + 1) for fixed (σ*², M, M′)",
  which is TC3's upper bound. It says explicitly that C depends on A.
- *No less.* The order also holds from below, because M₀ ≥ max{16, (A+1)s} ≥ 1 + s for integer s ≥ 0, A ≥ 1 (16 ≥ 1 + s when s ≤ 15; (A+1)s ≥ 2s ≥ 1 + s when s ≥ 1). Inline
  check: C²M₀/(1+s) stays in [4.3·10⁸, 2.6·10⁹] for A = 1 and s = 0…64. So "of order (1 + s₀^r) log n/n" is exact.
- *What the gloss leaves out.* The proof also gives C = O(A+1) explicitly. That is extra information, not a target clause, and
  it is recorded as a better-theorem proposal. Omitting it does not make the gloss weaker than TC3, which says nothing about C's
  dependence on A.

*Changelog tag of row 1.4.10: I agree.*
- **EQUAL on TC3.** The clause is not edited and is proved as written.
- **WEAKER on the descriptive sentence of (c).** The new sentence claims strictly less than the old one: A moves from free to
  fixed, and the free-A reading was not proved. The change log p_raw → log n changes no order once A is fixed. It is also the
  correct general form, since the setting has p_raw ≤ n^A, not equality. That sentence is not a target clause. The tag is honest:
  it does not present the old free-A sentence as having been proved.

## Gate table (on MANIFEST c5cd9cdd…)

| gate | verdict | basis |
|---|---|---|
| G1 correctness of every step | **PASS** | No proof step changed. DIST12 D.0–D.3, D.4 Steps 1–3, D.5 and D.6 are untouched, and `X.md` and every other proof file are unchanged since R1 (manifest). The one changed proof sentence (D.4, dependence paragraph) and its bracket are correct (Group 1). R1 verdict carried for everything else. |
| G2 hypotheses used = hypotheses stated | **PASS** | Carried from R1. The diff changes no hypothesis; (c) now fixes A, which is already fixed in (RD). |
| G3 no hidden assumptions | **PASS** | Carried from R1. The diff adds none. |
| G4 imports: status and content | **PASS** | Passed in R1. The diff makes the statuses of S, V, X, X′ and NEC carry "conditional on SOP:TH09" with `SOP:TH09@hyp`. This repairs R1-astra-01, and I agree with the repair. Every claim that uses a locked [P1] result now carries the condition; the others use none (Group 2). External input W3-MISR:R′: quoted lines unchanged, status PROVED-CHECKED (Group 4). |
| G5 constants and rates | **PASS** | Failed in R1 on R1-opus-01, now resolved. The rate gloss in STATEMENT (c), DIST12 D.4, TARGET P3 and the REPORT DIST-1 block states exactly what the constants give (3(b)). Constants unchanged otherwise; R1 verdict carried. |
| G6 fidelity to code; honesty of scope | **PASS** | Carried from R1 for the code: no code pin or code-facing text changed. Honesty of scope improved: the status conditions are now explicit, and the rate gloss no longer overstates. |

## Per-claim table

| id | decision | note |
|---|---|---|
| W3-DIST:DIST-1 | ACCEPT | decided again: (c) now proved as worded; (1.1) and (a), (b), (d), (e) unchanged |
| W3-DIST:DIST-2 | ACCEPT | proof (D.6) unchanged; carried |
| W3-DIST:DIST-3 | ACCEPT | carried |
| W3-DIST:DIST-C | ACCEPT | carried; consumes DIST-1's display only |
| W3-DIST:Thm-A | ACCEPT | carried; checked unaffected by the gloss |
| W3-DIST:Thm-B | ACCEPT | carried; conditional on W3-POST:Thm-1, as labelled |
| W3-DIST:Cor-C | ACCEPT | carried |
| W3-DIST:H | ACCEPT | carried |
| W3-DIST:T | ACCEPT | carried |
| W3-DIST:S | ACCEPT | decided again: status now "conditional on SOP:TH09", correct |
| W3-DIST:V | ACCEPT | decided again: status now conditional (conservative), correct |
| W3-DIST:X | ACCEPT | decided again: status now conditional, correct |
| W3-DIST:X' | ACCEPT | decided again: status now conditional, correct |
| W3-DIST:NEC | ACCEPT | decided again: status now conditional (conservative), correct |
| W3-DIST:P6 | ACCEPT | carried; uses no T01 result |
| W3-DIST:B0 | ACCEPT | decided again for the external change: the quoted lines of W3-MISR are byte-identical; R′ PROVED-CHECKED |
| W3-DIST:B1 | ACCEPT | carried |
| W3-DIST:B2core | ACCEPT | carried |
| W3-DIST:B2 | ACCEPT | carried |
| W3-DIST:B3 | ACCEPT | carried |

## New findings (C / S / F)

None.

*Note outside the scoring (not a finding; pre-existing text the diff does not change; recorded so the lead can decide whether
it belongs in `ERRATA.md`).*
- *What the text says.* STATEMENT (1.2) and the DIST-2 cell of TARGET's P3 row write DIST-2's best rate as
  "ε_n² ≍ (1 + s₀^r) log n·ℓ_n/n".
- *What the proof gives.* DIST-2's constants depend on s₀^r through C_m (`X.md` §9, `DIST12.md` D.1 C_T′), and the inline
  computation gives C₂²M₀′ growing like (1 + s₀^r)³. Taken literally as a statement about the sparsity, the factor (1 + s₀^r) is
  therefore not tracked.
- *Why it is not an S finding.* The theorem states explicitly that c, C, M₀ and n₀ depend on s₀^r, and s₀^r is fixed in (RD).
  Read literally, the ≍ statement is true as an order in n. TC6 fixes no sparsity dependence. This differs from R1-opus-01,
  where the parenthetical explicitly left A free.

## Overall score

**9.2 / 10** (C, S and F only). There is no C, S or F finding. Both R1 findings are repaired exactly, without changing a
statement, hypothesis, constant or target clause. The mathematics was accepted in R1 and is unchanged.

## Checks performed

- Manifest verified (`verify: OK`, digest c5cd9cdd…).
- Read every hunk of `reviews/DIFFS_R1_to_R2.patch`: STATEMENT, DIST12, TARGET, REPORT, REPORT_extra, mkreport.py, DEPS.tsv,
  the PINS/ERRATA notes and the W3-MISR hunks.
- Re-read the current `lemmas/DIST12.md:25-100` (D.1–D.6), `lemmas/X.md` §0 (constants, M₀) and §9 (constants of X′),
  `STATEMENT.md:72-100` (DIST-1, DIST-2), `:185-238` (reader text, constant dependence), `:430-439` (imports), and `TARGET.md:30, 53`.
- SHA-256 prefixes of STATEMENT, DIST12, TARGET, REPORT and DEPS.tsv, against the patch headers and the DEPS.tsv hash cells.
- `mkreport.py` regenerated in memory and compared with `REPORT.md`: identical.
- `status_source` line numbers and `depends_on` fields of every registry block in `REPORT.md`; `DEPS.tsv` `uses` cells for all
  claims (which claims use T01).
- W3-MISR: frozen and R1 versions (git read-only) compared on lines 60-90 (identical), line counts equal, B0's quotations against
  the current lines 70-72 and 75-77; `claims.tsv:412` status of R′.
- `ERRATA.md` against my E-01 … E-06 and the better-theorem proposals.
- One inline `nice` Python computation (no files) of C², M₀ and C²M₀/(1+s) for DIST-1 (A = 1, 4; s = 0…64), and of the
  analogous DIST-2 quantity.
- grep of the frozen operative files for leftover free-A rate wording.

## Not checked

- Unchanged text, not re-read (as the brief directs). In particular no proof file other than the D.4 paragraph of DIST12, and
  no code.
- `reviews/D5_sol_diff.md` and `D6_sol_diff.md` were consulted only to confirm the trail rows; I did not rely on them for any
  conclusion above.
- The other seat's R2 review (not available to me, and not read).
- No scratch directory was created; nothing to delete.

`COUNCIL-VERDICT round=R2 manifest=c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc seat=opus score=9.2 gates=PASS`

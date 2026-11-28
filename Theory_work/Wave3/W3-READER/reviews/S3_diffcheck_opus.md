# S3 diff check — W3-READER (PROTOCOL_v4 statement-change check)

Fresh independent checker, Claude Opus 5.5, effort high, one pass. Read-only except this file; no git state changed; no
subagents. Style and readability are not reviewed and no new theorems are proposed.

**Integrity.** `sha256sum -c MANIFEST_S3.txt` → all 21 entries OK. `MANIFEST_S2.txt` → all 11 OK. The live working
copies of STATEMENT, READER_VERSIONS, CLAIMS_CARD, NOTATION, REPORT, METHOD_INTUITION and R1–R4 are byte-identical to
`S3_frozen/`. The DIFF_* files are the review object. Empty diffs: NOTATION, R2, REPORT, STATEMENT. The staged delta
`deltas/thm3_W3-PSHARP-R.md` was hash-checked only and is not reviewed.

**Tag convention used here.** Tags rate the strength of the *statement* (hypotheses + conclusions) relative to the
S2-frozen text. Adding a premise or narrowing a conclusion is **WEAKER**. Dropping a premise or adding a claim is
**STRONGER**. The lead's logs tag the *convention list* "STRONGER" when premises are added; that is the opposite
direction for the theorem, and §3 lists every disagreement.

---

## 1. S2 findings F1–F9

| # | Verdict | Check against the cited source |
|---|---|---|
| F1 | **RESOLVED** | (S4)(i)–(iv) (`READER_VERSIONS.md:27-45`) now carries the items below. (i) IDEAL-W incl. stream-id/allocation overflow, EX-A as a unit-cost model incl. exp/log, and MACH(τ,τ₀,β,β₀) with the allocation-success, build and no-interruption clauses = `C-DLV/STATEMENT.md:24-31`. (ii) CONFIG = C-DLV:32-37: LS0 cap ℓ_n+\|S̃₀\|, TDP-IMPL with the exact O(p Σ_b(2^{\|C_b\|}+(K+1)²)) operations and O(Σ_b 2^{\|C_b\|}+J(K+1)) storage (C-DLV:38-42), e4 tie rule, default summary list, certificate budgets inside the allocation, w-fold memory, fixed islands, grid fallback on (F-UNI `L5_delivery.md:8-9`; FIN s6 Prop. F "Fallback"). (iii) EX-S, SR, GUARD-W. (iv) the seed domain (C-DLV:43-44), plus the allocation by exact reference to `FINAL/sections/s6_delivery.tex:29-62`: W_G, M_G, P₀, P₁, P̄_t, certificate budgets, P̄_LS0 and the archive term A. R3's MACH/CONFIG/TDP-IMPL/allocation rows now cite the right lines. Incorporating the allocation inequalities by reference is acceptable: "valid declared inputs" also carries the named finite positive `mem_gb`/`hours` fields through the reference and R3's seed row. |
| F2 | **RESOLVED, with a regression** | (S5) (`READER_VERSIONS.md:47-58`) now has EX-A, H-U within streams, SI, START **with** the exact Z̄₀ = Σ_Ω γ₀, KERNEL with the uniform state-independent order, CAL, MEAS (code bridge `L1_bridge.md:33-55`), and the potential run = N1 `STATEMENT.md:72-88`, matching SAMP §1 (`W3-SAMP/STATEMENT.md:64-70`). **However**, the S2 text's "independent of the data" was dropped in the rewrite; see finding **N1** (MAJOR). |
| F3 | **RESOLVED** | 𝒜 := {sampler branch} ∩ {calibration ok, fallback included} = SAMP:38-41 (`v3_fit.R:154` returns before any final run otherwise; `v3_calib.R:163-183`). The estimates are defined from the uninterrupted island records on 𝒜 and equal the printed fields on completed runs. That is SAMP:29-37 plus Lemma PC (SAMP:90-95), checked in code: `v3_run.R:143-149` suppresses estimates on a stop; `:150-163` computes the pooled fields. "Intersections, not conditioning; no lower bound on P(𝒜)" = SAMP:35-37 and §3. The added printed-field clause (rate × 1{completed}) follows from PC and {completed} ⊆ 𝒜. The exact branch is put outside the theorem (SAMP:186) and gets a separate remark; see N3 for its citation. |
| F4 | **RESOLVED** | Card row 3.6 (`CLAIMS_CARD.md:51`) now reads: errors × 1{calibration success} are O_P(n^{-1/2}e^{C√log n}); P(success ∩ MPM wrong) → 0; P(completes ∩ reported wrong) → 0; no lower bound on P(success). This matches C-v (SAMP:158-162). The "w.p. → 1" wording is gone. |
| F5 | **RESOLVED** | The row's setting is now Theorem 10's: signal fixed on the standardised scale, Theorem 2's population floor, Theorem 5's visibility/no leakage. W2-APP:POST is quoted in full and noted as covering this convention (`W2-APP/lemmas/L1_POST.md:11-18`, as R4 uses it). No raw-coefficient claim remains on the row. |
| F6 | **RESOLVED** | The title "no eigenvalue condition off S₀ beyond the vanishing floor (A5)" (`READER_VERSIONS.md:111`), remark (o) (:123-124) and card 1.1 are now true of the reader version. The only eigenvalue conditions are (A4′)'s floor on S₀ and (A5) (unnormalised g₀, i.e. g₀/(n−1) on the correlation scale). Master POST2 E (`W3-POST2/STATEMENT.md:128-133`) has (OS) in place of (A5); the reader keeps the stronger (A5), and the title now says so. |
| F7 | **NOT RESOLVED (partly)** | The new header (`R4:3-4`) says "the other cited inputs are 'PROVED-CHECKED'". That is false for two inputs R4 itself cites. (a) R1 B2.1/B6.1 (`R4:29, :32`) has status "PROVED (by this seat, unchecked)" (`R1:3`); the S2 line check passed it but did not change its status. (b) The posterior input W3-POST:Thm-1 item 6 = SOP:TH09 carries "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)", not "PROVED-CHECKED". See finding **N2**. |
| F8 | **RESOLVED** | R3 now quotes `v3_fit.R:151` exactly (`isTRUE(ls0) && isTRUE(getOption("v3.grid_fallback", TRUE))`) and requires both defaults through (S4)(ii). It cites recording at `v3_calib.R:120-124` and selection/freeze at `v3_calib.R:163-189` (verified: selection at :168-174, freeze through `v3_frozen` at :183-189). |
| F9 | **RESOLVED** | `R1:8`: d < 2.4664 (1/log 1.5 = 2.46630…). |

## 2. Other hunks: wording only, or a change in strength?

**Theorem 1, (A4′) and remarks (`READER_VERSIONS.md:111-141`).**
- (A4′): "c₁(s₀,A) an explicit constant, not optimised". Wording only. c₁ depends only on (s₀,A) (POST2:130).
- Remark (o) and (iii): the numerical values (c₁≈161, c₀=128, the c₀ formula) are removed, as H5-6 asks. Both are now
  "explicit constants depending only on (s₀,A), not optimised". That is consistent with POST2:136-137 ("both are proof
  artefacts") and POST:75. A grep of the S3 texts finds no remaining numerical value of c₀ or c₁. Wording only.
- Remark (v): "no eigenvalue condition (size-tail lemma, which uses a coefficient bound instead)". This is more
  accurate than "no eigenvalue condition at all": POST2 Claim B (:70-75) uses ‖μ‖² ≤ nM and B_T(ϑ) ≤ B. Wording only;
  if anything it narrows the description.
- **Remark (vi)** (scope of the rate). "On every design the miss is at least of order n^{-1/2}" is supported by PSHARP
  Corollary B (`W3-PSHARP/STATEMENT.md:92-96`): δ/(1−δ) ≥ c(p,s₀)/√n with c ≥ 1 for s₀ ≥ 1, needing only
  s₀ ≤ K−1. "The extra √log n only on the witness designs of Theorem 3(b)" matches H5-6's condition. "No two-sided
  √(log n/n) rate on every design is claimed" claims nothing, so the remark does not strengthen any conclusion. Two
  descriptive defects: the open item is mis-scoped (N4), and "shown to be attained only on" is ambiguous (N5).
- **Remark (vii)** (D-17). Descriptive and not a theorem. It is consistent with Theorem 3(a)/(b) and with the D-17
  record (main:`Docs/Experiments/P1M/DECISIONS.md:81`: "all S₀+j survive the cut and hold 0.5–1.2× S₀'s weight"). The
  order n^{-1/2}/p per superset agrees with Corollary B's j=1 term. It does not call the output a point mass at
  moderate n. "The theorem describes the limit n→∞" is neutral and does not present asymptotics as a limitation; it
  understates Theorem 1's finite-n expectation bound, which is not an overclaim. It is also compatible with
  HPM = MPM = S₀: each superset is individually light. Wording only.
- (A4′) "Why" line: "sufficient; not known to be necessary (open item O3)" (H5-6 verbatim intent); c₁ a proof
  artefact (O2), as POST2:137 says. Honest limits: no numerical values. Wording only.

**Theorem 3: new scope sentence (`:299-300`) and header (`:273`).** The sentence adds no claim: it says only that
part (a)'s order n^{-1/2} is proved on a general design, which is correct per PSHARP B, and that a matching lower bound
is open. No hypothesis or conclusion changes. The open item is mis-scoped (N4). The header points to the staged delta
and says "not in force". That is metadata only and correct.

**Theorem 6–7 (S4) changes.** Premises are added; this is not wording only. Tags are in §3.

**Theorem 10 (`:744-817`).**
- Scope sentence and 𝒜 (sampler branch ∩ ok): the conclusion is narrowed to a smaller event. Faithful to SAMP:38-41.
- Potential vs printed estimates: correct per SAMP §0 and PC. The printed-field clause is a valid consequence, not a
  new claim beyond C-v.
- "No lower bound on P(𝒜)": correct.
- **Exact-branch remark** (`:774-775`): a new claim, because the theorem's printed-output coverage is extended to the
  exact branch. It is true in substance: SAMP:186 says that on that branch "HPM, PIPs and MPM are exact and W3-POST
  applies directly"; `v3_fit.R:120-131` returns the exact log_Z, PIPs, MPM and HPM when `e$status == "exact"`. But it
  cites "Theorem 2 itself", which is stated for raw coefficients, while Theorem 10 fixes standardised θ*. That repeats
  the F5 conflation (N3).
- Header "Pending delta: post-freeze rider SAMP-R1": metadata only.
- "Why" line (D-17): wording only. The claim that π₀ at moderate n is the same S₀/superset mixture has no source
  (D-17 measured the posterior/store law); N9.
- (S5): see N1.

**Card rows.**
- 1.1: EQUAL. It matches the reader text after F6 and H5-6. NIT: c₁ is named but not linked to the margin constant c
  (N7).
- 1.3: only the "Buys" column changed. It narrows "yes" to the witness designs and states the every-design order
  n^{-1/2}, which is PSHARP A2/B scope (`W3-PSHARP/STATEMENT.md:92-110`). Same N4 scope wording.
- 3.5: the "Buys" column now credits Del Moral and says "for the method as coded, calibration included". This hunk
  comes from the lead's adoption of GATES row 3.5 (`GATES.md:99-103`), a source not named in the brief. The result
  column still says "Given the frozen calibration", so no conclusion changes. Wording only.
- 3.6: F4/F5 rewrite; tagged in §3.
- D-17 note (`CLAIMS_CARD.md:95-98`): descriptive and faithful to D-17. The cited path exists on `main`, not on this
  branch (N8).

**METHOD_INTUITION.**
- §3: "as n grows" added. Wording only. The sentence still gives c < ½ for "a small set" of imitators; that is right
  only when "small" means bounded size (START-R: c < ε for \|Q\| ≤ n^{1/2−ε}). That wording predates this diff;
  NIT N10.
- §7 moderate-n paragraph and the toy-example parenthetical: descriptive, no point-mass wording, wording only.

**Lemma edits.** All are wording or citation changes with no change to any lemma's claim:
- R1: typo fix.
- R3: premise table rows only.
- R4: header scope note. R4's claim already used SAMP's 𝒜.

## 3. Changelog tags (relative to S2-frozen)

| Item | My tag | Reason; for WEAKER: restores a master premise? | Lead's tag | Agree? |
|---|---|---|---|---|
| Thm 6 delivery clause ("always produces output") | **WEAKER** | Adds MACH constants, certificate budgets, TDP-IMPL cost/storage, w-fold memory, grid fallback on, LS0 archive/time allocation. Each one **restores a master premise**: C-DLV `STATEMENT.md:28-31` (MACH), :32-37 (CONFIG), :38-42 (TDP-IMPL), :43-46 (inputs/allocation); FIN `s6_delivery.tex:29-35` (fallback, W_G/M_G, P̄_LS0, A); F-UNI `L5_delivery.md:7-12`. | "convention list STRONGER (now faithful)"; S2_disposition: "theorem clauses EQUAL" | **Disagree.** Added premises make the clause weaker. "Theorem clauses EQUAL" is wrong for the delivery clause. |
| Thm 6 statistical and common-data-event clauses | EQUAL | (S4) is not used by them (R3:41-43). | (EQUAL) | Agree |
| Thm 7 delivery clause | **WEAKER** | Same as Thm 6, same master lines. | "as Theorem 6" | Disagree, as for Thm 6 |
| Thm 7 statistical and common-data-event clauses | EQUAL | As Thm 6. | — | — |
| Thm 10, via (S5) | **WEAKER, with one STRONGER component** | Adds START's exact normaliser, KERNEL's uniform order, MEAS, POT, SI. These **restore master premises**: N1 `STATEMENT.md:73-86`; SAMP :64-70. But the final streams' independence **from the data** was dropped. Relative to S2 (`S2_frozen/READER_VERSIONS.md:38-39`) and to the master (SAMP:39-41; PoolZ STATEMENT.md:31-33), that drop is **STRONGER** (N1). After N1's fix: WEAKER. | "convention list STRONGER (now faithful)" | **Disagree** on direction, and the lead's tag misses the dropped premise |
| Thm 10 scope (𝒜 = sampler ∩ ok; potential estimates; printed × 1{completed}) | **WEAKER** | Smaller event, and conclusions stated for defined objects only. **Restores master restrictions**: SAMP :38-41 (𝒜 = {SMC branch, status ok}), :29-37 (potential quantities, intersections only), :90-95 (PC), :186 (exact branch excluded). | WEAKER | Agree |
| Thm 10 exact-branch remark | **STRONGER** (new remark claim) | Adds a claim about the exact branch. Supported by SAMP:186, `v3_fit.R:120-131` and W2-APP:POST's standardised-signal coverage, but the citation is wrong (N3). | lumped into WEAKER | Disagree: tag separately |
| Thm 10 "why" line (D-17) | EQUAL | Not part of the statement. | EQUAL | Agree |
| PoolZ remark (Thm 10, row 3.5) | EQUAL | The remark text is unchanged and PoolZ's own setting already states the N1 premises. (S5) drops data independence, but the fixed-data identity does not need it; the joint-law form in STATEMENT.md:31-33 states it itself. | — | — |
| Thm 1 (A4′), title, remarks (o), (iii), (v), (vi), (vii), "why", limits | EQUAL | Descriptions, constants without values, non-claims. | EQUAL (v0.4–v0.6) | Agree |
| Thm 3 scope sentence | EQUAL | A non-claim. No log entry was written (N6). | none | — |
| Thm 3 header (staged delta) | EQUAL | Metadata only; not in force. | — | — |
| Card 1.1 | EQUAL | Description aligned with F6 and H5-6. | (EQUAL via F6) | Agree |
| Card 1.3 ("Buys") | **WEAKER** | "Optimal" is narrowed to the witness designs. **Restores master scope**: PSHARP `STATEMENT.md:92-110` (B: order n^{-1/2} on every design; A2/B3: √log only on witnesses with log p ≍ log n). | none | — |
| Card 3.5 ("Buys") | EQUAL | Attribution and context; the result column is unchanged. | none | — |
| Card 3.6 | **WEAKER** | F4: "w.p. → 1" replaced by intersections. **Restores** C-v (SAMP:158-162) and SAMP:35-37 / §3 ("nothing conditional on 𝒜; P(𝒜)→1 not claimed"). F5: the raw-coefficient setting, which no master supports for Theorem 5's conditions, is replaced by the standardised setting covered by APP `L1_POST.md:11-18` and START2. Strictly the two hypothesis sets are not nested, but the change removes unsupported coverage. Sampler-branch scope is added (SAMP:38-41). | F4 WEAKER; F5 "EQUAL to reader" | Agree on F4. On F5, EQUAL holds relative to reader Thm 10, but relative to the S2 card it is **WEAKER** |
| Card D-17 note | EQUAL | Description only. | — | — |
| METHOD_INTUITION hunks | EQUAL | Description only. | — | — |
| R1 / R3 / R4 edits | EQUAL | Typo, premise-table rows, header scope note; no claim changed. | — | — |

## 4. Findings

**N1 — MAJOR — (S5) drops the final streams' independence from the data.**
`S3_frozen/READER_VERSIONS.md:49-50`. S2 read "the final run's random numbers are ideal uniforms, independent of the
data and of the calibration's random numbers" (`S2_frozen/READER_VERSIONS.md:38-39`). S3 reads "within each random
stream, fresh independent ideal uniforms; the final run's stream for each island independent of the calibration's
streams". Independence from the data is gone. Theorem 10 is stated "under the joint law of design, noise and the
method's random numbers". SAMP's joint-law level requires "the final streams 10–13 … independent of the data as well as
of streams 0–9" (`W3-SAMP/STATEMENT.md:39-41`, "C1 Opus #7"). PoolZ's joint-law form uses the same premise
(`STATEMENT.md:31-33`). Without it, conditioning on (data, 𝒞) no longer leaves the final streams iid uniform, and C-v's
integration step fails. The hunk drops a hypothesis of the master.
*Minimal fix:* "the final run's stream for each island independent of the data and of the calibration's streams".

**N2 — MINOR — F7's repair misstates the input statuses.**
`R4:3-4`. Write "An assembly conditional on `W2-APP:POST` (status quoted below). The registry inputs `W3-SAMP:C` and
`W3-START2:IF-START` are 'PROVED-CHECKED'. The posterior input `W3-POST:Thm-1` item 6 carries its own label. The
bridges R1 B2.1/B6.1 are 'PROVED (by this seat, unchecked)'." No upgrade has occurred in the registry; only the
header is wrong.

**N3 — MINOR — the exact-branch remark cites "Theorem 2 itself".**
`READER_VERSIONS.md:774-775`. Reader Theorem 2 fixes raw β*; Theorem 10 fixes standardised θ*. *Minimal fix:* "their
consistency is the posterior input of B10.1 (`W2-APP:POST`, which covers the standardised-signal convention,
`L1_POST.md:11-18`; cf. `W3-SAMP/STATEMENT.md:186`), on runs where enumeration completes".

**N4 — MINOR — the open item behind the rate-scope sentences is mis-scoped.**
`READER_VERSIONS.md:136-137`, `:299-300`; `CLAIMS_CARD.md:32` "Buys". Post-freeze rider POST2-R1 is an **expectation**
lower bound Eδ_n ≥ c r_n − 4/n under a floor on S₀∪{j} (`CARD_ROW11_R03b.md:27`). The texts call "a matching
√(log n/n) lower bound on every design" open. Theorem 3's displays are pathwise and in probability. In probability,
the √log factor is tied to log p (PSHARP:87-88; B3 at :105-106: no claim when log p = o(log n)), so the in-probability
statement is not the rider's question. This is not a strength change: nothing is claimed. *Minimal fix:* "a matching
lower bound E[1−π(S₀|y)] ≳ √(log n/n) in expectation, under a floor on S₀∪{j}, is open (POST2-R1); in probability the
√log n factor is shown only when log p ≍ log n (Theorem 3(b))".

**N5 — NIT — ambiguous phrasing in remark (vi).**
`READER_VERSIONS.md:136`: "is shown to be attained only on the witness designs" can be read as "is attained only
there". Write "has been shown to be attained on the witness designs of Theorem 3(b); on other designs it is not
known".

**N6 — NIT — version bookkeeping.**
- thm1 header "Section version 0.4" while its log runs to v0.6, and the v0.4–v0.6 entries are in reverse order.
- thm6/thm7 headers 0.2 vs logs v0.4; thm10 header 0.3 vs log v0.5.
- thm3 has no log entry for the H5-6 scope sentence.
- The card header still says "v0.5" with no changelog entry for the S2/H5-6/D-17/3.5 edits; GATES:102 calls the 3.5
  change "card v0.6".

Fix: bump the headers, add the missing log lines, and use the tags in §3.

**N7 — NIT — c₁ is named but not linked to c on card row 1.1.**
`CLAIMS_CARD.md:30`. Write "residual signal ≥ cσ*² log n with c > c₁(s₀,A), an explicit constant, not optimised".

**N8 — NIT — status quote and source paths.**
(a) (S5)'s inherited-status quote gives START the KERNEL string. N1:73 gives START "PROVED (candidate)" only; the
reader follows SAMP:66-67, which does the same. Quote the two separately, or cite SAMP as the source of the joint
quote. (b) D-17's path `Docs/Experiments/P1M/DECISIONS.md` exists only on `main`, not on this branch; add the branch
or commit.

**N9 — NIT — π₀ at moderate n is unsourced.**
`READER_VERSIONS.md:784-785`. The claim that π₀ at moderate n is a mixture over S₀ and its one-variable supersets has
no source; D-17 measured the posterior/store law. Write "π (and π₀, which concentrates more slowly)", or drop π₀.

**N10 — NIT — "small set" in METHOD_INTUITION §3.**
`METHOD_INTUITION.md:69-71`. "Confined to a small set … c < ½" is right only for a set of bounded size. Write "a set
of bounded size", or give the exponent c < ε for \|Q\| ≤ n^{1/2−ε}. This predates the diff, but the sentence was
edited.

No FATAL finding. No hunk makes a conclusion stronger than its master, apart from N1, which drops a hypothesis. No hunk
asserts a finite-n property that the masters do not give: remarks (vi)–(vii), the card note and METHOD_INTUITION are
descriptive and say the theorems describe the limit. All quoted registry statuses are unchanged, except N2's header
wording.

## Summary table

| Item | Verdict | Tag |
|---|---|---|
| F1 (S4) / R3 rows | RESOLVED | Thm 6–7 delivery: WEAKER (restores C-DLV:28-46, FIN s6:29-35) |
| F2 (S5) | RESOLVED; regression N1 (MAJOR) | Thm 10: WEAKER + STRONGER component (N1) |
| F3 Thm 10 scope | RESOLVED | WEAKER (restores SAMP:29-41, 90-95, 186) |
| F4 card 3.6 | RESOLVED | WEAKER (restores SAMP:158-162, :35-37) |
| F5 card 3.6 | RESOLVED | WEAKER vs S2 card (EQUAL vs reader Thm 10) |
| F6 Thm 1′ title, (o), card 1.1 | RESOLVED | EQUAL |
| F7 R4 header | NOT RESOLVED (N2, MINOR) | — |
| F8 R3 fallback row | RESOLVED | EQUAL |
| F9 R1 decimal | RESOLVED | EQUAL |
| Thm 1 remarks (iii), (v), (vi), (vii); (A4′) | wording only; N4, N5 | EQUAL |
| Thm 3 scope sentence + header | wording only; N4 | EQUAL |
| Thm 10 exact-branch remark | substantively true; N3 | STRONGER (new remark claim) |
| Thm 10 "why" line | wording only; N9 | EQUAL |
| Card 1.1 | OK; N7 | EQUAL |
| Card 1.3 | OK; N4 | WEAKER (restores PSHARP:92-110) |
| Card 3.5 | OK (source: GATES row 3.5) | EQUAL |
| Card D-17 note | OK; N8(b) | EQUAL |
| METHOD_INTUITION | OK; N10 | EQUAL |
| Bookkeeping | N6 | — |

S3-VERDICT: FIXES-NEEDED

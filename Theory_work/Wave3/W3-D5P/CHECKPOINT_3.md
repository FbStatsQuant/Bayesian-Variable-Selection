# W3-D5P — CHECKPOINT_3 (CP3 package; 2026-11-17)

**Passing round.** HQ-ordered targeted re-check R3 (Opus 5.5 high, Claude Personal) on `reviews/MANIFEST_R3.txt`
(MANIFEST 35a027bee24df09f64dc3f3f5b5cb47de7d74b71f77817b87d782f26b5723c8a; branch theory/W3-D5P a2c465a4):
LIST-K ACCEPT, LIST-CODE ACCEPT, LIST-R ACCEPT (conditional on IMPL-LIST); all six gates PASS; score 9.4.
`manifest.py bind` → `reviews/BIND_R3.txt`: "bind: OK … council cell: R3; MANIFEST 35a027be…; opus=9.4 PASS(reviews/R3_council_opus.md)".
`manifest.py verify` on the final tree: OK. Council history: R1 (952d9840) sol 7.5 FAIL / opus 8.4 FAIL (3 F in derived
texts; 1 minor C, the pin → post-commit transfer step) → R2 diff round, Opus-only per manager (7431d66d) 8.8 FAIL (1 F in
CARD.md) → R3 (HQ order) 9.4 PASS. No finding ever against LIST-K or LIST-CODE; no C against the mathematics after R1.
Line checks: LC1 (Opus, Claude Third) VERIFIED-WITH-AMENDMENTS; LC1R (Opus) VERIFIED-WITH-AMENDMENTS (E only); statement
lock SL1 (Sol) LOCK WITH CHANGES. Every review file is in `reviews/` with its brief and disposition.

**Claims (statement `STATEMENT.md` v1.1.2 = locked v1.0 + EQUAL changelog rows; proofs `lemmas/L1–L3`).**
| claim | statement | proposed status (HQ records) |
|---|---|---|
| W3-D5P:LIST-K | `STATEMENT.md:67-75` | PROVED-CHECKED; council R3, MANIFEST 35a027be…, opus=9.4 PASS |
| W3-D5P:LIST-CODE | `STATEMENT.md:79-95` | CODE-CHECKED (code reading at core 4676af6); council R3, MANIFEST 35a027be…, opus=9.4 PASS |
| W3-D5P:LIST-R | `STATEMENT.md:99-125` | PROVED-CHECKED, conditional on IMPL-LIST (method commit pending); council R3, MANIFEST 35a027be…, opus=9.4 PASS |
Consumed (verbatim): W3-RM2-R:RM2-R-plus, RM0-plus, DLV-0 @1.0.1 "PROVED-CHECKED; council R3, MANIFEST 5d6d3c90… (= R3
b06a8588 re-frozen as R3r), sol=9.5 PASS, opus=9.4 PASS"; W3-SAMP:CC@1.1.2 "CODE-CHECKED (lead; SL1, LC1, SW1, both council
seats)"; W2-APP:POST@1.0.7 "PROVED-CHECKED". Hypotheses of LIST-R: those of RM2-R-plus = Theorem 6, nothing added (D109).

**Record correction for HQ (record-only re-freeze R3r; no claim text changes).** `ingest.py claims REPORT.md` refused the
frozen REGISTRY blocks on 8 format items (conclusion level tags; LIST-R hypotheses as prose instead of assumption ids;
non-commit `method_commit` values; a marker inside an assumption list). Corrected blocks + DEPS LIST-R row (checked by R3,
now OK) + `ERRATA.md` (R3's two E notes) are in `reviews/R3r_correction.patch` (`git apply --check` clean; expected
post-apply sha256 in `reviews/R3r_expected_sha256.txt`). With it, `ingest.py claims … --staged`: 0 problems; staged
check.py 0 ERROR; **acceptance PASS** for the 3 ids (`reviews/INGEST_staged_CP3.txt`). HQ applies it as a CORRECTION-ONLY
re-freeze (precedent W3-RM2-R R3r) or tells me to.

**DEPS** all OK at the R3 manifest except the LIST-R row, which R3 checked at its current sha (fixed in the patch).
**citecheck** `reviews/CITECHECK.txt`: 186 citations, 0 MISS. **HOLDS.md** (origin/main): no hold on a consumed claim.

**`log_Z_list` NA — when it can happen (SPEC §4; HQ: qualifier KEPT; to re-check against Engineering's commit).**
(1) Status other than `completed` / `exact`: the fields are absent (NULL), and there is no output — not an NA case.
(2) Exact branch: NA iff the implementation does not return the enumeration's store. At the pin the store is returned
(`fit$exact <- e` with `e$top`, `v3_fit.R:122`, `cpp/v3_core.cpp:565`); IMPL-LIST changes no other field, so it stays
returned — NA only if the commit fails to compute `log_Z_list` from `fit$exact$top`.
(3) `completed` with an empty list: SPEC sets NA + flag; cannot occur (LIST-CODE (iii): 𝒯 ∋ the HPM-order maximum of
the nonempty offered set). (4) Non-finite score: NA + flag; cannot occur under EX-A (scores finite, Lemma S.2); binary64
only, out of scope. Hence under EX-A + IMPL-LIST, `log_Z_list` is never NA on an output run if the commit computes it
from the exact store; under (D) every run outputs, so never NA on the delivery event. Check at the commit: (a) the
exact-branch path computes `log_Z_list` from `fit$exact$top`; (b) no other NA path. Then dropping the qualifier is a
STRONGER statement change with a statement-change check (HQ approval).

**Card text** `CARD.md` v0.3: Option A (recommended) new row 3.1L "Corollary 6L"; Option B a sentence in row 3.6; both
council-checked (R3 faithfulness PASS); E2 of ERRATA is one wording fix in Option B. **Reader text** `READER_DELTA.md` v0.2
(Corollary 6L under Theorem 6). **Proposals for HQ (not claimed):** Corollary 9C's list premise on designs inside both
Theorem 9 and Theorem 6 (`STATEMENT.md` §5 remark 3); dropping the NA qualifier (above; TARGET §4).
**Method pin.** LIST-CODE: core 4676af6 (= main 029bb748). LIST-R: method_commit **pending** (Engineering, D105); at the
commit, a code reading discharges IMPL-LIST (manager: premise discharge, not a new council).

**API blind-audit card D5P1** `reviews/api_card/` (README, SYSTEM, REQ_d5p, requests.json, REQUESTS.tsv, MANIFEST.tsv,
USAGE.txt, SCRUB_LOG.tsv; builder `d5p_card_build.py`), built at the passing commit a2c465a4: Fable 5.2, effort high,
2 samples, "Break the proof; findings only", 9 verdict lines `AUDIT D5P1 <claim> VERDICT=…`; no status words (builder
fails otherwise); ≈ $1.0 expected, ≤ $1.7 worst case. For HQ to count/submit with `API_AUDIT/audit_batch.py`.

**Budget.** Started 11-17 12:38 CST; CP3 the same day (≈ 0.4 of the 3-day kill budget).

# W3-D3 — CHECKPOINT 3 (hard; 2026-11-17; lead Claude Opus 5.5 high) — recording package for the manager

Tier B, NORMAL mode. Codex reviews used: 2 (L1 lock, R1 Sol seat), one at a time. Claude reviews: K1 line check, K2, K3
re-checks, R1 Opus seat, R2 diff round, F1 form check — all Opus 5.5 high on providerInstanceId claudeAgent_personal.
HOLDS.md (origin/main 9f939e8a): 0 HOLD lines. Consumed inputs unchanged between 029bb748 and origin/main 9f939e8a (all 12
external input files and claims.tsv rows); consumed claims ACTIVE: `W3-POST:Thm-1@1.0.1`, `W3-DIST:B0/B1/B2core/B2/B3@1.0.1`,
`W3-READER:R1@1.0.2`, statuses as quoted in STATEMENT §6. Kill point never reached; no new probability theory (owner
condition D105/D112: W3-DIST's bridge reused at every Gaussian step). Elapsed: about 1 hour of the 3-day budget.

## Passing round
- **R2 (diff round after R1; Opus-only per the ticket)**: seat review `reviews/R2_council_opus.md`, ACCEPT ×3, score 9.3, all
  gates PASS, on MANIFEST f559960469015b9c993e17cc82b3955ceee2890db189b8ae23e2aa2f1f4840a6 (`reviews/R2_bind.txt`: bind OK).
- **FORM-ONLY re-freeze R2f** (DEPS.tsv only: five rows re-verified by the R2 seat now name it as their check): form check
  `reviews/F1_formcheck_opus.md` **FORM-ONLY**; carrier `reviews/R2f_record_opus.md` → `reviews/R2f_bind.txt`: **bind: OK**,
  council cell `R2; MANIFEST c52866ef738795c479b2853ec386d193df7069698fe4e6a20d8a4f66e567a5d3; opus=9.3 PASS(reviews/R2f_record_opus.md)`.
  **Binding manifest: `reviews/MANIFEST_R2f.txt` = MANIFEST c52866ef738795c479b2853ec386d193df7069698fe4e6a20d8a4f66e567a5d3**;
  `manifest.py verify`: OK (final tree).
- R1 (MANIFEST de19cf54…): Sol 8.5 gates=FAIL, Opus 8.8 gates=FAIL — both ACCEPT all three claims; both FAIL on the same S1
  in prose outside the claim spans (card/REPORT/READER_DELTA dropped the centring and common-constant qualifiers). Resolved
  (R2 seat: all R1 findings RESOLVED). **Note for HQ:** the passing round has no OpenAI seat (ticket rule: diff rounds
  Opus-only); the Sol seat's last verdict is R1 FAIL on S1 (prose), with all three claims ACCEPT. A short Sol continuation on
  the R2 diff would add the OpenAI seat if HQ wants it (not run).

## Record state
- DEPS: 10 rows, all OK. citecheck: `reviews/CITECHECK.txt`, 70 checks, 0 failures.
- Staged ingest (`reviews/INGEST_staged.txt`): 3 claims, 2 new assumptions (A:POP-FLOOR-5LOG, A:SUBG-SPARSE-ROWS — the
  latter a variant of A:DIST-A3 on Theorem 2's window), **0 problems**, 0 ERROR, acceptance (W3-D3:B3w, W3-D3:ExSG,
  W3-D3:Thm2SG) **PASS**.
- Chain: L1 lock (Sol) LOCK-WITH-AMENDMENTS → K1 (Opus, blind) VERIFIED-WITH-AMENDMENTS (incl. statement-change check of
  ExSG (b), D114) → K2, K3 re-checks → R1 council → R2 diff round → F1 form check. Dispositions in `reviews/`.
- REPORT §4 still reads "Council: (filled at CP3)": REPORT is inside the frozen manifest; this checkpoint is the council record.

## Per-claim statuses (proposed; the recorder computes the final label)
- `W3-D3:Thm2SG` (STATEMENT.md:41-57): "PROVED (by this seat, unchecked)" (`lemmas/ASSEMBLY.md:3`) + council R2 above.
- `W3-D3:B3w` (STATEMENT.md:59-80): "PROVED (by this seat, unchecked)" (`lemmas/B3w.md:3`) + council R2.
- `W3-D3:ExSG` (STATEMENT.md:82-90): "PROVED (by this seat, unchecked)" (`lemmas/ASSEMBLY.md:3`) + council R2.
- Inputs all PROVED-CHECKED (STATEMENT §6), so no inherited condition. Registry blocks: REPORT.md §6 (:64-91).
  implies: none (Thm2SG gives row 1.2's reader conclusions on a larger class; conclusion-level note, not an edge to W2-APP:POST).

## For HQ / the card
- **Row 1.2 COEXIST**: card text REPORT §3 (added sentence under row 1.2; row 1.2 unchanged and stays clean); mark of the added
  sentence: clean once the three claims are recorded PROVED-CHECKED.
- Tag vs row 1.2 reader statement: **STRONGER** (Gaussian rows → (A4), L = 1 for Gaussian; (A1)–(A3) and conclusions verbatim).
  Against row 1.2's master: fixed floor kept (o2 OFF), SL1 extras not reproduced.
- **D109 class of (A4)**: class 1 per HQ ruling (D114) with the approved wording and the lead's two brackets (centred rows / L a
  fixed multiple for NH14; z = x − m_n for Song–Liang); 2b backup sentence (option A) with ExSG (b). Both sources quoted
  verbatim with pages (STATEMENT §5); NH14 from arXiv v1 pp. 16–17, journal version not checked.
- **API blind-audit card**: `API_CARD.md` + `api_request_build.py` + `reviews/API_CARD_README.md` (outside the manifest): final-tree
  build under `unshare -rn` (no API call); drops only status-quotation lines (B3w.md:44-45, ASSEMBLY.md:9-10, W3-POST
  STATEMENT 78, 90); 0 status words; requests.json sha256 prefix 3491251a14d8b09c; build manifest `reviews/API_build_MANIFEST.txt`.
- Better-theorem proposals (not adopted; HQ OFF): smaller window 3(A+1)(s₀+1) log n (o1); floor of order 1/n on the window (o2);
  explicit failure probability (R1 Opus seat).
- Errata after the freeze: none.

## Post-CP3 addendum (2026-11-17): H5 card 17 and FORM-ONLY re-freeze R2g
- H5 card 17 (consultant AGREE, binding): Thm2SG becomes the presented Theorem 2 once recorded and API-clean; the class-1 anchor
  of (A4) is **Narisetty–He only**; the Song–Liang implication stays as a separate factual remark (centred rows).
- Applied: STATEMENT v1.4 §5 (outside the claim spans; changelog row 1.4 EQUAL), REPORT §2 and §3 card, READER_DELTA, TARGET
  class cell, PLAN supersession note; DEPS S:class re-hashed. No change in STATEMENT §§0–3, `lemmas/`, numerics, tools, inputs.
- Form check `reviews/F2_formcheck_opus.md` (Opus 5.5 high, claudeAgent_personal): **FORM-ONLY**; no remaining anchor sentence.
  Borderline sentence noted by the checker and kept (a statement of position, not an anchor): STATEMENT §5 residual bullet,
  "(A4) sits between NH14 (identity covariance) and Song–Liang's weaker Condition 1".
- **Binding manifest now R2g:** `reviews/MANIFEST_R2g.txt` = MANIFEST c41a5b3485d712770989cc3c82a621fe8f5690f976bb8bb0378a188efa40665f;
  carrier `reviews/R2g_record_opus.md` → `reviews/R2g_bind.txt`: **bind: OK**; council cell
  `R2; MANIFEST c41a5b3485d712770989cc3c82a621fe8f5690f976bb8bb0378a188efa40665f; opus=9.3 PASS(reviews/R2g_record_opus.md)`.
  verify OK; citecheck 70/0; staged ingest 0 problems, acceptance PASS. Registry blocks: REPORT.md §6 (:65-92; content unchanged).
- API request rebuilt under `unshare -rn`: identical (requests.json sha256 prefix 3491251a14d8b09c; STATEMENT §§0–4 unchanged).

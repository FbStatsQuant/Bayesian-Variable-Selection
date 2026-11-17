# W3-D2 — CHECKPOINT 3 (hard; 2026-11-17; lead Claude Opus 5.5 high) — recording package for the manager

Tier B, NORMAL mode (Codex level 1: one Codex job at a time; 2 Codex reviews used: L1 lock, R1 Sol seat). HOLDS.md
(origin/main 47639f0e): 0 HOLD lines. Consumed claims unchanged on origin/main: `W3-MISR-R:CorGb-plus@1.0.1`,
`W3-READER:R1@1.0.2`, both ACTIVE, statuses as quoted in STATEMENT §5. Kill point never reached; no new lemma.

## Passing round
- **R2 (= the diff round the lead's brief called "D1"; Opus-only per the ticket)**: manifest `reviews/MANIFEST_D1.txt` =
  `reviews/MANIFEST_R2.txt` (byte copy) = **MANIFEST f62740c74ee1740a4cfbbcd9d12e0c845dc8435fb0adde6e380ca9bda3469d2b**.
  Seat: Opus 5.5 high (claudeAgent_personal), `reviews/D1_council_opus.md`: Thm2X ACCEPT, Cor2X ACCEPT, all gates PASS, 9.6.
  All 10 R1 findings RESOLVED (Sol F1 confirmed independently at 100-digit precision; P5 checked on 56.8 M grid cases).
- **Bind:** `reviews/D1_bind.txt` REFUSED **on form only** (the brief asked for `round=D1`; the tool accepts `round=R<k>`: the
  lead's error). Draft HQ carrier `reviews/R2_record_opus.md` (CITATION-ONLY, verbatim table, round=R2, same digest):
  `reviews/R2_bind_draft.txt` → **bind: OK**, council cell
  `R2; MANIFEST f62740c7…; opus=9.6 PASS(reviews/R2_record_opus.md)`. **`reviews/R2_record_opus.md` is the binding carrier
  (round=R2).** The D1 → R2 relabel is **form only**: same manifest, same digest f62740c74ee1740a4cfbbcd9d12e0c845dc8435fb0adde6e380ca9bda3469d2b
  (`MANIFEST_R2.txt` is a byte copy of `MANIFEST_D1.txt`), the seat's table and score copied verbatim; nothing reviewed changed.
  (Manager proposes to HQ a D99-pattern Sol carrier, not a new Sol review.)
- `manifest.py verify` on MANIFEST_R2 / D1: OK (final tree).
- R1 (MANIFEST 6f8c05aa…): Sol 9.2 **gates=FAIL** (F1 numerics only; both claims ACCEPT), Opus 9.6 PASS (`reviews/R1_bind.txt`:
  REFUSED). **Note for HQ:** the passing round has no OpenAI seat (the ticket's "diff rounds Opus-only"); the Sol seat's last
  verdict is R1 FAIL on F1, resolved per the D1 seat. If HQ wants the OpenAI seat on the passing manifest, one short Sol
  continuation on F1 + the diff suffices (Codex; not run).

## Record state
- DEPS: 11 rows, all OK (5 rows name the D1 review as their check; the D1 seat recomputed all 11 hashes).
- citecheck: `reviews/CITECHECK.txt`, 74 checks, 0 failures.
- Staged ingest (`reviews/INGEST_staged.txt`): 2 claims, 2 new assumptions (A:CORR-FLOOR-LOG, A:POP-SNR), **0 problems**,
  0 ERROR, acceptance (W3-D2:Thm2X, W3-D2:Cor2X) **PASS**.
- Reviews and their models: L1 lock Sol (gpt-6.1-sol high); K1 line check, K2, K3 re-checks, R1 Opus seat: Opus 5.5 high on
  claude_third; R1 Sol seat: Sol; D1/R2 Opus seat: Opus 5.5 high on claudeAgent_personal (manager's account check).

## Per-claim statuses (proposed; the recorder computes the final label)
- `W3-D2:Thm2X` (STATEMENT.md:29-48): "PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1,
  W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P" (PROOF.md:3) + council R2 above.
- `W3-D2:Cor2X` (STATEMENT.md:50-58): same.
- Registry blocks: REPORT.md §6 (:61-…). implies: none (Cor2X ⇒ row 1.2's reader statement is a conclusion-level note).

## For HQ / the card (decisions already taken)
- Row 1.2 **COEXIST**: card text REPORT §3 (added sentence under row 1.2, conditional mark; row 1.2 stays clean).
- Tag vs row 1.2 reader statement: **STRONGER** (floor at most 3(A+1)(s₀+1) log n vs 5(…); relative signal; expectation rates).
  Caveat (a): conditional status incl. Prop-LB (unchecked) and two wave-1 inputs (C-MIS:GDb, C-MIS:Prop-P). Caveat (b):
  Theorem 2X's own floor is stronger than LSF on the floor (k̄_n ≤ 3(…) log n, PROOF P5); the two masters are incomparable.
- X2 estimate: REPORT §3a (Tier B, ≈ 2–3 h + one Sol review; alone it does not make Thm2X clean).
- API blind-audit card: `API_CARD.md` + `api_request_build.py` + **`reviews/API_CARD_README.md`** (outside the frozen manifest;
  supersedes API_CARD.md:12-13): the final-tree build drops exactly PROOF.md:1 (version header), :3 (status line) and :97
  (P5's pointer to a review), and nothing else; no status words in the request; built under `unshare -rn` (no network): no API
  call. Build manifest `reviews/API_build_MANIFEST.txt`; requests.json sha256 f54aef98….
- Errata after the freeze (not applied; manifest frozen): PROOF P5 cites `[R1] B2.1 (:38-40)`, the step is at `:36` (D1 seat).
- Better-theorem proposals (R1 Opus seat; not adopted): fixed-level beta-min branch; random intercept; ξ_q and sup_{T≠S₀}
  bounds; hypotheses only for large n.

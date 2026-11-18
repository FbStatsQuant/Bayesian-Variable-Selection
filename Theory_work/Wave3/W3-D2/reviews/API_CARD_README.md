# W3-D2 — API card README (supersedes API_CARD.md:12-13 on the dropped lines; 2026-11-17)

`API_CARD.md` is inside the passing council manifest (MANIFEST f62740c7…) and is not edited (PROTOCOL_v4 §5.9). Its
lines 12-13 ("0 lines dropped except PROOF.md:3") describe a build made before PROOF v1.3. **For the final tree the builder
drops exactly three PROOF lines, and nothing else:**

| PROOF.md line | content | why dropped |
|---|---|---|
| 1 | file header (version history: "council R1 editorial", review file names) | carries a status/review word ("council"); version history, no mathematics |
| 3 | status line "PROVED (by this seat, unchecked), conditional on …" | status words (blind request) |
| 97 | P5's last line: "Numerical cross-check: council R1 Opus seat, … (`reviews/R1_council_opus.md`)" | points to a review (blind request); the P5 argument above it (:84-96) is complete without it |

No other source line is dropped (every other source shows `dropped(status words): []`). Build of record:
`python3 Theory_work/Wave3/W3-D2/api_request_build.py <outdir>` run under `unshare -rn` (no network namespace) on the
final tree: it completed and wrote `requests.json` (46 937 chars of user content; sha256
f54aef989bb2e496a8c714007be29443df64a7f54cc1ac3e917981e424f919e0) and `MANIFEST.txt` (copied here as
`reviews/API_build_MANIFEST.txt`). The request text contains none of PROVED, CHECKED, council, PASS, unchecked, VERIFIED,
MANIFEST. **No API call** is made by the builder (imports: hashlib, json, re, sys, pathlib only; it ran without network).
HQ submits with its own flow; everything else in `API_CARD.md` stands.

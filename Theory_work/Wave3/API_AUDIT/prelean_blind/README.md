# Pre-Lean BLIND API batch (builder output; HQ submits) — 2026-11-18

**What.** 6 targets × N = 2 independent samples = **12 Message Batches requests** for `claude-fable-5-2` ("break the proofs: find a genuine error or say none, file:line evidence; `AUDIT <id> FINDINGS=<k>`"), pattern of `W3-D3/api_request_build.py` + `API_AUDIT/audit_batch.py`. Built from **origin/main ad29c22e** (the pre-Lean correction batch has not landed). No API call was made.
**Rebuild (one command, from the worktree root, on a checkout of main).** `python3 Theory_work/Wave3/API_AUDIT/prelean_blind/prelean_blind_build.py --no-notes` rewrites all 12 requests, `BUILD_MANIFEST.txt` and `TOKENS.tsv` from the checked-out tree with **no** pending-corrections note (use it once the correction batch has landed); without the flag the notes of this build are included. Source line spans are hard-coded in `TARGETS` (the CORRECTIONS rows keep line counts unchanged); registry spans are read from `claims.tsv`; check the dropped-line lists in `BUILD_MANIFEST.txt` after a rebuild.
**Files.** `requests/PB-Tk-s{1,2}.jsonl` (one `{"custom_id","params"}` per file); `python3 prelean_blind_build.py` rebuilds them and writes `requests.json` (all 12, git-ignored; `audit_batch.py submit`-compatible list), `BUILD_MANIFEST.txt` (sha256 + last-touch commit + line span + dropped line numbers per source), `TOKENS.tsv`.
**Params (HQ to confirm).** model `claude-fable-5-2`, `output_config.effort = high`, `max_tokens` 64 000 (as `audit_batch.py`; the D3 builder left effort to HQ). The two samples of a target are byte-identical except `custom_id`.

## Per-request size (est. input tokens = chars / 3.5, system prompt included; pessimistic = chars / 2.5 for the unicode-heavy math)
| target | claims audited (closing `AUDIT` lines) | chars | est. tokens | pessimistic |
|---|---|---|---|---|
| PB-T1 | W3-PSHARP:B (Thm 3(a)) | 23 517 | 6 719 | 9 407 |
| PB-T3 | W3-DIST:H, W3-POST2:D0, W3-DIST:P6, W3-DIST:DIST-C, W3-DIST:Cor-C | 107 895 | 30 827 | 43 158 |
| PB-T4 | W3-POST2:C, W3-POST2:E, W3-D3:Thm2SG, :B3w, :ExSG | 106 358 | 30 388 | 42 543 |
| PB-T5 | W3-DIST:Thm-A, Thm-B, Cor-C (Thm 9, 9B, Cor 9C) | 320 076 | 91 450 | 128 030 |
| PB-T8 | W3-RM2-R:RM2-F-plus, RM0-plus, DLV-0 (Thm 7) | 105 339 | 30 097 | 42 136 |
| PB-T9 | W3-READER:R4 (Thm 10) | 43 801 | 12 515 | 17 520 |
| **per sample** | | 706 986 | **201 996** | 282 794 |
| **12 requests** | | 1 413 972 | **403 992** | 565 589 |
Every request is far below the 150k cap (largest: PB-T5 ≈ 91k, ≤ 128k pessimistic). **Nothing was split.**

## Content of a request (self-contained)
Target line, the claim ids, the "Known pending corrections" note, then numbered sections (`NNNN| ` = original line number of the named file, so findings cite file:line): the STATEMENT spans, the **full proof files**, and the **statements** (not proofs) of the consumed results, taken from `claims.tsv` spans (premises, notation, cited lemma statements). Short consumed proofs that the argument needs are included in full (CC_code_check for the output description; RM0-plus is the proof file of the target itself). Source list per target = `TARGETS` in `prelean_blind_build.py`.
**Blindness.** The script reads no review, council file, disposition, CHECKPOINT, LOG, CODEX_*, FABLE_CARD, PRE_LEAN_PASS file, earlier API result, ERRATA or CORRECTIONS file; the pending-correction lines are typed into the script. Inside source lines, status quotations (`"PROVED-CHECKED; council …"`), review tags (`[K01-F3]`, `[S2-04]` …) and review-process phrases ("after the cross-family line check", "(this stream, DRAFT)") are redacted; a line that still carries a status/review word is dropped. A scan of all 12 requests for PROVED, CHECKED, VERIFIED, council, MANIFEST, review, Opus, Astra, Sol, Fable, CODEX, CHECKPOINT, ERRATA, disposition, PRE_LEAN, API_AUDIT, reviews/, `[REG-`, HQ: **0 hits** outside the instruction header. 71 hand patches (`PATCHES`) remove only status wording and keep the line's mathematics; every dropped line number is in `BUILD_MANIFEST.txt`.
**Status policy.** As in auditD3, consumed results are marked "taken as true as stated" in the system prompt and their registry statuses are **not** quoted (a quoted `"PROVED-CHECKED; council …"` is review output). Conditionality that is a mathematical premise stays in the text (e.g. Theorem B's "conditional on W3-POST Theorem 1", EX-A, DLV audits "taken as hypotheses"). If HQ wants the plain statuses back verbatim, that is a one-line change; I did not do it because of the blindness rule.

## Known pending corrections put in the requests (CORRECTIONS.md on `origin/theory/PRE-LEAN` cdb5f027, plus the deferred T4 R4; one line each, location + old → new; the ids are not in the packets)
- PB-T1: T1-1 (two places, `λ ≥ 0`). PB-T3: T3-1 (`P6_DISTC.md:70-72`).
- PB-T4: T4-R4 deferred (`W3-D3/STATEMENT.md:64-65`, `B3w.md:25`; CORRECTIONS.md gives these lines, not the card's :61-62), T4-R1 (`W3-POST/STATEMENT.md:86`), T4-N1 (`READER_VERSIONS.md:109, 121-122`), T5-R3 (`E_bridges/B3.md:98-99`, the template).
- PB-T5: T3-1, T5-R3, T5-R1 (`W3-DIST/STATEMENT.md:96-97`), T5-R2 (`:78`), T5-R4 (`:151-152`), T5-R4-reader (`READER_VERSIONS.md:1065-1067`), T4-R1.
- PB-T8: T8-1 (`W3-RM2-R/STATEMENT.md:80-81`), T4-N1 (`READER_VERSIONS.md:824`, manager-ruled; the same fix at :885 is outside the packet). PB-T9: T8-2 (`W3-START2-R/STATEMENT.md:237`, inside the consumed span), T4-R1.
- Not listed because no packet contains the text: T8-1's other copies, the Sol/Sol4/Sol3 seat or dossier items, Sol2-S2-1/2/3, T5-R4's `CLAIMS_CARD` side. (The :824 phrase was ruled into the PB-T8 note by the manager.)
- This list was refreshed after the first build because CORRECTIONS.md grew (9 new rows) while I was building; the batch itself has not landed on main (still ad29c22e).

## Excluded / not packeted (for the manager)
- No review/card/walk material anywhere. Not included as proof text: `W3-DIST/lemmas/NEC.md` (sharpness, not a target clause), `X_route_a.md` (alternative route), `work/F_numerics`, API-attempt files, `REPORT*`, `ROUTES`, the §4 consumes table and changelog of `W3-DIST/STATEMENT.md`, the READER "Abstract forms of row 1.1" block (status bookkeeping), Claim D (Hellinger, in-sample) of W3-POST2.
- PB-T4 audits Thm 1 through `W3-POST2:C` / `:E` (their proofs are in the packet). The O_P form `W3-POST:Thm-1` has no proof file of its own: it is the T03♯ record, so its statement is packeted as a consumed result and is **not** an audited claim. Likewise SOP:TH09/TH128, W2-APP:POST and the C-PACK SL items are consumed statements only.
- PB-T8: DLV-0's two C-DLV code-reading audits, the C-DLV/C-GROW/W2-UNI/W3-RM statements it cites are packeted as statements (hypotheses), their proofs are not.
- PB-T9: the "Inputs (statuses verbatim)" section of `R4_printed_outputs.md` is cut (it quotes statuses); the inputs' statements come from their own files (W3-SAMP Theorem C, START-R/IF-START, W3-POST Thm 1, W2-APP:POST).
- Brief ambiguity: "registry statuses of inputs quoted verbatim" vs "no review … beyond what the statement carries"; I followed the D3 builder (statuses redacted).

# Pre-Lean BLIND API batch (builder output; HQ submits) — 2026-11-18

**What.** 6 targets × N = 2 independent samples = **12 Message Batches requests** for `claude-fable-5-2` ("break the proofs: find a genuine error or say none, file:line evidence; `AUDIT <id> FINDINGS=<k>`"), pattern of `W3-D3/api_request_build.py` + `API_AUDIT/audit_batch.py`. Built from **origin/main ad29c22e** (the pre-Lean correction batch has not landed). No API call was made.
**Files.** `requests/PB-Tk-s{1,2}.jsonl` (one `{"custom_id","params"}` per file); `python3 prelean_blind_build.py` rebuilds them and writes `requests.json` (all 12, git-ignored; `audit_batch.py submit`-compatible list), `BUILD_MANIFEST.txt` (sha256 + last-touch commit + line span + dropped line numbers per source), `TOKENS.tsv`.
**Params (HQ to confirm).** model `claude-fable-5-2`, `output_config.effort = high`, `max_tokens` 64 000 (as `audit_batch.py`; the D3 builder left effort to HQ). The two samples of a target are byte-identical except `custom_id`.

## Per-request size (est. input tokens = chars / 3.5, system prompt included; pessimistic = chars / 2.5 for the unicode-heavy math)
| target | claims audited (closing `AUDIT` lines) | chars | est. tokens | pessimistic |
|---|---|---|---|---|
| PB-T1 | W3-PSHARP:B (Thm 3(a)) | 23 517 | 6 719 | 9 407 |
| PB-T3 | W3-DIST:H, W3-POST2:D0, W3-DIST:P6, W3-DIST:DIST-C, W3-DIST:Cor-C | 107 539 | 30 725 | 43 016 |
| PB-T4 | W3-POST2:C, W3-POST2:E, W3-D3:Thm2SG, :B3w, :ExSG | 105 463 | 30 132 | 42 185 |
| PB-T5 | W3-DIST:Thm-A, Thm-B, Cor-C (Thm 9, 9B, Cor 9C) | 318 047 | 90 871 | 127 219 |
| PB-T8 | W3-RM2-R:RM2-F-plus, RM0-plus, DLV-0 (Thm 7) | 105 193 | 30 055 | 42 077 |
| PB-T9 | W3-READER:R4 (Thm 10) | 43 619 | 12 463 | 17 448 |
| **per sample** | | 703 378 | **200 965** | 281 351 |
| **12 requests** | | 1 406 756 | **401 930** | 562 702 |
Every request is far below the 150k cap (largest: PB-T5 ≈ 91k, ≤ 127k pessimistic). **Nothing was split.**

## Content of a request (self-contained)
Target line, the claim ids, the "Known pending corrections" note, then numbered sections (`NNNN| ` = original line number of the named file, so findings cite file:line): the STATEMENT spans, the **full proof files**, and the **statements** (not proofs) of the consumed results, taken from `claims.tsv` spans (premises, notation, cited lemma statements). Short consumed proofs that the argument needs are included in full (CC_code_check for the output description; RM0-plus is the proof file of the target itself). Source list per target = `TARGETS` in `prelean_blind_build.py`.
**Blindness.** The script reads no review, council file, disposition, CHECKPOINT, LOG, CODEX_*, FABLE_CARD, PRE_LEAN_PASS file, earlier API result, ERRATA or CORRECTIONS file; the pending-correction lines are typed into the script. Inside source lines, status quotations (`"PROVED-CHECKED; council …"`), review tags (`[K01-F3]`, `[S2-04]` …) and review-process phrases ("after the cross-family line check", "(this stream, DRAFT)") are redacted; a line that still carries a status/review word is dropped. A scan of all 12 requests for PROVED, CHECKED, VERIFIED, council, MANIFEST, review, Opus, Astra, Sol, Fable, CODEX, CHECKPOINT, ERRATA, disposition, PRE_LEAN, API_AUDIT, reviews/, `[REG-`, HQ: **0 hits** outside the instruction header. 71 hand patches (`PATCHES`) remove only status wording and keep the line's mathematics; every dropped line number is in `BUILD_MANIFEST.txt`.
**Status policy.** As in auditD3, consumed results are marked "taken as true as stated" in the system prompt and their registry statuses are **not** quoted (a quoted `"PROVED-CHECKED; council …"` is review output). Conditionality that is a mathematical premise stays in the text (e.g. Theorem B's "conditional on W3-POST Theorem 1", EX-A, DLV audits "taken as hypotheses"). If HQ wants the plain statuses back verbatim, that is a one-line change; I did not do it because of the blindness rule.

## Known pending corrections put in the requests (from `origin/theory/PRE-LEAN` CORRECTIONS.md, one line each, old → new)
- PB-T1: T1-1 (two places, `λ ≥ 0`). PB-T4: T4 R4 (deferred; `W3-D3/STATEMENT.md:61-62`, `B3w.md:24`). PB-T8: T8-1 (`W3-RM2-R/STATEMENT.md:80-81`). PB-T9: T8-2 (pending; `W3-START2-R/STATEMENT.md:237` lies in the consumed START-R span). PB-T3, PB-T5: "none".
- T8-1's other copies (READER carrier file, registry `A:IDEAL-W+` row) are not in any packet. Sol1/Sol3 seat additions are bookkeeping, not text.

## Excluded / not packeted (for the manager)
- No review/card/walk material anywhere. Not included as proof text: `W3-DIST/lemmas/NEC.md` (sharpness, not a target clause), `X_route_a.md` (alternative route), `work/F_numerics`, API-attempt files, `REPORT*`, `ROUTES`, the §4 consumes table and changelog of `W3-DIST/STATEMENT.md`, the READER "Abstract forms of row 1.1" block (status bookkeeping), Claim D (Hellinger, in-sample) of W3-POST2.
- PB-T4 audits Thm 1 through `W3-POST2:C` / `:E` (their proofs are in the packet). The O_P form `W3-POST:Thm-1` has no proof file of its own: it is the T03♯ record, so its statement is packeted as a consumed result and is **not** an audited claim. Likewise SOP:TH09/TH128, W2-APP:POST and the C-PACK SL items are consumed statements only.
- PB-T8: DLV-0's two C-DLV code-reading audits, the C-DLV/C-GROW/W2-UNI/W3-RM statements it cites are packeted as statements (hypotheses), their proofs are not.
- PB-T9: the "Inputs (statuses verbatim)" section of `R4_printed_outputs.md` is cut (it quotes statuses); the inputs' statements come from their own files (W3-SAMP Theorem C, START-R/IF-START, W3-POST Thm 1, W2-APP:POST).
- **Agreed-but-not-in-CORRECTIONS.md items that a blind reader may re-find (not added, manager's call):** T4 R1 (`W3-POST/STATEMENT.md:86`, item 4 `h:Ω→[0,1]`; inside PB-T4/T5/T9 text), T3-1 (`P6_DISTC.md:70-72`, positivity of m(S); PB-T3/T5), T5 R1–R4 (wording in W3-DIST STATEMENT; PB-T5).
- Brief ambiguity: "registry statuses of inputs quoted verbatim" vs "no review … beyond what the statement carries"; I followed the D3 builder (statuses redacted).

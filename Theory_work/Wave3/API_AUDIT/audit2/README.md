# AUDIT2 — blind Fable review of the v1.3 label changes (Song–Liang supplement)

**What it is.** A Message Batches card, prepared by Theory Dept (2026-11-16) for HQ to submit. W3-AUDIT `TRACK_B.md`
went v1.2 → v1.3 after Song–Liang's on-line supplement was read, and comparison labels changed. HQ's rule is that a
changed label gets a new blind API audit. Claude Fable 5.2, effort high, acts as a blind referee of **only what changed
in v1.3** (`theory/W3-AUDIT` @ f98cf498: `TRACK_B.md` §S, §T2 and the dossier lines they changed; `AUDIT.md` rows that
quote them; `WRITING_DELTA_v1.3.md`):

| item | what is tested | verdict ids |
|---|---|---|
| 1 | B4, coefficient size: "same as the setting of their proofs" (supp pp. 5, 15); "stronger than their statements" | `item1:B4.PROOFS`, `item1:B4.STATED` |
| 2 | B5 "not ordered" and B6 "weaker" against Theorem S ((22)–(23), supp p. 13) | `item2:B5.S`, `item2:B6.S` |
| 3 | sampler output: "a weaker counterpart" (supp pp. 12–13, 16–17); "nothing at a finite budget or jointly in n" | `item3:SAMP.LABEL`, `item3:SAMP.ABSENCE` |
| 4 | the new headline sentence (`WRITING_DELTA_v1.3.md:8-14`) | `item4:HEAD.ORDER`, `.S`, `.H`, `.CONC` |
| 5 | Theorem S against cores 1 and 3 (§S): the quotation, the label per row, "ours implies (24)", core 3 | `item5:S.QUOTE`, `S.MODEL`, `S.PRIOR`, `S.DIM`, `S.LOWER`, `S.UPPER`, `S.SIGNAL`, `S.CONC`, `S.CORE3` |

19 verdicts; one request, two independent samples (`audit2-s1`, `audit2-s2`; identical input; the shared context block
carries `cache_control`). No API call was made to prepare this card, and no key was read.

**Blindness.** As AUDIT1. The referee sees: (a) our theorem texts verbatim with file:line (reader versions
`W3-READER/READER_VERSIONS.md` @ 7eb818e6, the version the dossiers cite; master `W3-POST/STATEMENT.md` @ e8b5351c for
our posterior and Theorem 1's hypotheses); (b) the Song–Liang passages, main text and supplement, with page and display
numbers; (c) the audit sentences under test, verbatim (`AUDIT.md` rows: cells "Assumption" and "Song–Liang (2015)"
only). Status words are stripped by AUDIT1's rules (the builder fails if PROVED, CHECKED, council, PASS, VERIFIED,
AUDITCALC, Opus, Fable, Astra or "seat" survives). Clauses about our designs are declared not under test (the
inside/outside entries did not change in v1.3). Task text, verbatim: "Break the comparison; findings only." Each reply
ends with one line per verdict: `AUDIT2 <item>:<id> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>`.

**Files.**
- `SYSTEM.md` — the system prompt (AUDIT1's, narrowed to the changed labels; adds "one posterior against another" and
  "limits in n against limits in the number of sampler iterations" to the error list).
- `REQ_audit2.md` — the exact user message: the context block, then the task block.
- `requests.json` — the batch (audit_batch.py shape: `custom_id`, `file`, `claims`, `params`; `submit` sends only
  `custom_id` + `params`). Model `claude-fable-5-2`, `output_config: {effort: "high"}`, `max_tokens` 32000.
- `REQUESTS.tsv` — custom_id → verdict ids. `MANIFEST.tsv` — sha256 of every source at its commit (git blobs via
  `git show`); both Song–Liang PDFs are hashed, not copied (main `315c247c…`, supplement `a584b328…`, as cited in
  `TRACK_B.md:39-40`).
- `USAGE.txt` — offline token/cost estimate (overwritten by `wait` with billed usage).
- Builder: `../audit2_build.py` (`build` regenerates everything byte-identically while the pins hold; it loads AUDIT1's
  main-text transcriptions from `audit1_build.py` @ 37935108 rather than retyping them).

## How HQ submits (same commands as audit_batch.py; run from the repo root)

```
python Theory_work/Wave3/API_AUDIT/audit_batch.py count  Theory_work/Wave3/API_AUDIT/audit2   # free token count + cost
python Theory_work/Wave3/API_AUDIT/audit_batch.py submit Theory_work/Wave3/API_AUDIT/audit2   # writes batch_id.txt
python Theory_work/Wave3/API_AUDIT/audit_batch.py wait   Theory_work/Wave3/API_AUDIT/audit2   # results/, USAGE.txt
python Theory_work/Wave3/API_AUDIT/audit2_build.py verdicts                                   # AUDIT2_VERDICTS.tsv
```

`wait` collects only lines starting `AUDIT ` / `SHARP ` into `VERDICTS.tsv`, so for this card that file will hold only
non-`end_turn` stops; the last command parses the `AUDIT2 …` lines from `results/*.md` into `AUDIT2_VERDICTS.tsv` and
marks any expected verdict that is missing.

## Cost (estimate)

Offline estimate (characters / 3.5; HQ's `count` gives the exact input): input ≈ 23k tokens per request, ≈ 46k for both
→ $0.18 at the Fable 5.2 batch rate ($4 / MTok in, $20 / MTok out). Output expected ≈ 16k tokens per request → $0.64;
worst case (both at max_tokens 32000) $1.28. **Total ≈ $0.8 expected, ≤ $1.5 worst case** — inside HQ's ≈ $5 scope.

## How results map back

| verdict id | audit lines under test |
|---|---|
| item1:B4.PROOFS, B4.STATED | `TRACK_B.md:101-108`, `:298`, `:383`; `AUDIT.md:49`, `:83`; `WRITING_DELTA_v1.3.md:17-19` |
| item2:B5.S | `TRACK_B.md:129-132`, `:299`, `:384`; `AUDIT.md:47`; `WRITING_DELTA_v1.3.md:20-22` |
| item2:B6.S | `TRACK_B.md:154-156`, `:300`, `:385`; `AUDIT.md:48` |
| item3:SAMP.LABEL, SAMP.ABSENCE | `TRACK_B.md:367-374`, `:226-229`, `:389`; `AUDIT.md:71`; `WRITING_DELTA_v1.3.md:26-29` |
| item4:HEAD.* | `WRITING_DELTA_v1.3.md:8-13` (same answer: `TRACK_B.md:14-24`, `:308-312`; `AUDIT.md` one-paragraph answer) |
| item5:S.QUOTE | `TRACK_B.md:342-353` |
| item5:S.MODEL … S.CONC | `TRACK_B.md:359-365` (S.DIM also `:80-82`; S.CONC also `:24`, `AUDIT.md:52`, `WRITING_DELTA_v1.3.md:23-25`) |
| item5:S.CORE3 | `TRACK_B.md:375` |

A REFUTED or UNCLEAR line points at the rows above; the finding text in `results/<custom_id>.md` gives the reference.
Agreement between the two samples is the first filter (as in AUDIT1 and t03acc).

## Limits of the card (read before trusting a NO-FINDING)

- **Song–Liang passages are transcribed from the page images** (marked "[transcribed from … image]"; `pdftotext`
  drops ≺, ≻, ≠, ε and sub/superscripts). Supplement pages read as images at 110 dpi: 1, 5, 6, 9, 10, 12–17; re-read
  at 200 dpi: the end of the proof of Theorem 2.3 (supp p. 5) and the noncentrality display (supp p. 15); main-text (7)
  (p. 951) re-read at 220 dpi. Printed slips are kept and marked "[as printed]" (supp p. 10 "as n → ∞" for the
  iteration index; supp p. 13 "if V_ξ = I"; supp p. 15 "n l c²" and "n l, n l′" without subscripts). Omissions are
  marked "…"; no passage was paraphrased. Main-text passages are AUDIT1's transcriptions, reused unchanged.
- The supplement names the main-text results "Theorem 2.1–2.4" and uses conditions (A₁), (A₂), (B₁) without defining
  them; the request says so in a preparer's note and identifies Theorem 2.3 = main Theorem 3 and (B₁) = Condition 3
  by content. The note also states which pages hold sampler statements (text search for "converg"/"consisten" over all
  20 pages, each hit read), which is what the absence claim SAMP.ABSENCE is judged against.
- Reader versions are read at 7eb818e6 (the commit the audit cites, "READER pre-freeze"), as in AUDIT1.

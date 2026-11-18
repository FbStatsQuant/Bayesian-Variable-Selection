# AUDIT1 — blind Fable review of W3-AUDIT's Song–Liang comparisons (cores 1–3)

**What it is.** A Message Batches card, prepared by Theory Dept (2026-11-16) for HQ to submit. Claude Fable 5.2,
effort high, acts as a blind referee of the **Song–Liang comparisons** and the **inside/outside design verdicts** of
`W3-AUDIT` v1.1 (`TRACK_B.md` dossiers B1–B10, B12 and the summary table; the per-core tables of `AUDIT.md`;
`track_C/RESULTS.md` as evidence) for core theorems 1–3:

| request | rows | theorems | verdicts |
|---|---|---|---|
| `audit1-core1-s1`, `-s2` | 1.1, 1.2, 1.3 | Thm 1, 1′, 2, 3 (posterior finds the model; the rate) | 20 |
| `audit1-core2-s1`, `-s2` | 2.1 | Thm 9, 9B, Cor 9C (posterior finds the distribution) | 18 |
| `audit1-core3-s1`, `-s2` | 3.1 | Thm 6 (coded method reports the model) | 17 |

Two independent samples per core (identical input; the shared context block carries `cache_control`). No API call was
made to prepare this card, and no key was read.

**Blindness.** The referee sees, per item: (a) our assumption text, verbatim with file:line (reader version
`W3-READER/READER_VERSIONS.md` @ 7eb818e6, which is what the dossiers compare, and the master `STATEMENT.md` lines of
this branch @ e8b5351c); (b) the matching Song–Liang passages, with journal page and display/condition number; (c) the
verdict under test, quoted from `TRACK_B.md` (the **Verdict** line and the summary-table row) and `AUDIT.md` (only the
cells "Assumption" and "Song–Liang (2015)" of each table row); (d) the track C line(s), where one exists. The
dossiers' Evidence / Holds / Designs reasoning, the "Status or dossier" column, review records and status words are
withheld; the builder fails if any of PROVED, CHECKED, council, PASS, VERIFIED, AUDITCALC, Opus, Fable, Astra or "seat"
survives in an excerpt. Task text, verbatim: "Break the comparison; findings only." Each reply ends with one line per
verdict: `AUDIT1 <core>:<item> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>`.

**Files.**
- `SYSTEM.md` — the system prompt (all six requests).
- `REQ_core1.md`, `REQ_core2.md`, `REQ_core3.md` — the exact user message: the context block, then the task block.
- `requests.json` — the batch (audit_batch.py shape: `custom_id`, `file`, `claims`, `params`; `submit` sends only
  `custom_id` + `params`). Model `claude-fable-5-2`, `output_config: {effort: "high"}`, `max_tokens` 32000.
- `REQUESTS.tsv` — custom_id → core, rows, verdict ids. `MANIFEST.tsv` — sha256 of every source at its commit (git
  blobs via `git show`; the 1M plan is an untracked file; the Song–Liang PDF is hashed, not copied).
- `USAGE.txt` — offline token/cost estimate (overwritten by `wait` with billed usage).
- Builder: `../audit1_build.py` (`build` regenerates everything byte-identically while the pins hold).

## How HQ submits (same commands as audit_batch.py; run from the repo root)

```
python Theory_work/Wave3/API_AUDIT/audit_batch.py count  Theory_work/Wave3/API_AUDIT/audit1   # free token count + cost
python Theory_work/Wave3/API_AUDIT/audit_batch.py submit Theory_work/Wave3/API_AUDIT/audit1   # writes batch_id.txt
python Theory_work/Wave3/API_AUDIT/audit_batch.py wait   Theory_work/Wave3/API_AUDIT/audit1   # results/, USAGE.txt
python Theory_work/Wave3/API_AUDIT/audit1_build.py verdicts                                   # AUDIT1_VERDICTS.tsv
```

`wait` collects only lines starting `AUDIT ` / `SHARP ` into `VERDICTS.tsv`, so for this card that file will hold only
non-`end_turn` stops; the last command parses the `AUDIT1 …` lines from `results/*.md` into `AUDIT1_VERDICTS.tsv` and
marks any expected verdict that is missing.

## Cost (estimate)

Offline estimate (characters / 3.5; HQ's `count` gives the exact input): input ≈ 26.7k / 23.2k / 19.6k tokens per
request for cores 1 / 2 / 3, ≈ 139k for all six → $0.56 at the Fable 5.2 batch rate ($4 / MTok in, $20 / MTok out).
Output expected ≈ 16k tokens per request → $1.92; worst case (every request at max_tokens 32000) $3.84.
**Total ≈ $2.5 expected, ≤ $4.4 worst case** — well inside the $30 budget, so 2 samples per core.

## How results map back to the dossiers

Verdict ids are `<core>:<item>.<kind>`: `.SL` = the comparison with Song–Liang; `.IO` = the inside/outside row of the
summary table (`TRACK_B.md:242-255`) for that assumption; `.LEMMA` = an implication the audit proposes as a lemma
(`AUDIT.md:181-183`).

| verdict id | dossier / audit line under test |
|---|---|
| core1:B1.SL/.IO, core2:B1.*, core3:B1.SL | B1 (`TRACK_B.md:63`, `:244`; `AUDIT.md:36`, `:58`, `:76`) |
| core1:B2.*, core2:B2.*, core3:B2.SL | B2 (`TRACK_B.md:69-70`, `:245`; `AUDIT.md:37`, `:59`) |
| core1:B3.*, core2:B3.*, core3:A2.* | B3 (`TRACK_B.md:78-79`, `:246`; `AUDIT.md:39`, `:59`, `:77`) |
| core1:B4-UP.SL, B4-LO.SL, B4.IO; core2:B4.*; core3:A2.* | B4 (`TRACK_B.md:89-92`, `:247`; `AUDIT.md:40`, `:43`, `:62`) |
| core1:B5.*, core3:B5.SL, core3:A5.IO | B5 (`TRACK_B.md:101`, `:248`; `AUDIT.md:41`, `:80` first part) |
| core1:B6.*, core2:B6.* | B6 (`TRACK_B.md:125-126`, `:249`; `AUDIT.md:42`, `:61`) |
| core1:B7.*, core2:B7.SL/.IO, core3:B7.* | B7 (`TRACK_B.md:140`, `:250`; `AUDIT.md:44`, `:60`, `:76`) |
| core2:B7.LEMMA | the proposed lemma "Thm 9 (A3) ⇒ Condition 1, δ = √(3/8)/L, M = log 2" (`AUDIT.md:181-182`) |
| core3:B8.SL/.IO | B8 (`TRACK_B.md:155-156`, `:251`; `AUDIT.md:78`) |
| core3:B8.LEMMA | the proposed lemma "Thm 6 (A3) ⇒ Condition 5" (`AUDIT.md:183`) |
| core3:B9.* | B9 (`TRACK_B.md:175`, `:252`; `AUDIT.md:79`) |
| core3:B10-FL.SL, core3:A6.* | B10 (`TRACK_B.md:199-200`, `:253`; `AUDIT.md:80` second part, `:81`) |
| core1:ROW13.SL | B12 and row 1.3 (`TRACK_B.md:235-236`, `:255`; `AUDIT.md:119-121`) |
| core1:DR.SL, SUM.SL, PRIOR.SL | `AUDIT.md:45`, `:46`, `:38` (Song–Liang column) |
| core2:A6-9B.*, H.SL, C9C.SL | `AUDIT.md:63`, `:64`, `:65` (Song–Liang column); A6-9B.IO reads B4/B5 rows `:247-248` |
| coreK:SCOPE.IO | core-level answer (`TRACK_B.md:14-20`, `:24-27`) |

A REFUTED or UNCLEAR line points at the dossier above; the finding text in `results/<custom_id>.md` gives the
reference. Agreement between the two samples of a core is the first filter (as in t03acc).

## Limits of the card (read before trusting a NO-FINDING)

- **Song–Liang passages are all transcribed from the page images** (marked "[transcribed from p. N image]"):
  `pdftotext -layout` drops ≺, ≻, ≠, ε and several sub/superscripts on every page used (e.g. it renders (4) as
  "1{β*_j = 0}" and Theorem 1's conditions without ε_n). Each passage was checked against the page image at 110 dpi;
  the displays of Theorem 1 (p. 952), Condition 3 (p. 955), Corollary 1 (p. 954), the stage priors (p. 959) and
  Corollary 2 (p. 957) were re-read at 200 dpi. No passage was paraphrased; omissions are marked "…".
- The supplement (proofs, Theorem S) is not available; absence claims ("no lower bound in SL", "SL prove nothing on
  their sampler's output", "no parametric-rate result") are judged against the main-text passages and an index of
  SL's formal results compiled by the preparer (labelled as such in the requests).
- Reader versions are read at 7eb818e6 (the commit the audit cites, "READER pre-freeze"); later READER commits
  (e.g. the W3-RM2-R swap of row 3.1) are not reflected. Master texts are read on dept/theory @ e8b5351c.
- `track_C/RESULTS.md` is read at 56dafbdd (identical to 4f0f9a82: Owls part only; NOTS cells pending).
- The 1M plan (`/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/EXPERIMENT_PLAN.md`) is untracked; its
  sha256 is in the manifest.

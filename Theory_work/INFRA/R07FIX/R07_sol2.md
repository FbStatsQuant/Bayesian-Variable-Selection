# R07 rule 2: independent table-reader correctness test

Result: two false-acceptance families and one false-refusal family. One additional NOTE groups human-readable forms outside the specified normalization/reader contract. Counts below include that NOTE: 4 findings, 2 MAJOR.

Scope: read only the requested INFRA-R07 worktree; imported its `bvsreg` using `python -B` and the exact tools path in the brief. No git commands, no git-state changes, no source edits, no subagents, no lifecycle-suite execution, no test/temporary files. The sole file written is this report. The withdrawn `R07_sol.md` was not consulted. These are direct function tests, not an end-to-end A4 verdict-validation test.

References: `tools/bvsreg.py` lines 1462?1571 (R07 comment and functions), the inherited strict reader at 1363?1459, header helpers at 1289?1295, and `LIFECYCLE.md` lines 309?322. Runtime: Python 3.15.2, Unicode database 17.0.0.

## Reproduction conventions

All results call `bvsreg.seat_table(text, "T")`. Strings below are Python ASCII-escaped reprs, so invisible separators, literal backslashes and Unicode characters are unambiguous. The return value is `(decisions, problems, number_of_tables)`. Shared fixtures:

```python
H = '| id | decision |\n|---|---|\n'
A = '\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
```

Unless stated otherwise, a body case is `H + "| C | " + value + " |" + A`. A valid addendum ACCEPT must leave `T:C` true except for a specified body negative. Full mismatch inputs and observed tuples follow each finding.

## 1. MAJOR ? separator splitting starts too late and loses body rows/headers

The written rule makes CR, VT, FF, FS/GS/RS, NEL and U+2028/U+2029 body-line boundaries. But `_body_scan` first loops over LF-only lines and detects a header before splitting those lines on `_ROW_BREAK`. When a header and its rows share one LF-delimited chunk, header detection succeeds and `continue` discards the remaining logical lines. Every listed separator reproduces an accepted `T:C` despite an explicit `reject` decision.

Expected: `T:C` false, contradiction diagnostic, two tables. Actual: `({'T:C': True}, [], 2)`. The correctly detected header makes this independent of disputed Markdown header variants. An ordinary introductory sentence followed by U+2028 and a valid header is also missed entirely (one table reported instead of two).

Likely repair location: lines 1520?1529. Split logical body lines before header detection, blank-line handling, and row handling. Preserve the unchanged strict R06 reader.

Exact tested inputs and outputs:

```text
separator '\r'
input = '| id | decision |\r|---|---|\r| C | reject |\r\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

separator '\x0b'
input = '| id | decision |\x0b|---|---|\x0b| C | reject |\x0b\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

separator '\x0c'
input = '| id | decision |\x0c|---|---|\x0c| C | reject |\x0c\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

separator '\x1c'
input = '| id | decision |\x1c|---|---|\x1c| C | reject |\x1c\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

separator '\x1d'
input = '| id | decision |\x1d|---|---|\x1d| C | reject |\x1d\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

separator '\x1e'
input = '| id | decision |\x1e|---|---|\x1e| C | reject |\x1e\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

separator '\x85'
input = '| id | decision |\x85|---|---|\x85| C | reject |\x85\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

separator '\u2028'
input = '| id | decision |\u2028|---|---|\u2028| C | reject |\u2028\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

separator '\u2029'
input = '| id | decision |\u2029|---|---|\u2029| C | reject |\u2029\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

input = 'Intro\u2028| id | decision |\n|---|---|\n| C | reject |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 1)
```

## 2. MAJOR ? documented dash normalization only covers a subset of Unicode dashes

The comment and lifecycle rule say dashes become spaces. `_BODY_SPACE` is a fixed list, however, so U+2E3A TWO-EM DASH, U+2E3B THREE-EM DASH and other Unicode `Pd` characters remain in `_neg_norm`. Consequently `not?accepted` is neither `not accepted` nor `notaccepted`, and the addendum ACCEPT survives.

Expected: `T:C` false after dash-to-space normalization. Actual for every case below: `({'T:C': True}, [], 2)`. Exhaustively tested all 27 Unicode-17 `Pd` characters: 12 caught, 15 missed. This finding uses the ordinary meaning of the written word ?dashes,? supported by the Unicode punctuation-dash category; the prose does not restrict it to `_BODY_SPACE`. If that finite list was intended as the entire contract, the prose needs to explicitly limit ?dashes?; the implemented finite-list behavior itself is consistent with that narrower interpretation. U+2E3A/U+2E3B make the mismatch clear without relying on visually exotic hyphens.

Exact missed inputs (all category `Pd`) and outputs:

```text
U+058A ARMENIAN HYPHEN
input = '| id | decision |\n|---|---|\n| C | not\u058aaccepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+05BE HEBREW PUNCTUATION MAQAF
input = '| id | decision |\n|---|---|\n| C | not\u05beaccepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+1400 CANADIAN SYLLABICS HYPHEN
input = '| id | decision |\n|---|---|\n| C | not\u1400accepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+1806 MONGOLIAN TODO SOFT HYPHEN
input = '| id | decision |\n|---|---|\n| C | not\u1806accepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+2E17 DOUBLE OBLIQUE HYPHEN
input = '| id | decision |\n|---|---|\n| C | not\u2e17accepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+2E1A HYPHEN WITH DIAERESIS
input = '| id | decision |\n|---|---|\n| C | not\u2e1aaccepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+2E3A TWO-EM DASH
input = '| id | decision |\n|---|---|\n| C | not\u2e3aaccepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+2E3B THREE-EM DASH
input = '| id | decision |\n|---|---|\n| C | not\u2e3baccepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+2E40 DOUBLE HYPHEN
input = '| id | decision |\n|---|---|\n| C | not\u2e40accepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+2E5D OBLIQUE HYPHEN
input = '| id | decision |\n|---|---|\n| C | not\u2e5daccepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+301C WAVE DASH
input = '| id | decision |\n|---|---|\n| C | not\u301caccepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+3030 WAVY DASH
input = '| id | decision |\n|---|---|\n| C | not\u3030accepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+30A0 KATAKANA-HIRAGANA DOUBLE HYPHEN
input = '| id | decision |\n|---|---|\n| C | not\u30a0accepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+10D6E GARAY HYPHEN
input = '| id | decision |\n|---|---|\n| C | not\U00010d6eaccepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

U+10EAD YEZIDI HYPHENATION MARK
input = '| id | decision |\n|---|---|\n| C | not\U00010eadaccepted |\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': True}, [], 2)

```
Caught Pd codepoints: U+002D, U+2010, U+2011, U+2012, U+2013, U+2014, U+2015, U+FE31, U+FE32, U+FE58, U+FE63, U+FF0D.

## 3. MINOR ? separator-created blank lines fail to end a body table

A blank logical body line must have the same effect whether represented by LF or one of the specified separators. In the LF control, the blank ends the table and later standalone `rejected` is ignored free text. With each of the nine separators below, `_body_scan` skips the empty segment at lines 1531?1532 without leaving `in_tab` or clearing `last`, then treats the free text as a continuation. It falsely refuses `T:C` and invents a second negative id, `T:rejected`.

Expected: `({'T:C': True}, [], 2)`, identical to the LF control. This follows the required body-line splitting and free-text exclusion, and the existing blank-line table termination at lines 1526?1528. Actual is the same false tuple for every separator. This is the reverse direction of finding 1 and should be retained as a separate regression assertion even if one line-splitting repair fixes both.

Exact inputs and outputs:

```text
separator '\r'
input = '| id | decision |\n|---|---|\n| C | accepted |\n\r\rrejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': False, 'T:rejected': False}, ["claim T:C: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted", "claim T:rejected: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted"], 2)

separator '\x0b'
input = '| id | decision |\n|---|---|\n| C | accepted |\n\x0b\x0brejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': False, 'T:rejected': False}, ["claim T:C: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted", "claim T:rejected: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted"], 2)

separator '\x0c'
input = '| id | decision |\n|---|---|\n| C | accepted |\n\x0c\x0crejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': False, 'T:rejected': False}, ["claim T:C: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted", "claim T:rejected: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted"], 2)

separator '\x1c'
input = '| id | decision |\n|---|---|\n| C | accepted |\n\x1c\x1crejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': False, 'T:rejected': False}, ["claim T:C: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted", "claim T:rejected: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted"], 2)

separator '\x1d'
input = '| id | decision |\n|---|---|\n| C | accepted |\n\x1d\x1drejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': False, 'T:rejected': False}, ["claim T:C: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted", "claim T:rejected: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted"], 2)

separator '\x1e'
input = '| id | decision |\n|---|---|\n| C | accepted |\n\x1e\x1erejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': False, 'T:rejected': False}, ["claim T:C: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted", "claim T:rejected: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted"], 2)

separator '\x85'
input = '| id | decision |\n|---|---|\n| C | accepted |\n\x85\x85rejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': False, 'T:rejected': False}, ["claim T:C: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted", "claim T:rejected: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted"], 2)

separator '\u2028'
input = '| id | decision |\n|---|---|\n| C | accepted |\n\u2028\u2028rejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': False, 'T:rejected': False}, ["claim T:C: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted", "claim T:rejected: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted"], 2)

separator '\u2029'
input = '| id | decision |\n|---|---|\n| C | accepted |\n\u2029\u2029rejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
actual = ({'T:C': False, 'T:rejected': False}, ["claim T:C: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted", "claim T:rejected: listed with contradictory decisions: the body table's decision column reads as a negative ('reject') against the seat's addendum: read as NOT accepted"], 2)

LF control input = '| id | decision |\n|---|---|\n| C | accepted |\n\n\nrejected\n\nCOUNCIL-VERDICT: ACCEPT\n\n| id | decision |\n|---|---|\n| C | ACCEPT |\n'
LF control actual = ({'T:C': True}, [], 2)
```

## 4. NOTE ? accepted human-readable variants outside the written rule

These probes are not additional rule violations. Decision normalization is a substring operation with a closed term list; it is not HTML rendering, arbitrary spelling correction, row reconstruction or identifier canonicalization. Existing `_cells` / `_plain` header/id behavior is inherited, not widened by the decision-only normalization. In particular:

- HTML/entities: `not&#32;accepted`, `not&nbsp;accepted`, `re<em>j</em>ect`, `&#114;eject` leave `T:C` true. HTML decoding/tag removal is not specified.
- Synonyms/spelling: `declined`, `denied`, `not approved`, `NOT ACCEPT`, `n\u043et accepted` (Cyrillic o), and `not.ac cep ted` leave `T:C` true. None contains a required negative after the specified transformations.
- Splitting a word across rows (`| C | re\nject |`) leaves `T:C` true. The rule scans each decision/continuation separately; it does not concatenate fragments.
- Extra/missing/escaped pipes: `| C | re|ject |`, `| C || reject |`, `|| C | reject |`, `| C | not\\|accepted |` leave `T:C` true. The first two put the complete negative outside the second cell or divide it; the third lacks an id in the first cell; the fourth retains a literal pipe inside the second cell. None gives C's second cell a listed negative. `| C reject |` instead records `T:C reject` false and leaves `T:C` true. No rule infers a missing cell boundary.
- A continuation `| rejected |` or `| reject |` has a nonempty first cell and begins with `|`, so it is treated as a different id, not as a continuation of C. C remains true; the new id is false. In contrast, a no-id continuation `| | reject |` correctly refuses C.
- Headers `| _Id_ | _Decision_ |`, `| __Id__ | __Decision__ |`, fullwidth header names, `| i\u200bd | decision |`, internal empty-cell header `|| id || decision ||`, missing-opening-pipe `id | decision |`, and quoted `> | id | decision |` are not detected by the inherited lenient helper; their negative rows do not refuse C. A fully blockquoted table was tested, including the row prefix. This is a limit of that concrete helper, not a promised full Markdown renderer. `_seat_table_strict`'s broad phrase ?emphasis, extra pipes ... ignored? should not be read as support for every emphasis style or interior empty cell.
- Body ids `_C_`, `__C__`, `~~C~~`, `C\u200b`, fullwidth C, and `[C](#C)` differ from addendum C under `_plain`; each distinct id becomes false, while `T:C` stays true. Decision normalization is explicitly ?for the substring test only.? No generalized id normalization was promised.
- A prose line beginning `` `COUNCIL-VERDICT` is discussed here.`` really does satisfy the documented prefix test and therefore splits early; C is false when the descriptive body decision is then read strictly as addendum content. An embedded mention in a sentence does not split. Neither is a prefix-rule violation.
- Two separated addenda with matching ACCEPTs yield true here; conflicting ACCEPT / NOT-EXAMINED yields false. This reader does not enforce the separate overall ban on a second verdict line. `LIFECYCLE.md` assigns that check to verdict validation; no conclusion about A4 acceptance is drawn from `seat_table` alone.

## Required positives and additional passing coverage

All four required real decision cells were tried verbatim with body C and addendum C=ACCEPT; every result was `({'T:C': True}, [], 2)`:

1. `accepted with non-blocking remarks (Issue 5: the ? = 0 sentence is read under the premise of F1(ii))`
2. `accepted with non-blocking remarks (Issue 3)`
3. ``accepted with non-blocking remarks (Issue 2: wording of the P-OVL row in `STATEMENT.md` ?4, not of OVL itself)``
4. `accepted (F-1, F-2, F-3, G-1, G-2 verified; UNI-0 and AR(1) correctly not claimed)`

The exact 3-column header `| Id | Disposition | Basis |` with `|---|---|---|` and row `| C | accepted | <basis> |` also accepted C for Basis values `failed`, `rejected`, `withdrawn`, `not accepted`, and `NOT-EXAMINED`. An additional 18-case cross product used decision values `accepted`, `accepted with non-blocking remarks`, `not claimed` and Basis values `reject`, `not accepted`, `withdraw`, `not-examined`, `refus`, `fail`: all accepted. Free negative prose before a table or after its LF blank terminator was ignored.

### Negatives and Unicode

All seven literal closed terms refused C, as did `NOT-EXAMINED`, `rejected`, `accepted (withdrawn)`, `notaccepted`, `NOT_EXAMINED`, `r**e**ject`, `r\eject`, `r\u200beject`, fullwidth `reject`, `not\u00a0accepted`, `not\u2003accepted`, `refused`, and `failure`. Repeated ids cannot overwrite an earlier body negative. A second body table with a negative also refused C (3 tables counted).

Exhaustive insertion coverage under the installed Unicode database:

- Enumerated all 170 `Cf` codepoints and all 29 `str.isspace()` codepoints, plus the 13 characters in `*_` + backtick + `~`, backslash, ASCII hyphen, U+2010?U+2015, and U+2212.
- For each character inserted at every internal position in each of `notaccepted`, `reject`, `withdraw`, `notexamined`, `refus`, `fail`, `_neg_hit` detected a negative: **8,268 / 8,268**.
- The same construction through `seat_table`, excluding the 10 line-splitting characters LF/CR/VT/FF/FS/GS/RS/NEL/U+2028/U+2029 from whitespace insertions, refused C: **7,878 / 7,878**. Separators inside a word are deliberately not asserted to reconstruct a cross-line word.
- All 27 Unicode `Pd` characters were separately tested between `not` and `accepted`; finding 2 lists all 15 misses. This is additional to the insertion counts.

### Headers, ids and continuation handling

An 84-case cross product of first headers `id`, `Id`, `ID`, `claim`, `CLAIM`, `claim id`, `Claim\u00a0Id`; second headers `decision`, `DECISION`, `disposition`, `Disposition`; and decisions `reject`, `NOT-EXAMINED`, `accepted (withdrawn)` refused C in every case. Extra Basis cells were present and harmless.

Body headers with `**Id**` and backticked Decision worked; `||| id | decision |||` and NBSP/em-space `|\u00a0**Claim\u2003Id**\u00a0| `Disposition` |` also worked. A table inside a code fence was scanned and its reject refused C, as specified by this context-free reader.

Body ids C, T:C, `*C*`, `**C**`, backticked C, `T:*C*`, `**T:C**`, and space-trimmed C all matched addendum T:C and refused it for reject. Cases outside that normalization are in NOTE 4.

`C | reject |` (missing leading pipe) and `| C | reject` (missing trailing pipe) correctly refused C. No-id `| | reject |` and bare `rejected` continuations refused the previous C; the bare line also recorded its own first segment as a refused id. No-id continuations with `accepted` in their second cell and `rejected`/`failed` in a later cell refused C by the explicit whole-line continuation rule.

Each of the nine specified non-LF separators between two rows of an ALREADY detected table correctly found a later C=reject. The preceding D=accepted row, absent from the addendum, became false. This isolates finding 1 to detection/state boundaries rather than a missing separator in `_ROW_BREAK`.

### Verdict split, fallback, missing ids and addendum non-acceptance

- Mid-sentence COUNCIL-VERDICT mention before the real line: ignored; descriptive body C plus proper addendum ACCEPT accepted C.
- Prefixes `COUNCIL-VERDICT`, opening-backtick form, leading whitespace, and `COUNCIL-VERDICT-ish` split as the documented starts-with predicate requires. `prefix COUNCIL-VERDICT`, `> COUNCIL-VERDICT`, two initial backticks, and lowercase `council-verdict` did not split.
- A descriptive table after the verdict was read strictly and refused C; the same table before it plus valid ACCEPT addendum accepted C. Body CRLF with LF addendum accepted C.
- No verdict, no post-verdict table, emphasized malformed addendum header, wrong-width delimiter, absent delimiter at EOF, and a malformed second addendum table each returned exactly `_seat_table_strict(whole_text, "T")`. The descriptive body C stayed false. The strict helper comparison checked all three return components, not only C's Boolean.
- An addendum with a malformed row (extra cell), no-id continuation, or contradictory duplicate C refused C; these row-level errors do not need to invalidate the whole addendum.
- Positive body D omitted from an otherwise valid C addendum produced C=true and D=false with a missing-id diagnostic. Negative body D omitted from addendum also produced D=false. No claim was silently made true by omission in these valid-row controls.
- Addendum `NOT-EXAMINED` kept C=false. Legacy `accepted`, `Accepted`, `ACCEPTED` accepted C; `accept`, `ACCEPT (ok)`, and `rejected` refused C under the strict whitelist, with unknown-cell diagnostics where applicable.

## Suggested regression targets

Before changing unrelated parsing behavior, add focused assertions for each of the nine separator substitutions at header detection and blank termination, plus at least U+2E3A/U+2E3B in `not<dash>accepted`. Keep the four real positives, Basis exclusions, strict fallback controls, and existing normalization insertion controls passing. A shared pre-split body-line iterator would address both separator findings; a documented Unicode-dash policy would resolve finding 2.

R07-SOL2: 4 findings (2 MAJOR)

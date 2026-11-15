# R07 cell grammar correctness test - Sol

## Scope and method

Read only C:/Users/felip/BVS-wt/INFRA-R07. Imported its bvsreg.py with Python -B and sys.dont_write_bytecode; ran only in-memory decision_value and seat_table experiments. Did not execute test_lifecycle.py, invoke git, change git state, start subagents, or write any file except this report.

bvsreg.py SHA-256: 09ba5411ef5fe334d9833507556d7a2a2022323ea978b241fda1cc11199f23b8
Python: 3.15.2 (tags/v3.15.2:5e58eaa, Oct 25 2026, 17:27:03) [MSC v.1951 64 bit (AMD64)]

Independent oracle uses literal stems/phrase, spaces/tabs-only exterior trim, explicit separator exclusion, a character-by-character parenthesis stack, and Unicode-aware blank-content detection. The unqualified requirement "non-blank" (brief, bvsreg.py:1313, LIFECYCLE.md:320) is interpreted to exclude all whitespace-only contents. Exterior trim is expressly ASCII-only; interior non-blankness is not so qualified. Zero-width format characters are not Unicode whitespace: inside a remark they are uninterpreted text, not automatically negative test cases.

## Numbered findings

1. **MAJOR: Unicode-whitespace-only parentheticals read accepted.** The non-blank-content guard at bvsreg.py:1330 removes only ASCII space/tab. Consequently a remark containing only NBSP or other Unicode spaces returns accept instead of unknown, and seat_table accepts the claim without a problem. This is one root cause. The specification requires non-blank content (bvsreg.py:1313 and LIFECYCLE.md:320). Use a Unicode-aware interior blank check after the existing separator check, preserving the ASCII-only exterior trim. No code was changed.

Minimal exact reproductions:

    bvsreg.decision_value("accepted (\xa0)")
    # actual: 'accept'; expected: 'unknown'
    bvsreg.seat_table("| id | decision |\n|---|---|\n| A | accepted (\xa0) |\n", "T")
    # actual: ({'T:A': True}, [], 1); expected: T:A=False, with unreadable-cell problem

All directly tested nonseparator Unicode whitespace characters with this defect: '\x1f', '\xa0', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007', '\u2008', '\u2009', '\u200a', '\u202f', '\u205f', '\u3000'.

Every observed cell mismatch, in exact Python repr (ASCII escaped); tuple fields are group, cell, expected, actual. Repeated generated witnesses are retained:

    ('Unicode whitespace and format matrix', 'accepted (\x1f)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\x1f \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\xa0)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\xa0 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u1680)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u1680 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2000)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2000 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2001)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2001 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2002)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2002 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2003)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2003 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2004)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2004 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2005)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2005 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2006)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2006 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2007)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2007 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2008)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2008 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u2009)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u2009 \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u200a)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u200a \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u202f)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u202f \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u205f)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u205f \t)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted (\u3000)', 'unknown', 'accept')
    ('Unicode whitespace and format matrix', 'accepted ( \t\u3000 \t)', 'unknown', 'accept')
    ('seeded mutations', 'accepted (\u2009)', 'unknown', 'accept')
    ('seeded mutations', 'Accepted (\u2001)', 'unknown', 'accept')
    ('seeded mutations', 'ACCEPTED (\u2000)', 'unknown', 'accept')
    ('seeded mutations', 'ACCEPTED (\u2004)', 'unknown', 'accept')
    ('seeded mutations', 'ACCEPTED (\u2001)', 'unknown', 'accept')
    ('seeded mutations', 'accepted (\u2009)', 'unknown', 'accept')
    ('seeded mutations', 'accepted (\x1f)', 'unknown', 'accept')
    ('seeded mutations', 'accepted (\xa0)', 'unknown', 'accept')
    ('seeded mutations', 'Accepted (\u2002)', 'unknown', 'accept')
    ('seeded mutations', 'Accepted (\u2002)', 'unknown', 'accept')
    ('seeded mutations', 'Accepted (\u2007)', 'unknown', 'accept')
    ('seeded mutations', 'Accepted with non-blocking remarks (\u2001)', 'unknown', 'accept')
    ('seeded mutations', 'Accepted (\u205f)', 'unknown', 'accept')
    ('seeded mutations', 'accepted (\xa0)', 'unknown', 'accept')
    ('seeded mutations', 'Accepted (\u2000)', 'unknown', 'accept')
    ('seeded mutations', 'accepted with non-blocking remarks (\u2004)', 'unknown', 'accept')
    ('seeded mutations', 'Accepted (\x1f )', 'unknown', 'accept')

## Coverage

| Group | Calls | Expected accept | Expected not-accept | Mismatches |
|---|---:|---:|---:|---:|
| four real cells | 4 | 4 | 0 | 0 |
| positive and trim matrix | 1616 | 1600 | 16 | 0 |
| explicit negatives | 58 | 0 | 0 | 0 |
| Unicode whitespace and format matrix | 306 | 42 | 0 | 34 |
| separator matrix | 70 | 0 | 0 | 0 |
| exhaustive parentheses 0..8 | 87381 | 6908 | 0 | 0 |
| seeded mutations | 30000 | 2763 | 5 | 17 |
| long inputs | 32 | 8 | 0 | 0 |
| all accepted case variants | 1024 | 12 | 0 | 0 |
| single phrase case changes | 22 | 0 | 0 | 0 |
| all literal space joins | 414 | 14 | 0 | 0 |

All observed mismatches are manifestations of finding 1. No other cell mismatch or exception occurred.

### Four real cells

- 'accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))' -> accept; complete table row also accepted.
- 'accepted with non-blocking remarks (Issue 3)' -> accept; complete table row also accepted.
- 'accepted with non-blocking remarks (Issue 2: wording of the P-OVL row in `STATEMENT.md` \xa74, not of OVL itself)' -> accept; complete table row also accepted.
- 'accepted (F-1, F-2, F-3, G-1, G-2 verified; UNI-0 and AR(1) correctly not claimed)' -> accept; complete table row also accepted.

### Grouped inputs tried

- Positive/trim matrix: ACCEPT, accepted, Accepted, ACCEPTED, NOT-EXAMINED; all three accepted case variants with and without the literal phrase, bare or with each parenthetical content below. Each core is surrounded by all 16 combinations of empty, space, tab, and space-tab-space.

    texts = ['x', 'a (b) c', '((x))', '()', 'withdrawn', 'conditional on X', 'not accepted', 'a,b; except X', '\u03b7 = 0; \xa74; \u6f22\u5b57; \U0001f9ea', 'x\t y', 'x\xa0y', '\u200b', '\ufeff', '\x00', 'a | b']

- Explicit negative grammar: extra words, except/conditional/blocking phrases, commas, negation, trailing text or punctuation, two groups, early close/reopen, imbalance, empty/ASCII-blank groups, incorrect case/spacing, look-alikes, emphasis and code marks. Every cell below returned unknown:

    ['accept', 'Accept', 'aCcEpTeD', 'acceptable', 'accepted-ish', 'not accepted (x)', 'Not accepted (x)', 'accepted except part (ii)', 'accepted conditional on X', 'accepted, with non-blocking remarks', 'accepted, with blocking remarks (x)', 'accepted with blocking remarks (x)', 'accepted with remarks (x)', 'accepted With non-blocking remarks', 'accepted WITH NON-BLOCKING REMARKS', 'accepted with non-blocking remark', 'ACCEPT (x)', 'ACCEPT with non-blocking remarks', 'ACCEPT with non-blocking remarks (x)', 'accepted ()', 'accepted ( \t )', 'accepted (', 'accepted )', 'accepted (a (b)', 'accepted (x))', 'accepted (x) (y)', 'accepted (a) b (c)', 'accepted (x)()', 'accepted ((x))()', 'accepted )x(', 'accepted (x) withdrawn', 'accepted (x).', 'accepted (x);', 'accepted (x),', 'accepted (x) accepted', '(x) accepted', 'no accepted', 'accepted no', 'accepted  (x)', 'accepted\t(x)', 'accepted(x)', 'accepted with  non-blocking remarks', 'accepted with non-blocking remarks  (x)', 'accepted with non-blocking remarks(x)', '**accepted** (x)', '*accepted (x)*', '_accepted (x)_', '`accepted (x)`', 'accepted (\t)', 'accepted ( )', 'accepted () ()', 'accepted (()', 'accepted (()) )', '\u0430ccepted (x)', 'accept\u0435d (x)', '\uff21\uff23\uff23\uff25\uff30\uff34', 'accepted with non\u2011blocking remarks', 'accepted with non\u2013blocking remarks']

- Unicode matrix: all Unicode characters for which Python str.isspace() is true, plus the five format characters below. Each is tested before the cell, after it, replacing a grammar join after accepted / with / non-blocking, alone inside a parenthetical, space/tab-padded inside, and between interior x/y. Non-ASCII spaces/formats outside the parenthetical are rejected; ASCII exterior spaces/tabs are allowed. Nonseparator Unicode text inside is accepted, except that blank interiors should be refused (finding 1).

    whitespace = ['\t', '\n', '\x0b', '\x0c', '\r', '\x1c', '\x1d', '\x1e', '\x1f', ' ', '\x85', '\xa0', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007', '\u2008', '\u2009', '\u200a', '\u2028', '\u2029', '\u202f', '\u205f', '\u3000']
    formats = ['\u200b', '\u200c', '\u200d', '\u2060', '\ufeff']

- Separators: CR, LF, VT, FF, FS, GS, RS, NEL, U+2028, U+2029; each before/after ACCEPT, between accepted and its parenthetical, after the phrase, between interior x/y, alone inside, and after the closing parenthesis. All rejected.
- Exhaustive parentheses: every content string of length 0 through 8 over the four-character alphabet consisting of left parenthesis, right parenthesis, x, and ASCII space. Each wrapped as accepted (CONTENT). 87,381 cases; all matched the independent oracle.
- Additional sweeps: all 256 accepted case variants with four suffix choices; each alphabetic character of the literal phrase individually uppercased; every literal grammar space replaced by empty/double/tab/mixed whitespace and every Unicode space/format; Unicode exterior padding; every forbidden separator inserted at every boundary in the first real cell through seat_table; sticky contradictions and matching/contradictory duplicates across separate tables.
- Mutations: 30,000 cases, random.Random(20261112), cores above plus four real cells as bases; 1-3 insertion/deletion/substitution operations using parentheses, x, space, comma, semicolon, asterisk, backtick, tab, CR/LF, every whitespace character and the five format characters. The exact failing strings are listed above.
- Long inputs: n = 1,000 / 10,000 / 100,000 / 1,000,000. Plain n-character text; depth-n nesting; missing final close; missing one nested close; extra final close; early close, n-character text, reopening; late U+2028; ASCII-whitespace-only content. All classifications matched the oracle. Deep nesting did not require recursion.

### Row-level experiments

1078 row checks: 1061 passed, 17 failed (finding 1). The 1010 systematic real-cell separator insertion cases all passed; their inputs are generated by inserting each of the 10 forbidden separators at each of the 101 character boundaries of real cell 1, then embedding the result in the standard two-column A row. Each remaining tuple below gives name, exact text, expected claim map, actual full seat_table return, and pass flag. Valid LF/CRLF complete rows and an empty remarks column pass. Malformed boundaries, wrong widths, nonempty remarks column, split/continued rows, escaped or unescaped pipes, missing delimiters, separators, and contradictory duplicate ids refuse affected claims. Matching duplicate acceptances pass. Only Unicode-blank remarks fail the expected row checks.

    ('real 1', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': True}, ({'T:A': True}, [], 1), True)
    ('real 2', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 3) |\n', {'T:A': True}, ({'T:A': True}, [], 1), True)
    ('real 3', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 2: wording of the P-OVL row in `STATEMENT.md` \xa74, not of OVL itself) |\n', {'T:A': True}, ({'T:A': True}, [], 1), True)
    ('real 4', '| id | decision |\n|---|---|\n| A | accepted (F-1, F-2, F-3, G-1, G-2 verified; UNI-0 and AR(1) correctly not claimed) |\n', {'T:A': True}, ({'T:A': True}, [], 1), True)
    ('CRLF', '| id | decision |\r\n|---|---|\r\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\r\n', {'T:A': True}, ({'T:A': True}, [], 1), True)
    ('empty remarks column', '| id | decision | remarks |\n|---|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) | \t |\n', {'T:A': True}, ({'T:A': True}, [], 1), True)
    ('nonempty remarks column', '| id | decision | remarks |\n|---|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) | withdrawn |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: non-empty cell(s) after the decision (remarks are not read; write them outside the table): read as NOT accepted'], 1), True)
    ('extra nonempty cell', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) | x |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row has 3 cells, the table header 2: read as NOT accepted'], 1), True)
    ('extra empty cell width', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) | |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row has 3 cells, the table header 2: read as NOT accepted'], 1), True)
    ('missing opening boundary', '| id | decision |\n|---|---|\nA | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted'], 1), True)
    ('missing closing boundary', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted'], 1), True)
    ('split phrase', '| id | decision |\n|---|---|\n| A | accepted with non-blocking\nremarks (Issue 3) |\n', {'T:A': False}, ({'T:A': False, 'T:remarks (Issue 3)': False}, ['claim T:A: a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted', 'claim T:remarks (Issue 3): a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted'], 1), True)
    ('split paren', '| id | decision |\n|---|---|\n| A | accepted (Issue 3\n) |\n', {'T:A': False}, ({'T:A': False, 'T:)': False}, ['claim T:A: a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted', 'claim T:): a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted'], 1), True)
    ('split after paren', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))\n|\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted', "malformed per-claim table row '|': a line inside the table is not a complete row (`| id | decision |`): continued or split row"], 1), True)
    ('continued no id', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n| | (more) |\n', {'T:A': False}, ({'T:A': False}, ["claim T:A: a row without an id continues the previous row (a line after this claim's row): read as NOT accepted"], 1), True)
    ('continued form no id', '| id | decision |\n|---|---|\n| A | ACCEPT |\n| | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': False}, ({'T:A': False}, ["claim T:A: a row without an id continues the previous row (a line after this claim's row): read as NOT accepted"], 1), True)
    ('nonrow continuation', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\nmore\n', {'T:A': False}, ({'T:A': False}, ["claim T:A: a line inside the table is not a complete row (`| id | decision |`): continued or split row (a line after this claim's row): read as NOT accepted"], 1), True)
    ('malformed own and previous', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\nB | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': False, 'T:B': False}, ({'T:A': False, 'T:B': False}, ["claim T:A: a line inside the table is not a complete row (`| id | decision |`): continued or split row (a line after this claim's row): read as NOT accepted", 'claim T:B: a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted'], 1), True)
    ('pipe in paren', '| id | decision |\n|---|---|\n| A | accepted (a | b) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row has 3 cells, the table header 2: read as NOT accepted'], 1), True)
    ('escaped pipe', '| id | decision |\n|---|---|\n| A | accepted (a \\| b) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains an escaped pipe: read as NOT accepted'], 1), True)
    ('no delimiter', '| id | decision |\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': False}, ({'T:A': False}, ["claim T:A: the table is malformed: the line after its header is not a delimiter row `|---|---|` of the header's width: read as NOT accepted", "malformed per-claim table (the line after its header is not a delimiter row `|---|---|` of the header's width): its rows read as NOT accepted"], 1), True)
    ("duplicates ('accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))', 'NOT-EXAMINED')", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n| A | NOT-EXAMINED |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: listed with contradictory decisions: read as NOT accepted'], 1), True)
    ("duplicates ('NOT-EXAMINED', 'accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))')", '| id | decision |\n|---|---|\n| A | NOT-EXAMINED |\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: listed with contradictory decisions: read as NOT accepted'], 1), True)
    ("duplicates ('accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))', 'accepted except X')", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n| A | accepted except X |\n', {'T:A': False}, ({'T:A': False}, ["claim T:A: decision cell 'accepted except X' is not exactly ACCEPT or NOT-EXAMINED (legacy: accepted / Accepted / ACCEPTED, optionally ' with non-blocking remarks' and one final balanced '(...)'): read as NOT accepted", 'claim T:A: listed with contradictory decisions: read as NOT accepted'], 1), True)
    ("duplicates ('accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))', 'ACCEPT')", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n| A | ACCEPT |\n', {'T:A': True}, ({'T:A': True}, [], 1), True)
    ("duplicates ('accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))', 'accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))')", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': True}, ({'T:A': True}, [], 1), True)
    ("separator inside '\\x85'", '| id | decision |\n|---|---|\n| A | accepted (a\x85b) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator after row '\\x85'", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\x85 \n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator inside '\\r'", '| id | decision |\n|---|---|\n| A | accepted (a\rb) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator after row '\\r'", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\r \n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator inside '\\x1e'", '| id | decision |\n|---|---|\n| A | accepted (a\x1eb) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator after row '\\x1e'", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\x1e \n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator inside '\\u2028'", '| id | decision |\n|---|---|\n| A | accepted (a\u2028b) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator after row '\\u2028'", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\u2028 \n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator inside '\\x0c'", '| id | decision |\n|---|---|\n| A | accepted (a\x0cb) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator after row '\\x0c'", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\x0c \n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator inside '\\x1c'", '| id | decision |\n|---|---|\n| A | accepted (a\x1cb) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator after row '\\x1c'", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\x1c \n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator inside '\\x0b'", '| id | decision |\n|---|---|\n| A | accepted (a\x0bb) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator after row '\\x0b'", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\x0b \n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator inside '\\u2029'", '| id | decision |\n|---|---|\n| A | accepted (a\u2029b) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator after row '\\u2029'", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\u2029 \n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator inside '\\x1d'", '| id | decision |\n|---|---|\n| A | accepted (a\x1db) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator after row '\\x1d'", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\x1d \n', {'T:A': False}, ({'T:A': False}, ['claim T:A: the row contains a line or paragraph separator (row split): read as NOT accepted'], 1), True)
    ("separator inside '\\n'", '| id | decision |\n|---|---|\n| A | accepted (a\nb) |\n', {'T:A': False}, ({'T:A': False, 'T:b)': False}, ['claim T:A: a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted', 'claim T:b): a line inside the table is not a complete row (`| id | decision |`): continued or split row: read as NOT accepted'], 1), True)
    ("blank Unicode '\\x1f'", '| id | decision |\n|---|---|\n| A | accepted (\x1f) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\xa0'", '| id | decision |\n|---|---|\n| A | accepted (\xa0) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u1680'", '| id | decision |\n|---|---|\n| A | accepted (\u1680) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2000'", '| id | decision |\n|---|---|\n| A | accepted (\u2000) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2001'", '| id | decision |\n|---|---|\n| A | accepted (\u2001) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2002'", '| id | decision |\n|---|---|\n| A | accepted (\u2002) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2003'", '| id | decision |\n|---|---|\n| A | accepted (\u2003) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2004'", '| id | decision |\n|---|---|\n| A | accepted (\u2004) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2005'", '| id | decision |\n|---|---|\n| A | accepted (\u2005) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2006'", '| id | decision |\n|---|---|\n| A | accepted (\u2006) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2007'", '| id | decision |\n|---|---|\n| A | accepted (\u2007) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2008'", '| id | decision |\n|---|---|\n| A | accepted (\u2008) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u2009'", '| id | decision |\n|---|---|\n| A | accepted (\u2009) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u200a'", '| id | decision |\n|---|---|\n| A | accepted (\u200a) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u202f'", '| id | decision |\n|---|---|\n| A | accepted (\u202f) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u205f'", '| id | decision |\n|---|---|\n| A | accepted (\u205f) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("blank Unicode '\\u3000'", '| id | decision |\n|---|---|\n| A | accepted (\u3000) |\n', {'T:A': False}, ({'T:A': True}, [], 1), False)
    ("sticky contradiction ('accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))', 'NOT-EXAMINED', 'accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))')", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n| A | NOT-EXAMINED |\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: listed with contradictory decisions: read as NOT accepted', 'claim T:A: listed with contradictory decisions: read as NOT accepted'], 1), True)
    ("sticky contradiction ('NOT-EXAMINED', 'accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))', 'ACCEPT')", '| id | decision |\n|---|---|\n| A | NOT-EXAMINED |\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n| A | ACCEPT |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: listed with contradictory decisions: read as NOT accepted', 'claim T:A: listed with contradictory decisions: read as NOT accepted'], 1), True)
    ("sticky contradiction ('accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))', 'accepted except X', 'accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii))')", '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n| A | accepted except X |\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': False}, ({'T:A': False}, ["claim T:A: decision cell 'accepted except X' is not exactly ACCEPT or NOT-EXAMINED (legacy: accepted / Accepted / ACCEPTED, optionally ' with non-blocking remarks' and one final balanced '(...)'): read as NOT accepted", 'claim T:A: listed with contradictory decisions: read as NOT accepted', 'claim T:A: listed with contradictory decisions: read as NOT accepted'], 1), True)
    ('separate-table duplicate', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n\nAddendum\n\n| id | decision |\n|---|---|\n| A | ACCEPT |\n', {'T:A': True}, ({'T:A': True}, [], 2), True)
    ('separate-table duplicate', '| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n\nAddendum\n\n| id | decision |\n|---|---|\n| A | NOT-EXAMINED |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: listed with contradictory decisions: read as NOT accepted'], 2), True)
    ('separate-table duplicate', '| id | decision |\n|---|---|\n| A | NOT-EXAMINED |\n\nAddendum\n\n| id | decision |\n|---|---|\n| A | accepted with non-blocking remarks (Issue 5: the \u03b7 = 0 sentence is read under the premise of F1(ii)) |\n', {'T:A': False}, ({'T:A': False}, ['claim T:A: listed with contradictory decisions: read as NOT accepted'], 2), True)


### Long-input performance

Times are median and maximum of five calls per already-built string, in milliseconds; construction is excluded. No catastrophic regex/backtracking growth was observed. Long matched content is scanned linearly, including deeply nested parentheses. These are local timings, not a universal runtime bound.

| n | Shape | Cell length | Median ms | Max ms |
|---:|---|---:|---:|---:|
| 1000 | plain | 1011 | 0.067 | 0.067 |
| 1000 | deep | 2012 | 0.203 | 0.203 |
| 1000 | missing close | 1010 | 0.002 | 0.003 |
| 1000 | missing nested close | 2011 | 0.239 | 0.312 |
| 1000 | extra close | 1012 | 0.066 | 0.126 |
| 1000 | early close and reopen | 1015 | 0.015 | 0.015 |
| 1000 | late separator | 1012 | 0.014 | 0.014 |
| 1000 | blank | 1011 | 0.017 | 0.017 |
| 10000 | plain | 10011 | 0.689 | 0.691 |
| 10000 | deep | 20012 | 2.338 | 2.612 |
| 10000 | missing close | 10010 | 0.015 | 0.015 |
| 10000 | missing nested close | 20011 | 2.229 | 2.358 |
| 10000 | extra close | 10012 | 0.706 | 0.707 |
| 10000 | early close and reopen | 10015 | 0.051 | 0.054 |
| 10000 | late separator | 10012 | 0.058 | 0.058 |
| 10000 | blank | 10011 | 0.079 | 0.079 |
| 100000 | plain | 100011 | 8.120 | 8.625 |
| 100000 | deep | 200012 | 25.050 | 28.240 |
| 100000 | missing close | 100010 | 0.243 | 0.270 |
| 100000 | missing nested close | 200011 | 26.867 | 44.691 |
| 100000 | extra close | 100012 | 8.817 | 14.857 |
| 100000 | early close and reopen | 100015 | 1.502 | 2.084 |
| 100000 | late separator | 100012 | 1.679 | 1.836 |
| 100000 | blank | 100011 | 1.890 | 2.102 |
| 1000000 | plain | 1000011 | 84.240 | 98.347 |
| 1000000 | deep | 2000012 | 251.465 | 259.392 |
| 1000000 | missing close | 1000010 | 1.994 | 2.043 |
| 1000000 | missing nested close | 2000011 | 258.256 | 264.525 |
| 1000000 | extra close | 1000012 | 78.145 | 108.186 |
| 1000000 | early close and reopen | 1000015 | 13.672 | 14.309 |
| 1000000 | late separator | 1000012 | 16.091 | 17.059 |
| 1000000 | blank | 1000011 | 9.890 | 17.672 |

R07-SOL: 1 findings (1 MAJOR)

# DRAFT: GC_PREREG §10 deviation entry: `tests/test_gc_readback.py` fixture (B1 of `reviews/GC_P_READBACK_CHECK_OPUS.md`)

**Status: DRAFT for the manager's commit with W1. Nothing registered has been changed: `tests/test_gc_readback.py` on disk is still `c5ebaf077ec054a3…`.** Written Fri 2026-11-20.

**Entry for §10 (after commit):**
> **2026-11-20: test fixture, `tests/test_gc_readback.py`** (`c5ebaf077ec054a3…` → `c46582cd46b64178722834178ab74ddb139ff5d4fa033eb4ee6b8f0a9ee2cc71`). *Reason:* `test_real_11_17_record_parse` ran `gc_readback.py --records os.path.dirname(REAL)`, i.e. the whole `records/` root. After the GC_P pilot, three directories carry run id `6-AR-n200-r01-V-s1` (`F1M_pilot/`, `hygiene_1117/group1/runs/F1M_pilot/…`, `gc1m/GC_P/…`); `gb_readback.find()` keeps the last match per run id, so the test read the pilot (M1 0.0170710) instead of the 11-17 record (0.0171029…) and failed (7 of 8). *Change:* one token, `--records os.path.dirname(REAL)` → `--records REAL` (line 75), which scopes the walk to `records/F1M_pilot` alone. *Effect:* no script, threshold, rule or class value changes; `gc_readback.py` (`63767ad3312ef580…`), `gc_identity.py` (`6842354256c47a49…`), `gb_readback.py` (`870a610a…`) untouched. The GC_P read-back's own numbers are single-record (pilot only, `--records records/gc1m/GC_P`, 1 fit found) and were never affected.

**Verification (patched copy, not the registered file):** the one-token change was applied to a copy in scratch (with copies of `gc_readback.py` and `gb_readback.py` alongside) and `python3 -I tests/test_gc_readback.py` gave **8 / 8 OK**. The patched file's sha256 is the "new sha" above; the manager's commit should reproduce it byte for byte:
`sed 's|"--records", os.path.dirname(REAL)|"--records", REAL|' tests/test_gc_readback.py` (diff: exactly line 75).

**Rule for the block read-backs (no deviation, practice):** scope `--records` to `records/gc1m/<batch>`, never to the records root or anything containing `F1M_pilot` or `hygiene_1117`, and state the number of fits found.

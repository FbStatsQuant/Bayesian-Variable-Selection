#!/usr/bin/env python3
"""Validate the exact committed PROD-L output contract."""
import csv
import hashlib
import re
import sys
from pathlib import Path

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()

def verify(folder, prefix):
    folder = Path(folder)
    try:
        lines = (folder / (prefix + '.sha256')).read_text(encoding='utf-8').splitlines()
        wanted = [prefix + '.rds'] if prefix == 'EXACT' else [prefix + '.rds', prefix + '.csv']
        entries = {}
        for line in lines:
            m = re.fullmatch(r'([0-9a-fA-F]{64})  ([^/\\]+)', line)
            if not m or m.group(2) in entries:
                raise ValueError('malformed or duplicate checksum entry')
            entries[m.group(2)] = m.group(1).lower()
        if set(entries) != set(wanted) or len(lines) != len(wanted):
            raise ValueError('wrong checksum file set')
        for name in wanted:
            path = folder / name
            if not path.is_file() or path.stat().st_size == 0 or digest(path) != entries[name]:
                raise ValueError('missing, empty or mismatched ' + name)
        marker = (folder / (prefix + '.done')).read_text(encoding='utf-8').splitlines()
        if not marker or (prefix == 'EXACT' and marker[0] != entries['EXACT.rds']) or (prefix != 'EXACT' and not marker[0].startswith('status ')):
            raise ValueError('malformed done marker')
        if prefix != 'EXACT':
            with (folder / (prefix + '.csv')).open(newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, strict=True)
                if not reader.fieldnames or not {'status', 'v3_status'} <= set(reader.fieldnames):
                    raise ValueError('CSV missing status columns')
                rows = list(reader)
                if len(rows) != 2 or any(None in row or any(v is None for v in row.values()) for row in rows):
                    raise ValueError('CSV must contain exactly two complete rows')
        return True, 'verified'
    except (OSError, UnicodeError, ValueError, csv.Error) as e:
        return False, str(e)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(2)
    ok, reason = verify(sys.argv[1], sys.argv[2])
    print(reason)
    sys.exit(0 if ok else 1)

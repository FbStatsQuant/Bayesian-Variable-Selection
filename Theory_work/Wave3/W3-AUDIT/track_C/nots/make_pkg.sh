#!/usr/bin/env bash
# Build the frozen NOTS package from this worktree: bash make_pkg.sh DEST_DIR   (DEST_DIR must not exist)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); TC=$(dirname "$HERE"); W2=$(cd "$TC/../../../Wave2" && pwd)
DEST=$1; [[ ! -e $DEST ]] || { echo "exists: $DEST" >&2; exit 66; }
mkdir -p "$DEST/scripts" "$DEST/data"
cp "$TC"/scripts/c_designs.py "$TC"/scripts/c_proxies.py "$TC"/scripts/c_run_cell.py "$TC"/scripts/c_test.py "$TC"/scripts/c_collect.py "$DEST/scripts/"
cp "$W2"/W2-SIM/X/data/riboflavin_L.csv "$W2"/W2-SIM/X/data/fred_qd_L.csv "$DEST/data/"
cp "$HERE"/env_c.sh "$HERE"/run_task.sh "$HERE"/submit.sh "$HERE"/classes.tsv "$HERE"/tasks_*.tsv "$HERE"/README.md "$DEST/"
( cd "$TC" && git log -1 --format='commit %H %cI' -- . ) > "$DEST/COMMIT"
( cd "$DEST" && find . -type f ! -name MANIFEST.sha256 -print0 | sort -z | xargs -0 sha256sum > MANIFEST.sha256 )
chmod -R a-w "$DEST"
echo "package: $DEST ($(wc -l < "$DEST/MANIFEST.sha256") files)"

#!/usr/bin/env bash
# runs ON NOTS (via: ssh nots 'bash -s' < nots_index_add.sh): append two entries to scratch/INDEX.md (doc edit only; idempotent)
set -u
D=/scratch/fb31/SMC_Engineering_Department
echo "--- scratch/INDEX.md before (tail)"; tail -n 4 $D/INDEX.md | cut -c1-200
ls $D/code_ws | tr '\n' ' '; echo; ls $D/overlap1e4 | tr '\n' ' '; echo
if grep -q "code_ws/" $D/INDEX.md; then echo "entries already present: nothing appended"; exit 0; fi
cat >> $D/INDEX.md <<'EOF'
- 2026-11-19 — `code_ws/` (this directory; also reachable as `~/SMC_Engineering_Department/scratch/code_ws/`): the code trees of the campaign builds: git worktrees of the shallow clone of the freeze commit F (eefcbc4a...): `W1_Feefcbc4a_code` to `W3_...`, `PL_Feefcbc4a_code` (the precision leg), the `OV_W0_*_code` trees and `FREEZE_CHECK_1e5_code_*`; `scripts/<batch>/code` is a symlink into it (moved out of home 11-18, home quota). Owner: Engineering ops. Source only, regenerable from the clone; cleaned only after the leg builds are recorded and no wave is running; the 14-day atime purge applies.
- 2026-11-19 — `overlap1e4/` (this directory; a stray of the overlap rung, now also serving the precision leg): `clone_eefcbc4a/`, the 150 MB shallow git clone of F (built on Owls, rsynced; the source of every git worktree and git archive of the overlap and precision builds). Owner: Engineering ops. Cleaned together with `code_ws/` at the end of the leg; keep until then (the worktrees in `code_ws/` depend on it).
EOF
echo "--- after (tail)"; tail -n 2 $D/INDEX.md | cut -c1-110

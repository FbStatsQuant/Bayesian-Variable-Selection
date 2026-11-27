#!/usr/bin/env bash
# pull_to_owls.sh -- run on OWLS. Copy S1 / S2 SMC-BVS records from NOTS scratch to Owls and verify every file by sha256.
#   pull_to_owls.sh [--suite 1|2] --reps LO-HI [--tag b<K>] [--src-sub smcbvs | --method M] [--dest DIR] [--dry-run]
#   (--method M = --src-sub M: the benchmark records of method M, e.g. runs/S1S2/lasso_cv/S1_xx/...)
#   source : nots:/scratch/fb31/SMC-BVS/runs/S1S2/<src-sub>/S<suite>_*/rep_RRR.{json,rds}   (suite 1 = S1_01..S1_16, the
#            default; suite 2 = S2_001..S2_120; reps LO..HI)
#   dest   : /home/fb31/Bayesian-Variable-Selection/_local/engineering/runs/S1S2/<src-sub>/...   (--dest overrides the root)
# Steps: (1) on NOTS, sha256 of the existing record files of the range -> manifest (ONE ssh); (2) rsync exactly those
# files (--files-from); a different existing Owls file (e.g. the Owls smoke rep_001) is NOT overwritten silently: rsync
# moves it to <dest>/_superseded/<ts>/ first; (3) sha256sum -c of the manifest on Owls. Exit 0 only if every file
# verifies. The manifest is kept as <dest>/_manifests/pull_<tag>_<ts>.sha256 (package/free steps use it).
# Records of tasks still running are simply absent (run_one.R writes rds/json by atomic rename; *.tmp is never pulled).
set -euo pipefail
NRUNS=/scratch/fb31/SMC-BVS/runs/S1S2
DEST=/home/fb31/Bayesian-Variable-Selection/_local/engineering/runs/S1S2
reps=""; tag=""; sub=smcbvs; dry=0; suite=1
while (($#)); do case "$1" in --suite) suite="$2"; shift 2;; --reps) reps="$2"; shift 2;; --tag) tag="$2"; shift 2;; --src-sub|--method) sub="$2"; shift 2;;
  --dest) DEST="$2"; shift 2;; --dry-run) dry=1; shift;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$reps" =~ ^([0-9]+)-([0-9]+)$ ]] || { echo "need --reps LO-HI" >&2; exit 64; }
lo=${BASH_REMATCH[1]}; hi=${BASH_REMATCH[2]}; [[ "$sub" =~ ^[A-Za-z0-9_/]+$ ]] || exit 64
[[ "$suite" == 1 || "$suite" == 2 ]] || { echo "--suite must be 1 or 2" >&2; exit 64; }
ts=$(date -u +%Y%m%dT%H%M%SZ); tag=${tag:-r${lo}-${hi}}
mkdir -p "$DEST/_manifests"; man="$DEST/_manifests/pull_${tag}_${ts}.sha256"
# (1) remote manifest: paths relative to the NOTS runs root, e.g. smcbvs/S1_03/rep_001.rds (only S<suite>_* dirs)
ssh nots "cd '$NRUNS' && for d in $sub/S${suite}_*/; do for r in \$(seq $lo $hi); do for e in json rds; do
            f=\${d}rep_\$(printf %03d \$r).\$e; [ -f \"\$f\" ] && echo \"\$f\"; done; done; done | xargs -r -d '\n' sha256sum" > "$man.part"
mv "$man.part" "$man"
nf=$(wc -l < "$man"); echo "manifest: $man ($nf files)"
(( nf > 0 )) || { echo "nothing to pull"; exit 0; }
cut -c67- "$man" > "$man.list"
if ((dry)); then
  rsync -a -n -i --files-from="$man.list" "nots:$NRUNS/" "$DEST/" | head -20; echo "[dry-run] nothing copied"; rm -f "$man" "$man.list"; exit 0
fi
# (2) copy; changed existing files are moved aside, never silently replaced
rsync -a --files-from="$man.list" --backup --backup-dir="_superseded/$ts" "nots:$NRUNS/" "$DEST/"
rm -f "$man.list"
[[ -d "$DEST/_superseded/$ts" ]] && echo "NOTE: superseded Owls files kept in $DEST/_superseded/$ts/ ($(find "$DEST/_superseded/$ts" -type f | wc -l) files)"
# (3) verify
( cd "$DEST" && sha256sum --quiet -c "$man" ) && echo "VERIFIED: $nf files match the NOTS sha256 manifest" || { echo "FAILED: sha256 mismatch (see above)" >&2; exit 1; }

#!/usr/bin/env bash
# launch.sh <name> <spec> <outdir> <lat_max> : one owls_run -j 2 job (2 shards), rc written to <outdir>/<name>.rc
N=$1; SPEC=$2; OUT=$3; export LS0_LAT_MAX=$4
mkdir -p "$OUT"; rm -f "$OUT/$N.rc"
/home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- /home/fb31/ls0_work/run2.sh "$SPEC" "$OUT" > "$OUT/$N.owls_run.out" 2>&1
echo $? > "$OUT/$N.rc"

#!/usr/bin/env bash
# probe_remote.sh -- runs ON NOTS (fed through ONE ssh by monitor_probe.sh): ONE squeue + ONE sacct -X, plus plain file reads of the wave's run dirs.
# usage: bash -s -- <DEPT> <WAVE> <MAKE_CALIB_META 0|1> <batch>...   Read-only, except MAKE_CALIB_META=1: for a fit whose calib.bin exists and calib_meta.json does not,
# one nice'd `smcbvs4 info calib.bin --meta 1 --record calib_meta.json` (the batch's binary, env.sh sourced) writes calib_meta.json into that run dir (O-4 / O-7 artifact).
set -u
D=$1; WAVE=$2; MAKE=$3; shift 3; BL="$*"
echo "### META utc=$(date -u +%FT%TZ)"
ids=''
for b in $BL; do
  echo "### SUBMISSIONS $b"; cat $D/scratch/runs/$b/submissions.jsonl 2>/dev/null || true
  ids="$ids,$(grep -o '"job": *"[0-9]*"' $D/scratch/runs/$b/submissions.jsonl 2>/dev/null | grep -o '[0-9][0-9]*' | paste -sd, || true)"
done
ids=$(echo "$ids" | sed 's/^,*//; s/,,*/,/g; s/,*$//')
echo '### SQUEUE'; squeue -u fb31 -h -o '%i|%j|%T|%r|%M|%C'
echo '### SACCT'; [[ -n $ids ]] && sacct -X -P -n -j "$ids" --format=JobID,JobName,State,ElapsedRaw,AllocCPUS,CPUTimeRAW,Timelimit || true
if [[ $MAKE == 1 ]]; then
  for b in $BL; do for r in $D/scratch/runs/$b/*/; do
    [[ -s $r/calib.bin && -f $r/calib.bin.json && ! -f $r/calib_meta.json ]] || continue
    ( set +u; source $D/scripts/$b/env.sh >/dev/null 2>&1; nice -n 19 $D/scripts/$b/bin/smcbvs4 info $r/calib.bin --meta 1 --record $r/calib_meta.json >/dev/null 2>&1 ) || true
  done; done
fi
python3 - "$D" $BL <<'PY'
import glob, hashlib, json, os, re, sys
D, batches = sys.argv[1], sys.argv[2:]
def J(p):
    try:
        return json.load(open(p))
    except Exception:
        return None
out = {k: [] for k in ("DATA_HASH", "CALIB", "ISLAND_T", "DIAG", "BINSHA", "ENGINE_FLAGS")}
for b in batches:
    bp = os.path.join(D, "scripts", b, "bin", "smcbvs4")
    if os.path.exists(bp):
        h = hashlib.sha256()
        with open(bp, "rb") as f:
            for c in iter(lambda: f.read(1 << 20), b""):
                h.update(c)
        out["BINSHA"].append("%s|%s" % (b, h.hexdigest()))
    for r in sorted(glob.glob(os.path.join(D, "scratch", "runs", b, "*", ""))):
        rid = os.path.basename(r.rstrip("/"))
        dj, tj, cj, cm = J(r + "data.bin.json"), J(r + "truth.json"), J(r + "calib.bin.json"), J(r + "calib_meta.json")
        if dj or tj:
            out["DATA_HASH"].append("|".join([b, rid, (dj or {}).get("content_sha256", "-"), (tj or {}).get("X_sha256", "-"), (tj or {}).get("y_sha256", "-"),
                                              ((dj or {}).get("binary") or {}).get("sha256", "-")]))
        if cj or cm:
            st = (cj or {}).get("settings") or {}
            tiers = st.get("tiers") or []
            tf = (cj or {}).get("tier_final", 0)
            nfin = next((t.get("N_final") for t in tiers if t.get("tier") == tf), None)
            m = (cm or {}).get("meta") or {}
            rec = {"N": m.get("N", nfin), "refine_m": m.get("refine_m", st.get("refine_m")), "I_max": m.get("I_max", st.get("I_max")), "I_used": m.get("I_used"),
                   "rule": m.get("rule", st.get("rule")), "grid_unconverged": (m.get("flags") or {}).get("grid_unconverged"),
                   "status": (cj or {}).get("status"), "cal_status": (cj or {}).get("cal_status"), "source": "calib_meta.json" if cm else "calib.bin.json settings"}
            out["CALIB"].append("%s|%s|%s" % (b, rid, json.dumps(rec, sort_keys=True)))
        i1 = J(r + "island_1.bin.json")
        if i1 and "T" in i1:
            out["ISLAND_T"].append("%s|%s|%s" % (b, rid, i1["T"]))
        diag = [int(m.group(1)) for f in os.listdir(r + "cost") for m in [re.match(r"cost_diag_t\d+_k(\d+)_r\d+\.jsonl$", f)] if m] if os.path.isdir(r + "cost") else []
        if cj:
            out["DIAG"].append("%s|%s|%d|%d" % (b, rid, max(diag) if diag else -1, len(diag)))
        o = r + "OUTCOME"
        if os.path.exists(o):
            out["ENGINE_FLAGS"].append(o)
        for lg in glob.glob(r + "log/*.log"):
            try:
                if re.search(r"resource_limit|admission", open(lg, errors="replace").read(), re.I):
                    out["ENGINE_FLAGS"].append(lg)
            except OSError:
                pass
for k, v in out.items():
    print("### " + k)
    for l in v:
        print(l)
PY

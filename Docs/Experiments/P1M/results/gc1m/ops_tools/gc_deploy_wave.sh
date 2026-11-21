#!/usr/bin/env bash
# gc_deploy_wave.sh <WAVE P|D|D2|W1|W2|W3> <SCRIPTS_SRC> -- 1M pilot GC_P (GC_PLAN §2.1): COPYBIN ONLY of the ONE F2 binary (BUILD_F2 in deploy_gc.log); NO build, NEVER submits.
# Steps: local SHA256SUMS ok and plan checks (code_commit == F2, island_isa sapphirerapids, the explicit N / refine_m 1 / I_max in every fit's params) -> home guard (<= 7,900)
# -> refuse an already submitted batch (explicit EXISTS / FRESH) -> mkdir on NOTS -> rsync the driver files (no bin / code / build) -> sha256sum -c ON NOTS
# -> master binary scripts/VN_ID_1/bin/smcbvs4 must equal the BUILD_F2 sha -> `cp -p` into every batch's bin/ -> sha256 recomputed == BUILD_F2 -> `version` (env.sh sourced)
# git_commit == e993ece2.., sapphirerapids, libm pass -> one COPYBIN line per batch in deploy_gc.log (UTC, batch, COPYBIN, sha256, git, isa, libm, home MB, who).
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; SRC=${2:?SCRIPTS_SRC}; [[ $WAVE =~ ^(P|D|D2|W1|W2|W3)$ ]] || { echo "bad wave" >&2; exit 64; }
BL=${BATCHES:-$(batches_of "$SRC" "$WAVE")}; [[ -n $BL ]] || { echo "no batches the batches of wave $WAVE in $SRC" >&2; exit 64; }
SHA=$(f2_sha); [[ -n $SHA ]] || { echo "REFUSING: no BUILD_F2 line in $LOG" >&2; exit 65; }
for B in $BL; do
  (cd "$SRC/$B" && sha256sum --quiet -c SHA256SUMS) || { echo "FATAL: local SHA256SUMS differ in $B" >&2; exit 66; }
  python3 - "$SRC/$B" "$F2" "$B" <<'PY'
import json, sys, os
d, f2, b = sys.argv[1:]
p = json.load(open(d + "/plan.resolved.json"))
assert p["code_commit"] == f2 and p["batch"] == b and p["island_isa"] == "sapphirerapids" and not p.get("warnings"), "plan header"
for f in p["fits"]:
    pr = f.get("params") or {}
    want = {"6-AR-n200-r01-V-s1": ("AR", 200, 602020001), "6-AR-n1000-r01-V-s1": ("AR", 1000, 602100001), "6-AR-n200-r02-V-s1": ("AR", 200, 602020002), "6-AR-n200-r03-V-s1": ("AR", 200, 602020003), "6-AR-n200-r04-V-s1": ("AR", 200, 602020004), "6-AR-n200-r05-V-s1": ("AR", 200, 602020005), "6-AR-n200-r06-V-s1": ("AR", 200, 602020006), "6-ADJOPP-n200-r01-V-s1": ("ADJ-OPP", 200, 605020001)}.get(f["run_id"])
    assert want is not None and b in ("GC_P", "GC_D", "GC_D2", "GC_W1", "GC_W2", "GC_W3"), "fit %s is not a released 1M fit of batch %s" % (f["run_id"], b)
    assert f["N"] == 2500 and pr.get("refine_m") == 1 and pr.get("I_max") == 0 and f["Rp"] == 16 and f.get("seed") == want[2] and f.get("data_seed") == want[2] and f.get("n") == want[1] and f.get("p") == 1000000 and f.get("design") == want[0] and f.get("mode") == "V","fit %s: N / refine_m 1 / I_max 0 / R' 16 / seed / n / p / design not as the released plan" % f["run_id"]
    for st in ("calibrate", "island", "merge"):
        m = json.load(open("%s/manifests/%s/%s.json" % (d, f["run_id"], st)))["params"]
        assert (m.get("N"), m.get("refine_m"), m.get("I_max")) == (f["N"], 1, pr["I_max"]), "fit %s %s manifest params %s" % (f["run_id"], st, m)
print(b, "OK: code_commit == F2; %d fits, N / refine_m 1 / I_max explicit in the plan and in the calibrate / island / merge manifests; islands %s; worst %s core-h, cap %s, tasks %s" % (
    len(p["fits"]), p["fits"][0]["resources"]["islands"]["time"], p["worst_case_core_h"], p["core_h_cap"], p["n_tasks"]))
PY
done
home_guard
for B in $BL; do
  st=$(ssh $NOTS "if [[ -e $D/scratch/runs/$B/submissions.jsonl ]]; then echo EXISTS; else echo FRESH; fi" 2>/dev/null || true)
  [[ $st == FRESH ]] || { [[ $st == EXISTS ]] && echo "REFUSING: $B was already submitted" >&2 || echo "REFUSING: could not read the state of $B over ssh (got '$st'); retry (nothing was changed)" >&2; exit 65; }
  ssh $NOTS "mkdir -p $D/scratch/runs/$B $D/scripts/$B"
  rs --exclude code --exclude bin --exclude build "$SRC/$B"/ $NOTS:$D/scripts/$B/
  ssh $NOTS "cd $D/scripts/$B && sha256sum --quiet -c SHA256SUMS && echo '$B: SHA256SUMS verified on NOTS'"
done
for B in $BL; do
  ssh $NOTS "set -e; M=$D/scripts/$MASTER/bin; [[ \$(sha256sum \$M/smcbvs4 | cut -d' ' -f1) == $SHA ]] || { echo 'FATAL: the master binary does not match BUILD_F2' >&2; exit 67; }
    mkdir -p $D/scripts/$B/bin; cp -p \$M/smcbvs4 $D/scripts/$B/bin/smcbvs4; cp -p \$M/version.json $D/scripts/$B/bin/version.json
    sha256sum $D/scripts/$B/bin/smcbvs4 > $D/scripts/$B/bin/smcbvs4.sha256; echo '$MASTER' > $D/scripts/$B/bin/COPIED_FROM
    [[ \$(sha256sum $D/scripts/$B/bin/smcbvs4 | cut -d' ' -f1) == $SHA ]] && echo '$B: bin/smcbvs4 copied from $MASTER, sha256 == BUILD_F2'"
  ssh $NOTS "( set +u; source $D/scripts/$B/env.sh >/dev/null 2>&1; $D/scripts/$B/bin/smcbvs4 version 2>&1 )" > "$STG/.ver.$B" || true
  GC=$(grep -o '"git_commit": *"[^"]*"' "$STG/.ver.$B" | head -1 | grep -o '"[^"]*"$' | tr -d '"'); ISA=$(grep -o '"island_isa": *"[^"]*"' "$STG/.ver.$B" | head -1 | grep -o '"[^"]*"$' | tr -d '"'); LIBM=$(grep -c '"pass": *true' "$STG/.ver.$B" || true); rm -f "$STG/.ver.$B"
  [[ $GC == "$F2" && $ISA == sapphirerapids && $LIBM -ge 1 ]] || { echo "FATAL: $B version check failed (git_commit '$GC', isa '$ISA', libm '$LIBM')" >&2; exit 67; }
  log_gc "$B" COPYBIN "$SHA" "$GC" "$ISA" "$LIBM" "$(home_mb)"
done
home_guard
echo "deploy done (not submitted). Next: gc_presubmit.sh $WAVE"

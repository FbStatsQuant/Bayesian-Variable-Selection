#!/usr/bin/env bash
# free_nots_scratch.sh -- run on OWLS. Deletes the NOTS scratch copy of ONE batch's records, only when it is safe.
#   free_nots_scratch.sh --batch K --manifest <pull manifest used for the unit> [--go]      (default: dry run)
# Gates, each its own sha256 check, all must pass (else nothing is deleted):
#   G1 the desktop has verified the unit: 'S1S2_smcbvs_b<K>' is a line of crews/offload/desktop_verified.txt;
#   G2 the Owls copies (runs/S1S2/...) re-hash to the pull manifest, every file;
#   G3 the unit's tars re-hash to its SHA256SUMS -- if the unit is still on Owls (the offload crew deletes it after G1,
#      keeping records_manifests/<unit>/); otherwise records_manifests/<unit>/SHA256SUMS.txt must exist;
#   G4 on NOTS, immediately before rm, each file re-hashes to the manifest (sha256sum -c); only then are exactly the
#      manifest's files removed (rm per file, never a directory or glob). Empty setting dirs are left in place.
# Scratch purge (14 days without access, no backup) makes this step urgent but never skippable: pull + package right
# after each batch; delete only after G1-G4.
set -euo pipefail
ROOT=/home/fb31/Bayesian-Variable-Selection; ENG=$ROOT/_local/engineering
SRC=$ENG/runs/S1S2; NRUNS=/scratch/fb31/SMC-BVS/runs/S1S2
batch=""; man=""; go=0
while (($#)); do case "$1" in --batch) batch="$2"; shift 2;; --manifest) man="$2"; shift 2;; --go) go=1; shift;;
  *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$batch" =~ ^[0-9]+$ && -f "$man" ]] || { echo "usage: --batch K --manifest FILE [--go]" >&2; exit 64; }
unit=S1S2_smcbvs_b${batch}
grep -qxF "$unit" "$ENG/crews/offload/desktop_verified.txt" || { echo "G1 FAIL: $unit not in desktop_verified.txt"; exit 1; }; echo "G1 ok: desktop verified $unit"
( cd "$SRC" && sha256sum --quiet -c "$man" ) || { echo "G2 FAIL: Owls copies differ from $man"; exit 1; }; echo "G2 ok: Owls copies match ($(wc -l < "$man") files)"
if [[ -d "$ENG/records/$unit" ]]; then ( cd "$ENG/records/$unit" && sha256sum --quiet -c SHA256SUMS ) || { echo "G3 FAIL: unit tars"; exit 1; }; echo "G3 ok: unit tars verify"
else [[ -s "$ENG/records_manifests/$unit/SHA256SUMS.txt" ]] || { echo "G3 FAIL: unit gone from records/ and no records_manifests/$unit/SHA256SUMS.txt"; exit 1; }; echo "G3 ok: unit offloaded, manifest kept"; fi
grep -vE '^[0-9a-f]{64}  smcbvs/S1_[0-9]{2}/rep_[0-9]{3}\.(json|rds)$' "$man" && { echo "refusing: unexpected path in manifest"; exit 1; }
if ((go == 0)); then
  ssh nots "cd '$NRUNS' && sha256sum --quiet -c -" < "$man" && echo "G4 ok (dry run): NOTS files match; would delete $(wc -l < "$man") files" || echo "G4 FAIL (dry run)"
  exit 0
fi
ssh nots "set -euo pipefail; cd '$NRUNS'; m=\$(mktemp); cat > \"\$m\"; sha256sum --quiet -c \"\$m\" || { echo 'G4 FAIL: NOTS files differ; nothing deleted'; rm -f \"\$m\"; exit 1; }
          cut -c67- \"\$m\" | while IFS= read -r f; do rm -f -- \"\$f\"; done; echo \"G4 ok: deleted \$(wc -l < \"\$m\") files\"; rm -f \"\$m\"" < "$man"

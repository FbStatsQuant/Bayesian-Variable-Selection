#!/bin/bash
# d31_backups_archive.sh : (laptop; run via launch_with_shim.sh) D31 archive-then-erase, steps 1-3 for /home/fb31/backups: list (types, sizes, mtimes,
# sha256, open files), archive to the laptop by one tar stream, verify every file's sha256 locally. Deletes NOTHING.
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
A="/c/Users/felip/OneDrive - Rice University/NOTS Data/NOTS_home_archive/backups_20261030"
EV=$CAMP/ops/evidence/ops6_d31_backups
[ ! -e "$A" ] || { echo "archive folder exists: $A"; exit 1; }
mkdir -p "$A"
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'date -u +%FT%TZ; cd /home/fb31/backups || exit 3; echo "== entries"; find . -mindepth 1 -printf "%y\t%s\t%TY-%Tm-%TdT%TH:%TM\t%u\t%P\n" | sort -k5; echo "== symlinks"; find . -type l | wc -l; echo "== sha256"; find . -type f -print0 | sort -z | xargs -0 sha256sum; echo "== du"; du -sk /home/fb31/backups; echo "== open (this node)"; for p in /proc/[0-9]*; do [ "$(stat -c %U $p 2>/dev/null)" = fb31 ] || continue; ls -l $p/fd 2>/dev/null | grep -F /home/fb31/backups; done; echo "== end"' > "${EV}_listing.txt" 2>&1 || { cat "${EV}_listing.txt"; echo "LISTING FAILED"; exit 1; }
cat "${EV}_listing.txt"
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'tar -cf - -C /home/fb31 backups' > "$A.tar" 2> "${EV}_tar_stderr.txt" || { echo "TAR STREAM FAILED"; cat "${EV}_tar_stderr.txt"; exit 1; }
tar -xf "$A.tar" -C "$A" && rm -f -- "$A.tar"
sed -n '/^== sha256$/,/^== du$/p' "${EV}_listing.txt" | grep -E '^[0-9a-f]{64}  ' | sed 's#  \./#  backups/#' > "$A/REMOTE_SHA256.txt"
( cd "$A" && sha256sum --quiet -c REMOTE_SHA256.txt ) && echo "ARCHIVE VERIFIED: $(wc -l < "$A/REMOTE_SHA256.txt") files" || { echo "ARCHIVE NOT VERIFIED"; exit 1; }
find "$A/backups" -type f | wc -l | sed 's/^/local files: /'

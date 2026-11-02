#!/bin/bash
# d29_dbbackups_delete.sh v5 (OPS-4; HQ D29 + D30 + D31 + D34): erase the Sol-reviewed, ARCHIVED old Codex log-database folders under ~/.codex/db-backups only.
# History: v2 answered Sol R1 findings 2-8 (R1 finding 1 answered by D30: Codex runs only on loginx2); v3 replaced lsof by a /proc scan and added the archive gate;
# v4 answered Sol R2 (review/SOL_REVIEW_D29_DBBACKUPS_R2.md): quarantine by rename; every safety-critical status checked; keep membership by associative
# array; explicit unlink progress; strict helper identities; absolute-path usage.
# v5 answers Sol R3 (review/SOL_REVIEW_D29_DBBACKUPS_R3.md): F2 each /proc producer classified separately (status 0 + empty stderr = ok; otherwise only
# status 0/1 with non-empty diagnostics that are ALL ENOENT (fd closed mid-scan) or ALL EACCES (verified helper); nonzero-silent, signals, mixed -> abort);
# F3 mutation-started flag set before the first rm, progress counted right after each successful rm, any later failure = PARTIAL; F4 clobber-RESISTANT
# placement by reservation: mkdir(2) of the destination (exclusive: fails if anything exists; RENAME_NOREPLACE is unsupported on NOTS NFS,
# evidence/ops4_noreplace_probe_raw.txt), then rename(2) onto that reserved directory (fails if anything appeared inside it); identities are device.inode.
# v5.1 (Sol R4): F1 a vanished maps of a live process aborts before any helper exemption.
# Residuals accepted by HQ D34 (2026-10-30), same-user races in a window of seconds at paths only this script uses: (R3 F1) a process of fb31 opening the
# quarantine path, or receiving a passed descriptor, after its last scan; (R4 F2) a process of fb31 deleting our just-created EMPTY reservation and
# creating its own EMPTY directory there before our rename, which the rename would then replace (worst case: loss of that empty directory; no file data).
#
# Usage (laptop, ONE ssh to the pinned alias; the three files sit in /scratch/fb31/New_Campaign/runs/ops4_d29/):
#   ssh nots 'bash /scratch/fb31/New_Campaign/runs/ops4_d29/d29_dbbackups_delete.sh /scratch/fb31/New_Campaign/runs/ops4_d29/ops4_dbbackups_delete_list.tsv /scratch/fb31/New_Campaign/runs/ops4_d29/archive_manifest.sha256'        # dry run
#   ssh nots 'bash /scratch/fb31/New_Campaign/runs/ops4_d29/d29_dbbackups_delete.sh /scratch/fb31/New_Campaign/runs/ops4_d29/ops4_dbbackups_delete_list.tsv /scratch/fb31/New_Campaign/runs/ops4_d29/archive_manifest.sha256 --yes'  # erase
# Exit: 0 = completed; every row DELETED / WOULD-DELETE / KEPT (incl. RESTORED) with its files untouched.
#       1 = some row FAILED or PARTIAL (location of what remains is printed). 3 = refused before any mutation, or aborted (a row in quarantine is restored
#       first if no unlink was attempted on it; otherwise it is reported PARTIAL with its location).
#
# Per row (erase mode):
#   1. fresh scan: full find inventory of db-backups (status+stderr checked, structure deviation aborts); keep set = 3 newest by newest high-resolution mtime
#      (all ties at the 3rd value), every folder with newest mtime >= now - 24 h, every folder referenced by any fb31 process on this node (/proc: fd, cwd,
#      root, exe, maps; D30: the only node running Codex);
#   2. identity: outside the keep set; real directory, owner fb31, base device, canonical path; exactly the reviewed file names and sizes; reviewed mtime;
#   3. QUARANTINE: atomic rename(2) of db-backups/<name> to the private 0700 folder ~/.ops4_d29_quarantine/<name> (same filesystem; rename never copies).
#      This blocks opens by the OLD pathname; it does not exclude a process of fb31 opening the private quarantine path, or receiving a passed descriptor,
#      after its last scan (residual accepted by HQ D34). Directory and file device.inode identities are verified after the move;
#   4. two /proc scans (1 s apart) after the move: any reference to the folder (old or quarantine path) -> restore -> KEEP;
#   5. pass 1: every file's inode, type and sha256 = VERIFIED archive manifest; any mismatch -> restore -> KEEP;
#   6. pass 2: unlink each file after re-checking its inode, recording progress; rmdir. A failure after the first unlink is PARTIAL (exit 1), never KEEP.
# Dry run: steps 1, 2 and the pass-1 hash check in place; nothing is renamed, created or removed.
set -uo pipefail
export LC_ALL=C
cd / || exit 3
BASE=/home/fb31/.codex/db-backups
CODEX=/home/fb31/.codex
QUAR=/home/fb31/.ops4_d29_quarantine
LIST_SHA_EXPECTED=b5a2f47d5ff1537d305211b26738551e91d6fee51422f494a1e43c0c84571e9c
MANIFEST_SHA_EXPECTED=d2a67f0dd6e0a695ba5a8e92ad5788e9b540417bb6c9374500b17acddba81816
ROWS_EXPECTED=89
MANIFEST_LINES_EXPECTED=265
HEADER_EXPECTED=$'path\tdu_kb\tnewest_mtime_epoch\tnewest_mtime_utc\tdir_mtime_utc\tn_files\tfiles(name:bytes)'
MODE=DRYRUN; DONE=0; KEPT=0; FAILED=0; FREED=0; CUR=""; CUR_DINO=""; CUR_MUT=0; QUAR_MADE=0; PLACE_MSG=""
WORK=""
declare -A KEEP=() INVMT=()
cleanup() { [ -n "$WORK" ] && rm -rf -- "$WORK"; }
trap cleanup EXIT
refuse() { echo "REFUSE: $*" >&2; exit 3; }
summary() { echo "SUMMARY mode=$MODE $( [ "$MODE" = DELETE ] && echo deleted || echo would_delete )=$DONE kept=$KEPT failed_or_partial=$FAILED kb=$FREED end=$(date -u +%FT%TZ) status=$1"; }
abort() {
  echo "ABORT: $*"
  if [ -n "$CUR" ]; then
    if [ "$CUR_MUT" = 1 ]; then echo "PARTIAL $BASE/$CUR: aborted after an unlink was attempted; remaining in $QUAR/$CUR: $(residue "$QUAR/$CUR")"; FAILED=$((FAILED+1)); CUR=""
    else restore "$CUR" "$CUR_DINO" "abort"; fi
  fi
  [ $QUAR_MADE = 1 ] && rmdir -- "$QUAR" 2>/dev/null
  summary ABORTED; exit 3
}

# ---------- arguments, host, user, tools ----------
[ $# -ge 2 ] && [ $# -le 3 ] || refuse "usage: d29_dbbackups_delete.sh LIST MANIFEST [--yes]"
LIST=$1; MAN=$2
if [ $# -eq 3 ]; then [ "$3" = --yes ] || refuse "unknown argument '$3'"; MODE=DELETE; fi
[ "$(hostname -s)" = loginx2 ] || refuse "host $(hostname -s) is not loginx2"
[ "$(id -un)" = fb31 ] || refuse "user is not fb31"
for c in find stat sha256sum du awk sort readlink rmdir rm hostname mktemp od grep perl cat sleep cp tail head tr date; do command -v "$c" >/dev/null 2>&1 || refuse "missing tool $c"; done
[ -d /proc/self/fd ] || refuse "/proc not usable"
WORK=$(mktemp -d) || refuse "mktemp failed"
SELF_SHA=$(sha256sum "$0" | cut -c1-64) || refuse "self hash failed"
echo "d29 v5.1 mode=$MODE host=$(hostname) user=$(id -un) pid=$$ start=$(date -u +%FT%TZ) script_sha256=$SELF_SHA codex_dir_mode=$(stat -c %a "$CODEX")"

# ---------- inputs: private copies, hashes, schema ----------
pin() { # pin SRC EXPECTED_SHA DEST
  local src=$1 want=$2 dst=$3 got last
  [ -f "$src" ] && [ -r "$src" ] || refuse "$src not readable"
  cp -- "$src" "$dst" || refuse "copy of $src failed"
  got=$(sha256sum "$dst") || refuse "hash of $src failed"
  [ "${got:0:64}" = "$want" ] || refuse "$src sha256 ${got:0:64} differs from reviewed $want"
  last=$(tail -c1 "$dst" | od -An -c | tr -d ' ') || refuse "tail of $src failed"
  [ "$last" = '\n' ] || refuse "$src does not end in a newline"
  if grep -q $'\r' "$dst"; then refuse "$src contains CR"; elif [ $? -ne 1 ]; then refuse "grep on $src failed"; fi
}
LIST_COPY=$WORK/list.tsv; MAN_COPY=$WORK/manifest.sha256
pin "$LIST" "$LIST_SHA_EXPECTED" "$LIST_COPY"
pin "$MAN" "$MANIFEST_SHA_EXPECTED" "$MAN_COPY"
[ "$(head -n1 "$LIST_COPY")" = "$HEADER_EXPECTED" ] || refuse "list header differs from the reviewed schema"
VAL=$(awk -F'\t' -v want="$ROWS_EXPECTED" '
  NR==1{next}
  { n++; if (NF!=7) {print "row " NR ": " NF " fields"; bad=1}
    for (i=1;i<=7;i++) if ($i=="") {print "row " NR ": empty field " i; bad=1}
    if ($1 !~ /^\/home\/fb31\/\.codex\/db-backups\/sqlite-[0-9]+-0$/) {print "row " NR ": bad path"; bad=1}
    if ($2 !~ /^[0-9]+$/ || $3 !~ /^[0-9]+$/ || $6 !~ /^[1-3]$/) {print "row " NR ": non-numeric field"; bad=1}
    if (seen[$1]++) {print "row " NR ": duplicate path"; bad=1} }
  END{ if (n!=want) {print "rows " n " != " want; bad=1}; exit bad }' "$LIST_COPY") || refuse "list schema: $VAL"
VAL=$(awk -v want="$MANIFEST_LINES_EXPECTED" '
  { n++; if ($0 !~ /^[0-9a-f]{64}  sqlite-[0-9]+-0\/logs_2\.sqlite(-shm|-wal)?$/) {print "manifest line " NR " malformed"; bad=1}; if (seen[substr($0,67)]++) {print "duplicate " substr($0,67); bad=1} }
  END{ if (n!=want) {print "manifest lines " n " != " want; bad=1}; exit bad }' "$MAN_COPY") || refuse "manifest schema: $VAL"
VAL=$(awk -F'\t' 'NR==FNR{ if (FNR>1){ n=$1; sub(".*/","",n); k=split($7,f," "); for (i=1;i<=k;i++){ split(f[i],a,":"); L[n "/" a[1]]=1 } } next }
       { M[substr($0,67)]=1 }
       END{ for (x in L) if (!(x in M)) {print "list file not in manifest: " x; bad=1}; for (x in M) if (!(x in L)) {print "manifest file not in list: " x; bad=1}; exit bad }' "$LIST_COPY" "$MAN_COPY") \
  || refuse "list/manifest disagree: $VAL"

# ---------- base and quarantine ----------
[ -d "$BASE" ] && [ ! -L "$BASE" ] && [ ! -L "$CODEX" ] || refuse "base missing or a link"
CANON_BASE=$(readlink -f -- "$BASE") || refuse "readlink of base failed"
BASE_DEV=$(stat -c %d -- "$BASE") || refuse "stat of base failed"
QPARENT=${QUAR%/*}
CANON_QPARENT=$(readlink -f -- "$QPARENT") || refuse "readlink of quarantine parent failed"
[ "$(stat -c %d -- "$QPARENT")" = "$BASE_DEV" ] || refuse "quarantine parent is on another device"
CANON_QUAR=$CANON_QPARENT/${QUAR##*/}
[ ! -e "$QUAR" ] && [ ! -L "$QUAR" ] || refuse "quarantine $QUAR already exists (leftover of an earlier run: inspect it by hand)"

# ---------- open-file scan ----------
# Writes the referenced folder names to $WORK/refs as "B <name>" (under db-backups) or "Q <name>" (under the quarantine). Runs in the current shell.
# Fails closed: an unreadable live fb31 process aborts unless it is one of two strictly identified non-dumpable helpers (evidence/ops4_proc_probe_raw.txt):
#   sshd     : comm sshd, parent comm sshd, parent owner root;
#   (sd-pam) : comm (sd-pam), parent comm systemd, parent owner fb31, grandparent pid 1.
# References already read from such a helper are still recorded. A pid whose start time changes during its scan aborts.
# classify STATUS ERRFILE -> ok | enoent | eperm | bad. ok = status 0 and no diagnostics. Otherwise the status must be 0 or 1 (find and cat report ordinary
# errors with 1) AND the diagnostics non-empty AND all of one kind; a nonzero status without diagnostics, any other status (signals, >1), or mixed/unknown
# diagnostics is bad.
classify() {
  local rc=$1 f=$2 cnt t a b
  if [ "$rc" = 0 ] && [ ! -s "$f" ]; then echo ok; return 0; fi
  [ -s "$f" ] || { echo bad; return 0; }
  case "$rc" in 0|1) ;; *) echo bad; return 0;; esac
  cnt=$(awk '{t++} /No such file or directory/{a++} /Permission denied/{b++} END{print t+0, a+0, b+0}' "$f") || { echo bad; return 0; }
  read -r t a b <<< "$cnt"
  if [ "$t" -gt 0 ] && [ "$a" -eq "$t" ]; then echo enoent; elif [ "$t" -gt 0 ] && [ "$b" -eq "$t" ]; then echo eperm; else echo bad; fi
}
residue() { local o rc; o=$(find "$1" -mindepth 1 -printf '%f ' 2>&1); rc=$?; printf '[%s] (listing status %s)' "$o" "$rc"; }
starttime() { local s; s=$(cat -- "/proc/$1/stat" 2>/dev/null) || return 1; s=${s##*) }; set -- $s; printf '%s' "${20}"; }
open_scan() {
  local p pid u st1 st2 frc mrc cf cm diag e1=$WORK/e1 e2=$WORK/e2 fo=$WORK/fo mo=$WORK/mo c pp pu pc gpp
  : > "$WORK/refs" || abort "cannot write refs"
  for p in /proc/[0-9]*; do
    pid=${p#/proc/}
    u=$(stat -c %U -- "$p" 2>/dev/null) || { [ -d "$p" ] && abort "cannot stat live $p"; continue; }
    [ "$u" = fb31 ] || continue
    st1=$(starttime "$pid") || { [ -d "$p" ] && abort "cannot read start time of live $p"; continue; }
    find "$p/fd/" "$p/cwd" "$p/root" "$p/exe" -maxdepth 1 -type l -printf '%l\n' > "$fo" 2>"$e1"; frc=$?
    cat -- "$p/maps" > "$mo" 2>"$e2"; mrc=$?
    awk -v a="$CANON_BASE/" -v b="$BASE/" -v q="$CANON_QUAR/" -v r="$QUAR/" '
      { for (i=1;i<=NF;i++) { s=$i; t="";
          if (index(s,a)==1) {t="B"; s=substr(s,length(a)+1)} else if (index(s,b)==1) {t="B"; s=substr(s,length(b)+1)}
          else if (index(s,q)==1) {t="Q"; s=substr(s,length(q)+1)} else if (index(s,r)==1) {t="Q"; s=substr(s,length(r)+1)}
          if (t!="") { split(s,x,"/"); if (x[1]!="") print t " " x[1] } } }' "$fo" "$mo" >> "$WORK/refs" || abort "reference parser failed for $p"
    cf=$(classify "$frc" "$e1"); cm=$(classify "$mrc" "$e2")
    if [ "$cf" != ok ] || [ "$cm" != ok ]; then
      [ -d "$p" ] || continue                                                # process ended during its scan: it holds nothing now
      diag="fd-scan status=$frc class=$cf stderr=[$(head -c 150 "$e1" | tr '\n' ' ')] maps status=$mrc class=$cm stderr=[$(head -c 150 "$e2" | tr '\n' ' ')]"
      if [ "$cf" = bad ] || [ "$cm" = bad ] || [ -z "$cf" ] || [ -z "$cm" ]; then abort "open-file scan of live process $p failed: $diag"; fi
      # maps may only be ok or (verified helper) eperm: a vanished maps of a live process aborts BEFORE any helper exemption (Sol R4 F1)
      if [ "$cm" = enoent ]; then abort "maps of live process $p vanished: $diag"; fi
      if [ "$cf" = eperm ] || [ "$cm" = eperm ]; then
        c=$(cat -- "$p/comm" 2>/dev/null); pp=$(awk '/^PPid:/{print $2}' "$p/status" 2>/dev/null)
        pu=$(stat -c %U -- "/proc/$pp" 2>/dev/null); pc=$(cat -- "/proc/$pp/comm" 2>/dev/null); gpp=$(awk '/^PPid:/{print $2}' "/proc/$pp/status" 2>/dev/null)
        if [ "$c" = sshd ] && [ "$pc" = sshd ] && [ "$pu" = root ]; then
          echo "open-scan: skipped helper pid=$pid comm=sshd parent=$pp(sshd,root)" >&2
        elif [ "$c" = "(sd-pam)" ] && [ "$pc" = systemd ] && [ "$pu" = fb31 ] && [ "$gpp" = 1 ]; then
          echo "open-scan: skipped helper pid=$pid comm=(sd-pam) parent=$pp(systemd,fb31) grandparent=1" >&2
        else
          abort "live process $p (comm=$c parent=$pp comm=$pc owner=$pu grandparent=$gpp) is not inspectable: $diag"
        fi
      fi                                                                    # remaining case: fd scan all-ENOENT (a descriptor closed during the scan), maps ok
    fi
    st2=$(starttime "$pid") || { [ -d "$p" ] && abort "cannot re-read start time of live $p"; continue; }
    [ "$st1" = "$st2" ] || abort "pid $pid was replaced during its scan"
  done
}

# ---------- fresh state before every row: inventory + keep set ----------
scan() {
  local rc raw=$WORK/inv_raw kp=$WORK/keep_age now t n
  [ "$(readlink -f -- "$BASE")" = "$CANON_BASE" ] || abort "canonical base changed"
  find "$CANON_BASE" -mindepth 1 -printf '%d\t%y\t%P\t%T@\n' > "$raw" 2>"$WORK/fe"; rc=$?
  { [ $rc -eq 0 ] && [ ! -s "$WORK/fe" ]; } || abort "inventory find failed rc=$rc: $(head -c 300 "$WORK/fe")"
  t=$(awk -F'\t' '
      $1==1 && !($2=="d" && $3 ~ /^sqlite-[0-9]+-0$/) {print "unexpected depth-1 entry " $2 " " $3; exit}
      $1==2 && !($2=="f" && $3 ~ /^sqlite-[0-9]+-0\/logs_2\.sqlite(-shm|-wal)?$/) {print "unexpected depth-2 entry " $2 " " $3; exit}
      $1>2 {print "entry deeper than 2: " $3; exit}' "$raw") || abort "structure check failed to run"
  [ -z "$t" ] || abort "structure: $t"
  awk -F'\t' '{split($3,a,"/"); d=a[1]; if (!(d in m) || $4+0>m[d]+0) m[d]=$4} END{for (d in m) printf "%s\t%s\n", d, m[d]}' "$raw" > "$WORK/inv_agg" || abort "inventory aggregation failed"
  sort -t$'\t' -k2,2gr "$WORK/inv_agg" > "$WORK/inv" || abort "inventory sort failed"
  n=$(awk 'END{print NR}' "$WORK/inv") || abort "inventory count failed"
  [ "$n" -ge 1 ] || abort "empty inventory"
  INVMT=(); KEEP=()
  while IFS=$'\t' read -r d m; do INVMT[$d]=${m%%.*}; done < "$WORK/inv"
  [ ${#INVMT[@]} -eq "$n" ] || abort "inventory load mismatch"
  now=$(date +%s.%N) || abort "date failed"
  awk -F'\t' -v now="$now" 'NR<=3{t=$2} NR<=3 || $2+0>=t+0 || $2+0>=now-86400 {print $1}' "$WORK/inv" > "$kp" || abort "keep-set computation failed"
  while read -r d; do KEEP[$d]="top3/24h"; done < "$kp"
  open_scan
  while read -r t d; do
    [ "$t" = B ] || abort "a process references the quarantine at row start ($d)"
    KEEP[$d]="open"
  done < "$WORK/refs"
  [ ${#KEEP[@]} -ge $(( n < 3 ? n : 3 )) ] || abort "keep set smaller than min(3, folders)"
}

# ---------- rename helpers ----------
prename() { perl -e 'rename($ARGV[0], $ARGV[1]) or do { print STDERR "rename: $!\n"; exit 1 }' -- "$1" "$2"; }   # rename(2): atomic, never copies (EXDEV fails)
# place SRC DST ID : clobber-resistant move of directory SRC (identity ID = device.inode) to DST. Reserve DST with mkdir(2) (fails if DST exists), then
# rename(2) SRC onto that reserved directory (fails if anything appeared inside it). Residual (D34): an EMPTY directory substituted for our reservation
# by another fb31 process between mkdir and rename would be replaced.
# 0 = moved and verified; 1 = not moved (SRC untouched; our empty reservation removed if still ours); 2 = state uncertain (PLACE_MSG says where things are).
place() {
  local src=$1 dst=$2 id=$3 rid
  [ "$(stat -c %d.%i -- "$src" 2>/dev/null)" = "$id" ] || { PLACE_MSG="source identity changed"; return 1; }
  mkdir -- "$dst" 2>"$WORK/me" || { PLACE_MSG="destination exists or mkdir failed: $(head -c 150 "$WORK/me" | tr '\n' ' ')"; return 1; }
  rid=$(stat -c %d.%i -- "$dst") || { PLACE_MSG="cannot stat reservation $dst"; return 2; }
  if ! prename "$src" "$dst" 2>"$WORK/re"; then
    PLACE_MSG="rename onto reservation refused: $(head -c 150 "$WORK/re" | tr '\n' ' ')"
    if [ "$(stat -c %d.%i -- "$dst" 2>/dev/null)" = "$rid" ]; then rmdir -- "$dst" 2>/dev/null || PLACE_MSG="$PLACE_MSG; reservation $dst left in place (not empty)"; fi
    return 1
  fi
  if [ "$(stat -c %d.%i -- "$dst" 2>/dev/null)" = "$id" ] && [ ! -e "$src" ]; then return 0; fi
  PLACE_MSG="identity after rename differs (source still exists: $([ -e "$src" ] && echo yes || echo no))"; return 2
}
restore() { # restore NAME ID WHY : move QUAR/NAME back to BASE/NAME via place() (clobber-resistant, see above)
  local n=$1 di=$2 why=$3 r
  place "$QUAR/$n" "$BASE/$n" "$di"; r=$?
  if [ $r -eq 0 ]; then echo "RESTORED $BASE/$n ($why)"; CUR=""; return 0; fi
  echo "FAILED $BASE/$n: not restored ($why; $PLACE_MSG); the folder is at $QUAR/$n: $(residue "$QUAR/$n") (archived copy exists)"; FAILED=$((FAILED+1)); CUR=""; return 1
}

echo "keep set before row 1:"; scan; for d in "${!KEEP[@]}"; do echo "  $d ${KEEP[$d]}"; done | sort

if [ "$MODE" = DELETE ]; then mkdir -m 700 -- "$QUAR" || refuse "cannot create quarantine"; QUAR_MADE=1
  [ "$(stat -c %d -- "$QUAR")" = "$BASE_DEV" ] || abort "quarantine is on another device"; fi

# ---------- rows ----------
while IFS=$'\t' read -r path kb mt mtu dmu nf files; do
  [ "$path" = path ] && [ "$kb" = du_kb ] && continue
  name=${path##*/}
  scan
  if [ -n "${KEEP[$name]+x}" ]; then echo "KEEP $path: in keep set (${KEEP[$name]})"; KEPT=$((KEPT+1)); continue; fi
  if [ -z "${INVMT[$name]+x}" ]; then echo "KEEP $path: absent from current inventory (already gone?)"; KEPT=$((KEPT+1)); continue; fi
  why=""
  [ "${INVMT[$name]}" = "$mt" ] || why="$why mtime-changed($mt->${INVMT[$name]})"
  [ "$(readlink -f -- "$path")" = "$CANON_BASE/$name" ] || why="$why not-canonical"
  [ "$(stat -c %F -- "$path" 2>/dev/null)" = directory ] || why="$why not-a-directory"
  [ -L "$path" ] && why="$why symlink"
  [ "$(stat -c %U -- "$path" 2>/dev/null)" = fb31 ] || why="$why not-owned-by-fb31"
  [ "$(stat -c %d -- "$path" 2>/dev/null)" = "$BASE_DEV" ] || why="$why other-device"
  want=$(printf '%s\n' $files | sort) || why="$why sort-failed"
  if have=$(find "$path" -mindepth 1 -maxdepth 1 -printf '%y:%f:%s\n' 2>/dev/null); then
    have=$(printf '%s\n' "$have" | awk -F: '$1!="f"{print "NONFILE:" $2; next} {print $2 ":" $3}' | sort) || why="$why content-parse-failed"
  else why="$why content-scan-failed"; fi
  [ "$have" = "$want" ] || why="$why contents-differ"
  [ "$(printf '%s\n' "$want" | awk 'NF' | wc -l)" = "$nf" ] || why="$why n_files-mismatch"
  if [ -n "$why" ]; then echo "KEEP $path:$why"; KEPT=$((KEPT+1)); continue; fi
  dino=$(stat -c %d.%i -- "$path") || { echo "KEEP $path: stat failed"; KEPT=$((KEPT+1)); continue; }
  # file:inode:sha256(archive)
  fis=""
  for f in $(printf '%s\n' $files | cut -d: -f1); do
    h=$(awk -v k="$name/$f" 'substr($0,67)==k {print substr($0,1,64)}' "$MAN_COPY") || { fis=ERR; break; }
    i=$(stat -c %d.%i -- "$path/$f") || { fis=ERR; break; }
    [ ${#h} -eq 64 ] || { fis=ERR; break; }
    fis="$fis $f:$i:$h"
  done
  [ "$fis" != ERR ] || { echo "KEEP $path: inode/manifest lookup failed"; KEPT=$((KEPT+1)); continue; }
  k=$(du -sk -- "$path") || { echo "KEEP $path: du failed"; KEPT=$((KEPT+1)); continue; }; k=${k%%[[:space:]]*}
  [[ "$k" =~ ^[0-9]+$ ]] || { echo "KEEP $path: du output not numeric"; KEPT=$((KEPT+1)); continue; }
  verify_hashes() { # verify_hashes DIR : every file's inode, type and sha256 = archive; 0 = all good
    local dir=$1 x f r ino h got
    for x in $fis; do f=${x%%:*}; r=${x#*:}; ino=${r%%:*}; h=${r#*:}
      [ "$(stat -c %d.%i -- "$dir/$f" 2>/dev/null)" = "$ino" ] || return 12
      [ -f "$dir/$f" ] && [ ! -L "$dir/$f" ] || return 13
      got=$(sha256sum -- "$dir/$f") || return 15
      [ "${got:0:64}" = "$h" ] || return 14
    done; return 0; }
  if [ "$MODE" = DRYRUN ]; then
    verify_hashes "$path"; vr=$?
    if [ $vr -eq 0 ]; then echo "WOULD-DELETE $path kb=$k dir_inode=$dino archive-sha-ok"; DONE=$((DONE+1)); FREED=$((FREED+k))
    else echo "KEEP $path: archive hash/identity check failed (rc=$vr)"; KEPT=$((KEPT+1)); fi
    continue
  fi
  # ---- 3. quarantine by atomic rename ----
  CUR_MUT=0
  place "$path" "$QUAR/$name" "$dino"; pr=$?
  if [ $pr -eq 1 ]; then echo "KEEP $path: not quarantined ($PLACE_MSG)"; KEPT=$((KEPT+1)); continue; fi
  if [ $pr -eq 2 ]; then echo "FAILED $path: quarantine state uncertain ($PLACE_MSG); check $path and $QUAR/$name"; FAILED=$((FAILED+1)); continue; fi
  CUR=$name; CUR_DINO=$dino
  # ---- 4. two post-rename open scans ----
  hit=""
  for pass in 1 2; do
    [ $pass = 2 ] && { sleep 1 || abort "sleep failed"; }
    open_scan
    while read -r t d; do [ "$d" = "$name" ] && hit="$hit $t-pass$pass"; [ "$t" = Q ] && [ "$d" != "$name" ] && abort "unexpected quarantine reference $d"; done < "$WORK/refs"
  done
  if [ -n "$hit" ]; then restore "$name" "$dino" "open after quarantine:$hit" && { KEPT=$((KEPT+1)); }; continue; fi
  # ---- 5. pass 1: archive identity of every file ----
  verify_hashes "$QUAR/$name"; vr=$?
  if [ $vr -ne 0 ]; then restore "$name" "$dino" "archive hash/identity check failed rc=$vr" && { KEPT=$((KEPT+1)); }; continue; fi
  # ---- 6. pass 2: unlink with progress ----
  unl=0; perr=""; CUR_MUT=0
  for x in $fis; do f=${x%%:*}; r=${x#*:}; ino=${r%%:*}
    if [ "$(stat -c %d.%i -- "$QUAR/$name/$f" 2>/dev/null)" != "$ino" ]; then perr="identity changed before unlink of $f"; break; fi
    CUR_MUT=1                                                                # from here on, any failure is PARTIAL, never KEEP
    if rm -f -- "$QUAR/$name/$f"; then unl=$((unl+1)); else perr="rm of $f returned $?"; break; fi
    if [ -e "$QUAR/$name/$f" ]; then perr="$f present again after rm"; break; fi
  done
  if [ -n "$perr" ]; then
    if [ $CUR_MUT = 0 ]; then restore "$name" "$dino" "$perr (no unlink attempted)" && { KEPT=$((KEPT+1)); }
    else echo "PARTIAL $path: $perr after $unl successful rm; remaining in $QUAR/$name: $(residue "$QUAR/$name")"; FAILED=$((FAILED+1)); CUR=""; fi
    continue
  fi
  if [ "$(stat -c %d.%i -- "$QUAR/$name" 2>/dev/null)" = "$dino" ] && rmdir -- "$QUAR/$name" && [ ! -e "$QUAR/$name" ]; then
    echo "DELETED $path kb=$k dir_id=$dino unlinked=$unl archive-sha-ok"; DONE=$((DONE+1)); FREED=$((FREED+k)); CUR=""
  else
    echo "PARTIAL $path: $unl files unlinked but rmdir failed; remaining in $QUAR/$name: $(residue "$QUAR/$name")"; FAILED=$((FAILED+1)); CUR=""
  fi
done < "$LIST_COPY"

if [ $QUAR_MADE = 1 ]; then
  if rmdir -- "$QUAR"; then echo "quarantine removed"; else echo "quarantine NOT removed: $(residue "$QUAR")"; FAILED=$((FAILED+1)); fi
fi
remaining=$(find "$CANON_BASE" -mindepth 1 -maxdepth 1 -type d -printf x 2>"$WORK/fe") && [ ! -s "$WORK/fe" ] || { echo "final inventory failed"; FAILED=$((FAILED+1)); }
echo "remaining_folders=${#remaining}"
if [ $FAILED -eq 0 ]; then summary OK; exit 0; else summary FAILURES; exit 1; fi

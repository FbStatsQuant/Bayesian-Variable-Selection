#!/bin/bash
# d29_test_harness.sh v5.1: NOTS-side ASSERTING test of d29_dbbackups_delete.sh v5.1 on FAKE trees in scratch (never touches ~/.codex or home).
# Usage: bash d29_test_harness.sh DIR   (DIR holds d29_dbbackups_delete.sh). Prints PASS/FAIL per assertion and "HARNESS RESULT: n pass, m fail"; exit 0 only if m = 0.
# Fault injection (Sol R3 F5, R4 F1) uses PATH shims for find / cat / rm / mkdir that act ONLY on one named target and are present ONLY in the runs that test them;
# the script under test is the reviewed file with only the location / expected-hash / count constants substituted (diff printed).
set -u
D=$1; NP=0; NF=0
ok()   { echo "PASS: $*"; NP=$((NP+1)); }
bad()  { echo "FAIL: $*"; NF=$((NF+1)); }
chk()  { if [ "$1" = "$2" ]; then ok "$3 (= $2)"; else bad "$3: got [$1] want [$2]"; fi; }
outset() { grep -E "^$1 " "$2" | awk '{print $2}' | sed 's#.*/##; s#:$##' | sort | tr '\n' ' '; }   # outset VERB OUTFILE -> sorted folder names
fsig() { ( cd "$1" 2>/dev/null && for f in logs_2.sqlite logs_2.sqlite-shm logs_2.sqlite-wal; do printf '%s:%s:%s ' "$f" "$(stat -c %d.%i "$f" 2>/dev/null)" "$(sha256sum "$f" 2>/dev/null | cut -c1-64)"; done ); }
now=$(date +%s)
mk() { local b=$1 n=$2 age=$3; mkdir "$b/$n"; head -c 49152 /dev/urandom > "$b/$n/logs_2.sqlite"; head -c 32768 /dev/urandom > "$b/$n/logs_2.sqlite-shm"; head -c 1000 /dev/urandom > "$b/$n/logs_2.sqlite-wal"
  touch -d @$((now-age)) "$b/$n"/* "$b/$n"; }
mklist() { local b=$1 l=$2 m=$3 n; shift 3
  printf 'path\tdu_kb\tnewest_mtime_epoch\tnewest_mtime_utc\tdir_mtime_utc\tn_files\tfiles(name:bytes)\n' > "$l"
  for n in "$@"; do printf '%s\t%s\t%s\tX\tX\t3\tlogs_2.sqlite:49152 logs_2.sqlite-shm:32768 logs_2.sqlite-wal:1000\n' "$b/$n" 100 "$(stat -c %Y "$b/$n/logs_2.sqlite")" >> "$l"; done
  ( cd "$b" && for n in "$@"; do find "$n" -type f -print0; done | sort -z | xargs -0 sha256sum ) > "$m"; }
mkcopy() { local root=$1 l=$2 m=$3 rows=$4 lines=$5 out=$6 R
  R=$(printf '%s' "$root/.codex/db-backups/" | sed 's#[/.]#\\&#g')
  R="$R" B="$root/.codex/db-backups" C="$root/.codex" Q="$root/quarantine" S="$(sha256sum "$l" | cut -c1-64)" SM="$(sha256sum "$m" | cut -c1-64)" RO="$rows" LI="$lines" \
  perl -pe 's{\Q\/home\/fb31\/\.codex\/db-backups\/\E}{$ENV{R}}g; s{^BASE=.*}{BASE=$ENV{B}}; s{^CODEX=.*}{CODEX=$ENV{C}}; s{^QUAR=.*}{QUAR=$ENV{Q}};
            s{^LIST_SHA_EXPECTED=.*}{LIST_SHA_EXPECTED=$ENV{S}}; s{^MANIFEST_SHA_EXPECTED=.*}{MANIFEST_SHA_EXPECTED=$ENV{SM}}; s{^ROWS_EXPECTED=.*}{ROWS_EXPECTED=$ENV{RO}}; s{^MANIFEST_LINES_EXPECTED=.*}{MANIFEST_LINES_EXPECTED=$ENV{LI}}' \
    "$D/d29_dbbackups_delete.sh" > "$out"
  echo "--- diff reviewed vs test copy ($out)"; diff "$D/d29_dbbackups_delete.sh" "$out"; }
run() { local o=$1; shift; "$@" > "$o" 2>&1; echo $?; }
show() { grep -v 'skipped helper' "$1"; }

# ---- shims (used only via an explicit PATH in the fault-injection runs) ----
SH=$D/shims; rm -rf -- "$SH"; mkdir -p "$SH"
cat > "$SH/find" <<'EOS'
#!/bin/bash
# silent failure of the fd scan of one pid: status 1, no output, no diagnostics
if [ -n "${SHIM_FIND_PID:-}" ] && [ "${1:-}" = "/proc/$SHIM_FIND_PID/fd/" ]; then exit 1; fi
exec /usr/bin/find "$@"
EOS
cat > "$SH/cat" <<'EOS'
#!/bin/bash
# the maps of one pid "vanish": ENOENT diagnostic, status 1
if [ -n "${SHIM_CAT_PID:-}" ] && [ "${!#}" = "/proc/$SHIM_CAT_PID/maps" ]; then echo "cat: /proc/$SHIM_CAT_PID/maps: No such file or directory" >&2; exit 1; fi
exec /usr/bin/cat "$@"
EOS
cat > "$SH/rm" <<'EOS'
#!/bin/bash
# after really removing the target, something recreates a file at the same path
last=${!#}
if [ -n "${SHIM_RM_TARGET:-}" ] && [ "$last" = "$SHIM_RM_TARGET" ]; then /usr/bin/rm "$@"; rc=$?; echo intruder > "$SHIM_RM_TARGET"; exit $rc; fi
exec /usr/bin/rm "$@"
EOS
cat > "$SH/mkdir" <<'EOS'
#!/bin/bash
# PRE: the target is created (with a marker) just before our mkdir -> EEXIST.  POST: our mkdir succeeds, then a file appears inside the reservation.
last=${!#}
if [ -n "${SHIM_MKDIR_TARGET:-}" ] && [ "$last" = "$SHIM_MKDIR_TARGET" ]; then
  case "${SHIM_MKDIR_MODE:-}" in
    PRE)  /usr/bin/mkdir "$SHIM_MKDIR_TARGET" && echo marker > "$SHIM_MKDIR_TARGET/marker"; exec /usr/bin/mkdir "$@";;
    POST) /usr/bin/mkdir "$@"; rc=$?; echo intruder > "$SHIM_MKDIR_TARGET/intruder"; exit $rc;;
  esac
fi
exec /usr/bin/mkdir "$@"
EOS
chmod 755 "$SH"/*

# ===== tree A =====
T=$D/test; rm -rf -- "$T"; mkdir -p "$T/.codex/db-backups"; chmod 700 "$T/.codex"; B=$T/.codex/db-backups; Q=$T/quarantine
mk $B sqlite-100-0 864000; mk $B sqlite-150-0 830000; mk $B sqlite-200-0 777600; mk $B sqlite-250-0 740000; mk $B sqlite-300-0 691200; mk $B sqlite-400-0 604800; mk $B sqlite-500-0 518400
mk $B sqlite-600-0 7200; mk $B sqlite-700-0 600; mk $B sqlite-800-0 300; mk $B sqlite-900-0 60
L=$T/list.tsv; M=$T/manifest.sha256
mklist $B $L $M sqlite-100-0 sqlite-150-0 sqlite-200-0 sqlite-250-0 sqlite-300-0 sqlite-400-0 sqlite-500-0 sqlite-600-0 sqlite-700-0
awk -F'\t' 'BEGIN{OFS="\t"} $1 ~ /sqlite-500-0$/ {$3=$3+5} {print}' $L > $L.t && mv $L.t $L                                    # 500: listed mtime wrong
sed -i 's/^[0-9a-f]\{64\}  sqlite-150-0\/logs_2.sqlite-wal$/0000000000000000000000000000000000000000000000000000000000000000  sqlite-150-0\/logs_2.sqlite-wal/' $M   # 150: archive mismatch
head -c 3000 /dev/urandom > $B/sqlite-400-0/logs_2.sqlite-wal; touch -d @$((now-604800)) $B/sqlite-400-0/logs_2.sqlite-wal $B/sqlite-400-0   # 400: size changed
sleep 900 9<"$B/sqlite-300-0/logs_2.sqlite" & H1=$!                                                                             # 300: open fd
bash -c 'cd "$1" && exec sleep 900' _ "$B/sqlite-250-0" & H2=$!                                                                 # 250: cwd inside
sleep 1
X=$T/x.sh; mkcopy $T $L $M 9 27 $X
sig150=$(fsig $B/sqlite-150-0); sig250=$(fsig $B/sqlite-250-0); sig300=$(fsig $B/sqlite-300-0)

echo "### T1 unknown argument";        rc=$(run $T/o1 bash $X $L $M --force); cat $T/o1; chk $rc 3 "T1 rc"
echo "### T2 tampered list";            cp $L $T/bad.tsv; echo >> $T/bad.tsv; rc=$(run $T/o2 bash $X $T/bad.tsv $M); cat $T/o2; chk $rc 3 "T2 rc"
echo "### T3 dry run";                  rc=$(run $T/o3 bash $X $L $M); show $T/o3; chk $rc 0 "T3 rc"
chk "$(outset WOULD-DELETE $T/o3)" "sqlite-100-0 sqlite-200-0 " "T3 would-delete set"; chk "$( [ -e $Q ] && echo yes || echo no)" no "T3 no quarantine created"
echo "### T4 stray symlink";            ln -s /tmp $B/stray; rc=$(run $T/o4 bash $X $L $M --yes); show $T/o4; rm $B/stray
chk $rc 3 "T4 rc"; chk "$(ls $B | wc -l)" 11 "T4 all folders present"; chk "$( [ -e $Q ] && echo yes || echo no)" no "T4 quarantine absent"
echo "### T5 non-dumpable foreign process must abort"
if command -v python3 >/dev/null; then
  python3 -c 'import ctypes,time; ctypes.CDLL(None).prctl(4,0,0,0,0); time.sleep(600)' & H5=$!; sleep 1
  rc=$(run $T/o5 bash $X $L $M); show $T/o5; kill $H5; wait $H5 2>/dev/null
  chk $rc 3 "T5 rc"; chk "$(grep -c 'is not inspectable' $T/o5)" 1 "T5 abort reason"
else bad "T5: no python3"; fi
echo "### T5b (R3 F5b) silent failure (status 1, no stderr) of the fd scan of the process holding 300 must abort"
rc=$(run $T/o5b env PATH="$SH:$PATH" SHIM_FIND_PID=$H1 bash $X $L $M --yes); show $T/o5b
chk $rc 3 "T5b rc"; chk "$(grep -c "open-file scan of live process /proc/$H1 failed: fd-scan status=1 class=bad" $T/o5b)" 1 "T5b abort reason"
chk "$(fsig $B/sqlite-300-0)" "$sig300" "T5b 300 intact"; chk "$(ls $B | wc -l)" 11 "T5b nothing deleted"; chk "$( [ -e $Q ] && echo yes || echo no)" no "T5b quarantine absent"
echo "### T5c (R4 F1) a VERIFIED helper (fd scan EACCES) whose maps vanishes (ENOENT) must abort, not be exempted"
HELPER=$(ps -u fb31 -o pid=,comm= | awk '$2=="(sd-pam)"{print $1; exit}')
if [ -n "$HELPER" ]; then
  rc=$(run $T/o5c env PATH="$SH:$PATH" SHIM_CAT_PID=$HELPER bash $X $L $M --yes); show $T/o5c
  chk $rc 3 "T5c rc"; chk "$(grep -c "^ABORT: maps of live process /proc/$HELPER vanished: fd-scan status=1 class=eperm" $T/o5c)" 1 "T5c abort reason (helper pid $HELPER)"
  chk "$(ls $B | wc -l)" 11 "T5c nothing deleted"; chk "$( [ -e $Q ] && echo yes || echo no)" no "T5c quarantine absent"
else bad "T5c: no (sd-pam) helper process found"; fi
echo "### T6 erase";                    rc=$(run $T/o6 bash $X $L $M --yes); show $T/o6
chk $rc 0 "T6 rc"; chk "$(outset DELETED $T/o6)" "sqlite-100-0 sqlite-200-0 " "T6 deleted set"; chk "$(outset RESTORED $T/o6)" "sqlite-150-0 " "T6 restored set"
chk "$(outset KEEP $T/o6)" "sqlite-250-0 sqlite-300-0 sqlite-400-0 sqlite-500-0 sqlite-600-0 sqlite-700-0 " "T6 kept set"
chk "$(fsig $B/sqlite-150-0)" "$sig150" "T6 150 restored intact (inodes+hashes)"
chk "$( [ -e $Q ] && echo yes || echo no)" no "T6 quarantine removed"; chk "$(ls $B | tr '\n' ' ')" "sqlite-150-0 sqlite-250-0 sqlite-300-0 sqlite-400-0 sqlite-500-0 sqlite-600-0 sqlite-700-0 sqlite-800-0 sqlite-900-0 " "T6 remaining"
echo "### T7 a folder eligible at start is opened DURING the run"
kill $H2; wait $H2 2>/dev/null
( sleep 8; exec 9<"$B/sqlite-250-0/logs_2.sqlite"; exec sleep 900 ) & H7=$!
rc=$(run $T/o7 bash $X $L $M --yes); show $T/o7
chk $rc 0 "T7 rc"; chk "$(sed -n '/^keep set before row 1/,/^[A-Z]/p' $T/o7 | grep -c 'sqlite-250-0')" 0 "T7 250 eligible at start"
chk "$(grep -cE '^(KEEP|RESTORED) .*sqlite-250-0.*open' $T/o7)" 1 "T7 250 kept because open"; chk "$(fsig $B/sqlite-250-0)" "$sig250" "T7 250 intact"; chk "$(outset DELETED $T/o7)" "" "T7 nothing deleted"
echo "### T7b a folder opened AFTER its quarantine move must be restored, not deleted"
kill $H7; wait $H7 2>/dev/null; sleep 1
( while [ ! -f "$Q/sqlite-250-0/logs_2.sqlite" ]; do sleep 0.05; done; exec 9<"$Q/sqlite-250-0/logs_2.sqlite"; exec sleep 900 ) & H7B=$!
rc=$(run $T/o7b bash $X $L $M --yes); show $T/o7b
chk $rc 0 "T7b rc"; chk "$(grep -cE '^RESTORED .*sqlite-250-0 \(open after quarantine' $T/o7b)" 1 "T7b 250 restored after post-move open"
chk "$(fsig $B/sqlite-250-0)" "$sig250" "T7b 250 back intact"; chk "$(outset DELETED $T/o7b)" "" "T7b nothing deleted"; chk "$( [ -e $Q ] && echo yes || echo no)" no "T7b quarantine removed"
echo "### T7c (R3 F5d) restore destination created just before the reservation: must NOT clobber; folder stays in quarantine; the foreign entry then makes the next row's scan abort (rc 3)"
rc=$(run $T/o7c env PATH="$SH:$PATH" SHIM_MKDIR_TARGET="$B/sqlite-150-0" SHIM_MKDIR_MODE=PRE bash $X $L $M --yes); show $T/o7c
chk $rc 3 "T7c rc"; chk "$(grep -c '^ABORT: structure: unexpected depth-2 entry f sqlite-150-0/marker' $T/o7c)" 1 "T7c next scan aborts on the foreign entry"; chk "$(grep -cE '^FAILED .*sqlite-150-0: not restored .*destination exists' $T/o7c)" 1 "T7c FAILED, not restored"
chk "$(ls $B/sqlite-150-0 | tr '\n' ' ')" "marker " "T7c recreated destination untouched"; chk "$(fsig $Q/sqlite-150-0)" "$sig150" "T7c 150 intact in quarantine"
rm -rf -- "$B/sqlite-150-0"; mv -T "$Q/sqlite-150-0" "$B/sqlite-150-0"; rmdir "$Q"; chk "$(fsig $B/sqlite-150-0)" "$sig150" "T7c manual put-back"
echo "### T7d (R3 F5d) a file appears inside the reservation before the rename: rename must fail, nothing clobbered; the next row's scan then aborts (rc 3)"
rc=$(run $T/o7d env PATH="$SH:$PATH" SHIM_MKDIR_TARGET="$B/sqlite-150-0" SHIM_MKDIR_MODE=POST bash $X $L $M --yes); show $T/o7d
chk $rc 3 "T7d rc"; chk "$(grep -c '^ABORT: structure: unexpected depth-2 entry f sqlite-150-0/intruder' $T/o7d)" 1 "T7d next scan aborts on the foreign entry"; chk "$(grep -cE '^FAILED .*sqlite-150-0: not restored .*rename onto reservation refused' $T/o7d)" 1 "T7d FAILED, not restored"
chk "$(ls $B/sqlite-150-0 | tr '\n' ' ')" "intruder " "T7d intruder untouched"; chk "$(fsig $Q/sqlite-150-0)" "$sig150" "T7d 150 intact in quarantine"
rm -rf -- "$B/sqlite-150-0"; mv -T "$Q/sqlite-150-0" "$B/sqlite-150-0"; rmdir "$Q"; chk "$(fsig $B/sqlite-150-0)" "$sig150" "T7d manual put-back"
echo "### T8 (R3 F5c) holds released; a file is recreated right after the first successful rm of 250: 250 must be PARTIAL (rc 1), 300 deleted"
kill $H1 $H7B; wait $H1 $H7B 2>/dev/null; sleep 1
rc=$(run $T/o8 env PATH="$SH:$PATH" SHIM_RM_TARGET="$Q/sqlite-250-0/logs_2.sqlite" bash $X $L $M --yes); show $T/o8
chk $rc 1 "T8 rc"; chk "$(outset DELETED $T/o8)" "sqlite-300-0 " "T8 deleted set"; chk "$(grep -cE '^PARTIAL .*sqlite-250-0: logs_2.sqlite present again after rm after 1 successful rm' $T/o8)" 1 "T8 250 PARTIAL"
chk "$(grep -cE '^(KEEP|RESTORED) .*sqlite-250-0' $T/o8)" 0 "T8 250 not reported as kept"; chk "$(ls $Q/sqlite-250-0 2>/dev/null | tr '\n' ' ')" "logs_2.sqlite logs_2.sqlite-shm logs_2.sqlite-wal " "T8 residue in quarantine"
rm -rf -- "$Q"
echo "### T9 rerun is idempotent";       rc=$(run $T/o9 bash $X $L $M --yes); chk $rc 0 "T9 rc"; chk "$(outset DELETED $T/o9)" "" "T9 nothing deleted"
rm -rf -- "$T"

# ===== tree B: all folders old; tie at the 3rd-newest value =====
T=$D/test2; rm -rf -- "$T"; mkdir -p "$T/.codex/db-backups"; chmod 700 "$T/.codex"; B=$T/.codex/db-backups
mk $B sqlite-1-0 864000; mk $B sqlite-2-0 691200; mk $B sqlite-3-0 691200; mk $B sqlite-4-0 648000; mk $B sqlite-5-0 604800
L=$T/list.tsv; M=$T/manifest.sha256; mklist $B $L $M sqlite-1-0 sqlite-2-0 sqlite-3-0 sqlite-4-0
X=$T/x.sh; mkcopy $T $L $M 4 12 $X
echo "### T10 old top-3 with a tie";     rc=$(run $T/o10 bash $X $L $M --yes); show $T/o10
chk $rc 0 "T10 rc"; chk "$(outset DELETED $T/o10)" "sqlite-1-0 " "T10 deleted set"; chk "$(outset KEEP $T/o10)" "sqlite-2-0 sqlite-3-0 sqlite-4-0 " "T10 kept (top3 incl. tie)"
rm -rf -- "$T" "$SH"
echo "### test trees and shims removed: $( [ -e $D/test ] || [ -e $D/test2 ] || [ -e $D/shims ] && echo NO || echo yes)"
echo "HARNESS RESULT: $NP pass, $NF fail"
[ $NF -eq 0 ]

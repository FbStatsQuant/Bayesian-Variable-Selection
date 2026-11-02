#!/bin/bash
# d31_backups_erase_remote.sh (ON NOTS via: ssh nots "MODE=dry|yes bash -s" < this): erase exactly the two archived tarballs in /home/fb31/backups
# (D31; Sol review review/SOL_REVIEW_D31_BACKUPS.md F1/F2), then rmdir the empty folder. Fails closed; prints one result line.
# Gates, all before any unlink: host loginx2 + user fb31; /home/fb31/backups is a real directory (no link) at its canonical place; it holds EXACTLY the
# two named regular, non-link files; both sha256 equal the archived values; a fail-closed /proc scan of every fb31 process on this node (fd, cwd, maps;
# unreadable only for the two strictly identified helpers, sshd and (sd-pam), as in the Sol-R5-accepted d29 executor) finds no reference to the folder.
# Residual (not provable from loginx2; D34 precedent): a process on another NFS client holding a file open. Files are archived and verified.
set -uo pipefail
MODE=${MODE:-dry}
cd / || exit 3
D=/home/fb31/backups
F1=Extreme_individual_pkgs_before_tau90_93_20261021.tar.gz; H1=c9d0f4614ea15cb70f78a2981d5b6e9584251b83c0fec189f96177927c2327d2
F2=Extreme_Joint_Sampler_before_b0005_15k3k_20261022.tar.gz; H2=c56bb68ccf6a5181ded7c4aff747cb920096f7d68989c17cc3655dec59b3ce9e
refuse() { echo "REFUSE: $*"; echo "RESULT NOT_ERASED"; exit 3; }
[ "$(hostname -s)" = loginx2 ] || refuse "host is not loginx2"
[ "$(id -un)" = fb31 ] || refuse "user is not fb31"
[ -d "$D" ] && [ ! -L "$D" ] || refuse "$D missing or a link"
[ "$(readlink -f -- "$D")" = "$(readlink -f -- /home/fb31)/backups" ] || refuse "$D not canonical"
ents=$(find "$D" -mindepth 1 -printf '%y %P\n' 2>&1) || refuse "listing failed: $ents"
[ "$(printf '%s\n' "$ents" | LC_ALL=C sort)" = "$(printf 'f %s\nf %s\n' "$F2" "$F1" | LC_ALL=C sort)" ] || refuse "folder content differs: [$ents]"
for x in "$F1:$H1" "$F2:$H2"; do f=${x%%:*}; h=${x#*:}
  [ -f "$D/$f" ] && [ ! -L "$D/$f" ] || refuse "$f not a regular file"
  got=$(sha256sum -- "$D/$f") || refuse "hash of $f failed"; [ "${got:0:64}" = "$h" ] || refuse "sha256 of $f differs from the archive"
done
echo "gates: content exact, both sha256 = archive"
# fail-closed open scan on this node
e1=$(mktemp) e2=$(mktemp); trap 'rm -f -- "$e1" "$e2"' EXIT
classify() { local rc=$1 f=$2 t a b
  if [ "$rc" = 0 ] && [ ! -s "$f" ]; then echo ok; return; fi
  [ -s "$f" ] || { echo bad; return; }; case "$rc" in 0|1) ;; *) echo bad; return;; esac
  read -r t a b <<< "$(awk '{t++} /No such file or directory/{a++} /Permission denied/{b++} END{print t+0, a+0, b+0}' "$f")"
  if [ "$t" -gt 0 ] && [ "$a" -eq "$t" ]; then echo enoent; elif [ "$t" -gt 0 ] && [ "$b" -eq "$t" ]; then echo eperm; else echo bad; fi; }
hits=0; skipped=""
for p in /proc/[0-9]*; do
  u=$(stat -c %U -- "$p" 2>/dev/null) || { [ -d "$p" ] && refuse "cannot stat live $p"; continue; }
  [ "$u" = fb31 ] || continue
  fo=$(find "$p/fd/" "$p/cwd" "$p/root" "$p/exe" -maxdepth 1 -type l -printf '%l\n' 2>"$e1"); frc=$?
  mo=$(cat -- "$p/maps" 2>"$e2"); mrc=$?
  # no pipe (Sol D31 R2: `printf | grep -q` under pipefail can report a real match as no match via SIGPIPE); pure bash substring test
  if [[ "$fo"$'\n'"$mo" == *"$D"* ]]; then hits=$((hits+1)); echo "OPEN: ${p#/proc/} references $D"; fi
  cf=$(classify $frc "$e1"); cm=$(classify $mrc "$e2")
  if [ "$cf" != ok ] || [ "$cm" != ok ]; then
    [ -d "$p" ] || continue
    { [ "$cf" = bad ] || [ "$cm" = bad ]; } && refuse "scan of live $p failed (fd $frc/$cf, maps $mrc/$cm)"
    [ "$cm" = enoent ] && refuse "maps of live $p vanished"
    if [ "$cf" = eperm ] || [ "$cm" = eperm ]; then
      c=$(cat "$p/comm" 2>/dev/null); pp=$(awk '/^PPid:/{print $2}' "$p/status" 2>/dev/null); pu=$(stat -c %U "/proc/$pp" 2>/dev/null)
      pc=$(cat "/proc/$pp/comm" 2>/dev/null); gpp=$(awk '/^PPid:/{print $2}' "/proc/$pp/status" 2>/dev/null)
      if [ "$c" = sshd ] && [ "$pc" = sshd ] && [ "$pu" = root ]; then skipped="$skipped ${p#/proc/}(sshd)"
      elif [ "$c" = "(sd-pam)" ] && [ "$pc" = systemd ] && [ "$pu" = fb31 ] && [ "$gpp" = 1 ]; then skipped="$skipped ${p#/proc/}(sd-pam)"
      else refuse "live $p (comm=$c) not inspectable"; fi
    fi
  fi
done
[ $hits -eq 0 ] || refuse "$hits process(es) reference $D"
echo "open scan: no reference on loginx2; skipped helpers:${skipped:- none}"
if [ "$MODE" != yes ]; then echo "RESULT DRY_RUN_OK (nothing erased)"; exit 0; fi
rm -- "$D/$F1" "$D/$F2" || { echo "RESULT PARTIAL rm failed; remaining: $(ls -A "$D" 2>&1)"; exit 1; }
rmdir -- "$D" || { echo "RESULT PARTIAL files removed, rmdir refused; remaining: $(ls -A "$D" 2>&1)"; exit 1; }
[ ! -e "$D" ] && echo "RESULT ERASED 2 files, folder removed" || { echo "RESULT PARTIAL folder still present"; exit 1; }

#!/usr/bin/env bash
# test_install_script.sh -- install_competitor_packages.sh guards and the offline route (PR #19 MINOR-1..3), on dummy
# packages only (nothing from CRAN; no network). Needs TMPDIR inside $HOME/SMC_Engineering_Department (department rule);
# otherwise the install part is skipped, since the script refuses any --dept outside the department.
#   tools/competitors/test_install_script.sh
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S="$here/install_competitor_packages.sh"
ROOT=$(realpath -m "$HOME/SMC_Engineering_Department")
: "${TMPDIR:?set TMPDIR (department tmp folder)}"
W=$(mktemp -d "$TMPDIR/wp5_install_XXXXXX"); trap 'rm -rf "$W"' EXIT
fail=0
expect() {   # expect <exit code> <label> -- command...
  local want=$1 label=$2; shift 3; local rc=0
  "$@" > "$W/out.txt" 2>&1 || rc=$?
  if [[ $rc == "$want" ]]; then echo "  ok   $label (exit $rc)"; else echo "  FAIL $label: exit $rc, want $want"; sed 's/^/       /' "$W/out.txt"; fail=1; fi
}
# 1. guards (exit 64), before anything runs
expect 64 "--dept /tmp/x refused" -- "$S" --no-modules --dept /tmp/x
expect 64 "--dept dept/../x refused" -- "$S" --no-modules --dept "$ROOT/../x"
expect 64 "--dept sibling prefix refused" -- "$S" --no-modules --dept "${ROOT}_x"
expect 64 "P1M_TEST_ROOT bypass removed" -- env P1M_TEST_ROOT="$HOME" "$S" --no-modules --dept "$HOME/not_dept"
expect 64 "--download-only outside refused" -- "$S" --no-modules --download-only /tmp/x
expect 64 "--from-dir outside refused" -- "$S" --no-modules --from-dir /tmp/x
case "$(realpath -m "$W")" in
  "$ROOT"/*) inside=1 ;; *) inside=0 ;;
esac
if [[ $inside == 0 ]]; then
  echo "  skip install tests: TMPDIR is not inside $ROOT"
  [[ $fail == 0 ]] && { echo "install script: OK (guards only)"; exit 0; } || { echo "install script: FAILED"; exit 1; }
fi
ln -s /tmp "$W/link_out"
expect 64 "symlink in the department pointing out refused" -- "$S" --no-modules --dept "$W/link_out/x"
# 2. --apply needs CONFIRM=yes (exit 65), even inside the department
expect 65 "--apply without CONFIRM=yes refused" -- env -u CONFIRM "$S" --no-modules --apply --dept "$W/dept"
[[ ! -e $W/dept/R ]] && echo "  ok   refused --apply wrote no library" || { echo "  FAIL refused --apply created $W/dept/R"; fail=1; }
# 3. offline route: aaadep imports zzzbase; alphabetical order would install aaadep first and fail (MINOR-2)
mk() {   # mk <name> <version> <imports or ""> <outdir>
  local d="$W/src/$1_$2"; mkdir -p "$d/R" "$4"
  printf 'Package: %s\nVersion: %s\nTitle: Dummy\nDescription: Dummy package for a test.\nLicense: GPL-2\nAuthor: t\nMaintainer: t <t@example.org>\n' "$1" "$2" > "$d/DESCRIPTION"
  [[ -n $3 ]] && printf 'Imports: %s\n' "$3" >> "$d/DESCRIPTION"
  if [[ -n $3 ]]; then printf 'import(%s)\nexport(f_%s)\n' "$3" "$1"; else printf 'export(f_%s)\n' "$1"; fi > "$d/NAMESPACE"
  printf 'f_%s <- function() "%s"\n' "$1" "$2" > "$d/R/f.R"
  (cd "$4" && nice -n 19 R CMD build --no-manual --no-build-vignettes "$d" > /dev/null 2>&1)
}
mk zzzbase 1.0 "" "$W/from1"; mk aaadep 0.1 zzzbase "$W/from1"; mk aaadep 0.2 zzzbase "$W/from2"
printf 'package\tmin_version\tsnapshot_test\tmethods\tapi\tnotes\naaadep\t0.1\t0.1\tt\tt\tt\n' > "$W/list1.tsv"
printf 'package\tmin_version\tsnapshot_test\tmethods\tapi\tnotes\naaadep\t0.2\t0.2\tt\tt\tt\n' > "$W/list2.tsv"
printf 'package\tmin_version\tsnapshot_test\tmethods\tapi\tnotes\naaadep\t0.3\t0.3\tt\tt\tt\n' > "$W/list3.tsv"
RV=$(Rscript --vanilla -e 'cat(as.character(getRversion()))'); L="$W/dept/R/$RV/library"
expect 0 "dry --resolve --from-dir plans the closure" -- "$S" --no-modules --dept "$W/dept" --list "$W/list1.tsv" --resolve --from-dir "$W/from1"
grep -q zzzbase "$W/out.txt" && echo "  ok   closure lists zzzbase" || { echo "  FAIL closure misses zzzbase"; fail=1; }
[[ ! -e $W/dept/R ]] && echo "  ok   dry run wrote no library" || { echo "  FAIL dry run created $W/dept/R"; fail=1; }
expect 0 "--apply --from-dir installs in dependency order" -- env CONFIRM=yes "$S" --no-modules --ncpus 1 --dept "$W/dept" --list "$W/list1.tsv" --apply --from-dir "$W/from1"
[[ -f $L/aaadep/DESCRIPTION && -f $L/zzzbase/DESCRIPTION ]] && echo "  ok   aaadep and zzzbase in the department library" || { echo "  FAIL not installed"; fail=1; }
lock="$W/dept/R/$RV/competitor_packages.lock.tsv"
if [[ -f $lock ]] && grep -q "^aaadep	0.1	$L" "$lock" && grep -q "^zzzbase	1.0	$L" "$lock"; then echo "  ok   lock file records the closure with LibPath"
else echo "  FAIL lock file"; cat "$lock" 2> /dev/null; fail=1; fi
ls "$W/from1"/PACKAGES* > /dev/null 2>&1 && { echo "  FAIL --from-dir was written to"; fail=1; } || echo "  ok   --from-dir left read-only"
# 4. below floor (MINOR-3): installed aaadep 0.1 < floor 0.2 is reinstalled, not dropped from the plan
expect 0 "--apply upgrades a below-floor package" -- env CONFIRM=yes "$S" --no-modules --ncpus 1 --dept "$W/dept" --list "$W/list2.tsv" --apply --from-dir "$W/from2"
grep -q "^Version: 0.2" "$L/aaadep/DESCRIPTION" && echo "  ok   aaadep now 0.2" || { echo "  FAIL aaadep not upgraded"; fail=1; }
expect 1 "--apply fails when the floor is not met after install" -- env CONFIRM=yes "$S" --no-modules --ncpus 1 --dept "$W/dept" --list "$W/list3.tsv" --apply --from-dir "$W/from2"
ls -d "$W/dept/tmp/"r-install-* > /dev/null 2>&1 && { echo "  FAIL R temp folder left behind"; fail=1; } || echo "  ok   R temp folder (under the dept) removed"
[[ $fail == 0 ]] && echo "install script: OK" || { echo "install script: FAILED"; exit 1; }

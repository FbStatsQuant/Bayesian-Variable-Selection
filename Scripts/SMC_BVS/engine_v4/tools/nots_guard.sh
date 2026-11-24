# nots_guard.sh -- sourced by the tools/nots_*.sh scripts (review PR26 B4; BUILD_COMMON path rules; WP5 brief item 4).
# nots_guard <build-dir>: refuses (exit 2) unless TMPDIR is set and both TMPDIR and the build directory lie under
# ~/SMC_Engineering_Department/ or /scratch/fb31/SMC_Engineering_Department/ (never /tmp: gcc's temporaries of the
# in-job build follow TMPDIR). Sets LOGDIR="$build/logs" (logs live inside the build directory).
nots_guard() {
  local b="${1:?build dir}" roots=("$HOME/SMC_Engineering_Department" "/scratch/fb31/SMC_Engineering_Department") ok_t=0 ok_b=0 r t
  if [[ -z "${TMPDIR:-}" ]]; then echo "$(basename "$0"): set TMPDIR (department tmp folder via the scratch link; never /tmp)" >&2; exit 2; fi
  t="$(realpath -m "$TMPDIR")"; b="$(realpath -m "$b")"
  for r in "${roots[@]}"; do
    r="$(realpath -m "$r")"
    [[ "$t" == "$r"/* ]] && ok_t=1
    [[ "$b" == "$r"/* ]] && ok_b=1
  done
  if [[ $ok_t -ne 1 ]]; then echo "$(basename "$0"): TMPDIR=$TMPDIR is not under ${roots[*]}" >&2; exit 2; fi
  if [[ $ok_b -ne 1 ]]; then echo "$(basename "$0"): build dir $b is not under ${roots[*]}" >&2; exit 2; fi
  mkdir -p "$TMPDIR" "$b/logs"; export TMPDIR; LOGDIR="$b/logs"
}

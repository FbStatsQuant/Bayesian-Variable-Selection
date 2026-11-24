#!/usr/bin/env bash
# install_competitor_packages.sh -- the R packages of the competitor harness (Sol F8), installed into the DEPARTMENT folder
# on NOTS. Run by the Engineering manager; builders run the dry run only (POLICIES §12: no installs by builders).
#
#   install_competitor_packages.sh                          dry run (default): plan + what the R library has already
#   install_competitor_packages.sh --resolve                dry run + the dependency closure and versions at the snapshot
#                                                           (needs network access to the snapshot repository)
#   CONFIRM=yes install_competitor_packages.sh --apply      install the missing / below-floor packages (and their missing
#                                                           dependencies); refused without CONFIRM=yes (manager only)
#   install_competitor_packages.sh --download-only DIR      fetch the source tarballs of the closure into DIR (e.g. on Owls,
#                                                           when NOTS cannot reach the repository); then on NOTS:
#   CONFIRM=yes install_competitor_packages.sh --apply --from-dir DIR
#                                                           install from those tarballs only (no network; DIR is indexed
#                                                           as a local repository, so dependencies install first)
# Options: --dept DIR (default <home>/SMC_Engineering_Department), --snapshot YYYY-MM-DD (default below), --no-modules
# (Owls / tests: use the R on PATH), --ncpus k (default 3), --list TSV (default competitor_packages.tsv; tests).
# Guards (PR #19 MINOR-1): --dept, --download-only DIR and --from-dir DIR must resolve (realpath, symlinks followed) inside
# <home>/SMC_Engineering_Department, else exit 64. <home> is the passwd home of the calling uid (getent), and $HOME must
# resolve to it, else exit 64 (PR #19 re-check R-1: HOME=... cannot move the guard). R's TMPDIR is a fresh folder under
# $DEPT/tmp with --apply, else under <home>/SMC_Engineering_Department/tmp (a dry run creates no folder in $DEPT, R-2);
# it is removed on exit. R runs
# without the user library (R_LIBS_USER unset, .libPaths = target library + the R installation's own libraries).
#
# Pinning: every package this script installs comes from ONE dated CRAN snapshot (Posit Package Manager, source packages).
# Dependencies already present in the R installation's own library are used as they are. After an install, EVERY package
# of the closure of the competitor list (installed here or found in the R installation) is written to
#   $DEPT/R/<R version>/competitor_packages.lock.tsv   (package, version, LibPath, built, MD5 of DESCRIPTION)
# and the competitor jobs use  R_LIBS_USER=$DEPT/R/<R version>/library  ahead of the module's own library.
# The list and the APIs the harness uses: competitor_packages.tsv (min_version = the API floor the harness needs).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# the department root comes from the passwd database, never from the environment alone
REAL_HOME=$(getent passwd "$(id -u)" | cut -d: -f6)
[[ -n $REAL_HOME && -d $REAL_HOME ]] || { echo "refusing: no passwd home for uid $(id -u)" >&2; exit 64; }
[[ $(realpath -m "${HOME:-}") == $(realpath -m "$REAL_HOME") ]] || {
  echo "refusing: \$HOME (${HOME:-unset}) is not the passwd home of uid $(id -u) ($REAL_HOME)" >&2; exit 64; }
DEPT="$REAL_HOME/SMC_Engineering_Department"; SNAPSHOT="2026-11-02"; MODE=dry; RESOLVE=0; FROM=""; DL=""; MODULES=1; NCPUS=3
LIST="$here/competitor_packages.tsv"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) MODE=apply ;; --resolve) RESOLVE=1 ;;
    --from-dir|--download-only|--dept)   # a path value, never empty
      [[ $# -ge 2 && -n $2 ]] || { echo "$1 needs a non-empty DIR" >&2; exit 2; }
      case "$1" in --from-dir) FROM="$2" ;; --download-only) MODE=download; DL="$2" ;; --dept) DEPT="$2" ;; esac; shift ;; --snapshot) SNAPSHOT="$2"; shift ;; --no-modules) MODULES=0 ;; --ncpus) NCPUS="$2"; shift ;;
    --list) LIST="$2"; shift ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac; shift
done
[[ $SNAPSHOT =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || { echo "bad --snapshot $SNAPSHOT" >&2; exit 2; }
[[ $NCPUS =~ ^[1-3]$ ]] || { echo "bad --ncpus $NCPUS (1..3)" >&2; exit 2; }
[[ -f $LIST ]] || { echo "no package list $LIST" >&2; exit 2; }
ROOT=$(realpath -m "$REAL_HOME/SMC_Engineering_Department")
inside_dept() {   # $1 resolves (symlinks followed) to the department folder or below it
  local p; p=$(realpath -m "$1"); [[ $p == "$ROOT" || $p == "$ROOT"/* ]]; }
DEPT=$(realpath -m "$DEPT")
inside_dept "$DEPT" || { echo "refusing: --dept $DEPT is outside the department folder $ROOT" >&2; exit 64; }
if [[ -n $DL ]]; then DL=$(realpath -m "$DL"); inside_dept "$DL" || { echo "refusing: --download-only $DL is outside $ROOT" >&2; exit 64; }; fi
if [[ -n $FROM ]]; then
  FROM=$(realpath -m "$FROM"); inside_dept "$FROM" || { echo "refusing: --from-dir $FROM is outside $ROOT" >&2; exit 64; }
  [[ -d $FROM ]] || { echo "no such directory: --from-dir $FROM" >&2; exit 2; }
fi
if [[ $MODE == apply && ${CONFIRM:-} != yes ]]; then
  echo "refusing: --apply installs into $DEPT; the Engineering manager runs it with CONFIRM=yes (run the dry run first)" >&2; exit 65
fi
# R's temporary files (package builds) stay in the department folder: never /tmp
if [[ $MODE == apply ]]; then TBASE="$DEPT/tmp"; else TBASE="$ROOT/tmp"; fi   # dry / download: nothing created in $DEPT
mkdir -p "$TBASE"
RTMP=$(mktemp -d "$TBASE/r-install-$(date +%Y%m%d)-XXXXXX"); trap 'rm -rf "$RTMP"' EXIT
export TMPDIR="$RTMP" TMP="$RTMP" TEMP="$RTMP"
if [[ $MODULES == 1 ]]; then   # NOTS toolchain (env_scale.sh of W3-SCALE / G0): GCC 14.3.0, R 4.5.2
  set +u
  type module > /dev/null 2>&1 || source /etc/profile.d/modules.sh 2> /dev/null || source /usr/share/lmod/lmod/init/bash
  module use /opt/apps/modules/Core; module purge; module load GCC/14.3.0 R/4.5.2
  set -u
fi
command -v Rscript > /dev/null || { echo "FATAL: no Rscript" >&2; exit 66; }
# no user library (MINOR-3): R then sees the target library + the R installation's own (.Library.site from the module's
# R_LIBS_SITE, and .Library); the R code below also resets .libPaths() and prints them
unset R_LIBS R_LIBS_USER
RVER=$(Rscript --vanilla -e 'cat(as.character(getRversion()))')
LIB="$DEPT/R/$RVER/library"
REPO="https://packagemanager.posit.co/cran/$SNAPSHOT"
echo "== mode: $MODE   R $RVER ($(command -v Rscript))   target library: $LIB"
echo "== repository (source, snapshot $SNAPSHOT): $REPO"
[[ -n $FROM ]] && echo "== from local tarballs: $FROM (no network)"
if [[ $MODE == apply ]]; then mkdir -p "$LIB"; fi
export P1M_LIB="$LIB" P1M_REPO="$REPO" P1M_MODE="$MODE" P1M_RESOLVE="$RESOLVE" P1M_FROM="$FROM" P1M_DL="$DL" P1M_NCPUS="$NCPUS"
export P1M_LIST="$LIST"
MAKEFLAGS="-j$NCPUS" nice -n 19 Rscript --vanilla - <<'RS'
lib <- Sys.getenv("P1M_LIB"); repo <- Sys.getenv("P1M_REPO"); mode <- Sys.getenv("P1M_MODE")
from <- Sys.getenv("P1M_FROM"); dl <- Sys.getenv("P1M_DL")
ncpus <- as.integer(Sys.getenv("P1M_NCPUS")); resolve <- Sys.getenv("P1M_RESOLVE") == "1"
spec <- utils::read.delim(Sys.getenv("P1M_LIST"), stringsAsFactors = FALSE, colClasses = "character")
# only the target library and the R installation's own libraries (site + base); the user library ~/R/... is excluded
.libPaths(if (dir.exists(lib)) lib else character(0))
cat("== library paths:", paste(.libPaths(), collapse = " : "), "\n")
ip <- utils::installed.packages(lib.loc = .libPaths())
have <- function(p) p %in% rownames(ip)
floor_ok <- function(ipm, p, v) p %in% rownames(ipm) && utils::compareVersion(ipm[p, "Version"], v) >= 0
cat(sprintf("%-10s %-10s %-10s %-12s %s\n", "package", "min", "snapshot", "installed", "where"))
missing <- character(0)   # absent OR below its API floor: both are (re)installed
for (i in seq_len(nrow(spec))) {
  p <- spec$package[i]
  v <- if (have(p)) ip[p, "Version"] else "-"
  ok <- floor_ok(ip, p, spec$min_version[i])
  if (!ok) missing <- c(missing, p)
  cat(sprintf("%-10s %-10s %-10s %-12s %s\n", p, spec$min_version[i], spec[[3]][i], v,
              if (ok) ip[p, "LibPath"] else if (have(p)) "BELOW FLOOR" else "MISSING"))
}
cat("== to install:", if (length(missing)) paste(missing, collapse = ", ") else "nothing", "\n")
closure <- function(db, pkgs) {
  if (!length(pkgs)) return(character(0))
  deps <- tools::package_dependencies(pkgs, db = db, which = c("Depends", "Imports", "LinkingTo"), recursive = TRUE)
  all <- unique(c(pkgs, unlist(deps)))
  base <- rownames(utils::installed.packages(priority = "base"))
  setdiff(all, base)
}
# the source repository: the dated snapshot, or DIR indexed as a local repository (PR #19 MINOR-2: install.packages then
# resolves the dependency order exactly as online, e.g. bigmemory and BH before biglasso)
contrib <- NULL
if (nzchar(from)) {   # index a symlink copy of DIR in R's temp folder: DIR itself is only read
  idx <- file.path(tempdir(), "from_dir_repo"); dir.create(idx)
  tb <- list.files(from, pattern = "\\.tar\\.gz$", full.names = TRUE)
  if (!length(tb)) stop("--from-dir: no source tarballs in ", from)
  file.symlink(normalizePath(tb), file.path(idx, basename(tb)))
  tools::write_PACKAGES(idx, type = "source")
  contrib <- paste0("file://", normalizePath(idx))
  cat("== indexed", length(tb), "tarballs of", from, "as a local repository\n")
}
need <- missing
if (resolve || mode %in% c("download", "apply")) {
  ap <- if (is.null(contrib)) utils::available.packages(repos = repo, type = "source")
        else utils::available.packages(contriburl = contrib, type = "source")
  absent <- setdiff(missing, rownames(ap))
  if (length(absent)) cat("WARNING: not in the source repository:", paste(absent, collapse = ", "), "\n")
  cl <- closure(ap, intersect(missing, rownames(ap)))
  need <- union(missing, cl[!vapply(cl, have, TRUE)])   # below-floor top-level packages stay in `need`
  cat("== planned install (closure at the source, not yet installed or below floor):\n")
  if (length(need)) print(ap[intersect(need, rownames(ap)), c("Version"), drop = FALSE]) else cat("   none\n")
}
if (mode == "dry") { cat("== dry run: nothing installed\n"); quit(save = "no", status = 0) }
if (mode == "download") {
  dir.create(dl, recursive = TRUE, showWarnings = FALSE)
  utils::download.packages(need, destdir = dl, repos = repo, type = "source")
  cat("== downloaded", length(need), "source packages to", dl, "\n"); quit(save = "no", status = 0)
}
# apply
if (length(need)) {
  if (!is.null(contrib)) {
    utils::install.packages(need, lib = lib, contriburl = contrib, type = "source", Ncpus = ncpus, dependencies = NA)
  } else {
    utils::install.packages(need, lib = lib, repos = repo, type = "source", Ncpus = ncpus, dependencies = NA)
  }
}
.libPaths(lib)
ip2 <- utils::installed.packages(lib.loc = .libPaths())
bad <- character(0)
for (i in seq_len(nrow(spec)))
  if (!floor_ok(ip2, spec$package[i], spec$min_version[i])) bad <- c(bad, spec$package[i])
# lock file: every package of the installed closure of the competitor list, with where it was found
rows <- sort(intersect(closure(ip2, intersect(spec$package, rownames(ip2))), rownames(ip2)))
lock <- file.path(dirname(lib), "competitor_packages.lock.tsv")
desc_md5 <- vapply(rows, function(p) unname(tools::md5sum(file.path(ip2[p, "LibPath"], p, "DESCRIPTION"))), "")
utils::write.table(data.frame(package = rows, version = ip2[rows, "Version"], libpath = ip2[rows, "LibPath"],
                              built = ip2[rows, "Built"], description_md5 = desc_md5),
                   lock, sep = "\t", quote = FALSE, row.names = FALSE)
cat("== lock file:", lock, "(", length(rows), "packages )\n")
if (length(bad)) { cat("FAILED (missing or below floor after install):", paste(bad, collapse = ", "), "\n"); quit(save = "no", status = 1) }
for (p in spec$package) suppressPackageStartupMessages(library(p, lib.loc = .libPaths(), character.only = TRUE))
cat("== all competitor packages load, at or above their floors\n")
RS

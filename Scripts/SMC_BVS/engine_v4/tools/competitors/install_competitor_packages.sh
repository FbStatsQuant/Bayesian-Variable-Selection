#!/usr/bin/env bash
# install_competitor_packages.sh -- the R packages of the competitor harness (Sol F8), installed into the DEPARTMENT folder
# on NOTS. Run by the Engineering manager; builders run the dry run only (POLICIES §12: no installs by builders).
#
#   install_competitor_packages.sh                          dry run (default): plan + what the R library has already
#   install_competitor_packages.sh --resolve                dry run + the dependency closure and versions at the snapshot
#                                                           (needs network access to the snapshot repository)
#   install_competitor_packages.sh --apply                  install the missing packages (and their missing dependencies)
#   install_competitor_packages.sh --download-only DIR      fetch the source tarballs of the closure into DIR (e.g. on Owls,
#                                                           when NOTS cannot reach the repository); then on NOTS:
#   install_competitor_packages.sh --apply --from-dir DIR   install from those tarballs only (no network)
# Options: --dept DIR (default $HOME/SMC_Engineering_Department), --snapshot YYYY-MM-DD (default below), --no-modules
# (Owls / tests: use the R on PATH), --ncpus k (default 3).
#
# Pinning: every version comes from ONE dated CRAN snapshot (Posit Package Manager, source packages), so the whole
# dependency closure is reproducible. After an install the exact versions are written to
#   $DEPT/R/<R version>/competitor_packages.lock.tsv   (package, version, built, MD5 of DESCRIPTION)
# and the competitor jobs use  R_LIBS_USER=$DEPT/R/<R version>/library  ahead of the module's own library.
# The list and the APIs the harness uses: competitor_packages.tsv (min_version = the API floor the harness needs).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPT="$HOME/SMC_Engineering_Department"; SNAPSHOT="2026-11-02"; MODE=dry; RESOLVE=0; FROM=""; DL=""; MODULES=1; NCPUS=3
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) MODE=apply ;; --resolve) RESOLVE=1 ;; --from-dir) FROM="$2"; shift ;; --download-only) MODE=download; DL="$2"; shift ;;
    --dept) DEPT="$2"; shift ;; --snapshot) SNAPSHOT="$2"; shift ;; --no-modules) MODULES=0 ;; --ncpus) NCPUS="$2"; shift ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac; shift
done
[[ $SNAPSHOT =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || { echo "bad --snapshot $SNAPSHOT" >&2; exit 2; }
DEPT=$(realpath -m "$DEPT")
ROOT=$(realpath -m "$HOME/SMC_Engineering_Department")
[[ $DEPT == "$ROOT" || $DEPT == "$ROOT"/* || ( -n ${P1M_TEST_ROOT:-} && $DEPT == $(realpath -m "$P1M_TEST_ROOT")/* ) ]] || {
  echo "refusing: $DEPT is outside the department folder" >&2; exit 64; }
if [[ $MODULES == 1 ]]; then   # NOTS toolchain (env_scale.sh of W3-SCALE / G0): GCC 14.3.0, R 4.5.2
  set +u
  type module > /dev/null 2>&1 || source /etc/profile.d/modules.sh 2> /dev/null || source /usr/share/lmod/lmod/init/bash
  module use /opt/apps/modules/Core; module purge; module load GCC/14.3.0 R/4.5.2
  set -u
fi
command -v Rscript > /dev/null || { echo "FATAL: no Rscript" >&2; exit 66; }
RVER=$(Rscript --vanilla -e 'cat(as.character(getRversion()))')
LIB="$DEPT/R/$RVER/library"
REPO="https://packagemanager.posit.co/cran/$SNAPSHOT"
PKGS=$(awk -F'\t' 'NR > 1 {print $1}' "$here/competitor_packages.tsv" | paste -sd, -)
echo "== mode: $MODE   R $RVER ($(command -v Rscript))   target library: $LIB"
echo "== repository (source, snapshot $SNAPSHOT): $REPO"
[[ -n $FROM ]] && echo "== from local tarballs: $FROM (no network)"
if [[ $MODE == apply ]]; then mkdir -p "$LIB"; fi
export P1M_LIB="$LIB" P1M_REPO="$REPO" P1M_PKGS="$PKGS" P1M_MODE="$MODE" P1M_RESOLVE="$RESOLVE" P1M_FROM="$FROM" P1M_DL="$DL" P1M_NCPUS="$NCPUS"
export P1M_LIST="$here/competitor_packages.tsv"
MAKEFLAGS="-j$NCPUS" nice -n 19 Rscript --vanilla - <<'RS'
lib <- Sys.getenv("P1M_LIB"); repo <- Sys.getenv("P1M_REPO"); mode <- Sys.getenv("P1M_MODE")
pk <- strsplit(Sys.getenv("P1M_PKGS"), ",")[[1]]; from <- Sys.getenv("P1M_FROM"); dl <- Sys.getenv("P1M_DL")
ncpus <- as.integer(Sys.getenv("P1M_NCPUS")); resolve <- Sys.getenv("P1M_RESOLVE") == "1"
spec <- utils::read.delim(Sys.getenv("P1M_LIST"), stringsAsFactors = FALSE, colClasses = "character")
paths <- unique(c(if (dir.exists(lib)) lib, .libPaths()))
ip <- utils::installed.packages(lib.loc = paths)
have <- function(p) p %in% rownames(ip)
cat(sprintf("%-10s %-10s %-10s %-12s %s\n", "package", "min", "snapshot", "installed", "where"))
missing <- character(0)
for (i in seq_len(nrow(spec))) {
  p <- spec$package[i]
  v <- if (have(p)) ip[p, "Version"] else "-"
  ok <- have(p) && utils::compareVersion(v, spec$min_version[i]) >= 0
  if (!ok) missing <- c(missing, p)
  cat(sprintf("%-10s %-10s %-10s %-12s %s\n", p, spec$min_version[i], spec[[3]][i], v,
              if (have(p)) ip[p, "LibPath"] else if (ok) "" else "MISSING / too old"))
}
cat("== to install:", if (length(missing)) paste(missing, collapse = ", ") else "nothing", "\n")
closure <- function(ap, pkgs) {
  deps <- tools::package_dependencies(pkgs, db = ap, which = c("Depends", "Imports", "LinkingTo"), recursive = TRUE)
  all <- unique(c(pkgs, unlist(deps)))
  base <- rownames(utils::installed.packages(priority = "base"))
  setdiff(all, base)
}
if (resolve || mode %in% c("download", "apply") && !nzchar(from)) {
  ap <- utils::available.packages(repos = repo, type = "source")
  cl <- closure(ap, missing)
  need <- cl[!vapply(cl, have, TRUE)]
  cat("== closure at the snapshot (not yet installed):\n")
  if (length(need)) print(ap[need, c("Version"), drop = FALSE]) else cat("   none\n")
} else need <- missing
if (mode == "dry") { cat("== dry run: nothing installed\n"); quit(save = "no", status = 0) }
if (mode == "download") {
  dir.create(dl, recursive = TRUE, showWarnings = FALSE)
  utils::download.packages(need, destdir = dl, repos = repo, type = "source")
  cat("== downloaded", length(need), "source packages to", dl, "\n"); quit(save = "no", status = 0)
}
# apply
if (length(need)) {
  if (nzchar(from)) {
    tb <- list.files(from, pattern = "\\.tar\\.gz$", full.names = TRUE)
    utils::install.packages(tb, lib = lib, repos = NULL, type = "source", Ncpus = ncpus)
  } else {
    utils::install.packages(need, lib = lib, repos = repo, type = "source", Ncpus = ncpus, dependencies = NA)
  }
}
ip2 <- utils::installed.packages(lib.loc = c(lib, .libPaths()))
bad <- spec$package[!(spec$package %in% rownames(ip2))]
lock <- file.path(dirname(lib), "competitor_packages.lock.tsv")
rows <- rownames(ip2)[ip2[, "LibPath"] == lib]
desc_md5 <- vapply(rows, function(p) unname(tools::md5sum(file.path(lib, p, "DESCRIPTION"))), "")
utils::write.table(data.frame(package = rows, version = ip2[rows, "Version"], built = ip2[rows, "Built"], description_md5 = desc_md5),
                   lock, sep = "\t", quote = FALSE, row.names = FALSE)
cat("== lock file:", lock, "\n")
if (length(bad)) { cat("FAILED to install:", paste(bad, collapse = ", "), "\n"); quit(save = "no", status = 1) }
for (p in spec$package) suppressPackageStartupMessages(library(p, lib.loc = c(lib, .libPaths()), character.only = TRUE))
cat("== all competitor packages load\n")
RS

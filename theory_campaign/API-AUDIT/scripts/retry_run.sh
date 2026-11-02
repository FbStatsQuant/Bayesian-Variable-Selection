#!/usr/bin/env bash
# Retry owls_run until it is not REFUSED (exit 75); never bypasses the policy. Usage: retry_run.sh <j> <cmd...>
J=$1; shift
while true; do
  ~/.config/bvs-hq/owls/owls_run -j "$J" -- "$@"; rc=$?
  [ $rc -ne 75 ] && exit $rc
  sleep 30
done

#!/usr/bin/env bash
# helper (local): run a command on NOTS trying the three login nodes (the `nots` alias node .48 has been unreachable at times)
for h in 10.226.96.47 10.226.96.46 10.226.96.48; do
  ssh -o HostName=$h -o ConnectTimeout=15 nots "$@" && exit 0
  rc=$?; [ $rc -ne 255 ] && exit $rc
done; exit 255

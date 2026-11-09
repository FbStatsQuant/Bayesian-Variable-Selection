#!/usr/bin/env bash
# helper (local): scp with login-node fallback; args as for scp (remote side written as nots:PATH)
for h in 10.226.96.47 10.226.96.46 10.226.96.48; do
  scp -q -o HostName=$h -o ConnectTimeout=15 "$@" && exit 0
done; exit 255

#!/usr/bin/env bash
if [ "$1" = "--version" ]; then echo "time (GNU Time) 1.9"; exit 0; fi
[ "$1" = "-f" ] && [ "$3" = "-o" ] || exit 1
printf '0.01\t123\n' > "$4"

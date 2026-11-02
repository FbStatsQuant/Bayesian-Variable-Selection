#!/bin/bash
# One definition shared by cleanup and closure/resubmission checks.
stale_find() {
  find "$@" -depth \( -type d -name '*.lock' -o -type f -name '*.tmp*' \) -print
}

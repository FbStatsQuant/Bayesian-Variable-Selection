#!/bin/bash
# d29_upload_and_test.sh OUTFILE : (laptop, Git Bash) upload the delete script + harness to the NOTS scratch run folder over ONE ssh and run the harness there.
# Output (hashes, harness transcript, harness exit status) goes to OUTFILE. Touches nothing outside /scratch/fb31/New_Campaign/runs/ops4_d29 on NOTS.
set -u
OUT=${1:?outfile}
S=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold
D=/scratch/fb31/New_Campaign/runs/ops4_d29
sha256sum "$S/d29_dbbackups_delete.sh" "$S/d29_test_harness.sh" > "$OUT"
tar -C "$S" -cf - d29_dbbackups_delete.sh d29_test_harness.sh | MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots \
  "cd $D && tar -xf - && sha256sum d29_dbbackups_delete.sh d29_test_harness.sh ops4_dbbackups_delete_list.tsv archive_manifest.sha256 && echo === && timeout 2700 bash d29_test_harness.sh $D 2>&1; echo harness_rc=\$?" >> "$OUT" 2>&1
echo "ssh_rc=$?" >> "$OUT"
grep -E '^(FAIL|HARNESS|harness_rc|ssh_rc)' "$OUT"

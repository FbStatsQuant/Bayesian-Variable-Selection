#!/bin/bash
# f3_delete_chain.sh : (laptop; detached via detach_run.sh) run the Sol-accepted (R2 ACCEPT) F3 dev+prod scratch deletion
# ops/scaffold/f3_delete_remote_v2.sh detached on NOTS (control lane). ACCEPT_SFTP = the HQ D79-accepted pinned sftp-server (pid:starttime); a pin
# matches nothing if that process has ended. Output ops/evidence/ops8_f3_delete.txt; status line in ops8_f3_delete_chain.txt.
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence
echo "start $(date -u +%FT%TZ)" > $E/ops8_f3_delete_chain.txt
NOTS_SSH_LANE=control bash $S/remote_bg.sh f3_delete_$(date -u +%Y%m%dT%H%M%SZ) $S/f3_delete_remote_v2.sh $E/ops8_f3_delete.txt ACCEPT_SFTP=3742644:559291281
echo "delete_bg_rc=$?" >> $E/ops8_f3_delete_chain.txt
grep -q '^F3_DELETE_DONE' $E/ops8_f3_delete.txt && echo "CHAIN DONE $(date -u +%FT%TZ)" >> $E/ops8_f3_delete_chain.txt || echo "CHAIN STOP $(date -u +%FT%TZ)" >> $E/ops8_f3_delete_chain.txt
